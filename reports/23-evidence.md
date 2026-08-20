# GATE 23 — evidence register and owner-question set

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.23; `DECISION-02-evidence-markers.md` §D10–D13; `RUN-BLOCK-01.md` §A D1, D4, D8.

---

## 1. Method — corpus scan, not register reconciliation

Per D10.3 the register is built by scanning the rendered body copy of all 156 pages for every marker
token. `reports/placeholders.md` is a **cross-check, not a source**.

```text
  corpus            156 pages, Elementor content fields plus content:encoded
  tokens scanned    PLACEHOLDER, REAL_PHOTO_PENDING, VERIFY, REQUIRED-RESEARCH
  decode            encoding='utf-8', errors='strict'; CSV inputs read utf-8-sig
  settings excluded CSS, font names, widget IDs and style keys are not body copy
```

---

## 2. Reconciliation against the recorded totals — reported, not reconciled

```text
  token                scanned   recorded   divergence
  PLACEHOLDER              111        111            0
  REAL_PHOTO_PENDING        47         47            0
  VERIFY                     8          5           +3
  REQUIRED-RESEARCH          4          0           +4
  TOTAL                    170        163           +7

  arithmetic  163 recorded + 4 REQUIRED-RESEARCH + 3 bare VERIFY = 170
```

The +7 is exactly the set `reports/placeholders.md` missed: four literal `REQUIRED-RESEARCH` strings and
three bare, unbracketed `VERIFY` strings. All seven are sourced in the register as
`found-in-rendered-copy` rather than `register`, per D10.2.

The divergence is **reported, not silently reconciled**, per §4.23.2 and D10.4. The working total of 170
is **not treated as settled**, per D10.

---

## 3. Register contents

```text
  artifact                        reports/23-evidence-register.csv
  marker occurrences                                            170
  REQUIRED-RESEARCH data-field rows (45 unresearched suburbs)     90
  total rows                                                     260
  rows marked resolved                                             0
  rows blocking indexing                                         260

  columns  marker_id, type, form, source, post_id, slug, url, page_class, tier,
           status, context, fact_required, who_can_supply, clearable_by,
           blocks_indexing, resolved
```

Every marker occurrence appears **exactly once** and carries its own `marker_id`. None is marked resolved.

The 90 data-field rows are the `REQUIRED-RESEARCH` fields across the 45 unresearched suburbs in
`suburbs-expanded.json`, added as blocking rows per §4.23.3. They are evidence gaps even though they are
not marker strings in page copy.

---

## 4. Readiness superset — `reports/23-page-readiness-v2.csv`

Join performed per `RUN-BLOCK-01.md` §A D4.

```text
  join key                slug, normalised to leading-slash + trailing-slash + lowercase
  source CSV encoding     utf-8-sig (the original carries a BOM)
  rows in original         156
  rows in v2               157
  slugs unmatched            0
  slugs non-unique           0
  every original row present YES
  Index-ready values         no: 157   (no value changed from 'no')
```

Zero unmatched and zero non-unique, so the D4 stop-and-ask condition was not triggered.

Columns preserved from the original, plus: `Page ID` (sourced from `build/stage9-page-manifest.json`),
`Slug`, `Page class`, `Tier`, `Build status`, `Blocking marker IDs`, `Blocking count`, `Clearable by`,
`Wave assignment`, `Effective robots directive`.

The 157th row is the calculator, per `RUN-BLOCK-01.md` §A D1:

```text
  URL                          (slug pending Stage 31 approval)
  Build status                 not yet built — §4.31
  Index-ready                  no
  Blocking count               4     (Camden, Liverpool, Campbelltown, Wollondilly figures)
  Clearable by                 council source
  Wave assignment              4
  Effective robots directive   noindex,follow
```

A readiness row for an unbuilt page is legitimate. A *measurement* of one is not, and none was taken.

`CONTEXT.md`'s source-of-truth list now notes that v2 supersedes the original.
`reports/18-page-readiness.csv` is **not deleted**.

Per §4.23, no separate block-map artifact was created. One readiness record only.

---

## 5. Top 15 questions by pages unblocked

Full set in `reports/23-owner-questions.md`. No question suggests its own answer.

