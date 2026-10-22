"""Round 03 baseline batch B3 (independent Grok Bot audit, 2026-10-18).
Scope: ChatGPT's 100-item scope plus the full Number-sequence group = 123 baseline items
(GI R.A. 6713 37, GI Environment 27, Numerical Basic operations 31, Number sequence 28).
Reads docs/research/audit/data/baseline-550-2026-10-17.json (MSI export, read-only). Nothing is applied.
Writes:
  docs/research/audit/round-03-baseline-b3-review-request.md   (CoS packet)
  docs/research/audit/data/baseline-b3-verdicts-2026-10-18.csv (one row per item; ChatGPT columns 'pending file')
  docs/research/audit/fixes/round-03-baseline-b3-drafts.json   (full-schema drafts for FIX/HOLD items, status draft)
Run: python3 scripts/batches/audit/baseline_b3.py"""
import csv, json, os, re
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC = os.path.join(ROOT, "docs/research/audit/data/baseline-550-2026-10-17.json")
Q = {x["id"]: x for x in json.load(open(SRC, encoding="utf-8"))}
L6713 = "https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html"
L9003 = "https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html"
L8749 = "https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html"
L9729 = "https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html"
L11038 = "https://lawphil.net/statutes/repacts/ra2018/ra_11038_2018.html"
L11898 = "https://lawphil.net/statutes/repacts/ra2022/ra_11898_2022.html"
L9275 = "https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html"
PH = "Placeholder explanation ('Local practice item for Docker study.')."
JK = "joke/absurd distractors make the key obvious"
LK = "key is the only long, statute-worded option (length giveaway)"
def dup(ref, why=""): return ("REJECT", f"Duplicate of approved bank item {ref}{why}.", "Retire the baseline row to draft (history kept); the bank item already has full spec metadata.")
def bdup(keep, why=""): return ("REJECT", f"Duplicate of baseline #{keep}{why}.", f"Retire; keep #{keep}.")

