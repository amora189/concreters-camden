# Handoff state — session reconstruction from artifacts

Date: 18 August 2026 (Australia/Sydney)
Author: successor agent, picking up after the Codex session was cut off at an approved Gate 21.
Scope: `CLAUDE.md` §1 steps 1–4. No stage was started. Nothing was imported, deployed or containerised.

**Method.** Every figure below was recomputed directly from the artifacts in this session. Where a report
makes a claim, the claim was re-derived independently and the two are compared. Where they disagree, the
artifact is recorded as authoritative and the report is recorded as the divergent party. All checks ran with
`PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `sys.stdout` reconfigured to UTF-8, and every file opened
`encoding="utf-8", errors="strict"`. No assertion was narrowed, substring-matched or ASCII-folded.

---

## 1. Integrity verification (step 1) — PASS

All six hashes match the Gate 21 table in `CLAUDE.md` §1 exactly. No immutable file has changed.

**Emitted one field per line.** A 64-character SHA-256 does not survive a fixed-width table without
abbreviation, and an abbreviated hash is not a hash. Per `CODEX-BUILD-2.1.md` §3 rule 8 and §3.1, the
format yields to the assertion, never the reverse. No value below is elided, wrapped or shortened.

```text
FILE 1 of 6
  path      camden-concreting-import.xml
  bytes     10169943
  expected  A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  computed  A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  result    MATCH

FILE 2 of 6
  path      eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
  bytes     2797640
  expected  45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  computed  45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  result    MATCH

FILE 3 of 6
  path      build/stage9-page-manifest.json
  bytes     30742
  expected  578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  computed  578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  result    MATCH

FILE 4 of 6
  path      build/stage8-image-map.json
  bytes     48862
  expected  0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  computed  0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  result    MATCH

FILE 5 of 6
  path      reports/08-image-rename-map.csv
  bytes     40516
  expected  43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  computed  43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  result    MATCH

FILE 6 of 6
  path      CODEX-BUILD-2.1.md
  bytes     32753
  expected  BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  computed  BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  result    MATCH

SUPPLEMENTARY (not in the mandatory six)
  path      archive/governing/CODEX-BUILD-2.md
  bytes     19367
  expected  E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5
  computed  E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5
  source    reports/21-governing-doc-diff.md
  result    MATCH

