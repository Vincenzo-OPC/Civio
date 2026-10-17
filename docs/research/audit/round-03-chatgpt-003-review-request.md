# Round 03: Codex/ChatGPT batch 003 (100 General Information drafts), review request for Chief of Staff

Grok Bot, 2026-10-17. File: `docs/research/chatgpt-batch-003.json` (Codex commit eca4268; sources 716dc94, notes 9611b91). **All 100 stay `draft` / `unreviewed`. Nothing activated or imported.**

## Method

- Ran `qa.check_item`, `qa.check_round` (near 0.65) and `qa.baseline_hits` against every batch, gap-fill, supplement and ChatGPT file in the repo. This clears the QA blocker noted in 9611b91: 0 structural flags, 0 stem near-duplicates, 0 baseline hits, before and after the edits.
- Pulled the official texts from LawPhil (1987 Constitution; R.A. 6713, 9003, 8749, 9275, 9729, 9147) and checked every cited section, number and key against the text. **All 100 keys are correct and every citation points to the right section.** No legal error found in the keys.
- Checked one defensible answer per item, distractor plausibility and codes, giveaways (longest-option key, stem echo), and fact-level duplicates against the 127 GI items already in the bank.

## What was wrong (batch-wide)

1. **Method line was padding.** All 100 `reveal.shortcut` lines were the same template ("Match the task described to <cite> before considering similarly named duties"). Replaced with a one-line, item-specific memory cue from the provision text.
2. **Why-wrong reasons were tautological.** 263 of 300 repeated the option and said it "concerns a different legal concept". All 300 are rewritten to say what the wrong option actually is (its own section or body) and why it does not fit.
3. **Weak distractors.** Many were absurd ("Automatic citizenship for the landowner", "Foreign embassies", "Publishing an election precinct list"). Replaced with real sibling rights, bodies, numbers and norms from the same law, as the spec asks (§9 GI archetype table). Two `GI-OLD-RULE` traps were added where an older constitution differs (060028 warrants; 060046 'imminent danger').
4. **Giveaways.** 22 keys were much longer than every distractor; shortened or balanced (key wording only, same answer). Removed 'alone' tags that marked wrong options (060053-060057).
5. **Ambiguity.** Stems tightened where a second answer was defensible: 060026 (seize vs search), 060043 (awkward 'without the exception'), 060044 (not all options were presumptions), 060047 ('could be implicated' let due process in), 060085 (every Sec. 4 right is 'expressly recognized').
6. **Codes.** Recoded to match what each distractor is: sibling term 192, wrong body 40, sounds-right 38, neighbor number 28, old rule 2.

