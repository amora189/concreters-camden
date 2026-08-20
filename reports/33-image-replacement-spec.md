# Stage 33 Phase 1 — image replacement specification

Date: 18 August 2026 (Australia/Sydney).
Data: `reports/33-image-replacement-spec.csv` (20 rows), `reports/33-soil-module-removal.md`.

```text
  images downloaded        0
  images searched for      0
  images generated         0
  external requests made   0
  files modified           none; camden-concreting-import.xml untouched
```

---

## 1. Disposition summary

```text
  REPLACE                        16   photographic slots, generic imagery
  REMOVE_WITH_MODULE              1   attachment 1020, the soil photograph
  HOLD — LOGO, NOT PHOTOGRAPHY    3   attachments 306, 307, 422
  TOTAL                          20
```

The owner decision was "19 replaced, 1 removed". **Three of the 19 are not photographs — they are logo
files**, and a logo cannot be filled from a stock photography library. The true split is 16 / 1 / 3.

---

## 2. The 16 REPLACE slots

Full data in the CSV. Every proposed filename describes content only; no suburb, council or region name
appears in any of them.

```text
  ID    CURRENT (asserts a place)                          PROPOSED (asserts nothing)                        DIMS       AR     PAGES
  226   concretejob2camden-226.jpg                         residential-concrete-slab-finished-01.jpg          640x480    1.333     14
  480   oran-park1-480.webp                                suburban-street-concrete-driveways-01.webp        1280x960    1.333     14
  481   oran-park2-481.webp                                broom-finish-concrete-driveway-01.webp            1280x960    1.333     14
  482   oran-park3-482.webp                                concrete-edge-control-joint-01.webp                765x1020    0.750     14
  906   driveway-excavation-camden-906.jpg                 driveway-excavation-subbase-01.jpg                 738x384    1.922     14
  907   camden-town-centre-907.jpg                         suburban-street-kerb-and-crossing-01.jpg           515x388    1.327     14
  908   oran-park-growth-estate-908.jpg                    new-residential-estate-slabs-01.jpg                534x374    1.428     14
  924   coloured-concrete-south-west-sydney-924.png        coloured-oxide-concrete-finish-01.png            1200x1200    1.000     15
  925   stencil-concrete-south-west-sydney-925.webp        stencil-concrete-finish-01.webp                    600x450    1.333     15
  926   stamped-concrete-south-west-sydney-926.jpg         stamped-concrete-finish-01.jpg                     554x554    1.000     15
  956   south-west-sydney-growth-corridor-956.png          residential-subdivision-aerial-01.png              906x680    1.332     15
  1150  established-home-mount-annan-1150.jpg              established-home-ageing-driveway-01.jpg            569x368    1.546     14
  1152  mount-annan-established-housing-1152.jpg           established-residential-area-aerial-01.jpg         636x481    1.322     14
  1185  council-crossing-south-west-sydney-1185.jpg        vehicle-crossing-kerb-to-boundary-01.jpg           515x388    1.327     14
  1186  gregory-hills-commercial-concreting-1186.webp      commercial-concrete-hardstand-01.webp              984x554    1.776     14
  1187  leppington-new-estates-1187.jpg                    new-build-homes-fresh-slabs-01.jpg                 645x310    2.081     14
```

### Replacement briefs — photographic content, never place

Every brief specifies subject, framing, lighting, orientation and minimum resolution. Full text in the CSV
`replacement_brief` column.

