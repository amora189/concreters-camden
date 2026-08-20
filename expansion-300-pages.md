# 300-Page Expansion Architecture

**Supersedes:** the 32-page plan in `camden-site-structure-and-silo.md` §8. Everything else in that file (link rules, clone procedure, footprint rules) still applies.

---

## 1. The honest math

You cannot get to 300 defensible pages by multiplying 15 suburbs by 7 services. You get there by expanding geography first, because a new suburb is a new real place — different council, different soil, different estates, different job mix — while a new service in the same suburb is usually the same page with a different noun in it.

| Page class | Count | Why each page is genuinely distinct |
|---|---|---|
| Home | 1 | — |
| Utility (about, contact, quote, gallery) | 4 | — |
| Service pages | 10 | Different service, different spec, different price driver |
| **Suburb pages** | **60** | Different council, soil, estates, housing era, job mix, failure mode |
| **Suburb × service pages** | **180** | Only where a real differentiator exists — see §4 |
| Guides | 35 | Distinct informational query each |
| Cost & comparison pages | 10 | Distinct commercial-investigation query each |
| **Total** | **300** | |

The 60 suburbs are the load-bearing decision. They span four LGAs — Camden, Liverpool, Campbelltown and Wollondilly — which means four different vehicle-crossing processes, four fee schedules, and genuinely different ground: Wianamatta shale in Camden, alluvial river flats along the Nepean and Georges, sandstone through Wollondilly's Appin and Wilton, and documented salinity near Kemps Creek and South Creek. That is real material, not padding.

---

## 2. Suburb expansion — 60 suburbs across 4 LGAs

**Camden Council (20)** — Oran Park, Gregory Hills, Gledswood Hills, Catherine Field, Harrington Park, Narellan, Narellan Vale, Smeaton Grange, Mount Annan, Currans Hill, Spring Farm, Elderslie, Cobbitty, Camden South, Kirkham, Grasmere, Ellis Lane, Theresa Park, Camden Park, Cawdor

**Liverpool City Council (20)** — Austral, Leppington, Edmondson Park, Bringelly, Rossmore, Middleton Grange, West Hoxton, Hoxton Park, Carnes Hill, Horningsea Park, Elizabeth Hills, Len Waters Estate, Cecil Hills, Prestons, Casula, Moorebank, Chipping Norton, Wattle Grove, Kemps Creek, Cecil Park

**Campbelltown City Council (12)** — Campbelltown, Leumeah, Minto, Ingleburn, Glenfield, Macquarie Fields, Raby, Eagle Vale, Bradbury, Glen Alpine, Gilead, Menangle Park

**Wollondilly Shire (8)** — Wilton, Picton, Tahmoor, Appin, Douglas Park, Menangle, The Oaks, Bargo

**Deliberately excluded:** `Camden` itself (the homepage owns `concreters camden` — see the cannibalisation fix), `Denham Court` and `Bardia` until the LGA split is verified per lot.

Each new LGA earns its own guide, because the crossing process genuinely differs:
- `/guides/camden-council-driveway-crossing/`
- `/guides/liverpool-council-vehicle-crossing/`
- `/guides/campbelltown-council-driveway-crossing/`
- `/guides/wollondilly-council-driveway-crossing/`

---

## 3. Service pages — 7 to 10

Add three that have real standalone demand and no good home in the existing seven:

| New page | Justification |
|---|---|
| `/concrete-driveway-replacement-south-west-sydney/` | Replacement is a different query and a different buyer to "new driveway". Campbelltown and Camden's 1990s stock make it a top-3 service across 20+ suburbs. |
| `/shed-and-garage-slabs-south-west-sydney/` | Distinct query, distinct spec, and the dominant second job on every growth-corridor lot. |
| `/concrete-crossovers-and-laybacks-south-west-sydney/` | Council-facing intent. Four LGAs, four processes — this is the page that earns the crossing guides' links. |

