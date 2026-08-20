# Stage 21 encoding-integrity audit

Audit date: 18 August 2026 (Australia/Sydney)

## Environment and scope

All Stage 21 Python checks were run with `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `sys.stdout.reconfigure(encoding="utf-8")`, and explicit `encoding="utf-8"` plus strict error handling on every text-file open. PowerShell's pipeline and console encodings were also set to a no-BOM UTF-8 encoding before passing non-ASCII source through standard input.

The audit covered all 18 workspace scripts with `.py`, `.sh`, `.ps1`, `.js` or `.php` extensions. It searched for lossy decode modes, ASCII-only tests, transliteration, Unicode normalisation, character stripping, escaped-versus-literal comparisons and substitutions that could collapse dash or unit characters.

## Findings and corrections

| File and line | Finding | What it could fail to detect | Disposition |
|---|---|---|---|
| `lib/stage20_crawl.py:37` | The response decoder used `errors="replace"`. | An invalid UTF-8 byte in rendered titles, robots content or evidence markers could be replaced by `U+FFFD`, allowing a route audit to compare corrupted text rather than fail. | **Fixed:** decoding is now strict. The script also reconfigures stdout to UTF-8. |
| `lib/stage3_gate.py:58–61` | The historical Stage 3 repair routine replaces four exact question-mark corruption signatures with an em dash, en dash or `²`. | If reused as a validator, it could not distinguish a genuinely intended question mark in one of those exact strings from prior encoding damage; it repairs instead of detecting. | **Contained legacy mutation:** it is not used by Stage 21 or any current preflight assertion. It is recorded here and must not be reused as a gate. The immutable WXR files are checked directly. |
| `lib/stage8.py:475` | Attachment filename generation strips characters outside lowercase ASCII letters and digits when forming controlled slugs. | It would collapse a non-ASCII source filename character rather than preserve its code point. | **Scope-safe, not a content assertion:** this operates only on deliberately ASCII attachment slug names and is not used for body copy, meta lengths, blocklist scanning or uniqueness. The exact generated filenames are separately governed by the image map. |
| `lib/wxr.py:58` | Elementor JSON serialisation uses `ensure_ascii=True`. | None after parsing: JSON `\uXXXX` escaping changes the byte representation but is reversible and does not strip or substitute code points. A byte comparison of literal Unicode against the serialised escape form would be invalid. | **Retained:** round-trip tests compare parsed values. The Stage 21 canary separately verifies literal UTF-8 file I/O. |

No `errors="ignore"`, residual `errors="replace"`, transliteration library, `isascii()` gate, or Unicode-normalisation call remains in a workspace script.

## Restored full-fidelity assertions

The two previously weakened checks now compare the exact non-ASCII source strings:

1. Governing instruction: `## 4.25 — Stage 25: uniqueness enforcement`
2. Gate report: `PASS — 157 combined (156 main + 1 planned supplementary)`

Both assertions pass through `scripts/21-encoding-canary.py`. Neither is shortened to an ASCII-stable substring.

## Canary result

`tests/fixtures/encoding-canary.txt` contains an em dash, en dash, `²` and a non-breaking space. `scripts/21-encoding-canary.py` writes it to a temporary UTF-8 file, reads it back strictly, compares the complete string and verifies each required code point.

Result: **PASS — the fixture survived an exact UTF-8 read-write-compare cycle, and both restored assertions passed.** Canary failure is a mandatory preflight failure for Stage 28.
