# Camden Concreting — Site Structure, Silo & Clone Guide

**Source site:** `bestconcretersmelbourne.com.au` (E&T Co Concreters Melbourne) — your own site, WXR export dated 2026-08-14
**Target site:** `concreterscamden.com.au`
**Stack being cloned:** Astra theme + Elementor 4.2.0 + Rank Math, WordPress 7.0.4
**Companion files:** `suburbs.json` (page data), `codex-clone-prompt.md` (the Codex instruction), `oran-park-gold-standard.md` (the copy pattern)

---

## 1. What the export actually contains — and what it doesn't

| Contained in the WXR | Status |
|---|---|
| 18 pages (17 published, 1 draft) | ✅ Imports cleanly |
| 83 media attachments | ⚠️ Imports only if source site stays live during import, or you copy `/wp-content/uploads/` manually |
| 8 Elementor templates incl. `default-kit` | ✅ Global colours, fonts and Elementor kit come across |
| 4 nav menus (primary, primary-2, footer-areas, footer-services, footer-blogs) | ⚠️ Menu *items* import; menu *location assignment* does not |
| Rank Math title/description/focus keyword/breadcrumb | ✅ Plain postmeta, imports fine |
| Rank Math schema (`rank_math_schema_Service`, `_Article`) | ⚠️ PHP-serialised — corrupts if edited without recalculating byte lengths |
| 1 `custom_css` post | ✅ |

**Not in the export — you must move these separately:**
- **Astra Customizer settings** (header/footer builder layout, theme colours, typography, button styles, container widths). These live in `theme_mods_astra` in `wp_options`, which WXR does not touch. Export them from the source site with Astra's own **Astra Options Import/Export**, or use a Customizer Export/Import plugin. **Skip this and the site will import with correct content and completely wrong styling.**
- Plugin settings (Rank Math general config, LiteSpeed cache config, contact form config).
- The uploads directory itself, if you're not letting the importer download from the live source.

---

## 2. Two architectural fixes to make during the clone

The E&T structure works, but it carries two flaws. Don't clone them.

**Fix 1 — Standardise the suburb slugs.** E&T uses `concreter-werribee`, `concreter-point-cook`, `concreter-tarneit`, but `concreters-hoppers-crossing`, `concreters-truganina`. Inconsistent slugs make internal linking error-prone and look unmaintained. Camden uses **`/concreters-{suburb}/`** everywhere, no exceptions.

**Fix 2 — Kill the homepage-vs-suburb cannibalisation before it starts.** On E&T this never came up: the homepage targets "Concreters Melbourne" and there is no Melbourne suburb page. Camden is different — "Camden" is simultaneously the brand anchor, the LGA name **and** a suburb. If you build a homepage targeting `concreters camden` *and* a `/concreters-camden/` page, they will fight each other for the same query, and Google will pick the wrong one. This is the same failure mode as the engineered-timber cannibalisation on Alpha Flooring.

**The resolution:**

| Page | Primary query | Notes |
|---|---|---|
| `/` (homepage) | `concreters camden` | Also carries `concreters south west sydney` as secondary. Owns the LGA-level term outright. |
| `/concreters-elderslie/` | `concreters elderslie` | Absorbs the Camden-township material: heritage conservation area, Nepean flood levels, pre-1980 housing stock. |
| ~~`/concreters-camden/`~~ | — | **Do not build in v1.** Add only if Search Console later shows the homepage under-serving township-specific queries. |

Service page slugs use `-south-west-sydney`, not `-camden`, for the same reason — they'd otherwise compete with the homepage on the geo modifier while ranking for nothing wider.

---

## 3. Silo structure

