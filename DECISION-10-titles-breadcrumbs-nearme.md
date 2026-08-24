# DECISION-10 — titles, breadcrumbs and near-me targeting

Date: 24 August 2026 (Australia/Sydney).
Origin: owner instruction issued in session, 24 August 2026, in response to the three blocking
questions raised against the supplied meta titles / breadcrumbs / near-me targeting spec.
Status: **current owner decision.** Read-only once confirmed.

Decisions D42–D44, plus the revision D42-R1. Numbering continues from DECISION-09 (D39–D41).

**D42 is superseded by D42-R1 (24 August 2026).** It is retained below unedited so the
reversal has something to cite; read D42-R1 for the current position.

The supplied spec is the authority for titles, breadcrumbs, indexation, schema and near-me
targeting **except** where a clause below amends it. Where the spec and this file disagree,
this file governs. Where the spec and an earlier decision record disagree and this file is
silent, the earlier decision record governs.

---

## D42 — The (03) telephone number is retained — **SUPERSEDED by D42-R1**

The spec, §7.3 and §9 item 1, requires an NSW `02` number sitewide and treats the current
number as the blocker for all other work.

`data/verified-facts.yml` → `contact.phone` records `(03) 4328 3392` as owner-attested,
`verified: true`, `ownership_proven: true`, `routing_proven: true`, with the standing note
"the (03) area code is retained exactly as supplied". No `02` number exists anywhere in the
repository; `suburbs.json` → `site.phone_e164` is the unfilled placeholder `[[TWILIO_E164]]`.

**Decision:** keep `(03) 4328 3392` exactly as supplied, sitewide. §7.3's phone requirement
is overridden. The geographic contradiction the spec identifies is real and is accepted as a
known cost, not resolved.

Consequences:

1. §8's "no `(03)` or `+61 3` string in any output file" is **retired**, with this citation,
   in `scripts/57-seo-spec-gate.py`. It is not deleted and not silently relaxed.
2. No `telephone` property is emitted in any schema node, so no structured-data claim
   contradicts the `areaServed` values.
3. CLAUDE.md §3 hard stop 6 continues to apply. No NSW number may be inferred, researched or
   carried from another source. If the owner supplies one, D42 is superseded by a new record.

## D42-R1 — Reversal: the NSW number is required, and the build fails without it

Date: 24 August 2026 (Australia/Sydney). Origin: owner instruction issued in session.
**Supersedes D42 in full.** The spec's §7.3 and §9 item 1 are restored to force.

D42 reasoned from ownership. Ownership was never the issue: `ownership_proven: true` and
`routing_proven: true` say the owner controls the number, not that the number belongs on
this site. The defect is a **Victorian area code standing as the contact point on a site
whose entire ranking case is proximity to Camden, NSW**. D42's mitigation — omitting
`telephone` from schema — hid the contradiction from parsers while leaving it in the site
header, the footer and every call CTA, where the user and the crawler both still saw it.
That is worse than the untreated defect, because it makes the problem invisible to the
gate while leaving it fully visible to the audience.

**Decision:**

1. **The telephone has exactly one source.** `data/verified-facts.yml` →
   `contact.phone_display` and `contact.phone_e164`, resolved through `lib/seo_spec.py`.
   No template, partial or build script may hardcode a number. `scripts/56-build-static-export.py`
   no longer defines `PHONE` or `PHONE_URI`.

2. **`contact.nsw_number_pending` is an enforcement flag, not a warning.** While it is
   true, `seo_spec.require_deployable_phone()` raises at the top of `main()`, before the
   output directory is touched. There is no partial build and no stale deployable artifact.
   When the flag is false, the same function asserts the shape: `phone_e164` must begin
   `+612` and `phone_display` must match `(02) NNNN NNNN`. The area code is asserted, not
   trusted.

3. **A second line of defence scans the written output.** The templates are parameterised,
   but body copy lifted from the WXR derivatives still carries the superseded number in 66
   places. After writing, the build scans every deployable file for `(03)`, `03 NNNN NNNN`,
   `+61 3` and `tel:+613…`; on a hit it deletes the output directory and exits non-zero.

4. **The §8 phone assertion is un-retired.** `scripts/57-seo-spec-gate.py` carries it as an
   active `assert_`, over every deployable file rather than HTML alone, plus a companion
   assertion that the published number resolves from `verified-facts.yml`.

