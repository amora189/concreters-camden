# Post-import tasks

Complete these tasks in order. Do not submit a sitemap or remove a deliberate `noindex` until the relevant content and technical checks are complete.

## 1. Prepare WordPress

- Start with a fresh WordPress install.
- Install and activate Astra, Elementor **4.2.x**, and Rank Math before importing the WXR.
- Do not use Elementor 3.x: the imported pages contain Elementor 4 atomic `e-heading` widgets.

## 2. Import Astra Customizer settings separately

- Import the Astra Customizer settings through Astra Options Import/Export.
- These settings live in `theme_mods` and are not contained in the WXR.

### 2a. Two import-time exclusions (owner decision, 19 August 2026)

**`source-inputs/astra/astra-export.dat` is left exactly as received** — SHA-256 `F4841CF5…`, not
edited. The exclusions are applied at import, so the supplied file continues to match the audit
trail.

| Key | Action | Why |
|---|---|---|
| `wp_css` | **DO NOT IMPORT** | Byte-identical to the WXR's `custom_css` post 893 except one comment line: the export says `/* Local Werribee project cards */`, the WXR says `/* Local Camden project cards */`. The export is a pre-rename snapshot. |
| `mods.nav_menu_locations.footer_menu` | **DO NOT APPLY AS SUPPLIED** | Maps to term 13 (Footer Blogs); all 6 targets are withdrawn and draft. See step 8. |

- Import the generated active derivative, which excludes post 893 entirely because D32 removes every
  `.local-work-card` module and leaves the stylesheet dead. Do not recreate the post or assign
  `custom_css_post_id=893`.
- Whichever method is used (filter the keys before applying, or apply then correct), **do not edit
  the `.dat` file on disk.**
- Verify afterwards: **zero occurrences of `Werribee`** in `wp_posts` and `options`.

> **The global styling caveat that used to sit here has changed.** This export carries no colours,
> typography, layout, header, footer or button mods — because the source site never set any. There
> is no "wrong global styling" risk from skipping it, and no right global styling to gain: the
> design is inlined per-widget across 156 pages. See the standing finding in `CONTEXT.md` and
> `reports/42-astra-vs-elementor-design-carriage.md`.

## 3. Prepare and move uploads

- **First:** `scripts/22-media-audit.py` must pass. It now fails on any non-image file in
  `source-inputs/media/` (DECISION-08 D38) — that directory is staged for a public web server.
- Apply `reports/08-image-rename-map.csv` to the source upload filenames. Six binaries were
  delivered under a ` (1)` collision-rename and must be renamed to their authoritative names first;
  see `reports/22-media-intake-reconciliation.md` §4.
- Run `scripts/22-reencode-images.sh` **in WSL** (ImageMagick and exiftool are installed there, not
  on the Windows host) to strip EXIF, resize to 98%, and save at quality 82. The original
  `reencode-images.sh` has never parsed and must not be used.
- Regenerate and check `build/47-media-remediation.csv` through
  `scripts/46-architecture-import-gate.py`. It covers all 83 provenance records: **51 public
  files**, 16 excluded/retired files and 16 unresolved Band A files held fail-closed. Exclusions
  remain recoverable in `source-inputs/media-retired/`; blank-verdict Band A files remain in
  `source-inputs/media-held-band-a/`. Neither quarantine directory is copied to uploads.
- Move the resulting files into `/wp-content/uploads/`, preserving the `2026/07/` directory structure exactly.

## 4. Import the WXR

- Import only the generated `build/46-active-main-import.xml`, never the immutable 156-page WXR.
- Confirm that the main import contains exactly 75 active-architecture pages, **51 permitted
  attachments**, no `custom_css` record and none of the 81 withdrawn pages. Import the privacy WXR
  separately under its own allowlist entry. No excluded or held attachment record may be recreated
  by remote fetching.

## 4a. Do not run the retired Band B database mutator

- Band B, D32 and the broader Phase B payload rules are already applied by the reproducible
  derivative generator. `staging-authoritative/scripts/apply-band-b-remediation.sh` is now a
  deliberate fail-closed guard.
- Verify the generated contract instead: 17 D32 top-level sections removed across all 16 recorded
  pages, 47 `REAL_PHOTO_PENDING` fields absent, both UNUSABLE attachment records absent, and every
  remaining Elementor media reference resolving to a permitted attachment.

