"""B2 Analytical (100), tagged track 'both' as GT asked (CSC lists Analytical for the Professional level only; see the report):
25 series, 25 analogies, 25 simple logic, 25 data tables. Also builds the 40 reserve analogies for B3."""
import random
import re
from fractions import Fraction as F
from d22_common import mk, num
import d22_analogy as AN

D = "analytical"
B2, RES = [], []
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def iid(n):
    return f"CIVIO-D1022-ANA-{n:04d}"


n = 0
# ---------- Number series (13), recipe seq ----------
NS = [  # terms, rule text, wrong [(value, code, why)], difficulty
 ([7, 12, 17, 22, 27], "add 5 each time", [(31, "NUM-OFF-BY-ONE", "adds 4 instead of 5"), (35, "NUM-SEQ-OTHER-RULE", "adds 8, a step not in the series"), (54, "NUM-SEQ-OTHER-RULE", "doubles the last term")], "easy"),
 ([3, 5, 9, 15, 23], "the differences grow by 2 (2, 4, 6, 8, so next +10)", [(31, "NUM-SEQ-OTHER-RULE", "repeats the last difference of 8"), (32, "NUM-OFF-BY-ONE", "adds 9; the gaps grow by 2, not 1"), (46, "NUM-SEQ-OTHER-RULE", "doubles the last term")], "medium"),
 ([2, 6, 18, 54], "multiply by 3", [(108, "NUM-SEQ-OTHER-RULE", "multiplies by 2"), (90, "NUM-SEQ-OTHER-RULE", "adds 36 as if the gap were constant"), (160, "NUM-OFF-BY-ONE", "slips by 2 in the multiplication")], "easy"),
 ([4, 9, 19, 39], "double and add 1", [(78, "NUM-PARTIAL", "doubles but forgets the +1"), (59, "NUM-SEQ-OTHER-RULE", "adds the last gap of 20 again"), (80, "NUM-OFF-BY-ONE", "doubles and adds 2")], "medium"),
 ([2, 7, 22, 67], "multiply by 3 and add 1", [(201, "NUM-PARTIAL", "multiplies by 3 but forgets the +1"), (112, "NUM-SEQ-OTHER-RULE", "adds the last gap of 45 again"), (135, "NUM-SEQ-OTHER-RULE", "doubles and adds 1")], "medium"),
 ([6, 30, 9, 27, 12, 24], "two series take turns: 6, 9, 12 (+3) and 30, 27, 24 (−3)", [(21, "NUM-SEQ-OTHER-RULE", "continues the second series, but the next position belongs to the first"), (36, "NUM-SEQ-OTHER-RULE", "adds 12 to the last term"), (14, "NUM-OFF-BY-ONE", "adds 2 instead of 3 to the first series")], "hard"),
 ([2, 3, 5, 8, 13, 21], "each term is the sum of the two before it", [(29, "NUM-SEQ-OTHER-RULE", "adds the last gap of 8 again"), (42, "NUM-SEQ-OTHER-RULE", "doubles the last term"), (33, "NUM-OFF-BY-ONE", "adds 12, one short of 13")], "medium"),
 ([3, 6, 11, 18, 27], "square of the position plus 2 (gaps 3, 5, 7, 9, so next +11)", [(36, "NUM-SEQ-OTHER-RULE", "repeats the last gap of 9"), (37, "NUM-OFF-BY-ONE", "adds 10; the gaps are odd numbers"), (54, "NUM-SEQ-OTHER-RULE", "doubles the last term")], "medium"),
 ([1, 8, 27, 64], "cubes of 1, 2, 3, 4, so next is 5 × 5 × 5", [(100, "NUM-SEQ-OTHER-RULE", "takes 10 squared"), (101, "NUM-SEQ-OTHER-RULE", "adds 37, the last gap"), (128, "NUM-SEQ-OTHER-RULE", "doubles the last term")], "medium"),
 ([100, 96, 88, 76], "subtract 4, 8, 12, so next subtract 16", [(64, "NUM-SEQ-OTHER-RULE", "subtracts 12 again"), (56, "NUM-SEQ-OTHER-RULE", "subtracts 20, one step too far"), (62, "NUM-OFF-BY-ONE", "subtracts 14")], "medium"),
 ([81, 72, 64, 57], "subtract 9, 8, 7, so next subtract 6", [(50, "NUM-SEQ-OTHER-RULE", "subtracts 7 again"), (52, "NUM-OFF-BY-ONE", "subtracts 5"), (49, "NUM-SEQ-OTHER-RULE", "jumps to a perfect square")], "medium"),
 ([3, 4, 8, 17, 33], "add 1, 4, 9, 16 (square numbers), so next add 25", [(49, "NUM-SEQ-OTHER-RULE", "adds 16 again"), (66, "NUM-SEQ-OTHER-RULE", "doubles the last term"), (57, "NUM-OFF-BY-ONE", "adds 24, one short of 25")], "hard"),
 ([1458, 486, 162, 54], "divide by 3", [(27, "NUM-SEQ-OTHER-RULE", "divides by 2"), (45, "NUM-OFF-BY-ONE", "subtracts 9 instead of dividing by 3"), (6, "NUM-SEQ-OTHER-RULE", "divides by 9")], "easy"),
]
NS_FRAMES = ["Find the next number in the series: {s}, ___", "What number comes next: {s}, ___?", "Complete the series with the most logical number: {s}, ___", "Study the pattern and supply the missing term: {s}, ___", "Which number continues this sequence best: {s}, ___?"]
import solver_2026_10_22 as SV  # noqa: E402
for k, (xs, rule, wrong, diff) in enumerate(NS):
    n += 1
    key = SV._seq_next(xs)
    stem = NS_FRAMES[k % 5].format(s=", ".join(map(str, xs)))
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Number series", concept="number series", micro_skill="find the rule from the gaps between terms",
                 archetype="ANA-SYMBOL-SERIES", difficulty=diff, est=45 if diff == "easy" else 50, stem=stem, correct=str(key),
                 wrong=[(str(v), c, f"{v} {w}.") for v, c, w in wrong],
                 terms="A series follows one rule. Test the gaps first; if the gaps change, test the gaps of the gaps, then multiplication, then two series taking turns.",
                 shortcut="Write the differences under the terms; most series show their rule there.",
                 why_correct=f"The rule is: {rule}. Applied to {xs[-1]}, the next term is {key}. Each wrong choice comes from a rule that fits only part of the series.",
                 recipe={"op": "seq", "fmt": "num"}))
