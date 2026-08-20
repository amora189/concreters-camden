# RUN BLOCK 01 — Stages 22–30 and 32, continuous

**This file carries the D1–D9 clauses that never reached disk. It is the authoritative record of them.** If `DECISION-01-gate21.md` later appears in the repo, treat it as a duplicate: the two must agree in substance, and citations point here.

Save this to the repo root before acting on any clause.

---

## 0. Preconditions

Before starting, confirm and print:

1. All seven immutable file hashes still MATCH.
2. D10–D14 are applied and cited in `build/21-spec-ledger.json`.
3. §A below is applied — D1–D9, previously unavailable.
4. The Gate 21 confirmation report is printed, including the full 18-conflict resolution register, one field per line.

Then begin the batch.

---

## A. D1–D9 — Gate 21 resolutions

### D1 — Stage ordering: the 31A/31B split is declined

Your item 14 contradiction is real; the proposed resolution is not adopted. Stage 28 cannot return GO in this work block under any ordering, because the image binaries and Astra export are absent — so front-loading Stage 31 buys nothing at the gate it was meant to unblock. And building page copy before Stage 25 exists means writing it without the index that judges it; a fail at 31B would mean rewriting an already-approved page.

**Adopted ordering: 21 → 22 → 23 → 24 → 25 → 26 → 27 → 28 → 29 → 30 → 31 → 32, unchanged.**

| Stage | Assertion | Resolution |
|---|---|---|
| 23 | 157 readiness rows | Calculator gets a row flagged `Build status: not yet built — §4.31`, `Index-ready: no`. A readiness row for an unbuilt page is legitimate; a measurement of one is not. |
| 24 | Denominator 157 | 157. Calculator contributes zero image references until built — state that, don't omit it. |
| 25 | Measure all 157 | Measure 156. Calculator recorded `DEFERRED TO STAGE 31 — not yet built`. Never as passing, never as exempt. |
| 27 | Wave 4 includes the calculator | Include it, marked not-yet-built. Effective indexable counts unaffected — it is `noindex` on import. |
| 28 | Preflight runs against both XMLs | Runs against both. A missing supplementary artifact is a **genuine NO-GO reason, reported as one**, alongside missing media and Astra inputs. Never special-cased, suppressed or marked advisory. |

After Stage 31, run a bounded delta pass — `reports/31-delta.md` — re-running only the checks in Stages 23, 24, 25, 27 and 28 whose scope includes the calculator, scoped to that page alone. Not full stage re-runs. The delta pass is part of Gate 31.

### D2 — Dangling `#localbusiness` is a hard failure, resolved by omission

Suburb, intersection and service pages emit `Service` nodes whose `provider` references `#localbusiness`, but §4.30 forbids emitting `LocalBusiness` without a verified staffed address. Unresolved, the build emits references to an undefined `@id` on up to 140 pages — valid JSON that fails seo-spec §7.6 gate 2 and every external validator.

**The builder resolves by omission, never by emitting an undefined reference. In strict order:**
1. `#localbusiness` defined → `Service.provider` references it.
2. Not defined, but `#organization` defined from verified fields (verified legal entity name plus domain) → reference `#organization`.
3. Neither defined → **`Service` omits `provider` entirely.** A `Service` with no provider is incomplete but true. A `Service` pointing at an entity that does not exist is neither.

Never invent an address to define `#localbusiness`. Never assert "CoreX Concreters Camden" as a legal entity to define `#organization` — that identity is an open P1 blocker. Under current verification state, expect outcome 3 on every page; log it.

Add as a build-failing check: **zero references to any `@id` not defined in the same emitted graph.** Report the count of `Service` nodes omitting `provider`, per page class.

### D3 — 27, not 26

My arithmetic error. Classes with no sourced uniqueness threshold: 10 service + 11 cost/comparison + 1 guide hub + 1 homepage + 4 utility = **27**, of which 26 are currently built. Correct in the ledger. Everything else in §4.25.5 stands.

### D4 — Join key for the readiness superset

`reports/18-page-readiness.csv` has no page-ID column. **Join on slug**, normalised to leading-slash, trailing-slash, lowercase before comparison. Add `post_id` as a new column sourced from `build/stage9-page-manifest.json`. Report any slug in one file and not the other, and any slug not resolving to exactly one manifest entry — non-unique or unmatched is stop-and-ask, not best-effort.

### D5 — Module order is frozen as built

Structure doc §7 mitigation 4 (vary module order against the source site) conflicts with standing rule 6 (never restructure an Elementor layout). Both predate the validated WXR, which is now immutable.

