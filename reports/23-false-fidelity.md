# False-fidelity claim register

Commissioned by `DECISION-02-evidence-markers.md` §D11.3. Produced at handoff-state, before Stage 22.
Date: 18 August 2026 (Australia/Sydney).

**Status of this artifact.** Stage 23 has not run. This is the D11.3 scan delivered on its own terms so the
scope of the pattern is known before Wave 1 planning depends on it. Stage 23 must re-run it as part of the
full evidence register and confirm or extend these findings; it must not treat this file as a substitute
for that scan.

---

## What was searched, and how

Corpus: rendered body copy of all **156** pages in `camden-concreting-import.xml`. Body copy is taken from
Elementor **content** fields (`editor`, `title`, `text`, `html`, `testimonial_*`, `item_description`,
`tab_content`, and the rest of the content-key set) plus `content:encoded`. Settings and style strings —
font names, colours, widget IDs, spacing values — are excluded.

**Discriminator.** Every `[[...]]` marker is stripped from the sentence first; the fidelity test then runs
against the **remaining prose**. This distinction is the whole method:

- `[[PLACEHOLDER: verified CoreX ABN]]` — a correctly formed marker *requesting* a verified value.
  **Not a false-fidelity claim. Not counted.**
- `The recorded Leppington council specification is reproduced without alteration: REQUIRED-RESEARCH: ...`
  — prose *asserting* that reproduction already occurred, wrapped around a marker proving it did not.
  **Counted.**

A first pass that omitted this discriminator, and that also walked the whole Elementor settings tree,
returned 51 hits. That number was an artifact of the method and is discarded. The corrected figure is 6.

Fidelity terms tested: reproduced, reproduced without alteration, without alteration, verbatim, unaltered,
as recorded, the recorded, recorded, verified, confirmed, sighted, exactly as, unchanged from, as supplied,
as published.

---

## Result

**6 false-fidelity sentences across 4 pages.** D11 anticipated four; the scan found **two more**, both on
Bringelly, both of a different construction than the one D11 described.

```text
  by page class   suburb 6
  by status       publish 2, draft 4
  councils named  Liverpool 4
  pages affected  concreters-leppington, concreters-austral,
                  concreters-edmondson-park, concreters-bringelly
```

**Scope note added 19 August 2026.** The count of 6 above is the *prose sentence* scan and is
unchanged. False-fidelity claims that are made by a non-textual element — an image, a badge, an
icon — are outside what the sentence scan can see, and are registered separately in section **NT**
below. The first such claim, NT-1, was found during the Stage 22 media intake audit.

Campbelltown and Wollondilly do not appear in any false-fidelity sentence. The three Campbelltown,
Liverpool and Wollondilly `[[VERIFY: ...]]` guide markers are correctly formed and are **not** in this
register.

---

## The six, in full

```text
FALSE-FIDELITY 1 of 6
  page       /concreters-leppington/
  class      suburb
  status     publish
  wave       1 (Tier 1)
  triggers   recorded, reproduced, reproduced without alteration, the recorded, without alteration
  sentence   The recorded Leppington council specification is reproduced without alteration:
             REQUIRED-RESEARCH: confirm Liverpool City Council vehicle crossing specification, widths,
             strength and fee schedule at liverpool.nsw.gov.au.
  fault      Asserts reproduction of a specification that was never supplied.

FALSE-FIDELITY 2 of 6
  page       /concreters-austral/
  class      suburb
  status     publish
  wave       1 (Tier 1)
  triggers   recorded, reproduced, reproduced without alteration, the recorded, without alteration
  sentence   The recorded Austral council specification is reproduced without alteration:
             REQUIRED-RESEARCH: confirm Liverpool City Council vehicle crossing specification, widths,
             strength and fee schedule at liverpool.nsw.gov.au.
  fault      Asserts reproduction of a specification that was never supplied.

FALSE-FIDELITY 3 of 6
  page       /concreters-edmondson-park/
  class      suburb
  status     draft
  wave       not in Wave 1
  triggers   recorded, reproduced, reproduced without alteration, the recorded, without alteration
  sentence   The recorded Edmondson Park council specification is reproduced without alteration:
             REQUIRED-RESEARCH: confirm Liverpool City Council vehicle crossing specification, widths,
             strength and fee schedule at liverpool.nsw.gov.au.
  fault      Asserts reproduction of a specification that was never supplied.

FALSE-FIDELITY 4 of 6
  page       /concreters-bringelly/
  class      suburb
  status     draft
  wave       not in Wave 1
  triggers   verified
  sentence   The verified approval path for Bringelly is: VERIFY the governing LGA per lot on the NSW
             Planning Portal before quoting.
  fault      NOT ANTICIPATED BY D11. Different construction: asserts the approval path is verified, then
             instructs the reader to verify it. The bare VERIFY carries no [[...]] wrapper, so a
             bracket-keyed marker gate does not see it.

FALSE-FIDELITY 5 of 6
  page       /concreters-bringelly/
  class      suburb
  status     draft
  wave       not in Wave 1
  triggers   recorded, reproduced, reproduced without alteration, the recorded, without alteration
  sentence   The recorded Bringelly council specification is reproduced without alteration:
             REQUIRED-RESEARCH: confirm Liverpool City Council vehicle crossing specification, widths,
             strength and fee schedule at liverpool.nsw.gov.au.
  fault      Asserts reproduction of a specification that was never supplied.

FALSE-FIDELITY 6 of 6
  page       /concreters-bringelly/
  class      suburb
  status     draft
  wave       not in Wave 1
  triggers   verified
  sentence   For Bringelly, the verified project record says: VERIFY the governing LGA per lot on the NSW
             Planning Portal before quoting.
  fault      NOT ANTICIPATED BY D11. Asserts a "verified project record" exists. Per standing rule 1 no
             completed job may be claimed without evidence, so this sentence claims two unverified
             things at once: that a project record exists, and that it is verified.
```

