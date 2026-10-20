# Bulk ecommerce Product JSON-LD audit: a catalog migration checklist

Catalog migrations can silently introduce missing prices, currencies, SKU identifiers, product images and canonical metadata. This guide explains a repeatable QA workflow for ecommerce operators and technical SEO teams.

For a small local HTML sample, use the [free offline starter checker](../check_product_schema.py). For multiple **public** product pages, the [PAL Ecommerce Product Schema Checker on Apify](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check) audits up to 50 URLs per run and exports reviewable findings.

## 1. Choose a representative sample

Start with 2–5 pages covering different product templates, currencies or stock labels, not a random sample of your most popular items.

- A normal in-stock item with a price and SKU.
- An out-of-stock item whose Offer availability is published.
- A variable/multi-offer product if the storefront uses one.
- A page with deliberately incomplete metadata, to confirm findings make sense.

**Static HTML only:** the PAL Actor reads public HTML. JavaScript-rendered-only pages and gated login flows may not expose the data it needs. A missing value is a *review signal*, not proof of missing actual inventory or an SEO ranking penalty.

## 2. Run a small test first

Open the [public sample task](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check/examples/audit-product-listing-price-stock-sku). Use a prefilled example or enter an HTTPS product page:

```json
{
  "urls": [
    "https://scrapeme.live/shop/Pikachu/",
    "https://scrapeme.live/shop/Bulbasaur/"
  ]
}
```

The sample URLs are publicly accessible test catalog pages. Replace them with your own product URLs before operational use. If pages block automated requests or expose no Product/Offer JSON-LD, the results may be incomplete.

## 3. Inspect each category of findings

| Area | Questions for your team |
| --- | --- |
| Product name and brand | Are product fields consistently published across templates? |
| Price and currency | Are `Offer` price and `priceCurrency` populated? |
| Availability label | Does the published schema include a valid availability value? |
| Product identifiers | Are `sku`, GTIN or MPN fields populated where applicable? |
| Images | Are Product image URLs included, and is visible HTML alt text appropriate? |
| SEO metadata | Are canonical and description fields present and plausible? |

Not every field is required for every site or product type. Confirm relevant search-engine documentation and implementation needs before turning a warning into a development ticket.

## 4. Export and triage

1. Download the Actor Dataset in CSV or JSON format.
2. Group findings by **template**, **error type**, and **business importance**.
3. Assign a catalog or engineering owner to each class of issue.
4. Fix the underlying theme/template data source rather than manually editing dozens of individual pages.
5. Recheck the same product URLs after deployment, and compare issue counts.

## 5. Scale deliberately

The Actor supports up to 50 public product URLs per run. Partition a larger catalog into multiple batches, monitor result quality, and compare billing against the value of the checks.

**Before running or scheduling it, read the live Apify Pricing tab.** Pay-per-event charges may apply to successfully processed pages even when the audit finds no problems, and an Actor run may have a start charge. This guide does not execute any Actor or create a paid schedule.

## Related tools

- [Product Price & Availability Extractor](https://apify.com/practical_ai_lab_jp/my-actor)
- [Product SKU/GTIN/MPN Validator](https://apify.com/practical_ai_lab_jp/my-actor-3)
- [Product Offer Currency Checker](https://apify.com/practical_ai_lab_jp/pal-product-offer-currency-check)
- [Competitor Price & Stock Tracker](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta)
- [Repeatable competitor price monitoring tutorial](competitor-price-stock-monitoring.md)

*Practical AI Lab: educational guidance for public structured data. Not a Google, Shopify, or Apify endorsement; no guaranteed rankings or business results.*
