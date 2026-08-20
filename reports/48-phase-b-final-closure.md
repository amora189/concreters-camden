# Phase B final-closure verification

Date: 20 August 2026 (Australia/Sydney).

## Outcome

**BLOCKED — the claimed completed owner input is not present in the authoritative CSV.**

`reports/44-sighting-worksheet.csv` contains exactly 83 data rows and 16 Band A rows, but all
16 Band A `VERDICT` cells and all 16 corresponding `NOTE` cells are empty. The worksheet SHA-256 is
`6C7826FF7AA7184A23674C709FE03DF85D84FE43E0011E1AAAF8245E0D5C11B4`.

No verdict was inferred from a filename, old source location, replacement brief or photograph.
Consequently:

- no OK asset was accepted without cited provenance evidence;
- no Band A asset was reclassified as GENERIC;
- no replacement was selected or remotely fetched;
- no Band A asset was marked UNUSABLE;
- all 16 Band A assets remain fail-closed outside the public media directory and derivative; and
- `build/46-active-main-import.xml` was regenerated only through the reproducible pipeline using
  the current blank-verdict inputs; it retained its prior hash and 16-HOLD state. It was not
  manually edited or made to pretend the missing decisions had been supplied.

Phase B remains blocked. Index-ready remains **0 of 77** and launch remains **NO-GO**.

The requested `RUN-BLOCK-02-on-inputs.md` does not exist. The repository's actual governing run
block is `RUN-BLOCK-02.md`; it was read without alteration.

## Band A owner-verdict verification

| Tile | Attachment ID | Worksheet filename | VERDICT | NOTE | Enforced state |
|---:|---:|---|---|---|---|
| 1 | 907 | `camden-town-centre-907.jpg` | **BLANK** | **BLANK** | HOLD |
| 2 | 924 | `coloured-concrete-south-west-sydney-924.png` | **BLANK** | **BLANK** | HOLD |
| 3 | 226 | `concretejob2camden-226.jpg` | **BLANK** | **BLANK** | HOLD |
| 4 | 1185 | `council-crossing-south-west-sydney-1185.jpg` | **BLANK** | **BLANK** | HOLD |
| 5 | 906 | `driveway-excavation-camden-906.jpg` | **BLANK** | **BLANK** | HOLD |
| 6 | 1150 | `established-home-mount-annan-1150.jpg` | **BLANK** | **BLANK** | HOLD |
| 7 | 1186 | `gregory-hills-commercial-concreting-1186.webp` | **BLANK** | **BLANK** | HOLD |
| 8 | 1187 | `leppington-new-estates-1187.jpg` | **BLANK** | **BLANK** | HOLD |
| 9 | 1152 | `mount-annan-established-housing-1152.jpg` | **BLANK** | **BLANK** | HOLD |
| 10 | 908 | `oran-park-growth-estate-908.jpg` | **BLANK** | **BLANK** | HOLD |
| 11 | 480 | `oran-park1-480.webp` | **BLANK** | **BLANK** | HOLD |
| 12 | 481 | `oran-park2-481.webp` | **BLANK** | **BLANK** | HOLD |
| 13 | 482 | `oran-park3-482.webp` | **BLANK** | **BLANK** | HOLD |
| 14 | 956 | `south-west-sydney-growth-corridor-956.png` | **BLANK** | **BLANK** | HOLD |
| 15 | 926 | `stamped-concrete-south-west-sydney-926.jpg` | **BLANK** | **BLANK** | HOLD |
| 16 | 925 | `stencil-concrete-south-west-sydney-925.webp` | **BLANK** | **BLANK** | HOLD |

Summary: **0 explicit; 16 blank**.

## Verdict-specific controls

No verdict-specific Band A branch was authorised by the worksheet:

| Verdict | Recorded rows | Control result |
|---|---:|---|
| OK | 0 | No asset accepted. The required provenance citation condition was not reached. |
| GENERIC | 0 | No geographic filename, alt, metadata or placement rewrite was authorised. |
| REPLACE | 0 | No supplied replacement could be selected; no slot was opened. |
| UNUSABLE | 0 | No new asset exclusion or slot removal was authorised. |
| Blank | 16 | Every asset and affected slot remains fail-closed through `HOLD`. |

The existing Band B decisions remain enforced independently: seven GENERIC assets pass their
subject-only filename/alt and decorative-only contract, and attachments 280 and 1067 remain
excluded with all 28 source slots absent. Band B verification is **9 of 9 PASS**.

## Reproducible pipeline and Elementor verification

The pipeline regenerated the existing fail-closed derivative from the immutable WXR and current
authoritative mutable inputs during full preflight, then check mode reproduced it byte-for-byte:

```text
  build/46-active-main-import.xml
    SHA-256       4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B
    pages         75 active-main; 81 withdrawn absent
    attachments   51 permitted
    manifest      83 = 51 RENAME + 16 EXCLUDE + 16 HOLD
    Elementor     409 surviving references; unresolved 0

  build/47-media-remediation.csv
    SHA-256       067C20884CD4CE2DAA280FF567ADA592CF1E236489B1D87B076E4F6B52959798
```

All 16 held Band A records and their active-page Elementor slots are absent from the derivative.
All 16 binaries remain recoverably quarantined in `source-inputs/media-held-band-a/`; none is in
`source-inputs/media/`. This is a containment result, not an owner verdict.

## Verification results

