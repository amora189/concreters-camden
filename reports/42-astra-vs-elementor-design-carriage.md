# Stage 42 — where the design actually lives: Astra vs Elementor

Date: 19 August 2026 (Australia/Sydney).
Authority: owner instruction, 19 August 2026 — decision 4, *"verify… report which of the seven mod
groups are genuinely absent versus simply unset… confirm whether the Elementor kit carries the
colours, typography and button styles the audit expected from Astra."*

**Findings only. Nothing imported, nothing revised yet.** Immutable hashes unchanged.

---

## 1. The hypothesis, and how it fared

> *"The Astra export is likely complete as supplied… consistent with E&T running Astra near-stock and
> Elementor carrying the design."*

**First half: supported. Second half: half right, and the correction matters.**

Astra is near-stock — the export's shape is exactly what a never-customised Astra install produces.
But **the Elementor kit is also stock.** The design is not in the kit either. It is inlined
per-widget across 156 pages.

---

## 2. The Elementor kit is factory-default

`_elementor_page_settings` on the Default Kit (post 6), decoded in full — 1,754 of 1,754 bytes.

```text
  system_colors        #6EC1E4  #54595F  #7A7A7A  #61CE70   <- Elementor factory palette
  system_typography    Roboto / Roboto Slab / Roboto / Roboto  <- Elementor factory fonts
  custom_colors        {} empty
  custom_typography    {} empty
  site_logo            url:"" id:""     <- EMPTY
  site_favicon         url:"" id:""     <- EMPTY
  button settings      NONE — zero button, form_field, container_width,
                       space_between_widgets, body_typography or h1_typography keys
```

Twelve keys total, and the only non-default values are `site_name`, `site_description`,
`page_title_selector` and the two viewport breakpoints.

**So the kit does not carry the colours, typography or button styles the audit expected from Astra.**
It carries Elementor's factory defaults for the first two and nothing at all for the third.

### Where the design actually is

```text
  HEX        TOTAL   IN KIT   IN PAGE _elementor_data
  #1C244B      732       0        732
  #324A6D      901       0        901
  #467FF7      851       0        851
  #6EC1E4        1       1          0     <- Elementor default, kit only, never used
  #54595F        1       1          0     <- ditto
  #7A7A7A        1       1          0     <- ditto
  #61CE70        1       1          0     <- ditto

  typography_font_family across all pages:  Poppins x2,655  — ONE family, all in page data.
                                            The kit says Roboto. Nothing uses Roboto.
```

**The design is inlined per-widget in `_elementor_data` on 156 pages.** Neither Astra theme mods nor
the Elementor kit governs it.

### A correction this forces

`DECISION-08` D36 and the ledger record navy `#1C244B` as *"taken from the Elementor kit"*. **It is
not in the kit** — zero occurrences there, 732 in page data. The colour is right; the provenance
sentence is wrong and should be corrected to "taken from the source site's inlined page styling".

Also worth recording accurately: brand grey **`#7C8494` appears 0 times in the WXR**. It is a genuinely
new colour, not inherited.

---

## 3. Genuinely absent vs simply unset

A WordPress Customizer export carries `theme_mods`, and Astra keeps its settings in the
`astra-settings` option. **Both store only what has been explicitly set** — an untouched setting has
no key at all and Astra returns its default at runtime. So "absent from the export" and "never
customised" produce an identical file.

The export's eight `astra-settings[...]` keys are all present-but-empty, and all eight are
logo-callback / retina / transparent-header slots. That is the signature of a site where someone
opened the logo panel and set nothing else.

| Group | Verdict | Basis |
|---|---|---|
| site-identity | **SET** | `custom_logo: 469`, `site_icon: 472` — real values |
| colours | **UNSET, not missing** | no `astra-settings[theme-color]` key; page data carries the colours |
| typography | **UNSET, not missing** | no `astra-settings[body-font-family]` key; Poppins is inlined per widget |
| layout | **UNSET, not missing** | no `site-content-width` / `site-layout` key |
| header | **UNSET, not missing** | the 8 empty logo-slot keys are the only header-adjacent entries |
| footer | **UNSET, not missing** | no `footer-sml-layout` key |
| buttons | **UNSET, not missing** | absent from Astra **and** from the Elementor kit |

**I could not verify Astra's shipped defaults directly.** The only Astra artifact on disk is
`staging/vendor/astra.4.13.9.zip`, and Docker is not running, so no default `astra-settings` array
was read. The table above is inference from export semantics, not a value-by-value diff against a
live Astra install. Stated as inference so it is not mistaken for a comparison that was run.

---

## 4. What this means for the audit

**The owner is right that the current check is wrong.** `REQUIRED_GROUPS` asserts that Astra carries
colours, typography, layout, header, footer and buttons. On this site Astra carries none of them and
never did, so the check fails a correct file. A stock configuration is not a partial export.

**But deleting the groups would replace a wrong check with no check.** The finding that actually
matters — the design is inlined across 156 pages, in neither Astra nor the kit — is a real fragility
and currently nothing asserts it.

Proposed revision, **not implemented pending approval**:

```text
  KEEP as required
    site-identity      custom_logo and site_icon must resolve to real attachment IDs

  DOWNGRADE to reported-not-required
    colours, typography, layout, header, footer, buttons
      -> report SET or UNSET; UNSET is a valid stock configuration, not a failure

  ADD as required — this is the check that was missing
    design-carriage    the design must be locatable. Assert that colours and
                       typography resolve from at least one of: Astra mods,
                       the Elementor kit, or page _elementor_data — and REPORT
                       WHICH. On this build the answer is page data, which means
                       there is no single place to restyle the site.

  ADD as required
    internal-consistency   every attachment ID referenced by the export
                           (custom_logo, site_icon) must exist in the WXR
                           every menu term ID must exist as a wp:term
                           custom_css_post_id must match the WXR custom_css record
```

That converts a check that fails a correct file into one that would have caught the three things this
audit found by hand: the logo/favicon identity, the 893 content conflict, and the menu mapping.

---

## 5. Menu decision — corroborated

The owner's choice of **Footer Services** is independently confirmed by
`build/27-wave1-menus.json`, which already existed:

```text
  MENU              SOURCE  RETAINED  REMOVED
  Primary              23      10       13
  Primary (2)          23      10       13
  Footer Services       7       7        0    <- fully clean
  Footer Areas          6       0        6
  Footer Blogs          6       0        6
```

**Footer Areas would also have been unsafe**, which the earlier audit did not surface. Its 6 targets
carry zero withdrawn and zero draft — but all six are Tier 1 suburb pages **held `noindex,follow`**
(Oran Park, Leppington, Gregory Hills, Gledswood Hills, Austral, Harrington Park). It fails the Wave 1
test on the third condition, not the first two.

**Footer Services is the only one of the five menus that survives Wave 1 filtering intact** — 7 of 7
retained. The owner's assignment is the only safe one available.

This also confirms the proposed preflight assertion must test **all three** conditions — withdrawn,
draft, **and noindex-held**. Testing only the first two would have passed Footer Areas.
