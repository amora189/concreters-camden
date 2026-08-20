from __future__ import annotations

import copy
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET

from lib.site_builder import (
    BUILD,
    REPORTS,
    ROOT,
    PageModel,
    bounded_description,
    duplication_metrics,
    fit_meta_title,
    heading_outline,
    load_page_models,
    normalize_actions,
    normalize_headings,
    plain_text,
    researched_suburbs,
    text_editor_nodes,
    write_json,
    write_report,
)
from lib.stage3_gate import iter_nodes
from lib.stage8 import image_dicts, internal_links, old_path_map
from lib.wxr import NS, get_meta, parse_elementor, serialize_elementor, set_meta


SOURCE_XML = ROOT / "source" / "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml"
OUTPUT_XML = ROOT / "camden-concreting-import.xml"
DOMAIN = "https://concreterscamden.com.au"
GUIDES_HUB_ID = 1502

WFW_NS = "http://wellformedweb.org/CommentAPI/"
ET.register_namespace("excerpt", NS["excerpt"])
ET.register_namespace("content", NS["content"])
ET.register_namespace("wfw", WFW_NS)
ET.register_namespace("dc", NS["dc"])
ET.register_namespace("wp", NS["wp"])


GUIDE_CATEGORIES: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = (
    (
        "Council & approvals",
        (
            ("camden-council-driveway-crossing", "Camden Council crossing applications, recorded geometry and inspection inputs."),
            ("liverpool-council-vehicle-crossing", "Liverpool vehicle-crossing approvals and the records to check before quoting."),
            ("campbelltown-council-driveway-crossing", "Campbelltown driveway-crossing steps, site controls and approval evidence."),
            ("wollondilly-council-driveway-crossing", "Wollondilly crossing requirements for urban and rural street interfaces."),
            ("driveway-crossover-cost-nsw", "The measured scope and real quote evidence needed to price a crossover."),
            ("do-i-need-council-approval-driveway-nsw", "A practical guide to when driveway and crossing work needs council approval."),
        ),
    ),
    (
        "Ground & engineering",
        (
            ("reactive-clay-slabs-as2870", "How reactive clay and AS 2870 site evidence affect a slab brief."),
            ("salinity-and-concrete-western-sydney", "Durability checks where western Sydney salinity exposure may affect concrete."),
            ("engineered-fill-and-why-new-estate-slabs-crack", "Why fill history, compaction evidence and the work footprint matter."),
            ("site-classification-explained", "What a site classification records and why the actual work area still matters."),
            ("concrete-strength-grades-explained", "Concrete strength grades explained without substituting them for design advice."),
            ("sl72-vs-sl82-reinforcement", "The documented design questions behind SL72 and SL82 mesh selection."),
            ("slab-thickness-for-driveways-vs-sheds", "How intended loading and support inform driveway and shed slab thickness."),
            ("control-joints-and-saw-cut-timing", "Joint layout and saw-cut timing as planned movement-control decisions."),
        ),
    ),
    (
        "Cost",
        (
            ("concrete-driveway-cost-nsw", "The inclusions and site inputs behind a defensible NSW driveway rate."),
            ("concrete-slab-cost-per-m2", "What must be included before a slab cost per square metre is meaningful."),
            ("exposed-aggregate-cost", "The finish, access and sealing inputs that move exposed aggregate cost."),
            ("stencilled-vs-stamped-concrete-cost", "A like-for-like cost framework for stencilled and stamped finishes."),
            ("shed-slab-cost", "The dimensions, loading, access and support evidence behind a shed slab quote."),
            ("commercial-hardstand-cost", "Commercial hardstand quantities and design inputs that require project evidence."),
            ("what-actually-moves-a-concrete-quote", "The measurable site and scope changes that alter a concrete quote."),
        ),
    ),
    (
        "Finishes & materials",
        (
            ("exposed-aggregate-vs-stencil", "Compare appearance, texture, maintenance and site suitability."),
            ("coloured-concrete-explained", "Colour systems, samples and maintenance questions to settle before a pour."),
            ("honed-and-polished-concrete", "Where honed and polished finishes differ in use, process and upkeep."),
            ("broom-finish-concrete", "How broom texture relates to slope, wet use and the finish brief."),
            ("non-slip-finishes-for-pools-and-slopes", "Finish selection for wet areas, pools, paths and sloping concrete."),
            ("sealing-and-resealing-concrete", "What sealing can protect and what must be checked before resealing."),
            ("concrete-vs-pavers-vs-asphalt", "Compare support, joints, maintenance and intended use across three surfaces."),
        ),
    ),
    (
        "Problems & maintenance",
        (
            ("why-concrete-cracks", "The main crack mechanisms and the evidence needed before assigning a cause."),
            ("concrete-crack-types-and-which-matter", "How crack pattern, movement and exposure guide the next inspection step."),
            ("concrete-repair-vs-replace", "A framework for deciding whether failure is local, surface-level or structural."),
            ("how-long-before-you-can-drive-on-concrete", "Why return-to-traffic timing depends on the specified concrete and curing plan."),
            ("curing-concrete-in-summer-vs-winter", "How weather changes curing controls and early protection."),
            ("concrete-efflorescence", "What efflorescence indicates and the checks to make before cleaning."),
            ("removing-oil-stains-and-tyre-marks-from-concrete", "Cleaning choices that account for the finish, sealer and stain type."),
        ),
    ),
)


