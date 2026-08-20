# DECISION RECORD 05 — specification figures, site mark, pause

Cite in `build/21-spec-ledger.json`. Instruction documents remain read-only; this record corrects a clause in `CODEX-BUILD-2.1.md` §2 without editing it.

---

## D26 — The specification-figure clause is withdrawn

`CODEX-BUILD-2.1.md` §2 closes with: *"Where any document gives a specific figure (32 MPa, 125mm, SL72, 800mm vs 900mm footpath allocation, 1200mm, 4.0–5.5m, 4%, 1:6), reproduce it exactly. Never round, soften or paraphrase a specification."*

That clause was written on the assumption those figures were sourced. D23.3 established they are a template artefact repeated identically across ten service pages. **The clause was protecting unattested numbers from correction. It is withdrawn.**

**Replacement rule:**

1. No figure is protected by virtue of appearing in a planning document. Protection comes from attestation — a source, a sighted date, or an owner/engineer sign-off — not from prior appearance.
2. Every numeric specification currently on a page is `unattested` until entered in `data/service-specs.yml` with `verified: true` and a source.
3. Unattested figures are **not** deleted and **not** rounded. They are flagged in place and reported. Deletion loses information that may prove correct; alteration invents a second wrong number.
4. **Two populations, tracked separately.** Figures plausibly traceable to a council instrument — the 800mm/900mm footpath allocations, 1200mm width, 4.0–5.5m, 4%, 1:6 — go in `reports/35-figure-provenance.csv` as `council-sourced-pending-verification`. Figures that are service-dependent engineering values — 32 MPa, 125mm, SL72 — go in as `template-artefact-unattested`. Do not merge them; their verification paths differ.
5. Report every page carrying an unattested figure, and its import status. Any such page is blocked from every wave until its figures are attested.

---

## D27 — Site mark: wordmark

No honest mark exists. Attachment 177 is an AI-generated favicon, 159 its orphaned original, 306/307/422 the source business's symbol, and the header logo is undeterminable until the Astra export arrives.

**Decision: a text wordmark. No image mark ships.**

1. Remove attachment 177 as site icon. Remove 272 per D24. Leave 159, 306, 307 and 422 unreferenced; do not delete from the immutable WXR.
2. Specify the wordmark in `reports/35-site-mark-spec.md`: text, typeface from the existing Elementor kit, size and placement in the header and as favicon. **Do not implement** — the Astra export governs header rendering and does not exist yet.
3. The wordmark carries the trading name only. No ABN, no licence number, no claim of establishment, no "licensed" or "insured" wording until those are verified.
4. If the Astra export shows the header logo slot references any held attachment, report it. Do not act.

---

## D28 — The build pauses here

Every remaining task is owner-supplied. No further agent stage can proceed without inputs that do not exist.

**DO:**
1. Update `CONTEXT.md`: latest completed stage, architecture at 76, launch state NO-GO, index-ready 0, and a clear statement that the build is **paused pending owner inputs** rather than blocked on technical work.
2. Write `reports/35-owner-input-pack.md` — one page per input, stating exactly what is needed, in what format, where it goes on disk, what it unblocks, and how many pages it releases. This is the handover to me.
3. Confirm the seven immutable hashes a final time and record them as the pause baseline.
4. Do nothing further. Do not begin the service rebuild, do not source images, do not populate any `verified: false` field.

---

## Owner input pack — the whole remaining project

| # | Input | Unblocks |
|---|---|---|
| 1 | **Service specification matrix** — 10 services × 9 fields | The entire Wave 1 service rebuild. Nothing proceeds without it. |
| 2 | **83 image binaries + Astra Customizer export + working re-encode driver** | Authoritative staging import, header rendering, all media gates |
| 3 | **Legal entity, ABN, NSW licence, insurance, address and whether staffed, phone routing** | All schema; currently forces every `Service` node to omit `provider` |
| 4 | **Liverpool City Council crossing specification** | Two Wave 1 suburb pages, four false-fidelity sentences, and the §4.31 calculator |
| 5 | **Service page authorship decision** | Who writes the ~8,000 words, under the coherence and uniqueness gates |
| 6 | **Real Camden job photographs** | The 47 `REAL_PHOTO_PENDING` slots and the Tier 1 suburb noindex holds |

Items 1 and 2 are the critical path. Item 6 requires a Camden job to exist.
