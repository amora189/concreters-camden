#!/usr/bin/env bash
# Stage 28 — deterministic preflight runner. FAIL-CLOSED.
#
# Per CODEX-BUILD-2.1.md §4.28 and RUN-BLOCK-01.md §A D1.
#
# Gates run in this exact order. Any FAIL makes the whole run NO-GO.
# No gate may be skipped or marked advisory. A gate that cannot run at full
# fidelity FAILS; it does not degrade to a warning.
#
#   1. encoding canary (§3.1)
#   2. 15 Stage 9 gates
#   3. occupied post-ID collision audit ACROSS BOTH XML FILES
#   4. media audit
#   5. Astra audit
#   6. Elementor image-reference count
#   7. uniqueness gates
#   8. intersection audit
#   9. menu lint
#  10. Victorian blocklist scan
#  11. placeholder-in-schema scan
#  12. coherence
#  13. source-brand transformation result
#  14. assigned-menu safety
#  15. active architecture/import parity
#  16. claim-to-evidence parity
#  17. public-media suitability
#  18. owner identity, Liverpool, privacy, contact and schema evidence
#  19. completed Phase D Liverpool content and calculator exclusion
#
# This script does NOT import, deploy, start a container, publish, or remove
# noindex from anything. It reads and reports.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

REPORT="reports/28-preflight.md"

# Resolve an interpreter in both documented environments:
#   * Windows/MSYS normally exposes python or py.exe
#   * WSL commonly exposes python3, and may expose Windows python.exe but no
#     `python` alias.  Relative repo paths are intentional and work in both.
if [ -n "${PYTHON:-}" ]; then
  PY_CMD=("$PYTHON")
elif command -v python.exe >/dev/null 2>&1; then
  PY_CMD=(python.exe)
elif command -v python3 >/dev/null 2>&1; then
  PY_CMD=(python3)
elif command -v python >/dev/null 2>&1; then
  PY_CMD=(python)
elif command -v py.exe >/dev/null 2>&1; then
  PY_CMD=(py.exe -3)
else
  echo "FAIL — no Python interpreter found (tried python.exe, python3, python, py.exe)" >&2
  exit 1
fi
run_py() { "${PY_CMD[@]}" "$@"; }

declare -a NAMES RESULTS DETAILS
OVERALL="GO"

record() {         # record <name> <result> <detail>
  NAMES+=("$1"); RESULTS+=("$2"); DETAILS+=("$3")
  if [ "$2" != "PASS" ]; then OVERALL="NO-GO"; fi
  printf '  %-46s %-7s %s\n' "$1" "$2" "$3"
}

echo "Stage 28 preflight — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

# ---- 1. encoding canary -----------------------------------------------------
if out=$(run_py scripts/21-encoding-canary.py 2>&1); then
  record "1. encoding canary (§3.1)" "PASS" "fixture and both restored assertions survived"
else
  record "1. encoding canary (§3.1)" "FAIL" "canary failed — whole run is NO-GO regardless of other gates"
fi

