# Report 56 — Cloudflare Pages static export

Date: 21 August 2026 (Australia/Sydney)

- Source: approved mutable derivative `build/46-active-main-import.xml`.
- Export method: reproducible local static builder (`scripts/56-build-static-export.py`) from the approved derivative. The official Simply Static plugin was not run because the private PHP 8.3 WordPress staging/import environment was not available; this remains a production-release blocker requiring plugin-based parity verification.
- Output: `build/cloudflare-pages/`.
- Static HTML pages: 76.
- Permitted media copied: 55.
- Public PHP files: 0.
- Sitemap URLs: 76.
- Withdrawn pages: excluded.
- Calculator: absent.
- Forms: replaced with visible email CTA because no verified external endpoint exists; no native WordPress form processing is shipped.
- Indexability: retained `noindex,nofollow` in HTML, `X-Robots-Tag`, and `robots.txt Disallow: /`.

Cloudflare Pages project: `concreters-camden`.

Deployment URL: https://dcfb55ec.concreters-camden.pages.dev

Deployment ID/prefix: `dcfb55ec`.

No WordPress database, WXR, Docker files or credentials were uploaded.
