# Report 57b — conflicts between the titles/breadcrumbs/near-me spec and the governing record

Run: 24 August 2026 (Australia/Sydney). Companion to `reports/57-titles-breadcrumbs-nearme-audit.md`.
States what was verified against artifacts on disk. Describes no live site, launch or approval.

**Correction to check 10 of the checklist run:** JSON-LD `item` values contain no `#`, because the
builder normalises the Areas crumb to `https://concreterscamden.com.au/`. The **visible** breadcrumb
still links to `/#areas` (and `/#services`) on **70 of 77** pages. §6.1 defect 2 is real in the
rendered HTML; the JSON-LD hides it by collapsing that crumb to the homepage, producing exactly the
`Home / Home / Page` hierarchy §6.1 describes.

---

## C1 — The (03) number is owner-attested, not a defect

Spec §7.3 and §9 item 1 call `(03) 4328 3392` a Victorian area code that voids every geographic
signal, and make replacing it the blocker for all other work.

`data/verified-facts.yml` → `contact.phone`:

```yaml
value: "(03) 4328 3392"
uri: "tel:+61343283392"
verified: true
ownership_proven: true
routing_proven: true
note: >
  Owner-attested public telephone. It must not be described as a local Camden or
  Sydney number; the (03) area code is retained exactly as supplied.
source: "owner attestation, 21 August 2026"
```

No `02` number exists anywhere in the repository. `suburbs.json` → `site.phone_e164` is the unfilled
placeholder `[[TWILIO_E164]]`.

The SEO reasoning is sound — an (03) number on a Camden site is a genuine geographic contradiction.
But the number is a verified owner-supplied fact, and CLAUDE.md §3 hard stop 6 forbids inferring one.
**Order-of-work item 1 cannot be executed.** It needs either an owner-supplied NSW number, or an
explicit owner decision to keep the (03) number and omit `telephone` from schema.

## C2 — "Concreters {Suburb}" contradicts the verified operating model

§1 bans "enquiries" and "coordination" from titles; §2–§4 set every title and H1 to
`Concreters {Suburb}` / `Concreters in {Suburb}`.

DECISION-09 D39 and `verified-facts.yml` → `operating_model`:

```yaml
Structure Co Concreters Camden manages concreting enquiries and coordinates
suitable independent providers.
structure_co_direct_contractor: false
independent_providers: true
note: Do not ... imply that Structure Co directly performs regulated concreting work.
```

`legal_entity.nsw_fair_trading_licence` is unverified and empty. The current "enquiries" copy is
deliberate: the entity holds no licence and does not perform the work.

`Concreters in Oran Park` as an H1 on a page for an entity that is not a concreter is the class of
claim D39 exists to remove. The domain and the brand string ("Structure Co Concreters Camden") are
settled and are a different question from a page asserting the service.

**Owner decision required.** A middle path exists: the §1–§4 titles verbatim (they read as a
directory/market claim, not a licence claim), with H1s that do not assert direct performance.

## C3 — Scope: the spec covers 16 suburbs, the build has 60

| | |
|---|---|
| Suburb pages in `suburbs.json` | 16 |
| Suburb pages in `build/cloudflare-pages/` | 60 |
| In spec, not built | `camden` (correctly absent per §2) |
| Built, not in spec | **45** |

The 45: appin, bargo, bradbury, camden-park, camden-south, campbelltown, carnes-hill, casula,
cawdor, cecil-hills, cecil-park, chipping-norton, douglas-park, eagle-vale, elizabeth-hills,
ellis-lane, gilead, glen-alpine, glenfield, grasmere, horningsea-park, hoxton-park, ingleburn,
kemps-creek, kirkham, len-waters-estate, leumeah, macquarie-fields, menangle, menangle-park,
middleton-grange, minto, moorebank, narellan-vale, picton, prestons, raby, rossmore,
smeaton-grange, tahmoor, the-oaks, theresa-park, wattle-grove, west-hoxton, wilton.

DECISION-09 D41 says "attempt to rebuild all 76 active pages". The spec is silent on these 45.
Checklist item "Exactly 6 suburb pages are `index,follow`; the other 10 are `noindex,follow`" is
unsatisfiable while 60 suburb pages exist.

**Owner decision required:** noindex all 54 non-Tier-1 suburb pages, remove the 45 from the build,
or extend `suburbs.json` to cover them.

## C4 — The 16 meta descriptions do not meet the spec's own length rule

§1: "150–158 characters … All 16 suburb descriptions already exist in `suburbs.json` and are good —
use them verbatim."

Measured from `suburbs.json`:

| Suburb | Chars | Suburb | Chars |
|---|---|---|---|
| oran-park | 182 | narellan | 145 |
| gledswood-hills | 170 | mount-annan | 149 |
| gregory-hills | 169 | edmondson-park | 149 |
| camden | 164 | cobbitty | 137 |
| austral | 163 | bringelly | 136 |
| leppington | 162 | currans-hill | 131 |
| harrington-park | 156 | elderslie | 126 |
| spring-farm | 155 | | |
| catherine-field | 155 | | |

Only 4 of 16 fall inside 150–158; six are short, six are long. "Verbatim" and the length rule cannot
both hold.

**Recommendation:** take them verbatim and relax the rule to roughly 120–185. The descriptions are
specific and well written, and Google rewrites descriptions on most queries regardless.

## C5 — Service URL map is not 1:1

10 built service pages, 11 target `/services/` slugs. Eight map unambiguously:

| Built (flat root) | Target |
|---|---|
| `concrete-driveways-south-west-sydney` | `/services/concrete-driveways/` |
| `exposed-aggregate-south-west-sydney` | `/services/exposed-aggregate/` |
| `concrete-paths-south-west-sydney` | `/services/concrete-paths-and-footpaths/` |
| `concrete-patios-south-west-sydney` | `/services/alfresco-and-patio-slabs/` |
| `concrete-driveway-replacement-south-west-sydney` | `/services/concrete-removal-and-replacement/` |
| `shed-and-garage-slabs-south-west-sydney` | `/services/shed-and-garage-slabs/` |
| `concrete-crossovers-and-laybacks-south-west-sydney` | `/services/driveway-crossovers/` |
| `commercial-concreting-south-west-sydney` | `/services/commercial-concreting/` |

Two sources, three targets, unresolved:

- `concrete-slabs-south-west-sydney` → `/services/house-slabs/`? Its current copy covers shed, garage
  and extension slabs — which is the `shed-and-garage-slabs` page's subject. `/services/house-slabs/`
  has no source content.
- `decorative-concrete-south-west-sydney` → `/services/coloured-concrete/` **or**
  `/services/stencilled-and-stamped-concrete/`. Both are spec targets, one source page; a 301 can
  point at only one.

## C6 — §5.2, §4 and §7.2 are blocked on unverified owner data

| Requirement | Blocked by |
|---|---|
| §5.2 near-me price FAQ ("real price band, per m²") | `pricing.per_m2_ranges` unverified, `blocks_pages: 53` |
| §4 lifting `noindex` on Tier 2/3 (real quoted price **and** real photograph) | the above, plus `photography.real_camden_photographs` unverified, `blocks_pages: 16` |
| §5.2 first FAQ, "within {X} business days" | `X` is specified nowhere; owner fact |
| §7.2 `Organization` node | needs `telephone` (C1) and `legal_entity.legal_name`, unverified. DECISION-08 D35 clause 4: "Nothing in this decision authorises emitting `Organization` or `LocalBusiness`." |
| §4 Bringelly | `lga: "VERIFY — Liverpool City Council / Camden Council boundary"`. Hard stop 6 forbids inferring it. |

Applying the spec's own rules: with no verified prices and no verified photographs, **all 10 Tier 2/3
pages stay `noindex,follow` indefinitely**, and the second near-me FAQ is omitted on every page.

## C7 — The build currently marks all 76 pages indexable

`robots.txt` is `Allow: /`, the sitemap lists 76 URLs, and 76 of 77 pages are `index,follow` —
including all 60 suburb pages and all 10 flat service URLs the spec wants 301'd. Commit `fea543a`
("Enable indexing for live Camden site") set this. Under §4 this is the failure mode the spec warns
about: thin pages suppressing the strong ones.

---

## What is unblocked and can proceed without an owner answer

1. Breadcrumbs (§6) — drop the fourth crumb, remove the `/#areas` and `/#services` fragments, make
   the terminal crumb plain text with no `item`, align visible labels to JSON-LD. Depends on the
   `/areas/` and `/services/` hubs existing.
2. Build the `/areas/` and `/services/` hubs (§2, §5.3), including the varied anchor text.
3. Move service pages to `/services/{slug}/` and write a Cloudflare `_redirects` file — for the 8
   unambiguous mappings (C5), plus `/concreters-camden/ → /` as a defensive rule.
4. Apply the `noindex,follow` gate and regenerate the sitemap — pending the C3 scope answer for the
   45 out-of-spec suburbs.
5. Add the §5.1 near-me H2 and the §5.4 service-in-suburb H3 blocks.
6. Add the §6.5 and §8 build assertions to the gate scripts so regressions fail the build.
