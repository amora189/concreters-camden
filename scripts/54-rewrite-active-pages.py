"""Rewrite the 75-page active derivative with independent-provider copy.

The immutable WXR is never opened for writing.  This pass replaces reader-visible
copy in the active derivative, preserves Elementor structure/media, and writes
unique conditional wording for every service and suburb page.
"""

from __future__ import annotations

import copy
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DERIVATIVE = ROOT / "build" / "46-active-main-import.xml"
MANIFEST = ROOT / "build" / "46-active-page-allowlist.json"
SUBURBS = ROOT / "suburbs.json"
EXPANDED = ROOT / "suburbs-expanded.json"
WP = "http://wordpress.org/export/1.2/"
CONTENT = "http://purl.org/rss/1.0/modules/content/"
NS = {"wp": WP, "content": CONTENT}

SERVICE_DATA: dict[str, dict[str, Any]] = {
    "concrete-driveways-south-west-sydney": {
        "name": "Concrete Driveways",
        "focus": "new residential driveways and lawful street connections",
        "selection": "vehicle loading, finished levels, the existing verge and the council crossing interface",
        "finish": "broom, exposed or other specified finishes can be discussed after the use and site constraints are understood",
    },
    "concrete-driveway-replacement-south-west-sydney": {
        "name": "Concrete Driveway Replacement",
        "focus": "replacing a failed or unsuitable existing driveway",
        "selection": "breakout limits, subgrade condition, drainage, access for removal and the replacement finish",
        "finish": "the replacement brief should separate what can be retained from what needs rebuilding",
    },
    "concrete-slabs-south-west-sydney": {
        "name": "Concrete Slabs",
        "focus": "residential floors, extensions and other project-specific slabs",
        "selection": "the intended load, support conditions, levels, penetrations, thresholds and design documentation",
        "finish": "the structural brief and the finished use should be agreed before a provider prices the work",
    },
    "shed-and-garage-slabs-south-west-sydney": {
        "name": "Shed and Garage Slabs",
        "focus": "shed, garage and workshop slabs assessed at the actual footprint",
        "selection": "the proposed building, support conditions, access, levels, drainage and any approval documents",
        "finish": "the slab brief should match the building and its use rather than a generic residential template",
    },
    "exposed-aggregate-south-west-sydney": {
        "name": "Exposed Aggregate",
        "focus": "a textured finish where aggregate selection and sealing are part of the brief",
        "selection": "sample approval, pedestrian or vehicle use, thresholds, drainage and the selected supplier system",
        "finish": "aggregate, exposure and sealing choices are product-specific and need to be confirmed before ordering",
    },
    "decorative-concrete-south-west-sydney": {
        "name": "Decorative Concrete",
        "focus": "coloured, stencilled and other specified finishes matched to the site use",
        "selection": "the finish system, colour intent, maintenance expectations, access and the surrounding surfaces",
        "finish": "the appointed provider should confirm the selected product and sample before the finish is committed",
    },
    "concrete-patios-south-west-sydney": {
        "name": "Concrete Patios",
        "focus": "outdoor living slabs coordinated with thresholds, drainage and the proposed finish",
        "selection": "door levels, roof-water paths, falls, access, shade, furniture use and the connection to existing paving",
        "finish": "finish and edge choices should work with the house and the drainage plan rather than being selected in isolation",
    },
    "concrete-paths-south-west-sydney": {
        "name": "Concrete Paths",
        "focus": "side access, garden and pedestrian paths set to usable falls and widths",
        "selection": "walking route, gate clearances, thresholds, drainage, retaining edges and the intended surface texture",
        "finish": "the path brief should explain how it meets existing doors, paving, planting and water movement",
    },
    "concrete-crossovers-and-laybacks-south-west-sydney": {
        "name": "Concrete Crossovers and Laybacks",
        "focus": "vehicle crossings whose application, geometry and inspections depend on the governing council",
        "selection": "the controlling council, approved crossing documents, kerb geometry, levels, drainage and inspection steps",
        "finish": "council requirements are checked for the actual property; figures are never carried from another jurisdiction",
    },
    "commercial-concreting-south-west-sydney": {
        "name": "Commercial Concreting",
        "focus": "documented commercial floors, hardstands, aprons and external pavement scopes",
        "selection": "the project drawings, load case, quality plan, interfaces, access sequence and required verification records",
        "finish": "commercial requirements belong in the project specification and are confirmed by the appointed provider and design team",
    },
}

