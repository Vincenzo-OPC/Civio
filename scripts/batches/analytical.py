"""Analytical Ability (Professional track). Series, codes, ranking and tables are computed; syllogisms and analogies come from coded tables."""
from common import make, peso, num, Skip, FIRST, PLACES, OFFICES

B = dict(track="professional", domain="analytical")
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def L(i):
    return AZ[i % 26]


def letter_series(rng, iid):
    start = rng.randint(0, 8)
    a, b = rng.randint(1, 4), rng.randint(1, 3)
    # pairs: first letter +a, second letter +b, from a second start
    s2 = rng.randint(10, 20)
    terms = [L(start + a * i) + L(s2 + b * i) for i in range(4)]
    ans = L(start + a * 4) + L(s2 + b * 4)
    w1 = L(start + a * 4) + L(s2 + a * 4) if a != b else L(start + a * 4) + L(s2 + b * 4 + 1)
    w2 = L(start + a * 3 + 1) + L(s2 + b * 4)
    w3 = L(s2 + b * 4) + L(start + a * 4)
    if start + a * 4 > 25 or s2 + b * 4 > 25 or len({ans, w1, w2, w3}) < 4:
        raise Skip()
    return make(id=iid, **B, competency="Logic", concept="letter series", micro_skill="track two letter jumps at once", archetype="ANA-SYMBOL-SERIES",
                difficulty="medium", est=45, stem=f"What comes next in the series?  {', '.join(terms)}, ___", correct=ans,
                wrong=[(w1, "NUM-SEQ-OTHER-RULE", f"{w1} moves the second letter by {a}, the jump of the first letter. The second letter has its own jump, +{b}."),
                       (w2, "NUM-OFF-BY-ONE", f"{w2} moves the first letter by only 1. Its jump is +{a}."),
                       (w3, "ANA-REVERSED", f"{w3} has the right two letters in the wrong order.")],
                terms="A \"letter series\" works like a number series. Count each letter's place in the alphabet (A = 1, B = 2, and so on).",
                shortcut=f"Split each pair. First letters: {', '.join(t[0] for t in terms)} (jump +{a}). Second letters: {', '.join(t[1] for t in terms)} (jump +{b}). Move each one more step.",
                why_correct=f"{ans} is right: {terms[-1][0]} + {a} = {ans[0]} and {terms[-1][1]} + {b} = {ans[1]}.", rng=rng)


WORDS = ["CLERK", "PAPER", "STAMP", "FILES", "BOARD", "AGENT", "LEDGER", "MEMO", "VOTER", "TOWN", "CHAIR", "TAXES", "PERMIT", "RECORD", "NOTICE", "OFFICE",
         "MAYOR", "PUBLIC", "BUDGET", "AUDIT", "PLAZA", "RIVER", "FARM", "HEALTH", "SCHOOL", "MARKET", "CENSUS", "BRIDGE", "PORT", "LIBRARY"]


def code_shift(rng, iid):
    w1, w2 = rng.sample(WORDS, 2)
    k = rng.choice([1, 2, 3, -1, -2])
    enc = lambda w, s: "".join(L(AZ.index(c) + s) for c in w)
    ans = enc(w2, k)
    wa = enc(w2, -k)
    wb = enc(w2, k + (1 if k > 0 else -1))
    wc = ans[:-1] + L(AZ.index(w2[-1]))  # last letter left unshifted
    if len({ans, wa, wb, wc}) < 4:
        raise Skip()
    dirn = f"{abs(k)} place{'s' if abs(k) > 1 else ''} {'forward' if k > 0 else 'back'}"
    return make(id=iid, **B, competency="Logic", concept="letter coding", micro_skill="find and apply a letter shift", archetype="ANA-SYMBOL-SERIES",
                difficulty="medium", est=50, stem=f"In a certain code, {w1} is written as {enc(w1, k)}. How is {w2} written in the same code?", correct=ans,
                wrong=[(wa, "ANA-REVERSED", f"{wa} shifts each letter {abs(k)} the other way."),
                       (wb, "NUM-OFF-BY-ONE", f"{wb} shifts each letter one place too far."),
                       (wc, "NUM-PARTIAL", f"{wc} leaves the last letter unchanged.")],
                terms="In a \"code\" item, each letter is swapped for another by one rule. Find the rule from the example, then use it.",
                shortcut=f"Compare the first letters: {w1[0]} became {enc(w1, k)[0]}. That is {dirn}. Check one more letter, then shift every letter of {w2} the same way.",
                why_correct=f"{ans} is right: each letter of {w2} moved {dirn}.", rng=rng)


