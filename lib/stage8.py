from __future__ import annotations

import copy
import csv
import html
import json
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from lib.site_builder import (
    BUILD,
    REPORTS,
    ROOT,
    SERVICE_DEFINITIONS,
    SERVICE_URLS,
    TIER1,
    PageModel,
    expanded_suburbs,
    load_page_models,
    paragraphs,
    read_json,
    researched_suburbs,
    text_editor_nodes,
    write_json,
    write_report,
)
from lib.stage3_gate import iter_nodes
from lib.wxr import NS, get_meta, load_xml


NEW_DOMAIN = "https://concreterscamden.com.au"
OLD_DOMAINS = {
    "bestconcretersmelbourne.com.au",
    "www.bestconcretersmelbourne.com.au",
}

MENU_SERVICE_URLS = (
    SERVICE_URLS["driveways"],
    SERVICE_URLS["slabs"],
    SERVICE_URLS["exposed"],
    SERVICE_URLS["decorative"],
    SERVICE_URLS["patios"],
    SERVICE_URLS["paths"],
    SERVICE_URLS["commercial"],
)

MENU_GUIDE_URLS = (
    "/guides/concrete-driveway-cost-nsw/",
    "/guides/camden-council-driveway-crossing/",
    "/guides/liverpool-council-vehicle-crossing/",
    "/guides/why-concrete-cracks/",
    "/guides/reactive-clay-slabs-as2870/",
    "/guides/salinity-and-concrete-western-sydney/",
)

SERVICE_WEIGHT_KEYS = {
    SERVICE_URLS["driveways"]: "new_build",
    SERVICE_URLS["replacement"]: "replacement",
    SERVICE_URLS["slabs"]: "new_build",
    SERVICE_URLS["shed"]: "new_build",
    SERVICE_URLS["exposed"]: "decorative",
    SERVICE_URLS["decorative"]: "decorative",
    SERVICE_URLS["patios"]: "new_build",
    SERVICE_URLS["paths"]: "replacement",
    SERVICE_URLS["crossovers"]: "new_build",
    SERVICE_URLS["commercial"]: "commercial",
}

TOPICAL_GUIDES = {
    "oran-park": "/guides/engineered-fill-and-why-new-estate-slabs-crack/",
    "leppington": "/guides/reactive-clay-slabs-as2870/",
    "gregory-hills": "/guides/commercial-hardstand-cost/",
    "gledswood-hills": "/guides/salinity-and-concrete-western-sydney/",
    "austral": "/guides/engineered-fill-and-why-new-estate-slabs-crack/",
    "harrington-park": "/guides/concrete-repair-vs-replace/",
    "catherine-field": "/guides/site-classification-explained/",
    "narellan": "/guides/concrete-repair-vs-replace/",
    "mount-annan": "/guides/concrete-crack-types-and-which-matter/",
    "currans-hill": "/guides/control-joints-and-saw-cut-timing/",
    "spring-farm": "/guides/why-concrete-cracks/",
    "elderslie": "/guides/reactive-clay-slabs-as2870/",
    "cobbitty": "/guides/site-classification-explained/",
    "edmondson-park": "/guides/engineered-fill-and-why-new-estate-slabs-crack/",
    "bringelly": "/guides/commercial-hardstand-cost/",
}

COST_PARENT_SERVICES = {
    "/driveway-cost-calculator/": SERVICE_URLS["driveways"],
    "/slab-volume-calculator/": SERVICE_URLS["slabs"],
    "/concrete-vs-pavers/": SERVICE_URLS["driveways"],
    "/concrete-vs-asphalt/": SERVICE_URLS["driveways"],
    "/exposed-aggregate-vs-plain-concrete/": SERVICE_URLS["exposed"],
    "/diy-concrete-vs-hiring-a-concreter/": SERVICE_URLS["commercial"],
    "/plain-concrete-driveway-cost/": SERVICE_URLS["driveways"],
    "/exposed-aggregate-driveway-cost/": SERVICE_URLS["exposed"],
    "/coloured-concrete-driveway-cost/": SERVICE_URLS["decorative"],
    "/stencilled-concrete-driveway-cost/": SERVICE_URLS["decorative"],
}

