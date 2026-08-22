"""Build a static Cloudflare Pages export from the approved derivative WXR."""
from __future__ import annotations

import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "build" / "46-active-main-import.xml"
PRIVACY = ROOT / "build" / "51-privacy-import.xml"
OUT = ROOT / "build" / "cloudflare-pages"
MEDIA = ROOT / "source-inputs" / "media"
WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"

def clean(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<script[^>]*>.*?</script>", "", s, flags=re.I | re.S)
    s = re.sub(r"<style[^>]*>.*?</style>", "", s, flags=re.I | re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def body_for(item: ET.Element) -> str:
    encoded = clean(item.findtext(CONTENT + "encoded") or "")
    if encoded:
        return encoded
    for meta in item.findall(WP + "postmeta"):
        if (meta.findtext(WP + "meta_key") or "") == "_elementor_data":
            try:
                data = json.loads(meta.findtext(WP + "meta_value") or "[]")
            except json.JSONDecodeError:
                return ""
            chunks: list[str] = []
            def walk(v):
                if isinstance(v, dict):
                    for k, x in v.items():
                        if k in {"editor", "title", "title_text", "description_text", "text", "content"} and isinstance(x, str):
                            t = clean(x)
                            if t and not t.startswith("[fluentform"):
                                chunks.append(t)
                        else:
                            walk(x)
                elif isinstance(v, list):
                    for x in v: walk(x)
            walk(data)
            return " ".join(dict.fromkeys(chunks))
    return ""

def page_html(title: str, body: str, canonical: str) -> str:
    safe = html.escape(body)
    safe = re.sub(r"(https?://[^\s]+)", lambda m: html.escape(m.group(1)), safe)
    schema = json.dumps({"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical,"breadcrumb":{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://concreterscamden.com.au/"},{"@type":"ListItem","position":2,"name":title,"item":canonical}]}}, ensure_ascii=False)
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="Structure Co Concreters Camden enquiry coordination information."><meta name="robots" content="noindex,nofollow,noarchive"><link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{schema}</script></head><body><header><a href="/">Structure Co Concreters Camden</a><nav><a href="/">Home</a> <a href="/about/">About</a> <a href="/contact/">Contact</a> <a href="/privacy-policy/">Privacy</a></nav></header><main><p class="breadcrumbs"><a href="/">Home</a> / {html.escape(title)}</p><h1>{html.escape(title)}</h1><div class="content"><p>{safe}</p></div><aside><strong>Enquiries</strong><p>Submitting an enquiry does not create a construction contract. Email <a href="mailto:info@concreterscamden.com.au">info@concreterscamden.com.au</a> to begin coordination.</p></aside></main><footer>Structure Co Concreters Camden · (03) 4328 3392 · 15 Murray Street, Camden NSW 2570 (administrative office, not open to customers)</footer></body></html>'''

def main() -> int:
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "assets" / "media").mkdir(parents=True)
    for src in MEDIA.iterdir():
        if src.is_file(): shutil.copy2(src, OUT / "assets" / "media" / src.name)
    items = []
    for path in (SOURCE, PRIVACY):
        root = ET.parse(path).getroot()
        items.extend(i for i in root.findall("./channel/item") if (i.findtext(WP + "post_type") or "") == "page")
    seen = set(); rows = []
    for item in items:
        slug = (item.findtext(WP + "post_name") or "").strip()
        if not slug or slug in seen: continue
        seen.add(slug)
        title = (item.findtext("title") or slug.replace("-", " ").title()).strip()
        if slug in {"cost-comparison-calculator", "calculator"}: continue
        path = "/" if slug == "homepage" else f"/{slug}/"
        (OUT / path.strip("/")).mkdir(parents=True, exist_ok=True)
        (OUT / path.strip("/") / "index.html").write_text(page_html(title, body_for(item), "https://concreterscamden.com.au" + path), encoding="utf-8")
        rows.append((slug, path, title))
    # Privacy is in the approved privacy derivative and must be included.
    if not any(s in {"privacy", "privacy-policy"} for s, _, _ in rows):
        raise SystemExit("privacy page missing from approved derivatives")
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" + "".join(f"<url><loc>https://concreterscamden.com.au{p}</loc></url>" for _, p, _ in rows) + "</urlset>"
    (OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (OUT / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n", encoding="utf-8")
    (OUT / "404.html").write_text(page_html("Page not found", "The requested page could not be found.", "https://concreterscamden.com.au/404/"), encoding="utf-8")
    (OUT / "assets" / "site.css").write_text("body{font-family:system-ui,sans-serif;max-width: seventyrem;margin:auto;padding:1rem;line-height:1.6}header,footer{padding:1rem 0}nav a{margin-right:1rem}.content{max-width:70ch}aside{border:1px solid #ddd;padding:1rem;margin-top:2rem}", encoding="utf-8")
    (ROOT / "reports" / "56-cloudflare-pages-inventory.csv").write_text("slug,path,title\n" + "\n".join(f"{s},{p},{t.replace(',', ' ')}" for s,p,t in rows) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(rows), "media": len(list((OUT / 'assets' / 'media').iterdir())), "output": str(OUT)}, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
