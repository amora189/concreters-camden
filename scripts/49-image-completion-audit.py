#!/usr/bin/env python3
"""Generate the inspection-only image completion inventory for the 76 built pages.

The immutable WXR and the generated derivative are read-only inputs.  This
script inventories every Elementor image-capable slot in the 75 active main
WXR pages, adds the zero-slot privacy page and the two Astra brand slots, then
writes reports/49-image-completion-requirements.{csv,md}.

It deliberately does not mutate media, the derivative WXR, a decision, or an
immutable file.  Band A recommendations are audit findings only; a blank owner
worksheet remains blank and fail-closed.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "camden-concreting-import.xml"
DERIVATIVE = ROOT / "build" / "46-active-main-import.xml"
PRIVACY = ROOT / "camden-privacy-import.xml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
MANIFEST = ROOT / "build" / "47-media-remediation.csv"
WORKSHEET = ROOT / "reports" / "44-sighting-worksheet.csv"
CSV_OUT = ROOT / "reports" / "49-image-completion-requirements.csv"
MD_OUT = ROOT / "reports" / "49-image-completion-requirements.md"

WP = "{http://wordpress.org/export/1.2/}"

IMMUTABLES = {
    "camden-concreting-import.xml": "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884",
    "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml": "45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15",
    "build/stage9-page-manifest.json": "578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42",
    "build/stage8-image-map.json": "0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF",
    "reports/08-image-rename-map.csv": "43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8",
    "CODEX-BUILD-2.1.md": "BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C",
    "archive/governing/CODEX-BUILD-2.md": "E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5",
}

CSV_COLUMNS = [
    "requirement_id", "wave", "page_slug", "page_type", "elementor_widget_id",
    "section", "slot_classification", "required_or_optional", "asset_source",
    "subject", "orientation", "aspect_ratio", "min_dimensions", "preferred_format",
    "safe_filename", "alt_text_rule", "geographic_claim_allowed", "evidence_required",
    "reuse_allowed", "current_attachment_id", "current_filename", "required_action",
    "owner_input", "blocks_launch", "notes",
]

CONDITIONAL_MINIMUM = {"homepage", "about", "contact", "privacy-policy"}
PLACEHOLDER_ASSETS = {275, 276, 277, 278, 279, 323}
BRAND_SLOT_ASSETS = {306, 307}

# Visual inspection recommendations.  These do not populate the owner worksheet.
BAND_A_RECOMMENDATIONS = {
    907: ("UNUSABLE", "Identifiable Werribee heritage mansion and gardens; no concrete subject", "", ""),
    924: ("GENERIC", "Coloured residential concrete patio", "coloured-concrete-patio-924.png", "Coloured concrete patio beside a home"),
    226: ("GENERIC", "Freshly finished residential side-yard slab", "fresh-concrete-side-yard-slab-226.jpg", "Freshly finished concrete slab in a residential side yard"),
    1185: ("GENERIC", "Dark concrete driveway crossing", "dark-concrete-driveway-crossing-1185.jpg", "Dark concrete driveway crossing between a kerb and property"),
    906: ("GENERIC", "Excavated residential area", "residential-site-excavation-906.jpg", "Excavated residential area prepared for concrete work"),
    1150: ("GENERIC", "Single-storey brick home with driveway", "single-storey-brick-home-driveway-1150.jpg", "Single-storey brick home with a concrete driveway"),
    1186: ("GENERIC", "Modern commercial building with concrete hardstand", "commercial-building-concrete-hardstand-1186.webp", "Modern commercial building with a concrete hardstand"),
    1187: ("UNUSABLE", "Estate playground with prominent M locality branding; no concrete subject", "", ""),
    1152: ("GENERIC", "Aerial landscaped park surrounded by housing", "aerial-suburban-park-and-housing-1152.jpg", "Aerial view of a landscaped park surrounded by housing"),
    908: ("GENERIC", "Aerial view of a developing housing estate", "aerial-new-housing-estate-908.jpg", "Aerial view of a developing suburban housing estate"),
    480: ("UNUSABLE", "Synthetic turf and timber landscaping; no concrete subject", "", ""),
    481: ("UNUSABLE", "Timber bench or deck; no concrete subject", "", ""),
    482: ("UNUSABLE", "Timber deck framing and bare ground; no concrete subject", "", ""),
    956: ("UNUSABLE", "Identifiable Melbourne CBD skyline and hot-air balloon", "", ""),
    926: ("GENERIC", "Stamped concrete driveway", "stamped-concrete-driveway-926.jpg", "Stamped concrete driveway beside a brick home"),
    925: ("GENERIC", "Stencilled or patterned concrete driveway", "stencilled-concrete-driveway-925.webp", "Stencilled concrete driveway with a block pattern"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def clean_text(value: Any) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))
    return re.sub(r"\s+", " ", text).strip()


def elementor_text(value: Any) -> str:
    """Decode both classic strings and Elementor 4.2 typed text values."""
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        return clean_text(" ".join(elementor_text(part) for part in value))
    if not isinstance(value, dict):
        return ""
    if value.get("$$type") == "string":
        return clean_text(value.get("value"))
    if value.get("$$type") == "html-v3":
        return elementor_text(value.get("value", {}).get("content"))
    if "content" in value:
        decoded = elementor_text(value.get("content"))
        if decoded:
            return decoded
    if "value" in value:
        decoded = elementor_text(value.get("value"))
        if decoded:
            return decoded
    return ""


def page_items(path: Path) -> dict[int, ET.Element]:
    tree = ET.parse(path)
    result: dict[int, ET.Element] = {}
    for item in tree.findall("./channel/item"):
        if (item.findtext(WP + "post_type") or "").strip() != "page":
            continue
        pid = int(item.findtext(WP + "post_id") or 0)
        if pid in result:
            raise AssertionError(f"duplicate page ID {pid} in {path.name}")
        result[pid] = item
    return result


def elementor_data(item: ET.Element) -> list[dict[str, Any]]:
    for meta in item.findall(WP + "postmeta"):
        if (meta.findtext(WP + "meta_key") or "").strip() == "_elementor_data":
            raw = meta.findtext(WP + "meta_value") or ""
            return json.loads(raw) if raw.strip() else []
    return []


def simple_image_ref(value: Any) -> tuple[int | None, str, str]:
    """Return (attachment id, URL, alt) for classic and Elementor 4.2 image values."""
    if not isinstance(value, dict):
        return None, "", ""
    raw_id = value.get("id")
    if str(raw_id or "").isdigit():
        return int(raw_id), str(value.get("url") or ""), str(value.get("alt") or "")
    if value.get("$$type") == "image":
        inner = value.get("value", {}).get("src", {}).get("value", {})
        nested_id = inner.get("id", {}).get("value")
        if str(nested_id or "").isdigit():
            nested_url = inner.get("url")
            if isinstance(nested_url, dict):
                nested_url = nested_url.get("value")
            return int(nested_id), str(nested_url or ""), ""
    return None, str(value.get("url") or ""), str(value.get("alt") or "")


def section_label(node: dict[str, Any]) -> str:
    labels: list[str] = []

    def walk(value: Any) -> None:
        if len(labels) >= 3:
            return
        if isinstance(value, dict):
            settings = value.get("settings")
            if isinstance(settings, dict):
                for key in ("title", "heading_title", "title_text", "testimonial_name"):
                    label = elementor_text(settings.get(key))
                    if label and "PLACEHOLDER" not in label and label not in labels:
                        labels.append(label)
                        break
            for child in value.get("elements", []) if isinstance(value.get("elements"), list) else []:
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(node)
    return " / ".join(labels) if labels else "Untitled Elementor section"


def extract_slots(pid: int, slug: str, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []

    def visit(node: Any, section_id: str, section_name: str) -> None:
        if not isinstance(node, dict):
            return
        wid = str(node.get("id") or "unknown")
        widget_type = str(node.get("widgetType") or node.get("elType") or "element")
        settings = node.get("settings") if isinstance(node.get("settings"), dict) else {}
        title = elementor_text(
            settings.get("title_text") or settings.get("title") or settings.get("heading_title")
            or settings.get("testimonial_name") or ""
        )
        for setting_key in ("image", "background_image", "testimonial_image"):
            if setting_key not in settings:
                continue
            aid, url, alt = simple_image_ref(settings.get(setting_key))
            # Empty testimonial portraits are image-capable slots and must be inventoried.
            if aid is None and not (widget_type == "testimonial" and setting_key == "testimonial_image"):
                continue
            slots.append(
                {
                    "page_id": pid,
                    "slug": slug,
                    "section_id": section_id,
                    "section_name": section_name,
                    "widget_id": wid,
                    "widget_type": widget_type,
                    "setting": setting_key,
                    "attachment_id": aid,
                    "url": url,
                    "alt": alt,
                    "purpose": title or section_name,
                    "testimonial_text": elementor_text(settings.get("testimonial_content")),
                    "testimonial_name": elementor_text(settings.get("testimonial_name")),
                }
            )
        for child in node.get("elements", []) if isinstance(node.get("elements"), list) else []:
            visit(child, section_id, section_name)

    for index, top in enumerate(data):
        if not isinstance(top, dict):
            continue
        section_id = str(top.get("id") or f"top-{index}")
        name = section_label(top)
        visit(top, section_id, name)
    return slots


def key(slot: dict[str, Any]) -> tuple[str, str, str]:
    return slot["section_id"], slot["widget_id"], slot["setting"]


def dims(value: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"(\d+)x(\d+)", (value or "").strip())
    return (int(match.group(1)), int(match.group(2))) if match else None


def geometry(value: str) -> tuple[str, str]:
    parsed = dims(value)
    if not parsed:
        return "not applicable", "not applicable"
    width, height = parsed
    orientation = "square" if width == height else "landscape" if width > height else "portrait"
    from math import gcd
    divisor = gcd(width, height)
    return orientation, f"{width // divisor}:{height // divisor}"


def format_name(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    return {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WebP", ".avif": "AVIF", ".svg": "SVG"}.get(suffix, suffix.lstrip(".").upper() or "not applicable")


def normalise_wave(raw: str, slug: str) -> str:
    prefix = "conditional-minimum; " if slug in CONDITIONAL_MINIMUM else ""
    if raw == "1":
        return prefix + "Wave 1"
    if raw.startswith("3"):
        return "Wave 3 pending research"
    if "unresearched" in raw:
        return "D22 deferred — unresearched"
    return prefix + raw


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    for rel, expected in IMMUTABLES.items():
        actual = sha256(ROOT / rel)
        if actual != expected:
            raise AssertionError(f"immutable mismatch: {rel}: {actual} != {expected}")

    allow_doc = json.loads(ALLOWLIST.read_text(encoding="utf-8", errors="strict"))
    allow_pages = {int(p["page_id"]): p for p in allow_doc["pages"]}
    if len(allow_pages) != 76 or 1600 not in allow_pages:
        raise AssertionError("built allowlist is not 76 pages including privacy")
    source_pages = page_items(SOURCE)
    derived_pages = page_items(DERIVATIVE)
    active_main_ids = set(allow_pages) - {1600}
    if set(derived_pages) != active_main_ids:
        raise AssertionError("derivative page IDs differ from the 75 active main allowlist rows")

    manifest_rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig", newline="")))
    manifest = {int(r["attachment_id"]): r for r in manifest_rows}
    worksheet_rows = list(csv.DictReader(WORKSHEET.open(encoding="utf-8-sig", newline="")))
    worksheet = {int(r["attachment_id"]): r for r in worksheet_rows}
    band_a = [r for r in worksheet_rows if r["band"].strip().upper() == "A"]
    if len(band_a) != 16:
        raise AssertionError(f"Band A worksheet count is {len(band_a)}, expected 16")
    if set(BAND_A_RECOMMENDATIONS) != {int(r["attachment_id"]) for r in band_a}:
        raise AssertionError("Band A recommendation IDs do not match worksheet")

    page_slots: dict[int, list[dict[str, Any]]] = {}
    derivative_keys: dict[int, set[tuple[str, str, str]]] = {}
    derivative_sections: dict[int, set[str]] = {}
    for pid in sorted(active_main_ids):
        slug = allow_pages[pid]["slug"]
        page_slots[pid] = extract_slots(pid, slug, elementor_data(source_pages[pid]))
        derived_data = elementor_data(derived_pages[pid])
        dslots = extract_slots(pid, slug, derived_data)
        derivative_keys[pid] = {key(s) for s in dslots}
        derivative_sections[pid] = {str(node.get("id") or f"top-{i}") for i, node in enumerate(derived_data) if isinstance(node, dict)}

    source_slots = [slot for pid in sorted(page_slots) for slot in page_slots[pid]]
    if len(source_slots) != 610:
        raise AssertionError(f"active source image-capable slots {len(source_slots)} != 610")
    populated_source = [s for s in source_slots if s["attachment_id"] is not None]
    empty_source = [s for s in source_slots if s["attachment_id"] is None]
    if (len(populated_source), len(empty_source)) != (607, 3):
        raise AssertionError("expected 607 populated plus three empty testimonial slots")
    derivative_slot_rows = [
        slot
        for pid in active_main_ids
        for slot in extract_slots(pid, allow_pages[pid]["slug"], elementor_data(derived_pages[pid]))
    ]
    current_slots = sum(slot["attachment_id"] is not None for slot in derivative_slot_rows)
    if (len(derivative_slot_rows), current_slots) != (413, 410):
        raise AssertionError(
            "expected derivative 413 image-capable slots = 410 populated + 3 empty; "
            f"got {len(derivative_slot_rows)} = {current_slots} populated"
        )

    rows: list[dict[str, str]] = []
    per_asset_slots: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for slot in populated_source:
        per_asset_slots[int(slot["attachment_id"])].append(slot)

    for sequence, slot in enumerate(source_slots, 1):
        pid = int(slot["page_id"])
        aid = slot["attachment_id"]
        page = allow_pages[pid]
        slug = slot["slug"]
        wave = normalise_wave(str(page["evidence_readiness_state"]["wave"]), slug)
        present = key(slot) in derivative_keys[pid]
        whole_section_removed = slot["section_id"] not in derivative_sections[pid]
        row_manifest = manifest.get(int(aid)) if aid is not None else None
        sheet = worksheet.get(int(aid)) if aid is not None else None
        band = (row_manifest or {}).get("band", "")
        action = (row_manifest or {}).get("payload_action", "")
        current_filename = (row_manifest or {}).get("target_filename") if present else (row_manifest or {}).get("current_filename", "")
        current_filename = current_filename or ((sheet or {}).get("new_filename", ""))
        dimension = (sheet or {}).get("dimensions", "")
        orientation, ratio = geometry(dimension)
        rec = BAND_A_RECOMMENDATIONS.get(int(aid)) if aid is not None else None
        recommended = rec[0] if rec else ""
        visual_subject = rec[1] if rec else (row_manifest or {}).get("target_alt") or clean_text(slot["alt"]) or "Decorative image"
        safe_filename = rec[2] if rec and rec[0] == "GENERIC" else ((row_manifest or {}).get("target_filename") or "")
        alt_rule = rec[3] if rec and rec[0] == "GENERIC" else ((row_manifest or {}).get("target_alt") or "Describe only the visible subject; empty alt if purely decorative")
        geographic_source = (sheet or {}).get("claim_made", "") if band == "A" else "none in permitted derivative"

        classification = "EXISTING-APPROVED"
        required = "optional"
        asset_source = "existing re-encoded media"
        evidence = (row_manifest or {}).get("authority", "recorded public-media manifest")
        reuse = "yes — decorative/non-evidential only"
        owner_input = "none"
        blocks = "no"
        required_action = "retain current generic placement"
        evidential = "decorative"
        removability = "can be removed without loss of page meaning"
        permission = "pipeline-permitted in derivative" if present else "not in derivative"

        # The exact-one classification is launch-oriented.  Deferred-page rows
        # retain their eventual media disposition in notes/action.
        if "Wave 3" in wave or "D22 deferred" in wave:
            classification = "DEFERRED"
            required_action = "defer with page; before future release apply the recorded underlying media disposition"
            blocks = "no — page is outside the smallest launch"
        elif whole_section_removed:
            classification = "OPTIONAL-REMOVE"
            evidential = "evidential local-project/gallery module"
            required_action = "keep the D32 section removed; do not source a substitute"
            evidence = "D32: no Camden projects; remove evidential module"
            reuse = "no in this evidential placement"
            permission = "slot removed from derivative"
        elif aid is None:
            classification = "OPTIONAL-REMOVE"
            evidential = "testimonial/review"
            visual_subject = "Empty reviewer portrait beside placeholder testimonial copy"
            current_filename = ""
            safe_filename = ""
            alt_rule = "not applicable — remove the testimonial widget"
            evidence = "reports/45-testimonial-audit.md: unsupported placeholder testimonial"
            reuse = "no"
            required_action = "remove the complete placeholder testimonial widget, not only its empty portrait"
            owner_input = "none unless a genuine documented testimonial is later supplied"
            blocks = "yes for homepage publication"
            permission = "not permitted as a testimonial"
        elif aid in BRAND_SLOT_ASSETS:
            classification = "OWNER-BRAND"
            required = "required"
            asset_source = "already supplied Structure Co brand pack"
            visual_subject = "Structure Co horizontal wordmark"
            safe_filename = "structure-co-horizontal.svg"
            alt_rule = "Structure Co Concreters Camden"
            orientation, ratio, dimension = "vector/adaptive", "asset-native", "SVG vector"
            evidence = "D36 and source-inputs/brand/ supplied asset hashes"
            reuse = "yes — same wordmark may serve every in-page logo slot"
            required_action = "replace retired E&T attachment with supplied Structure Co wordmark during authorised import"
            owner_input = "no new file; later approve rendered placement"
            blocks = "yes for any page retaining this brand slot"
            permission = "retired attachment excluded; verified replacement already supplied"
        elif action == "EXCLUDE":
            classification = "OPTIONAL-REMOVE"
            required_action = "keep the prohibited asset and every direct slot removed; do not replace"
            evidence = (row_manifest or {}).get("authority", "recorded exclusion")
            reuse = "no"
            permission = "asset excluded from public payload"
        elif band == "A":
            classification = "BLOCKED-PENDING-VERDICT"
            evidential = "geographic-claim-bearing in source; decorative only if owner selects GENERIC"
            safe_filename = rec[2] if rec else ""
            alt_rule = rec[3] if rec and rec[0] == "GENERIC" else "remove with slot if UNUSABLE; no local alt is permitted without provenance"
            evidence = "No Camden/NSW provenance in repository; original Victorian filename is provenance of source, not NSW provenance"
            reuse = "yes only if owner records GENERIC" if recommended == "GENERIC" else "no — recommended UNUSABLE"
            required_action = f"owner records verdict; audit recommends {recommended}; transformer then regenerates derivative"
            owner_input = f"record explicit {recommended} (or another supported verdict) in worksheet; OK additionally needs documentary provenance"
            blocks = "yes — Band A public-media gate"
            permission = "HOLD; absent from derivative and public media"
        elif aid in PLACEHOLDER_ASSETS:
            classification = "OPTIONAL-REMOVE"
            visual_subject = "Blank image-placeholder graphic"
            safe_filename = ""
            alt_rule = "not applicable — remove blank placeholder slot"
            evidence = "pixel inspection of local binary; blank placeholder icon only"
            reuse = "no"
            required_action = "remove this visual placeholder without replacement"
            owner_input = "none"
            permission = "currently pipeline-permitted, but visually unusable"

        if classification == "DEFERRED":
            underlying = ""
            if whole_section_removed:
                underlying = "D32 section already removed"
            elif aid in BRAND_SLOT_ASSETS:
                underlying = "replace with supplied Structure Co wordmark"
                owner_input = "no new file; later approve rendered placement"
                required = "deferred; required if page is retained"
            elif action == "EXCLUDE":
                underlying = "prohibited slot already removed"
            elif band == "A":
                underlying = f"Band A HOLD; audit recommends {recommended}"
                permission = "HOLD; absent from derivative"
                owner_input = f"record explicit {recommended} (or another supported verdict); OK also requires cited provenance"
                blocks = "yes for Phase B/staging; page publication is deferred"
            elif aid in PLACEHOLDER_ASSETS:
                underlying = "blank placeholder; remove before future release"
            else:
                underlying = "permitted generic decoration"
            required_action += f"; underlying: {underlying}"

        title = slot["purpose"]
        subject = f"{visual_subject}; visible purpose: {title}"
        notes = (
            f"page_id={pid}; widget_type={slot['widget_type']}; setting={slot['setting']}; "
            f"{evidential}; permission={permission}; source_geographic_claim={geographic_source}; "
            f"project_claim={'yes' if evidential != 'decorative' else 'no'}; {removability}; "
            f"derivative_slot={'present' if present else 'absent'}"
        )
        rows.append(
            {
                "requirement_id": f"IMG-{sequence:04d}",
                "wave": wave,
                "page_slug": slug,
                "page_type": page["page_type"],
                "elementor_widget_id": slot["widget_id"],
                "section": f"{slot['section_id']} — {slot['section_name']}",
                "slot_classification": classification,
                "required_or_optional": required,
                "asset_source": asset_source,
                "subject": subject,
                "orientation": orientation,
                "aspect_ratio": ratio,
                "min_dimensions": dimension or "not applicable",
                "preferred_format": format_name(safe_filename or current_filename),
                "safe_filename": safe_filename,
                "alt_text_rule": alt_rule,
                "geographic_claim_allowed": "no",
                "evidence_required": evidence,
                "reuse_allowed": reuse,
                "current_attachment_id": "" if aid is None else str(aid),
                "current_filename": current_filename,
                "required_action": required_action,
                "owner_input": owner_input,
                "blocks_launch": blocks,
                "notes": notes,
            }
        )

    # Theme-mod slots are outside page Elementor JSON but are genuine launch
    # brand requirements.  The assets are already supplied; neither is a new
    # owner photograph requirement.
    for suffix, page_slug, section, subject, filename, alt in (
        ("H", "GLOBAL-header", "Astra header logo slot", "Structure Co horizontal wordmark", "structure-co-horizontal.svg", "Structure Co Concreters Camden"),
        ("I", "GLOBAL-site-icon", "WordPress site icon slot", "Structure Co icon", "structure-co-icon.svg", "Structure Co"),
    ):
        rows.append(
            {
                "requirement_id": f"IMG-BRAND-{suffix}", "wave": "conditional-minimum; global",
                "page_slug": page_slug, "page_type": "theme/global", "elementor_widget_id": "not Elementor",
                "section": section, "slot_classification": "OWNER-BRAND", "required_or_optional": "required",
                "asset_source": "already supplied Structure Co brand pack", "subject": subject,
                "orientation": "vector/adaptive", "aspect_ratio": "asset-native", "min_dimensions": "SVG vector",
                "preferred_format": "SVG", "safe_filename": filename, "alt_text_rule": alt,
                "geographic_claim_allowed": "no location claim", "evidence_required": "D36 and supplied brand pack hashes",
                "reuse_allowed": "yes in the matching brand role", "current_attachment_id": "469" if suffix == "H" else "472",
                "current_filename": "retired E&T header logo" if suffix == "H" else "retired E&T site icon",
                "required_action": "assign supplied Structure Co asset during authorised import; keep retired E&T attachment unavailable",
                "owner_input": "no new file; later approve rendered placement", "blocks_launch": "yes",
                "notes": "global slot; supplied replacement exists; no import performed in this audit",
            }
        )

    if list(rows[0]) != CSV_COLUMNS or any(list(r) != CSV_COLUMNS for r in rows):
        raise AssertionError("CSV row schema/order differs from required exact columns")
    with CSV_OUT.open("w", encoding="utf-8", errors="strict", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    # Mechanically re-read the output before using it for report totals.
    with CSV_OUT.open("r", encoding="utf-8", errors="strict", newline="") as handle:
        check_rows = list(csv.DictReader(handle))
        if len(check_rows) != len(rows) or list(check_rows[0]) != CSV_COLUMNS:
            raise AssertionError("CSV round-trip verification failed")
        if len({r["requirement_id"] for r in check_rows}) != len(check_rows):
            raise AssertionError("CSV requirement IDs are not unique")

    page_rows = rows[:-2]
    class_counts = Counter(r["slot_classification"] for r in page_rows)
    wave_counts = Counter(
        "Wave 1" if "Wave 1" in r["wave"] else "Wave 3" if "Wave 3" in r["wave"] else "D22"
        for r in page_rows
    )
    # All 51 permitted manifest assets are mechanically available, but the six
    # literal placeholder graphics are not useful/safe imagery.  The remaining
    # 45 are the site-wide existing generic asset pool, regardless of whether a
    # particular placement is on a deferred page.
    safe_asset_ids = {
        int(r["attachment_id"]) for r in manifest_rows
        if r["payload_action"] in {"RENAME", "RETAIN"}
        and int(r["attachment_id"]) not in PLACEHOLDER_ASSETS
    }
    placeholder_slot_count = sum(
        1 for r in page_rows if r["current_attachment_id"].isdigit() and int(r["current_attachment_id"]) in PLACEHOLDER_ASSETS
    )
    direct_band_a_slots = sum(
        1 for slot in source_slots
        if slot["attachment_id"] in BAND_A_RECOMMENDATIONS
        and slot["section_id"] in derivative_sections[int(slot["page_id"])]
    )
    recommended_remove_slots = sum(
        1 for slot in source_slots
        if (
            slot["section_id"] not in derivative_sections[int(slot["page_id"])]
            or slot["attachment_id"] is None
            or (
                slot["attachment_id"] not in BRAND_SLOT_ASSETS
                and (
                    (manifest.get(int(slot["attachment_id"])) or {}).get("payload_action") == "EXCLUDE"
                    or slot["attachment_id"] in PLACEHOLDER_ASSETS
                    or (
                        slot["attachment_id"] in BAND_A_RECOMMENDATIONS
                        and BAND_A_RECOMMENDATIONS[int(slot["attachment_id"])][0] == "UNUSABLE"
                    )
                )
            )
        )
    )
    useful_derivative_slots = sum(
        1 for slot in derivative_slot_rows
        if slot["attachment_id"] is not None and slot["attachment_id"] not in PLACEHOLDER_ASSETS
    )
    placeholder_derivative_slots = sum(
        1 for slot in derivative_slot_rows
        if slot["attachment_id"] is not None and slot["attachment_id"] in PLACEHOLDER_ASSETS
    )
    decided_removal_slots = sum(
        1 for r in page_rows
        if r["slot_classification"] == "OPTIONAL-REMOVE"
    )
    conditional_rows = [r for r in page_rows if r["page_slug"] in CONDITIONAL_MINIMUM]
    conditional_safe = {r["current_attachment_id"] for r in conditional_rows if r["slot_classification"] == "EXISTING-APPROVED" and r["current_attachment_id"]}
    conditional_brand = sum(r["slot_classification"] == "OWNER-BRAND" for r in conditional_rows) + 2
    band_a_blank = sum(not (r.get("VERDICT") or "").strip() for r in band_a)
    band_b_rows = [r for r in worksheet_rows if r["band"].strip().upper() == "B"]
    band_b_decided = sum(bool((r.get("VERDICT") or "").strip()) for r in band_b_rows)

    # Band A table and exact active placements.
    band_a_lines = []
    for sheet in sorted(band_a, key=lambda r: int(r["#"])):
        aid = int(sheet["attachment_id"])
        recommendation, visible, safe, _alt = BAND_A_RECOMMENDATIONS[aid]
        placements = []
        for slot in per_asset_slots[aid]:
            placements.append(
                f"/{slot['slug']}/ §{slot['section_id']} widget {slot['widget_id']} ({slot['widget_type']}:{slot['setting']})"
            )
        missing = (
            f"owner {recommendation} verdict"
            + ("; no new photograph needed" if recommendation in {"GENERIC", "UNUSABLE"} else "")
        )
        treatment = recommendation
        reason = (
            "Legitimate visible subject can be reused only as generic, non-evidential decoration; remove all locality/project implication."
            if recommendation == "GENERIC"
            else "Generic relabelling cannot cure the identifiable false locality or the absence of a concrete-related subject; remove every slot."
        )
        if recommendation == "GENERIC":
            treatment += f" → `{safe}`; alt `{_alt}`"
        band_a_lines.append(
            "| " + " | ".join(
                md_escape(v) for v in (
                    sheet["#"], aid, sheet["new_filename"], visible, sheet["claim_made"],
                    "none — original filename identifies a Victorian source", treatment, reason,
                    missing, "no", "; ".join(placements),
                )
            ) + " |"
        )

    # Page appendix: every page is present, including privacy's explicit zero.
    appendix_lines = []
    row_by_slug: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in page_rows:
        row_by_slug[row["page_slug"]].append(row)
    for pid, page in sorted(allow_pages.items(), key=lambda pair: (pair[1]["page_type"], pair[1]["slug"])):
        slug = page["slug"]
        these = row_by_slug.get(slug, [])
        derivative_count = sum(
            "derivative_slot=present" in r["notes"] and bool(r["current_attachment_id"])
            for r in these
        )
        counts = Counter(r["slot_classification"] for r in these)
        placements = "; ".join(
            f"{r['elementor_widget_id']}:{r['current_attachment_id'] or 'empty'}[{r['slot_classification']}]"
            for r in these
        ) or "none"
        appendix_lines.append(
            f"| {pid} | /{md_escape(slug)}/ | {md_escape(page['page_type'])} | {len(these)} | {derivative_count} | "
            f"{md_escape(', '.join(f'{k}={v}' for k, v in sorted(counts.items())) or 'no image slots')} | {md_escape(placements)} |"
        )

    hash_lines = [
        f"| `{rel}` | `{sha256(ROOT / rel)}` | MATCH |" for rel in IMMUTABLES
    ]
    derivative_hash = sha256(DERIVATIVE)
    generic_a = sum(v[0] == "GENERIC" for v in BAND_A_RECOMMENDATIONS.values())
    unusable_a = sum(v[0] == "UNUSABLE" for v in BAND_A_RECOMMENDATIONS.values())

    report = f"""# Image completion requirements audit

