# Project Context — Concreters Camden

Last updated: 21 August 2026 (Australia/Sydney)

## Overall goal

Build and safely launch an evidence-backed WordPress website for a concreting business serving Camden and South West Sydney, NSW, at `https://concreterscamden.com.au`.

The site is being transformed from a Melbourne WordPress/Elementor export while preserving the approved Astra/Elementor design structure. All Melbourne references, unsupported claims, and source-business details must be removed or replaced. The finished site should:

- generate qualified local concreting enquiries;
- target service and suburb searches without becoming doorway-page spam;
- use accurate Australian English and verified local, business, pricing, review, and project evidence;
- remain technically sound across WordPress, Elementor, Rank Math, forms, media, menus, schema, mobile performance, and accessibility; and
- launch in controlled publication waves rather than publishing all pages at once.

No business fact, price, licence, ABN, review, completed job, photograph, council requirement, or performance claim may be invented to make a page appear complete.

## Current stage

**THE BUILD IS PAUSED. Phase A evidence acquisition has 88/90 research cells resolved but is not
complete: two building-slab curing cells and the governing D23 owner/engineer attestation remain
unresolved. Phase D is complete for its authorised four-page Liverpool content scope. Phase B
remains runnable, but no staging build or import was started. Nothing is imported, deployed, live
or index-ready. Full preflight is NO-GO on uniqueness and coherence.**

The governing current handover is `HANDOVER-2026-08-19.md`. Older dated sections below are retained
as history; the 21 August delta immediately below supersedes their then-current identity, claim,
Liverpool, privacy, derivative-hash and preflight counts.

### 21 August 2026 — Phase A service-specification evidence acquisition incomplete

Full evidence and validation record: `reports/53-phase-a-evidence-acquisition.md`. Machine-readable
matrix: `build/53-service-specification-matrix.json`; 90-row CSV:
`reports/53-service-specification-matrix.csv`; cited council map:
`build/53-council-suburb-map.json`; unresolved questions:
`reports/53-unresolved-provider-inputs.md`.

The immutable manifest, active allowlist, ledger, source WXR and legacy service-spec keys agree on
exactly ten active services. All 214 existing figure-register rows were audited, including the 91
rows on the service pages. Those 91 service figures remain unsupported as universal specifications;
Liverpool's verified crossing figures apply only to Liverpool road-reserve work.

```text
  matrix cells                    90
  evidence-resolved               88
  design/site-specific            71
  provider-method                  6
  unresolved                       2 — curing for concrete slabs and shed/garage slabs
  research-complete services       8
  services formally unblocked      0
  current technical claim fields 187 — all unsupported in the existing service copy
  service figure-register rows    91 / 214 total
  council map                     60 pages; 8 split localities; 2 artifact contradictions
  derivative SHA-256              4D28AE2E24F6A6EE9BD34B4AA60497F30F8E93A7538E45606BAC809D130B6D18
  regression tests                31/31 PASS
  immutable hashes                 7/7 MATCH
  preflight                       NO-GO — only Gates 7 and 12 fail
```

The two direct jurisdiction contradictions are Camden Park and Theresa Park: the source suburb
artifact says Camden Council, while authoritative Wollondilly material places them in Wollondilly.
Bringelly, Leppington, Rossmore, Edmondson Park, Kemps Creek, Cawdor, Cecil Park and Ingleburn are
treated as split localities requiring lot-level NSW Planning Portal checking before naming a
controlling council. Fairfield and Penrith are therefore also relevant for those boundary cases.

Phase A is not marked complete. `data/service-specs.yml` was not modified: D23 reserves it for
owner/qualified-engineer attestation, it remains 0 verified true/91 false and `populated:false`, and
its ten service-specific blocks retain a pre-existing YAML syntax defect. The obsolete direct CCAA
curing PDF URL returned a 404 and was not used as evidence; the two unsupported curing cells remain
explicitly `UNRESOLVED`. Phase E was not started.

No import, deployment, publication, indexability change, Phase E rewrite, immutable edit or
governing/decision edit occurred.

### 21 August 2026 — Phase D Liverpool Council content complete

Full implementation and evidence record: `reports/52-phase-d-liverpool-completion.md`.

The current March 2026 Liverpool vehicular-crossing form was revalidated page by page against its
official downloaded PDF (18 pages; SHA-256
`43F74C0F01C5EA6F0C89919BE8C1859F758F96AF549A9CF71ADA5F87DD7CAF33`). All 13 Council
requirements pass. The utilities citation was corrected from page 6 to pages 6–7 because the
stormwater/pram-ramp controls continue on page 7.

The reproducible derivative now applies 12/12 evidence fields across IDs 221, 1163, 1387 and 1388.
It preserves site-specific assessment, current-form/current-fee checks, inspection and approval
before pouring, the property owner's contractor-licence/$10 million liability responsibility, and
the explicit statement that these are not Structure Co credentials. No precinct DCP control,
universal dimension, fee amount, approval time or permit outcome was introduced. Affected-page
false-fidelity residue is zero. The calculator remains absent and unbuilt.

```text
  official requirements          13/13 PASS
  affected pages                   4/4 PASS
  resolved fields                12/12 PASS
  Phase D false-fidelity             0
  derivative SHA-256              4D28AE2E24F6A6EE9BD34B4AA60497F30F8E93A7538E45606BAC809D130B6D18
  claim parity                    16 supported / 0 unsupported
  regression tests               24/24 PASS
  immutable hashes                7/7 MATCH
  preflight                       NO-GO — only Gates 7 and 12 fail
```

`scripts/52-phase-d-liverpool.py` is the fail-closed content/citation control and full preflight now
includes it as Gate 19. `scripts/37-preconditions.py` continues to show Phase D as `RUNNABLE`
because that table reports input readiness rather than execution history; Gate 19 and Report 52
record completion.

Eleven `reproduced without alteration` occurrences remain outside Phase D in blocked home/service
content and continue to be caught by the unchanged coherence controls. They were not rewritten
because no other content phase was authorised.

No import, deployment, publication, indexability change, immutable edit or governing/decision edit
occurred.

### 21 August 2026 — owner identity, claims and Liverpool evidence applied

Full implementation and evidence record: `reports/51-identity-claims-liverpool-remediation.md`.

Verified public facts now recorded in `data/verified-facts.yml` are the Structure Co Concreters
Camden public label, monitored email, `(03) 4328 3392` / `tel:+61343283392`, the staffed
administrative correspondence office at 15 Murray Street, and the enquiry-management/independent-
provider operating model. The office is not open to customers or visitors. The telephone is not
described as a local Camden/Sydney number. No ABN, legal entity, specific NSW contractor, licence
or insurance is asserted.

```text
  original claim register         232 occurrences / 228 unsupported
  Report 50/D32 removals           97
  removed without replacement      99
  neutralised                       24
  official Liverpool replacements  12
  additional blind spots closed   309
  final reader-visible claims      16 supported / 0 unsupported

  derivative SHA-256              9FA49392B181EE839954A0FB9F306B6E4EB7CA4891ED921CF14079EE8AE4CB82
  privacy derivative SHA-256      80AB5AF8C125E1A6C79E8CA2D976B8002FDE15686CFF9C6F627EF53B9C234E7B
  privacy blockers                 5
  schema                            76 graphs; 70 Service; no Organization,
                                    LocalBusiness, provider or rating
  Liverpool evidence              13 current-form facts; 12 fields on 4 pages
  form placements                  4/4 carry the adjacent no-contract disclosure
  regression tests                11 PASS
  immutable hashes                7/7 MATCH
  preflight                       NO-GO — only Gates 7 and 12 fail
```

The official Liverpool forms page, March 2026 vehicular-crossing form and online portal were
sighted on 21 August 2026 and recorded in `data/council-specs.yml`. Applied facts are limited to
section 138, owner cost responsibility, contractor licence/$10 million liability requirement,
plain concrete, 25/32 MPa strengths, 50/100 mm DGS20 bedding, pre-pour approval, drawing R25/site
directions, utility clearances, application/inspection process and current-schedule fees without
an invented dollar amount. These Council requirements are not treated as Structure Co credentials.

The privacy page now uses the attested public contact and operating facts but remains blocked on:
accountable legal entity; form delivery/storage/access controls; retention period; analytics state;
and publication date. No ABN marker remains. Phase C remains blocked under the existing precondition
on legal name, ABN, NSW licence and public liability. Phase A remains blocked on the empty 10-service
matrix (91 false, 0 true), so the service rebuild remains blocked. Phase D is now RUNNABLE but was not
started.

No import, deployment, publication, indexability change, immutable edit or governing/decision edit
occurred.

### 20 August 2026 — owner-approved final image remediation

The exact Report 49 zero-new-photograph plan is now implemented and verified. Full record:
`reports/50-final-image-remediation.md`.

```text
  Band A verdicts             16/16 explicit = 10 GENERIC + 6 UNUSABLE
  Band A HOLD                 0
  Band B                      9/9 PASS = 7 GENERIC + 2 UNUSABLE
  media manifest              83 = 55 RENAME + 28 EXCLUDE + 0 HOLD
  public media                PASS — 55/55; excluded quarantine 28/28
  Report 49 removals          164/164 exact; no additional Report 49 slot removed
  Band A generic placements  75/75 exact page/widget/setting contract
  final Elementor refs        440 primary = 440 independent; unresolved 0
  derivative SHA-256          C1E325576AACB12EB60E6FE5696CA852A6FB60D3FDC95450F3DB947201E406D9
  regression tests            19 PASS
  Phase B precondition        RUNNABLE — media/payload controls pass; staging not started
  preflight                   NO-GO — non-image Gates 7, 12 and 16 fail
```

