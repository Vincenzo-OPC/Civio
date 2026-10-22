"""Shared builder for the 22 Oct 2026 draft batches (GT approved). Items follow docs/CSE-Question-Design-Spec.md v0.1.9.
Every item is status draft / review_status unreviewed. Option order is a seeded shuffle of the item id, so builds are
reproducible. Arithmetic items carry a `recipe` that solver_2026_10_22.py recomputes from the stem text."""
import random
import re
from fractions import Fraction as F

PROV = {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-22T12:00:00+08:00", "spec_version": "0.1.9"}
NOTE = "New original draft, 22 Oct 2026. Design approach approved by GT; item not yet reviewed. Not copied from any reviewer; numbers, scenario and wording are Civio's own."


class Skip(Exception):
    pass


def peso(x):
    x = F(x)
    if x.denominator == 1:
        return f"₱{int(x):,}"
    return f"₱{float(x):,.2f}"


def num(x):
    x = F(x)
    if x.denominator == 1:
        return f"{int(x):,}"
    return f"{float(x):,.2f}".rstrip("0").rstrip(".")


def frac(x):
    """Lowest-terms fraction text; mixed number when above 1 (for example 1 5/12)."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, r = divmod(x.numerator, x.denominator)
    return f"{w} {F(r, x.denominator)}" if w else f"{x.numerator}/{x.denominator}"


def mk(*, id, track, domain, competency, concept, micro_skill, archetype, difficulty, est, stem, correct, wrong, terms, why_correct,
       shortcut=None, language="en", recipe=None, notes=NOTE, source="Original, Civio", url=None, **extra):
    """correct = key text; wrong = [(text, code, why)] x3."""
    texts = [correct] + [w[0] for w in wrong]
    if len(texts) != 4 or len({t.strip().lower() for t in texts}) != 4:
        raise Skip(f"{id}: options not 4 distinct: {texts}")
    order = list(range(4))
    random.Random(id).shuffle(order)
    opts, dr, ww, key = [], {}, {}, None
    for pos, src in enumerate(order):
        oid = f"o{pos + 1}"
        opts.append({"option_id": oid, "text": texts[src]})
        if src == 0:
            key = oid
        else:
            dr[oid], ww[oid] = wrong[src - 1][1], wrong[src - 1][2]
    rv = {"terms": terms}
    if shortcut:
        rv["shortcut"] = shortcut
    rv["why_correct"] = why_correct
    rv["why_wrong"] = ww
    it = {"id": id, "track": track, "domain": domain, "competency": competency, "concept": concept, "micro_skill": micro_skill,
          "archetype": archetype, "difficulty": difficulty, "est_seconds": est, "language": language, "stem": stem, "options": opts,
          "answer_option_id": key, "reveal": rv, "distractor_reasoning": dr, "source": source, "source_url": url, "source_group": "civio",
          "status": "draft", "review_status": "unreviewed", "reviewer": None, "reviewed_at": None, "provenance": PROV, "notes": notes}
    if shortcut:
        it["shortcut"] = shortcut
    if recipe:
        it["recipe"] = recipe
    it.update(extra)
    return it


def words(it):
    r = it["reveal"]
    txt = " ".join([r.get("terms", ""), r.get("shortcut", ""), r["why_correct"]] + list(r["why_wrong"].values()))
    return len(re.findall(r"\S+", txt))