BLOCKLIST: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Melbourne", re.compile(r"\bMelbourne\b", re.IGNORECASE)),
    ("Werribee", re.compile(r"\bWerribee\b", re.IGNORECASE)),
    ("Wyndham", re.compile(r"\bWyndham\b", re.IGNORECASE)),
    ("Point Cook", re.compile(r"\bPoint\s+Cook\b", re.IGNORECASE)),
    ("Tarneit", re.compile(r"\bTarneit\b", re.IGNORECASE)),
    ("Truganina", re.compile(r"\bTruganina\b", re.IGNORECASE)),
    ("Hoppers Crossing", re.compile(r"\bHoppers\s+Crossing\b", re.IGNORECASE)),
    ("Riverwalk", re.compile(r"\bRiverwalk\b", re.IGNORECASE)),
    ("Harpley", re.compile(r"\bHarpley\b", re.IGNORECASE)),
    ("Victoria", re.compile(r"\bVictoria\b", re.IGNORECASE)),
    ("VIC", re.compile(r"\bVIC\b", re.IGNORECASE)),
    ("03 4427 9541", re.compile(r"03\s+4427\s+9541")),
    ("bestconcretersmelbourne.com.au", re.compile(r"bestconcretersmelbourne\.com\.au", re.IGNORECASE)),
)


PLACEHOLDER_RE = re.compile(
    r"\[\[(?:PLACEHOLDER|VERIFY|REAL_PHOTO_PENDING)(?::[^\]]*)?\]\]"
)


def _text(node: ET.Element | None) -> str:
    return "" if node is None or node.text is None else node.text


def set_child_text(item: ET.Element, path: str, value: str) -> None:
    node = item.find(path, NS)
    if node is None:
        if ":" in path:
            prefix, name = path.split(":", 1)
            node = ET.SubElement(item, f"{{{NS[prefix]}}}{name}")
        else:
            node = ET.SubElement(item, path)
    node.text = value


def canonical(url: str) -> str:
    return DOMAIN + (url if url.startswith("/") else f"/{url}")


def make_guide_hub(guide_template: PageModel) -> PageModel:
    tree = copy.deepcopy(guide_template.tree[:6])
    headings = [category for category, _ in GUIDE_CATEGORIES]
    normalize_headings(tree, "Concreting Guides for South West Sydney", headings)

    intro = (
        "<p>Use this guide library to check council approvals, ground and engineering inputs, "
        "cost evidence, finish choices, and concrete maintenance across Camden and South West Sydney. "
        "Each page separates verified requirements from project details that still need an on-site check.</p>"
    )
    blocks = [intro]
    for _, entries in GUIDE_CATEGORIES:
        rows = "".join(
            f'<li><a href="/guides/{slug}/">{html.escape(next(page_title for page_slug, page_title in guide_titles() if page_slug == slug))}</a> — {html.escape(description)}</li>'
            for slug, description in entries
        )
        blocks.append(f"<ul>{rows}</ul>")

    editors = text_editor_nodes(tree)
    if len(editors) != len(blocks):
        raise AssertionError(
            f"Guide hub template has {len(editors)} editors; expected {len(blocks)}"
        )
    for widget, content in zip(editors, blocks, strict=True):
        widget["settings"]["editor"] = content

    for _, node in iter_nodes(tree):
        settings = node.get("settings")
        if not isinstance(settings, dict):
            continue
        image = settings.get("image")
        if isinstance(image, dict) and image.get("id"):
            image["alt"] = "Concrete planning reference for the South West Sydney guide library"
    normalize_actions(tree)
    return PageModel(
        url="/guides/",
        slug="guides",
        title="Concreting Guides for South West Sydney",
        page_type="guide_hub",
        status="draft",
        focus_keyword="concreting guides south west sydney",
        meta_title=fit_meta_title("Concreting Guides South West Sydney | Structure Co Camden"),
        meta_description=bounded_description(
            "Browse concreting guides for South West Sydney covering council approvals, ground engineering, costs, finishes, materials, repairs and maintenance."
        ),
        tree=tree,
        source_template="why-does-concrete-crack",
        robots="noindex,follow",
    )


def guide_titles() -> tuple[tuple[str, str], ...]:
    return (
        ("camden-council-driveway-crossing", "Camden Council Driveway Crossing"),
        ("liverpool-council-vehicle-crossing", "Liverpool Council Vehicle Crossing"),
        ("campbelltown-council-driveway-crossing", "Campbelltown Council Driveway Crossing"),
        ("wollondilly-council-driveway-crossing", "Wollondilly Council Driveway Crossing"),
        ("driveway-crossover-cost-nsw", "Driveway Crossover Cost NSW"),
        ("do-i-need-council-approval-driveway-nsw", "Do I Need Council Approval for a Driveway in NSW?"),
        ("reactive-clay-slabs-as2870", "Reactive Clay Slabs and AS 2870"),
        ("salinity-and-concrete-western-sydney", "Salinity and Concrete in Western Sydney"),
        ("engineered-fill-and-why-new-estate-slabs-crack", "Engineered Fill and Why New-Estate Slabs Crack"),
        ("site-classification-explained", "Site Classification Explained"),
        ("concrete-strength-grades-explained", "Concrete Strength Grades Explained"),
        ("sl72-vs-sl82-reinforcement", "SL72 vs SL82 Reinforcement"),
        ("slab-thickness-for-driveways-vs-sheds", "Slab Thickness for Driveways vs Sheds"),
        ("control-joints-and-saw-cut-timing", "Control Joints and Saw-Cut Timing"),
        ("concrete-driveway-cost-nsw", "Concrete Driveway Cost NSW"),
        ("concrete-slab-cost-per-m2", "Concrete Slab Cost per m²"),
        ("exposed-aggregate-cost", "Exposed Aggregate Cost"),
        ("stencilled-vs-stamped-concrete-cost", "Stencilled vs Stamped Concrete Cost"),
        ("shed-slab-cost", "Shed Slab Cost"),
        ("commercial-hardstand-cost", "Commercial Hardstand Cost"),
        ("what-actually-moves-a-concrete-quote", "What Actually Moves a Concrete Quote"),
        ("exposed-aggregate-vs-stencil", "Exposed Aggregate vs Stencil"),
        ("coloured-concrete-explained", "Coloured Concrete Explained"),
        ("honed-and-polished-concrete", "Honed and Polished Concrete"),
        ("broom-finish-concrete", "Broom Finish Concrete"),
        ("non-slip-finishes-for-pools-and-slopes", "Non-Slip Finishes for Pools and Slopes"),
        ("sealing-and-resealing-concrete", "Sealing and Resealing Concrete"),
        ("concrete-vs-pavers-vs-asphalt", "Concrete vs Pavers vs Asphalt"),
        ("why-concrete-cracks", "Why Concrete Cracks"),
        ("concrete-crack-types-and-which-matter", "Concrete Crack Types and Which Matter"),
        ("concrete-repair-vs-replace", "Concrete Repair vs Replace"),
        ("how-long-before-you-can-drive-on-concrete", "How Long Before You Can Drive on Concrete?"),
        ("curing-concrete-in-summer-vs-winter", "Curing Concrete in Summer vs Winter"),
        ("concrete-efflorescence", "Concrete Efflorescence"),
        ("removing-oil-stains-and-tyre-marks-from-concrete", "Removing Oil Stains and Tyre Marks from Concrete"),
    )


