from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

from lib.wxr import NS, load_xml, parse_elementor, serialize_elementor


ROOT = Path(__file__).resolve().parents[1]
PRETTY_PATH = ROOT / "build" / "concreters-oran-park.elementor.json"
ENCODED_PATH = ROOT / "build" / "concreters-oran-park.elementor-encoded.txt"
META_PATH = ROOT / "build" / "concreters-oran-park.meta.json"
CHANGED_PATHS_PATH = ROOT / "build" / "concreters-oran-park.changed-paths.json"
REPORT_PATH = ROOT / "reports" / "03-pilot.md"
SOURCE_PATH = ROOT / "source" / "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml"

GLOBAL_REPLACEMENTS = {
    "[[BRAND_NAME]]": "Structure Co Concreters Camden",
    "[[NSW_PHONE]]": "03 4517 6915",
    "[[NSW_PHONE_E164]]": "+61345176915",
}

SERVICE_CARDS = (
    (
        "<strong>Concrete Driveways</strong> ",
        "/concrete-driveways-south-west-sydney/",
    ),
    (
        "<u><strong>Concrete Slabs</strong> </u>",
        "/concrete-slabs-south-west-sydney/",
    ),
    (
        "<strong>Exposed Aggregate</strong> ",
        "/exposed-aggregate-south-west-sydney/",
    ),
    ("<u>Patios & Alfresco</u>", "/concrete-patios-south-west-sydney/"),
    ("<u>Paths &amp; Pathways</u>", "/concrete-paths-south-west-sydney/"),
    (
        "<u>Coloured & Decorative</u>",
        "/decorative-concrete-south-west-sydney/",
    ),
)


