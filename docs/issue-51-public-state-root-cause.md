# Public-state claim root-cause analysis

Date: 2026-09-23
Tracker: edoworks/factory#51

## Defect

NowNest pages described a downloadable, supported app even though Apple acceptance and release qualification remain incomplete. The pages were absent from the portfolio, sitemap, source-page manifest, and global navigation.

## Why chain

1. The pages implied current availability because release-oriented support, privacy, and terms copy was published with the initial product-page set.
2. The implication persisted because page publication was not coupled to the canonical lifecycle record.
3. Discovery omissions persisted because adding a page did not require simultaneous portfolio, sitemap, manifest, and navigation registration.
4. Unsupported response-time and download claims passed because no local claim validator checked public wording.
5. Evidence stops there; no claim is made about the intent behind the original copy.

## Corrections

- Immediate: identify NowNest as a qualification preview, remove download and response-time promises, and scope privacy and terms language to tested builds and website use.
- Root cause: register all four pages in active discovery surfaces and add a CI claim validator.
- Recurrence guard: `scripts/check_site_claims.py` rejects unsupported wording, the failed Rung hostname, missing local links, and incomplete NowNest discovery. Negative tests verify each failure class.