LOGO_ATTACHMENT_IDS = {159, 177, 250, 272, 306, 307, 308, 309, 422, 468, 469, 471, 472}


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.current_href: str | None = None
        self.current_text: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a" or self.current_href is not None:
            return
        self.current_href = dict(attrs).get("href")
        self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self.current_href is not None:
            self.links.append(
                (self.current_href, re.sub(r"\s+", " ", "".join(self.current_text)).strip())
            )
            self.current_href = None
            self.current_text = []


def strip_markup(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value))).strip()


def module_from_path(path: str) -> str:
    match = re.match(r"\$\[(\d+)\]", path)
    return f"section-{int(match.group(1)) + 1}" if match else "unknown"


def old_path_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    direct = read_json(BUILD / "url-map.json")["direct_transformations"]
    for source, target in direct.items():
        source_path = "/" if source == "homepage" else f"/{source}/"
        mapping[source_path] = target["url"]
    return mapping


def normalize_link(url: str, path_map: dict[str, str]) -> str:
    value = html.unescape(url).strip()
    if not value or value.startswith(("#", "tel:", "mailto:", "sms:")):
        return value
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https"):
        if parsed.netloc.lower() not in OLD_DOMAINS | {"concreterscamden.com.au", "www.concreterscamden.com.au"}:
            return value
        value = parsed.path or "/"
    if not value.startswith("/"):
        return value
    path = value.split("?", 1)[0].split("#", 1)[0]
    if path != "/" and not path.endswith("/") and "." not in Path(path).name:
        path += "/"
    return path_map.get(path, path)


def rewrite_existing_links(page: PageModel, path_map: dict[str, str]) -> None:
    replacements: list[tuple[str, str]] = []
    for old_path, new_path in path_map.items():
        for scheme in ("http", "https"):
            replacements.append((f"{scheme}://bestconcretersmelbourne.com.au{old_path}", new_path))
        replacements.append((old_path, new_path))
    replacements.sort(key=lambda item: len(item[0]), reverse=True)
    for _, node in iter_nodes(page.tree):
        settings = node.get("settings")
        if not isinstance(settings, dict):
            continue
        if node.get("widgetType") == "text-editor" and isinstance(settings.get("editor"), str):
            editor = settings["editor"]
            for old, new in replacements:
                editor = editor.replace(old, new)
            settings["editor"] = editor
        link = settings.get("link")
        if isinstance(link, dict) and isinstance(link.get("url"), str):
            link["url"] = normalize_link(link["url"], path_map)


def localize_repeated_copy(page: PageModel) -> None:
    for widget in text_editor_nodes(page.tree):
        editor = widget["settings"].get("editor", "")
        editor = editor.replace(
            "Related sources and project paths are ",
            f"Related sources for {html.escape(page.title)} are ",
        )
        if page.page_type == "suburb" and "REQUIRED-RESEARCH" in editor:
            suburb_name = page.title.removeprefix("Concreters ")
            editor = editor.replace(
                "The recorded council specification is reproduced without alteration:",
                f"The recorded {html.escape(suburb_name)} council specification is reproduced without alteration:",
            )
        widget["settings"]["editor"] = editor
    if page.page_type == "suburb":
        return
    question_lenses = (
        "site evidence",
        "approval record",
        "ground support",
        "finished levels",
        "cost basis",
        "handover check",
    )
    for _, node in iter_nodes(page.tree):
        if node.get("widgetType") != "nested-accordion":
            continue
        settings = node.get("settings", {})
        for index, item in enumerate(settings.get("items", [])):
            lens = question_lenses[index % len(question_lenses)]
            item["item_title"] = f"What does the {lens} require for {page.title}?"


def append_context(page: PageModel, editor_index: int, sentence: str) -> None:
    editors = text_editor_nodes(page.tree)
    if not editors:
        raise AssertionError(f"No editor available on {page.url}")
    editor = editors[editor_index % len(editors)]["settings"]
    if sentence not in editor.get("editor", ""):
        editor["editor"] = editor.get("editor", "") + paragraphs(sentence)


def service_definition(url: str) -> dict[str, str]:
    return next(item for item in SERVICE_DEFINITIONS if f'/{item["slug"]}/' == url)


