# Round 03 — gap-fill-005 review request (English, 60 drafts)

**For:** Chief of Staff  
**File:** `docs/research/gap-fill-005.json` (built by `scripts/batches/gapfill/gap_fill_005.py`)  
**Status:** all 60 items `draft` / `unreviewed`, not imported, not active anywhere.  
**Author:** Grok Bot (original items, written for the thin areas in the Sentinel dossier)

## Counts

| Area | Archetype | Items |
|---|---|---|
| Reading comprehension | VEN-RC-MAIN | 5 |
| Reading comprehension | VEN-RC-DETAIL | 4 |
| Reading comprehension | VEN-RC-INFER | 7 |
| Reading comprehension | VEN-RC-VOCAB | 4 |
| Paragraph organization | VEN-PARA-ORDER | 12 |
| Paragraph organization | VEN-PARA-INSERT | 8 |
| Sentence structure | VEN-SENT-STRUCTURE | 20 |
| **Total** | | **60** |

Key positions: o1 16, o2 15, o3 16, o4 13. Difficulty: easy 22, hard 5, medium 33.

## QA

- `python3 scripts/batches/qa_file.py docs/research/gap-fill-005.json`: 60 items checked against 1,684 bank items, **0 problems** (fields, 4 distinct options, a code and a why for every wrong option, unique ordering codes, key ≠ listed order, shortcut ≤300 characters, exact and near-duplicate stems at 0.65, baseline hits, 25% frame cap).
- `qa_all.py`: GREEN. Pest: 328/328 passing.
- All options and explanations were spell-checked; the only words flagged were Filipino or proper terms used on purpose (barangay, tanod, jeepney, baybayin, kudlit, and so on).

## Decisions for CoS

1. **New distractor codes (spec change, pending).** The sentence-structure items use three codes that were not in the spec: `VEN-RUN-ON`, `VEN-FRAGMENT` and `VEN-MODIFIER-PLACE`. I added them to `docs/CSE-Question-Design-Spec.md` after `PO-TRANSITION-IGNORED`, marked *(proposed v0.1.9, pending CoS)*. qa.py reads its codes from the spec, so these items only pass because of that addition. If you reject the codes, the 20 SS items need recoding.
2. **Passage length.** The RC passages run 96–129 words, below the spec's 150–250. I kept them short because each passage carries a single question. You can accept them as short-form RC, or I can lengthen them.
3. **One question per passage.** The app has no passage sets, so each RC item carries its own passage in the stem. Passages are not shared or reused.
4. **Sentence-structure stems.** The importer keys on stem, and qa.py rejects near-duplicate stems. Each SS stem therefore names its topic (for example, "Select the correctly written sentence about the relief truck on a flooded road."), rotating through 5 frames. Three items have special stems.
5. **Paragraph order.** The 12 ORDER items each use unique distractor codes, and none has the key in the listed order. I checked each one for a second defensible order, which was the reason 050028/050033 failed in chatgpt-batch-002.

## Items

