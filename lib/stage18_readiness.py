from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "build/stage9-page-manifest.json"
PLACEHOLDERS = ROOT / "reports/placeholders.md"
WXR = ROOT / "camden-concreting-import.xml"
OUTPUT = ROOT / "reports/18-page-readiness.csv"
WP_NS = "http://wordpress.org/export/1.2/"
NS = {"wp": WP_NS}


def wp_text(element: ET.Element, tag: str) -> str:
    child = element.find(tag, NS)
    return (child.text or "") if child is not None else ""


def parse_markers() -> dict[str, list[str]]:
    occurrences: dict[str, list[str]] = defaultdict(list)
    row = re.compile(r"^\| (?P<url>/[^|]*) \| `(?P<marker>\[\[.+\]\])` \|$")
    for line in PLACEHOLDERS.read_text(encoding="utf-8").splitlines():
        match = row.match(line)
        if match:
            occurrences[match.group("url")].append(match.group("marker"))

    counts = Counter(
        "photo" if marker.startswith("[[REAL_PHOTO_PENDING")
        else "verify" if marker.startswith("[[VERIFY")
        else "placeholder"
        for markers in occurrences.values()
        for marker in markers
    )
    assert sum(counts.values()) == 163, counts
    assert counts == Counter({"placeholder": 111, "photo": 47, "verify": 5}), counts
    return occurrences


def marker_description(marker: str) -> str:
    inner = marker.removeprefix("[[").removesuffix("]]")
    if ":" in inner:
        return inner.split(":", 1)[1].strip()
    if inner == "REAL_PHOTO_PENDING":
        return "verified project photograph, location/service/date record and permission to publish"
    return inner


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    markers_by_url = parse_markers()

    root = ET.parse(WXR).getroot()
    wxr_pages: dict[int, dict[str, object]] = {}
    for item in root.find("channel").findall("item"):
        if wp_text(item, "wp:post_type") != "page":
            continue
        post_id = int(wp_text(item, "wp:post_id"))
        meta: dict[str, str] = {}
        for postmeta in item.findall("wp:postmeta", NS):
            meta[wp_text(postmeta, "wp:meta_key")] = wp_text(postmeta, "wp:meta_value")
        serialized = "\n".join(meta.values())
        wxr_pages[post_id] = {
            "status": wp_text(item, "wp:status"),
            "robots": meta.get("rank_math_robots", ""),
            "phone": any(value in serialized for value in ("03 4517 6915", "+61345176915")),
            "form": meta.get("_has_fluentform") == "1" or "fluentform" in serialized,
        }

    assert len(manifest) == len(wxr_pages) == 156
    assert {row["post_id"] for row in manifest} == set(wxr_pages)
    assert set(markers_by_url).issubset({row["url"] for row in manifest})

    fields = [
        "URL",
        "Page type",
        "Current WordPress status",
        "Current robots setting",
        "Placeholder count",
        "Photo marker count",
        "Verification marker count",
        "Phone verified",
        "Form dependency",
        "Business-evidence dependency",
        "Index-ready",
        "Exact missing evidence",
        "Recommended action",
    ]

    rows: list[dict[str, object]] = []
    for page in manifest:
        url = page["url"]
        wxr = wxr_pages[page["post_id"]]
        markers = markers_by_url.get(url, [])
        placeholders = [m for m in markers if m.startswith("[[PLACEHOLDER")]
        photos = [m for m in markers if m.startswith("[[REAL_PHOTO_PENDING")]
        verifies = [m for m in markers if m.startswith("[[VERIFY")]

        per_page_noindex = bool(wxr["robots"])
        robots = "global staging: noindex,nofollow,noarchive; page: " + (
            "noindex,follow" if per_page_noindex else "default (no page override)"
        )
        phone = bool(wxr["phone"])
        form = bool(wxr["form"])

        missing: list[str] = ["verified legal/operating identity for Structure Co Concreters Camden"]
        if phone:
            missing.append("ownership and call-routing proof for 03 4517 6915")
        else:
            missing.append("verified global header/footer phone after Astra settings are supplied")
        if form:
            missing.append("approved Fluent Forms form 3, recipient email, privacy basis, SMTP and delivery test")
        missing.extend(marker_description(marker) for marker in markers)
        if page["status"] == "draft":
            missing.append("page-specific publication-wave approval")
        missing.append("authoritative media/Astra import and logged-out visual QA")

        deduped_missing = list(dict.fromkeys(missing))
        if page["status"] == "publish":
            action = "Keep protected and noindex; resolve every listed item, then repeat staging QA before approval."
        else:
            action = "Keep draft; resolve page evidence and wave gate, then stage and QA before any status change."
        if page["page_type"] == "hub":
            action = "Keep draft; publish only with the first approved Wave 2 guide batch, never alone."

        rows.append(
            {
                "URL": url,
                "Page type": page["page_type"],
                "Current WordPress status": page["status"],
                "Current robots setting": robots,
                "Placeholder count": len(placeholders),
                "Photo marker count": len(photos),
                "Verification marker count": len(verifies),
                "Phone verified": "no — number present" if phone else "no — global contact presentation unverified",
                "Form dependency": (
                    "Fluent Forms ID 3 + verified recipient/privacy/SMTP" if form else "none in page content"
                ),
                "Business-evidence dependency": "yes — legal/operating identity; plus any listed page-specific evidence",
                "Index-ready": "no",
                "Exact missing evidence": "; ".join(deduped_missing),
                "Recommended action": action,
            }
        )

    assert Counter(row["Current WordPress status"] for row in rows) == Counter({"draft": 135, "publish": 21})
    assert sum(int(row["Placeholder count"]) for row in rows) == 111
    assert sum(int(row["Photo marker count"]) for row in rows) == 47
    assert sum(int(row["Verification marker count"]) for row in rows) == 5
    assert sum("Fluent Forms" in str(row["Form dependency"]) for row in rows) == 4
    assert sum(row["Index-ready"] == "yes" for row in rows) == 0

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(
        json.dumps(
            {
                "rows": len(rows),
                "publish": sum(row["Current WordPress status"] == "publish" for row in rows),
                "draft": sum(row["Current WordPress status"] == "draft" for row in rows),
                "markers": {
                    "placeholder": sum(int(row["Placeholder count"]) for row in rows),
                    "photo": sum(int(row["Photo marker count"]) for row in rows),
                    "verify": sum(int(row["Verification marker count"]) for row in rows),
                },
                "form_pages": sum("Fluent Forms" in str(row["Form dependency"]) for row in rows),
                "index_ready": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
