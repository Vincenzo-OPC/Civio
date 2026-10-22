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
                        why="The terms roughly triple or double each time, which points to multiplication; the small leftover is a constant added or taken away.",
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


# ---- Families added 22 Oct pm (GT directive 3, item d): approved and reviewed rows, used only in -R1 proposals ----
from fractions import Fraction as _F
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(__file__))
from method_first_reviewed_2026_10_22 import H as _REV  # noqa: E402

_TIMES = {"twice": 2, "three times": 3, "four times": 4}


def fence(it):
    m = re.search(r"(\d+) m long and (\d+) m wide\. (?:A|An) ([\w -]+?) costs ₱([\d,]+) per meter", it["stem"])
    if not m:
        return None
    L, W, what, c = int(m.group(1)), int(m.group(2)), m.group(3), _n(m.group(4))
    P = 2 * (L + W)
    return dict(asked=f"The cost of putting the {what} around the whole rectangle.", givens=f"length {L} m, width {W} m, ₱{c:,} per meter",
                method="Find the perimeter, then multiply by the cost per meter.",
                why=f"The {what} goes around the outside, so you pay for the perimeter, not the area.",
                solve=f"Perimeter = 2 × ({L} + {W}) = 2 × {L + W} = {P} m. Cost = {P} × ₱{c:,} = {_p(P * c)}.",
                check=f"{L} + {W} + {L} + {W} = {P} m, and {_p(P * c)} ÷ ₱{c:,} = {P}.",
                shortcut=f"Add one length and one width ({L + W}), double it, then multiply by the price.")


def successive(it):
    m = re.search(r"for ₱([\d,]+)\. It raised the price by (\d+)%\. (?:A week later|Later), it (?:cut|lowered) the new price by (\d+)%", it["stem"])
    if not m:
        return None
    p, a, b = _n(m.group(1)), int(m.group(2)), int(m.group(3))
    up = p * (100 + a) // 100
    fin = up * (100 - b) // 100
    return dict(asked="The final price after a raise and then a cut.", givens=f"₱{p:,}; up {a}%; then down {b}% of the new price",
                method="Do the two changes one after the other; the second percent is taken of the new price.",
                why="The two percents have different bases, so they do not cancel or simply add.",
                solve=f"Up {a}%: {a}% of ₱{p:,} = {_p(p * a // 100)}, new price {_p(up)}. Down {b}%: {b}% of {_p(up)} = {_p(up - fin)}; final {_p(fin)}.",
                check=f"Multipliers: ₱{p:,} × {(100 + a) / 100:g} × {(100 - b) / 100:g} = {_p(fin)}.",
                shortcut=f"Multiply by {(100 + a) / 100:g}, then by {(100 - b) / 100:g}.")


def interest(it):
    m = re.search(r"borrows ₱([\d,]+) at (\d+)% simple interest per year\. How much interest (?:will she owe|is due) after (\d+) years?( and 6 months)?", it["stem"])
    if not m:
        return None
    p, r, y, half = _n(m.group(1)), int(m.group(2)), int(m.group(3)), bool(m.group(4))
    t = _F(2 * y + half, 2)
    i = p * r * t / 100
    ts = f"{y}.5" if half else f"{y}"
    return dict(asked="The simple interest owed.", givens=f"principal ₱{p:,}; rate {r}% per year; time {y} years{' and 6 months' if half else ''}",
                method="Simple interest = principal × rate × time (time in years).", why=f"6 months is half a year, so the time is {ts} years." if half else "Simple interest is the same every year.",
                solve=f"One year: {r}% of ₱{p:,} = {_p(p * r // 100) if p * r % 100 == 0 else p * r / 100}. Times {ts} years = {_p(int(i))}.",
                check=f"{_p(int(i))} ÷ {ts} = ₱{p * r / 100:,.0f} per year, which is {r}% of ₱{p:,}.",
                shortcut="Find one year's interest first, then multiply by the years.")


