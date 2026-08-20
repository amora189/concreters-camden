# GATE 29 — authoritative staging plan

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.29; `RUN-BLOCK-01.md` §A D1, §C.7.

---

## THIS PLAN DOES NOT RUN YET

```text
  Gate 28 verdict          NO-GO
  therefore                nothing below executes
  containers started       0
  imports performed        0
  deployments              0
```

The plan does not run until Gate 28 returns GO. Gate 28 currently returns NO-GO on four gates, two of
which (media, Astra) are owner-supplied inputs that no amount of work here can clear.

---

## 1. Scaffolding created

```text
  staging-authoritative/docker-compose.yml              PHP 8.3, all versions pinned
  staging-authoritative/apache-host-guard.conf          unexpected-host blocking
  staging-authoritative/mu-plugins/00-enforce-noindex.php   enforced global noindex
  staging-authoritative/scripts/checkpoint.sh           create / restore / verify / list
  staging-authoritative/scripts/import-media-local.sh   local-only media importer
  staging-authoritative/{checkpoints,uploads,import,secrets}/   working directories

  bash -n scripts/checkpoint.sh            SYNTAX OK
  bash -n scripts/import-media-local.sh    SYNTAX OK
```

Clearly separated from the disposable `staging/`. Different container names, different ports, different
volumes.

```text
  DISPOSABLE staging/            AUTHORITATIVE staging-authoritative/
  PHP 8.4                        PHP 8.3          (§4.29.1 — 8.4 logs an Elementor deprecation)
  port 127.0.0.1:8088            port 127.0.0.1:8099
  camden-wp / camden-db          camden-auth-wp / camden-auth-db
  smoke tests only               the real import target
```

### Pinned versions

```text
  wordpress:6.8.1-php8.3-apache
  mariadb:11.4.5
  wordpress:cli-2.11-php8.3
```

No floating tags, no `:latest`.

### Containment

```text
  binding                  127.0.0.1 only, both web and database
  unexpected-host blocking Apache rejects any Host header other than 127.0.0.1 / localhost,
                           including the production hostname
  enforced noindex         must-use plugin: blog_public forced 0, wp_robots forced
                           noindex/nofollow/noarchive/nosnippet, X-Robots-Tag header,
                           robots.txt Disallow /, sitemaps disabled
  remote media fetching    WP_HTTP_BLOCK_EXTERNAL true, plus a pre_http_request filter
                           that rejects every non-local host
  file editing             DISALLOW_FILE_EDIT true
```

The noindex is a **must-use plugin**, so it cannot be deactivated from wp-admin. Standing rule 4 says WXR
`publish` status is not launch approval; this makes that structurally true on staging.

---

## 2. The command sequence, with a rollback point after every mutating step

Read `CP:` as a rollback point. Every mutating step has one behind it.

