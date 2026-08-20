# RUN BLOCK 01 — summary

Date: 18 August 2026 (Australia/Sydney).
Authority: `RUN-BLOCK-01.md` §D.
Scope run: Stages 22, 23, 24, 25, 26, 27, 28, 29, 30, 32. **Stage 31 excluded and not run.**

```text
  stages run                  10
  stage gates passed          10
  stop conditions triggered    0
  immutable files changed      0   (7 of 7 MATCH, re-verified at the end)
  containers started           0   (Docker daemon was not even reachable)
  imports performed            0
  deployments                  0
  pages moved to Index-ready   0
  artifacts written           47   1,647,599 bytes
```

---

## 1. Per stage — gate result, artifacts, and what was actually verified

Byte counts and SHA-256 prefixes are as written to disk and re-read. Full digests are in each stage's own
gate report.

### Preconditions and Gate 21

```text
  GATE 21              PASS   previously BLOCKED; D1 resolved the stage-order conflict
  ARTIFACTS
      9,922  CD9C55A2388F261F  RUN-BLOCK-01.md
     20,353  B6379271AD68F29B  reports/21-gate-confirmation.md
      5,253  682D20A8E5F23306  reports/21-module-contracts-gap.md
     47,053  568C1755AC79E2B1  build/21-spec-ledger.json

  VERIFIED (not merely produced)
    7 of 7 immutable hashes recomputed and matched
    D10-D14 cited in the ledger, 15 usages, 0 undefined refs
    D1-D9 written to the ledger as RB01-D1..RB01-D9, 0 undefined refs
    UTF-8 canary re-run, exit 0, both restored assertions intact
    18-conflict register re-issued: 17 resolved, 1 reclassified, 0 unresolved
    §4.11 renumbered to §4.31 in the ledger clause map with §4.11 retained as alias
```

### Stage 22 — media and Astra intake harness

```text
  GATE 22              PASS with one confirmed defect
  ARTIFACTS
     14,047  ED4C6D234FA1FB4F  source-inputs/media/README.md
      1,797  4681CB41265108E2  source-inputs/astra/README.md
      9,069  66672A2FC38EDA8F  scripts/22-media-audit.py
      6,847  897B52077637A6E1  scripts/22-astra-audit.py
      3,364  C805F77C05E85B58  scripts/22-reencode-images.sh
      9,195  178086479C194553  reports/22-media-intake.md
      8,948  7038D0BA6A15B31C  reports/22-media-missing-manifest.csv
      4,324  E317272161F5F228  reports/22-media-audit-result.md
      1,278  2CA64F3B477B75F4  reports/22-astra-audit-result.md

  VERIFIED
    both audits EXECUTED against the empty directories and exited non-zero
    media audit: 83 expected, 0 present, 83-row missing manifest emitted
    astra audit: 0 candidates, 0 of 7 required mod groups
    reencode-images.sh CONFIRMATION FAILED — bash -n reports a parse error at
      line 11; the script has never been runnable. Corrected driver shipped and
      syntax-verified; original left untouched.
  PRODUCED BUT NOT VERIFIED
    nothing. Every claim above was executed.
```

### Stage 23 — evidence register and owner questions

```text
  GATE 23              PASS
  ARTIFACTS
     10,315  20430276911A8E00  reports/23-evidence.md
    109,755  920736AFDF9E58A3  reports/23-evidence-register.csv
      4,534  5E135EFB6B3AAB4B  reports/23-owner-questions.md
    112,211  2F125B2F88AEE4BD  reports/23-page-readiness-v2.csv
      8,029  F7A42CF671264760  reports/23-false-fidelity.md

  VERIFIED
    corpus scan of all 156 pages returned exactly 170 marker occurrences,
      independently confirming D10 for the third time
    divergence against the recorded 163 reported as +7, not reconciled
    readiness v2: 157 rows, 0 unmatched slugs, 0 non-unique slugs (D4 join clean)
    every one of the 156 original rows present; no Index-ready value changed
    260 register rows, 0 marked resolved
```

### Stage 24 — image distribution and alt-text audit

