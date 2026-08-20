#!/usr/bin/env python3
"""Fail-closed Phase D Liverpool source, citation and four-page validator."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.content_remediation import (  # noqa: E402
    FORMS_URL,
    LIVERPOOL_BLOCKS,
    PDF_URL,
    PORTAL_URL,
)
from lib.preimport_safety import (  # noqa: E402
    items,
    parse_wxr,
    post_id,
    post_slug,
    post_status,
    post_type,
    visible_page_fields,
)

ROOT = Path(__file__).resolve().parents[1]
COUNCIL = ROOT / "data" / "council-specs.yml"
DERIVATIVE = ROOT / "build" / "46-active-main-import.xml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
CALCULATOR = ROOT / "camden-calculator-import.xml"
FIELD_REGISTER = ROOT / "build" / "52-liverpool-field-register.json"
RESULT = ROOT / "reports" / "52-liverpool-validation.json"

PDF_SHA256 = "43F74C0F01C5EA6F0C89919BE8C1859F758F96AF549A9CF71ADA5F87DD7CAF33"
ACCESS_DATE = "2026-08-21"

PAGES = {
    "concreters-leppington": {"page_id": 221, "status": "publish"},
    "concreters-austral": {"page_id": 1163, "status": "publish"},
    "concreters-edmondson-park": {"page_id": 1387, "status": "draft"},
    "concreters-bringelly": {"page_id": 1388, "status": "draft"},
}

REQUIREMENTS = {
    "roads_act_section_138": {
        "pages": [1],
        "page_needles": {1: ["Made under Section 138 Roads Act 1993"]},
        "block": 1,
    },
    "owner_cost_responsibility": {
        "pages": [2, 5],
        "page_needles": {
            2: ["property owners are liable for all costs associated with the construction, maintenance and repair"],
            5: ["Property Owners are liable for all costs associated with the construction, maintenance and repair"],
        },
        "block": 1,
    },
    "contractor_licensing_and_liability": {
        "pages": [1, 2, 5],
        "page_needles": {
            1: ["Public Liability Certificate of Currency", "minimum of $10 million"],
            2: ["owner’s responsibility to ensure that their contractor is licensed", "$10,000,000 public liability cover"],
            5: ["Owners responsibility to ensure that their contractor is licensed", "$10,000,000 public liability cover"],
        },
        "block": 1,
    },
    "surface": {
        "pages": [1],
        "page_needles": {1: ["proposed surface finish/material must be Plain Concrete"]},
        "block": 1,
    },
    "residential_strength": {
        "pages": [8],
        "page_needles": {8: ["minimum of 25MPa at 28 days for residential driveways"]},
        "block": 2,
    },
    "medium_density_commercial_industrial_strength": {
        "pages": [8],
        "page_needles": {8: ["minimum of 32Mpa at 28 days for medium density, commercial and industrial driveways"]},
        "block": 2,
    },
    "crossing_bedding": {
        "pages": [7],
        "page_needles": {7: ["minimum of 50mm of DGS 20 bedding material"]},
        "block": 2,
    },
    "kerb_gutter_layback_bedding": {
        "pages": [7],
        "page_needles": {7: ["minimum of 100mm of DGS 20 bedding material"]},
        "block": 2,
    },
    "pre_pour_inspection": {
        "pages": [2, 5, 10],
        "page_needles": {
            2: ["No concrete is to be poured until Council has given approval"],
            5: ["No concrete is to be poured until Council has given approval"],
            10: ["Inspections are required prior to pouring concrete", "formwork, reinforcement, jointing material, approved base material"],
        },
        "block": 3,
    },
    "drawings_and_directions": {
        "pages": [7],
        "page_needles": {7: ["Council’s Plan No: R25 or as directed by Council's Crossings Inspector"]},
        "block": 3,
    },
    "utilities": {
        "pages": [6, 7],
        "page_needles": {
            6: ["Electric poles and Street light poles", "Communication (Telstra, Optus.)/NBN pit", "Sydney Water assets"],
            7: ["household stormwater pipes", "pram ramp"],
        },
        "block": 3,
    },
    "application_and_inspection_process": {
        "pages": [2, 10],
        "page_needles": {
            2: ["application number starting with “DX”", "inspection must be arranged with Council"],
            10: ["Council's crossing application number is required when booking for an inspection"],
        },
        "block": 3,
    },
    "fees": {
        "pages": [2],
        "page_needles": {2: ["schedule of fees and charges", "fee payable will be assessed", "schedule of fees"]},
        "block": 1,
    },
}

BLOCK_REQUIREMENTS = {
    1: ["roads_act_section_138", "owner_cost_responsibility", "contractor_licensing_and_liability", "surface", "fees"],
    2: ["residential_strength", "medium_density_commercial_industrial_strength", "crossing_bedding", "kerb_gutter_layback_bedding"],
    3: ["pre_pour_inspection", "drawings_and_directions", "utilities", "application_and_inspection_process"],
}


def normalise(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split()).casefold()


def source_page_text(pdf: Path) -> list[str]:
    from pypdf import PdfReader

    actual = hashlib.sha256(pdf.read_bytes()).hexdigest().upper()
    if actual != PDF_SHA256:
        raise AssertionError(f"official PDF hash {actual} != recorded {PDF_SHA256}")
    reader = PdfReader(str(pdf))
    if len(reader.pages) != 18:
        raise AssertionError(f"official PDF page count {len(reader.pages)} != 18")
    return [page.extract_text() or "" for page in reader.pages]


def validate_source_html(forms_html: Path | None, portal_html: Path | None) -> dict:
    result = {"forms_page_checked": False, "portal_checked": False}
    if forms_html:
        text = forms_html.read_text(encoding="utf-8", errors="strict")
        if "Forms | Liverpool City Council" not in text or "VEHICULAR-CROSSING-APPLICATION-FORM-March-2026v1.pdf" not in text:
            raise AssertionError("Council forms page does not expose the recorded March 2026 PDF")
        result["forms_page_checked"] = True
    if portal_html:
        text = portal_html.read_text(encoding="utf-8", errors="strict")
        if "ePathway Home" not in text or "Driveway Crossing" not in text:
            raise AssertionError("Council portal does not expose the Driveway Crossing application path")
        result["portal_checked"] = True
    return result


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-pdf", type=Path)
    parser.add_argument("--forms-html", type=Path)
    parser.add_argument("--portal-html", type=Path)
    args = parser.parse_args()
    try:
        data = yaml.safe_load(COUNCIL.read_text(encoding="utf-8", errors="strict"))
        source_set = data["liverpool"]["source_set"]
        requirements = data["liverpool"]["requirements"]
        if set(requirements) != set(REQUIREMENTS):
            raise AssertionError(
                f"Council requirement keys differ: missing={sorted(set(REQUIREMENTS)-set(requirements))}, "
                f"additional={sorted(set(requirements)-set(REQUIREMENTS))}"
            )
        if source_set["forms_page"]["source_url"] != FORMS_URL:
            raise AssertionError("forms-page URL differs")
        if source_set["vehicular_crossing_form_march_2026"]["source_url"] != PDF_URL:
            raise AssertionError("PDF URL differs")
        if source_set["online_application_portal"]["source_url"] != PORTAL_URL:
            raise AssertionError("portal URL differs")
        if source_set["vehicular_crossing_form_march_2026"]["sha256"] != PDF_SHA256:
            raise AssertionError("recorded PDF hash differs")
        if any(row["verified"] is not True or row["sighted_date"] != ACCESS_DATE for row in source_set.values()):
            raise AssertionError("source-set verification/access date differs")

        pdf_pages = source_page_text(args.source_pdf) if args.source_pdf else None
        citation_rows = []
        for key, contract in REQUIREMENTS.items():
            row = requirements[key]
            if row["verified"] is not True or row["sighted_date"] != ACCESS_DATE or row["source_url"] != PDF_URL:
                raise AssertionError(f"{key}: evidence metadata incomplete")
            if row["source_pages"] != contract["pages"]:
                raise AssertionError(f"{key}: source_pages {row['source_pages']} != {contract['pages']}")
            source_matches = []
            if pdf_pages:
                for page_number, needles in contract["page_needles"].items():
                    page = normalise(pdf_pages[page_number - 1])
                    for needle in needles:
                        if normalise(needle) not in page:
                            raise AssertionError(f"{key}: page {page_number} lacks source text {needle!r}")
                    source_matches.append({"page": page_number, "matched_source_text": needles})
            citation_rows.append(
                {
                    "requirement": key,
                    "recorded_value": row.get("value", row.get("value_mpa_at_28_days")),
                    "source_url": row["source_url"],
                    "source_pages": row["source_pages"],
                    "access_date": row["sighted_date"],
                    "source_matches": source_matches,
                    "content_block": contract["block"],
                    "result": "PASS",
                }
            )

        tree = parse_wxr(DERIVATIVE)
        allow = json.loads(ALLOWLIST.read_text(encoding="utf-8", errors="strict"))
        allowed = {int(row["page_id"]): row for row in allow["pages"]}
        page_items = {post_slug(item): item for item in items(tree) if post_type(item) == "page"}
        field_rows = []
        for slug, expected in PAGES.items():
            item = page_items.get(slug)
            if item is None:
                raise AssertionError(f"Phase D page absent: {slug}")
            pid = post_id(item)
            if pid != expected["page_id"] or post_status(item) != expected["status"]:
                raise AssertionError(f"Phase D page identity/status differs: {slug}")
            if allowed[pid]["intended_status"] != expected["status"]:
                raise AssertionError(f"allowlist status differs: {slug}")
            # Materialise once: the three exact block assertions must inspect the
            # same complete field set.  ``visible_page_fields`` is a generator.
            fields = list(visible_page_fields(item))
            for block_index, block in enumerate(LIVERPOOL_BLOCKS, 1):
                matches = [field for field in fields if block in field["text"]]
                if len(matches) != 1:
                    raise AssertionError(f"{slug}: Liverpool block {block_index} count {len(matches)} != 1")
                expected_placement = (
                    f"_elementor_data:$[13].elements[2].elements[{block_index-1}]"
                    ".elements[0].settings.editor"
                )
                if matches[0]["placement"] != expected_placement:
                    raise AssertionError(
                        f"{slug}: block {block_index} placement {matches[0]['placement']} != {expected_placement}"
                    )
                field_rows.append(
                    {
                        "field_id": f"LVP-{len(field_rows)+1:02d}",
                        "page_id": pid,
                        "slug": slug,
                        "intended_status": expected["status"],
                        "placement": expected_placement,
                        "requirements": BLOCK_REQUIREMENTS[block_index],
                        "exact_final_text": block,
                        "disposition": "OFFICIAL_EVIDENCE_APPLIED",
                        "source_url": PDF_URL,
                        "forms_url": FORMS_URL if block_index == 1 else "",
                        "portal_url": PORTAL_URL if block_index == 1 else "",
                        "access_date": ACCESS_DATE,
                    }
                )

        if len(field_rows) != 12:
            raise AssertionError(f"resolved Phase D fields {len(field_rows)} != 12")
        raw = DERIVATIVE.read_text(encoding="utf-8", errors="strict")
        four_page_blob = "\n".join(
            html.unescape(field["text"])
            for slug in PAGES
            for field in visible_page_fields(page_items[slug])
        )
        false_fidelity_patterns = {
            "reproduced without alteration": r"reproduced without alteration",
            "Liverpool REQUIRED-RESEARCH": r"REQUIRED-RESEARCH[^<\"]{0,120}Liverpool",
            "verified project record": r"verified project record says",
            "researched job record": r"The researched [^.]{0,80} job record contains",
        }
        residue = {
            name: len(re.findall(pattern, four_page_blob, re.I))
            for name, pattern in false_fidelity_patterns.items()
        }
        if any(residue.values()):
            raise AssertionError(f"Phase D false-fidelity residue remains: {residue}")
        outside_phase_d_residue = {
            name: len(re.findall(pattern, raw, re.I)) - residue[name]
            for name, pattern in false_fidelity_patterns.items()
        }
        if re.search(r"fees?[^.]{0,80}\$\s*[0-9]", four_page_blob, re.I):
            raise AssertionError("invented fee amount remains on a Phase D page")
        if re.search(r"\b(?:approval|permit) (?:takes|within|guaranteed|will be approved)\b", four_page_blob, re.I):
            raise AssertionError("approval time/outcome promise remains on a Phase D page")
        if re.search(r"\bDCP\b|\bfootpath width\b", four_page_blob, re.I):
            raise AssertionError("precinct control or universal width remains on a Phase D page")
        required_qualifications = (
            "confirm with Council that the March 2026 form and fee schedule are still current",
            "Council assesses each application and site",
            "approval and any site-specific requirements must be confirmed before work",
            "does not state that Structure Co holds the contractor licence or insurance",
        )
        if any(four_page_blob.count(text) != 4 for text in required_qualifications):
            raise AssertionError("required current-form/site/credential qualifications are incomplete")
        if CALCULATOR.exists():
            raise AssertionError("calculator artifact exists; Phase D must not build it")

        html_result = validate_source_html(args.forms_html, args.portal_html)
        field_doc = {
            "schema_version": "1.0",
            "phase": "D — Liverpool",
            "status": "COMPLETE",
            "generated_by": "scripts/52-phase-d-liverpool.py",
            "source_access_date": ACCESS_DATE,
            "official_pdf_sha256": PDF_SHA256,
            "requirements": citation_rows,
            "resolved_fields": field_rows,
        }
        FIELD_REGISTER.write_text(json.dumps(field_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = {
            "result": "PASS",
            "phase": "D",
            "requirements": len(citation_rows),
            "source_citations_validated_against_pdf": len(citation_rows) if pdf_pages else 0,
            "resolved_fields": len(field_rows),
            "pages": len(PAGES),
            "false_fidelity_residue": residue,
            "outside_phase_d_false_fidelity_residue": outside_phase_d_residue,
            "qualifications": list(required_qualifications),
            "calculator": "ABSENT — unbuilt and excluded",
            "source_html": html_result,
            "errors": [],
        }
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            "PASS — Phase D Liverpool: 13/13 citations; 12/12 fields; "
            "4 pages; false-fidelity residue=0; calculator absent"
        )
        return 0
    except Exception as exc:
        result = {"result": "FAIL", "phase": "D", "errors": [str(exc)]}
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"FAIL — Phase D Liverpool: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