```
/                                                    HOME — "concreters camden"
│
├── SILO 1: SERVICES (commercial)
│   ├── /concrete-driveways-south-west-sydney/
│   ├── /exposed-aggregate-south-west-sydney/
│   ├── /concrete-slabs-south-west-sydney/
│   ├── /concrete-paths-south-west-sydney/
│   ├── /concrete-patios-south-west-sydney/
│   ├── /decorative-concrete-south-west-sydney/
│   └── /commercial-concreting-south-west-sydney/     ← NEW, no E&T equivalent
│
├── SILO 2: AREAS (local commercial)
│   ├── TIER 1  /concreters-oran-park/
│   │           /concreters-leppington/
│   │           /concreters-gregory-hills/
│   │           /concreters-gledswood-hills/
│   │           /concreters-austral/
│   │           /concreters-harrington-park/
│   ├── TIER 2  /concreters-catherine-field/
│   │           /concreters-edmondson-park/
│   │           /concreters-narellan/
│   │           /concreters-mount-annan/
│   │           /concreters-spring-farm/
│   │           /concreters-elderslie/
│   └── TIER 3  /concreters-currans-hill/
│               /concreters-cobbitty/
│               /concreters-bringelly/
│
├── SILO 3: GUIDES (informational)
│   ├── /guides/concrete-driveway-cost-nsw/
│   ├── /guides/camden-council-driveway-crossing/
│   ├── /guides/liverpool-council-vehicle-crossing/
│   ├── /guides/why-concrete-cracks/
│   ├── /guides/reactive-clay-slabs-as2870/
│   └── /guides/salinity-and-concrete-western-sydney/
│
└── UTILITY  /about/  /contact/  /quote/  /gallery/
```

**Note the guides move under `/guides/`.** E&T has them at root (`/concrete-driveway-cost-melbourne/`, `/wyndham-council-vehicle-crossing/`). Root-level informational pages sitting alongside commercial pages is exactly the flat structure that got restructured on Alpha Flooring. Do it right the first time here.

The commercial service page for `/commercial-concreting-south-west-sydney/` has no E&T equivalent because Melbourne's west didn't need it. Camden does — Gregory Hills sits next to Smeaton Grange, Narellan anchors the retail spine, and Bringelly is 78% commercial off the back of the Aerotropolis.

---

## 4. Internal linking rules (directional — enforce these)

| Rule | From | To | Anchor |
|---|---|---|---|
| **A** | Home | all 7 service pages | service name only |
| **B** | Home | 6 Tier 1 suburb pages | suburb name only |
| **C** | Suburb page | its top 3–5 services (by `job_mix_weighting`) | `{service} in {suburb}` |
| **D** | Suburb page | 4 named neighbours (`internal_links_out`) | suburb name only |
| **E** | Suburb page | 1–2 relevant guides | descriptive, non-exact-match |
| **F** | Service page | 4–6 suburbs where that service weights highest | `{service} {suburb}` |
| **G** | Guide | 1–2 service pages + home | descriptive |

**Never:** suburb → suburb full mesh (16×15 = 240 links screams generated); guide → guide chains beyond one "next read"; service → service laterally except within the driveways ↔ exposed aggregate ↔ decorative trio.

---

## 5. Template anatomy — what gets cloned, module by module

### 5.1 Suburb page (source: `concreter-werribee`, ~1,400 words)

| # | Module | Widget types | Unique per suburb? | Data source |
|---|---|---|---|---|
| 1 | Hero: H1 + intro + 2 CTA buttons | `heading` (h1), `text-editor`, `button` ×2 | ✅ | `h1`, `unique_local_variable` |
| 2 | Our Services grid | `e-heading`, `text-editor`, `image-box` ×6 | ⬜ Shared | `services[]` reordered by `job_mix_weighting` |
| 3 | Local build context | `e-heading`, `text-editor` (~250w) | ✅ | `local_entities`, `housing_stock_era` |
| 4 | Ground conditions | `e-heading`, `text-editor` (~200w), `image` ×2 | ✅ | `ground_conditions` |
| 5 | How we prepare the ground | `e-heading`, `text-editor` (~150w) | ✅ | `ground_conditions` + `typical_jobs` |
| 6 | Drainage, levels, crack control | `e-heading`, `text-editor` (~200w), `image` ×2 | ⬜ Semi-shared | Reword per suburb; do not copy verbatim |
| 7 | Council crossovers | `e-heading`, `text-editor` (~150w) | ✅ | `approval_path`, `camden_driveway_spec` |
| 8 | Local Work Completed | `e-heading`, `image` ×3 + captions | ✅ | **Real photos only** |
| 9 | Why Customers Choose Us | `heading` (h2), `icon-box` ×4, `google_maps` | ⬜ Shared | Site config |
| 10 | Areas We Cover Around {Suburb} | `heading` (h2), `text-editor` | ✅ | `internal_links_out` |
| 11 | CTA + FAQ | `e-heading`, `button`, `nested-accordion` ×3 | ✅ | `faq_angles` |

