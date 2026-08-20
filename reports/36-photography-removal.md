# Stage 36 — evidential module removal (D32)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-06-resolvable-items.md` §D32.
Data: `reports/36-module8-removal.csv`, `reports/36-evidential-modules.csv`.

**Settled fact, not a pending input:** no Camden job has been completed, none is scheduled, and
fulfilment is Pakenham. The 47 `REAL_PHOTO_PENDING` slots have no path to being filled.

---

## 1. Page-by-page consequence (D32.4)

16 pages carry evidential slots. Removing the module — not just the image — costs **427 words in total**.

```text
  PAGE                          CLASS     STATUS    TOTAL   LOST   LEFT      %   RPP
  gallery                       utility   publish     108     58     50   53.7%    2
  concreters-currans-hill       suburb    draft     1,124     27  1,097    2.4%    3
  concreters-elderslie          suburb    draft     1,046     24  1,022    2.3%    3
  concreters-mount-annan        suburb    draft     1,243     27  1,216    2.2%    3
  concreters-gregory-hills      suburb    publish   1,257     27  1,230    2.1%    3
  concreters-catherine-field    suburb    draft     1,266     27  1,239    2.1%    3
  concreters-edmondson-park     suburb    draft     1,258     27  1,231    2.1%    3
  concreters-narellan           suburb    draft     1,166     24  1,142    2.1%    3
  concreters-spring-farm        suburb    draft     1,306     27  1,279    2.1%    3
  concreters-gledswood-hills    suburb    publish   1,329     27  1,302    2.0%    3
  concreters-harrington-park    suburb    publish   1,374     27  1,347    2.0%    3
  concreters-cobbitty           suburb    draft     1,194     24  1,170    2.0%    3
  concreters-leppington         suburb    publish   1,232     24  1,208    1.9%    3
  concreters-austral            suburb    publish   1,249     24  1,225    1.9%    3
  concreters-bringelly          suburb    draft     1,242     24  1,218    1.9%    3
  concreters-oran-park          suburb    publish   1,881      9  1,872    0.5%    3

  TOTAL                                            19,275    427 18,848          47
```

### Why the cost is so low

The evidential sections are almost entirely the markers themselves, with no surrounding prose:

```text
  /concreters-currans-hill/  section body, verbatim and complete:
    "[[REAL_PHOTO_PENDING: verified CoreX project in Currans Hill]]
     [[REAL_PHOTO_PENDING: verified CoreX project in Currans Hill]]
     [[REAL_PHOTO_PENDING: verified CoreX project in Currans Hill]]"
```

There is no "recent work" copy to lose. The module was a frame around three empty slots. **Removing it
removes nothing a reader would miss**, which is the clearest possible confirmation that it should go.

### Word-count floors

```text
  suburb pages dropping below any floor      0 of 15
  smallest surviving suburb page             1,022 words (Elderslie)
  no sourced word-count floor exists for any class
```

### Gallery is the exception, and it is a page-level decision

```text
  /gallery/   108 words total, 58 of them the evidential section
              after removal: 50 words, and no photographs

  A gallery with no images is not a gallery.
```

Three options, none of which I have taken:

```text
  (a) WITHDRAW the page, as with the guides and intersections. It has no content
      and no path to content.
  (b) REPURPOSE it as a finishes page using generic licensed imagery under the
      held Phase 2 briefs, renamed so it does not claim to show the operator's work.
  (c) KEEP it empty and noindexed indefinitely.

  RECOMMENDATION: (a) or (b). Option (c) leaves a linked, published, empty page.
  This is an owner decision and is recorded, not taken.
```

---

## 2. The Tier 1 photography hold (D32.4)

The six Tier 1 suburbs were held `noindex,follow` pending photography and evidence. The photography half
will never arrive.

```text
  TIER 1 PAGE                  PHOTOGRAPHY HOLD     OTHER BLOCKERS REMAINING
  concreters-oran-park         RELEASABLE           unattested figures (D26)
  concreters-gregory-hills     RELEASABLE           unattested figures (D26)
  concreters-gledswood-hills   RELEASABLE           unattested figures (D26)
  concreters-harrington-park   RELEASABLE           unattested figures (D26)
  concreters-leppington        RELEASABLE           Liverpool council spec (D13)
  concreters-austral           RELEASABLE           Liverpool council spec (D13)

  plus, on all six:  pricing placeholders, ABN, business address, phone routing
```

**The photography hold can be released on all six.** It is the first blocker in this project to be
*cleared* rather than deferred — but it clears one hold on pages that carry three or four others, so no
page becomes releasable as a result.

Recorded honestly: this reduces the blocker count, not the block.

---

## 3. Decorative versus evidential (D32.2 and D32.3)

```text
  EVIDENTIAL - module removed, no replacement
    47 REAL_PHOTO_PENDING slots across 16 pages
    function: to evidence completed local work
    a stock photograph here is a false claim however it was licensed

  DECORATIVE - eligible for generic licensed imagery under the held Phase 2 briefs
    the 16 REPLACE slots in reports/33-image-replacement-spec.csv
    function: illustration, not evidence
    honest filenames, alt text asserting nothing geographic or evidential
    STILL HELD - sourcing does not resume until after the service rebuild (D18)
```

The distinction is the module's function, not the image's quality.

---

## 4. Reopening condition (D32.5)

```text
  This decision is revisited if, and only if, a Camden job is completed AND
  photographed AND the property owner's permission to publish is obtained.

  At that point: the module returns to the affected page, the photograph fills the
  slot, and the page re-enters the readiness record with the photography blocker
  cleared by evidence rather than by removal.

  Until then this is settled, not pending. Item 6 is removed from the owner input
  pack.
```

---

## 5. A finding outside D32's scope that D32's premise surfaces

D32 states fulfilment is Pakenham. **Pakenham is in Victoria**, roughly 900km from Camden. That is the
same state as the source business this site was cloned from, and it bears on more than photography.

I checked what the existing copy actually claims about location, because the answer determines how far
this reaches:

```text
  CLAIM TYPE                                    SENTENCES   PAGES
  "locally based" / "locally owned"                     0       0
  "our crew" / "we pour" / "our yard"                   0       0
  "years in the area" / "established <year>"            0       0
  same-day / response-time claims                       0       0
  "AREAS WE COVER AROUND <SUBURB>" headings            16      16
```

**The page copy makes no local-presence claim.** It never says the business is based in Camden, has a
yard there, or has worked there for years. That is a genuinely good outcome and it means the Pakenham
fact does not invalidate the existing copy.

Two things it does bear on:

```text
  1  THE TAGLINE. The Elementor kit declares site_description as
     "Camden based Concrete Company Site". That IS a location claim, it is in the
     immutable artifact, and it is not supportable. Recorded in
     reports/36-source-name-sweep.md and in the Stage 29 runbook as step 14.

  2  SERVICE AREA. The 16 "AREAS WE COVER" headings are true only if the business
     will genuinely travel to those suburbs and work there. That is a business
     question, not a documentation one. data/verified-facts.yml carries
     service_areas as an unverified required field, and it should be answered on
     the basis of where work will actually be done - not where pages exist.
```

Neither is a reason to stop. Both are recorded so the answer is given deliberately rather than inherited.

---

## 6. Implementation

```text
  method        post-import edits; camden-concreting-import.xml is immutable
  scope         remove the evidential section on 16 pages
  cost          427 words
  pages below a floor after removal    0
  gallery       owner decision required, see §1
  recorded in   reports/post-import-tasks.md and the Stage 29 runbook
```
