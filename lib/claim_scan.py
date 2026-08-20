"""Shared reader-visible claim detection for pre-import controls.

The legacy rules reproduce the 20 August 2026 232-occurrence register when
run before D32/media remediation (228 text/widget rows plus four Band B
adjacencies).  The additional rules close marketing-copy blind spots found in
the 21 August identity pass.  Nothing in this module mutates content.
"""
from __future__ import annotations

import csv
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from lib.preimport_safety import (
    items,
    metas,
    post_id,
    post_slug,
    post_type,
    visible_page_fields,
)


def visible_text(value: str) -> str:
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def verified(node: object) -> bool:
    return isinstance(node, dict) and node.get("verified") is True


def nonempty_verified(node: object) -> bool:
    return verified(node) and bool(node.get("value"))


def negated_review(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:no|not|never|don['\N{RIGHT SINGLE QUOTATION MARK}]t|do not)\b.{0,50}"
            r"\b(?:review|testimonial)",
            text,
            re.I,
        )
    )


def privacy_response(text: str) -> bool:
    lower = text.lower()
    return (
        "reasonable period" in lower
        and "personal information" in lower
        and "office of the australian information commissioner" in lower
    )


def privacy_warranty_context(text: str) -> bool:
    lower = text.lower()
    return "tax and warranty purposes" in lower and "personal information" in lower


def permitted_operating_role(facts: dict, text: str) -> bool:
    role = facts.get("operating_model", {})
    lower = visible_text(text).lower()
    return (
        verified(role)
        and "manages concreting enquiries" in lower
        and "coordinates suitable independent providers" in lower
        and "must be confirmed before work begins" in lower
    )


@dataclass(frozen=True)
class Rule:
    category: str
    pattern: re.Pattern[str]
    citation: str
    disposition: str
    evidence_ok: Callable[[dict, str], bool]


def _rule(
    category: str,
    pattern: str,
    citation: str,
    disposition: str,
    evidence_ok: Callable[[dict, str], bool] | None = None,
) -> Rule:
    return Rule(
        category,
        re.compile(pattern, re.I),
        citation,
        disposition,
        evidence_ok or (lambda _facts, _text: False),
    )


