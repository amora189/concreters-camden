# GATE 21 — confirmation report

Date: 18 August 2026 (Australia/Sydney).
Authority: `RUN-BLOCK-01.md` §0 and §A (D1–D9), `DECISION-02-evidence-markers.md` (D10–D14).

This is the confirmation report Codex owed and could not print, because D1–D9 existed only in conversation.
`RUN-BLOCK-01.md` §A now carries them and is the authoritative record; `DECISION-01-gate21.md` is still
absent from the repository and, if it later appears, is a duplicate that must agree in substance.

All values below are emitted one field per line where a table would abbreviate them.

---

## 1. Preconditions

### 1.1 Immutable file hashes

```text
FILE 1 of 7
  path      camden-concreting-import.xml
  expected  A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  computed  A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
  result    MATCH

FILE 2 of 7
  path      eamptcoconcretersmelbourne_WordPress_2026-08-14.xml
  expected  45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  computed  45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
  result    MATCH

FILE 3 of 7
  path      build/stage9-page-manifest.json
  expected  578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  computed  578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
  result    MATCH

FILE 4 of 7
  path      build/stage8-image-map.json
  expected  0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  computed  0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
  result    MATCH

FILE 5 of 7
  path      reports/08-image-rename-map.csv
  expected  43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  computed  43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
  result    MATCH

FILE 6 of 7
  path      CODEX-BUILD-2.1.md
  expected  BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  computed  BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
  result    MATCH

FILE 7 of 7
  path      archive/governing/CODEX-BUILD-2.md
  expected  E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5
  computed  E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5
  result    MATCH

VERDICT  7 of 7 MATCH, 0 mismatches. Stop condition C1 not triggered.
```

### 1.2 D10–D14 applied and cited

```text
  DEC02-D10  defined; cited 5 times   marker undercount, working total 170, corpus-scan method
  DEC02-D11  defined; cited 2 times   false-fidelity claim category
  DEC02-D12  defined; cited 3 times   Liverpool = one question unblocking four pages
  DEC02-D13  defined; cited 3 times   Wave 1 gate, effective indexable 14 unchanged
  DEC02-D14  defined; cited 2 times   standing guidance placement
  undefined source_refs in ledger: none
```

### 1.3 D1–D9 applied and cited

```text
  RB01-D1  stage ordering 21..32, split declined; per-stage calculator handling
  RB01-D2  schema provider omission ladder; zero dangling @id is build-failing
  RB01-D3  unthresholded classes = 27, of which 26 built
  RB01-D4  readiness join on normalised slug; post_id column added
  RB01-D5  module order frozen; mitigation 4 NOT APPLIED as residual footprint risk
  RB01-D6  link Rule A covers 10 services; asserted at Stage 27
  RB01-D7  image reuse permitted; REAL_PHOTO_PENDING slots are not
  RB01-D8  items accepted, plus module-contracts gap, item 16 reclassified, §4.31 renumber
  RB01-D9  semantic restoration accepted; byte-exact restoration not claimed
  RB01-C   eight stop conditions

  ledger citation definitions   57
  undefined source_refs         none
  clause map                    §4.31 canonical, §4.11 retained as alias
```

### 1.4 UTF-8 canary

```text
  PASS — UTF-8 canary survived an exact read-write-compare cycle
  PASS — exact instruction assertion: ## 4.25 — Stage 25: uniqueness enforcement
  PASS — exact report assertion: PASS — 157 combined (156 main + 1 planned supplementary)
  exit 0. Stop condition C3 not triggered.
```

---

## 2. Class table reconciling to 157 / 156

```text
  CLASS            combined spec   main manifest   main WXR   import state
  home                         1               1          1   1 publish
  utility                      4               4          4   4 publish; Gallery noindex,follow
  service                     10              10         10   10 publish
  suburb                      60              60         60   6 publish / 54 draft; all 60 noindex,follow
  intersection                35              35         35   35 draft + noindex,follow
  guide_hub                    1               1          1   1 draft + noindex,follow
  guide                       35              35         35   35 draft + noindex,follow
  cost_comparison             11              10         10   10 main drafts + 1 planned supplementary
  TOTAL                      157             156        156   21 publish / 136 draft combined
                                                              21 publish / 135 draft in main WXR

  Known-good asymmetry: 157 spec vs 156 artifact = exactly one planned supplementary
  calculator page. Expected under §4.31.1 and §4.31.7. Every other divergence would be
  stop-and-ask; none was found.
```

---

## 3. Three-way reconciliation

```text
  spec vs manifest     157 vs 156   one planned supplementary calculator; expected
  spec vs main XML     157 vs 156   same single planned page; expected
  manifest vs main XML 156 vs 156   EXACT MATCH — zero divergences across post_id, slug,
                                    parent_id, status and served path

  Re-verified this session by direct parse. Stop condition C2 not triggered.
```

