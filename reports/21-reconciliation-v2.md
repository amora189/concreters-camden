# Stage 21 — specification reconciliation v2.1

Audit date: 18 August 2026 (Australia/Sydney)

## Governing-instruction status

`CODEX-BUILD-2.1.md` is the sole governing instruction for this work block. The superseded `CODEX-BUILD-2.md` was semantically restored and moved to `archive/governing/CODEX-BUILD-2.md`; no standalone Amendment A, B or C file exists in the workspace. Exact byte restoration of the archived file is unprovable because no pre-edit checksum exists and the observed restored length is one byte shorter than the earlier observed length. The complete restoration record is in `reports/21-governing-doc-diff.md`.

## Input assertion

Every file required by `CODEX-BUILD-2.1.md` §1 exists, is non-empty and parses in its native format. Markdown files decode strictly as UTF-8, JSON files load successfully, and both WXR files parse as XML.

| Input | Parse result |
|---|---|
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | PASS — well-formed XML |
| `camden-concreting-import.xml` | PASS — well-formed XML |
| `camden-site-structure-and-silo.md` | PASS — strict UTF-8 Markdown |
| `expansion-300-pages.md` | PASS — strict UTF-8 Markdown |
| `intersection-differentiators.json` | PASS — JSON, 35 allowed intersections |
| `camden-concreting-seo-spec.md` | PASS — strict UTF-8 Markdown |
| `suburbs.json` | PASS — JSON |
| `suburbs-expanded.json` | PASS — JSON, 60 suburb records |
| `oran-park-gold-standard.md` | PASS — strict UTF-8 Markdown |
| `codex-clone-prompt.md` | PASS — strict UTF-8 Markdown |

Neither WXR was modified.

## Citation remap

All 16 stable ledger citation definitions that formerly resolved to the superseded build file or Amendment B now resolve to the equivalent `CODEX-BUILD-2.1.md` clause. Those definitions cover 75 `source_refs`. Undefined references: zero. Spec values that lost a citation: zero. The complete old-to-new map is `reports/21-citation-remap.md`.

## Resolved class table

| Page class | Combined spec | Main manifest | Main WXR | Import state across planned artifacts | Uniqueness rule | Pre-Stage-27 wave state |
|---|---:|---:|---:|---|---|---|
| Home | 1 | 1 | 1 | 1 publish | Global 5-gram and pair caps; no sourced word-percentage floor | Wave 1 candidate |
| Utility | 4 | 4 | 4 | 4 publish; Gallery remains `noindex,follow` | Global caps; no sourced word-percentage floor | Wave 1 candidates, evidence-gated |
| Services | 10 | 10 | 10 | 10 publish | Global caps; no sourced word-percentage floor | Wave 1 candidates |
| Suburbs | 60 | 60 | 60 | 6 publish / 54 draft; all 60 `noindex,follow` | ≥60% unique body words; ≤40% pair overlap; first 80 words; 8/11 built modules unique | Six Wave 1 candidates, nine later researched candidates, 45 held without a wave |
| Intersections | 35 | 35 | 35 | 35 draft + `noindex,follow` | ≥50%; ≤40% pair overlap; first 80 words; differentiator mandatory | Wave 5 candidates |
| Guide hub | 1 | 1 | 1 | 1 draft + `noindex,follow` | Global caps; no sourced word-percentage floor | Wave 2 only with first approved guides |
| Guides | 35 | 35 | 35 | 35 draft + `noindex,follow` | ≥85%; ≤40% pair overlap | Legacy 15/20 Wave 2/4 split, pending recomputation |
| Cost/comparison | 11 | 10 | 10 | 10 main drafts plus one planned supplementary draft; all noindex | Global caps; no sourced word-percentage floor; calculator threshold awaits approval | Wave 4 default; calculator promotion is evidence- and owner-gated |
| **Total** | **157** | **156** | **156** | **21 publish / 136 draft combined; 21 publish / 135 draft in main WXR** | Any 5-gram on more than two pages fails | Final plan pending Stage 27 |

The detailed value-by-value citations are in `build/21-spec-ledger.json`.

## Module crosswalk and noindex translation

The full content-derived crosswalk is in `reports/21-module-crosswalk.md`. Its decisive mappings are:

| SEO §5 responsibility | Built 11-module location |
|---|---|
| SEO module 6 — typical jobs and real price band | Built modules 3 and 5, plus the price portion of built module 11 |
| SEO module 7 — recent job and photos | Built module 8 |

The noindex rule therefore checks built modules **3/5/11** for unresolved job or price evidence and built module **8** for verified recent-job evidence and real photographs. The page also remains draft/noindex when its `unique_local_variable` is missing or unresearched. Mapping by built positions 6 and 7 would be wrong.

## Conflicts explicitly listed in `CODEX-BUILD-2.1.md` §2

