# Round 03 audit: ChatGPT batch 002 (100 English Verbal drafts), review request for Chief of Staff

Grok Bot, 2026-10-17. File: `docs/research/chatgpt-batch-002.json`. **Everything stays draft/unreviewed.** Built by `scripts/batches/audit/chatgpt_002_audit.py`.

## Mechanical QA

`qa_file.py` finds 0 problems: required fields, 4 distinct choices, valid codes, no near-duplicate (0.65) against the bank or the baseline, and no order key that matches its listed order. Mechanical QA passes, but the content does not meet the bar.

Mix: {'VEN-RC-INFER': 20, 'VEN-RC-DETAIL': 2, 'VEN-RC-MAIN': 3, 'VEN-PARA-ORDER': 35, 'VEN-ERROR-AGREE': 15, 'VEN-ERROR-TENSE': 5, 'VEN-ERROR-MODIFIER': 20}. Keys: {'o1': 32, 'o2': 16, 'o3': 27, 'o4': 25} (o2 is under-used).

## Findings

1. **Error recognition (40): REJECT all.** There are only 4 sentence frames, each repeated with the nouns swapped:
   - 15 agreement items, all "The <noun> of the <nouns> is ...";
   - 5 tense items, all a past time marker followed by will/-s/-ing/-ed;
   - 10 adjective series;
   - 10 gerund series.
   The three wrong choices are always the same sentence with one form changed, so the key is simply the one that looks normal. Five items use non-words (balancedly, detailedly, workably, measur, stor, plann, guid), which breaks the keyboard-typo rule. Some choices are ungrammatical in two ways at once ("are being available"). The context sentence in each stem plays no part in the question.
2. **Paragraph organization (35): REJECT all.**
   - Every paragraph is the same four-step story: report, check, fix, verify.
   - The sentences carry explicit time cues ("after the inspection", "before reopening").
   - Keys rotate through 7 fixed patterns, and the LOG-ORDER-SWAP trap always swaps the first two sentences.
   - Two items have a second defensible order: 050028 and 050033.
   - The why-wrong lines all use one template ("X appears before Y even though the latter must happen first"), which is false for those two.
3. **Reading comprehension (25): FIX and keep.**
   - Passages are original, 159–187 words, and set in the Philippines.
   - Each item has one defensible key, and the keys are correct.
   - The weaknesses:
     - (a) All 25 passages carry the same lesson: a first measurement misled, then a better measure was used. Spread across the bank that is fine, but within one batch it is monotonous.
     - (b) Most items have 1–2 absurd or extreme distractors ("Printed text had been banned from the entire museum", "sell forever"), so the nuanced key stands out.
     - (c) Each passage ends with about two padded sentences that the question never uses.
   - Clear errors fixed now (text only, key unchanged): 050004 said 'teachers' where the passage means the agriculture office; 050006 had a broken verb ('and share').

**Proposed:** FIX 25 (all RC), REJECT 75 (all para-order and error items). The rejected areas are rewritten from scratch in **gap-fill-005** (20 RC, 20 paragraph organization, 20 sentence structure), so the bank still gains coverage there.

## Per item