5. **`telephone` stays out of every schema node until the NSW number lands.** At that point
   it is added to the `Organization` node only — which itself remains blocked by
   DECISION-08 D35 clause 4 until a legal entity is verified.

6. **CLAUDE.md §3 hard stop 6 is unchanged and binding.** No number may be inferred,
   researched, or carried from another source. The build stays failed until the owner
   attests one.

The superseded `contact.phone` block is retained in `verified-facts.yml` marked
`publishable: false` with `superseded_by`, because the frozen WXR-derivative pipeline
(`lib/content_remediation.py`, `scripts/51-evidence-validation.py` and the hash-locked
`build/46-active-main-import.xml`) was generated against that attestation and still
validates against it. Re-parameterising that pipeline would regenerate a hash-locked
derivative and is out of scope here.

## D43 — Spec titles verbatim, H1s with the direct-performance claim removed

The spec bans "enquiries" and "coordination" from titles (§1) and sets every H1 to
`Concreters in {Suburb}` (§2–§4). DECISION-09 D39 and `verified-facts.yml` →
`operating_model` record that Structure Co coordinates independent providers, does not itself
perform regulated concreting work, and holds no verified NSW Fair Trading licence.

**Decision:** apply the spec's title tags **verbatim** — they read as a market and category
claim, which is accurate. Write H1s that carry the same subject without asserting that
Structure Co performs the work:

| Page type | Spec H1 | H1 as built |
|---|---|---|
| Homepage | `Concreters in Camden, NSW` | `Concreting in Camden, NSW` |
| Suburb | `Concreters in {Suburb}` | `Concreting in {Suburb}` |
| Areas hub | `Suburbs We Concrete In` | `Areas We Service` |
| Services hub | `Our Concreting Services` | `Concreting Services` |
| Contact | `Get a Concreting Quote in Camden` | `Start a Concreting Quote in Camden` |
| Service pages | as §3 | as §3, unchanged |

The independent-provider disclosure stays in body copy, the footer and the enquiry form. D39's
prohibition on unsupported technical and licensing claims is unaffected.

Two title tags are applied verbatim under this clause and are flagged as the thinnest fit:

- `Free Concreting Quote | Camden & South West Sydney` — Structure Co coordinates the quote,
  it does not issue it. The page body says so.
- `Shed & Garage Slabs Camden | Thickness, Mesh & Cost` — the page publishes no thickness,
  mesh or cost figure, because D39 and `pricing.per_m2_ranges` prohibit it. The title promises
  content the page cannot carry.

Both should be revisited when the owner reviews commercial wording.

## D44 — All 54 non-Tier-1 suburb pages are noindex,follow

`suburbs.json` carries 16 suburb records. The build ships 60 suburb pages: 45 have no spec
record, and `camden` correctly has no page (§2 folds it into the homepage). The spec's
checklist item "exactly 6 suburb pages are `index,follow`, the other 10 are `noindex,follow`"
cannot hold against 60 pages.

**Decision:** keep all 60 suburb pages published and crawlable. Exactly the 6 Tier 1 pages are
`index,follow`. The other 54 — 9 Tier 2/3 spec suburbs plus the 45 out-of-scope suburbs — are
`noindex,follow`. Nothing is deleted; the internal link graph is preserved intact.

This is compatible with DECISION-09 D41 ("attempt to rebuild all 76 active pages"): the pages
exist and are built, they are simply not offered to the index.

The 45 out-of-scope pages carry no `suburbs.json` record, so they receive no near-me FAQ, no
`Service` node and no §5.4 service-in-suburb block. Emitting those from no data would be
fabrication. Extending `suburbs.json` to cover them is a separate, owner-scoped content job.

---

## Implementation contract

- Resolution layer: `lib/seo_spec.py`.
- Emitter: `scripts/56-build-static-export.py`.
- Assertions: `scripts/57-seo-spec-gate.py` — §6.5 and §8 as build gates. Retired and blocked
  assertions name their authority inline and are reported, never removed.
- Conflict register: `reports/57-spec-conflicts.md`.
- Checklist run: `reports/57-titles-breadcrumbs-nearme-audit.md`.

This decision authorises local source, script, report and build-output changes only. It does
not authorise edits to immutable artifacts or existing governing documents, production
deployment, DNS or indexability changes on a live host, live enquiries, or remote Git
operations.
