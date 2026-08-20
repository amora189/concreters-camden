# CODEX BUILD 2 — Camden Concreting, Stages 21–31

**Paste this entire file into Codex as the instruction for the next work block. It continues `CODEX-BUILD.md`, which covered Stages 0–10, and the Stage 11–20 staging work recorded in `CONTEXT.md`.**

You work in stages. **Each stage ends with a STOP GATE. You print the gate report and wait for my approval before starting the next stage.** If a gate fails, fix it and re-run. If you cannot fix it, stop and ask. Never proceed past a known failure.

You produce files on disk. You do not deploy. You do not touch a live site. You do not perform the authoritative staging import in this work block.

---

## 0. Read first

`CONTEXT.md` is the authoritative statement of current state. Read it and do not restate it back to me.

Current state in one line: 156 pages exist in a validated WXR, 0 are index-ready, the launch gate is NO-GO, and the authoritative staging import is blocked on two owner-supplied inputs (83 image binaries, Astra Customizer export).

### Input files that must exist

| File | Authority |
|---|---|
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | Source WXR. **Never modify.** |
| `camden-concreting-import.xml` | Validated build artifact. **Never modify.** All changes are new artifacts, patches or scripts run against a copy. |
| `camden-site-structure-and-silo.md` | Architecture: URLs, slugs, silo, link rules A–G, clone procedure, footprint rules |
| `expansion-300-pages.md` | Expanded architecture: suburb list, service list, guide taxonomy, wave plan, uniqueness enforcement, image rules |
| `intersection-differentiators.json` | **Sole authority on which intersection pages exist** |
| `camden-concreting-seo-spec.md` | §5 module/anti-doorway rules, §6 meta constraints, §7 schema plan, §10 |
| `suburbs.json`, `suburbs-expanded.json` | Per-suburb data |
| `oran-park-gold-standard.md` | Copy pattern and register |
| `codex-clone-prompt.md` | Elementor widget field map, mutation rules |

**Stage 21 asserts every one of these is present before anything else runs.** If a file is missing, stop and list what is missing. Do not reconstruct a missing data file from the WXR, from another document, or from inference.

---

## 1. Precedence — read before reading the files

These conflicts are real and you will hit them. Earlier documents were not retro-edited.

| Conflict | Resolution |
|---|---|
| `expansion-300-pages.md` §1 budgets 300 pages / 180 intersections | **Dead figure.** `intersection-differentiators.json` corrects it: 35 buildable intersections, 155 pages, and `CONTEXT.md` records 156 built (155 + guide hub). **156 is the build. There is no 300-page target.** |
| Any suburb or service intersection not listed in `intersection-differentiators.json` | **Does not exist.** Per that file's `hard_rule`: do not generate it, do not invent a differentiator to unlock it. |
| `camden-concreting-seo-spec.md` §8 specifies Astro | **Superseded. WordPress wins.** Use the seo-spec only for §5, §6, §7, §10. Ignore its §2 URL map, §8 stack and §9 build order. |
| seo-spec §9 and `suburbs.json` imply 11 services; `CODEX-BUILD.md` §3 built 7; `expansion-300-pages.md` §3 specifies 10 | **10 service pages** — the 7 plus driveway replacement, shed & garage slabs, crossovers & laybacks. |
| seo-spec §5 has a 10-module suburb template; structure doc §5.1 has 11 | **Structure doc's 11 modules win** (that is what was built). Stage 21 must emit an explicit crosswalk between the two numberings, because the `noindex` gate is defined against seo-spec module numbers 6 and 7 and must be re-expressed against the built module numbers. Do not assume the mapping — derive it from module content and print it. |
| Structure doc §8 lists 6 guides; expansion §5 lists 35 | **35 guides plus the hub.** |
| `CODEX-BUILD.md` gate 10 says no sentence on >2 pages, ≥60% unique for all pages; expansion §8 says 5-gram on >3 pages, and per-class thresholds | **Apply the stricter of the two at every point:** 5-gram appearing on >2 pages is a failure; suburb ≥60%, intersection ≥50%, guide ≥85% unique body words; no pair in a class >40% overlap. |
| Expansion §7 wave table was written for 300 pages (Wave 5 = 180 intersections) | **Recompute all waves against the real 156.** Stage 27 owns this. |
| `/concreters-camden/` or `/concreters-camden-town/` | **Never build.** The homepage owns `concreters camden`. |

Where any document gives a specific figure (32 MPa, 125mm, SL72, 800mm vs 900mm footpath allocation, 1200mm, 4.0–5.5m, 4%, 1:6), reproduce it exactly. Never round, soften or paraphrase a specification.

