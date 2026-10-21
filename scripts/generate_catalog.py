#!/usr/bin/env python3
"""Generate a static, accessible PAL Apify Store catalog from public listing data.
Publishes only already-public Actors; escapes ALL API-sourced HTML.
No tokens, runs, billing, or changes to Apify.
"""
from __future__ import annotations
import datetime
import html
import json
import pathlib
import re
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE="https://api.apify.com/v2/store?username=practical_ai_lab_jp&limit=100"
actors=[]
seen=set()
offset=0
for page in range(50):
    url=BASE+"&offset="+str(offset)
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"PAL-Public-Catalog-Generator/1.0"}),timeout=20) as response:
        data=json.load(response)["data"]
    batch=data.get("items",[])
    for a in batch:
        if a.get("username")=="practical_ai_lab_jp" and a.get("name") and a["name"] not in seen:
            seen.add(a["name"])
            actors.append(a)
    offset += len(batch)
    total=int(data.get("total",offset))
    if offset>=total:
        break
    if not batch:
        raise RuntimeError("Unexpected empty Apify Store page; refusing incomplete catalog")
else:
    raise RuntimeError("Apify Store pagination exceeds 5000 entries; refusing incomplete catalog")
actors.sort(key=lambda a:(0 if "ECOMMERCE" in (a.get("categories") or []) else 1,(a.get("title") or "").casefold(),a["name"]))
ESC=html.escape
def val(v):
    return ESC(str(v or ""),quote=True)
def strip_html(value):
    value=re.sub(r"<[^>]+>"," ",str(value or ""))
    return re.sub(r"\s+"," ",value).strip()
def card(actor):
    raw_title=str(actor.get("title") or actor["name"])
    raw_desc=strip_html(actor.get("description") or "Focused public-data QA workflow.")
    # Use a word boundary: never publish a broken mid-word product claim.
    display_desc=raw_desc
    if len(raw_desc)>260:
        display_desc=raw_desc[:260].rsplit(" ",1)[0].rstrip(" .,;:")+"…"
    title=val(raw_title)
    desc=val(display_desc)
    categories=actor.get("categories") or []
    badge="Ecommerce" if "ECOMMERCE" in categories else "Developer tools"
    href="https://apify.com/practical_ai_lab_jp/"+urllib.parse.quote(actor["name"],safe="-")
    searchable=val((raw_title+" "+raw_desc+" "+badge).lower())
    return (f'<article class="card" data-search="{searchable}">'
            f'<span class="tag">{badge}</span><h2>{title}</h2><p>{desc}</p>'
            f'<a class="card-link" href="{href}">View features & live pricing ↗</a></article>')
items="\n".join(card(a) for a in actors)
# Useful search-intent links, not claims about ratings, popularity or rank.
workflow_spec=[
    ("Compare published competitor prices", "pal-competitor-price-stock-delta",
     "Monitor public product price and stock-label changes across runs."),
    ("Audit ecommerce Product structured data", "pal-product-stock-schema-check",
     "Check Product/Offer JSON-LD, identifiers and published offer fields."),
    ("Check product names and SKU", "pal-product-name-schema-audit",
     "Review missing product-name and SKU fields in structured data."),
    ("Inspect H1 and heading hierarchy", "pal-h1-heading-checker",
     "Find missing or repeated H1 elements on public HTML pages."),
    ("Review image alt attributes", "pal-image-alt-text-checker",
     "Audit missing or empty image alternatives for accessibility QA."),
    ("Review hreflang annotations", "my-actor-15",
     "Inspect language and region references in static public markup."),
]
workflow_html="\n".join(
    '<li><a href="https://apify.com/practical_ai_lab_jp/'+val(slug)+'">'+val(label)+'</a>'
    '<span>'+val(explainer)+'</span></li>'
    for label,slug,explainer in workflow_spec if slug in seen
)
all_names=[{"@type":"ListItem","position":i,
            "name":a.get("title") or a["name"],
            "url":"https://apify.com/practical_ai_lab_jp/"+urllib.parse.quote(a["name"],safe="-")}
           for i,a in enumerate(actors,1)]
ld={"@context":"https://schema.org","@type":"ItemList",
    "name":"Practical AI Lab public Apify Actors","numberOfItems":len(actors),"itemListElement":all_names}