def ranking(rng, iid):
    n = rng.sample(FIRST, 4)
    rng.shuffle(n)
    trait = rng.choice([("finished the report earlier than", "finished first"), ("has served longer than", "has served the longest"),
                        ("scored higher than", "got the highest score"), ("lives nearer the office than", "lives nearest"),
                        ("arrived earlier than", "arrived first"), ("encoded more forms than", "encoded the most forms")])
    a, b, c, d = n
    cl = {"ca": f"{c} {trait[0]} {a}.", "ab": f"{a} {trait[0]} {b}.", "bd": f"{b} {trait[0]} {d}."}
    true = [c, a, b, d]  # from the top
    clues = list(cl.values())
    rng.shuffle(clues)
    ask = rng.choice(["second", "third"])
    if ask == "second":
        ans = a
        wrong = [(c, "LOG-ORDER-SWAP", f"{c} is first. Choosing {c} swaps the top two places."),
                 (b, "LOG-ORDER-REVERSED", f"{b} is second from the bottom, not from the top. This counts from the wrong end."),
                 (d, "LOG-IGNORED-CLUE", f"{d} could be second only if you skip the clue \"{cl['bd']}\" That clue puts {d} last.")]
    else:
        ans = b
        wrong = [(d, "LOG-ORDER-SWAP", f"{d} is last. Choosing {d} swaps the bottom two places."),
                 (a, "LOG-ORDER-REVERSED", f"{a} is third from the bottom, not from the top. This counts from the wrong end."),
                 (c, "LOG-IGNORED-CLUE", f"{c} could be third only if you skip the clue \"{cl['ca']}\" That clue puts {c} first.")]
    it = make(id=iid, **B, competency="Logic", concept="ordering", micro_skill="chain comparison clues into one order", archetype="ANA-CONCLUSION",
              difficulty="medium", est=60,
              stem=f"Four staff members are compared. {' '.join(clues)} Who is {ask} in the order (counting from the one who {trait[1]})?", correct=ans,
              wrong=wrong, terms="An \"ordering\" item gives pairs. Join the pairs into one line, and count from the end the question names.",
              shortcut=f"Start from the person nobody beats and follow the clues down: {' → '.join(true)}.",
              why_correct=f"{ans} is right. The clues give {' → '.join(true)}, so {ans} is {ask}.", rng=rng)
    return it


ITEMS = ["bond paper (reams)", "ballpens (boxes)", "folders (packs)", "toner (units)", "staplers", "envelopes (boxes)"]