---

## 2. Hard rules — violating any of these means stop and report

1. **Never invent a business fact.** No ABN, licence number, insurance detail, address, phone number, price, review, completed job, council fee, permit threshold, soil classification or performance claim. If a fact is missing, emit a blocking marker and an owner question. Do not fill it, do not infer it from a neighbouring suburb, do not carry a Melbourne figure across.
2. **Never invent a differentiator.** Suburb `unique_local_variable` and `intersection_differentiators.{service}` fields marked `REQUIRED-RESEARCH` stay unfilled. Any page without one builds `draft` + `noindex` and does not count toward any live total.
3. **No remote media fetching. Ever.** Do not generate, synthesise, upscale or substitute an image that could be mistaken for a real Camden job photo.
4. **WXR `publish` status is not launch approval.** Do not remove noindex from anything. Do not create or submit a sitemap. Do not run the authoritative staging import in this block.
5. **Victorian blocklist stays at zero:** Melbourne, Werribee, Wyndham, Point Cook, Tarneit, Truganina, Hoppers Crossing, Riverwalk, Harpley, Victoria, VIC, `03 4427 9541`, `bestconcretersmelbourne.com.au`. The known Victorian area code on the Camden number stays **flagged as a blocker, not silently corrected**.
6. **Never restructure an Elementor layout,** change a widget type, or improve the design. Preserve every `id`, `elType`, `widgetType`, `settings.classes`, `_elementor_used_global_class`, `__globals__` key and style/spacing/typography key.
7. Australian English throughout.
8. If a transformation is ambiguous, stop and ask rather than guessing.

---

# STAGE 21 — Input assertion and spec reconciliation v2

The build now spans six governing documents written at different times with contradictory numbers. Before any further work, collapse them into one machine-readable ledger.

**DO:**
1. Assert every input file in §0 is present and parses. Stop and list gaps if not.
2. Write `build/21-spec-ledger.json`: the single resolved specification. Per page class — count, URL pattern, module template, uniqueness threshold, status on import, wave, and the exact clause and source document each value came from. Every value must cite its source; nothing may be asserted without one.
3. Write `reports/21-module-crosswalk.md`: the seo-spec 10-module ↔ structure-doc 11-module mapping, derived from module content, with the `noindex` gate restated against built module numbers.
4. Write `reports/21-reconciliation-v2.md`: every conflict in §1 above, how it resolved, and **any conflict you found that is not listed in §1**. That last list is the important output — flag it loudly.
5. Reconcile the ledger against what is actually in `camden-concreting-import.xml`. Report every divergence between spec and artifact. Do not fix them yet.

**STOP GATE 21.** Ledger totals must reconcile to 156 pages by class. Print the class table, the crosswalk, and the unlisted-conflict list.

---

# STAGE 22 — Media and Astra intake harness

Both P0 blockers are owner-supplied. Build the harness that makes the eventual import one-shot.

**DO:**
1. Create `source-inputs/media/` and `source-inputs/astra/`, each with a README stating exactly what must be dropped in — expected filenames pulled from `build/stage8-image-map.json` and `reports/08-image-rename-map.csv`.
2. Write `scripts/22-media-audit.py`, fail-closed: all 83 required filenames present; exact filename match with no `-1` / `-scaled` / suffix drift; MIME type; dimensions; checksum recorded; file-size sanity; no unexpected extras. Non-zero exit and a missing-file manifest on any gap.
3. Write `scripts/22-astra-audit.py`: validate the file is a genuine Astra theme-mods / Customizer export and report which mods it contains, so a partial export is caught before import rather than after.
4. Confirm `reencode-images.sh` (strip EXIF, resize 98%, quality 82) is present and idempotent, and that its output feeds the audit — footprint requirement, not optimisation.

**STOP GATE 22.** Run both audits against the empty directories. Both must exit non-zero with a complete human-readable list of exactly what is missing. `reports/22-media-intake.md`.

---

# STAGE 23 — Evidence register and owner-question set

