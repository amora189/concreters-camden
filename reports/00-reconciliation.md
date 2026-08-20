STAGE 0 - Read and reconcile
=======================================
READ:      CODEX-BUILD.md; camden-site-structure-and-silo.md except superseded page inventory; codex-clone-prompt.md sections 1 and 9; oran-park-gold-standard.md; suburbs.json; camden-concreting-seo-spec.md sections 5 and 7; expansion-300-pages.md; suburbs-expanded.json; intersection-differentiators.json
DID:       Reconciled the build footprint to the revised 156-page budget, including the draft /guides/ hub. Used intersection-differentiators.json as the sole authority for intersection pages and kept the stale 180/300 figures in expansion-300-pages.md superseded.
ARTIFACTS: reports/00-reconciliation.md

# Revised Stage 0 Reconciliation - 156 Pages

## Effective precedence

- intersection-differentiators.json supersedes expansion-300-pages.md section 1 and section 4 for page counts and intersection selection.
- Build only the 35 intersection pages listed in intersection-differentiators.json.
- Do not generate any suburb/service intersection not listed there.
- suburbs-expanded.json remains the suburb-list authority: 60 suburbs across 4 LGAs.
- suburbs.json remains the deep-content authority for the 15 researched suburbs.
- expansion-300-pages.md still governs the expansion architecture except where superseded above.

## Revised page budget

| Page class | Count |
|---|---:|
| home | 1 |
| utility | 4 |
| services | 10 |
| suburbs | 60 |
| intersections | 35 |
| guide hub | 1 |
| guides | 35 |
| cost_and_comparison | 10 |
| total | 156 |

## Page list

