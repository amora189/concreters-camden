# Codex Prompt — Clone E&T Melbourne WXR into Camden Concreting

> Paste everything below the line into Codex. Upload alongside it:
> `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml`, `suburbs.json`,
> `camden-site-structure-and-silo.md`, `oran-park-gold-standard.md`.

---

## Task

You are transforming a WordPress WXR export of a Melbourne concreting site into a WXR export for a South West Sydney concreting site. The output is a single importable `.xml` file plus a set of reports. **You are not writing a WordPress plugin and you are not touching a live site — you are transforming an XML file on disk.**

Preserve every design decision: Elementor structure, widget types, widget IDs, CSS classes, global class references, layout, spacing, image positions, section order. Change only text content, headings, metadata, slugs, URLs and image filenames.

**Working directory:** `./camden-clone/`
**Input:** `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml`
**Output:** `camden-concreting-import.xml`

---

## Step 0 — Set up and inspect before changing anything

1. Create `./camden-clone/`, copy the input XML in, and **never modify the original**.
2. Use Python 3 with `lxml` or the stdlib `xml.etree` plus manual CDATA handling. Do not use a regex-only approach for the XML envelope.
3. Write `inventory.md` first, listing every `<item>` with: `post_type`, `post_id`, `post_name`, `status`, `title`, and for pages the count of each `widgetType` found inside `_elementor_data`. Do not proceed until this file exists and you have read it.
4. Report the total attachment count and every distinct image URL.

---

## Step 1 — How to parse and mutate `_elementor_data` (read carefully, this is where it breaks)

`_elementor_data` is stored as **HTML-entity-encoded JSON inside a CDATA block** in a `<wp:meta_value>` element. The round trip is:

```
extract CDATA → html.unescape() → json.loads() → mutate the tree → json.dumps(ensure_ascii=False) → html.escape(quote=False) → wrap in CDATA
```

Getting the escaping wrong produces a file that imports silently and renders blank pages. **Write a round-trip test first**: parse, re-serialise without mutating, and assert the output byte-matches the input. Do not proceed to mutation until that test passes.

### Widget types present in this export and where their text lives

This site mixes Elementor v3 legacy widgets and v4 atomic widgets. Handle both.

| `widgetType` | Text location | Notes |
|---|---|---|
| `heading` | `settings.title` (plain string) | `settings.header_size` holds `h1`/`h2`/`h3` |
| `e-heading` | `settings.title.value.content.value` | **Atomic v4.** Also has `settings.title.value.children[]` — an array of `{id, type, content}` objects mirroring inline tags. If `children` is non-empty you must update the matching `content` field there too, or the heading renders stale. |
| `text-editor` | `settings.editor` (HTML string) | Contains `<a href>` internal links — rewrite those |
| `e-paragraph` | `settings.paragraph.value.content.value` | Same atomic pattern as `e-heading` |
| `image-box` | `settings.title_text`, `settings.description_text`, `settings.image.url`, `settings.link.url` | |
| `icon-box` | `settings.title_text`, `settings.description_text` | |
| `nested-accordion` | `settings.items[].item_title` | Answer bodies are `text-editor` widgets nested in child containers |
| `image` | `settings.image.url`, `settings.image.id`, `settings.image.alt` | `id` must match an attachment `post_id` |
| `button` | `settings.text`, `settings.link.url` | |
| `google_maps` | `settings.address` | Change to a Camden LGA address |

**Do not alter:** `id`, `elType`, `widgetType`, `settings.classes`, `_elementor_used_global_class`, any key starting with `__globals__`, or any style/spacing/typography key. If you cannot confidently identify a key as text content, leave it alone.

---

## Step 2 — Global replacements

Apply across `post_content`, all `_elementor_data`, all Rank Math meta, `<title>`, `<link>`, `guid`, and `wp:post_name`.

