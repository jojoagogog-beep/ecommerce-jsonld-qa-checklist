# Ecommerce product identifier QA: SKU, GTIN, MPN and brand

Catalog migrations often create mismatched product identifiers or omit them from structured data even when the storefront looks correct. This guide shows a responsible way to review **published** `schema.org/Product` identifier fields.

Use the [PAL Product SKU/GTIN/MPN Validator](https://apify.com/practical_ai_lab_jp/my-actor-3) for focused identifier QA or the [PAL Product Name & SKU Schema Audit](https://apify.com/practical_ai_lab_jp/pal-product-name-schema-audit) to review name and SKU markup.

## 1. Know which field means what

| Field | Practical meaning | Caution |
| --- | --- | --- |
| `sku` | The merchant's internal stock-keeping identifier | Often unique only within that seller's catalog |
| `gtin`, `gtin13` and variants | Published global trade item identifier | Not every item has a GTIN; validity requires more than presence |
| `mpn` | Manufacturer part number | May be absent for products without an applicable MPN |
| `brand` | Brand associated with the product | Should reflect the actual brand, not an invented label |
| `name` | Product name in structured data | Must describe the right page's product |

This sample demonstrates *presence* and *format*, not registry authentication:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Example Water Bottle",
  "sku": "BOTTLE-BLUE-500",
  "brand": {"@type": "Brand", "name": "Example Brand"},
  "offers": {
    "@type": "Offer",
    "price": "19.95",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

The sample intentionally does not claim a real GTIN or manufacturer identity. Never fabricate a GTIN just to silence an audit warning.

## 2. Select catalog pages

Compare several representative product families: a standard physical product, an item sold in variants, a custom-made product and a product that may legitimately have no GTIN. Define the **applicable** identifier requirements with the merchandising team before making missing-field warnings into mandatory fixes.

## 3. Audit the published structured data

Open [PAL Product SKU/GTIN/MPN Validator](https://apify.com/practical_ai_lab_jp/my-actor-3) and start with a small public HTTPS input:

```json
{"urls":["https://scrapeme.live/shop/Pikachu/"]}
```

This is a public demo catalog URL; replace it with product pages you own or are authorized to check. Inspect the returned fields and warnings, then export the Dataset as CSV or JSON for your catalog QA process.

**Important limits:** these tools read static public HTML; they do not verify identifiers against GS1 or manufacturer registries, log in to stores, confirm live stock or change data. Missing identifiers can be appropriate for some products. Check each Actor's current Pricing tab; a successfully processed page can be chargeable even with no issues.

## 4. Turn findings into catalog improvements

1. Group missing identifiers by product family, supplier, template and source system.
2. Verify the actual identifier in your existing authoritative catalog.
3. Repair the upstream product data or theme template.
4. Repeat the same URL sample after deployment to confirm the *published* markup changed.
5. Keep the exported before/after records for internal QA, not for claims of search-ranking gains.

## 5. Related product checks

- [Bulk Product Schema Checker](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check): a wider audit for up to 50 public pages.
- [Price & Stock Extractor](https://apify.com/practical_ai_lab_jp/my-actor): export published Offer fields.
- [Free offline Product JSON-LD checklist](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/): understand the data before using an Actor.
- [Complete PAL catalog](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html): find other focused metadata checks.

*Practical AI Lab — independent catalog QA tutorial. No ranking, identifier authenticity or revenue outcome is guaranteed.*
