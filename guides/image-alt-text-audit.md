# Image alt text QA before an ecommerce website launch

**Make product images easier to review across an entire storefront template.** This checklist is for accessibility-oriented content teams and developers who need an evidence-based review of published HTML `alt` attributes. It does **not** certify WCAG compliance.

## 1. Understand the difference between missing and empty

A meaningful product photo may need a useful accessible alternative:

```html
<img src="/products/blue-jacket-front.jpg" alt="Front view of a blue rain jacket">
```

An intentionally decorative separator may correctly use an empty alternative:

```html
<img src="/decorations/divider.svg" alt="">
```

An image with no `alt` attribute at all is a different case:

```html
<img src="/products/blue-jacket-front.jpg">
```

**Important:** An empty `alt` is not necessarily a defect. The image's purpose, surrounding text and assistive-technology context determine the right decision. Automated tools generate review candidates, not final accessibility judgments.

## 2. Choose representative website pages

For a meaningful prelaunch review, select pages with different image patterns:

- A standard ecommerce product-detail page with gallery images.
- A product variant or color selector with thumbnail images.
- Collection pages with product cards.
- Marketing banners, icons and truly decorative graphics.
- Template pages where CMS editors supplied or omitted alternative text.

Review whether meaningful images have concise, accurate labels, not repeated keyword strings. Avoid adding product names indiscriminately to every decoration.

## 3. Run a small public sample

Use the [PAL Image Alt Text Checker](https://apify.com/practical_ai_lab_jp/pal-image-alt-text-checker) for up to 18 public HTTPS URLs:

```json
{"urls":["https://scrapeme.live/shop/Pikachu/"]}
```

The sample page is only for demonstration. Replace it with public pages you are authorized to assess. Review `issues`, `issueCount` and `details`, and export the Dataset as CSV/JSON to triage work by template. After content editors make changes, rerun the same URLs.

**Limits:** This checks attributes in static public HTML. It cannot render JavaScript-generated images, evaluate every accessibility technique, test screen readers, or fix your site. Successfully processed URLs can incur pay-per-event charges; review the live [Pricing tab](https://apify.com/practical_ai_lab_jp/pal-image-alt-text-checker).

## 4. Related metadata checks

For an ecommerce product's **structured image metadata**, use the separate [PAL Product Image Metadata & Alt Audit](https://apify.com/practical_ai_lab_jp/pal-product-image-schema-audit), which also reviews Product JSON-LD image URLs and Open Graph image presence.

For other page QA, see [H1 Heading Checker](https://apify.com/practical_ai_lab_jp/pal-h1-heading-checker) and [Open Graph Tag Checker](https://apify.com/practical_ai_lab_jp/my-actor-16). These are independent tools, not a required bundle.

Use the [complete PAL Actor catalog](https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html) to match a specific job to an Actor and its live pricing.

*Practical AI Lab — educational metadata QA, not a certification or ranking guarantee.*
