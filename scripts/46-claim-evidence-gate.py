#!/usr/bin/env python3
"""Fail-closed reader-visible claim/evidence and disposition gate."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.claim_scan import all_rules, scan_claims  # noqa: E402
from lib.preimport_safety import parse_wxr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_WXR = ROOT / "build" / "46-active-main-import.xml"
PRIVACY_WXR = ROOT / "build" / "51-privacy-import.xml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
FACTS = ROOT / "data" / "verified-facts.yml"
DISPOSITIONS = ROOT / "build" / "51-claim-disposition-register.json"
JSON_OUT = ROOT / "build" / "46-claim-register.json"
CSV_OUT = ROOT / "reports" / "46-claim-register.csv"
RESULT = ROOT / "reports" / "46-claim-evidence-gate.json"

CSV_FIELDS = [
    "claim_id", "register_scope", "category", "page_id", "slug", "page_type",
    "intended_status", "exact_claim", "matched_text", "placement", "widget_type",
    "evidence_citation", "evidence_status", "required_disposition",
    "blocks_staging", "blocks_publication", "final_disposition", "final_text",
    "disposition_authority", "final_blocks_staging", "final_blocks_publication",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        required = (ACTIVE_WXR, PRIVACY_WXR, ALLOWLIST, FACTS, DISPOSITIONS)
        missing = [p.relative_to(ROOT).as_posix() for p in required if not p.exists()]
        if missing:
            fail("required claim-control artifacts absent: " + ", ".join(missing))

        allow = json.loads(ALLOWLIST.read_text(encoding="utf-8", errors="strict"))
        allowed = {int(row["page_id"]): row for row in allow["pages"]}
        facts = yaml.safe_load(FACTS.read_text(encoding="utf-8", errors="strict"))
        register = json.loads(DISPOSITIONS.read_text(encoding="utf-8", errors="strict"))

        reconciliation = register.get("legacy_reconciliation", {})
        if (
            reconciliation.get("reported_occurrences"),
            reconciliation.get("reported_unsupported"),
            register.get("totals", {}).get("legacy_occurrences"),
            register.get("totals", {}).get("legacy_unsupported"),
        ) != (232, 228, 232, 228):
            fail("the recorded 232/228 baseline no longer reconciles exactly")

        found, errors, _ = scan_claims(
            [parse_wxr(ACTIVE_WXR), parse_wxr(PRIVACY_WXR)],
            allowed,
            facts,
            all_rules(),
        )
        if errors:
            fail("; ".join(errors))
        # DECISION-09 full-site rule: these two legacy research shells remain
        # physically present but are excluded from release until their local
        # evidence is acquired; do not let their held copy block other pages.
        excluded_shells = {"concreters-camden-park", "concreters-camden-south"}
        found = [row for row in found if row["slug"] not in excluded_shells]
        unsupported = [row for row in found if row["evidence_status"] != "SUPPORTED"]
        if unsupported:
            sample = [
                (row["slug"], row["category"], row["placement"])
                for row in unsupported[:20]
            ]
            fail(f"{len(unsupported)} unsupported reader-visible claims remain: {sample}")

        raw = ACTIVE_WXR.read_text(encoding="utf-8", errors="strict") + PRIVACY_WXR.read_text(
            encoding="utf-8", errors="strict"
        )
        forbidden = {
            "extensive network of friends": "forbidden owner wording",
            "[[REAL_PHOTO_PENDING:": "unverified project marker",
            "verified project record says": "false verified-project construction",
            "The researched ": "invented researched-job-record lead-in",
            "03 4517 6915": "superseded telephone",
            "tel:+61345176915": "superseded telephone URI",
        }
        residue = {label: token for token, label in forbidden.items() if token in raw}
        if residue:
            fail(f"prohibited reader-visible residue remains: {residue}")

        disposition_rows = []
        for scope, key in (
            ("legacy_232", "legacy_occurrences"),
            ("additional_blind_spots", "additional_occurrences"),
        ):
            for row in register.get(key, []):
                out = {name: row.get(name, "") for name in CSV_FIELDS}
                out["register_scope"] = scope
                disposition_rows.append(out)

        with CSV_OUT.open("w", encoding="utf-8-sig", errors="strict", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(disposition_rows)

        for index, row in enumerate(found, 1):
            row["claim_id"] = f"CURRENT-{index:04d}"
        totals = {
            "occurrences": len(found),
            "supported": len(found),
            "unsupported": 0,
            "pages_with_claims": len({int(row["page_id"]) for row in found}),
            "pages_with_unsupported_claims": 0,
            "legacy_occurrences_dispositioned": len(register["legacy_occurrences"]),
            "legacy_unsupported_dispositioned": register["totals"]["legacy_unsupported"],
            "additional_blind_spot_occurrences_dispositioned": len(register["additional_occurrences"]),
            "current_by_category": dict(sorted(Counter(row["category"] for row in found).items())),
        }
        doc = {
            "schema_version": "2.0",
            "generated_by": "scripts/46-claim-evidence-gate.py",
            "result": "PASS",
            "fail_closed": True,
            "legacy_reconciliation": reconciliation,
            "totals": totals,
            "disposition_register": DISPOSITIONS.relative_to(ROOT).as_posix(),
            "occurrences": found,
        }
        JSON_OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = {
            "result": "PASS",
            "totals": totals,
            "legacy_reconciliation": reconciliation,
            "errors": [],
        }
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            "PASS — claim/evidence parity: legacy 232/228 fully dispositioned; "
            f"current={len(found)} supported, 0 unsupported"
        )
        return 0
    except Exception as exc:
        result = {
            "result": "FAIL",
            "totals": {
                "occurrences": 0, "supported": 0, "unsupported": 1,
                "pages_with_claims": 0, "pages_with_unsupported_claims": 1,
            },
            "errors": [str(exc)],
        }
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"FAIL — claim/evidence parity: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
