"""gap-fill-005: 60 original English Verbal drafts (20 reading comprehension, 20 paragraph organization, 20 sentence structure).
Written by Grok Bot 2026-10-17 for the thin areas the Sentinel dossier found and to replace the 75 rejected batch-002 items. Writes docs/research/gap-fill-005.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gap_fill_005_rc import RC
from gap_fill_005_po import ORDER, INSERT
from gap_fill_005_ss import SS, STEMS, TOPIC
IDS = ["o1", "o2", "o3", "o4"]
items = []
def add(arch, comp, concept, micro, diff, secs, stem, choices, terms, method, sc, rotate=None):
    if rotate is not None:  # place the key at a fixed position to balance keys
        key = next(c for c in choices if c[1] is None); rest = [c for c in choices if c[1] is not None]
        choices = rest[:rotate] + [key] + rest[rotate:]
    k = next(IDS[i] for i, c in enumerate(choices) if c[1] is None)
    n = len(items) + 1
    it = {"id": f"CIVIO-GAP5-{arch}-{n:04d}", "track": "both", "domain": "verbal_en", "competency": comp, "concept": concept, "micro_skill": micro,
          "archetype": arch, "difficulty": diff, "est_seconds": secs, "language": "en", "stem": stem,
          "options": [{"option_id": IDS[i], "text": c[0]} for i, c in enumerate(choices)], "answer_option_id": k,
          "reveal": {"terms": terms, "shortcut": method, "why_correct": choices[IDS.index(k)][2],
                     "why_wrong": {IDS[i]: c[2] for i, c in enumerate(choices) if c[1]}},
          "distractor_reasoning": {IDS[i]: c[1] for i, c in enumerate(choices) if c[1]},
          "source": "Original, Civio", "source_url": None, "source_group": "civio", "status": "draft", "review_status": "unreviewed",
          "reviewer": None, "reviewed_at": None,
          "provenance": {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-17T16:30:00+08:00", "spec_version": "0.1.8"},
          "_legacy": True}
    if sc: it["shortcut"] = sc
    items.append(it)
MICRO = {"VEN-RC-MAIN": "identify the main idea or best title", "VEN-RC-DETAIL": "locate a stated detail", "VEN-RC-INFER": "draw a supported inference", "VEN-RC-VOCAB": "use context to find a word's meaning"}
SECS = {"VEN-RC-MAIN": 75, "VEN-RC-DETAIL": 60, "VEN-RC-INFER": 80, "VEN-RC-VOCAB": 55}
for j, (arch, diff, lead, passage, q, ch, terms, method, sc) in enumerate(RC):
    add(arch, "Reading comprehension", "reading comprehension", MICRO[arch], diff, SECS[arch], f"{lead}\n\n{passage}\n\n{q}", ch, terms, method, sc, rotate=(j * 3 + 1) % 4)
for diff, stem, ch, terms, method, sc in ORDER:
    add("VEN-PARA-ORDER", "Paragraph organization", "ordering", "order sentences using topic sentences, pointer words and transitions", diff, 75, stem, ch, terms, method, sc)
for diff, para, ins, key, wrong, why_ok, terms, method, sc in INSERT:
    pos = sorted(set(wrong) | {key})
    ch = [(f"After sentence {p}", None if p == key else wrong[p][0], why_ok if p == key else wrong[p][1]) for p in pos]
    add("VEN-PARA-INSERT", "Paragraph organization", "sentence insertion", "place an added sentence using its pointer words", diff, 70,
        f"Where does the following sentence best fit in the paragraph?\n\"{ins}\"\n\n{para}", ch, terms, method, sc)
for j, (diff, special, key, wrong, method) in enumerate(SS):
    ch = [(key, None, "It is the only choice that is one complete, correctly joined sentence with every describing phrase in place. " + method)] + list(wrong)
    add("VEN-SENT-STRUCTURE", "Sentence structure", "sentence structure", "recognize run-ons, fragments and misplaced modifiers", diff, 40,
        special or STEMS[j % len(STEMS)].format(TOPIC[j]), ch, "Run-on: two sentences joined with only a comma or nothing. Fragment: words punctuated as a sentence without a main clause. Misplaced or dangling modifier: a describing phrase attached to the wrong word.",
        method, None, rotate=(j + 2) % 4)
from collections import Counter
print(len(items), Counter(i["archetype"] for i in items), Counter(i["answer_option_id"] for i in items))
json.dump({"batch": "gap-fill-005", "spec_version": "0.1.8", "status": "draft (awaiting CoS)", "source_group": "civio",
           "notes": "Original English Verbal drafts for thin areas (Sentinel dossier) and to replace the rejected batch-002 para-order and error items. Sentence-structure codes VEN-RUN-ON, VEN-FRAGMENT, VEN-MODIFIER-PLACE are proposed (spec 0.1.9, pending CoS). _legacy: hand-written, so no generator solver applies.",
           "items": items}, open("docs/research/gap-fill-005.json", "w"), ensure_ascii=False, indent=2)
