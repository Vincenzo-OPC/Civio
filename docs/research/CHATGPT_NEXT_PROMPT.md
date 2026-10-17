# Prompt for ChatGPT: next English Verbal batch

GT: paste everything below the line into ChatGPT. **Note:** `docs/research/chatgpt-batch-002.json` already holds 100 English drafts covering these same three areas. They are still `draft` / `unreviewed`, and Grok Bot hasn't audited them yet. So this prompt asks for a **new** file, `chatgpt-batch-004.json` (003 is Codex's GI batch). It also tells ChatGPT not to repeat any passage, topic or sentence from 002. If you meant for ChatGPT to redo 002 itself, change the file name in step 1.

---

You are writing practice questions for **Civio**, a reviewer for the Philippine Civil Service Exam (Subprofessional level first). Civio is not affiliated with the Civil Service Commission; never say or imply that it is. Work in the GitHub repo `Vincenzo-OPC/Civio`, branch `main`. Before writing, read `docs/CSE-Question-Design-Spec.md` (v0.1.8 or later) and `docs/research/AUDIT_TRACKER.md`, then pull the latest `main` (others push at the same time; never force-push).

## Task

1. Create `docs/research/chatgpt-batch-004.json` with **100 English Verbal draft items**, using the same top-level keys as `chatgpt-batch-002.json` (`batch`, `spec_version`, `status`, `source_group`, `notes`, `items`):
   - **30 reading comprehension:** 30 new passages, one question each. Archetypes: about 8 `VEN-RC-MAIN`, 8 `VEN-RC-DETAIL`, 10 `VEN-RC-INFER`, 4 `VEN-RC-VOCAB`. Passages run 120 to 220 words and use Philippine office, community or public-service settings. They must be original, with no copied text.
   - **30 paragraph organization:** about 20 `VEN-PARA-ORDER` and 10 `VEN-PARA-INSERT`. Use 4 or 5 sentences each, and mix the labels (A-D, 1-4, or P-Q-R-S).
   - **40 error recognition:** about 12 `VEN-ERROR-AGREE`, 10 `VEN-ERROR-TENSE`, 10 `VEN-ERROR-MODIFIER` and 8 `VEN-SENT-STRUCTURE`. Spread these across pronoun case, collective nouns, either/or, tense signals, adjective vs adverb, comparisons, parallelism, dangling or misplaced modifiers, run-ons and fragments.
2. IDs: `CIVIO-<ARCHETYPE>-07xxxx`, starting at 070001. Every item has `status: "draft"`, `review_status: "unreviewed"`, `reviewer: null`, `reviewed_at: null`, `source_group: "civio"`, `track: "both"`, `domain: "verbal_en"`, `language: "en"`, and `provenance` = {author, method: "ai_assisted", created_at (ISO 8601 with +08:00), spec_version}.
3. Add a dated section to `docs/research/AUDIT_TRACKER.md` with the counts and anything you were unsure about. Commit with `[skip netlify]` in the message, pull with rebase, then push normally.

## Item rules (every item)

- Exactly 4 options, all different, with one correct answer and no second defensible answer. `answer_option_id` names the key. Spread keys evenly over o1-o4.
- The required fields from the spec: `id, track, domain, competency, concept, micro_skill, archetype, difficulty, est_seconds, language, stem, options, answer_option_id, reveal, distractor_reasoning, source, source_url, source_group, status, review_status, provenance`.
- `reveal` has `terms`, `shortcut` (the worked method, shown as "Method"), `why_correct`, and `why_wrong` with **one specific reason per wrong option**. Each reason says what that option gets wrong. Never write a template like "concerns a different concept", and never repeat the option text as the whole reason.
- `distractor_reasoning` gives every wrong option a code from the spec: `VEN-NEAREST-NOUN`, `VEN-TENSE`, `VEN-FORM`, `VEN-HOMOPHONE`, `VEN-PARTICLE`, `VEN-REGISTER`, `RC-NOT-IN-TEXT`, `RC-TOO-BROAD`, `RC-TOO-NARROW`, `RC-EXTREME`, `RC-OPPOSITE`, `RC-SUPPORTED-NOT-ASKED`, `LOG-ORDER-SWAP`, `LOG-ORDER-REVERSED`, `LOG-IGNORED-CLUE`. The code must describe the actual error in that option. Don't invent codes; if none fits, say so in `notes`.
- Distractors must be plausible to a real examinee. No joke options. A wrong option should come from a real misreading or a common grammar mistake.
- Never name a choice by letter or position ("option B", "the first choice") in any explanation. Choices are shuffled in the app.
- Use person names with matching pronouns, and use Filipino names and settings naturally.
- **Optional item-level `shortcut` field** (spec v0.1.7): one short, honest technique for solving the item, under 300 characters. Examples: "Cross out the phrase between the subject and the verb, then match the verb to the subject." or "The topic sentence names the subject without pointing back to anything." Include it only when a real technique exists, and never pad it. It is separate from `reveal.shortcut`.

## Rules added since batch 002 (Civio's QA script checks these)

- **No keyboard typos as "errors."** In error-recognition items the error must be a real grammar or usage mistake people make, never a random letter slip. Spelling is Clerical's job, so don't test spelling here.
- **Unique targets.** Don't test the same target sentence, word pair or rule example twice in this batch, and don't reuse any stem, passage or target from `chatgpt-batch-002.json`, `docs/batches/batch-*.json` or the other files in `docs/research/`. Near-duplicates (token overlap of 0.65 or more against any existing stem) fail QA.
- **No order key may match the listed order.** In ordering items the correct order must never be A-B-C-D (or 1-2-3-4, or the order the sentences are printed in). Each wrong order gets its own code: one `LOG-ORDER-SWAP`, one `LOG-ORDER-REVERSED`, one `LOG-IGNORED-CLUE`.
- **25% stem cap.** QA fails any stem wording used in more than 25% of a domain's items across the bank, so keep every lead-in under 25% of this batch too (for example, at most 10 of the 40 error items may start "Which sentence has an error..."). Vary the lead-ins.
- **One defensible answer in inference items.** Every RC inference must be supported by the passage. Wrong options should go beyond the text, overstate it with words like always/never/completely, or reverse it.
- **Shortcut honesty.** A shortcut must give the right answer when applied to the item. If it doesn't, leave it out.
- **KWF spelling (Filipino text only).** If any Filipino words appear (names of places or offices are fine), follow KWF: use reduplicated forms like *nakasasakit*, never *nakaka-*, and write *kaniya/kaniyang*, never *kanya/kanyang*.

## What not to do

- Don't edit any existing batch, test or app code, and don't mark anything approved. Grok Bot audits next, then Chief of Staff gives final approval.
- Don't import, activate or deploy anything.
- If you can't run `python3 scripts/batches/qa.py`, say so in the tracker instead of claiming it passed.
