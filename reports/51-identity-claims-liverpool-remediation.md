# Report 51 — owner identity, claims and Liverpool evidence application

Date: 21 August 2026 (Australia/Sydney)

## Outcome

The owner-attested public identity, contact data, non-customer office status and enquiry-coordination model are now applied through the reproducible derivative pipeline. The original claim baseline reconciles exactly at **232 occurrences / 228 unsupported**. Every baseline occurrence has an exact disposition; the regenerated reader-visible payload has **16 evidenced occurrences and zero unsupported occurrences**. The broader detector also dispositioned **309 claim-bearing surfaces** that were outside the former register.

Liverpool Council evidence is applied to 12 fields across Leppington, Austral, Edmondson Park and Bringelly. Schema remains fail-closed: 76 WebSite/WebPage graphs and 70 Service nodes are generated, with **no Organization, no LocalBusiness and no Service.provider**.

This does not make the site launchable. Full preflight remains **NO-GO** on Gate 7 (uniqueness) and Gate 12 (coherence). Index-ready remains zero. No import or deployment occurred.

## Owner facts recorded

| Fact | Recorded state | Public restriction |
|---|---|---|
| Public brand/site-operator label | Structure Co Concreters Camden — verified | A public label, not a legal entity |
| Email | `info@concreterscamden.com.au` — verified and monitored | Not evidence of a legal entity or contractor credential |
| Telephone | `(03) 4328 3392` — verified | Never described as a local Camden or Sydney number |
| Telephone URI | `tel:+61343283392` — verified | Same restriction |
| Address | 15 Murray Street, Camden NSW 2570 — verified | Administrative correspondence office only |
| Staffed | Yes — verified | Staffed status does not make it customer-facing |
| Customer/visitor access | No — verified | No visit invitation, showroom, customer-service-location or walk-in wording |
| Operating model | Enquiry management and coordination of suitable independent providers — verified | No implication that Structure Co directly performs regulated work |
| Enquiry legal effect | “Submitting an enquiry does not create a construction contract.” | Required beside every form |
| ABN | Empty and unverified | No ABN is published, requested or inferred |
| Legal entity | Empty and unverified | Identity/privacy blocker remains |
| NSW contractor/licence/insurance | Empty and unverified | No specific credential is authorised for publication |
| Service areas | Empty and unverified | Suburb pages do not prove where work will be performed |
| Provider-network size | Empty and unverified | No number or “extensive network of friends” wording |

The permitted public operating disclosure is applied materially as attested:

> Structure Co Concreters Camden manages concreting enquiries and coordinates suitable independent providers. Job-specific quotations, contractual terms, licensing, insurance and warranty information must be confirmed before work begins.

The verified facts are in `data/verified-facts.yml`. The owner authority and resulting controls are recorded in `build/21-spec-ledger.json` under `OWNER-2026-08-21-IDENTITY-CLAIMS-LIVERPOOL`.

## Claim remediation

### Exact baseline reconciliation

```text
  original registered occurrences                    232
  original unsupported                               228

  removed by Report 50 media/D32                       97
  removed without replacement                          99
  neutralised with attested/non-claim wording          24
  replaced with cited official Liverpool evidence      12
                                                      ---
  total dispositioned                                 232

  additional former-detector blind spots              309
    neutralised                                        255
    removed                                             54

  final reader-visible detected occurrences             16
    supported                                           16
    unsupported                                          0
```

The 16 final supported occurrences are 15 placements of the owner-attested operating disclosure, which says warranty information must be confirmed rather than promising a warranty, and one privacy-policy promise to respond to a personal-information request within a reasonable period. No unsupported claim is retained or blocked in the derivative. Publication remains blocked for independent reasons listed below.

Every occurrence, exact original field, placement, evidence state, final text, disposition and authority is in `build/51-claim-disposition-register.json`; the flattened register is `reports/46-claim-register.csv`.

### Baseline categories and dispositions

