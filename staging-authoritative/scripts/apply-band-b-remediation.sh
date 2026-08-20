#!/usr/bin/env bash
# Retired safety guard. Band B is now applied before import by the reproducible
# derivative generator; running the former database mutator would double-apply
# slot removals and operate against filenames that no longer exist.

set -euo pipefail

echo "FAIL: obsolete post-import mutator refused. Regenerate build/46-active-main-import.xml with scripts/46-architecture-import-gate.py and import that derivative." >&2
exit 1