```text
STEP  0   PRECONDITION — Gate 28 must return GO
          bash scripts/28-preflight.sh
          Refuse to continue on NO-GO. Currently returns NO-GO.

STEP  1   Bring up a clean stack
          docker compose -f staging-authoritative/docker-compose.yml up -d db wordpress
          VERIFY  curl -sI http://127.0.0.1:8099/ | head -1        -> 200
          VERIFY  curl -s http://127.0.0.1:8099/robots.txt         -> "Disallow: /"
          VERIFY  curl -sI http://127.0.0.1:8099/ | grep X-Robots  -> noindex present
          VERIFY  curl -sI -H 'Host: concreterscamden.com.au' http://127.0.0.1:8099/ -> 403
  CP: 01-clean-wordpress          ./scripts/checkpoint.sh create 01-clean-wordpress

STEP  2   Install and pin the theme and plugins
          wp theme install astra --version=4.11.7 --activate
          wp plugin install elementor --version=3.30.2 --activate
          wp plugin install seo-by-rank-math --version=1.0.235 --activate
          wp plugin install wordpress-importer --version=0.8.3 --activate
          wp plugin install fluentform --version=6.0.4 --activate
          VERIFY  wp theme list --status=active     -> astra
          VERIFY  wp plugin list --status=active    -> the four above
          NOTE    versions are the pinned set to confirm against the source install
                  before running. If any differs, STOP and ask; do not substitute.
  CP: 02-theme-and-plugins        ./scripts/checkpoint.sh create 02-theme-and-plugins

STEP  3   ASTRA CUSTOMIZER IMPORT — discrete step, own verification, BEFORE content
          python scripts/22-astra-audit.py            (must exit 0)
          wp import-customizer /import/astra/<export-file>
          VERIFY  wp option get theme_mods_astra --format=json | jq 'keys | length'
          VERIFY  all seven mod groups present: site-identity, colours, typography,
                  layout, header, footer, buttons
          VERIFY  wp eval 'echo get_theme_mod("custom_logo");'   -> non-empty
          BLOCKED currently: no Astra export exists. This step cannot run.
  CP: 03-astra-imported           ./scripts/checkpoint.sh create 03-astra-imported

STEP  4   MEDIA IMPORT — local-only, exact filenames, requested IDs
          python scripts/22-media-audit.py            (must exit 0)
          ./scripts/import-media-local.sh
          VERIFY  immutable intake baseline remains 83 records
          VERIFY  81 active attachments exist; 280 and 1067 are excluded as UNUSABLE
          VERIFY  zero filenames show -1 / -scaled / -e<timestamp> drift
          VERIFY  every active requested attachment ID matches the image map plus
                  build/45-media-remediation.csv
          VERIFY  checksums match reports/22-reencode-manifest.csv
  CP: 04-media-imported           ./scripts/checkpoint.sh create 04-media-imported

STEP  5   MAIN CONTENT IMPORT
          wp import /import/camden-concreting-import.xml --authors=create
          VERIFY  wp post list --post_type=page --format=count   -> 156
          VERIFY  21 publish / 135 draft
          VERIFY  all 156 post IDs match build/stage9-page-manifest.json
          VERIFY  65 nav_menu_item, 1 elementor_library, 1 custom_css
  CP: 05-main-imported            ./scripts/checkpoint.sh create 05-main-imported

STEP 5A   BAND B + D32 POST-IMPORT TRANSFORMATION — before any page verification
          ./scripts/apply-band-b-remediation.sh
          VERIFY  15 local-work modules removed
          VERIFY  106 surviving GENERIC references renamed + subject-only alt
          VERIFY  28 UNUSABLE references removed; zero remain for IDs 280 / 1067
          VERIFY  4 GENERIC references left with removed evidential modules
          VERIFY  zero GENERIC target remains in a local-work-card
  CP: 05a-band-b-applied          ./scripts/checkpoint.sh create 05a-band-b-applied

STEP  6   VERIFY the main import against the manifest
          python scripts/28-gates.py                  (re-run against the live DB)
          VERIFY  1,014 surviving image references resolve
          VERIFY  98 background_image references resolve   (see §5)
          VERIFY  zero unresolved attachment references
  CP: 06-main-verified            ./scripts/checkpoint.sh create 06-main-verified

STEP  7   SUPPLEMENTARY CALCULATOR IMPORT
          wp import /import/camden-calculator-import.xml --authors=skip
          VERIFY  157 pages total
          VERIFY  the calculator is draft + noindex
          VERIFY  its post_id is above 1567 and collides with nothing
          BLOCKED currently: camden-calculator-import.xml does not exist (Stage 31).
  CP: 07-calculator-imported      ./scripts/checkpoint.sh create 07-calculator-imported

STEP  8   VERIFY the calculator
          reports/31-delta.md — the bounded delta pass required by RUN-BLOCK-01 §A D1
  CP: 08-calculator-verified      ./scripts/checkpoint.sh create 08-calculator-verified

STEP  9   POST-IMPORT — search-replace, DRY RUN FIRST
          wp search-replace 'https://bestconcretersmelbourne.com.au' \
                            'https://concreterscamden.com.au' --dry-run --report-changed-only
          REVIEW the dry-run output in full before running it for real.
          wp search-replace 'https://bestconcretersmelbourne.com.au' \
                            'https://concreterscamden.com.au' --report-changed-only
          VERIFY  Victorian blocklist scan returns zero across the live DB
  CP: 09-urls-rewritten           ./scripts/checkpoint.sh create 09-urls-rewritten

STEP 10   POST-IMPORT — Elementor maintenance (CODEX-BUILD.md Stage 10)
          wp post meta delete --all _elementor_element_cache
          wp elementor flush-css
          wp elementor update db
          wp elementor library sync
          VERIFY  a sampled page renders with no Elementor deprecation in the log
  CP: 10-elementor-regenerated    ./scripts/checkpoint.sh create 10-elementor-regenerated
```

