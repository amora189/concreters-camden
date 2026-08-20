# Environment requirements

Authority: `DECISION-07-image-sourcing-tooling.md` §D34.4 — record tooling as a documented environment
requirement, not as an ad-hoc install.

This file lists what must be present **on the host** and **in the container**, and which build phase each
requirement gates. It is the answer to "why did that step fail" before it is asked.

---

## Host requirements

```text
  REQUIREMENT        VERSION / STATE            GATES              CURRENT STATE
  Python             3.11+                      all script phases  3.11 present
  bash               MSYS / Git Bash            preflight, drivers present
  Docker Desktop     engine running             Phase B step 5     NOT RUNNING
  ImageMagick        'magick' on PATH           Phase B step 3     NOT INSTALLED
  WSL                for the image finder       Phase F            launcher present
  SERPAPI_KEY        env var, paid key          Phase F            NOT SET in login shell
```

### ImageMagick — a Phase B precondition, not a convenience

```text
  used by     scripts/22-reencode-images.sh
  purpose     strip EXIF, resize 98%, quality 82
  why it gates the phase:
              the root-level reencode-images.sh has never parsed, so NO image in
              this build has ever been stripped. Without a working driver, EXIF -
              including GPS coordinates from Melbourne job sites and owner/device
              metadata - imports intact and publishes to a live website.
  substitute  NONE. The 98%/82/strip parameters are the footprint contract; another
              encoder is not equivalent.
  verified by scripts/22-media-audit.py EXIF assertion, itself proven against a
              known-dirty file by tests/test_exif_assertion.py
```

### SerpApi — Phase F only

```text
  location    ~/camden-images/ in WSL
                find_images.py    5,802 bytes
                .venv/            serpapi installed
                reports/
  key         SERPAPI_KEY, not set in the WSL login shell as at 18 Aug 2026
  status      NOT copied into the repo. D34.1 requires that copy WHEN PHASE F RUNS.
              Phase F is currently blocked, so the tool stays where it is and is
              recorded here rather than imported early.
  constraint  paid API. Do not spend credits until Phase F is unblocked and the
              spec CSV has been regenerated (D34.2).
```

---

## Container requirements — authoritative staging

Pinned in `staging-authoritative/docker-compose.yml`. No floating tags, no `:latest`.

```text
  wordpress:6.8.1-php8.3-apache      PHP 8.3, NOT 8.4 - 8.4 logs an Elementor deprecation
  mariadb:11.4.5
  wordpress:cli-2.11-php8.3
```

Theme and plugin versions in `reports/29-staging-plan.md` step 2 are a **proposal**, not a confirmed
match to the source install. Confirm each against the source before running; a version mismatch on
Elementor is how layouts silently shift.

---

## Environment checks

```text
  scripts/37-preconditions.py     phase-by-phase precondition gate, re-runnable
  tests/test_exif_assertion.py    proves the EXIF assertion fires before it is trusted
  scripts/21-encoding-canary.py   UTF-8 fidelity, preflight gate 1
```

Run `python scripts/37-preconditions.py` each time an owner input arrives. It prints the precondition
table and exits non-zero while every phase is blocked.

---

## What is deliberately absent

```text
  no Selenium, no headless browser, no image scraper
              D33 prohibits them. SerpApi with licenses=fmc is the only permitted
              search-engine-adjacent discovery mechanism, and it is a DISCOVERY
              filter, not a licence determination.
  no remote media fetching in staging
              WP_HTTP_BLOCK_EXTERNAL true, plus a pre_http_request filter rejecting
              every non-local host. Standing rule 3.
```
