from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from lib.media_payload import reconcile_elementor_media_references


ROOT = Path(__file__).resolve().parents[1]
WP = "{http://wordpress.org/export/1.2/}"


def csv_rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def test_phase_b_manifest_is_complete_and_fail_closed() -> None:
    rows = csv_rows("build/47-media-remediation.csv")
    assert len(rows) == 83
    assert len({int(row["attachment_id"]) for row in rows}) == 83
    assert Counter(row["payload_action"] for row in rows) == {
        "RENAME": 55,
        "EXCLUDE": 28,
    }
    band_a = {int(row["attachment_id"]): row for row in rows if row["band"] == "A"}
    assert {aid for aid, row in band_a.items() if row["payload_action"] == "RENAME"} == {
        226, 906, 908, 924, 925, 926, 1150, 1152, 1185, 1186,
    }
    assert {aid for aid, row in band_a.items() if row["payload_action"] == "EXCLUDE"} == {
        480, 481, 482, 907, 956, 1187,
    }
    assert not any(row["payload_action"] == "HOLD" for row in rows)
    for row in rows:
        if row["payload_action"] == "RENAME":
            assert not re.search(
                r"camden|south-west-sydney|testimonial|review|verified|our-work|completed-project",
                row["target_filename"],
                re.I,
            )


def test_derivative_has_only_permitted_media_and_valid_serialized_lengths() -> None:
    tree = ET.parse(ROOT / "build/46-active-main-import.xml")
    attachments = [
        item
        for item in tree.getroot().findall("./channel/item")
        if (item.findtext(WP + "post_type") or "").strip() == "attachment"
    ]
    assert len(attachments) == 55
    permitted = {
        int(row["attachment_id"])
        for row in csv_rows("build/47-media-remediation.csv")
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    assert {
        int((item.findtext(WP + "post_id") or "0").strip()) for item in attachments
    } == permitted
    serialized = re.compile(r's:(\d+):"([^"]*)";', re.S)
    for item in attachments:
        for postmeta in item.findall(WP + "postmeta"):
            if (postmeta.findtext(WP + "meta_key") or "") != "_wp_attachment_metadata":
                continue
            value = postmeta.findtext(WP + "meta_value") or ""
            matches = list(serialized.finditer(value))
            assert matches
            for match in matches:
                assert int(match.group(1)) == len(match.group(2).encode("utf-8"))


def test_public_intake_and_quarantines_match_manifest() -> None:
    rows = csv_rows("build/47-media-remediation.csv")
    media = {path.name for path in (ROOT / "source-inputs/media").iterdir() if path.is_file()}
    retired = {path.name for path in (ROOT / "source-inputs/media-retired").iterdir() if path.is_file()}
    held = {path.name for path in (ROOT / "source-inputs/media-held-band-a").iterdir() if path.is_file()}
    expected = {
        row["target_filename"] if row["payload_action"] == "RENAME" else row["current_filename"]
        for row in rows
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    assert media == expected
    assert all(row["current_filename"] in retired for row in rows if row["payload_action"] == "EXCLUDE")
    assert all(row["current_filename"] in held for row in rows if row["payload_action"] == "HOLD")
    assert not any(" (1)" in name for name in media | retired | held)


def test_recursive_elementor_detectors_agree_and_find_nested_typed_images() -> None:
    tree = ET.parse(ROOT / "build/46-active-main-import.xml")
    primary, independent = reconcile_elementor_media_references(tree)
    assert len(primary) == 440
    assert len(independent) == 440
    nested = [
        row for row in primary
        if row["page_id"] == 12
        and row["attachment_id"] == 609
        and row["widget_id"] == "306c538"
    ]
    assert nested
    assert all(row["encoding"] == "elementor-4.2-typed" for row in nested)


def test_original_forty_and_unusable_slots_reconcile() -> None:
    inventory = json.loads(
        (ROOT / "reports/47-original-media-blockers.json").read_text(
            encoding="utf-8", errors="strict"
        )
    )
    assert len(inventory["assertions"]) == 40
    assert inventory["assertion_totals"] == {
        "band_a_verdict_missing": 16,
        "band_b_derivative_disposition_missing": 9,
        "denied_asset_remains": 12,
        "false_geographic_remediation_pending": 3,
    }
    assert inventory["source_unusable_slots"] == 28
    assert sum(
        row["source_slots"] for row in inventory["band_b_unusable_slots"].values()
    ) == 28
