# Stage 40 — `build/global-replace.json` ordering fix, with behaviour diff

Date: 19 August 2026 (Australia/Sydney).
Authority: owner instruction, 19 August 2026 — *"fix it. Reorder longest-find-first across the whole
file, not just the brand rules, and report the behaviour diff."*

**Applied.** This is the only file changed by this fix. It is a mutable build artifact, not an
immutable one; the seven immutable hashes are re-verified in §6 and all match.

---

## 1. The defect

`global-replace.json` is a **sequential** find/replace contract: each rule runs over the output of
the previous one. When a shorter `find` runs before a longer one that contains it, the shorter rule
consumes the prefix and the longer rule can never match.

The output is not merely un-replaced. It is **corrupted** — the shorter rule's replacement is spliced
into the middle of what should have been a single token, leaving a dangling fragment.

```text
  idx 10  "Wyndham"   ran before  idx 17  "Wyndham Vale"
  idx 11  "Werribee"  ran before  idx 16  "Werribee South"
  idx 11  "Werribee"  ran before  idx 20  "Werribee River"
```

Three violations. All three predate this session and are unrelated to the Structure Co rename; they
were found by an ordering assertion written while inserting the brand rules.

---

## 2. Behaviour diff — the concrete change

Both orderings were run over a probe corpus of all 25 `find` strings plus realistic sentences.
**7 of 31 probed strings change result.** Every change is a corruption being repaired.

```text
INPUT   "Werribee River"
  before  "mapped Camden/South West Sydney suburb per page River"
  after   "per-suburb water feature"

INPUT   "Werribee River corridor"
  before  "mapped Camden/South West Sydney suburb per page River corridor"
  after   "per-suburb water feature corridor"

INPUT   "Werribee South"
  before  "mapped Camden/South West Sydney suburb per page South"
  after   "mapped Camden/South West Sydney suburb per page"

INPUT   "Werribee South estate"
  before  "mapped Camden/South West Sydney suburb per page South estate"
  after   "mapped Camden/South West Sydney suburb per page estate"

INPUT   "Wyndham Vale"
  before  "per-page LGA from suburbs-expanded.json Vale"
  after   "mapped Camden/South West Sydney suburb per page"

INPUT   "Wyndham Vale council"
  before  "per-page LGA from suburbs-expanded.json Vale council"
  after   "mapped Camden/South West Sydney suburb per page council"

INPUT   "concreting in Werribee South and Wyndham Vale"
  before  "concreting in mapped Camden/South West Sydney suburb per page South
           and per-page LGA from suburbs-expanded.json Vale"
  after   "concreting in mapped Camden/South West Sydney suburb per page
           and mapped Camden/South West Sydney suburb per page"
```

Note the two distinct failure modes:

- **`Werribee River`** was hitting the *wrong rule entirely* — it became a suburb placeholder with a
  stray "River", instead of the water-feature placeholder written for it.
- **`Wyndham Vale`** was hitting the LGA rule instead of the suburb rule, leaving "Vale" dangling.

Both would have produced visibly broken copy, and `Werribee River`'s case would have silently
substituted the wrong *category* of placeholder — a suburb where a water feature was intended.

---

## 3. What changed in the file

Stable sort by descending `len(find)`. **18 of 25 rules changed index. No rule was added, removed or
edited** — asserted as a pure permutation of the rule set.

| `find` | idx before | idx after |
|---|---:|---:|
| `CoreX Concreters Camden` | 4 | 3 |
| `Wyndham City Council` | 9 | 4 |
| `Melbourne's west` | 7 | 5 |
| `Hoppers Crossing` | 15 | 6 |
| `volcanic plains` | 21 | 7 |
| `Werribee South` | 16 | 8 |
| `Werribee River` | 20 | 9 |
| `03 4427 9541` | 6 | 10 |
| `Wyndham Vale` | 17 | 11 |
| `Melbourne` | 8 | 13 |
| `Riverwalk` | 18 | 15 |
| `Werribee` | 11 | 16 |
| `Victoria` | 23 | 17 |
| `Wyndham` | 10 | 18 |
| `Tarneit` | 13 | 19 |
| `Harpley` | 19 | 20 |
| `E&T Co` | 3 | 21 |
| `CoreX` | 5 | 23 |

