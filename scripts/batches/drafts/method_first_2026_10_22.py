"""Method-first Numerical explanations for draft rows of the flat-2100 manifest (CONTINUE directive 2026-10-22).

Adds reveal.method_steps with the eight parts: 1_asked, 2_givens, 3_method, 4_why, 5_solve_by_hand, 6_check, 7_distractors, 8_shortcut.
Families with a fixed structure (order of operations, difference/multiply series, rectangle edging, price after a discount)
are built from the numbers in the stem and recomputed here; every other row has a hand-written entry in HAND.
Only status "draft" rows are touched. Approved or reviewed rows get -R1 proposals instead (never edited in place)."""
import re
from fractions import Fraction as F


def _n(s):
    return int(s.replace(",", ""))


def _p(v):
    return f"₱{v:,}"


def _dist(it):
    rv = it["reveal"]
    return " ".join(f"{next(o['text'] for o in it['options'] if o['option_id'] == k)}: {v}" for k, v in rv["why_wrong"].items())


def ops(it):
    s = it["stem"]
    m = re.search(r"(\d+) − (\d+) ÷ (\d+) \+ (\d+)", s)
    if m:
        a, b, c, d = map(int, m.groups())
        q = b // c
        return dict(asked="The value of the expression, following the order of operations.", givens=f"{a} − {b} ÷ {c} + {d}",
                    method="Order of operations: × and ÷ before + and −; then + and − from left to right.",
                    why=f"The ÷ sign binds {b} and {c} together, so {b} ÷ {c} must be done before anything is subtracted from {a}.",
                    solve=f"{b} ÷ {c} = {q}. Then {a} − {q} = {a - q}. Then {a - q} + {d} = {a - q + d}.",
                    check=f"Rewrite as {a} + {d} − {q} = {a + d} − {q} = {a - q + d}: the same answer, so the order was right.",
                    shortcut="Circle every × and ÷ first and replace it with its value; what is left is only + and −.")
    m = re.search(r"(\d+) × \((\d+) − (\d+)\) \+ (\d+)", s)
    if m:
        a, b, c, d = map(int, m.groups())
        return dict(asked="The value of the expression, following the order of operations.", givens=f"{a} × ({b} − {c}) + {d}",
                    method="Parentheses first, then ×, then +.",
                    why="Parentheses group a part that must be finished before it is used in a product.",
                    solve=f"{b} − {c} = {b - c}. Then {a} × {b - c} = {a * (b - c)}. Then {a * (b - c)} + {d} = {a * (b - c) + d}.",
                    check=f"Estimate: {a} × {b - c} is about {round(a, -1)} × {b - c} = {round(a, -1) * (b - c)}; adding {d} gives a value near {round(a, -1) * (b - c) + d}, close to {a * (b - c) + d}.",
                    shortcut=f"Multiply {a} × {b - c} by splitting {a}: ({a - a % 10} × {b - c}) + ({a % 10} × {b - c}).")
    m = re.search(r"(\d+) × (\d+) ÷ \((\d+) − (\d+)\)", s)
    if m:
        a, b, c, d = map(int, m.groups())
        return dict(asked="The value of the expression, following the order of operations.", givens=f"{a} × {b} ÷ ({c} − {d})",
                    method="Parentheses first; then × and ÷ from left to right.",
                    why="The divisor is the whole parenthesis, so it must be found before dividing.",
                    solve=f"{c} − {d} = {c - d}. Then {a} × {b} = {a * b}. Then {a * b} ÷ {c - d} = {a * b // (c - d)}.",
                    check=f"Multiply back: {a * b // (c - d)} × {c - d} = {a * b}, which equals {a} × {b}.",
                    shortcut=f"Cancel before multiplying when you can: divide {a} or {b} by {c - d} first if it divides evenly.")
    return None


