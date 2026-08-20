# Stage 38 — trading-name rename plan: CoreX + E&T Co → Structure Co

Date: 19 August 2026 (Australia/Sydney).
Authority: `DECISION-08-trading-name-brand-nap.md` §D35, superseding `DECISION-06-resolvable-items.md` §D30.

**THIS PLAN IS NOT EXECUTED.** Nothing was renamed. No artifact was mutated by this report. The seven
immutable hashes are re-verified in §9 and all match.

---

## 0. The correction that has to come first

`build/21-spec-ledger.json` → `site_mark.trading_name_conflict.corex_occurrences_in_main_wxr`
records **345**. That figure is wrong and it is the figure D30 and `CONTEXT.md` both quote.

```text
  recorded            345
  actual              466   "CoreX", any case, camden-concreting-import.xml
  of which the full phrase "CoreX Concreters Camden"          71
```

No corpus in the repo yields 345. The nearest is `build/stage9-all-pages.json` at 352, which is a
build intermediate and not the artifact D30 was describing. The 345 is not reproducible and is
corrected in the ledger by this report. **Every count below is recomputed from the artifacts, and
attribution is asserted to be complete — the classifier aborts if any occurrence is unattributed
rather than reporting a remainder.**

---

## 1. Count per artifact

Occurrences of all name forms — `CoreX`, `E&T Co`, bare `E&T`, and the filename forms `e_t_co`,
`e-t-co`, `eandtco`, `eamptco`.

| Artifact class | Files | Occurrences | Rename? |
|---|---:|---:|---|
| Reports / audit trails | 52 | 4,026 | **No** — provenance |
| Build artifacts (mutable) | 13 | 1,199 | Partly — see §4 |
| **Immutable** (6 of the 7 baseline files) | 6 | 708 | **No** — post-import only |
| Source inputs | 4 | 151 | No |
| `lib/` + root docs | 9 | 65 | Partly — see §4 |
| Governing / state docs | 6 | 21 | Only `CONTEXT.md` |
| `scripts/` + `tests/` | 3 | 5 | No — they name the source WXR file |
| `data/` | 1 | 2 | **Yes** — done, §6 |
| **Total** | **94** | **6,177** | |

By name form:

```text
  CoreX             3,336        E&T Co              476        E&T (bare)      306
  e-t-co (file)       838        e_t_co (file)       811        eamptco (file)  312
  eandtco (file)       98        Structure Co          0  (before this session)
```

### The number that matters

**6,177 is not the size of the job.** Following the D30 §2 method — which was correct and is
retained — the great majority are provenance records doing their job. A rename map is *supposed* to
record the original filename; a sweep report is *supposed* to quote the term it swept for.

```text
  occurrences that reach a rendered page or a search result      366
  occurrences in provenance, audit trails and this build's
    own reporting, which MUST NOT be renamed                   5,811
```

---

## 2. `camden-concreting-import.xml` — the immutable artifact

466 occurrences of `CoreX`, fully attributed (sum equals total, no remainder):

| Field | Count | Reaches a reader? |
|---|---:|---|
| `postmeta _elementor_data` | 235 | partly — see breakdown |
| `postmeta rank_math_title` | 107 | **yes** — the search result title |
| `postmeta _wp_attachment_metadata` | 40 | no — generated size filenames |
| `element <title>` | 12 | **yes** — the item title |
| `element <guid>` | 10 | no |
| `element <link>` | 10 | no |
| `element <wp:post_name>` | 10 | no — slug |
| `element <wp:attachment_url>` | 10 | no |
| `postmeta _wp_attached_file` | 10 | no — filename |
| `postmeta _wp_attachment_image_alt` | 10 | **yes** — alt text |
| `postmeta rank_math_description` | 7 | **yes** — meta description |
| `channel header` (site title) | 2 | **yes** |
| `postmeta rank_math_breadcrumb_title` | 2 | **yes** |
| `postmeta rank_math_focus_keyword` | 1 | no |
| **Total** | **466** | |

