"""Reproducible identity, claims and Liverpool content remediation.

The immutable WXR is never edited.  This module operates only on in-memory
trees owned by the derivative generator and returns an occurrence-level audit
record for every legacy and newly detected marketing claim.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from lib.claim_scan import (
    add_band_b_adjacencies,
    additional_rules,
    all_rules,
    legacy_rules,
    occurrence_key,
    scan_claims,
    visible_text,
)
from lib.preimport_safety import CONTENT, items, metas, post_id, post_slug, post_type, visible_page_fields


OWNER_AUTHORITY = "owner attestation and remediation authority, 21 August 2026"
PUBLIC_LABEL = "Structure Co Concreters Camden"
PUBLIC_EMAIL = "info@concreterscamden.com.au"
PUBLIC_PHONE = "(03) 4328 3392"
PUBLIC_PHONE_URI = "tel:+61343283392"
ADMIN_ADDRESS = "15 Murray Street, Camden NSW 2570"
ROLE_TEXT = (
    "Structure Co Concreters Camden manages concreting enquiries and coordinates "
    "suitable independent providers. Job-specific quotations, contractual terms, "
    "licensing, insurance and warranty information must be confirmed before work begins."
)
NO_CONTRACT_TEXT = "Submitting an enquiry does not create a construction contract."
OFFICE_TEXT = (
    "Administrative correspondence office — not open to customers or visitors: "
    f"{ADMIN_ADDRESS}"
)

FORMS_URL = "https://www.liverpool.nsw.gov.au/council/Fees-Forms-Policies-and-Enforcement/forms"
PDF_URL = (
    "https://www.liverpool.nsw.gov.au/__data/assets/pdf_file/0003/286329/"
    "VEHICULAR-CROSSING-APPLICATION-FORM-March-2026v1.pdf"
)
PORTAL_URL = "https://mycouncil.liverpool.nsw.gov.au/ePathway/Production/Web/Default.aspx"
LIVERPOOL_SLUGS = {
    "concreters-leppington",
    "concreters-austral",
    "concreters-edmondson-park",
    "concreters-bringelly",
}

LIVERPOOL_BLOCKS = (
    (
        "Liverpool City Council vehicle crossings are applied for under section 138 of the "
        "Roads Act 1993. The property owner is responsible for the construction, maintenance "
        "and repair costs. Council requires the owner to ensure the contractor is licensed "
        "and has current public-liability cover of at least $10 million. The proposed surface "
        "must be plain concrete. Use Council's current forms page and online application portal; "
        "fees are assessed under Council's current schedule rather than stated here. Before "
        "relying on these requirements, confirm with Council that the March 2026 form and fee "
        "schedule are still current for the application. "
        f'<a href="{FORMS_URL}">Council forms</a> · '
        f'<a href="{PORTAL_URL}">online application portal</a>.'
    ),
    (
        "The March 2026 Liverpool specification requires concrete with a minimum strength at "
        "28 days of 25 MPa for residential driveways and 32 MPa for medium-density, commercial "
        "and industrial driveways. It requires at least 50 mm of compacted DGS20 bedding for "
        "the crossing and at least 100 mm of compacted DGS20 bedding where kerb, gutter or a "
        "layback is constructed. "
        f'<a href="{PDF_URL}">March 2026 Vehicular Crossing Application and Specifications</a>.'
    ),
    (
        "Construction must follow Liverpool City Council drawing R25 and any site-specific "
        "direction from Council's crossing inspector. Applicable utility clearances and "
        "approvals must be resolved, including the form's requirements for electricity assets, "
        "communications pits, Sydney Water assets, stormwater connections, drainage structures, "
        "street trees and pram ramps. Completed formwork, reinforcement, jointing, base material, "
        "barricades and signage must be inspected, and Council approval must be obtained before "
        "concrete is poured. The Council application number is required when booking the "
        "inspection. Council assesses each application and site; approval and any site-specific "
        "requirements must be confirmed before work. This is a Council process; it does not state "
        "that Structure Co holds the contractor licence or insurance. "
        f'<a href="{PDF_URL}">Current Council specification</a>.'
    ),
)


def _as_editor(text: str) -> str:
    return f"&lt;p&gt;{text}&lt;/p&gt;"


def _field_map(tree: object) -> dict[tuple[int, str], str]:
    result: dict[tuple[int, str], str] = {}
    for item in items(tree):
        if post_type(item) != "page":
            continue
        pid = post_id(item)
        for field in visible_page_fields(item):
            result[(pid, field["placement"])] = field["text"]
    return result


def _liverpool_block_for_path(path: str) -> str:
    match = re.search(r"\$\[13\]\.elements\[2\]\.elements\[(\d)\]", path)
    if not match:
        raise AssertionError(f"Liverpool evidence placement is not one of the three recorded cards: {path}")
    index = int(match.group(1))
    if index not in (0, 1, 2):
        raise AssertionError(f"Liverpool evidence card index is invalid: {path}")
    return _as_editor(LIVERPOOL_BLOCKS[index])


def _rewrite_value(slug: str, path: str, key: str, value: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    original = value

    # Attested contact replacement applies to visible labels and link settings.
    value, n = re.subn(r"03 4517 6915", PUBLIC_PHONE, value, flags=re.I)
    if n:
        reasons.append("attested telephone applied")
    value, n = re.subn(r"tel:\+61345176915", PUBLIC_PHONE_URI, value, flags=re.I)
    if n:
        reasons.append("attested telephone URI applied")

    exact = value.strip()
    displayed = visible_text(value)
    if displayed == "Get Your FREE Quote Today":
        value = "Submit a concreting enquiry"
        reasons.append("unsupported free-quote CTA neutralised")
    elif displayed == "Our Services":
        value = "Concreting enquiry types"
        reasons.append("direct service-ownership heading neutralised")
    elif re.fullmatch(r"Why (?:[A-Za-z -]+ )?customers choose us", displayed, re.I) or displayed.upper() == "WHY CUSTOMERS CHOOSE US":
        value = "How enquiry coordination works"
        reasons.append("unsupported customer social-proof heading neutralised")
    elif displayed == "Areas covered":
        value = "Enquiry information"
        reasons.append("unverified service-area heading neutralised")
    elif re.fullmatch(r"AREAS WE COVER AROUND .+", displayed, re.I):
        value = "Nearby suburb information"
        reasons.append("unverified service-area heading neutralised")
    elif displayed == "Concrete service areas":
        value = "Suburb information"
        reasons.append("unverified service-area heading neutralised")
    elif displayed == "Concrete services across Camden and South West Sydney":
        value = "Concreting enquiry types"
        reasons.append("unverified local service heading neutralised")
    elif displayed in {"How Structure Co scopes concrete work", f"Why customers use {PUBLIC_LABEL}"}:
        value = "How enquiry coordination works"
        reasons.append("direct operator/social-proof heading neutralised")
    elif displayed == "Local Work Completed":
        value = ""
        reasons.append("unsupported completed-local-work heading removed")
    elif re.fullmatch(r"Fixed-Price On-Site Quotes?.*", displayed, re.I):
        value = "Job-specific quotations"
        reasons.append("fixed-price/on-site quotation promise neutralised")
    elif re.fullmatch(r"Licensed\s*&\s*Insured.*", displayed, re.I):
        value = "Independent provider credentials"
        reasons.append("Structure Co licence/insurance implication neutralised")
    elif displayed == "NSW licence [[NSW_LICENCE_NO]], public liability and HBCF where required.":
        value = "Licensing and insurance must be confirmed for the independent provider before work begins."
        reasons.append("unsupported credential placeholder neutralised")
    elif displayed == "Written workmanship guarantee on every job.":
        value = "Provider-specific contract terms must be confirmed before work begins."
        reasons.append("unsupported workmanship guarantee neutralised")
    elif displayed == "We come to you, measure the job on site, and price it before we start.":
        value = f"{NO_CONTRACT_TEXT} Any site visit, quotation and terms must be agreed with the independent provider."
        reasons.append("direct on-site quotation promise neutralised")
    elif displayed == "[[PLACEHOLDER: verified Structure Co ABN]]":
        value = PUBLIC_EMAIL
        reasons.append("ABN placeholder removed; attested public email used")
    elif displayed == "[[PLACEHOLDER: verified Structure Co business address]]":
        value = OFFICE_TEXT
        reasons.append("attested administrative-office treatment applied")
    elif re.fullmatch(r"Mon-Fri 9:00AM - 5:00PM", displayed, re.I):
        value = f"Telephone: {PUBLIC_PHONE}"
        reasons.append("unsupported opening hours removed")

    # False-fidelity and invented job records are removed as complete fields.
    plain = re.sub(r"<[^>]+>", " ", value.replace("&lt;", "<").replace("&gt;", ">"))
    if re.search(r"verified project record says", plain, re.I):
        if slug in LIVERPOOL_SLUGS:
            value = _liverpool_block_for_path(path)
            reasons.append("false project record replaced with current official Liverpool evidence")
        else:
            value = ""
            reasons.append("false verified-project construction removed")
    elif re.search(r"The researched [^.]{0,80} job record contains", plain, re.I):
        value = ""
        reasons.append("invented researched-job-record construction removed")
    elif re.search(r"The researched ground note", plain, re.I):
        value = ""
        reasons.append("unsupported researched-ground-note construction removed")

    if re.search(r"verified local job mix", displayed, re.I):
        suburb = slug.removeprefix("concreters-").replace("-", " ").title()
        value = f"Concreting enquiry information for {suburb}."
        reasons.append("unsupported verified-local-job-mix framing removed")
    elif re.search(r"verified local distinction", displayed, re.I):
        value = ""
        reasons.append("unsupported verified-local-distinction field removed")
    elif re.search(r"verified approval (?:record|path)", displayed, re.I):
        value = ""
        reasons.append("unsupported verified-approval field removed")
    elif re.search(r"verified neighbouring service links", displayed, re.I):
        value = ""
        reasons.append("unsupported verified-service-area field removed")
    elif re.search(r"using the verified (?:Camden|Liverpool)", displayed, re.I):
        value = (
            "Concreting information only. Council requirements must be checked for the "
            "specific property and proposed work."
        )
        reasons.append("unsupported verified-council meta claim removed")
    elif re.search(r"verified at the work area", displayed, re.I):
        value = _as_editor("Site conditions must be checked for the specific work area by the independent provider.")
        reasons.append("direct-work verification implication neutralised")

    # Exact operating-model and utility-page surfaces.
    if slug == "homepage":
        if "provides on-site scopes for driveways" in displayed:
            value = _as_editor(ROLE_TEXT) if "&lt;p" in value else ROLE_TEXT
            reasons.append("homepage direct-contractor claim replaced with authorised role disclosure")
        elif displayed.startswith("Tier 1 service areas are"):
            value = _as_editor(
                "These suburb pages provide location-specific information only. Availability of a suitable independent provider must be confirmed for each enquiry."
            )
            reasons.append("homepage service-area claim neutralised")
        elif "service range covers" in displayed.lower():
            value = re.sub(r"The service range covers", "Enquiries may concern", value, flags=re.I)
            reasons.append("direct service-range presentation neutralised")
        elif key == "rank_math_description" and "scopes driveways" in value:
            value = ROLE_TEXT
            reasons.append("homepage meta direct-contractor claim neutralised")
        elif exact == "Concreters Camden | Driveways, Slabs & Local Concrete":
            value = "Concreters Camden | Concrete Enquiries"
            reasons.append("unsupported local-contractor meta wording neutralised")

    if slug in {"contact", "quote", "about", "gallery"}:
        if re.search(r" details$", displayed, re.I):
            value = NO_CONTRACT_TEXT
            reasons.append("form-adjacent no-contract disclosure applied")
        if slug == "contact":
            if "Contact Structure Co Concreters Camden about" in value:
                value = _as_editor(
                    f"{ROLE_TEXT} Contact {PUBLIC_EMAIL} or call {PUBLIC_PHONE}. {OFFICE_TEXT}."
                )
                reasons.append("contact intro replaced with role and attested contact facts")
            elif "Call (03) 4328 3392 or provide the site address" in value:
                value = _as_editor(
                    f"Call {PUBLIC_PHONE} or email {PUBLIC_EMAIL}. {OFFICE_TEXT}. {NO_CONTRACT_TEXT}"
                )
                reasons.append("contact instructions and office treatment applied")
            elif key == "rank_math_description" and "for an on-site project" in value:
                value = (
                    f"Contact {PUBLIC_LABEL} at {PUBLIC_EMAIL} or {PUBLIC_PHONE} to submit "
                    "a concreting enquiry. Submitting an enquiry does not create a construction contract."
                )
                reasons.append("contact meta project/quotation implication neutralised")
        elif slug == "quote":
            if displayed == "Request a Concrete Quote":
                value = "Submit a Concreting Enquiry"
                reasons.append("quotation promise changed to enquiry")
            elif "Request an on-site concrete quote" in value:
                value = _as_editor(
                    f"Submit a concreting enquiry with the property address, proposed use, approximate dimensions, access and preferred finish. {NO_CONTRACT_TEXT} {ROLE_TEXT}"
                )
                reasons.append("on-site quote promise replaced with non-contractual enquiry wording")
            elif "A price range is not invented" in value:
                value = _as_editor(
                    "A suitable independent provider must confirm any site visit, quotation, inclusions and turnaround for the specific job."
                )
                reasons.append("quotation placeholder replaced with provider-specific confirmation")
            elif key == "rank_math_description" and "on-site project scope" in value:
                value = f"Submit a concreting enquiry to {PUBLIC_LABEL}. Submitting an enquiry does not create a construction contract."
                reasons.append("quote meta promise neutralised")
            elif key == "rank_math_title" and value.startswith("Request a Concrete Quote"):
                value = value.replace("Request a Concrete Quote", "Submit a Concreting Enquiry", 1)
                reasons.append("quote meta title neutralised")
            elif key == "rank_math_breadcrumb_title" and exact == "Request a Concrete Quote":
                value = "Submit a Concreting Enquiry"
                reasons.append("quote breadcrumb neutralised")
            elif "Request a Concrete Quote" in displayed:
                value = value.replace("Request a Concrete Quote", "concreting enquiry")
                reasons.append("residual quotation-promise wording neutralised")
        elif slug == "about":
            if "scopes concrete work around the actual site" in value or "No licence, completed-project count or review claim" in value:
                value = _as_editor(ROLE_TEXT)
                reasons.append("about direct-contractor/credential placeholder replaced with role disclosure")
            elif "The current service scope is listed" in value:
                value = _as_editor("Concreting enquiry types are listed on the Camden homepage.")
                reasons.append("about service-scope claim neutralised")
            elif key == "rank_math_description" and "on-site project" in value:
                value = f"About {PUBLIC_LABEL}. {ROLE_TEXT}"
                reasons.append("about meta direct-project implication neutralised")
        elif slug == "gallery":
            if displayed == "Camden Concrete Project Gallery":
                value = "Project Gallery — Deferred"
                reasons.append("gallery visibly marked deferred")
            elif "reserved for verified Structure Co projects completed" in value:
                value = _as_editor(
                    "This gallery is deferred until a genuine, permission-backed project library exists. No project photographs are currently presented as Structure Co work."
                )
                reasons.append("gallery completed-project implication removed")
            elif key == "rank_math_description" and "on-site project" in value:
                value = "The project gallery is deferred until a genuine, permission-backed project library exists."
                reasons.append("gallery meta project implication removed")
            elif key in {"rank_math_title", "rank_math_breadcrumb_title"} and "Camden Concrete Project Gallery" in value:
                value = value.replace("Camden Concrete Project Gallery", "Project Gallery — Deferred")
                reasons.append("gallery meta marked deferred")

    # Current researched-page claim register fields.
    if re.search(r"We work across .+ surrounding", value, re.I):
        value = _as_editor(
            "These links provide nearby suburb information only. Availability of a suitable independent provider must be confirmed for each enquiry."
        )
        reasons.append("unverified service-area body claim neutralised")
    if slug == "concreters-oran-park":
        if "most of our work starts" in displayed or "Whatever the pour, we match you" in displayed:
            value = _as_editor(ROLE_TEXT) if "&lt;p" in value else ROLE_TEXT
            reasons.append("Oran Park direct-contractor claim replaced with role disclosure")
        elif displayed == "How we prepare the ground in Oran Park":
            value = "Site information to confirm with an independent provider"
            reasons.append("direct preparation heading neutralised")
        elif "On a handover lot the driveway area usually still has builder's spoil" in displayed:
            value = ""
            reasons.append("unsupported direct-work and invented job-record field removed")
        elif "Any driveway that crosses council land needs Camden Council approval" in displayed:
            value = ""
            reasons.append("unattested Camden specification and direct application claim removed")
        elif "It comes down to area, finish and access" in displayed:
            value = _as_editor(
                "Job-specific quotations, inclusions and terms must be confirmed with the independent provider before work begins."
            )
            reasons.append("unsupported price range and fixed-price promise removed")

    if key == "rank_math_description" and re.search(r"Request an on-site quote", value, re.I):
        suburb = slug.removeprefix("concreters-").replace("-", " ").title()
        value = (
            f"Concreting information for {suburb}. Structure Co manages enquiries and coordinates "
            "suitable independent providers; job-specific terms must be confirmed before work begins."
        )
        reasons.append("on-site quote/local approval meta promise neutralised")

    if original == value:
        return value, []
    return value, reasons or ["attested remediation applied"]


def _transform_tree(tree: object) -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    counters: Counter[str] = Counter()
    for item in items(tree):
        if post_type(item) != "page":
            continue
        pid = post_id(item)
        slug = post_slug(item)
        title = item.find("title")
        if title is not None and title.text:
            new, reasons = _rewrite_value(slug, "item.title", "item.title", title.text)
            if reasons:
                changes.append({"page_id": pid, "slug": slug, "placement": "item.title", "before": title.text, "after": new, "reasons": reasons})
                title.text = new
                counters.update(reasons)
        content = item.find(CONTENT + "encoded")
        if content is not None and content.text:
            if slug == "privacy-policy":
                before = content.text
                content.text = privacy_content()
                changes.append({"page_id": pid, "slug": slug, "placement": "post_content", "before": before, "after": content.text, "reasons": ["privacy policy rebuilt from attested facts; genuine blockers retained"]})
                counters["privacy policy rebuilt from attested facts; genuine blockers retained"] += 1
            else:
                new, reasons = _rewrite_value(slug, "post_content", "post_content", content.text)
                if reasons:
                    changes.append({"page_id": pid, "slug": slug, "placement": "post_content", "before": content.text, "after": new, "reasons": reasons})
                    content.text = new
                    counters.update(reasons)
        for _pm, meta_key, value_node in metas(item):
            value = value_node.text or ""
            if meta_key == "_elementor_data" and value:
                parsed = json.loads(value)

                def walk(node: Any, path: str = "$") -> None:
                    if isinstance(node, dict):
                        for child_key, child in list(node.items()):
                            child_path = f"{path}.{child_key}"
                            if isinstance(child, str):
                                new, reasons = _rewrite_value(slug, child_path, child_key, child)
                                if reasons:
                                    changes.append({"page_id": pid, "slug": slug, "placement": f"_elementor_data:{child_path}", "before": child, "after": new, "reasons": reasons})
                                    node[child_key] = new
                                    counters.update(reasons)
                            elif isinstance(child, (dict, list)):
                                walk(child, child_path)
                    elif isinstance(node, list):
                        for index, child in enumerate(node):
                            walk(child, f"{path}[{index}]")

                walk(parsed)
                value_node.text = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
            elif meta_key in {"rank_math_title", "rank_math_description", "rank_math_breadcrumb_title"}:
                new, reasons = _rewrite_value(slug, f"postmeta:{meta_key}", meta_key, value)
                if reasons:
                    changes.append({"page_id": pid, "slug": slug, "placement": f"postmeta:{meta_key}", "before": value, "after": new, "reasons": reasons})
                    value_node.text = new
                    counters.update(reasons)
    return changes, dict(sorted(counters.items()))


def privacy_content() -> str:
    return f"""<h1>Privacy Policy</h1>
