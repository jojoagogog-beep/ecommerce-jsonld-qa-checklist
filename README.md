# Ecommerce Product JSON-LD QA Checklist — Free Starter Guide

**Check product-page structured data before a catalog migration, storefront launch, or SEO handoff.** This free educational repository explains how to spot common `schema.org/Product` and `Offer` metadata omissions in public HTML. It includes a small offline Python example that you can run without an API key or paid service.

> Practical AI Lab builds focused Apify Store tools for public ecommerce catalog quality assurance. Start with the free checklist below; use a hosted PAL tool only if you need batch processing, recurring checks, or exportable reports.

## 1. The launch-day checklist

| Check | What to inspect | Why it matters |
| --- | --- | --- |
| Product JSON-LD | `<script type="application/ld+json">` includes `@type: Product` | Gives automated systems a structured representation |
| Product name | A meaningful `name` | Identifies the item being sold |
| Product IDs | `sku`, `gtin*`, or `mpn` when applicable | Helps match catalog records |
| Brand | `brand` when known | Improves catalog consistency |
| Offer price | Numeric/textual `offers.price` or supported price specification | Finds missing published price data |
| Currency | ISO-style `priceCurrency`, e.g. `USD` | Avoids ambiguous prices |
| Availability | `offers.availability` (published label only) | Documents advertised availability; does **not** verify warehouse stock |
| Images | `image` and appropriate HTML `alt` attributes | Improves image metadata completeness and accessibility review |
| Other SEO | Canonical URL, page title, meta description | Helps catch template-regression issues |

Missing structured data is a **review finding**, not automatic proof of a search-ranking problem. Some data fields are optional, and eligibility for search enhancements has additional requirements.

## 2. Try the free offline example

The repository includes a tiny dependency-free Python script that reads **one local HTML file** and prints a JSON checklist:

```bash
python3 check_product_schema.py examples/product_incomplete.html
```

The example intentionally contains an incomplete Product/Offer to demonstrate what a finding looks like. It does **not** crawl websites, scrape private accounts, generate fake reviews, access live stock, or make any network requests.

## 3. Scale to an ecommerce catalog with PAL on Apify

If you are responsible for dozens of public product URLs, prefer a cloud Actor with a documented input schema, CSV/JSON exports, and a repeatable workflow.

| Your job | Suggested PAL tool |
| --- | --- |
| Audit up to 50 public product pages and export prioritized fixes | [Ecommerce Product Schema Checker](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check) |
| Export current published price, currency, SKU, and availability | [Product Price & Availability Extractor](https://apify.com/practical_ai_lab_jp/my-actor) |
| Compare published competitor prices and stock labels between runs | [Competitor Price & Stock Tracker](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta) |
| Audit SKU, GTIN, MPN, and brand metadata | [Product SKU/GTIN/MPN Validator](https://apify.com/practical_ai_lab_jp/my-actor-3) |
| Check price/currency markup before launch | [Product Price & Currency QA](https://apify.com/practical_ai_lab_jp/pal-product-offer-currency-check) |

**How to start:** Open a relevant tool → choose a public Example task or prefilled sample → run a small test if you accept the charges → inspect the Dataset → export CSV/JSON. Check the live **Pricing** tab first. A successfully processed record may incur a pay-per-event charge even if the audit reports no error. Running an Actor may also incur a start charge; confirm on its Pricing tab.

## Hands-on workflows

- [Set up repeatable competitor price and stock monitoring](guides/competitor-price-stock-monitoring.md): baseline, repeat comparisons, pricing caveats and safe scheduling. This guide explains how to turn one-off checks into an operational workflow without claiming automatic notifications.
- [Bulk ecommerce Product JSON-LD catalog audit](guides/bulk-product-jsonld-catalog-audit.md): sample selection, reviewing findings and scaling to 50-page batches with transparent costs.

## 4. When to run these checks

- **Before publishing:** verify Product/Offer metadata on representative storefront pages.
- **After template or theme changes:** recheck the same page URLs for regressions.
- **During catalog migrations:** export findings for merchandising, development, and technical SEO teams.
- **For competitor monitoring:** reuse a monitor identifier on later runs; don't confuse published markup with checkout stock.

## 5. Important limits and responsible use

- The downloadable sample analyzes **offline HTML only**. It is deliberately narrow so it can be inspected and understood.
- PAL Apify tools vary by Actor. They generally target static publicly accessible HTTPS pages rather than rendered JavaScript or pages requiring sign-in.
- Some websites do not publish Product JSON-LD; an empty extraction is not proof that an item has no price.
- Respect site terms and avoid invasive requests. Never enter private customer, payment, or account credentials into an example.
- Apify pricing, input limits, and feature coverage may change; each Actor's live listing is the authoritative description.

## More tools and support

Explore the [Practical AI Lab Apify Store](https://apify.com/practical_ai_lab_jp) and use an Actor's Issues/Support section for product questions.

*Maintained by Practical AI Lab. Independent educational documentation; not endorsed by Shopify or Google.*