Date: 20 August 2026  
Scope: 76 built active pages (75 in the derivative main WXR plus the separate privacy page), with withdrawn pages excluded.

## Plain-English answer

**New owner photographs proven necessary for the current minimum honest Wave 1: 0. New owner photographs proven necessary for all 76 built active pages: 0.** That is not permission to launch. With no verified accountable identity and no signed NSW operator, the genuinely honest live set is presently **zero pages**. If those non-image blockers are resolved, the smallest non-contractor publisher/holding set is `/` (page slug `homepage`), `/about/`, `/contact/` and `/privacy-policy/`; it can be built with existing generic decoration, the already supplied Structure Co brand files and removal of the unsupported testimonial module.

The exact owner-photo count is zero because no surviving page is allowed to depend on a purported local job, customer, team, operator, vehicle, equipment or premises photograph. D32 removes those evidential modules. Optional evidential slots are safer removed than filled. `/gallery/` is not honestly launchable as a project gallery without a new authentic project library and should be deferred or removed from the launch navigation.

There are **{len(safe_asset_ids)} unique existing images that this audit can retain as useful generic decoration**, occupying {useful_derivative_slots} current derivative slots. The six blank placeholder binaries have {placeholder_slot_count} active-source placements, of which {placeholder_derivative_slots} survive in the derivative; none is counted as safe. **{recommended_remove_slots} active-page slots should ultimately be removed** under decisions already made plus this audit's Band A/placeholder recommendations; {decided_removal_slots} of those are in current Wave 1 and receive the exact-one OPTIONAL-REMOVE classification, while later-page rows are classified DEFERRED with the removal action retained in notes. **{band_a_blank} asset requirements are blocked only by the 16 blank Band A owner verdicts.** All 16 lack NSW provenance. This audit recommends {generic_a} GENERIC and {unusable_a} UNUSABLE; if the owner records those verdicts, they require no new photographs.