def di_table(rng, iid):
    offs = rng.sample(["Records", "Cashier", "HR", "Planning", "Engineering", "Health", "Library", "Assessor"], 3)
    item = rng.choice(ITEMS)
    q = {o: [rng.randint(5, 40) * 2 for _ in range(3)] for o in offs}
    months = rng.choice([["Jan", "Feb", "Mar"], ["Apr", "May", "Jun"], ["Jul", "Aug", "Sep"]])
    kind = rng.choice(["total", "diff", "pct"])
    tgt = rng.choice(offs)
    rows = "; ".join(f"{o}: {', '.join(f'{m} {v}' for m, v in zip(months, q[o]))}" for o in offs)
    stemhead = f"Supply use of {item} by office ({rows})."
    if kind == "total":
        ans = sum(q[tgt])
        col = sum(q[o][1] for o in offs)
        wr = [(str(col), "DI-WRONG-CELL", f"{col} adds the {months[1]} column for all offices, not the {tgt} row."),
              (str(sum(q[tgt][:2])), "NUM-PARTIAL", f"{sum(q[tgt][:2])} adds only {months[0]} and {months[1]}."),
              (str(round(ans / 3, 1)).rstrip("0").rstrip("."), "DI-NOT-SUPPORTED", "This is the monthly average. The question asks for the total.")]
        stem = f"{stemhead} How many did {tgt} use in all three months?"
        sc = f"Read across the {tgt} row only: {' + '.join(map(str, q[tgt]))}."
        wc = f"{ans} is right: {' + '.join(map(str, q[tgt]))} = {ans}."
    elif kind == "diff":
        o2 = rng.choice([o for o in offs if o != tgt])
        ans = abs(q[tgt][2] - q[o2][2])
        wr = [(str(abs(q[tgt][0] - q[o2][0])), "DI-WRONG-CELL", f"This uses {months[0]}, not {months[2]}."),
              (str(q[tgt][2] + q[o2][2]), "NUM-OP-SWAP", "This adds the two numbers instead of subtracting."),
              (str(abs(sum(q[tgt]) - sum(q[o2]))), "DI-WRONG-CELL", "This compares the three-month totals, not one month.")]
        if q[tgt][2] == q[o2][2]:
            raise Skip()
        big, small = (tgt, o2) if q[tgt][2] > q[o2][2] else (o2, tgt)
        stem = f"{stemhead} In {months[2]}, how many more did {big} use than {small}?"
        sc = f"Go to the {months[2]} column: {tgt} {q[tgt][2]}, {o2} {q[o2][2]}. Subtract the smaller from the larger."
        wc = f"{ans} is right: {max(q[tgt][2], q[o2][2])} − {min(q[tgt][2], q[o2][2])} = {ans}."
    else:
        tot = sum(q[tgt])
        v = q[tgt][0]
        if (v * 100) % tot:
            raise Skip()
        ans = f"{v * 100 // tot}%"
        allm = sum(q[o][0] for o in offs)
        wr = [(f"{num(v * 100 / allm)}%", "DI-WRONG-BASE", f"This divides by all offices' {months[0]} use ({allm}), not by {tgt}'s total."),
              (f"{v}%", "DI-SCALE", f"This reads the count {v} as a percent."),
              (f"{num(q[tgt][1] * 100 / tot)}%", "DI-WRONG-CELL", f"This uses {months[1]} instead of {months[0]}.")]
        stem = f"{stemhead} What percent of {tgt}'s three-month total was used in {months[0]}?"
        sc = f"Part ÷ whole × 100. Part = {v}; whole = {' + '.join(map(str, q[tgt]))} = {tot}."
        wc = f"{ans} is right: {v} ÷ {tot} = {num(v / tot)}, which is {ans}."
    return make(id=iid, **B, competency="Data interpretation", concept="table reading", micro_skill=f"table {kind}", archetype="ANA-DI-TABLE",
                difficulty="medium", est=75, stem=stem, correct=str(ans), wrong=wr,
                terms="A \"row\" runs across (one office). A \"column\" runs down (one month).", shortcut=sc, why_correct=wc, rng=rng)


# Syllogism frames. Categories nest: small ⊂ mid. Each tuple: (small, mid, big?) wording in plural.
CATS = [("encoders", "clerks", "employees"), ("nurses", "health workers", "public servants"), ("mangoes", "fruits", "farm products"),
        ("jeepneys", "public vehicles", "registered vehicles"), ("barangay captains", "elected officials", "public officers"),
        ("memos", "official papers", "records"), ("auditors", "accountants", "licensed workers"), ("tilapia", "fish", "market goods"),
        ("teachers", "school staff", "government workers"), ("tricycles", "motor vehicles", "taxed vehicles"),
        ("judges", "lawyers", "bar members"), ("ferries", "boats", "inspected vessels"), ("libraries", "public buildings", "insured properties"),
        ("seedlings", "plants", "nursery stock"), ("receipts", "documents", "filed items"), ("volunteers", "helpers", "registered persons"),
        ("bridges", "structures", "inspected works"), ("drivers", "workers", "persons with IDs"), ("farmers", "producers", "cooperative members"),
        ("typhoon reports", "bulletins", "public notices")]


