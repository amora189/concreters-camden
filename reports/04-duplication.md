STAGE 4 - Remaining Tier 1 suburbs
=======================================
READ:      suburbs.json; suburbs-expanded.json verified Tier 1 records; oran-park-gold-standard.md; approved Oran Park Elementor pilot; contextual-link rule approved after Gate 3
DID:       Classified only the three approved factual/boilerplate sentences as shared components. Diagnosed overlap by module, rewrote Leppington modules 4/6/7 and Gledswood Hills modules 6/7, and preserved every differentiator verbatim.
ARTIFACTS: build/stage4-leppington-preview.md; build/stage4-tier1-pages.json; reports/04-duplication.md

## Unique body percentage

Measured as the percentage of each page's body 5-gram positions that occur on no other Tier 1 page.

| Page | Unique body | Shared components | Result |
|---|---:|---:|---|
| /concreters-oran-park/ | 96.29% | 0.00% | PASS |
| /concreters-leppington/ | 76.71% | 3.52% | PASS |
| /concreters-gregory-hills/ | 71.74% | 7.10% | PASS |
| /concreters-gledswood-hills/ | 75.22% | 6.86% | PASS |
| /concreters-austral/ | 68.76% | 3.40% | PASS |
| /concreters-harrington-park/ | 74.73% | 6.65% | PASS |

## Pre-rewrite module drivers

- /concreters-leppington/ vs /concreters-austral/: M2 91.38%, M9 87.93%, M6 49.40%, M7 48.57%, M4 43.59%
- /concreters-leppington/ vs /concreters-gledswood-hills/: M2 91.38%, M9 87.93%, M6 44.44%, M4 40.00%, M8 30.00%
- /concreters-gregory-hills/ vs /concreters-gledswood-hills/: M2 91.53%, M9 88.33%, M6 46.67%, M8 36.36%, M5 26.32%

## Modules rewritten

- /concreters-leppington/: Module 4, Module 6, Module 7
- /concreters-gledswood-hills/: Module 6, Module 7

## Pairwise 5-gram overlap

| Page A | Page B | Overlap | Result |
|---|---|---:|---|
| /concreters-austral/ | /concreters-harrington-park/ | 32.10% | PASS |
| /concreters-gledswood-hills/ | /concreters-austral/ | 28.55% | PASS |
| /concreters-gledswood-hills/ | /concreters-harrington-park/ | 25.42% | PASS |
| /concreters-gregory-hills/ | /concreters-austral/ | 32.18% | PASS |
| /concreters-gregory-hills/ | /concreters-gledswood-hills/ | 26.81% | PASS |
| /concreters-gregory-hills/ | /concreters-harrington-park/ | 33.60% | PASS |
| /concreters-leppington/ | /concreters-austral/ | 27.31% | PASS |
| /concreters-leppington/ | /concreters-gledswood-hills/ | 22.05% | PASS |
| /concreters-leppington/ | /concreters-gregory-hills/ | 22.56% | PASS |
| /concreters-leppington/ | /concreters-harrington-park/ | 23.12% | PASS |
| /concreters-oran-park/ | /concreters-austral/ | 8.33% | PASS |
| /concreters-oran-park/ | /concreters-gledswood-hills/ | 7.93% | PASS |
| /concreters-oran-park/ | /concreters-gregory-hills/ | 8.52% | PASS |
| /concreters-oran-park/ | /concreters-harrington-park/ | 8.27% | PASS |
| /concreters-oran-park/ | /concreters-leppington/ | 7.67% | PASS |

Repeated sentences appearing on more than two pages: 0

GATE 4: PASS
  ✓ Every page >=60% unique body positions: yes
  ✓ No pair exceeds 40% overlap: yes
  ✓ No sentence appears on more than two pages: yes
  ✓ Shared components <=15% of every page: yes

Proceeding to Stage 5.
