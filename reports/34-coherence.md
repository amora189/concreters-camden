# GATE 34 — coherence scan

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-03-coherence-and-dispositions.md` §D15.
Artifacts: `scripts/34-coherence.py`, `reports/34-coherence.csv` (156 rows, 3 verbatim samples each),
`reports/34-coherence-summary.json`.

**Measured and reported. Nothing was fixed, rewritten or deleted.**

---

## THE EXTENT — the answer to D15.5

45 pages was a floor, as you expected. The real figure is **90 pages severely affected**, and the classes
involved are wider than the earlier scan suggested.

```text
  SEVERITY          PAGES   CLASSES
  SEVERE               90   service 10, intersection 35, guide 35, cost_comparison 10
  MODERATE             49   suburb 49
  BELOW THRESHOLD      12   suburb 11, guide_hub 1
  CLEAN                 5   homepage, about, contact, quote, gallery
  TOTAL               156

  corpus body words           181,571
  corpus filler words         149,686   82.4%
  filler words on SEVERE pages 145,064
```

**Guides (35) and cost/comparison pages (10) were not previously known to be affected.** The earlier
figure of 45 covered only service and intersection pages. D16 withdraws 35 intersections; that leaves
**55 SEVERE pages still in the architecture** — 10 service, 35 guide, 10 cost/comparison.

---

## The two populations — do not conflate them

The scan found two different problems, and a single percentage would have told you to scrap the
gold-standard page alongside the word salad.

### SEVERE — machine-generated word salad

The sentence subject is a slug or URL fragment. It asserts nothing that could be true or false.

```text
  /concrete-driveways-south-west-sydney/   (service, publish, Wave 1)
    "new-driveway scope records scope boundary; new-driveway scope identifies the record owner."
    "new-driveway scope records the exact; new-driveway scope identifies the record owner."
    "new-driveway scope cites work included; new-driveway scope keeps the basis explicit."

  /slab-volume-calculator/                 (cost_comparison, draft)
    "slab-volume-calculator-review states scope boundary; slab-volume-calculator-review flags the authority."
    "slab-volume-calculator-review maps work included; slab-volume-calculator-review preserves attribution."

  /campbelltown-council-driveway-crossing/ (guide, draft)
    "campbelltown-council-driveway-guide logs site identity; campbelltown-council-driveway-guide
     keeps the basis explicit."
```

### MODERATE — stilted prose carrying real content

Over-nominalised and awkward, but the subject is real and the content is checkable. **This needs an
editor, not a bin.**

```text
  /concreters-oran-park/    filler 14.5%  — BELOW the threshold, not flagged
    "The Oran Park evidence register identifies Oran Park Precinct DCP 2007, Oran Park Estate
     Design Guidelines and Camden Growth Centres LEP 2008 and records the local housing period
     as 2011–present, masterplanned."

  /concreters-leppington/   filler 23.0%
    "Post-handover shed and garage slabs in Leppington therefore start with the lot-specific
     level and the support beneath the proposed rear-yard footprint."
```

Those sentences name real instruments — DCP 2007, LEP 2008 — and make claims that could be checked and
could be wrong. That is the opposite of the SEVERE population.

---

## Detector design, and two corrections made during this scan

Five detectors per D15.1:

```text
  T1  slug subject             sentence subject is a slug or URL fragment
  T2  clause-head templating   4+ clauses in a block sharing a subject phrase
  T3  intra-sentence repeat    the same subject repeats inside one sentence
  T4  no verb of state/action  a clause of 8+ words with no finite verb
  T5  vacuous assertion        bookkeeping verb over an abstract object
```

**A sentence counts as filler only if it trips T1, T2, T3 or T5.** T4 alone is recorded but not counted.

### Correction 1 — the first run reported 85.5% and was wrong

T4 originally fired at 4 words and counted alone. It flagged legitimate site furniture:

```text
  "Call us - 03 4517 6915"              a CTA button label
  "Mon-Fri 9:00AM - 5:00PM"             opening hours
  "Side access, garden and front paths" a service-tile caption
