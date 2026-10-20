# H1 heading and page-structure QA: practical launch checklist

An ecommerce theme or CMS template can quietly remove the page's main heading, duplicate a product heading, or place headings out of order. A small, repeatable H1 audit helps teams spot these changes before a storefront migration.

The [PAL H1 Heading Checker & SEO Structure Audit](https://apify.com/practical_ai_lab_jp/pal-h1-heading-checker) inspects headings in **static public HTML**. It does not render JavaScript, measure ranking performance or certify accessibility compliance.

## 1. Know what you are checking

Compare these two simplified structures:

```html
<!-- Typical product page -->
<h1>Blue Rain Jacket</h1>
<h2>Features</h2>
<h2>Size and fit</h2>
```

```html
<!-- Needs human review, not automatic proof of a penalty -->
<h1>Blue Rain Jacket</h1>
<h1>Customer reviews</h1>
<h3>Shipping information</h3>
```

More than one H1 is not automatically a Google ranking penalty. The relevant question is whether the document's hierarchy is clear and accessible and whether heading patterns are consistent across templates.

## 2. Select a meaningful QA sample

Choose a small group of URLs representing each template your website uses:

1. Product detail pages with long and short product names.
2. Category or collection pages with filtering and navigation.
3. Content pages with multiple editorial sections.
4. Pages using alternative themes or responsive variants.
5. A URL with no visible product information to test error handling.

Do not treat the total count of page-level findings as a measure of your website's search traffic. It is a *markup consistency* review.

## 3. Run a public HTML check

Open [the PAL H1 Heading Checker](https://apify.com/practical_ai_lab_jp/pal-h1-heading-checker) on Apify. Try one public HTTPS URL first:

```json
{"urls":["https://scrapeme.live/shop/Pikachu/"]}
```

Then replace the example with pages you own or are authorized to audit. The Actor supports up to 18 URLs per run. Review each Dataset row's issue details, export findings as CSV or JSON, and group them by page template.

**Charges:** consult the current Pricing tab before running. Successfully processed pages can be billed even when no issue is found. Running the Actor does not repair your site.

## 4. Turn the report into a useful engineering ticket

Capture the affected URL, template, detected headings, expected heading structure and the change needed. Fix reusable templates rather than changing isolated content entries. Check again after deployment.

If your website relies on client-side rendering, pair the static HTML results with browser-rendered and accessibility tests before concluding the headings are absent.

## 5. Related metadata checks

- [Meta Description Checker](https://apify.com/practical_ai_lab_jp/my-actor-12): audit published description tags.
- [Canonical URL Tag Auditor](https://apify.com/practical_ai_lab_jp/my-actor-13): audit canonical markup.
- [Open Graph Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-16): audit social-preview metadata.
- [All PAL tools](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html): find a targeted public-HTML QA workflow.

*Practical AI Lab — independent training material; no indexing, accessibility or ranking guarantee.*