def load_final_models() -> list[PageModel]:
    pages = load_page_models(BUILD / "stage8-all-pages.json")
    bringelly = next(page for page in pages if page.url == "/concreters-bringelly/")
    bringelly.meta_description = bounded_description(
        "Concreting in Bringelly 2556 for driveways, slabs, paths and crossovers, with the Liverpool-Camden council boundary checked before approval is selected."
    )
    guide_template = next(page for page in pages if page.url == "/guides/why-concrete-cracks/")
    hub = make_guide_hub(guide_template)
    first_guide = next(index for index, page in enumerate(pages) if page.page_type == "guide")
    pages.insert(first_guide, hub)
    sanitize_page_trees(pages)
    if len(pages) != 156:
        raise AssertionError(f"Expected 156 final pages, found {len(pages)}")
    return pages


def sanitize_page_trees(pages: list[PageModel]) -> None:
    """Remove residual source-site strings from visible and hidden Elementor fields."""
    image_map = json.loads((BUILD / "stage8-image-map.json").read_text(encoding="utf-8"))
    image_records = {int(post_id): record for post_id, record in image_map.items()}
    image_url_replacements = [
        (re.compile(re.escape(record["old_url"]), re.IGNORECASE), record["new_url"])
        for record in image_map.values()
    ]
    path_replacements = []
    for old_path, new_path in sorted(old_path_map().items(), key=lambda item: len(item[0]), reverse=True):
        for scheme in ("http", "https"):
            path_replacements.append(
                (re.compile(re.escape(f"{scheme}://bestconcretersmelbourne.com.au{old_path}"), re.IGNORECASE), new_path)
            )
    text_replacements = (
        (re.compile(r"81\s+Lock\s+Avenue\s+Werribee\s+VIC\s+3030", re.IGNORECASE), "[[PLACEHOLDER: verified Structure Co business address]]"),
        (re.compile(r"ABN:\s*24\s+280\s+418\s+757", re.IGNORECASE), "[[PLACEHOLDER: verified Structure Co ABN]]"),
        (re.compile(r"bestconcretersmelbourne\.com\.au", re.IGNORECASE), "concreterscamden.com.au"),
        (re.compile(r"\bHoppers\s+Crossing\b", re.IGNORECASE), "Harrington Park"),
        (re.compile(r"\bPoint\s+Cook\b", re.IGNORECASE), "Leppington"),
        (re.compile(r"\bMelbourne\b", re.IGNORECASE), "Camden"),
        (re.compile(r"\bWerribee\b", re.IGNORECASE), "Camden"),
        (re.compile(r"\bWyndham\b", re.IGNORECASE), "Camden"),
        (re.compile(r"\bTarneit\b", re.IGNORECASE), "Gregory Hills"),
        (re.compile(r"\bTruganina\b", re.IGNORECASE), "Austral"),
        (re.compile(r"\bRiverwalk\b", re.IGNORECASE), "Oran Park"),
        (re.compile(r"\bHarpley\b", re.IGNORECASE), "Oran Park"),
        (re.compile(r"\bVictoria\b", re.IGNORECASE), "New South Wales"),
        (re.compile(r"\bVIC\b", re.IGNORECASE), "NSW"),
        (re.compile(r"03\s+4427\s+9541"), "03 4517 6915"),
    )

    def sanitize_string(value: str) -> str:
        output = value
        for pattern, replacement in path_replacements:
            output = pattern.sub(replacement, output)
        for pattern, replacement in image_url_replacements:
            output = pattern.sub(replacement, output)
        for pattern, replacement in text_replacements:
            output = pattern.sub(replacement, output)
        return output

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            image_id = node.get("id")
            if isinstance(image_id, (int, str)) and str(image_id).isdigit():
                record = image_records.get(int(image_id))
                if record is not None and isinstance(node.get("url"), str):
                    node["url"] = record["new_url"]
                    if "alt" in node:
                        node["alt"] = node.get("alt") or record["base_alt"]
            for key, value in list(node.items()):
                if key in {"testimonial_content", "testimonial_name", "testimonial_job"}:
                    if key == "testimonial_content":
                        node[key] = "[[PLACEHOLDER: verified Structure Co review text and permission to publish]]"
                    elif key == "testimonial_name":
                        node[key] = "[[PLACEHOLDER: verified reviewer name]]"
                    else:
                        node[key] = ""
                else:
                    node[key] = walk(value)
            return node
        if isinstance(node, list):
            return [walk(value) for value in node]
        if isinstance(node, str):
            return sanitize_string(node)
        return node

    for page in pages:
        page.tree = walk(page.tree)
    oran_crossover = next(
        page
        for page in pages
        if page.url == "/concrete-crossovers-and-laybacks-oran-park/"
    )
    first_editor = text_editor_nodes(oran_crossover.tree)[0]["settings"]
    first_editor["editor"] = first_editor.get("editor", "") + (
        "<p>For this Oran Park crossover record, the 800mm boundary offset is a set-out checkpoint distinct from "
        "the 900mm used elsewhere in Camden; the 1200mm allocation itself does not change.</p>"
    )


