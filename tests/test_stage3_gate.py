import json
import unittest
from pathlib import Path

from lib.stage3_gate import (
    GLOBAL_REPLACEMENTS,
    SERVICE_CARDS,
    first_editor_containing,
    service_nodes,
)
from lib.wxr import serialize_elementor


ROOT = Path(__file__).resolve().parents[1]
PRETTY_PATH = ROOT / "build" / "concreters-oran-park.elementor.json"
ENCODED_PATH = ROOT / "build" / "concreters-oran-park.elementor-encoded.txt"


class Stage3GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = json.loads(PRETTY_PATH.read_text(encoding="utf-8"))
        cls.pretty = PRETTY_PATH.read_text(encoding="utf-8")
        cls.encoded = ENCODED_PATH.read_text(encoding="utf-8")

    def test_unicode_survives_both_payload_representations(self) -> None:
        for character in ("\u2014", "\u2013", "\u00b2"):
            self.assertIn(character, self.pretty)
            self.assertIn(f"\\u{ord(character):04x}", self.encoded)

    def test_serializer_is_lossless(self) -> None:
        serialized = serialize_elementor(self.tree)
        self.assertEqual(json.loads(serialized), self.tree)
        self.assertEqual(serialized, self.encoded)

    def test_global_placeholders_are_resolved(self) -> None:
        for placeholder in GLOBAL_REPLACEMENTS:
            self.assertNotIn(placeholder, self.pretty)
        self.assertIn("Call us - 03 4517 6915", self.pretty)
        self.assertIn("tel:+61345176915", self.pretty)

    def test_service_links_and_wrappers(self) -> None:
        cards = service_nodes(self.tree)
        self.assertEqual(len(cards), 6)
        self.assertEqual(
            [card["settings"]["title_text"] for card in cards],
            [title for title, _ in SERVICE_CARDS],
        )
        self.assertEqual(
            [card["settings"]["link"]["url"] for card in cards],
            [url for _, url in SERVICE_CARDS],
        )

    def test_module_10_has_four_suburb_links(self) -> None:
        editor = first_editor_containing(
            self.tree, "surrounding Camden growth suburbs"
        )
        expected = (
            "/concreters-catherine-field/",
            "/concreters-gledswood-hills/",
            "/concreters-gregory-hills/",
            "/concreters-harrington-park/",
        )
        for url in expected:
            self.assertIn(f'href="{url}"', editor)

    def test_contextual_service_links(self) -> None:
        expected = {
            "rear-yard shed slab": "/shed-and-garage-slabs-south-west-sydney/",
            "crossover": "/concrete-crossovers-and-laybacks-south-west-sydney/",
        }
        editors = []

        def collect(value):
            if isinstance(value, dict):
                settings = value.get("settings")
                if isinstance(settings, dict) and isinstance(settings.get("editor"), str):
                    editors.append(settings["editor"])
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(self.tree)
        for anchor, url in expected.items():
            linked = f'<a href="{url}">{anchor}</a>'
            self.assertEqual(sum(editor.count(linked) for editor in editors), 1)


if __name__ == "__main__":
    unittest.main()
