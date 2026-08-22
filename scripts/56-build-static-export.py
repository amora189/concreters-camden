"""Build the approved Camden content as a polished static Cloudflare export."""
from __future__ import annotations

import csv
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
ALT_REGISTER = ROOT / "reports" / "24-image-distribution.csv"
MEDIA_REMEDIATION = ROOT / "build" / "47-media-remediation.csv"
WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
BASE = "https://concreterscamden.com.au"
BRAND = "Structure Co Concreters Camden"
EMAIL = "info@concreterscamden.com.au"
PHONE = "(03) 4328 3392"
PHONE_URI = "tel:+61343283392"
ADDRESS = "15 Murray Street, Camden NSW 2570"

SERVICES = {
    "concrete-driveways-south-west-sydney": ("Concrete Driveways", "Driveway enquiries shaped around access, existing surfaces, drainage and the intended use of the property.", "driveway"),
    "exposed-aggregate-south-west-sydney": ("Exposed Aggregate", "Explore a textured finish and the questions an appointed provider should confirm for the actual site.", "exposed"),
    "concrete-slabs-south-west-sydney": ("Concrete Slabs", "Coordinate an enquiry for shed, garage, extension or other slab requirements with the project-specific details in view.", "slab"),
    "concrete-paths-south-west-sydney": ("Concrete Paths", "Plan paths and side access with attention to levels, edges, access and the way the space will be used.", "path"),
    "concrete-patios-south-west-sydney": ("Concrete Patios", "Bring outdoor areas into focus with a clear brief for the surface, access and surrounding conditions.", "patio"),
    "decorative-concrete-south-west-sydney": ("Decorative Concrete", "Compare decorative directions while leaving product and finish requirements to the selected provider and supplier.", "coloured"),
    "concrete-driveway-replacement-south-west-sydney": ("Concrete Driveway Replacement", "Start with the existing driveway, access constraints and the questions that need answering before replacement.", "cracks"),
    "shed-and-garage-slabs-south-west-sydney": ("Shed and Garage Slabs", "A structured enquiry for slabs where design, site and selected-system requirements must be confirmed.", "garage"),
    "concrete-crossovers-and-laybacks-south-west-sydney": ("Concrete Crossovers and Laybacks", "Coordinate the council-facing questions for a vehicle crossing, layback or related frontage work.", "crossing"),
    "commercial-concreting-south-west-sydney": ("Commercial Concreting", "A clear starting point for commercial and industrial concreting enquiries across South-West Sydney.", "commercial"),
}

SERVICE_ORDER = list(SERVICES)
NAV_SERVICES = SERVICE_ORDER[:6]
SAFE_MEDIA = [
    "exposed-aggregate-concrete-50.jpg", "concrete-project-detail-17.jpg", "concrete-project-detail-18.jpg",
    "concrete-project-detail-19.jpg", "patiosandpathways-camden-53.webp", "patiosconcrete-camden-55.jpg",
    "concrete-slabs-1065.jpg", "reinforcedheavydutyconcrete-camden-121.webp", "concrete-vehicle-crossing-1153.jpg",
    "accessible-paths-concrete-184.jpg", "coloured-detailed-concrete-54.jpg", "commercial-building-concrete-hardstand-1186.webp",
    "front-and-entry-paths-concrete-183.jpg", "garage-slabs-concrete-167.jpg", "fresh-concrete-backyard-slab-47.webp",
    "control-joints-and-cracks-909.jpg", "structural-cracks-1233.jpg", "aerial-new-housing-estate-908.jpg",
]
KEY_IMAGES = {
    "driveway": "concrete-project-detail-17.jpg", "exposed": "exposed-aggregate-concrete-50.jpg",
    "slab": "concrete-slabs-1065.jpg", "path": "accessible-paths-concrete-184.jpg",
    "patio": "patiosandpathways-camden-53.webp", "coloured": "coloured-detailed-concrete-54.jpg",
    "cracks": "control-joints-and-cracks-909.jpg", "garage": "garage-slabs-concrete-167.jpg",
    "crossing": "concrete-vehicle-crossing-1153.jpg", "commercial": "commercial-building-concrete-hardstand-1186.webp",
    "aerial": "aerial-new-housing-estate-908.jpg", "project": "concrete-project-detail-18.jpg",
}


def clean(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<script[^>]*>.*?</script>", "", value, flags=re.I | re.S)
    value = re.sub(r"<style[^>]*>.*?</style>", "", value, flags=re.I | re.S)
    value = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()
    return value


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

            def walk(value):
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key in {"editor", "title", "title_text", "description_text", "text", "content"} and isinstance(child, str):
                            text = clean(child)
                            if text and not text.startswith("[fluentform"):
                                chunks.append(text)
                        else:
                            walk(child)
                elif isinstance(value, list):
                    for child in value:
                        walk(child)

            walk(data)
            return " ".join(dict.fromkeys(chunks))
    return ""


def load_alt_register() -> dict[str, str]:
    result: dict[str, str] = {}
    if MEDIA_REMEDIATION.exists():
        with MEDIA_REMEDIATION.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                filename = (row.get("target_filename") or "").strip()
                alt = (row.get("target_alt") or "").strip()
                if filename and alt:
                    result[filename] = alt
    if ALT_REGISTER.exists():
        with ALT_REGISTER.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                filename = (row.get("filename") or "").strip()
                alt = (row.get("attachment_alt") or "").strip()
                if filename and alt:
                    result[filename] = alt
    return result


def title_for(slug: str, raw_title: str) -> str:
    if raw_title and raw_title.lower() not in {"homepage", "home"}:
        return raw_title.strip()
    return slug.replace("-", " ").title()


def pretty_area(slug: str) -> str:
    return slug.removeprefix("concreters-").replace("-", " ").title()


def safe_excerpt(text: str, limit: int = 480) -> str:
    text = clean(text)
    # Keep approved factual copy useful while avoiding a false direct-contractor voice.
    text = re.sub(r"\bwe (pour|build|install|handle|provide)\b", "the appointed provider can \\1", text, flags=re.I)
    text = re.sub(r"\bfree (quote|consultation)\b", "enquiry", text, flags=re.I)
    return text[:limit].rstrip(" .,;:") + ("…" if len(text) > limit else "")


def image_for(key: str, media_names: list[str]) -> str:
    available = set(media_names)
    preferred = KEY_IMAGES.get(key)
    if preferred in available:
        return preferred
    for name in SAFE_MEDIA:
        if name in available and key in name:
            return name
    for name in SAFE_MEDIA:
        if name in available:
            return name
    return media_names[0]


def alt_for(filename: str, alt_register: dict[str, str]) -> str:
    if filename in alt_register:
        return alt_register[filename]
    stem = Path(filename).stem.replace("-", " ").replace("_", " ")
    return stem[:1].upper() + stem[1:]


def img(filename: str, alt_register: dict[str, str], eager: bool = False, class_name: str = "") -> str:
    loading = "eager"
    cls = f' class="{class_name}"' if class_name else ""
    return f'<img src="/assets/media/{html.escape(filename)}" alt="{html.escape(alt_for(filename, alt_register))}" loading="{loading}"{cls}>'


def link(href: str, label: str, class_name: str = "") -> str:
    cls = f' class="{class_name}"' if class_name else ""
    return f'<a href="{href}"{cls}>{html.escape(label)}</a>'


def breadcrumb(items: list[tuple[str, str]]) -> str:
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + " <span>/</span> ".join(link(url, label) for url, label in items) + "</nav>"


def page_head(title: str, description: str, canonical: str, alt_register: dict[str, str]) -> str:
    schema = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "name": title, "url": canonical,
        "description": description, "isPartOf": {"@type": "WebSite", "name": BRAND, "url": BASE + "/"},
    }, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)} | {BRAND}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)} | {BRAND}">
  <meta property="og:description" content="{html.escape(description)}"><meta property="og:url" content="{canonical}">
  <link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{schema}</script>
