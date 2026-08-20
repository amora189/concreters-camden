# Stage 20 — Mobile performance status

Audit date: 15 August 2026 (Australia/Sydney)

## Decision

Camden mobile performance and Core Web Vitals are **not measurable yet** because the authoritative pages, Astra settings, 83 images, menus, form, schema, and production-like cache are not present after rollback.

## Baseline-only synthetic run

A Lighthouse mobile run was completed against the protected WordPress sample page solely to verify the local Chrome/Lighthouse path. The JSON artifact is `build/stage20-lighthouse-baseline.json`.

| Metric/category | Baseline result |
|---|---:|
| Performance | 100 |
| Accessibility | 95 |
| Best Practices | 100 |
| SEO | 58 |
| First Contentful Paint | 1,363 ms |
| Largest Contentful Paint | 1,363 ms |
| Speed Index | 1,363 ms |
| Total Blocking Time | 0 ms |
| Cumulative Layout Shift | 0 |

Emulation used a mobile Moto G Power user agent. Accessibility lost points because baseline text links rely on colour. SEO was deliberately reduced by the mandatory indexing block and the sample page’s missing meta description.

Lighthouse wrote a complete parseable report, then its command exited nonzero while cleaning a Windows temporary profile (`EPERM`). The metrics above are therefore useful only as a tool-chain smoke test. They are not Camden scores and are not a launch gate result.

Field Core Web Vitals are unavailable for a loopback-only, never-published site. After authoritative import, run synthetic mobile tests on representative home, utility, service, Tier 1 suburb, guide, intersection, and cost templates, then collect real-user data only after an explicitly approved protected-to-live release.

No Elementor layout/style change was made for performance.

STAGE 20 MOBILE PERFORMANCE: BLOCKED — BASELINE TOOLING ONLY