# ---------- Letter series (12), native qa solver ----------
LS = [("CF", 2, 2), ("BY", 2, -2), ("AC", 1, 2), ("ZA", -2, 2), ("KM", 1, 2), ("PA", -2, 2), ("AE", 4, 4), ("BC", 3, 3), ("YB", -3, 2), ("DA", 3, 3), ("QZ", 1, -2), ("CA", 3, 1)]
for start, s1, s2 in LS:
    n += 1
    t = [AZ[AZ.index(start[0]) + s1 * k] + AZ[AZ.index(start[1]) + s2 * k] for k in range(5)]
    key = t[4]
    a_, b_ = AZ.index(t[3][0]), AZ.index(t[3][1])
    w = [(AZ[a_ + s1] + AZ[b_ + s2 - (1 if s2 > 0 else -1)], "NUM-OFF-BY-ONE", "moves the second letter one place too few"),
         (AZ[a_ + s1 + (1 if s1 > 0 else -1)] + AZ[b_ + s2], "NUM-OFF-BY-ONE", "moves the first letter one place too many"),
         (AZ[b_ + s2] + AZ[a_ + s1], "LOG-ORDER-SWAP", "has the right letters in swapped order")]
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Letter series", concept="letter series", micro_skill="track each letter position separately",
                 archetype="ANA-SYMBOL-SERIES", difficulty="medium", est=50, stem=f"What comes next in the series? {', '.join(t[:4])}, ___", correct=key,
                 wrong=[(x, c, f"{x} {why}.") for x, c, why in w],
                 terms="In a letter-pair series, each position usually follows its own rule. Number the alphabet (A = 1 … Z = 26) to see the steps.",
                 shortcut="Write the alphabet position under each letter and read the steps for the first and second letters separately.",
                 why_correct=f"First letters move {s1:+d} each time ({', '.join(x[0] for x in t[:4])} → {key[0]}); second letters move {s2:+d} ({', '.join(x[1] for x in t[:4])} → {key[1]}). So the next pair is {key}."))
# ---------- Analogies (25 for B2, 40 reserve) ----------
FRAMES = ["{a} : {b} :: ____", "{A} is to {b} as ____.", "Which pair shows the same relationship as \"{a} : {b}\"?"]
order = list(range(len(AN.A)))
random.Random("d22-analogy").shuffle(order)


def analogy(idx, row, track, prefix):
    a, b, rel, arch, (c, d), wr = row
    stem = FRAMES[idx % 3].format(a=a.upper() if idx % 3 == 0 else a, b=b.upper() if idx % 3 == 0 else b, A=a.capitalize())
    return mk(id=prefix, track=track, domain=D, competency="Word analogy", concept="word analogy", micro_skill="name the relationship, then match it",
              archetype=arch, difficulty="easy" if arch in (AN.SYN, AN.FM) else "medium", est=25 if arch == AN.SYN else 30, stem=stem, correct=f"{c} : {d}",
              wrong=[(f"{x} : {y}", code, f"\"{x} : {y}\" {AN.WHY[code]}.") for x, y, code in wr],
              terms=f"An analogy compares two relationships. Here the relationship is: {rel}.",
              shortcut=f"Make a sentence for the first pair (\"{a} is … {b}\") and test each choice in the same sentence, keeping the order.",
              why_correct=f"\"{c} : {d}\" fits the same sentence: {rel}. The order also matches: the first word stands to the second exactly as {a} stands to {b}.",
              recipe={"op": "judgment"})


