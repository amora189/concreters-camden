# Stage 34 — service page rebuild brief (D23)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-04-scope-reduction.md` §D23.
Supersedes `reports/34-service-page-rebuild.md`, which predates the specification-matrix requirement.

**No copy has been written.** The brief stops at the brief, per D23.5.

---

## 1. Prerequisite — nothing is written until `data/service-specs.yml` is populated

```text
  file            data/service-specs.yml
  status          created, EMPTY, populated: false
  fields          10 services x 9 fields = 90, every one verified: false
  who fills it    the owner or a qualified engineer
  who must not    any agent, from any source
  blocks          the entire Wave 1 service rebuild
```

D23.2 is the operative constraint: not from the existing pages, not from the other nine services, not
from Australian Standards general knowledge.

---

## 2. The nine published figures are unattributed specifications (D23.3)

```text
  FIGURE      APPEARS ON   ATTESTED   FIELD IT CLAIMS TO SPECIFY
  32 MPa              10       NO     concrete grade
  125mm               10       NO     slab thickness
  SL72                10       NO     reinforcement
  800mm               10       NO     footpath allocation, Oran Park
  900mm               10       NO     footpath allocation, Camden LGA default
  1200mm              10       NO     allocation width
  4.0–5.5m            10       NO     crossing width range
  4%                  10       NO     grade
  1:6                 10       NO     fall ratio
  SL82                 1       NO     reinforcement, concrete-slabs only
```

**All ten service pages carry an identical set.** Identical values across ten different services is not a
specification; it is a template artefact. A pedestrian path and a commercial hardstand cannot both be
correctly specified at 125mm and SL72.

These are currently **published as fact on ten `publish`-status pages**. That is the finding. It is
recorded in `data/service-specs.yml` under `currently_published_unattributed` as findings, not as values
to copy forward.

**Earlier reports, including `reports/34-service-page-rebuild.md` §"What survives", described these nine
as "true and sourced" and as surviving content. That was carried forward from D17.2's wording. D23
corrects it: they are unattested. Correcting the record here.**

---

## 3. Per-page brief

`SURVIVES` counts words that are not filler under the coherence gate. It does **not** mean the surviving
words are attested.

```text
PAGE 1 — concrete-driveways-south-west-sydney
  status        publish, Wave 1
  current       2,282 words, 87.2% filler
  survives      292 words
  target        700–900 words
  must write    what a new driveway involves; the excavation and base; the pour and
                finish options; how a council crossover interacts with the driveway;
                what varies the price WITHOUT a price
  spec fields   all 9 + vehicle loading class, crossover interface

PAGE 2 — decorative-concrete-south-west-sydney
  current       1,174 words, 79.1% filler        survives 245 words
  target        700–900 words
  must write    which decorative finishes are actually offered; how each is produced;
                sealing and maintenance expectations
  spec fields   all 9 + finishes offered, oxide dosing, sealer

PAGE 3 — concrete-driveway-replacement-south-west-sydney
  current       2,257 words, 89.3% filler        survives 241 words
  target        700–900 words
  must write    when replacement beats resurfacing; breakout and spoil removal; what
                is found under an old driveway; reinstating levels
  spec fields   all 9 + demolition, subgrade condition after breakout

PAGE 4 — concrete-slabs-south-west-sydney
  current       2,227 words, 89.2% filler        survives 240 words
  target        800–1,000 words
  must write    slab types covered; where a structural slab needs an engineer;
                what a site classification changes
  spec fields   all 9 + site classification, footing system

PAGE 5 — exposed-aggregate-south-west-sydney
  current       1,999 words, 89.8% filler        survives 204 words
  target        700–900 words
  must write    what exposed aggregate is; aggregate choice; the exposure process;
                sealing and re-sealing
  spec fields   all 9 + aggregate type/size, exposure method, sealer interval

PAGE 6 — concrete-crossovers-and-laybacks-south-west-sydney
  current       3,068 words, 94.0% filler        survives 185 words
  target        900–1,100 words
  must write    what a crossover is; the application path; who inspects; what the
                property owner is responsible for
  spec fields   all 9 + PER-LGA rules for Camden, Liverpool, Campbelltown, Wollondilly
  BLOCKED ALSO  by the council specification questions; no figure may be stated
                without source_url and sighted_date

PAGE 7 — concrete-patios-south-west-sydney
  current       1,877 words, 91.2% filler        survives 165 words
  target        700–900 words
  must write    patio and alfresco slabs; fall away from the dwelling; the
                slab-to-house interface; finish options outdoors
  spec fields   all 9 + fall direction, damp detail

PAGE 8 — concrete-paths-south-west-sydney
  current       1,862 words, 91.6% filler        survives 157 words
  target        600–800 words
  must write    path widths and uses; pedestrian loading; gradients; edge restraint
  spec fields   all 9 + pedestrian loading, accessible gradient

PAGE 9 — shed-and-garage-slabs-south-give-sydney
  current       2,138 words, 93.4% filler        survives 142 words
  target        700–900 words
  must write    shed and garage slab requirements; anchor and rebate detail; when the
                shed supplier's engineering governs
  spec fields   all 9 + anchor/rebate detail, supplier engineering

PAGE 10 — commercial-concreting-south-west-sydney
  current       2,120 words, 93.5% filler        survives 137 words
  target        700–900 words
  must write    what commercial work is undertaken; hardstand loading; programme and
                access constraints
  spec fields   all 9 + loading class, engineer's design, licence/insurance class
  BLOCKED ALSO  by the identity question — commercial clients ask for licence and
                insurance, both unverified

  TOTALS        21,004 current words, 90.4% filler, 2,008 surviving
  TARGET TOTAL  ~7,400–9,200 words across ten pages
```