“Zero new photographs” is a requirements result, not a completeness result: 16 Band A decisions still block the media gate, and the site has separate identity, claim, copy, legal and staging blockers.

## Ground verification

- Dirty tree: the repository has no tracked files; every path is reported by Git as untracked. No pre-existing change can be attributed to this pass through Git history.
- Active inventory: 156 immutable main-WXR pages = 75 active + 81 withdrawn; + one separate privacy page = 76 built active; the calculator remains unbuilt and excluded.
- Source active Elementor inventory: **610 image-capable slots = 607 populated + 3 empty testimonial portraits**.
- Current derivative Elementor inventory: **413 image-capable slots = 410 populated + the same 3 empty testimonial portraits**. The existing architecture audit reports 409 populated references because its walker misses the homepage nested Elementor 4.2 `e-image` widget (attachment 609, widget `306c538`).
- Current derivative SHA-256: `{derivative_hash}`.
- Band B: **{band_b_decided}/9 decided, verification PASS** (seven GENERIC, two UNUSABLE).
- Band A: **0/16 owner verdicts recorded; 16 HOLD; public-media gate FAIL**.
- Band D: 44 assets are pipeline-permitted as generic decoration, six of them are visually blank placeholder graphics and are OPTIONAL-REMOVE here. The worksheet's Band D cells remain blank because the existing decision/manifest, not an owner pixel verdict, is what currently permits them.
- Governing-file divergence: the requested `RUN-BLOCK-02-on-inputs.md` does not exist. The repository contains and this audit used `RUN-BLOCK-02.md`.

