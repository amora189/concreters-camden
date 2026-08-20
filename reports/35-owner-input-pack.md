# OWNER INPUT PACK — everything the build now needs from you

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-05-figures-mark-pause.md` §D28.

**The build is paused pending your inputs. It is not blocked on technical work.**

Every agent-executable stage that can run without owner data has run. Stages 21–30, 32 and 34–36 are
complete. Stage 31 awaits approval. What remains is five inputs, and nothing can proceed without them. A sixth — Camden job photography — was answered and is now settled rather than pending.

```text
  architecture        77 pages (76 + privacy policy, D31)
  index-ready         0
  launch gate         NO-GO
  effective Wave 1    4 utility pages, each with its own further blocker
```

---

# INPUT 1 — Service specification matrix

## THE CRITICAL PATH. Nothing proceeds without this.

```text
  WHAT        For each of the 10 services, 9 fields:
                slab_thickness, concrete_grade, reinforcement, base_preparation,
                control_joint_spacing, cure_time, fall_and_drainage,
                edge_treatment, service_specific_requirement

  FORMAT      Fill data/service-specs.yml in place. Each field takes:
                value:        the figure with its unit
                verified:     true
                attested_by:  owner | engineer | Australian Standard + clause
                source:       document, clause, or "owner attestation"
                sighted_date: YYYY-MM-DD

  ON DISK     data/service-specs.yml          (exists, empty, 10 x 9 = 90 fields)

  UNBLOCKS    All 10 service page rewrites (~8,000 words)
              22 pages currently blocked from every wave by unattested figures
              The 40% pairwise uniqueness cap - real spec differences make ten
              pages pass naturally; paraphrase does not

  RELEASES    10 service pages directly. Indirectly the homepage and 11 suburb
              pages that repeat the same figures.

  WHY YOU     The ten pages currently carry an IDENTICAL nine-value set:
              32 MPa, 125mm, SL72, 800mm, 900mm, 1200mm, 4.0-5.5m, 4%, 1:6.
              A pedestrian path and a commercial hardstand cannot both be
              correctly specified at 125mm and SL72. No agent may infer which
              values apply to which service - that is exactly how the current
              wrong set was produced.
```

---

# INPUT 2 — Media: binaries, Astra export, and a working re-encode driver

## Three parts. All three are required together.

```text
  2a  THE 83 IMAGE BINARIES
      WHAT      The 83 original files, named exactly as listed
      FORMAT    JPEG / PNG / WEBP, at or above the recorded dimensions
      ON DISK   source-inputs/media/          (exists, empty, README lists all 83)
      VERIFY    python scripts/22-media-audit.py     currently exits 1, 0 of 83

  2b  THE ASTRA CUSTOMIZER EXPORT
      WHAT      Astra theme mods from the source install
      FORMAT    .dat from Customizer Export/Import, OR theme_mods_astra JSON,
                OR Astra Import/Export Settings JSON
      ON DISK   source-inputs/astra/          (exists, empty, README lists 7
                                               required mod groups)
      VERIFY    python scripts/22-astra-audit.py     currently exits 1, 0 of 7 groups
      NOTE      A WXR does not carry theme mods. Site identity, colours,
                typography, layout, header, footer and buttons all live here and
                are lost without it. It also holds the header logo assignment,
                which is why the site mark question cannot be closed today.

  2c  A WORKING RE-ENCODE DRIVER  -  P0, newly promoted
      WHAT      Install ImageMagick, then use scripts/22-reencode-images.sh
      WHY       reencode-images.sh at the repo root HAS NEVER PARSED. bash -n
                fails at line 11. No image in this build has ever had EXIF
                stripped. If the binaries import without this step, GPS
                coordinates from Melbourne job sites and owner/device metadata
                publish to a live website.
      VERIFY    scripts/22-media-audit.py now carries a fail-closed EXIF
                assertion - zero GPS, owner/artist/serial and original-datetime
                tags - proven against a known-dirty file by
                tests/test_exif_assertion.py (currently PASS).

  UNBLOCKS      The authoritative staging import in full. Stage 28 gates 4 and 5.
                Header and brand rendering. All media gates.
  RELEASES      Nothing on its own, but no page can be released without it.

  STILL NOT COVERED: pixel-level verification. Every audit so far has read
  filenames, titles and alt text. Nothing has looked at the images themselves,
  and 20 of the 83 are Victorian photographs renamed to NSW places. Only the
  human-sighted QA check H4 catches that.
