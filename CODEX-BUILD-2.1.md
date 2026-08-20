# CODEX BUILD 2.1 — Camden Concreting, Stages 21–32

**This file replaces `CODEX-BUILD-2.md` and Amendments A, B and C. It is the single governing instruction for this work block. Archive the other four; do not read them again except to check provenance.**

Continues `CODEX-BUILD.md` (Stages 0–10) and the Stage 11–20 staging work recorded in `CONTEXT.md`.

You work in stages. **Each stage ends with a stop gate. Print the gate report and wait for approval before the next stage.** If a gate fails, fix it and re-run. If you cannot fix it, stop and ask. Never proceed past a known failure.

You produce files on disk. You do not deploy, do not touch a live site, and do not perform the authoritative staging import in this work block.

---

## 0. First actions

**Before anything else:**

1. Read `CONTEXT.md`. It is the authoritative statement of current state. Do not restate it back to me.
2. Reconcile against work already done. Gate 21 was passed against `CODEX-BUILD-2.md` plus Amendment B. Every citation in `build/21-spec-ledger.json` and `reports/21-reconciliation-v2.md` that points at `CODEX-BUILD-2.md §x` or `Amendment A/B/C` must be re-pointed at the equivalent clause of this file. Produce `reports/21-citation-remap.md` showing old citation → new citation for every one. **No spec value may lose its citation in the remap.**
3. Restore `CODEX-BUILD-2.md` to its original supplied content. It was edited during Amendment B application; that was not instructed. If exact restoration is impossible, write `reports/21-governing-doc-diff.md` listing every change made to it.
4. Confirm every input file in §1 is present and parses.

Current state in one line: 156 pages in a validated immutable WXR plus one planned supplementary page, 0 index-ready, launch gate NO-GO, authoritative staging import blocked on two owner-supplied inputs (83 image binaries, Astra Customizer export).

---

## 1. Input files

| File | Authority |
|---|---|
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | Source WXR. **Never modify.** |
| `camden-concreting-import.xml` | Validated main build artifact, 156 pages. **Never modify.** All changes are new artifacts, patches or scripts run against a copy. |
| `camden-site-structure-and-silo.md` | Architecture: URLs, slugs, silo, link rules A–G, clone procedure, footprint rules |
| `expansion-300-pages.md` | Expanded architecture: suburb list, service list, guide taxonomy, wave plan, uniqueness enforcement, image rules |
| `intersection-differentiators.json` | **Sole authority on which intersection pages exist** |
| `camden-concreting-seo-spec.md` | §5 module and anti-doorway rules, §6 meta constraints, §7 schema plan, §10 |
| `suburbs.json`, `suburbs-expanded.json` | Per-suburb data |
| `oran-park-gold-standard.md` | Copy pattern and register |
| `codex-clone-prompt.md` | Elementor widget field map, mutation rules |

If a file is missing, stop and list what is missing. **Never reconstruct a missing data file** from the WXR, from another document, or from inference.

---

## 2. Precedence — read before reading the files

These conflicts are real. Earlier documents were not retro-edited.

| Conflict | Resolution |
|---|---|
| `expansion-300-pages.md` §1 budgets 300 pages / 180 intersections | **Dead figure.** `intersection-differentiators.json` corrects it to 35 buildable intersections. **There is no 300-page target.** |
| Any intersection not listed in `intersection-differentiators.json` | **Does not exist.** Per that file's `hard_rule`: do not generate it, do not invent a differentiator to unlock it. |
| Total page count | **157 combined architecture** — 156 in the immutable main WXR plus 1 supplementary calculator page (§4.11). The main WXR stays at 156. |
| `camden-concreting-seo-spec.md` §8 specifies Astro | **Superseded. WordPress wins.** Use the seo-spec only for §5, §6, §7, §10. Ignore its §2 URL map, §8 stack, §9 build order. |
| seo-spec §9 and `suburbs.json` imply 11 services; `CODEX-BUILD.md` §3 built 7; expansion §3 specifies 10 | **10 service pages** — the 7 plus driveway replacement, shed & garage slabs, crossovers & laybacks. |
| seo-spec §5 has a 10-module suburb template; structure doc §5.1 has 11 | **Structure doc's 11 modules win** (that is what was built). The `noindex` gate is defined against seo-spec modules 6 and 7 and must be re-expressed against built module numbers. **Derive the crosswalk from module content; do not assume it.** |
| Structure doc §8 lists 6 guides; expansion §5 lists 35 | **35 guides plus the hub.** |
| `CODEX-BUILD.md` gate 10 vs expansion §8 uniqueness rules | **Stricter of the two at every point:** a 5-gram on more than 2 pages fails; suburb ≥60%, intersection ≥50%, guide ≥85% unique body words; no pair in a class exceeds 40% overlap. |
| Expansion §7 wave table was sized for 300 pages | **Recompute against the real 157.** §4.7 owns this. |
| Cost/comparison page count: expansion §6 lists 10 | **11.** The crossover requirements calculator is the eleventh (§4.11). |
| `/concreters-camden/` or `/concreters-camden-town/` | **Never build.** The homepage owns `concreters camden`. |

