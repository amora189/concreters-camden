# Report 53 — Phase A service specification evidence acquisition

Date: 21 August 2026

## Plain-English determination

The ten-service × nine-field matrix contains exactly 90 cells. 88 cells have an authoritative source supporting either a constraint or a justified non-universal classification. None creates a Structure Co construction method. There are 71 design/site-specific cells, 6 provider-method cells and 2 unresolved cells.

Phase A is **not marked complete**. Two curing cells remain unresolved because the accessible authority establishes a structural design pathway but not an exact curing specification for these broad services; the directly linked industry curing PDF could not be opened. Independently, the legacy D23 attestation file has zero verified values and a pre-existing YAML syntax defect. Zero service pages are formally unblocked for Phase E until the governing owner/engineer attestation requirement is resolved or explicitly superseded.

## Ground and service inventory

The seven immutable files matched their recorded SHA-256 values before work. Git has no tracked baseline: every repository file is untracked, so overlap attribution is unavailable; existing files were preserved.

The requested `RUN-BLOCK-02-on-inputs.md` does not exist. The repository's governing run block is `RUN-BLOCK-02.md`, which was read and applied.

| ID | Service | Slug |
|---:|---|---|
| 105 | Concrete Driveways | `concrete-driveways-south-west-sydney` |
| 129 | Exposed Aggregate | `exposed-aggregate-south-west-sydney` |
| 163 | Concrete Slabs | `concrete-slabs-south-west-sydney` |
| 178 | Concrete Paths | `concrete-paths-south-west-sydney` |
| 195 | Concrete Patios | `concrete-patios-south-west-sydney` |
| 922 | Decorative Concrete | `decorative-concrete-south-west-sydney` |
| 1366 | Concrete Driveway Replacement | `concrete-driveway-replacement-south-west-sydney` |
| 1367 | Shed and Garage Slabs | `shed-and-garage-slabs-south-west-sydney` |
| 1368 | Concrete Crossovers and Laybacks | `concrete-crossovers-and-laybacks-south-west-sydney` |
| 1369 | Commercial Concreting | `commercial-concreting-south-west-sydney` |

Reconciliation: declared 10; immutable manifest 10; active allowlist 10; source WXR 10; legacy YAML service keys 10. Exact agreement: PASS.

## Existing technical-claim and figure audit

Reader-visible technical fields audited: 187. Classification totals: unsupported 187. Every record preserves the exact source string and placement in `build/53-service-specification-matrix.json` under `current_claim_audit`; the CSV repeats the exact strings against each applicable field without elision.

The existing numeric register contains 214 rows overall and 91 rows on these ten service pages. Service-row populations: council-sourced-pending-verification 60, template-artefact-unattested 31. All 91 remain unattested and unsupported as universal service specifications. The repeated values are 32 MPa, 125mm, SL72, 800mm, 900mm, 1200mm, 4.0-5.5m, 4%, 1:6, plus SL82 on the concrete-slabs page.

The Liverpool values validated in Report 52 remain valid only for Liverpool road-reserve crossings. Their existence does not verify the identical sentence copied across all ten services or extend it to Camden, Campbelltown, Wollondilly or private-property slabs.

## Matrix result

| Classification | Cells |
|---|---:|
| AUTHORITY-FIXED | 0 |
| DESIGN-SPECIFIC | 44 |
| COUNCIL-SPECIFIC | 9 |
| PRODUCT-SPECIFIC | 2 |
| SITE-SPECIFIC | 27 |
| PROVIDER-METHOD | 6 |
| NOT-APPLICABLE | 0 |
| UNRESOLVED | 2 |

Verified/resolved cells: 88/90. Project-specific cells (DESIGN-SPECIFIC + SITE-SPECIFIC): 71. Provider-specific cells: 6. Unresolved cells: 2. Services with one or more provider/project questions: 10. Services with all nine research cells resolved: 8. Services formally unblocked for Phase E: 0.

`verified: true` in Report 53 means the classification and safe conditional wording are supported by the cited authority. It does not mean a thickness, strength, mesh, method or warranty has been attested for Structure Co or any future provider.

## Source validation

Primary/authoritative source records used: 23; access-verified on 21 August 2026: 23. The CCAA residential PDF was downloaded, all 12 physical pages rendered and visually checked; SHA-256 `2212D0491FA912A400C42E5A1A2EBCE4D2DA31732255A113D452E13FB36C97E4`. Liverpool's 18-page March 2026 form remains hash-verified and was visually checked in Phase D. Relied-on curing pages in the current 45-page Transport for NSW specification were rendered and visually checked. The obsolete CCAA standalone curing URL returned a 404 HTML page, so it is not a source and the unsupported building-slab curing cells remain unresolved.

No competitor pages, SEO articles, AI summaries, forums, search snippets or reconstructed Australian Standard clauses are used as evidence.

## Council-to-suburb jurisdiction reconciliation

Active suburb pages mapped: 60. Split localities requiring lot-level checking: 8. Direct artifact contradictions: 2. The full cited row-level map is `build/53-council-suburb-map.json`.