SUMMARY  6 of 6 mandatory files MATCH; 0 mismatches; 0 missing.
```

The archived instruction has not drifted since restoration.

---

## 2. What exists on disk

### Present and parsing

| Artifact | State |
|---|---|
| `camden-concreting-import.xml` | 306 `<item>` elements: 156 `page`, 83 `attachment`, 65 `nav_menu_item`, 1 `elementor_library`, 1 `custom_css`. Well-formed. Every page's `_elementor_data` parses as JSON. |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | Present, well-formed, unmodified. Also duplicated at `source/`. |
| `build/21-spec-ledger.json` | 42 citation definitions, 41 used, 161 `source_refs` occurrences, 0 undefined. Totals 157. |
| `build/stage9-page-manifest.json` | 156 records, fields `page_type / post_id / post_name / post_parent / status / url`. |
| `build/stage8-image-map.json` | 83 records, keyed by attachment ID. |
| `reports/08-image-rename-map.csv` | 83 data rows, header `attachment_id, old_filename, new_filename, pages_referencing`. |
| `intersection-differentiators.json` | 35 intersections. |
| `suburbs-expanded.json` | 60 suburbs. |
| `suburbs.json` | **16** suburb records (see §4.4). |
| `reports/18-page-readiness.csv` | 156 rows, all `Index-ready: no`. |
| `reports/placeholders.md` | Register recording 163 = 111 `PLACEHOLDER` / 47 `REAL_PHOTO_PENDING` / 5 `VERIFY`. |
| `scripts/21-encoding-canary.py`, `tests/fixtures/encoding-canary.txt` | Present. Canary re-run this session: **PASS**, exit 0. |
| `archive/governing/CODEX-BUILD-2.md` | Present, restored, provenance only. Sole file under `archive/`. |
| `staging/` | Disposable environment definition only (`docker-compose.yml`, `Dockerfile`, `README.md`, `.gitignore`). Not started. |
| All 22 files in `CONTEXT.md`'s source-of-truth list | All PRESENT. |

### Absent — and expected to be absent

- `camden-calculator-import.xml` — correct; Stage 31 has not run.
- `source-inputs/media/`, `source-inputs/astra/` — correct; Stage 22 has not started.
- `scripts/22-*` through `scripts/32-*`, `staging-authoritative/`, `data/verified-facts.yml`,
  `data/council-specs.yml` — correct; Stages 22–32 have not started.
- Amendment A / B / C files — never existed on disk; consistent with `reports/21-governing-doc-diff.md`.

### Absent — and NOT expected to be absent

- **`DECISION-01-gate21.md` does not exist anywhere in the repository.** No file with `decision` in its
  name exists. No artifact cites it. This is the hard finding of this session; see §5.

---

## 3. Report claims re-verified against the artifacts

Every claim below was independently recomputed. All of these **confirm**.

| Report | Claim | Independent result |
|---|---|---|
| `21-reconciliation-v2.md` | Manifest vs main XML: exact match, zero divergence across 156 pages | **CONFIRMED.** 0 divergences across post ID, slug, parent ID, status and served path. |
| `21-reconciliation-v2.md` | Per-class manifest/XML: 1 home, 4 utility, 10 service, 60 suburb, 35 intersection, 1 guide hub, 35 guide, 10 cost | **CONFIRMED** exactly. |
| `21-reconciliation-v2.md` | 21 publish / 135 draft in the main WXR | **CONFIRMED** in both manifest and XML. |
| `21-reconciliation-v2.md` | Ledger reconciles to 157; artifacts to 156; single expected supplementary asymmetry | **CONFIRMED.** Ledger `resolved_totals.total = 157`, `artifact_split` 156 + 1 planned. |
| `21-citation-remap.md` | 16 remapped keys covering 75 `source_refs` | **CONFIRMED.** Sum over the 16 keys = exactly 75. |
| `21-citation-remap.md` | 0 undefined refs; 42 definitions; 41 used; `SEO-6` the only unused | **CONFIRMED**, all four. |
| `21-citation-remap.md` | No stale governing citation remains outside the provenance table | **CONFIRMED.** Zero occurrences of `CODEX-BUILD-2.md` or `Amendment A/B/C` in the ledger. |
| `21-encoding-audit.md` | `lib/stage20_crawl.py` decoder now strict | **CONFIRMED.** `.decode("utf-8", errors="strict")`. |
| `21-encoding-audit.md` | Only two dispositioned residuals remain (`lib/stage8.py:475`, `lib/wxr.py:58`) | **CONFIRMED.** An independent 18-script sweep for `errors='ignore'`/`'replace'`, `unicodedata.normalize`, `.isascii()`, `encode('ascii')` and character stripping found exactly those two and nothing else. |
| `21-encoding-audit.md` | `lib/stage3_gate.py` `repair_text` is contained legacy mutation, not a gate | **CONFIRMED.** Present at lines 57–64, called only by the Stage 3 repair path. |
| `21-encoding-audit.md` | Canary and both restored full-fidelity assertions pass | **CONFIRMED** by re-running `scripts/21-encoding-canary.py` this session. Exit 0. |
| `21-governing-doc-diff.md` | Restored archive is 19,367 bytes, SHA-256 `E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5` | **CONFIRMED**, exactly. |
| `21-module-crosswalk.md` | 11 built modules; noindex gate restated against built 3/5/11 and 8 | Internally consistent and content-derived. Not re-derived from Elementor bodies this session; that is Stage 25/26 work. **Not disputed.** |
| `CONTEXT.md` | 83 attachments, 65 menu items, 1 Elementor kit, 1 Astra custom CSS record | **CONFIRMED**, all four. |
| `CONTEXT.md` | Victorian blocklist at zero | **CONFIRMED.** All 13 blocklist terms return 0 occurrences in the main WXR. |
| `CONTEXT.md` | Index-ready 0 of 157 | **CONFIRMED.** All 156 rows of `18-page-readiness.csv` are `no`; the 157th page does not exist. |
| `suburbs-expanded.json` derived figures | 15 researched / 45 `REQUIRED-RESEARCH`; tiers 6/9/21/24; legacy waves 6/9/45; import 6 publish / 54 draft | **CONFIRMED**, all four. |

---

## 4. Where the reports and the artifacts disagree

Trust the artifacts. Six items. None invalidates Gate 21's structural conclusions; three are material to
Stages 22–28 and must not be carried forward silently.

### 4.1 The Elementor image-reference figure of 1,085 is incomplete — MATERIAL

`CONTEXT.md` and `CODEX-BUILD-2.1.md` §4.28 both fix the count at **1,085 references across 83 attachments**.

Direct parse of every page's `_elementor_data`:

| Settings key | References |
|---|---:|
| `image` | **1,085** |
| `background_image` | **98** |
| **Total** | **1,183** |

The recorded 1,085 is exactly and only the `image` widget settings. There are a further **98
`background_image` references** that the figure does not cover. As written, the Stage 28 preflight gate
would count 1,085, pass, and never look at the 98. Those 98 resolve to 2 distinct attachment IDs, so a
missing binary there breaks section backgrounds site-wide without tripping the gate.

The subordinate claim "across 83 attachments" is also wrong on the artifact: `image` settings reference
**73** distinct attachment IDs, `background_image` adds no new ones, and `_thumbnail_id` is used by zero
pages. Union = **73 of 83**.

Not a divergence: the remaining **10** attachments (159, 177, 250, 308, 309, 422, 468, 469, 471, 472 — the
logo and site-identity PNGs) already carry an empty `pages_referencing` value in
`reports/08-image-rename-map.csv`. They are unreferenced by design because they are carried in theme mods —
i.e. in the Astra Customizer export, which is one of the two missing P0 inputs. All 83 binaries remain
required at Stage 22.

**Disposition:** do not edit the instruction. Record in the ledger at the appropriate gate that the
Stage 28 Elementor reference assertion is 1,085 `image` + 98 `background_image` = 1,183 across 73 of 83
referenced attachment IDs. Owner/approval decision required, because it changes a figure written into
`CODEX-BUILD-2.1.md` §4.28.

### 4.2 Three unregistered `VERIFY` instructions sit in live body copy — MATERIAL

`reports/placeholders.md` records 5 `VERIFY` occurrences. The main WXR contains **8**.

- 5 are bracketed markers of the form `[[VERIFY: ...]]` — these are the 5 in the register. Arithmetic is
  correct.
- 3 are **bare, unbracketed** uses of the word inside rendered Bringelly copy.

All 8 are emitted below in full. No sentence is elided, and each is given as extracted from the WXR after
XML-entity unescaping. Where the stored form is a JSON `\uXXXX` escape it is shown as stored; `—`
decodes to an em dash and the escaping is reversible (see `reports/21-encoding-audit.md` on
`lib/wxr.py:58`).

```text
BARE-VERIFY 1 of 3  — unregistered
  The Bringelly research brief assigns postcode 2556, authority VERIFY — Liverpool City Council /
  Camden Council boundary and primary query concreters bringelly.

