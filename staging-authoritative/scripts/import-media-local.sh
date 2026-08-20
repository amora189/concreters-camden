#!/usr/bin/env bash
# Stage 29 — LOCAL-ONLY media importer for authoritative staging.
#
# NOT RUN IN THIS WORK BLOCK.
#
# Per CODEX-BUILD-2.1.md §4.29.2: preserves exact filenames and requested
# attachment IDs, with remote fetching disabled at the WordPress level.
#
# Stage 15 proved WordPress will silently suffix a colliding filename (-1,
# -scaled). This importer fails on any such drift rather than accepting it,
# because a suffixed filename produces a page that renders a broken image and
# raises no error.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
MEDIA="$REPO/source-inputs/media"
RENAME_MAP="$REPO/reports/08-image-rename-map.csv"
REMEDIATION_MAP="$REPO/build/47-media-remediation.csv"
COMPOSE="docker compose -f $ROOT/docker-compose.yml"
WP="$COMPOSE run --rm --profile cli cli"

fail() { echo "FAIL: $*" >&2; exit 1; }

[ -f "$REMEDIATION_MAP" ] || fail "missing Phase B media manifest: $REMEDIATION_MAP"

# --- preconditions -----------------------------------------------------------
"$REPO/scripts/22-media-audit.py" >/dev/null 2>&1 \
  || python "$REPO/scripts/22-media-audit.py" >/dev/null 2>&1 \
  || fail "media audit does not pass. Import is refused until all 83 binaries are present and valid."

$WP option get siteurl >/dev/null 2>&1 || fail "WordPress is not reachable"

# Confirm remote fetching really is off before importing anything.
$WP eval 'if ( ! defined("WP_HTTP_BLOCK_EXTERNAL") || ! WP_HTTP_BLOCK_EXTERNAL ) { exit(1); }' \
  || fail "WP_HTTP_BLOCK_EXTERNAL is not enabled. Refusing to import media."

declare -A remediation_action remediation_current remediation_target expected_filename
remediation_count=0
while IFS=$'\t' read -r attachment_id current_filename payload_action target_filename; do
  [ -z "$attachment_id" ] && continue
  [ -z "${remediation_action[$attachment_id]+x}" ] \
    || fail "duplicate remediation row for attachment $attachment_id"
  remediation_action[$attachment_id]="$payload_action"
  remediation_current[$attachment_id]="$current_filename"
  remediation_target[$attachment_id]="$target_filename"
  remediation_count=$((remediation_count + 1))
done < <(python3 - "$REMEDIATION_MAP" <<'PY'
import csv, sys
with open(sys.argv[1], encoding="utf-8-sig", errors="strict", newline="") as handle:
    for row in csv.DictReader(handle):
        print("\t".join((
            row["attachment_id"],
            row["current_filename"],
            row["payload_action"],
            row["target_filename"],
        )))
PY
)
[ "$remediation_count" -eq 83 ] || fail "expected 83 Phase B remediation rows, found $remediation_count"

echo "==> importing 55 permitted attachments with requested IDs and remediated exact filenames"

imported=0
excluded=0
held=0
while IFS=, read -r attachment_id old_filename new_filename pages_referencing; do
  [ "$attachment_id" = "attachment_id" ] && continue
  [ -z "$attachment_id" ] && continue
  final_filename="$new_filename"
  action_override="${remediation_action[$attachment_id]:-}"
  [ -n "$action_override" ] || fail "attachment $attachment_id absent from Phase B manifest"
  [ "${remediation_current[$attachment_id]}" = "$new_filename" ] \
    || fail "attachment $attachment_id remediation filename does not match immutable rename map"
  if [ "$action_override" = "EXCLUDE" ]; then
    excluded=$((excluded + 1))
    continue
  elif [ "$action_override" = "HOLD" ]; then
    held=$((held + 1))
    continue
  elif [ "$action_override" = "RENAME" ]; then
    final_filename="${remediation_target[$attachment_id]}"
    [ -n "$final_filename" ] || fail "attachment $attachment_id RENAME has no target filename"
  elif [ "$action_override" = "RETAIN" ]; then
    final_filename="$new_filename"
  else
    fail "attachment $attachment_id has unknown payload_action '$action_override'"
  fi
  expected_filename[$attachment_id]="$final_filename"
  src="$MEDIA/$final_filename"
  [ -f "$src" ] || fail "missing binary: $final_filename"

  # Import with the requested post ID. --porcelain returns the created ID so we
  # can assert it matches; WordPress will happily allocate a different one.
  got="$($WP media import "/import/media/$final_filename" \
          --porcelain \
          --post_id=0 \
          --preserve-filetime 2>/dev/null)" || fail "import failed: $final_filename"

  # Force the attachment to the requested ID and assert the filename survived.
  $WP db query "UPDATE wp_posts SET ID=$attachment_id WHERE ID=$got" \
    || fail "could not set attachment ID $attachment_id"
  $WP db query "UPDATE wp_postmeta SET post_id=$attachment_id WHERE post_id=$got" \
    || fail "could not repoint postmeta for $attachment_id"

  stored="$($WP eval "echo basename( get_post_meta( $attachment_id, '_wp_attached_file', true ) );")"
  [ "$stored" = "$final_filename" ] \
    || fail "FILENAME DRIFT: requested '$final_filename', WordPress stored '$stored'"

  imported=$((imported + 1))
done < "$RENAME_MAP"

[ "$imported" -eq 55 ] || fail "expected 55 permitted attachments, imported $imported"
[ "$excluded" -eq 28 ] || fail "expected 28 excluded attachments, found $excluded"
[ "$held" -eq 0 ] || fail "expected zero held Band A attachments, found $held"

# --- post-import assertions --------------------------------------------------
echo "==> verifying"
count="$($WP post list --post_type=attachment --format=count)"
[ "$count" -eq 55 ] || fail "expected 55 attachments in the database, found $count"

for attachment_id in "${!expected_filename[@]}"; do
  stored="$($WP eval "echo basename( get_post_meta( $attachment_id, '_wp_attached_file', true ) );")"
  [ "$stored" = "${expected_filename[$attachment_id]}" ] \
    || fail "FILENAME DRIFT after import: attachment $attachment_id expected '${expected_filename[$attachment_id]}', stored '$stored'"
done

echo "OK: 55 permitted attachments imported, 28 excluded, zero Band A held, exact filenames and requested IDs preserved, zero drift"
