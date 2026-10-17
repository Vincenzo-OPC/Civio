"""Apply CoS verdicts on chatgpt-batch-003 (2026-10-17): 89 approved (80 accept incl. fixed 060009 + 4 former holds, 8 variants), 11 rejected.
Variants share a fact_id with their approved bank twin (mock builder rule: one item per fact_id per mock; see docs/research/briefs)."""
import json
P = "docs/research/chatgpt-batch-003.json"
REJECT = {"060094", "060096", "060089", "060024", "060015", "060022", "060008", "060059", "060074", "060073", "060079"}
FACT = {  # variant -> (fact_id, bank twins)
 "060001": ("FACT-CONST-II-3-CIVILIAN-SUPREMACY", [("docs/batches/batch-006.json", "CIVIO-GI-TERM-MATCH-000507")]),
 "060017": ("FACT-CONST-IXB-2-2-MERIT-APPOINTMENT", [("docs/batches/batch-010.json", "CIVIO-GI-TERM-MATCH-000909")]),
 "060019": ("FACT-CONST-IXB-2-4-NO-PARTISAN-POLITICS", [("docs/batches/batch-004.json", "CIVIO-GI-TERM-MATCH-000303")]),
 "060020": ("FACT-CONST-IXB-2-5-SELF-ORGANIZATION", [("docs/batches/batch-010.json", "CIVIO-GI-TERM-MATCH-000902")]),
 "060057": ("FACT-RA6713-4A-G-ACCOUNTABILITY", [("docs/batches/batch-011.json", "CIVIO-GI-TERM-MATCH-001003")]),
 "060075": ("FACT-RA6713-9-DIVESTMENT-60-DAYS", [("docs/batches/batch-006.json", "CIVIO-GI-DEADLINE-NUMBER-000502"), ("docs/batches/batch-011.json", "CIVIO-GI-DEADLINE-NUMBER-001008")]),
 "060076": ("FACT-RA9003-SEGREGATION-AT-SOURCE", [("docs/research/subprofessional-general-info-supplement-001.json", "CIVIO-GI-20261013-0002")]),
 "060084": ("FACT-RA8749-2-PRINCIPLE", [("docs/research/subprofessional-general-info-supplement-001.json", "CIVIO-GI-20261013-0008")]),
}
WHEN = "2026-10-17"
def save(f, obj):
    nl = open(f).read().endswith("\n")
    open(f, "w").write(json.dumps(obj, ensure_ascii=False, indent=2) + ("\n" if nl else ""))
d = json.load(open(P))
n = {"approved": 0, "rejected": 0}
for it in d["items"]:
    s = it["id"][-6:]
    if s == "060009":
        o4 = next(o for o in it["options"] if o["option_id"] == "o4")
        o4["text"] = "A tax exemption needs two-thirds of all members of Congress."
        it["reveal"]["why_wrong"]["o4"] = "\"A tax exemption needs two-thirds of all members of Congress.\" is incorrect. Sec. 28(4) asks for a majority of all the Members of Congress, not two-thirds, and it is a voting rule for exemptions, not the uniformity and equity rule."
        it["distractor_reasoning"]["o4"] = "GI-NEIGHBOR-NUMBER"
        it["notes"] += " | CoS 2026-10-17: o4 was true under Art. VI, Sec. 28(4) (majority); changed to 'two-thirds'."
    if s in REJECT:
        it["status"], it["review_status"] = "draft", "rejected"
        it["reviewer"], it["reviewed_at"] = "Chief of Staff (final approval, delegated by GT)", WHEN
        it["notes"] += " | CoS 2026-10-17: rejected (fact duplicate / mirror). Not imported."
        n["rejected"] += 1
    else:
        it["status"], it["review_status"] = "approved", "passed"
        it["reviewer"], it["reviewed_at"] = "Chief of Staff (final approval, delegated by GT)", WHEN
        n["approved"] += 1
    if s in FACT:
        it["fact_id"] = FACT[s][0]
save(P, d)
for s, (fid, twins) in FACT.items():
    for f, iid in twins:
        b = json.load(open(f)); items = b["items"] if isinstance(b, dict) else b
        x = next(i for i in items if i["id"] == iid); x["fact_id"] = fid
        save(f, b)
print(n)