def legacy_rules() -> list[Rule]:
    """The exact rule family used for the recorded 232/228 baseline."""
    return [
        _rule(
            "licence_insurance_accreditation",
            r"Licensed\s*&\s*Insured|NSW licence|Fair Trading licence|\baccredit(?:ed|ation)?\b|\bcertified\b",
            "data/verified-facts.yml licensing; no contractor credential is authorised",
            "remove or restate only as a requirement to verify the independent provider",
            lambda f, _t: nonempty_verified(
                f.get("licensing", {}).get("nsw_fair_trading_licence")
            )
            and nonempty_verified(
                f.get("licensing", {}).get("insurance_public_liability")
            ),
        ),
        _rule(
            "fixed_price_on_site_quote",
            r"Fixed-Price On-Site Quotes?|\bfixed price\b|\bfixed-price\b|\bgive you a fixed price\b|\bon[- ]site quote(?:s)?\b",
            "data/verified-facts.yml pricing and owner attestation 21 August 2026",
            "remove the promise; say only that job-specific quotations and terms must be confirmed",
            lambda f, _t: nonempty_verified(f.get("pricing", {}).get("per_m2_ranges"))
            and nonempty_verified(f.get("pricing", {}).get("minimum_job_value")),
        ),
        _rule(
            "workmanship_guarantee_warranty",
            r"workmanship guarantee|\bguarantee(?:d)?\b|\bwarrant(?:y|ies|ed)\b",
            "no verified written guarantee or warranty instrument",
            "remove the promise or state only that provider-specific terms must be confirmed",
            lambda f, text: privacy_warranty_context(text) or permitted_operating_role(f, text),
        ),
        _rule(
            "contractor_operator_claim",
            r"\bwe\s+(?:pour|build|handle|measure|install|prepare|remove|replace|deliver|service|do|match|lay|construct|excavate|form|reinforce|finish|manage|organise|coordinate|supply|complete|create|repair|resurface|clean|cut|seal|assess|inspect|quote|provide|offer)\b|\bour\s+(?:work\s+starts|crew|team|concreters?)\b|\bconcreters who do it\b",
            "owner operating-model attestation, 21 August 2026",
            "replace direct-contractor wording with the authorised enquiry-coordination disclosure",
            permitted_operating_role,
        ),
        _rule(
            "local_operation_or_premises",
            r"Camden based|\bbased in Camden\b|\blocal concreters?\b|\bour local\b|\bmost of our work starts\b|\bwork across\b|\bserving (?:Camden|South West Sydney)\b",
            "administrative office is not customer-facing; service_areas remains unverified",
            "remove local-contractor/premises implication",
            lambda f, _t: nonempty_verified(f.get("service_areas"))
            and verified(f.get("contact", {}).get("customer_facing_premises"))
            and f["contact"]["customer_facing_premises"].get("value") is True,
        ),
        _rule(
            "service_area_claim",
            r"AREAS WE COVER|SERVICE AREAS|\bwe work across\b|\bserv(?:e|ing) (?:the )?(?:Camden|South West Sydney)\b",
            "data/verified-facts.yml service_areas verified:false and empty",
            "replace with non-service suburb information or remove",
            lambda f, _t: nonempty_verified(f.get("service_areas")),
        ),
        _rule(
            "false_verified_project_record",
            r"verified project record says",
            "DECISION-06 D32: no Camden job completed or scheduled",
            "remove false project-record framing; retain only separately sourced public facts",
        ),
        _rule(
            "researched_job_record",
            r"The researched [^.]{0,80} job record contains",
            "DECISION-06 D32: no Camden job record exists",
            "remove the invented job-record construction",
        ),
        _rule(
            "real_photo_pending_local_project",
            r"\[\[REAL_PHOTO_PENDING:[^\]]+\]\]",
            "DECISION-06 D32 and Report 50",
            "remove the evidential local-work module",
        ),
        _rule(
            "review_rating_testimonial",
            r"\btestimonial(?:s)?\b|\breview(?:s|er)?\b|\bstar rating\b|\brated\s+[0-9]|verified reviewer name|verified .*review text",
            "data/verified-facts.yml reviews verified:false; permission_to_publish:false",
            "remove review/testimonial claim",
            lambda f, text: negated_review(text)
            or (
                nonempty_verified(f.get("reviews"))
                and f.get("reviews", {}).get("permission_to_publish") is True
            ),
        ),
        _rule(
            "award_claim",
            r"\baward(?:ed|s|[- ]winning)?\b",
            "no verified award record",
            "remove or cite awarding body, award and date",
        ),
        _rule(
            "trust_social_proof_claim",
            r"\btrusted by\b|\btrusted (?:local|Camden|concreters?)\b|\bcustomers? trust\b",
            "reviews and completed_projects are unverified",
            "remove unsupported social proof",
            lambda f, _t: nonempty_verified(f.get("reviews"))
            or nonempty_verified(f.get("completed_projects")),
        ),
        _rule(
            "response_time_promise",
            r"\brespond within\b|\bwithin (?:[0-9]+|one|two) (?:hour|hours|day|days)\b|\bsame[- ]day response\b|\bresponse within\b|\breasonable period\b",
            "no verified service SLA; privacy response wording is separate",
            "remove service response promise",
            lambda _f, text: privacy_response(text),
        ),
        _rule(
            "experience_years",
            r"\b[0-9]+\+? years(?: of)? experience\b|\bdecades? of experience\b|\byears in business\b|\byears of experience\b|\b(?:experienced|established) concreters?\b|\bextensive experience\b",
            "no verified operating-history field",
            "remove unsupported experience claim",
        ),
        _rule(
            "completed_job_count_or_recent_work",
            r"\b(?:[0-9,]+\+?|hundreds?|thousands?) (?:jobs|projects|pours)(?: completed)?\b|\bcompleted (?:jobs|projects|pours)\b|\brecent work\b|\blocal work completed\b",
            "DECISION-06 D32; completed_projects verified:false and empty",
            "remove completed-project claim",
            lambda f, _t: nonempty_verified(f.get("completed_projects")),
        ),
    ]


