"""Offline regression tests for truthful, strictly read-only Apify price display."""
import importlib.util
from decimal import Decimal
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("pal_live_price",ROOT/"scripts/sync_competitor_live_pricing.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
class TestPriceSync(unittest.TestCase):
 def test_regular_pricing_no_premature_discount_claim(self):
  sample={"tiered":False,"run":Decimal("0.00005"),"prices":{"FREE":Decimal("0.0035")}}
  x=module.build_section(sample)
  self.assertIn("USD 0.00355",x)
  self.assertIn("USD 0.01755",x)
  self.assertIn("USD 0.17505",x)
  self.assertIn("No plan-specific tier discounts are confirmed",x)
  self.assertNotIn("50% below standard",x)
 def test_25_40_50_plan_discount_only_after_live_source(self):
  values=[("FREE","0.0035"),("BRONZE","0.002625"),("SILVER","0.0021"),
          ("GOLD","0.00175"),("PLATINUM","0.00175"),("DIAMOND","0.00175")]
  x=module.build_section({"tiered":True,"run":Decimal("0.00005"),
                          "prices":{a:Decimal(b) for a,b in values}})
  for s in ("25% below standard","40% below standard","50% below standard",
            "USD 0.002625","USD 0.00175"):
   self.assertIn(s,x)
  self.assertNotIn("No plan-specific tier discounts",x)
 def test_current_site_is_real_price_and_has_only_one_bound_section(self):
  s=(ROOT/"competitor-price-tracker.html").read_text()
  self.assertEqual(s.count(module.BEGIN),1)
  self.assertEqual(s.count(module.END),1)
  self.assertLess(s.index(module.BEGIN),s.index(module.END))
  self.assertIn("USD 0.0035 per successfully processed",s)
  self.assertNotIn("USD 0.00905",s)
  self.assertNotIn("USD 0.45005",s)
 def test_scheduled_sync_uses_live_public_apify_api(self):
  script=(ROOT/"scripts/update_public_catalog.sh").read_text()
  self.assertIn("scripts/sync_competitor_live_pricing.py",script)
  self.assertIn("competitor-price-tracker.html",script)
  self.assertIn("CATALOG_REMOTE_CONFLICT_NEEDS_REVIEW",script)
  self.assertNotIn("curl -X PUT",script)
if __name__=="__main__":unittest.main()