| Find | Replace |
|---|---|
| `bestconcretersmelbourne.com.au` | `concreterscamden.com.au` |
| `E&T Co Concreters Melbourne`, `E&T Co` | `[[BRAND_NAME]]` |
| `03 4427 9541` | `[[NSW_PHONE]]` |
| `Melbourne`, `Melbourne's west` | `South West Sydney` (see per-page copy for context-correct phrasing) |
| `Wyndham City Council`, `Wyndham` | `Camden Council` / `Liverpool City Council` — **per suburb**, read `lga` from `suburbs.json` |
| `Werribee`, `Point Cook`, `Tarneit`, `Truganina`, `Hoppers Crossing`, `Werribee South`, `Wyndham Vale` | the corresponding Camden suburb per the page map in Step 3 |
| `Riverwalk`, `Harpley` | the correct estate names from `suburbs.json → local_entities.estates_developers` |
| `Werribee River` | the correct water feature per suburb (`South Creek`, `Upper South Creek`, `Nepean River`) |
| `volcanic plains`, `basalt` | `Wianamatta Shale` |
| `Victoria`, `VIC` | `New South Wales`, `NSW` |

**Emit a final report `residual-melbourne-terms.md` listing any remaining occurrence of any Victorian term anywhere in the output. The build fails if this file is non-empty.**

---

## Step 3 — Page map

Rename, retarget and rewrite according to this table. `suburbs.json` supplies the per-suburb data for every new suburb page.

### Direct transformations (source page → target page)

| Source `post_name` | Target `post_name` | Target primary keyword |
|---|---|---|
| `homepage` | `homepage` | `concreters camden` |
| `contact` | `contact` | — |
| `concrete-driveways-melbourne` | `concrete-driveways-south-west-sydney` | `concrete driveways south west sydney` |
| `exposed-aggregate-melbourne` | `exposed-aggregate-south-west-sydney` | `exposed aggregate sydney` |
| `concrete-slabs-melbourne` | `concrete-slabs-south-west-sydney` | `concrete slabs sydney` |
| `concrete-paths-melbourne` | `concrete-paths-south-west-sydney` | `concrete paths sydney` |
| `concrete-patios-melbourne` | `concrete-patios-south-west-sydney` | `concrete patios sydney` |
| `decorative-concrete-melbourne` | `decorative-concrete-south-west-sydney` | `decorative concrete sydney` |
| `concreter-werribee` | `concreters-oran-park` | `concreters oran park` |
| `concreter-point-cook` | `concreters-leppington` | `concreters leppington` |
| `concreter-tarneit` | `concreters-gregory-hills` | `concreters gregory hills` |
| `concreters-hoppers-crossing` | `concreters-harrington-park` | `concreters harrington park` |
| `concreters-truganina` | `concreters-austral` | `concreters austral` |
| `concrete-driveway-cost-melbourne` | `guides/concrete-driveway-cost-nsw` | `concrete driveway cost nsw` |
| `wyndham-council-vehicle-crossing` | `guides/camden-council-driveway-crossing` | `camden council driveway crossing` |
| `why-does-concrete-crack` | `guides/why-concrete-cracks` | `why does concrete crack` |
| `hello-world`, `privacy-policy`, `__trashed-3` | **DELETE** — remove these `<item>` elements entirely | |

### New pages (duplicate the `concreter-werribee` item, then rewrite)

Create one new page per suburb, cloning the full Werribee `_elementor_data` structure and assigning fresh sequential `post_id` values above the highest existing ID:

`concreters-gledswood-hills`, `concreters-catherine-field`, `concreters-edmondson-park`, `concreters-narellan`, `concreters-mount-annan`, `concreters-spring-farm`, `concreters-elderslie`, `concreters-currans-hill`, `concreters-cobbitty`, `concreters-bringelly`

Also create from scratch: `commercial-concreting-south-west-sydney` (clone the `concrete-slabs-melbourne` structure), `quote`, `about`, plus guide stubs `guides/liverpool-council-vehicle-crossing`, `guides/reactive-clay-slabs-as2870`, `guides/salinity-and-concrete-western-sydney`.

