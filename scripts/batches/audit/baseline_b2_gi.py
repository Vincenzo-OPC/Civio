"""Round 03 baseline batch B2: 70 baseline GI items (Philippine Constitution 49, Peace and Human Rights 21).
Findings only; nothing changed. Writes docs/research/audit/round-03-baseline-b2-gi-review-request.md."""
import json, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "docs/research/audit/data/baseline-550-2026-10-17.json"
K, F, D, OK = "KEY ERROR", "FIX", "DUPLICATE", "OK"
PH = "Placeholder explanation ('Local practice item for Docker study.')."
JK = "Joke distractors make the key obvious"
BP = "Explanation boilerplate lacks a period ('... Therefore, the correct option is ...')."
def bank(ref): return (D, f"Same fact as approved bank item {ref}, which has full spec metadata.", "Retire the baseline copy.")
F_ = {
1: (F, PH, "Real explanation (Art. XVIII, Sec. 27 ratification; the Constitution is the fundamental law). Keep."),
2: bank("000804"),
3: bank("000808"),
4: (D, PH + " Same task as #355.", "Retire; keep #355."),
5: (F, PH, "Real explanation: Article III is the Bill of Rights; drop 'mainly'."),
9: (D, PH + " Same idea as #399 and #74 (universality, non-discrimination).", "Retire; keep #399."),
10: (F, PH, "Real explanation: Art. XIII, Sec. 17 creates the CHR as an independent office."),
56: (OK, "Art. II, Sec. 1.", ""),
57: (OK, "Judicial review.", ""),
58: bank("000007"),
59: bank("000108"),
60: (OK, "COMELEC under Art. IX-C.", ""),
61: (OK, "Art. IV, Sec. 2. Keep; #361 duplicates it.", ""),
62: (OK, "Keep; #402 duplicates it.", "Note: amparo comes from a Supreme Court rule (2007), not the Constitution; recategorize under Peace and Human Rights."),
63: (OK, "Art. X, Sec. 4: general supervision of the President.", ""),
64: (OK, "Party-list (Art. VI, Sec. 5; R.A. 7941).", ""),
65: (OK, "CHR is not one of the three commissions.", ""),
74: (D, "Same idea as #399 and #9.", "Retire."),
75: (OK, "Keep; #365 duplicates it.", ""),
76: (OK, "CHR investigates, does not convict.", ""),
77: (F, "Not tied to any law; " + JK + " ('Forced labor as character building').", "Anchor to R.A. 7610 or the Constitution (Art. XV, Sec. 3(2)) and use real distractors, or retire."),
78: (OK, "Clear and present danger.", "Replace 'A private citizen asks politely' with a real test (e.g. 'the speech is unpopular')."),
79: (F, JK + " ('Glorifying violence').", "Retire or rewrite with a real peace-process concept."),
80: (OK, "R.A. 8371 (IPRA).", ""),
81: (OK, "Right to life.", "Distractors are weak."),
219: (OK, "Art. VII, Sec. 19: except in cases of impeachment.", "Replace 'All criminal offenses without limit' with 'Final conviction of a public official'."),
220: (OK, "Art. VI, Sec. 23(2).", ""),
221: (OK, "Art. IV, Sec. 5.", ""),
222: bank("000903"),
226: (F, JK + "; 'derogable' is not explained.", "Anchor to Art. III, Sec. 12(2) and R.A. 9745 (Anti-Torture Act)."),
227: (F, "Not tied to any law; " + JK + ".", "Anchor to Art. II, Sec. 14 or R.A. 9710 (Magna Carta of Women), or retire."),
354: (F, BP + " " + JK + " ('Hereditary succession').", "Real distractors: separation of powers, local autonomy, civilian supremacy."),
355: (F, BP + " 'Local school boards' is a joke option.", "Keep; replace that option with 'Constitutional commissions'."),
356: (OK, "Senate tries impeachment.", BP),
357: (F, BP + " " + JK + " ('All private corporations', 'Every foreign military').", "Real distractors: the PNP, the Cabinet, the National Security Council."),
358: (F, BP + " Joke distractors.", "Real distractors: right to information, freedom of assembly, privacy of communication."),
359: (OK, "Art. III, Sec. 2.", BP),
360: bank("000304"),
361: (D, "Same as #61.", "Retire."),
362: (OK, "CSC (Art. IX-B).", BP),
363: (F, BP + " Joke distractors ('Routine filing errors').", "Real distractors: equal protection, just compensation, ex post facto."),
364: (OK, "Art. VIII, Sec. 1.", BP),
365: (D, "Same as #75.", "Retire."),
366: bank("000507"),
367: (F, "Grammar: 'related to the law purpose'. Joke distractors.", "Stem: 'related to the purpose of the law'."),
368: (OK, "Eminent domain.", "Replace 'Police patrol only' with 'Police power'; 'Taxation' as another real power."),
369: bank("000910"),
370: (OK, "Art. VI, Sec. 3: at least 35 on election day.", BP),
371: (OK, "Suffrage (Art. V).", BP),
372: (OK, "Ex post facto (Art. III, Sec. 22).", BP),
373: (F, BP + " " + JK + " ('Weather Bureau', 'National Library').", "Real distractors: COA, CSC, CHR."),
374: (F, BP + " Joke distractors ('Print national currency').", "Real distractors: federal autonomy, independence from presidential supervision."),
375: (OK, "COMELEC.", BP),
376: (OK, "Art. III, Sec. 7.", BP),
377: (OK, "Art. III, Sec. 14(2).", BP),
378: (OK, "Art. VI, Sec. 29(1).", BP),
399: (F, BP + " Joke distractors.", "Keep as the one universality item."),
400: (F, "Common-sense item, no source; " + JK + ".", "Retire or anchor to a named peace framework."),
401: (OK, "Habeas data (Supreme Court rule, 2008).", "Recategorize as a rule-of-court remedy; joke distractors."),
402: (D, "Same as #62.", "Retire."),
403: (F, "Common-sense item, no source; joke distractors.", "Retire or anchor to the human-rights-based approach as CHR defines it."),
404: (F, "Common-sense item, no source; joke distractors.", "Retire."),
415: (F, "Common-sense item, no source; joke distractors.", "Retire."),
416: (OK, "Non-refoulement.", "Distractors are jokes; replace."),
519: (OK, "Bill of attainder (Art. III, Sec. 22).", BP),
520: (OK, "Expression and equal protection.", "Two rights in one key is fine; distractors are jokes."),
521: (F, BP + " " + JK + " ('A barangay sports club').", "Real distractors: the President, the DBM, COA."),
522: (F, BP + " Joke distractors ('Publishes a weather bulletin').", "Real distractors: imposes a tax, regulates a business (police power)."),
523: (OK, "Art. III, Sec. 5.", BP),
549: (F, "Common-sense item, no source; joke distractors.", "Retire."),
}
b = [x for x in json.load(open(SRC)) if x["sub"] in ("Philippine Constitution", "Peace and Human Rights Issues and Concepts")]
assert {x["id"] for x in b} == set(F_), sorted({x["id"] for x in b} ^ set(F_))
from collections import Counter
c = Counter(v[0] for v in F_.values())
L = ["# Round 03 baseline audit, batch B2: General Information, Constitution and Peace/Human Rights (70 items), review request for Chief of Staff", "",
     "Grok Bot, 2026-10-17. Source: `source_group='baseline'` GI rows in the MSI local Civio DB (Philippine Constitution 49, Peace and Human Rights 21), exported read-only to `docs/research/audit/data/baseline-550-2026-10-17.json`. Keys checked against the 1987 Constitution text on LawPhil. **No content was changed.** The remaining 64 baseline GI items (R.A. 6713 37, Environment 27) are batch B3, not started.", "",
     "## Summary", "",
     f"- **{c[K]} key errors.** Every key matches the Constitution or the cited law.",
     f"- **{c[D]} duplicates**: 8 repeat facts already in the approved bank (000007, 000108, 000304, 000507, 000804, 000808, 000903, 000910); 6 repeat other baseline items (habeas corpus, amparo, natural-born, universality, law-making).",
     f"- **{c[F]} fixes**: 5 placeholder explanations; joke distractors that make the key obvious on about 25 items; 7 Peace items with no legal source (common-sense mediation and peace-education questions, which CSC coverage frames as issues and concepts, not etiquette); one grammar error (#367); boilerplate explanations missing a period on #354-#549.",
     f"- **{c[OK]} OK** (several with optional distractor polish noted).", "",
     "**Gap noted:** Peace and Human Rights has no items on R.A. 9851 (IHL), R.A. 9745 (Anti-Torture), R.A. 10353 (Anti-Enforced Disappearance), R.A. 9710 (Magna Carta of Women) or R.A. 7610, all Philippine laws within CSC's stated scope. Proposed for a future gap-fill.", "",
     "## Per item", "", "| ID | Sub | Key now | Finding | Verdict | Proposal |", "|---|---|---|---|---|---|"]
for x in sorted(b, key=lambda x: x["id"]):
    v, why, prop = F_[x["id"]]
    key = x["options"][x["correct_option"]]
    sub = "Constitution" if x["sub"].startswith("Phil") else "Peace/HR"
    L.append(f"| {x['id']} | {sub} | {key.replace('|','/')} | {why.replace('|','/')} | {v} | {prop.replace('|','/')} |")
L += ["", "## Asks for CoS", "", "1. Approve retiring the 14 duplicates (draft, history kept).", "2. For the FIX items: approve rewritten replacements in a gap-fill file (drafts), or retire the common-sense Peace items outright.", "3. Approve a Peace and Human Rights gap-fill on the laws listed above."]
open("docs/research/audit/round-03-baseline-b2-gi-review-request.md", "w").write("\n".join(L) + "\n")
print(c)