def avg_join(it):
    m = re.search(r"average ([\w ]+?) of the (\d+) .*? is (\d+)(?: years)?\. (?:A new [\w ]+? who is (\d+) years old joins|One more person, with (\d+) years, joins)", it["stem"])
    if not m:
        return None
    n, a, v = int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(5))
    tot = n * a + v
    new = _F(tot, n + 1)
    return dict(asked=f"The new average {m.group(1)} of all {n + 1} people.", givens=f"{n} people averaging {a}; one more with {v}",
                method="Average = total ÷ number of people. Find the old total, add the newcomer, divide by the new count.",
                why="You cannot average the old average with the newcomer: the old average stands for many people.",
                solve=f"Old total = {n} × {a} = {n * a}. New total = {n * a} + {v} = {tot}. New average = {tot} ÷ {n + 1} = {new}.",
                check=f"{new} × {n + 1} = {tot}.", shortcut=f"The newcomer is {v - a} above the average; spread that over {n + 1} people: {a} + {v - a} ÷ {n + 1} = {new}.")


def share(it):
    s = it["stem"]
    m = re.search(r"₱([\d,]+)\b.*?ratio (\d+) : (\d+)\. (?:How much (?:is|will) ([\w' -]+?)(?:'s share| receive)|What is ([\w' -]+?)'s share)", s)
    if not m:
        return None
    T, a, b = _n(m.group(1)), int(m.group(2)), int(m.group(3))
    who = m.group(4) or m.group(5)
    second = re.search(r"(?:between|and) ([\w' -]+?)(?: will| in the ratio)", s)
    names = re.findall(r"([A-Z][\w-]*(?: [A-Z][\w-]*)?) and ([A-Z][\w-]*(?: [A-Z][\w-]*)?)", s)
    k = b
    if names and who.strip() == names[0][0].strip():
        k = a
    part = T // (a + b)
    return dict(asked=f"{who}'s share.", givens=f"₱{T:,} in the ratio {a} : {b}",
                method="Add the ratio terms to get the number of equal parts, find one part, then multiply.",
                why=f"The ₱{T:,} is cut into {a} + {b} = {a + b} equal parts.",
                solve=f"{a} + {b} = {a + b} parts. One part = ₱{T:,} ÷ {a + b} = {_p(part)}. {who}'s share = {k} × {_p(part)} = {_p(k * part)}.",
                check=f"{_p(a * part)} + {_p(b * part)} = ₱{T:,}.", shortcut=f"Share = {k}/{a + b} of the total.")


def ages(it):
    m = re.search(r"is (\d+|three|four|five) times as old as (?:his|her) (\w+)\. In (\d+) years, .*? will be (twice|three times|four times) as old", it["stem"])
    if not m:
        return None
    k, n, j = int(m.group(1)), int(m.group(3)), _TIMES[m.group(4)]
    # k*c + n = j*(c + n) -> c = n(j-1)/(k-j)
    c = n * (j - 1) // (k - j)
    rel = m.group(2)
    return dict(asked="The older person's age now.", givens=f"now {k} times as old as the {rel}; in {n} years, {j} times as old",
                method=f"Let the {rel}'s age be c. Now: {k}c. In {n} years: {k}c + {n} = {j}(c + {n}).",
                why="Both people get older by the same number of years, so add the years to both ages.",
                solve=f"{k}c + {n} = {j}c + {j * n} → {(str(k - j) if k - j > 1 else "")}c = {j * n - n}" + (f" → c = {c}" if k - j > 1 else "") + f". Older person = {k} × {c} = {k * c}.",
                check=f"In {n} years: {k * c + n} and {c + n}; {c + n} × {j} = {j * (c + n)}.",
                shortcut="Try the answer choices: divide by the multiplier, add the years to both, test the second ratio.")


def together(it):
    m = re.search(r"in (\d+) hours\. \w[\w ]*? can (?:do the same job|encode the same box) in (\d+) hours", it["stem"])
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    t = _F(a * b, a + b)
    from math import lcm
    L = lcm(a, b)
    return dict(asked="How long the two take working together.", givens=f"one alone {a} hours, the other alone {b} hours",
                method="Add the parts of the job each does in one hour, then flip.", why="Working together adds work rates; the times themselves do not add.",
                solve=f"Per hour: 1/{a} + 1/{b} = {L // a}/{L} + {L // b}/{L} = {_F(L // a + L // b, L)}. Time = {t} hours.",
                check=f"In {t} hours: {_F(t, a)} + {_F(t, b)} = 1 whole job.", shortcut=f"(a × b) ÷ (a + b) = {a * b} ÷ {a + b} = {t}.")