BARE-VERIFY 2 of 3  — unregistered
  The verified approval path for Bringelly is: VERIFY the governing LGA per lot on the NSW Planning
  Portal before quoting.

BARE-VERIFY 3 of 3  — unregistered
  For Bringelly, the verified project record says: VERIFY the governing LGA per lot on the NSW Planning
  Portal before quoting.

REGISTERED-VERIFY 1 of 5  — in reports/placeholders.md
  [[VERIFY: confirm whether the Oran Park estate design guidelines require the driveway to be complete
  before the Occupation Certificate is issued — check the current Oran Park Estate Design
  Guidelines before publishing this claim.]]

REGISTERED-VERIFY 2 of 5  — in reports/placeholders.md
  [[VERIFY: any unresearched figure or process stated under Camden Council Driveway Crossing before
  publication]]

REGISTERED-VERIFY 3 of 5  — in reports/placeholders.md
  [[VERIFY: current Campbelltown City Council vehicle-crossing specification, application, fees,
  inspections, widths and grades before this guide is published]]

REGISTERED-VERIFY 4 of 5  — in reports/placeholders.md
  [[VERIFY: current Liverpool City Council vehicle-crossing specification, application, fees,
  inspections, widths and grades before this guide is published]]

REGISTERED-VERIFY 5 of 5  — in reports/placeholders.md
  [[VERIFY: current Wollondilly Shire Council vehicle-crossing specification, application, fees,
  inspections, widths and grades before this guide is published]]
