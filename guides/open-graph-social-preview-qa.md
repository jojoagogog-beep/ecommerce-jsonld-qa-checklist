# Open Graph metadata QA before a product launch

**Avoid blank or misleading link previews when launching an ecommerce storefront.** This checklist covers the Open Graph tags that can be inspected in the published **static HTML**, and explains how to review many public pages with the [PAL Open Graph Meta Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-16) on Apify.

## 1. Understand the basic markup

A typical product page can declare its URL, title, description and share image:

```html
<meta property="og:type" content="product">
<meta property="og:title" content="Blue rain jacket">
<meta property="og:description" content="Waterproof jacket for everyday use">
<meta property="og:url" content="https://example.com/products/blue-jacket">
<meta property="og:image" content="https://example.com/images/blue-jacket.jpg">
```

These are **synthetic examples**, not actual ecommerce URLs. Metadata presence alone cannot guarantee a particular appearance on social platforms; each platform may cache, transform or ignore fields.

## 2. Check what a team can control

- Does `og:title` describe the specific product or category page rather than a generic shop title?
- Is `og:description` useful and consistent with the actual page?
- Does `og:url` point to the preferred page URL?
- Is `og:image` an accessible image the brand is authorized to use? Confirm this separately.
- Are your locale-specific product templates using appropriate text and URLs?
- After template changes, are the new values present in the HTML delivered to a basic HTTP client?

A missing Open Graph tag is a **review item**, not a promise that social sharing or SEO will fail.

## 3. Review multiple public pages

Open the [PAL Open Graph Meta Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-16). Try a small input first:

```json
{
  "urls": [
    "https://scrapeme.live/shop/Pikachu/",
    "https://scrapeme.live/shop/Bulbasaur/"
  ]
}
```

Check the dataset output for missing `og:title`, `og:description`, `og:url` and `og:image` fields. The Actor accepts up to **18 public HTML URLs per run**; export CSV or JSON for a developer or content-team review. Example pages may intentionally omit some social metadata.

**Scope and limitations:** static publicly accessible HTTPS HTML only. The Actor checks source tags but **does not render a real social-network preview** or guarantee a platform will fetch or display the image. Changes to the target website remain the responsibility of its owner.

## 4. Verify after your fixes

1. Fix the product template or CMS source, not just a single example page.
2. Rerun the same public URL list.
3. Confirm that flagged metadata issues no longer appear where you intentionally fixed them.
4. Inspect the final platform preview independently if visual accuracy matters.

Successfully processed pages may incur pay-per-event fees, even if no problem is found. **Check the Actor's live Pricing tab before running**; this guide does not create a run or schedule.

## Related PAL tools

- [Twitter/X Card Meta Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-17) — separately checks Twitter-specific tags.
- [Canonical URL Tag Auditor](https://apify.com/practical_ai_lab_jp/my-actor-13) — compare preferred URLs with published on-page references.
- [Product Image Metadata & Alt Audit](https://apify.com/practical_ai_lab_jp/pal-product-image-schema-audit) — inspect other image-related markup.

[Browse the public PAL Actor catalog](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html).

*Independent Practical AI Lab guidance. Not an endorsement by any social network, platform or search engine.*