---

## 3. The settings that do not travel in a WXR

§4.29.4. Each is an explicit step with its own verification check. A WXR carries posts, pages,
attachments and menu items — none of the following.

```text
STEP 11   STATIC HOMEPAGE ASSIGNMENT
          wp option update show_on_front page
          wp option update page_on_front <imported homepage post_id>
          VERIFY  curl -s http://127.0.0.1:8099/ | grep -o '<title>[^<]*'
                  resolves to the imported homepage, NOT a posts archive
          VERIFY  wp eval 'echo get_option("page_on_front");'  equals the manifest homepage ID
          FAILURE MODE if skipped: the front page serves a blog archive and every
          internal link from the homepage 404s.
  CP: 11-homepage-assigned        ./scripts/checkpoint.sh create 11-homepage-assigned

STEP 12   PERMALINKS
          wp rewrite structure '/%postname%/' --hard
          wp rewrite flush --hard
          VERIFY  curl -sI http://127.0.0.1:8099/about/ | head -1          -> 200
          VERIFY  trailing slash is present on the served URL
          VERIFY  canonical tag on a sampled page matches the served URL exactly
          VERIFY  curl -sI http://127.0.0.1:8099/about  (no slash) -> 301 to /about/
          FAILURE MODE if skipped: every page serves at ?page_id=N and every
          canonical disagrees with every internal link.
  CP: 12-permalinks-flushed       ./scripts/checkpoint.sh create 12-permalinks-flushed

STEP 13   MENU LOCATION ASSIGNMENT — against the Wave 1 JSON, not the full set
          Assign all five menus to their Astra theme locations, but populate them
          from build/27-wave1-menus.json (27 items), NOT the 65 imported items.
          wp menu location assign <menu> primary
          ...
          VERIFY  python scripts/27-menu-lint.py            -> exit 0
          VERIFY  no rendered menu item points at a draft or noindex page
          SPECIAL: 'Footer Areas' and 'Footer Blogs' retain ZERO items for Wave 1.
                   UNREGISTER those two locations rather than assigning an empty
                   menu — an Astra footer widget bound to an empty menu renders an
                   empty region rather than nothing.
  CP: 13-menus-assigned           ./scripts/checkpoint.sh create 13-menus-assigned


STEP 14   CORRECT THE SITE IDENTITY (DECISION-06 D30.1)
          The WXR is NOT edited. This is the only place the source business name
          can be removed from what a visitor sees.

          wp option update blogname '<approved trading name>'
          wp option update blogdescription '<approved tagline>'
          wp eval  update the Elementor kit site_name and site_description

          VERIFY  wp option get blogname            -> contains no "E&T"
          VERIFY  wp option get blogdescription     -> no "E&T", no "Camden based"
          VERIFY  kit site_name / site_description  -> neither term
          VERIFY  curl the homepage; <title> and rendered tagline clean
          VERIFY  bash scripts/28-preflight.sh gate 13 passes

          CURRENT VALUES IN THE ARTIFACT
            site_name         "E&T Co Concreters Camden"   <- another business
            site_description  "Camden based Concrete Company Site"  <- location claim,
                              unsupportable given Pakenham fulfilment (D32)

          BLOCKED BY  the identity question. The approved trading name is unknown;
                      "CoreX Concreters Camden" has no verified legal entity either.
  CP: 14-site-identity-corrected   ./scripts/checkpoint.sh create 14-site-identity-corrected
```

