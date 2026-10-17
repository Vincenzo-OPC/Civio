# Round 03: gap-fill-005 review request (60 English drafts), revised after the CoS rulings of 2026-10-17

**For:** Chief of Staff  
**File:** `docs/research/gap-fill-005.json`, built by `scripts/batches/gapfill/gap_fill_005.py`  
**Status:** all 60 items are `draft` / `unreviewed`. They are not imported and not active anywhere.  
**Author:** Grok Bot. The items are original, written for the thin areas the Sentinel dossier found.

## What changed after the CoS rulings

- **Codes:** `VEN-RUN-ON`, `VEN-FRAGMENT` and `VEN-MODIFIER-PLACE` are approved and now in the spec as v0.1.9.
- **Reading comprehension follows the spec:**
  - There are now **7 passages of 162–183 words**, each with **2–3 questions**: 6 passages carry 3 questions and 1 carries 2. That gives 20 items, all original, and no passage is reused from another batch.
  - Every passage has an inference item and a vocabulary-in-context item, as Section 3 requires. The six 3-question sets add a main-idea item (P01, P03, P05) or a detail item (P02, P04, P06).
  - Sentences stay within the spec's 25-word limit.
- **Passage tag:** the spec had no passage-ID field, so each item names its passage in `notes` ("Passage gap-fill-005-P0n, question k of m"). Spec 10.8 now records this convention. Every item carries the full passage in its stem plus its own question, so stems stay unique for the importer.
- **QA:** `qa.py` now treats items as siblings when they have an identical passage block (400 characters or more) and different questions after the last blank line. Siblings are exempt from the near-duplicate check. Exact duplicates and all other checks still apply.
- **Answer length:** the key is the longest option in 7 of 20 RC items, 6 of 20 paragraph items and 3 of 20 sentence-structure items.

## Counts

| Area | Archetype | Items |
|---|---|---|
| Reading comprehension | VEN-RC-MAIN | 3 |
| Reading comprehension | VEN-RC-DETAIL | 3 |
| Reading comprehension | VEN-RC-INFER | 7 |
| Reading comprehension | VEN-RC-VOCAB | 7 |
| Paragraph organization | VEN-PARA-ORDER | 12 |
| Paragraph organization | VEN-PARA-INSERT | 8 |
| Sentence structure | VEN-SENT-STRUCTURE | 20 |
| **Total** | | **60** |

Keys: o1 16, o2 15, o3 16, o4 13.

## QA

- `qa_file.py docs/research/gap-fill-005.json`: **0 problems** against the bank.
- `qa_all.py --no-fixes`: GREEN.

## Decisions for CoS

1. **Question mix.** Section 3 requires an inference item and a vocabulary item in every passage, so the RC mix is main 3, detail 3, inference 7, vocabulary 7. If you prefer more main-idea and detail items, I can drop one vocabulary item per set and relax that spec rule.
2. **Passage ID field.** Should the tag become a real `passage_id` field? If so, the mock builder could then keep a set together or limit it to one question per mock. That change is app code.
3. **Approval.** Accept, fix or reject each item. Nothing is imported until you rule.

## Items