PEOPLE = {"encoders", "nurses", "barangay captains", "auditors", "teachers", "judges", "volunteers", "drivers", "farmers"}
SOME_PROP = {"p": ["volunteers", "night-shift workers", "first-time applicants", "choir members", "blood donors", "union members", "scholars", "part-time workers"],
             "t": ["donations", "imported goods", "items on the March list", "rentals", "gifts from the province", "second-hand goods", "items marked for repair", "items in the audit sample"]}
NONE_PROP = {"p": ["late payers", "smokers", "absentees", "rule violators", "job-order hires", "new trainees"],
             "t": ["recalled items", "items marked for disposal", "items under quarantine", "stolen goods", "expired stock", "unregistered items"]}
SYL_FRAMES = {
    "chain": [("C1", "All {s} are {m}. All {m} are {b}. Which conclusion must be true?"),
              ("C2", "Statement 1: All {m} are {b}. Statement 2: All {s} are {m}. Which conclusion follows from both statements?"),
              ("C3", "Assume these are true: every one of the {s} is among the {m}, and every one of the {m} is among the {b}. What can be concluded for certain?")],
    "some": [("S1", "All {s} are {m}. Some {s} are {p}. Which conclusion must be true?"),
             ("S2", "Statement 1: Some {s} are {p}. Statement 2: All {s} are {m}. Which conclusion follows from both statements?"),
             ("S3", "Assume these are true: a few of the {s} are {p}, and all of the {s} are {m}. What can be concluded for certain?")],
    "none": [("N1", "All {s} are {m}. No {m} are {p}. Which conclusion must be true?"),
             ("N2", "Statement 1: No {m} are {p}. Statement 2: All {s} are {m}. Which conclusion follows from both statements?"),
             ("N3", "Assume these are true: none of the {m} are {p}, and every one of the {s} is among the {m}. What can be concluded for certain?")],
}


def syllogism(rng, iid, form=None, frame=None):
    s, m, b = rng.choice(CATS)
    form = form or rng.choice(list(SYL_FRAMES))
    fid, tpl = frame or least_used(rng, "SYL-" + form, SYL_FRAMES[form])
    kind = "p" if s in PEOPLE else "t"
    p = rng.choice((SOME_PROP if form == "some" else NONE_PROP)[kind])
    if p == s or p == m:
        p = (SOME_PROP if form == "some" else NONE_PROP)[kind][0]
    stem = tpl.format(s=s, m=m, b=b, p=p)
    if form == "chain":
        c = f"All {s} are {b}."
        wr = [(f"All {b} are {s}.", "LOG-CONVERSE", f"This flips the statement. Being {b} does not make something one of the {s}."),
              (f"Some {b} are not {m}.", "LOG-COULD-NOT-MUST", "This could be true, but the statements do not say it."),
              (f"No {m} are {s}.", "LOG-OVERSTRONG", f"This contradicts the statements: every one of the {s} is one of the {m}.")]
        sc = f"Draw circles: {s} inside {m}, {m} inside {b}. So {s} sit inside {b}."
    elif form == "some":
        c = f"Some {m} are {p}."
        wr = [(f"All {m} are {p}.", "LOG-OVERSTRONG", f"Only some of the {s} are {p}, so we cannot say all {m} are."),
              (f"All {p} are {s}.", "LOG-CONVERSE", f"This flips the statement about {p}. Some {p} may be outside the group."),
              (f"No {m} are {p}.", "LOG-OVERSTRONG", f"This contradicts the statements: the {s} who are {p} are also {m}.")]
        sc = f"The {s} who are {p} are also {m}. So at least some {m} are {p}."
    else:
        c = f"No {s} are {p}."
        wr = [(f"Some {s} are {p}.", "LOG-OVERSTRONG", f"This contradicts the statements: all {s} are {m}, and no {m} is {p}."),
              (f"No {b} are {p}.", "LOG-COULD-NOT-MUST", f"The statements say nothing about all {b}; some {b} may be outside the {m} group."),
              (f"All {m} are {s}.", "LOG-CONVERSE", "This flips the statement about the two groups.")]
        sc = f"Put the {s} circle inside {m}. The \"{p}\" circle sits outside {m}, so it is outside {s} too."
    it = make(id=iid, **B, competency="Logic", concept="syllogism", micro_skill=f"{form} form", archetype="ANA-SYLLOGISM", difficulty="medium", est=45,
              stem=stem, correct=c, wrong=wr, terms="A conclusion \"must be true\" only if the statements force it. Ignore what you know from real life.",
              shortcut=sc, why_correct=f"\"{c}\" is right. It follows from the two statements with no extra facts.", rng=rng)
    it["_frame"] = f"SYL-{fid}"
    it["_kind"] = "SYL-" + form
    it["_sig"] = f"SYL:{form}:{s}:{p if form != 'chain' else b}"
    return it