def remaining(it):
    m = re.search(r"had (\d+) ([\w ]+?)\. It gave out (\d+)/(\d+) of them on Monday and (\d+)/(\d+) of the remaining", it["stem"])
    if not m:
        return None
    N, what = int(m.group(1)), m.group(2)
    a, b, c, d = map(int, m.groups()[2:])
    g1 = N * a // b
    r1 = N - g1
    g2 = r1 * c // d
    return dict(asked=f"How many {what} are left after both days.", givens=f"{N} {what}; {a}/{b} given Monday; {c}/{d} of the rest given Tuesday",
                method="Work one day at a time; Tuesday's fraction is of what was left, not of the original.",
                why="\"Of the remaining\" changes the base for the second fraction.",
                solve=f"Monday: {a}/{b} of {N} = {g1}; left {r1}. Tuesday: {c}/{d} of {r1} = {g2}; left {r1 - g2}.",
                check=f"Fractions kept: {N} × {b - a}/{b} × {d - c}/{d} = {r1 - g2}.", shortcut="Multiply by the fractions kept, not the fractions given.")


def _tok(e):
    return re.findall(r"\d+|[-+×÷()]|−", e)


def _signcheck(cur, val):
    t = [int(x) for x in re.findall(r"[+-]?\s*\d+", cur.replace(" ", ""))]
    pos, neg = [x for x in t if x >= 0], [-x for x in t if x < 0]
    if not neg or len(t) < 2:
        return f"Undo the last step: work backward from {val:g} and you return to the numbers in the expression.".replace("-", "−")
    return (f"Group the signs: added terms {' + '.join(map(str, pos))} = {sum(pos)}; taken-away terms {' + '.join(map(str, neg))} = {sum(neg)}; "
            f"{sum(pos)} − {sum(neg)} = {val:g}.").replace("= -", "= −")


def _reduce(cur, steps):
    """Reduce a flat or parenthesized expression one operation at a time, logging each step."""
    while True:
        p = next((x for x in re.finditer(r"\(([^()]+)\)", cur) if not re.fullmatch(r"-\d+", x.group(1))), None)
        if p:
            inner = _reduce(p.group(1), steps)
            cur = cur[:p.start()] + (f"({inner})" if inner.startswith("-") else inner) + cur[p.end():]
            continue
        q = re.search(r"(\(-\d+\)|\d+)\s*([*/])\s*(\(-\d+\)|\d+)", cur)
        if q:
            v = eval(q.group(0), {"__builtins__": {}}); v = int(v) if v == int(v) else v
            steps.append((q.group(0), v)); cur = cur[:q.start()] + (f"({v})" if v < 0 else f"{v}") + cur[q.end():]; continue
        if re.fullmatch(r"-?\d+", cur.strip()):
            return cur.strip()
        flat = cur.replace("+(-", "-").replace("(-", "-").replace(")", "")
        v = eval(flat, {"__builtins__": {}}); v = int(v)
        steps.append((flat, v))
        return f"{v}"


def _pp(x):
    return (str(x).replace("*", " × ").replace("/", " ÷ ").replace("+", " + ").replace("-", " − ").replace("(", "(").replace("  ", " ")
            .replace("( − ", "(−").replace("× − ", "× (−").strip()).replace("− ", "−", 1) if str(x).startswith("-") else (str(x).replace("*", " × ").replace("/", " ÷ ").replace("+", " + ").replace("-", " − ").replace("( − ", "(−").strip())


def expr(it):
    m = re.fullmatch(r"What is the value of ([\d\s+×÷()−-]+)\?", it["stem"].strip())
    if not m:
        return None
    e = m.group(1).strip()
    py = e.replace("×", "*").replace("÷", "/").replace("−", "-").replace(" ", "")
    steps = []
    val = int(_reduce(py, steps))
    txt = ". ".join(f"{_pp(a)} = {_pp(b)}" for a, b in steps) + "."
    a, v = steps[-1]
    q = re.fullmatch(r"(\d+)/(\d+)", a)
    if q:
        chk = f"Multiply back: {val} × {q.group(2)} = {q.group(1)}."
    else:
        t = [int(x) for x in re.findall(r"[+-]?\d+", a)]
        pos, neg = [x for x in t if x >= 0], [-x for x in t if x < 0]
        j = lambda xs: " + ".join(map(str, xs)) + (f" = {sum(xs)}" if len(xs) > 1 else "")
        chk = (f"Group the signs: added {j(pos)}; taken away {j(neg)}; "
               f"{sum(pos)} − {sum(neg)} = {_pp(val)}.")
    return dict(asked="The value of the expression, following the order of operations.", givens=e,
                method="Parentheses first, then × and ÷ (left to right), then + and − (left to right).",
                why="Working strictly left to right gives a different, wrong value whenever × or ÷ comes after + or −.",
                solve=txt, check=chk, shortcut="Box every product and quotient first; only then add and subtract.")


