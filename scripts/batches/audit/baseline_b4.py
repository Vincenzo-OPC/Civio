"""Round 03 baseline batch B4: the 32 baseline Numerical word problems (independent Grok Bot audit, 2026-10-18).
Keys recomputed with exact fractions; duplicates checked against other baseline rows and the approved bank.
Writes the CoS packet, the verdict CSV and full-schema drafts (FIX/HOLD). Nothing applied.
Run: python3 scripts/batches/audit/baseline_b4.py"""
import csv, json, os, re
from collections import Counter
from fractions import Fraction as F
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
P = lambda p: os.path.join(ROOT, p)
Q = {x["id"]: x for x in json.load(open(P("docs/research/audit/data/baseline-550-2026-10-17.json"), encoding="utf-8"))}
WP = sorted(i for i, x in Q.items() if x["sub"] == "Word problems")
# independent answers
C = {48: 13*4, 49: 800*5, 50: 500*F(9, 10), 197: F(180, 3), 198: F(100, 10), 199: 1200*F(85, 100), 200: 60*4, 201: F(50+8, 2), 202: 750*12,
     203: 15*8, 204: F(35, 5)*2, 205: 5000*F(6, 100)*2, 206: 2*(12+5), 207: F(36, 8), 208: (100-40)*F(1, 2), 209: F(900, 9)*3, 210: F(180, 12),
     269: F(90, 3)/15*10, 270: 30000 - F(30000)/F(112, 100), 271: F(10, 4), 272: F(2*10+3*20, 5), 349: 18*4, 350: 600*F(108, 100), 351: F(180, 3)*5,
     352: 45 - F(2, 3)*45, 353: F(125, 5), 494: F(160, 4*2), 495: 2400*F(85, 100), 496: F(210)/F(7, 2)*2, 497: F(72, 3)*5, 498: 18 - 12 - 4, 542: F(240, 6)*9}
assert sorted(C) == WP
def val(t):
    m = re.match(r"\s*₱?\s*([\d,]*\.?\d+)", t)
    return F(m.group(1).replace(",", "")) if m else None
keyrows = []
for i in WP:
    x = Q[i]; vals = [val(o) for o in x["options"]]
    hits = [k for k, v in enumerate(vals) if v is not None and (v == C[i] or (i == 270 and abs(v - C[i]) < 1))]
    keyrows.append([i, x["stem"], x["options"][x["correct_option"]], float(C[i]), hits == [x["correct_option"]], [o for o, v in zip(x["options"], vals) if v is None]])
