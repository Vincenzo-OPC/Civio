# Audit round 02 fixes (CoS round 02 rulings, 2026-10-13)

Rulings applied: spec §10.5 (v0.1.6). GT's shortcut request: spec §10.6 (v0.1.7).

**Where the changes live.** Every rewrite of an approved item is in `docs/research/round-02-fixes.json` (178 items, same ids, status draft, review_status "changed"). Each item has a `replaces` field with its old stem and old key. The committed batch files and the local Civio DB keep the approved versions until CoS passes the rewrites. Note: the importer matches on stem, so when the rewrites are merged, the old-stem rows have to be retired in the DB, or they will be left behind as duplicates.

`qa_all.py` now checks the proposed bank (it overlays the fixes by id): **GREEN**. Run `qa_all.py --no-fixes` to check the committed files alone. That run fails the new frame cap and the new spelling-target rule, as expected, until the fixes are merged.

## 1. Spelling (93 items: 57 "misspelled", 36 "spelled correctly")
- Every batch spelling item now has its own target word, and no target repeats across the batches, the supplements or the baseline seed files.
- Every misspelling is a real one: doubled letters, ie/ei, silent letters, or sound-alike endings. There are no keyboard typos.
- Foils in the "misspelled" items are correctly spelled office words that are never used as targets.
- New code `SPL-SILENT`. `qa.py` checks that each coded error type describes its misspelling, and that targets are unique.
- **Ruling 4 (two wrong error labels):** 000194 (privilej) and 000195 (unanimus) are rewritten with new targets. Their new labels are machine-checked.
- Spelling stems now use 3 phrasings for "misspelled" items (19 each) and 2 for "spelled correctly" items (18 each).

