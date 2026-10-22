#!/usr/bin/env python3
"""Generate a truthful, public-only Apify Example Tasks buyer directory.
No Actor runs, task writes, requests for private task inputs, or paid services.
"""
from __future__ import annotations
import datetime,html,json,pathlib,ssl,urllib.parse,urllib.request
from zoneinfo import ZoneInfo
ROOT=pathlib.Path(__file__).resolve().parents[1]
TOKEN=(pathlib.Path.home()/".apify/pal_automation_token").read_text().strip()
CTX=ssl.create_default_context(cafile="/etc/ssl/cert.pem")
def api(path):
 req=urllib.request.Request("https://api.apify.com/v2/"+path,
      headers={"Authorization":"Bearer "+TOKEN,"User-Agent":"PAL-Public-Task-Catalog/1.0"})
 with urllib.request.urlopen(req,timeout=20,context=CTX) as r:return json.load(r)["data"]
def esc(s):return html.escape(str(s or ""),quote=True)
def short(s,n=260):
 s=" ".join(str(s or "").split())
 if len(s)<=n:return s
 return s[:n].rsplit(" ",1)[0].rstrip(" ,.;")+ "…"
def main():
 pub=api("store?username=practical_ai_lab_jp&limit=100")["items"]
 public={x["name"]:x for x in pub if x.get("username")=="practical_ai_lab_jp"}
 owner=api("actors?my=1&limit=1000")["items"]
 slugs={x["id"]:x["name"] for x in owner}
 fetched=api("actor-tasks?limit=300")
 if fetched.get("total",0)>len(fetched.get("items",[])):
  raise RuntimeError("Incomplete task list; refusing to publish a partial catalog")
 tasks=[]
 for t in fetched["items"]:
  if not t.get("isPublic"):continue
  slug=slugs.get(t.get("actId"))
  if not slug or slug not in public:continue
  name=t.get("name") or ""
  title=t.get("title") or ""
  if not name or not title:continue
  category="Ecommerce" if "ECOMMERCE" in (public[slug].get("categories") or []) else "Website and developer QA"
  url="https://apify.com/practical_ai_lab_jp/"+urllib.parse.quote(slug,safe="-")+"/examples/"+urllib.parse.quote(name,safe="-")
  tasks.append({"taskName":name,"actorSlug":slug,"title":title,
     "description":short(t.get("description"),220),
     "actorTitle":public[slug].get("title") or slug,
     "url":url,"category":category})
 tasks.sort(key=lambda x:(0 if x["category"]=="Ecommerce" else 1,x["title"].casefold(),x["actorSlug"],x["taskName"]))
 count=len(tasks)
 if count<40:raise RuntimeError("Unexpectedly few public example tasks; fail closed")
 cards=[]
 for x in tasks:
  safe_url=esc(x["url"]+"?utm_source=pal_github_pages&utm_medium=organic&utm_campaign=pal_example_directory")
  actor_url="https://apify.com/practical_ai_lab_jp/"+urllib.parse.quote(x["actorSlug"],safe="-")
  search=esc((x["title"]+" "+x["description"]+" "+x["actorTitle"]+" "+x["category"]).lower())
  cards.append(f'<article class="task" data-search="{search}"><span class="kind">{esc(x["category"])}</span>'
      f'<h2>{esc(x["title"])}</h2><p>{esc(x["description"] or "A public example task for this PAL Actor.")}</p>'
      f'<p class="actor">Actor: <a href="{esc(actor_url)}">{esc(x["actorTitle"])}</a></p>'
      f'<a class="cta" href="{safe_url}">See example and current Pricing ↗</a></article>')
 canonical="https://jojoagogog-beep.github.io/ecommerce-jsonld-qa-checklist/example-tasks.html"
 data={"@context":"https://schema.org","@type":"ItemList","name":"Practical AI Lab public Apify task examples",
       "numberOfItems":count,
       "itemListElement":[{"@type":"ListItem","position":n+1,"name":x["title"],"url":x["url"]} for n,x in enumerate(tasks)]}
 ld=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
 output=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{count} Practical Apify Example Tasks | Practical AI Lab</title>