```

The three bare occurrences are evidence gaps that would render to a visitor as literal instruction text,
and because they carry no `[[` `]]` delimiter, a marker-scanning gate keyed on the bracket form will not
see them. Two of the three are additionally worded as though a verification had already occurred — *"The
verified approval path for Bringelly is: VERIFY the governing LGA per lot"* — which is the exact failure
mode standing rule 1 exists to prevent: an unverified fact presented in the grammar of a verified one.

**Disposition:** Stage 23 §4.23.2 already requires reporting rather than silently reconciling a count
difference. Carry these three forward as blocking rows. Do not amend the register in this session.

### 4.3 Four `REQUIRED-RESEARCH` strings are inside the WXR body copy, not just the data file — MATERIAL

`CODEX-BUILD-2.1.md` §4.23.3 treats `REQUIRED-RESEARCH` as a field in `suburbs-expanded.json`. The main WXR
additionally contains **4** literal `REQUIRED-RESEARCH` strings in rendered page copy. All four are emitted
below in full, no elision:

```text
REQUIRED-RESEARCH 1 of 4  — Leppington
  The recorded Leppington council specification is reproduced without alteration: REQUIRED-RESEARCH:
  confirm Liverpool City Council vehicle crossing specification, widths, strength and fee schedule at
  liverpool.nsw.gov.au.

REQUIRED-RESEARCH 2 of 4  — Austral
  The recorded Austral council specification is reproduced without alteration: REQUIRED-RESEARCH:
  confirm Liverpool City Council vehicle crossing specification, widths, strength and fee schedule at
  liverpool.nsw.gov.au.

REQUIRED-RESEARCH 3 of 4  — Bringelly
  The recorded Bringelly council specification is reproduced without alteration: REQUIRED-RESEARCH:
  confirm Liverpool City Council vehicle crossing specification, widths, strength and fee schedule at
  liverpool.nsw.gov.au.

REQUIRED-RESEARCH 4 of 4  — Edmondson Park
  The recorded Edmondson Park council specification is reproduced without alteration: REQUIRED-RESEARCH:
  confirm Liverpool City Council vehicle crossing specification, widths, strength and fee schedule at
  liverpool.nsw.gov.au.
