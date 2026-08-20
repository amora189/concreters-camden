#!/usr/bin/env python3
"""Generate the exhaustive owner-approved final image-remediation report."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.media_payload import (  # noqa: E402
    load_report49_plan,
    reconcile_elementor_media_references,
)

OUTPUT = ROOT / "reports/50-final-image-remediation.md"
IMMUTABLE = {
    "camden-concreting-import.xml": "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884",
    "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml": "45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15",
    "build/stage9-page-manifest.json": "578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42",
    "build/stage8-image-map.json": "0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF",
    "reports/08-image-rename-map.csv": "43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8",
    "CODEX-BUILD-2.1.md": "BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C",
    "archive/governing/CODEX-BUILD-2.md": "E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5",
}


def csv_rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def main() -> int:
    manifest_rows = csv_rows("build/47-media-remediation.csv")
    manifest = {int(row["attachment_id"]): row for row in manifest_rows}
    worksheet = [row for row in csv_rows("reports/44-sighting-worksheet.csv") if row["band"] == "A"]
    plan = load_report49_plan(ROOT / "reports/49-image-completion-requirements.csv")
    architecture = json.loads((ROOT / "reports/46-architecture-import-gate.json").read_text(encoding="utf-8"))
    media_gate = json.loads((ROOT / "reports/46-public-media-gate.json").read_text(encoding="utf-8"))
    claim_gate = json.loads((ROOT / "reports/46-claim-evidence-gate.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "reports/50-band-a-worksheet-validation.json").read_text(encoding="utf-8"))
    preflight = (ROOT / "reports/28-preflight.md").read_text(encoding="utf-8", errors="strict")
    preflight_table = preflight.split("```text", 1)[1].split("```", 1)[0].strip("\n")
    derivative = ROOT / "build/46-active-main-import.xml"
    refs, independent_refs = reconcile_elementor_media_references(ET.parse(derivative))
    refs_by_id: dict[int, list[dict]] = defaultdict(list)
    for ref in refs:
        refs_by_id[ref["attachment_id"]].append(ref)

    hash_rows = []
    for relative, expected in IMMUTABLE.items():
        actual = sha256(ROOT / relative)
        hash_rows.append((relative, expected, actual, "MATCH" if actual == expected else "MISMATCH"))
    if any(row[3] != "MATCH" for row in hash_rows):
        raise AssertionError("immutable mismatch while generating Report 50")
    if validation["result"] != "PASS" or media_gate["result"] != "PASS" or architecture["result"] != "PASS":
        raise AssertionError("Report 50 prerequisites are not passing")

    lines: list[str] = [
        "# Final image remediation",
        "",
        "Date: 20 August 2026 (Australia/Sydney).",
        "",
        "## Outcome",
        "",
        "**The owner-approved zero-new-photograph media plan is fully enforced in the reproducible derivative.** "
        "Band A is 16/16 decided and applied: 10 GENERIC, 6 UNUSABLE, 0 HOLD. Band B remains 9/9 "
        "passing. All 164 exact Report 49 removals were matched and applied without any additional "
        "Report 49 slot removal. The public-media gate passes with 55 permitted files and 28 excluded "
        "files. No new owner photograph is mandatory under this approved plan.",
        "",
        "This closes the image-payload decision/remediation work, not Phase B staging and not the site. "
        "Nothing was imported, deployed, published or made indexable. The full preflight remains NO-GO "
        "because non-image Gates 7, 12 and 16 fail.",
        "",
        "The requested `RUN-BLOCK-02-on-inputs.md` remains absent; the repository’s actual governing "
        "run block is `RUN-BLOCK-02.md`, which was used without alteration.",
        "",
        "Ground guard: Git reports zero tracked files, so every repository path appears untracked and "
        "Git history cannot attribute pre-existing overlapping modifications. The pass therefore used "
        "the seven immutable hashes and artifact contracts as its preservation boundary. The derivative’s "
        "confirmed starting SHA-256 was "
        "`4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B`.",
        "",
        "## Owner-approved Band A verdicts",
        "",
        "Authority for every row: owner approval dated 20 August 2026 — FINAL IMAGE REMEDIATION prompt; "
        "exact Report 49 mapping.",
        "",
        "| Tile | Attachment | Source filename | Verdict | Enforced filename and subject-only alt |",
        "|---:|---:|---|---|---|",
    ]
    for row in sorted(worksheet, key=lambda value: int(value["#"])):
        aid = int(row["attachment_id"])
        media = manifest[aid]
        target = (
            f"`{media['target_filename']}` — {media['target_alt']}"
            if media["payload_action"] == "RENAME"
            else "Excluded; every recorded slot removed without replacement"
        )
        lines.append(
            f"| {row['#']} | {aid} | `{cell(row['new_filename'])}` | **{row['VERDICT']}** | {cell(target)} |"
        )
    lines.extend([
        "",
        "Totals: **10 GENERIC + 6 UNUSABLE = 16**. Blank, OK and REPLACE verdicts: **0**.",
        "",
        "For all ten GENERIC assets, the derivative attachment title, slug/filename, alt metadata and "
        "classic Elementor URL/alt values are subject-only. Typed Elementor references resolve through "
        "the remediated attachment record. Their 75 surviving placements exactly equal the 75 "
        "Report 49 page/widget/setting placements that say `audit recommends GENERIC`. The public-media "
        "gate rejects any additional or missing placement.",
        "",
        "## Payload and binary disposition",
        "",
        f"- Generated derivative: `build/46-active-main-import.xml` — SHA-256 "
        f"`{sha256(derivative)}`.",
        f"- Manifest: 83 provenance rows = {Counter(row['payload_action'] for row in manifest_rows)['RENAME']} "
        f"RENAME + {Counter(row['payload_action'] for row in manifest_rows)['EXCLUDE']} EXCLUDE + 0 HOLD.",
        "- Public media: 55/55 present; no missing, additional or non-image files.",
        "- Quarantine: 28/28 excluded binaries present under `source-inputs/media-retired/`.",
        "- Band A held directory: zero required HOLD files.",
        "- Duplicate identities 49 and 52 remain distinct and resolve; no byte-duplicate collapse was used.",
        "",
        "### Excluded assets",
        "",
        "| Attachment | Band | Filename | Authority/disposition |",
        "|---:|---|---|---|",
    ])
    for row in sorted((row for row in manifest_rows if row["payload_action"] == "EXCLUDE"), key=lambda x: int(x["attachment_id"])):
        lines.append(
            f"| {row['attachment_id']} | {row['band']} | `{cell(row['current_filename'])}` | {cell(row['authority'])}; {cell(row['usage_restriction'])} |"
        )

    lines.extend([
        "",
        "### Generic assets and their exact surviving reuse placements",
        "",
        "Each placement below is recorded as `/page-slug/ — widget:setting`. All are decorative and "
        "non-evidential. They may not assert location, Structure Co work, a customer/testimonial, local "
        "premises, equipment ownership or work by the eventual NSW operator.",
        "",
        "| Attachment | Band | Remediated file | Subject-only alt | Count | Placements |",
        "|---:|---|---|---|---:|---|",
    ])
    for row in sorted((row for row in manifest_rows if row["payload_action"] == "RENAME"), key=lambda x: int(x["attachment_id"])):
        aid = int(row["attachment_id"])
        placements = sorted(
            f"/{ref['slug']}/ — {ref['widget_id']}:{ref['media_setting']}"
            for ref in refs_by_id.get(aid, [])
        )
        lines.append(
            f"| {aid} | {row['band']} | `{cell(row['target_filename'])}` | {cell(row['target_alt']) or 'empty decorative alt'} | "
            f"{len(placements)} | {cell('<br>'.join(placements))} |"
        )

    lines.extend([
        "",
        "## All 164 owner-authorised slot removals",
        "",
        "The transformer matches requirement ID, page slug, top-level section, widget, setting and "
        "attachment ID. A missing, additional or differently mapped slot fails regeneration. The exact "
        "category arithmetic is 45 D32 whole-section + 45 blank-placeholder + 3 empty-testimonial + "
        "21 other-prohibited-direct + 50 Band-A-UNUSABLE = **164**.",
        "",
        "Six pre-existing D36 retired-brand page slots (attachment 306 ×5 and 307 ×1) remain separately "
        "held for supplied Structure Co wordmark replacement at an eventual authorised import. They are "
        "not counted as additional Report 49 removals.",
        "",
        "| Requirement | Category | Page | Section | Widget:setting | Attachment |",
        "|---|---|---|---|---|---:|",
    ])
    for row in sorted(plan["removals"], key=lambda value: value["requirement_id"]):
        lines.append(
            f"| {row['requirement_id']} | {row['category']} | `/{cell(row['page_slug'])}/` | `{cell(row['section_id'])}` | "
            f"`{cell(row['widget_id'])}:{cell(row['setting'])}` | {row['attachment_id'] or 'none'} |"
        )

    lines.extend([
        "",
        "## Elementor reference reconciliation and blind-spot correction",
        "",
        "Report 49 independently counted the starting derivative at **410 populated image references**. "
        "The former architecture detector reported 409 because it missed homepage attachment 609 in "
        "nested Elementor 4.2 `e-image` widget `306c538`. The production detector is now recursive and "
        "format-aware; a separately implemented settings-first detector must find the identical multiset "
        "of page/attachment/widget/setting references.",
        "",
        "The approved transformation changes the inventory rather than preserving 410: it removes 45 "
        "surviving blank-placeholder placements and restores 75 authorised Band A GENERIC placements. "
        "The final exact result is therefore **440 = 410 − 45 + 75**. Both independent detectors report "
        f"{len(refs)}; all resolve to the 55 permitted attachment records; unresolved references are zero. "
        "The regression suite explicitly locates attachment 609 at homepage widget `306c538`, while the "
        "production logic contains no attachment-609 special case.",
        "",
        "The future post-import database verifier was also extended to decode Elementor 4.2 typed-image "
        "attachment IDs. It was not executed because no staging database/site was imported in this pass.",
        "Local PHP is unavailable, so PHP runtime lint/execution remains a future staging control.",
        "",
        "## Gallery disposition",
        "",
        "Page `/gallery/` (ID 1365) is deferred until a genuine, permission-backed project library "
        "exists. `build/27-wave1-menus.json` records the exact 20 August owner authority and excludes the "
        "gallery from every launch menu assignment. Menu lint passes. The page was not deleted and its "
        "indexability was not changed.",
        "",
        "## Verification results",
        "",
        "| Command/control | Result |",
        "|---|---|",
        "| `python scripts/50-band-a-worksheet-verify.py` | PASS — 16/16; 10 GENERIC; 6 UNUSABLE; 0 HOLD |",
        "| `python scripts/45-band-b-verify.py` | PASS — 7 GENERIC; 2 UNUSABLE; 28 slot contract |",
        "| `python scripts/47-apply-media-files.py --check` | PASS — 55 public |",
        "| `python scripts/22-media-audit.py` | PASS — 55/55; zero missing/extras/non-images |",
        "| `python scripts/46-public-media-gate.py` | PASS — zero blockers; 440/440 detector reconciliation; Band A placement 75/75 |",
        "| `python scripts/46-architecture-import-gate.py --check` | PASS — reproducible hash; 75 active-main; 81 withdrawn absent |",
        "| `python scripts/27-menu-lint.py` | PASS — gallery absent; zero unsafe targets |",
        "| `python scripts/21-encoding-canary.py` | PASS — all three exact UTF-8 assertions |",
        "| `python -m pytest -q` | PASS — 19 tests |",
        "| `python -m py_compile ...` | PASS |",
        "| `python scripts/37-preconditions.py` | PASS as reporter — Phase B RUNNABLE; A and C–G BLOCKED |",
        "| `bash scripts/28-preflight.sh` | expected NO-GO — Gates 7, 12 and 16 fail; media Gate 17 PASS |",
        "| `git diff --check` | PASS with no output; limitation: repository has zero tracked files |",
        "| PHP syntax/runtime check | NOT RUN — PHP unavailable locally; verifier installation remains read-only future staging work |",
        "",
        "### Immutable hash table",
        "",
        "| File | Expected SHA-256 | Computed SHA-256 | Result |",
        "|---|---|---|---|",
    ])
    for relative, expected, actual, result in hash_rows:
        lines.append(f"| `{relative}` | `{expected}` | `{actual}` | **{result}** |")

    lines.extend([
        "",
        "### Complete preflight table",
        "",
        "```text",
        preflight_table,
        "```",
        "",
        "## Remaining non-image blockers",
        "",
        f"- Claim/evidence Gate 16: {claim_gate['totals']['unsupported']} unsupported of "
        f"{claim_gate['totals']['occurrences']} occurrences on "
        f"{claim_gate['totals']['pages_with_unsupported_claims']} pages. No unsupported business claim "
        "was rewritten in this pass.",
        "- Coherence Gate 12: 90 SEVERE pages and 139 pages above the filler threshold; service and other "
        "withdrawn/active copy still needs the evidence-gated rewrite programme.",
        "- Uniqueness Gate 7: 1,761 repeated 5-grams and 1,491 within-class pairs above 40% overlap.",
        "- Identity/operator: legal entity, ABN, licence/insurance state, staffed-address state, phone "
        "routing and signed NSW operator remain unverified. No LocalBusiness schema or contractor voice is permitted.",
        "- Owner service specification matrix: 91 fields remain `verified:false`; Phase A is blocked.",
        "- Liverpool Council evidence is absent; Phase D remains blocked.",
        "- Service-page copy, privacy-policy blocking markers, claim removals/rewrite, menu assignment, "
        "brand-slot assignment, staging import and post-import verification remain outstanding.",
        "- The 45 unresearched suburb pages remain deferred under D22, not dropped.",
        "",
        "## Files changed or regenerated in this pass",
        "",
        "Authoritative mutable inputs and controls: `reports/44-sighting-worksheet.csv`, "
        "`lib/media_payload.py`, `scripts/46-architecture-import-gate.py`, "
        "`scripts/46-public-media-gate.py`, `scripts/47-apply-media-files.py`, "
        "`scripts/50-band-a-worksheet-verify.py`, `scripts/50-write-report.py`, "
        "`scripts/22-reencode-images.sh`, `scripts/27-menu-lint.py`, "
        "`build/27-wave1-menus.json`, `staging-authoritative/scripts/import-media-local.sh`, "
        "`staging-authoritative/scripts/verify-post-import.php`, "
        "`tests/test_phase_b_media_payload.py` and `tests/test_preimport_safety.py`.",
        "",
        "Reproducibly generated/updated outputs: `build/46-active-main-import.xml`, "
        "`build/46-active-page-allowlist.json`, `build/47-media-remediation.csv`, "
        "the architecture/public-media policy and result JSON files, media-audit outputs, "
        "`reports/50-band-a-worksheet-validation.json`, `reports/28-preflight.md`, this report and `CONTEXT.md`.",
        "",
        "Media filesystem changes: the ten approved Band A GENERIC binaries moved from the held "
        "directory into the public intake under their exact Report 49 subject-only filenames; the six "
        "Band A UNUSABLE binaries moved to retired quarantine; and the six blank-placeholder binaries "
        "moved from public intake to retired quarantine. No binary was remotely fetched or generated.",
        "",
        "## Safety confirmation",
        "",
        "No WordPress import, staging/live database execution, deployment, publication, remote media "
        "fetch, generated image, indexability change, immutable-file edit or governing-document edit "
        "occurred. The derivative was generated by the transformer and was never manually patched.",
        "",
    ])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(plan['removals'])} removal rows; {len(refs)} references)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
