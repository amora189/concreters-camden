# Phase D — Liverpool Council content completion

Date: 21 August 2026 (Australia/Sydney)

## Outcome

Phase D is complete for its authorised scope. The current March 2026 Liverpool City Council
Vehicular Crossing Application and Specifications was checked page by page, 13 requirements were
validated, and 12 exact evidence fields were applied to the four Liverpool-affected pages through
the reproducible derivative pipeline. The affected-page false-fidelity residue is zero. The
calculator remains absent, unbuilt and excluded.

This does not authorise publication. Full preflight remains **NO-GO** on unchanged Gate 7
uniqueness and Gate 12 coherence failures.

## Source set

All sources were accessed on 21 August 2026.

- [Current March 2026 Vehicular Crossing Application and Specifications](https://www.liverpool.nsw.gov.au/__data/assets/pdf_file/0003/286329/VEHICULAR-CROSSING-APPLICATION-FORM-March-2026v1.pdf) — 18 pages; downloaded source SHA-256 `43F74C0F01C5EA6F0C89919BE8C1859F758F96AF549A9CF71ADA5F87DD7CAF33`.
- [Liverpool City Council forms](https://www.liverpool.nsw.gov.au/council/Fees-Forms-Policies-and-Enforcement/forms) — exposes the current March 2026 form.
- [Liverpool City Council online application portal](https://mycouncil.liverpool.nsw.gov.au/ePathway/Production/Web/Default.aspx) — exposes the Driveway Crossing application path.

The PDF was text-extracted and all 18 pages were rendered for visual checking. A citation defect
was corrected in the mutable Council register: `utilities.source_pages` was `[6]` and is now
`[6, 7]`. Electricity, communications and Sydney Water controls appear on page 6; stormwater and
pram-ramp controls continue on page 7. No Council meaning or requirement was changed.

## The 13 validated Council requirements

| # | Ledger field | Evidence-supported result | Form pages | Applied block |
|---:|---|---|---:|---:|
| 1 | `roads_act_section_138` | Application is made under section 138 of the Roads Act 1993. | 1 | 1 |
| 2 | `owner_cost_responsibility` | The property owner is responsible for crossing construction, maintenance and repair costs. | 2, 5 | 1 |
| 3 | `contractor_licensing_and_liability` | The owner must ensure the contractor is licensed and holds current public-liability cover of at least $10 million. This is not represented as a Structure Co credential. | 1, 2, 5 | 1 |
| 4 | `surface` | The proposed crossing surface is plain concrete. | 1 | 1 |
| 5 | `residential_strength` | Minimum 25 MPa at 28 days for residential driveways. | 8 | 2 |
| 6 | `medium_density_commercial_industrial_strength` | Minimum 32 MPa at 28 days for medium-density, commercial and industrial driveways. | 8 | 2 |
| 7 | `crossing_bedding` | Minimum 50 mm compacted DGS20 bedding for the crossing. | 7 | 2 |
| 8 | `kerb_gutter_layback_bedding` | Minimum 100 mm compacted DGS20 bedding where kerb, gutter or layback is constructed. | 7 | 2 |
| 9 | `pre_pour_inspection` | Completed formwork and associated works require inspection and Council approval before pouring. | 2, 5, 10 | 3 |
| 10 | `drawings_and_directions` | Construction is to follow Council drawing R25 and site-specific directions from the crossing inspector. | 7 | 3 |
| 11 | `utilities` | Applicable clearances and approvals for electricity, communications, Sydney Water, stormwater, drainage structures, street trees and pram ramps must be resolved. | 6, 7 | 3 |
| 12 | `application_and_inspection_process` | Apply through Council and book the required inspection using the Council application number. | 2, 10 | 3 |
| 13 | `fees` | Fees are assessed under Council's current schedule. No dollar amount is asserted. | 2 | 1 |

No precinct-specific DCP control, universal dimension, fee amount, approval time or permit outcome
was introduced.

## Exact content dispositions

The transformer applies the same three evidence blocks to the same three existing nested-accordion
fields on each affected page. The page IDs, slugs and intended WXR statuses were not changed.

| Field | Page ID | Page | Intended status | Exact Elementor placement | Disposition |
|---|---:|---|---|---|---|
| LVP-01 | 221 | `concreters-leppington` | publish | `_elementor_data:$[13].elements[2].elements[0].elements[0].settings.editor` | Block 1 applied from official evidence |
| LVP-02 | 221 | `concreters-leppington` | publish | `_elementor_data:$[13].elements[2].elements[1].elements[0].settings.editor` | Block 2 applied from official evidence |
| LVP-03 | 221 | `concreters-leppington` | publish | `_elementor_data:$[13].elements[2].elements[2].elements[0].settings.editor` | Block 3 applied from official evidence |
| LVP-04 | 1163 | `concreters-austral` | publish | `_elementor_data:$[13].elements[2].elements[0].elements[0].settings.editor` | Block 1 applied from official evidence |
| LVP-05 | 1163 | `concreters-austral` | publish | `_elementor_data:$[13].elements[2].elements[1].elements[0].settings.editor` | Block 2 applied from official evidence |
| LVP-06 | 1163 | `concreters-austral` | publish | `_elementor_data:$[13].elements[2].elements[2].elements[0].settings.editor` | Block 3 applied from official evidence |
| LVP-07 | 1387 | `concreters-edmondson-park` | draft | `_elementor_data:$[13].elements[2].elements[0].elements[0].settings.editor` | Block 1 applied from official evidence |
| LVP-08 | 1387 | `concreters-edmondson-park` | draft | `_elementor_data:$[13].elements[2].elements[1].elements[0].settings.editor` | Block 2 applied from official evidence |
| LVP-09 | 1387 | `concreters-edmondson-park` | draft | `_elementor_data:$[13].elements[2].elements[2].elements[0].settings.editor` | Block 3 applied from official evidence |
| LVP-10 | 1388 | `concreters-bringelly` | draft | `_elementor_data:$[13].elements[2].elements[0].elements[0].settings.editor` | Block 1 applied from official evidence |
| LVP-11 | 1388 | `concreters-bringelly` | draft | `_elementor_data:$[13].elements[2].elements[1].elements[0].settings.editor` | Block 2 applied from official evidence |
| LVP-12 | 1388 | `concreters-bringelly` | draft | `_elementor_data:$[13].elements[2].elements[2].elements[0].settings.editor` | Block 3 applied from official evidence |

The machine-readable record, including the exact final text and requirement-to-field mapping, is
`build/52-liverpool-field-register.json`.

### Block 1 disposition

Superseded research placeholders were replaced with section 138, owner cost responsibility,
contractor licence/$10 million public-liability responsibility, plain-concrete surface, current
forms/application links and current-schedule fee wording. The content says to confirm that the
March 2026 form and fee schedule remain current before relying on them.

### Block 2 disposition

False-fidelity specification wording was replaced with the verified 25/32 MPa at 28 days and
50/100 mm DGS20 bedding requirements. No universal crossing width or precinct DCP control is
stated.

### Block 3 disposition

The content now states drawing R25/site-specific inspector directions, applicable utility
clearances, the pre-pour inspection/approval requirement, and the Council application number used
to book inspection. It explicitly says Council assesses each application and site and that the
Council process does not state that Structure Co holds the contractor licence or insurance.

## Executable controls

- `scripts/52-phase-d-liverpool.py` fails on a missing, additional or differently cited Council
  requirement; a changed source URL/date/PDF hash; any missing or moved field; altered page ID,
  slug or status; Phase D false-fidelity residue; invented fee/approval language; precinct DCP or
  universal-width language; missing qualifications; or the calculator being present.
- The validator materialises recursive reader-visible fields before checking all three blocks;
  regression coverage prevents the prior generator-exhaustion blind spot.
- `scripts/28-preflight.sh` now includes fail-closed Gate 19, which asserts the generated Phase D
  result offline on every full preflight.
- `tests/test_phase_d_liverpool.py` covers the complete generated Phase D payload.
- The stale pre-Report-51 claim regression was corrected to require the current 16 supported,
  zero unsupported, fail-closed claim result.

The Phase D validator scans only the four authorised pages. The unchanged full-site coherence gate
still reports 11 `reproduced without alteration` occurrences outside Phase D in blocked home/service
content; they were not rewritten because another content phase was not authorised.

## Generated derivative

`build/46-active-main-import.xml` was regenerated from the immutable source by
`scripts/46-architecture-import-gate.py`; it was not manually patched.

| Artifact | SHA-256 |
|---|---|
| Starting derivative | `9FA49392B181EE839954A0FB9F306B6E4EB7CA4891ED921CF14079EE8AE4CB82` |
| Phase D derivative | `4D28AE2E24F6A6EE9BD34B4AA60497F30F8E93A7538E45606BAC809D130B6D18` |

Architecture arithmetic remains `156 main = 75 allowed + 81 withdrawn`; the separate privacy page
makes 76 built active pages. The calculator is absent.

## Verification results

| Check | Result | Detail |
|---|---|---|
| Immutable hashes | PASS | 7/7 match |
| Official PDF/source validation | PASS | 13/13 requirements, all cited page excerpts matched; forms and portal confirmed |
| Liverpool field validation | PASS | 12/12 fields on 4/4 pages |
| Phase D false-fidelity scan | PASS | 0 affected-page residues |
| Claim-to-evidence parity | PASS | 16 supported, 0 unsupported; 232/228 legacy occurrences dispositioned |
| Schema | PASS | 76 page graphs, 70 Service nodes, no Organization, LocalBusiness or provider |
| Identity/privacy/schema evidence | PASS | 12 Liverpool placements; 5 privacy blockers retained |
| Active/import architecture | PASS | 76 allowed including privacy; 81 withdrawn absent; calculator absent |
| UTF-8 canary | PASS | all three exact assertions survived |
| `unittest` discovery | PASS | 12/12 |
| `pytest` regressions | PASS | 24/24 |
| `git diff --check` | PASS | no whitespace errors in tracked diff; repository has no tracked baseline |

## Phase precondition table

This table reports input readiness, not phase execution history. Phase D therefore remains
`RUNNABLE` here while Gate 19 and this report record that its authorised execution is complete.

| Phase | Name | Status | Evidence |
|---|---|---|---|
| A | attest the figures | BLOCKED | 91 fields `verified:false`, 0 true |
| B | media and staging | RUNNABLE | public media 55/55; 28/28 excluded assets quarantined; no Band A hold |
| C | identity and schema | BLOCKED | 11 verified / 14 false; legal name, ABN, NSW licence and public liability remain unverified |
| D | Liverpool | RUNNABLE | 16 verified values, URLs and sighting dates; execution separately complete |
| E | service page rebuild | BLOCKED | requires Phase A service matrix |
| F | images | BLOCKED | designed to follow A–E |
| G | release | BLOCKED | requires preceding phases and preflight GO |

## Complete preflight table

| Gate | Result | Detail |
|---|---|---|
| 1. encoding canary | PASS | fixture and both restored assertions survived |
| 2. 15 Stage 9 gates | PASS | 15/15 pass |
| 3. post-ID collision audit | PASS | main 306 IDs; privacy 1; collisions 0; calculator absent |
| 4. media intake audit | PASS | public intake 55/55; immutable provenance baseline 83 |
| 5. Astra Customizer audit | PASS | required groups, design carriage and consistency pass |
| 6. Elementor image-reference count | PASS | 1,085 image + 98 background = 1,183; 73/83 attachment IDs; 0 unresolved |
| 7. uniqueness gates | **FAIL** | 1,761 five-grams on more than two pages; 1,491 within-class pairs over 40% overlap |
| 8. intersection audit | PASS | 35 built/allow-listed; all draft |
| 9. menu lint | PASS | zero draft, noindex or 404 targets in Wave 1 spec |
| 10. Victorian blocklist | PASS | zero in scoped public artifacts; 13 terms checked |
| 11. placeholder-in-schema | PASS | zero JSON-LD blocks and zero placeholder tokens |
| 12. coherence | **FAIL** | 90 SEVERE; 139 above threshold; corpus filler 0.8244 |
| 13. source-brand transformation | PASS | baseline 466 = 366 visible + 100 preserved; transformed visible 0 |
| 14. assigned-menu safety | PASS | zero unsafe assigned targets; held 6; withdrawn 81 |
| 15. architecture/import parity | PASS | 76 allowed; 75 main + privacy; 81 withdrawn; calculator absent |
| 16. claim/evidence parity | PASS | 16 occurrences; 0 unsupported; 6 pages; 0 unsupported pages |
| 17. public-media suitability | PASS | 0 blockers; 0 unrecorded Band A; 0 Band B failures |
| 18. identity/Liverpool/schema evidence | PASS | 0 unsupported claims; 12 Liverpool placements; 5 privacy blockers; 0 LocalBusiness |
| 19. Phase D Liverpool content | PASS | 13 requirements; 12 fields; 4 pages; 0 false-fidelity; calculator absent |
| **Overall** | **NO-GO** | Gates 7 and 12 fail |

Gate 7 and Gate 12 were not weakened.

## Immutable hash table

| Immutable file | Expected SHA-256 | Computed SHA-256 | Result |
|---|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | MATCH |

## Remaining Phase D blockers

None. Phase D's authorised evidence/content scope is complete.

The site remains blocked outside Phase D by the service specification matrix, service/home copy
coherence and uniqueness, identity/privacy inputs, staging/import verification and release approval.
The four affected WXR records retaining `publish` status are not approved for launch; WXR status is
not launch authorisation.

## Repository and scope notes

The requested `RUN-BLOCK-02-on-inputs.md` path is absent. The existing governing file is
`RUN-BLOCK-02.md`, which was read and followed. Git reports no tracked files, so it cannot attribute
pre-existing untracked content to an owner or task; all unrelated files were preserved.

Phase-authored or materially updated files are:

- `lib/content_remediation.py`
- `data/council-specs.yml`
- `scripts/52-phase-d-liverpool.py`
- `tests/test_phase_d_liverpool.py`
- `scripts/28-preflight.sh`
- `tests/test_preimport_safety.py`
- `build/21-spec-ledger.json`
- `build/46-active-main-import.xml` (generated)
- `build/52-liverpool-field-register.json` (generated)
- `reports/52-liverpool-validation.json` (generated)
- `reports/52-phase-d-liverpool-completion.md`
- `CONTEXT.md`

Existing architecture, claim, schema, media, coherence and preflight result artifacts were refreshed
by their normal validation commands.

No WordPress import, deployment, publication, indexability change, immutable-file edit or
governing/decision-document edit occurred.