Inside `_elementor_data`, by widget key:

```text
  editor                132   rendered body copy
  text                   48   rendered body copy
  alt                    24   alt attributes
  url                    10   NOT rendered — image URLs
  value                   6   rendered
  title                   6   rendered
  item_title              6   rendered
  testimonial_content     3   rendered
  ----------------------------
  rendered copy         201
  alt                    24
  non-rendered           10
```

**Reader-visible total in the main WXR: 366. Non-visible: 100.**

Distribution:

```text
  by post_type      page 354, attachment 110
  pages whose rendered Elementor copy carries CoreX     73 of 156  (21 publish, 52 draft)
  pages carrying CoreX on ANY reader-visible surface   111 of 156
  heaviest pages    /about/ 19, /contact/ 18, / 11, /gallery/ 9, /quote/ 8
```

### Also in the immutable artifact — the E&T kit values, still unfixed

D30's two page-reaching hits are unchanged and are now **three** targets:

```text
  elementor_library "Default Kit" > _elementor_page_settings
    site_name          "E&T Co Concreters Camden"        → "Structure Co Concreters Camden"
    site_description   "Camden based Concrete Company Site"
                       → NOT a rename. A location claim that is unsupportable from Pakenham
                         (D32). It must be rewritten or removed, not renamed.
  channel <title>      "CoreX Concreters Camden"         → "Structure Co Concreters Camden"
```

**None of the 466 + 3 can be edited in the file.** The artifact is immutable and its hash is a
launch gate. All of it is post-import work — §3.

---

## 3. Post-import steps, where the immutable WXR is involved

These run against the **database after import**, in this order, each with a rollback point. They are
additions to `reports/post-import-tasks.md` and to the `reports/29-staging-plan.md` sequence.

```text
STEP A — order matters, longest string first
  Run the phrase before the bare token, or "CoreX Concreters Camden" becomes
  "Structure Co Concreters Camden Concreters Camden".

  1. wp search-replace 'CoreX Concreters Camden' 'Structure Co Concreters Camden' \
       --all-tables --precise --dry-run
  2. wp search-replace 'CoreX' 'Structure Co' --all-tables --precise --dry-run
  3. wp search-replace 'E&T Co Concreters Camden' 'Structure Co Concreters Camden' \
       --all-tables --precise --dry-run

  --precise is REQUIRED. _elementor_data is a PHP-serialised / JSON blob in wp_postmeta;
  a byte-length-unaware replace corrupts it, and "CoreX" (5 chars) -> "Structure Co"
  (12 chars) changes every containing string's length.

  Review each dry-run count against this table before running without --dry-run:
     CoreX Concreters Camden      expect  71
     CoreX (remaining)            expect 395
     E&T Co Concreters Camden     expect   1  (kit site_name)

STEP B — filenames and slugs are NOT renamed
  The 100 non-visible occurrences are attachment filenames, GUIDs, slugs and URLs.
  Renaming them breaks every _elementor_data image reference and every uploads path,
  for zero reader benefit. corex-concreters-camden-logo-306.png stays that filename.
  DECIDE AND RECORD: this is a deliberate acceptance, not an oversight. The filenames
  carry a superseded trading name and will be visible in image URLs.

STEP C — the kit values (D30.1, unchanged method, new target)
  Elementor > Site Settings > site_name       -> "Structure Co Concreters Camden"
  Settings > General > Site Title             -> "Structure Co Concreters Camden"
  Settings > General > Tagline / site_description
      -> REWRITE, do not rename. "Camden based Concrete Company Site" is a location
         claim. Fulfilment is Pakenham (D32). Removing it entirely is the safe default.

STEP D — Rank Math
  114 rank_math_* occurrences (title 107, description 7, breadcrumb 2) are covered by
  STEP A, but Rank Math caches. Re-save or re-run the sitemap/meta regeneration and
  re-verify 0 hits.

STEP E — Elementor cache, after A-D
  DELETE FROM wp_postmeta WHERE meta_key = '_elementor_element_cache';
  Elementor > Tools > Regenerate CSS & Data, then Sync Library.

STEP F — verification, fail-closed
  Zero occurrences of CoreX, E&T, E&T Co, "Camden based" in: post_title, post_content,
  postmeta, options (blogname, blogdescription), theme_mods, term names, menu labels,
  and every rendered page fetched over HTTP.
  Filenames and GUIDs are EXCLUDED from this assertion by STEP B and that exclusion is
  named explicitly in the gate, not left implicit.
```

