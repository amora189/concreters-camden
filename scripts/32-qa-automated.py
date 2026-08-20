#!/usr/bin/env python3
"""Stage 32 — the automatable subset of the QA specification.

NOT RUN IN THIS WORK BLOCK. It executes against authoritative staging only
after Gate 28 returns GO, and its output feeds the page-by-page release
decision.

Fail-closed, machine-readable output. Covers only the checks that can be
verified mechanically. The human-sighted subset is specified in
reports/32-qa-spec.md and has NO automated shortcut.

Usage:
    python scripts/32-qa-automated.py --base http://127.0.0.1:8099 --out reports/32-qa-results.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 160
PLACEHOLDER_TOKENS = ("PLACEHOLDER", "REAL_PHOTO_PENDING", "REQUIRED-RESEARCH", "VERIFY")
BLOCKLIST = ["Melbourne", "Werribee", "Wyndham", "Point Cook", "Tarneit", "Truganina",
             "Hoppers Crossing", "Riverwalk", "Harpley", "Victoria", "VIC",
             "03 4427 9541", "bestconcretersmelbourne.com.au"]


def fetch(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Camden-Stage32-QA/1.0 (logged-out)"})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        resp = exc
    except urllib.error.URLError as exc:
        return {"error": str(exc), "status": 0, "body": "", "headers": {}}
    # strict decode: a mojibake page must FAIL, not be silently repaired (§3.1)
    raw = resp.read()
    try:
        body = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return {"error": f"response is not valid UTF-8: {exc}", "status": resp.status,
                "body": "", "headers": dict(resp.headers)}
    return {"status": resp.status, "final_url": resp.geturl(), "body": body,
            "headers": dict(resp.headers), "error": None}


def check_page(base: str, rec: dict) -> dict:
    url = base.rstrip("/") + rec["url"]
    r = fetch(url)
    checks: list[dict] = []

    def add(cid, name, ok, detail):
        checks.append({"id": cid, "name": name,
                       "result": "PASS" if ok else "FAIL", "detail": detail})

    if r["error"]:
        add("A1", "HTTP status", False, r["error"])
        return {"url": rec["url"], "post_id": rec["post_id"], "checks": checks}

    body = r["body"]
    expected = 200 if rec["status"] == "publish" else 404
    add("A1", "HTTP status (logged out)", r["status"] == expected,
        f"got {r['status']}, expected {expected} for status={rec['status']}")

    add("A2", "no redirect chain to a different path",
        r.get("final_url", url).rstrip("/") == url.rstrip("/"),
        f"final_url={r.get('final_url')}")

    # canonical
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', body, re.I)
    canon = m.group(1) if m else ""
    add("A3", "canonical present and matches served URL",
        bool(canon) and canon.rstrip("/") == url.rstrip("/"),
        f"canonical={canon or 'ABSENT'}")

    # robots
    m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', body, re.I)
    robots = m.group(1).strip().lower() if m else ""
    xrobots = r["headers"].get("X-Robots-Tag", "").lower()
    add("A4", "robots directive matches the release plan",
        "noindex" in robots or "noindex" in xrobots,
        f"meta={robots or 'ABSENT'}, header={xrobots or 'ABSENT'}")

    # headings
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
    add("A5", "exactly one H1", len(h1) == 1, f"found {len(h1)}")
    heads = [int(h) for h in re.findall(r"<h([1-6])[^>]*>", body, re.I)]
    skips = [f"h{a}->h{b}" for a, b in zip(heads, heads[1:]) if b > a + 1]
    add("A6", "no heading level skipped", not skips, f"{skips[:5]}")

    # meta lengths
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    add("A7", f"title {TITLE_MIN}-{TITLE_MAX} chars",
        TITLE_MIN <= len(title) <= TITLE_MAX, f"{len(title)} chars: {title[:70]!r}")
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', body, re.I)
    desc = (m.group(1) if m else "").strip()
    add("A8", f"meta description {DESC_MIN}-{DESC_MAX} chars",
        DESC_MIN <= len(desc) <= DESC_MAX, f"{len(desc)} chars")

    # media resolution
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)', body, re.I)
    broken = []
    for s in srcs:
        full = s if s.startswith("http") else base.rstrip("/") + s
        h = fetch(full, timeout=10)
        if h["status"] != 200:
            broken.append((s, h["status"]))
    add("A9", "every image resolves", not broken,
        f"{len(srcs)} images, {len(broken)} broken: {broken[:3]}")

    # internal links
    hrefs = re.findall(r'<a[^>]+href=["\'](/[^"\'#?]*)', body)
    bad = []
    for h in sorted(set(hrefs)):
        resp = fetch(base.rstrip("/") + h, timeout=10)
        if resp["status"] not in (200, 301, 302):
            bad.append((h, resp["status"]))
    add("A10", "every internal link resolves", not bad,
        f"{len(set(hrefs))} links, {len(bad)} broken: {bad[:3]}")

    # schema validity
    blobs = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body, re.S | re.I)
    invalid, dangling = 0, 0
    for b in blobs:
        try:
            g = json.loads(b)
        except json.JSONDecodeError:
            invalid += 1
            continue
        nodes = g.get("@graph", []) if isinstance(g, dict) else []
        defined = {n.get("@id") for n in nodes if isinstance(n, dict)}
        for n in nodes:
            for v in (n or {}).values():
                if isinstance(v, dict) and set(v) == {"@id"} and v["@id"] not in defined:
                    dangling += 1
    add("A11", "JSON-LD valid with no dangling @id",
        invalid == 0 and dangling == 0,
        f"{len(blobs)} blocks, {invalid} invalid, {dangling} dangling")

    # placeholders in rendered output
    found = {t: body.count(t) for t in PLACEHOLDER_TOKENS if body.count(t)}
    add("A12", "zero evidence markers in rendered HTML", not found, f"{found}")

    # Victorian blocklist
    hits = {b: body.count(b) for b in BLOCKLIST if body.count(b)}
    add("A13", "Victorian blocklist zero", not hits, f"{hits}")

    return {"url": rec["url"], "post_id": rec["post_id"], "status": rec["status"],
            "checks": checks}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", default="reports/32-qa-results.json")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    manifest = json.loads((ROOT / "build/stage9-page-manifest.json").read_text(
        encoding="utf-8", errors="strict"))
    if args.limit:
        manifest = manifest[:args.limit]

    results = [check_page(args.base, r) for r in manifest]

    tally: Counter[str] = Counter()
    per_check: dict[str, Counter] = {}
    for page in results:
        for c in page["checks"]:
            tally[c["result"]] += 1
            per_check.setdefault(c["id"], Counter())[c["result"]] += 1

    out = {
        "base": args.base,
        "pages_checked": len(results),
        "checks_per_page": len(results[0]["checks"]) if results else 0,
        "totals": dict(tally),
        "per_check": {k: dict(v) for k, v in sorted(per_check.items())},
        "verdict": "PASS" if tally["FAIL"] == 0 else "FAIL",
        "pages": results,
    }
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "pages"}, indent=1))
    return 0 if tally["FAIL"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
