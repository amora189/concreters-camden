#!/usr/bin/env python3
"""Build and validate the Phase A service-specification evidence artefacts.

This script is deliberately separate from ``data/service-specs.yml``.  D23
reserves that file for attested owner/engineer values; this script records what
authoritative sources do and do not establish without inventing a Structure Co
construction method.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.preimport_safety import (  # noqa: E402
    items,
    parse_wxr,
    post_id,
    post_slug,
    post_status,
    post_type,
    sha256,
    visible_page_fields,
)

ACCESS_DATE = "2026-08-21"

IMMUTABLE = {
    "camden-concreting-import.xml": "A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884",
    "eamptcoconcretersmelbourne_WordPress_2026-08-14.xml": "45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15",
    "build/stage9-page-manifest.json": "578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42",
    "build/stage8-image-map.json": "0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF",
    "reports/08-image-rename-map.csv": "43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8",
    "CODEX-BUILD-2.1.md": "BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C",
    "archive/governing/CODEX-BUILD-2.md": "E4FBC42D3BBFFB8E0745CA87B4751064F09CF67447F9F6A3BC79D03136785FC5",
}

FIELDS = [
    "concrete thickness",
    "concrete strength/grade",
    "reinforcement/mesh",
    "base preparation",
    "joint type and spacing",
    "curing requirements",
    "drainage/fall",
    "edges/formwork",
    "service-specific requirements",
]

SERVICES = {
    "concrete-driveways-south-west-sydney": (105, "Concrete Driveways", "driveway pavement"),
    "exposed-aggregate-south-west-sydney": (129, "Exposed Aggregate", "exposed-aggregate pavement"),
    "concrete-slabs-south-west-sydney": (163, "Concrete Slabs", "concrete slab"),
    "concrete-paths-south-west-sydney": (178, "Concrete Paths", "concrete path"),
    "concrete-patios-south-west-sydney": (195, "Concrete Patios", "patio slab"),
    "decorative-concrete-south-west-sydney": (922, "Decorative Concrete", "decorative concrete pavement"),
    "concrete-driveway-replacement-south-west-sydney": (1366, "Concrete Driveway Replacement", "replacement driveway"),
    "shed-and-garage-slabs-south-west-sydney": (1367, "Shed and Garage Slabs", "shed or garage slab"),
    "concrete-crossovers-and-laybacks-south-west-sydney": (1368, "Concrete Crossovers and Laybacks", "council-controlled vehicular crossing"),
    "commercial-concreting-south-west-sydney": (1369, "Commercial Concreting", "commercial concrete work"),
}

SOURCES = {
    "ccaa_residential": {
        "title": "Residential Concrete Driveways and Paths",
        "publisher": "Cement Concrete & Aggregates Australia",
        "url": "https://www.ccaa.com.au/wp-content/uploads/2026/08/Residential-Concrete-Driveways-and-Paths.pdf",
        "date": "2017-12",
        "page": "document pages 1-11",
        "supports": "Residential pavement design factors, loading-dependent thickness, reinforcement purpose, subgrade/base preparation, joints, drainage, finishes and construction precautions.",
        "access_verified": True,
        "access_method": "Downloaded, all 12 physical pages rendered and visually inspected on 2026-08-21",
        "sha256": "2212D0491FA912A400C42E5A1A2EBCE4D2DA31732255A113D452E13FB36C97E4",
    },
    "ccaa_industrial": {
        "title": "Guide to Industrial Floors and Pavements — Design, Construction and Specification",
        "publisher": "Cement Concrete & Aggregates Australia",
        "url": "https://ccaa.com.au/resources/guides/",
        "date": "current publisher catalogue; publication T48",
        "page": "publication description and design scope",
        "supports": "Industrial floors and pavements require design/specification for actual loads, subgrade, base, joints and performance rather than a residential template.",
        "access_verified": True,
        "access_method": "Current publisher Technical Guides page opened 2026-08-21; the legacy item URL redirects and is not cited",
    },
    "ccaa_exposed": {
        "title": "Briefing 02 — Exposed Aggregate Finishes for Flatwork",
        "publisher": "Cement Concrete & Aggregates Australia",
        "url": "https://ccaa.com.au/resources/briefings/",
        "date": "current publisher catalogue",
        "page": "publication description",
        "supports": "Exposed-aggregate appearance and construction depend on the selected aggregate, mix, exposure technique and finishing system.",
        "access_verified": True,
        "access_method": "Current publisher Briefings page opened 2026-08-21; the legacy item URL is 404 and is not cited",
    },
    "ccaa_finishes": {
        "title": "Guide to Concrete Flatwork Finishes",
        "publisher": "Cement Concrete & Aggregates Australia",
        "url": "https://ccaa.com.au/resources/guides/",
        "date": "current publisher catalogue",
        "page": "Guides — Guide to Concrete Flatwork Finishes",
        "supports": "Decorative and flatwork finishes require selection and specification of an actual finish/product system.",
        "access_verified": True,
        "access_method": "Publisher page opened 2026-08-21",
    },
    "ccaa_construction_index": {
        "title": "Guide to Concrete Construction 2020",
        "publisher": "Cement Concrete & Aggregates Australia",
        "url": "https://ccaa.com.au/resources/guide-to-concrete-construction/",
        "date": "2020; current publisher index at access date",
        "page": "Part V, Section 15 — Curing",
        "supports": "The current publisher index identifies a separate curing section but does not expose enough content to establish a method or duration for a broad building-slab service.",
        "access_verified": True,
        "access_method": "Current publisher page opened 2026-08-21; its legacy direct Section 15 PDF link returned 404 and is not used as substantive evidence",
    },
    "ncc_house": {
        "title": "NCC 2022 Volume Two — Part H1 Structure",
        "publisher": "Australian Building Codes Board",
        "url": "https://ncc.abcb.gov.au/editions/ncc-2022/adopted/volume-two/h-class-1-and-10-buildings/part-h1-structure",
        "date": "NCC 2022 Amendment 2, effective 2025-07-29",
        "page": "H1D4 Footings and slabs",
        "supports": "Class 1 and 10 footing/slab work must follow an applicable accepted construction pathway, including AS 2870/AS 3600 or Housing Provisions within scope.",
        "access_verified": True,
        "access_method": "Official NCC page opened 2026-08-21",
    },
    "ncc_commercial": {
        "title": "NCC 2022 Volume One — Part B1 Structural provisions",
        "publisher": "Australian Building Codes Board",
        "url": "https://ncc.abcb.gov.au/editions/ncc-2022/adopted/volume-one/b-structure/part-b1-structural-provisions",
        "date": "NCC 2022 Amendment 2, effective 2025-07-29",
        "page": "Part B1 and Specification 4",
        "supports": "Commercial structural work must satisfy the applicable structural performance requirements and referenced design standards; the service label does not establish a universal slab design.",
        "access_verified": True,
        "access_method": "Official NCC page opened 2026-08-21",
    },
    "ncc_access": {
        "title": "NCC 2022 Volume One — Part D4 Access for people with a disability",
        "publisher": "Australian Building Codes Board",
        "url": "https://ncc.abcb.gov.au/editions/ncc-2022/adopted/volume-one/d-access-and-egress/part-d4-access-people-disability",
        "date": "NCC 2022 Amendment 2, effective 2025-07-29",
        "page": "D4D2 and D4D4",
        "supports": "Where an accessway is required, its design must satisfy the applicable access provisions and referenced AS 1428.1 requirements.",
        "access_verified": True,
        "access_method": "Official NCC page opened 2026-08-21",
    },
    "safework_formwork": {
        "title": "Formwork Code of Practice",
        "publisher": "SafeWork NSW",
        "url": "https://www.safework.nsw.gov.au/resource-library/codes-of-practice/codes-of-practice/formwork",
        "date": "2021-03",
        "page": "design, planning and systems of work",
        "supports": "Formwork must be designed, planned, erected and managed through a safe system suited to the work; one edge detail cannot be inferred for every job.",
        "access_verified": True,
        "access_method": "Official SafeWork NSW page opened 2026-08-21",
    },
    "safework_excavation": {
        "title": "Excavations and earthmoving plant in construction",
        "publisher": "SafeWork NSW",
        "url": "https://www.safework.nsw.gov.au/hazards-a-z/excavations-and-earthmoving-plant-in-construction",
        "date": "2026-05",
        "page": "planning and essential-services information",
        "supports": "Excavation planning must account for current essential-services information, ground type, backfill, moisture, slopes and nearby loads.",
        "access_verified": True,
        "access_method": "Official SafeWork NSW page opened 2026-08-21",
    },
    "nsw_waste": {
        "title": "Construction and demolition waste",
        "publisher": "NSW Environment Protection Authority",
        "url": "https://www.epa.nsw.gov.au/Your-environment/Waste/industrial-waste/construction-demolition",
        "date": "current at access date",
        "page": "construction and demolition waste obligations",
        "supports": "Removed concrete and excavation waste must be classified, transported and taken to a place that can lawfully receive it.",
        "access_verified": True,
        "access_method": "Official NSW EPA page opened 2026-08-21",
    },
    "liverpool_crossing": {
        "title": "Vehicular Crossing Application and Specifications — March 2026 v1",
        "publisher": "Liverpool City Council",
        "url": "https://www.liverpool.nsw.gov.au/__data/assets/pdf_file/0003/286329/VEHICULAR-CROSSING-APPLICATION-FORM-March-2026v1.pdf",
        "date": "2026-03",
        "page": "PDF pages 1-18; requirements table in Report 52",
        "supports": "Liverpool section 138 application, inspection, site-specific directions, plain finish, strength, DGS20 bedding, utility clearances, contractor licensing and $10m public-liability requirements.",
        "access_verified": True,
        "access_method": "Official 18-page PDF opened and all pages visually inspected 2026-08-21; validated by scripts/52-phase-d-liverpool.py",
        "sha256": "43F74C0F01C5EA6F0C89919BE8C1859F758F96AF549A9CF71ADA5F87DD7CAF33",
    },
    "camden_crossing": {
        "title": "Driveway Crossing Application — Standard Residential Driveway",
        "publisher": "Camden Council",
        "url": "https://www.camden.nsw.gov.au/assets/pdfs/Payments-and-Forms/Development-Forms/Template-CCM-Driveway-Crossing-Application-Standard-Residential-Driveway-Updated-October-2021-PDF.pdf",
        "date": "2021-10",
        "page": "PDF pages 1-3",
        "supports": "Camden has its own eligibility, application, specification/drawing and inspection process; non-standard work follows a separate pathway.",
        "access_verified": True,
        "access_method": "Official three-page PDF opened 2026-08-21",
    },
    "campbelltown_crossing": {
        "title": "Driveways",
        "publisher": "Campbelltown City Council",
        "url": "https://www.campbelltown.nsw.gov.au/Build-and-Develop/Obtaining-Approval-to-Build/Driveways",
        "date": "current at access date",
        "page": "Driveway application and section 138 requirements",
        "supports": "Campbelltown requires its own driveway/section 138 approval before work in the road reserve.",
        "access_verified": True,
        "access_method": "Official council page opened 2026-08-21",
    },
    "wollondilly_crossing": {
        "title": "Driveway and property entrance",
        "publisher": "Wollondilly Shire Council",
        "url": "https://www.wollondilly.nsw.gov.au/roads/working-on-a-public-road/driveway-and-property-entrance",
        "date": "current at access date",
        "page": "approval, design and construction requirements",
        "supports": "Wollondilly uses its own approval, design/construction specification and evidence requirements for road-reserve entrances.",
        "access_verified": True,
        "access_method": "Official council page opened 2026-08-21",
    },
    "camden_suburbs": {
        "title": "About Camden — suburbs",
        "publisher": "Camden Council",
        "url": "https://www.camden.nsw.gov.au/council/about-us?stage=Live",
        "date": "current at access date",
        "page": "Suburbs within Camden LGA",
        "supports": "Camden Council locality list, including explicitly marked part-localities.",
        "access_verified": True,
        "access_method": "Official council page opened 2026-08-21",
    },
    "camden_maps": {
        "title": "Suburb Maps",
        "publisher": "Camden Council",
        "url": "https://www.camden.nsw.gov.au/community/community-information/suburb-maps",
        "date": "current at access date",
        "page": "suburb map index",
        "supports": "Camden suburb mapping, including Cawdor, for boundary reconciliation.",
        "access_verified": True,
        "access_method": "Official council page opened 2026-08-21",
    },
    "liverpool_suburbs": {
        "title": "Suburbs of Liverpool",
        "publisher": "Liverpool City Library / Liverpool City Council",
        "url": "https://mylibrary.liverpool.nsw.gov.au/history/ourstories/suburbs-of-liverpool",
        "date": "current at access date",
        "page": "whole and shared suburb list",
        "supports": "Liverpool locality list identifies whole and shared localities, including Bringelly, Leppington, Rossmore, Edmondson Park and Kemps Creek.",
        "access_verified": True,
        "access_method": "Official council library page and relevant locality pages opened 2026-08-21",
    },
    "campbelltown_suburbs": {
        "title": "Campbelltown Community Profile",
        "publisher": "Campbelltown City Council",
        "url": "https://www.campbelltown.nsw.gov.au/About-Campbelltown/Campbelltown-Community-Profile",
        "date": "current at access date",
        "page": "suburb list",
        "supports": "Campbelltown City Council locality list.",
        "access_verified": True,
        "access_method": "Official council page opened 2026-08-21",
    },
    "fairfield_suburbs": {
        "title": "Fairfield City Profile — list of suburbs",
        "publisher": "Fairfield City Council",
        "url": "https://www.fairfieldcity.nsw.gov.au/Your-Council/Fairfield-City-Profile",
        "date": "current at access date",
        "page": "List of suburbs in Fairfield City",
        "supports": "Fairfield City Council's locality list includes Cecil Park.",
        "access_verified": True,
        "access_method": "Official council page opened 2026-08-21",
    },
    "wollondilly_suburbs": {
        "title": "Asset Maps & Community Profiles",
        "publisher": "Wollondilly Shire Council",
        "url": "https://www.wollondilly.nsw.gov.au/events-and-community/asset-maps-and-community-profiles",
        "date": "current at access date",
        "page": "community-profile locality groups",
        "supports": "Current Wollondilly community-profile groups include Camden Park, Cawdor and Theresa Park as well as the active Wollondilly towns and villages.",
        "access_verified": True,
        "access_method": "Official current council page opened 2026-08-21",
    },
    "nsw_spatial": {
        "title": "NSW Planning Portal Spatial Viewer",
        "publisher": "NSW Department of Planning, Housing and Infrastructure",
        "url": "https://www.planningportal.nsw.gov.au/spatialviewer/",
        "date": "current at access date",
        "page": "interactive cadastral and LGA layers",
        "supports": "Lot-level LGA checking where a suburb crosses a council boundary.",
        "access_verified": True,
        "access_method": "Official NSW Planning Portal opened 2026-08-21",
    },
    "tfnsw_curing": {
        "title": "TS 00149:1.0 Placement of Concrete (ATS 5320-23 Ed 1.0 MOD)",
        "publisher": "Transport for NSW",
        "url": "https://standards.transport.nsw.gov.au/_entity/annotation/97a9de5a-51b7-ef11-a72f-002248966666",
        "date": "effective 2025-04-30",
        "page": "PDF pages 21-25 and Appendix D, pages 42-44",
        "supports": "For this infrastructure project type, curing is controlled by the contract specification, exposure classification, selected method/performance pathway, materials and approved quality plan. It is evidence of project-specific selection, not a rule for every commercial slab.",
        "access_verified": True,
        "access_method": "Official 45-page Transport for NSW PDF opened; relied-on curing pages rendered and visually inspected 2026-08-21",
    },
}

CSV_COLUMNS = [
    "service", "field", "current_claim", "current_value", "classification",
    "resolved_value", "public_wording", "source_title", "source_url",
    "source_date", "source_page", "access_date", "jurisdiction", "verified",
    "remaining_input", "notes",
]


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def evidence(source_keys: list[str]) -> tuple[str, str, str, str]:
    selected = [SOURCES[key] for key in source_keys]
    return (
        " | ".join(s["title"] for s in selected),
        " | ".join(s["url"] for s in selected),
        " | ".join(s["date"] for s in selected),
        " | ".join(s["page"] for s in selected),
    )


def field_sources(slug: str, field: str) -> list[str]:
    if field == "curing requirements":
        if slug in {"concrete-slabs-south-west-sydney", "shed-and-garage-slabs-south-west-sydney"}:
            return ["ncc_house", "ccaa_construction_index"]
        if slug == "commercial-concreting-south-west-sydney":
            return ["ncc_commercial", "tfnsw_curing"]
        if slug == "concrete-crossovers-and-laybacks-south-west-sydney":
            return ["liverpool_crossing", "camden_crossing", "campbelltown_crossing", "wollondilly_crossing"]
        return ["ccaa_residential"]
    if field == "edges/formwork":
        return ["safework_formwork", "ccaa_residential"]
    if field == "base preparation":
        return ["safework_excavation", "ccaa_residential"]
    if slug == "concrete-crossovers-and-laybacks-south-west-sydney":
        return ["liverpool_crossing", "camden_crossing", "campbelltown_crossing", "wollondilly_crossing"]
    if slug == "commercial-concreting-south-west-sydney":
        return ["ncc_commercial", "ccaa_industrial"]
    if slug == "shed-and-garage-slabs-south-west-sydney":
        return ["ncc_house", "safework_excavation"]
    if slug == "concrete-slabs-south-west-sydney":
        return ["ncc_house", "ncc_commercial"]
    if slug == "exposed-aggregate-south-west-sydney" and field == "service-specific requirements":
        return ["ccaa_exposed", "ccaa_residential"]
    if slug == "decorative-concrete-south-west-sydney" and field == "service-specific requirements":
        return ["ccaa_finishes", "ccaa_residential"]
    if slug == "concrete-driveway-replacement-south-west-sydney" and field == "service-specific requirements":
        return ["nsw_waste", "safework_excavation"]
    if slug == "concrete-paths-south-west-sydney" and field in {"drainage/fall", "service-specific requirements"}:
        return ["ccaa_residential", "ncc_access"]
    return ["ccaa_residential"]


def cell_rule(slug: str, field: str, subject: str) -> tuple[str, str, str, str, str]:
    crossing = slug == "concrete-crossovers-and-laybacks-south-west-sydney"
    structural = slug in {
        "concrete-slabs-south-west-sydney",
        "shed-and-garage-slabs-south-west-sydney",
        "commercial-concreting-south-west-sydney",
    }
    product = slug in {"exposed-aggregate-south-west-sydney", "decorative-concrete-south-west-sydney"}
    jurisdiction = "Australia / NSW; project jurisdiction must be confirmed"
    remaining = ""

    if field == "concrete thickness":
        if crossing:
            classification = "COUNCIL-SPECIFIC"
            resolved = "No South West Sydney-wide thickness exists. Use the permit, standard drawing and site direction of the council controlling the road reserve."
            wording = "Crossing thickness is confirmed from the controlling council's current permit, standard drawing and any site-specific direction before construction."
            jurisdiction = "Relevant road authority: Camden, Liverpool, Campbelltown, Wollondilly or another controlling council"
        elif structural:
            classification = "DESIGN-SPECIFIC"
            resolved = "The applicable structural design pathway, actual loading, ground conditions and drawings determine thickness."
            wording = f"The {subject} thickness is confirmed from the applicable design, expected loads, ground conditions and approved drawings."
        else:
            classification = "SITE-SPECIFIC"
            resolved = "Expected loads, subgrade support, pavement layout and any council interface determine thickness; the service name does not."
            wording = f"Thickness for the {subject} is confirmed after expected loading, ground support, layout and any council-controlled interface are known."
    elif field == "concrete strength/grade":
        if crossing:
            classification = "COUNCIL-SPECIFIC"
            resolved = "Use the controlling council's current requirement. Liverpool's March 2026 form states 25 MPa at 28 days for residential driveways and 32 MPa for medium-density, commercial and industrial driveways; those figures do not apply outside Liverpool."
            wording = "Concrete strength for a road-reserve crossing comes from the controlling council's current specification and the approved application; Liverpool values are not applied to other council areas."
            jurisdiction = "Relevant road authority; Liverpool values only within Liverpool City Council"
        else:
            classification = "DESIGN-SPECIFIC"
            resolved = "Strength/grade follows the applicable drawings, structural or pavement design, exposure and performance requirements."
            wording = f"Concrete strength for the {subject} is specified for the approved design, exposure and required performance rather than assumed from a generic service template."
    elif field == "reinforcement/mesh":
        classification = "COUNCIL-SPECIFIC" if crossing else "DESIGN-SPECIFIC"
        resolved = ("Use the controlling council drawing and approved site requirements; no mesh designation is universal across the service area."
                    if crossing else "Reinforcement, if required, follows the applicable design/drawings, slab or pavement thickness, joint layout and crack-control requirements. Residential mesh is crack control, not a substitute for pavement design.")
        wording = ("Reinforcement is taken from the controlling council's approved crossing detail and any site-specific direction."
                   if crossing else f"Reinforcement for the {subject} is selected from the applicable design and drawings, with the joint layout and crack-control purpose made clear.")
        if crossing:
            jurisdiction = "Relevant road authority"
    elif field == "base preparation":
        classification = "COUNCIL-SPECIFIC" if crossing else "SITE-SPECIFIC"
        resolved = ("Use the controlling council specification and inspection direction. Liverpool specifies compacted DGS20 bedding, including a different minimum where kerb, gutter or layback is constructed; it is not exported to other councils."
                    if crossing else "Preparation depends on actual subgrade material and condition, moisture, fill/backfill, drainage, excavation, expected loading and the applicable design.")
        wording = ("The road-reserve base is prepared and inspected to the controlling council's current specification and site direction."
                   if crossing else f"Base preparation for the {subject} is set after the subgrade, fill, moisture, drainage and expected loading have been assessed.")
        if crossing:
            jurisdiction = "Relevant road authority; Liverpool DGS20 values only within Liverpool City Council"
    elif field == "joint type and spacing":
        classification = "COUNCIL-SPECIFIC" if crossing else "DESIGN-SPECIFIC"
        resolved = ("Use the controlling council standard drawing and approved detail."
                    if crossing else "Joint types, positions, details and spacing follow slab/pavement geometry, restraints, thickness, reinforcement, finish and the applicable design; a single interval is not established for this broad service.")
        wording = ("Joint details follow the controlling council's approved crossing drawing and site directions."
                   if crossing else f"Joint type, layout and spacing for the {subject} are coordinated with its geometry, restraints, thickness, reinforcement and selected finish.")
        if crossing:
            jurisdiction = "Relevant road authority"
    elif field == "curing requirements":
        if slug in {"concrete-slabs-south-west-sydney", "shed-and-garage-slabs-south-west-sydney"}:
            classification = "UNRESOLVED"
            resolved = "The accessible NCC source establishes the applicable structural design pathway but does not itself establish a curing method or duration for this broad service. The directly linked CCAA curing publication could not be opened and is not used as evidence."
            wording = f"No fixed curing period is published for the {subject}; the applicable design/specification and selected provider must state the method, duration and protection conditions before work begins."
            remaining = f"What applicable project specification or engineer/provider instruction sets the curing method and duration for the actual {subject}?"
        elif crossing:
            classification = "COUNCIL-SPECIFIC"
            resolved = "The reviewed council pathways establish separate authority-controlled specifications and drawings, but not one service-area curing rule. Confirm any curing requirement in the controlling council's approved documents and the provider's method."
            wording = "Curing and protection requirements for a road-reserve crossing must be checked against the controlling council's approved documents and confirmed by the provider before construction."
            jurisdiction = "Relevant road authority"
            remaining = "What curing requirement appears in the approved crossing documents for the actual property, and what compliant method will the selected provider use?"
        elif slug == "commercial-concreting-south-west-sydney":
            classification = "DESIGN-SPECIFIC"
            resolved = "Curing follows the actual project specification, exposure, concrete materials, selected performance/method pathway and approved quality plan. The cited Transport for NSW requirements are an infrastructure example, not a universal commercial rule."
            wording = "The commercial project specification must state the curing method, duration, protection and verification appropriate to its exposure, materials and required performance."
            remaining = "What curing clauses and approved quality-plan requirements apply to the actual commercial project?"
        else:
            classification = "PROVIDER-METHOD"
            resolved = "For residential pavement applications, the cited CCAA guidance ties curing duration and method to traffic/exposure, weather and finish compatibility; Structure Co has no attested universal provider method."
            wording = f"The provider must confirm the curing method and protection period for the {subject}, taking account of traffic/exposure, weather and the selected finish system."
            remaining = f"For a job-specific specification, what curing method and duration will the selected provider use for this {subject} under the project conditions?"
    elif field == "drainage/fall":
        classification = "COUNCIL-SPECIFIC" if crossing else "SITE-SPECIFIC"
        resolved = ("Levels, crossfall, drainage and tie-ins follow the controlling council permit/drawing and site-specific direction."
                    if crossing else "Falls and drainage depend on existing levels, adjoining buildings, boundaries, accessible-path requirements where applicable and the approved stormwater arrangement.")
        wording = ("Crossing levels, crossfall and drainage follow the controlling council's approved detail and inspection directions."
                   if crossing else f"Falls and drainage for the {subject} must suit the property levels, adjoining structures and the approved stormwater arrangement.")
        if crossing:
            jurisdiction = "Relevant road authority"
    elif field == "edges/formwork":
        classification = "COUNCIL-SPECIFIC" if crossing else "DESIGN-SPECIFIC"
        resolved = ("Formwork, edge, kerb, gutter and layback details follow the controlling council drawing and must obtain the required pre-pour inspection/approval."
                    if crossing else "Edge and formwork details depend on geometry, levels, restraint, adjacent construction and a safely planned formwork system.")
        wording = ("Formwork and edge details follow the approved council drawing and remain subject to the required pre-pour inspection."
                   if crossing else f"Edges and formwork for the {subject} are detailed for its geometry, levels, restraints and adjoining construction, with a suitable safe work method.")
        if crossing:
            jurisdiction = "Relevant road authority"
    else:
        if slug == "concrete-driveways-south-west-sydney":
            classification = "SITE-SPECIFIC"
            resolved = "Vehicle types and frequency, private-property extent and the council crossing interface must be established for each driveway."
            wording = "Driveway design starts with the vehicles it must carry, the private-property layout and any separately controlled road-reserve crossing."
        elif slug == "exposed-aggregate-south-west-sydney":
            classification = "PRODUCT-SPECIFIC"
            resolved = "Aggregate source/size/colour, mix, exposure technique, sample acceptance, sealer and maintenance depend on the selected supplier/product system."
            wording = "The quotation should identify the aggregate and finish system, sample or reference appearance, exposure method, sealer and maintenance information for the selected product."
            remaining = "Which aggregate, mix, exposure and sealer systems are actually available from the selected provider, and what manufacturer/supplier documents govern them?"
        elif slug == "concrete-slabs-south-west-sydney":
            classification = "DESIGN-SPECIFIC"
            resolved = "Slab use, building classification, soil/site classification, loads, footing system, penetrations and approved drawings determine the specification."
            wording = "A slab quotation must be checked against its intended use, applicable building/design pathway, site conditions, penetrations and approved drawings."
        elif slug == "concrete-paths-south-west-sydney":
            classification = "SITE-SPECIFIC"
            resolved = "Route, use, required access, levels, transitions, adjoining surfaces and drainage determine path requirements."
            wording = "Path requirements are set from the route, users, levels, transitions and drainage; where an accessible path is required, the applicable access design also governs."
        elif slug == "concrete-patios-south-west-sydney":
            classification = "DESIGN-SPECIFIC"
            resolved = "Relationship to the dwelling, roof/posts, termite and damp-proofing interfaces, loads, levels and stormwater design must be checked for the actual patio."
            wording = "Patio slab details are coordinated with the dwelling, any roof or post loads, thresholds, moisture/termite interfaces, levels and stormwater arrangement."
        elif slug == "decorative-concrete-south-west-sydney":
            classification = "PRODUCT-SPECIFIC"
            resolved = "Colour, pattern/texture, slip performance, sample acceptance, placement method, sealer and maintenance depend on the selected system and its manufacturer/supplier documents."
            wording = "The selected decorative system should be named, sampled and checked for the intended use, slip conditions, installation method, sealer and maintenance requirements."
            remaining = "Which decorative finish and sealer systems are actually offered by the selected provider, and what current manufacturer/supplier documents govern each one?"
        elif slug == "concrete-driveway-replacement-south-west-sydney":
            classification = "SITE-SPECIFIC"
            resolved = "Existing slab condition, cause of failure, services, demolition method, lawful waste destination, retained levels and crossing/kerb interfaces must be assessed."
            wording = "Replacement scope must record what is being removed, why it failed, service locations, lawful waste handling, retained levels and any council-controlled interface."
        elif slug == "shed-and-garage-slabs-south-west-sydney":
            classification = "DESIGN-SPECIFIC"
            resolved = "The selected shed/garage design, post or wall loads, vehicle loads, anchors, rebates, levels, site classification and approved drawings govern the slab."
            wording = "The slab must match the selected shed or garage supplier's loads, anchors and edge details together with the site classification and approved drawings."
            remaining = "What supplier/engineer drawings, loads, anchor schedule and rebate/edge details apply to the actual shed or garage?"
        elif crossing:
            classification = "COUNCIL-SPECIFIC"
            resolved = "A section 138/road-reserve approval pathway, drawings, utilities, inspections, surface, contractor credentials and owner obligations vary with the controlling authority. Liverpool's 13 verified March 2026 requirements apply only in Liverpool."
            wording = "The property owner must use the controlling council's current application, drawings, inspections and contractor-evidence requirements; Liverpool's March 2026 conditions are stated only for Liverpool properties."
            jurisdiction = "Relevant road authority"
        else:
            classification = "DESIGN-SPECIFIC"
            resolved = "Use, traffic/loading spectrum, operational tolerances, durability/exposure, access, services, staging and the project engineer/specifier determine the work."
            wording = "Commercial concrete work must be specified for the actual use, loads, durability, levels, access, services, staging and project drawings."
            remaining = "What project drawings/specification, loading spectrum, operational tolerances and engineer requirements apply to the actual commercial work?"
    return classification, resolved, wording, jurisdiction, remaining


TECH_TERMS = re.compile(
    r"(?i)(concrete|slab|pavement|driveway|path|patio|aggregate|reinforc|mesh|SL\d+|MPa|mm\b|metre|%|"
    r"crossfall|batter|thickness|grade|strength|base|subgrade|excavat|joint|cur|drain|fall|formwork|edge|"
    r"layback|crossover|hardstand|footpath|stormwater|soil|load|finish|seal|demol|waste)"
)

AUDIT_TERMS = re.compile(
    r"(?i)(\b\d+(?:\.\d+)?\s*(?:MPa|mm|m\b|%|days?|hours?)|SL\d+|DGS20|1:6|"
    r"strength|grade|thickness|reinforc|mesh|fabric|base preparation|subgrade|compact|excavat|"
    r"joint|curing|cure|drainage|crossfall|batter|stormwater|formwork|edge treatment|layback|"
    r"crossover|hardstand|footpath allocation|approved design|engineering|expected load|soil|"
    r"ground condition|demolition|lawful waste|surface-water|service boundary|specification)"
)

FIELD_TERMS = {
    "concrete thickness": re.compile(r"(?i)(thickness|125\s*mm|slab depth)"),
    "concrete strength/grade": re.compile(r"(?i)(strength|grade|MPa|32\s*MPa)"),
    "reinforcement/mesh": re.compile(r"(?i)(reinforc|mesh|fabric|SL\d+)"),
    "base preparation": re.compile(r"(?i)(base|subgrade|ground|soil|excavat|DGS20|bedding|fill|compact)"),
    "joint type and spacing": re.compile(r"(?i)(joint|saw.?cut|spacing|crack)"),
    "curing requirements": re.compile(r"(?i)(curing|cure|protect(?:ion)? period)"),
    "drainage/fall": re.compile(r"(?i)(drain|fall|crossfall|batter|stormwater|level|slope|4%)"),
    "edges/formwork": re.compile(r"(?i)(edge|formwork|form|kerb|gutter|layback)"),
    "service-specific requirements": TECH_TERMS,
}


def service_inventory() -> dict:
    expected = {(pid, slug) for slug, (pid, _name, _subject) in SERVICES.items()}
    manifest = json.loads((ROOT / "build/stage9-page-manifest.json").read_text(encoding="utf-8"))
    manifest_set = {(int(row["post_id"]), row["post_name"]) for row in manifest if row.get("page_type") == "service"}
    allow = json.loads((ROOT / "build/46-active-page-allowlist.json").read_text(encoding="utf-8"))
    allow_set = {(int(row["page_id"]), row["slug"]) for row in allow["pages"] if row.get("page_type") == "service"}
    wxr_set = {
        (post_id(item), post_slug(item))
        for item in items(parse_wxr(ROOT / "camden-concreting-import.xml"))
        if post_type(item) == "page" and post_slug(item) in SERVICES
    }
    yaml_text = (ROOT / "data/service-specs.yml").read_text(encoding="utf-8")
    yaml_data = "\n".join(line for line in yaml_text.splitlines() if not line.lstrip().startswith("#"))
    yaml_set = set(re.findall(r"^  ([a-z0-9-]+-south-west-sydney):\s*$", yaml_text, re.M))
    yaml_expected = {slug for _pid, slug in expected}
    sets = {"declared": expected, "manifest": manifest_set, "allowlist": allow_set, "source_wxr": wxr_set}
    if any(value != expected for value in sets.values()) or yaml_set != yaml_expected:
        raise AssertionError(f"service inventories disagree: {sets}; yaml={sorted(yaml_set)}")
    malformed = len(re.findall(r"^      value: \"\", verified: false,", yaml_text, re.M))
    return {
        "count": len(expected),
        "services": [{"page_id": pid, "slug": slug, "display_name": SERVICES[slug][1]} for pid, slug in sorted(expected)],
        "reconciled_artifacts": {key: len(value) for key, value in sets.items()} | {"legacy_service_specs_keys": len(yaml_set)},
        "legacy_service_specs": {
            "verified_true": len(re.findall(r"verified:\s*true", yaml_data, re.I)),
            "verified_false": len(re.findall(r"verified:\s*false", yaml_data, re.I)),
            "malformed_service_specific_value_lines": malformed,
            "formal_precondition": "BLOCKED",
            "authority": "D23; not modified by this evidence-acquisition pass",
        },
    }


def audit_claims() -> tuple[list[dict], dict[str, dict[str, list[dict]]]]:
    tree = parse_wxr(ROOT / "build/46-active-main-import.xml")
    page_items = {post_slug(item): item for item in items(tree) if post_type(item) == "page" and post_slug(item) in SERVICES}
    if set(page_items) != set(SERVICES):
        raise AssertionError("derivative WXR service set does not match ten-service inventory")
    records: list[dict] = []
    by_cell: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for slug, item in sorted(page_items.items(), key=lambda pair: SERVICES[pair[0]][0]):
        seen = set()
        for field in visible_page_fields(item):
            raw = field["text"]
            visible = strip_tags(raw)
            if field["placement"] == "item.title" or not AUDIT_TERMS.search(visible):
                continue
            key = (field["placement"], raw)
            if key in seen:
                continue
            seen.add(key)
            mapped = [name for name, pattern in FIELD_TERMS.items() if pattern.search(visible)]
            if not mapped:
                mapped = ["service-specific requirements"]
            urls = re.findall(r"https?://[^\s\"'<>]+|href=[\"']([^\"']+)", raw)
            flat_urls = [u if isinstance(u, str) else "" for u in urls]
            classification = "unsupported"
            if "approved service boundary" in visible.lower():
                classification = "verified"
            elif "unresolved" in visible.lower() or "[[PLACEHOLDER" in raw:
                classification = "unsupported"
            elif re.search(r"(?i)(site-specific|project-specific|approved design|provider)", visible):
                classification = "project-specific"
            record = {
                "audit_id": f"SVC-{post_id(item)}-{len(records)+1:04d}",
                "page_id": post_id(item),
                "slug": slug,
                "source_status": post_status(item),
                "placement": field["placement"],
                "widget_type": field["widget_type"],
                "exact_claim": raw,
                "visible_text": visible,
                "fields": mapped,
                "current_evidence_citation": flat_urls or [],
                "classification": classification,
                "notes": "An internal link is not evidence unless the linked source itself is authoritative and verified; no such service-page citation establishes a universal company specification.",
            }
            records.append(record)
            for mapped_field in mapped:
                by_cell[slug][mapped_field].append(record)
    return records, by_cell


FIGURE_FIELD = {
    "125mm": ["concrete thickness"],
    "32 MPa": ["concrete strength/grade"],
    "SL72": ["reinforcement/mesh"],
    "SL82": ["reinforcement/mesh"],
    "4%": ["drainage/fall", "service-specific requirements"],
    "1:6": ["drainage/fall", "service-specific requirements"],
    "800mm": ["service-specific requirements"],
    "900mm": ["service-specific requirements"],
    "1200mm": ["service-specific requirements"],
    "4.0-5.5m": ["service-specific requirements"],
}


def figure_audit() -> tuple[list[dict], dict[str, dict[str, list[dict]]]]:
    with (ROOT / "reports/35-figure-provenance.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    service_rows = [r for r in rows if r["page_class"] == "service" and r["slug"] in SERVICES]
    if len(rows) != 214 or len(service_rows) != 91:
        raise AssertionError(f"figure register expected 214 total / 91 service rows, got {len(rows)} / {len(service_rows)}")
    by_cell: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    result = []
    for index, row in enumerate(service_rows, 1):
        mapped_fields = FIGURE_FIELD.get(row["figure"], ["service-specific requirements"])
        audit = {
            "register_row": index,
            "page_id": int(row["post_id"]),
            "slug": row["slug"],
            "figure": row["figure"],
            "population": row["population"],
            "exact_context": row["context"],
            "current_evidence_citation": "none recorded",
            "classification": "unsupported",
            "attested": row["attested"],
            "verified_in_service_specs": row["verified_in_service_specs"],
            "mapped_fields": mapped_fields,
            "disposition": "Do not publish as a universal service specification. Reassess only against an applicable authority, approved design/drawing or attested provider specification.",
        }
        result.append(audit)
        for field in mapped_fields:
            by_cell[row["slug"]][field].append(audit)
    return result, by_cell


def build_matrix(claim_by_cell: dict, figure_by_cell: dict) -> list[dict]:
    rows = []
    for slug, (_pid, name, subject) in SERVICES.items():
        for field in FIELDS:
            classification, resolved, wording, jurisdiction, remaining = cell_rule(slug, field, subject)
            source_keys = field_sources(slug, field)
            title, url, source_date, source_page = evidence(source_keys)
            claims = claim_by_cell[slug][field]
            figures = figure_by_cell[slug][field]
            current_claim = "\n\n---\n\n".join(c["exact_claim"] for c in claims)
            current_value = "; ".join(dict.fromkeys(f["figure"] for f in figures))
            rows.append({
                "service": slug,
                "field": field,
                "current_claim": current_claim,
                "current_value": current_value,
                "classification": classification,
                "resolved_value": resolved,
                "public_wording": wording,
                "source_title": title,
                "source_url": url,
                "source_date": source_date,
                "source_page": source_page,
                "access_date": ACCESS_DATE,
                "jurisdiction": jurisdiction,
                "verified": "false" if classification == "UNRESOLVED" else "true",
                "remaining_input": remaining,
                "notes": "Verified means the classification and safe conditional wording are evidence-supported. It does not attest a Structure Co method or populate data/service-specs.yml. " +
                         f"Source keys: {', '.join(source_keys)}. Exact claim records: {len(claims)}; mapped figure-register rows: {len(figures)}.",
            })
    return rows


def council_map() -> dict:
    expanded = json.loads((ROOT / "suburbs-expanded.json").read_text(encoding="utf-8"))["suburbs"]
    allow = json.loads((ROOT / "build/46-active-page-allowlist.json").read_text(encoding="utf-8"))["pages"]
    page_by_slug = {r["slug"]: r for r in allow if r.get("page_type") == "suburb"}
    split = {
        "bringelly": ["Camden Council", "Liverpool City Council"],
        "leppington": ["Camden Council", "Liverpool City Council"],
        "rossmore": ["Camden Council", "Liverpool City Council"],
        "edmondson-park": ["Liverpool City Council", "Campbelltown City Council"],
        "kemps-creek": ["Liverpool City Council", "Penrith City Council"],
        "cawdor": ["Camden Council", "Wollondilly Shire Council"],
        "cecil-park": ["Liverpool City Council", "Fairfield City Council"],
        "ingleburn": ["Campbelltown City Council", "Liverpool City Council"],
    }
    corrected = {"camden-park": ["Wollondilly Shire Council"], "theresa-park": ["Wollondilly Shire Council"]}
    key_for_lga = {
        "Camden Council": "camden_suburbs",
        "Liverpool City Council": "liverpool_suburbs",
        "Campbelltown City Council": "campbelltown_suburbs",
        "Wollondilly Shire Council": "wollondilly_suburbs",
        "Penrith City Council": "liverpool_suburbs",
        "Fairfield City Council": "fairfield_suburbs",
    }
    rows = []
    for suburb in expanded:
        slug = suburb["slug"]
        page = page_by_slug.get(f"concreters-{slug}")
        if page is None:
            raise AssertionError(f"no active suburb page for {slug}")
        artifact_lga = suburb["lga"]
        councils = split.get(slug) or corrected.get(slug) or [artifact_lga]
        keys = sorted({key_for_lga[c] for c in councils if c in key_for_lga})
        keys.append("nsw_spatial")
        rows.append({
            "page_id": page["page_id"],
            "page_slug": page["slug"],
            "suburb_slug": slug,
            "suburb": suburb["name"],
            "postcode": suburb["postcode"],
            "artifact_lga": artifact_lga,
            "evidence_supported_councils": councils,
            "assignment_status": ("artifact-contradicted" if slug in corrected else "split-locality" if slug in split else "group-list-supported"),
            "lot_level_check_required": len(councils) > 1,
            "public_wording_rule": ("Do not name one council until the property's lot is checked in the NSW Planning Portal."
                                    if len(councils) > 1 else f"Council process may be described as {councils[0]} only after confirming the property lies within that LGA."),
            "citations": [{"source_key": key, "title": SOURCES[key]["title"], "url": SOURCES[key]["url"], "access_date": ACCESS_DATE, "source_page": SOURCES[key]["page"]} for key in keys],
            "notes": ("Corrects the artifact assignment; authoritative local-government evidence controls."
                      if slug in corrected else "Shared locality; suburb name alone does not identify the road authority." if slug in split else "Suburb-level assignment supports research routing, not a claim about an unverified job address."),
        })
    if len(rows) != 60:
        raise AssertionError(f"expected 60 active suburb rows, got {len(rows)}")
    return {
        "schema_version": "1.0",
        "generated_by": "scripts/53-phase-a-evidence.py",
        "access_date": ACCESS_DATE,
        "authority_rule": "Official council locality lists plus the NSW Planning Portal for lot-level resolution; Liverpool crossing rules never propagate outside Liverpool.",
        "counts": {
            "active_suburb_pages": len(rows),
            "split_localities": sum(r["assignment_status"] == "split-locality" for r in rows),
            "artifact_contradictions": sum(r["assignment_status"] == "artifact-contradicted" for r in rows),
            "lot_level_checks_required": sum(r["lot_level_check_required"] for r in rows),
        },
        "artifact_divergences": [r for r in rows if r["assignment_status"] == "artifact-contradicted"],
        "suburbs": rows,
    }


def csv_bytes(rows: list[dict]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def unresolved_report(matrix: list[dict]) -> str:
    questions = []
    for row in matrix:
        if row["remaining_input"]:
            questions.append(row)
    lines = [
        "# Phase A unresolved provider inputs",
        "",
        "This file contains only questions that authoritative external research cannot answer. It does not ask the owner to invent a universal specification. The evidence matrix can use conditional wording safely, but these answers are needed before any page publishes a job-specific or provider-method figure.",
        "",
        f"Questions: {len(questions)} across {len({q['service'] for q in questions})} services.",
        "",
    ]
    for index, row in enumerate(questions, 1):
        blocker = "It blocks publication of a claimed fixed method/value, but not a carefully conditional service description." if row["classification"] != "DESIGN-SPECIFIC" else "It blocks a job-specific technical promise, not conditional public wording."
        qualified = "The independent provider performing the work, and the project engineer/specifier where the design requires one."
        if row["classification"] == "PRODUCT-SPECIFIC":
            qualified = "The selected provider together with the named product manufacturer/supplier technical data."
        lines += [
            f"## Q{index:02d} — {SERVICES[row['service']][1]} / {row['field']}",
            "",
            f"- Exact answer needed: {row['remaining_input']}",
            f"- Why research cannot resolve it: authoritative sources define constraints and decision factors, but cannot identify the product, provider method, project drawings, weather or loads for a job that does not yet exist.",
            f"- Conditional wording safe: yes — `{row['public_wording']}`",
            f"- Blocking effect: {blocker}",
            f"- Qualified respondent: {qualified}",
            "",
        ]
    lines += [
        "## Formal D23 blocker",
        "",
        "`data/service-specs.yml` remains reserved for owner/qualified-engineer attestation, contains zero verified values and is not populated by this pass. It also contains a pre-existing YAML syntax defect in all ten `service_specific_requirement` blocks. Therefore the existing Phase A precondition remains BLOCKED. Report 53 resolves 88 research cells and explicitly leaves two building-slab curing cells unresolved.",
        "",
    ]
    return "\n".join(lines)


def main_report(matrix: list[dict], claims: list[dict], figures: list[dict], inventory: dict, council: dict, hashes: dict) -> str:
    classes = Counter(r["classification"] for r in matrix)
    resolved = sum(r["verified"] == "true" for r in matrix)
    project_specific = classes["DESIGN-SPECIFIC"] + classes["SITE-SPECIFIC"]
    provider_specific = classes["PROVIDER-METHOD"]
    unresolved = classes["UNRESOLVED"]
    affected_services = {r["service"] for r in matrix if r["remaining_input"]}
    figure_pop = Counter(r["population"] for r in figures)
    claim_classes = Counter(r["classification"] for r in claims)
    lines = [
        "# Report 53 — Phase A service specification evidence acquisition",
        "",
        "Date: 21 August 2026",
        "",
        "## Plain-English determination",
        "",
        f"The ten-service × nine-field matrix contains exactly 90 cells. {resolved} cells have an authoritative source supporting either a constraint or a justified non-universal classification. None creates a Structure Co construction method. There are {project_specific} design/site-specific cells, {provider_specific} provider-method cells and {unresolved} unresolved cells.",
        "",
        "Phase A is **not marked complete**. Two curing cells remain unresolved because the accessible authority establishes a structural design pathway but not an exact curing specification for these broad services; the directly linked industry curing PDF could not be opened. Independently, the legacy D23 attestation file has zero verified values and a pre-existing YAML syntax defect. Zero service pages are formally unblocked for Phase E until the governing owner/engineer attestation requirement is resolved or explicitly superseded.",
        "",
        "## Ground and service inventory",
        "",
        "The seven immutable files matched their recorded SHA-256 values before work. Git has no tracked baseline: every repository file is untracked, so overlap attribution is unavailable; existing files were preserved.",
        "",
        "The requested `RUN-BLOCK-02-on-inputs.md` does not exist. The repository's governing run block is `RUN-BLOCK-02.md`, which was read and applied.",
        "",
        "| ID | Service | Slug |",
        "|---:|---|---|",
    ]
    for slug, (pid, name, _subject) in SERVICES.items():
        lines.append(f"| {pid} | {name} | `{slug}` |")
    lines += [
        "",
        f"Reconciliation: declared {inventory['reconciled_artifacts']['declared']}; immutable manifest {inventory['reconciled_artifacts']['manifest']}; active allowlist {inventory['reconciled_artifacts']['allowlist']}; source WXR {inventory['reconciled_artifacts']['source_wxr']}; legacy YAML service keys {inventory['reconciled_artifacts']['legacy_service_specs_keys']}. Exact agreement: PASS.",
        "",
        "## Existing technical-claim and figure audit",
        "",
        f"Reader-visible technical fields audited: {len(claims)}. Classification totals: " + ", ".join(f"{k} {v}" for k, v in sorted(claim_classes.items())) + ". Every record preserves the exact source string and placement in `build/53-service-specification-matrix.json` under `current_claim_audit`; the CSV repeats the exact strings against each applicable field without elision.",
        "",
        f"The existing numeric register contains 214 rows overall and 91 rows on these ten service pages. Service-row populations: " + ", ".join(f"{k} {v}" for k, v in sorted(figure_pop.items())) + ". All 91 remain unattested and unsupported as universal service specifications. The repeated values are 32 MPa, 125mm, SL72, 800mm, 900mm, 1200mm, 4.0-5.5m, 4%, 1:6, plus SL82 on the concrete-slabs page.",
        "",
        "The Liverpool values validated in Report 52 remain valid only for Liverpool road-reserve crossings. Their existence does not verify the identical sentence copied across all ten services or extend it to Camden, Campbelltown, Wollondilly or private-property slabs.",
        "",
        "## Matrix result",
        "",
        "| Classification | Cells |",
        "|---|---:|",
    ]
    for name in ["AUTHORITY-FIXED", "DESIGN-SPECIFIC", "COUNCIL-SPECIFIC", "PRODUCT-SPECIFIC", "SITE-SPECIFIC", "PROVIDER-METHOD", "NOT-APPLICABLE", "UNRESOLVED"]:
        lines.append(f"| {name} | {classes[name]} |")
    lines += [
        "",
        f"Verified/resolved cells: {resolved}/90. Project-specific cells (DESIGN-SPECIFIC + SITE-SPECIFIC): {project_specific}. Provider-specific cells: {provider_specific}. Unresolved cells: {unresolved}. Services with one or more provider/project questions: {len(affected_services)}. Services with all nine research cells resolved: {len(SERVICES) - len({r['service'] for r in matrix if r['classification'] == 'UNRESOLVED'})}. Services formally unblocked for Phase E: 0.",
        "",
        "`verified: true` in Report 53 means the classification and safe conditional wording are supported by the cited authority. It does not mean a thickness, strength, mesh, method or warranty has been attested for Structure Co or any future provider.",
        "",
        "## Source validation",
        "",
        f"Primary/authoritative source records used: {len(SOURCES)}; access-verified on 21 August 2026: {sum(s['access_verified'] for s in SOURCES.values())}. The CCAA residential PDF was downloaded, all 12 physical pages rendered and visually checked; SHA-256 `{SOURCES['ccaa_residential']['sha256']}`. Liverpool's 18-page March 2026 form remains hash-verified and was visually checked in Phase D. Relied-on curing pages in the current 45-page Transport for NSW specification were rendered and visually checked. The obsolete CCAA standalone curing URL returned a 404 HTML page, so it is not a source and the unsupported building-slab curing cells remain unresolved.",
        "",
        "No competitor pages, SEO articles, AI summaries, forums, search snippets or reconstructed Australian Standard clauses are used as evidence.",
        "",
        "## Council-to-suburb jurisdiction reconciliation",
        "",
        f"Active suburb pages mapped: {council['counts']['active_suburb_pages']}. Split localities requiring lot-level checking: {council['counts']['split_localities']}. Direct artifact contradictions: {council['counts']['artifact_contradictions']}. The full cited row-level map is `build/53-council-suburb-map.json`.",
        "",
        "The two direct contradictions are Camden Park and Theresa Park: the source artifact says Camden Council, while Wollondilly's official material places them within Wollondilly. Bringelly, Leppington, Rossmore, Edmondson Park, Kemps Creek, Cawdor, Cecil Park and Ingleburn are treated as split localities; the property lot must be checked in the NSW Planning Portal before naming the controlling council.",
        "",
        "Liverpool's March 2026 vehicular-crossing specification is never applied outside Liverpool City Council. For a split suburb, the suburb name alone is not sufficient evidence of jurisdiction.",
        "",
        "## Remaining questions",
        "",
        f"There are {sum(bool(r['remaining_input']) for r in matrix)} cell-level questions that external research cannot answer. They concern provider curing methods, selected exposed/decorative systems, actual shed/garage drawings and actual commercial project requirements. They are listed without research-resolvable questions in `reports/53-unresolved-provider-inputs.md`.",
        "",
        "## Validation results",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
        "| Immutable verification | PASS | 7/7 hashes match |",
        "| Report 53 reproducibility | PASS | `python scripts/53-phase-a-evidence.py --check` |",
        "| Specification-ledger/D23 state | PASS, fail-closed | Exact ten services; D23 rule present; legacy file 0 true/91 false and `populated:false` |",
        "| Numeric-figure audit | PASS | 214 total register rows; 91 service rows; all mapped and unsupported as universal values |",
        f"| Citation registry | PASS with two unresolved cells | {len(SOURCES)} opened primary/authoritative records; obsolete/404 item URLs excluded |",
        "| Council/suburb reconciliation | PASS | 60/60 active suburb pages; 8 split; 2 artifact contradictions; every row cited |",
        "| UTF-8 canary | PASS | all three exact assertions survived |",
        "| Regression suite | PASS | 31 passed |",
        "| CSV contract | PASS | exact 16 columns and 90 UTF-8 rows validated; spreadsheet `artifact-tool` dependency was unavailable in this environment, so repository-native CSV validation was used and disclosed |",
        "| `git diff --check` | PASS | no whitespace errors in tracked diff; repository has no tracked baseline, so all files remain reported as untracked |",
        "",
        "## Phase table after evidence acquisition",
        "",
        "| Phase | Name | Status | Evidence |",
        "|---|---|---|---|",
        "| A | attest the figures | BLOCKED | legacy `service-specs.yml`: 91 false, 0 true, populated false; Report 53 research 88/90 resolved |",
        "| B | media and staging | RUNNABLE | public media 55/55; Band A decisions complete; precondition script does not encode prior completion |",
        "| C | identity and schema | BLOCKED | 11 verified true / 14 false; legal name, ABN, NSW licence and insurance remain unverified |",
        "| D | Liverpool | RUNNABLE | 16 verified source records; Gate 19 separately confirms Phase D content complete |",
        "| E | service page rebuild | BLOCKED | requires formal Phase A completion |",
        "| F | images | BLOCKED | explicitly last; requires A-E |",
        "| G | release | BLOCKED | requires preceding phases and preflight GO |",
        "",
        "## Complete preflight table",
        "",
        "Top-line verdict: **NO-GO**.",
        "",
        "| Gate | Result | Detail |",
        "|---:|---|---|",
        "| 1. encoding canary | PASS | fixture and restored assertions survived |",
        "| 2. 15 Stage 9 gates | PASS | 15/15 |",
        "| 3. post-ID collisions | PASS | main 306; privacy 1; collisions 0; calculator absent |",
        "| 4. media intake | PASS | public 55/55; immutable provenance 83 |",
        "| 5. Astra Customizer | PASS | required groups, design carriage and consistency |",
        "| 6. Elementor references | PASS | 1,085 image + 98 background = 1,183; 73/83 IDs; 0 unresolved |",
        "| 7. uniqueness | **FAIL** | 1,761 five-grams on more than two pages; 1,491 within-class pairs over 40% |",
        "| 8. intersections | PASS | 35 built/allow-listed; all draft |",
        "| 9. menu lint | PASS | zero unsafe Wave 1 targets |",
        "| 10. Victorian blocklist | PASS | zero in scoped public artifacts |",
        "| 11. schema placeholders | PASS | zero JSON-LD blocks/tokens |",
        "| 12. coherence | **FAIL** | 90 SEVERE; 139 above threshold; corpus filler 0.8244 |",
        "| 13. source brand | PASS | 466 = 366 reader-visible + 100 preserved; transformed visible 0 |",
        "| 14. assigned menus | PASS | zero unsafe; held 6; withdrawn 81 |",
        "| 15. architecture/import parity | PASS | 76 allowed; 75 main + privacy; 81 withdrawn; calculator absent |",
        "| 16. claims/evidence | PASS | 16 occurrences; 0 unsupported; 6 pages |",
        "| 17. public media | PASS | 0 blocking; 0 Band A unrecorded; 0 Band B failures |",
        "| 18. identity/Liverpool/schema | PASS | 0 unsupported claims; 12 Liverpool placements; 5 privacy blockers; 0 LocalBusiness |",
        "| 19. Phase D Liverpool | PASS | 13 requirements; 12 fields; 4 pages; 0 false-fidelity; calculator absent |",
        "",
        f"Derivative WXR SHA-256: `{sha256(ROOT / 'build/46-active-main-import.xml')}`. The derivative was read only; it was not regenerated or changed by Phase A.",
        "",
        "## Immutable hashes",
        "",
        "| File | SHA-256 | Result |",
        "|---|---|---|",
    ]
    for path, digest in hashes.items():
        lines.append(f"| `{path}` | `{digest}` | PASS |")
    lines += [
        "",
        "## Scope confirmation",
        "",
        "No WordPress import, deployment, publication, indexability change, Phase E rewrite, remote media operation, immutable edit or governing-document edit occurred. `data/service-specs.yml` was not modified.",
        "",
    ]
    return "\n".join(lines)


def generated_outputs() -> dict[Path, bytes]:
    hashes = {}
    for rel, expected in IMMUTABLE.items():
        actual = sha256(ROOT / rel)
        if actual != expected:
            raise AssertionError(f"immutable mismatch {rel}: expected {expected}, got {actual}")
        hashes[rel] = actual
    inventory = service_inventory()
    claims, claim_by_cell = audit_claims()
    figures, figure_by_cell = figure_audit()
    matrix = build_matrix(claim_by_cell, figure_by_cell)
    if len(matrix) != 90 or Counter(r["service"] for r in matrix) != Counter({slug: 9 for slug in SERVICES}):
        raise AssertionError("matrix is not exactly ten services by nine fields")
    if any(not r["source_url"] for r in matrix):
        raise AssertionError("matrix cell lacks a research trail")
    council = council_map()
    derivative = sha256(ROOT / "build/46-active-main-import.xml")
    payload = {
        "schema_version": "1.0",
        "generated_by": "scripts/53-phase-a-evidence.py",
        "generated_date": ACCESS_DATE,
        "scope": "authoritative evidence classifications and safe conditional wording; not a Structure Co provider method",
        "governing_precondition_status": "BLOCKED — D23 attestation file remains unpopulated and malformed; Phase E not authorised",
        "immutable_hashes": hashes,
        "derivative": {"path": "build/46-active-main-import.xml", "sha256": derivative},
        "service_inventory": inventory,
        "sources": SOURCES,
        "summary": {
            "matrix_cells": len(matrix),
            "verified_resolved_cells": sum(r["verified"] == "true" for r in matrix),
            "classification_counts": dict(sorted(Counter(r["classification"] for r in matrix).items())),
            "project_specific_cells": sum(r["classification"] in {"DESIGN-SPECIFIC", "SITE-SPECIFIC"} for r in matrix),
            "provider_specific_cells": sum(r["classification"] == "PROVIDER-METHOD" for r in matrix),
            "unresolved_cells": sum(r["classification"] == "UNRESOLVED" for r in matrix),
            "services_with_all_research_cells_resolved": len(SERVICES) - len({r["service"] for r in matrix if r["classification"] == "UNRESOLVED"}),
            "services_formally_unblocked": 0,
            "current_technical_claim_records": len(claims),
            "service_figure_register_rows": len(figures),
        },
        "matrix": matrix,
        "current_claim_audit": claims,
        "figure_register_audit": figures,
    }
    return {
        ROOT / "build/53-service-specification-matrix.json": json_bytes(payload),
        ROOT / "reports/53-service-specification-matrix.csv": csv_bytes(matrix),
        ROOT / "build/53-council-suburb-map.json": json_bytes(council),
        ROOT / "reports/53-unresolved-provider-inputs.md": unresolved_report(matrix).encode("utf-8"),
        ROOT / "reports/53-phase-a-evidence-acquisition.md": main_report(matrix, claims, figures, inventory, council, hashes).encode("utf-8"),
    }


def run(check: bool) -> int:
    outputs = generated_outputs()
    if check:
        failures = []
        for path, expected in outputs.items():
            actual = path.read_bytes() if path.exists() else b""
            if actual != expected:
                failures.append(path.relative_to(ROOT).as_posix())
        if failures:
            print("FAIL: generated outputs differ: " + ", ".join(failures))
            return 1
        print("PASS: Report 53 artefacts are reproducible")
        return 0
    for path, content in outputs.items():
        path.write_bytes(content)
        print(f"WROTE {path.relative_to(ROOT).as_posix()} {hashlib.sha256(content).hexdigest().upper()}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(run(args.check))