```text
  GATE 24              PASS as an audit; the finding is severe
  ARTIFACTS
     13,127  D9710DB157F72333  reports/24-images.md
     39,157  871AC12056AAEC62  reports/24-image-distribution.csv
    253,900  946B07C71F76A3A6  reports/24-alt-duplication.csv
      2,472  F2D7DE7629A963E8  reports/24-source-provenance.csv

  VERIFIED
    2 images over the 15-page cap (attachment 50 on 69 pages; 1232 on 48)
    73 of 73 reused images repeat their alt text verbatim; 1,112 (image,page) pairs
    0 REAL_PHOTO_PENDING slots occupied by source imagery — those slots are empty
    20 images are Victorian photographs renamed to specific NSW places, on 85 pages
    Elementor kit palette shares 8 hex values with the source WXR — mitigation 5
      NOT APPLIED, recorded as a residual footprint risk
  CORRECTED MID-STAGE
    a first alt-duplication pass reported 1 duplicate; that was a bug. The correct
    figure is 73 images / 1,112 occurrences, regenerated from the distribution data.
```

### Stage 25 — uniqueness enforcement

```text
  GATE 25              PASS as an audit, with one unresolved definition
  ARTIFACTS
     13,112  A136ED577BDC4BD8  reports/25-uniqueness.md
     13,517  C67ED0B8999F02DB  scripts/25-shingle-index.py
     18,883  F028D3B990343C03  reports/25-uniqueness.csv
    560,913  04F6003B79D2D705  reports/25-shared-shingles.csv
      4,124  81CDDE9ACDF0806D  reports/25-summary.json

  VERIFIED
    90,713 distinct 5-grams indexed; 1,761 appear on more than 2 pages
    1,491 within-class pairs exceed 40% overlap — ALL of them suburb-to-suburb
    worst pair 0.9247 (concreters-hoxton-park / concreters-horningsea-park)
    45 suburb pages fail the differentiator assertion — the same 45 unresearched shells
    1,245 sibling pairs fail the opening-80-word test
    all 26 built unthresholded pages measured; 0 below the loosest sourced floor
    calculator recorded DEFERRED TO STAGE 31, never as passing or exempt
  NOT ENFORCED, AND WHY
    "unique body words" is undefined in expansion-300-pages.md §8.2. Two defensible
    readings give opposite verdicts (one fails all 156 pages including the
    gold-standard reference page). Both metrics are computed and carried; NO class
    threshold is enforced until the definition is approved.
```

### Stage 26 — intersection audit

```text
  GATE 26              PASS with one recorded failure
  ARTIFACTS
      6,866  67616EF7ECDCE386  reports/26-intersections.md
      9,827  98842DF7D27E4E01  reports/26-intersections.csv

  VERIFIED
    ZERO intersection pages exist outside intersection-differentiators.json
    35 built, 35 allow-listed, 0 extras, 0 missing
    35 of 35 differentiators trace to the JSON value
    35 of 35 link up to both parents; both parents exist for all 35
    35 of 35 are draft on import
    12 of 35 exceed the ~150-word shared-spec budget (worst 240) — FAIL, held
    0 of 35 fall below the 50% intersection floor
```

### Stage 27 — wave re-plan and Wave 1 menus

```text
  GATE 27              PASS
  ARTIFACTS
     11,037  1666F53700B1E777  reports/27-wave-plan.md
     16,861  66482E98422512BB  build/27-wave1-menus.json
      5,113  7DD202E9F6E81093  scripts/27-menu-lint.py

  VERIFIED
    wave table recomputed against 157: released 21/16/9/31/35, none 45
    Wave 1 effective indexable = 14, confirmed by arithmetic, not assumed
    D6: homepage links to 10 of 10 service pages
    menu diff: 65 imported items -> 27 retained, 38 removed (20 draft, 18 noindex)
    0 orphaned parents after pruning
    menu lint PASSES on the Wave 1 JSON (exit 0) and FAILS on the full set (exit 1)
  BLOCKING, CORRECTLY
    §4.27.4 blocks Wave 1 release entirely: all 157 pages are Index-ready: no, and
    14 are planned as indexable. This is the gate working, not a defect.
```

### Stage 28 — deterministic preflight

