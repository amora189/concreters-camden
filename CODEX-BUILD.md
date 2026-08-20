# CODEX BUILD — Camden Concreting Site

**Paste this entire file into Codex as the first and only instruction. Upload the six input files listed in §1 alongside it.**

You are building a WordPress site by transforming an existing WXR export. You work in stages. **Each stage ends with a STOP GATE. You do not begin the next stage until the gate passes and you have printed the gate report.** If a gate fails, fix it and re-run the gate. If you cannot fix it, stop and ask — do not proceed with a known failure.

Do not deploy anything. Do not touch a live site. You produce files on disk.

---

## 1. Input files

| File | What it governs |
|---|---|
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | The source WXR being transformed. Never modify it. |
| `camden-site-structure-and-silo.md` | **Architecture authority** — URLs, slugs, silo, internal link rules, clone procedure, footprint rules |
| `suburbs.json` | **Data authority** — per-suburb facts, keywords, titles, meta, entities, FAQ angles |
| `oran-park-gold-standard.md` | **Copy authority** — module structure, register, tone, uniqueness bar |
| `camden-concreting-seo-spec.md` | **Schema authority** — §7 JSON-LD plan. Also anti-doorway rules (§5) and integrity rules. |
| `codex-clone-prompt.md` | **Technical authority** — how to parse and mutate `_elementor_data`, widget-by-widget field map, validation gates |

### Precedence when files conflict

Read this table before reading the files. These conflicts are real and you will hit them.

| Conflict | Resolution |
|---|---|
| `camden-concreting-seo-spec.md` §8 recommends Astro; everything else assumes WordPress | **WordPress wins.** That section is superseded. The seo-spec is used ONLY for §5 (module/anti-doorway rules), §7 (schema) and §10. Ignore its §2 URL map and §8 stack. |
| seo-spec uses `/services/{slug}/`; structure doc uses `/{service}-south-west-sydney/` | **Structure doc wins.** |
| `suburbs.json` lists 11 services; structure doc specifies 7 service pages | **7 pages.** Fold per the mapping in §3 below. |
| `suburbs.json` has a `camden` suburb at `/concreters-camden-town/` | **Do not build it.** The homepage owns `concreters camden`. Skip this entry entirely. 15 suburb pages, not 16. |
| `suburbs.json` puts `elderslie` at tier 3; structure doc puts it at tier 2 | **Tier 2.** Elderslie absorbs the Camden-township material. |

Where a file gives a specific number (32 MPa, 125mm, SL72, 800mm, 4%, 1:6), reproduce it exactly. Never round, soften or paraphrase a specification.

---

## 2. Working directory and outputs

```
./camden-clone/
├── source/                          copy of the original XML, read-only
├── build/                           intermediate JSON per page
├── reports/                         every gate report
└── camden-concreting-import.xml     final deliverable
```

---

## 3. Service page mapping (resolves the 11 → 7 conflict)

| Built page (slug) | Absorbs these `suburbs.json` service concepts |
|---|---|
| `concrete-driveways-south-west-sydney` | concrete-driveways, driveway-crossovers, concrete-removal-and-replacement |
| `concrete-slabs-south-west-sydney` | house-slabs, shed-and-garage-slabs |
| `exposed-aggregate-south-west-sydney` | exposed-aggregate |
| `decorative-concrete-south-west-sydney` | stencilled-and-stamped-concrete, coloured-concrete |
| `concrete-patios-south-west-sydney` | alfresco-and-patio-slabs |
| `concrete-paths-south-west-sydney` | concrete-paths-and-footpaths |
| `commercial-concreting-south-west-sydney` | commercial-concreting |

Absorbed concepts become H2 sections within the parent page, not separate pages.

---

# STAGE 0 — Read and reconcile

**READ, in this order:** `camden-site-structure-and-silo.md` in full → `codex-clone-prompt.md` §1 and §9 → `oran-park-gold-standard.md` in full → `suburbs.json` → `camden-concreting-seo-spec.md` §5 and §7 only.

**DO:**
1. Create the working directory. Copy the source XML into `source/` and set it read-only.
2. Parse the XML. Write `reports/00-inventory.md` listing every `<item>`: `post_type`, `post_id`, `post_name`, `status`, `title`, and for pages a count of each `widgetType` inside `_elementor_data`.
3. Write `reports/00-reconciliation.md`: the final page list you intend to build — every URL, page type, primary keyword, source template, and publish status — derived from the precedence table above.

