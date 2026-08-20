# GATE 27 — wave re-plan and Wave 1 menu spec

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.27; `RUN-BLOCK-01.md` §A D1, D6; `DECISION-02-evidence-markers.md` §D13.
Artifacts: `build/27-wave1-menus.json`, `scripts/27-menu-lint.py`.

**This is a conditional release plan, not a state change.** Per `RUN-BLOCK-01.md` §A D8 item 16, the
present index-ready count is 0 and the Wave 1 effective indexable count is 14; both are true at once and
are never alternatives to one another.

---

## 1. The wave table — recomputed against the real 157

**The headline number is the effective indexable count, not the release count.**

```text
  WAVE   RELEASED   NOINDEX,FOLLOW   EFFECTIVE INDEXABLE   COMPOSITION
     1         21                7                    14   1 home, 4 utility, 10 service, 6 Tier 1 suburb
     2         16               16                     0   1 guide hub, 15 guides
     3          9                9                     0   9 researched Tier 2 suburbs
     4         31               31                     0   20 guides, 11 cost/comparison
     5         35               35                     0   35 intersections
  none         45               45                     0   45 unresearched suburbs — no wave

  TOTAL       157              143                    14
```

Nothing may report 21 published as 21 indexed. Wave 1 releases 21 pages and 14 of them are indexable.

### Wave 4 and the calculator

```text
  wave 4 released              31  = 20 guides + 10 built cost pages + 1 calculator
  calculator build status      not yet built — §4.31
  calculator robots on import  noindex
  effect on effective count    none; it is noindex, so Wave 4 stays at 0 indexable
```

Included and marked not-yet-built, per D1. Not omitted, and not counted as buildable.

---

## 2. Per-wave entry conditions

Drawn from `reports/23-page-readiness-v2.csv`. Wave 1 contains only pages whose blockers are clearable by
owner-supplied facts — no page whose release depends on research or on a council's publication schedule.

```text
WAVE 1 — entry conditions
  every page                  ABN, business address and staffing status verified
  every page                  phone number 03 4517 6915 ownership and routing proven, or replaced
  10 service pages            real per-square-metre ranges supplied (53-page pricing question)
  6 Tier 1 suburbs            HELD noindex,follow until photography and evidence gates pass
  Leppington, Austral         SECOND independent blocker: Liverpool City Council specification (D13)
  Gallery                     HELD noindex,follow until real photography exists
  homepage + 4 utility        clearable on owner facts alone

WAVE 2 — entry conditions
  guide hub                   NEVER publishes without its first approved guides (§4.27.3)
  15 guides                   council figures verified with source_url and sighted_date
  all 16                      remain noindex,follow until each guide's facts are individually approved

WAVE 3 — entry conditions
  9 researched Tier 2 suburbs uniqueness re-measured after the metric definition is approved (Gate 25 §0)
  all 9                       photography and evidence gates, as Tier 1

WAVE 4 — entry conditions
  20 guides                   as Wave 2
  10 built cost pages         individually approved; stay draft until then (§4.27.3)
  1 calculator                built at Stage 31, then all four LGA figures verified
                              PROMOTION CLAUSE: promotable to Wave 2 once, and only once, all four
                              LGAs are verified:true with sighted sources. Owner approval required.
                              Never self-promoted.

WAVE 5 — entry conditions
  35 intersections            parent suburb page live and indexable first
  12 of 35                    shared-spec component over the ~150-word budget (Gate 26 §2)

NO WAVE — the 45 unresearched suburbs
  entry condition             research completed; until then they enter no wave at all (§4.27.3)
```

---

## 3. Enforcement assertions

```text
ASSERTION 1 — Tier 1 suburbs and Gallery stay noindex,follow
  Tier 1 suburbs held         6 of 6   Oran Park, Gregory Hills, Gledswood Hills,
                                       Harrington Park, Austral, Leppington
  Gallery held                yes
  result                      PASS

ASSERTION 2 — the guide hub never publishes without its first approved guides
  hub wave                    2
  guides in wave 2            15
  hub released alone          never
  result                      PASS

ASSERTION 3 — the 45 unresearched suburbs enter no wave
  assigned to a wave          0 of 45
  result                      PASS

ASSERTION 4 — the 11 cost/comparison pages stay draft until individually approved
  cost pages in wave 4        11 (10 built + 1 not yet built)
  status                      all draft, all noindex
  result                      PASS

ASSERTION 5 (§4.27.4) — no wave's release set contains a page whose Index-ready is
                         'no' unless it is explicitly released as noindex,follow
  pages planned as indexable in Wave 1        14
  of those, currently Index-ready 'yes'        0
  result                      BLOCKING — see below
```

