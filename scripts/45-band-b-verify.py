#!/usr/bin/env python3
"""Verify and report the applied Band B media disposition."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WXR = ROOT / "camden-concreting-import.xml"
MANIFEST = ROOT / "build" / "45-media-remediation.csv"
FULL_MANIFEST = ROOT / "build" / "47-media-remediation.csv"
WORKSHEET = ROOT / "reports" / "44-sighting-worksheet.csv"
BANDS = ROOT / "build" / "44-sighting-bands.json"
SLOTS_OUT = ROOT / "reports" / "45-band-b-unusable-slots.csv"
REPORT_OUT = ROOT / "reports" / "45-band-b-application.md"
NS = {"wp": "http://wordpress.org/export/1.2/"}


def image_ids(value: Any, path: str = "") -> list[tuple[int, bool]]:
    found: list[tuple[int, bool]] = []
    if isinstance(value, dict):
        value_id = value.get("id")
        if isinstance(value_id, int) and any(
            key in value for key in ("url", "alt", "source")
        ):
            found.append((value_id, "background_image" in path))
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            found.extend(image_ids(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(image_ids(child, f"{path}[{index}]"))
    return found


def has_local_work_card(value: Any) -> bool:
    if isinstance(value, dict):
        settings = value.get("settings", {})
        if (
            isinstance(settings, dict)
            and "local-work-card" in str(settings.get("_css_classes", ""))
        ):
            return True
        return any(has_local_work_card(child) for child in value.values())
    if isinstance(value, list):
        return any(has_local_work_card(child) for child in value)
    return False


def walk_slots(
    value: Any,
    ancestors: list[dict[str, Any]],
    page: dict[str, str],
    unusable: set[int],
    slots: list[dict[str, str]],
) -> None:
    if isinstance(value, list):
        for child in value:
            walk_slots(child, ancestors, page, unusable, slots)
        return
    if not isinstance(value, dict):
        return
    settings = value.get("settings", {})
    direct = {image_id for image_id, _ in image_ids(settings)} & unusable
    for attachment_id in sorted(direct):
        top = ancestors[0] if ancestors else value
        if has_local_work_card(top):
            mode = "remove with D32 top-level local-work module"
        elif value.get("widgetType") == "image":
            mode = "remove image widget"
        elif value.get("widgetType") == "image-box":
            mode = "clear image setting; preserve title description and link"
        else:
            mode = "UNSUPPORTED"
        slots.append(
            {
                "attachment_id": str(attachment_id),
                **page,
                "widget_id": str(value.get("id", "")),
                "widget_type": str(
                    value.get("widgetType") or value.get("elType") or ""
                ),
                "removal_mode": mode,
            }
        )
    children = value.get("elements", [])
    if isinstance(children, list):
        for child in children:
            walk_slots(child, ancestors + [value], page, unusable, slots)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    failures: list[str] = []
    with MANIFEST.open("r", encoding="utf-8", errors="strict", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 9:
        failures.append(f"remediation rows {len(rows)} != 9")
    by_id = {int(row["attachment_id"]): row for row in rows}
    generic = {key for key, row in by_id.items() if row["ship_action"] == "RENAME"}
    unusable = {key for key, row in by_id.items() if row["ship_action"] == "EXCLUDE"}
    if len(generic) != 7 or len(unusable) != 2:
        failures.append(
            f"verdict split GENERIC={len(generic)} UNUSABLE={len(unusable)}, expected 7/2"
        )

    media = ROOT / "source-inputs" / "media"
    retired = ROOT / "source-inputs" / "media-retired"
    active_files = {path.name for path in media.iterdir() if path.is_file()}
    with FULL_MANIFEST.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        full_rows = list(csv.DictReader(handle))
    expected_public = sum(
        row["payload_action"] in {"RENAME", "RETAIN"} for row in full_rows
    )
    if len(active_files) != expected_public:
        failures.append(f"active media files {len(active_files)} != {expected_public}")
    for attachment_id, row in by_id.items():
        current = row["current_filename"]
        if row["ship_action"] == "RENAME":
            if row["target_filename"] not in active_files:
                failures.append(
                    f"attachment {attachment_id} target missing: {row['target_filename']}"
                )
            if current in active_files:
                failures.append(
                    f"attachment {attachment_id} pre-remediation filename remains active"
                )
        else:
            if current in active_files:
                failures.append(f"attachment {attachment_id} UNUSABLE file remains active")
            if not (retired / current).is_file():
                failures.append(
                    f"attachment {attachment_id} UNUSABLE provenance copy is missing"
                )

    if (
        hashlib.sha256((media / by_id[49]["target_filename"]).read_bytes()).digest()
        != hashlib.sha256((media / by_id[52]["target_filename"]).read_bytes()).digest()
    ):
        failures.append("attachments 49 and 52 are not byte-identical as recorded")

    worksheet = {
        int(row["attachment_id"]): row
        for row in csv.DictReader(
            WORKSHEET.open("r", encoding="utf-8", errors="strict", newline="")
        )
        if row["band"] == "B"
    }
    bands = {
        int(row["attachment_id"]): row
        for row in json.loads(BANDS.read_text(encoding="utf-8", errors="strict"))
        if row["band"] == "B"
    }
    for attachment_id, row in by_id.items():
        for label, source in (("worksheet", worksheet), ("bands JSON", bands)):
            if attachment_id not in source:
                failures.append(f"attachment {attachment_id} absent from {label}")
            elif source[attachment_id]["VERDICT"] != row["verdict"]:
                failures.append(
                    f"attachment {attachment_id} {label} verdict mismatch: "
                    f"{source[attachment_id]['VERDICT']} != {row['verdict']}"
                )

    slots: list[dict[str, str]] = []
    stats = Counter()
    for _, item in ET.iterparse(WXR, events=("end",)):
        if item.tag != "item":
            continue
        if item.findtext("wp:post_type", default="", namespaces=NS) != "page":
            item.clear()
            continue
        raw = ""
        for postmeta in item.findall("wp:postmeta", NS):
            if postmeta.findtext("wp:meta_key", default="", namespaces=NS) == "_elementor_data":
                raw = postmeta.findtext("wp:meta_value", default="", namespaces=NS)
                break
        if raw:
            data = json.loads(raw)
            page = {
                "post_id": item.findtext("wp:post_id", default="", namespaces=NS),
                "slug": item.findtext("wp:post_name", default="", namespaces=NS),
                "status": item.findtext("wp:status", default="", namespaces=NS),
            }
            walk_slots(data, [], page, unusable, slots)
            refs = image_ids(data)
            stats["foreground"] += sum(not background for _, background in refs)
            stats["background"] += sum(background for _, background in refs)
            for top in data:
                top_ids = [image_id for image_id, _ in image_ids(top)]
                if has_local_work_card(top):
                    stats["modules"] += 1
                    stats["module_refs"] += len(top_ids)
                    stats["generic_in_modules"] += sum(
                        image_id in generic for image_id in top_ids
                    )
                    stats["unusable_in_modules"] += sum(
                        image_id in unusable for image_id in top_ids
                    )
                else:
                    stats["generic_surviving"] += sum(
                        image_id in generic for image_id in top_ids
                    )
                    stats["unusable_outside_modules"] += sum(
                        image_id in unusable for image_id in top_ids
                    )
        item.clear()

    expected_stats = {
        "foreground": 1085,
        "background": 98,
        "modules": 15,
        "module_refs": 45,
        "generic_in_modules": 4,
        "unusable_in_modules": 2,
        "generic_surviving": 106,
        "unusable_outside_modules": 26,
    }
    for key, expected in expected_stats.items():
        if stats[key] != expected:
            failures.append(f"{key} {stats[key]} != {expected}")
    if len(slots) != 28:
        failures.append(f"UNUSABLE slot rows {len(slots)} != 28")
    unsupported = [row for row in slots if row["removal_mode"] == "UNSUPPORTED"]
    if unsupported:
        failures.append(f"unsupported slot removal contexts: {len(unsupported)}")

    slots.sort(
        key=lambda row: (
            int(row["attachment_id"]),
            row["status"] != "publish",
            int(row["post_id"]),
        )
    )
    with SLOTS_OUT.open("w", encoding="utf-8", errors="strict", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(slots[0]))
        writer.writeheader()
        writer.writerows(slots)

    lines = [
        "# Band B application report",
        "",
        "Date: 20 August 2026 (Australia/Sydney).",
        "Authority: owner instruction and `HANDOVER-2026-08-19.md` Part 2.",
        "",
        "## Result",
        "",
        "```text",
        f"  GENERIC assets renamed                  {len(generic)}",
        f"  UNUSABLE assets excluded                {len(unusable)}",
        f"  active public-media files               {len(active_files)}",
        f"  unusable Elementor slots registered     {len(slots)}",
        f"  verification failures                   {len(failures)}",
        f"  verdict                                 {'PASS' if not failures else 'FAIL'}",
        "```",
        "",
        "## GENERIC filename and alt remediation",
        "",
        "| ID | Target filename | Subject-only alt |",
        "|---:|---|---|",
    ]
    for attachment_id in sorted(generic):
        row = by_id[attachment_id]
        lines.append(
            f"| {attachment_id} | `{row['target_filename']}` | {row['target_alt']} |"
        )
    lines += [
        "",
        "All seven are decoration only. They cannot be used as customer evidence or in a recent/local-work module.",
        "Attachments 49 and 52 are exact binary duplicates but remain distinct IDs.",
        "",
        "## UNUSABLE slot removal",
        "",
        "| ID | Pages | Publish | Draft | D32 module | Image widget | Image-box setting |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for attachment_id in sorted(unusable):
        subset = [row for row in slots if int(row["attachment_id"]) == attachment_id]
        modes = Counter(row["removal_mode"] for row in subset)
        statuses = Counter(row["status"] for row in subset)
        lines.append(
            f"| {attachment_id} | {len(subset)} | {statuses['publish']} | {statuses['draft']} | "
            f"{modes['remove with D32 top-level local-work module']} | "
            f"{modes['remove image widget']} | "
            f"{modes['clear image setting; preserve title description and link']} |"
        )
    lines += [
        "",
        "The complete 28-row page/widget list is `reports/45-band-b-unusable-slots.csv`.",
        "No replacement image or substitute badge is permitted.",
        "",
        "## Post-import count contract",
        "",
        "```text",
        "  original foreground image references    1,085",
        "  background-image references                 98  unchanged",
        "  D32 local-work modules                     15  removing 45 images",
        "  GENERIC references removed with D32          4",
        "  surviving GENERIC references remediated     106",
        "  UNUSABLE references removed                  28",
        "  surviving foreground image references     1,014",
        "```",
        "",
        "The immutable WXR remains untouched. Band B is now enforced in the reproducibly generated",
        "`build/46-active-main-import.xml`; the former post-import mutator is a fail-closed guard.",
        "The public intake contains the seven Band B files under their target names and the two",
        "UNUSABLE binaries remain recoverable outside public uploads.",
    ]
    if failures:
        lines += ["", "## Failures", "", *[f"- {failure}" for failure in failures]]
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="strict")

    print(f"generic={len(generic)} unusable={len(unusable)} active={len(active_files)} slots={len(slots)}")
    print(f"failures={len(failures)}")
    print(f"report={REPORT_OUT.relative_to(ROOT).as_posix()}")
    print(f"slots={SLOTS_OUT.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