```

Each of the four names a council specification as "reproduced without alteration" while the specification
itself is absent — the sentence asserts fidelity to a figure that was never supplied. All four are
Liverpool City Council. None may be filled from a neighbouring suburb or another LGA.

All four sit on pages whose class the ledger treats as researched. They are not in the 163-marker register
and are not in the 45 unresearched-suburb set. Stage 23 must pick them up from both sources.

### 4.4 `suburbs.json` holds 16 records, not the 15 the reports imply — MINOR, but a build-safety flag

`build/21-spec-ledger.json` `authority_order` says "suburbs.json for the 15 researched suburbs' deep
content", and `21-reconciliation-v2.md` finding 3 says 15 researched. `suburbs-expanded.json` does mark
exactly 15 as `COMPLETE — see suburbs.json`.

`suburbs.json` itself contains **16**. The extra record is **Camden**. Expansion §2 (ledger `EXP-2`)
deliberately excludes Camden from the suburb list, and §2 of the governing instruction forbids
`/concreters-camden/` and `/concreters-camden-town/` outright.

So the "15" figure is a count of researched *expanded-list* records, not of `suburbs.json` rows, and the
documents never say so. The risk is a later stage iterating `suburbs.json` and producing a 61st suburb page
on a forbidden URL. Flagging it here; no artifact change.

### 4.5 `reports/18-page-readiness.csv` carries a UTF-8 BOM — MINOR, but a Stage 23 trap

Unlisted conflict 17 correctly records that the file has no page-ID column and that Stage 23 must derive the
ID by exact URL through the manifest. Additionally: the file is UTF-8 **with BOM**, so its first column
parses as `﻿URL` under a strict UTF-8 read. A strict join on `URL` will fail on every row unless the
reader uses `utf-8-sig`. Given the §3.1 prohibition on `errors='ignore'`/`'replace'`, the correct fix is the
`utf-8-sig` codec, not error suppression.

### 4.6 Gate 21's own state is recorded two different ways — the central contradiction

| Source | Gate 21 state |
|---|---|
| `reports/21-reconciliation-v2.md`, final line | **"GATE 21: BLOCKED — owner direction is required before Stage 22."** |
| `CONTEXT.md` §Current stage | Gate 21 **blocked** by the Stage 23/25/28-versus-31 instruction-order conflict |
| `CONTEXT.md` §Immediate blockers | That conflict is the **sole P0 before Stage 22** |
| `CLAUDE.md` §2 | "Stage 21 complete and **approved** subject to D1–D9" |

`CLAUDE.md` also states the mechanism by which the artifacts' blocker was cleared: D1 declined a 31A/31B
split and fixed the stage order as unchanged. That resolution is not present in any artifact. The
reconciliation report still carries unlisted conflict 14 as `UNRESOLVED — HARD BLOCKER`, and `CONTEXT.md`
still names it as the next required owner decision.

Per the standing instruction, the artifacts win: **on disk, Gate 21 is BLOCKED.** The approval exists only
in the handoff narrative and in a decision file that does not exist.

---

## 5. Was `DECISION-01-gate21.md` applied? (step 3)

**No — and it cannot be applied, because the file is not in the repository.**

The test `CLAUDE.md` §1.3 prescribes: *"assume it was not applied unless the ledger shows citations to
`DECISION-01` for each of D1–D9."*

- Occurrences of the string `DECISION-01` in `build/21-spec-ledger.json`: **0**.
- Occurrences of `DECISION-01` in any workspace file other than `CLAUDE.md` itself: **0**.
- Files matching `*decision*` anywhere in the repository: **none**.
- The ledger's 42 citation definitions resolve to `CODEX-BUILD-2.1.md`, the six source data documents,
  `CODEX-BUILD.md` and the main WXR. No decision record is among them.

### Status of D1–D9

| Clause | Content known to me | Reflected in artifacts? |
|---|---|---|
| **D1** | Known only in paraphrase, from `CLAUDE.md` §2: the proposed 31A/31B split was **declined**; stage order stays 21 → 22 → 23 → 24 → 25 → 26 → 27 → 28 → 29 → 30 → 31 → 32, sequential and unchanged. | **NOT APPLIED.** `21-reconciliation-v2.md` conflict 14 still reads `UNRESOLVED — HARD BLOCKER`; `CONTEXT.md` still lists the sequencing conflict as the sole P0 before Stage 22 and as the safest next action. |
| **D2–D9** | **Unknown.** No text, summary or paraphrase of these clauses exists in any file I can read. | **CANNOT BE DETERMINED.** Absence of a `DECISION-01` citation means, by the prescribed test, not applied — but I cannot state what they required, so I cannot state what applying them would change. |

---

## 6. Step 4 — what is delivered and what is blocked

**Blocked:** applying D1–D9 and printing Codex's owed D1–D9 confirmation report.

Reason, stated against the governing rules rather than as a preference:

- The decision text does not exist on disk. Reconstructing D2–D9 would be inventing the content of an
  owner decision record — the same class of act as inventing a council fee, and prohibited by
  `CODEX-BUILD-2.1.md` §3 rules 1 and 10 and `CLAUDE.md` §3.6.
- Even D1, whose substance is paraphrased in `CLAUDE.md`, cannot be entered into the ledger from that
  paraphrase. §3 rule 7 requires every ledger resolution to cite the clause that produced it; the citation
  target `DECISION-01-gate21.md` §D1 is unresolvable. `CLAUDE.md` §3.8 forbids treating a handoff note as
  the decision record. The correct mechanism, per §3 rule 7, is that the decision arrives as a numbered
  decision-record file — which is precisely what is missing.
- Applying an unresolvable citation would make the ledger assert a resolution with no verifiable source.
  That is the failure mode the ledger exists to prevent.

**Delivered in full** (it does not depend on the decision file): the resolution register for the 18
unlisted conflicts, below.

---

## 7. Resolution register — the 18 unlisted conflicts found at Gate 21

One line each. Resolutions are as recorded in `reports/21-reconciliation-v2.md`; citations are the clause or
ledger key that produced each resolution. Verified this session against the artifacts where the resolution
is artifact-checkable.

**Emitted one field per line.** Three of these entries do not fit a fixed-width table without losing the
end of the citation, and a resolution without its full citation is exactly the thing the ledger exists to
prevent. No field below is elided or shortened.

```text
CONFLICT 1
  conflict    CODEX-BUILD.md names 3 utilities (Contact, Quote, About); the structure and expansion
              documents and the artifact all include Gallery.
  resolution  Four utilities. Gallery stays evidence- and photography-gated at noindex,follow.
  citation    ledger EXP-1, WXR-UTILITY, WXR-ACTUAL; CODEX-BUILD-2.1.md §3 rule 4 (ledger B2-HARD-4)

CONFLICT 2
  conflict    The earlier build plan describes guides as published in the import; the expansion wave
              rule and the actual WXR hold them as drafts.
  resolution  Hub and all 35 guides remain draft. The hub never publishes alone.
  citation    ledger EXP-7, WXR-ACTUAL, B2-STAGE27; CODEX-BUILD-2.1.md §4.27.3

