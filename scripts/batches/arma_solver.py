"""Independent ARMA (ANSI/ARMA 12-2005 simplified rules) solver used by qa.py to recompute filing keys.
Covers stems in the newline format: '<question>?\\nA | B | C | D' (rank asked: FIRST, SECOND, THIRD, LAST)
or '<question>?\\n1. A\\n2. B\\n3. C\\n4. D' (key is the sequence, for example '3, 1, 4, 2').
'business' or 'organization' in the question selects business indexing; otherwise personal names.
Written separately from the gap-fill generator so a hand-assigned key is checked by a second implementation."""
import re

TITLES = {"dr", "atty", "engr", "mr", "mrs", "ms", "hon", "prof"}
ROMAN = {"ii": 2, "iii": 3, "iv": 4}
SUFFIX = {"jr", "sr", "cpa"} | set(ROMAN)
PREFIX = {"de", "del", "dela", "delos", "des", "di", "da", "la", "las", "los", "san", "santa", "sta", "van", "von", "der", "le", "du"}


def clean(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def unit(t):
    c = clean(t)
    m = re.fullmatch(r"(\d+)(st|nd|rd|th)?", c)
    return (0, int(m.group(1)), "") if m else (1, 0, c)


def personal(name):
    toks = name.split()
    last = None
    if clean(toks[0]) in TITLES:
        last = clean(toks.pop(0))
    if clean(toks[-1]) in SUFFIX:
        last = clean(toks.pop())
    mi = [i for i, t in enumerate(toks) if re.fullmatch(r"[A-Z]\.", t)]
    if mi:
        given, sur = toks[:mi[0] + 1], toks[mi[0] + 1:]
    else:
        p = [i for i, t in enumerate(toks) if i >= 1 and clean(t) in PREFIX]
        cut = p[0] if p else len(toks) - 1
        given, sur = toks[:cut], toks[cut:]
    units = [(1, 0, "".join(clean(t) for t in sur))] + [(1, 0, clean(t)) for t in given]
    if last:
        units.append((0, ROMAN[last], "") if last in ROMAN else (1, 0, last))
    return units


def business(name):
    toks = name.replace("&", " and ").split()
    if toks and toks[0].lower() == "the":
        toks = toks[1:] + ["the"]
    return [unit(t) for t in toks if clean(t)]


def solve(stem):
    q, body = stem.split("?\n", 1)
    idx = business if re.search(r"business|organization", q, re.I) else personal
    if re.match(r"\s*1\.\s", body):
        names = [re.sub(r"^\s*\d\.\s*", "", l).strip() for l in body.splitlines() if l.strip()]
        order = sorted(range(len(names)), key=lambda i: idx(names[i]))
        return ", ".join(str(i + 1) for i in order)
    names = [n.strip() for n in body.split(" | ")]
    order = sorted(names, key=idx)
    keys = [tuple(idx(n)) for n in names]
    if len(set(keys)) != len(keys):
        return None
    rank = {"FIRST": 0, "SECOND": 1, "THIRD": 2, "LAST": -1}[re.search(r"\b(FIRST|SECOND|THIRD|LAST)\b", q).group(1)]
    return order[rank]
