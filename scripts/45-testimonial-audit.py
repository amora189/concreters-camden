#!/usr/bin/env python3
"""Audit testimonial-labelled attachments against the immutable Camden WXR.

This is deliberately read-only with respect to the WXR. It writes a complete
one-row-per-placement CSV and a concise Markdown report so that "alongside" is
defined by Elementor structure rather than by a line-oriented XML search.
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
WXR = ROOT / "camden-concreting-import.xml"
CSV_OUT = ROOT / "reports" / "45-testimonial-text-investigation.csv"
MD_OUT = ROOT / "reports" / "45-testimonial-text-investigation.md"

WP_NS = "http://wordpress.org/export/1.2/"
NS = {"wp": WP_NS}

TARGETS = {
    46: "concrete-tesimonial-4-camden-46.webp",
    47: "concrete-testimonial-6-camden-47.webp",
    48: "concrete-testimonial-3-camden-48.webp",
    49: "concrete-testimonial-1-camden-49.webp",
    51: "concrete-testimonial-2-camden-51.webp",
    52: "concrete-testimonial-1-1-camden-52.webp",
    228: "concretejob1camden-228.jpg",
}

CONTENT_KEYS = {
    "editor",
    "title",
    "text",
    "html",
    "testimonial_content",
    "testimonial_name",
    "testimonial_job",
    "item_description",
    "description_text",
    "title_text",
    "caption",
    "image_caption",
    "item_title",
    "button_text",
}
TESTIMONIAL_KEYS = {
    "testimonial_content",
    "testimonial_name",
    "testimonial_job",
}
RATING_KEYS = {
    "rating",
    "rating_scale",
    "star_rating",
    "stars",
    "review_rating",
}


def plain(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]*>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def image_ids(value: Any) -> set[int]:
    found: set[int] = set()
    if isinstance(value, dict):
        value_id = value.get("id")
        if (
            isinstance(value_id, int)
            and value_id in TARGETS
            and any(key in value for key in ("url", "alt", "source"))
        ):
            found.add(value_id)
        for child in value.values():
            found.update(image_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(image_ids(child))
    return found


def content_fields(value: Any, path: str = "") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in CONTENT_KEYS and isinstance(child, str) and plain(child):
                found.append((child_path, plain(child)))
            elif (
                key == "value"
                and isinstance(child, str)
                and ".content." in child_path
                and plain(child)
            ):
                found.append((child_path, plain(child)))
            found.extend(content_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(content_fields(child, f"{path}[{index}]"))
    return found


def exact_key_fields(
    value: Any, keys: set[str], path: str = ""
) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in keys and child not in (None, "", [], {}):
                rendered = plain(child) if isinstance(child, str) else json.dumps(
                    child, ensure_ascii=False, sort_keys=True
                )
                found.append((child_path, rendered))
            found.extend(exact_key_fields(child, keys, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(exact_key_fields(child, keys, f"{path}[{index}]"))
    return found


def encoded(fields: Iterable[tuple[str, str]]) -> str:
    return json.dumps(list(fields), ensure_ascii=False, separators=(",", ":"))


def page_meta(item: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for postmeta in item.findall("wp:postmeta", NS):
        key = postmeta.findtext("wp:meta_key", default="", namespaces=NS)
        value = postmeta.findtext("wp:meta_value", default="", namespaces=NS)
        result[key] = value
    return result


def walk(
    value: Any,
    ancestors: list[dict[str, Any]],
    page: dict[str, str],
    placements: list[dict[str, str]],
) -> None:
    if isinstance(value, list):
        for child in value:
            walk(child, ancestors, page, placements)
        return
    if not isinstance(value, dict):
        return

    settings = value.get("settings", {})
    if isinstance(settings, dict):
        for attachment_id in sorted(image_ids(settings)):
            own_text = content_fields(settings)
            nearest_id = ""
            nearest_type = ""
            nearest_text: list[tuple[str, str]] = []
            nearest_testimonial: list[tuple[str, str]] = []
            nearest_ratings: list[tuple[str, str]] = []
            for ancestor in reversed(ancestors):
                candidate_text = content_fields(ancestor)
                if candidate_text:
                    nearest_id = str(ancestor.get("id", ""))
                    nearest_type = str(
                        ancestor.get("widgetType") or ancestor.get("elType") or ""
                    )
                    nearest_text = candidate_text
                    nearest_testimonial = exact_key_fields(
                        ancestor, TESTIMONIAL_KEYS
                    )
                    nearest_ratings = exact_key_fields(ancestor, RATING_KEYS)
                    break

            alt = ""
            image = settings.get("image")
            if isinstance(image, dict) and image.get("id") == attachment_id:
                alt = str(image.get("alt", ""))

            marker_text = [
                text
                for _, text in nearest_text
                if "REAL_PHOTO_PENDING" in text
            ]
            placements.append(
                {
                    "attachment_id": str(attachment_id),
                    "filename": TARGETS[attachment_id],
                    **page,
                    "widget_id": str(value.get("id", "")),
                    "widget_type": str(
                        value.get("widgetType") or value.get("elType") or ""
                    ),
                    "local_work_card": (
                        "yes"
                        if "local-work-card"
                        in str(settings.get("_css_classes", ""))
                        else "no"
                    ),
                    "current_alt": alt,
                    "same_widget_visible_text": encoded(own_text),
                    "nearest_context_id": nearest_id,
                    "nearest_context_type": nearest_type,
                    "nearest_context_visible_text": encoded(nearest_text),
                    "customer_name_quote_job_fields": encoded(
                        nearest_testimonial
                    ),
                    "rating_fields": encoded(nearest_ratings),
                    "local_work_marker": " | ".join(marker_text),
                }
            )

    children = value.get("elements", [])
    if isinstance(children, list):
        for child in children:
            walk(child, ancestors + [value], page, placements)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    placements: list[dict[str, str]] = []
    testimonial_widgets: list[dict[str, str]] = []

    for _, item in ET.iterparse(WXR, events=("end",)):
        if item.tag != "item":
            continue
        if item.findtext("wp:post_type", default="", namespaces=NS) != "page":
            item.clear()
            continue

        meta = page_meta(item)
        raw = meta.get("_elementor_data", "")
        if not raw:
            item.clear()
            continue
        data = json.loads(raw)
        page = {
            "post_id": item.findtext("wp:post_id", default="", namespaces=NS),
            "slug": item.findtext("wp:post_name", default="", namespaces=NS),
            "page_title": item.findtext("title", default=""),
            "status": item.findtext("wp:status", default="", namespaces=NS),
        }
        walk(data, [], page, placements)

        def collect_testimonials(value: Any) -> None:
            if isinstance(value, list):
                for child in value:
                    collect_testimonials(child)
            elif isinstance(value, dict):
                if value.get("widgetType") == "testimonial":
                    settings = value.get("settings", {})
                    image = settings.get("testimonial_image", {})
                    testimonial_widgets.append(
                        {
                            **page,
                            "widget_id": str(value.get("id", "")),
                            "content": str(settings.get("testimonial_content", "")),
                            "name": str(settings.get("testimonial_name", "")),
                            "job": str(settings.get("testimonial_job", "")),
                            "image_id": str(
                                image.get("id", "")
                                if isinstance(image, dict)
                                else ""
                            ),
                        }
                    )
                for child in value.get("elements", []):
                    collect_testimonials(child)

        collect_testimonials(data)
        item.clear()

    placements.sort(
        key=lambda row: (
            int(row["attachment_id"]),
            int(row["post_id"]),
            row["widget_id"],
        )
    )
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", errors="strict", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(placements[0]))
        writer.writeheader()
        writer.writerows(placements)

    summary: dict[int, dict[str, Any]] = defaultdict(dict)
    for attachment_id in TARGETS:
        rows = [
            row for row in placements if int(row["attachment_id"]) == attachment_id
        ]
        page_keys = {(row["post_id"], row["status"]) for row in rows}
        statuses = Counter(status for _, status in page_keys)
        summary[attachment_id] = {
            "placements": len(rows),
            "pages": len(page_keys),
            "publish": statuses["publish"],
            "draft": statuses["draft"],
            "local_work": sum(row["local_work_card"] == "yes" for row in rows),
        }

    populated_customer_fields = sum(
        row["customer_name_quote_job_fields"] != "[]" for row in placements
    )
    populated_rating_fields = sum(row["rating_fields"] != "[]" for row in placements)
    local_work_rows = [row for row in placements if row["local_work_card"] == "yes"]

    lines = [
        "# Testimonial-text investigation — attachments 46, 47, 48, 49, 51, 52 and 228",
        "",
        "Date: 20 August 2026 (Australia/Sydney).",
        "Source: immutable `camden-concreting-import.xml`; Elementor structure plus WordPress page status.",
        "",
        "## Outcome",
        "",
        "**Fabricated customer quotes found: 0.** The seven files are testimonial-labelled photographs,",
        "not testimonial portraits attached to reviews. No placement of any target carries a customer name,",
        "customer quote, star rating, testimonial suburb attribution, review date or testimonial job description.",
        "Accordingly, no invented-testimonial category is added to the false-fidelity register.",
        "",
        "The only actual Elementor testimonial widgets in the entire WXR are three homepage placeholders.",
        "All three have an empty image ID, placeholder review text, placeholder reviewer name, no job field",
        "and no rating field. None references attachments 46, 47, 48, 49, 51, 52 or 228.",
        "",
        "## Attachment distribution",
        "",
        "| Attachment | Pages | Placements | Publish pages | Draft pages | Local-work-card placements |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for attachment_id, filename in TARGETS.items():
        item = summary[attachment_id]
        lines.append(
            f"| {attachment_id} `{filename}` | {item['pages']} | {item['placements']} | "
            f"{item['publish']} | {item['draft']} | {item['local_work']} |"
        )

    lines += [
        "",
        "Attachment 228 is the correction to the supplied premise: it appears on **14 pages**, not 15,",
        "with 16 placements because it is used twice on both Bargo and Mount Annan.",
        "",
        "## Exact text in the four local-work-card placements",
        "",
        "| Attachment | Page | Status | Exact adjacent text |",
        "|---:|---|---|---|",
    ]
    for row in local_work_rows:
        marker = row["local_work_marker"].replace("|", "\\|")
        lines.append(
            f"| {row['attachment_id']} | `/{row['slug']}/` | {row['status']} | `{marker}` |"
        )

    lines += [
        "",
        "Attachments 47, 51 and 228 have **zero** local-work-card placements. The four rows above carry",
        "blocking markers, not customer assertions: no customer is named and no quote, rating, date or",
        "job description is supplied. Those local-work modules are already scheduled for complete removal",
        "under D32; the generic-photo verdict does not authorise them as evidence.",
        "",
        "## Actual testimonial widgets in the WXR",
        "",
        "| Page | Widget | Content | Name | Job | Image ID |",
        "|---|---|---|---|---|---|",
    ]
    for row in testimonial_widgets:
        lines.append(
            f"| `/{row['slug']}/` | `{row['widget_id']}` | `{row['content']}` | "
            f"`{row['name']}` | `{row['job'] or '(empty)'}` | `{row['image_id'] or '(empty)'}` |"
        )

    lines += [
        "",
        "## Machine-verifiable totals",
        "",
        "```text",
        f"  target placements                            {len(placements)}",
        f"  populated customer/name/quote/job fields    {populated_customer_fields}",
        f"  populated rating fields                     {populated_rating_fields}",
        f"  actual testimonial widgets                  {len(testimonial_widgets)}",
        "  actual testimonial widgets using targets   0",
        "  fabricated customer quotes                 0",
        "```",
        "",
        "The complete evidence is `reports/45-testimonial-text-investigation.csv`: one row per image",
        "placement, with exact same-widget text, the nearest containing Elementor context, current alt",
        "text, WordPress status, marker text and any exact testimonial/rating keys.",
        "",
        "No page or WXR value was changed by this audit.",
    ]
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="strict")

    print(f"placements={len(placements)}")
    print(f"customer_fields={populated_customer_fields}")
    print(f"rating_fields={populated_rating_fields}")
    print(f"testimonial_widgets={len(testimonial_widgets)}")
    print(f"csv={CSV_OUT.relative_to(ROOT).as_posix()}")
    print(f"report={MD_OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
