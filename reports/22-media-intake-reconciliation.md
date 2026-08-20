# Stage 22 — media intake reconciliation

Date: 19 August 2026 (Australia/Sydney).
Scope: **audit only.** Nothing was re-encoded, renamed, moved, imported or deployed. The immutable
files are unchanged and re-verified below.

Companion artifacts:
`reports/22-media-intake-reconciliation.csv` (83 rows, one per required original),
`reports/22-media-intake-reconciliation.json`,
`reports/22-media-audit-result.md` and `reports/22-media-missing-manifest.csv` (raw fail-closed output).

---

## 1. Precondition gate — `scripts/37-preconditions.py`

Immutable hashes: **7 of 7 MATCH**. No mismatch. Re-verified again after this session's only write
(an append to `reports/23-false-fidelity.md`), still matching.

```text
  PHASE  NAME                    STATUS    EVIDENCE
  A      attest the figures      BLOCKED   91 fields verified:false, 0 true; populated flag false
  B      media and staging       BLOCKED   media 189/83; astra 0 file(s); driver present;
                                           ImageMagick NOT INSTALLED
  C      identity and schema     BLOCKED   0 verified:true / 20 false
  D      Liverpool               BLOCKED   data/council-specs.yml absent
  E      service page rebuild    BLOCKED   requires Phase A
  F      images                  BLOCKED   explicitly last; requires A–E
  G      release                 BLOCKED   requires the preceding phases and a GO from preflight

  RUNNABLE PHASES: NONE.  Exit 1.
```

Phase B remains **BLOCKED**, correctly, on the Astra Customizer export — `source-inputs/astra/`
holds 0 files. Steps 3–7 of Phase B do not start.

### 1a. A defect in the gate itself — the ImageMagick probe is on the wrong host

`phase_b()` probes `command -v magick` through `bash` on **Windows**. The re-encode driver and the
EXIF assertion run in **WSL**. The gate is therefore reading a host that will never carry the tool
and would report `NOT INSTALLED` permanently, including after Phase B's real dependency is
satisfied.

Verified in WSL, directly:

```text
  /usr/bin/magick     ImageMagick 7.1.2-18 Q16 x86_64
  /usr/bin/convert
  /usr/bin/exiftool   13.50
```

**The assertion was not relaxed to make this pass, and the script was not edited.** The gate output
above is reproduced as the gate actually emitted it. Recorded here as a defect for correction under
its own approval: the probe must target the host that runs the driver. Note that the verdict is
unaffected either way — Phase B is blocked on the Astra export regardless.

---

## 2. `scripts/22-media-audit.py` — raw result

```text
  expected=83  present=189  ok=0  missing=83  extras=189  failures=272
  VERDICT: FAIL — media intake incomplete
```

**This FAIL is a name-space artifact, not an absence.** The audit compares the directory against the
`new_filename` column of `reports/08-image-rename-map.csv` — the post-rename Camden names
(`concrete-project-detail-camden-17.jpg`). The delivered set is the **E&T Melbourne uploads
directory**, which carries the `old_filename` names (`22d688903186d76070a16bfae68d96e22e496089.jpg`).
The rename is a Phase B step that has not run and must not run yet.

The audit is not wrong to fail; it is asserting a post-rename condition against a pre-rename
directory. Section 3 is the reconciliation it cannot perform. **`22-media-audit.py` must be re-run
and must pass on its own terms after the rename step, and the number below does not substitute for
that pass.**

---

## 3. How many of the 83 required binaries are present

```text
  required originals                                     83
  present, exact filename match                          77
  present under a mismatched filename (see §4)            6
  ---------------------------------------------------------
  content-complete                                       83
  genuinely absent                                        0
  present only as a dimensioned thumbnail variant         0  (see §5 — with a caveat)
```

**All 83 required binaries are present in content.** Six of them are not present under the filename
the build requires. Until those six are resolved, the intake is **not** clearable and Phase B step 1
does not pass.