## Exact inventory reconciliation

| Population | Slots |
|---|---:|
| Original active-page image-capable slots | 610 |
| Populated in immutable source | 607 |
| Empty testimonial portraits | 3 |
| Present in derivative | 410 |
| Removed between source and derivative | 197 |
| Global Astra/WordPress brand slots (outside Elementor, added to CSV) | 2 |
| CSV requirement rows | {len(rows)} |

The 197 removed slots consist of 45 slots removed with D32 sections plus 152 direct removals/holds. The CSV contains all 610 page slots plus two global brand slots. Wave allocation for page slots is {wave_counts['Wave 1']} Wave 1, {wave_counts['Wave 3']} Wave 3-pending and {wave_counts['D22']} D22-deferred.

| Exact-one slot classification | Page slots |
|---|---:|
""" + "\n".join(f"| {name} | {count} |" for name, count in sorted(class_counts.items())) + f"""

Deferred is an exact-one launch classification: its underlying eventual action (retain, hold, replace brand or remove) is stated in each CSV row.

## Minimum honest Wave 1

### Current identity state

The minimum is **no live pages**, so the immediate new-image requirement is exactly zero. No image decision can make the site honest while the accountable publisher/operator relationship is absent.

### Conditional four-page holding set after identity is resolved

| Measure | Exact result |
|---|---:|
| New owner photographs required | 0 |
| Existing approved image assets used | {len(conditional_safe)} unique |
| Existing approved placements | {sum(r['slot_classification'] == 'EXISTING-APPROVED' for r in conditional_rows)} |
| Already supplied brand assets required | 2 files: wordmark and icon |
| Brand placements to assign | {conditional_brand} (two in-page plus header and site icon) |
| Optional testimonial slots/modules to remove | {sum(r['slot_classification'] == 'OPTIONAL-REMOVE' for r in conditional_rows)} |
| Unresolved image assets | {len({r['current_attachment_id'] for r in conditional_rows if r['slot_classification'] == 'BLOCKED-PENDING-VERDICT'})} |

