# GATE 30 — fail-closed facts, schema and forms

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.30; `RUN-BLOCK-01.md` §A D2.
Artifacts: `data/verified-facts.yml`, `scripts/30-build-schema.py`, `build/30-schema-output.json`,
`reports/30-schema-refusals.md`, `reports/30-forms-spec.md`.

---

## GATE CONDITION — "the schema builder produces either nothing or minimal non-identity schema"

```text
  Organization emitted         NO
  LocalBusiness emitted        NO
  GeneralContractor emitted    NO
  AggregateRating emitted      NO
  Offer / price emitted        NO

  What IS emitted per page:    WebSite, WebPage, and on 105 pages a Service node
                               carrying only a name and serviceType.

  VERDICT: minimal non-identity schema. The builder asserts nothing about who the
  business is, where it is, what it charges, or what anyone thinks of it.
```

---

## 1. `data/verified-facts.yml`

Every business fact as an explicitly empty typed required field. Every field starts `verified: false`.

```text
  legal_entity      trading_name, legal_name, abn, entity_type
  licensing         nsw_fair_trading_licence, public liability, workers compensation
  contact           street_address, is_staffed, suburb, postcode, phone, email
  service_areas     the suburbs actually worked in, not the suburbs we built pages for
  pricing           per_m2_ranges, minimum_job_value
  reviews           value, permission_to_publish
  completed_projects
  photography       real_camden_photographs, permission_to_publish

  fields verified: true    0
  fields with a value      2   trading_name and phone, both verified: false
```

Two fields carry a value while remaining unverified, deliberately:

```text
  trading_name  "CoreX Concreters Camden"
                Appears in page copy. Presence in copy is not verification, and
                the legal entity behind the trading name is unknown.

  phone         "03 4517 6915"
                Present on 120 occurrences in the artifact. 03 is a VICTORIAN area
                code on a NSW business. Standing rule 5 requires it stay FLAGGED,
                not silently corrected. Both ownership_proven and routing_proven
                are false.
```

### `contact.is_staffed` is the decisive field

§4.30.2 forbids emitting `LocalBusiness` without a verified **staffed** address. An unstaffed address is
not a LocalBusiness location, and asserting one is a false claim about where customers can find the
business. The field is typed `null` and unverified, so `LocalBusiness` cannot be emitted at all.

---

## 2. D2 — the provider omission ladder

```text
  RANK  CONDITION                                          ACTION
     1  #localbusiness defined                             Service.provider -> #localbusiness
     2  #organization defined from verified legal name     Service.provider -> #organization
     3  neither defined                                    Service OMITS provider entirely

  Outcome under current verification state: RANK 3 on every page, as D2 predicted.
```

### Service nodes omitting `provider`, by page class

```text
  PAGE CLASS         SERVICE NODES   PROVIDER OMITTED
  suburb                        60                 60
  intersection                  35                 35
  service                       10                 10
  TOTAL                        105                105
```

**105 of 105.** Without this ladder the build would have emitted 105 `Service.provider` references and 95
`Service.areaServed` references pointing at `#localbusiness`, an `@id` that is never defined — 200
dangling references across 105 pages. Valid JSON that fails seo-spec §7.6 gate 2 and every external
validator.

A Service with no provider is incomplete but true. A Service pointing at an entity that does not exist is
neither.

---

## 3. Refusal log

Full log: `reports/30-schema-refusals.md`.

```text
  total refusals logged   309

  BY NODE
  Service.provider        105   neither #localbusiness nor #organization defined
  Service.areaServed       95   areaServed referenced #localbusiness, undefined
  Service.offers          105   pricing.per_m2_ranges unverified
  AggregateRating           2   reviews unverified, permission_to_publish false
  LocalBusiness             1   legal_name, street_address, is_staffed all unverified
  Organization              1   legal_name unverified
```

Every refusal names the specific unverified field that caused it. None is silent.

The `AggregateRating` refusal is worth stating plainly: emitting an unverified aggregate rating is both a
false claim and a Google structured-data policy violation. It is refused on both grounds.

---

## 4. §7.6 gates

```text
  GATE                                                  RESULT   DETAIL
  valid JSON                                            PASS     156 graphs serialise
  every referenced @id defined in the same graph        PASS     0 dangling references
  no LocalBusiness outside / and /contact/              PASS     0 stray
  every FAQPage Q&A verbatim in rendered HTML           PASS     0 FAQPage nodes; vacuous
  zero placeholder strings in any emitted JSON-LD       PASS     0 across all 4 tokens

  builder exit code   0
```

The second gate is the D2 build-failing check. It passes at zero because the ladder omitted rather than
dangled.

The FAQPage gate passes **vacuously** — no FAQPage node is emitted, because the Q&A content on the suburb
pages contains unresolved placeholders and cannot be asserted as verbatim rendered content. Stated as
vacuous rather than reported as a clean pass.

---

## 5. Forms

`reports/30-forms-spec.md` written. Specification only; nothing implemented.

```text
  form ID 3                      referenced by /about/ and /gallery/
  exists in the database         no
  travels in a WXR               no — Fluent Forms uses its own tables
  implementation status          NOT IMPLEMENTED
  approval status                AWAITING APPROVAL — 7 items
```

### The finding that matters most

```text
  privacy policy page       DOES NOT EXIST among the four utility pages
  consequence               the proposed form collects name, phone, email and
                            suburb with no published privacy basis and no stated
                            retention period
  status                    BLOCKER. The Australian Privacy Principles apply once
                            personal information is collected. This is an owner
                            decision with legal weight, not a form setting.
```

SMTP delivery is specified as a hard requirement rather than a preference: unauthenticated `mail()` from a
web host is routinely dropped silently, and a contact form that silently loses enquiries is worse than no
form, because the business believes it is working.

---

## 6. `CONTEXT.md` update and diff

```text
  Latest completed stage       29 -> 30
  Verified facts register      none -> data/verified-facts.yml, 0 fields verified
  Schema builder               none -> fail-closed, emits minimal non-identity schema only
  New blocker                  no privacy policy page exists; form 3 cannot go live
  Confirmed                    105 of 105 Service nodes omit provider (D2 outcome 3)
  Confirmed                    200 dangling @id references avoided by the ladder
  Index-ready                  0 of 157 — UNCHANGED
  Launch gate                  NO-GO — UNCHANGED
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

## GATE 30 RESULT

```text
  data/verified-facts.yml, every field empty and verified: false    PASS
  Schema builder implements seo-spec §7                             PASS
  One @graph per page, permanent @id spine                          PASS — 156 graphs
  LocalBusiness/GeneralContractor only on / and /contact/           PASS — and emitted on neither
  Refuses to emit nodes with unverified required fields             PASS — 309 refusals
  Logs every refusal with its reason                                PASS
  §7.6 gates implemented and passing                                PASS — 5 of 5
  D2 provider ladder implemented in strict order                    PASS
  Zero references to an undefined @id                               PASS — 0
  Service nodes omitting provider reported per class                PASS — 105, all three classes
  Forms specified, not implemented                                  PASS
  Builder produces nothing or minimal non-identity schema           PASS

  GATE 30: PASS.
```
