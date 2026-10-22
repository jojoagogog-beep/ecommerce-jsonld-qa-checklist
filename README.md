# Ecommerce Product JSON-LD QA Checklist — Free Starter Guide

**Check product-page structured data before a catalog migration, storefront launch, or SEO handoff.** This free educational repository explains how to spot common `schema.org/Product` and `Offer` metadata omissions in public HTML. It includes a small offline Python example that you can run without an API key or paid service.

> Practical AI Lab builds focused Apify Store tools for public ecommerce catalog quality assurance. Start with the free checklist below; use a hosted PAL tool only if you need batch processing, recurring checks, or exportable reports.


## Find the right tool in under one minute

Not every ecommerce data problem needs the same kind of automation. Start with the job, not the name of the tool:

| What you need | Where to start |
| --- | --- |
| Compare your own reference price with public competitor prices, then recheck changes | [Competitor Price Tracker and live Apify Pricing](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta?utm_source=github&utm_medium=organic&utm_campaign=pal_readme_buyer_jobs) |
| Audit up to 50 public Product/Offer JSON-LD pages before a product catalog update | [Ecommerce Product Schema Checker and live Apify Pricing](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check?utm_source=github&utm_medium=organic&utm_campaign=pal_readme_buyer_jobs) |
| Decide whether you need price monitoring, batch extraction or a structured-data audit | [Free buyer's tool-selection guide](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/tool-finder.html) |
| Inspect a concrete task with ready-to-review input instead of starting from scratch | [57 published Apify Example tasks](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/example-tasks.html) |
| Run a small local preview with no paid Actor execution | [Free in-browser Product JSON-LD preview](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/product-jsonld-preview.html) |

**Cost note:** Reading these pages is free. Running an Apify Actor can create event and usage charges; always review its current Pricing tab first. PAL does not verify hidden checkout prices, true warehouse stock or search ranking.


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

## Free browser-only Product JSON-LD checker

Use the [free Product JSON-LD preview](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/product-jsonld-preview.html) to paste a Product JSON-LD object, an `@graph` or static HTML with `application/ld+json` script tags. Check product names, price, currency, published availability, brand, image and SKU/GTIN/MPN clues entirely inside your browser. This preview never fetches a URL, uploads input or starts an Apify Actor; it is not a full Schema.org or Google Rich Results validator.

For a reviewable batch audit of up to 50 public product URLs, see [PAL Ecommerce Product Schema Checker](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check) and inspect current Pricing before running.

## Free offline hreflang audit example

For multilingual website QA, use the separate dependency-free [hreflang attribute checker](check_hreflang.py). It reviews a **single local HTML file**, flags duplicate locale tags, missing/relative alternate URLs and suspicious language formats, and returns JSON:

```bash
python3 check_hreflang.py examples/hreflang_sample.html --page-url https://www.example.com/us/example-product
```

It **does not crawl websites, validate reciprocal links, or verify indexing**. For an optional cloud batch review of up to 18 *public* URLs, see [PAL Hreflang Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-15) and consult the live Pricing tab before using it.

## Ten ready-to-paste website QA inputs

Prepare tested synthetic pages and ready-to-copy input JSON for [ten PAL website quality Actors](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/schema-audit-quickstart.html): FAQPage, BreadcrumbList, JSON-LD syntax, external-link safety, schema type inventory, mobile viewport, sitemap links, language declarations, duplicate meta and pagination. This page does not execute any Actor. Apify pricing still applies if you choose to run one.

## Free FAQPage JSON-LD structure checker

Try the [free browser-only FAQPage JSON-LD checker](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/faq-schema-checker.html). Paste one FAQPage JSON-LD object or one script block and review missing question names or accepted-answer text. It does not upload content, crawl websites, execute pasted code or start a paid Actor. This is a structural heuristic, not proof of answer accuracy, search indexing or Google rich-result eligibility.

For recurring checks of public HTTPS FAQ pages, see [PAL FAQ Schema Audit](https://apify.com/practical_ai_lab_jp/pal-faq-schema-checker) and review the live Pricing tab before running.

## Competitor price tracker: features, costs and first-run example

The [PAL competitor price tracker buyer's guide](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/competitor-price-tracker.html) explains the first-run own-price comparison, repeat price monitoring, CSV/JSON exports, supported static Product JSON-LD/Open Graph data, limitations, and a clearly labeled example of pay-per-event charges. It links to [the live Apify product listing](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta) and its authoritative Pricing tab. The guide is free to read and does not trigger an Actor run. Visit the [public first-run example](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta/examples/track-product-prices-from-open-graph-tags) to inspect its synthetic input, then read live pricing before initiating any Actor run.

## Free competitor price gap calculator

Try the [free browser-only competitor price calculator](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/competitor-price-calculator.html) before setting up a paid monitoring workflow. Enter your own reference price and a competitor's **published** price in the **same currency**. It calculates the difference locally with no signup, data upload, live website fetching or Apify Actor run. All initial values are fictitious.

If you need automated checks of real public product pages, [PAL Competitor Price Tracker](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta) supports optional first-run `referencePrices`, Product JSON-LD and explicitly product-typed Open Graph pricing metadata. Monitoring may incur event and run-start charges; read the live Pricing tab first. It cannot verify checkout prices or warehouse stock.

## Free offline competitor-price snapshot comparison

Try the [local price/availability comparison script](compare_product_snapshots.py) before subscribing to any recurring workflow. It compares two example JSON snapshots by product ID and reports added/removed products, price differences and **published** availability-label changes:

```bash
python3 compare_product_snapshots.py examples/price_before.json examples/price_after.json --threshold 10
```

The script makes **no web requests** and cannot retrieve real storefront prices. To automatically fetch public Product JSON-LD and compare later runs, see the [PAL Competitor Price & Stock Tracker](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta). Check current Apify pricing first.

## Explore the complete public Actor catalog

[Browse every currently published Practical AI Lab Actor by keyword](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html). This free page links directly to each Actor's live Apify listing and current pricing.

## Plan pay-per-event costs before scaling

Use the [free browser-only event-cost estimator](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/pricing-estimator.html) to model hypothetical processing volume and event charges. The inputs are examples, not live pricing. Always read the chosen Actor's Apify Pricing tab.

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

- [Choose between Product JSON-LD extraction, price tracking and schema QA](guides/product-jsonld-extractor-vs-price-tracker.md): compare use cases, inputs, billing and what each Actor actually delivers.
- [Set up repeatable competitor price and stock monitoring](guides/competitor-price-stock-monitoring.md): baseline, repeat comparisons, pricing caveats and safe scheduling. This guide explains how to turn one-off checks into an operational workflow without claiming automatic notifications.
- [Try the free in-browser hreflang checker](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/hreflang-checker.html): paste HTML and check language/region tags locally without sign-up, server calls or fees.
- [Review hreflang language and region tags](guides/hreflang-international-seo-qa.md): international SEO migration QA and static HTML alternates.
- [Review image alt text before a website launch](guides/image-alt-text-audit.md): missing vs. intentionally empty alt attributes, with practical page samples.
- [Audit Open Graph tags for accurate social preview metadata](guides/open-graph-social-preview-qa.md): public HTML tag checks, examples, and exportable QA findings.
- [Extract published Product JSON-LD prices and stock labels](guides/product-jsonld-price-extraction.md): static structured-data snapshots and repeat workflow limits.
- [Bulk ecommerce Product JSON-LD catalog audit](guides/bulk-product-jsonld-catalog-audit.md): sample selection, reviewing findings and scaling to 50-page batches with transparent costs.

- [Audit H1 headings and static HTML structure](guides/h1-heading-structure-qa.md): practical prelaunch checklist for product and content templates.
- [Review SKU, GTIN and MPN identifiers in Product JSON-LD](guides/product-identifiers-sku-gtin-qa.md): distinguish applicable identifiers from missing data without claiming registry authentication.

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