The recursive Elementor blind spot is fixed. Both independent detectors now find homepage
attachment 609 in nested Elementor 4.2 `e-image` widget `306c538`; production logic contains no
attachment-specific exception. Report 49's starting populated count is correctly 410, not 409.
The final count is 440 because the approved plan removes 45 blank-placeholder placements and
restores 75 exact Band A GENERIC decorative placements: `410 - 45 + 75 = 440`. The future
post-import database verifier now understands the same typed-image representation.

The owner approval source is recorded verbatim on all 16 Band A worksheet rows. Generic filenames,
attachment metadata and classic Elementor alt/URL fields are subject-only. The public-media gate
requires all 75 Band A GENERIC occurrences to match Report 49's exact placement map and rejects
arbitrary reuse. The six Band A UNUSABLE assets and six blank-placeholder binaries are quarantined;
all authorised slots are absent. No mandatory new owner photograph remains.

`/gallery/` (ID 1365) is explicitly deferred until a genuine, permission-backed project library
exists and is excluded from every launch menu assignment. It was not deleted and its indexability
was not changed.

No WordPress import, staging/live database execution, deployment, publication, remote media fetch,
generated image, indexability change, immutable-file edit or governing-document edit occurred.
The image-payload work is closed, but the site remains 0 index-ready and NO-GO because identity,
operator, claims, coherence, uniqueness, service-specification/copy, privacy and staging work remain.

### 20 August 2026 — image completion requirements audit

The complete 76-built-page image-slot audit is recorded in
`reports/49-image-completion-requirements.md` and the exact 612-row machine inventory is
`reports/49-image-completion-requirements.csv`. The CSV reconciles 610 Elementor image-capable
page slots plus the two global brand roles. Withdrawn pages are excluded.

Verified image requirement state:

```text
  active source slots          610 = 607 populated + 3 empty testimonial portraits
  derivative slots             413 = 410 populated + 3 empty testimonial portraits
  useful existing assets        45 unique / 365 populated derivative placements
  blank placeholder assets       6 unique / 49 active-source placements
                                      (45 still present in the derivative)
  eventual slot removals        164 = 45 D32 + 21 other prohibited + 3 testimonial
                                      + 45 blank-placeholder + 50 recommended Band A UNUSABLE
  supplied brand assets           2 required roles; no new owner file required
  Band B                          9/9 PASS
  Band A                          0/16 owner verdicts; 16 HOLD
  Band A audit recommendation    10 GENERIC + 6 UNUSABLE; recommendations are not verdicts
  new owner photographs           0 for the present minimum, conditional holding set, or all 76
```

The current honest live set remains zero pages because identity/operator evidence is absent. If
those non-image blockers clear, the smallest publisher/holding set is `/` (`homepage`), `/about/`,
`/contact/` and `/privacy-policy/`. It needs zero new photographs: seven existing generic images,
the two already supplied Structure Co brand files, and removal of the three unsupported homepage
testimonial widgets are sufficient in image terms. Across all 76 built pages, no authentic project,
customer, team, premises, vehicle or equipment photograph is structurally mandatory because D32
removes evidential project modules and optional evidential slots are to be removed. This is not
permission to make contractor/local-work claims.

No Band A image has documentary Camden or NSW provenance; visual plausibility is not provenance and
a renamed filename proves nothing. The audit recommends generic subject-only treatment for tiles
2–7, 9–10 and 15–16, and removal without replacement for tiles 1, 8 and 11–14. The owner worksheet
remains unchanged and blank. `/gallery/` should be deferred or removed from launch/navigation; it
cannot honestly launch as a completed-project gallery without a separately scoped authentic project
library and evidence packet.

The recursive placement inspection found one enforcement gap: the current architecture/media walker
reports 409 derivative references but misses homepage attachment 609 in nested Elementor 4.2
`e-image` widget `306c538`. The true populated derivative count is 410, all currently resolving.
This audit did not change the gate; strengthening it requires a separately authorised implementation
pass. It also visually confirmed that attachments 275–279 and 323 are literal placeholder graphics,
not photographs, even though the existing manifest permits them as generic decoration.

Seven immutable hashes remain MATCH and the derivative remains
`4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B`.
Full preflight remains NO-GO: Gates 7, 12, 16 and 17 fail; Gate 17 is exactly the 16 unrecorded
Band A verdicts with zero Band B failures. The requested `RUN-BLOCK-02-on-inputs.md` does not exist;
the repository's governing run block is `RUN-BLOCK-02.md`.

No import, deployment, publication, media mutation, remote fetch, generated image, indexability
change, derivative-WXR edit, immutable edit or governing-document edit occurred.

### 20 August 2026 — Band A final-closure input verification

The requested final Phase B media closure could not proceed because the stated completed owner
input is not present in the authoritative artifact. `reports/44-sighting-worksheet.csv` contains
exactly 16 Band A rows, but **0 explicit verdicts and 16 blank `VERDICT`/`NOTE` pairs**. Its SHA-256 is
`6C7826FF7AA7184A23674C709FE03DF85D84FE43E0011E1AAAF8245E0D5C11B4`.

No verdict was inferred. No OK asset was accepted without provenance, no GENERIC/REPLACE/UNUSABLE
action was invented, and no transformer source or media binary was changed. Full preflight
regenerated the derivative and manifest reproducibly from the unchanged fail-closed inputs; both
retained their prior hashes and 16-HOLD state. All 16 assets remain held outside the public intake
and derivative. Full record:
`reports/48-phase-b-final-closure.md`.

Verified state remains:

```text
  immutable files          7/7 MATCH
  derivative SHA-256       4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B
  media manifest           83 = 51 RENAME + 16 EXCLUDE + 16 HOLD
  Elementor references     409 surviving; unresolved 0
  Band B                   9/9 PASS
  Band A                   0 explicit; 16 blank; public-media gate FAIL
  regression tests         18 PASS
  preflight                NO-GO — Gates 7, 12, 16 and 17 fail
```

Phase B remains **BLOCKED**, index-ready remains **0 of 77**, and launch remains **NO-GO**. The next
safe action is for the owner to save all 16 explicit Band A verdicts and required notes into the CSV;
only then may the reproducible media transformation be regenerated. No import is authorised.

```text
  architecture        77 pages
  index-ready         0
  launch gate         NO-GO
  public media set    51 files (83 provenance records; 16 excluded; 16 Band A held)
  Phase B             PARTIAL — Band B and all recorded non-Band-A dispositions enforced;
                                 all 16 Band A owner verdicts remain blank and fail-closed
  critical path       identity/operator evidence; readiness/import/preflight repair;
                      Band A sighting; service specification matrix
```

### 20 August 2026 — Phase B media-payload enforcement

No WordPress import, staging/site execution, deployment, publication or indexability change occurred.
The immutable WXR and all seven immutable files remain hash-identical. Full record:
`reports/47-phase-b-media-payload-closure.md`.

The generated derivative now enforces the media decisions before import:

```text
  derivative                 build/46-active-main-import.xml
  derivative SHA-256         4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B
  media manifest             83 = 51 RENAME + 16 EXCLUDE + 16 HOLD
  public media audit         PASS — 51/51, zero missing/extras/non-images
  D32                        17 sections on 16 pages removed; 47 markers removed
  Elementor references       409; all resolve to 51 permitted attachment records
  Band B                     9/9 PASS in derivative; 7 GENERIC + 2 UNUSABLE
  unusable slots             28/28 absent (14 active slots removed; 14 on withdrawn pages)
  public-media gate          FAIL only on 16 blank Band A verdicts; Band B failures 0
  claim/evidence gate        FAIL — 144 occurrences, 140 unsupported, 16 unsupported pages
  regression tests           PASS — 18
  preflight                  NO-GO — Gates 7, 12, 16 and 17 fail
```

The original 40 public-media failures reconcile as 12 denied-asset assertions, 16 missing Band A
verdicts, three false-geography remediations and nine unapplied Band B dispositions. Thirty-four
were cleared; the remaining 16 are exactly the blank Band A verdicts. Their binaries are held in
`source-inputs/media-held-band-a/` and are absent from the public directory and derivative. This is
not a verdict: the gate continues to fail until the owner records one.

All Stage 8 naming-convention geography was reversed for permitted decorative assets under D24/D20.
The D18 assets 1056, 1151 and 1188 now have subject-only filenames/titles/alts; attachment 1020 is
removed under D19. Seven recorded E&T brand attachments, unauthorised AI material, the two Band B
UNUSABLE assets, the Astra logo (250), and E&T duplicate pair 468/471 are excluded. Pair 468/471 was
treated together; pair 49/52 remains two attachment identities and two filenames. Supplied Structure
Co logo/favicon files remain separate inputs for the eventual authorised import; post-import checks
now require the header and site-icon slots to resolve to those exact files.

The former post-import Band B mutator is retired fail-closed. The active derivative excludes the
`wp_css`/custom-CSS record, all prohibited/held attachment records and every stale media reference.
The local importer and re-encode driver now consume the 83-row Phase B manifest rather than the
superseded nine-row Band B overlay.

**Remaining Phase B work:** the owner must record all 16 Band A verdicts. After that, regenerate,
re-run the same gates, and obtain explicit staging-import authority. Index-ready remains 0 of 77 and
launch remains NO-GO.

### 20 August 2026 — pre-import safety enforcement pass

No phase was started. No WordPress import, container/site execution, deployment, publication or
indexability change occurred. The seven immutable files remain hash-identical. Latest completed
stage and index-ready state are unchanged: **0 of 77; launch NO-GO**. Full implementation record:
`reports/46-pre-import-safety-enforcement.md`.

Implemented and verified:

