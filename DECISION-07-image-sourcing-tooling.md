# DECISION RECORD 07 — image sourcing tooling

Cite in `build/21-spec-ledger.json`. Two clauses. Applies to Phase F of `RUN-BLOCK-02-on-inputs.md`.

---

## D33 — SerpApi is permitted as a discovery mechanism, not as a licence

`IMAGE-REPLACEMENT-PROMPT.md` §2.1 permits only Unsplash, Pexels and Openverse, and prohibits search-engine scrapers. A SerpApi-based finder was subsequently supplied. That contradiction is mine and is resolved here.

**Permitted:** the SerpApi Google Images API with `licenses=fmc` (free to use, share or modify, even commercially). It is a paid, terms-compliant query against Google's own usage-rights filter, not a scraper, and it returns structured results with source URLs.

**Prohibited, unchanged:** Selenium or requests-based Google Images scrapers, and any tool returning images without a retrievable source page.

**Conditions, all mandatory:**

1. `licenses=fmc` is a **discovery filter, not a licence determination.** It reflects what the hosting page declares about itself. It is not verification.
2. Every candidate's licence is verified on its `page_url` — the hosting page, not the image URL — **before download**. No exceptions, no batch approval.
3. Any candidate whose licence cannot be established on the source page is discarded. Absence of a stated licence is not permission.
4. Unsplash, Pexels and Openverse remain the preferred sources. Use SerpApi where a brief returns nothing usable from them, and expect the `fmc` pool to be small.
5. `reports/33-licence-register.csv` records licence, source URL, photographer, retrieval date and attribution requirement for every image shipped, regardless of source. Permanent build artifact.
6. **No `REAL_PHOTO_PENDING` slot is filled from any of these sources.** Superseded by D32 in any case — the evidential modules are removed, not restocked.

---

## D34 — Tooling locations

`find_images.py` is not in the repo. It exists at `~/camden-images/find_images.py` in WSL, alongside a venv with `serpapi` installed and `SERPAPI_KEY` in the environment.

**DO, when Phase F runs:**
1. Copy it into `scripts/` under version control. A build tool living outside the repo has no provenance and cannot be audited — the same reasoning that moved standing guidance out of agent-local memory under D14.
2. Update it to read the **regenerated** spec CSV. The existing `reports/33-image-replacement-spec.csv` describes 228 page-slots of which 110 are on withdrawn pages; it describes a site that no longer exists. Regenerate against the 77-page architecture before the script runs.
3. Broaden the briefs to decorative subjects. The originals were written to fill slots on service and suburb pages that are now rewritten or withdrawn, and narrow briefs return almost nothing under `fmc`.
4. `ImageMagick` is a Phase B precondition for the re-encode driver. Record it as a documented environment requirement alongside PHP 8.3 and the pinned Docker versions, not as an ad-hoc install.