def highest_weight_suburbs(service_url: str) -> list[dict[str, Any]]:
    key = SERVICE_WEIGHT_KEYS[service_url]
    records = list(researched_suburbs().values())
    tier_order = {slug: index for index, slug in enumerate(TIER1)}
    records.sort(
        key=lambda item: (
            -float(item.get("job_mix_weighting", {}).get(key, 0)),
            tier_order.get(item["slug"], len(TIER1)),
            item["name"],
        )
    )
    return records[:6]


def enforce_service_suburb_links(page: PageModel) -> None:
    definition = service_definition(page.url)
    anchors = [
        f'<a href="/concreters-{record["slug"]}/">{html.escape(definition["name"])} {html.escape(record["name"])}</a>'
        for record in highest_weight_suburbs(page.url)
    ]
    sentence = f"Highest-weight researched areas for this service are {natural_list(anchors)}."
    editors = text_editor_nodes(page.tree)
    target = editors[8 % len(editors)]["settings"]
    editor = target.get("editor", "")
    pattern = r"\s*Relevant Tier 1 examples are .*?(?=</p>)"
    if re.search(pattern, editor, flags=re.DOTALL):
        target["editor"] = re.sub(pattern, f" {sentence}", editor, count=1, flags=re.DOTALL)
    else:
        target["editor"] = editor + paragraphs(sentence)


def natural_list(values: Iterable[str]) -> str:
    items = list(values)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def council_guide(record: dict[str, Any], expanded: dict[str, dict[str, Any]]) -> str:
    return expanded[record["slug"]]["lga_crossing_guide"]


def add_researched_suburb_guides(pages: dict[str, PageModel]) -> None:
    expanded = expanded_suburbs()
    for slug, record in researched_suburbs().items():
        page = pages[f"/concreters-{slug}/"]
        guides = (council_guide(record, expanded), TOPICAL_GUIDES[slug])
        for index, guide_url in enumerate(dict.fromkeys(guides)):
            if guide_url in " ".join(
                widget["settings"].get("editor", "") for widget in text_editor_nodes(page.tree)
            ):
                continue
            guide = pages[guide_url]
            anchor = (
                f"{record['name']} council crossing requirements"
                if "council" in guide_url
                else f"{guide.title.lower()} reference for {record['name']}"
            )
            append_context(
                page,
                5 + index,
                f'{html.escape(record["name"])} uses the <a href="{guide_url}">{html.escape(anchor)}</a> when the {html.escape(record["name"])} evidence reaches that topic; the lot record still controls the decision.',
            )


def add_intersection_inbound_links(pages: dict[str, PageModel]) -> None:
    records = read_json(ROOT / "intersection-differentiators.json")["intersections"]
    per_suburb: Counter[str] = Counter()
    for record in records:
        parent = pages[record["parent_suburb"]]
        target = pages[record["url"]]
        suburb_name = researched_suburbs()[record["suburb"]]["name"]
        definition = next(
            item
            for item in SERVICE_DEFINITIONS
            if item["slug"] == f'{record["service"]}-south-west-sydney'
        )
        append_context(
            parent,
            3 + per_suburb[record["suburb"]],
            f'{html.escape(suburb_name)} separates its {html.escape(definition["name"].lower())} evidence from the general {html.escape(suburb_name)} brief; <a href="{target.url}">{html.escape(definition["name"])} in {html.escape(suburb_name)}</a> carries that service decision.',
        )
        per_suburb[record["suburb"]] += 1


def guide_parent_service(guide: PageModel) -> str:
    slug = guide.slug
    if any(term in slug for term in ("council", "crossing", "approval", "crossover")):
        return SERVICE_URLS["crossovers"]
    if any(term in slug for term in ("aggregate", "stencil", "coloured", "honed", "broom", "non-slip", "sealing")):
        return SERVICE_URLS["exposed"] if "aggregate" in slug else SERVICE_URLS["decorative"]
    if any(term in slug for term in ("slab", "fill", "classification", "strength", "sl72", "joint", "clay", "salinity")):
        return SERVICE_URLS["slabs"]
    if any(term in slug for term in ("repair", "crack", "curing", "efflorescence", "oil", "drive-on")):
        return SERVICE_URLS["replacement"]
    return SERVICE_URLS["driveways"]