```text
  UTF-8 canary              PASS in Windows and native WSL; 7 regression tests PASS
  active/import parity      PASS — 156 main = 75 allowed + 81 withdrawn
                                  + privacy 1 = 76 built allowed; calculator absent
  derived active WXR        build/46-active-main-import.xml
                             SHA-256 177528119D01E1AC1282C24DB9138B126143913E8B9BA09C2503DF4319A34DCF
  source-brand Gate 13      PASS — baseline 466 = 366 reader-visible + 100 path/file
                                  references; active derivative reader-visible remainder 0
  claim/evidence gate       FAIL — 232 occurrences, 228 unsupported, 24 pages
  public-media gate         FAIL — 40 blocking assertions
  preflight                 NO-GO — Gates 7, 12, 16 and 17 fail
```

The executable allowlist contains 76 built pages: 75 filtered main-WXR pages and the separate
privacy page. It rejects missing, additional, duplicate and mis-mapped IDs/slugs/URLs/types/statuses;
all 81 withdrawn pages are physically absent from the reproducible derivative. The apparent
“81 withdrawn” discrepancy is classification scope, not arithmetic: the immutable WXR has 156
pages (75 active + 81 withdrawn); privacy exists outside that WXR and the calculator is only an
unbuilt readiness row, producing 77 logical active pages but only 76 built/import-permitted pages.

The claim gate scans exact reader-visible fields and structural testimonial/rating widgets. Its
228 unsupported occurrences affect 24 pages (10 source-publish status, 14 draft); WXR status is
not launch approval and every occurrence blocks staging and publication. Exact mandatory subsets
remain 42 false `verified project record says` fields, 15 `researched ... job record contains`
fields and four attachment-specific local-project cards. The four non-blocking matches are
negated/non-marketing contexts on About and Privacy, not supported business claims.

The technical 81-file media audit still passes on its own terms, including the six former ` (1)`
collision-renames. Public suitability correctly remains failed. All 16 Band A verdicts are
unrecorded; 12 denied brand/AI/UNUSABLE attachment records or files remain in the derived/public
inputs; three known false-geographic filenames remain; and all nine Band B decisions are present
in the filesystem but absent from the derived WXR's filenames/alts/slot removals. This last point
supersedes the earlier directory-only statement that Band B was fully applied: the media files were
remediated, but the import payload was not.

Read-only post-import assertions are installed for a future explicitly authorised staging run.
They inspect the resulting WordPress database/Elementor output for exact page/menu inventory,
`wp_css` exclusion, denied media and slots, brand transformation, claims, identity-sensitive
schema, media resolution, canonical paths and the current all-noindex wave. They were deliberately
not executed because no staging import/site exists in this pass; local PHP is unavailable, so PHP
runtime validation remains part of that future staging run.

Remaining blockers were not cleared: owner identity/operator evidence, the service specification
matrix, Liverpool evidence, Band A sighting, derived Band B/media removals, 228 unsupported claims,
coherence/uniqueness failures, privacy markers and all downstream content/release work. The next
safe action is to record the 16 Band A owner verdicts and then build a media-safe derivative; no
import is authorised.

### 20 August 2026 — inspection pass, artifact state governs

No phase was started. Nothing was imported, deployed, published or indexed. The full inspection and
remaining-work inventory is `reports/45-remaining-work.md`.

Verified in this pass:

```text
  immutable hashes                 7 of 7 MATCH
  scripts/37-preconditions.py      A BLOCKED, B RUNNABLE, C-G BLOCKED
  standalone UTF-8 canary          PASS, all three exact assertions
  deterministic preflight          NO-GO
    failing                        1, 3, 7, 12, 13
    gate 1                         runner/environment defect: WSL export does not reach
                                   the Windows Python process; assertion is not relaxed
  media audit                      PASS — expected 81, present 81, OK 81, no gaps
  collision-renamed files          all six landed; zero ` (1)` remnants
  testimonial placements           110; fabricated customer quotes 0
```

The repository does **not** fully match `HANDOVER-2026-08-19.md`:

- The testimonial question has since been investigated. Attachment 228 is on 14 pages, not 15.
- The readiness CSV has 157 rows but omits the built privacy WXR. It therefore has 76
  non-withdrawn rows (75 main plus the unbuilt calculator), not the 77-page active architecture.
  Full logical scope is 158 rows: 156 main, privacy and calculator; 77 are active/non-withdrawn.
- `reports/29-staging-plan.md` is stale: it imports all 156 main-WXR pages, has no executable
  81-page withdrawal exclusion, omits the privacy import and retains superseded Astra/count text.
- The pixel worksheet has 9 decided Band B rows and 74 blank verdicts. Band C retirement is decided,
  but its pixel verdicts are not recorded; Band D can be deferred for the risk-bearing pass but has
  not been sighted.
- The current post-Band-B verification contract is 81 active attachments and 1,014 surviving
  foreground references plus 98 backgrounds, not the handover's 83/1,085 completion target.

The first systematic active-page marketing sweep found no star ratings, years-in-business claims,
numeric job counts, `trusted by` claims or awards. It did find:

```text
  unsupported Licensed & Insured headings       15 pages, 6 publish status
  fixed-price on-site quote headings             15 pages, 6 publish status
  written workmanship guarantee                   1 page,  publish status
  verified project record constructions          42 fields, 14 pages, 5 publish status
  researched job record constructions            15 fields, 15 pages, 6 publish status
  service-area headings                          15 pages, 6 publish status
```

D32 establishes that no Camden project exists. The 42 `verified project record says` fields are
therefore a larger false-fidelity population than the existing six-row textual register captured.
They are not testimonials, and no invented-testimonial category is created because that verified
count is zero. The exact strings and pages are preserved verbatim in the inspection report.

**Latest completed stage is unchanged. Index-ready remains 0 of 77 and launch remains NO-GO.**
No blocker was cleared by this inspection. The next safe action is owner resolution of the
accountable entity/operator model while the readiness, import and preflight contracts are repaired;
an authoritative import is not the next action.

### 20 August 2026 — testimonial investigation and Band B applied

The seven testimonial-labelled photographs (attachments 46, 47, 48, 49, 51, 52 and 228) were
traced through the immutable WXR at Elementor-widget level: **110 placements** in total. The only
three actual testimonial widgets in the WXR are homepage placeholders with empty image IDs.

```text
  fabricated customer quotes                         0
  customer name / quote / testimonial-job fields     0
  star-rating fields                                 0
  target images attached to testimonial widgets      0
  target local-work-card placements                  4
```

The four local-work occurrences are attachments 46 (Gregory Hills, publish), 48 and 49 (Edmondson
Park, draft), and 52 (Catherine Field, draft). Their exact adjacent copy is only the corresponding
`[[REAL_PHOTO_PENDING: verified CoreX project in <suburb>]]` marker. No testimonial attribution,
date or job description is present. Attachments 47, 51 and 228 never appear in a local-work card.
Attachment 228 corrects the supplied premise: **14 pages, not 15**, with 16 placements because two
pages use it twice. Full exact context: `reports/45-testimonial-text-investigation.md` and CSV.

No invented-testimonial category was added to the false-fidelity register because the verified
count is zero. Existing NT-1 remains: the unsupported VERIFIED badge is a separate non-textual
false-fidelity claim.

Band B is now complete:

```text
  GENERIC     7   filenames changed in source-inputs/media; subject-only alt mapped
  UNUSABLE    2   attachment 280 placeholder + 1067 VERIFIED badge
  public set 81   expected 81, present 81, OK 81, missing/extras/non-images 0
```

The seven photographs are decoration only: never customer evidence and never recent/local work.
Attachments 49 and 52 are byte-identical; both remain distinct attachment IDs. The two UNUSABLE
binaries were moved recoverably to `source-inputs/media-retired/`, so they cannot enter the public
uploads set. Their 28 WXR slots are removed after import without replacement; image-box text/links
survive with their image setting cleared. The post-import operation also executes the already-settled
D32 removal of the 15 suburb local-work modules before GENERIC remediation is verified.

Because the main WXR is immutable and no import is authorised, the per-page alt and slot mutations
are encoded but **not run** in `staging-authoritative/scripts/apply-band-b-remediation.php`. Expected
post-import counts are fail-closed: 15 D32 modules removed, 106 surviving GENERIC references
remediated, 4 GENERIC references removed with those modules, 28 UNUSABLE references removed, and
1,014 surviving Elementor image references. The main WXR and all seven immutable hashes remain
unchanged.

**Remaining Phase B action:** owner sights Band A (16 geographic claims). No staging import begins
without explicit approval. Index-ready remains 0 and launch remains NO-GO.

### 19 August 2026 — media binaries arrived; Phase B still blocked

The 83 image binaries were supplied as 190 files extracted from three cPanel zips of the E&T uploads
directory. **Audit only: nothing was re-encoded, renamed, imported or deployed.** Full record in
`reports/22-media-intake-reconciliation.md`.

```text
  required originals              83
  present, exact filename         77
  present, filename mismatched     6   ` (1)` collision-rename artifacts; corroborated against the
                                       source WXR's own declared dimensions and byte lengths
  genuinely absent                 0
  thumbnail-variant-only           0   but see below
```

- **Content-complete, not cleared.** The six mismatched files are the *only* copies of those binaries
  in the intake — in the WSL thumbnail store they exist solely as dimensioned variants. If they are
  swept as duplicates, six required originals are lost. They must not be cleaned up as extras.
- `scripts/22-media-audit.py` returns **FAIL (0 of 83)**. That is a name-space artifact: it asserts
  post-rename Camden filenames against a pre-rename E&T directory. It must be re-run after the rename
  step and **must pass on its own terms**; the reconciliation does not substitute for that pass.
- Attachments **468 and 471 are byte-identical**, and the source WXR declares both at 512×512 /
  302,716 bytes. The source site held one image under two IDs. The rename must write it out twice.