# Analogies: (a, b, relation, archetype, [distractor pairs with codes])
ANALOGIES = [
    ("cool", "cold", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("breeze", "gale"), [("cold", "cool", "ANA-REVERSED"), ("ice", "winter", "ANA-SAME-TOPIC"), ("hot", "cold", "ANA-OTHER-RELATION")]),
    ("tired", "exhausted", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("hungry", "starving"), [("exhausted", "tired", "ANA-REVERSED"), ("sleep", "bed", "ANA-SAME-TOPIC"), ("awake", "asleep", "ANA-OTHER-RELATION")]),
    ("pond", "lake", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("hill", "mountain"), [("lake", "pond", "ANA-REVERSED"), ("fish", "water", "ANA-SAME-TOPIC"), ("river", "bridge", "ANA-OTHER-RELATION")]),
    ("begin", "start", "similar meaning", "ANA-ANALOGY-SYN", ("end", "finish"), [("start", "stop", "ANA-OTHER-RELATION"), ("race", "runner", "ANA-SAME-TOPIC"), ("began", "begun", "ANA-SOUND")]),
    ("broom", "sweep", "tool : what it is used for", "ANA-ANALOGY-FUNCTION", ("scissors", "cut"), [("dust", "floor", "ANA-SAME-TOPIC"), ("sweep", "broom", "ANA-REVERSED"), ("brush", "bristle", "ANA-OTHER-RELATION")]),
    ("page", "book", "part : whole", "ANA-ANALOGY-PART", ("brick", "wall"), [("library", "shelf", "ANA-REVERSED"), ("author", "story", "ANA-OTHER-RELATION"), ("ink", "printer", "ANA-SAME-TOPIC")]),
    ("finger", "hand", "part : whole", "ANA-ANALOGY-PART", ("spoke", "wheel"), [("glove", "hand", "ANA-ONE-LINK"), ("arm", "elbow", "ANA-REVERSED"), ("ring", "jewel", "ANA-OTHER-RELATION")]),
    ("timid", "afraid", "similar meaning", "ANA-ANALOGY-SYN", ("happy", "glad"), [("brave", "afraid", "ANA-OTHER-RELATION"), ("tame", "lion", "ANA-SOUND"), ("shy", "crowd", "ANA-SAME-TOPIC")]),
    ("ancient", "old", "similar meaning", "ANA-ANALOGY-SYN", ("rapid", "fast"), [("new", "old", "ANA-OTHER-RELATION"), ("history", "past", "ANA-SAME-TOPIC"), ("antique", "shop", "ANA-OTHER-RELATION")]),
    ("warm", "hot", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("drizzle", "downpour"), [("hot", "warm", "ANA-REVERSED"), ("cold", "ice", "ANA-OTHER-RELATION"), ("sun", "heat", "ANA-SAME-TOPIC")]),
    ("whisper", "shout", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("smile", "laugh"), [("shout", "whisper", "ANA-REVERSED"), ("voice", "throat", "ANA-SAME-TOPIC"), ("quiet", "silent", "ANA-OTHER-RELATION")]),
    ("teacher", "school", "worker : workplace", "ANA-ANALOGY-FUNCTION", ("farmer", "field"), [("student", "teacher", "ANA-OTHER-RELATION"), ("classroom", "chalk", "ANA-SAME-TOPIC"), ("hospital", "nurse", "ANA-REVERSED")]),
    ("pilot", "airplane", "worker : what they operate", "ANA-ANALOGY-FUNCTION", ("captain", "ship"), [("passenger", "bus", "ANA-OTHER-RELATION"), ("sky", "cloud", "ANA-SAME-TOPIC"), ("train", "driver", "ANA-REVERSED")]),
    ("bud", "flower", "early stage : later stage", "ANA-ANALOGY-FORM", ("egg", "chicken"), [("petal", "stem", "ANA-OTHER-RELATION"), ("flower", "bud", "ANA-REVERSED"), ("garden", "soil", "ANA-SAME-TOPIC")]),
    ("caterpillar", "butterfly", "early stage : later stage", "ANA-ANALOGY-FORM", ("tadpole", "frog"), [("bee", "honey", "ANA-OTHER-RELATION"), ("wing", "bird", "ANA-OTHER-RELATION"), ("adult", "child", "ANA-REVERSED")]),
    ("doctor", "diagnosis", "worker : what they produce", "ANA-ANALOGY-FUNCTION", ("architect", "blueprint"), [("patient", "medicine", "ANA-SAME-TOPIC"), ("plan", "engineer", "ANA-REVERSED"), ("nurse", "doctor", "ANA-OTHER-RELATION")]),
    ("rice", "grain", "member : group", "ANA-ANALOGY-PART", ("carrot", "vegetable"), [("bread", "flour", "ANA-OTHER-RELATION"), ("fruit", "mango", "ANA-REVERSED"), ("field", "harvest", "ANA-SAME-TOPIC")]),
    ("hammer", "nail", "tool : what it acts on", "ANA-ANALOGY-FUNCTION", ("key", "lock"), [("saw", "carpenter", "ANA-OTHER-RELATION"), ("screw", "screwdriver", "ANA-REVERSED"), ("wood", "board", "ANA-SAME-TOPIC")]),
    ("drought", "rain", "condition : what it lacks", "ANA-ANALOGY-FORM", ("darkness", "light"), [("flood", "water", "ANA-OTHER-RELATION"), ("cloud", "rain", "ANA-SAME-TOPIC"), ("light", "darkness", "ANA-REVERSED")]),
    ("generous", "stingy", "opposite meaning", "ANA-ANALOGY-SYN", ("humble", "proud"), [("kind", "gentle", "ANA-OTHER-RELATION"), ("gift", "money", "ANA-SAME-TOPIC"), ("giver", "giving", "ANA-SOUND")]),
    ("expand", "shrink", "opposite meaning", "ANA-ANALOGY-SYN", ("rise", "fall"), [("grow", "increase", "ANA-OTHER-RELATION"), ("balloon", "air", "ANA-SAME-TOPIC"), ("expense", "spend", "ANA-SOUND")]),
    ("minute", "hour", "smaller unit : larger unit", "ANA-ANALOGY-PART", ("centimeter", "meter"), [("clock", "time", "ANA-SAME-TOPIC"), ("year", "month", "ANA-REVERSED"), ("second", "fast", "ANA-OTHER-RELATION")]),
    ("author", "novel", "maker : what they make", "ANA-ANALOGY-FUNCTION", ("composer", "song"), [("reader", "book", "ANA-OTHER-RELATION"), ("poem", "poet", "ANA-REVERSED"), ("page", "chapter", "ANA-SAME-TOPIC")]),
    ("lock", "secure", "thing : its purpose", "ANA-ANALOGY-FUNCTION", ("umbrella", "shield"), [("door", "open", "ANA-OTHER-RELATION"), ("key", "metal", "ANA-SAME-TOPIC"), ("protect", "helmet", "ANA-REVERSED")]),
    ("hungry", "eat", "need : action that meets it", "ANA-ANALOGY-FUNCTION", ("tired", "rest"), [("food", "plate", "ANA-SAME-TOPIC"), ("drink", "thirsty", "ANA-REVERSED"), ("hunger", "pain", "ANA-OTHER-RELATION")]),
    ("island", "ocean", "thing : what surrounds it", "ANA-ANALOGY-PART", ("oasis", "desert"), [("beach", "sand", "ANA-OTHER-RELATION"), ("lake", "island", "ANA-REVERSED"), ("boat", "wave", "ANA-SAME-TOPIC")]),
    ("bee", "hive", "animal : home", "ANA-ANALOGY-PART", ("bird", "nest"), [("honey", "bee", "ANA-OTHER-RELATION"), ("den", "bear", "ANA-REVERSED"), ("flower", "garden", "ANA-SAME-TOPIC")]),
    ("cashier", "money", "worker : what they handle", "ANA-ANALOGY-FUNCTION", ("librarian", "books"), [("bank", "vault", "ANA-SAME-TOPIC"), ("receipt", "cashier", "ANA-REVERSED"), ("salary", "work", "ANA-OTHER-RELATION")]),
    ("ice", "water", "solid form : liquid form", "ANA-ANALOGY-FORM", ("candle wax", "melted wax"), [("steam", "ice", "ANA-OTHER-RELATION"), ("water", "ice", "ANA-REVERSED"), ("cold", "freezer", "ANA-SAME-TOPIC")]),
    ("famine", "food", "condition : what it lacks", "ANA-ANALOGY-FORM", ("poverty", "money"), [("feast", "food", "ANA-OTHER-RELATION"), ("harvest", "rice", "ANA-SAME-TOPIC"), ("wealth", "poverty", "ANA-REVERSED")]),
    ("compass", "direction", "tool : what it shows", "ANA-ANALOGY-FUNCTION", ("map", "location"), [("north", "south", "ANA-OTHER-RELATION"), ("hiker", "trail", "ANA-SAME-TOPIC"), ("time", "watch", "ANA-REVERSED")]),
    ("chapter", "book", "part : whole", "ANA-ANALOGY-PART", ("verse", "song"), [("novel", "story", "ANA-OTHER-RELATION"), ("title", "cover", "ANA-SAME-TOPIC"), ("album", "track", "ANA-REVERSED")]),
    ("frown", "displeasure", "sign : what it shows", "ANA-ANALOGY-FORM", ("applause", "approval"), [("smile", "frown", "ANA-OTHER-RELATION"), ("face", "mouth", "ANA-SAME-TOPIC"), ("joy", "laugh", "ANA-REVERSED")]),
]


