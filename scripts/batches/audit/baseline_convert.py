"""Convert the 550-row baseline export to the full spec schema so qa_file.py can check it.
Input: docs/research/audit/data/baseline-550-2026-10-17.json (MSI export, pre-verdict text) plus the CoS-approved
change sets already applied on the MSI (audit/fixes/round-03-baseline-b1b2-cos.json updates + retire,
round-03-baseline-b1-spelling-swaps.json). Output mirrors current state:
docs/research/audit/data/baseline-550-spec-2026-10-18.json. Every item is status 'draft' (the qa schema's only
non-approved state); the real DB state is kept in `baseline_state` (active / retired) — this file changes no status.
Fields the baseline never had (distractor codes, per-option why_wrong, terms, shortcut) are left EMPTY on purpose so
QA reports them; nothing is invented. Run: python3 scripts/batches/audit/baseline_convert.py"""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
P = lambda p: os.path.join(ROOT, p)
rows = {x["id"]: dict(x) for x in json.load(open(P("docs/research/audit/data/baseline-550-2026-10-17.json"), encoding="utf-8"))}
cos = json.load(open(P("docs/research/audit/fixes/round-03-baseline-b1b2-cos.json"), encoding="utf-8"))
sw = json.load(open(P("docs/research/audit/fixes/round-03-baseline-b1-spelling-swaps.json"), encoding="utf-8"))["swaps"]
for u in cos["updates"]:
    rows[u["id"]].update(u["new"]); rows[u["id"]]["_applied"] = "round-03-b1b2-cos"
swapped = set()
for s in sw:
    r = rows[s["baseline_id"]]; swapped.add(s["baseline_id"])
    r.update(stem=s["stem"], options=s["options"], correct_option=s["correct_option"], explanation=s.get("explanation", r["explanation"]), _applied="round-03-b1-spelling-swaps")
retired = set(cos["retire"]) - swapped
DOM = {"General Information": "general_information", "Numerical Ability": "numerical", "Analytical Ability": "analytical", "Clerical Ability": "clerical"}
def dom(r): return ("verbal_fil" if r["language"] == "Filipino" else "verbal_en") if r["cat"] == "Verbal Ability" else DOM[r["cat"]]
TRACK = {"analytical": "professional", "clerical": "subprofessional"}
out = []
for i, r in sorted(rows.items()):
    d = dom(r); ids = [f"o{k+1}" for k in range(len(r["options"]))]; key = ids[r["correct_option"]]
    out.append({"id": f"CIVIO-BASELINE-{i:04d}", "track": TRACK.get(d, "both"), "domain": d, "competency": r["sub"], "concept": r["sub"].lower(),
        "micro_skill": "", "archetype": "BASELINE-" + d.upper(), "difficulty": "", "est_seconds": None,
        "language": "fil" if r["language"] == "Filipino" else "en", "stem": r["stem"],
        "options": [{"option_id": o, "text": t} for o, t in zip(ids, r["options"])], "answer_option_id": key,
        "reveal": {"terms": "", "shortcut": "", "why_correct": r.get("explanation") or "", "why_wrong": {}},
        "distractor_reasoning": {}, "source": "Civio baseline (legacy local bank)", "source_url": None, "source_group": "civio",
        "status": "draft", "review_status": "unreviewed", "baseline_state": "retired" if i in retired else "active",
        "baseline_id": i, "applied_change_set": r.get("_applied"),
        "provenance": {"author": "baseline (unknown)", "method": "legacy_import", "created_at": None, "spec_version": "0.1.9"},
        "_legacy": True, "notes": "Schema conversion only (Grok Bot 2026-10-18). source_group is 'civio' only because qa.py requires it; the DB row stays source_group='baseline'."})
json.dump({"batch": "baseline-550-spec", "spec_version": "0.1.9", "status": "conversion (not for import)", "source_group": "baseline",
           "counts": {"total": len(out), "active": sum(o["baseline_state"] == "active" for o in out), "retired": len(retired)}, "items": out},
          open(P("docs/research/audit/data/baseline-550-spec-2026-10-18.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "items;", sum(o["baseline_state"] == "active" for o in out), "active;", len(retired), "retired")