Delivered directory: **190 entries** (the precondition gate counts 189 because it excludes
`README.md`).

```text
  matched to a required original                         83
  duplicate " - Copy" of a delivered file                90
  non-image files                                        13
  surplus images not required by the build               10
  ---------------------------------------------------------
  total                                                 190
```

---

## 4. Filename mismatches against the required set

Six required originals are on disk only under a ` (1)` suffix — a **filesystem collision-rename
artifact** from extracting three overlapping cPanel zips into one directory. In every one of the six
cases the plain-named file is absent and only the ` (1)` form was delivered.

| id | required `old_filename` | on disk as | maps to `new_filename` |
|---:|---|---|---|
| 226 | `concretejob2werribee.jpg` | `concretejob2werribee (1).jpg` | `concretejob2camden-226.jpg` |
| 227 | `backyard-patio-concreter.jpg` | `backyard-patio-concreter (1).jpg` | `backyard-patio-concreter-camden-227.jpg` |
| 228 | `cocnretejob1weribee.jpg` | `cocnretejob1weribee (1).jpg` | `concretejob1camden-228.jpg` |
| 468 | `e-t-co-logo-transparent.png` | `e-t-co-logo-transparent (1).png` | `corex-concreters-camden-logo-468.png` |
| 471 | `e-t-co-logo-512.png` | `e-t-co-logo-512 (1).png` | `corex-concreters-camden-logo-471.png` |
| 609 | `exposed-aggregate-adelaide.jpg` | `exposed-aggregate-adelaide (1).jpg` | `exposed-aggregate-south-west-sydney-609.jpg` |

### 4a. Evidence that these are the correct binaries

The authoritative filename comes from `_wp_attached_file` in the immutable source WXR, which for all
six is the plain name. Each candidate was checked against the `_wp_attachment_metadata` the source
site recorded for that attachment:

```text
  id   delivered file                       actual dims   WXR declared   bytes vs declared
  226  concretejob2werribee (1).jpg         640x480       640x480        31714 = 31714
  227  backyard-patio-concreter (1).jpg     800x600       800x600        99651 = 99651
  228  cocnretejob1weribee (1).jpg          638x480       638x480        33709 = 33709
  468  e-t-co-logo-transparent (1).png      512x512       512x512        302716 = 302716
  471  e-t-co-logo-512 (1).png              512x512       512x512        302716 = 302716
  609  exposed-aggregate-adelaide (1).jpg   1448x1086     1448x1086      692544 = 692544
```

Dimensions and byte length match the source site's own record exactly in all six cases.

Attachment **227** carries independent corroboration: its EXIF `UserComment` is
`xr:d:DAEs8AkRkpw:853,j:1786070001474348981,t:23060804`, and that same string is the `<title>` of
attachment 227 in the source WXR. The binary on disk and the WXR record are demonstrably the same
asset.

**468 and 471 are byte-identical to each other** (SHA-256 `AEB1D311E19485EF…`). This is not a
delivery error. The source WXR declares both attachments at 512×512 and 302,716 bytes — the source
site itself held one image under two attachment IDs and two filenames. Both `new_filename` targets
resolve to the same binary, and the rename step must write it out twice rather than treating one as
a duplicate to skip.

**What this evidence does not establish.** WXR carries no checksum, so dimension-plus-byte-length
agreement is strong corroboration, not cryptographic proof of identity. It is sufficient to say the
binaries are present and to name the rename that is required. It is not a substitute for the §4.22.4
pixel-level sighting, which has still never been performed on any image in this build.

**Not renamed.** No file was touched. Renaming six delivered inputs is a mutation of owner-supplied
evidence and belongs to the Phase B step that owns it, on approval.

---

## 5. Required originals present only as a dimensioned thumbnail variant

**Within `source-inputs/media/`: none.** No required original is represented solely by a `-WxH`
variant there; the thumbnail sweep to WSL did its job and no dimensioned file remains in the intake
directory at all.

