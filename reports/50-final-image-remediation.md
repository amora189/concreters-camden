# Final image remediation

Date: 20 August 2026 (Australia/Sydney).

## Outcome

**The owner-approved zero-new-photograph media plan is fully enforced in the reproducible derivative.** Band A is 16/16 decided and applied: 10 GENERIC, 6 UNUSABLE, 0 HOLD. Band B remains 9/9 passing. All 164 exact Report 49 removals were matched and applied without any additional Report 49 slot removal. The public-media gate passes with 55 permitted files and 28 excluded files. No new owner photograph is mandatory under this approved plan.

This closes the image-payload decision/remediation work, not Phase B staging and not the site. Nothing was imported, deployed, published or made indexable. The full preflight remains NO-GO because non-image Gates 7, 12 and 16 fail.

The requested `RUN-BLOCK-02-on-inputs.md` remains absent; the repository’s actual governing run block is `RUN-BLOCK-02.md`, which was used without alteration.

Ground guard: Git reports zero tracked files, so every repository path appears untracked and Git history cannot attribute pre-existing overlapping modifications. The pass therefore used the seven immutable hashes and artifact contracts as its preservation boundary. The derivative’s confirmed starting SHA-256 was `4804CA4E5D2BA23D9AC5CE774454BB4F8ED50E916F6C4090B14F56E5180FDA2B`.

## Owner-approved Band A verdicts

Authority for every row: owner approval dated 20 August 2026 — FINAL IMAGE REMEDIATION prompt; exact Report 49 mapping.

| Tile | Attachment | Source filename | Verdict | Enforced filename and subject-only alt |
|---:|---:|---|---|---|
| 1 | 907 | `camden-town-centre-907.jpg` | **UNUSABLE** | Excluded; every recorded slot removed without replacement |
| 2 | 924 | `coloured-concrete-south-west-sydney-924.png` | **GENERIC** | `coloured-concrete-patio-924.png` — Coloured concrete patio beside a home |
| 3 | 226 | `concretejob2camden-226.jpg` | **GENERIC** | `fresh-concrete-side-yard-slab-226.jpg` — Freshly finished concrete slab in a residential side yard |
| 4 | 1185 | `council-crossing-south-west-sydney-1185.jpg` | **GENERIC** | `dark-concrete-driveway-crossing-1185.jpg` — Dark concrete driveway crossing between a kerb and property |
| 5 | 906 | `driveway-excavation-camden-906.jpg` | **GENERIC** | `residential-site-excavation-906.jpg` — Excavated residential area prepared for concrete work |
| 6 | 1150 | `established-home-mount-annan-1150.jpg` | **GENERIC** | `single-storey-brick-home-driveway-1150.jpg` — Single-storey brick home with a concrete driveway |
| 7 | 1186 | `gregory-hills-commercial-concreting-1186.webp` | **GENERIC** | `commercial-building-concrete-hardstand-1186.webp` — Modern commercial building with a concrete hardstand |
| 8 | 1187 | `leppington-new-estates-1187.jpg` | **UNUSABLE** | Excluded; every recorded slot removed without replacement |
| 9 | 1152 | `mount-annan-established-housing-1152.jpg` | **GENERIC** | `aerial-suburban-park-and-housing-1152.jpg` — Aerial view of a landscaped park surrounded by housing |
| 10 | 908 | `oran-park-growth-estate-908.jpg` | **GENERIC** | `aerial-new-housing-estate-908.jpg` — Aerial view of a developing suburban housing estate |
| 11 | 480 | `oran-park1-480.webp` | **UNUSABLE** | Excluded; every recorded slot removed without replacement |
| 12 | 481 | `oran-park2-481.webp` | **UNUSABLE** | Excluded; every recorded slot removed without replacement |
| 13 | 482 | `oran-park3-482.webp` | **UNUSABLE** | Excluded; every recorded slot removed without replacement |
| 14 | 956 | `south-west-sydney-growth-corridor-956.png` | **UNUSABLE** | Excluded; every recorded slot removed without replacement |
| 15 | 926 | `stamped-concrete-south-west-sydney-926.jpg` | **GENERIC** | `stamped-concrete-driveway-926.jpg` — Stamped concrete driveway beside a brick home |
| 16 | 925 | `stencil-concrete-south-west-sydney-925.webp` | **GENERIC** | `stencilled-concrete-driveway-925.webp` — Stencilled concrete driveway with a block pattern |

Totals: **10 GENERIC + 6 UNUSABLE = 16**. Blank, OK and REPLACE verdicts: **0**.

For all ten GENERIC assets, the derivative attachment title, slug/filename, alt metadata and classic Elementor URL/alt values are subject-only. Typed Elementor references resolve through the remediated attachment record. Their 75 surviving placements exactly equal the 75 Report 49 page/widget/setting placements that say `audit recommends GENERIC`. The public-media gate rejects any additional or missing placement.

## Payload and binary disposition

- Generated derivative: `build/46-active-main-import.xml` — SHA-256 `C1E325576AACB12EB60E6FE5696CA852A6FB60D3FDC95450F3DB947201E406D9`.
- Manifest: 83 provenance rows = 55 RENAME + 28 EXCLUDE + 0 HOLD.
- Public media: 55/55 present; no missing, additional or non-image files.
- Quarantine: 28/28 excluded binaries present under `source-inputs/media-retired/`.
- Band A held directory: zero required HOLD files.
- Duplicate identities 49 and 52 remain distinct and resolve; no byte-duplicate collapse was used.

### Excluded assets

| Attachment | Band | Filename | Authority/disposition |
|---:|---|---|---|
| 159 | D | `chatgpt-image-jul-6-2026-01-52-19-pm-camden-159.png` | D24/D36 retired AI/source-brand attachment;  |
| 177 | D | `cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177.png` | D24/D36 retired AI/source-brand attachment;  |
| 250 | D | `corex-concreters-camden-logo-250.png` | Astra product mark, not a Structure Co asset;  |
| 272 | D | `cropped-chatgpt-image-jul-6-2026-01-52-19-pm-camden-272.png` | D24 and C2PA/AI provenance finding;  |
| 275 | D | `image-placeholder-hero-camden-275.jpeg` | owner-approved Report 49 zero-new-photograph plan; blank placeholder asset; remove every recorded placeholder slot without replacement |
| 276 | D | `image-contact-1-camden-276.jpg` | owner-approved Report 49 zero-new-photograph plan; blank placeholder asset; remove every recorded placeholder slot without replacement |
| 277 | D | `image-placeholder-hero-1-camden-277.jpeg` | owner-approved Report 49 zero-new-photograph plan; blank placeholder asset; remove every recorded placeholder slot without replacement |
| 278 | D | `image-placeholder-about-1-camden-278.jpeg` | owner-approved Report 49 zero-new-photograph plan; blank placeholder asset; remove every recorded placeholder slot without replacement |
| 279 | D | `image-placeholder-about-camden-279.jpeg` | owner-approved Report 49 zero-new-photograph plan; blank placeholder asset; remove every recorded placeholder slot without replacement |
| 280 | B | `image-testemonials-camden-280.jpeg` | owner-recorded Band B verdict; build/45-media-remediation.csv; Remove every slot; do not replace |
| 306 | C | `corex-concreters-camden-logo-306.png` | D18/D36 retired E&T brand attachment; Structure Co replacements are supplied separately; old slot may not survive |
| 307 | C | `corex-concreters-camden-logo-307.png` | D18/D36 retired E&T brand attachment; Structure Co replacements are supplied separately; old slot may not survive |
| 308 | D | `corex-concreters-camden-logo-308.png` | D24 and C2PA/AI provenance finding;  |
| 309 | D | `corex-concreters-camden-logo-309.png` | D24 and C2PA/AI provenance finding;  |
| 323 | D | `about-2-hero-camden-323.jpg` | owner-approved Report 49 zero-new-photograph plan; blank placeholder asset; remove every recorded placeholder slot without replacement |
| 422 | C | `corex-concreters-camden-logo-422.png` | D18/D36 retired E&T brand attachment; Structure Co replacements are supplied separately; old slot may not survive |
| 468 | D | `corex-concreters-camden-logo-468.png` | E&T Concreters Melbourne wordmark; duplicate contract requires pair treatment;  |
| 469 | C | `corex-concreters-camden-logo-469.png` | D18/D36 retired E&T brand attachment; Structure Co replacements are supplied separately; old slot may not survive |
| 471 | D | `corex-concreters-camden-logo-471.png` | E&T Concreters Melbourne wordmark; duplicate contract requires pair treatment;  |
| 472 | C | `corex-concreters-camden-logo-472.png` | D18/D36 retired E&T brand attachment; Structure Co replacements are supplied separately; old slot may not survive |
| 480 | A | `oran-park1-480.webp` | owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping; remove public slots without replacement |
| 481 | A | `oran-park2-481.webp` | owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping; remove public slots without replacement |
| 482 | A | `oran-park3-482.webp` | owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping; remove public slots without replacement |
| 907 | A | `camden-town-centre-907.jpg` | owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping; remove public slots without replacement |
| 956 | A | `south-west-sydney-growth-corridor-956.png` | owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping; remove public slots without replacement |
| 1020 | D | `wianamatta-shale-clay-camden-1020.jpg` | D19 removes the Tarneit soil photograph and retains its containing sections;  |
| 1067 | B | `verified-badge-e1784545689665-camden-1067.avif` | owner-recorded Band B verdict; build/45-media-remediation.csv; Remove every slot; do not replace or substitute another badge |
| 1187 | A | `leppington-new-estates-1187.jpg` | owner approval dated 20 August 2026; exact Report 49 UNUSABLE mapping; remove public slots without replacement |

