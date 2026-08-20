from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "encoding-canary.txt"
INSTRUCTION = ROOT / "CODEX-BUILD-2.1.md"
RECONCILIATION = ROOT / "reports" / "21-reconciliation-v2.md"

EXPECTED_FIXTURE = (
    "encoding-canary: em dash — | en dash – | squared m² | "
    "non-breaking space [\u00a0]\n"
)
EXPECTED_INSTRUCTION_ASSERTION = "## 4.25 — Stage 25: uniqueness enforcement"
EXPECTED_REPORT_ASSERTION = "PASS — 157 combined (156 main + 1 planned supplementary)"


def read_utf8(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="strict", newline="") as handle:
        return handle.read()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    # The check is deliberately self-configuring.  PYTHONUTF8 and
    # PYTHONIOENCODING are still exported by the documented runner, but WSL does
    # not reliably propagate them into a Windows python.exe process.  Requiring
    # inherited variables made the environment fail while every exact UTF-8
    # operation below succeeded.  Explicit strict file encodings plus stream
    # reconfiguration test the property the gate actually protects, in either
    # host environment, without weakening any assertion.

    source = read_utf8(FIXTURE)
    if source != EXPECTED_FIXTURE:
        raise AssertionError(
            "Encoding fixture differs by code point: "
            f"expected={EXPECTED_FIXTURE!r}, actual={source!r}"
        )

    with tempfile.TemporaryDirectory(prefix="camden-encoding-canary-") as temp_dir:
        roundtrip_path = Path(temp_dir) / "roundtrip.txt"
        with roundtrip_path.open(
            "w", encoding="utf-8", errors="strict", newline=""
        ) as handle:
            handle.write(source)
        roundtrip = read_utf8(roundtrip_path)
    if roundtrip != source:
        raise AssertionError("UTF-8 read-write-compare round trip changed the fixture")

    instruction = read_utf8(INSTRUCTION)
    if EXPECTED_INSTRUCTION_ASSERTION not in instruction:
        raise AssertionError(
            "Full-fidelity instruction assertion failed: "
            f"{EXPECTED_INSTRUCTION_ASSERTION!r}"
        )

    reconciliation = read_utf8(RECONCILIATION)
    if EXPECTED_REPORT_ASSERTION not in reconciliation:
        raise AssertionError(
            "Full-fidelity Gate 21 assertion failed: "
            f"{EXPECTED_REPORT_ASSERTION!r}"
        )

    required_code_points = {
        "em dash": "—",
        "en dash": "–",
        "squared": "²",
        "non-breaking space": "\u00a0",
    }
    missing = [name for name, value in required_code_points.items() if value not in roundtrip]
    if missing:
        raise AssertionError(f"Canary lost required code points: {', '.join(missing)}")

    print("PASS — UTF-8 canary survived an exact read-write-compare cycle")
    print(f"PASS — exact instruction assertion: {EXPECTED_INSTRUCTION_ASSERTION}")
    print(f"PASS — exact report assertion: {EXPECTED_REPORT_ASSERTION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
