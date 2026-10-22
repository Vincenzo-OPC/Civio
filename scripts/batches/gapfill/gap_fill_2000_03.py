"""gap-fill-2000-03: original Analytical drafts for the 2,000 milestone: word analogy (67) and data interpretation tables (34).
Gap per docs/research/audit/gap-2000-2026-10-18.md and release_manifest.QUOTA: analogy ~61 short, data interpretation ~31 short (+~10% buffer).
Analogy content: gf03_analogies.py. Tables: gf03_di.py (text tables; ANA-DI-CHART stays out until the image pipeline exists, spec 3.4).
Keys are recomputed by qa.solve_ana (analogy registry + di_grid solver). Drafts only.
Run: python3 scripts/batches/gapfill/gap_fill_2000_03.py  -> docs/research/gap-fill-2000-03.json"""
import json, os, random, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import gf03_analogies as A, gf03_di as G, di_grid

PROV = {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T04:30:00+08:00", "spec_version": "0.1.9"}
FRAMES = [("A1", "{A} : {B} :: ____"), ("A2", "{Ac} is to {b} as ____."), ("A3", "Which pair shows the same relationship as \"{a} : {b}\"?"),
          ("A4", "Which pair matches the link in \"{a}\" and \"{b}\"?")]
CONCEPT = {A.D: "degree", A.S: "synonym or antonym", A.P: "part and whole", A.F: "function", A.M: "word form"}
EST = {A.D: 30, A.S: 25, A.P: 30, A.F: 30, A.M: 30}
TERMS = {A.D: "In a degree analogy, the second word is a stronger or bigger form of the first.",
         A.S: "Synonyms mean nearly the same thing; antonyms are opposites. Order does not change these links, so check the link itself.",
         A.P: "In a part-and-whole analogy, the first word is one piece or member of the second.",
         A.F: "In a function analogy, the pair links a thing or worker to its use, tool, product or contents.",
         A.M: "In a word-form analogy, the second word is a grammatical form of the first (plural, tense, case, abbreviation, gender)."}


def art(w):
    return ("an " if w[0].lower() in "aeiou" else "a ") + w


def sent(t, x, y):
    s = t.format(x=x, y=y, ax=art(x), ay=art(y))
    return s[0].upper() + s[1:]


def pair(p):
    return f"{p[0]} : {p[1]}"


def analogy_items():
    out, use = [], {}
    for n, (a, b, arch, diff, st, key, ds) in enumerate(A.ROWS, 1):
        k = use.get(arch, 0); use[arch] = k + 1
        fid, tpl = FRAMES[3 if a[0].isupper() else k % 4] if a[0].isupper() else FRAMES[k % 4]
        if a[0].isupper() and fid in ("A1", "A2"):
            fid, tpl = FRAMES[2]
        stem = tpl.format(A=a.upper(), B=b.upper(), Ac=a[0].upper() + a[1:], a=a, b=b)
        sk = sent(st, *key)
        wrong = [(pair((x, y)), c, f"\"{pair((x, y))}\" {note}. The first pair needs: {sent(st, a, b)}.") for x, y, c, note in ds]
        out.append(dict(id=f"CIVIO-GF2K03-{arch}-{n:04d}", track="pro", domain="analytical", competency="Word association (analogy)",
                        concept=CONCEPT[arch], micro_skill=("lesser : greater degree" if arch == A.D else st.replace("{ax}", "A").replace("{ay}", "B").replace("{x}", "A").replace("{y}", "B").replace('"', "")),
                        archetype=arch, difficulty=diff, est_seconds=EST[arch], language="en", stem=stem, gen_frame=f"ANA-{fid}",
                        _key=pair(key), _wrong=wrong, _terms=TERMS[arch],
                        _short=f"Say the link of the first pair as a sentence: {sent(st, a, b)}. Then put each choice into the same sentence" + ("." if arch == A.S else ", in the same order."),
                        _why=f"\"{pair(key)}\" is right: {sk}. That is the same link as the first pair" + ("." if arch == A.S else ", in the same order.")))
    return out


def f(x):
    return di_grid.fmt(x)


def di_items():
    out = []
    for n, (title, rh, cols, rows, q, kind, args, diff, wt) in enumerate(G.DI, 1):
        R = {r: [Fr(str(v)) for v in vs] for r, vs in rows}; order = [r for r, _ in rows]; ci = {c: i for i, c in enumerate(cols)}
        col = lambda c: [R[r][ci[c]] for r in order]
        money = "peso" in title.lower(); scaled = "thousands" in title.lower() and "in pesos" in q.lower()
        fac = 1000 if scaled else 1
        amt = lambda v, s=fac: ("₱" if money else "") + f(v * s)
        pct = lambda v: f(v) + "%"
        cell = lambda r, c: R[r][ci[c]]
        tab = lambda v: f(v)
        W = []
        if kind in ("sumcol", "sumrow"):
            vals = col(args[0]) if kind == "sumcol" else R[args[0]]
            S = sum(vals); key = amt(S)
            plus = " + ".join(tab(v) for v in vals)
            what = f"the {args[0]} column" if kind == "sumcol" else f"the {args[0]} row"
            sc = f"Read {what} only and add: {plus}." + (" The table is in thousands of pesos, so multiply the sum by 1,000." if scaled else "")
            why = f"{key} is right: add only {what}: {plus} = {tab(S)}" + (f" thousand pesos, which is {key}." if scaled else ".")
            for t in wt:
                if t.startswith("othercol:") or t.startswith("otherrow:"):
                    o = t.split(":", 1)[1]; ov = col(o) if kind == "sumcol" else R[o]
                    W.append((amt(sum(ov)), "DI-WRONG-CELL", f"This adds the {o} {'column' if kind == 'sumcol' else 'row'}, not {args[0]}."))
                elif t == "partial":
                    W.append((amt(sum(vals[:-1])), "NUM-PARTIAL", f"This leaves out the last {'row' if kind == 'sumcol' else 'column'} ({tab(vals[-1])})."))
                elif t == "avg":
                    W.append((amt(S / len(vals)), "NUM-EXTRA-STEP", f"This divides the total by {len(vals)}, giving the average. The question asks for the total."))
                elif t == "scale":
                    W.append((amt(S, 1), "DI-SCALE", "This ignores \"in thousands of pesos\" in the title and gives the table figure as pesos."))
            terms = "A column runs down the table; a row runs across. A total adds every value in the named row or column."
            concept, micro = "table total", f"add one {'column' if kind == 'sumcol' else 'row'}"
        elif kind == "grand":
            S = sum(sum(v) for v in R.values()); key = amt(S)
            colsums = [sum(col(c)) for c in cols]
            sc = "Add each column, then add the column totals: " + " + ".join(tab(x) for x in colsums) + "."
            why = f"{key} is right: " + "; ".join(f"{c} = {' + '.join(tab(v) for v in col(c))} = {tab(sum(col(c)))}" for c in cols) + f"; {' + '.join(tab(x) for x in colsums)} = {tab(S)}."
            for t in wt:
                if t.startswith("onecol:"):
                    o = t.split(":", 1)[1]; W.append((amt(sum(col(o))), "NUM-PARTIAL", f"This adds only the {o} column and stops before the other quarter."))
                elif t.startswith("onerow:"):
                    o = t.split(":", 1)[1]; W.append((amt(sum(R[o])), "DI-WRONG-CELL", f"This adds only the {o} row, not every cause."))
                elif t == "avg":
                    W.append((amt(S / len(cols)), "NUM-EXTRA-STEP", f"This divides the grand total by {len(cols)}, giving a per-quarter average."))
            terms = "A grand total adds every value in the table, across all rows and all columns."
            concept, micro = "table total", "add the whole table"
        elif kind in ("avgcol", "avgrow"):
            vals = col(args[0]) if kind == "avgcol" else R[args[0]]
            S = sum(vals); m = len(vals); key = amt(S / m)
            plus = " + ".join(tab(v) for v in vals)
            sc = f"Average = total ÷ number of values. There are {m} values in {'the ' + args[0] + ' column' if kind == 'avgcol' else 'the ' + args[0] + ' row'}; count them before dividing."
            why = f"{key} is right: {plus} = {tab(S)}, and {tab(S)} ÷ {m} = {tab(S / m)}" + (f" thousand pesos, which is {key}." if scaled else ".")
            for t in wt:
                if t == "total":
                    W.append((amt(S), "NUM-PARTIAL", f"This is the total ({tab(S)}). It stops before dividing by {m}."))
                elif t == "nminus":
                    W.append((amt(S / (m - 1)), "NUM-OFF-BY-ONE", f"This divides by {m - 1} instead of {m}: one value was left out of the count."))
                elif t.startswith("othercol:") or t.startswith("otherrow:"):
                    o = t.split(":", 1)[1]; ov = col(o) if kind == "avgcol" else R[o]
                    W.append((amt(sum(ov) / len(ov)), "DI-WRONG-CELL", f"This is the average for {o}, not {args[0]}."))
                elif t == "scale":
                    W.append((amt(S / m, 1), "DI-SCALE", "This ignores \"in thousands of pesos\" in the title."))
            terms = "The average (mean) is the total of the values divided by how many values there are."
            concept, micro = "table average", f"average one {'column' if kind == 'avgcol' else 'row'}"
        elif kind == "diff":
            mode = args[0]
            if mode == "r":
                r1, r2, c = args[1:]; a_, b_ = cell(r1, c), cell(r2, c); where = f"the {c} column: {r1} {tab(a_)}, {r2} {tab(b_)}"
            elif mode == "c":
                r, c1, c2 = args[1:]; a_, b_ = cell(r, c1), cell(r, c2); where = f"the {r} row: {c1} {tab(a_)}, {c2} {tab(b_)}"
            else:
                r1, r2 = args[1:]; a_, b_ = sum(R[r1]), sum(R[r2]); where = f"the row totals: {r1} {' + '.join(tab(v) for v in R[r1])} = {tab(a_)}, {r2} {' + '.join(tab(v) for v in R[r2])} = {tab(b_)}"
            D = abs(a_ - b_); key = amt(D)
            sc = (f"Find both numbers in the {c} column first, then subtract the smaller from the larger." if mode == "r" else
                  f"Stay in the {r} row: find both numbers, then subtract." if mode == "c" else
                  "Add each row across all the months first, then subtract the two totals.")
            why = f"{key} is right: {where}; {tab(max(a_, b_))} − {tab(min(a_, b_))} = {tab(D)}" + (f" thousand pesos, which is {key}." if scaled else ".")
            for t in wt:
                if t == "sum":
                    W.append((amt(a_ + b_), "NUM-OP-SWAP", "This adds the two numbers instead of subtracting them."))
                elif t.startswith("othercol:"):
                    o = t.split(":", 1)[1]; W.append((amt(abs(cell(r1, o) - cell(r2, o))), "DI-WRONG-CELL", f"This compares the {o} column, not {c}."))
                elif t.startswith("otherrow:"):
                    o = t.split(":", 1)[1]; W.append((amt(abs(cell(o, c1) - cell(o, c2))), "DI-WRONG-CELL", f"This uses the {o} row, not {r}."))
                elif t == "totals":
                    if mode == "r":
                        W.append((amt(abs(sum(R[r1]) - sum(R[r2]))), "DI-WRONG-CELL", f"This compares the row totals for all columns, not only {c}."))
                    else:
                        W.append((amt(abs(sum(col(c1)) - sum(col(c2)))), "DI-WRONG-CELL", f"This compares the column totals for every row, not only {r}."))
                elif t.startswith("onecol:"):
                    o = t.split(":", 1)[1]; W.append((amt(abs(cell(r1, o) - cell(r2, o))), "DI-WRONG-CELL", f"This compares {o} only, not the three months combined."))
                elif t.startswith("otherpair:"):
                    o = t.split(":", 1)[1]; W.append((amt(abs(sum(R[r1]) - sum(R[o]))), "DI-WRONG-CELL", f"This compares {r1} with {o}, not with {r2}."))
                elif t == "scale":
                    W.append((amt(D, 1), "DI-SCALE", "This ignores \"in thousands of pesos\" in the title."))
            terms = "\"How many more\" and \"how much more\" ask for a difference: subtract the smaller value from the larger one."
            concept, micro = "table difference", {"r": "compare two rows in one column", "c": "compare two columns in one row", "rt": "compare two row totals"}[mode]
        elif kind == "pchg":
            (ra, ca), (rb, cb) = args; a_, b_ = cell(ra, ca), cell(rb, cb); D = abs(b_ - a_)
            up = b_ > a_; key = pct(D * 100 / a_)
            other_axis = "col" if ra == rb else "row"
            sc = "Percent change = (new − old) ÷ old × 100. The old (earlier) value is always the base."
            why = f"{key} is right: the change is {tab(max(a_, b_))} − {tab(min(a_, b_))} = {tab(D)}, and {tab(D)} ÷ {tab(a_)} = {f(D / a_)}, which is {key}."
            for t in wt:
                if t == "newbase":
                    W.append((pct(D * 100 / b_), "DI-WRONG-BASE", f"This divides the change ({tab(D)}) by the newer value ({tab(b_)}) instead of the older one ({tab(a_)})."))
                elif t == "ratio":
                    W.append((pct(b_ * 100 / a_), "NUM-PARTIAL", f"This is {tab(b_)} ÷ {tab(a_)} = {f(b_ / a_)}, the new value as a percent of the old one. It stops before taking away 100%."))
                elif t.startswith("other:"):
                    o = t.split(":", 1)[1]
                    if other_axis == "col":
                        oa, ob = cell(o, ca), cell(o, cb)
                    else:
                        oa, ob = cell(ra, o), cell(rb, o)
                    W.append((pct(abs(ob - oa) * 100 / oa), "DI-WRONG-CELL", f"This is the change for {o} ({tab(oa)} to {tab(ob)}), not {ra if other_axis == 'col' else ca}."))
            terms = "Percent increase or decrease compares the change with the starting value: change ÷ old × 100."
            concept, micro = "percent change", "percent change from a table"
        elif kind == "share":
            r, c, base = args; v = cell(r, c)
            B = sum(R[r]) if base == "row" else sum(col(c)); key = pct(v * 100 / B)
            bl = (f"{r}'s row total = {' + '.join(tab(x) for x in R[r])} = {tab(B)}" if base == "row" else f"the {c} column total = {' + '.join(tab(x) for x in col(c))} = {tab(B)}")
            sc = f"Part ÷ whole × 100. The whole is {'the ' + r + ' row total' if base == 'row' else 'the ' + c + ' column total'}."
            why = f"{key} is right: the part is {tab(v)}; {bl}; {tab(v)} ÷ {tab(B)} = {f(v / B)}, which is {key}."
            for t in wt:
                if t == "grand":
                    G_ = sum(sum(x) for x in R.values()); W.append((pct(v * 100 / G_), "DI-WRONG-BASE", f"This divides by the whole table ({tab(G_)}) instead of {'the row' if base == 'row' else 'the ' + c + ' column'} total."))
                elif t == "colbase":
                    Cb = sum(col(c)); W.append((pct(v * 100 / Cb), "DI-WRONG-BASE", f"This divides by the {c} column total ({tab(Cb)}), which answers a different question: {r}'s share of all {c.lower()}."))
                elif t.startswith("othercol:"):
                    o = t.split(":", 1)[1]
                    ob = sum(R[r]) if base == "row" else sum(col(o))
                    W.append((pct(cell(r, o) * 100 / ob), "DI-WRONG-CELL", f"This uses the {o} {'value' if base == 'row' else 'column'} instead of {c}."))
                elif t.startswith("other:"):
                    o = t.split(":", 1)[1]; W.append((pct(cell(o, c) * 100 / B), "DI-WRONG-CELL", f"This uses the {o} row instead of {r}."))
            terms = "\"What percent of\" asks for a share: part ÷ whole × 100. Choose the whole the question names."
            concept, micro = "percent share", "share of a row or column total"
        elif kind == "rowshare":
            r = args[0]; v = sum(R[r]); G_ = sum(sum(x) for x in R.values()); key = pct(v * 100 / G_)
            sc = f"Part ÷ whole × 100. The part is the whole {r} row; the whole is every row added together."
            why = f"{key} is right: {r} = {' + '.join(tab(x) for x in R[r])} = {tab(v)}; all districts = {tab(G_)}; {tab(v)} ÷ {tab(G_)} = {f(v / G_)}, which is {key}."
            for t in wt:
                if t == "others":
                    W.append((pct(v * 100 / (G_ - v)), "DI-WRONG-BASE", f"This divides by the other districts only ({tab(G_ - v)}), not by the whole city total ({tab(G_)})."))
                elif t.startswith("other:"):
                    o = t.split(":", 1)[1]; W.append((pct(sum(R[o]) * 100 / G_), "DI-WRONG-CELL", f"This is the share for {o}, not {r}."))
                elif t.startswith("colonly:"):
                    o = t.split(":", 1)[1]; W.append((pct(cell(r, o) * 100 / sum(col(o))), "DI-WRONG-CELL", f"This is {r}'s share of {o.lower()} garbage only ({tab(cell(r, o))} ÷ {tab(sum(col(o)))}), not of all garbage."))
            terms = "\"What percent of\" asks for a share: part ÷ whole × 100. Here the part is a whole row."
            concept, micro = "percent share", "row share of the grand total"
        elif kind == "ratio":
            mode = args[0]
            if mode == "c":
                r, c1, c2 = args[1:]; a_, b_ = cell(r, c1), cell(r, c2); names = (c1, c2)
            else:
                c, r1, r2 = args[1:]; a_, b_ = cell(r1, c), cell(r2, c); names = (r1, r2)
            from math import gcd
            g = gcd(int(a_), int(b_)); key = f"{int(a_) // g} : {int(b_) // g}"
            sc = "Write the two numbers in the order the question names them, then divide both by their greatest common factor."
            why = f"{key} is right: {names[0]} {tab(a_)} and {names[1]} {tab(b_)}; {tab(a_)} : {tab(b_)}, and dividing both by {g} gives {key}."
            for t in wt:
                if t == "reversed":
                    W.append((f"{int(b_) // g} : {int(a_) // g}", "NUM-WRONG-BASE", f"This is the right ratio in the wrong order: {names[1]} to {names[0]}."))
                elif t == "partwhole":
                    h = gcd(int(a_), int(a_ + b_)); W.append((f"{int(a_) // h} : {int(a_ + b_) // h}", "NUM-WRONG-BASE", f"This compares {names[0]} with the two groups combined ({tab(a_ + b_)}), not with {names[1]}."))
                elif t.startswith("otherrow:"):
                    o = t.split(":", 1)[1]; x, y = cell(o, c1), cell(o, c2); h = gcd(int(x), int(y)); W.append((f"{int(x) // h} : {int(y) // h}", "DI-WRONG-CELL", f"This uses the {o} row ({tab(x)} : {tab(y)}), not {r}."))
                elif t.startswith("othercol:"):
                    o = t.split(":", 1)[1]
                    if mode == "c":
                        x, y = cell(r, c1), cell(r, o)
                        msg = f"This compares {c1} with {o} ({tab(x)} : {tab(y)}), not with {c2}."
                    else:
                        x, y = cell(r1, o), cell(r2, o)
                        msg = f"This uses the {o} column ({tab(x)} : {tab(y)}), not {c}."
                    h = gcd(int(x), int(y)); W.append((f"{int(x) // h} : {int(y) // h}", "DI-WRONG-CELL", msg))
            terms = "A ratio compares two amounts in a fixed order. \"A to B\" puts A first."
            concept, micro = "ratio", "ratio from a table, in lowest terms"
        elif kind == "arg":
            key = args[0]; W = list(wt)
            q_l = q.lower()
            if "percent increase" in q_l:
                c1, c2 = cols
                why = f"{key} is right: " + "; ".join(f"{r} {tab(R[r][1] - R[r][0])} ÷ {tab(R[r][0])} = {pct((R[r][1] - R[r][0]) * 100 / R[r][0])}" for r in order) + f". {key} has the largest percent increase."
                sc = "Percent increase = (new − old) ÷ old. A big increase in number can still be a small percent when the starting value is large."
                concept, micro = "compare rows", "largest percent change"
            elif "increase" in q_l:
                why = f"{key} is right: increases are " + "; ".join(f"{r} {tab(R[r][1])} − {tab(R[r][0])} = {tab(R[r][1] - R[r][0])}" for r in order) + f". {key} gained the most."
                sc = "Subtract the earlier column from the later one for every row, then compare the differences, not the totals."
                concept, micro = "compare rows", "largest increase"
            elif "combined" in q_l:
                why = f"{key} is right: totals are " + "; ".join(f"{r} {' + '.join(tab(v) for v in R[r])} = {tab(sum(R[r]))}" for r in order) + f". {key} has the highest total."
                sc = "Add each row first, then compare the totals. One big month does not decide it."
                concept, micro = "compare rows", "highest row total"
            else:
                c = [x for x in cols if x.lower() in q_l][0]
                why = f"{key} is right: in {c}, " + ", ".join(f"{r} {tab(cell(r, c))}" for r in order) + f". The fewest is {key} with {tab(cell(key, c))}."
                sc = f"Look only at the {c} column, and check whether the question asks for the most or the fewest."
                concept, micro = "compare rows", "lowest value in one column"
            terms = "A column runs down the table; a row runs across. Read only the rows and columns the question names."
        assert len(W) == 3, (n, W)
        lines = [title, " | ".join([rh] + cols)] + [" | ".join([r] + [tab(v) if v < 1000 else f"{int(v):,}" for v in R[r]]) for r in order]
        stem = "\n".join(lines) + "\n\n" + q
        solved = di_grid.solve(stem)
        assert solved == key, (n, solved, key)
        texts = [key] + [w[0] for w in W]
        assert len(set(texts)) == 4, (n, texts)
        out.append(dict(id=f"CIVIO-GF2K03-ANA-DI-TABLE-{n:04d}", track="pro", domain="analytical", competency="Data interpretation",
                        concept=concept, micro_skill=micro, archetype="ANA-DI-TABLE", difficulty=diff, est_seconds=75, language="en", stem=stem,
                        _key=key, _wrong=W, _terms=terms, _short=sc, _why=why))
    return out


def finish(items, seed=20261018):
    rng = random.Random(seed)
    slots = []
    for grp in (True, False):  # balance A-D separately for analogy and table items
        g = [i % 4 for i in range(sum((it["archetype"] == "ANA-DI-TABLE") == grp for it in items))]; rng.shuffle(g); slots.append(iter(g))
    slots = [next(slots[0] if it["archetype"] == "ANA-DI-TABLE" else slots[1]) for it in items]
    out = []
    for it, slot in zip(items, slots):
        key, W = it.pop("_key"), it.pop("_wrong")
        order = [w[0] for w in W]; order.insert(slot, key)
        ids = ["o1", "o2", "o3", "o4"]; idx = {t: ids[i] for i, t in enumerate(order)}
        frame = it.pop("gen_frame", None)
        it.update(options=[{"option_id": ids[i], "text": t} for i, t in enumerate(order)], answer_option_id=idx[key],
                  reveal={"terms": it.pop("_terms"), "shortcut": it.pop("_short"), "why_correct": it.pop("_why"), "why_wrong": {idx[t]: why for t, c, why in W}},
                  distractor_reasoning={idx[t]: c for t, c, why in W}, source="Original, Civio", source_url=None, source_group="civio",
                  status="draft", review_status="unreviewed", provenance=dict(PROV),
                  notes="gap-fill-2000-03 (Analytical). Invented practice figures; no real office or place is described. Pending CoS.")
        if frame:
            it["gen_frame"] = frame
        out.append(it)
    return out


if __name__ == "__main__":
    items = finish(analogy_items() + di_items())
    json.dump({"batch": "gap-fill-2000-03", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio",
               "notes": "Analytical gap fill for the 2,000 milestone: word analogy (all five relation types) and data interpretation (text tables).", "items": items},
              open(os.path.join(ROOT, "docs/research/gap-fill-2000-03.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(items), Counter(i["archetype"] for i in items), Counter([o["option_id"] for o in i["options"]].index(i["answer_option_id"]) for i in items))
