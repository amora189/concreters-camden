# Report 56 — Cloudflare Pages verification

Deployment verified over HTTPS at `https://dcfb55ec.concreters-camden.pages.dev`.

| Check | Result |
|---|---|
| Homepage | 200 |
| About/contact/privacy | 200 |
| Representative service/suburb pages | 200 |
| Sitemap | 200; 76 URLs |
| Robots | 200; `Disallow: /` |
| `X-Robots-Tag` | Present: `noindex, nofollow` |
| Canonical host | `https://concreterscamden.com.au/` in static HTML |
| Public PHP routes | None in export |
| `/wp-admin` links | None |
| localhost/staging URLs | None |
| Old E&T/Melbourne/CoreX residue | None in static HTML scan |
| JSON-LD | WebPage + BreadcrumbList on all 76 pages |
| Media | 55 local permitted assets copied and resolved |
| Form processing | No silent form; visible email CTA only |
| Custom domain | Not configured; DNS unchanged |

The deployment remains intentionally non-indexable. A custom domain and final release approval are still required before any indexability change.
