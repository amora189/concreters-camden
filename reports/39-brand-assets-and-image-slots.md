# Stage 39 — brand asset inventory, and the image slots left by removing 306/307

Date: 19 August 2026 (Australia/Sydney).
Authority: `DECISION-08-trading-name-brand-nap.md` §D36, plus the owner's five decisions of
19 August 2026.

**Nothing was implemented.** No asset was uploaded, converted, resized or placed. No page was edited.
The seven immutable hashes are re-verified in §6 and all match.

---

## 1. Brand asset inventory — verified on disk

`source-inputs/brand/`, five files, all present.

| File | Bytes | viewBox | w × h | paths | SHA-256 (first 16) |
|---|---:|---|---|---:|---|
| `structure-co-horizontal.svg` | 8,879 | `0 0 773 260` | 773 × 260 | 27 | `6E94B0700046E5A6` |
| `structure-co-horizontal-mono.svg` | 8,879 | `0 0 773 260` | 773 × 260 | 27 | `CFC176F3A9856FEA` |
| `structure-co-horizontal-reversed.svg` | 8,926 | `0 0 773 260` | 773 × 260 | 27 | `DFED6D255008AD56` |
| `structure-co-stacked.svg` | 8,607 | `0 0 527 308` | 527 × 308 | 27 | `F55B37ABF35EF9C7` |
| `structure-co-icon.svg` | 1,761 | `0 0 512 512` | 512 × 512 | 2 | `08E47165E9759327` |

### Claims tested, not accepted

| Claim | Result |
|---|---|
| Text converted to outlines | **HOLDS.** Zero `<text>`, zero `<tspan>` across all five. |
| No font dependency | **HOLDS.** Zero `font-family` references across all five. |
| Icon is 512 square | **HOLDS.** `viewBox="0 0 512 512"`, width and height both 512. |
| Navy `#1C244B` | **HOLDS** in horizontal, reversed, stacked, icon. |
| Grey `#7C8494` | **HOLDS** in horizontal and stacked. |
| Single-colour mono | **HOLDS.** `structure-co-horizontal-mono.svg` contains `#000000` only. |
| Self-contained | **HOLDS.** No external `href`, no embedded raster, no `<image>`, no `<script>`. |

### Palette, as confirmed

```text
  #1C244B   navy    primary brand colour, taken from the Elementor kit
  #7C8494   grey    secondary brand colour
  #AEB6C6   tint    REVERSED-CONTEXT TINT ONLY — #7C8494 lifted for legibility on navy.
                    Confirmed by the owner 19 August 2026. It is NOT a third brand
                    colour and must not be used as one: it appears only in
                    structure-co-horizontal-reversed.svg and only for that purpose.
```

### Two deviations from the brief, recorded

1. **Two filenames differ from those named.** The brief listed `-reversed.svg` and `-mono.svg`; on
   disk they are `structure-co-horizontal-reversed.svg` and `structure-co-horizontal-mono.svg`. The
   runbook now references the on-disk names. No action needed unless the names were meant to be
   literal.
2. ~~A third colour.~~ **RESOLVED 19 August 2026.** `#AEB6C6` is confirmed as `#7C8494` lifted
   for legibility on navy. Recorded above as a reversed-context tint, not a brand colour.

`structure-co-horizontal.svg` and `structure-co-horizontal-mono.svg` are the same byte length (8,879)
with different hashes — expected for identical geometry with a different fill.

### Favicon PNGs — supplied and verified

~~The site icon needs a PNG, and no PNG render is on disk.~~ **RESOLVED 19 August 2026.** Five PNG
renders supplied, at exactly the sizes WordPress generates for a site icon.

| File | Dimensions | Bytes | SHA-256 (first 12) |
|---|---|---:|---|
| `structure-co-icon-512.png` | 512 × 512 | 19,460 | `8243C074EF9A` |
| `structure-co-icon-270.png` | 270 × 270 | 22,866 | `832E028414DA` |
| `structure-co-icon-192.png` | 192 × 192 | 14,891 | `8F3665CEC3D1` |
| `structure-co-icon-180.png` | 180 × 180 | 15,391 | `FA138FCF6C9E` |
| `structure-co-favicon-32.png` | 32 × 32 | 2,902 | `1CA4E9C85A23` |