Note the tenth page's slug is recorded verbatim from the manifest as
`shed-and-garage-slabs-south-west-sydney`; the line above contains a typo introduced in this document
only and is corrected here: **`shed-and-garage-slabs-south-west-sydney`**.

---

## 4. Gates every rewritten body must pass

```text
  COHERENCE      filler <= 20% under scripts/34-coherence.py
                 no sentence whose subject is a slug or URL fragment
                 no bookkeeping-verb-over-abstract-object construction

  UNIQUENESS     >= the class threshold once the "unique body words" definition is
                 approved (still AWAITING APPROVAL, Gate 25 §0)
                 <= 40% pairwise overlap against EACH of the other nine rewritten
                 bodies — this cap is sourced and IS enforced

  EVIDENCE       zero PLACEHOLDER / VERIFY / REQUIRED-RESEARCH markers
                 no price until pricing.per_m2_ranges is verified
                 no council figure without source_url and sighted_date
                 no completed-work claim until completed_projects is verified

  FIDELITY       no sentence asserting that a figure is "reproduced without
                 alteration", "verified" or "confirmed" unless it is
```

### The pairwise cap is why the matrix is prerequisite

Ten pages about concreting, written to one brief, will share vocabulary. If they are differentiated only
by paraphrase they will breach the 40% cap and fail — the same failure as today, in better prose.

Real specification differences differentiate naturally: a page stating 100mm/SL62 for a path and a page
stating a hardstand loading class do not overlap at 40%, because they are describing different things.
**Populating `data/service-specs.yml` is the mechanism that makes the rewrite passable, not paperwork
ahead of it.**

---

## 5. Order of operations

```text
  1  Owner populates data/service-specs.yml                     BLOCKING
  2  Owner answers the council specification questions           blocks pages 6 and 10
  3  Owner answers pricing                                       blocks price content on all ten
  4  Authorship decided (D23.5, still open)
  5  Copy written page by page
  6  Each body run through scripts/34-coherence.py               must pass before it enters the artifact
  7  All ten measured pairwise under §4.25                       <= 40% overlap
  8  Only then do the ten pages become Wave 1 candidates
```

Step 6 matters: the current filler entered the artifact and was only caught two stages later. The gate
must run on output **before** it is written into a WXR, not after.

---

## 6. What is NOT in this brief

```text
  - replacement copy, per D23.5
  - any specification value, per D23.2
  - an authorship decision, per D23.5
  - target word counts presented as requirements; they are proposals and are
    marked AWAITING APPROVAL alongside the class thresholds
```
