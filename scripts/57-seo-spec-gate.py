#!/usr/bin/env python3
"""Spec sections 6.5 and 8 as build assertions over `build/cloudflare-pages/`.

Exit 0 only when every assertion passes. Assertions retired or amended by a decision
record name the decision inline; nothing is silently relaxed. See CLAUDE.md section 3
hard stop 7 — a check that cannot run at full fidelity is reported BLOCKED, never
narrowed to make it pass.

Usage:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/57-seo-spec-gate.py
"""
from __future__ import annotations

import html as H
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import seo_spec  # noqa: E402

OUT = ROOT / "build" / "cloudflare-pages"
BASE = "https://concreterscamden.com.au"


def utf8_canary() -> None:
    """CLAUDE.md section 4. Full read-write-compare cycle before trusting any content gate."""
    probe = "em—dash en–dash 32 MPa m² non breaking"
    scratch = OUT / ".utf8-canary"
    scratch.write_text(probe, encoding="utf-8")
    got = scratch.read_text(encoding="utf-8")
    scratch.unlink()
    if got != probe:
        raise SystemExit("UTF-8 canary failed; content gates cannot be trusted on this console")


def load() -> dict[str, dict]:
    pages: dict[str, dict] = {}
    for path in sorted(OUT.rglob("index.html")):
        rel = os.path.relpath(path, OUT).replace(os.sep, "/")
        src = path.read_text(encoding="utf-8")
        pages["/" + rel.replace("index.html", "")] = {
            "src": src,
            "title": H.unescape(first(src, r"<title>(.*?)</title>") or ""),
            "h1": H.unescape(re.sub(r"<[^>]+>", "", first(src, r"<h1[^>]*>(.*?)</h1>") or "")),
            "robots": first(src, r'<meta name="robots" content="(.*?)"') or "index,follow",
            "description": H.unescape(first(src, r'<meta name="description" content="(.*?)"') or ""),
            "ld": [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)],
        }
    return pages


def first(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, re.S)
    return m.group(1) if m else None


def nodes(page: dict, kind: str) -> list[dict]:
    found = []
    for blob in page["ld"]:
        for node in blob.get("@graph", [blob]):
            if node.get("@type") == kind:
                found.append(node)
    return found


RESULTS: list[tuple[str, str, str]] = []


def assert_(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, "PASS" if ok else "FAIL", detail))


def blocked(name: str, detail: str) -> None:
    RESULTS.append((name, "BLOCKED", detail))


def retired(name: str, detail: str) -> None:
    RESULTS.append((name, "RETIRED", detail))


