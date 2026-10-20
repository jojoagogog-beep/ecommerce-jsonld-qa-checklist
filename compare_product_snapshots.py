#!/usr/bin/env python3
"""Compare two LOCAL ecommerce product snapshots, without making web requests.
Free educational example for historical price / published stock label comparisons.
"""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

MAX_BYTES=2000000
MAX_PRODUCTS=10000

def load(path):
    p=Path(path)
    if p.stat().st_size>MAX_BYTES:
        raise ValueError("Snapshot exceeds 2 MB safety limit.")
    rows=json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(rows,list):
        raise ValueError("Snapshot must be a JSON array.")
    if len(rows)>MAX_PRODUCTS:
        raise ValueError("Snapshot exceeds 10,000 products.")
    result={}
    for row in rows:
        if not isinstance(row,dict):
            raise ValueError("Every product must be an object.")
        name=str(row.get("id") or "").strip()
        if not name:
            raise ValueError("Every product requires a nonempty id.")
        if name in result:
            raise ValueError("Duplicate product ID: "+name[:90])
        result[name]=row
    return result

def price_of(record):
    try:
        price=Decimal(str(record.get("price","")))
        if not price.is_finite() or price<0:
            return None
        return price
    except (InvalidOperation,TypeError,ValueError):
        return None

def compare(before,after,threshold=Decimal("5")):
    if threshold<0 or not threshold.is_finite():
        raise ValueError("threshold must be nonnegative")
    entries=[]
    for product in sorted(set(before)|set(after)):
        old=before.get(product);new=after.get(product)
        if old is None:
            entries.append({"id":product,"event":"added","new":new})
            continue
        if new is None:
            entries.append({"id":product,"event":"removed","old":old})
            continue
        old_p=price_of(old);new_p=price_of(new)
        old_c=str(old.get("currency") or "").strip().upper()
        new_c=str(new.get("currency") or "").strip().upper()
        flags=[]
        changes={"id":product,"event":"changed"}
        if old_c!=new_c:
            flags.append("currency_changed")
            changes["oldCurrency"]=old_c
            changes["newCurrency"]=new_c
        if old_p is None or new_p is None:
            flags.append("review_invalid_price")
        elif old_c==new_c:
            if old_p!=new_p:
                flags.append("price_changed")
                percent=((new_p-old_p)/old_p*100) if old_p!=0 else None
                changes.update(oldPrice=str(old_p),newPrice=str(new_p),
                               changePercent=(str(percent.quantize(Decimal("0.01"))) if percent is not None else None),
                               crossesThreshold=(abs(percent)>=threshold if percent is not None else None))
        old_stock=str(old.get("availability") or "")
        new_stock=str(new.get("availability") or "")
        if old_stock!=new_stock:
            flags.append("availability_label_changed")
            changes["oldAvailability"]=old_stock
            changes["newAvailability"]=new_stock
        if flags:
            changes["flags"]=flags
            entries.append(changes)
    return {"beforeProducts":len(before),"afterProducts":len(after),
            "thresholdPercent":str(threshold),"changedRecords":len(entries),
            "changes":entries,
            "note":"Offline comparison of supplied snapshots. Availability labels are not verified physical inventory."}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--threshold",default="5",help="Minimum percentage movement to flag (default 5)")
    args=parser.parse_args()
    try:
        result=compare(load(args.before),load(args.after),Decimal(args.threshold))
        print(json.dumps(result,indent=2,ensure_ascii=False))
    except (ValueError,InvalidOperation,OSError,json.JSONDecodeError) as e:
        print("Error: "+str(e),file=sys.stderr)
        return 2
    return 0

if __name__=="__main__":
    raise SystemExit(main())
