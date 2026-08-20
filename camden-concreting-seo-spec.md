# Camden Concreting — Keyword, Semantic SEO & Schema Specification

**Domain:** `concreterscamden.com.au`
**Market:** Camden LGA + South West Sydney Growth Area (Camden, Liverpool, part Campbelltown councils)
**Data file:** `suburbs.json` — Codex reads this, not this document, for per-page values
**Status:** specification only. Nothing here gets published until the `[[PLACEHOLDER]]` values in `suburbs.json` are replaced with real, verified data.

---

## 1. Read this before anything else

This site has 16 planned suburb pages. Sixteen near-identical pages with a suburb name swapped in is a **doorway page cluster**, and it is the single most common way local service sites get flattened by Google's scaled-content-abuse policy. The policy doesn't care whether a human or a model wrote the pages — it cares whether each page carries value that doesn't exist on the others.

The defence is already built into `suburbs.json`: every suburb carries a different council process, a different soil/flood/heritage constraint, a different estate set, a different job mix and a different failure mode. Oran Park's footpath allocation genuinely is 800mm when the rest of Camden's is 900mm. Harrington Grove's DCP genuinely does forbid any uncoloured concrete on a driveway. Cobbitty genuinely does need a dish crossing and a bitumen shoulder seal. Those are facts, not filler, and they're what makes the pages defensible.

**Hard rule: no suburb page ships without at least one real, first-hand element** — a photo of a job you actually poured, a price you actually quoted, or an observation you actually made on site. Until an operator is signed in Camden, that means launching six pages, not sixteen. Six pages with real substance beat sixteen with `[[placeholder]]` in them, and the sixteen will actively hold the domain back.

---

## 2. Architecture

```
/                                       Home — brand + primary market (Camden)
/services/                              Service hub
/services/{service-slug}/               11 service pages
/concreters-{suburb-slug}/              16 suburb pages
/guides/                                Informational hub
/guides/{topic}/                        Cost + how-to articles
/about/  /quote/  /gallery/  /contact/
```

**URL rules:**
- Suburb pages sit at root as `/concreters-{suburb}/`, not nested under `/areas/`. Shorter, matches the query, avoids a weak intermediate hub.
- Trailing slash everywhere, canonical matching exactly. (This is the exact bug that bit Alpha Flooring — set it once, sitewide, at the config level.)
- No suburb × service combination pages in v1. `/concreters-oran-park/` and `/services/exposed-aggregate/` cover it. Building 16 × 11 = 176 intersection pages is how you manufacture a doorway cluster.
- v2 exception: build a combination page **only** where the suburb page's own analytics show the intersection earning impressions on its own. Earn it, don't assume it.

**Internal linking (directional, enforced):**

| From | To | Anchor style |
|---|---|---|
| Home | all Tier 1 suburb pages | suburb name only |
| Home | all service pages | service name only |
| Suburb page | its 3–5 highest-weighted services | `{service} in {suburb}` |
| Suburb page | 4 named neighbouring suburbs (`internal_links_out`) | suburb name only |
| Service page | 4–6 suburbs where that service is weighted highest | `{service} {suburb}` |
| Guide | relevant service page | descriptive, non-exact-match |
| Anything | Home | brand name |

Never link suburb → suburb reciprocally in a full mesh. Use the curated `internal_links_out` array so the graph has direction and doesn't look machine-generated.

---

## 3. Keyword targeting model

**One page, one primary query.** Every page in `suburbs.json` carries `primary_keyword` and `secondary_keywords`. Do not target two competing primaries on one page.

### Suburb pages
- **Primary:** `concreters {suburb}` — this is the head local term and the one worth the H1 and title.
- **Secondary cluster:** `concreter {suburb}`, `concreting {suburb}`, `concrete driveway {suburb}`, `concrete slab {suburb}`, `{suburb} concrete contractors`, plus 1–3 suburb-specific modifiers drawn from the job mix (`battle axe driveway austral`, `warehouse slab gregory hills`, `rural driveway cobbitty`).
- **Do not chase** `concreters near me` on a page. It's a device-location query resolved by the map pack, not by a landing page.

### Service pages
- **Primary:** `{service} sydney` or `{service} south west sydney` — broader, harder, slower.
- These will rank later than suburb pages. Build them because they anchor the topical structure and receive links from suburb pages, not because they'll rank in month three.