---

## 4. Module crosswalk — noindex gate in built numbering

```text
  SEO module 6 (typical jobs & real price band) -> built modules 3, 5 and the price
                                                   portion of built module 11
  SEO module 7 (recent job + photos)            -> built module 8

  NOINDEX if (
    built module 3/5/11 contains unresolved SEO-module-6 job or price evidence
    OR built module 8 lacks verified recent-job evidence and real photos
    OR the suburb unique_local_variable is missing or unresearched
  )

  Mapping is content-derived. Mapping by built positions 6 and 7 would be wrong.
```

---

## 5. Resolution register — the 18 unlisted conflicts

One field per line. Resolutions incorporate D1–D9 where those clauses changed or confirmed an
earlier recorded resolution.

```text
CONFLICT 1
  conflict    CODEX-BUILD.md names 3 utilities (Contact, Quote, About); the structure and
              expansion documents and the artifact all include Gallery.
  resolution  Four utilities. Gallery stays evidence- and photography-gated at noindex,follow.
  citation    ledger EXP-1, WXR-UTILITY, WXR-ACTUAL; CODEX-BUILD-2.1.md §3 rule 4 (B2-HARD-4);
              accepted at RUN-BLOCK-01.md §A D8

CONFLICT 2
  conflict    The earlier build plan describes guides as published in the import; the expansion
              wave rule and the actual WXR hold them as drafts.
  resolution  Hub and all 35 guides remain draft. The hub never publishes alone.
  citation    ledger EXP-7, WXR-ACTUAL, B2-STAGE27; §4.27.3; accepted at RUN-BLOCK-01.md §A D8

CONFLICT 3
  conflict    Earlier architecture describes 15 built suburbs; the expansion and the WXR
              contain 60.
  resolution  60 suburb artifacts, of which 15 carry researched deep content and 45 are held
              research shells.
  citation    ledger SUBEXP-LIST, EXP-2, WXR-ACTUAL; accepted at RUN-BLOCK-01.md §A D8

CONFLICT 4
  conflict    Expansion §8 says a failing page is not written, while expansion §10 and standing
              rule 2 require draft + noindex shells.
  resolution  Standing rule 2 wins. Shells exist, stay non-live, and fail readiness.
  citation    CODEX-BUILD-2.1.md §3 rule 2 (ledger B2-HARD-2); accepted at RUN-BLOCK-01.md §A D8

CONFLICT 5
  conflict    suburbs-expanded.json assigns legacy waves to all 60 suburbs, including the 45
              REQUIRED-RESEARCH records; §4.27 forbids those 45 from every wave.
  resolution  The 45 have no operative wave until research passes.
  citation    CODEX-BUILD-2.1.md §4.27.3 (ledger B2-STAGE27), SUBEXP-WAVES; accepted at
              RUN-BLOCK-01.md §A D8

CONFLICT 6
  conflict    The structure document's link Rule A says "all seven services" after the service
              count resolved to ten.
  resolution  Rule A covers all TEN resolved service pages. Rules B through G are unchanged in
              scope. Stage 27 asserts that the homepage links to all ten.
  citation    RUN-BLOCK-01.md §A D6 (ledger RB01-D6); §2 service-page count
              (B2-PRECEDENCE-SERVICES); EXP-3

CONFLICT 7
  conflict    The structure document proposes varying module order (§7 mitigation 4); the clone
              contract and standing rule 6 prohibit restructuring an Elementor layout.
  resolution  Module order is FROZEN AS BUILT. Reorder nothing. Mitigation 4 is recorded NOT
              APPLIED and carried in CONTEXT.md as a residual footprint risk — shared section
              order with the source site — not as a task. Mitigation 5 (kit palette) checked
              and recorded identically.
  citation    RUN-BLOCK-01.md §A D5 (ledger RB01-D5); CODEX-BUILD-2.1.md §3 rule 6;
              codex-clone-prompt.md

CONFLICT 8
  conflict    The SEO specification asks for original per-page imagery; expansion §9 and Stage
              24 assume controlled reuse of a shared pool.
  resolution  Reuse permitted, subject to the ~15-page cap. "Original" means not stock and not
              byte-identical to the source site after re-encoding; it does not forbid reuse
              within the site. No REAL_PHOTO_PENDING slot may be filled by a re-encoded
              source-site image. Top-of-report item at Stage 24.
  citation    RUN-BLOCK-01.md §A D7 (ledger RB01-D7); CODEX-BUILD-2.1.md §3 rule 3; §4.24.4;
              expansion-300-pages.md §9

CONFLICT 9
  conflict    The structure document says place media in final uploads before the WXR import;
              Stage 15 proved WordPress may suffix colliding filenames.
  resolution  Later tested evidence wins. Use the local-only importer and audit exact filenames.
  citation    reports/15-import-verification.md; CODEX-BUILD-2.1.md §4.29.2; accepted at
              RUN-BLOCK-01.md §A D8

CONFLICT 10
  conflict    The structure document says re-enter schema manually; Stage 30 requires a
              deterministic fail-closed builder.
  resolution  The more specific current instruction wins. Builder only.
  citation    CODEX-BUILD-2.1.md §4.30.2; accepted at RUN-BLOCK-01.md §A D8

CONFLICT 11
  conflict    SEO §7 omits LocalBusiness without a verified staffed address, but suburb Service
              nodes reference #localbusiness and §7.6 forbids undefined @id values. Unresolved,
              the build emits references to an undefined @id on up to 140 pages.
  resolution  Resolve by OMISSION, never by emitting an undefined reference. Strict order:
              (1) #localbusiness defined -> Service.provider references it;
              (2) not defined but #organization defined from verified legal entity name plus
                  domain -> reference #organization;
              (3) neither defined -> Service omits provider entirely.
              Never invent an address. Never assert "CoreX Concreters Camden" as a legal
              entity. Build-failing check: zero references to any @id not defined in the same
              emitted graph. Report Service nodes omitting provider, per page class.
  citation    RUN-BLOCK-01.md §A D2 (ledger RB01-D2); CODEX-BUILD-2.1.md §4.30.2-3;
              camden-concreting-seo-spec.md §7, §7.6

CONFLICT 12
  conflict    Home, Utility, Guide hub, generic Guide and Cost/comparison have no complete
              normative module contract in any source document.
  resolution  Artifact-observed shapes remain contract_status observations, never silently
              promoted to rules. ADDITION: enumerate exactly which page classes lack a contract
              and what each is missing in reports/21-module-contracts-gap.md, proposing
              contracts marked "AWAITING APPROVAL — not enforced". Do not enforce an unapproved
              contract; do not treat its absence as a pass.
  citation    RUN-BLOCK-01.md §A D8 (ledger RB01-D8); ledger
              page_classes[].module_template.contract_status; §3 rule 6

CONFLICT 13
  conflict    Stage 25 says 26 unthresholded pages; the listed classes total 27.
  resolution  27. Arithmetic: 10 service + 11 cost/comparison + 1 guide hub + 1 homepage +
              4 utility = 27, of which 26 are currently built. The §4.25.5 figure of 26 was an
              arithmetic error. Everything else in §4.25.5 stands.
  citation    RUN-BLOCK-01.md §A D3 (ledger RB01-D3); §4.21.6; ledger resolved_totals

CONFLICT 14
  conflict    Stages 23, 25 and 28 each require the supplementary calculator before §4.31
              authorises its construction, and no gate may be narrowed or skipped.
  resolution  RESOLVED. The 31A/31B split is DECLINED. Ordering stays 21 through 32 sequential
              and unchanged. Stage 28 cannot return GO in this block under any ordering because
              the media and Astra inputs are absent, so front-loading Stage 31 buys nothing at
              the gate it was meant to unblock; and building page copy before Stage 25 exists
              means writing it without the index that judges it. Per-stage handling:
                23 -> readiness row, "Build status: not yet built — §4.31", Index-ready no
                24 -> denominator 157; calculator contributes zero image references, stated
                25 -> measure 156; calculator "DEFERRED TO STAGE 31 — not yet built"
                27 -> included in Wave 4 marked not-yet-built; effective counts unaffected
                28 -> runs against both XMLs; missing supplementary artifact is a genuine
                      NO-GO reason, never special-cased, suppressed or advisory
              A bounded delta pass (reports/31-delta.md) follows Stage 31 and is part of
              Gate 31. This conflict is no longer a blocker.
  citation    RUN-BLOCK-01.md §A D1 (ledger RB01-D1); §4.23.5, §4.25.5, §4.28, §4.31.2

CONFLICT 15
  conflict    Stage 25 says no sourced threshold exists for five classes, while §2 sources a
              40% within-class pairwise overlap cap globally.
  resolution  The global pair cap is already sourced and is enforced now. Only the
              class-specific unique-body-word percentage stays AWAITING APPROVAL - not enforced.
  citation    ledger B2-PRECEDENCE-UNIQUE, EXP-8; §4.25.6; accepted at RUN-BLOCK-01.md §A D8

CONFLICT 16
  conflict    Current index-ready is 0, yet Stage 27 specifies a Wave 1 effective indexable
              count of 14.
  resolution  RECLASSIFIED: this is NOT a conflict. 0 index-ready is present state; 14 is a
              conditional future Wave 1 count. Both are true simultaneously and must never be
              presented as alternatives to one another.
  citation    RUN-BLOCK-01.md §A D8 (ledger RB01-D8); §3.2 and §3 rule 4 (B2-HARD-4); §4.27.2

CONFLICT 17
  conflict    Stage 23 requires joining reports/18-page-readiness.csv on page ID, but that file
              has no page-ID column.
  resolution  Join on SLUG, normalised to leading-slash, trailing-slash and lowercase before
              comparison. Add post_id as a new column sourced from
              build/stage9-page-manifest.json. Report any slug in one file and not the other,
              and any slug not resolving to exactly one manifest entry — non-unique or
              unmatched is stop-and-ask, not best-effort. EXTENDED at handoff-state: the CSV
              carries a UTF-8 BOM and must be read with the utf-8-sig codec, never with an
              error-suppressing decode.
  citation    RUN-BLOCK-01.md §A D4 (ledger RB01-D4); §4.23.5; build/stage9-page-manifest.json;
              §3.1 on decoder fidelity

CONFLICT 18
  conflict    Stage 31 is numbered §4.11 and appears after Stage 30.
  resolution  Renumber Stage 31 from §4.11 to §4.31 in the ledger clause map, RETAINING §4.11
              as an alias so every existing citation continues to resolve. No instruction
              document is edited to renumber it; the clause map lives in the ledger.
  citation    RUN-BLOCK-01.md §A D8 (ledger RB01-D8, clause_map); §3 rule 7
```