The homepage can retain generic concrete imagery, but its three placeholder testimonial widgets must be removed. About and contact use the supplied wordmark. Privacy has no Elementor image slots. These four pages need no authentic project photograph because none may present completed work, a customer, staff, premises or contractor identity.

## All 76 built active pages

| Measure | Exact result |
|---|---:|
| New owner photographs currently required | 0 |
| Existing useful approved assets | {len(safe_asset_ids)} unique |
| Existing useful placements in the derivative | {useful_derivative_slots} |
| Already supplied brand assets required | 2 unique files |
| In-page/global brand assignments | {sum(r['slot_classification'] == 'OWNER-BRAND' for r in rows)} |
| Slots ultimately recommended for removal | {recommended_remove_slots} active-page slots |
| Decided Wave-1 optional removals | {decided_removal_slots} slots |
| Band A assets awaiting owner verdict | 16 unique / {direct_band_a_slots} direct held slots; other occurrences already disappear with D32 sections |
| Deferred page slots | {class_counts['DEFERRED']} |

The {recommended_remove_slots} removal recommendations reconcile without overlap: **45** D32 whole-section slots, **21** other prohibited direct slots, **3** empty testimonial portraits/widgets, **45** surviving blank-placeholder placements and **50** direct placements of the six Band A assets recommended UNUSABLE.