### Guides (informational — separate intent, separate page type)
Do not put informational content on a commercial suburb page. Build these under `/guides/`:
1. `concrete driveway cost nsw` — the highest-volume informational term in the niche
2. `driveway crossover approval camden council`
3. `exposed aggregate vs stencilled concrete`
4. `how long before you can drive on new concrete`
5. `reactive clay concrete slab as2870`
6. `salinity concrete western sydney`

Items 2, 5 and 6 are the winnable ones — low competition, and you can answer them from real jobs. Item 1 is the head term that will take links.

### The one honest caveat on keywords
There is no keyword tool output in this document because none of the volume figures would be yours. Before committing to the Tier 1 build order, pull actual volume and difficulty for `concreters {suburb}` across all 16 in Ahrefs or Keywords Everywhere and re-rank. The build order in `suburbs.json` (`tier`) is based on new-build volume, job value and how genuinely differentiated the page can be — not on verified search volume.

**Competitor recon note:** `westernsydneytrades.com.au` already runs a Leppington concreters page using the reactive Wianamatta clay, AS 2870 and Camden crossover-permit angle, with a cost calculator. That's a lead-gen aggregator, not an operator. Beat it where it can't compete: real photos of real pours, a named licensed operator, a specific licence number. Don't try to beat it on word count.

---

## 4. Semantic SEO — what makes each page locally relevant

Google understands a page's locality through **entity co-occurrence**, not through keyword repetition. `concreters oran park` written eleven times tells it nothing. "Oran Park Podium", "Peter Brock Drive", "Camden Growth Centres LEP 2008" and "Julia Reserve" appearing naturally in the same document tells it a great deal — those entities have unambiguous geographic coordinates in Google's knowledge graph, and a page that co-occurs with them is a page about that place.

Each suburb object in `suburbs.json` carries a `local_entities` block with four entity classes. Use them like this:

| Entity class | Where it belongs | How many |
|---|---|---|
| `estates_developers` | Local build context section | 2–4, named naturally |
| `streets_roads` | Job examples, access notes, service-area sentence | 2–3 |
| `landmarks` | Intro or "areas we cover" sentence | 2–3 |
| `planning_instruments` | Approval path section | 1–2, cited precisely |

**How not to do it.** Do not write "We service Oran Park Podium, Julia Reserve, Oran Park Library and Oran Park Anglican College." That's a stuffed list and it reads exactly like the scam sites you're trying not to resemble. Write instead: *"Most of our Oran Park work comes out of the newer releases north of the Podium, where the standard handover is a 350–450sqm lot with a double garage and no driveway poured yet."* Same entities, embedded in a real sentence that carries information.

**Semantic depth beyond entities.** The other half of semantic relevance is covering the *concepts* a genuine expert would cover. For concreting these are: AS 2870 site classification, reactive clay movement, engineered fill and compaction, SL72/SL82 reinforcement, MPa strength grades, slab thickness, control and expansion jointing, curing time vs trafficable time, crossfall and grade, saw-cut timing, and the finish types. Each suburb page should touch three or four of these — the ones that actually matter for that suburb's job mix — not all of them. A page that covers everything covers nothing.

---

## 5. Page module system (this is what keeps it out of doorway territory)

Every suburb page is built from ten modules. **Six must be unique per suburb.** The build gate is: **minimum 60% of body words unique across the suburb set, and no full sentence reused on more than two pages.**

| # | Module | Unique? | Source field in `suburbs.json` |
|---|---|---|---|
| 1 | H1 + opening 80 words | ✅ Unique | `unique_local_variable` — lead with it |
| 2 | Services we do here | ⬜ Shared component | `services[]`, filtered by `job_mix_weighting` |
| 3 | Local build context | ✅ Unique | `local_entities`, `housing_stock_era` |
| 4 | Ground conditions | ✅ Unique | `ground_conditions` |
| 5 | Council & approval path | ✅ Unique | `approval_path`, `geo_facts_shared.camden_driveway_spec` |
| 6 | Typical jobs & price band | ✅ Unique | `typical_jobs` + **your real quoted ranges** |
| 7 | Recent job + photos | ✅ Unique | **Real photos only.** Hold the page if none exist. |
| 8 | Suburb FAQ (3–4 Q) | ✅ Unique | `faq_angles` |
| 9 | Nearby areas | ⬜ Shared component | `internal_links_out` |
| 10 | Quote CTA | ⬜ Shared component | site config |

**Module 1 rule.** The first 80 words must contain something that is true of this suburb and false of the other fifteen. If you can copy the opening paragraph to another suburb page and it still reads correctly, it fails and the page doesn't ship.

