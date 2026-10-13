"""QA for the Filipino Verbal pool: item checks plus the bank-wide key/trap rule (CoS round 03).
Usage: python3 scripts/batches/qa_fil.py   (exit 1 on any failure)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import qa
R = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "research")
FILES = ["chatgpt-batch-001.json", "filipino-supplement-001.json", "gap-fill-001.json"]
items = [i for f in FILES for i in json.load(open(os.path.join(R, f), encoding="utf-8"))["items"] if i["domain"] == "verbal_fil"]
probs = [(i["id"], e) for i in items for e in qa.check_item(i) if "solver" not in e]
# Key/trap pairs are kept apart at session build time (app/Services/Exam/MockPoolState.php); listed here for authors.
pairs = qa.check_key_trap([i for i in items if i["archetype"] in ("VFIL-KASINGKAHULUGAN", "VFIL-KASALUNGAT", "VFIL-WIKAIN")])
print("Filipino items:", len(items), "| vocabulary key/trap pairs kept apart by MockPoolState:", len(pairs))
for p in pairs:
    print("INFO", *p)
for p in probs:
    print("FAIL", *p)
print("QA", "GREEN" if not probs else "RED")
sys.exit(1 if probs else 0)
