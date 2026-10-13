#!/usr/bin/env python3
"""Build a re-parameterized copy of the baseline practice bank.

Each new item keeps the subcategory and the skill, changes names, numbers,
and phrasing, and uses a key this script recomputes. Fact items keep the
same legal choice and change the wording and the option order.

Output: scripts/seeds/baseline_reparameterized.json
"""

from __future__ import annotations

import json
import re
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "storage/app/baseline-bank-export.json"
OUT = Path(__file__).with_name("baseline_reparameterized.json")
FACTS = Path(__file__).with_name("reparam_facts.tsv")


def pack(correct: str, wrongs: list[str], slot: int) -> tuple[list[str], int]:
    cleaned: list[str] = []
    for wrong in wrongs:
        if wrong == correct or wrong in cleaned:
            continue
        cleaned.append(wrong)
    if len(cleaned) < 3:
        raise ValueError(f"need 3 wrong choices for {correct!r}, got {cleaned!r}")
    cleaned = cleaned[:3]
    slot %= 4
    options: list[str | None] = [None, None, None, None]
    options[slot] = correct
    index = 0
    for position in range(4):
        if options[position] is None:
            options[position] = cleaned[index]
            index += 1
    return [str(option) for option in options], slot


def explain(correct: str, work: str, wrongs: list[str]) -> str:
    choice = correct.strip()
    closing = choice if choice.endswith((".", "?", "!")) else choice + "."
    work_line = work.strip()
    if not work_line.endswith((".", "?", "!")):
        work_line += "."
    bits = [work_line, f"The matching choice is “{closing}”"]
    if wrongs:
        shown = ", ".join(f"“{wrong.strip()}”" for wrong in wrongs[:3])
        bits.append(f"{shown} do not follow the same steps.")
    text = " ".join(bits)
    if "??" in text or "\ufffd" in text:
        raise ValueError(text)
    return text


def item(old: dict, stem: str, options: list[str], key: int, explanation: str, language: str | None = None) -> dict:
    if old["stem"].strip() == stem.strip():
        raise ValueError(f"stem unchanged for {old['id']}")
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(f"options for {old['id']}: {options}")
    if not 0 <= key <= 3:
        raise ValueError(key)
    if "??" in stem or any("??" in option for option in options):
        raise ValueError(stem)
    return {
        "replaces_id": old["id"],
        "prior_stem": old["stem"],
        "subcategory_id": old["subcategory_id"],
        "language": language or old["language"] or "English",
        "stem": stem.strip(),
        "options": options,
        "correct_option": key,
        "explanation": explanation.strip(),
    }


def money(value: int) -> str:
    return f"{value:,} pesos"


