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
    order = n[:]  # tallest/fastest... first
    rng.shuffle(order)
    trait = rng.choice([("finished the report earlier than", "finished first", "earliest"), ("has served longer than", "has served the longest", "longest"),
                        ("scored higher than", "got the highest score", "highest"), ("lives nearer the office than", "lives nearest", "nearest")])
    a, b, c, d = order
    clues = [f"{a} {trait[0]} {b}.", f"{c} {trait[0]} {a}.", f"{b} {trait[0]} {d}."]
    # true order: c > a > b > d
    true = [c, a, b, d]
    rng.shuffle(clues)
    ask = rng.choice(["second", "third"])
    pos = 1 if ask == "second" else 2
    ans = true[pos]
    others = [x for x in true if x != ans]
    reasons = {c: ("ANA-ONE-LINK", f"{c} is ahead of everyone; {c} is first."),
               a: ("ANA-ONE-LINK", f"{a} is second, not {ask}."),
               b: ("ANA-ONE-LINK", f"{b} is third, not {ask}."),
               d: ("ANA-ONE-LINK", f"{d} is behind everyone; {d} is last.")}
    return make(id=iid, **B, competency="Logic", concept="ordering", micro_skill="chain comparison clues into one order", archetype="ANA-CONCLUSION",
                difficulty="medium", est=60,
                stem=f"Four staff members are compared. {' '.join(clues)} Who is {ask} in the order (from the one who {trait[1]})?", correct=ans,
                wrong=[(o, "LOG-COULD-NOT-MUST", reasons[o][1]) for o in others],
                terms="An \"ordering\" item gives pairs. Join the pairs into one line.",
                shortcut=f"Start from the clue that names someone nobody beats. Line: {' → '.join(true)}.",
                why_correct=f"{ans} is right. The clues give {' → '.join(true)}, so {ans} is {ask}.", rng=rng)


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


def syllogism(rng, iid):
    s, m, b = rng.choice(CATS)
    form = rng.choice(["chain", "some", "none"])
    if form == "chain":
        stem = f"All {s} are {m}. All {m} are {b}. Which conclusion must be true?"
        c = f"All {s} are {b}."
        wr = [(f"All {b} are {s}.", "LOG-CONVERSE", f"This flips the statement. Being {b} does not make something one of the {s}."),
              (f"Some {b} are not {m}.", "LOG-COULD-NOT-MUST", f"This could be true, but the statements do not say it."),
              (f"No {m} are {s}.", "LOG-OVERSTRONG", f"This contradicts the statements: every one of the {s} is one of the {m}.")]
        sc = f"Draw circles: {s} inside {m}, {m} inside {b}. So {s} sit inside {b}."
    elif form == "some":
        stem = f"All {s} are {m}. Some {s} are volunteers. Which conclusion must be true?"
        c = f"Some {m} are volunteers."
        wr = [(f"All {m} are volunteers.", "LOG-OVERSTRONG", f"Only some of the {s} are volunteers, so we cannot say all {m} are."),
              (f"All volunteers are {s}.", "LOG-CONVERSE", "This flips the second statement. Some volunteers may be outside the group."),
              (f"No {m} are volunteers.", "LOG-OVERSTRONG", f"This contradicts the statements: the volunteer {s} are also {m}.")]
        sc = f"The {s} who are volunteers are also {m}. So at least some {m} are volunteers."
    else:
        stem = f"All {s} are {m}. No {m} are late payers. Which conclusion must be true?"
        c = f"No {s} are late payers."
        wr = [(f"Some {s} are late payers.", "LOG-OVERSTRONG", f"This contradicts the statements: all {s} are {m}, and no {m} is a late payer."),
              (f"No late payers are {b}.", "LOG-COULD-NOT-MUST", f"The statements say nothing about all {b}; some {b} may be outside the {m} group."),
              (f"All {m} are {s}.", "LOG-CONVERSE", "This flips the first statement.")]
        sc = f"Put the {s} circle inside {m}. The late payers circle sits outside {m}, so it is outside {s} too."
    return make(id=iid, **B, competency="Logic", concept="syllogism", micro_skill=f"{form} form", archetype="ANA-SYLLOGISM", difficulty="medium", est=45,
                stem=stem, correct=c, wrong=wr, terms="A conclusion \"must be true\" only if the statements force it. Ignore what you know from real life.",
                shortcut=sc, why_correct=f"\"{c}\" is right. It follows from the two statements with no extra facts.", rng=rng)