### Generic assets and their exact surviving reuse placements

Each placement below is recorded as `/page-slug/ — widget:setting`. All are decorative and non-evidential. They may not assert location, Structure Co work, a customer/testimonial, local premises, equipment ownership or work by the eventual NSW operator.

| Attachment | Band | Remediated file | Subject-only alt | Count | Placements |
|---:|---|---|---|---:|---|
| 17 | D | `concrete-project-detail-17.jpg` | Concrete project detail | 7 | /concreters-catherine-field/ — a86c195:image<br>/concreters-edmondson-park/ — e6c2ed7:image<br>/concreters-gregory-hills/ — 7bcc8c0:image<br>/concreters-menangle-park/ — f36a8f3:image<br>/concreters-prestons/ — 516941f:image<br>/decorative-concrete-south-west-sydney/ — 0864f76:image<br>/homepage/ — e8c038a:image |
| 18 | D | `concrete-project-detail-18.jpg` | Concrete project detail | 6 | /concreters-catherine-field/ — 516941f:image<br>/concreters-edmondson-park/ — af8ef50:image<br>/concreters-menangle-park/ — af91c52:image<br>/concreters-menangle-park/ — d06ebf3:image<br>/concreters-prestons/ — f36a8f3:image<br>/homepage/ — 8839302:image |
| 19 | D | `concrete-project-detail-19.jpg` | Concrete project detail | 6 | /concreters-catherine-field/ — f36a8f3:image<br>/concreters-edmondson-park/ — 2eb88ab:image<br>/concreters-menangle-park/ — e6c2ed7:image<br>/concreters-prestons/ — af91c52:image<br>/concreters-prestons/ — d06ebf3:image<br>/homepage/ — ea0736d:image |
| 46 | B | `exposed-aggregate-front-paths-46.webp` | Exposed aggregate paths leading to a home's front entry | 7 | /concreters-catherine-field/ — af91c52:image<br>/concreters-catherine-field/ — d06ebf3:image<br>/concreters-edmondson-park/ — 0ca264b:image<br>/concreters-menangle/ — a86c195:image<br>/concreters-prestons/ — e6c2ed7:image<br>/homepage/ — 0c5d989:image<br>/homepage/ — da41d16:image |
| 47 | B | `fresh-concrete-backyard-slab-47.webp` | Freshly poured concrete slab beside a two-storey home | 8 | /concrete-patios-south-west-sydney/ — 2f9d916e:image<br>/concreters-catherine-field/ — e6c2ed7:image<br>/concreters-edmondson-park/ — 7bcc8c0:image<br>/concreters-harrington-park/ — a86c195:image<br>/concreters-menangle/ — 516941f:image<br>/concreters-raby/ — a86c195:image<br>/homepage/ — b751729:image<br>/shed-and-garage-slabs-south-west-sydney/ — ae41c11:image |
| 48 | B | `exposed-aggregate-residential-driveway-48.webp` | Exposed aggregate driveway leading to a carport | 7 | /concrete-patios-south-west-sydney/ — 54b2712e:image<br>/concreters-catherine-field/ — af8ef50:image<br>/concreters-harrington-park/ — 516941f:image<br>/concreters-menangle/ — f36a8f3:image<br>/concreters-raby/ — 516941f:image<br>/homepage/ — 1542538:image<br>/shed-and-garage-slabs-south-west-sydney/ — 2fc74005:image |
| 49 | B | `fresh-concrete-pool-surround-49.webp` | Freshly poured concrete beside a swimming pool | 8 | /concrete-patios-south-west-sydney/ — 282eb1d0:image<br>/concreters-appin/ — a86c195:image<br>/concreters-catherine-field/ — 2eb88ab:image<br>/concreters-harrington-park/ — f36a8f3:image<br>/concreters-menangle/ — af91c52:image<br>/concreters-menangle/ — d06ebf3:image<br>/concreters-raby/ — f36a8f3:image<br>/shed-and-garage-slabs-south-west-sydney/ — 641391f1:image |
| 50 | D | `exposed-aggregate-concrete-50.jpg` | Exposed aggregate concrete | 69 | /concrete-patios-south-west-sydney/ — 51342c0b:image<br>/concreters-appin/ — 516941f:image<br>/concreters-appin/ — 7c2526d7:background_image<br>/concreters-austral/ — 7c2526d7:background_image<br>/concreters-bargo/ — 7c2526d7:background_image<br>/concreters-bradbury/ — 7c2526d7:background_image<br>/concreters-bringelly/ — 7c2526d7:background_image<br>/concreters-camden-park/ — 7c2526d7:background_image<br>/concreters-camden-south/ — 7c2526d7:background_image<br>/concreters-campbelltown/ — 7c2526d7:background_image<br>/concreters-carnes-hill/ — 7c2526d7:background_image<br>/concreters-casula/ — 7c2526d7:background_image<br>/concreters-catherine-field/ — 0ca264b:image<br>/concreters-catherine-field/ — 7c2526d7:background_image<br>/concreters-cawdor/ — 7c2526d7:background_image<br>/concreters-cecil-hills/ — 7c2526d7:background_image<br>/concreters-cecil-park/ — 7c2526d7:background_image<br>/concreters-chipping-norton/ — 7c2526d7:background_image<br>/concreters-cobbitty/ — 7c2526d7:background_image<br>/concreters-currans-hill/ — 7c2526d7:background_image<br>/concreters-douglas-park/ — 7c2526d7:background_image<br>/concreters-eagle-vale/ — 7c2526d7:background_image<br>/concreters-edmondson-park/ — 7c2526d7:background_image<br>/concreters-elderslie/ — 7c2526d7:background_image<br>/concreters-elizabeth-hills/ — 7c2526d7:background_image<br>/concreters-ellis-lane/ — 7c2526d7:background_image<br>/concreters-gilead/ — 7c2526d7:background_image<br>/concreters-gledswood-hills/ — 7c2526d7:background_image<br>/concreters-glen-alpine/ — 7c2526d7:background_image<br>/concreters-glenfield/ — 7c2526d7:background_image<br>/concreters-grasmere/ — 7c2526d7:background_image<br>/concreters-gregory-hills/ — 7c2526d7:background_image<br>/concreters-harrington-park/ — 7c2526d7:background_image<br>/concreters-harrington-park/ — af91c52:image<br>/concreters-harrington-park/ — d06ebf3:image<br>/concreters-horningsea-park/ — 7c2526d7:background_image<br>/concreters-hoxton-park/ — 7c2526d7:background_image<br>/concreters-ingleburn/ — 7c2526d7:background_image<br>/concreters-kemps-creek/ — 7c2526d7:background_image<br>/concreters-kirkham/ — 7c2526d7:background_image<br>/concreters-len-waters-estate/ — 7c2526d7:background_image<br>/concreters-leppington/ — 7c2526d7:background_image<br>/concreters-leumeah/ — 7c2526d7:background_image<br>/concreters-macquarie-fields/ — 7c2526d7:background_image<br>/concreters-menangle-park/ — 7c2526d7:background_image<br>/concreters-menangle/ — 7c2526d7:background_image<br>/concreters-menangle/ — e6c2ed7:image<br>/concreters-middleton-grange/ — 7c2526d7:background_image<br>/concreters-minto/ — 7c2526d7:background_image<br>/concreters-moorebank/ — 7c2526d7:background_image<br>/concreters-mount-annan/ — 7c2526d7:background_image<br>/concreters-narellan-vale/ — 7c2526d7:background_image<br>/concreters-narellan/ — 7c2526d7:background_image<br>/concreters-oran-park/ — 7c2526d7:background_image<br>/concreters-picton/ — 7c2526d7:background_image<br>/concreters-prestons/ — 7c2526d7:background_image<br>/concreters-raby/ — 7c2526d7:background_image<br>/concreters-raby/ — af91c52:image<br>/concreters-raby/ — d06ebf3:image<br>/concreters-rossmore/ — 7c2526d7:background_image<br>/concreters-smeaton-grange/ — 7c2526d7:background_image<br>/concreters-spring-farm/ — 7c2526d7:background_image<br>/concreters-tahmoor/ — 7c2526d7:background_image<br>/concreters-the-oaks/ — 7c2526d7:background_image<br>/concreters-theresa-park/ — 7c2526d7:background_image<br>/concreters-wattle-grove/ — 7c2526d7:background_image<br>/concreters-west-hoxton/ — 7c2526d7:background_image<br>/concreters-wilton/ — 7c2526d7:background_image<br>/shed-and-garage-slabs-south-west-sydney/ — 4a3b804f:image |
| 51 | B | `concrete-stepping-slabs-garden-path-51.webp` | Concrete stepping slabs laid through a garden | 7 | /concreters-appin/ — f36a8f3:image<br>/concreters-catherine-field/ — 7bcc8c0:image<br>/concreters-elderslie/ — a86c195:image<br>/concreters-harrington-park/ — e6c2ed7:image<br>/concreters-middleton-grange/ — a86c195:image<br>/concreters-raby/ — e6c2ed7:image<br>/shed-and-garage-slabs-south-west-sydney/ — 50151b3b:image |
| 52 | B | `fresh-concrete-pool-surround-52.webp` | Freshly poured concrete beside a swimming pool | 7 | /concreters-appin/ — af91c52:image<br>/concreters-appin/ — d06ebf3:image<br>/concreters-elderslie/ — 516941f:image<br>/concreters-harrington-park/ — af8ef50:image<br>/concreters-middleton-grange/ — 516941f:image<br>/concreters-rossmore/ — a86c195:image<br>/shed-and-garage-slabs-south-west-sydney/ — 899b5bf:image |
| 53 | D | `patiosandpathways-53.webp` | Patiosandpathways | 6 | /concreters-appin/ — e6c2ed7:image<br>/concreters-elderslie/ — f36a8f3:image<br>/concreters-harrington-park/ — 2eb88ab:image<br>/concreters-middleton-grange/ — f36a8f3:image<br>/concreters-rossmore/ — 516941f:image<br>/shed-and-garage-slabs-south-west-sydney/ — 18063b5:image |
| 54 | D | `coloured-detailed-concrete-54.jpg` | Coloured detailed concrete | 8 | /concreters-austral/ — a86c195:image<br>/concreters-elderslie/ — af91c52:image<br>/concreters-elderslie/ — d06ebf3:image<br>/concreters-harrington-park/ — 0ca264b:image<br>/concreters-middleton-grange/ — af91c52:image<br>/concreters-middleton-grange/ — d06ebf3:image<br>/concreters-rossmore/ — f36a8f3:image<br>/shed-and-garage-slabs-south-west-sydney/ — aab2150:image |
| 55 | D | `patiosconcrete-55.jpg` | Patiosconcrete | 8 | /concreters-austral/ — 516941f:image<br>/concreters-cawdor/ — a86c195:image<br>/concreters-elderslie/ — e6c2ed7:image<br>/concreters-harrington-park/ — 7bcc8c0:image<br>/concreters-middleton-grange/ — e6c2ed7:image<br>/concreters-rossmore/ — af91c52:image<br>/concreters-rossmore/ — d06ebf3:image<br>/shed-and-garage-slabs-south-west-sydney/ — 8aac8e0:image |
| 121 | D | `reinforcedheavydutyconcrete-121.webp` | Reinforcedheavydutyconcrete | 5 | /concreters-austral/ — f36a8f3:image<br>/concreters-cawdor/ — 516941f:image<br>/concreters-elderslie/ — af8ef50:image<br>/concreters-minto/ — a86c195:image<br>/concreters-rossmore/ — e6c2ed7:image |
| 144 | D | `paths-and-pathwaysconcrete-144.jpg` | Paths and pathwaysconcrete | 6 | /concreters-austral/ — af91c52:image<br>/concreters-austral/ — d06ebf3:image<br>/concreters-cawdor/ — f36a8f3:image<br>/concreters-elderslie/ — 2eb88ab:image<br>/concreters-minto/ — 516941f:image<br>/concreters-smeaton-grange/ — a86c195:image |
| 145 | D | `patiosandalfrescoconcrete-145.jpg` | Patiosandalfrescoconcrete | 6 | /concreters-austral/ — e6c2ed7:image<br>/concreters-cawdor/ — af91c52:image<br>/concreters-cawdor/ — d06ebf3:image<br>/concreters-elderslie/ — 0ca264b:image<br>/concreters-minto/ — f36a8f3:image<br>/concreters-smeaton-grange/ — 516941f:image |
| 146 | D | `concretepoolsurronds-146.jpg` | Concretepoolsurronds | 7 | /concreters-austral/ — af8ef50:image<br>/concreters-cawdor/ — e6c2ed7:image<br>/concreters-elderslie/ — 7bcc8c0:image<br>/concreters-horningsea-park/ — a86c195:image<br>/concreters-minto/ — af91c52:image<br>/concreters-minto/ — d06ebf3:image<br>/concreters-smeaton-grange/ — f36a8f3:image |
| 166 | D | `shedslabconcrete-166.jpg` | Shedslabconcrete | 6 | /concreters-austral/ — 2eb88ab:image<br>/concreters-cecil-hills/ — a86c195:image<br>/concreters-horningsea-park/ — 516941f:image<br>/concreters-minto/ — e6c2ed7:image<br>/concreters-smeaton-grange/ — af91c52:image<br>/concreters-smeaton-grange/ — d06ebf3:image |
| 167 | D | `garage-slabs-concrete-167.jpg` | Garage slabs concrete | 5 | /concreters-austral/ — 0ca264b:image<br>/concreters-cecil-hills/ — 516941f:image<br>/concreters-horningsea-park/ — f36a8f3:image<br>/concreters-moorebank/ — a86c195:image<br>/concreters-smeaton-grange/ — e6c2ed7:image |
| 168 | D | `extension-and-floor-slabs-concrete-168.jpg` | Extension and floor slabs concrete | 6 | /concreters-austral/ — 7bcc8c0:image<br>/concreters-cecil-hills/ — f36a8f3:image<br>/concreters-horningsea-park/ — af91c52:image<br>/concreters-horningsea-park/ — d06ebf3:image<br>/concreters-moorebank/ — 516941f:image<br>/concreters-spring-farm/ — a86c195:image |
| 181 | D | `side-access-paths-concrete-181.jpg` | Side access paths concrete | 6 | /concreters-cecil-hills/ — af91c52:image<br>/concreters-cecil-hills/ — d06ebf3:image<br>/concreters-elizabeth-hills/ — a86c195:image<br>/concreters-horningsea-park/ — e6c2ed7:image<br>/concreters-moorebank/ — f36a8f3:image<br>/concreters-spring-farm/ — 516941f:image |
| 182 | D | `concrete-garden-paths-and-connecting-paths-concrete-182.jpg` | Concrete garden paths and connecting paths concrete | 6 | /concreters-cecil-hills/ — e6c2ed7:image<br>/concreters-elizabeth-hills/ — 516941f:image<br>/concreters-hoxton-park/ — a86c195:image<br>/concreters-moorebank/ — af91c52:image<br>/concreters-moorebank/ — d06ebf3:image<br>/concreters-spring-farm/ — f36a8f3:image |
| 183 | D | `front-and-entry-paths-concrete-183.jpg` | Front and entry paths concrete | 6 | /concreters-cecil-park/ — a86c195:image<br>/concreters-elizabeth-hills/ — f36a8f3:image<br>/concreters-hoxton-park/ — 516941f:image<br>/concreters-moorebank/ — e6c2ed7:image<br>/concreters-spring-farm/ — af91c52:image<br>/concreters-spring-farm/ — d06ebf3:image |
| 184 | D | `accessible-paths-concrete-184.jpg` | Accessible paths concrete | 8 | /concreters-bargo/ — a86c195:image<br>/concreters-cecil-park/ — 516941f:image<br>/concreters-elizabeth-hills/ — af91c52:image<br>/concreters-elizabeth-hills/ — d06ebf3:image<br>/concreters-hoxton-park/ — f36a8f3:image<br>/concreters-mount-annan/ — a86c195:image<br>/concreters-spring-farm/ — e6c2ed7:image<br>/exposed-aggregate-south-west-sydney/ — ac3ac3a:image |
| 226 | A | `fresh-concrete-side-yard-slab-226.jpg` | Freshly finished concrete slab in a residential side yard | 8 | /concreters-bargo/ — 516941f:image<br>/concreters-cecil-park/ — f36a8f3:image<br>/concreters-elizabeth-hills/ — e6c2ed7:image<br>/concreters-hoxton-park/ — af91c52:image<br>/concreters-hoxton-park/ — d06ebf3:image<br>/concreters-mount-annan/ — 516941f:image<br>/concreters-spring-farm/ — af8ef50:image<br>/exposed-aggregate-south-west-sydney/ — 34c11481:image |
| 227 | D | `backyard-patio-concreter-227.jpg` | Backyard patio concreter | 9 | /concrete-driveway-replacement-south-west-sydney/ — fbc5b30:image<br>/concreters-bargo/ — f36a8f3:image<br>/concreters-cecil-park/ — af91c52:image<br>/concreters-cecil-park/ — d06ebf3:image<br>/concreters-ellis-lane/ — a86c195:image<br>/concreters-hoxton-park/ — e6c2ed7:image<br>/concreters-mount-annan/ — f36a8f3:image<br>/concreters-spring-farm/ — 2eb88ab:image<br>/exposed-aggregate-south-west-sydney/ — 280275a7:image |
| 228 | B | `fresh-concrete-side-yard-slab-228.jpg` | Freshly poured concrete slab along a side boundary | 10 | /concrete-driveway-replacement-south-west-sydney/ — d91bcc2:image<br>/concreters-bargo/ — af91c52:image<br>/concreters-bargo/ — d06ebf3:image<br>/concreters-cecil-park/ — e6c2ed7:image<br>/concreters-ellis-lane/ — 516941f:image<br>/concreters-ingleburn/ — a86c195:image<br>/concreters-mount-annan/ — af91c52:image<br>/concreters-mount-annan/ — d06ebf3:image<br>/concreters-spring-farm/ — 0ca264b:image<br>/exposed-aggregate-south-west-sydney/ — 2e70a00:image |
| 609 | D | `exposed-aggregate-residential-driveway-609.jpg` | Exposed aggregate driveway leading to a home | 8 | /concrete-driveways-south-west-sydney/ — 5e63315:image<br>/concreters-bringelly/ — e6c2ed7:image<br>/concreters-cobbitty/ — af8ef50:image<br>/concreters-gledswood-hills/ — f36a8f3:image<br>/concreters-kirkham/ — 516941f:image<br>/concreters-narellan-vale/ — f36a8f3:image<br>/concreters-the-oaks/ — 516941f:image<br>/homepage/ — 306c538:image |
| 906 | A | `residential-site-excavation-906.jpg` | Excavated residential area prepared for concrete work | 9 | /concrete-driveways-south-west-sydney/ — 7c2901e:image<br>/concreters-bringelly/ — af8ef50:image<br>/concreters-cobbitty/ — 2eb88ab:image<br>/concreters-gledswood-hills/ — af91c52:image<br>/concreters-gledswood-hills/ — d06ebf3:image<br>/concreters-kirkham/ — f36a8f3:image<br>/concreters-narellan-vale/ — af91c52:image<br>/concreters-narellan-vale/ — d06ebf3:image<br>/concreters-the-oaks/ — f36a8f3:image |
| 908 | A | `aerial-new-housing-estate-908.jpg` | Aerial view of a developing suburban housing estate | 7 | /concrete-driveways-south-west-sydney/ — 7886294:image<br>/concreters-bringelly/ — 0ca264b:image<br>/concreters-cobbitty/ — 7bcc8c0:image<br>/concreters-gledswood-hills/ — af8ef50:image<br>/concreters-kirkham/ — e6c2ed7:image<br>/concreters-narellan/ — a86c195:image<br>/concreters-the-oaks/ — e6c2ed7:image |
| 909 | D | `control-joints-and-cracks-909.jpg` | Control joints and cracks | 6 | /concrete-driveways-south-west-sydney/ — 154c6cb:image<br>/concreters-bringelly/ — 7bcc8c0:image<br>/concreters-gledswood-hills/ — 2eb88ab:image<br>/concreters-len-waters-estate/ — a86c195:image<br>/concreters-narellan/ — 516941f:image<br>/concreters-theresa-park/ — a86c195:image |
| 924 | A | `coloured-concrete-patio-924.png` | Coloured concrete patio beside a home | 6 | /commercial-concreting-south-west-sydney/ — ae41c11:image<br>/concrete-driveways-south-west-sydney/ — 51a4a3e:image<br>/concreters-gledswood-hills/ — 0ca264b:image<br>/concreters-len-waters-estate/ — 516941f:image<br>/concreters-narellan/ — f36a8f3:image<br>/concreters-theresa-park/ — 516941f:image |
| 925 | A | `stencilled-concrete-driveway-925.webp` | Stencilled concrete driveway with a block pattern | 6 | /commercial-concreting-south-west-sydney/ — 2fc74005:image<br>/concreters-gledswood-hills/ — 7bcc8c0:image<br>/concreters-len-waters-estate/ — f36a8f3:image<br>/concreters-narellan/ — af91c52:image<br>/concreters-narellan/ — d06ebf3:image<br>/concreters-theresa-park/ — f36a8f3:image |
| 926 | A | `stamped-concrete-driveway-926.jpg` | Stamped concrete driveway beside a brick home | 7 | /commercial-concreting-south-west-sydney/ — 641391f1:image<br>/concreters-currans-hill/ — a86c195:image<br>/concreters-len-waters-estate/ — af91c52:image<br>/concreters-len-waters-estate/ — d06ebf3:image<br>/concreters-narellan/ — e6c2ed7:image<br>/concreters-theresa-park/ — af91c52:image<br>/concreters-theresa-park/ — d06ebf3:image |
| 927 | D | `honed-and-polished-concrete-927.webp` | Honed and polished concrete | 6 | /commercial-concreting-south-west-sydney/ — 4a3b804f:image<br>/concreters-camden-park/ — a86c195:image<br>/concreters-currans-hill/ — 516941f:image<br>/concreters-len-waters-estate/ — e6c2ed7:image<br>/concreters-narellan/ — af8ef50:image<br>/concreters-theresa-park/ — e6c2ed7:image |
| 1056 | D | `aerial-waterway-residential-area-1056.jpg` | Aerial view of a waterway beside a residential area | 8 | /commercial-concreting-south-west-sydney/ — 18063b5:image<br>/concreters-camden-park/ — af91c52:image<br>/concreters-camden-park/ — d06ebf3:image<br>/concreters-currans-hill/ — e6c2ed7:image<br>/concreters-glen-alpine/ — 516941f:image<br>/concreters-leppington/ — f36a8f3:image<br>/concreters-narellan/ — 7bcc8c0:image<br>/concreters-wattle-grove/ — f36a8f3:image |
| 1065 | D | `concrete-slabs-1065.jpg` | Concrete slabs | 8 | /commercial-concreting-south-west-sydney/ — aab2150:image<br>/concreters-camden-park/ — e6c2ed7:image<br>/concreters-currans-hill/ — af8ef50:image<br>/concreters-glen-alpine/ — f36a8f3:image<br>/concreters-leppington/ — af91c52:image<br>/concreters-leppington/ — d06ebf3:image<br>/concreters-wattle-grove/ — af91c52:image<br>/concreters-wattle-grove/ — d06ebf3:image |
| 1066 | D | `pouring-a-concrete-slab-1066.jpg` | Pouring a concrete slab | 7 | /commercial-concreting-south-west-sydney/ — 8aac8e0:image<br>/concreters-camden-south/ — a86c195:image<br>/concreters-currans-hill/ — 2eb88ab:image<br>/concreters-glen-alpine/ — af91c52:image<br>/concreters-glen-alpine/ — d06ebf3:image<br>/concreters-leppington/ — e6c2ed7:image<br>/concreters-wattle-grove/ — e6c2ed7:image |
| 1068 | D | `what-is-a-concrete-slab-1068.jpg` | What is a concrete slab | 6 | /concreters-camden-south/ — f36a8f3:image<br>/concreters-currans-hill/ — 7bcc8c0:image<br>/concreters-glenfield/ — a86c195:image<br>/concreters-leppington/ — 2eb88ab:image<br>/concreters-oran-park/ — a86c195:image<br>/concreters-west-hoxton/ — 516941f:image |
| 1109 | D | `what-is-exposed-aggregate-1109.jpg` | What is exposed aggregate | 7 | /concrete-slabs-south-west-sydney/ — ae41c11:image<br>/concreters-camden-south/ — af91c52:image<br>/concreters-camden-south/ — d06ebf3:image<br>/concreters-glenfield/ — 516941f:image<br>/concreters-leppington/ — 0ca264b:image<br>/concreters-oran-park/ — 516941f:image<br>/concreters-west-hoxton/ — f36a8f3:image |
| 1150 | A | `single-storey-brick-home-driveway-1150.jpg` | Single-storey brick home with a concrete driveway | 7 | /concrete-slabs-south-west-sydney/ — 2fc74005:image<br>/concreters-camden-south/ — e6c2ed7:image<br>/concreters-glenfield/ — f36a8f3:image<br>/concreters-leppington/ — 7bcc8c0:image<br>/concreters-oran-park/ — f36a8f3:image<br>/concreters-west-hoxton/ — af91c52:image<br>/concreters-west-hoxton/ — d06ebf3:image |
| 1151 | D | `dry-cracked-ground-1151.jpg` | Dry cracked ground surface | 7 | /concrete-slabs-south-west-sydney/ — 641391f1:image<br>/concreters-campbelltown/ — a86c195:image<br>/concreters-glenfield/ — af91c52:image<br>/concreters-glenfield/ — d06ebf3:image<br>/concreters-oran-park/ — af91c52:image<br>/concreters-oran-park/ — d06ebf3:image<br>/concreters-west-hoxton/ — e6c2ed7:image |
| 1152 | A | `aerial-suburban-park-and-housing-1152.jpg` | Aerial view of a landscaped park surrounded by housing | 6 | /concrete-slabs-south-west-sydney/ — 4a3b804f:image<br>/concreters-campbelltown/ — 516941f:image<br>/concreters-douglas-park/ — a86c195:image<br>/concreters-glenfield/ — e6c2ed7:image<br>/concreters-oran-park/ — e6c2ed7:image<br>/concreters-wilton/ — a86c195:image |
| 1153 | D | `concrete-vehicle-crossing-1153.jpg` | Concrete vehicle crossing between a kerb and property boundary | 6 | /concrete-slabs-south-west-sydney/ — 50151b3b:image<br>/concreters-campbelltown/ — f36a8f3:image<br>/concreters-douglas-park/ — 516941f:image<br>/concreters-grasmere/ — a86c195:image<br>/concreters-oran-park/ — af8ef50:image<br>/concreters-wilton/ — 516941f:image |
| 1185 | A | `dark-concrete-driveway-crossing-1185.jpg` | Dark concrete driveway crossing between a kerb and property | 9 | /concrete-paths-south-west-sydney/ — 34b1791a:image<br>/concrete-slabs-south-west-sydney/ — 899b5bf:image<br>/concreters-campbelltown/ — af91c52:image<br>/concreters-campbelltown/ — d06ebf3:image<br>/concreters-douglas-park/ — f36a8f3:image<br>/concreters-grasmere/ — 516941f:image<br>/concreters-leumeah/ — a86c195:image<br>/concreters-oran-park/ — 2eb88ab:image<br>/concreters-wilton/ — f36a8f3:image |
| 1186 | A | `commercial-building-concrete-hardstand-1186.webp` | Modern commercial building with a concrete hardstand | 10 | /concrete-paths-south-west-sydney/ — 6fbeb295:image<br>/concrete-slabs-south-west-sydney/ — 18063b5:image<br>/concreters-campbelltown/ — e6c2ed7:image<br>/concreters-douglas-park/ — af91c52:image<br>/concreters-douglas-park/ — d06ebf3:image<br>/concreters-grasmere/ — f36a8f3:image<br>/concreters-leumeah/ — 516941f:image<br>/concreters-oran-park/ — 0ca264b:image<br>/concreters-wilton/ — af91c52:image<br>/concreters-wilton/ — d06ebf3:image |
| 1188 | D | `dry-cracked-ground-1188.jpg` | Dry cracked ground surface | 7 | /concrete-paths-south-west-sydney/ — 211e758d:image<br>/concrete-slabs-south-west-sydney/ — 8aac8e0:image<br>/concreters-carnes-hill/ — 516941f:image<br>/concreters-eagle-vale/ — a86c195:image<br>/concreters-grasmere/ — e6c2ed7:image<br>/concreters-leumeah/ — af91c52:image<br>/concreters-leumeah/ — d06ebf3:image |
| 1230 | D | `shrinkage-cracks-1230.jpg` | Shrinkage cracks | 4 | /concreters-carnes-hill/ — f36a8f3:image<br>/concreters-eagle-vale/ — 516941f:image<br>/concreters-gregory-hills/ — a86c195:image<br>/concreters-leumeah/ — e6c2ed7:image |
| 1231 | D | `settlement-cracks-1231.jpg` | Settlement cracks | 5 | /concreters-carnes-hill/ — af91c52:image<br>/concreters-carnes-hill/ — d06ebf3:image<br>/concreters-eagle-vale/ — f36a8f3:image<br>/concreters-gregory-hills/ — 516941f:image<br>/concreters-macquarie-fields/ — a86c195:image |
| 1232 | D | `heave-cracks-1232.jpg` | Heave cracks | 6 | /concreters-carnes-hill/ — e6c2ed7:image<br>/concreters-eagle-vale/ — af91c52:image<br>/concreters-eagle-vale/ — d06ebf3:image<br>/concreters-gregory-hills/ — f36a8f3:image<br>/concreters-macquarie-fields/ — 516941f:image<br>/concreters-picton/ — a86c195:image |
| 1233 | D | `structural-cracks-1233.jpg` | Structural cracks | 6 | /concreters-casula/ — a86c195:image<br>/concreters-eagle-vale/ — e6c2ed7:image<br>/concreters-gregory-hills/ — af91c52:image<br>/concreters-gregory-hills/ — d06ebf3:image<br>/concreters-macquarie-fields/ — f36a8f3:image<br>/concreters-picton/ — 516941f:image |
| 1345 | D | `concrete-sealing-1345.jpg` | Concrete sealing | 7 | /concreters-casula/ — 516941f:image<br>/concreters-edmondson-park/ — a86c195:image<br>/concreters-gregory-hills/ — e6c2ed7:image<br>/concreters-macquarie-fields/ — af91c52:image<br>/concreters-macquarie-fields/ — d06ebf3:image<br>/concreters-picton/ — f36a8f3:image<br>/decorative-concrete-south-west-sydney/ — 1ec60b61:image |
| 1359 | D | `concrete-driveway-cracks-1359.jpg` | Concrete driveway cracks | 7 | /concreters-casula/ — f36a8f3:image<br>/concreters-edmondson-park/ — 516941f:image<br>/concreters-gregory-hills/ — af8ef50:image<br>/concreters-macquarie-fields/ — e6c2ed7:image<br>/concreters-picton/ — af91c52:image<br>/concreters-picton/ — d06ebf3:image<br>/decorative-concrete-south-west-sydney/ — 262de5b8:image |
| 1361 | D | `concrete-driveway-cracks-1-1361.jpg` | Concrete driveway cracks 1 | 7 | /concreters-casula/ — af91c52:image<br>/concreters-casula/ — d06ebf3:image<br>/concreters-edmondson-park/ — f36a8f3:image<br>/concreters-gregory-hills/ — 2eb88ab:image<br>/concreters-menangle-park/ — a86c195:image<br>/concreters-picton/ — e6c2ed7:image<br>/decorative-concrete-south-west-sydney/ — 49a81d78:image |
| 1362 | D | `concrete-driveway-cracks-2-1362.jpg` | Concrete driveway cracks 2 | 7 | /concreters-casula/ — e6c2ed7:image<br>/concreters-edmondson-park/ — af91c52:image<br>/concreters-edmondson-park/ — d06ebf3:image<br>/concreters-gregory-hills/ — 0ca264b:image<br>/concreters-menangle-park/ — 516941f:image<br>/concreters-prestons/ — a86c195:image<br>/decorative-concrete-south-west-sydney/ — 2cdfdf10:image |

