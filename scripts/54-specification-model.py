"""Validate the independent-provider specification disposition model.

The model resolves claim disposition, not unsupported construction numbers.  A cell
with ``claim-removed`` keeps ``verified: false`` and cannot emit numeric wording.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "data" / "service-specs.yml"
LEDGER = ROOT / "build" / "54-independent-provider-decision.json"
DERIVATIVE = ROOT / "build" / "46-active-main-import.xml"
REPORT = ROOT / "reports" / "54-specification-model-validation.json"
WP = "http://wordpress.org/export/1.2/"
NS = {"wp": WP}

FIELDS = [
    "concrete thickness",
    "concrete strength/grade",
    "reinforcement/mesh",
    "base preparation",
    "joint type and spacing",
    "curing requirements",
    "drainage/fall",
    "edges/formwork",
    "service-specific requirements",
]
CLASSES = {
    "evidenced-fixed-value",
    "council-specific",
    "design-specific",
    "product-specific",
    "site-specific",
    "provider-confirmed",
    "not-applicable",
    "unresolved",
}
REPORT_CLASS = {
    "council-specific": "COUNCIL-SPECIFIC",
    "design-specific": "DESIGN-SPECIFIC",
    "product-specific": "PRODUCT-SPECIFIC",
    "site-specific": "SITE-SPECIFIC",
    "provider-confirmed": {"PROVIDER-METHOD", "UNRESOLVED"},
}
NUMERIC_OR_METHOD = re.compile(
    r"(?i)(?:\b\d+(?:\.\d+)?\s*(?:mpa|mm|cm|m|%|days?|hours?)\b|\bsl\d+\b|\b\d+\s*:\s*\d+\b|fixed\s+(?:price|method|period)|we\s+(?:build|pour|install|construct))"
)
CURING_NUMBER = re.compile(r"(?i)(?:curing|cure|protection).{0,100}\b\d+(?:\.\d+)?\s*(?:hours?|days?|h|d)\b")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_model() -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    errors: list[str] = []
    try:
        model = yaml.safe_load(MODEL.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {}, {}, [f"model YAML failed to parse: {exc}"]
    try:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        return model or {}, {}, [f"decision ledger failed to parse: {exc}"]
    if model.get("schema_version") != "2.0":
        fail(errors, "schema_version is not 2.0")
    if model.get("operating_model") != "independent-provider-coordination":
        fail(errors, "independent-provider operating model missing")
    services = model.get("services")
    if not isinstance(services, dict) or len(services) != 10:
        fail(errors, f"expected 10 services, found {len(services) if isinstance(services, dict) else 0}")
        services = services if isinstance(services, dict) else {}
    wording = model.get("approved_public_wording", {})
    if not isinstance(wording, dict):
        fail(errors, "approved_public_wording is not a mapping")
        wording = {}
    total = 0
    source_rows: dict[tuple[str, str], str] = {}
    csv_path = ROOT / "reports" / "53-service-specification-matrix.csv"
    import csv

    with csv_path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            source_rows[(row["service"], row["field"])] = row["classification"]
    for slug, service in services.items():
        cells = service.get("cells") if isinstance(service, dict) else None
        if not isinstance(cells, dict) or set(cells) != set(FIELDS):
            fail(errors, f"{slug}: fields do not exactly match the nine-cell contract")
            continue
        for field, classification in cells.items():
            total += 1
            if classification not in CLASSES:
                fail(errors, f"{slug}/{field}: invalid classification {classification!r}")
                continue
            if classification not in wording:
                fail(errors, f"{slug}/{field}: no approved public wording for {classification}")
            source = source_rows.get((slug, field))
            expected = REPORT_CLASS.get(classification)
            if expected is not None and source not in (expected if isinstance(expected, set) else {expected}):
                fail(errors, f"{slug}/{field}: classification {classification} disagrees with Report 53 {source}")
            if classification == "unresolved":
                fail(errors, f"{slug}/{field}: unresolved cell cannot emit public wording")
    if total != 90:
        fail(errors, f"expected 90 cells, found {total}")
    curing = model.get("curing_disposition", {})
    if curing.get("resolution") != "claim-removed" or curing.get("verified") is not False:
        fail(errors, "curing disposition must be claim-removed with verified:false")
    if curing.get("public_wording") != ledger.get("curing_public_wording"):
        fail(errors, "curing wording differs from owner decision ledger")
    if ledger.get("decision_id") != "DECISION-09":
        fail(errors, "DECISION-09 ledger missing")
    return model, ledger, errors


def service_texts() -> dict[str, str]:
    if not DERIVATIVE.exists():
        return {}
    root = ET.parse(DERIVATIVE).getroot()
    result: dict[str, str] = {}
    for item in root.findall(".//item"):
        if item.findtext("wp:post_type", namespaces=NS) != "page":
            continue
        slug = item.findtext("wp:post_name", namespaces=NS) or ""
        if slug not in {
            "concrete-driveways-south-west-sydney",
            "concrete-driveway-replacement-south-west-sydney",
            "concrete-slabs-south-west-sydney",
            "shed-and-garage-slabs-south-west-sydney",
            "exposed-aggregate-south-west-sydney",
            "decorative-concrete-south-west-sydney",
            "concrete-patios-south-west-sydney",
            "concrete-paths-south-west-sydney",
            "concrete-crossovers-and-laybacks-south-west-sydney",
            "commercial-concreting-south-west-sydney",
        }:
            continue
        chunks: list[str] = []
        for meta in item.findall(".//wp:postmeta", NS):
            if meta.findtext("wp:meta_key", namespaces=NS) != "_elementor_data":
                continue
            raw = meta.findtext("wp:meta_value", namespaces=NS) or ""
            try:
                tree = json.loads(raw)
            except json.JSONDecodeError:
                continue

            def walk(value: Any) -> None:
                if isinstance(value, str):
                    chunks.append(value)
                elif isinstance(value, dict):
                    for child in value.values():
                        walk(child)
                elif isinstance(value, list):
                    for child in value:
                        walk(child)

            walk(tree)
        result[slug] = " ".join(chunks)
    return result


def validate_derivative(errors: list[str]) -> dict[str, Any]:
    texts = service_texts()
    if len(texts) != 10:
        fail(errors, f"derivative service page count is {len(texts)}, expected 10")
    curing_wording = "Curing requirements are confirmed for the selected concrete system and project conditions before placement."
    bad: dict[str, list[str]] = {}
    for slug, text in texts.items():
        findings: list[str] = []
        if NUMERIC_OR_METHOD.search(text):
            findings.append("unsupported numeric or direct-method claim")
        if CURING_NUMBER.search(text):
            findings.append("numeric curing period")
        if "Curing requirements are confirmed" not in text and "curing" in text.lower():
            findings.append("curing wording not owner-approved")
        if any(token in text for token in ("REAL_PHOTO_PENDING", "VERIFY", "CoreX", "Melbourne")):
            findings.append("placeholder or retired-brand residue")
        if findings:
            bad[slug] = findings
    if bad:
        fail(errors, f"derivative service claim scan failed: {bad}")
    return {"service_pages": len(texts), "bad_pages": bad, "status": "PASS" if not bad else "FAIL"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--derivative", action="store_true", help="also scan the active derivative service payload")
    args = parser.parse_args()
    model, ledger, errors = load_model()
    derivative = validate_derivative(errors) if args.derivative else {"status": "NOT_RUN"}
    result = {
        "model": str(MODEL.relative_to(ROOT)),
        "decision": str(LEDGER.relative_to(ROOT)),
        "cells": 90,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "derivative": derivative,
        "numeric_output_prohibited_without_evidence": bool(model.get("numeric_output_prohibited_without_evidence")),
        "ledger_decision_id": ledger.get("decision_id"),
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
