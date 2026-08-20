from __future__ import annotations

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.wxr import NS, get_meta, parse_elementor, serialize_elementor


XML_PATH = ROOT / "source" / "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml"


def _text(node: ET.Element | None) -> str:
    return "" if node is None or node.text is None else node.text


def page_items() -> list[ET.Element]:
    root = ET.parse(XML_PATH).getroot()
    return [
        item
        for item in root.findall("./channel/item")
        if _text(item.find("wp:post_type", NS)) == "page"
    ]


class ElementorRoundTripTest(unittest.TestCase):
    def test_elementor_roundtrip_byte_match_per_page(self) -> None:
        failures: list[str] = []
        for item in page_items():
            slug = _text(item.find("wp:post_name", NS))
            original = get_meta(item, "_elementor_data")
            if original is None:
                continue
            reparsed = serialize_elementor(parse_elementor(item))
            if original != reparsed:
                failures.append(slug or "(empty-slug)")
        self.assertFalse(
            failures,
            "Elementor round-trip mismatch: " + ", ".join(failures),
        )


if __name__ == "__main__":
    unittest.main()
