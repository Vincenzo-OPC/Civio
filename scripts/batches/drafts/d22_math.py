"""B1 subprofessional math (60): fractions, ratios, basic algebra, non-percent word problems. Keys computed here;
solver_2026_10_22.py recomputes each from the stem numbers through the item's recipe (a separate implementation)."""
from fractions import Fraction as F
from math import ceil
from d22_common import mk, peso, num, frac

T, D = "subprofessional", "numerical"


def base(n, comp, concept, skill, arch, diff, est, **kw):
    return dict(id=f"CIVIO-D1022-SPMATH-{n:04d}", track=T, domain=D, competency=comp, concept=concept, micro_skill=skill,
                archetype=arch, difficulty=diff, est=est, **kw)


ITEMS = []
n = 0


def add(**kw):
    ITEMS.append(mk(**kw))


def nxt():
    global n
    n += 1
    return n


# ---------- Fractions ----------
for who, tot, a, b, unit, act1, act2 in [
        ("Rhea", 120, F(1, 4), F(2, 3), "permit forms", "checks", "encodes"),
        ("The records unit", 96, F(3, 8), F(1, 4), "old folders", "scans", "labels")]:
    first = tot * a; rest = tot - first; second = rest * b; left = rest - second
    s = (f"{who} has {tot} {unit}. In the morning {('she' if who == 'Rhea' else 'it')} {act1} {a} of them, and in the afternoon "
         f"{('she' if who == 'Rhea' else 'it')} {act2} {b} of the remaining {unit}. How many {unit} are still untouched at the end of the day?")
    add(**base(nxt(), "Fractions", "fraction of a remainder", "take a fraction of what is left, not of the original", "NUM-FRAC-DEC", "medium", 45),
        stem=s, correct=num(left),
        wrong=[(num(tot - first - tot * b), "NUM-WRONG-BASE", f"This takes {b} of all {tot}, but the afternoon fraction applies only to the {num(rest)} left after the morning."),
               (num(rest), "NUM-PARTIAL", f"{num(rest)} is what remains after the morning only; the afternoon work still has to come off."),
               (num(second), "NUM-OTHER-SHARE", f"{num(second)} is how many were handled in the afternoon, not how many are untouched.")],
        terms="\"Of the remaining\" means the second fraction is taken of what is left, not of the starting total.",
        shortcut=f"Multiply the leftover fractions: {tot} × {1 - a} × {1 - b}.",
        why_correct=f"Morning: {a} of {tot} = {num(first)}, leaving {num(rest)}. Afternoon: {b} of {num(rest)} = {num(second)}, leaving {num(rest)} − {num(second)} = {num(left)}.",
        recipe={"op": "frac_rest2", "args": {"total": tot, "f1": str(a), "f2": str(b)}, "fmt": "num"})

for ctx, x, y, unit, what in [("A carpenter cuts two boards for a counter, one {x} meter long and one {y} meter long.", F(3, 4), F(2, 3), "meters", "What is their total length in meters"),
                              ("A canteen worker pours {x} liter of soup into one pot and {y} liter into another.", F(5, 6), F(3, 8), "liters", "How many liters were poured in all")]:
    s = ctx.format(x=x, y=y) + f" {what}?"
    tot = x + y
    lcd = x.denominator * y.denominator // __import__("math").gcd(x.denominator, y.denominator)
    add(**base(nxt(), "Fractions", "adding unlike fractions", "rename to a common denominator before adding", "NUM-FRAC-DEC", "easy", 40),
        stem=s, correct=frac(tot),
        wrong=[(f"{x.numerator + y.numerator}/{x.denominator + y.denominator}", "NUM-OP-SWAP", "Adding tops and bottoms separately is not how fractions add; the pieces must first share a denominator."),
               (frac(tot - F(1, lcd)), "NUM-OFF-BY-ONE", f"This is 1/{lcd} short; recount the renamed numerators."),
               (frac(abs(x - y)), "NUM-OP-SWAP", "This is the difference between the two amounts; the question asks for the total.")],
        terms="Unlike fractions have different denominators; rename both over the least common denominator (LCD), then add the numerators.",
        shortcut="Cross-multiply: (a×d + b×c) / (b×d), then simplify.",
        why_correct=f"The LCD of {x.denominator} and {y.denominator} is {lcd}: {x} = {x.numerator * lcd // x.denominator}/{lcd} and {y} = {y.numerator * lcd // y.denominator}/{lcd}. Added: {x.numerator * lcd // x.denominator + y.numerator * lcd // y.denominator}/{lcd} = {frac(tot)} {unit}.",
        recipe={"op": "frac_add", "args": {"f1": str(x), "f2": str(y)}, "fmt": "frac"})

for ctx, w1, r1, w2, r2, unit in [("A household had {a} kilograms of rice and cooked {b} kilograms during the week.", 5, F(1, 2), 2, F(3, 4), "kilograms"),
                                  ("A health center had {a} boxes of gloves and used {b} boxes during a vaccination drive.", 7, F(1, 3), 4, F(5, 6), "boxes")]:
    A, Bv = w1 + r1, w2 + r2
    s = ctx.format(a=f"{w1} {r1}", b=f"{w2} {r2}") + f" How many {unit} are left?"
    left = A - Bv
    add(**base(nxt(), "Fractions", "subtracting mixed numbers", "borrow a whole when the fraction part is too small", "NUM-FRAC-DEC", "medium", 45),
        stem=s, correct=frac(left),
        wrong=[(frac((w1 - w2) + abs(r1 - r2)), "NUM-OP-SWAP", f"This subtracts the smaller fraction from the larger one; {r1} − {r2} needs borrowing instead."),
               (frac(A + Bv), "NUM-OP-SWAP", "This adds the two amounts; the question asks what is left."),
               (frac(left - 1), "NUM-OFF-BY-ONE", "This takes off one whole too many: after borrowing, only the remaining wholes are subtracted.")],
        terms="Mixed number: a whole number and a fraction. To subtract, rename both as improper fractions, or borrow 1 whole from the first number.",
        shortcut="Convert to improper fractions over one denominator, subtract, then convert back.",
        why_correct=f"{w1} {r1} = {A}, {w2} {r2} = {Bv} (as improper fractions). {A} − {Bv} = {left} = {frac(left)} {unit}.",
        recipe={"op": "frac_sub", "args": {"a": str(A), "b": str(Bv)}, "fmt": "frac"})

