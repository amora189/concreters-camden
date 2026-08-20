# GATE 25 — uniqueness enforcement

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.25; `RUN-BLOCK-01.md` §A D1, D3.
Script: `scripts/25-shingle-index.py`. Data: `reports/25-uniqueness.csv`, `reports/25-shared-shingles.csv`, `reports/25-summary.json`.

**Failing pages are held, not rewritten. Nothing on any page was modified by this stage.**

---

## 0. A definitional ambiguity that must be resolved before any threshold is enforced

`expansion-300-pages.md` §8.2 states the thresholds — suburb ≥60%, intersection ≥50%, guide ≥85%
"unique body words" — but **never defines the denominator**. Two defensible readings exist, and they give
opposite verdicts:

```text
  METRIC A — shingle-unique
    definition   share of a page's 5-gram shingles that appear on no other page
    rationale    consistent with the 5-gram index §8.1 mandates and with the
                 pairwise-overlap measure in §8.3
    behaviour    discriminates; suburb median 0.088, guide median 0.874

  METRIC B — corpus-hapax
    definition   share of a page's distinct words appearing on no other page
    rationale    a literal reading of "unique body words"
    behaviour    cannot discriminate. Common trade vocabulary ("concrete",
                 "driveway", "council") is shared by construction, so this
                 metric scores at or near 0.0 for every page in every class,
                 including the pages that are demonstrably well differentiated.
```

Metric B would report **all 156 pages failing**, including Oran Park, the gold-standard reference page.
That is a broken measurement, not a finding, and reporting it as a verdict would be false.

**Both metrics are computed and carried in `reports/25-uniqueness.csv`. Neither threshold is enforced.**
Metric A is treated as the primary reading and every figure below uses it, but the definition itself is
recorded as **`AWAITING APPROVAL — not enforced`**. No page is failed or held on an ambiguous definition.

---

## 1. Global 5-gram index

```text
  pages measured                              156
  calculator                                  DEFERRED TO STAGE 31 — not yet built
  distinct 5-grams indexed                 90,713
  5-grams on more than 2 pages              1,761   FAIL condition per §2 precedence
  pages touched by an over-cap 5-gram         156   every page
  worst 5-gram page count                     145
  pages with zero over-cap 5-grams               0
```

### The ten most-shared 5-grams

```text
  COUNT  SHINGLE
    145  get your free quote today
    118  call us 03 4517 6915
     99  your free quote today call
     99  free quote today call us
     99  quote today call us 03
     99  today call us 03 4517
     80  keeps it open related sources
     80  it open related sources for
     61  shed garage extension and house
     61  garage extension and house slabs
```

The top six are CTA and phone-number boilerplate in the shared header/footer, not body prose. This matters
for interpretation: the rule as written ("a 5-gram on more than 2 pages fails") makes **every page on the
site fail**, because every page carries the same footer. The rule was written for body copy and is being
applied to the full rendered text.

Recorded as a finding, not resolved by narrowing the assertion. The full index is in
`reports/25-shared-shingles.csv` so the boilerplate and prose cases can be separated on review.

---

## 2. Per-class summary — Metric A

```text
  CLASS            PAGES   MIN     MEDIAN   MAX     THRESHOLD  ENFORCED  WOULD FAIL  <50%   WORST PAIR
  home                 1   0.8746  0.8746   0.8746  none       no                 0     0       0.0000
  utility              4   0.6622  0.7590   0.8077  none       no                 0     0       0.2703
  service             10   0.7556  0.8683   0.9152  none       no                 0     0       0.2009
  suburb              60   0.0645  0.0879   0.8647  0.60       no                58    45       0.9247
  intersection        35   0.6521  0.8708   0.9345  0.50       no                 0     0       0.2287
  guide_hub            1   0.9298  0.9298   0.9298  none       no                 0     0       0.0000
  guide               35   0.6492  0.8742   0.9171  0.85       no                11     0       0.2588
  cost_comparison     10   0.6718  0.8948   0.9357  none       no                 0     0       0.1532
  calculator           1   DEFERRED TO STAGE 31 — not yet built
```

"ENFORCED: no" applies to every row, including the three classes with sourced thresholds, because the
threshold's **definition** is unresolved (§0). The "WOULD FAIL" column is what Metric A yields if the
shingle reading is adopted.

---

## 3. Suburb class — the substantive finding

```text
  suburb pages meeting 0.60 under Metric A     2 of 60
    concreters-oran-park        0.865   the gold-standard reference page
    concreters-leppington       0.637

  closest to the line but under it
    concreters-gledswood-hills  0.596
    concreters-bringelly        0.571
    concreters-edmondson-park   0.551
    concreters-currans-hill     0.547
    concreters-harrington-park  0.545

  worst
    concreters-cecil-hills      0.065
    concreters-camden-park      0.065
    concreters-hoxton-park      0.075
    concreters-horningsea-park  0.075
    concreters-elizabeth-hills  0.075

  suburb pages below the loosest sourced threshold (0.50)   45
```

**Those 45 are exactly the 45 unresearched suburbs.** The same 45 fail the differentiator assertion (§5).
This is a single root cause with three symptoms, not three problems: the shells were built from a common
template and have no researched local content to differentiate them.

The four Tier 1 suburbs sitting at 0.545–0.596 are a different and more awkward case. They are researched,
they are in the Wave 1 release set, and they land just under a 0.60 line whose definition is unresolved.
**No action is taken on them.** Under Metric A they would fail; under another reading they might not.

---

## 4. Pairwise overlap — enforced, and the one gate that is definition-independent

