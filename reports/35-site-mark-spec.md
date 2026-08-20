# Stage 35 — site mark specification (D27)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-05-figures-mark-pause.md` §D27.

**Decision: a text wordmark. No image mark ships.**

**NOT IMPLEMENTED.** The Astra Customizer export governs header rendering and does not exist. This is a
specification for the owner to approve and for a later stage to apply.

---

## 1. A finding that changes what the wordmark must say

The Elementor kit still carries the **source Melbourne business's trading name**:

```text
  elementor_library "Default Kit", _elementor_page_settings

    site_name          "E&T Co Concreters Camden"
    site_description   "Camden based Concrete Company Site"
    site_logo          url:"" id:"" alt:"Concreters in Camden"      <- empty slot
    site_favicon       url:"" id:"" alt:"Concreters in Camden"      <- empty slot
```

`E&T Co` is the source business — the same entity behind `e_t_co_concreters_favicon_512_symbol_only.png`
(attachments 306/307/422) and `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml`. The name appears
**6 times in the source WXR** and survives once in the main artifact, with "Camden" appended.

```text
  "CoreX" occurrences in the main WXR              345
  "E&T Co Concreters Camden" in the Elementor kit    1
```

**There are two trading names in this artifact and neither is verified.** `data/verified-facts.yml`
records `trading_name: "CoreX Concreters Camden"` with `verified: false`, and the legal entity behind it
is unknown.

This is a residual footprint of the same class as the shared module order and kit palette, and it is a
harder signal: a site's declared name matching another business's.

---

## 2. Wordmark specification

```text
  TEXT
    primary        "CoreX Concreters Camden"
    OWNER MUST CONFIRM: this is the name to use, and E&T Co is removed from the kit.
    Until confirmed, the wordmark is BLOCKED on the same identity question that
    blocks all schema.

  WHAT IT MUST NOT CARRY (D27.3)
    no ABN                    unverified
    no licence number         unverified
    no insurance claim        unverified
    no "licensed" / "insured" unverified
    no "established since"    unverified
    no address                unverified, and staffing status unknown
    trading name only

  TYPEFACE — from the existing Elementor kit, not a new one
    primary        Roboto, weight 600
    secondary      Roboto Slab, weight 400
    recommendation Roboto 600. It is the kit's primary and already loads; a slab
                   serif reads as decorative at small sizes.

  COLOUR — from the page-level brand palette actually in use
    #1C244B   darkest navy, recommended for the wordmark on light ground
    #324A6D   mid navy
    #467FF7   accent blue, recommended for a single accent word if desired
    NOTE: the kit's own system_colors are Elementor DEFAULTS (#6EC1E4, #54595F,
    #7A7A7A, #61CE70) and are NOT the brand palette. Do not draw from them.

  HEADER PLACEMENT
    position       header left, replacing the empty site_logo slot
    size           desktop 22-24px, tablet 20px, mobile 18px
    weight         600
    letter-spacing 0 to -0.01em
    link           to /
    alt/aria       the wordmark is text, so it needs no alt attribute; ensure it
                   is marked up as text and not as an image

  FAVICON
    form           a single letter "C" in Roboto 600, white on #1C244B, square
    sizes          512x512 master; WordPress derives 270, 192, 180, 32, 16
    file           to be produced at implementation, NOT sourced and NOT generated
                   from an image model
    replaces       attachment 177, which is AI-generated (see §3)
```

---

## 3. Removals directed by D27.1

None applied. `camden-concreting-import.xml` is immutable; these are post-import steps.

```text
  attachment 177   REMOVE as site icon. AI-generated (ChatGPT), currently the favicon.
                   Evidence: its metadata carries WordPress-generated site_icon-270,
                   site_icon-192 and site_icon-180 variants.
  attachment 272   REMOVE per D24. AI-generated, live on 14 pages.
  attachment 159   leave unreferenced. Orphaned AI-generated original of 177.
  attachments      leave unreferenced. The source business's favicon symbol.
  306, 307, 422
  NOT DELETED      none of the five is deleted from the immutable WXR.
```

---

## 4. If the Astra export shows a header logo reference (D27.4)

The header logo assignment lives in Astra theme mods and cannot be read today. When the export arrives:

```text
  CHECK    does any of custom_logo / transparent_header_logo / sticky_header_logo
           reference attachment 159, 177, 272, 306, 307 or 422?
  IF YES   REPORT IT. Do not act. D27.4 is explicit.
  IF NO    the header currently has no logo, and the wordmark fills an empty slot
           rather than replacing anything.
```

`scripts/22-astra-audit.py` already requires the `site-identity` mod group, so a partial export missing
the logo assignment fails intake before this question can be answered wrongly.

---

## 5. Status

```text
  specified            yes
  implemented          NO - and must not be until the Astra export exists
  blocked by           identity question (which trading name), Astra export
  owner decisions      1. Is "CoreX Concreters Camden" the name?
                       2. Confirm E&T Co is removed from the Elementor kit site_name.
                       3. Approve the wordmark treatment above.
```