for j, k in enumerate(order[:25]):
    n += 1
    B2.append(analogy(j, AN.A[k], "both", iid(n)))
for j, k in enumerate(order[25:]):
    RES.append(analogy(j + 1, AN.A[k], "professional", f"CIVIO-D1022-RSANA-{j + 1:04d}"))
# ---------- Simple logic (25) ----------
ORDS = [  # relation phrase, pairs (a before b), question
 ("finished the report earlier than", [("Carlo", "Ana"), ("Ana", "Ben"), ("Ben", "Dina")], "second"),
 ("has served longer than", [("Rhea", "Jomar"), ("Nestor", "Rhea"), ("Jomar", "Grace")], "third"),
 ("scored higher than", [("Tess", "Efren"), ("Bong", "Cora"), ("Efren", "Bong")], "second"),
 ("lives nearer the office than", [("Aileen", "Dindo"), ("Dindo", "Lourdes"), ("Marites", "Aileen")], "third"),
 ("arrived earlier than", [("Paolo", "Joy"), ("Joy", "Arnel"), ("Arnel", "Mylene")], "third"),
 ("encoded more forms than", [("Inday", "Rogelio"), ("Kimberly", "Inday"), ("Rogelio", "Analyn")], "second"),
]
for rel, pairs, which in ORDS:
    n += 1
    names = []
    rem = {x for p in pairs for x in p}
    while rem:
        top = [x for x in rem if not any(b == x and a in rem for a, b in pairs)]
        names.append(top[0]); rem.discard(top[0])
    k = 1 if which == "second" else 2
    key = names[k]
    sh = pairs[:]
    random.Random(rel).shuffle(sh)
    stem = "Four staff members are compared. " + " ".join(f"{a} {rel} {b}." for a, b in sh) + f" Who is {which}?"
    others = [x for x in names if x != key]
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Logical reasoning", concept="ordering", micro_skill="build a chain from pairwise clues",
                 archetype="ANA-CONCLUSION", difficulty="medium", est=60, stem=stem, correct=key,
                 wrong=[(others[0], "LOG-ORDER-REVERSED", f"{others[0]} is in position {names.index(others[0]) + 1}, not {which}."),
                        (others[1], "LOG-IGNORED-CLUE", f"{others[1]} is in position {names.index(others[1]) + 1}; one clue was skipped."),
                        (others[2], "LOG-ORDER-SWAP", f"{others[2]} is in position {names.index(others[2]) + 1}; check the direction of each clue.")],
                 terms="An ordering puzzle gives pairwise clues; link them into one chain from first to last.",
                 shortcut="Start with the person who never appears after \"than\"; that person is first.",
                 why_correct=f"Linking the clues gives the order {' → '.join(names)}. The {which} is {key}. Every clue is used once, and the chain has no gaps."))
