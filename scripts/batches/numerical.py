"""Numerical Ability templates. Keys computed in code; each distractor is a coded mistake."""
from fractions import Fraction as F
from common import make, peso, num, Skip, FIRST, PLACES, OFFICES

B = dict(track="both", domain="numerical")


def pct_change(rng, iid):
    p = rng.choice([150, 200, 240, 250, 320, 400, 480, 500, 600, 750, 800, 1200])
    up = rng.choice([10, 20, 25, 30, 40, 50])
    dn = rng.choice([10, 20, 25, 30, 40, 50])
    mid = p * (100 + up) / 100
    fin = mid * (100 - dn) / 100
    add = p * (100 + up - dn) / 100
    extra = fin * (100 + up) / 100
    if len({fin, add, mid, extra}) < 4 or fin != int(fin) or extra != round(extra, 2):
        raise Skip()
    item = rng.choice(["a sack of rice", "a box of bond paper", "a gallon of paint", "a bag of cement", "a set of school uniforms", "a tank of LPG"])
    who = rng.choice(["A hardware store", "A cooperative store", "A sari-sari store", "A supplier", "A market stall"])
    stem = f"{who} sold {item} for {peso(p)}. It raised the price by {up}%. Later, it lowered the new price by {dn}%. What is the final price?"
    return make(id=iid, **B, competency="Word problems", concept="successive percent change", micro_skill="chain a percent increase and a percent decrease",
                archetype="NUM-WP-PCT-CHANGE", difficulty="medium", est=90, stem=stem, correct=peso(fin),
                wrong=[(peso(add), "NUM-PCT-ADD", f"{peso(add)} adds and subtracts the percents first ({up}% − {dn}%). The second change is taken from the new price, not the old one."),
                       (peso(mid), "NUM-PARTIAL", f"{peso(mid)} is only the price after the raise. It stops before the cut."),
                       (peso(extra), "NUM-EXTRA-STEP", f"{peso(extra)} applies the {up}% raise again at the end. That is one step too many.")],
                terms="\"Percent\" means \"out of 100\". A raise or a cut of a percent is always taken from the price at that moment.",
                shortcut=f"Do one change at a time. {peso(p)} up {up}% is {peso(p)} + {peso(p * up / 100)} = {peso(mid)}. Then {dn}% of {peso(mid)} is {peso(mid * dn / 100)}, so {peso(mid)} − {peso(mid * dn / 100)} = {peso(fin)}.",
                why_correct=f"{peso(fin)} is right. Check: {num(p)} × {num((100 + up) / 100)} = {num(mid)}, and {num(mid)} × {num((100 - dn) / 100)} = {num(fin)}.", rng=rng)


def seq_diff(rng, iid):
    a = rng.randint(1, 15)
    d = rng.randint(1, 6)
    k = rng.randint(1, 3)
    s = [a]
    gaps = [d + k * i for i in range(5)]
    for g in gaps[:4]:
        s.append(s[-1] + g)
    ans = s[-1] + gaps[4]
    w1, w2, w3 = s[-1] + gaps[3], s[-1] + d, ans + k
    if len({ans, w1, w2, w3}) < 4:
        raise Skip()
    lead = rng.choice(["What number comes next in the series?", "Find the next number in the series.", "Which number should come next?"])
    gtxt = ", ".join(f"+{g}" for g in gaps[:4])
    return make(id=iid, **B, competency="Number sequence", concept="growing differences", micro_skill="extend a series whose jumps grow by a fixed amount",
                archetype="NUM-SEQ-DIFF", difficulty="medium", est=45, stem=f"{lead}  {', '.join(map(str, s))}, ___", correct=str(ans),
                wrong=[(str(w1), "NUM-PARTIAL", f"{w1} repeats the last jump, +{gaps[3]}. The jumps keep growing by {k}."),
                       (str(w2), "NUM-SEQ-OTHER-RULE", f"{w2} adds only the first jump, +{d}, as if the jump never changed."),
                       (str(w3), "NUM-OFF-BY-ONE", f"{w3} uses a jump of +{gaps[4] + k}, one step too far in the growing jumps.")],
                terms="A \"series\" is a list of numbers that follows one rule. The \"jump\" is how much you add to get the next number.",
                shortcut=f"Write the jumps under the list: {gtxt}. Each jump is {k} more than the one before. So the next jump is +{gaps[4]}.",
                why_correct=f"{ans} is right: {s[-1]} + {gaps[4]} = {ans}.", rng=rng)