| Listed conflict | Resolution applied |
|---|---|
| 300 pages / 180 intersections | Dead figures; only the 35 allow-listed intersections exist. |
| Intersection absent from `intersection-differentiators.json` | Does not exist and cannot be invented. |
| Total page count | 157 combined: 156 immutable main pages plus one supplementary calculator. |
| Astro versus WordPress | WordPress wins; only SEO-spec §§5, 6, 7 and 10 remain in scope. |
| 11, 7 or 10 services | Ten service pages. |
| Ten versus eleven suburb modules | Built eleven-module structure wins; semantic crosswalk applied. |
| Six versus 35 guides | 35 guides plus one hub. |
| Conflicting uniqueness gates | Stricter sourced rule at each point: 5-gram on >2 pages fails, 60%/50%/85% class floors, ≤40% pair overlap. |
| 300-page waves | Recompute against 157 in Stage 27. |
| Ten versus eleven cost/comparison pages | Eleven combined; calculator is supplementary. |
| Camden suburb URLs | Never build either forbidden Camden suburb URL; homepage owns the query. |

## IMPORTANT — conflicts not listed in §2

Eighteen additional conflicts, propagation errors or underspecified contracts were found. One is unresolved and blocks the prescribed stage order.

### 1. Three utilities versus four utilities

`CODEX-BUILD.md` names Contact, Quote and About, while the structure/expansion documents and artifact include Gallery. **Resolved:** four utilities; Gallery remains evidence- and photography-gated.

### 2. Old guide publish status versus the expansion boundary

The earlier build plan describes guides as published in the import; the expansion wave rule and actual WXR hold them as drafts. **Resolved:** hub and all 35 guides remain draft, and the hub never publishes alone.

### 3. Fifteen-suburb inventory versus the 60-suburb expansion

Earlier architecture describes 15 built suburbs; the expansion and WXR contain 60. **Resolved:** 60 artifacts, of which only 15 have researched deep content and 45 are held research shells.

### 4. “Do not write” versus retaining research shells

Expansion §8 says a failing page is not written, while expansion §10 and current standing rule 2 require draft/noindex shells. **Resolved:** standing rule 2 wins; shells remain non-live and fail readiness.

### 5. Legacy waves assigned to unresearched suburbs

`suburbs-expanded.json` gives legacy waves to all 60 suburbs, including 45 `REQUIRED-RESEARCH` records; current Stage 27 forbids those 45 from every wave. **Resolved:** the 45 have no operative wave until research passes.

### 6. “All seven services” in link Rule A after the count became ten

The structure document's fixed service inventory is stale. **Resolved:** “all services” means all ten resolved service pages for future menu/link planning.

### 7. Vary module order versus preserve Elementor layout

The structure document proposes module reordering, while the clone contract and standing rule 6 prohibit it. **Resolved:** layout preservation wins; no module order changes.

### 8. Original-only images versus controlled reuse

The SEO specification asks for original per-page imagery, while expansion §9 and Stage 24 audit reused assets. **Resolved:** controlled generic reuse is permitted, but no source-site image may occupy a `REAL_PHOTO_PENDING` slot or be represented as Camden work.

### 9. Media-first upload placement versus observed WordPress filename suffixing

The structure document says place media in final uploads before WXR import; Stage 15 proved colliding names may be suffixed. **Resolved:** later tested evidence wins; use the future local-only importer and audit exact filenames.

### 10. Manual schema rebuild versus deterministic fail-closed builder

The structure document says re-enter schema manually; Stage 30 requires a builder. **Resolved:** the more specific current Stage 30 instruction wins.

### 11. Potential dangling `#localbusiness` reference

SEO §7 says omit `LocalBusiness` without a verified staffed address, while suburb `Service` examples reference it and §7.6 forbids undefined `@id` values. **Resolved:** dependent references/nodes are omitted and logged whenever `#localbusiness` cannot be emitted.

### 12. Incomplete normative module contracts

Home, Utility, Guide hub, generic Guide and Cost/comparison do not all have complete normative module sequences in the source documents. **Resolved:** the ledger labels artifact-observed shapes as observations, not silently promoted rules; structural mutation remains prohibited.

### 13. Stage 25 arithmetic says 26 pages where the listed classes total 27

The listed unthresholded classes are 10 services + 11 cost/comparison + 1 guide hub + 1 homepage + 4 utilities = **27**, not 26. **Resolved:** explicit class counts and the 157 total win; Stage 25 must report 27 such pages.

### 14. Stage order requires a supplementary artifact before Stage 31 permits it to exist

- Stage 23 requires a 157th readiness row before the calculator has an approved slug, title or allocated ID.
- Stage 25 unconditionally requires measurement of all 157 pages before the calculator body exists.
- Stage 28 must audit collisions and unresolved image references across both XML files and may skip no gate.
- Stage 31, later in the mandatory sequence, requires inventory, a printed owner-approval pause, then construction of `camden-calculator-import.xml`.

**UNRESOLVED — HARD BLOCKER:** these requirements cannot all be met in stage order without either constructing the calculator before its approval gate or narrowing/skipping the 157-page assertions, both expressly forbidden. Owner direction on reordering or splitting Stage 31 is required.