Where any document gives a specific figure (32 MPa, 125mm, SL72, 800mm vs 900mm footpath allocation, 1200mm, 4.0–5.5m, 4%, 1:6), reproduce it exactly. Never round, soften or paraphrase a specification.

---

## 3. Standing rules — violating any of these means stop and report

1. **Never invent a business fact.** No ABN, licence number, insurance detail, address, phone number, price, review, completed job, council fee, permit threshold, soil classification or performance claim. If a fact is missing, emit a blocking marker and an owner question. Do not fill it, do not infer it from a neighbouring suburb, do not carry a Melbourne figure across.
2. **Never invent a differentiator.** Fields marked `REQUIRED-RESEARCH` stay unfilled. Any page without a real `unique_local_variable` or `intersection_differentiators.{service}` builds `draft` + `noindex` and counts toward no live total.
3. **No remote media fetching, ever.** Never generate, synthesise, upscale or substitute an image that could be mistaken for a real Camden job photo.
4. **WXR `publish` status is not launch approval.** Do not remove noindex from anything. Do not create or submit a sitemap. Do not run the authoritative staging import in this block.
5. **Victorian blocklist stays at zero:** Melbourne, Werribee, Wyndham, Point Cook, Tarneit, Truganina, Hoppers Crossing, Riverwalk, Harpley, Victoria, VIC, `03 4427 9541`, `bestconcretersmelbourne.com.au`. The Victorian area code on the Camden number stays **flagged as a blocker, not silently corrected**.
6. **Never restructure an Elementor layout,** change a widget type, or improve the design. Preserve every `id`, `elType`, `widgetType`, `settings.classes`, `_elementor_used_global_class`, `__globals__` key and style/spacing/typography key.
7. **This file and every archived amendment are read-only.** Never edit an instruction document. All resolutions, precedence decisions and amended figures live in `build/21-spec-ledger.json`, cited to the clause that produced them. The ledger is the mutable record; the instructions are not. Future amendments arrive as new numbered files.
8. **No assertion may be narrowed, relaxed or made lossy to accommodate an output, console or logging limitation.** If a check cannot run at full fidelity, it fails and is reported as blocked. See §3.1.
9. Australian English throughout.
10. If a transformation is ambiguous, stop and ask rather than guessing.

### 3.1 Encoding integrity (immediate, applies retroactively)

Two Stage 21 assertions were switched to ASCII-stable substrings to work around a Windows console encoding failure. That makes a gate pass without making the check work.

Non-ASCII characters are load-bearing here: en dashes in specification ranges, em dashes throughout the copy, `m²` and `32 MPa` in specifications, and Rank Math descriptions measured against a 140–160 character bound where every character counts. A duplication, blocklist, meta-length or uniqueness gate that cannot read non-ASCII passes by blindness.

