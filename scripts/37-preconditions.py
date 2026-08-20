#!/usr/bin/env python3
"""RUN-BLOCK-02 §1 — precondition gate.

Checks each phase's precondition against actual disk state and prints the table
RUN-BLOCK-02 requires before any phase starts. Re-runnable: this is the script
to run each time an owner input arrives, to see what has become unblocked.

Exits 0 if at least one phase is RUNNABLE, 1 if all are blocked.
Reports only. Runs no phase.
"""
from __future__ import annotations

import hashlib
import os
import json
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAUSE_BASELINE = {
    "camden-concreting-import.xml":
        "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884",
    "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml":
        "45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15",
    "build/stage9-page-manifest.json":
        "578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42",
    "build/stage8-image-map.json":
        "0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF",
    "reports/08-image-rename-map.csv":
        "43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8",
    "CODEX-BUILD-2.1.md":
        "BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C",
    "archive/governing/CODEX-BUILD-2.md":
        "E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5",
}


def strip_comments(t: str) -> str:
    """Drop comment lines.

    Without this, the instructional header in each data file - which explains
    'set verified: true' - is counted as an attested field. That would report a
    file as partly attested when nothing in it is, which is the wrong direction
    for a fail-closed gate to be wrong in.
    """
    return "\n".join(ln for ln in t.splitlines() if not ln.lstrip().startswith("#"))


def yaml_field_states(path: Path) -> tuple[int, int]:
    """Return (verified_true, verified_false) counts. Fail-closed: unreadable = 0 true."""
    if not path.exists():
        return 0, 0
    t = strip_comments(path.read_text(encoding="utf-8", errors="strict"))
    return (len(re.findall(r"verified:\s*true", t)),
            len(re.findall(r"verified:\s*false", t)))


def phase_a() -> tuple[str, str]:
    p = ROOT / "data" / "service-specs.yml"
    if not p.exists():
        return "BLOCKED", "data/service-specs.yml absent"
    t = strip_comments(p.read_text(encoding="utf-8", errors="strict"))
    ok, bad = yaml_field_states(p)
    populated = re.search(r"populated:\s*true", t) is not None
    if bad or not populated:
        return "BLOCKED", (f"{bad} fields still verified:false, {ok} true; "
                           f"populated flag {'true' if populated else 'false'}")
    return "RUNNABLE", f"{ok} fields verified:true, 0 false"


def phase_b() -> tuple[str, str]:
    media = ROOT / "source-inputs" / "media"
    retired = ROOT / "source-inputs" / "media-retired"
    held_dir = ROOT / "source-inputs" / "media-held-band-a"
    astra = ROOT / "source-inputs" / "astra"
    nm = len([p for p in media.iterdir()
              if p.is_file() and p.name.lower() not in ("readme.md", ".gitkeep")]) \
        if media.is_dir() else 0
    na = len([p for p in astra.iterdir()
              if p.is_file() and p.name.lower() not in ("readme.md", ".gitkeep")]) \
        if astra.is_dir() else 0
    remediation_path = ROOT / "build" / "47-media-remediation.csv"
    exclusions: list[str] = []
    holds: list[str] = []
    public_targets: list[str] = []
    if remediation_path.exists():
        with remediation_path.open("r", encoding="utf-8", errors="strict", newline="") as fh:
            remediation = list(csv.DictReader(fh))
        exclusions = [
            row["current_filename"] for row in remediation
            if row["payload_action"] == "EXCLUDE"
        ]
        holds = [
            row["current_filename"] for row in remediation
            if row["payload_action"] == "HOLD"
        ]
        public_targets = [
            row["target_filename"] if row["payload_action"] == "RENAME" else row["current_filename"]
            for row in remediation
            if row["payload_action"] in {"RENAME", "RETAIN"}
        ]
    retired_present = sum(
        (retired / filename).is_file() for filename in exclusions
    ) if retired.is_dir() else 0
    held_present = sum(
        (held_dir / filename).is_file() for filename in holds
    ) if held_dir.is_dir() else 0
    expected_active = len(public_targets)
    driver = ROOT / "scripts" / "22-reencode-images.sh"
    # The re-encode driver and the D25.2 EXIF assertion run in WSL, not on the
    # Windows host. Probing Windows bash reported NOT INSTALLED permanently and
    # would have kept reporting it after the real dependency was satisfied.
    # Probe the host that actually runs the driver; fall back to the local shell
    # so this stays correct on a non-Windows machine.
    def _probe(cmd: list[str]) -> bool:
        try:
            return subprocess.run(cmd, capture_output=True, timeout=60).returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False

    magick_host = None
    if _probe(["wsl", "-e", "bash", "-lc", "command -v magick"]):
        magick_host = "WSL"
    elif _probe(["bash", "-lc", "command -v magick"]):
        magick_host = "local shell"
    has_magick = magick_host is not None
    parts = [f"public media {nm}/{expected_active}",
             f"immutable source 83; excluded {retired_present}/{len(exclusions)} quarantined",
             f"Band A held {held_present}/{len(holds)}; owner verdicts missing {len(holds)}",
             f"astra {na} file(s)",
             f"driver {'present' if driver.exists() else 'ABSENT'}",
             f"ImageMagick {'installed in ' + magick_host if has_magick else 'NOT INSTALLED'}"]
    technical_ready = (
            len(exclusions) + len(holds) + len(public_targets) == 83
            and nm == expected_active
            and retired_present == len(exclusions)
            and held_present == len(holds) and na >= 1
            and driver.exists() and has_magick)
    if technical_ready and not holds:
        return "RUNNABLE", "; ".join(parts)
    return "BLOCKED", "; ".join(parts)