SYL = [
 ("All licensed midwives are registered health workers.", "All registered health workers are listed in the provincial health roster.", "All licensed midwives are listed in the provincial health roster.",
  [("All people in the provincial health roster are licensed midwives.", "LOG-CONVERSE"), ("Some registered health workers are not licensed midwives.", "LOG-COULD-NOT-MUST"), ("No licensed midwives are listed in the provincial health roster.", "LOG-OVERSTRONG")]),
 ("All barangay tanods are trained first responders.", "Some barangay tanods are retired soldiers.", "Some trained first responders are retired soldiers.",
  [("All trained first responders are retired soldiers.", "LOG-OVERSTRONG"), ("All retired soldiers are barangay tanods.", "LOG-CONVERSE"), ("No trained first responders are retired soldiers.", "LOG-COULD-NOT-MUST")]),
 ("All accredited cooperatives are registered with the CDA.", "No registered with the CDA are unlicensed lenders.", None, None),
 ("All scholarship grantees are enrolled students.", "No enrolled students are full-time employees of the city.", "No scholarship grantees are full-time employees of the city.",
  [("All full-time employees of the city are scholarship grantees.", "LOG-CONVERSE"), ("Some scholarship grantees are full-time employees of the city.", "LOG-COULD-NOT-MUST"), ("No enrolled students are scholarship grantees.", "LOG-OVERSTRONG")]),
 ("All public-school teachers are holders of a professional license.", "All holders of a professional license are listed with the PRC.", "All public-school teachers are listed with the PRC.",
  [("All listed with the PRC are public-school teachers.", "LOG-CONVERSE"), ("Some public-school teachers are not listed with the PRC.", "LOG-COULD-NOT-MUST"), ("No holders of a professional license are public-school teachers.", "LOG-OVERSTRONG")]),
 ("All coastal barangays are flood-risk areas.", "Some coastal barangays are tourist spots.", "Some flood-risk areas are tourist spots.",
  [("All tourist spots are flood-risk areas.", "LOG-OVERSTRONG"), ("All flood-risk areas are coastal barangays.", "LOG-CONVERSE"), ("No tourist spots are coastal barangays.", "LOG-COULD-NOT-MUST")]),
 ("All night-shift guards are holders of a security license.", "No holders of a security license are minors.", "No night-shift guards are minors.",
  [("All minors are night-shift guards.", "LOG-CONVERSE"), ("Some night-shift guards are minors.", "LOG-COULD-NOT-MUST"), ("No holders of a security license are night-shift guards.", "LOG-OVERSTRONG")]),
 ("All night-market vendors are holders of a sanitary permit.", "All holders of a sanitary permit are inspected each quarter.", "All night-market vendors are inspected each quarter.",
  [("All inspected each quarter are night-market vendors.", "LOG-CONVERSE"), ("Some night-market vendors are not inspected each quarter.", "LOG-COULD-NOT-MUST"), ("No holders of a sanitary permit are night-market vendors.", "LOG-OVERSTRONG")]),
 ("All approved permits are signed by the mayor.", "Some approved permits are building permits.", "Some signed by the mayor are building permits.", None),
]
SYL = [r for r in SYL if r[2] and r[3]]
for s1, s2, key, wr in SYL:
    n += 1
    stem = f"Statement 1: {s1} Statement 2: {s2} Which conclusion follows?"
    WHYC = {"LOG-CONVERSE": "reverses the statement; \"all A are B\" does not mean \"all B are A\"",
            "LOG-COULD-NOT-MUST": "may or may not be true; the statements do not decide it",
            "LOG-OVERSTRONG": "claims more than the statements give, or contradicts them"}
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Logical reasoning", concept="syllogism", micro_skill="draw only what must follow from two statements",
                 archetype="ANA-SYLLOGISM", difficulty="medium", est=60, stem=stem, correct=key,
                 wrong=[(t, c, f"This {WHYC[c]}.") for t, c in wr],
                 terms="A syllogism links two statements through a shared middle group. A valid conclusion must be true in every picture the statements allow.",
                 shortcut="Draw the groups as circles: put the first group inside the second, then test each conclusion.",
                 why_correct=f"Statement 1 puts one group inside the middle group, and Statement 2 says how the middle group relates to the last group. So \"{key}\" must be true; nothing else is guaranteed.",
                 gen_frame=f"SYL-{'A' if s2.startswith('All') else 'S' if s2.startswith('Some') else 'N'}-d22"))
CODES = [("PLANT", 2, "GRASS"), ("FILES", -1, "STAMP"), ("BUDGET", 3, "VOUCHER"), ("CLERK", 4, "DRAFT"), ("FORM", -2, "SEAL"), ("PERMIT", 5, "LICENSE")]
for w1, k, w2 in CODES:
    n += 1
    enc = lambda w, s: "".join(AZ[(AZ.index(ch) + s) % 26] for ch in w)
    key = enc(w2, k)
    stem = f"In a certain code, {w1} is written as {enc(w1, k)}. How is {w2} written in that code?"
    wr = [(enc(w2, -k), "LOG-ORDER-REVERSED", f"shifts each letter {-k:+d}, the opposite direction"),
          (enc(w2, k + (1 if k > 0 else -1)), "NUM-OFF-BY-ONE", f"shifts each letter {k + (1 if k > 0 else -1):+d}, one place too far"),
          (enc(w2, k)[::-1], "LOG-ORDER-SWAP", "has the right letters written backward")]
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Logical reasoning", concept="coding-decoding", micro_skill="find a letter shift and apply it",
                 archetype="ANA-SYMBOL-SERIES", difficulty="medium", est=50, stem=stem, correct=key,
                 wrong=[(t, c, f"{t} {why}.") for t, c, why in wr],
                 terms="A shift code moves every letter the same number of places in the alphabet; after Z it wraps back to A.",
                 shortcut=f"Compare one letter pair: {w1[0]} → {enc(w1, k)[0]} is {k:+d}; check one more pair to be sure.",
                 why_correct=f"Each letter of {w1} moves {k:+d} places to give {enc(w1, k)}. Applying {k:+d} to {w2} gives {key}."))