def internal_links(page: PageModel, path_map: dict[str, str]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for path, node in iter_nodes(page.tree):
        settings = node.get("settings")
        if not isinstance(settings, dict):
            continue
        if node.get("widgetType") == "text-editor" and isinstance(settings.get("editor"), str):
            parser = AnchorParser()
            parser.feed(settings["editor"])
            for url, anchor in parser.links:
                target = normalize_link(url, path_map)
                if target.startswith("/") and not target.startswith("/wp-content/"):
                    links.append(
                        {
                            "from_url": page.url,
                            "to_url": target,
                            "anchor_text": anchor or "linked text",
                            "module": module_from_path(path),
                        }
                    )
        link = settings.get("link")
        if isinstance(link, dict) and isinstance(link.get("url"), str):
            target = normalize_link(link["url"], path_map)
            if target.startswith("/") and not target.startswith("/wp-content/"):
                anchor = settings.get("text") or settings.get("title_text") or node.get("widgetType", "link")
                links.append(
                    {
                        "from_url": page.url,
                        "to_url": target,
                        "anchor_text": strip_markup(str(anchor)),
                        "module": module_from_path(path),
                    }
                )
    return links


def add_unlinked_guide_inbound(pages: dict[str, PageModel], path_map: dict[str, str]) -> None:
    graph = [link for page in pages.values() for link in internal_links(page, path_map)]
    inbound = Counter(link["to_url"] for link in graph)
    service_counters: Counter[str] = Counter()
    for guide in sorted(
        (page for page in pages.values() if page.page_type == "guide"),
        key=lambda page: page.url,
    ):
        if inbound[guide.url]:
            continue
        service_url = guide_parent_service(guide)
        source = pages[service_url]
        append_context(
            source,
            2 + service_counters[service_url],
            f'The evidence behind this decision is set out in <a href="{guide.url}">{html.escape(guide.title)}</a> before it is applied to a project scope.',
        )
        service_counters[service_url] += 1


def add_cost_inbound(pages: dict[str, PageModel]) -> None:
    counters: Counter[str] = Counter()
    for cost_url, service_url in COST_PARENT_SERVICES.items():
        cost = pages[cost_url]
        source = pages[service_url]
        append_context(
            source,
            11 + counters[service_url],
            f'The commercial inputs are separated in <a href="{cost.url}">{html.escape(cost.title)}</a> rather than presented as an unsupported universal price.',
        )
        counters[service_url] += 1


def attachment_records() -> list[dict[str, Any]]:
    xml = load_xml(ROOT / "source" / "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml")
    channel = xml.getroot().find("channel")
    if channel is None:
        raise AssertionError("Source WXR channel missing")
    records: list[dict[str, Any]] = []
    for item in channel.findall("item"):
        if item.findtext("wp:post_type", namespaces=NS) != "attachment":
            continue
        post_id = int(item.findtext("wp:post_id", namespaces=NS) or 0)
        old_url = item.findtext("wp:attachment_url", namespaces=NS) or ""
        old_file = get_meta(item, "_wp_attached_file") or Path(urlparse(old_url).path).name
        records.append(
            {
                "post_id": post_id,
                "old_url": old_url,
                "old_file": old_file,
                "old_filename": Path(old_file).name,
                "title": item.findtext("title") or "",
            }
        )
    return sorted(records, key=lambda record: record["post_id"])


def renamed_stem(record: dict[str, Any]) -> str:
    stem = Path(record["old_filename"]).stem.lower()
    special = {
        "tarneit-soil": "wianamatta-shale-clay-camden",
        "melbournes-west": "south-west-sydney-growth-corridor",
        "crossovers": "camden-council-driveway-crossing",
        "werribee-town": "camden-town-centre",
        "new-estates-werribee": "oran-park-growth-estate",
        "excavation-werribee": "driveway-excavation-camden",
        "davis-creek-tarneit": "south-creek-drainage-corridor",
        "1970s-home-hoppers-crossing": "established-home-mount-annan",
        "hoppers-crossing-aerial-shot": "mount-annan-established-housing",
        "truganina-commercial": "gregory-hills-commercial-concreting",
        "new-estates-truganina": "leppington-new-estates",
        "crossovers-concrete-truganina": "council-crossing-south-west-sydney",
        "exposed-aggregate-adelaide": "exposed-aggregate-south-west-sydney",
    }
    if stem in special:
        base = special[stem]
    elif re.fullmatch(r"[a-f0-9]{32,}", stem):
        base = "concrete-project-detail-camden"
    elif any(term in stem for term in ("logo", "favicon", "eandtcologo", "e-t-co")):
        base = "structure co-concreters-camden-logo"
    else:
        base = stem
        replacements = (
            ("melbournes-west", "south-west-sydney"),
            ("melbourne", "south-west-sydney"),
            ("werribee", "camden"),
            ("weribee", "camden"),
            ("point-cook", "oran-park"),
            ("pointcook", "oran-park"),
            ("tarneit", "oran-park"),
            ("truganina", "gregory-hills"),
            ("hoppers-crossing", "mount-annan"),
            ("adelaide", "south-west-sydney"),
            ("cocnrete", "concrete"),
            ("cocnreer", "concrete"),
            ("concrtee", "concrete"),
            ("copncrete", "concrete"),
            ("drivewya", "driveway"),
            ("pathsandpathwasy", "paths-and-pathways"),
            ("exension", "extension"),
            ("colourdanddetailedconcrete", "coloured-detailed-concrete"),
        )
        for old, new in replacements:
            base = base.replace(old, new)
        base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
        if not any(
            term in base
            for term in ("camden", "oran-park", "gregory-hills", "mount-annan", "south-west-sydney", "structure co", "wianamatta", "south-creek")
        ):
            base += "-camden"
    return f"{base}-{record['post_id']}"


def build_image_map(records: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    output: dict[int, dict[str, Any]] = {}
    for record in records:
        suffix = Path(record["old_filename"]).suffix.lower() or ".jpg"
        filename = renamed_stem(record) + suffix
        directory = str(Path(record["old_file"]).parent).replace("\\", "/")
        if directory == ".":
            directory = "2026/07"
        output[record["post_id"]] = {
            **record,
            "new_filename": filename,
            "new_file": f"{directory}/{filename}",
            "new_url": f"{NEW_DOMAIN}/wp-content/uploads/{directory}/{filename}",
            "base_alt": re.sub(r"\s+", " ", renamed_stem(record).rsplit("-", 1)[0].replace("-", " ")).strip().capitalize(),
        }
    return output


def image_dicts(page: PageModel) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for _, node in iter_nodes(page.tree):
        settings = node.get("settings")
        if isinstance(settings, dict) and isinstance(settings.get("image"), dict):
            image = settings["image"]
            if image.get("id") or image.get("url"):
                output.append(image)
    return output


def assign_images(pages: list[PageModel], image_map: dict[int, dict[str, Any]]) -> dict[int, set[str]]:
    content_pool = [record for post_id, record in image_map.items() if post_id not in LOGO_ATTACHMENT_IDS]
    assignment_index = 0
    usage: dict[int, set[str]] = defaultdict(set)
    for page in sorted(pages, key=lambda item: item.url):
        assigned: dict[str, dict[str, Any]] = {}
        for image in image_dicts(page):
            old_key = str(image.get("id") or image.get("url") or len(assigned))
            if old_key not in assigned:
                old_id = int(image.get("id") or 0)
                if old_id in LOGO_ATTACHMENT_IDS and old_id in image_map:
                    assigned[old_key] = image_map[old_id]
                else:
                    assigned[old_key] = content_pool[assignment_index % len(content_pool)]
                    assignment_index += 1
            record = assigned[old_key]
            image["id"] = record["post_id"]
            image["url"] = record["new_url"]
            if record["post_id"] in LOGO_ATTACHMENT_IDS:
                image["alt"] = "Structure Co Concreters Camden logo"
            else:
                image["alt"] = f'{record["base_alt"]} in the context of {page.title}'
            usage[record["post_id"]].add(page.url)
    return usage


def menu_manifest(pages: dict[str, PageModel]) -> dict[str, Any]:
    tier_items = [
        {"title": researched_suburbs()[slug]["name"], "url": f"/concreters-{slug}/"}
        for slug in TIER1
    ]
    service_items = [
        {"title": service_definition(url)["name"], "url": url} for url in MENU_SERVICE_URLS
    ]
    guide_items = [{"title": pages[url].title, "url": url} for url in MENU_GUIDE_URLS]
    primary = [
        {"title": "Services", "url": "#", "children": service_items},
        {"title": "Areas", "url": "#", "children": tier_items},
        {"title": "Blog", "url": "#", "children": guide_items},
        {"title": "Contact", "url": "/contact/", "children": []},
    ]
    return {
        "primary": primary,
        "primary-2": copy.deepcopy(primary),
        "footer-areas": tier_items,
        "footer-services": service_items,
        "footer-blogs": guide_items,
    }


def write_csv(path: Path, headers: list[str], rows: Iterable[Iterable[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def stage8() -> bool:
    pages_list = load_page_models(BUILD / "stage7-all-pages.json")
    pages = {page.url: page for page in pages_list}
    path_map = old_path_map()
    for page in pages_list:
        rewrite_existing_links(page, path_map)
        localize_repeated_copy(page)
    for page in pages_list:
        if page.page_type == "service":
            enforce_service_suburb_links(page)
    add_researched_suburb_guides(pages)
    add_intersection_inbound_links(pages)
    add_unlinked_guide_inbound(pages, path_map)
    add_cost_inbound(pages)

    records = attachment_records()
    image_map = build_image_map(records)
    image_usage = assign_images(pages_list, image_map)
    menus = menu_manifest(pages)

    graph = [link for page in pages_list for link in internal_links(page, path_map)]
    valid_urls = set(pages)
    unresolved_links = [link for link in graph if link["to_url"] not in valid_urls]
    inbound = Counter(link["to_url"] for link in graph)
    orphans = sorted(url for url in valid_urls if not inbound[url])

    image_ids = set(image_map)
    unresolved_images: list[tuple[str, Any]] = []
    for page in pages_list:
        for image in image_dicts(page):
            if int(image.get("id") or 0) not in image_ids:
                unresolved_images.append((page.url, image.get("id")))

    suburb_mesh: dict[str, list[str]] = {}
    for page in pages_list:
        if page.page_type != "suburb":
            continue
        targets = sorted(
            {
                link["to_url"]
                for link in graph
                if link["from_url"] == page.url
                and link["to_url"].startswith("/concreters-")
            }
        )
        if len(targets) > 4:
            suburb_mesh[page.url] = targets

    max_image_pages = max((len(urls) for urls in image_usage.values()), default=0)
    menu_counts = {
        "primary_services": len(menus["primary"][0]["children"]),
        "primary_areas": len(menus["primary"][1]["children"]),
        "primary_blogs": len(menus["primary"][2]["children"]),
        "primary_2_services": len(menus["primary-2"][0]["children"]),
        "primary_2_areas": len(menus["primary-2"][1]["children"]),
        "primary_2_blogs": len(menus["primary-2"][2]["children"]),
        "footer_areas": len(menus["footer-areas"]),
        "footer_services": len(menus["footer-services"]),
        "footer_blogs": len(menus["footer-blogs"]),
    }
    menus_valid = menu_counts == {
        "primary_services": 7,
        "primary_areas": 6,
        "primary_blogs": 6,
        "primary_2_services": 7,
        "primary_2_areas": 6,
        "primary_2_blogs": 6,
        "footer_areas": 6,
        "footer_services": 7,
        "footer_blogs": 6,
    }

    write_json(BUILD / "stage8-all-pages.json", [page.as_dict() for page in pages_list])
    write_json(BUILD / "stage8-menus.json", menus)
    write_json(BUILD / "stage8-image-map.json", {str(key): value for key, value in image_map.items()})
    write_csv(
        REPORTS / "08-link-graph.csv",
        ["from_url", "to_url", "anchor_text", "module"],
        (
            (link["from_url"], link["to_url"], link["anchor_text"], link["module"])
            for link in sorted(
                graph,
                key=lambda item: (
                    item["from_url"],
                    item["to_url"],
                    item["module"],
                    item["anchor_text"],
                ),
            )
        ),
    )
    write_csv(
        REPORTS / "08-image-rename-map.csv",
        ["attachment_id", "old_filename", "new_filename", "pages_referencing"],
        (
            (
                post_id,
                record["old_filename"],
                record["new_filename"],
                " | ".join(sorted(image_usage.get(post_id, set()))),
            )
            for post_id, record in sorted(image_map.items())
        ),
    )
    (ROOT / "reencode-images.sh").write_text(
        """#!/usr/bin/env bash
set -euo pipefail

input_dir=${1:-uploads/2026/07}
output_dir=${2:-uploads-reencoded/2026/07}
mkdir -p "$output_dir"

tail -n +2 reports/08-image-rename-map.csv | while IFS=, read -r attachment_id old_filename new_filename pages; do
  old_filename=${old_filename%\"}; old_filename=${old_filename#\"}
  new_filename=${new_filename%\"}; new_filename=${new_filename#\"}
  magick "$input_dir/$old_filename" -resize 98% -strip -quality 82 "$output_dir/$new_filename"
done
""",
        encoding="utf-8",
        newline="\n",
    )

    passed = (
        len(pages_list) == 155
        and not unresolved_links
        and not orphans
        and not unresolved_images
        and not suburb_mesh
        and len(records) == 83
        and max_image_pages <= 15
        and menus_valid
    )
    lines = [
        "STAGE 8 — Links, menus, images",
        "=======================================",
        "READ:      CODEX-BUILD.md Stage 8; camden-site-structure-and-silo.md §4 and §7; codex-clone-prompt.md §6–§8; expansion-300-pages.md §9; Stage 7 page models",
        "DID:       Rewrote internal links, added contextual inbound paths for intersections/guides/cost pages, enforced six highest-weight suburb links per service, built the requested menu manifest, renamed 83 attachments, distributed image use, and rewrote page-specific alt text.",
        "ARTIFACTS: build/stage8-all-pages.json; build/stage8-menus.json; build/stage8-image-map.json; reports/08-link-graph.csv; reports/08-image-rename-map.csv; reencode-images.sh; reports/08-links.md",
        "",
        "## Link graph",
        "",
        f"- Internal link records: {len(graph)}",
        f"- Existing target URLs: {len(valid_urls)}",
        f"- Unresolved targets: {len(unresolved_links)}",
        f"- Orphan pages: {len(orphans)}",
        f"- Suburb pages exceeding four direct suburb neighbours: {len(suburb_mesh)}",
        "",
        "## Menus",
        "",
        f"- Primary and Primary (2): Services {menu_counts['primary_services']}, Areas {menu_counts['primary_areas']}, Blog {menu_counts['primary_blogs']}, Contact 1 each",
        f"- Footer: Areas {menu_counts['footer_areas']}, Services {menu_counts['footer_services']}, Blogs {menu_counts['footer_blogs']}",
        "- Primary parent/child relationships are represented explicitly in build/stage8-menus.json for Stage 9 assembly.",
        "",
        "## Images",
        "",
        f"- Attachment records renamed: {len(records)}",
        f"- Widget image IDs unresolved: {len(unresolved_images)}",
        f"- Maximum pages using one attachment: {max_image_pages}",
        "- Every assigned widget image URL names the attachment selected by its post ID.",
        "",
        f"GATE 8: {'PASS' if passed else 'FAIL'}",
        f"  {'✓' if not unresolved_links else '✗'} Every internal link target exists: {len(unresolved_links)} failures",
        f"  {'✓' if not orphans else '✗'} Zero orphan pages: {len(orphans)} orphans" + ("" if not orphans else f" — {', '.join(orphans)}"),
        f"  {'✓' if not unresolved_images else '✗'} Every image ID resolves to an attachment: {len(unresolved_images)} failures",
        f"  {'✓' if not suburb_mesh else '✗'} No suburb-to-suburb full mesh: {len(suburb_mesh)} violations",
        f"  {'✓' if max_image_pages <= 15 else '✗'} No attachment appears on more than 15 pages: maximum {max_image_pages}",
        f"  {'✓' if menus_valid else '✗'} Menu counts and parent groups match the Stage 8 specification: {json.dumps(menu_counts, ensure_ascii=False)}",
        "",
        "Proceeding to Stage 9." if passed else "HALTING. Stage 8 link, menu, or image gate failed.",
    ]
    if unresolved_links:
        lines.extend(("", "## Unresolved links", ""))
        lines.extend(
            f"- {item['from_url']} → {item['to_url']} ({item['anchor_text']})"
            for item in unresolved_links
        )
    write_report(REPORTS / "08-links.md", "\n".join(lines))
    return passed


if __name__ == "__main__":
    raise SystemExit(0 if stage8() else 1)