def main() -> int:
    utf8_canary()
    pages = load()
    suburbs = {u: p for u, p in pages.items() if u.startswith("/concreters-")}
    services = {u: p for u, p in pages.items() if u.startswith("/services/") and u != "/services/"}

    # ---------------------------------------------------------------- section 8
    assert_("no 'enquir' in any title or h1",
            not [u for u, p in pages.items() if "enquir" in p["title"].lower() or "enquir" in p["h1"].lower()],
            "titles and H1s")
    assert_("no 'near me' in any title, h1 or URL",
            not [u for u, p in pages.items() if "near me" in p["title"].lower() or "near me" in p["h1"].lower() or "near-me" in u])
    over = {u: len(p["title"]) for u, p in pages.items() if len(p["title"]) > 60}
    assert_("every title <= 60 characters", not over, "; ".join(f"{u} ({n})" for u, n in over.items()))
    dupes = {t: c for t, c in Counter(p["title"] for p in pages.values()).items() if c > 1}
    assert_("every title unique sitewide", not dupes, "; ".join(dupes))

    # DECISION-10 D43-R1. A word in a title is a promise: `Cost`, `Price`, `$`, `Quote`,
    # `Thickness`, `Mesh` and `Specs` each require the matching content module to be
    # declared on that page. Prevents the class of defect, not the two instances found.
    unkept = []
    for url, page in pages.items():
        for word, module in seo_spec.title_promises(page["title"]).items():
            if f'data-module="{module}"' not in page["src"]:
                unkept.append(f'{url}: title says "{word}" but carries no {module} module')
    assert_("no title promises a content module the page does not carry",
            not unkept, "; ".join(unkept))

    unsourced = []
    for slug, row in seo_spec.SUBURB_SPEC.items():
        if slug == seo_spec.HOMEPAGE_SUBURB:
            continue
        url = f"/concreters-{slug}/"
        page = pages.get(url)
        if not page:
            unsourced.append(f"{url} missing")
        elif page["title"] != row["title_tag"]:
            unsourced.append(f"{url} title not from suburbs.json")
        elif page["description"] != row["meta_description"]:
            unsourced.append(f"{url} description not from suburbs.json")
    assert_("spec suburb titles and descriptions resolved from suburbs.json, no template fallback",
            not unsourced, "; ".join(unsourced))

    # Spec section 1: 150-158 characters. Applied to descriptions authored here. The 16
    # suburbs.json descriptions are exempt: the spec orders them used verbatim and only
    # 4 of 16 fall inside the range (reports/57-spec-conflicts.md C4).
    verbatim = {row["meta_description"] for row in seo_spec.SUBURB_SPEC.values()}
    off_length = {u: len(p["description"]) for u, p in pages.items()
                  if p["description"] not in verbatim and not 150 <= len(p["description"]) <= 158}
    assert_("authored meta descriptions are 150-158 characters",
            not off_length, "; ".join(f"{u} ({n})" for u, n in off_length.items()))
    assert_("suburbs.json meta descriptions are used verbatim, length rule waived (C4)",
            all(pages[f"/concreters-{s}/"]["description"] == r["meta_description"]
                for s, r in seo_spec.SUBURB_SPEC.items() if s != seo_spec.HOMEPAGE_SUBURB),
            f"{len(seo_spec.SUBURB_SPEC) - 1} descriptions, 126-182 chars as authored in suburbs.json")

    # -------------------------------------------- fallback tier (DECISION-10 D45)
    banned = ("enquir", "near me", "best", "cheap", "#1")
    fallback_urls = sorted(u for u in pages
                           if u.startswith("/concreters-")
                           and u.removeprefix("/concreters-").rstrip("/") not in seo_spec.SUBURB_SPEC)
    pattern_bad, banned_hits = [], []
    for url in fallback_urls:
        page = pages[url]
        want = seo_spec.suburb_title(url.strip("/"))
        if page["title"] != want:
            pattern_bad.append(f"{url}: {page['title']!r} != {want!r}")
        for word in banned:
            if word in page["title"].lower() or word in page["h1"].lower():
                banned_hits.append(f'{url}: "{word}"')
    assert_("fallback-tier titles follow the documented pattern",
            not pattern_bad, "; ".join(pattern_bad[:4]))
    assert_("no title or h1 contains enquir / near me / best / cheap / #1",
            not banned_hits and not [u for u, p in pages.items()
                                     if any(w in p["title"].lower() or w in p["h1"].lower() for w in banned)],
            "; ".join(banned_hits[:4]))
    dupe_desc = {d: c for d, c in Counter(p["description"] for p in pages.values()).items() if c > 1}
    assert_("every meta description unique sitewide", not dupe_desc, "; ".join(list(dupe_desc)[:2]))
    # Generic-but-true: a fallback page must not carry a suburb-specific claim it has no
    # data for. The section 5.4 block and the near-me FAQ are the only places those live.
    fabricated = [u for u in fallback_urls
                  if 'class="suburb-service"' in pages[u]["src"] or nodes(pages[u], "FAQPage")]
    assert_("no fallback-tier page carries a fabricated suburb specific",
            not fabricated, "; ".join(fabricated[:4]))

    # ------------------------------------------- postcodes (verified file only)
    emitted, unlisted, mismatched_pc = {}, [], []
    for url, page in pages.items():
        if not url.startswith("/concreters-"):
            continue  # service pages carry a coarse string areaServed, not a Place
        for node in nodes(page, "Service"):
            area = node.get("areaServed")
            if not isinstance(area, dict):
                continue
            got = area["address"]["postalCode"]
            emitted[url] = got
            if got not in seo_spec.PERMITTED_POSTCODES:
                unlisted.append(f"{url}: {got}")
            want, _ = seo_spec.postcode_provenance(url.strip("/"))
            if want != got:
                mismatched_pc.append(f"{url}: emitted {got}, file says {want}")
    assert_("no postalCode emitted that is absent from camden-verified-postcodes.json",
            not unlisted, "; ".join(unlisted[:6]))
    assert_("every emitted postalCode matches camden-verified-postcodes.json",
            not mismatched_pc, "; ".join(mismatched_pc[:6]))
    omitted_area = sorted(u for u in pages
                          if u.startswith("/concreters-") and u not in emitted)
    assert_("areaServed omitted rather than guessed where the file has no entry",
            all(seo_spec.postcode_provenance(u.strip("/"))[0] is None for u in omitted_area),
            f"{len(omitted_area)} pages: {', '.join(u.strip('/').removeprefix('concreters-') for u in omitted_area)}")

    # ---------------------------------------------------- FAQ blocks not empty
    empty_faq = []
    for url, page in pages.items():
        for node in nodes(page, "FAQPage"):
            if not node.get("mainEntity"):
                empty_faq.append(f"{url}: empty mainEntity")
            for qa in node.get("mainEntity", []):
                text = (qa.get("acceptedAnswer") or {}).get("text", "").strip()
                if not qa.get("name", "").strip() or not text:
                    empty_faq.append(f"{url}: empty Q or A")
                if re.search(r"\[\[|\{[A-Z_]{3,}\}|TBC|TBA", qa.get("name", "") + text):
                    empty_faq.append(f"{url}: placeholder in FAQ")
    assert_("no empty or placeholder FAQ entry", not empty_faq, "; ".join(empty_faq[:4]))

    assert_("/areas/ exists and is indexable",
            "/areas/" in pages and not pages["/areas/"]["robots"].startswith("noindex"))
    assert_("/services/ exists and is indexable",
            "/services/" in pages and not pages["/services/"]["robots"].startswith("noindex"))

    redirects = (OUT / "_redirects").read_text(encoding="utf-8")
    rules = [line.split() for line in redirects.splitlines() if line and not line.startswith("#")]
    targets = {src: dst for src, dst, _code in rules}
    assert_("/concreters-camden/ 301s to /",
            targets.get("/concreters-camden/") == "/" and not (OUT / "concreters-camden").exists())
    missing_301 = [f"/{old}/" for old in seo_spec.SERVICE_MOVE if targets.get(f"/{old}/") != seo_spec.service_path(old)]
    assert_("every old flat service URL 301s to /services/{slug}/", not missing_301, "; ".join(missing_301))
    chains = [src for src, dst in targets.items() if dst in targets]
    loops = [src for src, dst in targets.items() if dst == src]
    assert_("no redirect chains and no loops", not chains and not loops, f"chains={chains} loops={loops}")
    stale = [f"/{old}/" for old in seo_spec.SERVICE_MOVE if (OUT / old).exists()]
    assert_("no flat service directory still serves a page", not stale, "; ".join(stale))

    # ---------------------------------------------------------------- section 6.5
    frag, too_many, terminal, mismatch, subject = [], [], [], [], []
    for url, page in pages.items():
        for node in nodes(page, "BreadcrumbList"):
            items = node["itemListElement"]
            if any("#" in (i.get("item") or "") for i in items):
                frag.append(url)
            if len(items) > 3:
                too_many.append(url)
            if items[-1].get("item"):
                terminal.append(url)
            visible = first(page["src"], r'(<nav class="breadcrumbs".*?</nav>)')
            if visible:
                labels = [H.unescape(x) for x in re.findall(r"<a [^>]*>([^<]+)</a>|<span aria-current=\"page\">([^<]+)</span>", visible) for x in x if x]
                names = [i["name"] for i in items]
                if labels != names:
                    mismatch.append(f"{url}: {labels} vs {names}")
            # Scoped to suburb, service and hub pages. The spec's own section 6.2 table
            # pairs "Home / Contact" with an H1 of "Get a Concreting Quote in Camden", so
            # the rule cannot hold on utility pages as the spec itself writes them.
            last = items[-1]["name"]
            scoped = url.startswith("/concreters-") or url.startswith("/services/") or url == "/areas/"
            if scoped and last.lower() not in page["h1"].lower() and page["h1"].lower() not in last.lower():
                subject.append(f"{url}: crumb '{last}' vs h1 '{page['h1']}'")
    assert_("no '#' in any BreadcrumbList item", not frag, "; ".join(frag))
    assert_("no BreadcrumbList exceeds 3 items", not too_many, "; ".join(too_many))
    assert_("terminal ListItem carries no item", not terminal, "; ".join(terminal))
    assert_("visible breadcrumb labels match JSON-LD names", not mismatch, "; ".join(mismatch[:4]))
    assert_("terminal crumb matches the page h1 subject", not subject, "; ".join(subject[:4]))
    assert_("homepage carries no breadcrumb", not nodes(pages["/"], "BreadcrumbList"))
    crumb_urls = {i["item"] for p in pages.values() for n in nodes(p, "BreadcrumbList") for i in n["itemListElement"] if i.get("item")}
    dead = [u for u in crumb_urls if u.replace(BASE, "") not in pages]
    assert_("every crumb URL resolves to a built page", not dead, "; ".join(dead))

    # ---------------------------------------------------------------- indexation
    # DECISION-10 D45 supersedes the D44 gate. The tier logic is retained in
    # seo_spec.suburb_robots(); setting INDEX_ALL_SUBURBS = False re-arms it and this
    # assertion flips back with it.
    if seo_spec.INDEX_ALL_SUBURBS:
        noindexed = sorted(u for u, p in suburbs.items() if p["robots"].startswith("noindex"))
        assert_("every suburb page is index,follow (DECISION-10 D45)",
                not noindexed, f"{len(suburbs)} suburb pages indexed; noindex on {noindexed}")
        assert_("D45 re-armable: the D44 tier gate is retained, not deleted",
                seo_spec.suburb_robots.__doc__ is not None and bool(seo_spec.TIER1),
                f"INDEX_ALL_SUBURBS=False restores Tier 1 only ({len(seo_spec.TIER1)} pages)")
    else:
        indexable_subs = sorted(u for u, p in suburbs.items() if not p["robots"].startswith("noindex"))
        expected = sorted(f"/concreters-{s}/" for s in seo_spec.TIER1)
        assert_("exactly the 6 Tier 1 suburb pages are index,follow",
                indexable_subs == expected, f"got {indexable_subs}")
        noindexed = [u for u, p in suburbs.items() if p["robots"] != "noindex,follow" and u not in expected]
        assert_("every non-Tier-1 suburb page is noindex,follow (DECISION-10 D44)",
                not noindexed, "; ".join(noindexed))
    sitemap = (OUT / "sitemap.xml").read_text(encoding="utf-8")
    locs = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
    in_sitemap_noindex = [u for u, p in pages.items() if p["robots"].startswith("noindex") and BASE + u in locs]
    assert_("sitemap contains zero noindex URLs", not in_sitemap_noindex, "; ".join(in_sitemap_noindex))
    missing_from_sitemap = [u for u, p in pages.items() if not p["robots"].startswith("noindex") and BASE + u not in locs]
    assert_("every indexable page is in the sitemap", not missing_from_sitemap, "; ".join(missing_from_sitemap))
    indexable_set = {BASE + u for u, p in pages.items() if not p["robots"].startswith("noindex")}
    assert_("sitemap matches the indexable set exactly", locs == indexable_set,
            f"{len(locs)} URLs in sitemap, {len(indexable_set)} indexable pages")

    # ---------------------------------------------------------------- schema
    assert_("no LocalBusiness or GeneralContractor node outside / and /contact/",
            not [u for u, p in pages.items() if (nodes(p, "LocalBusiness") or nodes(p, "GeneralContractor")) and u not in ("/", "/contact/")])
    assert_("no AggregateRating or Review markup anywhere",
            not [u for u, p in pages.items() if "AggregateRating" in p["src"] or '"Review"' in p["src"]])
    faq_bad = []
    for url, page in pages.items():
        for node in nodes(page, "FAQPage"):
            for qa in node["mainEntity"]:
                for text in (qa["name"], qa["acceptedAnswer"]["text"]):
                    if H.escape(text) not in page["src"] and text not in page["src"]:
                        faq_bad.append(f"{url}: {text[:60]}")
    assert_("every FAQPage Q&A string appears verbatim in the rendered HTML", not faq_bad, "; ".join(faq_bad[:3]))
    spec_subs = [f"/concreters-{s}/" for s in seo_spec.SUBURB_SPEC if s != seo_spec.HOMEPAGE_SUBURB]
    no_service = [u for u in spec_subs if not nodes(pages[u], "Service")]
    assert_("every in-scope suburb page carries a Service node with areaServed", not no_service, "; ".join(no_service))
    bad_pc = []
    for url in spec_subs:
        for node in nodes(pages[url], "Service"):
            got = node["areaServed"]["address"]["postalCode"]
            want = seo_spec.SUBURB_SPEC[url.removeprefix("/concreters-").rstrip("/")]["postcode"]
            if got != want:
                bad_pc.append(f"{url}: {got} != {want}")
    assert_("areaServed postalCode comes from suburbs.json", not bad_pc, "; ".join(bad_pc))
    dangling = [u for u, p in pages.items() if "#organization" in p["src"] and not nodes(p, "Organization")]
    assert_("no dangling #organization reference", not dangling, "; ".join(dangling))

    # ---------------------------------------------------------------- near-me
    missing_h2 = [u for u in spec_subs if "Looking for concreters near you in" not in pages[u]["src"]]
    assert_("spec section 5.1 near-me H2 on every in-scope suburb page", not missing_h2, "; ".join(missing_h2))
    doubled = [u for u in spec_subs if pages[u]["src"].count("Looking for concreters near you in") > 1]
    assert_("near-me H2 appears exactly once per page", not doubled, "; ".join(doubled))
    missing_faq = [u for u in spec_subs if not nodes(pages[u], "FAQPage")]
    assert_("spec section 5.2 near-me FAQ on every in-scope suburb page", not missing_faq, "; ".join(missing_faq))
    length_bad = []
    for url in spec_subs:
        for node in nodes(pages[url], "FAQPage"):
            for qa in node["mainEntity"]:
                words = len(qa["acceptedAnswer"]["text"].split())
                if not 40 <= words <= 60:
                    length_bad.append(f"{url}: {words} words")
    assert_("near-me FAQ answers are 40-60 words", not length_bad, "; ".join(length_bad[:6]))
    block_bad, para_bad = [], []
    for url in spec_subs:
        h3s = re.findall(r'<article class="suburb-service"><h3>.*?</h3><p>(.*?)</p>', pages[url]["src"], re.S)
        if not 3 <= len(h3s) <= 5:
            block_bad.append(f"{url}: {len(h3s)} services")
        for para in h3s:
            words = len(H.unescape(para).split())
            if not 40 <= words <= 70:
                para_bad.append(f"{url}: {words} words")
    assert_("spec section 5.4 lists 3-5 services per suburb", not block_bad, "; ".join(block_bad[:6]))
    assert_("spec section 5.4 paragraphs are 40-70 words", not para_bad, "; ".join(para_bad[:6]))
    paras = [H.unescape(p) for u in spec_subs for p in re.findall(r'<article class="suburb-service"><h3>.*?</h3><p>(.*?)</p>', pages[u]["src"], re.S)]
    assert_("spec section 5.4 paragraphs are unique sitewide",
            len(paras) == len(set(paras)), f"{len(paras) - len(set(paras))} duplicates")
    anchors = re.findall(r'<a class="area-pill" href="[^"]+"><span>([^<]+)</span>', pages["/areas/"]["src"])
    exact = sum(1 for a in anchors if a.startswith("Concreters in "))
    assert_("spec section 5.3 /areas/ anchor text is varied",
            anchors and 0.4 <= exact / len(anchors) <= 0.8, f"{exact}/{len(anchors)} exact-match")

    # ---------------------------------------------------------------- reachability
    reachable = {"/"}
    frontier = {"/"}
    for _ in range(2):
        nxt = set()
        for url in frontier:
            for href in {h.split("#", 1)[0].split("?", 1)[0] for h in re.findall(r'href="(/[^"]*)"', pages[url]["src"])}:
                if href in pages and href not in reachable:
                    reachable.add(href)
                    nxt.add(href)
        frontier = nxt
    unreachable = sorted(set(pages) - reachable)
    assert_("every page is reachable within 2 clicks of /", not unreachable, "; ".join(unreachable))

    # ---------------------------------------------------------- internal links
    # Every internal href must resolve to a file that exists in the build. A link to a
    # redirect source is a needless hop and is reported separately from a dead link.
    def resolves(href: str) -> bool:
        if href == "/":
            return (OUT / "index.html").is_file()
        clean = href.lstrip("/")
        return (OUT / clean / "index.html").is_file() or (OUT / clean).is_file()

    dead: list[str] = []
    via_redirect: list[str] = []
    bad_fragment: list[str] = []
    external: set[str] = set()
    for url, page in pages.items():
        for raw in sorted(set(re.findall(r'href="([^"]+)"', page["src"]))):
            if raw.startswith(("mailto:", "tel:", "#")):
                continue
            if raw.startswith(("http://", "https://", "//")):
                external.add(raw)
                continue
            path, _, fragment = raw.partition("#")
            path = path.split("?", 1)[0]
            if not path.startswith("/"):
                dead.append(f"{url} -> {raw} (not absolute)")
                continue
            if not resolves(path):
                (via_redirect if path in targets else dead).append(f"{url} -> {raw}")
                continue
            if fragment and path in pages and f'id="{fragment}"' not in pages[path]["src"]:
                bad_fragment.append(f"{url} -> {raw}")
    assert_("every internal link resolves to a file in the build", not dead, "; ".join(dead[:8]))
    assert_("no internal link points at a redirect source", not via_redirect, "; ".join(via_redirect[:8]))
    assert_("every internal fragment link has a matching id", not bad_fragment, "; ".join(bad_fragment[:8]))
    unbuilt_linked = [s for s in seo_spec.UNBUILT_SERVICES
                      if any(f'href="/services/{s}/"' in p["src"] for p in pages.values())]
    assert_("no link points at an unbuilt service page", not unbuilt_linked, "; ".join(unbuilt_linked))
    dead_redirect_targets = sorted({d for d in targets.values() if not resolves(d)})
    assert_("every redirect target resolves to a file in the build",
            not dead_redirect_targets, "; ".join(dead_redirect_targets))
    sitemap_dead = sorted(u for u in locs if not resolves(u.replace(BASE, "")))
    assert_("every sitemap URL resolves to a file in the build", not sitemap_dead, "; ".join(sitemap_dead))
    if external:
        RESULTS.append(("external links present (not fetched)", "PASS", "; ".join(sorted(external))))

    # ------------------------------------------------------ placeholder tokens
    tokens: list[str] = []
    for url, page in pages.items():
        found = re.findall(r"\[\[[^\]]{1,80}\]\]", page["src"])
        found += [m for m in re.findall(r"\{[A-Z_]{3,40}\}", page["src"])]
        if found:
            tokens.append(f"{url}: {sorted(set(found))[:3]}")
    assert_("no [[...]] or {TOKEN} placeholder reaches the output", not tokens, "; ".join(tokens[:6]))

    # ------------------------------------------------------------ JSON-LD sanity
    ids = {n["@id"] for p in pages.values() for b in p["ld"] for n in b.get("@graph", [b]) if n.get("@id")}
    refs: list[str] = []
    for url, page in pages.items():
        for blob in page["ld"]:
            for node in blob.get("@graph", [blob]):
                for value in node.values():
                    if isinstance(value, dict) and set(value) == {"@id"} and value["@id"] not in ids:
                        refs.append(f"{url} -> {value['@id']}")
    assert_("every referenced JSON-LD @id is defined", not refs, "; ".join(refs[:6]))

    # ------------------------------------------------- decisions and blockers
    # DECISION-10 D42-R2 clause 4. The assertion stays active but is inverted: every
    # phone-shaped string in every deployable file must equal the attested number.
    mismatched: list[str] = []
    for path in sorted(OUT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".txt", ".json", ".css", ".js"}:
            continue
        hits = seo_spec.scan_phone_mismatches(path.read_text(encoding="utf-8"))
        if hits:
            mismatched.append(f"{path.relative_to(OUT)}: {sorted(set(hits))}")
    assert_("every phone string in output matches verified-facts.yml exactly",
            not mismatched, "; ".join(mismatched[:6]))
    assert_("area_code_override recorded and dated (D42-R2)",
            seo_spec.area_code_override()
            and bool(seo_spec._contact["area_code_override"].get("reviewed")),
            f"reviewed {seo_spec._contact['area_code_override'].get('reviewed')}")
    assert_("telephone resolves from verified-facts.yml only, zero hardcodes",
            seo_spec.phone_display() in pages["/contact/"]["src"]
            and seo_spec.phone_uri() in pages["/contact/"]["src"],
            "contact.phone_display / contact.phone_e164 are the single source")
    schema_phone = [u for u, p in pages.items()
                    if any("telephone" in n for b in p["ld"] for n in b.get("@graph", [b]))]
    assert_("no telephone property in any schema node", not schema_phone, "; ".join(schema_phone))
    blocked("sitewide Organization node (spec section 7.2)",
            "DECISION-08 D35 clause 4 does not authorise an Organization node; "
            "legal_entity.legal_name is unverified. Service + WebPage + BreadcrumbList "
            "+ FAQPage ship instead. No @id is referenced, so nothing dangles.")
    blocked("spec section 5.2 price FAQ and '{X} business days'",
            "pricing.per_m2_ranges verified:false, blocks_pages:53. No response-time "
            "commitment recorded. Both withheld with an inline marker in every page.")
    retired("Tier 2 and Tier 3 noindex cannot be lifted",
            "DECISION-10 D45. The owner instructed that every built page ships indexed "
            "without per-m2 pricing or original photography, superseding the spec "
            "section 4 gate condition. pricing.per_m2_ranges and "
            "photography.real_camden_photographs remain verified:false; the gate code is "
            "retained and re-arms via seo_spec.INDEX_ALL_SUBURBS = False.")
    blocked("spec section 3 /services/stencilled-and-stamped-concrete/",
            "Resolved by removal, not by padding: no source page exists in "
            "build/46-active-main-import.xml, nothing in the build links to it, and the "
            "services hub records it in an HTML comment rather than an anchor. 10 of the "
            "spec's 11 service pages ship. Reopens when source content exists.")
    bringelly = seo_spec.COUNCIL["bringelly"]
    assert_("Bringelly council resolved against evidence",
            bringelly["assignment_status"] == "split-locality" and bringelly["lot_level_check_required"],
            "resolved as split-locality per build/53-council-suburb-map.json: Camden Council "
            "and Liverpool City Council, lot-level check required. The page names no single "
            "council, per its public_wording_rule. The spec's 'resolve to one council' is "
            "unsatisfiable because the locality genuinely straddles the boundary.")
    fallback = sorted(u for u in suburbs if u.removeprefix("/concreters-").rstrip("/") not in seo_spec.SUBURB_SPEC)
    blocked("fallback-tier suburb pages carry no suburbs.json record",
            f"{len(fallback)} pages ship indexed under D45 on the documented fallback "
            "tier: pattern title, generic-but-true meta, H1, breadcrumbs and a Service "
            "node. They carry no near-me FAQ and no section 5.4 block, because both need "
            "per-suburb job data that does not exist. Nothing is fabricated to fill them.")

    width = max(len(n) for n, _, _ in RESULTS)
    for name, verdict, detail in RESULTS:
        print(f"{verdict:8} {name.ljust(width)}  {detail}".rstrip())
    fails = [r for r in RESULTS if r[1] == "FAIL"]
    counts = Counter(v for _, v, _ in RESULTS)
    print()
    print(f"{counts['PASS']} pass, {counts['FAIL']} fail, {counts['BLOCKED']} blocked, {counts['RETIRED']} retired")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