**DO:**
1. Parse `reports/placeholders.md` and the WXR into `reports/23-evidence-register.csv`: one row per marker occurrence — type (`PLACEHOLDER` / `REAL_PHOTO_PENDING` / `VERIFY`), page ID, slug, page class, tier, exact surrounding context, the fact required, who can supply it, and whether it blocks indexing for that page.
2. Reconcile against the recorded totals (163 markers: 111 / 47 / 5). **If your count differs, report the discrepancy. Do not silently reconcile.**
3. Add every `REQUIRED-RESEARCH` field across the 45 unresearched suburbs in `suburbs-expanded.json` to the register as blocking rows. These are evidence gaps even though they are not marker strings.
4. Write `reports/23-owner-questions.md`: the deduplicated minimum question set, grouped, ordered so answering the top items unblocks the most pages. **No question may suggest its own answer.** Include the count of pages each answer unblocks.
5. Write `reports/23-page-block-map.csv`: page → blocking marker IDs → count → clearable-by (owner fact / photo / council source / research). This is the gate input for every release decision after this.
**STOP GATE 23.** Every marker occurrence appears exactly once. No marker is marked resolved. Print the top 15 questions by pages-unblocked.

---

# STAGE 24 — Image distribution and alt-text audit

83 images across 156 pages and 1,085 Elementor references. Reuse is fine; concentration and duplicated alt text are not.

**DO:**
1. Write `reports/24-image-distribution.csv`: per image — attachment ID, filename, page count, list of pages, and whether it exceeds the ~15-page cap from `expansion-300-pages.md` §9.
2. Flag every image over the cap with a redistribution proposal. Do not redistribute yet.
3. Audit alt text: every occurrence of the same image on a different page must have alt text written for that page's context. Emit `reports/24-alt-duplication.csv` listing every image whose alt text repeats verbatim across pages.
4. Flag every `REAL_PHOTO_PENDING` slot that is currently filled by a re-encoded Melbourne image. Those are false-claim risks, not cosmetic issues — list them separately at the top of the report.

**STOP GATE 24.** `reports/24-images.md` with three counts: images over cap, alt strings duplicated, pending-photo slots currently occupied by source-site imagery.

---

# STAGE 25 — Uniqueness enforcement at 156 pages

Replace the Stage 4/7/9 spot checks with the mechanical enforcement in `expansion-300-pages.md` §8.

**DO:**
1. Build `scripts/25-shingle-index.py`: a global 5-gram index across every page's body text. Flag any 5-gram appearing on more than 2 pages (stricter rule wins).
2. Enforce per-class thresholds: suburb ≥60% unique body words, intersection ≥50%, guide ≥85%. Pairwise overlap ≤40% within a class.
3. Differentiator assertion: every suburb and intersection page must carry a non-empty `unique_local_variable` or `intersection_differentiators.{service}`. Fail the page otherwise.
4. Opening-paragraph test: for every suburb and intersection page, assert the first 80 words are false if pasted onto a sibling page. Report pass/fail per page with the reason.
5. Write `reports/25-uniqueness.md`: per-page and per-pair results, plus a ranked remediation list.

**Failing pages are not rewritten weaker — they are held. Report them; do not soften a page to pass a gate.**

**STOP GATE 25.** Print the per-class summary table and every failing page with its failure mode.

---

# STAGE 26 — Intersection page audit

**DO:** Audit all 35 intersection pages in the WXR against `intersection-differentiators.json`:
1. Exactly 35 exist; no extras; every one appears in the JSON.
2. Each page's differentiator text traces to the JSON `differentiator` value and is not diluted or generalised.
3. Each links up to both `parent_service` and `parent_suburb`, and both parents exist in the build.
4. No intersection is the only page targeting its suburb — the suburb page always exists first.
5. Every intersection is `draft` on import.
6. Shared spec component length is within the ~150-word budget from expansion §4 and does not push the page below the 50% uniqueness floor.

**STOP GATE 26.** `reports/26-intersections.md`, one row per page, plus explicit confirmation that zero intersection pages exist outside the JSON.

---

# STAGE 27 — Wave re-plan against 156 and Wave 1 menu spec

The expansion §7 wave table was sized for 300 pages. Recompute it.

**DO:**
1. Write `reports/27-wave-plan.md`: waves 1–5 as explicit page sets against the real 156, with per-page entry conditions drawn from the Stage 23 block map. Wave 1 contains only pages whose blockers are clearable by owner-supplied facts.
2. Enforce: the six Tier 1 suburb pages and Gallery stay `noindex,follow` until evidence and photography gates pass; **the guide hub never publishes without its first approved guides**; the 45 unresearched suburbs cannot enter any wave.
3. Write `build/27-wave1-menus.json`: exact Wave 1 menu structures with zero links to draft or noindex-pending pages, plus a diff against the 65 imported menu items showing which are removed or held. Preserve `_menu_item_menu_item_parent` relationships.
4. Write `scripts/27-menu-lint.py`: fails if any menu item resolves to a draft page, a noindex page, or a 404.

**STOP GATE 27.** Menu lint passes against the Wave 1 JSON and fails when pointed at the full imported menu set. Print the wave table with per-wave page counts and gates.