---

## 4. Post-import guide-side link edits (§4.31.6)

The four LGA crossing guides live inside the never-modify main file, so their links to the calculator are
**post-import edits**. Listed here with exact target page IDs and anchor text.

```text
  BLOCKED: the calculator has no slug or post_id until Stage 31 §4.31.2 approval.
  The edits cannot be specified with exact targets until then.

  GUIDE PAGE                                    POST_ID   ANCHOR TEXT (descriptive, non-exact-match)
  camden-council-driveway-crossing              1524      "work out what your crossing needs"
  liverpool-council-vehicle-crossing            1521      "check the requirements for your lot"
  campbelltown-council-driveway-crossing        (per manifest)  "see what applies to your driveway"
  wollondilly-council-driveway-crossing         (per manifest)  "check your crossing requirements"

  target: the calculator page, slug pending Stage 31 approval

  ORPHAN DECLARATION: because every inbound link is a post-import edit, the
  calculator is an ORPHAN at the moment of import. This is declared explicitly
  here rather than letting the orphan check fail silently or be waived.
```

---

## 5. Known issues carried into this plan

```text
  1  The 98 background_image references are outside the recorded 1,085 figure.
     Step 6 verifies them anyway. If the owner decides the recorded figure stands,
     that verification becomes advisory — but it is NOT advisory today.

  2  reencode-images.sh at repo root does not parse. Use scripts/22-reencode-images.sh.
     ImageMagick must be installed before step 4 can produce inputs.

  3  Plugin and theme versions in step 2 are a proposal, not a confirmed match to
     the source install. Confirm them against the source before running; a version
     mismatch on Elementor is how layouts silently shift.

  4  20 images are Victorian photographs renamed to specific NSW places (Gate 24).
     They will import and render. Nothing in this plan detects that, because the
     files are valid and correctly named. This is an owner decision, not a
     technical gate.
```

---

## 6. `CONTEXT.md` update and diff

```text
  Latest completed stage    28 -> 29
  Authoritative staging     none -> scaffolding created, PHP 8.3, pinned, not started
  Rollback points defined   13
  Containers started        0
  Imports performed         0
  Index-ready               0 of 157 — UNCHANGED
  Launch gate               NO-GO — UNCHANGED
```

---

## 7. Hash table

```text
  camden-concreting-import.xml                          A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884  MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15  MATCH
  build/stage9-page-manifest.json                       578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42  MATCH
  build/stage8-image-map.json                           0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF  MATCH
  reports/08-image-rename-map.csv                       43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8  MATCH
  CODEX-BUILD-2.1.md                                    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C  MATCH

  6 of 6 MATCH.
```

---

## GATE 29 RESULT

```text
  staging-authoritative/ created, separated from disposable staging/   PASS
  docker-compose pinned to PHP 8.3, all versions explicit              PASS
  loopback-only binding                                                PASS
  unexpected-host blocking                                             PASS
  enforced global noindex (must-use plugin, cannot be disabled)        PASS
  clean checkpoint creation script                                     PASS
  DB + uploads rollback script                                         PASS
  local-only media importer, remote fetching disabled                  PASS
  command sequence printed                                             PASS — 13 steps
  rollback point after every mutating step                             PASS — 13 points
  Astra import as a discrete step before content                       PASS — step 3
  static homepage assignment with verification                         PASS — step 11
  permalinks flushed, trailing slash and canonical verified            PASS — step 12
  menu locations assigned against the Wave 1 JSON                      PASS — step 13
  post-import guide-side link edits listed                             PARTIAL — targets pending Stage 31
  orphan declaration made explicitly                                   PASS
  no containers started                                                PASS — 0
  nothing imported                                                     PASS — 0

  GATE 29: PASS. The plan states plainly that it does not run until Gate 28
  returns GO, and Gate 28 returns NO-GO.
```
