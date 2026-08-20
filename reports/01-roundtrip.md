STAGE 1 - Round-trip harness
=======================================
READ:      codex-clone-prompt.md section 1 widget field map; source/eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
DID:       Built lib/wxr.py, lib/walk.py and tests/test_roundtrip.py. Probed _elementor_data inside CDATA and confirmed raw HTML is stored verbatim, so the serializer preserves source encoding: json.dumps(..., ensure_ascii=True, separators=(',', ':')) plus forward-slash escaping, with no HTML entity pass.
ARTIFACTS: lib/wxr.py; lib/walk.py; tests/test_roundtrip.py; reports/01-roundtrip.md

## Test command

`python -m unittest tests.test_roundtrip -v`

## Probe

- _elementor_data values inspected: 25
- Values containing raw `<p>` or `<br>` HTML: 23
- Values containing entity-escaped `&lt;p&gt;` or `&lt;br&gt;`: 0
- Result: no html.unescape/html.escape pass is applied to Elementor data.

## Per-page round-trip results

| Page slug | Title | Result | Detail |
|---|---|---|---|
| `privacy-policy` | Privacy Policy | PASS | no _elementor_data meta present |
| `homepage` | Homepage | PASS | 60831 bytes byte-match |
| `exposed-aggregate-melbourne` | Exposed Aggregate | PASS | 50863 bytes byte-match |
| `concrete-slabs-melbourne` | Concrete Slabs in Melbourne | PASS | 57812 bytes byte-match |
| `concrete-paths-melbourne` | Concrete Paths and Pathways Melbourne | PASS | 58790 bytes byte-match |
| `concrete-patios-melbourne` | Concrete Patios &amp; Alfresco Melbourne | PASS | 60475 bytes byte-match |
| `concreter-point-cook` | Concreters in Point Cook | PASS | 52071 bytes byte-match |
| `contact` | Contact Page | PASS | 19508 bytes byte-match |
| `concrete-driveways-melbourne` | Concrete Driveways in Melbourne | PASS | 70460 bytes byte-match |
| `concreter-werribee` | Concreters in Werribee | PASS | 64757 bytes byte-match |
| `concrete-driveway-cost-melbourne` | Concrete driveway cost per m2 melbourne | PASS | 75836 bytes byte-match |
| `wyndham-council-vehicle-crossing` | What Wyndham Council Actually Requires for a Vehicle Crossing (2026) | PASS | 51383 bytes byte-match |
| `decorative-concrete-melbourne` | Coloured &amp; Decorative Concrete Melbourne | PASS | 38878 bytes byte-match |
| `concreter-tarneit` | Concreters Tarneit | PASS | 49597 bytes byte-match |
| `__trashed-3` | Elementor Page #981 | PASS | no _elementor_data meta present |
| `concreters-hoppers-crossing` | Concreters Hoppers Crossing | PASS | 44182 bytes byte-match |
| `concreters-truganina` | Concreters Truganina | PASS | 46498 bytes byte-match |
| `why-does-concrete-crack` | Why Does Concrete Crack? A Melbourne Homeowner's Guide | PASS | 28762 bytes byte-match |

GATE 1: PASS
  ? Harness files written: lib/wxr.py, lib/walk.py, tests/test_roundtrip.py
  ? Every page byte-matches after parse and re-serialise: 18 pass, 0 fail
  ? Remaining byte diff count: 0

Proceeding to Stage 2.