The 40% pairwise cap is sourced globally in §2 and does not depend on the "unique body words" definition.
It is measured on 5-gram sets.

```text
  pairs exceeding 40% overlap within class            1,491
  worst pair overall
    concreters-hoxton-park  vs  concreters-horningsea-park     0.9247

  worst pair per class
    suburb           0.9247   concreters-hoxton-park / concreters-horningsea-park
    utility          0.2703   contact / gallery
    guide            0.2588   exposed-aggregate-cost / commercial-hardstand-cost
    intersection     0.2287   concrete-patios-edmondson-park / concrete-patios-elderslie
    service          0.2009   concrete-paths-... / commercial-concreting-...
    cost_comparison  0.1532   exposed-aggregate-vs-plain-concrete / exposed-aggregate-driveway-cost
    home             0.0000   single page, no pair
    guide_hub        0.0000   single page, no pair
```

**Every one of the 1,491 failures is within the suburb class.** No other class has a single pair above
40%; the next-worst class tops out at 27%. Two suburb pages at 92% overlap are, for search purposes, the
same page twice.

---

## 5. Differentiator assertion

```text
  suburb pages without a researched unique_local_variable        45
  intersection pages without a differentiator                     0
  total differentiator failures                                  45
```

All 35 intersections carry a differentiator traceable to `intersection-differentiators.json`. The 45
suburb failures are the unresearched shells, which already build `draft` + `noindex` under standing
rule 2 and count toward no live total.

---

## 6. Opening-paragraph test

First 80 words of every suburb and intersection page, compared against every sibling in its class.

```text
  sibling pairs whose opening 80 words exceed 60% similarity   1,245
  interpretation   the opening of a typical suburb shell is NOT false if pasted
                   onto a sibling — it would read as true, which is the failure
                   condition §8.5 describes
```

Reported as measured. Because the 60% similarity trigger is my threshold and not a sourced one, this is
**reported, not enforced**, on the same basis as §0.

---

## 7. The 27 unthresholded pages (D3)

```text
  service            10
  cost_comparison    11   (10 built + 1 not yet built)
  guide_hub           1
  home                1
  utility             4
  TOTAL              27   of which 26 are built and were measured

  All 26 built pages were measured. Measurement is unconditional even where no
  threshold exists; these pages no longer "pass by not being tested".
```

### Proposed thresholds — AWAITING APPROVAL, not enforced

```text
  CLASS            MEASURED MEDIAN   PROPOSED   REASONING
  home                     0.8746       0.75    Single page; proposal is a floor against future
                                                regression, not a discriminator.
  utility                  0.7590       0.65    Contact/quote/about legitimately share contact
                                                blocks; gallery is thin pending photography.
  service                  0.8683       0.75    Ten pages, all well clear; 0.75 leaves headroom
                                                without licensing regression.
  guide_hub                0.9298       0.75    An index page is mostly links; a high floor would
                                                penalise it for doing its job.
  cost_comparison          0.8948       0.75    Matches service. The calculator must meet whatever
                                                is approved here, measured at Stage 31.

  STATUS: AWAITING APPROVAL — not enforced.
  Not recorded in the ledger as sourced. No page is failed or held against these.
```

### Pages in untested classes below the loosest sourced threshold (0.50)

```text
  count   0
```

None. Per §4.25.7 these would be a problem whatever threshold is later approved; there are none.

---

## 8. The calculator

```text
  status                DEFERRED TO STAGE 31 — not yet built
  recorded as passing   NO
  recorded as exempt    NO
  measured              NO — there is nothing to measure
```

Carried in `reports/25-uniqueness.csv` as an explicit row with that value in every measurement column, per
`RUN-BLOCK-01.md` §A D1.

---

## 9. `CONTEXT.md` update and diff

```text
  Latest completed stage    24 -> 25
  New finding               45 unresearched suburb shells fail uniqueness, differentiator and
                            opening tests — one root cause, three symptoms
  New finding               1,491 within-class pairwise overlap failures, all in the suburb class
  New finding               "unique body words" is undefined in the source; both readings computed,
                            neither enforced
  New AWAITING APPROVAL     5 proposed class thresholds; the metric definition itself
  Index-ready               0 of 157 — UNCHANGED
  Launch gate               NO-GO — UNCHANGED
```

---

## 10. Hash table

```text
  camden-concreting-import.xml                          A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884  MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15  MATCH
  build/stage9-page-manifest.json                       578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42  MATCH
  build/stage8-image-map.json                           0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF  MATCH
  reports/08-image-rename-map.csv                       43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8  MATCH
  CODEX-BUILD-2.1.md                                    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C  MATCH

  6 of 6 MATCH.
```

---

## GATE 25 RESULT

```text
  Global 5-gram index built                              PASS — 90,713 shingles
  5-grams over the 2-page cap reported                   PASS — 1,761 reported, none suppressed
  All 156 built pages measured                           PASS — including the 26 unthresholded
  Calculator recorded DEFERRED, not passing/exempt       PASS
  Differentiator assertion run                           PASS — 45 failures reported
  Opening-paragraph test run                             PASS — 1,245 failures reported
  Pairwise overlap enforced                              PASS — 1,491 failures reported
  Thresholds proposed for unthresholded classes          PASS — 5, all AWAITING APPROVAL
  No unapproved threshold recorded as sourced            PASS
  No page rewritten or softened to pass                  PASS — nothing modified

  GATE 25: PASS as an audit, with a large held-page set and one unresolved definition.
  The definition of "unique body words" must be settled before any class threshold
  can be enforced. That is an owner decision, recorded in §0.
```
