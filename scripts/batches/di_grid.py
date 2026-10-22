"""Independent solver for pipe-table data-interpretation stems (ANA-DI-TABLE, gap-fill-2000-03 format).
Stem layout: title line, header 'RowHead | Col1 | Col2 ...', one line per row, blank line, question.
The key is recomputed from the stem text only: rows/columns named in the question are found by whole-word match,
the operation by keywords. Returns the canonical answer text, or None if the stem is not in this format."""
import re
from fractions import Fraction as F
from math import gcd


def parse(stem):
    if "\n\n" not in stem or " | " not in stem:
        return None
    body, q = stem.rsplit("\n\n", 1)
    lines = body.split("\n")
    title, grid = lines[0], [l for l in lines[1:] if " | " in l]
    head = [c.strip() for c in grid[0].split("|")]
    rows = []
    for l in grid[1:]:
        cells = [c.strip() for c in l.split("|")]
        rows.append((cells[0], [F(c.replace(",", "").replace("₱", "")) for c in cells[1:]]))
    return title, head[1:], rows, q.strip()


def fmt(x):
    x = F(x)
    if x.denominator == 1:
        return f"{int(x):,}"
    s = f"{float(x):,.2f}".rstrip("0").rstrip(".")
    return s


def find(names, q):
    hits = []
    for n in names:
        base = n[:-1] if n.endswith("s") and len(n) > 3 else n
        m = re.search(r"(?<![\w.])" + re.escape(base) + r"(?:s|'s)?(?![\w])", q, re.I)
        if m:
            hits.append((m.start(), n))
    return [n for _, n in sorted(hits)]


def solve(stem):
    p = parse(stem)
    if not p:
        return None
    title, cols, rows, q = p
    ql = q.lower()
    R = dict(rows)
    ci = {c: i for i, c in enumerate(cols)}
    cs, rs = find(cols, q), find([r for r, _ in rows], q)
    money = "peso" in title.lower()
    factor = 1000 if ("thousands" in title.lower() and "in pesos" in ql) else 1
    def amt(v):
        return ("₱" if money else "") + fmt(v * factor)
    def pct(v):
        return fmt(v) + "%"
    colv = lambda c: [R[r][ci[c]] for r, _ in rows]
    rowv = lambda r: R[r]
    if ql.startswith("which"):
        hi = any(w in ql for w in ("most", "highest", "largest", "greatest"))
        if "increase" in ql and len(cs) == 2:
            a, b = ci[cs[0]], ci[cs[1]]
            met = {r: ((v[b] - v[a]) / v[a] if "percent" in ql else v[b] - v[a]) for r, v in rows}
        elif len(cs) == 1:
            met = {r: v[ci[cs[0]]] for r, v in rows}
        else:
            met = {r: sum(v) for r, v in rows}
        best = (max if hi else min)(met.values())
        win = [r for r, m in met.items() if m == best]
        return win[0] if len(win) == 1 else None
    if "ratio of" in ql:
        if len(cs) == 2 and len(rs) == 1:
            a, b = R[rs[0]][ci[cs[0]]], R[rs[0]][ci[cs[1]]]
        elif len(rs) == 2 and len(cs) == 1:
            a, b = R[rs[0]][ci[cs[0]]], R[rs[1]][ci[cs[0]]]
        else:
            return None
        g = gcd(int(a), int(b))
        return f"{int(a) // g} : {int(b) // g}"
    if "percent" in ql and any(w in ql for w in ("increase", "decrease", "drop", "rise", "grow", "fall")):
        if len(rs) == 2 and len(cs) == 1:
            a, b = R[rs[0]][ci[cs[0]]], R[rs[1]][ci[cs[0]]]
        elif len(cs) == 2 and len(rs) == 1:
            a, b = R[rs[0]][ci[cs[0]]], R[rs[0]][ci[cs[1]]]
        else:
            return None
        return pct(abs(b - a) * 100 / a)
    if "percent of" in ql:
        if len(rs) == 1 and len(cs) == 1:
            v = R[rs[0]][ci[cs[0]]]
            base = sum(rowv(rs[0])) if "'s total" in ql or "of its total" in ql else sum(colv(cs[0]))
            return pct(v * 100 / base)
        if len(rs) == 1 and not cs:
            return pct(sum(rowv(rs[0])) * 100 / sum(sum(v) for _, v in rows))
        return None
    if "how many more" in ql or "how much more" in ql or "difference" in ql:
        if len(rs) == 2 and len(cs) == 1:
            a, b = R[rs[0]][ci[cs[0]]], R[rs[1]][ci[cs[0]]]
        elif len(cs) == 2 and len(rs) == 1:
            a, b = R[rs[0]][ci[cs[0]]], R[rs[0]][ci[cs[1]]]
        elif len(rs) == 2 and not cs:
            a, b = sum(rowv(rs[0])), sum(rowv(rs[1]))
        elif len(cs) == 2 and not rs:
            a, b = sum(colv(cs[0])), sum(colv(cs[1]))
        else:
            return None
        return amt(abs(a - b))
    if "average" in ql:
        if len(cs) == 1 and not rs:
            v = colv(cs[0])
        elif len(rs) == 1 and not cs:
            v = rowv(rs[0])
        else:
            return None
        return amt(F(sum(v), len(v)))
    if "total" in ql or "in all" in ql or "altogether" in ql:
        if len(cs) == 1 and not rs:
            return amt(sum(colv(cs[0])))
        if len(rs) == 1 and not cs:
            return amt(sum(rowv(rs[0])))
        if not cs and not rs:
            return amt(sum(sum(v) for _, v in rows))
    return None