**Do NOT create a `concreters-camden` page.** The homepage owns that query. Creating both causes cannibalisation. This is deliberate — see `camden-site-structure-and-silo.md` §2.

---

## Step 4 — Writing the suburb page copy

Read `oran-park-gold-standard.md` in full before writing any copy. It is the pattern. Every suburb page follows its module structure and its register.

For each suburb, pull from `suburbs.json`:

| Module | Field |
|---|---|
| 1 — Hero H1 + intro | `h1`, `unique_local_variable` |
| 2 — Services grid | `services[]`, ordered by `job_mix_weighting` (highest weight first) |
| 3 — Local build context (~250w) | `local_entities`, `housing_stock_era`, `typical_jobs` |
| 4 — Ground conditions (~200w) | `ground_conditions` |
| 5 — Ground prep (~150w) | `ground_conditions` + `typical_jobs` |
| 6 — Drainage/levels/cracks (~200w) | **Rewrite per suburb** around that suburb's actual water problem |
| 7 — Council crossovers (~150w) | `approval_path` + `geo_facts_shared.camden_driveway_spec` |
| 8 — Local Work Completed | Leave as `[[REAL_PHOTO_PENDING]]` placeholders |
| 9 — Why Customers Choose Us | Shared, suburb name substituted |
| 10 — Areas We Cover | `internal_links_out`, as real anchor links |
| 11 — CTA + FAQ ×3 | `faq_angles` |

### Hard content rules

1. **Module 1's first 80 words must contain a fact that is true of this suburb and false of the other fifteen.** Test it: if the opening paragraph reads correctly when pasted onto a different suburb page, it fails. Rewrite it.
2. **No sentence may appear on more than two suburb pages.** After generating all copy, run a shingle-overlap check (5-gram) across the suburb set and report any pair exceeding 40% similarity in `duplication-report.md`.
3. **Minimum 60% unique body words per suburb page.** Report the actual figure per page.
4. **Never invent data.** No prices you haven't quoted, no jobs you haven't done, no review text, no "we've poured 200 driveways in Oran Park". Where a real number is needed, emit `[[PLACEHOLDER: description of what's needed]]` and list every one in `placeholders.md`.
5. **Council specifications must be cited exactly as they appear in `suburbs.json`.** Do not round 32 MPa to "about 30", do not turn "125mm" into "roughly 125mm", do not change SL72. Where `suburbs.json` marks something VERIFY, write the sentence and append `[[VERIFY]]`.
6. Write in the source site's register: plain, direct, second person, trade-competent, no marketing adjectives, no "nestled in the heart of". Read the Werribee copy in the export and match its voice.
7. Australian English throughout.

---

## Step 5 — Rank Math metadata

For every page set:
- `rank_math_title` — 50–60 chars, primary keyword near the front, reads human. Take from `suburbs.json → title_tag` for suburb pages.
- `rank_math_description` — 140–160 chars. Take from `suburbs.json → meta_description`.
- `rank_math_focus_keyword` — the primary keyword, correctly spelled. (The source has `Concreter Werribe`, a typo. Do not replicate that class of error.)
- `rank_math_breadcrumb_title` — suburb name only.

**Delete every `rank_math_schema_*` meta key.** These are PHP-serialised strings with byte-length prefixes (`s:22:"Concreters in Werribee"`); editing the text without recalculating every length silently corrupts the value and Rank Math will discard it. Schema gets rebuilt after import per §7 of `camden-concreting-seo-spec.md`. Note this in `post-import-tasks.md`.

Assert: no two pages share a `rank_math_title` structure verbatim, and every title/description falls inside its character range. Report violations.

---

## Step 6 — Images and attachments