```

It also missed real verbs, so *"Leppington straddles the Camden and Liverpool council boundary"* — good
prose — was flagged. Raising T4 to 8 words and requiring a substantive detector brought the corpus figure
from 85.5% to 82.4% and moved the homepage from 5.6% to 0.0%.

### Correction 2 — the utility pages were briefly reported SEVERE

`"Mon-Fri 9:00AM - 5:00PM"` matched the slug pattern, because `mon-fri` is hyphenated lowercase. One
flagged sentence on a 126-word page produced a 100% severe share. Fixed with a not-a-slug list and by
gating severity on the threshold. All four utility pages are now correctly **CLEAN**.

Both corrections are in the script as comments so the next agent does not re-introduce them.

---

## Validation against known-good pages

```text
  PAGE                      FILLER%   SEVERITY            READS AS
  /homepage/                 0.0000   CLEAN               correct
  /about/                    0.0476   CLEAN               correct
  /contact/                  0.0476   CLEAN               correct
  /quote/                    0.0517   CLEAN               correct
  /gallery/                  0.0556   CLEAN               correct
  /guides/                   0.0797   BELOW THRESHOLD     correct
  /concreters-oran-park/     0.1451   BELOW THRESHOLD     correct — the gold-standard page passes
  /concreters-mount-annan/   0.1577   BELOW THRESHOLD     correct
```

A detector that failed Oran Park would have been measuring the wrong thing. It passes.

---

## Worst pages

```text
  PAGE                                            CLASS             FILLER%
  camden-council-driveway-crossing                guide              0.9733
  driveway-cost-calculator                        cost_comparison    0.9717
  slab-volume-calculator                          cost_comparison    0.9716
  coloured-concrete-driveway-cost                 cost_comparison    0.9685
  exposed-aggregate-driveway-cost                 cost_comparison    0.9685
  plain-concrete-driveway-cost                    cost_comparison    0.9685
  stencilled-concrete-driveway-cost               cost_comparison    0.9685
  concrete-crossovers-and-laybacks-spring-farm    intersection       0.9583
  concrete-crossovers-and-laybacks-austral        intersection       0.9580
  concrete-crossovers-and-laybacks-leppington     intersection       0.9575
  concrete-driveway-cost-nsw                      guide              0.9571
  concrete-crossovers-and-laybacks-currans-hill   intersection       0.9557
```

---

## The gate is live and build-failing

Added to `build/21-spec-ledger.json` as `coherence_gate` and to `scripts/28-preflight.sh` as gate 12.

```text
  12. coherence gate (D15)   FAIL   90 pages SEVERE, 139 above threshold,
                                    corpus filler 0.8244 — no page above the
                                    threshold may enter any wave

  Stage 28 OVERALL: NO-GO   (now 5 failing gates, was 4)
```

The rule as recorded: **any page above the filler threshold cannot enter any wave, regardless of
uniqueness, evidence or media status.**

---

## Why no earlier gate caught this

```text
  Stage 9, 15 gates    measured structure, meta length, ID parity, duplication.
                       All 15 still pass. None inspects meaning.

  Stage 25 uniqueness  measured DIFFERENCE. It scored the filler pages among the
                       MOST unique on the site, because the slug token differs on
                       every page:
                           service pages       0.756 - 0.915
                           intersection pages  0.652 - 0.935
                       A page can be 90% unique and 100% unpublishable.

  Stage 24 images      looked at images.
  Stage 30 schema      looked at emitted JSON-LD, and correctly emitted almost none.
```

`camden-concreting-import.xml` has been structurally valid and substantively hollow since Stage 9, and
both have been true simultaneously the whole time. This is the specification defect D15 names, not an
execution error.

---

## Scope decision outstanding

D16 withdraws the 35 intersections. That leaves:

```text
  55 SEVERE pages remaining in the architecture
     10  service           Wave 1 critical path — D17 rebuild brief written
     35  guide             NOT addressed by any decision yet
     10  cost_comparison   NOT addressed by any decision yet

  49 MODERATE suburb pages  need editing, not rebuilding
```

**The 35 guides and 10 cost/comparison pages need a scope decision.** They are as severe as the
intersections that were withdrawn. I have not assumed a disposition for them.

---

## `CONTEXT.md` update and diff

```text
  Coherence gate            none -> build-failing, in ledger and preflight
  Pages SEVERE              45 (partial) -> 90 (full scan)
  Corpus filler             54.9% (partial) -> 82.4% (full scan, corrected method)
  Preflight failing gates   4 -> 5
  Architecture              157 -> 122 (D16)
  Index-ready               0 — UNCHANGED
  Launch gate               NO-GO — UNCHANGED
```

---

## Hash table

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

## GATE 34 RESULT

```text
  All 156 pages scanned                                    PASS
  Five detectors implemented per D15.1                     PASS
  Filler percentage per page reported                      PASS — reports/34-coherence.csv
  Three verbatim samples per flagged page                  PASS
  Nothing fixed, rewritten or deleted                      PASS
  Coherence added as a build-failing gate                  PASS — ledger + preflight gate 12
  Full extent reported before scope decision               PASS — 90 SEVERE, not 45

  GATE 34: PASS as an audit. The finding is that 90 of 156 pages carry
  machine-generated filler, and 55 of them remain in the architecture after D16.
```
