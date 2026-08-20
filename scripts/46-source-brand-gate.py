#!/usr/bin/env python3
"""Gate 13 — assert the D35 transformation result, not the rename plan."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.preimport_safety import (  # noqa: E402
    WP,
    classify_corex,
    items,
    metas,
    parse_wxr,
    post_id,
    post_type,
    sha256,
    visible_page_fields,
)

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "camden-concreting-import.xml"
TARGET = ROOT / "build" / "46-active-main-import.xml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
RESULT = ROOT / "reports" / "46-source-brand-gate.json"
EXPECTED_BASELINE_SHA = "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884"
SOURCE_NAME = re.compile(r"CoreX|E(?:&amp;|&)T\s*Co|E(?:&amp;|&)T\b", re.I)
UNSUPPORTED_TAGLINE = re.compile(r"Camden based Concrete Company Site", re.I)


def page_visible_hits(path: Path) -> list[dict]:
    out = []
    tree = parse_wxr(path)
    for item in items(tree):
        if post_type(item) != "page":
            continue
        for field in visible_page_fields(item):
            source_hits = SOURCE_NAME.findall(field["text"])
            tagline_hits = UNSUPPORTED_TAGLINE.findall(field["text"])
            if source_hits or tagline_hits:
                out.append(
                    {
                        "page_id": post_id(item),
                        "placement": field["placement"],
                        "source_name_hits": len(source_hits),
                        "tagline_hits": len(tagline_hits),
                    }
                )
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    errors: list[str] = []
    if sha256(BASELINE) != EXPECTED_BASELINE_SHA:
        errors.append("immutable main WXR hash mismatch")
    if not TARGET.exists() or not ALLOWLIST.exists():
        errors.append("active derivative or allowlist absent")
    baseline = classify_corex(parse_wxr(BASELINE))
    if baseline["unknown"]:
        errors.append(f"unattributed baseline CoreX paths: {baseline['unknown']}")
    if (
        baseline["total"],
        baseline["reader_visible"],
        baseline["nonvisible_filenames_urls_slugs"],
    ) != (466, 366, 100):
        errors.append(f"baseline classification is not 466 -> 366 + 100: {baseline}")

    target = None
    allow = None
    visible_hits: list[dict] = []
    if TARGET.exists() and ALLOWLIST.exists():
        allow = json.loads(ALLOWLIST.read_text(encoding="utf-8", errors="strict"))
        if allow["derived_import"]["sha256"] != sha256(TARGET):
            errors.append("derived WXR hash differs from the allowlist provenance")
        target_tree = parse_wxr(TARGET)
        target = classify_corex(target_tree)
        if target["unknown"]:
            errors.append(f"unattributed target CoreX paths: {target['unknown']}")
        if target["reader_visible"]:
            errors.append(f"reader-visible CoreX remains in target: {target['reader_visible']}")
        visible_hits = page_visible_hits(TARGET)
        if visible_hits:
            errors.append(f"source name/tagline remains on {len(visible_hits)} visible fields")

        # The Elementor kit is non-page content, so inspect its serialised values
        # explicitly in addition to page fields.
        kit_values = []
        for item in items(target_tree):
            if post_type(item) != "elementor_library":
                continue
            for _pm, key, value_node in metas(item):
                if key == "_elementor_page_settings":
                    kit_values.append(value_node.text or "")
        if len(kit_values) != 1:
            errors.append(f"expected one Elementor kit settings blob, found {len(kit_values)}")
        elif SOURCE_NAME.search(kit_values[0]) or UNSUPPORTED_TAGLINE.search(kit_values[0]):
            errors.append("source name or unsupported tagline remains in Elementor kit")
        if not kit_values or 's:9:"site_name";s:30:"Structure Co Concreters Camden";' not in kit_values[0]:
            errors.append("Elementor kit site_name is not the exact D35 target")
        if not kit_values or 's:16:"site_description";s:0:"";' not in kit_values[0]:
            errors.append("Elementor kit site_description was not removed")

        transform = allow["derived_import"]["brand_transform"]
        renamed = int(transform["corex_reader_visible_renamed"])
        excluded = baseline["reader_visible"] - renamed
        if renamed + excluded != 366 or excluded < 0:
            errors.append("reader-visible transformation/exclusion arithmetic does not total 366")
    else:
        renamed = excluded = 0

    doc = {
        "result": "FAIL" if errors else "PASS",
        "gate": 13,
        "baseline": baseline,
        "classification": "466 total = 366 rename targets + 100 filename/URL/slug provenance",
        "active_derivative": target,
        "reader_visible_disposition": {
            "renamed_in_active_derivative": renamed,
            "excluded_with_withdrawn_pages": excluded,
            "remaining": target["reader_visible"] if target else None,
        },
        "preserved_prefix_rule": (
            "immutable corex- attachment provenance is untouched; the active derivative may remove or "
            "rename a prefix only through the Phase B manifest while all Elementor references remain resolved"
        ),
        "visible_source_name_or_tagline_hits": visible_hits,
        "errors": errors,
    }
    RESULT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("FAIL — Gate 13: " + "; ".join(errors), file=sys.stderr)
        return 1
    print(
        "PASS — Gate 13: baseline 466 = 366 reader targets + 100 preserved path references; "
        f"active derivative renamed {renamed}, excluded {excluded} with withdrawn pages, remaining 0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
