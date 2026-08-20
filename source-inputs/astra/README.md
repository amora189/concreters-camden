# `source-inputs/astra/` — the Astra Customizer / theme-mods export

**Status: EMPTY. This is a P0 blocker on the authoritative staging import.**

## What must be dropped in here

One export of the Astra theme's Customizer settings from the source WordPress install,
in any of these forms:

```text
  1. WordPress 'Customizer Export/Import' plugin   ->  *.dat   (PHP-serialised, 'mods' key)
  2. theme_mods_astra option dump                  ->  *.json
  3. Astra > Import/Export Settings                ->  *.json  (astra-settings blob)
```

## Why a WXR is not enough

A WXR carries posts, pages, attachments and menu items. It does **not** carry theme mods.
Everything below lives outside the WXR and will be lost unless this export is supplied:

```text
  site-identity   custom_logo, site_icon, title/tagline display
  colours         theme-color, link-color, text-color, heading-base-color
  typography      body font family and size, H1-H6 families and sizes
  layout          site-content-width, site-layout, sidebar layout
  header          header-main layout and width, transparent header
  footer          footer-layout, footer-sml-layout, footer-adv
  buttons         button colour, background, radius, padding
```

The audit fails if ANY of those seven groups is absent, so a partial export is caught
here rather than after import.

## Verification

```
python scripts/22-astra-audit.py
```

Fail-closed. Exits non-zero while the directory is empty, while no file parses as a
genuine Astra export, or while any required mod group is missing.

## Import order

Per `CODEX-BUILD-2.1.md` §4.29.3 the Astra Customizer import is a **discrete step with its
own verification, performed BEFORE content**. Do not fold it into the WXR import.

