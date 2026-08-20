# Context for ChatGPT — Camden concreting WordPress build

Copy everything below this line into a new ChatGPT conversation. If possible, also attach the reports listed under **Files to attach**.

---

You are advising me on the safe import, QA, launch, SEO rollout, and ongoing publication of a newly generated WordPress website for a concreting business serving Camden and South West Sydney, NSW, Australia.

Act as a critical WordPress migration lead, technical SEO reviewer, content-quality reviewer, and launch-risk adviser. Use Australian English. Do not invent business details, prices, licence information, an ABN, reviews, completed jobs, photographs, council requirements, or performance claims. When evidence is missing, tell me exactly what I need to obtain and how to verify it.

## Current date and project state

- Current project date: 15 August 2026.
- Workspace: `C:\Users\Home\Documents\concreters-camden`.
- Target domain: `https://concreterscamden.com.au`.
- Old source domain: `bestconcretersmelbourne.com.au`.
- This is an offline WXR transformation. Nothing has been deployed and no live WordPress site has been changed.
- The build completed all ten stages. Stage 9 passed all 15 validation gates and Stage 10 produced the handover pack.
- Final import file: `camden-concreting-import.xml`.
- Intended platform: a fresh WordPress install using Astra, Elementor 4.2.x, and Rank Math.

## What was built

The WXR contains 156 pages:

| Page type | Publish in import | Draft in import | Total |
|---|---:|---:|---:|
| Home | 1 | 0 | 1 |
| Utility | 4 | 0 | 4 |
| Services | 10 | 0 | 10 |
| Suburbs | 6 | 54 | 60 |
| Guide hub | 0 | 1 | 1 |
| Guides | 0 | 35 | 35 |
| Suburb/service intersections | 0 | 35 | 35 |
| Cost and comparison pages | 0 | 10 | 10 |
| Total | 21 | 135 | 156 |

The import also contains:

- 83 attachment records;
- 65 rebuilt menu items across five menus;
- one Elementor kit;
- Astra custom CSS.

The six Tier 1 suburb pages are Oran Park, Leppington, Gregory Hills, Gledswood Hills, Austral, and Harrington Park. They have `publish` status but deliberately use `noindex,follow` while real project photography is outstanding. The gallery is also `publish` plus `noindex,follow`.

Of the 21 pages marked `publish`, 14 currently use the default index setting and seven use `noindex,follow`.

## Guide hierarchy

- Hub URL: `/guides/`.
- Title: `Concreting Guides for South West Sydney`.
- Hub post ID: `1502`.
- Hub `post_name`: `guides`.
- Hub `post_parent`: `0`.
- Hub status: `draft`.
- All 35 guide pages are draft children with `post_parent=1502`.
- Every guide `post_name` is its final path segment only; no `post_name` contains `/`.
- No service, suburb, intersection, utility, home, or cost page has a nested URL or requires a parent.
- The hub links to all 35 guides, grouped under Council & approvals, Ground & engineering, Cost, Finishes & materials, and Problems & maintenance.
- The hub is exempt from the duplication metric because it is a shared index component.

Wave 2 rule: publish `/guides/` and its first guide batch together. Never publish the hub alone. A published hub with 35 draft children is an empty index and a soft-404 risk.

## Validation already completed

Stage 9 passed all 15 gates:

1. The XML parses and contains exactly 156 page items.
2. Elementor JSON parses on all 156 pages.
3. Elementor JSON round-trips exactly on all 156 pages.
4. Every page has exactly one H1.
5. The assembled XML has zero blocked Victorian/source terms, including the old domain and old phone number.
6. Every Elementor image ID resolves to one of the 83 attachment records.
7. Internal page and menu links resolve and there are zero orphans in the assembled model.
8. No `rank_math_schema_*` meta remains.
9. No `_elementor_element_cache` meta remains.
10. Duplication passes across 105 substantive pages: minimum unique score 60.46%, maximum pair overlap 35.16%, and no repeated sentence violates the limit. Forty-five research shells and the guide hub are deliberately exempt.
11. Rank Math titles are 50–60 characters and descriptions are 140–160 characters.
12. Complete Rank Math titles are unique.
13. All evidence markers are registered in `reports/placeholders.md`.
14. Every page has a non-empty focus keyword and the known Werribee spelling-error class was not copied.
15. Statuses match the intended split: 21 publish and 135 draft; the hub and all guides are draft.