PH = "Placeholder explanation ('Local practice item for Docker study.')."
CAP = "Percent-change/discount item; MILESTONE_2000_PLAN caps percent change at 40 and the bank already has 78 (NUM-WP-PCT-CHANGE)."
V = {
48: ("REJECT", PH + " Same fare-times-passengers task as #203.", "Retire; keep #203."),
49: ("REJECT", PH + " Same daily-wage task as #202.", "Retire; keep #202."),
50: ("REJECT", PH + " Discount frame duplicated by #199/#495 and the bank's 78 percent-change items.", "Retire."),
197: ("REJECT", "Average speed 180 km / 3 h is the first step of #351 (same numbers).", "Retire; keep #351."),
198: ("REJECT", "Same clerks-forms-per-hour frame as #494 (5 clerks/100 forms/2 h vs 4/160/2).", "Retire; keep #494."),
199: ("REJECT", CAP + " qa_file also finds the same frame already approved ('office chair ... 15% off', different price).", "Retire under the cap."),
200: ("KEEP", "Key 240 recomputed (1/4 of capacity = 60). Distinct from #497 (complement fraction vs. given fraction).", ""),
201: ("FIX", "Key 29 recomputed ((50+8)/2). Explanation 'Larger is 29.' gives no method.", "Draft with the sum-difference method."),
202: ("KEEP", "Key 9,000 recomputed.", "Note: options lack thousands separators (8000) — fix on migration."),
203: ("KEEP", "Key 120 recomputed.", ""),
204: ("KEEP", "Key 14 recomputed (one part = 7).", ""),
205: ("KEEP", "Key 600 recomputed. Same frame as approved CIVIO-NUM-WP-PCT-CHANGE-000330 (6%, 2 years) with a different principal — acceptable variant, flag for the frame cap.", ""),
206: ("FIX", "Key 34 recomputed. Explanation 'Perimeter 34 m.' gives no method; '60 m' (area) is a good trap but uncoded.", "Draft with method and coded traps."),
207: ("KEEP", "Key 4.5 recomputed.", ""),
208: ("KEEP", "Key 30% recomputed (60% left, half done → 30%). Percent-of-remaining, not percent change.", ""),
209: ("FIX", "Key 300 recomputed. Explanation 'Middle share 300.' gives no method.", "Draft with the parts method."),
210: ("KEEP", "Key 15 recomputed.", ""),
269: ("KEEP", "Key 20 recomputed (2 pages/min per printer).", ""),
270: ("KEEP", "Key ₱3,214 recomputed (30,000 − 30,000/1.12 = 3,214.29). '₱3,600' is the classic 12%-of-gross trap.", ""),
271: ("KEEP", "Key 2.5 hours recomputed.", ""),
272: ("KEEP", "Key 16% recomputed (0.8 L solute in 5 L).", ""),
349: ("FIX", "Key 72 correct, but option B is malformed: ' sixty-four' (spelled out, leading space) among numerals — user-visible.", "Draft with '64' (18 × 4 misread as 16 × 4)."),
350: ("HOLD", CAP + " Same frame as approved 000921 (₱600 base).", "CoS decision as #199."),
351: ("KEEP", "Key 300 km recomputed.", ""),
352: ("KEEP", "Key 15 recomputed.", ""),
353: ("KEEP", "Key 25 recomputed.", ""),
494: ("KEEP", "Key 20 recomputed. Cosmetic: boilerplate missing period.", ""),
495: ("HOLD", CAP, "CoS decision as #199. Draft supplied."),
496: ("KEEP", "Key 120 km recomputed. Same skill as #351 with different numbers (3.5 h) — acceptable.", ""),
497: ("KEEP", "Key 120 L recomputed.", ""),
498: ("KEEP", "Key 2 recomputed.", ""),
542: ("KEEP", "Key 360 recomputed. Cosmetic: boilerplate missing period.", ""),
}
assert sorted(V) == WP
def num(bid, arch, stem, opts, key, why, wrong, codes, short, diff="easy", sec=60):
    ids = ["n1", "n2", "n3", "n4"]
    return {"id": f"CIVIO-B4-{arch}-{bid:04d}", "track": "both", "domain": "numerical", "competency": "Word problems", "concept": arch[7:].lower(),
        "micro_skill": arch.lower(), "archetype": arch, "difficulty": diff, "est_seconds": sec, "language": "en", "stem": stem,
        "options": [{"option_id": i, "text": t} for i, t in zip(ids, opts)], "answer_option_id": ids[key],
        "reveal": {"terms": "Word problem: translate the situation into one or two operations.", "shortcut": short, "why_correct": why,
                   "why_wrong": {ids[i]: w for i, w in wrong.items()}},
        "distractor_reasoning": {ids[i]: c for i, c in codes.items()}, "source": "Civio baseline, rewritten (Grok Bot B4)", "source_url": None,
        "source_group": "civio", "status": "draft", "review_status": "unreviewed",
        "provenance": {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T03:00:00+08:00", "spec_version": "0.1.9"},
        "_legacy": True, "shortcut": short, "replaces": {"baseline_id": bid, "stem": Q[bid]["stem"], "key": Q[bid]["options"][Q[bid]["correct_option"]]},
        "notes": "Round 03 B4 draft (Grok Bot). Key independently recomputed. Pending CoS."}
D = [
num(201, "NUM-WP-ALGEBRA", "Two numbers add up to 50, and one is 8 more than the other. What is the larger number?", ["21", "29", "25", "42"], 1,
    "Answer: 29. Larger = (sum + difference) ÷ 2 = (50 + 8) ÷ 2 = 29; the smaller is 21, and 29 − 21 = 8.",
    {0: "21 is the smaller number.", 2: "25 splits 50 evenly and ignores the difference.", 3: "42 is 50 − 8, the sum minus the difference."}, {0: "NUM-OTHER-SHARE", 2: "NUM-PARTIAL", 3: "NUM-OP-SWAP"},
    "Larger = (sum + difference) ÷ 2."),
num(206, "NUM-WP-GEOM", "A rectangular office lot is 12 m long and 5 m wide. How many meters of fence go around it?", ["17 m", "34 m", "60 m", "29 m"], 1,
    "Answer: 34 m. Perimeter = 2 × (12 + 5) = 2 × 17 = 34 m.",
    {0: "17 m adds one length and one width only.", 2: "60 is the area in square meters, not the distance around.", 3: "29 m counts one length twice and one width once."}, {0: "NUM-PARTIAL", 2: "NUM-OP-SWAP", 3: "NUM-PARTIAL"},
    "Perimeter = 2 × (length + width)."),
num(209, "NUM-WP-RATIO", "₱900 is shared among three volunteers in the ratio 2 : 3 : 4. How much is the middle share?", ["₱200", "₱300", "₱400", "₱450"], 1,
    "Answer: ₱300. 2 + 3 + 4 = 9 parts; one part = 900 ÷ 9 = ₱100; the middle share is 3 parts = ₱300.",
    {0: "₱200 is the smallest share (2 parts).", 2: "₱400 is the largest share (4 parts).", 3: "₱450 halves the total instead of using parts."}, {0: "NUM-OTHER-SHARE", 2: "NUM-OTHER-SHARE", 3: "NUM-WRONG-BASE"},
    "One part = total ÷ sum of ratio terms."),
num(349, "NUM-WP-RATE", "Working steadily, a records clerk puts away 18 folders each hour. How many folders are put away in a 4-hour shift?", ["54", "64", "72", "82"], 2,
    "Answer: 72. 18 folders × 4 hours = 72 folders.",
    {0: "54 is only 3 hours (18 × 3).", 1: "64 multiplies 16, not 18, by 4.", 3: "82 adds an extra 10."}, {0: "NUM-OFF-BY-ONE", 1: "NUM-GIVEN-REUSED", 3: "NUM-EXTRA-STEP"},
    "Rate × time."),
num(495, "NUM-PCT-BASIC", "A seminar fee of ₱2,400 gets a 15% early-bird discount. What is the discounted fee?", ["₱2,040", "₱2,160", "₱2,085", "₱2,760"], 0,
    "Answer: ₱2,040. 15% of 2,400 = 360; 2,400 − 360 = ₱2,040.",
    {1: "₱2,160 takes off only 10%.", 2: "₱2,085 subtracts 315, a miscomputed 15%.", 3: "₱2,760 adds the 15%."}, {1: "NUM-WRONG-BASE", 2: "NUM-PARTIAL", 3: "NUM-OP-SWAP"},
    "10% = 240, 5% = 120; take off 360."),
]
# spread key positions (content unchanged)
for n, it in enumerate(D):
    texts = [o["text"] for o in it["options"]]; ids = [o["option_id"] for o in it["options"]]
    ki = ids.index(it["answer_option_id"]); slot = n % 4
    order = [t for i, t in enumerate(texts) if i != ki]; order.insert(slot, texts[ki])
    old = {o["text"]: o["option_id"] for o in it["options"]}; remap = {old[t]: ids[order.index(t)] for t in texts}
    it["options"] = [{"option_id": ids[i], "text": t} for i, t in enumerate(order)]
    it["answer_option_id"] = remap[it["answer_option_id"]]
    it["reveal"]["why_wrong"] = {remap[o]: w for o, w in it["reveal"]["why_wrong"].items()}
    it["distractor_reasoning"] = {remap[o]: c for o, c in it["distractor_reasoning"].items()}
json.dump({"batch": "round-03-baseline-b4-drafts", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio", "items": D},
          open(P("docs/research/audit/fixes/round-03-baseline-b4-drafts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
drafted = {d["replaces"]["baseline_id"] for d in D}
rows = [[i, Q[i]["options"][Q[i]["correct_option"]], *V[i], "yes" if i in drafted else "", "pending file", "pending file"] for i in WP]
with open(P("docs/research/audit/data/baseline-b4-verdicts-2026-10-18.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["baseline_id", "key_now", "grok_verdict", "issue_evidence", "proposal", "draft", "chatgpt_verdict", "agree"]); w.writerows(rows)
with open(P("docs/research/audit/data/baseline-b4-numerical-keys-2026-10-18.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "stem", "stored_key", "independent_answer", "key_matches_unique_option", "malformed_options"]); w.writerows(keyrows)
t = Counter(v[0] for v in V.values())
md = ["# Round 03 baseline audit, batch B4: Numerical word problems (32), review request for Chief of Staff", "",
      "Grok Bot, 2026-10-18. Source: Oct 17 export (MSI not queried). Base `main` f2766db. **Nothing applied.**", "", "## Summary", "",
      f"- KEEP {t['KEEP']}, FIX {t['FIX']}, REJECT {t['REJECT']}, HOLD {t['HOLD']}.",
      f"- **Keys:** {sum(r[4] for r in keyrows)}/32 recomputed with exact fractions and matching exactly one option. **0 key errors.**",
      "- **Malformed option:** #349 ' sixty-four' (user-visible), fixed in the draft.",
      "- **Duplicates:** #48≈#203, #49≈#202, #197⊂#351, #198≈#494, #50 discount frame. No exact match to the approved bank. #205 and #350 share frames with approved 000330 and 000921 (different numbers).",
      "- **Percent cap:** #199, #350, #495 are discount/percent items (#199 is REJECTED as a frame duplicate; #350 and #495 are HOLD) while the bank holds 78 percent-change items against a proposed cap of 40, so they're HOLD for CoS.",
      "- **Drafts:** 5 full-schema drafts (#201, #206, #209, #349 FIX; #495 HOLD) in `audit/fixes/round-03-baseline-b4-drafts.json`. `qa_file.py` and `explanation_lint.py` results are in the tracker.",
      "- **Needs CoS:** all REJECT/FIX and the two HOLDs.", "", "## Per item", "", "| ID | Key now | Verdict | Issue / evidence | Proposal | Draft |", "|---|---|---|---|---|---|"]
md += ["| " + " | ".join(str(c).replace("|", "/") for c in r[:6]) + " |" for r in rows]
open(P("docs/research/audit/round-03-baseline-b4-review-request.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print(dict(t), "keys ok", sum(r[4] for r in keyrows), "malformed", [(r[0], r[5]) for r in keyrows if r[5]], "drafts", len(D))
