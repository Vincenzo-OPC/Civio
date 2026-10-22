"""Independent key check for the 22 Oct 2026 drafts. qa.check_item calls solve(it) for items that carry a `recipe`.
Arithmetic recipes: every number named in recipe.args must appear in the stem text, and the key is recomputed here with
its own formula (not the generator's code), then formatted. Returns the expected key text, or None when it cannot check.
Recipe "table" items (analogies, judgment items) return the answer recorded in TABLES, a hand-keyed answer sheet kept
apart from the option shuffle; those still need a human review and are reported as such."""
import re
from fractions import Fraction as F
from math import ceil, gcd

TABLES = {}


def _num(x):
    x = F(x)
    return f"{int(x):,}" if x.denominator == 1 else f"{float(x):,.2f}".rstrip("0").rstrip(".")


def _frac(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, r = divmod(x.numerator, x.denominator)
    return f"{w} {F(r, x.denominator)}" if w else f"{x.numerator}/{x.denominator}"


def _peso(x):
    x = F(x)
    return f"₱{int(x):,}" if x.denominator == 1 else f"₱{float(x):,.2f}"


def _hm(m):
    return f"{m // 60} hours {m % 60} minutes" if m % 60 else f"{m // 60} hours"


def _forms(v):
    v = F(v)
    out = {str(v), _num(v), str(float(v)) if v.denominator != 1 else str(int(v))}
    if v.denominator != 1:
        out.add(f"{v.numerator}/{v.denominator}")
        w, r = divmod(v.numerator, v.denominator)
        if w:
            out.add(f"{w} {F(r, v.denominator)}")
    return out


def _in(stem, v):
    s = stem.replace("−", "-")
    for f in _forms(abs(F(v))):
        if re.search(r"(?<![\d/.])" + re.escape(f) + r"(?![\d/]|\.\d)", s):
            return True
    words = {1: "one", 2: "two|twice|half", 3: "three|tripled|third", 4: "four|fourth", 5: "five", 6: "six", 10: "ten"}
    if abs(F(v)) == F(1, 2) and re.search(r"\bhalf\b", s, re.I):
        return True
    return abs(F(v)) in words and re.search(r"\b(" + words[abs(F(v))] + r")\b", s, re.I) is not None


def _need(stem, *vals):
    for v in vals:
        if isinstance(v, (list, tuple)):
            _need(stem, *v)
        elif not _in(stem, v):
            raise LookupError(f"{v} not in stem")


def compute(op, a, stem):
    if op == "frac_rest2":
        _need(stem, a["total"], a["f1"], a["f2"])
        r = F(a["total"]) * (1 - F(a["f1"]))
        return r * (1 - F(a["f2"]))
    if op == "frac_add":
        _need(stem, a["f1"], a["f2"]); return F(a["f1"]) + F(a["f2"])
    if op == "frac_sub":
        _need(stem, a["a"], a["b"]); return F(a["a"]) - F(a["b"])
    if op == "frac_of":
        _need(stem, a["total"], a["f"]); return F(a["f"]) * a["total"]
    if op == "frac_div":
        _need(stem, a["total"], a["f"]); return F(a["total"]) / F(a["f"])
    if op == "frac_whole":
        _need(stem, a["part"], a["f"]); return F(a["part"]) / F(a["f"])
    if op == "frac_mul":
        _need(stem, a["f1"], a["f2"]); return F(a["f1"]) * F(a["f2"])
    if op == "frac_max":
        _need(stem, *a["fs"]); return max(F(x) for x in a["fs"])
    if op == "ratio_share":
        _need(stem, a["total"], *a["parts"]); return F(a["total"]) * a["parts"][a["idx"]] / sum(a["parts"])
    if op == "ratio_part":
        _need(stem, a["known"], *a["parts"]); p = a["parts"]; return F(a["known"]) / p[a["ki"]] * p[1 - a["ki"]]
    if op == "ratio_diff":
        _need(stem, a["diff"], *a["parts"]); p = a["parts"]; return F(a["diff"]) / (p[0] - p[1]) * p[0]
    if op == "ratio_chain":
        _need(stem, *a["ab"], *a["bc"]); x, y = a["ab"][0] * a["bc"][0], a["ab"][1] * a["bc"][1]; g = gcd(x, y)
        return f"{x // g} : {y // g}"
    if op == "mul":
        _need(stem, a["a"], a["b"]); return F(a["a"]) * F(a["b"])
    if op == "proportion":
        _need(stem, a["a"], a["b"], a["c"]); return F(a["a"]) * a["c"] / a["b"]
    if op == "lin":
        _need(stem, a["b"], a["c"]); return (F(a["c"]) - F(a["b"])) / F(a["a"])
    if op == "lin2":
        m = re.search(r"(\d+)\((\w) ([+−]) (\d+)\) = (\d+)\w ([+−]) (\d+)", stem)
        p, s1, q, r, s2, t = int(m.group(1)), m.group(3), int(m.group(4)), int(m.group(5)), m.group(6), int(m.group(7))
        q = q if s1 == "+" else -q
        t = t if s2 == "+" else -t
        return F(t - p * q, p - r)
    if op == "consec":
        _need(stem, a["total"]); n, st = a["count"], a["step"]
        lo = F(a["total"] - st * n * (n - 1) // 2, n)
        return lo + st * (n - 1) if a["want"] == "largest" else lo
    if op == "multiple":
        _need(stem, a["k"], a["total"]); return F(a["total"], a["k"] + 1)
    if op == "coins":
        _need(stem, a["count"], a["value"])
        hi = F(a["value"] - a["d1"] * a["count"], a["d2"] - a["d1"])
        return hi if a["want"] == a["d2"] else a["count"] - hi
    if op == "age":
        _need(stem, a["k"], a["years"]); return F(a["years"], a["k"] - 2)
    if op == "change":
        _need(stem, a["paid"], *[x for pair in a["items"] for x in pair]); return a["paid"] - sum(q * p for q, p in a["items"])
    if op == "elapsed":
        h1, m1 = a["start"]; h2, m2 = a["end"]
        _need(stem, m1 if m1 else h1)
        return (h2 * 60 + m2) - (h1 * 60 + m1) - a["brk"]
    if op == "travel_time":
        _need(stem, a["d"], a["v"]); return int(F(a["d"], a["v"]) * 60)
    if op == "together":
        _need(stem, a["a"], a["b"]); return 1 / (F(1, a["a"]) + F(1, a["b"]))
    if op == "avg_missing":
        _need(stem, a["target"], *a["scores"]); return a["target"] * (len(a["scores"]) + 1) - sum(a["scores"])
    if op == "ceil_div":
        _need(stem, a["need"], a["pack"]); return ceil(F(a["need"], a["pack"]))
    if op == "posts":
        _need(stem, a["length"], a["gap"]); return a["length"] // a["gap"] + 1
    if op == "installment":
        _need(stem, a["price"], a["down"], a["months"]); return F(a["price"] - a["down"], a["months"])
    if op == "expr":
        # a["expr"] is arithmetic over numbers that must all appear in the stem
        nums = re.findall(r"\d+(?:\.\d+)?", a["expr"])
        _need(stem, *[F(x) for x in nums])
        return eval(re.sub(r"(\d+(?:\.\d+)?)", r"F('\1')", a["expr"]), {"__builtins__": {}, "F": F, "ceil": ceil, "max": max, "min": min})
    if op == "table":
        return TABLES.get(a["key"])
    raise KeyError(op)


def fmt(v, r):
    f = r.get("fmt", "num")
    if isinstance(v, str):
        return v
    if f == "num":
        return _num(v)
    if f == "peso":
        return _peso(v)
    if f == "frac":
        return _frac(v)
    if f == "fracraw":
        v = F(v); return f"{v.numerator}/{v.denominator}"
    if f == "unit":
        return f"{_num(v)} {r['unit']}"
    if f == "hm":
        return _hm(int(v))
    if f == "pre":
        return r["pre"] + _num(v) + r.get("post", "")
    return str(v)


def solve(it):
    r = it.get("recipe")
    if not r:
        return None
    try:
        v = compute(r["op"], r.get("args", {}), it["stem"])
    except (LookupError, KeyError, AttributeError, ZeroDivisionError, TypeError, ValueError):
        return None
    return None if v is None else fmt(v, r)


def _seq_next(xs):
    """Next term of an integer series, found by trying simple rules; None unless exactly one distinct prediction."""
    cands = set()
    d = [b - a for a, b in zip(xs, xs[1:])]
    if len(set(d)) == 1:
        cands.add(xs[-1] + d[0])
    dd = [b - a for a, b in zip(d, d[1:])]
    if len(set(dd)) == 1 and len(set(d)) > 1:
        cands.add(xs[-1] + d[-1] + dd[0])
    ddd = [b - a for a, b in zip(dd, dd[1:])]
    if len(ddd) >= 2 and len(set(ddd)) == 1 and len(set(dd)) > 1:
        cands.add(xs[-1] + d[-1] + dd[-1] + ddd[0])
    if all(a != 0 for a in xs):
        r = {F(b, a) for a, b in zip(xs, xs[1:])}
        if len(r) == 1 and r != {1}:
            v = xs[-1] * r.pop()
            if v.denominator == 1:
                cands.add(int(v))
    for m in (2, 3):
        c = {b - m * a for a, b in zip(xs, xs[1:])}
        if len(c) == 1 and len(set(d)) > 1:
            cands.add(xs[-1] * m + c.pop())
    ev, od = xs[0::2], xs[1::2]
    if len(ev) >= 3 and len(od) >= 2:
        de, do = {b - a for a, b in zip(ev, ev[1:])}, {b - a for a, b in zip(od, od[1:])}
        if len(de) == 1 and len(do) == 1 and de != do:
            cands.add((ev[-1] + de.pop()) if len(xs) % 2 == 0 else (od[-1] + do.pop()))
    if len(xs) >= 4 and all(xs[k] == xs[k - 1] + xs[k - 2] for k in range(2, len(xs))):
        cands.add(xs[-1] + xs[-2])
    if all(x > 0 and round(x ** (1 / 3)) ** 3 == x for x in xs) and [round(x ** (1 / 3)) for x in xs] == list(range(round(xs[0] ** (1 / 3)), round(xs[0] ** (1 / 3)) + len(xs))):
        cands.add((round(xs[-1] ** (1 / 3)) + 1) ** 3)
    return cands.pop() if len(cands) == 1 else None


def _table(stem):
    body = stem.rsplit("\n\n", 1)[0]
    grid = [l for l in body.split("\n") if " | " in l]
    head = [c.strip() for c in grid[0].split("|")][1:]
    rows = {}
    for l in grid[1:]:
        cells = [c.strip() for c in l.split("|")]
        rows[cells[0]] = [F(c.replace(",", "").replace("₱", "")) for c in cells[1:]]
    return head, rows


def _tbl(a, stem):
    head, rows = _table(stem)
    q = stem.rsplit("\n\n", 1)[1]
    for nm in a.get("rows", []) + a.get("cols", []):
        if nm.lower() not in q.lower():
            raise LookupError(f"{nm} not named in the question")
    col = lambda c: [rows[r][head.index(c)] for r in rows]
    cell = lambda r, c: rows[r][head.index(c)]
    do = a["do"]
    if do == "cell_diff":
        (r1, c1), (r2, c2) = a["cells"]; return cell(r1, c1) - cell(r2, c2)
    if do == "row_sum":
        return sum(rows[a["rows"][0]])
    if do == "col_sum":
        return sum(col(a["cols"][0]))
    if do == "row_avg":
        return F(sum(rows[a["rows"][0]]), len(head))
    if do == "col_avg":
        return F(sum(col(a["cols"][0])), len(rows))
    if do == "argmax_col":
        v = col(a["cols"][0]); m = max(v)
        assert v.count(m) == 1; return list(rows)[v.index(m)]
    if do == "argmin_col":
        v = col(a["cols"][0]); m = min(v)
        assert v.count(m) == 1; return list(rows)[v.index(m)]
    if do == "argmax_rowsum":
        s = {r: sum(v) for r, v in rows.items()}; m = max(s.values())
        assert list(s.values()).count(m) == 1; return max(s, key=s.get)
    if do == "col_range":
        v = col(a["cols"][0]); return max(v) - min(v)
    if do == "two_col_diff_total":
        c1, c2 = a["cols"]; return sum(col(c1)) - sum(col(c2))
    if do == "count_above":
        return sum(1 for x in col(a["cols"][0]) if x > a["t"])
    if do == "times":
        (r1, c1), (r2, c2) = a["cells"]; return cell(r1, c1) / cell(r2, c2)
    if do == "cost":
        (r1, c1) = a["cells"][0]; return cell(r1, c1) * F(a["price"])
    raise KeyError(do)


_compute0 = compute


def compute(op, a, stem):  # noqa: F811  (extends the arithmetic ops above)
    if op == "seq":
        body = stem.split("___")[0]
        body = body.split(":", 1)[1] if ":" in body else body.split("?", 1)[-1]
        xs = [int(x) for x in re.findall(r"-?\d+", body)]
        return _seq_next(xs)
    if op == "tbl":
        return _tbl(a, stem)
    return _compute0(op, a, stem)