def percent_of(base: int, pct: int, noun: str, qid: int) -> tuple[str, list[str], int, str]:
    if base * pct % 100 != 0:
        raise ValueError((base, pct))
    answer = base * pct // 100
    stem = f"What is {pct} percent of {base} {noun}?"
    options, key = pack(str(answer), [str(answer + 1), str(answer + pct), str(max(answer - 1, 0)), str(base), str(pct)], qid)
    work = f"{pct} percent is {pct}/100. {base} times {pct}, divided by 100, is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def fraction_of(whole: int, num: int, den: int, noun: str, qid: int) -> tuple[str, list[str], int, str]:
    if whole % den != 0:
        raise ValueError((whole, den))
    answer = whole // den * num
    stem = f"A clerk finishes {num}/{den} of {whole} {noun}. How many {noun} is that?"
    options, key = pack(str(answer), [str(whole // den), str(whole - answer), str(answer + 1), str(max(answer - 1, 0)), str(whole)], qid)
    work = f"{whole} divided by {den} is {whole // den}. Times {num} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def order_ops(a: int, b: int, c: int, d: int, qid: int) -> tuple[str, list[str], int, str]:
    answer = a - b * c + d
    stem = f"Evaluate {a} minus {b} multiplied by {c}, then add {d}."
    options, key = pack(str(answer), [str((a - b) * c + d), str(a - b - c + d), str(a + b * c + d), str(b * c)], qid)
    work = f"Multiply first: {b} times {c} is {b * c}. Then {a} minus {b * c} plus {d} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def discount(price: int, pct: int, qid: int) -> tuple[str, list[str], int, str]:
    if price * pct % 100 != 0:
        raise ValueError((price, pct))
    off = price * pct // 100
    answer = price - off
    stem = f"A fee of {money(price)} is reduced by {pct} percent. What is the amount due?"
    options, key = pack(money(answer), [money(price + off), money(off), money(price - pct), money(answer + 50)], qid)
    work = f"{pct} percent of {price} is {off}. {price} minus {off} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def _ops(old: dict, built: tuple[str, list[str], int, str]) -> dict:
    stem, options, key, explanation = built
    return item(old, stem, options, key, explanation)


def build_operations(old: dict, index: int) -> dict:
    kind = index % 5
    n = index + 2
    if kind == 0:
        pct = 20 if n % 2 == 0 else 10
        base = (8 + n) * 10
        return _ops(old, percent_of(base, pct, "forms", index))
    if kind == 1:
        return _ops(old, order_ops(15 + n, 4, 3, 6, index))
    if kind == 2:
        root = 12 + n
        number = root * root
        options, key = pack(str(root), [str(root - 1), str(root + 1), str(root + 2)], index)
        return item(old, f"What is the square root of {number}?", options, key, explain(options[key], f"{root} times {root} is {number}.", [o for i, o in enumerate(options) if i != key]))
    if kind == 3:
        whole = (n + 4) * 6
        return _ops(old, fraction_of(whole, 5, 6, "pages", index))
    a, b = 6 + n, 8 + (n % 5)
    answer = a * b // gcd(a, b)
    options, key = pack(str(answer), [str(a * b), str(gcd(a, b)), str(a + b), str(answer + a)], index)
    return item(
        old,
        f"What is the least common multiple of {a} and {b}?",
        options,
        key,
        explain(options[key], f"The least common multiple of {a} and {b} is {answer}.", [o for i, o in enumerate(options) if i != key]),
    )


def reverse_percent_problem(qid: int) -> tuple[str, list[str], int, str]:
    result, pct = ((180, 20), (240, 20), (150, 25), (330, 10))[qid % 4]
    if result * 100 % (100 + pct) != 0:
        raise ValueError
    original = result * 100 // (100 + pct)
    stem = f"After a {pct} percent increase, a fee is {money(result)}. What was the original fee?"
    options, key = pack(money(original), [money(result - pct * 2), money(result * pct // 100), money(original + 20), money(result)], qid)
    work = f"The new fee is {100 + pct} percent of the original. {result} times 100, divided by {100 + pct}, is {original}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def sequence_problem(index: int) -> tuple[str, list[str], int, str]:
    kind = index % 8
    start = 3 + index
    if kind == 0:
        series = [(start + i) ** 2 for i in range(4)]
        answer = (start + 4) ** 2
        work = f"These are consecutive squares starting at {start} squared. The next square is {answer}."
    elif kind == 1:
        series = [start * (2**i) for i in range(4)]
        answer = series[-1] * 2
        work = f"Each term doubles. {series[-1]} times 2 is {answer}."
    elif kind == 2:
        series = [start, start + 2]
        while len(series) < 5:
            series.append(series[-1] + series[-2])
        answer = series[-1] + series[-2]
        series = series[:5]
        work = f"Add the last two terms. {series[-2]} plus {series[-1]} is {answer}."
    elif kind == 3:
        series = [start * 16]
        while len(series) < 4:
            series.append(series[-1] // 2)
        answer = series[-1] // 2
        work = f"Divide by 2 each time. The next term is {answer}."
    elif kind == 4:
        series = [start]
        jump = 3
        while len(series) < 4:
            series.append(series[-1] + jump)
            jump += 2
        answer = series[-1] + jump
        work = f"The gaps grow by 2. The next gap is {jump}, so the next term is {answer}."
    elif kind == 5:
        series = [start]
        while len(series) < 4:
            series.append(series[-1] * 2 + 1)
        answer = series[-1] * 2 + 1
        work = f"Multiply by 2 and add 1. {series[-1]} times 2 plus 1 is {answer}."
    elif kind == 6:
        series = [start]
        factor = 2
        while len(series) < 4:
            series.append(series[-1] * factor)
            factor += 1
        answer = series[-1] * factor
        work = f"The multipliers increase by 1. The next multiplier is {factor}, so the next term is {answer}."
    else:
        # Odd numbers that are not all prime: skip. Use primes offset by index via a fixed table sliced uniquely.
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        series = primes[index : index + 4]
        answer = primes[index + 4]
        work = f"These are prime numbers. The next prime after {series[-1]} is {answer}."
    shown = ", ".join(str(number) for number in series)
    options, key = pack(
        str(answer),
        [str(answer + 1), str(answer + 2), str(max(answer - 1, 0)), str(series[-1] + start)],
        index,
    )
    return f"What number comes next: {shown}, ___?", options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def build_sequence(old: dict, index: int) -> dict:
    return _ops(old, sequence_problem(index))


def speed_problem(qid: int) -> tuple[str, list[str], int, str]:
    hours = 4
    rate = 45 + (qid % 4) * 5
    distance = rate * hours
    stem = f"Van route {qid + 1} covers {distance} kilometers in {hours} hours at a steady speed. What is that speed?"
    options, key = pack(f"{rate} km/h", [f"{distance} km/h", f"{hours} km/h", f"{rate + 10} km/h", f"{rate - 5} km/h"], qid)
    work = f"{distance} divided by {hours} is {rate} kilometers per hour."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def build_word_problem(old: dict, index: int) -> dict:
    problems = [
        speed_problem, clerks_problem, discount_problem, tank_problem, sum_diff_problem,
        wage_problem, ratio_problem, interest_problem, perimeter_problem, weight_problem,
        unfinished_problem, share_problem, fuel_problem, printers_problem, walk_problem,
        mixture_problem, folders_problem, remain_problem, equal_boxes_problem, tasks_problem,
    ]
    return _ops(old, problems[index % len(problems)](index))


def clerks_problem(qid: int) -> tuple[str, list[str], int, str]:

    clerks, hours, each = (4, 2, 12 + (qid % 4) * 3)
    if each * clerks * hours % 1:
        raise ValueError
    total = clerks * hours * each
    stem = f"{clerks} clerks in team {qid + 1} finish {total} forms in {hours} hours at the same rate. How many forms does one clerk finish in one hour?"
    options, key = pack(str(each), [str(total // clerks), str(total // hours), str(each * clerks), str(total)], qid)
    work = f"Divide {total} by {clerks} clerks and by {hours} hours. One clerk finishes {each} forms an hour."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def discount_problem(qid: int) -> tuple[str, list[str], int, str]:
    prices = (1200, 1500, 1600, 1800, 2400, 2500)
    pcts = (10, 20, 25, 15)
    price = prices[qid % len(prices)]
    pct = pcts[qid % len(pcts)]
    if price * pct % 100 != 0:
        pct = 10
    return discount(price, pct, qid)


def tank_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((2, 5, 48), (3, 4, 90), (2, 3, 48), (3, 5, 90), (4, 5, 80), (3, 8, 48))
    part, den, liters = setups[qid % len(setups)]
    full = liters * den // part
    stem = f"Tank {qid + 1} is {part}/{den} full and holds {liters} liters at that level. What is its full capacity?"
    options, key = pack(
        f"{full} liters",
        [f"{liters + den} liters", f"{liters * part} liters", f"{full - liters} liters", f"{full + liters} liters"],
        qid,
    )
    work = f"One part is {liters} divided by {part}, or {liters // part} liters. {den} parts make {full} liters."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def sum_diff_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((60, 12), (48, 8), (70, 10), (90, 16), (40, 6))
    total, diff = setups[qid % len(setups)]
    large = (total + diff) // 2
    small = total - large
    if large - small != diff or (total + diff) % 2:
        raise ValueError
    stem = f"Two counts in set {qid + 1} add up to {total} and the larger is {diff} more than the smaller. What is the larger count?"
    options, key = pack(str(large), [str(small), str(total - diff), str(diff), str(large + 2)], qid)
    work = f"Add the difference to the total and divide by 2. {total} plus {diff} is {total + diff}, divided by 2 is {large}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def wage_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((680, 15), (540, 12), (750, 10), (620, 20), (480, 15))
    daily, days = setups[qid % len(setups)]
    answer = daily * days
    stem = f"A worker on crew {qid + 1} earns {money(daily)} a day. With no deductions, what is the pay for {days} days?"
    options, key = pack(money(answer), [money(daily * (days - 2)), money(answer + daily), money(days * 100), money(answer - daily)], qid)
    work = f"{daily} times {days} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def ratio_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((4, 3, 28), (5, 2, 35), (3, 2, 24), (4, 1, 32), (5, 3, 40))
    left, right, cups = setups[qid % len(setups)]
    part = cups // left
    sugar = part * right
    stem = f"Mix {qid + 1} uses rice and beans in the ratio {left}:{right}. If the rice is {cups} cups, how many cups of beans are needed?"
    options, key = pack(str(sugar), [str(sugar + 1), str(sugar - 1), str(cups), str(part), str(left + right)], qid)
    work = f"One rice part is {cups} divided by {left}, or {part}. Beans take {right} parts, so {sugar} cups."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def interest_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((4000, 5, 3), (5000, 6, 2), (2500, 8, 2), (8000, 5, 1), (3000, 4, 5))
    principal, rate, years = setups[qid % len(setups)]
    interest_amount = principal * rate * years // 100
    stem = f"What is the simple interest on account {qid + 1}, {money(principal)} at {rate} percent a year for {years} years?"
    options, key = pack(
        money(interest_amount),
        [money(principal + interest_amount), money(principal * rate // 100), money(interest_amount + principal // 10), money(rate * years * 10)],
        qid,
    )
    work = f"Interest is principal times rate times time. {principal} times {rate} times {years} divided by 100 is {interest_amount}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def perimeter_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((14, 6), (12, 5), (15, 8), (9, 4), (18, 7))
    length, width = setups[qid % len(setups)]
    answer = 2 * (length + width)
    stem = f"Lot {qid + 1} is a rectangle {length} meters by {width} meters. What is its perimeter?"
    options, key = pack(f"{answer} m", [f"{length * width} m", f"{length + width} m", f"{answer + 2} m", f"{length * 2} m"], qid)
    work = f"Perimeter is 2 times ({length} plus {width}). That is {answer} meters."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def weight_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((6, 27, "4.5 kg"), (8, 36, "4.5 kg"), (4, 18, "4.5 kg"), (5, 20, "4 kg"), (8, 20, "2.5 kg"))
    packs, total, answer = setups[qid % len(setups)]
    stem = f"Shipment {qid + 1}: {packs} identical packs weigh {total} kilograms. How much does one pack weigh?"
    options, key = pack(answer, ["3 kg", "5 kg", "6 kg", "2 kg"], qid)
    work = f"{total} divided by {packs} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def unfinished_problem(qid: int) -> tuple[str, list[str], int, str]:
    done = (20, 40, 30, 50)[qid % 4]
    remaining = 100 - done
    still = remaining // 2
    stem = f"Job {qid + 1} is {done} percent complete. Next week the crew finishes half of what is left. What percent is still unfinished after that week?"
    options, key = pack(f"{still}%", [f"{remaining}%", f"{done}%", f"{still + 10}%", f"{100 - still}%"], qid)
    work = f"{remaining} percent is left. Half of that is finished next week, so {still} percent is still unfinished."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def share_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((1200, (2, 3, 5)), (900, (2, 3, 4)), (1800, (1, 2, 3)), (1500, (2, 3, 5)), (2400, (3, 5, 4)))
    total, parts = setups[qid % len(setups)]
    if total % sum(parts) != 0:
        raise ValueError((total, parts))
    unit = total // sum(parts)
    middle = unit * parts[1]
    stem = f"Fund {qid + 1}, {money(total)}, is shared in the ratio {parts[0]}:{parts[1]}:{parts[2]}. How much is the middle share?"
    options, key = pack(money(middle), [money(unit * parts[0]), money(unit * parts[2]), money(unit), money(total // 2 if total // 2 != middle else unit * 2)], qid)
    work = f"The parts add to {sum(parts)}. One part is {unit} pesos. The middle share is {parts[1]} parts, or {middle} pesos."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def fuel_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((15, 180), (12, 180), (10, 150), (8, 120), (18, 180))
    per, distance = setups[qid % len(setups)]
    liters = distance // per
    stem = f"Vehicle {qid + 1} runs {per} kilometers per liter. How many liters are needed for {distance} kilometers?"
    options, key = pack(f"{liters} liters", [f"{per} liters", f"{liters + 3} liters", f"{distance // 10} liters", f"{liters * 2} liters"], qid)
    work = f"{distance} divided by {per} is {liters} liters."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def printers_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((120, 10, 3, 5), (90, 15, 3, 10), (80, 8, 2, 4), (150, 10, 5, 6))
    pages, minutes, printers, ask = setups[qid % len(setups)]
    each_per_min = pages // minutes // printers
    if each_per_min * minutes * printers != pages:
        raise ValueError((pages, minutes, printers))
    answer = each_per_min * ask
    stem = f"Room {qid + 1}: {printers} printers produce {pages} pages in {minutes} minutes at the same speed. How many pages does one printer produce in {ask} minutes?"
    options, key = pack(str(answer), [str(pages // printers), str(pages // minutes), str(answer * printers), str(ask * printers)], qid)
    work = f"Together they print {pages // minutes} pages a minute, or {each_per_min} per printer. In {ask} minutes one printer makes {answer} pages."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def walk_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((5, 15, "3 hours"), (4, 10, "2.5 hours"), (6, 18, "3 hours"), (4, 14, "3.5 hours"), (5, 20, "4 hours"))
    speed, distance, answer = setups[qid % len(setups)]
    stem = f"Walker {qid + 1} moves at {speed} kilometers per hour. How long does it take to cover {distance} kilometers?"
    options, key = pack(answer, ["2 hours", "5 hours", "1.5 hours", "6 hours"], qid)
    work = f"{distance} divided by {speed} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def mixture_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = (
        ("One liter of a 10 percent solution is mixed with 3 liters of a 30 percent solution.", "25%", "0.1 plus 0.9 is 1 liter of solute in 4 liters, which is 25 percent."),
        ("Two liters of a 10 percent solution are mixed with 2 liters of a 30 percent solution.", "20%", "0.2 plus 0.6 is 0.8 liter of solute in 4 liters, which is 20 percent."),
        ("One liter of a 20 percent solution is mixed with 1 liter of a 40 percent solution.", "30%", "0.2 plus 0.4 is 0.6 liter of solute in 2 liters, which is 30 percent."),
    )
    stem, correct, work = setups[qid % len(setups)]
    stem = f"Batch {qid + 1}: {stem} What is the resulting concentration?"
    options, key = pack(correct, ["15%", "40%", "10%", "35%"], qid)
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def folders_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((16, 5), (18, 4), (15, 6), (22, 3), (14, 5))
    rate, hours = setups[qid % len(setups)]
    answer = rate * hours
    stem = f"Team {qid + 1} files {rate} folders an hour. At that rate, how many folders can it file in {hours} hours?"
    options, key = pack(str(answer), [str(rate + hours), str(answer - rate), str(rate * (hours - 1)), str(hours * 10)], qid)
    work = f"{rate} times {hours} is {answer}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def remain_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((48, 3, 4), (36, 2, 3), (40, 3, 5), (60, 3, 4), (42, 5, 6))
    pages, num, den = setups[qid % len(setups)]
    used = pages // den * num
    left = pages - used
    stem = f"Report {qid + 1} uses {num}/{den} of a {pages}-page allotment. How many pages are left?"
    options, key = pack(str(left), [str(used), str(pages // den), str(left + den), str(num * den)], qid)
    work = f"{num}/{den} of {pages} is {used}. {pages} minus {used} is {left}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def equal_boxes_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((8, 192), (6, 144), (5, 125), (9, 108), (7, 84))
    boxes, total = setups[qid % len(setups)]
    each = total // boxes
    stem = f"Set {qid + 1}: {boxes} equal boxes hold {total} forms in all. How many forms are in each box?"
    options, key = pack(str(each), [str(each + boxes), str(total // 2), str(boxes), str(each - 1 if each > 1 else each + 3)], qid)
    work = f"{total} divided by {boxes} is {each}."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])


def tasks_problem(qid: int) -> tuple[str, list[str], int, str]:
    setups = ((24, 5), (18, 3), (30, 4), (21, 4), (27, 6))
    total, more = setups[qid % len(setups)]
    if total % 3:
        raise ValueError(total)
    first = total * 2 // 3
    left = total - first - more
    if left <= 0:
        raise ValueError((total, more, left))
    stem = f"Checklist {qid + 1} has {total} tasks. A team finishes 2/3 in week one and {more} more in week two. How many tasks remain?"
    options, key = pack(str(left), [str(first), str(more), str(left + 2), str(total - first)], qid)
    work = f"Two-thirds of {total} is {first}. After {more} more, {first + more} are done and {left} remain."
    return stem, options, key, explain(options[key], work, [o for i, o in enumerate(options) if i != key])
