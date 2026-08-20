# START HERE — Camden Concreting Build Launcher

**Paste this whole message into Codex and attach `concreters-camden.zip`. Nothing else.**

---

## Who you are and what you're doing

You are executing a staged, gated build that transforms a WordPress WXR export of a Melbourne concreting site into an importable WXR for a South West Sydney concreting site. The full stage script is inside the zip at `CODEX-BUILD.md`. This message is the launcher: it tells you how to unpack, how to verify you've read the specs correctly, and how to behave for the rest of the job.

You produce **files on disk only**. You do not deploy. You do not touch a live WordPress site. You do not run anything against a public URL.

---

## Execution protocol — this governs everything that follows

1. **Stages run in order. No skipping, no merging, no "I'll do 4 and 5 together."**
2. **Every stage ends with a STOP GATE.** Run the gate, print the report, and only then continue.
3. **A failed gate halts the build.** Fix it and re-run the gate. If you can't fix it, stop and ask me. Never proceed with a known failure and never note a failure and carry on.
4. **Three gates require my explicit approval before you continue:** Gate 0, Gate 3, and Gate 9. At these you stop and wait for me to reply. Do not assume approval.
5. **Never summarise a spec file instead of reading it.** These files contain specific numbers that must be reproduced exactly. Read them in full.
6. **Never invent.** No prices, completed jobs, reviews, licence numbers, ABNs, volume claims or council figures you cannot cite from the supplied files. Emit `[[PLACEHOLDER: what's needed]]` instead and log it.
7. **Never round or paraphrase a specification.** 32 MPa stays 32 MPa. 125mm stays 125mm. SL72 stays SL72. 800mm stays 800mm.
8. **Never restructure an Elementor layout**, change a widget type, rename a CSS class, or "improve" the design. You change text, metadata, URLs and image references. Nothing else.
9. **Australian English throughout.**
10. If a transformation is ambiguous, **stop and ask.** Guessing costs more than asking.

---

## Step A — Unpack and verify the manifest

```bash
mkdir -p ./camden-clone && cd ./camden-clone
unzip -o ../concreters-camden.zip -d ./inputs
find ./inputs -type f | sort
```

Confirm all seven files are present:

| File | Role |
|---|---|
| `CODEX-BUILD.md` | The stage script you will execute |
| `camden-site-structure-and-silo.md` | Architecture authority — URLs, silo, link rules, clone procedure |
| `suburbs.json` | Data authority — per-suburb facts, keywords, metadata |
| `oran-park-gold-standard.md` | Copy authority — module structure, register, uniqueness bar |
| `camden-concreting-seo-spec.md` | Schema authority (§7) + anti-doorway rules (§5) |
| `codex-clone-prompt.md` | Technical authority — Elementor parsing, widget field map, gates |
| `eamptcoconcretersmelbourne_WordPress_2026-08-14.xml` | The source WXR being transformed |

**If any file is missing, stop and tell me which one.** Do not attempt to proceed or reconstruct it.

Set up the working structure:

```bash
mkdir -p source build reports lib tests
cp ./inputs/eamptcoconcretersmelbourne_WordPress_2026-08-14.xml ./source/
chmod 444 ./source/*.xml
```

The source XML is read-only from this point. Never modify it.

---

## Step B — Read the specs in this order

Read each in full. Do not skim.

1. `CODEX-BUILD.md` — the stage script and the precedence table
2. `camden-site-structure-and-silo.md` — architecture, §2 the two fixes, §4 link rules, §6 clone procedure, §7 footprint
3. `codex-clone-prompt.md` — §1 the widget field map (this is where builds break), §2 global replacements, §9 gates
4. `oran-park-gold-standard.md` — the copy pattern, all 11 modules, the register notes at the end
5. `suburbs.json` — every suburb object
6. `camden-concreting-seo-spec.md` — **§5 and §7 only.** The rest is superseded, per the precedence table.

---

## Step C — Comprehension check (prove you read them)

Before writing a single line of build code, answer these eight questions in plain text. Each has one correct answer that exists in the files. **Getting any of these wrong means you skimmed — go back and read properly.**

1. What is the footpath allocation offset in Oran Park, and how does it differ from the rest of the Camden LGA?
2. How many services does `suburbs.json` list, how many service *pages* get built, and what resolves that difference?
3. `suburbs.json` contains a suburb entry for Camden. Do you build that page? Why or why not?
4. Where does the text of an `e-heading` widget live, and what second location must be kept in sync with it?
5. Which two postmeta keys must be deleted from every page, and what breaks if you leave each one?
6. Which spec file's recommended tech stack is superseded, and by what?
7. Which suburb pages ship as `publish` and which ship as `draft`, and why?
8. Name the two hard-failure gates at Stage 9.

Print your answers, then stop.

---

## Step D — Execute

Once your comprehension answers are correct, begin **Stage 0** of `CODEX-BUILD.md` and follow it through to Stage 10.

### Reporting format for every stage

```
═══════════════════════════════════════
STAGE {n} — {name}
═══════════════════════════════════════
READ:      {files consulted this stage}
DID:       {what you changed, concretely}
ARTIFACTS: {files written, with paths}

GATE {n}: PASS / FAIL
  ✓ {assertion}: {result}
  ✗ {assertion}: {result + the failing items enumerated}

{if FAIL}      → HALTING. {what's wrong, what you need}
{if approval}  → AWAITING APPROVAL. Reply "continue" to proceed to Stage {n+1}.
{if PASS}      → Proceeding to Stage {n+1}.
```

Write every gate report to `reports/{nn}-{name}.md` as well as printing it.

### Approval gates — stop and wait at these three

| Gate | What I'm checking |
|---|---|
| **0** | The page list. Must show 15 suburb pages, no `concreters-camden`, 7 services, 6 guides, correct publish/draft split. If it shows 16 suburbs you read `suburbs.json` over the precedence table — say so and fix it. |
| **3** | The Oran Park pilot page, rendered module by module. One page wrong is one fix; fifteen pages wrong is a rebuild. |
| **9** | Final validation, all 15 gates. |

### Work incrementally

Within a stage, if you're transforming multiple pages, do the first one completely and show it before batching the rest. Batching first and reviewing later is how systematic errors get multiplied.

---

## What this build is and isn't

You are producing `camden-concreting-import.xml` plus a reports directory. That file is not a live site — it's an import artifact that requires a manual post-import sequence (Astra Customizer settings, uploads folder, search-replace, cache purge, menu locations, schema rebuild). Stage 10 writes that runbook. Do not claim the site is built or live; claim the import file is ready and the runbook is written.

The gates are what make this reliable, not the length of the instructions. Run them honestly. A gate you passed by loosening the assertion is worse than a gate you failed.

---

**Begin at Step A.**