**The caveat, which is the real answer to the question.** The WSL thumbnail store
(`~/camden-images/source-inputs/media-thumbnails/`, 462 files) was checked for the six mismatched
originals in §4. All six appear there **only** as dimensioned variants:

```text
  concretejob2werribee-150x150.jpg, -300x225.jpg
  backyard-patio-concreter-150x150.jpg, -300x225.jpg, -768x576.jpg
  cocnretejob1weribee-150x150.jpg, -300x226.jpg
  e-t-co-logo-transparent-150x150.png  (+ cropped- variants)
  cropped-e-t-co-logo-512-150x150.png, -180x180.png, -192x192.png, -270x270.png
  exposed-aggregate-adelaide-150x150.jpg, -300x225.jpg, -768x576.jpg, -1024x768.jpg
```

So the plain-named originals were not swept into the thumbnail store by mistake — they were never
delivered under that name at all, and the ` (1)` files in §4 are the only copies of those six
binaries in the intake. **If the ` (1)` files are discarded as duplicates, six required originals are
lost and only thumbnails remain.** They must not be cleaned up as extras.

No required original is thumbnail-only in the sense of being unrecoverable at full size. Zero of 83
would need to be reconstructed from a downscaled variant.

---

## 6. Unexpected extras

### 6a. Surplus images (10)

```text
  Screenshot 2026-08-18 061842.png              135,722 bytes
  Screenshot 2026-08-18 061943.png               55,505 bytes
  verified-badge.avif                            44,358 bytes   see §7
  verified-badge-e1784545609908.avif             46,237 bytes   see §7
  backyard-patio-concreter (1).jpg                              counted in §4, not surplus
  cocnretejob1weribee (1).jpg                                   counted in §4, not surplus
  concretejob2werribee (1).jpg                                  counted in §4, not surplus
  e-t-co-logo-512 (1).png                                       counted in §4, not surplus
  e-t-co-logo-transparent (1).png                               counted in §4, not surplus
  exposed-aggregate-adelaide (1).jpg                            counted in §4, not surplus
```

The six ` (1)` files are classified surplus by filename and required by content. Genuinely surplus:
**4 files** — two screenshots and two unused `verified-badge` variants.

### 6b. Non-image files delivered into the media directory (13)

```text
  ApexFrame_Case_Study.pdf, -1.pdf, -2.pdf, -3.pdf
  B2B_Outreach_Framework.pdf
  Objection_Handling_Playbook.pdf, -1.pdf
  Shaun_Gunar_Resume.pdf
  Shaun_Gunar_Resume_Upwork.pdf
  eamptcoconcretersmelbourne.WordPress.2026-08-18.xml
  CLAUDE.md
  CODEX-BUILD-2.md
  README.md
```

Two of these need a decision rather than a sweep:

- **`Shaun_Gunar_Resume.pdf` / `Shaun_Gunar_Resume_Upwork.pdf`** are a named individual's personal
  documents sitting in a directory whose entire purpose is to be uploaded to a public web server.
  They must not enter the import under any circumstance. Flagging, not deleting — they are
  owner-supplied files and deletion is the owner's call.
- **`eamptcoconcretersmelbourne.WordPress.2026-08-18.xml`** is a **fourth WXR export**, dated four
  days after the immutable source WXR (2026-08-14) that the entire build is reconciled against. It
  is not in any hash table and no artifact cites it. It is **not** being read, compared or merged.
  Its existence is reported; whether it supersedes anything is an owner question, and adopting it
  would invalidate the pause baseline.

### 6c. `- Copy` duplicates (90)

Every one of the 90 is a byte-level duplicate of a file already delivered under its plain name.
Harmless to the audit, and excluded from every count above. They must be excluded from the import
set, not resolved by picking whichever sorts first.

---

## 7. `verified-badge` — registered as a false-fidelity claim