The two direct contradictions are Camden Park and Theresa Park: the source artifact says Camden Council, while Wollondilly's official material places them within Wollondilly. Bringelly, Leppington, Rossmore, Edmondson Park, Kemps Creek, Cawdor, Cecil Park and Ingleburn are treated as split localities; the property lot must be checked in the NSW Planning Portal before naming the controlling council.

Liverpool's March 2026 vehicular-crossing specification is never applied outside Liverpool City Council. For a split suburb, the suburb name alone is not sufficient evidence of jurisdiction.

## Remaining questions

There are 14 cell-level questions that external research cannot answer. They concern provider curing methods, selected exposed/decorative systems, actual shed/garage drawings and actual commercial project requirements. They are listed without research-resolvable questions in `reports/53-unresolved-provider-inputs.md`.

## Validation results

| Check | Result | Detail |
|---|---|---|
| Immutable verification | PASS | 7/7 hashes match |
| Report 53 reproducibility | PASS | `python scripts/53-phase-a-evidence.py --check` |
| Specification-ledger/D23 state | PASS, fail-closed | Exact ten services; D23 rule present; legacy file 0 true/91 false and `populated:false` |
| Numeric-figure audit | PASS | 214 total register rows; 91 service rows; all mapped and unsupported as universal values |
| Citation registry | PASS with two unresolved cells | 23 opened primary/authoritative records; obsolete/404 item URLs excluded |
| Council/suburb reconciliation | PASS | 60/60 active suburb pages; 8 split; 2 artifact contradictions; every row cited |
| UTF-8 canary | PASS | all three exact assertions survived |
| Regression suite | PASS | 31 passed |
| CSV contract | PASS | exact 16 columns and 90 UTF-8 rows validated; spreadsheet `artifact-tool` dependency was unavailable in this environment, so repository-native CSV validation was used and disclosed |
| `git diff --check` | PASS | no whitespace errors in tracked diff; repository has no tracked baseline, so all files remain reported as untracked |

## Phase table after evidence acquisition

| Phase | Name | Status | Evidence |
|---|---|---|---|
| A | attest the figures | BLOCKED | legacy `service-specs.yml`: 91 false, 0 true, populated false; Report 53 research 88/90 resolved |
| B | media and staging | RUNNABLE | public media 55/55; Band A decisions complete; precondition script does not encode prior completion |
| C | identity and schema | BLOCKED | 11 verified true / 14 false; legal name, ABN, NSW licence and insurance remain unverified |
| D | Liverpool | RUNNABLE | 16 verified source records; Gate 19 separately confirms Phase D content complete |
| E | service page rebuild | BLOCKED | requires formal Phase A completion |
| F | images | BLOCKED | explicitly last; requires A-E |
| G | release | BLOCKED | requires preceding phases and preflight GO |

## Complete preflight table

Top-line verdict: **NO-GO**.

| Gate | Result | Detail |
|---:|---|---|
| 1. encoding canary | PASS | fixture and restored assertions survived |
| 2. 15 Stage 9 gates | PASS | 15/15 |
| 3. post-ID collisions | PASS | main 306; privacy 1; collisions 0; calculator absent |
| 4. media intake | PASS | public 55/55; immutable provenance 83 |
| 5. Astra Customizer | PASS | required groups, design carriage and consistency |
| 6. Elementor references | PASS | 1,085 image + 98 background = 1,183; 73/83 IDs; 0 unresolved |
| 7. uniqueness | **FAIL** | 1,761 five-grams on more than two pages; 1,491 within-class pairs over 40% |
| 8. intersections | PASS | 35 built/allow-listed; all draft |
| 9. menu lint | PASS | zero unsafe Wave 1 targets |
| 10. Victorian blocklist | PASS | zero in scoped public artifacts |
| 11. schema placeholders | PASS | zero JSON-LD blocks/tokens |
| 12. coherence | **FAIL** | 90 SEVERE; 139 above threshold; corpus filler 0.8244 |
| 13. source brand | PASS | 466 = 366 reader-visible + 100 preserved; transformed visible 0 |
| 14. assigned menus | PASS | zero unsafe; held 6; withdrawn 81 |
| 15. architecture/import parity | PASS | 76 allowed; 75 main + privacy; 81 withdrawn; calculator absent |
| 16. claims/evidence | PASS | 16 occurrences; 0 unsupported; 6 pages |
| 17. public media | PASS | 0 blocking; 0 Band A unrecorded; 0 Band B failures |
| 18. identity/Liverpool/schema | PASS | 0 unsupported claims; 12 Liverpool placements; 5 privacy blockers; 0 LocalBusiness |
| 19. Phase D Liverpool | PASS | 13 requirements; 12 fields; 4 pages; 0 false-fidelity; calculator absent |

Derivative WXR SHA-256: `4D28AE2E24F6A6EE9BD34B4AA60497F30F8E93A7538E45606BAC809D130B6D18`. The derivative was read only; it was not regenerated or changed by Phase A.

## Immutable hashes

| File | SHA-256 | Result |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | PASS |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | PASS |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | PASS |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | PASS |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | PASS |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | PASS |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | PASS |

## Scope confirmation

No WordPress import, deployment, publication, indexability change, Phase E rewrite, remote media operation, immutable edit or governing-document edit occurred. `data/service-specs.yml` was not modified.
