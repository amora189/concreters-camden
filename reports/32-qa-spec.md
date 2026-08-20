# GATE 32 — QA specification

Date: 18 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.32; `CONTEXT.md` P1.
Artifacts: this file, `scripts/32-qa-automated.py`.

**NONE OF THIS WAS RUN.** It executes against authoritative staging after Gate 28 returns GO, and its
output feeds the page-by-page release decision. Gate 28 currently returns NO-GO.

---

## Check inventory

```text
  automatable          13
  human-sighted        16
  TOTAL                29

  checks that must pass before ONE page can move to Index-ready: yes    29
```

Every check is per-page. A page passing 28 of 29 is not releasable.

---

## A. Automatable — `scripts/32-qa-automated.py`

Fail-closed, machine-readable JSON output. Runs logged out.

```text
CHECK A1 — HTTP status, logged out
  pass condition   publish pages return 200; draft pages return 404 to a logged-out client
  evidence         status code per URL from a session with no cookies
  why              a draft page reachable logged-out is a leak, not a draft

CHECK A2 — no unexpected redirect
  pass condition   final URL equals the requested URL
  evidence         resolved final_url after redirects

CHECK A3 — canonical matches the served URL
  pass condition   rel=canonical present and byte-equal to the served URL, trailing slash included
  evidence         the canonical href, compared exactly

CHECK A4 — robots directive matches the release plan
  pass condition   the page's meta robots or X-Robots-Tag matches reports/27-wave-plan.md
  evidence         both the meta tag and the header
  why              this is the check that stops a held Tier 1 suburb going indexable by accident

CHECK A5 — exactly one H1
  pass condition   exactly one <h1> in rendered HTML
  evidence         count

CHECK A6 — no heading level skipped
  pass condition   no h(n) followed by h(n+2) or deeper
  evidence         the ordered heading sequence

CHECK A7 — Rank Math title 50-60 characters
  pass condition   50 <= len(title) <= 60, counted on the rendered <title>
  evidence         character count and the exact string
  why              non-ASCII is load-bearing here; the count is over code points,
                   read with errors='strict' (§3.1)

CHECK A8 — meta description 140-160 characters
  pass condition   140 <= len(description) <= 160
  evidence         character count

CHECK A9 — every image resolves
  pass condition   every <img src> returns 200
  evidence         status per image URL
  why              1,183 Elementor image references depend on exact filenames surviving import

CHECK A10 — every internal link resolves
  pass condition   every internal href returns 200, 301 or 302; none 404
  evidence         status per link

CHECK A11 — JSON-LD valid with no dangling @id
  pass condition   every JSON-LD block parses, and every referenced @id is defined
                   in the same graph
  evidence         parse result and dangling-reference count
  why              this is the D2 build-failing check, verified against rendered output
                   rather than against the builder's own output

CHECK A12 — zero evidence markers in rendered HTML
  pass condition   no PLACEHOLDER, REAL_PHOTO_PENDING, REQUIRED-RESEARCH or bare
                   VERIFY string appears in what a visitor sees
  evidence         token counts
  why              170 marker occurrences exist today; every one must be resolved
                   or removed before its page is released

CHECK A13 — Victorian blocklist zero
  pass condition   zero occurrences of all 13 blocklist terms
  evidence         per-term counts
```

### Sitemap consistency — deliberately NOT automated per page

```text
  A sitemap must not exist at all during staging. The Stage 29 mu-plugin disables
  wp_sitemaps outright. Checking a sitemap per page would imply one should exist.
  The correct check is a single site-level assertion that no sitemap is served,
  and it belongs to the launch gate, not to per-page QA.
```

---

## B. Human-sighted — no automated shortcut

§4.32.3 requires these be specified with no automated substitute. Each names what a person must look at
and what constitutes a pass.