ANA_FRAMES = [("A1", "{A} : {B} :: ____"), ("A2", "{a} is to {b} as ____."), ("A3", "Which pair shows the same relationship as \"{a} : {b}\"?"),
              ("A4", "Find the pair whose link matches the link between \"{a}\" and \"{b}\".")]


from collections import Counter, defaultdict
FRAME_USE = defaultdict(Counter)  # type -> frame -> uses so far in the bank (build.py keeps it current)


def least_used(rng, kind, frames):
    low = min(FRAME_USE[kind][f[0]] for f in frames)
    return rng.choice([f for f in frames if FRAME_USE[kind][f[0]] == low])


def analogy(rng, iid, frame=None):
    a, b, rel, arch, good, bad = rng.choice(ANALOGIES)
    fid, tpl = frame or least_used(rng, arch, ANA_FRAMES)
    fmt = lambda p: f"{p[0]} : {p[1]}"
    why = {"ANA-SAME-TOPIC": "is about the same topic but not the same link", "ANA-REVERSED": "has the right link but in reverse order",
           "ANA-OTHER-RELATION": "is linked in a different way", "ANA-SOUND": "is linked only by sound or spelling", "ANA-ONE-LINK": "is linked to only one stem word"}
    stem = tpl.format(A=a.upper(), B=b.upper(), a=a.capitalize() if fid == "A2" else a, b=b)
    it = make(id=iid, **B, competency="Word association (analogy)", concept="analogy", micro_skill=rel, archetype=arch, difficulty="medium", est=30,
              stem=stem, correct=fmt(good),
              wrong=[(fmt(p), c, f"\"{fmt(p)}\" {why[c]}. The stem pair is {rel}.") for p, c in [(x[:2], x[2]) for x in bad]],
              terms="\"A : B :: C : D\" means A is to B as C is to D. The two pairs must share the same link.",
              shortcut=f"Make a sentence for the stem: \"{a} is to {b}\" as {rel}. Test each choice in that sentence.",
              why_correct=f"\"{fmt(good)}\" is right. It has the same link, {rel}, in the same order.", rng=rng)
    it["_frame"] = f"ANA-{fid}"
    it["_kind"] = arch
    it["_sig"] = f"ANA:{a}:{b}"
    return it