def seq_mult(rng, iid):
    a = rng.randint(1, 6)
    m = rng.choice([2, 3])
    c = rng.choice([-2, -1, 1, 2, 3])
    s = [a]
    for _ in range(4):
        s.append(s[-1] * m + c)
    ans = s[-1] * m + c
    w1, w2 = s[-1] * m, s[-1] + (s[-1] - s[-2])
    w3 = ans + c if c else ans + 1
    if len({ans, w1, w2, w3}) < 4 or s[-1] > 400:
        raise Skip()
    op = f"+ {c}" if c > 0 else f"− {-c}"
    return make(id=iid, **B, competency="Number sequence", concept="multiply then add", micro_skill="find a ×k then ±c rule",
                archetype="NUM-SEQ-MULT", difficulty="hard", est=50, stem=f"What number comes next?  {', '.join(map(str, s))}, ___", correct=str(ans),
                wrong=[(str(w1), "NUM-PARTIAL", f"{w1} multiplies by {m} but forgets the {op} step."),
                       (str(w2), "NUM-SEQ-OTHER-RULE", f"{w2} repeats the last difference ({s[-1] - s[-2]}). The jumps are not the same each time."),
                       (str(w3), "NUM-EXTRA-STEP", f"{w3} does the {op} step twice.")],
                terms="A \"rule\" is the same steps done to each number to get the next one.",
                shortcut=f"Test \"times {m}, then {op}\" on the first numbers: {s[0]} × {m} {op} = {s[1]}; {s[1]} × {m} {op} = {s[2]}. It works, so use it on {s[-1]}.",
                why_correct=f"{ans} is right: {s[-1]} × {m} = {s[-1] * m}, then {op} gives {ans}.", rng=rng)


def ratio(rng, iid):
    a, b = rng.choice([(2, 3), (3, 4), (4, 5), (2, 5), (3, 5), (5, 7), (1, 3), (3, 7)])
    unit = rng.choice([500, 1000, 1200, 1500, 2000, 2500, 3000])
    total = (a + b) * unit
    x, y = rng.sample(FIRST, 2)
    thing = rng.choice(["prize money", "cleanup fund", "harvest income", "allowance fund", "commission"])
    stem = rng.choice([f"{x} and {y} will share {peso(total)} of {thing} in the ratio {a} : {b}. How much is {y}'s share?",
                       f"A {peso(total)} {thing} is divided between {x} and {y} in the ratio {a} : {b}. What is {y}'s share?"])
    ans, other, part, wb = b * unit, a * unit, unit, total / b
    if len({ans, other, part, wb}) < 4:
        raise Skip()
    return make(id=iid, **B, competency="Word problems", concept="ratio", micro_skill="split a total in a ratio", archetype="NUM-WP-RATIO",
                difficulty="medium", est=75, stem=stem, correct=peso(ans),
                wrong=[(peso(other), "NUM-OTHER-SHARE", f"{peso(other)} is {x}'s share ({a} parts). The question asks for {y}."),
                       (peso(part), "NUM-PARTIAL", f"{peso(part)} is one part. It stops before multiplying by {b}."),
                       (peso(wb), "NUM-WRONG-BASE", f"{peso(wb)} divides the total by {b} alone, not by all {a + b} parts.")],
                terms=f"A ratio of {a} : {b} means for every {a} pesos one person gets, the other gets {b} pesos.",
                shortcut=f"Add the ratio numbers to get equal parts: {a} + {b} = {a + b}. One part = {peso(total)} ÷ {a + b} = {peso(unit)}. Then multiply by the parts you need.",
                why_correct=f"{peso(ans)} is right: {b} × {peso(unit)} = {peso(ans)}. Check: {peso(other)} + {peso(ans)} = {peso(total)}.", rng=rng)