| id | old target | new key | target word |
|---|---|---|---|
| CIVIO-CLR-SPELL-WRONG-000010 | ocassion | aquire | acquire |
| CIVIO-CLR-SPELL-RIGHT-000088 | millennium | apparent | apparent |
| CIVIO-CLR-SPELL-WRONG-000089 | definittely | arguement | argument |
| CIVIO-CLR-SPELL-WRONG-000090 | millnnium | basicly | basically |
| CIVIO-CLR-SPELL-WRONG-000092 | parliamnt | benificial | beneficial |
| CIVIO-CLR-SPELL-WRONG-000093 | personel | beleive | believe |
| CIVIO-CLR-SPELL-WRONG-000094 | acquaintence | changable | changeable |
| CIVIO-CLR-SPELL-WRONG-000096 | liison | committment | commitment |
| CIVIO-CLR-SPELL-WRONG-000098 | separrate | concious | conscious |
| CIVIO-CLR-SPELL-WRONG-000099 | accessble | decieve | deceive |
| CIVIO-CLR-SPELL-WRONG-000100 | vacum | dependant | dependent |
| CIVIO-CLR-SPELL-WRONG-000101 | pronnciation | dissapoint | disappoint |
| CIVIO-CLR-SPELL-WRONG-000187 | commitmant | disipline | discipline |
| CIVIO-CLR-SPELL-WRONG-000188 | maintennce | eigth | eighth |
| CIVIO-CLR-SPELL-RIGHT-000189 | fluorescent | environment | environment |
| CIVIO-CLR-SPELL-WRONG-000191 | consceince | equiptment | equipment |
| CIVIO-CLR-SPELL-WRONG-000192 | harss | especialy | especially |
| CIVIO-CLR-SPELL-WRONG-000194 | privilej | excede | exceed |
| CIVIO-CLR-SPELL-WRONG-000195 | unanimus | excellant | excellent |
| CIVIO-CLR-SPELL-RIGHT-000196 | conscience | existence | existence |
| CIVIO-CLR-SPELL-RIGHT-000197 | acknowledgment | familiar | familiar |
| CIVIO-CLR-SPELL-RIGHT-000199 | accessible | fascinate | fascinate |
| CIVIO-CLR-SPELL-WRONG-000201 | privillege | Febuary | February |
| CIVIO-CLR-SPELL-WRONG-000287 | receve | fullfill | fulfill |
| CIVIO-CLR-SPELL-WRONG-000289 | commttee | goverment | government |
| CIVIO-CLR-SPELL-WRONG-000291 | mischevous | grammer | grammar |
| CIVIO-CLR-SPELL-WRONG-000292 | indepndence | guidence | guidance |
| CIVIO-CLR-SPELL-WRONG-000293 | occsionally | hieght | height |
| CIVIO-CLR-SPELL-RIGHT-000295 | receipt | incidentally | incidentally |
| CIVIO-CLR-SPELL-WRONG-000296 | atendance | interupt | interrupt |
| CIVIO-CLR-SPELL-RIGHT-000298 | recommend | knowledge | knowledge |
| CIVIO-CLR-SPELL-WRONG-000300 | licnse | liesure | leisure |
| CIVIO-CLR-SPELL-WRONG-000301 | inculate | libary | library |
| CIVIO-CLR-SPELL-WRONG-000387 | addres | lighning | lightning |
| CIVIO-CLR-SPELL-RIGHT-000390 | phenomenon | marriage | marriage |
| CIVIO-CLR-SPELL-WRONG-000391 | foregn | medecine | medicine |
| CIVIO-CLR-SPELL-RIGHT-000394 | allotment | mortgage | mortgage |
| CIVIO-CLR-SPELL-RIGHT-000395 | pronunciation | neighbor | neighbor |
| CIVIO-CLR-SPELL-WRONG-000396 | phenomnon | nineth | ninth |
| CIVIO-CLR-SPELL-WRONG-000397 | apropriation | noticable | noticeable |
| CIVIO-CLR-SPELL-RIGHT-000399 | calendar | obedience | obedience |
| CIVIO-CLR-SPELL-RIGHT-000400 | achievement | opportunity | opportunity |
| CIVIO-CLR-SPELL-WRONG-000487 | emberrass | paralell | parallel |
| CIVIO-CLR-SPELL-WRONG-000488 | beginnng | percieve | perceive |
| CIVIO-CLR-SPELL-WRONG-000489 | noticeble | perseverence | perseverance |
| CIVIO-CLR-SPELL-RIGHT-000492 | definitely | persistent | persistent |
| CIVIO-CLR-SPELL-WRONG-000494 | ocurred | posess | possess |
| CIVIO-CLR-SPELL-WRONG-000496 | notticeable | preceed | precede |
| CIVIO-CLR-SPELL-WRONG-000498 | exstence | prefered | preferred |
| CIVIO-CLR-SPELL-RIGHT-000499 | acquaintance | prejudice | prejudice |
| CIVIO-CLR-SPELL-WRONG-000500 | liutenant | presense | presence |
| CIVIO-CLR-SPELL-WRONG-000501 | irrelvant | procede | proceed |
| CIVIO-CLR-SPELL-WRONG-000587 | sieze | publically | publicly |
| CIVIO-CLR-SPELL-WRONG-000588 | defintely | referance | reference |
| CIVIO-CLR-SPELL-WRONG-000590 | seze | relevent | relevant |
| CIVIO-CLR-SPELL-RIGHT-000591 | transferred | religious | religious |
| CIVIO-CLR-SPELL-WRONG-000596 | threshld | rememberance | remembrance |
| CIVIO-CLR-SPELL-RIGHT-000598 | guarantee | resistance | resistance |
| CIVIO-CLR-SPELL-WRONG-000599 | conscince | restaraunt | restaurant |
| CIVIO-CLR-SPELL-WRONG-000600 | grivance | rythm | rhythm |
| CIVIO-CLR-SPELL-RIGHT-000601 | beginning | ridiculous | ridiculous |
| CIVIO-CLR-SPELL-RIGHT-000687 | separate | scissors | scissors |
| CIVIO-CLR-SPELL-RIGHT-000689 | entrepreneur | secretary | secretary |
| CIVIO-CLR-SPELL-RIGHT-000691 | lieutenant | siege | siege |
| CIVIO-CLR-SPELL-RIGHT-000692 | disbursement | similar | similar |
| CIVIO-CLR-SPELL-RIGHT-000694 | colleague | sincerely | sincerely |
| CIVIO-CLR-SPELL-RIGHT-000699 | unanimous | subtle | subtle |
| CIVIO-CLR-SPELL-WRONG-000700 | forreign | succede | succeed |
| CIVIO-CLR-SPELL-RIGHT-000701 | independence | successful | successful |
| CIVIO-CLR-SPELL-RIGHT-000787 | occasionally | surprise | surprise |
| CIVIO-CLR-SPELL-RIGHT-000789 | manageable | temperature | temperature |
| CIVIO-CLR-SPELL-WRONG-000791 | gurantee | tendancy | tendency |
| CIVIO-CLR-SPELL-RIGHT-000793 | maintenance | thorough | thorough |
| CIVIO-CLR-SPELL-WRONG-000795 | conscence | tommorow | tomorrow |
| CIVIO-CLR-SPELL-WRONG-000800 | inoculte | tounge | tongue |
| CIVIO-CLR-SPELL-RIGHT-000801 | reimbursement | truly | truly |
| CIVIO-CLR-SPELL-RIGHT-000887 | liaison | twelfth | twelfth |
| CIVIO-CLR-SPELL-WRONG-000889 | indpendence | untill | until |
| CIVIO-CLR-SPELL-RIGHT-000891 | noticeable | vacuum | vacuum |
| CIVIO-CLR-SPELL-WRONG-000892 | beleve | viscious | vicious |
| CIVIO-CLR-SPELL-WRONG-000893 | occrrence | Wensday | Wednesday |
| CIVIO-CLR-SPELL-WRONG-000898 | correspondance | wierd | weird |
| CIVIO-CLR-SPELL-RIGHT-000900 | cemetery | yield | yield |
| CIVIO-CLR-SPELL-RIGHT-000901 | occurrence | handkerchief | handkerchief |
| CIVIO-CLR-SPELL-WRONG-000989 | questonnaire | psycology | psychology |
| CIVIO-CLR-SPELL-WRONG-000990 | collague | neumonia | pneumonia |
| CIVIO-CLR-SPELL-WRONG-000992 | persnnel | colum | column |
| CIVIO-CLR-SPELL-RIGHT-000994 | parliament | doubt | doubt |
| CIVIO-CLR-SPELL-RIGHT-000996 | schedule | island | island |
| CIVIO-CLR-SPELL-RIGHT-000997 | foreign | counterfeit | counterfeit |
| CIVIO-CLR-SPELL-WRONG-000998 | reciept | hygeine | hygiene |
| CIVIO-CLR-SPELL-RIGHT-000999 | miscellaneous | foreign | foreign |
| CIVIO-CLR-SPELL-WRONG-001000 | recmmend | acheivement | achievement |

