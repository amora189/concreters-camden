# Stage 9 — Final validation and assembly

Assembled `camden-concreting-import.xml` with 156 pages, 83 attachments, the Elementor kit, Astra custom CSS and five rebuilt menus.

## Pre-assembly hierarchy assertions

- `/guides/`: post ID 1502, `post_name=guides`, `post_parent=0`, status `draft`.
- Guide children: 35; every child has `post_parent=1502` and a final-segment-only `post_name`.
- Unexpected nested URLs: 0.
- Slash-bearing `post_name` values in `build/`: 0.

## Gate results

| Gate | Check | Result | Detail |
|---:|---|---|---|
| 1 | XML well-formed | PASS | XML parsed; 156 pages; hierarchy manifest clean; slash-bearing post_name values: 0 |
| 2 | Elementor JSON | PASS | Elementor JSON parsed for 156 of 156 pages |
| 3 | Round trip | PASS | Elementor JSON round trip matched for 156 pages |
| 4 | H1 | PASS | Exactly one H1 on every page |
| 5 | Victorian blocklist | PASS | Victorian blocklist returned zero matches in the assembled XML |
| 6 | Image IDs | PASS | All widget image IDs resolve against 83 attachments |
| 7 | Links | PASS | All page and menu links resolve; 0 orphans |
| 8 | Schema meta | PASS | No rank_math_schema_* meta keys remain |
| 9 | Cache | PASS | No _elementor_element_cache meta keys remain |
| 10 | Duplication | PASS | 105 substantive pages checked; minimum unique 60.46%; maximum pair overlap 35.16%; 45 research shells and the shared-component hub exempt |
| 11 | Meta lengths | PASS | Every Rank Math title is 50-60 characters and description is 140-160 characters |
| 12 | Meta uniqueness | PASS | Every complete Rank Math title is unique |
| 13 | Placeholders | PASS | All 163 placeholder/verify/photo markers are registered |
| 14 | Focus keywords | PASS | Every page has a non-empty focus keyword; no Werribe-class typo found |
| 15 | Status | PASS | Status split is 21 publish / 135 draft; hub and 35 guides are draft |

## Failing items

None.

GATE 9: PASS

HALT AT GATE 9. Stage 10 has not been run.