## 5. Run the domain replacement

- Run a dry-run first:

  `wp search-replace 'bestconcretersmelbourne.com.au' 'concreterscamden.com.au' --all-tables --dry-run`

- Review the result, then run the same command without `--dry-run` if replacements are reported. WordPress import remapping is not reliable inside `_elementor_data` stored in `wp_postmeta`.

## 5a. Rename the trading name to Structure Co (DECISION-08 D35)

Plan and counts: `reports/38-trading-name-rename-plan.md`. Run **after** the domain replacement in
step 5 and **before** the Elementor cache clear in step 6.

**Order matters. Longest string first**, or `CoreX Concreters Camden` becomes
`Structure Co Concreters Camden Concreters Camden`.

```bash
wp search-replace 'CoreX Concreters Camden'  'Structure Co Concreters Camden' --all-tables --precise --dry-run
wp search-replace 'CoreX'                    'Structure Co'                   --all-tables --precise --dry-run
wp search-replace 'E&T Co Concreters Camden' 'Structure Co Concreters Camden' --all-tables --precise --dry-run
```

- `--precise` is **required**. `_elementor_data` is a serialised blob in `wp_postmeta`, and
  `CoreX` (5 chars) → `Structure Co` (12 chars) changes every containing string's length. A
  length-unaware replace corrupts it.
- Check each dry-run count before running for real: **71** for the full phrase, **395** for the
  remaining bare `CoreX`, **1** for the kit `site_name`.
- **Attachment filenames, slugs, GUIDs and URLs are NOT renamed** — 100 of the 466 occurrences.

  > **DELIBERATE ACCEPTANCE, owner decision 19 August 2026.** Image URLs keep the `corex-` prefix
  > permanently. Rationale as decided: breaking 1,085 Elementor image references for a string no
  > reader sees is a bad trade. Consequence accepted: `…/uploads/2026/07/corex-concreters-camden-
  > logo-306.png` and 99 similar paths will be visible in page source, image URLs and any CDN log
  > for the life of the site. This is recorded so it is never re-raised as an oversight, and so the
  > §5d verification gate can exclude filenames explicitly rather than implicitly.

## 5b. Correct the site name and tagline (D30, retargeted by D35)

- Elementor → Site Settings → `site_name` → **Structure Co Concreters Camden**
- Settings → General → Site Title → **Structure Co Concreters Camden**
- Settings → General → Tagline: the current value is `Camden based Concrete Company Site`.
  **REMOVE it. Set it empty.** Owner decision, 19 August 2026: it is not renamed and not rewritten,
  because no trading name makes "Camden based" supportable — fulfilment is Pakenham (D32).
  - Set `blogdescription` to an empty string, and confirm the Astra header/footer does not render a
    fallback tagline in its place. Some Astra header layouts print the site title and tagline as a
    pair; an empty tagline must render as nothing, not as a placeholder.
  - Verify afterwards: zero occurrences of `Camden based` anywhere in `options`, `theme_mods`, or
    any rendered page.

## 5c. Assign the favicon and header logo (DECISION-08 D36)

**PARTIALLY UNBLOCKED.** As at 19 August 2026:

1. ~~`source-inputs/brand/` is empty.~~ **CLEARED** — five SVGs and five favicon PNGs verified on
   disk. Inventory: `reports/39-brand-assets-and-image-slots.md`.
2. ~~The site icon needs a PNG render.~~ **CLEARED** — PNGs supplied at 512, 270, 192, 180 and 32,
   dimensions read from the file headers and metadata confirmed clean.
3. **The Astra Customizer export does not exist, and it governs header rendering.** Unchanged. Do
   not attempt the header, sticky, footer or mobile assignments until it arrives.

**The site icon proceeds independently.** `Settings → General → Site Icon` is a WordPress core
setting, not an Astra theme mod, so it does not wait on the Customizer export — only on the import.

