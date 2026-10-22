#!/usr/bin/env python3
"""GT directive 3 (b): P1 editorial fixes as draft revisions (-R1). The reviewed originals in batch-subpro-num-001.json are not
edited (history kept); each -R1 is a draft with replaces=<original>, a change log, and method-first steps. No approval is recorded.
Writes docs/research/audit/fixes/p1-editorial-r1-2026-10-22.json. Run from the repo root."""
import copy, json, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent), str(Path(__file__).parent.parent)]
import method_first_2026_10_22 as MF  # noqa: E402

SRC, OUT = "docs/research/batch-subpro-num-001.json", "docs/research/audit/fixes/p1-editorial-r1-2026-10-22.json"
FIX = {
 "CIVIO-NUM-WP-ALGEBRA-926041": dict(
    change="Scenario made realistic: a 12-year-old 'trainee' (7 years old five years ago) is implausible; now a mother and son. Numbers, key and distractors unchanged.",
    stem="A mother is 21 years older than her son. Five years ago, the mother was four times as old as her son. How old is the son today?",
    theme="mother-son-past-ages", concept="past ages with a fixed gap",
    reveal={"terms": "An age difference stays the same as both people grow older.",
            "shortcut": "Five years ago the mother was 4 times the son's age, so the 21-year gap is 3 of the son's ages then: 21 ÷ 3 = 7. Add the 5 years back: 7 + 5 = 12.",
            "why_correct": "12 years is right. Today the son is 12 and the mother 33. Five years ago they were 7 and 28, and 28 = 4 × 7.",
            "why_wrong": {"o2": "33 years is the mother's age today, not the son's.",
                          "o3": "16 years is 21 − 5: it subtracts the five years from the age gap instead of using the 'four times' relation.",
                          "o4": "7 years is the son's age five years ago; add the 5 years back to get his age today."}},
    steps=("The son's age today.", "gap 21 years; five years ago, mother = 4 × son",
           "Use the fixed gap. When one age is 4 times the other, the gap is 3 times the smaller age.", "The gap never changes, so it is the same 21 years five years ago.",
           "Five years ago: 4s − s = 3s = 21, so s = 7. Today: 7 + 5 = 12 years.", "Today 12 and 33 (gap 21). Five years ago 7 and 28; 4 × 7 = 28.",
           "Smaller past age = gap ÷ (multiplier − 1).")),
 "CIVIO-NUM-WP-ALGEBRA-926039": dict(
    change="Explanation fix: the 18-kg distractor is the stock left after the sale (30 − 12), not a sign error; 24-kg explanation made exact.",
    reveal_patch={"why_wrong": {"o1": "24 kilograms assumes the 12 kilograms sold was exactly half the stock (12 × 2) and ignores the extra 3 kilograms in the remainder.",
                                "o2": "15 kilograms is half the starting stock (x/2 = 15), the middle step, not the full starting amount.",
                                "o4": "18 kilograms is the stock left after the sale (30 − 12 = 18), not the stock at the start."}},
    steps=None),
 "CIVIO-NUM-WP-ALGEBRA-926042": dict(
    change="Explanation fix: the 21-year distractor is the younger cousin's age four years from now (17 + 4), not a missed step.",
    reveal_patch={"why_wrong": {"o4": "21 years is the younger cousin's age four years from now (17 + 4); the question asks for the age today."}},
    steps=None),
 "CIVIO-NUM-WP-RATE-926043": dict(
    change="Explanation fix: teach the work-rate calculation for 400 kits step by step (kits per volunteer-hour, then new volunteer-hours).",
    reveal_patch={"terms": "A \"volunteer-hour\" is one volunteer working for one hour. At a steady pace, every volunteer-hour packs the same number of kits.",
                  "shortcut": "Step 1: first crew = 3 volunteers × 6 hours = 18 volunteer-hours. Step 2: 360 kits ÷ 18 = 20 kits per volunteer-hour. Step 3: new crew = 5 × 4 = 20 volunteer-hours. Step 4: 20 × 20 = 400 kits.",
                  "why_correct": "400 kits is right: 5 volunteers × 4 hours = 20 volunteer-hours, and each volunteer-hour packs 20 kits, so 20 × 20 = 400. Check: 400 ÷ 20 = 20 volunteer-hours = 5 × 4."},
    steps=None),
}


RECIPE = {  # recomputed by drafts/solver_2026_10_22.py so qa.check_item verifies each key from the stem
 "CIVIO-NUM-WP-ALGEBRA-926041": {"op": "past_age_gap", "args": {"gap": 21, "k": 4, "years_ago": 5}, "fmt": "unit", "unit": "years"},
 "CIVIO-NUM-WP-ALGEBRA-926039": {"op": "expr", "args": {"expr": "(12 + 3) * 2"}, "fmt": "unit", "unit": "kilograms"},
 "CIVIO-NUM-WP-ALGEBRA-926042": {"op": "expr", "args": {"expr": "(48 - 4 - 4 - 6) / 2"}, "fmt": "unit", "unit": "years"},
 "CIVIO-NUM-WP-RATE-926043": {"op": "expr", "args": {"expr": "360 / (3 * 6) * 5 * 4"}, "fmt": "unit", "unit": "kits"},
}


def main():
    src = {i["id"]: i for i in json.load(open(SRC, encoding="utf-8"))["items"]}
    out = []
    for oid, fx in FIX.items():
        it = copy.deepcopy(src[oid])
        it.update({"id": oid + "-R1", "replaces": oid, "status": "draft", "review_status": "unreviewed", "reviewer": None, "reviewed_at": None,
                   "revision_history": [{"from": oid, "date": "2026-10-22", "by": "bank worker", "change": fx["change"], "reason": "P1 editorial fix, GT directive 3 (b)"}],
                   "notes": f"Draft revision of {oid} (reviewed). {fx['change']} Pending independent review; not approved."})
        for k in ("stem", "theme", "concept"):
            if k in fx:
                it[k] = fx[k]
        if "reveal" in fx:
            it["reveal"] = fx["reveal"]
        for k, v in fx.get("reveal_patch", {}).items():
            if isinstance(v, dict):
                it["reveal"][k].update(v)
            else:
                it["reveal"][k] = v
        if fx.get("steps"):
            a = fx["steps"]
            it["reveal"]["method_steps"] = {"1_asked": a[0], "2_givens": a[1], "3_method": a[2], "4_why": a[3], "5_solve_by_hand": a[4], "6_check": a[5], "7_distractors": MF._dist(it), "8_shortcut": a[6]}
        else:
            it["reveal"]["method_steps"] = MF.steps(dict(it, id=oid))
        it["recipe"] = RECIPE[oid]
        out.append(it)
    Path(OUT).write_text(json.dumps({"batch": "p1-editorial-r1-2026-10-22", "spec_version": "0.1.9", "status": "draft (pending independent review; not approved)",
                                     "items": out}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "written")


if __name__ == "__main__":
    main()