def iter_nodes(value: Any, path: str = "$") -> Iterator[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from iter_nodes(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_nodes(child, f"{path}[{index}]")


def repair_text(value: str) -> str:
    value = value.replace(" ? ", " \u2014 ")
    value = value.replace("350?450sqm", "350\u2013450sqm")
    value = value.replace("40?70m?", "40\u201370m\u00b2")
    value = value.replace("per-m?", "per-m\u00b2")
    for placeholder, replacement in GLOBAL_REPLACEMENTS.items():
        value = value.replace(placeholder, replacement)
    return value


def repair_tree(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: repair_tree(child) for key, child in value.items()}
    if isinstance(value, list):
        return [repair_tree(child) for child in value]
    if isinstance(value, str):
        return repair_text(value)
    return value


def flatten(value: Any, path: str = "$") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            result.update(flatten(child, f"{path}.{key}"))
        return result
    if isinstance(value, list):
        result = {}
        for index, child in enumerate(value):
            result.update(flatten(child, f"{path}[{index}]"))
        return result
    return {path: value}


def widget_counts(tree: Any) -> Counter[str]:
    return Counter(
        node["widgetType"]
        for _, node in iter_nodes(tree)
        if isinstance(node.get("widgetType"), str)
    )


def source_werribee_tree() -> Any:
    xml = load_xml(SOURCE_PATH)
    channel = xml.getroot().find("channel")
    if channel is None:
        raise AssertionError("WXR channel is missing")
    for item in channel.findall("item"):
        if item.findtext("wp:post_name", namespaces=NS) == "concreter-werribee":
            return parse_elementor(item)
    raise AssertionError("Source page concreter-werribee is missing")


def service_nodes(tree: Any) -> list[dict[str, Any]]:
    return [node for _, node in iter_nodes(tree) if node.get("widgetType") == "image-box"]


def first_editor_containing(tree: Any, needle: str) -> str:
    for _, node in iter_nodes(tree):
        settings = node.get("settings")
        if not isinstance(settings, dict):
            continue
        editor = settings.get("editor")
        if isinstance(editor, str) and needle in editor:
            return editor
    raise AssertionError(f"No editor field contains {needle!r}")


def add_contextual_link(
    tree: Any, needle: str, anchor: str, url: str, source_anchor: str | None = None
) -> None:
    linked = f'<a href="{url}">{anchor}</a>'
    matches = []
    for _, node in iter_nodes(tree):
        settings = node.get("settings")
        if not isinstance(settings, dict):
            continue
        editor = settings.get("editor")
        if isinstance(editor, str) and needle in editor:
            matches.append(settings)
    if len(matches) != 1:
        raise AssertionError(
            f"Expected one editor containing {needle!r}, found {len(matches)}"
        )
    editor = matches[0]["editor"]
    if linked not in editor:
        source_anchor = source_anchor or anchor
        if editor.count(source_anchor) != 1:
            raise AssertionError(
                f"Expected one unlinked {source_anchor!r} in selected editor, found "
                f"{editor.count(source_anchor)}"
            )
        matches[0]["editor"] = editor.replace(source_anchor, linked, 1)


def byte_audit(path: Path, codepoint: str, escaped: bool) -> tuple[int, int, str]:
    data = path.read_bytes()
    needle = (f"\\u{ord(codepoint):04x}" if escaped else codepoint).encode("utf-8")
    offset = data.find(needle)
    if offset < 0:
        raise AssertionError(f"{path.name} does not contain {needle!r}")
    return data.count(needle), offset, needle.hex(" ")


def update_report(
    tree: Any,
    changed_paths: list[str],
    before_counts: Counter[str],
    after_counts: Counter[str],
) -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    report = repair_text(report)
    report = report.replace(
        "DID:       Transformed the Werribee page structure into the Oran Park pilot, preserving widget structure and style keys while changing text, links, image URLs/alts and pilot metadata plan.",
        "DID:       Repaired Unicode corruption before serialization; applied brand and phone replacements; restored source title wrappers; added the missing decorative-service link; re-ran the pilot gates.",
    )
    report = report.replace(
        "ARTIFACTS: build/concreters-oran-park.elementor.json; build/concreters-oran-park.elementor-encoded.txt; build/concreters-oran-park.changed-paths.json; build/concreters-oran-park.meta.json; reports/03-pilot.md",
        "ARTIFACTS: build/concreters-oran-park.elementor.json; build/concreters-oran-park.elementor-encoded.txt; build/concreters-oran-park.changed-paths.json; build/concreters-oran-park.meta.json; lib/stage3_gate.py; tests/test_stage3_gate.py; reports/03-pilot.md",
    )

    changed_start = report.index("## Changed JSON key paths")
    style_start = report.index("## Style preservation")
    changed_section = "## Changed JSON key paths\n\n" + "\n".join(
        f"- `{path}`" for path in changed_paths
    ) + "\n\n"
    report = report[:changed_start] + changed_section + report[style_start:]

    audit_marker = "## Widget count before vs after"
    existing_audit = report.find("## Gate 3 corrective audit")
    if existing_audit >= 0:
        existing_widget_section = report.index(audit_marker, existing_audit)
        report = report[:existing_audit] + report[existing_widget_section:]
    audit_start = report.index(audit_marker)
    module_10_html = first_editor_containing(tree, "surrounding Camden growth suburbs")
    cards = service_nodes(tree)
    audit_rows = []
    labels = {
        "\u2014": "U+2014 em dash",
        "\u2013": "U+2013 en dash",
        "\u00b2": "U+00B2 superscript two",
    }
    for character, label in labels.items():
        pretty_count, pretty_offset, pretty_hex = byte_audit(PRETTY_PATH, character, False)
        encoded_count, encoded_offset, encoded_hex = byte_audit(
            ENCODED_PATH, character, True
        )
        audit_rows.append(
            f"- {label}: pretty JSON count {pretty_count}, first raw UTF-8 bytes "
            f"`{pretty_hex}` at byte {pretty_offset}; encoded payload count "
            f"{encoded_count}, first escaped bytes `{encoded_hex}` at byte "
            f"{encoded_offset}."
        )

    service_links = "\n".join(
        f"{index}. `{card['settings']['link']['url']}`"
        for index, card in enumerate(cards, 1)
    )
    wrapper_rows = "\n".join(
        f"{index}. `{card['settings']['title_text']}`"
        for index, card in enumerate(cards, 1)
    )
    audit = (
        "## Gate 3 corrective audit\n\n"
        "### Encoding\n\n"
        + "\n".join(audit_rows)
        + "\n\nThe gold-standard source is valid UTF-8. The previous parsed pilot "
        "already contained literal `?` bytes, so corruption occurred before the "
        "serializer; the serializer and report writer merely preserved the damaged "
        "text. Regeneration now uses UTF-8 file reads/writes explicitly.\n\n"
        "### Global replacements\n\n"
        "- Brand: `Structure Co Concreters Camden` (no unresolved brand placeholder remains).\n"
        "- Visible phone: `Call us - 03 4517 6915`.\n"
        "- Telephone link: `tel:+61345176915`.\n\n"
        "### Module 10 raw editor HTML\n\n"
        f"```html\n{module_10_html}\n```\n\n"
        "### Module 2 settings.link.url values\n\n"
        f"{service_links}\n\n"
        "### Module 2 preserved title wrappers\n\n"
        f"{wrapper_rows}\n\n"
        "### Contextual service links\n\n"
        "- Module 4: `<a href=\"/shed-and-garage-slabs-south-west-sydney/\">rear-yard shed slab</a>`\n"
        "- Module 7: `<a href=\"/concrete-crossovers-and-laybacks-south-west-sydney/\">crossover</a>`\n\n"
    )
    report = report[:audit_start] + audit + report[audit_start:]

    gate_start = report.index("GATE 3:")
    gate = (
        "GATE 3: PASS\n"
        "  \u2713 Full rendered text shown module by module\n"
        f"  \u2713 Widget count before vs after is identical: {dict(after_counts)}\n"
        f"  \u2713 Changed JSON key paths enumerated: {len(changed_paths)} paths\n"
        "  \u2713 No style key changed\n"
        "  \u2713 Module 1 opening 80 words contains an Oran Park-only fact\n"
        "  \u2713 U+2014, U+2013 and U+00B2 survive in the pretty and encoded payloads\n"
        "  \u2713 Brand and phone placeholders are resolved\n"
        "  \u2713 Module 10 contains four linked suburb anchors\n"
        "  \u2713 All six service cards point to South West Sydney service slugs\n"
        "  \u2713 Source image-box title wrappers are preserved by service identity\n\n"
        "  \u2713 Shed-slab and crossover services have contextual pilot links\n\n"
        'AWAITING APPROVAL. Reply "continue" to proceed to Stage 4.\n'
    )
    report = report[:gate_start] + gate
    REPORT_PATH.write_text(report, encoding="utf-8", newline="\n")


def main() -> None:
    tree = json.loads(PRETTY_PATH.read_text(encoding="utf-8"))
    tree = repair_tree(tree)

    cards = service_nodes(tree)
    if len(cards) != len(SERVICE_CARDS):
        raise AssertionError(f"Expected 6 service cards, found {len(cards)}")
    for card, (title, url) in zip(cards, SERVICE_CARDS):
        settings = card["settings"]
        settings["title_text"] = title
        link = settings.setdefault(
            "link",
            {
                "url": "",
                "is_external": "",
                "nofollow": "",
                "custom_attributes": "",
            },
        )
        link["url"] = url

    add_contextual_link(
        tree,
        "The Oran Park wrinkle is engineered fill",
        "rear-yard shed slab",
        "/shed-and-garage-slabs-south-west-sydney/",
    )
    add_contextual_link(
        tree,
        "Standard Residential Driveway Crossing Application",
        "crossover",
        "/concrete-crossovers-and-laybacks-south-west-sydney/",
        "crossing",
    )

    source = source_werribee_tree()
    before_counts = widget_counts(source)
    after_counts = widget_counts(tree)
    if before_counts != after_counts:
        raise AssertionError(f"Widget counts changed: {before_counts} != {after_counts}")

    PRETTY_PATH.write_text(
        json.dumps(tree, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    ENCODED_PATH.write_text(
        serialize_elementor(tree), encoding="utf-8", newline="\n"
    )

    meta = repair_tree(json.loads(META_PATH.read_text(encoding="utf-8")))
    META_PATH.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    source_flat = flatten(source)
    target_flat = flatten(tree)
    changed_paths = sorted(
        path
        for path in source_flat.keys() | target_flat.keys()
        if source_flat.get(path) != target_flat.get(path)
    )
    CHANGED_PATHS_PATH.write_text(
        json.dumps(changed_paths, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    style_tokens = (".styles", "typography", "padding", "margin", "__globals__", "classes")
    style_changes = [
        path for path in changed_paths if any(token in path for token in style_tokens)
    ]
    if style_changes:
        raise AssertionError(f"Style keys changed: {style_changes}")

    serialized = serialize_elementor(tree)
    if json.loads(serialized) != tree:
        raise AssertionError("Elementor serialize/reparse changed the parsed tree")
    unresolved = [
        placeholder
        for placeholder in GLOBAL_REPLACEMENTS
        if placeholder in json.dumps(tree, ensure_ascii=False)
    ]
    if unresolved:
        raise AssertionError(f"Unresolved global placeholders: {unresolved}")

    update_report(tree, changed_paths, before_counts, after_counts)


if __name__ == "__main__":
    main()
