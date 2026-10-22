"""Release Collection manifest: select EXACTLY EV300 FV300 Num400 Ana400 Cler300 GI300 = 2,000 with round subtopic quotas.
Pool = approved Civio items (docs/batches, docs/research; status approved/passed) + active baseline rows from the converted export
that are not proposed REJECT in any round-03 baseline verdict CSV. --include-drafts adds pending draft files (projection only).
Selection inside each subtopic: lint-clean first (explanation_lint), then Civio before baseline, then stable id order.
Over-target pools are trimmed by selection only: nothing is deleted or demoted. Under-target subtopics are reported as shortfalls.
Writes docs/research/release/release-collection-manifest.json and verifies counts; exit 1 if any subject or subtopic is not exact.
Usage: python3 scripts/batches/release/release_manifest.py [--include-drafts] [--baseline PATH] [--out PATH]"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "batches", "audit"))
import explanation_lint as L
QUOTA = {
 "verbal_en": {"word meaning": 45, "sentence completion": 60, "error recognition": 60, "sentence structure": 30, "paragraph organization": 45, "reading comprehension": 60},
 "verbal_fil": {"synonym": 75, "antonym": 60, "idiom": 45, "grammar": 45, "reading": 45, "paragraph order": 30},
 "numerical": {"basic operations": 120, "number sequence": 80, "word problems": 200},
 "analytical": {"word analogy": 120, "symbolic logic": 80, "assumptions and conclusions": 100, "data interpretation": 100},
 "clerical": {"filing": 165, "spelling": 135},
 "general_information": {"constitution": 120, "ra 6713": 90, "peace and human rights": 50, "environment": 40},
}
TARGET = {d: sum(q.values()) for d, q in QUOTA.items()}
assert sum(TARGET.values()) == 2000
def subtopic(it):
    d, a, c = it["domain"], it.get("archetype", ""), (it.get("competency") or "").lower()
    if d == "verbal_en":
        for k, pats in [("word meaning", ["WORD-MEANING", "word meaning", "vocab"]), ("sentence completion", ["SENT-COMP", "completion"]), ("error recognition", ["ERROR", "error"]),
                        ("sentence structure", ["STRUCTURE", "structure"]), ("paragraph organization", ["PARA", "VEN-PO", "paragraph"]), ("reading comprehension", ["RC", "reading"])]:
            if any(p in a or p in c for p in pats): return k
    if d == "verbal_fil":
        m = {"VFIL-KASINGKAHULUGAN": "synonym", "VFIL-VOCAB": "synonym", "VFIL-KASALUNGAT": "antonym", "VFIL-WIKAIN": "idiom", "VFIL-BALARILA": "grammar", "VFIL-GRAM": "grammar",
             "VFIL-COMP": "grammar", "VFIL-PAGBASA": "reading", "VFIL-READ": "reading", "VFIL-PAGSUSUNOD": "paragraph order", "VFIL-PARA": "paragraph order"}
        return m.get(a) or ("grammar" if "completion" in c or "structure" in c else "reading" if "reading" in c else "paragraph order" if "paragraph" in c else "synonym" if "meaning" in c else None)
    if d == "numerical":
        if "SEQ" in a or "sequence" in c: return "number sequence"
        if a.startswith("NUM-WP") or "word problem" in c: return "word problems"
        return "basic operations"
    if d == "analytical":
        if "ANALOGY" in a or "analogy" in c: return "word analogy"
        if "SYMBOL" in a or "symbolic" in c or a == "ANA-SYLLOGISM" or c == "logic": return "symbolic logic" if ("SYMBOL" in a or "symbolic" in c) else "assumptions and conclusions"
        if "ASSUME" in a or "CONCLUSION" in a or "assumption" in c: return "assumptions and conclusions"
        if "DI-" in a or "data" in c: return "data interpretation"
    if d == "clerical":
        return "spelling" if ("SPELL" in a or "spelling" in c) else "filing"
    if d == "general_information":
        if "6713" in c or "code of conduct" in c: return "ra 6713"
        if any(k in c for k in ["environment", "air", "water", "waste", "climate", "compost", "wildlife", "habitat", "ecolog", "polluter", "segregation", "endemic", "anthropogenic", "land-based", "solid", "public participation", "government responsibility"]): return "environment"
        if any(k in c for k in ["peace", "human rights", "harassment", "safe spaces", "online safety", "public-space", "equal protection"]): return "peace and human rights"
        return "constitution"
    return None
def load(paths, approved_only=True):
    out, seen = [], set()
    for f in paths:
        try: d = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        items = d.get("items") if isinstance(d, dict) else d
        if not isinstance(items, list): continue
        for i in items:
            if not isinstance(i, dict) or "options" not in i or "answer_option_id" not in i or i["id"] in seen: continue
            if approved_only and not (i.get("status") == "approved" and i.get("review_status") == "passed"): continue
            if not approved_only and (i.get("status") != "draft" or i.get("review_status") == "rejected"): continue
            seen.add(i["id"]); out.append(dict(i, _file=os.path.relpath(f, ROOT)))
    return out
def main():
    a = sys.argv[1:]
    bpath = a[a.index("--baseline") + 1] if "--baseline" in a else os.path.join(ROOT, "docs/research/audit/data/baseline-550-spec-2026-10-18.json")
    outp = a[a.index("--out") + 1] if "--out" in a else os.path.join(ROOT, "docs/research/release/release-collection-manifest.json")
    files = sorted(glob.glob(os.path.join(ROOT, "docs/batches/batch-*.json"))) + sorted(f for f in glob.glob(os.path.join(ROOT, "docs/research/*.json")) if "round-02-fixes" not in f and "shortcuts" not in f)
    pool = load(files)
    rej = set()
    for f in glob.glob(os.path.join(ROOT, "docs/research/audit/data/baseline-b*-verdicts-*.csv")):
        rej |= {int(r["baseline_id"]) for r in csv.DictReader(open(f, encoding="utf-8")) if r.get("grok_verdict") == "REJECT"}
    if os.path.exists(bpath):
        for b in json.load(open(bpath, encoding="utf-8"))["items"]:
            if b.get("baseline_state") == "active" and b["baseline_id"] not in rej: pool.append(dict(b, _file="baseline"))
    if "--include-drafts" in a:
        pool += load([f for f in files] + glob.glob(os.path.join(ROOT, "docs/research/audit/fixes/*-drafts.json")), approved_only=False)
    by = defaultdict(list)
    for it in pool:
        s = subtopic(it)
        if s: by[(it["domain"], s)].append(it)
    manifest, report, ok = {}, [], True
    for d, q in QUOTA.items():
        manifest[d] = {}
        for s, n in q.items():
            cand = sorted(by[(d, s)], key=lambda i: (bool(L.lint_item(i)), i["_file"] == "baseline", i.get("status") != "approved", i["id"]))
            pick = cand[:n]; manifest[d][s] = [i["id"] for i in pick]
            report.append((d, s, n, len(cand), len(pick), sum(not L.lint_item(i) for i in pick)))
            ok &= len(pick) == n
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    json.dump({"targets": QUOTA, "include_drafts": "--include-drafts" in a, "baseline_rejects_excluded": len(rej), "manifest": manifest}, open(outp, "w", encoding="utf-8"), indent=1)
    print(f"{'subject':20} {'subtopic':28} {'quota':>5} {'pool':>5} {'picked':>6} {'lint-clean':>10} {'short':>5}")
    for d, s, n, p, k, c in report: print(f"{d:20} {s:28} {n:5} {p:5} {k:6} {c:10} {n-k:5}")
    tot = {d: sum(len(v) for v in manifest[d].values()) for d in manifest}
    print("subject totals:", tot, "sum", sum(tot.values()), "target 2000")
    ids = [i for d in manifest.values() for v in d.values() for i in v]
    assert len(ids) == len(set(ids)), "duplicate id in manifest"
    print("EXACT" if ok and sum(tot.values()) == 2000 else "NOT EXACT (shortfalls above)")
    sys.exit(0 if ok else 1)
if __name__ == "__main__": main()