**STOP GATE 0.** Print `reports/00-reconciliation.md`. It must show exactly:
- 1 homepage, 3 utility pages (`contact`, `quote`, `about`)
- 7 service pages
- 15 suburb pages (6 Tier 1 → `publish`; 9 Tier 2/3 → `draft`)
- 6 guide pages under `/guides/`
- **No** `concreters-camden` or `concreters-camden-town`
- Deletions: `hello-world`, `privacy-policy`, `__trashed-3`

**Wait for my approval before Stage 1.**

---

# STAGE 1 — Round-trip harness

The single highest-risk operation in this build is parsing and re-serialising `_elementor_data`. It is HTML-entity-encoded JSON inside CDATA. Wrong escaping produces a file that imports without error and renders blank pages.

**DO:**
1. Build `lib/wxr.py` with: `load_xml`, `get_meta(item, key)`, `set_meta(item, key, value)`, `parse_elementor(item)`, `write_elementor(item, tree)`, `save_xml`.
   Round trip: `CDATA → html.unescape() → json.loads() → mutate → json.dumps(ensure_ascii=False) → html.escape(quote=False) → CDATA`.
2. Build `lib/walk.py` implementing the widget field map from `codex-clone-prompt.md` §1 — `heading`, `e-heading` (**including the mirrored `settings.title.value.children[]` array**), `text-editor`, `e-paragraph`, `image-box`, `icon-box`, `nested-accordion`, `image`, `button`, `google_maps`.
3. Write `tests/test_roundtrip.py`: for every page item, parse and re-serialise **without mutating**, and assert the output byte-matches the input.

**STOP GATE 1.** Run the test. Print pass/fail per page to `reports/01-roundtrip.md`. **Every page must byte-match.** Do not proceed on a partial pass.

---

# STAGE 2 — URL map and ID allocation

**DO:**
1. Write `build/url-map.json`: old slug → new slug for every transformed page, plus every new page. Use the page map in `codex-clone-prompt.md` §3, corrected by Stage 0 reconciliation.
2. Allocate `post_id` values for new pages sequentially above the highest existing ID. Record in `build/id-map.json`.
3. Write `build/global-replace.json`: the find/replace table from `codex-clone-prompt.md` §2.

**STOP GATE 2.** Assert every new `post_id` is unique and unused; every URL in the map is unique; every slug is lowercase, hyphenated, no trailing slash in `post_name`. Print `reports/02-urlmap.md`.

---

# STAGE 3 — Pilot page (Oran Park)

Transform exactly one page end to end. This is the pattern check.

**DO:** Take the `concreter-werribee` item. Transform it into `concreters-oran-park` following `oran-park-gold-standard.md` module by module — all 11 modules, using its exact copy where the gold standard supplies it, and its register where it doesn't.

Preserve: every `id`, `elType`, `widgetType`, `settings.classes`, `_elementor_used_global_class`, every `__globals__` key, every style/spacing/typography key.
Change: text content, headings, image URLs and alt, link hrefs, Rank Math meta, slug, `<link>`, `guid`.
Delete: `_elementor_element_cache`, `rank_math_schema_*`.

**STOP GATE 3.** Print to `reports/03-pilot.md`:
- The full rendered text of the page, module by module, in reading order
- Widget count before vs after (must be identical)
- Diff of every changed JSON key path
- Confirmation that no style key changed
- Uniqueness note: does module 1's opening 80 words contain a fact false of the other 14 suburbs?

**Wait for my approval before Stage 4.** This is the most important gate in the build — if the pilot is wrong, everything after it is wrong fifteen times over.

---

# STAGE 4 — Remaining Tier 1 suburbs

**DO:** Clone the Werribee structure five more times: Leppington, Gregory Hills, Gledswood Hills, Austral, Harrington Park. Write copy per `suburbs.json` and the gold standard.

Apply the content rules from `codex-clone-prompt.md` §4:
- Module 1's first 80 words must contain a fact true of that suburb and false of the others
- Module 6 rewritten per suburb around that suburb's actual water problem (Leppington = Upper South Creek flood planning level; Gledswood Hills = salinity in the riparian corridor; Harrington Park = 25-year-old slab edge failure; Austral = undocumented market-garden fill; Gregory Hills = commercial subgrade)
- Module 8 stays `[[REAL_PHOTO_PENDING]]`
- No invented prices, jobs, review text or volume claims — emit `[[PLACEHOLDER: what's needed]]`
- Council specs reproduced exactly

Status: `publish`. Any page whose module 8 is still placeholder gets `<meta name="robots" content="noindex,follow">` — implement via a `_rank_math_robots` meta or a documented post-import task, and list it in `reports/post-import-tasks.md`.

