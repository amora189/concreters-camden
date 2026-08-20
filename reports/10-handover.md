# Stage 10 — Handover pack

Stage 10 packages the passing Gate 9 import with the ordered post-import runbook and publication safeguards. No live site was changed or deployed.

## Import summary

| Page type | Publish | Draft | Total |
|---|---:|---:|---:|
| Home | 1 | 0 | 1 |
| Utility | 4 | 0 | 4 |
| Services | 10 | 0 | 10 |
| Suburbs | 6 | 54 | 60 |
| Guide hub | 0 | 1 | 1 |
| Guides | 0 | 35 | 35 |
| Intersections | 0 | 35 | 35 |
| Cost and comparison | 0 | 10 | 10 |
| **Total** | **21** | **135** | **156** |

The `/guides/` hub has post ID `1502`, status `draft`, and `post_parent=0`. All 35 guides are draft children with `post_parent=1502` and final-segment-only `post_name` values.

## Outstanding evidence

There are **163 outstanding marker occurrences** in `reports/placeholders.md`:

| What is needed | Count | Included markers |
|---|---:|---|
| Operator-supplied commercial evidence | 55 | Real quoted rates, formulas, assumptions, quote turnaround, inclusions, and site-specific price inputs |
| Verified business identity and review evidence | 56 | ABN, business address, licence/insurance/operator profile, reviewer identity, review text, and permission |
| Verified project photography | 47 | Real project image, suburb, service, date, and permission to publish |
| Authoritative verification | 5 | Current council processes/specifications and the identified Oran Park estate claim |
| **Total** | **163** | 111 `PLACEHOLDER`, 47 `REAL_PHOTO_PENDING`, and 5 `VERIFY` occurrences |

Repeated markers remain separate occurrences because each rendered page must be checked and cleared independently.

## Three prerequisites before indexing

1. Complete the import correctly: install the required theme/plugins first, import Astra settings and prepared uploads, import the WXR, run the domain dry-run/replacement, clear caches, and regenerate Elementor data.
2. Replace every marker on pages intended for release with defensible evidence and rebuild the required Rank Math schema. Do not invent prices, business details, reviews, project claims, photographs, or council facts.
3. Verify the logged-out site end to end: intended publish status and robots directives, permalinks, canonicals, internal links, media, schema, mobile Core Web Vitals, and publication-wave rules. Only then submit the sitemap or request indexing.

## Wave 2 safeguard

Publish the guide hub and its first guide batch together. Never publish `/guides/` while all guide children remain drafts.

## Handover files

- `camden-concreting-import.xml` — validated import file.
- `reports/09-validation.md` — all 15 Gate 9 checks passed.
- `reports/post-import-tasks.md` — ordered WordPress import and release runbook.
- `reports/placeholders.md` — occurrence-level evidence register.
- `reports/08-image-rename-map.csv` and `reencode-images.sh` — upload preparation inputs.

STAGE 10: COMPLETE
