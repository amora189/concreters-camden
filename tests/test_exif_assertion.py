"""D25.3 — verify the EXIF assertion catches a known-dirty file before it is trusted.

An assertion that has never been shown to fire is not evidence. This builds a
JPEG carrying GPS coordinates, an Artist tag and DateTimeOriginal, and asserts
that scripts/22-media-audit.py's detector reports all three. It then builds a
clean JPEG and asserts the detector stays silent.

Run:  python tests/test_exif_assertion.py
"""
from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("media_audit", ROOT / "scripts" / "22-media-audit.py")
media_audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media_audit)
exif_findings = media_audit.exif_findings

# Minimal 1x1 baseline JPEG, no EXIF.
CLEAN_JPEG = bytes.fromhex(
    "ffd8ffdb004300ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc20011"
    "08000100010101110000ffc40014000100000000000000000000000000000009ffda0008010100"
    "00013f10"
)


def build_dirty_jpeg() -> bytes:
    """A JPEG whose APP1 EXIF carries GPS, Artist and DateTimeOriginal."""
    endian = b"II"
    entries_ifd0 = []

    def entry(tag: int, typ: int, count: int, value: int) -> bytes:
        return struct.pack("<HHI I", tag, typ, count, value)

    # Values area starts after IFD0 (n entries * 12 + 2 + 4) and the two sub-IFDs.
    artist = b"J. Photographer\x00"
    dto = b"2026:07:06 13:52:19\x00"

    # Layout: TIFF header (8) | IFD0 | EXIF IFD | GPS IFD | value blob
    n0 = 3                      # Artist, ExifIFD pointer, GPSIFD pointer
    ifd0_off = 8
    ifd0_size = 2 + n0 * 12 + 4
    exif_off = ifd0_off + ifd0_size
    n_exif = 1                  # DateTimeOriginal
    exif_size = 2 + n_exif * 12 + 4
    gps_off = exif_off + exif_size
    n_gps = 2                   # GPSLatitudeRef, GPSLatitude
    gps_size = 2 + n_gps * 12 + 4
    blob_off = gps_off + gps_size

    artist_off = blob_off
    dto_off = artist_off + len(artist)
    lat_off = dto_off + len(dto)
    lat = struct.pack("<IIIIII", 37, 1, 48, 1, 5000, 100)   # 37 deg 48' 50.00"

    ifd0 = struct.pack("<H", n0)
    ifd0 += entry(0x013B, 2, len(artist), artist_off)        # Artist
    ifd0 += entry(0x8769, 4, 1, exif_off)                    # ExifIFD pointer
    ifd0 += entry(0x8825, 4, 1, gps_off)                     # GPSIFD pointer
    ifd0 += struct.pack("<I", 0)

    exif_ifd = struct.pack("<H", n_exif)
    exif_ifd += entry(0x9003, 2, len(dto), dto_off)          # DateTimeOriginal
    exif_ifd += struct.pack("<I", 0)

    gps_ifd = struct.pack("<H", n_gps)
    gps_ifd += struct.pack("<HHI4s", 0x0001, 2, 2, b"S\x00\x00\x00")   # GPSLatitudeRef
    gps_ifd += entry(0x0002, 5, 3, lat_off)                  # GPSLatitude
    gps_ifd += struct.pack("<I", 0)

    tiff = endian + struct.pack("<HI", 42, ifd0_off) + ifd0 + exif_ifd + gps_ifd
    tiff += artist + dto + lat

    app1 = b"Exif\x00\x00" + tiff
    seg = struct.pack(">H", len(app1) + 2) + app1
    return CLEAN_JPEG[:2] + b"\xff\xe1" + seg + CLEAN_JPEG[2:]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    failures = 0

    print("TEST 1 — the assertion must FIRE on a known-dirty file")
    dirty = build_dirty_jpeg()
    found = exif_findings(dirty)
    print(f"  findings: {found}")
    for expected in ("GPS IFD present", "owner tag Artist", "capture time DateTimeOriginal"):
        ok = expected in found
        print(f"    {'PASS' if ok else 'FAIL'}  detects {expected}")
        failures += 0 if ok else 1

    print("\nTEST 2 — the assertion must STAY SILENT on a clean file")
    found_clean = exif_findings(CLEAN_JPEG)
    ok = found_clean == []
    print(f"  findings: {found_clean}")
    print(f"    {'PASS' if ok else 'FAIL'}  no false positive on a clean JPEG")
    failures += 0 if ok else 1

    print("\nTEST 3 — PNG text-chunk detection")
    png = (b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0btEXtArtist\x00J. Photographer"
           + b"\x00" * 32)
    found_png = exif_findings(png)
    ok = any("Artist" in f for f in found_png)
    print(f"  findings: {found_png}")
    print(f"    {'PASS' if ok else 'FAIL'}  detects PNG Artist text chunk")
    failures += 0 if ok else 1

    print(f"\nOVERALL: {'PASS' if failures == 0 else f'FAIL ({failures})'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
