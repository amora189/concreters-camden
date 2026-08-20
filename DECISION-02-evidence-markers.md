# DECISION RECORD 02 — unregistered evidence markers

Issued at handoff-state, before Stage 22. Read alongside `DECISION-01-gate21.md`. Instruction documents remain read-only; cite this file in `build/21-spec-ledger.json` for every value it sets.

---

## D10 — The marker register is undercounted

`CONTEXT.md` records 163 evidence markers (111 `PLACEHOLDER`, 47 `REAL_PHOTO_PENDING`, 5 `VERIFY`). The handoff scan found **seven further occurrences in rendered page copy** that are in neither the register nor the 45-suburb research set: four literal `REQUIRED-RESEARCH` strings and three unregistered `VERIFY` strings.

**Working total: 170 occurrences.** Do not treat this as settled either.

**DO:**
1. Correct the register total in `CONTEXT.md` and the ledger, citing this clause and showing the arithmetic: 163 recorded + 4 + 3 = 170.
2. Add all seven to `reports/23-evidence-register.csv` at Stage 23, sourced as `found-in-rendered-copy` rather than `register`.
3. **Amend §4.23.1 method:** the register is built by scanning the rendered body copy of all 156 pages for every marker token — `PLACEHOLDER`, `REAL_PHOTO_PENDING`, `VERIFY`, `REQUIRED-RESEARCH` and any other bracketed or upper-case marker convention found in the corpus — **not** by reading `reports/placeholders.md` and reconciling to it. That file is now a cross-check, not a source. Report every occurrence it missed.
4. The Stage 23 discrepancy rule stands and now has a known answer: report the divergence between scanned count and recorded count. Do not silently reconcile.

---

## D11 — "Reproduced without alteration" is a false-fidelity claim

All four `REQUIRED-RESEARCH` occurrences take the form *"The recorded {suburb} council specification is reproduced without alteration: REQUIRED-RESEARCH: confirm Liverpool City Council vehicle crossing specification…"*.

The sentence asserts fidelity to a specification that was never supplied. Filling the marker is necessary but not sufficient — the claim is the problem, not just the gap.

**DO:**
1. Flag all four in the register as **false-fidelity claims**, a distinct category from a missing fact. They are a consumer-law exposure on a trades site, not only an SEO gap.
2. The sentence may stand **only if** the inserted specification is verbatim from the Liverpool City Council source, with `source_url` and `sighted_date` recorded. If the figure is approximated, summarised, or carried from another LGA, **the sentence must be rewritten**, not merely completed.
3. Scan all 156 pages for the same construction with other councils — any sentence asserting that a specification, figure, price or standard is reproduced, verified, confirmed or unaltered where the underlying value is a marker. Report every instance in `reports/23-false-fidelity.md`. Four is what the handoff scan surfaced; it was not looking for this pattern deliberately.

---

## D12 — Liverpool City Council is one owner task unblocking four pages

All four occurrences are the same specification: Liverpool City Council vehicle crossing widths, strength and fee schedule.

**DO:**
1. Record it in `reports/23-owner-questions.md` as a **single question unblocking four pages**, ranked accordingly.
2. **None may be filled from a neighbouring suburb, from Camden Council, or from any other LGA.** Leppington additionally splits Camden/Liverpool per `intersection-differentiators.json`, so a Camden figure is wrong there for a second, independent reason.
3. Cross-check against `data/council-specs.yml` at Stage 31 — the same Liverpool figures are required by the calculator. One verification clears both. Record the dependency so it is not researched twice or, worse, satisfied twice with different numbers.

---

## D13 — Two of the four are Wave 1

Leppington and Austral are Tier 1 and sit in the 21-page publish set. Bringelly and Edmondson Park are draft.

**DO:**
1. Add the Liverpool specification to Wave 1's release gate in `reports/27-wave-plan.md`. Wave 1 cannot release Leppington or Austral until it is verified and inserted verbatim.
2. Both pages are already `noindex,follow` under the Tier 1 photography gate, so the effective indexable Wave 1 count of **14 is unchanged**. Confirm that rather than assuming it.
3. Record in `reports/23-page-readiness-v2.csv` that Leppington and Austral now carry two independent blockers — photography and the Liverpool specification — and that clearing one does not release the page.

---

## D14 — Standing guidance belongs in the ledger

The handoff session reported writing memories and saving standing guidance for later gates. Confirm exactly what was written and where.

Standing guidance goes in `build/21-spec-ledger.json` or a numbered report, never appended to `CLAUDE.md`, `CODEX-BUILD-2.1.md`, or any decision record. If any instruction document was modified, restore it and record the diff. Standing rule 7 applies to every agent working this repo, including the one that wrote the guidance.

---

## Resume

Apply D10–D14 to the forward plan. They change Stage 23's method, Stage 27's Wave 1 gate and the register total; they do not change stage ordering. Then continue with `DECISION-01-gate21.md` D1–D9 and the Gate 21 confirmation report before Stage 22.
