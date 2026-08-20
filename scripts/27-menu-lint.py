#!/usr/bin/env python3
"""Stage 27 — menu lint. Fail-closed.

Fails if any menu item resolves to a draft page, a noindex page, or a 404
(an object_id that resolves to no page in the main WXR).

Usage:
    python scripts/27-menu-lint.py                      # lint build/27-wave1-menus.json
    python scripts/27-menu-lint.py --full-imported-set  # lint all 65 imported items

Gate 27 requires the first to PASS and the second to FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = "{http://wordpress.org/export/1.2/}"
WAVE1 = ROOT / "build" / "27-wave1-menus.json"


def load_pages() -> dict[int, dict]:
    tree = ET.parse(str(ROOT / "camden-concreting-import.xml"))
    with (ROOT / "build/stage9-page-manifest.json").open(encoding="utf-8", errors="strict") as fh:
        mani = {int(r["post_id"]): r for r in json.load(fh)}
    out = {}
    for it in tree.getroot().findall("./channel/item"):
        if (it.findtext(WP + "post_type") or "").strip() != "page":
            continue
        pid = int((it.findtext(WP + "post_id") or "0").strip())
        m = mani.get(pid, {})
        out[pid] = {
            "slug": (it.findtext(WP + "post_name") or "").strip(),
            "status": (it.findtext(WP + "status") or "").strip(),
            "page_type": m.get("page_type", "?"),
        }
    return out


def load_menu_items() -> list[dict]:
    tree = ET.parse(str(ROOT / "camden-concreting-import.xml"))
    items = []
    for it in tree.getroot().findall("./channel/item"):
        if (it.findtext(WP + "post_type") or "").strip() != "nav_menu_item":
            continue
        meta = {(pm.findtext(WP + "meta_key") or ""): (pm.findtext(WP + "meta_value") or "")
                for pm in it.findall(WP + "postmeta")}
        items.append({
            "post_id": int((it.findtext(WP + "post_id") or "0").strip()),
            "title": (it.findtext("title") or "").strip(),
            "object_id": meta.get("_menu_item_object_id", ""),
            "type": meta.get("_menu_item_type", ""),
            "_menu_item_menu_item_parent": meta.get("_menu_item_menu_item_parent", ""),
            "nav_menu": [c.text for c in it.findall("category") if c.get("domain") == "nav_menu"],
        })
    return items


def noindex(page: dict) -> bool:
    """A page held noindex,follow under the current release gates."""
    if page["page_type"] == "suburb":
        return True                       # all 60 suburbs held
    if page["slug"] == "gallery":
        return True
    return page["page_type"] in ("guide", "guide_hub", "intersection", "cost_comparison")


def lint(items: list[dict], pages: dict[int, dict], label: str) -> int:
    failures: list[str] = []
    reasons: Counter[str] = Counter()
    ids = {i["post_id"] for i in items}

    for it in items:
        oid = it.get("object_id", "")
        if it.get("type") == "custom":
            continue
        if not oid.isdigit() or int(oid) not in pages:
            failures.append(f"item {it['post_id']} '{it['title']}': 404 — object_id "
                            f"{oid!r} resolves to no page in the main WXR")
            reasons["404"] += 1
            continue
        page = pages[int(oid)]
        if page["status"] != "publish":
            failures.append(f"item {it['post_id']} '{it['title']}': target /{page['slug']}/ "
                            f"is {page['status']}")
            reasons["draft target"] += 1
            continue
        if noindex(page):
            failures.append(f"item {it['post_id']} '{it['title']}': target /{page['slug']}/ "
                            f"is held noindex,follow")
            reasons["noindex target"] += 1
            continue

    parent = it = None
    for i in items:
        p = i.get("_menu_item_menu_item_parent", "")
        if p and p != "0" and int(p) not in ids:
            failures.append(f"item {i['post_id']} '{i['title']}': parent {p} is not in this set")
            reasons["orphaned parent"] += 1

    print(f"--- {label} ---")
    print(f"  items linted   {len(items)}")
    print(f"  failures       {len(failures)}")
    for k, v in reasons.most_common():
        print(f"    {k:<18} {v}")
    for f in failures[:12]:
        print(f"    - {f}")
    if len(failures) > 12:
        print(f"    ... and {len(failures)-12} more")
    print(f"  VERDICT        {'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-imported-set", action="store_true")
    args = ap.parse_args()
    pages = load_pages()

    if args.full_imported_set:
        return lint(load_menu_items(), pages, "FULL IMPORTED SET (65 items)")

    with WAVE1.open(encoding="utf-8", errors="strict") as fh:
        w1 = json.load(fh)
    expected_gallery_hold = [{
        "page_id": 1365,
        "slug": "gallery",
        "navigation_disposition": "excluded from all launch menu assignments",
        "authority": "Owner approval dated 20 August 2026 — FINAL IMAGE REMEDIATION prompt",
    }]
    if w1.get("owner_deferred_pages") != expected_gallery_hold:
        print("FAIL — gallery deferral is absent or differs from the exact owner-approved disposition")
        return 1
    if any(str(item.get("object_id", "")) == "1365" for item in w1["items"]):
        print("FAIL — gallery remains in the launch menu specification")
        return 1
    return lint(w1["items"], pages, "WAVE 1 MENU SPEC (build/27-wave1-menus.json)")


if __name__ == "__main__":
    raise SystemExit(main())
