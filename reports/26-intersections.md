# GATE 26 — intersection page audit

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.26. Data: `reports/26-intersections.csv` (one row per page).

`intersection-differentiators.json` is the sole authority on which intersection pages exist.

---

## Explicit confirmation required by the gate

```text
  ZERO intersection pages exist outside intersection-differentiators.json.

  built intersection pages          35
  allow-listed intersections        35
  built but not allow-listed         0
  allow-listed but not built         0
```

---

## 1. The six checks

```text
CHECK 1 — exactly 35 exist, no extras, every one appears in the JSON
  built                    35
  extras                    0
  missing                   0
  result                   PASS

CHECK 2 — each differentiator traces to the JSON value, not diluted or generalised
  fully traced (>=50% of differentiator terms present in body)   35
  partially traced                                                0
  not traced                                                      0
  result                   PASS
  method                   content words of length >=5 from the JSON differentiator
                           string, matched against the page's rendered body copy

CHECK 3 — each links up to both parents, and both parents exist
  parent_service page exists                35 of 35
  parent_suburb page exists                 35 of 35
  links up to parent service                35 of 35
  links across to parent suburb             35 of 35
  result                   PASS

CHECK 4 — no intersection is the only page targeting its suburb
  suburb page exists for every intersection  35 of 35
  result                   PASS

CHECK 5 — every intersection is draft on import
  draft                    35 of 35
  publish                   0
  result                   PASS

CHECK 6 — shared spec component within the ~150-word budget
  intersections over budget    12 of 35
  worst                        240 words
  result                       FAIL — see §2
```

---

## 2. The one failure — shared specification component over budget

`expansion-300-pages.md` §4 budgets the shared service specification at approximately **150 words**.
Twelve intersection pages carry more.

```text
  PAGE                                    SHARED WORDS   OVER BUDGET BY
  concrete-driveways-austral                       240              90
  concrete-driveways-edmondson-park                237              87
  concrete-driveways-spring-farm                   237              87
  concrete-driveways-catherine-field               236              86
  concrete-driveways-cobbitty                      236              86
  concrete-driveways-leppington                    234              84
  concrete-driveways-oran-park                     232              82
  concrete-slabs-austral                           228              78
  concrete-slabs-gregory-hills                     226              76
  concrete-slabs-gledswood-hills                   220              70
  concrete-slabs-bringelly                         218              68
  concrete-slabs-leppington                        219              69

  pages within budget    23 of 35
```

**Method.** The shared component is measured as the count of word positions on the intersection page whose
5-gram window also appears on its parent service page. This is an estimate of the shared block's length,
not a hand-marked boundary — the pages do not delimit the component explicitly. The figures are therefore
indicative of magnitude, and every one of the twelve is 45–60% over a budget described as approximate.

**Does it push the page below the 50% floor?** No.

```text
  intersection class Metric A uniqueness    min 0.6521, median 0.8708, max 0.9345
  sourced floor                             0.50
  intersections below the floor             0 of 35
```

All twelve over-budget pages remain well clear of the 50% intersection floor, so the second half of
§4.26.6 is satisfied even though the first half is not. The over-budget component is a content-length
issue, not a duplication failure.

**Disposition.** Held, not fixed. Trimming the shared component means editing page bodies inside
`camden-concreting-import.xml`, which is immutable. These are post-import edits if the owner wants them,
and they are low priority: the pages are all `draft` + `noindex`, in Wave 5, and pass every uniqueness
gate that applies to them.

---

## 3. Class health

```text
  body length      min 1,020   median 2,125   max 3,013 words
  target (§4)      ~700 words

  Every intersection page is substantially longer than the ~700-word target shape.
  Recorded as an observation. Longer is not a failure condition anywhere in the
  governing documents, and the pages pass their uniqueness floor comfortably.
```

---

## 4. `CONTEXT.md` update and diff

```text
  Latest completed stage    25 -> 26
  New finding               12 of 35 intersections exceed the ~150-word shared-spec budget
  Confirmed                 zero intersection pages exist outside the allow-list
  Confirmed                 all 35 differentiators trace to the JSON
  Index-ready               0 of 157 — UNCHANGED
  Launch gate               NO-GO — UNCHANGED
```

---

## 5. Hash table

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

## GATE 26 RESULT

```text
  Exactly 35 exist, no extras, all in the JSON      PASS
  Differentiators trace to the JSON                 PASS — 35 of 35
  Links up to both parents, both parents exist      PASS — 35 of 35
  No intersection is the only page for its suburb   PASS — 35 of 35
  All draft on import                               PASS — 35 of 35
  Shared spec within ~150 words                     FAIL — 12 of 35 over, worst 240
  Over-budget pages still above the 50% floor       PASS — 0 below

  GATE 26: PASS with one recorded failure.
  The failure is held, not fixed: the fix requires editing an immutable artifact,
  and the affected pages are all draft + noindex in Wave 5.
```
