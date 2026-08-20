# Stage 44 — §4.22.4 pixel sighting: what it requires

Date: 19 August 2026 (Australia/Sydney).
**Phase B stops here.** Nothing is imported. Staging is not built. The sighting is owner work.

---

## 1. How many images

**83 images, one pass each.** Not 1,017 — that is the number of image-on-page *placements*, and you
do not need to look at the same photograph fourteen times. You are judging the **file**, and the
consequence of a bad file propagates to every page that uses it.

```text
  83   images to sight
   1   pass each
  ~2   minutes each, honestly — most are decided in ten seconds
```

The re-encoded, renamed files are in **`source-inputs/media/`** under their Camden names. The
as-received E&T originals are preserved in `source-inputs/media-original/` if you want to compare.

### Priority order, because the first 16 carry the actual risk

| Band | Count | Why |
|---|---:|---|
| **A — geographic claims** | **16** | Filename and alt text assert a specific NSW place. These are the 20-Victorian-images problem. **Sight these first.** |
| **B — testimonial and evidential** | 9 | Seven filenames assert testimonial/completed-job context; one is an unusable placeholder and one is an unsupported verification badge |
| **C — logo / brand** | 5 | 306, 307, 422, 469, 472 — retiring at import, but confirm nothing else in the set is an E&T mark |
| **D — decorative / generic** | 55 | Lowest risk; a wrong one is embarrassing, not a false claim |

Band A is the check that would have caught all 20 false-geographic images at source. If you only do
one band, do that one.

---

## 2. What you are confirming, per image

Four questions. Three are yes/no; the fourth is the one that matters.

```text
  1. IS IT A PHOTOGRAPH OF CONCRETE WORK?
       or is it a stock scene, a logo, a screenshot, an AI render, a placeholder?

  2. DOES IT SHOW WHAT THE FILENAME SAYS?
       "camden-town-centre-907.jpg" must show Camden town centre.
       "wianamatta-shale-clay-camden-1020.jpg" must show that soil.
       If the filename names a PLACE and you cannot confirm the place, that is a NO.

  3. DOES IT SHOW WHAT THE ALT TEXT SAYS?
       usually the same answer as 2, but alt text sometimes claims more

  4. COULD IT BE ANYWHERE?
       If the image shows a driveway with no identifying context, it is SAFE as a
       decorative image but must NOT sit under a filename or caption naming a place.
       This is the most common correct answer, and it is the useful one.
```

**You are not judging quality.** A dull photo of a real slab is fine. You are judging **whether the
image supports the claim its filename and alt text make.**

### The verdicts

```text
  OK        image supports its filename and alt text — no action
  GENERIC   image is fine but the NAME/ALT claims a place it does not show
            -> rename and rewrite alt, keep the image
  REPLACE   image is wrong, misleading, or not concrete work -> needs sourcing
  UNUSABLE  not a usable image at all (too small, corrupt, a logo in a photo slot)
```

### Band B — completed 20 August 2026

```text
  GENERIC    7   attachments 46, 47, 48, 49, 51, 52, 228
  UNUSABLE   2   attachments 280, 1067
```

The seven photographs have been renamed in the active intake and now carry subject-only alt-text
specifications in `build/45-media-remediation.csv`. They are decoration only and may never be used
as customer evidence or in a recent/local-work module. Attachments 49 and 52 are byte-identical;
both remain distinct attachment IDs for now.

The two unusable assets are excluded from the public media set and retained under
`source-inputs/media-retired/` for provenance. All 28 Elementor references are removed after the
immutable WXR import; no replacement slot and no substitute badge is permitted. The post-import
operation is fail-closed in `staging-authoritative/scripts/apply-band-b-remediation.php`.

The accompanying text investigation found **zero fabricated customer quotes**. Full evidence:
`reports/45-testimonial-text-investigation.md` and its one-row-per-placement CSV.

`GENERIC` will be the most common verdict on band A, and it is the cheapest fix — no sourcing cost,
just honest naming.

---

## 3. The fastest format