CONFLICT 3
  conflict    Earlier architecture describes 15 built suburbs; the expansion and the WXR contain 60.
  resolution  60 suburb artifacts, of which 15 carry researched deep content and 45 are held research
              shells.
  citation    ledger SUBEXP-LIST, EXP-2, WXR-ACTUAL

CONFLICT 4
  conflict    Expansion §8 says a failing page is not written, while expansion §10 and standing rule 2
              require draft + noindex shells.
  resolution  Standing rule 2 wins. Shells exist, stay non-live, and fail readiness.
  citation    CODEX-BUILD-2.1.md §3 rule 2 (ledger B2-HARD-2)

CONFLICT 5
  conflict    suburbs-expanded.json assigns legacy waves to all 60 suburbs, including the 45
              REQUIRED-RESEARCH records; §4.27 forbids those 45 from every wave.
  resolution  The 45 have no operative wave until research passes.
  citation    CODEX-BUILD-2.1.md §4.27.3 (ledger B2-STAGE27); ledger SUBEXP-WAVES

CONFLICT 6
  conflict    The structure document's link Rule A says "all seven services" after the service count
              resolved to ten.
  resolution  "All services" means all ten resolved service pages, for future menu and link planning.
  citation    CODEX-BUILD-2.1.md §2 service-page count (ledger B2-PRECEDENCE-SERVICES); ledger EXP-3

CONFLICT 7
  conflict    The structure document proposes varying module order; the clone contract and standing
              rule 6 prohibit changing an Elementor layout.
  resolution  Layout preservation wins. No module reordering.
  citation    CODEX-BUILD-2.1.md §3 rule 6; codex-clone-prompt.md

CONFLICT 8
  conflict    The SEO specification asks for original per-page imagery; expansion §9 and Stage 24
              assume controlled reuse of a shared pool.
  resolution  Controlled generic reuse is permitted, but no source-site image may occupy a
              REAL_PHOTO_PENDING slot or be represented as Camden work.
  citation    CODEX-BUILD-2.1.md §3 rule 3; §4.24.4; expansion-300-pages.md §9

CONFLICT 9
  conflict    The structure document says place media in final uploads before the WXR import; Stage 15
              proved WordPress may suffix colliding filenames.
  resolution  Later tested evidence wins. Use the future local-only importer and audit exact filenames.
  citation    reports/15-import-verification.md; CODEX-BUILD-2.1.md §4.29.2

CONFLICT 10
  conflict    The structure document says re-enter schema manually; Stage 30 requires a deterministic
              fail-closed builder.
  resolution  The more specific current instruction wins. Builder only.
  citation    CODEX-BUILD-2.1.md §4.30.2

CONFLICT 11
  conflict    SEO §7 omits LocalBusiness without a verified staffed address, but suburb Service nodes
              reference #localbusiness and §7.6 forbids undefined @id values.
  resolution  Dependent references and nodes are omitted whenever #localbusiness cannot be emitted, and
              every omission is logged with its reason.
  citation    CODEX-BUILD-2.1.md §4.30.2 and §4.30.3; camden-concreting-seo-spec.md §7 and §7.6

CONFLICT 12
  conflict    Home, Utility, Guide hub, generic Guide and Cost/comparison have no complete normative
              module contract in any source document.
  resolution  Artifact-observed shapes are labelled as contract_status observations and never silently
              promoted to rules. Structural mutation remains prohibited.
  citation    ledger page_classes[].module_template.contract_status; CODEX-BUILD-2.1.md §3 rule 6

CONFLICT 13
  conflict    Stage 25 says 26 unthresholded pages; the listed classes total 27
              (10 service + 11 cost/comparison + 1 guide hub + 1 home + 4 utility).
  resolution  Explicit class counts and the 157 total win. Stage 25 must report 27 such pages.
  citation    CODEX-BUILD-2.1.md §4.21.6 and §2 total page count; ledger resolved_totals.
              Arithmetic re-verified against the ledger this session.

CONFLICT 14
  conflict    Stages 23, 25 and 28 each require the supplementary calculator before §4.11 authorises
              its construction, and no gate may be narrowed or skipped.
  resolution  UNRESOLVED - HARD BLOCKER. Owner direction required. CLAUDE.md states D1 resolved this by
              declining a 31A/31B split; that resolution is present in no artifact, and its source file
              DECISION-01-gate21.md does not exist in the workspace.
  citation    CODEX-BUILD-2.1.md §4.23.5, §4.25.5, §4.28, §4.11.2; §3 rule 8 forbids narrowing the
              157-page assertions to escape the ordering problem.