| # | ID | Archetype | Difficulty | Key | Passage / stem (start) |
|---|---|---|---|---|---|
| 1 | CIVIO-GAP5-VEN-RC-MAIN-0001 | VEN-RC-MAIN | medium | o2 | gap-fill-005-P01, question 1 of 3 · Which statement best expresses the main idea of the passage? |
| 2 | CIVIO-GAP5-VEN-RC-INFER-0002 | VEN-RC-INFER | medium | o1 | gap-fill-005-P01, question 2 of 3 · Why would cutting the mangroves eventually hurt the families' ow |
| 3 | CIVIO-GAP5-VEN-RC-VOCAB-0003 | VEN-RC-VOCAB | easy | o4 | gap-fill-005-P01, question 3 of 3 · In the last sentence, the word "established" most nearly means: |
| 4 | CIVIO-GAP5-VEN-RC-DETAIL-0004 | VEN-RC-DETAIL | easy | o3 | gap-fill-005-P02, question 1 of 3 · According to the passage, when does Aling Rosa allow new credit  |
| 5 | CIVIO-GAP5-VEN-RC-INFER-0005 | VEN-RC-INFER | medium | o2 | gap-fill-005-P02, question 2 of 3 · Why does Aling Rosa believe her credit rule protects friendships |
| 6 | CIVIO-GAP5-VEN-RC-VOCAB-0006 | VEN-RC-VOCAB | medium | o1 | gap-fill-005-P02, question 3 of 3 · As used in the passage, "tie up money" means to: |
| 7 | CIVIO-GAP5-VEN-RC-MAIN-0007 | VEN-RC-MAIN | medium | o4 | gap-fill-005-P03, question 1 of 3 · What is the passage mainly about? |
| 8 | CIVIO-GAP5-VEN-RC-INFER-0008 | VEN-RC-INFER | hard | o3 | gap-fill-005-P03, question 2 of 3 · Based on the passage, clearing the forest at the summit would mo |
| 9 | CIVIO-GAP5-VEN-RC-VOCAB-0009 | VEN-RC-VOCAB | easy | o2 | gap-fill-005-P03, question 3 of 3 · In the passage, the phrase "for lack of hands" means a shortage  |
| 10 | CIVIO-GAP5-VEN-RC-DETAIL-0010 | VEN-RC-DETAIL | easy | o1 | gap-fill-005-P04, question 1 of 3 · According to the passage, where does the Aedes mosquito breed? |
| 11 | CIVIO-GAP5-VEN-RC-INFER-0011 | VEN-RC-INFER | medium | o4 | gap-fill-005-P04, question 2 of 3 · A family empties its water drum every week but never scrubs it.  |
| 12 | CIVIO-GAP5-VEN-RC-VOCAB-0012 | VEN-RC-VOCAB | easy | o3 | gap-fill-005-P04, question 3 of 3 · As used in the passage, the word "routine" refers to: |
| 13 | CIVIO-GAP5-VEN-RC-MAIN-0013 | VEN-RC-MAIN | medium | o2 | gap-fill-005-P05, question 1 of 3 · Which statement best expresses the main idea of the passage? |
| 14 | CIVIO-GAP5-VEN-RC-INFER-0014 | VEN-RC-INFER | medium | o1 | gap-fill-005-P05, question 2 of 3 · Which conclusion is best supported by the passage? |
| 15 | CIVIO-GAP5-VEN-RC-VOCAB-0015 | VEN-RC-VOCAB | easy | o4 | gap-fill-005-P05, question 3 of 3 · In the last sentence, the word "exposure" most nearly means: |
| 16 | CIVIO-GAP5-VEN-RC-DETAIL-0016 | VEN-RC-DETAIL | medium | o3 | gap-fill-005-P06, question 1 of 3 · According to the passage, why can the loss of a few adult eagles |
| 17 | CIVIO-GAP5-VEN-RC-INFER-0017 | VEN-RC-INFER | hard | o2 | gap-fill-005-P06, question 2 of 3 · It can be inferred that releasing a captive-bred pair into a sma |
| 18 | CIVIO-GAP5-VEN-RC-VOCAB-0018 | VEN-RC-VOCAB | medium | o1 | gap-fill-005-P06, question 3 of 3 · As used in the passage, "set back" means to: |
| 19 | CIVIO-GAP5-VEN-RC-INFER-0019 | VEN-RC-INFER | medium | o4 | gap-fill-005-P07, question 1 of 2 · The last two sentences suggest that many people fall for the sca |
| 20 | CIVIO-GAP5-VEN-RC-VOCAB-0020 | VEN-RC-VOCAB | easy | o3 | gap-fill-005-P07, question 2 of 2 · As used in the passage, the word "legitimate" most nearly means: |
| 21 | CIVIO-GAP5-VEN-PARA-ORDER-0021 | VEN-PARA-ORDER | medium | o1 | Arrange the sentences to form a logical paragraph.
P. These figures, however, hide wide differences  |
| 22 | CIVIO-GAP5-VEN-PARA-ORDER-0022 | VEN-PARA-ORDER | easy | o1 | Which sentence should come FIRST in the paragraph?
1. As a result, the town market now closes an hou |
| 23 | CIVIO-GAP5-VEN-PARA-ORDER-0023 | VEN-PARA-ORDER | medium | o4 | Arrange the sentences in the best order.
A. Instead, she copied each sale by hand into a notebook ev |
| 24 | CIVIO-GAP5-VEN-PARA-ORDER-0024 | VEN-PARA-ORDER | easy | o3 | Which sentence should come LAST in the paragraph?
A. The answer lies in what the plant eats.
B. Many |
| 25 | CIVIO-GAP5-VEN-PARA-ORDER-0025 | VEN-PARA-ORDER | medium | o3 | Choose the best order for the sentences.
1. This is why the old building on Rizal Street is now bein |
| 26 | CIVIO-GAP5-VEN-PARA-ORDER-0026 | VEN-PARA-ORDER | easy | o3 | Arrange the sentences to show the correct order.
A. If both houses approve the same version, it is s |
| 27 | CIVIO-GAP5-VEN-PARA-ORDER-0027 | VEN-PARA-ORDER | medium | o1 | Which sentence should come SECOND in the paragraph?
1. The trick is to pick the fruit when its skin  |
| 28 | CIVIO-GAP5-VEN-PARA-ORDER-0028 | VEN-PARA-ORDER | medium | o1 | Arrange the sentences to form a coherent paragraph.
W. Others argue that the money would be better s |
| 29 | CIVIO-GAP5-VEN-PARA-ORDER-0029 | VEN-PARA-ORDER | medium | o4 | Choose the order that makes the paragraph logical.
A. As the warm air rises, it cools, and the water |
| 30 | CIVIO-GAP5-VEN-PARA-ORDER-0030 | VEN-PARA-ORDER | easy | o2 | Which sentence should come FIRST?
1. Second, it gives employers a quick way to check what an applica |
| 31 | CIVIO-GAP5-VEN-PARA-ORDER-0031 | VEN-PARA-ORDER | medium | o4 | Arrange the sentences in the most logical order.
A. She found that each form was being stamped twice |
| 32 | CIVIO-GAP5-VEN-PARA-ORDER-0032 | VEN-PARA-ORDER | easy | o2 | Arrange the sentences to describe the process in order.
1. The fibers are then washed and hung to dr |
| 33 | CIVIO-GAP5-VEN-PARA-INSERT-0033 | VEN-PARA-INSERT | medium | o3 | (1) Public markets in many Philippine towns are owned by the local government. (2) Vendors rent thei |
| 34 | CIVIO-GAP5-VEN-PARA-INSERT-0034 | VEN-PARA-INSERT | medium | o1 | (1) Many Filipino words for food come from other languages. (2) "Pansit," for instance, is usually t |
| 35 | CIVIO-GAP5-VEN-PARA-INSERT-0035 | VEN-PARA-INSERT | easy | o2 | (1) Rice is the staple food of most Filipinos. (2) For decades the country has imported part of its  |
| 36 | CIVIO-GAP5-VEN-PARA-INSERT-0036 | VEN-PARA-INSERT | medium | o2 | (1) Barangay tanod are volunteers who help keep peace and order in their communities. (2) They patro |
| 37 | CIVIO-GAP5-VEN-PARA-INSERT-0037 | VEN-PARA-INSERT | easy | o1 | (1) Coconut trees grow in nearly every province of the Philippines. (2) The meat, for one, is dried  |
| 38 | CIVIO-GAP5-VEN-PARA-INSERT-0038 | VEN-PARA-INSERT | medium | o2 | (1) Jeepney drivers usually pay a daily "boundary" to the owner of the vehicle. (2) Whatever they ea |
| 39 | CIVIO-GAP5-VEN-PARA-INSERT-0039 | VEN-PARA-INSERT | easy | o3 | (1) Reading a payslip carefully can save an employee from costly mistakes. (2) The top section shows |
| 40 | CIVIO-GAP5-VEN-PARA-INSERT-0040 | VEN-PARA-INSERT | medium | o3 | (1) Many offices now accept documents by email. (2) This saves applicants a trip, but it creates a n |
| 41 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0041 | VEN-SENT-STRUCTURE | easy | o3 | Which sentence about the printer and the emailed report is correctly constructed? |
| 42 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0042 | VEN-SENT-STRUCTURE | easy | o4 | Choose the best-built sentence about Mr. Santos and the dark streetlights. |
| 43 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0043 | VEN-SENT-STRUCTURE | medium | o1 | Which sentence about the office closing on Monday is complete and correctly punctuated? |
| 44 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0044 | VEN-SENT-STRUCTURE | medium | o2 | Which sentence about applicants with incomplete forms has no error in structure? |
| 45 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0045 | VEN-SENT-STRUCTURE | easy | o3 | Select the correctly written sentence about the relief truck on a flooded road. |
| 46 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0046 | VEN-SENT-STRUCTURE | medium | o4 | Which sentence about the supervisor's instructions on checking figures is correctly constructed? |
| 47 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0047 | VEN-SENT-STRUCTURE | hard | o1 | Which sentence states clearly that no one without a valid ID may enter the records room? |
| 48 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0048 | VEN-SENT-STRUCTURE | easy | o2 | Which sentence about volunteers clearing branches after a typhoon is complete and correctly punctuat |
| 49 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0049 | VEN-SENT-STRUCTURE | medium | o3 | Which sentence about leaving the office at day's end has no error in structure? |
| 50 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0050 | VEN-SENT-STRUCTURE | medium | o4 | Select the correctly written sentence about the clinic that opened in March. |
| 51 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0051 | VEN-SENT-STRUCTURE | easy | o1 | Which sentence about an unpaid application fee is correctly constructed? |
| 52 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0052 | VEN-SENT-STRUCTURE | hard | o2 | Which sentence makes clear that it was the volunteers who worked through the night? |
| 53 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0053 | VEN-SENT-STRUCTURE | easy | o3 | Which sentence about a training postponed by a cancelled flight is complete and correctly punctuated |
| 54 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0054 | VEN-SENT-STRUCTURE | medium | o4 | Which sentence is best for a formal memo to all staff? |
| 55 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0055 | VEN-SENT-STRUCTURE | hard | o1 | Select the correctly written sentence about scholarship application requirements. |
| 56 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0056 | VEN-SENT-STRUCTURE | easy | o2 | Which sentence about the guard's bag inspection at the entrance is correctly constructed? |
| 57 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0057 | VEN-SENT-STRUCTURE | medium | o3 | Choose the best-built sentence about Ms. Reyes and the budget proposal. |
| 58 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0058 | VEN-SENT-STRUCTURE | medium | o4 | Which sentence about counting ballots during a power outage is complete and correctly punctuated? |
| 59 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0059 | VEN-SENT-STRUCTURE | medium | o1 | Which sentence about a report with a data annex has no error in structure? |
| 60 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0060 | VEN-SENT-STRUCTURE | easy | o2 | Select the correctly written sentence about fishers who go out at night. |