Verified, not assumed:

- **Dimensions read from the PNG headers**, not from the filenames. All five match their stated size.
- **All five carry real artwork.** Mean luminance is 0.4498–0.4502 across every size — the same
  image rendered at five scales, not a blank or a mismatch. Fully opaque (`alpha_mean = 1`), correct
  for a navy square icon.
- **Metadata clean.** Zero GPS, zero Artist/Copyright/Owner/Serial, zero Make/Model, zero
  `DateTimeOriginal`, zero `Software`. They carry only PNG `cHRM`/`bKGD` chunks and a generation
  timestamp (`2026-08-18T22:22:32Z` = 19 Aug 08:22 AEST). Nothing sensitive, nothing identifying.
- **SVG upload stays disabled** — agreed, a stored-XSS vector is not worth one favicon.

Minor: the 32px render is named `structure-co-favicon-32.png` while the other four are
`structure-co-icon-NNN.png`. Cosmetic only; the runbook uses the on-disk names.

Note the 270 px file (22,866 B) is larger than the 512 px file (19,460 B). Expected — the 512 has
more flat area to compress, and unique-colour counts confirm it (1,126 at 512 vs 2,276 at 270).

**The site icon is therefore unblocked independently of the Astra export**, since
`Settings → General → Site Icon` is WordPress core rather than an Astra theme mod. It waits only on
the import itself. Header, footer, sticky and mobile slots still wait on the Customizer export.

`D36` is flipped in the ledger from `ON_DISK: ABSENT` to present-and-verified.

---

## 2. The ten image slots — and what they actually need

Removing attachments **306** and **307** under D36 empties **10 image slots across 10 pages**.
Confirmed against `camden-concreting-import.xml` and cross-checked to
`reports/33-image-replacement-spec.csv`.

| # | Page | Attachment | Architecture state |
|---:|---|---|---|
| 1 | `/about/` | 306 | **active** |
| 2 | `/contact/` | 306 | **active** |
| 3 | `/quote/` | 306 | **active** |
| 4 | `/gallery/` | 306 | **active** |
| 5 | `/concrete-patios-south-west-sydney/` | 306 | **active** |
| 6 | `/concrete-paths-south-west-sydney/` | 307 | **active** |
| 7 | `/concrete-patios-gledswood-hills/` | 306 | WITHDRAWN (D16) |
| 8 | `/concrete-patios-edmondson-park/` | 306 | WITHDRAWN (D16) |
| 9 | `/concrete-patios-elderslie/` | 306 | WITHDRAWN (D16) |
| 10 | `/concrete-paths-edmondson-park/` | 307 | WITHDRAWN (D16) |

**Ten slots, but only six sit on pages in the architecture.** Four are on withdrawn intersection
pages that are excluded at import and enter no wave.

### Direction given, 19 August 2026 — the slots are resolved

```text
  306, 307, 422   RETIRED. The Structure Co wordmark replaces them.
  in-page brand placement     structure-co-horizontal.svg
  on dark backgrounds         structure-co-horizontal-reversed.svg
  6 slots on live pages       take the wordmark
  4 slots on withdrawn pages  need nothing — those pages enter no wave
  sourcing cost               ZERO, as expected
```

**The §4.22.4 sighting still applies.** No slot is called correct until it has been looked at: the
wordmark being the right *asset* does not establish that it is the right size, position or context in
each of the six placements, and that check has never been performed on any image in this build.

### Why these were brand slots, not photography slots

Both attachments are recorded in the existing spec with `role: logo/brand asset` and disposition
`HOLD — LOGO, NOT PHOTOGRAPHY`. 306 is the E&T favicon symbol at 512×512; 307 is a 512×374 crop of
the same symbol. Both render as a plain image widget, not inside a service tile.

The spec's own note said the hold could only be lifted by owner direction: *"commission a logo,
supply an existing one, or confirm the source business's symbol may be used."* **That direction has
now arrived** — the Structure Co brand assets in §1.

The six live slots take `structure-co-horizontal.svg`, or
`structure-co-horizontal-reversed.svg` where the background is dark. **Not sourced imagery.** The
sourcing cost is zero and this is a placement task inside the brand rollout, not a stock-image job.