CONFLICT 15
  conflict    Stage 25 says no sourced threshold exists for five classes, while §2 sources a 40%
              within-class pairwise overlap cap globally.
  resolution  The global pair cap is already sourced and is enforced now. Only the class-specific
              unique-body-word percentage stays AWAITING APPROVAL - not enforced.
  citation    ledger B2-PRECEDENCE-UNIQUE, EXP-8; CODEX-BUILD-2.1.md §4.25.6

CONFLICT 16
  conflict    Current index-ready is 0, yet Stage 27 specifies a Wave 1 effective indexable count of 14.
  resolution  Stage 27 is a conditional release plan, not a current-state mutation. No page becomes
              index-ready in this work block.
  citation    CODEX-BUILD-2.1.md §3.2 and §3 rule 4 (ledger B2-HARD-4); §4.27.2

CONFLICT 17
  conflict    Stage 23 requires joining reports/18-page-readiness.csv on page ID, but that file has no
              page-ID column.
  resolution  Derive the page ID by exact URL through the Stage 9 manifest, add a Page ID column to the
              v2 superset, and fail on any missing or non-unique URL match. EXTENDED THIS SESSION per
              §4.5 above: the CSV carries a UTF-8 BOM and must be read with the utf-8-sig codec, not
              with an error-suppressing decode.
  citation    CODEX-BUILD-2.1.md §4.23.5; build/stage9-page-manifest.json; §3.1 on decoder fidelity

CONFLICT 18
  conflict    Stage 31 is numbered §4.11 and appears after Stage 30.
  resolution  Resolved for provenance only. Citations use the exact supplied identifier §4.11. No
              instruction file is edited to renumber it.
  citation    CODEX-BUILD-2.1.md §4.11 heading; §3 rule 7
```

Three further conflicts surfaced in this session's artifact re-verification and are **not** among the 18.
They are recorded in §4.1, §4.2 and §4.3 above and are new findings, not resolutions.

---

## 8. `CONTEXT.md` update and diff

Additive only. No blocker was removed, no count changed, no page became index-ready, and the Gate 21
BLOCKED state was not altered.

| Field | Before | After |
|---|---|---|
| Last updated | 18 August 2026 | 18 August 2026 (unchanged date; handoff verification appended) |
| P0 before Stage 22 | 1 item — the Stage 23/25/28-versus-31 sequencing conflict | 2 items — that conflict, **plus** `DECISION-01-gate21.md` absent from the workspace |
| Source-of-truth list | 22 entries | 23 entries — adds `reports/handoff-state.md` |
| Index-ready | 0 of 157 | **0 of 157 — unchanged** |
| Launch state | NO-GO | **NO-GO — unchanged** |
| Owner-supplied import blockers | 83 image binaries; Astra Customizer export | **Unchanged; neither cleared** |
| Gate 21 | BLOCKED | **BLOCKED — unchanged** |

Nothing in this session was performed against a live site, a container, or a real import. No WXR was
modified. Docker was not started.

---

## 9. DECISION-02 (D10–D14) — application record

`DECISION-02-evidence-markers.md` was supplied in conversation and **written to disk first**, before any
clause was acted on. DECISION-01 was supplied the same way and never reached disk, which is why D1–D9 are
unrecoverable; that failure is not repeated here.

```text
  path      DECISION-02-evidence-markers.md
  bytes     4423
  sha256    (see §10 read-back table)
  status    read-only from this point; cited in build/21-spec-ledger.json as DEC02-D10..DEC02-D14
```

### D10 — register undercount — APPLIED, and independently confirmed

Corrected in `CONTEXT.md` and in the ledger under `evidence_markers`, with the arithmetic shown:
**163 recorded + 4 + 3 = 170.**

An independent scan of the rendered body copy of all 156 pages returned **exactly 170**:

```text
  token                bracketed [[...]]   bare   corpus total   register
  PLACEHOLDER                        111      0            111        111
  REAL_PHOTO_PENDING                  47      0             47         47
  VERIFY                               5      3              8          5
  REQUIRED-RESEARCH                    0      4              4          0
  TOTAL                              163      7            170        163

  divergence scanned vs recorded = +7, reported not reconciled
