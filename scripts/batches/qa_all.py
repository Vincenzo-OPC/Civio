"""Whole-bank QA for batch-002..011: item checks, per-batch and bank-wide CoS rules, dedup vs batch-001 and the baseline bank.
Usage: python3 scripts/batches/qa_all.py   (exit 1 on any failure)"""
import glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import qa
from build import DOCS, LEGACY_IDS

batches = sorted(p for p in glob.glob(os.path.join(DOCS, "batch-*.json")) if not p.endswith("batch-001.json"))
# Proposed bank: rewrites waiting for CoS (docs/research/round-*-fixes.json) replace their batch items by id.
# Pass --no-fixes to check the committed batch files alone (the round 02 frame cap then fails until CoS merges the fixes).
FIX = {}
if "--no-fixes" not in sys.argv:
    for fp in sorted(glob.glob(os.path.join(DOCS, "..", "research", "round-*-fixes.json"))):
        FIX.update({i["id"]: i for i in json.load(open(fp, encoding="utf-8"))["items"]})
allv, problems = [], []
for p in batches:
    items = [FIX.get(i["id"], i) for i in json.load(open(p, encoding="utf-8"))["items"]]
    view = []
    for i in items:
        v = dict(i)
        if "gen_fact" in i:
            v["_fact"] = i["gen_fact"]
        if i["id"][-6:] in LEGACY_IDS:
            v["_legacy"] = True
        view.append(v)
    problems += [(os.path.basename(p), *x) for x in qa.check_batch_rules(view)]
    allv += view
b1 = [FIX.get(i["id"], i)["stem"] for i in json.load(open(os.path.join(DOCS, "batch-001.json"), encoding="utf-8"))["items"]]
problems += qa.check_round(allv, b1)
problems += qa.check_bank_rules(allv)
hits = qa.baseline_hits(allv)
problems += [(h[0], f"baseline {h[1]} match ({h[2]}): {h[3]}") for h in hits]
ev = qa.check_gi_evidence([v for v in allv if "_fact" in v])
print(f"overlay fixes: {len(FIX)}; items: {len(allv)}; baseline stems compared: {len(qa.BASE)}; baseline exact: {sum(h[1] == 'exact' for h in hits)}, near: {sum(h[1] == 'near' for h in hits)}")
print("GI quotes checked against official text:", "skipped (no cache)" if ev is None else f"{len(ev)} missing")
print("domains:", dict(Counter(v["domain"] for v in allv)))
print("verbal concepts:", dict(Counter(v["concept"] for v in allv if v["domain"] == "verbal_en")))
for p in problems:
    print("FAIL", *p)
print("QA", "GREEN" if not problems and not ev else "RED")
sys.exit(1 if problems or ev else 0)
