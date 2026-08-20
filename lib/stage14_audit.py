from __future__ import annotations

import argparse
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


WP_NS = "http://wordpress.org/export/1.2/"
NS = {"wp": WP_NS}
EXPECTED_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".avif": "image/avif",
}


def child_text(element: ET.Element, tag: str) -> str:
    child = element.find(tag, NS)
    return (child.text or "") if child is not None else ""


def attachment_meta(item: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for meta in item.findall("wp:postmeta", NS):
        key = child_text(meta, "wp:meta_key")
        value = child_text(meta, "wp:meta_value")
        result[key] = value
    return result


def expected_dimensions(serialized: str) -> tuple[str, str]:
    match = re.search(r's:5:"width";i:(\d+);s:6:"height";i:(\d+);', serialized)
    if not match:
        return "", ""
    return match.group(1), match.group(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    image_map = json.loads((root / "build/stage8-image-map.json").read_text(encoding="utf-8"))
    tree = ET.parse(root / "camden-concreting-import.xml")
    attachments: dict[int, ET.Element] = {}
    for item in tree.getroot().find("channel").findall("item"):
        if child_text(item, "wp:post_type") == "attachment":
            attachments[int(child_text(item, "wp:post_id"))] = item

    rows: list[dict[str, str]] = []
    for key, mapped in image_map.items():
        attachment_id = int(key)
        item = attachments[attachment_id]
        meta = attachment_meta(item)
        expected_filename = mapped["new_filename"]
        extension = Path(expected_filename).suffix
        expected_mime = child_text(item, "wp:post_mime_type") or EXPECTED_MIME.get(extension.lower(), "")
        width, height = expected_dimensions(meta.get("_wp_attachment_metadata", ""))
        source_path = root / "staging/source-media/2026/07" / mapped["old_filename"]
        prepared_path = root / "staging/media-prepared/2026/07" / expected_filename
        source_found = source_path.is_file()
        prepared_found = prepared_path.is_file()

        rows.append(
            {
                "attachment_id": str(attachment_id),
                "old_filename": mapped["old_filename"],
                "expected_filename": expected_filename,
                "expected_upload_path": f"/wp-content/uploads/2026/07/{expected_filename}",
                "expected_extension": extension.lower(),
                "extension_case_ok": "yes" if extension == extension.lower() else "no",
                "expected_mime": expected_mime,
                "expected_width": width,
                "expected_height": height,
                "source_binary_found": "yes" if source_found else "no",
                "prepared_binary_found": "yes" if prepared_found else "no",
                "actual_mime": "",
                "actual_width": "",
                "actual_height": "",
                "metadata_stripped": "unverifiable",
                "sha256": "",
                "audit_result": "blocked_missing_binary" if not prepared_found else "requires_binary_inspection",
                "notes": "Expected metadata comes from the WXR; no original or prepared binary was supplied.",
            }
        )

    output = root / "reports/14-media-audit.csv"
    fieldnames = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"rows={len(rows)}")
    print(f"source_found={sum(row['source_binary_found'] == 'yes' for row in rows)}")
    print(f"prepared_found={sum(row['prepared_binary_found'] == 'yes' for row in rows)}")
    print(f"output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