</head>'''


def header() -> str:
    service_links = "".join(link(f"/{slug}/", SERVICES[slug][0]) for slug in NAV_SERVICES)
    return f'''<header class="site-header">
  <div class="utility"><div class="container utility__inner"><span>Independent-provider enquiry coordination · Camden &amp; South-West Sydney</span><span class="utility__contact"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{PHONE_URI}">{PHONE}</a></span></div></div>
  <div class="container nav-wrap"><a class="brand" href="/"><span class="brand-mark">SC</span><span><strong>Structure Co</strong><small>Concreters Camden</small></span></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav">Menu <span>☰</span></button>
    <nav id="primary-nav" class="primary-nav" aria-label="Primary navigation"><a href="/">Home</a><div class="nav-dropdown"><button type="button" aria-expanded="false">Services <span>⌄</span></button><div class="nav-dropdown__menu">{service_links}</div></div><a href="/about/">About</a><a href="/gallery/">Gallery</a><a href="/contact/">Contact</a><a class="nav-cta" href="/quote/">Start an enquiry <span>↗</span></a></nav>
  </div>
</header>'''


def footer() -> str:
    service_links = "".join(f'<li>{link(f"/{slug}/", SERVICES[slug][0])}</li>' for slug in NAV_SERVICES)
    return f'''<footer class="site-footer"><div class="container footer-grid"><div><a class="brand brand--footer" href="/"><span class="brand-mark">SC</span><span><strong>Structure Co</strong><small>Concreters Camden</small></span></a><p class="footer-intro">A considered starting point for concreting enquiries in Camden and South-West Sydney, coordinated with suitable independent providers.</p></div><div><h2>Explore</h2><ul><li>{link("/about/", "About")}</li><li>{link("/gallery/", "Gallery")}</li><li>{link("/contact/", "Contact")}</li><li>{link("/privacy-policy/", "Privacy")}</li></ul></div><div><h2>Services</h2><ul>{service_links}</ul></div><div><h2>Enquiries</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{PHONE_URI}">{PHONE}</a></p><p class="footer-address">{ADDRESS}<br><small>Administrative office only; not open to customers.</small></p><a class="button button--small" href="/quote/">Tell us about your project</a></div></div><div class="container footer-bottom"><span>© <span data-year>2026</span> {BRAND}</span><span>Submitting an enquiry does not create a construction contract.</span></div></footer>'''


def document(title: str, description: str, canonical: str, content: str, alt_register: dict[str, str]) -> str:
    return page_head(title, description, canonical, alt_register) + header() + f'<main>{content}</main>' + footer() + '<script src="/assets/site.js" defer></script></body></html>'


def cta_band(heading: str = "Ready to shape the brief?") -> str:
    return f'''<section class="cta-band"><div><span class="eyebrow eyebrow--light">Start with the right questions</span><h2>{heading}</h2><p>Share the site, intended use and any access or timing questions. We will coordinate the next step with an independent provider where appropriate.</p></div><div class="cta-band__actions"><a class="button button--light" href="/quote/">Start an enquiry <span>↗</span></a><a class="text-link text-link--light" href="mailto:{EMAIL}">Email {EMAIL}</a></div></section>'''


def card_image(filename: str, alt_register: dict[str, str]) -> str:
    return f'<div class="card-image">{img(filename, alt_register)}</div>'


def service_cards(alt_register: dict[str, str], media_names: list[str], slugs: list[str] | None = None) -> str:
    slugs = slugs or SERVICE_ORDER
    cards = []
    for index, slug in enumerate(slugs):
        name, description, key = SERVICES[slug]
        filename = image_for(key, media_names)
        cards.append(f'''<article class="service-card">{card_image(filename, alt_register)}<div class="service-card__body"><span class="card-number">0{index + 1:02d}</span><h3>{link(f'/{slug}/', name)}</h3><p>{description}</p><a class="arrow-link" href="/{slug}/">Explore service <span>→</span></a></div></article>''')
    return "".join(cards)


