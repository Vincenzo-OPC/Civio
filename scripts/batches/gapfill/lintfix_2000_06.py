"""gap-fill-2000-06: explanation/lint fixes for the 247 non-English Release Collection picks that fail explanation_lint
(Filipino Verbal 39, Analytical 96, Clerical 58, General Information 54).
Each fix is a full copy of the picked item with id <orig>-LINTFIX, fix_of=<orig>, status draft / review_status unreviewed.
Originals are NOT edited and no status changes. why_correct always opens with 'Answer: <key>.' and gives the specific reason.
Generated reasons (recomputed in code, never copied): letter series, supply tables, numeric/date filing.
Hand-written reasons and option rewrites live in lintfix_2000_06_data.py. LONG-KEY items get wrong options rewritten to similar
length with the same error; GI keys are never edited (gi_facts key match). GI law citations were checked against LawPhil text.
Run: python3 scripts/batches/gapfill/lintfix_2000_06.py MANIFEST.json -> docs/research/audit/fixes/gap-fill-2000-06-lintfix.json"""
import copy, glob, json, os, re, sys
from collections import Counter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "batches", "audit"))
import explanation_lint as L
sys.path.insert(0, os.path.dirname(__file__))
import lintfix_2000_06_data as D
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DOMS = ["verbal_fil", "analytical", "clerical", "general_information"]
manifest = json.load(open(sys.argv[1]))["manifest"]
idx = {}
files = sorted(glob.glob(os.path.join(ROOT, "docs/batches/batch-*.json"))) + sorted(glob.glob(os.path.join(ROOT, "docs/research/*.json"))) \
    + sorted(glob.glob(os.path.join(ROOT, "docs/research/audit/fixes/*-drafts.json"))) + [os.path.join(ROOT, "docs/research/audit/data/baseline-550-spec-2026-10-18.json")]
for f in files:
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    for i in (d.get("items") if isinstance(d, dict) else d) or []:
        if isinstance(i, dict) and "id" in i and "options" in i: idx.setdefault(i["id"], i)