| Command | Result |
|---|---|
| `python scripts/21-encoding-canary.py` | PASS — all three exact UTF-8 assertions |
| `python scripts/46-architecture-import-gate.py --check` | PASS — derivative reproducible; 75 active main + privacy; 81 withdrawn absent |
| `python scripts/47-apply-media-files.py --check` | PASS — public filesystem parity 51 |
| `python scripts/22-media-audit.py` | PASS — 51/51; missing/extras/non-images 0 |
| `python scripts/22-astra-audit.py` | PASS |
| `python scripts/45-band-b-verify.py` | PASS — 7 GENERIC + 2 UNUSABLE; 28 slots |
| `python scripts/46-source-brand-gate.py` | PASS — reader-visible CoreX remainder 0 |
| `python scripts/46-claim-evidence-gate.py` | expected FAIL — 144 occurrences; 140 unsupported; 16 unsupported pages |
| `python scripts/46-public-media-gate.py` | expected FAIL — 16 Band A verdicts unrecorded; Band B failures 0 |
| `python scripts/37-preconditions.py` | expected BLOCKED — every phase; Phase B cites 16 missing owner verdicts |
| `wsl.exe bash scripts/28-preflight.sh` | NO-GO — Gates 7, 12, 16 and 17 fail |
| `python -m pytest -q` | PASS — 18 tests |

### Preflight table

| Gate | Result | Detail |
|---:|---|---|
| 1 | PASS | UTF-8 canary |
| 2 | PASS | Stage 9, 15/15 |
| 3 | PASS | post-ID collisions 0 |
| 4 | PASS | public media 51/51 |
| 5 | PASS | Astra |
| 6 | PASS | immutable Elementor references: 1,085 images + 98 backgrounds; unresolved 0 |
| 7 | **FAIL** | 1,761 repeated 5-grams; 1,491 pairs over overlap cap |
| 8 | PASS | intersections |
| 9 | PASS | Wave 1 menu lint |
| 10 | PASS | Victorian blocklist |
| 11 | PASS | schema placeholders |
| 12 | **FAIL** | 90 SEVERE; 139 above threshold; corpus filler 0.8244 |
| 13 | PASS | source-brand transformation |
| 14 | PASS | assigned menus |
| 15 | PASS | active/import parity |
| 16 | **FAIL** | claims 144; unsupported 140 |
| 17 | **FAIL** | Band A unrecorded 16; Band B failed 0 |
| **Overall** | **NO-GO** | Any failure is build-failing |

### Phase table

| Phase | Name | Status | Evidence |
|---|---|---|---|
| A | figures | BLOCKED | 91 fields `verified:false`; 0 true |
| B | media/staging | BLOCKED | public 51/51; excluded 16/16; held 16/16; owner verdicts missing 16 |
| C | identity/schema | BLOCKED | 1 verified true; 19 false |
| D | Liverpool | BLOCKED | `data/council-specs.yml` absent |
| E | service rebuild | BLOCKED | requires Phase A |
| F | images | BLOCKED | requires A–E |
| G | release | BLOCKED | requires preceding phases and preflight GO |

## Immutable hashes

| File | Expected/computed SHA-256 | Result |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | MATCH |

## Changed-file list

The repository has zero tracked files, so Git cannot infer a byte-diff baseline. The only
substantive pass-authored state changes are:

```text
  reports/48-phase-b-final-closure.md
  CONTEXT.md
```

The required verification commands also reproducibly rewrote their generated outputs/evidence:

```text
  build/46-active-main-import.xml
  build/46-active-page-allowlist.json
  build/46-claim-register.json
  build/46-public-media-policy.json
  build/47-media-remediation.csv
  reports/22-media-audit-result.md
  reports/22-media-missing-manifest.csv
  reports/22-astra-audit-result.md
  reports/28-gates.err
  reports/28-gates.json
  reports/28-preflight.md
  reports/34-coherence.csv
  reports/34-coherence-summary.json
  reports/34-coherence.out
  reports/45-band-b-application.md
  reports/45-band-b-unusable-slots.csv
  reports/46-architecture-import-gate.json
  reports/46-architecture-import-gate.out
  reports/46-claim-evidence-gate.json
  reports/46-claim-evidence-gate.out
  reports/46-claim-register.csv
  reports/46-public-media-gate.json
  reports/46-public-media-gate.out
  reports/46-source-brand-gate.json
  reports/46-source-brand-gate.out
  reports/47-media-file-application.json
```

The generated derivative and remediation manifest retained their prior SHA-256 values. The pytest
cache was refreshed. No transformer source, media binary, immutable file, governing instruction or
decision document was changed.

## Remaining Phase B action

The owner must save an explicit `OK`, `GENERIC`, `REPLACE` or `UNUSABLE` value in the `VERDICT`
column for each of rows 1–16 in `reports/44-sighting-worksheet.csv`, with the required evidence or
remediation detail in `NOTE`:

- OK requires a cited provenance source that proves the geographic claim;
- GENERIC requires an authorised subject-only filename and alt description;
- REPLACE requires an already supplied verified replacement mapping, otherwise the slot remains
  fail-closed; and
- UNUSABLE removes the asset and all slots without replacement.

After that file exists on disk with all 16 decisions, rerun this closure pass. No staging import is
authorised by completing the worksheet.

## No-action confirmation

**No WordPress import, remote media fetch, deployment, publication, indexability change, unsupported
claim rewrite, immutable-file edit or governing-document edit occurred.** No assertion was weakened.
