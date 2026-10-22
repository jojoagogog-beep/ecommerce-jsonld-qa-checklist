#!/usr/bin/env python3
"""Extend public no-cost QA quickstart from five to ten verified Actors."""
import json,pathlib,html
ROOT=pathlib.Path(__file__).resolve().parent.parent
PAL=pathlib.Path.home()/"Projects/pal-actor-catalog50/growth"
p=ROOT/"schema-audit-quickstart.html"
txt=p.read_text()
staged=json.loads((PAL/"pal_five_placeholder_example_replacements_staged_20261021.json").read_text())
qa=json.loads((PAL/"pal_html_navigation_audit_demo_local_verified_20261022.json").read_text())
assert len(staged["affectedSlugs"])==10 and len(qa["checks"])==5
assert "Five focused audits." in txt and txt.count('class="card"')==5
reps={
'5 Free Schema Audit Examples | Practical AI Lab Apify Quickstart':'10 Free Website QA Examples | Practical AI Lab Apify Quickstart',
'Get ready-to-paste example inputs for PAL FAQ schema, BreadcrumbList, external link security, JSON-LD syntax and schema type Actors. Public demo, no paid run to prepare.':'Copy ten verified synthetic example inputs for Practical AI Lab Apify Actors: schema, FAQ, links, metadata, sitemap and navigation. Free to prepare; check live pricing before running.',
'5 Ready-to-Paste Schema QA Example Inputs | Practical AI Lab':'10 Ready-to-Paste Website QA Example Inputs | Practical AI Lab',
'Explore five focused website QA tools and prepare their first input with verified synthetic data.':'Explore ten focused website QA tools and prepare their first input using verified synthetic pages.',
'Five focused audits. One working public example.':'Ten focused audits. Two verified public examples.',
'Prepare an input for five Apify website quality checks using one verified synthetic demonstration page.':'Prepare inputs for ten Apify website quality checks using two verified synthetic demonstration pages.',
'It includes BreadcrumbList and FAQPage JSON-LD, plus examples of outbound links.':'One includes BreadcrumbList and FAQPage JSON-LD with outbound links. The other includes language and viewport declarations, pagination, sitemap links and intentionally duplicate metadata.',
'First <a href="examples/pal-structured-data-audit-demo.html">inspect the synthetic source page</a>.':'First inspect the <a href="examples/pal-structured-data-audit-demo.html">schema demonstration</a> or the <a href="examples/pal-html-navigation-qa-demo.html">HTML navigation and metadata demonstration</a>.'
}
for a,b in reps.items():
 assert txt.count(a)==1,(a,txt.count(a))
 txt=txt.replace(a,b)
extra=[
 ("pal-mobile-viewport-checker","Mobile viewport metadata","Check a static viewport declaration and detect a missing device-width setting."),
 ("pal-sitemap-link-discovery","Sitemap link discovery","Find public sitemap link references in page HTML without crawling the whole website."),
 ("pal-html-language-checker","HTML language declaration","Inspect a document's declared language and detect absent or malformed language codes."),
 ("pal-duplicate-meta-detector","Duplicate metadata detector","Detect the two deliberately duplicated meta description tags on the synthetic page."),
 ("pal-pagination-link-checker","Pagination link audit","Review declared rel=next and rel=prev links in static HTML.")
]
expected={a["actor"] for a in qa["checks"]}
assert expected=={a[0] for a in extra}
out=[]
for slug,title,detail in extra:
 url=staged["fixtureBySlug"][slug]
 assert url.endswith("pal-html-navigation-qa-demo.html")
 sample=json.dumps({"urls":[url]},separators=(",",":"))
 out.append('<article class="card" data-slug="'+html.escape(slug)+'">\n'
    '<h2>'+html.escape(title)+'</h2><p>'+html.escape(detail)+'</p>\n'
    '<pre class="example" aria-label="'+html.escape(title)+' sample input">'+html.escape(sample)+'</pre>\n'
    '<div class="actions"><button type="button" class="copy">Copy sample JSON</button>'
    '<a href="https://apify.com/practical_ai_lab_jp/'+slug+'">Open Actor &amp; live Pricing ↗</a></div></article>\n')
close='</div>\n<p id="feedback" role="status" aria-live="polite"></p>'
assert txt.count(close)==1
txt=txt.replace(close,''.join(out)+close)
assert txt.count('class="card"')==10
p.write_text(txt)
print("EXTENDED_TO_TEN_LOCAL",p)