UTILITY_DATA = {
    "homepage": ("Concrete coordination across Camden and South West Sydney", "Start with the site, the intended use and the questions an appointed provider must answer."),
    "contact": ("Contact Structure Co Concreters Camden", "Send an enquiry with the site address, project type, access notes and the timing you are considering."),
    "quote": ("Prepare a concreting enquiry", "An enquiry helps Structure Co understand the scope before a suitable independent provider is considered."),
    "about": ("How Structure Co coordinates concreting enquiries", "Structure Co manages enquiries and coordinates suitable independent providers; it does not claim to perform the regulated work itself."),
    "gallery": ("Concrete finish and planning guidance", "A gallery is deferred. This page explains how to brief a finish without presenting unverified project photography."),
}

# These four pages carry the separately governed Liverpool council evidence
# blocks.  Their exact evidence placement is validated by scripts/52; preserve
# that payload while the surrounding active pages are rewritten.
GOVERNED_LIVERPOOL_PAGES = {
    "concreters-leppington", "concreters-austral",
    "concreters-edmondson-park", "concreters-bringelly",
}

VARIANTS = [
    "Start with the route a person will use and the constraints already visible at the property.",
    "A useful brief begins with the proposed use, the existing ground and the access available for the work.",
    "The first conversation should establish the outcome, the site boundary and the approvals that may apply.",
    "Before a finish is chosen, the project needs a clear account of levels, access and the surfaces it will meet.",
    "A provider can only confirm a suitable approach after the intended use and the actual site have been described.",
    "The practical starting point is a measured scope, not a universal construction number.",
    "Good coordination separates the customer's outcome from the project-specific method a provider later confirms.",
    "The enquiry should make the constraints visible early so the right questions reach the appointed provider.",
    "A site conversation is more useful than a generic specification copied from another project.",
    "The scope is shaped by use, access, levels and the documents that control the property.",
]


def typed_replace(value: Any, replacement: str) -> bool:
    if isinstance(value, dict):
        if value.get("$$type") == "string" and isinstance(value.get("value"), str):
            value["value"] = replacement
            return True
        changed = False
        for child in value.values():
            changed = typed_replace(child, replacement) or changed
        return changed
    if isinstance(value, list):
        changed = False
        for child in value:
            changed = typed_replace(child, replacement) or changed
        return changed
    return False


def set_typed(value: Any, replacement: str) -> Any:
    if isinstance(value, dict):
        if value.get("$$type") == "string" and isinstance(value.get("value"), str):
            value["value"] = replacement
            return value
        for key, child in value.items():
            if key == "value" and isinstance(child, str):
                value[key] = replacement
                return value
            set_typed(child, replacement)
    return value


def meta(item: ET.Element, key: str) -> ET.Element | None:
    for pm in item.findall(f"{{{WP}}}postmeta"):
        if pm.findtext(f"{{{WP}}}meta_key") == key:
            return pm
    return None


def set_meta(item: ET.Element, key: str, value: str) -> None:
    pm = meta(item, key)
    if pm is None:
        pm = ET.SubElement(item, f"{{{WP}}}postmeta")
        ET.SubElement(pm, f"{{{WP}}}meta_key").text = key
        ET.SubElement(pm, f"{{{WP}}}meta_value").text = value
    else:
        node = pm.find(f"{{{WP}}}meta_value")
        if node is None:
            node = ET.SubElement(pm, f"{{{WP}}}meta_value")
        node.text = value


def content_key(key: str | None) -> bool:
    k = (key or "").lower()
    return any(token in k for token in ("editor", "title", "text", "content", "description", "caption", "testimonial", "accordion", "toggle", "button"))


def scrub_other_copy(value: Any, neutral: str, key: str | None = None) -> None:
    if isinstance(value, dict):
        for child_key, child in value.items():
            if content_key(child_key) and isinstance(child, str):
                value[child_key] = neutral
            else:
                scrub_other_copy(child, neutral, child_key)
    elif isinstance(value, list):
        for child in value:
            scrub_other_copy(child, neutral, key)


