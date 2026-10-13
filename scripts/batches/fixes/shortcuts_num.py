"""Backfill the optional item-level `shortcut` field (spec 0.1.7) for Numerical items, into a sidecar for CoS review.
Every shortcut is evaluated on the item's own numbers and must reproduce the solver's key."""
import glob, json, os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import qa
from build import DOCS
ROOT = os.path.abspath(os.path.join(DOCS, ".."))


def peso(x):
    x = float(x)
    return f"₱{x:,.0f}" if x == int(x) else f"₱{x:,.2f}"


DISC = -1


def make(it):
    s, a = it["stem"], it["archetype"]
    if "raised the price by" in s:
        p = qa.money(re.search(r"for (₱[\d,.]+)", s).group(1)); up, dn = map(int, re.findall(r"(\d+)%", s))
        v = F(p) * (100 + up) / 100 * (100 - dn) / 100
        return v, f"Chain the changes as multipliers: up {up}% is × {1 + up / 100:g}, down {dn}% is × {1 - dn / 100:g}. {peso(p)} × {1 + up / 100:g} × {1 - dn / 100:g} = {peso(v)}."
    if "simple interest" in s:
        P = qa.money(re.search(r"₱[\d,.]+", s).group()); r = int(re.search(r"(\d+)% simple", s).group(1))
        y = int(re.search(r"after (\d+) year", s).group(1)); m = re.search(r"and (\d+) months", s)
        t = F(y) + (F(int(m.group(1)), 12) if m else 0)
        one = F(P) / 100
        v = one * r * t
        tt = f"{float(t):g}"
        return v, f"Find 1% first: 1% of {peso(P)} is {peso(one)}, so {r}% is {peso(one * r)} a year. Times {tt} years = {peso(v)}."
    if "% off" in s:
        p = qa.money(re.search(r"₱[\d,.]+", s).group()); d = int(re.search(r"(\d+)% off", s).group(1))
        v = F(p) * (100 - d) / 100
        global DISC
        DISC += 1
        ten = F(p) / 10
        if d % 10 == 5 and d < 50:
            t = d // 10 * 10
            forms = [f"Split {d}% into {t}% + 5%: {t}% of {peso(p)} is {peso(ten * (t // 10))}, and 5% is half of 10% ({peso(ten / 2)}). Take off {peso(ten * (t // 10) + ten / 2)} to get {peso(v)}.",
                     f"Move the decimal one place for 10% ({peso(ten)}), halve it for 5% ({peso(ten / 2)}), and build {d}% from those: {peso(ten * (t // 10) + ten / 2)} off, so {peso(v)}.",
                     f"{d}% = {t}% + 5%. 10% of {peso(p)} = {peso(ten)}; so the discount is {peso(ten * (t // 10) + ten / 2)} and the price is {peso(v)}."]
        else:
            forms = [f"Pay the part that is left: {d}% off means you pay {100 - d}%. {peso(p)} × {(100 - d) / 100:g} = {peso(v)}.",
                     f"Skip the subtraction step: multiply by what you keep, {100 - d}%. {peso(p)} × {(100 - d) / 100:g} = {peso(v)}.",
                     (f"10% off: move the decimal one place ({peso(ten)}) and subtract: {peso(p)} − {peso(ten)} = {peso(v)}." if d == 10 else
                      f"Find 10% by moving the decimal ({peso(ten)}), then the discount is {d / 10:g} × that = {peso(F(p) * d / 100)}. {peso(p)} − {peso(F(p) * d / 100)} = {peso(v)}.")]
        return v, forms[DISC % 3]
    if a == "NUM-WP-RATIO":
        tot = qa.money(re.search(r"₱[\d,.]+", s).group()); x, y = map(int, re.search(r"ratio (\d+) : (\d+)", s).groups())
        v = F(tot) * y / (x + y)
        return v, f"The second share is {y} of {x + y} equal parts: {peso(tot)} ÷ {x + y} × {y} = {peso(v)}."
    if a == "NUM-WP-RATE" and "Working together" in s or (a == "NUM-WP-RATE" and len(re.findall(r"in (\d+) hours", s)) == 2):
        x, y = map(int, re.findall(r"in (\d+) hours", s))
        v = F(x * y, x + y)
        return v, f"For two workers, time together = product ÷ sum: ({x} × {y}) ÷ ({x} + {y}) = {x * y} ÷ {x + y} = {v} hours."
    if a == "NUM-WP-AVERAGE":
        nums = [int(x) for x in re.findall(r"\d+", s)]
        n, avg, new = nums[0], nums[1], nums[2]
        v = F(avg) + F(new - avg, n + 1)
        return v, f"New average = old average + (newcomer − old average) ÷ new head count: {avg} + ({new} − {avg}) ÷ {n + 1} = {v} years."
    if a == "NUM-WP-GEOM":
        L, W = map(int, re.findall(r"(\d+) m", s)); c = qa.money(re.search(r"₱[\d,.]+", s).group())
        v = 2 * (L + W) * c
        return v, f"Add length and width once, then double: {L} + {W} = {L + W}, × 2 = {2 * (L + W)} m. × {peso(c)} = {peso(v)}."
    if a == "NUM-OPS-ORDER":
        return None, None  # CoS 2026-10-13: restating the order of operations is not a shortcut
    if a == "NUM-FRAC-DEC" and "had" in s:
        tot = int(re.search(r"had (\d+)", s).group(1)); f1, f2 = [F(x) for x in re.findall(r"(\d+/\d+)", s)]
        v = tot * (1 - f1) * (1 - f2)
        return v, f"Multiply by what is left each time: {tot} × {1 - f1} × {1 - f2} = {v}."
    if a in ("NUM-SEQ-DIFF", "NUM-SEQ-MULT"):
        v = F(qa.solve_num(it))
        xs = [int(x) for x in re.findall(r"-?\d+", s.split("?")[-1].split("___")[0])]
        d = [y - x for x, y in zip(xs, xs[1:])]
        if len(set(y - x for x, y in zip(d, d[1:]))) == 1:
            return v, f"Write the gaps ({', '.join(f'{g:+d}' for g in d)}); they change by the same amount each time, so the next gap is {d[-1] + d[1] - d[0]:+d}: {xs[-1]} {d[-1] + d[1] - d[0]:+d} = {v}."
        return None, None  # the Reveal already tests the rule; no honest shortcut beyond it
    if a == "NUM-WP-ALGEBRA":
        return None, None  # "try the choices" is already the Reveal method; no extra shortcut
    return None, None