- **EXIF, read-only across all 83: zero GPS, zero camera make/model, zero owner/artist/serial.** The
  P0 concern about Melbourne job-site coordinates does not materialise in these binaries. Remaining:
  6 `DateTimeOriginal`, 1 Adobe `UserComment`, 11 `Software`. The driver is still required and still
  unrun; D25.2 must pass after re-encoding.
- **New:** two required binaries carry intact C2PA content credentials naming `gpt-image` v2.0 —
  `ChatGPT-Image-Jul-6-2026-01_52_19-PM.png` and `eandtcologo.png`, the E&T logo. First binary-level
  evidence for the AI-generated-image finding, which previously rested on filenames. Two of three
  confirmed by self-declared provenance; classification remains open.
- **Delivered but not wanted:** 2 personal résumé PDFs (must never enter the import), 2 screenshots,
  90 `- Copy` duplicates, and a **fourth WXR export dated 2026-08-18** which is in no hash table and
  **has not been read**. Whether it supersedes anything is an owner question.
- **Phase B remains BLOCKED at step 2** on the Astra Customizer export. `source-inputs/astra/` holds
  0 files. Steps 3–7 do not start.

**Gate defect recorded, not worked around.** `scripts/37-preconditions.py` probes for ImageMagick via
Windows `bash`, while the driver and EXIF assertion run in **WSL**, where ImageMagick 7.1.2-18 and
exiftool 13.50 are installed and verified. The gate would report `NOT INSTALLED` permanently. The
assertion was not relaxed and the script was not edited; the probe needs correcting under its own
approval. The Phase B verdict is unaffected — the Astra export blocks it either way.

### 19 August 2026 — DECISION-08: trading name, brand assets, partial NAP

Three owner inputs. **None of them clears a blocker.** Full plan in
`reports/38-trading-name-rename-plan.md`; decisions transcribed in
`DECISION-08-trading-name-brand-nap.md` (D35–D38).

**D35 — the trading name is "Structure Co Concreters Camden".** It supersedes both "CoreX
Concreters Camden" (the built copy) and "E&T Co Concreters Camden" (the source Melbourne business,
still declared in the Elementor kit `site_name`). Rename plan produced, **not executed**.

```text
  all name forms, all artifacts        6,177 occurrences across 94 files
  reaching a reader                      366
  provenance / audit trail, MUST NOT
    be renamed                         5,811

  main WXR, "CoreX"                      466   fully attributed, no remainder
    of which reader-visible              366   body copy 201, alt 24, rank_math 117,
                                               item titles 12, site title 2
    of which filenames/URLs/slugs        100   NOT renamed — renaming breaks 1,085
                                               Elementor image references
  pages with CoreX in rendered copy    73 of 156   (21 publish, 52 draft)
  pages with CoreX on any visible surface 111 of 156
```

**A recorded figure was wrong.** The ledger and D30 both quote **345** CoreX occurrences in the main
WXR. The actual count is **466**. 345 is not reproducible from any corpus in the repo. Corrected in
`build/21-spec-ledger.json` with the recomputation method recorded.

**D36 — brand assets supersede the inherited marks. ON DISK AND VERIFIED (updated 19 August,
later the same day).** Five SVGs in `source-inputs/brand/`. Claims tested rather than accepted:
text converted to outlines (zero `<text>`/`<tspan>`), no font dependency (zero `font-family`), icon
genuinely 512 square, all self-contained (no external refs, no embedded raster, no `<script>`).
Inventory and hashes: `reports/39-brand-assets-and-image-slots.md`.

```text
  structure-co-horizontal.svg           773x260   #1C244B #7C8494
  structure-co-horizontal-mono.svg      773x260   #000000
  structure-co-horizontal-reversed.svg  773x260   #1C244B #AEB6C6 #FFFFFF
  structure-co-stacked.svg              527x308   #1C244B #7C8494
  structure-co-icon.svg                 512x512   #1C244B #FFFFFF
```

Two deviations recorded: two filenames differ from those named in the brief
(`-horizontal-reversed` / `-horizontal-mono`, not `-reversed` / `-mono`), and the reversed lockup
carries a third colour **`#AEB6C6`** not in the stated palette — confirm it is intended before it
reaches a stylesheet.

~~One gap blocks the favicon.~~ **CLEARED later the same day.** Five favicon PNGs supplied and
verified — 512, 270, 192, 180 and 32, dimensions read from the file headers, all carrying the same
artwork (mean luminance 0.4498–0.4502), fully opaque, and metadata clean: zero GPS, owner, camera or
capture-time tags. **No SVG-upload plugin will be installed** — owner decision; a stored-XSS vector
is not worth one favicon.

Palette confirmed: navy `#1C244B`, grey `#7C8494`, and `#AEB6C6` as a **reversed-context tint only**
— `#7C8494` lifted for legibility on navy, not a third brand colour.

Still **not implemented**, but the blocking is now split. The **site icon proceeds independently of
the Astra export** (`Settings → General → Site Icon` is WordPress core, not an Astra theme mod) and
waits only on the import. The header, sticky, footer and mobile slots still wait on the Customizer
export.

> **Correction to D27.** D27 recorded attachments 306, 307 and 422 as unreferenced and directed
> that they be left that way. **306 and 307 are not unreferenced.** 306 is live on **8 pages**
> (`/contact/`, `/quote/`, `/about/`, `/gallery/`, `/concrete-patios-south-west-sydney/` — all
> publish — plus 3 draft patio pages); 307 is live on **2** (`/concrete-paths-south-west-sydney/`
> publish, `/concrete-paths-edmondson-park/` draft). Removing them leaves **10 empty image slots**
> needing a replacement decision.

**D37 — partial NAP recorded, unverified.** `info@concreterscamden.com.au` and
`15 Murray Street, Camden NSW 2570` are in `data/verified-facts.yml`. Address `verified: false`,
`is_staffed: unknown`, per the owner. The email is **also** recorded unverified — the owner supplied
the value but attested nothing about it, and the file's own rule treats an unattested value as
absent. **Phone still outstanding**; `03 4517 6915` remains flagged as a Victorian area code on a
NSW site.

**No `LocalBusiness` and no `Organization` schema.** D2's ladder resolves to **outcome 3** on every
page — `Service` omits `provider` entirely. §4.30.2 requires a verified *staffed* address; an
address alone does not satisfy it, and a trading name is not a legal entity. Runbook step 9 rewritten
to say so.

**D38 — the media intake directory is asserted image-only.** The owner quarantined two personal
résumé PDFs and an unregistered WXR export. `scripts/22-media-audit.py` now fails on any non-image
file, with **no per-name exemption** — the previous `readme.md`/`.gitkeep` carve-out was removed,
since a carve-out is how a non-image file sits in an intake directory unnoticed.

> **The directory is now image-only — confirmed.** 172 files, **0 non-images**, verified by the new
> assertion on 19 August 2026. It was delivered with 13 non-images; the owner quarantined the two
> résumé PDFs and the unregistered WXR, then the remaining PDFs and three markdown files. The
> assertion caught each round and now returns `non_images=0`.
>
> The media audit still FAILS overall, on a different and expected ground: it asserts post-rename
> Camden filenames against a pre-rename E&T directory. That clears only after the rename step.

### The five decisions, applied 19 August 2026

```text
  1  attachment filenames keep the corex- prefix    DELIBERATE ACCEPTANCE, recorded
  2  update the lib/ generator constants            APPLIED — 39 replacements, 5 modules
  3  retarget build/global-replace.json             APPLIED — 22 -> 25 rules
  4  email attested                                 APPLIED — verified: true, sighted 2026-08-19
  5  remove the tagline, do not rename it           runbook step 5b rewritten
```

**Decision 2** changes no built artifact — only what a regeneration would emit. Note `Structure Co`
is 7 characters longer than `CoreX` and `fit_meta_title()` truncates, so a regeneration will not be
a clean diff.

**Decision 4 is the first attested field in the build.** `contact.email` = `verified: true`,
`sighted_date: 2026-08-19` — **1 of 20**. Scope recorded in the file: the mailbox is live and
monitored; it attests nothing about a legal entity. Usable as a contact address and form recipient;
**not** usable as evidence of a verified business. **Phase C is unaffected and remains BLOCKED** —
email is not among the seven required identity fields.

> **Pre-existing defect found in `build/global-replace.json` — since FIXED** on owner instruction
> the same day. Detail below and in `reports/40-global-replace-ordering-fix.md`.

### Phase F — TWO CONCURRENT TARGETS

Confirmed by the owner 19 August 2026: these are separate, additional jobs. **Neither replaces the
other.** The earlier conflation is resolved.

```text
  TARGET A — brand placement                              RESOLVED, zero sourcing
    306, 307 and 422 are RETIRED; the Structure Co wordmark replaces them
    in-page brand placement       structure-co-horizontal.svg
    on dark backgrounds           structure-co-horizontal-reversed.svg
    6 slots on live pages         take the wordmark
    4 slots on withdrawn pages    need nothing
    outstanding                   §4.22.4 sighting before any slot is called correct

  TARGET B — false geographic claims                      STANDS, real sourcing cost
    16 REPLACE rows: Victorian photographs renamed to NSW places
    distinct pages               76      still active  38      withdrawn  38
    what is stale                the PAGE ARITHMETIC only, per D34.2
    action                       regenerate against the 77-page architecture
                                 before any credit is spent
```

Target B is the false-geographic-claim remediation on **38 active pages** — `TARNEIT-SOIL.jpg` as
`wianamatta-shale-clay-camden-1020.jpg`, `werribee-town.jpg` as `camden-town-centre-907.jpg`, and 14
more. The brand assets fix Target A and do nothing for Target B.

### `build/global-replace.json` ordering defect — FIXED

