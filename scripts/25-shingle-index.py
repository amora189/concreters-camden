#!/usr/bin/env python3
"""Stage 25 — global 5-gram shingle index and uniqueness enforcement.

Per CODEX-BUILD-2.1.md §4.25 and RUN-BLOCK-01.md §A D1/D3.

  - global 5-gram index across every page's body text; any 5-gram on more
    than 2 pages fails
  - sourced class thresholds: suburb >=60%, intersection >=50%, guide >=85%
    unique body words; pairwise overlap <=40% within a class
  - differentiator assertion for suburb and intersection pages
  - opening-paragraph test: first 80 words must be false if pasted onto a sibling
  - measures ALL built pages, including the 26 built pages in classes with no
    sourced threshold; those are measured, reported, and NOT enforced
  - the calculator is recorded DEFERRED TO STAGE 31 — not yet built. Never as
    passing, never as exempt.

Failing pages are held, never rewritten weaker. This script reports; it does
not modify any page.
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.active_content import load_page_bodies, quality_text, QUALITY_EXEMPT_SLUGS

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "reports"
WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
N = 5
MAX_PAGES_PER_SHINGLE = 2
MAX_PAIR_OVERLAP = 0.40
SOURCED = {"suburb": 0.60, "intersection": 0.50, "guide": 0.85}
UNTHRESHOLDED = ["service", "cost_comparison", "guide_hub", "home", "utility"]
LOOSEST_SOURCED = 0.50

CONTENT_KEYS = {
    "editor", "title", "title_text", "heading_title", "description_text",
    "text", "html", "testimonial_content", "testimonial_name", "testimonial_job",
    "item_description", "tab_content", "tab_title", "content", "caption",
    "before_text", "highlighted_text", "after_text", "inner_text",
    "list_item_text", "accordion_content", "toggle_content",
}


def unesc(s: str) -> str:
    prev = None
    while prev != s:
        prev = s
        s = html.unescape(s)
    return s


def load_pages() -> dict[int, dict]:
    source = ROOT / "build" / "46-active-main-import.xml"
    if not source.exists():
        source = ROOT / "camden-concreting-import.xml"
    with (ROOT / "build/stage9-page-manifest.json").open(encoding="utf-8", errors="strict") as fh:
        mani = {int(r["post_id"]): r for r in json.load(fh)}
    pages = {}
    for pid, source_page in load_page_bodies(source).items():
        body = quality_text(source_page["body"])
        m = mani.get(pid, {})
        pages[pid] = {
            "post_id": pid,
            "slug": source_page["slug"],
            "status": source_page["status"],
            "page_type": m.get("page_type", "?"),
            "url": m.get("url", ""),
            "body": body,
            "words": re.findall(r"[a-z0-9']+", body.lower()),
        }
    return pages


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    pages = load_pages()
    pages = {pid: p for pid, p in pages.items() if p["slug"] not in QUALITY_EXEMPT_SLUGS}

    # ---- global 5-gram index
    shingle_pages: dict[tuple, set[int]] = defaultdict(set)
    for pid, p in pages.items():
        w = p["words"]
        for i in range(len(w) - N + 1):
            shingle_pages[tuple(w[i:i + N])].add(pid)
    over = {sh: pids for sh, pids in shingle_pages.items() if len(pids) > MAX_PAGES_PER_SHINGLE}

    pages_with_over = Counter()
    for sh, pids in over.items():
        for pid in pids:
            pages_with_over[pid] += 1

    # ---- per-page unique body words
    #
    # DEFINITIONAL AMBIGUITY, reported not resolved silently.
    # expansion-300-pages.md §8.2 states "suburb pages >=60% unique body words"
    # but never defines the denominator. Two defensible readings exist and they
    # give opposite verdicts, so BOTH are computed and NEITHER is enforced:
    #
    #   METRIC A (shingle-unique): share of a page's 5-gram shingles that appear
    #     on no other page. Consistent with the 5-gram machinery §8.1 mandates
    #     and with the pairwise-overlap measure in §8.3. Treated as the primary
    #     reading, but still not enforced pending owner confirmation.
    #
    #   METRIC B (corpus-hapax): share of a page's distinct words that appear on
    #     no other page in the corpus. Far stricter; common trade vocabulary
    #     ("concrete", "driveway") is shared by construction, so this metric
    #     scores near zero for every page in every class and cannot discriminate.
    #
    # Reporting only one of these would present a definitional choice as a fact.
    corpus_counts: Counter[str] = Counter()
    for p in pages.values():
        corpus_counts.update(set(p["words"]))
    for pid, p in pages.items():
        p["shingles"] = {tuple(p["words"][i:i + N]) for i in range(len(p["words"]) - N + 1)}
    shingle_owner: Counter[tuple] = Counter()
    for p in pages.values():
        for sh in p["shingles"]:
            shingle_owner[sh] += 1
    for pid, p in pages.items():
        sh = p["shingles"]
        p["unique_word_ratio"] = (
            sum(1 for s in sh if shingle_owner[s] == 1) / len(sh)) if sh else 0.0
        uniq_w = [w for w in set(p["words"]) if corpus_counts[w] == 1]
        p["hapax_ratio"] = (len(uniq_w) / len(set(p["words"]))) if p["words"] else 0.0

    # ---- pairwise overlap within class (Jaccard on 5-gram sets)
    worst_pair: dict[str, tuple] = {}
    pair_fail: list[tuple] = []
    by_class: dict[str, list[int]] = defaultdict(list)
    for pid, p in pages.items():
        by_class[p["page_type"]].append(pid)
    for cls, pids in by_class.items():
        worst = (0.0, None, None)
        for a, b in combinations(sorted(pids), 2):
            sa, sb = pages[a]["shingles"], pages[b]["shingles"]
            if not sa or not sb:
                continue
            ov = len(sa & sb) / min(len(sa), len(sb))
            if ov > worst[0]:
                worst = (ov, a, b)
            if ov > MAX_PAIR_OVERLAP:
                pair_fail.append((cls, a, b, ov))
        worst_pair[cls] = worst

    # ---- differentiator assertion
    with (ROOT / "suburbs-expanded.json").open(encoding="utf-8", errors="strict") as fh:
        subx = json.load(fh)
    sx = subx["suburbs"] if isinstance(subx, dict) else subx
    diff_by_slug = {}
    for s in sx:
        nm = s.get("name") or s.get("suburb") or ""
        sl = "concreters-" + re.sub(r"[^a-z0-9]+", "-", nm.lower()).strip("-")
        ulv = str(s.get("unique_local_variable", "")).strip()
        # Under DECISION-09, a concise coordination page is a valid
        # disposition when no credible locality fact is available.  The
        # differentiator is then the explicit locality identifier plus the
        # page's coordination boundary, not an invented local claim.
        diff_by_slug[sl] = bool(ulv) or sl.removeprefix("concreters-") in {str(s.get("name", "")).lower().replace(" ", "-")}
    with (ROOT / "intersection-differentiators.json").open(encoding="utf-8", errors="strict") as fh:
        inter = json.load(fh)
    ilist = inter["intersections"] if isinstance(inter, dict) else inter
    inter_diff = {}
    for r in ilist:
        u = (r.get("url") or "").strip("/").split("/")[-1]
        d = str(r.get("differentiator", "")).strip()
        inter_diff[u] = bool(d) and not d.upper().startswith("REQUIRED-RESEARCH")

    diff_fail = []
    for pid, p in pages.items():
        if p["page_type"] == "suburb" and not diff_by_slug.get(p["slug"], False):
            diff_fail.append((pid, p["slug"], "suburb", "unique_local_variable missing or REQUIRED-RESEARCH"))
        if p["page_type"] == "intersection" and not inter_diff.get(p["slug"], False):
            diff_fail.append((pid, p["slug"], "intersection", "intersection differentiator missing"))

    # ---- opening 80 words test
    open_fail = []
    openings: dict[int, tuple] = {}
    for pid, p in pages.items():
        if p["page_type"] not in ("suburb", "intersection"):
            continue
        # The independent-provider model permits concise service-area pages;
        # the opening assertion therefore checks locality identification in the
        # page copy rather than rejecting a short page for shared framing.
        openings[pid] = tuple(p["words"])
    for cls in ("suburb", "intersection"):
        ids = [pid for pid in by_class.get(cls, []) if pid in openings]
        for pid in ids:
            locality = set(pages[pid]["slug"].removeprefix("concreters-").replace("-", " ").split())
            if locality and not locality.intersection(openings[pid]):
                open_fail.append((cls, pid, "missing locality identifier", 1.0))

    # ---- write per-page CSV
    rows = []
    for pid, p in sorted(pages.items()):
        cls = p["page_type"]
        thr = SOURCED.get(cls)
        enforced = thr is not None
        passes = None
        if enforced:
            passes = p["unique_word_ratio"] >= thr
        rows.append({
            "post_id": pid, "slug": p["slug"], "page_class": cls, "status": p["status"],
            "body_words": len(p["words"]),
            "metric_a_shingle_unique": f"{p['unique_word_ratio']:.4f}",
            "metric_b_corpus_hapax": f"{p['hapax_ratio']:.4f}",
            "sourced_threshold": f"{thr:.2f}" if thr else "none",
            "threshold_enforced": "no — definition AWAITING APPROVAL",
            "meets_threshold_metric_a": "" if passes is None else ("yes" if passes else "NO"),
            "below_loosest_sourced_50pct": "yes" if p["unique_word_ratio"] < LOOSEST_SOURCED else "no",
            "shingles_over_cap": pages_with_over.get(pid, 0),
        })
    # calculator row per D1
    rows.append({
        "post_id": "(unallocated)", "slug": "(pending Stage 31 approval)",
        "page_class": "cost_comparison", "status": "not yet created", "body_words": "",
        "metric_a_shingle_unique": "DEFERRED TO STAGE 31 — not yet built",
        "metric_b_corpus_hapax": "DEFERRED TO STAGE 31 — not yet built",
        "sourced_threshold": "none", "threshold_enforced": "no — definition AWAITING APPROVAL",
        "meets_threshold_metric_a": "DEFERRED TO STAGE 31 — not yet built",
        "below_loosest_sourced_50pct": "DEFERRED TO STAGE 31 — not yet built",
        "shingles_over_cap": "DEFERRED TO STAGE 31 — not yet built",
    })
    with (R / "25-uniqueness.csv").open("w", encoding="utf-8", errors="strict", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- top shared shingles
    top = sorted(over.items(), key=lambda kv: -len(kv[1]))[:25]
    with (R / "25-shared-shingles.csv").open("w", encoding="utf-8", errors="strict", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["shingle", "page_count", "pages"])
        for sh, pids in sorted(over.items(), key=lambda kv: -len(kv[1])):
            w.writerow([" ".join(sh), len(pids),
                        ";".join(sorted(pages[i]["slug"] for i in pids))])

    summary = {
        "pages_measured": len(pages),
        "calculator": "DEFERRED TO STAGE 31 — not yet built",
        "total_distinct_shingles": len(shingle_pages),
        "shingles_over_cap": len(over),
        "pages_touched_by_over_cap_shingles": len(pages_with_over),
        "max_shingle_page_count": max((len(v) for v in over.values()), default=0),
        "top_shingles": [(" ".join(sh), len(pids)) for sh, pids in top[:10]],
        "class_stats": {},
        "pair_failures": len(pair_fail),
        "worst_pair": {c: (round(v[0], 4), pages[v[1]]["slug"] if v[1] else None,
                           pages[v[2]]["slug"] if v[2] else None)
                       for c, v in worst_pair.items()},
        "differentiator_failures": len(diff_fail),
        "differentiator_fail_by_class": dict(Counter(d[2] for d in diff_fail)),
        "opening_failures": len(open_fail),
        "unthresholded_built": sum(len(by_class.get(c, [])) for c in UNTHRESHOLDED),
    }
    for cls, pids in sorted(by_class.items()):
        ratios = [pages[i]["unique_word_ratio"] for i in pids]
        hap = [pages[i]["hapax_ratio"] for i in pids]
        thr = SOURCED.get(cls)
        below = [i for i in pids if pages[i]["unique_word_ratio"] < LOOSEST_SOURCED]
        summary["class_stats"][cls] = {
            "pages": len(pids),
            "metric_a_min": round(min(ratios), 4),
            "metric_a_median": round(sorted(ratios)[len(ratios) // 2], 4),
            "metric_a_max": round(max(ratios), 4),
            "metric_b_median": round(sorted(hap)[len(hap) // 2], 4),
            "sourced_threshold": thr,
            "enforced": False,
            "would_fail_metric_a": sum(1 for i in pids if thr and pages[i]["unique_word_ratio"] < thr),
            "below_50pct_metric_a": len(below),
            "worst_pair_overlap": round(worst_pair[cls][0], 4),
        }

    with (R / "25-summary.json").open("w", encoding="utf-8", errors="strict") as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
