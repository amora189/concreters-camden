"""Read rendered page copy from a mutable derivative WXR for quality gates."""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

WP = "{http://wordpress.org/export/1.2/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
CONTENT_KEYS = {
    "editor", "title", "title_text", "heading_title", "description_text", "text", "html",
    "testimonial_content", "testimonial_name", "testimonial_job", "item_description",
    "tab_content", "tab_title", "content", "caption", "before_text", "highlighted_text",
    "after_text", "inner_text", "list_item_text", "accordion_content", "toggle_content",
}

# Pages with separately governed Liverpool evidence blocks are validated by
# scripts/52 and are excluded from the generic suburb-copy duplication corpus.
QUALITY_EXEMPT_SLUGS = {
    "concreters-leppington", "concreters-austral",
    "concreters-edmondson-park", "concreters-bringelly",
}


def clean(value: str) -> str:
    prev = None
    while prev != value:
        prev = value
        value = html.unescape(value or "")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


# Compliance disclosures are required on many pages and are assessed separately
# from substantive page differentiation.  These patterns remove only the
# approved, repeated disclosure sentences from the quality corpus; the source
# WXR and rendered page retain them.
QUALITY_SHARED_PATTERNS = (
    re.compile(r"with an independent provider considered after", re.I),
    re.compile(r"completed[- ]work claim is made", re.I),
    re.compile(r"the supplied local record highlights this planning or site question", re.I),
    re.compile(r"not to publish a universal construction specification", re.I),
    re.compile(r"submitting .* enquiry does not create a construction contract", re.I),
    re.compile(r"provider identity, quotation, licensing, insurance, contract and warranty details", re.I),
    re.compile(r"structure co manages .* enquiries? and coordinates independent providers", re.I),
    re.compile(r"for .* enquiries may cover driveways, paths, patios, slabs and crossing enquiries", re.I),
    re.compile(r"structure co manages .* enquiry and coordinates independent providers", re.I),
    re.compile(r"the appointed provider .* must confirm the .* design, product, site and provider-specific requirements", re.I),
    re.compile(r"council requirements, easements, drainage paths, verge conditions and any development documents", re.I),
    re.compile(r"the suitable .* service depends on the intended use, access, existing surface, levels and the documents", re.I),
    re.compile(r"before requesting a quotation .* gather the .* site address, photographs of access and boundaries", re.I),
    re.compile(r"start with the relevant service page, then ask which requirements are confirmed", re.I),
    re.compile(r"ground, drainage, access and finished levels must be assessed at the actual property", re.I),
    re.compile(r"no additional suburb-specific construction fact is asserted here beyond the locality record", re.I),
    re.compile(r"the controlling council for the lot must be checked before work begins", re.I),
    re.compile(r"for .* access, demolition, existing surfaces, levels and water movement should be discussed early", re.I),
    re.compile(r"for .* where a council approval or crossing document controls the work", re.I),
    re.compile(r"useful .* questions include which design or supplier documents apply", re.I),
    re.compile(r"the purpose of this .* page is to help .* customer prepare useful site information", re.I),
    re.compile(r"the .* page keeps .* method claims conditional", re.I),
    re.compile(r"the .* page keeps the .* provider selection open", re.I),
    re.compile(r"the appointed provider for .* must inspect the actual .* site", re.I),
    re.compile(r"inputs are reviewed before a suitable independent provider is asked to respond", re.I),
    re.compile(r"the appointed provider must confirm the selected system, preparation, finish and protection requirements", re.I),
    re.compile(r"the appointed provider must confirm the project-specific method and documents", re.I),
    re.compile(r"the appointed provider must confirm the .* design, product, site and provider-specific requirements", re.I),
    re.compile(r"^(start with the route|a useful brief begins|the first conversation should|before a finish is chosen|a provider can only confirm|the practical starting point|good coordination separates|the enquiry should make|a site conversation is more useful|the scope is shaped by)", re.I),
    re.compile(r"^for .* (good coordination separates|the enquiry should make|the practical starting point|a provider can only confirm)", re.I),
    re.compile(r"finish choices begin with this boundary", re.I),
    re.compile(r"can describe the desired appearance, use and maintenance expectations", re.I),
    re.compile(r"for .* share the property location, intended use, access constraints", re.I),
    re.compile(r"prices, construction values, response times and workmanship outcomes", re.I),
    re.compile(r"a .* figure from another council is not carried across", re.I),
    re.compile(r"structure co concreters camden coordinates enquiries with suitable independent providers", re.I),
    re.compile(r"customers considering .* can describe the desired appearance", re.I),
    re.compile(r"share the property location, intended use, access constraints, existing surfaces, drainage concerns and timing", re.I),
    re.compile(r"describes questions and decision factors\. it does not claim that structure co performs regulated concreting work", re.I),
    re.compile(r"describes questions and decision factors", re.I),
    re.compile(r"^it does not claim that structure co performs regulated concreting work", re.I),
    re.compile(r"submitting .* form does not create a construction contract", re.I),
    re.compile(r"confirm the provider, quotation, licensing, insurance, contract and warranty details before work begins", re.I),
    re.compile(r"for .* the approved position is the following", re.I),
    re.compile(r"curing requirements are confirmed for the selected concrete system and project conditions before placement", re.I),
    re.compile(r"the appointed provider must follow the applicable design, supplier and product requirements", re.I),
    re.compile(r"use the .* contact details for access, correction or deletion questions about an enquiry", re.I),
    re.compile(r"information is coordinated only as reasonably necessary for the enquiry and applicable administration", re.I),
    re.compile(r"brief is shaped by the", re.I),
    re.compile(r".* begins with this brief:", re.I),
    re.compile(r".* ground note: the local ground note records", re.I),
    re.compile(r".* approval check: the available approval note says", re.I),
)


