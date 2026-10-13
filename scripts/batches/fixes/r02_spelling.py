"""Round 02 fix 1 + 4: rewrite every batch spelling item with a unique real misspelling target (CoS ruling, 2026-10-13)."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fixes.spell_words import T, FOILS, EXPLAIN, check_code
from build import DOCS
CHANGED = "changed (round 02 fixes; awaiting CoS review)"

def run():
    targets = iter(T)
    foil_i = 0
    changed = []
    for p in sorted(glob.glob(os.path.join(DOCS, "batch-*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        for it in d["items"]:
            a = it["archetype"]
            if a not in ("CLR-SPELL-RIGHT", "CLR-SPELL-WRONG"):
                continue
            w, ms = next(targets)
            for m, c in ms:
                assert check_code(w, m, c), (w, m, c)
            ids = [o["option_id"] for o in it["options"]]
            key = it["answer_option_id"]
            others = [x for x in ids if x != key]
            old = {o["option_id"]: o["text"] for o in it["options"]}[key]
            if a == "CLR-SPELL-RIGHT":
                texts = {key: w}
                for oid, (m, c) in zip(others, ms):
                    texts[oid] = m
                it["reveal"]["why_correct"] = f"\"{w}\" is the standard spelling."
                it["reveal"]["why_wrong"] = {oid: f"\"{m}\" {EXPLAIN[c]}. The correct spelling is \"{w}\"." for oid, (m, c) in zip(others, ms)}
                it["distractor_reasoning"] = {oid: c for oid, (m, c) in zip(others, ms)}
                it["gen_sig"] = "R:" + w
            else:
                m, c = ms[0]
                texts = {key: m}
                for oid in others:
                    texts[oid] = FOILS[foil_i % len(FOILS)]; foil_i += 1
                it["reveal"]["why_correct"] = f"\"{m}\" is misspelled: it {EXPLAIN[c]}. The correct spelling is \"{w}\"."
                it["reveal"]["why_wrong"] = {oid: f"\"{texts[oid]}\" is spelled correctly, even if it looks unusual." for oid in others}
                it["distractor_reasoning"] = {oid: "CLR-SPELL-CORRECT-FOIL" for oid in others}
                it["gen_sig"] = "W:" + m
                it["error_code"] = c
            for o in it["options"]:
                o["text"] = texts[o["option_id"]]
            q = "Which word is spelled correctly?" if a == "CLR-SPELL-RIGHT" else "Which word is misspelled?"
            it["stem"] = q + "  " + " | ".join(o["text"] for o in it["options"])
            it["reveal"]["shortcut"] = "Check the usual traps: doubled letters, i before e, silent letters, and sound-alike endings such as -ance/-ence."
            it["previous_review"] = {"reviewer": it.get("reviewer"), "reviewed_at": it.get("reviewed_at"), "old_target": old}
            it.update(status="draft", review_status=CHANGED, reviewer=None, reviewed_at=None)
            it["notes"] = f"Round 02 fix: target replaced ({old} -> {w}) per CoS ruling 2026-10-13."
            it.pop("review_line", None)
            changed.append((it["id"], old, texts[key], w))
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    return changed

if __name__ == "__main__":
    for c in run():
        print(*c, sep="\t")