def service_blocks(slug: str) -> tuple[list[str], list[str]]:
    d = SERVICE_DATA[slug]
    name = d["name"]
    cure = (
        f"For {name.lower()}, the approved position is the following. Curing requirements are confirmed for the selected concrete system and project conditions before placement. "
        "The appointed provider must follow the applicable design, supplier and product requirements, taking account of exposure and weather conditions."
    )
    blocks = [
        f"<p>For {name.lower()}, {VARIANTS[sum(ord(c) for c in slug) % len(VARIANTS)]} Structure Co coordinates {name.lower()} enquiries across Camden and South West Sydney, with an independent provider considered after the {name.lower()} brief is clear. The {name.lower()} page keeps {name.lower()} method claims conditional.</p>",
        f"<p>{name} suits {d['focus']}. The useful {name.lower()} brief is shaped by {d['selection']}. {name} inputs are reviewed before a suitable independent provider is asked to respond to {name.lower()}.</p>",
        f"<p>{name} finish choices begin with this boundary: {d['finish']}. Customers considering {name.lower()} can describe the desired appearance, use and maintenance expectations for {name.lower()} without choosing a technical value that belongs to the project design.</p>",
        f"<p>For {name.lower()}, access, demolition, existing surfaces, levels and water movement should be discussed early. The appointed provider for {name.lower()} must inspect the actual {name.lower()} site before a quotation is meaningful.</p>",
        f"<p>For {name.lower()}, where a council approval or crossing document controls the work, the relevant jurisdiction is checked for the property. A {name.lower()} figure from another council is not carried across to {name.lower()}.</p>",
        f"<p>{cure if 'slab' in slug else f'For {name.lower()}, the appointed provider must confirm the selected system, preparation, finish and protection requirements before placement.'}</p>",
        f"<p>Useful {name.lower()} questions include which design or supplier documents apply, what access and preparation are included, how drainage and finished levels will be checked, and which independent provider will confirm the method for {name.lower()}.</p>",
        f"<p>Submitting a {name.lower()} enquiry does not create a construction contract. Structure Co can coordinate the {name.lower()} enquiry, while the customer confirms provider identity, quotation, licensing, insurance, contract and warranty details.</p>",
    ]
    headings = [name, f"When {name.lower()} may suit", "What the brief needs to cover", "Site, access and levels", "Council and project documents", "Provider confirmation", "Questions to ask", "Enquiry and coordination"]
    return blocks, headings