COND = [
 ("If the generator is switched on, the server room lights are on. The server room lights are off. What follows?", "The generator is not switched on.",
  [("The generator is switched on.", "LOG-CONVERSE", "contradicts the statement: lights off rules out a running generator"), ("The power from the grid is out.", "LOG-IRRELEVANT", "brings in a fact the statements never mention"), ("The lights are broken.", "LOG-COULD-NOT-MUST", "might be true, but the statements do not say so")],
  "If P then Q; not Q; so not P (modus tollens)."),
 ("Only employees with an ID may enter the records room. Lito entered the records room. What follows?", "Lito has an ID.",
  [("Lito is a records officer.", "LOG-COULD-NOT-MUST", "may be true, but the rule only says entrants have an ID"), ("Everyone with an ID enters the records room.", "LOG-CONVERSE", "reverses the rule; \"only\" sets a requirement, not a promise"), ("Lito does not have an ID.", "LOG-OVERSTRONG", "contradicts the rule")],
  "\"Only A may do B\" means anyone who does B is A."),
 ("Either the meeting is in Room 2 or it is in the conference hall. It is not in the conference hall. Where is the meeting?", "In Room 2",
  [("In both rooms", "LOG-OVERSTRONG", "the statements give two exclusive places"), ("It cannot be determined", "LOG-MISSED-NEEDED", "the second statement removes one of the only two choices"), ("In the conference hall", "LOG-CONVERSE", "contradicts the second statement")],
  "Either A or B; not B; so A (disjunctive syllogism)."),
 ("If a form is signed, it is filed the same day. Form 18 was filed the same day. What can be concluded?", "Nothing certain about whether Form 18 was signed",
  [("Form 18 was signed.", "LOG-CONVERSE", "assumes the converse; unsigned forms might also be filed the same day"), ("Form 18 was not signed.", "LOG-OVERSTRONG", "nothing rules out a signature"), ("All forms are filed the same day.", "LOG-OVERSTRONG", "generalizes beyond the statement")],
  "Affirming the consequent is invalid: Q being true does not prove P."),
 ("No applicant without a birth certificate is interviewed. Joy was interviewed. What follows?", "Joy has a birth certificate.",
  [("Joy was hired.", "LOG-IRRELEVANT", "hiring is never mentioned"), ("Every applicant with a birth certificate is interviewed.", "LOG-CONVERSE", "reverses the rule"), ("Joy has no birth certificate.", "LOG-OVERSTRONG", "contradicts the rule")],
  "\"No one without A does B\" means everyone who does B has A."),
 ("If it rains, the outreach is moved to the covered court. If the outreach is moved to the covered court, the chairs must be borrowed from the school. It rains. What follows?", "The chairs must be borrowed from the school.",
  [("The outreach is cancelled.", "LOG-IRRELEVANT", "cancellation is never mentioned"), ("The school is closed.", "LOG-IRRELEVANT", "nothing is said about the school's schedule"), ("The outreach stays outdoors.", "LOG-CONVERSE", "contradicts the first statement")],
  "If P then Q, and if Q then R; P; so R (a chain of conditions)."),
]
for stem, key, wr, rule in COND:
    n += 1
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Logical reasoning", concept="conditional reasoning", micro_skill="apply if-then, only-if and either-or rules",
                 archetype="ANA-CONCLUSION", difficulty="medium", est=60, stem=stem, correct=key, wrong=[(t, c, f"This {w}.") for t, c, w in wr],
                 terms=f"Conditional statements fix what must follow. Rule used here: {rule}",
                 shortcut="Rewrite the statements as arrows (P → Q) and follow only the arrows given.",
                 why_correct=f"\"{key}\" is the only choice that must be true. {rule} The other choices reverse the rule, overreach, or bring in outside facts.",
                 recipe={"op": "judgment"}))
