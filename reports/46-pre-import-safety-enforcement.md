# Pre-import safety enforcement

Date: 20 August 2026 (Australia/Sydney)

## Verdict

**NO-GO.** This pass implemented validation, reproducible transformation planning and import-safety
controls only. No WordPress content was imported. No site or container was started. Nothing was
deployed, published or made indexable. No content phase started. None of the seven immutable files,
the governing instructions or D1–D38 was edited.

The main preflight now has 17 executable gates. Gates 7, 12, 16 and 17 fail, so staging remains
prohibited. Index-ready remains 0 of 77.

The requested `RUN-BLOCK-02-on-inputs.md` does not exist in the repository. The actual governing
file is `RUN-BLOCK-02.md`; that file was read in its place and was not modified.

## Ground and dirty-tree guard

The Git repository has **zero tracked files**. At entry, `git status --short` reported 39 untracked
top-level paths covering the entire project. Git therefore provides no tracked baseline from which
to distinguish older user edits from pristine files. Every pre-existing file was treated as
user-owned. There were no identifiable tracked modifications to overwrite, and the implementation
was confined to the files listed below.

### Immutable hashes

| Immutable file | SHA-256 | Result |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | MATCH |

Verdict: **7 of 7 match; hard-stop condition did not occur.** Hashes were checked before work and
again through `scripts/37-preconditions.py` after implementation.

## Changed-file list

Because Git tracks nothing, this is the pass-local change record rather than a Git-derived diff.

### Implementation and tests

- `CONTEXT.md`
- `lib/preimport_safety.py`
- `scripts/21-encoding-canary.py`
- `scripts/28-gates.py`
- `scripts/28-preflight.sh`
- `scripts/46-architecture-import-gate.py`
- `scripts/46-claim-evidence-gate.py`
- `scripts/46-public-media-gate.py`
- `scripts/46-source-brand-gate.py`
- `staging-authoritative/scripts/verify-post-import.php`
- `staging-authoritative/scripts/verify-post-import.sh`
- `tests/test_utf8_gate.py`
- `tests/test_preimport_safety.py`
- `reports/46-pre-import-safety-enforcement.md`

### Generated machine controls and primary results

- `build/46-active-main-import.xml`
- `build/46-active-page-allowlist.json`
- `build/46-claim-register.json`
- `build/46-public-media-policy.json`
- `reports/46-architecture-import-gate.json`
- `reports/46-architecture-import-gate.out`
- `reports/46-claim-evidence-gate.json`
- `reports/46-claim-evidence-gate.out`
- `reports/46-claim-register.csv`
- `reports/46-public-media-gate.json`
- `reports/46-public-media-gate.out`
- `reports/46-source-brand-gate.json`
- `reports/46-source-brand-gate.out`

### Existing audit outputs refreshed by required verification runs

- `reports/22-astra-audit-result.md`
- `reports/22-media-audit-result.md`
- `reports/22-media-missing-manifest.csv`
- `reports/28-gates.err`
- `reports/28-gates.json`
- `reports/28-preflight.md`
- `reports/34-coherence.csv`
- `reports/34-coherence.out`
- `reports/34-coherence-summary.json`

## Controls implemented

### 1. UTF-8 Gate 1

The canary now configures its own stdout/stderr as UTF-8 and uses explicit strict UTF-8 for every
file read and write. It does not depend on `PYTHONUTF8` or `PYTHONIOENCODING` crossing the WSL to
Windows-process boundary. No assertion was removed or changed:

1. the fixture must survive an exact UTF-8 read/write/compare cycle;
2. `## 4.25 — Stage 25: uniqueness enforcement` must exist exactly; and
3. `PASS — 157 combined (156 main + 1 planned supplementary)` must exist exactly.

The regression suite runs the canary with both variables absent and with the deliberately hostile
pair `PYTHONUTF8=0` / `PYTHONIOENCODING=ascii`. Windows standalone, native WSL standalone and Gate 1
inside the full WSL preflight all return PASS. The generated preflight report also strict-decodes as
UTF-8.

### 2. Active architecture/import parity

`scripts/46-architecture-import-gate.py` derives the inventory from the immutable WXR and manifest,
`reports/23-page-readiness-v2.csv`, the privacy WXR and D16/D21/D22/D31/D35. It fails closed on:

- immutable input drift;
- missing or additional page IDs;
- duplicate IDs, slugs or URLs;
- WXR/manifest/readiness slug, URL, type or status mismatch;
- a missing or malformed privacy page;
- any ID collision between the main and privacy WXRs;
- any withdrawn page in the derivative;
- the calculator appearing before its control is reviewed; or
- stale/missing generated control files under `--check`.

The machine allowlist records page ID, slug, URL, page type, intended WXR status, import artifact,
index-readiness/blocker state and authority for all 76 built permitted pages. `publish` remains a
source status only, not launch approval.