## All 164 owner-authorised slot removals

The transformer matches requirement ID, page slug, top-level section, widget, setting and attachment ID. A missing, additional or differently mapped slot fails regeneration. The exact category arithmetic is 45 D32 whole-section + 45 blank-placeholder + 3 empty-testimonial + 21 other-prohibited-direct + 50 Band-A-UNUSABLE = **164**.

Six pre-existing D36 retired-brand page slots (attachment 306 ×5 and 307 ×1) remain separately held for supplied Structure Co wordmark replacement at an eventual authorised import. They are not counted as additional Report 49 removals.

| Requirement | Category | Page | Section | Widget:setting | Attachment |
|---|---|---|---|---|---:|
| IMG-0009 | empty testimonial | `/homepage/` | `7fc5ce03` | `5a4a4815:testimonial_image` | none |
| IMG-0010 | empty testimonial | `/homepage/` | `7fc5ce03` | `16805a15:testimonial_image` | none |
| IMG-0011 | empty testimonial | `/homepage/` | `7fc5ce03` | `51fc6392:testimonial_image` | none |
| IMG-0012 | other prohibited direct | `/concrete-driveways-south-west-sydney/` | `5140093` | `fbc5b30:image` | 280 |
| IMG-0013 | blank placeholder | `/concrete-driveways-south-west-sydney/` | `f4f418c` | `d91bcc2:image` | 323 |
| IMG-0014 | Band A UNUSABLE | `/concrete-driveways-south-west-sydney/` | `b61f1c2` | `104d481:image` | 480 |
| IMG-0015 | Band A UNUSABLE | `/concrete-driveways-south-west-sydney/` | `a2970f7` | `620b9f2:image` | 481 |
| IMG-0016 | Band A UNUSABLE | `/concrete-driveways-south-west-sydney/` | `a32399d` | `015aff8:image` | 482 |
| IMG-0019 | Band A UNUSABLE | `/concrete-driveways-south-west-sydney/` | `a089da8` | `ae99959:image` | 907 |
| IMG-0027 | blank placeholder | `/exposed-aggregate-south-west-sydney/` | `356b1e76` | `47d78a35:image` | 275 |
| IMG-0035 | Band A UNUSABLE | `/concrete-slabs-south-west-sydney/` | `43f7482` | `aab2150:image` | 1187 |
| IMG-0039 | Band A UNUSABLE | `/concrete-paths-south-west-sydney/` | `141fb611` | `4c0594f2:image` | 1187 |
| IMG-0048 | Band A UNUSABLE | `/concreters-leppington/` | `9e36728` | `a86c195:image` | 956 |
| IMG-0049 | other prohibited direct | `/concreters-leppington/` | `9e36728` | `516941f:image` | 1020 |
| IMG-0054 | other prohibited direct | `/concreters-leppington/` | `40d980a` | `af8ef50:image` | 1067 |
| IMG-0058 | D32 whole-section | `/concreters-leppington/` | `36efc778` | `0424a72:image` | 1151 |
| IMG-0059 | D32 whole-section | `/concreters-leppington/` | `36efc778` | `4195f9b:image` | 1152 |
| IMG-0060 | D32 whole-section | `/concreters-leppington/` | `36efc778` | `e5f56c0:image` | 1153 |
| IMG-0072 | Band A UNUSABLE | `/concreters-oran-park/` | `a599284` | `7bcc8c0:image` | 1187 |
| IMG-0073 | D32 whole-section | `/concreters-oran-park/` | `36efc778` | `0424a72:image` | 1188 |
| IMG-0074 | D32 whole-section | `/concreters-oran-park/` | `36efc778` | `4195f9b:image` | 1230 |
| IMG-0075 | D32 whole-section | `/concreters-oran-park/` | `36efc778` | `e5f56c0:image` | 1231 |
| IMG-0092 | D32 whole-section | `/concreters-gregory-hills/` | `36efc778` | `0424a72:image` | 18 |
| IMG-0093 | D32 whole-section | `/concreters-gregory-hills/` | `36efc778` | `4195f9b:image` | 19 |
| IMG-0094 | D32 whole-section | `/concreters-gregory-hills/` | `36efc778` | `e5f56c0:image` | 46 |
| IMG-0106 | D32 whole-section | `/concreters-harrington-park/` | `36efc778` | `0424a72:image` | 121 |
| IMG-0107 | D32 whole-section | `/concreters-harrington-park/` | `36efc778` | `4195f9b:image` | 144 |
| IMG-0108 | D32 whole-section | `/concreters-harrington-park/` | `36efc778` | `e5f56c0:image` | 145 |
| IMG-0120 | D32 whole-section | `/concreters-austral/` | `36efc778` | `0424a72:image` | 181 |
| IMG-0121 | D32 whole-section | `/concreters-austral/` | `36efc778` | `4195f9b:image` | 182 |
| IMG-0122 | D32 whole-section | `/concreters-austral/` | `36efc778` | `e5f56c0:image` | 183 |
| IMG-0128 | blank placeholder | `/concrete-driveway-replacement-south-west-sydney/` | `b61f1c2` | `104d481:image` | 275 |
| IMG-0129 | blank placeholder | `/concrete-driveway-replacement-south-west-sydney/` | `a2970f7` | `620b9f2:image` | 276 |
| IMG-0130 | blank placeholder | `/concrete-driveway-replacement-south-west-sydney/` | `a32399d` | `015aff8:image` | 277 |
| IMG-0131 | blank placeholder | `/concrete-driveway-replacement-south-west-sydney/` | `a32399d` | `5e63315:image` | 278 |
| IMG-0132 | blank placeholder | `/concrete-driveway-replacement-south-west-sydney/` | `a32399d` | `7c2901e:image` | 279 |
| IMG-0133 | other prohibited direct | `/concrete-driveway-replacement-south-west-sydney/` | `a089da8` | `ae99959:image` | 280 |
| IMG-0134 | blank placeholder | `/concrete-driveway-replacement-south-west-sydney/` | `4b91b73` | `7886294:image` | 323 |
| IMG-0135 | Band A UNUSABLE | `/concrete-driveway-replacement-south-west-sydney/` | `57035e1` | `154c6cb:image` | 480 |
| IMG-0136 | Band A UNUSABLE | `/concrete-driveway-replacement-south-west-sydney/` | `b4df2ad` | `51a4a3e:image` | 481 |
| IMG-0146 | other prohibited direct | `/concrete-crossovers-and-laybacks-south-west-sydney/` | `17d9b581` | `74b5f96b:image` | 272 |
| IMG-0151 | Band A UNUSABLE | `/commercial-concreting-south-west-sydney/` | `5bb41fd3` | `50151b3b:image` | 956 |
| IMG-0152 | other prohibited direct | `/commercial-concreting-south-west-sydney/` | `3a44da3` | `899b5bf:image` | 1020 |
| IMG-0157 | Band A UNUSABLE | `/concreters-gledswood-hills/` | `9e36728` | `a86c195:image` | 481 |
| IMG-0158 | Band A UNUSABLE | `/concreters-gledswood-hills/` | `9e36728` | `516941f:image` | 482 |
| IMG-0161 | Band A UNUSABLE | `/concreters-gledswood-hills/` | `98fbeea` | `e6c2ed7:image` | 907 |
| IMG-0167 | D32 whole-section | `/concreters-gledswood-hills/` | `36efc778` | `0424a72:image` | 926 |
| IMG-0168 | D32 whole-section | `/concreters-gledswood-hills/` | `36efc778` | `4195f9b:image` | 927 |
| IMG-0169 | D32 whole-section | `/concreters-gledswood-hills/` | `36efc778` | `e5f56c0:image` | 956 |
| IMG-0181 | D32 whole-section | `/concreters-catherine-field/` | `36efc778` | `0424a72:image` | 52 |
| IMG-0182 | D32 whole-section | `/concreters-catherine-field/` | `36efc778` | `4195f9b:image` | 53 |
| IMG-0183 | D32 whole-section | `/concreters-catherine-field/` | `36efc778` | `e5f56c0:image` | 54 |
| IMG-0192 | Band A UNUSABLE | `/concreters-narellan/` | `77cc745` | `2eb88ab:image` | 956 |
| IMG-0193 | other prohibited direct | `/concreters-narellan/` | `8d1059a` | `0ca264b:image` | 1020 |
| IMG-0195 | D32 whole-section | `/concreters-narellan/` | `36efc778` | `0424a72:image` | 1065 |
| IMG-0196 | D32 whole-section | `/concreters-narellan/` | `36efc778` | `4195f9b:image` | 1066 |
| IMG-0197 | D32 whole-section | `/concreters-narellan/` | `36efc778` | `e5f56c0:image` | 1067 |
| IMG-0199 | Band A UNUSABLE | `/concreters-narellan-vale/` | `9e36728` | `a86c195:image` | 481 |
| IMG-0200 | Band A UNUSABLE | `/concreters-narellan-vale/` | `9e36728` | `516941f:image` | 482 |
| IMG-0203 | Band A UNUSABLE | `/concreters-narellan-vale/` | `98fbeea` | `e6c2ed7:image` | 907 |
| IMG-0217 | blank placeholder | `/concreters-mount-annan/` | `98fbeea` | `e6c2ed7:image` | 275 |
| IMG-0219 | blank placeholder | `/concreters-mount-annan/` | `40d980a` | `af8ef50:image` | 276 |
| IMG-0220 | blank placeholder | `/concreters-mount-annan/` | `77cc745` | `2eb88ab:image` | 277 |
| IMG-0221 | blank placeholder | `/concreters-mount-annan/` | `8d1059a` | `0ca264b:image` | 278 |
| IMG-0222 | blank placeholder | `/concreters-mount-annan/` | `a599284` | `7bcc8c0:image` | 279 |
| IMG-0223 | D32 whole-section | `/concreters-mount-annan/` | `36efc778` | `0424a72:image` | 280 |
| IMG-0224 | D32 whole-section | `/concreters-mount-annan/` | `36efc778` | `4195f9b:image` | 323 |
| IMG-0225 | D32 whole-section | `/concreters-mount-annan/` | `36efc778` | `e5f56c0:image` | 480 |
| IMG-0229 | Band A UNUSABLE | `/concreters-currans-hill/` | `9e36728` | `f36a8f3:image` | 956 |
| IMG-0230 | other prohibited direct | `/concreters-currans-hill/` | `98fbeea` | `af91c52:image` | 1020 |
| IMG-0232 | other prohibited direct | `/concreters-currans-hill/` | `98fbeea` | `d06ebf3:image` | 1020 |
| IMG-0235 | other prohibited direct | `/concreters-currans-hill/` | `8d1059a` | `0ca264b:image` | 1067 |
| IMG-0237 | D32 whole-section | `/concreters-currans-hill/` | `36efc778` | `0424a72:image` | 1109 |
| IMG-0238 | D32 whole-section | `/concreters-currans-hill/` | `36efc778` | `4195f9b:image` | 1150 |
| IMG-0239 | D32 whole-section | `/concreters-currans-hill/` | `36efc778` | `e5f56c0:image` | 1151 |
| IMG-0250 | blank placeholder | `/concreters-spring-farm/` | `a599284` | `7bcc8c0:image` | 275 |
| IMG-0251 | D32 whole-section | `/concreters-spring-farm/` | `36efc778` | `0424a72:image` | 276 |
| IMG-0252 | D32 whole-section | `/concreters-spring-farm/` | `36efc778` | `4195f9b:image` | 277 |
| IMG-0253 | D32 whole-section | `/concreters-spring-farm/` | `36efc778` | `e5f56c0:image` | 278 |
| IMG-0265 | D32 whole-section | `/concreters-elderslie/` | `36efc778` | `0424a72:image` | 166 |
| IMG-0266 | D32 whole-section | `/concreters-elderslie/` | `36efc778` | `4195f9b:image` | 167 |
| IMG-0267 | D32 whole-section | `/concreters-elderslie/` | `36efc778` | `e5f56c0:image` | 168 |
| IMG-0269 | other prohibited direct | `/concreters-cobbitty/` | `9e36728` | `a86c195:image` | 280 |
| IMG-0270 | blank placeholder | `/concreters-cobbitty/` | `9e36728` | `516941f:image` | 323 |
| IMG-0271 | Band A UNUSABLE | `/concreters-cobbitty/` | `9e36728` | `f36a8f3:image` | 480 |
| IMG-0272 | Band A UNUSABLE | `/concreters-cobbitty/` | `98fbeea` | `af91c52:image` | 481 |
| IMG-0273 | Band A UNUSABLE | `/concreters-cobbitty/` | `98fbeea` | `e6c2ed7:image` | 482 |
| IMG-0274 | Band A UNUSABLE | `/concreters-cobbitty/` | `98fbeea` | `d06ebf3:image` | 481 |
| IMG-0277 | Band A UNUSABLE | `/concreters-cobbitty/` | `8d1059a` | `0ca264b:image` | 907 |
| IMG-0279 | D32 whole-section | `/concreters-cobbitty/` | `36efc778` | `0424a72:image` | 909 |
| IMG-0280 | D32 whole-section | `/concreters-cobbitty/` | `36efc778` | `4195f9b:image` | 924 |
| IMG-0281 | D32 whole-section | `/concreters-cobbitty/` | `36efc778` | `e5f56c0:image` | 925 |
| IMG-0284 | other prohibited direct | `/concreters-camden-south/` | `9e36728` | `516941f:image` | 1067 |
| IMG-0290 | Band A UNUSABLE | `/concreters-kirkham/` | `9e36728` | `a86c195:image` | 482 |
| IMG-0293 | Band A UNUSABLE | `/concreters-kirkham/` | `98fbeea` | `af91c52:image` | 907 |
| IMG-0295 | Band A UNUSABLE | `/concreters-kirkham/` | `98fbeea` | `d06ebf3:image` | 907 |
| IMG-0300 | Band A UNUSABLE | `/concreters-grasmere/` | `98fbeea` | `af91c52:image` | 1187 |
| IMG-0302 | Band A UNUSABLE | `/concreters-grasmere/` | `98fbeea` | `d06ebf3:image` | 1187 |
| IMG-0306 | blank placeholder | `/concreters-ellis-lane/` | `9e36728` | `f36a8f3:image` | 275 |
| IMG-0307 | blank placeholder | `/concreters-ellis-lane/` | `98fbeea` | `af91c52:image` | 276 |
| IMG-0308 | blank placeholder | `/concreters-ellis-lane/` | `98fbeea` | `e6c2ed7:image` | 277 |
| IMG-0309 | blank placeholder | `/concreters-ellis-lane/` | `98fbeea` | `d06ebf3:image` | 276 |
| IMG-0319 | Band A UNUSABLE | `/concreters-camden-park/` | `9e36728` | `516941f:image` | 956 |
| IMG-0320 | other prohibited direct | `/concreters-camden-park/` | `9e36728` | `f36a8f3:image` | 1020 |
| IMG-0342 | D32 whole-section | `/concreters-edmondson-park/` | `36efc778` | `0424a72:image` | 48 |
| IMG-0343 | D32 whole-section | `/concreters-edmondson-park/` | `36efc778` | `4195f9b:image` | 49 |
| IMG-0344 | D32 whole-section | `/concreters-edmondson-park/` | `36efc778` | `e5f56c0:image` | 50 |
| IMG-0346 | blank placeholder | `/concreters-bringelly/` | `9e36728` | `a86c195:image` | 323 |
| IMG-0347 | Band A UNUSABLE | `/concreters-bringelly/` | `9e36728` | `516941f:image` | 480 |
| IMG-0348 | Band A UNUSABLE | `/concreters-bringelly/` | `9e36728` | `f36a8f3:image` | 481 |
| IMG-0349 | Band A UNUSABLE | `/concreters-bringelly/` | `98fbeea` | `af91c52:image` | 482 |
| IMG-0351 | Band A UNUSABLE | `/concreters-bringelly/` | `98fbeea` | `d06ebf3:image` | 482 |
| IMG-0353 | Band A UNUSABLE | `/concreters-bringelly/` | `77cc745` | `2eb88ab:image` | 907 |
| IMG-0356 | D32 whole-section | `/concreters-bringelly/` | `36efc778` | `0424a72:image` | 924 |
| IMG-0357 | D32 whole-section | `/concreters-bringelly/` | `36efc778` | `4195f9b:image` | 925 |
| IMG-0358 | D32 whole-section | `/concreters-bringelly/` | `36efc778` | `e5f56c0:image` | 926 |
| IMG-0374 | other prohibited direct | `/concreters-west-hoxton/` | `9e36728` | `a86c195:image` | 1067 |
| IMG-0388 | Band A UNUSABLE | `/concreters-carnes-hill/` | `9e36728` | `a86c195:image` | 1187 |
| IMG-0444 | blank placeholder | `/concreters-chipping-norton/` | `9e36728` | `a86c195:image` | 275 |
| IMG-0445 | blank placeholder | `/concreters-chipping-norton/` | `9e36728` | `516941f:image` | 276 |
| IMG-0446 | blank placeholder | `/concreters-chipping-norton/` | `9e36728` | `f36a8f3:image` | 277 |
| IMG-0447 | blank placeholder | `/concreters-chipping-norton/` | `98fbeea` | `af91c52:image` | 278 |
| IMG-0448 | blank placeholder | `/concreters-chipping-norton/` | `98fbeea` | `e6c2ed7:image` | 279 |
| IMG-0449 | blank placeholder | `/concreters-chipping-norton/` | `98fbeea` | `d06ebf3:image` | 278 |
| IMG-0451 | Band A UNUSABLE | `/concreters-wattle-grove/` | `9e36728` | `a86c195:image` | 956 |
| IMG-0452 | other prohibited direct | `/concreters-wattle-grove/` | `9e36728` | `516941f:image` | 1020 |
| IMG-0458 | blank placeholder | `/concreters-kemps-creek/` | `9e36728` | `a86c195:image` | 279 |
| IMG-0459 | other prohibited direct | `/concreters-kemps-creek/` | `9e36728` | `516941f:image` | 280 |
| IMG-0460 | blank placeholder | `/concreters-kemps-creek/` | `9e36728` | `f36a8f3:image` | 323 |
| IMG-0461 | Band A UNUSABLE | `/concreters-kemps-creek/` | `98fbeea` | `af91c52:image` | 480 |
| IMG-0462 | Band A UNUSABLE | `/concreters-kemps-creek/` | `98fbeea` | `e6c2ed7:image` | 481 |
| IMG-0463 | Band A UNUSABLE | `/concreters-kemps-creek/` | `98fbeea` | `d06ebf3:image` | 480 |
| IMG-0481 | Band A UNUSABLE | `/concreters-leumeah/` | `9e36728` | `f36a8f3:image` | 1187 |
| IMG-0494 | blank placeholder | `/concreters-ingleburn/` | `9e36728` | `516941f:image` | 275 |
| IMG-0495 | blank placeholder | `/concreters-ingleburn/` | `9e36728` | `f36a8f3:image` | 276 |
| IMG-0496 | blank placeholder | `/concreters-ingleburn/` | `98fbeea` | `af91c52:image` | 277 |
| IMG-0497 | blank placeholder | `/concreters-ingleburn/` | `98fbeea` | `e6c2ed7:image` | 278 |
| IMG-0498 | blank placeholder | `/concreters-ingleburn/` | `98fbeea` | `d06ebf3:image` | 277 |
| IMG-0528 | blank placeholder | `/concreters-bradbury/` | `9e36728` | `a86c195:image` | 276 |
| IMG-0529 | blank placeholder | `/concreters-bradbury/` | `9e36728` | `516941f:image` | 277 |
| IMG-0530 | blank placeholder | `/concreters-bradbury/` | `9e36728` | `f36a8f3:image` | 278 |
| IMG-0531 | blank placeholder | `/concreters-bradbury/` | `98fbeea` | `af91c52:image` | 279 |
| IMG-0532 | other prohibited direct | `/concreters-bradbury/` | `98fbeea` | `e6c2ed7:image` | 280 |
| IMG-0533 | blank placeholder | `/concreters-bradbury/` | `98fbeea` | `d06ebf3:image` | 279 |
| IMG-0535 | other prohibited direct | `/concreters-glen-alpine/` | `9e36728` | `a86c195:image` | 1020 |
| IMG-0539 | other prohibited direct | `/concreters-glen-alpine/` | `98fbeea` | `e6c2ed7:image` | 1067 |
| IMG-0542 | blank placeholder | `/concreters-gilead/` | `9e36728` | `a86c195:image` | 278 |
| IMG-0543 | blank placeholder | `/concreters-gilead/` | `9e36728` | `516941f:image` | 279 |
| IMG-0544 | other prohibited direct | `/concreters-gilead/` | `9e36728` | `f36a8f3:image` | 280 |
| IMG-0545 | blank placeholder | `/concreters-gilead/` | `98fbeea` | `af91c52:image` | 323 |
| IMG-0546 | Band A UNUSABLE | `/concreters-gilead/` | `98fbeea` | `e6c2ed7:image` | 480 |
| IMG-0547 | blank placeholder | `/concreters-gilead/` | `98fbeea` | `d06ebf3:image` | 323 |
| IMG-0560 | Band A UNUSABLE | `/concreters-wilton/` | `98fbeea` | `e6c2ed7:image` | 1187 |
| IMG-0570 | blank placeholder | `/concreters-tahmoor/` | `9e36728` | `a86c195:image` | 279 |
| IMG-0571 | other prohibited direct | `/concreters-tahmoor/` | `9e36728` | `516941f:image` | 280 |
| IMG-0572 | blank placeholder | `/concreters-tahmoor/` | `9e36728` | `f36a8f3:image` | 323 |
| IMG-0573 | Band A UNUSABLE | `/concreters-tahmoor/` | `98fbeea` | `af91c52:image` | 480 |
| IMG-0574 | Band A UNUSABLE | `/concreters-tahmoor/` | `98fbeea` | `e6c2ed7:image` | 481 |
| IMG-0575 | Band A UNUSABLE | `/concreters-tahmoor/` | `98fbeea` | `d06ebf3:image` | 480 |
| IMG-0588 | Band A UNUSABLE | `/concreters-douglas-park/` | `98fbeea` | `e6c2ed7:image` | 1187 |
| IMG-0598 | Band A UNUSABLE | `/concreters-the-oaks/` | `9e36728` | `a86c195:image` | 482 |
| IMG-0601 | Band A UNUSABLE | `/concreters-the-oaks/` | `98fbeea` | `af91c52:image` | 907 |
| IMG-0603 | Band A UNUSABLE | `/concreters-the-oaks/` | `98fbeea` | `d06ebf3:image` | 907 |
| IMG-0609 | blank placeholder | `/concreters-bargo/` | `98fbeea` | `e6c2ed7:image` | 275 |