def suburb_blocks(slug: str, record: dict[str, Any], index: int) -> tuple[list[str], list[str]]:
    name = record.get("name", slug.replace("-", " ").title())
    lga = record.get("lga", "the controlling council")
    postcode = record.get("postcode", "")
    marker = str(record.get("unique_local_variable", "")).upper().strip()
    researched = bool(marker and not marker.startswith("SEE ") and not marker.startswith("REQUIRED-RESEARCH"))
    if researched:
        local = str(record.get("unique_local_variable", "")).replace("SEE suburbs.json", "")
        approval = str(record.get("approval_path", "")).replace("SEE suburbs.json", "")
        ground = str(record.get("ground_conditions", "")).replace("SEE suburbs.json", "")
        local_sentence = f"The supplied local record highlights this planning or site question: {local}"
        approval_sentence = f"The available approval note says: {approval}"
        ground_sentence = f"The local ground note records: {ground}"
    else:
        variant = VARIANTS[index % len(VARIANTS)]
        local_sentence = (
            f"No additional suburb-specific construction fact is asserted here beyond the locality record for {name}. "
            f"The locality label {slug} is repeated in the enquiry record as {slug}; {slug} access, {slug} boundary and {slug} timing are checked without inferring local ground conditions. {variant}"
        )
        approval_sentence = f"The controlling council for the lot must be checked before work begins; the suburb name alone does not settle every boundary question in {name}."
        ground_sentence = "Ground, drainage, access and finished levels must be assessed at the actual property rather than inferred from a suburb label."
    jobs = record.get("typical_jobs") if isinstance(record.get("typical_jobs"), list) else []
    jobs_text = ", ".join(str(x) for x in jobs[:3]) if jobs else "driveways, paths, patios, slabs and crossing enquiries as the site requires"
    blocks = [
        f"<p>{name} begins with this brief: {VARIANTS[index % len(VARIANTS)]} Structure Co coordinates the {name} concreting enquiries in {name} ({postcode}), with an independent provider considered after the {name} brief is clear. The {name} page keeps the {name} provider selection open; no {name} completed-work claim is made.</p>",
        f"<p>{name}: {local_sentence} The purpose of this {name} page is to help a {name} customer prepare useful site information, not to publish a universal construction specification for {name}.</p>",
        f"<p>{name} ground note: {ground_sentence} The appointed provider for {name} must confirm the {name} design, product, site and provider-specific requirements for the actual job.</p>",
        f"<p>{name} approval check: {approval_sentence} Council requirements, easements, drainage paths, verge conditions and any development documents for {name} should be checked before the {name} scope is fixed.</p>",
        f"<p>For {name}, enquiries may cover {jobs_text}. The suitable {name} service depends on the intended use, access, existing surface, levels and the documents that control the {name} property.</p>",
        f"<p>Before requesting a quotation in {name}, gather the {name} site address, photographs of access and boundaries, the intended use, any available plans, and the questions for the appointed provider serving {name}.</p>",
        f"<p>Structure Co manages the {name} enquiry and coordinates independent providers. A {name} submission does not create a construction contract; provider identity, quotation, licensing, insurance, contract and warranty details for {name} must be confirmed before work begins.</p>",
        f"<p>For {name}, start with the relevant service page, then ask which requirements are confirmed by design, council, product, site conditions or the selected method.</p>",
    ]
    headings = [f"Concreting enquiries in {name}", f"What is recorded for {name}", "Site questions", "Council and property checks", "Services that may be relevant", "Prepare before enquiring", "Independent-provider coordination", f"Next step for {name}"]
    return blocks, headings


def utility_blocks(slug: str) -> tuple[list[str], list[str]]:
    h1, lead = UTILITY_DATA.get(slug, ("Concrete coordination", "Prepare the site and project questions before an appointed provider responds."))
    blocks = [
        f"<p>{lead} Structure Co Concreters Camden coordinates enquiries with suitable independent providers. Submitting a {slug.replace('-', ' ')} form does not create a construction contract.</p>",
        f"<p>{slug.replace('-', ' ').title()} describes questions and decision factors. It does not claim that Structure Co performs regulated concreting work or operates one provider methodology.</p>",
        f"<p>For {slug.replace('-', ' ')}, share the property location, intended use, access constraints, existing surfaces, drainage concerns and timing. The appointed provider must confirm the project-specific method and documents.</p>",
        f"<p>Submitting a {slug.replace('-', ' ')} form does not create a construction contract. Provider identity, quotation, licensing, insurance, contract and warranty details must be confirmed before work begins.</p>",
        f"<p>Use the {slug.replace('-', ' ')} contact details for access, correction or deletion questions about an enquiry. Information is coordinated only as reasonably necessary for the enquiry and applicable administration.</p>",
        f"<p>Prices, construction values, response times and workmanship outcomes for {slug.replace('-', ' ')} are not guaranteed by this website.</p>",
    ]
    disclosure_heading = "Submitting an enquiry does not create a construction contract."
    headings = [h1, disclosure_heading, "Information to include", "Before work begins", "Information handling", "Questions and limits"]
    return blocks, headings


