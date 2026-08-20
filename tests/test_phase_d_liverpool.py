from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PhaseDLiverpoolRegressionTest(unittest.TestCase):
    def test_generated_phase_d_payload_passes_without_network(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "52-phase-d-liverpool.py")],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        result = json.loads(
            (ROOT / "reports" / "52-liverpool-validation.json").read_text(encoding="utf-8")
        )
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["requirements"], 13)
        self.assertEqual(result["resolved_fields"], 12)
        self.assertEqual(result["false_fidelity_residue"], {
            "reproduced without alteration": 0,
            "Liverpool REQUIRED-RESEARCH": 0,
            "verified project record": 0,
            "researched job record": 0,
        })
        self.assertEqual(result["calculator"], "ABSENT — unbuilt and excluded")


if __name__ == "__main__":
    unittest.main()