| # | ID | Archetype | Difficulty | Key | Stem (start) |
|---|---|---|---|---|---|
| 1 | CIVIO-GAP5-VEN-RC-MAIN-0001 | VEN-RC-MAIN | medium | o2 | Read the passage and answer the question that follows.  Along the coast of Bohol, fishing … |
| 2 | CIVIO-GAP5-VEN-RC-INFER-0002 | VEN-RC-INFER | medium | o1 | Read the passage and answer the question that follows.  Many sari-sari stores let regular … |
| 3 | CIVIO-GAP5-VEN-RC-VOCAB-0003 | VEN-RC-VOCAB | easy | o4 | Read the selection below, then answer the question.  The rice terraces of Ifugao were carv… |
| 4 | CIVIO-GAP5-VEN-RC-DETAIL-0004 | VEN-RC-DETAIL | easy | o3 | Read the passage and answer the question that follows.  Dengue cases in the Philippines us… |
| 5 | CIVIO-GAP5-VEN-RC-INFER-0005 | VEN-RC-INFER | medium | o2 | Read the selection below, then answer the question.  PAGASA reports not only the air tempe… |
| 6 | CIVIO-GAP5-VEN-RC-MAIN-0006 | VEN-RC-MAIN | medium | o1 | Read the passage and answer the question that follows.  Bamboo grows quickly in most parts… |
| 7 | CIVIO-GAP5-VEN-RC-VOCAB-0007 | VEN-RC-VOCAB | medium | o4 | Read the selection below, then answer the question.  Since 2016, people may request record… |
| 8 | CIVIO-GAP5-VEN-RC-DETAIL-0008 | VEN-RC-DETAIL | medium | o3 | Read the passage and answer the question that follows.  The Philippine eagle is one of the… |
| 9 | CIVIO-GAP5-VEN-RC-INFER-0009 | VEN-RC-INFER | hard | o2 | Read the selection below, then answer the question.  For many families of overseas Filipin… |
| 10 | CIVIO-GAP5-VEN-RC-MAIN-0010 | VEN-RC-MAIN | medium | o1 | Read the passage and answer the question that follows.  PAGASA's tropical cyclone wind sig… |
| 11 | CIVIO-GAP5-VEN-RC-VOCAB-0011 | VEN-RC-VOCAB | easy | o4 | Read the selection below, then answer the question.  During the dry months of a strong El … |
| 12 | CIVIO-GAP5-VEN-RC-INFER-0012 | VEN-RC-INFER | medium | o3 | Read the passage and answer the question that follows.  A text message says that a package… |
| 13 | CIVIO-GAP5-VEN-RC-DETAIL-0013 | VEN-RC-DETAIL | easy | o2 | Read the selection below, then answer the question.  Tubbataha Reefs Natural Park lies in … |
| 14 | CIVIO-GAP5-VEN-RC-INFER-0014 | VEN-RC-INFER | medium | o1 | Read the passage and answer the question that follows.  Health workers in a town in Iloilo… |
| 15 | CIVIO-GAP5-VEN-RC-MAIN-0015 | VEN-RC-MAIN | easy | o4 | Read the selection below, then answer the question.  Long before jeepneys filled the stree… |
| 16 | CIVIO-GAP5-VEN-RC-VOCAB-0016 | VEN-RC-VOCAB | easy | o3 | Read the passage and answer the question that follows.  The new records policy requires ev… |
| 17 | CIVIO-GAP5-VEN-RC-INFER-0017 | VEN-RC-INFER | medium | o2 | Read the selection below, then answer the question.  Many people believe that lightning ne… |
| 18 | CIVIO-GAP5-VEN-RC-DETAIL-0018 | VEN-RC-DETAIL | medium | o1 | Read the passage and answer the question that follows.  A birth that is not registered wit… |
| 19 | CIVIO-GAP5-VEN-RC-MAIN-0019 | VEN-RC-MAIN | medium | o4 | Read the selection below, then answer the question.  A barangay in Quezon City began colle… |
| 20 | CIVIO-GAP5-VEN-RC-INFER-0020 | VEN-RC-INFER | hard | o3 | Read the passage and answer the question that follows.  Baybayin, a script used in parts o… |
| 21 | CIVIO-GAP5-VEN-PARA-ORDER-0021 | VEN-PARA-ORDER | medium | o1 | Arrange the sentences to form a logical paragraph. P. These figures, however, hide wide di… |
| 22 | CIVIO-GAP5-VEN-PARA-ORDER-0022 | VEN-PARA-ORDER | easy | o1 | Which sentence should come FIRST in the paragraph? 1. As a result, the town market now clo… |
| 23 | CIVIO-GAP5-VEN-PARA-ORDER-0023 | VEN-PARA-ORDER | medium | o4 | Arrange the sentences in the best order. A. Instead, she copied each sale by hand into a n… |
| 24 | CIVIO-GAP5-VEN-PARA-ORDER-0024 | VEN-PARA-ORDER | easy | o3 | Which sentence should come LAST in the paragraph? A. The answer lies in what the plant eat… |
| 25 | CIVIO-GAP5-VEN-PARA-ORDER-0025 | VEN-PARA-ORDER | medium | o3 | Choose the best order for the sentences. 1. This is why the old building on Rizal Street i… |
| 26 | CIVIO-GAP5-VEN-PARA-ORDER-0026 | VEN-PARA-ORDER | easy | o3 | Arrange the sentences to show the correct order. A. If both houses approve the same versio… |
| 27 | CIVIO-GAP5-VEN-PARA-ORDER-0027 | VEN-PARA-ORDER | medium | o1 | Which sentence should come SECOND in the paragraph? 1. The trick is to pick the fruit when… |
| 28 | CIVIO-GAP5-VEN-PARA-ORDER-0028 | VEN-PARA-ORDER | medium | o1 | Arrange the sentences to form a coherent paragraph. W. Others argue that the money would b… |
| 29 | CIVIO-GAP5-VEN-PARA-ORDER-0029 | VEN-PARA-ORDER | medium | o4 | Choose the order that makes the paragraph logical. A. As the warm air rises, it cools, and… |
| 30 | CIVIO-GAP5-VEN-PARA-ORDER-0030 | VEN-PARA-ORDER | easy | o2 | Which sentence should come FIRST? 1. Second, it gives employers a quick way to check what … |
| 31 | CIVIO-GAP5-VEN-PARA-ORDER-0031 | VEN-PARA-ORDER | medium | o4 | Arrange the sentences in the most logical order. A. She found that each form was being sta… |
| 32 | CIVIO-GAP5-VEN-PARA-ORDER-0032 | VEN-PARA-ORDER | easy | o2 | Arrange the sentences to describe the process in order. 1. The fibers are then washed and … |
| 33 | CIVIO-GAP5-VEN-PARA-INSERT-0033 | VEN-PARA-INSERT | medium | o3 | Where does the following sentence best fit in the paragraph? "Some lose regular customers … |
| 34 | CIVIO-GAP5-VEN-PARA-INSERT-0034 | VEN-PARA-INSERT | medium | o1 | Where does the following sentence best fit in the paragraph? "Among the oldest are words f… |
| 35 | CIVIO-GAP5-VEN-PARA-INSERT-0035 | VEN-PARA-INSERT | easy | o2 | Where does the following sentence best fit in the paragraph? "One reason is that local pro… |
| 36 | CIVIO-GAP5-VEN-PARA-INSERT-0036 | VEN-PARA-INSERT | medium | o2 | Where does the following sentence best fit in the paragraph? "This allowance is set by eac… |
| 37 | CIVIO-GAP5-VEN-PARA-INSERT-0037 | VEN-PARA-INSERT | easy | o1 | Where does the following sentence best fit in the paragraph? "Almost every part of the fru… |
| 38 | CIVIO-GAP5-VEN-PARA-INSERT-0038 | VEN-PARA-INSERT | medium | o2 | Where does the following sentence best fit in the paragraph? "On busy days, the arrangemen… |
| 39 | CIVIO-GAP5-VEN-PARA-INSERT-0039 | VEN-PARA-INSERT | easy | o3 | Where does the following sentence best fit in the paragraph? "Each of these should match t… |
| 40 | CIVIO-GAP5-VEN-PARA-INSERT-0040 | VEN-PARA-INSERT | medium | o3 | Where does the following sentence best fit in the paragraph? "Such names make a file hard … |
| 41 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0041 | VEN-SENT-STRUCTURE | easy | o3 | Which sentence about the printer and the emailed report is correctly constructed? |
| 42 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0042 | VEN-SENT-STRUCTURE | easy | o4 | Choose the best-built sentence about Mr. Santos and the dark streetlights. |
| 43 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0043 | VEN-SENT-STRUCTURE | medium | o1 | Which sentence about the office closing on Monday is complete and correctly punctuated? |
| 44 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0044 | VEN-SENT-STRUCTURE | medium | o2 | Which sentence about applicants with incomplete forms has no error in structure? |
| 45 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0045 | VEN-SENT-STRUCTURE | easy | o3 | Select the correctly written sentence about the relief truck on a flooded road. |
| 46 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0046 | VEN-SENT-STRUCTURE | medium | o4 | Which sentence about the supervisor's instructions on checking figures is correctly constr… |
| 47 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0047 | VEN-SENT-STRUCTURE | hard | o1 | Which sentence states clearly that no one without a valid ID may enter the records room? |
| 48 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0048 | VEN-SENT-STRUCTURE | easy | o2 | Which sentence about volunteers clearing branches after a typhoon is complete and correctl… |
| 49 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0049 | VEN-SENT-STRUCTURE | medium | o3 | Which sentence about leaving the office at day's end has no error in structure? |
| 50 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0050 | VEN-SENT-STRUCTURE | medium | o4 | Select the correctly written sentence about the clinic that opened in March. |
| 51 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0051 | VEN-SENT-STRUCTURE | easy | o1 | Which sentence about an unpaid application fee is correctly constructed? |
| 52 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0052 | VEN-SENT-STRUCTURE | hard | o2 | Which sentence makes clear that it was the volunteers who worked through the night? |
| 53 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0053 | VEN-SENT-STRUCTURE | easy | o3 | Which sentence about a training postponed by a cancelled flight is complete and correctly … |
| 54 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0054 | VEN-SENT-STRUCTURE | medium | o4 | Which sentence is best for a formal memo to all staff? |
| 55 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0055 | VEN-SENT-STRUCTURE | hard | o1 | Select the correctly written sentence about scholarship application requirements. |
| 56 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0056 | VEN-SENT-STRUCTURE | easy | o2 | Which sentence about the guard's bag inspection at the entrance is correctly constructed? |
| 57 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0057 | VEN-SENT-STRUCTURE | medium | o3 | Choose the best-built sentence about Ms. Reyes and the budget proposal. |
| 58 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0058 | VEN-SENT-STRUCTURE | medium | o4 | Which sentence about counting ballots during a power outage is complete and correctly punc… |
| 59 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0059 | VEN-SENT-STRUCTURE | medium | o1 | Which sentence about a report with a data annex has no error in structure? |
| 60 | CIVIO-GAP5-VEN-SENT-STRUCTURE-0060 | VEN-SENT-STRUCTURE | easy | o2 | Select the correctly written sentence about fishers who go out at night. |

## Ask

For each item: **accept / fix / reject**, plus rulings on decisions 1–2. Nothing will be imported or activated until you rule.