<meta name="description" content="Browse {count} public Practical AI Lab Apify example tasks by business goal. Review prefilled input examples for ecommerce pricing, product markup and SEO; check Apify pricing before running.">
<meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">
<meta property="og:title" content="Practical AI Lab Apify Example Task Directory">
<meta property="og:type" content="website"><meta property="og:description" content="Find ready-to-review Apify example tasks for ecommerce and website QA.">
<meta property="og:url" content="{canonical}">
<style>
:root{{color-scheme:dark;--bg:#0b1727;--fg:#eff6ff;--muted:#c2d1df;--edge:#39556e;--mint:#91e5cc}}
*{{box-sizing:border-box}}body{{margin:0;font:16px/1.56 system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--fg)}}
a{{color:#a6dfff}}nav,main,footer{{max-width:1110px;margin:auto;padding:20px}}nav{{display:flex;gap:19px;flex-wrap:wrap;align-items:center}}
h1{{font-size:clamp(32px,5vw,50px);line-height:1.13;letter-spacing:-.025em;margin:12px 0 23px}}
header{{border-bottom:1px solid var(--edge)}}h2{{font-size:19px;line-height:1.33;margin:8px 0}}
p{{color:var(--muted)}}.intro{{max-width:870px;margin:40px 0}}.brand{{font-weight:900;letter-spacing:.08em;margin-right:auto}}
label{{display:block;font-weight:700;margin-bottom:8px}}
input{{width:min(100%,640px);border:1px solid #7394a7;background:#13283c;color:#fff;padding:13px;border-radius:9px;font:inherit}}
#result{{margin-top:10px;font-size:14px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:32px 0}}
.task{{display:flex;flex-direction:column;border:1px solid var(--edge);border-radius:13px;background:#162b3e;padding:20px}}.kind{{color:var(--mint);font-size:12px;text-transform:uppercase;letter-spacing:.06em;font-weight:800}}
.task p{{font-size:14px;margin:9px 0}}.task .actor{{margin-top:auto}}.cta{{background:var(--mint);color:#082b35;text-decoration:none;font-weight:800;display:inline-block;padding:11px 12px;border-radius:8px;margin-top:10px}}
.cta:hover{{text-decoration:underline}}.task[hidden]{{display:none}}footer{{border-top:1px solid var(--edge);font-size:13px;color:var(--muted)}}
@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media(max-width:580px){{.grid{{grid-template-columns:1fr}}}}
</style>
<script type="application/ld+json">{ld}</script>
</head><body>
<header><nav><span class="brand">PRACTICAL AI LAB</span><a href="./">Home</a><a href="tool-finder.html">Choose by task</a><a href="catalog.html">All public Actors</a></nav></header>
<main><div class="intro"><p>PAL · Public Apify Example Tasks</p>
<h1>Find a real workflow, not just an app name.</h1>
<p>Browse {count} published example task configurations for Practical AI Lab's ecommerce, product-data and website quality tools. These are already published Apify task pages, not made-up ratings or customer testimonials.</p>
<p><strong>How to use:</strong> open an example, inspect the prefilled data, replace synthetic samples with a public page you are permitted to analyze, and check the Actor's live Pricing tab before executing. Merely viewing an example does not start a paid run.</p></div>
<label for="filter">Find a workflow by keyword</label><input id="filter" type="search" placeholder="Try competitor price, Product schema, UTM, H1 or migration…" aria-label="Search published Apify example tasks">
<p id="result" aria-live="polite">{count} examples</p>
<div class="grid" id="examples">{''.join(cards)}</div>
<p>Still not sure which kind of tool fits? <a href="tool-finder.html">Start with the task-based tool selector</a> or <a href="competitor-price-readiness.html">check price-page compatibility for free</a>.</p>
</main><footer>Practical AI Lab · These examples are not proof of paid customers or guaranteed results. Public task configurations can change; verify current Apify details and pricing.</footer>
<script>
const filter=document.getElementById("filter"),cards=[...document.querySelectorAll(".task")];
filter.addEventListener("input",()=>{{const q=filter.value.trim().toLowerCase();let n=0;for(const card of cards){{const show=card.dataset.search.includes(q);card.hidden=!show;if(show)n++;}}document.getElementById("result").textContent=n+" examples";}});
</script></body></html>
'''
 (ROOT/"example-tasks.html").write_text(output)
 (ROOT/"examples-directory-public-manifest.json").write_text(json.dumps({
  "publicActorCount":len(public),"publicExampleTaskCount":count,
  "privateTasksExcluded":sum(not t.get("isPublic") for t in fetched["items"]),
  "examples":[{"actorSlug":x["actorSlug"],"taskName":x["taskName"],"url":x["url"]} for x in tasks],
  "usesOnlyPublicTasks":True,"paidRuns":0,"storeEdits":0},indent=2)+"\n")
 print("PUBLIC_TASK_DIRECTORY_GENERATED",count,"PUBLIC_ACTORS",len(public),flush=True)
if __name__=="__main__":main()