**DO:**
1. Fix the environment, not the test: `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `sys.stdout` reconfigured to UTF-8, every file opened with `encoding='utf-8'` declared. Where console output stays unreliable, write reports to disk and read them back rather than trimming what the assertion compares.
2. Restore both weakened assertions to full-fidelity comparison against the exact source strings and re-run.
3. Audit every script written so far for the same class of substitution — ASCII-only comparison, character stripping, `errors='ignore'`, `errors='replace'`, transliteration, normalisation collapsing dash variants. List each in `reports/21-encoding-audit.md` with file, line, and what it currently fails to detect.
4. Add a preflight canary: a fixture containing an em dash, en dash, `²` and non-breaking space, asserted to survive a full read-write-compare cycle. Canary failure makes the whole run NO-GO regardless of every other gate.

### 3.2 Gate report contents (every gate, from now on)

Every stop gate report includes, in addition to its stage-specific output:

1. **`CONTEXT.md` update and diff.** Record the date (Australia/Sydney), latest completed stage, **what was actually verified** (not attempted), remaining blockers, next safe action. Never describe a generated artifact, smoke test, WXR status or local container as a live site, launch or approval. Never reduce the blocker list unless a blocker was cleared by verified evidence — a script that checks a blocker is not a cleared blocker. Keep the index-ready count accurate; nothing in Stages 21–32 can raise it above 0. If findings contradict `CONTEXT.md`, say so explicitly rather than silently overwriting.
2. **Hash table.** SHA-256 of `camden-concreting-import.xml`, `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml`, `build/stage9-page-manifest.json`, `build/stage8-image-map.json`, `reports/08-image-rename-map.csv`, and this file. **Any change to a hash on a file that is supposed to be immutable is a hard failure — stop and report.**

---

# 4. Stages

## 4.21 — Stage 21: input assertion and spec reconciliation (re-open and re-print)

Gate 21 was passed against an incomplete instruction set. Re-open it, back-fill, re-print.

**DO:**
1. Complete §0 items 1–4, including the citation remap and governing-doc restoration.
2. `build/21-spec-ledger.json` — the single resolved specification. Per page class: count, URL pattern, module template, uniqueness threshold, status on import, wave, and the exact clause and source document each value came from. Every value cites its source; nothing is asserted without one.
3. `reports/21-module-crosswalk.md` — seo-spec 10-module ↔ structure-doc 11-module mapping, derived from module content, with the `noindex` gate restated against built module numbers.
4. `reports/21-reconciliation-v2.md` — every conflict in §2, how it resolved, **and every conflict you found that is not listed in §2.** That last list is the most important output of this stage. Print it explicitly, or state as a finding that zero unlisted conflicts were found — never by omission. Across six governing documents written at different times, zero would be a surprising result.
5. **Three-way reconciliation.** Reconcile the ledger against `build/stage9-page-manifest.json` **and** `camden-concreting-import.xml`, reporting divergence three ways: spec vs manifest, spec vs XML, manifest vs XML. The third is the critical one — if the manifest and the XML disagree, one of two source-of-truth files is wrong, and that is stop-and-ask, not reconciliation.
6. Reconcile the class table against `CONTEXT.md`: 1 home, 4 utility, 10 service, 60 suburb, 1 guide hub, 35 guides, 35 intersections, **11 cost/comparison** = **157 combined**, of which 156 are in the main WXR. Report any differing class count; do not adjust it.
7. §3.1 encoding audit and restored assertions.

**Known-good asymmetry:** the ledger reconciles to 157 while the manifest and main XML reconcile to 156, because the eleventh cost page is a supplementary artifact. This specific divergence is expected and explained. **Every other manifest-vs-XML divergence is stop-and-ask.**

**GATE 21.** Print: class table reconciling to 157/156, crosswalk, unlisted-conflict list, three-way reconciliation, encoding audit, citation remap, governing-doc restoration status, plus §3.2 items.

---

## 4.22 — Stage 22: media and Astra intake harness

Both P0 blockers are owner-supplied. Build the harness that makes the eventual import one-shot.

**DO:**
1. Create `source-inputs/media/` and `source-inputs/astra/`, each with a README stating exactly what must be dropped in, filenames pulled from `build/stage8-image-map.json` and `reports/08-image-rename-map.csv`.
2. `scripts/22-media-audit.py`, fail-closed: all 83 filenames present; exact match with no `-1` / `-scaled` / suffix drift; MIME type; dimensions; checksum recorded; file-size sanity; no unexpected extras. Non-zero exit and a missing-file manifest on any gap.
3. `scripts/22-astra-audit.py`: validate the file is a genuine Astra theme-mods / Customizer export and report which mods it contains, so a partial export is caught before import rather than after.
4. Confirm `reencode-images.sh` (strip EXIF, resize 98%, quality 82) is present, idempotent, and feeds the audit — footprint requirement, not optimisation.

**GATE 22.** Both audits run against the empty directories and exit non-zero with a complete list of what is missing. `reports/22-media-intake.md`.

---

## 4.23 — Stage 23: evidence register and owner-question set

**DO:**
1. `reports/23-evidence-register.csv` — one row per marker occurrence: type (`PLACEHOLDER` / `REAL_PHOTO_PENDING` / `VERIFY`), page ID, slug, class, tier, exact surrounding context, fact required, who can supply it, whether it blocks indexing.
2. Reconcile against the recorded totals (163: 111 / 47 / 5). **If your count differs, report the discrepancy. Do not silently reconcile.**
3. Add every `REQUIRED-RESEARCH` field across the 45 unresearched suburbs in `suburbs-expanded.json` as blocking rows. These are evidence gaps even though they are not marker strings.
4. `reports/23-owner-questions.md` — deduplicated minimum question set, grouped, ordered so the top answers unblock the most pages, with the page count each answer unblocks. **No question may suggest its own answer.**
5. `reports/23-page-readiness-v2.csv` — a **superset of the existing `reports/18-page-readiness.csv`**, joined on page ID, preserving every existing column and adding: blocking marker IDs, blocking count, clearable-by category (owner fact / photo / council source / research), wave assignment, effective robots directive. Every row in the original must appear; report any page in one and not the other. **No `Index-ready` value may change from `no` in this work block.** 157 rows. Update `CONTEXT.md`'s source-of-truth list to note v2 supersedes the original; do not delete the original.

Do not create a separate block-map artifact. One readiness record only.

**GATE 23.** Every marker occurrence appears exactly once, none marked resolved. Print the top 15 questions by pages-unblocked.

---

## 4.24 — Stage 24: image distribution and alt-text audit

83 images, 157 pages, 1,085 Elementor references. Reuse is fine; concentration and duplicated alt text are not.

**DO:**
1. `reports/24-image-distribution.csv` — per image: attachment ID, filename, page count, page list, whether it exceeds the ~15-page cap from expansion §9. Page denominator is 157.
2. Flag every image over the cap with a redistribution proposal. Do not redistribute yet.
3. `reports/24-alt-duplication.csv` — every image whose alt text repeats verbatim across pages. Each occurrence needs alt text written for that page's context.
4. **At the top of the report:** every `REAL_PHOTO_PENDING` slot currently filled by a re-encoded Melbourne image. These are false-claim risks, not cosmetic ones.

**GATE 24.** `reports/24-images.md` with three counts: images over cap, alt strings duplicated, pending-photo slots occupied by source-site imagery.

---

## 4.25 — Stage 25: uniqueness enforcement

Replace the Stage 4/7/9 spot checks with mechanical enforcement per expansion §8.

**DO:**
1. `scripts/25-shingle-index.py` — global 5-gram index across every page's body text. Flag any 5-gram on more than 2 pages.
2. Enforce sourced thresholds: suburb ≥60%, intersection ≥50%, guide ≥85% unique body words; pairwise overlap ≤40% within a class.
3. Differentiator assertion: every suburb and intersection page carries a non-empty `unique_local_variable` or `intersection_differentiators.{service}`. Fail the page otherwise.
4. Opening-paragraph test: for every suburb and intersection page, assert the first 80 words are false if pasted onto a sibling page. Report pass/fail with reason.
5. **Measure all 157 pages**, including the classes with no sourced threshold — 10 service, 11 cost/comparison, guide hub, homepage, 4 utility. Measurement is unconditional even where no threshold exists; those 26 pages currently pass by not being tested.
6. **No source document specifies thresholds for those classes. Do not silently pick one.** Report measured uniqueness and worst-pair overlap per class, propose a threshold with reasoning, and mark each **`AWAITING APPROVAL — not enforced`**. Do not fail or hold a page against an unapproved threshold, and do not record an unapproved threshold in the ledger as sourced.
7. Flag separately any page in an untested class measuring below the loosest sourced threshold (50%). Those are a problem whatever threshold is later approved.

**Failing pages are held, not rewritten weaker.** Report them; never soften a page to pass a gate.

**GATE 25.** Per-class summary table plus every failing page with its failure mode.

---

## 4.26 — Stage 26: intersection page audit

Audit all 35 intersections against `intersection-differentiators.json`:

1. Exactly 35 exist, no extras, every one appears in the JSON.
2. Each differentiator traces to the JSON `differentiator` value, not diluted or generalised.
3. Each links up to both `parent_service` and `parent_suburb`, and both parents exist.
4. No intersection is the only page targeting its suburb — the suburb page always exists first.
5. Every intersection is `draft` on import.
6. The shared spec component is within the ~150-word budget from expansion §4 and does not push the page below the 50% floor.

**GATE 26.** `reports/26-intersections.md`, one row per page, plus explicit confirmation that zero intersection pages exist outside the JSON.

---

## 4.27 — Stage 27: wave re-plan and Wave 1 menu spec

**DO:**
1. `reports/27-wave-plan.md` — waves 1–5 as explicit page sets against the real 157, with per-page entry conditions from `reports/23-page-readiness-v2.csv`. Wave 1 contains only pages whose blockers are clearable by owner-supplied facts.
2. **State per wave: pages released, pages `noindex,follow`, and effective indexable count. The headline number is the effective indexable count, not the release count.** Wave 1 releases 21 pages but 6 Tier 1 suburbs and Gallery stay `noindex,follow` — effective indexable Wave 1 is **14**, and nothing may report 21 published as 21 indexed.
3. Enforce: Tier 1 suburbs and Gallery stay `noindex,follow` until evidence and photography gates pass; **the guide hub never publishes without its first approved guides**; the 45 unresearched suburbs enter no wave; the 11 cost/comparison pages stay `draft` until individually approved.
4. Assert no wave's release set contains a page whose `Index-ready` is `no` unless it is explicitly released as `noindex,follow`.
5. `build/27-wave1-menus.json` — exact Wave 1 menu structures with zero links to draft or noindex-pending pages, plus a diff against the 65 imported menu items showing which are removed or held. Preserve `_menu_item_menu_item_parent` relationships.
6. `scripts/27-menu-lint.py` — fails if any menu item resolves to a draft page, a noindex page, or a 404.

**GATE 27.** Menu lint passes against the Wave 1 JSON and fails against the full imported set. Print the wave table with release counts, noindex counts and effective indexable counts.

---

## 4.28 — Stage 28: deterministic preflight runner

**DO:** `scripts/28-preflight.sh`, fail-closed, in order: encoding canary (§3.1) → 15 Stage 9 gates → occupied post-ID collision audit **across both XML files** → media audit → Astra audit → Elementor image-reference count (1,085 across 83 attachments in the main file; supplementary file adds zero unresolved references) → uniqueness gates → intersection audit → menu lint → Victorian blocklist scan → placeholder-in-schema scan.

`reports/28-preflight.md` carries a single top-line **GO / NO-GO** with per-gate detail. Any FAIL makes the run NO-GO. No gate may be skipped or marked advisory.

**GATE 28.** Running it now returns NO-GO citing the missing media and Astra inputs plus genuine content failures — and nothing failing for a spurious or environmental reason.

---

## 4.29 — Stage 29: authoritative staging scaffolding (PHP 8.3)

**DO:** Create `staging-authoritative/`, clearly separated from the disposable `staging/`:

1. Pinned `docker-compose` — PHP **8.3** (the disposable 8.4 environment logs an Elementor deprecation), WordPress, MariaDB, all versions pinned explicitly. Loopback-only binding, unexpected-host blocking, enforced global noindex.
2. Scripts for clean checkpoint creation, DB + uploads rollback, and a **local-only media importer** preserving exact filenames and requested attachment IDs with remote fetching disabled at the WordPress level.
3. `reports/29-staging-plan.md` — the exact command sequence from clean checkpoint to verified import, **with a rollback point after every mutating step**, in this order: Astra Customizer import (discrete step, own verification, before content) → media → `camden-concreting-import.xml` → verify → rollback point → `camden-calculator-import.xml` → verify. Then the `CODEX-BUILD.md` Stage 10 post-import tasks: search-replace dry-run first, delete `_elementor_element_cache`, regenerate CSS and data, sync library.
4. **The settings that do not travel in a WXR**, each an explicit step with a verification check: **static homepage assignment** (Settings → Reading; verify the front page resolves to the imported homepage ID, not a posts archive); **permalinks** `/%postname%/` flushed, trailing slashes and canonicals verified against the served URL; **menu location assignment** for all five menus, verified against `build/27-wave1-menus.json` rather than the full imported set.
5. The post-import guide-side link edits from §4.11.6.

**Do not start containers. Do not import anything.** The plan states plainly that it does not run until Gate 28 returns GO.

**GATE 29.** Print the command sequence and every rollback point.

---

## 4.30 — Stage 30: fail-closed facts, schema and forms

**DO:**
1. `data/verified-facts.yml` — every business fact as an explicitly empty typed required field: legal entity behind "CoreX Concreters Camden", ABN, NSW Fair Trading licence, insurance, street address **and whether it is staffed**, phone number **and proof of current routing**, service areas, real per-m² ranges, real reviews. Every field starts `verified: false`.
2. `scripts/30-build-schema.py` implementing seo-spec §7: one `@graph` per page, permanent `@id` spine, `LocalBusiness`/`GeneralContractor` **only** on `/` and `/contact/`, suburb and intersection pages get `Service` + `areaServed` referencing `#localbusiness`. It refuses to emit any node whose required fields are unverified — including omitting `LocalBusiness` entirely with no verified staffed address — and logs every refusal with its reason.
3. Implement the §7.6 gates: valid JSON; every referenced `@id` defined; no `LocalBusiness` outside the two allowed URLs; every `FAQPage` Q&A verbatim in rendered HTML; **zero placeholder strings in any emitted JSON-LD**.
4. `reports/30-forms-spec.md` — Fluent Forms form ID 3: fields, recipient, consent and privacy basis, SMTP delivery requirement, use on About and Gallery. **A specification requiring approval, not an implementation.**