### Assertion 5 is currently blocking, and that is the correct outcome

All 157 pages are `Index-ready: no`, and nothing in Stages 22–32 can change that. Wave 1 plans to release
14 pages as indexable. Under §4.27.4, read literally and correctly, **Wave 1 cannot be released today**.

This is not a defect in the plan. It is the gate doing its job: the 14 pages become releasable only once
each is individually moved to `Index-ready: yes` through evidence resolution and Stage 32 QA. Recorded as
a **release-time gate**, evaluated at the moment of release rather than now.

```text
  Wave 1 release status today     BLOCKED
  what unblocks it                14 pages individually reaching Index-ready: yes
  what cannot unblock it          anything in this work block
```

---

## 4. D6 — link Rule A covers all ten services

```text
  service pages                          10
  linked from the homepage               10
  missing                                 0
  result                               PASS
```

Rule A is satisfied at ten, not seven. Rules B–G unchanged in scope.

---

## 5. Wave 1 menu spec — `build/27-wave1-menus.json`

```text
  imported menu items       65
  retained for Wave 1       27
  removed or held           38
  orphaned parents after prune   0   (_menu_item_menu_item_parent preserved for all retained items)

  REMOVAL REASONS
    target is draft                20
    target is held noindex,follow  18

  PER MENU              SOURCE   RETAINED   REMOVED
    Primary                 23         10        13
    Primary (2)             23         10        13
    Footer Areas             6          0         6
    Footer Services          7          7         0
    Footer Blogs             6          0         6
```

Two menus empty completely for Wave 1:

```text
  Footer Areas    all 6 items point at Tier 1 suburb pages, which are held noindex,follow
  Footer Blogs    all 6 items point at guides, which are draft
```

Both must be unregistered from their theme locations for Wave 1, not merely emptied — an Astra footer
widget bound to an empty menu renders an empty region rather than nothing. Recorded for Stage 29's menu
location assignment step.

---

## 6. GATE 27 condition — menu lint passes on Wave 1, fails on the full set

```text
RUN 1 — python scripts/27-menu-lint.py
  items linted   27
  failures        0
  exit code       0
  VERDICT      PASS

RUN 2 — python scripts/27-menu-lint.py --full-imported-set
  items linted   65
  failures       38   (20 draft targets, 18 noindex targets)
  exit code       1
  VERDICT      FAIL

  Gate condition satisfied: passes against the Wave 1 JSON, fails against the
  full imported set.
```

Sample of what the full-set run catches:

```text
  item 1512 'Oran Park'                        -> /concreters-oran-park/ held noindex,follow
  item 1513 'Leppington'                       -> /concreters-leppington/ held noindex,follow
  item 1518 'Blog'                             -> /guides/ is draft
  item 1520 'Camden Council Driveway Crossing' -> draft
  item 1521 'Liverpool Council Vehicle Crossing' -> draft
```

The lint also fails on any menu item whose `object_id` resolves to no page (404) and on any retained item
whose parent was pruned. Neither occurs in the Wave 1 set.

---

## 7. `CONTEXT.md` update and diff

```text
  Latest completed stage     26 -> 27
  Wave plan                  legacy 300-page waves -> recomputed against 157
  Wave 1 effective indexable 14 (conditional; 0 today)
  New blocking gate          §4.27.4 blocks Wave 1 release until 14 pages reach Index-ready: yes
  New Stage 29 task          unregister Footer Areas and Footer Blogs menu locations for Wave 1
  Index-ready                0 of 157 — UNCHANGED
  Launch gate                NO-GO — UNCHANGED
```

---

## 8. Hash table

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

## GATE 27 RESULT

```text
  Waves 1-5 as explicit page sets against the real 157   PASS
  Per-wave release / noindex / effective indexable       PASS — headline is the effective count
  Tier 1 suburbs and Gallery held noindex,follow         PASS
  Guide hub never publishes alone                        PASS
  45 unresearched suburbs enter no wave                  PASS
  11 cost pages stay draft                               PASS
  §4.27.4 release assertion                              BLOCKING — correctly; 0 of 14 Index-ready
  D6 homepage links all ten services                     PASS — 10 of 10
  build/27-wave1-menus.json with zero draft/noindex links PASS
  Menu diff against the 65 imported items                PASS — 27 retained, 38 removed
  Menu lint passes on Wave 1                             PASS — exit 0
  Menu lint fails on the full imported set                PASS — exit 1, 38 failures

  GATE 27: PASS. Wave 1 release itself is blocked by §4.27.4 until pages
  individually reach Index-ready: yes, which is the intended behaviour.
```
