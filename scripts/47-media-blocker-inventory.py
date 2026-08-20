#!/usr/bin/env python3
"""Reproduce and enrich the original 40 public-media assertions.

The inventory is derived from the immutable WXR, so it remains reproducible
after the public intake and derivative have been remediated.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.media_payload import elementor_media_references  # noqa: E402
from lib.preimport_safety import items, metas, parse_wxr, post_id, post_slug, post_status, post_type  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "camden-concreting-import.xml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
RENAME = ROOT / "reports" / "08-image-rename-map.csv"
MANIFEST = ROOT / "build" / "47-media-remediation.csv"
OUT = ROOT / "reports" / "47-original-media-blockers.json"

ORIGINAL_DENIED = [159, 177, 272, 280, 306, 307, 308, 309, 422, 469, 472, 1067]
BAND_A = [907, 924, 226, 1185, 906, 1150, 1186, 1187, 1152, 908, 480, 481, 482, 956, 926, 925]
FALSE_GEO = [1056, 1151, 1188]
BAND_B = [46, 52, 49, 51, 48, 47, 228, 280, 1067]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def detailed_references() -> dict[int, list[dict[str, Any]]]:
    found: dict[int, list[dict[str, Any]]] = defaultdict(list)
    tree = parse_wxr(MAIN)
    for item in items(tree):
        if post_type(item) != "page":
            continue
        for _pm, key, value_node in metas(item):
            if key != "_elementor_data" or not (value_node.text or "").strip():
                continue
            parsed = json.loads(value_node.text or "[]")

            def walk(node: Any, path: str = "$", widget_id: str = "", widget_type: str = "") -> None:
                if isinstance(node, dict):
                    current_widget_id = str(node.get("id") or widget_id)
                    current_widget_type = str(node.get("widgetType") or widget_type)
                    media_id = node.get("id")
                    if (
                        isinstance(media_id, int)
                        and media_id > 0
                        and "url" in node
                    ):
                        found[media_id].append(
                            {
                                "page_id": post_id(item),
                                "slug": post_slug(item),
                                "status": post_status(item),
                                "elementor_path": path,
                                "widget_id": current_widget_id,
                                "widget_type": current_widget_type,
                                "url": str(node.get("url") or ""),
                                "alt": str(node.get("alt") or ""),
                            }
                        )
                    for child_key, child in node.items():
                        if isinstance(child, (dict, list)):
                            walk(
                                child,
                                f"{path}.{child_key}",
                                current_widget_id,
                                current_widget_type,
                            )
                elif isinstance(node, list):
                    for index, child in enumerate(node):
                        walk(child, f"{path}[{index}]", widget_id, widget_type)

            walk(parsed)
    return found


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    allow = json.loads(ALLOWLIST.read_text(encoding="utf-8", errors="strict"))
    active_ids = {
        int(row["page_id"])
        for row in allow["pages"]
        if row["import_artifact"] == "build/46-active-main-import.xml"
    }
    base = {int(row["attachment_id"]): row for row in read_csv(RENAME)}
    manifest = {int(row["attachment_id"]): row for row in read_csv(MANIFEST)}
    references = detailed_references()
    assertions: list[dict[str, Any]] = []

    def add(category: str, attachment_id: int, reason: str, disposition: str) -> None:
        placements = references.get(attachment_id, [])
        active = [row for row in placements if row["page_id"] in active_ids]
        withdrawn = [row for row in placements if row["page_id"] not in active_ids]
        row = manifest[attachment_id]
        assertions.append(
            {
                "assertion_number": len(assertions) + 1,
                "category": category,
                "attachment_id": attachment_id,
                "filename_at_failure": base[attachment_id]["new_filename"],
                "elementor_references": len(placements),
                "pages": len({item["page_id"] for item in placements}),
                "active_elementor_references": len(active),
                "active_pages": len({item["page_id"] for item in active}),
                "withdrawn_elementor_references": len(withdrawn),
                "withdrawn_pages": len({item["page_id"] for item in withdrawn}),
                "placements": placements,
                "why_it_failed": reason,
                "authorised_disposition": disposition,
                "transformation_required": (
                    f"{row['payload_action']}"
                    + (f" as {row['target_filename']} with alt {row['target_alt']!r}" if row["payload_action"] == "RENAME" else "")
                ),
                "final_payload_action": row["payload_action"],
            }
        )

    for attachment_id in ORIGINAL_DENIED:
        row = manifest[attachment_id]
        add(
            "denied_asset_remains",
            attachment_id,
            "retired brand, unauthorised AI, or owner-confirmed UNUSABLE asset remained represented in the public payload",
            row["authority"],
        )
    for attachment_id in BAND_A:
        add(
            "band_a_verdict_missing",
            attachment_id,
            "owner pixel-sighting verdict is blank",
            "HOLD outside public intake and derivative; continue failing until the owner records a verdict",
        )
    for attachment_id in FALSE_GEO:
        add(
            "false_geographic_remediation_pending",
            attachment_id,
            "filename/title/alt made an unsupported geographic or geological assertion",
            manifest[attachment_id]["authority"],
        )
    for attachment_id in BAND_B:
        add(
            "band_b_derivative_disposition_missing",
            attachment_id,
            "owner-recorded Band B decision had not been applied to the generated derivative",
            manifest[attachment_id]["authority"],
        )
    if len(assertions) != 40:
        raise AssertionError(f"original assertion count {len(assertions)} != 40")

    unusable = {}
    for attachment_id in (280, 1067):
        placements = references[attachment_id]
        unusable[str(attachment_id)] = {
            "source_slots": len(placements),
            "active_slots": sum(row["page_id"] in active_ids for row in placements),
            "withdrawn_slots": sum(row["page_id"] not in active_ids for row in placements),
            "pages": sorted({row["slug"] for row in placements}),
        }
    if sum(row["source_slots"] for row in unusable.values()) != 28:
        raise AssertionError("Band B unusable slot total no longer reconciles to 28")

    document = {
        "schema_version": "1.0",
        "generated_by": "scripts/47-media-blocker-inventory.py",
        "scope_note": (
            "The original 40 are assertions from preflight Gate 17. Gate 7 is uniqueness; "
            "Gate 16 is claim-to-evidence and separately contained four Band B local-project adjacencies."
        ),
        "assertion_totals": dict(sorted(Counter(row["category"] for row in assertions).items())),
        "assertions": assertions,
        "band_b_unusable_slots": unusable,
        "source_unusable_slots": 28,
    }
    OUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in assertions:
        print(
            f"{row['assertion_number']:02d}. [{row['category']}] attachment {row['attachment_id']} "
            f"{row['filename_at_failure']} — refs={row['elementor_references']} "
            f"(active={row['active_elementor_references']}, withdrawn={row['withdrawn_elementor_references']}) — "
            f"{row['why_it_failed']} — {row['transformation_required']}"
        )
    print(f"TOTAL: {len(assertions)} assertions")
    print(f"inventory -> {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