## Elementor reference reconciliation and blind-spot correction

Report 49 independently counted the starting derivative at **410 populated image references**. The former architecture detector reported 409 because it missed homepage attachment 609 in nested Elementor 4.2 `e-image` widget `306c538`. The production detector is now recursive and format-aware; a separately implemented settings-first detector must find the identical multiset of page/attachment/widget/setting references.

The approved transformation changes the inventory rather than preserving 410: it removes 45 surviving blank-placeholder placements and restores 75 authorised Band A GENERIC placements. The final exact result is therefore **440 = 410 − 45 + 75**. Both independent detectors report 440; all resolve to the 55 permitted attachment records; unresolved references are zero. The regression suite explicitly locates attachment 609 at homepage widget `306c538`, while the production logic contains no attachment-609 special case.

The future post-import database verifier was also extended to decode Elementor 4.2 typed-image attachment IDs. It was not executed because no staging database/site was imported in this pass.
Local PHP is unavailable, so PHP runtime lint/execution remains a future staging control.

## Gallery disposition

Page `/gallery/` (ID 1365) is deferred until a genuine, permission-backed project library exists. `build/27-wave1-menus.json` records the exact 20 August owner authority and excludes the gallery from every launch menu assignment. Menu lint passes. The page was not deleted and its indexability was not changed.