Final order:

```text
   0  bestconcretersmelbourne.com.au  -> concreterscamden.com.au
   1  E&T Co Concreters Melbourne     -> Structure Co Concreters Camden
   2  E&T Co Concreters Camden        -> Structure Co Concreters Camden
   3  CoreX Concreters Camden         -> Structure Co Concreters Camden
   4  Wyndham City Council            -> Camden / Liverpool / Campbelltown / Wollondilly per page
   5  Melbourne's west                -> South West Sydney
   6  Hoppers Crossing                -> mapped suburb per page
   7  volcanic plains                 -> Wianamatta Shale / page-specific geology
   8  Werribee South                  -> mapped suburb per page
   9  Werribee River                  -> per-suburb water feature
  10  03 4427 9541                    -> [[NSW_PHONE]]
  11  Wyndham Vale                    -> mapped suburb per page
  12  Point Cook                      -> mapped suburb per page
  13  Melbourne                       -> South West Sydney
  14  Truganina                       -> mapped suburb per page
  15  Riverwalk                       -> per-suburb estate from data
  16  Werribee                        -> mapped suburb per page
  17  Victoria                        -> New South Wales
  18  Wyndham                         -> per-page LGA from suburbs-expanded.json
  19  Tarneit                         -> mapped suburb per page
  20  Harpley                         -> per-suburb estate from data
  21  E&T Co                          -> Structure Co
  22  basalt                          -> Wianamatta Shale / page-specific geology
  23  CoreX                           -> Structure Co
  24  VIC                             -> NSW
```

The domain rule stays first, which also protects it: `bestconcretersmelbourne.com.au` contains
`melbourne`, and running it first means the `Melbourne` rule can never reach inside the domain.

---

## 4. Checks run

| Check | Before | After |
|---|---:|---:|
| Containment violations (shorter `find` preceding a longer one containing it) | **3** | **0** |
| Replacement-feeds-find hazards (a rule's output re-matched by a later rule) | 0 | 0 |
| Rule count | 25 | 25 |
| Rule set identical (permutation only) | — | **asserted** |

The second check matters as much as the first and was clean both ways: no rule's `replace` string
contains a later rule's `find`, so no output is re-processed downstream. Had that existed, a pure
length sort would not have been sufficient and a dependency order would have been needed.

---

## 5. What this does and does not affect

**Does not affect any built artifact.** `global-replace.json` is the replacement *contract*; it is
consumed at generation time. No page, no WXR, no report changes because of this fix. The immutable
main WXR was generated under the old ordering.

**The obvious follow-on question — did the corruption reach the built pages? — was run, not
deferred.** The 156-page WXR was generated with the broken ordering in place, so if `Werribee
South`, `Werribee River` or `Wyndham Vale` had appeared in the source corpus, the corrupted forms
would be sitting in the built copy.

Both built artifacts were scanned for all three corrupted output strings, for every residual
Victorian source token, and for every unresolved placeholder string:

```text
  camden-concreting-import.xml   10,114,884 chars   NO HITS on any probe
  camden-privacy-import.xml           6,735 chars   NO HITS on any probe

  probes: "suburb per page South", "suburb per page River",
          "suburbs-expanded.json Vale", Werribee, Wyndham, Tarneit, Truganina,
          Point Cook, Hoppers Crossing, Melbourne,
          "mapped Camden/South West Sydney suburb per page",
          "per-suburb water feature", "per-page LGA from suburbs-expanded.json",
          "per-suburb estate from data"
```

**The defect was latent.** It never fired on the built corpus — those three multi-word tokens do not
occur in it, and no placeholder leaked through unresolved. Nothing needs repairing in the artifacts;
the fix protects future generations, which matters because the ten service pages are being rewritten
and will regenerate through this contract.

---

## 6. Immutable hash table

```text
  camden-concreting-import.xml                          MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   MATCH
  build/stage9-page-manifest.json                       MATCH
  build/stage8-image-map.json                           MATCH
  reports/08-image-rename-map.csv                       MATCH
  CODEX-BUILD-2.1.md                                    MATCH
  archive/governing/CODEX-BUILD-2.md                    MATCH

  7 of 7 MATCH.
```