def series(it):
    m = re.search(r"([\d, ]+), ___", it["stem"])
    if not m:
        return None
    xs = [int(x) for x in re.findall(r"\d+", m.group(1))]
    key = _n(next(o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"]))
    d = [b - a for a, b in zip(xs, xs[1:])]
    dd = {b - a for a, b in zip(d, d[1:])}
    if len(dd) == 1:
        g = dd.pop()
        return dict(asked="The next number in the series.", givens=", ".join(map(str, xs)),
                    method="Write the jumps between terms; if the jumps themselves change by a fixed amount, continue that pattern.",
                    why="When the terms grow faster and faster but not by multiplying, the jumps usually form their own simple series.",
                    solve=f"Jumps: {', '.join(map(str, d))}; each jump is {g} more than the last. Next jump: {d[-1]} + {g} = {d[-1] + g}. Next term: {xs[-1]} + {d[-1] + g} = {xs[-1] + d[-1] + g}.",
                    check=f"Rebuild the series from {xs[0]} with jumps {', '.join(map(str, d + [d[-1] + g]))}: you get {', '.join(map(str, xs))}, {key}.",
                    shortcut="Two rows: terms on top, jumps below. Extend the bottom row first.")
    for k in (2, 3):
        c = xs[1] - k * xs[0]
        if all(b == k * a + c for a, b in zip(xs, xs[1:])):
            return dict(asked="The next number in the series.", givens=", ".join(map(str, xs)),
                        method=f"Test a multiply-then-add rule: term × {k} {'+' if c >= 0 else '−'} {abs(c)}.",
                        why="The terms roughly triple or double each time, which points to multiplication; the small leftover is a constant added.",
                        solve=f"{xs[-1]} × {k} = {xs[-1] * k}; {xs[-1] * k} {'+' if c >= 0 else '−'} {abs(c)} = {xs[-1] * k + c}.",
                        check=f"Test the rule on an early pair: {xs[0]} × {k} {'+' if c >= 0 else '−'} {abs(c)} = {xs[1]}, and {xs[1]} × {k} {'+' if c >= 0 else '−'} {abs(c)} = {xs[2]}.",
                        shortcut=f"Divide a term by the one before (about {k}); the multiplier is {k}, then find what is added.")
    return None


def edging(it):
    m = re.search(r"(\d+) m long and (\d+) m wide\. Edging costs ₱([\d,]+) per meter", it["stem"])
    if not m:
        return None
    L, W, c = int(m.group(1)), int(m.group(2)), _n(m.group(3))
    P = 2 * (L + W)
    return dict(asked="The cost of edging all the way around the rectangle.", givens=f"length {L} m, width {W} m, ₱{c:,} per meter",
                method="Find the perimeter, then multiply by the cost per meter.",
                why="Edging goes around the outside, so the distance to pay for is the perimeter, not the area.",
                solve=f"Perimeter = 2 × ({L} + {W}) = 2 × {L + W} = {P} m. Cost = {P} × ₱{c:,} = {_p(P * c)}.",
                check=f"Walk the sides: {L} + {W} + {L} + {W} = {P} m. Then {_p(P * c)} ÷ ₱{c:,} = {P} m.",
                shortcut=f"Add one length and one width ({L + W}), double it, then multiply: {L + W} × 2 × {c}.")


def discount(it):
    m = re.search(r"priced at ₱([\d,]+)\. It is sold at (\d+)% off", it["stem"])
    if not m:
        return None
    p, r = _n(m.group(1)), int(m.group(2))
    dsc = p * r // 100
    return dict(asked="The price the buyer pays after the discount.", givens=f"price ₱{p:,}, discount {r}%",
                method=f"Find {r}% of the price and subtract it, or pay {100 - r}% of the price directly.",
                why="\"Off\" means taken away from the price, so the buyer pays the part that is left.",
                solve=f"10% of ₱{p:,} = ₱{p // 10:,}. {r}% = {_p(dsc)}. ₱{p:,} − {_p(dsc)} = {_p(p - dsc)}.",
                check=f"{100 - r}% of ₱{p:,} = {_p(p * (100 - r) // 100)}, the same answer.",
                shortcut=f"Pay {100 - r}%: ₱{p:,} × {100 - r} ÷ 100.")


HAND = {
 "CIVIO-NUM-WP-RATE-000116-R1": dict(asked="How long the two painters take working together.", givens="Nestor alone 21 hours, Aling Rosa alone 28 hours",
    method="Add the work rates (jobs per hour), then invert.", why="Working together means their hourly work adds up; times do not add.",
    solve="Nestor: 1/21 of the job per hour; Aling Rosa: 1/28. With denominator 84: 4/84 + 3/84 = 7/84 = 1/12. So the job takes 12 hours.",
    check="In 12 hours, Nestor does 12/21 = 4/7 and Aling Rosa 12/28 = 3/7; 4/7 + 3/7 = 1 whole job.", shortcut="Together time = (a × b) ÷ (a + b) = (21 × 28) ÷ 49 = 12."),
 "CIVIO-B3-NUM-DECIMAL-0175": dict(asked="The product 125 × 0.8.", givens="125 and 0.8", method="Change 0.8 to the fraction 4/5.",
    why="Dividing by 5 and multiplying by 4 is easier by hand than multiplying by a decimal.", solve="125 ÷ 5 = 25; 25 × 4 = 100.",
    check="0.8 is a little less than 1, so the answer must be a little less than 125: 100 fits.", shortcut="× 0.8 = × 8 ÷ 10: 1,000 ÷ 10 = 100."),
 "CIVIO-B3-NUM-FRAC-DEC-0180": dict(asked="0.125 written as a fraction in lowest terms.", givens="0.125", method="Write the decimal over 1,000, then reduce.",
    why="Three decimal places mean thousandths.", solve="0.125 = 125/1,000. Divide top and bottom by 125: 1/8.",
    check="1 ÷ 8 = 0.125.", shortcut="Know the eighths: 1/8 = 0.125, 3/8 = 0.375, 5/8 = 0.625."),
 "CIVIO-B3-NUM-FRAC-DEC-0183": dict(asked="The fraction of all items that are pens.", givens="pens : pencils = 3 : 5", method="Add the ratio terms to get the whole.",
    why="A part-to-part ratio becomes a part-to-whole fraction over the sum of the parts.", solve="3 + 5 = 8 parts in all; pens are 3 of them: 3/8.",
    check="Pencils would be 5/8, and 3/8 + 5/8 = 1.", shortcut="Part ÷ (sum of the ratio terms)."),
 "CIVIO-B3-NUM-PCT-BASIC-0173": dict(asked="18% of 450 thousand pesos, in thousands.", givens="450 (thousand pesos), 18%", method="Split 18% into 10% and 8%.",
    why="10% and 1% are easy to find by moving the decimal point.", solve="10% of 450 = 45. 1% = 4.5, so 8% = 36. 45 + 36 = 81.",
    check="20% would be 90; 18% must be a little less: 81 fits.", shortcut="18% = 20% − 2%: 90 − 9 = 81."),
 "CIVIO-B3-NUM-PCT-BASIC-0184": dict(asked="2.5% of ₱800.", givens="₱800, 2.5%", method="Find 1%, then multiply by 2.5.",
    why="1% of a number is that number ÷ 100.", solve="1% of 800 = 8; 2.5 × 8 = 20.", check="5% of 800 is 40; half of that is 20.", shortcut="2.5% = 1/40: 800 ÷ 40 = 20."),
 "CIVIO-B3-NUM-PCT-BASIC-0265": dict(asked="The allowance before a 20% raise.", givens="after the raise: ₱180; raise 20%",
    method="The new amount is 120% of the old one; divide by 1.2.", why="The 20% is 20% of the old amount, not of ₱180.",
    solve="120% = ₱180, so 10% = ₱15 and 100% = ₱150.", check="20% of 150 = 30; 150 + 30 = 180.", shortcut="Old = new ÷ 1.2 (or new × 5/6)."),
 "CIVIO-B3-NUM-PROPERTY-0041": dict(asked="15 + 27.", givens="15, 27", method="Add tens, then ones.", why="Place value lets you add in parts.",
    solve="10 + 20 = 30; 5 + 7 = 12; 30 + 12 = 42.", check="42 − 27 = 15.", shortcut="Round 27 to 30: 15 + 30 = 45, minus 3 = 42."),
 "CIVIO-B3-NUM-PROPERTY-0042": dict(asked="96 ÷ 8.", givens="96, 8", method="Split 96 into parts that 8 divides.", why="80 and 16 are both multiples of 8.",
    solve="80 ÷ 8 = 10; 16 ÷ 8 = 2; 10 + 2 = 12.", check="8 × 12 = 96.", shortcut="Halve three times: 96 → 48 → 24 → 12."),
 "CIVIO-B3-NUM-PROPERTY-0043": dict(asked="7 × 9.", givens="7, 9", method="Use 7 × 10 and take away one 7.", why="9 is one less than 10.",
    solve="7 × 10 = 70; 70 − 7 = 63.", check="63 ÷ 9 = 7.", shortcut="For × 9, the digits of the answer add to 9: 6 + 3 = 9."),
 "CIVIO-B3-NUM-PROPERTY-0044": dict(asked="100 − 37.", givens="100, 37", method="Count up from 37 to 100.", why="Counting up avoids borrowing across zeros.",
    solve="37 + 3 = 40; 40 + 60 = 100; 3 + 60 = 63.", check="63 + 37 = 100.", shortcut="Subtract each digit of 37 from 9 except the last from 10: 6 and 3."),
 "CIVIO-B3-NUM-PROPERTY-0176": dict(asked="The value of 2⁵.", givens="base 2, exponent 5", method="Multiply 2 by itself five times.", why="The exponent counts the factors, not a multiplier.",
    solve="2 × 2 = 4; × 2 = 8; × 2 = 16; × 2 = 32.", check="2⁵ is not 2 × 5 = 10; doubling 1 five times gives 32.", shortcut="Learn the powers of 2: 2, 4, 8, 16, 32, 64."),
 "CIVIO-B3-NUM-PROPERTY-0178": dict(asked="The least common multiple of 6 and 8.", givens="6, 8", method="List multiples of the larger number until one is divisible by the smaller.",
    why="The LCM is the smallest number both divide evenly.", solve="Multiples of 8: 8, 16, 24. 24 ÷ 6 = 4, so the LCM is 24.",
    check="24 ÷ 8 = 3 and 24 ÷ 6 = 4, both whole; 16 ÷ 6 is not.", shortcut="LCM = a × b ÷ GCF = 48 ÷ 2 = 24."),
 "CIVIO-B3-NUM-PROPERTY-0179": dict(asked="The greatest common factor of 36 and 54.", givens="36, 54", method="Factor both and take the shared part.",
    why="The GCF is the largest number dividing both.", solve="36 = 2 × 18; 54 = 3 × 18. 2 and 3 share no factor, so the GCF is 18.",
    check="36 ÷ 18 = 2, 54 ÷ 18 = 3, and no larger number divides both.", shortcut="GCF(36, 54) = GCF(36, 54 − 36) = GCF(36, 18) = 18."),
 "CIVIO-B3-NUM-PROPERTY-0263": dict(asked="The whole number whose square is 196.", givens="196", method="Bracket between known squares.",
    why="13² = 169 and 15² = 225, so the root is between 13 and 15.", solve="196 ends in 6, so the root ends in 4 or 6; 14 is the only choice between 13 and 15. 14 × 14 = 196.",
    check="14 × 14 = 140 + 56 = 196.", shortcut="Squares ending in 6 come from numbers ending in 4 or 6."),
 "CIVIO-B3-NUM-SEQ-DIFF-0045": dict(asked="The next number.", givens="3, 6, 9, 12", method="Find the constant difference.", why="The terms rise by the same amount each time.",
    solve="Difference 3; 12 + 3 = 15.", check="These are the multiples of 3: 3 × 5 = 15.", shortcut="Same jump every time: add it once more."),
 "CIVIO-B3-NUM-SEQ-DIFF-0187": dict(asked="The next term.", givens="1, 1, 2, 3, 5, 8", method="Add the two terms before.", why="Jumps 0, 1, 1, 2, 3 repeat the series itself, the sign of a Fibonacci series.",
    solve="5 + 8 = 13.", check="3 + 5 = 8 and 2 + 3 = 5, so the rule holds throughout.", shortcut="Each term = the two before it added."),
 "CIVIO-B3-NUM-SEQ-DIFF-0193": dict(asked="The next number.", givens="1, 4, 9, 16, 25", method="Recognize perfect squares (or jumps 3, 5, 7, 9).", why="Both views give the same rule.",
    solve="6² = 36 (or 25 + 11 = 36).", check="Jumps 3, 5, 7, 9, 11 rise by 2.", shortcut="Learn squares 1 to 15."),
 "CIVIO-B3-NUM-SEQ-DIFF-0196": dict(asked="The next number.", givens="11, 13, 17, 19, 23", method="Check for primes.", why="Jumps 2, 4, 2, 4 do not settle, but every term is prime.",
    solve="After 23: 24, 25, 26, 27 and 28 are not prime; 29 is.", check="29 has no divisor other than 1 and itself.", shortcut="Primes after 20: 23, 29, 31, 37."),
 "CIVIO-B3-NUM-SEQ-MULT-0190": dict(asked="The next term.", givens="7, 14, 28, 56", method="Find the ratio.", why="Each term is twice the one before.",
    solve="56 × 2 = 112.", check="14 ÷ 7 = 28 ÷ 14 = 56 ÷ 28 = 2.", shortcut="Doubling: add the number to itself."),
 "CIVIO-B3-NUM-SEQ-MULT-0267": dict(asked="The fifth term.", givens="1, 2, 6, 24", method="Find the multipliers.", why="The multipliers are 2, 3, 4, so the next is 5.",
    solve="24 × 5 = 120.", check="1 × 2 × 3 × 4 × 5 = 120.", shortcut="These are factorials: 5! = 120."),
 "CIVIO-B3-NUM-UNIT-0264": dict(asked="Minutes in 3.5 hours.", givens="3.5 hours, 60 minutes per hour", method="Multiply hours by 60.", why="Each hour is 60 minutes.",
    solve="3 × 60 = 180; 0.5 × 60 = 30; 180 + 30 = 210.", check="210 ÷ 60 = 3.5.", shortcut="Half an hour is 30 minutes."),
 "CIVIO-B4-NUM-WP-ALGEBRA-0201": dict(asked="The larger of two numbers.", givens="sum 50, difference 8", method="Larger = (sum + difference) ÷ 2.",
    why="Adding the difference to the sum gives two copies of the larger number.", solve="(50 + 8) ÷ 2 = 29.", check="Smaller = 29 − 8 = 21; 29 + 21 = 50.",
    shortcut="Split the sum in half (25), then add half the difference (4): 29."),
 "CIVIO-B4-NUM-WP-GEOM-0206": dict(asked="The length of fence around the lot.", givens="12 m by 5 m", method="Perimeter of a rectangle = 2 × (length + width).",
    why="A fence goes around the outside edge.", solve="2 × (12 + 5) = 2 × 17 = 34 m.", check="12 + 5 + 12 + 5 = 34.", shortcut="Add one length and one width, then double."),
 "CIVIO-B4-NUM-WP-RATE-0349": dict(asked="Folders put away in 4 hours.", givens="18 folders per hour, 4 hours", method="Rate × time.", why="The same amount is done each hour.",
    solve="18 × 4 = 72.", check="72 ÷ 4 = 18.", shortcut="Double twice: 36, 72."),
 "CIVIO-B4-NUM-WP-RATIO-0209": dict(asked="The middle share.", givens="₱900, ratio 2 : 3 : 4", method="Find one part, then the shares.", why="The ratio terms add up to the number of equal parts.",
    solve="2 + 3 + 4 = 9 parts; ₱900 ÷ 9 = ₱100; middle share 3 × ₱100 = ₱300.", check="₱200 + ₱300 + ₱400 = ₱900.", shortcut="Middle term over sum: 3/9 = 1/3 of ₱900."),
 "CIVIO-NUM-WP-ALGEBRA-926051": dict(asked="Forms in each set before 4 damaged ones were removed.", givens="3 sets, 4 removed from each, 24 usable in all",
    method="Undo the steps backward: share the usable forms, then add back the removed ones.", why="The 24 usable forms are split evenly across 3 sets.",
    solve="24 ÷ 3 = 8 usable per set; 8 + 4 = 12 forms per set before removal.", check="3 × (12 − 4) = 3 × 8 = 24.", shortcut="Equation: 3(x − 4) = 24, so x − 4 = 8 and x = 12."),
}


def steps(it):
    h = HAND.get(it["id"])
    f = h or ops(it) or series(it) or edging(it) or discount(it)
    if not f:
        return None
    return {"1_asked": f["asked"], "2_givens": f["givens"], "3_method": f["method"], "4_why": f["why"], "5_solve_by_hand": f["solve"],
            "6_check": f["check"], "7_distractors": _dist(it), "8_shortcut": f["shortcut"]}
