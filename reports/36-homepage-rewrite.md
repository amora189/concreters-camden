# Stage 36 — homepage sentence rewrite (D29)

Date: 18 August 2026 (Australia/Sydney).
Authority: `DECISION-06-resolvable-items.md` §D29.

**The replacement copy is written below. It is a POST-IMPORT EDIT.**
`camden-concreting-import.xml` is immutable; the sentence cannot be changed in the artifact.

---

## 1. The sentence, verbatim

```text
  page      /homepage/  (post_id 12, publish)
  location  Camden Council crossing section

  CURRENT:
  "For a Camden Council residential crossing, the recorded specification is
   32 MPa concrete, 125mm thickness, SL72 fabric, 4.0-5.5m urban width, a 1200mm
   footpath allocation, 4% crossfall and a maximum 1:6 batter."
```

Two faults, as D29 states:

```text
  1  "the recorded specification is" asserts a record that has not been shown to
     exist. Same construction class as the six registered in
     reports/23-false-fidelity.md.
  2  Seven unattested figures presented as fact on the front page. All seven are
     in reports/35-figure-provenance.csv; none is attested.
```

---

## 2. Replacement — PREFERRED, per D29.2 (numbers cut)

```text
  "Camden Council sets the requirements for a residential vehicle crossing —
   width, concrete grade, reinforcement, crossfall and the footpath allocation.
   Those requirements differ between councils and change over time, so check the
   current specification with your council before work begins."
```

### Why this wording

```text
  removes  "the recorded specification is"        no record is asserted
  removes  all seven unattested figures            nothing unverified is stated
  asserts  only that councils set requirements     true, and checkable
  asserts  nothing about the operator              no process or capability claim
  keeps    the page useful                         tells the reader what governs the job
                                                   and that it varies by council
```

The sentence deliberately makes **no claim about what CoreX does**. An earlier draft read "we confirm the
current requirements with Council before quoting", which asserts an operator process that is not verified
either. That draft is rejected for the same reason as the original.

---

## 3. Replacement — FALLBACK, per D29.1 (figures reframed, not cut)

Only if the owner wants the figures retained on the homepage before the matrix lands.

```text
  "Residential vehicle crossings are commonly built around 32 MPa concrete at
   125mm with SL72 fabric, with widths in the 4.0-5.5m range, a 1200mm footpath
   allocation, about 4% crossfall and a batter no steeper than 1:6. These are
   general indicative figures, not a Camden Council specification — requirements
   differ between councils, and we confirm the current figures before quoting."
```

```text
  STATUS   NOT RECOMMENDED
  reason   it still puts seven disputed numbers on the front page, and the closing
           clause reintroduces an operator process claim
  expiry   this wording is valid only until data/service-specs.yml is populated,
           at which point the figures are replaced with attested values or removed
```

**Recommendation: use §2.** A homepage does not need seven specifications, and every one is disputed.

---

## 4. D29.3 — the four utility pages scanned

Scanned for the same construction class: *the recorded*, *recorded specification*, *reproduced without
alteration*, *the verified*, *verified project record*, *as recorded*, *unaltered*, *verbatim*,
*confirmed specification*.

```text
  PAGE         CLASS     STATUS    WORDS   FALSE-FIDELITY SENTENCES
  /homepage/   home      publish     461   1
  /contact/    utility   publish     126   0
  /quote/      utility   publish     116   0
  /about/      utility   publish     126   0
  /gallery/    utility   publish     108   0
```

**The four utility pages are clean.** The homepage sentence is the only instance outside the six already
registered in `reports/23-false-fidelity.md`.

D29.3's premise holds and is worth recording: coherence measures sense, not truth. These four pages scored
CLEAN on coherence and that told us nothing about whether they assert false records. They happen not to.

---

## 5. Implementation

```text
  method        post-import edit; the WXR is immutable
  where         reports/post-import-tasks.md and the Stage 29 runbook
  when          after the main content import, with the search-replace step
  verification  re-run the false-fidelity scan against rendered staging output;
                expect 0 on the homepage
  figures       once data/service-specs.yml is populated, revisit: attested values
                or removal
```