**STOP GATE 4.** Run the duplication check: 5-gram shingle overlap across all 6 Tier 1 pages. Write `reports/04-duplication.md` with per-page unique-body-word percentage and every page pair's overlap. **Gate: no sentence appears on more than 2 pages; no pair exceeds 40% overlap; every page ≥60% unique body words.** Print the table.

---

# STAGE 5 — Homepage, utility pages, service pages

**DO:**
1. **Homepage** from `homepage`. Primary keyword `concreters camden`, secondary `concreters south west sydney`. Its local-context module carries the LGA-wide framing plus the Camden township material (heritage conservation area on Argyle/John/Murray/Oxley, Nepean flood planning) — this is why no separate Camden suburb page exists. Links to all 7 services and all 6 Tier 1 suburbs.
2. **`contact`** transformed; **`quote`** and **`about`** created from the contact structure.
3. **7 service pages** from `concrete-driveways-melbourne` (and `concrete-slabs-melbourne` for commercial). Substitute geography: Melbourne's west reactive clay → Wianamatta Shale clay; Wyndham crossover rules → Camden's 32 MPa / 125mm / SL72 / 4.0–5.5m spec; 350–520m² estate lots → Camden's 350–450m² growth-corridor lots. Fold absorbed concepts in as H2 sections per §3.

**STOP GATE 5.** Assert exactly one `h1` per page across all pages built so far. Print `reports/05-headings.md` listing every page's full heading outline (H1/H2/H3 in document order). Confirm no page has zero or two H1s.

---

# STAGE 6 — Guides

**DO:** Build 6 pages under `/guides/`:

| Slug | Source template | Primary keyword |
|---|---|---|
| `guides/concrete-driveway-cost-nsw` | `concrete-driveway-cost-melbourne` | concrete driveway cost nsw |
| `guides/camden-council-driveway-crossing` | `wyndham-council-vehicle-crossing` | camden council driveway crossing |
| `guides/why-concrete-cracks` | `why-does-concrete-crack` | why does concrete crack |
| `guides/liverpool-council-vehicle-crossing` | clone of the Camden guide | liverpool council vehicle crossing |
| `guides/reactive-clay-slabs-as2870` | clone of why-concrete-cracks | reactive clay concrete slab as2870 |
| `guides/salinity-and-concrete-western-sydney` | clone of why-concrete-cracks | salinity concrete western sydney |

**Fix the source bug:** `concrete-driveway-cost-melbourne` has two H1s — "Concrete Driveway Cost Per m²..." and "CONCRETE DRIVEWAY COST PER m² BY FINISH". The second becomes an H2.

Cost guide: **no invented prices.** Structure the page and emit `[[PLACEHOLDER: real per-m² range for {finish} in South West Sydney]]` for each finish. Costs must come from Shaun's own quotes.

**STOP GATE 6.** Re-run the heading assertion across all pages. Confirm the double-H1 is fixed. Print `reports/06-guides.md`.

---

# STAGE 7 — Tier 2 and Tier 3 suburbs

**DO:** Build the remaining 9 suburb pages: Catherine Field, Edmondson Park, Narellan, Mount Annan, Spring Farm, Elderslie (Tier 2); Currans Hill, Cobbitty, Bringelly (Tier 3).

**Status: `draft`, not `publish`.** These sit in the import file ready to publish once real photos and real quoted prices exist. Publishing 15 suburb pages simultaneously with placeholder content in modules 6 and 7 is exactly the scaled-content pattern described in `camden-concreting-seo-spec.md` §1.

Same content rules as Stage 4.

**STOP GATE 7.** Re-run the full duplication check across all 15 suburb pages. Same thresholds. Print `reports/07-duplication-full.md`. If any pair exceeds 40%, rewrite the weaker page before proceeding.

---

# STAGE 8 — Links, menus, images

**DO:**
1. **Internal links.** Enforce rules A–G from `camden-site-structure-and-silo.md` §4. Rewrite every `href` in `text-editor` HTML and every `settings.link.url`. Emit `reports/08-link-graph.csv` (from_url, to_url, anchor_text, module).
2. **Menus.** `primary` → Services dropdown (7), Areas dropdown (**Tier 1 only, 6 items**), Blog dropdown (6 guides), Contact. `footer-areas` → 6 Tier 1. `footer-services` → 7. `footer-blogs` → 6 guides. Preserve `_menu_item_menu_item_parent` relationships.
3. **Images.** Rewrite every `wp:attachment_url`, `guid`, `_wp_attached_file` and `settings.image.url` to the new domain. Rename every file to a descriptive Camden slug and update all references. Rewrite every alt. Preserve every `settings.image.id` ↔ attachment `post_id` pairing. Emit `reports/08-image-rename-map.csv` and `reencode-images.sh` (strip EXIF, resize 98%, quality 82 — footprint requirement, not optimisation).