Three containment faults predated this session: `Wyndham` ran before `Wyndham Vale`, and `Werribee`
before both `Werribee South` and `Werribee River`. In a sequential contract the shorter find wins,
so the longer rule never matched and the output was **corrupted**, not merely un-replaced.

Reordered longest-find-first across the whole file on owner instruction. **3 violations → 0. 18 of
25 rules moved index. Pure permutation — no rule added, removed or edited, asserted.**

```text
  "Werribee River"  before: "mapped ... suburb per page River"   <- WRONG RULE
                    after:  "per-suburb water feature"
  "Wyndham Vale"    before: "per-page LGA from suburbs-expanded.json Vale"   <- WRONG RULE
                    after:  "mapped ... suburb per page"
  "Werribee South"  before: "mapped ... suburb per page South"    <- dangling fragment
                    after:  "mapped ... suburb per page"
```

**The defect was latent.** Both built WXRs were scanned for all three corrupted output strings, every
residual Victorian token and every unresolved placeholder: **no hits**. Nothing needs repairing in
the artifacts. The fix protects future generations — which matters, because the ten service pages are
being rewritten and will regenerate through this contract.
Detail: `reports/40-global-replace-ordering-fix.md`.

**Identity blockers cleared by DECISION-08 and the five decisions: zero.**

```text
  legal entity / legal name        unverified      unchanged
  ABN                              unverified      unchanged
  NSW Fair Trading licence         unverified      unchanged
  public liability insurance       unverified      unchanged
  workers compensation insurance   unverified      unchanged
  street address                   absent    ->    recorded, unverified
  staffed status                   unknown   ->    explicitly "unknown", unverified
  phone ownership + routing        unverified      unchanged, still flagged
  email                            absent    ->    ATTESTED, verified: true
  trading name                     3 names   ->    1 name, still unverified
```

`data/verified-facts.yml` now reports **1 field `verified: true`** — the email, which is not one of
the seven fields Phase C requires. **Phase C stays BLOCKED** on `legal_name`, `abn`,
`nsw_fair_trading_licence`, `insurance_public_liability`, `street_address`, `is_staffed` and
`phone`. No `LocalBusiness`, no `Organization`, D2 ladder outcome 3 unchanged.

Two real gains, neither of them a cleared blocker: the site will stop declaring another business's
trading name, and the build has its first attested fact.

### 19 August 2026 — Astra Customizer export supplied. Audit FAILS. Phase B still blocked.

`source-inputs/astra/astra-export.dat`, 2,627 bytes, SHA-256 `F4841CF5…`. Full audit:
`reports/41-astra-export-audit.md`. **Audit only — nothing imported or implemented.**

The file is **genuine** — it parses cleanly as a PHP-serialised Customizer export, 2,627 of 2,627
bytes consumed with no remainder, `template: astra`. It is also **partial**, and the audit fails on
that:

```text
  scripts/22-astra-audit.py    FAIL — 1 of 7 required mod groups present
    site-identity  PRESENT     custom_logo, site_icon
    colours        ABSENT      typography ABSENT   layout   ABSENT
    header         ABSENT      footer     ABSENT   buttons  ABSENT
```

It carries four pieces of real configuration — `custom_logo: 469`, `site_icon: 472`,
`custom_css_post_id: 893`, three menu locations — plus 1,832 characters of CSS. **All eight
`astra-settings[...]` keys in it are empty strings.**

**Astra design fidelity is NOT restored.** The long-standing note that this export *"governs header
rendering"* is only half answered: it names the logo, but carries no header layout, no colours, no
typography, no footer and no button mods, so Astra would fall back to defaults. A full Customizer
export remains outstanding.

**UPDATE, later the same day: the audit was revised and Phase B's precondition now clears.** The
six design groups are REPORTED rather than required — a Customizer export stores only what was
explicitly set, so UNSET is a valid stock configuration, not a partial export. Two genuinely
load-bearing checks replace them: **design-carriage** (the design must be locatable, and the report
must say where) and **internal-consistency** (every attachment ID, menu term and `custom_css_post_id`
the export references must exist in the WXR). The revised audit **PASSES**, and the ImageMagick probe
now targets WSL.

```text
  PHASE B PRECONDITION   RUNNABLE   the first phase in this build to clear its entry condition
    media 172/83; astra 1 file(s); driver present; ImageMagick installed in WSL

  Phase B step 1  media audit   FAIL   name-space artifact — asserts post-rename Camden
                                       filenames against a pre-rename E&T directory
  Phase B step 2  astra audit   PASS   required 1/1, carriage PASS, consistency PASS
```

**The precondition is the ENTRY condition, not the completion condition.** Phase B may now start. It
is not complete, nothing has been imported, and step 1 still fails until the six ` (1)`
collision-renamed files are renamed on approval.

#### Four reconciliations, all of which found something

**1. `custom_logo` 469 and `site_icon` 472 — the sixth and seventh brand files.** Both are E&T source
marks (`cropped-e-t-co-logo-transparent.png` 507×296, `cropped-e-t-co-logo-512.png` 512×512). Neither
was in the retired set, and neither is referenced by any page — because **theme mods do not travel in
a WXR**, so the only record that these are the live logo and favicon was in the file that did not
exist until today.

> **Correction to D27.** D27 directed *"remove attachment 177 as site icon"*. **177 is not the site
> icon — 472 is.** The WXR carries generated `site_icon-*` sizes for both, consistent with 177 being
> a former favicon replaced by 472 before the export was taken. 177 is AI-generated and stays
> retired; it simply was not the live one. **Retirement list is now 159, 177, 306, 307, 422, 469,
> 472.**

Neither 469 nor 472 carries C2PA or any AI marker, and neither derives from `eandtcologo.png`
(perceptual RMSE 0.65–0.67 — a different mark). **But absence of C2PA does not establish that an
image is not AI-generated, and this file set proves it:** `eandtcologo.png` carries a full manifest
naming *OpenAI Media Service API*, `gpt-image v2.0`, and the IPTC code `trainedAlgorithmicMedia`,
while its own crop `cropped-eandtcologo.png` carries **zero** — the crop stripped it. 469 and 472 are
themselves crops. No positive evidence of AI generation; the negative is not establishable from the
binaries. **The Structure Co wordmark and icon replace both regardless** — they are another
business's mark.

**2. `custom_css_post_id` 893 reconciles — but the two artifacts disagree on its content.** The WXR
has exactly one `custom_css` record, post_id 893, post_name `astra`, publish. The IDs match. The
bodies do not:

```text
  WXR post 893      1,830 chars   /* Local Camden project cards */     Werribee 0
  export wp_css     1,832 chars   /* Local Werribee project cards */   Werribee 1
  difference        exactly one line; everything else byte-identical
```

**The export is a pre-rename snapshot.** `Werribee` appears **zero** times in the main WXR; this
export is the only importable artifact in the build that contains it. The runbook imports the export
at step 2 and the WXR at step 4, and which version of post 893 survives has never been tested.
Recommended (not executed): correct the comment in the export, or strip `wp_css` from it and let the
WXR supply post 893.

**3. `.local-work-card` — not dead yet, dead the moment D32 runs.** 10 selectors in post 893; **45
class usages across 15 suburb pages** (6 publish, 9 draft). The WXR is immutable, so the D32 module
removal has not happened and every usage will import. The rules become dead when D32 is executed
post-import, and should be removed in the **same operation** — dead CSS styling a removed evidential
module is a trace of the module having existed. Note this audit counts the class (15 pages), D32
counts the module (16); reconcile at that step.

The `/* Local Werribee project cards */` comment is **registered as a footprint string**. It is not
covered by post-import rename steps 5a–5d, and **not** by preflight gate 13, which asserts the source
*business* name rather than source *locations*. `global-replace.json` has a `Werribee` rule, so a
regeneration would catch it — an import would not. **It needs its own assertion.**

**4. `nav_menu_locations` — supplied, and unsafe as given.** Three of five menus are mapped:
`primary → 9` (Primary), `mobile_menu → 10` (Primary (2)), `footer_menu → 13` (**Footer Blogs**).
**The two with no location are `footer-services` (11) and `footer-areas` (12).**

Three of five is defensible in principle — Astra registers three theme locations here, and the other
two menus are placed by the Footer Builder or an Elementor widget. **Which menu got the footer
location is not defensible:**

```text
  MENU              ITEMS   PAGE TARGETS   WITHDRAWN   DRAFT
  primary             23         21             7        7
  primary-2           23         21             7        7
  footer-services      7          7             0        0    <- unassigned
  footer-areas         6          6             0        0    <- unassigned
  footer-blogs         6          6             6        6    <- ASSIGNED to footer_menu
```

**All six Footer Blogs targets are withdrawn and draft.** Applying the mapping as supplied puts six
links to withdrawn, draft, noindexed pages in the footer of every page — a direct breach of the
standing safeguard *"Do not expose draft guide links in Wave 1 menus"*. The inversion is the striking
part: the two clean menus are the unassigned ones. `primary` and `mobile_menu` are also unsafe, at
7 withdrawn/draft targets each.

Recorded for Stage 29 step 4, **not executed**: do not apply `footer_menu → 13`; give it
`footer-services` or `footer-areas`; prune or rebuild `primary`/`mobile_menu`; and **add a preflight
assertion that zero menu items in an assigned location may target a withdrawn, draft or noindexed
page** — no existing gate covers this, which is why the mapping arrived unflagged.

### Pause baseline — the seven immutable hashes

```text
  camden-concreting-import.xml
    A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
    45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  build/stage9-page-manifest.json
    578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  build/stage8-image-map.json
    0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  reports/08-image-rename-map.csv
    43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  CODEX-BUILD-2.1.md
    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  archive/governing/CODEX-BUILD-2.md
    E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5

  7 of 7 MATCH at pause, 18 August 2026. Re-verified 7 of 7 MATCH, 19 August 2026
  (twice: after the media intake audit, and again after the DECISION-08 writes).
```

