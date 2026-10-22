#!/usr/bin/env python3
"""GT decision 15:48: template-repetition audit of the APPROVED Numerical items.
A group is "substantively repetitive" only when its items share the archetype, the same numbers and the same key, with wording that
differs only in names and the object of the task (near-same scenario, numbers and wording). Sharing a method or a stem frame with
different numbers is NOT enough and is only listed for information.
For each substantively repetitive group the first item (lowest id) is kept and every other item gets ONE replacement draft with new
numbers, written to docs/research/audit/fixes/num-template-replacements-2026-10-22.json. Nothing is swapped into the manifest and no
approved item is edited, retired or removed: the replacements wait for authorized review.
Writes docs/research/audit/num-template-audit-2026-10-22.md and .json."""
import collections, copy, json, re, sys
from fractions import Fraction as F
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent.parent), str(Path(__file__).parent.parent / "drafts")]
import qa, solver_2026_10_22 as S  # noqa: E402

MAN = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json"
OUT = Path("docs/research/audit/fixes/num-template-replacements-2026-10-22.json")
REP_MD, REP_JSON = Path("docs/research/audit/num-template-audit-2026-10-22.md"), Path("docs/research/audit/num-template-audit-2026-10-22.json")

# new numbers per replaced id: ratio (total, a, b); rate (a, b); age (k, years)
NEW = {
    "CIVIO-NUM-WP-RATIO-000516": (16000, 3, 5), "CIVIO-NUM-WP-RATIO-000629": (21000, 2, 5), "CIVIO-NUM-WP-RATIO-000714": (8400, 5, 9),
    "CIVIO-NUM-WP-RATIO-000740": (6300, 4, 5), "CIVIO-NUM-WP-RATIO-000816": (4800, 5, 7), "CIVIO-NUM-WP-RATIO-000929": (7200, 2, 7),
    "CIVIO-NUM-WP-RATIO-000637": (13500, 4, 5), "CIVIO-NUM-WP-RATIO-000813": (11200, 3, 4),
    "CIVIO-NUM-WP-RATE-000042": (9, 72), "CIVIO-NUM-WP-RATE-000212": (24, 12), "CIVIO-NUM-WP-RATE-000524": (30, 15),
    "CIVIO-NUM-WP-RATE-000424": (20, 5), "CIVIO-NUM-WP-RATE-000722": (28, 84), "CIVIO-NUM-WP-RATE-000521": (10, 90),
    "CIVIO-NUM-WP-RATE-000419": (60, 20), "CIVIO-NUM-WP-RATE-000518": (16, 48), "CIVIO-NUM-WP-RATE-000635": (20, 80),
    "CIVIO-NUM-WP-RATE-000721": (24, 40), "CIVIO-NUM-WP-RATE-000814": (33, 66),
    "CIVIO-NUM-WP-ALGEBRA-000418": (3, 9), "CIVIO-NUM-WP-ALGEBRA-000823": (3, 13),
}


def nums(s):
    return tuple(re.findall(r"\d[\d,]*(?:\.\d+)?", s))


def key_text(it):
    return next(o["text"] for o in it["options"] if o["option_id"] == it["answer_option_id"])


def peso(v):
    return S._peso(F(v))


def h(v):
    return S._num(F(v)) + " hours"


def opts(seed, key, wrongs):
    """key plus three wrongs in a fixed order that depends on the item (no positional pattern)."""
    vals = [key] + [w for w, _ in wrongs]
    order = [(seed + i * 7) % 4 for i in range(4)]
    perm = sorted(range(4), key=lambda i: (order[i], i))
    ids = ["o1", "o2", "o3", "o4"]
    pos = {src: ids[n] for n, src in enumerate(perm)}
    return ([{"option_id": pos[i], "text": vals[i]} for i in sorted(range(4), key=lambda i: pos[i])], pos[0],
            {pos[i + 1]: why for i, (_, why) in enumerate(wrongs)})