The immutable source is not edited. The reproducible derivative is
`build/46-active-main-import.xml`, SHA-256
`177528119D01E1AC1282C24DB9138B126143913E8B9BA09C2503DF4319A34DCF`. It contains exactly 75
active main-WXR pages and zero withdrawn pages. Privacy remains a separate one-page WXR. The
calculator is absent.

### Inventory reconciliation

| Scope | Home | Utility | Service | Suburb | Guide hub | Guide | Intersection | Cost/comparison | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Immutable main WXR | 1 | 4 | 10 | 60 | 1 | 35 | 35 | 10 | 156 |
| Active main pages | 1 | 4 | 10 | 60 | 0 | 0 | 0 | 0 | 75 |
| Withdrawn main pages | 0 | 0 | 0 | 0 | 1 | 35 | 35 | 10 | 81 |
| Separate built privacy | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| Unbuilt calculator | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |

Exact arithmetic:

```text
156 main = 75 active + 81 withdrawn
75 active main + 1 privacy = 76 built/import-permitted
76 built + 1 unbuilt calculator = 77 logical active architecture
156 main + 1 privacy + 1 calculator = 158 full logical rows
```

The legacy readiness CSV has 157 rows because it contains all 156 main pages plus the unbuilt
calculator, but omits the built privacy page. The “81 withdrawn” statement is correct for the 156
main-WXR pages. The discrepancy is the document's mixed physical/logical scope, not a different
withdrawal count.

### 3. Claim-to-evidence parity

`scripts/46-claim-evidence-gate.py` scans the exact reader-visible fields of the 75-page derivative
and privacy WXR, plus structural Elementor testimonial/review/rating/star widgets. Each occurrence
records page ID/slug/type/status, exact claim, matched text, placement/widget, evidence citation,
required disposition and whether it blocks staging/publication. It does not rewrite any claim.

Current result: **FAIL — 232 occurrences, 228 unsupported, 24 pages with unsupported claims.**
Unsupported occurrences split 102 on source-`publish` pages and 126 on draft pages. The affected
page set is 10 source-`publish` pages and 14 drafts. Every unsupported row blocks both staging and
publication; source status confers no approval.

| Category | Occurrences |
|---|---:|
| Award claim | 0 |
| Band B attachment-specific local-project card | 4 |
| Completed-job count or recent-work claim | 1 |
| Contractor/operator claim (`we pour/build/handle` and equivalents) | 6 |
| Experience/years-in-business claim | 0 |
| False `verified project record says` field | 42 |
| Fixed-price/on-site quote promise | 30 |
| Licence/insurance/accreditation claim | 16 |
| Local operation or premises claim | 2 |
| `REAL_PHOTO_PENDING` local-project field | 44 |
| `researched ... job record contains` construction | 15 |
| Response-time promise/context | 1 |
| Review/rating/testimonial text | 48 |
| Structural review/rating/testimonial widget | 3 |
| Service-area claim | 18 |
| `trusted by`/social-proof claim | 0 |
| Workmanship guarantee/warranty claim/context | 2 |
| **Total** | **232** |

The required fixed subsets reconcile exactly: 42 false verified-project fields, 15 researched-job
constructions and four Band B local-project cards. Four matches are classified as supported
non-marketing contexts: two negated review references on About and the privacy policy's legal
warranty-retention/response wording. They do not attest a business claim. The complete rows are in
`build/46-claim-register.json` and `reports/46-claim-register.csv`.

The register also carries an executable schema policy derived from verified facts. Current outcome:
no `Organization`, `LocalBusiness`/`GeneralContractor` or `Service.provider` is permitted.

### 4. Source-brand enforcement

Gate 13 now asserts the derived transformation result. It reproduces the complete immutable-WXR
classification:

```text
466 CoreX occurrences = 366 reader-visible rename targets
                       + 100 attachment filename/URL/slug references to preserve
```

Of the 366 reader-visible targets, 183 are renamed in the active derivative and 183 disappear with
withdrawn pages. The active derivative has zero reader-visible CoreX occurrences. Its 96 remaining
CoreX strings are classified filename/URL/slug references; the reduction from 100 is caused by four
references on withdrawn pages. Required `corex-` attachment paths remain intact. The Elementor kit
has the exact 30-byte `Structure Co Concreters Camden` site name and an empty unsupported tagline.

### 5. Public-media enforcement

The Stage 22 binary/integrity audit and public suitability are now separate assertions. The former
passes 81/81; it is not publication approval. The public gate currently fails 40 assertions:

| Public-media assertion group | Failures |
|---|---:|
| Denied brand/AI/Band B UNUSABLE assets still in public intake and/or derivative | 12 |
| Band A pixel verdict unrecorded | 16 |
| Known false-geographic filename/alt remediation pending | 3 |
| Band B filesystem verdict absent from derived WXR filename/alt/slot state | 9 |
| **Total** | **40** |

Denied IDs are 159, 177, 272, 280, 306, 307, 308, 309, 422, 469, 472 and 1067. This union covers
the seven retired E&T marks, known unauthorised AI material, testimonial thumbnail 280 and VERIFIED
badge 1067. The two Band B UNUSABLE binaries are absent from the 81-file directory, but their WXR
records/slots still exist, so the gate correctly fails them.

All seven Band B GENERIC files exist under their subject-only filenames, but the immutable-derived
payload still contains the old filenames/alts. The gate now rejects that partial state. A future
authorised derivative transformation must update every WXR attachment/Elementor reference and
remove the UNUSABLE slots before Gate 17 can pass.

The gate never infers a Band A verdict. A future `GENERIC` decision must have a recorded RENAME row
with target filename and visible-only alt text, present both in the public directory and derivative.
A future `REPLACE`/`UNUSABLE` decision must be absent from both. No replacement is fetched.

Duplicate-ID contracts pass: attachments 49/52 remain separate despite byte identity; 468/471 also
retain both identities, and any later authorised retirement must remove both together rather than
collapse one Elementor reference target.

The six former ` (1)` delivery collision-renames are confirmed present and there are zero ` (1)`
files remaining:

| Attachment | Current public-intake filename |
|---:|---|
| 226 | `concretejob2camden-226.jpg` |
| 227 | `backyard-patio-concreter-camden-227.jpg` |
| 228 | `fresh-concrete-side-yard-slab-228.jpg` |
| 468 | `corex-concreters-camden-logo-468.png` |
| 471 | `corex-concreters-camden-logo-471.png` |
| 609 | `exposed-aggregate-south-west-sydney-609.jpg` |

### 6. Post-import database/rendered verification

`staging-authoritative/scripts/verify-post-import.php` is a fail-closed, read-only WP-CLI verifier;
the shell wrapper is explicitly for a later authorised staging import. It inspects the resulting
WordPress database and Elementor-rendered output, not planning prose, for:

- exact allowlisted page IDs, slugs and statuses across every database page status;
- all withdrawn pages absent, privacy present and calculator absent;
- Astra `wp_css` excluded and Werribee absent from custom CSS/theme mods;
- exact menu location assignment, retained item IDs/targets/order and deliberate non-assignment;
- retired/AI/UNUSABLE attachment records, URLs and upload binaries absent;
- GENERIC filenames/alts and Elementor URLs remediated;
- unusable/retired Elementor slots absent and every media reference resolving locally;
- reader-visible CoreX, E&T and unsupported tagline absent;
- every registered unsupported claim absent;
- JSON-LD valid with no undefined `@id`, and identity/provider nodes following verified facts;
- permalink and canonical paths equal the allowlist; and
- per-page noindex, global staging noindex and sitemap-disabled state matching the current approved
  wave (which remains empty).

This verifier was **not executed**. Doing so requires a future explicitly authorised import and a
WordPress database/rendered staging environment. No host PHP interpreter is installed, so this pass
performed static/read-only-contract regression only; runtime verification remains intentionally
pending.

## Phase preconditions

Output of `scripts/37-preconditions.py` after implementation:

| Phase | Name | Status | Evidence |
|---|---|---|---|
| A | Attest the figures | BLOCKED | 91 fields `verified:false`, 0 true; populated flag false |
| B | Media and staging | RUNNABLE | Technical preconditions only: media 81/81, Astra present, driver present, ImageMagick in WSL |
| C | Identity and schema | BLOCKED | 1 of 20 verified; legal name, ABN, licence, insurance, staffed address and phone unresolved |
| D | Liverpool | BLOCKED | `data/council-specs.yml` absent |
| E | Service page rebuild | BLOCKED | Requires Phase A/service matrix |
| F | Images | BLOCKED | Deliberately last; requires A–E |
| G | Release | BLOCKED | Requires preceding phases and preflight GO |

`RUNNABLE` is a phase-precondition state, not permission to import or a public-media pass. Phase B
remains incomplete at the human Band A sighting and Gate 17.

## Preflight table