for ctx, f_, tot in [("In a municipal office of {t} employees, {f} ride the jeepney to work. How many employees ride the jeepney?", F(2, 5), 35),
                     ("A school ordered {t} chairs, and {f} of them have arrived. How many chairs have arrived?", F(5, 9), 63)]:
    v = f_ * tot
    add(**base(nxt(), "Fractions", "fraction of a whole number", "divide by the denominator, multiply by the numerator", "NUM-FRAC-DEC", "easy", 35),
        stem=ctx.format(t=tot, f=f_), correct=num(v),
        wrong=[(num(tot - v), "NUM-OTHER-SHARE", "This is the part that does not fit the description, the complement of the fraction."),
               (num(F(tot, f_.denominator)), "NUM-PARTIAL", f"This is only one {f_.denominator}th of {tot}; it still has to be multiplied by {f_.numerator}."),
               (num(tot * f_.numerator), "NUM-PARTIAL", "This multiplies by the numerator but never divides by the denominator.")],
        terms="\"Fraction of\" a number means multiply: (numerator ÷ denominator) × the number.",
        shortcut=f"Divide first to keep numbers small: {tot} ÷ {f_.denominator} = {tot // f_.denominator}, then × {f_.numerator}.",
        why_correct=f"{tot} ÷ {f_.denominator} = {tot // f_.denominator}, and {tot // f_.denominator} × {f_.numerator} = {num(v)}.",
        recipe={"op": "frac_of", "args": {"total": tot, "f": str(f_)}, "fmt": "num"})

for ctx, L, f_, unit in [("A {L}-meter roll of packing tape is cut into strips, each {f} meter long. How many strips can be cut?", 6, F(3, 4), "strips"),
                         ("A {L}-liter container of disinfectant is poured into spray bottles that each hold {f} liter. How many bottles can be filled?", 10, F(2, 5), "bottles")]:
    v = F(L) / f_
    add(**base(nxt(), "Fractions", "dividing by a fraction", "dividing by a fraction is multiplying by its reciprocal", "NUM-FRAC-DEC", "medium", 40),
        stem=ctx.format(L=L, f=f_), correct=num(v),
        wrong=[(num(F(L) * f_), "NUM-OP-SWAP", "This multiplies by the fraction; fitting pieces into a length is division."),
               (num(v - 1), "NUM-OFF-BY-ONE", "This is one short; the division comes out exact, so no piece is wasted."),
               (num(F(L * f_.denominator)), "NUM-PARTIAL", f"This multiplies by {f_.denominator} but never divides by {f_.numerator}.")],
        terms="To divide by a fraction, multiply by its reciprocal (flip it): ÷ a/b = × b/a.",
        shortcut=f"{L} ÷ {f_} = {L} × {f_.denominator}/{f_.numerator}.",
        why_correct=f"{L} × {f_.denominator} = {L * f_.denominator}, and {L * f_.denominator} ÷ {f_.numerator} = {num(v)} {unit}.",
        recipe={"op": "frac_div", "args": {"total": L, "f": str(f_)}, "fmt": "num"})

for ctx, f_, part, money in [("A barangay spent {p} on medicines, which is {f} of its health budget for the quarter. What is the whole quarterly health budget?", F(3, 8), 4500, True),
                             ("After a cleanup, volunteers had collected {p} sacks of plastic, which is {f} of their target. How many sacks is the full target?", F(4, 7), 52, False)]:
    whole = F(part) / f_
    fm = peso if money else num
    add(**base(nxt(), "Fractions", "finding the whole from a part", "part ÷ fraction = whole", "NUM-FRAC-DEC", "medium", 45),
        stem=ctx.format(p=fm(part), f=f_), correct=fm(whole),
        wrong=[((fm(F(part) * f_), "NUM-OP-SWAP", "This takes a fraction of the part; the part is already the fraction, so divide.") if money or (F(part) * f_).denominator == 1
                else (fm(part * f_.denominator), "NUM-PARTIAL", f"This multiplies by {f_.denominator} but forgets to divide by {f_.numerator}.")),
               (fm(F(part, f_.numerator)), "NUM-PARTIAL", f"This is one {f_.denominator}th of the whole; multiply by {f_.denominator} to finish."),
               (fm(whole - part), "NUM-OTHER-SHARE", "This is the rest of the whole, the part not yet counted.")],
        terms=f"If {f_} of a whole is known, one {f_.denominator}th is the part ÷ {f_.numerator}, and the whole is {f_.denominator} of those.",
        shortcut="Whole = part × denominator ÷ numerator.",
        why_correct=f"{fm(part)} ÷ {f_.numerator} = {fm(F(part, f_.numerator))} per {f_.denominator}th; × {f_.denominator} = {fm(whole)}.",
        recipe={"op": "frac_whole", "args": {"part": part, "f": str(f_)}, "fmt": "peso" if money else "num"})

for ctx, a, b in [("Half of a covered court is reserved for a job fair, and {b} of that reserved area is set aside for registration. What fraction of the whole court is the registration area?", F(1, 2), F(2, 3)),
                  ("{a} of a provincial road project is in Town A, and {b} of the Town A portion is already paved. What fraction of the whole project is the paved part in Town A?", F(3, 4), F(2, 9))]:
    v = a * b
    add(**base(nxt(), "Fractions", "fraction of a fraction", "\"of\" between fractions means multiply", "NUM-FRAC-DEC", "easy", 35),
        stem=ctx.format(a=a, b=b), correct=frac(v),
        wrong=[(frac(a + b), "NUM-OP-SWAP", "This adds the two fractions; a fraction of a fraction is found by multiplying.") if a + b < 1 else
               (f"{a.numerator + b.numerator}/{a.denominator + b.denominator}", "NUM-OP-SWAP", "This adds tops and bottoms; a fraction of a fraction is found by multiplying."),
               (frac(b), "NUM-WRONG-BASE", "This is the share of the smaller area only, not of the whole."),
               (frac(abs(a - b)), "NUM-OP-SWAP", "This subtracts; \"of\" calls for multiplication.")],
        terms="A fraction of a fraction: multiply numerators and multiply denominators, then simplify.",
        shortcut="Cancel common factors across before multiplying.",
        why_correct=f"{a} × {b} = {a.numerator * b.numerator}/{a.denominator * b.denominator} = {frac(v)} of the whole.",
        recipe={"op": "frac_mul", "args": {"f1": str(a), "f2": str(b)}, "fmt": "frac"})