No active built page is structurally required to carry an authentic photograph. Therefore every active page can, in image terms, be completed without a new photograph by retaining honest generic decoration and removing unsupported/blank/evidential slots. **No page can currently launch**, because the non-image launch gates remain closed. No page is allowed to claim local completed work merely because a generic photograph is available.

Pages that could launch without new photographs once their non-image blockers clear: all 76 in image terms; the specifically smallest holding set is `/`, `/about/`, `/contact/` and `/privacy-policy/`. Pages that cannot launch without authentic photographs: **none under the current architecture**. `/gallery/` is the exception only if the owner insists on launching it as a completed-project gallery; in that case it needs a newly scoped authentic project library and is not part of the minimum wave.

The supplied horizontal wordmark unlocks the retained brand role on `/about/`, `/contact/`, `/quote/`, `/gallery/`, `/concrete-patios-south-west-sydney/`, `/concrete-paths-south-west-sydney/` and the global header. The supplied icon unlocks the global site-icon role. Homepage testimonial removal unlocks its three unsupported review modules without requiring portrait photographs. Each Band A decision's exact page/widget reach is listed in the Band A table below.

## Ordered owner photograph shot list

**None. There is no mandatory owner photograph to request under the current D32/D22 architecture.** The safe fallback for every optional evidential module is removal. If the owner later chooses to reopen a local-project card, `/gallery/`, a testimonial portrait, or a team/premises module, that is a new evidenced-content scope and the following packet is mandatory.