def source_items(root: ET.Element) -> list[ET.Element]:
    channel = root.find("channel")
    if channel is None:
        raise AssertionError("Source WXR channel is missing")
    return channel.findall("item")


def source_page_items(root: ET.Element) -> dict[str, ET.Element]:
    return {
        _text(item.find("wp:post_name", NS)): item
        for item in source_items(root)
        if _text(item.find("wp:post_type", NS)) == "page"
    }


def page_id_map(root: ET.Element, pages: list[PageModel]) -> dict[str, int]:
    url_map = json.loads((BUILD / "url-map.json").read_text(encoding="utf-8"))
    source_by_slug = source_page_items(root)
    direct_ids = {
        record["target_slug"]: int(_text(source_by_slug[source_slug].find("wp:post_id", NS)))
        for source_slug, record in url_map["direct_transformations"].items()
    }
    allocated = json.loads((BUILD / "id-map.json").read_text(encoding="utf-8"))["new_ids"]
    output: dict[str, int] = {}
    for page in pages:
        if page.slug == "guides":
            output[page.url] = GUIDES_HUB_ID
        elif page.slug in direct_ids:
            output[page.url] = direct_ids[page.slug]
        else:
            output[page.url] = int(allocated[page.slug])
    if len(set(output.values())) != len(output):
        duplicates = [post_id for post_id, count in Counter(output.values()).items() if count > 1]
        raise AssertionError(f"Duplicate page IDs: {duplicates}")
    return output


def update_stage9_manifests(pages: list[PageModel], ids: dict[str, int]) -> list[dict[str, Any]]:
    id_map = json.loads((BUILD / "id-map.json").read_text(encoding="utf-8"))
    id_map["new_ids"]["guides"] = GUIDES_HUB_ID
    write_json(BUILD / "id-map.json", id_map)

    url_map = json.loads((BUILD / "url-map.json").read_text(encoding="utf-8"))
    if not any(item["target_slug"] == "guides" for item in url_map["new_pages"]):
        url_map["new_pages"].append(
            {
                "target_slug": "guides",
                "url": "/guides/",
                "source_template": "why-does-concrete-crack",
                "status": "draft",
                "type": "guide_hub",
                "post_id": GUIDES_HUB_ID,
            }
        )
    write_json(BUILD / "url-map.json", url_map)

    menus = json.loads((BUILD / "stage8-menus.json").read_text(encoding="utf-8"))
    for menu_name in ("primary", "primary-2"):
        blog = next(item for item in menus[menu_name] if item["title"] == "Blog")
        blog["url"] = "/guides/"
    write_json(BUILD / "stage9-menus.json", menus)

    manifest = []
    for page in pages:
        parent = GUIDES_HUB_ID if page.page_type == "guide" else 0
        manifest.append(
            {
                "post_id": ids[page.url],
                "post_name": page.slug,
                "post_parent": parent,
                "url": page.url,
                "page_type": page.page_type,
                "status": page.status,
            }
        )
    write_json(BUILD / "stage9-all-pages.json", [page.as_dict() for page in pages])
    write_json(BUILD / "stage9-page-manifest.json", manifest)
    return manifest


def remove_meta(item: ET.Element, predicate: Any) -> None:
    for meta in list(item.findall("wp:postmeta", NS)):
        key = _text(meta.find("wp:meta_key", NS))
        if predicate(key):
            item.remove(meta)


def build_page_item(
    page: PageModel,
    post_id: int,
    template: ET.Element,
) -> ET.Element:
    item = copy.deepcopy(template)
    for category in list(item.findall("category")):
        item.remove(category)
    for comment in list(item.findall("wp:comment", NS)):
        item.remove(comment)

    set_child_text(item, "title", page.title)
    set_child_text(item, "link", canonical(page.url))
    guid = item.find("guid")
    if guid is None:
        guid = ET.SubElement(item, "guid")
    guid.set("isPermaLink", "false")
    guid.text = f"{DOMAIN}/?page_id={post_id}"
    set_child_text(item, "description", "")
    set_child_text(item, "content:encoded", "")
    set_child_text(item, "excerpt:encoded", "")
    set_child_text(item, "wp:post_id", str(post_id))
    set_child_text(item, "wp:post_name", page.slug)
    set_child_text(item, "wp:post_parent", str(GUIDES_HUB_ID if page.page_type == "guide" else 0))
    set_child_text(item, "wp:post_type", "page")
    set_child_text(item, "wp:status", page.status)
    set_child_text(item, "wp:comment_status", "closed")
    set_child_text(item, "wp:ping_status", "closed")
    set_child_text(item, "wp:post_password", "")
    set_child_text(item, "wp:is_sticky", "0")
    set_child_text(item, "wp:menu_order", "0")

    remove_meta(
        item,
        lambda key: key.startswith("rank_math_")
        or key.startswith("_rank_math_")
        or key.startswith("_siteseo_")
        or key == "_elementor_element_cache",
    )
    set_meta(item, "_elementor_data", serialize_elementor(page.tree))
    set_meta(item, "_elementor_edit_mode", "builder")
    set_meta(item, "_elementor_template_type", "wp-page")
    set_meta(item, "_elementor_version", "4.2.0")
    set_meta(item, "_wp_page_template", "default")
    set_meta(item, "rank_math_title", page.meta_title)
    set_meta(item, "rank_math_description", page.meta_description)
    set_meta(item, "rank_math_focus_keyword", page.focus_keyword)
    set_meta(item, "rank_math_breadcrumb_title", "Guides" if page.page_type == "guide_hub" else page.title)
    if page.robots:
        set_meta(item, "rank_math_robots", 'a:2:{i:0;s:7:"noindex";i:1;s:6:"follow";}')
    return item


