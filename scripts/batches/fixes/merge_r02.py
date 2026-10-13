"""Merge round 02 fixes after CoS PASS (2026-10-13): rewrites into batches, shortcuts into items, approvals recorded."""
import glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
os.chdir(ROOT)
APPROVE = dict(status="approved", review_status="passed", reviewer="Chief of Staff (final approval, delegated by GT)", reviewed_at="2026-10-13",
               review_line="[x] CoS PASS (final, per GT delegation, 2026-10-13)")
dump = lambda p, d: open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
subprocess.check_call(["git", "checkout", "df61273", "--", "docs/batches"])
subprocess.check_call([sys.executable, os.path.join(HERE, "r02_spelling.py")], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, os.path.join(HERE, "r02_frames.py")], stdout=subprocess.DEVNULL)
fixes = []
for p in sorted(glob.glob("docs/batches/batch-*.json")):
    d = json.load(open(p))
    old = {i["id"]: i for i in json.loads(subprocess.check_output(["git", "show", "df61273:" + p]))["items"]}
    for i in d["items"]:
        if i.get("review_status", "").startswith("changed"):
            o = old[i["id"]]
            i["replaces"] = {"batch": os.path.basename(p), "stem": o["stem"], "key": next(t["text"] for t in o["options"] if t["option_id"] == o["answer_option_id"])}
            i.update(APPROVE)
            i["notes"] += " CoS PASS 2026-10-13 (round 02 fixes)."
            fixes.append(i)
    dump(p, d)
dump("docs/research/round-02-fixes.json", {"batch": "round-02-fixes", "spec_version": "0.1.7",
     "status": "approved (CoS PASS 2026-10-13); merged into the batch files; kept as the change record (replaces = old stem and key)", "items": fixes})
subprocess.check_call([sys.executable, os.path.join(HERE, "shortcuts_num.py")])
sh = json.load(open("docs/research/shortcuts-num-001.json"))
sc = {x["id"]: x["shortcut"] for x in sh["shortcuts"]}
for p in sorted(glob.glob("docs/batches/batch-*.json")):
    d = json.load(open(p))
    for i in d["items"]:
        if i["id"] in sc:
            i["shortcut"] = sc[i["id"]]
    dump(p, d)
sh["status"] = "approved (CoS PASS 2026-10-13); merged into the batch items as `shortcut`"
dump("docs/research/shortcuts-num-001.json", sh)
for f in ["gap-fill-003", "filipino-supplement-001", "subprofessional-clerical-supplement-001", "subprofessional-general-info-supplement-001"]:
    p = f"docs/research/{f}.json"
    d = json.load(open(p))
    for i in d["items"]:
        i.update(APPROVE)
    d["status"] = "approved (CoS PASS 2026-10-13)"
    dump(p, d)
print(len(fixes), "rewrites merged;", len(sc), "shortcuts merged")