# ---------- Data tables (25), recipe tbl ----------
rng = random.Random("d22-tables")
TB = [
 ("Permits issued by the Business Permits Office, first quarter (number of permits)", "Type", ["January", "February", "March"], ["New business", "Renewal", "Special event"], [("row_sum", ["Renewal"], [], "How many renewal permits were issued in the whole quarter?")]),
 ("Patients seen at a rural health unit by day (number of patients)", "Service", ["Monday", "Tuesday", "Wednesday", "Thursday"], ["Check-up", "Immunization", "Prenatal", "Dental"], [("argmax_col", [], ["Tuesday"], "Which service had the most patients on Tuesday?")]),
 ("Relief packs released by three evacuation centers (packs)", "Center", ["Day 1", "Day 2", "Day 3"], ["School", "Gym", "Chapel"], [("cell_diff", ["Gym", "School"], ["Day 2"], "On Day 2, how many more packs did the Gym release than the School?")]),
 ("Books borrowed from the municipal library by month (number of books)", "Section", ["June", "July", "August"], ["Fiction", "Reference", "Children"], [("col_sum", [], ["July"], "How many books were borrowed in July from all sections?")]),
 ("Seedlings planted by barangay (number of seedlings)", "Barangay", ["Mahogany", "Narra", "Mango"], ["Bagong Silang", "San Roque", "Poblacion", "Malinis"], [("argmin_col", [], ["Narra"], "Which barangay planted the fewest Narra seedlings?")]),
 ("Monthly electricity use of three offices (kWh)", "Office", ["April", "May", "June"], ["Treasury", "Assessor", "Engineering"], [("row_avg", ["Assessor"], [], "What was the Assessor office's average monthly use over the three months, in kWh?")]),
 ("Complaints received by the Action Center by channel (number of complaints)", "Channel", ["Week 1", "Week 2", "Week 3", "Week 4"], ["Hotline", "Walk-in", "Email"], [("col_range", [], ["Week 3"], "In Week 3, what is the difference between the largest and smallest number of complaints across the channels?")]),
 ("Kilograms of rice distributed by a feeding program (kg)", "School", ["Term 1", "Term 2"], ["Rizal ES", "Bonifacio ES", "Mabini ES", "Luna ES"], [("two_col_diff_total", [], ["Term 2", "Term 1"], "How many more kilograms were distributed in Term 2 than in Term 1, for all schools combined?")]),
 ("Applicants screened per day at a job fair (number of applicants)", "Booth", ["Day 1", "Day 2", "Day 3"], ["Retail", "BPO", "Construction", "Health"], [("count_above", [], ["Day 2"], "On Day 2, how many booths screened more than {t} applicants?")]),
 ("Water consumed by four public markets (cubic meters)", "Market", ["July", "August"], ["North", "South", "East", "West"], [("argmax_rowsum", [], [], "Which market used the most water over the two months combined?")]),
 ("Trainees who finished each course (number of trainees)", "Course", ["Batch A", "Batch B", "Batch C"], ["Welding", "Baking", "Driving"], [("times", ["Baking", "Driving"], ["Batch A"], "In Batch A, how many times as many trainees finished Baking as finished Driving?")]),
 ("Bond paper used by three divisions (reams)", "Division", ["Q1", "Q2", "Q3"], ["Admin", "Finance", "Legal"], [("cost", ["Finance"], ["Q2"], "If a ream costs ₱{p}, how much did the Finance division's Q2 paper cost?")]),
 ("Vehicles passing a checkpoint by hour (number of vehicles)", "Vehicle", ["6–7 a.m.", "7–8 a.m.", "8–9 a.m."], ["Jeepney", "Tricycle", "Truck", "Private car"], [("row_sum", ["Tricycle"], [], "How many tricycles passed in the three hours?")]),
 ("Fish landed at the municipal port by boat type (kilograms)", "Boat", ["Monday", "Tuesday", "Wednesday"], ["Banca", "Motorboat", "Trawler"], [("col_avg", [], ["Wednesday"], "What was the average catch per boat type on Wednesday, in kilograms?")]),
 ("Voters assisted at four precincts (number of voters)", "Precinct", ["Morning", "Afternoon"], ["Precinct 1", "Precinct 2", "Precinct 3", "Precinct 4"], [("argmin_col", [], ["Afternoon"], "Which precinct assisted the fewest voters in the afternoon?")]),
 ("Garbage collected by truck route (tons)", "Route", ["Week 1", "Week 2", "Week 3"], ["Route A", "Route B", "Route C"], [("cell_diff", ["Route C", "Route A"], ["Week 1"], "In Week 1, how many more tons did Route C collect than Route A?")]),
 ("Students in each grade who joined the reading camp (number of students)", "Grade", ["Boys", "Girls"], ["Grade 3", "Grade 4", "Grade 5", "Grade 6"], [("col_sum", [], ["Girls"], "How many girls joined the reading camp in all?")]),
 ("Typhoon shelters' occupancy by night (families)", "Shelter", ["Night 1", "Night 2", "Night 3", "Night 4"], ["Covered court", "Day care", "Health center"], [("row_avg", ["Day care"], [], "On average, how many families stayed at the Day care each night?")]),
 ("Tickets sold for a town fiesta event (tickets)", "Event", ["Friday", "Saturday", "Sunday"], ["Concert", "Fun run", "Cook-off", "Film night"], [("argmax_col", [], ["Saturday"], "Which event sold the most tickets on Saturday?")]),
 ("Hours of overtime logged by unit (hours)", "Unit", ["May", "June", "July"], ["Records", "Cashier", "IT", "Motor pool"], [("col_range", [], ["June"], "In June, what is the difference between the most and the fewest overtime hours logged by a unit?")]),
 ("Liters of fuel used by service vehicles (liters)", "Vehicle", ["Week 1", "Week 2"], ["Ambulance", "Patrol car", "Dump truck"], [("two_col_diff_total", [], ["Week 1", "Week 2"], "How many more liters were used in Week 1 than in Week 2, for all vehicles together?")]),
 ("Visitors to provincial tourist sites (visitors)", "Site", ["March", "April", "May"], ["Falls", "Lighthouse", "Old church", "Beach park"], [("count_above", [], ["April"], "In April, how many sites had more than {t} visitors?")]),
 ("Meals served by a school canteen (meals)", "Meal", ["Monday", "Tuesday", "Wednesday"], ["Breakfast", "Lunch", "Snack"], [("times", ["Lunch", "Breakfast"], ["Wednesday"], "On Wednesday, how many times as many lunches were served as breakfasts?")]),
 ("Bags of cement delivered to project sites (bags)", "Site", ["Week 1", "Week 2", "Week 3"], ["Bridge", "Health center", "Covered court"], [("cost", ["Bridge"], ["Week 3"], "At ₱{p} a bag, what was the cost of the cement delivered to the Bridge site in Week 3?")]),
 ("Barangay clearances issued by purpose (clearances)", "Purpose", ["January", "February", "March"], ["Employment", "Loan", "Travel", "School"], [("argmax_rowsum", [], [], "For which purpose were the most clearances issued over the three months?")]),
]
DIF = {"row_sum": ("easy", 45), "col_sum": ("easy", 45), "cell_diff": ("easy", 45), "argmax_col": ("easy", 40), "argmin_col": ("easy", 40),
       "row_avg": ("medium", 75), "col_avg": ("medium", 75), "col_range": ("medium", 60), "two_col_diff_total": ("medium", 75), "count_above": ("medium", 60),
       "argmax_rowsum": ("medium", 75), "times": ("medium", 60), "cost": ("medium", 60)}