## Verification results

| Command/control | Result |
|---|---|
| `python scripts/50-band-a-worksheet-verify.py` | PASS — 16/16; 10 GENERIC; 6 UNUSABLE; 0 HOLD |
| `python scripts/45-band-b-verify.py` | PASS — 7 GENERIC; 2 UNUSABLE; 28 slot contract |
| `python scripts/47-apply-media-files.py --check` | PASS — 55 public |
| `python scripts/22-media-audit.py` | PASS — 55/55; zero missing/extras/non-images |
| `python scripts/46-public-media-gate.py` | PASS — zero blockers; 440/440 detector reconciliation; Band A placement 75/75 |
| `python scripts/46-architecture-import-gate.py --check` | PASS — reproducible hash; 75 active-main; 81 withdrawn absent |
| `python scripts/27-menu-lint.py` | PASS — gallery absent; zero unsafe targets |
| `python scripts/21-encoding-canary.py` | PASS — all three exact UTF-8 assertions |
| `python -m pytest -q` | PASS — 19 tests |
| `python -m py_compile ...` | PASS |
| `python scripts/37-preconditions.py` | PASS as reporter — Phase B RUNNABLE; A and C–G BLOCKED |
| `bash scripts/28-preflight.sh` | expected NO-GO — Gates 7, 12 and 16 fail; media Gate 17 PASS |
| `git diff --check` | PASS with no output; limitation: repository has zero tracked files |
| PHP syntax/runtime check | NOT RUN — PHP unavailable locally; verifier installation remains read-only future staging work |