def ratio(o, total, a, b):
    m = re.match(r"(?:(.+?) and (.+?) will share ₱[\d,]+ of (.+?) in the ratio|A ₱[\d,]+ (.+?) is divided between (.+?) and (.+?) in the ratio)", o["stem"])
    if m.group(1):
        p1, p2, what = m.group(1), m.group(2), m.group(3)
        stem = f"{p1} and {p2} will share ₱{total:,} of {what} in the ratio {a} : {b}. How much is {p2}'s share?"
    else:
        what, p1, p2 = m.group(4), m.group(5), m.group(6)
        stem = f"A ₱{total:,} {what} is divided between {p1} and {p2} in the ratio {a} : {b}. What is {p2}'s share?"
    part = F(total, a + b); key = part * b
    wr = [(peso(part * a), f"{peso(part * a)} is {p1}'s share ({a} parts). The question asks for {p2}."),
          (peso(F(total, b)), f"{peso(F(total, b))} divides the total by {b} alone, not by all {a + b} parts."),
          (peso(part), f"{peso(part)} is one part. It stops before multiplying by {b}.")]
    rv = {"terms": f"A ratio of {a} : {b} means for every {a} pesos {p1} gets, {p2} gets {b} pesos.",
          "shortcut": f"Add the ratio numbers: {a} + {b} = {a + b} equal parts. One part = ₱{total:,} ÷ {a + b} = {peso(part)}. {p2} gets {b} parts.",
          "why_correct": f"{peso(key)} is right: {b} × {peso(part)} = {peso(key)}. Check: {peso(part * a)} + {peso(key)} = ₱{total:,}.",
          "method_steps": {"1_asked": f"{p2}'s share.", "2_givens": f"total ₱{total:,}; ratio {a} : {b}",
                           "3_method": "Split the total into equal parts, then take the parts for the person asked.",
                           "4_why": "A ratio says how many equal parts each person gets.",
                           "5_solve_by_hand": f"{a} + {b} = {a + b}; ₱{total:,} ÷ {a + b} = {peso(part)}; {peso(part)} × {b} = {peso(key)}.",
                           "6_check": f"{peso(part * a)} + {peso(key)} = ₱{total:,}, and {peso(part * a)} : {peso(key)} = {a} : {b}.",
                           "8_shortcut": f"Share = total × {b}/{a + b}."}}
    rec = {"op": "ratio_share", "args": {"total": total, "parts": [a, b], "idx": 1}, "fmt": "peso"}
    return stem, peso(key), wr, rv, rec, ["NUM-OTHER-SHARE", "NUM-WRONG-BASE", "NUM-PARTIAL"]


def rate(o, a, b):
    m = re.match(r"(.+?) can (.+?) in \d+ hours\. (.+?) can (?:do the same job|.+?) in \d+ hours\.", o["stem"])
    p1, task, p2 = m.group(1), m.group(2), m.group(3)
    stem = f"{p1} can {task} in {a} hours. {p2} can do the same job in {b} hours. Working together, how long will they take?"
    key = F(a * b, a + b); avg = F(a + b, 2); fast = min(a, b)
    wr = [(h(a + b), f"{h(a + b)} adds the two times. Add the work done per hour, not the hours."),
          (h(avg), f"{h(avg)} is the average of the two times. Together they must be faster than the faster person alone."),
          (h(fast), f"{h(fast)} is how long the faster worker needs alone; with help the job takes less time.")]
    rv = {"terms": "A \"rate\" is how much of the job gets done in one hour.",
          "shortcut": f"Per hour, {p1} does 1/{a} and {p2} does 1/{b} of the job. Together: 1/{a} + 1/{b} = {S._frac(F(1, a) + F(1, b))}, so the job takes {h(key)}.",
          "why_correct": f"{h(key)} is right. Check: in {h(key)}, {p1} does {S._frac(key / a)} and {p2} does {S._frac(key / b)} of the job; together that is 1 whole job.",
          "method_steps": {"1_asked": "The time to finish one job working together.", "2_givens": f"{p1} alone {a} hours; {p2} alone {b} hours",
                           "3_method": "Add the hourly rates, then turn the combined rate back into a time.",
                           "4_why": "Each person finishes a fraction of the job per hour, and those fractions add.",
                           "5_solve_by_hand": f"1/{a} + 1/{b} = {S._frac(F(1, a) + F(1, b))} of the job per hour; 1 ÷ {S._frac(F(1, a) + F(1, b))} = {h(key)}.",
                           "6_check": f"{S._frac(key / a)} + {S._frac(key / b)} = 1 job.",
                           "8_shortcut": f"Time together = product ÷ sum: ({a} × {b}) ÷ ({a} + {b}) = {a * b} ÷ {a + b} = {h(key)}."}}
    rec = {"op": "together", "args": {"a": a, "b": b}, "fmt": "unit", "unit": "hours"}
    return stem, h(key), wr, rv, rec, ["NUM-OP-SWAP", "NUM-WRONG-BASE", "NUM-PARTIAL"]