def work_rate(rng, iid):
    a, b = rng.choice([(6, 3), (4, 12), (10, 15), (6, 12), (12, 4), (20, 30), (8, 24), (9, 18), (15, 10)])
    t = F(a * b, a + b)
    if t.denominator != 1:
        raise Skip()
    t = int(t)
    x, y = rng.sample(FIRST, 2)
    job = rng.choice(["encode a box of survey forms", "paint a classroom", "sort a sack of mail", "inventory a supply room", "clean the plaza"])
    avg = F(a + b, 2)
    fmt = lambda h: f"{num(float(h))} hours" if h != 1 else "1 hour"
    if len({t, a + b, avg, F(1, t)}) < 4:
        raise Skip()
    return make(id=iid, **B, competency="Word problems", concept="work rate", micro_skill="add work rates", archetype="NUM-WP-RATE", difficulty="medium",
                est=90, stem=f"{x} can {job} in {a} hours. {y} can do the same job in {b} hours. Working together, how long will they take?",
                correct=fmt(t),
                wrong=[(fmt(a + b), "NUM-OP-SWAP", f"{fmt(a + b)} adds the two times. Add the work done per hour, not the hours."),
                       (fmt(avg), "NUM-WRONG-BASE", f"{fmt(avg)} is the average of the two times. Together they must be faster than the faster person alone."),
                       (f"{num(60 / t)} minutes" if 60 % t == 0 else fmt(F(1, t) * 60), "NUM-PARTIAL", f"This reads the combined rate (1/{t} of the job per hour) as a time. It stops before turning the rate into hours.")],
                terms="A \"rate\" is how much of the job gets done in one hour.",
                shortcut=f"Per hour, {x} does 1/{a} and {y} does 1/{b}. Together: 1/{a} + 1/{b} = 1/{t}. So the whole job takes {t} hours.",
                why_correct=f"{fmt(t)} is right. Check: in {t} hours, {x} does {t}/{a} and {y} does {t}/{b}; together that is 1 whole job.", rng=rng)


def average_join(rng, iid):
    n = rng.randint(4, 9)
    avg = rng.randint(20, 45)
    new_avg = avg + rng.randint(1, 4)
    new = new_avg * (n + 1) - avg * n
    group = rng.choice(["staff members", "barangay health workers", "clerks", "teachers", "drivers"])
    what = rng.choice(["age", "years of service"])
    if what == "years of service":
        avg, new_avg = avg // 3 + 2, avg // 3 + 2 + (new_avg - avg)
        new = new_avg * (n + 1) - avg * n
    unit = "years"
    tot = avg * n + new
    w1 = round(avg + (new - avg) / n, 2)
    w2 = F(avg + new, 2)
    if len({new_avg, w1, float(w2), tot}) < 4 or new <= 0:
        raise Skip()
    off = rng.choice(OFFICES)
    return make(id=iid, **B, competency="Word problems", concept="average", micro_skill="new average after one value joins", archetype="NUM-WP-AVERAGE",
                difficulty="medium", est=60,
                stem=f"The average {what} of the {n} {group} in the {off} is {avg} {unit}. One more person, with {new} {unit}, joins them. What is the new average {what}?",
                correct=f"{new_avg} {unit}",
                wrong=[(f"{num(w1)} {unit}", "NUM-OFF-BY-ONE", f"This shares the extra {new - avg} {unit} among {n} people. After the new person joins there are {n + 1}."),
                       (f"{num(float(w2))} {unit}", "NUM-WRONG-BASE", f"This averages {avg} and {new} only, treating the {n} old members as one person."),
                       (f"{tot} {unit}", "NUM-PARTIAL", f"This is the total of all {n + 1} values. It stops before dividing by {n + 1}.")],
                terms="\"Average\" means share equally.",
                shortcut=f"The new person is {new} − {avg} = {new - avg} above the old average. Share that among all {n + 1} people: {new - avg} ÷ {n + 1} = {new_avg - avg}. Add it: {avg} + {new_avg - avg} = {new_avg}.",
                why_correct=f"{new_avg} {unit} is right. Long way: {n} × {avg} = {avg * n}; + {new} = {tot}; ÷ {n + 1} = {new_avg}.", rng=rng)