| URL | Page type | Primary keyword | Source template / authority | Status |
|---|---|---|---|---|
| / | Home | concreters camden | homepage | publish |
| /about/ | Utility | - | contact clone | publish |
| /contact/ | Utility | - | contact | publish |
| /quote/ | Utility | - | contact clone | publish |
| /gallery/ | Utility | - | new/gallery from media inventory | publish |
| /concrete-driveways-south-west-sydney/ | Service | concrete driveways south west sydney | concrete-driveways-melbourne | publish |
| /concrete-driveway-replacement-south-west-sydney/ | Service | concrete driveway replacement south west sydney | concrete-driveways-melbourne clone | publish |
| /concrete-slabs-south-west-sydney/ | Service | concrete slabs south west sydney | concrete-slabs-melbourne | publish |
| /shed-and-garage-slabs-south-west-sydney/ | Service | shed and garage slabs south west sydney | concrete-slabs-melbourne clone | publish |
| /exposed-aggregate-south-west-sydney/ | Service | exposed aggregate south west sydney | exposed-aggregate-melbourne | publish |
| /decorative-concrete-south-west-sydney/ | Service | decorative concrete south west sydney | decorative-concrete-melbourne | publish |
| /concrete-patios-south-west-sydney/ | Service | concrete patios south west sydney | concrete-patios-melbourne | publish |
| /concrete-paths-south-west-sydney/ | Service | concrete paths south west sydney | concrete-paths-melbourne | publish |
| /concrete-crossovers-and-laybacks-south-west-sydney/ | Service | concrete crossovers and laybacks south west sydney | wyndham-council-vehicle-crossing + service clone | publish |
| /commercial-concreting-south-west-sydney/ | Service | commercial concreting south west sydney | concrete-slabs-melbourne clone | publish |
| /concreters-oran-park/ | Suburb Tier 1 (Camden Council) | concreters oran park | suburbs-expanded.json skeleton + suburbs.json deep fields | publish |
| /concreters-gregory-hills/ | Suburb Tier 1 (Camden Council) | concreters gregory hills | suburbs-expanded.json skeleton + suburbs.json deep fields | publish |
| /concreters-gledswood-hills/ | Suburb Tier 1 (Camden Council) | concreters gledswood hills | suburbs-expanded.json skeleton + suburbs.json deep fields | publish |
| /concreters-catherine-field/ | Suburb Tier 2 (Camden Council) | concreters catherine field | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-harrington-park/ | Suburb Tier 1 (Camden Council) | concreters harrington park | suburbs-expanded.json skeleton + suburbs.json deep fields | publish |
| /concreters-narellan/ | Suburb Tier 2 (Camden Council) | concreters narellan | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-narellan-vale/ | Suburb Tier 3 (Camden Council) | concreters narellan vale | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-smeaton-grange/ | Suburb Tier 3 (Camden Council) | concreters smeaton grange | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-mount-annan/ | Suburb Tier 2 (Camden Council) | concreters mount annan | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-currans-hill/ | Suburb Tier 3 (Camden Council) | concreters currans hill | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-spring-farm/ | Suburb Tier 2 (Camden Council) | concreters spring farm | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-elderslie/ | Suburb Tier 2 (Camden Council) | concreters elderslie | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-cobbitty/ | Suburb Tier 3 (Camden Council) | concreters cobbitty | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-camden-south/ | Suburb Tier 3 (Camden Council) | concreters camden south | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-kirkham/ | Suburb Tier 4 (Camden Council) | concreters kirkham | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-grasmere/ | Suburb Tier 4 (Camden Council) | concreters grasmere | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-ellis-lane/ | Suburb Tier 4 (Camden Council) | concreters ellis lane | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-theresa-park/ | Suburb Tier 4 (Camden Council) | concreters theresa park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-camden-park/ | Suburb Tier 4 (Camden Council) | concreters camden park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-cawdor/ | Suburb Tier 4 (Camden Council) | concreters cawdor | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-austral/ | Suburb Tier 1 (Liverpool City Council) | concreters austral | suburbs-expanded.json skeleton + suburbs.json deep fields | publish |
| /concreters-leppington/ | Suburb Tier 1 (Liverpool City Council) | concreters leppington | suburbs-expanded.json skeleton + suburbs.json deep fields | publish |
| /concreters-edmondson-park/ | Suburb Tier 2 (Liverpool City Council) | concreters edmondson park | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-bringelly/ | Suburb Tier 3 (Liverpool City Council) | concreters bringelly | suburbs-expanded.json skeleton + suburbs.json deep fields | draft |
| /concreters-rossmore/ | Suburb Tier 4 (Liverpool City Council) | concreters rossmore | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-middleton-grange/ | Suburb Tier 2 (Liverpool City Council) | concreters middleton grange | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-west-hoxton/ | Suburb Tier 3 (Liverpool City Council) | concreters west hoxton | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-hoxton-park/ | Suburb Tier 3 (Liverpool City Council) | concreters hoxton park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-carnes-hill/ | Suburb Tier 3 (Liverpool City Council) | concreters carnes hill | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-horningsea-park/ | Suburb Tier 4 (Liverpool City Council) | concreters horningsea park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-elizabeth-hills/ | Suburb Tier 4 (Liverpool City Council) | concreters elizabeth hills | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-len-waters-estate/ | Suburb Tier 4 (Liverpool City Council) | concreters len waters estate | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-cecil-hills/ | Suburb Tier 3 (Liverpool City Council) | concreters cecil hills | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-prestons/ | Suburb Tier 3 (Liverpool City Council) | concreters prestons | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-casula/ | Suburb Tier 3 (Liverpool City Council) | concreters casula | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-moorebank/ | Suburb Tier 3 (Liverpool City Council) | concreters moorebank | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-chipping-norton/ | Suburb Tier 4 (Liverpool City Council) | concreters chipping norton | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-wattle-grove/ | Suburb Tier 4 (Liverpool City Council) | concreters wattle grove | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-kemps-creek/ | Suburb Tier 4 (Liverpool City Council) | concreters kemps creek | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-cecil-park/ | Suburb Tier 4 (Liverpool City Council) | concreters cecil park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-campbelltown/ | Suburb Tier 2 (Campbelltown City Council) | concreters campbelltown | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-leumeah/ | Suburb Tier 3 (Campbelltown City Council) | concreters leumeah | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-minto/ | Suburb Tier 3 (Campbelltown City Council) | concreters minto | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-ingleburn/ | Suburb Tier 3 (Campbelltown City Council) | concreters ingleburn | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-glenfield/ | Suburb Tier 4 (Campbelltown City Council) | concreters glenfield | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-macquarie-fields/ | Suburb Tier 4 (Campbelltown City Council) | concreters macquarie fields | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-raby/ | Suburb Tier 4 (Campbelltown City Council) | concreters raby | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-eagle-vale/ | Suburb Tier 4 (Campbelltown City Council) | concreters eagle vale | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-bradbury/ | Suburb Tier 4 (Campbelltown City Council) | concreters bradbury | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-glen-alpine/ | Suburb Tier 4 (Campbelltown City Council) | concreters glen alpine | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-gilead/ | Suburb Tier 3 (Campbelltown City Council) | concreters gilead | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-menangle-park/ | Suburb Tier 3 (Campbelltown City Council) | concreters menangle park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-wilton/ | Suburb Tier 2 (Wollondilly Shire Council) | concreters wilton | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-picton/ | Suburb Tier 3 (Wollondilly Shire Council) | concreters picton | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-tahmoor/ | Suburb Tier 3 (Wollondilly Shire Council) | concreters tahmoor | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-appin/ | Suburb Tier 3 (Wollondilly Shire Council) | concreters appin | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-douglas-park/ | Suburb Tier 4 (Wollondilly Shire Council) | concreters douglas park | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-menangle/ | Suburb Tier 4 (Wollondilly Shire Council) | concreters menangle | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-the-oaks/ | Suburb Tier 4 (Wollondilly Shire Council) | concreters the oaks | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concreters-bargo/ | Suburb Tier 4 (Wollondilly Shire Council) | concreters bargo | suburbs-expanded.json skeleton + REQUIRED-RESEARCH placeholders; noindex | draft |
| /concrete-crossovers-and-laybacks-oran-park/ | Intersection | concrete crossovers and laybacks oran park | intersection-differentiators.json | draft |
| /concrete-driveways-oran-park/ | Intersection | concrete driveways oran park | intersection-differentiators.json | draft |
| /shed-and-garage-slabs-oran-park/ | Intersection | shed and garage slabs oran park | intersection-differentiators.json | draft |
| /exposed-aggregate-oran-park/ | Intersection | exposed aggregate oran park | intersection-differentiators.json | draft |
| /concrete-crossovers-and-laybacks-leppington/ | Intersection | concrete crossovers and laybacks leppington | intersection-differentiators.json | draft |
| /concrete-slabs-leppington/ | Intersection | concrete slabs leppington | intersection-differentiators.json | draft |
| /concrete-driveways-leppington/ | Intersection | concrete driveways leppington | intersection-differentiators.json | draft |
| /commercial-concreting-gregory-hills/ | Intersection | commercial concreting gregory hills | intersection-differentiators.json | draft |
| /concrete-slabs-gregory-hills/ | Intersection | concrete slabs gregory hills | intersection-differentiators.json | draft |
| /concrete-slabs-gledswood-hills/ | Intersection | concrete slabs gledswood hills | intersection-differentiators.json | draft |
| /exposed-aggregate-gledswood-hills/ | Intersection | exposed aggregate gledswood hills | intersection-differentiators.json | draft |
| /concrete-patios-gledswood-hills/ | Intersection | concrete patios gledswood hills | intersection-differentiators.json | draft |
| /concrete-driveways-austral/ | Intersection | concrete driveways austral | intersection-differentiators.json | draft |
| /concrete-slabs-austral/ | Intersection | concrete slabs austral | intersection-differentiators.json | draft |
| /concrete-crossovers-and-laybacks-austral/ | Intersection | concrete crossovers and laybacks austral | intersection-differentiators.json | draft |
| /exposed-aggregate-harrington-park/ | Intersection | exposed aggregate harrington park | intersection-differentiators.json | draft |
| /decorative-concrete-harrington-park/ | Intersection | decorative concrete harrington park | intersection-differentiators.json | draft |
| /concrete-driveway-replacement-harrington-park/ | Intersection | concrete driveway replacement harrington park | intersection-differentiators.json | draft |
| /concrete-driveways-catherine-field/ | Intersection | concrete driveways catherine field | intersection-differentiators.json | draft |
| /shed-and-garage-slabs-catherine-field/ | Intersection | shed and garage slabs catherine field | intersection-differentiators.json | draft |
| /concrete-paths-edmondson-park/ | Intersection | concrete paths edmondson park | intersection-differentiators.json | draft |
| /concrete-patios-edmondson-park/ | Intersection | concrete patios edmondson park | intersection-differentiators.json | draft |
| /concrete-driveways-edmondson-park/ | Intersection | concrete driveways edmondson park | intersection-differentiators.json | draft |
| /commercial-concreting-narellan/ | Intersection | commercial concreting narellan | intersection-differentiators.json | draft |
| /concrete-driveway-replacement-narellan/ | Intersection | concrete driveway replacement narellan | intersection-differentiators.json | draft |
| /concrete-driveway-replacement-mount-annan/ | Intersection | concrete driveway replacement mount annan | intersection-differentiators.json | draft |
| /concrete-driveways-spring-farm/ | Intersection | concrete driveways spring farm | intersection-differentiators.json | draft |
| /concrete-crossovers-and-laybacks-spring-farm/ | Intersection | concrete crossovers and laybacks spring farm | intersection-differentiators.json | draft |
| /concrete-patios-elderslie/ | Intersection | concrete patios elderslie | intersection-differentiators.json | draft |
| /concrete-crossovers-and-laybacks-currans-hill/ | Intersection | concrete crossovers and laybacks currans hill | intersection-differentiators.json | draft |
| /concrete-driveway-replacement-currans-hill/ | Intersection | concrete driveway replacement currans hill | intersection-differentiators.json | draft |
| /concrete-driveways-cobbitty/ | Intersection | concrete driveways cobbitty | intersection-differentiators.json | draft |
| /commercial-concreting-cobbitty/ | Intersection | commercial concreting cobbitty | intersection-differentiators.json | draft |
| /commercial-concreting-bringelly/ | Intersection | commercial concreting bringelly | intersection-differentiators.json | draft |
| /concrete-slabs-bringelly/ | Intersection | concrete slabs bringelly | intersection-differentiators.json | draft |
| /guides/ | Guide hub | concreting guides south west sydney | shared guide-index component | draft |
| /guides/camden-council-driveway-crossing/ | Guide | camden council driveway crossing | guide template clone | draft |
| /guides/liverpool-council-vehicle-crossing/ | Guide | liverpool council vehicle crossing | guide template clone | draft |
| /guides/campbelltown-council-driveway-crossing/ | Guide | campbelltown council driveway crossing | guide template clone | draft |
| /guides/wollondilly-council-driveway-crossing/ | Guide | wollondilly council driveway crossing | guide template clone | draft |
| /guides/driveway-crossover-cost-nsw/ | Guide | driveway crossover cost nsw | guide template clone | draft |
| /guides/do-i-need-council-approval-driveway-nsw/ | Guide | do i need council approval driveway nsw | guide template clone | draft |
| /guides/reactive-clay-slabs-as2870/ | Guide | reactive clay slabs as2870 | guide template clone | draft |
| /guides/salinity-and-concrete-western-sydney/ | Guide | salinity and concrete western sydney | guide template clone | draft |
| /guides/engineered-fill-and-why-new-estate-slabs-crack/ | Guide | engineered fill and why new estate slabs crack | guide template clone | draft |
| /guides/site-classification-explained/ | Guide | site classification explained | guide template clone | draft |
| /guides/concrete-strength-grades-explained/ | Guide | concrete strength grades explained | guide template clone | draft |
| /guides/sl72-vs-sl82-reinforcement/ | Guide | sl72 vs sl82 reinforcement | guide template clone | draft |
| /guides/slab-thickness-for-driveways-vs-sheds/ | Guide | slab thickness for driveways vs sheds | guide template clone | draft |
| /guides/control-joints-and-saw-cut-timing/ | Guide | control joints and saw cut timing | guide template clone | draft |
| /guides/concrete-driveway-cost-nsw/ | Guide | concrete driveway cost nsw | guide template clone | draft |
| /guides/concrete-slab-cost-per-m2/ | Guide | concrete slab cost per m2 | guide template clone | draft |
| /guides/exposed-aggregate-cost/ | Guide | exposed aggregate cost | guide template clone | draft |
| /guides/stencilled-vs-stamped-concrete-cost/ | Guide | stencilled vs stamped concrete cost | guide template clone | draft |
| /guides/shed-slab-cost/ | Guide | shed slab cost | guide template clone | draft |
| /guides/commercial-hardstand-cost/ | Guide | commercial hardstand cost | guide template clone | draft |
| /guides/what-actually-moves-a-concrete-quote/ | Guide | what actually moves a concrete quote | guide template clone | draft |
| /guides/exposed-aggregate-vs-stencil/ | Guide | exposed aggregate vs stencil | guide template clone | draft |
| /guides/coloured-concrete-explained/ | Guide | coloured concrete explained | guide template clone | draft |
| /guides/honed-and-polished-concrete/ | Guide | honed and polished concrete | guide template clone | draft |
| /guides/broom-finish-concrete/ | Guide | broom finish concrete | guide template clone | draft |
| /guides/non-slip-finishes-for-pools-and-slopes/ | Guide | non slip finishes for pools and slopes | guide template clone | draft |
| /guides/sealing-and-resealing-concrete/ | Guide | sealing and resealing concrete | guide template clone | draft |
| /guides/concrete-vs-pavers-vs-asphalt/ | Guide | concrete vs pavers vs asphalt | guide template clone | draft |
| /guides/why-concrete-cracks/ | Guide | why concrete cracks | guide template clone | draft |
| /guides/concrete-crack-types-and-which-matter/ | Guide | concrete crack types and which matter | guide template clone | draft |
| /guides/concrete-repair-vs-replace/ | Guide | concrete repair vs replace | guide template clone | draft |
| /guides/how-long-before-you-can-drive-on-concrete/ | Guide | how long before you can drive on concrete | guide template clone | draft |
| /guides/curing-concrete-in-summer-vs-winter/ | Guide | curing concrete in summer vs winter | guide template clone | draft |
| /guides/concrete-efflorescence/ | Guide | concrete efflorescence | guide template clone | draft |
| /guides/removing-oil-stains-and-tyre-marks-from-concrete/ | Guide | removing oil stains and tyre marks from concrete | guide template clone | draft |
| /driveway-cost-calculator/ | Cost/comparison | driveway cost calculator | calculator/comparison template | draft |
| /slab-volume-calculator/ | Cost/comparison | slab volume calculator | calculator/comparison template | draft |
| /concrete-vs-pavers/ | Cost/comparison | concrete vs pavers | calculator/comparison template | draft |
| /concrete-vs-asphalt/ | Cost/comparison | concrete vs asphalt | calculator/comparison template | draft |
| /exposed-aggregate-vs-plain-concrete/ | Cost/comparison | exposed aggregate vs plain concrete | calculator/comparison template | draft |
| /diy-concrete-vs-hiring-a-concreter/ | Cost/comparison | diy concrete vs hiring a concreter | calculator/comparison template | draft |
| /plain-concrete-driveway-cost/ | Cost/comparison | plain concrete driveway cost | calculator/comparison template | draft |
| /exposed-aggregate-driveway-cost/ | Cost/comparison | exposed aggregate driveway cost | calculator/comparison template | draft |
| /coloured-concrete-driveway-cost/ | Cost/comparison | coloured concrete driveway cost | calculator/comparison template | draft |
| /stencilled-concrete-driveway-cost/ | Cost/comparison | stencilled concrete driveway cost | calculator/comparison template | draft |

