"""Titles, breadcrumbs and near-me targeting spec — resolution layer.

Authority: the meta titles / breadcrumbs / near-me targeting spec supplied 24 August 2026,
as amended by DECISION-10 D42-D44. Reads `suburbs.json` (title_tag, meta_description,
postcode, tier, local entities) and `build/53-council-suburb-map.json` (evidence-supported
council per suburb, with citations and the public wording rule).

Nothing here invents a council figure, a price, a soil classification, a licence or a
turnaround time. Where the spec requires one of those, the value is withheld and a blocking
marker is emitted instead. See CLAUDE.md section 3 hard stop 6.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SUBURBS_JSON = ROOT / "suburbs.json"
COUNCIL_MAP = ROOT / "build" / "53-council-suburb-map.json"
VERIFIED_FACTS = ROOT / "data" / "verified-facts.yml"

BASE = "https://concreterscamden.com.au"

# ------------------------------------------------------------ telephone (D42-R1)

_facts = yaml.safe_load(VERIFIED_FACTS.read_text(encoding="utf-8"))
_contact = _facts["contact"]


class PhonePending(RuntimeError):
    """Raised when the build would emit a number that must not be published."""


def nsw_number_pending() -> bool:
    """DECISION-10 D42-R1 enforcement flag."""
    return bool(_contact["nsw_number_pending"]["value"])


def phone_display() -> str:
    """The published telephone, resolved from data/verified-facts.yml only."""
    require_deployable_phone()
    return str(_contact["phone_display"]["value"])


def phone_e164() -> str:
    require_deployable_phone()
    return str(_contact["phone_e164"]["value"])


def phone_uri() -> str:
    return "tel:" + phone_e164()


def require_deployable_phone() -> None:
    """Fail closed. This is the enforcement mechanism, not a warning.

    Nothing may be published while the NSW number is outstanding: the superseded (03)
    number is a Victorian area code on a Camden NSW site, and no number may be inferred
    to fill the gap (CLAUDE.md section 3 hard stop 6).
    """
    if nsw_number_pending():
        raise PhonePending(
            "NSW telephone number pending. data/verified-facts.yml -> "
            "contact.nsw_number_pending is true, so no deployable output may be written.\n"
            "  Set contact.phone_display.value  to the NSW number as it should read, "
            'e.g. "(02) NNNN NNNN"\n'
            "  Set contact.phone_e164.value     to the same number in E.164, "
            'e.g. "+612NNNNNNNN"\n'
            "  Set both verified: true with a source and sighted_date, then set "
            "contact.nsw_number_pending.value to false.\n"
            "  Authority: DECISION-10 D42-R1. Do not infer a number."
        )
    display = str(_contact["phone_display"]["value"]).strip()
    e164 = str(_contact["phone_e164"]["value"]).strip()
    if not display or not e164:
        raise PhonePending(
            "nsw_number_pending is false but contact.phone_display / contact.phone_e164 "
            "are empty in data/verified-facts.yml. Refusing to emit an empty telephone."
        )
    if not e164.startswith("+612"):
        raise PhonePending(
            f"contact.phone_e164 is {e164!r}; an NSW landline must begin '+612'. "
            "Refusing to publish a non-NSW area code (DECISION-10 D42-R1)."
        )
    if not re.match(r"^\(02\)\s?\d{4}\s?\d{4}$", display):
        raise PhonePending(
            f"contact.phone_display is {display!r}; expected the NSW form "
            '"(02) NNNN NNNN". Refusing to publish it.'
        )


#: strings that must never appear in deployable output. Section 4 checklist line 1.
FORBIDDEN_PHONE_PATTERNS = (
    r"\(03\)",
    r"\+61\s?3\b",
    r"\+613\d",
    r"\btel:\+613\d",
    r"\b03\s\d{4}\s?\d{4}\b",
)


def scan_forbidden_phone(text: str) -> list[str]:
    """Every forbidden telephone fragment in `text`, for the output gate."""
    hits: list[str] = []
    for pattern in FORBIDDEN_PHONE_PATTERNS:
        hits.extend(match.group(0) for match in re.finditer(pattern, text))
    return hits

# ---------------------------------------------------------------- source data

_spec_raw = json.loads(SUBURBS_JSON.read_text(encoding="utf-8"))
#: suburb slug (no page prefix) -> spec record, 16 entries incl. `camden`
SUBURB_SPEC: dict[str, dict] = {row["slug"]: row for row in _spec_raw["suburbs"]}

_council_raw = json.loads(COUNCIL_MAP.read_text(encoding="utf-8"))
#: suburb slug -> evidence record for all 60 built suburb pages
COUNCIL: dict[str, dict] = {row["suburb_slug"]: row for row in _council_raw["suburbs"]}

#: spec section 2 - the homepage carries `concreters camden`; no /concreters-camden/ page.
HOMEPAGE_SUBURB = "camden"

#: spec section 4 - Tier 1 is index,follow. Everything else in the suburb set is noindex,follow.
TIER1 = tuple(slug for slug, row in SUBURB_SPEC.items() if row["tier"] == 1)

# --------------------------------------------------------------- service move

# spec section 3: flat-root service URLs move under /services/. Eight map unambiguously.
# `concrete-slabs` -> house-slabs and `decorative-concrete` -> coloured-concrete are the two
# judgement calls recorded in reports/57-spec-conflicts.md C5.
# `stencilled-and-stamped-concrete` is a spec target with no source page and is NOT built.
SERVICE_MOVE: dict[str, tuple[str, str, str]] = {
    # old flat slug: (new slug under /services/, title tag, h1)
    "concrete-driveways-south-west-sydney": (
        "concrete-driveways",
        "Concrete Driveways | Camden & South West Sydney",
        "Concrete Driveways in Camden & South West Sydney",
    ),
    "concrete-crossovers-and-laybacks-south-west-sydney": (
        "driveway-crossovers",
        "Driveway Crossover Camden Council | Layback & Approval",
        "Driveway Crossovers & Council Laybacks",
    ),
    "concrete-slabs-south-west-sydney": (
        "house-slabs",
        "House Slabs & Footings | Camden & South West Sydney",
        "House Slabs & Footings",
    ),
    "shed-and-garage-slabs-south-west-sydney": (
        "shed-and-garage-slabs",
        "Shed & Garage Slabs | Camden & South West Sydney",
        "Shed & Garage Slabs",
    ),
    "exposed-aggregate-south-west-sydney": (
        "exposed-aggregate",
        "Exposed Aggregate Driveways | Camden & SW Sydney",
        "Exposed Aggregate Concrete",
    ),
    "decorative-concrete-south-west-sydney": (
        "coloured-concrete",
        "Coloured Concrete Driveways Camden | Oxide vs Topping",
        "Coloured Concrete",
    ),
    "concrete-patios-south-west-sydney": (
        "alfresco-and-patio-slabs",
        "Alfresco & Patio Slabs | Camden & South West Sydney",
        "Alfresco & Patio Slabs",
    ),
    "concrete-paths-south-west-sydney": (
        "concrete-paths-and-footpaths",
        "Concrete Paths & Footpaths | Camden & SW Sydney",
        "Concrete Paths & Footpaths",
    ),
    "concrete-driveway-replacement-south-west-sydney": (
        "concrete-removal-and-replacement",
        "Concrete Driveway Replacement Camden | Removal & Repour",
        "Concrete Removal & Replacement",
    ),
    "commercial-concreting-south-west-sydney": (
        "commercial-concreting",
        "Commercial Concreting South West Sydney | Hardstands",
        "Commercial Concreting & Hardstands",
    ),
}

#: spec section 6.2/6.4 — the terminal crumb is the short service name, not the H1.
SERVICE_CRUMB: dict[str, str] = {
    "concrete-driveways-south-west-sydney": "Concrete Driveways",
    "concrete-crossovers-and-laybacks-south-west-sydney": "Driveway Crossovers",
    "concrete-slabs-south-west-sydney": "House Slabs & Footings",
    "shed-and-garage-slabs-south-west-sydney": "Shed & Garage Slabs",
    "exposed-aggregate-south-west-sydney": "Exposed Aggregate",
    "decorative-concrete-south-west-sydney": "Coloured Concrete",
    "concrete-patios-south-west-sydney": "Alfresco & Patio Slabs",
    "concrete-paths-south-west-sydney": "Concrete Paths & Footpaths",
    "concrete-driveway-replacement-south-west-sydney": "Concrete Removal & Replacement",
    "commercial-concreting-south-west-sydney": "Commercial Concreting",
}

#: spec section 1 — 150-158 characters, names the service, carries one concrete specific,
#: ends on an action. Authored here rather than truncated from body copy.
SERVICE_DESCRIPTION: dict[str, str] = {
    "concrete-driveways-south-west-sydney": "Concrete driveways across Camden and South West Sydney. Thickness questions, finishes, and the Council crossover at the front of every job. Get a quote.",
    "concrete-crossovers-and-laybacks-south-west-sydney": "Driveway crossovers and laybacks in the Camden and Liverpool LGAs. Who applies, what Council inspects, why the layback set-out decides it. Start here.",
    "concrete-slabs-south-west-sydney": "House slabs and footings across Camden and South West Sydney. What the engineer fixes, what the site changes, what the builder confirms. Ask us first.",
    "shed-and-garage-slabs-south-west-sydney": "Shed and garage slabs across Camden and South West Sydney. Access into a finished yard, falls to the door, and what the shed supplier needs. Enquire now.",
    "exposed-aggregate-south-west-sydney": "Exposed aggregate driveways across Camden and South West Sydney. Stone choice, wash-off finish, sealing, and how it wears out the front. Request a quote.",
    "decorative-concrete-south-west-sydney": "Coloured concrete driveways across Camden and South West Sydney. Through-mix oxide against a coloured topping, and how each one ages. Compare them here.",
    "concrete-patios-south-west-sydney": "Alfresco and patio slabs across Camden and South West Sydney. Finished floor levels, falls away from the house, and the builder's step down. Talk to us.",
    "concrete-paths-south-west-sydney": "Concrete paths and footpaths across Camden and South West Sydney. Widths that actually work, side access past a wall, falls that move water. Get it priced.",
    "concrete-driveway-replacement-south-west-sydney": "Driveway removal and replacement across Camden and South West Sydney. Why the old slab failed, what comes out, and what changes on the repour. Ask today.",
    "commercial-concreting-south-west-sydney": "Commercial concreting and hardstands across South West Sydney. Warehouse floors, carparks and machinery pads, and the design that comes first. Enquire.",
}

#: spec target with no source content; recorded, not built.
UNBUILT_SERVICES = ("stencilled-and-stamped-concrete",)


def service_path(old_slug: str) -> str:
    """`/services/{new}/` for a flat-root service slug."""
    return "/services/" + SERVICE_MOVE[old_slug][0] + "/"


def rewrite_service_links(markup: str) -> str:
    """Point every internal link at the moved service URL."""
    for old, (new, _title, _h1) in SERVICE_MOVE.items():
        markup = markup.replace(f'href="/{old}/"', f'href="/services/{new}/"')
    return markup


def redirects_file() -> str:
    """Cloudflare `_redirects`. No chains: every source maps straight to its final URL."""
    lines = ["# spec section 3 and section 2. Generated by scripts/56-build-static-export.py."]
    for old, (new, _t, _h) in SERVICE_MOVE.items():
        lines.append(f"/{old}/ /services/{new}/ 301")
        lines.append(f"/{old} /services/{new}/ 301")
    # spec section 2: the homepage IS the Camden page. Defensive - the page is not built.
    lines.append("/concreters-camden/ / 301")
    lines.append("/concreters-camden / 301")
    return "\n".join(lines) + "\n"


# ---------------------------------------------- title promises (DECISION-10 D43-R1)

#: A word in a title tag is a promise. Each of these requires the matching content module
#: to be present on that page, declared as `data-module="..."` in the rendered HTML.
#: The gate fails the build on a mismatch, which prevents the class of defect rather than
#: the two instances that were found.
TITLE_PROMISES: dict[str, str] = {
    "cost": "pricing",
    "price": "pricing",
    "prices": "pricing",
    "pricing": "pricing",
    "$": "pricing",
    "quote": "quote-request",
    "thickness": "specification",
    "mesh": "specification",
    "specs": "specification",
}


def title_promises(title: str) -> dict[str, str]:
    """Trigger word -> required module, for one title tag."""
    found: dict[str, str] = {}
    for word, module in TITLE_PROMISES.items():
        pattern = re.escape(word) if word == "$" else r"(?<![a-z])" + re.escape(word) + r"(?![a-z])"
        if re.search(pattern, title, re.I):
            found[word] = module
    return found


# ------------------------------------------------------------- titles and H1s

HUB_META = {
    "/areas/": (
        "Areas We Service | Concreters Across Camden & SW Sydney",
        "Areas We Service",
        "Concreting suburb by suburb across the Camden LGA and South West Sydney. "
        "Estate context, the council pathway and the service mix in your street. Find yours.",
    ),
    "/services/": (
        "Concreting Services | Camden & South West Sydney",
        "Concreting Services",
        "Driveways, council crossovers, house and shed slabs, exposed aggregate, coloured "
        "concrete, patios, paths and hardstands across Camden. Start with your job.",
    ),
}

UTILITY_META = {
    "homepage": (
        "Concreters Camden | Driveways, Slabs & Crossovers",
        "Concreting in Camden, NSW",
        None,  # description resolved in the builder
    ),
    "about": (
        "About Structure Co | Camden Concreters",
        "About Structure Co",
        None,
    ),
    "contact": (
        "Contact | Concreters Camden | Structure Co",
        "Start a Concreting Quote in Camden",
        None,
    ),
    "quote": (
        "Request a Concreting Quote | Camden & SW Sydney",
        "Request a Quote",
        None,
    ),
    "gallery": (
        "Concrete Finishes Gallery | Camden & SW Sydney",
        "Concrete Finishes & Site Conditions",
        None,
    ),
    "privacy-policy": (
        "Privacy Policy | Concreters Camden | Structure Co",
        "Privacy Policy",
        None,
    ),
}


def area_name(page_slug: str) -> str:
    """Display name for a `concreters-x` page slug, spec spelling where we have it."""
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug) or COUNCIL.get(slug)
    if row:
        return row.get("name") or row.get("suburb") or slug.replace("-", " ").title()
    return slug.replace("-", " ").title()


def suburb_title(page_slug: str) -> str:
    """spec section 4 title_tag verbatim where the suburb is in scope."""
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug)
    if row:
        return row["title_tag"]
    return f"Concreters {area_name(page_slug)} | Driveways, Slabs & Paths"


def suburb_h1(page_slug: str) -> str:
    """DECISION-10 D43: spec H1 with the direct-performance claim removed."""
    return f"Concreting in {area_name(page_slug)}"


#: closing actions of varying length, so the generated fallback description lands inside
#: the spec's 150-158 window for suburb names from 4 to 17 characters.
_FALLBACK_TAILS = (
    "Tell us about the site and timing for a quote.",
    "Send the site details and timing for a quote.",
    "Send the dimensions, access notes and timing.",
    "Tell us about the site and we will quote it.",
    "Send the details and we will quote the job.",
    "Get the local context and a real quote.",
    "Send the site details and get a quote.",
    "Ask us for local context and a price.",
    "Request a quote for the actual site.",
    "Ask for a quote on the actual site.",
    "Ask for local context and a quote.",
    "Get a quote for the actual site.",
    "Get local context and a quote.",
    "Request a quote today.",
)


def suburb_description(page_slug: str) -> str:
    """spec section 1: meta_description from suburbs.json, verbatim, where it exists."""
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug)
    if row:
        return row["meta_description"]
    name = area_name(page_slug)
    core = (
        f"Concreting in {name} and across South West Sydney — driveways, shed and "
        f"garage slabs, paths and outdoor areas."
    )
    for tail in _FALLBACK_TAILS:
        candidate = f"{core} {tail}"
        if 150 <= len(candidate) <= 158:
            return candidate
    return core  # the section 1 length gate reports this rather than shipping it silently


def suburb_robots(page_slug: str) -> str:
    """spec section 4 + DECISION-10 D44: Tier 1 only is indexable."""
    slug = page_slug.removeprefix("concreters-")
    return "index,follow" if slug in TIER1 else "noindex,follow"


# ---------------------------------------------------------------- breadcrumbs

def crumbs_for(page_type: str, page_slug: str, label: str) -> list[tuple[str | None, str]]:
    """spec section 6.2. Max three levels; the last crumb is the current page, unlinked."""
    if page_type == "home":
        return []
    if page_type == "areas-hub":
        return [("/", "Home"), (None, "Areas")]
    if page_type == "services-hub":
        return [("/", "Home"), (None, "Services")]
    if page_type == "service":
        return [("/", "Home"), ("/services/", "Services"), (None, SERVICE_CRUMB.get(page_slug, label))]
    if page_type == "suburb":
        return [("/", "Home"), ("/areas/", "Areas"), (None, label)]
    if page_type == "404":
        return []
    return [("/", "Home"), (None, label)]


def crumb_markup(crumbs: list[tuple[str | None, str]]) -> str:
    """Visible trail. Labels are identical to the JSON-LD `name` sequence."""
    if not crumbs:
        return ""
    parts = []
    for url, label in crumbs:
        if url is None:
            parts.append(f'<span aria-current="page">{html.escape(label)}</span>')
        else:
            parts.append(f'<a href="{url}">{html.escape(label)}</a>')
    return (
        '<nav class="breadcrumbs" aria-label="Breadcrumb">'
        + " <span>/</span> ".join(parts)
        + "</nav>"
    )


def crumb_jsonld(crumbs: list[tuple[str | None, str]]) -> dict | None:
    """spec section 6.3/6.4. The terminal ListItem carries no `item`."""
    if not crumbs:
        return None
    items = []
    for position, (url, label) in enumerate(crumbs, 1):
        node: dict[str, object] = {"@type": "ListItem", "position": position, "name": label}
        if url is not None:
            node["item"] = BASE + url
        items.append(node)
    return {"@type": "BreadcrumbList", "itemListElement": items}


# -------------------------------------------------------- geographic relevance

def service_schema(page_slug: str) -> dict | None:
    """spec section 7.1. Emitted only where the postcode is a spec-supplied value.

    `provider` is deliberately absent: DECISION-08 D35 clause 4 does not authorise an
    Organization node, and a dangling @id reference would be worse than none.
    """
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug)
    if not row:
        return None
    return {
        "@type": "Service",
        "serviceType": "Concreting",
        "areaServed": {
            "@type": "Place",
            "name": row["name"],
            "address": {
                "@type": "PostalAddress",
                "addressLocality": row["name"],
                "addressRegion": "NSW",
                "postalCode": row["postcode"],
                "addressCountry": "AU",
            },
        },
    }


def council_sentence(page_slug: str) -> str:
    """Council wording that obeys `public_wording_rule` in 53-council-suburb-map.json."""
    slug = page_slug.removeprefix("concreters-")
    row = COUNCIL.get(slug)
    if not row:
        return (
            "Confirm the controlling council for the actual property before any frontage "
            "or crossing work is committed."
        )
    councils = row["evidence_supported_councils"]
    if row.get("lot_level_check_required") or len(councils) > 1:
        joined = " and ".join(councils)
        return (
            f"{row['suburb']} straddles the {joined} boundary, so the controlling council "
            f"has to be confirmed lot by lot in the NSW Planning Portal before a crossing "
            f"application is lodged."
        )
    return (
        f"{row['suburb']} sits in {councils[0]}, which should be confirmed for the actual "
        f"property before a crossing or frontage application is lodged."
    )


# -------------------------------------------------- section 5.4 service blocks

#: keyword -> flat service slug, used to score which services matter in a suburb
_SERVICE_SIGNALS: dict[str, tuple[str, ...]] = {
    "concrete-driveways-south-west-sydney": ("driveway", "access", "two-car", "double"),
    "concrete-crossovers-and-laybacks-south-west-sydney": (
        "crossover", "crossing", "layback", "dish", "frontage",
    ),
    "concrete-slabs-south-west-sydney": ("house slab", "footing", "extension"),
    "shed-and-garage-slabs-south-west-sydney": ("shed", "garage", "colorbond", "workshop", "stable"),
    "exposed-aggregate-south-west-sydney": ("exposed aggregate", "aggregate"),
    "decorative-concrete-south-west-sydney": ("coloured", "colour", "decorative", "stencil", "stamped"),
    "concrete-patios-south-west-sydney": ("alfresco", "patio", "outdoor", "pool surround", "entertaining"),
    "concrete-paths-south-west-sydney": ("path", "footpath", "side path", "pathway"),
    "concrete-driveway-replacement-south-west-sydney": (
        "replacement", "replace", "repair", "crack", "resurfac", "repour", "removal",
    ),
    "commercial-concreting-south-west-sydney": (
        "commercial", "hardstand", "machinery", "industrial", "warehouse", "carpark",
    ),
}

#: job_mix_weighting category -> services it pulls through
_MIX_SERVICES: dict[str, tuple[str, ...]] = {
    "new_build": (
        "concrete-driveways-south-west-sydney",
        "concrete-crossovers-and-laybacks-south-west-sydney",
        "concrete-patios-south-west-sydney",
    ),
    "replacement": (
        "concrete-driveway-replacement-south-west-sydney",
        "concrete-paths-south-west-sydney",
    ),
    "decorative": (
        "exposed-aggregate-south-west-sydney",
        "decorative-concrete-south-west-sydney",
    ),
    "commercial": (
        "commercial-concreting-south-west-sydney",
        "shed-and-garage-slabs-south-west-sydney",
    ),
}


def services_for_suburb(page_slug: str, limit: int = 4) -> list[str]:
    """spec section 5.4: the 3-5 services that actually matter here, from job_mix_weighting."""
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug)
    if not row:
        return []
    haystack = " ".join(row.get("typical_jobs", [])).lower()
    haystack += " " + str(row.get("unique_local_variable", "")).lower()
    haystack += " " + str(row.get("housing_stock_era", "")).lower()

    scores: dict[str, float] = {}
    for service, signals in _SERVICE_SIGNALS.items():
        scores[service] = sum(2.0 for token in signals if token in haystack)
    for category, weight in (row.get("job_mix_weighting") or {}).items():
        for service in _MIX_SERVICES.get(category, ()):
            scores[service] = scores.get(service, 0.0) + float(weight) * 3.0

    order = sorted(scores, key=lambda s: (-scores[s], list(_SERVICE_SIGNALS).index(s)))
    picked = [s for s in order if scores[s] > 0][:limit]
    if len(picked) < 3:
        for service in order:
            if service not in picked:
                picked.append(service)
            if len(picked) == 3:
                break
    return picked


def _matching_jobs(row: dict, service: str) -> list[str]:
    signals = _SERVICE_SIGNALS[service]
    return [job for job in row.get("typical_jobs", []) if any(t in job.lower() for t in signals)]


def _estate_phrase(row: dict) -> str:
    entities = row.get("local_entities") or {}
    estates = [e for e in entities.get("estates_developers", []) if e]
    if estates:
        # One name only: several records pair an estate with a descriptive phrase, and
        # joining them with "and" reads badly.
        return re.sub(r"\s*\(.*?\)", "", estates[0]).strip()
    streets = entities.get("streets_roads", [])
    if streets:
        return " and ".join(streets[:2])
    return ""


#: service-specific opening clause, so no two paragraphs on a page share a first sentence
_SERVICE_ANGLE: dict[str, str] = {
    "concrete-driveways-south-west-sydney": "Driveways are the job that sets the tone for the whole frontage in {name}",
    "concrete-crossovers-and-laybacks-south-west-sydney": "The crossover is the one part of a job in {name} that Council signs off, not you",
    "concrete-slabs-south-west-sydney": "House slabs and footings in {name} are designed before they are priced",
    "shed-and-garage-slabs-south-west-sydney": "Shed and garage slabs in {name} usually go in after handover, into a finished yard",
    "exposed-aggregate-south-west-sydney": "Exposed aggregate is the most common upgrade request in {name}",
    "decorative-concrete-south-west-sydney": "Coloured and decorative finishes in {name} are chosen off a sample, not a screen",
    "concrete-patios-south-west-sydney": "Alfresco and patio slabs in {name} live or die on levels and falls",
    "concrete-paths-south-west-sydney": "Paths and side access in {name} are the cheapest part of the job to get wrong",
    "concrete-driveway-replacement-south-west-sydney": "Replacement work in {name} starts with why the existing slab failed",
    "commercial-concreting-south-west-sydney": "Commercial and hardstand work in {name} is a different pour to a driveway",
}

#: short display label for the section 5.4 H3, matching the destination page
_SERVICE_LABEL: dict[str, str] = {
    "concrete-driveways-south-west-sydney": "Concrete driveways",
    "concrete-crossovers-and-laybacks-south-west-sydney": "Driveway crossovers",
    "concrete-slabs-south-west-sydney": "House slabs & footings",
    "shed-and-garage-slabs-south-west-sydney": "Shed & garage slabs",
    "exposed-aggregate-south-west-sydney": "Exposed aggregate driveways",
    "decorative-concrete-south-west-sydney": "Coloured concrete",
    "concrete-patios-south-west-sydney": "Alfresco & patio slabs",
    "concrete-paths-south-west-sydney": "Concrete paths & footpaths",
    "concrete-driveway-replacement-south-west-sydney": "Driveway replacement",
    "commercial-concreting-south-west-sydney": "Commercial concreting",
}

#: rotating lead-in for the typical job, keyed by position. Never lowercases the job
#: string — `suburbs.json` carries proper nouns like "Dart West" and "The Hermitage".
_JOB_LEAD = (
    "Most often: {job}.",
    "The version that comes up here: {job}.",
    "In practice: {job}.",
    "The common brief: {job}.",
    "Locally: {job}.",
)

#: rotating closing clause, keyed by position in the block
_SERVICE_CLOSE = (
    "Bring the dimensions, the existing surface and any drawings so the appointed provider can price the actual site.",
    "Send photos of the area and the access route — that answers half the questions before anyone visits.",
    "Measurements, levels and the intended use are enough to get a realistic conversation started.",
    "The appointed provider confirms the specification against the design and the site before quoting.",
    "Say what the area has to do and what is already there; the rest follows from a site visit.",
)


#: filler used only to reach the spec's word floor; never carries a claim
_PAD = (
    "Access, levels and what is already on the ground decide most of the scope.",
    "What the area has to carry, and how the truck reaches it, shape the rest.",
    "Existing surfaces, falls and drainage paths are worth noting before anyone quotes.",
)


def _balance(sentences: list[str], low: int, high: int, pad: tuple[str, ...] = ()) -> str:
    """Join sentences, trimming optional middles down and padding up to fit [low, high]."""
    keep = list(sentences)
    while len(" ".join(keep).split()) > high and len(keep) > 2:
        del keep[-2]
    for filler in pad:
        if len(" ".join(keep).split()) >= low:
            break
        if len(" ".join(keep + [filler]).split()) <= high:
            keep.insert(-1, filler)
    return " ".join(keep)


def service_in_suburb_blocks(page_slug: str, service_names: dict[str, str]) -> str:
    """spec section 5.4 H2 + H3 block. Unique per suburb, drawn from suburbs.json only.

    No council figure, price, soil class or thickness is published here. The regulatory
    detail in `suburbs.json` is not in the verified evidence set (`data/council-specs.yml`
    covers Liverpool only) and is therefore withheld under CLAUDE.md section 3 hard stop 6.
    """
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug)
    picked = services_for_suburb(page_slug)
    if not row or not picked:
        return ""
    name = row["name"]
    era = str(row.get("housing_stock_era", "")).strip().rstrip(".")
    estates = _estate_phrase(row)

    entities = row.get("local_entities") or {}
    landmarks = entities.get("landmarks", [])
    streets = entities.get("streets_roads", [])

    articles = []
    used_jobs: set[str] = set()
    for position, service in enumerate(picked):
        label = _SERVICE_LABEL[service]
        href = service_path(service)
        jobs = [j for j in _matching_jobs(row, service) if j not in used_jobs]

        sentences = [_SERVICE_ANGLE[service].format(name=name) + "."]
        if jobs:
            used_jobs.add(jobs[0])
            sentences.append(_JOB_LEAD[position % len(_JOB_LEAD)].format(job=jobs[0].rstrip(".")))
        # One rotating suburb-specific detail per position keeps every paragraph distinct.
        detail = ""
        if position == 0 and estates:
            detail = f"Around {estates} that usually means working to an established set-out and a fixed handover date."
        elif position == 1 and era:
            joiner = ", which sets" if "—" in era or "–" in era else " — that sets"
            detail = f"Housing stock here runs {era.lower()}{joiner} the lot shape and the levels you work to."
        elif position == 2 and landmarks:
            detail = f"Jobs near {landmarks[0]} tend to bring their own access and staging constraints."
        elif position == 3 and streets:
            detail = f"Frontages off {streets[0]} in particular need the access route sorted before the pour date."
        elif len(jobs) > 1:
            used_jobs.add(jobs[1])
            detail = f"{jobs[1].rstrip('.')} often comes up in the same conversation."
        if detail:
            sentences.append(detail)
        sentences.append(_SERVICE_CLOSE[position % len(_SERVICE_CLOSE)])
        paragraph = _balance(sentences, 40, 70, (_PAD[position % len(_PAD)],) + _PAD)

        articles.append(
            f'<article class="suburb-service"><h3><a href="{href}">'
            f"{html.escape(label)} in {html.escape(name)}</a></h3>"
            f"<p>{html.escape(paragraph)}</p></article>"
        )

    return (
        '<section class="section section--suburb-services"><div class="container">'
        f"<h2>Concreting services in {html.escape(name)}</h2>"
        '<div class="suburb-service-grid">' + "".join(articles) + "</div></div></section>"
    )


# ------------------------------------------------------- section 5.1 and 5.2

def near_me_h2(page_slug: str) -> str:
    """spec section 5.1. One per page, directly above the service links block."""
    return (
        '<h2 class="near-me-heading">Looking for concreters near you in '
        f"{html.escape(area_name(page_slug))}?</h2>"
    )


def near_me_faq(page_slug: str) -> tuple[str, dict | None]:
    """spec section 5.2. Returns (html, FAQPage node).

    Q1 is emitted with facts that exist. The `{X} business days` clause in the spec template
    is withheld - no response-time commitment is recorded in data/verified-facts.yml.

    Q2 (price) is omitted entirely: `pricing.per_m2_ranges` is unverified with
    `blocks_pages: 53`, and the spec itself says the question is omitted without a genuine
    quoted figure.
    """
    slug = page_slug.removeprefix("concreters-")
    row = SUBURB_SPEC.get(slug)
    if not row:
        return "", None
    name = row["name"]
    jobs = row.get("typical_jobs", [])
    mix = row.get("job_mix_weighting") or {}
    top = max(mix, key=mix.get) if mix else "new_build"
    mix_words = {
        "new_build": "new-build work on recently released lots",
        "replacement": "replacing and repairing concrete that has already had a life",
        "decorative": "decorative finishes and upgrades to existing surfaces",
        "commercial": "commercial, machinery and hardstand work",
    }[top]

    question = f"Do you have concreters near me in {name}?"
    core = [
        f"Yes — {name} is inside the area this site covers, and it has its own page because "
        f"the work here has its own shape.",
        f"Most of it is {mix_words}.",
    ]
    if jobs:
        core.append(f"Typically that means {jobs[0].rstrip('.').lower()}.")
    if len(jobs) > 1:
        core.append(f"{jobs[1].rstrip('.').capitalize()} is the next most common.")
    core.append(
        "The appointed independent provider confirms scope, licensing and the quotation "
        "before any work starts."
    )
    answer = _balance(core, 40, 60)
    if len(answer.split()) < 40:
        answer = _balance(core[:-1] + [council_sentence(page_slug)] + core[-1:], 40, 60)

    marker = (
        "<!-- BLOCKED: spec section 5.2 second FAQ (per-m2 price band) withheld. "
        "data/verified-facts.yml pricing.per_m2_ranges verified:false, blocks_pages:53. "
        "Owner-supplied figure required; no value may be inferred. -->"
        "<!-- BLOCKED: spec section 5.2 '{X} business days' withheld. No response-time "
        "commitment is recorded in data/verified-facts.yml. -->"
    )
    markup = (
        '<section class="section section--near-me-faq"><div class="container narrow">'
        f"{marker}"
        f'<h2>Concreters near you in {html.escape(name)}</h2>'
        '<div class="faq-list">'
        f'<details class="faq-item" open><summary>{html.escape(question)}</summary>'
        f"<p>{html.escape(answer)}</p></details>"
        "</div></div></section>"
    )
    node = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        ],
    }
    return markup, node


# ------------------------------------------------- section 5.3 areas hub links

def area_anchor(page_slug: str, index: int) -> str:
    """spec section 5.3: roughly 60% exact `concreters {suburb}`, 40% near-me variants."""
    name = area_name(page_slug)
    bucket = index % 5
    if bucket in (0, 1, 2):
        return f"Concreters in {name}"
    if bucket == 3:
        return f"Concreting services near {name}"
    return f"Find a concreter near {name}"