**Module 6 and 7 integrity rule.** These carry the non-commodity signal — the thing that separates a ranking page from AI sludge in 2026. They must be real. Do not invent a price you've never quoted, a job you've never poured, or a photo you didn't take. If you don't have them yet, render the module as an explicit placeholder in the codebase and set the page to `noindex` until it's filled. A fabricated case study on a trades site is a consumer-law problem in Australia, not just an SEO one.

**Stock photos are a footprint risk.** Alpha and Woodland already shared byte-identical image hashes across domains. Do not repeat that here. Every image needs to be original, resized per page, with a distinct filename (`oran-park-exposed-aggregate-driveway-2570.webp`) and descriptive alt text that describes the photo rather than repeating the keyword.

---

## 6. Title tags and meta descriptions

Written per suburb in `suburbs.json` — deliberately not templated. Templated titles (`Concreters {Suburb} | Best Concreting {Suburb} | Free Quote {Suburb}`) are a visible pattern in the SERP and a visible pattern to Google.

Constraints Codex must enforce:
- `title_tag`: 50–60 characters. Primary keyword near the front. Reads like a person wrote it.
- `meta_description`: 140–160 characters. Written for click-through, and where possible mentioning the suburb-specific fact so the snippet differentiates itself.
- No two suburb pages share a title or description structure verbatim. If the pattern is visible across three or more pages, rewrite.
- **Regression guard:** the `seoForPath()` normalisation bug on Alpha silently fell back to the wrong template for 50 pages. Codex must add an explicit assertion in the build: every route resolves a `title_tag` and `meta_description` that is *present in the data file*, and the build fails loudly on any fallback. Do not let a silent default template ship again.

---

## 7. Schema markup plan

**The approach in one paragraph.** Every page emits exactly one `<script type="application/ld+json">` block containing a single `@graph` array, rather than several loose scripts. Inside that graph, the site's stable entities — the `Organization`, the `WebSite` and the physical `LocalBusiness` — are declared once with permanent `@id` values anchored to the domain (`https://concreterscamden.com.au/#organization`, `/#website`, `/#localbusiness`), and every page thereafter *references* those `@id`s rather than redeclaring them. This is what turns a pile of disconnected markup into a connected entity graph Google can actually resolve: the crawler sees one business, one website, and many pages that point back to the same business, instead of sixteen separate businesses that happen to share a phone number. The page-specific nodes then hang off that spine — a `WebPage` node identified by the page URL, a `BreadcrumbList` showing where it sits in the hierarchy, and a `Service` node describing what's offered, with the `Service` node's `provider` property pointing at the `#localbusiness` `@id` and its `areaServed` property naming the suburb as a `City` or `AdministrativeArea` entity. The single most important rule here, and the one most local sites get catastrophically wrong: **the suburb pages must not each emit their own `LocalBusiness` node.** A `LocalBusiness` asserts a physical place with an address, and declaring one for a suburb you don't have premises in is a false claim that Google's local systems treat as spam — it is functionally the same footprint mistake as the multi-account GBP setup that got listings suspended. One real business address, declared once, on the homepage and contact page only. Suburb pages describe *services offered in an area*, which is what `Service` + `areaServed` exists to express. Beyond that: `FAQPage` markup goes only on pages where the questions and answers are genuinely visible to a human visitor, and it should be understood that since Google's 2023 restriction of FAQ rich results to authoritative government and health sites, this markup no longer earns you stars in the SERP — it is worth including anyway because it clarifies entity relationships and materially improves the odds of being quoted by AI search surfaces, which is a growing share of how people find trades. `AggregateRating` and `Review` markup should only ever be emitted from reviews that genuinely exist and were genuinely left by customers, and self-serving review markup collected on your own site has been ineligible for rich results since 2019 — so include it for honest entity signal, never as a rich-result play. Finally, every value inside the JSON-LD must match what a human sees on the rendered page: if the schema says the phone number is one thing and the footer says another, that's not a technicality, it's an inconsistency that undermines the NAP signal the entire local ranking system is built on.

### 7.1 Site-wide entity spine (emit on every page)