## Evidence packet for any future real-project photograph

For every real-project photograph, supply all of:

1. The original unedited file (a renamed derivative is not provenance).
2. Photographer/source identity and date taken.
3. Genuine project suburb and project type.
4. The person or business that actually performed the work.
5. Written permission to publish and confirmation the project may be associated with this website.
6. Customer/property consent where identifiable property, people or private information appears.
7. A redaction instruction for faces, house numbers and registration plates.
8. The project's relationship to the eventual signed NSW operator.
9. A supporting job record whenever the page makes a completed-project claim.

A filename changed to contain “Camden” or another NSW suburb is not evidence. Visual plausibility is not geographic provenance.

If a future shot becomes authorised, the brief must state subject, genuine-project requirement, orientation/aspect ratio, minimum dimensions, JPEG/WebP delivery, safe subject-only filename, visible-subject-only alt, release needs, permitted reuse and the exact claim supported. If the evidence packet cannot be supplied, remove the module.

## Band A — all 16 owner decisions still missing

No asset qualifies for OK: the repository contains no evidence supporting Camden or South West Sydney provenance. Original filenames identify Victorian places for all 16. Ten photographs have a legitimate generic subject and six are unusable because the subject itself carries a false locality or is unrelated to concrete.

| Tile | ID | Current filename | Visible content only | Current claim | Documentary NSW provenance | Recommended treatment | Reason | Missing owner input | New photograph actually required | Every active source placement |
|---:|---:|---|---|---|---|---|---|---|---|---|
""" + "\n".join(band_a_lines) + f"""

