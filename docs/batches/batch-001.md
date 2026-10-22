# Civio batch 001 (approved: CoS PASS, final per GT delegation)

Spec: `docs/CSE-Question-Design-Spec.md` v0.1.3. Author: CSE (Grok Bot, AI-assisted). Reviewer: Chief of Staff.
**Review result: CoS PASS on all 10 items (2026-10-13). Final approval: GT delegated approvals to Chief of Staff.**
All items are original, `source_group: civio`. Bank status on import: `active` (`php artisan civio:import-batch docs/batches/batch-001.json`). Seed-ready copy: `docs/batches/batch-001.json`.
Civio is an independent reviewer and is not affiliated with the Civil Service Commission.

Mix: 3 Numerical, 3 Verbal (English), 2 General Information, 1 Analytical (Professional), 1 Clerical spelling (Subprofessional).
Post-review fixes: Item 3 r3 code is now `NUM-OTHER-SHARE`; Item 9 y2 code is now `ANA-OTHER-RELATION` with a reworded Reveal line.

## 1. CIVIO-NUM-WP-PCT-CHANGE-000001

- track: both · domain: numerical · archetype: NUM-WP-PCT-CHANGE · difficulty: medium · est: 90 s
- competency: Word problems · concept: successive percent change
- micro_skill: chain a percent increase and a percent decrease on the same price
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** A store sold a sack of rice for ₱250. It raised the price by 20%. A week later, it cut the new price by 20%. What is the final price of the sack?

| option_id | text | shown as |
|---|---|---|
| n1 | ₱240 | A |
| n2 | ₱250 | B |
| n3 | ₱288 | C |
| n4 | ₱300 | D |

`answer_option_id`: n1 (₱240)

`distractor_reasoning`: n2 = `NUM-PCT-ADD`; n3 = `NUM-EXTRA-STEP`; n4 = `NUM-PARTIAL`

**Reveal**

1. *Meaning.* "Percent" means "out of 100". 20% of a price is 20 pesos for every 100 pesos. "Raise by 20%" means add 20% of the price at that moment. "Cut by 20%" means take away 20% of the price at that moment.
2. *Shortcut.* Each change uses the price right before it. Tiny example: ₱100 up 10% is ₱110. Then down 10% is ₱110 − ₱11 = ₱99, not ₱100. Now this item: ₱250 up 20% is ₱250 + ₱50 = ₱300. Then down 20% of ₱300 is ₱300 − ₱60 = ₱240.
3. *Why it is right.* ₱240 is right. Check another way: 250 × 1.2 = 300, and 300 × 0.8 = 240.
4. *Why the others are wrong.*
   - ₱250: ₱250 treats +20% and −20% as cancelling out. The cut is taken from the bigger price, ₱300, so it removes more than the raise added.
   - ₱288: ₱288 adds the 20% raise again to ₱240. That is one step too many.
   - ₱300: ₱300 is only the price after the raise. It stops before the cut.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 2. CIVIO-NUM-SEQ-DIFF-000002

- track: both · domain: numerical · archetype: NUM-SEQ-DIFF · difficulty: medium · est: 45 s
- competency: Number sequence · concept: number series with growing differences
- micro_skill: find the rule in the differences and extend it
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** What number comes next in the series?  4, 7, 12, 19, 28, ___

| option_id | text | shown as |
|---|---|---|
| s1 | 31 | A |
| s2 | 37 | B |
| s3 | 39 | C |
| s4 | 41 | D |

`answer_option_id`: s3 (39)

`distractor_reasoning`: s1 = `NUM-SEQ-OTHER-RULE`; s2 = `NUM-PARTIAL`; s4 = `NUM-OFF-BY-ONE`

**Reveal**

1. *Meaning.* A "series" is a list of numbers that follows one rule. The "difference" is how much you add to get from one number to the next.
2. *Shortcut.* Write the jumps under the list. 4 to 7 is +3. 7 to 12 is +5. 12 to 19 is +7. 19 to 28 is +9. The jumps go up by 2 each time. So the next jump is +11.
3. *Why it is right.* 39 is right: 28 + 11 = 39. Check the jumps: 3, 5, 7, 9, 11 each grow by 2.
4. *Why the others are wrong.*
   - 31: 31 adds only the first jump, +3, to 28. The jump does not stay at 3.
   - 37: 37 repeats the last jump, +9. The jump keeps growing, so it should be +11.
   - 41: 41 adds 13. That skips one step in the jumps (it goes 9 then 13 instead of 9 then 11).

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 3. CIVIO-NUM-WP-RATIO-000003