---

## Disposition per D11.2

None of the six may be closed by filling the marker alone.

| # | Page | Sentence may stand only if | Otherwise |
|---:|---|---|---|
| 1 | Leppington | Liverpool City Council specification inserted **verbatim**, with `source_url` and `sighted_date` | Rewrite the sentence |
| 2 | Austral | Same | Rewrite the sentence |
| 3 | Edmondson Park | Same | Rewrite the sentence |
| 5 | Bringelly | Same | Rewrite the sentence |
| 4 | Bringelly | **Cannot stand.** No approval path can be described as verified while the governing LGA is unresolved | Rewrite |
| 6 | Bringelly | **Cannot stand.** Claims a verified project record; no completed job may be claimed without evidence (standing rule 1) | Rewrite |

Items 4 and 6 are not fillable. There is no value that makes *"the verified project record says: VERIFY"*
a true sentence. They require rewriting regardless of what the owner supplies.

Per D12.2, none of the four Liverpool figures may be filled from a neighbouring suburb, from Camden
Council, or from any other LGA. Leppington additionally straddles the Camden/Liverpool boundary per
`intersection-differentiators.json`, so a Camden figure is wrong there for a second, independent reason.

---

## Wave impact per D13

Leppington and Austral are `publish` and Tier 1, so they sit in the 21-page Wave 1 release set. Both were
already held `noindex,follow` under the Tier 1 photography and evidence gate. The Liverpool specification
is therefore a **second, independent blocker on already-held pages**, and clearing either one alone does
not release the page.

```text
  21  pages at publish status in the main WXR (Wave 1 release set)
  -6  Tier 1 suburb pages held noindex,follow (Oran Park, Gregory Hills, Gledswood Hills,
      Harrington Park, Austral, Leppington)
  -1  Gallery held noindex,follow
  =14 effective indexable

  => effective indexable Wave 1 remains 14. Confirmed against the artifacts, not assumed.
```

Edmondson Park and Bringelly are `draft` and enter no wave until researched.


---

## NT — Non-textual false-fidelity claims

A false-fidelity claim does not have to be a sentence. An image can assert the same thing a sentence
asserts, and the D11.3 prose scan cannot see it. This section registers claims carried by assets.

### NT-1 — `verified-badge` graphic

```text
  asset          verified-badge-e1784545689665-camden-1067.avif
  attachment id  1067
  source asset   verified-badge-e1784545689665.avif (E&T Melbourne uploads, 2026/07)
  found by       Stage 22 media intake audit, 19 August 2026
  register       NOT previously in any register — not in 23-false-fidelity.md, not in
                 23-evidence-register.csv, not in 23-owner-questions.md
  pages          14 (1 publish, 13 draft)
  claim          A verification badge asserts that some entity, licence, insurance or
                 credential has been verified by someone.
  fault          There is no verified entity behind this site. Phase C is BLOCKED with
                 legal_name, abn, nsw_fair_trading_licence, insurance_public_liability,
                 street_address, is_staffed and phone all verified:false in
                 data/verified-facts.yml — 0 of 20 fields verified:true. The badge therefore
                 asserts a verification that has not occurred, names no verifying body, and
                 points at no credential. It is an unsupported claim under standing rule 1.
  aggravating    The badge is inherited artwork from the E&T Melbourne site. Even if CoreX
                 Concreters Camden were later verified, this graphic would not be evidence of
                 it; it would be evidence of nothing, reused.
  alt text       Every one of the 14 instances carries alt text beginning "Verified badge",
                 so the claim is also made to assistive technology and to search engines,
                 not only visually.
```

