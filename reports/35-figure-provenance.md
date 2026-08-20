# Stage 35 — figure provenance (D26)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-05-figures-mark-pause.md` §D26.
Data: `reports/35-figure-provenance.csv` (214 rows), `reports/35-figure-provenance-summary.json`.

**Nothing was deleted. Nothing was rounded.** Every figure is flagged in place, per D26.3.

---

## 1. The withdrawn clause

`CODEX-BUILD-2.1.md` §2 closing paragraph is **withdrawn** by D26. The instruction document is not
edited; the withdrawal lives here and in the ledger under `DEC05-D26`.

```text
  WAS   "Where any document gives a specific figure (32 MPa, 125mm, SL72, 800mm vs
         900mm footpath allocation, 1200mm, 4.0-5.5m, 4%, 1:6), reproduce it exactly.
         Never round, soften or paraphrase a specification."

  NOW   No figure is protected by virtue of appearing in a planning document.
        Protection comes from attestation - a source, a sighted date, or an
        owner/engineer sign-off - not from prior appearance.
```

The clause had been protecting unattested numbers from correction.

---

## 2. Scan result

```text
  rows                                        214
  distinct pages carrying an unattested figure 29
    of which ACTIVE (not withdrawn)            22
    of which already withdrawn                  7

  by population
    council-sourced-pending-verification      137 rows
    template-artefact-unattested               77 rows

  active rows by class    service 91, suburb 97, home 7
  active rows by status   publish 132, draft 63
```

### The two populations, kept separate per D26.4

```text
  COUNCIL-SOURCED-PENDING-VERIFICATION
  Plausibly traceable to a council instrument. Verification path: the relevant
  council's current published specification, with source_url and sighted_date.

    800mm       22 occurrences    footpath allocation, Oran Park
    900mm       22               footpath allocation, Camden LGA default
    1200mm      24               allocation width
    4.0-5.5m    22               crossing width range
    4%          23               crossfall
    1:6         24               maximum batter

  TEMPLATE-ARTEFACT-UNATTESTED
  Service-dependent engineering values, currently identical across ten different
  services. Verification path: owner or engineer attestation per service, entered
  in data/service-specs.yml.

    32 MPa      24               concrete grade
    125mm       24               slab thickness
    SL72        26               reinforcement fabric
    SL82         3               reinforcement fabric, concrete-slabs only
```

They are not merged. A council can settle the first group; only an engineer or the operator can settle
the second.

---

## 3. Every active page carrying an unattested figure

Per D26.5, each is **blocked from every wave** until its figures are attested.

```text
  PAGE                                                 CLASS     STATUS
  homepage                                             home      publish
  commercial-concreting-south-west-sydney              service   publish
  concrete-crossovers-and-laybacks-south-west-sydney   service   publish
  concrete-driveway-replacement-south-west-sydney      service   publish
  concrete-driveways-south-west-sydney                 service   publish
  concrete-paths-south-west-sydney                     service   publish
  concrete-patios-south-west-sydney                    service   publish
  concrete-slabs-south-west-sydney                     service   publish
  decorative-concrete-south-west-sydney                service   publish
  exposed-aggregate-south-west-sydney                  service   publish
  shed-and-garage-slabs-south-west-sydney              service   publish
  concreters-catherine-field                           suburb    draft
  concreters-cobbitty                                  suburb    draft
  concreters-currans-hill                              suburb    draft
  concreters-elderslie                                 suburb    draft
  concreters-gledswood-hills                           suburb    publish
  concreters-gregory-hills                             suburb    publish
  concreters-harrington-park                           suburb    publish
  concreters-mount-annan                               suburb    draft
  concreters-narellan                                  suburb    draft
  concreters-oran-park                                 suburb    publish
  concreters-spring-farm                               suburb    draft

  22 active pages. 7 further affected pages are already withdrawn under D16/D21.
```

---

## 4. The homepage — and why this matters more than the count suggests

The homepage was the **only page to score CLEAN on the coherence scan**. It carries the entire
unattested set in a single sentence:

```text
  "...idential crossing, the recorded specification is 32 MPa concrete, 125mm
   thickness, SL72 fabric, 4.0-5.5m urban width, a 1200mm footpath allocation,
   4% crossfall and a maximum 1:6 batter."
```

Two problems in one sentence:

```text
  1  Seven unattested figures presented as a specification.
  2  "the recorded specification is" - a false-fidelity construction of exactly the
     class registered in reports/23-false-fidelity.md. It asserts a record that has
     not been shown to exist.
```

The page that passed every coherence test is asserting seven unverified numbers as recorded fact on the
site's front page.

---

## 5. Consequence — Wave 1 collapses from 30 to 8

D26.5 blocks any page carrying an unattested figure from every wave. Applied to the D21 Wave 1:

```text
  WAVE 1 BEFORE D26        30   1 home + 4 utility + 10 service + 15 researched suburbs
  BLOCKED BY D26          -22   1 home + 10 service + 11 researched suburbs
  WAVE 1 REMAINING          8   4 utility + 4 suburbs

  the 4 remaining suburbs   concreters-austral, concreters-bringelly,
                            concreters-edmondson-park, concreters-leppington
```

And each of those four carries its own separate blocker:

```text
  concreters-austral        Liverpool council specification (D13); Tier 1 photography hold
  concreters-leppington     Liverpool council specification (D13); Tier 1 photography hold
  concreters-bringelly      2 unfillable false-fidelity sentences (D11)
  concreters-edmondson-park Liverpool council specification (D12)
```

**Effective Wave 1 is 4 utility pages**, and those depend on the identity and phone answers plus, for
`/about/` and `/gallery/`, the unbuilt Fluent Forms form and the non-existent privacy policy.

This is not a reason to soften D26. It is the honest consequence of applying it, and it is better known
now than after publication.

---

## 6. Disposition

```text
  deleted            0 figures
  rounded            0 figures
  altered            0 figures
  flagged in place   214 occurrences across 29 pages
  blocked from waves 22 active pages
```

Per D26.3: deletion loses information that may prove correct; alteration invents a second wrong number.
Every figure stays exactly where it is, marked `attested: NO`.
