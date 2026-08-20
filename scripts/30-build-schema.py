#!/usr/bin/env python3
"""Fail-closed JSON-LD builder for the 76-page derived import architecture."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.preimport_safety import items, parse_wxr, post_id, post_slug, post_type  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://concreterscamden.com.au"
FACTS = ROOT / "data" / "verified-facts.yml"
ALLOWLIST = ROOT / "build" / "46-active-page-allowlist.json"
MAIN = ROOT / "build" / "46-active-main-import.xml"
PRIVACY = ROOT / "build" / "51-privacy-import.xml"
OUTPUT = ROOT / "build" / "30-schema-output.json"
REFUSALS = ROOT / "reports" / "30-schema-refusals.md"
PLACEHOLDER_TOKENS = ("PLACEHOLDER", "REAL_PHOTO_PENDING", "REQUIRED-RESEARCH", "VERIFY")


def verified(node: object, *, allow_false: bool = False) -> bool:
    if not isinstance(node, dict) or node.get("verified") is not True:
        return False
    value = node.get("value")
    return value is not None if allow_false else bool(value)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    facts = yaml.safe_load(FACTS.read_text(encoding="utf-8", errors="strict"))
    allow = json.loads(ALLOWLIST.read_text(encoding="utf-8", errors="strict"))
    allowed = {int(row["page_id"]): row for row in allow["pages"]}
    if len(allowed) != 76:
        raise AssertionError(f"schema allowlist count {len(allowed)} != 76")

    pages: dict[int, dict] = {}
    for artifact in (MAIN, PRIVACY):
        for item in items(parse_wxr(artifact)):
            if post_type(item) != "page":
                continue
            pid = post_id(item)
            if pid not in allowed:
                raise AssertionError(f"schema encountered non-allowlisted page {pid}:{post_slug(item)}")
            if post_slug(item) != allowed[pid]["slug"]:
                raise AssertionError(f"schema slug mismatch for page {pid}")
            if pid in pages:
                raise AssertionError(f"schema duplicate page {pid}")
            pages[pid] = {
                **allowed[pid],
                "title": (item.findtext("title") or "").strip(),
            }
    if set(pages) != set(allowed):
        raise AssertionError(
            f"schema page parity failure missing={sorted(set(allowed)-set(pages))} "
            f"additional={sorted(set(pages)-set(allowed))}"
        )

    label = facts["legal_entity"]["trading_name"]
    if not verified(label) or label["value"] != "Structure Co Concreters Camden":
        raise AssertionError("verified public site-operator label is absent")
    legal_name_ok = verified(facts["legal_entity"]["legal_name"])
    address_ok = verified(facts["contact"]["street_address"])
    staffed_ok = facts["contact"]["is_staffed"].get("verified") is True and facts["contact"]["is_staffed"].get("value") is True
    visitor_ok = facts["contact"]["open_to_visitors"].get("verified") is True and facts["contact"]["open_to_visitors"].get("value") is True
    customer_premises_ok = facts["contact"]["customer_facing_premises"].get("verified") is True and facts["contact"]["customer_facing_premises"].get("value") is True
    can_organization = legal_name_ok
    can_localbusiness = legal_name_ok and address_ok and staffed_ok and visitor_ok and customer_premises_ok
    if can_localbusiness:
        raise AssertionError("LocalBusiness became emittable despite the owner-attested non-customer office")

    graphs: dict[str, dict] = {}
    refusals: list[dict] = []
    provider_omitted: Counter[str] = Counter()
    service_nodes = 0
    for pid, page in sorted(pages.items()):
        path = page["url"]
        full = SITE.rstrip("/") + path
        nodes: list[dict] = [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "url": f"{SITE}/",
                "name": label["value"],
                "inLanguage": "en-AU",
            },
            {
                "@type": "WebPage",
                "@id": f"{full}#webpage",
                "url": full,
                "name": page["title"],
                "isPartOf": {"@id": f"{SITE}/#website"},
                "inLanguage": "en-AU",
            },
        ]
        if page["page_type"] in {"service", "suburb"}:
            service_nodes += 1
            nodes.append(
                {
                    "@type": "Service",
                    "@id": f"{full}#service",
                    "name": page["title"],
                    "serviceType": "Concreting enquiry coordination",
                }
            )
            provider_omitted[page["page_type"]] += 1
            refusals.append(
                {
                    "node": "Service.provider",
                    "scope": path,
                    "reason": "no verified legal entity or specific contracting provider is authorised",
                    "action": "provider omitted under D2 outcome 3",
                }
            )
        graphs[path] = {"@context": "https://schema.org", "@graph": nodes}

    refusals.insert(0, {
        "node": "Organization",
        "scope": "site-wide",
        "reason": "legal_entity.legal_name remains unverified; the public label is not a legal entity",
        "action": "node omitted; legalName and ABN are not asserted",
    })
    refusals.insert(1, {
        "node": "LocalBusiness / GeneralContractor",
        "scope": "site-wide",
        "reason": "the staffed address is an administrative correspondence office not open to customers or visitors, and legal_name is unverified",
        "action": "node omitted; no storefront, opening hours or customer-facing premises are asserted",
    })

    blob = json.dumps(graphs, ensure_ascii=False)
    forbidden_keys = ("legalName", "taxID", "openingHours", "telephone", "address", "AggregateRating", "award")
    checks = {
        "76 derived graphs": len(graphs) == 76,
        "70 Service nodes": service_nodes == 70,
        "zero Organization": '"@type": "Organization"' not in blob,
        "zero LocalBusiness": "LocalBusiness" not in blob and "GeneralContractor" not in blob,
        "zero Service.provider": '"provider"' not in blob,
        "zero unsupported identity/schema keys": not any(f'"{key}"' in blob for key in forbidden_keys),
        "zero placeholder tokens": not any(token in blob for token in PLACEHOLDER_TOKENS),
    }
    if not all(checks.values()):
        raise AssertionError(f"schema assertions failed: {checks}")

    OUTPUT.write_text(json.dumps(graphs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Stage 30 — schema refusal log", "",
        "Generated by `scripts/30-build-schema.py` from the 76-page derived allowlist.", "",
        "```text",
        f"  pages/graphs                     {len(graphs)}",
        f"  Service nodes                    {service_nodes}",
        "  Organization emitted             NO",
        "  LocalBusiness emitted            NO",
        f"  Service.provider omitted         {sum(provider_omitted.values())}",
        "```", "", "## Refusals", "", "```text",
    ]
    grouped = Counter((row["node"], row["reason"], row["action"]) for row in refusals)
    for (node, reason, action), count in grouped.items():
        lines += [f"REFUSAL — {node}", f"  occurrences  {count}", f"  reason       {reason}", f"  action       {action}", ""]
    lines += ["```", "", "## Gate results", "", "```text"]
    for name, passed in checks.items():
        lines.append(f"  {name:<48} {'PASS' if passed else 'FAIL'}")
    lines += ["```", ""]
    REFUSALS.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"PASS — schema: pages={len(graphs)}, services={service_nodes}, "
        "Organization=NO, LocalBusiness=NO, providers omitted=70"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