<h2>What this policy covers</h2>
<p>This policy explains how personal information submitted through this website is handled. The public site-operator label is {PUBLIC_LABEL}. The accountable legal entity remains [[PLACEHOLDER: accountable legal entity for privacy obligations]] and this policy must not be published until that entity is identified.</p>
<h2>Operating model</h2>
<p>{ROLE_TEXT} {NO_CONTRACT_TEXT}</p>
<h2>What is collected</h2>
<p>The planned enquiry form may collect a name, phone number, suburb, requested service, optional email address, approximate job size and a free-text message. It must not collect payment details.</p>
<h2>Why it is collected and disclosed</h2>
<p>Information is used to respond to the enquiry and, with the submitter's consent, may be shared with a suitable independent provider so that the provider can assess the enquiry. It is not sold, rented or disclosed for third-party marketing.</p>
<h2>Delivery, storage and retention</h2>
<p>Form submissions are to be delivered to {PUBLIC_EMAIL}. [[VERIFY: form delivery, authenticated sending domain, database storage and access controls before publication.]] Enquiry records are retained for [[PLACEHOLDER: owner-decided retention period]] and then deleted unless a lawful obligation requires otherwise.</p>
<h2>Consent and contracts</h2>
<p>The form must require consent to contact the submitter, store the supplied information and share it with a suitable independent provider for the enquiry. Consent is not pre-ticked and may be withdrawn. {NO_CONTRACT_TEXT}</p>
<h2>Access, correction and complaints</h2>
<p>Requests to access, correct or delete personal information may be sent to {PUBLIC_EMAIL} or made by telephone on {PUBLIC_PHONE}. Postal correspondence may be sent to {ADMIN_ADDRESS}. This is an administrative correspondence office and is not open to customers or visitors. We will respond within a reasonable period. Complaints may also be made to the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au/">oaic.gov.au</a>.</p>
<h2>Cookies and analytics</h2>
<p>[[VERIFY: confirm which analytics or tracking scripts are installed before publication and describe them here, or state that none are present.]]</p>
<h2>Changes</h2>
<p>If this policy changes, the revised version will be published on this page. Effective date: [[PLACEHOLDER: publication date]].</p>"""


def build_disposition_register(
    pre_media_trees: list[object],
    pre_claim_trees: list[object],
    final_trees: list[object],
    allowed: dict[int, dict],
    facts: dict,
    testimonial_csv: Path,
    changes: list[dict],
) -> dict:
    legacy, errors, legacy_visible = scan_claims(pre_media_trees, allowed, facts, legacy_rules())
    legacy_text_count = len(legacy)
    legacy_text_unsupported = sum(row["evidence_status"] == "UNSUPPORTED" for row in legacy)
    errors += add_band_b_adjacencies(legacy, legacy_visible, allowed, testimonial_csv)
    pre_legacy, pre_errors, _ = scan_claims(pre_claim_trees, allowed, facts, legacy_rules())
    errors += pre_errors
    pre_additional, add_errors, _ = scan_claims(pre_claim_trees, allowed, facts, additional_rules())
    errors += add_errors
    final, final_errors, _ = scan_claims(final_trees, allowed, facts, all_rules())
    errors += final_errors

    legacy_unsupported = sum(row["evidence_status"] == "UNSUPPORTED" for row in legacy)
    pre_legacy_unsupported = sum(row["evidence_status"] == "UNSUPPORTED" for row in pre_legacy)
    if (legacy_text_count, legacy_text_unsupported) != (228, 224):
        raise AssertionError(
            "legacy text/widget baseline changed: "
            f"{legacy_text_count}/{legacy_text_unsupported} != 228/224"
        )
    if (len(pre_legacy), pre_legacy_unsupported) != (135, 131):
        raise AssertionError(
            f"post-media legacy baseline changed: {len(pre_legacy)}/{pre_legacy_unsupported} != 135/131"
        )
    if len(legacy) != 232 or legacy_unsupported != 228:
        raise AssertionError(
            "Band B adjacency reconciliation did not produce 232/228: "
            f"{len(legacy)}/{legacy_unsupported}"
        )

    final_unsupported = [row for row in final if row["evidence_status"] == "UNSUPPORTED"]
    if final_unsupported:
        sample = [
            (r["slug"], r["category"], r["placement"], r["exact_claim"][:180])
            for r in final_unsupported[:50]
        ]
        raise AssertionError(f"unsupported claims remain after remediation: {sample}")
    if errors:
        raise AssertionError("claim scan errors: " + "; ".join(errors))

    def field_occurrence_key(row: dict) -> tuple:
        return (row["category"], int(row["page_id"]), row["placement"])

    pre_legacy_keys = {field_occurrence_key(row) for row in pre_legacy}
    pre_legacy_content_keys = {
        (row["category"], int(row["page_id"]), row["exact_claim"])
        for row in pre_legacy
    }
    pre_additional_keys = {occurrence_key(row) for row in pre_additional}
    final_keys = {occurrence_key(row) for row in final}
    final_fields: dict[tuple[int, str], str] = {}
    for tree in final_trees:
        final_fields.update(_field_map(tree))

    changed_fields = {(int(row["page_id"]), row["placement"]): row for row in changes}

    def disposition(row: dict, present_before_claims: bool) -> dict:
        key = occurrence_key(row)
        field_key = (int(row["page_id"]), row["placement"])
        if not present_before_claims:
            action = "REMOVED_BY_REPORT_50_MEDIA_AND_D32"
            final_text = ""
            authority = "DECISION-06 D32; owner-approved Report 49/Report 50 media plan"
        elif key in final_keys:
            action = "RETAINED_WITH_EVIDENCE"
            final_text = row["exact_claim"]
            authority = row["evidence_citation"]
        else:
            final_text = final_fields.get(field_key, "")
            change = changed_fields.get(field_key)
            reasons = change["reasons"] if change else []
            if row["slug"] in LIVERPOOL_SLUGS and row["category"] == "false_verified_project_record":
                action = "REPLACED_WITH_OFFICIAL_LIVERPOOL_EVIDENCE"
                authority = f"{PDF_URL}; accessed 2026-08-21"
            elif final_text:
                action = "NEUTRALISED_WITH_ATTESTED_OR_NONCLAIM_WORDING"
                authority = OWNER_AUTHORITY
            else:
                action = "REMOVED_WITHOUT_REPLACEMENT"
                authority = OWNER_AUTHORITY
            if reasons:
                authority += "; " + " | ".join(reasons)
        result = dict(row)
        result.update(
            {
                "final_disposition": action,
                "final_text": final_text,
                "disposition_authority": authority,
                "final_blocks_staging": False,
                "final_blocks_publication": False,
            }
        )
        return result

    legacy_rows = []
    for index, row in enumerate(legacy, 1):
        present = (
            field_occurrence_key(row) in pre_legacy_keys
            or (row["category"], int(row["page_id"]), row["exact_claim"])
            in pre_legacy_content_keys
        )
        out = disposition(row, present)
        out["claim_id"] = f"LEG-{index:04d}"
        legacy_rows.append(out)
    additional_rows = []
    for index, row in enumerate(pre_additional, 1):
        out = disposition(row, occurrence_key(row) in pre_additional_keys)
        out["claim_id"] = f"ADD-{index:04d}"
        additional_rows.append(out)

    for index, row in enumerate(final, 1):
        row["claim_id"] = f"FINAL-{index:04d}"

    return {
        "schema_version": "1.0",
        "generated_by": "scripts/46-architecture-import-gate.py via lib/content_remediation.py",
        "authority": OWNER_AUTHORITY,
        "legacy_reconciliation": {
            "reported_occurrences": 232,
            "reported_unsupported": 228,
            "text_and_widget_occurrences": 228,
            "band_b_adjacencies": 4,
            "unsupported_text_and_widgets": 224,
            "unsupported_band_b_adjacencies": 4,
            "post_report50_occurrences": 135,
            "post_report50_unsupported": 131,
            "arithmetic": "232 = 228 text/widget + 4 Band B adjacency; 228 unsupported = 224 + 4. Report 50 removed 97 occurrences, leaving 135/131 before this pass.",
        },
        "totals": {
            "legacy_occurrences": len(legacy_rows),
            "legacy_unsupported": legacy_unsupported,
            "additional_blind_spot_occurrences": len(additional_rows),
            "final_reader_visible_claim_occurrences": len(final),
            "final_unsupported": 0,
            "content_field_changes": len(changes),
            "legacy_by_final_disposition": dict(Counter(r["final_disposition"] for r in legacy_rows)),
            "additional_by_final_disposition": dict(Counter(r["final_disposition"] for r in additional_rows)),
        },
        "legacy_occurrences": legacy_rows,
        "additional_occurrences": additional_rows,
        "final_occurrences": final,
        "content_changes": changes,
    }


def apply_and_register(
    main_tree: object,
    privacy_tree: object,
    pre_media_main_tree: object,
    allowed: dict[int, dict],
    facts: dict,
    testimonial_csv: Path,
) -> tuple[dict, dict]:
    pre_claim_main = type(main_tree)(main_tree.getroot())
    # The caller passes clones; make exact byte-level clones through serialisation
    # unnecessary by collecting the scan before mutation.
    pre_claim_main_fields = _field_map(main_tree)
    pre_claim_privacy_fields = _field_map(privacy_tree)
    pre_legacy, _, _ = scan_claims([main_tree, privacy_tree], allowed, facts, legacy_rules())
    if len(pre_legacy) != 135:
        raise AssertionError(f"expected 135 post-media legacy claims before transformation, found {len(pre_legacy)}")

    # Deep-copy the pre-claim trees for occurrence reconciliation.
    import copy
    pre_claim_main = type(main_tree)(copy.deepcopy(main_tree.getroot()))
    pre_claim_privacy = type(privacy_tree)(copy.deepcopy(privacy_tree.getroot()))
    pre_media_privacy = type(privacy_tree)(copy.deepcopy(privacy_tree.getroot()))

    main_changes, main_counts = _transform_tree(main_tree)
    privacy_changes, privacy_counts = _transform_tree(privacy_tree)
    changes = main_changes + privacy_changes
    register = build_disposition_register(
        [pre_media_main_tree, pre_media_privacy],
        [pre_claim_main, pre_claim_privacy],
        [main_tree, privacy_tree],
        allowed,
        facts,
        testimonial_csv,
        changes,
    )
    summary = {
        "authority": OWNER_AUTHORITY,
        "content_field_changes": len(changes),
        "main_change_reasons": main_counts,
        "privacy_change_reasons": privacy_counts,
        "legacy_232_dispositions": register["totals"]["legacy_by_final_disposition"],
        "additional_blind_spot_occurrences": register["totals"]["additional_blind_spot_occurrences"],
        "final_claim_occurrences": register["totals"]["final_reader_visible_claim_occurrences"],
        "final_unsupported": 0,
        "phone_text_before_fields": sum("03 4517 6915" in value for value in pre_claim_main_fields.values()),
        "privacy_fields_before": len(pre_claim_privacy_fields),
    }
    return summary, register
