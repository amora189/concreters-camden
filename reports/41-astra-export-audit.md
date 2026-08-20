# Stage 41 — Astra Customizer export audit and reconciliation

Date: 19 August 2026 (Australia/Sydney).
File: `source-inputs/astra/astra-export.dat`, 2,627 bytes,
SHA-256 `F4841CF538810C9A7A2CBCBD28B145AACD4DF45AA8C6407E4EEA45356DB7AA01`.

**Audit only.** Nothing imported, re-encoded or implemented. The seven immutable hashes are
re-verified in §8 and all match.

---

## 1. Gate results

### `scripts/22-astra-audit.py` — **FAIL**

```text
  candidates=1  parsed=1  groups_present=1/7  failures=6
  VERDICT: FAIL — Astra intake incomplete

  site-identity    PRESENT  custom_logo, site_icon
  colours          ABSENT
  typography       ABSENT
  layout           ABSENT
  header           ABSENT
  footer           ABSENT
  buttons          ABSENT
```

**This is a partial export.** It parses cleanly as a genuine PHP-serialised Customizer export —
2,627 of 2,627 bytes consumed, no remainder — so the format is real. What is missing is the content:
six of the seven mod groups the build depends on carry nothing.

### Precondition gate — Phase B still **BLOCKED**

```text
  B   media and staging   BLOCKED   media 172/83; astra 1 file(s); driver present;
                                    ImageMagick NOT INSTALLED
  RUNNABLE PHASES: NONE
```

The file-count precondition (`astra >= 1`) is now satisfied, so the gate's *arithmetic* reason for
blocking Phase B has gone. Phase B is still BLOCKED, on the ImageMagick probe defect already
recorded — the probe targets Windows, the driver runs in WSL. **The audit is the real gate here, and
it fails.** A file that satisfies a count and fails its content audit has not unblocked anything.

---

## 2. What the export actually contains

Decoded in full rather than key-probed.

```text
  template   "astra"

  mods       0                      => false          (stray artifact, integer key)
             nav_menu_locations     => primary:9, mobile_menu:10, footer_menu:13
             custom_css_post_id     => 893
             custom_logo            => 469

  options    site_icon              => "472"
             astra-settings[ast-callback-notice-header-transparent-header-logo]      => ""
             astra-settings[ast-callback-notice-header-transparent-header-logo-link] => ""
             astra-settings[ast-header-retina-logo]                                   => ""
             astra-settings[mobile-header-logo]                                       => ""
             astra-settings[ast-callback-notice-header-transparent-meta-enabled-with-link] => ""
             astra-settings[transparent-header-logo]                                  => ""
             astra-settings[transparent-header-retina-logo]                           => ""
             nav_menus_created_posts => (empty)

  wp_css     1,832 characters, entirely .local-work-card rules
```

**Every one of the eight `astra-settings[...]` keys is an empty string.** They are logo-callback and
retina/transparent-logo slots with no values. The export therefore carries **four** pieces of real
configuration: the logo, the site icon, the CSS post pointer, and three menu locations.

### What this does not answer

`CONTEXT.md` has recorded since the pause that *"the header logo is undeterminable until the Astra
export arrives"* and that the export *"governs header rendering"*. Half of that is now resolved and
half is not:

- **Resolved:** which attachment is the header logo (469) and which is the site icon (472).
- **NOT resolved:** how the header renders. There is no `header-layouts`, no
  `header-main-layout-width`, no `transparent-header-enable`, no `footer-layout`, no
  `site-content-width`, no colour and no typography. Astra will fall back to its **defaults** for all
  of it.

The header/footer/mobile logo slots in runbook step 5c were waiting on this export. They are still
waiting — the export names the logo but not the header structure that places it.

---

## 3. Point 1 — `custom_logo` 469 and `site_icon` 472

### Classification

| | `custom_logo` | `site_icon` |
|---|---|---|
| Attachment ID | **469** | **472** |
| Current filename | `corex-concreters-camden-logo-469.png` | `corex-concreters-camden-logo-472.png` |
| E&T source file | `cropped-e-t-co-logo-transparent.png` | `cropped-e-t-co-logo-512.png` |
| Dimensions | 507 × 296 | 512 × 512 |
| Bytes | 104,719 | 141,390 |
| Pages referencing it | **0** | **0** |
| `site_icon-*` sizes in WXR | no | **yes** |

