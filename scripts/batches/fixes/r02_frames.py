"""Round 02 fix 3: frame cap (CoS ruling 2026-10-13). Rewrites stems only where a phrasing exceeds 25% of its domain,
and spreads the order-of-operations items across six expression shapes (every key recomputed)."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from build import DOCS
CHANGED = "changed (round 02 fixes; awaiting CoS review)"
BC = "Choose the word that best completes the sentence: "
VERB_FRAMES = {
    "subject-verb agreement": "Which verb agrees with the subject of the sentence? ",
    "commonly confused words": "Which word correctly fills the blank? ",
    "prepositions": "Which preposition correctly fills the blank? ",
    "pronoun case": "Which pronoun correctly fills the blank? ",
}
SPELL_WRONG = ["Which word is misspelled?", "Which of these words has a spelling error?", "One word below is spelled wrong. Which one?"]
SPELL_RIGHT = ["Which word is spelled correctly?", "Which of these words is spelled the standard way?"]


def ops(a, b, c, d, shape):
    """Return (expression, key, shortcut, why_correct, wrong list [(value, code, reason)])."""
    if shape == 0:
        k = a + b * c - d
        return (f"{a} + {b} × {c} − {d}", k, f"Multiply first: {b} × {c} = {b*c}. Then go left to right: {a} + {b*c} − {d}.",
                f"{k} is right: {a} + {b*c} = {a+b*c}, and {a+b*c} − {d} = {k}.",
                [((a + b) * c - d, "NUM-ORDER-OPS", f"works left to right: ({a} + {b}) × {c} − {d}. Multiplication comes first."),
                 (a + b * (c - d), "NUM-ORDER-OPS", f"subtracts {d} from {c} before multiplying, which the expression does not say."),
                 (a + b + c - d, "NUM-OP-SWAP", f"adds {b} and {c} instead of multiplying them."),
                 (a + b * c, "NUM-PARTIAL", f"stops before subtracting {d}.")])
    if shape == 1:
        k = (a + b) * c - d
        return (f"({a} + {b}) × {c} − {d}", k, f"Brackets first: {a} + {b} = {a+b}. Then multiply: {a+b} × {c} = {(a+b)*c}. Then subtract {d}.",
                f"{k} is right: ({a} + {b}) × {c} = {(a+b)*c}, and {(a+b)*c} − {d} = {k}.",
                [(a + b * c - d, "NUM-ORDER-OPS", f"ignores the brackets and multiplies {b} × {c} first."),
                 ((a + b) * c, "NUM-PARTIAL", f"stops before subtracting {d}."),
                 ((a + b) * (c - d), "NUM-ORDER-OPS", f"subtracts {d} from {c} before multiplying."),
                 ((a + b) + c - d, "NUM-OP-SWAP", f"adds {c} instead of multiplying by it.")])
    if shape == 2:
        d = d if d >= 2 else 3
        e = c * d
        k = a * b - c
        out = []
        if (a * b - e) % d == 0:
            out.append(((a * b - e) // d, "NUM-ORDER-OPS", f"works left to right: ({a} × {b} − {e}) ÷ {d}. Division comes before subtraction."))
        out += [(a * b - e, "NUM-PARTIAL", f"skips the division and subtracts all of {e}."),
                (a * b + c, "NUM-OP-SWAP", f"adds {c} instead of subtracting it."),
                (a + b - c, "NUM-OP-SWAP", f"adds {a} and {b} instead of multiplying them.")]
        return (f"{a} × {b} − {e} ÷ {d}", k, f"Do × and ÷ first: {a} × {b} = {a*b} and {e} ÷ {d} = {c}. Then subtract.",
                f"{k} is right: {a*b} − {c} = {k}.", out)
    if shape == 3:
        k = a - b * c + d
        return (f"{a} − {b} × {c} + {d}", k, f"Multiply first: {b} × {c} = {b*c}. Then go left to right: {a} − {b*c} + {d}.",
                f"{k} is right: {a} − {b*c} = {a-b*c}, and {a-b*c} + {d} = {k}.",
                [((a - b) * c + d, "NUM-ORDER-OPS", f"works left to right: ({a} − {b}) × {c} + {d}. Multiplication comes first."),
                 (a - b * c - d, "NUM-OP-SWAP", f"subtracts {d} instead of adding it."),
                 (a - (b * c + d), "NUM-ORDER-OPS", f"adds {d} to {b*c} before subtracting, so {d} is wrongly taken away."),
                 (a + b * c + d, "NUM-OP-SWAP", f"adds {b*c} instead of subtracting it.")])
    if shape == 4:
        k = a + b * (c - d)
        return (f"{a} + {b} × ({c} − {d})", k, f"Brackets first: {c} − {d} = {c-d}. Then multiply: {b} × {c-d} = {b*(c-d)}. Then add {a}.",
                f"{k} is right: {a} + {b*(c-d)} = {k}.",
                [((a + b) * (c - d), "NUM-ORDER-OPS", f"adds {a} and {b} before multiplying."),
                 (a + b * c - d, "NUM-ORDER-OPS", f"ignores the brackets and multiplies {b} × {c} first."),
                 (b * (c - d), "NUM-PARTIAL", f"stops before adding {a}."),
                 (a + b * (c + d), "NUM-OP-SWAP", f"adds {d} inside the brackets instead of subtracting it.")])
    if shape == 5:
        d = next(x for x in ([d] if d >= 2 else []) + [2, 3, 4, 5, 7] if (a * b) % x == 0)
        g = 2 * c + (-2 * c) % d
        k = (a * b + g) // d
        out = []
        if g % d == 0:
            out.append((a * b + g // d, "NUM-ORDER-OPS", f"ignores the brackets and divides only {g} by {d}."))
        out.append((a * b + g, "NUM-PARTIAL", f"stops before dividing by {d}."))
        if (a * b - g) % d == 0:
            out.append(((a * b - g) // d, "NUM-OP-SWAP", f"subtracts {g} instead of adding it."))
        if (a * (b + g)) % d == 0:
            out.append((a * (b + g) // d, "NUM-ORDER-OPS", f"adds {b} and {g} before multiplying by {a}."))
        out.append(((a + b + g) // d if (a + b + g) % d == 0 else None, "NUM-OP-SWAP", f"adds {a} and {b} instead of multiplying them."))
        out.append((a * b // d + g if (a * b) % d == 0 else None, "NUM-ORDER-OPS", f"divides only {a} × {b} by {d}, then adds {g}."))
        return (f"({a} × {b} + {g}) ÷ {d}", k, f"Inside the brackets, multiply first: {a} × {b} = {a*b}, plus {g} is {a*b+g}. Then divide by {d}.",
                f"{k} is right: {a*b+g} ÷ {d} = {k}.", [x for x in out if x[0] is not None])


def mark(it, note):
    if it.get("review_status") != CHANGED:
        it["previous_review"] = it.get("previous_review") or {"reviewer": it.get("reviewer"), "reviewed_at": it.get("reviewed_at")}
        it.update(status="draft", review_status=CHANGED, reviewer=None, reviewed_at=None)
        it.pop("review_line", None)
    it["notes"] = ((it.get("notes") or "") + " " + note).strip()


def run():
    log, n_ops, n_ver, n_sw, n_sr = [], 0, {}, 0, 0
    keep_bc = {"subject-verb agreement": 16}
    for p in sorted(glob.glob(os.path.join(DOCS, "batch-*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        for it in d["items"]:
            s = it["stem"]
            if it["archetype"] == "NUM-OPS-ORDER":
                import re
                a, b, c, dd = map(int, re.findall(r"\d+", s))
                shape = n_ops % 6
                n_ops += 1
                if shape == 0:
                    continue
                expr, k, sc, wc, wrong = ops(a, b, c, dd, shape)
                ids = [o["option_id"] for o in it["options"]]
                key = it["answer_option_id"]
                vals, picks = {k}, []
                for v, code, why in wrong:
                    if v not in vals and len(picks) < 3:
                        vals.add(v); picks.append((v, code, why))
                assert len(picks) == 3, (it["id"], expr, wrong)
                texts = {key: str(k)}
                others = [x for x in ids if x != key]
                for oid, (v, code, why) in zip(others, picks):
                    texts[oid] = str(v)
                for o in it["options"]:
                    o["text"] = texts[o["option_id"]]
                it["stem"] = f"What is the value of {expr}?"
                it["gen_sig"] = it["stem"]
                it["reveal"]["shortcut"] = sc
                it["reveal"]["why_correct"] = wc
                it["reveal"]["why_wrong"] = {oid: f"{v} {why}" for oid, (v, code, why) in zip(others, picks)}
                it["distractor_reasoning"] = {oid: code for oid, (v, code, why) in zip(others, picks)}
                mark(it, f"Round 02 fix: order-of-operations shape changed ({s} -> {it['stem']}), key recomputed ({k}).")
                log.append((it["id"], s, it["stem"], str(k)))
            elif s.startswith(BC) and it["concept"] in VERB_FRAMES:
                cpt = it["concept"]
                n_ver[cpt] = n_ver.get(cpt, 0) + 1
                if n_ver[cpt] <= keep_bc.get(cpt, 0):
                    continue
                it["stem"] = VERB_FRAMES[cpt] + s[len(BC):]
                if it.get("gen_sig") == s:
                    it["gen_sig"] = it["stem"]
                mark(it, "Round 02 fix: stem phrasing changed (frame cap); sentence, options and key unchanged.")
                log.append((it["id"], s, it["stem"], "key unchanged"))
            elif it["archetype"] in ("CLR-SPELL-WRONG", "CLR-SPELL-RIGHT"):
                fr = SPELL_WRONG if it["archetype"] == "CLR-SPELL-WRONG" else SPELL_RIGHT
                i = n_sw if it["archetype"] == "CLR-SPELL-WRONG" else n_sr
                if it["archetype"] == "CLR-SPELL-WRONG":
                    n_sw += 1
                else:
                    n_sr += 1
                q = fr[i % len(fr)]
                body = s.split("  ", 1)[1]
                it["stem"] = q + "  " + body
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    return log


if __name__ == "__main__":
    for row in run():
        print(*row, sep="\t")
