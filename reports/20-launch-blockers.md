# Stage 20 — Launch blockers

Audit date: 15 August 2026 (Australia/Sydney)

Launch and indexing decision: **NO-GO**. Current index-ready pages: **0 of 156**.

## Owner action

### P0 — required before authoritative staging import/visual approval

- Supply the original 83 image binaries that correspond to the Stage 8 image map.
- Supply the separate Astra Customizer export/theme-mods evidence.

### P1 — required before page approval/indexing

- Confirm the legal/operating business identity and relationship to “CoreX Concreters Camden”.
- Supply ABN, licence, insurance, operator profile, and legitimate staffed-address evidence where each is intended to be shown.
- Prove ownership and current call routing for `03 4517 6915`; otherwise supply the correct number for global replacement.
- Approve the Fluent Forms ID 3 fields, verified recipient email, consent/privacy wording or basis, and whether the forms on About and Gallery remain.
- Supply real quote evidence for price/range/turnaround claims; do not supply estimates created for SEO copy.
- Supply review text, reviewer identity, publication permission, and any necessary source record.
- Supply verified project photography with suburb, service, completion date, and permission to publish.
- Approve pages individually by publication wave; do not approve by page-count target.

## Technical action

### P0 — import integrity

- Rebuild authoritative staging on PHP 8.3 or a confirmed Elementor-compatible patch level.
- Start from the clean database/uploads checkpoint and repeat the occupied-ID audit.
- Keep prepared source media outside the final upload path and use a local-only audited import adapter so WordPress Importer creates all 83 requested attachment IDs without network downloading or filename suffixing.
- Remove/isolate the backed-up local Elementor kit 4 before import; verify WXR kit 6 and deliberately make it active only after import.
- Require exact file checksum/MIME/dimension/name-to-ID and all 1,085 Elementor reference checks to pass; rollback on any mismatch.

### P1 — configuration and QA

- Import and verify Astra Customizer settings before visual approval.
- Run production/old-domain search-replace dry runs, apply only genuine replacements, clear safe cache metadata, regenerate Elementor data, sync the library, and clear all cache layers.
- Configure static homepage, canonical/URL behaviour, and reviewed Wave 1-safe menus with no guide links.
- Build/import Fluent Forms form 3, configure SMTP outside the repository, and prove notification/Reply-To delivery.
- Rebuild Rank Math schema only after identity/contact evidence matches visible content.
- Repeat logged-out crawl, desktop/mobile visual QA, accessibility, mixed-content, console, Lighthouse, caching, backup/restore, security/update, and analytics-readiness checks.

## Authoritative verification

- Resolve all 163 registered markers from `reports/placeholders.md`: 111 placeholders, 47 photo markers, and five verification markers.
- Verify the current council/estate statements identified by the five `VERIFY` records against current authoritative sources at publication time.
- Verify business registration/licensing/insurance and staffed-address claims against appropriate authoritative records and owner documents.
- Verify photo provenance and review permissions; media appearance or an old filename is not evidence of a Camden job.
- Verify phone ownership by a real call-routing/ownership test, not by recurrence in the WXR.
- Re-run `reports/18-page-readiness.csv` after each approved evidence replacement.

## Publication constraints still in force

- Wave 1 is a maximum candidate set, not automatic approval.
- Six Tier 1 suburbs and Gallery remain `noindex,follow` until their evidence gates pass.
- `/guides/` and its first approved guide batch must publish together; never publish the hub alone.
- The remaining guides, 54 suburbs, 35 intersections, and ten cost/comparison pages remain draft until individually ready.
- No page becomes indexable without explicit approval.

## Safest next action

Obtain the **83 original image binaries and the Astra Customizer export together**, place them in a clearly identified source-input directory, and rerun Stage 14 before another import attempt.

STAGE 20 LAUNCH GATE: NO-GO