for ctx, fs in [("Four teams report how much of their encoding is done: Team 1, 5/8; Team 2, 3/5; Team 3, 7/12; Team 4, 2/3. Which fraction shows the team that is farthest along?", [F(5, 8), F(3, 5), F(7, 12), F(2, 3)]),
                ("Four water jugs are filled to these levels: 4/9, 3/7, 5/11 and 2/5. Which jug holds the largest fraction of its capacity?", [F(4, 9), F(3, 7), F(5, 11), F(2, 5)])]:
    m = max(fs)
    others = [x for x in fs if x != m]
    add(**base(nxt(), "Fractions", "comparing fractions", "compare by cross-multiplying or by decimals", "NUM-FRAC-DEC", "medium", 45),
        stem=ctx, correct=f"{m.numerator}/{m.denominator}",
        wrong=[(f"{x.numerator}/{x.denominator}", c, w) for x, c, w in zip(sorted(others, key=lambda t: -t.denominator), ["NUM-WRONG-BASE", "NUM-PARTIAL", "NUM-DECIMAL"],
               ["The largest denominator does not make the largest fraction; compare the values.", "A larger numerator alone does not decide it; the denominator matters too.", "As a decimal this is smaller than the key; check each to two places."])],
        terms="To compare fractions, cross-multiply (a/b > c/d when a×d > b×c) or convert each to a decimal.",
        shortcut="Compare each fraction with 1/2 first, then cross-multiply the close ones.",
        why_correct="As decimals: " + ", ".join(f"{x.numerator}/{x.denominator} ≈ {float(x):.3f}" for x in fs) + f". The largest is {m.numerator}/{m.denominator}.",
        recipe={"op": "frac_max", "args": {"fs": [str(x) for x in fs]}, "fmt": "fracraw"})

# ---------- Ratios ----------
for ctx, tot, r, idx, label in [("Two cousins share a ₱{t} prize from a barangay quiz bee in the ratio {r}. How much does the cousin with the smaller share get?", 7200, (5, 3), 1, "smaller"),
                                ("A cooperative divides ₱{t} of earnings between its savings fund and its members' dividends in the ratio {r}. How much goes to dividends?", 18000, (4, 5), 1, "second")]:
    a, b = r
    share = F(tot * r[idx], a + b)
    add(**base(nxt(), "Ratios", "sharing in a ratio", "total ÷ number of parts × parts wanted", "NUM-WP-RATIO", "easy", 60),
        stem=ctx.format(t=f"{tot:,}", r=f"{a} : {b}"), correct=peso(share),
        wrong=[(peso(F(tot * r[1 - idx], a + b)), "NUM-OTHER-SHARE", "This is the other person's (or fund's) share, not the one asked for."),
               (peso(F(tot, 2)), "NUM-PARTIAL", "This splits the total equally and ignores the ratio."),
               (peso(F(tot * r[idx], a)), "NUM-WRONG-BASE", f"This divides by {a} parts instead of the {a + b} parts in the whole ratio.")],
        terms="A ratio a : b splits a total into a + b equal parts; each side gets its number of parts.",
        shortcut=f"One part = {peso(tot)} ÷ {a + b}.",
        why_correct=f"{a} + {b} = {a + b} parts, so one part is {peso(F(tot, a + b))}. The share asked for is {r[idx]} parts = {peso(share)}.",
        recipe={"op": "ratio_share", "args": {"total": tot, "parts": list(r), "idx": idx}, "fmt": "peso"})

for ctx, tot, r, idx in [("Three volunteers pack {t} relief bags in the ratio {r} according to the hours each can give. How many bags does the second volunteer pack?", 600, (2, 3, 5), 1),
                         ("A town spreads {t} seedlings among three barangays in the ratio {r}. How many seedlings go to the barangay with the largest share?", 1260, (3, 5, 6), 2)]:
    s = sum(r); share = F(tot * r[idx], s)
    add(**base(nxt(), "Ratios", "three-way ratio", "add all the parts first", "NUM-WP-RATIO", "medium", 75),
        stem=ctx.format(t=f"{tot:,}", r=" : ".join(map(str, r))), correct=num(share),
        wrong=[(num(F(tot * r[(idx + 1) % 3], s)), "NUM-OTHER-SHARE", "This is a different person's (or barangay's) share."),
               (num(F(tot, 3)), "NUM-PARTIAL", "This splits the total into three equal shares and ignores the ratio."),
               (num(F(tot * r[idx], r[idx] + r[(idx + 1) % 3])), "NUM-WRONG-BASE", "This uses only two of the three parts as the base.")],
        terms="In a three-way ratio a : b : c, the whole is a + b + c parts.",
        shortcut=f"One part = {tot:,} ÷ {s} = {num(F(tot, s))}.",
        why_correct=f"{' + '.join(map(str, r))} = {s} parts; one part = {num(F(tot, s))}; the share asked for is {r[idx]} × {num(F(tot, s))} = {num(share)}.",
        recipe={"op": "ratio_share", "args": {"total": tot, "parts": list(r), "idx": idx}, "fmt": "num"})