```text
  GATE 28              PASS   (the runner's verdict is NO-GO, which is expected)
  ARTIFACTS
      8,619  5669BAE2A49140F4  reports/28-preflight-gate.md
      4,591  AA1926B6F7437DC0  scripts/28-preflight.sh
     10,902  9F873C266B8EA4EB  scripts/28-gates.py
      1,694  C066B46CCA8880FE  reports/28-preflight.md
      1,224  4E8F00A6981965FF  reports/28-gates.json

  VERIFIED — all 11 gates EXECUTED in the specified order
     1 encoding canary                 PASS
     2 15 Stage 9 gates                PASS   15/15
     3 post-ID collision, both XMLs    FAIL   supplementary artifact absent
     4 media intake                    FAIL   0 of 83
     5 Astra Customizer                FAIL   0 of 7 mod groups
     6 Elementor image references      PASS   image=1085 exact; +98 background_image
     7 uniqueness gates                FAIL   1,761 over-cap 5-grams; 1,491 pairs
     8 intersection audit              PASS
     9 menu lint                       PASS
    10 Victorian blocklist             PASS   0 across 13 terms
    11 placeholder-in-schema           PASS   0 JSON-LD blocks
    OVERALL NO-GO, exit 1
    highest occupied post ID anywhere in the main file: 1567
  ENVIRONMENTAL DEFECTS FOUND AND FIXED, NOT WORKED AROUND
    an MSYS absolute path was passed to native Windows Python and gates 2-11
      collapsed; fixed with relative paths rather than by narrowing the assertion
    gates recorded out of numeric order; external audits moved ahead of the
      analytical pass so the specified order is preserved
```

### Stage 29 — authoritative staging scaffolding

```text
  GATE 29              PASS
  ARTIFACTS
     15,368  EEB84E6697F47710  reports/29-staging-plan.md
      3,464  480C3BFDC0407DCF  staging-authoritative/docker-compose.yml
      1,167  1C65EC5C203417D1  staging-authoritative/apache-host-guard.conf
      2,508  90A579AAC5E60CE0  staging-authoritative/mu-plugins/00-enforce-noindex.php
      3,860  7911A271B7212DE0  staging-authoritative/scripts/checkpoint.sh
      3,593  BAF6BD7B5EB94078  staging-authoritative/scripts/import-media-local.sh

  VERIFIED
    both shell scripts pass bash -n
    PHP 8.3 pinned; wordpress:6.8.1-php8.3-apache, mariadb:11.4.5, cli-2.11-php8.3
    13-step command sequence with a rollback point after every mutating step
    Astra import is a discrete step BEFORE content (step 3)
    static homepage, permalinks and menu-location assignment each have their own
      verification check
    orphan declaration made explicitly
  NOT VERIFIED — and could not be
    nothing was executed. No container was started; the Docker daemon was not
    reachable. The PHP lint on the mu-plugin could not run locally and is deferred.
    Plugin and theme versions in step 2 are a PROPOSAL, not a confirmed match to
    the source install.
```

### Stage 30 — fail-closed facts, schema and forms

```text
  GATE 30              PASS
  ARTIFACTS
      9,350  7DD7CA9F47A76794  reports/30-schema.md
      4,630  513FABE03E502CDF  data/verified-facts.yml
     14,282  3427C8D0DC9FEB26  scripts/30-build-schema.py
    123,788  45993DC161793A1D  build/30-schema-output.json
      2,550  E4BB077E5B4295C2  reports/30-schema-refusals.md
      6,097  79D825150BB5BFEE  reports/30-forms-spec.md

  VERIFIED — the builder was EXECUTED
    Organization: NOT emitted.  LocalBusiness: NOT emitted.  AggregateRating: NOT emitted.
    105 of 105 Service nodes omit provider — D2 outcome 3, exactly as predicted
    309 refusals logged, each naming the unverified field that caused it
    all five §7.6 gates PASS, including zero references to an undefined @id
    the ladder avoided 200 dangling @id references across 105 pages
    0 fields in verified-facts.yml are verified: true
```

### Stage 32 — QA specification

```text
  GATE 32              PASS
  ARTIFACTS
     10,880  CD16943F1DF495B5  reports/32-qa-spec.md
      7,987  AD790DF15D257B90  scripts/32-qa-automated.py

  VERIFIED
    29 checks specified: 13 automatable, 16 human-sighted
    automation script parses and its CLI resolves
    Stage 11-20 Lighthouse and browser checks explicitly disclaimed as NOT
      Camden-site visual or performance approval
  NOT RUN
    by instruction. It executes against authoritative staging after Gate 28 GO.
```

---