def simple_interest(rng, iid):
    P = rng.choice([10000, 12000, 15000, 18000, 20000, 24000, 25000, 30000, 40000, 50000])
    r = rng.choice([3, 4, 5, 6, 8, 10, 12])
    yrs, mo = rng.choice([(1, 6), (2, 6), (3, 6), (2, 0), (3, 0), (1, 0), (4, 6)])
    t = yrs + mo / 12
    I = P * r * t / 100
    if I != int(I):
        raise Skip()
    tt = f"{yrs} year{'s' if yrs > 1 else ''}" + (f" and {mo} months" if mo else "")
    wrong = [(peso(P + I), "NUM-EXTRA-STEP", f"{peso(P + I)} is the loan plus interest. The question asks for the interest only.")]
    if mo:
        wrong += [(peso(P * r * yrs / 100), "NUM-PARTIAL", "This counts only the whole years and leaves out the months."),
                  (peso(P * r * (yrs + mo / 10) / 100), "NUM-UNIT", f"This uses {yrs}.{mo} years. {mo} months is {num(mo / 12)} of a year, not 0.{mo}.")]
    else:
        wrong += [(peso(P * r / 100), "NUM-PARTIAL", "This is one year's interest. It stops before multiplying by the years."),
                  (peso(P * r * t / 10), "NUM-DECIMAL", "This slips the decimal point: it uses r as a tenth instead of a hundredth.")]
    who = rng.choice(["A cooperative member", "A teacher", "A farmer", "A vendor", "A government employee"])
    return make(id=iid, **B, competency="Word problems", concept="simple interest", micro_skill="interest = principal × rate × time",
                archetype="NUM-WP-PCT-CHANGE", difficulty="medium", est=75,
                stem=f"{who} borrows {peso(P)} at {r}% simple interest per year. How much interest is due after {tt}?", correct=peso(I), wrong=wrong,
                terms=f"\"Simple interest\" is the extra money paid for borrowing, the same amount each year. {r}% per year means ₱{r} for every ₱100 each year.",
                shortcut=f"Find one year first: {r}% of {peso(P)} = {peso(P * r / 100)}. Time is {num(t)} years. Multiply: {num(t)} × {peso(P * r / 100)} = {peso(I)}.",
                why_correct=f"{peso(I)} is right. Check: {num(P)} × {num(r / 100)} × {num(t)} = {num(I)}.", rng=rng)


def age(rng, iid):
    s = rng.randint(5, 16)
    m = rng.choice([3, 4, 5])
    k = rng.choice([2, 3])
    # parent = m*s now; in y years parent = k*(child)
    # m s + y = k (s + y) -> y = (m - k) s / (k - 1)
    y = F((m - k) * s, k - 1)
    if m <= k or y.denominator != 1 or not 2 <= y <= 30:
        raise Skip()
    y = int(y)
    P = m * s
    x = rng.choice(FIRST)
    rel = rng.choice(["son", "daughter", "nephew", "niece"])
    times = {2: "twice", 3: "three times"}[k]
    if len({P, s, s + y, P + y}) < 4:
        raise Skip()
    return make(id=iid, **B, competency="Word problems", concept="age problem", micro_skill="set up now-and-later ages", archetype="NUM-WP-ALGEBRA",
                difficulty="hard", est=90, stem=f"{x} is {m} times as old as {('her' if rng.random() < 0.5 else 'his')} {rel}. In {y} years, {x} will be {times} as old as the {rel}. How old is {x} now?",
                correct=str(P),
                wrong=[(str(s), "NUM-OTHER-SHARE", f"{s} is the {rel}'s age now, not {x}'s."),
                       (str(s + y), "NUM-OTHER-SHARE", f"{s + y} is the {rel}'s age {y} years from now."),
                       (str(P + y), "NUM-EXTRA-STEP", f"{P + y} is {x}'s age {y} years from now, not today.")],
                terms=f"\"{m} times as old\" means the age is the younger person's age multiplied by {m}.",
                shortcut=f"Try the choices. If {x} is {P}, the {rel} is {s}. In {y} years: {P + y} and {s + y}. {P + y} = {k} × {s + y}, so it works.",
                why_correct=f"{P} is right. Algebra: {rel} = s, {x} = {m}s; {m}s + {y} = {k}(s + {y}) gives s = {s}, so {x} = {P}.", rng=rng)


