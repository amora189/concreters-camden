# Stage 15 — Disposable WXR import verification

Test date: 15 August 2026 (Australia/Sydney)

## Classification and result

This was a **disposable technical smoke-test import**, not the authoritative staging import. It was permitted by the Stage 11 exception and was run without attachment fetching so that no external site or old-domain media endpoint would be contacted.

Result: **FAILED MEDIA/ATTACHMENT INTEGRITY GATE; ROLLED BACK**.

The WXR was not changed. No live domain, DNS, public staging site, sitemap, or indexing setting was touched.

## What imported correctly

- WordPress Importer exited successfully for the non-media records.
- All 156 page IDs were present.
- Page statuses were exactly 21 `publish` and 135 `draft`.
- `/guides/` was page ID 1502, status `draft`, slug `guides`, and parent 0.
- Exactly 35 draft guide children had `post_parent=1502`.
- All 65 navigation menu-item IDs were present.
- Menu-item hierarchy/object metadata matched the WXR, and the five menu counts were 23, 23, 7, 6, and 6.
- All 156 `_elementor_data` values parsed as JSON.
- No `_elementor_element_cache` rows and no `rank_math_schema_*` rows were imported.
- Elementor kit ID 6 and Astra custom-CSS ID 893 were created at their requested IDs.

WordPress normally rebuilt navigation item `post_name`, display title, and `post_parent` fields from their linked objects. The authoritative menu hierarchy fields—`_menu_item_menu_item_parent`, object ID/type, URL, and menu term relationships—remained correct. Those normalizations are not an ID remap.

## Hard failure

Attachment fetching was deliberately disabled. WordPress Importer 0.9.5 therefore returned an attachment-processing error for every attachment and created **0 of the required 83 attachment records**.

Consequences:

- 83 required attachment IDs were absent.
- The 156 pages contained 1,085 Elementor image references using 73 distinct attachment IDs, all unresolved at runtime.
- The image IDs were unchanged in Elementor JSON, but they did not resolve to any attachment, let alone the intended binary.
- The required “existing and correct attachment” test could not pass.

The raw machine-readable failure record is `build/stage15-import-verification.json`.

## Importer-sequence defect confirmed

The completed handover says to place prepared files in their final `/wp-content/uploads/2026/07/` paths before WXR import. Inspection of the active WordPress Importer code and the smoke test establish that:

1. With attachment fetching disabled, `process_attachment()` exits before creating an attachment post.
2. With attachment fetching enabled, the importer downloads each attachment URL to a temporary file and copies it into the upload directory.
3. If the intended final filename is already present, `wp_unique_filename()` can suffix the imported file, breaking the exact filename-to-ID map.

This is an import-procedure defect, not evidence that the completed WXR itself should be regenerated. The original WXR remains unchanged.

## Elementor kit observation

Plugin activation created a local default kit at ID 4. The imported WXR kit kept ID 6, but WordPress normalized its slug to `default-kit-2` because `default-kit` already existed. The active-kit option remained 4, as expected because WXR does not carry that option.

Before an authoritative import, the backed-up local kit should be removed or otherwise isolated, and after import kit ID 6 must be verified before deliberately setting `elementor_active_kit=6`. Slug normalization alone is not attachment corruption, but leaving kit 4 active would render the wrong global settings.

## Rollback

The database was immediately restored from:

- `staging/backups/01-before-disposable-wxr-import/database.sql`
- `staging/backups/01-before-disposable-wxr-import/uploads.tar.gz`

After restore, the database again contained only the WordPress baseline IDs 1–3 and Elementor kit ID 4. Imported Camden pages, menus, attachment attempts, kit 6, and custom CSS 893 are no longer present.

## Safest authoritative recovery

Do not retry until the 83 original binaries and Astra export are supplied. Then:

1. Re-encode and checksum the 83 binaries into a source-staging directory outside the final uploads directory.
2. Use a local-only, audited import adapter to supply those prepared binaries to WordPress Importer without any network download and without pre-existing filename collisions; keep the completed WXR untouched.
3. Re-run the clean ID audit, remove/isolate the backed-up local kit 4, and import into a fresh checkpoint.
4. Require all 83 requested attachment IDs, `_wp_attached_file` names, signature MIME types, dimensions, checksums, and all 1,085 Elementor references to pass before continuing.

No domain replacement, Elementor regeneration, library sync, cache clearing, menu assignment, or post-import configuration was performed after the failed media gate.

STAGE 15: BLOCKED — DISPOSABLE IMPORT ROLLED BACK; AUTHORITATIVE IMPORT NOT PERFORMED