**GATE 30.** The schema builder produces either nothing or minimal non-identity schema. Print the refusal log.

---

## 4.11 — Stage 31: the eleventh cost page (crossover requirements calculator)

Owner decision: the crossover requirements calculator is the **eleventh cost/comparison page**. Combined total 157.

### 4.11.1 The main import file is not modified
`camden-concreting-import.xml` passed all 15 Stage 9 gates as a 156-page artifact and stays under the never-modify rule. The calculator ships as a separate supplementary artifact, `camden-calculator-import.xml`, imported after the main file in the same authoritative staging environment.

- Its `post_id` is allocated above the highest ID occupied **anywhere** in the main file — pages, attachments, menu items, Elementor kit, custom CSS records.
- Re-run the occupied post-ID collision audit across **both** files before either is imported. A collision is a hard failure.
- It claims no attachment ID from the 83 unless that image is genuinely used on the page. If it uses none, it declares no attachments.
- It carries no menu items. Menu placement is handled in §4.27.

### 4.11.2 Derive the URL and page shape; do not invent them
Before writing anything: read the ten existing cost/comparison pages in the main WXR and record their exact URL pattern, title pattern, module structure, word-count range and Rank Math meta shape in `reports/31-cost-page-inventory.md`. Confirm no crossover calculator already exists among them under another name — if one does, stop and ask. Derive the eleventh page's slug and title from the observed pattern; do not invent a new one, and do not apply the service-page `-south-west-sydney` convention unless the existing cost pages use it. Match the observed Elementor module structure. **Print the derived slug, title and module outline for approval before building the page body.**