Full list: driveways, driveway replacement, slabs, shed & garage slabs, exposed aggregate, decorative, patios, paths, crossovers & laybacks, commercial.

---

## 4. Suburb × service — the 180, and the gate that keeps them legitimate

**URL pattern:** `/{service-slug}-{suburb-slug}/` — e.g. `/exposed-aggregate-harrington-park/`

**Not every intersection gets built.** 60 × 10 = 600 possible; you build 180. The selection rule is the entire defence, so it's mechanical:

> An intersection page is built **only if** `suburbs.json` supplies a non-empty `intersection_differentiators.{service}` value for that suburb — a fact about that service in that suburb that is false in at least half the other suburbs.

Three per suburb, on average, chosen from the suburb's own `job_mix_weighting`. If a suburb only yields two real differentiators, it gets two pages. If it yields five, it gets five. **Never pad to hit a quota.**

Worked examples of what qualifies:

| Intersection | Differentiator | Verdict |
|---|---|---|
| Exposed aggregate × Harrington Park | Harrington Grove DCP forbids any uncoloured concrete on a driveway | ✅ Build |
| Commercial × Gregory Hills | Smeaton Grange industrial estate adjacency; forklift-rated slabs, loading aprons | ✅ Build |
| Driveways × Cobbitty | Rural dish crossing, table-drain invert alignment, bitumen shoulder seal | ✅ Build |
| Driveway replacement × Mount Annan | 1990s stock at 25–30 years, layback settlement is the dominant failure mode | ✅ Build |
| Crossovers × Leppington | Suburb splits Camden/Liverpool — two applications, two fee schedules | ✅ Build |
| Paths × Currans Hill | Nothing true here that isn't true of Mount Annan | ❌ Skip |
| Patios × Elizabeth Hills | Nothing suburb-specific | ❌ Skip |

**Intersection page shape (~700 words, shorter than a suburb page):** H1 `{Service} {Suburb}` → 120-word intro leading with the differentiator → the differentiator section (~250w, unique) → spec/process for this service (shared component, drawn from the parent service page, ~150w) → what it costs here (~100w, real ranges or placeholder) → 2-question FAQ (unique) → links up to the parent service page and across to the suburb page.

**Hard rule:** an intersection page must link up to both parents and must never be the only page targeting its suburb. The suburb page always exists first.

---

## 5. Guides — 7 to 35

Guides are the safest way to add page count because each targets a genuinely distinct informational query and none of them are geo-multiplied.

**Council & approvals (6)** — one per LGA, plus `driveway-crossover-cost-nsw`, `do-i-need-council-approval-driveway-nsw`

**Ground & engineering (8)** — reactive clay & AS 2870, salinity & concrete in western Sydney, engineered fill and why new-estate slabs crack, site classification explained, concrete strength grades explained, SL72 vs SL82 reinforcement, slab thickness for driveways vs sheds, control joints and saw-cut timing

**Cost (7)** — driveway cost per m² NSW, slab cost per m², exposed aggregate cost, stencilled vs stamped cost, shed slab cost, commercial hardstand cost, what actually moves a concrete quote

**Finishes & materials (7)** — exposed aggregate vs stencil, coloured concrete explained, honed and polished, broom finish, non-slip finishes for pools and slopes, sealing and resealing, concrete vs pavers vs asphalt

**Problems & maintenance (7)** — why concrete cracks, crack types and which matter, repair vs replace, how long before you can drive on it, curing in summer vs winter, efflorescence, removing oil stains and tyre marks

---

## 6. Cost & comparison pages (10)

Commercial-investigation intent, distinct from both service pages and guides: driveway cost calculator, slab volume calculator, concrete vs pavers, concrete vs asphalt, exposed aggregate vs plain, DIY vs hiring a concreter, and four `{finish} cost` pages.