```jsonc
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://concreterscamden.com.au/#organization",
      "name": "[[BRAND_NAME]]",
      "url": "https://concreterscamden.com.au/",
      "logo": { "@type": "ImageObject", "@id": "https://concreterscamden.com.au/#logo", "url": "https://concreterscamden.com.au/logo.png", "width": 512, "height": 512 },
      "telephone": "[[TWILIO_E164]]",
      "email": "[[EMAIL]]",
      "sameAs": ["[[GBP_MAPS_URL]]", "[[FACEBOOK_URL]]", "[[INSTAGRAM_URL]]"]
    },
    {
      "@type": "WebSite",
      "@id": "https://concreterscamden.com.au/#website",
      "url": "https://concreterscamden.com.au/",
      "name": "[[BRAND_NAME]]",
      "publisher": { "@id": "https://concreterscamden.com.au/#organization" },
      "inLanguage": "en-AU"
    }
  ]
}
```

### 7.2 LocalBusiness node — homepage and `/contact/` ONLY

```jsonc
{
  "@type": "GeneralContractor",
  "@id": "https://concreterscamden.com.au/#localbusiness",
  "name": "[[BRAND_NAME]]",
  "url": "https://concreterscamden.com.au/",
  "telephone": "[[TWILIO_E164]]",
  "priceRange": "$$",
  "image": "https://concreterscamden.com.au/images/[[REAL_PHOTO]].webp",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[[REAL_STREET_ADDRESS]]",
    "addressLocality": "[[HQ_SUBURB]]",
    "addressRegion": "NSW",
    "postalCode": "[[HQ_POSTCODE]]",
    "addressCountry": "AU"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "[[LAT]]", "longitude": "[[LNG]]" },
  "areaServed": [
    { "@type": "AdministrativeArea", "name": "Camden Council" },
    { "@type": "City", "name": "Oran Park", "addressRegion": "NSW" }
    // ...one entry per suburb, generated from suburbs.json
  ],
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "07:00", "closes": "17:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00" }
  ],
  "parentOrganization": { "@id": "https://concreterscamden.com.au/#organization" }
}
```

`GeneralContractor` is a subtype of `HomeAndConstructionBusiness`, which is a subtype of `LocalBusiness` — it inherits everything and is more specific, which is better for entity resolution.

The address must be a real, staffed address. A virtual office or a residential address you don't operate from is the same category of risk as the GBP setup that got suspended. If there is no legitimate address yet, **omit the `LocalBusiness` node entirely** and run `Organization` + `Service` only. An incomplete graph is survivable; a false address is not.

### 7.3 Suburb page graph (the critical one)

```jsonc
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://concreterscamden.com.au/#organization" /* reference only */ },
    {
      "@type": "WebPage",
      "@id": "https://concreterscamden.com.au/concreters-oran-park/#webpage",
      "url": "https://concreterscamden.com.au/concreters-oran-park/",
      "name": "{{title_tag}}",
      "description": "{{meta_description}}",
      "isPartOf": { "@id": "https://concreterscamden.com.au/#website" },
      "breadcrumb": { "@id": "https://concreterscamden.com.au/concreters-oran-park/#breadcrumb" },
      "inLanguage": "en-AU",
      "primaryImageOfPage": { "@id": "https://concreterscamden.com.au/concreters-oran-park/#primaryimage" }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://concreterscamden.com.au/concreters-oran-park/#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://concreterscamden.com.au/" },
        { "@type": "ListItem", "position": 2, "name": "Areas We Service", "item": "https://concreterscamden.com.au/areas/" },
        { "@type": "ListItem", "position": 3, "name": "Concreters Oran Park" }
      ]
    },
    {
      "@type": "Service",
      "@id": "https://concreterscamden.com.au/concreters-oran-park/#service",
      "serviceType": "Concreting",
      "name": "Concreting in Oran Park",
      "description": "{{first sentence of unique_local_variable}}",
      "provider": { "@id": "https://concreterscamden.com.au/#localbusiness" },
      "areaServed": {
        "@type": "City",
        "name": "Oran Park",
        "address": { "@type": "PostalAddress", "addressLocality": "Oran Park", "postalCode": "2570", "addressRegion": "NSW", "addressCountry": "AU" }
      },
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Concreting services in Oran Park",
        "itemListElement": [
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Concrete driveways", "url": "https://concreterscamden.com.au/services/concrete-driveways/" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Shed and garage slabs", "url": "https://concreterscamden.com.au/services/shed-and-garage-slabs/" } }
          // generated from job_mix_weighting, top 3–5 only
        ]
      }
    },
    {
      "@type": "FAQPage",
      "@id": "https://concreterscamden.com.au/concreters-oran-park/#faq",
      "mainEntity": [
        { "@type": "Question", "name": "{{faq_angles[0]}}", "acceptedAnswer": { "@type": "Answer", "text": "{{visible answer text, verbatim}}" } }
      ]
    }
  ]
}
```