## Intersection pages

| URL | Parent service | Parent suburb | Differentiator | Status |
|---|---|---|---|---|
| /concrete-crossovers-and-laybacks-oran-park/ | /concrete-crossovers-and-laybacks-south-west-sydney/ | /concreters-oran-park/ | The footpath allocation in Oran Park starts 800mm from the property boundary, not the 900mm that applies across the rest of the Camden LGA. The allocation is 1200mm wide either way. Get the layback set-out wrong by that 100mm and the crossover fails inspection. | draft |
| /concrete-driveways-oran-park/ | /concrete-driveways-south-west-sydney/ | /concreters-oran-park/ | Oran Park builders hand over with the house complete and the driveway not poured. The first job on almost every lot is a two-car driveway from kerb to double garage on a 350-450sqm block — not a replacement, a first pour onto a finished house. | draft |
| /shed-and-garage-slabs-oran-park/ | /shed-and-garage-slabs-south-west-sydney/ | /concreters-oran-park/ | Compaction testing at subdivision stage was done for the house footprint, not the whole lot. Fill that is sound under the house pad is often softer where a rear-yard shed is going, which is why shed slabs here settle differentially in a way no amount of mesh prevents. | draft |
| /exposed-aggregate-oran-park/ | /exposed-aggregate-south-west-sydney/ | /concreters-oran-park/ | The Hermitage and the newer premium releases already have exposed aggregate through the streetscape, so owners specify it to match rather than to stand out. Matching an existing street's stone and finish is the actual brief here. | draft |
| /concrete-crossovers-and-laybacks-leppington/ | /concrete-crossovers-and-laybacks-south-west-sydney/ | /concreters-leppington/ | Leppington straddles the Camden and Liverpool council boundary. Two lots on opposite sides of the same street can require two different crossover applications, two fee schedules and two inspection processes. The lot has to be checked on the NSW Planning Portal before anyone quotes. | draft |
| /concrete-slabs-leppington/ | /concrete-slabs-south-west-sydney/ | /concreters-leppington/ | Streets affected by Upper South Creek carry a flood planning level that governs slab height and fall. On those lots the finished level is a design input set before anything else, not something adjusted on the day. | draft |
| /concrete-driveways-leppington/ | /concrete-driveways-south-west-sydney/ | /concreters-leppington/ | Leppington was built by at least four developers running concurrently between Ingleburn Road and Heath Road, so handover specs, kerb profiles and estate design guidelines differ street by street rather than across one masterplan. | draft |
| /commercial-concreting-gregory-hills/ | /commercial-concreting-south-west-sydney/ | /concreters-gregory-hills/ | The Turner Road business precinct and Smeaton Grange sit directly alongside residential Gregory Hills. Forklift-rated floors, loading dock aprons and truck hardstands get quoted off the same drive as a domestic driveway — different mix design, different reinforcement, different jointing, and a subgrade that needs CBR verification. | draft |
| /concrete-slabs-gregory-hills/ | /concrete-slabs-south-west-sydney/ | /concreters-gregory-hills/ | A warehouse floor and a residential slab are not the same product. Commercial slabs here need a thicker reinforced section over a verified subgrade; quoting one off a residential rate is the most common costing error in this suburb. | draft |
| /concrete-slabs-gledswood-hills/ | /concrete-slabs-south-west-sydney/ | /concreters-gledswood-hills/ | Lots backing onto the South Creek riparian corridor and the Sydney Water Upper Canal sit near documented sulfate and chloride concentrations. This is where the Western Sydney Salinity Code of Practice and the CCAA saline-environments guide change the mix and the cover you specify, not just the paperwork. | draft |
| /exposed-aggregate-gledswood-hills/ | /exposed-aggregate-south-west-sydney/ | /concreters-gledswood-hills/ | Lots run 350-600sqm with wide frontages, so driveway areas are large enough that the per-square-metre premium on exposed aggregate becomes a material line item rather than a rounding difference. | draft |
| /concrete-patios-gledswood-hills/ | /concrete-patios-south-west-sydney/ | /concreters-gledswood-hills/ | Cumberland Plain Woodland conservation overlays restrict truck access on parts of the estate, so alfresco and outdoor-kitchen slabs are placed by line pump or boom pump rather than direct chute. That is a cost input, not an afterthought. | draft |
| /concrete-driveways-austral/ | /concrete-driveways-south-west-sydney/ | /concreters-austral/ | Austral is old five-acre market-garden blocks being cut up lot by lot, not a masterplanned estate. That produces 40 to 60 metre battle-axe handle driveways — high volume per job, terrible access, and almost always a line pump. | draft |
| /concrete-slabs-austral/ | /concrete-slabs-south-west-sydney/ | /concreters-austral/ | Decades of market-garden use left undocumented fill across much of the suburb. Assuming a Class M site here without testing is how a granny flat slab ends up cracking within two years. | draft |
| /concrete-crossovers-and-laybacks-austral/ | /concrete-crossovers-and-laybacks-south-west-sydney/ | /concreters-austral/ | Dual occupancies are the dominant development type, and each approved parking facility needs its own crossing. Liverpool City Council wants the crossing to match what was approved on the DA or CDC, which catches people who added a second dwelling after the fact. | draft |
| /exposed-aggregate-harrington-park/ | /exposed-aggregate-south-west-sydney/ | /concreters-harrington-park/ | Under the Harrington Grove schedule of the Camden DCP a driveway must be built across its full width in stencilled or stamped concrete, clay pavers or exposed aggregate — no portion may be uncoloured concrete. Anyone quoting a plain broom finish here has not read the controls. | draft |
| /decorative-concrete-harrington-park/ | /decorative-concrete-south-west-sydney/ | /concreters-harrington-park/ | The same Harrington Grove schedule sets width at 3m to 5.5m, average grade at 1:6, and requires the driveway to sit at least 500mm clear of kerb drainage structures and side fencing. The decorative finish is mandated, not optional, which changes the baseline price rather than the upgrade price. | draft |
| /concrete-driveway-replacement-harrington-park/ | /concrete-driveway-replacement-south-west-sydney/ | /concreters-harrington-park/ | The 1995-2010 stock is now 20 to 30 years old and failing at the edges and at the layback rather than mid-slab. Those driveways were poured thinner and with less reinforcement than current Camden spec, which is why replacement rather than resurfacing is usually the honest answer. | draft |
| /concrete-driveways-catherine-field/ | /concrete-driveways-south-west-sydney/ | /concreters-catherine-field/ | Catherine Field is mid-transition. On one street it is a 4.5m urban crossover to Camden's 32 MPa, 125mm, SL72 standard; two streets over it is an RU acreage lot needing a Council standard dish crossing aligned to the table drain invert plus a bitumen shoulder seal back to the pavement. Two completely different specs in one suburb. | draft |
| /shed-and-garage-slabs-catherine-field/ | /shed-and-garage-slabs-south-west-sydney/ | /concreters-catherine-field/ | The retained acreage lots carry machinery, floats and delivery trucks that a suburban shed slab never sees. Section thickness and access-run design are sized for that traffic, not for a garden shed. | draft |
| /concrete-paths-edmondson-park/ | /concrete-paths-south-west-sydney/ | /concreters-edmondson-park/ | A meaningful share of work here is strata rather than residential — common-area paths, bin-store slabs and shared driveway aprons where the client is an owners corporation. That means a committee resolution before work starts, different insurance requirements, and repeat work if the first job goes well. | draft |
| /concrete-patios-edmondson-park/ | /concrete-patios-south-west-sydney/ | /concreters-edmondson-park/ | Terraces and townhouses with no truck access mean courtyard slabs go in by barrow, kibble or line pump. That has to be priced at quote rather than discovered on the day. | draft |
| /concrete-driveways-edmondson-park/ | /concrete-driveways-south-west-sydney/ | /concreters-edmondson-park/ | Shared driveway aprons across lot boundaries raise a question no detached suburb raises: who pays. The answer sits in the strata plan or the easement, and it needs settling before anyone pours. | draft |
| /commercial-concreting-narellan/ | /commercial-concreting-south-west-sydney/ | /concreters-narellan/ | Narellan Town Centre and Smeaton Grange make this the LGA's commercial spine. The highest-value jobs are carpark slabs, loading aprons and warehouse floors that have to be poured overnight or in staged sections so the tenancy keeps trading. | draft |
| /concrete-driveway-replacement-narellan/ | /concrete-driveway-replacement-south-west-sydney/ | /concreters-narellan/ | Narellan and Narellan Vale residential stock dates from the 1980s and 90s and is at end of life. Unlike the growth corridor, nearly all residential work here is breaking out and rebuilding rather than pouring new. | draft |
| /concrete-driveway-replacement-mount-annan/ | /concrete-driveway-replacement-south-west-sydney/ | /concreters-mount-annan/ | Mount Annan was built out through the 1990s, so its concrete is now 25 to 30 years old — exactly the age where driveways fail at the edges and settle at the layback. The real question homeowners ask is resurface or replace, and the answer depends on whether the failure is surface-level or structural. | draft |
| /concrete-driveways-spring-farm/ | /concrete-driveways-south-west-sydney/ | /concreters-spring-farm/ | Spring Farm sits on genuinely sloping ground, which the flat growth-corridor releases do not. Camden requires an average driveway grade of 1:6 with controlled vertical curves, so blocks here regularly need stepped pours, integrated retaining and a scratch or broom finish for traction rather than a smooth decorative one. | draft |
| /concrete-crossovers-and-laybacks-spring-farm/ | /concrete-crossovers-and-laybacks-south-west-sydney/ | /concreters-spring-farm/ | Where the grade cannot meet Camden's standard specification the job goes to a Non-Standard Driveway Application with a written explanation of why. On the steeper Spring Farm blocks that is the normal path, not the exception. | draft |
| /concrete-patios-elderslie/ | /concrete-patios-south-west-sydney/ | /concreters-elderslie/ | Elderslie stock is mostly 2000s-era, which puts it in an awkward middle age — old enough that owners are upgrading outdoor areas, young enough that the driveway is still structurally sound. The work skews to adding rather than replacing: alfresco slabs, pergola bases, extended side access. | draft |
| /concrete-crossovers-and-laybacks-currans-hill/ | /concrete-crossovers-and-laybacks-south-west-sydney/ | /concreters-currans-hill/ | Currans Hill lots are noticeably smaller than Mount Annan or Harrington Park, so driveways are short, single-width and heavily trafficked. The dominant failure is settlement at the layback rather than mid-slab cracking, which changes whether you are repairing the crossover or the driveway. | draft |
| /concrete-driveway-replacement-currans-hill/ | /concrete-driveway-replacement-south-west-sydney/ | /concreters-currans-hill/ | Because the driveways are short, a full replacement here is often cheaper than the staged repair people expect to be quoted — the demolition and disposal is a smaller share of the job than on a longer drive. | draft |
| /concrete-driveways-cobbitty/ | /concrete-driveways-south-west-sydney/ | /concreters-cobbitty/ | Most Cobbitty frontages have no kerb and gutter, so Council requires a standard concrete dish crossing aligned to the table drain invert, plus a bitumen shoulder seal from the dish back to the edge of existing pavement. A pipe crossing is only permitted where a dish will not give suitable access, and only with Council approval. Three scope items most quotes leave off. | draft |
| /commercial-concreting-cobbitty/ | /commercial-concreting-south-west-sydney/ | /concreters-cobbitty/ | Machinery shed floors, stable slabs and workshop hardstands on acreage carry loads a residential slab never sees, on undisturbed profiles with no engineered fill. Section thickness and crossfall are sized for delivery trucks and plant. | draft |
| /commercial-concreting-bringelly/ | /commercial-concreting-south-west-sydney/ | /concreters-bringelly/ | Bringelly is the closest residential locality to the Aerotropolis build-out. Western Sydney International opens to freight from July 2026 and passengers in October 2026, and private project value around the Aerotropolis has risen from $9.8bn to $21.6bn in fourteen months. The work here is industrial floors, hardstands and yard slabs for clients who tender rather than take a homeowner quote. | draft |
| /concrete-slabs-bringelly/ | /concrete-slabs-south-west-sydney/ | /concreters-bringelly/ | Documented sulfate concentrations near western Sydney creek lines make aggressivity assessment under AS 2159 a real design input on industrial slabs here, not a formality skipped to save a week. | draft |

