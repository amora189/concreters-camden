#!/usr/bin/env python3
"""Build/check the active-page allowlist and reproducible filtered import WXR.

The immutable main WXR is read only.  The derivative removes exactly the page
items classified WITHDRAWN by D16/D21, applies the authorised D35 reader-
visible brand transform, and applies the Phase B media manifest.  Privacy
remains a separate supplementary import.
The unbuilt calculator is represented in the reconciliation but cannot enter
the allowlist until its artifact exists and a later authorised build updates
the control.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from io import BytesIO
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.preimport_safety import (  # noqa: E402
    WP,
    apply_reader_visible_brand_transform,
    classify_corex,
    items,
    parse_wxr,
    post_id,
    post_slug,
    post_status,
    post_type,
    sha256,
)
from lib.media_payload import (  # noqa: E402
    apply_media_payload_transform,
    build_manifest_rows,
    manifest_bytes,
    load_report49_plan,
    reconcile_elementor_media_references,
)
from lib.content_remediation import apply_and_register  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "camden-concreting-import.xml"
PRIVACY = ROOT / "camden-privacy-import.xml"
CALCULATOR = ROOT / "camden-calculator-import.xml"
MANIFEST = ROOT / "build" / "stage9-page-manifest.json"
READINESS = ROOT / "reports" / "23-page-readiness-v2.csv"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
DERIVED = ROOT / "build" / "46-active-main-import.xml"
DERIVED_PRIVACY = ROOT / "build" / "51-privacy-import.xml"
CLAIM_DISPOSITIONS = ROOT / "build" / "51-claim-disposition-register.json"
RESULT = ROOT / "reports" / "46-architecture-import-gate.json"
SIGHTING = ROOT / "reports" / "44-sighting-worksheet.csv"
BAND_B_REMEDIATION = ROOT / "build" / "45-media-remediation.csv"
RENAME_MAP = ROOT / "reports" / "08-image-rename-map.csv"
MEDIA_MANIFEST = ROOT / "build" / "47-media-remediation.csv"
REPORT49 = ROOT / "reports" / "49-image-completion-requirements.csv"
FACTS = ROOT / "data" / "verified-facts.yml"
TESTIMONIAL_CONTEXT = ROOT / "reports" / "45-testimonial-text-investigation.csv"

EXPECTED_IMMUTABLE_HASHES = {
    "camden-concreting-import.xml": "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884",
    "build/stage9-page-manifest.json": "578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42",
}
EXPECTED_WITHDRAWN = Counter(
    {"intersection": 35, "guide": 35, "cost_comparison": 10, "guide_hub": 1}
)
EXPECTED_ACTIVE_MAIN = Counter({"suburb": 60, "service": 10, "utility": 4, "home": 1})


def fail(message: str) -> None:
    raise AssertionError(message)


def read_csv() -> list[dict[str, str]]:
    with READINESS.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def serialise(tree: ET.ElementTree) -> bytes:
    buffer = BytesIO()
    tree.write(buffer, encoding="utf-8", xml_declaration=True, short_empty_elements=True)
    return buffer.getvalue()


def build_outputs() -> tuple[bytes, bytes, bytes, bytes, bytes, dict]:
    for rel, expected in EXPECTED_IMMUTABLE_HASHES.items():
        actual = sha256(ROOT / rel)
        if actual != expected:
            fail(f"immutable hash mismatch for {rel}: {actual} != {expected}")
    if CALCULATOR.exists():
        fail("calculator artifact now exists; this pre-calculator allowlist must be reviewed, not silently widened")

    manifest_rows = json.loads(MANIFEST.read_text(encoding="utf-8", errors="strict"))
    if len(manifest_rows) != 156:
        fail(f"manifest count {len(manifest_rows)} != 156")
    manifest = {int(row["post_id"]): row for row in manifest_rows}
    if len(manifest) != 156:
        fail("duplicate page IDs in manifest")

    readiness_rows = read_csv()
    if len(readiness_rows) != 157:
        fail(f"readiness count {len(readiness_rows)} != expected legacy 157")
    numeric_rows: dict[int, dict[str, str]] = {}
    planned = []
    for row in readiness_rows:
        raw_id = (row.get("Page ID") or "").strip()
        if raw_id.isdigit():
            pid = int(raw_id)
            if pid in numeric_rows:
                fail(f"duplicate readiness page ID {pid}")
            numeric_rows[pid] = row
        else:
            planned.append(row)
    if set(numeric_rows) != set(manifest):
        fail(
            "readiness/manifest ID mismatch: "
            f"missing={sorted(set(manifest)-set(numeric_rows))} "
            f"additional={sorted(set(numeric_rows)-set(manifest))}"
        )
    if len(planned) != 1 or "not yet built" not in (planned[0].get("Build status") or "").lower():
        fail("readiness must contain exactly one explicit unbuilt calculator row")

    main_tree = parse_wxr(MAIN)
    main_items = items(main_tree)
    main_page_items = [it for it in main_items if post_type(it) == "page"]
    main_pages = {post_id(it): it for it in main_page_items}
    if len(main_page_items) != 156 or len(main_pages) != 156:
        fail(
            f"main WXR page count/uniqueness failure: physical={len(main_page_items)}, "
            f"unique_ids={len(main_pages)}"
        )
    if set(main_pages) != set(manifest):
        fail("main WXR and manifest page IDs differ")

    withdrawn_ids: set[int] = set()
    active_ids: set[int] = set()
    withdrawn_classes: Counter[str] = Counter()
    active_classes: Counter[str] = Counter()
    allow_pages: list[dict] = []
    for pid in sorted(manifest):
        mrow = manifest[pid]
        rrow = numeric_rows[pid]
        if post_slug(main_pages[pid]) != mrow["post_name"] or rrow["Slug"] != mrow["post_name"]:
            fail(f"incorrect slug mapping for page {pid}")
        if rrow["URL"] != mrow["url"]:
            fail(f"incorrect URL mapping for page {pid}: {rrow['URL']} != {mrow['url']}")
        if rrow["Page type"] != mrow["page_type"]:
            fail(f"incorrect page-type mapping for page {pid}: {rrow['Page type']} != {mrow['page_type']}")
        if (
            post_status(main_pages[pid]) != mrow["status"]
            or rrow["Current WordPress status"] != mrow["status"]
        ):
            fail(f"incorrect status mapping for page {pid}")
        withdrawn = (rrow.get("Withdrawn") or "").strip().upper() == "YES"
        page_class = mrow["page_type"]
        if withdrawn:
            withdrawn_ids.add(pid)
            withdrawn_classes[page_class] += 1
        else:
            active_ids.add(pid)
            active_classes[page_class] += 1
            allow_pages.append(
                {
                    "page_id": pid,
                    "slug": mrow["post_name"],
                    "url": mrow["url"],
                    "page_type": page_class,
                    "intended_status": mrow["status"],
                    "import_artifact": "build/46-active-main-import.xml",
                    "evidence_readiness_state": {
                        "index_ready": rrow["Index-ready"],
                        "blocking_count": int(rrow["Blocking count"] or 0),
                        "blocking_marker_ids": [
                            value for value in rrow["Blocking marker IDs"].split(";") if value
                        ],
                        "effective_robots": rrow["Effective robots directive"],
                        "wave": rrow["Wave assignment"],
                    },
                    "authority": "reports/23-page-readiness-v2.csv joined to immutable manifest; D16/D21",
                }
            )
    if withdrawn_classes != EXPECTED_WITHDRAWN:
        fail(f"withdrawn classification {dict(withdrawn_classes)} != {dict(EXPECTED_WITHDRAWN)}")
    if active_classes != EXPECTED_ACTIVE_MAIN:
        fail(f"active main classification {dict(active_classes)} != {dict(EXPECTED_ACTIVE_MAIN)}")
    if len(withdrawn_ids) != 81 or len(active_ids) != 75:
        fail(f"expected 75 active + 81 withdrawn, got {len(active_ids)} + {len(withdrawn_ids)}")

    privacy_tree = parse_wxr(PRIVACY)
    privacy_items = items(privacy_tree)
    privacy_pages = [it for it in privacy_items if post_type(it) == "page"]
    if len(privacy_pages) != 1:
        fail(f"privacy WXR must contain one page, found {len(privacy_pages)}")
    privacy = privacy_pages[0]
    if (post_id(privacy), post_slug(privacy), post_status(privacy)) != (1600, "privacy-policy", "draft"):
        fail("privacy page identity/status does not match D31")
    main_occupied = {post_id(it) for it in main_items}
    privacy_occupied = [post_id(it) for it in privacy_items]
    if len(privacy_occupied) != len(set(privacy_occupied)):
        fail("privacy WXR contains duplicate occupied IDs")
    collisions = main_occupied & set(privacy_occupied)
    if collisions:
        fail(f"privacy WXR IDs collide with main WXR: {sorted(collisions)}")
    allow_pages.append(
        {
            "page_id": 1600,
            "slug": "privacy-policy",
            "url": "/privacy-policy/",
            "page_type": "utility",
            "intended_status": "draft",
            "import_artifact": "build/51-privacy-import.xml",
            "evidence_readiness_state": {
                "index_ready": "no",
                "blocking_count": 5,
                "blocking_marker_ids": [],
                "effective_robots": "noindex,follow",
                "wave": "none — accountable-entity and privacy-system markers unresolved",
            },
            "authority": "DECISION-06 D31; camden-privacy-import.xml",
        }
    )
    if (
        len({p["page_id"] for p in allow_pages}) != 76
        or len({p["slug"] for p in allow_pages}) != 76
        or len({p["url"] for p in allow_pages}) != 76
    ):
        fail("allowlist page IDs/slugs/URLs are not unique across main + privacy")

    # Filter only page items. Non-page records remain unchanged so the derivative
    # preserves the original attachment/menu/kit/custom-CSS provenance.
    channel = main_tree.getroot().find("./channel")
    if channel is None:
        fail("main WXR channel absent")
    for item in list(channel.findall("item")):
        if post_type(item) == "page" and post_id(item) in withdrawn_ids:
            channel.remove(item)

    baseline_brand = classify_corex(parse_wxr(MAIN))
    if baseline_brand["unknown"]:
        fail(f"unattributed CoreX baseline paths: {baseline_brand['unknown']}")
    if (
        baseline_brand["total"],
        baseline_brand["reader_visible"],
        baseline_brand["nonvisible_filenames_urls_slugs"],
    ) != (466, 366, 100):
        fail(f"CoreX baseline no longer reconciles 466 -> 366 + 100: {baseline_brand}")
    transform = apply_reader_visible_brand_transform(main_tree)
    pre_media_main_tree = ET.ElementTree(copy.deepcopy(main_tree.getroot()))
    report49_plan = load_report49_plan(REPORT49)
    media_rows = build_manifest_rows(RENAME_MAP, SIGHTING, BAND_B_REMEDIATION, REPORT49)
    media_transform = apply_media_payload_transform(main_tree, media_rows, report49_plan)
    facts = yaml.safe_load(FACTS.read_text(encoding="utf-8", errors="strict"))
    allowed_by_id = {int(row["page_id"]): row for row in allow_pages}
    claims_transform, claim_register = apply_and_register(
        main_tree,
        privacy_tree,
        pre_media_main_tree,
        allowed_by_id,
        facts,
        TESTIMONIAL_CONTEXT,
    )
    target_brand = classify_corex(main_tree)
    if target_brand["unknown"] or target_brand["reader_visible"]:
        fail(f"reader-visible CoreX remains in derivative: {target_brand}")
    derived_page_items = [it for it in items(main_tree) if post_type(it) == "page"]
    derived_pages = {post_id(it) for it in derived_page_items}
    if len(derived_page_items) != 75 or derived_pages != active_ids:
        fail(
            f"derived page parity failure missing={sorted(active_ids-derived_pages)} "
            f"additional={sorted(derived_pages-active_ids)}"
        )

    derived_attachment_items = [it for it in items(main_tree) if post_type(it) == "attachment"]
    derived_attachment_ids = {post_id(it) for it in derived_attachment_items}
    permitted_attachment_ids = {
        int(row["attachment_id"])
        for row in media_rows
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    if (
        len(derived_attachment_items) != len(permitted_attachment_ids)
        or derived_attachment_ids != permitted_attachment_ids
    ):
        fail(
            "derived media payload differs from the generated permitted attachment set; "
            f"physical={len(derived_attachment_items)}, expected={len(permitted_attachment_ids)}, "
            f"missing={sorted(permitted_attachment_ids-derived_attachment_ids)}, "
            f"additional={sorted(derived_attachment_ids-permitted_attachment_ids)}"
        )
    media_references, independent_media_references = reconcile_elementor_media_references(main_tree)
    unresolved_media = [
        row for row in media_references if row["attachment_id"] not in derived_attachment_ids
    ]
    if unresolved_media:
        fail(f"Elementor references do not resolve to permitted attachment records: {unresolved_media[:10]}")

    raw_derivative = ET.tostring(main_tree.getroot(), encoding="unicode")
    for row in media_rows:
        attachment_id = int(row["attachment_id"])
        stale_stem = Path(row["current_filename"]).stem
        if row["payload_action"] in {"EXCLUDE", "HOLD"}:
            if (
                attachment_id in derived_attachment_ids
                or row["current_filename"] in raw_derivative
                or stale_stem in raw_derivative
            ):
                fail(f"excluded/held attachment {attachment_id} remains in the derivative")
        elif row["payload_action"] == "RENAME":
            if row["current_filename"] in raw_derivative or stale_stem in raw_derivative:
                fail(f"attachment {attachment_id} stale filename remains in the derivative")
            if row["target_filename"] not in raw_derivative:
                fail(f"attachment {attachment_id} target filename absent from the derivative")
    if "REAL_PHOTO_PENDING" in raw_derivative or "local-work-card" in raw_derivative:
        fail("D32 evidential module residue remains in the derivative")
    if any(post_type(it) == "custom_css" for it in items(main_tree)):
        fail("wp_css/custom_css record remains in the derivative")

    raw_privacy = ET.tostring(privacy_tree.getroot(), encoding="unicode")
    privacy_markers = raw_privacy.count("[[PLACEHOLDER:") + raw_privacy.count("[[VERIFY:")
    if privacy_markers != 5:
        fail(f"derived privacy marker count {privacy_markers} != 5 genuine blockers")
    if "[[PLACEHOLDER: verified Structure Co ABN]]" in raw_privacy or "ABN" in raw_privacy:
        fail("ABN assertion/placeholder remains in derived privacy policy")

    derived_bytes = serialise(main_tree)
    privacy_bytes = serialise(privacy_tree)
    # Reparse the exact bytes which will be written; do not trust only the in-memory tree.
    reparsed = ET.ElementTree(ET.fromstring(derived_bytes))
    reparsed_page_items = [it for it in items(reparsed) if post_type(it) == "page"]
    reparsed_pages = {post_id(it) for it in reparsed_page_items}
    if len(reparsed_page_items) != 75 or reparsed_pages != active_ids:
        fail("serialised derivative changed the permitted page set")
    derived_hash = hashlib.sha256(derived_bytes).hexdigest().upper()
    privacy_hash = hashlib.sha256(privacy_bytes).hexdigest().upper()
    claim_register_bytes = (
        json.dumps(claim_register, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    allowlist_doc = {
        "schema_version": "1.0",
        "generated_by": "scripts/46-architecture-import-gate.py",
        "fail_closed": True,
        "source_provenance": {
            "main_wxr": {"path": MAIN.name, "sha256": sha256(MAIN), "physical_pages": 156},
            "manifest": {"path": MANIFEST.relative_to(ROOT).as_posix(), "sha256": sha256(MANIFEST)},
            "readiness": {"path": READINESS.relative_to(ROOT).as_posix(), "sha256": sha256(READINESS)},
            "privacy_wxr": {"path": PRIVACY.name, "sha256": sha256(PRIVACY)},
            "owner_identity_claims_authority": {
                "source": "owner attestation and remediation authority, 21 August 2026",
                "verified_facts": {
                    "path": FACTS.relative_to(ROOT).as_posix(),
                    "sha256": sha256(FACTS),
                },
            },
            "owner_image_approval": {
                "path": REPORT49.relative_to(ROOT).as_posix(),
                "sha256": sha256(REPORT49),
                "worksheet": SIGHTING.relative_to(ROOT).as_posix(),
                "worksheet_sha256": sha256(SIGHTING),
                "date": "2026-08-20",
            },
            "decisions": [
                "D16", "D18", "D19", "D20", "D21", "D22", "D24",
                "D31", "D32", "D35", "D36", "owner Band B verdicts",
                "owner approval dated 20 August 2026; Report 49 exact image plan",
            ],
        },
        "inventory_reconciliation": {
            "main_wxr_physical_pages": 156,
            "active_main_pages": 75,
            "withdrawn_main_pages": 81,
            "withdrawn_by_class": dict(sorted(withdrawn_classes.items())),
            "privacy_pages": 1,
            "built_allowed_pages": 76,
            "unbuilt_calculator": 1,
            "logical_active_architecture": 77,
            "logical_rows_including_withdrawn": 158,
            "readiness_rows_before_control": 157,
            "classification_discrepancy": "privacy is absent from readiness; the unbuilt calculator is present",
            "arithmetic": "156 main = 75 active + 81 withdrawn; 75 + privacy 1 = 76 built allowed; + calculator 1 unbuilt = 77 logical active; 156 + privacy 1 + calculator 1 = 158 logical rows",
        },
        "derived_import": {
            "path": DERIVED.relative_to(ROOT).as_posix(),
            "sha256": derived_hash,
            "pages": 75,
            "withdrawn_pages": 0,
            "privacy_imported_separately": DERIVED_PRIVACY.relative_to(ROOT).as_posix(),
            "privacy_sha256": privacy_hash,
            "privacy_blocking_markers": privacy_markers,
            "calculator_included": False,
            "brand_transform": transform,
            "corex_baseline": baseline_brand,
            "corex_derivative": target_brand,
            "media_transform": media_transform,
            "claims_transform": claims_transform,
            "permitted_attachment_records": len(derived_attachment_ids),
            "elementor_media_references": len(media_references),
            "independent_elementor_media_references": len(independent_media_references),
            "elementor_media_detectors_reconciled": True,
            "all_elementor_media_references_resolve": True,
            "media_manifest": {
                "path": MEDIA_MANIFEST.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(manifest_bytes(media_rows)).hexdigest().upper(),
            },
            "claim_disposition_register": {
                "path": CLAIM_DISPOSITIONS.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(claim_register_bytes).hexdigest().upper(),
            },
        },
        "pages": sorted(allow_pages, key=lambda row: row["page_id"]),
    }
    allowlist_bytes = (json.dumps(allowlist_doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    result_doc = {
        "result": "PASS",
        "allowed_pages": 76,
        "active_main": 75,
        "privacy": 1,
        "calculator": "ABSENT — correctly excluded",
        "withdrawn": 81,
        "withdrawn_by_class": dict(sorted(withdrawn_classes.items())),
        "derived_sha256": derived_hash,
        "privacy_derivative_sha256": privacy_hash,
        "immutable_main_sha256": sha256(MAIN),
        "permitted_attachment_records": len(derived_attachment_ids),
        "elementor_media_references": len(media_references),
        "independent_elementor_media_references": len(independent_media_references),
        "elementor_media_detectors_reconciled": True,
        "media_transform": media_transform,
        "claims_transform": claims_transform,
    }
    return (
        allowlist_bytes,
        derived_bytes,
        privacy_bytes,
        manifest_bytes(media_rows),
        claim_register_bytes,
        result_doc,
    )


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated controls are absent/stale")
    args = parser.parse_args()
    try:
        (
            allowlist_bytes,
            derived_bytes,
            privacy_bytes,
            media_manifest_bytes,
            claim_register_bytes,
            result,
        ) = build_outputs()
        if args.check:
            stale = []
            if not ALLOWLIST.exists() or ALLOWLIST.read_bytes() != allowlist_bytes:
                stale.append(ALLOWLIST.relative_to(ROOT).as_posix())
            if not DERIVED.exists() or DERIVED.read_bytes() != derived_bytes:
                stale.append(DERIVED.relative_to(ROOT).as_posix())
            if not DERIVED_PRIVACY.exists() or DERIVED_PRIVACY.read_bytes() != privacy_bytes:
                stale.append(DERIVED_PRIVACY.relative_to(ROOT).as_posix())
            if not MEDIA_MANIFEST.exists() or MEDIA_MANIFEST.read_bytes() != media_manifest_bytes:
                stale.append(MEDIA_MANIFEST.relative_to(ROOT).as_posix())
            if not CLAIM_DISPOSITIONS.exists() or CLAIM_DISPOSITIONS.read_bytes() != claim_register_bytes:
                stale.append(CLAIM_DISPOSITIONS.relative_to(ROOT).as_posix())
            if stale:
                fail("generated controls absent or stale: " + ", ".join(stale))
        else:
            ALLOWLIST.write_bytes(allowlist_bytes)
            DERIVED.write_bytes(derived_bytes)
            DERIVED_PRIVACY.write_bytes(privacy_bytes)
            MEDIA_MANIFEST.write_bytes(media_manifest_bytes)
            CLAIM_DISPOSITIONS.write_bytes(claim_register_bytes)
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            "PASS — active/import parity: 156 main = 75 allowed + 81 withdrawn; "
            "privacy=1; calculator absent; built allowlist=76"
        )
        print(f"derived sha256={result['derived_sha256']}")
        return 0
    except Exception as exc:
        result = {"result": "FAIL", "error": str(exc)}
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"FAIL — active/import parity: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
