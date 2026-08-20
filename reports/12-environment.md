# Stage 12 — Protected local staging environment

Environment created: 15 August 2026 (Australia/Sydney)

## Classification

**Disposable technical smoke test — not authoritative staging.**

The local environment exists to test post IDs, WXR import behaviour, hierarchy, metadata, routes, WordPress configuration, and basic rendering. It cannot receive visual or launch approval because the original 83 image files and Astra Customizer export are absent.

## URL and isolation

- URL: `http://127.0.0.1:8088/`
- Docker publishes Apache only on loopback: `127.0.0.1:8088->80/tcp`.
- The database has no published host port.
- WordPress `blog_public`: `0`.
- Every Apache response carries `X-Robots-Tag: noindex, nofollow, noarchive`.
- Physical `/robots.txt` returns HTTP 200 with `User-agent: *` and `Disallow: /`.
- A must-use plugin repeats the robots directives at WordPress level.
- An unexpected `Host` header returns HTTP 403.
- WordPress environment type is `staging`.
- No public staging URL, live site, DNS, Search Console, sitemap, or indexing setting was changed.

## Versions

| Component | Version | State |
|---|---:|---|
| Docker Engine | 29.7.2 | Local engine |
| Docker Compose | 5.3.1 | Local orchestration |
| WordPress | 7.0.4 | Installed |
| PHP | 8.4.24 | Installed; CLI and Apache module |
| Apache | 2.4.68 | Local web server |
| MariaDB server | 10.11.18 | Healthy, isolated container |
| WP-CLI | 2.12.0 | Available through disposable tool container |
| Astra | 4.13.9 | Active theme; default settings only |
| Elementor | 4.2.2 | Active; matches required 4.2.x atomic generation |
| Rank Math SEO | 1.0.276 | Active |
| WordPress Importer | 0.9.5 | Active |
| Fluent Forms | 6.2.12 | Active for shortcode compatibility testing |

The fixed package versions were obtained from official WordPress.org release/download endpoints on 15 August 2026. Elementor's official listing identified 4.2.2 as current and recommended PHP 8.3. The local Debian base supplies PHP 8.4.24, which causes a logged Elementor deprecation notice in `atomic-global-styles.php:410`. Errors are not displayed publicly, but PHP 8.4 is a smoke-test caveat; authoritative staging should use PHP 8.3 or a confirmed Elementor patch level before visual approval.

## Package integrity

All cached release archives passed ZIP/TAR structure checks.

| Package | SHA-256 |
|---|---|
| WordPress 7.0.4 | `26B99ABFC65427FBAB52B24315539B944DCEF1467899A5256B6C1DE2C4AE7E46` |
| WP-CLI | `CE34DDD838F7351D6759068D09793F26755463B4A4610A5A5C0A97B68220D85C` |
| Astra 4.13.9 | `5ABB56A986629FBF5DA979026D4A60C5EBF54CA411D96F693023F119032367CB` |
| Elementor 4.2.2 | `4638F58C4CC476BC714941C34679E9284493A2FE7233D7923E7E834D42D653DB` |
| Rank Math 1.0.276 | `5252B6E233FE6FE73E69B57FBB039B50140BB5F12438DA0ADA1C2A973A99F83D` |
| WordPress Importer 0.9.5 | `0D60E58269D8DADF938442E073456D7D1F0CD02AC5C75BD77409ED67B79AD699` |
| Fluent Forms 6.2.12 | `37E2CED9B0C95B66A1104317B70E9826120E1AFB12073AB20189531C8117013D` |

## Configuration

- Site language: English (Australia), `en_AU`.
- Timezone: `Australia/Sydney`.
- PHP memory limit: 512 MB.
- PHP upload and POST limit: 64 MB.
- WordPress debug logging: enabled.
- Public PHP/WordPress error display: disabled.
- Direct HTTP access to `wp-content/debug.log`: denied with HTTP 403 and the global `X-Robots-Tag` header.
- Permalink structure: `/%postname%/`; Apache rewrite rules are present and a published baseline page resolves at its post-name route.
- WordPress automatic core updates: disabled for reproducible smoke testing.
- File editor: disabled.
- No SMTP, API, production, owner, or hosting secret was added.
- Local credentials in the Compose definition are explicitly disposable and are not valid on any external system.

Fluent Forms activation created two demonstration forms in its own table: form ID 1 (`Contact Form Demo`) and form ID 2 (`Subscription Form`). Form ID 3 remains absent. It was not invented because its fields, recipient, consent wording, and notification behaviour have not been approved.

## Clean rollback checkpoint

Created before Astra or any plugin activation:

- `staging/backups/00-clean-before-plugins/database.sql`
  - Size: 91,229 bytes
  - SHA-256: `26B7C36697813E035439CD07AFF60A9E8844B92BD9D25138EDCDAD8FDEB73BF2`
- `staging/backups/00-clean-before-plugins/uploads.tar.gz`
  - Size: 151 bytes
  - SHA-256: `B97F16996A8D5D995783AD477F305D397FAEC57837A0CD90EBF240319FFBF374`

The database and WordPress named volumes are `camden_concreting_smoke_database` and `camden_concreting_smoke_wordpress`.

## Browser verification

The fresh WordPress installer was checked with a real Chromium session:

- HTTP load: pass.
- Meaningful WordPress content: pass.
- Error overlay: none.
- Captured console errors: none.
- Interactive language selector and Continue control: present.
- Screenshot: `staging/screenshots/12-wordpress-install.png`.

A later protected-baseline browser check also rendered `/sample-page/` without console or page errors; its screenshot is `staging/screenshots/20-rolled-back-baseline.png`. The baseline draft `/privacy-policy/` and a random nonexistent route both return HTTP 404. This is environment-level evidence only.

This verifies the local server/browser path only. It is not a Camden design approval.

## Stage decision

- Protected disposable environment: **PASS**.
- Clean pre-plugin rollback point: **PASS**.
- Authoritative staging environment: **FAIL/BLOCKED** by missing Astra export, missing media, and PHP 8.4 smoke-test caveat.
- Live deployment/indexing: **not authorised**.

STAGE 12: DISPOSABLE ENVIRONMENT READY