### 4.11.3 The interactive component
Elementor has no native calculator. State and justify the implementation against Core Web Vitals before writing it. Default: HTML widget with inline vanilla JS — no framework, no external library, no CDN dependency. No render-blocking script. No layout shift on interaction; reserve the output area's height. **The page must be fully readable and useful with JavaScript disabled** — the four LGA rule sets render as static content and the calculator is an enhancement over that, not a replacement. Do not add a plugin, custom post type or shortcode the staging environment does not already have.

### 4.11.4 Fail-closed data guard
`data/council-specs.yml` — Camden, Liverpool, Campbelltown, Wollondilly. Every figure `verified: false` with a required `source_url` and `sighted_date`: application type, width limits, grade limits, fee, lodgement path per LGA.

**If any figure on a given path is unverified, that path renders "we can't confirm this figure — contact the council" instead of a number.** No fallbacks, no approximations, no "typically around", no carrying Camden's figure to Liverpool. The 800mm Oran Park footpath allocation against the 900mm Camden LGA default, and the 1200mm allocation width, are reproduced exactly where they appear and remain subject to the same `verified` flag. Zero placeholder strings in emitted JSON-LD.

### 4.11.5 Status, wave and promotion
**On import: `draft` + `noindex`.** Default wave: **4**, with the other ten cost pages. **Promotion clause:** promotable to Wave 2 once, and only once, all four LGAs' figures are `verified: true` with sighted sources. The gate is fee verification, not the calendar — an unverified calculator published early is four councils' worth of wrong numbers, and a verified one held to month nine is a self-inflicted delay on the only asset in the build designed to earn referring domains. Record the promotion as **awaiting owner approval**; never promote it yourself.

