# DECISION-08 — trading name, brand assets, partial NAP

Date: 19 August 2026 (Australia/Sydney).
Origin: owner instruction issued in session, 19 August 2026.
Status: **transcription of the owner's instruction, recorded so the ledger has a citable authority.**
If any clause below misstates the instruction, the owner's correction governs and this file is
reissued. Read-only once confirmed.

Decisions D35–D38. Numbering continues from DECISION-07 (D33–D34).

---

## D35 — The trading name is "Structure Co Concreters Camden"

The repo carries three trading names. Structure Co replaces both of the others.

```text
  CoreX Concreters Camden        the name in the built copy        SUPERSEDED
  E&T Co Concreters Camden       the source Melbourne business,    SUPERSEDED
                                 still declared in the Elementor
                                 kit site_name
  Structure Co Concreters Camden the name from 19 August 2026      CURRENT
```

**DO:**

1. Produce a complete rename plan — every location, every artifact, and the post-import steps
   required where the immutable WXR is involved. Report the count per artifact.
   **Do not execute it.** → `reports/38-trading-name-rename-plan.md`.
2. Update D30. D30 was written to correct `E&T Co` → `CoreX`. Its target is now `Structure Co`, and
   its scope widens: the correction is no longer two kit values but a full-corpus rename.
   D30's method is unchanged and remains correct — correct at import, never in the artifact.
3. **The rename does not clear the identity blocker.** Structure Co has no verified legal entity, no
   ABN and no NSW Fair Trading licence, exactly as CoreX had none. This replaces one unverified name
   with another. It is an improvement in accuracy — the site stops declaring a different business's
   name — and it is not a resolution. The identity blocker list keeps every entry it had.
4. Nothing in this decision authorises emitting `Organization` or `LocalBusiness`. D2's ladder is
   unaffected: a trading name is not a verified legal entity.

## D36 — Brand assets supersede the inherited marks under D27

Supplied: wordmark in horizontal, reversed, single-colour, stacked and square-icon forms; SVG with
text converted to outlines, plus PNG renders. Navy `#1C244B` (recorded at the time as "from the
Elementor kit"; corrected in clause 4 below — it is from inlined page styling), grey
`#7C8494`.

**DO:**

1. These assets supersede, under D27:
   - **177** — AI-generated favicon, currently the site icon
   - **159** — its orphaned original
   - **306, 307, 422** — the E&T symbol files
2. Add the favicon and header logo assignment to the post-import runbook as explicit verified steps.
   **Do not implement.** The Astra Customizer export governs header rendering and still does not
   exist.
3. D27's core decision is amended, not overturned. D27 resolved "a text wordmark, no image mark
   ships" *because no honest mark existed*. A supplied brand asset removes that premise. What does
   not change: the mark carries the trading name only — no ABN, no licence number, no claim of
   establishment, no "licensed" or "insured" wording, until those are verified.
4. ~~`#1C244B` is taken from the source Elementor kit palette.~~ **CORRECTED 19 August 2026,
   owner-accepted.** `#1C244B` appears **732 times in page `_elementor_data` and zero times in the
   Elementor kit**. It comes from the source site's inlined per-widget page styling. It remains an
   unchanged residual footprint inherited from the source site and already disclosed in
   `CONTEXT.md`, and reusing it is the owner's choice — only the provenance sentence was wrong. The
   kit itself holds Elementor's factory palette (`#6EC1E4`, `#54595F`, `#7A7A7A`, `#61CE70`), each
   appearing exactly once in the whole WXR and used by nothing. **`#7C8494` is genuinely new** —
   zero occurrences in the WXR, inheriting nothing — and `#AEB6C6` is a lift of it, so also new.
   Recorded in `build/21-spec-ledger.json` `corrections_register` with `corrected_from` preserved;
   evidence in `reports/42-astra-vs-elementor-design-carriage.md`.

## D37 — Partial NAP recorded; phone still outstanding

Supplied:

```text
  email     info@concreterscamden.com.au
  address   15 Murray Street, Camden NSW 2570
```

**DO:**

1. Record both in `data/verified-facts.yml`.
2. **The address stays `verified: false` and `is_staffed: unknown`** until the owner attests it.
3. Phone remains outstanding. `03 4517 6915` stays flagged: a Victorian area code on a NSW site,
   ownership and routing unproven. It is not silently corrected and it is not removed.
4. **Do not emit `LocalBusiness` schema.** D2's ladder resolves to **outcome 3** — `Service` omits
   `provider` entirely — until the entity and the staffed status are both verified. An address on
   its own does not define a `LocalBusiness`; §4.30.2 requires a verified *staffed* address.

## D38 — The media intake directory is image-only, and that becomes an assertion

Two personal résumé PDFs and an unregistered WXR export have been quarantined out of
`source-inputs/media/`.

**DO:**

1. Confirm the directory now contains only image binaries.
2. Add a media-intake assertion that **fails on any non-image file**. That directory feeds a public
   web server; a non-image file arriving there is a disclosure risk, not an untidy directory.

---

## Effect

Architecture is unchanged at 77. Index-ready is unchanged at 0. The launch gate is unchanged at
NO-GO. Phase B remains blocked at step 2 on the Astra Customizer export.

D35 and D37 both narrow what the site falsely claims without clearing a single blocker, which is the
honest characterisation of both.