- track: both · domain: numerical · archetype: NUM-WP-RATIO · difficulty: medium · est: 75 s
- competency: Word problems · concept: ratio
- micro_skill: split a total in a given ratio and find the larger share
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** A barangay will split a ₱18,000 cleanup fund between Purok Uno and Purok Dos in the ratio 4 : 5. How much will Purok Dos receive?

| option_id | text | shown as |
|---|---|---|
| r1 | ₱2,000 | A |
| r2 | ₱3,600 | B |
| r3 | ₱8,000 | C |
| r4 | ₱10,000 | D |

`answer_option_id`: r4 (₱10,000)

`distractor_reasoning`: r1 = `NUM-PARTIAL`; r2 = `NUM-WRONG-BASE`; r3 = `NUM-OTHER-SHARE`

**Reveal**

1. *Meaning.* A "ratio" of 4 : 5 means that for every 4 pesos one side gets, the other side gets 5 pesos.
2. *Shortcut.* Add the ratio numbers to get the number of equal parts: 4 + 5 = 9 parts. One part is the total ÷ 9. Then multiply by the parts you need. Tiny example: ₱90 in 4 : 5 gives 9 parts of ₱10, so ₱40 and ₱50.
3. *Why it is right.* ₱10,000 is right. ₱18,000 ÷ 9 = ₱2,000 per part. Purok Dos has 5 parts: 5 × ₱2,000 = ₱10,000. Check: ₱8,000 + ₱10,000 = ₱18,000.
4. *Why the others are wrong.*
   - ₱2,000: ₱2,000 is the value of one part. It stops before multiplying by 5.
   - ₱3,600: ₱3,600 divides ₱18,000 by 5 alone. It should divide by all 9 parts.
   - ₱8,000: ₱8,000 is Purok Uno's share (4 parts). The question asks for Purok Dos.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 4. CIVIO-VEN-WORD-MEANING-000004

- track: both · domain: verbal_en · archetype: VEN-WORD-MEANING · difficulty: easy · est: 20 s
- competency: Vocabulary (word meaning) · concept: word meaning in context
- micro_skill: choose the sense of 'defer' that fits the sentence
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** What is the meaning of the word "defer" in the sentence?  The council chose to defer the vote on the new parking rules until all barangay captains could attend.

| option_id | text | shown as |
|---|---|---|
| w1 | postpone | A |
| w2 | cancel | B |
| w3 | yield to another's opinion | C |
| w4 | hurry | D |

`answer_option_id`: w1 (postpone)

`distractor_reasoning`: w2 = `RC-EXTREME`; w3 = `RC-NOT-IN-TEXT`; w4 = `RC-OPPOSITE`

**Reveal**

1. *Meaning.* "Context" means the words around a word. They tell you which meaning the writer wants.
2. *Shortcut.* Swap each choice into the sentence and read it again. Keep the one that still makes sense. The clue here is "until all barangay captains could attend". That points to a later time.
3. *Why it is right.* "Postpone" is right. "The council chose to postpone the vote ... until all barangay captains could attend" means the vote moves to a later day.
4. *Why the others are wrong.*
   - cancel: "Cancel" goes too far. "Until" shows the vote will still happen later.
   - yield to another's opinion: "Yield to another's opinion" is a real meaning of "defer" (as in "defer to the expert"). It does not fit a vote that is being moved.
   - hurry: "Hurry" is the opposite. Waiting for everyone slows the vote down.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 5. CIVIO-VEN-SENT-COMP-PHRASAL-000005

- track: both · domain: verbal_en · archetype: VEN-SENT-COMP-PHRASAL · difficulty: easy · est: 25 s
- competency: Sentence completion · concept: phrasal verbs
- micro_skill: pick the particle that gives 'call ___' the meaning 'cancel'
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** Because of the typhoon warning, the town fiesta parade was called ______.

| option_id | text | shown as |
|---|---|---|
| p1 | off | A |
| p2 | out | B |
| p3 | up | C |
| p4 | in | D |

`answer_option_id`: p1 (off)

`distractor_reasoning`: p2 = `VEN-PARTICLE`; p3 = `VEN-PARTICLE`; p4 = `VEN-PARTICLE`

**Reveal**

1. *Meaning.* A "phrasal verb" is a verb plus a small word like off, out, up or in. The small word changes the meaning.
2. *Shortcut.* Ask what happens to a parade during a typhoon warning. It is stopped before it starts. Then match that meaning: "call off" = cancel.
3. *Why it is right.* "Off" is right. "The parade was called off" means it was cancelled because of the typhoon.
4. *Why the others are wrong.*
   - out: "Called out" means named or criticized in public. It does not mean cancelled.
   - up: "Called up" means phoned or summoned, for example for duty. A parade is not phoned.
   - in: "Called in" means asked to come, like calling in extra staff. It does not stop an event.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 6. CIVIO-VEN-SENT-COMP-WORD-000006

