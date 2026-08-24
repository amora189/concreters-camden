# Report 57 — spec sections 6.5 and 8, run against the built output

Run: 25 August 2026 (Australia/Sydney). Command: `scripts/57-seo-spec-gate.py`.
Target: `build/cloudflare-pages/` (78 pages + 404). Authority: the supplied titles /
breadcrumbs / near-me spec as amended by DECISION-10 D42-R2, D43-R1, D44 and D45.

States what was verified against artifacts on disk. `BLOCKED` and `RETIRED` rows name
their authority; no assertion was narrowed or deleted to make it pass (CLAUDE.md §3
hard stop 7).

| # | Assertion | Result | Detail |
|---|---|---|---|
| 1 | no 'enquir' in any title or h1 | **PASS** | titles and H1s |
| 2 | no 'near me' in any title, h1 or URL | **PASS** |  |
| 3 | every title <= 60 characters | **PASS** |  |
| 4 | every title unique sitewide | **PASS** |  |
| 5 | no title promises a content module the page does not carry | **PASS** |  |
| 6 | spec suburb titles and descriptions resolved from suburbs.json, no template fallback | **PASS** |  |
| 7 | authored meta descriptions are 150-158 characters | **PASS** |  |
| 8 | suburbs.json meta descriptions are used verbatim, length rule waived (C4) | **PASS** | 15 descriptions, 126-182 chars as authored in suburbs.json |
| 9 | fallback-tier titles follow the documented pattern | **PASS** |  |
| 10 | no title or h1 contains enquir / near me / best / cheap / #1 | **PASS** |  |
| 11 | every meta description unique sitewide | **PASS** |  |
| 12 | no fallback-tier page carries a fabricated suburb specific | **PASS** |  |
| 13 | no postalCode emitted that is absent from camden-verified-postcodes.json | **PASS** |  |
| 14 | every emitted postalCode matches camden-verified-postcodes.json | **PASS** |  |
| 15 | areaServed omitted rather than guessed where the file has no entry | **PASS** | 5 pages: cecil-park, chipping-norton, glen-alpine, moorebank, wattle-grove |
| 16 | no empty or placeholder FAQ entry | **PASS** |  |
| 17 | /areas/ exists and is indexable | **PASS** |  |
| 18 | /services/ exists and is indexable | **PASS** |  |
| 19 | /concreters-camden/ 301s to / | **PASS** |  |
| 20 | every old flat service URL 301s to /services/{slug}/ | **PASS** |  |
| 21 | no redirect chains and no loops | **PASS** | chains=[] loops=[] |
| 22 | no flat service directory still serves a page | **PASS** |  |
| 23 | no '#' in any BreadcrumbList item | **PASS** |  |
| 24 | no BreadcrumbList exceeds 3 items | **PASS** |  |
| 25 | terminal ListItem carries no item | **PASS** |  |
| 26 | visible breadcrumb labels match JSON-LD names | **PASS** |  |
| 27 | terminal crumb matches the page h1 subject | **PASS** |  |
| 28 | homepage carries no breadcrumb | **PASS** |  |
| 29 | every crumb URL resolves to a built page | **PASS** |  |
| 30 | every suburb page is index,follow (DECISION-10 D45) | **PASS** | 60 suburb pages indexed; noindex on [] |
| 31 | D45 re-armable: the D44 tier gate is retained, not deleted | **PASS** | INDEX_ALL_SUBURBS=False restores Tier 1 only (6 pages) |
| 32 | sitemap contains zero noindex URLs | **PASS** |  |
| 33 | every indexable page is in the sitemap | **PASS** |  |
| 34 | sitemap matches the indexable set exactly | **PASS** | 78 URLs in sitemap, 78 indexable pages |
| 35 | no LocalBusiness or GeneralContractor node outside / and /contact/ | **PASS** |  |
| 36 | no AggregateRating or Review markup anywhere | **PASS** |  |
| 37 | every FAQPage Q&A string appears verbatim in the rendered HTML | **PASS** |  |
| 38 | every in-scope suburb page carries a Service node with areaServed | **PASS** |  |
| 39 | areaServed postalCode comes from suburbs.json | **PASS** |  |
| 40 | no dangling #organization reference | **PASS** |  |
| 41 | spec section 5.1 near-me H2 on every in-scope suburb page | **PASS** |  |
| 42 | near-me H2 appears exactly once per page | **PASS** |  |
| 43 | spec section 5.2 near-me FAQ on every in-scope suburb page | **PASS** |  |
| 44 | near-me FAQ answers are 40-60 words | **PASS** |  |
| 45 | spec section 5.4 lists 3-5 services per suburb | **PASS** |  |
| 46 | spec section 5.4 paragraphs are 40-70 words | **PASS** |  |
| 47 | spec section 5.4 paragraphs are unique sitewide | **PASS** | 0 duplicates |
| 48 | spec section 5.3 /areas/ anchor text is varied | **PASS** | 36/60 exact-match |
| 49 | every page is reachable within 2 clicks of / | **PASS** |  |
| 50 | every internal link resolves to a file in the build | **PASS** |  |
| 51 | no internal link points at a redirect source | **PASS** |  |
| 52 | every internal fragment link has a matching id | **PASS** |  |
| 53 | no link points at an unbuilt service page | **PASS** |  |
| 54 | every redirect target resolves to a file in the build | **PASS** |  |
| 55 | every sitemap URL resolves to a file in the build | **PASS** |  |
| 56 | external links present (not fetched) | **PASS** | https://concreterscamden.com.au/; https://concreterscamden.com.au/about/; https://concreterscamden.com.au/areas/; https://concreterscamden.com.au/concreters-appin/; https://concreterscamden.com.au/concreters-austral/; https://concretersc… |
| 57 | no [[...]] or {TOKEN} placeholder reaches the output | **PASS** |  |
| 58 | every referenced JSON-LD @id is defined | **PASS** |  |
| 59 | every phone string in output matches verified-facts.yml exactly | **PASS** |  |
| 60 | area_code_override recorded and dated (D42-R2) | **PASS** | reviewed 2026-08-25 |
| 61 | telephone resolves from verified-facts.yml only, zero hardcodes | **PASS** | contact.phone_display / contact.phone_e164 are the single source |
| 62 | no telephone property in any schema node | **PASS** |  |
| 63 | sitewide Organization node (spec section 7.2) | **BLOCKED** | DECISION-08 D35 clause 4 does not authorise an Organization node; legal_entity.legal_name is unverified. Service + WebPage + BreadcrumbList + FAQPage ship instead. No @id is referenced, so nothing dangles. |
| 64 | spec section 5.2 price FAQ and '{X} business days' | **BLOCKED** | pricing.per_m2_ranges verified:false, blocks_pages:53. No response-time commitment recorded. Both withheld with an inline marker in every page. |
| 65 | Tier 2 and Tier 3 noindex cannot be lifted | **RETIRED** | DECISION-10 D45. The owner instructed that every built page ships indexed without per-m2 pricing or original photography, superseding the spec section 4 gate condition. pricing.per_m2_ranges and photography.real_camden_photographs remain… |
| 66 | spec section 3 /services/stencilled-and-stamped-concrete/ | **BLOCKED** | Resolved by removal, not by padding: no source page exists in build/46-active-main-import.xml, nothing in the build links to it, and the services hub records it in an HTML comment rather than an anchor. 10 of the spec's 11 service pages … |
| 67 | Bringelly council resolved against evidence | **PASS** | resolved as split-locality per build/53-council-suburb-map.json: Camden Council and Liverpool City Council, lot-level check required. The page names no single council, per its public_wording_rule. The spec's 'resolve to one council' is u… |
| 68 | fallback-tier suburb pages carry no suburbs.json record | **BLOCKED** | 45 pages ship indexed under D45 on the documented fallback tier: pattern title, generic-but-true meta, H1, breadcrumbs and a Service node. They carry no near-me FAQ and no section 5.4 block, because both need per-suburb job data that doe… |

**63 pass, 0 fail, 4 blocked, 1 retired**

## Hash table — CLAUDE.md §1 immutable files

| File | SHA-256 | Gate 21 |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |

**6/6 MATCH.** No immutable artifact, instruction document or `archive/` file was modified.

## Postcode resolution

Source: `data/camden-verified-postcodes.json` (85 verified suburbs, 7 estate-name parents,
0 ambiguous). 55 of 60 suburb pages resolve directly. Five have no entry, so `areaServed`
is omitted entirely rather than guessed: **Cecil Park, Chipping Norton, Glen Alpine,
Moorebank, Wattle Grove.** Elderslie resolves to **2570**, disambiguated in the file from
2335 in the Hunter Valley; the emitted value matches and the assertion holds it there.
No page carries a postcode that disagrees with the file.

## Fallback tier

45 suburb pages have no `suburbs.json` record and ship on the documented D45 fallback
tier. Full list with the generated title and meta: `reports/58-fallback-tier.tsv`.
