#!/usr/bin/env python3
"""No-network tests for the offline single-file hreflang reviewer."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from check_hreflang import inspect

class HreflangTests(unittest.TestCase):
    def check(self, html, page_url=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fixture.html"
            p.write_text(html,encoding="utf-8")
            return inspect(str(p),page_url=page_url)

    def test_valid_alternates(self):
        page="https://example.com/en/product"
        result=self.check('<link rel="alternate" hreflang="en-US" href="'+page+'">'
                          '<link rel="alternate" hreflang="ja-JP" href="https://example.com/ja/product">',
                          page)
        self.assertEqual(result["issueCount"],0)
        self.assertEqual(result["alternateCount"],2)

    def test_duplicate_language(self):
        result=self.check('<link rel="alternate" hreflang="en-US" href="https://example.com/a">'
                          '<link rel="alternate" hreflang="en-us" href="https://example.com/b">')
        self.assertIn("duplicate_hreflang",{x["code"] for x in result["issues"]})

    def test_missing_and_relative_target(self):
        result=self.check('<link rel="alternate" hreflang="en-GB">'
                          '<link rel="alternate" hreflang="ja-JP" href="/jp/local">')
        self.assertEqual({"missing_href","review_absolute_url"},
                         {x["code"] for x in result["issues"]})

    def test_non_hreflang_alternate_is_not_an_error(self):
        result=self.check('<link rel="alternate" type="application/rss+xml" href="/rss.xml">')
        self.assertEqual(result["alternateCount"],0)
        self.assertEqual(result["issueCount"],0)

    def test_self_reference_optional(self):
        result=self.check('<link rel="alternate" hreflang="en-US" href="https://example.com/en">'
                          ,page_url="https://example.com/ja")
        self.assertIn("review_self_reference",{x["code"] for x in result["issues"]})

    def test_invalid_language_format(self):
        result=self.check('<link rel="alternate" hreflang="bad_region_format" href="https://example.com/lang">')
        self.assertIn("review_language_tag",{x["code"] for x in result["issues"]})

if __name__=="__main__":
    unittest.main()
