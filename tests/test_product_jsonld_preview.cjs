// Regression tests for the free, browser-only Product JSON-LD preview.
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm");
const html=fs.readFileSync(path.join(__dirname,"../product-jsonld-preview.html"),"utf8");
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/);
assert(script,"inline validator script required");
const source=script[1];
new Function(source);
assert(!/innerHTML|fetch\s*\(|XMLHttpRequest|sendBeacon/.test(source),"no network calls or untrusted HTML injection");
function el(initial=""){return {value:initial,textContent:initial,className:"",children:[],listeners:{},
 replaceChildren(){this.children=[];this.textContent="";},
 appendChild(item){this.children.push(item);},addEventListener(name,fn){this.listeners[name]=fn}};}
const sample=html.match(/<textarea[^>]*>([\s\S]*?)<\/textarea>/);
assert(sample);
const nodes={source:el(sample[1]),status:el(),findings:el(),summary:el(),check:el(),sample:el()};
vm.runInNewContext(source,{document:{getElementById:id=>nodes[id],createElement:tag=>{let node=el();node.tag=tag;return node;}},JSON,Array,String,Number,Error});
function inspect(input){
 nodes.source.value=input;nodes.check.listeners.click();
 return {status:nodes.status.textContent,product:nodes.findings.children[0]};
}
assert.match(nodes.status.textContent,/1 Product record/);
let r=inspect(JSON.stringify({"@type":"Product","name":"Zero-cost sample","offers":{"price":0,"priceCurrency":"USD"}}));
assert.match(r.status,/1 Product record/);
assert(r.product.children.some(x=>/Price: 0 USD/.test(x.textContent)),"zero-price offer must remain visible");
r=inspect(JSON.stringify({"@graph":[{"@type":"WebPage"},{"@type":["Thing","Product"],"name":"Graph item","offers":[{"price":35,"priceCurrency":"USD"},{"price":40,"priceCurrency":"USD"}]}]}));
assert.match(r.status,/1 Product record/);
assert(r.product.children.some(x=>/Multiple offers/.test(x.textContent)));
r=inspect('<html><script type="application/ld+json">'+JSON.stringify({"@type":"Product","name":"HTML Product","offers":{"price":10,"priceCurrency":"USD"}})+'</script></html>');
assert.match(r.status,/1 Product record/);
assert.match(inspect('<script type="application/ld+json">{broken}</script>').status,/invalid JSON/);
assert.match(inspect('<html><main>Hello</main></html>').status,/No application\/ld\+json/);
assert.match(inspect(JSON.stringify({"@type":"BreadcrumbList"})).status,/No schema.org Product/);
assert.match(inspect("x".repeat(525000)).status,/too large/);
nodes.sample.listeners.click();assert.match(nodes.status.textContent,/1 Product record/);
console.log("PASS 9 Product JSON-LD preview regression checks");
