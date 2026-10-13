"""Shared helpers for the Civio batch generator (spec v0.1.3).

Every generator returns item dicts in the batch JSON schema used by
docs/batches/batch-001.json. Keys are computed in code; distractors come from
coded mistakes (spec section 3 distractor codes).
"""
import random
import re

SPEC = "0.1.3"
PROVENANCE = {"author": "CSE (Grok Bot)", "method": "ai_assisted", "created_at": "2026-10-13T19:30:00+08:00", "spec_version": SPEC}

FIRST = ["Liza", "Ramon", "Teresa", "Datu", "Aling Rosa", "Mang Jun", "Bea", "Carlo", "Nonoy", "Inday", "Joy", "Paolo", "Mylene", "Arnel", "Grace",
         "Rhea", "Jomar", "Nestor", "Aileen", "Dindo", "Marites", "Efren", "Lourdes", "Bong", "Analyn", "Jun-jun", "Cora", "Rogelio", "Tess", "Kimberly"]
PLACES = ["Iloilo", "Tacloban", "Cagayan de Oro", "Baguio", "Naga", "Dumaguete", "Zamboanga", "Tuguegarao", "Legazpi", "Butuan", "Vigan", "Cotabato",
          "Puerto Princesa", "Laoag", "Ormoc", "Dipolog", "Roxas", "Calbayog", "Koronadal", "Lucena"]
OFFICES = ["municipal health office", "barangay hall", "city treasurer's office", "public library", "provincial capitol", "district hospital",
           "public market office", "records section", "civil registry", "engineering office", "social welfare office", "agriculture office"]


def peso(x):
    x = round(x, 2)
    if abs(x - round(x)) < 1e-9:
        return f"₱{int(round(x)):,}"
    return f"₱{x:,.2f}"


def num(x):
    x = round(x, 4)
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x)):,}"
    return f"{x:,}".rstrip("0").rstrip(".")


class Skip(Exception):
    """Raised when random draws give an item that would fail QA (ties, odd numbers)."""


def make(*, id, track, domain, competency, concept, micro_skill, archetype, difficulty, est, stem, correct, wrong, terms, shortcut, why_correct,
         source="Original, Civio", url=None, notes="", rng=None, prefix="o"):
    """correct = text; wrong = list of (text, code, why). Options are shuffled with rng."""
    texts = [correct] + [w[0] for w in wrong]
    if len(texts) != 4 or len(set(t.strip().lower() for t in texts)) != 4:
        raise Skip("options not 4 distinct")
    order = list(range(4))
    (rng or random).shuffle(order)
    opts, dr, ww = [], {}, {}
    key = None
    for pos, src in enumerate(order):
        oid = f"{prefix}{pos + 1}"
        opts.append({"option_id": oid, "text": texts[src]})
        if src == 0:
            key = oid
        else:
            _, code, why = wrong[src - 1]
            dr[oid] = code
            ww[oid] = why
    return {"id": id, "track": track, "domain": domain, "competency": competency, "concept": concept, "micro_skill": micro_skill,
            "archetype": archetype, "difficulty": difficulty, "est_seconds": est, "language": "en", "stem": stem, "options": opts,
            "answer_option_id": key, "reveal": {"terms": terms, "shortcut": shortcut, "why_correct": why_correct, "why_wrong": ww},
            "distractor_reasoning": dr, "source": source, "source_url": url, "source_group": "civio", "status": "draft",
            "review_status": "unreviewed", "reviewer": None, "reviewed_at": None, "provenance": PROVENANCE, "notes": notes}


def tokens(s):
    return set(re.findall(r"[a-z]+|\d+", s.lower()))


def jaccard(a, b):
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / max(1, len(ta | tb))