Passing these gates means the file is internally consistent. It does not mean the current `publish` pages are ready to be indexed.

## Outstanding evidence

There are 163 unresolved marker occurrences:

- 55 need operator-supplied commercial evidence: real quoted rates, formulas, assumptions, quote turnaround, inclusions, or site-specific price inputs.
- 56 need verified business identity or review evidence: ABN, address, licence/insurance/operator profile, reviewer identity, review wording, and permission.
- 47 need verified project photography with suburb, service, date, and publication permission.
- 5 require authoritative verification: current council processes/specifications or the identified Oran Park estate claim.

Marker totals are 111 `PLACEHOLDER`, 47 `REAL_PHOTO_PENDING`, and five `VERIFY` occurrences.

Important exposure: 16 pages currently marked `publish` contain at least one `PLACEHOLDER`; seven published pages contain `REAL_PHOTO_PENDING`; one published page contains a `VERIFY` marker. Do not advise me to index all 21 publish-status pages merely because Gate 9 passed. I need a page-by-page readiness decision.

## Known launch blockers and risks that still need investigation

Treat these as priority issues:

1. **Unverified phone number:** `03 4517 6915` and `tel:+61345176915` appear throughout the model—120 visible-number occurrences across 119 pages, including published pages. Confirm ownership, correctness, and whether an `03` number is genuinely intended for a Sydney business. If it is not verified, it must be replaced everywhere before launch.
2. **Missing form dependency:** `/contact/`, `/quote/`, `/about/`, and `/gallery/` each contain `[fluentform id="3"]`. The WXR does not include a Fluent Forms form definition, and the current Stage 10 plugin list did not include Fluent Forms. Decide whether to install Fluent Forms and create/import form ID 3, or replace/remove those widgets. Verify recipient email, SMTP delivery, spam protection, consent/privacy copy, success handling, and mobile behaviour. Also decide whether forms belong on About and Gallery at all.
3. **Missing image binaries:** the workspace contains attachment metadata and an 83-file rename map, but not the actual `/uploads/2026/07/` image files. The files must be obtained from the source site or backup before `reencode-images.sh` can run. Attachment records passing the XML gate does not prove that images will render.
4. **Missing Astra Customizer export:** the runbook requires a separate Astra Options Import/Export file because `theme_mods` is not in the WXR, but no obvious Astra settings export is present in this workspace. Locate/export it or document how the global design will be reconstructed and visually verified.
5. **Draft links in menus:** both primary menus currently have a Blog parent pointing to `/guides/` and six guide children; `footer-blogs` also lists six guides. The hub and guides are drafts until Wave 2. If these menu locations are assigned during Wave 1, logged-out visitors may receive 404s or invalid menu items. Keep guide links out of the live Wave 1 navigation, or assign the guide menu only when the hub and first guides publish together.
6. **Published pages with markers:** the homepage and service/utility pages include unresolved evidence markers, while many are indexable by default. Audit rendered visibility and set temporary `noindex,follow` or draft status until each intended Wave 1 page is genuinely complete.
7. **Static homepage setting:** the WXR has a page model for the homepage, but `show_on_front` and `page_on_front` are WordPress options rather than normal page content. Set and verify the static homepage under Settings → Reading.
8. **Post-ID collisions:** Elementor image IDs and the guide hierarchy depend on imported post IDs. Before import, inspect the fresh target database after installing plugins. If target posts already occupy imported IDs, the WordPress importer may remap them while IDs embedded inside Elementor JSON may not be remapped reliably. Compare the target against `build/stage9-page-manifest.json` and `build/stage8-image-map.json`, take a database backup, and test the import on staging first.
9. **Attachment delivery sequence:** the prepared image files must exist at the new domain/path or be moved into the correct upload directory before attachment imports are relied upon. Verify original and generated thumbnail filenames, MIME types, file permissions, and case sensitivity.
10. **Schema requires real business data:** schema was deliberately removed. Rebuild one Rank Math `@graph` per page only after real business identity/contact data is confirmed. Use `LocalBusiness` on `/` and `/contact/` only. Suburb pages use `Service` plus `areaServed` referencing the canonical `#localbusiness` ID; never create a LocalBusiness node for each suburb.

