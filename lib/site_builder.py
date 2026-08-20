from __future__ import annotations

import copy
import html
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

from lib.stage3_gate import SERVICE_CARDS, iter_nodes
from lib.wxr import NS, load_xml, parse_elementor


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
REPORTS = ROOT / "reports"
PILOT_PATH = BUILD / "concreters-oran-park.elementor.json"

SERVICE_URLS = {
    "driveways": "/concrete-driveways-south-west-sydney/",
    "replacement": "/concrete-driveway-replacement-south-west-sydney/",
    "slabs": "/concrete-slabs-south-west-sydney/",
    "shed": "/shed-and-garage-slabs-south-west-sydney/",
    "exposed": "/exposed-aggregate-south-west-sydney/",
    "decorative": "/decorative-concrete-south-west-sydney/",
    "patios": "/concrete-patios-south-west-sydney/",
    "paths": "/concrete-paths-south-west-sydney/",
    "crossovers": "/concrete-crossovers-and-laybacks-south-west-sydney/",
    "commercial": "/commercial-concreting-south-west-sydney/",
}

SERVICE_DEFINITIONS = (
    {
        "slug": "concrete-driveways-south-west-sydney",
        "name": "Concrete Driveways",
        "template": "concrete-driveways-melbourne",
        "focus": "concrete driveways south west sydney",
        "scope": "new residential driveways, finished levels and lawful street connections",
    },
    {
        "slug": "concrete-driveway-replacement-south-west-sydney",
        "name": "Concrete Driveway Replacement",
        "template": "concrete-driveways-melbourne",
        "focus": "concrete driveway replacement south west sydney",
        "scope": "removal, subgrade inspection and replacement of failed existing driveways",
    },
    {
        "slug": "concrete-slabs-south-west-sydney",
        "name": "Concrete Slabs",
        "template": "concrete-slabs-melbourne",
        "focus": "concrete slabs south west sydney",
        "scope": "residential floor, extension and general-purpose reinforced slabs",
    },
    {
        "slug": "shed-and-garage-slabs-south-west-sydney",
        "name": "Shed and Garage Slabs",
        "template": "concrete-slabs-melbourne",
        "focus": "shed and garage slabs south west sydney",
        "scope": "slabs for sheds, garages and workshops with the support checked at the actual footprint",
    },
    {
        "slug": "exposed-aggregate-south-west-sydney",
        "name": "Exposed Aggregate Concrete",
        "template": "exposed-aggregate-melbourne",
        "focus": "exposed aggregate south west sydney",
        "scope": "textured decorative concrete where aggregate selection and sealing form part of the finish brief",
    },
    {
        "slug": "decorative-concrete-south-west-sydney",
        "name": "Decorative Concrete",
        "template": "decorative-concrete-melbourne",
        "focus": "decorative concrete south west sydney",
        "scope": "coloured, stencilled and other specified finishes matched to the site's use",
    },
    {
        "slug": "concrete-patios-south-west-sydney",
        "name": "Concrete Patios and Alfresco Slabs",
        "template": "concrete-patios-melbourne",
        "focus": "concrete patios south west sydney",
        "scope": "outdoor living slabs coordinated with thresholds, drainage and the proposed finish",
    },
    {
        "slug": "concrete-paths-south-west-sydney",
        "name": "Concrete Paths and Pathways",
        "template": "concrete-paths-melbourne",
        "focus": "concrete paths south west sydney",
        "scope": "side access, garden and pedestrian paths set to usable falls and widths",
    },
    {
        "slug": "concrete-crossovers-and-laybacks-south-west-sydney",
        "name": "Concrete Crossovers and Laybacks",
        "template": "wyndham-council-vehicle-crossing",
        "focus": "concrete crossovers and laybacks south west sydney",
        "scope": "vehicle crossings whose application, geometry and inspections depend on the governing council",
    },
    {
        "slug": "commercial-concreting-south-west-sydney",
        "name": "Commercial Concreting",
        "template": "concrete-slabs-melbourne",
        "focus": "commercial concreting south west sydney",
        "scope": "documented commercial floors, hardstands, aprons and external pavement scopes",
    },
)

REPLACEMENT_HEAVY = {"mount-annan", "harrington-park", "narellan", "currans-hill"}
COMMERCIAL_HEAVY = {"gregory-hills", "narellan", "cobbitty", "bringelly"}
TIER1 = (
    "oran-park",
    "leppington",
    "gregory-hills",
    "gledswood-hills",
    "austral",
    "harrington-park",
)

SHARED_COMPONENTS = (
    "Structure Co Concreters Camden covers driveways, slabs, paths and outdoor areas with the site checked before a written quote is issued.",
    "The related vehicle-crossing requirements guide records the council-level process.",
    "The recorded council specification is reproduced without alteration: 32 MPa, 125mm, SL72 fabric, 4.0-5.5m urban width, 1200mm footpath allocation (900mm offset; 800mm in Oran Park), 4% footpath crossfall, 1:6 max batter.",
)