## Checks

- Total reconciled pages: 156
- Suburbs: 60
- Camden Council: 20
- Liverpool City Council: 20
- Campbelltown City Council: 12
- Wollondilly Shire Council: 8
- Suburb publish/draft split: 6 publish, 54 draft
- Researched suburb count: 15
- REQUIRED-RESEARCH suburb count: 45
- Intersection pages: 35 listed, all draft
- Guide hub: 1, draft, root-level post with `post_name=guides`
- Guide hierarchy: all 35 guides are children of the guide hub and use only their final URL segment as `post_name`
- Other nested URLs requiring a parent: 0

## Exclusions

- No /concreters-camden/ page.
- No /concreters-camden-town/ page.
- No Denham Court or Bardia suburb page.
- 145 unvalidated intersections remain unbuilt.

## Deletions from source WXR

- hello-world
- privacy-policy
- __trashed-3

GATE 0: PASS
  ? Revised total: 156 pages
  ? 1 homepage: /
  ? 4 utility pages: about, contact, quote, gallery
  ? 10 service pages: listed
  ? 60 suburb pages: listed from suburbs-expanded.json
  ? 35 intersection pages: exactly the entries in intersection-differentiators.json
  ? 1 draft guide hub: /guides/
  ? 35 guide pages: listed
  ? 10 cost/comparison pages: listed
  ? 4 LGAs: Camden 20, Liverpool 20, Campbelltown 12, Wollondilly 8
  ? Publish/draft split for suburbs: 6 publish, 54 draft
  ? All intersections have an existing parent suburb and parent service
  ? No Camden, Denham Court or Bardia suburb page
  ? Deletions include hello-world, privacy-policy, __trashed-3

AWAITING APPROVAL. Reply "continue" to proceed to Stage 1.
