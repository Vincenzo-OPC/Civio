"""Automated QA for a generated round. Keys are recomputed from the stem text by independent solvers."""
import json, math, os, re
from fractions import Fraction as F
from common import jaccard
import clerical, verbal, verbal_more, analytical, gi_facts, baseline

SPEC = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "CSE-Question-Design-Spec.md")
CODES = set(re.findall(r"`([A-Z]{2,4}-[A-Z][A-Z0-9-]*[A-Z0-9])`", open(SPEC, encoding="utf-8").read()))

REQ = ["id", "track", "domain", "competency", "concept", "micro_skill", "archetype", "difficulty", "est_seconds", "language", "stem", "options",
       "answer_option_id", "reveal", "distractor_reasoning", "source", "source_url", "source_group", "status", "review_status", "provenance"]
GI_URLS = {gi_facts.C, gi_facts.R}
ARMA = "This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule {}), not a rule published by the CSC."
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def money(s):
    return float(s.replace("₱", "").replace(",", ""))


def nums(s):
    return [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", s)]


def solve_num(it):
    s, a = it["stem"], it["archetype"]
    if a == "NUM-SEQ-DIFF" or a == "NUM-SEQ-MULT":
        xs = [int(x) for x in re.findall(r"-?\d+", s.split("?")[-1].split("___")[0])]
        d = [y - x for x, y in zip(xs, xs[1:])]
        dd = [y - x for x, y in zip(d, d[1:])]
        if len(set(dd)) == 1:
            return str(xs[-1] + d[-1] + dd[0])
        for m in (2, 3):
            cs = {y - m * x for x, y in zip(xs, xs[1:])}
            if len(cs) == 1:
                return str(xs[-1] * m + cs.pop())
        return None
    if "raised the price by" in s:
        p, up, dn = money(re.search(r"for (₱[\d,.]+)", s).group(1)), *map(float, re.findall(r"(\d+)%", s))
        return p * (1 + up / 100) * (1 - dn / 100)
    if "ratio" in s:
        tot = money(re.search(r"₱[\d,.]+", s).group())
        a_, b_ = map(int, re.search(r"ratio (\d+) : (\d+)", s).groups())
        return tot * b_ / (a_ + b_)
    if "Working together" in s:
        a_, b_ = map(int, re.findall(r"in (\d+) hours", s))
        return f"{a_ * b_ // (a_ + b_)} hours"
    if "One more person" in s:
        n, avg, new = map(int, re.search(r"the (\d+) .*? is (\d+) years\. One more person, with (\d+)", s).groups())
        return f"{(n * avg + new) // (n + 1)} years"
    if "simple interest" in s:
        P = money(re.search(r"₱[\d,.]+", s).group())
        r = int(re.search(r"(\d+)% simple", s).group(1))
        y = int(re.search(r"after (\d+) year", s).group(1))
        m = re.search(r"and (\d+) months", s)
        t = y + (int(m.group(1)) / 12 if m else 0)
        return P * r / 100 * t
    if "times as old" in s:
        m = int(re.search(r"is (\d+) times", s).group(1))
        y = int(re.search(r"In (\d+) years", s).group(1))
        k = 2 if "twice" in s else 3
        for c in range(1, 100):
            if m * c + y == k * (c + y):
                return str(m * c)
    if "% off" in s:
        p = money(re.search(r"₱[\d,.]+", s).group())
        d = int(re.search(r"(\d+)% off", s).group(1))
        return p * (100 - d) / 100
    if a == "NUM-OPS-ORDER":
        ex = re.search(r"value of (.+)\?", s).group(1).replace("×", "*").replace("−", "-").replace("÷", "/")
        v = F(eval(re.sub(r"(\d+)", r"F(\1)", ex), {"__builtins__": {}, "F": F}))
        return str(v.numerator) if v.denominator == 1 else None
    if a == "NUM-FRAC-DEC":
        tot = int(re.search(r"had (\d+)", s).group(1))
        f1, f2 = [F(x) for x in re.findall(r"(\d+/\d+)", s)]
        rest = tot - tot * f1
        return str(int(rest - rest * f2))
    if a == "NUM-WP-GEOM":
        L, W = map(int, re.findall(r"(\d+) m", s))
        c = money(re.search(r"₱[\d,.]+", s).group())
        return 2 * (L + W) * c
    return None


def solve_ana(it):
    s, a = it["stem"], it["archetype"]
    if s.startswith("What comes next in the series?"):
        ts = s.split("?")[1].split("___")[0].replace(",", " ").split()
        out = ""
        for k in range(2):
            idx = [AZ.index(t[k]) for t in ts]
            d = {y - x for x, y in zip(idx, idx[1:])}
            if len(d) != 1:
                return None
            out += AZ[idx[-1] + d.pop()]
        return out
    if "In a certain code" in s:
        w1, c1, w2 = re.search(r"code, (\w+) is written as (\w+)\. How is (\w+)", s).groups()
        k = (AZ.index(c1[0]) - AZ.index(w1[0])) % 26
        assert all((AZ.index(y) - AZ.index(x)) % 26 == k for x, y in zip(w1, c1))
        return "".join(AZ[(AZ.index(c) + k) % 26] for c in w2)
    if s.startswith("Four staff members"):
        pairs = re.findall(r"([A-Z][\w\- ]+?) (?:finished the report earlier than|has served longer than|scored higher than|lives nearer the office than|arrived earlier than|encoded more forms than) ([A-Z][\w\- ]+?)\.", s)
        names = {x for p in pairs for x in p}
        order = []
        rem = set(names)
        while rem:
            top = [n for n in rem if not any(b == n and a_ in rem for a_, b in pairs)]
            assert len(top) == 1
            order.append(top[0]); rem.discard(top[0])
        return order[1 if "Who is second" in s else 2]
    if a == "ANA-DI-TABLE":
        rows = dict(re.findall(r"(\w+): (\w+ \d+, \w+ \d+, \w+ \d+)", s))
        tab = {k: [int(x) for x in re.findall(r"\d+", v)] for k, v in rows.items()}
        m = re.search(r"How many did (\w+) use in all three", s)
        if m:
            return str(sum(tab[m.group(1)]))
        m = re.search(r"how many more did (\w+) use than (\w+)\?", s)
        if m:
            return str(tab[m.group(1)][2] - tab[m.group(2)][2])
        m = re.search(r"What percent of (\w+)'s", s)
        if m:
            v = tab[m.group(1)]
            return f"{v[0] * 100 // sum(v)}%"
    if a == "ANA-SYLLOGISM":
        t = s.replace("Statement 1: ", "").replace("Statement 2: ", "").replace("Assume these are true: ", "")
        t = re.sub(r"every one of the (.+?) is among the (.+?)(,|\.)", r"All \1 are \2.", t)
        t = re.sub(r"none of the (.+?) are (.+?)(,|\.)", r"No \1 are \2.", t)
        t = re.sub(r"a few of the (.+?) are (.+?)(,|\.)", r"Some \1 are \2.", t)
        t = re.sub(r"all of the (.+?) are (.+?)(,|\.)", r"All \1 are \2.", t)
        alls = re.findall(r"All (.+?) are (.+?)\.", t)
        some = re.findall(r"Some (.+?) are (.+?)\.", t)
        no = re.findall(r"No (.+?) are (.+?)\.", t)
        if len(alls) == 2:
            (x1, y1), (x2, y2) = alls
            return f"All {x1} are {y2}." if y1 == x2 else f"All {x2} are {y1}." if y2 == x1 else None
        if alls and some:
            (x, y), (sx, p_) = alls[0], some[0]
            return f"Some {y} are {p_}." if sx == x else None
        if alls and no:
            (x, y), (nx, p_) = alls[0], no[0]
            return f"No {x} are {p_}." if nx == y else None
        return None
    if a == "ANA-ASSUME-I-II" and not it.get("_legacy"):
        import assume
        for st, a1, a2, key in assume.ROWS:
            if s.startswith(f"Statement: {st}"):
                return analytical.OPT[key]
    if a.startswith("ANA-ANALOGY"):
        m = re.match(r"(.+?) : (.+?) :: ____$", s) or re.match(r"(.+?) is to (.+?) as ____\.$", s) or re.search(r'"(.+?) : (.+?)"', s) or re.search(r'"(.+?)" and "(.+?)"', s)
        if not m:
            return None
        a_, b_ = m.group(1).strip().lower(), m.group(2).strip().lower()
        for t in analytical.ANALOGIES:
            if (t[0], t[1]) == (a_, b_):
                return f"{t[4][0]} : {t[4][1]}"
    return None


from fixes import spell_words
CORRECT = set(clerical.WORDS) | {w for w, _ in spell_words.T} | set(spell_words.FOILS)
MISSPELT = {m: (w, c) for w, ms in spell_words.T for m, c in ms}


def solve_cler(it):
    s, a = it["stem"], it["archetype"]
    if a == "CLR-SPELL-RIGHT":
        ok = [o["text"] for o in it["options"] if o["text"] in CORRECT]
        return ok[0] if len(ok) == 1 else None
    if a == "CLR-SPELL-WRONG":
        bad = [o["text"] for o in it["options"] if o["text"] not in CORRECT]
        return bad[0] if len(bad) == 1 else None
    if a == "CLR-FILE-POSITION":
        names = s.split("?  ")[1].split(" | ")
        def k(n):
            parts = n.split()
            if parts[0] in clerical.TITLES:
                t, parts = parts[0], parts[1:]
            else:
                t = ""
            g, m, sur = parts[0], parts[1], " ".join(parts[2:])
            return (re.sub(r"[^a-z]", "", sur.lower()), g.lower(), m.lower(), t)
        ks = sorted(names, key=k)
        assert len({k(n)[:3] for n in names}) == 4
        return ks[-1] if "LAST" in s else ks[0]
    return None


def solve_verb(it):
    s, a = it["stem"], it["archetype"]
    if a == "VEN-ERROR-AGREE":
        for subj, noun, preds in verbal.AGREE:
            for vs, vp, rest in preds:
                if s.endswith(f"{subj} ____ {rest}."):
                    return vs
    if a == "VEN-ERROR-TENSE":
        sig = s.split(": ")[1].split(",")[0]
        t = dict(verbal.TENSE)[sig]
        for row in verbal.TV:
            if s.rstrip(".").endswith(row[7]) or (row[7] + " on time") in s:
                return {"past": row[1], "future": row[2], "present": row[3], "presperf": row[4], "futperf": row[5], "prog": row[6]}[t]
    tables = verbal.CONFUSED + verbal.PHRASAL + verbal.PRON + verbal_more.PREP + verbal_more.SCOMP + verbal_more.IDIOMS
    for sent, word, c, _ in verbal_more.VIC:
        if s.endswith(sent):
            return c
    for sent, c, _ in tables:
        if s.endswith(sent):
            return c
    m = re.search(r"capital letters\?  (\w+)", s)
    if m:
        for w, syn, wr in verbal.SYN:
            if w.upper() == m.group(1):
                return wr[0][0] if "OPPOSITE" in s else syn
    return None


def key_text(it):
    return next(o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"])


from common import FIRST, FEMALE

PRON_F, PRON_M = {"she", "her", "hers", "herself"}, {"he", "him", "his", "himself"}


def pronoun_errors(it):
    """Rescan every text field that mentions a person: a sentence with exactly one named person must use matching pronouns."""
    out = []
    texts = [it["stem"], it["reveal"]["shortcut"], it["reveal"]["why_correct"], *it["reveal"]["why_wrong"].values(), *(o["text"] for o in it["options"])]
    for t in texts:
        for sent in re.split(r"(?<=[.?!])\s+", t):
            names = [n for n in FIRST if re.search(r"\b%s\b" % re.escape(n), sent)]
            if len(names) != 1:
                continue
            low = sent.lower()
            f = names[0] in FEMALE
            rel = r"(son|daughter|nephew|niece|child|children|father|mother|brother|sister|staff|office|desk|team)"
            # "his son" / "her niece": the pronoun is the named person's, so it must match the name
            for pr in re.findall(r"\b(his|her)\s+" + rel + r"\b", low):
                if (pr[0] == "his") == f:
                    out.append(f"pronoun does not match {names[0]}: {sent[:60]}")
            # other pronouns are fine only if a person of that gender is also in the sentence
            rest = re.sub(r"\b(his|her)\s+" + rel + r"\b", " ", low)
            words = set(re.findall(r"[a-z]+", rest))
            male_rel = words & {"son", "nephew", "father", "brother", "man", "boy"}
            fem_rel = words & {"daughter", "niece", "mother", "sister", "woman", "girl"}
            if (f and words & PRON_M and not male_rel) or (not f and words & PRON_F and not fem_rel):
                out.append(f"pronoun does not match {names[0]}: {sent[:60]}")
    return out


def check_item(it):
    errs = pronoun_errors(it)
    for k in REQ:
        if k not in it:
            errs.append(f"missing {k}")
    if errs:
        return errs
    ids = [o["option_id"] for o in it["options"]]
    texts = [o["text"].strip().lower() for o in it["options"]]
    if len(ids) != 4 or len(set(ids)) != 4 or len(set(texts)) != 4:
        errs.append("options must be 4 distinct")
    if it["answer_option_id"] not in ids:
        errs.append("answer not in options")
    wrong = set(ids) - {it["answer_option_id"]}
    if set(it["distractor_reasoning"]) != wrong or set(it["reveal"]["why_wrong"]) != wrong:
        errs.append("every wrong option needs a code and a why")
    for f in ("terms", "shortcut", "why_correct"):
        if not it["reveal"].get(f):
            errs.append(f"reveal.{f} empty")
    if "shortcut" in it:
        sc = it["shortcut"]
        if not isinstance(sc, str) or not sc.strip():
            errs.append("shortcut: omit the field instead of leaving it empty")
        elif len(sc) > 300:
            errs.append("shortcut longer than 300 characters (keep it to one technique)")
        elif re.search(r"\b(choice|option|letter) [A-D]\b", sc):
            errs.append("shortcut names a choice by letter")
    kt = next((o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"]), "")
    labs = re.findall(r"^\s*([1-9A-Z])[.)]\s", it["stem"], re.M)
    if len(labs) >= 3 and re.sub(r"[^0-9A-Z]", "", kt) == "".join(labs):
        errs.append("order item: key matches listed order")
    approved = (it["status"] == "approved" and it.get("review_status") == "passed"
                and it.get("reviewer") and it.get("reviewed_at"))
    if not (it["status"] == "draft" or approved) or it["source_group"] != "civio":
        errs.append("status/source_group")
    for o in it["options"]:
        if re.search(r"\b(choice|option|letter) [A-D]\b", it["reveal"]["why_correct"] + " ".join(it["reveal"]["why_wrong"].values())):
            errs.append("names a choice by letter")
            break
    for oid, code in it["distractor_reasoning"].items():
        if code not in CODES:
            errs.append(f"code {code} not in spec")
    codes = list(it["distractor_reasoning"].values())
    if it.get("concept") == "ordering" and len(set(codes)) != len(codes):
        errs.append("ordering item: each wrong option needs its own code")
    if it["archetype"].startswith("CLR-FILE"):
        sub = it.get("distractor_subreason", {})
        if set(codes) != {"CLR-FILE-ORDER"} or set(sub) != set(it["distractor_reasoning"]) or not all(re.search(r"ARMA Rule \d", v) and v.split(":")[0] in CODES for v in sub.values()):
            errs.append("filing: parent code CLR-FILE-ORDER plus an ARMA-rule sub-reason for every distractor")
    if it.get("concept") in ("synonyms", "antonyms") and "RC-OPPOSITE" in codes:
        errs.append("synonym/antonym traps must use VRB-SYNONYM-TRAP / VRB-ANTONYM-TRAP")
    d = it["domain"]
    if d == "general_information" and not it.get("_legacy"):
        if it["source_url"] not in GI_URLS:
            errs.append("GI url not verified")
        f = gi_facts.F[it["_fact"]] if "_fact" in it else next((x for x in gi_facts.F if x[2] == it["stem"]), None)
        if not f or key_text(it) != f[3]:
            errs.append("GI key mismatch")
    if it["archetype"].startswith("CLR-FILE"):
        if not any(ARMA.format(n) in it["reveal"]["why_correct"] for n in range(1, 9)):
            errs.append("filing item lacks ARMA note")
    solver = None if it.get("_legacy") else {"numerical": solve_num, "analytical": solve_ana, "clerical": solve_cler, "verbal_en": solve_verb}.get(d)
    if solver:
        exp = solver(it)
        if exp is None:
            errs.append("solver could not recompute the key")
        else:
            kt = key_text(it)
            ok = (abs(money(kt) - exp) < 0.005) if isinstance(exp, float) else (kt == exp)
            if not ok:
                errs.append(f"key mismatch: key {kt!r}, solver {exp!r}")
            others = [o["text"] for o in it["options"] if o["option_id"] != it["answer_option_id"]]
            if (isinstance(exp, float) and any(t.startswith("₱") and abs(money(t) - exp) < 0.005 for t in others)) or exp in others:
                errs.append("more than one option matches the key")
    return errs


def norm_stem(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def check_round(items, prior_stems, near=0.9):
    """Return list of (id, error). prior_stems: stems from earlier batches and the dev DB."""
    out = []
    seen = list(prior_stems)
    seenset = {norm_stem(x) for x in seen}
    for it in items:
        for e in check_item(it):
            out.append((it["id"], e))
        ns = norm_stem(it["stem"])
        if ns in seenset:
            out.append((it["id"], "duplicate stem"))
        else:
            for p in seen:
                if jaccard(p, it["stem"]) >= near:
                    out.append((it["id"], f"near-duplicate of: {p[:70]}"))
                    break
        seen.append(it["stem"])
        seenset.add(ns)
        if re.search(r"variant \d", it["stem"], re.I):
            out.append((it["id"], "variant label in stem"))
    return out


def check_gi_evidence(items, cache="/workspace/gi"):
    """Check each GI quote against the fetched official text, when the cache is present."""
    paths = {gi_facts.C: os.path.join(cache, "cons1987.html.txt"), gi_facts.R: os.path.join(cache, "ra_6713_1989.html.txt")}
    if not all(os.path.exists(p) for p in paths.values()):
        return None
    txt = {u: re.sub(r"\s+", " ", open(p).read()).lower() for u, p in paths.items()}
    bad = []
    for it in items:
        if it["domain"] == "general_information":
            f = gi_facts.F[it["_fact"]]
            if re.sub(r"\s+", " ", f[5]).lower() not in txt[f[0]]:
                bad.append(it["id"])
    return bad


BASE = None


def baseline_hits(items, near=0.65):
    """Exact and near matches of item stems against the baseline bank (normalized stems)."""
    global BASE
    if BASE is None:
        BASE = [(src, baseline.norm(st), pre) for src, st, pre in baseline.stems()]
    hits = []
    for it in items:
        n = baseline.norm(it["stem"])
        for src, b, pre in BASE:
            if (pre and n.startswith(b[:50])) or n == b:
                hits.append((it["id"], "exact", src, b[:70]))
                break
            if not pre and jaccard(n, b) >= near:
                hits.append((it["id"], "near", src, b[:70]))
                break
            if it.get("archetype", "").startswith("ANA-ANALOGY") and not pre:
                pair = analogy_pair(it["stem"])
                if pair and re.search(r"\b%s\b.{0,12}\b%s\b" % tuple(map(re.escape, pair)), b):
                    hits.append((it["id"], "near (same analogy pair)", src, b[:70]))
                    break
    return hits


def analogy_pair(s):
    m = re.match(r"(.+?) : (.+?) :: _+$", s) or re.match(r"(.+?) is to (.+?) as _+\.$", s) or re.search(r'"(.+?) : (.+?)"', s) or re.search(r'"(.+?)" and "(.+?)"', s)
    return (m.group(1).strip().lower(), m.group(2).strip().lower()) if m else None


TENSE_CONCEPTS = {"verb tense", "tense consistency"}


def check_batch_rules(batch_items):
    """Per-batch CoS rules: tense <= 5, frame <= 2."""
    out = []
    t = sum(1 for i in batch_items if i.get("concept") in TENSE_CONCEPTS)
    if t > 5:
        out.append(("batch", f"{t} tense items (max 5)"))
    from collections import Counter
    for f, n in Counter(i.get("gen_frame") for i in batch_items if i.get("gen_frame")).items():
        if n > 2:
            out.append(("batch", f"frame {f} used {n} times (max 2)"))
    return out


def stem_frame(s):
    """Stem phrasing: text before the first colon, question mark or double space, with numbers as N."""
    return re.sub(r"\d+(\.\d+)?", "N", re.split(r"[:?]|  ", s)[0]).strip()[:70]


def spell_target(it):
    k = key_text(it)
    return (MISSPELT.get(k, (k,))[0] if it["archetype"] == "CLR-SPELL-WRONG" else k).lower()


def check_spelling(all_items):
    """Round 02 CoS rule: one spelling target per item bank-wide; coded error types must match the misspelling."""
    out, seen = [], {}
    for it in all_items:
        if it["archetype"] not in ("CLR-SPELL-RIGHT", "CLR-SPELL-WRONG"):
            continue
        t = spell_target(it)
        if t in seen:
            out.append((it["id"], f"spelling target '{t}' repeats {seen[t]}"))
        seen[t] = it["id"]
        for o in it["options"]:
            if o["text"] in MISSPELT:
                w, c = MISSPELT[o["text"]]
                code = it["distractor_reasoning"].get(o["option_id"]) or it.get("error_code")
                if code != c or not spell_words.check_code(w, o["text"], c):
                    out.append((it["id"], f"error code {code} does not describe {o['text']}"))
    return out


def check_bank_rules(all_items):
    """Bank-wide CoS rules: tense <= 50 of Verbal; every syllogism/analogy type has >= 3 frames; spelling targets unique."""
    out = check_spelling(all_items)
    from collections import Counter
    dom = Counter(i["domain"] for i in all_items)
    fr = Counter((i["domain"], stem_frame(i["stem"])) for i in all_items)
    for (d, f), n in fr.items():
        if n > 0.25 * dom[d]:
            out.append(("bank", f"{d}: phrasing '{f}' used {n}/{dom[d]} (max 25%)"))
    t = sum(1 for i in all_items if i.get("concept") in TENSE_CONCEPTS)
    if t > 50:
        out.append(("bank", f"{t} tense items (max 50)"))
    types = {}
    for i in all_items:
        if i["archetype"] == "ANA-SYLLOGISM" or i["archetype"].startswith("ANA-ANALOGY"):
            key = ("SYL-" + i.get("gen_frame", "SYL-?")[4]) if i["archetype"] == "ANA-SYLLOGISM" else i["archetype"]
            types.setdefault(key, set()).add(i.get("gen_frame", "hand-written"))
    for k, fr in types.items():
        if len(fr) < 3:
            out.append(("bank", f"{k}: only {len(fr)} frames"))
    return out