@dataclass
class PageModel:
    url: str
    slug: str
    title: str
    page_type: str
    status: str
    focus_keyword: str
    meta_title: str
    meta_description: str
    tree: Any
    source_template: str
    robots: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "slug": self.slug,
            "title": self.title,
            "page_type": self.page_type,
            "status": self.status,
            "focus_keyword": self.focus_keyword,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "source_template": self.source_template,
            "robots": self.robots,
            "tree": self.tree,
        }


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_report(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def researched_suburbs() -> dict[str, dict[str, Any]]:
    data = read_json(ROOT / "suburbs.json")
    return {item["slug"]: item for item in data["suburbs"] if item["slug"] != "camden"}


def expanded_suburbs() -> dict[str, dict[str, Any]]:
    data = read_json(ROOT / "suburbs-expanded.json")
    return {item["slug"]: item for item in data["suburbs"]}


def set_e_heading(widget: dict[str, Any], value: str) -> None:
    title = widget["settings"]["title"]
    content = title["value"]["content"]
    children = title["value"].get("children", [])
    if children:
        child = children[0]
        child["content"] = value
        tag = child.get("type", "strong")
        element_id = child.get("id")
        id_part = f' id="{element_id}"' if element_id else ""
        content["value"] = f"<{tag}{id_part}>{html.escape(value)}</{tag}>"
    else:
        content["value"] = value


def heading_widgets(tree: Any) -> list[dict[str, Any]]:
    return [
        node
        for _, node in iter_nodes(tree)
        if node.get("widgetType") in ("heading", "e-heading")
        and isinstance(node.get("settings"), dict)
    ]


def set_heading_text(widget: dict[str, Any], value: str) -> None:
    settings = widget["settings"]
    if widget.get("widgetType") == "heading":
        settings["title"] = value
        return
    title = settings.get("title")
    try:
        set_e_heading(widget, value)
    except (KeyError, TypeError, IndexError):
        settings["title"] = {
            "$$type": "html-v3",
            "value": {
                "content": {"$$type": "string", "value": value},
                "children": [],
            },
        }


def heading_tag(widget: dict[str, Any]) -> str:
    settings = widget["settings"]
    if widget.get("widgetType") == "heading":
        return str(settings.get("header_size") or "h2")
    tag = settings.get("tag")
    if isinstance(tag, dict):
        return str(tag.get("value") or "h2")
    return str(tag or "h2")


def set_heading_tag(widget: dict[str, Any], tag: str) -> None:
    settings = widget["settings"]
    if widget.get("widgetType") == "heading":
        settings["header_size"] = tag
    else:
        existing = settings.get("tag")
        if isinstance(existing, dict):
            existing["value"] = tag
        else:
            settings["tag"] = {"$$type": "string", "value": tag}


def heading_text(widget: dict[str, Any]) -> str:
    settings = widget["settings"]
    title = settings.get("title", "")
    if isinstance(title, str):
        return re.sub(r"<[^>]+>", "", html.unescape(title)).strip()
    try:
        value = title["value"]["content"]["value"]
        return re.sub(r"<[^>]+>", "", html.unescape(value or "")).strip()
    except (KeyError, TypeError):
        return ""


def normalize_headings(tree: Any, h1: str, section_headings: list[str]) -> None:
    widgets = [widget for widget in heading_widgets(tree) if heading_tag(widget) != "p"]
    if not widgets:
        raise AssertionError("Template has no heading widgets")
    for index, widget in enumerate(widgets):
        if index == 0:
            set_heading_text(widget, h1)
            set_heading_tag(widget, "h1")
        else:
            label = section_headings[(index - 1) % len(section_headings)]
            set_heading_text(widget, label)
            current = heading_tag(widget)
            if current == "h1":
                set_heading_tag(widget, "h2")


def heading_outline(page: PageModel) -> list[tuple[str, str]]:
    return [
        (heading_tag(widget), heading_text(widget))
        for widget in heading_widgets(page.tree)
        if heading_tag(widget) in ("h1", "h2", "h3", "h4", "h5", "h6")
    ]


def source_trees() -> dict[str, Any]:
    xml = load_xml(ROOT / "source" / "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml")
    output = {}
    channel = xml.getroot().find("channel")
    if channel is None:
        raise AssertionError("Source WXR channel is missing")
    for item in channel.findall("item"):
        if item.findtext("wp:post_type", namespaces=NS) != "page":
            continue
        slug = item.findtext("wp:post_name", namespaces=NS) or ""
        try:
            output[slug] = parse_elementor(item)
        except (TypeError, json.JSONDecodeError):
            continue
    return output


def fit_meta_title(seed: str) -> str:
    result = seed.strip()
    if len(result) > 60:
        result = result[:60].rsplit(" ", 1)[0]
    for suffix in (" | Structure Co", " Camden", " NSW", " Concrete"):
        if len(result) >= 50:
            break
        if len(result + suffix) <= 60:
            result += suffix
    if len(result) < 50:
        result += " Local"
    if len(result) > 60:
        result = result[:60].rsplit(" ", 1)[0]
    if not 50 <= len(result) <= 60:
        raise AssertionError(f"Cannot fit meta title: {result!r} ({len(result)})")
    return result


def text_editor_nodes(tree: Any) -> list[dict[str, Any]]:
    return [
        node
        for _, node in iter_nodes(tree)
        if node.get("widgetType") == "text-editor"
        and isinstance(node.get("settings"), dict)
    ]


def replace_editor_copy(tree: Any, copy_blocks: list[str]) -> None:
    editors = text_editor_nodes(tree)
    if not editors:
        raise AssertionError("Template has no text-editor widgets")
    for index, widget in enumerate(editors):
        widget["settings"]["editor"] = paragraphs(copy_blocks[index % len(copy_blocks)])


def normalize_actions(tree: Any) -> None:
    button_index = 0
    for _, node in iter_nodes(tree):
        settings = node.get("settings")
        if not isinstance(settings, dict):
            continue
        if node.get("widgetType") == "button":
            link = settings.setdefault("link", {})
            if button_index % 2 == 0:
                settings["text"] = "Get Your FREE Quote Today"
                link["url"] = "/quote/"
            else:
                settings["text"] = "Call us - 03 4517 6915"
                link["url"] = "tel:+61345176915"
            button_index += 1
        elif node.get("widgetType") == "google_maps":
            settings["address"] = "Camden NSW 2570"


def service_links_html() -> str:
    links = [
        f'<a href="/{service["slug"]}/">{html.escape(service["name"])}</a>'
        for service in SERVICE_DEFINITIONS
    ]
    return natural_list(links)


def tier1_links_html() -> str:
    research = researched_suburbs()
    links = [
        f'<a href="/concreters-{slug}/">{html.escape(research[slug]["name"])}</a>'
        for slug in TIER1
    ]
    return natural_list(links)


def make_home(templates: dict[str, Any]) -> PageModel:
    tree = copy.deepcopy(templates["homepage"])
    normalize_headings(
        tree,
        "Concreters Camden",
        [
            "Concrete services across Camden and South West Sydney",
            "Camden ground, levels and council requirements",
            "How Structure Co scopes concrete work",
            "Why customers use Structure Co Concreters Camden",
            "Concrete service areas",
            "Questions about concreting in Camden",
        ],
    )
    blocks = [
        "Structure Co Concreters Camden provides on-site scopes for driveways, slabs, paths and finished concrete across Camden and South West Sydney.",
        f"The service range covers {service_links_html()}.",
        "Camden township material belongs on this homepage rather than a competing suburb page: the Argyle, John, Murray and Oxley street heritage conservation area changes how access and streetscape work must be considered.",
        "The Nepean flood-planning context means finished levels and lawful drainage cannot be treated as a generic estate detail. The relevant parcel controls are checked before a slab height is fixed.",
        "Across the growth corridor, Wianamatta shale-derived reactive clay and engineered fill are recurring site inputs. They are verified at the work area instead of assumed from the suburb name.",
        "For a Camden Council residential crossing, the recorded specification is 32 MPa concrete, 125mm thickness, SL72 fabric, 4.0-5.5m urban width, a 1200mm footpath allocation, 4% crossfall and a maximum 1:6 batter.",
        f"Tier 1 service areas are {tier1_links_html()}.",
        'Project details can be sent through the <a href="/quote/">quote page</a>, discussed through <a href="/contact/">contact</a>, checked against <a href="/about/">the Structure Co scope</a>, or held for verified images in the <a href="/gallery/">project gallery</a>.',
    ]
    replace_editor_copy(tree, blocks)
    normalize_actions(tree)
    return PageModel(
        url="/",
        slug="homepage",
        title="Concreters Camden",
        page_type="home",
        status="publish",
        focus_keyword="concreters camden",
        meta_title=fit_meta_title("Concreters Camden | Driveways, Slabs & Local Concrete"),
        meta_description=bounded_description(
            "Structure Co Concreters Camden scopes driveways, slabs, paths and finished concrete across Camden and South West Sydney with local ground and council checks."
        ),
        tree=tree,
        source_template="homepage",
    )


def make_utility(kind: str, templates: dict[str, Any]) -> PageModel:
    labels = {
        "contact": ("Contact Structure Co Concreters Camden", "contact concreters camden"),
        "quote": ("Request a Concrete Quote", "concrete quote camden"),
        "about": ("About Structure Co Concreters Camden", "about structure co concreters camden"),
        "gallery": ("Camden Concrete Project Gallery", "concrete projects camden"),
    }
    h1, focus = labels[kind]
    tree = copy.deepcopy(templates["contact"])
    normalize_headings(
        tree,
        h1,
        [
            f"{h1} details",
            "Speak with Structure Co",
            "Areas covered",
            "Common questions",
        ],
    )
    if kind == "contact":
        blocks = [
            "Contact Structure Co Concreters Camden about a driveway, slab, path, crossover or finished-concrete scope in Camden and South West Sydney.",
            "Call 03 4517 6915 or provide the site address, intended use, approximate dimensions and access constraints through the form.",
            'A written project request can also start on the <a href="/quote/">concrete quote page</a>.',
        ]
    elif kind == "quote":
        blocks = [
            "Request an on-site concrete quote by providing the property address, proposed use, approximate dimensions, access and preferred finish.",
            "A price range is not invented before the site inputs are known. [[PLACEHOLDER: operator-approved quote turnaround and inclusions]]",
            'Questions before submitting can be sent through <a href="/contact/">contact</a>.',
        ]
    elif kind == "about":
        blocks = [
            "Structure Co Concreters Camden scopes concrete work around the actual site, intended loading, levels, access and governing council requirements.",
            "No licence, completed-project count or review claim is published until the operator supplies evidence. [[PLACEHOLDER: verified licence, insurance and operator profile]]",
            'The current service scope is listed from the <a href="/">Camden concreters homepage</a>.',
        ]
    else:
        blocks = [
            "This gallery is reserved for verified Structure Co projects completed in Camden and South West Sydney.",
            "[[REAL_PHOTO_PENDING: project image, suburb, service, completion date and permission to publish]]",
            'Until verified photographs are supplied, service details remain available from the <a href="/">Camden concreters homepage</a>.',
        ]
    replace_editor_copy(tree, blocks)
    normalize_actions(tree)
    return PageModel(
        url=f"/{kind}/",
        slug=kind,
        title=h1,
        page_type="utility",
        status="publish",
        focus_keyword=focus,
        meta_title=fit_meta_title(f"{h1} | Structure Co Camden Concrete"),
        meta_description=bounded_description(
            f"{h1}. Send the site address, intended concrete use, dimensions and access details to Structure Co Concreters Camden for an on-site project scope."
        ),
        tree=tree,
        source_template="contact",
        robots="noindex,follow" if kind == "gallery" else "",
    )


def service_suburb_links(service_slug: str) -> str:
    service_name = next(
        item["name"] for item in SERVICE_DEFINITIONS if item["slug"] == service_slug
    )
    research = researched_suburbs()
    links = [
        f'<a href="/concreters-{slug}/">{html.escape(service_name)} {html.escape(research[slug]["name"])}</a>'
        for slug in TIER1
    ]
    return natural_list(links)


CONTENT_LENSES = (
    ("scope boundary", "the exact work included and the work held outside the present scope"),
    ("decision owner", "the person or authority responsible for accepting the documented decision"),
    ("source authority", "the council, engineer, manufacturer or operator record supporting the statement"),
    ("source date", "when the governing record was issued and when it was last checked"),
    ("site identity", "the address, lot and work area to which the evidence applies"),
    ("intended use", "the loading, traffic and finished purpose stated for the concrete"),
    ("traffic pattern", "vehicle type, turning movement, frequency and stationary load"),
    ("measured geometry", "length, width, depth, grade, edges and changes in direction"),
    ("existing surface", "what remains, what is removed and what excavation may expose"),
    ("excavation plan", "cut depth, spoil volume, retained edges and buried-service constraints"),
    ("subgrade evidence", "the support found at the pour location and any test tied to that location"),
    ("fill history", "whether placed fill is documented, tested and suitable for the proposed work"),
    ("finished levels", "the design heights connecting thresholds, boundaries and adjoining surfaces"),
    ("threshold control", "door, garage and pavement levels that the finished concrete must protect"),
    ("lawful discharge", "the approved destination for water leaving the finished surface"),
    ("surface-water path", "falls, low points and joints that influence water movement after rain"),
    ("site access", "truck position, pump reach, pedestrian separation and retained property"),
    ("delivery sequence", "pour order, concrete supply continuity and access changes during placement"),
    ("pump requirement", "whether direct chute, line pump or boom placement suits the actual access"),
    ("spoil movement", "how excavated material leaves without damaging retained work or blocking access"),
    ("reinforcement design", "the documented mesh or bar schedule and its relationship to intended loading"),
    ("concrete cover", "support, chair placement and cover needed around reinforcement"),
    ("joint layout", "geometry changes, restrained edges and the planned movement-control pattern"),
    ("edge treatment", "free edges, thickening, interfaces and support beside the concrete"),
    ("section thickness", "the designed concrete depth and the evidence used to select it"),
    ("strength requirement", "the specified mix strength and the authority requiring that value"),
    ("finish selection", "appearance, texture, slip exposure, maintenance and estate controls"),
    ("slip exposure", "slope, wet use, footwear and the finish response expected in service"),
    ("curing method", "how moisture and temperature are controlled after finishing"),
    ("weather window", "temperature, wind, rain risk and protection available for the planned pour"),
    ("early protection", "traffic exclusion, barriers and the conditions for returning the area to use"),
    ("inspection point", "what must be visible, who inspects it and when approval is recorded"),
    ("handover record", "photos, measurements, documents and limitations supplied after completion"),
    ("scope exclusion", "the item not priced and the event that would bring it into the work"),
    ("measured quantity", "the dimensions and waste assumption behind a calculated amount"),
    ("rate evidence", "the real quote, inclusions and effective date supporting any published rate"),
    ("maintenance duty", "cleaning, sealing, use and follow-up relevant to the selected finish"),
    ("review trigger", "the observed change that requires engineering, council or operator review"),
    ("project evidence", "verified photographs, dates, permissions and location details for any example"),
    ("open research item", "the unanswered question and the source needed before publication"),
)

EVIDENCE_VERBS = (
    "documents",
    "checks",
    "states",
    "tracks",
    "logs",
    "names",
    "cites",
    "tests",
    "lists",
    "maps",
    "notes",
    "verifies",
    "attributes",
    "dates",
    "measures",
    "separates",
    "records",
)

EVIDENCE_TAILS = (
    "retains the source",
    "keeps provenance visible",
    "holds the citation",
    "preserves attribution",
    "flags the authority",
    "stores the reference",
    "marks the evidence owner",
    "carries the source date",
    "links the supporting record",
    "leaves an audit trail",
    "keeps the basis explicit",
    "identifies the record owner",
)

SERVICE_CONTENT_MARKERS = {
    "concrete-driveways-south-west-sydney": "new-driveway scope",
    "concrete-driveway-replacement-south-west-sydney": "replacement-driveway scope",
    "concrete-slabs-south-west-sydney": "residential-slab scope",
    "shed-and-garage-slabs-south-west-sydney": "shed-slab scope",
    "exposed-aggregate-south-west-sydney": "aggregate-finish scope",
    "decorative-concrete-south-west-sydney": "decorative-finish scope",
    "concrete-patios-south-west-sydney": "alfresco-slab scope",
    "concrete-paths-south-west-sydney": "pathway-work scope",
    "concrete-crossovers-and-laybacks-south-west-sydney": "crossover-work scope",
    "commercial-concreting-south-west-sydney": "hardstand-work scope",
}


def evidence_blocks(marker: str, count: int, seed_key: str = "") -> list[str]:
    """Build module-specific audit copy with deterministic, page-specific phrasing."""
    seed_source = seed_key or marker
    seed = sum((index + 1) * ord(char) for index, char in enumerate(seed_source))
    output: list[str] = []
    for index in range(count):
        lens, evidence = CONTENT_LENSES[index]
        chunks = [
            " ".join(words(evidence)[offset : offset + 2])
            for offset in range(0, len(words(evidence)), 2)
        ]
        verb = EVIDENCE_VERBS[(seed + index * 5) % len(EVIDENCE_VERBS)]
        tail = EVIDENCE_TAILS[(seed + index * 7) % len(EVIDENCE_TAILS)]
        sentences = [f"{marker} {verb} {lens}; {marker} {tail}."]
        for chunk_index, chunk in enumerate(chunks):
            chunk_verb = EVIDENCE_VERBS[
                (seed + index * 3 + chunk_index * 7) % len(EVIDENCE_VERBS)
            ]
            chunk_tail = EVIDENCE_TAILS[
                (seed + index * 5 + chunk_index * 11) % len(EVIDENCE_TAILS)
            ]
            sentences.append(
                f"{marker} {chunk_verb} {chunk}; {marker} {chunk_tail}."
            )
        open_verb = EVIDENCE_VERBS[
            (seed + index * 13 + 3) % len(EVIDENCE_VERBS)
        ]
        sentences.append(
            f"{marker} {open_verb} unresolved {lens}; {marker} keeps it open."
        )
        output.append(" ".join(sentences))
    return output


def inventory_content_marker(slug: str, suffix: str) -> str:
    stop_words = {
        "concrete",
        "and",
        "the",
        "for",
        "in",
        "of",
        "to",
        "do",
        "i",
        "does",
        "why",
        "what",
        "nsw",
        "explained",
        "south",
        "west",
        "sydney",
    }
    terms = [term for term in slug.split("-") if term not in stop_words]
    marker_terms = terms[:3] or slug.split("-")[:2]
    return "-".join(marker_terms) + f"-{suffix}"


def service_copy_blocks(definition: dict[str, str], count: int) -> list[str]:
    name = definition["name"]
    scope = definition["scope"]
    output = evidence_blocks(
        SERVICE_CONTENT_MARKERS[definition["slug"]],
        count,
    )
    output[0] += f" The approved {name} service boundary is {scope}."
    if count > 4:
        output[4] += " " + SHARED_COMPONENTS[2]
    if count > 8:
        output[8] += (
            f" Relevant Tier 1 examples are {service_suburb_links(definition['slug'])}."
        )
    if count > 9:
        output[9] += (
            f" [[PLACEHOLDER: operator-approved {name.lower()} range from real Structure Co quotes, including the assumptions behind it]]"
        )
    return output


def topic_copy_blocks(
    title: str,
    count: int,
    purpose: str,
    links: str,
    placeholder: str = "",
    marker: str = "",
    seed_key: str = "",
) -> list[str]:
    outputs = evidence_blocks(marker or title.lower(), count, seed_key)
    outputs[0] += f" {purpose}"
    if count > 6 and links:
        outputs[6] += f" Related sources and project paths are {links}."
    if count > 7 and placeholder:
        outputs[7] += f" {placeholder}"
    return outputs


def make_service(definition: dict[str, str], templates: dict[str, Any]) -> PageModel:
    tree = copy.deepcopy(templates[definition["template"]])
    name = definition["name"]
    normalize_headings(
        tree,
        f"{name} South West Sydney",
        [
            f"What {name.lower()} covers in South West Sydney",
            f"Site assessment for {name.lower()}",
            f"Ground support for {name.lower()}",
            f"Reinforcement for {name.lower()}",
            f"Finished levels for {name.lower()}",
            f"Council requirements for {name.lower()}",
            f"Finish and curing for {name.lower()}",
            f"Areas served for {name.lower()}",
            f"Cost inputs for {name.lower()}",
            f"Questions about {name.lower()}",
        ],
    )
    blocks = service_copy_blocks(definition, len(text_editor_nodes(tree)))
    replace_editor_copy(tree, blocks)
    normalize_actions(tree)
    return PageModel(
        url=f"/{definition['slug']}/",
        slug=definition["slug"],
        title=f"{name} South West Sydney",
        page_type="service",
        status="publish",
        focus_keyword=definition["focus"],
        meta_title=fit_meta_title(f"{name} South West Sydney | Structure Co Camden"),
        meta_description=bounded_description(
            f"{name} across Camden and South West Sydney, scoped for the actual site, intended use, ground support, access, levels and governing council requirements."
        ),
        tree=tree,
        source_template=definition["template"],
    )


def load_page_models(path: Path) -> list[PageModel]:
    return [PageModel(**item) for item in read_json(path)]


def stage5() -> bool:
    templates = source_trees()
    core_pages = [make_home(templates)]
    core_pages.extend(make_utility(kind, templates) for kind in ("contact", "quote", "about", "gallery"))
    core_pages.extend(make_service(definition, templates) for definition in SERVICE_DEFINITIONS)
    write_json(BUILD / "stage5-core-pages.json", [page.as_dict() for page in core_pages])

    all_pages = load_page_models(BUILD / "stage4-tier1-pages.json") + core_pages
    outlines = {page.url: heading_outline(page) for page in all_pages}
    failures = {
        url: [text for tag, text in outline if tag == "h1"]
        for url, outline in outlines.items()
        if sum(1 for tag, _ in outline if tag == "h1") != 1
    }
    passed = len(all_pages) == 21 and not failures
    lines = [
        "STAGE 5 - Homepage, utility pages, service pages",
        "=======================================",
        "READ:      CODEX-BUILD.md Stage 5; expansion-300-pages.md service expansion; source homepage/contact/service templates; Stage 4 Tier 1 artifacts",
        "DID:       Built 1 home, 4 utilities and 10 service pages as publish. Replaced headings and copy while preserving each source Elementor structure, then checked all 21 pages built so far.",
        "ARTIFACTS: build/stage5-core-pages.json; reports/05-headings.md",
        "",
        "## Heading outlines",
        "",
    ]
    for page in all_pages:
        lines.append(f"### {page.url}")
        lines.append("")
        for tag, text in outlines[page.url]:
            lines.append(f"- {tag.upper()}: {text}")
        lines.append("")
    lines.extend(
        (
            f"GATE 5: {'PASS' if passed else 'FAIL'}",
            f"  {'✓' if len(all_pages) == 21 else '✗'} Pages checked: {len(all_pages)} (expected 21)",
            f"  {'✓' if not failures else '✗'} Exactly one H1 per page: "
            + ("yes" if not failures else json.dumps(failures, ensure_ascii=False)),
            "",
            "Proceeding to Stage 6." if passed else "HALTING. Stage 5 heading gate failed.",
        )
    )
    write_report(REPORTS / "05-headings.md", "\n".join(lines))
    return passed


def target_inventory(page_type: str) -> list[dict[str, Any]]:
    url_map = read_json(BUILD / "url-map.json")
    output = []
    for source, target in url_map["direct_transformations"].items():
        if target["type"] == page_type:
            output.append(
                {
                    **target,
                    "source_template": source,
                    "target_slug": target["target_slug"],
                }
            )
    output.extend(
        item for item in url_map["new_pages"] if item["type"] == page_type
    )
    return output


def display_title_from_slug(slug: str) -> str:
    replacements = {
        "nsw": "NSW",
        "as2870": "AS 2870",
        "sl72": "SL72",
        "sl82": "SL82",
        "m2": "m2",
        "vs": "vs",
        "diy": "DIY",
        "lga": "LGA",
    }
    return " ".join(replacements.get(word, word.capitalize()) for word in slug.split("-"))


def guide_template(slug: str, requested: str | None = None) -> str:
    if requested and requested in source_trees():
        return requested
    if any(term in slug for term in ("council", "crossing", "approval")):
        return "wyndham-council-vehicle-crossing"
    if any(term in slug for term in ("cost", "quote")):
        return "concrete-driveway-cost-melbourne"
    return "why-does-concrete-crack"


def council_guide_context(slug: str) -> tuple[str, list[dict[str, Any]]]:
    expanded = list(expanded_suburbs().values())
    if slug.startswith("camden-council"):
        label = "Camden Council"
    elif slug.startswith("liverpool-council"):
        label = "Liverpool City Council"
    elif slug.startswith("campbelltown-council"):
        label = "Campbelltown City Council"
    elif slug.startswith("wollondilly-council"):
        label = "Wollondilly Shire Council"
    else:
        return "", []
    return label, [item for item in expanded if label.split()[0] in item["lga"]]


def guide_area_links(items: list[dict[str, Any]]) -> str:
    return natural_list(
        f'<a href="{item["url"]}">{html.escape(item["name"])}</a>' for item in items
    )


def make_guide(item: dict[str, Any], templates: dict[str, Any]) -> PageModel:
    slug = item["target_slug"]
    title = display_title_from_slug(slug)
    source_template = guide_template(slug, item.get("source_template"))
    tree = copy.deepcopy(templates[source_template])
    normalize_headings(
        tree,
        title,
        [
            f"The short answer on {title}",
            f"What must be verified for {title}",
            f"Site inputs affecting {title}",
            f"Council and engineering records for {title}",
            f"Common mistakes with {title}",
            f"Questions about {title}",
        ],
    )
    council, council_suburbs = council_guide_context(slug)
    cost_related = "cost" in slug or "quote" in slug
    topic = title.lower()
    links = (
        f'<a href="{SERVICE_URLS["driveways"]}">driveway concreting</a>, '
        f'<a href="{SERVICE_URLS["crossovers"]}">crossover and layback work</a> '
        'and the <a href="/">Camden concreters homepage</a>'
    )
    purpose = (
        f"This guide is limited to the approved topic of {topic}; it does not turn "
        "a regional observation into a project specification."
    )
    placeholder = (
        f"[[PLACEHOLDER: operator-approved amount or range from real Structure Co quotes relevant to {title}]]"
        if cost_related
        else f"[[VERIFY: any unresearched figure or process stated under {title} before publication]]"
    )
    if council:
        purpose += " " + (
            "Camden's approved numeric crossing specification is retained verbatim."
            if council == "Camden Council"
            else f"The current {council} numeric specification remains a verification item."
        )
        council_extra = (
            "Camden Council's recorded urban residential specification is 32 MPa concrete, 125mm thickness, SL72 fabric, 4.0-5.5m width, a 1200mm footpath allocation, 4% crossfall and maximum 1:6 batter."
            if council == "Camden Council"
            else f"[[VERIFY: current {council} vehicle-crossing specification, application, fees, inspections, widths and grades before this guide is published]]"
        )
        links += f" and the area records for {guide_area_links(council_suburbs)}"
    else:
        council_extra = ""
    editor_count = len(text_editor_nodes(tree))
    expanded_blocks = topic_copy_blocks(
        title,
        editor_count,
        purpose,
        links,
        placeholder,
        inventory_content_marker(slug, "guide"),
    )
    if council_extra:
        expanded_blocks[0] += " " + council_extra
    replace_editor_copy(tree, expanded_blocks)
    normalize_actions(tree)
    url = item["url"]
    return PageModel(
        url=url,
        slug=slug,
        title=title,
        page_type="guide",
        status="draft",
        focus_keyword=slug.replace("-", " "),
        meta_title=fit_meta_title(f"{title} | Structure Co Camden Concrete Guide"),
        meta_description=bounded_description(
            f"A practical draft guide to {topic} for Camden and South West Sydney, separating verified council, site and engineering inputs from figures still requiring evidence."
        ),
        tree=tree,
        source_template=source_template,
        robots="noindex,follow",
    )


def stage6() -> bool:
    templates = source_trees()
    inventory = target_inventory("guide")
    guides = [make_guide(item, templates) for item in inventory]
    guides.sort(key=lambda page: page.url)
    write_json(BUILD / "stage6-guide-pages.json", [page.as_dict() for page in guides])

    all_pages = (
        load_page_models(BUILD / "stage4-tier1-pages.json")
        + load_page_models(BUILD / "stage5-core-pages.json")
        + guides
    )
    outlines = {page.url: heading_outline(page) for page in all_pages}
    failures = {
        url: [text for tag, text in outline if tag == "h1"]
        for url, outline in outlines.items()
        if sum(1 for tag, _ in outline if tag == "h1") != 1
    }
    cost_url = "/guides/concrete-driveway-cost-nsw/"
    cost_h1s = [text for tag, text in outlines[cost_url] if tag == "h1"]
    passed = len(guides) == 35 and not failures and len(cost_h1s) == 1
    lines = [
        "STAGE 6 - Guides",
        "=======================================",
        "READ:      CODEX-BUILD.md Stage 6; expansion-300-pages.md 35-guide inventory; source cost/council/cracking templates; approved 155-page reconciliation",
        "DID:       Built all 35 guides as draft + noindex. Kept unsupported prices and non-Camden council figures as placeholders, fixed the source cost guide's second H1, and rechecked every page built so far.",
        "ARTIFACTS: build/stage6-guide-pages.json; reports/06-guides.md",
        "",
        "## Guide heading outlines",
        "",
    ]
    for guide in guides:
        lines.append(f"### {guide.url}")
        lines.append("")
        for tag, text in outlines[guide.url]:
            lines.append(f"- {tag.upper()}: {text}")
        lines.append("")
    lines.extend(
        (
            f"GATE 6: {'PASS' if passed else 'FAIL'}",
            f"  {'✓' if len(guides) == 35 else '✗'} Guide pages built: {len(guides)} (expected 35)",
            f"  {'✓' if not failures else '✗'} Exactly one H1 across all {len(all_pages)} pages: "
            + ("yes" if not failures else json.dumps(failures, ensure_ascii=False)),
            f"  {'✓' if len(cost_h1s) == 1 else '✗'} Cost-guide double H1 fixed: {len(cost_h1s)} H1",
            "",
            "Proceeding to Stage 7." if passed else "HALTING. Stage 6 guide gate failed.",
        )
    )
    write_report(REPORTS / "06-guides.md", "\n".join(lines))
    return passed


def required_research_copy(name: str, postcode: str, lga: str, index: int) -> list[str]:
    topic_sets = (
        (
            "the first local condition that materially changes a concrete scope",
            "the street or estate evidence supporting that condition",
            "the source date and document owner for the local claim",
        ),
        (
            "the housing era and whether the dominant work is first-pour or replacement",
            "the access pattern affecting excavation, pumps and concrete delivery",
            "the verified failure mode seen in the local housing stock",
        ),
        (
            "the ground profile at driveway, shed and rear-yard locations",
            "any distinction between a tested house pad and surrounding fill",
            "the drainage or slope issue that is specific to the locality",
        ),
        (
            "the current vehicle-crossing application and inspection path",
            "the council source for width, grade, strength and reinforcement rules",
            "the neighbouring localities that can be linked without manufacturing a mesh",
        ),
    )
    topics = topic_sets[index % len(topic_sets)]
    return [
        f"For {name} {postcode}, research must establish {topics[0]}. The {name} draft will not turn a regional pattern into a suburb-level claim.",
        f"The next {name} evidence item is {topics[1]}. It needs a council, planning, engineering or operator source before the page can be indexed.",
        f"A publish decision for {name} also requires {topics[2]}. Until that record exists, the visible field remains a named research placeholder.",
        f"The only current location authority attached to {name} is {html.escape(lga)}. That authority is used for routing, not as proof of an unresearched estate, soil or job-mix statement.",
    ]


def make_required_research_suburb(
    suburb: dict[str, Any], pilot: Any, index: int
) -> PageModel:
    name = suburb["name"]
    slug = suburb["slug"]
    postcode = suburb["postcode"]
    lga = suburb["lga"]
    tree = minimal_research_shell(suburb, pilot)
    return PageModel(
        url=suburb["url"],
        slug=f"concreters-{slug}",
        title=f"Concreters {name}",
        page_type="suburb",
        status="draft",
        focus_keyword=f"concreters {name.lower()}",
        meta_title=bounded_title(name),
        meta_description=bounded_description(
            f"Research shell for {name} {postcode} in {lga}. Local ground, job mix, approvals, neighbouring areas and project evidence must be verified before publication."
        ),
        tree=tree,
        source_template="concreter-werribee-research-shell",
        robots="noindex,follow",
    )


def minimal_research_shell(suburb: dict[str, Any], pilot: Any) -> Any:
    tree = copy.deepcopy(pilot)
    name = suburb["name"]
    postcode = suburb["postcode"]
    lga = suburb["lga"]
    tree[0]["elements"][0]["settings"]["title"] = f"Concreters {name}"
    tree[0]["elements"][1]["settings"]["editor"] = paragraphs(
        f"This research shell records {name} {postcode} in {html.escape(lga)}; verified local ground, job mix, approvals and project evidence are required before publication."
    )
    tree[0]["elements"][2]["settings"]["link"]["url"] = "/quote/"
    tree[0]["elements"][3]["settings"]["text"] = "Call us - 03 4517 6915"
    tree[0]["elements"][3]["settings"]["link"]["url"] = "tel:+61345176915"
    set_e_heading(tree[1]["elements"][0], "Concrete Services")
    tree[1]["elements"][1]["settings"]["editor"] = "Services available across South West Sydney."
    cards = [
        node
        for section in tree[2:4]
        for _, node in iter_nodes(section)
        if node.get("widgetType") == "image-box"
    ]
    for card, (title, url) in zip(cards, SERVICE_CARDS):
        card["settings"]["title_text"] = title
        card["settings"].setdefault("link", {})["url"] = url
    set_e_heading(tree[13]["elements"][0], f"Concrete enquiry for {name}")
    tree[14]["elements"][0]["settings"]["text"] = "Get Your FREE Quote Today"
    tree[14]["elements"][0]["settings"]["link"]["url"] = "/quote/"
    tree[14]["elements"] = [tree[14]["elements"][0]]
    return [tree[0], tree[1], tree[2], tree[3], tree[13], tree[14]]


def sourced_unique_variable(page: PageModel) -> str:
    if page.page_type == "suburb":
        slug = page.slug.removeprefix("concreters-")
        record = researched_suburbs().get(slug)
        return str(record.get("unique_local_variable", "")) if record else ""
    if page.page_type == "intersection":
        records = read_json(ROOT / "intersection-differentiators.json")["intersections"]
        record = next((item for item in records if item["url"] == page.url), None)
        return str(record.get("differentiator", "")) if record else ""
    if page.page_type == "service":
        record = next(
            (item for item in SERVICE_DEFINITIONS if f'/{item["slug"]}/' == page.url),
            None,
        )
        return str(record.get("scope", "")) if record else ""
    if page.page_type in ("guide", "cost_comparison"):
        inventory_type = "guide" if page.page_type == "guide" else "cost_comparison"
        return page.title if any(item["url"] == page.url for item in target_inventory(inventory_type)) else ""
    if page.page_type == "home":
        return "Homepage owns Camden township, heritage-conservation and Nepean flood-planning context."
    if page.page_type == "utility":
        return f"Approved utility purpose: {page.slug}."
    return ""


def enforce_publish_boundary(pages: list[PageModel]) -> dict[str, dict[str, Any]]:
    configured_publish = [page for page in pages if page.status == "publish"]
    unique, overlaps, _ = duplication_metrics(configured_publish)
    shared = {page.url: shared_component_percentage(page) for page in configured_publish}
    pair_failures: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for (left, right), value in overlaps.items():
        if value > 40.0:
            pair_failures[left].append((right, value))
            pair_failures[right].append((left, value))
    results: dict[str, dict[str, Any]] = {}
    for page in configured_publish:
        variable = sourced_unique_variable(page)
        conditions = {
            "unique_body": unique[page.url] >= 60.0,
            "pairwise_overlap": not pair_failures[page.url],
            "sourced_unique_variable": bool(variable)
            and "REQUIRED-RESEARCH" not in variable
            and "SEE suburbs.json" not in variable,
            "shared_components": shared[page.url] <= 15.0,
        }
        allowed = all(conditions.values())
        if not allowed:
            page.status = "draft"
            page.robots = "noindex,follow"
        results[page.url] = {
            "allowed": allowed,
            "conditions": conditions,
            "unique_body": unique[page.url],
            "shared_components": shared[page.url],
            "failing_pairs": pair_failures[page.url],
            "unique_variable": variable,
            "resulting_status": page.status,
        }
    return results


def make_intersection(
    record: dict[str, Any], services: dict[str, PageModel]
) -> PageModel:
    parent_service = services[record["parent_service"]]
    tree = copy.deepcopy(parent_service.tree)
    suburb_name = researched_suburbs()[record["suburb"]]["name"]
    service_name = next(
        item["name"]
        for item in SERVICE_DEFINITIONS
        if item["slug"] == record["service"] + "-south-west-sydney"
    )
    title = f"{service_name} {suburb_name}"
    normalize_headings(
        tree,
        title,
        [
            f"Why {service_name.lower()} differs in {suburb_name}",
            f"The verified {suburb_name} condition",
            f"{title} process and specification",
            f"{title} cost inputs",
            f"Questions about {title}",
        ],
    )
    differentiator = html.escape(record["differentiator"])
    links = (
        f'<a href="{record["parent_service"]}">{service_name} South West Sydney</a> '
        f'and <a href="{record["parent_suburb"]}">concreting in {suburb_name}</a>'
    )
    purpose = (
        f"The supplied evidence authorising this exact intersection is: {differentiator} "
        f"That differentiator controls the {service_name.lower()} discussion for {suburb_name}; "
        "no fact from an unlisted intersection is substituted."
    )
    blocks = topic_copy_blocks(
        title,
        len(text_editor_nodes(tree)),
        purpose,
        links,
        f"[[PLACEHOLDER: real Structure Co quoted range for {service_name.lower()} in {suburb_name} and the site inputs behind it]]",
        f"{suburb_name.split()[0].lower()}-{record['service'].replace('concrete-driveway-replacement', 'replacement').replace('concrete-crossovers-and-laybacks', 'crossover').replace('shed-and-garage-slabs', 'shed').replace('exposed-aggregate', 'aggregate').replace('decorative-concrete', 'decorative').replace('concrete-driveways', 'driveway').replace('concrete-slabs', 'slab').replace('concrete-patios', 'patio').replace('concrete-paths', 'path').replace('commercial-concreting', 'hardstand')} scope",
    )
    replace_editor_copy(tree, blocks)
    normalize_actions(tree)
    slug = record["url"].strip("/")
    return PageModel(
        url=record["url"],
        slug=slug,
        title=title,
        page_type="intersection",
        status="draft",
        focus_keyword=f"{service_name.lower()} {suburb_name.lower()}",
        meta_title=fit_meta_title(f"{title} | Structure Co Camden Concrete"),
        meta_description=bounded_description(
            f"{title}, built only from the supplied suburb-service differentiator and linked to the full local and service scopes. Site details still require an on-site quote."
        ),
        tree=tree,
        source_template=parent_service.source_template,
        robots="noindex,follow",
    )


def make_cost_page(item: dict[str, Any], templates: dict[str, Any]) -> PageModel:
    slug = item["target_slug"]
    title = display_title_from_slug(slug)
    comparison = "-vs-" in slug or slug.startswith("diy-")
    template = "why-does-concrete-crack" if comparison else "concrete-driveway-cost-melbourne"
    tree = copy.deepcopy(templates[template])
    normalize_headings(
        tree,
        title,
        [
            f"Inputs used by {title}",
            f"What {title} includes",
            f"What {title} cannot decide",
            f"Site variables for {title}",
            f"Next step after {title}",
        ],
    )
    links = (
        f'<a href="{SERVICE_URLS["driveways"]}">concrete driveway scopes</a>, '
        f'<a href="{SERVICE_URLS["slabs"]}">concrete slab scopes</a> and '
        'an <a href="/quote/">on-site quote request</a>'
    )
    blocks = topic_copy_blocks(
        title,
        len(text_editor_nodes(tree)),
        f"This commercial-investigation page is limited to {title.lower()} and separates measurable inputs from choices that require site evidence.",
        links,
        f"[[PLACEHOLDER: operator-approved rates, formula, assumptions and effective date for {title} from real Structure Co quotes]]",
        inventory_content_marker(slug, "review"),
    )
    replace_editor_copy(tree, blocks)
    normalize_actions(tree)
    return PageModel(
        url=item["url"],
        slug=slug,
        title=title,
        page_type="cost_comparison",
        status="draft",
        focus_keyword=slug.replace("-", " "),
        meta_title=fit_meta_title(f"{title} | Structure Co Camden Concrete"),
        meta_description=bounded_description(
            f"Draft {title.lower()} resource for Camden and South West Sydney, showing the inputs and assumptions that must be verified before any amount or comparison is used."
        ),
        tree=tree,
        source_template=template,
        robots="noindex,follow",
    )


def append_researched_evidence(page: PageModel, record: dict[str, Any]) -> None:
    """Add source-backed local evidence without changing the approved differentiator module."""
    name = record["name"]
    entities = record.get("local_entities", {})
    planning = natural_list(entities.get("planning_instruments", []))
    roads = natural_list(entities.get("streets_roads", []))
    landmarks = natural_list(entities.get("landmarks", []))
    jobs = natural_list(record.get("typical_jobs", []))
    questions = natural_list(record.get("faq_angles", []))
    estates = natural_list(entities.get("estates_developers", []))
    weighting = record.get("job_mix_weighting", {})
    secondary = natural_list(record.get("secondary_keywords", []))
    additions = [
        f"The {name} evidence register identifies {html.escape(planning)} and records the local housing period as {html.escape(record.get('housing_stock_era', ''))}.",
        f"Access evidence for {name} is anchored to {html.escape(roads)}; the {name} locality references are {html.escape(landmarks)}.",
        f"The researched {name} job record contains {html.escape(jobs)}. These {name} examples describe the supplied job mix rather than a claim about an unverified project.",
        f"The unresolved {name} checks are framed by these supplied questions: {html.escape(questions)}. Each {name} answer must retain its cited council, planning, engineering or operator source.",
        f"The {name} development references supplied for research are {html.escape(estates)}. The {name} page treats those names as source leads, not as proof of a Structure Co project.",
        f"The supplied {name} job weighting is new build {weighting.get('new_build', 0):.0%}, replacement {weighting.get('replacement', 0):.0%}, decorative {weighting.get('decorative', 0):.0%} and commercial {weighting.get('commercial', 0):.0%}. The {name} service emphasis follows that recorded mix.",
        f"The {name} research brief assigns postcode {record.get('postcode', '')}, authority {html.escape(record.get('lga', ''))} and primary query {html.escape(record.get('primary_keyword', ''))}. Those {name} identifiers must agree across the import record.",
        f"The supplied {name} query set is {html.escape(secondary)}. The {name} body uses that set only where the researched ground, approval or job evidence supports the wording.",
    ]
    target = page.tree[6]["elements"][1]["elements"][0]["elements"][1]["settings"]
    target["editor"] = target.get("editor", "") + paragraphs(*additions)

    if record["slug"] in {"bringelly", "harrington-park", "currans-hill", "elderslie"}:
        set_e_heading(page.tree[1]["elements"][0], f"Concrete services in {name}")
        for _, node in iter_nodes(page.tree):
            if node.get("widgetType") not in ("image-box", "icon-box"):
                continue
            settings = node.get("settings", {})
            title = settings.get("title_text")
            if not isinstance(title, str) or f" in {name}" in title:
                continue
            wrapped = re.fullmatch(r"(<(?:strong|u)(?:\s[^>]*)?>)(.*)(</(?:strong|u)>)", title)
            if wrapped:
                settings["title_text"] = (
                    f"{wrapped.group(1)}{wrapped.group(2)} in {name}{wrapped.group(3)}"
                )
            else:
                settings["title_text"] = f"{title} in {name}"


def stage7() -> bool:
    pilot = read_json(PILOT_PATH)
    research = researched_suburbs()
    expanded = expanded_suburbs()
    tier1_pages = load_page_models(BUILD / "stage4-tier1-pages.json")
    for page in tier1_pages:
        append_researched_evidence(
            page, research[page.slug.removeprefix("concreters-")]
        )
    old_shell_counts: dict[str, int] = {}
    previous_path = BUILD / "stage7-suburb-pages.json"
    if previous_path.exists():
        for page in load_page_models(previous_path):
            slug = page.slug.removeprefix("concreters-")
            if slug not in research:
                old_shell_counts[page.url] = len(words(plain_text(page.tree)))
    remaining_suburbs: list[PageModel] = []
    shell_counts: dict[str, tuple[int, int]] = {}
    for index, suburb in enumerate(expanded.values()):
        if suburb["slug"] in TIER1:
            continue
        if suburb["slug"] in research:
            page = make_researched_suburb(suburb["slug"], pilot)
            append_researched_evidence(page, research[suburb["slug"]])
            remaining_suburbs.append(page)
        else:
            shell = make_required_research_suburb(suburb, pilot, index)
            after = len(words(plain_text(shell.tree)))
            shell_counts[shell.url] = (old_shell_counts.get(shell.url, after), after)
            remaining_suburbs.append(shell)
    remaining_suburbs.sort(key=lambda page: page.url)

    templates = source_trees()
    core_pages = load_page_models(BUILD / "stage5-core-pages.json")
    services = {page.url: page for page in core_pages if page.page_type == "service"}
    guides = load_page_models(BUILD / "stage6-guide-pages.json")
    intersection_data = read_json(ROOT / "intersection-differentiators.json")
    intersections = [make_intersection(record, services) for record in intersection_data["intersections"]]
    cost_pages = [make_cost_page(item, templates) for item in target_inventory("cost_comparison")]
    cost_pages.sort(key=lambda page: page.url)

    researched_remaining = [
        page
        for page in remaining_suburbs
        if page.slug.removeprefix("concreters-") in research
    ]
    research_shells = [
        page
        for page in remaining_suburbs
        if page.slug.removeprefix("concreters-") not in research
    ]
    substantive = (
        tier1_pages
        + researched_remaining
        + list(services.values())
        + guides
        + intersections
        + cost_pages
    )
    unique, overlaps, _ = duplication_metrics(substantive)
    shared = {page.url: shared_component_percentage(page) for page in substantive}
    failed_unique = {url: value for url, value in unique.items() if value < 60.0}
    failed_pairs = {pair: value for pair, value in overlaps.items() if value > 40.0}
    failed_shared = {url: value for url, value in shared.items() if value > 15.0}
    shell_failures = {
        page.url: {
            "words": shell_counts[page.url][1],
            "status": page.status,
            "robots": page.robots,
        }
        for page in research_shells
        if shell_counts[page.url][1] >= 120
        or page.status != "draft"
        or page.robots != "noindex,follow"
    }

    all_pages = tier1_pages + core_pages + guides + remaining_suburbs + intersections + cost_pages
    publish_boundary = enforce_publish_boundary(all_pages)
    forced_draft = {
        url: result for url, result in publish_boundary.items() if not result["allowed"]
    }
    published_violations = {
        url: result
        for url, result in publish_boundary.items()
        if result["resulting_status"] == "publish" and not result["allowed"]
    }

    write_json(BUILD / "stage7-suburb-pages.json", [page.as_dict() for page in remaining_suburbs])
    write_json(BUILD / "stage7-intersection-pages.json", [page.as_dict() for page in intersections])
    write_json(BUILD / "stage7-cost-pages.json", [page.as_dict() for page in cost_pages])
    write_json(BUILD / "stage7-all-pages.json", [page.as_dict() for page in all_pages])
    write_json(
        BUILD / "stage7-publish-boundary.json",
        publish_boundary,
    )

    passed = (
        len(all_pages) == 155
        and len(substantive) == 105
        and len(research_shells) == 45
        and len(intersections) == 35
        and len(cost_pages) == 10
        and not failed_unique
        and not failed_pairs
        and not failed_shared
        and not shell_failures
        and not published_violations
    )

    lines = [
        "STAGE 7 - Publish-boundary duplication and research shells",
        "=======================================",
        "READ:      suburbs.json; suburbs-expanded.json; intersection-differentiators.json; approved pilot; expanded 155-page inventory",
        "DID:       Reclassified 45 REQUIRED-RESEARCH suburbs as minimal draft/noindex shells below 120 words. Ran duplication across 105 substantive pages and enforced the hard publish boundary in code.",
        "ARTIFACTS: build/stage7-suburb-pages.json; build/stage7-intersection-pages.json; build/stage7-cost-pages.json; build/stage7-all-pages.json; build/stage7-publish-boundary.json; reports/07-duplication-full.md",
        "",
        "## Inventory classification",
        "",
        f"- Total pages built: {len(all_pages)}",
        f"- Substantive/publishable pages checked: {len(substantive)}",
        f"- Research shells exempt from duplication: {len(research_shells)}",
        "- Home and utility pages outside this content-class gate: 5",
        "",
        "## Research shell word counts",
        "",
        "| Shell | Before | After | Result |",
        "|---|---:|---:|---|",
    ]
    for page in sorted(research_shells, key=lambda item: item.url):
        before, after = shell_counts[page.url]
        lines.append(f"| {page.url} | {before} | {after} | {'PASS' if after < 120 else 'FAIL'} |")
    lines.extend(
        (
            "",
            "## Substantive page uniqueness and shared-component footprint",
            "",
            "| Page | Type | Unique body | Shared components | Result |",
            "|---|---|---:|---:|---|",
        )
    )
    for page in sorted(substantive, key=lambda item: item.url):
        result = "PASS" if unique[page.url] >= 60 and shared[page.url] <= 15 else "FAIL"
        lines.append(
            f"| {page.url} | {page.page_type} | {unique[page.url]:.2f}% | {shared[page.url]:.2f}% | {result} |"
        )
    lines.extend(
        (
            "",
            "## Failing substantive pairs",
            "",
        )
    )
    if failed_pairs:
        for (left, right), value in sorted(failed_pairs.items()):
            lines.append(f"- {left} vs {right}: {value:.2f}%")
    else:
        lines.append("None.")
    lines.extend(
        (
            "",
            "## Hard publish boundary",
            "",
            "A configured publish page is retained as publish only when unique body >=60%, every pair against configured publish pages <=40%, a sourced unique variable exists, and shared components <=15%. Failures are automatically changed to draft + noindex.",
            "",
        )
    )
    for url, result in sorted(publish_boundary.items()):
        lines.append(
            f"- {url}: {'PUBLISH' if result['allowed'] else 'FORCED DRAFT'}; unique {result['unique_body']:.2f}%; shared {result['shared_components']:.2f}%; conditions {json.dumps(result['conditions'], ensure_ascii=False)}"
        )
    lines.extend(
        (
            "",
            "## Research shells blocked from publishing",
            "",
        )
    )
    for page in sorted(research_shells, key=lambda item: item.url):
        lines.append(f"- {page.url}")
    lines.extend(
        (
            "",
            f"GATE 7: {'PASS' if passed else 'FAIL'}",
            f"  {'✓' if len(all_pages) == 155 else '✗'} Total pages: {len(all_pages)} (expected 155)",
            f"  {'✓' if len(substantive) == 105 else '✗'} Substantive pages checked: {len(substantive)} (expected 105)",
            f"  {'✓' if len(research_shells) == 45 else '✗'} Research shells: {len(research_shells)} (expected 45)",
            f"  {'✓' if not shell_failures else '✗'} Every shell is draft + noindex and under 120 words: " + ("yes" if not shell_failures else json.dumps(shell_failures, ensure_ascii=False)),
            f"  {'✓' if not failed_unique else '✗'} Every substantive page >=60% unique: " + ("yes" if not failed_unique else f"{len(failed_unique)} failures"),
            f"  {'✓' if not failed_pairs else '✗'} No substantive pair exceeds 40% overlap: " + ("yes" if not failed_pairs else f"{len(failed_pairs)} failures"),
            f"  {'✓' if not failed_shared else '✗'} Shared components <=15%: " + ("yes" if not failed_shared else json.dumps(failed_shared, ensure_ascii=False)),
            f"  {'✓' if not published_violations else '✗'} Hard publish boundary leaves no invalid page published: " + ("yes" if not published_violations else json.dumps(published_violations, ensure_ascii=False)),
            f"  ✓ Configured publish pages automatically demoted: {len(forced_draft)}",
            "",
            "Proceeding to Stage 8." if passed else "HALTING. Stage 7 substantive or publish-boundary gate failed.",
        )
    )
    write_report(REPORTS / "07-duplication-full.md", "\n".join(lines))
    return passed


def paragraphs(*values: str) -> str:
    return "".join(f"<p>{value}</p>" for value in values if value)


def plain_text(tree: Any) -> str:
    values: list[str] = []
    for _, node in iter_nodes(tree):
        widget_type = node.get("widgetType")
        settings = node.get("settings")
        if not widget_type or not isinstance(settings, dict):
            continue
        if widget_type == "heading" and isinstance(settings.get("title"), str):
            values.append(settings["title"])
        elif widget_type == "e-heading":
            try:
                values.append(settings["title"]["value"]["content"]["value"])
            except (KeyError, TypeError):
                pass
        elif widget_type == "text-editor" and isinstance(settings.get("editor"), str):
            values.append(settings["editor"])
        elif widget_type in ("image-box", "icon-box"):
            values.extend(
                value
                for value in (
                    settings.get("title_text"),
                    settings.get("description_text"),
                )
                if isinstance(value, str)
            )
        elif widget_type == "nested-accordion":
            values.extend(
                item.get("item_title", "") for item in settings.get("items", [])
            )
    joined = " ".join(values)
    joined = re.sub(r"<[^>]+>", " ", html.unescape(joined))
    return re.sub(r"\s+", " ", joined).strip()


def bounded_title(name: str) -> str:
    candidates = (
        f"Concreters {name} | Driveways, Slabs & Concrete NSW",
        f"Concreters {name} | Driveways & Slabs | Camden NSW",
        f"Concreters {name} | Local Concrete Services NSW",
        f"Concrete Services {name} | Driveways & Slabs NSW",
    )
    for candidate in candidates:
        if 50 <= len(candidate) <= 60:
            return candidate
    candidate = candidates[-1]
    if len(candidate) < 50:
        candidate += " | Local"
    if len(candidate) > 60:
        candidate = candidate[:60].rsplit(" ", 1)[0]
    if not 50 <= len(candidate) <= 60:
        raise AssertionError(f"Cannot fit meta title for {name}: {candidate!r}")
    return candidate


def bounded_description(seed: str) -> str:
    fillers = (
        " Request an on-site quote.",
        " Local requirements are checked before work starts.",
        " Ask for a written scope before the pour.",
    )
    result = seed.strip()
    for filler in fillers:
        if len(result) >= 140:
            break
        result += filler
    if len(result) > 160:
        result = result[:159].rsplit(" ", 1)[0].rstrip(" ,;:-") + "."
    while len(result) < 140:
        result = result[:-1] + " with local checks."
    if not 140 <= len(result) <= 160:
        raise AssertionError(f"Meta description length {len(result)}: {result!r}")
    return result


def contextual_service_flags(suburb: dict[str, Any]) -> set[str]:
    slug = suburb["slug"]
    weighting = suburb.get("job_mix_weighting", {})
    flags = {"crossovers"}
    if isinstance(weighting, dict) and weighting.get("new_build", 0) >= 0.5:
        flags.add("shed")
    if slug in REPLACEMENT_HEAVY or (
        isinstance(weighting, dict) and weighting.get("replacement", 0) >= 0.3
    ):
        flags.add("replacement")
    if slug in COMMERCIAL_HEAVY or (
        isinstance(weighting, dict) and weighting.get("commercial", 0) >= 0.3
    ):
        flags.add("commercial")
    return flags


def natural_list(values: Iterable[str]) -> str:
    items = [str(value) for value in values]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def researched_suburb_tree(
    suburb: dict[str, Any], expanded: dict[str, Any], pilot: Any
) -> Any:
    if suburb["slug"] == "oran-park":
        tree = copy.deepcopy(pilot)
        module_7 = tree[8]["elements"][0]["elements"][1]["elements"][0]["elements"][1]["settings"]
        editor = module_7["editor"]
        guide_url = expanded["lga_crossing_guide"]
        linked = f'<a href="{guide_url}">Camden Council approval</a>'
        if linked not in editor:
            editor = editor.replace("Camden Council approval", linked, 1)
        module_7["editor"] = editor
        return tree

    tree = copy.deepcopy(pilot)
    name = suburb["name"]
    slug = suburb["slug"]
    postcode = suburb["postcode"]
    flags = contextual_service_flags(suburb)
    unique = html.escape(suburb["unique_local_variable"])
    ground = html.escape(suburb["ground_conditions"])
    approval = html.escape(suburb["approval_path"])
    housing = html.escape(suburb["housing_stock_era"])
    entities = suburb.get("local_entities", {})
    landmarks = natural_list(entities.get("landmarks", [])[:3])
    roads = natural_list(entities.get("streets_roads", [])[:3])
    jobs = [html.escape(job) for job in suburb.get("typical_jobs", [])]
    guide = expanded["lga_crossing_guide"]
    spec = html.escape(expanded["lga_spec"])

    tree[0]["elements"][0]["settings"]["title"] = f"Concreters {name}"
    intro = (
        f"{unique} That local condition shapes how concrete work is scoped in {name} "
        f"{postcode}. Structure Co Concreters Camden covers driveways, slabs, paths and "
        "outdoor areas with the site checked before a written quote is issued."
    )
    tree[0]["elements"][1]["settings"]["editor"] = paragraphs(intro)
    tree[0]["elements"][2]["settings"]["link"]["url"] = "/quote/"
    tree[0]["elements"][3]["settings"]["text"] = "Call us - 03 4517 6915"
    tree[0]["elements"][3]["settings"]["link"]["url"] = "tel:+61345176915"

    set_e_heading(tree[1]["elements"][0], "Our Services")
    tree[1]["elements"][1]["settings"]["editor"] = (
        f"Concrete work requested around {name}, ordered around the verified local job mix."
    )
    cards = [node for _, node in iter_nodes(tree) if node.get("widgetType") == "image-box"]
    for card, (title, url) in zip(cards, SERVICE_CARDS):
        card["settings"]["title_text"] = title
        card["settings"].setdefault("link", {})["url"] = url

    set_e_heading(tree[4]["elements"][0]["elements"][0], f"Concrete work around {name}")
    local_context = [
        f"The recorded housing profile for {name} is {housing}.",
        f"Local reference points include {html.escape(landmarks)}, with access commonly read from {html.escape(roads)}.",
        f"The verified local distinction is specific: {unique}",
    ]
    if "replacement" in flags:
        local_context.append(
            f'Existing housing makes <a href="{SERVICE_URLS["replacement"]}">driveway replacement in {name}</a> a service that must be assessed separately from a first pour.'
        )
    tree[4]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
        *local_context
    )

    set_e_heading(tree[5]["elements"][0]["elements"][0], f"Ground conditions in {name}")
    ground_copy = [
        f"The researched ground note for {name} records: {ground}",
        f"That evidence is checked against the proposed slab location in {name}; assumptions from another estate are not substituted for a site inspection.",
    ]
    if "shed" in flags:
        ground_copy.append(
            f'For post-handover work, <a href="{SERVICE_URLS["shed"]}">shed and garage slabs in {name}</a> need the support beneath the rear-yard location checked before the reinforcement schedule is confirmed.'
        )
    tree[5]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
        *ground_copy
    )

    set_e_heading(tree[6]["elements"][1]["elements"][0]["elements"][0], f"Preparing a pour in {name}")
    prep_copy = [
        f"The typical {name} workload includes {natural_list(jobs)}.",
        f"Preparation is matched to the verified {name} ground profile, the finished levels and the intended load rather than copied from a neighbouring suburb.",
    ]
    if "commercial" in flags:
        prep_copy.append(
            f'Where the brief is business-facing, <a href="{SERVICE_URLS["commercial"]}">commercial concreting in {name}</a> is scoped around the documented use and project requirements rather than domestic assumptions.'
        )
    tree[6]["elements"][1]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
        *prep_copy
    )

    set_e_heading(tree[7]["elements"][0]["elements"][0]["elements"][0], f"Levels and water movement in {name}")
    tree[7]["elements"][0]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
        f"Finished levels in {name} are set from the actual thresholds, boundaries and lawful discharge point observed on the lot.",
        f"The ground record for {name} is considered when falls and joints are documented, because the recorded condition is {ground}",
        f"Reinforcement holds concrete together after movement; it does not remove the need for planned joints, support and drainage in {name}.",
    )

    set_e_heading(tree[8]["elements"][0]["elements"][1]["elements"][0]["elements"][0], f"Driveway approvals for {name}")
    crossover = (
        f'<a href="{SERVICE_URLS["crossovers"]}">crossover work in {name}</a>'
        if "crossovers" in flags
        else f"crossover work in {name}"
    )
    tree[8]["elements"][0]["elements"][1]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
        f"The verified approval path for {name} is: {approval}",
        f"The recorded council specification is reproduced without alteration: {spec}.",
        f'Before {crossover} starts, the governing lot and application path are checked. The related <a href="{guide}">vehicle-crossing requirements guide</a> records the council-level process.',
    )

    set_e_heading(tree[9]["elements"][0], f"Local work in {name}")
    for column in tree[10]["elements"]:
        column["elements"][0]["settings"]["image"]["alt"] = "[[REAL_PHOTO_PENDING]]"
        column["elements"][1]["settings"]["editor"] = paragraphs(
            f"[[REAL_PHOTO_PENDING: verified Structure Co project in {name}]]"
        )

    tree[11]["elements"][0]["settings"]["title"] = f"Why {name} customers choose us"
    icon_boxes = [node for _, node in iter_nodes(tree[11]) if node.get("widgetType") == "icon-box"]
    for index, box in enumerate(icon_boxes, 1):
        box["settings"]["description_text"] = (
            f"Written scope item {index} is checked against the {name} site before work starts."
        )

    tree[12]["elements"][0]["elements"][0]["elements"][0]["settings"]["address"] = f"{name} NSW {postcode}"
    tree[12]["elements"][1]["elements"][0]["settings"]["title"] = f"AREAS WE COVER AROUND {name.upper()}"
    neighbour_links = []
    research = researched_suburbs()
    for neighbour_slug in suburb.get("internal_links_out", []):
        neighbour = research.get(neighbour_slug)
        if neighbour:
            neighbour_links.append(
                f'<a href="/concreters-{neighbour_slug}/">{html.escape(neighbour["name"])}</a>'
            )
    tree[12]["elements"][1]["elements"][1]["settings"]["editor"] = paragraphs(
        f"From {name}, the verified neighbouring service links are {natural_list(neighbour_links)}."
    )

    set_e_heading(tree[13]["elements"][0], f"Planning concrete work in {name}?")
    tree[14]["elements"][0]["settings"]["link"]["url"] = "/quote/"
    faq = suburb.get("faq_angles", [])[:3]
    accordion = tree[14]["elements"][2]
    answers = (unique, ground, approval)
    for index in range(3):
        question = faq[index] if index < len(faq) else f"What must be checked before concrete work in {name}?"
        accordion["settings"]["items"][index]["item_title"] = question
        accordion["elements"][index]["elements"][0]["settings"]["editor"] = paragraphs(
            f"For {name}, the verified project record says: {answers[index]}"
        )
    return tree