HAND.update({
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0006": dict(asked="3/4 + 5/6.", givens="3/4, 5/6", method="Common denominator 12.", why="Only like fractions can be added directly.",
    solve="3/4 = 9/12; 5/6 = 10/12; 19/12 = 1 7/12.", check="0.75 + 0.83 ≈ 1.58 ≈ 1 7/12.", shortcut="LCD of 4 and 6 is 12."),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0007": dict(asked="2.5 × 0.04.", givens="2.5, 0.04", method="Multiply as whole numbers, then place the decimal point.", why="Decimal places add up: 1 + 2 = 3.",
    solve="25 × 4 = 100; three decimal places: 0.100 = 0.1.", check="0.04 is 4 hundredths; 2.5 × 4 = 10 hundredths = 0.1.", shortcut="× 0.04 = × 4 ÷ 100."),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0008": dict(asked="7.2 ÷ 0.08.", givens="7.2, 0.08", method="Move both decimal points two places right.", why="Multiplying both by 100 keeps the quotient the same.",
    solve="7.2 ÷ 0.08 = 720 ÷ 8 = 90.", check="90 × 0.08 = 7.2.", shortcut="Make the divisor a whole number first."),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0009": dict(asked="The greatest of 0.6, 5/8, 0.58, 3/5.", givens="0.6, 5/8, 0.58, 3/5", method="Change all to decimals.", why="Decimals line up place by place.",
    solve="5/8 = 0.625; 3/5 = 0.6. Order: 0.58 < 0.6 = 3/5 < 0.625. Greatest: 5/8.", check="5/8 − 3/5 = 25/40 − 24/40 = 1/40 > 0.", shortcut="Write every number to three decimal places."),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0010": dict(asked="Sheets left from 500.", givens="2/5 Monday, 1/4 Tuesday, both of the same ream", method="Add the fractions used, subtract from 1, multiply.", why="Both fractions are of the whole ream.",
    solve="2/5 + 1/4 = 8/20 + 5/20 = 13/20 used; 7/20 left; 7/20 of 500 = 175.", check="Used 200 + 125 = 325; 500 − 325 = 175.", shortcut="Find each day's sheets: 200 and 125."),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0011": dict(asked="1 2/3 × 3/5.", givens="1 2/3, 3/5", method="Change to an improper fraction, then multiply.", why="Mixed numbers cannot be multiplied part by part.",
    solve="1 2/3 = 5/3; 5/3 × 3/5 = 15/15 = 1.", check="5/3 and 3/5 are reciprocals, so the product is 1.", shortcut="Spot reciprocals."),
 "CIVIO-NUM-WP-RATIO-000003": None,
})
HAND.pop("CIVIO-NUM-WP-RATIO-000003")
for _k, _v in _REV.items():
    HAND.setdefault("_rev_" + _k, dict(zip(("asked", "givens", "method", "why", "solve", "check", "shortcut"), _v)))

_base_steps = steps


def steps(it):  # noqa: F811
    h = HAND.get(it["id"]) or (HAND.get("_rev_" + it["id"][-6:]) if it["id"].startswith(("CIVIO-NUM-", )) and it["id"][-6:] in _REV and it["id"][-7:-6] == "-" else None)
    f = h or ops(it) or series(it) or edging(it) or discount(it) or fence(it) or successive(it) or interest(it) or avg_join(it) or share(it) or ages(it) or together(it) or remaining(it) or expr(it)
    if not f:
        return None
    return {"1_asked": f["asked"], "2_givens": f["givens"], "3_method": f["method"], "4_why": f["why"], "5_solve_by_hand": f["solve"],
            "6_check": f["check"], "7_distractors": _dist(it), "8_shortcut": f["shortcut"]}
