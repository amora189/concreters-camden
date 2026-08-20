from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANARY = ROOT / "scripts" / "21-encoding-canary.py"
EXPECTED = [
    "PASS — UTF-8 canary survived an exact read-write-compare cycle",
    "PASS — exact instruction assertion: ## 4.25 — Stage 25: uniqueness enforcement",
    "PASS — exact report assertion: PASS — 157 combined (156 main + 1 planned supplementary)",
]


def run_canary(env: dict[str, str]) -> list[str]:
    result = subprocess.run(
        [sys.executable, str(CANARY)],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip().splitlines()


def test_canary_is_independent_of_inherited_utf8_variables() -> None:
    clean = os.environ.copy()
    clean.pop("PYTHONUTF8", None)
    clean.pop("PYTHONIOENCODING", None)
    assert run_canary(clean) == EXPECTED


def test_canary_repairs_an_ascii_console_contract() -> None:
    hostile = os.environ.copy()
    hostile["PYTHONUTF8"] = "0"
    hostile["PYTHONIOENCODING"] = "ascii"
    assert run_canary(hostile) == EXPECTED