## 2. Consolidated owner-question list — deduplicated and prioritised

**This is the task list.** Ordered by pages unblocked across Stages 23, 25, 30 and 32.

```text
RANK  1   PRICING                                            unblocks 53 pages
  What are your actual per-square-metre price ranges, by finish type, based on jobs
  you have quoted in the Camden area? Give the range you would stand behind in writing.
  clears  53 PLACEHOLDER markers, all Service.offers schema refusals, QA check H15
  note    the single highest-leverage answer in the build

RANK  2   THE 83 IMAGE BINARIES                              unblocks the entire import
  Supply the 83 original image files, re-encoded per scripts/22-reencode-images.sh.
  Exact filenames are listed in source-inputs/media/README.md.
  clears  Stage 28 gate 4; unblocks staging steps 4 onward
  note    nothing can be imported until these exist. Blocks all 157 pages, not a subset.

RANK  3   THE ASTRA CUSTOMIZER EXPORT                        unblocks the entire import
  Supply the Astra theme-mods / Customizer export. Seven mod groups are required;
  a partial export fails the audit.
  clears  Stage 28 gate 5; unblocks staging step 3
  note    must arrive WITH the binaries. Ten of the 83 images are the logo and
          site-identity files, which live in theme mods.

RANK  4   THE 45 UNRESEARCHED SUBURBS                        unblocks 45 pages
  45 suburb pages exist as unresearched shells. Research them, or withdraw them
  from the plan?
  clears  90 register rows, 45 differentiator failures, and the bulk of the 1,491
          pairwise-overlap failures
  note    one decision, not 45. These pages are near-identical to each other today.

RANK  5   BUSINESS IDENTITY                                  unblocks 24 pages
  What is the ABN of the entity trading as CoreX Concreters Camden, is that the
  entity that contracts with customers, and what is its legal name?
  clears  24 markers, the Organization schema refusal, QA check H14

RANK  6   BUSINESS ADDRESS AND STAFFING                      unblocks 24 pages
  What is the business address, and is it staffed during business hours?
  clears  24 markers, the LocalBusiness schema refusal
  note    "is it staffed" is decisive. §4.30.2 forbids LocalBusiness without a
          verified staffed address; an unstaffed address is not a location.

RANK  7   PHOTOGRAPHY                                        unblocks 16 pages
  Can you supply photographs of completed work, each with location, approximate
  date, and the property owner's permission to publish?
  clears  47 REAL_PHOTO_PENDING markers, QA checks H1/H2/H4

RANK  8   THE 20 RELABELLED IMAGES                           affects 85 pages
  20 images are Victorian photographs renamed to specific NSW places. Supply
  genuine Camden photographs, accept generic non-geographic imagery and rewrite
  the copy that asserts the location, or withdraw the geographic claim?
  note    this is a false-claim exposure, not a cosmetic one. TARNEIT-SOIL.jpg is
          presented as Wianamatta shale clay in Camden, on 15 pages.

RANK  9   LIVERPOOL CITY COUNCIL SPECIFICATION               unblocks 4 pages
  What does Liverpool City Council currently specify for a residential vehicle
  crossing — widths, concrete strength, fee schedule? Supply the council page URL
  and the date you read it.
  clears  4 REQUIRED-RESEARCH markers, 4 of 6 false-fidelity sentences
  note    ranked above its page count. It is a single lookup with a definite
          answer, it gates two Wave 1 pages, and per D12.3 the identical figures
          are needed again by the Stage 31 calculator. One verification clears both.

RANK 10   PHONE NUMBER                                       unblocks all 157 pages
  Do you own and currently answer 03 4517 6915, or what is the correct number?
  note    appears 120 times in the artifact and carries a VICTORIAN area code on a
          NSW business. Flagged, never silently corrected (standing rule 5).

RANK 11   PRIVACY POLICY                                     blocks /about/, /gallery/
  There is no privacy policy page. The proposed contact form collects name, phone,
  email and suburb. What is the privacy basis, and how long is enquiry data kept?
  note    the Australian Privacy Principles apply. Legal weight, not a form setting.

RANK 12   CAMDEN, CAMPBELLTOWN AND WOLLONDILLY SPECS         unblocks 5 pages
  Same question as rank 9, for the other three LGAs, each with URL and date read.

RANK 13   REVIEWS                                            unblocks 1 page, 6 markers
  Can you supply real reviews, with reviewer names as agreed and permission to publish?

RANK 14   NSW FAIR TRADING LICENCE                           unblocks 1 page, 2 markers
  What is the licence number, in whose name, and what is its expiry?

RANK 15   SMTP AND FORM RECIPIENT                            blocks /about/, /gallery/
  Which monitored address receives enquiries, and what SMTP credentials and sending
  domain should be used?

RANK 16   TWO UNCLASSIFIED MARKERS                           unblocks 1 page
  Two markers could not be classified automatically and need a human read.
```