## 3. Frame cap (25% of a subject)
- **Verbal:** "Choose the word that best completes the sentence" is down from 89 of 203 items to 29 (60 rewritten). The sentence, options and key are unchanged; only the lead-in changed, matched to the concept:
  - agreement, 15 items: "Which verb agrees with the subject of the sentence?"
  - confused words, 21: "Which word correctly fills the blank?"
  - prepositions, 14: "Which preposition correctly fills the blank?"
  - pronoun case, 10: "Which pronoun correctly fills the blank?"
- **Numerical:** 25 of the 30 N + N × N − N items moved to 5 other shapes (5 each): (a + b) × c − d, a × b − e ÷ d, a − b × c + d, a + b × (c − d), and (a × b + g) ÷ d. Five keep the original shape. Every key and distractor was recomputed, and `qa.py`'s solver now evaluates brackets and ÷ exactly.
- **Highest phrasing per subject now:** clerical filing FIRST 34/151, Verbal "best completes" 29/203, and Verbal "Choose the correct verb" 29/203. All are under 25%. `qa.py` enforces the cap.

| id | old stem | new stem | key |
|---|---|---|---|
| CIVIO-NUM-OPS-ORDER-000039 | What is the value of 4 + 8 × 2 − 5? | What is the value of (4 + 8) × 2 − 5? | 19 |
| CIVIO-NUM-OPS-ORDER-000041 | What is the value of 9 + 4 × 3 − 1? | What is the value of 9 × 4 − 9 ÷ 3? | 33 |
| CIVIO-NUM-OPS-ORDER-000118 | What is the value of 3 + 3 × 7 − 2? | What is the value of 3 − 3 × 7 + 2? | -16 |
| CIVIO-NUM-OPS-ORDER-000131 | What is the value of 2 + 8 × 7 − 8? | What is the value of 2 + 8 × (7 − 8)? | -6 |
| CIVIO-NUM-OPS-ORDER-000135 | What is the value of 14 + 2 × 3 − 7? | What is the value of (14 × 2 + 7) ÷ 7? | 5 |
| CIVIO-NUM-OPS-ORDER-000235 | What is the value of 17 + 6 × 8 − 3? | What is the value of (17 + 6) × 8 − 3? | 181 |
| CIVIO-NUM-OPS-ORDER-000240 | What is the value of 19 + 2 × 5 − 2? | What is the value of 19 × 2 − 10 ÷ 2? | 33 |
| CIVIO-NUM-OPS-ORDER-000319 | What is the value of 8 + 5 × 2 − 3? | What is the value of 8 − 5 × 2 + 3? | 1 |
| CIVIO-NUM-OPS-ORDER-000321 | What is the value of 9 + 4 × 5 − 9? | What is the value of 9 + 4 × (5 − 9)? | -7 |
| CIVIO-NUM-OPS-ORDER-000322 | What is the value of 8 + 8 × 8 − 3? | What is the value of (8 × 8 + 16) ÷ 2? | 40 |
| CIVIO-NUM-OPS-ORDER-000416 | What is the value of 14 + 2 × 7 − 6? | What is the value of (14 + 2) × 7 − 6? | 106 |
| CIVIO-NUM-OPS-ORDER-000433 | What is the value of 5 + 3 × 6 − 1? | What is the value of 5 × 3 − 18 ÷ 3? | 9 |
| CIVIO-NUM-OPS-ORDER-000520 | What is the value of 6 + 4 × 8 − 7? | What is the value of 6 − 4 × 8 + 7? | -19 |
| CIVIO-NUM-OPS-ORDER-000525 | What is the value of 14 + 2 × 5 − 8? | What is the value of 14 + 2 × (5 − 8)? | 8 |
| CIVIO-NUM-OPS-ORDER-000536 | What is the value of 14 + 7 × 6 − 8? | What is the value of (14 × 7 + 12) ÷ 2? | 55 |
| CIVIO-NUM-OPS-ORDER-000638 | What is the value of 8 + 4 × 7 − 2? | What is the value of (8 + 4) × 7 − 2? | 82 |
| CIVIO-NUM-OPS-ORDER-000640 | What is the value of 18 + 3 × 2 − 6? | What is the value of 18 × 3 − 12 ÷ 6? | 52 |
| CIVIO-NUM-OPS-ORDER-000719 | What is the value of 17 + 9 × 3 − 12? | What is the value of 17 − 9 × 3 + 12? | 2 |
| CIVIO-NUM-OPS-ORDER-000720 | What is the value of 14 + 2 × 9 − 1? | What is the value of 14 + 2 × (9 − 1)? | 30 |
| CIVIO-NUM-OPS-ORDER-000729 | What is the value of 15 + 7 × 3 − 3? | What is the value of (15 × 7 + 6) ÷ 3? | 37 |
| CIVIO-NUM-OPS-ORDER-000833 | What is the value of 3 + 8 × 7 − 8? | What is the value of (3 + 8) × 7 − 8? | 69 |
| CIVIO-NUM-OPS-ORDER-000839 | What is the value of 6 + 6 × 5 − 2? | What is the value of 6 × 6 − 10 ÷ 2? | 31 |
| CIVIO-NUM-OPS-ORDER-000912 | What is the value of 7 + 3 × 6 − 11? | What is the value of 7 − 3 × 6 + 11? | 0 |
| CIVIO-NUM-OPS-ORDER-000914 | What is the value of 10 + 6 × 7 − 6? | What is the value of 10 + 6 × (7 − 6)? | 16 |
| CIVIO-NUM-OPS-ORDER-000932 | What is the value of 20 + 5 × 3 − 1? | What is the value of (20 × 5 + 6) ÷ 2? | 53 |