for ctx, r, known, ki in [("In a training class, the ratio of men to women is {r}. If there are {k} women, how many men are there?", (4, 5), 35, 1),
                          ("A clinic's ratio of nurses to midwives is {r}. If there are {k} nurses, how many midwives work there?", (7, 3), 28, 0)]:
    other = 1 - ki
    v = F(known * r[other], r[ki])
    add(**base(nxt(), "Ratios", "finding a quantity from a ratio", "scale the ratio up to the known amount", "NUM-WP-RATIO", "easy", 50),
        stem=ctx.format(r=f"{r[0]} : {r[1]}", k=known), correct=num(v),
        wrong=[(num(F(known * r[ki], r[other])), "NUM-OP-SWAP", "This flips the ratio; match each number to the group it describes."),
               (num(v + known), "NUM-EXTRA-STEP", "This adds both groups; the question asks for one group only."),
               (num(known - (r[ki] - r[other])) if known - (r[ki] - r[other]) != v else num(v + 2), "NUM-PARTIAL", "Subtracting the difference of the ratio terms does not scale the ratio.")],
        terms="Equivalent ratios: multiply both terms by the same number. Find that multiplier from the known group.",
        shortcut=f"Multiplier = {known} ÷ {r[ki]} = {num(F(known, r[ki]))}.",
        why_correct=f"{known} ÷ {r[ki]} = {num(F(known, r[ki]))}, and {r[other]} × {num(F(known, r[ki]))} = {num(v)}.",
        recipe={"op": "ratio_part", "args": {"known": known, "parts": list(r), "ki": ki}, "fmt": "num"})

for ctx, r, diff in [("The ages of two siblings are in the ratio {r}, and the older one is {d} years older. How old is the older sibling?", (7, 4), 27),
                     ("Two offices received complaint letters in the ratio {r}. The first office received {d} more letters than the second. How many letters did the first office receive?", (9, 5), 32)]:
    part = F(diff, r[0] - r[1]); v = part * r[0]
    add(**base(nxt(), "Ratios", "ratio with a known difference", "the difference of the terms equals the known difference", "NUM-WP-RATIO", "medium", 75),
        stem=ctx.format(r=f"{r[0]} : {r[1]}", d=diff), correct=num(v),
        wrong=[(num(part * r[1]), "NUM-OTHER-SHARE", "This is the smaller quantity, not the larger one asked for."),
               (num(F(diff * r[0], r[0] + r[1])), "NUM-WRONG-BASE", "This treats the difference as if it were the total."),
               (num(part), "NUM-PARTIAL", "This is the size of one part only.")],
        terms="If a : b and the difference is known, then (a − b) parts equal that difference.",
        shortcut=f"One part = {diff} ÷ ({r[0]} − {r[1]}).",
        why_correct=f"{r[0]} − {r[1]} = {r[0] - r[1]} parts = {diff}, so one part is {num(part)}. The larger is {r[0]} × {num(part)} = {num(v)}.",
        recipe={"op": "ratio_diff", "args": {"diff": diff, "parts": list(r)}, "fmt": "num"})

for ctx, ab, bc in [("In a warehouse, the ratio of rice sacks to sugar sacks is {ab}, and the ratio of sugar sacks to flour sacks is {bc}. What is the ratio of rice sacks to flour sacks?", (2, 3), (4, 5)),
                    ("At a job fair, the ratio of applicants to interviewers is {ab}, and the ratio of interviewers to booths is {bc}. What is the ratio of applicants to booths?", (15, 2), (4, 3))]:
    a, b = ab; b2, c = bc
    A, C = a * b2, b * c
    from math import gcd
    g = gcd(A, C)
    key = f"{A // g} : {C // g}"
    add(**base(nxt(), "Ratios", "combining ratios", "make the shared term equal", "NUM-WP-RATIO", "medium", 75),
        stem=ctx.format(ab=f"{a} : {b}", bc=f"{b2} : {c}"), correct=key,
        wrong=[(f"{a} : {c}", "NUM-PARTIAL", "This joins the outer terms without making the middle terms match."),
               (f"{C // g} : {A // g}", "NUM-OP-SWAP", "This reverses the order asked for."),
               (f"{a + b2} : {b + c}", "NUM-OP-SWAP", "Adding terms of two ratios does not combine them.")],
        terms="To chain a : b and b : c, rewrite both so the shared middle term is the same number.",
        shortcut="Multiply across: (a × second b) : (first b × c).",
        why_correct=f"Make the middle terms equal: {a} : {b} = {a * b2} : {b * b2} and {b2} : {c} = {b * b2} : {b * c}. So the outer ratio is {A} : {C}" + ("." if f"{A} : {C}" == key else f", which simplifies to {key}."),
        recipe={"op": "ratio_chain", "args": {"ab": list(ab), "bc": list(bc)}, "fmt": "raw"})

for ctx, sc, d, unit in [("On a provincial road map, 1 cm stands for {s} km. Two town halls are {d} cm apart on the map. What is the actual distance?", F(5, 2), F(32, 5), "km"),
                         ("A floor plan uses a scale of 1 cm to {s} m. A hallway measures {d} cm on the plan. How long is the actual hallway?", F(3, 2), F(9, 1), "m")]:
    v = sc * d
    add(**base(nxt(), "Ratios", "map scale", "multiply the map length by the scale", "NUM-WP-RATIO", "easy", 45),
        stem=ctx.format(s=num(sc), d=num(d)), correct=f"{num(v)} {unit}",
        wrong=[(f"{num(d / sc)} {unit}", "NUM-OP-SWAP", "This divides by the scale; each centimeter stands for more distance, so multiply."),
               (f"{num(d + sc)} {unit}", "NUM-OP-SWAP", "This adds the scale to the map length."),
               (f"{num(v * 10)} {unit}", "NUM-UNIT", "This slips a factor of ten; the scale is already in the answer unit.")],
        terms="A map scale 1 cm : k units means every centimeter on paper is k units on the ground.",
        shortcut="Actual = map length × scale value.",
        why_correct=f"{num(d)} × {num(sc)} = {num(v)} {unit}.",
        recipe={"op": "mul", "args": {"a": str(sc), "b": str(d)}, "fmt": "unit", "unit": unit})