- track: both · domain: verbal_en · archetype: VEN-SENT-COMP-WORD · difficulty: medium · est: 25 s
- competency: Sentence completion · concept: commonly confused words
- micro_skill: tell 'affect' (verb) from 'effect'
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** The new route ordinance will ______ every tricycle driver in the municipality.

| option_id | text | shown as |
|---|---|---|
| a1 | affect | A |
| a2 | effect | B |
| a3 | afflict | C |
| a4 | infect | D |

`answer_option_id`: a1 (affect)

`distractor_reasoning`: a2 = `VEN-HOMOPHONE`; a3 = `VEN-REGISTER`; a4 = `VEN-HOMOPHONE`

**Reveal**

1. *Meaning.* A "verb" is an action word. A "noun" is a thing. Here the blank needs a verb, because it comes right after "will".
2. *Shortcut.* Remember "A for Action": "affect" is the action (to change or influence). "Effect" is usually the result, a thing. Tiny example: "Rain affects traffic. The effect is delay."
3. *Why it is right.* "Affect" is right. "The ordinance will affect every driver" means it will change how every driver works.
4. *Why the others are wrong.*
   - effect: "Effect" sounds the same but is usually a noun (a result). As a verb it means "to bring about", and you cannot bring about a driver.
   - afflict: "Afflict" means to cause pain or suffering. It is too strong and negative for a route rule.
   - infect: "Infect" means to spread a disease. It only sounds close to "affect".

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 7. CIVIO-GI-WHO-HOLDS-POWER-000007

- track: both · domain: general_information · archetype: GI-WHO-HOLDS-POWER · difficulty: easy · est: 20 s
- competency: Philippine Constitution · concept: impeachment
- micro_skill: name the body with the exclusive power to initiate impeachment
- source: 1987 Const., Art. XI, Sec. 3(1) (https://lawphil.net/consti/cons1987.html)
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** Under the 1987 Constitution, which body has the exclusive power to initiate all cases of impeachment?

| option_id | text | shown as |
|---|---|---|
| g1 | House of Representatives | A |
| g2 | Senate | B |
| g3 | Supreme Court | C |
| g4 | Office of the Ombudsman | D |

`answer_option_id`: g1 (House of Representatives)

`distractor_reasoning`: g2 = `GI-WRONG-BODY`; g3 = `GI-WRONG-BODY`; g4 = `GI-SOUNDS-RIGHT`

**Reveal**

1. *Meaning.* "Impeachment" is the way Congress can remove top officials, like the President or the Ombudsman. "Initiate" means start the case.
2. *Shortcut.* Think of a court case: one side files, the other side judges. In impeachment the House files (starts) and the Senate judges (tries).
3. *Why it is right.* "House of Representatives" is right. Article XI, Section 3(1) says the House has the exclusive power to initiate all cases of impeachment.
4. *Why the others are wrong.*
   - Senate: The Senate tries and decides impeachment cases (Art. XI, Sec. 3(6)). It does not start them.
   - Supreme Court: The Supreme Court does not start impeachment. Its Chief Justice only presides when the President is on trial in the Senate (Art. XI, Sec. 3(6)).
   - Office of the Ombudsman: The Ombudsman investigates complaints against officials (Art. XI, Sec. 13). The Ombudsman can be impeached but does not start impeachment.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 8. CIVIO-GI-SCENARIO-APPLY-000008

- track: both · domain: general_information · archetype: GI-SCENARIO-APPLY · difficulty: medium · est: 35 s
- competency: Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) · concept: norms of conduct
- micro_skill: match a described behavior to the R.A. 6713 norm it shows
- source: R.A. 6713, Sec. 4(A)(h) (https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html)
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** A municipal assessor and her family live within her salary. They avoid showing off expensive cars, jewelry, or parties. Which norm of conduct under R.A. 6713 does this best show?

| option_id | text | shown as |
|---|---|---|
| e1 | Simple living | A |
| e2 | Professionalism | B |
| e3 | Commitment to public interest | C |
| e4 | Nationalism and patriotism | D |

`answer_option_id`: e1 (Simple living)

`distractor_reasoning`: e2 = `GI-SIBLING-TERM`; e3 = `GI-SIBLING-TERM`; e4 = `GI-SIBLING-TERM`

**Reveal**

