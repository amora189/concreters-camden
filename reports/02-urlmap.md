STAGE 2 - URL map and ID allocation
=======================================
READ:      reports/00-reconciliation.md; codex-clone-prompt.md section 2 and section 3; suburbs-expanded.json; intersection-differentiators.json; source WXR item IDs
DID:       Built URL map for direct transformations, new pages and deletions; allocated sequential post IDs above the highest source ID; wrote global replacement table.
ARTIFACTS: build/url-map.json; build/id-map.json; build/global-replace.json; reports/02-urlmap.md

- Highest existing post_id: 1362
- New pages allocated: 139
- New post_id range: 1363 to 1501
- Direct transformations: 16
- Deletions: 3
- Total target URLs mapped: 155

GATE 2: PASS
  ? Every new post_id is unique and unused
  ? Every target URL in the map is unique
  ? Every post_name slug is lowercase and hyphenated with no trailing slash

Proceeding to Stage 3.