for title, rh, cols, rows, [(do, rr, cc, q)] in TB:
    n += 1
    for _ in range(200):
        data = {r: [rng.randrange(12, 99) for _ in cols] for r in rows}
        if do in ("row_avg",):
            s = sum(data[rr[0]]); data[rr[0]][-1] += (-s) % len(cols)
        if do == "col_avg":
            ci = cols.index(cc[0]); s = sum(data[r][ci] for r in rows); data[rows[-1]][ci] += (-s) % len(rows)
        if do == "times":
            ci = cols.index(cc[0]); data[rr[1]][ci] = rng.randrange(6, 16); data[rr[0]][ci] = data[rr[1]][ci] * rng.choice([2, 3, 4])
        if do in ("cell_diff",):
            ci = cols.index(cc[0])
            if data[rr[0]][ci] <= data[rr[1]][ci]:
                data[rr[0]][ci], data[rr[1]][ci] = data[rr[1]][ci] + 7, data[rr[0]][ci]
        if do == "two_col_diff_total":
            c1, c2 = cols.index(cc[0]), cols.index(cc[1])
            if sum(data[r][c1] for r in rows) <= sum(data[r][c2] for r in rows):
                for r in rows:
                    data[r][c1], data[r][c2] = data[r][c2], data[r][c1]
        vals = [v for r in rows for v in data[r]]
        ok = True
        if do in ("argmax_col", "argmin_col"):
            v = [data[r][cols.index(cc[0])] for r in rows]; ok = len(set(v)) == len(v)
        if do == "argmax_rowsum":
            v = [sum(data[r]) for r in rows]; ok = len(set(v)) == len(v)
        if ok:
            break
    t = 50
    if do == "count_above":
        ci = cols.index(cc[0]); t = sorted(data[r][ci] for r in rows)[1] + 0
        if any(data[r][ci] == t for r in rows):
            pass
    price = rng.choice([195, 215, 240, 265]) if do == "cost" and "ream" in q else rng.choice([255, 280, 310])
    qq = q.format(t=t, p=price)
    table = f"{title}\n{rh} | " + " | ".join(cols) + "\n" + "\n".join(f"{r} | " + " | ".join(str(x) for x in data[r]) for r in rows)
    stem = f"Study the table, then answer the question.\n{table}\n\n{qq}"
    args = {"do": do, "rows": rr, "cols": cc}
    if do in ("cell_diff", "times"):
        args["cells"] = [[rr[0], cc[0]], [rr[1], cc[0]]]
    if do == "cost":
        args["cells"] = [[rr[0], cc[0]]]; args["price"] = price
    if do == "count_above":
        args["t"] = t
    recipe = {"op": "tbl", "args": args, "fmt": "peso" if do == "cost" else "num"}
    key = SV.fmt(SV._tbl(args, stem), recipe)
    ci = cols.index(cc[0]) if cc else None
    if do.startswith("arg"):
        wrong_names = [r for r in rows if r != key][:3]
        wr = [(w, "DI-WRONG-CELL", f"{w} is not the {'highest' if 'max' in do else 'lowest'} value asked for; recheck the {cc[0] if cc else 'row totals'}.") for w in wrong_names]
        how = "Compare the values in the named column" if cc else "Add each row across, then compare the totals"
    else:
        kv = SV._tbl(args, stem)
        alts = {
            "row_sum": lambda: [kv - data[rr[0]][-1], kv + data[rows[0]][0] if rows[0] != rr[0] else kv + data[rows[1]][0], max(data[rr[0]])],
            "col_sum": lambda: [kv - data[rows[-1]][ci], sum(data[rows[0]]), kv + 10],
            "cell_diff": lambda: [data[rr[0]][ci] + data[rr[1]][ci], data[rr[0]][ci], kv + 10],
            "row_avg": lambda: [sum(data[rr[0]]), kv + 3, F(sum(data[rr[0]]), len(cols) - 1)],
            "col_avg": lambda: [sum(data[r][ci] for r in rows), kv + 4, F(sum(data[r][ci] for r in rows), len(rows) + 1)],
            "col_range": lambda: [max(data[r][ci] for r in rows), kv + 5, max(data[r][ci] for r in rows) - sorted(data[r][ci] for r in rows)[1]],
            "two_col_diff_total": lambda: [sum(data[r][cols.index(cc[0])] for r in rows), kv + 10, abs(data[rows[0]][cols.index(cc[0])] - data[rows[0]][cols.index(cc[1])])],
            "count_above": lambda: [kv + 1, kv - 1 if kv > 1 else kv + 2, len(rows)],
            "times": lambda: [kv + 1, data[rr[0]][ci] - data[rr[1]][ci], F(data[rr[1]][ci], data[rr[0]][ci])],
            "cost": lambda: [kv + price, F(data[rr[0]][ci]), kv - price],
        }[do]()
        codes = {"row_sum": ["DI-WRONG-CELL", "DI-WRONG-CELL", "DI-NOT-SUPPORTED"], "col_sum": ["DI-WRONG-CELL", "DI-WRONG-CELL", "NUM-OFF-BY-ONE"],
                 "cell_diff": ["NUM-OP-SWAP", "NUM-PARTIAL", "NUM-OFF-BY-ONE"], "row_avg": ["NUM-PARTIAL", "NUM-OFF-BY-ONE", "DI-WRONG-BASE"],
                 "col_avg": ["NUM-PARTIAL", "NUM-OFF-BY-ONE", "DI-WRONG-BASE"], "col_range": ["NUM-PARTIAL", "NUM-OFF-BY-ONE", "DI-WRONG-CELL"],
                 "two_col_diff_total": ["NUM-PARTIAL", "NUM-OFF-BY-ONE", "DI-WRONG-CELL"], "count_above": ["NUM-OFF-BY-ONE", "NUM-OFF-BY-ONE", "DI-NOT-SUPPORTED"],
                 "times": ["NUM-OFF-BY-ONE", "NUM-OP-SWAP", "DI-WRONG-BASE"], "cost": ["NUM-EXTRA-STEP", "NUM-PARTIAL", "NUM-OFF-BY-ONE"]}[do]
        whys = {"DI-WRONG-CELL": "uses a wrong row or column from the table", "DI-NOT-SUPPORTED": "is a single cell, not the total asked for", "NUM-OFF-BY-ONE": "is a near miss from a slip in adding or counting",
                "NUM-OP-SWAP": "uses the wrong operation", "NUM-PARTIAL": "stops before the last step", "DI-WRONG-BASE": "divides by the wrong count or compares in the wrong direction",
                "NUM-EXTRA-STEP": "adds a step the question does not ask for"}
        wr = []
        for v, c in zip(alts, codes):
            t_ = SV.fmt(F(v), recipe)
            if t_ == key or t_ in [w[0] for w in wr]:
                t_ = SV.fmt(F(v) + 2, recipe)
            wr.append((t_, c, f"{t_} {whys[c]}."))
        how = {"row_sum": "Add the three cells in that row", "col_sum": "Add every cell in that column", "cell_diff": "Find the two cells and subtract",
               "row_avg": "Add the row and divide by the number of months or days", "col_avg": "Add the column and divide by the number of rows",
               "col_range": "Find the largest and smallest values in the column and subtract", "two_col_diff_total": "Total each column, then subtract",
               "count_above": "Count the values in the column that are greater than the threshold", "times": "Divide the first cell by the second",
               "cost": "Multiply the quantity in the cell by the unit price"}[do]
    diff, est = DIF[do]
    B2.append(mk(id=iid(n), track="both", domain=D, competency="Data interpretation", concept="data table", micro_skill="read the right cells and compute",
                 archetype="ANA-DI-TABLE", difficulty=diff, est=est, stem=stem, correct=key, wrong=wr,
                 terms="A data table lists values by row and column. Locate the row and column named in the question before you compute.",
                 shortcut="Put a finger on the row label and another on the column label; read only where they meet.",
                 why_correct=f"{how}: the result is {key}. The table gives every value needed, so nothing outside it is assumed.",
                 recipe=recipe))