---

## 3. Registering the ten as the Phase F target — and what that must not drop

Recorded as instructed. One thing has to be said plainly first, because the two things being swapped
are not the same problem.

### The "16-slot spec" is the false-geographic-claim remediation

`reports/33-image-replacement-spec.csv` holds 20 rows: **16 `REPLACE`**, 3 `HOLD — LOGO` (306, 307,
422), 1 `REMOVE_WITH_MODULE`. The 16 `REPLACE` rows are the **Victorian photographs renamed to
specific NSW places**.

```text
  16 REPLACE rows, every one carrying a geographic_claim:
    TARNEIT-SOIL.jpg          -> wianamatta-shale-clay-camden-1020.jpg
    werribee-town.jpg         -> camden-town-centre-907.jpg
    oran-park1/2/3            -> asserts Oran Park, NSW
    ... 11 more, each asserting Camden, Oran Park, Mount Annan, Leppington,
        Gregory Hills or South West Sydney

  distinct pages touched            76
    of which WITHDRAWN              38
    of which STILL ACTIVE           38
```

**These 16 rows and the 10 logo slots are different problems.** The brand assets fix the logo slots
and do nothing for the 16. Retiring the 16-row spec in favour of the 10 would drop the remediation
for **38 active pages that currently make false geographic claims** — the single most concrete
truth-in-content defect in the build.

### What is actually stale about it

Not the 16 rows. **Its page coverage**: 38 of the 76 pages it targets have been withdrawn, so the
slot arithmetic is wrong. That is exactly what `DECISION-07` D34.2 already requires — regenerate the
spec against the post-D32 architecture before Phase F spends a credit.

### Recorded position — TWO CONCURRENT TARGETS, confirmed 19 August 2026

The owner confirmed these are separate, additional jobs. **Neither replaces the other.**

```text
  PHASE F, TARGET A — brand placement (RESOLVED, zero sourcing)
    ten slots from retiring 306/307/422
      on active pages                6    take structure-co-horizontal.svg,
                                          or -reversed.svg on dark backgrounds
      on withdrawn pages             4    need nothing
    sourcing cost                    ZERO
    outstanding                      §4.22.4 sighting before any slot is called correct

  PHASE F, TARGET B — false geographic claims (STANDS, unchanged in substance)
    16 REPLACE rows, Victorian photographs renamed to NSW places
      distinct pages                76
      still active                  38    <- the remediation target
      withdrawn                     38
    what is stale                    the PAGE ARITHMETIC only, per D34.2
    action                           regenerate the spec against the 77-page
                                     architecture before any credit is spent
    sourcing cost                    real — 16 replacement images
```

The earlier concern is resolved: the owner confirms the two were conflated and that the 16-row
photograph spec **is not retired**. Only its page counts are stale.

---

## 4. The five decisions, as applied

| # | Decision | Applied | Where |
|---|---|---|---|
| 1 | Attachment filenames keep `corex-` | Recorded as deliberate acceptance | runbook §5a, ledger |
| 2 | Update `lib/` generator constants | **39 replacements across 5 modules** | `lib/*.py` |
| 3 | Retarget `build/global-replace.json` | 22 → 25 rules | `build/global-replace.json` |
| 4 | Email attested | `verified: true`, `sighted_date: 2026-08-19` | `data/verified-facts.yml` |
| 5 | Remove the tagline | Runbook says remove, verify zero `Camden based` | runbook §5b |

### Decision 2 detail

```text
  lib/site_builder.py        27      lib/stage9.py               6
  lib/stage8.py               3      lib/stage3_gate.py          2
  lib/stage18_readiness.py    1      TOTAL                      39
```

All five modules compile. Zero `CoreX` in any case remains in `lib/`. **This changes no built
artifact** — it changes what a regeneration would emit. Note that `Structure Co` is 7 characters
longer than `CoreX`, and `fit_meta_title()` truncates: regenerated meta titles will differ in length
and some will truncate differently. Not a defect, but a regeneration will not be a clean diff.

### Decision 3 detail

Brand rules inserted longest-first, which is required — a shorter `find` running first consumes the
prefix of a longer one:

```text
   1  E&T Co Concreters Melbourne   -> Structure Co Concreters Camden
   2  E&T Co Concreters Camden      -> Structure Co Concreters Camden
   3  E&T Co                        -> Structure Co
   4  CoreX Concreters Camden       -> Structure Co Concreters Camden
   5  CoreX                         -> Structure Co
```

The `[[BRAND_NAME]]` placeholder indirection is retired for these rules: the name is resolved, so the
rules now name it directly.

> **Pre-existing defect found in this file, NOT fixed.** Three ordering faults predate this session
> and are unrelated to the brand rules:
> ```text
>   "Wyndham"  (index 10) precedes "Wyndham Vale"   (index 17)
>   "Werribee" (index 11) precedes "Werribee South" (index 16)
>   "Werribee" (index 11) precedes "Werribee River" (index 20)
> ```
> Run in order, `Werribee` is consumed first, so `Werribee South` never matches and would yield
> *"mapped Camden/South West Sydney suburb per page South"*. Same for `Werribee River` and
> `Wyndham Vale`. **Not corrected** — reordering a replacement contract changes build behaviour and
> is outside the five decisions. Flagged for an explicit decision.

### Decision 4 detail

`info@concreterscamden.com.au` is the **first field in `verified-facts.yml` to reach an attested
state**: 1 of 20 `verified: true`.

The attestation's scope is recorded in the file: the mailbox is live and monitored. It attests
nothing about a legal entity. It may now be used as a contact address and form recipient; it may not
be presented as evidence of a verified business.

**Phase C remains BLOCKED.** Email is not among the seven required identity fields, all of which are
still unverified: `legal_name`, `abn`, `nsw_fair_trading_licence`, `insurance_public_liability`,
`street_address`, `is_staffed`, `phone`. Address stays `verified: false`; `is_staffed` stays
`unknown`; **no `LocalBusiness`, no `Organization`, D2 ladder outcome 3 unchanged.**

---

## 5. Two findings registered

Both were reported in the previous gate and are now recorded in `build/21-spec-ledger.json` as
corrections rather than observations.

**466 against a recorded 345.** The ledger's `site_mark.trading_name_conflict` and D30 both quoted
345 CoreX occurrences in the main WXR. The true figure is **466**, recomputed with attribution
asserted complete. 345 is not reproducible from any corpus in the repo. Recorded with
`corrected_from: 345` so the discrepancy stays visible rather than being quietly overwritten.

**306 and 307 are live, not orphaned.** D27 recorded 306, 307 and 422 as unreferenced and directed
that they be left unreferenced. **422 is genuinely orphaned; 306 and 307 are not** — they are on 10
pages, 6 of them in the architecture and 5 of those at `publish` status. Removing them is not a
no-op, and the ten slots in §2 are the consequence.

All three are now **retired** by the owner's direction of 19 August 2026, replaced by the Structure
Co wordmark. They remain in the immutable WXR and are not deleted from it.

---

## 6. Immutable hash table

```text
  camden-concreting-import.xml                          MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   MATCH
  build/stage9-page-manifest.json                       MATCH
  build/stage8-image-map.json                           MATCH
  reports/08-image-rename-map.csv                       MATCH
  CODEX-BUILD-2.1.md                                    MATCH
  archive/governing/CODEX-BUILD-2.md                    MATCH

  7 of 7 MATCH.
```

---

## 7. State

Phase B remains **BLOCKED at step 2** on the Astra Customizer export. Architecture 77, index-ready 0,
launch gate NO-GO — all unchanged. One field is now attested, out of the twenty-plus that gate Phase C.

**All five open questions from the first issue of this report are now answered:**

```text
  1  #AEB6C6 intended?                     YES — reversed-context tint, recorded in §1
  2  who produces the favicon PNG?         SUPPLIED — five renders verified in §1
  3  do the six slots take the wordmark?   YES — horizontal, reversed on dark (§2)
  4  is the 16-row photo spec retired?     NO — it stands; two concurrent targets (§3)
  5  fix the global-replace ordering?      DONE — reports/40-global-replace-ordering-fix.md
```

**What remains open here:** the §4.22.4 sighting of the six live brand placements, which is part of
the wider sighting that has never been performed on any image in this build.