```text
CHECK H1 — Camden-site visual approval, desktop
  who      owner or a person who knows the Camden market
  pass     the page looks like a real local business's page, not a template with
           the suburb name swapped
  evidence a sighting, recorded per page. NOT a screenshot diff.

CHECK H2 — Camden-site visual approval, mobile
  pass     as H1, at 375px and 414px widths on a real device

CHECK H3 — responsive behaviour
  pass     no horizontal scroll, no overlapping text, no clipped CTA, at 320,
           375, 768, 1024 and 1440px

CHECK H4 — image appropriateness and provenance
  pass     every image on the page depicts something that is plausibly what the
           surrounding copy says it is
  why      20 images are Victorian photographs renamed to specific NSW places
           (Gate 24). No automated check catches this: the files are valid, the
           filenames are correct, and the alt text agrees with the filename.
           A person who knows Camden must look at them.

CHECK H5 — alt text describes the image, not the slot
  pass     alt text describes what is in the photograph for this page's context
  why      1,112 (image, page) pairs currently share alt text by construction

CHECK H6 — copy reads as written by a person who knows the suburb
  pass     the local detail is specific and correct
  why      45 suburb pages are unresearched shells

CHECK H7 — no sentence asserts verification that has not occurred
  pass     no "reproduced without alteration", "the verified approval path",
           "the verified project record says" over an unfilled value
  why      6 such sentences exist today (reports/23-false-fidelity.md); 2 are
           unfillable and need rewriting regardless of what is supplied

CHECK H8 — accessibility beyond automated checks
  pass     keyboard-only navigation reaches every interactive element in a
           sensible order; focus is visible; the page is usable with a screen
           reader
  why      automated tools catch contrast and alt presence, not whether a
           keyboard user can actually complete an enquiry

CHECK H9 — colour contrast on real content
  pass     WCAG 2.1 AA on actual text over actual backgrounds

CHECK H10 — form delivery confirmation
  pass     a test submission ARRIVES IN THE REAL INBOX
  evidence the received email, not a mail log entry
  why      a form that silently loses enquiries is worse than no form

CHECK H11 — form consent and privacy basis
  pass     consent checkbox is unticked by default, wording is approved, and it
           links to a privacy policy that exists
  why      no privacy policy page exists today (reports/30-forms-spec.md §4)

CHECK H12 — phone number ownership and routing
  pass     calling the number reaches the business
  why      03 4517 6915 carries a Victorian area code on a NSW business and
           appears 120 times in the artifact

CHECK H13 — mobile Core Web Vitals on authoritative staging
  pass     LCP, CLS and INP within thresholds on a throttled mobile profile
           against the real Camden site
  why      the Stage 11-20 environment-level Lighthouse runs are NOT this

CHECK H14 — business facts match reality
  pass     ABN, licence, insurance, address and staffing status as stated match
           what the owner can evidence

CHECK H15 — pricing is defensible
  pass     every price range shown is one the owner would stand behind in writing

CHECK H16 — reviews are real and permitted
  pass     each review is genuine, the reviewer's name appears as they agreed,
           and permission to publish is on record
```

---

## C. What the Stage 11–20 checks are NOT

Stated plainly, per §4.32.3.

```text
  The Stage 11-20 environment-level Lighthouse runs and browser checks verified
  that a WordPress container responded, that routes were protected, that rollback
  worked, and that a browser could reach the environment.

  They are NOT Camden-site visual approval.
  They are NOT Camden-site performance approval.
  They were run against a protected baseline environment that did NOT contain the
  Camden site. The disposable import failed the media integrity gate and was
  rolled back.

  Nothing in reports/20-mobile-performance.md or build/stage20-lighthouse-baseline.json
  may be cited as evidence that any Camden page performs acceptably.
```

---

## D. Release arithmetic

```text
  checks per page                              29
  pages                                       157
  total check-passes required for full release  4,553

  pages currently at Index-ready: yes             0
  checks currently runnable                       0   (authoritative staging does
                                                       not exist; Gate 28 is NO-GO)
```

---

## `CONTEXT.md` update and diff

```text
  Latest completed stage    30 -> 32   (31 excluded from this run block)
  QA specification          none -> 29 checks, 13 automatable / 16 human-sighted
  QA automation             none -> scripts/32-qa-automated.py, syntax verified, NOT RUN
  Index-ready               0 of 157 — UNCHANGED
  Launch gate               NO-GO — UNCHANGED
```

---

## Hash table

```text
  camden-concreting-import.xml                          A7FF47A1C8C351DF06AF8033518EC657AC57169294992646B035A32B9E773884  MATCH
  eamptcoconcretersmelbourne_WordPress_2026-08-14.xml   45B61BF040742C69156DCB6CFE1C5C9B63F0C86CDF8A06691AD2C56C11DCDC15  MATCH
  build/stage9-page-manifest.json                       578CC81636A5FE2C51FC54A95272D4A3DC70272F6025E294198D6F372ED6EF42  MATCH
  build/stage8-image-map.json                           0C0B9E45102F08169BC1253FBE03050F2DCB4783358482F7C021942A551E4FBF  MATCH
  reports/08-image-rename-map.csv                       43E7977893EDB91675947586FD42B1D11D9A77A9AAB1A24FAAD3C2775E151BA8  MATCH
  CODEX-BUILD-2.1.md                                    BB3686B8BFB2A98064B5A2C8AADD9421F8491989D7C014C306C1C7E4D4DA2D9C  MATCH

  6 of 6 MATCH.
```

---

## GATE 32 RESULT

```text
  Every CONTEXT.md P1 check specified as a discrete numbered item   PASS — 29
  Each has a pass condition and stated evidence                     PASS
  Automatable / human-sighted split declared                        PASS — 13 / 16
  Automation script written, fail-closed, machine-readable          PASS
  Human-sighted subset specified with no automated shortcut         PASS — 16
  Stage 11-20 checks explicitly disclaimed                          PASS
  Count that must pass before one page reaches Index-ready: yes     PASS — 29
  Nothing run                                                       PASS

  GATE 32: PASS.
```