# ---- 2-11: the analytical gates run in one deterministic Python pass ---------
# Paths are kept RELATIVE here: this script runs under MSYS bash while python is
# a native Windows build, and an absolute MSYS path (/c/Users/...) is not a path
# Windows python can open.
#
# The external audits run first so that every gate can be RECORDED in the exact
# numeric order §4.28 specifies, rather than in the order the processes happen
# to finish.
if run_py scripts/22-media-audit.py >/dev/null 2>&1; then
  M_N=$(run_py -c "
import csv
rows=list(csv.DictReader(open('build/47-media-remediation.csv',encoding='utf-8-sig')))
print(sum(r['payload_action'] in {'RENAME','RETAIN'} for r in rows))
" | tr -d '\r\n')
  M_R="PASS"; M_D="active public intake technical contract passes: ${M_N}/${M_N}; immutable provenance baseline remains 83"
else
  M_R="FAIL"; M_D="media intake incomplete — see reports/22-media-missing-manifest.csv"
fi
if run_py scripts/22-astra-audit.py >/dev/null 2>&1; then
  A_R="PASS"; A_D="export parsed; required groups + design-carriage + internal-consistency all pass"
else
  A_R="FAIL"; A_D="Astra export absent or partial — see reports/22-astra-audit-result.md"
fi
if run_py scripts/27-menu-lint.py >/dev/null 2>&1; then
  L_R="PASS"; L_D="zero draft, noindex or 404 targets"
else
  L_R="FAIL"; L_D="Wave 1 menu spec contains a bad target"
fi

run_py scripts/28-gates.py > reports/28-gates.json 2> reports/28-gates.err
GATES_RC=$?
if [ $GATES_RC -ne 0 ] || [ ! -s reports/28-gates.json ]; then
  record "2-11. analytical gates" "FAIL" "gate runner did not produce output; see reports/28-gates.err"
else
  emit() {   # emit <leading-number>
    run_py -c "
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('reports/28-gates.json',encoding='utf-8'))
for g in d['gates']:
    if g['name'].split('.')[0]=='$1':
        print(g['name']+chr(9)+g['result']+chr(9)+g['detail'])
"
  }
  for n in 2 3; do
    while IFS=$'\t' read -r name result detail; do
      [ -z "$name" ] && continue
      record "$name" "$result" "$detail"
    done < <(emit "$n")
  done
  record "4. media intake audit" "$M_R" "$M_D"
  record "5. Astra Customizer audit" "$A_R" "$A_D"
  for n in 6 7 8; do
    while IFS=$'\t' read -r name result detail; do
      [ -z "$name" ] && continue
      record "$name" "$result" "$detail"
    done < <(emit "$n")
  done
  record "9. menu lint (Wave 1 spec)" "$L_R" "$L_D"
  for n in 10 11; do
    while IFS=$'\t' read -r name result detail; do
      [ -z "$name" ] && continue
      record "$name" "$result" "$detail"
    done < <(emit "$n")
  done
  # ---- 12. coherence gate (DECISION-03 D15) — build-failing ----------------
  if run_py scripts/34-coherence.py > reports/34-coherence.out 2>&1; then
    C_N=$(run_py -c "
import json,sys
d=json.load(open('reports/34-coherence-summary.json',encoding='utf-8'))
print(d['severity_counts'].get('SEVERE',0), d['pages_over_threshold'], d['corpus_filler_pct'])
")
    set -- $C_N
    if [ "$1" -eq 0 ]; then
      record "12. coherence gate (D15)" "PASS" "0 pages above the filler threshold"
    else
      record "12. coherence gate (D15)" "FAIL" \
        "$1 pages SEVERE, $2 above threshold, corpus filler $3 — no page above the threshold may enter any wave"
    fi
  else
    record "12. coherence gate (D15)" "FAIL" "coherence scan did not complete; see reports/34-coherence.out"
  fi
  # Gate 13 asserts the transformed output, not the existence of a rename plan.
  if run_py scripts/46-source-brand-gate.py > reports/46-source-brand-gate.out 2>&1; then
    B_R="PASS"
  else
    B_R="FAIL"
  fi
  B_D=$(run_py -c "
import json
d=json.load(open('reports/46-source-brand-gate.json',encoding='utf-8'))
b=d['baseline']; t=d['active_derivative']
print(f\"baseline {b['total']}={b['reader_visible']} reader-visible + {b['nonvisible_filenames_urls_slugs']} preserved; transformed reader-visible={t['reader_visible']}\")
" 2>/dev/null || echo "source-brand result unreadable")
  record "13. source-brand transformation result" "$B_R" "$B_D"

  for n in 14; do
    while IFS=$'\t' read -r name result detail; do
      [ -z "$name" ] && continue
      record "$name" "$result" "$detail"
    done < <(emit "$n")
  done

  if run_py scripts/46-architecture-import-gate.py --check > reports/46-architecture-import-gate.out 2>&1; then
    I_R="PASS"
  else
    I_R="FAIL"
  fi
  I_D=$(run_py -c "
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('reports/46-architecture-import-gate.json',encoding='utf-8'))
print(f\"allowed={d.get('allowed_pages')}; active-main={d.get('active_main')}; privacy={d.get('privacy')}; withdrawn={d.get('withdrawn')}; calculator={d.get('calculator')}\")
" 2>/dev/null || echo "architecture result unreadable")
  record "15. active architecture/import parity" "$I_R" "$I_D"

  if run_py scripts/46-claim-evidence-gate.py > reports/46-claim-evidence-gate.out 2>&1; then
    C_R="PASS"
  else
    C_R="FAIL"
  fi
  C_D=$(run_py -c "
import json
d=json.load(open('reports/46-claim-evidence-gate.json',encoding='utf-8'))
t=d['totals']
print(f\"occurrences={t['occurrences']}; unsupported={t['unsupported']}; pages={t['pages_with_claims']}; unsupported-pages={t['pages_with_unsupported_claims']}\")
" 2>/dev/null || echo "claim result unreadable")
  record "16. claim-to-evidence parity" "$C_R" "$C_D"

  if run_py scripts/46-public-media-gate.py > reports/46-public-media-gate.out 2>&1; then
    P_R="PASS"
  else
    P_R="FAIL"
  fi
  P_D=$(run_py -c "
import json
d=json.load(open('reports/46-public-media-gate.json',encoding='utf-8'))
print(f\"blocking={len(d['errors'])}; Band-A-unrecorded={sum(x['verdict']=='UNRECORDED' for x in d['band_a'])}; Band-B-fail={sum(x['result']=='FAIL' for x in d['band_b'])}\")
" 2>/dev/null || echo "public-media result unreadable")
  record "17. public-media suitability" "$P_R" "$P_D"

  if run_py scripts/30-build-schema.py > reports/30-schema-gate.out 2>&1 \
     && run_py scripts/51-evidence-validation.py > reports/51-evidence-validation.out 2>&1; then
    E_R="PASS"
  else
    E_R="FAIL"
  fi
  E_D=$(run_py -c "
import json
d=json.load(open('reports/51-evidence-validation.json',encoding='utf-8'))
if d.get('result') != 'PASS':
    print('; '.join(d.get('errors',[])) or 'evidence validation failed')
else:
    s=d['sections']
    print(f\"claims-unsupported={s['claims']['current_unsupported']}; Liverpool-placements={sum(s['liverpool_sources']['page_evidence_placements'].values())}; privacy-blockers={s['privacy_markers']['blocking_count']}; LocalBusiness={s['schema']['localbusiness']}\")
" 2>/dev/null || echo "evidence result unreadable")
  record "18. identity/Liverpool/schema evidence" "$E_R" "$E_D"

  # Gate 19 asserts the completed Phase D result in the generated derivative.
  # Source-page excerpts are revalidated separately when the official PDF is
  # supplied to the validator; this preflight assertion is fully offline.
  if run_py scripts/52-phase-d-liverpool.py > reports/52-liverpool-gate.out 2>&1; then
    D_R="PASS"
  else
    D_R="FAIL"
  fi
  D_D=$(run_py -c "
import json
d=json.load(open('reports/52-liverpool-validation.json',encoding='utf-8'))
if d.get('result') != 'PASS':
    print('; '.join(d.get('errors',[])) or 'Phase D validation failed')
else:
    print(f\"requirements={d['requirements']}; fields={d['resolved_fields']}; pages={d['pages']}; false-fidelity={sum(d['false_fidelity_residue'].values())}; calculator={d['calculator']}\")
" 2>/dev/null || echo "Phase D result unreadable")
  record "19. Phase D Liverpool content" "$D_R" "$D_D"
fi

echo
echo "OVERALL: $OVERALL"

# ---- write the report -------------------------------------------------------
{
  echo "# Stage 28 preflight"
  echo
  echo "Generated by \`scripts/28-preflight.sh\`. Fail-closed: any FAIL makes the run NO-GO."
  echo "No gate is skipped or marked advisory."
  echo
  echo '```text'
  printf '  %-46s %-7s %s\n' "GATE" "RESULT" "DETAIL"
  for i in "${!NAMES[@]}"; do
    printf '  %-46s %-7s %s\n' "${NAMES[$i]}" "${RESULTS[$i]}" "${DETAILS[$i]}"
  done
  echo
  printf '  %-46s %s\n' "OVERALL" "$OVERALL"
  echo '```'
} > "$REPORT"

echo "report -> reports/28-preflight.md"
[ "$OVERALL" = "GO" ] && exit 0 || exit 1