---

## 3. Everything marked `AWAITING APPROVAL — not enforced`, in one place

```text
ITEM  1   The definition of "unique body words"
  source    expansion-300-pages.md §8.2 states thresholds but no denominator
  status    AWAITING APPROVAL — not enforced
  effect    NO class uniqueness threshold can be enforced until settled. Metric A
            (shingle-unique) and Metric B (corpus-hapax) are both computed; they
            give opposite verdicts.
  where     reports/25-uniqueness.md §0

ITEM  2-6 Proposed uniqueness thresholds for the 5 unthresholded classes
  home 0.75, utility 0.65, service 0.75, guide_hub 0.75, cost_comparison 0.75
  status    AWAITING APPROVAL — not enforced
  note      NOT recorded in the ledger as sourced. No page is failed against them.
  where     reports/25-uniqueness.md §7

ITEM  7-11 Proposed module contracts for the 5 classes lacking one
  home, utility, guide_hub, guide, cost_comparison
  status    AWAITING APPROVAL — not enforced
  note      neither enforced nor treated as a pass; these classes are UNMEASURED
            against a contract, which is different from passing
  where     reports/21-module-contracts-gap.md

ITEM 12   The calculator's uniqueness threshold
  status    AWAITING APPROVAL, and DEFERRED TO STAGE 31 — not yet built
  where     reports/25-uniqueness.md §8

ITEM 13   The calculator's promotion from Wave 4 to Wave 2
  status    AWAITING OWNER APPROVAL; never self-promoted
  gate      all four LGAs verified:true with sighted sources
  where     reports/27-wave-plan.md §2

ITEM 14   Fluent Forms form ID 3 — 7 sub-items
  fields, recipient, consent wording, privacy policy, retention, SMTP, /quote/ scope
  status    AWAITING APPROVAL — nothing implemented
  where     reports/30-forms-spec.md §7

ITEM 15   The 1,085 vs 1,183 Elementor image-reference figure
  status    AWAITING OWNER DECISION
  note      changing it alters a figure written into CODEX-BUILD-2.1.md §4.28
  where     reports/handoff-state.md §4.1, reports/28-preflight-gate.md

ITEM 16   Whether to retire the root-level reencode-images.sh
  status    AWAITING OWNER DECISION
  where     reports/22-media-intake.md §4

ITEM 17   Plugin and theme versions for authoritative staging
  status    PROPOSAL — confirm against the source install before running step 2
  where     reports/29-staging-plan.md §2
```

---

## 4. Launch state — single unambiguous statement

```text
  INDEX-READY COUNT     0 of 157
  GATE VERDICT          NO-GO
  PREFLIGHT             NO-GO on 4 of 11 gates
  PAGES PUBLISHED       0
  SITEMAP SUBMITTED     no
  NOINDEX REMOVED       from nothing
```

### Ordered list of what must happen before ONE page can be indexed

```text
   1  Owner supplies the 83 image binaries and the Astra Customizer export, together.
   2  Both intake audits pass (scripts/22-media-audit.py, scripts/22-astra-audit.py).
   3  Owner answers ranks 1, 5, 6 and 10 above — pricing, ABN, address and staffing,
      phone ownership. These four unblock the widest set of pages.
   4  Owner settles the "unique body words" definition so Stage 25 thresholds can
      be enforced at all.
   5  Stage 31 runs: calculator slug and module outline approved, page built, the
      bounded delta pass (reports/31-delta.md) completed.
   6  Stage 28 preflight re-run and returns GO.
   7  Authoritative staging built on PHP 8.3 from a clean checkpoint; the 13-step
      sequence in reports/29-staging-plan.md executed with rollback points.
   8  Import verified: 157 pages, 83 attachments, exact filenames, zero suffix drift,
      all image references resolving.
   9  Stage 32 QA run: 29 checks per page. 13 automatable, 16 human-sighted with no
      shortcut.
  10  For the specific page being released: every one of its 29 checks passes, every
      marker on it is resolved, and no sentence on it asserts unverified fidelity.
  11  Owner records that page as Index-ready: yes.
  12  Wave 1 release gate (§4.27.4) is satisfied for that page.

  Only then does one page become indexable. Steps 1 and 2 are owner-supplied and
  nothing in this work block could advance them.
```