def additional_rules() -> list[Rule]:
    """Marketing surfaces the former detector did not assert."""
    return [
        _rule(
            "quote_or_scope_promise",
            r"Get Your FREE Quote|Request an on-site (?:concrete )?quote|Request a Concrete Quote|provides on-site scopes|for an on-site project(?: scope)?|to quote on the work",
            "owner operating-model attestation; no quotation policy or contractor is authorised",
            "replace with a non-contractual concreting-enquiry invitation",
        ),
        _rule(
            "customer_social_proof_heading",
            r"Why (?:[A-Za-z -]+ )?customers (?:choose|use) us|WHY CUSTOMERS CHOOSE US",
            "reviews and completed_projects are unverified",
            "replace with a factual enquiry-coordination heading",
        ),
        _rule(
            "direct_service_or_scope_presentation",
            r"Structure Co Concreters Camden (?:provides|scopes)|How Structure Co scopes|\bOur Services\b|\bservice range covers\b|\bcurrent service scope\b",
            "owner operating-model attestation, 21 August 2026",
            "replace with enquiry types and the authorised coordination disclosure",
            permitted_operating_role,
        ),
        _rule(
            "local_service_presentation",
            r"Concrete services across Camden and South West Sydney|finished concrete across Camden and South West Sydney|scope in Camden and South West Sydney",
            "service_areas remains unverified",
            "replace with non-geographic enquiry wording",
        ),
        _rule(
            "unsupported_opening_hours",
            r"Mon(?:day)?\s*[-\N{EN DASH}]\s*Fri(?:day)?\s+[0-9:.]+\s*(?:AM|PM)\s*[-\N{EN DASH}]\s*[0-9:.]+\s*(?:AM|PM)",
            "no opening-hours attestation; office is not open to visitors",
            "remove opening-hours presentation",
        ),
        _rule(
            "customer_facing_premises",
            r"\bvisit (?:us|our office)\b|\bshowroom\b|\bwalk[- ]in\b|\bcustomer[- ]service location\b",
            "owner attestation: administrative office is not open to visitors",
            "remove customer-facing premises invitation",
        ),
        _rule(
            "equipment_vehicle_crew_ownership",
            r"\bour (?:vehicles?|trucks?|equipment|machinery|crews?|operators?)\b",
            "no ownership evidence",
            "remove ownership implication",
        ),
        _rule(
            "provider_network_size",
            r"\bnetwork of (?:[0-9]+|hundreds?|dozens?)\b|\b[0-9]+ independent providers?\b|extensive network of friends",
            "no verified provider-network size",
            "remove network-size claim",
        ),
        _rule(
            "unsupported_verified_local_evidence",
            r"verified local job mix|verified local distinction|verified approval (?:record|path)|verified neighbouring service links|using the verified (?:Camden|Liverpool)|verified at the work area|The researched ground note",
            "no occurrence-level evidence citation supports the reader-visible verification claim",
            "remove the claim; use only separately cited current official facts",
        ),
    ]


def all_rules() -> list[Rule]:
    return legacy_rules() + additional_rules()


def claim_widgets(item: object) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for _pm, key, value_node in metas(item):
        if key != "_elementor_data" or not (value_node.text or "").strip():
            continue
        parsed = json.loads(value_node.text or "[]")

        def walk(node: object, path: str = "$") -> None:
            if isinstance(node, dict):
                widget_type = str(node.get("widgetType") or "")
                if re.search(r"testimonial|review|rating|star", widget_type, re.I):
                    settings = node.get("settings") if isinstance(node.get("settings"), dict) else {}
                    parts = []
                    for setting in (
                        "testimonial_content",
                        "testimonial_name",
                        "testimonial_job",
                        "rating",
                        "rating_scale",
                        "title",
                        "text",
                    ):
                        value = settings.get(setting)
                        if value not in (None, "", [], {}):
                            parts.append(f"{setting}={value}")
                    if parts:
                        found.append(
                            {
                                "placement": f"_elementor_data:{path}",
                                "widget_type": widget_type,
                                "exact_claim": " | ".join(parts),
                            }
                        )
                for child_key, child in node.items():
                    if isinstance(child, (dict, list)):
                        walk(child, f"{path}.{child_key}")
            elif isinstance(node, list):
                for index, child in enumerate(node):
                    walk(child, f"{path}[{index}]")

        walk(parsed)
    return found


