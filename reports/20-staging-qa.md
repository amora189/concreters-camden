# Stage 20 — Protected staging QA

Audit date: 15 August 2026 (Australia/Sydney)

## Overall result

**BLOCKED — full Camden staging QA was not performed.**

The disposable WXR import failed the required attachment-resolution gate and was rolled back. The current local URL is a protected, functioning WordPress baseline, not an imported Camden website. Results below prove environment controls and rollback behaviour only; they are not visual or launch approval for any Camden page.

## Completed checks

| Check | Result | Evidence |
|---|---|---|
| Loopback isolation | Pass | Apache is published only at `127.0.0.1:8088`; database port is not published |
| Unexpected host protection | Pass | Request with `Host: concreterscamden.com.au` returns HTTP 403 |
| Global indexing block | Pass | Every route-crawl response includes `X-Robots-Tag: noindex, nofollow, noarchive`; `blog_public=0` |
| Robots file | Pass | `/robots.txt` disallows `/` |
| Debug secrecy | Pass after fix | `/wp-content/debug.log` returns HTTP 403; PHP errors are not displayed in pages |
| Permalinks | Pass at environment level | `/%postname%/`; baseline `/sample-page/` returns 200 |
| Draft handling | Pass at environment level | baseline draft `/privacy-policy/` returns logged-out HTTP 404 |
| Genuine 404 | Pass | random control route returns HTTP 404 |
| Desktop baseline browser render | Pass | no browser console/page errors; `staging/screenshots/20-rolled-back-baseline.png` |
| Mobile baseline browser render | Pass | 390×844 render; `staging/screenshots/20-rolled-back-baseline-mobile.png` |
| Database rollback | Pass | failed import was removed by restoring `01-before-disposable-wxr-import/database.sql` |
| Upload rollback | Pass | empty pre-import uploads checkpoint retained and validated by archive/checksum |

The debug-log check initially found HTTP 200 exposure. Apache configuration was corrected to deny the file, the image was rebuilt, and the repeat check returned 403.

## Route crawl

`reports/20-route-crawl.csv` contains all 156 expected URLs plus one genuine-404 control row.

- Expected Camden routes tested: 156.
- Actual HTTP 200: 1 (`/`, but it is the baseline site rather than imported homepage ID 12).
- Actual HTTP 404: 155 expected routes.
- Genuine 404 control: pass.
- Responses carrying global noindex header: 157 of 157.
- Camden QA decisions: 156 `BLOCKED` because the database was rolled back.

Draft-route 404s in this crawl cannot be credited as imported-draft handling: those page rows are absent. The separate baseline Privacy Policy draft provides the WordPress-level draft test.

## Checks blocked by the failed import gate

The following required checks could not be completed or approved:

- 156 imported routes/statuses and Wave 1 navigation.
- Correct Elementor rendering, kit 6, header/footer, colours, typography, spacing, responsive settings, and menu locations.
- All 83 attachments, thumbnails, image binaries, and 1,085 image-widget resolutions.
- Canonicals, per-page robots, Rank Math sitemap inclusion/exclusion, and one-graph schema output.
- Internal links, orphan detection, guide-link exclusion, redirects, and trailing-slash behaviour across imported routes.
- Visible evidence-token absence on approved pages.
- Old-domain/Victorian runtime search after domain replacement.
- Fluent Forms ID 3 rendering, mobile submission, SMTP and notification delivery.
- Phone link/routing and visible business details.
- Camden mobile performance, Core Web Vitals, caching behaviour, mixed content, and accessibility.
- Analytics/Search Console readiness beyond confirming that nothing was connected or submitted.

## Security/update and operational state

- Component versions and package checksums are recorded in `reports/12-environment.md`.
- PHP 8.4 emits a logged Elementor deprecation; authoritative staging should use PHP 8.3 or a confirmed patched Elementor version.
- No cache plugin or external cache layer is configured in the disposable environment.
- No production secret, SMTP credential, analytics identifier, or Search Console integration was added.
- No sitemap was submitted and no indexing protection was removed.

STAGE 20: PARTIAL ENVIRONMENT QA COMPLETE — CAMDEN SITE QA BLOCKED
