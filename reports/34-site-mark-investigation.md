# Stage 34 — is 159 or 177 the site mark? (D24)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-04-scope-reduction.md` §D24 — *"determine whether either is the site mark by
inspecting the Elementor kit and Astra theme mods, and report. Do not classify or act."*

**Reported. Not classified, not acted on.**

---

## ANSWER — 177 is the site icon, and it is AI-generated

```text
  attachment 177
  original filename   cropped-ChatGPT-Image-Jul-6-2026-07_59_41-PM.png
  current filename    cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177.png
  page references     0
  verdict             THIS IS THE SITE ICON (favicon)
```

### The evidence

`_wp_attachment_metadata` for attachment 177 contains WordPress-generated **`site_icon` size variants**:

```text
  site_icon-270   cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177-270x270.png
  site_icon-192   cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177-192x192.png
  site_icon-180   cropped-chatgpt-image-jul-6-2026-07-59-41-pm-camden-177-180x180.png
```

WordPress generates the `site_icon-270`, `site_icon-192` and `site_icon-180` intermediate sizes **only**
when an image is assigned as the Site Icon. Their presence is conclusive: 177 was the favicon on the
source install, and the attachment record carrying that assignment travels in the WXR.

So the site's favicon is a ChatGPT-generated image, renamed to assert Camden.

---

## Attachment 159 — not the site mark

```text
  attachment 159
  original filename   ChatGPT-Image-Jul-6-2026-01_52_19-PM.png
  page references     0
  site_icon sizes     none
  "id":159 refs       0
  verdict             AI-generated, unreferenced, NOT the site mark
```

It is the uncropped original from which 177 was cropped, retained as an orphan attachment.

---

## The Elementor kit carries no logo

```text
  elementor_library "Default Kit", _elementor_page_settings, site_logo:
      url:    ""            <- EMPTY
      id:     ""            <- EMPTY
      size:   ""
      alt:    "Concreters in Camden"
      source: "library"
```

The kit declares a `site_logo` slot with alt text already written, and **no image in it**.

---

## What the WXR cannot tell us

```text
  custom_logo occurrences in the WXR       0
  theme_mods occurrences                   0
  astra-settings occurrences               0
```

A WXR does not carry theme mods. The Astra Customizer export — the missing P0 input — is the only place
the header logo assignment lives. So:

```text
  FAVICON       determined: attachment 177, AI-generated. Evidence is in the WXR.
  HEADER LOGO   UNDETERMINABLE from available artifacts. The assignment lives in the
                Astra theme mods, which do not exist. Attachments 306, 307 and 422
                (the source business's favicon symbol) are used as plain image
                widgets in page content, but whether any is ALSO the theme header
                logo cannot be established until the Astra export arrives.
```

---

## What this means against D24, stated but not acted on

D24: *"If the logo is AI-generated it joins the three held favicon files under D18 — the site ships
without a mark rather than with a generated one asserting a brand identity that has no verified legal
entity behind it."*

The condition is met for the **favicon**. The header logo remains undetermined.

```text
  CURRENT SITE MARK INVENTORY
    favicon        attachment 177   AI-generated                    D24 condition MET
    header logo    unknown          pending the Astra export        undetermined
    in-page logo   306, 307, 422    source business's favicon       held under D18
    kit site_logo  empty slot       alt text written, no image      no image to hold
```

Every candidate for a site mark is either AI-generated, the source business's own symbol, or unknown.
**There is currently no honest mark available to ship.**

No action taken. This is a report.

---

## Owner question arising

```text
  The site favicon is a ChatGPT-generated image. The in-page logo files are the
  source Melbourne business's favicon symbol. The Elementor kit's logo slot is
  empty with alt text already written. The header logo assignment is unknown until
  the Astra export arrives.

  Commission or supply a distinct CoreX mark — favicon and logo — or confirm the
  site ships with no mark.
```
