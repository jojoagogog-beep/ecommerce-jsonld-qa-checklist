"""No-cost regression test for ten independent PAL Apify onboarding examples."""
import html,unittest,json,pathlib,re
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parent.parent
ACTORS=pathlib.Path.home()/"Projects/pal-actor-catalog50/growth"
class Cards(HTMLParser):
 def __init__(self):
  super().__init__();self.articles=[];self.active=None;self.pre=False;self.anchors=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="article" and "card" in a.get("class","").split():
   self.active={"slug":a.get("data-slug"),"pre":"","hrefs":[]};self.articles.append(self.active)
  if self.active is not None and tag=="pre":self.pre=True
  if self.active is not None and tag=="a":self.active["hrefs"].append(a.get("href"))
 def handle_data(self,data):
  if self.active is not None and self.pre:self.active["pre"]+=data
 def handle_endtag(self,tag):
  if tag=="pre":self.pre=False
  if tag=="article":self.active=None
class Smoke(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=(ROOT/"schema-audit-quickstart.html").read_text()
  cls.plan=json.loads((ACTORS/"pal_five_placeholder_example_replacements_staged_20261021.json").read_text())
  cls.page=Cards();cls.page.feed(cls.source)
 def test_ten_cards_unique(self):
  slugs=[x["slug"] for x in self.page.articles]
  self.assertEqual(len(slugs),10)
  self.assertEqual(len(set(slugs)),10)
  self.assertEqual(set(slugs),set(self.plan["affectedSlugs"]))
 def test_every_example_matches_verified_fixture(self):
  for x in self.page.articles:
   with self.subTest(x=x["slug"]):
    value=json.loads(x["pre"])
    self.assertEqual(value,{"urls":[self.plan["fixtureBySlug"][x["slug"]]]})
    self.assertEqual(len(x["hrefs"]),1)
    self.assertEqual(x["hrefs"][0],"https://apify.com/practical_ai_lab_jp/"+x["slug"])
 def test_both_sources_exist_and_are_explicitly_synthetic(self):
  urls=set(self.plan["fixtureBySlug"].values())
  self.assertEqual(len(urls),2)
  for u in urls:
   with self.subTest(u=u):
    page=ROOT/("examples/"+u.rsplit("/",1)[-1])
    source=page.read_text()
    self.assertIn("Synthetic",source)
    self.assertIn("noindex",source)
 def test_price_disclosure(self):
  self.assertIn("check live prices",self.source.lower())
  self.assertIn("charges may apply",self.source)
  self.assertIn("does not start a run",self.source)
 def test_public_page_unconnected_to_paid_execution(self):
  self.assertNotRegex(self.source,r"\bfetch\s*\(")
  self.assertNotRegex(self.source,r"\binnerHTML\s*=")
  self.assertNotRegex(self.source,r"\bXMLHttpRequest\b")
if __name__=="__main__":unittest.main()
