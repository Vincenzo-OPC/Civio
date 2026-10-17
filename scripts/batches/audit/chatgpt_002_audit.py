"""Round 03 audit of chatgpt-batch-002.json (100 English Verbal drafts). Applies the two clear text errors, keeps everything draft,
and writes docs/research/audit/round-03-chatgpt-002-review-request.md."""
import json, re, sys, os
from collections import Counter
sys.path.insert(0, "scripts/batches")
P = "docs/research/chatgpt-batch-002.json"
raw = open(P).read(); d = json.loads(raw)
FIXES = {"050004": ("The teachers planned a follow-up", "The office planned a follow-up", "'teachers' contradicted the passage (the agriculture office runs the training)"),
         "050006": ("to reach the shelter and share the results", "to reach the shelter, and it shared the results", "broken verb ('and share')")}
log = []
for it in d["items"]:
    s = it["id"][-6:]
    if s in FIXES:
        a, b, why = FIXES[s]
        if a in it["stem"]:
            it["stem"] = it["stem"].replace(a, b)
            it["notes"] = (it.get("notes", "") + f" | Grok Bot audit 2026-10-17: fixed {why}. Still draft.").lstrip(" |")
            log.append(s)
open(P, "w").write(json.dumps(d, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""))
items = d["items"]
AMBIG = {"050028": "Listing farmers' needs and checking the storeroom are independent; the swap order B-D-C-A is just as defensible.",
         "050033": "Taking requests and counting stock are independent; the swap order D-B-A-C is just as defensible."}
NONWORD = {"050083": "balancedly", "050090": "detailedly, workably", "050092": "measur, stor", "050097": "plann", "050099": "guid"}
V, R = {}, {}
for it in items:
    s, a = it["id"][-6:], it["archetype"]
    if "RC" in a:
        V[s] = "FIX"; R[s] = "Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences."
    elif a == "VEN-PARA-ORDER":
        V[s] = "REJECT"; R[s] = AMBIG.get(s, "Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences.")
    else:
        V[s] = "REJECT"; R[s] = ("Non-words in the choices (" + NONWORD[s] + "), which breaks the keyboard-typo rule. " if s in NONWORD else "") + {
            "VEN-ERROR-AGREE": "One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...').",
            "VEN-ERROR-TENSE": "One frame repeated 5 times (past time marker + will/-s/-ing/-ed).",
            "VEN-ERROR-MODIFIER": "One frame repeated 20 times (three-item adjective or gerund series with one form changed)."}[a]
c = Counter(V.values())
ac = Counter(it["archetype"] for it in items)
keys = Counter(it["answer_option_id"] for it in items)
L = ["# Round 03 audit: ChatGPT batch 002 (100 English Verbal drafts), review request for Chief of Staff", "",
     "Grok Bot, 2026-10-17. File: `docs/research/chatgpt-batch-002.json`. **Everything stays draft/unreviewed.** Built by `scripts/batches/audit/chatgpt_002_audit.py`.", "",
     "## Mechanical QA", "",
     "`qa_file.py` finds 0 problems: required fields, 4 distinct choices, valid codes, no near-duplicate (0.65) against the bank or the baseline, and no order key that matches its listed order. Mechanical QA passes, but the content does not meet the bar.", "",
     f"Mix: {dict(ac)}. Keys: {dict(sorted(keys.items()))} (o2 is under-used).", "",
     "## Findings", "",
     "1. **Error recognition (40): REJECT all.** There are only 4 sentence frames, each repeated with the nouns swapped:",
     "   - 15 agreement items, all \"The <noun> of the <nouns> is ...\";",
     "   - 5 tense items, all a past time marker followed by will/-s/-ing/-ed;",
     "   - 10 adjective series;",
     "   - 10 gerund series.",
     "   The three wrong choices are always the same sentence with one form changed, so the key is simply the one that looks normal. Five items use non-words (balancedly, detailedly, workably, measur, stor, plann, guid), which breaks the keyboard-typo rule. Some choices are ungrammatical in two ways at once (\"are being available\"). The context sentence in each stem plays no part in the question.",
     "2. **Paragraph organization (35): REJECT all.**",
     "   - Every paragraph is the same four-step story: report, check, fix, verify.",
     "   - The sentences carry explicit time cues (\"after the inspection\", \"before reopening\").",
     "   - Keys rotate through 7 fixed patterns, and the LOG-ORDER-SWAP trap always swaps the first two sentences.",
     "   - Two items have a second defensible order: 050028 and 050033.",
     "   - The why-wrong lines all use one template (\"X appears before Y even though the latter must happen first\"), which is false for those two.",
     "3. **Reading comprehension (25): FIX and keep.**",
     "   - Passages are original, 159–187 words, and set in the Philippines.",
     "   - Each item has one defensible key, and the keys are correct.",
     "   - The weaknesses:",
     "     - (a) All 25 passages carry the same lesson: a first measurement misled, then a better measure was used. Spread across the bank that is fine, but within one batch it is monotonous.",
     "     - (b) Most items have 1–2 absurd or extreme distractors (\"Printed text had been banned from the entire museum\", \"sell forever\"), so the nuanced key stands out.",
     "     - (c) Each passage ends with about two padded sentences that the question never uses.",
     "   - Clear errors fixed now (text only, key unchanged): 050004 said 'teachers' where the passage means the agriculture office; 050006 had a broken verb ('and share').", "",
     f"**Proposed:** FIX {c['FIX']} (all RC), REJECT {c['REJECT']} (all para-order and error items). The rejected areas are rewritten from scratch in **gap-fill-005** (20 RC, 20 paragraph organization, 20 sentence structure), so the bank still gains coverage there.", "",
     "## Per item", "", "| ID | Archetype | Verdict | Reason |", "|---|---|---|---|"]
for it in items:
    s = it["id"][-6:]
    L.append(f"| {it['id']} | {it['archetype']} | {V[s]} | {R[s]} |")
L += ["", "## Asks for CoS", "",
      "1. Approve rejecting the 75 templated para-order and error items, with gap-fill-005 as the replacement.",
      "2. For the 25 RC items, choose between (a) Grok Bot rewriting the weak distractors and trimming the tails, then bringing them back for a pass, and (b) keeping only about 10 of them because of the single theme.",
      "3. Ask ChatGPT not to reuse batch 002's frames in batch 004 (`CHATGPT_NEXT_PROMPT.md` already bans copying 002)."]
open("docs/research/audit/round-03-chatgpt-002-review-request.md", "w").write("\n".join(L) + "\n")
print(c, "fixed:", log)
