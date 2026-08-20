# Stage 36 — source business name sweep (D30)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-06-resolvable-items.md` §D30.
Data: `reports/36-source-name-sweep.csv` (783 rows, classified).

---

## 1. What actually reaches a rendered site

D30 asks for every hit. Reporting 783 raw hits, or even the 136 the pattern called "brand leakage", would
overstate it. Nearly all are **provenance records doing their job** — a rename map is supposed to record
the original filename.

**Two values reach a live page. Both are in the immutable WXR's Elementor kit.**

```text
  HIT 1 — the site name
    location   elementor_library "Default Kit" > _elementor_page_settings > site_name
    value      "E&T Co Concreters Camden"
    reaches    the browser title bar, the WordPress site title, and anywhere the
               theme prints the site name
    fault      declares another business's trading name

  HIT 2 — the tagline
    location   same settings blob > site_description
    value      "Camden based Concrete Company Site"
    reaches    the tagline wherever Astra renders it
    fault      a LOCATION claim. Per DECISION-06 D32, fulfilment is Pakenham and no
               Camden pour has been completed. "Camden based" is not supportable.
```

Neither can be fixed in the artifact. Both are post-import steps.

---

## 2. Full classification of the sweep

```text
  CLASSIFICATION                        HITS   REACHES A LIVE PAGE?
  our-own-reporting-of-the-issue         538   no - this session's reports and decisions
  source-wxr-filename-reference          109   no - scripts and reports naming the source WXR file
  BRAND LEAKAGE - filename                58   no - see below
  BRAND LEAKAGE - name in data            78   no - see below
  TOTAL                                  783
```

### Why the 136 "brand leakage" hits do not reach a page

```text
  build/stage8-image-map.json          34   records old_filename and the ORIGINAL attachment
                                            title "E&T CO Concreters Logo". This is the
                                            provenance record. Removing it would destroy the
                                            audit trail that caught the problem.
  reports/00-inventory.md              27   Stage 0 inventory of the SOURCE site. Historical.
  camden-site-structure-and-silo.md    13   names the source site in its own header. Correct.
  build/stage7-*.json                  20   build intermediates holding source URLs
  reports/08-image-rename-map.csv       7   the rename map. Its whole purpose is old -> new.
  reports/14/22/24-*.csv               20   audit outputs quoting old filenames
  codex-clone-prompt.md                 5   the find/replace contract. Naming the term to
                                            replace is how it gets replaced.
  build/global-replace.json             4   the replacement rule itself
  oran-park-gold-standard.md            3   names the source template
  lib/stage8.py                         1   a rename rule matching "e-t-co" to route logos
                                            to corex-concreters-camden-logo
```

**None of these is a defect.** They are the mechanism by which the source name was removed from the site,
and the record of what was removed. Deleting them would destroy provenance and break the audit trail.

The attachment titles in the main WXR were correctly renamed: attachment 159's title in the artifact is
"Chatgpt image jul 6 2026 01 52 19 pm camden", not "E&T CO Concreters Logo". The old title survives only
in the map.

---

## 3. Post-import runbook step (D30.1)

Added to `reports/29-staging-plan.md` as a discrete verified step.

```text
STEP 14   CORRECT THE SITE IDENTITY  -  the WXR is NOT edited

  wp option update blogname '<approved trading name>'
  wp option update blogdescription '<approved tagline>'
  wp eval '$k = get_option("elementor_active_kit"); ...'   update kit site_name
                                                          and site_description

  VERIFY  wp option get blogname          -> no "E&T"
  VERIFY  wp option get blogdescription   -> no "E&T", no "Camden based"
  VERIFY  kit site_name and site_description contain neither
  VERIFY  curl the homepage; <title> and any rendered tagline contain neither

  BLOCKED BY  the identity question. The approved trading name is not known:
              "CoreX Concreters Camden" has no verified legal entity behind it.
              The tagline cannot say "Camden based" given Pakenham fulfilment.
```

---

## 4. Preflight assertion (D30.2)

Added to `scripts/28-gates.py` as gate 13 and wired into `scripts/28-preflight.sh`.

```text
  GATE 13  source business name
  asserts  zero occurrences of "E&T", "E&T Co", "e_t_co", "eandtco" or
           "E&T Co Concreters" in:
             - the Elementor kit settings blob
             - site_name and site_description
             - any rendered page body
           in BOTH the main and supplementary WXR files
  status   currently FAILS on the kit site_name, which is correct - the value is
           in the immutable artifact and can only be corrected at import
```

Provenance and audit files are explicitly out of scope for the gate. It scans artifacts destined for the
site, not the records of how they were made.

---

## 5. D30.4 — the note for `CONTEXT.md`

Recorded, in the words D30 asks for:

> Correcting `site_name` replaces an **incorrect** claim with an **unverified** one. "CoreX Concreters
> Camden" has no verified legal entity behind it either. This is an improvement, not a resolution, and
> the identity blocker stands.

The tagline is worse than unverified. "Camden based Concrete Company Site" is a positive location claim,
and D32 establishes that fulfilment is Pakenham. It cannot be corrected to a different location claim
without one that is true.