### 15. Global 40% pair cap versus “no threshold” for five classes

Stage 25 says no sourced thresholds exist for Home, Utility, Service, Guide hub and Cost/comparison, while §2 explicitly sources a ≤40% within-class pair cap globally. **Resolved:** the global pair cap is already sourced and enforced; only a class-specific unique-body-word percentage remains `AWAITING APPROVAL — not enforced`.

### 16. Zero current index-ready pages versus Wave 1 effective indexable 14

Standing §3.2 keeps current readiness at 0; Stage 27 specifies a future effective Wave 1 count of 14. **Resolved:** Stage 27 is a conditional release plan, not a current state mutation. No page becomes index-ready in this work block.

### 17. Stage 23 says join the original readiness CSV on page ID, but it has no page-ID column

`reports/18-page-readiness.csv` begins with URL and contains no page ID. **Resolved:** derive the page ID by exact URL through the manifest, add a Page ID column in the v2 superset, and fail on any missing or non-unique URL match.

### 18. Stage 31 is numbered §4.11 after Stage 30

The heading is `§4.11`, not sequential `§4.31`. **Resolved for provenance only:** citations use the exact supplied identifier `§4.11`; no instruction file is edited to renumber it.

## Three-way reconciliation

The ledger was compared with `build/stage9-page-manifest.json` and a direct parse of every `wp:post_type=page` item in `camden-concreting-import.xml`.

| Comparison | Result | Divergence |
|---|---|---|
| Spec versus manifest | 157 versus 156 | Exactly one planned cost/comparison calculator and one planned draft/noindex status; expected under §4.11.1 and §4.11.7 |
| Spec versus main XML | 157 versus 156 | Same single planned supplementary calculator; expected |
| Manifest versus main XML | **156 versus 156; exact match** | **None:** zero missing/extra IDs and zero mismatches across post ID, slug, parent ID, status and served path |

Per-class manifest/XML counts are 1 home, 4 utility, 10 service, 60 suburb, 35 intersection, 1 guide hub, 35 guide and 10 cost/comparison. Manifest/XML import statuses are 21 publish and 135 draft. Every non-calculator class matches the ledger exactly.

`CONTEXT.md` independently records 1/4/10/60/1/35/35/11 = 157, the 156+1 artifact split and 0 of 157 index-ready. No differing class count was found.

## Encoding integrity

`reports/21-encoding-audit.md` records the full 18-script review. The only lossy decoder found, `errors="replace"` in the Stage 20 crawler, now fails strictly. The canary containing an em dash, en dash, `²` and non-breaking space survived an exact UTF-8 read-write-compare cycle. The two restored exact assertions pass:

- `## 4.25 — Stage 25: uniqueness enforcement`
- `PASS — 157 combined (156 main + 1 planned supplementary)`

## Mandatory Gate 21 hash table

| File | Bytes | SHA-256 | Comparison status |
|---|---:|---|---|
| `camden-concreting-import.xml` | 10,169,943 | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | Matches the previously recorded immutable hash |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | 2,797,640 | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | Matches the previously recorded immutable hash |
| `build/stage9-page-manifest.json` | 30,742 | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | Gate 21 baseline established; direct content reconciliation passes |
| `build/stage8-image-map.json` | 48,862 | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | Gate 21 baseline established; parses as 83 records |
| `reports/08-image-rename-map.csv` | 40,516 | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | Gate 21 baseline established |
| `CODEX-BUILD-2.1.md` | 32,753 | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | Gate 21 immutable baseline established |

No immutable-file hash change was detected where a prior hash exists. The other four hashes become the mandatory comparison baseline for every later gate.

## `CONTEXT.md` update and diff

`CONTEXT.md` now records this re-opened Gate 21's verified checks, the unresolved stage-order blocker, unchanged owner-supplied media/Astra blockers, unchanged launch NO-GO and unchanged 0-of-157 readiness. No blocker was removed. The explicit before/after record is `reports/21-context-diff.md`.

## Gate 21 result

| Acceptance check | Result |
|---|---|
| Required inputs present and parsed strictly | PASS |
| Ledger class total | PASS — 157 combined (156 main + 1 planned supplementary) |
| Ledger values retain source citations | PASS |
| Citation remap | PASS — 75 affected references, zero lost |
| Module crosswalk and translated noindex gate | PASS |
| Explicit §2 conflicts reconciled | PASS |
| Unlisted conflicts printed | PASS — 18 findings |
| Spec versus manifest/XML known asymmetry | PASS — exactly one planned supplementary page |
| Manifest versus XML | PASS — zero divergences across all 156 pages |
| Encoding canary and restored assertions | PASS |
| Governing-document restoration | PASS with documented byte-level limitation; semantic edits reversed and file archived |
| Mandatory hash table | PASS; baselines recorded |
| Stage-order consistency | **FAIL — supplementary artifact is required before its authorised construction stage** |

**GATE 21: BLOCKED — owner direction is required before Stage 22.**