# Analogies: (a, b, relation, archetype, [distractor pairs with codes])
ANALOGIES = [
    ("pen", "write", "tool : what it is used for", "ANA-ANALOGY-FUNCTION", ("scissors", "cut"), [("ink", "paper", "ANA-SAME-TOPIC"), ("read", "book", "ANA-REVERSED"), ("knife", "sharp", "ANA-OTHER-RELATION")]),
    ("thermometer", "temperature", "tool : what it measures", "ANA-ANALOGY-FUNCTION", ("scale", "weight"), [("clock", "alarm", "ANA-OTHER-RELATION"), ("heat", "fever", "ANA-SAME-TOPIC"), ("distance", "ruler", "ANA-REVERSED")]),
    ("page", "book", "part : whole", "ANA-ANALOGY-PART", ("brick", "wall"), [("library", "shelf", "ANA-REVERSED"), ("author", "story", "ANA-OTHER-RELATION"), ("ink", "printer", "ANA-SAME-TOPIC")]),
    ("finger", "hand", "part : whole", "ANA-ANALOGY-PART", ("spoke", "wheel"), [("glove", "hand", "ANA-ONE-LINK"), ("arm", "elbow", "ANA-REVERSED"), ("ring", "jewel", "ANA-OTHER-RELATION")]),
    ("timid", "afraid", "similar meaning", "ANA-ANALOGY-SYN", ("happy", "glad"), [("brave", "afraid", "ANA-OTHER-RELATION"), ("tame", "lion", "ANA-SOUND"), ("shy", "crowd", "ANA-SAME-TOPIC")]),
    ("ancient", "old", "similar meaning", "ANA-ANALOGY-SYN", ("rapid", "fast"), [("new", "old", "ANA-OTHER-RELATION"), ("history", "past", "ANA-SAME-TOPIC"), ("antique", "shop", "ANA-OTHER-RELATION")]),
    ("warm", "hot", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("drizzle", "downpour"), [("hot", "warm", "ANA-REVERSED"), ("cold", "ice", "ANA-OTHER-RELATION"), ("sun", "heat", "ANA-SAME-TOPIC")]),
    ("whisper", "shout", "lesser : greater degree", "ANA-ANALOGY-DEGREE", ("smile", "laugh"), [("shout", "whisper", "ANA-REVERSED"), ("voice", "throat", "ANA-SAME-TOPIC"), ("quiet", "silent", "ANA-OTHER-RELATION")]),
    ("teacher", "school", "worker : workplace", "ANA-ANALOGY-FUNCTION", ("farmer", "field"), [("student", "teacher", "ANA-OTHER-RELATION"), ("classroom", "chalk", "ANA-SAME-TOPIC"), ("hospital", "nurse", "ANA-REVERSED")]),
    ("pilot", "airplane", "worker : what they operate", "ANA-ANALOGY-FUNCTION", ("captain", "ship"), [("passenger", "bus", "ANA-OTHER-RELATION"), ("sky", "cloud", "ANA-SAME-TOPIC"), ("train", "driver", "ANA-REVERSED")]),
    ("seed", "tree", "early stage : later stage", "ANA-ANALOGY-FORM", ("egg", "chicken"), [("leaf", "branch", "ANA-OTHER-RELATION"), ("fruit", "seed", "ANA-REVERSED"), ("soil", "water", "ANA-SAME-TOPIC")]),
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


def analogy(rng, iid):
    a, b, rel, arch, good, bad = rng.choice(ANALOGIES)
    fmt = lambda p: f"{p[0]} : {p[1]}"
    why = {"ANA-SAME-TOPIC": "is about the same topic but not the same link", "ANA-REVERSED": "has the right link but in reverse order",
           "ANA-OTHER-RELATION": "is linked in a different way", "ANA-SOUND": "is linked only by sound or spelling", "ANA-ONE-LINK": "is linked to only one stem word"}
    return make(id=iid, **B, competency="Word association (analogy)", concept="analogy", micro_skill=rel, archetype=arch, difficulty="medium", est=30,
                stem=f"{a.upper()} : {b.upper()} :: ____", correct=fmt(good),
                wrong=[(fmt(p), c, f"\"{fmt(p)}\" {why[c]}. The stem pair is {rel}.") for p, c in [(x[:2], x[2]) for x in bad]],
                terms="\"A : B :: C : D\" means A is to B as C is to D. The two pairs must share the same link.",
                shortcut=f"Make a sentence for the stem: \"{a} is to {b}\" as {rel}. Test each choice in that sentence.",
                why_correct=f"\"{fmt(good)}\" is right. It has the same link, {rel}, in the same order.", rng=rng)


TEMPLATES = [letter_series, code_shift, ranking, di_table, di_table, syllogism, analogy]
