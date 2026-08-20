# DECISION RECORD 04 — scope reduction, service rebuild, image dispositions

Cite in `build/21-spec-ledger.json`. Instruction documents remain read-only.

The coherence scan settles what this build is. The immutable WXR is a sound structure carrying mostly non-writing: 82.4% filler, five clean pages. Structure, page IDs, menus, URL architecture, the 15 researched suburbs, the 35 intersection differentiators and the nine specifications all survive. The copy does not. From here this is a content rebuild on a surviving skeleton, not a repair.

---

## D21 — Withdraw the 35 guides, the 10 cost/comparison pages, and the guide hub

Same disposition as the intersections, for the same reason and for consistency: 45 pages cannot stay in the architecture at a severity that justified withdrawing 35 others.

**DO:**
1. Mark all 35 guides, all 10 cost/comparison pages and the guide hub `WITHDRAWN` in `reports/23-page-readiness-v2.csv`. Excluded at import, **not deleted from the immutable WXR**.
2. The guide hub goes because §4.27 forbids publishing it without its first approved guides, and there are none.
3. Combined architecture: **122 − 46 = 76.** Propagate per the §4.31.7 pattern — ledger, readiness CSV, wave plan, image denominator, preflight, `CONTEXT.md`.
4. Waves 2, 4 and 5 are now empty. State that plainly rather than leaving them populated.
5. Retain every withdrawn page's research inputs as rebuild material, as with `intersection-differentiators.json`. The guide taxonomy in `expansion-300-pages.md` §5 stays valid; only the generated copy is discarded.

**Resulting architecture: 76 pages** — 1 homepage, 4 utility, 10 service, 60 suburb, plus the calculator as a separate build target under §4.31.

**Realistic Wave 1: ~30 pages** — homepage, 4 utility, 10 rewritten service pages, 15 researched suburb pages. The 45 unresearched suburbs remain draft + noindex pending D22.

---

## D22 — The 45 unresearched suburbs: decision deferred, not dropped

They stay in the architecture as draft + noindex. They enter no wave, count toward no live total, and are not rewritten. Revisit once the 30-page core is live and earning impressions. Record as an explicit open scope decision in `CONTEXT.md` so it is not silently resolved by inaction.

---

## D23 — Service page rebuild: the specification matrix comes first

9.6% of service page words survive. All nine specifications survive on all ten pages — and are identical across all ten, which cannot be right. A patio slab and a commercial hardstand do not share thickness and mesh.

**Nothing is written until the matrix exists.** Writing ten pages against one undifferentiated spec set reproduces the original failure in better prose.

**DO:**
1. Produce `data/service-specs.yml` as an **empty required structure**: for each of the ten services — slab thickness, concrete grade, mesh/reinforcement, base preparation, control joint spacing, cure time, fall/drainage, edge treatment, and any service-specific requirement. Every field `verified: false`, each requiring a source or an owner/engineer attestation.
2. **Do not populate it.** Not from the existing pages, not from the other nine services, not from Australian Standards general knowledge. The owner supplies it.
3. Flag every field where a value currently appears on a page but is not attested — those are unattributed specifications now published as fact.
4. `reports/34-service-rebuild-brief.md` per page: surviving real content verbatim, what must be written, target word count, the ≤40% pairwise cap against the other nine rewritten bodies, and the uniqueness and coherence gates the rewritten body must pass.
5. **Do not write copy.** The brief stops at the brief. Authorship is decided separately once the matrix exists.

Your flag about failing uniqueness in the other direction is correct and is why the matrix is prerequisite: ten pages differentiated by real specification differences pass the cap naturally; ten pages differentiated by paraphrase do not.

---

## D24 — AI-generated images

**Attachment 272** (`cropped-ChatGPT-Image-Jul-6-2026-01_52_19-PM.png`, live on 14 pages): **remove.** A generated image presented as photographic evidence on a trades site is the same class of claim as a renamed Melbourne photo. It is not replaced from stock until the pages it sits on are rebuilt.

**159 and 177**: determine whether either is the site mark by inspecting the Elementor kit and Astra theme mods, and report. Do not classify or act. If the logo is AI-generated it joins the three held favicon files under D18 — the site ships without a mark rather than with a generated one asserting a brand identity that has no verified legal entity behind it.

**The 60 naming-convention artefacts**: reverse per D20 — filename, attachment title and per-page alt text as one operation. These are not substitutions and are not treated as such.

**Assume a fourth gap.** Every audit so far has read filenames, titles and alt text. Nothing has examined pixels, and the binaries are not local. Record pixel-level verification as a required step at media intake, not as complete.

---

## D25 — The re-encode driver is now a P0 blocker, not a footprint task

`reencode-images.sh` has never parsed, so no image has ever been stripped or re-encoded. If the 83 binaries arrive and import without a working driver, embedded EXIF — including GPS coordinates from Melbourne job sites and owner/device metadata — publishes to a live website.

**DO:**
1. Promote the corrected driver to a **P0 blocker in `CONTEXT.md`**, alongside the media binaries and the Astra export.
2. Add to `scripts/22-media-audit.py` a **fail-closed EXIF assertion**: zero GPS tags, zero owner/artist/serial fields, zero original-datetime on every file, verified after re-encode and before import.
3. Verify the assertion catches a known-dirty test file before trusting it on the real set.

---

## Owner tasks arising

1. **Service specification matrix** — ten services, nine-plus fields each. Blocks the entire Wave 1 rebuild. Owner-supplied; not inferable.
2. **83 image binaries + Astra export** — unchanged, still P0.
3. **Liverpool City Council crossing specification** — unchanged.
4. **Legal entity, ABN, licence, insurance, staffed address, phone routing** — unchanged; still forces every `Service` node to omit `provider`.
5. **Service page authorship** — decide who writes, under the coherence and uniqueness gates.
6. **Site mark** — commission or supply, pending D24.

Launch state unchanged: index-ready 0, NO-GO.