### Immutable hash table

| File | Expected SHA-256 | Computed SHA-256 | Result |
|---|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | **MATCH** |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | **MATCH** |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | **MATCH** |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | **MATCH** |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | **MATCH** |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | **MATCH** |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | **MATCH** |

### Complete preflight table

```text
  GATE                                           RESULT  DETAIL
  1. encoding canary (§3.1)                     PASS    fixture and both restored assertions survived
  2. 15 Stage 9 gates                            PASS    15/15 pass
  3. post-ID collision audit (present WXRs)      PASS    main=306 IDs; privacy=1 IDs; collisions=0; calculator=absent (required until built)
  4. media intake audit                          PASS    active public intake technical contract passes: 55/55; immutable provenance baseline remains 83
  5. Astra Customizer audit                      PASS    export parsed; required groups + design-carriage + internal-consistency all pass
  6. Elementor image-reference count             PASS    image=1085 (expected 1085), background_image=98 (NOT covered by the recorded figure), total=1183, distinct attachment ids referenced=73 of 83, unresolved refs=0
  7. uniqueness gates                            FAIL    5-grams on >2 pages=1761; within-class pairs over 40% overlap=1491
  8. intersection audit                          PASS    built=35, allow-listed=35, extras=0, missing=0, all draft=True
  9. menu lint (Wave 1 spec)                     PASS    zero draft, noindex or 404 targets
  10. Victorian blocklist scan                   PASS    main WXR=0; supplementary WXR=absent; privacy WXR=0; Astra export=0 (wp_css excluded at import); terms=13
  11. placeholder-in-schema scan                 PASS    JSON-LD blocks found in Elementor data=0; containing a placeholder token=0
  12. coherence gate (D15)                       FAIL    90 pages SEVERE, 139 above threshold, corpus filler 0.8244
 — no page above the threshold may enter any wave
  13. source-brand transformation result         PASS    baseline 466=366 reader-visible + 100 preserved; transformed reader-visible=0
  14. menu targets in assigned locations         PASS    primary->primary: 0 unsafe; mobile_menu->primary-2: 0 unsafe; footer_menu->footer-services: 0 unsafe; held-set=6, withdrawn-set=81
  15. active architecture/import parity          PASS    allowed=76; active-main=75; privacy=1; withdrawn=81; calculator=ABSENT — correctly excluded
  16. claim-to-evidence parity                   FAIL    occurrences=135; unsupported=131; pages=18; unsupported-pages=16
  17. public-media suitability                   PASS    blocking=0; Band-A-unrecorded=0; Band-B-fail=0

  OVERALL                                        NO-GO
```

