# Hreflang QA checklist for multilingual ecommerce sites

**Use this before a country-store launch, locale migration or multilingual template change.** This practical checklist helps technical SEO teams review the `hreflang` references published in static HTML. For batch reporting, use the [PAL Hreflang Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-15) on Apify.

## 1. Understand what hreflang declares

A language/region alternate should identify a corresponding localized page. For example:

```html
<link rel="alternate" hreflang="en-US" href="https://www.example.com/us/water-bottle">
<link rel="alternate" hreflang="en-GB" href="https://www.example.com/uk/water-bottle">
<link rel="alternate" hreflang="ja-JP" href="https://www.example.com/jp/water-bottle">
<link rel="alternate" hreflang="x-default" href="https://www.example.com/global/water-bottle">
```

These are **illustrative URL patterns**, not links to actual products. A tag being present does not mean a search engine will accept, index or use it.

## 2. Make the review list

For each localized product template, check:

- **Language and region format:** e.g. `en-US`, `ja-JP`; avoid arbitrary regional abbreviations.
- **Real destination URLs:** `href` points to an accessible localized equivalent, not an unrelated category.
- **Self-reference:** check that each locale's alternates include the current page when your implementation expects it.
- **Return links:** confirm the target locale references the corresponding source page. A single-page checker cannot prove reciprocity; inspect both pages separately or use a proper site-wide crawl.
- **Canonical handling:** ensure canonical URLs and locale alternates describe consistent pages. Don't point all localized pages at one unrelated canonical.
- **Changes after deploy:** compare the same list after a theme or routing release.

## 3. Test the public markup in Apify

Open the [PAL Hreflang Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-15), then enter a *public HTTPS page you own or are authorized to audit*:

```json
{"urls":["https://scrapeme.live/shop/Pikachu/"]}
```

This public catalog example is for testing the input form; it **may have no hreflang annotations**, which is not automatically an error for a single-language page.

Check the Dataset for declared language/region references, URL-level issue flags and relevant `details`. The tool can process up to 18 public URLs per run. Export CSV/JSON, review findings, then fix your own website and rerun the same pages.

**Limits:** static HTML only; it does not follow every alternate to verify reciprocal links, render JavaScript, crawl an entire website or guarantee an SEO outcome. Each successfully processed page may be charged. Consult the live [Pricing tab](https://apify.com/practical_ai_lab_jp/my-actor-15) before running.

## 4. Pair with related PAL checks

- [Canonical URL Tag Auditor](https://apify.com/practical_ai_lab_jp/my-actor-13): review canonical URL markup.
- [Open Graph Meta Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-16): review localization-specific social preview fields.
- [7-Point On-Page SEO Audit](https://apify.com/practical_ai_lab_jp/my-actor-11): inspect other published on-page metadata.

None of these tools changes a storefront or guarantees rankings. Start with a small sample before committing to a larger paid workflow.

For a central list of all publicly available PAL tools, visit the [searchable Actor catalog](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html).

*Practical AI Lab — independent educational material, not an official search-engine policy statement.*
