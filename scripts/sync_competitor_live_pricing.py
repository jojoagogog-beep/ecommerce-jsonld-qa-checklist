#!/usr/bin/env python3
"""Read-only Apify price-to-public-page sync for PAL competitor price monitor.

No Store writes, no Actor runs, no fake promotional claims. Fail closed
if price shape changes; the public page is left unchanged.
"""
from __future__ import annotations
from decimal import Decimal,InvalidOperation
from html import escape
from pathlib import Path
import json,re,ssl,urllib.request
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"competitor-price-tracker.html"
API="https://api.apify.com/v2/actors/Tif3ano7veFzfdOTk"
BASE="https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta"
CTX=ssl.create_default_context(cafile="/etc/ssl/cert.pem")
BEGIN="<!-- PAL-ACTOR-PRICING:BEGIN -->"
END="<!-- PAL-ACTOR-PRICING:END -->"
ORDER=["FREE","BRONZE","SILVER","GOLD","PLATINUM","DIAMOND"]
def get_prices():
    req=urllib.request.Request(API,headers={"User-Agent":"PAL-Live-Price-ReadOnly-Sync/1.0"})
    with urllib.request.urlopen(req,timeout=19,context=CTX) as res:
        info=json.load(res)["data"]
    if info.get("name")!="pal-competitor-price-stock-delta" or info.get("isPublic") is not True:
        raise ValueError("Price API returned wrong or unpublished Actor")
    profiles=info.get("pricingInfos") or []
    if not profiles or profiles[-1].get("pricingModel")!="PAY_PER_EVENT":
        raise ValueError("Unsupported pricing model: refusing stale pricing")
    events=profiles[-1]["pricingPerEvent"]["actorChargeEvents"]
    if set(events)!={"product-check","apify-actor-start"}:
        raise ValueError("Unexpected charge events")
    product=events["product-check"];start=events["apify-actor-start"]
    run=Decimal(str(start["eventPriceUsd"]))
    if run<=0 or run>Decimal("0.1"):raise ValueError("Unexpected run-start price")
    tiers=product.get("eventTieredPricingUsd")
    if tiers:
        prices={t:Decimal(str((tiers.get(t) or {})["tieredEventPriceUsd"])) for t in ORDER}
        if any(x<=0 or x>Decimal("0.1") for x in prices.values()):
            raise ValueError("Tier prices outside expected bounds")
        if prices["FREE"]<prices["GOLD"]:
            raise ValueError("Invalid tier discount progression")
        tiered=True
    else:
        prices={"FREE":Decimal(str(product["eventPriceUsd"]))}
        if prices["FREE"]<=0 or prices["FREE"]>Decimal("0.1"):
            raise ValueError("Invalid standard price")
        tiered=False
    return {"run":run,"prices":prices,"tiered":tiered}
def usd(value):
    return "USD "+format(value.quantize(Decimal("0.00000001")).normalize(),"f")
def build_section(prices):
    regular=prices["prices"]["FREE"]
    rows=[f"<tr><td>{n} product URL{'s' if n!=1 else ''}, once</td><td>{n} priced-product event{'s' if n!=1 else ''}, 1 run start</td><td>{escape(usd(n*regular+prices['run']))}</td></tr>" for n in (1,5,50)]
    if prices["tiered"]:
        blocks=[]
        for tier in ORDER:
            current=prices["prices"][tier]
            percent=100*(1-current/regular)
            label= "standard price" if tier=="FREE" else str(int(percent.quantize(Decimal('1'))))+"% below standard"
            blocks.append(f"<tr><td>{escape(tier.title())}</td><td>{escape(usd(current))}</td><td>{escape(label)}</td></tr>")
        tier_detail='<h3>Current plan-specific per-product event rates</h3><table><thead><tr><th>Apify plan</th><th>Published product event</th><th>Comparison</th></tr></thead><tbody>'+''.join(blocks)+'</tbody></table><p>These discounts are shown only after the current Apify API confirms them. They apply to eligible plan-specific event pricing; account plans and usage costs may vary.</p>'
    else:
        tier_detail="<p><strong>No plan-specific tier discounts are confirmed in the current public Actor API response.</strong> Any proposed promotion should not be treated as live until Apify displays it.</p>"
    return (BEGIN+'\n<section><div class="wrap">\n'
        '<h2>What will a run cost?</h2>\n'
        '<p>Published Apify pricing checked during this page\'s automated catalog sync: '
        f'<strong>{escape(usd(regular))} per successfully processed priced-product event</strong>, '
        f'plus <strong>{escape(usd(prices["run"]))} per run-start event</strong>. '
        'A URL can contain zero, one, or multiple product offers; the calculations below assume exactly one billable product event per URL.</p>\n'
        '<table><thead><tr><th>Illustrative check</th><th>Event assumption</th><th>Standard event fees</th></tr></thead><tbody>\n'
        +'\n'.join(rows)+'</tbody></table>\n'+tier_detail+'\n'
        f'<aside><strong>Always verify <a href="{BASE}">current Apify Pricing</a> before executing.</strong> '
        'Actual event counts, add-on usage, proxy/storage costs and future pricing may differ. '
        'The figures are examples, not a binding quote.</aside>\n'
        '<p>Want to estimate your workflow? '
        '<a href="workflow-time-savings.html">Calculate possible manual time savings and costs</a> '
        'or <a href="pricing-estimator.html">use the Apify event-fee calculator</a>.</p>\n'
        '</div></section>\n'+END)
def main():
    data=get_prices()
    current=FILE.read_text()
    replacement=build_section(data)
    if current.count(BEGIN)==1 and current.count(END)==1:
        a=current.index(BEGIN);b=current.index(END,a)+len(END)
        new=current[:a]+replacement+current[b:]
    else:
        start='<section><div class="wrap">\n<h2>What will a run cost?</h2>'
        if current.count(start)!=1:raise RuntimeError("Legacy pricing section anchor missing")
        a=current.index(start)
        next_section=current.find('<section><div class="wrap">',a+len(start))
        if next_section<0:raise RuntimeError("Missing next content section")
        new=current[:a]+replacement+'\n'+current[next_section:]
    if new!=current:FILE.write_text(new)
    print("PAL_LIVE_PRICE_SYNC",json.dumps({"tieredDiscountVerified":data["tiered"],
     "regularPerProductUsd":str(data["prices"]["FREE"]),
     "runStartUsd":str(data["run"]),
     "publishedPriceTiers":{k:str(v) for k,v in data["prices"].items()},
     "siteFileChanged":new!=current}),flush=True)
if __name__=="__main__":main()
