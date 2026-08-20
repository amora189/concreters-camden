# DECISION RECORD 03 — filler copy, image dispositions, sequencing

Supersedes the sequencing assumptions in `IMAGE-REPLACEMENT-PROMPT.md`. Instruction documents stay read-only; cite this file in `build/21-spec-ledger.json`.

**Phase 2 image sourcing is halted.** Do not run it. Do not spend SerpApi credits.

---

## D15 — The uniqueness gate has no coherence check. That is a specification defect, not an execution error.

Stage 25 measured difference and scored 45 pages of machine-generated filler among the most unique on the site. The 15 Stage 9 gates measured structure, meta length and duplication. Nothing measured whether a sentence carries meaning. `camden-concreting-import.xml` is structurally valid and substantively hollow, and both have been true since Stage 9.

**DO — this runs before anything else:**

1. Write `scripts/34-coherence.py` and scan **all 156 pages**, not the 45 already found. Flag per page: repeated subject-predicate templating with slot substitution; sentences whose subject is a slug or URL fragment (`new-driveway scope`); clauses repeating within a sentence; noun-phrase chains with no verb of state or action; and any sentence that cannot be paraphrased without loss because it asserts nothing.
2. Report **percentage of filler body words per page** in `reports/34-coherence.csv`, with three verbatim samples per flagged page.
3. Do not fix, rewrite or delete anything in this stage. Measure and report.
4. Add coherence as a **build-failing gate** in the ledger and in preflight: any page above a filler threshold cannot enter any wave, regardless of uniqueness, evidence or media status.
5. **Report the full extent before I decide scope.** 45 pages is what a scan looking for something else found. Treat it as a floor.

---

## D16 — The 35 intersection pages are withdrawn

They are entirely filler, they were Wave 5 at nine to twelve months out, and rebuilding them from real differentiators later beats repairing word salad now.

**DO:**
1. Mark all 35 `WITHDRAWN` in `reports/23-page-readiness-v2.csv`. **Do not delete them from the immutable WXR** — mark them withdrawn in the readiness record and exclude them at import.
2. Combined architecture: **157 − 35 = 122**. Propagate per the §4.31.7 pattern: ledger, readiness CSV, wave plan, image distribution denominator, preflight, `CONTEXT.md`.
3. `intersection-differentiators.json` stays authoritative for any future rebuild. The 35 differentiators are real research and are not discarded — record them as a rebuild input.
4. Wave 5 is now empty. Say so plainly rather than leaving it in the plan.

---

## D17 — The 10 service pages are the Wave 1 critical path

Non-optional: a concreting site without working service pages is not a site. Rewriting them is now the project's principal remaining work, ahead of images and ahead of suburb research.

**DO:**
1. `reports/34-service-page-rebuild.md` — per page: what survives (real specifications, verified figures, genuine structure), what is filler, current word count versus surviving word count, and what must be written.
2. **Preserve every real specification.** 32 MPa, 125mm, SL72, the 800/900/1200mm allocations, 4.0–5.5m, 4%, 1:6 — these are true and sourced. The filler surrounds them; it does not replace them.
3. Do not write replacement copy yet. Produce the rebuild brief and stop. I decide whether copy is written by an agent under a coherence gate or by hand.
4. Assert at Gate 34 that no service page can enter Wave 1 until it passes the coherence gate and the §4.25 uniqueness measurement on its rewritten body.

---

## D18 — Image dispositions

**16 REPLACE briefs:** approved as specifications. **Hold sourcing.** The pages they sit on are being rewritten or withdrawn, so slot dimensions and roles may change. Keep the briefs on file; revisit after D17.

**3 logo files (306, 307, 422):** correct to hold — a brand asset cannot come from a stock library. The source business's favicon serving as the CoreX mark is also a direct cross-domain footprint link between two sites presented as unrelated businesses, which is a stronger signal than shared section order. **Commission or generate a distinct CoreX mark.** Record it as an owner task. Until then the site ships with no logo rather than another business's.

**1151 and 1188** (`reactive-clay-concreter*.jpg`, "camden" added at Stage 8): the reactive-clay claim may well be true — Wianamatta Group shale is reactive — but the photograph does not evidence it and the filename asserts it. Rename honestly with no geographic or geological assertion; keep the images if they depict concrete work generically.

**1056** (`davis-creek-tarneit.jpg → south-creek-drainage-corridor-1056.jpg`, 14 pages): same class as the soil image and correctly caught. A Victorian creek named as a specific NSW watercourse. It is decorative, so rename honestly rather than remove.

**Amend the Stage 24 detector:** it missed 1056 because it tested for suburb names. Extend it to watercourses, parks, estates, roads, councils, geological formations and any other proper noun asserting place. Re-run against all 83 and report what else it missed. Two detectors have now under-reported; assume a third gap.

---

## D19 — Soil image: recommendation accepted

Remove the image, keep the sections. Deleting the service tiles and guide-link grids to remove one photograph would be destructive well beyond the finding, and you were right to stop and say so rather than execute as briefed.

The Wianamatta text survives subject to a source, per your reasoning. The Leppington *"the verified project record says…"* sentence is rewritten regardless, per D11 — it asserts a completed project record that does not exist.

---

## D20 — Alt text and attachment titles change together

Alt text is auto-generated from the attachment title, so the false geography is inherited. Every rename must update filename, attachment title and per-page alt text as one operation, verified together. A renamed file with its original title still asserts the same place.

---

## Sequence from here

1. **D15 coherence scan, all 156 pages** — report before any decision on scope.
2. D16 withdrawal and propagation to 122.
3. D17 service page rebuild brief.
4. D18 dispositions and the extended Stage 24 detector.
5. Then, and only then, image sourcing.

Nothing in this record changes the launch state: index-ready 0, NO-GO, blocked on the same owner inputs.