---

# STAGE 28 — Deterministic preflight runner

One command, one verdict.

**DO:** Write `scripts/28-preflight.sh` running, in order and fail-closed: the 15 Stage 9 gates → occupied post-ID collision audit → media audit (22) → Astra audit (22) → Elementor image-reference count (1,085 refs across 83 attachments) → uniqueness gates (25) → intersection audit (26) → menu lint (27) → Victorian blocklist scan → placeholder-in-schema scan.

Output `reports/28-preflight.md` with a single top-line **GO / NO-GO** and per-gate detail. Any FAIL makes the whole run NO-GO. No gate may be skipped or marked advisory.

**STOP GATE 28.** Running it now must return NO-GO citing the missing media and Astra inputs plus any genuine content gate failures — and nothing failing for an unrelated or spurious reason.

---

# STAGE 29 — Authoritative staging scaffolding (PHP 8.3)

**DO:** Create `staging-authoritative/`, clearly separated from the disposable `staging/`:
1. Pinned `docker-compose` — PHP **8.3** (the disposable 8.4 environment logs an Elementor deprecation), WordPress, MariaDB, all versions pinned explicitly. Loopback-only binding, unexpected-host blocking, enforced global noindex.
2. Scripts for clean checkpoint creation, DB + uploads rollback, and a **local-only media importer** that preserves exact filenames and requested attachment IDs with remote fetching disabled at the WordPress level.
3. `reports/29-staging-plan.md`: the exact command sequence from clean checkpoint to verified import, with a rollback step after every mutating step, and the post-import task order from `CODEX-BUILD.md` Stage 10 (search-replace dry-run first, delete `_elementor_element_cache`, regenerate CSS, sync library, assign menu locations).

**Do not start containers. Do not import anything.** The plan must state plainly that it does not run until Stage 28 returns GO.

**STOP GATE 29.** Print the command sequence and the rollback points.

---

# STAGE 30 — Fail-closed facts, schema and forms

**DO:**
1. Create `data/verified-facts.yml`: every business fact the site needs, as an explicitly empty typed required field — legal entity behind "CoreX Concreters Camden", ABN, NSW Fair Trading licence, insurance, street address **and whether it is staffed**, phone number **and proof of current routing**, service areas, real per-m² ranges, real reviews. Every field starts `verified: false`.
2. Write `scripts/30-build-schema.py` implementing `camden-concreting-seo-spec.md` §7: one `@graph` per page, permanent `@id` spine, `LocalBusiness`/`GeneralContractor` **only** on `/` and `/contact/`, suburb and intersection pages get `Service` + `areaServed` referencing `#localbusiness`. It must refuse to emit any node whose required fields are unverified — including omitting `LocalBusiness` entirely with no verified staffed address — and log every refusal with the reason.
3. Implement the §7.6 gates: valid JSON, every referenced `@id` defined, no `LocalBusiness` outside the two allowed URLs, every `FAQPage` Q&A verbatim in rendered HTML, **zero placeholder strings in any emitted JSON-LD**.
4. Write `reports/30-forms-spec.md`: Fluent Forms form ID 3 — fields, recipient, consent and privacy basis, SMTP delivery requirement, use on About and Gallery. A specification requiring approval, **not an implementation**.

**STOP GATE 30.** Running the schema builder now produces either nothing or minimal non-identity schema, and logs every refused type. Print the refusal log.

---

# STAGE 31 — The crossover requirements calculator (gated)

`expansion-300-pages.md` §6 and seo-spec §10 both identify this as the one asset that earns links passively. It is also the easiest place in the entire build to publish a wrong number across four councils.

**DO:**
1. Write `reports/31-calculator-spec.md`: input model (address or LGA → application type, width and grade limits, fee, lodgement path), output model, and the four LGA rule sets as **empty, sourced-fee-required structures** — Camden, Liverpool, Campbelltown, Wollondilly.
2. Create `data/council-specs.yml` with every figure `verified: false` plus a required `source_url` and `sighted_date` per figure.
3. Build the calculator UI and logic against that data file, with a hard guard: **if any figure used in a given path is unverified, the tool renders "we can't confirm this figure — contact the council" rather than a number.** No fallbacks, no approximations, no "typically around".
4. Do not publish it. It ships `draft` + `noindex` and is listed as a Wave 4 candidate.

**STOP GATE 31.** Demonstrate the guard: every LGA path currently renders the unverified state, and the tool cannot be made to output a number from unverified data.

---

# Start

Begin with **Stage 21 only**. Print the file tree you intend to create, implement, run the acceptance checks, print the gate report, then stop for approval.