for ctx, a, b, c, unit in [("A feeding program uses {a} kilograms of rice for every {b} children. How many kilograms are needed for {c} children?", 3, 12, 30, "kilograms"),
                           ("A printer uses {a} toner cartridges for every {b} reams of paper printed. How many cartridges are needed for {c} reams?", 2, 15, 75, "cartridges")]:
    v = F(a * c, b)
    add(**base(nxt(), "Ratios", "direct proportion", "set up equal ratios and cross-multiply", "NUM-WP-RATIO", "easy", 50),
        stem=ctx.format(a=a, b=b, c=c), correct=f"{num(v)} {unit}",
        wrong=[(f"{num(F(c, b))} {unit}", "NUM-PARTIAL", f"This is only the scaling factor ({c} ÷ {b}); multiply it by {a}."),
               (f"{num(a + (c - b))} {unit}", "NUM-OP-SWAP", "Adding the increase does not keep the rate the same."),
               (f"{num(F(a * c, b) * 2)} {unit}", "NUM-EXTRA-STEP", "This doubles the answer for no reason in the problem.")],
        terms="In a direct proportion, both quantities grow by the same factor: a/b = x/c.",
        shortcut=f"Factor = {c} ÷ {b} = {num(F(c, b))}; multiply {a} by it.",
        why_correct=f"{c} ÷ {b} = {num(F(c, b))}, and {a} × {num(F(c, b))} = {num(v)} {unit}.",
        recipe={"op": "proportion", "args": {"a": a, "b": b, "c": c}, "fmt": "unit", "unit": unit})

# ---------- Basic algebra ----------
for ctx, a, b, c in [("Solve for x: {a}x + {b} = {c}.", 3, 7, 31), ("A tricycle driver's fare rule is {b} pesos plus {a} pesos for every kilometer. A passenger paid {c} pesos. Writing the fare as {a}x + {b} = {c}, how many kilometers (x) was the ride?", 2, 15, 37)]:
    x = F(c - b, a)
    add(**base(nxt(), "Basic algebra", "one-variable linear equation", "undo the addition, then the multiplication", "NUM-WP-ALGEBRA", "easy", 40),
        stem=ctx.format(a=a, b=b, c=c), correct=num(x),
        wrong=[(num(F(c + b, a)), "NUM-OP-SWAP", f"This adds {b} instead of subtracting it from both sides."),
               (num(c - b), "NUM-PARTIAL", f"This stops after subtracting {b}; still divide by {a}."),
               (num(F(c, a) - b) if F(c, a) - b > 0 else num(x + 3), "NUM-ORDER-OPS", "This divides first and subtracts later, which undoes the steps in the wrong order.")],
        terms="Solving a linear equation: do the same operation on both sides, undoing addition first, then multiplication.",
        shortcut=f"x = ({c} − {b}) ÷ {a}.",
        why_correct=f"{a}x = {c} − {b} = {c - b}, so x = {c - b} ÷ {a} = {num(x)}. Check: {a} × {num(x)} + {b} = {c}.",
        recipe={"op": "lin", "args": {"a": a, "b": b, "c": c}, "fmt": "num"})

for ctx, k, sub, res in [("When a number is tripled and 8 is subtracted, the result is 49. What is the number?", 3, 8, 49),
                         ("Ramon thinks of a number, multiplies it by 5, then subtracts 12. He gets 63. What number did he start with?", 5, 12, 63)]:
    x = F(res + sub, k)
    add(**base(nxt(), "Basic algebra", "translating words to an equation", "write the steps as an equation, then undo them in reverse", "NUM-WP-ALGEBRA", "easy", 45),
        stem=ctx, correct=num(x),
        wrong=[(num(F(res - sub, k)), "NUM-OP-SWAP", f"This subtracts {sub} again instead of adding it back."),
               (num(res + sub), "NUM-PARTIAL", f"This adds {sub} back but forgets to divide by {k}."),
               (num(F(res, k) + sub) if F(res, k).denominator == 1 else num(x + 2), "NUM-ORDER-OPS", "This divides before adding back, which reverses the steps in the wrong order.")],
        terms="Working backward: undo the last step first. The opposite of subtracting is adding; the opposite of multiplying is dividing.",
        shortcut=f"({res} + {sub}) ÷ {k}.",
        why_correct=f"Let the number be x: {k}x − {sub} = {res}. Then {k}x = {res + sub}, so x = {num(x)}. Check: {k} × {num(x)} − {sub} = {res}.",
        recipe={"op": "lin", "args": {"a": k, "b": -sub, "c": res}, "fmt": "num"})