An owner GENERIC verdict authorises subject-only filename/alt remediation and decorative placement. An owner UNUSABLE verdict excludes the asset and removes every slot without replacement. An OK would additionally require a cited evidence packet. A REPLACE cannot be satisfied because no verified replacement is currently supplied.

## Existing approved reuse and forbidden implications

- The seven Band B photographs may be reused only as generic decoration. They must not sit with a customer quote or in “our recent work,” verified-project or completed-project presentation.
- The 38 useful surviving Band D assets may remain only as generic, non-evidential decoration under the current manifest. Six additional Band D binaries are blank placeholders and should be removed.
- The 10 Band A photographs recommended GENERIC may be reused after — and only after — the owner records that verdict and the reproducible transformer is rerun.
- Generic reuse never proves location, customer experience, staff, premises, equipment ownership or contractor identity.

## `/gallery/`

`/gallery/` should **not launch as a gallery**. Its D32 evidential gallery sections are removed, its E&T logo slot requires the supplied Structure Co wordmark, and there is no authentic project library tied to a verified NSW operator. Defer it or remove it from launch/navigation. A later gallery should be rebuilt from real projects with the complete evidence packet; the number of future photographs is a design/content decision and is not a current launch requirement.

## Deferred imagery

- Nine researched-but-later pages carry {wave_counts['Wave 3']} source slots and remain Wave 3-pending.
- Forty-five unresearched suburbs carry {wave_counts['D22']} source slots and are deferred under D22, not dropped.
- Eighty-one withdrawn pages are excluded from this requirements count. Their old 110 image placements are provenance, not future image briefs. Rebuilt deferred/withdrawn content must receive a fresh slot inventory; no historical “one image per suburb” target is carried forward.

No unique suburb photograph is required merely for SEO. A single approved generic concrete photograph may be reused where page context creates no locality or completed-project implication.

## Current media-control results and gaps

- `scripts/22-media-audit.py`: current public intake passes its 51-asset contract.
- `scripts/45-band-b-verify.py`: PASS, 9/9 decisions, zero Band B failures.
- `scripts/46-public-media-gate.py`: FAIL solely on 16 Band A HOLD assets.
- `scripts/46-architecture-import-gate.py --check`: passes its current 409-reference contract, but the true recursive count is 410 because nested Elementor 4.2 `e-image` data is not walked. That omission could allow a broken or prohibited nested image to pass, so the gate should be strengthened in a separately authorised implementation pass.

## Immutable hash table

| Immutable file | SHA-256 | Result |
|---|---|---|
""" + "\n".join(hash_lines) + f"""

## Page-by-page placement appendix

Notation is `widget:attachment[classification]`. The detailed section, visible purpose, current filename, permission, geography/project claim, removability, reuse rule and required action are in the CSV.

| Page ID | Slug | Type | Source slots | Derivative populated | Classification counts | Placements |
|---:|---|---|---:|---:|---|---|
""" + "\n".join(appendix_lines) + f"""

## Final audit statement

- Immutable hashes: 7/7 MATCH.
- Current derivative: `{derivative_hash}`.
- Band A: 0/16 owner verdicts, 16 HOLD, recommendations only (10 GENERIC, 6 UNUSABLE).
- Band B: 9/9 PASS.
- Minimum honest Wave 1 new-image total: **0** (current honest page total is also zero).
- Full 76-page new-image total: **0 currently required** under removal/generic-reuse policy.
- Remaining owner media decisions: **16 Band A verdicts**; a later `/gallery/` disposition and any decision to add evidenced project/team/premises modules are separate scope.
- No import, deployment, publication, media mutation, remote fetch, generated image, indexability change, derivative-WXR edit, immutable edit or governing-document edit occurred.
"""
    MD_OUT.write_text(report, encoding="utf-8", errors="strict", newline="\n")
    # Re-read both outputs strictly and print the evidence-backed headline.
    MD_OUT.read_text(encoding="utf-8", errors="strict")
    print(f"PASS — wrote {CSV_OUT.relative_to(ROOT)} ({len(rows)} rows) and {MD_OUT.relative_to(ROOT)}")
    print(f"source slots=610 (607 populated + 3 empty); derivative slots=410; CSV rows={len(rows)}")
    print(f"Band A owner verdicts={16-band_a_blank}/16; recommendations={generic_a} GENERIC + {unusable_a} UNUSABLE")
    print(f"Band B={band_b_decided}/9; safe existing assets={len(safe_asset_ids)}; new owner photos=0")
    print(f"derivative sha256={derivative_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