```

---

# INPUT 3 — Business identity

```text
  WHAT        legal entity name behind the trading name
              ABN, and whether that entity contracts with customers
              NSW Fair Trading licence number, holder, expiry
              public liability and workers compensation insurance
              street address, AND whether it is staffed in business hours
              proof you own and answer 03 4517 6915, or the correct number

  FORMAT      Fill data/verified-facts.yml in place, same field shape as Input 1.

  ON DISK     data/verified-facts.yml         (exists, 0 fields verified)

  UNBLOCKS    All schema. Right now the builder refuses to emit Organization and
              LocalBusiness entirely, which forces all 105 Service nodes to omit
              provider. 309 refusals are logged.
              The wordmark, which cannot name an unverified entity.
              24 evidence markers across 24 pages.

  RELEASES    Contributes to every page. Blocks all 77.

  TWO POINTS  1. "Is it staffed" is decisive, not incidental. An unstaffed address
                 is not a LocalBusiness location and asserting one is a false claim
                 about where customers can find you.
              2. 03 4517 6915 is a VICTORIAN area code on a NSW business, appearing
                 120 times in the artifact. It has been flagged, never silently
                 corrected.
              3. The Elementor kit still declares site_name "E&T Co Concreters
                 Camden" - the source Melbourne business. The copy says "CoreX".
                 Two trading names, neither verified. Confirm which is correct.
```

---

# INPUT 4 — Council crossing specifications

```text
  WHAT        Per LGA - Liverpool, Camden, Campbelltown, Wollondilly:
              vehicle crossing widths, concrete strength, grade limits,
              application path, fee schedule

  FORMAT      Per figure: the value, the council page URL you read it on, and the
              date you read it. No figure without both.

  ON DISK     data/council-specs.yml for the calculator (Stage 31)
              data/service-specs.yml service_specific_requirement for crossovers

  UNBLOCKS    LIVERPOOL specifically: 4 REQUIRED-RESEARCH markers, 4 of the 6
              false-fidelity sentences, 2 Wave 1 suburb pages
              ALL FOUR: the crossovers service page, and the §4.31 calculator
              which needs the identical figures - one verification clears both

  RELEASES    4 pages on Liverpool alone. More across the other three.

  RULE        No figure may be filled from a neighbouring suburb, from another
              LGA, or from a Melbourne figure. Leppington straddles the
              Camden/Liverpool boundary, so a Camden figure is wrong there for a
              second, independent reason.
```

---

# INPUT 5 — Service page authorship decision

```text
  WHAT        Who writes the ~8,000 words across 10 service pages.

  OPTIONS     (a) an agent, under the coherence gate, with output measured BEFORE
                  it enters the artifact
              (b) a human writer who knows concreting
              (c) a mix - agent drafts structure, human writes the technical body

  ON DISK     no artifact; a decision recorded in a new decision record

  UNBLOCKS    the rewrite itself, once Input 1 exists

  NOTE        The current filler was generated, entered the artifact, and was only
              caught two stages later by a scan looking for something else. If (a),
              the gate must run on output before it is written into any WXR.
              scripts/34-coherence.py exists and is build-failing.

  SEQUENCE    This decision is NOT urgent. Input 1 must land first; there is
              nothing to write against until it does.
```

---

# INPUT 6 — WITHDRAWN: Camden job photographs

```text
  STATUS   NOT AN INPUT. SETTLED FACT.

  Per DECISION-06 D32: no Camden job has been completed, none is scheduled, and
  fulfilment is Pakenham. The 47 REAL_PHOTO_PENDING slots have no path to being
  filled, so they are not waiting on anything.

  RESOLUTION   the evidential modules are REMOVED, not held.
               16 pages, 427 words, no page drops below any floor.
               See reports/36-photography-removal.md.

  REOPENS IF   a Camden job is completed AND photographed AND permission to
               publish is obtained. Only then.

  SIDE EFFECT  the Tier 1 photography hold is RELEASABLE on all six pages - the
               first blocker in this project cleared rather than deferred. Those
               pages still carry three or four other blockers each, so none
               becomes releasable as a result.

  ONE OWNER DECISION REMAINS
    /gallery/ is 108 words, 58 of them the removed section. A gallery with no
    images is not a gallery. Withdraw it, repurpose it as a finishes page using
    generic licensed imagery, or keep it empty and noindexed. Recommendation:
    withdraw or repurpose.
```

---

# Priority

```text
  1  INPUT 1   service specification matrix     THE critical path
  2  INPUT 2   media + Astra + re-encode driver  gates the entire import
  3  INPUT 3   business identity                 gates all schema, blocks all 76 pages
  4  INPUT 4   council specifications            Liverpool first, 4 pages
  5  INPUT 5   authorship                        not urgent; needs Input 1 first
  -  INPUT 6   WITHDRAWN - settled, not pending; modules removed instead
```

Inputs 1 and 2 are the critical path. Input 6 is withdrawn: the answer was given and the modules are removed.

---

# What happens when they arrive

```text
  Input 1        -> service page rewrite begins, under the coherence gate
  Input 2        -> media and Astra audits pass; authoritative staging can be built
  Inputs 1-4     -> Stage 28 preflight can return GO
  Then           -> Stage 31 calculator, Stage 32 QA, then page-by-page release
```

Until then nothing further is done. No stage is begun, no image is sourced, and no `verified: false`
field is populated.
