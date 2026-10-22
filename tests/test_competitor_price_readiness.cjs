"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const mod=require("../scripts/competitor-price-readiness.js");
const inspect=mod.inspect;
const html=fs.readFileSync(path.join(__dirname,"../competitor-price-readiness.html"),"utf8");
assert.match(html,/robots.*index,follow/);
assert.match(html,/scripts\/competitor-price-readiness\.js/);
assert.match(html,/apify\.com\/practical_ai_lab_jp\/pal-competitor-price-stock-delta/);
const js=fs.readFileSync(path.join(__dirname,"../scripts/competitor-price-readiness.js"),"utf8");
assert(!/innerHTML|fetch\s*\(|XMLHttpRequest|sendBeacon|eval\s*\(/.test(js),"no network or DOM insertion");
function check(label,s,expected){
 const x=inspect(s);assert.equal(x.status,expected,label);return x;
}
assert.match(check("Product JSONLD",JSON.stringify({"@type":"Product","name":"Synthetic","offers":{"price":"39.90","priceCurrency":"USD","availability":"https://schema.org/InStock"}}),"Static metadata looks compatible").details,/39.90/);
assert.match(check("zero-price",JSON.stringify({"@type":"Product","offers":{"price":0,"priceCurrency":"USD"}}),"Static metadata looks compatible").details,/price: 0/);
check("OpenGraph",'<meta property="og:type" content="product"><meta property="product:price:amount" content="32.99"><meta property="product:price:currency" content="USD">',"Static metadata looks compatible");
check("OpenGraph untyped",'<meta property="product:price:amount" content="42">',"Not confirmed");
check("Missing currency",JSON.stringify({"@type":"Product","offers":{"price":39}}),"Needs review");
check("Multiple offers",JSON.stringify({"@type":"Product","offers":[{"price":39},{"price":40}]}),"Needs review");
check("Not Product",JSON.stringify({"@type":"Article","headline":"Text"}),"Not confirmed");
check("Graph",JSON.stringify({"@graph":[{"@type":"WebPage"},{"@type":"Product","offers":{"price":9,"priceCurrency":"GBP"}}]}),"Static metadata looks compatible");
check("Nested HTML",'<script type="application/ld+json">'+JSON.stringify({"@type":"Product","offers":{"price":"12","priceCurrency":"JPY"}})+'</script>',"Static metadata looks compatible");
check("Discount unsupported price",JSON.stringify({"@type":"Product","offers":{"price":"$39.90","priceCurrency":"USD"}}),"Needs review");
assert.throws(()=>inspect("x".repeat(525000)),/512 KB/);
assert.throws(()=>inspect('<script type="application/ld+json">{bad}</script>'),/Invalid JSON-LD/);
console.log("PASS 12 competitor price readiness regression checks");