1. *Meaning.* A "norm of conduct" is a standard of behavior that every government worker must follow. R.A. 6713 Section 4(A) lists eight of them.
2. *Shortcut.* Find the key idea in the story and match it to the name. Here the key idea is a modest lifestyle with no showing off of wealth. The norm with "modest lives" in it is Simple living.
3. *Why it is right.* "Simple living" is right. R.A. 6713, Sec. 4(A)(h) says officials and their families shall lead modest lives that fit their position and income, and shall not make an extravagant display of wealth.
4. *Why the others are wrong.*
   - Professionalism: Professionalism (Sec. 4(A)(b)) is about doing the job with excellence and skill. The story is about lifestyle, not job skill.
   - Commitment to public interest: Commitment to public interest (Sec. 4(A)(a)) is about putting the public first and not wasting government funds. The story is about the family's own spending.
   - Nationalism and patriotism: Nationalism and patriotism (Sec. 4(A)(f)) is about loyalty to the country and using local products. The story does not mention that.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 9. CIVIO-ANA-ANALOGY-PART-WHOLE-000009

- track: pro · domain: analytical · archetype: ANA-ANALOGY-PART/WHOLE · difficulty: easy · est: 30 s
- competency: Word association (analogy) · concept: part to whole
- micro_skill: keep the part-to-whole direction
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** PAGE : BOOK :: ______

| option_id | text | shown as |
|---|---|---|
| y1 | barangay : municipality | A |
| y2 | library : book | B |
| y3 | author : manuscript | C |
| y4 | page : paper | D |

`answer_option_id`: y1 (barangay : municipality)

`distractor_reasoning`: y2 = `ANA-OTHER-RELATION`; y3 = `ANA-SAME-TOPIC`; y4 = `ANA-ONE-LINK`

**Reveal**

1. *Meaning.* An "analogy" compares two pairs. The second pair must have the same link, in the same order, as the first pair.
2. *Shortcut.* Make a short sentence for the first pair: "A page is one part of a book." Then test each choice in the same sentence.
3. *Why it is right.* "Barangay : municipality" is right. "A barangay is one part of a municipality." Same link, same order.
4. *Why the others are wrong.*
   - library : book: A library holds books: container and contents, not part and whole.
   - author : manuscript: "An author writes a manuscript." That is maker and product, not part and whole.
   - page : paper: "A page is made of paper." That is a material, and it links to only one word from the first pair.

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## 10. CIVIO-CLR-SPELL-WRONG-000010

- track: sub · domain: clerical · archetype: CLR-SPELL-WRONG · difficulty: easy · est: 15 s
- competency: Spelling · concept: commonly misspelled words
- micro_skill: spot the one misspelled word among hard but correct words
- source: Original, Civio
- status: approved · review_status: passed · reviewer: Chief of Staff (final approval, delegated by GT) (2026-10-13T19:16:00+08:00)

**Stem:** Which word is misspelled?

| option_id | text | shown as |
|---|---|---|
| c1 | accommodate | A |
| c2 | receive | B |
| c3 | maintenance | C |
| c4 | ocassion | D |

`answer_option_id`: c4 (ocassion)

`distractor_reasoning`: c1 = `SPL-DOUBLE`; c2 = `SPL-IE-EI`; c3 = `SPL-SOUND`

**Reveal**

1. *Meaning.* "Misspelled" means written with wrong letters. Only one choice is wrong here.
2. *Shortcut.* Check the double letters first, because they cause most errors. "Occasion" has a double c and a single s: oc-ca-sion.
3. *Why it is right.* "Ocassion" is the misspelled word. The correct spelling is "occasion": two c's, one s.
4. *Why the others are wrong.*
   - accommodate: "Accommodate" is correct. It has two c's and two m's, which looks odd but is right.
   - receive: "Receive" is correct. After c, the e comes before the i.
   - maintenance: "Maintenance" is correct. It is spelled "main-ten-ance", not like the verb "maintain".

Review: [x] CoS PASS (final, per GT delegation, 2026-10-13)

## Checks done by the author

- Math recomputed twice: Item 1: 250 × 1.2 = 300, 300 × 0.8 = 240 (and 250 + 50 − 60 = 240). Item 2: differences 3, 5, 7, 9, 11, so 28 + 11 = 39. Item 3: 18,000 ÷ 9 = 2,000; 5 × 2,000 = 10,000; 4 × 2,000 = 8,000; total 18,000.
- GI text checked against the LawPhil copies: 1987 Const. Art. XI Sec. 3(1), 3(6), Sec. 13; R.A. 6713 Sec. 4(A)(a), (b), (f), (h).
