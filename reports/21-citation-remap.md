# Stage 21 citation remap

Audit date: 18 August 2026 (Australia/Sydney)

`CODEX-BUILD-2.1.md` replaces `CODEX-BUILD-2.md` and Amendments A, B and C as the single governing instruction for this work block. The stable citation keys in `build/21-spec-ledger.json` have been retained so existing `source_refs` remain intact; their definitions now resolve exclusively to the replacement file.

| Stable key | Old citation | New citation | Ledger references after remap |
|---|---|---|---:|
| `B2-PRECEDENCE-TOTAL` | `CODEX-BUILD-2.md` §1, first conflict, plus Amendment B | `CODEX-BUILD-2.1.md` §2, Total page count | 5 |
| `B2-PRECEDENCE-INTERSECTIONS` | `CODEX-BUILD-2.md` §1, second conflict | `CODEX-BUILD-2.1.md` §2, intersections outside `intersection-differentiators.json` | 3 |
| `B2-PRECEDENCE-SERVICES` | `CODEX-BUILD-2.md` §1, fourth conflict | `CODEX-BUILD-2.1.md` §2, service-page count | 1 |
| `B2-PRECEDENCE-MODULES` | `CODEX-BUILD-2.md` §1, fifth conflict | `CODEX-BUILD-2.1.md` §2, suburb-module conflict | 1 |
| `B2-PRECEDENCE-GUIDES` | `CODEX-BUILD-2.md` §1, sixth conflict | `CODEX-BUILD-2.1.md` §2, guide-count conflict | 2 |
| `B2-PRECEDENCE-UNIQUE` | `CODEX-BUILD-2.md` §1, seventh conflict | `CODEX-BUILD-2.1.md` §2, uniqueness-rule conflict | 26 |
| `B2-PRECEDENCE-WAVES` | `CODEX-BUILD-2.md` §1, eighth conflict and Stage 27 | `CODEX-BUILD-2.1.md` §2, wave-table conflict; §4.27 | 6 |
| `B2-PRECEDENCE-CAMDEN` | `CODEX-BUILD-2.md` §1, ninth conflict | `CODEX-BUILD-2.1.md` §2, forbidden Camden suburb URLs | 3 |
| `B2-HARD-2` | `CODEX-BUILD-2.md` §2, hard rule 2 | `CODEX-BUILD-2.1.md` §3, standing rule 2 | 3 |
| `B2-HARD-4` | `CODEX-BUILD-2.md` §2, hard rule 4 | `CODEX-BUILD-2.1.md` §3, standing rule 4 | 6 |
| `B2-STAGE27` | `CODEX-BUILD-2.md`, Stage 27 | `CODEX-BUILD-2.1.md` §4.27 | 6 |
| `AMEND-B1` | Amendment B, B1 | `CODEX-BUILD-2.1.md` §4.11.1 | 4 |
| `AMEND-B2` | Amendment B, B2 | `CODEX-BUILD-2.1.md` §4.11.2 | 3 |
| `AMEND-B5` | Amendment B, B5 | `CODEX-BUILD-2.1.md` §4.11.5 | 2 |
| `AMEND-B7` | Amendment B, B7 | `CODEX-BUILD-2.1.md` §4.11.7 | 2 |
| `AMEND-B8` | Amendment B, B8 | `CODEX-BUILD-2.1.md` §4.11.8 | 2 |

## Integrity result

- Remapped stable citation definitions: **16**.
- Ledger `source_refs` covered by those definitions: **75**.
- Undefined `source_refs`: **0**.
- Spec values that lost a citation: **0**.
- The ledger contains 42 citation definitions and uses 41 of them. `SEO-6` remains defined but unused; this is an existing redundant definition, not a lost citation.
- Outside this provenance table, neither `build/21-spec-ledger.json` nor `reports/21-reconciliation-v2.md` may cite the superseded governing file or an amendment as current authority.

Result: **PASS — every former governing-instruction citation is re-pointed without loss.**