for ctx, cnt, step, tot, want in [("The sum of three consecutive odd numbers is 81. What is the largest of the three?", 3, 2, 81, "largest"),
                                  ("Four consecutive whole numbers add up to 106. What is the smallest of them?", 4, 1, 106, "smallest")]:
    first = F(tot - step * cnt * (cnt - 1) // 2, cnt)
    last = first + step * (cnt - 1)
    v = last if want == "largest" else first
    add(**base(nxt(), "Basic algebra", "consecutive numbers", "the middle value is the average", "NUM-WP-ALGEBRA", "medium", 60),
        stem=ctx, correct=num(v),
        wrong=[(num(first if want == "largest" else last), "NUM-OTHER-SHARE", f"This is the {'smallest' if want == 'largest' else 'largest'} number, not the {want}."),
               (num(F(tot, cnt)) if F(tot, cnt).denominator == 1 else num(first + 1 if want == 'smallest' else last - 1), "NUM-PARTIAL", "This is the middle (average) value, not the one asked for."),
               (num(v + step if want == "largest" else v - step), "NUM-OFF-BY-ONE", "This is one step past the end of the list of numbers.")],
        terms=f"Consecutive {'odd' if step == 2 else 'whole'} numbers go up by {step}: x, x + {step}, x + {2 * step}…",
        shortcut=f"Average = {tot} ÷ {cnt}; count out from the middle.",
        why_correct=f"Write them as x, x + {step}, …; the sum is {cnt}x + {step * cnt * (cnt - 1) // 2} = {tot}, so x = {num(first)}. The numbers run {num(first)} to {num(last)}; the {want} is {num(v)}.",
        recipe={"op": "consec", "args": {"count": cnt, "step": step, "total": tot, "want": want}, "fmt": "num"})

for ctx, k, tot in [("Two numbers add up to 72, and one is 5 times the other. What is the smaller number?", 5, 72),
                    ("A school's two buildings have 96 classrooms in all. The new building has 3 times as many classrooms as the old one. How many classrooms are in the old building?", 3, 96)]:
    s = F(tot, k + 1)
    add(**base(nxt(), "Basic algebra", "one number as a multiple of another", "x + kx = total", "NUM-WP-ALGEBRA", "easy", 45),
        stem=ctx, correct=num(s),
        wrong=[(num(s * k), "NUM-OTHER-SHARE", "This is the larger number."),
               (num(F(tot, k)), "NUM-WRONG-BASE", f"This divides by {k}, forgetting that the smaller number is one more part: {k} + 1 = {k + 1}."),
               (num(F(tot, 2)), "NUM-PARTIAL", "This splits the total in half, ignoring the multiple.")],
        terms="If one number is k times the other, together they make k + 1 equal parts.",
        shortcut=f"{tot} ÷ ({k} + 1).",
        why_correct=f"x + {k}x = {k + 1}x = {tot}, so x = {num(s)} (and the larger is {num(s * k)}).",
        recipe={"op": "multiple", "args": {"k": k, "total": tot}, "fmt": "num"})

for ctx, d1, d2, cnt, val, want in [("A cashier's drawer has 40 coins, all five-peso and ten-peso coins, worth ₱290 in all. How many ten-peso coins are there?", 5, 10, 40, 290, 10),
                                    ("Joy paid exactly ₱210 for snacks using 30 coins, all one-peso and ten-peso coins. How many one-peso coins did she use?", 1, 10, 30, 210, 1)]:
    tens = F(val - d1 * cnt, d2 - d1); ones = cnt - tens
    v = tens if want == d2 else ones
    add(**base(nxt(), "Basic algebra", "coin problem", "assume all coins are the smaller kind, then trade up", "NUM-WP-ALGEBRA", "medium", 75),
        stem=ctx, correct=num(v),
        wrong=[(num(ones if want == d2 else tens), "NUM-OTHER-SHARE", "This is the number of the other kind of coin."),
               (num(F(val, d2)) if F(val, d2).denominator == 1 else num(v + 3), "NUM-PARTIAL", "This divides the total value by one coin value and ignores the coin count."),
               (num(F(cnt, 2)), "NUM-PARTIAL", "This splits the coins evenly without checking the value.")],
        terms="Two-unknown problem: let x be one kind; the other kind is (total coins − x). Write one equation for the value.",
        shortcut=f"If all {cnt} were ₱{d1} coins, the value would be ₱{d1 * cnt}; each swap to a ₱{d2} coin adds ₱{d2 - d1}.",
        why_correct=f"All ₱{d1}: ₱{d1 * cnt}. Shortfall ₱{val} − ₱{d1 * cnt} = ₱{val - d1 * cnt}; ÷ ₱{d2 - d1} = {num(tens)} ten-peso coins, and {num(ones)} of the other kind.",
        recipe={"op": "coins", "args": {"d1": d1, "d2": d2, "count": cnt, "value": val, "want": want}, "fmt": "num"})

for v_, ctx, dist, why, ans, ws in [
        ("x", "Solve for x: 5(x − 2) = 3x + 4.", "5x − 10 = 3x + 4", "2x = 14", "7",
         [("−3", "NUM-OP-SWAP", "This moves −10 across without changing its sign (2x = 4 − 10)."),
          ("1.75", "NUM-OP-SWAP", "This adds 5x and 3x instead of subtracting (8x = 14)."),
          ("3", "NUM-ORDER-OPS", "This writes 5(x − 2) as 5x − 2, forgetting to multiply the 2 by 5.")]),
        ("y", "Solve for y: 4(y + 3) = 7y − 9.", "4y + 12 = 7y − 9", "21 = 3y", "7",
         [("1", "NUM-OP-SWAP", "This moves −9 across without changing its sign (3 = 3y)."),
          ("−7", "NUM-OP-SWAP", "This keeps the sign wrong when moving the y terms; check by substituting back."),
          ("4", "NUM-ORDER-OPS", "This writes 4(y + 3) as 4y + 3, forgetting to multiply the 3 by 4.")])]:
    add(**base(nxt(), "Basic algebra", "variables on both sides", "distribute, collect the variable on one side", "NUM-WP-ALGEBRA", "medium", 60),
        stem=ctx, correct=ans, wrong=ws,
        terms="Distributive property: a(x + b) = ax + ab. Then gather the variable terms on one side and the numbers on the other, changing signs as terms cross.",
        shortcut="Distribute first; then move the smaller variable term so its coefficient stays positive.",
        why_correct=f"Distribute: {dist}. Collect terms: {why}, so {v_} = {ans}. Check by substituting {ans} into both sides.",
        recipe={"op": "lin2", "args": {"stem": ctx}, "fmt": "num"})

for ctx, k, ag, d4, w4 in [("A grandmother is 5 times as old as her grandson. In 18 years she will be twice as old as he will be then. How old is the grandson now?", 5, 18, "9", "This divides 18 by (5 − 3); the equation 5x + 18 = 2(x + 18) gives x = 18 ÷ (5 − 2)."),
                   ("A father is 4 times as old as his daughter. In 20 years he will be twice as old as she will be then. How old is the daughter now?", 4, 20, "5", "This divides 20 by 4; the equation 4x + 20 = 2(x + 20) gives x = 20 ÷ (4 − 2).")]:
    s = F(ag, k - 2)
    add(**base(nxt(), "Basic algebra", "age problem", "add the years to both people", "NUM-WP-ALGEBRA", "hard", 90),
        stem=ctx, correct=num(s),
        wrong=[(num(s * k), "NUM-OTHER-SHARE", "This is the parent's present age."),
               (num(s + ag), "NUM-EXTRA-STEP", "This is the child's age in the future, not now."),
               (d4, "NUM-WRONG-BASE", w4)],
        terms="Age problems: both people get older by the same number of years.",
        shortcut=f"{k}x + {ag} = 2(x + {ag}) gives x = {ag} ÷ ({k} − 2).",
        why_correct=f"Let the child be x now; the parent is {k}x. In {ag} years: {k}x + {ag} = 2(x + {ag}), so {'' if k == 3 else str(k - 2)}x = {ag}{'' if k == 3 else f' and x = {num(s)}'}.",
        recipe={"op": "age", "args": {"k": k, "years": ag}, "fmt": "num"})

add(**base(nxt(), "Basic algebra", "equation with a fraction", "clear the fraction by multiplying", "NUM-WP-ALGEBRA", "easy", 40),
    stem="If one fourth of a number, decreased by 3, equals 5, what is the number?", correct="32",
    wrong=[("8", "NUM-PARTIAL", "8 is one fourth of the number; multiply by 4 to get the number."), ("20", "NUM-OP-SWAP", "This subtracts 3 instead of adding it back before multiplying."),
           ("23", "NUM-ORDER-OPS", "This multiplies 5 by 4 and then adds 3, undoing the steps in the wrong order.")],
    terms="\"One fourth of a number, decreased by 3\" is x/4 − 3. Undo the subtraction first, then the division.",
    shortcut="(5 + 3) × 4.", why_correct="x/4 − 3 = 5, so x/4 = 8 and x = 32. Check: 32 ÷ 4 − 3 = 5.",
    recipe={"op": "lin", "args": {"a": "1/4", "b": -3, "c": 5}, "fmt": "num"})

# ---------- Word problems (non-percent) ----------
for ctx, items_, paid in [("At a school supply store, Teresa buys 4 ballpens at ₱18 each and 3 folders at ₱25 each. She pays with a ₱200 bill. How much change should she get?", [(4, 18), (3, 25)], 200),
                          ("For a seminar, Carlo buys 6 bottles of water at ₱15 each and 2 boxes of pandesal at ₱85 each, paying with a ₱500 bill. What is his change?", [(6, 15), (2, 85)], 500)]:
    cost = sum(q * p for q, p in items_)
    add(**base(nxt(), "Word problems", "change from a purchase", "total the cost, then subtract from the bill", "NUM-WP-RATE", "easy", 45),
        stem=ctx, correct=peso(paid - cost),
        wrong=[(peso(cost), "NUM-PARTIAL", "This is the total bill, not the change."),
               (peso(paid - sum(p for _, p in items_)), "NUM-PARTIAL", "This subtracts one of each item only and forgets the quantities."),
               (peso(paid - cost - 10), "NUM-EXTRA-STEP", "This takes off an extra ₱10 that is not in the problem.")],
        terms="Change = amount paid − total cost. Total cost = sum of (quantity × unit price).",
        shortcut="Group each item's subtotal before subtracting.",
        why_correct=" + ".join(f"{q} × ₱{p} = ₱{q * p}" for q, p in items_) + f"; total ₱{cost}. Change: ₱{paid} − ₱{cost} = {peso(paid - cost)}.",
        recipe={"op": "change", "args": {"items": items_, "paid": paid}, "fmt": "peso"})

for ctx, start, end, brk in [("A data encoder starts work at 8:45 a.m. and stops at 1:20 p.m., taking a 30-minute lunch break in between. How long did she actually encode?", (8, 45), (13, 20), 30),
                             ("A seminar ran from 9:50 a.m. to 3:05 p.m., with a 45-minute lunch and a 15-minute snack break. How much time was spent in actual sessions?", (9, 50), (15, 5), 60)]:
    mins = (end[0] * 60 + end[1]) - (start[0] * 60 + start[1]) - brk
    hm = lambda m: f"{m // 60} hours {m % 60} minutes" if m % 60 else f"{m // 60} hours"
    add(**base(nxt(), "Word problems", "elapsed time", "count to the next hour, then whole hours, then the leftover", "NUM-WP-RATE", "medium", 60),
        stem=ctx, correct=hm(mins),
        wrong=[(hm(mins + brk), "NUM-PARTIAL", "This is the time from start to finish; the breaks still come off."),
               (hm(mins - 40 if (mins - 40) % 60 else mins - 50), "NUM-UNIT", "This treats the clock like decimals (100 minutes in an hour) when subtracting."),
               (hm(mins - 60), "NUM-OFF-BY-ONE", "This loses one hour when the times cross noon; convert p.m. times to 24-hour time first.")],
        terms="Elapsed time: change both times to minutes after midnight (or count up hour by hour), subtract, then remove the breaks.",
        shortcut="Count up: to the next whole hour, then full hours, then the remaining minutes.",
        why_correct=f"From start to end is {hm(mins + brk)}. Minus {brk} minutes of breaks leaves {hm(mins)}.",
        recipe={"op": "elapsed", "args": {"start": list(start), "end": list(end), "brk": brk}, "fmt": "hm"})

for ctx, d, v in [("A bus from Roxas to Iloilo covers 150 km at an average of 60 km/h. How long is the trip?", 150, 60),
                  ("A delivery van travels 210 km at an average speed of 84 km/h. How long does the trip take?", 210, 84)]:
    t = F(d, v); mins = int(t * 60)
    hm = lambda m: f"{m // 60} hours {m % 60} minutes" if m % 60 else f"{m // 60} hours"
    add(**base(nxt(), "Word problems", "distance, rate and time", "time = distance ÷ speed", "NUM-WP-RATE", "easy", 50),
        stem=ctx, correct=hm(mins),
        wrong=[(f"{num(t)} hours 0 minutes".replace(" 0 minutes", "") if False else f"{int(t)} hours {int(round((t - int(t)) * 100))} minutes", "NUM-DECIMAL", f"This reads {num(t)} hours as hours and hundredths; 0.5 hour is 30 minutes, not 50."),
               (hm(mins + 30), "NUM-OFF-BY-ONE", "This adds an extra half hour not supported by the numbers."),
               (hm(int(F(d, v + 10) * 60)), "NUM-GIVEN-REUSED", "This uses a different speed from the one given.")],
        terms="Distance = speed × time, so time = distance ÷ speed. A decimal hour must be converted: × 60 for minutes.",
        shortcut="Fraction of an hour × 60 = minutes.",
        why_correct=f"{d} ÷ {v} = {num(t)} hours = {hm(mins)}.",
        recipe={"op": "travel_time", "args": {"d": d, "v": v}, "fmt": "hm"})

for ctx, a, b in [("Bea can type the minutes of a meeting in 6 hours; Nonoy can type the same minutes in 3 hours. If they split the work and type at the same time, how many hours will it take?", 6, 3),
                  ("One hose fills a water tank in 4 hours, and a second hose fills it in 12 hours. If both run at once, how long until the tank is full?", 4, 12)]:
    t = F(a * b, a + b)
    add(**base(nxt(), "Word problems", "combined work rate", "add the rates, not the times", "NUM-WP-RATE", "medium", 75),
        stem=ctx, correct=f"{num(t)} hours",
        wrong=[(f"{num(F(a + b, 2))} hours", "NUM-OP-SWAP", "Averaging the two times ignores that both work at once."),
               (f"{num(a + b)} hours", "NUM-OP-SWAP", "Adding the times gives longer, not shorter, work."),
               (f"{num(min(a, b))} hours", "NUM-PARTIAL", "This is how long the faster one needs alone; with help the job finishes sooner.")],
        terms="Work rate: a job done in h hours means 1/h of the job per hour. Rates add when people (or pipes) work together.",
        shortcut="Together time = (a × b) ÷ (a + b).",
        why_correct=f"1/{a} + 1/{b} = {F(1, a) + F(1, b)} of the job per hour, so the job takes {num(t)} hours.",
        recipe={"op": "together", "args": {"a": a, "b": b}, "fmt": "unit", "unit": "hours"})

for ctx, sc, target in [("Paolo scored 82, 75 and 90 on three quizzes. What score does he need on the fourth quiz to average 85?", [82, 75, 90], 85),
                        ("A clinic served 46, 52, 39 and 55 patients on four days. How many must it serve on the fifth day to average 50 patients a day?", [46, 52, 39, 55], 50)]:
    need = target * (len(sc) + 1) - sum(sc)
    add(**base(nxt(), "Word problems", "missing value for a target average", "target total − current total", "NUM-WP-AVERAGE", "medium", 60),
        stem=ctx, correct=num(need),
        wrong=[(num(target), "NUM-PARTIAL", "This assumes the next value only has to equal the target average."),
               (num(F(sum(sc), len(sc)).__round__()), "NUM-GIVEN-REUSED", "This is close to the current average, which is not what is needed."),
               (num(round(2 * target - F(sum(sc), len(sc)))), "NUM-PARTIAL", "This adds the gap between the target and the current average only once; the new value must lift every earlier value too.")],
        terms="Average = total ÷ number of values. A target average fixes the needed total.",
        shortcut=f"Needed total = {target} × {len(sc) + 1}; subtract what is already in.",
        why_correct=f"Needed total: {target} × {len(sc) + 1} = {target * (len(sc) + 1)}. Current total: {sum(sc)}. Needed value: {need}.",
        recipe={"op": "avg_missing", "args": {"scores": sc, "target": target}, "fmt": "num"})

for ctx, need, pack, pu in [("A barangay office needs 250 envelopes for its notices. Envelopes are sold only in packs of 40. How many packs must it buy?", 250, 40, "packs"),
                        ("A school needs 130 meal boxes for a field trip. The caterer sells them only in trays of 12. How many trays are needed?", 130, 12, "trays")]:
    v = ceil(F(need, pack))
    add(**base(nxt(), "Word problems", "rounding up in context", "a part pack still has to be bought", "NUM-WP-RATE", "easy", 45),
        stem=ctx, correct=num(v),
        wrong=[(num(need // pack), "NUM-OFF-BY-ONE", "This rounds down; the leftover need still requires one more full pack."),
               (num(v * pack - need), "NUM-PARTIAL", f"This is how many spare items {v} {pu} leave over, not the number of {pu}."),
               (num(v + 1), "NUM-EXTRA-STEP", "This buys one pack more than needed.")],
        terms="When items come only in whole packs, divide and round UP whenever there is a remainder.",
        shortcut="If pack × quotient falls short, add one pack.",
        why_correct=f"{need // pack} {pu} hold only {need // pack} × {pack} = {need // pack * pack}, which is short of {need}. One more makes {v} × {pack} = {v * pack}, enough, so {v} {pu} are needed.",
        recipe={"op": "ceil_div", "args": {"need": need, "pack": pack}, "fmt": "num"})

for ctx, L, gap in [("A straight fence 48 m long gets a post every 4 m, with a post at both ends. How many posts are needed?", 48, 4),
                    ("Along a 90-meter straight path, a barangay plants a tree every 6 meters, starting at one end and finishing at the other. How many trees are planted?", 90, 6)]:
    v = L // gap + 1
    add(**base(nxt(), "Word problems", "posts and gaps", "posts = gaps + 1 on a straight line", "NUM-WP-GEOM", "easy", 45),
        stem=ctx, correct=num(v),
        wrong=[(num(L // gap), "NUM-OFF-BY-ONE", "This counts gaps, not posts; a straight line with both ends needs one more."),
               (num(L // gap - 1), "NUM-OFF-BY-ONE", "This leaves out both end posts."),
               (num(L // gap * 2), "NUM-EXTRA-STEP", "This doubles the count, as if both sides of the path were planted.")],
        terms="Fence-post rule: on a straight line with something at both ends, the count is (length ÷ spacing) + 1.",
        shortcut="Picture a tiny case: 8 m with posts every 4 m needs 3 posts.",
        why_correct=f"{L} ÷ {gap} = {L // gap} gaps, so {L // gap} + 1 = {v}.",
        recipe={"op": "posts", "args": {"length": L, "gap": gap}, "fmt": "num"})

add(**base(nxt(), "Word problems", "installment payment", "subtract the down payment, then divide", "NUM-WP-RATE", "easy", 45),
    stem="An electric fan costs ₱3,960. The buyer pays ₱1,200 down and the rest in 6 equal monthly payments. How much is each monthly payment?", correct="₱460",
    wrong=[("₱660", "NUM-PARTIAL", "This divides the full price by 6 and forgets the down payment."), ("₱860", "NUM-OP-SWAP", "This adds the down payment back before dividing."),
           ("₱552", "NUM-WRONG-BASE", "This divides the balance by 5 months instead of 6.")],
    terms="Installment: balance = price − down payment; each payment = balance ÷ number of payments.",
    shortcut="Take out the down payment first.", why_correct="₱3,960 − ₱1,200 = ₱2,760 balance; ₱2,760 ÷ 6 = ₱460 a month.",
    recipe={"op": "installment", "args": {"price": 3960, "down": 1200, "months": 6}, "fmt": "peso"})