Edits are reproducible: `scripts/batches/fixes/b3/apply.py` rebuilds the file from eca4268 using `c1.py`-`c4.py` (each wrong option's text, code and reason is listed there for review).

## Proposed verdicts

- **ACCEPT 77**, **ACCEPT as variant 8** (applied scenario on a fact the bank already tests; CoS decides whether both formats stay), **HOLD 4**, **REJECT 11** (10 fact duplicates of approved items, 1 mirror pair).
- Note: GI items share sibling options across items by design (for example the eight R.A. 6713 norms). Unlike the Filipino synonym items, a key appearing as another item's distractor does not give the answer away here, so the mock key/trap separation is not extended to GI.

| ID | Source | Proposed | Why | Edits made |
|---|---|---|---|---|
| CIVIO-GI-SCENARIO-APPLY-060001 | 1987 Constitution, Art. II, Sec. 3 | ACCEPT (variant) | applied scenario on a fact already in the bank (000507); keep only if CoS wants both formats | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060002 | 1987 Constitution, Art. II, Sec. 4 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060003 | 1987 Constitution, Art. II, Sec. 14 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060004 | 1987 Constitution, Art. II, Sec. 25 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060005 | 1987 Constitution, Art. II, Sec. 28 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060006 | 1987 Constitution, Art. VI, Sec. 1 | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060007 | 1987 Constitution, Art. VI, Sec. 24 | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060008 | 1987 Constitution, Art. VI, Sec. 27(1) | REJECT | fact duplicate of approved 000910 (veto override) | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060009 | 1987 Constitution, Art. VI, Sec. 28(1) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060010 | 1987 Constitution, Art. VI, Sec. 32 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060011 | 1987 Constitution, Art. VII, Sec. 1 | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060012 | 1987 Constitution, Art. VII, Sec. 21 | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060013 | 1987 Constitution, Art. VII, Sec. 18 | HOLD | reviewer watchlist item: verify the extension wording ("in the same manner") reads clearly to examinees | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060014 | 1987 Constitution, Art. VIII, Sec. 1 | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060015 | 1987 Constitution, Art. VIII, Sec. 8 | REJECT | fact duplicate of approved 000503 (JBC) | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060016 | 1987 Constitution, Art. IX-A, Sec. 1 | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060017 | 1987 Constitution, Art. IX-B, Sec. 2(2) | ACCEPT (variant) | applied scenario on a fact already in the bank (000909); keep only if CoS wants both formats | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060018 | 1987 Constitution, Art. IX-B, Sec. 2(3) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060019 | 1987 Constitution, Art. IX-B, Sec. 2(4) | ACCEPT (variant) | applied scenario on a fact already in the bank (000303); keep only if CoS wants both formats | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060020 | 1987 Constitution, Art. IX-B, Sec. 2(5) | ACCEPT (variant) | applied scenario on a fact already in the bank (000902); keep only if CoS wants both formats | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060021 | 1987 Constitution, Art. IX-C, Sec. 2(1) | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060022 | 1987 Constitution, Art. IX-D, Sec. 2(1) | REJECT | fact duplicate of approved 000304 (COA) | 1 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-TERM-MATCH-060023 | 1987 Constitution, Art. XI, Sec. 1 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060024 | 1987 Constitution, Art. XI, Sec. 3(1) | REJECT | fact duplicate of approved 000007 (House initiates impeachment) | why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060025 | 1987 Constitution, Art. XI, Sec. 3(6) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060026 | 1987 Constitution, Art. III, Sec. 1 | ACCEPT |  | stem; 1 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060027 | 1987 Constitution, Art. III, Sec. 1 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060028 | 1987 Constitution, Art. III, Sec. 2 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060029 | 1987 Constitution, Art. III, Sec. 2 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060030 | 1987 Constitution, Art. III, Sec. 3(1) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060031 | 1987 Constitution, Art. III, Sec. 3(2) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060032 | 1987 Constitution, Art. III, Sec. 4 | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060033 | 1987 Constitution, Art. III, Sec. 4 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060034 | 1987 Constitution, Art. III, Sec. 5 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060035 | 1987 Constitution, Art. III, Sec. 5 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060036 | 1987 Constitution, Art. III, Sec. 6 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060037 | 1987 Constitution, Art. III, Sec. 7 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060038 | 1987 Constitution, Art. III, Sec. 8 | HOLD | overlaps 060020 (association vs self-organization); keep one | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060039 | 1987 Constitution, Art. III, Sec. 9 | HOLD | distractor o1 relies on case law (courts, not assessors, fix just compensation); confirm acceptable for Subprofessional | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060040 | 1987 Constitution, Art. III, Sec. 11 | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060041 | 1987 Constitution, Art. III, Sec. 12(1) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060042 | 1987 Constitution, Art. III, Sec. 12(2) | ACCEPT |  | key wording (same answer); 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060043 | 1987 Constitution, Art. III, Sec. 13 | ACCEPT |  | stem; key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060044 | 1987 Constitution, Art. III, Sec. 14(2) | ACCEPT |  | stem; 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060045 | 1987 Constitution, Art. III, Sec. 14(2) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060046 | 1987 Constitution, Art. III, Sec. 15 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060047 | 1987 Constitution, Art. III, Sec. 16 | ACCEPT |  | stem; 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060048 | 1987 Constitution, Art. III, Sec. 17 | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-RIGHTS-APPLY-060049 | 1987 Constitution, Art. III, Sec. 20 | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-WHO-HOLDS-POWER-060050 | 1987 Constitution, Art. XIII, Sec. 18(1) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060051 | R.A. 6713, Sec. 4(A)(a) | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060052 | R.A. 6713, Sec. 4(A)(b) | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060053 | R.A. 6713, Sec. 4(A)(c) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060054 | R.A. 6713, Sec. 4(A)(d) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060055 | R.A. 6713, Sec. 4(A)(e) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060056 | R.A. 6713, Sec. 4(A)(f) | ACCEPT |  | 1 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060057 | R.A. 6713, Sec. 4(A)(g) | ACCEPT (variant) | applied scenario on a fact already in the bank (001003); keep only if CoS wants both formats | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060058 | R.A. 6713, Sec. 4(A)(h) | ACCEPT |  | 1 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060059 | R.A. 6713, Sec. 5(a) | REJECT | fact duplicate of approved 000020 and 000708 (15 working days; the bank already has this twice) | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060060 | R.A. 6713, Sec. 5(a) | ACCEPT |  | 1 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060061 | R.A. 6713, Sec. 5(b) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060062 | R.A. 6713, Sec. 5(c) | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060063 | R.A. 6713, Sec. 5(d) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060064 | R.A. 6713, Sec. 5(e) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060065 | R.A. 6713, Sec. 7(a) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060066 | R.A. 6713, Sec. 7(b)(1) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060067 | R.A. 6713, Sec. 7(b)(2) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060068 | R.A. 6713, Sec. 7(b)(3) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060069 | R.A. 6713, Sec. 7(c) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-SCENARIO-APPLY-060070 | R.A. 6713, Sec. 7(d) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060071 | R.A. 6713, Sec. 8(A) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060072 | R.A. 6713, Sec. 8(A) | ACCEPT |  | 1 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060073 | R.A. 6713, Sec. 8(A) | REJECT | fact duplicate of approved 000511 (30 days after separation) | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060074 | R.A. 6713, Sec. 8(C)(2) | REJECT | fact duplicate of approved 000705 (10 working days) | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-DEADLINE-NUMBER-060075 | R.A. 6713, Sec. 9 | ACCEPT (variant) | applied scenario on a fact already in the bank (000502 / 001008); keep only if CoS wants both formats | why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060076 | R.A. 9003, Sec. 3(jj) | ACCEPT (variant) | applied scenario on a fact already in the bank (3-0002); keep only if CoS wants both formats | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060077 | R.A. 9003, Sec. 22(b) | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060078 | R.A. 9003, Sec. 10 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060079 | R.A. 9003, Sec. 10 | REJECT | mirror of 060078 (same Sec. 10 split); each gives the other away | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060080 | R.A. 9003, Sec. 10 | HOLD | third Sec. 10 item with 060078/060079; keep if 060079 is rejected | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060081 | R.A. 9003, Sec. 3(r) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060082 | R.A. 9003, Sec. 3(f) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060083 | R.A. 9003, Sec. 48(3) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060084 | R.A. 8749, Sec. 2 | ACCEPT (variant) | applied scenario on a fact already in the bank (3-0008); keep only if CoS wants both formats | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060085 | R.A. 8749, Sec. 4(a) | ACCEPT |  | stem; 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060086 | R.A. 8749, Sec. 4(c) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060087 | R.A. 8749, Sec. 4(e) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060088 | R.A. 8749, Sec. 3(c) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060089 | R.A. 9275, Sec. 2 | REJECT | fact duplicate of approved 3-0012 | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060090 | R.A. 9275, Sec. 3 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060091 | R.A. 9275, Sec. 2(g) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060092 | R.A. 9275, Sec. 4(a) | ACCEPT |  | 2 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060093 | R.A. 9275, Sec. 2(h) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060094 | R.A. 9729, Sec. 4 | REJECT | fact duplicate of approved 3-0021 (same question, same key) | why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060095 | R.A. 9729, Sec. 3(a) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060096 | R.A. 9729, Sec. 3(c) | REJECT | fact duplicate of approved 3-0023 | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060097 | R.A. 9729, Sec. 9(a) | ACCEPT |  | key wording (same answer); 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060098 | R.A. 9729, Sec. 2 | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060099 | R.A. 9147, Sec. 2 | ACCEPT |  | why-wrong rewritten; method line. |
| CIVIO-GI-ENV-PRINCIPLE-060100 | R.A. 9147, Sec. 2(b) | ACCEPT |  | 3 distractor(s) replaced; why-wrong rewritten; method line. |

## Asks for CoS

1. Pass, fix or reject each ID (table above).
2. Rule on fact duplicates: keep the applied scenario and the recall item both, or one per fact?
3. After your pass, items go approved/passed; activation stays a separate step.
