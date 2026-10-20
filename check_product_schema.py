#!/usr/bin/env python3
"""Offline Product JSON-LD checklist. Educational; no network calls or dependencies."""
from __future__ import annotations
import html.parser
import json
import pathlib
import sys

class JsonLdReader(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_jsonld = False
        self.chunks: list[str] = []
        self.scripts: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":
            attributes = dict(attrs)
            value = (attributes.get("type") or "").lower().strip()
            self.in_jsonld = value == "application/ld+json"
            self.chunks = []
    def handle_data(self, data):
        if self.in_jsonld:
            self.chunks.append(data)
    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.in_jsonld:
            self.scripts.append("".join(self.chunks))
            self.in_jsonld = False
            self.chunks = []

def flatten(node):
    if isinstance(node, list):
        for v in node:
            yield from flatten(v)
    elif isinstance(node, dict):
        yield node
        for key in ("@graph", "mainEntity"):
            if key in node:
                yield from flatten(node[key])

def is_type(node, expected):
    value = node.get("@type", [])
    types = value if isinstance(value, list) else [value]
    return any(str(v).rstrip("/").split("/")[-1].lower() == expected.lower() for v in types)

def flag(code, field, message):
    return {"code": code, "field": field, "message": message}

def audit(file_path):
    raw = pathlib.Path(file_path).read_text(encoding="utf-8")
    parser = JsonLdReader()
    parser.feed(raw)
    nodes = []
    errors = []
    for block in parser.scripts:
        try:
            nodes.extend(flatten(json.loads(block)))
        except (ValueError, TypeError):
            errors.append(flag("invalid_json_ld", "JSON-LD", "A JSON-LD script could not be parsed."))
    products = [node for node in nodes if is_type(node, "Product")]
    results = []
    for product in products:
        findings = []
        for key in ("name", "brand", "image"):
            if not product.get(key):
                findings.append(flag("missing_" + key, key, "Review whether this Product should include " + key + "."))
        if not any(product.get(k) for k in ("sku", "gtin", "gtin8", "gtin12", "gtin13", "gtin14", "mpn")):
            findings.append(flag("missing_identifier", "sku/gtin/mpn", "Review the applicable product identifiers."))
        offers = product.get("offers") or []
        if isinstance(offers, dict):
            offers = [offers]
        if not isinstance(offers, list):
            offers = []
        if not offers:
            findings.append(flag("missing_offer", "offers", "No Product Offer was found."))
        for i, offer in enumerate(offers):
            if not isinstance(offer, dict):
                findings.append(flag("invalid_offer", "offers", "Offer entry is not an object."))
                continue
            for key in ("price", "priceCurrency", "availability"):
                if not offer.get(key):
                    findings.append(flag("missing_" + key.lower(), f"offers[{i}].{key}",
                                        "Review whether the published Offer should include " + key + "."))
        results.append({"product": str(product.get("name") or "Untitled")[:160],
                        "offersFound": len(offers), "issues": findings, "issueCount": len(findings)})
    return {"file": str(file_path), "jsonLdBlocks": len(parser.scripts),
            "productsFound": len(products), "parseIssues": errors, "products": results}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_product_schema.py examples/product_incomplete.html", file=sys.stderr)
        return 2
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