def discount(rng, iid):
    p = rng.choice([400, 480, 560, 640, 800, 960, 1200, 1500, 1800, 2400])
    d = rng.choice([10, 15, 20, 25, 30, 35, 40])
    sale = p * (100 - d) / 100
    if sale != int(sale):
        raise Skip()
    item = rng.choice(["pair of school shoes", "electric fan", "rice cooker", "office chair", "backpack", "umbrella set"])
    return make(id=iid, **B, competency="Word problems", concept="discount", micro_skill="price after a percent discount", archetype="NUM-WP-PCT-CHANGE",
                difficulty="easy", est=45, stem=f"A {item} is priced at {peso(p)}. It is sold at {d}% off. How much does a buyer pay?", correct=peso(sale),
                wrong=[(peso(p * d / 100), "NUM-PARTIAL", f"{peso(p * d / 100)} is the discount itself. The buyer pays the price minus this amount."),
                       (peso(p - d), "NUM-WRONG-BASE", f"{peso(p - d)} subtracts {d} pesos, not {d}% of the price."),
                       (peso(p * (100 + d) / 100), "NUM-OP-SWAP", f"{peso(p * (100 + d) / 100)} adds {d}% instead of taking it off.")],
                terms=f"\"{d}% off\" means {d} pesos less for every 100 pesos of the price.",
                shortcut=f"Pay {100 - d}% of the price: {peso(p)} × {num((100 - d) / 100)} = {peso(sale)}.",
                why_correct=f"{peso(sale)} is right. Check: discount {peso(p * d / 100)}; {peso(p)} − {peso(p * d / 100)} = {peso(sale)}.", rng=rng)


def order_ops(rng, iid):
    a, b, c, d = rng.randint(2, 20), rng.randint(2, 9), rng.randint(2, 9), rng.randint(1, 12)
    ans = a + b * c - d
    ltr = (a + b) * c - d
    w2 = a + b * (c - d)
    w3 = a + b + c - d
    if len({ans, ltr, w2, w3}) < 4:
        raise Skip()
    return make(id=iid, **B, competency="Basic operations", concept="order of operations", micro_skill="multiply before adding and subtracting",
                archetype="NUM-OPS-ORDER", difficulty="easy", est=35, stem=f"What is the value of {a} + {b} × {c} − {d}?", correct=str(ans),
                wrong=[(str(ltr), "NUM-ORDER-OPS", f"{ltr} works left to right: ({a} + {b}) × {c}. Multiplication comes first."),
                       (str(w2), "NUM-ORDER-OPS", f"{w2} subtracts {d} from {c} before multiplying, which the expression does not say."),
                       (str(w3), "NUM-OP-SWAP", f"{w3} adds {b} and {c} instead of multiplying them.")],
                terms="\"Order of operations\" is the rule for which step to do first: multiply and divide before you add and subtract.",
                shortcut=f"Circle the × first: {b} × {c} = {b * c}. Then go left to right: {a} + {b * c} − {d}.",
                why_correct=f"{ans} is right: {a} + {b * c} = {a + b * c}, and {a + b * c} − {d} = {ans}.", rng=rng)


