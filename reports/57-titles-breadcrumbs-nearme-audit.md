# Report 57 — spec sections 6.5 and 8, run against the built output

Run: 24 August 2026 (Australia/Sydney). Command: `scripts/57-seo-spec-gate.py`.
Target: `build/cloudflare-pages/` (78 pages + 404). Authority: the supplied titles /
breadcrumbs / near-me spec as amended by DECISION-10 D42–D44.

This report states what was verified against artifacts on disk. It describes no live site,
no launch and no approval. `BLOCKED` rows name their authority; no assertion
was narrowed or deleted to make it pass (CLAUDE.md §3 hard stop 7).

| # | Assertion | Result | Detail |
|---|---|---|---|
| 1 | no 'enquir' in any title or h1 | **PASS** | titles and H1s |
| 2 |  | **PASS** | no 'near me' in any title, h1 or URL |
| 3 |  | **PASS** | every title <= 60 characters |
| 4 |  | **PASS** | every title unique sitewide |
| 5 |  | **PASS** | spec suburb titles and descriptions resolved from suburbs.json, no template fallback |
| 6 |  | **PASS** | authored meta descriptions are 150-158 characters |
| 7 | suburbs.json meta descriptions are used verbatim, length rule waived (C4) | **PASS** | 15 descriptions, 126-182 chars as authored in suburbs.json |
| 8 |  | **PASS** | /areas/ exists and is indexable |
| 9 |  | **PASS** | /services/ exists and is indexable |
| 10 |  | **PASS** | /concreters-camden/ 301s to / |
| 11 |  | **PASS** | every old flat service URL 301s to /services/{slug}/ |
| 12 | no redirect chains and no loops | **PASS** | chains=[] loops=[] |
| 13 |  | **PASS** | no flat service directory still serves a page |
| 14 |  | **PASS** | no '#' in any BreadcrumbList item |
| 15 |  | **PASS** | no BreadcrumbList exceeds 3 items |
| 16 |  | **PASS** | terminal ListItem carries no item |
| 17 |  | **PASS** | visible breadcrumb labels match JSON-LD names |
| 18 |  | **PASS** | terminal crumb matches the page h1 subject |
| 19 |  | **PASS** | homepage carries no breadcrumb |
| 20 |  | **PASS** | every crumb URL resolves to a built page |
| 21 | exactly the 6 Tier 1 suburb pages are index,follow | **PASS** | got ['/concreters-austral/', '/concreters-gledswood-hills/', '/concreters-gregory-hills/', '/concreters-harrington-park/', '/concreters-leppington/', '/concreters-oran-park/'] |
| 22 |  | **PASS** | every non-Tier-1 suburb page is noindex,follow (DECISION-10 D44) |
| 23 |  | **PASS** | sitemap contains zero noindex URLs |
| 24 |  | **PASS** | every indexable page is in the sitemap |
| 25 |  | **PASS** | no LocalBusiness or GeneralContractor node outside / and /contact/ |
| 26 |  | **PASS** | no AggregateRating or Review markup anywhere |
| 27 |  | **PASS** | every FAQPage Q&A string appears verbatim in the rendered HTML |
| 28 |  | **PASS** | every in-scope suburb page carries a Service node with areaServed |
| 29 |  | **PASS** | areaServed postalCode comes from suburbs.json |
| 30 |  | **PASS** | no dangling #organization reference |
| 31 |  | **PASS** | spec section 5.1 near-me H2 on every in-scope suburb page |
| 32 |  | **PASS** | near-me H2 appears exactly once per page |
| 33 |  | **PASS** | spec section 5.2 near-me FAQ on every in-scope suburb page |
| 34 |  | **PASS** | near-me FAQ answers are 40-60 words |
| 35 |  | **PASS** | spec section 5.4 lists 3-5 services per suburb |
| 36 |  | **PASS** | spec section 5.4 paragraphs are 40-70 words |
| 37 | spec section 5.4 paragraphs are unique sitewide | **PASS** | 0 duplicates |
| 38 | spec section 5.3 /areas/ anchor text is varied | **PASS** | 36/60 exact-match |
| 39 |  | **PASS** | every page is reachable within 2 clicks of / |
| 41 | sitewide Organization node (spec section 7.2) | **BLOCKED** | DECISION-08 D35 clause 4 does not authorise an Organization node; legal_entity.legal_name is unverified. Service + WebPage + BreadcrumbList + FAQPage ship instead. No @id is referenced, so nothing dangles. |
| 42 | spec section 5.2 price FAQ and '{X} business days' | **BLOCKED** | pricing.per_m2_ranges verified:false, blocks_pages:53. No response-time commitment recorded. Both withheld with an inline marker in every page. |
| 43 | Tier 2 and Tier 3 noindex cannot be lifted | **BLOCKED** | Spec section 4 requires a real quoted price AND a real photograph. pricing.per_m2_ranges and photography.real_camden_photographs are both verified:false. All 10 stay noindex,follow. |
| 44 | spec section 3 /services/stencilled-and-stamped-concrete/ | **BLOCKED** | No source page exists in build/46-active-main-import.xml. Not built rather than published thin. 10 of the spec's 11 service pages ship. |
| 45 | Bringelly council resolved against evidence | **PASS** | resolved as split-locality per build/53-council-suburb-map.json: Camden Council and Liverpool City Council, lot-level check required. The page names no single council, per its public_wording_rule. The spec's 'resolve to one council' is unsatisfiable because the locality genuinely straddles the boundary. |
| 46 | 45 out-of-scope suburb pages carry no spec data | **BLOCKED** | DECISION-10 D44 keeps them published and noindex,follow. They have no suburbs.json record, so no near-me FAQ, Service node or section 5.4 block is emitted for them. |