| Slot | Asset file (verified on disk) | Where | Waits on Astra export? |
|---|---|---|---|
| Site icon / favicon | `structure-co-icon-512.png` (WordPress generates 270/192/180/32; the pre-rendered versions are on disk if needed) | Settings → General → Site Icon | **No** |
| Header logo | `structure-co-horizontal.svg` | Astra → Header Builder → Site Identity | Yes |
| Sticky / condensed header | `structure-co-horizontal.svg` or `structure-co-icon.svg` | Astra → Header Builder, sticky variant | Yes |
| Footer mark | `structure-co-horizontal-reversed.svg` (on navy) or `structure-co-horizontal-mono.svg` | Astra → Footer Builder | Yes |
| Mobile header | `structure-co-stacked.svg` or `structure-co-icon.svg` | Astra → Header Builder, mobile variant | Yes |

**Upload the PNG, not the SVG, for the site icon.** WordPress does not accept an SVG site icon, and
**no SVG-upload plugin is to be installed** — owner decision, 19 August 2026: a stored-XSS vector is
not worth one favicon. The SVGs are for the Astra logo slots, which accept them.

- Upload the brand assets as **new** attachments. Do not overwrite 177, 159, 306, 307 or 422 —
  the WXR is immutable and its attachment IDs must keep resolving.
- Palette for any accompanying CSS, verified from the files themselves and confirmed by the owner
  19 August 2026:

  | Colour | Role |
  |---|---|
  | `#1C244B` | navy, primary |
  | `#7C8494` | grey, secondary |
  | `#AEB6C6` | **reversed-context tint only** — `#7C8494` lifted for legibility on navy. Not a third brand colour; do not use it as one. |
- Then unset the superseded marks:
  - **177** — currently the site icon. Replace it; it is AI-generated.
  - **272** — remove per D24; AI-generated, live on 14 pages.
  - **159, 422** — orphaned. Leave unreferenced. Do not delete.
  - **306, 307 and 422 are RETIRED** (owner, 19 August 2026), replaced by the Structure Co
    wordmark. They stay in the immutable WXR and are not deleted from it.
  - **306 and 307 were NOT orphaned.** D27 recorded them as unreferenced; they were not. **306 was
    on 8 pages** (`/contact/`, `/quote/`, `/about/`, `/gallery/`,
    `/concrete-patios-south-west-sydney/` — all publish — plus 3 draft patio pages). **307 was on
    2 pages** (`/concrete-paths-south-west-sydney/` publish, `/concrete-paths-edmondson-park/`
    draft). Their replacement is decided:

    | Placement | Asset |
    |---|---|
    | In-page brand placement | `structure-co-horizontal.svg` |
    | On a dark background | `structure-co-horizontal-reversed.svg` |

    **6 slots are on live pages and take the wordmark. 4 are on withdrawn intersection pages and
    need nothing** — those pages are excluded at import and enter no wave. Sourcing cost: zero.

    **The §4.22.4 sighting still applies.** No slot is called correct until it has been looked at —
    the right asset is not the same as the right size, position and context.
- Colours for any CSS: navy `#1C244B`, grey `#7C8494`. Note `#1C244B` is inherited from the source
  Elementor kit palette — a disclosed residual footprint, reused by owner choice.
- Verify the favicon at 32×32, 180×180, 192×192 and 270×270. WordPress generates these from the
  square icon; check the small sizes are legible rather than assuming.

## 5d. Verify the rename, fail-closed

Zero occurrences of `CoreX`, `E&T`, `E&T Co`, or `Camden based` in: `post_title`, `post_content`,
`postmeta`, `options` (`blogname`, `blogdescription`), `theme_mods`, term names, menu labels, and
every rendered page fetched over HTTP.

Attachment filenames and GUIDs are **excluded** by 5a; the gate names that exclusion explicitly
rather than leaving it implicit. Preflight gate 13 must be widened to cover `CoreX` and **will fail
until this step runs**, which is correct.

Rank Math caches its titles: 114 `rank_math_*` occurrences are covered by 5a, but regenerate the
metadata and sitemap afterwards and re-verify zero hits.

## 6. Clear Elementor element caches

- Back up the database, confirm the table prefix, then remove stale Elementor element caches:

  `DELETE FROM wp_postmeta WHERE meta_key = '_elementor_element_cache';`

## 7. Regenerate Elementor data

- In WordPress, open Elementor → Tools.
- Run **Regenerate CSS & Data**, then **Sync Library**.

## 8. Assign menu locations

Menu-location assignments are stored in `theme_mods` and are not carried by the WXR. The Astra
export supplies them, and **the supplied `footer_menu` mapping must not be applied.**