def phase_c() -> tuple[str, str]:
    p = ROOT / "data" / "verified-facts.yml"
    ok, bad = yaml_field_states(p)
    REQ = ["legal_name", "abn", "nsw_fair_trading_licence", "insurance_public_liability",
           "street_address", "is_staffed", "phone"]
    if not p.exists():
        return "BLOCKED", "data/verified-facts.yml absent"
    t = strip_comments(p.read_text(encoding="utf-8", errors="strict"))
    missing = []
    for f in REQ:
        m = re.search(rf"{f}:\s*\n(?:.*\n)*?\s*verified:\s*(true|false)", t)
        if not m or m.group(1) != "true":
            missing.append(f)
    if missing:
        return "BLOCKED", f"{ok} verified:true / {bad} false; unverified required: {', '.join(missing)}"
    return "RUNNABLE", f"{ok} fields verified:true"


def phase_d() -> tuple[str, str]:
    p = ROOT / "data" / "council-specs.yml"
    if not p.exists():
        return "BLOCKED", "data/council-specs.yml absent (Stage 31 artifact, not yet created)"
    t = strip_comments(p.read_text(encoding="utf-8", errors="strict"))
    liv = re.search(r"liverpool", t, re.I)
    ver = len(re.findall(r"verified:\s*true", t))
    src = len(re.findall(r"source_url:\s*\S+", t))
    sight = len(re.findall(r"sighted_date:\s*\S+", t))
    if liv and ver and src and sight:
        return "RUNNABLE", f"{ver} verified, {src} source_url, {sight} sighted_date"
    return "BLOCKED", (f"liverpool section {'present' if liv else 'absent'}; "
                       f"verified:true {ver}; source_url {src}; sighted_date {sight}")


def phase_e(a_status: str) -> tuple[str, str]:
    if a_status != "RUNNABLE":
        return "BLOCKED", "requires Phase A; the attested matrix does not exist"
    supplied = ROOT / "source-inputs" / "service-copy"
    n = len(list(supplied.glob("*"))) if supplied.is_dir() else 0
    if n:
        return "RUNNABLE", f"{n} supplied copy file(s)"
    return "BLOCKED", "no supplied copy and no recorded authorship authorisation"


def phase_f(prior: list[tuple[str, str]]) -> tuple[str, str]:
    """Phase F carries its own sub-preconditions from DECISION-07 D33/D34.

    Phase F spends money. Every condition below must hold before a single SerpApi
    credit is used, and the licence rule in D33.2 - verify on the hosting page,
    before download, no batch approval - is not automatable and is not checked here.
    """
    if any(st != "RUNNABLE" for st, _ in prior):
        return "BLOCKED", "explicitly last; requires A-E"
    unmet = []
    if not (ROOT / "scripts" / "find_images.py").exists():
        unmet.append("find_images.py not copied into scripts/ (D34.1)")
    spec = ROOT / "reports" / "33-image-replacement-spec.csv"
    regen = ROOT / "reports" / "37-image-replacement-spec.csv"
    if not regen.exists():
        unmet.append("spec not regenerated against the 77-page architecture (D34.2)")
    if not os.environ.get("SERPAPI_KEY"):
        unmet.append("SERPAPI_KEY not set")
    if not (ROOT / "reports" / "33-licence-register.csv").exists():
        unmet.append("licence register not initialised (D33.5)")
    if unmet:
        return "BLOCKED", "; ".join(unmet)
    return "RUNNABLE", "A-E complete and D33/D34 sub-preconditions met"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 78)
    print("RUN BLOCK 02 §1 — PRECONDITION TABLE")
    print("=" * 78)
    print()

    print("IMMUTABLE HASHES vs the pause baseline")
    print()
    bad = 0
    for i, (rel, exp) in enumerate(PAUSE_BASELINE.items(), 1):
        live = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest().upper()
        ok = live == exp
        bad += 0 if ok else 1
        print(f"FILE {i} of 7")
        print(f"  path      {rel}")
        print(f"  baseline  {exp}")
        print(f"  computed  {live}")
        print(f"  result    {'MATCH' if ok else 'MISMATCH — HARD STOP'}")
        print()
    print(f"  VERDICT   {len(PAUSE_BASELINE)-bad} of {len(PAUSE_BASELINE)} MATCH, "
          f"{bad} mismatches")
    print()

    a = phase_a()
    b = phase_b()
    c = phase_c()
    d = phase_d()
    e = phase_e(a[0])
    f = phase_f([a, b, c, d, e])
    g = ("BLOCKED", "requires the preceding phases and a GO from preflight") if any(
        x[0] != "RUNNABLE" for x in (a, b, c, d, e, f)) else ("RUNNABLE", "all phases complete")

    rows = [("A", "attest the figures", a), ("B", "media and staging", b),
            ("C", "identity and schema", c), ("D", "Liverpool", d),
            ("E", "service page rebuild", e), ("F", "images", f), ("G", "release", g)]

    print("PHASE PRECONDITIONS")
    print()
    print(f"  {'PHASE':<7}{'NAME':<24}{'STATUS':<10}EVIDENCE")
    for k, name, (st, ev) in rows:
        print(f"  {k:<7}{name:<24}{st:<10}{ev}")
    print()
    runnable = [k for k, _, (st, _) in rows if st == "RUNNABLE"]
    print(f"  RUNNABLE PHASES: {', '.join(runnable) if runnable else 'NONE'}")
    print()
    print("=" * 78)
    if bad:
        print("RESULT: HARD STOP — immutable hash mismatch. Run nothing.")
        return 1
    if not runnable:
        print("RESULT: ALL PHASES BLOCKED. Nothing is run. Build remains paused.")
        return 1
    print(f"RESULT: {len(runnable)} phase(s) runnable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
