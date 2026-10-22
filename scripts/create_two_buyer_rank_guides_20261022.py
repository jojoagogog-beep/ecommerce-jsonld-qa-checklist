#!/usr/bin/env python3
"""Write two distinct, factual buyer-intent guides for weak generic search terms."""
from pathlib import Path
import json,html
BASE="https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/"
ROOT=Path(__file__).resolve().parents[1]
guides=[
{
"slug":"ecommerce-price-tracker-workflow.html",
"title":"Ecommerce Price Tracker: Compare Public Product Prices | PAL",
"description":"Practical ecommerce price monitoring for public HTML product pages: one-time comparison, later price deltas, limits and a real Apify example task.",
"eyebrow":"For retail price analysts",
"h1":"Ecommerce price tracking starts with the right product data.",
"lead":"A price tracker is only useful when it can identify a comparable published product offer. This guide explains the small, verifiable workflow supported by PAL on Apify before you schedule repeated checks.",
"kind":"Compare first, monitor later",
"source":"https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta",
"label":"Open price-tracking Actor and current Pricing",
"sections":[
("Confirm the public data source first",
 "Check that your target page is publicly accessible through HTTPS and contains a usable static Product/Offer JSON-LD price, or product-typed Open Graph price tags. Pages whose prices exist only after login, checkout or JavaScript rendering are outside the tool's supported scope. Use the free compatibility tester before paying for a run.",
 [("Try the free compatibility tester","competitor-price-readiness.html"),("Prepare a valid JSON input locally","competitor-tracker-input-builder.html")]),
("Get an initial comparison instead of an empty history",
 "Set your own product reference price using the optional referencePrices field, with the exact target URL and the same currency as the competitor's declared price. On its first run, the Actor can compare your reference price with that published competitor price. It does not advise a profitable price or verify shipping, taxes or promotions.",
 [("Inspect the published first-run example","https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta/examples/track-product-prices-from-open-graph-tags")]),
("Recheck the same product and monitor identifier",
 "Keep monitorId consistent across subsequent runs and compare the Actor's published price and availability-label observations over time. Review output in CSV or JSON. The Actor reports signals in data; it does not send automatic notifications or prove physical stock.",
 [("Read the monitoring setup and limitations","competitor-price-tracker.html")]),
("Estimate cost before adding more pages",
 "A single run and its processed offers may each incur separate pay-per-event charges. The Actor supports up to 50 public product URLs per run, but charges and limits can change. Start small, inspect the output and live Pricing tab, then decide whether a repeat schedule has economic value.",
 [("Model hypothetical per-event charges","pricing-estimator.html")])],
"notfor":"JavaScript-only prices, login-protected portals, checkout-exclusive discounts, live inventory confirmation, automatic alert delivery, guaranteed price savings or sales growth.",
"seealso":"product-jsonld-extraction-workflow.html",
"seealsoLabel":"Need a one-time Product JSON-LD export instead of a tracker?"
},
{
"slug":"product-jsonld-extraction-workflow.html",
"title":"Product JSON-LD Extractor: Export Price, SKU and Stock Labels | PAL",
"description":"How to extract published Product JSON-LD from ecommerce URLs for CSV/JSON catalog review, with a verified Apify example and clear limits.",
"eyebrow":"For catalog operations and feed QA",
"h1":"Extract product JSON-LD data before you compare or migrate catalogs.",
"lead":"One-time extraction is different from competitor price monitoring. Use this workflow to collect public Product JSON-LD fields for a catalog review without requesting admin access to a shop.",
"kind":"One-time structured product export",
"source":"https://apify.com/practical_ai_lab_jp/my-actor",
"label":"Open Product JSON-LD Extractor and current Pricing",
"sections":[
("Check whether the page actually declares Product JSON-LD",
 "Inspect application/ld+json script tags for a Product item and a published Offer. The Actor extracts declared price, currency, SKU, brand and advertised stock labels from static public product pages. It does not create missing Product data or access commerce accounts.",
 [("Check a Product JSON-LD sample in your browser","product-jsonld-preview.html")]),
("Start with one public URL, then increase batch size",
 "Before using up to 50 public product URLs in one run, open the published example task and inspect its prefilled input. Replace synthetic URLs with permitted public pages. One small test is better than paying for a large batch whose pages do not expose useful metadata.",
 [("Open the public one-URL extraction example","https://apify.com/practical_ai_lab_jp/my-actor/examples/extract-product-price-and-stock-from-one-url")]),
("Review exported fields before import",
 "Inspect the returned CSV/JSON for product name, available identifiers, brand, currency, declared price and advertised availability labels. Missing values need manual investigation; they are not proof of a data corruption or a real out-of-stock condition. Compare source URLs and currencies before merging feed records.",
 [("Review a batch CSV workflow example","https://apify.com/practical_ai_lab_jp/my-actor/examples/extract-product-prices-sku-stock-to-csv")]),
("Choose the correct next tool",
 "If your job is to find missing Product/Offer metadata across storefront templates, use the Product Schema QA checker. If you need later competitor-price changes and first-run reference-price comparison, use the dedicated Competitor Price Tracker. A one-time extractor is not a historical tracker.",
 [("Choose between the three jobs","tool-finder.html"),("Browse all published PAL tasks","example-tasks.html")])],
"notfor":"Live checkout stock, authenticated admin feeds, JavaScript-only shopping prices, competitor history without repeat monitoring, and guaranteed Google rich-result eligibility.",
"seealso":"ecommerce-price-tracker-workflow.html",
"seealsoLabel":"Need a recurring ecommerce price tracker instead of extraction?"
}
]
css='''<style>:root{color-scheme:dark;--bg:#0b1727;--fg:#f0f7ff;--mute:#bed0df;--mint:#86e1c3}*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);font:16px/1.67 system-ui,-apple-system,Segoe UI,sans-serif;margin:0}a{color:#a7dcff}a:focus-visible{outline:3px solid var(--mint);outline-offset:4px}.wrap{max-width:980px;padding:0 22px;margin:auto}header,footer{border-bottom:1px solid #344a5e}header nav{display:flex;gap:19px;flex-wrap:wrap;align-items:center;padding:18px 0}.brand{margin-right:auto;font-weight:850;letter-spacing:.07em}h1{font-size:clamp(33px,5vw,54px);line-height:1.13;letter-spacing:-.03em;max-width:900px}h2{font-size:26px;line-height:1.3}p{color:var(--mute)}.hero{padding:66px 0 47px}.eyebrow{color:var(--mint);font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.09em}.lead{font-size:19px;max-width:800px}.cta{display:inline-block;background:var(--mint);padding:14px 20px;border-radius:9px;color:#042f38;text-decoration:none;font-weight:850;margin:15px 0}article{padding:25px 0;border-top:1px solid #344a5e}article ul{padding-left:21px}li{margin:8px 0}.limitations{border:1px solid #476577;border-radius:12px;padding:21px;background:#14293e;margin:25px 0 42px}footer{border-top:1px solid #344a5e;border-bottom:none;padding:25px 0;font-size:13px;color:var(--mute)}@media(max-width:600px){.hero{padding-top:40px}h1{font-size:35px}}</style>'''
for g in guides:
 url=BASE+g["slug"];q=lambda s:html.escape(s,quote=True)
 product=g["source"]+"?utm_source=pal_github_pages&utm_medium=organic&utm_campaign="+g["slug"].replace(".html","")
 parts=[]
 for heading,body,links in g["sections"]:
  links_html="".join('<li><a href="'+q(link)+'">'+q(label)+' ↗</a></li>' for label,link in links)
  parts.append("<article><h2>"+q(heading)+"</h2><p>"+q(body)+"</p><ul>"+links_html+"</ul></article>")
 jsonld=json.dumps({"@context":"https://schema.org","@type":"HowTo","name":g["h1"],"description":g["description"],"step":[{"@type":"HowToStep","name":h,"text":b} for h,b,links in g["sections"]],"publisher":{"@type":"Organization","name":"Practical AI Lab"}},ensure_ascii=False).replace("<","\\u003c")
 source='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+q(g["title"])+'''</title><meta name="description" content="'''+q(g["description"])+'''"><meta name="robots" content="index,follow"><link rel="canonical" href="'''+q(url)+'''"><meta property="og:type" content="article"><meta property="og:title" content="'''+q(g["title"])+'''"><meta property="og:description" content="'''+q(g["description"])+'''"><meta property="og:url" content="'''+q(url)+'''"><script type="application/ld+json">'''+jsonld+'''</script>'''+css+'''</head><body>
