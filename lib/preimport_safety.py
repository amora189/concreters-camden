"""Shared fail-closed helpers for the pre-import safety controls.

This module never writes an immutable input.  Callers may build reproducible
derivatives from those inputs and must verify the immutable hashes separately.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterator


WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
EXCERPT = "{http://wordpress.org/export/1.2/excerpt/}"

NAMESPACES = {
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "wp": "http://wordpress.org/export/1.2/",
}
for _prefix, _uri in NAMESPACES.items():
    ET.register_namespace(_prefix, _uri)

COREX_RE = re.compile(r"CoreX", re.I)
ET_RE = re.compile(r"E(?:&amp;|&)T\s*Co\s*Concreters\s*Camden", re.I)
TAGLINE_RE = re.compile(r"Camden based Concrete Company Site", re.I)

# These are the keys attributed as reader-visible in the accepted 466 -> 366
# classification in reports/38-trading-name-rename-plan.md.
VISIBLE_ELEMENTOR_KEYS = {
    "editor",
    "text",
    "alt",
    "value",
    "title",
    "item_title",
    "testimonial_content",
}
NONVISIBLE_ELEMENTOR_KEYS = {"url"}
VISIBLE_META_KEYS = {
    "rank_math_title",
    "rank_math_description",
    "rank_math_breadcrumb_title",
    # Not rendered as body copy, but it is the one non-path field needed for
    # the accepted 366 rename-target / 100 path-provenance partition.
    "rank_math_focus_keyword",
    "_wp_attachment_image_alt",
}
NONVISIBLE_META_KEYS = {
    "_wp_attachment_metadata",
    "_wp_attached_file",
}

# Broader than the CoreX classification: these settings can carry readable
# claims and are therefore included in the claim register.
CLAIM_TEXT_KEYS = {
    "editor",
    "title",
    "title_text",
    "heading_title",
    "description_text",
    "text",
    "html",
    "testimonial_content",
    "testimonial_name",
    "testimonial_job",
    "item_description",
    "item_title",
    "tab_content",
    "tab_title",
    "content",
    "caption",
    "alt",
    "before_text",
    "highlighted_text",
    "after_text",
    "inner_text",
    "list_item_text",
    "accordion_content",
    "toggle_content",
    "value",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def parse_wxr(path: Path) -> ET.ElementTree:
    return ET.parse(path)


def items(tree: ET.ElementTree) -> list[ET.Element]:
    return tree.getroot().findall("./channel/item")


def post_id(item: ET.Element) -> int:
    raw = (item.findtext(WP + "post_id") or "").strip()
    if not raw.isdigit():
        raise ValueError(f"item has invalid wp:post_id {raw!r}")
    return int(raw)


def post_type(item: ET.Element) -> str:
    return (item.findtext(WP + "post_type") or "").strip()


def post_slug(item: ET.Element) -> str:
    return (item.findtext(WP + "post_name") or "").strip()


def post_status(item: ET.Element) -> str:
    return (item.findtext(WP + "status") or "").strip()


def metas(item: ET.Element) -> Iterator[tuple[ET.Element, str, ET.Element]]:
    for pm in item.findall(WP + "postmeta"):
        key = (pm.findtext(WP + "meta_key") or "").strip()
        value_node = pm.find(WP + "meta_value")
        if value_node is not None:
            yield pm, key, value_node


def walk_strings(node: Any, path: str = "$", key: str | None = None) -> Iterator[tuple[str, str | None, str]]:
    if isinstance(node, dict):
        for child_key, value in node.items():
            yield from walk_strings(value, f"{path}.{child_key}", child_key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, f"{path}[{index}]", key)
    elif isinstance(node, str):
        yield path, key, node


def transform_json_strings(node: Any) -> int:
    """Rename CoreX only in accepted reader-visible Elementor settings."""
    changed = 0
    if isinstance(node, dict):
        for key, value in list(node.items()):
            if isinstance(value, str) and key in VISIBLE_ELEMENTOR_KEYS:
                replacement, count = COREX_RE.subn("Structure Co", value)
                if count:
                    node[key] = replacement
                    changed += count
            else:
                changed += transform_json_strings(value)
    elif isinstance(node, list):
        for value in node:
            changed += transform_json_strings(value)
    return changed


def replace_serialized_string(blob: str, key: str, replacement: str) -> tuple[str, int]:
    """Replace one PHP-serialised scalar while repairing its byte length."""
    pattern = re.compile(
        rf'(s:{len(key.encode("utf-8"))}:"{re.escape(key)}";s:)\d+:("[^"]*";)',
        re.S,
    )

    def repl(match: re.Match[str]) -> str:
        quoted = f'"{replacement}";'
        return f"{match.group(1)}{len(replacement.encode('utf-8'))}:{quoted}"

    return pattern.subn(repl, blob)


def apply_reader_visible_brand_transform(tree: ET.ElementTree) -> dict[str, int]:
    """Apply D35 to a derivative WXR, preserving filenames, URLs and slugs."""
    counts = {
        "corex_reader_visible_renamed": 0,
        "et_kit_site_name_renamed": 0,
        "unsupported_tagline_removed": 0,
    }
    channel = tree.getroot().find("./channel")
    if channel is None:
        raise ValueError("WXR has no channel")
    channel_title = channel.find("title")
    if channel_title is not None and channel_title.text:
        channel_title.text, n = COREX_RE.subn("Structure Co", channel_title.text)
        counts["corex_reader_visible_renamed"] += n
    channel_image_title = channel.find("./image/title")
    if channel_image_title is not None and channel_image_title.text:
        channel_image_title.text, n = COREX_RE.subn(
            "Structure Co", channel_image_title.text
        )
        counts["corex_reader_visible_renamed"] += n

    for item in items(tree):
        title = item.find("title")
        if title is not None and title.text:
            title.text, n = COREX_RE.subn("Structure Co", title.text)
            counts["corex_reader_visible_renamed"] += n

        content_node = item.find(CONTENT + "encoded")
        if content_node is not None and content_node.text:
            content_node.text, n = COREX_RE.subn("Structure Co", content_node.text)
            counts["corex_reader_visible_renamed"] += n

        for _pm, key, value_node in metas(item):
            value = value_node.text or ""
            if key == "_elementor_data" and value:
                parsed = json.loads(value)
                n = transform_json_strings(parsed)
                if n:
                    value_node.text = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
                    counts["corex_reader_visible_renamed"] += n
            elif key in VISIBLE_META_KEYS:
                value_node.text, n = COREX_RE.subn("Structure Co", value)
                counts["corex_reader_visible_renamed"] += n
            elif key == "_elementor_page_settings" and value:
                value, n = replace_serialized_string(
                    value, "site_name", "Structure Co Concreters Camden"
                )
                counts["et_kit_site_name_renamed"] += n
                value, n = replace_serialized_string(value, "site_description", "")
                counts["unsupported_tagline_removed"] += n
                value_node.text = value
    return counts


def classify_corex(tree: ET.ElementTree) -> dict[str, Any]:
    """Reproduce the accepted full-WXR 466 -> 366 + 100 attribution.

    Unknown paths are fatal to callers: a new occurrence cannot be silently
    called provenance merely because the classifier has not seen it before.
    """
    visible = 0
    nonvisible = 0
    unknown: list[str] = []
    detail: dict[str, int] = {}

    def add(bucket: str, count: int) -> None:
        nonlocal visible, nonvisible
        if not count:
            return
        detail[bucket] = detail.get(bucket, 0) + count
        if bucket.startswith("visible:"):
            visible += count
        elif bucket.startswith("nonvisible:"):
            nonvisible += count

    channel = tree.getroot().find("./channel")
    if channel is None:
        raise ValueError("WXR has no channel")
    for child in list(channel):
        if child.tag == "item":
            continue
        count = len(COREX_RE.findall(child.text or ""))
        if count:
            if child.tag in {"title", "description"}:
                add(f"visible:channel:{child.tag}", count)
            elif child.tag in {"link"}:
                add(f"nonvisible:channel:{child.tag}", count)
            else:
                unknown.append(f"channel/{child.tag}:{count}")
        if child.tag == "image":
            image_title = child.find("title")
            image_count = len(
                COREX_RE.findall(image_title.text or "")
            ) if image_title is not None else 0
            add("visible:channel:image:title", image_count)

    for item in items(tree):
        pid = post_id(item)
        for tag, bucket in (
            ("title", "visible:item:title"),
            ("link", "nonvisible:item:link"),
            ("guid", "nonvisible:item:guid"),
            (WP + "post_name", "nonvisible:item:post_name"),
            (WP + "attachment_url", "nonvisible:item:attachment_url"),
            (CONTENT + "encoded", "visible:item:post_content"),
            (EXCERPT + "encoded", "visible:item:excerpt"),
        ):
            node = item.find(tag)
            add(bucket, len(COREX_RE.findall(node.text or "")) if node is not None else 0)

        for _pm, key, value_node in metas(item):
            value = value_node.text or ""
            count = len(COREX_RE.findall(value))
            if not count:
                continue
            if key == "_elementor_data":
                parsed = json.loads(value)
                attributed = 0
                for path, child_key, string in walk_strings(parsed):
                    n = len(COREX_RE.findall(string))
                    if not n:
                        continue
                    attributed += n
                    if child_key in VISIBLE_ELEMENTOR_KEYS:
                        add(f"visible:elementor:{child_key}", n)
                    elif child_key in NONVISIBLE_ELEMENTOR_KEYS:
                        add(f"nonvisible:elementor:{child_key}", n)
                    else:
                        unknown.append(f"post {pid} _elementor_data {path}:{n}")
                if attributed != count:
                    unknown.append(
                        f"post {pid} _elementor_data raw={count} attributed={attributed}"
                    )
            elif key in VISIBLE_META_KEYS:
                add(f"visible:meta:{key}", count)
            elif key in NONVISIBLE_META_KEYS:
                add(f"nonvisible:meta:{key}", count)
            else:
                unknown.append(f"post {pid} meta {key}:{count}")

    return {
        "total": visible + nonvisible,
        "reader_visible": visible,
        "nonvisible_filenames_urls_slugs": nonvisible,
        "detail": dict(sorted(detail.items())),
        "unknown": unknown,
    }


def visible_page_fields(item: ET.Element) -> Iterator[dict[str, str]]:
    """Yield exact reader-visible strings and stable placements for claim scans."""
    title = item.findtext("title") or ""
    if title.strip():
        yield {"placement": "item.title", "text": title, "widget_type": "wordpress"}
    content = item.findtext(CONTENT + "encoded") or ""
    if content.strip():
        yield {"placement": "post_content", "text": content, "widget_type": "wordpress"}
    for _pm, key, value_node in metas(item):
        value = value_node.text or ""
        if key == "_elementor_data" and value:
            parsed = json.loads(value)

            def walk(node: Any, path: str = "$", widget: str = "elementor") -> Iterator[dict[str, str]]:
                if isinstance(node, dict):
                    current_widget = str(node.get("widgetType") or widget)
                    for child_key, child in node.items():
                        child_path = f"{path}.{child_key}"
                        if isinstance(child, str) and child_key in CLAIM_TEXT_KEYS and child.strip():
                            yield {
                                "placement": f"_elementor_data:{child_path}",
                                "text": child,
                                "widget_type": current_widget,
                            }
                        elif isinstance(child, (dict, list)):
                            yield from walk(child, child_path, current_widget)
                elif isinstance(node, list):
                    for index, child in enumerate(node):
                        yield from walk(child, f"{path}[{index}]", widget)

            yield from walk(parsed)
        elif key in {
            "rank_math_title",
            "rank_math_description",
            "rank_math_breadcrumb_title",
            "_wp_attachment_image_alt",
        } and value.strip():
            yield {"placement": f"postmeta:{key}", "text": value, "widget_type": "meta"}


def clone_tree(tree: ET.ElementTree) -> ET.ElementTree:
    return ET.ElementTree(copy.deepcopy(tree.getroot()))
