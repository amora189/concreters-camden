# Stage 19 — Rank Math schema validation status

Audit date: 15 August 2026 (Australia/Sydney)

## Current evidence

- The completed WXR contains zero `rank_math_schema_*` postmeta rows, as required by Stage 9.
- The disposable import also produced zero such rows before rollback.
- Legal/operating business identity, phone ownership/routing, ABN, licence, insurance, and a legitimate staffed address are not verified.
- Form/contact presentation is not approved.
- The authoritative Camden pages are not currently imported into staging.

## Decision

Schema was **not rebuilt**. Rebuilding it now would require inventing or prematurely approving identity, telephone, address, and service facts.

No page is schema-approved. In particular:

- No `LocalBusiness` or `GeneralContractor` node is authorised.
- No suburb-specific LocalBusiness entity is authorised.
- No Review or AggregateRating data is authorised.
- No FAQ schema is authorised until the exact visible questions and answers can be checked on the authoritative render.
- No graph may reference a missing address-dependent entity.

Once owner evidence is supplied, the authoritative staging import passes, and visible content matches that evidence, build and validate one JSON-LD `@graph` per representative page type. Use stable Organization/WebSite IDs; add LocalBusiness/GeneralContractor only on `/` and `/contact/` if a legitimate staffed address exists; otherwise use Organization/Service relationships without a nonexistent LocalBusiness ID. Suburb pages use Service plus `areaServed`.

STAGE 19: BLOCKED — BUSINESS IDENTITY AND AUTHORITATIVE RENDER MISSING