Both are **E&T Co source-business logo files**, cropped derivatives of the `e-t-co-logo-*` family
(468 and 471, the uncropped originals, which are byte-identical to each other).

**Neither was in the retired set** — correct. 159, 177, 306, 307 and 422 were retired; 469 and 472
were not, because nothing in the WXR referenced them. That is exactly why they looked orphaned:
**theme mods do not travel in a WXR**, so the only record that these two are the live logo and
favicon was sitting in the file that did not exist until today. 469 and 472 are the sixth and seventh
brand files, not the sixth alone.

### AI generation and C2PA

Both were checked directly with `exiftool`.

```text
  469  cropped-e-t-co-logo-transparent.png   no C2PA, no JUMBF, no gpt-image, no AI markers
  472  cropped-e-t-co-logo-512.png           no C2PA, no JUMBF, no gpt-image, no AI markers
  468  e-t-co-logo-transparent.png           clean
  471  e-t-co-logo-512.png                   clean
```

They are also **not derived from** `eandtcologo.png`, the file that does carry credentials.
Perceptual comparison at matched scale gives RMSE 0.65–0.67 against the eandtcologo family — a
different mark entirely, not a crop or recolour of it.

**But absence of C2PA does not establish that an image is not AI-generated, and this file set proves
it.** `eandtcologo.png` (attachment 308) carries a complete C2PA manifest:

```text
  Claim_Generator_InfoName    OpenAI Media Service API
  ActionsSoftwareAgentName    gpt-image  v2.0
  ActionsAction               c2pa.created, c2pa.converted, c2pa.watermarked.unbound
  ActionsDigitalSourceType    http://cv.iptc.org/newscodes/digitalsourcetype/
                              trainedAlgorithmicMedia          <- the IPTC code for AI-generated
  ActionsWhen                 2026:07:07
```

Its own crop, `cropped-eandtcologo.png` (attachment 309), carries **zero** C2PA. The crop stripped
the manifest. So for 469 and 472 the honest finding is:

> **No positive evidence of AI generation. The negative cannot be established from the binaries**,
> because a cropped AI image in this very set reads as clean. Both are cropped derivatives, which is
> the exact transformation that erases the evidence.

This does not change the outcome, which is why it is recorded rather than escalated.

### Recorded regardless

**The Structure Co wordmark and icon replace both, whatever their provenance.** 469 and 472 are the
source Melbourne business's mark. Retaining them would keep another business's logo as this site's
header logo and favicon — the same fault as the kit `site_name`, and a harder one, because it is
visible on every page.

```text
  custom_logo  469  ->  structure-co-horizontal.svg
  site_icon    472  ->  structure-co-icon-512.png   (PNG, not SVG)
```

**Correction to DECISION-05 D27.** D27 directed *"Remove attachment 177 as site icon."* Per this
export, **177 is not the site icon — 472 is.** The WXR carries generated `site_icon-*` sizes for
*both* 177 and 472, consistent with 177 having been the site icon earlier and 472 having replaced it
before the export was taken. D27's instruction targeted a former favicon. The operative one is 472,
and it was not in the retired set until now.

Retirement list, updated: **159, 177, 306, 307, 422, 469, 472.**

---

## 4. Point 2 — `custom_css_post_id` 893

**The ID reconciles exactly.** The main WXR contains one `custom_css` record:

```text
  post_type  custom_css      post_id  893      post_name  astra
  status     publish         title    astra
```

`reports/13-id-collision-audit.md` already records it: *"Astra custom CSS | 1 | ID 893"*. The mod
points at the right post.

### But the two artifacts disagree about that post's content

Both the WXR record and the export's `wp_css` define the body of post 893, and **they are not the
same**.

```text
  WXR post 893 content:encoded   1,830 chars   sha256 BC9C77D2378D64CF...
  astra-export.dat wp_css        1,832 chars   sha256 4D4B798F9E306C49...
  identical?                     NO
```

The entire difference is one line:

```diff
--- WXR post 893 content:encoded
+++ astra-export.dat wp_css
@@ -1,2 +1,2 @@
-/* Local Camden project cards */
+/* Local Werribee project cards */
 .local-work-card {
```

