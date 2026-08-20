# Stage 33 §1.4 — the soil image and its "module"

Date: 18 August 2026 (Australia/Sydney).
Attachment 1020, `TARNEIT-SOIL.jpg` → `wianamatta-shale-clay-camden-1020.jpg`.

---

## THE PREMISE DOES NOT HOLD — there is no ground-conditions module to remove

The instruction directs that the soil image be "removed along with its module". I could not carry that
out as written, because **on 14 of its 15 pages the image is not in a ground-conditions module at all.**

It is a **generic decorative tile**, rotating through the service grid alongside the other 19 images.

```text
  WHERE ATTACHMENT 1020 ACTUALLY SITS

  PAGE                                        CLASS        WIDGET       TILE TITLE
  /concreters-camden-park/                    suburb       image-box    " Exposed Aggregate "
  /concreters-currans-hill/                   suburb       image-box    " Patios & Alfresco in Currans Hill "
  /concreters-currans-hill/                   suburb       image-box    " Coloured & Decorative in Currans Hill "
  /concreters-glen-alpine/                    suburb       image-box    " Concrete Driveways "
  /concreters-wattle-grove/                   suburb       image-box    " Concrete Slabs "
  /concreters-leppington/                     suburb       image-box    " Concrete Slabs "
  /concreters-narellan/                       suburb       image        (plain, no tile)
  /concrete-slabs-leppington/                 intersection image        (plain, no tile)
  /concrete-driveways-catherine-field/        intersection image        (plain, no tile)
  /concrete-driveways-spring-farm/            intersection image        (plain, in a grid)
  /commercial-concreting-south-west-sydney/   service      image        (plain, no tile)
  /campbelltown-council-driveway-crossing/    guide        image        (in a guide-link grid)
  /curing-concrete-in-summer-vs-winter/       guide        image        (in a guide-link grid)
  /reactive-clay-slabs-as2870/                guide        image        (in a guide-link grid)
  /why-concrete-cracks/                       guide        image        (in a guide-link grid)
  /guides/                                    guide_hub    image        (in a guide-link grid)

  class distribution   suburb 6, guide 4, intersection 3, service 1, guide_hub 1
  sections with a ground-conditions heading   1 of 15  ("The verified Spring Farm condition")
  sections with NO heading at all            12 of 15
```

A photograph of soil is currently serving as the thumbnail for **"Exposed Aggregate"**, **"Patios &
Alfresco"** and **"Coloured & Decorative"**. Removing "its module" would delete service tiles and
guide-link grids, not a ground-conditions section.

**Removing the image is straightforward. Removing "its module" is not a coherent instruction against this
artifact, and I have not guessed at one.**

---

## What the module removal WOULD destroy, if performed as briefed

If the containing section were removed on each of the 15 pages:

```text
  PAGE                                      SECTION WORDS   PAGE WORDS   WOULD LOSE
  /concreters-camden-park/                              0           29   a service tile
  /concreters-glen-alpine/                              0           30   a service tile
  /concreters-wattle-grove/                             0           30   a service tile
  /concreters-currans-hill/                             0          935   two service tiles
  /concreters-leppington/                               0        1,083   a service tile
  /concreters-narellan/                                85        1,017   85 words
  /concrete-driveways-catherine-field/                 87        2,078   87 words
  /concrete-driveways-spring-farm/                     91        2,071   91 words
  /concrete-slabs-leppington/                         101        2,046   101 words
  /commercial-concreting-south-west-sydney/           116        2,069   116 words
  /campbelltown-council-driveway-crossing/            116          832   116 words
  /curing-concrete-in-summer-vs-winter/               116          784   116 words
  /reactive-clay-slabs-as2870/                        116          784   116 words
  /why-concrete-cracks/                                85          574   85 words
  /guides/                                            102          586   102 words
```

Three suburb pages (`camden-park`, `glen-alpine`, `wattle-grove`) have **29–30 total body words**. They
are empty shells; nothing meaningful is lost or preserved either way.

---

## The Wianamatta text — SEPARATE from the photograph, and it survives

The instruction is right that the copy may survive. It does, and it is **not co-located with the image**.

```text
  'Wianamatta' occurrences in the artifact   47
  'shale'                                    76
  'reactive clay'                            69
  'AS 2870' / 'AS2870'                       28 / 6
```