| Category | Total | Final disposition |
|---|---:|---|
| Band B local-project adjacency | 4 | 4 removed by Report 50/D32 |
| REAL_PHOTO_PENDING local-project text | 44 | 44 removed by Report 50/D32 |
| Review/rating/testimonial body claims | 48 | 46 removed by Report 50; 2 neutralised |
| Review/rating/testimonial widgets | 3 | 3 removed by Report 50 |
| False “verified project record says” | 42 | 30 removed; 12 replaced with official Liverpool evidence |
| Invented “researched … job record contains” | 15 | 15 removed |
| Licensed/insured/accreditation | 16 | 16 removed |
| Fixed-price/on-site quotation promises | 30 | 16 removed; 14 neutralised |
| Service-area claims | 18 | 16 removed; 2 neutralised |
| Direct contractor/operator claims | 6 | 3 removed; 3 neutralised |
| Local-operation/premises claims | 2 | 1 removed; 1 neutralised |
| Workmanship guarantee/warranty promise | 2 | 1 removed; 1 neutralised |
| Completed/recent local work | 1 | removed |
| Response-time wording | 1 | neutralised to the supported privacy context |

No baseline award, years-in-business, completed-job-count, equipment/vehicle/crew-ownership or provider-network-size occurrence survived the registered scan.

### Additional blind spots closed

| Previously unasserted surface | Total | Action |
|---|---:|---|
| Free/on-site quote and scope CTAs | 162 | Neutralised to an enquiry action |
| Direct service/scope presentation | 33 | Neutralised to enquiry types/coordination |
| Customer-choice/social-proof headings | 15 | Neutralised to coordination information |
| Local-service presentation | 8 | Neutralised without a local-operation claim |
| Unsupported opening hours | 7 | Removed; public telephone substituted where appropriate |
| Unsupported “verified local” and “researched ground note” framing | 84 | 54 fields removed; 30 neutralised |

The latter 84 are the next coherence-style blind spot: the previous detector looked for specified marketing phrases but allowed copy to call unlinked local job mixes, approval paths, neighbouring service links, local distinctions and ground notes “verified”. These are now executable failures rather than prose-review observations.

## Contact placements and form treatment

Counts in the two generated public import artifacts:

| Placement token | Occurrences |
|---|---:|
| `(03) 4328 3392` | 78 |
| `tel:+61343283392` | 65 |
| `info@concreterscamden.com.au` | 14 |
| `15 Murray Street, Camden NSW 2570` | 12 |
| Non-contract disclosure | 13 |
| Superseded `03 4517 6915` | 0 |
| Superseded `tel:+61345176915` | 0 |

`/about/`, `/contact/`, `/gallery/` and `/quote/` each contain one `[fluentform id="3"]` placeholder and the exact non-contract disclosure as the immediately following Elementor widget. This changes only the derived payload; the Fluent Forms record itself is not built or imported. `reports/30-forms-spec.md` now records the verified recipient and operating model, plus the outstanding form, consent, SMTP and privacy controls.

The address is presented only as a staffed administrative correspondence office not open to customers or visitors. No opening hours, visit invitation, showroom, walk-in, local-number or storefront wording remains.

## Schema treatment

`scripts/30-build-schema.py` now reads the 76-page allowlist and both generated import artifacts rather than the immutable 156-page WXR.

```text
  graphs                             76
  WebSite nodes                      76 — verified public label only
  WebPage nodes                      76
  Service nodes                      70 — 10 service + 60 suburb
  Organization                       0 — legal_name unverified
  LocalBusiness/GeneralContractor     0 — non-customer office; legal_name unverified
  Service.provider                    0 — D2 outcome 3
  AggregateRating                     0
  legalName / ABN / licence data      0
  address/opening-hours schema        0
```

Staffed status alone is deliberately insufficient. The office is not customer-facing or open to visitors, so LocalBusiness remains forbidden even before the unresolved legal-name requirement is considered.

## Liverpool Council evidence

Sources sighted 21 August 2026:

- [Liverpool City Council forms page](https://www.liverpool.nsw.gov.au/council/Fees-Forms-Policies-and-Enforcement/forms)
- [March 2026 Vehicular Crossing Application and Specifications](https://www.liverpool.nsw.gov.au/__data/assets/pdf_file/0003/286329/VEHICULAR-CROSSING-APPLICATION-FORM-March-2026v1.pdf), 18 pages, SHA-256 `43F74C0F01C5EA6F0C89919BE8C1859F758F96AF549A9CF71ADA5F87DD7CAF33`
- [Liverpool City Council online application portal](https://mycouncil.liverpool.nsw.gov.au/ePathway/Production/Web/Default.aspx)

Only these current-form requirements are recorded in `data/council-specs.yml` and applied:

1. Application under section 138 of the Roads Act 1993.
2. Property-owner responsibility for construction, maintenance and repair costs.
3. Owner responsibility to ensure the contractor is licensed and holds current public-liability cover of at least $10 million.
4. Plain-concrete surface.
5. Minimum 25 MPa at 28 days for residential driveways.
6. Minimum 32 MPa at 28 days for medium-density, commercial and industrial driveways.
7. Minimum 50 mm compacted DGS20 bedding for the crossing.
8. Minimum 100 mm compacted DGS20 bedding where kerb, gutter or layback is constructed.
9. Formwork/associated-work inspection and Council approval before pouring.
10. Construction to Council drawing R25 and site-specific inspector directions.
11. Applicable utility clearances and approvals.
12. Council application and inspection process, including the application number for booking.
13. Fees assessed under Council’s current schedule; no dollar fee is invented.

The 12 derivative placements are three fields on each of `/concreters-leppington/`, `/concreters-austral/`, `/concreters-edmondson-park/` and `/concreters-bringelly/`. No precinct-specific DCP control is generalised. The Council’s contractor requirement is explicitly not presented as evidence that Structure Co is licensed or insured.

## Privacy and identity blockers that remain

The derived privacy page uses the verified public label, email, telephone, administrative address, non-visitor treatment, operating model and non-contract disclosure. Its blockers reduce from 11 to five genuine markers:

1. accountable legal entity for privacy obligations;
2. form delivery, authenticated sending domain, database storage and access controls;
3. owner-decided retention period;
4. installed analytics/tracking state;
5. publication/effective date.

No ABN marker or ABN assertion remains. The identity blocker is narrower but real: no accountable legal entity or specific contracting NSW provider is verified, and no licence or insurance is authorised. `service_areas` also remains empty/unverified.

Phase C therefore remains BLOCKED under the existing governing precondition: 11 fields are verified true and 14 remain false; the required unresolved fields are legal name, ABN, NSW Fair Trading licence and public-liability insurance. The owner’s “do not publish or assert an ABN” direction is preserved; the gate was not weakened to make Phase C pass.

## Service-specification blockers

Phase A is unchanged: `data/service-specs.yml` contains **91 verified:false, 0 verified:true**, with `populated:false`. The ten service-page rebuilds remain blocked. No unsupported service specification was invented or rewritten in this pass.

Phase D is now RUNNABLE: `data/council-specs.yml` contains 16 verified source/fact nodes, 16 source URLs and 16 sighted dates. This pass did not start Phase D or build the calculator.

## Changed files

Authoritative mutable inputs and implementation:

- `data/verified-facts.yml`
- `data/council-specs.yml` — new
- `build/21-spec-ledger.json`
- `reports/30-forms-spec.md`
- `lib/claim_scan.py` — new shared detector
- `lib/content_remediation.py` — new reproducible transformation/audit layer
- `scripts/46-architecture-import-gate.py`
- `scripts/46-claim-evidence-gate.py`
- `scripts/30-build-schema.py`
- `scripts/51-evidence-validation.py` — new
- `scripts/28-preflight.sh`
- `tests/test_identity_claims_liverpool.py` — new
- `CONTEXT.md`
- `reports/51-identity-claims-liverpool-remediation.md` — this report

Generated controls and payloads:

- `build/46-active-page-allowlist.json`
- `build/46-active-main-import.xml`
- `build/51-privacy-import.xml`
- `build/47-media-remediation.csv` — reproducibly regenerated; media decisions unchanged
- `build/51-claim-disposition-register.json`
- `build/46-claim-register.json`
- `build/30-schema-output.json`
- `reports/46-claim-register.csv`
- `reports/46-architecture-import-gate.json`
- `reports/46-claim-evidence-gate.json`
- `reports/46-public-media-gate.json`
- `reports/46-source-brand-gate.json`
- `reports/30-schema-refusals.md`
- `reports/51-evidence-validation.json`
- `reports/28-preflight.md`

The preflight also deterministically refreshed its normal supporting outputs: Reports 22 media/Astra, 28 analytical gates, and 34 coherence output. No immutable or governing file was changed.

## Derivative hashes

| Artifact | SHA-256 |
|---|---|
| `build/46-active-main-import.xml` | `9FA49392B181EE839954A0FB9F306B6E4EB7CA4891ED921CF14079EE8AE4CB82` |
| `build/51-privacy-import.xml` | `80AB5AF8C125E1A6C79E8CA2D976B8002FDE15686CFF9C6F627EF53B9C234E7B` |
| `build/51-claim-disposition-register.json` | `E9A2F3FD81D4781CBCCE216D8F211595B5ACA2C15942A6DCFFCF80FD91BD464F` |
| `build/30-schema-output.json` | `A99386B6341AB51C4CDB0044445AEFBBC9B065CCB7BD858DFED493A4AF4582F6` |

The main derivative was regenerated by `scripts/46-architecture-import-gate.py`; it was not manually edited.

## Immutable hashes

| Immutable file | SHA-256 | Result |
|---|---|---|
| `camden-concreting-import.xml` | `A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884` | MATCH |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | `45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15` | MATCH |
| `build/stage9-page-manifest.json` | `578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42` | MATCH |
| `build/stage8-image-map.json` | `0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF` | MATCH |
| `reports/08-image-rename-map.csv` | `43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8` | MATCH |
| `CODEX-BUILD-2.1.md` | `BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C` | MATCH |
| `archive/governing/CODEX-BUILD-2.md` | `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | MATCH |

## Validation results

| Validation | Result |
|---|---|
| UTF-8 canary and three exact assertions | PASS |
| Owner-attestation validation | PASS |
| Claim-to-evidence parity | PASS — 232/228 dispositioned; current 16/16 supported |
| Liverpool-source validation | PASS — 13 facts; 12 page placements |
| Schema validation | PASS — no Organization/LocalBusiness/provider |
| Privacy-marker audit | PASS — exactly five genuine blockers |
| Contact-data consistency | PASS — old phone/URI zero; four form disclosures adjacent |
| Media intake audit | PASS — 55/55 |
| Public-media suitability | PASS — 55 files cleared; Band A/B complete |
| Active/import parity and reproducibility | PASS — 75 main + privacy = 76; 81 withdrawn absent |
| Regression tests | PASS — 11 |
| `git diff --check` | PASS |

## Phase table

| Phase | Status | Evidence |
|---|---|---|
| A — attest figures | BLOCKED | 91 false, 0 true; populated false |
| B — media and staging | RUNNABLE | 55/55 public media; 28/28 excluded; no Band A holds |
| C — identity and schema | BLOCKED | 11 true / 14 false; legal name, ABN, licence and public liability unresolved |
| D — Liverpool | RUNNABLE | 16 verified, 16 source URLs, 16 sighted dates |
| E — service rebuild | BLOCKED | Requires Phase A |
| F — images | BLOCKED | Requires A–E; remains last |
| G — release | BLOCKED | Requires preceding phases and preflight GO |

## Complete preflight

| Gate | Result | Detail |
|---|---|---|
| 1. Encoding canary | PASS | Fixture and exact assertions survived |
| 2. Stage 9 gates | PASS | 15/15 |
| 3. Post-ID collisions | PASS | Main 306 IDs; privacy 1; collisions 0; calculator absent |
| 4. Media intake | PASS | 55/55 |
| 5. Astra | PASS | Required groups/design carriage/consistency pass |
| 6. Elementor reference count | PASS | 1,183 total; unresolved 0 |
| 7. Uniqueness | **FAIL** | 1,761 repeated 5-grams; 1,491 within-class pairs over 40% |
| 8. Intersection audit | PASS | 35/35 allowlisted; all draft |
| 9. Menu lint | PASS | Zero unsafe Wave 1 targets |
| 10. Victorian blocklist | PASS | Zero in governed public artifacts |
| 11. Schema placeholders | PASS | Zero |
| 12. Coherence | **FAIL** | 90 SEVERE; 139 above threshold; corpus filler 82.44% |
| 13. Source brand | PASS | 466 = 366 transformed + 100 preserved paths; reader-visible remainder zero |
| 14. Assigned menus | PASS | Zero unsafe assigned targets |
| 15. Active/import parity | PASS | 76 allowed; 81 withdrawn; calculator absent |
| 16. Claim/evidence parity | PASS | 16 supported; 0 unsupported |
| 17. Public media | PASS | Blocking 0; Band A unrecorded 0; Band B failures 0 |
| 18. Identity/Liverpool/schema evidence | PASS | Unsupported claims 0; Liverpool 12; privacy blockers 5; LocalBusiness 0 |

**Overall: NO-GO.** The only failing preflight gates are 7 and 12. They were not weakened.

## Explicit non-actions

No WordPress import, database execution, deployment, publication, indexability change, sitemap submission, remote media fetch or generated image occurred. No immutable file or governing/decision document was edited. The original privacy and main WXRs were not changed. Temporary PDF-rendering and diagnostic files used to verify the official Liverpool source were removed after their facts, source URLs, page citations and PDF hash were recorded.
