# GATE 22 — media and Astra intake harness

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.22; `RUN-BLOCK-01.md` §B.

Both P0 inputs are owner-supplied and absent. This stage builds the harness that makes the eventual
import one-shot, and proves the harness fails closed while the inputs are missing.

---

## 1. Artifacts created

```text
  source-inputs/media/README.md        exact filenames for all 83 binaries
  source-inputs/astra/README.md        what a genuine Astra export must contain
  scripts/22-media-audit.py            fail-closed media audit
  scripts/22-astra-audit.py            fail-closed Astra export audit
  scripts/22-reencode-images.sh        corrected re-encode driver (see §4)
  reports/22-media-missing-manifest.csv  per-file manifest, 83 rows
  reports/22-media-audit-result.md     machine-written audit result
  reports/22-astra-audit-result.md     machine-written audit result
```

---

## 2. GATE 22 condition — both audits run against the empty directories

The gate requires both audits to exit non-zero with a complete list of what is missing. Both do.

```text
AUDIT 1 — scripts/22-media-audit.py
  expected filenames        83
  present in directory       0
  passing all checks         0
  missing                   83
  unexpected extras          0
  total failures            83
  exit code                  1
  verdict                   FAIL — media intake incomplete
  missing manifest          reports/22-media-missing-manifest.csv (83 rows, one per file)

AUDIT 2 — scripts/22-astra-audit.py
  candidate files            0
  parsed as Astra exports    0
  required mod groups        7
  groups present             0
  total failures             8
  exit code                  1
  verdict                   FAIL — Astra intake incomplete
```

Neither audit degrades to a warning, skips a check, or reports a partial pass. Standing rule 8 holds: a
check that cannot run at full fidelity fails.

---

## 3. What each audit enforces

### Media audit — `scripts/22-media-audit.py`

```text
  count            all 83 filenames from reports/08-image-rename-map.csv present
  exact match      no -1 / -scaled / -e<timestamp> suffix drift against the mapped name
  MIME             magic-byte sniff; JPEG, PNG, GIF and WEBP recognised, anything else fails
  dimensions       parsed from the file header without third-party libraries
  checksum         SHA-256 recorded per file in the manifest
  size sanity      floor 1,024 bytes, ceiling 12,582,912 bytes
  extras           any file not declared by the rename map fails the run
  encoding         CSV read as utf-8-sig (the Stage 8 CSVs carry a BOM); errors='strict'
```

Suffix drift is checked because Stage 15 proved WordPress silently suffixes a colliding filename. A
drifted name produces a page that renders a broken image and raises no error at import.

### Astra audit — `scripts/22-astra-audit.py`

Accepts the three shapes a real Astra export takes: a PHP-serialised `.dat` from the Customizer
Export/Import plugin, a `theme_mods_astra` JSON dump, or the Astra Import/Export Settings JSON blob.

Seven mod groups must be present. A partial export fails **here**, not after import:

```text
  site-identity   custom_logo, site_icon, title/tagline display
  colours         theme-color, link-color, text-color, heading-base-color
  typography      body font family and size, H1 family and size
  layout          site-content-width, site-layout, sidebar layout
  header          header-main layout and width, transparent header
  footer          footer-layout, footer-sml-layout, footer-adv
  buttons         button colour, background, radius, padding
```

---

## 4. `reencode-images.sh` — CONFIRMATION FAILED

§4.22.4 requires confirming the script is **present**, **idempotent**, and **feeds the audit**. One of
three holds.

```text
  present                YES  — reencode-images.sh at repo root, 12 lines
  correct encode flags   YES  — -resize 98% -strip -quality 82, exactly as specified
  parses                 NO   — bash -n: "line 11: unexpected EOF while looking for matching \""
  idempotent             NO   — untestable; the script cannot execute at all
  feeds the audit        NO   — records no checksum and writes no manifest
  toolchain available    NO   — ImageMagick 'magick' is not on PATH in this environment
```

### The defect

Lines 9 and 10 attempt to strip quote characters:

