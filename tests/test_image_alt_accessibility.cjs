const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { check, findImgTags, parseAttributes } = require("../assets/image-alt-auditor.js");
const root = path.join(__dirname, "..");
const tests = [
  ["missing attribute", '<img src="product.jpg">', {total:1,missing:1,empty:0,weak:0,present:0}],
  ["empty decorative", '<img src="border.svg" alt="">', {total:1,missing:0,empty:1,weak:0,present:0}],
  ["whitespace alt", '<img src="border.svg" alt="   ">', {total:1,missing:0,empty:1,weak:0,present:0}],
  ["valid text", '<img src="coat.jpg" alt="Warm blue winter coat folded on shelf">', {total:1,missing:0,empty:0,weak:0,present:1}],
  ["weak generic", '<IMG SRC="main.png" ALT="image">', {total:1,missing:0,empty:0,weak:1,present:0}],
  ["filename label", '<img src="main.png" alt="IMG_1234.jpg">', {total:1,missing:0,empty:0,weak:1,present:0}],
  ["HTML comments ignored", '<!-- <img src="tracking.jpg"> --> <img alt="Red backpack" src="a.jpg">', {total:1,missing:0,empty:0,weak:0,present:1}],
  ["script content ignored", '<script>const snippet = "<img src=never.jpg>";</script><img alt="Result photo">', {total:1,missing:0,empty:0,weak:0,present:1}],
  ["style content ignored", '<style>body::after{content:"<img src=never.jpg>"}</style><img alt="">', {total:1,missing:0,empty:1,weak:0,present:0}],
  ["quoted > in alt", '<img src="test.png" alt="Price > 25 euros">', {total:1,missing:0,empty:0,weak:0,present:1}],
  ["unquoted attributes", '<img src=a.png alt=Photo>', {total:1,missing:0,empty:0,weak:1,present:0}],
  ["multiline tags", '<img\n  src="product.png"\n  alt="Orange running shoes">', {total:1,missing:0,empty:0,weak:0,present:1}],
  ["srcset only", '<img srcset="x.png 1x, x2.png 2x" alt="Blue car">', {total:1,missing:0,empty:0,weak:0,present:1}],
  ["nothing in HTML", '<div>There are no images</div>', {total:0,missing:0,empty:0,weak:0,present:0}],
  ["nested no internet", '<img src="https://invalid.test/side-effect.png" alt="A map of Europe">', {total:1,missing:0,empty:0,weak:0,present:1}],
];
for (const [label,input,expected] of tests) {
  const actual = check(input);
  for (const [k,v] of Object.entries(expected)) assert.equal(actual[k],v, label+": "+k);
}
const page = fs.readFileSync(path.join(root,"image-alt-accessibility-audit.html"),"utf8");
const sitemap = fs.readFileSync(path.join(root,"sitemap.xml"),"utf8");
assert(page.includes('src="assets/image-alt-auditor.js"'));
assert(page.includes("image_accessibility_audit"));
assert(page.includes("No image fetches"));
assert(page.includes("Pricing"));
assert(page.includes('id="source"'));
assert(page.includes('href="https://apify.com/practical_ai_lab_jp/pal-image-alt-text-checker'));
assert(sitemap.includes("/image-alt-accessibility-audit.html"));
assert(!fs.readFileSync(path.join(root,"assets/image-alt-auditor.js"),"utf8").includes("fetch("));
assert(!fs.readFileSync(path.join(root,"assets/image-alt-auditor.js"),"utf8").includes("new Image"));
console.log("PASS",tests.length,"local image alt audit edge cases + page, sitemap and no-network integration checks");
