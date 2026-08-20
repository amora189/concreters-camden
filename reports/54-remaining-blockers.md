# Remaining blockers — 21 August 2026

## Mandatory blockers

| ID | Blocker | Evidence | Required clearance |
|---|---|---|---|
| D23-01 | Concrete Slabs curing cell unresolved | `reports/53-unresolved-provider-inputs.md` Q04 | Applicable project specification or qualified provider/engineer instruction |
| D23-02 | Shed and Garage Slabs curing cell unresolved | same report Q10 | Applicable project specification or qualified provider/engineer instruction |
| D23-03 | Attestation matrix empty | `data/service-specs.yml`: 0 verified values | Populate only with evidence/attestation; never infer |
| G7 | Uniqueness gate fails | 1,761 repeated five-grams; 1,491 pairs | Substantive page rewrites after D23; threshold unchanged |
| G12 | Coherence gate fails | 90 severe; 139 above threshold; ratio 0.8244 | Individual human-readable rewrites; zero severe pages |

## Deferred until mandatory blockers clear

- Ten service-page rebuild and 60 suburb-page rebuild.
- Identity/privacy/form implementation in staging.
- Derivative WXR regeneration for release.
- PHP 8.3 WordPress/Elementor staging import.
- Database verification, visual QA, performance QA and any release-wave approval.

## Explicitly not blockers because they passed

Immutable hashes, recovery tests, media intake, Astra audit, Phase D Liverpool,
Elementor reference resolution, source-brand removal, claim/evidence parity,
architecture parity, menu safety and schema placeholder checks all passed in this run.
