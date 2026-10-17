"""QA one research batch file against the whole repo bank.
Usage: python3 scripts/batches/qa_file.py docs/research/<file>.json [--near 0.65]
Runs qa.check_item on every item, duplicate/near-duplicate stems against every other bank file, baseline hits,
spelling-target uniqueness bank-wide, and the 25% stem-frame cap within the file's domains. Exit 1 on any failure."""
import glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import qa
path = sys.argv[1]
near = float(sys.argv[sys.argv.index("--near") + 1]) if "--near" in sys.argv else 0.65
root = os.path.join(os.path.dirname(__file__), "..", "..", "docs")
mine = json.load(open(path, encoding="utf-8"))["items"]
others = []
for f in sorted(glob.glob(os.path.join(root, "batches", "batch-*.json")) + glob.glob(os.path.join(root, "research", "*.json"))):
    if os.path.abspath(f) == os.path.abspath(path):
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    items = d.get("items") if isinstance(d, dict) else d
    if isinstance(items, list):
        others += [i for i in items if isinstance(i, dict) and "archetype" in i and "stem" in i and i.get("review_status") != "rejected"]
view = [dict(i, _legacy=True) if i.get("domain") == "general_information" else i for i in mine]
probs = qa.check_round(view, [o["stem"] for o in others], near=near)
probs += [(h[0], f"baseline {h[1]} match ({h[2]}): {h[3]}") for h in qa.baseline_hits(view)]
spell = [p for p in qa.check_spelling(others + view) if p[0] in {i["id"] for i in mine}]
probs += spell
dom = Counter(i["domain"] for i in mine)
for (d, f), n in Counter((i["domain"], qa.stem_frame(i["stem"])) for i in mine).items():
    if n > 0.25 * dom[d]:
        probs.append(("file", f"{d}: phrasing '{f}' used {n}/{dom[d]} (max 25%)"))
for p in probs:
    print("FAIL", *p)
print(f"{os.path.basename(path)}: {len(mine)} items, compared with {len(others)} bank items; {len(probs)} problem(s)")
sys.exit(1 if probs else 0)