### Register summary

```text
  total unlisted conflicts        18
  resolved                        17
  reclassified as not-a-conflict   1  (item 16)
  unresolved blockers              0  (item 14 resolved by D1)
  new obligations created          3  (item 12 -> 21-module-contracts-gap.md;
                                       item 11 -> provider omission ladder + dangling-@id gate;
                                       item 6  -> homepage-links-all-ten assertion at Stage 27)
```

Three further conflicts surfaced after Gate 21 and are recorded separately in
`reports/handoff-state.md` §4.1–4.3: the 1,085-versus-1,183 Elementor reference count, the three
unregistered bare `VERIFY` strings, and the four in-copy `REQUIRED-RESEARCH` strings. D10–D13 dispose of
the second and third. The first remains open and is carried into Stage 28.

---

## 6. Encoding integrity

```text
  scripts audited                          18
  lossy decoders remaining                  0
  dispositioned residuals                   2  (lib/stage8.py:475 ASCII slug generation,
                                                lib/wxr.py:58 ensure_ascii JSON serialisation)
  contained legacy mutation                 1  (lib/stage3_gate.py:57-64 repair_text, not a gate)
  canary                                 PASS
  restored full-fidelity assertions       2/2 PASS
```

---

## 7. Governing-document restoration status

```text
  claim                    semantic restoration only
  byte-exact restoration   NOT CLAIMED — no pre-edit checksum exists
  observed difference      1 byte (19,368 observed pre-edit; 19,367 restored)
  restored SHA-256         E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5
  status                   archived at archive/governing/CODEX-BUILD-2.md, provenance only
  baseline                 this hash is the comparison baseline from here
  recurrence prevention    standing rule 7
  source                   RUN-BLOCK-01.md §A D9 (ledger RB01-D9)
```

