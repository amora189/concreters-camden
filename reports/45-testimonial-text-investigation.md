# Testimonial-text investigation — attachments 46, 47, 48, 49, 51, 52 and 228

Date: 20 August 2026 (Australia/Sydney).
Source: immutable `camden-concreting-import.xml`; Elementor structure plus WordPress page status.

## Outcome

**Fabricated customer quotes found: 0.** The seven files are testimonial-labelled photographs,
not testimonial portraits attached to reviews. No placement of any target carries a customer name,
customer quote, star rating, testimonial suburb attribution, review date or testimonial job description.
Accordingly, no invented-testimonial category is added to the false-fidelity register.

The only actual Elementor testimonial widgets in the entire WXR are three homepage placeholders.
All three have an empty image ID, placeholder review text, placeholder reviewer name, no job field
and no rating field. None references attachments 46, 47, 48, 49, 51, 52 or 228.

## Attachment distribution

| Attachment | Pages | Placements | Publish pages | Draft pages | Local-work-card placements |
|---:|---:|---:|---:|---:|---:|
| 46 `concrete-tesimonial-4-camden-46.webp` | 15 | 17 | 2 | 13 | 1 |
| 47 `concrete-testimonial-6-camden-47.webp` | 15 | 15 | 4 | 11 | 0 |
| 48 `concrete-testimonial-3-camden-48.webp` | 15 | 15 | 4 | 11 | 1 |
| 49 `concrete-testimonial-1-camden-49.webp` | 15 | 16 | 3 | 12 | 1 |
| 51 `concrete-testimonial-2-camden-51.webp` | 15 | 15 | 2 | 13 | 0 |
| 52 `concrete-testimonial-1-1-camden-52.webp` | 15 | 16 | 2 | 13 | 1 |
| 228 `concretejob1camden-228.jpg` | 14 | 16 | 2 | 12 | 0 |

Attachment 228 is the correction to the supplied premise: it appears on **14 pages**, not 15,
with 16 placements because it is used twice on both Bargo and Mount Annan.

## Exact text in the four local-work-card placements

| Attachment | Page | Status | Exact adjacent text |
|---:|---|---|---|
| 46 | `/concreters-gregory-hills/` | publish | `[[REAL_PHOTO_PENDING: verified CoreX project in Gregory Hills]]` |
| 48 | `/concreters-edmondson-park/` | draft | `[[REAL_PHOTO_PENDING: verified CoreX project in Edmondson Park]]` |
| 49 | `/concreters-edmondson-park/` | draft | `[[REAL_PHOTO_PENDING: verified CoreX project in Edmondson Park]]` |
| 52 | `/concreters-catherine-field/` | draft | `[[REAL_PHOTO_PENDING: verified CoreX project in Catherine Field]]` |

Attachments 47, 51 and 228 have **zero** local-work-card placements. The four rows above carry
blocking markers, not customer assertions: no customer is named and no quote, rating, date or
job description is supplied. Those local-work modules are already scheduled for complete removal
under D32; the generic-photo verdict does not authorise them as evidence.

## Actual testimonial widgets in the WXR

| Page | Widget | Content | Name | Job | Image ID |
|---|---|---|---|---|---|
| `/homepage/` | `5a4a4815` | `[[PLACEHOLDER: verified CoreX review text and permission to publish]]` | `[[PLACEHOLDER: verified reviewer name]]` | `(empty)` | `(empty)` |
| `/homepage/` | `16805a15` | `[[PLACEHOLDER: verified CoreX review text and permission to publish]]` | `[[PLACEHOLDER: verified reviewer name]]` | `(empty)` | `(empty)` |
| `/homepage/` | `51fc6392` | `[[PLACEHOLDER: verified CoreX review text and permission to publish]]` | `[[PLACEHOLDER: verified reviewer name]]` | `(empty)` | `(empty)` |

## Machine-verifiable totals

```text
  target placements                            110
  populated customer/name/quote/job fields    0
  populated rating fields                     0
  actual testimonial widgets                  3
  actual testimonial widgets using targets   0
  fabricated customer quotes                 0
```

The complete evidence is `reports/45-testimonial-text-investigation.csv`: one row per image
placement, with exact same-widget text, the nearest containing Elementor context, current alt
text, WordPress status, marker text and any exact testimonial/rating keys.

No page or WXR value was changed by this audit.