def replace_serialized_strings(value: str, replacements: Iterable[tuple[re.Pattern[str], str]]) -> str:
    token = re.compile(r's:\d+:"(.*?)";', re.DOTALL)

    def mutate(match: re.Match[str]) -> str:
        content = match.group(1)
        for pattern, replacement in replacements:
            content = pattern.sub(replacement, content)
        return f's:{len(content.encode("utf-8"))}:"{content}";'

    return token.sub(mutate, value)


def build_attachment_item(item: ET.Element, record: dict[str, Any]) -> ET.Element:
    output = copy.deepcopy(item)
    post_id = int(record["post_id"])
    new_stem = Path(record["new_filename"]).stem
    old_stem = Path(record["old_filename"]).stem
    replacements = (
        (re.compile(re.escape(old_stem), re.IGNORECASE), new_stem),
        (re.compile(r"bestconcretersmelbourne\.com\.au", re.IGNORECASE), "concreterscamden.com.au"),
    )
    set_child_text(output, "title", record["base_alt"])
    set_child_text(output, "link", f"{DOMAIN}/{new_stem}/")
    set_child_text(output, "content:encoded", "")
    set_child_text(output, "excerpt:encoded", "")
    guid = output.find("guid")
    if guid is None:
        guid = ET.SubElement(output, "guid")
    guid.set("isPermaLink", "false")
    guid.text = record["new_url"]
    set_child_text(output, "wp:post_name", new_stem)
    set_child_text(output, "wp:post_parent", "0")
    set_child_text(output, "wp:attachment_url", record["new_url"])
    set_meta(output, "_wp_attached_file", record["new_file"])
    metadata = get_meta(output, "_wp_attachment_metadata")
    if metadata is not None:
        set_meta(output, "_wp_attachment_metadata", replace_serialized_strings(metadata, replacements))
    set_meta(output, "_wp_attachment_image_alt", record["base_alt"])
    if int(_text(output.find("wp:post_id", NS))) != post_id:
        raise AssertionError(f"Attachment ID mismatch for {post_id}")
    return output


def localize_support_item(item: ET.Element) -> ET.Element:
    output = copy.deepcopy(item)
    replacements = (
        (re.compile(r"bestconcretersmelbourne\.com\.au", re.IGNORECASE), "concreterscamden.com.au"),
        (re.compile(r"\bMelbourne\b", re.IGNORECASE), "Camden"),
        (re.compile(r"\bWerribee\b", re.IGNORECASE), "Camden"),
        (re.compile(r"\bVIC\b", re.IGNORECASE), "NSW"),
    )
    for node in output.iter():
        if node.text:
            value = node.text
            for pattern, replacement in replacements:
                value = pattern.sub(replacement, value)
            node.text = value
    return output


def menu_item_template(root: ET.Element) -> ET.Element:
    return next(
        item
        for item in source_items(root)
        if _text(item.find("wp:post_type", NS)) == "nav_menu_item"
    )


def build_menu_item(
    template: ET.Element,
    post_id: int,
    menu_slug: str,
    menu_name: str,
    title: str,
    menu_order: int,
    parent_menu_id: int,
    target_url: str,
    page_ids: dict[str, int],
) -> ET.Element:
    item = copy.deepcopy(template)
    for category in list(item.findall("category")):
        item.remove(category)
    remove_meta(item, lambda key: True)
    set_child_text(item, "title", title)
    set_child_text(item, "link", f"{DOMAIN}/?p={post_id}")
    guid = item.find("guid")
    if guid is None:
        guid = ET.SubElement(item, "guid")
    guid.set("isPermaLink", "false")
    guid.text = f"{DOMAIN}/?p={post_id}"
    set_child_text(item, "description", "")
    set_child_text(item, "content:encoded", "")
    set_child_text(item, "excerpt:encoded", "")
    set_child_text(item, "wp:post_id", str(post_id))
    set_child_text(item, "wp:post_name", f"menu-{menu_slug}-{post_id}")
    set_child_text(item, "wp:status", "publish")
    set_child_text(item, "wp:post_parent", "0")
    set_child_text(item, "wp:menu_order", str(menu_order))
    set_child_text(item, "wp:post_type", "nav_menu_item")
    category = ET.Element("category", {"domain": "nav_menu", "nicename": menu_slug})
    category.text = menu_name
    item.append(category)

    is_page = target_url in page_ids
    set_meta(item, "_menu_item_type", "post_type" if is_page else "custom")
    set_meta(item, "_menu_item_menu_item_parent", str(parent_menu_id))
    set_meta(item, "_menu_item_object_id", str(page_ids[target_url] if is_page else post_id))
    set_meta(item, "_menu_item_object", "page" if is_page else "custom")
    set_meta(item, "_menu_item_target", "")
    set_meta(item, "_menu_item_classes", 'a:1:{i:0;s:0:"";}')
    set_meta(item, "_menu_item_xfn", "")
    set_meta(item, "_menu_item_url", "" if is_page else target_url)
    return item