```

D10's working total is confirmed without adjustment. D10.2–D10.4 are Stage 23 forward-plan items and are
recorded in the ledger's `deferred_validation` block, including the §4.23.1 method amendment making the
corpus the source and `reports/placeholders.md` a cross-check.

### D11 — false-fidelity claims — APPLIED; scan found more than D11 anticipated

`reports/23-false-fidelity.md` written. **6 instances across 4 pages**, not 4. D11 anticipated four; two
further instances exist on Bringelly, of a construction D11 did not describe:

- *"The verified approval path for Bringelly is: VERIFY the governing LGA per lot on the NSW Planning
  Portal before quoting."*
- *"For Bringelly, the verified project record says: VERIFY the governing LGA per lot on the NSW Planning
  Portal before quoting."*

Both are **unfillable**. No supplied value makes *"the verified project record says: VERIFY"* a true
sentence, and the second additionally claims a completed project record exists — two unverified assertions
in one sentence, against standing rule 1. They require rewriting regardless of what the owner supplies.

**A first pass returned 51 and was wrong.** It walked the whole Elementor settings tree, pulling CSS and
widget IDs into the "body copy", and it counted `[[PLACEHOLDER: verified CoreX ABN]]` as a fidelity claim.
That marker correctly *requests* a verified value; it does not assert one. The corrected method strips
`[[...]]` markers and tests only the surrounding prose. 51 was an artifact of method and is discarded.

Campbelltown and Wollondilly appear in no false-fidelity sentence. All four council-specification
instances are Liverpool.

### D12 — Liverpool is one owner task unblocking four pages — APPLIED

Recorded in the ledger as `liverpool_specification_dependency` with the four pages named, the prohibition
on sourcing from another LGA, Leppington's second independent reason (Camden/Liverpool boundary split per
`intersection-differentiators.json`), and the Stage 31 `data/council-specs.yml` cross-dependency so the
figures are neither researched twice nor satisfied twice with different numbers.

### D13 — two of the four are Wave 1 — APPLIED, and D13.2 confirmed rather than assumed

Verified against the artifacts: Leppington and Austral are both `publish` and both Tier 1, inside the
21-page Wave 1 release set. The six Tier 1 suburbs are Oran Park, Gregory Hills, Gledswood Hills,
Harrington Park, Austral and Leppington.

```text
  21  pages at publish status in the main WXR (Wave 1 release set)
  -6  Tier 1 suburb pages held noindex,follow
  -1  Gallery held noindex,follow
  =14 effective indexable

  Leppington and Austral are inside the already-held Tier 1 six. The Liverpool
  specification is a SECOND, independent hold on pages that were already held.
  It removes nothing from the indexable set.
  => 14 is unchanged. CONFIRMED against the artifacts, not assumed.
```

### D14 — standing guidance placement — CONFIRMED AND CORRECTED

**What was written, and where.** The previous turn wrote exactly two files, both **outside this
repository**, in the agent-local memory directory:

```text
  C:\Users\Home\.claude\projects\C--Users-Home-Documents-concreters-camden\memory\MEMORY.md
  C:\Users\Home\.claude\projects\C--Users-Home-Documents-concreters-camden\memory\reports-to-disk-then-read-back.md
```

Their content is the full-fidelity reporting rule: write reports to disk, read back, never abbreviate a
value to fit a table, confirm byte counts.

**No instruction document was modified.** `CODEX-BUILD-2.1.md` and `archive/governing/CODEX-BUILD-2.md`
both still hash to their recorded baselines (§1 and §10). `CLAUDE.md` and `CODEX-BUILD.md` were read only
and never opened for write; baseline hashes for both are now recorded in §10 so future sessions have the
comparison that was missing for `CODEX-BUILD-2.md`. No decision record was appended to. Nothing needs
restoring.

**Correction applied.** Agent-local memory is neither the ledger nor a numbered report, so the guidance was
not where D14 requires it. It is now recorded in `build/21-spec-ledger.json` under `standing_guidance`,
citing `DEC02-D14`, together with an explicit disclaimer that the out-of-repo memory file carries no
authority, is not a project artifact, and may not be cited by any gate. The ledger entry is authoritative.

---

## 10. Next safe action

Supply `DECISION-01-gate21.md` as a file in the workspace. Steps 3 and 4 of `CLAUDE.md` §1 resume the moment
it exists, and Gate 21 can then be closed against a citable source. Nothing else in Stages 22–32 should
begin before that, because D1 fixes the stage order that all of them run in.

Alongside it, three items above need an owner ruling because they change figures written into the governing
instruction or the marker register: the 1,085-versus-1,183 Elementor reference count (§4.1), the three
unregistered bare `VERIFY` strings in Bringelly copy (§4.2), and the four in-copy `REQUIRED-RESEARCH`
strings (§4.3).
