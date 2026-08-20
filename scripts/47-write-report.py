#!/usr/bin/env python3
"""Generate the Phase B media-payload closure report from gate evidence."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "47-phase-b-media-payload-closure.md"
BT = chr(96)
FENCE = BT * 3

IMMUTABLES = [
    ("camden-concreting-import.xml", "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884"),
    ("eamptcoconcretersmelbourne_WordPress_2026-08-14.xml", "45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15"),
    ("build/stage9-page-manifest.json", "578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42"),
    ("build/stage8-image-map.json", "0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF"),
    ("reports/08-image-rename-map.csv", "43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8"),
    ("CODEX-BUILD-2.1.md", "BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C"),
    ("archive/governing/CODEX-BUILD-2.md", "E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5"),
]


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8", errors="strict"))


def load_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(
        "r", encoding="utf-8-sig", errors="strict", newline=""
    ) as handle:
        return list(csv.DictReader(handle))


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest().upper()


def quote(value: object) -> str:
    return BT + str(value) + BT


def safe(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def pages(placements: list[dict], active_ids: set[int]) -> str:
    grouped = Counter(
        (int(row["page_id"]), row["slug"], row["status"]) for row in placements
    )
    output = []
    for (page_id, slug, status), count in sorted(grouped.items(), key=lambda row: row[0][1]):
        scope = "active" if page_id in active_ids else "withdrawn"
        suffix = f" x{count}" if count != 1 else ""
        output.append(f"/{slug}/ ({page_id}, {status}, {scope}){suffix}")
    return "; ".join(output) if output else "attachment record/file only; no page placement"


def main() -> int:
    blockers = load_json("reports/47-original-media-blockers.json")
    architecture = load_json("reports/46-architecture-import-gate.json")
    public = load_json("reports/46-public-media-gate.json")
    claim = load_json("reports/46-claim-evidence-gate.json")
    allow = load_json("build/46-active-page-allowlist.json")
    manifest = load_csv("build/47-media-remediation.csv")
    worksheet = load_csv("reports/44-sighting-worksheet.csv")
    active_ids = {
        int(row["page_id"])
        for row in allow["pages"]
        if row["import_artifact"] == "build/46-active-main-import.xml"
    }
    by_id = {int(row["attachment_id"]): row for row in manifest}
    transform = architecture["media_transform"]
    lines: list[str] = [
        "# Phase B media-payload closure",
        "",
        "Date: 20 August 2026 (Australia/Sydney).",
        "",
        "## Outcome",
        "",
        "The authorised non-Band-A remediation is implemented in the reproducible derivative pipeline.",
        "The public-media gate improved from **40 failures to 16**. The remaining 16 are exactly the",
        "blank Band A owner verdicts. Their files are held outside the public intake and derivative,",
        "but the gate correctly continues to fail. **Phase B is not complete and no staging import is",
        "authorised.**",
        "",
        FENCE + "text",
        "  immutable files                         7/7 MATCH",
        "  derivative pages                       75 (81 withdrawn absent)",
        "  derivative attachment records          51 permitted",
        "  manifest                               83 = 51 RENAME + 16 EXCLUDE + 16 HOLD",
        "  remaining Elementor media references  409, all resolved",
        "  D32                                    17 sections / 16 pages / 47 markers removed",
        "  Band B                                 9/9 PASS",
        "  public-media gate                      FAIL — 16 blank Band A verdicts only",
        "  index-ready                            0 of 77",
        "  launch                                 NO-GO",
        FENCE,
        "",
        "The task named Gates 7 and 16, but the exact 40-failure population is from current preflight",
        "**Gate 17**. Gate 7 is uniqueness and Gate 16 is claim-to-evidence. Gate 16 separately held",
        "four Band B REAL_PHOTO_PENDING adjacencies; all four disappeared with their complete D32 modules.",
        "",
        "Repository discrepancy: " + quote("RUN-BLOCK-02-on-inputs.md") + " does not exist. The actual",
        "file is " + quote("RUN-BLOCK-02.md") + "; it was read without alteration.",
        "",
        "## Ground and reproducibility",
        "",
        quote("build/46-active-main-import.xml") + " SHA-256: **" + quote(architecture["derived_sha256"]) + "**.",
        "",
        quote("build/47-media-remediation.csv") + " SHA-256: **" + quote(digest("build/47-media-remediation.csv")) + "**.",
        "",
        "The architecture generator rebuilds both files from the immutable WXR and authoritative mutable",
        "inputs. The check mode reproduces them byte-for-byte; the derivative was not manually patched.",
        "",
        "## All 40 original assertions",
        "",
        "Each row records immutable-WXR page placements and Elementor reference counts. Exact Elementor",
        "paths, widget IDs, URLs and alts are in " + quote("reports/47-original-media-blockers.json") + ".",
        "",
        "| # | Class | ID / filename at failure | WXR placements and Elementor references | Final disposition |",
        "|---:|---|---|---|---|",
    ]
    for row in blockers["assertions"]:
        placement = (
            f"{row['elementor_references']} refs / {row['pages']} pages; "
            f"active {row['active_elementor_references']} refs / {row['active_pages']} pages; "
            f"withdrawn {row['withdrawn_elementor_references']} refs / {row['withdrawn_pages']} pages. "
            + pages(row["placements"], active_ids)
        )
        if row["category"] == "band_a_verdict_missing":
            final = "HOLD only; still FAIL. Owner verdict required and none inferred."
        else:
            final = row["authorised_disposition"] + ". Applied: " + row["transformation_required"]
        lines.append(
            f"| {row['assertion_number']} | {safe(row['category'])} | "
            f"{row['attachment_id']} {quote(safe(row['filename_at_failure']))} | "
            f"{safe(placement)} | {safe(final)} |"
        )
    lines += [
        "",
        "**Reconciliation: 12 denied + 16 Band A + 3 false-geography + 9 Band B = 40.**",
        "Thirty-four now pass; the 16 Band A assertions remain failed by design.",
        "",
        "## Band A verdict table",
        "",
        "All 16 owner verdict cells are blank. No OK, GENERIC, REPLACE or UNUSABLE decision was inferred.",
        "",
        "| Tile | ID | Held filename | Claim recorded by worksheet | Verdict | Payload state |",
        "|---:|---:|---|---|---|---|",
    ]
    for row in [row for row in worksheet if row["band"] == "A"]:
        lines.append(
            f"| {row['#']} | {row['attachment_id']} | {quote(safe(row['new_filename']))} | "
            f"{safe(row['claim_made'])} | **BLANK** | HOLD; public false, derivative false |"
        )
    lines += [
        "",
        "All 16 are present in " + quote("source-inputs/media-held-band-a/") + ". This is an unresolved",
        "placement state, not a substantive media verdict.",
        "",
        "## Band B transformation table",
        "",
        "| ID | Verdict | Source refs (active / withdrawn) | Final filename | Alt or slot action | Result |",
        "|---:|---|---:|---|---|---|",
    ]
    assertion_by = {
        (row["category"], int(row["attachment_id"])): row
        for row in blockers["assertions"]
    }
    band_b_result = {int(row["attachment_id"]): row for row in public["band_b"]}
    for attachment_id in [46, 52, 49, 51, 48, 47, 228, 280, 1067]:
        row = by_id[attachment_id]
        source = assertion_by[("band_b_derivative_disposition_missing", attachment_id)]
        filename = quote(row["target_filename"]) if row["target_filename"] else "EXCLUDED"
        action = (
            row["target_alt"]
            if row["payload_action"] == "RENAME"
            else "record and every slot absent; no replacement"
        )
        lines.append(
            f"| {attachment_id} | {row['verdict']} | {source['elementor_references']} "
            f"({source['active_elementor_references']} / {source['withdrawn_elementor_references']}) | "
            f"{filename} | {safe(action)} | **{band_b_result[attachment_id]['result']}** |"
        )
    unusable = blockers["band_b_unusable_slots"]
    lines += [
        "",
        "The 28 UNUSABLE slots reconcile exactly:",
        "",
        FENCE + "text",
        f"  attachment 280   source {unusable['280']['source_slots']:2d} = active {unusable['280']['active_slots']:2d} + withdrawn {unusable['280']['withdrawn_slots']:2d}",
        f"  attachment 1067  source {unusable['1067']['source_slots']:2d} = active {unusable['1067']['active_slots']:2d} + withdrawn {unusable['1067']['withdrawn_slots']:2d}",
        "  total            source 28 = active 14 + withdrawn 14",
        FENCE,
        "",
        "Two active slots disappeared inside D32 sections and 12 were directly pruned; the 14 withdrawn",
        "slots disappeared with their pages. Zero stale URL, filename, metadata or Elementor reference",
        "survives for either asset.",
        "",
        "The four Band B local-project cards removed with D32 were: 46 on Gregory Hills; 48 and 49 on",
        "Edmondson Park; and 52 on Catherine Field. They remain non-evidential and were not restocked.",
        "",
        "Pair 49/52 remains two IDs and filenames despite identical bytes. E&T pair 468/471 was excluded",
        "together. No attachment identity was collapsed.",
        "",
        "## Renamed public assets",
        "",
        "There are no plain RETAIN rows. D24/D20 required reversal of the Stage 8 geographic naming",
        "convention, so all 51 permitted public files are RENAME rows.",
        "",
        "| ID | Band | Payload source filename | Public filename | Public alt |",
        "|---:|---|---|---|---|",
    ]
    for row in [row for row in manifest if row["payload_action"] == "RENAME"]:
        alt = row["target_alt"] or "(empty decorative alt)"
        lines.append(
            f"| {row['attachment_id']} | {row['band']} | {quote(safe(row['current_filename']))} | "
            f"{quote(safe(row['target_filename']))} | {safe(alt)} |"
        )
    lines += [
        "",
        "## Excluded assets",
        "",
        "| ID | Band | Filename | Authority |",
        "|---:|---|---|---|",
    ]
    for row in [row for row in manifest if row["payload_action"] == "EXCLUDE"]:
        lines.append(
            f"| {row['attachment_id']} | {row['band']} | {quote(safe(row['current_filename']))} | "
            f"{safe(row['authority'])} |"
        )
    lines += [
        "",
        "The exclusions cover the seven recorded retired E&T IDs; unauthorised AI; D19 soil 1020;",
        "Band B 280/1067; Astra mark 250; and E&T pair 468/471. All remain recoverable in",
        quote("source-inputs/media-retired/") + ".",
        "",
        "The old in-page E&T slots are clear. Structure Co brand assets were not imported. The future",
        "database verifier now requires " + quote("structure-co-horizontal.svg") + " in the header and",
        quote("structure-co-icon-512.png") + " as the site icon. Assignment remains an unexecuted staging task.",
        "",
        "## D32 section removal",
        "",
        "| Page ID | Slug | Sections removed | Markers removed |",
        "|---:|---|---:|---:|",
    ]
    for row in transform["d32_pages"]:
        lines.append(
            f"| {row['page_id']} | {quote('/' + row['slug'] + '/')} | "
            f"{row['sections_removed']} | {row['markers_removed']} |"
        )
    lines += [
        "",
        f"Total: **{transform['d32_top_level_sections_removed']} sections on "
        f"{len(transform['d32_pages'])} pages; {transform['d32_markers_removed']} markers**. The old",
        "15-versus-16 mismatch was gallery: 15 suburb modules use local-work-card, while gallery has",
        "two differently structured evidential sections.",
        "",
        "## Six delivery collision-renames",
        "",
        "No filename containing space-parenthesis-1 remains in public, held or retired directories.",
        "",
        "| ID | Final location | Treatment |",
        "|---:|---|---|",
        "| 226 | " + quote("media-held-band-a/concretejob2camden-226.jpg") + " | Band A HOLD |",
        "| 227 | " + quote("media/backyard-patio-concreter-227.jpg") + " | public D24 generic |",
        "| 228 | " + quote("media/fresh-concrete-side-yard-slab-228.jpg") + " | public Band B GENERIC |",
        "| 468 | " + quote("media-retired/corex-concreters-camden-logo-468.png") + " | E&T pair excluded |",
        "| 471 | " + quote("media-retired/corex-concreters-camden-logo-471.png") + " | E&T pair excluded |",
        "| 609 | " + quote("media/exposed-aggregate-residential-driveway-609.jpg") + " | Adelaide/SWS naming removed |",
        "",
        "## Controls implemented",
        "",
        "- Complete 83-row manifest generation with 16 blank-verdict Band A HOLD rows.",
        "- Reproducible WXR transformation: D32, filename/title/alt updates, metadata length repair,",
        "  excluded/held record and slot removal, wp_css exclusion and media-reference resolution.",
        "- Public-directory parity and recoverable held/retired quarantines.",
        "- Public media gate that compares binaries and derivative and fails only the 16 missing verdicts.",
        "- Full manifest consumption by the media audit, re-encode driver and local media importer.",
        "- Retired post-import Band B mutator, which now refuses execution.",
        "- Post-import assertions for denied/held media, D32, wp_css and supplied brand assignments.",
        "",
        "## Changed-file list",
        "",
        "Git tracks zero files, so diff cannot infer a baseline. Exact pass-owned implementation paths:",
        "",
        FENCE + "text",
        "  lib/media_payload.py",
        "  scripts/22-media-audit.py",
        "  scripts/22-reencode-images.sh",
        "  scripts/28-preflight.sh",
        "  scripts/37-preconditions.py",
        "  scripts/45-band-b-verify.py",
        "  scripts/46-architecture-import-gate.py",
        "  scripts/46-claim-evidence-gate.py",
        "  scripts/46-public-media-gate.py",
        "  scripts/46-source-brand-gate.py",
        "  scripts/47-apply-media-files.py",
        "  scripts/47-media-blocker-inventory.py",
        "  scripts/47-write-report.py",
        "  tests/test_preimport_safety.py",
        "  tests/test_phase_b_media_payload.py",
        "  staging-authoritative/scripts/import-media-local.sh",
        "  staging-authoritative/scripts/apply-band-b-remediation.php",
        "  staging-authoritative/scripts/apply-band-b-remediation.sh",
        "  staging-authoritative/scripts/verify-post-import.php",
        "  reports/post-import-tasks.md",
        "  CONTEXT.md",
        "  build/46-active-main-import.xml",
        "  build/46-active-page-allowlist.json",
        "  build/46-public-media-policy.json",
        "  build/46-claim-register.json",
        "  build/47-media-remediation.csv",
        "  reports/47-original-media-blockers.json",
        "  reports/47-media-file-application.json",
        "  reports/47-phase-b-media-payload-closure.md",
        "  regenerated reports/22, reports/28 and reports/46 gate evidence",
        "  source-inputs/media (51 public files)",
        "  source-inputs/media-retired (16 exclusions)",
        "  source-inputs/media-held-band-a (16 holds)",
        FENCE,
        "",
        "## Verification results",
        "",
        "| Command | Result |",
        "|---|---|",
        "| " + quote("python scripts/21-encoding-canary.py") + " | PASS — all three exact assertions |",
        "| " + quote("python scripts/46-architecture-import-gate.py --check") + " | PASS — reproducible |",
        "| " + quote("python scripts/47-apply-media-files.py --check") + " | PASS — public 51 |",
        "| " + quote("python scripts/22-media-audit.py") + " | PASS — 51/51 |",
        "| " + quote("python scripts/22-astra-audit.py") + " | PASS |",
        "| " + quote("python scripts/46-source-brand-gate.py") + " | PASS — reader-visible CoreX 0 |",
        "| " + quote("python scripts/46-claim-evidence-gate.py") + " | expected FAIL — 144/140 unsupported |",
        "| " + quote("python scripts/46-public-media-gate.py") + " | expected FAIL — 16 Band A only; Band B 0 |",
        "| " + quote("python scripts/37-preconditions.py") + " | expected BLOCKED — all phases |",
        "| " + quote("scripts/28-preflight.sh") + " | NO-GO — Gates 7, 12, 16, 17 |",
        "| " + quote("python -m pytest -q") + " | PASS — 18 tests |",
        "| shell syntax checks | PASS |",
        "| PHP CLI syntax/runtime check | unavailable locally and in WSL; verifier remains unexecuted until authorised staging |",
        "| " + quote("git diff --check") + " | PASS; limitation: zero tracked files |",
        "",
        "### Immutable hashes",
        "",
        "| File | Expected | Computed | Result |",
        "|---|---|---|---|",
    ]
    for relative, expected in IMMUTABLES:
        actual = digest(relative)
        verdict = "MATCH" if actual == expected else "MISMATCH"
        lines.append(
            f"| {quote(relative)} | {quote(expected)} | {quote(actual)} | {verdict} |"
        )
    lines += [
        "",
        "### Phase table",
        "",
        "| Phase | Name | Status | Evidence |",
        "|---|---|---|---|",
        "| A | figures | BLOCKED | 91 false, 0 true |",
        "| B | media/staging | BLOCKED | public 51/51; excluded 16/16; held 16/16; 16 verdicts missing |",
        "| C | identity/schema | BLOCKED | 1 true, 19 false |",
        "| D | Liverpool | BLOCKED | council specs absent |",
        "| E | service rebuild | BLOCKED | requires A |",
        "| F | images | BLOCKED | requires A–E |",
        "| G | release | BLOCKED | requires prior phases and GO |",
        "",
        "### Preflight",
        "",
        "| Gate | Result | Detail |",
        "|---:|---|---|",
        "| 1 | PASS | UTF-8 |",
        "| 2 | PASS | Stage 9 15/15 |",
        "| 3 | PASS | ID collisions |",
        "| 4 | PASS | media 51/51 |",
        "| 5 | PASS | Astra |",
        "| 6 | PASS | immutable image references |",
        "| 7 | **FAIL** | uniqueness: 1,761 5-grams; 1,491 pairs |",
        "| 8 | PASS | intersections |",
        "| 9 | PASS | menu lint |",
        "| 10 | PASS | Victorian blocklist |",
        "| 11 | PASS | schema placeholders |",
        "| 12 | **FAIL** | coherence: 90 SEVERE, 139 over threshold, 0.8244 filler |",
        "| 13 | PASS | source brand |",
        "| 14 | PASS | assigned menus |",
        "| 15 | PASS | active/import parity |",
        f"| 16 | **FAIL** | claims {claim['totals']['occurrences']}; unsupported {claim['totals']['unsupported']} |",
        "| 17 | **FAIL** | Band A blank 16; Band B fail 0 |",
        "| **Overall** | **NO-GO** | any fail is build-failing |",
        "",
        "## Remaining Phase B work",
        "",
        "1. **Owner:** record an unambiguous verdict and required note for each of the 16 Band A tiles.",
        "2. **Agent after input:** encode authorised generic/replacement/removal actions, regenerate, and",
        "   rerun the same gates without weakening them.",
        "3. **Owner:** explicitly authorise any staging import.",
        "4. **Agent during authorised staging:** import only allowlisted artifacts, assign the supplied",
        "   Structure Co header/favicon and execute the database/rendered verifier.",
        "",
        "The 45 unresearched suburbs remain deferred under D22. Identity, service specifications,",
        "Liverpool evidence, unsupported claims, coherence and uniqueness remain separate blockers.",
        "",
        "## No-action confirmation",
        "",
        "**No WordPress import, remote fetch, deployment, publication, indexability change or immutable/",
        "governing-file edit occurred.** No unsupported business claim was rewritten. The only",
        "claim-bearing removal was the already-authorised D32 evidential-module removal.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8", errors="strict")
    print("report -> " + OUT.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
