#!/usr/bin/env python3
"""Fail-closed public-media payload gate.

Binary integrity is checked separately by Stage 22.  This gate asserts the
generated Phase B manifest against both the local public intake and the exact
derived WXR.  Blank Band A verdicts always fail even though their assets are
held out of both payloads.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.media_payload import (  # noqa: E402
    BAND_B_UNUSABLE,
    OTHER_PROHIBITED,
    RECORDED_RETIRED_BRAND,
    UNAUTHORISED_AI,
    reconcile_elementor_media_references,
)
from lib.preimport_safety import items, parse_wxr, post_id, post_type  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "source-inputs" / "media"
RETIRED = ROOT / "source-inputs" / "media-retired"
HELD = ROOT / "source-inputs" / "media-held-band-a"
MANIFEST = ROOT / "build" / "47-media-remediation.csv"
SIGHTING = ROOT / "reports" / "44-sighting-worksheet.csv"
DERIVED = ROOT / "build" / "46-active-main-import.xml"
POLICY = ROOT / "build" / "46-public-media-policy.json"
RESULT = ROOT / "reports" / "46-public-media-gate.json"
REPORT49 = ROOT / "reports" / "49-image-completion-requirements.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    errors: list[str] = []
    manifest_rows = rows(MANIFEST)
    sighting_rows = rows(SIGHTING)
    if len(manifest_rows) != 83:
        errors.append(f"Phase B manifest has {len(manifest_rows)} rows, expected 83")
    manifest = {int(row["attachment_id"]): row for row in manifest_rows}
    if len(manifest) != 83:
        errors.append("Phase B manifest contains duplicate attachment IDs")
    if len(sighting_rows) != 83:
        errors.append(f"sighting worksheet has {len(sighting_rows)} rows, expected 83")

    present_names = {path.name for path in MEDIA.iterdir() if path.is_file()} if MEDIA.is_dir() else set()
    expected_names = {
        row["target_filename"] if row["payload_action"] == "RENAME" else row["current_filename"]
        for row in manifest_rows
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    if present_names != expected_names:
        errors.append(
            f"public intake parity mismatch missing={sorted(expected_names-present_names)} "
            f"additional={sorted(present_names-expected_names)}"
        )

    if not DERIVED.is_file():
        errors.append("active derivative WXR absent")
        derivative_tree = None
        derivative_raw = ""
        derived_attachment_ids: set[int] = set()
        media_refs: list[dict] = []
        independent_media_refs: list[dict] = []
    else:
        derivative_tree = parse_wxr(DERIVED)
        derivative_raw = DERIVED.read_text(encoding="utf-8", errors="strict")
        derived_attachment_ids = {
            post_id(item) for item in items(derivative_tree) if post_type(item) == "attachment"
        }
        media_refs, independent_media_refs = reconcile_elementor_media_references(derivative_tree)

    permitted_ids = {
        attachment_id
        for attachment_id, row in manifest.items()
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    if derived_attachment_ids != permitted_ids:
        errors.append(
            f"derived attachment parity mismatch missing={sorted(permitted_ids-derived_attachment_ids)} "
            f"additional={sorted(derived_attachment_ids-permitted_ids)}"
        )
    unresolved_refs = [row for row in media_refs if row["attachment_id"] not in permitted_ids]
    if unresolved_refs:
        errors.append(f"{len(unresolved_refs)} Elementor media references target non-permitted assets")

    denied_findings = []
    generic_assets = []
    held_band_a_ids = []
    other_excluded_ids = []
    for attachment_id, row in sorted(manifest.items()):
        action = row["payload_action"]
        current = row["current_filename"]
        if action == "RENAME":
            target = row["target_filename"]
            derivative_ok = (
                current not in derivative_raw
                and target in derivative_raw
                and attachment_id in derived_attachment_ids
            )
            intake_ok = target in present_names and current not in present_names
            refs = [ref for ref in media_refs if ref["attachment_id"] == attachment_id]
            refs_ok = all(
                (
                    ref["encoding"] == "elementor-4.2-typed"
                    and not ref["url"]
                    and not ref["alt"]
                )
                or (
                    target in ref["url"] and ref["alt"] == row["target_alt"]
                )
                for ref in refs
            )
            if not (derivative_ok and intake_ok and refs_ok):
                errors.append(
                    f"attachment {attachment_id} RENAME not fully enforced: "
                    f"derivative={derivative_ok}, intake={intake_ok}, refs={refs_ok}"
                )
            generic_assets.append(
                {
                    "attachment_id": attachment_id,
                    "source_filename": current,
                    "target_filename": target,
                    "target_title": row["target_title"],
                    "target_alt": row["target_alt"],
                    "elementor_references": len(refs),
                    "usage_restriction": row["usage_restriction"],
                    "result": "PASS" if derivative_ok and intake_ok and refs_ok else "FAIL",
                }
            )
        elif action in {"EXCLUDE", "HOLD"}:
            quarantine = HELD if action == "HOLD" else RETIRED
            in_public = current in present_names
            in_derivative = attachment_id in derived_attachment_ids or current in derivative_raw
            quarantined = (quarantine / current).is_file()
            if in_public or in_derivative or not quarantined:
                errors.append(
                    f"attachment {attachment_id} {action} not enforced: "
                    f"public={in_public}, derivative={in_derivative}, quarantined={quarantined}"
                )
            if action == "HOLD":
                held_band_a_ids.append(attachment_id)
            elif attachment_id not in RECORDED_RETIRED_BRAND and attachment_id not in BAND_B_UNUSABLE:
                other_excluded_ids.append(attachment_id)
            denied_findings.append(
                {
                    "attachment_id": attachment_id,
                    "filename": current,
                    "payload_action": action,
                    "verdict": row["verdict"],
                    "reasons": [row["authority"]],
                    "present_in_public_intake": in_public,
                    "present_in_derived_wxr": in_derivative,
                    "quarantine_path": quarantine.relative_to(ROOT).as_posix(),
                    "quarantined": quarantined,
                    "result": "PASS" if not in_public and not in_derivative and quarantined else "FAIL",
                }
            )
        elif action == "RETAIN":
            if current not in present_names or attachment_id not in derived_attachment_ids:
                errors.append(f"attachment {attachment_id} RETAIN not present in both payloads")
        else:
            errors.append(f"attachment {attachment_id} has unknown action {action!r}")

    band_a_findings = []
    for worksheet in [row for row in sighting_rows if row["band"].upper() == "A"]:
        attachment_id = int(worksheet["attachment_id"])
        manifest_row = manifest[attachment_id]
        verdict = (worksheet.get("VERDICT") or "").strip().upper()
        result = "PASS"
        if not verdict:
            verdict = "UNRECORDED"
            result = "FAIL"
            errors.append(f"Band A attachment {attachment_id} has no recorded pixel verdict")
        elif verdict not in {"OK", "GENERIC", "REPLACE", "UNUSABLE"}:
            result = "FAIL"
            errors.append(f"Band A attachment {attachment_id} has invalid verdict {verdict!r}")
        elif (
            verdict == "GENERIC" and manifest[attachment_id]["payload_action"] != "RENAME"
        ) or (
            verdict == "UNUSABLE" and manifest[attachment_id]["payload_action"] != "EXCLUDE"
        ):
            result = "FAIL"
            errors.append(
                f"Band A attachment {attachment_id} verdict/action mismatch: "
                f"{verdict}/{manifest[attachment_id]['payload_action']}"
            )
        band_a_findings.append(
            {
                "attachment_id": attachment_id,
                "filename": manifest_row["current_filename"],
                "target_filename": manifest_row["target_filename"],
                "claim_made": worksheet["claim_made"],
                "verdict": verdict,
                "payload_action": manifest_row["payload_action"],
                "present_in_public_intake": (
                    manifest_row["target_filename"] in present_names
                    if manifest_row["payload_action"] == "RENAME"
                    else manifest_row["current_filename"] in present_names
                ),
                "present_in_derived_wxr": attachment_id in derived_attachment_ids,
                "result": result,
            }
        )
    if len(band_a_findings) != 16:
        errors.append(f"Band A has {len(band_a_findings)} rows, expected 16")

    # The owner approved the exact Report 49 reuse map, not arbitrary movement
    # of a generic asset to another widget. Reconcile every surviving Band A
    # GENERIC reference against its page/widget/setting contract.
    band_a_generic_ids = {
        attachment_id
        for attachment_id, row in manifest.items()
        if row["band"] == "A" and row["payload_action"] == "RENAME"
    }
    report49_generic_slots: Counter[tuple[str, str, str, int]] = Counter()
    for row in rows(REPORT49):
        raw_id = row["current_attachment_id"].strip()
        if not raw_id.isdigit() or int(raw_id) not in band_a_generic_ids:
            continue
        if "audit recommends GENERIC" not in row["required_action"]:
            continue
        setting = re.search(r"(?:^|;) setting=([^;]+)", row["notes"])
        if not setting:
            errors.append(f"Report 49 generic slot {row['requirement_id']} lacks setting identity")
            continue
        report49_generic_slots[
            (
                row["page_slug"],
                row["elementor_widget_id"],
                setting.group(1).strip(),
                int(raw_id),
            )
        ] += 1
    derivative_generic_slots = Counter(
        (
            ref["slug"], ref["widget_id"], ref["media_setting"], ref["attachment_id"]
        )
        for ref in media_refs
        if ref["attachment_id"] in band_a_generic_ids
    )
    if derivative_generic_slots != report49_generic_slots:
        errors.append(
            "Band A generic placement contract differs: "
            f"missing={list((report49_generic_slots-derivative_generic_slots).elements())[:10]} "
            f"additional={list((derivative_generic_slots-report49_generic_slots).elements())[:10]}"
        )

    band_b_findings = []
    for worksheet in [row for row in sighting_rows if row["band"].upper() == "B"]:
        attachment_id = int(worksheet["attachment_id"])
        row = manifest[attachment_id]
        action = row["payload_action"]
        if action == "RENAME":
            generic = next(asset for asset in generic_assets if asset["attachment_id"] == attachment_id)
            ok = generic["result"] == "PASS"
            present = row["target_filename"] in present_names
        else:
            denied = next(asset for asset in denied_findings if asset["attachment_id"] == attachment_id)
            ok = denied["result"] == "PASS"
            present = row["current_filename"] in present_names
        if not ok:
            errors.append(f"Band B attachment {attachment_id} disposition is not fully enforced")
        band_b_findings.append(
            {
                "attachment_id": attachment_id,
                "verdict": row["verdict"],
                "payload_action": action,
                "filename": row["target_filename"] or None,
                "present": present,
                "derived_wxr_remediated": ok,
                "result": "PASS" if ok else "FAIL",
            }
        )

    false_geo_ids = {609, 1056, 1151, 1153, 1188}
    false_geo_findings = []
    for attachment_id in sorted(false_geo_ids):
        row = manifest[attachment_id]
        stale = row["current_filename"] in present_names or row["current_filename"] in derivative_raw
        target_ok = (
            row["target_filename"] in present_names and row["target_filename"] in derivative_raw
        )
        if stale or not target_ok:
            errors.append(f"attachment {attachment_id} false-geography remediation incomplete")
        false_geo_findings.append(
            {
                "attachment_id": attachment_id,
                "source_filename": row["current_filename"],
                "target_filename": row["target_filename"],
                "target_alt": row["target_alt"],
                "result": "PASS" if not stale and target_ok else "FAIL",
            }
        )

    hashes: dict[str, list[tuple[int, str]]] = defaultdict(list)
    filename_to_id = {
        (row["target_filename"] if row["payload_action"] == "RENAME" else row["current_filename"]): attachment_id
        for attachment_id, row in manifest.items()
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    for filename in sorted(present_names):
        digest = hashlib.sha256((MEDIA / filename).read_bytes()).hexdigest().upper()
        hashes[digest].append((filename_to_id[filename], filename))
    duplicate_groups = [
        {"sha256": digest, "members": [{"attachment_id": i, "filename": n} for i, n in members]}
        for digest, members in sorted(hashes.items())
        if len(members) > 1
    ]
    duplicate_contracts = []
    for member_ids, treatment in [
        ({49, 52}, "preserve both IDs and both generic filenames; decoration only"),
        ({468, 471}, "exclude both E&T source identities together; never collapse one reference target"),
    ]:
        present_ids = member_ids & permitted_ids
        required = member_ids if member_ids == {49, 52} else set()
        if present_ids != required:
            errors.append(
                f"duplicate contract {sorted(member_ids)} has public IDs {sorted(present_ids)}, "
                f"expected {sorted(required)}"
            )
        duplicate_contracts.append(
            {
                "attachment_ids": sorted(member_ids),
                "present_ids": sorted(present_ids),
                "required_treatment": treatment,
                "result": "PASS" if present_ids == required else "FAIL",
            }
        )

    policy = {
        "schema_version": "2.0",
        "generated_by": "scripts/46-public-media-gate.py",
        "technical_audit_is_not_publication_approval": True,
        "retired_brand_ids": sorted(RECORDED_RETIRED_BRAND),
        "band_b_unusable_ids": sorted(BAND_B_UNUSABLE),
        "held_band_a_ids": sorted(held_band_a_ids),
        "band_a_denied_ids": sorted(
            attachment_id
            for attachment_id, row in manifest.items()
            if row["band"] == "A" and row["payload_action"] in {"EXCLUDE", "HOLD"}
        ),
        "other_excluded_ids": sorted(other_excluded_ids),
        "unauthorised_ai_ids": {
            str(value): "D24/C2PA or later AI provenance finding"
            for value in sorted(UNAUTHORISED_AI)
        },
        "denied_assets": sorted(denied_findings, key=lambda row: row["attachment_id"]),
        "generic_assets": sorted(generic_assets, key=lambda row: row["attachment_id"]),
        "false_geographic_remediated": false_geo_findings,
        "band_a_rule": (
            "Only exact recorded owner verdicts are accepted; the 20 August 2026 Report 49 "
            "mapping is 10 GENERIC and 6 UNUSABLE, with zero HOLD assets"
        ),
        "duplicate_rule": "Never collapse byte duplicates when distinct attachment IDs are referenced",
    }
    POLICY.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {
        "result": "FAIL" if errors else "PASS",
        "public_intake_files": len(present_names),
        "derived_attachment_records": len(derived_attachment_ids),
        "elementor_media_references": len(media_refs),
        "independent_elementor_media_references": len(independent_media_refs) if derivative_tree is not None else 0,
        "elementor_media_detectors_reconciled": derivative_tree is not None,
        "unresolved_elementor_media_references": unresolved_refs,
        "manifest_actions": dict(sorted(Counter(row["payload_action"] for row in manifest_rows).items())),
        "denied_assets": sorted(denied_findings, key=lambda row: row["attachment_id"]),
        "band_a": band_a_findings,
        "band_a_generic_placement_contract": {
            "expected": sum(report49_generic_slots.values()),
            "actual": sum(derivative_generic_slots.values()),
            "reconciled": derivative_generic_slots == report49_generic_slots,
        },
        "band_b": band_b_findings,
        "false_geographic_remediated": false_geo_findings,
        "duplicate_groups_found": duplicate_groups,
        "duplicate_contracts": duplicate_contracts,
        "errors": errors,
    }
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print(
            f"FAIL — public media suitability: {len(errors)} blocking findings; "
            f"Band A unresolved={sum(x['verdict']=='UNRECORDED' for x in band_a_findings)}; "
            f"Band B failed={sum(x['result']=='FAIL' for x in band_b_findings)}",
            file=sys.stderr,
        )
        return 1
    print(f"PASS — public media suitability: {len(present_names)} files cleared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