```text
RANK  PAGES  MARKERS  CLEARABLE BY     QUESTION
   1     53       53  owner fact       Actual per-square-metre price ranges by finish type, from jobs
                                       quoted in the Camden area
   2     45       90  research         The 45 unresearched suburb shells: research them, or withdraw
                                       them from the plan
   3     24       24  owner fact       ABN of the entity trading as CoreX Concreters Camden, and
                                       whether that entity contracts with customers
   4     24       24  owner fact       Business address, and whether it is staffed during business
                                       hours
   5     16       47  photo            Photographs of completed work, each with location, approximate
                                       date, and owner permission to publish
   6      5        5  council source   Camden, Campbelltown and Wollondilly vehicle-crossing
                                       specification, application path and fee, with URL and date read
   7      4        4  council source   Liverpool City Council vehicle crossing specification: widths,
                                       strength, fee schedule, with URL and date read
   8      1        6  owner fact       Real customer reviews with reviewer names as agreed and
                                       permission to publish
   9      1        3  council source   Bringelly governing LGA, and whether it varies by lot
  10      1        2  owner fact       NSW Fair Trading licence number, holder, and expiry
  11      1        2  owner fact       Two unclassified markers needing a human read
  12-15   1        1  research         Per-suburb research items, ranked within the rank-2 programme
```

Ranks 12 onward are individual per-suburb research fields, each affecting one page. They are consolidated
into rank 2 rather than occupying the top of the list one suburb at a time.

### Ranking note

The pricing question alone unblocks **53 pages** and is the highest-leverage answer in the build. ABN and
address unblock 24 each and are one conversation.

The Liverpool question unblocks only 4 pages but is ranked above the 45-suburb research programme in
practical priority because it is a single lookup with a definite answer, it gates two Wave 1 pages
(Leppington and Austral), and per D12.3 the identical figures are required again by the Stage 31
calculator — one verification clears both.

---

## 6. False-fidelity carry-forward (D11)

The six false-fidelity claims from `reports/23-false-fidelity.md` are represented in the register. Four
carry `fact_required` naming the Liverpool specification; three Bringelly rows carry a `fact_required`
that states plainly that the sentence asserts verification which has not occurred.

**Two of the six are not fillable.** No supplied value makes *"the verified project record says: VERIFY"*
true. They require rewriting regardless of what the owner supplies, and clearing the Liverpool question
does not clear them.

---

## 7. Module contract gap (D8 item 12)

`reports/21-module-contracts-gap.md` written.

```text
  classes with a complete normative contract   3   service, suburb, intersection
  classes with a partial contract              3   guide_hub, guide, cost_comparison
  classes with no contract                     2   home, utility
  proposed contracts                           5   all marked AWAITING APPROVAL — not enforced
```

Neither enforced nor treated as a pass. Both statements hold at once.

---

## 8. `CONTEXT.md` update and diff

```text
  Latest completed stage      22 -> 23
  Evidence marker total       163 -> 170 (already corrected under D10)
  Register method             placeholders.md reconciliation -> corpus scan
  Readiness record            18-page-readiness.csv -> v2 supersedes; original retained
  Readiness rows              156 -> 157
  Index-ready                 0 of 157 — UNCHANGED
  Launch gate                 NO-GO — UNCHANGED
  Blockers                    none cleared; 260 register rows all unresolved
```

---

## 9. Hash table

```text
  camden-concreting-import.xml                          A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884  MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15  MATCH
  build/stage9-page-manifest.json                       578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42  MATCH
  build/stage8-image-map.json                           0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF  MATCH
  reports/08-image-rename-map.csv                       43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8  MATCH
  CODEX-BUILD-2.1.md                                    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C  MATCH

  6 of 6 MATCH. Stop condition C1 not triggered.
```

---

## GATE 23 RESULT

```text
  Every marker occurrence appears exactly once            PASS — 170 occurrences, 170 rows
  None marked resolved                                    PASS — 0 of 260 resolved
  45 unresearched suburbs added as blocking rows          PASS — 90 data-field rows
  Discrepancy against recorded totals reported            PASS — +7, reported not reconciled
  Readiness v2 is a superset, every original row present  PASS — 156 of 156 matched
  157 rows                                                PASS
  No Index-ready value changed from 'no'                  PASS — 157 of 157 remain 'no'
  Join produced no unmatched or non-unique slug           PASS — 0 and 0
  Top 15 questions printed                                PASS
  No question suggests its own answer                     PASS
  Module contract gap enumerated (D8 item 12)             PASS

  GATE 23: PASS.
```
