#!/usr/bin/env python3
"""Validate the 21 August owner facts, claims, Liverpool evidence and schema."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.content_remediation import (  # noqa: E402
    ADMIN_ADDRESS,
    FORMS_URL,
    LIVERPOOL_BLOCKS,
    LIVERPOOL_SLUGS,
    NO_CONTRACT_TEXT,
    PDF_URL,
    PORTAL_URL,
    PUBLIC_EMAIL,
    PUBLIC_LABEL,
    PUBLIC_PHONE,
    PUBLIC_PHONE_URI,
    ROLE_TEXT,
)
from lib.preimport_safety import items, metas, parse_wxr, post_id, post_slug, post_type, visible_page_fields  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FACTS = ROOT / "data" / "verified-facts.yml"
COUNCIL = ROOT / "data" / "council-specs.yml"
MAIN = ROOT / "build" / "46-active-main-import.xml"
PRIVACY = ROOT / "build" / "51-privacy-import.xml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
CLAIMS = ROOT / "reports" / "46-claim-evidence-gate.json"
DISPOSITIONS = ROOT / "build" / "51-claim-disposition-register.json"
SCHEMA = ROOT / "build" / "30-schema-output.json"
OUT = ROOT / "reports" / "51-evidence-validation.json"

EXPECTED_PDF_SHA256 = "43F74C0F01C5EA6F0C89919BE8C1859F758F96AF549A9CF71ADA5F87DD7CAF33"
EXPECTED_PRIVACY_MARKERS = {
    "[[PLACEHOLDER: accountable legal entity for privacy obligations]]",
    "[[VERIFY: form delivery, authenticated sending domain, database storage and access controls before publication.]]",
    "[[PLACEHOLDER: owner-decided retention period]]",
    "[[VERIFY: confirm which analytics or tracking scripts are installed before publication and describe them here, or state that none are present.]]",
    "[[PLACEHOLDER: publication date]]",
}


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")


def item_by_slug(tree: object) -> dict[str, object]:
    return {
        post_slug(item): item
        for item in items(tree)
        if post_type(item) == "page"
    }


def page_blob(item: object) -> str:
    return "\n".join(field["text"] for field in visible_page_fields(item))


def validate_owner(facts: dict) -> dict:
    legal = facts["legal_entity"]
    contact = facts["contact"]
    role = facts["operating_model"]
    checks = {
        "public_label": legal["trading_name"]["verified"] is True and legal["trading_name"]["value"] == PUBLIC_LABEL,
        "email": contact["email"]["verified"] is True and contact["email"]["value"] == PUBLIC_EMAIL,
        "phone": contact["phone"]["verified"] is True and contact["phone"]["value"] == PUBLIC_PHONE and contact["phone"]["uri"] == PUBLIC_PHONE_URI,
        "address": contact["street_address"]["verified"] is True and contact["street_address"]["value"] == ADMIN_ADDRESS,
        "staffed": contact["is_staffed"]["verified"] is True and contact["is_staffed"]["value"] is True,
        "not_open_to_visitors": contact["open_to_visitors"]["verified"] is True and contact["open_to_visitors"]["value"] is False,
        "not_customer_facing": contact["customer_facing_premises"]["verified"] is True and contact["customer_facing_premises"]["value"] is False,
        "operating_model": role["verified"] is True and role["value"] == ROLE_TEXT and role["structure_co_direct_contractor"] is False,
        "no_contract": role["enquiry_contract_disclosure"] == NO_CONTRACT_TEXT,
        "no_abn": legal["abn"]["verified"] is False and not legal["abn"]["value"],
        "no_legal_entity": legal["legal_name"]["verified"] is False and not legal["legal_name"]["value"],
        "no_credential": all(not facts["licensing"][key]["verified"] and not facts["licensing"][key]["value"] for key in facts["licensing"]),
        "service_areas_unverified": facts["service_areas"]["verified"] is False and facts["service_areas"]["value"] == [],
    }
    if not all(checks.values()):
        raise AssertionError(f"owner-attestation assertions failed: {checks}")
    return {"result": "PASS", "checks": checks}


def validate_contacts(main_tree: object, privacy_tree: object) -> dict:
    raw_main = MAIN.read_text(encoding="utf-8", errors="strict")
    raw_privacy = PRIVACY.read_text(encoding="utf-8", errors="strict")
    raw = raw_main + raw_privacy
    assert_equal(raw.count("03 4517 6915"), 0, "superseded phone occurrences")
    assert_equal(raw.count("tel:+61345176915"), 0, "superseded phone URI occurrences")
    counts = {
        "public_phone": raw.count(PUBLIC_PHONE),
        "public_phone_uri": raw.count(PUBLIC_PHONE_URI),
        "public_email": raw.count(PUBLIC_EMAIL),
        "administrative_address": raw.count(ADMIN_ADDRESS),
        "no_contract_disclosure": raw.count(NO_CONTRACT_TEXT),
    }
    if min(counts.values()) < 1:
        raise AssertionError(f"attested contact/disclosure placement absent: {counts}")
    if re.search(r"(?:local|Camden|Sydney) (?:phone|telephone|number).{0,40}\(03\) 4328 3392", raw, re.I):
        raise AssertionError("public telephone is described as local")
    if re.search(r"\b(?:visit our office|walk[- ]in office|customer-service location|showroom)\b", raw, re.I):
        raise AssertionError("customer-facing office invitation remains")

    form_pages = {"about", "contact", "gallery", "quote"}
    form_adjacencies: dict[str, dict] = {}
    for slug, item in item_by_slug(main_tree).items():
        if slug not in form_pages:
            continue
        matches = []
        for _meta, key, value_node in metas(item):
            if key != "_elementor_data":
                continue
            data = json.loads(value_node.text or "[]")

            def walk(node: object) -> None:
                if isinstance(node, dict):
                    elements = node.get("elements")
                    if isinstance(elements, list):
                        for index, child in enumerate(elements):
                            if not isinstance(child, dict) or child.get("widgetType") != "shortcode":
                                continue
                            shortcode = child.get("settings", {}).get("shortcode")
                            if shortcode != '[fluentform id="3"]':
                                continue
                            adjacent = elements[index + 1] if index + 1 < len(elements) else {}
                            disclosure = (
                                adjacent.get("settings", {})
                                .get("title", {})
                                .get("value", {})
                                .get("content", {})
                                .get("value")
                            ) if isinstance(adjacent, dict) else None
                            matches.append((shortcode, disclosure))
                    for child in node.values():
                        if isinstance(child, (dict, list)):
                            walk(child)
                elif isinstance(node, list):
                    for child in node:
                        walk(child)

            walk(data)
        if matches != [('[fluentform id="3"]', NO_CONTRACT_TEXT)]:
            raise AssertionError(f"form/non-contract adjacency failure on {slug}: {matches}")
        form_adjacencies[slug] = {"form_id": 3, "adjacent_disclosure": NO_CONTRACT_TEXT}
    assert_equal(set(form_adjacencies), form_pages, "form placement pages")
    return {"result": "PASS", "counts": counts, "form_adjacencies": form_adjacencies}


def validate_liverpool(council: dict, main_tree: object) -> dict:
    source = council["liverpool"]["source_set"]
    assert_equal(source["forms_page"]["source_url"], FORMS_URL, "Liverpool forms URL")
    assert_equal(source["vehicular_crossing_form_march_2026"]["source_url"], PDF_URL, "Liverpool PDF URL")
    assert_equal(source["vehicular_crossing_form_march_2026"]["sha256"], EXPECTED_PDF_SHA256, "Liverpool PDF hash")
    assert_equal(source["vehicular_crossing_form_march_2026"]["pages"], 18, "Liverpool PDF page count")
    assert_equal(source["online_application_portal"]["source_url"], PORTAL_URL, "Liverpool portal URL")
    if any(node["sighted_date"] != "2026-08-21" or node["verified"] is not True for node in source.values()):
        raise AssertionError("Liverpool source set is not fully sighted/verified on 2026-08-21")
    requirements = council["liverpool"]["requirements"]
    if len(requirements) != 13 or any(node["verified"] is not True for node in requirements.values()):
        raise AssertionError("Liverpool current-form requirement set is incomplete")

    page_items = item_by_slug(main_tree)
    placements: dict[str, int] = {}
    for slug in sorted(LIVERPOOL_SLUGS):
        blob = page_blob(page_items[slug])
        missing = [index + 1 for index, block in enumerate(LIVERPOOL_BLOCKS) if block not in blob]
        if missing:
            raise AssertionError(f"Liverpool evidence blocks missing from {slug}: {missing}")
        if "verified project record says" in blob.lower():
            raise AssertionError(f"false project-record wording remains on {slug}")
        if re.search(r"fees?[^.]{0,80}\$\s*[0-9]", blob, re.I):
            raise AssertionError(f"invented Liverpool fee amount remains on {slug}")
        placements[slug] = sum(block in blob for block in LIVERPOOL_BLOCKS)
    assert_equal(sum(placements.values()), 12, "Liverpool evidence placements")
    return {
        "result": "PASS",
        "official_sources": [FORMS_URL, PDF_URL, PORTAL_URL],
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "verified_requirements": len(requirements),
        "page_evidence_placements": placements,
    }


def validate_privacy(privacy_tree: object) -> dict:
    pages = item_by_slug(privacy_tree)
    assert_equal(set(pages), {"privacy-policy"}, "privacy derivative page set")
    item = pages["privacy-policy"]
    content = item.findtext("{http://purl.org/rss/1.0/modules/content/}encoded") or ""
    markers = set(re.findall(r"\[\[(?:PLACEHOLDER|VERIFY):[^\]]+\]\]", content))
    assert_equal(markers, EXPECTED_PRIVACY_MARKERS, "privacy blocking markers")
    for token in (PUBLIC_LABEL, PUBLIC_EMAIL, PUBLIC_PHONE, ADMIN_ADDRESS, ROLE_TEXT, NO_CONTRACT_TEXT, "not open to customers or visitors"):
        if token not in content:
            raise AssertionError(f"privacy policy omits required fact/disclosure: {token}")
    if "ABN" in content:
        raise AssertionError("privacy policy requests or asserts an ABN")
    return {"result": "PASS", "blocking_markers": sorted(markers), "blocking_count": len(markers)}


def validate_schema() -> dict:
    graphs = json.loads(SCHEMA.read_text(encoding="utf-8", errors="strict"))
    types = Counter(str(node.get("@type")) for graph in graphs.values() for node in graph["@graph"])
    assert_equal(len(graphs), 76, "schema graph count")
    assert_equal(types["Service"], 70, "schema Service count")
    blob = json.dumps(graphs, ensure_ascii=False)
    for token in ("LocalBusiness", "GeneralContractor", '"@type": "Organization"', '"provider"', '"legalName"', '"taxID"', '"openingHours"', '"AggregateRating"'):
        if token in blob:
            raise AssertionError(f"unsupported schema token emitted: {token}")
    names = {node["name"] for graph in graphs.values() for node in graph["@graph"] if node.get("@type") == "WebSite"}
    assert_equal(names, {PUBLIC_LABEL}, "schema WebSite name")
    return {"result": "PASS", "graphs": len(graphs), "service_nodes": types["Service"], "organization": 0, "localbusiness": 0, "providers": 0}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        required = (FACTS, COUNCIL, MAIN, PRIVACY, ALLOWLIST, CLAIMS, DISPOSITIONS, SCHEMA)
        missing = [p.relative_to(ROOT).as_posix() for p in required if not p.exists()]
        if missing:
            raise AssertionError("validation inputs absent: " + ", ".join(missing))
        facts = yaml.safe_load(FACTS.read_text(encoding="utf-8", errors="strict"))
        council = yaml.safe_load(COUNCIL.read_text(encoding="utf-8", errors="strict"))
        main_tree = parse_wxr(MAIN)
        privacy_tree = parse_wxr(PRIVACY)
        claims = json.loads(CLAIMS.read_text(encoding="utf-8", errors="strict"))
        dispositions = json.loads(DISPOSITIONS.read_text(encoding="utf-8", errors="strict"))
        assert_equal(claims["result"], "PASS", "claim gate result")
        assert_equal(claims["totals"]["unsupported"], 0, "unsupported current claims")
        assert_equal((dispositions["totals"]["legacy_occurrences"], dispositions["totals"]["legacy_unsupported"]), (232, 228), "legacy claim baseline")
        assert_equal(dispositions["totals"]["final_unsupported"], 0, "final unsupported register")

        sections = {
            "owner_attestation": validate_owner(facts),
            "contact_consistency": validate_contacts(main_tree, privacy_tree),
            "liverpool_sources": validate_liverpool(council, main_tree),
            "privacy_markers": validate_privacy(privacy_tree),
            "schema": validate_schema(),
            "claims": {
                "result": "PASS",
                "legacy_occurrences": 232,
                "legacy_unsupported_dispositioned": 228,
                "additional_blind_spot_occurrences_dispositioned": dispositions["totals"]["additional_blind_spot_occurrences"],
                "current_supported": claims["totals"]["supported"],
                "current_unsupported": 0,
            },
        }
        result = {"result": "PASS", "sections": sections, "errors": []}
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            "PASS — owner/contact/Liverpool/privacy/schema validation: "
            "232/228 dispositioned; current unsupported=0; Liverpool placements=12; privacy blockers=5"
        )
        return 0
    except Exception as exc:
        result = {"result": "FAIL", "sections": {}, "errors": [str(exc)]}
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"FAIL — owner/contact/Liverpool/privacy/schema validation: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
