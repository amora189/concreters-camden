from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WP = "{http://wordpress.org/export/1.2/}"


def run_script(name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8", errors="strict"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_active_import_control_is_exact_and_reproducible() -> None:
    generated = run_script("46-architecture-import-gate.py")
    assert generated.returncode == 0, generated.stderr
    derivative = ROOT / "build" / "46-active-main-import.xml"
    first_hash = sha256(derivative)

    checked = run_script("46-architecture-import-gate.py", "--check")
    assert checked.returncode == 0, checked.stderr
    assert sha256(derivative) == first_hash

    control = load_json("build/46-active-page-allowlist.json")
    pages = control["pages"]
    assert len(pages) == 76
    assert len({page["page_id"] for page in pages}) == 76
    assert len({page["slug"] for page in pages}) == 76
    assert Counter(page["page_type"] for page in pages) == {
        "suburb": 60,
        "service": 10,
        "utility": 5,
        "home": 1,
    }
    assert any(page["page_id"] == 1600 and page["slug"] == "privacy-policy" for page in pages)
    assert not any("crossover-requirements" in page["slug"] for page in pages)

    tree = ET.parse(derivative)
    derivative_pages = [
        item
        for item in tree.getroot().findall("./channel/item")
        if (item.findtext(WP + "post_type") or "").strip() == "page"
    ]
    assert len(derivative_pages) == 75
    assert {
        int((item.findtext(WP + "post_id") or "0").strip()) for item in derivative_pages
    } == {
        page["page_id"] for page in pages if page["import_artifact"] == "build/46-active-main-import.xml"
    }
    derivative_attachments = [
        item
        for item in tree.getroot().findall("./channel/item")
        if (item.findtext(WP + "post_type") or "").strip() == "attachment"
    ]
    assert len(derivative_attachments) == 55
    raw = derivative.read_text(encoding="utf-8", errors="strict")
    assert "REAL_PHOTO_PENDING" not in raw
    assert "local-work-card" not in raw
    assert "concrete-tesimonial-4-camden-46.webp" not in raw
    assert "exposed-aggregate-front-paths-46.webp" in raw


def test_source_brand_gate_asserts_the_transformed_result() -> None:
    result = run_script("46-source-brand-gate.py")
    assert result.returncode == 0, result.stderr
    report = load_json("reports/46-source-brand-gate.json")
    assert report["baseline"]["total"] == 466
    assert report["baseline"]["reader_visible"] == 366
    assert report["baseline"]["nonvisible_filenames_urls_slugs"] == 100
    assert report["active_derivative"]["reader_visible"] == 0
    assert report["reader_visible_disposition"] == {
        "renamed_in_active_derivative": 183,
        "excluded_with_withdrawn_pages": 183,
        "remaining": 0,
    }


def test_claim_gate_passes_only_after_all_current_claims_are_supported() -> None:
    result = run_script("46-claim-evidence-gate.py")
    assert result.returncode == 0, result.stderr
    report = load_json("reports/46-claim-evidence-gate.json")
    totals = report["totals"]
    assert totals["occurrences"] == 16
    assert totals["supported"] == 16
    assert totals["unsupported"] == 0
    assert totals["pages_with_unsupported_claims"] == 0
    assert totals["legacy_occurrences_dispositioned"] == 232
    assert totals["legacy_unsupported_dispositioned"] == 228
    assert totals["additional_blind_spot_occurrences_dispositioned"] == 309
    assert totals["current_by_category"] == {
        "response_time_promise": 1,
        "workmanship_guarantee_warranty": 15,
    }
    register = load_json("build/46-claim-register.json")
    assert register["generated_by"] == "scripts/46-claim-evidence-gate.py"
    assert register["fail_closed"] is True
    assert register["result"] == "PASS"
    assert register["totals"] == totals


def test_public_media_gate_passes_exact_owner_approved_band_a_plan() -> None:
    result = run_script("46-public-media-gate.py")
    assert result.returncode == 0, result.stderr
    report = load_json("reports/46-public-media-gate.json")
    assert len(report["band_a"]) == 16
    assert Counter(row["verdict"] for row in report["band_a"]) == {
        "GENERIC": 10,
        "UNUSABLE": 6,
    }
    assert Counter(row["payload_action"] for row in report["band_a"]) == {
        "RENAME": 10,
        "EXCLUDE": 6,
    }
    assert all(row["present_in_public_intake"] == (row["verdict"] == "GENERIC") for row in report["band_a"])
    assert all(row["present_in_derived_wxr"] == (row["verdict"] == "GENERIC") for row in report["band_a"])
    assert len(report["band_b"]) == 9
    assert all(row["result"] == "PASS" for row in report["band_b"])
    assert all(row["derived_wxr_remediated"] for row in report["band_b"])
    assert report["errors"] == []
    assert report["unresolved_elementor_media_references"] == []
    assert report["elementor_media_references"] == 440
    assert report["independent_elementor_media_references"] == 440
    assert report["elementor_media_detectors_reconciled"] is True
    assert report["band_a_generic_placement_contract"] == {
        "expected": 75,
        "actual": 75,
        "reconciled": True,
    }
    policy = load_json("build/46-public-media-policy.json")
    assert len(policy["retired_brand_ids"]) == 7
    assert policy["band_b_unusable_ids"] == [280, 1067]
    assert policy["held_band_a_ids"] == []
    assert policy["band_a_denied_ids"] == [480, 481, 482, 907, 956, 1187]
    assert policy["denied_assets"] == report["denied_assets"]


def test_post_import_verifier_is_read_only_and_covers_required_outputs() -> None:
    php = (ROOT / "staging-authoritative" / "scripts" / "verify-post-import.php").read_text(
        encoding="utf-8", errors="strict"
    )
    shell = (ROOT / "staging-authoritative" / "scripts" / "verify-post-import.sh").read_text(
        encoding="utf-8", errors="strict"
    )
    required_assertions = [
        "active page inventory exact",
        "privacy page present",
        "calculator absent until built",
        "Astra wp_css excluded / custom CSS post 893 absent",
        "replaced header logo slot uses Structure Co horizontal wordmark",
        "replaced favicon slot uses Structure Co icon",
        "menu location",
        "denied attachment",
        "denied media binary",
        "unusable/retired media slots removed",
        "reader-visible CoreX/E&T/tagline absent",
        "schema matches verified identity state",
        "no registered unsupported claim survives",
        "all Elementor media references resolve",
        "permalink/canonical path matches allowlist",
        "page-level indexability matches approved wave",
        "current approved wave remains globally noindex",
    ]
    for assertion in required_assertions:
        assert assertion in php
    forbidden_mutations = [
        "wp_insert_post(",
        "wp_update_post(",
        "wp_delete_post(",
        "update_option(",
        "delete_option(",
        "$wpdb->insert(",
        "$wpdb->update(",
        "$wpdb->delete(",
        "$wpdb->query(",
    ]
    for mutation in forbidden_mutations:
        assert mutation not in php
    assert "This pass installs the verifier but does not run it." in shell
    assert "eval-file" in shell