Everything else is byte-identical. **The WXR version has been through the rename; the export has
not.** The export is a pre-rename snapshot of the same stylesheet.

```text
  WXR post 893      Werribee 0   Camden 1
  astra-export.dat  Werribee 1   Camden 0
```

**This is a regression hazard, not a cosmetic one.** `Werribee` appears **zero** times in the entire
main WXR. This export is the only importable artifact in the build that contains it. Importing it
reintroduces a source-location footprint string that the build had already eliminated.

**And the runbook imports the export first.** Step 2 imports the Astra Customizer settings; step 4
imports the WXR. Which version of post 893 survives depends on how each importer treats an existing
custom_css post, and that interaction has never been tested for this file. Either outcome is a
problem worth naming:

- If the WXR wins, the mod's target content is the Camden version — correct, but only by accident of
  ordering.
- If the export wins, the live stylesheet carries `/* Local Werribee project cards */`.
- If they do not bind to the same post, there are two custom_css posts and `custom_css_post_id: 893`
  may point at the wrong one.

**Recommendation, not executed:** correct the comment in the export to match the WXR before import,
or strip `wp_css` from the export and let the WXR supply post 893. Either makes the ordering
irrelevant. This is an owner decision because it means editing a supplied input.

---

## 5. Point 3 — `.local-work-card` and the D32 removal

### Where the class is used

```text
  .local-work-card  (CSS selectors)   10 occurrences, all inside custom_css post 893
  local-work-card   (_css_classes)    45 occurrences, on 15 suburb pages, 3 per page
                                      6 publish, 9 draft
```

Pages: `concreters-oran-park`, `-leppington`, `-gregory-hills`, `-gledswood-hills`, `-austral`,
`-harrington-park` (all publish), plus `-bringelly`, `-catherine-field`, `-cobbitty`,
`-currans-hill`, `-edmondson-park`, `-elderslie`, `-mount-annan`, `-narellan`, `-spring-farm`
(draft).

### Are the rules dead?

**Not yet — and that is the point.** D32 directed removal of the evidential "Local Work Completed"
module from 16 pages. The WXR is immutable, so **the removal has not happened**: all 45 class
usages are still in the artifact and will import.

```text
  BEFORE D32 is executed   the CSS is LIVE and styles 45 elements on 15 pages
  AFTER  D32 is executed   the CSS is DEAD — 1,832 bytes of rules matching nothing
```

So the correct statement is conditional: the rules are **not dead today, and become dead the moment
the D32 removal is applied post-import.** They should be removed in the same operation, not left
behind — dead CSS that styles a removed evidential module is a trace of the module having existed.

The 15 pages here versus D32's 16 is worth checking during that step; this audit counts the class,
not the module, and a page could carry the module without this class.

### The Werribee comment as a footprint string

Registered. `/* Local Werribee project cards */` is:

- the **only** occurrence of `Werribee` in any importable artifact — the main WXR has zero;
- **not** covered by the post-import rename steps 5a–5d, which target `CoreX`, `E&T` and
  `Camden based` in `post_title`, `post_content`, `postmeta`, `options`, `theme_mods`, term names and
  menu labels. A comment inside `wp_css` is reached only if the search-replace covers the custom_css
  post's content;
- **not** covered by preflight gate 13, which asserts the source *business* name, not source
  *locations*.

`build/global-replace.json` does carry a `Werribee` rule — now at index 16 after the ordering fix —
so a regeneration would catch it. An import would not.

**Registered as a footprint string for the rename**, with the note that it needs its own assertion:
the existing gates would not have caught it.

---

## 6. Point 4 — `nav_menu_locations`, and a Wave 1 problem

### The mapping, resolved against the WXR's terms

The WXR defines five `nav_menu` terms:

```text
  term  9   primary            "Primary"
  term 10   primary-2          "Primary (2)"
  term 11   footer-services    "Footer Services"
  term 12   footer-areas       "Footer Areas"
  term 13   footer-blogs       "Footer Blogs"
```

The export assigns three:

| Astra location | Term | Menu | Items |
|---|---:|---|---:|
| `primary` | 9 | Primary | 23 |
| `mobile_menu` | 10 | Primary (2) | 23 |
| `footer_menu` | **13** | **Footer Blogs** | 6 |