**Note the absence.** There is no `LocalBusiness` node on this page. That is deliberate and it is the most important line in this section.

### 7.4 Service page graph
Same shape, but the `Service` node's `areaServed` becomes the full `AdministrativeArea` list rather than a single `City`, and `hasOfferCatalog` lists suburbs instead of services.

### 7.5 Guide/article graph
`Article` (or `BlogPosting`) with `author` pointing at a real named person `@id`, `publisher` referencing `#organization`, plus `datePublished` and `dateModified` that reflect reality. E-E-A-T for trades content is carried by a named, credentialed author — an unattributed article on concrete specification is worth less than a signed one.

### 7.6 Schema validation gate (Codex must implement)
1. Every page's JSON-LD parses as valid JSON — build fails otherwise.
2. Every `@id` referenced somewhere is defined somewhere on the site.
3. No `LocalBusiness`/`GeneralContractor` node appears on any URL other than `/` and `/contact/`.
4. Every `FAQPage` question/answer string appears verbatim in the rendered HTML.
5. No `[[PLACEHOLDER]]` string appears in any emitted JSON-LD — build fails if one does.
6. Post-build: run every URL type through Google's Rich Results Test and the Schema.org validator before submitting the sitemap.

---

## 8. Technical build requirements

- **Stack:** Astro (matches the Alpha/Woodland codebase — static output, fast by default, and you already know it). WordPress is viable but adds CWV work you don't need.
- **Core Web Vitals targets:** LCP < 2.5s, INP < 200ms, CLS < 0.1. No hero video — that's what's hurting Spick n Span's LCP. Hero is a single optimised WebP with explicit width/height.
- **Canonical:** absolute URL, trailing slash, matching the served URL exactly. Assert this in the build.
- **Sitemap:** auto-generated, excluding any page flagged `noindex`. Submit in Search Console at launch.
- **robots.txt:** allow all, point to sitemap. No accidental disallows.
- **Images:** WebP, lazy-loaded below fold, `loading="eager"` + `fetchpriority="high"` on the LCP image only.
- **Phone:** one Twilio tracking number, consistent everywhere — footer, schema, GBP, citations. Whisper forwarding to the operator once signed.
- **`noindex` gate:** any suburb page whose Module 6 or 7 still contains placeholder content is rendered with `<meta name="robots" content="noindex,follow">`. Codex must derive this from the data file, not from a manual list.

---

## 9. Build order

| Phase | Pages | Gate to proceed |
|---|---|---|
| 0 | Verify all `[[PLACEHOLDER]]` values; confirm Camden + Liverpool council specs at source | Nothing ships until done |
| 1 | Home, `/quote/`, `/contact/`, `/about/`, service hub | Live, indexed, CWV green |
| 2 | 6 Tier 1 suburb pages: Oran Park, Leppington, Gregory Hills, Gledswood Hills, Austral, Harrington Park | Each has ≥1 real photo or real quoted price |
| 3 | 11 service pages | Linked from Tier 1 suburbs |
| 4 | 6 Tier 2 suburb pages | Only once Phase 2 pages show impressions in GSC |
| 5 | 6 guides | Target the winnable informational terms first |
| 6 | 4 Tier 3 suburb pages | Only if Tier 2 is earning impressions |

Phases 4 and 6 are conditional on measured performance, not on the calendar. If the Tier 1 pages aren't earning impressions after 8–10 weeks, adding ten more pages makes the problem worse, not better.

---

## 10. What this spec does not solve

On-page work is one of three inputs and it is the one that saturates first. Once these pages are built to this standard, the bottleneck moves entirely to **referring domains**, which this site will have zero of on day one — the same gap that has capped every site in the portfolio so far. The plan for that is separate: foundational NSW citations with identical NAP, then local editorial links (Camden and Macarthur sponsorships, builder and estate partner pages, supplier listings), then one linkable asset — a Camden Council driveway crossover requirements calculator is the obvious candidate, since it's genuinely useful, nobody has built one, and local trades and builders will link to it.

Second: the map pack is a different competition with different levers. Nothing in this document wins it. That's proximity, GBP categories, review volume and recency — and given the suspension history, it should be treated as upside rather than as the plan.