| ID | Archetype | Verdict | Reason |
|---|---|---|---|
| CIVIO-VEN-RC-INFER-050001 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050002 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-DETAIL-050003 | VEN-RC-DETAIL | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-MAIN-050004 | VEN-RC-MAIN | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-MAIN-050005 | VEN-RC-MAIN | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050006 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-DETAIL-050007 | VEN-RC-DETAIL | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050008 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-MAIN-050009 | VEN-RC-MAIN | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050010 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050011 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050012 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050013 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050014 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050015 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050016 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050017 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050018 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050019 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050020 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050021 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050022 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050023 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050024 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-RC-INFER-050025 | VEN-RC-INFER | FIX | Keep after fixes: replace the absurd or 'every/never' distractors with plausible unsupported readings; trim the two padded closing sentences. |
| CIVIO-VEN-PARA-ORDER-050026 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050027 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050028 | VEN-PARA-ORDER | REJECT | Listing farmers' needs and checking the storeroom are independent; the swap order B-D-C-A is just as defensible. |
| CIVIO-VEN-PARA-ORDER-050029 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050030 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050031 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050032 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050033 | VEN-PARA-ORDER | REJECT | Taking requests and counting stock are independent; the swap order D-B-A-C is just as defensible. |
| CIVIO-VEN-PARA-ORDER-050034 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050035 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050036 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050037 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050038 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050039 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050040 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050041 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050042 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050043 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050044 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050045 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050046 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050047 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050048 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050049 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050050 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050051 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050052 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050053 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050054 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050055 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050056 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050057 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050058 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050059 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-PARA-ORDER-050060 | VEN-PARA-ORDER | REJECT | Template paragraph (problem, check, fix, verify) with explicit time cues; the key is one of 7 rotating patterns and the swap trap always swaps the first two sentences. |
| CIVIO-VEN-ERROR-AGREE-050061 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050062 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050063 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050064 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050065 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050066 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050067 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050068 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050069 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050070 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050071 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050072 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050073 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050074 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-AGREE-050075 | VEN-ERROR-AGREE | REJECT | One frame repeated 15 times ('The <noun> of the <nouns> is/are/have been/are being ...'). |
| CIVIO-VEN-ERROR-TENSE-050076 | VEN-ERROR-TENSE | REJECT | One frame repeated 5 times (past time marker + will/-s/-ing/-ed). |
| CIVIO-VEN-ERROR-TENSE-050077 | VEN-ERROR-TENSE | REJECT | One frame repeated 5 times (past time marker + will/-s/-ing/-ed). |
| CIVIO-VEN-ERROR-TENSE-050078 | VEN-ERROR-TENSE | REJECT | One frame repeated 5 times (past time marker + will/-s/-ing/-ed). |
| CIVIO-VEN-ERROR-TENSE-050079 | VEN-ERROR-TENSE | REJECT | One frame repeated 5 times (past time marker + will/-s/-ing/-ed). |
| CIVIO-VEN-ERROR-TENSE-050080 | VEN-ERROR-TENSE | REJECT | One frame repeated 5 times (past time marker + will/-s/-ing/-ed). |
| CIVIO-VEN-ERROR-MODIFIER-050081 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050082 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050083 | VEN-ERROR-MODIFIER | REJECT | Non-words in the choices (balancedly), which breaks the keyboard-typo rule. One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050084 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050085 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050086 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050087 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050088 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050089 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050090 | VEN-ERROR-MODIFIER | REJECT | Non-words in the choices (detailedly, workably), which breaks the keyboard-typo rule. One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050091 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050092 | VEN-ERROR-MODIFIER | REJECT | Non-words in the choices (measur, stor), which breaks the keyboard-typo rule. One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050093 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050094 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050095 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050096 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050097 | VEN-ERROR-MODIFIER | REJECT | Non-words in the choices (plann), which breaks the keyboard-typo rule. One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050098 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050099 | VEN-ERROR-MODIFIER | REJECT | Non-words in the choices (guid), which breaks the keyboard-typo rule. One frame repeated 20 times (three-item adjective or gerund series with one form changed). |
| CIVIO-VEN-ERROR-MODIFIER-050100 | VEN-ERROR-MODIFIER | REJECT | One frame repeated 20 times (three-item adjective or gerund series with one form changed). |

## Asks for CoS

1. Approve rejecting the 75 templated para-order and error items, with gap-fill-005 as the replacement.
2. For the 25 RC items, choose between (a) Grok Bot rewriting the weak distractors and trimming the tails, then bringing them back for a pass, and (b) keeping only about 10 of them because of the single theme.
3. Ask ChatGPT not to reuse batch 002's frames in batch 004 (`CHATGPT_NEXT_PROMPT.md` already bans copying 002).

## CoS verdict (2026-10-17), applied

- **Rejected (88):** all 75 para-order and error items, plus 13 RC items. In 050075 the key is also semantically odd. Every rejected item stays draft with review_status `rejected`.
- **Kept and fixed (12 RC):** 050002, 003, 005, 007, 011, 012, 015, 019, 020, 022, 023 and 025. The fixes were made by `scripts/batches/audit/chatgpt_002_verdict.py`:
  - The padded closing sentences are trimmed, keeping each passage at 150 words or more (now 150–167).
  - Every distractor is rewritten as a plausible but unsupported or contradicted reading and recoded. For example, 050003's distractors are now RC-OPPOSITE, because each one contradicts a stated design choice.
  - The why lines are rewritten.
  - Keys are spread across positions (o1 2, o2 4, o3 3, o4 3), and the key is the longest option in only 1 of 12.
- **Theme tag:** 8 of the 12 items carry `"theme": "first-measure-misleads"`. A mock may serve at most 2 of them. That is app code, written up in `docs/FACT_ID_MOCK_RULE_BRIEF.md` for Codex.
- **Activated:** the 12 approved items are imported as active on the MSI local DB.