```text
  226   Freshly poured and finished residential concrete slab, mid-job, trowel marks
        visible, no people in frame, overcast daylight, landscape 4:3. Min 640x480.
  480   Australian suburban residential street, single-storey brick-and-tile homes,
        concrete driveways visible from kerb, native street trees, clear daylight,
        landscape 4:3. Min 1280x960.
  481   Plain broom-finished concrete driveway running from kerb to a single garage,
        clean control joints, no vehicles, overcast daylight, landscape 4:3. Min 1280x960.
  482   Close vertical crop of a concrete edge and control joint against garden bed,
        shallow depth of field, portrait 3:4. Min 765x1020.
  906   Excavator bucket cutting a driveway sub-base, exposed subgrade and spoil pile,
        no operator face visible, daylight, wide landscape 2:1. Min 738x384.
  907   Australian suburban streetscape with kerb, footpath and vehicle crossing, no
        shopfront signage, overcast daylight, landscape 4:3. Min 515x388.
  908   New-build residential estate under construction, house frames and fresh concrete
        slabs, no signage or branding, daylight, landscape 3:2. Min 534x374.
  924   Coloured (oxide) concrete surface, close overhead crop showing colour and texture,
        even daylight, square 1:1. Min 1200x1200.
  925   Stencil-patterned decorative concrete surface, close crop showing the pattern joint
        lines, even daylight, landscape 4:3. Min 600x450.
  926   Stamped concrete surface with a tile or slate pattern, close crop, even daylight,
        square 1:1. Min 554x554.
  956   Aerial or elevated view of a low-density residential subdivision with sealed roads
        and concrete driveways, no identifiable signage, landscape 4:3. Min 906x680.
  1150  Established single-storey brick home from the street, mature front garden, ageing
        concrete driveway, overcast daylight, landscape 3:2. Min 569x368.
  1152  Elevated view of an established low-density residential area, mature trees, mixed
        roof ages, no identifiable signage, landscape 4:3. Min 636x481.
  1185  Concrete vehicle crossing between kerb and property boundary, footpath crossing
        visible, no house number or signage, daylight, landscape 4:3. Min 515x388.
  1186  Large commercial concrete hardstand or car park slab, saw-cut joints visible, no
        branding or signage, daylight, wide landscape 16:9. Min 984x554.
  1187  Row of new-build homes under construction with fresh concrete slabs and driveways,
        no signage, daylight, wide landscape 2:1. Min 645x310.

  MUST NOT APPEAR IN ANY OF THE 16
    identifiable faces; number plates; visible business signage or branding;
    non-Australian architecture, vegetation or road markings; left-hand-drive vehicles;
    snow; competitor branding.
```

### Proposed alt text

One string per image, reused across its pages, with zero geographic assertion and zero implication of
operator authorship.

```text
  226   "Freshly finished residential concrete slab"
  480   "Suburban street with concrete driveways to single-storey homes"
  481   "Broom-finished concrete driveway leading to a single garage"
  482   "Concrete driveway edge and control joint beside a garden bed"
  906   "Excavation of a driveway sub-base before pouring"
  907   "Suburban street showing kerb, footpath and a vehicle crossing"
  908   "New residential estate with recently poured house slabs"
  924   "Coloured oxide concrete surface finish"
  925   "Stencil-patterned decorative concrete surface"
  926   "Stamped concrete surface with a patterned finish"
  956   "Elevated view of a residential subdivision with sealed roads and driveways"
  1150  "Established single-storey home with an ageing concrete driveway"
  1152  "Elevated view of an established residential area"
  1185  "Concrete vehicle crossing between kerb and property boundary"
  1186  "Commercial concrete hardstand with saw-cut joints"
  1187  "New-build homes with recently poured slabs and driveways"

  None says "our", "we", "recent" or any place name.
```

---

## 3. Why the `module` column says NOT ATTRIBUTABLE

§1.1 asks which built module each image sits in, per the Stage 21 crosswalk. **None of them sits in a
consistent module, because they are not subject-matched to content at all.**

Each image rotates through the service-tile grid as generic decoration:

```text
  ATTACHMENT 1020 (a photograph of SOIL) is currently the tile image for:
      " Exposed Aggregate "                  on /concreters-camden-park/
      " Patios & Alfresco in Currans Hill "  on /concreters-currans-hill/
      " Coloured & Decorative in Currans Hill "
      " Concrete Driveways "                 on /concreters-glen-alpine/
      " Concrete Slabs "                     on /concreters-wattle-grove/ and /concreters-leppington/

  ATTACHMENT 924 (coloured concrete) is the tile image for " Concrete Slabs " and " Exposed Aggregate ".
  ATTACHMENT 480 (a streetscape) is the tile image for " Patios & Alfresco " and " Coloured & Decorative ".
```

The pattern holds for all 20. Between 8 and 12 uses per image are plain `image` widgets with no tile title
at all.

**Consequence for the replacement:** this is good news for Phase 2. Because the slots are generic
decoration rather than subject-matched illustration, generic licensed imagery genuinely fits. It is bad
news for the site: a soil photograph captioned "Exposed Aggregate" is wrong twice over.

---

## 4. The current alt text is auto-generated, which is why it asserts geography

```text
  pattern    "<attachment title> in the context of <page title>"
  examples   "Wianamatta shale clay camden in the context of Concreters Camden Park"
             "Oran park1 in the context of Commercial Concreting Narellan"
             "Camden town centre in the context of Broom Finish Concrete"
  distinct strings per image   14-15, one per page
```

The geographic falsehood is inherited from the **attachment title**, which was renamed at Stage 8. Fixing
the filename without fixing the attachment title leaves the alt text asserting the same false place.
**Both must change together**, and both are post-import edits.

---

## 5. FINDINGS OUTSIDE THE BRIEF — three, and the third is the largest

### 5.1 A second and third image making a geological claim

§1.1 says to flag these and not classify them. Flagged, not classified:

```text
  1151  reactive-clay-concreter.jpg    -> reactive-clay-concreter-camden-1151.jpg
  1188  reactive-clay-concreter-1.jpg  -> reactive-clay-concreter-1-camden-1188.jpg
```

Neither has a Victorian place name in its ORIGINAL filename, so neither is in the 20. But the Stage 8
rename **added "camden"** to both, so each now asserts that this is reactive clay *at Camden* — a
site-classification claim about a specific place. Same class of falsity as 1020, different provenance.

**Not classified. Owner direction required.**

### 5.2 A Victorian image asserting a specific NSW watercourse, missed by the count of 20

```text
  1056  davis-creek-tarneit.jpg -> south-creek-drainage-corridor-1056.jpg
```

A Victorian creek presented as the **South Creek drainage corridor**, a specific NSW waterway. It was
excluded from the "20" only because the Stage 24 detector matched suburb names and `south-creek` is a
watercourse, not a suburb. It is the same falsity and appears on 14 pages.

**The count of 20 undercounts by at least one. Owner direction required on 1056.**

### 5.3 55% of all body copy is machine-generated filler

This is the largest finding in this exercise and it is not about images.

```text
  text blocks in the main WXR                1,842
  blocks matching the filler pattern           957   52.0%
  body words total                         171,486
  body words inside filler blocks           94,143   54.9%
  pages affected                                45   of 156
  by class                    ALL 10 service pages, ALL 35 intersection pages
  worst single page                             31   filler blocks
```

Verbatim sample from `/concrete-driveways-south-west-sydney/`, a **published** service page:

```text
  "new-driveway scope records scope boundary; new-driveway scope identifies the record owner.
   new-driveway scope records the exact; new-driveway scope identifies the record owner.
   new-driveway scope cites work included; new-driveway scope keeps the basis explicit."
```

This is not prose. It repeats a slug token at the head of nearly every clause with rotating verb phrases,
and reads as broken to any human within one sentence.

**Why no gate caught it.** Stage 25 measured these pages as among the *most* unique on the site — service
pages 0.756–0.915, intersections 0.652–0.935 — because the filler is different on every page. Uniqueness
measures difference, not sense. A page can be 90% unique and 100% unpublishable.

**Why it matters to this exercise.** Ten of these 45 pages are in the Wave 1 release set. Buying licensed
photography for pages whose body copy is generated word salad is spending in the wrong order.

---

## 6. What Phase 2 would do, on approval

```text
  sources       Unsplash API, Pexels API, Openverse API (commercial-use filter) only
  forbidden     Google Images, Bing, any search-engine scraper
  per slot      5 candidates -> reports/33-image-candidates.csv
  downloads     NONE until specific candidates are approved
  terms         each source's current terms read and the reading date recorded
  attribution   Openverse candidates carry a per-image attribution obligation that
                follows the image onto the page and into the credits
```

**Untouched by Phase 2:** the 47 `REAL_PHOTO_PENDING` slots. Those require genuine photographs of the
operator's own completed work and stay flagged. A licensed stock photo in a "Local Work Completed" module
is the same false claim as a renamed Melbourne photo, just better sourced.

---

## 7. `CONTEXT.md` update and diff

```text
  Stage 33 Phase 1            complete; spec written, nothing downloaded
  Replacement slots           16 REPLACE / 1 REMOVE / 3 HOLD (logo)
  New finding                 1151, 1188 make a Camden reactive-clay claim — flagged, unclassified
  New finding                 1056 asserts the South Creek corridor; the count of 20 undercounts
  New finding                 54.9% of body words are template filler across all service
                              and intersection pages
  Soil image                  no ground-conditions module exists to remove; image removal
                              recommended, section removal not
  Index-ready                 0 of 157 — UNCHANGED
  Launch gate                 NO-GO — UNCHANGED
```

---

## 8. Hash table

```text
  camden-concreting-import.xml                          A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884  MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15  MATCH
  build/stage9-page-manifest.json                       578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42  MATCH
  build/stage8-image-map.json                           0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF  MATCH
  reports/08-image-rename-map.csv                       43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8  MATCH
  CODEX-BUILD-2.1.md                                    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C  MATCH

  6 of 6 MATCH.
```

---

## PHASE 1 GATE

```text
  spec table written                        PASS — 20 rows, reports/33-image-replacement-spec.csv
  briefs describe content, not place        PASS — 16 briefs
  filenames assert nothing geographic       PASS — 16 proposed
  alt text asserts nothing geographic       PASS — 16 proposed, no "our" or "recent"
  soil module removal reported              PASS — reports/33-soil-module-removal.md
  second geological claim flagged           PASS — 1151 and 1188, flagged not classified
  nothing downloaded, searched or generated PASS — 0

  PHASE 1 COMPLETE. PAUSED FOR APPROVAL BEFORE PHASE 2.
```