Added to `reports/23-false-fidelity.md` as **NT-1**, in a new section for non-textual claims. The
existing prose count of 6 is unchanged; a badge is not a sentence and the D11.3 scan could not see
it. Full disposition is in that register. Summary:

- The build requires exactly one of the three badge files: **`verified-badge-e1784545689665.avif`**,
  attachment **1067**, renamed to `verified-badge-e1784545689665-camden-1067.avif`. Present and
  matched. `verified-badge.avif` and `verified-badge-e1784545609908.avif` are surplus.
- It was in **no** register — not `23-false-fidelity.md`, not `23-evidence-register.csv`, not
  `23-owner-questions.md`.
- A verification badge asserts that something was verified. Phase C reports **0 of 20 fields
  verified:true**; there is no verified entity, licence, insurance or ABN behind this site. The badge
  names no verifying body and points at no credential.
- All 14 instances carry alt text beginning `"Verified badge …"`, so the claim also reaches assistive
  technology and search engines.

### Pages using it — verified against `camden-concreting-import.xml` directly

15 items reference the asset: the 14 pages below, plus attachment item 1067 itself.

```text
   #  status   id    page                                                      use
   1  publish  221   /concreters-leppington/                                   standalone image
   2  draft    1372  /concreters-narellan/                                     standalone image
   3  draft    1376  /concreters-currans-hill/                                 standalone image
   4  draft    1380  /concreters-camden-south/                                 image-box "Concrete Slabs"
   5  draft    1391  /concreters-west-hoxton/                                  image-box "Concrete Driveways"
   6  draft    1414  /concreters-glen-alpine/                                  image-box "Paths & Pathways"
   7  draft    1427  /guides/wollondilly-council-driveway-crossing/            standalone image
   8  draft    1429  /guides/do-i-need-council-approval-driveway-nsw/          standalone image
   9  draft    1445  /guides/coloured-concrete-explained/                      standalone image
  10  draft    1456  /guides/removing-oil-stains-and-tyre-marks-from-concrete/ standalone image
  11  draft    1472  /concrete-slabs-leppington/                               standalone image
  12  draft    1485  /concrete-driveways-catherine-field/                      standalone image
  13  draft    1493  /concrete-driveways-spring-farm/                          standalone image
  14  draft    1497  /concrete-driveway-replacement-currans-hill/              standalone image
```

**One page is `publish`: `/concreters-leppington/`**, which sits in the Wave 1 release set. It
already carries false-fidelity sentence 1 of 6 and is already held `noindex,follow` under the Tier 1
evidence gate, so NT-1 is a third independent blocker on a page that was already held. **Effective
indexable Wave 1 is unchanged at 14.** The other 13 are draft and enter no wave.

On three pages the badge is not used as a badge at all but as the illustration of a service tile
titled *Concrete Slabs*, *Paths & Pathways* and *Concrete Driveways*. That is a second, independent
fault of the §4.22.4 class — an image that does not depict what its caption says it depicts —
found here by filename rather than by sighting.

---

## 8. EXIF inventory — read-only, driver not run

The re-encode driver was **not** run and no file was modified. `exiftool` was used read-only across
all 83 required binaries, because these binaries have never been examined and the P0 concern is
Melbourne GPS coordinates reaching a live site.

```text
  GPS latitude / longitude / position          0 files   ← the P0 risk does not materialise
  Artist / Copyright / OwnerName / SerialNumber 0 files
  Make / Model (camera)                        0 files
  DateTimeOriginal                             6 files
  UserComment                                  1 file
  Software                                    11 files
  ICC ProfileCopyright / DeviceModel           4 files
  C2PA content-credential manifest             2 files
```

**No GPS data and no camera/owner identification anywhere in the delivered set.** The single largest
stated risk in `CONTEXT.md` §"before authoritative staging import" 2a does not materialise in these
binaries. That is a finding about *these* files; the driver is still required, still unrun, and the
D25.2 fail-closed assertion still has to pass on its own terms after re-encoding.