def age(o, k, y):
    m = re.match(r"(.+?) is \d+ times as old as (his|her) (\w+)\.", o["stem"])
    p, pr, rel = m.group(1), m.group(2), m.group(3)
    stem = f"{p} is {k} times as old as {pr} {rel}. In {y} years, {p} will be twice as old as the {rel}. How old is {p} now?"
    s = F(y, k - 2); key = k * s
    wr = [(S._num(s), f"{S._num(s)} is the {rel}'s age now, not {p}'s."), (S._num(key + y), f"{S._num(key + y)} is {p}'s age {y} years from now, not today."),
          (S._num(s + y), f"{S._num(s + y)} is the {rel}'s age {y} years from now.")]
    rv = {"terms": f"\"{k} times as old\" means the age is the younger person's age multiplied by {k}.",
          "shortcut": f"Try the choices. If {p} is {S._num(key)}, the {rel} is {S._num(s)}. In {y} years: {S._num(key + y)} and {S._num(s + y)}, and {S._num(key + y)} = 2 × {S._num(s + y)}.",
          "why_correct": f"{S._num(key)} is right. Algebra: {rel} = s, {p} = {k}s; {k}s + {y} = 2(s + {y}) gives s = {S._num(s)}, so {p} = {S._num(key)}.",
          "method_steps": {"1_asked": f"{p}'s age now.", "2_givens": f"now {p} = {k} × {rel}; in {y} years {p} = 2 × {rel}",
                           "3_method": "Let the younger age be s and write the 'in the future' sentence as an equation.",
                           "4_why": f"Both people get {y} years older, so add {y} to each age.",
                           "5_solve_by_hand": f"{k}s + {y} = 2s + {2 * y}, so {k - 2}s = {y} and s = {S._num(s)}; {p} = {k} × {S._num(s)} = {S._num(key)}.",
                           "6_check": f"In {y} years: {S._num(key + y)} = 2 × {S._num(s + y)}.",
                           "8_shortcut": f"Younger age = years ÷ ({k} − 2); multiply by {k}."}}
    rec = {"op": "expr", "args": {"expr": f"{k}*{y}"}, "fmt": "num"} if k == 3 else None
    return stem, S._num(key), wr, rv, rec, ["NUM-OTHER-SHARE", "NUM-EXTRA-STEP", "NUM-OTHER-SHARE"]


