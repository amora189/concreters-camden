# GATE 24 — image distribution and alt-text audit

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.24; `RUN-BLOCK-01.md` §A D5, D7.

---

## TOP OF REPORT — source-site imagery occupying Camden-specific slots

§4.24.4 requires this first because it is a false-claim risk, not a cosmetic one.

**20 of the 83 images are Victorian photographs renamed to specific NSW places.** They are not generic
concrete textures given a tidier filename. They are geographically specific photographs of Victorian
suburbs, relabelled as geographically specific NSW suburbs, and in several cases given alt text asserting
the NSW location.

```text
   ID   ORIGINAL FILENAME                                        RENAMED TO                                            PAGES
  226   concretejob2werribee.jpg                                 concretejob2camden-226.jpg                               14
  480   pointcook1.webp                                          oran-park1-480.webp                                      14
  481   pointcook2.webp                                          oran-park2-481.webp                                      14
  482   pointcook3.webp                                          oran-park3-482.webp                                      14
  906   excavation-werribee.jpg                                  driveway-excavation-camden-906.jpg                       14
  907   werribee-town.jpg                                        camden-town-centre-907.jpg                               14
  908   new-estates-werribee.jpg                                 oran-park-growth-estate-908.jpg                          14
  924   coloured-concrete-melbourne.png                          coloured-concrete-south-west-sydney-924.png              15
  925   stencil-concrete-melbourne.webp                          stencil-concrete-south-west-sydney-925.webp              15
  926   stamped-copncrete-melbourne.jpg                          stamped-concrete-south-west-sydney-926.jpg               15
  956   melbournes-west.png                                      south-west-sydney-growth-corridor-956.png                15
 1020   TARNEIT-SOIL.jpg                                         wianamatta-shale-clay-camden-1020.jpg                    15
 1056   davis-creek-tarneit.jpg                                  south-creek-drainage-corridor-1056.jpg                   14
 1150   1970s-home-hoppers-crossing.jpg                          established-home-mount-annan-1150.jpg                    14
 1152   hoppers-crossing-aerial-shot.jpg                         mount-annan-established-housing-1152.jpg                 14
 1185   crossovers-concrete-truganina.jpg                        council-crossing-south-west-sydney-1185.jpg              14
 1186   truganina-commercial.webp                                gregory-hills-commercial-concreting-1186.webp            14
 1187   new-estates-truganina.jpg                                leppington-new-estates-1187.jpg                          14
  306   e_t_co_concreters_favicon_512_symbol_only.png            corex-concreters-camden-logo-306.png                      8
  307   cropped-e_t_co_..._symbol_only.png                       corex-concreters-camden-logo-307.png                      2

  images with Victorian provenance                     21
  of those, renamed to a specific NSW place            20
  pages carrying at least one renamed Victorian image  85  of 156
```

Full detail: `reports/24-source-provenance.csv`.

### Why these are not equivalent

Three are materially worse than the rest, because the image is the evidence for a factual claim about
Camden ground conditions or geography:

```text
  1020  TARNEIT-SOIL.jpg -> wianamatta-shale-clay-camden-1020.jpg
        A photograph of Tarneit soil (Victorian basalt plains) presented as Wianamatta shale
        clay in Camden. These are different geologies. The image appears on 15 pages, in the
        module that explains local ground conditions.

  1056  davis-creek-tarneit.jpg -> south-creek-drainage-corridor-1056.jpg
        A Victorian creek presented as the South Creek drainage corridor, on 14 pages, in the
        drainage and levels module.

   907  werribee-town.jpg -> camden-town-centre-907.jpg
        A photograph of Werribee town centre presented as Camden town centre, on 14 pages.
```

The logo files (306, 307, 422) are a separate and benign case: the source business's favicon reused as the
CoreX logo. That is a branding decision for the owner, not a false geographic claim — but the owner should
know the current logo is the source business's symbol.

### Disposition

This is **not** a defect to fix by editing the validated artifact. Standing rule 6 and D5 forbid mutating
`camden-concreting-import.xml`, and standing rule 3 forbids generating or substituting a replacement image.

```text
  action required   OWNER DECISION, recorded as a blocker
  options           (a) supply genuine Camden photographs for these 20 slots, or
                    (b) accept generic non-geographic imagery and rewrite the alt text and
                        any surrounding copy that asserts the location, or
                    (c) withdraw the geographic claim from the affected modules
  what is forbidden generating, synthesising, upscaling or sourcing a substitute image
  status            none of the 20 may go live in a geographically-asserting slot
```

### Relationship to `REAL_PHOTO_PENDING`

Distinct problems, both live:

```text
  REAL_PHOTO_PENDING markers        47 occurrences across 16 pages — slots that are EMPTY and
                                    correctly marked as awaiting a real photograph
  renamed Victorian imagery         20 images across 85 pages — slots that are FILLED, and
                                    filled with something that misrepresents its subject
```

The marked-empty case is honest. The filled case is the one that reads as correct and is not. Per
`RUN-BLOCK-01.md` §A D7 the rule is unchanged and is satisfied: no `REAL_PHOTO_PENDING` slot is currently
filled by a re-encoded source-site image, because those slots are empty. The exposure is the 85 pages where
a relabelled image sits in an unmarked slot.

