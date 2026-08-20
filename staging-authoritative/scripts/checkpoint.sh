#!/usr/bin/env bash
# Stage 29 — clean checkpoint creation and rollback for authoritative staging.
#
# NOT RUN IN THIS WORK BLOCK. Provided so that every mutating step in
# reports/29-staging-plan.md has a rollback point behind it.
#
# Usage:
#   ./checkpoint.sh create <label>     snapshot DB + uploads
#   ./checkpoint.sh restore <label>    roll DB + uploads back to a snapshot
#   ./checkpoint.sh list               show snapshots
#   ./checkpoint.sh verify <label>     confirm a snapshot is complete and readable

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
CP="$ROOT/checkpoints"
COMPOSE="docker compose -f $ROOT/docker-compose.yml"
DB_CONTAINER="camden-auth-db"

fail() { echo "FAIL: $*" >&2; exit 1; }

require_stack() {
  docker ps --format '{{.Names}}' | grep -qx "$DB_CONTAINER" \
    || fail "the authoritative stack is not running. Start it only after Gate 28 returns GO."
}

case "${1:-}" in
  create)
    label="${2:?usage: checkpoint.sh create <label>}"
    require_stack
    dir="$CP/$label"
    [ -e "$dir" ] && fail "checkpoint '$label' already exists; refusing to overwrite"
    mkdir -p "$dir"
    echo "==> dumping database"
    $COMPOSE exec -T db sh -c \
      'exec mariadb-dump --single-transaction --routines --triggers \
        -u root -p"$(cat /run/secrets/db_root_password)" camden_authoritative' \
      > "$dir/db.sql" || fail "database dump failed"
    echo "==> archiving uploads"
    tar -C "$ROOT" -czf "$dir/uploads.tar.gz" uploads || fail "uploads archive failed"
    echo "==> recording manifest"
    {
      echo "label=$label"
      echo "created=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "db_sha256=$(sha256sum "$dir/db.sql" | cut -d' ' -f1)"
      echo "uploads_sha256=$(sha256sum "$dir/uploads.tar.gz" | cut -d' ' -f1)"
      echo "db_bytes=$(stat -c%s "$dir/db.sql")"
      echo "uploads_bytes=$(stat -c%s "$dir/uploads.tar.gz")"
    } > "$dir/manifest.txt"
    cat "$dir/manifest.txt"
    echo "checkpoint '$label' created"
    ;;

  restore)
    label="${2:?usage: checkpoint.sh restore <label>}"
    require_stack
    dir="$CP/$label"
    [ -d "$dir" ] || fail "no such checkpoint: $label"
    "$0" verify "$label" || fail "checkpoint '$label' failed verification; refusing to restore"
    echo "==> restoring database"
    $COMPOSE exec -T db sh -c \
      'exec mariadb -u root -p"$(cat /run/secrets/db_root_password)" camden_authoritative' \
      < "$dir/db.sql" || fail "database restore failed"
    echo "==> restoring uploads"
    rm -rf "$ROOT/uploads"
    tar -C "$ROOT" -xzf "$dir/uploads.tar.gz" || fail "uploads restore failed"
    echo "==> flushing object cache"
    $COMPOSE run --rm --profile cli cli cache flush || true
    echo "rolled back to '$label'"
    ;;

  verify)
    label="${2:?usage: checkpoint.sh verify <label>}"
    dir="$CP/$label"
    [ -d "$dir" ] || fail "no such checkpoint: $label"
    [ -s "$dir/db.sql" ] || fail "db.sql missing or empty"
    [ -s "$dir/uploads.tar.gz" ] || fail "uploads.tar.gz missing or empty"
    [ -s "$dir/manifest.txt" ] || fail "manifest.txt missing"
    db_now="$(sha256sum "$dir/db.sql" | cut -d' ' -f1)"
    up_now="$(sha256sum "$dir/uploads.tar.gz" | cut -d' ' -f1)"
    grep -qx "db_sha256=$db_now" "$dir/manifest.txt" || fail "db.sql checksum drift"
    grep -qx "uploads_sha256=$up_now" "$dir/manifest.txt" || fail "uploads checksum drift"
    tar -tzf "$dir/uploads.tar.gz" >/dev/null || fail "uploads archive unreadable"
    echo "checkpoint '$label' verified"
    ;;

  list)
    [ -d "$CP" ] || { echo "no checkpoints"; exit 0; }
    for d in "$CP"/*/; do
      [ -f "$d/manifest.txt" ] && { echo "--- $(basename "$d")"; sed 's/^/  /' "$d/manifest.txt"; }
    done
    ;;

  *)
    echo "usage: checkpoint.sh {create|restore|verify|list} [label]" >&2
    exit 2
    ;;
esac
