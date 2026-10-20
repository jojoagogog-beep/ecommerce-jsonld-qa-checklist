#!/usr/bin/env python3
"""Free offline hreflang markup review for ONE HTML file.
Educational only: no network, no reciprocity crawl, no SEO guarantees.
"""
import argparse
from collections import defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlparse

LANG_PATTERN = re.compile(r"^(?:[a-zA-Z]{2,3}(?:-[a-zA-Z]{4})?(?:-(?:[a-zA-Z]{2}|[0-9]{3}))?|x-default)$")

class LinkReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "link":
            return
        attributes = dict(attrs)
        if "alternate" not in (attributes.get("rel") or "").lower().split():
            return
        self.links.append({
            "hreflang": (attributes.get("hreflang") or "").strip(),
            "href": (attributes.get("href") or "").strip()
        })

def inspect(path, page_url=None):
    file = Path(path)
    if file.stat().st_size > 2000000:
        raise ValueError("The offline sample is limited to HTML files of 2 MB or less.")
    reader = LinkReader()
    reader.feed(file.read_text(encoding="utf-8"))
    issues = []
    by_language = defaultdict(list)
    alternatives = []
    for index, item in enumerate(reader.links):
        language = item["hreflang"]
        href = item["href"]
        if not language:
            # Some alternate links target other media types, not locales.
            # Omit from hreflang review instead of claiming this is an error.
            continue
        by_language[language.casefold()].append(href)
        parsed = urlparse(href)
        alternatives.append({"hreflang": language, "href": href})
        if not LANG_PATTERN.fullmatch(language):
            issues.append({"code":"review_language_tag","hreflang":language,
                           "message":"Review language/region format against applicable BCP 47 and search-engine guidance."})
        if not href:
            issues.append({"code":"missing_href","hreflang":language,
                           "message":"The localized alternate is missing an href."})
        elif parsed.scheme not in ("https","http") or not parsed.netloc:
            issues.append({"code":"review_absolute_url","hreflang":language,"href":href,
                           "message":"Review the alternate URL: an absolute HTTP(S) URL is typically appropriate."})
    for language, values in by_language.items():
        if len(values) > 1:
            issues.append({"code":"duplicate_hreflang","hreflang":language,
                           "destinations":values,
                           "message":"More than one alternate was declared for this language/region; review duplicates."})
    if page_url and alternatives:
        if not any(item["href"].rstrip("/") == page_url.rstrip("/") for item in alternatives):
            issues.append({"code":"review_self_reference","pageUrl":page_url,
                           "message":"No alternate target matches the supplied current page URL. Check whether self-reference is required for this implementation."})
    return {
        "source":str(file),
        "checkedPageUrl":page_url,
        "scope":"single local HTML file, not a site-wide reciprocal-link audit",
        "alternates":alternatives,
        "alternateCount":len(alternatives),
        "issues":issues,
        "issueCount":len(issues),
        "note":"Possible review candidates only; no online access, destination checks, indexing or SEO ranking guarantees."
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file",help="Path to a local HTML file")
    parser.add_argument("--page-url",help="Optional URL of the source page for self-reference review")
    args=parser.parse_args()
    print(json.dumps(inspect(args.html_file,args.page_url),ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