| # | Gate | Result | Key result |
|---:|---|---|---|
| 1 | Encoding canary | PASS | Fixture and both exact restored assertions survive |
| 2 | 15 Stage 9 gates | PASS | 15/15 |
| 3 | Post-ID collision, present WXRs | PASS | Main 306 occupied IDs; privacy 1; collisions 0; calculator correctly absent |
| 4 | Technical media intake | PASS | 81/81; immutable provenance baseline 83 |
| 5 | Astra Customizer | PASS | Parse, required groups, carriage and consistency pass |
| 6 | Elementor image references | PASS | 1,085 foreground + 98 backgrounds; unresolved 0 |
| 7 | Uniqueness | **FAIL** | 1,761 repeated 5-grams; 1,491 within-class pairs over 40% |
| 8 | Intersection audit | PASS | 35 built/35 allowlisted; all draft |
| 9 | Menu lint | PASS | 27 retained items; no unsafe targets |
| 10 | Victorian blocklist | PASS | Zero across main/privacy/Astra import payload; calculator absent |
| 11 | Placeholder in schema | PASS | Zero JSON-LD placeholder blocks |
| 12 | Coherence | **FAIL** | 90 SEVERE; 139 over threshold; corpus filler 0.8244 |
| 13 | Source-brand transformation | PASS | 466=366+100; transformed reader-visible CoreX 0 |
| 14 | Assigned-menu safety | PASS | Zero unsafe retained targets in all three locations |
| 15 | Active architecture/import parity | PASS | 75 main + privacy; 81 withdrawn excluded; calculator absent |
| 16 | Claim-to-evidence parity | **FAIL** | 232 occurrences; 228 unsupported; 24 pages |
| 17 | Public-media suitability | **FAIL** | 40 assertions; Band A unresolved 16; Band B derivative failures 9 |
|  | **Overall** | **NO-GO** | Any failure prohibits staging/import |

## Verification commands and results

| Command | Result |
|---|---|
| `python scripts/21-encoding-canary.py` | PASS, all three exact lines |
| `wsl.exe env -u PYTHONUTF8 -u PYTHONIOENCODING python3 .../scripts/21-encoding-canary.py` | PASS, same three exact lines |
| `python -m pytest tests/test_utf8_gate.py tests/test_preimport_safety.py -q` | PASS, 7 tests |
| `python scripts/37-preconditions.py` | Completed; A/C–G BLOCKED, B RUNNABLE |
| `bash scripts/28-preflight.sh` | Expected non-zero; NO-GO on Gates 7, 12, 16, 17 |
| Strict UTF-8 read of `reports/28-preflight.md` | PASS |
| `python scripts/22-media-audit.py` | PASS, 81/81 |
| `python scripts/22-astra-audit.py` | PASS |
| `python scripts/27-menu-lint.py` | PASS, 27 items |
| `python scripts/46-architecture-import-gate.py --check` | PASS; generated controls current |
| `python scripts/46-source-brand-gate.py` | PASS |
| `python scripts/46-claim-evidence-gate.py` | Expected non-zero; 228 unsupported claims |
| `python scripts/46-public-media-gate.py` | Expected non-zero; 40 public-media failures |
| Python bytecode compilation and `bash -n scripts/28-preflight.sh` | PASS |
| `git diff --check` | PASS, with the limitation that Git tracks zero files |
| Strict UTF-8/trailing-whitespace scan of pass-local text files | PASS |

## Remaining blockers

1. **Owner:** provide the 10×9 service specification matrix. Phase A/E and the ten service-page
   rebuilds remain blocked.
2. **Owner:** establish the accountable legal entity/ABN, operator/referral model, NSW licence and
   insurance evidence where claimed, staffed-address status, phone ownership/routing and actual
   `service_areas` from where work will be performed.
3. **Owner:** record all 16 Band A pixel verdicts. No verdict was inferred in this pass.
4. **Agent after recorded authority:** produce a media-safe derivative that enforces the nine Band B
   WXR changes, removes all denied/unauthorised assets and slots, and applies recorded Band A
   decisions without breaking duplicate attachment identities or Elementor references.
5. **Owner/research:** provide the dated Liverpool Council crossing specification and source URL.
6. **Content/evidence:** disposition all 228 unsupported active-page claim occurrences and all 214
   unattested numeric figures across 29 pages. This pass deliberately rewrote none.
7. **Content:** rebuild the ten services and any pages admitted to Wave 1; current uniqueness and
   coherence gates remain build-failing.
8. **Privacy:** resolve all 11 blocking markers and name the accountable entity before publication.
9. **Architecture decisions:** `/gallery/` disposition remains undecided; the 45 unresearched suburbs
   remain deferred under D22, not dropped; the calculator remains unbuilt/excluded.
10. **Future authorised staging only:** import using the filtered derivative and separate privacy WXR,
    exclude `wp_css`, prune/assign menus, then run the database/rendered verifier. That authorisation
    was not given in this pass.

## Explicit non-actions

- No WordPress import or database mutation.
- No container or staging site started.
- No deployment or remote write.
- No publication, status promotion, robots/indexability or sitemap change.
- No content phase started and no reader-visible claim rewritten.
- No remote media fetch and no unrecorded Band A verdict applied.
- No immutable, governing-instruction or decision-document edit.