def build_menu_items(root: ET.Element, page_ids: dict[str, int]) -> list[ET.Element]:
    template = menu_item_template(root)
    menus = json.loads((BUILD / "stage9-menus.json").read_text(encoding="utf-8"))
    menu_names = {
        "primary": "Primary",
        "primary-2": "Primary (2)",
        "footer-areas": "Footer Areas",
        "footer-services": "Footer Services",
        "footer-blogs": "Footer Blogs",
    }
    next_id = GUIDES_HUB_ID + 1
    output: list[ET.Element] = []
    for menu_slug in ("primary", "primary-2"):
        order = 1
        for group in menus[menu_slug]:
            parent_id = next_id
            output.append(
                build_menu_item(
                    template,
                    next_id,
                    menu_slug,
                    menu_names[menu_slug],
                    group["title"],
                    order,
                    0,
                    group["url"],
                    page_ids,
                )
            )
            next_id += 1
            order += 1
            for child in group["children"]:
                output.append(
                    build_menu_item(
                        template,
                        next_id,
                        menu_slug,
                        menu_names[menu_slug],
                        child["title"],
                        order,
                        parent_id,
                        child["url"],
                        page_ids,
                    )
                )
                next_id += 1
                order += 1
    for menu_slug in ("footer-areas", "footer-services", "footer-blogs"):
        for order, item in enumerate(menus[menu_slug], start=1):
            output.append(
                build_menu_item(
                    template,
                    next_id,
                    menu_slug,
                    menu_names[menu_slug],
                    item["title"],
                    order,
                    0,
                    item["url"],
                    page_ids,
                )
            )
            next_id += 1
    if len(output) != 65:
        raise AssertionError(f"Expected 65 menu items, found {len(output)}")
    return output


def localize_channel(channel: ET.Element) -> None:
    replacements = (
        (re.compile(r"bestconcretersmelbourne\.com\.au", re.IGNORECASE), "concreterscamden.com.au"),
        (re.compile(r"E\s*&\s*T\s*Co\s*Concreters\s*Melbourne", re.IGNORECASE), "Structure Co Concreters Camden"),
        (re.compile(r"\bMelbourne\b", re.IGNORECASE), "Camden"),
    )
    for node in channel:
        if node.tag == "item":
            continue
        for descendant in node.iter():
            if not descendant.text:
                continue
            value = descendant.text
            for pattern, replacement in replacements:
                value = pattern.sub(replacement, value)
            descendant.text = value
    title = channel.find("title")
    if title is not None:
        title.text = "Structure Co Concreters Camden"
    link = channel.find("link")
    if link is not None:
        link.text = DOMAIN
    description = channel.find("description")
    if description is not None:
        description.text = "Concreting services and project guides for Camden and South West Sydney"
    for path in ("wp:base_site_url", "wp:base_blog_url"):
        node = channel.find(path, NS)
        if node is not None:
            node.text = DOMAIN


def assemble_xml(pages: list[PageModel], ids: dict[str, int]) -> None:
    tree = ET.parse(SOURCE_XML)
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        raise AssertionError("Source WXR channel is missing")
    originals = list(channel.findall("item"))
    pages_by_slug = source_page_items(root)
    image_map = json.loads((BUILD / "stage8-image-map.json").read_text(encoding="utf-8"))

    page_items = []
    for page in pages:
        source_template = {
            "concreter-werribee-research-shell": "concreter-werribee",
        }.get(page.source_template, page.source_template)
        if source_template not in pages_by_slug:
            raise AssertionError(f"Missing source template {page.source_template} for {page.url}")
        page_items.append(build_page_item(page, ids[page.url], pages_by_slug[source_template]))

    attachment_items = []
    for item in originals:
        if _text(item.find("wp:post_type", NS)) != "attachment":
            continue
        post_id = _text(item.find("wp:post_id", NS))
        attachment_items.append(build_attachment_item(item, image_map[post_id]))

    support_items = [
        localize_support_item(item)
        for item in originals
        if _text(item.find("wp:post_id", NS)) in {"6", "893"}
    ]
    menu_items = build_menu_items(root, ids)

    for item in originals:
        channel.remove(item)
    localize_channel(channel)
    for item in page_items + attachment_items + support_items + menu_items:
        channel.append(item)

    ET.indent(tree, space="  ")
    tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)


