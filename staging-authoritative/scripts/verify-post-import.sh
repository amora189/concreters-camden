#!/usr/bin/env bash
# Execute only after an explicitly authorised authoritative staging import.
# This pass installs the verifier but does not run it.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGING="$(cd "$HERE/.." && pwd)"
REPO="$(cd "$STAGING/.." && pwd)"
COMPOSE=(docker compose -f "$STAGING/docker-compose.yml")
WP=("${COMPOSE[@]}" run --rm --profile cli cli)

fail() { echo "FAIL: $*" >&2; exit 1; }

controls=(
  build/46-active-page-allowlist.json
  build/46-claim-register.json
  build/22-menu-assignment.json
  build/46-public-media-policy.json
)
for rel in "${controls[@]}"; do
  [ -f "$REPO/$rel" ] || fail "missing control $rel"
  cp "$REPO/$rel" "$STAGING/import/$(basename "$rel")"
done
cp "$HERE/verify-post-import.php" "$STAGING/import/verify-post-import.php"

set +e
"${WP[@]}" eval-file \
  /import/verify-post-import.php \
  /import/46-active-page-allowlist.json \
  /import/46-claim-register.json \
  /import/22-menu-assignment.json \
  /import/46-public-media-policy.json \
  > "$REPO/reports/46-post-import-verification.json"
rc=$?
set -e

[ -s "$REPO/reports/46-post-import-verification.json" ] \
  || fail "post-import verifier produced no machine-readable output"
[ "$rc" -eq 0 ] || fail "post-import verification failed; see reports/46-post-import-verification.json"

echo "PASS: post-import database/rendered-output verification"