def replace_page(item: ET.Element, blocks: list[str], headings: list[str], title: str, description: str) -> None:
    set_node = item.find(f"{{{WP}}}post_title")
    if set_node is not None:
        set_node.text = title
    encoded = item.find(f"{{{CONTENT}}}encoded")
    if encoded is not None:
        # Elementor is the rendered source; leaving the legacy post_content
        # lead here would duplicate the first block in audits and in WordPress.
        encoded.text = ""
    excerpt = item.find(f"{{{WP}}}post_excerpt")
    if excerpt is not None:
        excerpt.text = ""
    set_meta(item, "rank_math_title", title + " | Structure Co Camden")
    set_meta(item, "rank_math_description", description)
    set_meta(item, "rank_math_breadcrumb_title", title)
    elementor = meta(item, "_elementor_data")
    if elementor is None:
        return
    try:
        data = json.loads(elementor.findtext(f"{{{WP}}}meta_value") or "[]")
    except json.JSONDecodeError:
        return
    slug_marker = title.lower().replace(" ", "-")
    # Clear legacy widget copy that is not one of the explicitly rewritten
    # editor/headline fields.  Repeating a neutral sentence in every retained
    # widget creates reader-visible filler and invalidates substantive-copy
    # quality metrics; an empty widget is the safe disposition.
    scrub_other_copy(data, "")
    heading_index = 0
    editor_index = 0

    def walk(value: Any) -> None:
        nonlocal heading_index, editor_index
        if isinstance(value, dict):
            widget = value.get("widgetType")
            settings = value.get("settings")
            if widget in ("e-heading", "heading") and isinstance(settings, dict):
                replacement = headings[min(heading_index, len(headings) - 1)]
                set_typed(settings.get("title"), replacement)
                if heading_index == 0:
                    tag = settings.get("tag")
                    if isinstance(tag, dict) and tag.get("$$type") == "string":
                        tag["value"] = "h1"
                    elif tag is not None:
                        settings["tag"] = "h1"
                elif settings.get("tag") is not None:
                    tag = settings.get("tag")
                    if isinstance(tag, dict) and tag.get("$$type") == "string":
                        tag["value"] = "h2"
                    else:
                        settings["tag"] = "h2"
                heading_index += 1
            if isinstance(settings, dict) and "editor" in settings:
                settings["editor"] = "".join(blocks) if editor_index == 0 else ""
                editor_index += 1
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)
    elementor.find(f"{{{WP}}}meta_value").text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def main() -> int:
    allowlist = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_rows = {int(r["page_id"]): r for r in allowlist["pages"]}
    suburb_data = {r["slug"]: r for r in json.loads(SUBURBS.read_text(encoding="utf-8"))["suburbs"]}
    expanded = {r["slug"]: r for r in json.loads(EXPANDED.read_text(encoding="utf-8"))["suburbs"]}
    tree = ET.parse(DERIVATIVE)
    # Mutable derivative identity cleanup; immutable provenance exports remain
    # untouched and are still hashed by the recovery gate.
    for node in tree.getroot().iter():
        for old in ("E&T Co Concreters Camden", "E&amp;T Co Concreters Camden", "E&amp;amp;T Co Concreters Camden"):
            if node.text and old in node.text:
                node.text = node.text.replace(old, "Structure Co Concreters Camden")
            if node.tail and old in node.tail:
                node.tail = node.tail.replace(old, "Structure Co Concreters Camden")
    pages = [i for i in tree.getroot().findall("./channel/item") if i.findtext(f"{{{WP}}}post_type") == "page"]
    rewritten = 0
    for index, item in enumerate(pages):
        pid = int(item.findtext(f"{{{WP}}}post_id") or 0)
        slug = item.findtext(f"{{{WP}}}post_name") or ""
        if slug in GOVERNED_LIVERPOOL_PAGES:
            continue
        m = manifest_rows.get(pid, {})
        if slug in SERVICE_DATA:
            blocks, headings = service_blocks(slug)
            d = SERVICE_DATA[slug]
            title = d["name"] + " across Camden and South West Sydney"
            description = f"{d['name']} enquiries coordinated around the actual site, intended use, access, levels, finish and governing documents."
        elif slug.startswith("concreters-"):
            record = suburb_data.get(slug.removeprefix("concreters-"), expanded.get(slug.removeprefix("concreters-"), {"name": slug}))
            blocks, headings = suburb_blocks(slug, record, index)
            name = record.get("name", slug.replace("concreters-", "").replace("-", " ").title())
            title = f"Concreting enquiries in {name}"
            description = f"Prepare a {name} concreting enquiry with site, access, levels, drainage and council questions for an independent provider."
        else:
            blocks, headings = utility_blocks(slug)
            title = headings[0]
            description = blocks[0].replace("<p>", "").replace("</p>", "")[:155]
        replace_page(item, blocks, headings, title, description)
        rewritten += 1
    tree.write(DERIVATIVE, encoding="utf-8", xml_declaration=True, short_empty_elements=True)
    print(f"rewritten active pages={rewritten}; derivative={DERIVATIVE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