---

## 4. Artifacts that are renamed before import

| Artifact | Hits | Action |
|---|---:|---|
| `data/verified-facts.yml` | 2 | **Done this session** — `trading_name` now Structure Co, `verified: false`. §6 |
| `build/21-spec-ledger.json` | 8 | **Done this session** — supersession recorded with citation. §7 |
| `camden-privacy-import.xml` | **0** | Nothing to do. It names no entity — that is its 11 blocking markers doing their job. |
| `build/global-replace.json` | 2 | **Owner decision.** It is the find/replace *rule*. Naming the old term is how replacement works. Recommend: update the rule's target to Structure Co; keep the old term as the search key. |
| `lib/site_builder.py`, `lib/stage9.py`, `lib/stage8.py`, `lib/stage3_gate.py`, `lib/stage18_readiness.py` | 45 | **Owner decision.** These are the generators. If the corpus is ever regenerated they emit CoreX again. Recommend updating the string constants; note this does **not** change any built artifact. |
| `build/stage4–stage9-*.json` | 1,189 | **Do not rename.** Build intermediates, superseded by the WXR. Renaming them creates a second, divergent record of what was built. |
| `camden-site-structure-and-silo.md`, `oran-park-gold-standard.md`, `codex-clone-prompt.md` | 19 | **Do not rename.** They name the *source* site, correctly. |

---

## 5. What must NOT be renamed, and why

5,811 of the 6,177 occurrences. Renaming them destroys the audit trail that caught the problem.

```text
  reports/36-source-name-sweep.csv        2,506   the sweep record itself
  reports/23-evidence-register.csv          394   evidence register
  reports/18/23-page-readiness*.csv         542   readiness matrices
  reports/placeholders.md                   145   marker register
  build/stage8-image-map.json                79   IMMUTABLE, and the provenance record
  reports/08-image-rename-map.csv            19   IMMUTABLE, old -> new by definition
  eamptcoconcretersmelbourne_*.xml          138   IMMUTABLE source export
  archive/                                    2   provenance only
  every other report                        ...   this build's own reporting
```

D30 §2 established this principle for E&T and it holds unchanged for CoreX: **a provenance record
naming a superseded value is not a defect, it is the mechanism.**

---

## 6. `data/verified-facts.yml` — applied

| Field | Before | After | verified |
|---|---|---|---|
| `trading_name` | CoreX Concreters Camden | **Structure Co Concreters Camden** | `false` |
| `email` | *(empty)* | **info@concreterscamden.com.au** | `false` |
| `street_address` | *(empty)* | **15 Murray Street, Camden NSW 2570** | `false` |
| `suburb` | *(empty)* | Camden | `false` |
| `postcode` | *(empty)* | 2570 | `false` |
| `is_staffed` | `null` | **`unknown`** | `false` |
| `phone` | 03 4517 6915 | unchanged, still flagged | `false` |

Per D37 the address stays unverified until the owner attests it. **The email is also recorded
`verified: false`** — the owner supplied the value but did not attest it, and under the file's own
rule a value without `verified: true` is treated as absent. If the intent was that the mailbox exists
and is monitored, say so and it flips with a `sighted_date`.

`is_staffed: unknown` is recorded as the string `unknown`, distinct from the previous `null`. `null`
meant "not yet asked"; `unknown` means "asked, answer pending". The schema builder treats both as
unverified and neither emits `LocalBusiness`.

