# Stage 30 — Fluent Forms specification

Date updated: 21 August 2026 (Australia/Sydney).
Authority: `CODEX-BUILD-2.1.md` §4.30.4 and owner attestations dated 21 August 2026.

**Specification only.** No form was created or imported and no Fluent Forms setting was changed. The four active Elementor pages `/about/`, `/contact/`, `/gallery/` and `/quote/` each reference `[fluentform id="3"]`; the form does not travel in WXR and is not verified to exist in the target database.

## Operating disclosure

The following disclosure is mandatory beside every form placement and in the eventual form confirmation:

> Submitting an enquiry does not create a construction contract.

The form and its surrounding text must also communicate the verified operating model: Structure Co Concreters Camden manages enquiries and coordinates suitable independent providers. Job-specific quotations, contractual terms, licensing, insurance and warranty information must be confirmed before work begins.

## Fields

```text
  FIELD           TYPE       REQUIRED   VALIDATION                     NOTES
  name            text       yes        1–100 characters               no separate first/last
  phone           tel        yes        AU format, +61 or 0 prefix     primary contact route
  email           email      no         RFC-valid                      optional
  suburb          text       yes        1–60 characters                enquiry location only
  service         select     yes        one of 10 service concepts     an enquiry type, not a promise
  job_size        select     no         approximate square-metre bands not a quotation
  message         textarea   no         0–2000 characters              free text
  consent         checkbox   yes        must be ticked                  see consent section
  honeypot        hidden     n/a        must remain empty              spam control
```

No field or label may imply that Structure Co accepts a construction contract, supplies a fixed-price quote, performs the work, holds a licence or insurance, or guarantees a response time.

## Recipient and delivery

```text
  recipient              info@concreterscamden.com.au — owner-attested and monitored
  reply-to               submitter email if supplied; otherwise none
  from address           authenticated address on the site domain
  public telephone       (03) 4328 3392 / tel:+61343283392
  telephone description  public telephone only; never “local Camden/Sydney number”
  delivery mechanism     authenticated SMTP
  delivery proof         still required before publication
```

PHP `mail()` is not accepted. SPF/DKIM-aligned authenticated delivery and a human-sighted test receipt in the attested mailbox remain publication blockers.

## Consent and provider disclosure

Proposed consent text, still requiring final form-level approval:

> I agree to Structure Co Concreters Camden contacting me about this enquiry, storing the information I provide, and sharing it with a suitable independent provider so that the provider can assess the enquiry. Submitting this enquiry does not create a construction contract.

The checkbox must not be pre-ticked. A link to `/privacy-policy/` must appear beside it. The provider relationship must use neutral language; no provider number or credential may be asserted without evidence.

## Privacy blockers

The derived privacy page now uses the attested email, telephone, administrative correspondence address and operating model. It retains five genuine markers: accountable legal entity; delivery/storage/access controls; retention period; analytics/tracking state; and publication date. Those markers block publication even though the public contact facts are now verified. No ABN is requested or asserted.

## Placement and status

```text
  /about/     form ID 3 placeholder; non-contract disclosure required
  /contact/   form ID 3 placeholder; non-contract disclosure required
  /gallery/   form ID 3 placeholder; page deferred and absent from launch navigation
  /quote/     form ID 3 placeholder; non-contract disclosure required

  form implementation     NOT IMPLEMENTED
  form approval            PARTIAL — owner facts/operating model applied; field and consent build approval remains
  publication              BLOCKED — form, SMTP and five privacy markers unresolved
```

The administrative correspondence office at 15 Murray Street, Camden NSW 2570 is not open to customers or visitors. The form and confirmation email must not invite visits or describe it as a showroom, customer-service location or walk-in office.