---

## 8. Citation remap

```text
  remapped stable citation definitions   16
  ledger source_refs covered by them     75
  undefined source_refs                   0
  spec values that lost a citation        0
  stale governing strings in ledger       0
```

---

## GATE 21 RESULT

```text
  Required inputs present and parsed strictly            PASS
  Ledger class total                                     PASS — 157 combined (156 main + 1 planned supplementary)
  Ledger values retain source citations                  PASS
  Citation remap                                         PASS — 75 references, zero lost
  Module crosswalk and translated noindex gate           PASS
  Explicit §2 conflicts reconciled                       PASS
  Unlisted conflicts printed                             PASS — 18 findings, full register above
  Spec vs manifest/XML known asymmetry                   PASS — exactly one planned supplementary page
  Manifest vs XML                                        PASS — zero divergences across all 156 pages
  Encoding canary and restored assertions                PASS
  Governing-document restoration                         PASS with documented byte-level limitation
  Mandatory hash table                                   PASS — 7 of 7 MATCH
  Stage-order consistency                                PASS — resolved by D1; split declined
  D1-D9 applied and cited                                PASS
  D10-D14 applied and cited                              PASS

  GATE 21: PASS. Previously BLOCKED on the stage-order conflict; D1 resolves it.
  Launch state unchanged: index-ready 0 of 157, launch gate NO-GO.
```