# ---------- verdicts: id -> (verdict, issue/evidence, proposal) ----------
V = {
# R.A. 6713 (37)
6: dup("CIVIO-GI-TERM-MATCH-000302", " (short title, Sec. 1)"),
7: dup("CIVIO-GI-TERM-MATCH-000810", " (Sec. 4(A)(a)); also placeholder explanation"),
8: ("REJECT", PH + " Vague ('an example of transparency'); its key restates #72's topic, so the pair discloses each other. No statutory anchor: R.A. 6713 has no 'disclosure of conflict' norm as such (conflict is handled by Sec. 9 divestment).", "Retire; conflict of interest is covered by #388 (Sec. 3(i)) and #72 (rewritten)."),
66: dup("CIVIO-GI-TERM-MATCH-000810", " (Sec. 4(A)(a)); same as baseline #7 and #379"),
67: ("FIX", "Key correct (Sec. 8(A): within 30 days after assumption, on or before April 30 every year, within 30 days after separation). Explanation uncited; " + LK + "; 'Only if salary exceeds a fixed threshold' is a fair trap but the other two are weak.", "Draft: same triad fact, balanced options built from real wrong combinations (wrong deadline numbers), cite Sec. 8(A)(a)-(c). Not a duplicate of 000403/000511/060072, which test one deadline each."),
68: dup("CIVIO-GI-TERM-MATCH-000405", " and 060070 (Sec. 7(d) gifts)"),
69: dup("CIVIO-GI-SCENARIO-APPLY-060064", " (Sec. 5(e) documents accessible); explanation uncited and 'Keeping all procurement secret until after award forever' is a joke option"),
70: ("REJECT", "Overlaps #389 (definition, Sec. 3(j)) and approved 000502/060075 (60-day period, Sec. 9). Key 'within a required period' is vague.", "Retire; keep #389."),
71: dup("CIVIO-GI-TERM-MATCH-000402", " and 060058 (simple living, Sec. 4(A)(h))"),
72: ("FIX", "Key is defensible as common usage, but the scenario (a relative owns a bidder) is NOT R.A. 6713's definition of conflict of interest, which is about the official's own board seat, office, substantial stock or business interest (Sec. 3(i)); relatives fall under Sec. 4(A)(c) and R.A. 3019. Distractors are joke options. Discloses #8.", "Draft: scenario where the official is a substantial stockholder of a bidder; cite Sec. 3(i) and Sec. 9."),
73: ("REJECT", "R.A. 6713 has no whistleblowing provision; the key ('consistent with the duty to uphold public interest') is an inference, distractors are joke options. Not testable against the statute.", "Retire. Whistleblower protection is outside R.A. 6713."),
223: ("REJECT", "Disposal of government property is governed by P.D. 1445 (Government Auditing Code) and COA rules, not R.A. 6713. Joke distractors ('Social media announcement', 'Family consent').", "Retire (wrong law for this subtopic)."),
224: ("HOLD", "Anti-nepotism in appointments is E.O. 292 (Administrative Code of 1987), Book V, Sec. 59, not R.A. 6713; R.A. 6713 only bars undue favors to relatives (Sec. 4(A)(c)), already tested by #395. 'Merit-based promotions' and 'Use of email' are weak.", "CoS: recategorize to a civil-service-law item (needs E.O. 292 text check) or retire. No draft until decided."),
225: dup("CIVIO-GI-TERM-MATCH-000309", " and 060052 (professionalism, Sec. 4(A)(b)); joke distractors"),
379: dup("CIVIO-GI-TERM-MATCH-000810", " (Sec. 4(A)(a)); same as baseline #7 and #66"),
380: dup("CIVIO-GI-SCENARIO-APPLY-060070", " (gift tied to a pending transaction, Sec. 7(d)); joke distractors ('wrapped')"),
381: dup("CIVIO-GI-DEADLINE-NUMBER-000020", " and 000708 (15 working days, Sec. 5(a))"),
382: dup("CIVIO-GI-DEADLINE-NUMBER-060072", " (April 30, Sec. 8(A)(b))"),
383: dup("CIVIO-GI-DEADLINE-NUMBER-000403", " and 060071 (30 days after assumption, Sec. 8(A)(a))"),
384: dup("CIVIO-GI-DEADLINE-NUMBER-000511", " (30 days after separation, Sec. 8(A)(c))"),
385: dup("CIVIO-GI-TERM-MATCH-000807", " and 060054 (political neutrality, Sec. 4(A)(d))"),
386: dup("CIVIO-GI-TERM-MATCH-000402", " and 060058 (simple living)"),
387: dup("CIVIO-GI-TERM-MATCH-000309", " (professionalism)"),
388: ("FIX", "Key correct (Sec. 3(i) 'may be opposed to or affected by the faithful performance of official duty'). Stem omits that the interest is a board seat, office, substantial stock or business interest; " + LK + "; 'A public holiday' is a joke option.", "Draft with the full Sec. 3(i) trigger and sibling distractors (Sec. 7(a) financial interest, Sec. 4(A)(c) relatives, Sec. 9 divestment)."),
389: ("FIX", "Key correct (Sec. 3(j)): transfer of title voluntarily, completely and actually, to someone other than spouse and relatives. The key omits the spouse/relatives limit, which is the testable point; joke distractors ('Borrowing a colleague's ID').", "Draft: options contrast transfer to spouse/relative (not divestment), listing in the SALN, resignation (Sec. 9 resign rule) — cite Sec. 3(j), Sec. 9."),
390: dup("CIVIO-GI-TERM-MATCH-000908", " and 060069 (confidential information, Sec. 7(c))"),
391: dup("CIVIO-GI-SCENARIO-APPLY-060064", " (Sec. 5(e)); same fact as baseline #69"),
392: dup("CIVIO-GI-DEADLINE-NUMBER-000203", " and 060062 (three signatories, Sec. 5(c))"),
393: ("FIX", "Key correct (Sec. 12: CSC has primary responsibility for administration and enforcement). Not in the approved bank (000202 tests the awards committee). Distractors 'Department of Tourism', 'A private contractor' are implausible; boilerplate missing period.", "Draft with real sibling bodies: Office of the Ombudsman (receives SALN copies / prosecutes), COA, Sandiganbayan."),
394: dup("CIVIO-GI-SCENARIO-APPLY-060068", " (recommending a person to a firm with a pending transaction, Sec. 7(b)(4))"),
395: ("FIX", "Key correct (Sec. 4(A)(c) undue favors to relatives) but the testable exception (confidential positions and coterminous personal staff) is missing; joke distractors ('award every contract to relatives').", "Draft: test the statutory exception; cite Sec. 4(A)(c)."),
396: ("FIX", "Key correct (Sec. 8 opening paragraph); joke distractors ('favorite books'); the family scope (spouse, unmarried children under 18 living in the household) is the better testable fact.", "Draft on whose interests must be declared; cite Sec. 8."),
397: ("FIX", "Key correct (Sec. 7(d), Congress consents to a foreign-government gift of nominal value received as souvenir or mark of courtesy; also scholarships/medical treatment and certain travel grants). Distractors are bribes, so the key is obvious.", "Draft listing real Sec. 7(d) categories vs. non-consented ones."),
398: dup("CIVIO-GI-TERM-MATCH-000807", " (political neutrality); same as baseline #385"),
524: dup("CIVIO-GI-SCENARIO-APPLY-060051", " (official vehicle for a private holiday, Sec. 4(A)(a)); distractors are unrelated constitutional topics"),
525: dup("CIVIO-GI-TERM-MATCH-000610", " and 060055 (responsiveness, Sec. 4(A)(e)); the key is the only competent-sounding option"),
526: ("FIX", "Defensible but uncited; R.A. 6713 Sec. 10(a) says the reviewing body informs the filer and directs corrective action. Joke distractors.", "Draft anchored to Sec. 10(a)."),
# Environment (27)
11: ("FIX", PH + " Distractors are absurd ('Scientific research').", "Draft citing the Brundtland definition as adopted in R.A. 9003, Sec. 2(c) 'ecologically sustainable development principles'; sibling distractors (conservation-only, zero use, growth-first)."),
12: bdup(83, " (EIA purpose); placeholder explanation; joke distractors"),
82: bdup(405, " (R.A. 9003 subject)"),
83: ("FIX", "Key correct (P.D. 1586, Philippine EIS System). Explanation uncited; 'Applies only to residential backyard gardens' is a joke option.", "Draft citing P.D. 1586 (EIS System); distractors: replaces ECC? no — use real confusions (post-construction audit, LGU permit, tax incentive). Source text to be checked on LawPhil (P.D. 1586) before CoS."),
84: bdup(410, " (precautionary principle)"),
85: dup("CIVIO-GI-ENV-PRINCIPLE-060095", " (adaptation, R.A. 9729); joke distractors"),
86: ("HOLD", "Common-sense item, joke distractors ('Stock market indexes', 'Postal delivery'). Needs a P.D. 705 (Revised Forestry Code) anchor that I have not verified on LawPhil in this session.", "Rewrite after P.D. 705 text check, or retire."),
87: dup("CIVIO-GI-20261013-0002", " and 060076 (segregation at source, R.A. 9003 Sec. 21)"),
88: bdup(413, " (protected areas)"),
89: bdup(414, " (DENR)"),
228: ("FIX", "Key correct; 'Only produce oil', 'Block all rainfall' are joke options; no source.", "Draft citing R.A. 9275 Sec. 5 (water quality management areas use watersheds/river basins as units); sibling distractors."),
229: ("FIX", "Key correct (R.A. 9003 Sec. 37 prohibits open dumps; Sec. 3(t) defines them). 'Improves groundwater always' is a joke; 'Is required by R.A. 9003' is a good GI-OLD-RULE-style trap.", "Draft citing Secs. 3(t), 37, 48(9)."),
405: ("FIX", "Key correct (R.A. 9003 Sec. 1). Note: R.A. 9003 was amended by R.A. 11898 (EPR Act of 2022); short title unchanged. Distractors 'Data Privacy Act', 'Civil Service Law' are off-domain giveaways.", "Draft with environmental sibling laws only (R.A. 8749, 9275, 6969)."),
406: dup("CIVIO-GI-20261013-0002", " (segregation at source); same as baseline #87"),
407: dup("CIVIO-GI-20261013-0003", " and 060082 (composting)"),
408: ("FIX", "Key correct (R.A. 8749 Sec. 1). Distractors 'Anti-Graft', 'Cybercrime' are off-domain giveaways.", "Draft with environmental siblings (R.A. 9003, 9275, 9729)."),
409: bdup(83, " (EIA purpose)"),
410: ("FIX", "Key correct; R.A. 9729 Sec. 2 adopts the Precautionary Principle for climate risk decisions (also Rule 20, Rules of Procedure for Environmental Cases, A.M. 09-6-8-SC). Joke distractors ('Harm is certain to be harmless').", "Draft citing R.A. 9729 Sec. 2."),
411: bdup(228, " (watershed); 'Stores only marine passwords' is a joke option"),
412: ("FIX", "Key correct but " + JK + "; uncited.", "Draft citing R.A. 9003 Sec. 21 (segregation at source) and Sec. 48(1) (littering/dumping in canals and esteros is prohibited)."),
413: ("FIX", "Key correct (R.A. 7586 Sec. 2 as amended by R.A. 11038 (E-NIPAS Act of 2018)). Joke distractors.", "Draft citing R.A. 11038 Sec. 2 (amending R.A. 7586 Sec. 2)."),
414: ("FIX", "Key correct; off-domain distractors (BIR, LTO, PSA) make it trivial.", "Draft with environment-adjacent agencies (EMB is a DENR bureau, DA-BFAR, MMDA, NWRB) asking which department is primary. Cite E.O. 192 (1987) — text check pending."),
417: ("FIX", "Key correct; R.A. 11898 (2022) inserted a 'circular economy' definition into R.A. 9003 Sec. 3(d-1). Joke distractors.", "Draft citing R.A. 9003 Sec. 3(d-1) as amended by R.A. 11898."),
418: dup("CIVIO-GI-ENV-PRINCIPLE-060083", " (open burning, R.A. 9003 Sec. 48(3))"),
527: ("FIX", "Key correct (R.A. 9003 Sec. 2(c): avoidance and volume reduction through source reduction, reuse, recycling and recovery before disposal). Joke distractors; uncited.", "Draft citing Sec. 2(c)."),
528: ("FIX", "Key correct (ecology concept, no statute needed); joke distractors.", "Draft with plausible ecological siblings (carbon only, freshwater recharge, fisheries ban)."),
529: ("REJECT", "Records-management office practice, not Environment Management and Protection; reads as a Clerical item.", "Retire."),
# Numerical Basic operations (31)
41: ("FIX", PH + " One-step addition is below CSE difficulty but valid as an easy warm-up.", "Draft with coded distractors (carry error, off by one)."),
42: ("FIX", PH, "Draft with coded distractors."),
43: ("FIX", PH, "Draft with coded distractors."),
44: ("FIX", PH, "Draft with coded distractors (borrow error)."),
173: ("FIX", PH, "Draft; same frame as #340/#486/#184 — keep but vary stems."),
174: ("KEEP", "Key 17/12 recomputed; explanation correct.", "Migrate to schema later (codes, why_wrong)."),
175: ("FIX", PH, "Draft."),
176: ("FIX", PH, "Draft (16 = 2^4 off-by-one, 10 = 2x5)."),
177: ("KEEP", "Key recomputed; explanation correct.", "Migrate to schema later."),
178: ("FIX", PH, "Draft (48 = product, 12 = common multiple of 6 only)."),
179: ("FIX", PH, "Draft."),
180: ("FIX", PH, "Draft."),
181: ("HOLD", PH + " Percent-change item; MILESTONE_2000_PLAN caps percent change at 40 and the bank already has 78.", "CoS: count it under Basic operations (one-step percent) or retire under the cap. Draft supplied."),
182: ("KEEP", "Key 9 recomputed; explanation correct.", "Migrate later."),
183: ("FIX", PH + " Stem wording is awkward ('equals which fraction for the first part over total').", "Draft with a clear stem."),
184: ("FIX", PH, "Draft."),
262: bdup(487, " (7/8 of 64, same numbers)"),
263: ("FIX", PH, "Draft."),
264: ("FIX", PH, "Draft."),
265: ("HOLD", PH + " Reverse-percent item; percent-change cap applies.", "CoS decision as #181. Draft supplied."),
339: ("KEEP", "Key 22 recomputed.", ""), 340: ("KEEP", "Key 36 recomputed.", ""), 341: ("KEEP", "Key 150 recomputed.", ""), 342: ("KEEP", "Key 4.35 recomputed.", ""),
343: ("REJECT", "Key 720 correct, but option B is malformed (' von 760', user-visible), and qa_file finds the same fact already approved as CIVIO-NUM-WP-PCT-CHANGE-000528 (₱800 at 10% off; that item itself reads 'A electric fan', a grammar slip to flag, not edited).", "Retire the baseline row (removes the malformed option from users); bank 000528 covers the fact."),
485: ("KEEP", "Key 30 recomputed. Cosmetic: boilerplate missing period ('... is 30 Therefore').", "Add the period on migration."),
486: ("KEEP", "Key 45 recomputed. Same frame as #173 with different numbers (acceptable).", ""),
487: ("KEEP", "Key 56 recomputed; kept over #262.", ""),
488: ("KEEP", "Key 3.65 recomputed.", ""),
489: ("HOLD", "Key 1,320 recomputed; percent-decrease item under the percent-change cap.", "CoS decision as #181."),
540: ("KEEP", "Key 41 recomputed.", ""),
# Number sequence (28)
45: ("FIX", PH + " Very easy (+3).", "Draft."),
46: bdup(190, " (doubling; #46 and #186 are the same sequence 5,10,20,40)"),
47: bdup(345, " (#47's sequence 2,5,10,17 is a prefix of #345)"),
185: bdup(193, " (squares, same answer 36)"),
186: bdup(190, " (doubling; exact duplicate of #46)"),
187: ("FIX", PH, "Draft (Fibonacci)."),
188: bdup(346, " (81, 27, 9, 3 — same sequence)"),
189: ("KEEP", "Key 42 recomputed (n(n+1)); kept over #491.", ""),
190: ("FIX", PH, "Draft; representative doubling item."),
191: ("KEEP", "Key 63 recomputed (x2+1).", ""),
192: ("KEEP", "Key 50 recomputed; kept over #541.", ""),
193: ("FIX", PH, "Draft; representative squares item."),
194: ("KEEP", "Key 17 recomputed; kept over #266.", ""),
195: bdup(492, " (halving)"),
196: ("FIX", PH, "Draft (consecutive primes)."),
266: bdup(194, " (same rule: differences +1, +2, +3, ...)"),
267: ("FIX", PH, "Draft (factorials)."),
268: bdup(193, " (consecutive squares again)"),
344: bdup(190, " (doubling)"),
345: ("KEEP", "Key 37 recomputed.", ""),
346: ("KEEP", "Key 1 recomputed; kept over #188.", ""),
347: ("KEEP", "Key 66 recomputed (x2-2).", ""),
348: bdup(193, " (consecutive squares)"),
490: bdup(191, " (x2+1 vs x2-1, same rule family; keep one)"),
491: bdup(189, " (2, 6, 12, 20, same sequence)"),
492: ("KEEP", "Key 6 recomputed.", ""),
493: ("KEEP", "Key 48 recomputed (missing middle term, a distinct format).", ""),
541: bdup(192, " (growing subtraction, same rule)"),
}
SUB = {"Code of Conduct and Ethical Standards (R.A. 6713)": "GI-6713", "Environment Management and Protection": "GI-ENV", "Basic operations": "NUM-OPS", "Number sequence": "NUM-SEQ"}
target = [x for x in Q.values() if x["sub"] in SUB]
assert {x["id"] for x in target} == set(V), set(x["id"] for x in target) ^ set(V)