### P0 — unattested specification figures (DECISION-05 D26)

The `CODEX-BUILD-2.1.md` §2 clause protecting specific figures from correction is **withdrawn**. It had been protecting unattested numbers. Protection now comes from attestation, not from prior appearance.

- **214 unattested figure occurrences across 29 pages**, 22 of them active. Nothing deleted, nothing rounded — every figure is flagged in place per D26.3.
- Two populations tracked separately: **council-sourced-pending-verification** (800mm, 900mm, 1200mm, 4.0–5.5m, 4%, 1:6) and **template-artefact-unattested** (32 MPa, 125mm, SL72, SL82). Their verification paths differ and they must not be merged.
- **Any page carrying an unattested figure is blocked from every wave.** Wave 1 therefore collapses from 30 to **8**, and effectively to the 4 utility pages, since each of the 4 remaining suburbs carries its own separate blocker.
- The **homepage** — the only page that scored CLEAN on the coherence scan — carries all seven figures in one sentence beginning *"the recorded specification is"*, which is also a false-fidelity construction.
- Detail: `reports/35-figure-provenance.md`, `reports/35-figure-provenance.csv`.

### P0 — site mark (DECISION-05 D27, amended by DECISION-08 D36)

**D27 decided a text wordmark BECAUSE no honest mark existed. D36 removes that premise** — brand
assets have been supplied (though not yet placed on disk). The retained constraint: the mark carries
the trading name only, with no ABN, licence number, or establishment/licensed/insured wording until
those are verified.

**Original D27 decision, for the record: a text wordmark. No image mark ships.** Specified in `reports/35-site-mark-spec.md`, **not implemented** — the Astra export governs header rendering and does not exist.

A new finding: the Elementor kit still declares `site_name` as **"E&T Co Concreters Camden"** — the source Melbourne business — while the copy uses "CoreX Concreters Camden" 345 times. **Two trading names in one artifact, neither verified.** This is a residual footprint and a harder signal than shared module order or kit palette.


### How the build reached the pause

Gate 21 passed, and Stages 22–30 and 32 ran continuously under `RUN-BLOCK-01.md` §B. Stage 31 is excluded and was not run. Stages 34–35 then ran under DECISION-03, 04 and 05. All stage gates pass as audits; the audits' findings are what reduced the architecture from 157 pages to 76. Stage 28 preflight returns NO-GO on five gates, which is the expected and correct outcome.

The stage-order conflict that previously blocked Gate 21 was resolved by `RUN-BLOCK-01.md` §A D1: the 31A/31B split is declined and ordering stays 21 → 32 sequential. D1–D9 are recorded in `RUN-BLOCK-01.md`, which is the authoritative record of clauses that never reached disk as `DECISION-01-gate21.md`.

This is a post-build, pre-authoritative-staging project. It is not a live or launch-ready website:

- The offline WXR build completed Stages 0–10.
- `camden-concreting-import.xml` passed all 15 Stage 9 structural/content validation gates as an immutable 156-page artifact.
- `CODEX-BUILD-2.1.md` governs one crossover requirements calculator as a future supplementary artifact, `camden-calculator-import.xml`. It must not be added to or regenerated into the main WXR and has not yet been built.
- Stages 11–20 audited staging readiness, created a protected disposable local WordPress environment, tested IDs and import behaviour, and documented launch blockers.
- The disposable import test did not create the required attachment records because media fetching was deliberately disabled. It failed the media integrity gate and was rolled back.
- The local environment now contains only the protected WordPress baseline, not the Camden site. The Docker engine was not running when this file was updated.
- The authoritative staging import has not been performed.
- Nothing has been deployed to the live domain, no sitemap has been submitted, and no indexing has been authorised.
- Current index-ready count: **0 of 76 pages**.

## Architecture and artifact boundary

The resolved site architecture contains:

| Content | Count | State |
|---|---:|---|
| Home | 1 | active |
| Utility | 4 | active |
| Services | 10 | active, all 10 blocked by unattested figures |
| Suburbs | 60 | active; 15 researched, 45 deferred under D22 |
| Cost/comparison calculator | 1 | separate build target, §4.31, not yet built |
| **Total active** | **76** | |
| Guide hub | 1 | **WITHDRAWN** (D21) |
| Guides | 35 | **WITHDRAWN** (D21) |
| Cost/comparison, built | 10 | **WITHDRAWN** (D21) |
| Suburb/service intersections | 35 | **WITHDRAWN** (D16) |
| **Total withdrawn** | **81** | excluded at import, retained in the WXR |

Withdrawn pages are **not deleted** from the immutable WXR. Their research inputs are retained as rebuild material: `intersection-differentiators.json` and the `expansion-300-pages.md` §5 guide taxonomy both remain valid.

Artifact placement is deliberately split:

| Artifact | State | Pages | Import status |
|---|---|---:|---|
| `camden-concreting-import.xml` | Existing, immutable, Stage 9 validated | 156 physical | 21 publish / 135 draft |
| — of which withdrawn | Excluded at import, retained in the file | 81 | not imported |
| — of which active | The architecture | 75 | |
| `camden-calculator-import.xml` | Approved for Stage 31; not yet created | 1 | Must be draft + noindex |
| **Active architecture** | Current resolved plan | **76** | |

The validated main import also contains:

| Content | Count |
|---|---:|
| Attachment records | 83 |
| Menu items across five menus | 65 |
| Elementor kits | 1 |
| Astra custom CSS records | 1 |

The main artifact's passing internal validation means it is structurally consistent; it does **not** mean its publish-status pages are approved for launch or indexing. Its Stage 9 pass does not extend to the future supplementary calculator, which requires its own Stage 31 gates and combined cross-page checks.

## Work completed after the build

- Re-opened Gate 21 under the replacement governing instruction, remapped all 75 affected ledger references without citation loss, and confirmed the 157-page combined architecture against the 156-page manifest and immutable main WXR.
- Verified that the Stage 9 manifest and main WXR agree on all 156 page IDs, slugs, parent IDs, statuses and URLs.
- Added and passed a strict UTF-8 canary containing an em dash, en dash, `²` and a non-breaking space; corrected the one lossy decoder found in existing scripts.
- Restored and archived the superseded `CODEX-BUILD-2.md` semantically. Exact byte restoration is unprovable because no pre-edit checksum exists; the one-byte uncertainty is recorded in `reports/21-governing-doc-diff.md`.
- Created a loopback-only Docker WordPress smoke-test environment at `http://127.0.0.1:8088/`, protected by global noindex rules and unexpected-host blocking.
- Installed and recorded compatible test components, including Astra, Elementor 4.2.x, Rank Math, WordPress Importer, and Fluent Forms.
- Created clean database/uploads rollback checkpoints.
- Passed the pre-import post-ID collision audit.
- Confirmed that page IDs, statuses, guide hierarchy, menus, Elementor JSON, the imported Elementor kit, and Astra custom CSS survive a disposable non-media import.
- Confirmed that all 83 attachments and all 1,085 Elementor image references remain unresolved unless the real media binaries are imported correctly.
- Rolled the failed disposable import back to the clean protected baseline.
- Produced the existing readiness record for all 156 main-WXR pages; every row is `Index-ready: no`. Stage 23 must produce a 157-row v2 record including the blocked calculator.
- Verified environment-level route protection, rollback, desktop/mobile browser access, and Lighthouse tooling. These baseline checks are not Camden-site visual or performance approval.

## Immediate blockers

### P0 — before Stage 22

1. Resolve the governing sequence conflict: Stage 23 requires a 157th readiness row, Stage 25 requires measurement of all 157 pages, and Stage 28 requires both XML artifacts, while the supplementary calculator cannot be derived and built until Stage 31 and requires an approval pause before its body is written.
2. Supply `DECISION-01-gate21.md`. The handoff records Gate 21 as approved subject to owner decisions D1–D9, but that decision record does not exist anywhere in the workspace and no artifact cites it. D1–D9 are therefore unapplied and cannot be applied without inventing the content of an owner decision. Gate 21 remains BLOCKED on disk. See `reports/handoff-state.md`.

### Image sourcing — contradiction resolved (DECISION-07)

`IMAGE-REPLACEMENT-PROMPT.md` §2.1 permitted only Unsplash, Pexels and Openverse and prohibited search-engine scrapers; a SerpApi finder was then supplied. D33 resolves it: **SerpApi with `licenses=fmc` is permitted as a discovery mechanism, not as a licence.** Scrapers remain prohibited.

The operative guardrail: `fmc` reflects what a hosting page declares about itself. **Every candidate's licence is verified on its hosting page, before download, with no batch approval**, and any candidate whose licence cannot be established there is discarded — absence of a stated licence is not permission. `reports/33-licence-register.csv` becomes a permanent build artifact.

Tooling stays where it is until Phase F runs: `find_images.py` (5,802 bytes) and its venv live at `~/camden-images/` in WSL. `SERPAPI_KEY` is not set in the login shell. **No credits are spent until Phase F is unblocked and the spec CSV is regenerated** — the existing spec describes 228 page-slots of which 110 sit on withdrawn pages.

Environment requirements are now documented in `ENVIRONMENT.md` rather than assumed: ImageMagick (Phase B — **installed and verified in WSL, 19 August 2026**, alongside exiftool 13.50; the re-encode driver and EXIF assertion run there, not on Windows), Docker (not running), SERPAPI_KEY (not set), and the pinned container versions.

### P0 — resolved without new inputs (DECISION-06)

Four items executed. None needed owner data.

