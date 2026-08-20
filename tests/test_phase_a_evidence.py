from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "build/53-service-specification-matrix.json"
MAP_PATH = ROOT / "build/53-council-suburb-map.json"
CSV_PATH = ROOT / "reports/53-service-specification-matrix.csv"

CSV_COLUMNS = [
    "service", "field", "current_claim", "current_value", "classification",
    "resolved_value", "public_wording", "source_title", "source_url",
    "source_date", "source_page", "access_date", "jurisdiction", "verified",
    "remaining_input", "notes",
]


def load_matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def test_report53_outputs_are_reproducible() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/53-phase-a-evidence.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_exact_ten_by_nine_matrix_and_csv_contract() -> None:
    payload = load_matrix()
    rows = payload["matrix"]
    assert len(rows) == 90
    assert len({row["service"] for row in rows}) == 10
    assert Counter(row["service"] for row in rows) == Counter({row["service"]: 9 for row in rows})
    assert all(len({row["field"] for row in rows if row["service"] == slug}) == 9 for slug in {r["service"] for r in rows})
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        csv_rows = list(reader)
        assert reader.fieldnames == CSV_COLUMNS
    assert len(csv_rows) == 90


def test_unresolved_cells_are_explicit_and_not_marked_verified() -> None:
    payload = load_matrix()
    unresolved = [row for row in payload["matrix"] if row["classification"] == "UNRESOLVED"]
    assert {(row["service"], row["field"]) for row in unresolved} == {
        ("concrete-slabs-south-west-sydney", "curing requirements"),
        ("shed-and-garage-slabs-south-west-sydney", "curing requirements"),
    }
    assert all(row["verified"] == "false" and row["remaining_input"] for row in unresolved)
    assert payload["summary"]["verified_resolved_cells"] == 88
    assert payload["summary"]["services_with_all_research_cells_resolved"] == 8
    assert payload["summary"]["services_formally_unblocked"] == 0


def test_sources_are_authoritative_opened_and_not_disallowed() -> None:
    payload = load_matrix()
    disallowed = ("competitor", "forum", "reddit.com", "quora.com", "blogspot", "medium.com")
    assert payload["sources"]
    for source in payload["sources"].values():
        assert source["access_verified"] is True
        assert source["url"].startswith("https://")
        assert not any(term in source["url"].lower() for term in disallowed)
        assert source["title"] and source["publisher"] and source["page"] and source["access_method"]
    for row in payload["matrix"]:
        assert row["source_title"] and row["source_url"] and row["source_page"]
        assert row["access_date"] == "2026-08-21"


def test_existing_claim_and_figure_audits_are_complete_and_exact() -> None:
    payload = load_matrix()
    claims = payload["current_claim_audit"]
    figures = payload["figure_register_audit"]
    assert claims
    assert all(row["exact_claim"] and row["placement"] and row["page_id"] for row in claims)
    assert all(row["classification"] in {"verified", "contradicted", "project-specific", "provider-specific", "obsolete", "unsupported"} for row in claims)
    assert len(figures) == 91
    assert all(row["classification"] == "unsupported" for row in figures)
    with (ROOT / "reports/35-figure-provenance.csv").open(encoding="utf-8-sig", newline="") as handle:
        register = list(csv.DictReader(handle))
    assert len(register) == 214
    assert len([row for row in register if row["page_class"] == "service"]) == 91


def test_service_inventory_and_d23_ledger_state_are_fail_closed() -> None:
    payload = load_matrix()
    inventory = payload["service_inventory"]
    assert inventory["count"] == 10
    assert set(inventory["reconciled_artifacts"].values()) == {10}
    assert inventory["legacy_service_specs"]["verified_true"] == 0
    assert inventory["legacy_service_specs"]["verified_false"] == 91
    assert inventory["legacy_service_specs"]["malformed_service_specific_value_lines"] == 10
    assert inventory["legacy_service_specs"]["formal_precondition"] == "BLOCKED"
    ledger_text = (ROOT / "build/21-spec-ledger.json").read_text(encoding="utf-8")
    assert "No service page copy is written until data/service-specs.yml is populated" in ledger_text
    assert "Two populations are tracked separately and never merged" in ledger_text


def test_council_suburb_map_reconciles_all_active_pages() -> None:
    payload = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    assert payload["counts"] == {
        "active_suburb_pages": 60,
        "split_localities": 8,
        "artifact_contradictions": 2,
        "lot_level_checks_required": 8,
    }
    assert len(payload["suburbs"]) == 60
    assert {row["suburb_slug"] for row in payload["artifact_divergences"]} == {"camden-park", "theresa-park"}
    splits = {row["suburb_slug"] for row in payload["suburbs"] if row["assignment_status"] == "split-locality"}
    assert splits == {"bringelly", "leppington", "rossmore", "edmondson-park", "kemps-creek", "cawdor", "cecil-park", "ingleburn"}
    assert all(row["citations"] and all(c["url"] and c["access_date"] == "2026-08-21" for c in row["citations"]) for row in payload["suburbs"])
    assert all(row["lot_level_check_required"] for row in payload["suburbs"] if row["suburb_slug"] in splits)