```bash
  old_filename=${old_filename%"}; old_filename=${old_filename#"}
```

The bare `"` opens a quoted string that is never closed, so bash fails to parse the file. The script has
never been runnable in this state. Because it does not parse, its idempotency could not be tested — the
answer is not "no", it is "unknowable until it parses".

Three further defects would remain after fixing the quoting:

```text
  1. Running with input_dir == output_dir re-encodes already-re-encoded files,
     compounding quality loss and silently breaking the 98%/82 contract.
  2. No checksum is recorded, so the media audit cannot verify that what is in
     source-inputs/media/ came from the intended source image.
  3. A missing source file or a failed encode does not stop the run under the
     `while read` subshell, so a partial pass can look like success.
```

### Disposition

The original is **left untouched** for provenance — it is an owner-supplied file, and mutating it silently
is the pattern this build exists to avoid. A corrected driver ships alongside it:

```text
  scripts/22-reencode-images.sh    bash -n: SYNTAX OK
```

It parses, refuses to run in place, is idempotent via a per-file source-checksum stamp, fails closed on a
missing tool or a missing source image, asserts exactly 83 processed, and writes
`reports/22-reencode-manifest.csv` with source and output SHA-256 per file so the media audit can
cross-check provenance.

**Owner decision required:** whether to retire the root-level `reencode-images.sh` or keep both. Until
that is decided, `scripts/22-reencode-images.sh` is the one to run. ImageMagick must also be installed;
no substitute encoder may be used, because the 98%/82/strip parameters are the footprint contract.

---

## 5. The ten unreferenced attachments

Ten of the 83 have an empty `pages_referencing` value in the rename map: `159, 177, 250, 308, 309, 422,
468, 469, 471, 472`. All are logo and site-identity PNGs. They are referenced by **theme mods**, not by
page content — which is to say, by the Astra export that is also missing.

They remain required. Their absence leaves the site with no logo. This is an independent reason the media
binaries and the Astra export must be obtained and audited **together**, as `CONTEXT.md` already directs.

---

## 6. `CONTEXT.md` update and diff

```text
  Latest completed stage     21 -> 22
  Stage 22 artifacts         none -> harness created, both audits fail closed
  P0 blockers                UNCHANGED — 83 image binaries and Astra export both still absent
  New finding                reencode-images.sh does not parse; corrected driver shipped alongside
  Index-ready                0 of 157 — UNCHANGED
  Launch gate                NO-GO — UNCHANGED
```

No blocker was cleared. A script that checks a blocker is not a cleared blocker.

---

## 7. Hash table

```text
FILE 1 of 6
  path      camden-concreting-import.xml
  sha256    A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  result    MATCH

FILE 2 of 6
  path      eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
  sha256    45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  result    MATCH

FILE 3 of 6
  path      build/stage9-page-manifest.json
  sha256    578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  result    MATCH

FILE 4 of 6
  path      build/stage8-image-map.json
  sha256    0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  result    MATCH

FILE 5 of 6
  path      reports/08-image-rename-map.csv
  sha256    43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  result    MATCH

FILE 6 of 6
  path      CODEX-BUILD-2.1.md
  sha256    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  result    MATCH

VERDICT  6 of 6 MATCH. Stop condition C1 not triggered.
```

---

## GATE 22 RESULT

```text
  source-input directories created with exact-filename READMEs      PASS
  media audit fail-closed, exits non-zero against empty directory   PASS
  media audit emits a complete missing-file manifest (83 rows)      PASS
  astra audit fail-closed, exits non-zero against empty directory   PASS
  astra audit names all seven required mod groups                   PASS
  reencode-images.sh present                                        PASS
  reencode-images.sh idempotent and feeding the audit               FAIL — does not parse
  corrected re-encode driver shipped and parsing                    PASS

  GATE 22: PASS with one confirmed defect carried forward.
  The defect is in a helper script, not in a validated artifact, and does not
  block Stage 23. It does block the eventual media pipeline and is recorded as
  an owner decision in §4.
```