**Distinctness budget: modules 1, 3, 4, 5, 7, 8, 10, 11 must be genuinely unique. That's 8 of 11 — higher than E&T achieves and higher than the 60% minimum, because 16 suburb pages is more than 5 and the doorway risk scales with count.**

**Module 6 warning.** On E&T, "Drainage, levels and crack control" is near-identical across suburb pages. With 5 pages that's survivable. With 16 it's a visible template. Rewrite it per suburb around that suburb's actual water problem — Spring Farm is slope and water tracking behind a slab, Leppington is Upper South Creek flood planning levels, Gledswood Hills is salinity in the riparian corridor, Mount Annan is edge failure on 30-year-old slabs.

**Module 8 gate.** No real photos yet in Camden means module 8 has nothing honest to put in it. Any suburb page whose module 8 is empty ships with `<meta name="robots" content="noindex,follow">` until you have real job photos. This is not optional caution — a "Local Work Completed" gallery showing Melbourne jobs on a Sydney page is a false claim, and it's the same category of problem as the GBP setup.

### 5.2 Service page (source: `concrete-driveways-melbourne`, ~2,000 words)

H1 → intro + CTA → finish types (4 image + heading + description blocks) → "Why driveways crack here" H2 + 3 images → "Thickness, reinforcement and what goes under" H2 → "How we build a driveway that lasts" H2 → "Drainage, falls and finished levels" H2 → "Replacing an old driveway" H2 → "How big is a typical driveway?" H2 → "Concrete, pavers or asphalt?" H2 → "Sealing and looking after it" H2 → "Areas we service" H2 + map + suburb links → cost H3 + link to cost guide.

This template is strong and needs mostly geographic substitution: Melbourne's west reactive clay → Wianamatta Shale clay; Wyndham crossover rules → Camden's 32 MPa / 125mm / SL72 spec; 350–520m² estate lots → Camden's 350–450m² growth-corridor lots.

### 5.3 Guide page (source: `concrete-driveway-cost-melbourne`)

⚠️ **Bug in the source:** this page has **two H1s** — "Concrete Driveway Cost Per m² in Melbourne (2026 Guide)" and "CONCRETE DRIVEWAY COST PER m² BY FINISH". Fix on clone: the second becomes an H2. Codex must assert one H1 per page across the whole build.

---

## 6. The clone procedure (order matters)

1. **Fresh WordPress install** on the new domain. Same PHP/WP version if possible.
2. **Install Astra + Elementor + Rank Math** *before* importing. Match the Elementor major version (4.2.x) — importing v4 atomic widgets into a v3 install will break `e-heading` elements.
3. **Move the media first, not last.** Either (a) FTP/download `/wp-content/uploads/` from the source and upload to the new host preserving the `2026/07/` folder structure, then run Media Library regeneration; or (b) leave attachment URLs pointing at the live source and let the importer download them. Option (a) is more reliable and doesn't depend on E&T staying online.
4. **Import Astra Customizer settings** via Astra Options Import/Export. Without this the site imports content-correct and style-wrong.
5. **Import the rewritten WXR** (the file Codex produces). Tick "Download and import file attachments" only if you chose option (b).
6. **Search-replace the domain in postmeta.** WordPress's importer remaps URLs in `post_content` but does **not** reliably remap `_elementor_data`, which lives in `wp_postmeta`. Run Better Search Replace or `wp search-replace 'bestconcretersmelbourne.com.au' 'concreterscamden.com.au' --all-tables`. Dry-run first.
7. **Delete every `_elementor_element_cache` postmeta row.** This holds pre-rendered HTML of the *Melbourne* content. Leave it and your Camden pages will render Werribee copy until the cache expires. `DELETE FROM wp_postmeta WHERE meta_key = '_elementor_element_cache';`
8. **Elementor → Tools → Regenerate CSS & Data**, then **Sync Library**.
9. **Assign menus to locations** (Appearance → Menus → Manage Locations). Menu items import; the assignment doesn't.
10. **Re-enter Rank Math schema by hand** on each page. The `rank_math_schema_*` values are PHP-serialised with byte-length prefixes (`s:22:"Concreters in Werribee"`). Editing the string without recalculating every length silently corrupts the whole meta value. Safer to strip these on export and rebuild them in the Rank Math UI, which takes about ten minutes for 25 pages.
11. **Set permalinks** to `/%postname%/`, flush, verify trailing slashes and canonicals match.
12. **Re-encode every image** (see §7), then submit the sitemap.