Verbal lead-in changes (key unchanged): 000071, 000074, 000077, 000169, 000170, 000175, 000179, 000181, 000183, 000272, 000274, 000281, 000286, 000368, 000371, 000372, 000373, 000467, 000472, 000473, 000477, 000481, 000570, 000571, 000572, 000580, 000583, 000585, 000667, 000671, 000673, 000675, 000681, 000683, 000684, 000685, 000686, 000768, 000770, 000775, 000776, 000778, 000779, 000784, 000868, 000869, 000873, 000874, 000877, 000879, 000883, 000884, 000967, 000968, 000971, 000973, 000976, 000977, 000982, 000984.

## 2. Filing coverage: gap-fill-003 (10 new drafts)
`docs/research/gap-fill-003.json`, ARMA Rules 2, 3, 4, 7 and 8, two items each. Each key is computed from the indexed units by `scripts/batches/fixes/gap3_filing.py`. Each cites ARMA / ANSI/ARMA 12-2005, not CSC. Each distractor is the result of breaking one named rule.

| id | rule | asks | key | trap |
|---|---|---|---|---|
| CIVIO-GAP3-CLR-FILE-ORDER-0015 | ARMA Rule 2 | FIRST | R & S Hardware | skips the symbol |
| CIVIO-GAP3-CLR-FILE-ORDER-0016 | ARMA Rule 2 | LAST | Luz of the Valley Resort | breaks ARMA Rule 2 |
| CIVIO-GAP3-CLR-FILE-ORDER-0017 | ARMA Rule 3 | FIRST | Ana Carinderia | drops the possessive s |
| CIVIO-GAP3-CLR-FILE-ORDER-0018 | ARMA Rule 3 | LAST | Cruz-Lim Trading | splits the hyphenated name |
| CIVIO-GAP3-CLR-FILE-ORDER-0019 | ARMA Rule 4 | FIRST | J. Ramos | breaks ARMA Rule 4 |
| CIVIO-GAP3-CLR-FILE-ORDER-0020 | ARMA Rule 4 | FIRST | A B Cruz Store | splits the acronym |
| CIVIO-GAP3-CLR-FILE-ORDER-0021 | ARMA Rule 7 | FIRST | 7 Seas Shipping | compares digits one by one |
| CIVIO-GAP3-CLR-FILE-ORDER-0022 | ARMA Rule 7 | LAST | Three Sisters Bakery | breaks ARMA Rule 7 |
| CIVIO-GAP3-CLR-FILE-ORDER-0023 | ARMA Rule 8 | LAST | University of the East | drops a minor word |
| CIVIO-GAP3-CLR-FILE-ORDER-0024 | ARMA Rule 8 | LAST | Ateneo Law School | drops a minor word |