**The calculators are the linkable asset.** A Camden/Liverpool/Campbelltown/Wollondilly crossover-requirements calculator that tells someone which application they need, the width and grade limits and the fee — nobody has built one, it's genuinely useful, and local builders and estate agents link to that kind of thing. One asset earning links passively beats fifty more suburb pages.

---

## 7. Publishing waves — this is not optional

300 pages appearing on a three-week-old domain is the strongest possible scaled-content signal you can send. Build all 300 in the WXR; publish in five waves.

| Wave | Pages | Cumulative | Gate to release |
|---|---|---|---|
| 1 | Home, 4 utility, 10 services, 6 Tier 1 suburbs | 21 | Live, indexed, CWV green |
| 2 | 15 guides | 36 | Wave 1 pages earning impressions in GSC |
| 3 | 24 more suburbs (Camden + Liverpool remainder) | 60 | ≥1 real photo or real quoted price per page |
| 4 | 30 suburbs (Campbelltown + Wollondilly) + 20 guides + 10 cost pages | 120 | Wave 3 earning impressions; operator signed |
| 5 | 180 intersection pages, in batches of 30 | 300 | Each batch gated on the previous batch's impressions |

Everything past Wave 1 ships in the import file as `draft`. You publish when the gate passes, not when the calendar says so.

**Honest expectation:** at Wave 5 you're publishing intersection pages roughly 9–12 months from launch. If that sounds slow, the alternative isn't faster — it's a domain that ranks for nothing.

---

## 8. Uniqueness enforcement at 300 pages

The 60%-unique rule from the 32-page plan doesn't scale — at 300 pages you need mechanical enforcement, not a spot check.

1. **Global 5-gram index.** Every sentence written is hashed into an index. Any 5-gram appearing on more than 3 pages is flagged and the newer page rewritten.
2. **Per-class thresholds:** suburb pages ≥60% unique body words; intersection pages ≥50% (they legitimately share a spec component); guides ≥85%.
3. **Pairwise cap:** no two pages in the same class exceed 40% overlap.
4. **Differentiator assertion:** every suburb and intersection page must have a non-empty `unique_local_variable` or `intersection_differentiators.{service}`. Build fails on any page without one.
5. **Opening-paragraph test:** the first 80 words must be false if pasted onto a sibling page. Codex reports pass/fail per page.

Any page failing 1–5 is not written. Not rewritten weaker — **not written.** The page count is an output of how much real material exists, not a target the material gets stretched to fit.

---

## 9. Images at 300 pages

You have 83 source images. 300 pages sharing 83 images is fine — image reuse across pages is normal and not a ranking problem. What matters:

- **Every image re-encoded** so hashes differ from the Melbourne originals (footprint rule, unchanged)
- **Alt text written per page**, describing the image in that page's context — the same photo on the Oran Park and Cobbitty pages gets different alt text
- **No image appears on more than ~15 pages** — spread the 83 across the set rather than putting the same hero on 60 suburb pages
- **Suburb-specific photos replace generic ones as you get them.** Your `[[REAL_PHOTO_PENDING]]` slots stay flagged until filled.

---

## 10. What this costs you

Being straight about the trade: 300 pages is roughly 210,000 words of content that must all be defensible. Even generated, that's a large surface area to keep accurate — every council spec, every soil classification, every fee. One wrong figure repeated across 30 intersection pages is 30 wrong pages.

The 60 new suburbs also need the research the original 16 got: council, soil, estates, water feature, housing era, job mix, failure mode. `suburbs-expanded.json` supplies the verified skeleton — LGA, postcode, tier, growth profile — and marks the deep fields `REQUIRED-RESEARCH`. **Codex must not invent those fields.** Any suburb whose research fields are unfilled builds as `draft` + `noindex` and doesn't count toward the live page total.

The realistic near-term number is Wave 1 and 2: **36 live pages** with real substance. The 300 is the architecture those 36 grow into over a year, gated on evidence at every step.