**A pre-filled CSV, one row per image, you fill two columns.**

I will generate `reports/44-sighting-worksheet.csv` on your word, pre-filled with:

```text
  #  band  new_filename  dimensions  pages_using  claims_place  current_alt_text  |  VERDICT  NOTE
```

sorted band A first, then B, C, D. You fill **VERDICT** and, only where it is not `OK`, a short
**NOTE**. Everything else is already there so you never have to look anything up.

**How to run it in practice:**

1. Open `source-inputs/media/` in Windows Explorer, **Large icons** view, sorted by name.
2. Open the CSV beside it.
3. Work down band A — 16 images — against the icons. Most are decided at thumbnail size; open the
   few that need it.
4. Then B (7), C (5), and D (55) if you have the appetite. **Band D can be deferred**; bands A, B
   and C are 28 images and cover every claim-bearing file.

That is **28 images for the risk-bearing pass**, and 83 for a complete one.

If you would rather not use a spreadsheet, the alternative is a contact sheet — I can render all 83
as a single labelled montage PNG, and you reply with just the filenames that are not `OK`. That is
faster to review and slower to act on, because the notes are less structured. Say which you prefer.

---

## 4. Two things already found, which seed the list

**`image-testemonials-camden-280.jpeg` — SETTLED `UNUSABLE`, 20 August 2026, owner-confirmed.**
62 × 62 at 624 bytes; the E&T original is 63 × 63. Not a failed encode, not a photograph, and it
cannot become one. It failed the media audit's `MIN_BYTES` floor while present. It is now outside
the active 81-file set, whose media audit passes 81/81 on the unchanged floor.

It is worse than the numbers suggest: the Elementor widget renders it at **width 69%, height 267px**
— roughly a **4× upscale of a 62-pixel source**, so it currently displays as a blurred smear.

**Disposition: remove the slot, do not replace. Sourcing cost zero.**

```text
  14 pages reference it
   6  WITHDRAWN — 2 intersection, 3 guide, 1 cost/comparison; enter no wave
   8  ACTIVE
        2 publish   /concrete-driveways-south-west-sydney/
                    /concrete-driveway-replacement-south-west-sydney/
        6 draft     concreters-bradbury, -cobbitty, -gilead,
                    -kemps-creek, -mount-annan, -tahmoor
```

**What the 8 active pages lose:** the image half of a two-column text-plus-image block. The text
column is untouched, so no word count changes and no page drops below any floor. The container is
left with one populated column — the layout collapses to full-width text rather than breaking. On
the 2 publish pages this removes a visible element from a live-eligible page, which is a
**presentation** change, not an evidence change: a 62-pixel smear evidences nothing, so nothing
evidential is lost.

Recorded in `build/21-spec-ledger.json` under `sighting_verdicts`, and pre-filled in the worksheet.

**The five brand files** — 306, 307, 422, 469, 472 — resolve to E&T marks until the Structure Co
wordmark replaces them at import. That is runbook work, not Phase B, and they are in band C only so
you can confirm nothing *else* in the set is an inherited mark.

---

## 5. Why this cannot be automated

Every audit in this build so far has read filenames, titles and alt text. Metadata was clean on all
83 after the strip — **and that says nothing about what the photographs depict**. An honestly-named
file can still show a Melbourne street. The only instrument that catches it is a person looking at
the image, which is why §4.22.4 exists and why it has never been performed.

---

## 6. State at the stop

```text
  media intake        83 of 83 present, renamed, re-encoded, EXIF clean
  media audit         82 of 83 OK — 1 genuine failure (the 62x62 image)
  Astra audit         PASS
  preflight           NO-GO, 5 gates failing: 3, 4, 7, 12, 13
  gates 10 and 14     PASS
  imported            NOTHING
  staging             NOT built
```

**Phase B ends at the sighting.** Steps 5, 6 and 7 of RUN-BLOCK-02 Phase B — build
`staging-authoritative/`, import in order, verify attachments — are not started and are not next
until the sighting is done.
