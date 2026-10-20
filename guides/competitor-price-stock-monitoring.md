# Repeatable competitor price & stock monitoring

A practical workflow for ecommerce pricing teams, catalog managers, and developers who want to compare **published** product price and availability data over time.

This tutorial uses [PAL Competitor Price & Stock Tracker on Apify](https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta). It reads static `schema.org/Product` / `Offer` JSON-LD from public HTTPS product pages. It does not confirm checkout prices or warehouse stock, log in to shops, or render JavaScript storefronts.

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

1. Run a small sample and verify that your target pages expose static Product/Offer JSON-LD.
2. Use Apify's Schedule functionality for checks at a cadence that justifies the expense.
3. Send actionable output to a supported webhook or downstream integration if you need notifications.
4. Review dataset rows and export CSV/JSON for reporting or API integrations.
5. Confirm the current **Pricing** tab and actual costs before increasing URL counts or run frequency.

A recurring schedule triggers repeated work, which can incur recurring Apify charges. Nothing in this tutorial creates or activates a schedule for you.

## Troubleshooting and limitations

- New `monitorId` on every run → unrelated baselines, not useful deltas.
- `resetBaseline=true` → comparison history resets for that group.
- Dynamic-only data without JSON-LD → results may be missing or incomplete.
- `alertSignal=true` → a dataset field, not an SMS or email.
- Published `InStock` labels → not verified inventory.
- `emitUnchanged=false` → smaller dataset, not necessarily lower processing charges.

## Other PAL tools

- [Bulk product schema QA](https://apify.com/practical_ai_lab_jp/pal-product-stock-schema-check): audit up to 50 static product pages.
- [Current price and availability extractor](https://apify.com/practical_ai_lab_jp/my-actor): export published Product JSON-LD fields.
- [Product Offer currency QA](https://apify.com/practical_ai_lab_jp/pal-product-offer-currency-check): review price/currency metadata.

Start with the [free offline JSON-LD checklist](../README.md) if you do not need hosted processing.

*Practical AI Lab. This educational workflow does not guarantee revenue, ranking, inventory or pricing outcomes.*