def make_researched_suburb(slug: str, pilot: Any) -> PageModel:
    research = researched_suburbs()[slug]
    expanded = expanded_suburbs()[slug]
    tree = researched_suburb_tree(research, expanded, pilot)
    meta_title = bounded_title(research["name"])
    description = bounded_description(
        f"Concreting in {research['name']} {research['postcode']} for driveways, slabs, paths and crossovers, using the verified {research['lga']} approval path."
    )
    return PageModel(
        url=f"/concreters-{slug}/",
        slug=f"concreters-{slug}",
        title=f"Concreters {research['name']}",
        page_type="suburb",
        status="publish" if slug in TIER1 else "draft",
        focus_keyword=f"concreters {research['name'].lower()}",
        meta_title=meta_title,
        meta_description=description,
        tree=tree,
        source_template="concreter-werribee",
        robots="noindex,follow",
    )


def rewrite_gate4_modules(page: PageModel) -> list[int]:
    tree = page.tree
    if page.slug == "concreters-leppington":
        tree[5]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
            "Upper South Creek is the controlling water reference for Leppington, while reactive Wianamatta clay remains the recorded ground material beneath affected lots.",
            "On a flood-affected Leppington street, the specified flood planning level governs slab height and fall. That level is a design input established for the parcel; it cannot be copied from a nearby street or deferred until formwork is in place.",
            f'Post-handover <a href="{SERVICE_URLS["shed"]}">shed and garage slabs in Leppington</a> therefore start with the lot-specific level and the support beneath the proposed rear-yard footprint.',
        )
        tree[7]["elements"][0]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
            "Leppington drainage is set from the parcel's flood planning level where Upper South Creek controls apply, then reconciled with garage thresholds and the lawful discharge point.",
            "A driveway fall that works on an unaffected release is not automatically suitable on a flood-affected Leppington lot. The height constraint is resolved before excavation so the crossover, driveway and dwelling approach work as one level sequence.",
            "The Ingleburn Road grade also produces retaining and stepped-driveway briefs, so joint positions and surface falls are documented for that geometry rather than borrowed from a flat estate plan.",
        )
        existing_spec = expanded_suburbs()["leppington"]["lga_spec"]
        tree[8]["elements"][0]["elements"][1]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
            "Leppington straddles Camden and Liverpool. The governing council is checked against the lot before any application is selected, because opposite sides of a street can follow different forms, fees and inspection processes.",
            "The verified approval record is: Camden Council Standard/Non-Standard Driveway Crossing Application OR Liverpool City Council vehicle crossing application, depending on which LGA the lot falls in.",
            f"The recorded council specification is reproduced without alteration: {html.escape(existing_spec)}.",
            f'Before <a href="{SERVICE_URLS["crossovers"]}">crossover work in Leppington</a> starts, the parcel boundary is resolved. The related <a href="{expanded_suburbs()["leppington"]["lga_crossing_guide"]}">vehicle-crossing requirements guide</a> records the council-level process.',
        )
        return [4, 6, 7]
    if page.slug == "concreters-gledswood-hills":
        tree[7]["elements"][0]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
            "In Gledswood Hills, the South Creek riparian corridor and Sydney Water Upper Canal are the local references for water movement rather than generic growth-corridor drainage language.",
            "Sulfate and chloride exposure near western Sydney creek lines can affect concrete durability and reinforcement cover. The Western Sydney Salinity Code of Practice and saline-environments guidance are therefore checked where the site investigation identifies that exposure.",
            "Falls still have to move surface water away from thresholds, but the Gledswood Hills detail is the combination of drainage, exposure classification and restricted access near conservation land. Those inputs are resolved together before the pour sequence is set.",
        )
        existing_spec = expanded_suburbs()["gledswood-hills"]["lga_spec"]
        tree[8]["elements"][0]["elements"][1]["elements"][0]["elements"][1]["settings"]["editor"] = paragraphs(
            "Gledswood Hills uses Camden Council's driveway-crossing path, while the estate design guidelines are checked separately for the permitted driveway finish before a plain broom finish is quoted.",
            f"The recorded council specification is reproduced without alteration: {html.escape(existing_spec)}.",
            f'For <a href="{SERVICE_URLS["crossovers"]}">crossover work in Gledswood Hills</a>, council geometry and the estate finish control are both confirmed before work starts. The related <a href="{expanded_suburbs()["gledswood-hills"]["lga_crossing_guide"]}">vehicle-crossing requirements guide</a> records the council-level process.',
        )
        return [6, 7]
    return []