def key_text(it): return next(o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"])
def q(t): return t if re.fullmatch(r"[-\d.,%₱/ ]+", t) else f"\"{t}\""
def end(t): return t if t.rstrip()[-1:] in ".?!\"" else t + "."

# ---------- generated reasons ----------
def series(it):
    terms = re.search(r"series\?\s+(.*?),\s*_+", it["stem"]).group(1).split(", ")
    a = [AZ.index(t[0]) for t in terms]; b = [AZ.index(t[1]) for t in terms]
    ja = {y - x for x, y in zip(a, a[1:])}; jb = {y - x for x, y in zip(b, b[1:])}
    assert len(ja) == 1 and len(jb) == 1, it["id"]
    ja, jb = ja.pop(), jb.pop(); nxt = AZ[a[-1] + ja] + AZ[b[-1] + jb]
    k = key_text(it); assert k == nxt, (it["id"], k, nxt)
    why = (f"First letters {', '.join(t[0] for t in terms)} go up by {ja} each step, so {terms[-1][0]} + {ja} = {k[0]}. "
           f"Second letters {', '.join(t[1] for t in terms)} go up by {jb}, so {terms[-1][1]} + {jb} = {k[1]}.")
    ww = {}
    for o in it["options"]:
        if o["option_id"] == it["answer_option_id"]: continue
        t = o["text"]
        if t == k[::-1]: ww[o["option_id"]] = f"\"{t}\" has the right two letters in the wrong order."; continue
        parts = []
        if t[0] != k[0]: parts.append(f"its first letter ({t[0]}) is {terms[-1][0]} + {AZ.index(t[0]) - a[-1]}, but the first letters move by +{ja}")
        if t[1] != k[1]:
            dj = AZ.index(t[1]) - b[-1]
            parts.append(f"its second letter ({t[1]}) is {terms[-1][1]} + {dj}" + (f" (the first letters' jump)" if dj == ja else "") + f", but the second letters move by +{jb}")
        ww[o["option_id"]] = f"\"{t}\": " + "; ".join(parts) + "."
    return why, ww

DI = re.compile(r"Supply use of (.+?) by office \((.+)\)\. (.+)$")
def di_table(it):
    m = DI.match(it["stem"]); item, rows, ques = m.groups()
    tab = {}
    for r in rows.split("; "):
        off, vals = r.split(": ", 1)
        tab[off] = {mm: int(v) for mm, v in (x.split(" ") for x in vals.split(", "))}
    months = list(next(iter(tab.values())).keys())
    k = key_text(it); ww = {}
    m1 = re.match(r"In (\w+), how many more did (.+?) use than (.+?)\?$", ques)
    m2 = re.match(r"How many did (.+?) use in all three months\?$", ques)
    if m1:
        mo, x, y = m1.groups(); vx, vy = tab[x][mo], tab[y][mo]; ans = vx - vy
        assert str(ans) == k, (it["id"], k, ans)
        why = f"In the {mo} column, {x} used {vx} and {y} used {vy}, so {vx} − {vy} = {ans} more."
        other = [mm for mm in months if mm != mo]
        cand = {str(vx + vy): f"adds {vx} + {vy} instead of subtracting."}
        cand[str(sum(tab[x].values()) - sum(tab[y].values()))] = f"subtracts the three-month totals ({sum(tab[x].values())} − {sum(tab[y].values())}); the question asks about {mo} only."
        cand[str(abs(sum(tab[x].values()) - sum(tab[y].values())))] = cand[str(sum(tab[x].values()) - sum(tab[y].values()))]
        for mm in other:
            cand.setdefault(str(tab[x][mm] - tab[y][mm]), f"uses the {mm} column ({tab[x][mm]} − {tab[y][mm]}), not {mo}.")
            cand.setdefault(str(abs(tab[x][mm] - tab[y][mm])), f"uses the {mm} column ({tab[x][mm]} and {tab[y][mm]}), not {mo}.")
    elif m2:
        x = m2.group(1); v = [tab[x][mm] for mm in months]; ans = sum(v)
        assert str(ans) == k, (it["id"], k, ans)
        why = f"Add {x}'s row across the three months: {months[0]} {v[0]} + {months[1]} {v[1]} + {months[2]} {v[2]} = {ans}."
        cand = {f"{ans/3:.1f}".rstrip("0").rstrip("."): f"is the monthly average ({ans} ÷ 3); the question asks for the total."}
        for i in range(3):
            for j in range(i + 1, 3):
                cand.setdefault(str(v[i] + v[j]), f"adds only {months[i]} and {months[j]} ({v[i]} + {v[j]}) and leaves out {months[3 - i - j]}.")
        for mm in months:
            cs = sum(tab[o][mm] for o in tab)
            cand.setdefault(str(cs), f"adds the {mm} column for all three offices, not {x}'s row.")
    else: raise ValueError(it["id"])
    for o in it["options"]:
        if o["option_id"] == it["answer_option_id"]: continue
        c = cand.get(o["text"])
        if c: ww[o["option_id"]] = f"{o['text']} {c}"
    return why, ww

STD = "This follows standard office numeric/chronologic filing, not a rule published by the CSC. Source standard: ANSI/ARMA 12-2005."
def clr_order(it):
    lines = it["stem"].split("\n"); vals = lines[-1].split(": ", 1)[1].split(" | ")
    asc = sorted(vals, key=lambda s: int(s.replace("-", "")))
    first = "FIRST" in it["stem"]; want = asc[0] if first else asc[-1]; k = key_text(it)
    assert k == want, (it["id"], k, want)
    kind = "dates from earliest to latest" if "-" in vals[0] else "numbers in ascending order"
    how = "Compare year, then month, then day." if "-" in vals[0] else "Compare all five digits, keeping the leading zeros."
    why = f"{how} Sorted as {kind}: {', '.join(asc)}. So {k} is placed {'first' if first else 'last'}. {STD}"
    return why, {}

# ---------- build ----------
out, log, skipped = [], [], []
sys.path.insert(0, os.path.join(ROOT, "scripts", "batches"))
import gi_facts
def shift(s, k): return "".join(AZ[AZ.index(c) + k] if c in AZ else c for c in s)
comp = set(D.COMPANIONS)
for dom in DOMS:
    for sub, ids in manifest[dom].items():
        for oid in ids:
            it = idx[oid]; probs = L.lint_item(it)
            if not probs and oid not in comp: continue
            if oid in D.SKIP: skipped.append((oid, D.SKIP[oid])); continue
            fx = copy.deepcopy(it); rv = fx.setdefault("reveal", {}); rv.setdefault("why_wrong", {})
            changed = []
            for o in fx["options"]:
                new = D.OPT.get(oid, {}).get(o["text"])
                if new is None: continue
                if o["option_id"] == fx["answer_option_id"]:
                    assert dom != "general_information" or fx.get("_legacy"), oid  # GI keys are fixed by gi_facts
                o["text"] = new; changed.append(o["option_id"])
            if oid in D.STEM:
                if dom == "general_information":  # keep the gi_facts link when the stem is reworded
                    fx["_fact"] = next(n for n, x in enumerate(gi_facts.F) if x[2] == it["stem"])
                fx["stem"] = D.STEM[oid]
            if "\n\n" in fx["stem"]:
                for head, add in D.PASSAGE_ADD.items():
                    pa, qq = fx["stem"].rsplit("\n\n", 1)
                    if head in pa: fx["stem"] = pa + add + "\n\n" + qq; changed_stem = True
            if oid in D.REBASE:
                k = D.REBASE[oid]; head, ser = fx["stem"].split("?", 1); fx["stem"] = head + "?" + shift(ser, k)
                for o in fx["options"]: o["text"] = shift(o["text"], k)
            m = re.match(r"CIVIO-CLR-20261013-(\d{4})$", oid)
            if m and m.group(1) in D.REC:
                fx["stem"] = re.sub(r"Which (dated )?record should", lambda mm: f"Which {'dated ' if mm.group(1) else ''}{D.REC[m.group(1)]} should", fx["stem"], count=1)
            a = fx.get("archetype", "")
            gen_ww = {}
            if a == "ANA-SYMBOL-SERIES": body, gen_ww = series(fx)
            elif a == "ANA-DI-TABLE" and fx["stem"].startswith("Supply use"): body, gen_ww = di_table(fx)
            elif a in ("CLR-NUMERIC", "CLR-CHRONOLOGICAL"): body, gen_ww = clr_order(fx)
            elif a == "CLR-SPELL-RIGHT": body = D.SPELL[key_text(fx)]
            else:
                body = D.WHY.get(oid)
                assert body, f"no reason for {oid} {probs}"
                if body == D.KEEP:
                    body = re.sub(r'^"[^"]*" (is right|is correct|ang tamang sagot)\.\s*', "", it["reveal"]["why_correct"].strip())
            for k2, v in gen_ww.items(): rv["why_wrong"][k2] = v
            for k2, v in D.WW.get(oid, {}).items(): rv["why_wrong"][k2] = v
            if oid in D.COMPLETE:
                terms, sc, codes = D.COMPLETE[oid]
                rv["terms"], rv["shortcut"] = terms, sc
                fx["distractor_reasoning"] = {}
                for o in fx["options"]:
                    if o["option_id"] != fx["answer_option_id"]:
                        c, w = codes[o["text"]]; fx["distractor_reasoning"][o["option_id"]] = c; rv["why_wrong"][o["option_id"]] = w
            olds = {o["option_id"]: o["text"] for o in it["options"]}
            for oid2 in changed:
                if oid2 != fx["answer_option_id"] and oid2 not in D.WW.get(oid, {}) and oid not in D.COMPLETE and oid2 not in gen_ww:
                    newt = next(o["text"] for o in fx["options"] if o["option_id"] == oid2)
                    rv["why_wrong"][oid2] = rv["why_wrong"].get(oid2, "").replace(f"\"{olds[oid2]}\"", f"\"{newt}\"")
            k = key_text(fx)
            rv["why_correct"] = f"Answer: {q(k)}{'' if k.rstrip()[-1:] in '.?!' else '.'} {body}"
            fx["id"] = oid + "-LINTFIX"; fx["fix_of"] = oid
            fx["status"] = "draft"; fx["review_status"] = "unreviewed"
            for kk in ("reviewer", "reviewed_at", "review_line"): fx.pop(kk, None)
            fx["source_group"] = "civio"
            if oid in D.SRC: fx["source"], fx["source_url"] = D.SRC[oid]
            if oid in D.LEGACY: fx["_legacy"] = True
            if oid in D.REBASE: fx["notes_rebase"] = True
            fx["notes"] = ((f"gap-fill-2000-06 passage-set companion of {oid}: passage lengthened with its siblings (spec 10.8 sibling floor); explanation unchanged. " if not probs else
                            f"gap-fill-2000-06 lint fix of {oid} (was: {', '.join(probs)}). ")
                           + ("Wrong options rewritten for length: " + ", ".join(changed) + ". " if changed else "")
                           + (f"Series re-based by {D.REBASE[oid]:+d} letters to remove a near-duplicate of a bank series. " if oid in D.REBASE else "")
                           + ("Stem reworded (near-duplicate or solver format). " if oid in D.STEM else "")
                           + (D.NOTE[oid] + " " if oid in D.NOTE else "") + "Pending CoS.")
            fx.pop("notes_rebase", None)
            out.append(fx); log.append((dom, sub, oid, probs, changed))
dst = os.path.join(ROOT, "docs/research/audit/fixes/gap-fill-2000-06-lintfix.json")
json.dump({"batch": "gap-fill-2000-06-lintfix", "spec_version": "0.1.9", "status": "draft (pending CoS)", "items": out}, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), Counter(d for d, *_ in log)); print("skipped:", skipped)
json.dump([[d, s, o, p, c] for d, s, o, p, c in log], open("/tmp/lf06-log.json", "w"))