def fraction_rest(rng, iid):
    tot = rng.choice([120, 180, 240, 360, 480, 600, 720, 900])
    f1 = rng.choice([F(1, 3), F(1, 4), F(2, 5), F(1, 6), F(3, 8)])
    f2 = rng.choice([F(1, 2), F(1, 3), F(1, 4), F(2, 3)])
    used1 = tot * f1
    rest = tot - used1
    used2 = rest * f2
    left = rest - used2
    if any(v.denominator != 1 for v in (used1, used2, left)):
        raise Skip()
    w1 = tot - used1 - tot * f2
    if len({left, rest, used2, w1}) < 4 or w1 <= 0:
        raise Skip()
    it = rng.choice(["sacks of relief rice", "face masks", "seedlings", "notebooks", "liters of fuel"])
    return make(id=iid, **B, competency="Word problems", concept="fraction of the remainder", micro_skill="take a fraction of what is left",
                archetype="NUM-FRAC-DEC", difficulty="hard", est=75,
                stem=f"A barangay had {tot} {it}. It gave out {f1} of them on Monday and {f2} of the remaining {it} on Tuesday. How many are left?",
                correct=str(int(left)),
                wrong=[(str(int(w1)), "NUM-WRONG-BASE", f"{int(w1)} takes {f2} of the original {tot}. Tuesday's share is {f2} of what was left after Monday."),
                       (str(int(rest)), "NUM-PARTIAL", f"{int(rest)} is what was left after Monday only."),
                       (str(int(used2)), "NUM-PARTIAL", f"{int(used2)} is how many were given on Tuesday, not how many are left.")],
                terms="A \"fraction of the remaining\" is a part of what is left, not of the starting amount.",
                shortcut=f"Go day by day. Monday: {f1} of {tot} = {int(used1)}, so {int(rest)} left. Tuesday: {f2} of {int(rest)} = {int(used2)}, so {int(rest)} − {int(used2)} = {int(left)} left.",
                why_correct=f"{int(left)} is right. Check: {int(used1)} + {int(used2)} + {int(left)} = {tot}.", rng=rng)


def rect(rng, iid):
    L, W = rng.randint(8, 40), rng.randint(3, 20)
    if L == W:
        raise Skip()
    cost = rng.choice([25, 40, 50, 75, 120, 150])
    per = 2 * (L + W)
    what = rng.choice(["fence", "edging", "lace border", "chain-link fence"])
    lot = rng.choice(["vegetable garden", "school lot", "basketball court", "parking area", "drying yard"])
    return make(id=iid, **B, competency="Word problems", concept="perimeter and cost", micro_skill="find perimeter, then multiply by cost per meter",
                archetype="NUM-WP-GEOM", difficulty="medium", est=75,
                stem=f"A rectangular {lot} is {L} m long and {W} m wide. A {what} costs {peso(cost)} per meter. How much will it cost to put the {what} around the whole {lot}?",
                correct=peso(per * cost),
                wrong=[(peso(L * W * cost), "NUM-WRONG-BASE", f"This uses the area ({L * W} square meters). Going around uses the perimeter."),
                       (peso((L + W) * cost), "NUM-PARTIAL", f"This uses only one length and one width ({L + W} m). A rectangle has two of each."),
                       (peso(per), "NUM-PARTIAL", f"{peso(per)} is just the perimeter in meters written as pesos. It stops before multiplying by {peso(cost)}.")],
                terms="\"Perimeter\" is the distance around a shape. For a rectangle it is 2 × (length + width).",
                shortcut=f"Around = 2 × ({L} + {W}) = {per} m. Cost = {per} × {peso(cost)}.",
                why_correct=f"{peso(per * cost)} is right: {per} m × {peso(cost)} = {peso(per * cost)}.", rng=rng)


TEMPLATES = [pct_change, seq_diff, seq_mult, ratio, work_rate, average_join, simple_interest, age, discount, order_ops, fraction_rest, rect]