def home_content(alt_register: dict[str, str], media_names: list[str], suburb_slugs: list[str]) -> str:
    hero_image = image_for("exposed", media_names)
    area_cards = []
    for slug in suburb_slugs[:12]:
        area = pretty_area(slug)
        area_cards.append(f'<a class="area-pill" href="/{slug}/"><span>{html.escape(area)}</span><span>↗</span></a>')
    return f'''<section class="hero hero--home"><div class="container hero-grid"><div class="hero-copy"><span class="eyebrow">Camden · South-West Sydney</span><h1>Concrete enquiries, <em>structured</em> around your site.</h1><p class="hero-lead">Structure Co Concreters Camden helps turn a rough idea into a clear, considered enquiry for driveways, slabs, paths and outdoor spaces.</p><div class="hero-actions"><a class="button" href="/quote/">Start an enquiry <span>↗</span></a><a class="button button--ghost" href="{PHONE_URI}">Call {PHONE}</a></div><p class="micro-note">Independent-provider coordination. An enquiry is not a construction contract.</p></div><div class="hero-media"><div class="hero-media__frame">{img(hero_image, alt_register, True)}</div><div class="hero-stamp"><strong>01</strong><span>Local context<br>matters</span></div></div></div></section>
<section class="trust-strip"><div class="container trust-grid"><div><strong>01</strong><span>Start with a clear brief</span></div><div><strong>02</strong><span>Understand the site questions</span></div><div><strong>03</strong><span>Coordinate the next step</span></div></div></section>
<section class="section section--services"><div class="container"><div class="section-heading"><div><span class="eyebrow">What can we help coordinate?</span><h2>Services for the way Camden lives.</h2></div><p>Explore the main service pathways and the information an appointed provider should confirm before work begins.</p></div><div class="service-grid">{service_cards(alt_register, media_names, SERVICE_ORDER)}</div></div></section>
<section class="section section--tint"><div class="container split-grid"><div class="split-media">{img(image_for("aerial", media_names), alt_register)}<span class="image-caption">Camden and the South-West Sydney growth corridor</span></div><div class="split-copy"><span class="eyebrow">A local starting point</span><h2>Good concrete decisions begin before the concrete.</h2><p>Access, existing surfaces, levels, drainage, intended use and council interfaces can all change the questions a project needs to answer. A useful enquiry puts those details on the table early.</p><p>We coordinate enquiries with suitable independent providers. The appointed provider and project designer confirm the applicable requirements for the actual property, system and conditions.</p><a class="arrow-link" href="/about/">How the model works <span>→</span></a></div></div></section>
<section class="section"><div class="container"><div class="section-heading section-heading--center"><span class="eyebrow">The enquiry path</span><h2>Simple on the surface. Thoughtful underneath.</h2><p>Three useful steps keep the conversation focused without promising a construction outcome.</p></div><div class="process-grid"><article class="process-step"><span>01</span><h3>Tell us about the site</h3><p>Share the property location, intended use, existing surface, access constraints, drainage concerns and timing.</p></article><article class="process-step"><span>02</span><h3>Clarify the questions</h3><p>We help frame the information an appointed provider needs to assess the actual site and proposed scope.</p></article><article class="process-step"><span>03</span><h3>Coordinate the next step</h3><p>Provider identity, quotation, contract, licensing, insurance and warranty details are confirmed before work begins.</p></article></div></div></section>
<section class="section section--dark"><div class="container council-grid"><div><span class="eyebrow eyebrow--light">Council context</span><h2>Frontage work needs the right local check.</h2><p>For properties in Liverpool City Council, a vehicle crossing application is made under section 138 of the Roads Act 1993. Current forms, inspections, drawings, utilities and fees should be checked with Council for the actual property.</p><p>That information is a coordination reference, not evidence that Structure Co is licensed or insured.</p></div><div class="council-card"><span class="council-card__icon">◎</span><h3>Own a Liverpool property?</h3><p>Bring the crossing location and any current Council correspondence to the enquiry.</p><a class="text-link text-link--light" href="/concrete-crossovers-and-laybacks-south-west-sydney/">Explore crossovers &amp; laybacks <span>→</span></a></div></div></section>
<section class="section section--areas"><div class="container"><div class="section-heading"><div><span class="eyebrow">Service areas</span><h2>Camden at the centre.</h2></div><p>Browse the existing area pages for local context. Property boundaries and council requirements should always be confirmed for the actual address.</p></div><div class="area-grid">{''.join(area_cards)}</div></div></section>
<section class="section section--faq"><div class="container faq-grid"><div><span class="eyebrow">Questions, answered carefully</span><h2>Before you send an enquiry.</h2><p>These answers describe the coordination model and the information worth having ready.</p><a class="arrow-link" href="/contact/">Ask a question <span>→</span></a></div><div class="faq-list">{faq_items([('What happens after I enquire?', 'We review the project information and coordinate the next conversation where an independent provider is suitable. An enquiry does not create a construction contract.'), ('Do you publish prices?', 'No universal price is asserted. Scope, access, existing conditions, finish and project requirements need to be confirmed for the actual site.'), ('What should I include?', 'The property location, intended use, approximate dimensions, access constraints, existing surfaces, drainage concerns and timing are useful starting points.'), ('Can I visit the address?', 'No. {ADDRESS} is an administrative correspondence office and is not open to customers or visitors.')])}</div></div></section>
{cta_band()}'''


def faq_items(items: list[tuple[str, str]]) -> str:
    return "".join(f'<details class="faq-item"><summary>{html.escape(question)}</summary><p>{answer}</p></details>' for question, answer in items)


def service_content(slug: str, title: str, description: str, key: str, alt_register: dict[str, str], media_names: list[str], suburb_slugs: list[str]) -> str:
    filename = image_for(key, media_names)
    related = SERVICE_ORDER[:5] if slug not in SERVICE_ORDER[:5] else [s for s in SERVICE_ORDER if s != slug][:5]
    area_links = " · ".join(link(f"/{s}/", pretty_area(s)) for s in suburb_slugs[:8])
    faqs = [
        (f"What should I include for a {title.lower()} enquiry?", "Start with the property location, intended use, approximate dimensions, access, existing surfaces, drainage concerns and timing."),
        ("Who confirms the technical requirements?", "The appointed provider and project designer must confirm the applicable requirement for the actual design, site and selected system before work begins."),
        ("Is a price or construction outcome assured?", "No. Scope, quotation, contract, provider credentials and warranty information must be confirmed before work begins."),
    ]
    return f'''<section class="page-hero"><div class="container page-hero__grid"><div>{breadcrumb([("/", "Home"), ("/", "Services"), (f"/{slug}/", title)])}<span class="eyebrow">Service pathway</span><h1>{html.escape(title)} in South-West Sydney.</h1><p class="hero-lead">{description}</p><div class="hero-actions"><a class="button" href="/quote/">Start an enquiry <span>↗</span></a><a class="button button--ghost" href="{PHONE_URI}">Call {PHONE}</a></div></div><div class="page-hero__image">{img(filename, alt_register, True)}</div></div></section>
<section class="section"><div class="container"><div class="section-heading"><div><span class="eyebrow">A better brief</span><h2>Make the site questions visible.</h2></div><p>Every project is different. These are useful prompts for a conversation with the appointed provider, not a specification or promise of method.</p></div><div class="feature-grid"><article><span class="feature-icon">01</span><h3>Use &amp; access</h3><p>Explain how the area will be used, how people or vehicles reach it, and what needs to remain accessible.</p></article><article><span class="feature-icon">02</span><h3>Existing conditions</h3><p>Note current slabs, paving, soil, levels, drainage paths, edges and anything that may need investigation.</p></article><article><span class="feature-icon">03</span><h3>Project documents</h3><p>Bring drawings, approvals, easements or Council correspondence that may apply to the actual property.</p></article></div></div></section>
<section class="section section--tint"><div class="container split-grid split-grid--reverse"><div class="split-media">{img(image_for("cracks", media_names), alt_register)}<span class="image-caption">Existing conditions need an on-site assessment</span></div><div class="split-copy"><span class="eyebrow">Project-specific by design</span><h2>Technical details are confirmed for the actual system.</h2><p>Concrete thickness, strength or grade, reinforcement, base preparation, joints, curing, drainage and edges are not universal values. The appointed provider and project designer must confirm the applicable requirement before work begins.</p><p>For a selected product or finish, the supplier and appointed provider must also confirm what applies to the chosen system and conditions.</p></div></div></section>
<section class="section"><div class="container"><div class="section-heading section-heading--center"><span class="eyebrow">Related pathways</span><h2>Keep exploring the brief.</h2><p>These service pages sit alongside this enquiry pathway.</p></div><div class="service-grid service-grid--compact">{service_cards(alt_register, media_names, related)}</div></div></section>
<section class="section section--areas"><div class="container"><div class="section-heading"><div><span class="eyebrow">Areas</span><h2>Camden and nearby South-West Sydney.</h2></div><p>Area pages provide local context only. Confirm the actual property and council before committing to a scope.</p></div><div class="inline-links">{area_links}</div></div></section>
<section class="section section--faq"><div class="container faq-grid"><div><span class="eyebrow">Frequently asked</span><h2>Questions for this service.</h2></div><div class="faq-list">{faq_items(faqs)}</div></div></section>
{cta_band(f"Start a {title.lower()} enquiry") }'''