**The two with no location are `footer-services` (11) and `footer-areas` (12).**

### Is that correct for Wave 1? No — and the assignment is inverted

Three of five menus is not itself wrong: Astra registers three theme locations in this export, and
the remaining two menus would be placed by the Footer Builder or an Elementor widget, not a theme
location. The problem is **which** menu got the footer location.

```text
  MENU               ITEMS   PAGE TARGETS   WITHDRAWN   DRAFT
  primary              23         21             7        7
  primary-2            23         21             7        7
  footer-services       7          7             0        0
  footer-areas          6          6             0        0
  footer-blogs          6          6             6        6    <- assigned to footer_menu
```

**Every one of Footer Blogs' six targets is withdrawn AND draft:**

```text
  555   concrete-driveway-cost-nsw            draft, WITHDRAWN
  706   camden-council-driveway-crossing      draft, WITHDRAWN
  1425  liverpool-council-vehicle-crossing    draft, WITHDRAWN
  1215  why-concrete-cracks                   draft, WITHDRAWN
  1430  reactive-clay-slabs-as2870            draft, WITHDRAWN
  1431  salinity-and-concrete-western-sydney  draft, WITHDRAWN
```

Applying this mapping as supplied would put **six links to withdrawn, draft, noindexed pages into the
site footer on every page**. That is a direct breach of the standing safeguard in `CONTEXT.md`: *"Do
not expose draft guide links in Wave 1 menus."*

**The inversion is the striking part.** The two menus with **zero** withdrawn and **zero** draft
targets — Footer Services and Footer Areas — are the two the export leaves unassigned. The one that
is 100% withdrawn is the one it assigns.

**`primary` and `mobile_menu` are also unsafe as supplied**: 7 of 21 page targets in each are
withdrawn and draft.

### What this means for Stage 29 step 4

The export supplies the assignment data, and **the data is not usable as supplied**. Runbook step 8
currently says to assign the five menus "to the appropriate theme locations", which also mis-states
the shape of the problem — there are five menus and three locations, and the mapping is a decision,
not a lookup.

Recorded for Stage 29, **not executed**:

1. Do **not** apply `footer_menu → 13` as supplied.
2. `footer_menu` should take **Footer Services (11)** or **Footer Areas (12)** — both are clean.
   Which one is an owner decision.
3. `primary` (9) and `mobile_menu` (10) need their 7 withdrawn/draft items pruned before Wave 1,
   or the menus rebuilt from `build/stage9-menus.json` against the 77-page architecture.
4. Add a preflight assertion: **zero menu items in an assigned location may target a withdrawn,
   draft or noindexed page.** No existing gate covers this — it is why the mapping arrived unflagged.

---

## 7. Summary

```text
  the export is GENUINE           parses cleanly, 2,627/2,627 bytes, template astra
  the export is PARTIAL           1 of 7 required mod groups; audit FAILS
  it answers                      which attachment is the logo (469) and favicon (472)
  it does NOT answer              how the header renders — no layout, colour, typography,
                                  header, footer or button mods at all
  it introduces                   one Werribee footprint string absent from every other artifact
  it supplies                     menu assignment data that is unsafe as given
  Phase B                         still BLOCKED
```

**Four findings that need an owner decision, none acted on:**

1. **472 is the site icon, not 177.** D27's removal instruction named the wrong attachment. Retirement
   list becomes 159, 177, 306, 307, 422, **469, 472**.
2. **The export's `wp_css` would reintroduce "Werribee"** into post 893, which the WXR has already
   corrected to "Camden". Fix the export or strip `wp_css` from it before import.
3. **`footer_menu → Footer Blogs` must not be applied** — 6 of 6 targets withdrawn and draft.
   Choose Footer Services or Footer Areas instead, and prune `primary` / `mobile_menu`.
4. **The `.local-work-card` CSS becomes dead when D32 is executed.** Remove the rules in the same
   operation rather than leaving 1,832 bytes styling nothing.

Astra design fidelity is **not** restored by this file. If the intent was to preserve the approved
Astra/Elementor design, this export does not carry it, and a full Customizer export — colours,
typography, layout, header, footer, buttons — is still outstanding.

---

## 8. Immutable hash table

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
