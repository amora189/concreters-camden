# CLAUDE.md — Camden Concreting build, session handoff

You are picking up a staged WordPress build that another agent (Codex) was executing. It stopped mid-handoff at an approved Gate 21. **You have no memory of that session. Reconstruct state from artifacts, not from assumption.**

---

## 0. Governing documents

| File | Role |
|---|---|
| `CONTEXT.md` | Authoritative current state. Read first. |
| `CODEX-BUILD-2.1.md` | The build instruction, Stages 21–32. **Read-only. Never edit.** |
| `DECISION-01-gate21.md` | Owner decisions D1–D9 resolving Gate 21. **Read-only. Never edit.** |
| `build/21-spec-ledger.json` | The mutable record of every resolved spec value and its citation. |
| `archive/` | Superseded instruction documents. **Do not read except to check provenance.** Reading them will reintroduce conflicts 2.1 already resolved. |

`CODEX-BUILD-2.1.md` standing rules 1–10 and §3.1–3.2 apply to you in full, unchanged. Read them before doing anything. They are not advisory.

---

## 1. First actions, in this order

**Do not start any stage until steps 1–4 are complete and printed.**

1. **Verify integrity.** Recompute SHA-256 for `camden-concreting-import.xml`, `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml`, `build/stage9-page-manifest.json`, `build/stage8-image-map.json`, `reports/08-image-rename-map.csv`, `CODEX-BUILD-2.1.md`. Compare against the Gate 21 hash table below. **Any mismatch on an immutable file is a hard stop — report it and do nothing else.**

   ```
   Main WXR          A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884
   Source WXR        45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15
   Stage 9 manifest  578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42
   Stage 8 image map 0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF
   Image rename map  43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8
   Governing instr.  BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C
   ```

2. **Reconstruct state from artifacts.** Read `CONTEXT.md`, then `reports/21-reconciliation-v2.md`, `reports/21-citation-remap.md`, `reports/21-encoding-audit.md`, `reports/21-module-crosswalk.md`, `reports/21-governing-doc-diff.md`, `reports/21-context-diff.md`, and `build/21-spec-ledger.json`. Write `reports/handoff-state.md`: what exists on disk, what each report claims was verified, and **every place the reports and the artifacts disagree.** Trust the artifacts over the reports.

3. **Determine whether `DECISION-01-gate21.md` was applied.** The previous session was cut off before printing its D1–D9 confirmation report, so assume it was **not** applied unless the ledger shows citations to `DECISION-01` for each of D1–D9. State which of D1–D9 are already reflected in the artifacts and which are not.

4. **Apply any unapplied D1–D9 clauses** and print the confirmation report Codex owed, including the full resolution register for the 18 unlisted conflicts found at Gate 21 — one line each, resolution and citation.

Then stop and wait for approval before Stage 22.

---

## 2. State as of handoff

- Stage 21 complete and **approved** subject to D1–D9. Stage 22 not started.
- Architecture: **157 pages combined** — 156 in the immutable main WXR, plus 1 planned supplementary calculator page not yet built. 21 publish / 135 draft in the main WXR.
- **Index-ready: 0 of 157. Launch gate NO-GO.**
- Blocked on two owner-supplied P0 inputs that do not exist yet: the 83 original image binaries and the Astra Customizer export. **Nothing you do in Stages 22–32 can unblock these.**
- Stage ordering is **21 → 22 → 23 → ... → 31 → 32, sequential and unchanged.** A proposed 31A/31B split was declined in D1. Do not revisit it.
- Docker is not running. The local environment holds only a protected WordPress baseline, not the Camden site.

---

## 3. Hard stops for this session

You execute commands, which the previous agent largely did not. That widens the blast radius. These are absolute:

1. **Do not import anything.** Not to the disposable environment, not to authoritative staging, not anywhere. Stage 29 builds the scaffolding and writes the plan; it does not run it.
2. **Do not start Docker containers.**
3. **Do not modify `camden-concreting-import.xml`, the source WXR, or any file in `archive/`.**
4. **Do not build the calculator page.** That is Stage 31, after the enforcement machinery exists.
5. **Do not deploy, push to a live host, submit a sitemap, or remove noindex from anything.**
6. **Do not research or infer a council fee, permit threshold, soil classification, licence number, ABN, address or price** — not from the web, not from a neighbouring suburb, not from a Melbourne figure. These are owner-supplied. Emit a blocking marker and an owner question. This is the single most likely way for you to damage this build: a plausible fabricated council fee propagates to 30 pages and reads as correct.
7. **Never narrow, relax or make lossy an assertion to work around a console, output or encoding limitation.** If a check cannot run at full fidelity it fails and is reported as blocked. See §3.1 of the instruction — the previous session had exactly this failure on Windows and it was caught. You are on the same platform.
8. **Never edit an instruction document.** Resolutions go in `build/21-spec-ledger.json` with a citation. New decisions arrive as new numbered decision-record files.

---

## 4. Windows encoding setup

This repo lives on Windows and the previous session hit a console encoding false negative on em-dash text that briefly weakened two assertions.

Before running any script: set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`, reconfigure `sys.stdout` to UTF-8 explicitly, and open every file with `encoding='utf-8'` declared. Never use `errors='ignore'` or `errors='replace'`. Run the UTF-8 canary from §3.1 — em dash, en dash, `²`, non-breaking space through a full read-write-compare cycle — before trusting any content gate. `32 MPa`, `m²` and the specification ranges depend on it.

---

## 5. Every gate report includes

Per §3.2 of the instruction, without exception:

1. **`CONTEXT.md` update and diff** — date (Australia/Sydney), latest completed stage, **what was actually verified** rather than attempted, remaining blockers, next safe action. Never describe a generated artifact, smoke test, WXR `publish` status or local container as a live site, launch or approval. Never reduce the blocker list unless a blocker was cleared by verified evidence; a script that checks a blocker is not a cleared blocker.
2. **Hash table** for all six files in §1.
3. Then stop and wait for approval. **Do not chain stages.** The gates are the review points and they are the only thing keeping fabricated evidence out of this site.

---

## 6. Next action

Steps 1–4 of §1, then stop. Stage 22 begins only on approval.
