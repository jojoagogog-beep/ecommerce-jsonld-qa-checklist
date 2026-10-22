"""Check usefulness, correct links and no fake results in the migration QA guide."""
from __future__ import annotations
import html.parser,pathlib,json,unittest,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
SIX=["pal-product-stock-schema-check","my-actor","my-actor-15",
    "pal-h1-heading-checker","pal-image-alt-text-checker",
    "pal-competitor-price-stock-delta"]
class LinkParser(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.headings=[];self.inh=False
 def handle_starttag(self,tag,attrs):
  if tag=="a":self.links.append(dict(attrs).get("href",""))
  if tag=="h1":self.inh=True
 def handle_data(self,data):
  if self.inh:self.headings.append(data)
 def handle_endtag(self,tag):
  if tag=="h1":self.inh=False
class GuideTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.page=(ROOT/"storefront-migration-audit.html").read_text()
  cls.parsed=LinkParser();cls.parsed.feed(cls.page)
 def test_all_six_lagging_actors_are_recommended(self):
  root="https://apify.com/practical_ai_lab_jp/"
  for slug in SIX:
   with self.subTest(slug=slug):
    targets=[s for s in self.parsed.links if s.startswith(root+slug+"?")]
    self.assertEqual(len(targets),1)
    self.assertIn("utm_campaign=step",targets[0].replace("&amp;","&"))
 def test_metadata_and_pricing_caveats(self):
  for text in ["application/ld+json","HowTo","live Pricing tab",
               "static","No checkout confirmation","stock",
               "run-start","public pages"]:
   self.assertIn(text,self.page)
  self.assertEqual(len(self.parsed.headings),1)
 def test_real_internal_links(self):
  for link in self.parsed.links:
   if link.startswith("http") or link.startswith("#") or link=="./":continue
   self.assertTrue((ROOT/link).is_file(),link)
 def test_single_sitemap_entry_and_entrypoints(self):
  sitemap=(ROOT/"sitemap.xml").read_text()
  self.assertEqual(sitemap.count("/storefront-migration-audit.html"),1)
  for f in ["index.html","catalog.html","README.md"]:
   self.assertIn("storefront-migration-audit.html",(ROOT/f).read_text())
 def test_no_fake_traffic_claim(self):
  for phrase in ["#1 on Apify", "guaranteed sales increase", "Verified customers"]:
   self.assertNotIn(phrase,self.page)
if __name__=="__main__":unittest.main()
