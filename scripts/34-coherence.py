#!/usr/bin/env python3
"""Stage 34 — coherence scan. Measures whether sentences carry meaning.

Authority: DECISION-03-coherence-and-dispositions.md §D15.

The uniqueness gate measures DIFFERENCE. It scored 45 pages of machine-generated
filler among the most unique on the site, because the filler differs on every
page. This scans for the opposite property: whether a sentence asserts anything.

Scans ALL 156 pages, not the 45 already found.

Five detectors, per D15.1:
  T1  slug subject          sentence subject is a slug or URL fragment
                            ("new-driveway scope logs decision owner")
  T2  clause-head templating a block where >=4 clauses share a subject phrase
  T3  intra-sentence repeat  the same subject repeats inside one sentence
  T4  no verb of state/action a clause with no finite verb
  T5  vacuous assertion      built from bookkeeping verbs over abstract objects,
                            asserting nothing that could be false

MEASURES AND REPORTS ONLY. Fixes, rewrites and deletes nothing.
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "reports"
WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"

FILLER_THRESHOLD = 0.20   # proposed build-failing gate; see reports/34-coherence.md

CONTENT_KEYS = {
    "editor", "title", "title_text", "heading_title", "description_text", "text", "html",
    "testimonial_content", "testimonial_name", "testimonial_job", "item_description",
    "tab_content", "tab_title", "content", "caption", "before_text", "highlighted_text",
    "after_text", "inner_text", "list_item_text", "accordion_content", "toggle_content",
}

# Bookkeeping verbs: they describe record-keeping about a claim rather than
# making one. "X records the address" asserts nothing checkable about a driveway.
BOOKKEEPING = {
    "logs", "records", "cites", "documents", "tracks", "notes", "maps", "flags",
    "holds", "keeps", "retains", "identifies", "marks", "preserves", "links",
    "carries", "leaves", "states", "verifies", "checks", "lists", "separates",
    "measures", "tests", "attributes", "names", "dates", "stores", "reports",
}
# Abstract bookkeeping objects the above verbs take in the filler pattern.
ABSTRACT = {
    "provenance", "citation", "attribution", "basis", "record", "records", "owner",
    "authority", "source", "reference", "evidence", "trail", "identity", "boundary",
    "scope", "date", "person", "decision",
}
VERBS = re.compile(
    r"\b(is|are|was|were|be|been|being|has|have|had|do|does|did|can|could|will|"
    r"would|should|may|might|must|needs?|requires?|uses?|sits?|runs?|takes?|gives?|"
    r"makes?|goes?|comes?|gets?|puts?|sets?|helps?|means?|works?|costs?|adds?|"
    r"stops?|starts?|holds?|moves?|falls?|pours?|cures?|cracks?|swells?|shrinks?|"
    r"drains?|slopes?|forms?|builds?|lays?|cuts?|seals?|finish(es)?|prevent(s)?|"
    r"allow(s)?|"
    r"\w+(ed|ing)s?)\b", re.I)
SLUGWORD = re.compile(r"^[a-z0-9]+(-[a-z0-9]+){1,}$")
# Hyphenated English that is NOT a slug. Without this, "Mon-Fri 9:00AM - 5:00PM"
# on the utility pages trips the slug-subject detector and reports a contact
# block as machine-generated.
NOT_SLUGS = {
    "mon-fri", "mon-sat", "e-mail", "wi-fi", "co-op", "on-site", "off-street",
    "one-off", "long-term", "short-term", "day-to-day", "up-to-date", "self-levelling",
    "high-quality", "well-drained", "free-draining", "pre-mixed", "ready-mixed",
    "cross-fall", "non-slip", "heavy-duty", "single-storey", "two-storey",
}


def unesc(s: str) -> str:
    prev = None
    while prev != s:
        prev = s
        s = html.unescape(s or "")
    return s


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unesc(s))).strip()


def words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", s.lower())


def analyse_block(block: str) -> tuple[list[dict], int, int]:
    """Return (flagged clauses, total words, filler words) for one text block."""
    total_w = len(words(block))
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", block) if s.strip()]
    clauses_all = []
    for s in sentences:
        parts = [c.strip() for c in re.split(r";\s*", s) if c.strip()]
        clauses_all.append((s, parts))

    # T2 — clause-head templating across the whole block
    heads = Counter()
    flat = [c for _, parts in clauses_all for c in parts]
    for c in flat:
        heads[" ".join(c.split()[:2]).lower()] += 1
    templated_heads = {h for h, n in heads.items() if n >= 4}

    flagged: list[dict] = []
    filler_w = 0
    for sent, parts in clauses_all:
        hits = set()
        sw = words(sent)

        # T1 — slug subject
        first = sent.split()[0].strip(",.;:").lower() if sent.split() else ""
        if SLUGWORD.match(first) and first not in NOT_SLUGS:
            hits.add("T1")

        # T2
        for c in parts:
            if " ".join(c.split()[:2]).lower() in templated_heads:
                hits.add("T2")
                break

        # T3 — same subject repeated inside one sentence
        if len(parts) > 1:
            subs = [" ".join(c.split()[:2]).lower() for c in parts]
            if len(subs) != len(set(subs)):
                hits.add("T3")

        # T4 — a LONG clause with no finite verb.
        # Threshold is 8 words, not 4. A short verbless string is a UI label, a
        # heading or a service-tile caption ("Call us - 03 4517 6915",
        # "Mon-Fri 9:00AM - 5:00PM", "Side access, garden and front paths").
        # Those are legitimate site furniture, not filler, and counting them
        # inflated the first run's corpus figure from 45% to 85%.
        for c in parts:
            if len(words(c)) >= 8 and not VERBS.search(c):
                hits.add("T4")
                break

        # T5 — vacuous: bookkeeping verb over an abstract object
        for c in parts:
            cw = words(c)
            if any(v in cw for v in BOOKKEEPING) and any(a in cw for a in ABSTRACT):
                hits.add("T5")
                break

        # T4 alone is NOT sufficient to call a sentence filler. It is a weak
        # signal that fires on legitimate headings and labels. A sentence counts
        # as filler only if it trips one of the substantive detectors.
        substantive = hits & {"T1", "T2", "T3", "T5"}
        if hits:
            flagged.append({"sentence": sent, "tests": sorted(hits),
                            "counted": bool(substantive)})
        if substantive:
            filler_w += len(sw)

    return flagged, total_w, filler_w


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    tree = ET.parse(str(ROOT / "camden-concreting-import.xml"))
    mani = {int(r["post_id"]): r for r in json.loads(
        (ROOT / "build/stage9-page-manifest.json").read_text(encoding="utf-8", errors="strict"))}

    rows = []
    for it in tree.getroot().findall("./channel/item"):
        if (it.findtext(WP + "post_type") or "").strip() != "page":
            continue
        pid = int(it.findtext(WP + "post_id"))
        blocks = []
        pc = it.findtext(CONTENT + "encoded") or ""
        if pc.strip():
            blocks.append(clean(pc))
        for pm in it.findall(WP + "postmeta"):
            if (pm.findtext(WP + "meta_key") or "").strip() != "_elementor_data":
                continue
            try:
                data = json.loads(pm.findtext(WP + "meta_value") or "[]")
            except json.JSONDecodeError:
                continue

            def walk(n, key=None):
                if isinstance(n, dict):
                    for k, v in n.items():
                        walk(v, k)
                elif isinstance(n, list):
                    for v in n:
                        walk(v, key)
                elif isinstance(n, str) and key in CONTENT_KEYS:
                    t = clean(n)
                    if t:
                        blocks.append(t)

            walk(data)

        total_w = filler_w = 0
        all_flagged = []
        for b in blocks:
            fl, tw, fw = analyse_block(b)
            total_w += tw
            filler_w += fw
            all_flagged.extend(fl)

        m = mani.get(pid, {})
        pct = (filler_w / total_w) if total_w else 0.0
        counted = [f for f in all_flagged if f.get("counted")]
        tests = Counter(t for f in all_flagged for t in f["tests"])

        # SEVERITY. Two populations exist and must not be conflated:
        #
        #   SEVERE   the sentence subject is a slug or URL fragment (T1).
        #            "new-driveway scope records scope boundary" asserts nothing.
        #            This is machine-generated word salad.
        #
        #   MODERATE templated or nominalised prose with a real subject.
        #            "The Oran Park evidence register identifies Oran Park Precinct
        #            DCP 2007 ... and records the local housing period as
        #            2011-present" is stilted and over-nominalised, but it carries
        #            real, checkable content. It needs an editor, not a bin.
        #
        # Reporting these as one number would tell the owner to scrap the gold-
        # standard reference page alongside the word salad.
        slug_subject = sum(1 for f in counted if "T1" in f["tests"])
        severe_share = (slug_subject / len(counted)) if counted else 0.0
        pct_now = (filler_w / total_w) if total_w else 0.0
        if not counted:
            severity = "CLEAN"
        elif pct_now <= FILLER_THRESHOLD:
            # Severity is only meaningful above the threshold. Below it, a page
            # with one flagged sentence is not a filler page.
            severity = "BELOW THRESHOLD — not material"
        elif severe_share >= 0.5:
            severity = "SEVERE — slug-subject word salad"
        else:
            severity = "MODERATE — stilted prose, real content"
        # Samples are drawn from COUNTED sentences so the evidence shown matches
        # the figure reported, not from weak T4-only hits.
        samples = [f["sentence"] for f in counted[:3]]
        rows.append({
            "post_id": pid,
            "slug": (it.findtext(WP + "post_name") or "").strip(),
            "page_class": m.get("page_type", "?"),
            "status": (it.findtext(WP + "status") or "").strip(),
            "body_words": total_w,
            "filler_words": filler_w,
            "filler_pct": f"{pct:.4f}",
            "filler_sentences_counted": len(counted),
            "weak_flags_not_counted": len(all_flagged) - len(counted),
            "severity": severity,
            "slug_subject_sentences": slug_subject,
            "severe_share_of_counted": f"{severe_share:.3f}",
            "T1_slug_subject": tests.get("T1", 0),
            "T2_clause_templating": tests.get("T2", 0),
            "T3_intra_sentence_repeat": tests.get("T3", 0),
            "T4_no_verb": tests.get("T4", 0),
            "T5_vacuous_assertion": tests.get("T5", 0),
            "exceeds_threshold": "YES" if pct > FILLER_THRESHOLD else "no",
            "sample_1": samples[0][:400] if len(samples) > 0 else "",
            "sample_2": samples[1][:400] if len(samples) > 1 else "",
            "sample_3": samples[2][:400] if len(samples) > 2 else "",
        })

    rows.sort(key=lambda r: -float(r["filler_pct"]))
    with (R / "34-coherence.csv").open("w", encoding="utf-8", errors="strict", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    over = [r for r in rows if r["exceeds_threshold"] == "YES"]
    by_class = Counter(r["page_class"] for r in over)
    all_class = Counter(r["page_class"] for r in rows)
    tot_w = sum(r["body_words"] for r in rows)
    tot_f = sum(r["filler_words"] for r in rows)

    sev = Counter(r["severity"].split(" —")[0] for r in rows)
    sev_by_class = defaultdict(Counter)
    for r in rows:
        sev_by_class[r["page_class"]][r["severity"].split(" —")[0]] += 1
    severe_pages = [r for r in rows if r["severity"].startswith("SEVERE")]
    severe_words = sum(r["filler_words"] for r in severe_pages)

    summary = {
        "pages_scanned": len(rows),
        "threshold": FILLER_THRESHOLD,
        "severity_counts": dict(sev),
        "severity_by_class": {k: dict(v) for k, v in sorted(sev_by_class.items())},
        "severe_pages": len(severe_pages),
        "severe_filler_words": severe_words,
        "pages_over_threshold": len(over),
        "pages_with_any_filler": sum(1 for r in rows if r["filler_words"] > 0),
        "pages_clean": sum(1 for r in rows if r["filler_words"] == 0),
        "total_body_words": tot_w,
        "total_filler_words": tot_f,
        "corpus_filler_pct": round(tot_f / tot_w, 4) if tot_w else 0,
        "over_by_class": dict(by_class),
        "all_by_class": dict(all_class),
        "worst": [(r["slug"], r["page_class"], r["filler_pct"]) for r in rows[:12]],
        "best": [(r["slug"], r["page_class"], r["filler_pct"]) for r in rows[-8:]],
    }
    (R / "34-coherence-summary.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