def suburb_content(slug: str, title: str, original: str, alt_register: dict[str, str], media_names: list[str], suburb_slugs: list[str]) -> str:
    area = pretty_area(slug)
    excerpt = safe_excerpt(original, 560) or f"An enquiry for {area} should describe the property, intended use, access, existing surfaces, drainage concerns and timing."
    neighbours = [s for s in suburb_slugs if s != slug][:6]
    local_image = image_for("aerial", media_names) if "park" in slug or "hills" in slug else image_for("driveway", media_names)
    context_note = "Council boundaries and approval pathways can vary by property. The controlling council's current requirements and approved documents must be checked for the actual address."
    return f'''<section class="page-hero page-hero--area"><div class="container page-hero__grid"><div>{breadcrumb([("/", "Home"), ("/", "Service areas"), (f"/{slug}/", area)])}<span class="eyebrow">Service area</span><h1>Concreting enquiries in {html.escape(area)}.</h1><p class="hero-lead">A considered starting point for residential, access and outdoor concrete questions around {html.escape(area)} and the wider South-West Sydney region.</p><div class="hero-actions"><a class="button" href="/quote/">Start an enquiry <span>↗</span></a><a class="button button--ghost" href="/contact/">Contact us</a></div></div><div class="page-hero__image">{img(local_image, alt_register, True)}</div></div></section>
<section class="section"><div class="container"><div class="section-heading"><div><span class="eyebrow">Local context</span><h2>Begin with what is true of your site.</h2></div><p>{context_note}</p></div><div class="local-context"><p>{html.escape(excerpt)}</p></div></div></section>
<section class="section section--tint"><div class="container"><div class="section-heading section-heading--center"><span class="eyebrow">Service pathways</span><h2>Choose the conversation that fits.</h2><p>Use the service pages to prepare a useful brief; the appointed provider confirms the project-specific requirements.</p></div><div class="service-grid service-grid--compact">{service_cards(alt_register, media_names, SERVICE_ORDER[:6])}</div></div></section>
<section class="section"><div class="container split-grid"><div class="split-media">{img(image_for("path", media_names), alt_register)}<span class="image-caption">Access, levels and edges are useful enquiry details</span></div><div class="split-copy"><span class="eyebrow">Questions worth bringing</span><h2>Access, drainage and intended use.</h2><p>Tell us what the area needs to do, what is already there and what might make access or levels difficult. Photographs, sketches and relevant Council correspondence can make the first conversation more useful.</p><p>For frontage work, confirm the controlling council and its current application, inspection and construction requirements before any commitment.</p><a class="arrow-link" href="/concrete-crossovers-and-laybacks-south-west-sydney/">Read about crossovers &amp; laybacks <span>→</span></a></div></div></section>
<section class="section section--areas"><div class="container"><div class="section-heading"><div><span class="eyebrow">Nearby areas</span><h2>Continue around South-West Sydney.</h2></div><p>These links are existing area pages, not a claim that every project is accepted or every boundary is identical.</p></div><div class="area-grid">{''.join(f'<a class="area-pill" href="/{n}/"><span>{html.escape(pretty_area(n))}</span><span>↗</span></a>' for n in neighbours)}</div></div></section>
<section class="section section--faq"><div class="container faq-grid"><div><span class="eyebrow">Area FAQ</span><h2>Before an area enquiry.</h2></div><div class="faq-list">{faq_items([(f"Do you work in {area}?", "This page is an enquiry pathway. We coordinate suitable independent-provider conversations after the property and scope are understood."), ("What should I send first?", "The address or locality, intended use, approximate dimensions, access constraints, existing surfaces, drainage concerns and timing are a useful start."), ("Are council requirements the same everywhere?", "No. The controlling council's current requirements and approved documents must be checked for the actual property."), ("Is the Camden address open to visitors?", f"No. {ADDRESS} is an administrative correspondence office and is not open to customers or visitors.")])}</div></div></section>
{cta_band(f"Start a {area} enquiry") }'''