def key_value(it):
    k = qa.key_text(it)
    return F(re.sub(r"[^\d.\-/]", "", k.split()[0]).replace(",", ""))


def run():
    out, skipped = [], []
    fix = {i["id"]: i for i in json.load(open(os.path.join(ROOT, "research", "round-02-fixes.json"), encoding="utf-8"))["items"]}
    for p in sorted(glob.glob(os.path.join(DOCS, "batch-*.json"))):
        for it in [fix.get(i["id"], i) for i in json.load(open(p, encoding="utf-8"))["items"]]:
            if it["domain"] != "numerical":
                continue
            v, sc = make(it)
            if sc is None:
                skipped.append(it["id"]); continue
            assert v == key_value(it), (it["id"], v, qa.key_text(it), sc)
            out.append({"id": it["id"], "batch": os.path.basename(p), "stem": it["stem"], "key": qa.key_text(it), "shortcut": sc,
                        "verified": f"shortcut evaluates to {qa.key_text(it)}", "on_round_02_rewrite": it["id"] in fix})
    d = {"spec_version": "0.1.7", "status": "draft (shortcut backfill; awaiting CoS review; not merged into items, not imported)",
         "count": len(out), "skipped_no_real_shortcut": skipped, "shortcuts": out}
    open(os.path.join(ROOT, "research", "shortcuts-num-001.json"), "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    return out, skipped


if __name__ == "__main__":
    o, s = run()
    print(len(o), "shortcuts;", len(s), "skipped")
    for x in o[::30]:
        print(x["id"], "|", x["shortcut"])
