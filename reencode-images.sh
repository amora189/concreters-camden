#!/usr/bin/env bash
set -euo pipefail

input_dir=${1:-uploads/2026/07}
output_dir=${2:-uploads-reencoded/2026/07}
mkdir -p "$output_dir"

tail -n +2 reports/08-image-rename-map.csv | while IFS=, read -r attachment_id old_filename new_filename pages; do
  old_filename=${old_filename%"}; old_filename=${old_filename#"}
  new_filename=${new_filename%"}; new_filename=${new_filename#"}
  magick "$input_dir/$old_filename" -resize 98% -strip -quality 82 "$output_dir/$new_filename"
done