---

## 1. Image distribution

`reports/24-image-distribution.csv`. Denominator **157** per D1; the calculator contributes **zero** image
references because it is not yet built, and that is stated rather than omitted.

```text
  attachments                                  83
  referenced by at least one page              73
  unreferenced (logo / site identity)          10   carried in Astra theme mods, not page content
  denominator                                 157
  cap (expansion §9)                           15   pages per image
  over cap                                      2
  exactly at cap                               19
  maximum concentration                        69   pages, attachment 50
```

### Over-cap images and redistribution proposals

Flagged only; **no redistribution performed**, per §4.24.2.

```text
IMAGE 1 of 2
  attachment_id   50
  filename        exposed-aggregate-concrete-camden-50.jpg
  alt             Exposed aggregate concrete camden
  pages           69 of 157  (44.0% of the site)
  over cap by     54 pages
  proposal        This single image carries the exposed-aggregate finish across nearly half the
                  site. Redistribute across the finish-specific images already in the pool
                  (924 coloured, 925 stencil, 926 stamped) so each finish module shows its own
                  finish, and reserve 50 for the exposed-aggregate service and cost pages only.
                  Target: no more than 15 pages.

IMAGE 2 of 2
  attachment_id   1232
  filename        heave-cracks-camden-1232.jpg
  alt             Heave cracks camden
  pages           48 of 157  (30.6% of the site)
  over cap by     33 pages
  proposal        Used as the generic "cracking" illustration on every suburb page's crack
                  control module. Because the module is meant to be rewritten per suburb around
                  that suburb's real water and level problem (see the built module 6 contract),
                  a single shared crack photograph undercuts the module's purpose. Redistribute
                  once genuine per-suburb photography exists; until then this is a photography
                  blocker, not an image-management one.
```

Nineteen further images sit exactly at 15 pages. They are at the cap, not over it, so they do not fail —
but a cap described as "~15" in expansion §9 with 19 images pinned exactly to it suggests the pool was
sized to the cap rather than to the content. Recorded as an observation, not a failure.

---

## 2. Alt-text duplication

`reports/24-alt-duplication.csv`.

```text
  attachments with alt text set                    83 of 83
  distinct alt strings                             72
  attachments used on more than one page           73
  attachments whose alt therefore repeats verbatim 73
  total (image, page) occurrences needing per-page alt   1,112
```

Alt text is stored once on the attachment record (`_wp_attachment_image_alt`), so **every image reused
across pages repeats its alt verbatim on every one of those pages by construction**. This is not an
oversight in a few places; it is the structural default, and it affects 73 of the 73 reused images.

Two alt strings are additionally shared across *different* attachments:

```text
  "Concrete project detail camden"   3 attachments (17, 18, 19)
  "Corex concreters camden logo"    10 attachments
```

The logo case is legitimate — same logo, same alt. The "Concrete project detail camden" case is three
different photographs sharing one generic description.

### Quality observations

```text
  lowercase place name       every alt ends "camden" rather than "Camden"
  typo                       attachment 46: "Concrete tesimonial 4 camden"
  non-descriptive pattern    "Concrete testimonial 1/3/4/6 camden" describes the slot, not the image
```

None of these is fixable by mutating the validated artifact. They are post-import edits, and they belong
in the post-import runbook alongside the guide-side link edits.

---

## 3. D5 mitigation check — Elementor kit palette

D5 requires checking mitigation 5 and recording it identically to mitigation 4.

```text
  HEX COLOUR   MAIN WXR   SOURCE WXR   SHARED
  #324A6D           901          194   yes
  #467FF7           851          136   yes
  #1C244B           732          141   yes
  #FFFFFF           522           72   yes
  #020101           393           56   yes
  #F3F5F8           266           71   yes
  #435963           238           20   yes
  #C8D5DC            83           32   yes

  verdict   mitigation 5 NOT APPLIED — the Elementor kit palette is unchanged from source
  status    residual footprint risk, recorded not fixed
  reason    varying it would require mutating the validated artifact, which D5 forbids
```

Recorded in the ledger under `residual_footprint_risks.mitigation_5_kit_palette`, identically to
mitigation 4 (module order).

---

## 4. `CONTEXT.md` update and diff

```text
  Latest completed stage       23 -> 24
  New residual footprint risk  kit palette unchanged from source (mitigation 5 NOT APPLIED)
  New blocker                  20 Victorian images renamed to specific NSW places, on 85 pages
  New post-import task set     1,112 per-page alt strings; 2 over-cap redistributions
  Index-ready                  0 of 157 — UNCHANGED
  Launch gate                  NO-GO — UNCHANGED
```

No blocker cleared.

---

## 5. Hash table

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

## GATE 24 RESULT — the three required counts

```text
  images over the ~15-page cap                                    2
  alt strings duplicated across pages                            73 images, 1,112 occurrences
  pending-photo slots occupied by source-site imagery              0

  Fourth count, not requested but material:
  images with Victorian provenance renamed to a specific NSW place  20, across 85 pages

  GATE 24: PASS as an audit. The audit's finding is severe.
  The third count is zero only because those slots are empty and honestly marked.
  The fourth count is the real exposure and is now an owner blocker.
```
