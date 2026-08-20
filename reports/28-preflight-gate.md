# GATE 28 — deterministic preflight runner

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.28; `RUN-BLOCK-01.md` §A D1.
Artifacts: `scripts/28-preflight.sh`, `scripts/28-gates.py`, `reports/28-preflight.md`, `reports/28-gates.json`.

**The machine-written result is `reports/28-preflight.md`.** This file is the gate report around it.

---

## TOP LINE

```text
  OVERALL: NO-GO
  exit code: 1
```

§4.28 requires that running it now returns NO-GO "citing the missing media and Astra inputs plus genuine
content failures — and nothing failing for a spurious or environmental reason." That is what it does.

---

## The eleven gates, in the order §4.28 specifies

```text
  GATE                                            RESULT   DETAIL
  1. encoding canary (§3.1)                       PASS     fixture and both restored assertions survived
  2. 15 Stage 9 gates                             PASS     15/15 pass
  3. post-ID collision audit (both XMLs)          FAIL     supplementary artifact absent
  4. media intake audit                           FAIL     0 of 83 binaries present
  5. Astra Customizer audit                       FAIL     export absent; 0 of 7 mod groups
  6. Elementor image-reference count              PASS     image=1085 as recorded; +98 background_image
  7. uniqueness gates                             FAIL     1,761 over-cap 5-grams; 1,491 pair failures
  8. intersection audit                           PASS     35 built, 35 allow-listed, all draft
  9. menu lint (Wave 1 spec)                      PASS     zero draft, noindex or 404 targets
  10. Victorian blocklist scan                    PASS     0 occurrences across 13 terms
  11. placeholder-in-schema scan                  PASS     0 JSON-LD blocks, 0 placeholders

  OVERALL                                         NO-GO
```

No gate was skipped, suppressed, or marked advisory. Four FAIL; any one of them alone makes the run NO-GO.

---

## The four failures, each a genuine reason

### Gate 3 — supplementary artifact absent

```text
  camden-calculator-import.xml     ABSENT
  main file occupies               306 post IDs
  highest occupied ID              1567
  audit across both files          CANNOT RUN
  result                           FAIL
```

Per `RUN-BLOCK-01.md` §A D1 this is **a genuine NO-GO reason, reported as one**. It is not special-cased,
not suppressed, and not marked advisory. The calculator is built at Stage 31, which is excluded from this
run block; until it exists the cross-file collision audit cannot run, and a gate that cannot run at full
fidelity fails.

When the calculator is built, its `post_id` must be allocated **above 1567**, the highest ID occupied
anywhere in the main file.

### Gate 4 — media intake

```text
  expected binaries    83
  present               0
  result             FAIL
```

Owner-supplied P0 input. Nothing in this work block can clear it.

### Gate 5 — Astra Customizer export

```text
  candidate files       0
  mod groups present    0 of 7
  result             FAIL
```

Owner-supplied P0 input. Nothing in this work block can clear it.

### Gate 7 — uniqueness, a genuine content failure

```text
  5-grams appearing on more than 2 pages         1,761
  within-class page pairs over 40% overlap       1,491
  result                                          FAIL
```

This is the substantive content failure, not an environmental one. Both figures are dominated by the
suburb class: all 1,491 pair failures are suburb-to-suburb, and the worst pair
(`concreters-hoxton-park` / `concreters-horningsea-park`) sits at 92.5%.

Note the interpretation recorded at Gate 25 §1: the top over-cap 5-grams are shared header and footer
boilerplate ("get your free quote today", the phone number), which every page carries. The rule as written
fails every page. That interpretation question is carried forward; it is **not** used to soften this gate,
which reports the raw measurement.

---

## Nothing failed for a spurious or environmental reason

§4.28's gate condition requires this explicitly, so it is stated explicitly.

```text
  PASS gates that could have failed environmentally, and did not:
    1   encoding canary — ran under PYTHONUTF8=1 / PYTHONIOENCODING=utf-8
    2   all 15 Stage 9 structural gates re-verified from the artifact
    6   image reference count matched the recorded 1,085 exactly
   10   blocklist clean across all 13 terms
   11   no JSON-LD in Elementor data, so no placeholder can leak into schema
```

One environmental defect **was** encountered and fixed rather than worked around: the first run passed an
MSYS-style absolute path (`/c/Users/...`) to a native Windows Python, which could not open it, and gate
2–11 collapsed with a `FileNotFoundError`. Per standing rule 8 the assertion was not narrowed to
accommodate it — the script was corrected to use relative paths, and the gates now run at full fidelity.

A second, smaller defect was also corrected: gates initially *recorded* out of numeric order because the
external audits finished at a different time than the analytical pass. §4.28 specifies an order, so the
external audits now run first and every gate is recorded in the specified sequence.

---

## Gate 6 — the recorded figure is correct but incomplete

```text
  image widget references              1,085   matches the recorded figure exactly
  background_image references             98   NOT covered by the recorded figure
  total                                1,183
  distinct attachment IDs referenced      73   of 83
  unresolved references                    0
```

Gate 6 PASSES because the assertion as written ("1,085 across 83 attachments") is met on its `image`
component and no reference is unresolved. The 98 `background_image` references sit outside the recorded
assertion, so the gate as specified does not inspect them. This is the open finding first recorded in
`reports/handoff-state.md` §4.1 and it remains open — an owner decision, because correcting it changes a
figure written into `CODEX-BUILD-2.1.md` §4.28.

The subordinate claim "across 83 attachments" is not met on the artifact: 73 of 83 are referenced. The
other 10 are the logo and site-identity PNGs carried in Astra theme mods.

---

## `CONTEXT.md` update and diff

```text
  Latest completed stage     27 -> 28
  Preflight runner           none -> scripts/28-preflight.sh, fail-closed, 11 gates
  Preflight verdict          NO-GO (4 FAIL, 7 PASS)
  Confirmed                  highest occupied post ID anywhere in the main file is 1567
  Index-ready                0 of 157 — UNCHANGED
  Launch gate                NO-GO — UNCHANGED
```

A script that checks a blocker is not a cleared blocker. No blocker was cleared.

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

## GATE 28 RESULT

```text
  Runner exists and is fail-closed                          PASS
  All 11 gates run in the specified order                   PASS
  No gate skipped or marked advisory                        PASS
  Single top-line GO / NO-GO with per-gate detail           PASS
  Returns NO-GO now                                         PASS — as required
  Cites missing media input                                 PASS — gate 4
  Cites missing Astra input                                 PASS — gate 5
  Cites genuine content failures                            PASS — gate 7
  Missing supplementary XML reported as a genuine reason    PASS — gate 3, not special-cased
  Nothing failing for a spurious or environmental reason    PASS — one env defect found and fixed,
                                                                   not worked around

  GATE 28: PASS. The runner's verdict is NO-GO, which is the expected and
  correct outcome, not a failure of the run (RUN-BLOCK-01.md §C).
```