## 5. VFIL-0007 recode
CIVIO-GAP1-VFIL-WIKAIN-0007, option o2 ("madaling magalit"): code FIL-SAME-FIELD → `FIL-OTHER-TRAIT` (new code in §3.3). The why-wrong line now says it is a real trait unrelated to the idiom. Codes only, as CoS ruled.

## Gap-fill 002 (CoS PASS, fixes applied)
- VEN-ERROR-0005 o4 → VEN-FORM.
- VEN-ERROR-0003 o2 ("myself") → VEN-FORM.
- NUM-FRAC-DEC-0007 o1 now reads "moved 2 places", and o2 now reads "adds instead of multiplies" (2.5 + 0.04 = 2.54).
- NUM-FRAC-DEC-0011 o4 now reads "drops the fraction part: 1 × 3/5".
- All 14 are marked approved/passed by Chief of Staff, 2026-10-13.

## Shortcut field (GT request; spec v0.1.7)
- New optional item-level `shortcut`. `qa.py` accepts it and rejects an empty or padded one.
- The importer shows it first as "Shortcut: …", with the worked steps after it as "Method: …". There is no UI change, and items without the field render exactly as before (Pest test added).
- **Numerical backfill:** `docs/research/shortcuts-num-001.json` has 267 shortcuts. Each was evaluated on the item's own numbers and equals the key.
- 36 items were skipped on purpose: age problems, and sequences that are not constant second-difference. These have no honest shortcut beyond the Reveal method.
- The shortcuts are not merged into the items and not imported until CoS passes them.