**STOP GATE 8.** Assert: every internal link target exists in the output; zero orphan pages (every page has ≥1 inbound internal link); every `settings.image.id` resolves to an attachment item in the same file; no suburb→suburb full mesh. Print `reports/08-links.md`.

---

# STAGE 9 — Final validation and assembly

**DO:** Write `camden-concreting-import.xml`. Then run all ten gates from `codex-clone-prompt.md` §9 plus these:

| # | Gate | Pass condition |
|---|---|---|
| 1 | XML well-formed | parses clean |
| 2 | Elementor JSON | every `_elementor_data` unescapes to valid JSON |
| 3 | Round trip | every page passes |
| 4 | H1 | exactly one per page |
| 5 | Victorian blocklist | zero occurrences of: Melbourne, Werribee, Wyndham, Point Cook, Tarneit, Truganina, Hoppers Crossing, Riverwalk, Harpley, Victoria, VIC, `03 4427 9541`, `bestconcretersmelbourne.com.au` |
| 6 | Image IDs | all resolve |
| 7 | Links | all resolve, no orphans |
| 8 | Schema meta | zero `rank_math_schema_*` keys remain |
| 9 | Cache | zero `_elementor_element_cache` keys remain |
| 10 | Duplication | no sentence on >2 pages, no pair >40%, every page ≥60% unique |
| 11 | Meta lengths | every `rank_math_title` 50–60 chars, every `rank_math_description` 140–160 chars |
| 12 | Meta uniqueness | no two titles structurally identical |
| 13 | Placeholders | every `[[PLACEHOLDER]]` / `[[VERIFY]]` / `[[REAL_PHOTO_PENDING]]` listed in `reports/placeholders.md` |
| 14 | Focus keywords | every page has one, spelled correctly (source has a typo: `Concreter Werribe` — do not replicate that class of error) |
| 15 | Status | 6 Tier 1 suburbs + home + utility + services + guides = `publish`; 9 Tier 2/3 suburbs = `draft` |

**STOP GATE 9.** Print `reports/09-validation.md` — all 15 gates, pass/fail, with the failing items enumerated. **Gate 5 and gate 10 are hard failures — do not deliver on either.**

---

# STAGE 10 — Handover pack

**DO:** Write `reports/post-import-tasks.md` covering, in order:

1. Fresh WP install; Astra + Elementor **4.2.x** + Rank Math installed *before* import (v4 atomic `e-heading` widgets break on a v3 Elementor).
2. **Import Astra Customizer settings separately** via Astra Options Import/Export — these live in `theme_mods`, are NOT in the WXR, and without them the site imports content-correct and style-wrong.
3. Move `/wp-content/uploads/` manually preserving the `2026/07/` structure, after running `reencode-images.sh` and applying `08-image-rename-map.csv`.
4. Import `camden-concreting-import.xml`.
5. `wp search-replace 'bestconcretersmelbourne.com.au' 'concreterscamden.com.au' --all-tables` (dry-run first) — the importer does not reliably remap `_elementor_data` in `wp_postmeta`.
6. `DELETE FROM wp_postmeta WHERE meta_key = '_elementor_element_cache';`
7. Elementor → Tools → Regenerate CSS & Data, then Sync Library.
8. Appearance → Menus → Manage Locations (assignments are not in the WXR).
9. Rebuild Rank Math schema per `camden-concreting-seo-spec.md` §7 — one `@graph` per page, `LocalBusiness` on `/` and `/contact/` ONLY, suburb pages get `Service` + `areaServed` referencing the `#localbusiness` `@id`. Never a `LocalBusiness` node per suburb.
10. Permalinks `/%postname%/`, flush, verify trailing slashes and canonicals match.
11. Fill `reports/placeholders.md`, then publish the Tier 2/3 drafts.
12. Verify Core Web Vitals on mobile before submitting the sitemap.

**FINAL OUTPUT.** Print a summary: pages built by type and status, total placeholders outstanding grouped by what's needed, and the three things that must happen before anything is indexed.

---

## Standing constraints

- Never invent a price, a completed job, a review, a licence number, an ABN or a volume claim. Emit a placeholder.
- Never round or paraphrase a council specification.
- Never restructure an Elementor layout, change a widget type, or "improve" the design.
- Never proceed past a failed gate.
- Australian English throughout.
- If a transformation is ambiguous, stop and ask rather than guessing.
