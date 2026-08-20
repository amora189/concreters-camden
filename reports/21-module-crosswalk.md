# Stage 21 — Suburb module crosswalk

Audit date: 18 August 2026 (Australia/Sydney)

## Authorities and method

The semantic numbering comes from `camden-concreting-seo-spec.md` §5. The implemented numbering comes from `camden-site-structure-and-silo.md` §5.1 and is demonstrated module by module in `oran-park-gold-standard.md`.

The mapping is content-based, not position-based. The SEO specification describes ten semantic responsibilities. The built template expands the technical ground content into three sections, adds a shared trust section, and combines CTA, FAQ and the price answer in its final module. A one-to-one positional mapping would therefore be wrong after built module 4.

## SEO 10-module → built 11-module crosswalk

| SEO §5 module | Semantic responsibility | Built module(s) | Mapping reason |
|---:|---|---|---|
| 1 | H1 + opening 80 words | **1 — Hero** | Exact content match: H1, differentiator-led opening and CTAs. |
| 2 | Services we do here | **2 — Our Services** | Exact content match: service grid ordered by local job mix. |
| 3 | Local build context | **3 — Local build context** | Exact content match: entities, housing era and local work profile. |
| 4 | Ground conditions | **4 — Ground conditions**, extended by **5 — Ground preparation** and **6 — Drainage, levels and crack control** | Built module 4 carries geology/soil. Built modules 5 and 6 expand the consequences into preparation, water, levels and movement; those extra technical sections have no standalone rows in the SEO ten-module list. |
| 5 | Council & approval path | **7 — Council crossovers** | Exact content match: application path and exact council specifications. |
| 6 | Typical jobs & real price band | Split across **3 — Local build context**, **5 — Ground preparation**, and the price portion of **11 — CTA + FAQ** | The built template has no standalone “typical jobs & price band” section. Typical job mix appears in modules 3 and 5; the real price question/placeholder appears in module 11's FAQ. |
| 7 | Recent job + photos | **8 — Local Work Completed** | Exact content match: real completed-work evidence and photographs only. |
| 8 | Suburb FAQ | FAQ portion of **11 — CTA + FAQ** | Exact semantic match, combined with the CTA in the built template. |
| 9 | Nearby areas | **10 — Areas We Cover** | Exact content match: curated neighbouring-suburb links. |
| 10 | Quote CTA | CTA portion of **11 — CTA + FAQ** | Exact semantic match, combined with the FAQ in the built template. |

## Built modules without a standalone SEO row

| Built module | Treatment |
|---:|---|
| **5 — Ground preparation** | An expansion of SEO module 4, with part of SEO module 6's typical-job context. It remains unique per suburb. |
| **6 — Drainage, levels and crack control** | An expansion of SEO module 4. It must be rewritten around the suburb's real water/level problem and is not a reusable generic block. |
| **9 — Why Customers Choose Us** | A shared trust component with no standalone semantic row in the SEO ten-module model. Its claims still require verified business evidence. |

## Noindex gate in built numbering

The SEO specification's noindex gate refers to **SEO modules 6 and 7**, not built modules 6 and 7. Against the implemented 11-module template, the gate is:

1. **SEO module 6 — typical jobs & price band:** inspect the relevant content spread across built modules **3, 5 and 11**. If a job assertion or price-band field is a placeholder or is not supported by real operator evidence, the page remains `noindex,follow`.
2. **SEO module 7 — recent job + photos:** inspect built module **8**. If it is empty, contains `REAL_PHOTO_PENDING`, uses stock media, or presents source-site/Melbourne imagery as Camden work, the page remains `noindex,follow`.

This gate is additive to the current hard rule for differentiators: a suburb page without a researched `unique_local_variable` remains `draft` + `noindex` even if its other modules are structurally present.

### Compact restatement

```text
NOINDEX if (
  built module 3/5/11 contains unresolved SEO-module-6 job or price evidence
  OR built module 8 lacks verified recent-job evidence and real photos
  OR the suburb unique_local_variable is missing/unresearched
)
```

WXR `publish` status does not override this gate.

## Crosswalk gate result

- All ten SEO semantic responsibilities map to the implemented template.
- All eleven built modules are accounted for.
- The noindex gate has been translated by content rather than by matching module numbers.
- Result: **PASS**.