def main():
    m = json.load(open(MAN)); cache, rows = {}, []
    for r in m["items"]:
        if r["domain"] != "numerical":
            continue
        f = r["source_file"]
        if f not in cache:
            d = json.load(open(f)); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        if cache[f][r["id"]]["status"] == "approved":
            rows.append(cache[f][r["id"]])
    groups = collections.defaultdict(list)
    for it in rows:
        groups[(it["archetype"], nums(it["stem"]), key_text(it))].append(it)
    rep = sorted([sorted(v, key=lambda x: x["id"]) for v in groups.values() if len(v) > 1], key=lambda v: v[0]["id"])
    # informational: same stem frame (names/numbers normalized), different numbers
    fr = collections.defaultdict(list)
    for it in rows:
        fr[re.sub(r"\b[A-Z][a-z]+\b", "N", re.sub(r"[₱]?\d[\d,]*(\.\d+)?", "#", it["stem"]))].append(it["id"])
    frames = sorted([v for v in fr.values() if len(v) > 1], key=len, reverse=True)
    used = {(it["archetype"], nums(it["stem"])) for it in rows}
    want = {it["id"] for v in rep for it in v[1:]}
    assert want == set(NEW), (sorted(want - set(NEW)), sorted(set(NEW) - want))
    out = []
    for v in rep:
        for o in v[1:]:
            fn = {"NUM-WP-RATIO": ratio, "NUM-WP-RATE": rate, "NUM-WP-ALGEBRA": age}[o["archetype"]]
            stem, key, wr, rv, rec, codes = fn(o, *NEW[o["id"]])
            assert (o["archetype"], nums(stem)) not in used and (o["archetype"], nums(stem)[::-1]) not in used, (o["id"], nums(stem))
            used.add((o["archetype"], nums(stem)))
            options, ans, why = opts(int(o["id"][-3:]), key, [(w, (y, c)) for (w, y), c in zip(wr, codes)])
            dr = {i: c for i, (_, c) in why.items()}; why = {i: y for i, (y, _) in why.items()}
            assert len({x["text"] for x in options}) == 4, (o["id"], options)
            it = copy.deepcopy(o)
            for k in ("gen_sig", "reviewer", "reviewed_at"):
                it.pop(k, None)
            rv["why_wrong"] = why
            rv["method_steps"]["7_distractors"] = " ".join(why[i] for i in sorted(why))
            it.update(id=o["id"] + "-TR1", stem=stem, options=options, answer_option_id=ans, reveal=rv,
                      distractor_reasoning=dr,
                      status="draft", review_status="unreviewed", reviewer=None, reviewed_at=None,
                      proposed_replacement_for=o["id"], kept_original=v[0]["id"],
                      provenance={"author": "Grok Bot (bank worker)", "method": "ai_assisted", "created_at": "2026-10-22T16:30:00+08:00", "spec_version": "0.1.9"},
                      notes=f"Template-repetition replacement draft for {o['id']} (same numbers, key and wording as {v[0]['id']}). Not in the manifest; the approved original stays until authorized review.",
                      shortcut=rv["method_steps"]["8_shortcut"])
            if rec:
                it["recipe"] = rec
                assert S.solve(it) == key, (it["id"], S.solve(it), key)
            e = qa.check_item(it)
            assert not e, (it["id"], e)
            out.append(it)
    OUT.write_text(json.dumps({"batch": "num-template-replacements-2026-10-22", "status": "draft proposals (not approved, not in manifest)",
                               "note": "One-for-one replacement drafts for substantively repetitive approved Numerical items. Approved originals are unchanged.",
                               "items": out}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REP_JSON.write_text(json.dumps({"approved_numerical": len(rows), "repetitive_groups": [[x["id"] for x in v] for v in rep],
                                    "replacement_drafts": len(out), "same_frame_different_numbers": frames}, indent=1) + "\n")
    md = ["# Approved Numerical template-repetition audit (22 Oct 2026)", "",
          f"Scope: the {len(rows)} approved Numerical items in the flat-2100 manifest. GT rule (15:48): recommend a replacement only when items are",
          "substantively repetitive (near-same scenario, numbers and wording), not merely because they share a method. No approved item was edited, retired or removed.", "",
          "**Test used.** Same archetype, identical numbers in the stem and the same key, with wording that differs only in names and the task noun.", "",
          f"## Substantively repetitive: {len(rep)} groups, {len(out)} replacement drafts", "",
          "| Keep (first id) | Repeats (replacement draft proposed) | Shared numbers | Key |", "|---|---|---|---|"]
    for v in rep:
        md.append(f"| {v[0]['id']} | {', '.join(x['id'] for x in v[1:])} | {' / '.join(nums(v[0]['stem']))} | {key_text(v[0])} |")
    md += ["", f"Drafts: `{OUT}` (ids `<original>-TR1`, status draft, `proposed_replacement_for` set). They are **not** in the manifest;",
           "the reviewer decides per pair whether to retire the original and swap the draft in (count stays 2,100 one-for-one).", "",
           "## Same stem frame, different numbers (no replacement recommended)", "",
           "These share a template and method but use different numbers and keys, so under the GT rule they are not repetitive. Listed for the reviewer's judgment only.", ""]
    for v in frames:
        md.append(f"- {len(v)} items: {', '.join(v)}")
    REP_MD.write_text("\n".join(md) + "\n")
    print(json.dumps({"approved_numerical": len(rows), "groups": len(rep), "drafts": len(out), "frame_groups_info": len(frames)}))


if __name__ == "__main__":
    main()
