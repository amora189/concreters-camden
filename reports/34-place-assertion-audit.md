# Stage 34 — extended place-assertion detector (D18)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-03-coherence-and-dispositions.md` §D18.
Data: `reports/34-place-assertion-audit.csv`.

D18: *"Two detectors have now under-reported; assume a third gap."* There was one, and it is the worst
of the three.

---

## The detector, extended

The Stage 24 detector tested suburb names only. Extended to seven categories:

```text
  suburb_nsw     Camden, Oran Park, Narellan, Leppington, ... (24 names)
  region         South West Sydney, Macarthur
  watercourse    South Creek, Nepean, Georges River, creek, catchment, corridor
  council_lga    council, LGA, Liverpool, Campbelltown, Wollondilly
  geology        Wianamatta, shale, clay, soil, reactive, basalt, sandstone, alluvial
  estate_park    estate, precinct, podium, reserve, homestead, park, gardens
  road           -road, -drive, -avenue, -street, -parade, -way, -highway
```

Re-run against all 83.

```text
  filenames asserting a place, any category      83 of 83
  previously caught by the Stage 24 detector           20
  newly caught                                         63
  of the newly caught, Victorian source provenance      1

  category tally  suburb_nsw 76, region 6, road 4, geology 3, watercourse 2,
                  council_lga 2, estate_park 2
```

### Read that 83 carefully — most of it is a naming convention, not a lie

Stage 8 appended `-camden-<id>` to **every** filename. So `exposed-aggregate-concrete.jpg` became
`exposed-aggregate-concrete-camden-50.jpg`. That is a weaker claim than renaming a Tarneit soil photo to
`wianamatta-shale-clay-camden-1020.jpg`, but it is not nothing: the image sits on 69 pages with alt text
"Exposed aggregate concrete camden", asserting the photograph is of Camden work.

```text
  TIER 1  place substituted for a different place        20   the original 20
  TIER 2  generic image given a "-camden-" suffix        60   systematic, from the Stage 8 convention
  TIER 3  AI-generated images                             3   see below — the real gap
```

Tier 2 is a **naming-convention decision to reverse**, not 60 separate falsehoods. Per D20 the fix is one
operation across filename, attachment title and per-page alt text.

---

## THE THIRD GAP — three AI-generated images, one live on 14 pages

Neither previous detector looked for this, and it is a direct breach of standing rule 3: *"Never
generate, synthesise, upscale or substitute an image that could be mistaken for a real Camden job
photo."*

```text
  ID    ORIGINAL FILENAME                                        CURRENT FILENAME                                          PAGES
  272   cropped-ChatGPT-Image-Jul-6-2026-01_52_19-PM.png         cropped-chatgpt-image-...-pm-camden-272.png                  14
  159   ChatGPT-Image-Jul-6-2026-01_52_19-PM.png                 chatgpt-image-...-pm-camden-159.png                           0
  177   cropped-ChatGPT-Image-Jul-6-2026-07_59_41-PM.png         cropped-chatgpt-image-...-pm-camden-177.png                   0
```

**Attachment 272 is live on 14 pages** and named `...-camden-272.png` with alt text "Cropped chatgpt
image jul 6 2026 01 52 19 pm camden". The pages it appears on:

```text
  /camden-council-driveway-crossing/          /concrete-crossovers-and-laybacks-oran-park/
  /coloured-concrete-driveway-cost/           /concrete-crossovers-and-laybacks-south-west-sydney/
  /concrete-crossovers-and-laybacks-austral/  /concrete-crossovers-and-laybacks-spring-farm/
  /concrete-crossovers-and-laybacks-currans-hill/  /driveway-cost-calculator/
  /concrete-crossovers-and-laybacks-leppington/    /exposed-aggregate-driveway-cost/
  /concrete-driveway-cost-nsw/                /plain-concrete-driveway-cost/
  /slab-volume-calculator/                    /stencilled-concrete-driveway-cost/
```

159 and 177 are unreferenced by page content, which means they sit in **theme mods** — the same place the
logo lives. Given 177's original name is `cropped-...`, it is a plausible favicon or logo candidate,
which would mean the site's mark is AI-generated as well as being the source business's symbol.

```text
  STATUS   FLAGGED, NOT CLASSIFIED. Standing rule 3 is unambiguous that generated
           imagery must not be used, but these predate this session and their
           disposition is an owner decision. I have not removed or renamed them.

  OWNER QUESTION
  Attachment 272 is an AI-generated image published on 14 pages. Remove it, or
  replace it under the D18 brief? And are 159/177 the site's logo/favicon?
```

---

## Dispositions carried out from D18

None applied to the artifact — every change below is a **post-import edit**, and
`camden-concreting-import.xml` is immutable. Recorded for the runbook:

```text
  1151  reactive-clay-concreter-camden-1151.jpg
        -> proposed: concrete-slab-on-reactive-ground-01.jpg
        alt: "Concrete slab poured over prepared reactive ground"
        no geographic or geological assertion; the reactive-clay claim moves to
        body copy where it can carry a source

  1188  reactive-clay-concreter-1-camden-1188.jpg
        -> proposed: reinforced-slab-preparation-01.jpg
        alt: "Reinforcing mesh laid before a slab pour"

  1056  south-creek-drainage-corridor-1056.jpg
        -> proposed: open-drainage-channel-01.jpg
        alt: "Open drainage channel beside a residential area"
        decorative on 14 pages; renamed rather than removed, per D18

  306/307/422  logos — HOLD. Commission a distinct CoreX mark. Until then the site
        ships with no logo rather than another business's favicon. Recorded as an
        owner task.

  1020  soil image — REMOVE, sections retained (D19).
```

**Per D20**, each rename updates filename, attachment title and per-page alt text as one verified
operation. A renamed file with its original title still asserts the same place.

---

## Assume a fourth gap

Three detectors have now under-reported. What this scan still does **not** cover:

```text
  - image CONTENT. Every check here reads filenames and alt text. Nothing has
    looked at the pixels, and the binaries do not exist locally to look at.
    A photograph of a Melbourne streetscape with an honest filename still shows
    Melbourne. QA check H4 is the only thing that catches it, and it is
    human-sighted.
  - EXIF and embedded metadata, which may carry GPS coordinates, camera owner or
    the source business's name. reencode-images.sh strips EXIF, but it has never
    parsed, so no image in this build has been stripped.
  - reverse-image provenance. Whether any of the 83 is licensed at all is unknown.
```

The EXIF point is material: **if the binaries arrive and are imported without a working re-encode step,
any embedded GPS or owner metadata travels with them onto a public site.**