---

## 7. Cross-domain footprint — read this before you import

Alpha Flooring and Woodland Flooring already share byte-identical image hashes and duplicated copy, and that was flagged as a real footprint risk. Cloning E&T into Camden creates the same problem at a larger scale: 83 identical files, identical Elementor structure, identical CSS classes, identical section order.

Different states and different verticals-within-a-vertical make this lower risk than two Melbourne flooring sites, but "lower" is not "none", and both domains are yours.

**Mitigations, in priority order:**

1. **Re-encode every image so the hashes differ.** Strip EXIF, change dimensions by a few percent, re-save at a different quality. A one-line ImageMagick pass over the uploads folder does it:
   `mogrify -resize 98% -strip -quality 82 -path ./out ./uploads/2026/07/*.jpg`
2. **Rename every file to a Camden-relevant, descriptive filename.** `TARNEIT-SOIL.jpg` → `wianamatta-shale-clay-camden.jpg`. `crossovers.jpg` → `camden-council-driveway-crossing.jpg`. Update the references in `_elementor_data` and the attachment posts.
3. **Rewrite alt text** to describe the image in its new context, not to repeat the keyword.
4. **Vary the module order** between the two sites. Move "Why Customers Choose Us" above "Local Work Completed" on Camden. Small structural divergence, meaningful footprint reduction.
5. **Change the colour palette** in the Elementor kit. Two sites with identical hex values and identical section order are trivially clusterable.
6. **Different hosting IP** from E&T if practical.
7. **Never** reuse the same testimonial text, the same "Client Testimonials" names, or the same phone number.

Items 1–3 are mandatory. Items 4–6 are strongly recommended and cheap.

---

## 8. Page inventory to build

| # | URL | Type | Primary keyword | Source template | Phase |
|---|---|---|---|---|---|
| 1 | `/` | Home | concreters camden | `homepage` | 1 |
| 2 | `/contact/` | Utility | — | `contact` | 1 |
| 3 | `/quote/` | Utility | — | new | 1 |
| 4 | `/about/` | Utility | — | new | 1 |
| 5–11 | 7 service pages | Service | `{service} south west sydney` | `concrete-driveways-melbourne` | 3 |
| 12–17 | 6 Tier 1 suburbs | Suburb | `concreters {suburb}` | `concreter-werribee` | 2 |
| 18–23 | 6 Tier 2 suburbs | Suburb | `concreters {suburb}` | `concreter-werribee` | 4 |
| 24–26 | 3 Tier 3 suburbs | Suburb | `concreters {suburb}` | `concreter-werribee` | 6 |
| 27–32 | 6 guides | Guide | see silo map | `concrete-driveway-cost-melbourne`, `why-does-concrete-crack`, `wyndham-council-vehicle-crossing` | 5 |

Phases 4 and 6 are gated on Search Console impressions from the prior phase, not on the calendar.

---

## 9. Verification checklist before submitting the sitemap

- [ ] Exactly one H1 per page (the source cost guide has two — fix it)
- [ ] No occurrence of "Melbourne", "Werribee", "Wyndham", "Point Cook", "Tarneit", "Truganina", "Hoppers Crossing", "Riverwalk", "Harpley", "Victoria" or "VIC" anywhere in the database
- [ ] No occurrence of `bestconcretersmelbourne.com.au` in any table
- [ ] No `03 4427 9541` anywhere — replaced with the new NSW tracking number
- [ ] Every `_elementor_element_cache` row deleted
- [ ] All internal links resolve (no 404s, no links back to the Melbourne domain)
- [ ] Every image loads from the new domain and has been re-encoded
- [ ] All Rank Math titles 50–60 chars, descriptions 140–160 chars, no two structurally identical
- [ ] Suburb pages with empty module 8 are `noindex,follow`
- [ ] Astra Customizer settings imported and the site looks like the source
- [ ] Core Web Vitals green on mobile (Elementor + Astra can be heavy — check before launch, not after)