## Required post-import order

1. Use a fresh WordPress install and install Astra, Elementor 4.2.x, Rank Math, and the decided form dependency before importing.
2. Import Astra Customizer settings separately.
3. Obtain, rename, re-encode, and move image files while preserving `/wp-content/uploads/2026/07/`.
4. Import `camden-concreting-import.xml`.
5. Run the old-domain `wp search-replace` as a dry-run first, then apply only if matches exist.
6. Delete `_elementor_element_cache` rows after backing up and confirming the database prefix.
7. Run Elementor Regenerate CSS & Data, then Sync Library.
8. Configure the static homepage and assign only menu locations appropriate for the current publication wave.
9. Rebuild Rank Math schema using verified facts.
10. Set permalinks to `/%postname%/`, flush, and verify trailing slashes, canonicals, and the guide parent/child URLs.
11. Resolve evidence markers page by page and publish only when each wave gate passes.
12. Crawl the logged-out site, verify mobile Core Web Vitals, then submit the sitemap only when intended pages are indexable.

## Publishing approach

- Do not publish all 156 pages together.
- Wave 1 is intended to contain the home, four utilities, ten services, and six Tier 1 suburbs, but every page still needs a readiness decision. The six Tier 1 suburbs and gallery deliberately remain noindex until real images/evidence are supplied.
- Wave 2 adds the guide hub and the first guide batch together. The old cumulative wave counts need recalculation because the hub adds a page and the project was reduced from the original 300-page architecture to 156 pages with only 35 validated intersections.
- Later suburbs, remaining guides, cost/comparison pages, and intersections remain draft until their research, evidence, performance, and impression gates pass.

## Files to attach if you can inspect files

Prioritise these smaller files instead of asking me to upload the 10 MB WXR immediately:

- `reports/10-handover.md`
- `reports/09-validation.md`
- `reports/post-import-tasks.md`
- `reports/placeholders.md`
- `reports/00-reconciliation.md`
- `build/stage9-page-manifest.json`
- `build/stage9-menus.json`
- `build/stage8-image-map.json`
- `reports/08-image-rename-map.csv`

The final WXR is `camden-concreting-import.xml`; ask for it only if you need to inspect XML implementation details.

## What I want from you

Give me a practical, critical next-step plan. Do not give generic SEO advice and do not assume that a passing build is launch-ready.

Please return:

1. A risk register split into **P0 blockers**, **P1 before indexing**, and **P2 before later waves**, with the evidence for each risk and the exact pass condition.
2. A staging-first import runbook with stop/go checks and a rollback point after each risky step.
3. A Wave 1 page-readiness matrix explaining which page groups can be indexable, which should be noindex, and what evidence is missing.
4. A revised publication-wave plan for the 156-page architecture, explicitly including the guide hub in Wave 2.
5. A WordPress QA checklist covering plugin/version compatibility, post-ID remapping, Astra settings, Elementor rendering, forms, menus, media, redirects, 404s, permalinks, canonicals, schema, robots, sitemaps, caching, security, backups, analytics, Search Console, and mobile Core Web Vitals.
6. A content and trust checklist covering phone, business name, address/service-area model, ABN, licensing/insurance wording, reviews, project claims, photos/permissions, quote evidence, and council citations.
7. A short list of questions I must answer or evidence I must obtain before you would approve indexing.
8. A recommended first 48-hour action plan and first 30-day monitoring plan.

Where current WordPress, Elementor, Rank Math, Astra, Fluent Forms, or search-engine behaviour matters, check current official documentation if browsing is available and label any inference. Challenge my assumptions when the safer answer is to delay indexing.