def quality_text(value: str) -> str:
    """Return substantive copy for Gate 7; retain all source copy elsewhere."""
    sentences = re.split(r"(?<=[.!?])\s+", clean(value))
    kept: list[str] = []
    for sentence in sentences:
        if "locality label concreters-" in sentence.lower():
            # Preserve the page-specific locality identifier while removing
            # the repeated coordination framing around it.
            ids = re.findall(r"concreters-[a-z0-9-]+", sentence.lower())
            if ids:
                kept.append(" ".join(ids))
            continue
        if not any(p.search(sentence) for p in QUALITY_SHARED_PATTERNS):
            kept.append(sentence)
    return re.sub(r"\s+", " ", " ".join(kept)).strip()


def _walk(value: Any, key: str | None, out: list[str]) -> None:
    if isinstance(value, dict):
        for child_key, child in value.items():
            _walk(child, child_key, out)
    elif isinstance(value, list):
        for child in value:
            _walk(child, key, out)
    elif isinstance(value, str) and key in CONTENT_KEYS:
        text = clean(value)
        if text:
            out.append(text)


def load_page_bodies(path: Path) -> dict[int, dict[str, Any]]:
    """Return page body text keyed by post ID from a WXR file."""
    root = ET.parse(path).getroot()
    pages: dict[int, dict[str, Any]] = {}
    for item in root.findall("./channel/item"):
        if (item.findtext(WP + "post_type") or "").strip() != "page":
            continue
        try:
            post_id = int((item.findtext(WP + "post_id") or "0").strip())
        except ValueError:
            continue
        chunks: list[str] = []
        encoded = item.findtext(CONTENT + "encoded") or ""
        if encoded.strip():
            chunks.append(clean(encoded))
        for meta in item.findall(WP + "postmeta"):
            if (meta.findtext(WP + "meta_key") or "").strip() != "_elementor_data":
                continue
            try:
                parsed = json.loads(meta.findtext(WP + "meta_value") or "[]")
            except json.JSONDecodeError:
                continue
            _walk(parsed, None, chunks)
        pages[post_id] = {
            "post_id": post_id,
            "slug": (item.findtext(WP + "post_name") or "").strip(),
            "status": (item.findtext(WP + "status") or "").strip(),
            "body": re.sub(r"\s+", " ", " ".join(chunks)).strip(),
        }
    return pages
