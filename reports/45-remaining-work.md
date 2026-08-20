# Inspection pass — actual remaining work to Wave 1

Date: 20 August 2026 (Australia/Sydney)  
Scope: inspection only. No phase was started, no container was started, and nothing was imported,
deployed, published or indexed.

## Executive verdict

The repository does **not** fully match `HANDOVER-2026-08-19.md`. The immutable ground is intact,
index-ready remains **0**, and launch remains **NO-GO**, but several later artifacts supersede the
handover and several planning artifacts are internally stale.

The most consequential new finding is not a testimonial: there are **zero fabricated customer
quotes**. It is the unaudited marketing copy. Fifteen active suburb pages assert `Licensed &
Insured` and fixed-price on-site quotes; Oran Park promises a written workmanship guarantee; 42
strings on 14 active suburb pages say `the verified project record says` although D32 establishes
that no Camden project exists. No preflight gate tests claim-to-evidence parity in rendered copy.

The second consequential finding is an architecture/import gap. The logical architecture is 158
rows — 156 main-WXR pages, one privacy page, and one planned calculator — but the readiness CSV has
157 rows because it contains the calculator and omits the built privacy page. More seriously, the
authoritative staging plan imports all 156 main-WXR pages and contains no executable mechanism to
exclude the 81 withdrawn pages.

## 0. Ground verification

### Immutable hashes

| File | Recomputed SHA-256 | Result |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | MATCH |

**7 of 7 match.** No hard stop was triggered.

### Phase preconditions

Exact result from `scripts/37-preconditions.py`:

| Phase | Name | Status | Evidence |
|---|---|---|---|
| A | attest the figures | BLOCKED | 91 service-spec fields `verified:false`, 0 true; populated flag false |
| B | media and staging | RUNNABLE | active media 81/81; immutable source 83; owner-excluded 2/2 retained; Astra 1; driver present; ImageMagick in WSL |
| C | identity and schema | BLOCKED | 1 verified true / 19 false; seven required identity fields unverified |
| D | Liverpool | BLOCKED | `data/council-specs.yml` absent |
| E | service page rebuild | BLOCKED | requires Phase A |
| F | images | BLOCKED | explicitly last; requires A–E |
| G | release | BLOCKED | requires preceding phases and preflight GO |

`RUNNABLE` is an entry condition. Phase B was not started.

### Deterministic preflight

The first WSL invocation could not find `python`. The full invocation used the repo's Windows Python
from WSL and produced all gates. Its top-line verdict is **NO-GO**.