**40 pass, 0 fail, 5 blocked, 1 retired**

## What the blocked rows need

| Blocker | Owner input required |
|---|---|
| Tier 2/3 indexation, and the §5.2 price FAQ | A per-m² price band per finish the owner will stand behind in writing, and real Camden photographs with permission to publish. `verified-facts.yml` records both as `verified: false`, blocking 53 and 16 pages respectively. |
| `Organization` schema (§7.2) | A verified legal entity name. DECISION-08 D35 clause 4 does not authorise the node; a trading name is not a legal entity. |
| §5.2 "within {X} business days" | A response-time commitment the owner will stand behind. None is recorded. |
| `/services/stencilled-and-stamped-concrete/` | Source content. The spec lists 11 service pages; 10 have a source page in `build/46-active-main-import.xml`. Not built rather than published thin. |
| The 45 out-of-scope suburb pages | Tier, title, meta description, postcode, local entities and job mix per suburb, if they are ever to be indexable. They ship `noindex,follow` under D44. |

## Bringelly

The spec asks for the LGA to be "resolved to a single verified council". It cannot be, and
that is the correct answer rather than a gap. `build/53-council-suburb-map.json` records
Bringelly as `split-locality` across Camden Council and Liverpool City Council with
`lot_level_check_required: true`, citing both councils' own suburb lists and the NSW Planning
Portal. The page therefore names no single council and states that the controlling council
must be confirmed lot by lot, per that record's `public_wording_rule`. Leppington is handled
the same way for the same reason.

## Hash table — CLAUDE.md §1 immutable files

Recomputed 24 August 2026 against the Gate 21 table. All six match; none was modified.

| File | SHA-256 | Gate 21 |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |

**6/6 MATCH.**

---

## Superseded

The `RETIRED` row for the §8 telephone assertion, recorded here on 24 August 2026 under
DECISION-10 D42, has been removed. **D42-R1 reverses D42** and restores the check as an
active assertion over every deployable file. This report is regenerated by
`scripts/57-seo-spec-gate.py` on the next passing run; until the owner supplies an NSW 02
number the build fails closed and there is no output to assert against.
