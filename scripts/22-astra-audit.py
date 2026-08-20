#!/usr/bin/env python3
"""Stage 22 — Astra Customizer / theme-mods intake audit. Fail-closed.

Per CODEX-BUILD-2.1.md §4.22.3: validate that the supplied file is a genuine
Astra theme-mods / Customizer export and report which mods it contains, so a
PARTIAL export is caught before import rather than after.

Accepts the three shapes a real Astra export takes:
  1. WordPress Customizer export plugin  .dat  (PHP-serialised, with 'mods' key)
  2. JSON theme-mods dump                .json (astra-settings / theme_mods_astra)
  3. Astra "Import/Export Settings"      .json (the astra-settings blob alone)

Exits non-zero if the directory is empty, if no candidate parses as one of
those, or if a parsed export is missing any REQUIRED mod group.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASTRA = ROOT / "source-inputs" / "astra"
REPORT_OUT = ROOT / "reports" / "22-astra-audit-result.md"

# --------------------------------------------------------------------------
# REVISED 19 August 2026 per reports/42-astra-vs-elementor-design-carriage.md §4.
#
# The previous list made all seven groups REQUIRED, on the assumption that Astra
# carries the design. On this site it does not, and never did: Astra is
# near-stock and the Elementor kit holds factory defaults that nothing uses. A
# Customizer export stores only what was explicitly set, so an untouched setting
# has no key at all -- meaning "absent from the export" and "never customised"
# produce an identical file. The old list therefore FAILED a correct export.
#
# Deleting the groups outright would replace a wrong check with no check, so the
# six are downgraded to REPORTED, and two genuinely load-bearing checks are added
# in their place.
# --------------------------------------------------------------------------

# Required: the export must actually identify the site's mark.
REQUIRED_GROUPS = {
    "site-identity": ["custom_logo", "site_icon", "display-site-title", "display-site-tagline"],
}

# Reported, never required. UNSET is a valid stock configuration, not a failure.
REPORTED_GROUPS = {
    "colours": ["theme-color", "link-color", "text-color", "heading-base-color",
                "astra-settings[theme-color]", "astra-settings[link-color]"],
    "typography": ["body-font-family", "body-font-size", "font-family-h1", "font-size-h1",
                   "astra-settings[body-font-family]", "astra-settings[font-family-h1]"],
    "layout": ["site-content-width", "site-layout", "header-layouts", "site-sidebar-layout",
               "astra-settings[site-content-width]", "astra-settings[site-layout]"],
    "header": ["header-main-rt-section", "header-main-layout-width", "transparent-header-enable",
               "astra-settings[header-main-layout-width]"],
    "footer": ["footer-layout", "footer-sml-layout", "footer-adv",
               "astra-settings[footer-sml-layout]"],
    "buttons": ["button-color", "button-bg-color", "button-radius", "theme-button-padding",
                "astra-settings[button-bg-color]"],
}

MAIN_WXR = ROOT / "camden-concreting-import.xml"

SERIALISED_KEY = re.compile(rb's:\d+:"([^"]+)"')


def parse_candidate(path: Path) -> tuple[str, set[str]] | None:
    """Return (format_label, set_of_mod_keys) or None if unrecognised."""
    raw = path.read_bytes()

    if raw.lstrip()[:1] in (b"{", b"["):
        try:
            data = json.loads(raw.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        keys: set[str] = set()

        def collect(node, prefix=""):
            if isinstance(node, dict):
                for k, v in node.items():
                    keys.add(str(k))
                    collect(v, k)
            elif isinstance(node, list):
                for v in node:
                    collect(v, prefix)

        collect(data)
        label = "JSON theme-mods / astra-settings export"
        if isinstance(data, dict) and "mods" in data:
            label = "JSON Customizer export (mods wrapper)"
        return label, keys

    if b"a:" in raw[:64] or b"O:" in raw[:64] or raw[:4] == b'\x00\x00\x00\x00':
        keys = {m.group(1).decode("utf-8", errors="strict")
                for m in SERIALISED_KEY.finditer(raw)}
        if keys:
            return "PHP-serialised Customizer export (.dat)", keys
    return None


def design_carriage(all_keys: set[str]) -> tuple[bool, str]:
    """REQUIRED. The design must be locatable, and the report must say WHERE.

    Fails only if colours and typography resolve from NOWHERE -- not Astra, not
    the Elementor kit, not page data. A site whose design lives in page data
    passes, and is told so, because that is a real and reportable state rather
    than a broken export.
    """
    astra_colour = any(k for k in all_keys if "color" in k.lower())
    astra_type = any(k for k in all_keys if "font" in k.lower())
    kit_colour = kit_type = page_colour = page_type = 0
    if MAIN_WXR.exists():
        raw = MAIN_WXR.read_text(encoding="utf-8", errors="strict")
        for m in re.finditer(r"<wp:post_type>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</wp:post_type>", raw):
            pass
        kit = re.search(r'"system_colors";a:\d+:\{(.*?)\}\}s:', raw, re.S)
        kit_colour = len(re.findall(r's:5:"color";s:7:"(#[0-9A-Fa-f]{6})"', raw))
        kit_type = len(re.findall(r's:22:"typography_font_family"', raw))
        page_colour = len(re.findall(r'"#[0-9A-Fa-f]{6}"', raw))
        page_type = len(re.findall(r'"typography_font_family":"', raw))
    where = []
    if astra_colour or astra_type:
        where.append("Astra mods")
    if kit_colour or kit_type:
        where.append(f"Elementor kit ({kit_colour} colours, {kit_type} type entries)")
    if page_colour or page_type:
        where.append(f"page _elementor_data ({page_colour} colour literals, "
                     f"{page_type} type entries)")
    if not where:
        return False, "design resolves from NOWHERE: not Astra, not the kit, not page data"
    note = ""
    if where and "Astra mods" not in where and page_type and page_type > kit_type * 10:
        note = ("  [!] the design is carried in PAGE DATA, not in a governing layer — "
                "the site cannot be restyled centrally")
    return True, "resolves from: " + "; ".join(where) + note


def internal_consistency(data_keys: set[str], raw_texts: list[str]) -> tuple[bool, list[str]]:
    """REQUIRED. Everything the export references must exist in the WXR."""
    problems: list[str] = []
    if not MAIN_WXR.exists():
        return False, ["main WXR absent; the export cannot be reconciled against anything"]
    wxr = MAIN_WXR.read_text(encoding="utf-8", errors="strict")
    blob = "\n".join(raw_texts)

    att_ids = set()
    for key in ("custom_logo", "site_icon"):
        for m in re.finditer(r's:%d:"%s";(?:i:(\d+)|s:\d+:"(\d+)")' % (len(key), key), blob):
            att_ids.add(m.group(1) or m.group(2))
    for aid in sorted(att_ids):
        if not re.search(r"<wp:post_id>%s</wp:post_id>" % aid, wxr):
            problems.append(f"attachment {aid} referenced by the export is not in the WXR")

    for m in re.finditer(r's:\d+:"(primary|mobile_menu|footer_menu)";i:(\d+);', blob):
        tid = m.group(2)
        if not re.search(r"<wp:term_id>(?:<!\[CDATA\[)?%s(?:\]\]>)?</wp:term_id>" % tid, wxr):
            problems.append(f"menu term {tid} ({m.group(1)}) is not a wp:term in the WXR")

    for m in re.finditer(r's:18:"custom_css_post_id";i:(\d+);', blob):
        pid = m.group(1)
        if not re.search(r"<wp:post_id>%s</wp:post_id>" % pid, wxr):
            problems.append(f"custom_css_post_id {pid} has no matching post in the WXR")
    return not problems, problems


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    failures: list[str] = []
    findings: list[str] = []

    if not ASTRA.is_dir():
        failures.append(f"astra directory absent: {ASTRA.relative_to(ROOT)}")
        candidates: list[Path] = []
    else:
        candidates = [p for p in ASTRA.iterdir() if p.is_file()
                      and p.name.lower() not in ("readme.md", ".gitkeep")]

    if not candidates:
        failures.append("no Astra export file supplied")

    parsed: list[tuple[Path, str, set[str]]] = []
    for p in candidates:
        result = parse_candidate(p)
        if result is None:
            failures.append(f"{p.name}: not a recognised Astra Customizer or theme-mods export")
            continue
        label, keys = result
        parsed.append((p, label, keys))
        findings.append(f"{p.name}: parsed as {label}, {len(keys)} keys")

    group_status: dict[str, tuple[bool, list[str]]] = {}
    reported_status: dict[str, tuple[bool, list[str]]] = {}
    carriage = (False, "not evaluated")
    consistency: tuple[bool, list[str]] = (False, ["not evaluated"])
    if parsed:
        all_keys: set[str] = set()
        for _, _, keys in parsed:
            all_keys |= keys
        for group, probes in REQUIRED_GROUPS.items():
            found = [k for k in probes if k in all_keys]
            group_status[group] = (bool(found), found)
            if not found:
                failures.append(f"required mod group absent from export: {group}")
        for group, probes in REPORTED_GROUPS.items():
            found = [k for k in probes if k in all_keys]
            reported_status[group] = (bool(found), found)

        raw_texts = [p.read_text(encoding="utf-8", errors="replace") for p, _, _ in parsed]
        carriage = design_carriage(all_keys)
        if not carriage[0]:
            failures.append(f"design-carriage: {carriage[1]}")
        consistency = internal_consistency(all_keys, raw_texts)
        for prob in consistency[1]:
            failures.append(f"internal-consistency: {prob}")
    else:
        for group in REQUIRED_GROUPS:
            group_status[group] = (False, [])
            failures.append(f"required mod group unverifiable, no export parsed: {group}")
        for group in REPORTED_GROUPS:
            reported_status[group] = (False, [])
        failures.append("design-carriage unverifiable, no export parsed")
        failures.append("internal-consistency unverifiable, no export parsed")

    lines = [
        "# Stage 22 Astra audit result",
        "",
        "Generated by `scripts/22-astra-audit.py`. Fail-closed: a partial export fails here,",
        "not after import.",
        "",
        "```text",
        f"  candidate files           {len(candidates)}",
        f"  parsed as Astra exports   {len(parsed)}",
        f"  required mod groups       {len(REQUIRED_GROUPS)}",
        f"  groups present            {sum(1 for ok, _ in group_status.values() if ok)}",
        f"  design-carriage           {'PASS' if carriage[0] else 'FAIL'}",
        f"  internal-consistency      {'PASS' if consistency[0] else 'FAIL'}",
        f"  total failures            {len(failures)}",
        f"  verdict                   {'PASS' if not failures else 'FAIL'}",
        "```",
        "",
        "Revised 19 August 2026 per `reports/42-astra-vs-elementor-design-carriage.md` §4. The six",
        "design groups are REPORTED, not required: a Customizer export stores only what was",
        "explicitly set, so UNSET is a valid stock configuration rather than a partial export.",
        "",
        "## Required mod groups",
        "",
        "```text",
    ]
    for group, (ok, found) in group_status.items():
        lines.append(f"  {group:<16} {'PRESENT' if ok else 'ABSENT '}  "
                     f"{', '.join(found) if found else 'no probe key matched'}")
    lines += ["```", "", "## Required — design carriage", "", "```text",
              f"  {'PASS' if carriage[0] else 'FAIL'}  {carriage[1]}", "```", "",
              "## Required — internal consistency", "", "```text"]
    if consistency[1]:
        lines += [f"  FAIL  {p}" for p in consistency[1]]
    else:
        lines += ["  PASS  every attachment ID, menu term and custom_css_post_id the export "
                  "references exists in the WXR"]
    lines += ["```", "", "## Reported mod groups (not required)", "", "```text"]
    for group, (ok, found) in reported_status.items():
        lines.append(f"  {group:<16} {'SET    ' if ok else 'UNSET  '}  "
                     f"{', '.join(found) if found else 'never customised — valid stock configuration'}")
    lines += ["```", ""]
    if findings:
        lines += ["## Parse findings", "", "```text"]
        lines += [f"  {f}" for f in findings]
        lines += ["```", ""]
    if failures:
        lines += ["## Failures", "", "```text"]
        lines += [f"  {i:>3}. {f}" for i, f in enumerate(failures, 1)]
        lines += ["```", ""]
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"candidates={len(candidates)} parsed={len(parsed)} "
          f"required_groups={sum(1 for ok, _ in group_status.values() if ok)}/{len(REQUIRED_GROUPS)} "
          f"reported_set={sum(1 for ok, _ in reported_status.values() if ok)}/{len(REPORTED_GROUPS)} "
          f"carriage={'PASS' if carriage[0] else 'FAIL'} "
          f"consistency={'PASS' if consistency[0] else 'FAIL'} "
          f"failures={len(failures)}")
    print(f"design carriage: {carriage[1]}")
    print(f"report -> {REPORT_OUT.relative_to(ROOT).as_posix()}")
    if failures:
        print("VERDICT: FAIL — Astra intake incomplete")
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