### 4.11.6 Internal links and the orphan declaration
The four LGA crossing guides each link to the calculator with descriptive, non-exact-match anchors. The calculator links up to `/concrete-crossovers-and-laybacks-south-west-sydney/`. Enforce existing link rules A–G for everything else; create no new rule.

Those guides live inside the never-modify main file, so the guide-side links are **post-import edits** — list them in the post-import runbook with exact target page IDs and anchor text, and do not edit the main file. Because the inbound links are post-import, the calculator is an orphan at the moment of import: **declare that explicitly in the orphan check** rather than letting the gate fail silently or be waived.

### 4.11.7 Propagate 157
Update, each citing this clause: `build/21-spec-ledger.json` (cost class 10 → 11, total 156 → 157); Stage 21 three-way reconciliation (record the known-good asymmetry); `reports/23-page-readiness-v2.csv` (157 rows, calculator `Index-ready: no`, blocked on four LGAs' fee verification); `reports/27-wave-plan.md` (Wave 4 +1, promotion clause, effective indexable counts unchanged since the page is noindex); `reports/24-image-distribution.csv` (denominator 157); `scripts/28-preflight.sh` (runs against both XMLs); `reports/29-staging-plan.md` (separately rollback-able calculator import); `CONTEXT.md` (composition line to 157, noting 156 in the validated import and 1 supplementary, index-ready **0 of 157**).

### 4.11.8 Validate the new page on its own terms
The main file's Stage 9 pass does not extend to the supplementary artifact.

| Gate | Scope |
|---|---|
| XML well-formed; Elementor JSON valid; round trip byte-matches | supplementary |
| Exactly one H1 | supplementary |
| Victorian blocklist zero occurrences | supplementary |
| Attachment/image IDs resolve | supplementary |
| Rank Math title 50–60 chars, description 140–160 chars | supplementary |
| Meta uniqueness — not structurally identical to any of the ten cost pages | combined |
| Duplication — 5-gram index and pairwise overlap against all 156 | combined |
| Focus keyword present, correctly spelled | supplementary |
| Placeholders registered in `reports/placeholders.md` | combined |
| Schema — no `LocalBusiness`, `@id` spine referenced not redeclared, no placeholder in JSON-LD | supplementary |
| Status `draft` + `noindex` | supplementary |

The calculator has no sourced uniqueness threshold: measure it, propose one marked `AWAITING APPROVAL — not enforced`, and flag it if it measures below 50%.

**GATE 31.** Print the derived slug and module outline, the guard demonstration across all four LGAs, the full gate table, the post-import guide-side link edits, and the orphan declaration.

---

## 4.32 — Stage 32: QA specification (build the checklist, do not run it)

`CONTEXT.md` P1 requires logged-out route, visual, responsive, accessibility, link, canonical, robots, sitemap, schema, form, media, security and performance QA before any page is approved for indexing.

**DO:**
1. `reports/32-qa-spec.md` — every check in that list as a discrete numbered item with its pass condition, the evidence constituting a pass, and whether it is automatable or requires human sighting.
2. `scripts/32-qa-automated.py` — the automatable subset only: HTTP status and logged-out route checks, internal link resolution, canonical/robots/sitemap consistency, schema validity, media resolution, heading structure, meta length and uniqueness. Fail-closed, machine-readable output.
3. Specify the human-sighted subset with no automated shortcut: Camden-site visual approval, responsive behaviour, accessibility beyond automated checks, form delivery confirmation, mobile Core Web Vitals on authoritative staging. State plainly that the Stage 11–20 environment-level Lighthouse and browser checks are **not** Camden-site visual or performance approval.
4. Do not run any of it. It executes against authoritative staging after Gate 28 returns GO, and its output feeds the page-by-page release decision.

**GATE 32.** Print the check inventory with the automatable/human-sighted split and the count of checks that must pass before a single page can move to `Index-ready: yes`.

---

# Start

Begin by completing §0 and re-printing **Gate 21**. Then stop for approval. Proceed in stage order thereafter, stopping at every gate.