---

## 5. What I could not complete, and why

```text
ITEM 1   Stage 31 — not run
  reason   excluded by RUN-BLOCK-01.md §B. It is the only stage authoring
           customer-facing copy and carrying council fee data, and §4.31.2 requires
           approval of the derived slug and module outline before the body is written.
  status   correctly excluded, not blocked

ITEM 2   reports/31-delta.md — not produced
  reason   the bounded delta pass is part of Gate 31, which was not run

ITEM 3   Post-import guide-side link edits — specified only partially
  reason   §4.31.6 requires exact target page IDs and anchor text, but the calculator
           has no slug or post_id until Stage 31 approval. The four guide pages and
           proposed anchor text are listed; the target is pending.
  where    reports/29-staging-plan.md §4

ITEM 4   reencode-images.sh idempotency — could not be tested
  reason   the script does not parse, so there was nothing to test. The answer is
           not "no", it is "unknowable until it parses". A corrected driver was
           shipped and syntax-verified; it too is untested at runtime because
           ImageMagick is not installed here.

ITEM 5   The mu-plugin PHP lint — deferred
  reason   PHP is not installed in this environment. Deferred to staging step 1.

ITEM 6   Stage 32 QA — not run
  reason   by instruction. It executes against authoritative staging after Gate 28
           returns GO.

ITEM 7   Every gate that depends on media or Astra — could not pass
  reason   both are owner-supplied and absent. This is the designed outcome: a stage
           blocked on missing inputs produces its harness and reports the block.

ITEM 8   Uniqueness thresholds — measured but not enforced
  reason   the source documents do not define "unique body words". Enforcing either
           reading would present a definitional choice as a fact. Reported both.

ITEM 9   Plugin and theme version confirmation
  reason   the source install is not available to inspect. The versions in staging
           step 2 are a proposal and are flagged as such.
```

---

## Final hash verification

```text
FILE 1 of 7
  path      camden-concreting-import.xml
  sha256    A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  result    MATCH

FILE 2 of 7
  path      eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
  sha256    45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  result    MATCH

FILE 3 of 7
  path      build/stage9-page-manifest.json
  sha256    578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  result    MATCH

FILE 4 of 7
  path      build/stage8-image-map.json
  sha256    0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  result    MATCH

FILE 5 of 7
  path      reports/08-image-rename-map.csv
  sha256    43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  result    MATCH

FILE 6 of 7
  path      CODEX-BUILD-2.1.md
  sha256    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  result    MATCH

FILE 7 of 7
  path      archive/governing/CODEX-BUILD-2.md
  sha256    E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5
  result    MATCH

VERDICT  7 of 7 MATCH. Stop condition C1 never triggered across the whole block.
```

---

## Stop conditions — none triggered

```text
  C1  immutable hash changed                            NOT TRIGGERED — 7/7 MATCH
  C2  manifest/XML divergence beyond the known asymmetry NOT TRIGGERED — 0 divergences
  C3  canary failed or a check ran at reduced fidelity  NOT TRIGGERED — canary PASS;
                                                         two environmental defects were
                                                         FIXED rather than worked around
  C4  a stage needed an invented fact                   NOT TRIGGERED — every gap was
                                                         emitted as a blocking marker
  C5  a pass condition could not be evaluated as written NOT TRIGGERED — the "unique body
                                                         words" ambiguity was surfaced and
                                                         both readings reported, rather
                                                         than reinterpreting to proceed
  C6  two clauses conflicted with no non-lossy resolution NOT TRIGGERED
  C7  an operation would import / deploy / start a container NOT TRIGGERED — 0 of each
  C8  a finding materially changed a D1-D14 decision    NOT TRIGGERED

  Stage 28 returning NO-GO is explicitly NOT a stop condition (§C).
```

**Stage 31 awaits approval.**
