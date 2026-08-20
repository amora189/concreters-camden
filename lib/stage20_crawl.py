from __future__ import annotations

import csv
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8088"
MANIFEST = ROOT / "build/stage9-page-manifest.json"
WXR = ROOT / "camden-concreting-import.xml"
OUTPUT = ROOT / "reports/20-route-crawl.csv"
WP_NS = "http://wordpress.org/export/1.2/"
NS = {"wp": WP_NS}


def wp_text(element: ET.Element, tag: str) -> str:
    child = element.find(tag, NS)
    return (child.text or "") if child is not None else ""


def fetch(path: str) -> dict[str, str | int]:
    request = urllib.request.Request(
        BASE + path,
        headers={"User-Agent": "Camden-Stage20-Local-Crawler/1.0", "Host": "127.0.0.1:8088"},
    )
    try:
        response = urllib.request.urlopen(request, timeout=20)
    except urllib.error.HTTPError as exc:
        response = exc
    body = response.read().decode("utf-8", errors="strict")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", body, flags=re.I | re.S)
    robots_match = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', body, flags=re.I)
    return {
        "actual_http_status": int(response.status),
        "final_url": response.geturl(),
        "x_robots_tag": response.headers.get("X-Robots-Tag", ""),
        "robots_meta": robots_match.group(1).strip() if robots_match else "",
        "rendered_title": re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "",
        "visible_marker": "yes" if any(token in body for token in ("[[PLACEHOLDER", "[[VERIFY", "[[REAL_PHOTO_PENDING")) else "no",
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    root = ET.parse(WXR).getroot()
    expected_titles = {
        int(wp_text(item, "wp:post_id")): (item.findtext("title") or "")
        for item in root.find("channel").findall("item")
        if wp_text(item, "wp:post_type") == "page"
    }

    targets = list(manifest) + [
        {
            "post_id": "",
            "url": "/_stage20-definitely-not-a-real-route/",
            "page_type": "404-control",
            "status": "not-a-page",
        }
    ]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda page: fetch(page["url"]), targets))

    rows: list[dict[str, object]] = []
    for page, actual in zip(targets, results, strict=True):
        expected_status = 200 if page["status"] == "publish" else 404
        if page["page_type"] == "404-control":
            decision = "PASS" if actual["actual_http_status"] == 404 else "FAIL"
            note = "Genuine 404 control request."
        else:
            decision = "BLOCKED"
            if page["status"] == "publish":
                note = "Authoritative import was rolled back; this is not the expected Camden page."
            else:
                note = "404 observed, but the draft is absent after rollback; imported draft handling is not proven."
        rows.append(
            {
                "URL": page["url"],
                "Page type": page["page_type"],
                "WXR status": page["status"],
                "Expected logged-out HTTP": expected_status,
                **actual,
                "Expected WXR title": expected_titles.get(page["post_id"], ""),
                "QA decision": decision,
                "Notes": note,
            }
        )

    fields = [
        "URL",
        "Page type",
        "WXR status",
        "Expected logged-out HTTP",
        "actual_http_status",
        "final_url",
        "x_robots_tag",
        "robots_meta",
        "rendered_title",
        "visible_marker",
        "Expected WXR title",
        "QA decision",
        "Notes",
    ]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "expected_routes": len(manifest),
        "control_routes": 1,
        "actual_200": sum(row["actual_http_status"] == 200 for row in rows),
        "actual_404": sum(row["actual_http_status"] == 404 for row in rows),
        "blocked_expected_routes": sum(row["QA decision"] == "BLOCKED" for row in rows),
        "control_404_pass": rows[-1]["QA decision"] == "PASS",
        "all_responses_protected": all("noindex" in str(row["x_robots_tag"]) for row in rows),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