def utility_content(slug: str, title: str, original: str, alt_register: dict[str, str], media_names: list[str]) -> str:
    if slug == "about":
        return f'''<section class="page-hero page-hero--simple"><div class="container narrow">{breadcrumb([("/", "Home"), ("/about/", "About")])}<span class="eyebrow">About Structure Co</span><h1>A clearer way to begin a concreting conversation.</h1><p class="hero-lead">{BRAND} coordinates enquiries with suitable independent providers across Camden and South-West Sydney.</p></div></section><section class="section"><div class="container split-grid"><div class="split-media">{img(image_for("project", media_names), alt_register, True)}</div><div class="split-copy"><span class="eyebrow">The model</span><h2>Useful information first.</h2><p>We help organise the site details and questions that make an enquiry easier to assess. The appointed provider confirms the method, documents, quotation and contractual details for the actual project.</p><p>Submitting an enquiry does not create a construction contract. The address is administrative correspondence only, and no public business credentials are asserted here.</p><a class="button" href="/quote/">Start an enquiry <span>↗</span></a></div></div></section><section class="section section--dark"><div class="container principles"><span class="eyebrow eyebrow--light">Our principles</span><div class="principle-grid"><article><h3>Specific, not sweeping.</h3><p>Site, design, council and product requirements are confirmed where they apply.</p></article><article><h3>Independent, not implied.</h3><p>Provider identity, licensing, insurance and warranty information are checked before work begins.</p></article><article><h3>Clear, not pushy.</h3><p>An enquiry gives you a place to start; it does not promise a price or outcome.</p></article></div></div></section>{cta_band("Have a question about the model?")}'''
    if slug == "contact":
        return f'''<section class="page-hero page-hero--simple"><div class="container narrow">{breadcrumb([("/", "Home"), ("/contact/", "Contact")])}<span class="eyebrow">Contact</span><h1>Bring the project questions.</h1><p class="hero-lead">Tell us about the site, the intended use and anything that needs a closer look.</p><div class="hero-actions"><a class="button" href="mailto:{EMAIL}">Email {EMAIL} <span>↗</span></a><a class="button button--ghost" href="{PHONE_URI}">Call {PHONE}</a></div></div></section><section class="section"><div class="container contact-grid"><div class="contact-card contact-card--primary"><span class="eyebrow">Enquiries</span><h2>Start by email or phone.</h2><p>Include the property locality, intended use, access constraints, existing surfaces, drainage concerns and timing where you can.</p><p><a class="contact-value" href="mailto:{EMAIL}">{EMAIL}</a><br><a class="contact-value" href="{PHONE_URI}">{PHONE}</a></p></div><div class="contact-card"><span class="eyebrow">Correspondence address</span><h2>{ADDRESS}</h2><p>This is an administrative office for correspondence only. It is not open to customers or visitors.</p><p class="muted">Submitting an enquiry does not create a construction contract.</p></div></div></section>{cta_band("Ready to share the essentials?")}'''
    if slug == "quote":
        return f'''<section class="page-hero page-hero--simple"><div class="container narrow">{breadcrumb([("/", "Home"), ("/quote/", "Start an enquiry")])}<span class="eyebrow">Start an enquiry</span><h1>Give the next conversation a head start.</h1><p class="hero-lead">A few useful details help us understand the shape of the question before an independent-provider conversation is coordinated.</p><a class="button" href="mailto:{EMAIL}?subject=Concrete%20enquiry%20for%20Camden">Email the enquiry <span>↗</span></a></div></section><section class="section"><div class="container enquiry-grid"><div><span class="eyebrow">What to include</span><h2>A practical brief can be simple.</h2><ul class="check-list"><li>Property address or locality</li><li>Intended use and approximate dimensions</li><li>Existing surface, access and drainage notes</li><li>Relevant drawings or Council correspondence</li><li>Preferred timing and any constraints</li></ul></div><div class="enquiry-note"><span class="feature-icon">i</span><h3>What happens next?</h3><p>We review the information and coordinate the next step where a suitable independent provider can assess the scope. Provider identity, quotation, contract, licensing, insurance and warranty details must be confirmed before work begins.</p><p>Submitting an enquiry does not create a construction contract.</p></div></div></section>{cta_band("Prefer to talk first?")}'''
    if slug == "gallery":
        gallery_images = SAFE_MEDIA[:9]
        return f'''<section class="page-hero page-hero--simple"><div class="container narrow">{breadcrumb([("/", "Home"), ("/gallery/", "Gallery")])}<span class="eyebrow">Approved image library</span><h1>Materials for the conversation.</h1><p class="hero-lead">A visual reference for finishes, access and existing conditions. These images do not represent a completed Camden project or a testimonial.</p></div></section><section class="section"><div class="container gallery-grid">{''.join(f'<figure>{img(name, alt_register)}<figcaption>{html.escape(alt_for(name, alt_register))}</figcaption></figure>' for name in gallery_images if name in media_names)}</div></section>{cta_band("Have a project image to share?")}'''
    if slug in {"privacy-policy", "privacy"}:
        return f'''<section class="page-hero page-hero--simple"><div class="container narrow">{breadcrumb([("/", "Home"), ("/privacy-policy/", "Privacy")])}<span class="eyebrow">Privacy</span><h1>Privacy and enquiry information.</h1><p class="hero-lead">A plain-language summary of how enquiry information is handled.</p></div></section><section class="section"><div class="container legal-copy"><h2>Information shared with us</h2><p>The public site label is {BRAND}. Enquiry information is coordinated only as reasonably necessary to respond to a request and for applicable administration.</p><p>An enquiry may include a name, phone number, suburb, requested service, optional email address, approximate job size and a free-text message. Payment details are not requested.</p><h2>Why information is used</h2><p>Information is used to respond to an enquiry and, with the submitter's consent, may be shared with a suitable independent provider so that the provider can assess the enquiry. It is not sold, rented or disclosed for third-party marketing.</p><h2>Questions or corrections</h2><p>For access, correction or deletion questions about an enquiry, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p>Submitting an enquiry does not create a construction contract.</p></div></section>'''
    body = safe_excerpt(original, 1500) or "This page provides approved information for a considered concreting enquiry."
    return f'''<section class="page-hero page-hero--simple"><div class="container narrow">{breadcrumb([("/", "Home"), (f"/{slug}/", title)])}<span class="eyebrow">Camden guide</span><h1>{html.escape(title)}</h1><p class="hero-lead">A practical reference for planning the questions around a concrete project.</p></div></section><section class="section"><div class="container article-layout"><article class="article-copy"><p class="lede">{html.escape(body[:500])}</p><h2>Start with the actual property.</h2><p>Site access, existing surfaces, levels, drainage, intended use and the relevant council context can all affect the questions that need to be answered. The appointed provider and project designer confirm what applies before work begins.</p><h2>Keep the enquiry specific.</h2><p>Share drawings, photos, dimensions or current correspondence where available. This helps separate a useful project question from a universal claim.</p></article><aside class="article-aside"><span class="eyebrow">Next step</span><h3>Talk through the brief.</h3><p>We can coordinate an enquiry with a suitable independent provider.</p><a class="button button--small" href="/quote/">Start an enquiry</a></aside></div></section>{cta_band()}'''


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "media").mkdir(parents=True)
    for source in MEDIA.iterdir():
        if source.is_file():
            shutil.copy2(source, OUT / "assets" / "media" / source.name)
    media_names = sorted(path.name for path in (OUT / "assets" / "media").iterdir() if path.is_file())
    alt_register = load_alt_register()
    items: list[ET.Element] = []
    for path in (SOURCE, PRIVACY):
        root = ET.parse(path).getroot()
        items.extend(item for item in root.findall("./channel/item") if (item.findtext(WP + "post_type") or "") == "page")
    pages: dict[str, tuple[str, str]] = {}
    for item in items:
        slug = (item.findtext(WP + "post_name") or "").strip()
        if not slug or slug in pages or slug in {"cost-comparison-calculator", "calculator"}:
            continue
        pages[slug] = (title_for(slug, item.findtext("title") or ""), body_for(item))
    if not any(slug in pages for slug in {"privacy", "privacy-policy"}):
        raise SystemExit("privacy page missing from approved derivatives")
    suburb_slugs = sorted(slug for slug in pages if slug.startswith("concreters-"))
    rows: list[tuple[str, str, str]] = []
    for slug, (title, original) in pages.items():
        path = "/" if slug == "homepage" else f"/{slug}/"
        output_dir = OUT if path == "/" else OUT / path.strip("/")
        output_dir.mkdir(parents=True, exist_ok=True)
        if slug == "homepage":
            description = "Structured concreting enquiries for Camden and South-West Sydney, coordinated with suitable independent providers."
            content = home_content(alt_register, media_names, suburb_slugs)
        elif slug in SERVICES:
            description = SERVICES[slug][1]
            content = service_content(slug, *SERVICES[slug], alt_register, media_names, suburb_slugs)
        elif slug.startswith("concreters-"):
            description = f"Concreting enquiry coordination for {pretty_area(slug)} and South-West Sydney."
            content = suburb_content(slug, title, original, alt_register, media_names, suburb_slugs)
        else:
            description = f"{title} · {BRAND}"
            content = utility_content(slug, title, original, alt_register, media_names)
        canonical = BASE + path
        (output_dir / "index.html").write_text(document(title, description, canonical, content, alt_register), encoding="utf-8")
        rows.append((slug, path, title))
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "site.js").write_text(JS, encoding="utf-8")
    (OUT / "sitemap.xml").write_text("<?xml version=\"1.0\" encoding=\"UTF-8\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" + "".join(f"<url><loc>{BASE}{path}</loc></url>" for _, path, _ in rows) + "</urlset>", encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (OUT / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n", encoding="utf-8")
    not_found = document("Page not found", "The requested page could not be found.", BASE + "/404/", f'<section class="page-hero page-hero--simple"><div class="container narrow"><span class="eyebrow">404</span><h1>That page is not here.</h1><p class="hero-lead">Try the homepage or explore the service pathways.</p><a class="button" href="/">Back to the homepage <span>↗</span></a></div></section>', alt_register)
    (OUT / "404.html").write_text(not_found, encoding="utf-8")
    print(json.dumps({"pages": len(rows), "images": len(media_names), "stylesheets": 1, "scripts": 1, "output": str(OUT)}, indent=2))
    return 0


JS = r'''(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  if (toggle && nav) toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('[data-year]').forEach(node => { node.textContent = new Date().getFullYear(); });
})();
'''


CSS = r'''@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--ink:#15211f;--muted:#60706c;--line:#dbe3df;--paper:#f7f8f5;--white:#fff;--green:#173f36;--green-2:#235e50;--lime:#c8e86b;--sand:#edf0e9;--orange:#e78b55;--shadow:0 20px 60px rgba(17,47,39,.1);--radius:18px;--container:1180px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:'DM Sans',Arial,sans-serif;font-size:16px;line-height:1.65}a{color:inherit;text-decoration:none}img{display:block;max-width:100%}.container{width:min(var(--container),calc(100% - 48px));margin:0 auto}.narrow{max-width:820px}.utility{background:var(--green);color:#dceae2;font-size:12px;letter-spacing:.03em}.utility__inner{display:flex;justify-content:space-between;gap:20px;padding:9px 0}.utility a{color:#f4f8e9}.utility__contact{display:flex;gap:18px}.site-header{position:sticky;top:0;z-index:20;background:rgba(247,248,245,.96);backdrop-filter:blur(15px);border-bottom:1px solid rgba(219,227,223,.8)}.nav-wrap{min-height:78px;display:flex;align-items:center;justify-content:space-between;gap:30px}.brand{display:flex;align-items:center;gap:11px;line-height:1.08}.brand-mark{display:grid;place-items:center;width:38px;height:38px;border-radius:10px;background:var(--lime);color:var(--green);font-family:'Space Grotesk';font-size:13px;font-weight:700;letter-spacing:-.08em}.brand strong,.brand small{display:block}.brand strong{font-family:'Space Grotesk';font-size:16px;letter-spacing:-.04em}.brand small{font-size:11px;color:var(--muted);margin-top:3px}.primary-nav{display:flex;align-items:center;gap:25px;font-size:14px;font-weight:600}.primary-nav>a,.nav-dropdown>button{transition:color .2s}.primary-nav>a:hover,.nav-dropdown>button:hover{color:var(--green-2)}.nav-dropdown{position:relative}.nav-dropdown>button{border:0;background:none;font:inherit;color:inherit;cursor:pointer;padding:30px 0}.nav-dropdown__menu{position:absolute;top:71px;left:-18px;display:none;width:255px;padding:15px;border:1px solid var(--line);border-radius:14px;background:var(--white);box-shadow:var(--shadow)}.nav-dropdown:hover .nav-dropdown__menu,.nav-dropdown:focus-within .nav-dropdown__menu{display:grid;gap:2px}.nav-dropdown__menu a{padding:9px 10px;border-radius:8px;font-size:13px}.nav-dropdown__menu a:hover{background:var(--sand)}.nav-cta,.button{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:var(--green);color:var(--white);padding:13px 19px;border-radius:999px;font-size:14px;font-weight:700;transition:transform .2s,background .2s}.nav-cta{padding:11px 16px;background:var(--orange)}.button:hover,.nav-cta:hover{transform:translateY(-2px);background:var(--green-2)}.button--ghost{background:transparent;color:var(--green);border:1px solid var(--green)}.button--ghost:hover{color:var(--white);background:var(--green)}.button--light{background:var(--lime);color:var(--green)}.button--small{font-size:13px;padding:10px 14px}.menu-toggle{display:none;border:1px solid var(--line);background:var(--white);border-radius:9px;padding:8px 12px;font:inherit;color:var(--ink)}
h1,h2,h3{font-family:'Space Grotesk',Arial,sans-serif;line-height:1.08;letter-spacing:-.055em;margin:0 0 18px}h1{font-size:clamp(44px,6vw,78px);max-width:750px}h2{font-size:clamp(32px,4vw,52px)}h3{font-size:22px}.eyebrow{display:inline-flex;align-items:center;gap:9px;color:var(--green-2);font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;margin-bottom:16px}.eyebrow:before{content:'';display:block;width:24px;height:2px;background:var(--orange)}.eyebrow--light{color:var(--lime)}.eyebrow--light:before{background:var(--lime)}.hero{overflow:hidden}.hero--home{padding:88px 0 74px;background:linear-gradient(120deg,#f7f8f5 5%,#eef2eb 100%)}.hero-grid,.page-hero__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(380px,.87fr);align-items:center;gap:72px}.hero-copy{position:relative;z-index:1}.hero h1 em{font-style:normal;color:var(--green-2);position:relative}.hero h1 em:after{content:'';position:absolute;left:2px;right:0;bottom:-4px;height:9px;background:var(--lime);z-index:-1;transform:skew(-14deg)}.hero-lead{font-size:19px;line-height:1.55;max-width:620px;color:#40504b;margin:0 0 28px}.hero-actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px}.micro-note{color:var(--muted);font-size:12px;margin:17px 0 0}.hero-media{position:relative}.hero-media__frame,.page-hero__image{border-radius:24px;overflow:hidden;background:var(--green);box-shadow:var(--shadow);aspect-ratio:1.03}.hero-media img,.page-hero__image img{width:100%;height:100%;object-fit:cover}.hero-stamp{position:absolute;bottom:-24px;left:-28px;background:var(--lime);border-radius:14px;padding:18px 22px;display:flex;align-items:center;gap:13px;box-shadow:0 12px 28px rgba(28,61,48,.15)}.hero-stamp strong{font:700 31px 'Space Grotesk';color:var(--green)}.hero-stamp span{font-size:11px;font-weight:700;line-height:1.35;text-transform:uppercase;letter-spacing:.08em}.trust-strip{background:var(--green);color:var(--white)}.trust-grid{display:grid;grid-template-columns:repeat(3,1fr);padding:20px 0}.trust-grid div{display:flex;align-items:center;gap:16px;padding:9px 24px;border-right:1px solid rgba(255,255,255,.2)}.trust-grid div:first-child{padding-left:0}.trust-grid div:last-child{border:0}.trust-grid strong{font:600 13px 'Space Grotesk';color:var(--lime)}.trust-grid span{font-size:13px;color:#d7e5dc}.section{padding:105px 0}.section--services{background:var(--white)}.section--tint,.section--areas{background:var(--sand)}.section--dark{background:var(--green);color:var(--white)}.section--faq{background:var(--white)}.section-heading{display:flex;align-items:end;justify-content:space-between;gap:40px;margin-bottom:42px}.section-heading>p{max-width:430px;color:var(--muted);margin:0}.section-heading--center{display:block;text-align:center;max-width:680px;margin-left:auto;margin-right:auto}.section-heading--center>p{margin:0 auto}.service-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.service-grid--compact{grid-template-columns:repeat(3,1fr)}.service-card{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--paper);transition:transform .25s,box-shadow .25s}.service-card:hover{transform:translateY(-5px);box-shadow:var(--shadow)}.card-image{height:190px;overflow:hidden;background:#dfe7df}.card-image img{width:100%;height:100%;object-fit:cover;transition:transform .5s}.service-card:hover .card-image img{transform:scale(1.05)}.service-card__body{padding:22px 23px 24px;position:relative}.card-number{color:var(--orange);font:700 11px 'Space Grotesk';letter-spacing:.1em}.service-card h3{font-size:23px;margin:8px 0 10px}.service-card h3 a:hover{color:var(--green-2)}.service-card p{color:var(--muted);font-size:14px;line-height:1.55;min-height:68px;margin:0 0 17px}.arrow-link,.text-link{display:inline-flex;align-items:center;gap:8px;color:var(--green-2);font-size:13px;font-weight:700}.arrow-link span,.text-link span{font-size:18px;transition:transform .2s}.arrow-link:hover span,.text-link:hover span{transform:translateX(4px)}.split-grid{display:grid;grid-template-columns:1fr 1fr;gap:85px;align-items:center}.split-grid--reverse{grid-template-columns:1fr 1fr}.split-grid--reverse .split-media{order:2}.split-media{position:relative}.split-media img{width:100%;aspect-ratio:1.14;object-fit:cover;border-radius:20px;box-shadow:var(--shadow)}.image-caption{position:absolute;bottom:15px;left:15px;right:15px;padding:9px 12px;border-radius:9px;background:rgba(21,33,31,.82);color:#fff;font-size:11px}.split-copy p{max-width:510px;color:var(--muted)}.process-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;border:1px solid var(--line);background:var(--line);border-radius:18px;overflow:hidden}.process-step{background:var(--white);padding:31px 28px 34px}.process-step>span{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--lime);color:var(--green);font:700 12px 'Space Grotesk';margin-bottom:26px}.process-step p{color:var(--muted);font-size:14px}.council-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:100px;align-items:center}.section--dark p{color:#c9d7d0}.council-card{background:#215345;border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:30px}.council-card__icon{font-size:34px;color:var(--lime);display:block;margin-bottom:16px}.council-card h3{color:var(--white)}.text-link--light{color:var(--lime)}.area-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.area-pill{display:flex;justify-content:space-between;align-items:center;padding:17px 18px;border:1px solid #d5ded6;border-radius:11px;background:rgba(255,255,255,.58);font-size:13px;font-weight:700;transition:background .2s,border .2s}.area-pill:hover{background:var(--white);border-color:var(--green-2)}.faq-grid{display:grid;grid-template-columns:.72fr 1.28fr;gap:90px}.faq-list{border-top:1px solid var(--line)}.faq-item{border-bottom:1px solid var(--line);padding:18px 0}.faq-item summary{cursor:pointer;list-style:none;font:600 17px 'Space Grotesk';display:flex;justify-content:space-between;gap:20px}.faq-item summary::-webkit-details-marker{display:none}.faq-item summary:after{content:'+';color:var(--orange);font-size:24px;line-height:1}.faq-item[open] summary:after{content:'−'}.faq-item p{color:var(--muted);font-size:14px;max-width:680px;margin:12px 0 0}.cta-band{margin:0 auto 0;padding:60px max(24px,calc((100% - var(--container))/2));background:var(--orange);color:var(--green);display:flex;justify-content:space-between;align-items:center;gap:40px}.cta-band h2{font-size:38px;max-width:600px;margin-bottom:10px}.cta-band p{max-width:590px;margin:0;color:#315448}.cta-band__actions{display:flex;align-items:center;gap:20px;flex-wrap:wrap}.page-hero{padding:64px 0 76px;background:linear-gradient(120deg,#eef2eb,#f7f8f5)}.page-hero__grid{gap:70px}.page-hero h1{font-size:clamp(42px,5vw,67px)}.page-hero__image{aspect-ratio:1.15}.breadcrumbs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 40px;color:var(--muted);font-size:12px}.breadcrumbs span{color:#a4b0aa}.breadcrumbs a:last-child{color:var(--green);font-weight:700}.page-hero--simple{padding:70px 0 83px}.page-hero--simple h1{max-width:780px}.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.feature-grid article,.principle-grid article{border:1px solid var(--line);border-radius:16px;padding:27px;background:var(--white)}.feature-icon{display:grid;place-items:center;width:36px;height:36px;background:var(--lime);border-radius:9px;color:var(--green);font:700 12px 'Space Grotesk';margin-bottom:24px}.feature-grid p,.principle-grid p{color:var(--muted);font-size:14px}.inline-links{display:flex;flex-wrap:wrap;gap:11px 20px}.inline-links a{text-decoration:underline;text-decoration-color:#b4cdb7;text-underline-offset:5px}.principles .eyebrow{margin-bottom:35px}.principle-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.principle-grid article{background:#215345;border-color:rgba(255,255,255,.13)}.principle-grid h3{color:var(--white)}.principle-grid p{color:#c9d7d0}.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.contact-card{border:1px solid var(--line);border-radius:18px;padding:35px;background:var(--white)}.contact-card--primary{background:var(--green);color:var(--white);border-color:var(--green)}.contact-card--primary p{color:#d0e0d7}.contact-card h2{font-size:31px}.contact-value{font:600 20px 'Space Grotesk';color:var(--lime)}.muted{color:var(--muted)}.enquiry-grid{display:grid;grid-template-columns:1fr 1fr;gap:90px}.check-list{padding:0;margin:25px 0;list-style:none}.check-list li{padding:13px 0 13px 28px;border-bottom:1px solid var(--line);position:relative}.check-list li:before{content:'✓';position:absolute;left:0;color:var(--green-2);font-weight:700}.enquiry-note{border-radius:18px;padding:32px;background:var(--sand);align-self:start}.gallery-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.gallery-grid figure{margin:0;background:var(--white);border:1px solid var(--line);border-radius:15px;overflow:hidden}.gallery-grid img{width:100%;aspect-ratio:1.2;object-fit:cover}.gallery-grid figcaption{padding:13px 15px;color:var(--muted);font-size:12px}.legal-copy,.article-copy{max-width:800px}.legal-copy h2,.article-copy h2{font-size:32px;margin-top:42px}.legal-copy p,.article-copy p{color:var(--muted)}.article-layout{display:grid;grid-template-columns:1fr 310px;gap:75px}.article-copy .lede{font-size:20px;color:var(--ink)}.article-aside{align-self:start;background:var(--sand);border-radius:18px;padding:27px}.article-aside p{font-size:14px}.site-footer{background:#102d27;color:#d8e4dc;padding:70px 0 22px}.brand--footer{color:var(--white)}.brand--footer small{color:#b3c9bd}.footer-grid{display:grid;grid-template-columns:1.35fr .65fr 1fr 1fr;gap:40px}.site-footer h2{font:600 13px 'Space Grotesk';letter-spacing:.12em;text-transform:uppercase;color:var(--lime);margin:4px 0 18px}.site-footer ul{list-style:none;padding:0;margin:0;display:grid;gap:8px;font-size:13px}.site-footer li a:hover{color:var(--lime)}.footer-intro{max-width:300px;color:#a9c1b6;font-size:13px;margin-top:25px}.site-footer p{font-size:13px;color:#a9c1b6}.site-footer a{color:#f1f5ed}.footer-address{line-height:1.7}.footer-address small{color:#a9c1b6}.footer-bottom{border-top:1px solid rgba(255,255,255,.14);display:flex;justify-content:space-between;gap:20px;padding-top:20px;margin-top:60px;color:#9db5aa;font-size:11px}
@media (max-width:980px){.primary-nav{gap:14px}.hero-grid,.page-hero__grid{grid-template-columns:1fr 1fr;gap:38px}.service-grid,.service-grid--compact{grid-template-columns:repeat(2,1fr)}.area-grid{grid-template-columns:repeat(3,1fr)}.footer-grid{grid-template-columns:1.3fr 1fr 1fr}.footer-grid>div:last-child{grid-column:2}.council-grid{gap:45px}.section{padding:80px 0}}
@media (max-width:720px){.container{width:min(var(--container),calc(100% - 32px))}.utility__inner{display:block;text-align:center}.utility__contact{justify-content:center;margin-top:3px}.nav-wrap{min-height:68px}.menu-toggle{display:block}.primary-nav{display:none;position:absolute;top:100%;left:0;right:0;background:var(--paper);border-bottom:1px solid var(--line);padding:14px 16px 20px;flex-direction:column;align-items:stretch;gap:3px;box-shadow:0 16px 30px rgba(17,47,39,.08)}.primary-nav.is-open{display:flex}.primary-nav>a,.nav-dropdown>button{padding:12px 10px;text-align:left}.nav-dropdown__menu{position:static;width:auto;border:0;box-shadow:none;padding:0 0 5px 12px;background:transparent;display:grid}.nav-cta{text-align:center!important;margin-top:8px}.hero--home{padding:54px 0 65px}.hero-grid,.page-hero__grid,.split-grid,.split-grid--reverse,.council-grid,.faq-grid,.contact-grid,.enquiry-grid,.article-layout{grid-template-columns:1fr;gap:38px}.hero h1{font-size:48px}.hero-lead{font-size:17px}.hero-media{margin:0 15px 15px}.hero-stamp{left:-15px}.trust-grid{grid-template-columns:1fr;gap:0;padding:7px 0}.trust-grid div,.trust-grid div:first-child{border-right:0;border-bottom:1px solid rgba(255,255,255,.2);padding:12px 0}.section{padding:65px 0}.section-heading{display:block;margin-bottom:28px}.section-heading>p{margin-top:14px}.service-grid,.service-grid--compact,.feature-grid,.principle-grid,.gallery-grid{grid-template-columns:1fr}.service-card p{min-height:auto}.card-image{height:210px}.split-grid--reverse .split-media{order:0}.split-copy h2{font-size:36px}.process-grid{grid-template-columns:1fr}.area-grid{grid-template-columns:repeat(2,1fr)}.cta-band{display:block;padding:48px 24px}.cta-band h2{font-size:33px}.cta-band__actions{margin-top:25px}.page-hero{padding:45px 0 58px}.page-hero--simple{padding:52px 0 62px}.breadcrumbs{margin-bottom:28px}.page-hero__image{order:-1;aspect-ratio:1.4}.page-hero__grid .page-hero__image{margin-bottom:10px}.page-hero__grid>div:first-child{order:1}.footer-grid{grid-template-columns:1fr 1fr;gap:35px}.footer-grid>div:last-child{grid-column:auto}.footer-bottom{display:block;margin-top:40px}.footer-bottom span{display:block;margin-top:7px}.hero-actions .button{width:100%}.contact-value{font-size:18px}}
'''


if __name__ == "__main__":
    raise SystemExit(main())
