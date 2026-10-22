"""Offline checks for PAL buyer-facing homepage conversion design."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Extract(HTMLParser):
    def __init__(self):
        super().__init__();self.hero=False;self.details=False;self.main_buttons=[];self.extra_buttons=[];self.attrs=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="section" and d.get("class")=="hero":self.hero=True
        if self.hero and tag=="details" and d.get("class")=="more-tools":self.details=True
        if tag=="a" and self.hero:
            (self.extra_buttons if self.details else self.main_buttons).append(d.get("href",""))
    def handle_endtag(self,tag):
        if tag=="details":self.details=False
        if tag=="section":self.hero=False
class Focus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page=(ROOT/"index.html").read_text()
        cls.h=Extract();cls.h.feed(cls.page)
    def test_first_screen_decision_paths(self):
        self.assertEqual(len(self.h.main_buttons),4)  # three action links + price disclosure
        self.assertIn("competitor-price-readiness.html",self.h.main_buttons)
        self.assertIn("#free",self.h.main_buttons)
        self.assertTrue(any("utm_campaign=focused_homepage" in x for x in self.h.main_buttons))
        self.assertTrue(any("apify.com/practical_ai_lab_jp/pal-competitor-price-stock-delta" in x for x in self.h.main_buttons))
    def test_other_catalog_and_free_tools_remain(self):
        self.assertGreaterEqual(len(self.h.extra_buttons),14)
        for value in ("catalog.html","competitor-price-tracker.html","example-tasks.html",
                      "h1-heading-structure-audit.html","image-alt-accessibility-audit.html"):
            self.assertIn(value,self.h.extra_buttons)
        self.assertIn('<summary>More free checks',self.page)
    def test_no_unverified_urgency(self):
        self.assertNotIn("Limited-time 50% off",self.page)
        self.assertNotIn("Guaranteed sales",self.page)
    def test_compatible_with_accessible_mobile(self):
        self.assertIn('aria-label="Choose the next step"',self.page)
        self.assertIn('summary:focus-visible',self.page)
        self.assertIn('@media(max-width:760px)',self.page)
if __name__=="__main__":unittest.main()
