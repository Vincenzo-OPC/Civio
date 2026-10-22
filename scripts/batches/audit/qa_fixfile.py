"""QA a lint-fix file (items carrying fix_of=<original id>) against the whole bank, the same checks as qa_file.py,
except that each fix is not compared with the original it replaces (a fix necessarily repeats its original's stem).
Usage: python3 scripts/batches/audit/qa_fixfile.py docs/research/audit/fixes/<file>.json [--near 0.65] [--baseline PATH]
Exit 1 on any failure."""
import glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import qa
path = sys.argv[1]
near = float(sys.argv[sys.argv.index("--near") + 1]) if "--near" in sys.argv else 0.65
root = os.path.join(os.path.dirname(__file__), "..", "..", "..", "docs")
mine = json.load(open(path, encoding="utf-8"))["items"]
orig = {i["fix_of"] for i in mine}
others = []
srcs = sorted(glob.glob(os.path.join(root, "batches", "batch-*.json")) + glob.glob(os.path.join(root, "research", "*.json")))
if "--baseline" in sys.argv: srcs.append(sys.argv[sys.argv.index("--baseline") + 1])
for f in srcs:
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    items = d.get("items") if isinstance(d, dict) else d
    if isinstance(items, list):
        others += [i for i in items if isinstance(i, dict) and "archetype" in i and "stem" in i and i.get("review_status") != "rejected" and i.get("id") not in orig]
view = [dict(i, _legacy=True) if i.get("domain") == "general_information" else i for i in mine]
probs = qa.check_round(view, [o["stem"] for o in others], near=near)
bl = [h for h in qa.baseline_hits(view) if not h[0].startswith("CIVIO-BASELINE-")]  # a baseline item's fix matches its own seed
probs += [(h[0], f"baseline {h[1]} match ({h[2]}): {h[3]}") for h in bl]
probs += [p for p in qa.check_spelling(others + view) if p[0] in {i["id"] for i in mine}]
for p in probs: print("FAIL", *p)
print(f"{os.path.basename(path)}: {len(mine)} fixes, compared with {len(others)} bank items (originals excluded); {len(probs)} problem(s)")
sys.exit(1 if probs else 0)