The copy lives in `text-editor` widgets on suburb pages. Verbatim, no elision:

```text
  HEADING
    "Wianamatta clay and engineered fill"

  BODY (Oran Park)
    "Oran Park sits on Wianamatta Group shale, and the residual soil above it is reactive
     clay — it swells when it's wet and shrinks when it dries, moving through the seasons
     underneath whatever you pour on it."

  BODY (Leppington)
    "Upper South Creek is the controlling water reference for Leppington, while reactive
     Wianamatta clay remains the recorded ground material beneath affected lots."

  BODY (Leppington, project record)
    "For Leppington, the verified project record says: Reactive Wianamatta clay with Upper
     South Creek drainage running through parts of the suburb."

  BODY (growth corridor, appears on multiple pages)
    "Across the growth corridor, Wianamatta shale-derived reactive clay and engineered fill
     are recurring site inputs."
```

### Which is true and which is false

```text
  THE TEXT     Geologically consistent with the area. The Camden / Oran Park district does
               sit on Wianamatta Group shale with reactive residual clay above it. Nothing
               in the wording asserts the operator measured it.
               DISPOSITION: retain, subject to the owner confirming a source. Do NOT delete
               to be safe — deleting true, sourced local content is its own kind of damage.

  THE PHOTO    A Tarneit, VIC soil photograph. Tarneit sits on the Victorian basalt plains.
               Basalt-derived soil and Wianamatta shale-derived clay are different geologies
               and do not look alike.
               DISPOSITION: REMOVE. It cannot be made honest by renaming.

  ONE EXCEPTION, FLAGGED NOT RESOLVED
               "For Leppington, the verified project record says: ..." is one of the six
               false-fidelity sentences already registered in reports/23-false-fidelity.md.
               The geology may be true; the claim that a VERIFIED PROJECT RECORD says it is
               not established. That sentence needs rewriting regardless of the image.
```

---

## Uniqueness and word-count impact

```text
  Removing the IMAGE ONLY (recommended):
    body words removed          0
    uniqueness impact           none — images are not counted in body text
    word-count floor impact     none
    pages dropping below any threshold   0

  Removing the CONTAINING SECTION (as briefed):
    body words removed          1,015 across 15 pages
    largest single-page loss    116 words from a 574-word page (/why-concrete-cracks/),
                                a 20.2% reduction
    suburb pages affected       6, of which 3 have under 31 total words already
    uniqueness impact           the removed text is template filler (see below), so removing
                                it would RAISE measured uniqueness, not lower it
    pages dropping below a threshold     0 — but see the caveat
```

**Caveat on that last line.** No suburb page currently meets the 0.60 threshold anyway (only Oran Park at
0.865 and Leppington at 0.637 do, and neither is in this set), and the "unique body words" definition is
itself unresolved (Gate 25 §0). "Nothing drops below a threshold" is true but weak: most of these pages
are already below it.

---

## Related finding — the removable text is largely template filler

The section bodies proposed for removal are not prose. Sample, verbatim from
`/campbelltown-council-driveway-crossing/`:

```text
  "campbelltown-council-driveway-guide logs site identity; campbelltown-council-driveway-guide
   keeps the basis explicit. campbelltown-council-driveway-guide dates the address;
   campbelltown-council-driveway-guide holds the citation. campbelltown-council-driveway-guide
   tracks lot and; campbelltown-council-driveway-guide keeps provenance visible."
```

This is machine-generated word salad repeating a slug token at the head of every clause. It is a much
larger problem than the image, and it is **not confined to these 15 sections** — see
`reports/33-image-replacement-spec.md` §5.

---

## Recommendation

```text
  1  REMOVE attachment 1020 from all 15 pages. Do not replace it.
  2  DO NOT remove the containing sections. They are service tiles and guide-link grids,
     not a ground-conditions module, and removing them would delete navigation.
  3  RETAIN the Wianamatta text, subject to the owner confirming a geological source.
  4  REWRITE the "verified project record" sentence on Leppington regardless.
  5  Treat the tile slots left empty by removal as a layout question for the post-import
     runbook: either the tile loses its image or it takes one of the 16 replacements.

  All of the above are POST-IMPORT edits. camden-concreting-import.xml is immutable.
```
