# RUN BLOCK 02 — execute on input arrival

**Do not start this until the preconditions in §1 are met.** It is written now so that no time is lost later. Standing rules from `CODEX-BUILD-2.1.md` and decisions D1–D32 apply unchanged.

Architecture at pause: **77 pages**, index-ready 0, launch gate NO-GO, 5 owner inputs outstanding.

---

## 1. Preconditions — check each, run only what is unblocked

This block is **modular**. Each phase has its own precondition. If an input is missing, skip that phase, record it as skipped, and run the rest. Do not wait for all five.

| Phase | Precondition | Skip if absent |
|---|---|---|
| A | `data/service-specs.yml` fully populated, every field `verified: true` with source or attestation | Yes |
| B | 83 binaries in `source-inputs/media/` + Astra export in `source-inputs/astra/` + corrected re-encode driver | Yes |
| C | Legal entity, ABN, licence, insurance, address and staffed status, phone routing in `data/verified-facts.yml` | Yes |
| D | Liverpool City Council crossing specification with `source_url` and `sighted_date` | Yes |
| E | Service page copy written and supplied, or authorship authorised | Requires A |

Print the precondition table before starting. Confirm the seven immutable hashes against the pause baseline.

---

## PHASE A — Attest the figures

1. Validate `data/service-specs.yml`: every field populated, `verified: true`, with a source or a named attestation. **Any field still false halts Phase A.**
2. Reconcile against `reports/35-figure-provenance.csv`. For each of the 214 flagged figures: replaced with an attested value, confirmed correct, or removed. **No figure survives unattested.**
3. Report every page where an attested value differs from what is currently published — those pages carried a wrong specification and the diff is the record of it.
4. Re-run the coherence and uniqueness gates on any page whose body changed.

## PHASE B — Media and staging

1. `scripts/22-media-audit.py` — all 83 filenames, exact match, MIME, dimensions, checksums, no extras. Fail closed.
2. `scripts/22-astra-audit.py` — genuine Customizer export, mods enumerated.
3. Run the **corrected** re-encode driver. Then the EXIF assertion: zero GPS, zero owner/artist/serial, zero original-datetime. **This has never run on real files. Treat a pass with suspicion until you have inspected three files by hand.**
4. Pixel-level verification, per the fourth gap: confirm each image depicts what its filename and alt text claim. This cannot be automated and is not optional — it is how the 20 Victorian substitutions would have been caught at source.
5. Build `staging-authoritative/` per `reports/29-staging-plan.md`. PHP 8.3, loopback-only, global noindex, clean checkpoint.
6. Import in order with a rollback point after each: Astra → media → main WXR → verify → privacy WXR → verify. **Runbook step 14: correct `site_name` and `site_description`.** Preflight gate 13 must pass afterwards.
7. Verify all 83 attachments and every Elementor image reference resolve.

## PHASE C — Identity and schema

1. Populate `data/verified-facts.yml`. Every field needs a source, not an assertion.
2. Re-run `scripts/30-build-schema.py`. Report how many `Service` nodes now carry a provider — previously 0 of 105.
3. Enforce: zero references to any `@id` not defined in the same graph.
4. Resolve the 11 blocking markers in the privacy policy. It cannot publish naming no accountable entity.
5. Create Fluent Forms form ID 3 per `reports/30-forms-spec.md`, with SMTP delivery verified by a real test send.

## PHASE D — Liverpool

1. Insert the specification verbatim into the four pages, with `source_url` and `sighted_date`.
2. **The "reproduced without alteration" sentence stands only if the insertion is verbatim.** Otherwise rewrite it, per D11.
3. Rewrite the two Bringelly sentences regardless — no supplied value makes *"the verified project record says: VERIFY"* true.
4. Populate the Liverpool rows of `data/council-specs.yml` for the §4.31 calculator. One verification, both uses, same numbers.

## PHASE E — Service page rebuild

1. Ten pages, ~7,400–9,200 words total, against the attested matrix.
2. Every page passes: coherence gate, its uniqueness threshold, the ≤40% pairwise cap against the other nine, and the opening-80-word test.
3. **Differentiate by real specification difference, not paraphrase.** A patio and a commercial hardstand differ because their specs differ; if the rewritten bodies breach the pairwise cap, the matrix is insufficiently differentiated and that is the finding, not a writing problem.
4. No page ships until it passes all four gates. A failing page is held, never softened to pass.

## PHASE F — Images, last

Only after A–E. Regenerate `reports/33-image-replacement-spec.csv` against the post-D32 architecture — the existing file is stale, written against 156 pages when 81 are withdrawn. Report the revised slot count. Then broaden the briefs to decorative subjects and run `find_images.py`. Verify each licence on its source page before download.

## PHASE G — Release

1. `scripts/28-preflight.sh` — full run, all gates including coherence (12) and source-name (13). **NO-GO on any fail.**
2. `scripts/32-qa-automated.py`, then the human-sighted checklist. Environment-level Lighthouse from Stages 11–20 is not Camden-site approval.
3. Page-by-page release decision from `reports/23-page-readiness-v2.csv`. **WXR publish status is not launch approval.**
4. Wave 1 only. Effective indexable count, not release count.
5. Sitemap and indexing only after the gate passes.

---

## 2. Standing

Unchanged throughout: no invented facts, no remote fetching, no assertion weakened to fit an output limitation, no instruction document edited, immutable files immutable, `CONTEXT.md` and hash table at every gate.

## 3. Outstanding decisions carried into this block

- `/gallery/` — 108 words, no images, not a gallery. Withdraw, repurpose as a finishes page, or keep empty and noindexed.
- The kit tagline "Camden based Concrete Company Site" is a location claim that is not supportable from Pakenham.
- `service_areas` answered from where work will actually be done, not from where pages exist.
- The 45 unresearched suburbs — deferred under D22, not dropped.
- Site mark — wordmark specified, not implemented, pending the Astra export.