def scan_claims(
    trees: Iterable[object],
    allowed: dict[int, dict],
    facts: dict,
    ruleset: list[Rule],
) -> tuple[list[dict], list[str], dict[int, list[str]]]:
    found: list[dict] = []
    errors: list[str] = []
    visible_raw_by_page: dict[int, list[str]] = {}
    seen_fields: set[tuple[int, str, str]] = set()
    for tree in trees:
        for item in items(tree):
            if post_type(item) != "page":
                continue
            pid = post_id(item)
            slug = post_slug(item)
            if pid not in allowed:
                errors.append(f"claim scan encountered non-allowlisted page {pid}:{slug}")
                continue
            if allowed[pid]["slug"] != slug:
                errors.append(f"claim scan slug mismatch for {pid}")
                continue
            for field in visible_page_fields(item):
                visible_raw_by_page.setdefault(pid, []).append(field["text"])
                text = visible_text(field["text"])
                if not text:
                    continue
                key = (pid, field["placement"], text)
                if key in seen_fields:
                    continue
                seen_fields.add(key)
                for rule in ruleset:
                    matches = list(rule.pattern.finditer(text))
                    if not matches:
                        continue
                    supported = bool(rule.evidence_ok(facts, text))
                    found.append(
                        {
                            "category": rule.category,
                            "page_id": pid,
                            "slug": slug,
                            "page_type": allowed[pid]["page_type"],
                            "intended_status": allowed[pid]["intended_status"],
                            "exact_claim": text,
                            "matched_text": " | ".join(m.group(0) for m in matches),
                            "placement": field["placement"],
                            "widget_type": field["widget_type"],
                            "evidence_citation": rule.citation if supported else "NONE — " + rule.citation,
                            "evidence_status": "SUPPORTED" if supported else "UNSUPPORTED",
                            "required_disposition": (
                                "retain; evidence condition satisfied" if supported else rule.disposition
                            ),
                            "blocks_staging": not supported,
                            "blocks_publication": not supported,
                        }
                    )
            for widget in claim_widgets(item):
                reviews = facts.get("reviews", {})
                supported = nonempty_verified(reviews) and reviews.get("permission_to_publish") is True
                found.append(
                    {
                        "category": "review_rating_testimonial_widget",
                        "page_id": pid,
                        "slug": slug,
                        "page_type": allowed[pid]["page_type"],
                        "intended_status": allowed[pid]["intended_status"],
                        "exact_claim": widget["exact_claim"],
                        "matched_text": widget["widget_type"],
                        "placement": widget["placement"],
                        "widget_type": widget["widget_type"],
                        "evidence_citation": (
                            "data/verified-facts.yml reviews verified and publishable"
                            if supported
                            else "NONE — reviews unverified; permission_to_publish:false"
                        ),
                        "evidence_status": "SUPPORTED" if supported else "UNSUPPORTED",
                        "required_disposition": (
                            "retain; evidence condition satisfied"
                            if supported
                            else "remove claim-bearing widget"
                        ),
                        "blocks_staging": not supported,
                        "blocks_publication": not supported,
                    }
                )
    return found, errors, visible_raw_by_page


def add_band_b_adjacencies(
    found: list[dict],
    visible_raw_by_page: dict[int, list[str]],
    allowed: dict[int, dict],
    csv_path: Path,
) -> list[str]:
    errors: list[str] = []
    with csv_path.open("r", encoding="utf-8-sig", errors="strict", newline="") as handle:
        cards = [
            row
            for row in csv.DictReader(handle)
            if (row.get("local_work_card") or "").strip().lower() == "yes"
            and (row.get("local_work_marker") or "").strip()
        ]
    for row in cards:
        pid = int(row["post_id"])
        if pid not in allowed:
            errors.append(f"Band B local-project card is not allowlisted: {pid}")
            continue
        marker = row["local_work_marker"]
        transformed_marker = marker.replace("CoreX", "Structure Co")
        visible_blob = "\n".join(visible_raw_by_page.get(pid, []))
        if marker in visible_blob:
            actual_marker = marker
        elif transformed_marker in visible_blob:
            actual_marker = transformed_marker
        else:
            continue
        found.append(
            {
                "category": "band_b_real_photo_pending_card",
                "page_id": pid,
                "slug": row["slug"],
                "page_type": allowed[pid]["page_type"],
                "intended_status": allowed[pid]["intended_status"],
                "exact_claim": actual_marker,
                "matched_text": actual_marker,
                "placement": (
                    f"adjacent to attachment {row['attachment_id']}; image widget "
                    f"{row['widget_id']}; context {row['nearest_context_id']}"
                ),
                "widget_type": row["widget_type"],
                "evidence_citation": "NONE — DECISION-06 D32 and Report 45",
                "evidence_status": "UNSUPPORTED",
                "required_disposition": "remove with the evidential local-work module",
                "blocks_staging": True,
                "blocks_publication": True,
            }
        )
    return errors


def occurrence_key(row: dict) -> tuple:
    return (
        row["category"],
        int(row["page_id"]),
        row["placement"],
        row["exact_claim"],
    )