## Remaining non-image blockers

- Claim/evidence Gate 16: 131 unsupported of 135 occurrences on 16 pages. No unsupported business claim was rewritten in this pass.
- Coherence Gate 12: 90 SEVERE pages and 139 pages above the filler threshold; service and other withdrawn/active copy still needs the evidence-gated rewrite programme.
- Uniqueness Gate 7: 1,761 repeated 5-grams and 1,491 within-class pairs above 40% overlap.
- Identity/operator: legal entity, ABN, licence/insurance state, staffed-address state, phone routing and signed NSW operator remain unverified. No LocalBusiness schema or contractor voice is permitted.
- Owner service specification matrix: 91 fields remain `verified:false`; Phase A is blocked.
- Liverpool Council evidence is absent; Phase D remains blocked.
- Service-page copy, privacy-policy blocking markers, claim removals/rewrite, menu assignment, brand-slot assignment, staging import and post-import verification remain outstanding.
- The 45 unresearched suburb pages remain deferred under D22, not dropped.

## Files changed or regenerated in this pass

Authoritative mutable inputs and controls: `reports/44-sighting-worksheet.csv`, `lib/media_payload.py`, `scripts/46-architecture-import-gate.py`, `scripts/46-public-media-gate.py`, `scripts/47-apply-media-files.py`, `scripts/50-band-a-worksheet-verify.py`, `scripts/50-write-report.py`, `scripts/22-reencode-images.sh`, `scripts/27-menu-lint.py`, `build/27-wave1-menus.json`, `staging-authoritative/scripts/import-media-local.sh`, `staging-authoritative/scripts/verify-post-import.php`, `tests/test_phase_b_media_payload.py` and `tests/test_preimport_safety.py`.

Reproducibly generated/updated outputs: `build/46-active-main-import.xml`, `build/46-active-page-allowlist.json`, `build/47-media-remediation.csv`, the architecture/public-media policy and result JSON files, media-audit outputs, `reports/50-band-a-worksheet-validation.json`, `reports/28-preflight.md`, this report and `CONTEXT.md`.

Media filesystem changes: the ten approved Band A GENERIC binaries moved from the held directory into the public intake under their exact Report 49 subject-only filenames; the six Band A UNUSABLE binaries moved to retired quarantine; and the six blank-placeholder binaries moved from public intake to retired quarantine. No binary was remotely fetched or generated.

## Safety confirmation

No WordPress import, staging/live database execution, deployment, publication, remote media fetch, generated image, indexability change, immutable-file edit or governing-document edit occurred. The derivative was generated by the transformer and was never manually patched.