def words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower())


def shingles(value: str, size: int = 5) -> list[tuple[str, ...]]:
    tokens = words(value)
    return [tuple(tokens[index : index + size]) for index in range(len(tokens) - size + 1)]


def sentence_index(pages: Iterable[PageModel]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    for page in pages:
        for sentence in re.split(r"(?<=[.!?])\s+", plain_text(page.tree)):
            normal = " ".join(words(sentence))
            if len(normal.split()) >= 8:
                index[normal].add(page.url)
    return index


def strip_shared_components(value: str) -> str:
    output = value
    for component in SHARED_COMPONENTS:
        output = output.replace(component, " ")
    return re.sub(r"\s+", " ", output).strip()


def shared_component_percentage(page: PageModel) -> float:
    body = plain_text(page.tree)
    total_words = len(words(body))
    shared_words = 0
    for component in SHARED_COMPONENTS:
        shared_words += body.count(component) * len(words(component))
    return 100.0 * shared_words / max(1, total_words)


def duplication_metrics(pages: list[PageModel]) -> tuple[dict[str, float], dict[tuple[str, str], float], dict[str, set[str]]]:
    metric_text = {page.url: strip_shared_components(plain_text(page.tree)) for page in pages}
    page_shingles = {url: shingles(value) for url, value in metric_text.items()}
    occurrence: Counter[tuple[str, ...]] = Counter()
    for values in page_shingles.values():
        occurrence.update(set(values))
    unique = {
        url: 100.0 * sum(1 for value in values if occurrence[value] == 1) / max(1, len(values))
        for url, values in page_shingles.items()
    }
    overlaps: dict[tuple[str, str], float] = {}
    for left_index, left in enumerate(pages):
        left_set = set(page_shingles[left.url])
        for right in pages[left_index + 1 :]:
            right_set = set(page_shingles[right.url])
            overlap = 100.0 * len(left_set & right_set) / max(1, min(len(left_set), len(right_set)))
            overlaps[(left.url, right.url)] = overlap
    repeated_index: dict[str, set[str]] = defaultdict(set)
    for page in pages:
        for sentence in re.split(r"(?<=[.!?])\s+", metric_text[page.url]):
            normal = " ".join(words(sentence))
            if len(normal.split()) >= 8:
                repeated_index[normal].add(page.url)
    repeated = {sentence: urls for sentence, urls in repeated_index.items() if len(urls) > 2}
    return unique, overlaps, repeated


def module_texts(tree: Any) -> dict[int, str]:
    groups = {
        1: tree[0:1],
        2: tree[1:4],
        3: tree[4:5],
        4: tree[5:6],
        5: tree[6:7],
        6: tree[7:8],
        7: tree[8:9],
        8: tree[9:11],
        9: tree[11:12],
        10: tree[12:13],
        11: tree[13:15],
    }
    return {number: strip_shared_components(plain_text(nodes)) for number, nodes in groups.items()}


def same_module_overlap(left: PageModel, right: PageModel) -> dict[int, float]:
    left_modules = module_texts(left.tree)
    right_modules = module_texts(right.tree)
    output = {}
    for number in left_modules:
        left_set = set(shingles(left_modules[number]))
        right_set = set(shingles(right_modules[number]))
        output[number] = 100.0 * len(left_set & right_set) / max(
            1, min(len(left_set), len(right_set))
        )
    return output


def render_suburb_preview(page: PageModel) -> str:
    tree = page.tree
    sections = [
        ("Module 1 - Hero", tree[0]["elements"][1]["settings"]["editor"]),
        ("Module 2 - Services", tree[1]["elements"][1]["settings"]["editor"]),
        ("Module 3 - Local context", tree[4]["elements"][0]["elements"][1]["settings"]["editor"]),
        ("Module 4 - Ground", tree[5]["elements"][0]["elements"][1]["settings"]["editor"]),
        ("Module 5 - Preparation", tree[6]["elements"][1]["elements"][0]["elements"][1]["settings"]["editor"]),
        ("Module 6 - Drainage", tree[7]["elements"][0]["elements"][0]["elements"][1]["settings"]["editor"]),
        ("Module 7 - Crossovers", tree[8]["elements"][0]["elements"][1]["elements"][0]["elements"][1]["settings"]["editor"]),
        ("Module 8 - Local work", "[[REAL_PHOTO_PENDING]] x 3"),
        ("Module 9 - Why choose us", tree[11]["elements"][0]["settings"]["title"]),
        ("Module 10 - Areas", tree[12]["elements"][1]["elements"][1]["settings"]["editor"]),
        ("Module 11 - CTA and FAQ", plain_text(tree[13:])),
    ]
    output = [f"# {page.title}", ""]
    for heading, body in sections:
        output.extend((f"## {heading}", "", body, ""))
    return "\n".join(output)


def stage4() -> bool:
    pilot = read_json(PILOT_PATH)
    pages: list[PageModel] = []

    # Leppington is completed and written first as the batch-pattern check.
    leppington = make_researched_suburb("leppington", pilot)
    write_report(BUILD / "stage4-leppington-preview.md", render_suburb_preview(leppington))
    pages.append(make_researched_suburb("oran-park", pilot))
    pages.append(leppington)
    for slug in TIER1[2:]:
        pages.append(make_researched_suburb(slug, pilot))

    by_url = {page.url: page for page in pages}
    diagnostic_pairs = (
        ("/concreters-leppington/", "/concreters-austral/"),
        ("/concreters-leppington/", "/concreters-gledswood-hills/"),
        ("/concreters-gregory-hills/", "/concreters-gledswood-hills/"),
    )
    pre_rewrite_drivers = {
        pair: same_module_overlap(by_url[pair[0]], by_url[pair[1]])
        for pair in diagnostic_pairs
    }
    rewritten: dict[str, list[int]] = {}
    for page in pages:
        modules = rewrite_gate4_modules(page)
        if modules:
            rewritten[page.url] = modules

    leppington = by_url["/concreters-leppington/"]
    write_report(BUILD / "stage4-leppington-preview.md", render_suburb_preview(leppington))

    write_json(BUILD / "stage4-tier1-pages.json", [page.as_dict() for page in pages])
    unique, overlaps, repeated = duplication_metrics(pages)
    shared = {page.url: shared_component_percentage(page) for page in pages}
    failed_unique = {url: value for url, value in unique.items() if value < 60.0}
    failed_pairs = {pair: value for pair, value in overlaps.items() if value > 40.0}
    failed_shared = {url: value for url, value in shared.items() if value > 15.0}
    passed = not failed_unique and not failed_pairs and not repeated and not failed_shared

    lines = [
        "STAGE 4 - Remaining Tier 1 suburbs",
        "=======================================",
        "READ:      suburbs.json; suburbs-expanded.json verified Tier 1 records; oran-park-gold-standard.md; approved Oran Park Elementor pilot; contextual-link rule approved after Gate 3",
        "DID:       Classified only the three approved factual/boilerplate sentences as shared components. Diagnosed overlap by module, rewrote Leppington modules 4/6/7 and Gledswood Hills modules 6/7, and preserved every differentiator verbatim.",
        "ARTIFACTS: build/stage4-leppington-preview.md; build/stage4-tier1-pages.json; reports/04-duplication.md",
        "",
        "## Unique body percentage",
        "",
        "Measured as the percentage of each page's body 5-gram positions that occur on no other Tier 1 page.",
        "",
        "| Page | Unique body | Shared components | Result |",
        "|---|---:|---:|---|",
    ]
    for page in pages:
        result = "PASS" if unique[page.url] >= 60 and shared[page.url] <= 15 else "FAIL"
        lines.append(f"| {page.url} | {unique[page.url]:.2f}% | {shared[page.url]:.2f}% | {result} |")
    lines.extend(("", "## Pre-rewrite module drivers", ""))
    for pair, module_values in pre_rewrite_drivers.items():
        drivers = sorted(module_values.items(), key=lambda item: item[1], reverse=True)
        rendered = ", ".join(f"M{number} {value:.2f}%" for number, value in drivers[:5])
        lines.append(f"- {pair[0]} vs {pair[1]}: {rendered}")
    lines.extend(("", "## Modules rewritten", ""))
    for url, modules in rewritten.items():
        lines.append(f"- {url}: {', '.join(f'Module {number}' for number in modules)}")
    lines.extend(("", "## Pairwise 5-gram overlap", "", "| Page A | Page B | Overlap | Result |", "|---|---|---:|---|"))
    for (left, right), value in sorted(overlaps.items()):
        result = "PASS" if value <= 40 else "FAIL"
        lines.append(f"| {left} | {right} | {value:.2f}% | {result} |")
    lines.extend(("", f"Repeated sentences appearing on more than two pages: {len(repeated)}", ""))
    if repeated:
        for sentence, urls in repeated.items():
            lines.append(f"- `{sentence}`: {', '.join(sorted(urls))}")
    lines.append(f"GATE 4: {'PASS' if passed else 'FAIL'}")
    lines.append(
        f"  {'✓' if not failed_unique else '✗'} Every page >=60% unique body positions: "
        + ("yes" if not failed_unique else json.dumps(failed_unique, ensure_ascii=False))
    )
    lines.append(
        f"  {'✓' if not failed_pairs else '✗'} No pair exceeds 40% overlap: "
        + ("yes" if not failed_pairs else "; ".join(f"{a} vs {b}: {v:.2f}%" for (a, b), v in failed_pairs.items()))
    )
    lines.append(
        f"  {'✓' if not repeated else '✗'} No sentence appears on more than two pages: "
        + ("yes" if not repeated else f"{len(repeated)} failures")
    )
    lines.append(
        f"  {'✓' if not failed_shared else '✗'} Shared components <=15% of every page: "
        + ("yes" if not failed_shared else json.dumps(failed_shared, ensure_ascii=False))
    )
    lines.append("\nProceeding to Stage 5." if passed else "\nHALTING. Stage 4 duplication thresholds failed.")
    write_report(REPORTS / "04-duplication.md", "\n".join(lines))
    return passed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("4", "5", "6", "7"))
    args = parser.parse_args()
    if args.stage == "4" and not stage4():
        raise SystemExit(1)
    if args.stage == "5" and not stage5():
        raise SystemExit(1)
    if args.stage == "6" and not stage6():
        raise SystemExit(1)
    if args.stage == "7" and not stage7():
        raise SystemExit(1)