1. Rewrite every `<wp:attachment_url>`, `guid`, `_wp_attached_file` and in-Elementor `settings.image.url` to the new domain.
2. Rename every file to a descriptive Camden-relevant slug and update all references consistently. Examples: `TARNEIT-SOIL.jpg` → `wianamatta-shale-clay-camden.jpg`; `crossovers.jpg` → `camden-council-driveway-crossing.jpg`; `melbournes-west.png` → `south-west-sydney-growth-corridor.png`. Emit `image-rename-map.csv` mapping old filename → new filename → pages referencing it, so the uploads folder can be renamed to match.
3. Rewrite every `settings.image.alt` and attachment `_wp_attachment_image_alt` to describe the image in its Camden context. Alt text describes the photo; it does not repeat the keyword.
4. Preserve every `settings.image.id` ↔ attachment `post_id` pairing exactly. Broken IDs mean broken images.
5. Emit `reencode-images.sh` — a shell script that strips EXIF, resizes to 98% and re-saves at quality 82, so file hashes differ from the Melbourne originals. This is a footprint requirement, not an optimisation.

---

## Step 7 — Internal links

Rewrite every `href` in `text-editor` HTML and every `settings.link.url` to the new URL map. Then enforce the link rules from `camden-site-structure-and-silo.md` §4:

- Suburb page → its top 3–5 services, anchor `{service} in {suburb}`
- Suburb page → 4 neighbours from `internal_links_out`, anchor = suburb name only
- Suburb page → 1–2 relevant guides, descriptive anchor
- Service page → 4–6 suburbs where it weights highest
- No suburb→suburb full mesh

Emit `internal-link-graph.csv` (from_url, to_url, anchor_text, module) and assert every target URL exists in the output. Report orphans — any page with zero inbound internal links.

---

## Step 8 — Menus

Update the five nav menus. `footer-areas` and the `Areas` dropdown under `primary` list the 6 Tier 1 suburbs only, not all 16 — a 16-item dropdown is a usability problem and dilutes the link equity. `footer-services` lists all 7 services. `footer-blogs` lists the 6 guides. Preserve `_menu_item_menu_item_parent` relationships.

Note in `post-import-tasks.md` that menu location assignment lives in `theme_mods` and must be reassigned manually after import.

---

## Step 9 — Validation gates (all must pass)

1. Output XML is well-formed; every `_elementor_data` value parses as valid JSON after unescaping.
2. Round-trip test passes on every page.
3. Exactly one `h1` per page. **The source `concrete-driveway-cost-melbourne` has two — fix it, don't replicate it.**
4. Zero occurrences of any term in the Victorian blocklist (Melbourne, Werribee, Wyndham, Point Cook, Tarneit, Truganina, Hoppers Crossing, Riverwalk, Harpley, Victoria, VIC, the old phone number, the old domain).
5. Every `settings.image.id` resolves to an attachment item in the same file.
6. Every internal link target exists.
7. No `rank_math_schema_*` keys remain.
8. Duplication check passes: no sentence on >2 suburb pages, no page pair >40% 5-gram overlap.
9. Every `[[PLACEHOLDER]]` is listed in `placeholders.md`.
10. `residual-melbourne-terms.md` is empty.

---

## Deliverables

```
camden-clone/
├── camden-concreting-import.xml     ← the importable file
├── inventory.md                     ← Step 0 audit
├── placeholders.md                  ← every [[PLACEHOLDER]] and what's needed
├── duplication-report.md            ← per-page uniqueness %, overlapping pairs
├── internal-link-graph.csv
├── image-rename-map.csv
├── reencode-images.sh
├── residual-melbourne-terms.md      ← must be empty
├── post-import-tasks.md             ← Astra settings, menu locations, schema, cache purge
└── validation-report.md             ← all 10 gates, pass/fail
```

---

## Constraints

- Do not deploy anything. Do not touch a live WordPress site. Output files only.
- Do not restructure Elementor layouts, change widget types, or "improve" the design.
- Do not invent facts, prices, reviews, job counts or completion figures.
- If a source page is ambiguous or a transformation is unclear, stop and ask rather than guessing.
- Work incrementally: get the round-trip test passing, then transform one suburb page end to end, show it for review, and only then batch the rest.
