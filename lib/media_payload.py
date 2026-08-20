"""Deterministic Phase B public-media manifest and WXR transformations.

The immutable WXR and Stage 8 rename map remain provenance inputs.  This
module derives the public payload from recorded decisions and the owner
sighting worksheet.  A blank Band A verdict is represented as HOLD and is
excluded fail-closed; it is never converted into a substantive verdict.
"""
from __future__ import annotations

import csv
import io
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from lib.preimport_safety import WP, items, metas, post_id, post_slug, post_type


MANIFEST_COLUMNS = [
    "attachment_id",
    "band",
    "verdict",
    "payload_action",
    "current_filename",
    "target_filename",
    "target_title",
    "target_alt",
    "authority",
    "usage_restriction",
]

# D32's complete source inventory: 15 local-work modules plus two evidential
# sections on gallery.  Gallery is the documented sixteenth page even though
# it does not carry the local-work-card CSS class.
D32_PAGE_IDS = {
    1365,
    1376,
    1378,
    1375,
    969,
    1371,
    1387,
    1372,
    1377,
    1370,
    1126,
    1379,
    221,
    1163,
    1388,
    474,
}

RECORDED_RETIRED_BRAND = {159, 177, 306, 307, 422, 469, 472}
BAND_B_UNUSABLE = {280, 1067}
UNAUTHORISED_AI = {159, 177, 272, 308, 309}
OTHER_PROHIBITED = {
    250: "Astra product mark, not a Structure Co asset",
    468: "E&T Concreters Melbourne wordmark; duplicate contract requires pair treatment",
    471: "E&T Concreters Melbourne wordmark; duplicate contract requires pair treatment",
    1020: "D19 removes the Tarneit soil photograph and retains its containing sections",
}

EXPLICIT_GENERIC = {
    1056: (
        "aerial-waterway-residential-area-1056.jpg",
        "Aerial waterway beside a residential area",
        "Aerial view of a waterway beside a residential area",
        "D18/D20: Victorian Davis Creek cannot be named as South Creek",
    ),
    1151: (
        "dry-cracked-ground-1151.jpg",
        "Dry cracked ground",
        "Dry cracked ground surface",
        "D18/D20: remove unsupported geographic and geological assertion",
    ),
    1188: (
        "dry-cracked-ground-1188.jpg",
        "Dry cracked ground",
        "Dry cracked ground surface",
        "D18/D20: remove unsupported geographic and geological assertion",
    ),
    609: (
        "exposed-aggregate-residential-driveway-609.jpg",
        "Exposed aggregate residential driveway",
        "Exposed aggregate driveway leading to a home",
        "D24/D20: reverse Adelaide to South West Sydney naming substitution",
    ),
    1153: (
        "concrete-vehicle-crossing-1153.jpg",
        "Concrete vehicle crossing",
        "Concrete vehicle crossing between a kerb and property boundary",
        "D24/D20: remove unsupported Camden council/location assertion",
    ),
}

# These binaries are visual placeholders.  D24 still requires the Stage 8
# Camden suffix to be reversed; an empty alt keeps them decorative and avoids
# inventing a visible subject during this pass.
DECORATIVE_EMPTY_ALT = {275, 276, 277, 278, 279, 323}
REPORT49_PLACEHOLDER_ASSETS = frozenset(DECORATIVE_EMPTY_ALT)
REPORT49_BAND_A_GENERIC = {226, 906, 908, 924, 925, 926, 1150, 1152, 1185, 1186}
REPORT49_BAND_A_UNUSABLE = {480, 481, 482, 907, 956, 1187}
REPORT49_APPROVAL_NOTE = "Owner approval dated 20 August 2026 — FINAL IMAGE REMEDIATION prompt; exact Report 49 mapping."