# ---------- full-schema drafts ----------
def gi(bid, comp, arch, stem, opts, key, terms, why, wrong, codes, src, url, quote, fact, shortcut, diff="medium", sec=30):
    ids = ["o1", "o2", "o3", "o4"]
    return {"id": f"CIVIO-B3-GI-{arch[3:]}-{bid:04d}", "track": "both", "domain": "general_information", "competency": comp,
        "concept": "ethics law" if "6713" in comp else "environmental law", "micro_skill": f"recall and apply {src}",
        "archetype": arch, "difficulty": diff, "est_seconds": sec, "language": "en", "stem": stem,
        "options": [{"option_id": i, "text": t} for i, t in zip(ids, opts)], "answer_option_id": ids[key],
        "reveal": {"terms": terms, "shortcut": shortcut, "why_correct": why, "why_wrong": {ids[i]: w for i, w in wrong.items()}},
        "distractor_reasoning": {ids[i]: c for i, c in codes.items()}, "source": src, "source_url": url, "source_quote": quote,
        "source_group": "civio", "status": "draft", "review_status": "unreviewed",
        "provenance": {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T02:30:00+08:00", "spec_version": "0.1.9"},
        "_legacy": True, "fact_id": fact, "shortcut": shortcut,
        "replaces": {"baseline_id": bid, "stem": Q[bid]["stem"], "key": Q[bid]["options"][Q[bid]["correct_option"]]},
        "notes": "Round 03 B3 draft (Grok Bot, independent audit). Pending CoS."}
R6 = "Code of Conduct and Ethical Standards (R.A. 6713)"; EN = "Environment Management and Protection"
D = [
gi(67, R6, "GI-DEADLINE-NUMBER", "Under R.A. 6713, when must a covered public employee file the Statement of Assets, Liabilities and Net Worth (SALN)?",
   ["Within 30 days after assuming office, on or before April 30 every year, and within 30 days after leaving the service",
    "Within 60 days after assuming office, on or before April 15 every year, and within 60 days after leaving the service",
    "Within 30 days after assuming office, on or before December 31 every year, and within one year after leaving the service",
    "Within 15 working days after assuming office, on or before June 30 every year, and only if asked after leaving the service"], 0,
   "SALN: sworn statement of assets, liabilities, net worth and business interests (Sec. 8).",
   "Sec. 8(A) sets three filing points: (a) within 30 days after assumption of office, (b) on or before April 30 of every year thereafter, and (c) within 30 days after separation from the service.",
   {1: "60 days is the Sec. 9 divestment period, and April 15 is the income-tax deadline, not the SALN date.", 2: "December 31 is the as-of date of the figures, not the filing deadline; separation filing is 30 days, not one year.", 3: "15 working days is the Sec. 5(a) reply period for letters; separation filing is mandatory, not on request."},
   {1: "GI-NEIGHBOR-NUMBER", 2: "GI-NEIGHBOR-NUMBER", 3: "GI-SIBLING-TERM"}, "R.A. 6713, Sec. 8(A)", L6713,
   "(a) within thirty (30) days after assumption of office; (b) on or before April 30, of every year thereafter; and (c) within thirty (30) days after separation from the service",
   "FACT-RA6713-8A-SALN-TRIAD", "30 in, April 30 yearly, 30 out."),
gi(72, R6, "GI-SCENARIO-APPLY", "A procurement officer owns 20% of the shares of a supplier that has just bid on a contract her office will award. Under R.A. 6713, what is this situation called?",
   ["A conflict of interest", "Undue favor to a relative", "Divestment of a business interest", "Outside employment during incumbency"], 0,
   "Conflict of interest: an official who is a board member, officer or substantial stockholder of a business whose interest may be opposed to or affected by faithful performance of duty (Sec. 3(i)).",
   "A substantial stockholding in a business that her official decision can affect is exactly the Sec. 3(i) definition; Sec. 9 then requires resignation or divestment.",
   {1: "Sec. 4(A)(c) concerns favors to relatives; here the interest is the officer's own.", 2: "Divestment (Sec. 3(j)) is the cure for the conflict, not its name.", 3: "Sec. 7(b) outside employment concerns working for a regulated firm; owning shares is not employment."},
   {1: "GI-SIBLING-TERM", 2: "GI-SIBLING-TERM", 3: "GI-SIBLING-TERM"}, "R.A. 6713, Sec. 3(i) and Sec. 9", L6713,
   "\"Conflict of interest\" arises when a public official or employee is a member of a board, an officer, or a substantial stockholder of a private corporation or owner or has a substantial interest in a business, and the interest of such corporation or business, or his rights or duties therein, may be opposed to or affected by the faithful performance of official duty",
   "FACT-RA6713-3I-CONFLICT-DEFINITION", "Own stake + your decision affects it = conflict of interest."),
gi(388, R6, "GI-TERM-MATCH", "Under R.A. 6713, a conflict of interest arises when an official is a board member, officer or substantial stockholder of a business whose interest may be what?",
   ["Opposed to or affected by the faithful performance of official duty", "Regulated by any other government agency", "Owned partly by the official's relatives within the fourth degree", "Larger than the official's annual salary"], 0,
   "Conflict of interest (Sec. 3(i)).",
   "Sec. 3(i) ties the conflict to a business interest that 'may be opposed to or affected by the faithful performance of official duty'.",
   {1: "Regulation by another agency does not involve the official's own duty.", 2: "Relatives matter under Sec. 4(A)(c) and Sec. 8(B), not the Sec. 3(i) definition.", 3: "The Act sets no salary-size test; the test is the effect on official duty."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SIBLING-TERM", 3: "GI-SOUNDS-RIGHT"}, "R.A. 6713, Sec. 3(i)", L6713,
   "may be opposed to or affected by the faithful performance of official duty", "FACT-RA6713-3I-CONFLICT-DEFINITION", "Ask: can my official duty affect this business?"),
gi(389, R6, "GI-TERM-MATCH", "An official with a conflicting shareholding transfers all the shares to his wife. Under R.A. 6713, why is this NOT a valid divestment?",
   ["Divestment must be in favor of someone other than the spouse and relatives", "Divestment must be made only to the government", "Shares can never be divested, only declared in the SALN", "Divestment requires resigning from government first"], 0,
   "Divestment (Sec. 3(j)): transfer of title by voluntarily, completely and actually giving up the right to it, to a person other than one's spouse and relatives.",
   "Sec. 3(j) excludes transfers to the spouse and relatives, so moving shares to a wife leaves the conflict in the family.",
   {1: "The Act does not require transfer to the government; any person other than spouse and relatives qualifies.", 2: "Sec. 9 expressly requires divesting shareholdings within 60 days; declaring alone is not enough.", 3: "Sec. 9 requires resigning from the private enterprise, not from government."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SIBLING-TERM", 3: "GI-SIBLING-TERM"}, "R.A. 6713, Sec. 3(j) and Sec. 9", L6713,
   "in favor of a person or persons other than his spouse and relatives as defined in this Act", "FACT-RA6713-3J-DIVESTMENT-DEFINITION", "Divest = give it away outside the family."),
gi(393, R6, "GI-WHO-HOLDS-POWER", "Which body has the primary responsibility for administering and enforcing R.A. 6713?",
   ["Civil Service Commission", "Office of the Ombudsman", "Commission on Audit", "Sandiganbayan"], 0,
   "Administration and enforcement: issuing rules and acting on violations of the Act.",
   "Sec. 12 gives the Civil Service Commission primary responsibility for administration and enforcement and the power to promulgate rules.",
   {1: "The Ombudsman co-chairs the awards committee (Sec. 6) and receives prosecutions, but Sec. 12 names the CSC.", 2: "COA audits government accounts; it is not named in Sec. 12.", 3: "The Sandiganbayan is an anti-graft court that tries cases; it does not administer the Act."},
   {1: "GI-WRONG-BODY", 2: "GI-WRONG-BODY", 3: "GI-WRONG-BODY"}, "R.A. 6713, Sec. 12", L6713,
   "The Civil Service Commission shall have the primary responsibility for the administration and enforcement of this Act.", "FACT-RA6713-12-CSC-ENFORCES", "Civil service ethics law → Civil Service Commission."),
gi(395, R6, "GI-SCENARIO-APPLY", "A mayor appoints his nephew to a position. Under R.A. 6713, Sec. 4(A)(c), in which case is this NOT an undue favor to a relative?",
   ["The position is strictly confidential or on the mayor's personal staff, coterminous with him", "The nephew passed the civil service examination and meets every qualification of the position", "The nephew agrees to serve without any pay for the first six months of the appointment", "The appointment is announced publicly on the city's website and posted at city hall"], 0,
   "Undue favor on account of office (Sec. 4(A)(c), justness and sincerity).",
   "Sec. 4(A)(c) bars undue favors to relatives except appointments to strictly confidential positions or to personal staff whose terms are coterminous with the official.",
   {1: "Eligibility is a separate requirement; it does not create the statutory exception.", 2: "Serving without pay is not an exception in the Act.", 3: "Publicity does not cure an undue favor."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 6713, Sec. 4(A)(c)", L6713,
   "except with respect to appointments of such relatives to positions considered strictly confidential or as members of their personal staff whose terms are coterminous with theirs",
   "FACT-RA6713-4C-RELATIVES-EXCEPTION", "Exception = confidential or coterminous personal staff."),
gi(396, R6, "GI-TERM-MATCH", "Under R.A. 6713, Sec. 8, a public official's declaration covers his own assets and interests and also those of whom?",
   ["His spouse and unmarried children under 18 living in his household", "All relatives within the fourth civil degree", "His spouse only, since children file their own statements", "All of his children, regardless of their age or where they live"], 0,
   "Declaration under oath of assets, liabilities, net worth and financial and business interests (Sec. 8).",
   "Sec. 8 extends the declaration to the spouse and unmarried children under eighteen living in the household.",
   {1: "The fourth civil degree defines 'relatives' for the separate Sec. 8(B) disclosure of relatives in government.", 2: "Sec. 8 also covers unmarried minor children in the household.", 3: "Only unmarried children under 18 living in the household are covered."},
   {1: "GI-SIBLING-TERM", 2: "GI-SIBLING-TERM", 3: "GI-NEIGHBOR-NUMBER"}, "R.A. 6713, Sec. 8", L6713,
   "including those of their spouses and of unmarried children under eighteen (18) years of age living in their households", "FACT-RA6713-8-SALN-FAMILY-SCOPE", "Spouse + unmarried minors at home."),
gi(397, R6, "GI-TERM-MATCH", "Under R.A. 6713, Sec. 7(d), which gift from a foreign government may a public official accept with the consent given by Congress?",
   ["A gift of nominal value received as a souvenir or mark of courtesy", "A gift of any value if reported in the next SALN", "Cash below one month's salary for official travel", "A gift accepted on behalf of a relative"], 0,
   "Congressional consent to certain foreign-government gifts (Sec. 7(d)).",
   "Sec. 7(d) lists consented foreign-government gifts: nominal-value souvenirs or marks of courtesy, scholarship/fellowship or medical treatment, and certain travel grants.",
   {1: "Reporting does not make a valuable gift acceptable; only the listed categories are consented.", 2: "The Act consents to certain travel grants and expenses, not to cash gifts.", 3: "Accepting through a relative is still indirect acceptance, barred by Sec. 7(d)."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SIBLING-TERM", 3: "GI-SOUNDS-RIGHT"}, "R.A. 6713, Sec. 7(d)", L6713,
   "The acceptance and retention by a public official or employee of a gift of nominal value tendered and received as a souvenir or mark of courtesy", "FACT-RA6713-7D-FOREIGN-GIFT", "Foreign gift: nominal souvenir, scholarship, medical, travel grant."),
gi(526, R6, "GI-SCENARIO-APPLY", "The reviewing body finds an official's statement incomplete. Under R.A. 6713, Sec. 10(a), what must it do?",
   ["Inform the official and direct him to take corrective action", "File a criminal case against the official at once", "Publish the statement online with the errors marked", "Return the statement and treat it as if it was never filed"], 0,
   "Review and compliance procedure (Sec. 10).",
   "Sec. 10(a) says that when a statement is not timely, complete or in proper form, the reviewing body shall inform the reporting individual and direct corrective action.",
   {1: "Prosecution is not the first step for an incomplete statement under Sec. 10(a).", 2: "Sec. 10(a) does not provide for publishing marked errors.", 3: "The law directs correction, not treating the filing as void."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 6713, Sec. 10(a)", L6713,
   "the appropriate Committee shall so inform the reporting individual and direct him to take the necessary corrective action", "FACT-RA6713-10A-CORRECTIVE-ACTION", "Incomplete SALN → told to correct it."),
# Environment
gi(11, EN, "GI-ENV-PRINCIPLE", "Sustainable development is development that meets present needs without doing what?",
   ["Compromising the ability of future generations to meet their own needs", "Using any natural resources to support present economic growth", "Allowing private companies to operate inside protected areas", "Allowing a country's population to increase over the next decades"], 0,
   "Sustainable development (Brundtland Commission, 1987); R.A. 9003, Sec. 2(c) requires ecologically sustainable development principles.",
   "The standard definition: meeting the needs of the present without compromising the ability of future generations to meet their own needs.",
   {1: "Sustainable development allows resource use; it limits use that harms future generations.", 2: "Private activity is regulated by protected-area law, not excluded by the definition.", 3: "Population growth is not part of the definition."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SIBLING-TERM", 3: "GI-SOUNDS-RIGHT"}, "Our Common Future (WCED, 1987); R.A. 9003, Sec. 2(c)", L9003,
   "in accordance with ecologically sustainable development principles", "FACT-ENV-SUSTAINABLE-DEVELOPMENT", "Now, without stealing from the future.", "easy", 20),
gi(83, EN, "GI-ENV-PRINCIPLE", "What is the main purpose of the Philippine Environmental Impact Statement (EIS) System under P.D. 1586?",
   ["To assess a covered project's likely environmental effects before it proceeds", "To audit a project's pollution only after it starts operating", "To replace the local business and building permits", "To grant tax incentives to environment-friendly firms"], 0,
   "EIS System: covered projects need an Environmental Compliance Certificate (ECC) after impact assessment.",
   "P.D. 1586 requires environmentally critical projects or projects in critical areas to undergo assessment and secure an ECC before operation.",
   {1: "Assessment is done before, not only after, the project starts.", 2: "An ECC does not replace LGU permits.", 3: "Tax incentives are not the EIS System's function."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SIBLING-TERM", 3: "GI-SOUNDS-RIGHT"}, "P.D. 1586 (Philippine Environmental Impact Statement System), Secs. 2 and 4", "https://lawphil.net/statutes/presdecs/pd1978/pd_1586_1978.html",
   "TO BE QUOTED after LawPhil check (P.D. 1586 Sec. 4)", "FACT-PD1586-EIS-PURPOSE", "EIS = look before you build."),
gi(228, EN, "GI-ENV-PRINCIPLE", "Why does R.A. 9275 use watersheds and river basins as units for water quality management areas?",
   ["Water and pollutants move through a drainage area toward a common outlet", "Watersheds are the only places where factories may operate", "Watersheds collect only rainwater that cannot be polluted", "Watersheds follow barangay boundaries exactly"], 0,
   "Watershed: land area that drains to a common outlet.",
   "R.A. 9275 Sec. 5 designates management areas using physiographic units such as watersheds and river basins, because water and its pollutants move through a shared drainage area.",
   {1: "Watersheds are not factory zones.", 2: "Runoff picks up pollutants; that is why they are managed.", 3: "Watersheds follow terrain, not political boundaries; that is why LGUs must cooperate."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 9275 (Philippine Clean Water Act of 2004), Sec. 5", L9275,
   "using appropriate physiographic units such as watershed, river basins or water resources regions", "FACT-RA9275-5-WATERSHED-UNIT", "Water flows downhill together; manage it together."),
gi(229, EN, "GI-ENV-PRINCIPLE", "What does R.A. 9003 say about open dumps for solid waste?",
   ["They are prohibited and existing ones must be closed or converted", "They are allowed if the barangay approves them", "They are required in every municipality as a stopgap", "They are allowed for biodegradable waste only"], 0,
   "Open dump: disposal area where waste is indiscriminately thrown without planning or health standards (Sec. 3(t)).",
   "Sec. 37 prohibits establishing or operating open dumps and set a conversion/closure schedule; Sec. 48(9) penalizes it.",
   {1: "No barangay approval makes an open dump lawful under Sec. 37.", 2: "The Act requires closure, not open dumps.", 3: "Sec. 48(6) also prohibits dumping biodegradable materials in flood-prone areas; no exception for biodegradables."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-OLD-RULE", 3: "GI-SOUNDS-RIGHT"}, "R.A. 9003, Secs. 3(t), 37, 48(9)", L9003,
   "No open dumps shall be established and operated, nor any practice or disposal of solid waste by any person, including LGUs, which constitutes the use of open dumps for solid wastes, be allowed", "FACT-RA9003-37-OPEN-DUMP-BAN", "Open dumps: banned."),
gi(405, EN, "GI-TERM-MATCH", "R.A. 9003 is known as what law?",
   ["Ecological Solid Waste Management Act of 2000", "Philippine Clean Air Act of 1999", "Philippine Clean Water Act of 2004", "Toxic Substances and Hazardous and Nuclear Wastes Control Act of 1990"], 0,
   "R.A. 9003 (amended by R.A. 11898, the EPR Act of 2022; short title unchanged).", "Sec. 1 gives the short title 'Ecological Solid Waste Management Act of 2000'.",
   {1: "That is R.A. 8749.", 2: "That is R.A. 9275.", 3: "That is R.A. 6969."}, {1: "GI-SIBLING-TERM", 2: "GI-SIBLING-TERM", 3: "GI-SIBLING-TERM"},
   "R.A. 9003, Sec. 1", L9003, "This Act shall be known as the \"Ecological Solid Waste Management Act of 2000.\"", "FACT-RA9003-1-TITLE", "9003 → waste (2000).", "easy", 15),
gi(408, EN, "GI-TERM-MATCH", "Which short title belongs to Republic Act No. 8749, the country's main air-quality law?",
   ["Philippine Clean Air Act of 1999", "Ecological Solid Waste Management Act of 2000", "Philippine Clean Water Act of 2004", "Climate Change Act of 2009"], 0,
   "R.A. 8749.", "Sec. 1 gives the short title 'Philippine Clean Air Act of 1999'.",
   {1: "That is R.A. 9003.", 2: "That is R.A. 9275.", 3: "That is R.A. 9729."}, {1: "GI-SIBLING-TERM", 2: "GI-SIBLING-TERM", 3: "GI-SIBLING-TERM"},
   "R.A. 8749, Sec. 1", L8749, "This Act shall be known as the \" Philippine Clean Air Act of 1999. \"", "FACT-RA8749-1-TITLE", "8749 → air (1999).", "easy", 15),
gi(410, EN, "GI-ENV-PRINCIPLE", "R.A. 9729 adopts the Precautionary Principle to guide climate risk decisions. What does that principle allow?",
   ["Preventive action against a serious threat even without full scientific certainty", "Taking action only after the harm is proven beyond reasonable doubt", "Making the polluter pay for the cleanup after the damage has already occurred", "Shifting all of the costs of climate action to developed countries alone"], 0,
   "Precautionary Principle.", "R.A. 9729 Sec. 2 names the Precautionary Principle; lack of full scientific certainty is not a reason to postpone preventive measures (see also Rule 20, A.M. No. 09-6-8-SC).",
   {1: "That is the opposite of precaution.", 2: "That is the polluter-pays principle.", 3: "That distorts common but differentiated responsibilities, a separate Sec. 2 principle."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SIBLING-TERM", 3: "GI-SIBLING-TERM"}, "R.A. 9729 (Climate Change Act of 2009), Sec. 2", L9729,
   "common but differentiated responsibilities and the Precautionary Principle to guide decision-making in climate risk management", "FACT-RA9729-2-PRECAUTION", "Don't wait for proof to prevent serious harm."),
gi(412, EN, "GI-SCENARIO-APPLY", "A barangay wants to stop plastic waste from clogging its canals and esteros. Which measure follows R.A. 9003 most directly?",
   ["Require segregation at source and stop dumping in canals", "Burn collected plastics in an open lot every week", "Mix plastics with other waste so collection is faster", "Bury plastic waste along the creek banks"], 0,
   "Segregation at source (Sec. 21); prohibited acts (Sec. 48).",
   "Sec. 21 requires segregation at the source, and Sec. 48(1) prohibits dumping waste in canals and esteros.",
   {1: "Open burning is prohibited by Sec. 48(3).", 2: "Collecting unsorted waste is prohibited by Sec. 48(4).", 3: "Burying waste in flood-prone areas is prohibited by Sec. 48(6)."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 9003, Secs. 21 and 48", L9003,
   "Littering, throwing, dumping of waste matters in public places, such as roads, sidewalks, canals, esteros or parks", "FACT-RA9003-48-CANAL-DUMPING", "Segregate, don't dump."),
gi(413, EN, "GI-ENV-PRINCIPLE", "Under the NIPAS Act as amended by R.A. 11038 (E-NIPAS Act of 2018), what is the main purpose of protected areas?",
   ["To conserve biological diversity and maintain ecological processes", "To set aside land for future housing projects", "To reserve forests for large-scale commercial logging", "To create tourism zones that are exempt from regulation"], 0,
   "NIPAS: National Integrated Protected Areas System.",
   "R.A. 11038 Sec. 2 (amending R.A. 7586 Sec. 2) establishes NIPAS for biologically important areas, to be managed consistently with biological diversity and sustainable development.",
   {1: "Protected areas are not housing reserves.", 2: "Commercial exploitation is restricted, not the purpose.", 3: "Tourism in protected areas is regulated, not exempt."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 7586, Sec. 2, as amended by R.A. 11038, Sec. 2", L11038,
   "consistent with the principles of biological diversity and sustainable development", "FACT-RA11038-2-NIPAS-PURPOSE", "Protected area = protect biodiversity."),
gi(414, EN, "GI-WHO-HOLDS-POWER", "Which department is primarily responsible for the conservation, management and development of the country's environment and natural resources?",
   ["Department of Environment and Natural Resources", "Department of Agriculture", "Department of the Interior and Local Government", "Department of Energy"], 0,
   "DENR (E.O. 192, 1987).", "E.O. 192 (1987) makes the DENR the primary government agency for the environment and natural resources; the EMB is one of its bureaus.",
   {1: "The DA handles agriculture and, through BFAR, fisheries.", 2: "The DILG supervises LGUs, which implement local waste rules.", 3: "The DOE handles energy resources."},
   {1: "GI-WRONG-BODY", 2: "GI-WRONG-BODY", 3: "GI-WRONG-BODY"}, "E.O. 192 (1987), Sec. 4", "https://lawphil.net/executive/execord/eo1987/eo_192_1987.html",
   "TO BE QUOTED after LawPhil check (E.O. 192 Sec. 4)", "FACT-EO192-DENR-PRIMARY", "Environment + natural resources = DENR.", "easy", 15),
gi(417, EN, "GI-TERM-MATCH", "R.A. 11898 added a definition of 'circular economy' to R.A. 9003. What does a circular economy aim to do?",
   ["Keep products and materials in use longer through design, servicing and recovery", "Collect all of a city's waste in one large circular landfill", "Recycle materials only after they reach final disposal sites", "Ban the production and sale of all plastic products nationwide"], 0,
   "Circular economy (R.A. 9003 Sec. 3(d-1), as amended by R.A. 11898).",
   "The amended Sec. 3(d-1) describes creating value by extending product lifespan through improved design and servicing, so resources stay in continual use.",
   {1: "Landfilling is the end of a linear model, not a circular one.", 2: "Recovery happens before disposal, not after.", 3: "The EPR Act regulates plastic packaging; it does not ban all plastic."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 9003, Sec. 3(d-1), as amended by R.A. 11898 (EPR Act of 2022)", L11898,
   "Circular economy shall refer to an economic model of creating value by extending product lifespan through improved design and servicing", "FACT-RA11898-CIRCULAR-ECONOMY", "Circular = keep it in use."),
gi(527, EN, "GI-ENV-PRINCIPLE", "Under R.A. 9003, Sec. 2(c), which order of waste-management actions does the law favor?",
   ["Reduce and reuse first, recycle and recover next, dispose last", "Dispose first, then recover what remains at the landfill", "Recycle first, then reduce what cannot be recycled", "Burn first to reduce volume, then recycle the ash"], 0,
   "Waste hierarchy: avoidance and volume reduction before collection, treatment and disposal.",
   "Sec. 2(c) sets targets for avoidance and volume reduction through source reduction, composting, recycling, re-use and recovery before collection, treatment and disposal.",
   {1: "Disposal is the last step, not the first.", 2: "Reduction comes before recycling.", 3: "Burning is prohibited (Sec. 48(3); R.A. 8749 Sec. 20 bans incineration)."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "R.A. 9003, Sec. 2(c)", L9003,
   "solid waste avoidance and volume reduction through source reduction and waste minimization measures, including composting, recycling, re-use, recovery, green charcoal process, and others, before collection, treatment and disposal",
   "FACT-RA9003-2C-WASTE-HIERARCHY", "Reduce, reuse, recover, then dispose."),
gi(528, EN, "GI-ENV-PRINCIPLE", "How do mangrove forests mainly help coastal communities?",
   ["They provide fish nursery habitat and reduce wave and erosion damage", "They supply most of the freshwater used by coastal towns", "They store carbon but have little effect on fisheries", "They prevent typhoons from forming near the coast"], 0,
   "Mangroves: salt-tolerant coastal forests.", "Mangrove roots shelter young fish and shellfish and absorb wave energy, reducing erosion and storm-surge damage.",
   {1: "Mangroves grow in brackish water; they are not a main freshwater source.", 2: "They store carbon AND support fisheries.", 3: "No forest prevents typhoons from forming; mangroves only reduce damage."},
   {1: "GI-SOUNDS-RIGHT", 2: "GI-SOUNDS-RIGHT", 3: "GI-SOUNDS-RIGHT"}, "General ecology (no statute)", None, "", "FACT-ENV-MANGROVE-FUNCTION", "Mangroves: nursery + natural seawall.", "easy", 20),
]
# Numerical drafts
def num(bid, arch, comp, stem, opts, key, why, wrong, codes, short, diff="easy", sec=30, legacy=True):
    ids = ["n1", "n2", "n3", "n4"]
    it = {"id": f"CIVIO-B3-{arch}-{bid:04d}", "track": "both", "domain": "numerical", "competency": comp, "concept": comp.lower(),
        "micro_skill": arch.lower(), "archetype": arch, "difficulty": diff, "est_seconds": sec, "language": "en", "stem": stem,
        "options": [{"option_id": i, "text": t} for i, t in zip(ids, opts)], "answer_option_id": ids[key],
        "reveal": {"terms": "", "shortcut": short, "why_correct": why, "why_wrong": {ids[i]: w for i, w in wrong.items()}},
        "distractor_reasoning": {ids[i]: c for i, c in codes.items()}, "source": "Civio baseline, rewritten (Grok Bot B3)", "source_url": None,
        "source_group": "civio", "status": "draft", "review_status": "unreviewed",
        "provenance": {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T02:30:00+08:00", "spec_version": "0.1.9"},
        "shortcut": short, "replaces": {"baseline_id": bid, "stem": Q[bid]["stem"], "key": Q[bid]["options"][Q[bid]["correct_option"]]},
        "notes": "Round 03 B3 draft (Grok Bot). Key independently recomputed (numcheck). Pending CoS."}
    it["reveal"]["terms"] = {"Basic operations": "Operations: add, subtract, multiply, divide, percent, fraction.", "Number sequence": "Sequence: find the rule between terms, then apply it once more."}[comp]
    if legacy: it["_legacy"] = True
    return it
BO, NS = "Basic operations", "Number sequence"
P, O, X, G = "NUM-PARTIAL", "NUM-OFF-BY-ONE", "NUM-OP-SWAP", "NUM-GIVEN-REUSED"
D += [
num(41, "NUM-PROPERTY", BO, "What is 15 + 27?", ["42", "32", "52", "41"], 0, "15 + 27 = 42 (5 + 7 = 12, carry 1; 1 + 2 + 1 = 4).", {1: "Forgot the carried 1.", 2: "Carried 1 twice.", 3: "Off by one."}, {1: P, 2: "NUM-EXTRA-STEP", 3: O}, "Add tens then ones: 10 + 20 = 30, 5 + 7 = 12, total 42."),
num(42, "NUM-PROPERTY", BO, "What is 96 ÷ 8?", ["12", "8", "16", "11"], 0, "8 × 12 = 96, so 96 ÷ 8 = 12.", {1: "Repeats the divisor.", 2: "96 ÷ 6, wrong divisor.", 3: "Off by one."}, {1: G, 2: "NUM-WRONG-BASE", 3: O}, "Halve three times: 96 → 48 → 24 → 12."),
num(43, "NUM-PROPERTY", BO, "What is 7 × 9?", ["63", "56", "72", "64"], 0, "7 × 9 = 63.", {1: "7 × 8.", 2: "8 × 9.", 3: "8 × 8, a nearby square."}, {1: O, 2: O, 3: "NUM-WRONG-BASE"}, "7 × 10 − 7 = 63."),
num(44, "NUM-PROPERTY", BO, "What is 100 − 37?", ["63", "73", "67", "53"], 0, "100 − 37 = 63.", {1: "Borrowing error in the tens.", 2: "Subtracted 33 instead of 37 (digits swapped in the ones step).", 3: "Borrowed twice."}, {1: P, 2: "NUM-DECIMAL", 3: "NUM-EXTRA-STEP"}, "Count up: 37 → 40 is 3, 40 → 100 is 60; 63."),
num(173, "NUM-PCT-BASIC", BO, "An office budget of 450 thousand pesos sets aside 18% for supplies. How many thousand pesos is that?", ["72", "81", "90", "99"], 1, "0.18 × 450 = 81 (10% = 45, 8% = 36; 45 + 36 = 81).", {0: "16% of 450.", 2: "20% of 450.", 3: "22% of 450."}, {0: "NUM-WRONG-BASE", 2: "NUM-WRONG-BASE", 3: "NUM-WRONG-BASE"}, "10% = 45; 20% = 90; subtract 2% (9): 81."),
num(175, "NUM-DECIMAL", BO, "What is 125 × 0.8?", ["90", "100", "110", "1,000"], 1, "125 × 0.8 = 125 × 8 ÷ 10 = 1,000 ÷ 10 = 100.", {0: "Subtracted 35 by estimate.", 2: "Subtracted only 15.", 3: "Forgot to move the decimal point."}, {0: "NUM-WRONG-BASE", 2: P, 3: "NUM-DECIMAL"}, "0.8 = 4/5; 125 ÷ 5 × 4 = 100."),
num(176, "NUM-PROPERTY", BO, "Evaluate 2⁵ (two multiplied by itself five times).", ["10", "16", "32", "25"], 2, "2 × 2 × 2 × 2 × 2 = 32.", {0: "Multiplied 2 × 5.", 1: "Only four factors of 2.", 3: "5 squared, base and exponent swapped."}, {0: X, 1: O, 3: X}, "Double five times: 2, 4, 8, 16, 32."),
num(178, "NUM-PROPERTY", BO, "What is the least common multiple (LCM) of 6 and 8?", ["12", "24", "48", "2"], 1, "Multiples of 8: 8, 16, 24; 24 is the first divisible by 6.", {0: "A multiple of 6 but not of 8.", 2: "The product 6 × 8, a common multiple but not the least.", 3: "The GCF, not the LCM."}, {0: P, 2: "NUM-EXTRA-STEP", 3: X}, "LCM = product ÷ GCF = 48 ÷ 2 = 24."),
num(179, "NUM-PROPERTY", BO, "What is the greatest common factor (GCF) of 36 and 54?", ["6", "9", "18", "108"], 2, "36 = 2 × 18, 54 = 3 × 18; 18 is the largest common factor.", {0: "A common factor, but not the greatest.", 1: "A common factor, but not the greatest.", 3: "The LCM."}, {0: P, 1: P, 3: X}, "GCF(36, 54) = GCF(36, 18) = 18."),
num(180, "NUM-FRAC-DEC", BO, "What is 0.125 as a fraction in lowest terms?", ["1/5", "1/8", "1/4", "125/100"], 1, "0.125 = 125/1000 = 1/8.", {0: "0.2.", 2: "0.25.", 3: "Wrong place value (that is 1.25)."}, {0: "NUM-WRONG-BASE", 2: "NUM-DECIMAL", 3: "NUM-DECIMAL"}, "Halve 1/4 (0.25) to get 1/8 (0.125)."),
num(181, "NUM-PCT-BASIC", BO, "A box of bond paper went from ₱200 last year to ₱260 now. By what percent did its price go up?", ["23%", "30%", "60%", "130%"], 1, "Increase 60 ÷ original 200 = 0.30 = 30%.", {0: "Divided by the new price 260.", 2: "Used the peso increase as the percent.", 3: "New price as a percent of old."}, {0: "NUM-WRONG-BASE", 2: G, 3: "NUM-EXTRA-STEP"}, "Change ÷ original: 60 ÷ 200 = 30%."),
num(183, "NUM-FRAC-DEC", BO, "Pens and pencils are in the ratio 3 : 5. What fraction of all the items are pens?", ["3/5", "3/8", "5/8", "5/3"], 1, "3 + 5 = 8 parts; pens are 3 of 8 = 3/8.", {0: "Pens over pencils, not over the total.", 2: "Pencils' share.", 3: "Pencils over pens."}, {0: "NUM-WRONG-BASE", 2: "NUM-OTHER-SHARE", 3: X}, "Part ÷ (sum of parts)."),
num(184, "NUM-PCT-BASIC", BO, "A clerk earns a 2.5% commission on ₱800 of sales. How much is the commission, in pesos?", ["2", "20", "25", "200"], 1, "1% of 800 = 8; 2.5 × 8 = 20.", {0: "Decimal moved one place too far.", 2: "Took 2.5% of 1,000.", 3: "Decimal moved one place the wrong way (25%)."}, {0: "NUM-DECIMAL", 2: "NUM-WRONG-BASE", 3: "NUM-DECIMAL"}, "1% = 8, so 2.5% = 20."),
num(263, "NUM-PROPERTY", BO, "Which whole number, multiplied by itself, gives 196?", ["13", "14", "16", "98"], 1, "14 × 14 = 196.", {0: "13 × 13 = 169.", 2: "16 × 16 = 256.", 3: "Halved instead of taking the root."}, {0: O, 2: "NUM-WRONG-BASE", 3: X}, "196 ends in 6, so the root ends in 4 or 6; 14² = 196."),
num(264, "NUM-UNIT", BO, "How many minutes are in 3.5 hours?", ["180", "200", "210", "350"], 2, "3.5 × 60 = 210.", {0: "Dropped the half hour.", 1: "Treated .5 h as 20 min.", 3: "Used 100 minutes per hour."}, {0: P, 1: "NUM-UNIT", 3: "NUM-UNIT"}, "3 h = 180, half hour = 30; 210."),
num(265, "NUM-PCT-BASIC", BO, "After a 20% raise, a daily allowance is ₱180. What was the allowance before the raise, in pesos?", ["144", "150", "160", "216"], 1, "1.2 × n = 180, so n = 150. Check: 150 + 30 = 180.", {0: "Took 20% off 180 (wrong base).", 2: "Subtracted 20 instead of 20%.", 3: "Added 20% to 180."}, {0: "NUM-WRONG-BASE", 2: X, 3: X}, "Divide by 1.2: 180 ÷ 1.2 = 150."),
# sequences
num(45, "NUM-SEQ-DIFF", NS, "What number comes next? 3, 6, 9, 12, ___", ["15", "14", "18", "24"], 0, "Add 3 each time: 12 + 3 = 15.", {1: "Added 2.", 2: "Added 6.", 3: "Doubled the last term."}, {1: O, 2: "NUM-SEQ-OTHER-RULE", 3: "NUM-SEQ-OTHER-RULE"}, "Constant difference 3.", legacy=False),
num(187, "NUM-SEQ-DIFF", NS, "Which term follows 1, 1, 2, 3, 5, 8?", ["11", "12", "13", "16"], 2, "Each term is the sum of the two before it: 5 + 8 = 13.", {0: "Added the last difference 3.", 1: "Added 4.", 3: "Doubled 8."}, {0: "NUM-SEQ-OTHER-RULE", 1: O, 3: "NUM-SEQ-OTHER-RULE"}, "Fibonacci: add the last two terms."),
num(190, "NUM-SEQ-MULT", NS, "Continue the series 7, 14, 28, 56 with the next term.", ["84", "98", "112", "70"], 2, "Multiply by 2: 56 × 2 = 112.", {0: "Added 28 (the previous term).", 1: "Added 42.", 3: "Added 14 (the first difference)."}, {0: "NUM-SEQ-OTHER-RULE", 1: "NUM-SEQ-OTHER-RULE", 3: "NUM-SEQ-OTHER-RULE"}, "Ratio 2.", legacy=False),
num(193, "NUM-SEQ-DIFF", NS, "What number comes next? 1, 4, 9, 16, 25, ___", ["30", "34", "36", "49"], 2, "Squares 1², 2², ..., 5²; next is 6² = 36.", {0: "Added 5 again.", 1: "Added 9, the previous odd difference.", 3: "Skipped to 7²."}, {0: "NUM-SEQ-OTHER-RULE", 1: O, 3: O}, "Differences 3, 5, 7, 9, then 11.", legacy=False),
num(196, "NUM-SEQ-DIFF", NS, "Which number should follow 11, 13, 17, 19, 23?", ["25", "27", "29", "31"], 2, "Consecutive primes; the prime after 23 is 29.", {0: "Added 2 (25 = 5 × 5 is not prime).", 1: "Added 4 (27 = 3 × 9).", 3: "Skipped the prime 29."}, {0: "NUM-SEQ-OTHER-RULE", 1: "NUM-SEQ-OTHER-RULE", 3: O}, "List primes: 23, 29."),
num(267, "NUM-SEQ-MULT", NS, "In the series 1, 2, 6, 24, each term is a product of the one before. What is the fifth term?", ["48", "96", "120", "144"], 2, "Multiply by 2, 3, 4, then 5: 24 × 5 = 120.", {0: "Multiplied by 2.", 1: "Multiplied by 4 again.", 3: "Multiplied by 6."}, {0: "NUM-SEQ-OTHER-RULE", 1: "NUM-SEQ-OTHER-RULE", 3: O}, "Factorials: 5! = 120."),
]

# ---------- post-process: state the key in why_correct; spread key positions (content unchanged) ----------
for n, it in enumerate(D):
    k = next(o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"])
    if not it["reveal"]["why_correct"].lower().startswith(k.lower()[:20]):
        it["reveal"]["why_correct"] = f"Answer: {k}. " + it["reveal"]["why_correct"]
    texts = [o["text"] for o in it["options"]]; ids = [o["option_id"] for o in it["options"]]
    ki = ids.index(it["answer_option_id"]); slot = n % 4
    order = [t for i, t in enumerate(texts) if i != ki]; order.insert(slot, texts[ki])
    old = {o["text"]: o["option_id"] for o in it["options"]}
    newid = {t: ids[i] for i, t in enumerate(order)}
    remap = {old[t]: newid[t] for t in texts}
    it["options"] = [{"option_id": ids[i], "text": t} for i, t in enumerate(order)]
    it["answer_option_id"] = remap[it["answer_option_id"]]
    it["reveal"]["why_wrong"] = {remap[o]: w for o, w in it["reveal"]["why_wrong"].items()}
    it["distractor_reasoning"] = {remap[o]: c for o, c in it["distractor_reasoning"].items()}

# ---------- outputs ----------
json.dump({"batch": "round-03-baseline-b3-drafts", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio",
           "notes": "Full-schema drafts replacing baseline rows (see each item's 'replaces'). Generated by scripts/batches/audit/baseline_b3.py. Not applied, not imported.",
           "items": D}, open(os.path.join(ROOT, "docs/research/audit/fixes/round-03-baseline-b3-drafts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
drafted = {d["replaces"]["baseline_id"] for d in D}
rows = []
for x in sorted(target, key=lambda x: (list(SUB).index(x["sub"]), x["id"])):
    v, issue, prop = V[x["id"]]
    rows.append([SUB[x["sub"]], x["id"], x["options"][x["correct_option"]], v, issue, prop, "yes" if x["id"] in drafted else "", "pending file", "pending file"])
with open(os.path.join(ROOT, "docs/research/audit/data/baseline-b3-verdicts-2026-10-18.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["group", "baseline_id", "key_now", "grok_verdict", "issue_evidence", "proposal", "draft", "chatgpt_verdict", "agree"]); w.writerows(rows)
from collections import Counter
cnt = {g: Counter(r[3] for r in rows if r[0] == g) for g in SUB.values()}
tot = Counter(r[3] for r in rows)
md = ["# Round 03 baseline audit, batch B3 (independent): GI R.A. 6713 + Environment, Numerical Basic operations + Number sequence — review request for Chief of Staff", "",
"Grok Bot, 2026-10-18. Source: `docs/research/audit/data/baseline-550-2026-10-17.json` (read-only MSI export of 17 Oct; MSI not queried). Repo base `f2766db`. **Nothing applied, imported or activated.**", "",
"ChatGPT's preliminary audit files (audit/fixes/milestone, 2026-10-18) were **not received**; this is an independent audit. ChatGPT columns in the CSV read `pending file`.", "",
"## Summary", "", "| Group | Items | KEEP | FIX | REJECT | HOLD |", "|---|---:|---:|---:|---:|---:|"]
for g, c in cnt.items(): md.append(f"| {g} | {sum(c.values())} | {c['KEEP']} | {c['FIX']} | {c['REJECT']} | {c['HOLD']} |")
md.append(f"| **Total** | **{sum(tot.values())}** | **{tot['KEEP']}** | **{tot['FIX']}** | **{tot['REJECT']}** | **{tot['HOLD']}** |")
md += ["", "- **0 key errors.** R.A. 6713 keys checked against LawPhil text (Secs. 3(i), 3(j), 4(A), 5, 7, 8, 9, 10, 12); environment keys against R.A. 9003 (incl. R.A. 11898 amendments), 8749, 9275, 9729, 7586/11038. All 59 Numerical keys recomputed by code (`numcheck`), each matching exactly one option.",
"- **Missed defects:** #343 option B reads ' von 760' (malformed, user-visible) and its fact duplicates approved bank 000528, so #343 is retired. Approved 000528 reads 'A electric fan' (grammar; flagged, not edited).",
"- **Duplicates dominate R.A. 6713:** 23 of 37 repeat facts already in the approved bank (000020, 000203, 000302, 000309, 000402, 000403, 000405, 000511, 000610, 000807, 000810, 000908; 060051-060072). Same precedent as B2: retire the baseline row to draft.",
"- **Wrong law for the subtopic:** #223 (property disposal → P.D. 1445/COA), #224 (nepotism → E.O. 292 Book V Sec. 59, HOLD), #73 (whistleblowing, not in R.A. 6713), #72 (relative-owned bidder is not R.A. 6713's Sec. 3(i) conflict of interest; rewritten).",
"- **Length giveaway:** in the GI subjects the key is the uniquely longest option in 52 of 64 items (median key/distractor length ratio about 1.7). The drafts balance option lengths and replace joke distractors with sibling-term traps.",
"- **Positions:** stored keys are A/B only in all 64 GI items (A 49, B 15). Mocks and offline drills shuffle choices at display (`mock-pool.ts` shuffleOptionsForQuestion; `lib/offline/grader.ts`). **Online drills do not shuffle choices** (see below), so stored position IS user-facing there.",
"- **Percent-change cap:** #181, #265, #489 are percent-change items while the bank already exceeds the proposed cap of 40 (78). HOLD for a CoS category/cap decision.",
"- **Number sequence:** 13 of 28 are duplicates or same-rule repeats (squares x4, doubling x4, ÷3 x2, halving x2, ...). Rejecting them widens the sequence gap (MILESTONE §5); new original sequence items should use other rules (alternating, two interleaved series, cubes).", "",
"## Online drill choice shuffling (code check)", "",
"- `app/Services/DrillService.php` orders questions with `inRandomOrder()` only and serves `options` as stored.",
"- `resources/js/pages/user/drills/**` never calls `shuffleOptionsForQuestion` or any option shuffle; `custom-builder-view.tsx` shuffles question IDs only. `originalOptionIndices` exists in `drills/types.ts` but is never set on the online path.",
"- Only `mock-session.ts`, `use-exam-hydration.ts` (mocks) and `lib/offline/grader.ts` (offline drills) shuffle choices.",
"- **Conclusion:** in online drills the stored answer position is shown, so the baseline A/B skew is a real giveaway. Fix is app code → Codex Astra brief (apply `shuffleOptionsForQuestion` on the drill path), not an editorial change.", "",
"## Needs CoS approval", "",
"- All REJECT (retire to draft) and FIX (replace with the full-schema draft in `docs/research/audit/fixes/round-03-baseline-b3-drafts.json`).",
"- HOLD decisions: #224 (recategorize to civil-service law or retire), #86 (needs P.D. 705 anchor), #181/#265/#489 (percent cap).",
"- Two drafts (#83 P.D. 1586, #414 E.O. 192) carry `source_quote: TO BE QUOTED`; I did not fetch those texts this session. Approve only after the quote is filled.", "",
"## Per item", "", "| Group | ID | Key now | Verdict | Issue / evidence | Proposal | Draft |", "|---|---|---|---|---|---|---|"]
for r in rows: md.append("| " + " | ".join(str(c).replace("|", "/") for c in r[:7]) + " |")
open(os.path.join(ROOT, "docs/research/audit/round-03-baseline-b3-review-request.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print(dict(tot), {g: dict(c) for g, c in cnt.items()}, "drafts", len(D))
