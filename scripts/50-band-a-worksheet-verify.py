#!/usr/bin/env python3
"""Fail-closed verification of the 20 August 2026 Band A owner decision."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.media_payload import (  # noqa: E402
    REPORT49_APPROVAL_NOTE,
    REPORT49_BAND_A_GENERIC,
    REPORT49_BAND_A_UNUSABLE,
    load_report49_plan,
)

WORKSHEET = ROOT / "reports/44-sighting-worksheet.csv"
REPORT49 = ROOT / "reports/49-image-completion-requirements.csv"
MANIFEST = ROOT / "build/47-media-remediation.csv"
OUTPUT = ROOT / "reports/50-band-a-worksheet-validation.json"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    plan = load_report49_plan(REPORT49)
    expected = plan["band_a"]
    worksheet = {
        int(row["attachment_id"]): row
        for row in rows(WORKSHEET)
        if row["band"] == "A"
    }
    if set(worksheet) != set(expected):
        raise AssertionError(
            f"Band A worksheet IDs differ: worksheet={sorted(worksheet)} expected={sorted(expected)}"
        )
    verdicts = {attachment_id: row["VERDICT"].strip() for attachment_id, row in worksheet.items()}
    if verdicts != {attachment_id: row["verdict"] for attachment_id, row in expected.items()}:
        raise AssertionError(f"Band A verdict mapping differs from Report 49: {verdicts}")
    if Counter(verdicts.values()) != Counter({"GENERIC": 10, "UNUSABLE": 6}):
        raise AssertionError(f"Band A verdict totals differ: {Counter(verdicts.values())}")
    if any(row["NOTE"].strip() != REPORT49_APPROVAL_NOTE for row in worksheet.values()):
        raise AssertionError("one or more Band A rows lack the exact owner-approval source note")

    manifest = {
        int(row["attachment_id"]): row
        for row in rows(MANIFEST)
        if row["band"] == "A"
    }
    if set(manifest) != set(expected):
        raise AssertionError("Band A manifest inventory differs from Report 49")
    if {aid for aid, row in manifest.items() if row["payload_action"] == "RENAME"} != REPORT49_BAND_A_GENERIC:
        raise AssertionError("Band A GENERIC manifest mapping differs")
    if {aid for aid, row in manifest.items() if row["payload_action"] == "EXCLUDE"} != REPORT49_BAND_A_UNUSABLE:
        raise AssertionError("Band A UNUSABLE manifest mapping differs")
    if any(row["payload_action"] == "HOLD" for row in manifest.values()):
        raise AssertionError("Band A HOLD remains")

    result = {
        "result": "PASS",
        "authority": "Owner approval dated 20 August 2026 — FINAL IMAGE REMEDIATION prompt",
        "report49_sha256": sha256(REPORT49),
        "worksheet_sha256": sha256(WORKSHEET),
        "verdict_totals": dict(sorted(Counter(verdicts.values()).items())),
        "blank_verdicts": 0,
        "ok_or_replace_verdicts": 0,
        "hold_assets": 0,
        "mapping": [
            {
                "worksheet_number": worksheet[aid]["#"],
                "attachment_id": aid,
                "verdict": verdicts[aid],
                "payload_action": manifest[aid]["payload_action"],
                "target_filename": manifest[aid]["target_filename"],
                "target_alt": manifest[aid]["target_alt"],
            }
            for aid in sorted(expected, key=lambda value: int(worksheet[value]["#"]))
        ],
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS — Band A worksheet: 16/16 explicit; 10 GENERIC; 6 UNUSABLE; 0 HOLD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
