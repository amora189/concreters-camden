# DECISION RECORD 06 — items resolvable without new inputs

Cite in `build/21-spec-ledger.json`. The build remains paused; these four items need no owner-supplied data and can be executed in one short session.

---

## D29 — The homepage sentence is rewritten now

The homepage is the only content page scoring CLEAN, and it carries all seven unattested figures in one construction: *"…the recorded specification is 32 MPa concrete, 125mm thickness, SL72 fabric, 4.0-5.5m urban width, a 1200mm footpath allocation, 4% crossfall and a maximum 1:6 batter."*

Two separate faults: *"the recorded specification is"* asserts a record that does not exist, and seven unverified numbers are presented as fact on the front page.

**DO:**
1. Rewrite the sentence to remove the false-fidelity framing. The figures may remain **only** if reframed as general indicative practice rather than a recorded specification, and only until the matrix lands — at which point they are replaced by attested values or removed.
2. Preferred: cut the numbers from the homepage entirely. A homepage does not need seven specifications, and every one of them is currently disputed.
3. Scan the four utility pages for the same construction. They score CLEAN on coherence, which measures sense, not truth — a clean page can still assert a false record.

---

## D30 — `site_name` is corrected at import, not in the artifact

The Elementor kit declares `site_name` as "E&T Co Concreters Camden" while the copy uses "CoreX Concreters Camden" 345 times. A site declaring another business's trading name is a stronger footprint link than shared module order or kit palette, and it is also simply wrong.

**DO:**
1. Add to the post-import runbook in `reports/29-staging-plan.md`: correct `site_name`, WordPress Settings → General site title, and any tagline carrying the source name, as an explicit verified step. **Do not edit the immutable WXR.**
2. Add a preflight assertion: zero occurrences of "E&T", "E&T Co", or the source business name in kit settings, theme mods, site title, tagline, or any rendered page.
3. Sweep the same terms across every artifact that is not the immutable WXR — filenames, alt text, attachment titles, schema, form recipients, menu labels. Report every hit. The favicon filename `e_t_co_concreters_favicon` proves this is not confined to the kit.
4. **Note in `CONTEXT.md`:** "CoreX Concreters Camden" has no verified legal entity behind it either. Correcting the name replaces an incorrect claim with an unverified one, which is an improvement but not a resolution. It stays on the identity blocker list.

---

## D31 — Privacy policy is a new utility page; the form spec stands

`/about/` and `/gallery/` carry form ID 3, which collects personal data, and no privacy policy exists. Under the Australian Privacy Principles that is a genuine compliance gap, not a nice-to-have, and it blocks two of the four remaining Wave 1 pages.

**DO:**
1. Add a privacy policy page as a fifth utility page. Architecture: **76 → 77.** Propagate per the §4.31.7 pattern.
2. Build it as a supplementary artifact alongside `camden-calculator-import.xml`, not by editing the main WXR. Same post-ID discipline, same validation table.
3. Draft it against `reports/30-forms-spec.md`: what the form collects, where it goes, retention, and contact for access or correction requests. **Every field that requires a legal entity or contact address stays a blocking marker** — a privacy policy naming no accountable entity is not a privacy policy.
4. Do not publish it or the form until the identity blocker clears. This unblocks the page's existence, not its release.

---

## D32 — No Camden job photographs exist. Remove the modules.

Answering the open item directly: fulfilment is Pakenham, no Camden pour has been completed, and none is scheduled. The 47 `REAL_PHOTO_PENDING` slots have no path to being filled.

**DO:**
1. Treat "no genuine local photography available" as a **settled fact**, not a pending input. Remove item 6 from the owner input pack.
2. For every module whose function is to evidence completed local work — the built module 8 "Local Work Completed" family — **remove the module**, not just the image. A gallery of stock photos on a "our recent work" section is a false claim regardless of how the images were licensed.
3. Where an image slot is decorative rather than evidential, it takes generic licensed imagery under the held Phase 2 briefs with honest filenames and alt text asserting nothing.
4. Report the page-by-page consequence: which pages lose a module, what survives, whether any drops below its word-count floor, and whether the Tier 1 photography hold can now be **released** — those six pages were held pending photography that will never arrive, so the hold becomes a removal decision instead.
5. Revisit only if a Camden job is completed and photographed. Record that as the reopening condition.

---

## Effect

D31 takes the architecture to 77. D32 may release the Tier 1 photography hold, which is the first blocker in this project to be cleared rather than deferred. Neither changes the launch gate: the service specification matrix and the media inputs remain the critical path, and index-ready stays 0.
