"""Buyer-relevance, public path and truthfulness regression. Offline."""
from html.parser import HTMLParser
from pathlib import Path
import re, unittest
ROOT=Path(__file__).resolve().parents[1]
NAME="competitor-price-monitoring-guide.html"
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.scripts=[];self.title=[];self.structured=[]
        self.js=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=="a":self.links.append(attrs.get("href"))
        if tag=="script" and attrs.get("type")=="application/ld+json":self.js=True
        if tag=="script":self.scripts.append(attrs)
    def handle_endtag(self,tag):
        if tag=="script":self.js=False
class Guides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=(ROOT/NAME).read_text()
        cls.parser=Parser();cls.parser.feed(cls.raw)
    def test_seo_and_pricing(self):
        self.assertIn("Competitor Price Monitoring",self.raw)
        self.assertIn('rel="canonical"',self.raw)
        self.assertIn("https://apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta",self.raw)
        self.assertIn("utm_campaign=competitor_monitoring_fit_guide",self.raw)
        self.assertIn("application/ld+json",self.raw)
    def test_does_not_misrepresent_features(self):
        for phrase in ("Not supported","No promise","No. The Actor","not a universal retailer scraper",
                       "does not automatically email alerts","human validation","not proven customer outcomes"):
            self.assertIn(phrase,self.raw)
        self.assertNotIn("guaranteed SEO rank",self.raw)
        self.assertNotIn("50% OFF",self.raw)
        self.assertNotIn("100% coverage",self.raw)
    def test_all_local_links_exist(self):
        for link in self.parser.links:
            if not link or link=="./" or link.startswith(("http://","https://","#","mailto:")):continue
            self.assertTrue((ROOT/link.split("#")[0].split("?")[0]).is_file(),link)
    def test_inbound_links_sitemap(self):
        for name in ("index.html","competitor-price-tracker.html",
                     "ecommerce-price-tracker-workflow.html","sitemap.xml","README.md"):
            self.assertIn(NAME,(ROOT/name).read_text(),name)
    def test_no_auto_run_or_browser_tracking(self):
        self.assertNotIn("fetch(",self.raw)
        self.assertNotIn("navigator.sendBeacon(",self.raw)
        self.assertNotIn("https://api.apify.com/v2/acts/",self.raw)
if __name__=="__main__":unittest.main()