import assume as _A
OPT = {"I": "Only I", "II": "Only II", "both": "Both I and II", "neither": "Neither I nor II"}


def assumption(rng, iid):
    st, a1, a2, key = rng.choice(_A.ROWS)
    why = {"I": f"Only assumption I is needed. II (\"{a2}\") is not required by the statement.",
           "II": f"Only assumption II is needed. I (\"{a1}\") is not required by the statement.",
           "both": "Both assumptions are needed for the plan to make sense.", "neither": "Neither assumption is needed; both go beyond the statement."}
    code = {("I", "II"): "LOG-IRRELEVANT", ("I", "both"): "LOG-COULD-NOT-MUST", ("I", "neither"): "LOG-MISSED-NEEDED",
            ("II", "I"): "LOG-IRRELEVANT", ("II", "both"): "LOG-COULD-NOT-MUST", ("II", "neither"): "LOG-MISSED-NEEDED",
            ("both", "I"): "LOG-MISSED-NEEDED", ("both", "II"): "LOG-MISSED-NEEDED", ("both", "neither"): "LOG-MISSED-NEEDED",
            ("neither", "I"): "LOG-COULD-NOT-MUST", ("neither", "II"): "LOG-COULD-NOT-MUST", ("neither", "both"): "LOG-COULD-NOT-MUST"}
    expl = {"LOG-IRRELEVANT": "picks the assumption the statement does not need and drops the one it does",
            "LOG-COULD-NOT-MUST": "accepts an assumption that is merely plausible, not required",
            "LOG-MISSED-NEEDED": "rejects an assumption the statement does need"}
    wr = [(OPT[k], code[(key, k)], f"\"{OPT[k]}\" {expl[code[(key, k)]]}.") for k in OPT if k != key]
    it = make(id=iid, **B, competency="Assumptions and conclusions", concept="assumption", micro_skill="spot an assumption the statement needs",
              archetype="ANA-ASSUME-I-II", difficulty="medium", est=60,
              stem=f"Statement: {st}\nAssumption I: {a1}\nAssumption II: {a2}\nWhich assumption is implicit in the statement?", correct=OPT[key], wrong=wr,
              terms="An \"implicit assumption\" is something the speaker must take as true for the statement to make sense, even if it is not said.",
              shortcut="Negate each assumption. If the statement stops making sense, the assumption is needed.", why_correct=f"\"{OPT[key]}\" is right. {why[key]}", rng=rng)
    it["_sig"] = "ASM:" + st
    return it


TEMPLATES = [letter_series, code_shift, ranking, di_table, syllogism, analogy, assumption]
# per-batch minimums (CoS: assumption/conclusion at least 15) and caps (take room from over-full topics)
MINS = {"assumption": 2}
CAPS = {"letter series": 5, "letter coding": 5, "table reading": 6, "ordering": 4, "syllogism": 5, "analogy": 4, "assumption": 2}