**Whatever module order exists in `camden-concreting-import.xml` stands. Reorder nothing.** Record mitigation 4 as **not applied** and add it to `CONTEXT.md` as a **residual footprint risk** — shared section order with `bestconcretersmelbourne.com.au` — not as a task. Same for mitigation 5 (Elementor kit palette) if the kit is unchanged from source: check and record identically. Disclosed risks, not defects to fix by mutating a validated artifact.

### D6 — Link Rule A covers all ten services

Rule A (Home → all service pages) now covers **10**, not 7. Rules B–G unchanged in scope. Assert at Stage 27 that the homepage links to all ten.

### D7 — Image reuse permitted; pending-photo slots are not

Reuse of the 83 re-encoded images across Camden pages is permitted per expansion §9, subject to the ~15-page cap. "Original" in seo-spec §5 means not stock and not byte-identical to the source site after re-encoding; it does not forbid reuse within the site. **Unchanged: no `REAL_PHOTO_PENDING` slot may be filled by a re-encoded source-site image.** Top-of-report item at Stage 24.

### D8 — Items 1–5, 9, 10, 12, 15, 16, 18

Recorded resolutions accepted. Three additions:
- **Item 12** (incomplete normative module contracts): enumerate exactly which page classes lack a contract and what each is missing, in `reports/21-module-contracts-gap.md`. Propose contracts marked **`AWAITING APPROVAL — not enforced`**. Do not enforce an unapproved contract; do not treat its absence as a pass.
- **Item 16** is not a conflict. 0 index-ready is present state; 14 is a conditional future Wave 1 count. Both true. Never present them as alternatives.
- **Item 18**: renumber Stage 31 from §4.11 to **§4.31** in the ledger clause map, retaining §4.11 as an alias so existing citations resolve.

Surface the full 18-item resolution register at the confirmation report — one line each, resolution and citation.

### D9 — Governing document restoration

Accepted as recorded. Semantic restoration with a one-byte difference and no prior checksum is the honest outcome; do not claim byte-exact restoration. The Gate 21 hash is the baseline from here; standing rule 7 prevents recurrence.

---

## B. Batch authorisation

**Run Stages 22, 23, 24, 25, 26, 27, 28, 29, 30 and 32 continuously without pausing for approval between them.**

Every stage still: produces its full gate report, writes it to disk, reads it back, confirms byte count, and includes the §3.2 `CONTEXT.md` diff and hash table. The reports are the review surface. What changes is that you do not wait between them.

**Stage 31 is excluded and is not run.** It is the only stage authoring customer-facing copy and the only one carrying council fee data, and §4.31.2 requires approval of the derived slug and module outline before the body is written. Stop before it.

Ordering within the batch is unchanged and strictly sequential. Do not reorder, parallelise, or skip a stage because its inputs are missing — a stage blocked on missing inputs produces its harness and reports the block, which is its designed outcome.

---

## C. Stop conditions — halt the batch immediately and report

Non-negotiable. Any one of these ends the run where it stands:

1. Any immutable file hash changes.
2. Manifest-versus-XML divergence beyond the known-good one-page calculator asymmetry.
3. The UTF-8 canary fails, or any check cannot run at full fidelity.
4. Any stage cannot proceed without inventing a business fact, council figure, price, photo, identity or specification.
5. A gate's pass condition cannot be evaluated as written and would require reinterpreting the instruction to proceed.
6. Two governing clauses conflict with no non-lossy resolution.
7. Any operation would import, deploy, start a container, publish, remove noindex, or write to a live host.
8. A finding materially changes a decision already made in D1–D14.

A stage failing its own gate is **not** a stop condition — that is a normal, expected result to record and carry forward. Stage 28 returning NO-GO is the expected outcome, not a failure of the run.

---

## D. Final deliverable

At the end of the batch, produce `reports/run-block-01-summary.md`:

1. Per stage: gate result, artifacts written with byte counts and hashes, and what was actually verified as distinct from what was produced.
2. **One consolidated, deduplicated, prioritised owner-question list** across Stages 23, 25, 30 and 32 — ordered by pages unblocked, with the Liverpool City Council specification and the 83 image binaries expected near the top. This is the single most useful output of the whole block; it is my task list.
3. Every item marked `AWAITING APPROVAL — not enforced` in one place: uniqueness thresholds for the 27 unthresholded pages, module contracts from item 12, and anything else deferred.
4. A single unambiguous statement of launch state: index-ready count, gate verdict, and the ordered list of what must happen before one page can be indexed.
5. Everything you were unable to complete, and why.

Then stop. Stage 31 awaits approval.
