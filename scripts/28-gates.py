#!/usr/bin/env python3
"""Stage 28 — analytical preflight gates. Emits JSON on stdout.

Driven by scripts/28-preflight.sh. Every gate is fail-closed. A gate that
cannot be evaluated at full fidelity returns FAIL, never a warning.
"""
from __future__ import annotations

import html
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
MAIN = ROOT / "camden-concreting-import.xml"
SUPP = ROOT / "camden-calculator-import.xml"
SOURCE = ROOT / "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml"

BLOCKLIST = ["Melbourne", "Werribee", "Wyndham", "Point Cook", "Tarneit", "Truganina",
             "Hoppers Crossing", "Riverwalk", "Harpley", "Victoria", "VIC",
             "03 4427 9541", "bestconcretersmelbourne.com.au"]

CONTENT_KEYS = {
    "editor", "title", "title_text", "heading_title", "description_text", "text", "html",
    "testimonial_content", "testimonial_name", "testimonial_job", "item_description",
    "tab_content", "tab_title", "content", "caption", "before_text", "highlighted_text",
    "after_text", "inner_text", "list_item_text", "accordion_content", "toggle_content",
}

gates: list[dict] = []


def g(name: str, ok: bool, detail: str) -> None:
    gates.append({"name": name, "result": "PASS" if ok else "FAIL", "detail": detail})


def unesc(s: str) -> str:
    prev = None
    while prev != s:
        prev = s
        s = html.unescape(s)
    return s