REPORT49_REMOVAL_COUNTS = Counter(
    {
        "D32 whole-section": 45,
        "other prohibited direct": 21,
        "empty testimonial": 3,
        "blank placeholder": 45,
        "Band A UNUSABLE": 50,
    }
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def load_report49_plan(path: Path) -> dict[str, Any]:
    """Load the exact owner-approved Band A mapping and 164 removal slots.

    Report 49 is both the human approval target and the machine-readable slot
    contract.  This loader fails if the recommendation mapping, filename/alt
    remediation, category counts or requirement IDs drift.
    """
    rows = read_csv(path)
    required_columns = {
        "requirement_id", "page_slug", "elementor_widget_id", "section",
        "current_attachment_id", "safe_filename", "alt_text_rule",
        "required_action", "notes",
    }
    if len(rows) != 612 or not rows or not required_columns.issubset(rows[0]):
        raise AssertionError("Report 49 must contain 612 rows and the approved slot-contract columns")
    if len({row["requirement_id"] for row in rows}) != 612:
        raise AssertionError("Report 49 requirement IDs are not unique")

    band_a: dict[int, dict[str, str]] = {}
    all_band_a_ids = REPORT49_BAND_A_GENERIC | REPORT49_BAND_A_UNUSABLE
    for row in rows:
        raw_id = row["current_attachment_id"].strip()
        if not raw_id.isdigit() or int(raw_id) not in all_band_a_ids:
            continue
        attachment_id = int(raw_id)
        match = re.search(r"audit recommends (GENERIC|UNUSABLE)", row["required_action"])
        if not match:
            continue
        verdict = match.group(1)
        candidate = {
            "verdict": verdict,
            "target_filename": row["safe_filename"].strip() if verdict == "GENERIC" else "",
            "target_alt": row["alt_text_rule"].strip() if verdict == "GENERIC" else "",
        }
        prior = band_a.get(attachment_id)
        if prior and prior != candidate:
            raise AssertionError(f"Report 49 has inconsistent Band A mapping for {attachment_id}")
        band_a[attachment_id] = candidate

    if set(band_a) != all_band_a_ids:
        raise AssertionError(
            "Report 49 Band A ID mapping differs: "
            f"missing={sorted(all_band_a_ids-set(band_a))} additional={sorted(set(band_a)-all_band_a_ids)}"
        )
    if {key for key, value in band_a.items() if value["verdict"] == "GENERIC"} != REPORT49_BAND_A_GENERIC:
        raise AssertionError("Report 49 GENERIC mapping differs from the owner-approved ten")
    if {key for key, value in band_a.items() if value["verdict"] == "UNUSABLE"} != REPORT49_BAND_A_UNUSABLE:
        raise AssertionError("Report 49 UNUSABLE mapping differs from the owner-approved six")
    for attachment_id in REPORT49_BAND_A_GENERIC:
        mapped = band_a[attachment_id]
        if not mapped["target_filename"] or not mapped["target_alt"]:
            raise AssertionError(f"Report 49 GENERIC {attachment_id} lacks filename/alt")
    for attachment_id in REPORT49_BAND_A_UNUSABLE:
        if band_a[attachment_id]["target_filename"]:
            raise AssertionError(f"Report 49 UNUSABLE {attachment_id} declares a replacement")

    removals: list[dict[str, str]] = []
    category_counts: Counter[str] = Counter()
    for row in rows:
        action = row["required_action"]
        raw_id = row["current_attachment_id"].strip()
        attachment_id = int(raw_id) if raw_id.isdigit() else None
        category = ""
        if "D32 section already removed" in action or "keep the D32 section removed" in action:
            category = "D32 whole-section"
        elif not raw_id and "remove the complete placeholder testimonial widget" in action:
            category = "empty testimonial"
        elif "prohibited slot already removed" in action or "keep the prohibited asset and every direct slot removed" in action:
            category = "other prohibited direct"
        elif attachment_id in REPORT49_PLACEHOLDER_ASSETS and (
            "blank placeholder" in action or "remove this visual placeholder" in action
        ):
            category = "blank placeholder"
        elif attachment_id in REPORT49_BAND_A_UNUSABLE and "audit recommends UNUSABLE" in action:
            category = "Band A UNUSABLE"
        if not category:
            continue
        section_id = row["section"].split(" — ", 1)[0].strip()
        setting_match = re.search(r"(?:^|;) setting=([^;]+)", row["notes"])
        if not section_id or not row["elementor_widget_id"].strip() or not setting_match:
            raise AssertionError(f"Report 49 removal row {row['requirement_id']} lacks placement identity")
        removals.append(
            {
                "requirement_id": row["requirement_id"],
                "page_slug": row["page_slug"],
                "section_id": section_id,
                "widget_id": row["elementor_widget_id"].strip(),
                "setting": setting_match.group(1).strip(),
                "attachment_id": "" if attachment_id is None else str(attachment_id),
                "category": category,
            }
        )
        category_counts[category] += 1
    if len(removals) != 164 or category_counts != REPORT49_REMOVAL_COUNTS:
        raise AssertionError(
            f"Report 49 removal contract differs: rows={len(removals)}, categories={dict(category_counts)}"
        )
    return {"band_a": band_a, "removals": removals, "removal_counts": category_counts}


def _generic_target(current: str, attachment_id: int) -> tuple[str, str, str]:
    path = Path(current)
    stem = path.stem
    suffix = path.suffix.lower()
    id_suffix = f"-{attachment_id}"
    if not stem.endswith(id_suffix):
        raise AssertionError(f"attachment {attachment_id} filename lacks deterministic ID suffix: {current}")
    subject = stem[: -len(id_suffix)]
    subject = re.sub(r"(?:^|-)south-west-sydney(?:-|$)", "-", subject, flags=re.I)
    subject = re.sub(r"(?:^|-)camden(?:-|$)", "-", subject, flags=re.I)
    subject = re.sub(r"-+", "-", subject).strip("-")
    if not subject:
        raise AssertionError(f"attachment {attachment_id} generic filename became empty")
    target = f"{subject}-{attachment_id}{suffix}"
    title = re.sub(r"\s+", " ", subject.replace("-", " ")).strip().capitalize()
    alt = "" if attachment_id in DECORATIVE_EMPTY_ALT else title
    return target, title, alt


def build_manifest_rows(
    rename_map: Path,
    sighting_worksheet: Path,
    band_b_remediation: Path,
    report49_plan: Path,
) -> list[dict[str, str]]:
    base_rows = read_csv(rename_map)
    sighting_rows = read_csv(sighting_worksheet)
    band_b_rows = read_csv(band_b_remediation)
    completion = load_report49_plan(report49_plan)
    if len(base_rows) != 83 or len(sighting_rows) != 83:
        raise AssertionError(
            f"media inputs must contain 83 rows: rename={len(base_rows)}, sighting={len(sighting_rows)}"
        )
    base = {int(row["attachment_id"]): row for row in base_rows}
    sighting = {int(row["attachment_id"]): row for row in sighting_rows}
    band_b = {int(row["attachment_id"]): row for row in band_b_rows}
    if len(base) != 83 or set(base) != set(sighting):
        raise AssertionError("rename map and sighting worksheet attachment IDs do not match exactly")
    if set(band_b) != {46, 47, 48, 49, 51, 52, 228, 280, 1067}:
        raise AssertionError("Band B remediation IDs changed from the owner-authorised nine")

    recorded_band_a = {
        int(row["attachment_id"]): {
            "verdict": (row.get("VERDICT") or "").strip().upper(),
            "note": (row.get("NOTE") or "").strip(),
        }
        for row in sighting_rows
        if row["band"].strip().upper() == "A"
    }
    if set(recorded_band_a) != REPORT49_BAND_A_GENERIC | REPORT49_BAND_A_UNUSABLE:
        raise AssertionError("worksheet Band A IDs differ from the approved Report 49 mapping")
    for attachment_id, approved in completion["band_a"].items():
        recorded = recorded_band_a[attachment_id]
        if recorded["verdict"] != approved["verdict"]:
            raise AssertionError(
                f"worksheet/Report 49 verdict mismatch for {attachment_id}: "
                f"{recorded['verdict']!r} != {approved['verdict']!r}"
            )
        if recorded["note"] != REPORT49_APPROVAL_NOTE:
            raise AssertionError(f"worksheet Band A {attachment_id} lacks the exact owner-approval source")

    output: list[dict[str, str]] = []
    for attachment_id in sorted(base):
        source = base[attachment_id]
        sighted = sighting[attachment_id]
        band = sighted["band"].strip().upper()
        verdict = (sighted.get("VERDICT") or "").strip().upper()
        current = source["new_filename"]
        action = ""
        target_filename = ""
        target_title = ""
        target_alt = ""
        authority = ""
        restriction = ""

        if band == "A":
            if not verdict:
                action = "HOLD"
                verdict = "UNRECORDED"
                authority = "owner worksheet blank; fail-closed under Phase B instruction"
                restriction = "not permitted into public intake or derivative until owner verdict"
            elif verdict == "OK":
                # An OK must carry provenance evidence in the owner's note.
                note = (sighted.get("NOTE") or "").strip()
                if not note:
                    raise AssertionError(f"Band A attachment {attachment_id} OK lacks provenance evidence")
                action = "RETAIN"
                target_filename = current
                authority = "owner worksheet OK with recorded provenance: " + note
            elif verdict == "GENERIC":
                overlay = completion["band_a"].get(attachment_id)
                if not overlay or overlay["verdict"] != "GENERIC":
                    raise AssertionError(f"Band A attachment {attachment_id} differs from Report 49")
                action = "RENAME"
                target_filename = overlay["target_filename"]
                target_title = re.sub(
                    r"\s+", " ", Path(target_filename).stem.rsplit(f"-{attachment_id}", 1)[0].replace("-", " ")
                ).strip().capitalize()
                target_alt = overlay["target_alt"]
                authority = "owner approval dated 20 August 2026; exact Report 49 GENERIC mapping"
                restriction = (
                    "decorative/non-evidential only; no Camden/South West Sydney, completed project, "
                    "customer, testimonial, premises, equipment-ownership or NSW-operator implication"
                )
            elif verdict in {"REPLACE", "UNUSABLE"}:
                if verdict != "UNUSABLE" or attachment_id not in REPORT49_BAND_A_UNUSABLE:
                    raise AssertionError(f"Band A attachment {attachment_id} is not an approved Report 49 UNUSABLE")
                action = "EXCLUDE"
                authority = "owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping"
                restriction = "remove public slots without replacement"
            else:
                raise AssertionError(f"Band A attachment {attachment_id} has invalid verdict {verdict!r}")
        elif band == "B":
            overlay = band_b.get(attachment_id)
            if not overlay or verdict != overlay["verdict"]:
                raise AssertionError(f"Band B attachment {attachment_id} worksheet/remediation mismatch")
            action = overlay["ship_action"]
            target_filename = overlay["target_filename"]
            target_title = overlay["target_title"]
            target_alt = overlay["target_alt"]
            authority = "owner-recorded Band B verdict; build/45-media-remediation.csv"
            restriction = overlay["usage_restriction"]
        elif band == "C":
            if attachment_id not in {306, 307, 422, 469, 472}:
                raise AssertionError(f"unexpected Band C attachment {attachment_id}")
            action = "EXCLUDE"
            verdict = "RETIRED"
            authority = "D18/D36 retired E&T brand attachment"
            restriction = "Structure Co replacements are supplied separately; old slot may not survive"
        elif band == "D":
            if attachment_id in REPORT49_PLACEHOLDER_ASSETS:
                action = "EXCLUDE"
                verdict = "UNUSABLE"
                authority = "owner-approved Report 49 zero-new-photograph plan; blank placeholder asset"
                restriction = "remove every recorded placeholder slot without replacement"
            elif attachment_id in RECORDED_RETIRED_BRAND:
                action = "EXCLUDE"
                verdict = "RETIRED"
                authority = "D24/D36 retired AI/source-brand attachment"
            elif attachment_id in UNAUTHORISED_AI:
                action = "EXCLUDE"
                verdict = "UNUSABLE"
                authority = "D24 and C2PA/AI provenance finding"
            elif attachment_id in OTHER_PROHIBITED:
                action = "EXCLUDE"
                verdict = "UNUSABLE"
                authority = OTHER_PROHIBITED[attachment_id]
            else:
                action = "RENAME"
                verdict = "GENERIC"
                if attachment_id in EXPLICIT_GENERIC:
                    target_filename, target_title, target_alt, authority = EXPLICIT_GENERIC[attachment_id]
                else:
                    target_filename, target_title, target_alt = _generic_target(current, attachment_id)
                    authority = "D24/D20 naming-convention reversal"
                restriction = "decorative/non-evidential; no geographic or completed-project implication"
        else:
            raise AssertionError(f"attachment {attachment_id} has unknown sighting band {band!r}")

        if action == "RENAME":
            if not target_filename or not target_title:
                raise AssertionError(f"attachment {attachment_id} RENAME lacks target filename/title")
            if re.search(r"camden|south-west-sydney|testimonial|review|verified|our-work|completed-project", target_filename, re.I):
                raise AssertionError(f"attachment {attachment_id} target filename retains prohibited implication")
        elif action in {"EXCLUDE", "HOLD"}:
            if target_filename or target_title or target_alt:
                raise AssertionError(f"attachment {attachment_id} {action} cannot declare a public target")
        elif action == "RETAIN":
            if target_filename != current:
                raise AssertionError(f"attachment {attachment_id} RETAIN target differs from current filename")
        else:
            raise AssertionError(f"attachment {attachment_id} unknown payload action {action!r}")

        output.append(
            {
                "attachment_id": str(attachment_id),
                "band": band,
                "verdict": verdict,
                "payload_action": action,
                "current_filename": current,
                "target_filename": target_filename,
                "target_title": target_title,
                "target_alt": target_alt,
                "authority": authority,
                "usage_restriction": restriction,
            }
        )

    counts = Counter(row["payload_action"] for row in output)
    if counts != Counter({"RENAME": 55, "EXCLUDE": 28}):
        raise AssertionError(f"unexpected Phase B manifest action counts: {dict(counts)}")
    return output


def manifest_bytes(rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=MANIFEST_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def _repair_serialized_strings(blob: str, old_stem: str, new_stem: str) -> tuple[str, int]:
    pattern = re.compile(r's:(\d+):"((?:[^"\\]|\\.)*)";', re.S)
    changed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        value = match.group(2)
        replaced = value.replace(old_stem, new_stem)
        if replaced == value:
            return match.group(0)
        changed += 1
        return f's:{len(replaced.encode("utf-8"))}:"{replaced}";'

    return pattern.sub(replace, blob), changed


def _contains_marker(node: Any) -> bool:
    if isinstance(node, dict):
        if any(_contains_marker(value) for value in node.values()):
            return True
    elif isinstance(node, list):
        if any(_contains_marker(value) for value in node):
            return True
    elif isinstance(node, str):
        return "REAL_PHOTO_PENDING" in node or "local-work-card" in node
    return False


def _count_marker(node: Any) -> int:
    if isinstance(node, dict):
        return sum(_count_marker(value) for value in node.values())
    if isinstance(node, list):
        return sum(_count_marker(value) for value in node)
    if isinstance(node, str):
        return node.count("REAL_PHOTO_PENDING")
    return 0


def _media_id(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def _remove_excluded_media(node: Any, excluded: set[int], counts: Counter[int]) -> Any:
    """Prune denied media settings while preserving non-image widget content."""
    if isinstance(node, list):
        output = []
        for child in node:
            transformed = _remove_excluded_media(child, excluded, counts)
            if transformed is not None:
                output.append(transformed)
        return output
    if not isinstance(node, dict):
        return node

    settings = node.get("settings")
    widget_type = str(node.get("widgetType") or "")
    if isinstance(settings, dict):
        primary = settings.get("image")
        if isinstance(primary, dict):
            attachment_id = _media_id(primary.get("id"))
            if attachment_id in excluded:
                counts[attachment_id] += 1
                if widget_type == "image":
                    return None
                settings.pop("image", None)

        for key in list(settings):
            value = settings[key]
            if isinstance(value, dict):
                attachment_id = _media_id(value.get("id"))
                if attachment_id in excluded and ("url" in value or key.endswith("image")):
                    counts[attachment_id] += 1
                    settings.pop(key, None)
                    continue
            settings[key] = _remove_excluded_media(value, excluded, counts)

    for key in list(node):
        if key == "settings":
            continue
        value = node[key]
        if isinstance(value, (dict, list)):
            transformed = _remove_excluded_media(value, excluded, counts)
            if transformed is None:
                node.pop(key, None)
            else:
                node[key] = transformed
    return node


def _update_media_alt(node: Any, targets: dict[int, dict[str, str]], counts: Counter[int]) -> None:
    if isinstance(node, dict):
        attachment_id = _media_id(node.get("id"))
        if attachment_id in targets and "url" in node:
            node["alt"] = targets[attachment_id]["target_alt"]
            counts[attachment_id] += 1
        for value in node.values():
            _update_media_alt(value, targets, counts)
    elif isinstance(node, list):
        for value in node:
            _update_media_alt(value, targets, counts)


def _classic_or_typed_image(value: Any) -> tuple[int | None, str, str, str]:
    """Decode classic Elementor media dicts and Elementor 4.2 typed images."""
    if not isinstance(value, dict):
        return None, "", "", ""
    attachment_id = _media_id(value.get("id"))
    if attachment_id is not None and "url" in value:
        return attachment_id, str(value.get("url") or ""), str(value.get("alt") or ""), "classic"
    if value.get("$$type") == "image":
        source = value.get("value", {}).get("src", {}).get("value", {})
        if isinstance(source, dict):
            typed_id = _media_id(source.get("id", {}).get("value")) if isinstance(source.get("id"), dict) else None
            if typed_id is not None:
                raw_url = source.get("url")
                if isinstance(raw_url, dict):
                    raw_url = raw_url.get("value")
                return typed_id, str(raw_url or ""), "", "elementor-4.2-typed"
    return None, "", "", ""


def _apply_direct_report49_removals(
    parsed: list[Any],
    page_slug: str,
    contract_rows: list[dict[str, str]],
    applied: set[str],
) -> list[Any]:
    by_key: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in contract_rows:
        if row["page_slug"] == page_slug and row["category"] != "D32 whole-section":
            by_key[(row["section_id"], row["widget_id"])].append(row)

    def transform(node: Any, section_id: str) -> Any:
        if isinstance(node, list):
            output = []
            for child in node:
                changed = transform(child, section_id)
                if changed is not None:
                    output.append(changed)
            return output
        if not isinstance(node, dict):
            return node
        widget_id = str(node.get("id") or "")
        matches = by_key.get((section_id, widget_id), [])
        settings = node.get("settings")
        for row in matches:
            if not isinstance(settings, dict) or row["setting"] not in settings:
                raise AssertionError(
                    f"Report 49 slot {row['requirement_id']} absent at /{page_slug}/ "
                    f"section {section_id} widget {widget_id} setting {row['setting']}"
                )
            value = settings[row["setting"]]
            actual_id, _url, _alt, _encoding = _classic_or_typed_image(value)
            expected_id = int(row["attachment_id"]) if row["attachment_id"] else None
            if actual_id != expected_id:
                raise AssertionError(
                    f"Report 49 slot {row['requirement_id']} attachment differs: "
                    f"{actual_id} != {expected_id}"
                )
            applied.add(row["requirement_id"])
            if row["category"] == "empty testimonial" or (
                str(node.get("widgetType") or "") == "image" and row["setting"] == "image"
            ):
                return None
            settings.pop(row["setting"])

        children = node.get("elements")
        if isinstance(children, list):
            node["elements"] = transform(children, section_id)
        return node

    output = []
    for top in parsed:
        if not isinstance(top, dict):
            output.append(top)
            continue
        section_id = str(top.get("id") or "")
        changed = transform(top, section_id)
        if changed is not None:
            output.append(changed)
    return output


def _report49_slot_matches(top: Any, row: dict[str, str]) -> bool:
    if not isinstance(top, dict) or str(top.get("id") or "") != row["section_id"]:
        return False
    found = False

    def walk(node: Any) -> None:
        nonlocal found
        if found or not isinstance(node, dict):
            return
        if str(node.get("id") or "") == row["widget_id"]:
            settings = node.get("settings")
            if isinstance(settings, dict) and row["setting"] in settings:
                actual_id, _url, _alt, _encoding = _classic_or_typed_image(settings[row["setting"]])
                expected_id = int(row["attachment_id"]) if row["attachment_id"] else None
                if actual_id == expected_id:
                    found = True
                    return
        for child in node.get("elements", []) if isinstance(node.get("elements"), list) else []:
            walk(child)

    walk(top)
    return found


def apply_media_payload_transform(
    tree: ET.ElementTree,
    manifest_rows: list[dict[str, str]],
    report49_plan: dict[str, Any],
) -> dict[str, Any]:
    manifest = {int(row["attachment_id"]): row for row in manifest_rows}
    if len(manifest) != 83:
        raise AssertionError("Phase B media manifest must cover exactly 83 attachment IDs")
    excluded = {
        attachment_id
        for attachment_id, row in manifest.items()
        if row["payload_action"] in {"EXCLUDE", "HOLD"}
    }
    targets = {
        attachment_id: row
        for attachment_id, row in manifest.items()
        if row["payload_action"] == "RENAME"
    }
    result: dict[str, Any] = {
        "manifest_actions": dict(sorted(Counter(row["payload_action"] for row in manifest_rows).items())),
        "d32_pages": [],
        "d32_top_level_sections_removed": 0,
        "d32_markers_removed": 0,
        "report49_removal_contract": dict(sorted(report49_plan["removal_counts"].items())),
        "report49_direct_slots_removed": 0,
        "report49_removal_ids_applied": [],
        "brand_replacement_slots_held": {},
        "excluded_slots_removed": {},
        "renamed_elementor_references": {},
        "attachment_records_excluded": 0,
        "attachment_records_renamed": 0,
        "serialized_metadata_strings_repaired": 0,
        "wp_css_records_excluded": 0,
    }

    # D32: remove the complete evidential section from all 16 recorded pages.
    d32_contract = [
        row for row in report49_plan["removals"] if row["category"] == "D32 whole-section"
    ]
    if len(d32_contract) != 45:
        raise AssertionError(f"Report 49 D32 slot contract is {len(d32_contract)}, expected 45")
    d32_applied: set[str] = set()
    pages_seen: set[int] = set()
    for item in items(tree):
        if post_type(item) != "page" or post_id(item) not in D32_PAGE_IDS:
            continue
        pages_seen.add(post_id(item))
        for _pm, key, value_node in metas(item):
            if key != "_elementor_data" or not (value_node.text or "").strip():
                continue
            parsed = json.loads(value_node.text or "[]")
            if not isinstance(parsed, list):
                raise AssertionError(f"page {post_id(item)} Elementor root is not a list")
            kept = []
            removed = []
            for top in parsed:
                if _contains_marker(top):
                    removed.append(top)
                    for contract_row in d32_contract:
                        if contract_row["page_slug"] == post_slug(item) and _report49_slot_matches(top, contract_row):
                            d32_applied.add(contract_row["requirement_id"])
                else:
                    kept.append(top)
            if not removed:
                raise AssertionError(f"D32 page {post_id(item)} {post_slug(item)} has no evidential top-level section")
            result["d32_top_level_sections_removed"] += len(removed)
            result["d32_markers_removed"] += sum(_count_marker(node) for node in removed)
            result["d32_pages"].append(
                {
                    "page_id": post_id(item),
                    "slug": post_slug(item),
                    "sections_removed": len(removed),
                    "markers_removed": sum(_count_marker(node) for node in removed),
                }
            )
            value_node.text = json.dumps(kept, ensure_ascii=False, separators=(",", ":"))
    if pages_seen != D32_PAGE_IDS:
        raise AssertionError(f"D32 page inventory mismatch: missing={sorted(D32_PAGE_IDS-pages_seen)}")
    if result["d32_markers_removed"] != 47:
        raise AssertionError(f"D32 removed {result['d32_markers_removed']} markers, expected 47")
    expected_d32_ids = {row["requirement_id"] for row in d32_contract}
    if d32_applied != expected_d32_ids:
        raise AssertionError(
            "Report 49 D32 slot application differs: "
            f"missing={sorted(expected_d32_ids-d32_applied)} additional={sorted(d32_applied-expected_d32_ids)}"
        )

    # Rename text/URLs throughout the derivative before parsing Elementor data.
    for attachment_id, row in targets.items():
        old_name = row["current_filename"]
        new_name = row["target_filename"]
        old_stem = Path(old_name).stem
        new_stem = Path(new_name).stem
        for node in tree.getroot().iter():
            if not node.text:
                continue
            if node.tag == WP + "meta_value":
                # PHP-serialized attachment metadata must retain correct byte lengths.
                repaired, repaired_count = _repair_serialized_strings(node.text, old_stem, new_stem)
                if repaired_count:
                    node.text = repaired
                    result["serialized_metadata_strings_repaired"] += repaired_count
            node.text = (node.text or "").replace(old_name, new_name).replace(old_stem, new_stem)

    slot_counts: Counter[int] = Counter()
    alt_counts: Counter[int] = Counter()
    direct_contract = [
        row for row in report49_plan["removals"] if row["category"] != "D32 whole-section"
    ]
    direct_applied: set[str] = set()
    for item in items(tree):
        if post_type(item) == "page":
            for pm, key, value_node in list(metas(item)):
                if key == "_elementor_data" and (value_node.text or "").strip():
                    parsed = json.loads(value_node.text or "[]")
                    parsed = _apply_direct_report49_removals(
                        parsed, post_slug(item), direct_contract, direct_applied
                    )
                    parsed = _remove_excluded_media(parsed, excluded, slot_counts)
                    _update_media_alt(parsed, targets, alt_counts)
                    value_node.text = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
                elif key in {"_thumbnail_id", "_elementor_page_settings"}:
                    raw = (value_node.text or "").strip()
                    if raw.isdigit() and int(raw) in excluded:
                        item.remove(pm)
    expected_direct_ids = {row["requirement_id"] for row in direct_contract}
    if direct_applied != expected_direct_ids or len(direct_applied) != 119:
        raise AssertionError(
            "Report 49 direct-slot application differs: "
            f"applied={len(direct_applied)} missing={sorted(expected_direct_ids-direct_applied)} "
            f"additional={sorted(direct_applied-expected_direct_ids)}"
        )
    # The only denied references allowed outside the 164-row removal contract
    # are the six recorded D36 page-logo replacement slots.  They were already
    # held out by the pre-existing derivative and await supplied Structure Co
    # wordmark assignment at the eventual authorised import.
    if slot_counts != Counter({306: 5, 307: 1}):
        raise AssertionError(
            "unrecorded denied-slot removals outside Report 49/D36: " + repr(dict(slot_counts))
        )
    all_contract_applied = d32_applied | direct_applied
    if len(all_contract_applied) != 164:
        raise AssertionError(f"Report 49 applied removal total {len(all_contract_applied)} != 164")
    result["report49_direct_slots_removed"] = len(direct_applied)
    result["report49_removal_ids_applied"] = sorted(all_contract_applied)
    result["brand_replacement_slots_held"] = {
        str(key): value for key, value in sorted(slot_counts.items())
    }

    channel = tree.getroot().find("./channel")
    if channel is None:
        raise AssertionError("WXR channel absent")
    for item in list(channel.findall("item")):
        item_type = post_type(item)
        attachment_id = post_id(item)
        if item_type == "custom_css":
            channel.remove(item)
            result["wp_css_records_excluded"] += 1
            continue
        if item_type != "attachment":
            continue
        if attachment_id in excluded:
            channel.remove(item)
            result["attachment_records_excluded"] += 1
            continue
        row = targets.get(attachment_id)
        if not row:
            continue
        title = item.find("title")
        slug = item.find(WP + "post_name")
        if title is not None:
            title.text = row["target_title"]
        if slug is not None:
            slug.text = Path(row["target_filename"]).stem
        for _pm, key, value_node in metas(item):
            if key == "_wp_attachment_image_alt":
                value_node.text = row["target_alt"]
        result["attachment_records_renamed"] += 1

    contract_attachment_counts: Counter[int] = Counter(
        int(row["attachment_id"])
        for row in direct_contract
        if row["attachment_id"]
    )
    result["excluded_slots_removed"] = {
        str(key): value for key, value in sorted(contract_attachment_counts.items())
    }
    result["renamed_elementor_references"] = {
        str(key): value for key, value in sorted(alt_counts.items())
    }
    result["d32_pages"] = sorted(result["d32_pages"], key=lambda row: row["page_id"])
    return result


def elementor_media_references(tree: ET.ElementTree) -> list[dict[str, Any]]:
    """Primary recursive detector for classic and typed Elementor media."""
    found: list[dict[str, Any]] = []
    for item in items(tree):
        if post_type(item) != "page":
            continue
        for _pm, key, value_node in metas(item):
            if key != "_elementor_data" or not (value_node.text or "").strip():
                continue
            parsed = json.loads(value_node.text or "[]")

            def walk(
                node: Any,
                path: str = "$",
                widget_id: str = "",
                media_setting: str = "",
            ) -> None:
                if isinstance(node, dict):
                    if node.get("id") and isinstance(node.get("settings"), dict):
                        widget_id = str(node["id"])
                    attachment_id, url, alt, encoding = _classic_or_typed_image(node)
                    if attachment_id is not None:
                        found.append(
                            {
                                "page_id": post_id(item),
                                "slug": post_slug(item),
                                "attachment_id": attachment_id,
                                "path": path,
                                "widget_id": widget_id,
                                "media_setting": media_setting,
                                "url": url,
                                "alt": alt,
                                "encoding": encoding,
                            }
                        )
                    for child_key, child in node.items():
                        if isinstance(child, (dict, list)):
                            next_setting = media_setting
                            if child_key in {"image", "background_image", "testimonial_image"}:
                                next_setting = child_key
                            walk(child, f"{path}.{child_key}", widget_id, next_setting)
                elif isinstance(node, list):
                    for index, child in enumerate(node):
                        walk(child, f"{path}[{index}]", widget_id, media_setting)

            walk(parsed)
    return found


def independent_elementor_media_references(tree: ET.ElementTree) -> list[dict[str, Any]]:
    """Independent settings-first detector used to catch primary-walker gaps."""
    found: list[dict[str, Any]] = []
    for item in items(tree):
        if post_type(item) != "page":
            continue
        for _pm, key, value_node in metas(item):
            if key != "_elementor_data" or not (value_node.text or "").strip():
                continue
            parsed = json.loads(value_node.text or "[]")

            def scan_setting(value: Any, widget_id: str, setting: str, path: str) -> None:
                attachment_id, url, alt, encoding = _classic_or_typed_image(value)
                if attachment_id is not None:
                    found.append(
                        {
                            "page_id": post_id(item),
                            "slug": post_slug(item),
                            "attachment_id": attachment_id,
                            "path": path,
                            "widget_id": widget_id,
                            "media_setting": setting,
                            "url": url,
                            "alt": alt,
                            "encoding": encoding,
                        }
                    )
                    return
                if isinstance(value, dict):
                    for child_key, child in value.items():
                        if isinstance(child, (dict, list)):
                            scan_setting(child, widget_id, setting, f"{path}.{child_key}")
                elif isinstance(value, list):
                    for index, child in enumerate(value):
                        scan_setting(child, widget_id, setting, f"{path}[{index}]")

            def walk_elements(nodes: Any, path: str = "$") -> None:
                if not isinstance(nodes, list):
                    return
                for index, node in enumerate(nodes):
                    if not isinstance(node, dict):
                        continue
                    node_path = f"{path}[{index}]"
                    widget_id = str(node.get("id") or "")
                    settings = node.get("settings")
                    if isinstance(settings, dict):
                        for setting, value in settings.items():
                            if isinstance(value, (dict, list)):
                                scan_setting(
                                    value, widget_id, setting, f"{node_path}.settings.{setting}"
                                )
                    walk_elements(node.get("elements"), f"{node_path}.elements")

            walk_elements(parsed)
    return found


def reconcile_elementor_media_references(
    tree: ET.ElementTree,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    primary = elementor_media_references(tree)
    independent = independent_elementor_media_references(tree)

    def signature(rows: list[dict[str, Any]]) -> Counter[tuple[int, int, str, str]]:
        return Counter(
            (
                int(row["page_id"]), int(row["attachment_id"]),
                str(row["widget_id"]), str(row["media_setting"]),
            )
            for row in rows
        )

    first = signature(primary)
    second = signature(independent)
    if first != second:
        raise AssertionError(
            "Elementor media detectors disagree: "
            f"primary-only={list((first-second).elements())[:10]} "
            f"independent-only={list((second-first).elements())[:10]}"
        )
    return primary, independent
