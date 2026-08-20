# DECISION-09 — independent-provider specification model

Date: 21 August 2026 (Australia/Sydney).
Origin: owner instruction issued in session, 21 August 2026.
Status: **current owner decision for the mutable specification model.**
This decision does not edit or supersede Decisions D1–D38; it records the authorised
operating-model disposition for claims that are removed from public copy.

Decisions D39–D41. Numbering continues from DECISION-08 (D35–D38).

---

## D39 — Independent-provider specification model

Structure Co Concreters Camden is an enquiry and coordination service. It does not claim
to operate one universal construction methodology across independent providers.

The website must not publish a provider-specific thickness, strength, reinforcement, base,
joint, curing, drainage, edge or service-specific method unless supported by an applicable
authority, design, product specification or identified provider attestation.

A specification cell may be resolved without a numeric value when all of the following
are true:

1. the website makes no universal technical claim for that field;
2. the field is correctly classified as design-, council-, product-, site- or provider-specific;
3. the public wording explains who must confirm it and when;
4. claim-to-evidence validation proves no unsupported value appears; and
5. the classification is supported by an authoritative source or the verified
   independent-provider operating model.

This is a removal of an unsupported claim, not verification of a technical value.

The mutable model therefore records `verified: false` for a removed numeric value while
recording a separate `resolution: claim-removed` disposition. Numeric output is prohibited
unless a future evidenced-fixed-value cell supplies a source and sighted date.

## D40 — Curing disposition

For Concrete Slabs and Shed and Garage Slabs, the website publishes no universal curing
method or duration. The approved public position is:

> Curing requirements are confirmed for the selected concrete system and project conditions
> before placement. The appointed provider must follow the applicable design, supplier and
> product requirements, taking account of exposure and weather conditions.

No number of hours or days may be added without project-applicable evidence. Specifications
from unrelated councils must not be copied. The two Report 53 unresolved cells are therefore
resolved as `provider-confirmed` with `claim-removed`; this does not attest a provider method.

## D41 — Full-site completion model

Attempt to rebuild all 76 active pages. Any page that cannot meet evidence, uniqueness and
coherence requirements remains excluded from release rather than being padded, spun or
falsely approved. The 81 withdrawn pages remain physically excluded and the calculator
remains absent.

## Implementation contract

The authoritative mutable implementation is `data/service-specs.yml` schema version 2.0,
with the machine-readable decision ledger in `build/54-independent-provider-decision.json`.
The 90-cell migration retains the Report 53 evidence row as the classification source,
prohibits unsupported numeric output, and requires a regression scan over the derivative.

This decision authorises local source, script, report and checkpoint changes only. It does
not authorise edits to immutable artifacts or existing governing documents, production
deployment, DNS/indexability changes, live enquiries, or remote Git operations.
