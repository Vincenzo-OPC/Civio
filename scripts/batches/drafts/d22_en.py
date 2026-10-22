"""Verbal (English) drafts, 22 Oct 2026: 30 paragraph-order, 15 sentence-insertion, 18 reading passages x 3 questions.
Order keys are computed by script from the authored sentence order; the meaning judgments need a human reviewer (recipe judgment)."""
import random
from d22_common import mk
from en_text_2026_10_22 import PARA, INSERT
from en_rc_2026_10_22 import RC

D, T = "verbal_en", "both"
J = {"op": "judgment", "why": "paragraph logic / reading judgment; order keys computed from the authored order"}
ITEMS = []
L = "PQRS"
FR = ["Arrange the sentences to form a logical paragraph. Which order is correct?",
      "Which sequence of sentences P, Q, R and S makes the most logical paragraph?",
      "Put the sentences below in the best order. Which arrangement is correct?"]
PERMS = [((0, 2, 1, 3), "LOG-ORDER-SWAP", "This swaps the middle two sentences, so a sentence comes before the idea it builds on{clue_short}"),
         ((3, 2, 1, 0), "LOG-ORDER-REVERSED", "This runs the paragraph backward, so it ends with the topic sentence and opens with the conclusion."),
         ((1, 0, 2, 3), "PO-OPENER-MISPLACED", "This opens with a supporting sentence; the topic sentence must come first."),
         ((0, 1, 3, 2), "PO-TRANSITION-IGNORED", "This puts the closing sentence before the sentence it depends on.")]
for n, (sents, clue) in enumerate(PARA, 1):
    iid = f"CIVIO-D1022-VEN-PO-{n:04d}"
    rnd = random.Random(iid)
    while True:
        lab = list(L); rnd.shuffle(lab)  # lab[i] = label of the sentence in correct position i
        key = "-".join(lab)
        if key.replace("-", "") != L:
            break
    listed = sorted(range(4), key=lambda i: lab[i])
    stem = FR[n % 3] + "\n" + "\n".join(f"{lab[i]}. {sents[i]}" for i in listed)
    wrong, used = [], set()
    for perm, code, why in PERMS:
        t = "-".join(lab[i] for i in perm)
        if t == key or t.replace("-", "") == L or t in used or len(wrong) == 3:
            continue
        used.add(t)
        wrong.append((t, code, why.format(clue_short=".")))
    ITEMS.append(mk(id=iid, track=T, domain=D, competency="Paragraph organization", concept="ordering",
                    micro_skill="order sentences using the topic sentence, pointer words and transitions", archetype="VEN-PARA-ORDER",
                    difficulty="medium", est=75, stem=stem, correct=key, wrong=wrong,
                    terms="Paragraph order: the topic sentence needs nothing before it; pointer words (this, these, such, they) and transitions (however, therefore, as a result) must follow what they refer to.",
                    shortcut="Find the sentence that can stand first on its own, then chain each pointer word to the sentence it points back to.",
                    why_correct=f"Answer: \"{key}\". {clue[0].upper() + clue[1:]}. Read in this order, every pointer word has something before it to refer to.",
                    recipe=J))

IF = ["Where does the following sentence best fit in the paragraph?", "Read the paragraph. After which sentence should the added sentence be placed?"]
for n, (sents, new, k, clue) in enumerate(INSERT, 1):
    iid = f"CIVIO-D1022-VEN-INS-{n:04d}"
    stem = IF[n % 2] + f"\n\"{new}\"\n\n" + " ".join(f"({i + 1}) {s}" for i, s in enumerate(sents))
    wrong = []
    for j in range(1, 5):
        if j == k:
            continue
        code = "PO-TRANSITION-IGNORED" if abs(j - k) == 1 else "LOG-IGNORED-CLUE"
        why = (f"After sentence {j}, the added sentence would sit next to an idea it does not refer to; " if j != 4 else "At the end, the added sentence would come after the paragraph's closing point; ") + f"it belongs after sentence {k} because {clue}."
        wrong.append((f"After sentence {j}", code, why))
    ITEMS.append(mk(id=iid, track=T, domain=D, competency="Paragraph organization", concept="sentence insertion",
                    micro_skill="place an added sentence using its pointer words", archetype="VEN-PARA-INSERT", difficulty="medium", est=70,
                    stem=stem, correct=f"After sentence {k}", wrong=wrong,
                    terms="Sentence insertion: an added sentence goes right after the sentence its pointer words (this, these, such, also, for example) refer to.",
                    shortcut="Underline the pointer word in the added sentence and find the sentence that names what it points to.",
                    why_correct=f"Answer: \"After sentence {k}\". The added sentence fits there because {clue}; the sentence that follows still reads smoothly.",
                    recipe=J))

for p, (title, text, qs) in enumerate(RC, 1):
    pid = f"CIVIO-D1022-VEN-RC-P{p:02d}"
    for q, (arch, question, key, wrong, why) in enumerate(qs, 1):
        iid = f"CIVIO-D1022-VEN-RC-{p:02d}{q}"
        stem = "Read the passage, then answer the question.\n\n" + text + "\n\n" + question
        ITEMS.append(mk(id=iid, track=T, domain=D, competency="Reading comprehension",
                        concept={"VEN-RC-MAIN": "main idea", "VEN-RC-DETAIL": "stated detail", "VEN-RC-INFER": "inference", "VEN-RC-VOCAB": "vocabulary in context"}[arch],
                        micro_skill={"VEN-RC-MAIN": "choose the statement that covers the whole passage", "VEN-RC-DETAIL": "find the stated fact",
                                     "VEN-RC-INFER": "draw the conclusion the passage supports", "VEN-RC-VOCAB": "use context to fix a word's meaning"}[arch],
                        archetype=arch, difficulty={"VEN-RC-DETAIL": "easy", "VEN-RC-VOCAB": "easy"}.get(arch, "medium"),
                        est={"VEN-RC-MAIN": 60, "VEN-RC-DETAIL": 45, "VEN-RC-INFER": 70, "VEN-RC-VOCAB": 40}[arch],
                        stem=stem, correct=key, wrong=[(w, c, y) for w, c, y in wrong],
                        terms={"VEN-RC-MAIN": "Main idea: the statement that covers the whole passage, neither one detail (too narrow) nor a topic bigger than the text (too broad).",
                               "VEN-RC-DETAIL": "Stated detail: the answer is written in the passage; find the sentence and match it.",
                               "VEN-RC-INFER": "Inference: a conclusion the passage supports without saying it word for word; reject choices that go beyond the text or use extreme words.",
                               "VEN-RC-VOCAB": "Vocabulary in context: the meaning the word has in this sentence, which may differ from its most common meaning."}[arch],
                        shortcut={"VEN-RC-MAIN": "Ask which choice the first and last sentences would both agree with.",
                                  "VEN-RC-DETAIL": "Scan for the key noun in the question, then read that sentence closely.",
                                  "VEN-RC-INFER": "Find the sentence the question points to, then pick the choice that follows from it with no extra assumptions.",
                                  "VEN-RC-VOCAB": "Replace the word with each choice and keep the one that leaves the sentence's meaning unchanged."}[arch],
                        why_correct=f"Answer: \"{key}\". {why}",
                        passage_id=pid, recipe=J,
                        notes=f"New original draft, 22 Oct 2026 (GT approved). Passage {pid} (\"{title}\"), question {q} of {len(qs)}."))
