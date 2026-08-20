#!/usr/bin/env bash
# Stage 22 — corrected re-encode driver.
#
# REPLACES the root-level reencode-images.sh, which does not parse: a quoting
# bug at its line 11 ("unexpected EOF while looking for matching \"") makes the
# original unrunnable. The original is left untouched for provenance; this file
# is the one to run. See reports/22-media-intake.md for the defect list.
#
# Footprint requirement, not optimisation: strip EXIF, resize 98%, quality 82.
#
# Properties the original lacked and this one has:
#   - parses
#   - idempotent: re-running with unchanged inputs rewrites nothing
#   - refuses to run in place (input_dir == output_dir would compound quality loss)
#   - feeds the audit: writes reports/22-reencode-manifest.csv with source and
#     output checksums, which scripts/22-media-audit.py can cross-check
#   - fail-closed: missing tool, missing source file, or a failed encode is a
#     non-zero exit, never a skipped file

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
input_dir="${1:-uploads/2026/07}"
output_dir="${2:-source-inputs/media}"
rename_map="${ROOT}/reports/08-image-rename-map.csv"
remediation_map="${ROOT}/build/47-media-remediation.csv"
manifest="${ROOT}/reports/22-reencode-manifest.csv"

fail() { echo "FAIL: $*" >&2; exit 1; }

command -v magick >/dev/null 2>&1 || fail "ImageMagick 'magick' not on PATH. Install it; do not substitute another encoder."
[ -f "$rename_map" ] || fail "rename map not found: $rename_map"
[ -f "$remediation_map" ] || fail "remediation map not found: $remediation_map"
[ -d "$input_dir" ] || fail "input directory not found: $input_dir"

# Refuse in-place operation: re-encoding an already-re-encoded file compounds
# quality loss and silently breaks the 98%/82 contract.
if [ "$(cd "$input_dir" && pwd)" = "$(cd "$output_dir" 2>/dev/null && pwd || echo __nonexistent__)" ]; then
  fail "input_dir and output_dir are the same directory. Refusing to re-encode in place."
fi

mkdir -p "$output_dir"
# Idempotency stamps live OUTSIDE the output directory. The output directory is
# staged for upload to a public web server and scripts/22-media-audit.py asserts
# it contains image binaries only (DECISION-08 D38). Sidecar files there would
# either be uploaded or force the assertion to carve out an exemption, and an
# exemption is how a non-image file goes unnoticed.
stamp_dir="${ROOT}/build/22-reencode-stamps"
mkdir -p "$stamp_dir"
printf 'attachment_id,old_filename,new_filename,source_sha256,output_sha256,action\n' > "$manifest"

declare -A remediation_action remediation_current remediation_target
remediation_count=0
while IFS=$'\t' read -r attachment_id current_filename payload_action target_filename; do
  [ -z "$attachment_id" ] && continue
  [ -z "${remediation_action[$attachment_id]+x}" ] \
    || fail "duplicate remediation row for attachment $attachment_id"
  remediation_action[$attachment_id]="$payload_action"
  remediation_current[$attachment_id]="$current_filename"
  remediation_target[$attachment_id]="$target_filename"
  remediation_count=$((remediation_count + 1))
done < <(python3 - "$remediation_map" <<'PY'
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

processed=0; active=0; excluded=0; held=0; skipped=0; encoded=0

# Read the CSV with a real field split. The original's ${var%"} construct is
# what broke it; there are no quoted fields in this map, so IFS=, is correct.
while IFS=, read -r attachment_id old_filename new_filename pages_referencing; do
  [ "$attachment_id" = "attachment_id" ] && continue
  [ -z "$attachment_id" ] && continue
  src="$input_dir/$old_filename"
  [ -f "$src" ] || fail "source image missing: $src (attachment $attachment_id)"

  src_sha="$(sha256sum "$src" | cut -d' ' -f1)"
  final_filename="$new_filename"
  action_override="${remediation_action[$attachment_id]:-}"
  [ -n "$action_override" ] || fail "attachment $attachment_id absent from Phase B remediation manifest"
  [ "${remediation_current[$attachment_id]}" = "$new_filename" ] \
    || fail "attachment $attachment_id remediation filename does not match immutable rename map"
  if [ "$action_override" = "EXCLUDE" ]; then
    [ ! -f "$output_dir/$new_filename" ] \
      || fail "excluded UNUSABLE asset remains in the public output directory: $new_filename"
    printf '%s,%s,%s,%s,%s,%s\n' \
      "$attachment_id" "$old_filename" "$new_filename" "$src_sha" "" "excluded" >> "$manifest"
    excluded=$((excluded + 1))
    processed=$((processed + 1))
    continue
  elif [ "$action_override" = "HOLD" ]; then
    [ ! -f "$output_dir/$new_filename" ] \
      || fail "held Band A asset remains in the public output directory: $new_filename"
    printf '%s,%s,%s,%s,%s,%s\n' \
      "$attachment_id" "$old_filename" "$new_filename" "$src_sha" "" "held-band-a" >> "$manifest"
    held=$((held + 1))
    processed=$((processed + 1))
    continue
  elif [ "$action_override" = "RENAME" ]; then
    final_filename="${remediation_target[$attachment_id]}"
    [ -n "$final_filename" ] || fail "attachment $attachment_id RENAME has no target filename"
    [ ! -f "$output_dir/$new_filename" ] \
      || fail "pre-remediation filename remains in the public output directory: $new_filename"
  elif [ "$action_override" = "RETAIN" ]; then
    final_filename="$new_filename"
  else
    fail "attachment $attachment_id has unknown payload_action '$action_override'"
  fi

  dst="$output_dir/$final_filename"
  stamp="$stamp_dir/${final_filename}.sha256"

  if [ -f "$dst" ] && [ -f "$stamp" ] && [ "$(cat "$stamp")" = "$src_sha" ]; then
    action="skipped-idempotent"
    skipped=$((skipped + 1))
  else
    magick "$src" -resize 98% -strip -quality 82 "$dst" || fail "encode failed: $src"
    printf '%s' "$src_sha" > "$stamp"
    action="encoded"
    encoded=$((encoded + 1))
  fi

  out_sha="$(sha256sum "$dst" | cut -d' ' -f1)"
  printf '%s,%s,%s,%s,%s,%s\n' \
    "$attachment_id" "$old_filename" "$final_filename" "$src_sha" "$out_sha" "$action" >> "$manifest"
  active=$((active + 1))
  processed=$((processed + 1))
done < "$rename_map"

echo "processed=$processed active=$active excluded=$excluded held=$held encoded=$encoded skipped=$skipped"
echo "manifest -> ${manifest#"$ROOT/"}"
[ "$processed" -eq 83 ] || fail "expected 83 images, processed $processed"
[ "$active" -eq 55 ] || fail "expected 55 public images after owner-approved Phase B enforcement, found $active"
[ "$excluded" -eq 28 ] || fail "expected 28 excluded assets, found $excluded"
[ "$held" -eq 0 ] || fail "expected zero held Band A assets, found $held"
echo "Now run: python scripts/22-media-audit.py"