- **D29 homepage sentence rewritten.** The front page asserted *"the recorded specification is"* followed by seven unattested figures. Replacement copy written in `reports/36-homepage-rewrite.md`; the preferred version cuts the numbers entirely and claims nothing about the operator. A post-import edit — the WXR is immutable. **The four utility pages were scanned and are clean**; the homepage was the only instance outside the six already registered.
- **D30 `site_name` correction specified — RETARGETED by DECISION-08 D35 on 19 August 2026.** The Elementor kit declares **"E&T Co Concreters Camden"** — another business — and a tagline of **"Camden based Concrete Company Site"**, which is a location claim. Both reach a live page and neither can be fixed in the artifact. Runbook step 14 added; **preflight gate 13 added and currently FAILS**, which is correct. The wider sweep found 783 hits, but 781 are provenance records and audit trails doing their job; only those two reach a page.
  **D30's method is unchanged and remains correct — corrected at import, never in the artifact. Its target and scope have changed:** the correction is now to **"Structure Co Concreters Camden"** and covers `CoreX` as well as `E&T`, which widens it from 2 page-reaching values to **366 reader-visible occurrences across 111 of 156 pages**. Gate 13's pattern must be widened to include `CoreX`, and it will fail until the post-import rename runs. The tagline is a **rewrite, not a rename** — no trading name makes "Camden based" supportable from Pakenham. D30.4 stands verbatim: the correction replaces an incorrect claim with an unverified one. See `reports/38-trading-name-rename-plan.md`.
- **D31 privacy policy built.** `camden-privacy-import.xml`, post_id **1600** (above the highest occupied 1567, no collision), draft + noindex, 427 words, **11 blocking markers** for entity, ABN, recipient, retention and contact. Architecture **76 → 77**. Not published; this unblocks the page's existence, not its release.
- **D32 evidential modules removed.** No Camden job exists and fulfilment is Pakenham, so the 47 `REAL_PHOTO_PENDING` slots are settled, not pending. 16 pages lose the module for **427 words total**; no page drops below any floor. **The Tier 1 photography hold is releasable on all six pages** — the first blocker cleared rather than deferred, though each page still carries three or four others.

**Open owner decision:** `/gallery/` also carries attachment 306, one of the E&T symbol files superseded by D36, so its image slot is affected by that removal too. `/gallery/` is 108 words, 58 of them removed. A gallery with no images is not a gallery — withdraw it, repurpose it, or keep it empty and noindexed.

**Location premise checked:** the page copy makes **no** "locally based", "our crew", "years in the area" or response-time claims — only 16 "AREAS WE COVER" headings. The Pakenham fact does not invalidate the existing copy. It does bear on the kit tagline and on `service_areas`, which should be answered from where work will actually be done rather than from where pages exist.

### P0 — scope and rebuild (DECISION-04)

1. **Architecture reduced to 76 pages.** 157 → 122 (D16, 35 intersections) → **76** (D21, 35 guides + 10 cost/comparison + the guide hub). 81 pages withdrawn in total: marked `WITHDRAWN` in `reports/23-page-readiness-v2.csv`, excluded at import, **not deleted from the immutable WXR**. Waves 2, 4 and 5 are **empty**. Research inputs retained as rebuild material — `intersection-differentiators.json` and the `expansion-300-pages.md` §5 guide taxonomy both stay valid; only the generated copy is discarded.
2. **Composition: 1 homepage, 4 utility, 10 service, 60 suburb** in the main WXR, plus the calculator as a separate build target under §4.31. **Realistic Wave 1 is ~30 pages** — homepage, 4 utility, 10 rewritten service pages, 15 researched suburbs.
3. **`data/service-specs.yml` created and deliberately EMPTY.** Ten services × nine-plus fields, every field `verified: false`. **It must not be populated by an agent** — not from the existing pages, not from the other nine services, not from Australian Standards general knowledge (D23.2). It blocks the entire Wave 1 service rebuild.
4. **The nine "surviving" specifications are unattributed.** 32 MPa, 125mm, SL72, 800/900/1200mm, 4.0–5.5m, 4%, 1:6 appear **identically on all ten service pages** and are published as fact with no attestation. Identical values across ten different services is a template artefact, not a specification. Earlier reports described these as "true and sourced"; D23 corrects that and the correction is recorded in `reports/34-service-rebuild-brief.md` §2.

### OPEN SCOPE DECISION — the 45 unresearched suburbs (D22)

Deferred, **not dropped**. They remain in the architecture as draft + noindex, enter no wave, count toward no live total, and are not rewritten. Revisit once the ~30-page core is live and earning impressions. **Recorded here explicitly so it is not silently resolved by inaction.**

### P0 — coherence (DECISION-03 D15)

1. **82.4% of body words in the main WXR are machine-generated filler.** A full coherence scan of all 156 pages found **90 SEVERE** pages (all 10 service, all 35 intersection, all 35 guide, all 10 cost/comparison), 49 MODERATE suburb pages, 12 below threshold, and 5 clean (homepage plus the four utility pages). Sentences take a slug as their subject and assert nothing: *"new-driveway scope records scope boundary; new-driveway scope identifies the record owner."* See `reports/34-coherence.md`.
2. **Coherence is now a build-failing gate** in `build/21-spec-ledger.json` and `scripts/28-preflight.sh` (gate 12). No page above the filler threshold may enter any wave regardless of uniqueness, evidence or media status. Preflight now fails 5 gates, was 4.
3. **The 35 intersection pages are WITHDRAWN** (D16). Architecture 157 → **122**. They are marked withdrawn in `reports/23-page-readiness-v2.csv` and excluded at import, not deleted from the immutable WXR. Wave 5 is now empty. `intersection-differentiators.json` is retained as a rebuild input.
4. **Scope decision outstanding: 35 guides and 10 cost/comparison pages** are as SEVERE as the withdrawn intersections and have no disposition. 55 SEVERE pages remain in the architecture after D16.
5. **The 10 service pages are the Wave 1 critical path** (D17). Only **2,008 of 21,004 words survive** (9.6%). All nine real specifications survive on all ten pages — but they are identical across all ten, which needs owner or engineer input. See `reports/34-service-page-rebuild.md`.
6. **Three AI-generated images**, one (`272`) live on 14 pages — a direct standing rule 3 breach. Flagged, not classified. See `reports/34-place-assertion-audit.md`.

### P0 — new findings from Run Block 01

1. **20 of the 83 images are Victorian photographs renamed to specific NSW places**, on 85 of 156 pages. `TARNEIT-SOIL.jpg` became `wianamatta-shale-clay-camden-1020.jpg` and sits on 15 pages in the local-ground-conditions module; `werribee-town.jpg` became `camden-town-centre-907.jpg`. These are false geographic claims, not filename tidying. Owner decision required: supply genuine photographs, accept generic non-geographic imagery and rewrite the asserting copy, or withdraw the geographic claim. See `reports/24-images.md`.
2. **No privacy policy page exists**, yet Fluent Forms form ID 3 is specified for `/about/` and `/gallery/` and would collect name, phone, email and suburb. See `reports/30-forms-spec.md` §4.
3. **`reencode-images.sh` does not parse** — a quoting bug at line 11 makes it unrunnable, and ImageMagick is not installed. Corrected driver shipped as `scripts/22-reencode-images.sh`; the original is untouched pending an owner decision on which to retire.
4. **"Unique body words" is undefined in the source documents.** Two defensible readings give opposite verdicts, so no class uniqueness threshold can be enforced until the definition is settled. See `reports/25-uniqueness.md` §0.

### P0 — before authoritative staging import

1. ~~Obtain the original 83 image binaries referenced by the image map.~~ **Supplied 19 August 2026 and content-complete: 83 of 83 present, 77 under the exact required filename and 6 under a ` (1)` collision-rename.** This blocker is **NOT cleared.** It clears only when the six are renamed on approval, `22-media-audit.py` passes on its own terms, the re-encode driver runs and D25.2 passes, and the pixel-level sighting in 2b is done. See `reports/22-media-intake-reconciliation.md`.
2. ~~Obtain the separate Astra Customizer export/theme-mods evidence.~~ **A file was supplied 19 August 2026 and it FAILS the intake audit — 1 of 7 required mod groups.** It is a genuine but partial export: it names the logo (469) and favicon (472) and three menu locations, and carries no colours, typography, layout, header, footer or button mods at all. **This blocker is NOT cleared.** Astra design fidelity is not restored and a full Customizer export is still outstanding. See `reports/41-astra-export-audit.md`.
2a. **A working re-encode driver (D25).** `reencode-images.sh` has never parsed, so **no image in this build has ever had EXIF stripped**. If the 83 binaries import without it, embedded GPS coordinates from Melbourne job sites and owner/device metadata publish to a live website. Use `scripts/22-reencode-images.sh` (syntax-verified) and install ImageMagick. `scripts/22-media-audit.py` now carries a fail-closed EXIF assertion — zero GPS, owner/artist/serial and original-datetime tags — **verified against a known-dirty test file** by `tests/test_exif_assertion.py`.
2b. **Pixel-level verification is REQUIRED and not complete.** Every image audit so far has read filenames, titles and alt text only. Nothing has examined the images themselves. **The binaries are now local (19 August 2026), so this check is for the first time performable — and it has still not been performed.** Metadata will not catch it: the EXIF scan came back clean of GPS, which says nothing about what the photographs depict. An honestly-named photograph of a Melbourne street still shows Melbourne; only the human-sighted QA check H4 catches that.
3. Rebuild authoritative staging on PHP 8.3 or a confirmed Elementor-compatible patch level. The disposable PHP 8.4 environment logs an Elementor deprecation.
4. Start from a clean rollback checkpoint and repeat the occupied post-ID audit.
5. Import prepared media through a local-only, audited process that preserves all requested attachment IDs and exact filenames without remote fetching or filename suffixing.
6. Verify all media checksums, MIME types, dimensions, filenames, attachment IDs, and 1,085 Elementor image references before proceeding.

