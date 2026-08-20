#!/usr/bin/env python3
"""Apply the generated Phase B manifest to the local public-media intake.

This operation is idempotent and recoverable. EXCLUDE files move to
media-retired; any future HOLD files move to media-held-band-a; RENAME files
stay in the public intake under their declared generic names.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "build" / "47-media-remediation.csv"
MEDIA = ROOT / "source-inputs" / "media"
RETIRED = ROOT / "source-inputs" / "media-retired"
HELD = ROOT / "source-inputs" / "media-held-band-a"
RESULT = ROOT / "reports" / "47-media-file-application.json"


def rows() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        return list(csv.DictReader(handle))


def assert_inside(path: Path, parent: Path) -> None:
    resolved = path.resolve()
    base = parent.resolve()
    if resolved != base and base not in resolved.parents:
        raise AssertionError(f"path escapes intended directory: {resolved} not within {base}")


def move_once(source: Path, destination: Path) -> str:
    assert_inside(source, ROOT)
    assert_inside(destination, ROOT)
    if source.exists() and destination.exists():
        if source.read_bytes() != destination.read_bytes():
            raise AssertionError(f"source/destination collision differs: {source.name}")
        source.unlink()
        return "removed-identical-duplicate"
    if source.exists():
        source.replace(destination)
        return "moved"
    if destination.exists():
        return "already-applied"
    raise AssertionError(f"neither source nor destination exists: {source.name}")


def locate_by_attachment_id(attachment_id: int) -> list[Path]:
    pattern = f"-{attachment_id}"
    found = []
    for directory in (MEDIA, RETIRED, HELD):
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.is_file() and path.stem.endswith(pattern):
                found.append(path)
    return found


def place_asset(attachment_id: int, destination: Path) -> str:
    """Move the one provenance binary from any known Phase B directory."""
    assert_inside(destination, ROOT)
    candidates = locate_by_attachment_id(attachment_id)
    if destination in candidates:
        extras = [path for path in candidates if path != destination]
        if extras:
            raise AssertionError(
                f"attachment {attachment_id} has duplicate provenance files: "
                + ", ".join(str(path.relative_to(ROOT)) for path in candidates)
            )
        return "already-applied"
    if len(candidates) != 1:
        raise AssertionError(
            f"attachment {attachment_id} expected one movable provenance file, found "
            f"{len(candidates)}: {[str(path.relative_to(ROOT)) for path in candidates]}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    candidates[0].replace(destination)
    return "moved"


def apply() -> dict:
    manifest = rows()
    if len(manifest) != 83:
        raise AssertionError(f"manifest has {len(manifest)} rows, expected 83")
    MEDIA.mkdir(parents=True, exist_ok=True)
    RETIRED.mkdir(parents=True, exist_ok=True)
    HELD.mkdir(parents=True, exist_ok=True)
    operations = []
    for row in manifest:
        attachment_id = int(row["attachment_id"])
        action = row["payload_action"]
        current = row["current_filename"]
        target = row["target_filename"]
        if action == "RENAME":
            status = place_asset(attachment_id, MEDIA / target)
            operations.append(
                {
                    "attachment_id": attachment_id,
                    "action": action,
                    "source": current,
                    "destination": target,
                    "status": status,
                }
            )
        elif action == "EXCLUDE":
            status = place_asset(attachment_id, RETIRED / current)
            operations.append(
                {
                    "attachment_id": attachment_id,
                    "action": action,
                    "source": current,
                    "destination": f"source-inputs/media-retired/{current}",
                    "status": status,
                }
            )
        elif action == "HOLD":
            status = place_asset(attachment_id, HELD / current)
            operations.append(
                {
                    "attachment_id": attachment_id,
                    "action": action,
                    "source": current,
                    "destination": f"source-inputs/media-held-band-a/{current}",
                    "status": status,
                }
            )
        elif action == "RETAIN":
            status = place_asset(attachment_id, MEDIA / current)
            operations.append(
                {
                    "attachment_id": attachment_id,
                    "action": action,
                    "source": current,
                    "destination": current,
                    "status": status,
                }
            )
        else:
            raise AssertionError(f"attachment {attachment_id} has unknown action {action!r}")

    expected_public = {
        row["target_filename"] if row["payload_action"] == "RENAME" else row["current_filename"]
        for row in manifest
        if row["payload_action"] in {"RENAME", "RETAIN"}
    }
    actual_public = {path.name for path in MEDIA.iterdir() if path.is_file()}
    if actual_public != expected_public:
        raise AssertionError(
            f"public directory parity failure missing={sorted(expected_public-actual_public)} "
            f"additional={sorted(actual_public-expected_public)}"
        )
    if any(" (1)" in name for name in actual_public):
        raise AssertionError("collision-suffixed filename remains in public intake")
    result = {
        "result": "PASS",
        "public_files": len(actual_public),
        "actions": dict(sorted(Counter(row["payload_action"] for row in manifest).items())),
        "operations": operations,
    }
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def check() -> dict:
    manifest = rows()
    errors = []
    for row in manifest:
        action = row["payload_action"]
        current = row["current_filename"]
        target = row["target_filename"]
        if action == "RENAME" and not (MEDIA / target).is_file():
            errors.append(f"attachment {row['attachment_id']} target absent: {target}")
        elif action == "EXCLUDE" and (
            (MEDIA / current).exists() or not (RETIRED / current).is_file()
        ):
            errors.append(f"attachment {row['attachment_id']} exclusion not applied")
        elif action == "HOLD" and (
            (MEDIA / current).exists() or not (HELD / current).is_file()
        ):
            errors.append(f"attachment {row['attachment_id']} Band A hold not applied")
        elif action == "RETAIN" and not (MEDIA / current).is_file():
            errors.append(f"attachment {row['attachment_id']} retained file absent")
    expected = sum(row["payload_action"] in {"RENAME", "RETAIN"} for row in manifest)
    actual = len([path for path in MEDIA.iterdir() if path.is_file()])
    if actual != expected:
        errors.append(f"public intake count {actual} != manifest {expected}")
    result = {
        "result": "FAIL" if errors else "PASS",
        "public_files": actual,
        "expected_public_files": expected,
        "errors": errors,
    }
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        raise AssertionError("; ".join(errors))
    return result


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = check() if args.check else apply()
        print(
            f"PASS — Phase B media files: public={result['public_files']}; "
            f"mode={'check' if args.check else 'apply'}"
        )
        return 0
    except Exception as exc:
        RESULT.write_text(
            json.dumps({"result": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"FAIL — Phase B media files: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
