# Band B application report

Date: 20 August 2026 (Australia/Sydney).
Authority: owner instruction and `HANDOVER-2026-08-19.md` Part 2.

## Result

```text
  GENERIC assets renamed                  7
  UNUSABLE assets excluded                2
  active public-media files               55
  unusable Elementor slots registered     28
  verification failures                   0
  verdict                                 PASS
```

## GENERIC filename and alt remediation

| ID | Target filename | Subject-only alt |
|---:|---|---|
| 46 | `exposed-aggregate-front-paths-46.webp` | Exposed aggregate paths leading to a home's front entry |
| 47 | `fresh-concrete-backyard-slab-47.webp` | Freshly poured concrete slab beside a two-storey home |
| 48 | `exposed-aggregate-residential-driveway-48.webp` | Exposed aggregate driveway leading to a carport |
| 49 | `fresh-concrete-pool-surround-49.webp` | Freshly poured concrete beside a swimming pool |
| 51 | `concrete-stepping-slabs-garden-path-51.webp` | Concrete stepping slabs laid through a garden |
| 52 | `fresh-concrete-pool-surround-52.webp` | Freshly poured concrete beside a swimming pool |
| 228 | `fresh-concrete-side-yard-slab-228.jpg` | Freshly poured concrete slab along a side boundary |

All seven are decoration only. They cannot be used as customer evidence or in a recent/local-work module.
Attachments 49 and 52 are exact binary duplicates but remain distinct IDs.

## UNUSABLE slot removal

| ID | Pages | Publish | Draft | D32 module | Image widget | Image-box setting |
|---:|---:|---:|---:|---:|---:|---:|
| 280 | 14 | 2 | 12 | 1 | 8 | 5 |
| 1067 | 14 | 1 | 13 | 1 | 10 | 3 |

The complete 28-row page/widget list is `reports/45-band-b-unusable-slots.csv`.
No replacement image or substitute badge is permitted.

## Post-import count contract

```text
  original foreground image references    1,085
  background-image references                 98  unchanged
  D32 local-work modules                     15  removing 45 images
  GENERIC references removed with D32          4
  surviving GENERIC references remediated     106
  UNUSABLE references removed                  28
  surviving foreground image references     1,014
```

The immutable WXR remains untouched. Band B is now enforced in the reproducibly generated
`build/46-active-main-import.xml`; the former post-import mutator is a fail-closed guard.
The public intake contains the seven Band B files under their target names and the two
UNUSABLE binaries remain recoverable outside public uploads.
