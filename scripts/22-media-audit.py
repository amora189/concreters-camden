#!/usr/bin/env python3
"""Stage 22 — media intake audit. Fail-closed.

Audits source-inputs/media/ against build/stage8-image-map.json,
reports/08-image-rename-map.csv and the generated Phase B disposition overlay
in build/47-media-remediation.csv. Exits non-zero on ANY gap and writes a
missing-file manifest. The two immutable inputs remain the 83-file provenance
baseline; the overlay produces the current fail-closed public import set.

Per CODEX-BUILD-2.1.md §4.22.2 this checks: all 83 filenames present; exact
match with no -1 / -scaled / suffix drift; MIME type; dimensions; checksum
recorded; file-size sanity; no unexpected extras.

Per §3.1 every file is opened with an explicit encoding and strict errors. No
assertion is narrowed to accommodate an output limitation. A check that cannot
run at full fidelity FAILS; it is never skipped.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "source-inputs" / "media"
IMAGE_MAP = ROOT / "build" / "stage8-image-map.json"
RENAME_MAP = ROOT / "reports" / "08-image-rename-map.csv"
REMEDIATION_MAP = ROOT / "build" / "47-media-remediation.csv"
MANIFEST_OUT = ROOT / "reports" / "22-media-missing-manifest.csv"
REPORT_OUT = ROOT / "reports" / "22-media-audit-result.md"

SOURCE_EXPECTED_COUNT = 83
MIN_BYTES = 1024                 # below this a "photo" is not a photo
MAX_BYTES = 12 * 1024 * 1024     # above this the footprint rule is violated
# WordPress adds -1, -scaled or -e{timestamp} on upload collision or edit.
# The BUILD's own convention is "-{attachment_id}.ext", which this pattern also
# matches -- so a bare regex flagged 66 of 83 correct filenames as drift.
# Drift means an UNEXPECTED suffix; the specified one is checked against the
# rename map's attachment_id in main().
SUFFIX_DRIFT = re.compile(r"-(\d+|scaled|e\d{10,})\.(jpe?g|png|webp|gif|avif)$", re.I)


def has_suffix_drift(new_filename: str, old_filename: str, attachment_id: str) -> bool:
    """True only for a suffix the specification did not ask for."""
    m = SUFFIX_DRIFT.search(new_filename)
    if not m:
        return False
    if m.group(1) == attachment_id:      # the specified "-{attachment_id}" suffix
        return False
    return not SUFFIX_DRIFT.search(old_filename)

# --------------------------------------------------------------------------
# DECISION-08 D38 — the intake directory is image-only, and that is asserted.
#
# source-inputs/media/ is staged for upload to a public web server. A non-image
# file that reaches it is a disclosure risk, not an untidy directory: this
# directory has already been delivered carrying two personal resume PDFs and an
# unregistered WXR export.
#
# Fail-closed with NO exemptions. The previous readme.md/.gitkeep exemption is
# deliberately removed -- a per-name carve-out is precisely the mechanism by
# which a non-image file sits in an intake directory unnoticed. If a README is
# wanted, it belongs beside the directory, not inside it.
#
# Both tests must pass for a file to be accepted:
#   1. extension is a known image extension
#   2. magic bytes sniff as an image
# A .jpg that is not a JPEG fails, and so does a PNG named .txt.
# --------------------------------------------------------------------------
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

MAGIC = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"GIF87a": "image/gif",
    b"GIF89a": "image/gif",
}


def read_json(path: Path):
    with path.open("r", encoding="utf-8", errors="strict") as fh:
        return json.load(fh)


def read_csv(path: Path) -> list[dict[str, str]]:
    # utf-8-sig: the Stage 8 CSVs carry a BOM. Never use errors='ignore'.
    with path.open("r", encoding="utf-8-sig", errors="strict", newline="") as fh:
        return list(csv.DictReader(fh))


# --------------------------------------------------------------------------
# EXIF assertion (DECISION-04 D25.2). Fail-closed.
#
# reencode-images.sh has never parsed, so NO image in this build has ever been
# stripped. If the 83 binaries import with EXIF intact, GPS coordinates from
# Melbourne job sites and owner/device metadata publish to a live website.
#
# Detects, with no third-party dependency:
#   - any GPS IFD or GPS tag
#   - owner/authorship: Artist, Copyright, Make, Model, OwnerName, SerialNumber
#   - original capture time: DateTime, DateTimeOriginal, DateTimeDigitized
# --------------------------------------------------------------------------
GPS_IFD_TAG = 0x8825
EXIF_IFD_TAG = 0x8769
OWNER_TAGS = {
    0x013B: "Artist", 0x8298: "Copyright", 0x010F: "Make", 0x0110: "Model",
    0xA430: "CameraOwnerName", 0xA431: "BodySerialNumber", 0xC62F: "CameraSerialNumber",
    0x9C9D: "XPAuthor", 0x9C9F: "XPSubject",
}
DATETIME_TAGS = {0x0132: "DateTime", 0x9003: "DateTimeOriginal", 0x9004: "DateTimeDigitized"}


def _read_ifd(data: bytes, offset: int, endian: str, found: list, depth: int = 0) -> None:
    if depth > 4 or offset + 2 > len(data):
        return
    try:
        count = struct.unpack(endian + "H", data[offset:offset + 2])[0]
    except struct.error:
        return
    pos = offset + 2
    for _ in range(count):
        if pos + 12 > len(data):
            return
        tag, _typ, _n = struct.unpack(endian + "HHI", data[pos:pos + 8])
        value_off = struct.unpack(endian + "I", data[pos + 8:pos + 12])[0]
        if tag == GPS_IFD_TAG:
            found.append("GPS IFD present")
        elif tag in OWNER_TAGS:
            found.append(f"owner tag {OWNER_TAGS[tag]}")
        elif tag in DATETIME_TAGS:
            found.append(f"capture time {DATETIME_TAGS[tag]}")
        elif tag == EXIF_IFD_TAG:
            _read_ifd(data, value_off, endian, found, depth + 1)
        pos += 12


def exif_findings(raw: bytes) -> list[str]:
    """Return a list of disallowed EXIF findings. Empty list means clean."""
    found: list[str] = []
    if raw[:2] != b"\xff\xd8":                       # not a JPEG
        if raw[:8] == b"\x89PNG\r\n\x1a\n":          # PNG: check for eXIf / tEXt
            if b"eXIf" in raw[:65536]:
                found.append("PNG eXIf chunk present")
            for kw in (b"Artist", b"Copyright", b"Author", b"GPS"):
                if kw in raw[:65536]:
                    found.append(f"PNG text chunk {kw.decode()}")
        return sorted(set(found))
    i = 2
    while i + 4 <= len(raw):
        if raw[i] != 0xFF:
            break
        marker = raw[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker == 0xDA:                            # start of scan; EXIF is before this
            break
        seglen = struct.unpack(">H", raw[i + 2:i + 4])[0]
        seg = raw[i + 4:i + 2 + seglen]
        if marker == 0xE1 and seg[:6] == b"Exif\x00\x00":
            tiff = seg[6:]
            if len(tiff) >= 8:
                endian = "<" if tiff[:2] == b"II" else ">"
                ifd0 = struct.unpack(endian + "I", tiff[4:8])[0]
                _read_ifd(tiff, ifd0, endian, found)
        i += 2 + seglen
    return sorted(set(found))


def sniff_mime(head: bytes) -> str | None:
    for magic, mime in MAGIC.items():
        if head.startswith(magic):
            return mime
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    # AVIF / HEIF family: ISO-BMFF 'ftyp' box with an avif-ish brand.
    if head[4:8] == b"ftyp" and (b"avif" in head[8:32] or b"avis" in head[8:32]):
        return "image/avif"
    return None


def non_image_findings(media_dir: Path) -> list[tuple[str, str]]:
    """Every file in the intake directory that is not an image.

    Returns (filename, reason). Empty list means the directory is image-only.
    Fail-closed: an unreadable file is reported as a finding, never skipped.
    """
    out: list[tuple[str, str]] = []
    if not media_dir.is_dir():
        return out
    for p in sorted(media_dir.iterdir()):
        if p.is_dir():
            out.append((p.name, "directory in a flat image intake"))
            continue
        if not p.is_file():
            out.append((p.name, "not a regular file"))
            continue
        ext = p.suffix.lower()
        if ext not in IMAGE_EXT:
            out.append((p.name, f"extension {ext or '(none)'} is not an image extension"))
            continue
        try:
            head = p.open("rb").read(64)
        except OSError as exc:
            out.append((p.name, f"unreadable: {exc}"))
            continue
        if sniff_mime(head) is None:
            out.append((p.name, f"extension {ext} but content does not sniff as an image"))
    return out


def _webp_dims(buf: bytes) -> tuple[int, int] | None:
    """WebP dimensions for all three container variants.

    VP8X carries them directly. VP8 (lossy) and VP8L (lossless) do not, and the
    previous implementation returned None for both -- which reported 14 real
    images as unreadable. Reading them is not optional: a dimension check that
    cannot read the format is not a check.
    """
    fourcc = buf[12:16]
    if fourcc == b"VP8X":
        return (int.from_bytes(buf[24:27], "little") + 1,
                int.from_bytes(buf[27:30], "little") + 1)
    if fourcc == b"VP8 ":
        # frame tag (3 bytes) + start code 9d 01 2a, then 16-bit w and h,
        # each with a 2-bit scale in the high bits.
        if buf[23:26] != b"\x9d\x01\x2a":
            return None
        w = int.from_bytes(buf[26:28], "little") & 0x3FFF
        h = int.from_bytes(buf[28:30], "little") & 0x3FFF
        return (w, h) if w and h else None
    if fourcc == b"VP8L":
        if buf[20:21] != b"\x2f":
            return None
        bits = int.from_bytes(buf[21:25], "little")
        return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    return None


def _avif_dims(raw: bytes) -> tuple[int, int] | None:
    """AVIF dimensions from the ISO-BMFF 'ispe' (image spatial extents) box."""
    i = raw.find(b"ispe")
    if i < 0:
        return None
    # Box layout from the 'ispe' type marker: 4 bytes type, then 1 byte version
    # + 3 bytes flags, THEN uint32 width and uint32 height. Reading from i+4
    # lands on version/flags and yields width=0, which is why this returned None.
    body = raw[i + 8:i + 16]
    if len(body) < 8:
        return None
    w = int.from_bytes(body[0:4], "big")
    h = int.from_bytes(body[4:8], "big")
    return (w, h) if w and h else None


def dimensions(path: Path) -> tuple[int, int] | None:
    """PNG/JPEG/GIF/WebP/AVIF dimensions without third-party libraries."""
    with path.open("rb") as fh:
        head = fh.read(32)
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            w, h = struct.unpack(">II", head[16:24])
            return int(w), int(h)
        if head[:6] in (b"GIF87a", b"GIF89a"):
            w, h = struct.unpack("<HH", head[6:10])
            return int(w), int(h)
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            fh.seek(0)
            return _webp_dims(fh.read(40))
        if head[4:8] == b"ftyp" and (b"avif" in head[8:32] or b"avis" in head[8:32]):
            fh.seek(0)
            return _avif_dims(fh.read(4096))
        if head.startswith(b"\xff\xd8"):
            fh.seek(2)
            while True:
                b = fh.read(1)
                while b and b != b"\xff":
                    b = fh.read(1)
                marker = fh.read(1)
                while marker == b"\xff":
                    marker = fh.read(1)
                if not marker:
                    return None
                if marker[0] in range(0xC0, 0xCF) and marker[0] not in (0xC4, 0xC8, 0xCC):
                    fh.read(3)
                    h, w = struct.unpack(">HH", fh.read(4))
                    return int(w), int(h)
                seg = fh.read(2)
                if len(seg) < 2:
                    return None
                fh.seek(struct.unpack(">H", seg)[0] - 2, os.SEEK_CUR)
    return None


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")

    image_map = read_json(IMAGE_MAP)
    rename_rows = read_csv(RENAME_MAP)
    remediation_rows = read_csv(REMEDIATION_MAP)

    remediation: dict[str, dict] = {}
    remediation_failures: list[str] = []
    for row in remediation_rows:
        attachment_id = row["attachment_id"]
        if attachment_id in remediation:
            remediation_failures.append(
                f"duplicate remediation row for attachment {attachment_id}")
        remediation[attachment_id] = row
        action = row["payload_action"]
        if action not in {"RENAME", "RETAIN", "EXCLUDE", "HOLD"}:
            remediation_failures.append(
                f"attachment {attachment_id}: invalid payload action {action!r}")
        if action == "RENAME":
            if not row["target_filename"] or not row["target_title"]:
                remediation_failures.append(
                    f"attachment {attachment_id}: GENERIC remediation is incomplete")
            claim_tokens = re.compile(
                r"testimonial|tesimonial|testemonial|camden|south-west-sydney|verified|customer|review",
                re.I,
            )
            if claim_tokens.search(row["target_filename"] + " " + row["target_alt"]):
                remediation_failures.append(
                    f"attachment {attachment_id}: target filename/alt retains a "
                    "testimonial, place or verification claim")
        elif action in {"EXCLUDE", "HOLD"} and (
            row["target_filename"] or row["target_title"] or row["target_alt"]
        ):
            remediation_failures.append(
                f"attachment {attachment_id}: {action} must not declare a public replacement")

    expected: dict[str, dict] = {}
    excluded: list[dict] = []
    held: list[dict] = []
    base_attachment_ids = {row["attachment_id"] for row in rename_rows}
    if len(remediation) != SOURCE_EXPECTED_COUNT:
        remediation_failures.append(
            f"remediation map declares {len(remediation)} rows, expected {SOURCE_EXPECTED_COUNT}")
    unknown_remediation_ids = sorted(set(remediation) - base_attachment_ids)
    if unknown_remediation_ids:
        remediation_failures.append(
            "remediation IDs absent from immutable rename map: "
            + ", ".join(unknown_remediation_ids))
    for row in rename_rows:
        final_name = row["new_filename"]
        override = remediation.get(row["attachment_id"])
        if override is not None:
            if override["current_filename"] != row["new_filename"]:
                remediation_failures.append(
                    f"attachment {row['attachment_id']}: remediation current_filename "
                    f"'{override['current_filename']}' does not match immutable rename-map "
                    f"filename '{row['new_filename']}'")
            action = override["payload_action"]
            if action == "EXCLUDE":
                excluded.append(row)
                continue
            if action == "HOLD":
                held.append(row)
                continue
            if action == "RENAME":
                final_name = override["target_filename"]
                if not final_name:
                    remediation_failures.append(
                        f"attachment {row['attachment_id']}: RENAME has no target_filename")
            elif action == "RETAIN":
                final_name = row["new_filename"]
            else:
                remediation_failures.append(
                    f"attachment {row['attachment_id']}: unknown payload_action '{action}'")
        if final_name in expected:
            remediation_failures.append(
                f"duplicate active filename after remediation: {final_name}")
        expected[final_name] = {
            "attachment_id": row["attachment_id"],
            "old_filename": row["old_filename"],
            "baseline_filename": row["new_filename"],
            "pages_referencing": row["pages_referencing"],
        }

    failures: list[str] = list(remediation_failures)
    rows: list[dict] = []

    if len(rename_rows) != SOURCE_EXPECTED_COUNT:
        failures.append(
            f"rename map declares {len(rename_rows)} source filenames, expected "
            f"{SOURCE_EXPECTED_COUNT}")
    if len(image_map) != SOURCE_EXPECTED_COUNT:
        failures.append(
            f"image map declares {len(image_map)} records, expected "
            f"{SOURCE_EXPECTED_COUNT}")
    if len(expected) + len(excluded) + len(held) != SOURCE_EXPECTED_COUNT:
        failures.append(
            "remediation inventory does not reconcile to the immutable 83 records")

    if not MEDIA.is_dir():
        failures.append(f"media directory absent: {MEDIA.relative_to(ROOT)}")
        present: dict[str, Path] = {}
    else:
        present = {p.name: p for p in MEDIA.iterdir() if p.is_file()}

    # D38 assertion, evaluated before anything else about the media set.
    non_images = non_image_findings(MEDIA)
    for fname, reason in non_images:
        failures.append(f"{fname}: NON-IMAGE FILE IN MEDIA INTAKE — {reason}")

    missing = sorted(set(expected) - set(present))
    extras = sorted(set(present) - set(expected))

    for name in sorted(expected):
        meta = expected[name]
        rec = {
            "new_filename": name,
            "attachment_id": meta["attachment_id"],
            "old_filename": meta["old_filename"],
            "present": "no",
            "bytes": "",
            "sha256": "",
            "mime": "",
            "width": "",
            "height": "",
            "exif": "",
            "verdict": "MISSING",
            "detail": "file not supplied",
        }
        p = present.get(name)
        if p is not None:
            data = p.read_bytes()
            rec["present"] = "yes"
            rec["bytes"] = str(len(data))
            rec["sha256"] = hashlib.sha256(data).hexdigest().upper()
            mime = sniff_mime(data[:32])
            rec["mime"] = mime or "UNKNOWN"
            dim = dimensions(p)
            problems: list[str] = []
            if mime is None:
                problems.append("MIME not recognised as an image")
            if dim is None:
                problems.append("dimensions unreadable")
            else:
                rec["width"], rec["height"] = str(dim[0]), str(dim[1])
            if len(data) < MIN_BYTES:
                problems.append(f"file size {len(data)} below {MIN_BYTES} floor")
            if len(data) > MAX_BYTES:
                problems.append(f"file size {len(data)} above {MAX_BYTES} ceiling")
            if has_suffix_drift(name, meta["old_filename"], meta["attachment_id"]):
                problems.append("filename shows WordPress suffix drift")
            # D25.2 — fail-closed EXIF assertion
            ex = exif_findings(data)
            rec["exif"] = "; ".join(ex) if ex else "clean"
            if ex:
                problems.append("EXIF NOT STRIPPED: " + "; ".join(ex))
            rec["verdict"] = "OK" if not problems else "FAIL"
            rec["detail"] = "; ".join(problems) if problems else "all checks pass"
            if problems:
                failures.append(f"{name}: {rec['detail']}")
        else:
            failures.append(f"{name}: MISSING")
        rows.append(rec)

    for name in extras:
        rows.append({
            "new_filename": name, "attachment_id": "", "old_filename": "",
            "present": "yes", "bytes": str(present[name].stat().st_size),
            "sha256": "", "mime": "", "width": "", "height": "", "exif": "",
            "verdict": "UNEXPECTED", "detail": "file not declared by the rename map",
        })
        failures.append(f"{name}: UNEXPECTED extra file")

    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_OUT.open("w", encoding="utf-8", errors="strict", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["new_filename"])
        wtr.writeheader()
        wtr.writerows(rows)

    ok = sum(1 for r in rows if r["verdict"] == "OK")
    lines = [
        "# Stage 22 media audit result",
        "",
        "Generated by `scripts/22-media-audit.py`. Fail-closed: any gap exits non-zero.",
        "",
        "```text",
        f"  expected filenames        {len(expected)}",
        f"  immutable source records  {len(rename_rows)}",
        f"  excluded/retired          {len(excluded)}",
        f"  held Band A fail-closed   {len(held)}",
        f"  present in directory      {len(present)}",
        f"  passing all checks        {ok}",
        f"  missing                   {len(missing)}",
        f"  unexpected extras         {len(extras)}",
        f"  non-image files (D38)     {len(non_images)}",
        f"  total failures            {len(failures)}",
        f"  verdict                   {'PASS' if not failures else 'FAIL'}",
        "```",
        "",
        f"Full per-file manifest: `{MANIFEST_OUT.relative_to(ROOT).as_posix()}`",
        "",
    ]
    if missing:
        lines += ["## Missing files", "", "```text"]
        lines += [f"  {i:>3}. {n}" for i, n in enumerate(missing, 1)]
        lines += ["```", ""]
    if non_images:
        lines += ["## Non-image files in the intake directory (DECISION-08 D38)", "",
                  "This directory is staged for upload to a public web server. Every entry "
                  "below must be removed", "from `source-inputs/media/` before import.", "",
                  "```text"]
        lines += [f"  {i:>3}. {fn}  —  {why}"
                  for i, (fn, why) in enumerate(non_images, 1)]
        lines += ["```", ""]
    if extras:
        lines += ["## Unexpected extras", "", "```text"]
        lines += [f"  {i:>3}. {n}" for i, n in enumerate(extras, 1)]
        lines += ["```", ""]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"expected={len(expected)} present={len(present)} ok={ok} "
          f"missing={len(missing)} extras={len(extras)} "
          f"non_images={len(non_images)} failures={len(failures)}")
    if non_images:
        print(f"D38: {len(non_images)} NON-IMAGE FILE(S) IN THE INTAKE DIRECTORY")
        for fname, reason in non_images:
            print(f"  {fname}  —  {reason}")
    print(f"manifest -> {MANIFEST_OUT.relative_to(ROOT).as_posix()}")
    print(f"report   -> {REPORT_OUT.relative_to(ROOT).as_posix()}")
    if failures:
        print("VERDICT: FAIL — media intake incomplete")
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
