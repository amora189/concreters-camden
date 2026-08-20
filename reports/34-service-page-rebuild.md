# Stage 34 — service page rebuild brief

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-03-coherence-and-dispositions.md` §D17.

**No replacement copy has been written.** This is the brief only, per D17.3.

---

## Headline

```text
  service pages                 10
  current body words        21,004
  filler words              18,996   90.4%
  SURVIVING WORDS            2,008    9.6%
  average surviving per page   ~201 words
```

All ten pages are **SEVERE** on the coherence gate. Every one is `publish` status and in the Wave 1
release set. A concreting site's service pages are not optional, which is why D17 puts them on the
critical path.

---

## Per page

```text
  PAGE                                                WORDS   FILLER%   SURVIVES   SPECS
  concrete-driveways-south-west-sydney                2,282    0.8720        292       9
  decorative-concrete-south-west-sydney               1,174    0.7913        245       9
  concrete-driveway-replacement-south-west-sydney     2,257    0.8932        241       9
  concrete-slabs-south-west-sydney                    2,227    0.8922        240      11
  exposed-aggregate-south-west-sydney                 1,999    0.8979        204       9
  concrete-crossovers-and-laybacks-south-west-sydney  3,068    0.9397        185       9
  concrete-patios-south-west-sydney                   1,877    0.9121        165       9
  concrete-paths-south-west-sydney                    1,862    0.9157        157       9
  shed-and-garage-slabs-south-west-sydney             2,138    0.9336        142       9
  commercial-concreting-south-west-sydney             2,120    0.9354        137       9
  TOTALS                                             21,004    0.9044      2,008
```

---

## What survives — every real specification is preserved

D17.2 requires preserving these. All are present and none is filler. **Nine specifications appear on all
ten pages; `concrete-slabs` carries two more.**

```text
  SPECIFICATION      PAGES CARRYING IT   NOTE
  32 MPa                          10     concrete strength
  125mm                           10     slab / driveway thickness
  SL72                            10     reinforcing mesh
  800mm                           10     Oran Park footpath allocation
  900mm                           10     Camden LGA default footpath allocation
  1200mm                          10     allocation width
  4.0–5.5m                        10     crossing width range
  4%                              10     grade
  1:6                             10     fall ratio
  SL82                             1     concrete-slabs only
  m²                               1     concrete-slabs only
```

**These are true and sourced. The filler surrounds them; it does not replace them.** Every rebuilt page
must carry its specifications forward verbatim — never rounded, softened or paraphrased (§2 of the
governing instruction).

### But the specifications are undifferentiated

All ten pages carry the identical nine values. A patios page and a commercial hardstand page should not
specify the same thickness and mesh. This is a content problem the rebuild must fix, and it needs owner
or engineer input — **it may not be resolved by inference.** A patio does not need 125mm and SL72 because
a driveway does; asserting otherwise would be inventing a specification.

```text
  OWNER QUESTION (new, from this brief)
  Which of the nine specifications actually apply to each of the ten services, and
  what are the correct values where they differ? Supply per service, or confirm that
  one specification set genuinely covers all ten.
```

---

## What must be written

Per page, the rebuild needs:

```text
  1  An opening that states what the service is and who it is for, in plain
     Australian English, without a slug subject.
  2  The service-specific specification set, once the owner answers the question
     above. Verbatim values, no rounding.
  3  What the job involves on a real site: preparation, pour, finish, cure.
  4  What varies the price, WITHOUT stating a price until pricing is verified
     (53-page pricing question, still open).
  5  Council interaction where relevant — crossovers and laybacks especially.
     No council figure may be stated until verified with source_url and sighted_date.
  6  Where the service is offered. No suburb-specific claim beyond the service area
     the owner confirms.
  7  A close that links to the relevant cost page and to /quote/.

  Target length: to be set after the structure is agreed. The current 1,174-3,068
  word range is a product of the filler generator and is not a target.
```

### What must NOT be written

```text
  - any price, before pricing.per_m2_ranges is verified
  - any council fee, width or grade beyond the nine verified specifications
  - any claim of completed local work, before completed_projects is verified
  - any "we have" / "our recent" phrasing, which asserts operator authorship
  - any sentence whose subject is a slug
```

---

## The Wave 1 assertion required by D17.4

```text
  No service page may enter Wave 1 until:
    (a) it passes the coherence gate at or below the 20% filler threshold, AND
    (b) it passes the §4.25 uniqueness measurement on its REWRITTEN body, AND
    (c) its Index-ready value is 'yes' per §4.27.4.

  Current state: 0 of 10 satisfy (a). All ten are SEVERE.
  Recorded in build/21-spec-ledger.json under DEC03-D17.
```

Note the interaction: rewriting ten pages from a common brief risks **failing the uniqueness gate in the
other direction**. The rewritten bodies must be measured against each other, not only against the
threshold, and the ≤40% within-class pairwise cap applies.

---

## Sequencing consequence

```text
  Images        HELD. The 16 REPLACE briefs are approved as specifications but the
                slots sit on pages being rewritten, so dimensions and roles may
                change (D18).

  Suburb pages  49 MODERATE pages need editing, not rebuilding. Lower priority
                than the service rewrite per D17.

  Guides and    35 guides and 10 cost/comparison pages are equally SEVERE and have
  cost pages    NO disposition yet. See reports/34-coherence.md.
```

---

## Who writes it — the decision D17.3 reserves

Not taken. The brief stops here, as instructed. Recorded for the decision:

```text
  If written by an agent under a coherence gate:
    + consistent structure across ten pages, measurable against the gate
    - the same generator class produced the current filler; the gate must run on
      output BEFORE it enters the artifact, not after

  If written by hand:
    + a person who knows concreting will not write "new-driveway scope records scope boundary"
    - ten pages of technical copy is real work

  Either way the specification question above must be answered first. Neither an
  agent nor a writer may infer which specifications apply to which service.
```
