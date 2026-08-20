from __future__ import annotations

import base64
import json
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "staging"
WXR = ROOT / "camden-concreting-import.xml"
WP_NS = "http://wordpress.org/export/1.2/"
NS = {"wp": WP_NS}


def text(element: ET.Element, tag: str) -> str:
    child = element.find(tag, NS)
    return (child.text or "") if child is not None else ""


def query(sql: str) -> list[list[str]]:
    command = [
        "docker",
        "compose",
        "-f",
        "docker-compose.yml",
        "exec",
        "-T",
        "database",
        "mariadb",
        "--skip-ssl",
        "-ucamden_smoke",
        "-pdisposable-local-only",
        "camden_smoke",
        "-N",
        "-B",
        "-e",
        sql,
    ]
    completed = subprocess.run(command, cwd=STAGING, check=True, capture_output=True, text=True)
    return [line.split("\t") for line in completed.stdout.splitlines() if line]


def walk_images(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        settings = value.get("settings")
        if isinstance(settings, dict):
            image = settings.get("image")
            if isinstance(image, dict) and (image.get("id") or image.get("url")):
                yield image
        for child in value.values():
            yield from walk_images(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_images(child)


def main() -> int:
    root = ET.parse(WXR).getroot()
    expected: dict[int, dict[str, Any]] = {}
    expected_nav: dict[int, dict[str, str]] = {}
    for item in root.find("channel").findall("item"):
        post_id = int(text(item, "wp:post_id"))
        post_type = text(item, "wp:post_type")
        expected[post_id] = {
            "type": post_type,
            "status": text(item, "wp:status"),
            "slug": text(item, "wp:post_name"),
            "parent": int(text(item, "wp:post_parent") or 0),
            "title": text(item, "title"),
        }
        if post_type == "nav_menu_item":
            meta: dict[str, str] = {}
            for postmeta in item.findall("wp:postmeta", NS):
                meta[text(postmeta, "wp:meta_key")] = text(postmeta, "wp:meta_value")
            expected_nav[post_id] = {
                "parent": meta.get("_menu_item_menu_item_parent", "0"),
                "url": meta.get("_menu_item_url", ""),
                "object_id": meta.get("_menu_item_object_id", ""),
                "item_type": meta.get("_menu_item_type", ""),
            }

    post_rows = query(
        "SELECT ID, post_type, post_status, post_name, post_parent, post_title "
        "FROM wp_posts ORDER BY ID;"
    )
    actual = {
        int(row[0]): {
            "type": row[1],
            "status": row[2],
            "slug": row[3],
            "parent": int(row[4]),
            "title": row[5],
        }
        for row in post_rows
    }

    failures: list[str] = []
    importer_normalizations: list[dict[str, Any]] = []
    for post_id, wanted in expected.items():
        got = actual.get(post_id)
        if got is None:
            failures.append(f"missing imported post ID {post_id}")
        elif wanted["type"] == "nav_menu_item":
            # WordPress rebuilds nav-menu post slugs/titles/parents from the linked
            # object. Menu integrity is checked below using menu-item metadata and
            # term relationships, which are the authoritative hierarchy fields.
            if (got["type"], got["status"]) != (wanted["type"], wanted["status"]):
                failures.append(f"post ID {post_id} type/status mismatch: expected {wanted!r}; got {got!r}")
        elif wanted["type"] == "elementor_library":
            # A locally generated Default Kit can force WordPress to suffix the
            # imported slug. The ID, type, status, title and active-kit option are
            # the fields that control Elementor. Record the normalization without
            # treating it as attachment or hierarchy corruption.
            stable_fields = ("type", "status", "parent", "title")
            if any(got[field] != wanted[field] for field in stable_fields):
                failures.append(f"post ID {post_id} mismatch: expected {wanted!r}; got {got!r}")
            elif got["slug"] != wanted["slug"]:
                importer_normalizations.append(
                    {"post_id": post_id, "field": "post_name", "expected": wanted["slug"], "actual": got["slug"]}
                )
        elif got != wanted:
            failures.append(f"post ID {post_id} mismatch: expected {wanted!r}; got {got!r}")

    allowed_extra = {4}
    extra_ids = sorted(set(actual) - set(expected) - allowed_extra)
    if extra_ids:
        failures.append(f"unexpected wp_posts IDs: {extra_ids}")

    expected_type_counts = Counter(record["type"] for record in expected.values())
    imported_actual = {post_id: actual[post_id] for post_id in expected if post_id in actual}
    actual_type_counts = Counter(record["type"] for record in imported_actual.values())
    if actual_type_counts != expected_type_counts:
        failures.append(
            f"post type counts differ: expected {dict(expected_type_counts)}; got {dict(actual_type_counts)}"
        )

    page_rows = [record for record in imported_actual.values() if record["type"] == "page"]
    page_statuses = Counter(record["status"] for record in page_rows)
    if page_statuses != Counter({"draft": 135, "publish": 21}):
        failures.append(f"page status split mismatch: {dict(page_statuses)}")

    hub = actual.get(1502)
    if hub is None or (hub["type"], hub["status"], hub["slug"], hub["parent"]) != (
        "page",
        "draft",
        "guides",
        0,
    ):
        failures.append(f"guide hub mismatch: {hub!r}")
    guide_children = [
        record
        for post_id, record in imported_actual.items()
        if record["type"] == "page" and record["parent"] == 1502
    ]
    if len(guide_children) != 35 or any(record["status"] != "draft" for record in guide_children):
        failures.append(f"guide child mismatch: count={len(guide_children)}")

    nav_rows = query(
        "SELECT p.ID, "
        "COALESCE(MAX(CASE WHEN pm.meta_key='_menu_item_menu_item_parent' THEN pm.meta_value END),'0'), "
        "COALESCE(MAX(CASE WHEN pm.meta_key='_menu_item_url' THEN pm.meta_value END),''), "
        "COALESCE(MAX(CASE WHEN pm.meta_key='_menu_item_object_id' THEN pm.meta_value END),''), "
        "COALESCE(MAX(CASE WHEN pm.meta_key='_menu_item_type' THEN pm.meta_value END),'') "
        "FROM wp_posts p LEFT JOIN wp_postmeta pm ON pm.post_id=p.ID "
        "WHERE p.post_type='nav_menu_item' GROUP BY p.ID ORDER BY p.ID;"
    )
    actual_nav = {
        int(row[0]): {
            "parent": row[1],
            "url": row[2],
            "object_id": row[3],
            "item_type": row[4],
        }
        for row in nav_rows
    }
    if actual_nav != expected_nav:
        missing = sorted(set(expected_nav) - set(actual_nav))
        changed = sorted(
            post_id
            for post_id in set(expected_nav) & set(actual_nav)
            if expected_nav[post_id] != actual_nav[post_id]
        )
        failures.append(f"menu hierarchy mismatch: missing={missing}, changed={changed}")

    menu_counts = {
        row[0]: int(row[1])
        for row in query(
            "SELECT t.name, COUNT(*) FROM wp_terms t "
            "JOIN wp_term_taxonomy tt ON tt.term_id=t.term_id AND tt.taxonomy='nav_menu' "
            "JOIN wp_term_relationships tr ON tr.term_taxonomy_id=tt.term_taxonomy_id "
            "JOIN wp_posts p ON p.ID=tr.object_id AND p.post_type='nav_menu_item' "
            "GROUP BY t.name ORDER BY t.name;"
        )
    }
    wanted_menu_counts = {
        "Footer Areas": 6,
        "Footer Blogs": 6,
        "Footer Services": 7,
        "Primary": 23,
        "Primary (2)": 23,
    }
    if menu_counts != wanted_menu_counts:
        failures.append(f"menu counts mismatch: expected {wanted_menu_counts}; got {menu_counts}")

    image_map = json.loads((ROOT / "build/stage8-image-map.json").read_text(encoding="utf-8"))
    attachment_rows = query(
        "SELECT p.ID, p.post_mime_type, COALESCE(pm.meta_value,'') FROM wp_posts p "
        "LEFT JOIN wp_postmeta pm ON pm.post_id=p.ID AND pm.meta_key='_wp_attached_file' "
        "WHERE p.post_type='attachment' ORDER BY p.ID;"
    )
    attachments = {int(row[0]): {"mime": row[1], "file": row[2]} for row in attachment_rows}
    wanted_attachment_ids = {int(value) for value in image_map}
    if set(attachments) != wanted_attachment_ids:
        failures.append(
            f"attachment ID set mismatch: missing={sorted(wanted_attachment_ids-set(attachments))}, "
            f"extra={sorted(set(attachments)-wanted_attachment_ids)}"
        )
    for post_id, mapped in image_map.items():
        got = attachments.get(int(post_id))
        if got and got["file"] != mapped["new_file"]:
            failures.append(
                f"attachment {post_id} file mismatch: expected {mapped['new_file']}; got {got['file']}"
            )

    element_rows = query(
        "SELECT pm.post_id, REPLACE(TO_BASE64(pm.meta_value), CHAR(10), '') "
        "FROM wp_postmeta pm JOIN wp_posts p ON p.ID=pm.post_id "
        "WHERE pm.meta_key='_elementor_data' AND p.post_type='page' ORDER BY pm.post_id;"
    )
    image_reference_count = 0
    image_reference_ids: set[int] = set()
    for post_id_text, encoded in element_rows:
        try:
            data = json.loads(base64.b64decode(encoded).decode("utf-8"))
        except Exception as exc:
            failures.append(f"page {post_id_text} Elementor JSON failed after import: {exc}")
            continue
        for image in walk_images(data):
            image_reference_count += 1
            raw_id = image.get("id")
            if not str(raw_id).isdigit():
                failures.append(f"page {post_id_text} has non-numeric Elementor image ID {raw_id!r}")
                continue
            image_id = int(raw_id)
            image_reference_ids.add(image_id)
            mapped = image_map.get(str(image_id))
            attached = attachments.get(image_id)
            if mapped is None or attached is None:
                failures.append(f"page {post_id_text} unresolved Elementor image ID {image_id}")
                continue
            if attached["file"] != mapped["new_file"]:
                failures.append(f"page {post_id_text} image ID {image_id} resolves to wrong attachment file")
            url = image.get("url")
            if url and url != mapped["new_url"]:
                failures.append(
                    f"page {post_id_text} image ID {image_id} URL mismatch: expected {mapped['new_url']}; got {url}"
                )

    if len(element_rows) != 156:
        failures.append(f"Elementor page row count mismatch: {len(element_rows)}")

    cache_count = int(query("SELECT COUNT(*) FROM wp_postmeta WHERE meta_key='_elementor_element_cache';")[0][0])
    schema_count = int(query("SELECT COUNT(*) FROM wp_postmeta WHERE meta_key LIKE 'rank_math_schema_%';")[0][0])
    if cache_count:
        failures.append(f"stale Elementor cache rows imported: {cache_count}")
    if schema_count:
        failures.append(f"Rank Math schema rows imported: {schema_count}")

    result = {
        "expected_wxr_posts": len(expected),
        "imported_wxr_posts_present": len(imported_actual),
        "allowed_local_posts": sorted(allowed_extra & set(actual)),
        "type_counts": dict(sorted(actual_type_counts.items())),
        "page_statuses": dict(sorted(page_statuses.items())),
        "guide_children": len(guide_children),
        "menu_counts": menu_counts,
        "attachments": len(attachments),
        "elementor_pages": len(element_rows),
        "elementor_image_references": image_reference_count,
        "elementor_image_ids_used": len(image_reference_ids),
        "elementor_cache_rows": cache_count,
        "rank_math_schema_rows": schema_count,
        "importer_normalizations": importer_normalizations,
        "failures": failures,
        "pass": not failures,
    }
    output = ROOT / "build/stage15-import-verification.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
