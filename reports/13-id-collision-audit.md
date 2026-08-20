# Stage 13 — Post-ID collision audit

Audit date: 15 August 2026 (Australia/Sydney)

Environment: disposable local WordPress smoke test at `http://127.0.0.1:8088/`.

## Imported ID inventory

The WXR contains 306 unique `wp_posts` IDs:

| Imported post type | Count | ID range / exact IDs |
|---|---:|---|
| Pages | 156 | Minimum 12; maximum 1502; exact set in `build/stage9-page-manifest.json` |
| Attachments | 83 | Minimum 17; maximum 1362; exact set in `build/stage8-image-map.json` |
| Elementor library kit | 1 | ID 6 |
| Astra custom CSS | 1 | ID 893 |
| Navigation menu items | 65 | IDs 1503–1567 |
| **Total** | **306** | All unique across post types |

The guide hub is page ID 1502. Its 35 guide children reference parent 1502. The 83 attachment IDs are also embedded in Elementor JSON and therefore must not be silently remapped.

## Occupied IDs by activation step

| Step | Occupied `wp_posts.ID` values | Change |
|---|---|---|
| Fresh WordPress 7.0.4 installation | 1, 2, 3 | Hello World post, Sample Page, draft Privacy Policy |
| Activate Astra 4.13.9 | 1, 2, 3 | No posts created |
| Activate Elementor 4.2.2 | 1, 2, 3, 4 | Default Elementor kit created at ID 4 |
| Activate Rank Math 1.0.276 | 1, 2, 3, 4 | No posts created |
| Activate WordPress Importer 0.9.5 | 1, 2, 3, 4 | No posts created |
| Activate Fluent Forms 6.2.12 | 1, 2, 3, 4 | No `wp_posts` rows created |

Fluent Forms created form IDs 1 and 2 in `wp_fluentform_forms`. Those are custom-table IDs, not `wp_posts.ID` values, and do not collide with WXR post IDs. The shortcode-required form ID 3 remains free but undefined.

## Collision result

- Final occupied `wp_posts.ID` set before import: `{1, 2, 3, 4}`.
- Current `wp_posts` auto-increment value: `5`.
- Imported Elementor kit ID: `6` — free.
- Imported page, guide-parent, attachment, custom CSS, and menu-item IDs — all free.
- Intersection of occupied IDs and all 306 imported IDs: **empty set**.
- Exact collisions: **0**.

Elementor's locally generated active kit is ID 4. The WXR kit is ID 6, and WXR import does not import the `elementor_active_kit` option. After import, ID 6 must be verified and then deliberately selected as the active kit; leaving option value 4 would render against the wrong default kit even though the import IDs themselves are intact.

## Hard-stop decision

The collision hard stop is **not triggered**. A disposable WXR smoke-test import may proceed without fetching attachments.

This does not authorise the authoritative import. The missing original media and Astra export continue to block that path.

STAGE 13: PASS — ZERO IMPORTED POST-ID COLLISIONS
