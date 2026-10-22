const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {check}=require('../assets/h1-heading-auditor.js');
const inputs=[
 ['none','<main><h2>Overview</h2></main>',0,1,0],
 ['normal','<h1>My catalog</h1>',1,0,0],
 ['multiple','<h1>A</h1><h1>B</h1>',2,1,0],
 ['empty','<h1></h1>',1,1,1],
 ['whitespace','<h1>  <span> </span>  </h1>',1,1,1],
 ['nested','<h1>Boots <strong>and coats</strong></h1>',1,0,0],
 ['script ignored','<script>const html="<h1>Fake</h1>";</script><h1>Real</h1>',1,0,0],
 ['style ignored','<style>content:"<h1>Fake</h1>"</style><h1>Real</h1>',1,0,0],
 ['comments ignored','<!--<h1>Fake</h1>--><h1>Real</h1>',1,0,0],
 ['unclosed','<h1>Incomplete',1,1,0],
 ['mixed case','<H1>Large title</H1>',1,0,0],
 ['textarea ignored','<textarea><h1>Fake</h1></textarea><h1>Real</h1>',1,0,0]
];
for(const [label,html,total,issues,empty] of inputs){
 const d=check(html);
 assert.equal(d.total,total,label+':total');
 assert.equal(d.issues.length,issues,label+':issues');
 assert.equal(d.empty,empty,label+':empty');
}
const root=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(root,'h1-heading-structure-audit.html'),'utf8');
const site=fs.readFileSync(path.join(root,'sitemap.xml'),'utf8');
assert(page.includes('src="assets/h1-heading-auditor.js"'));
assert(page.includes('https://apify.com/practical_ai_lab_jp/pal-h1-heading-checker'));
assert(page.includes('h1_heading_audit'));
assert(page.includes('Multiple H1 headings are not automatically'));
assert(site.includes('h1-heading-structure-audit.html'));
assert(!fs.readFileSync(path.join(root,'assets/h1-heading-auditor.js'),'utf8').includes('fetch('));
console.log('PASS',inputs.length,'H1 HTML audit cases + no-fetch and Apify Store link checks');