**Second, independent fault on three pages.** On `concreters-camden-south`, `concreters-glen-alpine`
and `concreters-west-hoxton` the badge is not used as a badge at all — it is the image of an
Elementor image-box service tile titled *Concrete Slabs*, *Paths & Pathways* and *Concrete Driveways*
respectively. There the asset is both an unsupported verification claim and an image whose subject
does not depict what its tile says it depicts. That is the §4.22.4 pixel-verification failure class,
found here by filename rather than by sighting.

### NT-1 — pages affected

```text
   #  status   post_id  page                                                 badge use
   1  publish  221      /concreters-leppington/                              standalone image
   2  draft    1372     /concreters-narellan/                                standalone image
   3  draft    1376     /concreters-currans-hill/                            standalone image
   4  draft    1380     /concreters-camden-south/                            image-box "Concrete Slabs"
   5  draft    1391     /concreters-west-hoxton/                             image-box "Concrete Driveways"
   6  draft    1414     /concreters-glen-alpine/                             image-box "Paths & Pathways"
   7  draft    1427     /guides/wollondilly-council-driveway-crossing/        standalone image
   8  draft    1429     /guides/do-i-need-council-approval-driveway-nsw/      standalone image
   9  draft    1445     /guides/coloured-concrete-explained/                  standalone image
  10  draft    1456     /guides/removing-oil-stains-and-tyre-marks-from-concrete/  standalone image
  11  draft    1472     /concrete-slabs-leppington/                          standalone image
  12  draft    1485     /concrete-driveways-catherine-field/                 standalone image
  13  draft    1493     /concrete-driveways-spring-farm/                     standalone image
  14  draft    1497     /concrete-driveway-replacement-currans-hill/         standalone image
```

Counts verified against `camden-concreting-import.xml` directly: 15 items reference the asset — the
14 pages above plus attachment item 1067 itself, which accounts for 9 of the 23 raw string
occurrences (its own URL plus generated size variants).

### NT-1 — wave impact

`concreters-leppington` is `publish` and sits in the 21-page Wave 1 release set. It already carries
false-fidelity sentence 1 of 6 and is already held `noindex,follow` under the Tier 1 photography and
evidence gate. NT-1 is a **third independent blocker on that page**. The effective indexable Wave 1
count is unchanged at 14 — Leppington was already held, so nothing is added to or removed from the
held set by this finding.

The other 13 pages are `draft` and enter no wave.

### NT-1 — disposition

The badge cannot be closed by supplying a value, and it cannot be closed by Phase C alone.

```text
  1. REMOVE the asset from all 14 pages. This is the default and it is not blocked by any
     owner input — it requires no verified fact, only deletion.
  2. On the three image-box tiles, remove the image setting and preserve the service text/link.
     The empty slot is NOT replaced. Owner verdict, 20 August 2026.
  3. The badge may be reinstated ONLY if the owner supplies a named verifying body, the
     credential verified, and a source that can be sighted — at which point it stops being a
     false-fidelity claim and becomes an evidence-backed one. Absent all three it does not
     return, and Phase C completing does not by itself reinstate it: a verified ABN is not a
     verification badge.
  4. Do not substitute a differently-worded badge. The fault is the claim, not the wording.
```

**Owner disposition recorded 20 August 2026.** Remove every slot and do not replace or substitute
another badge. No verifying body, licence number or credential is inferred.

**Applied to the media intake; page mutation staged but not run.** The badge is excluded from the
81-file public media set and retained in `source-inputs/media-retired/` for provenance. The
fail-closed post-import transformation removes all 14 slots; it has not run because nothing has
been imported. `camden-concreting-import.xml` is immutable and untouched; its SHA-256 is unchanged.

---

## Testimonial-labelled photograph investigation — no new register category

Attachments 46, 47, 48, 49, 51, 52 and 228 were traced through every Elementor placement on
20 August 2026. **Fabricated customer quotes found: 0.** None of the 110 placements carries a
customer name, quote, star rating, testimonial suburb attribution, review date or testimonial job
description. The only three actual testimonial widgets in the WXR are homepage placeholders with
empty image IDs; none uses the seven attachments.

Four target photographs occur once each inside the already-condemned D32 local-work modules. Their
only adjacent text is a `REAL_PHOTO_PENDING` marker, not a customer assertion. Those modules are
removed by the post-import transformation before the generic filename/alt remediation is verified.

Because the count is zero, no invented-testimonial false-fidelity category is created. If a real
customer quotation is later supplied, it still requires the review text, reviewer identity and
permission to publish; the GENERIC photos cannot be attached as evidence. Full placement evidence:
`reports/45-testimonial-text-investigation.md` and
`reports/45-testimonial-text-investigation.csv`.
