from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class IdentityClaimsLiverpoolRegressionTest(unittest.TestCase):
    maxDiff = None

    def run_script(self, script: str, *args: str) -> str:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *args],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc.stdout

    def test_generated_derivatives_are_reproducible(self) -> None:
        output = self.run_script("46-architecture-import-gate.py", "--check")
        self.assertIn("PASS", output)

    def test_owner_attestation_is_exact_and_fail_closed(self) -> None:
        facts = yaml.safe_load((ROOT / "data" / "verified-facts.yml").read_text(encoding="utf-8"))
        self.assertEqual(facts["legal_entity"]["trading_name"]["value"], "Structure Co Concreters Camden")
        self.assertTrue(facts["legal_entity"]["trading_name"]["verified"])
        self.assertEqual(facts["contact"]["phone"]["value"], "(03) 4328 3392")
        self.assertEqual(facts["contact"]["phone"]["uri"], "tel:+61343283392")
        self.assertTrue(facts["contact"]["is_staffed"]["value"])
        self.assertFalse(facts["contact"]["open_to_visitors"]["value"])
        self.assertFalse(facts["contact"]["customer_facing_premises"]["value"])
        self.assertFalse(facts["legal_entity"]["abn"]["verified"])
        self.assertFalse(facts["legal_entity"]["legal_name"]["verified"])

    def test_claim_register_reconciles_and_current_claims_pass(self) -> None:
        self.run_script("46-claim-evidence-gate.py")
        disposition = json.loads((ROOT / "build" / "51-claim-disposition-register.json").read_text(encoding="utf-8"))
        self.assertEqual(disposition["totals"]["legacy_occurrences"], 232)
        self.assertEqual(disposition["totals"]["legacy_unsupported"], 228)
        self.assertEqual(disposition["totals"]["final_unsupported"], 0)
        self.assertEqual(len(disposition["legacy_occurrences"]), 232)
        self.assertTrue(all(row["final_disposition"] for row in disposition["legacy_occurrences"]))

    def test_schema_and_consolidated_evidence_gate(self) -> None:
        self.run_script("30-build-schema.py")
        output = self.run_script("51-evidence-validation.py")
        self.assertIn("Liverpool placements=12", output)
        result = json.loads((ROOT / "reports" / "51-evidence-validation.json").read_text(encoding="utf-8"))
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["sections"]["privacy_markers"]["blocking_count"], 5)
        self.assertEqual(result["sections"]["schema"]["localbusiness"], 0)


if __name__ == "__main__":
    unittest.main()