<header><nav class="wrap"><span class="brand">PRACTICAL AI LAB</span><a href="./">Home</a><a href="tool-finder.html">Choose a tool</a><a href="catalog.html">All public Actors</a></nav></header>
<main><section class="hero wrap"><p class="eyebrow">'''+q(g["eyebrow"])+''' · '''+q(g["kind"])+'''</p><h1>'''+q(g["h1"])+'''</h1><p class="lead">'''+q(g["lead"])+'''</p><a class="cta" href="'''+q(product)+'''">'''+q(g["label"])+''' ↗</a><p>Viewing the Store page is free. Running an Actor may incur usage/event charges. Check its live Pricing tab.</p></section>
<section class="wrap">'''+''.join(parts)+'''<aside class="limitations"><h2>What this workflow does not do</h2><p>'''+q(g["notfor"])+'''</p><p><a href="'''+q(g["seealso"])+'''">'''+q(g["seealsoLabel"])+''' ↗</a></p></aside>
<a class="cta" href="'''+q(product)+'''">'''+q(g["label"])+''' ↗</a><p>No claims of guaranteed ranking, paid users, savings or revenue. Verify supported input, current pricing and outputs before scaling.</p></section></main><footer><div class="wrap">Practical AI Lab · Practical public-page QA guidance · October 2026</div></footer></body></html>'''
 path=ROOT/g["slug"]
 path.write_text(source)
 assert len(parts)==4
 print("UNIQUE_BUYER_GUIDE_CREATED",path.name,"BYTES",len(source))
