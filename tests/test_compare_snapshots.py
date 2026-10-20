#!/usr/bin/env python3
import sys
import unittest
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from compare_product_snapshots import compare,load

class CompareTest(unittest.TestCase):
    def setUp(self):
        root=Path(__file__).resolve().parents[1]
        self.before=load(root/"examples/price_before.json")
        self.after=load(root/"examples/price_after.json")
    def test_price_change(self):
        r=compare(self.before,self.after,Decimal("10"))
        entry=next(x for x in r["changes"] if x["id"]=="item-a")
        self.assertIn("price_changed",entry["flags"])
        self.assertTrue(entry["crossesThreshold"])
        self.assertEqual(entry["changePercent"],"-16.67")
    def test_availability_changed(self):
        r=compare(self.before,self.after)
        entry=next(x for x in r["changes"] if x["id"]=="item-b")
        self.assertEqual(entry["newAvailability"],"OutOfStock")
    def test_added_removed(self):
        r=compare(self.before,self.after)
        self.assertEqual(next(x for x in r["changes"] if x["id"]=="item-c")["event"],"removed")
        self.assertEqual(next(x for x in r["changes"] if x["id"]=="item-d")["event"],"added")
    def test_currency_change_no_price_delta(self):
        before={"x":{"price":"10.00","currency":"USD"}}
        after={"x":{"price":"8.00","currency":"EUR"}}
        change=compare(before,after)["changes"][0]
        self.assertIn("currency_changed",change["flags"])
        self.assertNotIn("price_changed",change["flags"])
    def test_duplicate_ids_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"invalid.json"
            p.write_text('[{"id":"x"},{"id":"x"}]')
            with self.assertRaises(ValueError):
                load(p)
    def test_empty_no_changes(self):
        self.assertEqual(compare({}, {})["changedRecords"],0)

if __name__=="__main__":
    unittest.main()
