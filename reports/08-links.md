STAGE 8 — Links, menus, images
=======================================
READ:      CODEX-BUILD.md Stage 8; camden-site-structure-and-silo.md §4 and §7; codex-clone-prompt.md §6–§8; expansion-300-pages.md §9; Stage 7 page models
DID:       Rewrote internal links, added contextual inbound paths for intersections/guides/cost pages, enforced six highest-weight suburb links per service, built the requested menu manifest, renamed 83 attachments, distributed image use, and rewrote page-specific alt text.
ARTIFACTS: build/stage8-all-pages.json; build/stage8-menus.json; build/stage8-image-map.json; reports/08-link-graph.csv; reports/08-image-rename-map.csv; reencode-images.sh; reports/08-links.md

## Link graph

- Internal link records: 1163
- Existing target URLs: 155
- Unresolved targets: 0
- Orphan pages: 0
- Suburb pages exceeding four direct suburb neighbours: 0

## Menus

- Primary and Primary (2): Services 7, Areas 6, Blog 6, Contact 1 each
- Footer: Areas 6, Services 7, Blogs 6
- Primary parent/child relationships are represented explicitly in build/stage8-menus.json for Stage 9 assembly.

## Images

- Attachment records renamed: 83
- Widget image IDs unresolved: 0
- Maximum pages using one attachment: 15
- Every assigned widget image URL names the attachment selected by its post ID.

GATE 8: PASS
  ✓ Every internal link target exists: 0 failures
  ✓ Zero orphan pages: 0 orphans
  ✓ Every image ID resolves to an attachment: 0 failures
  ✓ No suburb-to-suburb full mesh: 0 violations
  ✓ No attachment appears on more than 15 pages: maximum 15
  ✓ Menu counts and parent groups match the Stage 8 specification: {"primary_services": 7, "primary_areas": 6, "primary_blogs": 6, "primary_2_services": 7, "primary_2_areas": 6, "primary_2_blogs": 6, "footer_areas": 6, "footer_services": 7, "footer_blogs": 6}

Proceeding to Stage 9.
