from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}


def load_xml(path: str | Path) -> ET.ElementTree:
    return ET.parse(path)


def _text(node: ET.Element | None) -> str:
    return "" if node is None or node.text is None else node.text


def get_meta(item: ET.Element, key: str) -> str | None:
    for meta in item.findall("wp:postmeta", NS):
        meta_key = _text(meta.find("wp:meta_key", NS))
        if meta_key == key:
            return _text(meta.find("wp:meta_value", NS))
    return None


def set_meta(item: ET.Element, key: str, value: str) -> None:
    for meta in item.findall("wp:postmeta", NS):
        meta_key = _text(meta.find("wp:meta_key", NS))
        if meta_key == key:
            meta_value = meta.find("wp:meta_value", NS)
            if meta_value is None:
                meta_value = ET.SubElement(meta, f"{{{NS['wp']}}}meta_value")
            meta_value.text = value
            return

    meta = ET.SubElement(item, f"{{{NS['wp']}}}postmeta")
    meta_key = ET.SubElement(meta, f"{{{NS['wp']}}}meta_key")
    meta_key.text = key
    meta_value = ET.SubElement(meta, f"{{{NS['wp']}}}meta_value")
    meta_value.text = value


def parse_elementor(item: ET.Element) -> Any:
    raw = get_meta(item, "_elementor_data")
    if raw is None:
        return None
    return json.loads(raw)


def serialize_elementor(tree: Any) -> str:
    dumped = json.dumps(tree, ensure_ascii=True, separators=(",", ":"))
    return dumped.replace("/", "\\/")


def write_elementor(item: ET.Element, tree: Any) -> None:
    set_meta(item, "_elementor_data", serialize_elementor(tree))


def save_xml(tree: ET.ElementTree, path: str | Path) -> None:
    tree.write(path, encoding="utf-8", xml_declaration=True)
