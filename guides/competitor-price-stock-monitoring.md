# Repeatable competitor price & stock monitoring

A practical workflow for ecommerce pricing teams, catalog managers, and developers who want to compare **published** product price and availability data over time.

This tutorial uses [PAL Competitor Price & Stock Tracker on Apify](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta). It reads public static HTML, preferring `schema.org/Product` / `Offer` JSON-LD and, when absent, strictly product-typed Open Graph price metadata with validated numeric amounts and currency. It does not verify checkout prices, warehouse stock, store login or JavaScript-rendered storefronts.

## Free first-run price comparison

Use the [free browser price-gap calculator](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/competitor-price-calculator.html) to compare your own reference price with a competitor's published price without signup or paid Actor use. It runs locally in the browser, and the example prices are fictitious.

The hosted PAL Actor also supports an optional `referencePrices` map so you can obtain a useful comparison **on your first paid run**, even before change history exists:

```json
{
  "urls": ["https://api.apify.com/v2/key-value-stores/DHMHtotPcN9CAKXYj/records/pal-open-graph-product-price-20261021.html"],
  "monitorId": "example-reference-gap",
  "referencePrices": {
    "https://api.apify.com/v2/key-value-stores/DHMHtotPcN9CAKXYj/records/pal-open-graph-product-price-20261021.html": {
      "price": 45,
      "currency": "USD"
    }
  }
}
```

This synthetic page initially publishes USD 39.90, so a comparison against USD 45 is 11.33% lower when the page stays unchanged. The Actor skips reference comparison when the page has multiple offers or its currency does not match. It does not convert currencies or recommend a selling price. **Successful priced product checks may still be billed**, including unchanged checks, and a run-start charge may apply. Check the [live Pricing tab](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta) before running.

## 0. Try offline comparisons for free

You can explore the workflow without running a paid Actor. Download the [free local snapshot comparison tool](../compare_product_snapshots.py) and two synthetic example files. Run:

```bash
python3 compare_product_snapshots.py examples/price_before.json examples/price_after.json --threshold 10
```

The script detects price moves, availability-label differences and added/removed products in two **local** JSON arrays. It does not retrieve current competitor data, check stock in warehouses, send alerts or consume Apify credits. The hosted PAL Actor adds public-page fetching, persistent baseline handling and a dataset workflow.

## 1. Establish your first baseline

Open the [public example task](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta/examples/track-competitor-product-prices-and-stock) and inspect its input. Replace the sample URL with your public product-page URLs. A minimal example is:

```json
{
  "urls": ["https://scrapeme.live/shop/Pikachu/"],
  "monitorId": "my-catalog-group",
  "resetBaseline": false,
  "emitUnchanged": true,
  "minPriceChangePercent": 5
}
```

The first successful run creates a comparison baseline for `monitorId`. **No price change can be inferred from a first-ever baseline.**

## 2. Compare across later runs

Reuse the **same `monitorId`** and product URLs. To focus on significant price movements:

```json
{
  "urls": ["https://scrapeme.live/shop/Pikachu/"],
  "monitorId": "my-catalog-group",
  "resetBaseline": false,
  "emitUnchanged": false,
  "minPriceChangePercent": 10
}
```

When `emitUnchanged=false`, unchanged rows are omitted but **may still be billed** because the pages were processed. `minPriceChangePercent` controls the output's `alertSignal` threshold; it **does not deliver a notification** by itself.

## 3. Make it useful in real operations

1. Run a small sample and verify the target pages expose static Product/Offer JSON-LD or explicitly product-typed Open Graph price metadata.
2. Use Apify's Schedule functionality for checks at a cadence that justifies the expense.
3. Send actionable output to a supported webhook or downstream integration if you need notifications.
4. Review dataset rows and export CSV/JSON for reporting or API integrations.
5. Confirm the current **Pricing** tab and actual costs before increasing URL counts or run frequency.

A recurring schedule triggers repeated work, which can incur recurring Apify charges. Nothing in this tutorial creates or activates a schedule for you.

## Troubleshooting and limitations

- New `monitorId` on every run → unrelated baselines, not useful deltas.
- `resetBaseline=true` → comparison history resets for that group.
- Pages with only JavaScript-rendered prices and no supported static product metadata → the Actor cannot retrieve those prices.
- `alertSignal=true` → a dataset field, not an SMS or email.
- Published `InStock` labels → not verified inventory.
- `emitUnchanged=false` → smaller dataset, not necessarily lower processing charges.

## Other PAL tools

- [Bulk product schema QA](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check): audit up to 50 static product pages.
- [Current price and availability extractor](https://apify.com/practical_ai_lab_jp/my-actor): export published Product JSON-LD fields.
- [Product Offer currency QA](https://apify.com/practical_ai_lab_jp/pal-product-offer-currency-check): review price/currency metadata.

Start with the [free offline JSON-LD checklist](../README.md) if you do not need hosted processing.

*Practical AI Lab. This educational workflow does not guarantee revenue, ranking, inventory or pricing outcomes.*