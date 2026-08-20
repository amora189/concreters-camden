# Stage 21 item 12 — module contract gap analysis

Date: 18 August 2026 (Australia/Sydney).
Authority: `RUN-BLOCK-01.md` §A D8, item 12 (ledger `RB01-D8`).

Unlisted conflict 12 recorded that several page classes have no complete normative module
contract in any source document. D8 requires enumerating exactly which classes lack one and
what each is missing, and proposing contracts marked `AWAITING APPROVAL — not enforced`.

**An unapproved contract is not enforced. Its absence is also not a pass.** Both statements
hold simultaneously; a class below is neither passing nor failing its module contract, it is
unmeasured.

## Status by page class

```text
  CLASS home
    status   NO CONTRACT
    have     CODEX-BUILD.md Stage 5 names responsibilities, not a module sequence.
    missing  A normative ordered module list. Current sequence is artifact-derived from post_id 12.

  CLASS utility
    status   NO CONTRACT
    have     No governing document defines a utility module sequence.
    missing  A normative sequence, and a statement of how Gallery legitimately differs from Contact.

  CLASS service
    status   CONTRACT EXISTS
    have     camden-site-structure-and-silo.md §5.2 gives the full sequence.
    missing  Nothing. This class is specified.

  CLASS suburb
    status   CONTRACT EXISTS
    have     structure doc §5.1, 11 modules, with oran-park-gold-standard.md as the worked example.
    missing  Nothing. This class is specified and is the only class with a per-module uniqueness rule (8 of 11).

  CLASS intersection
    status   CONTRACT EXISTS
    have     expansion-300-pages.md §4 gives the content shape and the 150-word shared-spec budget.
    missing  Nothing.

  CLASS guide_hub
    status   PARTIAL
    have     expansion §5 specifies the five-section taxonomy but not an Elementor module sequence.
    missing  The module sequence. Taxonomy is not a layout contract.

  CLASS guide
    status   PARTIAL
    have     structure doc §5.3 names the clone source and the H1->H2 correction only.
    missing  A complete generic guide contract. The observed 7-section shape is artifact-derived.

  CLASS cost_comparison
    status   PARTIAL
    have     expansion §6 lists the ten pages but specifies no module sequence.
    missing  The module sequence, which Stage 31 must match for the calculator. §4.31.2 requires deriving it from the ten existing pages.

```

## Summary

```text
  classes with a complete normative contract   3  (service, suburb, intersection)
  classes with a partial contract              3  (guide_hub, guide, cost_comparison)
  classes with no contract                     2  (home, utility)
  total classes                                8
```

## Proposed contracts — AWAITING APPROVAL, not enforced

Each proposal below is the shape observed in the validated artifact, written down. Adopting a
proposal makes it a rule; until then it is a description. **Do not enforce these, and do not
treat a page as passing because it matches one.**

```text
  PROPOSED CONTRACT — home
    status    AWAITING APPROVAL — not enforced
    module  1  hero
    module  2  services
    module  3  Camden local conditions
    module  4  job scoping
    module  5  trust
    module  6  service areas
    module  7  FAQ/CTA
    basis     artifact observation only; no governing document specifies this

  PROPOSED CONTRACT — utility
    status    AWAITING APPROVAL — not enforced
    observed  Contact-style Elementor template; Gallery is the same layout pending real media.
    basis     artifact observation only; no governing document specifies this

  PROPOSED CONTRACT — guide_hub
    status    AWAITING APPROVAL — not enforced
    module  1  H1/intro
    module  2  Council & approvals
    module  3  Ground & engineering
    module  4  Cost
    module  5  Finishes & materials
    module  6  Problems & maintenance
    basis     artifact observation only; no governing document specifies this

  PROPOSED CONTRACT — guide
    status    AWAITING APPROVAL — not enforced
    module  1  topic-led H1
    module  2  short answer
    module  3  facts requiring verification
    module  4  site inputs
    module  5  council/engineering records
    module  6  common mistakes
    module  7  FAQ
    basis     artifact observation only; no governing document specifies this

  PROPOSED CONTRACT — cost_comparison
    status    AWAITING APPROVAL — not enforced
    module  1  topic-led H1
    module  2  inputs
    module  3  inclusions
    module  4  limits
    module  5  site variables
    module  6  next step
    basis     artifact observation only; no governing document specifies this

```

## Consequence for later stages

```text
  Stage 25  measures uniqueness for these classes but enforces no class threshold,
            because none is sourced. See ledger unthresholded_classes = 27.
  Stage 31  must derive the calculator's module outline from the ten existing cost pages
            per §4.31.2, precisely because no normative contract exists to copy.
  Stage 32  cannot QA a page against a contract that has not been approved.
```
