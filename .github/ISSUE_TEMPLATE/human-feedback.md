---
name: Website Feedback
about: Submit feedback for an edoworks website page (FS-6 channel). No free-text, no PII.
title: "Feedback: [rating] - [category] - edoworks"
labels: ["website-feedback"]
---

<!--
  FS-6 Website Feedback Channel — human-form transport.
  This template is the human counterpart to the AI-agent REST transport
  documented at /.well-known/feedback.json.

  Rules (enforced by pull_website_feedback.py):
    - rating MUST be one of: helpful, partly, not_helpful
    - category MUST be one of: bug, suggestion, praise, question
    - source_page_id MUST be one of: home, blog-index, blog-post,
      portfolio, privacy, terms, support, other
    - source_type MUST be: human-form  (AI agents use the REST path)
    - No free-text, no names, no emails, no URLs in the body.
    - The issue title is NOT retained by the puller (only the structured
      fields below are ingested into the product-feedback ledger).

  See .factory/standards/website-feedback-channel.md for the full standard.
-->

**Product:** edoworks
**Rating:** [helpful / partly / not_helpful]
**Category:** [bug / suggestion / praise / question]
**Source page id:** [home / blog-index / blog-post / portfolio / privacy / terms / support / other]
**Source type:** human-form