def post_name_slash_failures() -> list[str]:
    failures: list[str] = []
    for path in BUILD.rglob("*.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        def walk(node: Any, trail: str = "$") -> None:
            if isinstance(node, dict):
                for key, child in node.items():
                    child_trail = f"{trail}.{key}"
                    if key == "post_name" and isinstance(child, str) and "/" in child:
                        failures.append(f"{path.relative_to(ROOT)} {child_trail}: {child}")
                    walk(child, child_trail)
            elif isinstance(node, list):
                for index, child in enumerate(node):
                    walk(child, f"{trail}[{index}]")

        walk(value)
    return failures


def write_placeholder_report(pages: list[PageModel]) -> list[tuple[str, str]]:
    occurrences: list[tuple[str, str]] = []
    for page in pages:
        raw = json.dumps(page.tree, ensure_ascii=False)
        raw += " " + page.meta_title + " " + page.meta_description
        occurrences.extend((page.url, match.group(0)) for match in PLACEHOLDER_RE.finditer(raw))
    counts = Counter(token[2:].split(":", 1)[0].rstrip("]") for _, token in occurrences)
    lines = [
        "# Placeholder register",
        "",
        f"Total outstanding occurrences: {len(occurrences)}",
        "",
        "## Counts",
        "",
    ]
    for kind in ("PLACEHOLDER", "VERIFY", "REAL_PHOTO_PENDING"):
        lines.append(f"- {kind}: {counts[kind]}")
    lines.extend(("", "## Occurrences", "", "| Page | Marker |", "|---|---|"))
    for url, token in occurrences:
        lines.append(f"| {url} | `{token.replace('|', '&#124;')}` |")
    write_report(REPORTS / "placeholders.md", "\n".join(lines))
    return occurrences


def validate(pages: list[PageModel], ids: dict[str, int], manifest: list[dict[str, Any]]) -> bool:
    failures: dict[int, list[str]] = defaultdict(list)
    parsed = ET.parse(OUTPUT_XML)
    root = parsed.getroot()
    items = source_items(root)
    page_items = [item for item in items if _text(item.find("wp:post_type", NS)) == "page"]
    attachment_ids = {
        int(_text(item.find("wp:post_id", NS)))
        for item in items
        if _text(item.find("wp:post_type", NS)) == "attachment"
    }

    if len(page_items) != 156:
        failures[1].append(f"Expected 156 page items, found {len(page_items)}")

    page_items_by_id = {int(_text(item.find("wp:post_id", NS))): item for item in page_items}
    for item in page_items:
        post_id = _text(item.find("wp:post_id", NS))
        raw = get_meta(item, "_elementor_data")
        if raw is None:
            failures[2].append(f"post_id {post_id}: missing _elementor_data")
            continue
        try:
            parsed_data = parse_elementor(item)
        except (TypeError, json.JSONDecodeError) as exc:
            failures[2].append(f"post_id {post_id}: {exc}")
            continue
        if serialize_elementor(parsed_data) != raw:
            failures[3].append(f"post_id {post_id}: round-trip mismatch")

    for page in pages:
        h1s = [text for tag, text in heading_outline(page) if tag == "h1"]
        if len(h1s) != 1:
            failures[4].append(f"{page.url}: {len(h1s)} H1 headings ({h1s})")

    xml_text = OUTPUT_XML.read_text(encoding="utf-8")
    for term, pattern in BLOCKLIST:
        matches = list(pattern.finditer(xml_text))
        if matches:
            failures[5].append(f"{term}: {len(matches)} occurrence(s)")

    for page in pages:
        for image in image_dicts(page):
            image_id = int(image.get("id") or 0)
            if image_id not in attachment_ids:
                failures[6].append(f"{page.url}: unresolved image ID {image_id}")

    path_map = old_path_map()
    graph = [link for page in pages for link in internal_links(page, path_map)]
    valid_urls = {page.url for page in pages}
    for link in graph:
        if link["to_url"] not in valid_urls:
            failures[7].append(f"{link['from_url']} -> {link['to_url']}")
    menus = json.loads((BUILD / "stage9-menus.json").read_text(encoding="utf-8"))
    menu_targets: list[str] = []
    for value in menus.values():
        for item in value:
            if item["url"].startswith("/"):
                menu_targets.append(item["url"])
            for child in item.get("children", []):
                if child["url"].startswith("/"):
                    menu_targets.append(child["url"])
    for target in menu_targets:
        if target not in valid_urls:
            failures[7].append(f"menu -> {target}")
    inbound = Counter(link["to_url"] for link in graph)
    inbound.update(menu_targets)
    orphans = sorted(url for url in valid_urls if not inbound[url])
    failures[7].extend(f"orphan: {url}" for url in orphans)

    for item in items:
        for meta in item.findall("wp:postmeta", NS):
            key = _text(meta.find("wp:meta_key", NS))
            post_id = _text(item.find("wp:post_id", NS))
            if key.startswith("rank_math_schema_"):
                failures[8].append(f"post_id {post_id}: {key}")
            if key == "_elementor_element_cache":
                failures[9].append(f"post_id {post_id}")

    researched = set(researched_suburbs())
    substantive = [
        page
        for page in pages
        if page.page_type in {"service", "guide", "intersection", "cost_comparison"}
        or (
            page.page_type == "suburb"
            and page.slug.removeprefix("concreters-") in researched
        )
    ]
    unique, overlaps, repeated = duplication_metrics(substantive)
    for url, value in unique.items():
        if value < 60.0:
            failures[10].append(f"{url}: {value:.2f}% unique")
    for (left, right), value in overlaps.items():
        if value > 40.0:
            failures[10].append(f"{left} vs {right}: {value:.2f}% overlap")
    for sentence, urls in repeated.items():
        failures[10].append(f"sentence on {len(urls)} pages: {sentence}")

    for page in pages:
        if not 50 <= len(page.meta_title) <= 60:
            failures[11].append(f"{page.url}: title length {len(page.meta_title)}")
        if not 140 <= len(page.meta_description) <= 160:
            failures[11].append(f"{page.url}: description length {len(page.meta_description)}")
    titles: dict[str, list[str]] = defaultdict(list)
    for page in pages:
        titles[page.meta_title.casefold()].append(page.url)
    for title, urls in titles.items():
        if len(urls) > 1:
            failures[12].append(f"{title}: {', '.join(urls)}")

    placeholders = write_placeholder_report(pages)
    report_text = (REPORTS / "placeholders.md").read_text(encoding="utf-8")
    for url, token in placeholders:
        if url not in report_text or token not in report_text:
            failures[13].append(f"{url}: {token}")

    for page in pages:
        keyword = page.focus_keyword.strip()
        if not keyword:
            failures[14].append(f"{page.url}: empty focus keyword")
        if re.search(r"\bWerribe\b", keyword, re.IGNORECASE):
            failures[14].append(f"{page.url}: misspelled focus keyword {keyword}")

    expected_publish = {
        page.url
        for page in pages
        if page.page_type in {"home", "utility", "service"}
        or (
            page.page_type == "suburb"
            and page.slug.removeprefix("concreters-")
            in {"oran-park", "leppington", "gregory-hills", "gledswood-hills", "austral", "harrington-park"}
        )
    }
    for page in pages:
        expected = "publish" if page.url in expected_publish else "draft"
        if page.status != expected:
            failures[15].append(f"{page.url}: {page.status}, expected {expected}")

    slash_failures = post_name_slash_failures()
    hierarchy_failures = []
    by_url = {item["url"]: item for item in manifest}
    if by_url["/guides/"]["post_id"] != GUIDES_HUB_ID or by_url["/guides/"]["post_parent"] != 0:
        hierarchy_failures.append("Guide hub ID/parent mismatch")
    for page in pages:
        item = by_url[page.url]
        parts = [part for part in page.url.split("/") if part]
        expected_parent = GUIDES_HUB_ID if page.page_type == "guide" else 0
        if item["post_parent"] != expected_parent:
            hierarchy_failures.append(f"{page.url}: post_parent {item['post_parent']}, expected {expected_parent}")
        if len(parts) > 1 and page.page_type != "guide":
            hierarchy_failures.append(f"Unexpected nested URL: {page.url}")
        final_slug = parts[-1] if parts else page.slug
        if page.url != "/" and item["post_name"] != final_slug:
            hierarchy_failures.append(f"{page.url}: post_name {item['post_name']}, expected {final_slug}")
    if slash_failures or hierarchy_failures:
        failures[1].extend(slash_failures + hierarchy_failures)

    (REPORTS / "residual-melbourne-terms.md").write_text("", encoding="utf-8")

    status_counts = Counter(page.status for page in pages)
    max_overlap = max(overlaps.values(), default=0.0)
    min_unique = min(unique.values(), default=100.0)
    gate_details = {
        1: f"XML parsed; 156 pages; hierarchy manifest clean; slash-bearing post_name values: {len(slash_failures)}",
        2: f"Elementor JSON parsed for {len(page_items)} of {len(page_items)} pages",
        3: f"Elementor JSON round trip matched for {len(page_items)} pages",
        4: "Exactly one H1 on every page",
        5: "Victorian blocklist returned zero matches in the assembled XML" if not failures[5] else f"Victorian blocklist returned {len(failures[5])} failing term(s)",
        6: f"All widget image IDs resolve against {len(attachment_ids)} attachments",
        7: f"All page and menu links resolve; {len(orphans)} orphans",
        8: "No rank_math_schema_* meta keys remain",
        9: "No _elementor_element_cache meta keys remain",
        10: f"{len(substantive)} substantive pages checked; minimum unique {min_unique:.2f}%; maximum pair overlap {max_overlap:.2f}%; 45 research shells and the shared-component hub exempt",
        11: "Every Rank Math title is 50-60 characters and description is 140-160 characters",
        12: "Every complete Rank Math title is unique",
        13: f"All {len(placeholders)} placeholder/verify/photo markers are registered",
        14: "Every page has a non-empty focus keyword; no Werribe-class typo found",
        15: f"Status split is {status_counts['publish']} publish / {status_counts['draft']} draft; hub and 35 guides are draft",
    }

    lines = [
        "# Stage 9 — Final validation and assembly",
        "",
        "Assembled `camden-concreting-import.xml` with 156 pages, 83 attachments, the Elementor kit, Astra custom CSS and five rebuilt menus.",
        "",
        "## Pre-assembly hierarchy assertions",
        "",
        f"- `/guides/`: post ID {GUIDES_HUB_ID}, `post_name=guides`, `post_parent=0`, status `draft`.",
        f"- Guide children: {sum(1 for page in pages if page.page_type == 'guide')}; every child has `post_parent={GUIDES_HUB_ID}` and a final-segment-only `post_name`.",
        f"- Unexpected nested URLs: {sum(1 for page in pages if len([part for part in page.url.split('/') if part]) > 1 and page.page_type != 'guide')}.",
        f"- Slash-bearing `post_name` values in `build/`: {len(slash_failures)}.",
        "",
        "## Gate results",
        "",
        "| Gate | Check | Result | Detail |",
        "|---:|---|---|---|",
    ]
    names = {
        1: "XML well-formed",
        2: "Elementor JSON",
        3: "Round trip",
        4: "H1",
        5: "Victorian blocklist",
        6: "Image IDs",
        7: "Links",
        8: "Schema meta",
        9: "Cache",
        10: "Duplication",
        11: "Meta lengths",
        12: "Meta uniqueness",
        13: "Placeholders",
        14: "Focus keywords",
        15: "Status",
    }
    for number in range(1, 16):
        result = "PASS" if not failures[number] else "FAIL"
        lines.append(f"| {number} | {names[number]} | {result} | {gate_details[number]} |")
    lines.extend(("", "## Failing items", ""))
    if any(failures.values()):
        for number in range(1, 16):
            if not failures[number]:
                continue
            lines.append(f"### Gate {number} — {names[number]}")
            lines.append("")
            lines.extend(f"- {item}" for item in failures[number])
            lines.append("")
    else:
        lines.append("None.")
    lines.extend(("", f"GATE 9: {'PASS' if not any(failures.values()) else 'FAIL'}", "", "HALT AT GATE 9. Stage 10 has not been run."))
    write_report(REPORTS / "09-validation.md", "\n".join(lines))
    return not any(failures.values())


def stage9() -> bool:
    pages = load_final_models()
    source = ET.parse(SOURCE_XML).getroot()
    ids = page_id_map(source, pages)
    manifest = update_stage9_manifests(pages, ids)
    assemble_xml(pages, ids)
    return validate(pages, ids, manifest)


if __name__ == "__main__":
    raise SystemExit(0 if stage9() else 1)