**No `LocalBusiness` is emitted.** D2's ladder resolves to **outcome 3** on every page — `Service`
omits `provider`. An address without a verified staffed status does not define a `LocalBusiness`;
§4.30.2 is explicit and this input does not satisfy it.

---

## 7. D30 as updated

D30's method survives intact. Its target and scope change.

```text
  WAS  correct the Elementor kit's "E&T Co Concreters Camden" to "CoreX Concreters Camden"
       at import. 2 values reach a page. 781 of 783 hits are provenance.

  NOW  correct BOTH "E&T Co Concreters Camden" AND "CoreX Concreters Camden" to
       "Structure Co Concreters Camden" at import. 366 occurrences reach a reader
       across 111 of 156 pages. 5,811 of 6,177 hits are provenance.

  UNCHANGED
       - corrected at import, never in the immutable artifact
       - preflight gate 13 asserts zero source-name occurrences; its pattern must now
         also cover "CoreX"
       - the sweep principle: provenance records are not defects
       - D30.4: the correction replaces an incorrect claim with an UNVERIFIED one.
         It is an improvement, not a resolution. The identity blocker stands.
```

Recorded in `build/21-spec-ledger.json` under `source_name_correction`, citing `DEC08-D35`. The
decision documents themselves are read-only and were not edited.

### Preflight gate 13 needs widening

Gate 13 currently asserts zero `E&T` occurrences. It must also assert zero `CoreX`. **It will fail
until the post-import steps run, and that is correct.** It is not widened and then satisfied in the
same breath — the gate is written to fail now.

---

## 8. The identity blocker list — unchanged in substance

Structure Co has no verified legal entity, no ABN, no NSW Fair Trading licence and no insurance
evidence. The rename swaps one unverified trading name for another.

| # | Blocker | Before | After this session |
|---|---|---|---|
| 1 | Legal entity / legal name | unverified | **unverified** |
| 2 | ABN | unverified | **unverified** |
| 3 | NSW Fair Trading licence | unverified | **unverified** |
| 4 | Public liability insurance | unverified | **unverified** |
| 5 | Workers compensation insurance | unverified | **unverified** |
| 6 | Street address | absent | **recorded, unverified** |
| 7 | Staffed status | unknown | **explicitly `unknown`, unverified** |
| 8 | Phone ownership + routing | unverified, VIC area code | **unchanged, still flagged** |
| 9 | Email | absent | **recorded, unverified** |
| 10 | Trading name | two conflicting, both unverified | **one name, still unverified** |

**Net: 0 blockers cleared.** Two fields moved from absent to recorded-but-unverified, and the name
conflict collapsed from three names to one. `verified-facts.yml` still reports **0 of 20+ fields
`verified: true`**, so Phase C stays BLOCKED and the schema builder still emits no provider.

The one real gain: the site will stop declaring **another business's** trading name. That is a
footprint fix, and it is worth having on its own terms.

---

## 9. Immutable hash table

```text
  camden-concreting-import.xml                          MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   MATCH
  build/stage9-page-manifest.json                       MATCH
  build/stage8-image-map.json                           MATCH
  reports/08-image-rename-map.csv                       MATCH
  CODEX-BUILD-2.1.md                                    MATCH
  archive/governing/CODEX-BUILD-2.md                    MATCH

  7 of 7 MATCH, recomputed after every write in this session.
```

---

## 10. Owner decisions this plan raises

1. **§3 STEP B** — confirm that attachment filenames and slugs keep the `corex-` prefix. They will be
   visible in image URLs. The alternative breaks 1,085 Elementor image references.
2. **§4** — update the `lib/` generator string constants, or leave them? They affect regeneration only.
3. **§4** — `build/global-replace.json`: update the replacement target?
4. **§6** — is `info@concreterscamden.com.au` attested (mailbox exists, monitored)? If so it flips to
   `verified: true` with a `sighted_date`.
5. **§2** — the tagline "Camden based Concrete Company Site" needs a rewrite, not a rename. Removing
   it is the safe default; confirm.