| Gate | Result | Exact reported detail |
|---:|---|---|
| 1 | FAIL | canary failed — whole run is NO-GO regardless of other gates |
| 2 | PASS | 15/15 pass |
| 3 | FAIL | calculator WXR absent; main occupies 306 IDs, highest 1567 |
| 4 | PASS | all 83 binaries present and valid *(stale wrapper text; the audit's actual contract is 81 active)* |
| 5 | PASS | Astra parsed; carriage and consistency pass |
| 6 | PASS | 1,085 foreground, 98 background, 1,183 total, 73 of 83 IDs referenced, 0 unresolved |
| 7 | FAIL | 1,761 5-grams on more than two pages; 1,491 within-class pairs above 40% |
| 8 | PASS | 35 built, 35 allow-listed, all draft |
| 9 | PASS | planned Wave 1 menu JSON has zero draft/noindex/404 targets |
| 10 | PASS | main 0; calculator absent; privacy 0; Astra 0 after declared `wp_css` exclusion |
| 11 | PASS | zero JSON-LD blocks found, therefore zero placeholder-bearing blocks |
| 12 | FAIL | 90 SEVERE, 139 pages above threshold, corpus filler 0.8244 |
| 13 | FAIL | one E&T kit setting remains |
| 14 | PASS | planned retained menu sets show zero unsafe assigned targets |

Current failing gates are **1, 3, 7, 12 and 13**, not the handover's **3, 4, 7, 12 and 13**.

### UTF-8 canary

The standalone command under Windows Python passes all three assertions:

```text
PASS — UTF-8 canary survived an exact read-write-compare cycle
PASS — exact instruction assertion: ## 4.25 — Stage 25: uniqueness enforcement
PASS — exact report assertion: PASS — 157 combined (156 main + 1 planned supplementary)
```

Gate 1 fails only through the WSL-to-Windows-Python wrapper: WSL exports `PYTHONUTF8=1`, but the
interoperability boundary does not pass it to the Windows process. That is a real runner defect. The
assertion is not weakened or marked passing.

### Handover-versus-artifact divergences

1. The handover says testimonial text is unexamined. Artifacts dated 20 August contain a complete
   110-placement investigation and zero fabricated quotes.
2. Attachment 228 is on **14 pages**, not 15; it has 16 placements.
3. The handover says 83 active media files. The current active set is **81**; IDs 280 and 1067 are
   quarantined. The immutable media map still correctly has 83 source records.
4. The handover says all that remains of the sighting is Band A. The worksheet has only 9 verdicts
   and **74 blank rows**: A 16, C 5 and D 53. Band C retirement is decided, but its pixel verdicts
   are blank. Band D is deferrable under the brief, not completed.
5. The pixel-sighting brief says Band D has 55 items although the worksheet and band JSON have 53;
   its displayed band arithmetic totals 85 rather than 83.
6. The handover says Band A review completes Phase B. `RUN-BLOCK-02.md` also requires authoritative
   staging build, ordered imports and attachment/reference verification. Those steps have not run.
7. The handover's next verification target is 83 attachments and 1,085 image references. Band B's
   current post-import contract is 81 active attachments and 1,014 surviving foreground references,
   plus 98 background references.
8. Preflight gate 4 now passes; gate 1 now fails through the wrapper. The five-failure list changed.
9. The logical active architecture is 77, but `reports/23-page-readiness-v2.csv` has only **76
   non-withdrawn rows**: 75 built main-WXR pages plus the unbuilt calculator. It omits the built
   privacy page. A complete readiness record would have 158 total rows and 77 non-withdrawn rows.
10. The handover names `RUN-BLOCK-02-on-inputs.md`; the actual governing file is `RUN-BLOCK-02.md`.
11. `reports/29-staging-plan.md` still says the Astra export is absent and must carry seven design
    groups. The current Astra audit passes with one required group and valid stock defaults.
12. That staging plan imports all 156 main-WXR pages, does not import the privacy WXR, and implements
    no withdrawal filter. This contradicts the claimed 81-page import exclusion.
13. The staging plan says all five menus are assigned to Astra locations, although the resolved
    artifact correctly defines three assigned menus and two deliberately unassigned menus.
14. `build/21-spec-ledger.json` retains mutually stale snapshots: Astra `FAIL` and later `PASS`;
    media audit `FAIL` and later Band B `PASS`; gate 10 and gate 14 “current” values that no longer
    match the runner.
15. `reports/36-photography-removal.md` and `CONTEXT.md` say 16 `AREAS WE COVER` headings. Direct WXR
    inspection finds **15**, on the 15 researched suburb pages.
16. `data/verified-facts.yml` still treats real Camden photography and completed projects as pending
    inputs, contrary to D32's settled no-project/module-removal decision.
17. All seven retired brand binaries, AI image 272, soil image 1020 and the D18 generic-rename files
    remain in the technically passing 81-file directory. “Media audit PASS” therefore means binary,
    name-map, MIME, dimension and metadata integrity — not suitability to publish.
18. The six delivered ` (1)` collision files **were** renamed: attachment 226 to
    `concretejob2camden-226.jpg`, 227 to `backyard-patio-concreter-camden-227.jpg`, 228 to
    `fresh-concrete-side-yard-slab-228.jpg` (the later Band B generic rename), 468 to
    `corex-concreters-camden-logo-468.png`, 471 to `corex-concreters-camden-logo-471.png`, and 609
    to `exposed-aggregate-south-west-sydney-609.jpg`. There are zero ` (1)` remnants, and
    `scripts/22-media-audit.py` passes on its current terms: expected 81, present 81, OK 81, no
    missing, extras, non-images or failures.

## 1. Testimonial investigation

### Finding

**Fabricated customer testimonials: 0. Affected pages: 0. Publish-status pages: 0. Real people
named: 0.** No invented-testimonial category is added to the false-fidelity register.

| Attachment | Pages | Placements | Publish pages | Draft pages | Actual testimonial fields beside it |
|---:|---:|---:|---:|---:|---|
| 46 | 15 | 17 | 2 | 13 | none |
| 47 | 15 | 15 | 4 | 11 | none |
| 48 | 15 | 15 | 4 | 11 | none |
| 49 | 15 | 16 | 3 | 12 | none |
| 51 | 15 | 15 | 2 | 13 | none |
| 52 | 15 | 16 | 2 | 13 | none |
| 228 | 14 | 16 | 2 | 12 | none |

The only claim-bearing adjacency is four already-condemned local-work cards:

| Attachment | Page | Status | Exact text |
|---:|---|---|---|
| 46 | `/concreters-gregory-hills/` | publish | `[[REAL_PHOTO_PENDING: verified CoreX project in Gregory Hills]]` |
| 48 | `/concreters-edmondson-park/` | draft | `[[REAL_PHOTO_PENDING: verified CoreX project in Edmondson Park]]` |
| 49 | `/concreters-edmondson-park/` | draft | `[[REAL_PHOTO_PENDING: verified CoreX project in Edmondson Park]]` |
| 52 | `/concreters-catherine-field/` | draft | `[[REAL_PHOTO_PENDING: verified CoreX project in Catherine Field]]` |

Attachments 47, 51 and 228 have no local-work-card placement. Across all 110 placements there is no
customer name, quotation, star rating, testimonial suburb attribution, date, completed-job
description or price. The unchanged 110-row verbatim placement record is
`reports/45-testimonial-text-investigation.csv`.

The WXR has three actual testimonial widgets, all on publish-status `/homepage/`. All three contain
exactly:

```text
content  [[PLACEHOLDER: verified CoreX review text and permission to publish]]
name     [[PLACEHOLDER: verified reviewer name]]
job      (empty)
image    (empty)
rating   (absent)
```

None uses any of the seven attachments.

### Band B state

Band B is correctly recorded as seven `GENERIC` and two `UNUSABLE`. The seven filenames are changed
in the intake and title/alt remediation is encoded. IDs 280 and 1067 are quarantined and their 28
slot removals are encoded. The database transformation has **not run** and has not been runtime-
verified under PHP 8.3.

## 2. Marketing-claims sweep across the active architecture

### Corpus boundary

There are 77 logical active pages, but only 76 exist: 75 active pages in the main WXR and the draft
privacy WXR. The 77th, the calculator, is not built and cannot be audited. The sweep inspected every
visible Elementor text field on the 75 and the privacy body — 76 of 76 existing active pages.

| Claim family | Finding | Pages | Publish-status pages |
|---|---|---:|---:|
| Review/testimonial claims | three homepage placeholders; one About negation | 2 | 2 |
| Review counts | none | 0 | 0 |
| Star ratings | none | 0 | 0 |
| Years in business/experience | none | 0 | 0 |
| Numeric job/project/pour counts | none | 0 | 0 |
| `trusted` / `trusted by` | none | 0 | 0 |
| Accreditation/licence/insurance | unsupported positive headings on 15 researched suburbs | 15 | 6 |
| Awards | none | 0 | 0 |
| Guarantee/warranty | one workmanship guarantee; one privacy-policy use of “warranty” | 2 | 1 |
| Fixed-price assurance | 15 suburb headings plus two Oran Park body claims | 15 | 6 |
| Service-area/local-operation claims | 15 headings plus six Oran Park operator statements | 15 | 6 |
| Response-time promises | privacy policy says “reasonable period”; no service response-time promise | 1 | 0 |
| False verified-record construction | 42 strings across 14 researched suburbs | 14 | 5 |
| “Researched job record contains” | one per researched suburb | 15 | 6 |

`Get Your FREE Quote Today` occurs on 70 active main-WXR pages. It is a CTA, not a promise to reply
today, so it is recorded but not misclassified as a response-time promise.

### Exact unsupported marketing text

The shared 15-page set is:

```text
publish  /concreters-oran-park/ /concreters-leppington/
         /concreters-gregory-hills/ /concreters-gledswood-hills/
         /concreters-austral/ /concreters-harrington-park/
draft    /concreters-bringelly/ /concreters-catherine-field/
         /concreters-cobbitty/ /concreters-currans-hill/
         /concreters-edmondson-park/ /concreters-elderslie/
         /concreters-mount-annan/ /concreters-narellan/
         /concreters-spring-farm/
```

Accreditation headings, verbatim:

```text
Licensed & Insured
Licensed & Insured in Bringelly
Licensed & Insured in Currans Hill
Licensed & Insured in Elderslie
Licensed & Insured in Harrington Park
```

`Licensed & Insured` is used on the other eleven pages in the shared set. The current facts register
has no verified licence or insurance.

Price-assurance headings, verbatim:

```text
Fixed-Price On-Site Quotes in Oran Park
Fixed-Price On-Site Quotes in Oran Park in Bringelly
Fixed-Price On-Site Quotes in Oran Park in Currans Hill
Fixed-Price On-Site Quotes in Oran Park in Elderslie
Fixed-Price On-Site Quotes in Oran Park in Harrington Park
```

The first is used on the other eleven pages, even where the page is not Oran Park. The four doubled
headings are also template-collision evidence.

Other exact claims:

> Written workmanship guarantee on every job.

> NSW licence [[NSW_LICENCE_NO]], public liability and HBCF where required.

> We work across Oran Park and the surrounding Camden growth suburbs, including Catherine Field , Gledswood Hills , Gregory Hills and Harrington Park .

> Whatever the pour, we match you with concreters who do it every week.

> Oran Park sits at the geographic centre of the Camden LGA and it's where most of our work starts — new driveways at handover, alfresco slabs once the landscaping goes in, and shed slabs out the back a year later. One local detail worth knowing before anyone quotes you: the footpath allocation in Oran Park starts 800mm from your property boundary, not the 900mm that applies across the rest of Camden. Get the crossover set-out wrong by that 100mm and it fails inspection. We build driveways, slabs, paths and outdoor areas across Oran Park with proper base preparation, correct reinforcement and a fixed price before we start.

> It comes down to area, finish and access. A standard two-car driveway on a 350–450sqm lot is usually somewhere in the 40–70m² range from kerb to garage, and plain concrete sits at the lower end with exposed aggregate and decorative finishes above it. We measure on site and give you a fixed price rather than a per-metre estimate off an aerial photo. [[PLACEHOLDER: insert your real per-m² ranges once you've quoted 5+ Camden jobs]]

> Camden Council specifies SL72 fabric in a 125mm slab at 32 MPa for a residential crossing, and that's the standard we build the whole driveway to, not just the section on council land.

> We handle the application and the inspections as part of the job so you're not chasing Council yourself.

The 15 service-area headings are exactly `AREAS WE COVER AROUND ` followed by, respectively:
`AUSTRAL`, `BRINGELLY`, `CATHERINE FIELD`, `COBBITTY`, `CURRANS HILL`, `EDMONDSON PARK`, `ELDERSLIE`,
`GLEDSWOOD HILLS`, `GREGORY HILLS`, `HARRINGTON PARK`, `LEPPINGTON`, `MOUNT ANNAN`, `NARELLAN`,
`ORAN PARK`, and `SPRING FARM`. `service_areas` is empty and unverified; page existence is not
evidence that work will be performed there.

The privacy policy's only response-time wording is:

> We will respond within a reasonable period.

It remains draft and carries 11 identity, recipient, retention, contact, analytics and publication-
date blockers.

### False-fidelity construction missed by the existing register

There are 42 exact `verified project record` fields across 14 pages. They are not customer
testimonials, but the construction is false fidelity: D32 says no Camden job has been completed or
scheduled. Even where the underlying locality statement may be researchable, the claimed “verified
project record” does not exist. The exact fields are preserved in Appendix A.

Fifteen pages also use `The researched [suburb] job record contains...`. Each then says the examples
are a supplied job mix rather than an unverified project, but calling the source a “job record” is
still claim-bearing and must be rewritten or tied to a real source. Exact text is also in Appendix A.

## 3. Remaining-work inventory

Effort is elapsed hands-on effort, not a promise. “Pages unblocked” is the widest direct scope; it
does not mean those pages become launchable without their other blockers.

### Owner tasks, ordered by pages unblocked

| ID | Task | Who | Pages unblocked | Blocks | Effort | Current blocker |
|---|---|---|---:|---|---:|---|
| O1 | Establish the accountable operating model: legal entity/legal name, ABN, whether the site is a contractor or a lead-referral publisher, and a signed licensed NSW operator for fulfilment | Owner | all 77 | honest trading claim, privacy accountability, contracts, operator copy, schema, forms, launch | business task | no verified entity and no signed operator |
| O2 | Supply and attest licence holder/number/expiry, public-liability insurance, workers compensation and operator profile; otherwise direct removal of every related claim | Owner | all claim-bearing pages; 15 immediate | `Licensed & Insured`, guarantee, provider schema and any “we build/pour” wording | 30–60 min plus documents | all fields false |
| O3 | Prove phone ownership/routing or supply a NSW-routed replacement; attest or withdraw `15 Murray Street`; answer whether it is staffed | Owner | site-wide shared NAP; 24 marker pages | footer/contact copy, phone CTAs, `LocalBusiness`, privacy contact | 10–30 min plus evidence | phone unverified; address unverified; staffed unknown |
| O4 | Define real `service_areas` from where work will actually be done, not from the 60 suburb URLs | Owner | 60 suburb pages; 15 immediate claims | “AREAS WE COVER”, `areaServed`, local-operation wording | 15–30 min | value empty and false |
| O5 | Supply real per-m² ranges by finish and minimum job value, or approve removal of all pricing assertions | Owner | 53 | 53 pricing markers, fixed-price headings, Offers schema | 30–60 min | no quoted Camden evidence |
| O6 | Complete the service specification matrix: 10 services × 9-plus fields, each with source or named attestation | Owner/engineer/operator | 10 service pages; contributes to 22 figure-blocked active pages | Phase A, service copy, 91 active figure rows | 1–2 hr | 91 false, 0 true |
| O7 | Complete pixel sighting. Minimum claim-bearing remainder: A 16 and C 5; full pass also has D 53. Record `OK/GENERIC/REPLACE/UNUSABLE` and notes | Owner | 38 active pages directly; Phase B/site-wide indirectly | geographic imagery, brand confirmation, staging entry | 30–90 min | 74 worksheet verdicts blank |
| O8 | Supply Liverpool City Council vehicle-crossing widths, strength and fee schedule with URL and sighted date | Owner or explicitly authorised researcher | 4 pages; calculator data reused | Leppington, Austral, Edmondson Park, Bringelly and shared calculator row | 20–40 min | `council-specs.yml` absent |
| O9 | Decide `/gallery/`: withdraw, repurpose as a generic finishes page, or keep empty/noindexed | Owner | 1 | D32's two residual slots, navigation, form placement, MVP scope | 5 min | no genuine gallery and only 50 words after removal |
| O10 | Approve privacy/form decisions: accountable entity, retention, consent text, recipient, sending domain/SMTP, analytics disclosure and whether `/quote/` has its own form | Owner | privacy, About, Gallery, Quote | 11 privacy markers; Fluent Forms ID 3 | 30–60 min plus SMTP | seven form decisions and privacy identity unresolved |
| O11 | Supply the ten service drafts or explicitly authorise agent authorship after O6 | Owner | 10 | Phase E | one decision; copy ~1 week if owner-written | authorship not authorised and matrix absent |
| O12 | Decide whether unsupported marketing claims are removed or evidenced: licence, insurance, fixed price, guarantee, operator processes and “verified project record” wording | Owner | 15 researched suburbs plus homepage/utility surfaces | claim-remediation brief | 20–40 min | claims have no evidence |
| O13 | Resolve the still-live approval set: definition of unique body words; five class thresholds; five module contracts; calculator threshold/promotion; form sub-items; 1,085-vs-1,183 reference wording; root driver retirement; pinned staging versions | Owner | all gates/QA; direct page count varies | enforcement and reproducible staging | 45–90 min | all remain explicitly unapproved |
| O14 | Approve the Stage 31 derived calculator slug/module outline when produced | Owner | Gate 3 / all Wave 1 indirectly | calculator artifact and preflight GO | 10 min | inventory/outline not yet produced in an authorised Stage 31 run |
| O15 | Give explicit page-release, deployment, noindex-removal and sitemap/indexing approval after all gates pass | Owner | selected Wave 1 | live release | 15–30 min | no page is ready and this inspection authorises no release |

The 45 unresearched suburbs are **not** an owner task on the Wave 1 critical path. D22 defers them:
they remain draft + noindex, enter no wave, and are revisited after the core earns impressions.

### Agent tasks, ordered by pages unblocked

| ID | Task | Who | Pages unblocked | Blocks | Effort | Current blocker |
|---|---|---|---:|---|---:|---|
| A1 | Reconcile the architecture to 158 logical rows/77 active: add privacy to readiness, preserve calculator as unbuilt, and propagate counts to wave, schema and QA artifacts | Agent | all 77 | trustworthy release record | 2–4 hr | readiness currently substitutes calculator for privacy |
| A2 | Build an executable withdrawn-page import filter/prepared derivative WXR and assert that 81 withdrawn pages never enter authoritative staging | Agent | all 77 | honest architecture and staging import | 4–8 hr | plan currently imports all 156 pages |
| A3 | Repair the authoritative staging plan to current facts: Astra PASS contract, 81 active media, privacy import, calculator order, three menu locations, Structure Co target and current counts | Agent | all 77 | executable import | 2–4 hr | plan is a stale Stage 29 snapshot |
| A4 | Implement Astra import exclusions rather than merely declare them: exclude `wp_css`, override footer mapping, verify hashes and prove zero Werribee after import | Agent | all 77 | safe Astra import | 2–4 hr | exclusion JSON exists; importer/filter does not |
| A5 | Make the preflight wrapper platform-consistent so the exact canary passes without relaxing it | Agent | all 77 | Gate 1 | 1–2 hr | WSL environment is not reaching Windows Python |
| A6 | Replace preflight gate 2's mislabeled structural subset with true re-execution of the 15 Stage 9 gates; require exactly one H1 | Agent | all 77 | trustworthy preflight | 3–5 hr | current “15/15” is not the Stage 9 gate set |
| A7 | Expand post-ID collision auditing across main WXR, privacy WXR, calculator WXR, attachment/menu/kit/custom-CSS records | Agent | all 77 | Gate 3 and supplementary imports | 1–2 hr | gate omits privacy ID 1600 |
| A8 | Correct gate 4's 83-file text and assert both immutable 83-source provenance and active 81-file shipment | Agent | all 77 | unambiguous media gate | 1 hr | wrapper detail contradicts audit |
| A9 | Split gate 6 into immutable-WXR baseline and post-remediation staging assertions: 1,085→1,014 foreground, 98 background, 81 active attachments | Agent | all 77 | live media verification | 2–3 hr | current gate passes only the raw WXR |
| A10 | Widen gate 13 to fail on all reader-visible CoreX/E&T forms and the unsupported `Camden based` tagline, while preserving 100 deliberate filename/URL prefixes and provenance | Agent | all 77 | 366→0 reader-visible rename verification | 2–4 hr | current regex does not test CoreX |
| A11 | Change menu gates from plan-only validation to a two-stage assertion: plan is safe and authoritative staging actually contains/assigns exactly 27 retained items | Agent | all 77 | menu release | 2–3 hr | gates 9/14 can pass before prune or assignment |
| A12 | Add an active-architecture parity gate: exactly the approved 77 logical rows, 76 built before calculator, no withdrawn page imported or linked | Agent | all 77 | next coherence-like structural gap | 2–3 hr | no gate asserts plan versus imported database |
| A13 | Add a rendered claim-to-evidence gate for licence, insurance, accreditation, awards, reviews, ratings, years, job counts, guarantees, fixed-price, response time, service areas and local-operation wording | Agent | all 77 | next coherence-like truth gap | 3–6 hr | current gates scan schema/markers, not marketing copy |
| A14 | Register and remediate the 42 `verified project record says` fields and 15 `researched ... job record contains` fields; retain only sourced locality facts with honest attribution | Agent | 15 researched suburbs | truth-in-copy gate | 2–4 days including source re-check | no claimed project record exists |
| A15 | Remove or evidence the 15 `Licensed & Insured` headings, 15 fixed-price headings, Oran Park guarantee and all operator-process claims | Agent after O2/O5/O12 | 15 | researched suburb release | 4–8 hr | owner evidence/disposition absent |
| A16 | Rewrite the homepage as a transparent publisher/referral surface: apply D29, remove three review placeholders, remove operator/local-project/price claims and correct the business model | Agent after O1/O12 | homepage | MVP | 4–8 hr | identity/model decision absent |
| A17 | Rewrite all ten service pages against the attested matrix; then pass coherence, approved uniqueness, ≤40% pair cap and opening test | Agent after O6/O11 | 10 | Phase E / service core | 5–7 days | matrix/authorship |
| A18 | Rewrite and re-source the 15 researched suburb pages to clear coherence and false-fidelity while preserving genuine local research | Agent after O4/O8/O12 | 15 | realistic Wave 1 suburbs | 5–8 days | service areas, council and claim disposition |
| A19 | Reconcile all 214 unattested figures across 29 pages: replace, confirm or remove; rerun gates on the 22 active affected pages | Agent after O6/O8 | 22 active | Phase A completion | 1–2 days | sources/attestations absent |
| A20 | Apply Band A verdicts: rename filename/title/per-page alt for GENERIC, remove UNUSABLE, and source only authorised/licensed REPLACE images | Agent after O7 | 38 active | Phase B/F image truth | 1–3 days depending on replacements | verdicts absent; Phase F last |
| A21 | Reverse the 60 `-camden-` naming artefacts and the settled D18 renames (1056, 1151, 1188) as filename/title/alt atomic operations | Agent | up to 77 | honest media naming | 1–2 days | post-import transformation not built |
| A22 | Remove AI attachment 272 from its 14 WXR placements; keep 159/177 retired; verify no AI/generated asset is presented as work | Agent | active subset plus withdrawn | D24 | 2–4 hr | only a textual runbook instruction exists |
| A23 | Retire attachments 159, 177, 306, 307, 422, 469 and 472; upload Structure Co assets as new attachments; replace six active in-page slots plus header/site icon; leave four withdrawn slots absent | Agent | six active pages + site-wide brand | D36 | 3–6 hr | no import/database exists |
| A24 | Remove soil image 1020 while retaining its sections, then resolve the remaining 16-row geographic-image specification against the active architecture | Agent after O7 | 38 active | D19 / Target B | 1–3 days | Band A verdicts and Phase F ordering |
| A25 | Finish D32: run the 15-module/45-image transformer, separately execute the chosen Gallery disposition for its two slots, remove dead `.local-work-card` CSS, and verify zero local-work claims | Agent after O9 | 16 | evidential-module cleanup | 3–5 hr | Gallery decision; PHP runtime not yet tested |
| A26 | Runtime-lint and dry-run the Band B/D32 PHP transformation under the pinned PHP 8.3 WordPress stack; retain its exact-count rollback contract | Agent | all affected media pages | safe post-import mutation | 2–4 hr | no container/import; host PHP unavailable |
| A27 | Apply the CoreX rename at import: 466 total occurrences attributed, exactly 366 reader-visible targets renamed, 100 path/filename occurrences retained; verify zero residual reader-visible forms | Agent | 111 source pages before withdrawal filter; all imported pages after | identity cleanup | 2–4 hr | no import; gate incomplete |
| A28 | Apply D29 site title/tagline, static homepage, permalinks, Elementor cache/CSS regeneration and current brand assignments with rollback after each mutation | Agent | all imported pages | correct rendering | 3–5 hr | authoritative staging not built |
| A29 | Prune primary/mobile from 23 to 10 each, retain seven Footer Services items, leave Footer Areas/Blogs unassigned, then test rendered menus logged out | Agent | all imported pages | navigation | 2–3 hr | plan-only artifacts |
| A30 | Resolve the privacy policy's 11 markers from O1/O3/O10 and add it to the readiness/release records | Agent after owner facts | privacy + forms | privacy compliance | 3–5 hr | accountable entity/retention/analytics/contact absent |
| A31 | Implement Fluent Forms ID 3 only after approval; configure authenticated SMTP, consent, retention and real test delivery; settle About/Gallery/Quote placements | Agent after O10 | 2–3 utilities | enquiry collection | 3–6 hr | seven approvals and identity |
| A32 | Regenerate schema for the imported active set only; emit no `LocalBusiness`/`Organization` without verified fields, no dangling IDs, no placeholder FAQ, and no schema for withdrawn pages | Agent after O1/O3/O4 | all imported pages | schema gate | 3–5 hr | identity/service areas; current output covers stale scope |
| A33 | Build the calculator as a separate draft/noindex artifact after outline approval, run its own gates and the bounded Stage 31 delta, and add it to collision/readiness records | Agent after O14 | Gate 3 / all Wave 1 indirectly | preflight GO | 1–2 days | Stage 31 not authorised; outline absent |
| A34 | Build clean PHP 8.3 authoritative staging, import in the corrected order with rollback after every mutation, and verify page/media/menu/brand/reference counts | Agent after gates and owner inputs | all 77 | release QA | 1–2 days | preflight NO-GO and plan defects |
| A35 | Run the 29-check QA specification: 13 automated plus 16 human-sighted, including forms, responsive/accessibility, security and mobile Core Web Vitals | Agent + owner sighting | selected Wave 1 | index-ready decision | 1–2 days | no authoritative staging |
| A36 | Make page-by-page release decisions, deploy only the approved set, retain global noindex until approval, then remove noindex and submit sitemap only after GO | Agent after O15 | selected Wave 1 | live/indexing | 0.5–1 day | all preceding work and explicit authority |

### Explicitly deferred, not dropped

- The 45 unresearched suburbs remain draft + noindex under D22. They are not rewritten for Wave 1.
- The 35 intersections, 35 guides, 10 built cost/comparison pages and guide hub remain withdrawn,
  with their research inputs retained for future rebuilds.
- The site-wide inlined Elementor style layer and shared source module order are disclosed inherited
  limitations, not tasks.

## 4. What fell through

### D1–D38 application audit

“Applied” below means the required artifact reflects the decision. It does not imply that a
post-import action has run.

| Decision | State | Artifact finding |
|---|---|---|
| D1 | PARTIAL | Stage order and missing-calculator NO-GO are applied. The Stage 31 delta is correctly pending. Later privacy WXR is absent from the collision/readiness model. |
| D2 | APPLIED OFFLINE | Schema builder omits provider and avoids dangling IDs. It has not been regenerated for the corrected active architecture. |
| D3 | APPLIED | Ledger/report use 27 unthresholded pages, 26 built at that time. Privacy later added a utility without readiness propagation. |
| D4 | APPLIED AT STAGE 23 | Slug join and page IDs were used. The later privacy page has no row. |
| D5 | APPLIED | Module order and inherited styling are disclosed residual risks, not mutation tasks. |
| D6 | APPLIED IN PLAN | Wave 1 menu plan links all ten services. No live/imported menu exists. |
| D7 | SUPERSEDED IN PART | Reuse policy stands; evidential-photo slots are superseded by D32 removal. Generic images still need honest context. |
| D8 | APPLIED, APPROVALS OPEN | Module-contract gap report and clause alias exist. Five proposed contracts remain unenforced. |
| D9 | APPLIED | Semantic restoration and the immutable baseline are recorded; no byte-exact claim is made. |
| D10 | PARTIAL AFTER LATER CHANGES | The 170-marker WXR scan exists. Privacy's 11 markers are outside the 157-row readiness register, and D32 removals are not executed. |
| D11 | UNDER-APPLIED | Six text claims and NT-1 are registered, but this inspection found 42 additional `verified project record says` fields on active pages. |
| D12 | APPLIED | Liverpool is one deduplicated owner task and calculator dependency. |
| D13 | APPLIED AT THE TIME; STALE AFTER D32 | Liverpool blockers are recorded. Tier 1 photography holds are still encoded in menu/gate artifacts although D32 made them releasable. |
| D14 | APPLIED | Standing guidance is in ledger/reports, not appended to read-only instructions. |
| D15 | APPLIED | Full coherence scan and build-failing gate 12 exist. It tests sense, not truth. |
| D16 | PARTIAL | Intersections are `WITHDRAWN` in readiness, but there is no executable import exclusion. |
| D17 | APPLIED AS BRIEF | Service rebuild brief exists; replacement copy correctly remains unwritten. |
| D18 | PARTIAL | Extended detector and dispositions exist. 1056/1151/1188 renames, geographic replacements and logo retirement have not run. |
| D19 | UNAPPLIED POST-IMPORT ACTION | Soil image 1020 remains in the active 81-file directory and WXR placements. |
| D20 | PARTIAL | Band B filename/title/alt atomic update is encoded. The wider D18/D24/60-file operation is not. |
| D21 | PARTIAL | 46 more pages are marked withdrawn; no import exclusion implements the disposition. |
| D22 | APPLIED | Forty-five suburb shells are explicitly deferred, not dropped. |
| D23 | APPLIED AS HARNESS | Empty matrix and rebuild brief exist. Matrix remains 91 false; no service copy is authorised. |
| D24 | PARTIAL | 272 removal is only in the runbook. 159/177 were later absorbed into D36 retirement. All three binaries remain in the active directory. |
| D25 | APPLIED | Correct driver ran, EXIF was stripped and media audit passes. Root broken driver retirement remains undecided. |
| D26 | APPLIED AS REGISTER | 214 figures across 29 pages are recorded. None has been reconciled because sources/attestations are absent. |
| D27 | SUPERSEDED/CORRECTED | D36 supplies assets; 177 was not the live site icon, and 306/307 were not orphaned. |
| D28 | SUPERSEDED PAUSE STATE | Later owner inputs resumed limited work. Current build is still paused, but not for the original media/Astra reasons. |
| D29 | WRITTEN, NOT APPLIED | Preferred homepage replacement exists only in a report/runbook. Immutable WXR still has the false sentence. |
| D30 | PLANNED, NOT APPLIED | Import-time identity correction has not run. Gate 13 is not widened to CoreX and can false-pass after only E&T is removed. |
| D31 | PARTIAL | Privacy WXR exists and validates, but is absent from readiness, collision gate, staging sequence and page totals. |
| D32 | PARTIAL | Removal of 15 suburb modules/45 images is encoded but unrun. Gallery's two slots remain subject to O9. Forty-two “verified project record” fields and 15 job-record fields remain. |
| D33 | APPLIED AS POLICY | SerpApi/licence rules are recorded; sourcing correctly has not run. |
| D34 | PENDING BY DESIGN | Finder is still outside the repo and the 16-row spec is stale. Work waits for Phase F. |
| D35 | PLAN COMPLETE, EXECUTION PENDING | 466 total CoreX occurrences are attributed; 366 reader-visible targets await import-time rename. |
| D36 | PARTIAL | Assets are verified and six active replacement slots are decided. Seven retired old-brand files remain in active media and no slot assignment has run. |
| D37 | PARTIAL AS DECIDED | Email is the only verified fact. Trading name, address, staffed status and phone remain unverified; no identity blocker cleared. |
| D38 | APPLIED | Active intake is image-only and audit passes 81/81. Suitability to publish is outside this technical assertion. |

### All still-operative `AWAITING APPROVAL — not enforced` items

1. Definition/denominator of “unique body words”.
2. Home unique-body floor 0.75.
3. Utility floor 0.65.
4. Service floor 0.75.
5. Guide-hub floor 0.75.
6. Cost/comparison floor 0.75. Together, items 2–6 govern the stated 27 unthresholded logical
   pages: 1 home + 4 utilities + 10 services + 1 guide hub + 11 cost/comparison (26 are built; the
   calculator is the planned eleventh cost/comparison page).
7. Home module contract.
8. Utility module contract.
9. Guide-hub module contract.
10. Guide module contract.
11. Cost/comparison module contract.
12. Calculator uniqueness threshold after it exists.
13. Calculator promotion from Wave 4 to Wave 2 after all four LGA datasets are verified.
14. Fluent Forms ID 3's seven decisions: fields, recipient, consent, privacy, retention, SMTP and
    `/quote/` scope.
15. Correction of the governing 1,085 reference figure to distinguish 1,085 foreground from 1,183
    total including 98 backgrounds.
16. Retirement of root `reencode-images.sh`.
17. Authoritative staging theme/plugin versions against the source installation.
18. Stage 31 derived slug and module outline, once produced.

The Gallery disposition and service authorship are open owner decisions, but they were not labelled
with the exact `AWAITING APPROVAL — not enforced` phrase in the source reports.

### What every current preflight gate asserts — and what may pass while false

| Gate | Actual assertion | False-pass surface |
|---:|---|---|
| 1 | One UTF-8 fixture round-trips and two exact strings exist | Other scripts may still decode lossily; wrapper can fail despite a good runtime |
| 2 | Fifteen structural parity checks written inside `28-gates.py` | It is not the 15 Stage 9 gate set; missing H1 passes because it tests `<=1`; links, meta, cache, placeholder registration and focus keywords are not re-run here |
| 3 | Main and calculator occupied IDs do not collide | Privacy WXR ID 1600 is omitted; calculator absence fails, but a future privacy collision could pass |
| 4 | Active media matches the technical audit overlay | Says “83” while contract is 81; pixels, licensing, retirement decisions and database attachment resolution are not tested |
| 5 | Astra serialisation, carriage location and referenced IDs/terms are internally consistent | Does not prove import execution, `wp_css` exclusion, correct menu override or visual header fidelity |
| 6 | Raw immutable WXR has exactly 1,085 foreground refs and zero unresolved IDs | Background 98 is advisory; post-Band-B 1,014 contract and active 81 attachments are not tested |
| 7 | No global 5-gram appears on >2 pages and no within-class pair exceeds 40% | Does not test meaning or truth; class percentages are unenforced; withdrawn pages dominate the raw corpus |
| 8 | Intersection slug set equals JSON, count 35, all draft | Does not test differentiator fidelity, parent links, shared-spec budget or that withdrawn pages are excluded |
| 9 | `build/27-wave1-menus.json` is safe | Can pass before any menu is pruned or assigned in WordPress |
| 10 | Declared effective import payload has zero terms from a 13-term Victorian list | Trusts a declarative Astra exclusion not yet implemented; missing supplementary is not itself a gate-10 failure; list is finite |
| 11 | No placeholder token appears in inline Elementor JSON-LD | Passes vacuously because there are zero JSON-LD blocks; does not validate external/current schema output |
| 12 | Filler ratio stays below threshold | Sensible lies, unsupported licence/guarantee/price claims and false fidelity pass |
| 13 | E&T patterns are absent from kit/body/calculator | Does not scan CoreX despite D35; does not require correct Structure Co value; can pass with all 366 CoreX reader targets intact |
| 14 | Planned retained item IDs, combined with raw WXR statuses/holds, yield no unsafe assigned target | Can pass before prune/assignment; does not crawl rendered navigation or verify the live DB |

The **next coherence-like gap** is rendered **claim-to-evidence parity**. Structural, schema and
coherence gates can all pass while a page says `Licensed & Insured`, promises a guarantee or calls
unsourced copy a verified project record. A separate active-architecture/import-parity gate is also
required so gates cannot pass against safe plans while WordPress contains all 81 withdrawn pages.

### The original 15 Stage 9 gates and their blind spots

| Gate | Check | What can still be false when it passes |
|---:|---|---|
| 1 | XML well formed | semantics, truth, completeness |
| 2 | Elementor JSON parses | rendered meaning and validity of individual settings |
| 3 | JSON round trip | truth and rendering |
| 4 | exactly one H1 | heading quality and hierarchy below H1 |
| 5 | Victorian blocklist zero | renamed Victorian assets, finite-list omissions and unsupported NSW claims |
| 6 | image IDs resolve to 83 attachment records | binaries absent, wrong pixels, false filenames/alts |
| 7 | links resolve and zero orphans | withdrawn/noindex targets and navigation intent |
| 8 | no Rank Math schema meta | absence of valid schema can pass |
| 9 | no Elementor cache meta | rendered site can still be stale/broken after import |
| 10 | duplication thresholds on an exempted subset | incoherent unique filler and 45 shell exemptions |
| 11 | meta lengths | truthful/meaningful meta not tested |
| 12 | meta uniqueness | unique nonsense or unique false claims pass |
| 13 | 163 markers registered | the register was undercounted; unmarked false claims pass |
| 14 | focus keyword non-empty/spelled | relevance, stuffing and truth not tested |
| 15 | 21 publish / 135 draft | WXR status is not release approval |

### Artifact contradictions requiring correction

- `reports/23-page-readiness-v2.csv`: 157 rows and 76 non-withdrawn; privacy missing. The correct
  logical model is 158 rows and 77 non-withdrawn.
- `reports/29-staging-plan.md`: stale Astra precondition; no privacy import; imports all 156 pages;
  no withdrawal filter; stale counts; five-menu/three-location contradiction; identity target stale.
- `build/21-spec-ledger.json`: current-state fields coexist with superseded snapshots without a clear
  supersession pointer for Astra, Phase B and preflight gates.
- `reports/36-photography-removal.md` and `CONTEXT.md`: 16 service-area headings versus 15 in WXR.
- `data/verified-facts.yml`: completed-project/photography inputs contradict D32; `service_areas` and
  pricing remain genuinely open; email comments lag its verified state.
- `reports/post-import-tasks.md`: still directs marker work from superseded `reports/placeholders.md`
  rather than the corpus-scan evidence register; some project-photography language predates D32.
- `reports/44-pixel-sighting-brief.md`: Band D 55 versus actual 53 and internally impossible total 85.
- `scripts/28-preflight.sh`: hard-coded gate-4 detail says all 83; platform contract assumes MSYS bash
  plus Windows Python although this repo uses WSL bash.
- `scripts/28-gates.py`: gate 2 is mislabeled, gate 3 omits privacy, gate 13 omits CoreX, gates 9/14
  validate planned state rather than applied state.
- `staging-authoritative/`: contains compose, containment, checkpoint, media importer and Band B
  transformer, but no executable Customizer exclusion/filter, withdrawn-page filter, privacy import,
  menu prune/assignment, identity rename, brand replacement or full orchestration script.

## 5. Honest launch assessment

### Minimum viable Wave 1

**In the current identity/operator state, the minimum honest Wave 1 is empty: zero pages.** No page
can be released while the shared site identity, phone/footer, operating model and accountable privacy
entity are unresolved. A publish-status WXR row does not change that.

If the owner verifies an accountable publisher and explicitly changes the offer to a transparent
lead/referral service, but still has no signed NSW operator, the smallest conditional informational
set would be:

1. `/homepage/`
2. `/about/`
3. `/contact/`
4. `/privacy-policy/`

That would be a publisher/referral holding site, **not a concreting contractor site**, and it must not
accept fulfilment-bound leads until a signed operator exists. `/quote/`, `/gallery/`, all ten service
pages and all suburb pages remain out of that minimum.

### What each conditional page still needs

| Page | Required before release |
|---|---|
| `/homepage/` | transparent publisher/referral disclosure; verified accountable entity; D29 applied; all three review placeholders removed; no “we build/pour”, local-job, licence, insurance, guarantee, fixed-price or local-presence claim; honest media; clean footer/NAP; Structure Co rename/brand; coherence/claims/schema/menu/QA pass |
| `/about/` | legal publisher identity and role; no operator/licence/review claim; brand slot 306 replaced; form absent or fully approved; privacy link; clean phone/address/footer; QA |
| `/contact/` | attested email may be used; unverified phone/address removed or proven; brand slot 306 replaced; no form until privacy/consent/SMTP pass; QA |
| `/privacy-policy/` | all 11 markers resolved; accountable entity, recipient, retention, contact, analytics and effective date verified; added to readiness/collision/import/menu records; QA |

Even this conditional set is not viable now because the publisher/legal entity is unverified.

### Claims prohibited in the current state

- No NSW licence, licence number, accreditation or “Licensed & Insured”.
- No public-liability/workers-compensation claim.
- No “we pour”, “we build”, “we handle the application”, “our work starts”, or equivalent contractor
  process claim.
- No Camden/local-presence, local-work, recent-work or completed-project claim.
- No `LocalBusiness`, `GeneralContractor` or `Organization` schema based on the trading name/address.
- No staffed-location claim for 15 Murray Street.
- No use of `03 4517 6915` as a verified NSW contact route.
- No fixed-price, response-time, workmanship guarantee or warranty term without a real written basis.
- No review, star rating, reviewer name or testimonial without the genuine text, identity and
  permission to publish.
- No “verified/reproduced/recorded” fidelity wording unless the cited source or record exists and has
  been sighted.
- No area-served claim based only on where suburb pages exist.
- No photograph presented as Camden work, customer evidence or a named NSW place unless it supports
  that claim and publication rights are recorded.

### Critical path

1. **[OWNER] O1/O2/O3:** settle accountable entity, operating/referral model, signed NSW operator,
   licence/insurance disposition, phone and address/staffing. If this does not happen, honest Wave 1
   remains zero.
2. **[AGENT] A1–A13:** repair architecture/readiness, staging plan and gates before relying on any GO.
3. **[OWNER] O6/O11:** attest the service matrix and authorise/supply service copy.
4. **[OWNER] O4/O5/O12:** settle real service areas, pricing and unsupported marketing-claim
   disposition.
5. **[OWNER] O7:** complete at least Bands A and C; Band D remains for a complete sighting.
6. **[AGENT] A14–A25:** rewrite active copy, reconcile figures and remediate imagery/brand/D32.
7. **[OWNER] O8/O9/O10/O13/O14:** Liverpool source, Gallery, privacy/form decisions, approvals and
   calculator outline.
8. **[AGENT] A26–A33:** runtime-test transformations, build calculator/privacy integration, schema,
   forms, menus and post-import actions.
9. **[AGENT] A34:** clean authoritative PHP 8.3 staging import with rollback and exact verification.
10. **[AGENT + OWNER] A35:** automated and human-sighted QA; page-by-page readiness remains `no`
    until evidence is recorded.
11. **[OWNER] O15:** explicit release/deploy/indexing approval.
12. **[AGENT] A36:** deploy only the approved minimum, then sitemap/indexing after GO.

## 6. Final state of this inspection

```text
immutable hashes       7/7 MATCH
existing active pages  76 (75 main + privacy)
planned calculator      1 (absent)
logical active total   77
readiness rows         157, DEFECTIVE — privacy omitted
index-ready             0
preflight               NO-GO
fabricated testimonials 0
phase started           none
import/deploy            none
```

The next safe action is not an import. It is owner resolution of identity/operator scope while the
agent repairs the readiness/import/gate contracts and removes unsupported marketing claims from the
Wave 1 brief.

## Appendix A — exact newly surfaced record/job constructions

Every quotation below is copied from a visible Elementor text field. Nothing is abbreviated.

### `/concreters-austral/` — publish

> For Austral, the verified project record says: Austral is not a masterplanned estate — it is old five-acre market-garden blocks being cut up lot by lot. That produces work no growth-corridor estate produces: 40–60 metre battle-axe handle driveways, double crossovers for dual occupancies, and second-dwelling slabs squeezed behind an existing house. Volume per job is high, access is usually terrible, and the pour almost always needs a line pump.

> For Austral, the verified project record says: Reactive clay with variable historic fill from decades of market-garden use. Undocumented fill is common — test before you assume a Class M site.

> For Austral, the verified project record says: Liverpool City Council vehicle crossing application — a different process and fee schedule to Camden. Dual occupancies typically require the crossing to match the approved parking facility on the DA or CDC.

> The researched Austral job record contains Long battle-axe handle driveways, Dual occupancy double crossovers, Granny flat and secondary dwelling slabs and Rear-yard hardstand and shed slabs. These Austral examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-bringelly/` — draft

> For Bringelly, the verified project record says: Bringelly is the closest residential locality to the Aerotropolis build-out. Western Sydney International opens to freight from July 2026 and passengers in October 2026, and private project value around the Aerotropolis has risen from $9.8bn to $21.6bn in fourteen months. That reshapes the work here from domestic driveways to industrial floors, hardstands and yard slabs — and toward B2B clients who tender rather than take a homeowner quote.

> For Bringelly, the verified project record says: Rural profiles with documented sulfate concentrations near creek lines in western Sydney. Salinity and aggressivity assessment under AS 2159 is a real input on industrial slabs here, not a formality.

> For Bringelly, the verified project record says: VERIFY the governing LGA per lot on the NSW Planning Portal before quoting. Industrial slabs typically sit under DA conditions rather than a standalone driveway application.

> The researched Bringelly job record contains Industrial and warehouse floor slabs, Truck hardstands and yard slabs, Rural access driveways and Shed and workshop floors. These Bringelly examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-catherine-field/` — draft

> For Catherine Field, the verified project record says: Catherine Field is mid-transition. On one street you're pouring a 4.5m urban crossover to Camden's 32 MPa / 125mm / SL72 standard; two streets over you're on an RU acreage lot where Council requires a standard concrete dish crossing aligned to the table drain invert and a bitumen shoulder seal back to the existing pavement. Two completely different specs in the same suburb.

> For Catherine Field, the verified project record says: Shale clay, engineered fill in the new releases, undisturbed profile on the remaining acreage. Rural lots often need a longer, thicker access section to carry delivery and machinery traffic.

> For Catherine Field, the verified project record says: Urban lots: Camden Standard Residential Driveway Crossing Application. Rural lots: rural residential driveway spec with dish crossing; pipe crossings only by Council approval.

> The researched Catherine Field job record contains New-release urban driveways and crossovers, Long rural access driveways with dish crossings, Machinery and shed hardstand on acreage and Alfresco slabs. These Catherine Field examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-cobbitty/` — draft

> For Cobbitty, the verified project record says: Cobbitty is where Camden's rural driveway specification actually bites. There's no kerb and gutter on most frontages, so Council requires a standard concrete dish crossing aligned to the table drain invert, plus a bitumen shoulder seal from the dish back to the edge of the existing road pavement. A pipe crossing is only permitted where a dish won't provide suitable access, and only with Council approval. That's three separate scope items most quotes leave off.

> For Cobbitty, the verified project record says: Undisturbed shale and alluvial profiles, no engineered fill. Long access runs need a thicker section and proper crossfall to survive delivery trucks and machinery.

> For Cobbitty, the verified project record says: Rural residential driveway specification via Camden Council. Dish crossing standard; pipe crossing by approval only. Bitumen shoulder seal required.

> The researched Cobbitty job record contains Long rural access driveways, Dish crossings and shoulder seals, Machinery shed floors and hardstands and Stable and workshop slabs. These Cobbitty examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-currans-hill/` — draft

> For Currans Hill, the verified project record says: Currans Hill was one of the first 1990s Camden subdivisions and its lots are noticeably smaller than Mount Annan or Harrington Park. Driveways are short, single-width and heavily trafficked, and the common failure is settlement at the layback rather than mid-slab cracking — which changes whether you're repairing the crossover or the driveway.

> For Currans Hill, the verified project record says: Shale clay, compact lots, tight side access.

> For Currans Hill, the verified project record says: Camden Standard Driveway Crossing Application where the crossover is altered or widened.

> The researched Currans Hill job record contains Short driveway replacement, Crossover and layback repair, Side path and gate access and Small shed slabs. These Currans Hill examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-edmondson-park/` — draft

> For Edmondson Park, the verified project record says: Edmondson Park is the densest suburb in this corridor — terraces, townhouses and small lots rather than 450sqm detached blocks. The jobs are small, access is tight, and a meaningful share of the work is strata: common-area paths, bin-store slabs and shared driveway aprons where the client is a strata committee, not a homeowner. Different sales cycle, different insurance requirements, repeat work if you do it well.

> For Edmondson Park, the verified project record says: Clay over shale on engineered fill. Tight access means barrow, kibble or line pump on most jobs — factor it into the quote rather than discovering it on the day.

> For Edmondson Park, the verified project record says: Liverpool City Council vehicle crossing application. Strata common property works need owners corporation approval and usually a committee resolution before you start.

> The researched Edmondson Park job record contains Compact single driveways and aprons, Courtyard and alfresco slabs, Strata common-area paths and bin store slabs and Shared driveway repair. These Edmondson Park examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-elderslie/` — draft

> For Elderslie, the verified project record says: Elderslie homes are mostly 2000s-era, which puts their concrete in an awkward middle age — old enough that owners are ready to upgrade the outdoor areas, young enough that the driveway itself is usually still structurally sound. The work here skews to adding rather than replacing: alfresco slabs, pergola bases, extended side access.

> For Elderslie, the verified project record says: Shale clay transitioning to Nepean alluvial closer to the river. Check flood mapping on the lower lots.

> For Elderslie, the verified project record says: Camden Standard Driveway Crossing Application for new or altered crossovers.

> The researched Elderslie job record contains Alfresco and pergola slabs, Side access and path extensions, Driveway widening and Shed slabs. These Elderslie examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-gledswood-hills/` — publish

> For Gledswood Hills, the verified project record says: Parts of Gledswood Hills back onto the South Creek riparian corridor and the Sydney Water Upper Canal. Sulfate and chloride levels in subsoil near western Sydney creek lines can be aggressive to concrete and reinforcement — this is the suburb where the Western Sydney Salinity Code of Practice and the CCAA saline-environments guide actually change the mix and the cover you specify, not just the paperwork.

> For Gledswood Hills, the verified project record says: Clay over shale, larger lots (350–600sqm), some Cumberland Plain Woodland conservation overlays restricting access and requiring line-pump or boom-pump placement rather than direct chute.

> For Gledswood Hills, the verified project record says: Camden Council Standard Driveway Crossing Application. Check estate design guidelines for permitted driveway finishes before quoting a plain broom finish.

> The researched Gledswood Hills job record contains Exposed aggregate driveways on premium lots, Pool surrounds and coping, Large alfresco and outdoor kitchen slabs and Pumped pours where tree protection restricts truck access. These Gledswood Hills examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-gregory-hills/` — publish

> For Gregory Hills, the verified project record says: Gregory Hills is the one Camden growth suburb where residential and light-industrial work sit side by side. The Turner Road business precinct and the Smeaton Grange estate next door mean forklift-rated slabs, loading-dock aprons and truck hardstands are quoted off the same drive as a domestic driveway — different mix design, different reinforcement, different jointing.

> For Gregory Hills, the verified project record says: Shale-derived clay on engineered fill. Commercial hardstand areas need subgrade CBR testing and a thicker reinforced section than a residential driveway — do not quote a warehouse apron off a residential rate.

> For Gregory Hills, the verified project record says: Residential: Camden Council Standard Driveway Crossing Application. Commercial/industrial: Non-Standard Driveway Application, plus any DA conditions attached to the site.

> The researched Gregory Hills job record contains Residential driveways on the more affordable Dart West stock, Warehouse and factory floor slabs, Loading dock aprons and truck hardstands and Carpark slabs and kerbing. These Gregory Hills examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-harrington-park/` — publish

> For Harrington Park, the verified project record says: Under the Harrington Grove schedule of the Camden DCP, a driveway must be built across its full width in stencilled or stamped concrete, clay pavers or exposed aggregate — no portion may be uncoloured concrete. Width is 3m to 5.5m, average grade 1:6, and it must sit at least 500mm clear of kerb drainage structures and side fencing. Anyone quoting you a plain broom finish here has not read the controls.

> For Harrington Park, the verified project record says: Established suburb on shale-derived clay. The 1990s–2000s driveways are now at 20–30 years and showing edge failure, settlement at the crossover, and cracking where the original slab was under-reinforced by today's standards.

> For Harrington Park, the verified project record says: Camden Council Standard Driveway Crossing Application for a new or altered crossover. Like-for-like replacement inside the property boundary generally does not, but confirm before starting.

> The researched Harrington Park job record contains Full driveway removal and replacement, Decorative upgrades from plain to exposed aggregate or stencil, Pool surround replacement and Crossover repair where the layback has settled. These Harrington Park examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-leppington/` — publish

> For Leppington, the verified project record says: Leppington straddles the Camden and Liverpool council boundary. Two lots on opposite sides of the same street can require two different crossover applications, two fee schedules and two inspection processes. Check the lot on the NSW Planning Portal before quoting.

> For Leppington, the verified project record says: Reactive Wianamatta clay with Upper South Creek drainage running through parts of the suburb. Flood-affected streets have a specified flood planning level that governs slab height and fall — this is a design input, not an afterthought.

> For Leppington, the verified project record says: Camden Council Standard/Non-Standard Driveway Crossing Application OR Liverpool City Council vehicle crossing application, depending on which LGA the lot falls in.

> The researched Leppington job record contains High-volume new-build driveways across the 2016–present release area, Crossovers for house-and-land handovers, Alfresco slabs and Retaining and stepped driveways on the Ingleburn Road grade. These Leppington examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-mount-annan/` — draft

> For Mount Annan, the verified project record says: Mount Annan was built out through the 1990s, which means its concrete is now 25 to 30 years old — the exact age where original driveways start failing at the edges and settling at the layback. Almost nothing here is a new pour. The question homeowners actually ask is whether to resurface or replace, and the honest answer depends on whether the failure is surface-level or structural.

> For Mount Annan, the verified project record says: Shale clay, sloping topography in parts. Original 1990s driveways were often poured thinner and with less reinforcement than current Camden spec, which is why edge cracking is the dominant failure mode.

> For Mount Annan, the verified project record says: Like-for-like replacement inside the boundary generally doesn't need a new crossing application, but a widened or relocated crossover does — Camden Standard Driveway Crossing Application.

> The researched Mount Annan job record contains Full driveway removal and replacement, Resurfacing and overlays where the base is sound, Path and side-access renewal and Shed and pergola slabs. These Mount Annan examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-narellan/` — draft

> For Narellan, the verified project record says: Narellan is the LGA's commercial spine. Smeaton Grange sits directly north and Narellan Town Centre anchors the retail strip, which means the highest-value jobs here aren't driveways — they're carpark slabs, loading aprons and warehouse floors that have to be poured overnight or in staged sections so the tenancy keeps trading.

> For Narellan, the verified project record says: Established shale clay. Older residential driveways from the 1980s–90s are at end of life. Commercial subgrades need CBR verification, especially where existing pavement is being broken out.

> For Narellan, the verified project record says: Camden Council Standard Driveway Crossing Application for residential. Commercial and industrial crossings use the Non-Standard Driveway Application.

> The researched Narellan job record contains Retail and industrial carpark slabs, Loading dock aprons, Established-home driveway replacement and Kerb and channel, wheel stops, line-marked bays. These Narellan examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-oran-park/` — publish

> The researched Oran Park job record contains Two-car driveway and crossover at handover (350–450sqm lots), Alfresco and side-path slabs post-handover, Colorbond shed slabs in rear yards and Exposed aggregate upgrades on the Hermitage releases. These Oran Park examples describe the supplied job mix rather than a claim about an unverified project.

### `/concreters-spring-farm/` — draft

> For Spring Farm, the verified project record says: Spring Farm sits on genuinely sloping ground, and that is what makes it different from the flat growth-corridor releases. Camden requires an average driveway grade of 1:6 with controlled vertical curves — on a steep Spring Farm block you either engineer the grade properly or you lodge a Non-Standard Driveway Application. Blocks here regularly need stepped pours, integrated retaining and a scratch or broom finish for traction rather than a smooth decorative one.

> For Spring Farm, the verified project record says: Shale clay on graded fill benches. Retaining and drainage behind the driveway matter more here than anywhere else in the LGA — water tracking behind a slab on a slope is the failure mode.

> For Spring Farm, the verified project record says: Camden Standard Driveway Crossing Application where the grade complies; Non-Standard Driveway Application where it cannot, with an explanation of why the standard spec can't be met.

> The researched Spring Farm job record contains Stepped and graded driveways, Concrete retaining and edge beams, High-traction finishes on steep approaches and Terraced alfresco slabs. These Spring Farm examples describe the supplied job mix rather than a claim about an unverified project.