Still to be stripped:

```text
  DateTimeOriginal   concrete-testimonial-1.webp      2025:05:08 13:33:24
                     concrete-testimonial-1-1.webp    2025:05:08 13:33:24
                     concrete-testimonial-2.webp      2026:01:19 16:22:53
                     concrete-testimonial-3.webp      2026:07:05 12:08:36
                     patiosandpathways.webp           2025:01:28 12:53:14
                     reinforcedheavydutycocnreer.webp 2024:05:08 14:03:10
  UserComment        backyard-patio-concreter (1).jpg  xr:d:DAEs8AkRkpw:853,…  (Adobe asset id)
  Software           Picasa (8 files), Instagram (1), paint.net 5.0.6 (1)
```

### 8a. New finding — C2PA credentials name the image generator

Two required binaries carry an intact C2PA content-credential manifest:

```text
  ChatGPT-Image-Jul-6-2026-01_52_19-PM.png   ActionsSoftwareAgentName: gpt-image  v2.0
  eandtcologo.png                            ActionsSoftwareAgentName: gpt-image  v2.0
```

`CONTEXT.md` records *"Three AI-generated images, one (272) live on 14 pages — a direct standing rule
3 breach. Flagged, not classified."* This is the first **binary-level** evidence for that finding:
the assets state their own generator rather than merely being inferred from a filename. One of the
two is `eandtcologo.png` — the E&T logo itself.

This does not close that item. It confirms two, by different evidence than filename; the third is not
identified here, and classification remains open. Recorded so the next stage starts from evidence
rather than from a filename heuristic.

---

## 9. What is and is not cleared

**Not cleared.** The blocker *"obtain the original 83 image binaries"* is **not** marked resolved.
The binaries have arrived and are content-complete, which is a different statement. Before it can be
cleared:

1. The Astra Customizer export must arrive. Phase B is blocked at step 2 regardless of media.
2. The six ` (1)` files must be renamed to their authoritative names, on approval.
3. `scripts/22-media-audit.py` must be re-run after the rename and must **pass on its own terms**.
4. The re-encode driver must run in WSL and the D25.2 EXIF assertion must pass afterwards.
5. §4.22.4 pixel-level sighting must be performed. It never has been, on any image. The 20 Victorian
   photographs renamed to NSW places are still unaddressed and no metadata check will catch them.

**Cleared, narrowly.** ImageMagick and exiftool are installed and verified in WSL. The precondition
gate's ImageMagick probe targets the wrong host and reports otherwise; the probe is the defect, not
the environment.

---

## 10. Immutable hash table

Recomputed at the end of this session, after the only write performed (an append to
`reports/23-false-fidelity.md`, which is a report and not an immutable file).

```text
  camden-concreting-import.xml
    A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884   MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
    45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15   MATCH
  build/stage9-page-manifest.json
    578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42   MATCH
  build/stage8-image-map.json
    0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF   MATCH
  reports/08-image-rename-map.csv
    43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8   MATCH
  CODEX-BUILD-2.1.md
    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C   MATCH
  archive/governing/CODEX-BUILD-2.md
    E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5   MATCH

  7 of 7 MATCH.
```

---

## 11. Next safe action

Obtain the **Astra Customizer export**. It is the only remaining input blocking Phase B, and no
amount of media work advances past step 2 without it.

Owner decisions raised by this audit, none of them acted on:

1. Approve the rename of the six ` (1)` files to their authoritative names (§4).
2. Confirm removal of `verified-badge` from all 14 pages, or supply a verifying body, the credential
   verified, and a sightable source (§7).
3. Remove the two personal résumé PDFs from the media directory (§6b).
4. State whether `eamptcoconcretersmelbourne.WordPress.2026-08-18.xml` supersedes anything. It has
   not been read (§6b).
5. Decide replacement imagery for the three service tiles that currently use the badge (§7).