### P1 — before any page can be approved for indexing

- Resolve all **170** evidence-marker occurrences. Arithmetic per `DECISION-02-evidence-markers.md` §D10: **163 recorded + 4 + 3 = 170**, where the 163 recorded are 111 `PLACEHOLDER`, 47 `REAL_PHOTO_PENDING` and 5 `VERIFY`, and the seven additional are 4 literal `REQUIRED-RESEARCH` strings and 3 bare unbracketed `VERIFY` strings found in rendered page copy and present in neither the register nor the 45-suburb research set. An independent scan of all 156 pages returned exactly 170, confirming the total without adjustment. **This total is not settled**; Stage 23 rebuilds the register by corpus scan and reports any further divergence.
- Rewrite the **6 false-fidelity claims** registered in `reports/23-false-fidelity.md` (D11), and resolve **NT-1**, the non-textual claim added to that register on 19 August 2026: the `verified-badge` graphic on **14 pages** (1 publish, 13 draft) asserts a verification that has not occurred, on a site with 0 of 20 identity fields verified. It was in no register. Its default disposition is removal, which needs no owner input. The one `publish` page, `/concreters-leppington/`, was already held, so **effective indexable Wave 1 is unchanged at 14**. On three pages the badge is also serving as a service-tile illustration, a separate §4.22.4 fault. These assert that a council specification is reproduced, verified or unaltered where the underlying value is still a marker. Filling the marker does not clear them. Two of the six, both on Bringelly, are not fillable at all and require rewriting regardless of what the owner supplies.
- Obtain the **Liverpool City Council vehicle crossing specification** — widths, strength and fee schedule. One owner task unblocking four pages (Leppington, Austral, Edmondson Park, Bringelly). It may not be filled from a neighbouring suburb, from Camden Council, or from any other LGA. The Stage 31 calculator needs the same figures via `data/council-specs.yml`; one verification clears both and must not be satisfied twice with different numbers.
- Verify the legal/operating identity behind **“Structure Co Concreters Camden”** (DECISION-08 D35; supersedes “CoreX Concreters Camden”), including any intended ABN, licence, insurance, operator profile, and staffed-address claims. **The rename does not touch this blocker** — Structure Co has no verified entity, ABN or NSW licence either.
- **Attest the supplied address** `15 Murray Street, Camden NSW 2570` and answer whether it is **staffed**. Recorded 19 August 2026 as `verified: false` / `is_staffed: unknown`. Until both are verified, §4.30.2 forbids `LocalBusiness` and D2's ladder stays at outcome 3.
- ~~Confirm whether `info@concreterscamden.com.au` is attested.~~ **ATTESTED 19 August 2026** — mailbox exists and is monitored, `verified: true`, `sighted_date: 2026-08-19`. It may now be used as a contact address and as the Fluent Forms recipient. It is **not** evidence of a verified business and does not license any schema node.
- Prove ownership and current routing of `03 4517 6915`, or provide the correct replacement number. **Still outstanding after the 19 August partial NAP** — a Victorian area code on a NSW site.
- Create or import Fluent Forms form ID 3 only after its fields, recipient, consent/privacy basis, SMTP delivery, and use on About/Gallery are approved.
- Rebuild Rank Math schema only from verified facts and after checking the authoritative rendered pages.
- Configure the static homepage and Wave 1-safe menus. Draft guide links must not appear in live Wave 1 navigation.
- Complete logged-out route, visual, responsive, accessibility, link, canonical, robots, sitemap, schema, form, media, security, and performance QA.
- Make a page-by-page release decision; WXR `publish` status is not launch approval.

## Residual footprint risks — disclosed, not fixed

Both predate the validated WXR and cannot be fixed without mutating an immutable artifact. Recorded per `RUN-BLOCK-01.md` §A D5 as disclosed risks, not as tasks.

- **Module order is unchanged from the source site.** Structure doc §7 mitigation 4 (vary module order) is **NOT APPLIED**; standing rule 6 forbids restructuring an Elementor layout.
- **The Elementor kit palette is unchanged from the source site.** Mitigation 5 is **NOT APPLIED**; `#324A6D`, `#467FF7`, `#1C244B` and five further hex values appear in both WXRs. **Provenance corrected 19 August 2026:** these values are inherited through **inlined per-widget page styling**, not through the kit — the kit itself holds Elementor's factory palette, used by nothing. See the standing finding below.

- **No governing style layer — inherited architectural limitation.** Registered 19 August 2026 as a **standing finding, not a task**. Evidence: `reports/42-astra-vs-elementor-design-carriage.md`.

  ```text
    Astra theme mods   near-stock. Every design group UNSET, not missing.
    Elementor kit      factory defaults: #6EC1E4 #54595F #7A7A7A #61CE70,
                       Roboto / Roboto Slab. custom_colors and custom_typography
                       both empty. Zero button settings. site_logo and site_favicon
                       both empty. Each kit colour appears exactly ONCE in the whole
                       WXR - in the kit - and is used by nothing.

    the real design    inlined per-widget in page _elementor_data:
                         #1C244B  732 occurrences,    0 in kit
                         #324A6D  901 occurrences,    0 in kit
                         #467FF7  851 occurrences,    0 in kit
                         Poppins  2,655 occurrences,  one family, none in kit
  ```

  **Consequence: the site cannot be restyled centrally.** Any colour or type change is a mass edit across page data on 156 pages. There is no single place to change a brand colour, a heading font or a button style.

  **Do not attempt to build a governing kit.** That is a rebuild decision, not a Phase B one. Recorded here so it is neither forgotten nor mistaken for outstanding work.

## Safest next action

Obtain an owner decision on the Stage 31 sequencing conflict. The safe proposed resolution is to bring the Stage 31 inventory/approval/build gate forward before the first stage that requires the supplementary artifact, then resume the numbered stages without weakening the 157-page checks.

The **83 original image binaries have now been supplied** and audited (19 August 2026). Obtain the **Astra Customizer export**, which is the only remaining input blocking Phase B, then run the fail-closed intake audits to a genuine pass — including the post-rename re-run of `22-media-audit.py`, the re-encode driver in WSL, and the D25.2 EXIF assertion — before attempting another import. The pixel-level sighting of all 83 images is now performable and must happen before any page carrying a geographic claim is released.

After those inputs pass audit, rebuild clean authoritative staging, import and verify the complete site, resolve evidence page by page, and then approve the first publication wave. The guide hub and its first approved guides must be published together; the hub must never be published alone.

## Key safeguards

- Do not edit the source WXR export.
- Do not treat the disposable local environment as authoritative staging.
- Do not retry the authoritative import without the media and Astra inputs.
- Do not publish all 157 pages together.
- Keep the six Tier 1 suburb pages and Gallery `noindex,follow` until their evidence and photography gates pass. Leppington and Austral now carry a second, independent blocker — the Liverpool City Council specification — and clearing either one alone does not release the page. Effective indexable Wave 1 remains **14**, confirmed against the artifacts rather than assumed.
- Keep later suburbs, guides, intersections, and cost/comparison pages as drafts until individually approved.
- Do not create schema, reviews, pricing, local project claims, or business identity details from assumptions.
- Do not expose draft guide links in Wave 1 menus.
- Do not submit a sitemap or remove indexing protection until the launch gate passes.
- Do not modify or regenerate `camden-concreting-import.xml` to add the calculator. Build and validate the supplementary file separately at Stage 31.

## Source-of-truth files

- `camden-concreting-import.xml` — validated WXR import artifact.
- `CODEX-BUILD-2.1.md` — single active governing instruction for Stages 21–32.
- `archive/governing/CODEX-BUILD-2.md` — restored superseded instruction, retained for provenance only.
- `build/21-spec-ledger.json` — resolved 157-page specification and 156+1 artifact split.
- `reports/21-reconciliation-v2.md` — re-opened Gate 21 reconciliation, expected supplementary divergence and unresolved sequencing conflict.
- `reports/21-citation-remap.md` — complete old-to-new governing citation map.
- `reports/21-encoding-audit.md` — Unicode-integrity audit and canary result.
- `reports/21-governing-doc-diff.md` — restoration record for the superseded instruction.
- `reports/handoff-state.md` — successor-session artifact reconstruction, report-versus-artifact divergences, and the D1–D9 application status.
- `DECISION-02-evidence-markers.md` — owner decisions D10–D14 on unregistered evidence markers, false-fidelity claims and standing-guidance placement. Read-only.
- `reports/23-false-fidelity.md` — the D11.3 false-fidelity scan across all 156 pages. Produced at handoff-state; Stage 23 must re-run and confirm or extend it.
- `reports/placeholders.md` — evidence-marker register. **Superseded as a source by D10.3**: it is now a cross-check only, and the register is rebuilt by scanning the corpus.
- `reports/09-validation.md` — final build validation.
- `reports/10-handover.md` — completed build summary.
- `reports/11-staging-readiness.md` — staging entry conditions.
- `reports/15-import-verification.md` — disposable import failure and rollback evidence.
- `reports/18-page-readiness.csv` — page-by-page readiness matrix.
- `reports/20-launch-blockers.md` — current owner and technical blockers.
- `reports/20-staging-qa.md` — completed and blocked staging QA.
- `reports/placeholders.md` — evidence-marker register.
- `reports/post-import-tasks.md` — ordered import and release runbook.
- `build/stage9-page-manifest.json` — authoritative page manifest.
- `build/stage8-image-map.json` and `reports/08-image-rename-map.csv` — required media mapping.
- `staging/README.md` — disposable environment status and constraints.

## Updating this file

Update `CONTEXT.md` whenever a major gate changes. Record the date, the latest completed stage, what was actually verified, the remaining blockers, and the next safe action. Never describe a generated artifact, smoke test, or WXR publish status as a live-site launch.
