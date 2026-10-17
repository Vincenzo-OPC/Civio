"""Explanation and answer-key lint for any spec-schema batch file (docs/batches/*.json, docs/research/*.json, audit drafts).
Usage: python3 scripts/batches/audit/explanation_lint.py FILE [FILE ...] [--csv out.csv] [--strict]
Item checks (code -> meaning):
  PLACEHOLDER   why_correct empty, under 40 characters (12 for numerical), or placeholder text ('Local practice item', 'Docker', 'TBD', 'lorem')
  KEY-NOT-STATED why_correct does not contain the keyed answer (text for words; the number for numeric keys)
  NUM-RESULT    numerical item whose arithmetic in why_correct does not end in the key value (checks 'a op b = c' steps)
  GI-NO-SECTION  GI item naming a law (R.A./P.D./E.O./Constitution) with no 'Sec.'/'Section'/'Art.' in why_correct or source
  BOILERPLATE   sentence run-on before 'Therefore' (missing period) or 'The other choices fail because the other choices'
  LONG-KEY      key is the uniquely longest option and at least 1.5x the mean distractor length (text options only)
File checks: POSITION  any answer position above 40% or below 10% of items (files with 20+ items).
Exit 0 unless --strict and any problem was found."""
import csv, json, re, sys
from collections import Counter
from fractions import Fraction as F
PH = re.compile(r"local practice item|docker|\bTBD\b|lorem|placeholder|TO BE QUOTED", re.I)
LAW = re.compile(r"\b(R\.?A\.?|Republic Act|P\.?D\.?|E\.?O\.?|Constitution|Art(icle)?\.?)\s*(No\.\s*)?\d*", re.I)
SEC = re.compile(r"\b(Sec(tion)?s?\.?|Art(icle)?\.?)\s*[\dIVX]", re.I)
def norm(s): return re.sub(r"[^a-z0-9./ ]", "", s.lower().replace(",", "").replace("₱", "")).strip()
def num(s):
    m = re.fullmatch(r"\s*₱?\s*(-?[\d,]*\.?\d+(?:/\d+)?)\s*(%|[a-zA-Z /]*)?\s*", s)
    if not m: return None
    try: return F(m.group(1).replace(",", ""))
    except Exception: return None
def nums_in(t): return {F(x.replace(",", "")) for x in re.findall(r"-?\d[\d,]*\.?\d*(?:/\d+)?", t) if re.search(r"\d", x) and not x.endswith(",")}
def lint_item(it):
    p = []
    opts = {o["option_id"]: o["text"] for o in it["options"]}
    key = opts.get(it["answer_option_id"], "")
    rv = it.get("reveal") or {}
    wc = (rv.get("why_correct") or "").strip()
    minlen = 12 if it.get("domain") == "numerical" else 40
    if len(wc) < minlen or PH.search(wc): p.append("PLACEHOLDER")
    kn = num(key)
    if wc and not PH.search(wc):
        if kn is not None:
            try: ok = kn in nums_in(wc)
            except Exception: ok = False
            if not ok: p.append("KEY-NOT-STATED")
        else:
            k = norm(key); w = norm(wc)
            words = [x for x in k.split() if len(x) > 3]
            if k not in w and (not words or sum(x in w for x in words) / len(words) < 0.6): p.append("KEY-NOT-STATED")
    if it.get("domain") == "numerical" and kn is not None and wc:
        steps = re.findall(r"=\s*₱?(-?[\d,]*\.?\d+)", wc)
        if steps and F(steps[-1].replace(",", "")) != kn and kn not in nums_in(wc): p.append("NUM-RESULT")
    if it.get("domain") == "general_information":
        blob = " ".join([it.get("stem", ""), it.get("source") or "", wc])
        if re.search(r"\b(R\.?A\.?|Republic Act|P\.?D\.?|E\.?O\.?)\s*(No\.\s*)?\d{3,5}|Constitution", blob) and not SEC.search(wc + " " + (it.get("source") or "")):
            p.append("GI-NO-SECTION")
    if re.search(r"[a-z0-9\"] Therefore", wc) or "The other choices fail because the other choices" in wc: p.append("BOILERPLATE")
    if kn is None and len(opts) >= 3:
        L = {o: len(t) for o, t in opts.items()}; kl = L[it["answer_option_id"]]
        others = [v for o, v in L.items() if o != it["answer_option_id"]]
        if kl > max(others) and kl >= 1.5 * (sum(others) / len(others)): p.append("LONG-KEY")
    return p
def lint_file(path):
    d = json.load(open(path, encoding="utf-8")); items = d["items"] if isinstance(d, dict) else d
    items = [i for i in items if isinstance(i, dict) and "options" in i and "answer_option_id" in i]
    res = [(i["id"], lint_item(i)) for i in items]
    pos = Counter([o["option_id"] for o in i["options"]].index(i["answer_option_id"]) for i in items)
    fp = []
    if len(items) >= 20:
        for k in range(4):
            s = pos.get(k, 0) / len(items)
            if s > 0.40 or s < 0.10: fp.append(f"POSITION {'ABCD'[k]} {pos.get(k,0)}/{len(items)} ({s:.0%})")
    return items, res, pos, fp
if __name__ == "__main__":
    args = sys.argv[1:]; out = None; strict = "--strict" in args
    if "--csv" in args: out = args[args.index("--csv") + 1]; args.remove("--csv"); args.remove(out)
    args = [a for a in args if a != "--strict"]; rows = []; bad = 0
    for f in args:
        items, res, pos, fp = lint_file(f)
        c = Counter(x for _, ps in res for x in ps); flagged = sum(bool(ps) for _, ps in res)
        print(f"{f}: {len(items)} items, {flagged} flagged; " + ", ".join(f"{k} {v}" for k, v in c.most_common()) + f"; positions {dict(sorted((('ABCD'[k]), v) for k, v in pos.items()))}")
        for x in fp: print("  FILE", x)
        bad += flagged + len(fp)
        rows += [[f, i, ";".join(ps)] for i, ps in res if ps]
    if out:
        with open(out, "w", newline="", encoding="utf-8") as fh: w = csv.writer(fh); w.writerow(["file", "id", "problems"]); w.writerows(rows)
    sys.exit(1 if strict and bad else 0)