ld_json=json.dumps(ld,ensure_ascii=False,separators=(",",":")).replace("<",chr(92)+"u003c")
document=f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>All {len(actors)} PAL Ecommerce & Developer QA Tools | Practical AI Lab</title>
<meta name="description" content="Find all {len(actors)} currently public Practical AI Lab Apify Actors for ecommerce product-schema QA, price monitoring, metadata audits and developer automation.">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/catalog.html">
<style>
:root{{color-scheme:dark;font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#0a1020;color:#eaf2fd}}
*{{box-sizing:border-box}}body{{margin:0;line-height:1.55}}
a{{color:#8cd0f1}}.container{{max-width:1140px;margin:auto;padding:0 23px}}
header{{background:#0e192b;border-bottom:1px solid #354a64;padding:18px 0}}
.nav{{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}}
.brand{{color:#eff8ff;font-weight:800;letter-spacing:.035em}}
a:hover{{text-decoration:underline}}.hero{{padding:63px 0 35px;background:radial-gradient(ellipse at top left,#183c60,transparent 65%)}}
h1{{font-size:clamp(2.15rem,5vw,3.3rem);line-height:1.12;margin:0 0 14px;letter-spacing:-.025em}}
.lead{{color:#c5d4e8;max-width:750px;font-size:1.1rem}}
.tag{{display:inline-block;border:1px solid #437580;border-radius:50px;padding:3px 10px;font-size:.76rem;color:#9ce5df}}
.controls{{margin-top:29px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
input{{font:inherit;width:min(100%,530px);padding:13px 15px;border:1px solid #5c7893;border-radius:10px;background:#101f31;color:#eef8ff}}
#count{{color:#bbccdd}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:17px;margin:20px 0 55px}}
.card{{background:#131f31;border:1px solid #30445c;border-radius:15px;padding:22px;display:flex;flex-direction:column}}
[hidden]{{display:none!important}}
.card h2{{font-size:1.11rem;line-height:1.32;margin:12px 0}}
.card p{{color:#bccde0;font-size:.95rem;flex:1}}
.card-link{{font-weight:700;margin-top:12px}}
.workflows{{padding:18px 0 14px}}
.workflows h2{{font-size:1.4rem;margin:0 0 5px}}
.workflows p{{color:#bacbdc;margin:0 0 13px}}
.workflows ul{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;list-style:none;padding:0}}
.workflows li{{border:1px solid #30445c;border-radius:11px;padding:12px 15px}}
.workflows li a{{display:block;font-weight:700}}
.workflows li span{{display:block;color:#bacbdc;font-size:.9rem;margin-top:3px}}
.notes{{border-top:1px solid #253c57;padding:22px 0 50px;color:#bacbdc}}
footer{{background:#0d1727;border-top:1px solid #2c425c;padding:27px 0;color:#c1d1df}}
@media(max-width:790px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media(max-width:560px){{.grid,.workflows ul{{grid-template-columns:1fr}}}}
</style>
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<header><div class="container nav"><div class="brand">PRACTICAL AI LAB</div><nav><a href="./">Free guide & workflows</a> · <a href="product-jsonld-preview.html">Free Product schema preview</a> · <a href="https://apify.com/practical_ai_lab_jp">Apify Store ↗</a></nav></div></header>
<main>
<section class="hero"><div class="container">
<h1>Find a focused tool for your next ecommerce data task.</h1>
<p class="lead">Browse all <strong>{len(actors)}</strong> publicly listed Practical AI Lab Actors. Find schema audits, price monitoring, SEO metadata checks and tools for structured data. Start with a small public example and check each tool's live pricing.</p>
<div class="controls"><label for="search">Search tools:</label><input id="search" type="search" aria-label="Filter PAL tools by keyword" placeholder="Try product, price, schema, H1, stock …"><span id="count" aria-live="polite">{len(actors)} tools</span></div>
</div></section>
<section class="container workflows" aria-labelledby="workflow-title">
<h2 id="workflow-title">Choose a tool for the work you need done</h2>
<p>Need FAQ, BreadcrumbList, JSON-LD syntax, outbound-link or schema-type checks? <a href="schema-audit-quickstart.html">Use five ready-to-copy example inputs</a> before launching a charged run.</p>
<p>Start with a relevant example, verify that it matches your public data, and check the live Apify pricing before running.</p>
<ul>{workflow_html}</ul>
</section>
<section class="container"><div class="grid" id="list">
{items}
</div></section>
<section class="notes"><div class="container">
<h2>Before you run an Actor</h2>
<p>These are public listings, not claims that an Actor can log into stores or verify checkout prices. Most PAL tools inspect <strong>static public HTML or Product JSON-LD</strong>. Pricing, eligibility, input limits, and capabilities vary. Check the current listing and pricing, then start small.</p>
<p>Prefer a no-cost starting point? Try our <a href="product-jsonld-preview.html">free in-browser Product JSON-LD preview</a>, read the <a href="./">offline Product JSON-LD checklist</a>, our <a href="https://github.com/jojoagogog-beep/ecommerce-jsonld-qa-checklist/blob/main/guides/bulk-product-jsonld-catalog-audit.md">catalog migration guide</a>, or use the <a href="pricing-estimator.html">event-cost calculator</a> and <a href="hreflang-checker.html">free hreflang checker</a>.</p>
</div></section>
</main><footer><div class="container">Practical AI Lab · <a href="https://apify.com/practical_ai_lab_jp">Full Apify Store</a> · <a href="https://github.com/jojoagogog-beep/ecommerce-jsonld-qa-checklist">Source and tutorials</a></div></footer>
<script>
const field=document.querySelector("#search");
const cards=[...document.querySelectorAll(".card")];
field.addEventListener("input",()=>{{
 const q=field.value.trim().toLowerCase();
 let n=0;
 cards.forEach(el=>{{const show=el.dataset.search.includes(q);el.hidden=!show;if(show)n++;}});
 document.querySelector("#count").textContent=n+" tools";
}});
</script>
</body></html>
"""
output=ROOT/"catalog.html"
output.write_text(document,encoding="utf-8")
print("CATALOG_GENERATED",len(actors),"at",datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds"),flush=True)
