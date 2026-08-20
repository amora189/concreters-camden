# Stage 16 — WordPress configuration status

Audit date: 15 August 2026 (Australia/Sydney)

## Safely completed on the protected baseline

- WordPress Address and Site Address: `http://127.0.0.1:8088` (also fixed by local configuration constants).
- Timezone: `Australia/Sydney`.
- Language: `en_AU`.
- Search visibility: blocked (`blog_public=0`) with web-server and WordPress robots protection.
- Permalink structure: `/%postname%/`.
- Standard Apache trailing/post-name rewrite rules: installed and verified.
- Published baseline page `/sample-page/`: HTTP 200.
- Baseline draft `/privacy-policy/` as a logged-out visitor: HTTP 404.
- Genuine random missing route: HTTP 404.
- Theme menu locations are unassigned; no draft-guide menu was exposed.

## Deliberately not completed

The authoritative import was rolled back, so the following cannot be truthfully configured or verified against Camden pages yet:

- Static homepage assignment to WXR page ID 12.
- Exact trailing-slash/canonical behaviour for all 156 Camden routes.
- Wave 1-safe primary/mobile/footer menu assignments.
- Runtime checks for orphaned Wave 1 pages, old-domain links, or links to unpublished guide pages.
- Runtime Rank Math canonical, robots, and sitemap decisions.

The imported menus must not be assigned unchanged in Wave 1 because their Blog/guide branches target draft content. At authoritative import time, use Wave 1-safe menu copies or a reviewed menu configuration that excludes `/guides/` and all guide children. The guide hub must remain draft until it and the first approved guide batch publish together.

No draft was published and no page was made indexable.

STAGE 16: BASELINE SETTINGS PASS — CAMDEN PAGE CONFIGURATION BLOCKED BY ROLLBACK
