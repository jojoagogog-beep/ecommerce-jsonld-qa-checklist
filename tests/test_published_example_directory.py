"""Validate the PAL public Apify task directory and prevent private-task leaks."""
from __future__ import annotations
import html.parser,json,pathlib,re,unittest,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Parser(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.cards=[];self.current=None;self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="article" and "task" in a.get("class","").split():
   self.current={"search":a.get("data-search"),"links":[]};self.cards.append(self.current)
  if tag=="a" and self.current is not None:self.current["links"].append(a.get("href",""))
  if tag=="a":self.links.append(a.get("href",""))
 def handle_endtag(self,tag):
  if tag=="article":self.current=None
class TestDirectory(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=(ROOT/"example-tasks.html").read_text()
  cls.manifest=json.loads((ROOT/"examples-directory-public-manifest.json").read_text())
  cls.dom=Parser();cls.dom.feed(cls.source)
  cls.entries=cls.manifest["examples"]
 def test_public_only(self):
  self.assertTrue(self.manifest["usesOnlyPublicTasks"])
  self.assertGreaterEqual(self.manifest["publicExampleTaskCount"],57)
  self.assertEqual(len(self.dom.cards),len(self.entries))
  self.assertEqual(len(set(x["url"] for x in self.entries)),len(self.entries))
  self.assertGreaterEqual(self.manifest["privateTasksExcluded"],0)
 def test_every_card_links_to_published_landing(self):
  for card,x in zip(self.dom.cards,self.entries):
   with self.subTest(task=x["taskName"]):
    path="/practical_ai_lab_jp/"+x["actorSlug"]+"/examples/"+x["taskName"]
    self.assertTrue(any(url.startswith("https://apify.com"+path+"?utm_source=") for url in card["links"]))
    self.assertTrue(card["search"])
 def test_private_drafts_are_not_indexed(self):
  generator=(ROOT/"scripts/generate_public_example_tasks.py").read_text()
  self.assertIn('if not t.get("isPublic"):continue',generator)
  self.assertTrue(self.manifest["usesOnlyPublicTasks"])
 def test_public_urls_exist_in_prior_live_url_audit(self):
  source=pathlib.Path.home()/"Projects/pal-actor-catalog50/growth/pal_public_task_landing_audit_20261022.json"
  old=json.loads(source.read_text())
  urls={x["requestedUrl"] for x in old["rows"] if x["status"]=="OK"}
  self.assertTrue(urls <= {x["url"] for x in self.entries})
 def test_sitemap_and_entrypoints(self):
  self.assertIn("/example-tasks.html",(ROOT/"sitemap.xml").read_text())
  self.assertIn('href="example-tasks.html"',(ROOT/"index.html").read_text())
  self.assertIn('href="example-tasks.html"',(ROOT/"catalog.html").read_text())
  self.assertIn('href="example-tasks.html"',(ROOT/"tool-finder.html").read_text())
 def test_no_actor_runs_or_billing(self):
  generator=(ROOT/"scripts/generate_public_example_tasks.py").read_text()
  self.assertNotIn("actor-runs",generator)
  self.assertNotIn('"POST"',generator)
  self.assertNotIn('"PUT"',generator)
  self.assertNotIn('fetch(',self.source)
 def test_stable_json_manifest(self):
  self.assertNotIn("generatedAtJst",self.manifest)
  self.assertGreaterEqual(self.manifest["publicActorCount"],35)
if __name__=="__main__":unittest.main()