def load(path: Path):
    tree = ET.parse(str(path))
    return tree.getroot().findall("./channel/item")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")

    items = load(MAIN)
    raw_main = MAIN.read_text(encoding="utf-8", errors="strict")
    pages, attach, occupied = {}, set(), set()
    for it in items:
        pt = (it.findtext(WP + "post_type") or "").strip()
        pid = int((it.findtext(WP + "post_id") or "0").strip())
        occupied.add(pid)
        if pt == "attachment":
            attach.add(pid)
        if pt != "page":
            continue
        texts = []
        pc = it.findtext(CONTENT + "encoded") or ""
        if pc.strip():
            texts.append(pc)
        elem = ""
        for pm in it.findall(WP + "postmeta"):
            if (pm.findtext(WP + "meta_key") or "").strip() == "_elementor_data":
                elem = pm.findtext(WP + "meta_value") or ""
                try:
                    parsed = json.loads(elem)
                except json.JSONDecodeError:
                    parsed = None
                if parsed is not None:
                    def walk(n, key=None):
                        if isinstance(n, dict):
                            for k, v in n.items():
                                walk(v, k)
                        elif isinstance(n, list):
                            for v in n:
                                walk(v, key)
                        elif isinstance(n, str) and key in CONTENT_KEYS:
                            texts.append(n)
                    walk(parsed)
        pages[pid] = {
            "slug": (it.findtext(WP + "post_name") or "").strip(),
            "status": (it.findtext(WP + "status") or "").strip(),
            "elem": elem,
            "body": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unesc("\n".join(texts)))).strip(),
        }

    # ---- 2. the 15 Stage 9 gates (structural re-verification) ----------------
    manifest = json.loads((ROOT / "build/stage9-page-manifest.json").read_text(
        encoding="utf-8", errors="strict"))
    mani = {int(r["post_id"]): r for r in manifest}
    s9 = []
    s9.append(("XML well-formed", True))
    s9.append(("156 pages", len(pages) == 156))
    s9.append(("83 attachments", len(attach) == 83))
    s9.append(("manifest/XML id parity", set(mani) == set(pages)))
    s9.append(("slug parity", all(mani[i]["post_name"] == pages[i]["slug"] for i in pages)))
    s9.append(("status parity", all(mani[i]["status"] == pages[i]["status"] for i in pages)))
    s9.append(("21 publish / 135 draft",
               Counter(p["status"] for p in pages.values()) == {"publish": 21, "draft": 135}))
    ejson_ok = True
    for pid, p in pages.items():
        if p["elem"]:
            try:
                json.loads(p["elem"])
            except json.JSONDecodeError:
                ejson_ok = False
    s9.append(("Elementor JSON valid on every page", ejson_ok))
    h1 = {pid: len(re.findall(r"<h1[\s>]", p["elem"], re.I)) for pid, p in pages.items()}
    s9.append(("no page declares multiple H1 in Elementor data",
               all(v <= 1 for v in h1.values())))
    s9.append(("every page has a slug", all(p["slug"] for p in pages.values())))
    s9.append(("no duplicate slugs",
               len({p["slug"] for p in pages.values()}) == len(pages)))
    s9.append(("all parents resolve",
               all((int(mani[i]["post_parent"]) in pages or int(mani[i]["post_parent"]) == 0)
                   for i in pages)))
    s9.append(("no forbidden Camden suburb URL",
               not any(p["slug"] in ("concreters-camden", "concreters-camden-town")
                       for p in pages.values())))
    s9.append(("35 intersections", sum(1 for i in pages if mani[i]["page_type"] == "intersection") == 35))
    s9.append(("60 suburbs", sum(1 for i in pages if mani[i]["page_type"] == "suburb") == 60))
    failed9 = [n for n, ok in s9 if not ok]
    g("2. 15 Stage 9 gates", not failed9,
      f"{len(s9)-len(failed9)}/{len(s9)} pass" + (f"; failing: {', '.join(failed9)}" if failed9 else ""))

    # ---- 3. occupied post-ID collision audit across every PRESENT WXR --------
    # The calculator is deliberately unbuilt and must remain absent. Privacy is
    # a real WXR and was previously omitted from this collision audit.
    privacy = ROOT / "camden-privacy-import.xml"
    collision_sets = {"main": occupied}
    missing_required = []
    if privacy.exists():
        collision_sets["privacy"] = {
            int((it.findtext(WP + "post_id") or "0").strip()) for it in load(privacy)
        }
    else:
        missing_required.append("privacy")
    unexpected = []
    if SUPP.exists():
        collision_sets["calculator"] = {
            int((it.findtext(WP + "post_id") or "0").strip()) for it in load(SUPP)
        }
        unexpected.append("calculator exists before it is built/approved")
    collisions = []
    labels = list(collision_sets)
    for index, left in enumerate(labels):
        for right in labels[index + 1:]:
            overlap = collision_sets[left] & collision_sets[right]
            if overlap:
                collisions.append(f"{left}/{right}={sorted(overlap)}")
    ok3 = not collisions and not missing_required and not unexpected
    detail3 = "; ".join(f"{label}={len(ids)} IDs" for label, ids in collision_sets.items())
    detail3 += f"; collisions={collisions or 0}; calculator=absent (required until built)"
    if missing_required:
        detail3 += f"; missing required={missing_required}"
    if unexpected:
        detail3 += f"; unexpected={unexpected}"
    g("3. post-ID collision audit (present WXRs)", ok3, detail3)

    # ---- 6. Elementor image-reference count ---------------------------------
    img_refs = bg_refs = 0
    ref_ids = set()
    unresolved = 0
    for pid, p in pages.items():
        if not p["elem"]:
            continue
        try:
            parsed = json.loads(p["elem"])
        except json.JSONDecodeError:
            continue

        def walk(n, key=None):
            nonlocal img_refs, bg_refs, unresolved
            if isinstance(n, dict):
                if isinstance(n.get("id"), int) and isinstance(n.get("url"), str) \
                        and "wp-content/uploads" in n["url"]:
                    if key == "image":
                        img_refs += 1
                    else:
                        bg_refs += 1
                    ref_ids.add(n["id"])
                    if n["id"] not in attach:
                        unresolved += 1
                for k, v in n.items():
                    walk(v, k)
            elif isinstance(n, list):
                for v in n:
                    walk(v, key)

        walk(parsed)
    expected_img = 1085
    ok6 = (img_refs == expected_img and unresolved == 0)
    g("6. Elementor image-reference count", ok6,
      f"image={img_refs} (expected {expected_img}), background_image={bg_refs} "
      f"(NOT covered by the recorded figure), total={img_refs+bg_refs}, "
      f"distinct attachment ids referenced={len(ref_ids & attach)} of {len(attach)}, "
      f"unresolved refs={unresolved}")

    # ---- 7. uniqueness gates -------------------------------------------------
    words = {pid: re.findall(r"[a-z0-9']+", p["body"].lower()) for pid, p in pages.items()}
    shing = {pid: {tuple(w[i:i+5]) for i in range(len(w)-4)} for pid, w in words.items()}
    owner: Counter = Counter()
    for s in shing.values():
        for sh in s:
            owner[sh] += 1
    over = sum(1 for c in owner.values() if c > 2)
    bycls = defaultdict(list)
    for pid in pages:
        bycls[mani[pid]["page_type"]].append(pid)
    pairfail = 0
    for cls, ids in bycls.items():
        for a, b in combinations(ids, 2):
            sa, sb = shing[a], shing[b]
            if sa and sb and len(sa & sb)/min(len(sa), len(sb)) > 0.40:
                pairfail += 1
    g("7. uniqueness gates", over == 0 and pairfail == 0,
      f"5-grams on >2 pages={over}; within-class pairs over 40% overlap={pairfail}")

    # ---- 8. intersection audit ----------------------------------------------
    inter = json.loads((ROOT / "intersection-differentiators.json").read_text(
        encoding="utf-8", errors="strict"))
    ilist = inter["intersections"] if isinstance(inter, dict) else inter
    allowed = {(r.get("url") or "").strip("/").split("/")[-1] for r in ilist}
    built = {pages[i]["slug"] for i in pages if mani[i]["page_type"] == "intersection"}
    all_draft = all(pages[i]["status"] == "draft" for i in pages
                    if mani[i]["page_type"] == "intersection")
    ok8 = built == allowed and len(built) == 35 and all_draft
    g("8. intersection audit", ok8,
      f"built={len(built)}, allow-listed={len(allowed)}, extras={len(built-allowed)}, "
      f"missing={len(allowed-built)}, all draft={all_draft}")

    # ---- 10. Victorian blocklist scan, EVERY importable artifact -------------
    #
    # Previously this scanned the main WXR and the supplementary WXR only. That
    # left a structural gap: the Astra Customizer export imports into the same
    # database and was never scanned. It carried "/* Local Werribee project
    # cards */" in wp_css -- the only importable Werribee string in the build --
    # and no gate would have seen it.
    #
    # The rule is now: if an artifact imports, it is scanned. An artifact that
    # imports but is not scanned is exactly how the next one gets through.
    IMPORTABLE = [
        ("main WXR", MAIN),
        ("supplementary WXR", SUPP),
        ("privacy WXR", ROOT / "camden-privacy-import.xml"),
        ("Astra export", ROOT / "source-inputs" / "astra" / "astra-export.dat"),
    ]
    per_artifact: list[str] = []
    blocklist_total = 0
    unscanned: list[str] = []
    for label, path in IMPORTABLE:
        if not path.exists():
            per_artifact.append(f"{label}=absent")
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError) as exc:
            # Fail closed: an artifact that cannot be read cannot be cleared.
            unscanned.append(f"{label}: unreadable ({exc.__class__.__name__})")
            per_artifact.append(f"{label}=UNSCANNED")
            continue
        # Scan what will actually be imported. Declared exclusions
        # (build/22-astra-import-exclusions.json) are removed from the payload
        # first: the supplied file stays byte-identical on disk, and a gate that
        # failed on a string which is never imported would assert nothing.
        excluded_note = ""
        if label == "Astra export":
            excl_path = ROOT / "build" / "22-astra-import-exclusions.json"
            if excl_path.exists():
                excl = json.loads(excl_path.read_text(encoding="utf-8", errors="strict"))
                if excl.get("source_sha256", "").upper() != hashlib.sha256(
                        path.read_bytes()).hexdigest().upper():
                    # Fail closed: exclusions were written against a different file.
                    unscanned.append(f"{label}: exclusion manifest sha256 mismatch")
                    per_artifact.append(f"{label}=UNSCANNED")
                    continue
                for k in (e["key"] for e in excl.get("excluded_keys", [])):
                    if k == "wp_css":
                        raw = re.sub(r's:6:"wp_css";s:\d+:".*?";(?=\}?$|s:)', "", raw, flags=re.S)
                        excluded_note = " (wp_css excluded at import)"
        c = sum(raw.count(b) for b in BLOCKLIST)
        blocklist_total += c
        per_artifact.append(f"{label}={c}{excluded_note}")
    g("10. Victorian blocklist scan", blocklist_total == 0 and not unscanned,
      f"{'; '.join(per_artifact)}; terms={len(BLOCKLIST)}"
      + (f"; UNSCANNED={unscanned}" if unscanned else ""))

    # ---- 11. placeholder-in-schema scan -------------------------------------
    schema_blobs = []
    for pid, p in pages.items():
        for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>',
                             p["elem"], re.S | re.I):
            schema_blobs.append((pid, m.group(1)))
    bad = [(pid, t) for pid, t in schema_blobs
           if any(k in t for k in ("PLACEHOLDER", "REAL_PHOTO_PENDING", "REQUIRED-RESEARCH"))]
    g("11. placeholder-in-schema scan", not bad,
      f"JSON-LD blocks found in Elementor data={len(schema_blobs)}; "
      f"containing a placeholder token={len(bad)}")

    # ---- 13. source business name (DECISION-06 D30.2) ---------------------
    # Scans artifacts destined for the SITE. Provenance and audit records are out
    # of scope: a rename map is supposed to record the original filename.
    SRC_NAME = re.compile(r"E&(?:amp;)*T\s*Co|e_t_co|eandtco|E&(?:amp;)*T", re.I)
    kit_hits, body_hits, ident_hits = 0, 0, []
    for it in items:
        pt = (it.findtext(WP + "post_type") or "").strip()
        if pt == "elementor_library":
            for pm in it.findall(WP + "postmeta"):
                v = pm.findtext(WP + "meta_value") or ""
                kit_hits += len(SRC_NAME.findall(v))
                for key in ("site_name", "site_description"):
                    m = re.search(rf's:\d+:"{key}";s:\d+:"([^"]*)"', v)
                    if m and SRC_NAME.search(m.group(1)):
                        ident_hits.append(f"{key}={m.group(1)!r}")
    for pid, p_ in pages.items():
        body_hits += len(SRC_NAME.findall(p_["body"]))
    supp_hits = 0
    if SUPP.exists():
        supp_hits = len(SRC_NAME.findall(SUPP.read_text(encoding="utf-8", errors="strict")))
    g("13. source business name", kit_hits == 0 and body_hits == 0 and supp_hits == 0,
      f"kit settings={kit_hits}, page bodies={body_hits}, supplementary={supp_hits}; "
      f"identity fields={ident_hits or 'clean'}")

    # ---- 14. menu targets in assigned locations ------------------------------
    #
    # No menu item in an ASSIGNED theme location may resolve to a page that is
    # withdrawn, draft, or held noindex.
    #
    # All THREE conditions are tested deliberately. Footer Areas is the reason:
    # it carries zero withdrawn and zero draft targets, and is still unsafe
    # because all six are Tier 1 suburb pages held noindex,follow. A two-condition
    # test would have passed it.
    assign_path = ROOT / "build" / "22-menu-assignment.json"
    ASSIGNED_LOCATIONS = {}
    retained_ids: dict[str, set[str]] = {}
    if assign_path.exists():
        _a = json.loads(assign_path.read_text(encoding="utf-8", errors="strict"))
        for loc, v in _a.get("locations", {}).items():
            ASSIGNED_LOCATIONS[loc] = v["menu"]
        for menu_name, its in _a.get("retained_items", {}).items():
            retained_ids[menu_name] = {str(i.get("object_id")) for i in its}
    else:
        ASSIGNED_LOCATIONS = {"primary": "primary", "mobile_menu": "primary-2",
                              "footer_menu": "footer-services"}
    wave1 = ROOT / "build" / "27-wave1-menus.json"
    readiness = ROOT / "reports" / "23-page-readiness-v2.csv"

    menu_detail: list[str] = []
    menu_bad: list[str] = []
    if not wave1.exists() or not readiness.exists():
        # Fail closed: without both inputs the assertion cannot run at full fidelity.
        g("14. menu targets in assigned locations", False,
          f"cannot evaluate: 27-wave1-menus.json exists={wave1.exists()}, "
          f"23-page-readiness-v2.csv exists={readiness.exists()}")
    else:
        import csv as _csv
        # Three PRECISE per-page signals. The two robots columns in the readiness
        # CSV are uniform across all 157 rows -- "global staging:
        # noindex,nofollow,noarchive" and "noindex,follow" -- because nothing is
        # index-ready yet. Matching on those flags every page and asserts nothing.
        #
        #   withdrawn     readiness column "Withdrawn" == YES
        #   draft         the WXR's own wp:status
        #   noindex-held  the Tier 1 photography/evidence hold, whose authoritative
        #                 list is the "is held noindex,follow" reasons already
        #                 computed in build/27-wave1-menus.json
        withdrawn: set[str] = set()
        with readiness.open(encoding="utf-8-sig", errors="strict", newline="") as fh:
            for row in _csv.DictReader(fh):
                slug = (row.get("Slug") or "").strip().strip("/")
                if slug and (row.get("Withdrawn") or "").strip().upper() == "YES":
                    withdrawn.add(slug)

        w1 = json.loads(wave1.read_text(encoding="utf-8", errors="strict"))
        held: set[str] = set()
        for it_ in w1.get("removed_items", []):
            m = re.search(r"target /([^/]*(?:/[^/]*)*)/ is held noindex", it_.get("reason", ""))
            if m:
                held.add(m.group(1).strip("/").split("/")[-1])
        if not held:
            # Fail closed: the hold list must be derivable, or the third condition
            # is silently not being tested at all.
            g("14. menu targets in assigned locations", False,
              "cannot derive the noindex-held set from build/27-wave1-menus.json; "
              "the third condition would go untested")
            menu_detail = None

        if menu_detail is not None:
            for loc, menu_slug in ASSIGNED_LOCATIONS.items():
                offenders = []
                for it in items:
                    if (it.findtext(WP + "post_type") or "").strip() != "nav_menu_item":
                        continue
                    cats = [c.get("nicename") for c in it.findall("category")
                            if c.get("domain") == "nav_menu"]
                    if menu_slug not in cats:
                        continue
                    obj = objid = None
                    for pm in it.findall(WP + "postmeta"):
                        k = (pm.findtext(WP + "meta_key") or "").strip()
                        if k == "_menu_item_object":
                            obj = (pm.findtext(WP + "meta_value") or "").strip()
                        elif k == "_menu_item_object_id":
                            objid = (pm.findtext(WP + "meta_value") or "").strip()
                    if obj != "page" or not objid:
                        continue
                    # Only items the prune RETAINS are actually assigned. An item
                    # the prune removes never reaches a live menu, so judging the
                    # raw WXR menu would fail a correctly-pruned assignment.
                    menu_name = {"primary": "Primary", "primary-2": "Primary (2)",
                                 "footer-services": "Footer Services",
                                 "footer-areas": "Footer Areas",
                                 "footer-blogs": "Footer Blogs"}.get(menu_slug)
                    if retained_ids and menu_name in retained_ids:
                        if objid not in retained_ids[menu_name]:
                            continue
                    p = pages.get(int(objid))
                    if p is None:
                        offenders.append(f"{objid}:target-missing")
                        continue
                    slug = p.get("slug", "")
                    why = []
                    if slug in withdrawn:
                        why.append("withdrawn")
                    if p.get("status") == "draft":
                        why.append("draft")
                    if slug in held:
                        why.append("noindex-held")
                    if why:
                        offenders.append(f"{slug}({'+'.join(why)})")
                menu_detail.append(f"{loc}->{menu_slug}: {len(offenders)} unsafe")
                if offenders:
                    menu_bad.append(f"{loc}->{menu_slug}: " + ", ".join(sorted(offenders)[:6]))
            g("14. menu targets in assigned locations", not menu_bad,
              "; ".join(menu_detail) + (
                  "; OFFENDERS " + " | ".join(menu_bad) if menu_bad else "")
              + f"; held-set={len(held)}, withdrawn-set={len(withdrawn)}")

    json.dump({"gates": gates}, sys.stdout, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