**There are five menus and three Astra theme locations.** This is a decision, not a lookup.

| Astra location | Term | Menu | Items | Status |
|---|---:|---|---:|---|
| `primary` | 9 | Primary | **10** | prune from 23 |
| `mobile_menu` | 10 | Primary (2) | **10** | prune from 23 |
| `footer_menu` | **11** | **Footer Services** | **7** | clean as-is |
| — | 12 | Footer Areas | — | **unassigned** |
| — | 13 | Footer Blogs | — | **unassigned** |

- **Prune `primary` and `mobile_menu` against `build/27-wave1-menus.json`** — 23 → 10 items each,
  13 removed from each. That file preserves `_menu_item_menu_item_parent` relationships for retained
  items, so parent/child structure survives the prune.
- **`footer_menu` takes Footer Services (term 11)**, not the supplied term 13. All 7 items are
  retained by Wave 1 filtering — it is the only one of the five menus that survives intact.
- **Footer Blogs (13) is not assigned at all.** All 6 targets are withdrawn and draft.
- **Footer Areas (12) is not assigned either.** It has zero withdrawn and zero draft, but all 6
  targets are Tier 1 suburb pages **held `noindex,follow`** — Oran Park, Leppington, Gregory Hills,
  Gledswood Hills, Austral, Harrington Park. 0 of 6 retained. **It fails on the third condition, not
  the first two**, which is exactly why the preflight assertion tests all three.
- Preflight gate: **no menu item in an assigned location may resolve to a withdrawn, draft or
  noindex-held page.**

## 9. Rebuild Rank Math schema

**As at 19 August 2026 this step emits NO `LocalBusiness` and NO `Organization`.** See D2's ladder
and `DECISION-08` D37.

- Rebuild schema according to `camden-concreting-seo-spec.md` §7, using one `@graph` per page.
- **`LocalBusiness` requires a verified STAFFED address (§4.30.2).** An address alone does not
  satisfy it. `data/verified-facts.yml` records `15 Murray Street, Camden NSW 2570` with
  `verified: false` and `is_staffed: unknown`, so the node **must not be emitted** — not on `/`,
  not on `/contact/`, not anywhere.
- `Organization` requires a verified legal entity. `Structure Co Concreters Camden` is a trading
  name with `verified: false`; it is **not** an entity and must not define `#organization`.
- Therefore **D2 ladder outcome 3 applies on every page: `Service` omits `provider` entirely.**
  A `Service` with no provider is incomplete but true; a `Service` pointing at an undefined `@id`
  is neither. Log the count of `Service` nodes omitting `provider`, per page class.
- Build-failing check: **zero references to any `@id` not defined in the same emitted graph.**
- When the entity and staffed status are verified, revisit: add `LocalBusiness` only on `/` and
  `/contact/`; suburb pages use `Service` plus `areaServed` referencing the canonical
  `#localbusiness` `@id`; never create a separate `LocalBusiness` node per suburb.

## 10. Configure and verify permalinks

- Set the permalink structure to `/%postname%/` and flush rewrite rules.
- Confirm that page URLs use trailing slashes and that Rank Math canonicals match.
- Verify `/guides/` is the parent of all 35 guide pages and that the child URLs resolve as `/guides/{final-segment}/`.

## 11. Resolve evidence markers and publish by wave

- Work through every occurrence in `reports/placeholders.md`. Supply only verified operator details, real quote evidence, approved project photographs, and current authoritative council information.
- Keep research shells, intersections, cost pages, and other later-wave content as `draft` until their specific release gate is satisfied.
- Publish eligible Tier 2/3 pages only after their research, real-photo, pricing, schema, and noindex requirements are complete.

### Wave 2 — guide hub constraint

- Publish `/guides/` and its first Wave 2 guides together. Never publish the hub alone.
- A published hub whose 35 children remain drafts is an empty index and a soft-404 risk.
- The import deliberately keeps the hub and all 35 guide children as `draft`.

## 12. Verify performance before sitemap submission

- Crawl the site as a logged-out visitor and confirm page status, canonicals, internal links, image loading, schema, robots directives, and the guide hierarchy.
- Verify Core Web Vitals on mobile.
- Submit the sitemap only after the intended first-wave pages are complete and indexable.
