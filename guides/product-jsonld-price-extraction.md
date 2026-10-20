# Export ecommerce product prices and stock labels from JSON-LD

**Need a structured snapshot of public product information without opening each page manually?** This guide helps merchandising teams and developers understand the difference between a published Product/Offer JSON-LD snapshot and a live inventory feed.

The [PAL Ecommerce Product Price & Stock Extractor](https://apify.com/practical_ai_lab_jp/my-actor) reads fields that are actually present in static public ecommerce HTML. It is not a checkout price verifier, private inventory API or login-based data extractor.

## 1. What a public page may expose

A product page may include structured metadata like:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Example rain jacket",
  "sku": "JACKET-001",
  "brand": {"@type": "Brand", "name": "Example Brand"},
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

This is a **synthetic example**. A published `InStock` label does not prove inventory exists at a particular warehouse or that checkout will accept an order. A structured price can differ from a negotiated, personalized or live checkout price.

## 2. Start with a tiny sample

Open the [PAL price and stock extractor](https://apify.com/practical_ai_lab_jp/my-actor) and use its Input tab or a public Example task:

```json
{
  "urls": [
    "https://scrapeme.live/shop/Pikachu/",
    "https://scrapeme.live/shop/Bulbasaur/"
  ]
}
```

The demo pages are public educational product pages. Replace them with pages your team is authorized to check.

Inspect the resulting Dataset for the published name, price, currency, SKU, brand and availability information. **Export CSV/JSON** for a catalog review, internal comparison or downstream pipeline.

## 3. What to do with missing fields

- **No Product JSON-LD:** check whether the page uses other formats or renders metadata only in JavaScript.
- **Price or currency missing:** ask whether your store template emits Offer metadata for that product.
- **No SKU:** consider whether it is published elsewhere or deliberately unavailable.
- **Offer availability missing:** don't infer zero inventory; it may be unpublished or unavailable to static parsing.
- **Inconsistent page results:** inspect public redirects, locale changes and template differences.

Absence of a field is a review signal, not proof of an ecommerce, SEO or legal defect.

## 4. Turn it into a repeatable workflow

1. Run a few representative public URLs.
2. Check the result quality and the **current Apify Pricing tab** before increasing volume.
3. Export the Dataset to CSV/JSON for catalog reconciliation.
4. Run again after changing your own product templates to check published fields.
5. If you need **change history** rather than independent snapshots, use a stateful monitor that reuses a persistent identifier.

For published price/availability **changes across multiple runs**, use the separate [PAL Competitor Price & Stock Tracker](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta) and the [repeat-monitoring tutorial](competitor-price-stock-monitoring.md).

For a broader structured-data quality report, use the [PAL Ecommerce Product Schema Checker](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check).

**Billing and technical limits:** Actor processing may carry per-event and run-start fees. It reads public static HTML, does not access private pages or authenticate to a storefront, and cannot guarantee real-time inventory. Check the live Pricing and documentation before any run.

[Explore all currently public PAL tools](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html).

*Practical AI Lab: educational guidance for publicly published structured data, with no ranking, inventory or revenue guarantees.*
