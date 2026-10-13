# CIVIO MASTER RESEARCH + COMPLETE 1,160 QUESTION BANK

Snapshot date: 13 October 2026
Compiled from Vincenzo-OPC/Civio repository source files. This is a self-contained text dossier; source JSON files remain the canonical inputs.
IMPORTANT: Contains 1,160 questions, not 1,160 independently verified questions. The original 1,010 are now marked approved/passed in the repository following commit 4a996c2 (Chief of Staff approval), while the three new supplements total 150 draft/unreviewed. This approval is repository metadata, NOT independent verification by this assistant. These flags reflect repository metadata, not an independent factual audit. DO NOT ACTIVATE unreviewed content. No production deployment was made.

## Scope, constraints, and key research findings

The official CSC Examination Announcement No. 03, s. 2026 covers the CSE-PPT. SUBPROFESSIONAL: General Information (1987 Constitution; R.A. 6713; peace/human rights; environmental management and protection), Verbal Ability (English and Filipino, including word meaning, sentence completion, error recognition, sentence structure, paragraph organization and reading comprehension), Numerical Ability (English: basic operations, sequence and word problems), and Clerical Ability (English: filing and spelling). PROFESSIONAL replaces Clerical with Analytical Ability. No official CSC subtest percentage weights have been established from that announcement; Civio practice proportions are NOT claimed to be official. The cited passing standard is at least 80.00; calculator use is banned for the cited exam. Civio is not affiliated with CSC.

Existing batches 001–011: 1,010 entries. Domain totals: 303 Numerical, 251 Analytical, 203 English Verbal, 151 Clerical, 102 General Information. All 1,010 were tagged language=en, exposing a Filipino language gap. IMPORTANT UPDATED STATUS: As of commit 4a996c2, all 1,010 existing items are flagged approved/passed by Chief of Staff after fixes. Earlier in this session only 10 were flagged passed. Status flags changed concurrently; independently check the claimed approvals and question accuracy rather than relying on flags alone. Its 34 archetypes include many highly repeated templates, so precise similarity checking is needed despite zero identical existing stems and IDs.

New content created in this session: 80 original Filipino Verbal drafts (24 vocabulary, 20 completion, 10 grammar/structure, 20 comprehension, 6 organization); 30 original General Information drafts with primary-law links, adding environmental and human-rights coverage; and 40 original Clerical drafts (8 surname filing, 6 reference-number filing, 6 chronological filing, 20 spelling). These underwent structural/uniqueness checks, and filing-answer sorting was recomputed. They are not yet fully independently reviewed.

The importer was modified to require status=approved AND review_status=passed before active import, with regression tests. At compilation the supplement regression tests had passed; subsequent CI status may change. Check latest GitHub Actions before publishing. Do not claim a green full release or live availability.

Official source: https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf
1987 Constitution: https://lawphil.net/consti/cons1987.html
R.A. 6713: https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html
R.A. 9003: https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html
R.A. 8749: https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html
R.A. 9275: https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html
R.A. 9147: https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html
R.A. 9729: https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html
R.A. 11313: https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html

Secondary reviewer/examinee ecosystem was consulted for item archetypes, time pressure and distractor mechanisms only. The original source and pattern log follows in the full appended Civio design spec. No third-party reviewer questions are intentionally reproduced here.

## Independent Astra reviewer instructions

Work in small batches of 50 to 100. Solve each item BLIND before seeing its marked answer. Check exactly one defensible answer, explanation, distractor plausibility, typo/formatting, source authenticity, intended skill, natural Filipino wording, track appropriateness and timed difficulty. For laws, cite a section-level primary source. Independently calculate numerical/filing answers from the stem, flag hidden assumptions. Check duplicate and near-duplicate stems and templates across all 1,160 entries and any baseline bank. Record one ACCEPT / REVISE / REJECT / HOLD result per item, and concrete corrections. Never auto-approve by modifying metadata, publish drafts, change live scoring rules, claim CSC endorsement, or infer official test weightings. Never import material copied or lightly paraphrased from reviewer sites.

## Full questions, exact choices, marked keys and explanations

### 1 | CIVIO-NUM-WP-PCT-CHANGE-000001
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
A store sold a sack of rice for ₱250. It raised the price by 20%. A week later, it cut the new price by 20%. What is the final price of the sack?
A. ₱240
B. ₱250
C. ₱288
D. ₱300
MARKED ANSWER A. ₱240
WHY ₱240 is right. Check another way: 250 × 1.2 = 300, and 300 × 0.8 = 240.
SHORTCUT Each change uses the price right before it. Tiny example: ₱100 up 10% is ₱110. Then down 10% is ₱110 − ₱11 = ₱99, not ₱100. Now this item: ₱250 up 20% is ₱250 + ₱50 = ₱300. Then down 20% of ₱300 is ₱300 − ₱60 = ₱240.

### 2 | CIVIO-NUM-SEQ-DIFF-000002
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
What number comes next in the series?  4, 7, 12, 19, 28, ___
A. 31
B. 37
C. 39
D. 41
MARKED ANSWER C. 39
WHY 39 is right: 28 + 11 = 39. Check the jumps: 3, 5, 7, 9, 11 each grow by 2.
SHORTCUT Write the jumps under the list. 4 to 7 is +3. 7 to 12 is +5. 12 to 19 is +7. 19 to 28 is +9. The jumps go up by 2 each time. So the next jump is +11.

### 3 | CIVIO-NUM-WP-RATIO-000003
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
A barangay will split a ₱18,000 cleanup fund between Purok Uno and Purok Dos in the ratio 4 : 5. How much will Purok Dos receive?
A. ₱2,000
B. ₱3,600
C. ₱8,000
D. ₱10,000
MARKED ANSWER D. ₱10,000
WHY ₱10,000 is right. ₱18,000 ÷ 9 = ₱2,000 per part. Purok Dos has 5 parts: 5 × ₱2,000 = ₱10,000. Check: ₱8,000 + ₱10,000 = ₱18,000.
SHORTCUT Add the ratio numbers to get the number of equal parts: 4 + 5 = 9 parts. One part is the total ÷ 9. Then multiply by the parts you need. Tiny example: ₱90 in 4 : 5 gives 9 parts of ₱10, so ₱40 and ₱50.

### 4 | CIVIO-VEN-WORD-MEANING-000004
TRACK both | DOMAIN verbal_en | SKILL Vocabulary (word meaning) | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
What is the meaning of the word "defer" in the sentence?  The council chose to defer the vote on the new parking rules until all barangay captains could attend.
A. postpone
B. cancel
C. yield to another's opinion
D. hurry
MARKED ANSWER A. postpone
WHY "Postpone" is right. "The council chose to postpone the vote ... until all barangay captains could attend" means the vote moves to a later day.
SHORTCUT Swap each choice into the sentence and read it again. Keep the one that still makes sense. The clue here is "until all barangay captains could attend". That points to a later time.

### 5 | CIVIO-VEN-SENT-COMP-PHRASAL-000005
TRACK both | DOMAIN verbal_en | SKILL Sentence completion | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
Because of the typhoon warning, the town fiesta parade was called ______.
A. off
B. out
C. up
D. in
MARKED ANSWER A. off
WHY "Off" is right. "The parade was called off" means it was cancelled because of the typhoon.
SHORTCUT Ask what happens to a parade during a typhoon warning. It is stopped before it starts. Then match that meaning: "call off" = cancel.

### 6 | CIVIO-VEN-SENT-COMP-WORD-000006
TRACK both | DOMAIN verbal_en | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
The new route ordinance will ______ every tricycle driver in the municipality.
A. affect
B. effect
C. afflict
D. infect
MARKED ANSWER A. affect
WHY "Affect" is right. "The ordinance will affect every driver" means it will change how every driver works.
SHORTCUT Remember "A for Action": "affect" is the action (to change or influence). "Effect" is usually the result, a thing. Tiny example: "Rain affects traffic. The effect is delay."

### 7 | CIVIO-GI-WHO-HOLDS-POWER-000007
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
Under the 1987 Constitution, which body has the exclusive power to initiate all cases of impeachment?
A. House of Representatives
B. Senate
C. Supreme Court
D. Office of the Ombudsman
MARKED ANSWER A. House of Representatives
WHY "House of Representatives" is right. Article XI, Section 3(1) says the House has the exclusive power to initiate all cases of impeachment.
SHORTCUT Think of a court case: one side files, the other side judges. In impeachment the House files (starts) and the Senate judges (tries).
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 8 | CIVIO-GI-SCENARIO-APPLY-000008
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
A municipal assessor and her family live within her salary. They avoid showing off expensive cars, jewelry, or parties. Which norm of conduct under R.A. 6713 does this best show?
A. Simple living
B. Professionalism
C. Commitment to public interest
D. Nationalism and patriotism
MARKED ANSWER A. Simple living
WHY "Simple living" is right. R.A. 6713, Sec. 4(A)(h) says officials and their families shall lead modest lives that fit their position and income, and shall not make an extravagant display of wealth.
SHORTCUT Find the key idea in the story and match it to the name. Here the key idea is a modest lifestyle with no showing off of wealth. The norm with "modest lives" in it is Simple living.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 9 | CIVIO-ANA-ANALOGY-PART-WHOLE-000009
TRACK pro | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
PAGE : BOOK :: ______
A. barangay : municipality
B. library : book
C. author : manuscript
D. page : paper
MARKED ANSWER A. barangay : municipality
WHY "Barangay : municipality" is right. "A barangay is one part of a municipality." Same link, same order.
SHORTCUT Make a short sentence for the first pair: "A page is one part of a book." Then test each choice in the same sentence.

### 10 | CIVIO-CLR-SPELL-WRONG-000010
TRACK sub | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-001.json
STEM
Which word is misspelled?
A. accommodate
B. receive
C. maintenance
D. ocassion
MARKED ANSWER D. ocassion
WHY "Ocassion" is the misspelled word. The correct spelling is "occasion": two c's, one s.
SHORTCUT Check the double letters first, because they cause most errors. "Occasion" has a double c and a single s: oc-ca-sion.

### 11 | CIVIO-NUM-WP-RATE-000011
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Liza can encode a box of survey forms in 6 hours. Ramon can encode the same box in 3 hours. If they work together, how long will it take them to encode one box?
A. 30 minutes
B. 2 hours
C. 4 hours 30 minutes
D. 9 hours
MARKED ANSWER B. 2 hours
WHY 2 hours is right. Check: in 2 hours Liza does 2/6 = 1/3 and Ramon does 2/3. 1/3 + 2/3 = 1 whole box.
SHORTCUT Turn each time into "part of the job per hour", then add. Liza does 1/6 of the box each hour. Ramon does 1/3, which is 2/6. Together they do 3/6 = 1/2 of the box each hour. Half a box per hour means one box takes 2 hours.

### 12 | CIVIO-NUM-WP-AVERAGE-000012
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
The average age of the 5 staff members in a municipal library is 32. A new librarian who is 44 years old joins them. What is the new average age of the 6 staff members?
A. 34
B. 34.4
C. 38
D. 204
MARKED ANSWER A. 34
WHY 34 is right. Check the long way: 5 × 32 = 160. 160 + 44 = 204. 204 ÷ 6 = 34.
SHORTCUT Share the extra years. The new person is 44 − 32 = 12 years above the old average. Those 12 extra years are shared by all 6 people now: 12 ÷ 6 = 2. So the average goes up by 2: 32 + 2 = 34.

### 13 | CIVIO-NUM-WP-PCT-CHANGE-000013
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A cooperative member borrows ₱20,000 at 6% simple interest per year. How much interest will she owe after 2 years and 6 months?
A. ₱2,400
B. ₱3,000
C. ₱3,120
D. ₱23,000
MARKED ANSWER B. ₱3,000
WHY ₱3,000 is right. Check: 20,000 × 0.06 × 2.5 = 1,200 × 2.5 = 3,000.
SHORTCUT Find one year first, then multiply by the years. One year: 6% of ₱20,000 = ₱1,200. Six months is half a year, so 2 years and 6 months = 2.5 years. 2.5 × ₱1,200 = ₱3,000.

### 14 | CIVIO-NUM-WP-ALGEBRA-000014
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Teresa is 3 times as old as her son. In 12 years, she will be twice as old as her son. How old is Teresa now?
A. 12
B. 24
C. 36
D. 48
MARKED ANSWER C. 36
WHY 36 is right. Algebra check: son = s, Teresa = 3s. 3s + 12 = 2(s + 12), so 3s + 12 = 2s + 24, so s = 12 and Teresa = 36.
SHORTCUT Try the choices instead of using algebra. Take each choice as Teresa's age now, divide by 3 for the son, add 12 to both, and see if she is twice his age. 36: son is 12. In 12 years: 48 and 24. 48 is twice 24.

### 15 | CIVIO-ANA-SYLLOGISM-000015
TRACK pro | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
All records clerks in the provincial office are trained in filing. No employee trained in filing is a new hire. Which statement must be true?
A. All employees trained in filing are records clerks.
B. No records clerk in the provincial office is a new hire.
C. Some employees who are not new hires are not records clerks.
D. No new hire works in the records section.
MARKED ANSWER B. No records clerk in the provincial office is a new hire.
WHY "No records clerk in the provincial office is a new hire" is right. Every clerk is trained in filing, and nobody trained in filing is a new hire.
SHORTCUT Draw circles. The records-clerk circle sits inside the trained-in-filing circle. The new-hire circle sits outside the trained-in-filing circle. So the records-clerk circle cannot touch the new-hire circle.

### 16 | CIVIO-ANA-ASSUME-I-II-000016
TRACK pro | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Statement: The municipal treasurer's office will stay open until 7 p.m. so that working residents can pay their real property tax after work.
Assumption I: Some residents cannot pay during regular office hours because of their work.
Assumption II: Staying open later will increase the town's total tax collection.
Which assumption is implicit in the statement?
A. Only I
B. Only II
C. Both I and II
D. Neither I nor II
MARKED ANSWER A. Only I
WHY "Only I" is right. If no resident had trouble paying during work hours, there would be no reason to open until 7 p.m. So I is needed. If collection stayed the same, the plan could still help residents pay more easily. So II is not needed.
SHORTCUT Use the "if not" test. Say the opposite of each assumption and ask: does the plan still make sense? If the plan falls apart, the assumption is needed.

### 17 | CIVIO-ANA-SYMBOL-SERIES-000017
TRACK pro | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What letter comes next in the series?  B, E, I, N, ___
A. Q
B. S
C. T
D. U
MARKED ANSWER C. T
WHY T is right. Check by counting from N: O, P, Q, R, S, T is 6 steps.
SHORTCUT Change letters to numbers, then look at the jumps. B, E, I, N = 2, 5, 9, 14. The jumps are +3, +4, +5. The next jump is +6: 14 + 6 = 20, and the 20th letter is T.

### 18 | CIVIO-VEN-ERROR-TENSE-000019
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which part of the sentence contains an error?  Last Friday, the new clerk / finishes encoding / all the leave forms / before the office closed.
A. Last Friday, the new clerk
B. finishes encoding
C. all the leave forms
D. before the office closed
MARKED ANSWER B. finishes encoding
WHY "Finishes encoding" is the error. It is present tense, but "last Friday" is past. It should be "finished encoding".
SHORTCUT Find the time signal first, then check every verb against it. "Last Friday" is past. So every action in the sentence should be past.

### 19 | CIVIO-GI-DEADLINE-NUMBER-000020
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Under R.A. 6713, within how many working days must public officials and employees respond to letters and requests sent by the public?
A. 10 working days
B. 15 working days
C. 30 days
D. 45 working days
MARKED ANSWER B. 15 working days
WHY "15 working days" is right. R.A. 6713, Sec. 5(a) says officials and employees shall respond to letters and other communications from the public within fifteen working days from receipt, and the reply must state the action taken.
SHORTCUT Link each number in the law to its job: 15 = answer the public's letters. 30 = file the SALN after taking office. 45 = agency's yearly performance report. 10 = when a filed SALN can be copied.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 20 | CIVIO-NUM-WP-RATIO-000021
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Rhea and Liza will share ₱10,500 of prize money in the ratio 2 : 5. How much is Liza's share?
A. ₱7,500
B. ₱2,100
C. ₱1,500
D. ₱3,000
MARKED ANSWER A. ₱7,500
WHY ₱7,500 is right: 5 × ₱1,500 = ₱7,500. Check: ₱3,000 + ₱7,500 = ₱10,500.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 5 = 7. One part = ₱10,500 ÷ 7 = ₱1,500. Then multiply by the parts you need.

### 21 | CIVIO-NUM-WP-RATIO-000022
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Rogelio and Kimberly will share ₱25,000 of prize money in the ratio 3 : 7. How much is Kimberly's share?
A. ₱2,500
B. ₱3,571.43
C. ₱17,500
D. ₱7,500
MARKED ANSWER C. ₱17,500
WHY ₱17,500 is right: 7 × ₱2,500 = ₱17,500. Check: ₱7,500 + ₱17,500 = ₱25,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱25,000 ÷ 10 = ₱2,500. Then multiply by the parts you need.

### 22 | CIVIO-NUM-SEQ-DIFF-000023
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Find the next number in the series.  6, 12, 19, 27, 36, ___
A. 45
B. 42
C. 46
D. 47
MARKED ANSWER C. 46
WHY 46 is right: 36 + 10 = 46.
SHORTCUT Write the jumps under the list: +6, +7, +8, +9. Each jump is 1 more than the one before. So the next jump is +10.

### 23 | CIVIO-NUM-WP-PCT-CHANGE-000024
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A supplier sold a bag of cement for ₱1,200. It raised the price by 10%. Later, it lowered the new price by 40%. What is the final price?
A. ₱1,320
B. ₱871.20
C. ₱792
D. ₱840
MARKED ANSWER C. ₱792
WHY ₱792 is right. Check: 1,200 × 1.1 = 1,320, and 1,320 × 0.6 = 792.
SHORTCUT Do one change at a time. ₱1,200 up 10% is ₱1,200 + ₱120 = ₱1,320. Then 40% of ₱1,320 is ₱528, so ₱1,320 − ₱528 = ₱792.

### 24 | CIVIO-NUM-WP-ALGEBRA-000025
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Rogelio is 3 times as old as his daughter. In 5 years, Rogelio will be twice as old as the daughter. How old is Rogelio now?
A. 10
B. 20
C. 5
D. 15
MARKED ANSWER D. 15
WHY 15 is right. Algebra: daughter = s, Rogelio = 3s; 3s + 5 = 2(s + 5) gives s = 5, so Rogelio = 15.
SHORTCUT Try the choices. If Rogelio is 15, the daughter is 5. In 5 years: 20 and 10. 20 = 2 × 10, so it works.

### 25 | CIVIO-NUM-WP-ALGEBRA-000026
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Aileen is 4 times as old as her nephew. In 10 years, Aileen will be twice as old as the nephew. How old is Aileen now?
A. 15
B. 20
C. 30
D. 5
MARKED ANSWER B. 20
WHY 20 is right. Algebra: nephew = s, Aileen = 4s; 4s + 10 = 2(s + 10) gives s = 5, so Aileen = 20.
SHORTCUT Try the choices. If Aileen is 20, the nephew is 5. In 10 years: 30 and 15. 30 = 2 × 15, so it works.

### 26 | CIVIO-NUM-WP-GEOM-000027
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A rectangular vegetable garden is 16 m long and 6 m wide. A fence costs ₱50 per meter. How much will it cost to put the fence around the whole vegetable garden?
A. ₱2,200
B. ₱4,800
C. ₱1,100
D. ₱44
MARKED ANSWER A. ₱2,200
WHY ₱2,200 is right: 44 m × ₱50 = ₱2,200.
SHORTCUT Around = 2 × (16 + 6) = 44 m. Cost = 44 × ₱50.

### 27 | CIVIO-NUM-WP-RATE-000028
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Ramon can wash the ambulance fleet in 8 hours. Bong can do the same job in 24 hours. Working together, how long will they take?
A. 32 hours
B. 10 minutes
C. 6 hours
D. 16 hours
MARKED ANSWER C. 6 hours
WHY 6 hours is right. Check: in 6 hours, Ramon does 6/8 and Bong does 6/24; together that is 1 whole job.
SHORTCUT Per hour, Ramon does 1/8 and Bong does 1/24. Together: 1/8 + 1/24 = 1/6. So the whole job takes 6 hours.

### 28 | CIVIO-NUM-WP-PCT-CHANGE-000029
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A vendor borrows ₱10,000 at 10% simple interest per year. How much interest is due after 4 years and 6 months?
A. ₱4,600
B. ₱4,000
C. ₱14,500
D. ₱4,500
MARKED ANSWER D. ₱4,500
WHY ₱4,500 is right. Check: 10,000 × 0.1 × 4.5 = 4,500.
SHORTCUT Find one year first: 10% of ₱10,000 = ₱1,000. Time is 4.5 years. Multiply: 4.5 × ₱1,000 = ₱4,500.

### 29 | CIVIO-NUM-WP-PCT-CHANGE-000030
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A pair of school shoes is priced at ₱480. It is sold at 15% off. How much does a buyer pay?
A. ₱408
B. ₱465
C. ₱72
D. ₱552
MARKED ANSWER A. ₱408
WHY ₱408 is right. Check: discount ₱72; ₱480 − ₱72 = ₱408.
SHORTCUT Pay 85% of the price: ₱480 × 0.85 = ₱408.

### 30 | CIVIO-NUM-OPS-ORDER-000031
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What is the value of 4 + 2 × 4 − 10?
A. 2
B. -8
C. 0
D. 14
MARKED ANSWER A. 2
WHY 2 is right: 4 + 8 = 12, and 12 − 10 = 2.
SHORTCUT Circle the × first: 2 × 4 = 8. Then go left to right: 4 + 8 − 10.

### 31 | CIVIO-NUM-WP-AVERAGE-000032
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
The average age of the 4 clerks in the engineering office is 22 years. One more person, with 32 years, joins them. What is the new average age?
A. 24 years
B. 24.5 years
C. 120 years
D. 27 years
MARKED ANSWER A. 24 years
WHY 24 years is right. Long way: 4 × 22 = 88; + 32 = 120; ÷ 5 = 24.
SHORTCUT The new person is 32 − 22 = 10 above the old average. Share that among all 5 people: 10 ÷ 5 = 2. Add it: 22 + 2 = 24.

### 32 | CIVIO-NUM-WP-PCT-CHANGE-000033
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A government employee borrows ₱50,000 at 12% simple interest per year. How much interest is due after 3 years and 6 months?
A. ₱71,000
B. ₱18,000
C. ₱21,000
D. ₱21,600
MARKED ANSWER C. ₱21,000
WHY ₱21,000 is right. Check: 50,000 × 0.12 × 3.5 = 21,000.
SHORTCUT Find one year first: 12% of ₱50,000 = ₱6,000. Time is 3.5 years. Multiply: 3.5 × ₱6,000 = ₱21,000.

### 33 | CIVIO-NUM-FRAC-DEC-000034
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A barangay had 600 liters of fuel. It gave out 1/5 of them on Monday and 3/4 of the remaining liters of fuel on Tuesday. How many are left?
A. 360
B. 120
C. 480
D. 30
MARKED ANSWER B. 120
WHY 120 is right. Check: 120 + 360 + 120 = 600.
SHORTCUT Go day by day. Monday: 1/5 of 600 = 120, so 480 left. Tuesday: 3/4 of 480 = 360, so 480 − 360 = 120 left.

### 34 | CIVIO-NUM-SEQ-MULT-000035
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What number comes next?  2, 6, 14, 30, 62, ___
A. 124
B. 94
C. 128
D. 126
MARKED ANSWER D. 126
WHY 126 is right: 62 × 2 = 124, then + 2 gives 126.
SHORTCUT Test "times 2, then + 2" on the first numbers: 2 × 2 + 2 = 6; 6 × 2 + 2 = 14. It works, so use it on 62.

### 35 | CIVIO-NUM-WP-PCT-CHANGE-000036
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A backpack is priced at ₱400. It is sold at 15% off. How much does a buyer pay?
A. ₱340
B. ₱60
C. ₱385
D. ₱460
MARKED ANSWER A. ₱340
WHY ₱340 is right. Check: discount ₱60; ₱400 − ₱60 = ₱340.
SHORTCUT Pay 85% of the price: ₱400 × 0.85 = ₱340.

### 36 | CIVIO-NUM-WP-AVERAGE-000037
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
The average years of service of the 4 barangay health workers in the district hospital is 9 years. One more person, with 19 years, joins them. What is the new average years of service?
A. 11 years
B. 14 years
C. 55 years
D. 11.5 years
MARKED ANSWER A. 11 years
WHY 11 years is right. Long way: 4 × 9 = 36; + 19 = 55; ÷ 5 = 11.
SHORTCUT The new person is 19 − 9 = 10 above the old average. Share that among all 5 people: 10 ÷ 5 = 2. Add it: 9 + 2 = 11.

### 37 | CIVIO-NUM-WP-PCT-CHANGE-000038
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A hardware store sold a gallon of paint for ₱800. It raised the price by 30%. Later, it lowered the new price by 50%. What is the final price?
A. ₱640
B. ₱676
C. ₱1,040
D. ₱520
MARKED ANSWER D. ₱520
WHY ₱520 is right. Check: 800 × 1.3 = 1,040, and 1,040 × 0.5 = 520.
SHORTCUT Do one change at a time. ₱800 up 30% is ₱800 + ₱240 = ₱1,040. Then 50% of ₱1,040 is ₱520, so ₱1,040 − ₱520 = ₱520.

### 38 | CIVIO-NUM-OPS-ORDER-000039
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What is the value of 4 + 8 × 2 − 5?
A. 9
B. 15
C. -20
D. 19
MARKED ANSWER B. 15
WHY 15 is right: 4 + 16 = 20, and 20 − 5 = 15.
SHORTCUT Circle the × first: 8 × 2 = 16. Then go left to right: 4 + 16 − 5.

### 39 | CIVIO-NUM-WP-RATIO-000040
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Aileen and Efren will share ₱21,000 of commission in the ratio 3 : 4. How much is Efren's share?
A. ₱5,250
B. ₱12,000
C. ₱9,000
D. ₱3,000
MARKED ANSWER B. ₱12,000
WHY ₱12,000 is right: 4 × ₱3,000 = ₱12,000. Check: ₱9,000 + ₱12,000 = ₱21,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 4 = 7. One part = ₱21,000 ÷ 7 = ₱3,000. Then multiply by the parts you need.

### 40 | CIVIO-NUM-OPS-ORDER-000041
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What is the value of 9 + 4 × 3 − 1?
A. 20
B. 15
C. 17
D. 38
MARKED ANSWER A. 20
WHY 20 is right: 9 + 12 = 21, and 21 − 1 = 20.
SHORTCUT Circle the × first: 4 × 3 = 12. Then go left to right: 9 + 12 − 1.

### 41 | CIVIO-NUM-WP-RATE-000042
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Ramon can encode a box of survey forms in 6 hours. Arnel can do the same job in 3 hours. Working together, how long will they take?
A. 9 hours
B. 2 hours
C. 30 minutes
D. 4.5 hours
MARKED ANSWER B. 2 hours
WHY 2 hours is right. Check: in 2 hours, Ramon does 2/6 and Arnel does 2/3; together that is 1 whole job.
SHORTCUT Per hour, Ramon does 1/6 and Arnel does 1/3. Together: 1/6 + 1/3 = 1/2. So the whole job takes 2 hours.

### 42 | CIVIO-NUM-WP-GEOM-000043
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A rectangular school lot is 30 m long and 6 m wide. A chain-link fence costs ₱40 per meter. How much will it cost to put the chain-link fence around the whole school lot?
A. ₱1,440
B. ₱72
C. ₱2,880
D. ₱7,200
MARKED ANSWER C. ₱2,880
WHY ₱2,880 is right: 72 m × ₱40 = ₱2,880.
SHORTCUT Around = 2 × (30 + 6) = 72 m. Cost = 72 × ₱40.

### 43 | CIVIO-NUM-SEQ-DIFF-000044
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which number should come next?  4, 8, 15, 25, 38, ___
A. 42
B. 54
C. 57
D. 51
MARKED ANSWER B. 54
WHY 54 is right: 38 + 16 = 54.
SHORTCUT Write the jumps under the list: +4, +7, +10, +13. Each jump is 3 more than the one before. So the next jump is +16.

### 44 | CIVIO-NUM-WP-PCT-CHANGE-000045
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A cooperative store sold a tank of LPG for ₱150. It raised the price by 50%. Later, it lowered the new price by 20%. What is the final price?
A. ₱225
B. ₱270
C. ₱195
D. ₱180
MARKED ANSWER D. ₱180
WHY ₱180 is right. Check: 150 × 1.5 = 225, and 225 × 0.8 = 180.
SHORTCUT Do one change at a time. ₱150 up 50% is ₱150 + ₱75 = ₱225. Then 20% of ₱225 is ₱45, so ₱225 − ₱45 = ₱180.

### 45 | CIVIO-NUM-FRAC-DEC-000046
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
A barangay had 900 face masks. It gave out 2/5 of them on Monday and 1/3 of the remaining face masks on Tuesday. How many are left?
A. 180
B. 360
C. 540
D. 240
MARKED ANSWER B. 360
WHY 360 is right. Check: 360 + 180 + 360 = 900.
SHORTCUT Go day by day. Monday: 2/5 of 900 = 360, so 540 left. Tuesday: 1/3 of 540 = 180, so 540 − 180 = 360 left.

### 46 | CIVIO-ANA-CONCLUSION-000047
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Four staff members are compared. Aling Rosa lives nearer the office than Teresa. Kimberly lives nearer the office than Aling Rosa. Jun-jun lives nearer the office than Kimberly. Who is second in the order (counting from the one who lives nearest)?
A. Kimberly
B. Jun-jun
C. Teresa
D. Aling Rosa
MARKED ANSWER A. Kimberly
WHY Kimberly is right. The clues give Jun-jun → Kimberly → Aling Rosa → Teresa, so Kimberly is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Jun-jun → Kimberly → Aling Rosa → Teresa.

### 47 | CIVIO-ANA-CONCLUSION-000048
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Four staff members are compared. Cora scored higher than Inday. Ramon scored higher than Cora. Joy scored higher than Ramon. Who is second in the order (counting from the one who got the highest score)?
A. Ramon
B. Cora
C. Joy
D. Inday
MARKED ANSWER A. Ramon
WHY Ramon is right. The clues give Joy → Ramon → Cora → Inday, so Ramon is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Joy → Ramon → Cora → Inday.

### 48 | CIVIO-ANA-ANALOGY-SYN-000049
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
EXPAND : SHRINK :: ____
A. expense : spend
B. rise : fall
C. grow : increase
D. balloon : air
MARKED ANSWER B. rise : fall
WHY "rise : fall" is right. It has the same link, opposite meaning, in the same order.
SHORTCUT Make a sentence for the stem: "expand is to shrink" as opposite meaning. Test each choice in that sentence.

### 49 | CIVIO-ANA-SYMBOL-SERIES-000050
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What comes next in the series?  EO, GP, IQ, KR, ___
A. MW
B. LS
C. MS
D. SM
MARKED ANSWER C. MS
WHY MS is right: K + 2 = M and R + 1 = S.
SHORTCUT Split each pair. First letters: E, G, I, K (jump +2). Second letters: O, P, Q, R (jump +1). Move each one more step.

### 50 | CIVIO-ANA-CONCLUSION-000051
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Four staff members are compared. Lourdes arrived earlier than Jun-jun. Inday arrived earlier than Lourdes. Bea arrived earlier than Inday. Who is second in the order (counting from the one who arrived first)?
A. Jun-jun
B. Lourdes
C. Bea
D. Inday
MARKED ANSWER D. Inday
WHY Inday is right. The clues give Bea → Inday → Lourdes → Jun-jun, so Inday is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Bea → Inday → Lourdes → Jun-jun.

### 51 | CIVIO-ANA-CONCLUSION-000052
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Four staff members are compared. Teresa arrived earlier than Carlo. Jomar arrived earlier than Analyn. Analyn arrived earlier than Teresa. Who is third in the order (counting from the one who arrived first)?
A. Teresa
B. Jomar
C. Analyn
D. Carlo
MARKED ANSWER A. Teresa
WHY Teresa is right. The clues give Jomar → Analyn → Teresa → Carlo, so Teresa is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Jomar → Analyn → Teresa → Carlo.

### 52 | CIVIO-ANA-SYLLOGISM-000053
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Statement 1: Some mangoes are rentals. Statement 2: All mangoes are fruits. Which conclusion follows from both statements?
A. No fruits are rentals.
B. Some fruits are rentals.
C. All fruits are rentals.
D. All rentals are mangoes.
MARKED ANSWER B. Some fruits are rentals.
WHY "Some fruits are rentals." is right. It follows from the two statements with no extra facts.
SHORTCUT The mangoes who are rentals are also fruits. So at least some fruits are rentals.

### 53 | CIVIO-ANA-SYLLOGISM-000054
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
All typhoon reports are bulletins. No bulletins are stolen goods. Which conclusion must be true?
A. Some typhoon reports are stolen goods.
B. No public notices are stolen goods.
C. All bulletins are typhoon reports.
D. No typhoon reports are stolen goods.
MARKED ANSWER D. No typhoon reports are stolen goods.
WHY "No typhoon reports are stolen goods." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the typhoon reports circle inside bulletins. The "stolen goods" circle sits outside bulletins, so it is outside typhoon reports too.

### 54 | CIVIO-ANA-SYMBOL-SERIES-000055
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In a certain code, NOTICE is written as QRWLFH. How is PUBLIC written in the same code?
A. MRYIFZ
B. SXEOLC
C. TYFPMG
D. SXEOLF
MARKED ANSWER D. SXEOLF
WHY SXEOLF is right: each letter of PUBLIC moved 3 places forward.
SHORTCUT Compare the first letters: N became Q. That is 3 places forward. Check one more letter, then shift every letter of PUBLIC the same way.

### 55 | CIVIO-ANA-SYMBOL-SERIES-000056
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What comes next in the series?  CR, GS, KT, OU, ___
A. SV
B. SH
C. VS
D. PV
MARKED ANSWER A. SV
WHY SV is right: O + 4 = S and U + 1 = V.
SHORTCUT Split each pair. First letters: C, G, K, O (jump +4). Second letters: R, S, T, U (jump +1). Move each one more step.

### 56 | CIVIO-ANA-ANALOGY-FUNCTION-000057
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
TEACHER : SCHOOL :: ____
A. hospital : nurse
B. classroom : chalk
C. student : teacher
D. farmer : field
MARKED ANSWER D. farmer : field
WHY "farmer : field" is right. It has the same link, worker : workplace, in the same order.
SHORTCUT Make a sentence for the stem: "teacher is to school" as worker : workplace. Test each choice in that sentence.

### 57 | CIVIO-ANA-ASSUME-I-II-000058
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Statement: The office will print forms in both English and Filipino so every visitor can fill them out.
Assumption I: Some visitors read Filipino more easily than English.
Assumption II: Some visitors read English more easily than Filipino.
Which assumption is implicit in the statement?
A. Only II
B. Both I and II
C. Neither I nor II
D. Only I
MARKED ANSWER B. Both I and II
WHY "Both I and II" is right. Both assumptions are needed for the plan to make sense.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 58 | CIVIO-ANA-SYMBOL-SERIES-000059
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In a certain code, BRIDGE is written as EULGJH. How is NOTICE written in the same code?
A. QRWLFE
B. KLQFZB
C. QRWLFH
D. RSXMGI
MARKED ANSWER C. QRWLFH
WHY QRWLFH is right: each letter of NOTICE moved 3 places forward.
SHORTCUT Compare the first letters: B became E. That is 3 places forward. Check one more letter, then shift every letter of NOTICE the same way.

### 59 | CIVIO-ANA-ANALOGY-FUNCTION-000060
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Broom is to sweep as ____.
A. scissors : cut
B. sweep : broom
C. brush : bristle
D. dust : floor
MARKED ANSWER A. scissors : cut
WHY "scissors : cut" is right. It has the same link, tool : what it is used for, in the same order.
SHORTCUT Make a sentence for the stem: "broom is to sweep" as tool : what it is used for. Test each choice in that sentence.

### 60 | CIVIO-ANA-ANALOGY-FUNCTION-000061
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which pair shows the same relationship as "cashier : money"?
A. receipt : cashier
B. salary : work
C. librarian : books
D. bank : vault
MARKED ANSWER C. librarian : books
WHY "librarian : books" is right. It has the same link, worker : what they handle, in the same order.
SHORTCUT Make a sentence for the stem: "cashier is to money" as worker : what they handle. Test each choice in that sentence.

### 61 | CIVIO-ANA-SYMBOL-SERIES-000062
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What comes next in the series?  AN, EP, IR, MT, ___
A. NV
B. QD
C. VQ
D. QV
MARKED ANSWER D. QV
WHY QV is right: M + 4 = Q and T + 2 = V.
SHORTCUT Split each pair. First letters: A, E, I, M (jump +4). Second letters: N, P, R, T (jump +2). Move each one more step.

### 62 | CIVIO-ANA-ASSUME-I-II-000063
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Statement: The guard keeps a logbook of visitors to the records room.
Assumption I: Knowing who entered the records room is useful.
Assumption II: Records can be needed later, so who handled them matters.
Which assumption is implicit in the statement?
A. Both I and II
B. Only I
C. Only II
D. Neither I nor II
MARKED ANSWER A. Both I and II
WHY "Both I and II" is right. Both assumptions are needed for the plan to make sense.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 63 | CIVIO-ANA-DI-TABLE-000064
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Supply use of toner (units) by office (Cashier: Jul 58, Aug 24, Sep 14; HR: Jul 38, Aug 58, Sep 48; Engineering: Jul 52, Aug 48, Sep 76). In Sep, how many more did Engineering use than HR?
A. 124
B. 32
C. 14
D. 28
MARKED ANSWER D. 28
WHY 28 is right: 76 − 48 = 28.
SHORTCUT Go to the Sep column: Engineering 76, HR 48. Subtract the smaller from the larger.

### 64 | CIVIO-ANA-SYMBOL-SERIES-000065
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In a certain code, RECORD is written as UHFRUG. How is PERMIT written in the same code?
A. SHUPLW
B. TIVQMX
C. MBOJFQ
D. SHUPLT
MARKED ANSWER A. SHUPLW
WHY SHUPLW is right: each letter of PERMIT moved 3 places forward.
SHORTCUT Compare the first letters: R became U. That is 3 places forward. Check one more letter, then shift every letter of PERMIT the same way.

### 65 | CIVIO-ANA-DI-TABLE-000066
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Supply use of staplers by office (Planning: Jul 64, Aug 18, Sep 46; Library: Jul 26, Aug 74, Sep 74; HR: Jul 10, Aug 60, Sep 64). How many did Planning use in all three months?
A. 82
B. 128
C. 42.7
D. 152
MARKED ANSWER B. 128
WHY 128 is right: 64 + 18 + 46 = 128.
SHORTCUT Read across the Planning row only: 64 + 18 + 46.

### 66 | CIVIO-ANA-DI-TABLE-000067
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Supply use of toner (units) by office (HR: Jan 48, Feb 44, Mar 40; Cashier: Jan 48, Feb 28, Mar 78; Assessor: Jan 50, Feb 38, Mar 52). How many did HR use in all three months?
A. 92
B. 110
C. 44
D. 132
MARKED ANSWER D. 132
WHY 132 is right: 48 + 44 + 40 = 132.
SHORTCUT Read across the HR row only: 48 + 44 + 40.

### 67 | CIVIO-ANA-SYMBOL-SERIES-000068
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What comes next in the series?  HP, KR, NT, QV, ___
A. XT
B. TX
C. TB
D. RX
MARKED ANSWER B. TX
WHY TX is right: Q + 3 = T and V + 2 = X.
SHORTCUT Split each pair. First letters: H, K, N, Q (jump +3). Second letters: P, R, T, V (jump +2). Move each one more step.

### 68 | CIVIO-VEN-ERROR-AGREE-000069
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the word that best completes the sentence: The schedule of the trainings ____ posted on the bulletin board.
A. be
B. being
C. are
D. is
MARKED ANSWER D. is
WHY "is" is right: "The schedule" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The schedule ____". The subject is singular, so use the singular verb.

### 69 | CIVIO-VEN-SENT-COMP-PHRASAL-000070
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the phrase that best completes the sentence: We ran ____ of bond paper this morning.
A. over
B. into
C. out
D. off
MARKED ANSWER C. out
WHY "out" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 70 | CIVIO-VEN-SENT-COMP-WORD-000071
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the word that best completes the sentence: She has worked in the office ____ 2018.
A. during
B. for
C. from
D. since
MARKED ANSWER D. since
WHY "since" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 71 | CIVIO-VEN-RC-VOCAB-000072
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The team reached a FAIR decision after a long meeting.
A. just
B. biased
C. light-colored
D. trade show
MARKED ANSWER A. just
WHY "just" is right: it is the sense of "fair" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "fair".

### 72 | CIVIO-VEN-SENT-COMP-PHRASAL-000073
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the phrase that best completes the sentence: The old printer finally ____ after ten years.
A. broke up
B. broke down
C. broke out
D. broke in
MARKED ANSWER B. broke down
WHY "broke down" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 73 | CIVIO-VEN-SENT-COMP-WORD-000074
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the word that best completes the sentence: The committee voted to ____ the new proposal.
A. accepts
B. accept
C. except
D. access
MARKED ANSWER B. accept
WHY "accept" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 74 | CIVIO-VEN-ERROR-TENSE-000075
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the correct verb: Two days ago, the engineering office staff ____ the voters' list.
A. has updated
B. will have updated
C. will update
D. updated
MARKED ANSWER D. updated
WHY "updated" is right: the simple past matches "Two days ago".
SHORTCUT Find the time signal first: "Two days ago". It calls for the simple past.

### 75 | CIVIO-VEN-ERROR-AGREE-000076
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the word that best completes the sentence: A stack of folders ____ left in the conference room.
A. were
B. being
C. been
D. was
MARKED ANSWER D. was
WHY "was" is right: "A stack" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "A stack ____". The subject is singular, so use the singular verb.

### 76 | CIVIO-VEN-SENT-COMP-WORD-000077
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the word that best completes the sentence: All staff must arrive ____ the venue before 8 a.m.
A. at
B. into
C. on
D. to
MARKED ANSWER A. at
WHY "at" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 77 | CIVIO-VEN-WORD-MEANING-000078
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is closest in meaning to the word in capital letters?  ABUNDANT
A. plentiful
B. redundant
C. abandoned
D. scarce
MARKED ANSWER A. plentiful
WHY "plentiful" is right. "Abundant" means plentiful.
SHORTCUT Make a short sentence with "abundant", then swap in each choice. Watch for words that only look or sound like "abundant".

### 78 | CIVIO-VEN-WORD-MEANING-000079
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What does the phrase in capital letters mean?  The treasurer is TIGHTENING THE BELT this quarter.
A. spending less
B. losing weight
C. spending nothing at all
D. spending more
MARKED ANSWER A. spending less
WHY "spending less" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 79 | CIVIO-VEN-RC-VOCAB-000080
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The mayor will ADDRESS the flooding problem at the next session.
A. ignore
B. dress up
C. deal with
D. live at
MARKED ANSWER C. deal with
WHY "deal with" is right: it is the sense of "address" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "address".

### 80 | CIVIO-VEN-WORD-MEANING-000081
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What does the phrase in capital letters mean?  We should not CRY OVER SPILLED MILK; let us redo the forms.
A. regret what cannot be changed
B. clean the pantry
C. punish the one who erred
D. celebrate a mistake
MARKED ANSWER A. regret what cannot be changed
WHY "regret what cannot be changed" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 81 | CIVIO-VEN-ERROR-AGREE-000082
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the word that best completes the sentence: The price of school supplies ____ every June.
A. to rise
B. rise
C. rises
D. rising
MARKED ANSWER C. rises
WHY "rises" is right: "The price" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The price ____". The subject is singular, so use the singular verb.

### 82 | CIVIO-VEN-ERROR-TENSE-000083
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the correct verb: Yesterday, Rhea ____ the relief goods.
A. will deliver
B. has delivered
C. will have delivered
D. delivered
MARKED ANSWER D. delivered
WHY "delivered" is right: the simple past matches "Yesterday".
SHORTCUT Find the time signal first: "Yesterday". It calls for the simple past.

### 83 | CIVIO-VEN-WORD-MEANING-000084
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is closest in meaning to the word in capital letters?  PRUDENT
A. reckless
B. prominent
C. careful
D. prude
MARKED ANSWER C. careful
WHY "careful" is right. "Prudent" means careful.
SHORTCUT Make a short sentence with "prudent", then swap in each choice. Watch for words that only look or sound like "prudent".

### 84 | CIVIO-VEN-ERROR-TENSE-000085
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the correct verb: Right now, Ramon ____ the plaza.
A. cleaned
B. will have cleaned
C. is cleaning
D. cleans
MARKED ANSWER C. is cleaning
WHY "is cleaning" is right: the present progressive matches "Right now".
SHORTCUT Find the time signal first: "Right now". It calls for the present progressive.

### 85 | CIVIO-VEN-WORD-MEANING-000086
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  TEDIOUS
A. timid
B. tidy
C. boring
D. exciting
MARKED ANSWER D. exciting
WHY "exciting" is right. "Tedious" means boring; "exciting" is the reverse.
SHORTCUT First say what "tedious" means (boring). Then look for the word that means the reverse.

### 86 | CIVIO-VEN-ERROR-TENSE-000087
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Choose the correct verb: By next week, the city treasurer's office staff ____ the health center.
A. will have visited
B. is visiting
C. visited
D. has visited
MARKED ANSWER A. will have visited
WHY "will have visited" is right: the future perfect matches "By next week".
SHORTCUT Find the time signal first: "By next week". It calls for the future perfect.

### 87 | CIVIO-CLR-SPELL-RIGHT-000088
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is spelled correctly?  millennium | milennium | millennum | millnnium
A. millennium
B. milennium
C. millennum
D. millnnium
MARKED ANSWER A. millennium
WHY "millennium" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 88 | CIVIO-CLR-SPELL-WRONG-000089
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  definittely | beginning | recommend | receipt
A. definittely
B. beginning
C. recommend
D. receipt
MARKED ANSWER A. definittely
WHY "definittely" is misspelled: it doubles or undoubles a consonant. The correct spelling is "definitely".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 89 | CIVIO-CLR-SPELL-WRONG-000090
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  millnnium | cemetery | dilemma | jewelry
A. millnnium
B. cemetery
C. dilemma
D. jewelry
MARKED ANSWER A. millnnium
WHY "millnnium" is misspelled: it drops a letter. The correct spelling is "millennium".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 90 | CIVIO-CLR-FILE-POSITION-000091
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In alphabetical filing, which name is filed FIRST?  Andres M. Del Mundo | Ernesto D. Flores | Atty. Benito R. Delos Reyes | Danilo T. Leon
A. Ernesto D. Flores
B. Atty. Benito R. Delos Reyes
C. Andres M. Del Mundo
D. Danilo T. Leon
MARKED ANSWER C. Andres M. Del Mundo
WHY "Andres M. Del Mundo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Andres M. Del Mundo → DELMUNDO, Andres; Atty. Benito R. Delos Reyes → DELOSREYES, Benito; Ernesto D. Flores → FLORES, Ernesto; Danilo T. Leon → LEON, Danilo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 91 | CIVIO-CLR-SPELL-WRONG-000092
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  parliamnt | transferred | schedule | surveillance
A. parliamnt
B. transferred
C. schedule
D. surveillance
MARKED ANSWER A. parliamnt
WHY "parliamnt" is misspelled: it drops a letter. The correct spelling is "parliament".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 92 | CIVIO-CLR-SPELL-WRONG-000093
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  colleague | conscientious | convenience | personel
A. colleague
B. conscientious
C. convenience
D. personel
MARKED ANSWER D. personel
WHY "personel" is misspelled: it doubles or undoubles a consonant. The correct spelling is "personnel".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 93 | CIVIO-CLR-SPELL-WRONG-000094
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  embarrass | acquaintence | inoculate | maintenance
A. embarrass
B. acquaintence
C. inoculate
D. maintenance
MARKED ANSWER B. acquaintence
WHY "acquaintence" is misspelled: it is spelled the way the word sounds. The correct spelling is "acquaintance".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 94 | CIVIO-CLR-FILE-POSITION-000095
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In alphabetical filing, which name is filed LAST?  Ernesto C. Santos | Engr. Benito B. Leon | Ana B. Jose | Engr. Liza L. Reyes
A. Ernesto C. Santos
B. Engr. Liza L. Reyes
C. Ana B. Jose
D. Engr. Benito B. Leon
MARKED ANSWER A. Ernesto C. Santos
WHY "Ernesto C. Santos" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Ana B. Jose → JOSE, Ana; Engr. Benito B. Leon → LEON, Benito; Engr. Liza L. Reyes → REYES, Liza; Ernesto C. Santos → SANTOS, Ernesto.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 95 | CIVIO-CLR-SPELL-WRONG-000096
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  separate | liison | rhythm | exaggerate
A. separate
B. liison
C. rhythm
D. exaggerate
MARKED ANSWER B. liison
WHY "liison" is misspelled: it drops a letter. The correct spelling is "liaison".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 96 | CIVIO-CLR-FILE-POSITION-000097
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In alphabetical filing, which name is filed LAST?  Juan A. Pascual | Imelda S. Dela Cruz | Atty. Corazon A. Garcia | Dr. Benito A. Del Rosario
A. Dr. Benito A. Del Rosario
B. Atty. Corazon A. Garcia
C. Juan A. Pascual
D. Imelda S. Dela Cruz
MARKED ANSWER C. Juan A. Pascual
WHY "Juan A. Pascual" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Imelda S. Dela Cruz → DELACRUZ, Imelda; Dr. Benito A. Del Rosario → DELROSARIO, Benito; Atty. Corazon A. Garcia → GARCIA, Corazon; Juan A. Pascual → PASCUAL, Juan.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 97 | CIVIO-CLR-SPELL-WRONG-000098
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  separrate | exaggerate | bureaucracy | conscience
A. separrate
B. exaggerate
C. bureaucracy
D. conscience
MARKED ANSWER A. separrate
WHY "separrate" is misspelled: it doubles or undoubles a consonant. The correct spelling is "separate".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 98 | CIVIO-CLR-SPELL-WRONG-000099
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  miscellaneous | occasionally | existence | accessble
A. miscellaneous
B. occasionally
C. existence
D. accessble
MARKED ANSWER D. accessble
WHY "accessble" is misspelled: it drops a letter. The correct spelling is "accessible".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 99 | CIVIO-CLR-SPELL-WRONG-000100
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  license | noticeable | vacum | achievement
A. license
B. noticeable
C. vacum
D. achievement
MARKED ANSWER C. vacum
WHY "vacum" is misspelled: it drops a letter. The correct spelling is "vacuum".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 100 | CIVIO-CLR-SPELL-WRONG-000101
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Which word is misspelled?  requisition | phenomenon | pronnciation | definitely
A. requisition
B. phenomenon
C. pronnciation
D. definitely
MARKED ANSWER C. pronnciation
WHY "pronnciation" is misspelled: it drops a letter. The correct spelling is "pronunciation".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 101 | CIVIO-CLR-FILE-POSITION-000102
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
In alphabetical filing, which name is filed LAST?  Atty. Ramon B. San Juan | Juan D. Bautista | Rosario V. Flores | Engr. Nora V. Mendoza
A. Rosario V. Flores
B. Juan D. Bautista
C. Engr. Nora V. Mendoza
D. Atty. Ramon B. San Juan
MARKED ANSWER D. Atty. Ramon B. San Juan
WHY "Atty. Ramon B. San Juan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Juan D. Bautista → BAUTISTA, Juan; Rosario V. Flores → FLORES, Rosario; Engr. Nora V. Mendoza → MENDOZA, Nora; Atty. Ramon B. San Juan → SANJUAN, Ramon.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 102 | CIVIO-GI-DEADLINE-NUMBER-000103
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
How many years must a person have lived in the Philippines immediately before the election to be President?
A. 15 years
B. 2 years
C. 10 years
D. 5 years
MARKED ANSWER C. 10 years
WHY "10 years" is right. Art. VII, Sec. 2 says: "a resident of the Philippines for at least ten years immediately preceding such election".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 2. Ten years of residence is required.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 103 | CIVIO-GI-DEADLINE-NUMBER-000104
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Under the 1987 Constitution, a proclamation of martial law may not last longer than how many days without extension by Congress?
A. 15 days
B. 30 days
C. 90 days
D. 60 days
MARKED ANSWER D. 60 days
WHY "60 days" is right. Art. VII, Sec. 18 says: "for a period not exceeding sixty days".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 18. Martial law is limited to 60 days unless Congress extends it.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 104 | CIVIO-GI-DEADLINE-NUMBER-000105
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
How many Commissioners does the Civil Service Commission have, besides its Chairman?
A. Three
B. Six
C. Four
D. Two
MARKED ANSWER D. Two
WHY "Two" is right. Art. IX-B, Sec. 1(1) says: "composed of a Chairman and two Commissioners".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 1(1). The CSC has a Chairman and two Commissioners.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 105 | CIVIO-GI-DEADLINE-NUMBER-000106
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
How long is the term of office of a Senator under the 1987 Constitution?
A. 6 years
B. 4 years
C. 3 years
D. 9 years
MARKED ANSWER A. 6 years
WHY "6 years" is right. Art. VI, Sec. 4 says: "The term of office of the Senators shall be six years".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 4. Senators serve 6-year terms.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 106 | CIVIO-GI-WHO-HOLDS-POWER-000107
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What does the 1987 Constitution say about the death penalty?
A. It may be imposed by any court
B. It shall not be imposed, unless Congress provides for it for compelling reasons involving heinous crimes
C. It may be imposed by the President
D. It is required for all heinous crimes
MARKED ANSWER B. It shall not be imposed, unless Congress provides for it for compelling reasons involving heinous crimes
WHY "It shall not be imposed, unless Congress provides for it for compelling reasons involving heinous crimes" is right. Art. III, Sec. 19(1) says: "Neither shall death penalty be imposed, unless, for compelling reasons involving heinous crimes, the Congress hereafter provides for it".
SHORTCUT Tie the fact to its section: Art. III, Sec. 19(1). Default: no death penalty.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 107 | CIVIO-GI-DEADLINE-NUMBER-000108
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
How long is the term of a Member of the House of Representatives?
A. 6 years
B. 2 years
C. 4 years
D. 3 years
MARKED ANSWER D. 3 years
WHY "3 years" is right. Art. VI, Sec. 7 says: "shall be elected for a term of three years".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 7. House Members serve 3-year terms.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 108 | CIVIO-GI-DEADLINE-NUMBER-000109
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
Up to what age may members of the Supreme Court hold office?
A. 60 years
B. 75 years
C. 70 years
D. 65 years
MARKED ANSWER C. 70 years
WHY "70 years" is right. Art. VIII, Sec. 11 says: "until they reach the age of seventy years".
SHORTCUT Tie the fact to its section: Art. VIII, Sec. 11. Justices serve until age 70.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 109 | CIVIO-GI-TERM-MATCH-000110
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
What must a public officer submit under oath upon assuming office and as often as required by law?
A. A medical certificate
B. A declaration of assets, liabilities, and net worth
C. An income tax return only
D. A police clearance
MARKED ANSWER B. A declaration of assets, liabilities, and net worth
WHY "A declaration of assets, liabilities, and net worth" is right. Art. XI, Sec. 17 says: "submit a declaration under oath of his assets, liabilities, and net worth".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 17. This is the SALN.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 110 | CIVIO-GI-DEADLINE-NUMBER-000111
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-002.json
STEM
How long is the term of the Chairman of the Civil Service Commission?
A. 9 years, without reappointment
B. 5 years, without reappointment
C. 7 years, without reappointment
D. 6 years, with one reappointment
MARKED ANSWER C. 7 years, without reappointment
WHY "7 years, without reappointment" is right. Art. IX-B, Sec. 1(2) says: "for a term of seven years without reappointment".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 1(2). CSC Chairman: one 7-year term, no reappointment.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 111 | CIVIO-NUM-WP-RATE-000112
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Mang Jun can wash the ambulance fleet in 18 hours. Datu can do the same job in 9 hours. Working together, how long will they take?
A. 6 hours
B. 10 minutes
C. 13.5 hours
D. 27 hours
MARKED ANSWER A. 6 hours
WHY 6 hours is right. Check: in 6 hours, Mang Jun does 6/18 and Datu does 6/9; together that is 1 whole job.
SHORTCUT Per hour, Mang Jun does 1/18 and Datu does 1/9. Together: 1/18 + 1/9 = 1/6. So the whole job takes 6 hours.

### 112 | CIVIO-NUM-WP-PCT-CHANGE-000113
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A hardware store sold a tank of LPG for ₱240. It raised the price by 50%. Later, it lowered the new price by 50%. What is the final price?
A. ₱270
B. ₱240
C. ₱360
D. ₱180
MARKED ANSWER D. ₱180
WHY ₱180 is right. Check: 240 × 1.5 = 360, and 360 × 0.5 = 180.
SHORTCUT Do one change at a time. ₱240 up 50% is ₱240 + ₱120 = ₱360. Then 50% of ₱360 is ₱180, so ₱360 − ₱180 = ₱180.

### 113 | CIVIO-NUM-WP-AVERAGE-000114
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
The average years of service of the 8 drivers in the records section is 13 years. One more person, with 40 years, joins them. What is the new average years of service?
A. 144 years
B. 26.5 years
C. 16.38 years
D. 16 years
MARKED ANSWER D. 16 years
WHY 16 years is right. Long way: 8 × 13 = 104; + 40 = 144; ÷ 9 = 16.
SHORTCUT The new person is 40 − 13 = 27 above the old average. Share that among all 9 people: 27 ÷ 9 = 3. Add it: 13 + 3 = 16.

### 114 | CIVIO-NUM-WP-AVERAGE-000115
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
The average years of service of the 4 staff members in the public library is 14 years. One more person, with 24 years, joins them. What is the new average years of service?
A. 16.5 years
B. 80 years
C. 16 years
D. 19 years
MARKED ANSWER C. 16 years
WHY 16 years is right. Long way: 4 × 14 = 56; + 24 = 80; ÷ 5 = 16.
SHORTCUT The new person is 24 − 14 = 10 above the old average. Share that among all 5 people: 10 ÷ 5 = 2. Add it: 14 + 2 = 16.

### 115 | CIVIO-NUM-WP-RATE-000116
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Nestor can paint a classroom in 21 hours. Aling Rosa can do the same job in 28 hours. Working together, how long will they take?
A. 12 hours
B. 24.5 hours
C. 49 hours
D. 5 minutes
MARKED ANSWER A. 12 hours
WHY 12 hours is right. Check: in 12 hours, Nestor does 12/21 and Aling Rosa does 12/28; together that is 1 whole job.
SHORTCUT Per hour, Nestor does 1/21 and Aling Rosa does 1/28. Together: 1/21 + 1/28 = 1/12. So the whole job takes 12 hours.

### 116 | CIVIO-NUM-SEQ-DIFF-000117
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What number comes next in the series?  5, 7, 10, 14, 19, ___
A. 25
B. 24
C. 26
D. 21
MARKED ANSWER A. 25
WHY 25 is right: 19 + 6 = 25.
SHORTCUT Write the jumps under the list: +2, +3, +4, +5. Each jump is 1 more than the one before. So the next jump is +6.

### 117 | CIVIO-NUM-OPS-ORDER-000118
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What is the value of 3 + 3 × 7 − 2?
A. 40
B. 11
C. 22
D. 18
MARKED ANSWER C. 22
WHY 22 is right: 3 + 21 = 24, and 24 − 2 = 22.
SHORTCUT Circle the × first: 3 × 7 = 21. Then go left to right: 3 + 21 − 2.

### 118 | CIVIO-NUM-WP-PCT-CHANGE-000119
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A vendor borrows ₱12,000 at 12% simple interest per year. How much interest is due after 2 years and 6 months?
A. ₱15,600
B. ₱3,744
C. ₱2,880
D. ₱3,600
MARKED ANSWER D. ₱3,600
WHY ₱3,600 is right. Check: 12,000 × 0.12 × 2.5 = 3,600.
SHORTCUT Find one year first: 12% of ₱12,000 = ₱1,440. Time is 2.5 years. Multiply: 2.5 × ₱1,440 = ₱3,600.

### 119 | CIVIO-NUM-WP-RATE-000120
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Carlo can repack the relief goods in 45 hours. Joy can do the same job in 30 hours. Working together, how long will they take?
A. 75 hours
B. 37.5 hours
C. 18 hours
D. 3.3333 hours
MARKED ANSWER C. 18 hours
WHY 18 hours is right. Check: in 18 hours, Carlo does 18/45 and Joy does 18/30; together that is 1 whole job.
SHORTCUT Per hour, Carlo does 1/45 and Joy does 1/30. Together: 1/45 + 1/30 = 1/18. So the whole job takes 18 hours.

### 120 | CIVIO-NUM-WP-PCT-CHANGE-000121
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A backpack is priced at ₱2,400. It is sold at 25% off. How much does a buyer pay?
A. ₱3,000
B. ₱600
C. ₱1,800
D. ₱2,375
MARKED ANSWER C. ₱1,800
WHY ₱1,800 is right. Check: discount ₱600; ₱2,400 − ₱600 = ₱1,800.
SHORTCUT Pay 75% of the price: ₱2,400 × 0.75 = ₱1,800.

### 121 | CIVIO-NUM-SEQ-DIFF-000122
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which number should come next?  7, 11, 16, 22, 29, ___
A. 37
B. 36
C. 38
D. 33
MARKED ANSWER A. 37
WHY 37 is right: 29 + 8 = 37.
SHORTCUT Write the jumps under the list: +4, +5, +6, +7. Each jump is 1 more than the one before. So the next jump is +8.

### 122 | CIVIO-NUM-SEQ-DIFF-000123
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Find the next number in the series.  8, 14, 22, 32, 44, ___
A. 56
B. 58
C. 60
D. 50
MARKED ANSWER B. 58
WHY 58 is right: 44 + 14 = 58.
SHORTCUT Write the jumps under the list: +6, +8, +10, +12. Each jump is 2 more than the one before. So the next jump is +14.

### 123 | CIVIO-NUM-WP-PCT-CHANGE-000124
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A hardware store sold a gallon of paint for ₱250. It raised the price by 20%. Later, it lowered the new price by 25%. What is the final price?
A. ₱300
B. ₱270
C. ₱237.50
D. ₱225
MARKED ANSWER D. ₱225
WHY ₱225 is right. Check: 250 × 1.2 = 300, and 300 × 0.75 = 225.
SHORTCUT Do one change at a time. ₱250 up 20% is ₱250 + ₱50 = ₱300. Then 25% of ₱300 is ₱75, so ₱300 − ₱75 = ₱225.

### 124 | CIVIO-NUM-WP-RATIO-000125
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Ramon and Dindo will share ₱14,000 of commission in the ratio 2 : 5. How much is Dindo's share?
A. ₱10,000
B. ₱2,000
C. ₱2,800
D. ₱4,000
MARKED ANSWER A. ₱10,000
WHY ₱10,000 is right: 5 × ₱2,000 = ₱10,000. Check: ₱4,000 + ₱10,000 = ₱14,000.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 5 = 7. One part = ₱14,000 ÷ 7 = ₱2,000. Then multiply by the parts you need.

### 125 | CIVIO-NUM-WP-RATIO-000126
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Marites and Lourdes will share ₱5,000 of cleanup fund in the ratio 3 : 7. How much is Lourdes's share?
A. ₱714.29
B. ₱1,500
C. ₱500
D. ₱3,500
MARKED ANSWER D. ₱3,500
WHY ₱3,500 is right: 7 × ₱500 = ₱3,500. Check: ₱1,500 + ₱3,500 = ₱5,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱5,000 ÷ 10 = ₱500. Then multiply by the parts you need.

### 126 | CIVIO-NUM-WP-GEOM-000127
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A rectangular vegetable garden is 19 m long and 20 m wide. A chain-link fence costs ₱120 per meter. How much will it cost to put the chain-link fence around the whole vegetable garden?
A. ₱4,680
B. ₱45,600
C. ₱78
D. ₱9,360
MARKED ANSWER D. ₱9,360
WHY ₱9,360 is right: 78 m × ₱120 = ₱9,360.
SHORTCUT Around = 2 × (19 + 20) = 78 m. Cost = 78 × ₱120.

### 127 | CIVIO-NUM-WP-GEOM-000128
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A rectangular parking area is 31 m long and 9 m wide. A fence costs ₱120 per meter. How much will it cost to put the fence around the whole parking area?
A. ₱9,600
B. ₱80
C. ₱4,800
D. ₱33,480
MARKED ANSWER A. ₱9,600
WHY ₱9,600 is right: 80 m × ₱120 = ₱9,600.
SHORTCUT Around = 2 × (31 + 9) = 80 m. Cost = 80 × ₱120.

### 128 | CIVIO-NUM-SEQ-MULT-000129
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What number comes next?  2, 8, 26, 80, 242, ___
A. 728
B. 726
C. 730
D. 404
MARKED ANSWER A. 728
WHY 728 is right: 242 × 3 = 726, then + 2 gives 728.
SHORTCUT Test "times 3, then + 2" on the first numbers: 2 × 3 + 2 = 8; 8 × 3 + 2 = 26. It works, so use it on 242.

### 129 | CIVIO-NUM-WP-ALGEBRA-000130
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Nestor is 5 times as old as his daughter. In 15 years, Nestor will be three times as old as the daughter. How old is Nestor now?
A. 75
B. 90
C. 15
D. 30
MARKED ANSWER A. 75
WHY 75 is right. Algebra: daughter = s, Nestor = 5s; 5s + 15 = 3(s + 15) gives s = 15, so Nestor = 75.
SHORTCUT Try the choices. If Nestor is 75, the daughter is 15. In 15 years: 90 and 30. 90 = 3 × 30, so it works.

### 130 | CIVIO-NUM-OPS-ORDER-000131
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What is the value of 2 + 8 × 7 − 8?
A. 9
B. 50
C. 62
D. -6
MARKED ANSWER B. 50
WHY 50 is right: 2 + 56 = 58, and 58 − 8 = 50.
SHORTCUT Circle the × first: 8 × 7 = 56. Then go left to right: 2 + 56 − 8.

### 131 | CIVIO-NUM-WP-AVERAGE-000132
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
The average years of service of the 8 staff members in the records section is 13 years. One more person, with 49 years, joins them. What is the new average years of service?
A. 17.5 years
B. 31 years
C. 153 years
D. 17 years
MARKED ANSWER D. 17 years
WHY 17 years is right. Long way: 8 × 13 = 104; + 49 = 153; ÷ 9 = 17.
SHORTCUT The new person is 49 − 13 = 36 above the old average. Share that among all 9 people: 36 ÷ 9 = 4. Add it: 13 + 4 = 17.

### 132 | CIVIO-NUM-WP-PCT-CHANGE-000133
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A cooperative member borrows ₱12,000 at 3% simple interest per year. How much interest is due after 3 years?
A. ₱13,080
B. ₱360
C. ₱10,800
D. ₱1,080
MARKED ANSWER D. ₱1,080
WHY ₱1,080 is right. Check: 12,000 × 0.03 × 3 = 1,080.
SHORTCUT Find one year first: 3% of ₱12,000 = ₱360. Time is 3 years. Multiply: 3 × ₱360 = ₱1,080.

### 133 | CIVIO-NUM-WP-PCT-CHANGE-000134
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A farmer borrows ₱25,000 at 3% simple interest per year. How much interest is due after 3 years and 6 months?
A. ₱2,700
B. ₱27,625
C. ₱2,250
D. ₱2,625
MARKED ANSWER D. ₱2,625
WHY ₱2,625 is right. Check: 25,000 × 0.03 × 3.5 = 2,625.
SHORTCUT Find one year first: 3% of ₱25,000 = ₱750. Time is 3.5 years. Multiply: 3.5 × ₱750 = ₱2,625.

### 134 | CIVIO-NUM-OPS-ORDER-000135
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What is the value of 14 + 2 × 3 − 7?
A. 12
B. 6
C. 41
D. 13
MARKED ANSWER D. 13
WHY 13 is right: 14 + 6 = 20, and 20 − 7 = 13.
SHORTCUT Circle the × first: 2 × 3 = 6. Then go left to right: 14 + 6 − 7.

### 135 | CIVIO-NUM-WP-RATIO-000136
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A ₱7,500 allowance fund is divided between Liza and Kimberly in the ratio 2 : 3. What is Kimberly's share?
A. ₱2,500
B. ₱1,500
C. ₱3,000
D. ₱4,500
MARKED ANSWER D. ₱4,500
WHY ₱4,500 is right: 3 × ₱1,500 = ₱4,500. Check: ₱3,000 + ₱4,500 = ₱7,500.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 3 = 5. One part = ₱7,500 ÷ 5 = ₱1,500. Then multiply by the parts you need.

### 136 | CIVIO-NUM-SEQ-MULT-000137
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What number comes next?  3, 8, 23, 68, 203, ___
A. 607
B. 609
C. 608
D. 338
MARKED ANSWER C. 608
WHY 608 is right: 203 × 3 = 609, then − 1 gives 608.
SHORTCUT Test "times 3, then − 1" on the first numbers: 3 × 3 − 1 = 8; 8 × 3 − 1 = 23. It works, so use it on 203.

### 137 | CIVIO-NUM-SEQ-MULT-000138
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What number comes next?  6, 15, 33, 69, 141, ___
A. 282
B. 285
C. 288
D. 213
MARKED ANSWER B. 285
WHY 285 is right: 141 × 2 = 282, then + 3 gives 285.
SHORTCUT Test "times 2, then + 3" on the first numbers: 6 × 2 + 3 = 15; 15 × 2 + 3 = 33. It works, so use it on 141.

### 138 | CIVIO-NUM-WP-PCT-CHANGE-000139
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A backpack is priced at ₱2,400. It is sold at 35% off. How much does a buyer pay?
A. ₱2,365
B. ₱1,560
C. ₱3,240
D. ₱840
MARKED ANSWER B. ₱1,560
WHY ₱1,560 is right. Check: discount ₱840; ₱2,400 − ₱840 = ₱1,560.
SHORTCUT Pay 65% of the price: ₱2,400 × 0.65 = ₱1,560.

### 139 | CIVIO-NUM-FRAC-DEC-000140
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A barangay had 480 liters of fuel. It gave out 1/8 of them on Monday and 1/3 of the remaining liters of fuel on Tuesday. How many are left?
A. 260
B. 140
C. 280
D. 420
MARKED ANSWER C. 280
WHY 280 is right. Check: 60 + 140 + 280 = 480.
SHORTCUT Go day by day. Monday: 1/8 of 480 = 60, so 420 left. Tuesday: 1/3 of 420 = 140, so 420 − 140 = 280 left.

### 140 | CIVIO-NUM-FRAC-DEC-000141
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
A barangay had 840 liters of fuel. It gave out 1/3 of them on Monday and 1/4 of the remaining liters of fuel on Tuesday. How many are left?
A. 420
B. 140
C. 560
D. 350
MARKED ANSWER A. 420
WHY 420 is right. Check: 280 + 140 + 420 = 840.
SHORTCUT Go day by day. Monday: 1/3 of 840 = 280, so 560 left. Tuesday: 1/4 of 560 = 140, so 560 − 140 = 420 left.

### 141 | CIVIO-ANA-SYMBOL-SERIES-000142
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In a certain code, HEALTH is written as IFBMUI. How is PUBLIC written in the same code?
A. QVCMJC
B. RWDNKE
C. QVCMJD
D. OTAKHB
MARKED ANSWER C. QVCMJD
WHY QVCMJD is right: each letter of PUBLIC moved 1 place forward.
SHORTCUT Compare the first letters: H became I. That is 1 place forward. Check one more letter, then shift every letter of PUBLIC the same way.

### 142 | CIVIO-ANA-ANALOGY-SYN-000143
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Generous is to stingy as ____.
A. humble : proud
B. giver : giving
C. gift : money
D. kind : gentle
MARKED ANSWER A. humble : proud
WHY "humble : proud" is right. It has the same link, opposite meaning, in the same order.
SHORTCUT Make a sentence for the stem: "generous is to stingy" as opposite meaning. Test each choice in that sentence.

### 143 | CIVIO-ANA-SYLLOGISM-000144
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
All encoders are clerks. Some encoders are blood donors. Which conclusion must be true?
A. Some clerks are blood donors.
B. No clerks are blood donors.
C. All blood donors are encoders.
D. All clerks are blood donors.
MARKED ANSWER A. Some clerks are blood donors.
WHY "Some clerks are blood donors." is right. It follows from the two statements with no extra facts.
SHORTCUT The encoders who are blood donors are also clerks. So at least some clerks are blood donors.

### 144 | CIVIO-ANA-ANALOGY-FORM-000145
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Caterpillar is to butterfly as ____.
A. adult : child
B. tadpole : frog
C. bee : honey
D. wing : bird
MARKED ANSWER B. tadpole : frog
WHY "tadpole : frog" is right. It has the same link, early stage : later stage, in the same order.
SHORTCUT Make a sentence for the stem: "caterpillar is to butterfly" as early stage : later stage. Test each choice in that sentence.

### 145 | CIVIO-ANA-SYMBOL-SERIES-000146
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In a certain code, MARKET is written as NBSLFU. How is CENSUS written in the same code?
A. DFOTVS
B. EGPUWU
C. BDMRTR
D. DFOTVT
MARKED ANSWER D. DFOTVT
WHY DFOTVT is right: each letter of CENSUS moved 1 place forward.
SHORTCUT Compare the first letters: M became N. That is 1 place forward. Check one more letter, then shift every letter of CENSUS the same way.

### 146 | CIVIO-ANA-SYLLOGISM-000147
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Assume these are true: none of the public buildings are unregistered items, and every one of the libraries is among the public buildings. What can be concluded for certain?
A. No insured properties are unregistered items.
B. All public buildings are libraries.
C. Some libraries are unregistered items.
D. No libraries are unregistered items.
MARKED ANSWER D. No libraries are unregistered items.
WHY "No libraries are unregistered items." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the libraries circle inside public buildings. The "unregistered items" circle sits outside public buildings, so it is outside libraries too.

### 147 | CIVIO-ANA-SYLLOGISM-000148
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
All tricycles are motor vehicles. All motor vehicles are taxed vehicles. Which conclusion must be true?
A. Some taxed vehicles are not motor vehicles.
B. All taxed vehicles are tricycles.
C. All tricycles are taxed vehicles.
D. No motor vehicles are tricycles.
MARKED ANSWER C. All tricycles are taxed vehicles.
WHY "All tricycles are taxed vehicles." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: tricycles inside motor vehicles, motor vehicles inside taxed vehicles. So tricycles sit inside taxed vehicles.

### 148 | CIVIO-ANA-SYMBOL-SERIES-000149
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In a certain code, FARM is written as DYPK. How is MAYOR written in the same code?
A. JXVLO
B. KYWMR
C. OCAQT
D. KYWMP
MARKED ANSWER D. KYWMP
WHY KYWMP is right: each letter of MAYOR moved 2 places back.
SHORTCUT Compare the first letters: F became D. That is 2 places back. Check one more letter, then shift every letter of MAYOR the same way.

### 149 | CIVIO-ANA-ASSUME-I-II-000150
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Statement: The city hall added a second cashier window to cut the long lines on payday.
Assumption I: One more window can serve more people at the same time.
Assumption II: The cashiers on the first window are lazy.
Which assumption is implicit in the statement?
A. Neither I nor II
B. Only I
C. Both I and II
D. Only II
MARKED ANSWER B. Only I
WHY "Only I" is right. Only assumption I is needed. II ("The cashiers on the first window are lazy.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 150 | CIVIO-ANA-SYLLOGISM-000151
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Assume these are true: a few of the volunteers are scholars, and all of the volunteers are helpers. What can be concluded for certain?
A. All helpers are scholars.
B. All scholars are volunteers.
C. Some helpers are scholars.
D. No helpers are scholars.
MARKED ANSWER C. Some helpers are scholars.
WHY "Some helpers are scholars." is right. It follows from the two statements with no extra facts.
SHORTCUT The volunteers who are scholars are also helpers. So at least some helpers are scholars.

### 151 | CIVIO-ANA-ASSUME-I-II-000152
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Statement: The market will put up signs with prices to stop vendors from overcharging.
Assumption I: Buyers can see posted prices.
Assumption II: Some vendors have charged more than the fair price.
Which assumption is implicit in the statement?
A. Only II
B. Only I
C. Both I and II
D. Neither I nor II
MARKED ANSWER C. Both I and II
WHY "Both I and II" is right. Both assumptions are needed for the plan to make sense.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 152 | CIVIO-ANA-DI-TABLE-000153
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Supply use of bond paper (reams) by office (Assessor: Apr 68, May 44, Jun 52; Library: Apr 28, May 48, Jun 44; Records: Apr 24, May 46, Jun 12). How many did Assessor use in all three months?
A. 54.7
B. 138
C. 164
D. 112
MARKED ANSWER C. 164
WHY 164 is right: 68 + 44 + 52 = 164.
SHORTCUT Read across the Assessor row only: 68 + 44 + 52.

### 153 | CIVIO-ANA-SYLLOGISM-000154
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Statement 1: No health workers are job-order hires. Statement 2: All nurses are health workers. Which conclusion follows from both statements?
A. Some nurses are job-order hires.
B. No nurses are job-order hires.
C. No public servants are job-order hires.
D. All health workers are nurses.
MARKED ANSWER B. No nurses are job-order hires.
WHY "No nurses are job-order hires." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the nurses circle inside health workers. The "job-order hires" circle sits outside health workers, so it is outside nurses too.

### 154 | CIVIO-ANA-ANALOGY-SYN-000155
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which pair shows the same relationship as "timid : afraid"?
A. brave : afraid
B. happy : glad
C. shy : crowd
D. tame : lion
MARKED ANSWER B. happy : glad
WHY "happy : glad" is right. It has the same link, similar meaning, in the same order.
SHORTCUT Make a sentence for the stem: "timid is to afraid" as similar meaning. Test each choice in that sentence.

### 155 | CIVIO-ANA-ANALOGY-FORM-000156
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Find the pair whose link matches the link between "drought" and "rain".
A. darkness : light
B. light : darkness
C. flood : water
D. cloud : rain
MARKED ANSWER A. darkness : light
WHY "darkness : light" is right. It has the same link, condition : what it lacks, in the same order.
SHORTCUT Make a sentence for the stem: "drought is to rain" as condition : what it lacks. Test each choice in that sentence.

### 156 | CIVIO-ANA-CONCLUSION-000157
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Four staff members are compared. Mang Jun scored higher than Rhea. Rhea scored higher than Marites. Marites scored higher than Bea. Who is third in the order (counting from the one who got the highest score)?
A. Rhea
B. Marites
C. Bea
D. Mang Jun
MARKED ANSWER B. Marites
WHY Marites is right. The clues give Mang Jun → Rhea → Marites → Bea, so Marites is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Mang Jun → Rhea → Marites → Bea.

### 157 | CIVIO-ANA-SYMBOL-SERIES-000158
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In a certain code, MEMO is written as PHPR. How is CENSUS written in the same code?
A. FHQVXS
B. FHQVXV
C. GIRWYW
D. ZBKPRP
MARKED ANSWER B. FHQVXV
WHY FHQVXV is right: each letter of CENSUS moved 3 places forward.
SHORTCUT Compare the first letters: M became P. That is 3 places forward. Check one more letter, then shift every letter of CENSUS the same way.

### 158 | CIVIO-ANA-CONCLUSION-000159
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Four staff members are compared. Bong lives nearer the office than Arnel. Teresa lives nearer the office than Bong. Cora lives nearer the office than Teresa. Who is second in the order (counting from the one who lives nearest)?
A. Teresa
B. Bong
C. Arnel
D. Cora
MARKED ANSWER A. Teresa
WHY Teresa is right. The clues give Cora → Teresa → Bong → Arnel, so Teresa is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Cora → Teresa → Bong → Arnel.

### 159 | CIVIO-ANA-SYMBOL-SERIES-000160
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In a certain code, CENSUS is written as EGPUWU. How is AUDIT written in the same code?
A. YSBGR
B. CWFKT
C. DXGLW
D. CWFKV
MARKED ANSWER D. CWFKV
WHY CWFKV is right: each letter of AUDIT moved 2 places forward.
SHORTCUT Compare the first letters: C became E. That is 2 places forward. Check one more letter, then shift every letter of AUDIT the same way.

### 160 | CIVIO-ANA-CONCLUSION-000161
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Four staff members are compared. Tess finished the report earlier than Nonoy. Carlo finished the report earlier than Tess. Nonoy finished the report earlier than Nestor. Who is second in the order (counting from the one who finished first)?
A. Carlo
B. Nonoy
C. Tess
D. Nestor
MARKED ANSWER C. Tess
WHY Tess is right. The clues give Carlo → Tess → Nonoy → Nestor, so Tess is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Carlo → Tess → Nonoy → Nestor.

### 161 | CIVIO-ANA-CONCLUSION-000162
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Four staff members are compared. Liza has served longer than Bea. Carlo has served longer than Liza. Bea has served longer than Nestor. Who is second in the order (counting from the one who has served the longest)?
A. Nestor
B. Liza
C. Bea
D. Carlo
MARKED ANSWER B. Liza
WHY Liza is right. The clues give Carlo → Liza → Bea → Nestor, so Liza is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Carlo → Liza → Bea → Nestor.

### 162 | CIVIO-ANA-SYMBOL-SERIES-000163
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What comes next in the series?  FR, IS, LT, OU, ___
A. PV
B. RD
C. VR
D. RV
MARKED ANSWER D. RV
WHY RV is right: O + 3 = R and U + 1 = V.
SHORTCUT Split each pair. First letters: F, I, L, O (jump +3). Second letters: R, S, T, U (jump +1). Move each one more step.

### 163 | CIVIO-ANA-DI-TABLE-000164
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Supply use of envelopes (boxes) by office (Library: Jul 76, Aug 38, Sep 50; Assessor: Jul 18, Aug 40, Sep 76; Planning: Jul 64, Aug 14, Sep 22). In Sep, how many more did Assessor use than Planning?
A. 54
B. 46
C. 98
D. 34
MARKED ANSWER A. 54
WHY 54 is right: 76 − 22 = 54.
SHORTCUT Go to the Sep column: Planning 22, Assessor 76. Subtract the smaller from the larger.

### 164 | CIVIO-ANA-SYMBOL-SERIES-000165
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What comes next in the series?  AN, DP, GR, JT, ___
A. MV
B. VM
C. MZ
D. KV
MARKED ANSWER A. MV
WHY MV is right: J + 3 = M and T + 2 = V.
SHORTCUT Split each pair. First letters: A, D, G, J (jump +3). Second letters: N, P, R, T (jump +2). Move each one more step.

### 165 | CIVIO-ANA-SYMBOL-SERIES-000166
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What comes next in the series?  HL, JN, LP, NR, ___
A. PT
B. OT
C. TP
D. PU
MARKED ANSWER A. PT
WHY PT is right: N + 2 = P and R + 2 = T.
SHORTCUT Split each pair. First letters: H, J, L, N (jump +2). Second letters: L, N, P, R (jump +2). Move each one more step.

### 166 | CIVIO-VEN-ERROR-AGREE-000167
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The head of the three sections ____ absent during the audit.
A. being
B. were
C. was
D. been
MARKED ANSWER C. was
WHY "was" is right: "The head" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The head ____". The subject is singular, so use the singular verb.

### 167 | CIVIO-VEN-SENT-COMP-WORD-000168
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The doctor's advice was ____, so the patient followed it.
A. sense
B. sensitive
C. foolish
D. sensible
MARKED ANSWER D. sensible
WHY "sensible" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 168 | CIVIO-VEN-SENT-COMP-WORD-000169
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: All offices must ____ with the new dress code.
A. compile
B. comply
C. complain
D. comply to
MARKED ANSWER B. comply
WHY "comply" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 169 | CIVIO-VEN-SENT-COMP-WORD-000170
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The town is famous ____ its woven mats.
A. in
B. with
C. for
D. of
MARKED ANSWER C. for
WHY "for" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 170 | CIVIO-VEN-WORD-MEANING-000171
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What does the phrase in capital letters mean?  Let us not BEAT AROUND THE BUSH; the report is late.
A. speak directly
B. clear a garden
C. shout at someone
D. avoid the main point
MARKED ANSWER D. avoid the main point
WHY "avoid the main point" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 171 | CIVIO-VEN-ERROR-AGREE-000172
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The list of approved applicants ____ posted at the city hall lobby.
A. is
B. being
C. be
D. are
MARKED ANSWER A. is
WHY "is" is right: "The list" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The list ____". The subject is singular, so use the singular verb.

### 172 | CIVIO-VEN-ERROR-AGREE-000173
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The supply of vaccines ____ delivered on Monday.
A. been
B. being
C. were
D. was
MARKED ANSWER D. was
WHY "was" is right: "The supply" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The supply ____". The subject is singular, so use the singular verb.

### 173 | CIVIO-VEN-SENT-COMP-WORD-000174
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The report was so ____ that the board read it in five minutes.
A. brief
B. lengthy
C. briefing
D. brave
MARKED ANSWER A. brief
WHY "brief" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 174 | CIVIO-VEN-SENT-COMP-WORD-000175
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The ____ of the new policy was explained at the flag ceremony.
A. porpoise
B. purpose
C. propose
D. purpost
MARKED ANSWER B. purpose
WHY "purpose" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 175 | CIVIO-VEN-ERROR-AGREE-000176
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The quality of the roads ____ the travel time of buses.
A. affecting
B. affect
C. affects
D. to affect
MARKED ANSWER C. affects
WHY "affects" is right: "The quality" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The quality ____". The subject is singular, so use the singular verb.

### 176 | CIVIO-VEN-RC-VOCAB-000177
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The office had to RESOLVE the dispute between the two vendors.
A. decide firmly to do
B. worsen
C. revolve
D. settle
MARKED ANSWER D. settle
WHY "settle" is right: it is the sense of "resolve" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "resolve".

### 177 | CIVIO-VEN-RC-VOCAB-000178
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The new rule will AFFECT all employees.
A. pretend to feel
B. leave untouched
C. effect
D. have an effect on
MARKED ANSWER D. have an effect on
WHY "have an effect on" is right: it is the sense of "affect" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "affect".

### 178 | CIVIO-VEN-SENT-COMP-WORD-000179
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: Each employee must bring ____ own ID.
A. one's
B. their own's
C. its
D. his or her
MARKED ANSWER D. his or her
WHY "his or her" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 179 | CIVIO-VEN-SENT-COMP-PHRASAL-000180
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the phrase that best completes the sentence: Please ____ your report before Friday.
A. hand in
B. hand over
C. hand out
D. hand down
MARKED ANSWER A. hand in
WHY "hand in" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 180 | CIVIO-VEN-SENT-COMP-WORD-000181
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: Between you and ____, the plan needs more work.
A. I
B. me
C. mine
D. myself
MARKED ANSWER B. me
WHY "me" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 181 | CIVIO-VEN-WORD-MEANING-000182
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  FEASIBLE
A. workable
B. impossible
C. visible
D. festive
MARKED ANSWER B. impossible
WHY "impossible" is right. "Feasible" means workable; "impossible" is the reverse.
SHORTCUT First say what "feasible" means (workable). Then look for the word that means the reverse.

### 182 | CIVIO-VEN-SENT-COMP-WORD-000183
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the word that best completes the sentence: The team worked faster ____ the other shift.
A. as
B. that
C. then
D. than
MARKED ANSWER D. than
WHY "than" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 183 | CIVIO-VEN-WORD-MEANING-000184
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What does the phrase in capital letters mean?  The two offices finally SEE EYE TO EYE on the budget.
A. agree
B. disagree
C. meet in person
D. agree on everything forever
MARKED ANSWER A. agree
WHY "agree" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 184 | CIVIO-VEN-WORD-MEANING-000185
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is closest in meaning to the word in capital letters?  DETERIORATE
A. determine
B. worsen
C. detour
D. improve
MARKED ANSWER B. worsen
WHY "worsen" is right. "Deteriorate" means worsen.
SHORTCUT Make a short sentence with "deteriorate", then swap in each choice. Watch for words that only look or sound like "deteriorate".

### 185 | CIVIO-VEN-SENT-COMP-PHRASAL-000186
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Choose the phrase that best completes the sentence: The barangay will ____ the cause of the blackout.
A. look for
B. look into
C. look up
D. look on
MARKED ANSWER B. look into
WHY "look into" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 186 | CIVIO-CLR-SPELL-WRONG-000187
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  conscientious | commitmant | jewelry | entrepreneur
A. conscientious
B. commitmant
C. jewelry
D. entrepreneur
MARKED ANSWER B. commitmant
WHY "commitmant" is misspelled: it is spelled the way the word sounds. The correct spelling is "commitment".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 187 | CIVIO-CLR-SPELL-WRONG-000188
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  noticeable | maintennce | assessment | foreign
A. noticeable
B. maintennce
C. assessment
D. foreign
MARKED ANSWER B. maintennce
WHY "maintennce" is misspelled: it drops a letter. The correct spelling is "maintenance".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 188 | CIVIO-CLR-SPELL-RIGHT-000189
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is spelled correctly?  fluoresent | fluorscent | fluorrescent | fluorescent
A. fluoresent
B. fluorscent
C. fluorrescent
D. fluorescent
MARKED ANSWER D. fluorescent
WHY "fluorescent" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 189 | CIVIO-CLR-FILE-POSITION-000190
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In alphabetical filing, which name is filed FIRST?  Felipe D. Leon | Atty. Danilo F. Rosario | Elena P. Delos Reyes | Engr. Carlos T. De los Santos
A. Engr. Carlos T. De los Santos
B. Atty. Danilo F. Rosario
C. Elena P. Delos Reyes
D. Felipe D. Leon
MARKED ANSWER C. Elena P. Delos Reyes
WHY "Elena P. Delos Reyes" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Elena P. Delos Reyes → DELOSREYES, Elena; Engr. Carlos T. De los Santos → DELOSSANTOS, Carlos; Felipe D. Leon → LEON, Felipe; Atty. Danilo F. Rosario → ROSARIO, Danilo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 190 | CIVIO-CLR-SPELL-WRONG-000191
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  consceince | dilemma | seize | accessible
A. consceince
B. dilemma
C. seize
D. accessible
MARKED ANSWER A. consceince
WHY "consceince" is misspelled: it swaps the order of i and e. The correct spelling is "conscience".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 191 | CIVIO-CLR-SPELL-WRONG-000192
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  address | harss | inoculate | omission
A. address
B. harss
C. inoculate
D. omission
MARKED ANSWER B. harss
WHY "harss" is misspelled: it drops a letter. The correct spelling is "harass".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 192 | CIVIO-CLR-FILE-POSITION-000193
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In alphabetical filing, which name is filed FIRST?  Danilo P. San Juan | Benito N. Salazar | Dr. Victoria S. Del Rosario | Engr. Evelyn L. Garcia
A. Engr. Evelyn L. Garcia
B. Benito N. Salazar
C. Danilo P. San Juan
D. Dr. Victoria S. Del Rosario
MARKED ANSWER D. Dr. Victoria S. Del Rosario
WHY "Dr. Victoria S. Del Rosario" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Dr. Victoria S. Del Rosario → DELROSARIO, Victoria; Engr. Evelyn L. Garcia → GARCIA, Evelyn; Benito N. Salazar → SALAZAR, Benito; Danilo P. San Juan → SANJUAN, Danilo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 193 | CIVIO-CLR-SPELL-WRONG-000194
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  occurred | mischievous | permissible | privilej
A. occurred
B. mischievous
C. permissible
D. privilej
MARKED ANSWER D. privilej
WHY "privilej" is misspelled: it is spelled the way the word sounds. The correct spelling is "privilege".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 194 | CIVIO-CLR-SPELL-WRONG-000195
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  liaison | unanimus | schedule | transferred
A. liaison
B. unanimus
C. schedule
D. transferred
MARKED ANSWER B. unanimus
WHY "unanimus" is misspelled: it is spelled the way the word sounds. The correct spelling is "unanimous".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 195 | CIVIO-CLR-SPELL-RIGHT-000196
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is spelled correctly?  consceince | consciance | conscince | conscience
A. consceince
B. consciance
C. conscince
D. conscience
MARKED ANSWER D. conscience
WHY "conscience" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 196 | CIVIO-CLR-SPELL-RIGHT-000197
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is spelled correctly?  acknowledgmant | acknowledgment | acknowldgment | acknwledgment
A. acknowledgmant
B. acknowledgment
C. acknowldgment
D. acknwledgment
MARKED ANSWER B. acknowledgment
WHY "acknowledgment" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 197 | CIVIO-CLR-FILE-POSITION-000198
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In alphabetical filing, which name is filed LAST?  Atty. Elena M. Navarro | Ana C. Rivera | Atty. Maria A. Mendoza | Jose N. Del Rosario
A. Ana C. Rivera
B. Atty. Maria A. Mendoza
C. Jose N. Del Rosario
D. Atty. Elena M. Navarro
MARKED ANSWER A. Ana C. Rivera
WHY "Ana C. Rivera" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Jose N. Del Rosario → DELROSARIO, Jose; Atty. Maria A. Mendoza → MENDOZA, Maria; Atty. Elena M. Navarro → NAVARRO, Elena; Ana C. Rivera → RIVERA, Ana.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 198 | CIVIO-CLR-SPELL-RIGHT-000199
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is spelled correctly?  accessable | acessible | accessible | accssible
A. accessable
B. acessible
C. accessible
D. accssible
MARKED ANSWER C. accessible
WHY "accessible" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 199 | CIVIO-CLR-FILE-POSITION-000200
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In alphabetical filing, which name is filed FIRST?  Engr. Felipe R. Ramos | Eduardo P. Salazar | Victoria E. Ocampo | Corazon C. Delos Reyes
A. Victoria E. Ocampo
B. Eduardo P. Salazar
C. Corazon C. Delos Reyes
D. Engr. Felipe R. Ramos
MARKED ANSWER C. Corazon C. Delos Reyes
WHY "Corazon C. Delos Reyes" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Corazon C. Delos Reyes → DELOSREYES, Corazon; Victoria E. Ocampo → OCAMPO, Victoria; Engr. Felipe R. Ramos → RAMOS, Felipe; Eduardo P. Salazar → SALAZAR, Eduardo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 200 | CIVIO-CLR-SPELL-WRONG-000201
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which word is misspelled?  privillege | omission | conscience | accessible
A. privillege
B. omission
C. conscience
D. accessible
MARKED ANSWER A. privillege
WHY "privillege" is misspelled: it doubles or undoubles a consonant. The correct spelling is "privilege".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 201 | CIVIO-GI-WHO-HOLDS-POWER-000202
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Under R.A. 6713, who co-chair the Committee on Awards to Outstanding Public Officials and Employees?
A. The Chairman of the Commission on Audit and the Ombudsman
B. The Chairman of the Civil Service Commission and the Secretary of Justice
C. The Ombudsman and the Chairman of the Civil Service Commission
D. The President and the Senate President
MARKED ANSWER C. The Ombudsman and the Chairman of the Civil Service Commission
WHY "The Ombudsman and the Chairman of the Civil Service Commission" is right. R.A. 6713, Sec. 6 says: "the Ombudsman and Chairman of the Civil Service Commission as Co-Chairmen".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 6. The Ombudsman and the CSC Chairman co-chair; the COA Chairman is a member.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 202 | CIVIO-GI-DEADLINE-NUMBER-000203
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Under R.A. 6713, public officials and employees must process documents and papers how?
A. In the order of the applicant's rank
B. Within 60 working days, with up to five signatories
C. Only after the head of office signs personally
D. Within a reasonable time, with not more than three signatories as far as practicable
MARKED ANSWER D. Within a reasonable time, with not more than three signatories as far as practicable
WHY "Within a reasonable time, with not more than three signatories as far as practicable" is right. R.A. 6713, Sec. 5(c) says: "processed and completed within a reasonable time from the preparation thereof and must contain, as far as practicable, not more than three (3) signatories".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 5(c). Reasonable time; at most three signatories as far as practicable.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 203 | CIVIO-GI-DEADLINE-NUMBER-000204
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Within how many days must a Constitutional Commission decide a case after it is submitted for decision?
A. 90 days
B. 60 days
C. 30 days
D. 15 days
MARKED ANSWER B. 60 days
WHY "60 days" is right. Art. IX-A, Sec. 7 says: "within sixty days from the date of its submission for decision".
SHORTCUT Tie the fact to its section: Art. IX-A, Sec. 7. Commissions decide within 60 days of submission.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 204 | CIVIO-GI-DEADLINE-NUMBER-000205
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
How many successive terms may the Vice-President serve?
A. Two
B. No limit
C. One
D. Three
MARKED ANSWER A. Two
WHY "Two" is right. Art. VII, Sec. 4 says: "No Vice-President shall serve for more than two successive terms".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 4. The Vice-President is limited to two successive terms.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 205 | CIVIO-GI-DEADLINE-NUMBER-000206
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
How many members make up the Supreme Court, counting the Chief Justice?
A. 13
B. 9
C. 11
D. 15
MARKED ANSWER D. 15
WHY "15" is right. Art. VIII, Sec. 4(1) says: "a Chief Justice and fourteen Associate Justices".
SHORTCUT Tie the fact to its section: Art. VIII, Sec. 4(1). One Chief Justice plus 14 Associate Justices.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 206 | CIVIO-GI-WHO-HOLDS-POWER-000207
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
In whom is executive power vested under the 1987 Constitution?
A. The Senate President
B. The President
C. The Vice-President
D. The Cabinet
MARKED ANSWER B. The President
WHY "The President" is right. Art. VII, Sec. 1 says: "The executive power shall be vested in the President of the Philippines".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 1. Executive power belongs to the President.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 207 | CIVIO-GI-DEADLINE-NUMBER-000208
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What is the minimum age to be a Member of the House of Representatives?
A. 35 years old
B. 21 years old
C. 25 years old
D. 30 years old
MARKED ANSWER C. 25 years old
WHY "25 years old" is right. Art. VI, Sec. 6 says: "at least twenty-five years of age".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 6. A House Member must be at least 25 on election day.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 208 | CIVIO-GI-WHO-HOLDS-POWER-000209
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
Which body has the sole power to try and decide impeachment cases?
A. Senate
B. Supreme Court
C. Sandiganbayan
D. House of Representatives
MARKED ANSWER A. Senate
WHY "Senate" is right. Art. XI, Sec. 3(6) says: "The Senate shall have the sole power to try and decide all cases of impeachment".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 3(6). The Senate tries impeachment.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 209 | CIVIO-GI-DEADLINE-NUMBER-000210
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What vote of all Senators is needed to convict in an impeachment case?
A. One-third
B. Two-thirds
C. Majority
D. Three-fourths
MARKED ANSWER B. Two-thirds
WHY "Two-thirds" is right. Art. XI, Sec. 3(6) says: "concurrence of two-thirds of all the Members of the Senate".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 3(6). Conviction needs two-thirds of all Senators.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 210 | CIVIO-GI-DEADLINE-NUMBER-000211
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-003.json
STEM
What is the minimum age to be elected President of the Philippines?
A. 50 years old
B. 45 years old
C. 35 years old
D. 40 years old
MARKED ANSWER D. 40 years old
WHY "40 years old" is right. Art. VII, Sec. 2 says: "at least forty years of age on the day of the election".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 2. The President must be at least 40 on election day.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 211 | CIVIO-NUM-WP-RATE-000212
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Grace can paint a classroom in 6 hours. Mang Jun can do the same job in 3 hours. Working together, how long will they take?
A. 2 hours
B. 9 hours
C. 4.5 hours
D. 30 minutes
MARKED ANSWER A. 2 hours
WHY 2 hours is right. Check: in 2 hours, Grace does 2/6 and Mang Jun does 2/3; together that is 1 whole job.
SHORTCUT Per hour, Grace does 1/6 and Mang Jun does 1/3. Together: 1/6 + 1/3 = 1/2. So the whole job takes 2 hours.

### 212 | CIVIO-NUM-OPS-ORDER-000213
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What is the value of 7 + 9 × 8 − 9?
A. 119
B. -2
C. 15
D. 70
MARKED ANSWER D. 70
WHY 70 is right: 7 + 72 = 79, and 79 − 9 = 70.
SHORTCUT Circle the × first: 9 × 8 = 72. Then go left to right: 7 + 72 − 9.

### 213 | CIVIO-NUM-SEQ-MULT-000214
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What number comes next?  3, 11, 35, 107, 323, ___
A. 973
B. 971
C. 539
D. 969
MARKED ANSWER B. 971
WHY 971 is right: 323 × 3 = 969, then + 2 gives 971.
SHORTCUT Test "times 3, then + 2" on the first numbers: 3 × 3 + 2 = 11; 11 × 3 + 2 = 35. It works, so use it on 323.

### 214 | CIVIO-NUM-WP-AVERAGE-000215
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
The average age of the 5 drivers in the district hospital is 45 years. One more person, with 51 years, joins them. What is the new average age?
A. 46 years
B. 276 years
C. 46.2 years
D. 48 years
MARKED ANSWER A. 46 years
WHY 46 years is right. Long way: 5 × 45 = 225; + 51 = 276; ÷ 6 = 46.
SHORTCUT The new person is 51 − 45 = 6 above the old average. Share that among all 6 people: 6 ÷ 6 = 1. Add it: 45 + 1 = 46.

### 215 | CIVIO-NUM-WP-ALGEBRA-000216
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Inday is 3 times as old as her nephew. In 11 years, Inday will be twice as old as the nephew. How old is Inday now?
A. 33
B. 44
C. 11
D. 22
MARKED ANSWER A. 33
WHY 33 is right. Algebra: nephew = s, Inday = 3s; 3s + 11 = 2(s + 11) gives s = 11, so Inday = 33.
SHORTCUT Try the choices. If Inday is 33, the nephew is 11. In 11 years: 44 and 22. 44 = 2 × 22, so it works.

### 216 | CIVIO-NUM-WP-PCT-CHANGE-000217
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A teacher borrows ₱20,000 at 5% simple interest per year. How much interest is due after 1 year and 6 months?
A. ₱1,500
B. ₱1,600
C. ₱1,000
D. ₱21,500
MARKED ANSWER A. ₱1,500
WHY ₱1,500 is right. Check: 20,000 × 0.05 × 1.5 = 1,500.
SHORTCUT Find one year first: 5% of ₱20,000 = ₱1,000. Time is 1.5 years. Multiply: 1.5 × ₱1,000 = ₱1,500.

### 217 | CIVIO-NUM-WP-PCT-CHANGE-000218
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A vendor borrows ₱30,000 at 3% simple interest per year. How much interest is due after 2 years and 6 months?
A. ₱2,340
B. ₱1,800
C. ₱32,250
D. ₱2,250
MARKED ANSWER D. ₱2,250
WHY ₱2,250 is right. Check: 30,000 × 0.03 × 2.5 = 2,250.
SHORTCUT Find one year first: 3% of ₱30,000 = ₱900. Time is 2.5 years. Multiply: 2.5 × ₱900 = ₱2,250.

### 218 | CIVIO-NUM-WP-ALGEBRA-000219
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Analyn is 3 times as old as her son. In 10 years, Analyn will be twice as old as the son. How old is Analyn now?
A. 20
B. 10
C. 30
D. 40
MARKED ANSWER C. 30
WHY 30 is right. Algebra: son = s, Analyn = 3s; 3s + 10 = 2(s + 10) gives s = 10, so Analyn = 30.
SHORTCUT Try the choices. If Analyn is 30, the son is 10. In 10 years: 40 and 20. 40 = 2 × 20, so it works.

### 219 | CIVIO-NUM-SEQ-DIFF-000220
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What number comes next in the series?  11, 15, 20, 26, 33, ___
A. 41
B. 42
C. 37
D. 40
MARKED ANSWER A. 41
WHY 41 is right: 33 + 8 = 41.
SHORTCUT Write the jumps under the list: +4, +5, +6, +7. Each jump is 1 more than the one before. So the next jump is +8.

### 220 | CIVIO-NUM-WP-PCT-CHANGE-000221
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A office chair is priced at ₱480. It is sold at 15% off. How much does a buyer pay?
A. ₱72
B. ₱408
C. ₱465
D. ₱552
MARKED ANSWER B. ₱408
WHY ₱408 is right. Check: discount ₱72; ₱480 − ₱72 = ₱408.
SHORTCUT Pay 85% of the price: ₱480 × 0.85 = ₱408.

### 221 | CIVIO-NUM-SEQ-DIFF-000222
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which number should come next?  4, 9, 16, 25, 36, ___
A. 47
B. 41
C. 51
D. 49
MARKED ANSWER D. 49
WHY 49 is right: 36 + 13 = 49.
SHORTCUT Write the jumps under the list: +5, +7, +9, +11. Each jump is 2 more than the one before. So the next jump is +13.

### 222 | CIVIO-NUM-WP-RATIO-000223
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A ₱3,500 prize money is divided between Aileen and Tess in the ratio 3 : 4. What is Tess's share?
A. ₱500
B. ₱2,000
C. ₱1,500
D. ₱875
MARKED ANSWER B. ₱2,000
WHY ₱2,000 is right: 4 × ₱500 = ₱2,000. Check: ₱1,500 + ₱2,000 = ₱3,500.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 4 = 7. One part = ₱3,500 ÷ 7 = ₱500. Then multiply by the parts you need.

### 223 | CIVIO-NUM-WP-PCT-CHANGE-000224
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A rice cooker is priced at ₱960. It is sold at 25% off. How much does a buyer pay?
A. ₱935
B. ₱240
C. ₱720
D. ₱1,200
MARKED ANSWER C. ₱720
WHY ₱720 is right. Check: discount ₱240; ₱960 − ₱240 = ₱720.
SHORTCUT Pay 75% of the price: ₱960 × 0.75 = ₱720.

### 224 | CIVIO-NUM-WP-GEOM-000225
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A rectangular vegetable garden is 38 m long and 14 m wide. A lace border costs ₱75 per meter. How much will it cost to put the lace border around the whole vegetable garden?
A. ₱104
B. ₱39,900
C. ₱3,900
D. ₱7,800
MARKED ANSWER D. ₱7,800
WHY ₱7,800 is right: 104 m × ₱75 = ₱7,800.
SHORTCUT Around = 2 × (38 + 14) = 104 m. Cost = 104 × ₱75.

### 225 | CIVIO-NUM-WP-GEOM-000226
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A rectangular parking area is 22 m long and 7 m wide. A edging costs ₱40 per meter. How much will it cost to put the edging around the whole parking area?
A. ₱6,160
B. ₱58
C. ₱2,320
D. ₱1,160
MARKED ANSWER C. ₱2,320
WHY ₱2,320 is right: 58 m × ₱40 = ₱2,320.
SHORTCUT Around = 2 × (22 + 7) = 58 m. Cost = 58 × ₱40.

### 226 | CIVIO-NUM-WP-PCT-CHANGE-000227
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A supplier sold a tank of LPG for ₱1,200. It raised the price by 40%. Later, it lowered the new price by 40%. What is the final price?
A. ₱1,411.20
B. ₱1,680
C. ₱1,200
D. ₱1,008
MARKED ANSWER D. ₱1,008
WHY ₱1,008 is right. Check: 1,200 × 1.4 = 1,680, and 1,680 × 0.6 = 1,008.
SHORTCUT Do one change at a time. ₱1,200 up 40% is ₱1,200 + ₱480 = ₱1,680. Then 40% of ₱1,680 is ₱672, so ₱1,680 − ₱672 = ₱1,008.

### 227 | CIVIO-NUM-WP-PCT-CHANGE-000228
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A cooperative member borrows ₱10,000 at 12% simple interest per year. How much interest is due after 2 years and 6 months?
A. ₱3,000
B. ₱13,000
C. ₱2,400
D. ₱3,120
MARKED ANSWER A. ₱3,000
WHY ₱3,000 is right. Check: 10,000 × 0.12 × 2.5 = 3,000.
SHORTCUT Find one year first: 12% of ₱10,000 = ₱1,200. Time is 2.5 years. Multiply: 2.5 × ₱1,200 = ₱3,000.

### 228 | CIVIO-NUM-WP-ALGEBRA-000229
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Rhea is 5 times as old as her son. In 24 years, Rhea will be twice as old as the son. How old is Rhea now?
A. 40
B. 8
C. 64
D. 32
MARKED ANSWER A. 40
WHY 40 is right. Algebra: son = s, Rhea = 5s; 5s + 24 = 2(s + 24) gives s = 8, so Rhea = 40.
SHORTCUT Try the choices. If Rhea is 40, the son is 8. In 24 years: 64 and 32. 64 = 2 × 32, so it works.

### 229 | CIVIO-NUM-WP-PCT-CHANGE-000230
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A backpack is priced at ₱1,800. It is sold at 25% off. How much does a buyer pay?
A. ₱2,250
B. ₱1,775
C. ₱450
D. ₱1,350
MARKED ANSWER D. ₱1,350
WHY ₱1,350 is right. Check: discount ₱450; ₱1,800 − ₱450 = ₱1,350.
SHORTCUT Pay 75% of the price: ₱1,800 × 0.75 = ₱1,350.

### 230 | CIVIO-NUM-FRAC-DEC-000231
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A barangay had 180 bags of cement. It gave out 1/3 of them on Monday and 3/5 of the remaining bags of cement on Tuesday. How many are left?
A. 48
B. 120
C. 12
D. 72
MARKED ANSWER A. 48
WHY 48 is right. Check: 60 + 72 + 48 = 180.
SHORTCUT Go day by day. Monday: 1/3 of 180 = 60, so 120 left. Tuesday: 3/5 of 120 = 72, so 120 − 72 = 48 left.

### 231 | CIVIO-NUM-WP-AVERAGE-000232
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
The average years of service of the 9 drivers in the engineering office is 12 years. One more person, with 52 years, joins them. What is the new average years of service?
A. 16 years
B. 16.44 years
C. 32 years
D. 160 years
MARKED ANSWER A. 16 years
WHY 16 years is right. Long way: 9 × 12 = 108; + 52 = 160; ÷ 10 = 16.
SHORTCUT The new person is 52 − 12 = 40 above the old average. Share that among all 10 people: 40 ÷ 10 = 4. Add it: 12 + 4 = 16.

### 232 | CIVIO-NUM-WP-AVERAGE-000233
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
The average age of the 4 clerks in the barangay hall is 24 years. One more person, with 34 years, joins them. What is the new average age?
A. 26 years
B. 29 years
C. 26.5 years
D. 130 years
MARKED ANSWER A. 26 years
WHY 26 years is right. Long way: 4 × 24 = 96; + 34 = 130; ÷ 5 = 26.
SHORTCUT The new person is 34 − 24 = 10 above the old average. Share that among all 5 people: 10 ÷ 5 = 2. Add it: 24 + 2 = 26.

### 233 | CIVIO-NUM-WP-RATIO-000234
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A ₱12,000 commission is divided between Teresa and Grace in the ratio 3 : 7. What is Grace's share?
A. ₱8,400
B. ₱1,200
C. ₱3,600
D. ₱1,714.29
MARKED ANSWER A. ₱8,400
WHY ₱8,400 is right: 7 × ₱1,200 = ₱8,400. Check: ₱3,600 + ₱8,400 = ₱12,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱12,000 ÷ 10 = ₱1,200. Then multiply by the parts you need.

### 234 | CIVIO-NUM-OPS-ORDER-000235
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What is the value of 17 + 6 × 8 − 3?
A. 181
B. 47
C. 62
D. 28
MARKED ANSWER C. 62
WHY 62 is right: 17 + 48 = 65, and 65 − 3 = 62.
SHORTCUT Circle the × first: 6 × 8 = 48. Then go left to right: 17 + 48 − 3.

### 235 | CIVIO-NUM-WP-GEOM-000236
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A rectangular parking area is 23 m long and 16 m wide. A lace border costs ₱50 per meter. How much will it cost to put the lace border around the whole parking area?
A. ₱18,400
B. ₱3,900
C. ₱78
D. ₱1,950
MARKED ANSWER B. ₱3,900
WHY ₱3,900 is right: 78 m × ₱50 = ₱3,900.
SHORTCUT Around = 2 × (23 + 16) = 78 m. Cost = 78 × ₱50.

### 236 | CIVIO-NUM-FRAC-DEC-000237
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
A barangay had 1440 bags of cement. It gave out 1/3 of them on Monday and 1/3 of the remaining bags of cement on Tuesday. How many are left?
A. 640
B. 480
C. 960
D. 320
MARKED ANSWER A. 640
WHY 640 is right. Check: 480 + 320 + 640 = 1440.
SHORTCUT Go day by day. Monday: 1/3 of 1440 = 480, so 960 left. Tuesday: 1/3 of 960 = 320, so 960 − 320 = 640 left.

### 237 | CIVIO-NUM-SEQ-DIFF-000238
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What number comes next in the series?  7, 12, 18, 25, 33, ___
A. 42
B. 38
C. 43
D. 41
MARKED ANSWER A. 42
WHY 42 is right: 33 + 9 = 42.
SHORTCUT Write the jumps under the list: +5, +6, +7, +8. Each jump is 1 more than the one before. So the next jump is +9.

### 238 | CIVIO-NUM-WP-RATE-000239
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Bea can label the census boxes in 30 hours. Rhea can do the same job in 60 hours. Working together, how long will they take?
A. 3 minutes
B. 20 hours
C. 90 hours
D. 45 hours
MARKED ANSWER B. 20 hours
WHY 20 hours is right. Check: in 20 hours, Bea does 20/30 and Rhea does 20/60; together that is 1 whole job.
SHORTCUT Per hour, Bea does 1/30 and Rhea does 1/60. Together: 1/30 + 1/60 = 1/20. So the whole job takes 20 hours.

### 239 | CIVIO-NUM-OPS-ORDER-000240
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What is the value of 19 + 2 × 5 − 2?
A. 24
B. 27
C. 103
D. 25
MARKED ANSWER B. 27
WHY 27 is right: 19 + 10 = 29, and 29 − 2 = 27.
SHORTCUT Circle the × first: 2 × 5 = 10. Then go left to right: 19 + 10 − 2.

### 240 | CIVIO-NUM-SEQ-MULT-000241
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What number comes next?  4, 13, 40, 121, 364, ___
A. 1092
B. 1093
C. 1094
D. 607
MARKED ANSWER B. 1093
WHY 1093 is right: 364 × 3 = 1092, then + 1 gives 1093.
SHORTCUT Test "times 3, then + 1" on the first numbers: 4 × 3 + 1 = 13; 13 × 3 + 1 = 40. It works, so use it on 364.

### 241 | CIVIO-ANA-CONCLUSION-000242
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Four staff members are compared. Analyn finished the report earlier than Efren. Inday finished the report earlier than Mang Jun. Mang Jun finished the report earlier than Analyn. Who is second in the order (counting from the one who finished first)?
A. Analyn
B. Efren
C. Mang Jun
D. Inday
MARKED ANSWER C. Mang Jun
WHY Mang Jun is right. The clues give Inday → Mang Jun → Analyn → Efren, so Mang Jun is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Inday → Mang Jun → Analyn → Efren.

### 242 | CIVIO-ANA-ASSUME-I-II-000243
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Statement: The treasurer will send payment reminders by text and by letter to reach all taxpayers.
Assumption I: Some taxpayers may not get text messages.
Assumption II: Some taxpayers may not read mailed letters.
Which assumption is implicit in the statement?
A. Both I and II
B. Only I
C. Only II
D. Neither I nor II
MARKED ANSWER A. Both I and II
WHY "Both I and II" is right. Both assumptions are needed for the plan to make sense.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 243 | CIVIO-ANA-SYLLOGISM-000244
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Statement 1: No official papers are unregistered items. Statement 2: All memos are official papers. Which conclusion follows from both statements?
A. Some memos are unregistered items.
B. No records are unregistered items.
C. All official papers are memos.
D. No memos are unregistered items.
MARKED ANSWER D. No memos are unregistered items.
WHY "No memos are unregistered items." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the memos circle inside official papers. The "unregistered items" circle sits outside official papers, so it is outside memos too.

### 244 | CIVIO-ANA-DI-TABLE-000245
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Supply use of ballpens (boxes) by office (Engineering: Apr 56, May 74, Jun 38; HR: Apr 52, May 60, Jun 52; Planning: Apr 46, May 30, Jun 26). In Jun, how many more did Engineering use than Planning?
A. 66
B. 12
C. 10
D. 64
MARKED ANSWER B. 12
WHY 12 is right: 38 − 26 = 12.
SHORTCUT Go to the Jun column: Engineering 38, Planning 26. Subtract the smaller from the larger.

### 245 | CIVIO-ANA-SYLLOGISM-000246
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
All barangay captains are elected officials. No elected officials are late payers. Which conclusion must be true?
A. All elected officials are barangay captains.
B. No public officers are late payers.
C. Some barangay captains are late payers.
D. No barangay captains are late payers.
MARKED ANSWER D. No barangay captains are late payers.
WHY "No barangay captains are late payers." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the barangay captains circle inside elected officials. The "late payers" circle sits outside elected officials, so it is outside barangay captains too.

### 246 | CIVIO-ANA-SYLLOGISM-000247
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Assume these are true: none of the elected officials are new trainees, and every one of the barangay captains is among the elected officials. What can be concluded for certain?
A. Some barangay captains are new trainees.
B. All elected officials are barangay captains.
C. No barangay captains are new trainees.
D. No public officers are new trainees.
MARKED ANSWER C. No barangay captains are new trainees.
WHY "No barangay captains are new trainees." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the barangay captains circle inside elected officials. The "new trainees" circle sits outside elected officials, so it is outside barangay captains too.

### 247 | CIVIO-ANA-SYMBOL-SERIES-000248
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What comes next in the series?  HK, KN, NQ, QT, ___
A. TW
B. WT
C. TX
D. RW
MARKED ANSWER A. TW
WHY TW is right: Q + 3 = T and T + 3 = W.
SHORTCUT Split each pair. First letters: H, K, N, Q (jump +3). Second letters: K, N, Q, T (jump +3). Move each one more step.

### 248 | CIVIO-ANA-SYMBOL-SERIES-000249
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In a certain code, BRIDGE is written as EULGJH. How is MEMO written in the same code?
A. PHPR
B. QIQS
C. JBJL
D. PHPO
MARKED ANSWER A. PHPR
WHY PHPR is right: each letter of MEMO moved 3 places forward.
SHORTCUT Compare the first letters: B became E. That is 3 places forward. Check one more letter, then shift every letter of MEMO the same way.

### 249 | CIVIO-ANA-SYMBOL-SERIES-000250
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In a certain code, MAYOR is written as NBZPS. How is BOARD written in the same code?
A. DQCTF
B. ANZQC
C. CPBSD
D. CPBSE
MARKED ANSWER D. CPBSE
WHY CPBSE is right: each letter of BOARD moved 1 place forward.
SHORTCUT Compare the first letters: M became N. That is 1 place forward. Check one more letter, then shift every letter of BOARD the same way.

### 250 | CIVIO-ANA-SYMBOL-SERIES-000251
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What comes next in the series?  CN, EO, GP, IQ, ___
A. KR
B. RK
C. JR
D. KV
MARKED ANSWER A. KR
WHY KR is right: I + 2 = K and Q + 1 = R.
SHORTCUT Split each pair. First letters: C, E, G, I (jump +2). Second letters: N, O, P, Q (jump +1). Move each one more step.

### 251 | CIVIO-ANA-ANALOGY-DEGREE-000252
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
POND : LAKE :: ____
A. hill : mountain
B. fish : water
C. river : bridge
D. lake : pond
MARKED ANSWER A. hill : mountain
WHY "hill : mountain" is right. It has the same link, lesser : greater degree, in the same order.
SHORTCUT Make a sentence for the stem: "pond is to lake" as lesser : greater degree. Test each choice in that sentence.

### 252 | CIVIO-ANA-SYLLOGISM-000253
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Statement 1: No accountants are absentees. Statement 2: All auditors are accountants. Which conclusion follows from both statements?
A. No auditors are absentees.
B. No licensed workers are absentees.
C. Some auditors are absentees.
D. All accountants are auditors.
MARKED ANSWER A. No auditors are absentees.
WHY "No auditors are absentees." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the auditors circle inside accountants. The "absentees" circle sits outside accountants, so it is outside auditors too.

### 253 | CIVIO-ANA-SYLLOGISM-000254
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Assume these are true: a few of the memos are items in the audit sample, and all of the memos are official papers. What can be concluded for certain?
A. Some official papers are items in the audit sample.
B. All official papers are items in the audit sample.
C. All items in the audit sample are memos.
D. No official papers are items in the audit sample.
MARKED ANSWER A. Some official papers are items in the audit sample.
WHY "Some official papers are items in the audit sample." is right. It follows from the two statements with no extra facts.
SHORTCUT The memos who are items in the audit sample are also official papers. So at least some official papers are items in the audit sample.

### 254 | CIVIO-ANA-DI-TABLE-000255
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Supply use of ballpens (boxes) by office (Library: Apr 46, May 40, Jun 74; Records: Apr 78, May 28, Jun 72; Planning: Apr 10, May 32, Jun 78). In Jun, how many more did Planning use than Library?
A. 40
B. 4
C. 152
D. 36
MARKED ANSWER B. 4
WHY 4 is right: 78 − 74 = 4.
SHORTCUT Go to the Jun column: Library 74, Planning 78. Subtract the smaller from the larger.

### 255 | CIVIO-ANA-SYMBOL-SERIES-000256
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In a certain code, CLERK is written as ENGTM. How is MEMO written in the same code?
A. OGOQ
B. KCKM
C. OGOO
D. PHPR
MARKED ANSWER A. OGOQ
WHY OGOQ is right: each letter of MEMO moved 2 places forward.
SHORTCUT Compare the first letters: C became E. That is 2 places forward. Check one more letter, then shift every letter of MEMO the same way.

### 256 | CIVIO-ANA-CONCLUSION-000257
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Four staff members are compared. Inday encoded more forms than Mang Jun. Arnel encoded more forms than Inday. Ramon encoded more forms than Arnel. Who is third in the order (counting from the one who encoded the most forms)?
A. Arnel
B. Mang Jun
C. Inday
D. Ramon
MARKED ANSWER C. Inday
WHY Inday is right. The clues give Ramon → Arnel → Inday → Mang Jun, so Inday is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Ramon → Arnel → Inday → Mang Jun.

### 257 | CIVIO-ANA-ASSUME-I-II-000258
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Statement: The school asks parents to sign a form before students join the field trip.
Assumption I: Parents' consent matters for the trip.
Assumption II: All students dislike field trips.
Which assumption is implicit in the statement?
A. Only I
B. Neither I nor II
C. Both I and II
D. Only II
MARKED ANSWER A. Only I
WHY "Only I" is right. Only assumption I is needed. II ("All students dislike field trips.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 258 | CIVIO-ANA-ANALOGY-SYN-000259
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Find the pair whose link matches the link between "ancient" and "old".
A. antique : shop
B. rapid : fast
C. new : old
D. history : past
MARKED ANSWER B. rapid : fast
WHY "rapid : fast" is right. It has the same link, similar meaning, in the same order.
SHORTCUT Make a sentence for the stem: "ancient is to old" as similar meaning. Test each choice in that sentence.

### 259 | CIVIO-ANA-SYMBOL-SERIES-000260
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What comes next in the series?  AP, DR, GT, JV, ___
A. MX
B. XM
C. MB
D. KX
MARKED ANSWER A. MX
WHY MX is right: J + 3 = M and V + 2 = X.
SHORTCUT Split each pair. First letters: A, D, G, J (jump +3). Second letters: P, R, T, V (jump +2). Move each one more step.

### 260 | CIVIO-ANA-ANALOGY-PART-000261
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
CHAPTER : BOOK :: ____
A. album : track
B. novel : story
C. verse : song
D. title : cover
MARKED ANSWER C. verse : song
WHY "verse : song" is right. It has the same link, part : whole, in the same order.
SHORTCUT Make a sentence for the stem: "chapter is to book" as part : whole. Test each choice in that sentence.

### 261 | CIVIO-ANA-CONCLUSION-000262
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Four staff members are compared. Arnel arrived earlier than Nonoy. Dindo arrived earlier than Arnel. Nonoy arrived earlier than Analyn. Who is third in the order (counting from the one who arrived first)?
A. Analyn
B. Nonoy
C. Dindo
D. Arnel
MARKED ANSWER B. Nonoy
WHY Nonoy is right. The clues give Dindo → Arnel → Nonoy → Analyn, so Nonoy is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Dindo → Arnel → Nonoy → Analyn.

### 262 | CIVIO-ANA-ANALOGY-FUNCTION-000263
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Find the pair whose link matches the link between "author" and "novel".
A. page : chapter
B. composer : song
C. poem : poet
D. reader : book
MARKED ANSWER B. composer : song
WHY "composer : song" is right. It has the same link, maker : what they make, in the same order.
SHORTCUT Make a sentence for the stem: "author is to novel" as maker : what they make. Test each choice in that sentence.

### 263 | CIVIO-ANA-SYMBOL-SERIES-000264
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What comes next in the series?  DM, GN, JO, MP, ___
A. PQ
B. NQ
C. PY
D. QP
MARKED ANSWER A. PQ
WHY PQ is right: M + 3 = P and P + 1 = Q.
SHORTCUT Split each pair. First letters: D, G, J, M (jump +3). Second letters: M, N, O, P (jump +1). Move each one more step.

### 264 | CIVIO-ANA-SYMBOL-SERIES-000265
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In a certain code, PERMIT is written as QFSNJU. How is VOTER written in the same code?
A. WPUFS
B. UNSDQ
C. XQVGT
D. WPUFR
MARKED ANSWER A. WPUFS
WHY WPUFS is right: each letter of VOTER moved 1 place forward.
SHORTCUT Compare the first letters: P became Q. That is 1 place forward. Check one more letter, then shift every letter of VOTER the same way.

### 265 | CIVIO-ANA-CONCLUSION-000266
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Four staff members are compared. Lourdes scored higher than Nestor. Bong scored higher than Bea. Nestor scored higher than Bong. Who is second in the order (counting from the one who got the highest score)?
A. Lourdes
B. Bong
C. Bea
D. Nestor
MARKED ANSWER D. Nestor
WHY Nestor is right. The clues give Lourdes → Nestor → Bong → Bea, so Nestor is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Lourdes → Nestor → Bong → Bea.

### 266 | CIVIO-VEN-SENT-COMP-WORD-000267
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The vendors ____ the new rule because it raised their fees.
A. supposed
B. opposite
C. supported
D. opposed
MARKED ANSWER D. opposed
WHY "opposed" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 267 | CIVIO-VEN-WORD-MEANING-000268
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is closest in meaning to the word in capital letters?  DILIGENT
A. diluted
B. delicate
C. hard-working
D. lazy
MARKED ANSWER C. hard-working
WHY "hard-working" is right. "Diligent" means hard-working.
SHORTCUT Make a short sentence with "diligent", then swap in each choice. Watch for words that only look or sound like "diligent".

### 268 | CIVIO-VEN-WORD-MEANING-000269
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What does the phrase in capital letters mean?  Let us CALL IT A DAY and finish tomorrow.
A. quit the job
B. work all night
C. stop working for now
D. name the date
MARKED ANSWER C. stop working for now
WHY "stop working for now" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 269 | CIVIO-VEN-ERROR-AGREE-000270
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The list of approved applicants ____ to be checked again before Friday.
A. need
B. to need
C. needing
D. needs
MARKED ANSWER D. needs
WHY "needs" is right: "The list" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The list ____". The subject is singular, so use the singular verb.

### 270 | CIVIO-VEN-ERROR-TENSE-000271
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the correct verb: Tomorrow, Liza ____ the relief goods.
A. will have delivered
B. has delivered
C. delivered
D. will deliver
MARKED ANSWER D. will deliver
WHY "will deliver" is right: the simple future matches "Tomorrow".
SHORTCUT Find the time signal first: "Tomorrow". It calls for the simple future.

### 271 | CIVIO-VEN-SENT-COMP-WORD-000272
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: Please comply ____ the dress code.
A. at
B. to
C. with
D. on
MARKED ANSWER C. with
WHY "with" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 272 | CIVIO-VEN-WORD-MEANING-000273
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What does the phrase in capital letters mean?  The mayor said the new road will COST AN ARM AND A LEG.
A. cause injuries
B. be cheap
C. be very expensive
D. never be built
MARKED ANSWER C. be very expensive
WHY "be very expensive" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 273 | CIVIO-VEN-SENT-COMP-WORD-000274
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The meeting will start ____ 9 a.m. on Monday.
A. at
B. on
C. for
D. in
MARKED ANSWER A. at
WHY "at" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 274 | CIVIO-VEN-ERROR-TENSE-000275
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the correct verb: Right now, Cora ____ the census forms.
A. encoded
B. will have encoded
C. encodes
D. is encoding
MARKED ANSWER D. is encoding
WHY "is encoding" is right: the present progressive matches "Right now".
SHORTCUT Find the time signal first: "Right now". It calls for the present progressive.

### 275 | CIVIO-VEN-ERROR-AGREE-000276
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The group of farmers ____ asked for new seedlings.
A. to have
B. having
C. have
D. has
MARKED ANSWER D. has
WHY "has" is right: "The group" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The group ____". The subject is singular, so use the singular verb.

### 276 | CIVIO-VEN-SENT-COMP-WORD-000277
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The typhoon left the road ____, so the trucks had to wait.
A. impassable
B. passable
C. impossible
D. passing
MARKED ANSWER A. impassable
WHY "impassable" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 277 | CIVIO-VEN-ERROR-TENSE-000278
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the correct verb: By the end of the year, Ramon ____ the leave forms.
A. reviewed
B. is reviewing
C. has reviewed
D. will have reviewed
MARKED ANSWER D. will have reviewed
WHY "will have reviewed" is right: the future perfect matches "By the end of the year".
SHORTCUT Find the time signal first: "By the end of the year". It calls for the future perfect.

### 278 | CIVIO-VEN-ERROR-TENSE-000279
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the correct verb: Two days ago, Jun-jun ____ the attendance sheets.
A. has checked
B. will check
C. will have checked
D. checked
MARKED ANSWER D. checked
WHY "checked" is right: the simple past matches "Two days ago".
SHORTCUT Find the time signal first: "Two days ago". It calls for the simple past.

### 279 | CIVIO-VEN-WORD-MEANING-000280
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is closest in meaning to the word in capital letters?  VACANT
A. occupied
B. vague
C. empty
D. vacation
MARKED ANSWER C. empty
WHY "empty" is right. "Vacant" means empty.
SHORTCUT Make a short sentence with "vacant", then swap in each choice. Watch for words that only look or sound like "vacant".

### 280 | CIVIO-VEN-SENT-COMP-WORD-000281
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The chief asked Ramon and ____ to stay late.
A. us
B. ours
C. ourselves
D. we
MARKED ANSWER A. us
WHY "us" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 281 | CIVIO-VEN-ERROR-AGREE-000282
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The leader of the volunteers ____ asked for more trash bags.
A. have
B. having
C. has
D. to have
MARKED ANSWER C. has
WHY "has" is right: "The leader" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The leader ____". The subject is singular, so use the singular verb.

### 282 | CIVIO-VEN-SENT-COMP-PHRASAL-000283
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the phrase that best completes the sentence: Volunteers ____ food packs to the evacuees.
A. gave up
B. gave out
C. gave off
D. gave in
MARKED ANSWER B. gave out
WHY "gave out" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 283 | CIVIO-VEN-ERROR-AGREE-000284
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: Neither of the drivers ____ the new route.
A. to know
B. knows
C. knowing
D. know
MARKED ANSWER B. knows
WHY "knows" is right: "Neither" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "Neither ____". The subject is singular, so use the singular verb.

### 284 | CIVIO-VEN-RC-VOCAB-000285
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  Water supply will be RESTORED by evening.
A. repainted
B. stored again
C. brought back
D. cut off
MARKED ANSWER C. brought back
WHY "brought back" is right: it is the sense of "restored" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "restored".

### 285 | CIVIO-VEN-SENT-COMP-WORD-000286
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Choose the word that best completes the sentence: The new rules apply to both you and ____.
A. they
B. themselves
C. them
D. theirs
MARKED ANSWER C. them
WHY "them" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 286 | CIVIO-CLR-SPELL-WRONG-000287
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  miscellaneous | receve | calendar | questionnaire
A. miscellaneous
B. receve
C. calendar
D. questionnaire
MARKED ANSWER B. receve
WHY "receve" is misspelled: it drops a letter. The correct spelling is "receive".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 287 | CIVIO-CLR-FILE-POSITION-000288
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In alphabetical filing, which name is filed LAST?  Engr. Rodrigo E. Pedro | Maria P. Rivera | Engr. Carlos B. Cruz | Victoria G. Aquino
A. Victoria G. Aquino
B. Maria P. Rivera
C. Engr. Rodrigo E. Pedro
D. Engr. Carlos B. Cruz
MARKED ANSWER B. Maria P. Rivera
WHY "Maria P. Rivera" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Victoria G. Aquino → AQUINO, Victoria; Engr. Carlos B. Cruz → CRUZ, Carlos; Engr. Rodrigo E. Pedro → PEDRO, Rodrigo; Maria P. Rivera → RIVERA, Maria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 288 | CIVIO-CLR-SPELL-WRONG-000289
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  privilege | irrelevant | vacuum | commttee
A. privilege
B. irrelevant
C. vacuum
D. commttee
MARKED ANSWER D. commttee
WHY "commttee" is misspelled: it drops a letter. The correct spelling is "committee".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 289 | CIVIO-CLR-FILE-POSITION-000290
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In alphabetical filing, which name is filed FIRST?  Nora A. Salazar | Lourdes G. Austria | Dr. Elena T. Del Rosario | Eduardo D. Garcia-Lopez
A. Nora A. Salazar
B. Lourdes G. Austria
C. Eduardo D. Garcia-Lopez
D. Dr. Elena T. Del Rosario
MARKED ANSWER B. Lourdes G. Austria
WHY "Lourdes G. Austria" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Lourdes G. Austria → AUSTRIA, Lourdes; Dr. Elena T. Del Rosario → DELROSARIO, Elena; Eduardo D. Garcia-Lopez → GARCIALOPEZ, Eduardo; Nora A. Salazar → SALAZAR, Nora.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 290 | CIVIO-CLR-SPELL-WRONG-000291
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  mischevous | requisition | possession | rhythm
A. mischevous
B. requisition
C. possession
D. rhythm
MARKED ANSWER A. mischevous
WHY "mischevous" is misspelled: it drops a letter. The correct spelling is "mischievous".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 291 | CIVIO-CLR-SPELL-WRONG-000292
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  occasionally | accommodate | indepndence | parliament
A. occasionally
B. accommodate
C. indepndence
D. parliament
MARKED ANSWER C. indepndence
WHY "indepndence" is misspelled: it drops a letter. The correct spelling is "independence".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 292 | CIVIO-CLR-SPELL-WRONG-000293
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  believe | occsionally | jewelry | license
A. believe
B. occsionally
C. jewelry
D. license
MARKED ANSWER B. occsionally
WHY "occsionally" is misspelled: it drops a letter. The correct spelling is "occasionally".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 293 | CIVIO-CLR-FILE-POSITION-000294
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In alphabetical filing, which name is filed FIRST?  Gloria E. De Leon | Engr. Ana C. Santos | Victoria L. Pedro | Atty. Evelyn A. Del Mundo
A. Gloria E. De Leon
B. Victoria L. Pedro
C. Atty. Evelyn A. Del Mundo
D. Engr. Ana C. Santos
MARKED ANSWER A. Gloria E. De Leon
WHY "Gloria E. De Leon" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Gloria E. De Leon → DELEON, Gloria; Atty. Evelyn A. Del Mundo → DELMUNDO, Evelyn; Victoria L. Pedro → PEDRO, Victoria; Engr. Ana C. Santos → SANTOS, Ana.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 294 | CIVIO-CLR-SPELL-RIGHT-000295
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is spelled correctly?  recept | receipt | recipt | reciept
A. recept
B. receipt
C. recipt
D. reciept
MARKED ANSWER B. receipt
WHY "receipt" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 295 | CIVIO-CLR-SPELL-WRONG-000296
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  requisition | guarantee | privilege | atendance
A. requisition
B. guarantee
C. privilege
D. atendance
MARKED ANSWER D. atendance
WHY "atendance" is misspelled: it doubles or undoubles a consonant. The correct spelling is "attendance".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 296 | CIVIO-CLR-FILE-POSITION-000297
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In alphabetical filing, which name is filed LAST?  Cristina R. Castillo | Atty. Benito T. Del Mundo | Ramon E. Rosario | Gloria N. Dela Torre
A. Cristina R. Castillo
B. Gloria N. Dela Torre
C. Ramon E. Rosario
D. Atty. Benito T. Del Mundo
MARKED ANSWER C. Ramon E. Rosario
WHY "Ramon E. Rosario" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Cristina R. Castillo → CASTILLO, Cristina; Gloria N. Dela Torre → DELATORRE, Gloria; Atty. Benito T. Del Mundo → DELMUNDO, Benito; Ramon E. Rosario → ROSARIO, Ramon.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 297 | CIVIO-CLR-SPELL-RIGHT-000298
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is spelled correctly?  recommend | recommnd | recmmend | recomend
A. recommend
B. recommnd
C. recmmend
D. recomend
MARKED ANSWER A. recommend
WHY "recommend" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 298 | CIVIO-CLR-FILE-POSITION-000299
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
In alphabetical filing, which name is filed FIRST?  Atty. Corazon V. Leon | Alfredo P. Garcia-Lopez | Evelyn B. Pascual | Nora N. Cruz-Manalo
A. Evelyn B. Pascual
B. Atty. Corazon V. Leon
C. Nora N. Cruz-Manalo
D. Alfredo P. Garcia-Lopez
MARKED ANSWER C. Nora N. Cruz-Manalo
WHY "Nora N. Cruz-Manalo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Nora N. Cruz-Manalo → CRUZMANALO, Nora; Alfredo P. Garcia-Lopez → GARCIALOPEZ, Alfredo; Atty. Corazon V. Leon → LEON, Corazon; Evelyn B. Pascual → PASCUAL, Evelyn.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 299 | CIVIO-CLR-SPELL-WRONG-000300
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  existence | convenience | embarrass | licnse
A. existence
B. convenience
C. embarrass
D. licnse
MARKED ANSWER D. licnse
WHY "licnse" is misspelled: it drops a letter. The correct spelling is "license".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 300 | CIVIO-CLR-SPELL-WRONG-000301
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which word is misspelled?  attendance | inculate | appropriation | acknowledgment
A. attendance
B. inculate
C. appropriation
D. acknowledgment
MARKED ANSWER B. inculate
WHY "inculate" is misspelled: it drops a letter. The correct spelling is "inoculate".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 301 | CIVIO-GI-TERM-MATCH-000302
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
What is the short title of R.A. 6713?
A. Civil Service Law
B. Ease of Doing Business Act
C. Code of Conduct and Ethical Standards for Public Officials and Employees
D. Anti-Graft and Corrupt Practices Act
MARKED ANSWER C. Code of Conduct and Ethical Standards for Public Officials and Employees
WHY "Code of Conduct and Ethical Standards for Public Officials and Employees" is right. R.A. 6713, Sec. 2 says: "Code of Conduct and Ethical Standards for Public Officials and Employees".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 2. That is R.A. 6713; the Anti-Graft law is R.A. 3019.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 302 | CIVIO-GI-TERM-MATCH-000303
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Under the 1987 Constitution, may a civil service officer or employee engage in partisan political campaigns?
A. Yes, if on leave
B. No, directly or indirectly
C. Yes, outside office hours
D. Only for local elections
MARKED ANSWER B. No, directly or indirectly
WHY "No, directly or indirectly" is right. Art. IX-B, Sec. 2(4) says: "shall engage, directly or indirectly, in any electioneering or partisan political campaign".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 2(4). Civil servants may not campaign, directly or indirectly.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 303 | CIVIO-GI-WHO-HOLDS-POWER-000304
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which constitutional body examines, audits and settles accounts of government revenues and expenditures?
A. Commission on Audit
B. Civil Service Commission
C. Department of Budget and Management
D. Office of the Ombudsman
MARKED ANSWER A. Commission on Audit
WHY "Commission on Audit" is right. Art. IX-D, Sec. 2(1) says: "The Commission on Audit shall have the power, authority, and duty to examine, audit, and settle all accounts".
SHORTCUT Tie the fact to its section: Art. IX-D, Sec. 2(1). COA audits government funds.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 304 | CIVIO-GI-TERM-MATCH-000305
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which of these is NOT a ground for impeachment under the 1987 Constitution?
A. Graft and corruption
B. Poor performance rating
C. Betrayal of public trust
D. Culpable violation of the Constitution
MARKED ANSWER B. Poor performance rating
WHY "Poor performance rating" is right. Art. XI, Sec. 2 says: "culpable violation of the Constitution, treason, bribery, graft and corruption, other high crimes, or betrayal of public trust".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 2. The grounds are listed in Sec. 2; poor performance is not one.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 305 | CIVIO-GI-DEADLINE-NUMBER-000306
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
How many members does the Commission on Elections have, counting the Chairman?
A. 9
B. 3
C. 5
D. 7
MARKED ANSWER D. 7
WHY "7" is right. Art. IX-C, Sec. 1(1) says: "composed of a Chairman and six Commissioners".
SHORTCUT Tie the fact to its section: Art. IX-C, Sec. 1(1). COMELEC: a Chairman and six Commissioners.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 306 | CIVIO-GI-DEADLINE-NUMBER-000307
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Within how many hours after a proclamation of martial law must the President report to Congress?
A. 24 hours
B. 48 hours
C. 7 days
D. 72 hours
MARKED ANSWER B. 48 hours
WHY "48 hours" is right. Art. VII, Sec. 18 says: "Within forty-eight hours from the proclamation of martial law".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 18. The report to Congress is due within 48 hours.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 307 | CIVIO-GI-DEADLINE-NUMBER-000308
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Under R.A. 6713, what is the maximum fine that may be imposed as an administrative penalty for violating the Act?
A. Six months' salary
B. One year's salary
C. Three months' salary
D. ₱10,000
MARKED ANSWER A. Six months' salary
WHY "Six months' salary" is right. R.A. 6713, Sec. 11 says: "fine not exceeding the equivalent of six (6) months' salary".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 11. Up to six months' salary, or suspension up to one year, or removal.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 308 | CIVIO-GI-TERM-MATCH-000309
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Under R.A. 6713, which norm of conduct requires officials to perform duties with the highest degree of excellence, professionalism, intelligence and skill?
A. Justness and sincerity
B. Simple living
C. Professionalism
D. Political neutrality
MARKED ANSWER C. Professionalism
WHY "Professionalism" is right. R.A. 6713, Sec. 4(A) says: "highest degree of excellence, professionalism, intelligence and skill".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). This is the norm of professionalism, Sec. 4(A)(b).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 309 | CIVIO-GI-TERM-MATCH-000310
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Which officials are removable from office by impeachment?
A. The President, Vice-President, Supreme Court Members, Constitutional Commission members and the Ombudsman
B. Only the President
C. All elected officials, including mayors
D. All Cabinet members and senators
MARKED ANSWER A. The President, Vice-President, Supreme Court Members, Constitutional Commission members and the Ombudsman
WHY "The President, Vice-President, Supreme Court Members, Constitutional Commission members and the Ombudsman" is right. Art. XI, Sec. 2 says: "the Members of the Supreme Court, the Members of the Constitutional Commissions, and the Ombudsman may be removed from office on impeachment".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 2. These are the impeachable officers.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 310 | CIVIO-GI-WHO-HOLDS-POWER-000311
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-004.json
STEM
Under the 1987 Constitution, may a public officer accept a title of nobility from a foreign government without the consent of Congress?
A. Yes, with the President's consent alone
B. Yes, after retirement only
C. Yes, if it is honorary
D. No
MARKED ANSWER D. No
WHY "No" is right. Art. IX-B, Sec. 8 says: "accept without the consent of the Congress, any present, emolument, office, or title of any kind from any foreign government".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 8. Congress must consent to any foreign title, gift or office.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 311 | CIVIO-NUM-WP-RATIO-000312
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Teresa and Rogelio will share ₱36,000 of allowance fund in the ratio 5 : 7. How much is Rogelio's share?
A. ₱3,000
B. ₱5,142.86
C. ₱21,000
D. ₱15,000
MARKED ANSWER C. ₱21,000
WHY ₱21,000 is right: 7 × ₱3,000 = ₱21,000. Check: ₱15,000 + ₱21,000 = ₱36,000.
SHORTCUT Add the ratio numbers to get equal parts: 5 + 7 = 12. One part = ₱36,000 ÷ 12 = ₱3,000. Then multiply by the parts you need.

### 312 | CIVIO-NUM-WP-RATE-000313
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Rogelio can sort a sack of mail in 36 hours. Kimberly can do the same job in 12 hours. Working together, how long will they take?
A. 48 hours
B. 24 hours
C. 6.6667 hours
D. 9 hours
MARKED ANSWER D. 9 hours
WHY 9 hours is right. Check: in 9 hours, Rogelio does 9/36 and Kimberly does 9/12; together that is 1 whole job.
SHORTCUT Per hour, Rogelio does 1/36 and Kimberly does 1/12. Together: 1/36 + 1/12 = 1/9. So the whole job takes 9 hours.

### 313 | CIVIO-NUM-FRAC-DEC-000314
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A barangay had 180 notebooks. It gave out 1/4 of them on Monday and 3/5 of the remaining notebooks on Tuesday. How many are left?
A. 81
B. 54
C. 135
D. 27
MARKED ANSWER B. 54
WHY 54 is right. Check: 45 + 81 + 54 = 180.
SHORTCUT Go day by day. Monday: 1/4 of 180 = 45, so 135 left. Tuesday: 3/5 of 135 = 81, so 135 − 81 = 54 left.

### 314 | CIVIO-NUM-WP-GEOM-000315
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A rectangular drying yard is 14 m long and 18 m wide. A fence costs ₱25 per meter. How much will it cost to put the fence around the whole drying yard?
A. ₱6,300
B. ₱64
C. ₱800
D. ₱1,600
MARKED ANSWER D. ₱1,600
WHY ₱1,600 is right: 64 m × ₱25 = ₱1,600.
SHORTCUT Around = 2 × (14 + 18) = 64 m. Cost = 64 × ₱25.

### 315 | CIVIO-NUM-SEQ-DIFF-000316
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which number should come next?  11, 16, 22, 29, 37, ___
A. 42
B. 47
C. 45
D. 46
MARKED ANSWER D. 46
WHY 46 is right: 37 + 9 = 46.
SHORTCUT Write the jumps under the list: +5, +6, +7, +8. Each jump is 1 more than the one before. So the next jump is +9.

### 316 | CIVIO-NUM-WP-RATE-000317
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Aileen can paint a classroom in 6 hours. Ramon can do the same job in 12 hours. Working together, how long will they take?
A. 18 hours
B. 4 hours
C. 9 hours
D. 15 minutes
MARKED ANSWER B. 4 hours
WHY 4 hours is right. Check: in 4 hours, Aileen does 4/6 and Ramon does 4/12; together that is 1 whole job.
SHORTCUT Per hour, Aileen does 1/6 and Ramon does 1/12. Together: 1/6 + 1/12 = 1/4. So the whole job takes 4 hours.

### 317 | CIVIO-NUM-WP-GEOM-000318
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A rectangular drying yard is 38 m long and 18 m wide. A chain-link fence costs ₱120 per meter. How much will it cost to put the chain-link fence around the whole drying yard?
A. ₱6,720
B. ₱112
C. ₱13,440
D. ₱82,080
MARKED ANSWER C. ₱13,440
WHY ₱13,440 is right: 112 m × ₱120 = ₱13,440.
SHORTCUT Around = 2 × (38 + 18) = 112 m. Cost = 112 × ₱120.

### 318 | CIVIO-NUM-OPS-ORDER-000319
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What is the value of 8 + 5 × 2 − 3?
A. 12
B. 3
C. 23
D. 15
MARKED ANSWER D. 15
WHY 15 is right: 8 + 10 = 18, and 18 − 3 = 15.
SHORTCUT Circle the × first: 5 × 2 = 10. Then go left to right: 8 + 10 − 3.

### 319 | CIVIO-NUM-WP-RATIO-000320
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Paolo and Lourdes will share ₱2,500 of allowance fund in the ratio 2 : 3. How much is Lourdes's share?
A. ₱1,000
B. ₱833.33
C. ₱500
D. ₱1,500
MARKED ANSWER D. ₱1,500
WHY ₱1,500 is right: 3 × ₱500 = ₱1,500. Check: ₱1,000 + ₱1,500 = ₱2,500.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 3 = 5. One part = ₱2,500 ÷ 5 = ₱500. Then multiply by the parts you need.

### 320 | CIVIO-NUM-OPS-ORDER-000321
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What is the value of 9 + 4 × 5 − 9?
A. 9
B. 56
C. -7
D. 20
MARKED ANSWER D. 20
WHY 20 is right: 9 + 20 = 29, and 29 − 9 = 20.
SHORTCUT Circle the × first: 4 × 5 = 20. Then go left to right: 9 + 20 − 9.

### 321 | CIVIO-NUM-OPS-ORDER-000322
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What is the value of 8 + 8 × 8 − 3?
A. 48
B. 69
C. 125
D. 21
MARKED ANSWER B. 69
WHY 69 is right: 8 + 64 = 72, and 72 − 3 = 69.
SHORTCUT Circle the × first: 8 × 8 = 64. Then go left to right: 8 + 64 − 3.

### 322 | CIVIO-NUM-WP-PCT-CHANGE-000323
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A office chair is priced at ₱800. It is sold at 35% off. How much does a buyer pay?
A. ₱765
B. ₱520
C. ₱280
D. ₱1,080
MARKED ANSWER B. ₱520
WHY ₱520 is right. Check: discount ₱280; ₱800 − ₱280 = ₱520.
SHORTCUT Pay 65% of the price: ₱800 × 0.65 = ₱520.

### 323 | CIVIO-NUM-WP-PCT-CHANGE-000324
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A market stall sold a set of school uniforms for ₱250. It raised the price by 20%. Later, it lowered the new price by 10%. What is the final price?
A. ₱275
B. ₱270
C. ₱324
D. ₱300
MARKED ANSWER B. ₱270
WHY ₱270 is right. Check: 250 × 1.2 = 300, and 300 × 0.9 = 270.
SHORTCUT Do one change at a time. ₱250 up 20% is ₱250 + ₱50 = ₱300. Then 10% of ₱300 is ₱30, so ₱300 − ₱30 = ₱270.

### 324 | CIVIO-NUM-WP-RATE-000325
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Ramon can label the census boxes in 10 hours. Rhea can do the same job in 40 hours. Working together, how long will they take?
A. 8 hours
B. 50 hours
C. 25 hours
D. 7.5 hours
MARKED ANSWER A. 8 hours
WHY 8 hours is right. Check: in 8 hours, Ramon does 8/10 and Rhea does 8/40; together that is 1 whole job.
SHORTCUT Per hour, Ramon does 1/10 and Rhea does 1/40. Together: 1/10 + 1/40 = 1/8. So the whole job takes 8 hours.

### 325 | CIVIO-NUM-WP-PCT-CHANGE-000326
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A farmer borrows ₱40,000 at 12% simple interest per year. How much interest is due after 2 years and 6 months?
A. ₱12,480
B. ₱52,000
C. ₱9,600
D. ₱12,000
MARKED ANSWER D. ₱12,000
WHY ₱12,000 is right. Check: 40,000 × 0.12 × 2.5 = 12,000.
SHORTCUT Find one year first: 12% of ₱40,000 = ₱4,800. Time is 2.5 years. Multiply: 2.5 × ₱4,800 = ₱12,000.

### 326 | CIVIO-NUM-WP-RATIO-000327
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Datu and Arnel will share ₱9,000 of cleanup fund in the ratio 4 : 5. How much is Arnel's share?
A. ₱1,800
B. ₱5,000
C. ₱1,000
D. ₱4,000
MARKED ANSWER B. ₱5,000
WHY ₱5,000 is right: 5 × ₱1,000 = ₱5,000. Check: ₱4,000 + ₱5,000 = ₱9,000.
SHORTCUT Add the ratio numbers to get equal parts: 4 + 5 = 9. One part = ₱9,000 ÷ 9 = ₱1,000. Then multiply by the parts you need.

### 327 | CIVIO-NUM-WP-PCT-CHANGE-000328
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A market stall sold a tank of LPG for ₱750. It raised the price by 20%. Later, it lowered the new price by 40%. What is the final price?
A. ₱540
B. ₱600
C. ₱648
D. ₱900
MARKED ANSWER A. ₱540
WHY ₱540 is right. Check: 750 × 1.2 = 900, and 900 × 0.6 = 540.
SHORTCUT Do one change at a time. ₱750 up 20% is ₱750 + ₱150 = ₱900. Then 40% of ₱900 is ₱360, so ₱900 − ₱360 = ₱540.

### 328 | CIVIO-NUM-WP-PCT-CHANGE-000329
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A hardware store sold a tank of LPG for ₱800. It raised the price by 40%. Later, it lowered the new price by 25%. What is the final price?
A. ₱920
B. ₱840
C. ₱1,120
D. ₱1,176
MARKED ANSWER B. ₱840
WHY ₱840 is right. Check: 800 × 1.4 = 1,120, and 1,120 × 0.75 = 840.
SHORTCUT Do one change at a time. ₱800 up 40% is ₱800 + ₱320 = ₱1,120. Then 25% of ₱1,120 is ₱280, so ₱1,120 − ₱280 = ₱840.

### 329 | CIVIO-NUM-WP-PCT-CHANGE-000330
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A government employee borrows ₱50,000 at 6% simple interest per year. How much interest is due after 2 years?
A. ₱60,000
B. ₱6,000
C. ₱3,000
D. ₱56,000
MARKED ANSWER B. ₱6,000
WHY ₱6,000 is right. Check: 50,000 × 0.06 × 2 = 6,000.
SHORTCUT Find one year first: 6% of ₱50,000 = ₱3,000. Time is 2 years. Multiply: 2 × ₱3,000 = ₱6,000.

### 330 | CIVIO-NUM-WP-AVERAGE-000331
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
The average years of service of the 8 clerks in the agriculture office is 10 years. One more person, with 19 years, joins them. What is the new average years of service?
A. 14.5 years
B. 99 years
C. 11 years
D. 11.12 years
MARKED ANSWER C. 11 years
WHY 11 years is right. Long way: 8 × 10 = 80; + 19 = 99; ÷ 9 = 11.
SHORTCUT The new person is 19 − 10 = 9 above the old average. Share that among all 9 people: 9 ÷ 9 = 1. Add it: 10 + 1 = 11.

### 331 | CIVIO-NUM-SEQ-DIFF-000332
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What number comes next in the series?  11, 15, 21, 29, 39, ___
A. 49
B. 51
C. 43
D. 53
MARKED ANSWER B. 51
WHY 51 is right: 39 + 12 = 51.
SHORTCUT Write the jumps under the list: +4, +6, +8, +10. Each jump is 2 more than the one before. So the next jump is +12.

### 332 | CIVIO-NUM-FRAC-DEC-000333
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A barangay had 1440 face masks. It gave out 2/5 of them on Monday and 1/4 of the remaining face masks on Tuesday. How many are left?
A. 648
B. 864
C. 216
D. 504
MARKED ANSWER A. 648
WHY 648 is right. Check: 576 + 216 + 648 = 1440.
SHORTCUT Go day by day. Monday: 2/5 of 1440 = 576, so 864 left. Tuesday: 1/4 of 864 = 216, so 864 − 216 = 648 left.

### 333 | CIVIO-NUM-SEQ-MULT-000334
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What number comes next?  1, 4, 10, 22, 46, ___
A. 70
B. 92
C. 96
D. 94
MARKED ANSWER D. 94
WHY 94 is right: 46 × 2 = 92, then + 2 gives 94.
SHORTCUT Test "times 2, then + 2" on the first numbers: 1 × 2 + 2 = 4; 4 × 2 + 2 = 10. It works, so use it on 46.

### 334 | CIVIO-NUM-SEQ-MULT-000335
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What number comes next?  5, 13, 37, 109, 325, ___
A. 541
B. 971
C. 973
D. 975
MARKED ANSWER C. 973
WHY 973 is right: 325 × 3 = 975, then − 2 gives 973.
SHORTCUT Test "times 3, then − 2" on the first numbers: 5 × 3 − 2 = 13; 13 × 3 − 2 = 37. It works, so use it on 325.

### 335 | CIVIO-NUM-SEQ-DIFF-000336
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What number comes next in the series?  1, 6, 13, 22, 33, ___
A. 44
B. 48
C. 38
D. 46
MARKED ANSWER D. 46
WHY 46 is right: 33 + 13 = 46.
SHORTCUT Write the jumps under the list: +5, +7, +9, +11. Each jump is 2 more than the one before. So the next jump is +13.

### 336 | CIVIO-NUM-SEQ-MULT-000337
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What number comes next?  4, 7, 13, 25, 49, ___
A. 96
B. 98
C. 97
D. 73
MARKED ANSWER C. 97
WHY 97 is right: 49 × 2 = 98, then − 1 gives 97.
SHORTCUT Test "times 2, then − 1" on the first numbers: 4 × 2 − 1 = 7; 7 × 2 − 1 = 13. It works, so use it on 49.

### 337 | CIVIO-NUM-WP-AVERAGE-000338
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
The average age of the 5 drivers in the public market office is 26 years. One more person, with 50 years, joins them. What is the new average age?
A. 30 years
B. 180 years
C. 38 years
D. 30.8 years
MARKED ANSWER A. 30 years
WHY 30 years is right. Long way: 5 × 26 = 130; + 50 = 180; ÷ 6 = 30.
SHORTCUT The new person is 50 − 26 = 24 above the old average. Share that among all 6 people: 24 ÷ 6 = 4. Add it: 26 + 4 = 30.

### 338 | CIVIO-NUM-WP-AVERAGE-000339
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
The average years of service of the 6 staff members in the public market office is 11 years. One more person, with 18 years, joins them. What is the new average years of service?
A. 12 years
B. 14.5 years
C. 84 years
D. 12.17 years
MARKED ANSWER A. 12 years
WHY 12 years is right. Long way: 6 × 11 = 66; + 18 = 84; ÷ 7 = 12.
SHORTCUT The new person is 18 − 11 = 7 above the old average. Share that among all 7 people: 7 ÷ 7 = 1. Add it: 11 + 1 = 12.

### 339 | CIVIO-NUM-WP-PCT-CHANGE-000340
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A backpack is priced at ₱800. It is sold at 15% off. How much does a buyer pay?
A. ₱920
B. ₱680
C. ₱785
D. ₱120
MARKED ANSWER B. ₱680
WHY ₱680 is right. Check: discount ₱120; ₱800 − ₱120 = ₱680.
SHORTCUT Pay 85% of the price: ₱800 × 0.85 = ₱680.

### 340 | CIVIO-NUM-WP-PCT-CHANGE-000341
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
A backpack is priced at ₱480. It is sold at 35% off. How much does a buyer pay?
A. ₱648
B. ₱168
C. ₱312
D. ₱445
MARKED ANSWER C. ₱312
WHY ₱312 is right. Check: discount ₱168; ₱480 − ₱168 = ₱312.
SHORTCUT Pay 65% of the price: ₱480 × 0.65 = ₱312.

### 341 | CIVIO-ANA-SYLLOGISM-000342
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Assume these are true: none of the public buildings are items under quarantine, and every one of the libraries is among the public buildings. What can be concluded for certain?
A. No insured properties are items under quarantine.
B. No libraries are items under quarantine.
C. Some libraries are items under quarantine.
D. All public buildings are libraries.
MARKED ANSWER B. No libraries are items under quarantine.
WHY "No libraries are items under quarantine." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the libraries circle inside public buildings. The "items under quarantine" circle sits outside public buildings, so it is outside libraries too.

### 342 | CIVIO-ANA-DI-TABLE-000343
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Supply use of staplers by office (Health: Apr 48, May 24, Jun 12; Records: Apr 30, May 38, Jun 24; Library: Apr 28, May 34, Jun 68). In Jun, how many more did Library use than Records?
A. 44
B. 92
C. 38
D. 2
MARKED ANSWER A. 44
WHY 44 is right: 68 − 24 = 44.
SHORTCUT Go to the Jun column: Records 24, Library 68. Subtract the smaller from the larger.

### 343 | CIVIO-ANA-SYMBOL-SERIES-000344
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What comes next in the series?  IK, ML, QM, UN, ___
A. VO
B. YA
C. OY
D. YO
MARKED ANSWER D. YO
WHY YO is right: U + 4 = Y and N + 1 = O.
SHORTCUT Split each pair. First letters: I, M, Q, U (jump +4). Second letters: K, L, M, N (jump +1). Move each one more step.

### 344 | CIVIO-ANA-CONCLUSION-000345
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Four staff members are compared. Marites finished the report earlier than Grace. Efren finished the report earlier than Marites. Grace finished the report earlier than Jomar. Who is third in the order (counting from the one who finished first)?
A. Marites
B. Grace
C. Efren
D. Jomar
MARKED ANSWER B. Grace
WHY Grace is right. The clues give Efren → Marites → Grace → Jomar, so Grace is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Efren → Marites → Grace → Jomar.

### 345 | CIVIO-ANA-CONCLUSION-000346
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Four staff members are compared. Joy finished the report earlier than Mang Jun. Mang Jun finished the report earlier than Marites. Jun-jun finished the report earlier than Joy. Who is second in the order (counting from the one who finished first)?
A. Marites
B. Jun-jun
C. Joy
D. Mang Jun
MARKED ANSWER C. Joy
WHY Joy is right. The clues give Jun-jun → Joy → Mang Jun → Marites, so Joy is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Jun-jun → Joy → Mang Jun → Marites.

### 346 | CIVIO-ANA-DI-TABLE-000347
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Supply use of envelopes (boxes) by office (Library: Jul 76, Aug 32, Sep 80; Records: Jul 38, Aug 24, Sep 48; Assessor: Jul 70, Aug 14, Sep 66). In Sep, how many more did Assessor use than Records?
A. 18
B. 40
C. 32
D. 114
MARKED ANSWER A. 18
WHY 18 is right: 66 − 48 = 18.
SHORTCUT Go to the Sep column: Assessor 66, Records 48. Subtract the smaller from the larger.

### 347 | CIVIO-ANA-SYLLOGISM-000348
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Assume these are true: every one of the memos is among the official papers, and every one of the official papers is among the records. What can be concluded for certain?
A. Some records are not official papers.
B. No official papers are memos.
C. All records are memos.
D. All memos are records.
MARKED ANSWER D. All memos are records.
WHY "All memos are records." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: memos inside official papers, official papers inside records. So memos sit inside records.

### 348 | CIVIO-ANA-SYMBOL-SERIES-000349
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In a certain code, RECORD is written as PCAMPB. How is PUBLIC written in the same code?
A. NSZJGA
B. MRYIFZ
C. RWDNKE
D. NSZJGC
MARKED ANSWER A. NSZJGA
WHY NSZJGA is right: each letter of PUBLIC moved 2 places back.
SHORTCUT Compare the first letters: R became P. That is 2 places back. Check one more letter, then shift every letter of PUBLIC the same way.

### 349 | CIVIO-ANA-DI-TABLE-000350
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Supply use of bond paper (reams) by office (HR: Jul 58, Aug 62, Sep 40; Cashier: Jul 20, Aug 52, Sep 48; Library: Jul 20, Aug 32, Sep 52). How many did Cashier use in all three months?
A. 146
B. 120
C. 40
D. 72
MARKED ANSWER B. 120
WHY 120 is right: 20 + 52 + 48 = 120.
SHORTCUT Read across the Cashier row only: 20 + 52 + 48.

### 350 | CIVIO-ANA-CONCLUSION-000351
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Four staff members are compared. Jomar finished the report earlier than Cora. Bong finished the report earlier than Jomar. Efren finished the report earlier than Bong. Who is third in the order (counting from the one who finished first)?
A. Jomar
B. Bong
C. Cora
D. Efren
MARKED ANSWER A. Jomar
WHY Jomar is right. The clues give Efren → Bong → Jomar → Cora, so Jomar is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Efren → Bong → Jomar → Cora.

### 351 | CIVIO-ANA-DI-TABLE-000352
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Supply use of folders (packs) by office (Assessor: Apr 22, May 54, Jun 20; Cashier: Apr 32, May 22, Jun 26; HR: Apr 22, May 66, Jun 60). How many did HR use in all three months?
A. 49.3
B. 142
C. 148
D. 88
MARKED ANSWER C. 148
WHY 148 is right: 22 + 66 + 60 = 148.
SHORTCUT Read across the HR row only: 22 + 66 + 60.

### 352 | CIVIO-ANA-ASSUME-I-II-000353
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Statement: Applicants must bring a valid ID so the clerk can confirm who they are.
Assumption I: Any paper with a name on it will do.
Assumption II: A valid ID shows who the holder is.
Which assumption is implicit in the statement?
A. Both I and II
B. Only I
C. Neither I nor II
D. Only II
MARKED ANSWER D. Only II
WHY "Only II" is right. Only assumption II is needed. I ("Any paper with a name on it will do.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 353 | CIVIO-ANA-SYMBOL-SERIES-000354
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What comes next in the series?  FM, JO, NQ, RS, ___
A. VU
B. UV
C. SU
D. VC
MARKED ANSWER A. VU
WHY VU is right: R + 4 = V and S + 2 = U.
SHORTCUT Split each pair. First letters: F, J, N, R (jump +4). Second letters: M, O, Q, S (jump +2). Move each one more step.

### 354 | CIVIO-ANA-DI-TABLE-000355
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Supply use of ballpens (boxes) by office (Assessor: Jan 76, Feb 70, Mar 20; Records: Jan 10, Feb 28, Mar 56; Engineering: Jan 24, Feb 20, Mar 48). In Mar, how many more did Records use than Assessor?
A. 66
B. 76
C. 72
D. 36
MARKED ANSWER D. 36
WHY 36 is right: 56 − 20 = 36.
SHORTCUT Go to the Mar column: Assessor 20, Records 56. Subtract the smaller from the larger.

### 355 | CIVIO-ANA-SYMBOL-SERIES-000356
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What comes next in the series?  DR, FS, HT, JU, ___
A. LZ
B. KV
C. VL
D. LV
MARKED ANSWER D. LV
WHY LV is right: J + 2 = L and U + 1 = V.
SHORTCUT Split each pair. First letters: D, F, H, J (jump +2). Second letters: R, S, T, U (jump +1). Move each one more step.

### 356 | CIVIO-ANA-SYLLOGISM-000357
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Statement 1: Some volunteers are first-time applicants. Statement 2: All volunteers are helpers. Which conclusion follows from both statements?
A. No helpers are first-time applicants.
B. Some helpers are first-time applicants.
C. All helpers are first-time applicants.
D. All first-time applicants are volunteers.
MARKED ANSWER B. Some helpers are first-time applicants.
WHY "Some helpers are first-time applicants." is right. It follows from the two statements with no extra facts.
SHORTCUT The volunteers who are first-time applicants are also helpers. So at least some helpers are first-time applicants.

### 357 | CIVIO-ANA-CONCLUSION-000358
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Four staff members are compared. Mylene encoded more forms than Arnel. Arnel encoded more forms than Nestor. Bea encoded more forms than Mylene. Who is third in the order (counting from the one who encoded the most forms)?
A. Bea
B. Nestor
C. Arnel
D. Mylene
MARKED ANSWER C. Arnel
WHY Arnel is right. The clues give Bea → Mylene → Arnel → Nestor, so Arnel is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Bea → Mylene → Arnel → Nestor.

### 358 | CIVIO-ANA-ANALOGY-PART-000359
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Bee is to hive as ____.
A. honey : bee
B. den : bear
C. bird : nest
D. flower : garden
MARKED ANSWER C. bird : nest
WHY "bird : nest" is right. It has the same link, animal : home, in the same order.
SHORTCUT Make a sentence for the stem: "bee is to hive" as animal : home. Test each choice in that sentence.

### 359 | CIVIO-ANA-ASSUME-I-II-000360
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Statement: To save power, the office will switch off the air conditioners at 5 p.m.
Assumption I: Running the air conditioners uses electricity.
Assumption II: No one works after 5 p.m.
Which assumption is implicit in the statement?
A. Only I
B. Both I and II
C. Only II
D. Neither I nor II
MARKED ANSWER A. Only I
WHY "Only I" is right. Only assumption I is needed. II ("No one works after 5 p.m.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 360 | CIVIO-ANA-SYLLOGISM-000361
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
All volunteers are helpers. No helpers are absentees. Which conclusion must be true?
A. No volunteers are absentees.
B. Some volunteers are absentees.
C. No registered persons are absentees.
D. All helpers are volunteers.
MARKED ANSWER A. No volunteers are absentees.
WHY "No volunteers are absentees." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the volunteers circle inside helpers. The "absentees" circle sits outside helpers, so it is outside volunteers too.

### 361 | CIVIO-ANA-SYLLOGISM-000362
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
All volunteers are helpers. Some volunteers are blood donors. Which conclusion must be true?
A. Some helpers are blood donors.
B. No helpers are blood donors.
C. All helpers are blood donors.
D. All blood donors are volunteers.
MARKED ANSWER A. Some helpers are blood donors.
WHY "Some helpers are blood donors." is right. It follows from the two statements with no extra facts.
SHORTCUT The volunteers who are blood donors are also helpers. So at least some helpers are blood donors.

### 362 | CIVIO-ANA-SYMBOL-SERIES-000363
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What comes next in the series?  GP, IQ, KR, MS, ___
A. OT
B. TO
C. NT
D. OX
MARKED ANSWER A. OT
WHY OT is right: M + 2 = O and S + 1 = T.
SHORTCUT Split each pair. First letters: G, I, K, M (jump +2). Second letters: P, Q, R, S (jump +1). Move each one more step.

### 363 | CIVIO-ANA-SYMBOL-SERIES-000364
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In a certain code, HEALTH is written as GDZKSG. How is MAYOR written in the same code?
A. LZXNR
B. KYWMP
C. LZXNQ
D. NBZPS
MARKED ANSWER C. LZXNQ
WHY LZXNQ is right: each letter of MAYOR moved 1 place back.
SHORTCUT Compare the first letters: H became G. That is 1 place back. Check one more letter, then shift every letter of MAYOR the same way.

### 364 | CIVIO-ANA-DI-TABLE-000365
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Supply use of toner (units) by office (Engineering: Jan 16, Feb 64, Mar 42; Health: Jan 54, Feb 78, Mar 62; Library: Jan 42, Feb 16, Mar 56). How many did Library use in all three months?
A. 58
B. 114
C. 158
D. 38
MARKED ANSWER B. 114
WHY 114 is right: 42 + 16 + 56 = 114.
SHORTCUT Read across the Library row only: 42 + 16 + 56.

### 365 | CIVIO-ANA-ANALOGY-PART-000366
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which pair shows the same relationship as "rice : grain"?
A. field : harvest
B. fruit : mango
C. carrot : vegetable
D. bread : flour
MARKED ANSWER C. carrot : vegetable
WHY "carrot : vegetable" is right. It has the same link, member : group, in the same order.
SHORTCUT Make a sentence for the stem: "rice is to grain" as member : group. Test each choice in that sentence.

### 366 | CIVIO-VEN-SENT-COMP-WORD-000367
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: The officer was praised for her ____; she never took a bribe.
A. honor roll
B. hostility
C. greed
D. honesty
MARKED ANSWER D. honesty
WHY "honesty" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 367 | CIVIO-VEN-SENT-COMP-WORD-000368
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: Heavy rain can ____ the delivery of relief goods.
A. effect
B. affection
C. infect
D. affect
MARKED ANSWER D. affect
WHY "affect" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 368 | CIVIO-VEN-WORD-MEANING-000369
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What does the phrase in capital letters mean?  Her comment HIT THE NAIL ON THE HEAD.
A. hurt someone
B. was rude
C. was exactly right
D. was completely wrong
MARKED ANSWER C. was exactly right
WHY "was exactly right" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 369 | CIVIO-VEN-SENT-COMP-PHRASAL-000370
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the phrase that best completes the sentence: The fire truck had to ____ the road because of the flood.
A. turn back
B. turn in
C. turn over
D. turn up
MARKED ANSWER A. turn back
WHY "turn back" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 370 | CIVIO-VEN-SENT-COMP-WORD-000371
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: The ____ of the school called a parents' meeting.
A. principled
B. principal
C. principally
D. principle
MARKED ANSWER B. principal
WHY "principal" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 371 | CIVIO-VEN-SENT-COMP-WORD-000372
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: The town ____ the drivers who joined the cleanup.
A. complied
B. complimented
C. complemented
D. compliment
MARKED ANSWER B. complimented
WHY "complimented" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 372 | CIVIO-VEN-SENT-COMP-WORD-000373
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: To ____ should I give the signed vouchers?
A. which
B. who
C. whose
D. whom
MARKED ANSWER D. whom
WHY "whom" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 373 | CIVIO-VEN-WORD-MEANING-000374
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is closest in meaning to the word in capital letters?  INTEGRITY
A. integration
B. intensity
C. honesty
D. corruption
MARKED ANSWER C. honesty
WHY "honesty" is right. "Integrity" means honesty.
SHORTCUT Make a short sentence with "integrity", then swap in each choice. Watch for words that only look or sound like "integrity".

### 374 | CIVIO-VEN-ERROR-TENSE-000375
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the correct verb: By the end of the year, the city treasurer's office staff ____ the relief goods.
A. is delivering
B. delivered
C. has delivered
D. will have delivered
MARKED ANSWER D. will have delivered
WHY "will have delivered" is right: the future perfect matches "By the end of the year".
SHORTCUT Find the time signal first: "By the end of the year". It calls for the future perfect.

### 375 | CIVIO-VEN-RC-VOCAB-000376
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The guard will not TOLERATE rude behavior at the gate.
A. measure
B. forbid
C. allow
D. tell
MARKED ANSWER C. allow
WHY "allow" is right: it is the sense of "tolerate" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "tolerate".

### 376 | CIVIO-VEN-ERROR-AGREE-000377
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: The teachers in the school ____ finished the grading.
A. to have
B. have
C. having
D. has
MARKED ANSWER B. have
WHY "have" is right: "The teachers" is plural.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The teachers ____". The subject is plural, so use the plural verb.

### 377 | CIVIO-VEN-WORD-MEANING-000378
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  PRUDENT
A. prominent
B. prude
C. careful
D. reckless
MARKED ANSWER D. reckless
WHY "reckless" is right. "Prudent" means careful; "reckless" is the reverse.
SHORTCUT First say what "prudent" means (careful). Then look for the word that means the reverse.

### 378 | CIVIO-VEN-WORD-MEANING-000379
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is closest in meaning to the word in capital letters?  HOSTILE
A. hostage
B. welcoming
C. hostel
D. unfriendly
MARKED ANSWER D. unfriendly
WHY "unfriendly" is right. "Hostile" means unfriendly.
SHORTCUT Make a short sentence with "hostile", then swap in each choice. Watch for words that only look or sound like "hostile".

### 379 | CIVIO-VEN-SENT-COMP-PHRASAL-000380
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the phrase that best completes the sentence: The office will ____ a new system for leave requests.
A. set off
B. set back
C. set up
D. set aside
MARKED ANSWER C. set up
WHY "set up" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 380 | CIVIO-VEN-ERROR-AGREE-000381
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: The number of complaints ____ lower than last month.
A. be
B. is
C. being
D. are
MARKED ANSWER B. is
WHY "is" is right: "The number" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The number ____". The subject is singular, so use the singular verb.

### 381 | CIVIO-VEN-WORD-MEANING-000382
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  CANDID
A. frank
B. candidate
C. candied
D. secretive
MARKED ANSWER D. secretive
WHY "secretive" is right. "Candid" means frank; "secretive" is the reverse.
SHORTCUT First say what "candid" means (frank). Then look for the word that means the reverse.

### 382 | CIVIO-VEN-WORD-MEANING-000383
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  INTEGRITY
A. corruption
B. honesty
C. integration
D. intensity
MARKED ANSWER A. corruption
WHY "corruption" is right. "Integrity" means honesty; "corruption" is the reverse.
SHORTCUT First say what "integrity" means (honesty). Then look for the word that means the reverse.

### 383 | CIVIO-VEN-RC-VOCAB-000384
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The engineer gave a RELIABLE estimate of the cost.
A. relieved
B. reliant
C. dependable
D. doubtful
MARKED ANSWER C. dependable
WHY "dependable" is right: it is the sense of "reliable" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "reliable".

### 384 | CIVIO-VEN-SENT-COMP-WORD-000385
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the word that best completes the sentence: The witness gave a ____ account that matched the video exactly.
A. accustomed
B. accuracy
C. accurate
D. false
MARKED ANSWER C. accurate
WHY "accurate" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 385 | CIVIO-VEN-ERROR-TENSE-000386
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Choose the correct verb: By the end of the year, Lourdes ____ the drainage canal.
A. is inspecting
B. has inspected
C. will have inspected
D. inspected
MARKED ANSWER C. will have inspected
WHY "will have inspected" is right: the future perfect matches "By the end of the year".
SHORTCUT Find the time signal first: "By the end of the year". It calls for the future perfect.

### 386 | CIVIO-CLR-SPELL-WRONG-000387
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is misspelled?  maintenance | addres | acknowledgment | manageable
A. maintenance
B. addres
C. acknowledgment
D. manageable
MARKED ANSWER B. addres
WHY "addres" is misspelled: it doubles or undoubles a consonant. The correct spelling is "address".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 387 | CIVIO-CLR-FILE-POSITION-000388
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In alphabetical filing, which name is filed FIRST?  Engr. Benito B. Ocampo | Nora D. De Leon | Atty. Cristina A. Mendoza | Corazon V. Flores
A. Nora D. De Leon
B. Corazon V. Flores
C. Engr. Benito B. Ocampo
D. Atty. Cristina A. Mendoza
MARKED ANSWER A. Nora D. De Leon
WHY "Nora D. De Leon" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Nora D. De Leon → DELEON, Nora; Corazon V. Flores → FLORES, Corazon; Atty. Cristina A. Mendoza → MENDOZA, Cristina; Engr. Benito B. Ocampo → OCAMPO, Benito.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 388 | CIVIO-CLR-FILE-POSITION-000389
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In alphabetical filing, which name is filed FIRST?  Danilo B. Juan | Felipe T. Dela Cruz | Juan S. Santos-Ocampo | Engr. Maria B. De los Santos
A. Engr. Maria B. De los Santos
B. Danilo B. Juan
C. Felipe T. Dela Cruz
D. Juan S. Santos-Ocampo
MARKED ANSWER C. Felipe T. Dela Cruz
WHY "Felipe T. Dela Cruz" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Felipe T. Dela Cruz → DELACRUZ, Felipe; Engr. Maria B. De los Santos → DELOSSANTOS, Maria; Danilo B. Juan → JUAN, Danilo; Juan S. Santos-Ocampo → SANTOSOCAMPO, Juan.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 389 | CIVIO-CLR-SPELL-RIGHT-000390
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is spelled correctly?  fenomenon | phenomennon | phenomenon | phenomnon
A. fenomenon
B. phenomennon
C. phenomenon
D. phenomnon
MARKED ANSWER C. phenomenon
WHY "phenomenon" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 390 | CIVIO-CLR-SPELL-WRONG-000391
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is misspelled?  foregn | mischievous | perseverance | necessary
A. foregn
B. mischievous
C. perseverance
D. necessary
MARKED ANSWER A. foregn
WHY "foregn" is misspelled: it drops a letter. The correct spelling is "foreign".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 391 | CIVIO-CLR-FILE-POSITION-000392
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In alphabetical filing, which name is filed LAST?  Dr. Rodrigo A. Manalo | Benito P. De los Santos | Maria A. Rosario | Alfredo A. Pascual
A. Benito P. De los Santos
B. Alfredo A. Pascual
C. Dr. Rodrigo A. Manalo
D. Maria A. Rosario
MARKED ANSWER D. Maria A. Rosario
WHY "Maria A. Rosario" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Benito P. De los Santos → DELOSSANTOS, Benito; Dr. Rodrigo A. Manalo → MANALO, Rodrigo; Alfredo A. Pascual → PASCUAL, Alfredo; Maria A. Rosario → ROSARIO, Maria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 392 | CIVIO-CLR-FILE-POSITION-000393
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In alphabetical filing, which name is filed FIRST?  Danilo V. Rivera | Atty. Rodrigo N. Villanueva | Lourdes G. Dela Cruz | Imelda S. Castillo
A. Danilo V. Rivera
B. Imelda S. Castillo
C. Lourdes G. Dela Cruz
D. Atty. Rodrigo N. Villanueva
MARKED ANSWER B. Imelda S. Castillo
WHY "Imelda S. Castillo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Imelda S. Castillo → CASTILLO, Imelda; Lourdes G. Dela Cruz → DELACRUZ, Lourdes; Danilo V. Rivera → RIVERA, Danilo; Atty. Rodrigo N. Villanueva → VILLANUEVA, Rodrigo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 393 | CIVIO-CLR-SPELL-RIGHT-000394
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is spelled correctly?  allotmnt | allotmant | allotment | alotment
A. allotmnt
B. allotmant
C. allotment
D. alotment
MARKED ANSWER C. allotment
WHY "allotment" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 394 | CIVIO-CLR-SPELL-RIGHT-000395
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is spelled correctly?  pronnunciation | pronunciasion | pronnciation | pronunciation
A. pronnunciation
B. pronunciasion
C. pronnciation
D. pronunciation
MARKED ANSWER D. pronunciation
WHY "pronunciation" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 395 | CIVIO-CLR-SPELL-WRONG-000396
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is misspelled?  phenomnon | exaggerate | occurred | surveillance
A. phenomnon
B. exaggerate
C. occurred
D. surveillance
MARKED ANSWER A. phenomnon
WHY "phenomnon" is misspelled: it drops a letter. The correct spelling is "phenomenon".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 396 | CIVIO-CLR-SPELL-WRONG-000397
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is misspelled?  guarantee | withhold | apropriation | jewelry
A. guarantee
B. withhold
C. apropriation
D. jewelry
MARKED ANSWER C. apropriation
WHY "apropriation" is misspelled: it doubles or undoubles a consonant. The correct spelling is "appropriation".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 397 | CIVIO-CLR-FILE-POSITION-000398
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In alphabetical filing, which name is filed FIRST?  Dr. Corazon F. Garcia | Carlos E. De los Santos | Benito D. Santos | Imelda D. San Pedro
A. Imelda D. San Pedro
B. Benito D. Santos
C. Dr. Corazon F. Garcia
D. Carlos E. De los Santos
MARKED ANSWER D. Carlos E. De los Santos
WHY "Carlos E. De los Santos" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Carlos E. De los Santos → DELOSSANTOS, Carlos; Dr. Corazon F. Garcia → GARCIA, Corazon; Imelda D. San Pedro → SANPEDRO, Imelda; Benito D. Santos → SANTOS, Benito.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 398 | CIVIO-CLR-SPELL-RIGHT-000399
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is spelled correctly?  calender | calendar | callendar | calndar
A. calender
B. calendar
C. callendar
D. calndar
MARKED ANSWER B. calendar
WHY "calendar" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 399 | CIVIO-CLR-SPELL-RIGHT-000400
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Which word is spelled correctly?  achievemant | achievemment | acheivement | achievement
A. achievemant
B. achievemment
C. acheivement
D. achievement
MARKED ANSWER D. achievement
WHY "achievement" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 400 | CIVIO-CLR-FILE-POSITION-000401
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
In alphabetical filing, which name is filed LAST?  Atty. Mario R. San Juan | Maria D. Del Rosario | Rodrigo L. Juan | Benito M. Dizon
A. Maria D. Del Rosario
B. Atty. Mario R. San Juan
C. Rodrigo L. Juan
D. Benito M. Dizon
MARKED ANSWER B. Atty. Mario R. San Juan
WHY "Atty. Mario R. San Juan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Maria D. Del Rosario → DELROSARIO, Maria; Benito M. Dizon → DIZON, Benito; Rodrigo L. Juan → JUAN, Rodrigo; Atty. Mario R. San Juan → SANJUAN, Mario.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 401 | CIVIO-GI-TERM-MATCH-000402
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Under R.A. 6713, which norm of conduct requires officials to lead modest lives appropriate to their positions and income?
A. Nationalism and patriotism
B. Simple living
C. Commitment to public interest
D. Responsiveness to the public
MARKED ANSWER B. Simple living
WHY "Simple living" is right. R.A. 6713, Sec. 4(A) says: "shall lead modest lives appropriate to their positions and income".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). This is simple living, Sec. 4(A)(h).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 402 | CIVIO-GI-DEADLINE-NUMBER-000403
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Under R.A. 6713, within how many days after assuming office must a public official file the SALN?
A. 45 days
B. 15 days
C. 30 days
D. 60 days
MARKED ANSWER C. 30 days
WHY "30 days" is right. R.A. 6713, Sec. 8(A) says: "within thirty (30) days after assumption of office".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 8(A). SALN within 30 days of assuming office.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 403 | CIVIO-GI-DEADLINE-NUMBER-000404
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What is the term of the Ombudsman and Deputies?
A. 7 years, without reappointment
B. 9 years, without reappointment
C. 5 years, without reappointment
D. 6 years, with reappointment
MARKED ANSWER A. 7 years, without reappointment
WHY "7 years, without reappointment" is right. Art. XI, Sec. 8 says: "shall serve for a term of seven years without reappointment".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 8. Ombudsman: 7 years, no reappointment.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 404 | CIVIO-GI-TERM-MATCH-000405
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Under R.A. 6713, may a public employee solicit or accept a gift from anyone in connection with an official transaction?
A. Yes, after the transaction is finished
B. No
C. Yes, if the head of office knows
D. Yes, if the gift is worth less than ₱1,000
MARKED ANSWER B. No
WHY "No" is right. R.A. 6713, Sec. 7(d) says: "Public officials and employees shall not solicit or accept, directly or indirectly, any gift".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 7(d). Gifts tied to official work are prohibited.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 405 | CIVIO-GI-TERM-MATCH-000406
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Under the 1987 Constitution, the President, Vice-President and Cabinet members may NOT hold what during their tenure, unless the Constitution provides otherwise?
A. Any other office or employment
B. Membership in a religious group
C. A university degree program
D. A bank account
MARKED ANSWER A. Any other office or employment
WHY "Any other office or employment" is right. Art. VII, Sec. 13 says: "shall not, unless otherwise provided in this Constitution, hold any other office or employment during their tenure".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 13. No other office or employment.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 406 | CIVIO-GI-TERM-MATCH-000407
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Under Art. II, Sec. 16, the State shall protect and advance the right of the people to what?
A. Free electricity
B. A balanced and healthful ecology
C. Tax-free land
D. Unlimited use of natural resources
MARKED ANSWER B. A balanced and healthful ecology
WHY "A balanced and healthful ecology" is right. Art. II, Sec. 16 says: "right of the people to a balanced and healthful ecology".
SHORTCUT Tie the fact to its section: Art. II, Sec. 16. This is the environmental right.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 407 | CIVIO-GI-DEADLINE-NUMBER-000408
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
How long is the term of elective local officials, except barangay officials?
A. 6 years
B. 2 years
C. 3 years
D. 4 years
MARKED ANSWER C. 3 years
WHY "3 years" is right. Art. X, Sec. 8 says: "shall be three years and no such official shall serve for more than three consecutive terms".
SHORTCUT Tie the fact to its section: Art. X, Sec. 8. Local officials: 3-year terms, three-term limit.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 408 | CIVIO-GI-DEADLINE-NUMBER-000409
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
What is the minimum age to be appointed Chairman or Commissioner of the Civil Service Commission?
A. 40 years old
B. 45 years old
C. 35 years old
D. 30 years old
MARKED ANSWER C. 35 years old
WHY "35 years old" is right. Art. IX-B, Sec. 1(1) says: "at least thirty-five years of age".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 1(1). CSC members must be at least 35 when appointed.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 409 | CIVIO-GI-DEADLINE-NUMBER-000410
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
How many days does the President have to veto a bill before it becomes law without signature?
A. 30 days from receipt
B. 60 days from receipt
C. 10 days from receipt
D. 15 days from receipt
MARKED ANSWER A. 30 days from receipt
WHY "30 days from receipt" is right. Art. VI, Sec. 27(1) says: "within thirty days after the date of receipt thereof".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 27(1). A bill becomes law if not vetoed within 30 days.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 410 | CIVIO-GI-DEADLINE-NUMBER-000411
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-005.json
STEM
Within how many days from receipt of a copy may a decision of a Constitutional Commission be brought to the Supreme Court on certiorari?
A. 60 days
B. 15 days
C. 30 days
D. 10 days
MARKED ANSWER C. 30 days
WHY "30 days" is right. Art. IX-A, Sec. 7 says: "within thirty days from receipt of a copy thereof".
SHORTCUT Tie the fact to its section: Art. IX-A, Sec. 7. The petition to the Supreme Court is due within 30 days.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 411 | CIVIO-NUM-OPS-ORDER-000412
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What is the value of 12 + 3 × 5 − 8?
A. 12
B. 19
C. 67
D. 3
MARKED ANSWER B. 19
WHY 19 is right: 12 + 15 = 27, and 27 − 8 = 19.
SHORTCUT Circle the × first: 3 × 5 = 15. Then go left to right: 12 + 15 − 8.

### 412 | CIVIO-NUM-WP-AVERAGE-000413
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
The average years of service of the 5 teachers in the civil registry is 8 years. One more person, with 26 years, joins them. What is the new average years of service?
A. 11.6 years
B. 66 years
C. 11 years
D. 17 years
MARKED ANSWER C. 11 years
WHY 11 years is right. Long way: 5 × 8 = 40; + 26 = 66; ÷ 6 = 11.
SHORTCUT The new person is 26 − 8 = 18 above the old average. Share that among all 6 people: 18 ÷ 6 = 3. Add it: 8 + 3 = 11.

### 413 | CIVIO-NUM-WP-PCT-CHANGE-000414
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A cooperative member borrows ₱20,000 at 4% simple interest per year. How much interest is due after 2 years?
A. ₱1,600
B. ₱800
C. ₱16,000
D. ₱21,600
MARKED ANSWER A. ₱1,600
WHY ₱1,600 is right. Check: 20,000 × 0.04 × 2 = 1,600.
SHORTCUT Find one year first: 4% of ₱20,000 = ₱800. Time is 2 years. Multiply: 2 × ₱800 = ₱1,600.

### 414 | CIVIO-NUM-WP-PCT-CHANGE-000415
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A cooperative store sold a gallon of paint for ₱600. It raised the price by 50%. Later, it lowered the new price by 25%. What is the final price?
A. ₱900
B. ₱1,012.50
C. ₱750
D. ₱675
MARKED ANSWER D. ₱675
WHY ₱675 is right. Check: 600 × 1.5 = 900, and 900 × 0.75 = 675.
SHORTCUT Do one change at a time. ₱600 up 50% is ₱600 + ₱300 = ₱900. Then 25% of ₱900 is ₱225, so ₱900 − ₱225 = ₱675.

### 415 | CIVIO-NUM-OPS-ORDER-000416
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What is the value of 14 + 2 × 7 − 6?
A. 22
B. 106
C. 16
D. 17
MARKED ANSWER A. 22
WHY 22 is right: 14 + 14 = 28, and 28 − 6 = 22.
SHORTCUT Circle the × first: 2 × 7 = 14. Then go left to right: 14 + 14 − 6.

### 416 | CIVIO-NUM-WP-PCT-CHANGE-000417
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A rice cooker is priced at ₱800. It is sold at 20% off. How much does a buyer pay?
A. ₱160
B. ₱960
C. ₱780
D. ₱640
MARKED ANSWER D. ₱640
WHY ₱640 is right. Check: discount ₱160; ₱800 − ₱160 = ₱640.
SHORTCUT Pay 80% of the price: ₱800 × 0.8 = ₱640.

### 417 | CIVIO-NUM-WP-ALGEBRA-000418
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Bong is 3 times as old as his daughter. In 12 years, Bong will be twice as old as the daughter. How old is Bong now?
A. 24
B. 12
C. 36
D. 48
MARKED ANSWER C. 36
WHY 36 is right. Algebra: daughter = s, Bong = 3s; 3s + 12 = 2(s + 12) gives s = 12, so Bong = 36.
SHORTCUT Try the choices. If Bong is 36, the daughter is 12. In 12 years: 48 and 24. 48 = 2 × 24, so it works.

### 418 | CIVIO-NUM-WP-RATE-000419
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Kimberly can encode a box of survey forms in 36 hours. Carlo can do the same job in 12 hours. Working together, how long will they take?
A. 9 hours
B. 24 hours
C. 6.6667 hours
D. 48 hours
MARKED ANSWER A. 9 hours
WHY 9 hours is right. Check: in 9 hours, Kimberly does 9/36 and Carlo does 9/12; together that is 1 whole job.
SHORTCUT Per hour, Kimberly does 1/36 and Carlo does 1/12. Together: 1/36 + 1/12 = 1/9. So the whole job takes 9 hours.

### 419 | CIVIO-NUM-SEQ-DIFF-000420
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Find the next number in the series.  6, 7, 11, 18, 28, ___
A. 41
B. 44
C. 29
D. 38
MARKED ANSWER A. 41
WHY 41 is right: 28 + 13 = 41.
SHORTCUT Write the jumps under the list: +1, +4, +7, +10. Each jump is 3 more than the one before. So the next jump is +13.

### 420 | CIVIO-NUM-WP-PCT-CHANGE-000421
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A rice cooker is priced at ₱480. It is sold at 30% off. How much does a buyer pay?
A. ₱336
B. ₱450
C. ₱624
D. ₱144
MARKED ANSWER A. ₱336
WHY ₱336 is right. Check: discount ₱144; ₱480 − ₱144 = ₱336.
SHORTCUT Pay 70% of the price: ₱480 × 0.7 = ₱336.

### 421 | CIVIO-NUM-WP-GEOM-000422
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A rectangular basketball court is 32 m long and 11 m wide. A fence costs ₱150 per meter. How much will it cost to put the fence around the whole basketball court?
A. ₱86
B. ₱52,800
C. ₱6,450
D. ₱12,900
MARKED ANSWER D. ₱12,900
WHY ₱12,900 is right: 86 m × ₱150 = ₱12,900.
SHORTCUT Around = 2 × (32 + 11) = 86 m. Cost = 86 × ₱150.

### 422 | CIVIO-NUM-WP-PCT-CHANGE-000423
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A umbrella set is priced at ₱1,500. It is sold at 15% off. How much does a buyer pay?
A. ₱1,725
B. ₱1,485
C. ₱225
D. ₱1,275
MARKED ANSWER D. ₱1,275
WHY ₱1,275 is right. Check: discount ₱225; ₱1,500 − ₱225 = ₱1,275.
SHORTCUT Pay 85% of the price: ₱1,500 × 0.85 = ₱1,275.

### 423 | CIVIO-NUM-WP-RATE-000424
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Bea can clean the plaza in 18 hours. Aileen can do the same job in 9 hours. Working together, how long will they take?
A. 13.5 hours
B. 6 hours
C. 10 minutes
D. 27 hours
MARKED ANSWER B. 6 hours
WHY 6 hours is right. Check: in 6 hours, Bea does 6/18 and Aileen does 6/9; together that is 1 whole job.
SHORTCUT Per hour, Bea does 1/18 and Aileen does 1/9. Together: 1/18 + 1/9 = 1/6. So the whole job takes 6 hours.

### 424 | CIVIO-NUM-SEQ-DIFF-000425
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What number comes next in the series?  1, 4, 8, 13, 19, ___
A. 26
B. 27
C. 25
D. 22
MARKED ANSWER A. 26
WHY 26 is right: 19 + 7 = 26.
SHORTCUT Write the jumps under the list: +3, +4, +5, +6. Each jump is 1 more than the one before. So the next jump is +7.

### 425 | CIVIO-NUM-WP-RATIO-000426
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A ₱27,000 commission is divided between Bea and Cora in the ratio 4 : 5. What is Cora's share?
A. ₱5,400
B. ₱3,000
C. ₱15,000
D. ₱12,000
MARKED ANSWER C. ₱15,000
WHY ₱15,000 is right: 5 × ₱3,000 = ₱15,000. Check: ₱12,000 + ₱15,000 = ₱27,000.
SHORTCUT Add the ratio numbers to get equal parts: 4 + 5 = 9. One part = ₱27,000 ÷ 9 = ₱3,000. Then multiply by the parts you need.

### 426 | CIVIO-NUM-SEQ-DIFF-000427
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which number should come next?  11, 13, 18, 26, 37, ___
A. 54
B. 51
C. 48
D. 39
MARKED ANSWER B. 51
WHY 51 is right: 37 + 14 = 51.
SHORTCUT Write the jumps under the list: +2, +5, +8, +11. Each jump is 3 more than the one before. So the next jump is +14.

### 427 | CIVIO-NUM-WP-PCT-CHANGE-000428
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A hardware store sold a sack of rice for ₱400. It raised the price by 10%. Later, it lowered the new price by 40%. What is the final price?
A. ₱440
B. ₱280
C. ₱290.40
D. ₱264
MARKED ANSWER D. ₱264
WHY ₱264 is right. Check: 400 × 1.1 = 440, and 440 × 0.6 = 264.
SHORTCUT Do one change at a time. ₱400 up 10% is ₱400 + ₱40 = ₱440. Then 40% of ₱440 is ₱176, so ₱440 − ₱176 = ₱264.

### 428 | CIVIO-NUM-WP-PCT-CHANGE-000429
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A market stall sold a bag of cement for ₱600. It raised the price by 30%. Later, it lowered the new price by 40%. What is the final price?
A. ₱468
B. ₱540
C. ₱608.40
D. ₱780
MARKED ANSWER A. ₱468
WHY ₱468 is right. Check: 600 × 1.3 = 780, and 780 × 0.6 = 468.
SHORTCUT Do one change at a time. ₱600 up 30% is ₱600 + ₱180 = ₱780. Then 40% of ₱780 is ₱312, so ₱780 − ₱312 = ₱468.

### 429 | CIVIO-NUM-WP-RATE-000430
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Grace can repack the relief goods in 20 hours. Bea can do the same job in 30 hours. Working together, how long will they take?
A. 25 hours
B. 12 hours
C. 5 minutes
D. 50 hours
MARKED ANSWER B. 12 hours
WHY 12 hours is right. Check: in 12 hours, Grace does 12/20 and Bea does 12/30; together that is 1 whole job.
SHORTCUT Per hour, Grace does 1/20 and Bea does 1/30. Together: 1/20 + 1/30 = 1/12. So the whole job takes 12 hours.

### 430 | CIVIO-NUM-WP-AVERAGE-000431
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
The average age of the 8 drivers in the barangay hall is 42 years. One more person, with 69 years, joins them. What is the new average age?
A. 405 years
B. 55.5 years
C. 45 years
D. 45.38 years
MARKED ANSWER C. 45 years
WHY 45 years is right. Long way: 8 × 42 = 336; + 69 = 405; ÷ 9 = 45.
SHORTCUT The new person is 69 − 42 = 27 above the old average. Share that among all 9 people: 27 ÷ 9 = 3. Add it: 42 + 3 = 45.

### 431 | CIVIO-NUM-WP-RATIO-000432
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Carlo and Aling Rosa will share ₱14,400 of cleanup fund in the ratio 5 : 7. How much is Aling Rosa's share?
A. ₱2,057.14
B. ₱1,200
C. ₱6,000
D. ₱8,400
MARKED ANSWER D. ₱8,400
WHY ₱8,400 is right: 7 × ₱1,200 = ₱8,400. Check: ₱6,000 + ₱8,400 = ₱14,400.
SHORTCUT Add the ratio numbers to get equal parts: 5 + 7 = 12. One part = ₱14,400 ÷ 12 = ₱1,200. Then multiply by the parts you need.

### 432 | CIVIO-NUM-OPS-ORDER-000433
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What is the value of 5 + 3 × 6 − 1?
A. 47
B. 13
C. 20
D. 22
MARKED ANSWER D. 22
WHY 22 is right: 5 + 18 = 23, and 23 − 1 = 22.
SHORTCUT Circle the × first: 3 × 6 = 18. Then go left to right: 5 + 18 − 1.

### 433 | CIVIO-NUM-WP-RATIO-000434
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Aileen and Joy will share ₱12,500 of cleanup fund in the ratio 2 : 3. How much is Joy's share?
A. ₱4,166.67
B. ₱5,000
C. ₱7,500
D. ₱2,500
MARKED ANSWER C. ₱7,500
WHY ₱7,500 is right: 3 × ₱2,500 = ₱7,500. Check: ₱5,000 + ₱7,500 = ₱12,500.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 3 = 5. One part = ₱12,500 ÷ 5 = ₱2,500. Then multiply by the parts you need.

### 434 | CIVIO-NUM-WP-ALGEBRA-000435
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Nestor is 5 times as old as his daughter. In 10 years, Nestor will be three times as old as the daughter. How old is Nestor now?
A. 50
B. 60
C. 20
D. 10
MARKED ANSWER A. 50
WHY 50 is right. Algebra: daughter = s, Nestor = 5s; 5s + 10 = 3(s + 10) gives s = 10, so Nestor = 50.
SHORTCUT Try the choices. If Nestor is 50, the daughter is 10. In 10 years: 60 and 20. 60 = 3 × 20, so it works.

### 435 | CIVIO-NUM-WP-AVERAGE-000436
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
The average age of the 6 staff members in the district hospital is 20 years. One more person, with 34 years, joins them. What is the new average age?
A. 22 years
B. 154 years
C. 22.33 years
D. 27 years
MARKED ANSWER A. 22 years
WHY 22 years is right. Long way: 6 × 20 = 120; + 34 = 154; ÷ 7 = 22.
SHORTCUT The new person is 34 − 20 = 14 above the old average. Share that among all 7 people: 14 ÷ 7 = 2. Add it: 20 + 2 = 22.

### 436 | CIVIO-NUM-WP-GEOM-000437
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A rectangular basketball court is 36 m long and 3 m wide. A chain-link fence costs ₱150 per meter. How much will it cost to put the chain-link fence around the whole basketball court?
A. ₱78
B. ₱16,200
C. ₱5,850
D. ₱11,700
MARKED ANSWER D. ₱11,700
WHY ₱11,700 is right: 78 m × ₱150 = ₱11,700.
SHORTCUT Around = 2 × (36 + 3) = 78 m. Cost = 78 × ₱150.

### 437 | CIVIO-NUM-SEQ-MULT-000438
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What number comes next?  5, 11, 23, 47, 95, ___
A. 191
B. 190
C. 143
D. 192
MARKED ANSWER A. 191
WHY 191 is right: 95 × 2 = 190, then + 1 gives 191.
SHORTCUT Test "times 2, then + 1" on the first numbers: 5 × 2 + 1 = 11; 11 × 2 + 1 = 23. It works, so use it on 95.

### 438 | CIVIO-NUM-WP-GEOM-000439
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A rectangular school lot is 30 m long and 16 m wide. A fence costs ₱25 per meter. How much will it cost to put the fence around the whole school lot?
A. ₱2,300
B. ₱1,150
C. ₱12,000
D. ₱92
MARKED ANSWER A. ₱2,300
WHY ₱2,300 is right: 92 m × ₱25 = ₱2,300.
SHORTCUT Around = 2 × (30 + 16) = 92 m. Cost = 92 × ₱25.

### 439 | CIVIO-NUM-FRAC-DEC-000440
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A barangay had 1200 sacks of relief rice. It gave out 1/4 of them on Monday and 1/6 of the remaining sacks of relief rice on Tuesday. How many are left?
A. 700
B. 750
C. 150
D. 900
MARKED ANSWER B. 750
WHY 750 is right. Check: 300 + 150 + 750 = 1200.
SHORTCUT Go day by day. Monday: 1/4 of 1200 = 300, so 900 left. Tuesday: 1/6 of 900 = 150, so 900 − 150 = 750 left.

### 440 | CIVIO-NUM-FRAC-DEC-000441
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
A barangay had 1080 school chairs. It gave out 1/6 of them on Monday and 2/3 of the remaining school chairs on Tuesday. How many are left?
A. 600
B. 300
C. 180
D. 900
MARKED ANSWER B. 300
WHY 300 is right. Check: 180 + 600 + 300 = 1080.
SHORTCUT Go day by day. Monday: 1/6 of 1080 = 180, so 900 left. Tuesday: 2/3 of 900 = 600, so 900 − 600 = 300 left.

### 441 | CIVIO-ANA-ANALOGY-FORM-000442
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
ICE : WATER :: ____
A. candle wax : melted wax
B. steam : ice
C. water : ice
D. cold : freezer
MARKED ANSWER A. candle wax : melted wax
WHY "candle wax : melted wax" is right. It has the same link, solid form : liquid form, in the same order.
SHORTCUT Make a sentence for the stem: "ice is to water" as solid form : liquid form. Test each choice in that sentence.

### 442 | CIVIO-ANA-SYLLOGISM-000443
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Statement 1: No plants are recalled items. Statement 2: All seedlings are plants. Which conclusion follows from both statements?
A. Some seedlings are recalled items.
B. No nursery stock are recalled items.
C. All plants are seedlings.
D. No seedlings are recalled items.
MARKED ANSWER D. No seedlings are recalled items.
WHY "No seedlings are recalled items." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the seedlings circle inside plants. The "recalled items" circle sits outside plants, so it is outside seedlings too.

### 443 | CIVIO-ANA-SYMBOL-SERIES-000444
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In a certain code, TOWN is written as UPXO. How is AGENT written in the same code?
A. BHFOT
B. ZFDMS
C. CIGPV
D. BHFOU
MARKED ANSWER D. BHFOU
WHY BHFOU is right: each letter of AGENT moved 1 place forward.
SHORTCUT Compare the first letters: T became U. That is 1 place forward. Check one more letter, then shift every letter of AGENT the same way.

### 444 | CIVIO-ANA-ANALOGY-PART-000445
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Find the pair whose link matches the link between "page" and "book".
A. author : story
B. ink : printer
C. brick : wall
D. library : shelf
MARKED ANSWER C. brick : wall
WHY "brick : wall" is right. It has the same link, part : whole, in the same order.
SHORTCUT Make a sentence for the stem: "page is to book" as part : whole. Test each choice in that sentence.

### 445 | CIVIO-ANA-SYMBOL-SERIES-000446
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In a certain code, MEMO is written as KCKM. How is PORT written in the same code?
A. NMPR
B. RQTV
C. MLOQ
D. NMPT
MARKED ANSWER A. NMPR
WHY NMPR is right: each letter of PORT moved 2 places back.
SHORTCUT Compare the first letters: M became K. That is 2 places back. Check one more letter, then shift every letter of PORT the same way.

### 446 | CIVIO-ANA-SYLLOGISM-000447
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Statement 1: All structures are inspected works. Statement 2: All bridges are structures. Which conclusion follows from both statements?
A. Some inspected works are not structures.
B. All inspected works are bridges.
C. All bridges are inspected works.
D. No structures are bridges.
MARKED ANSWER C. All bridges are inspected works.
WHY "All bridges are inspected works." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: bridges inside structures, structures inside inspected works. So bridges sit inside inspected works.

### 447 | CIVIO-ANA-ANALOGY-FORM-000448
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which pair shows the same relationship as "famine : food"?
A. harvest : rice
B. wealth : poverty
C. feast : food
D. poverty : money
MARKED ANSWER D. poverty : money
WHY "poverty : money" is right. It has the same link, condition : what it lacks, in the same order.
SHORTCUT Make a sentence for the stem: "famine is to food" as condition : what it lacks. Test each choice in that sentence.

### 448 | CIVIO-ANA-DI-TABLE-000449
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Supply use of toner (units) by office (Library: Apr 44, May 12, Jun 76; HR: Apr 70, May 46, Jun 70; Records: Apr 28, May 66, Jun 68). How many did Records use in all three months?
A. 54
B. 162
C. 94
D. 124
MARKED ANSWER B. 162
WHY 162 is right: 28 + 66 + 68 = 162.
SHORTCUT Read across the Records row only: 28 + 66 + 68.

### 449 | CIVIO-ANA-SYMBOL-SERIES-000450
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In a certain code, AUDIT is written as CWFKV. How is AGENT written in the same code?
A. CIGPT
B. YECLR
C. CIGPV
D. DJHQW
MARKED ANSWER C. CIGPV
WHY CIGPV is right: each letter of AGENT moved 2 places forward.
SHORTCUT Compare the first letters: A became C. That is 2 places forward. Check one more letter, then shift every letter of AGENT the same way.

### 450 | CIVIO-ANA-CONCLUSION-000451
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Four staff members are compared. Bea finished the report earlier than Inday. Inday finished the report earlier than Kimberly. Datu finished the report earlier than Bea. Who is second in the order (counting from the one who finished first)?
A. Inday
B. Datu
C. Bea
D. Kimberly
MARKED ANSWER C. Bea
WHY Bea is right. The clues give Datu → Bea → Inday → Kimberly, so Bea is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Datu → Bea → Inday → Kimberly.

### 451 | CIVIO-ANA-SYMBOL-SERIES-000452
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In a certain code, BRIDGE is written as DTKFIG. How is PAPER written in the same code?
A. NYNCP
B. RCRGT
C. RCRGR
D. SDSHU
MARKED ANSWER B. RCRGT
WHY RCRGT is right: each letter of PAPER moved 2 places forward.
SHORTCUT Compare the first letters: B became D. That is 2 places forward. Check one more letter, then shift every letter of PAPER the same way.

### 452 | CIVIO-ANA-ASSUME-I-II-000453
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Statement: The cooperative will train members to keep simple records of their sales.
Assumption I: All members already keep perfect records.
Assumption II: Simple records can help members run their business.
Which assumption is implicit in the statement?
A. Neither I nor II
B. Both I and II
C. Only II
D. Only I
MARKED ANSWER C. Only II
WHY "Only II" is right. Only assumption II is needed. I ("All members already keep perfect records.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 453 | CIVIO-ANA-ANALOGY-FORM-000454
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
BUD : FLOWER :: ____
A. egg : chicken
B. petal : stem
C. flower : bud
D. garden : soil
MARKED ANSWER A. egg : chicken
WHY "egg : chicken" is right. It has the same link, early stage : later stage, in the same order.
SHORTCUT Make a sentence for the stem: "bud is to flower" as early stage : later stage. Test each choice in that sentence.

### 454 | CIVIO-ANA-ASSUME-I-II-000455
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Statement: The health center will open on Saturdays so working mothers can bring their babies for vaccines.
Assumption I: Some working mothers cannot come on weekdays.
Assumption II: Vaccines given on Saturday work better.
Which assumption is implicit in the statement?
A. Both I and II
B. Only II
C. Neither I nor II
D. Only I
MARKED ANSWER D. Only I
WHY "Only I" is right. Only assumption I is needed. II ("Vaccines given on Saturday work better.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 455 | CIVIO-ANA-DI-TABLE-000456
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Supply use of ballpens (boxes) by office (Library: Apr 54, May 80, Jun 60; HR: Apr 28, May 62, Jun 22; Cashier: Apr 28, May 18, Jun 36). In Jun, how many more did Library use than Cashier?
A. 96
B. 112
C. 24
D. 26
MARKED ANSWER C. 24
WHY 24 is right: 60 − 36 = 24.
SHORTCUT Go to the Jun column: Library 60, Cashier 36. Subtract the smaller from the larger.

### 456 | CIVIO-ANA-CONCLUSION-000457
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Four staff members are compared. Joy arrived earlier than Paolo. Nonoy arrived earlier than Joy. Cora arrived earlier than Nonoy. Who is third in the order (counting from the one who arrived first)?
A. Joy
B. Cora
C. Nonoy
D. Paolo
MARKED ANSWER A. Joy
WHY Joy is right. The clues give Cora → Nonoy → Joy → Paolo, so Joy is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Cora → Nonoy → Joy → Paolo.

### 457 | CIVIO-ANA-CONCLUSION-000458
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Four staff members are compared. Marites finished the report earlier than Bea. Mang Jun finished the report earlier than Arnel. Bea finished the report earlier than Mang Jun. Who is third in the order (counting from the one who finished first)?
A. Bea
B. Marites
C. Mang Jun
D. Arnel
MARKED ANSWER C. Mang Jun
WHY Mang Jun is right. The clues give Marites → Bea → Mang Jun → Arnel, so Mang Jun is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Marites → Bea → Mang Jun → Arnel.

### 458 | CIVIO-ANA-SYMBOL-SERIES-000459
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In a certain code, VOTER is written as XQVGT. How is AUDIT written in the same code?
A. CWFKV
B. DXGLW
C. CWFKT
D. YSBGR
MARKED ANSWER A. CWFKV
WHY CWFKV is right: each letter of AUDIT moved 2 places forward.
SHORTCUT Compare the first letters: V became X. That is 2 places forward. Check one more letter, then shift every letter of AUDIT the same way.

### 459 | CIVIO-ANA-SYLLOGISM-000460
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
All jeepneys are public vehicles. Some jeepneys are gifts from the province. Which conclusion must be true?
A. All gifts from the province are jeepneys.
B. All public vehicles are gifts from the province.
C. No public vehicles are gifts from the province.
D. Some public vehicles are gifts from the province.
MARKED ANSWER D. Some public vehicles are gifts from the province.
WHY "Some public vehicles are gifts from the province." is right. It follows from the two statements with no extra facts.
SHORTCUT The jeepneys who are gifts from the province are also public vehicles. So at least some public vehicles are gifts from the province.

### 460 | CIVIO-ANA-CONCLUSION-000461
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Four staff members are compared. Jomar has served longer than Rogelio. Bea has served longer than Jomar. Cora has served longer than Bea. Who is second in the order (counting from the one who has served the longest)?
A. Bea
B. Cora
C. Jomar
D. Rogelio
MARKED ANSWER A. Bea
WHY Bea is right. The clues give Cora → Bea → Jomar → Rogelio, so Bea is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Cora → Bea → Jomar → Rogelio.

### 461 | CIVIO-ANA-SYLLOGISM-000462
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Statement 1: Some jeepneys are items on the March list. Statement 2: All jeepneys are public vehicles. Which conclusion follows from both statements?
A. Some public vehicles are items on the March list.
B. All items on the March list are jeepneys.
C. No public vehicles are items on the March list.
D. All public vehicles are items on the March list.
MARKED ANSWER A. Some public vehicles are items on the March list.
WHY "Some public vehicles are items on the March list." is right. It follows from the two statements with no extra facts.
SHORTCUT The jeepneys who are items on the March list are also public vehicles. So at least some public vehicles are items on the March list.

### 462 | CIVIO-ANA-SYLLOGISM-000463
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Assume these are true: a few of the barangay captains are part-time workers, and all of the barangay captains are elected officials. What can be concluded for certain?
A. Some elected officials are part-time workers.
B. No elected officials are part-time workers.
C. All part-time workers are barangay captains.
D. All elected officials are part-time workers.
MARKED ANSWER A. Some elected officials are part-time workers.
WHY "Some elected officials are part-time workers." is right. It follows from the two statements with no extra facts.
SHORTCUT The barangay captains who are part-time workers are also elected officials. So at least some elected officials are part-time workers.

### 463 | CIVIO-ANA-DI-TABLE-000464
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Supply use of folders (packs) by office (Library: Jan 76, Feb 12, Mar 54; Engineering: Jan 44, Feb 18, Mar 24; Assessor: Jan 18, Feb 78, Mar 38). How many did Assessor use in all three months?
A. 134
B. 44.7
C. 108
D. 96
MARKED ANSWER A. 134
WHY 134 is right: 18 + 78 + 38 = 134.
SHORTCUT Read across the Assessor row only: 18 + 78 + 38.

### 464 | CIVIO-ANA-DI-TABLE-000465
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Supply use of ballpens (boxes) by office (Planning: Jul 72, Aug 12, Sep 10; Library: Jul 62, Aug 74, Sep 34; HR: Jul 80, Aug 66, Sep 30). In Sep, how many more did HR use than Planning?
A. 8
B. 20
C. 82
D. 40
MARKED ANSWER B. 20
WHY 20 is right: 30 − 10 = 20.
SHORTCUT Go to the Sep column: HR 30, Planning 10. Subtract the smaller from the larger.

### 465 | CIVIO-ANA-DI-TABLE-000466
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Supply use of ballpens (boxes) by office (Planning: Jan 28, Feb 36, Mar 60; HR: Jan 58, Feb 22, Mar 48; Records: Jan 26, Feb 22, Mar 66). In Mar, how many more did Records use than Planning?
A. 126
B. 2
C. 6
D. 10
MARKED ANSWER C. 6
WHY 6 is right: 66 − 60 = 6.
SHORTCUT Go to the Mar column: Records 66, Planning 60. Subtract the smaller from the larger.

### 466 | CIVIO-VEN-SENT-COMP-WORD-000467
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The certificates were given to Liza and ____.
A. mine
B. I
C. me
D. myself
MARKED ANSWER C. me
WHY "me" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 467 | CIVIO-VEN-WORD-MEANING-000468
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  HOSTILE
A. welcoming
B. unfriendly
C. hostage
D. hostel
MARKED ANSWER A. welcoming
WHY "welcoming" is right. "Hostile" means unfriendly; "welcoming" is the reverse.
SHORTCUT First say what "hostile" means (unfriendly). Then look for the word that means the reverse.

### 468 | CIVIO-VEN-SENT-COMP-WORD-000469
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The budget is ____, so the office cannot buy new chairs this year.
A. limping
B. unlimited
C. limited
D. limit
MARKED ANSWER C. limited
WHY "limited" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 469 | CIVIO-VEN-ERROR-AGREE-000470
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The box of old receipts ____ found under the cashier's table.
A. been
B. being
C. was
D. were
MARKED ANSWER C. was
WHY "was" is right: "The box" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The box ____". The subject is singular, so use the singular verb.

### 470 | CIVIO-VEN-WORD-MEANING-000471
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is closest in meaning to the word in capital letters?  COURTEOUS
A. courageous
B. curious
C. polite
D. rude
MARKED ANSWER C. polite
WHY "polite" is right. "Courteous" means polite.
SHORTCUT Make a short sentence with "courteous", then swap in each choice. Watch for words that only look or sound like "courteous".

### 471 | CIVIO-VEN-SENT-COMP-WORD-000472
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The treasurer gave sound ____ on the budget.
A. advice
B. advices
C. device
D. advise
MARKED ANSWER A. advice
WHY "advice" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 472 | CIVIO-VEN-SENT-COMP-WORD-000473
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The applicants left ____ IDs at the guard post.
A. they're
B. their
C. there
D. them
MARKED ANSWER B. their
WHY "their" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 473 | CIVIO-VEN-RC-VOCAB-000474
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The new clerk was asked to FILE the complaint before noon.
A. withdraw
B. smooth with a tool
C. submit formally
D. photograph
MARKED ANSWER C. submit formally
WHY "submit formally" is right: it is the sense of "file" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "file".

### 474 | CIVIO-VEN-ERROR-TENSE-000475
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the correct verb: Two days ago, Mylene ____ the census forms.
A. will have encoded
B. will encode
C. encoded
D. has encoded
MARKED ANSWER C. encoded
WHY "encoded" is right: the simple past matches "Two days ago".
SHORTCUT Find the time signal first: "Two days ago". It calls for the simple past.

### 475 | CIVIO-VEN-ERROR-TENSE-000476
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the correct verb: Since January, Kimberly ____ the drainage canal on time each week.
A. has inspected
B. will inspect
C. inspected
D. will have inspected
MARKED ANSWER A. has inspected
WHY "has inspected" is right: the present perfect matches "Since January".
SHORTCUT Find the time signal first: "Since January". It calls for the present perfect.

### 476 | CIVIO-VEN-SENT-COMP-WORD-000477
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The guard was accused ____ sleeping on duty.
A. with
B. of
C. in
D. for
MARKED ANSWER B. of
WHY "of" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 477 | CIVIO-VEN-SENT-COMP-PHRASAL-000478
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the phrase that best completes the sentence: The guard ____ a wallet at the gate and returned it.
A. came down
B. came up
C. came across
D. came over
MARKED ANSWER C. came across
WHY "came across" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 478 | CIVIO-VEN-WORD-MEANING-000479
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What does the phrase in capital letters mean?  The new system will KILL TWO BIRDS WITH ONE STONE.
A. harm animals
B. solve every problem
C. solve two problems with one action
D. create two new problems
MARKED ANSWER C. solve two problems with one action
WHY "solve two problems with one action" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 479 | CIVIO-VEN-RC-VOCAB-000480
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The audit revealed a SHORTAGE of medicines in the district hospital.
A. surplus
B. storage
C. lack
D. short height
MARKED ANSWER C. lack
WHY "lack" is right: it is the sense of "shortage" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "shortage".

### 480 | CIVIO-VEN-SENT-COMP-WORD-000481
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The payroll depends ____ the attendance sheets.
A. from
B. on
C. of
D. with
MARKED ANSWER B. on
WHY "on" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 481 | CIVIO-VEN-ERROR-AGREE-000482
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the word that best completes the sentence: The head of the three sections ____ every leave form.
A. sign
B. signing
C. to sign
D. signs
MARKED ANSWER D. signs
WHY "signs" is right: "The head" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The head ____". The subject is singular, so use the singular verb.

### 482 | CIVIO-VEN-WORD-MEANING-000483
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  TEMPORARY
A. contemporary
B. permanent
C. temperate
D. short-term
MARKED ANSWER B. permanent
WHY "permanent" is right. "Temporary" means short-term; "permanent" is the reverse.
SHORTCUT First say what "temporary" means (short-term). Then look for the word that means the reverse.

### 483 | CIVIO-VEN-WORD-MEANING-000484
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What does the phrase in capital letters mean?  The new clerk is still LEARNING THE ROPES.
A. an expert already
B. training to climb
C. about to quit
D. learning how things are done
MARKED ANSWER D. learning how things are done
WHY "learning how things are done" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 484 | CIVIO-VEN-RC-VOCAB-000485
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The clerk will POST the results on the bulletin board.
A. display publicly
B. mail
C. wooden pole
D. hide
MARKED ANSWER A. display publicly
WHY "display publicly" is right: it is the sense of "post" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "post".

### 485 | CIVIO-VEN-ERROR-TENSE-000486
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Choose the correct verb: Yesterday, Liza ____ the voters' list.
A. will have updated
B. updated
C. will update
D. has updated
MARKED ANSWER B. updated
WHY "updated" is right: the simple past matches "Yesterday".
SHORTCUT Find the time signal first: "Yesterday". It calls for the simple past.

### 486 | CIVIO-CLR-SPELL-WRONG-000487
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  lieutenant | seize | emberrass | requisition
A. lieutenant
B. seize
C. emberrass
D. requisition
MARKED ANSWER C. emberrass
WHY "emberrass" is misspelled: it is spelled the way the word sounds. The correct spelling is "embarrass".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 487 | CIVIO-CLR-SPELL-WRONG-000488
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  beginnng | phenomenon | manageable | separate
A. beginnng
B. phenomenon
C. manageable
D. separate
MARKED ANSWER A. beginnng
WHY "beginnng" is misspelled: it drops a letter. The correct spelling is "beginning".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 488 | CIVIO-CLR-SPELL-WRONG-000489
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  noticeble | exaggerate | correspondence | separate
A. noticeble
B. exaggerate
C. correspondence
D. separate
MARKED ANSWER A. noticeble
WHY "noticeble" is misspelled: it drops a letter. The correct spelling is "noticeable".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 489 | CIVIO-CLR-FILE-POSITION-000490
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In alphabetical filing, which name is filed FIRST?  Felipe R. Cruz | Dr. Victoria T. Dela Cruz | Mario P. Lim | Engr. Elena G. Navarro
A. Engr. Elena G. Navarro
B. Mario P. Lim
C. Dr. Victoria T. Dela Cruz
D. Felipe R. Cruz
MARKED ANSWER D. Felipe R. Cruz
WHY "Felipe R. Cruz" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Felipe R. Cruz → CRUZ, Felipe; Dr. Victoria T. Dela Cruz → DELACRUZ, Victoria; Mario P. Lim → LIM, Mario; Engr. Elena G. Navarro → NAVARRO, Elena.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 490 | CIVIO-CLR-FILE-POSITION-000491
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In alphabetical filing, which name is filed FIRST?  Ernesto B. Lim | Liza L. Delos Reyes | Danilo G. San Pedro | Felipe V. Dizon
A. Danilo G. San Pedro
B. Felipe V. Dizon
C. Liza L. Delos Reyes
D. Ernesto B. Lim
MARKED ANSWER C. Liza L. Delos Reyes
WHY "Liza L. Delos Reyes" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Liza L. Delos Reyes → DELOSREYES, Liza; Felipe V. Dizon → DIZON, Felipe; Ernesto B. Lim → LIM, Ernesto; Danilo G. San Pedro → SANPEDRO, Danilo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 491 | CIVIO-CLR-SPELL-RIGHT-000492
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is spelled correctly?  definnitely | definitely | defintely | defnitely
A. definnitely
B. definitely
C. defintely
D. defnitely
MARKED ANSWER B. definitely
WHY "definitely" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 492 | CIVIO-CLR-FILE-POSITION-000493
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In alphabetical filing, which name is filed FIRST?  Rafael A. Santos | Teresita N. Delos Reyes | Victoria L. Flores | Corazon N. San Pedro
A. Teresita N. Delos Reyes
B. Victoria L. Flores
C. Rafael A. Santos
D. Corazon N. San Pedro
MARKED ANSWER A. Teresita N. Delos Reyes
WHY "Teresita N. Delos Reyes" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Teresita N. Delos Reyes → DELOSREYES, Teresita; Victoria L. Flores → FLORES, Victoria; Corazon N. San Pedro → SANPEDRO, Corazon; Rafael A. Santos → SANTOS, Rafael.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 493 | CIVIO-CLR-SPELL-WRONG-000494
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  ocurred | maintenance | entrepreneur | millennium
A. ocurred
B. maintenance
C. entrepreneur
D. millennium
MARKED ANSWER A. ocurred
WHY "ocurred" is misspelled: it doubles or undoubles a consonant. The correct spelling is "occurred".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 494 | CIVIO-CLR-FILE-POSITION-000495
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In alphabetical filing, which name is filed LAST?  Andres B. Lim | Mario M. Dela Cruz | Rosario V. Cruz-Manalo | Dr. Corazon F. De Guzman
A. Rosario V. Cruz-Manalo
B. Andres B. Lim
C. Dr. Corazon F. De Guzman
D. Mario M. Dela Cruz
MARKED ANSWER B. Andres B. Lim
WHY "Andres B. Lim" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Rosario V. Cruz-Manalo → CRUZMANALO, Rosario; Dr. Corazon F. De Guzman → DEGUZMAN, Corazon; Mario M. Dela Cruz → DELACRUZ, Mario; Andres B. Lim → LIM, Andres.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 495 | CIVIO-CLR-SPELL-WRONG-000496
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  surveillance | notticeable | transferred | disbursement
A. surveillance
B. notticeable
C. transferred
D. disbursement
MARKED ANSWER B. notticeable
WHY "notticeable" is misspelled: it doubles or undoubles a consonant. The correct spelling is "noticeable".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 496 | CIVIO-CLR-FILE-POSITION-000497
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
In alphabetical filing, which name is filed FIRST?  Rodrigo D. De los Santos | Eduardo T. Rivera | Mario M. Dela Torre | Ramon T. Pascual
A. Rodrigo D. De los Santos
B. Ramon T. Pascual
C. Eduardo T. Rivera
D. Mario M. Dela Torre
MARKED ANSWER D. Mario M. Dela Torre
WHY "Mario M. Dela Torre" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Mario M. Dela Torre → DELATORRE, Mario; Rodrigo D. De los Santos → DELOSSANTOS, Rodrigo; Ramon T. Pascual → PASCUAL, Ramon; Eduardo T. Rivera → RIVERA, Eduardo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 497 | CIVIO-CLR-SPELL-WRONG-000498
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  possession | exstence | appropriation | allotment
A. possession
B. exstence
C. appropriation
D. allotment
MARKED ANSWER B. exstence
WHY "exstence" is misspelled: it drops a letter. The correct spelling is "existence".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 498 | CIVIO-CLR-SPELL-RIGHT-000499
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is spelled correctly?  acquintance | acquaintance | acquaintnce | acquaintence
A. acquintance
B. acquaintance
C. acquaintnce
D. acquaintence
MARKED ANSWER B. acquaintance
WHY "acquaintance" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 499 | CIVIO-CLR-SPELL-WRONG-000500
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  grievance | accessible | foreign | liutenant
A. grievance
B. accessible
C. foreign
D. liutenant
MARKED ANSWER D. liutenant
WHY "liutenant" is misspelled: it drops a letter. The correct spelling is "lieutenant".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 500 | CIVIO-CLR-SPELL-WRONG-000501
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which word is misspelled?  acquaintance | occurrence | assessment | irrelvant
A. acquaintance
B. occurrence
C. assessment
D. irrelvant
MARKED ANSWER D. irrelvant
WHY "irrelvant" is misspelled: it drops a letter. The correct spelling is "irrelevant".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 501 | CIVIO-GI-DEADLINE-NUMBER-000502
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Under R.A. 6713, when a conflict of interest arises, within how many days from assuming office must an official divest his or her shareholdings or interest?
A. 90 days
B. 60 days
C. 30 days
D. 15 days
MARKED ANSWER B. 60 days
WHY "60 days" is right. R.A. 6713, Sec. 9 says: "divest himself of his shareholdings or interest within sixty (60) days from such assumption".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 9. Resign from the business within 30 days; divest within 60 days.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 502 | CIVIO-GI-WHO-HOLDS-POWER-000503
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Which body recommends appointees to the Judiciary under the 1987 Constitution?
A. Commission on Appointments
B. Department of Justice
C. Judicial and Bar Council
D. Integrated Bar of the Philippines
MARKED ANSWER C. Judicial and Bar Council
WHY "Judicial and Bar Council" is right. Art. VIII, Sec. 8(1) says: "A Judicial and Bar Council is hereby created".
SHORTCUT Tie the fact to its section: Art. VIII, Sec. 8(1). The JBC screens and recommends nominees to the courts.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 503 | CIVIO-GI-DEADLINE-NUMBER-000504
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
By what vote may Congress propose amendments to the Constitution acting as a constituent assembly?
A. Two-thirds of all its Members
B. One-half of its Members
C. A simple majority
D. Three-fourths of all its Members
MARKED ANSWER D. Three-fourths of all its Members
WHY "Three-fourths of all its Members" is right. Art. XVII, Sec. 1 says: "upon a vote of three-fourths of all its Members".
SHORTCUT Tie the fact to its section: Art. XVII, Sec. 1. Constituent assembly: three-fourths vote.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 504 | CIVIO-GI-DEADLINE-NUMBER-000505
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
How many norms of conduct does R.A. 6713 list in Section 4(A)?
A. Eight
B. Ten
C. Five
D. Six
MARKED ANSWER A. Eight
WHY "Eight" is right. R.A. 6713, Sec. 4(A) says: "(h) Simple living".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). Sec. 4(A) lists (a) to (h): eight norms.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 505 | CIVIO-GI-TERM-MATCH-000506
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
What is the national language of the Philippines under the 1987 Constitution?
A. Filipino
B. Pilipino
C. Tagalog
D. English
MARKED ANSWER A. Filipino
WHY "Filipino" is right. Art. XIV, Sec. 6 says: "The national language of the Philippines is Filipino".
SHORTCUT Tie the fact to its section: Art. XIV, Sec. 6. The national language is Filipino.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 506 | CIVIO-GI-TERM-MATCH-000507
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
According to the 1987 Constitution, civilian authority is supreme over what?
A. Local governments
B. The courts
C. Congress
D. The military
MARKED ANSWER D. The military
WHY "The military" is right. Art. II, Sec. 3 says: "Civilian authority is, at all times, supreme over the military".
SHORTCUT Tie the fact to its section: Art. II, Sec. 3. Civilian supremacy over the military.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 507 | CIVIO-GI-TERM-MATCH-000508
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Under R.A. 6713, being loyal to the Republic and to the Filipino people and promoting the use of locally produced goods is which norm?
A. Commitment to democracy
B. Political neutrality
C. Nationalism and patriotism
D. Responsiveness to the public
MARKED ANSWER C. Nationalism and patriotism
WHY "Nationalism and patriotism" is right. R.A. 6713, Sec. 4(A) says: "Nationalism and patriotism".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). Sec. 4(A)(f).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 508 | CIVIO-GI-TERM-MATCH-000509
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
For purposes of communication and instruction, what are the official languages of the Philippines?
A. English and Spanish
B. Filipino and Spanish
C. Filipino only
D. Filipino and, until otherwise provided by law, English
MARKED ANSWER D. Filipino and, until otherwise provided by law, English
WHY "Filipino and, until otherwise provided by law, English" is right. Art. XIV, Sec. 7 says: "the official languages of the Philippines are Filipino and, until otherwise provided by law, English".
SHORTCUT Tie the fact to its section: Art. XIV, Sec. 7. Filipino and English.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 509 | CIVIO-GI-DEADLINE-NUMBER-000510
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Within how long after an election may a losing candidate NOT be appointed to a government office?
A. Within two years after the election
B. Within three years after the election
C. Within one year after the election
D. Within six months after the election
MARKED ANSWER C. Within one year after the election
WHY "Within one year after the election" is right. Art. IX-B, Sec. 6 says: "No candidate who has lost in any election, shall within one year after such election".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 6. Losing candidates wait one year before appointment.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 510 | CIVIO-GI-DEADLINE-NUMBER-000511
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-006.json
STEM
Under R.A. 6713, within how many days after separation from the service must a SALN be filed?
A. 60 days
B. 15 days
C. 10 working days
D. 30 days
MARKED ANSWER D. 30 days
WHY "30 days" is right. R.A. 6713, Sec. 8(A) says: "within thirty (30) days after separation from the service".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 8(A). On entry, every April 30, and within 30 days after leaving.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 511 | CIVIO-NUM-WP-ALGEBRA-000512
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Bea is 5 times as old as her niece. In 16 years, Bea will be three times as old as the niece. How old is Bea now?
A. 96
B. 16
C. 32
D. 80
MARKED ANSWER D. 80
WHY 80 is right. Algebra: niece = s, Bea = 5s; 5s + 16 = 3(s + 16) gives s = 16, so Bea = 80.
SHORTCUT Try the choices. If Bea is 80, the niece is 16. In 16 years: 96 and 32. 96 = 3 × 32, so it works.

### 512 | CIVIO-NUM-SEQ-DIFF-000513
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which number should come next?  3, 4, 7, 12, 19, ___
A. 30
B. 20
C. 28
D. 26
MARKED ANSWER C. 28
WHY 28 is right: 19 + 9 = 28.
SHORTCUT Write the jumps under the list: +1, +3, +5, +7. Each jump is 2 more than the one before. So the next jump is +9.

### 513 | CIVIO-NUM-WP-PCT-CHANGE-000514
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A government employee borrows ₱12,000 at 8% simple interest per year. How much interest is due after 2 years and 6 months?
A. ₱2,496
B. ₱1,920
C. ₱2,400
D. ₱14,400
MARKED ANSWER C. ₱2,400
WHY ₱2,400 is right. Check: 12,000 × 0.08 × 2.5 = 2,400.
SHORTCUT Find one year first: 8% of ₱12,000 = ₱960. Time is 2.5 years. Multiply: 2.5 × ₱960 = ₱2,400.

### 514 | CIVIO-NUM-WP-PCT-CHANGE-000515
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A sari-sari store sold a tank of LPG for ₱240. It raised the price by 10%. Later, it lowered the new price by 50%. What is the final price?
A. ₱132
B. ₱264
C. ₱144
D. ₱145.20
MARKED ANSWER A. ₱132
WHY ₱132 is right. Check: 240 × 1.1 = 264, and 264 × 0.5 = 132.
SHORTCUT Do one change at a time. ₱240 up 10% is ₱240 + ₱24 = ₱264. Then 50% of ₱264 is ₱132, so ₱264 − ₱132 = ₱132.

### 515 | CIVIO-NUM-WP-RATIO-000516
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Bong and Teresa will share ₱25,000 of harvest income in the ratio 3 : 7. How much is Teresa's share?
A. ₱7,500
B. ₱3,571.43
C. ₱2,500
D. ₱17,500
MARKED ANSWER D. ₱17,500
WHY ₱17,500 is right: 7 × ₱2,500 = ₱17,500. Check: ₱7,500 + ₱17,500 = ₱25,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱25,000 ÷ 10 = ₱2,500. Then multiply by the parts you need.

### 516 | CIVIO-NUM-WP-PCT-CHANGE-000517
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A electric fan is priced at ₱640. It is sold at 25% off. How much does a buyer pay?
A. ₱615
B. ₱480
C. ₱160
D. ₱800
MARKED ANSWER B. ₱480
WHY ₱480 is right. Check: discount ₱160; ₱640 − ₱160 = ₱480.
SHORTCUT Pay 75% of the price: ₱640 × 0.75 = ₱480.

### 517 | CIVIO-NUM-WP-RATE-000518
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Dindo can paint a classroom in 36 hours. Aling Rosa can do the same job in 12 hours. Working together, how long will they take?
A. 24 hours
B. 6.6667 hours
C. 48 hours
D. 9 hours
MARKED ANSWER D. 9 hours
WHY 9 hours is right. Check: in 9 hours, Dindo does 9/36 and Aling Rosa does 9/12; together that is 1 whole job.
SHORTCUT Per hour, Dindo does 1/36 and Aling Rosa does 1/12. Together: 1/36 + 1/12 = 1/9. So the whole job takes 9 hours.

### 518 | CIVIO-NUM-WP-RATIO-000519
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Lourdes and Rogelio will share ₱10,500 of cleanup fund in the ratio 3 : 4. How much is Rogelio's share?
A. ₱6,000
B. ₱4,500
C. ₱1,500
D. ₱2,625
MARKED ANSWER A. ₱6,000
WHY ₱6,000 is right: 4 × ₱1,500 = ₱6,000. Check: ₱4,500 + ₱6,000 = ₱10,500.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 4 = 7. One part = ₱10,500 ÷ 7 = ₱1,500. Then multiply by the parts you need.

### 519 | CIVIO-NUM-OPS-ORDER-000520
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What is the value of 6 + 4 × 8 − 7?
A. 11
B. 31
C. 10
D. 73
MARKED ANSWER B. 31
WHY 31 is right: 6 + 32 = 38, and 38 − 7 = 31.
SHORTCUT Circle the × first: 4 × 8 = 32. Then go left to right: 6 + 32 − 7.

### 520 | CIVIO-NUM-WP-RATE-000521
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Paolo can scan the old land titles in 30 hours. Grace can do the same job in 60 hours. Working together, how long will they take?
A. 45 hours
B. 20 hours
C. 90 hours
D. 3 minutes
MARKED ANSWER B. 20 hours
WHY 20 hours is right. Check: in 20 hours, Paolo does 20/30 and Grace does 20/60; together that is 1 whole job.
SHORTCUT Per hour, Paolo does 1/30 and Grace does 1/60. Together: 1/30 + 1/60 = 1/20. So the whole job takes 20 hours.

### 521 | CIVIO-NUM-WP-RATIO-000522
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Liza and Jomar will share ₱15,000 of cleanup fund in the ratio 2 : 3. How much is Jomar's share?
A. ₱3,000
B. ₱9,000
C. ₱5,000
D. ₱6,000
MARKED ANSWER B. ₱9,000
WHY ₱9,000 is right: 3 × ₱3,000 = ₱9,000. Check: ₱6,000 + ₱9,000 = ₱15,000.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 3 = 5. One part = ₱15,000 ÷ 5 = ₱3,000. Then multiply by the parts you need.

### 522 | CIVIO-NUM-WP-PCT-CHANGE-000523
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A supplier sold a box of bond paper for ₱200. It raised the price by 50%. Later, it lowered the new price by 50%. What is the final price?
A. ₱200
B. ₱150
C. ₱300
D. ₱225
MARKED ANSWER B. ₱150
WHY ₱150 is right. Check: 200 × 1.5 = 300, and 300 × 0.5 = 150.
SHORTCUT Do one change at a time. ₱200 up 50% is ₱200 + ₱100 = ₱300. Then 50% of ₱300 is ₱150, so ₱300 − ₱150 = ₱150.

### 523 | CIVIO-NUM-WP-RATE-000524
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Cora can repack the relief goods in 6 hours. Lourdes can do the same job in 3 hours. Working together, how long will they take?
A. 2 hours
B. 30 minutes
C. 9 hours
D. 4.5 hours
MARKED ANSWER A. 2 hours
WHY 2 hours is right. Check: in 2 hours, Cora does 2/6 and Lourdes does 2/3; together that is 1 whole job.
SHORTCUT Per hour, Cora does 1/6 and Lourdes does 1/3. Together: 1/6 + 1/3 = 1/2. So the whole job takes 2 hours.

### 524 | CIVIO-NUM-OPS-ORDER-000525
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What is the value of 14 + 2 × 5 − 8?
A. 13
B. 16
C. 8
D. 72
MARKED ANSWER B. 16
WHY 16 is right: 14 + 10 = 24, and 24 − 8 = 16.
SHORTCUT Circle the × first: 2 × 5 = 10. Then go left to right: 14 + 10 − 8.

### 525 | CIVIO-NUM-WP-AVERAGE-000526
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
The average years of service of the 4 teachers in the engineering office is 16 years. One more person, with 31 years, joins them. What is the new average years of service?
A. 95 years
B. 23.5 years
C. 19 years
D. 19.75 years
MARKED ANSWER C. 19 years
WHY 19 years is right. Long way: 4 × 16 = 64; + 31 = 95; ÷ 5 = 19.
SHORTCUT The new person is 31 − 16 = 15 above the old average. Share that among all 5 people: 15 ÷ 5 = 3. Add it: 16 + 3 = 19.

### 526 | CIVIO-NUM-WP-AVERAGE-000527
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
The average years of service of the 6 staff members in the agriculture office is 16 years. One more person, with 30 years, joins them. What is the new average years of service?
A. 18.33 years
B. 23 years
C. 18 years
D. 126 years
MARKED ANSWER C. 18 years
WHY 18 years is right. Long way: 6 × 16 = 96; + 30 = 126; ÷ 7 = 18.
SHORTCUT The new person is 30 − 16 = 14 above the old average. Share that among all 7 people: 14 ÷ 7 = 2. Add it: 16 + 2 = 18.

### 527 | CIVIO-NUM-WP-PCT-CHANGE-000528
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A electric fan is priced at ₱800. It is sold at 10% off. How much does a buyer pay?
A. ₱720
B. ₱80
C. ₱880
D. ₱790
MARKED ANSWER A. ₱720
WHY ₱720 is right. Check: discount ₱80; ₱800 − ₱80 = ₱720.
SHORTCUT Pay 90% of the price: ₱800 × 0.9 = ₱720.

### 528 | CIVIO-NUM-SEQ-MULT-000529
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What number comes next?  3, 10, 31, 94, 283, ___
A. 472
B. 849
C. 851
D. 850
MARKED ANSWER D. 850
WHY 850 is right: 283 × 3 = 849, then + 1 gives 850.
SHORTCUT Test "times 3, then + 1" on the first numbers: 3 × 3 + 1 = 10; 10 × 3 + 1 = 31. It works, so use it on 283.

### 529 | CIVIO-NUM-WP-PCT-CHANGE-000530
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A farmer borrows ₱18,000 at 3% simple interest per year. How much interest is due after 2 years?
A. ₱1,080
B. ₱540
C. ₱19,080
D. ₱10,800
MARKED ANSWER A. ₱1,080
WHY ₱1,080 is right. Check: 18,000 × 0.03 × 2 = 1,080.
SHORTCUT Find one year first: 3% of ₱18,000 = ₱540. Time is 2 years. Multiply: 2 × ₱540 = ₱1,080.

### 530 | CIVIO-NUM-WP-PCT-CHANGE-000531
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A supplier sold a box of bond paper for ₱480. It raised the price by 25%. Later, it lowered the new price by 40%. What is the final price?
A. ₱408
B. ₱600
C. ₱360
D. ₱450
MARKED ANSWER C. ₱360
WHY ₱360 is right. Check: 480 × 1.25 = 600, and 600 × 0.6 = 360.
SHORTCUT Do one change at a time. ₱480 up 25% is ₱480 + ₱120 = ₱600. Then 40% of ₱600 is ₱240, so ₱600 − ₱240 = ₱360.

### 531 | CIVIO-NUM-SEQ-DIFF-000532
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What number comes next in the series?  2, 7, 15, 26, 40, ___
A. 54
B. 45
C. 60
D. 57
MARKED ANSWER D. 57
WHY 57 is right: 40 + 17 = 57.
SHORTCUT Write the jumps under the list: +5, +8, +11, +14. Each jump is 3 more than the one before. So the next jump is +17.

### 532 | CIVIO-NUM-SEQ-DIFF-000533
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Find the next number in the series.  12, 13, 17, 24, 34, ___
A. 35
B. 50
C. 44
D. 47
MARKED ANSWER D. 47
WHY 47 is right: 34 + 13 = 47.
SHORTCUT Write the jumps under the list: +1, +4, +7, +10. Each jump is 3 more than the one before. So the next jump is +13.

### 533 | CIVIO-NUM-WP-GEOM-000534
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A rectangular school lot is 29 m long and 19 m wide. A edging costs ₱25 per meter. How much will it cost to put the edging around the whole school lot?
A. ₱96
B. ₱13,775
C. ₱2,400
D. ₱1,200
MARKED ANSWER C. ₱2,400
WHY ₱2,400 is right: 96 m × ₱25 = ₱2,400.
SHORTCUT Around = 2 × (29 + 19) = 96 m. Cost = 96 × ₱25.

### 534 | CIVIO-NUM-WP-PCT-CHANGE-000535
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A government employee borrows ₱40,000 at 6% simple interest per year. How much interest is due after 1 year and 6 months?
A. ₱3,600
B. ₱3,840
C. ₱43,600
D. ₱2,400
MARKED ANSWER A. ₱3,600
WHY ₱3,600 is right. Check: 40,000 × 0.06 × 1.5 = 3,600.
SHORTCUT Find one year first: 6% of ₱40,000 = ₱2,400. Time is 1.5 years. Multiply: 1.5 × ₱2,400 = ₱3,600.

### 535 | CIVIO-NUM-OPS-ORDER-000536
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What is the value of 14 + 7 × 6 − 8?
A. 19
B. 0
C. 48
D. 118
MARKED ANSWER C. 48
WHY 48 is right: 14 + 42 = 56, and 56 − 8 = 48.
SHORTCUT Circle the × first: 7 × 6 = 42. Then go left to right: 14 + 42 − 8.

### 536 | CIVIO-NUM-WP-PCT-CHANGE-000537
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A electric fan is priced at ₱800. It is sold at 25% off. How much does a buyer pay?
A. ₱600
B. ₱1,000
C. ₱200
D. ₱775
MARKED ANSWER A. ₱600
WHY ₱600 is right. Check: discount ₱200; ₱800 − ₱200 = ₱600.
SHORTCUT Pay 75% of the price: ₱800 × 0.75 = ₱600.

### 537 | CIVIO-NUM-SEQ-MULT-000538
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What number comes next?  5, 14, 41, 122, 365, ___
A. 1093
B. 1095
C. 1094
D. 608
MARKED ANSWER C. 1094
WHY 1094 is right: 365 × 3 = 1095, then − 1 gives 1094.
SHORTCUT Test "times 3, then − 1" on the first numbers: 5 × 3 − 1 = 14; 14 × 3 − 1 = 41. It works, so use it on 365.

### 538 | CIVIO-NUM-SEQ-MULT-000539
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What number comes next?  6, 13, 27, 55, 111, ___
A. 224
B. 167
C. 222
D. 223
MARKED ANSWER D. 223
WHY 223 is right: 111 × 2 = 222, then + 1 gives 223.
SHORTCUT Test "times 2, then + 1" on the first numbers: 6 × 2 + 1 = 13; 13 × 2 + 1 = 27. It works, so use it on 111.

### 539 | CIVIO-NUM-FRAC-DEC-000540
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A barangay had 720 bags of cement. It gave out 1/8 of them on Monday and 1/3 of the remaining bags of cement on Tuesday. How many are left?
A. 630
B. 390
C. 420
D. 210
MARKED ANSWER C. 420
WHY 420 is right. Check: 90 + 210 + 420 = 720.
SHORTCUT Go day by day. Monday: 1/8 of 720 = 90, so 630 left. Tuesday: 1/3 of 630 = 210, so 630 − 210 = 420 left.

### 540 | CIVIO-NUM-FRAC-DEC-000541
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
A barangay had 240 bags of cement. It gave out 1/4 of them on Monday and 1/4 of the remaining bags of cement on Tuesday. How many are left?
A. 120
B. 135
C. 180
D. 45
MARKED ANSWER B. 135
WHY 135 is right. Check: 60 + 45 + 135 = 240.
SHORTCUT Go day by day. Monday: 1/4 of 240 = 60, so 180 left. Tuesday: 1/4 of 180 = 45, so 180 − 45 = 135 left.

### 541 | CIVIO-ANA-SYMBOL-SERIES-000542
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In a certain code, BRIDGE is written as DTKFIG. How is LIBRARY written in the same code?
A. OLEUDUB
B. NKDTCTA
C. NKDTCTY
D. JGZPYPW
MARKED ANSWER B. NKDTCTA
WHY NKDTCTA is right: each letter of LIBRARY moved 2 places forward.
SHORTCUT Compare the first letters: B became D. That is 2 places forward. Check one more letter, then shift every letter of LIBRARY the same way.

### 542 | CIVIO-ANA-SYMBOL-SERIES-000543
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What comes next in the series?  AN, EQ, IT, MW, ___
A. ZQ
B. QD
C. QZ
D. NZ
MARKED ANSWER C. QZ
WHY QZ is right: M + 4 = Q and W + 3 = Z.
SHORTCUT Split each pair. First letters: A, E, I, M (jump +4). Second letters: N, Q, T, W (jump +3). Move each one more step.

### 543 | CIVIO-ANA-SYLLOGISM-000544
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
All ferries are boats. No boats are expired stock. Which conclusion must be true?
A. All boats are ferries.
B. No inspected vessels are expired stock.
C. Some ferries are expired stock.
D. No ferries are expired stock.
MARKED ANSWER D. No ferries are expired stock.
WHY "No ferries are expired stock." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the ferries circle inside boats. The "expired stock" circle sits outside boats, so it is outside ferries too.

### 544 | CIVIO-ANA-SYMBOL-SERIES-000545
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What comes next in the series?  BO, EQ, HS, KU, ___
A. NA
B. NW
C. WN
D. LW
MARKED ANSWER B. NW
WHY NW is right: K + 3 = N and U + 2 = W.
SHORTCUT Split each pair. First letters: B, E, H, K (jump +3). Second letters: O, Q, S, U (jump +2). Move each one more step.

### 545 | CIVIO-ANA-CONCLUSION-000546
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Four staff members are compared. Rhea arrived earlier than Joy. Paolo arrived earlier than Rhea. Joy arrived earlier than Marites. Who is third in the order (counting from the one who arrived first)?
A. Paolo
B. Marites
C. Joy
D. Rhea
MARKED ANSWER C. Joy
WHY Joy is right. The clues give Paolo → Rhea → Joy → Marites, so Joy is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Paolo → Rhea → Joy → Marites.

### 546 | CIVIO-ANA-SYMBOL-SERIES-000547
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In a certain code, PAPER is written as SDSHU. How is RECORD written in the same code?
A. UHFRUD
B. VIGSVH
C. OBZLOA
D. UHFRUG
MARKED ANSWER D. UHFRUG
WHY UHFRUG is right: each letter of RECORD moved 3 places forward.
SHORTCUT Compare the first letters: P became S. That is 3 places forward. Check one more letter, then shift every letter of RECORD the same way.

### 547 | CIVIO-ANA-DI-TABLE-000548
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Supply use of folders (packs) by office (Health: Jan 22, Feb 62, Mar 50; Assessor: Jan 10, Feb 60, Mar 76; Engineering: Jan 22, Feb 54, Mar 52). How many did Health use in all three months?
A. 176
B. 44.7
C. 134
D. 84
MARKED ANSWER C. 134
WHY 134 is right: 22 + 62 + 50 = 134.
SHORTCUT Read across the Health row only: 22 + 62 + 50.

### 548 | CIVIO-ANA-ASSUME-I-II-000549
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Statement: The barangay will post the new garbage schedule on every street corner so residents know their pickup day.
Assumption I: Residents can read the posted schedule.
Assumption II: Every resident owns a mobile phone.
Which assumption is implicit in the statement?
A. Neither I nor II
B. Both I and II
C. Only I
D. Only II
MARKED ANSWER C. Only I
WHY "Only I" is right. Only assumption I is needed. II ("Every resident owns a mobile phone.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 549 | CIVIO-ANA-ASSUME-I-II-000550
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Statement: The engineering office will repair the bridge before the rainy season starts.
Assumption I: The rainy season could make the damage worse or the repair harder.
Assumption II: The bridge was built last year.
Which assumption is implicit in the statement?
A. Only I
B. Only II
C. Neither I nor II
D. Both I and II
MARKED ANSWER B. Only II
WHY "Only II" is right. Only assumption II is needed. I ("The rainy season could make the damage worse or the repair harder.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 550 | CIVIO-ANA-DI-TABLE-000551
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Supply use of staplers by office (Health: Jul 10, Aug 30, Sep 62; Engineering: Jul 66, Aug 16, Sep 58; HR: Jul 38, Aug 60, Sep 46). How many did Engineering use in all three months?
A. 46.7
B. 106
C. 82
D. 140
MARKED ANSWER D. 140
WHY 140 is right: 66 + 16 + 58 = 140.
SHORTCUT Read across the Engineering row only: 66 + 16 + 58.

### 551 | CIVIO-ANA-DI-TABLE-000552
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Supply use of toner (units) by office (Records: Apr 12, May 74, Jun 20; Planning: Apr 66, May 70, Jun 66; HR: Apr 60, May 34, Jun 66). In Jun, how many more did HR use than Records?
A. 48
B. 86
C. 54
D. 46
MARKED ANSWER D. 46
WHY 46 is right: 66 − 20 = 46.
SHORTCUT Go to the Jun column: HR 66, Records 20. Subtract the smaller from the larger.

### 552 | CIVIO-ANA-CONCLUSION-000553
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Four staff members are compared. Nestor encoded more forms than Teresa. Teresa encoded more forms than Inday. Inday encoded more forms than Joy. Who is third in the order (counting from the one who encoded the most forms)?
A. Nestor
B. Joy
C. Teresa
D. Inday
MARKED ANSWER D. Inday
WHY Inday is right. The clues give Nestor → Teresa → Inday → Joy, so Inday is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Nestor → Teresa → Inday → Joy.

### 553 | CIVIO-ANA-ANALOGY-DEGREE-000554
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which pair shows the same relationship as "warm : hot"?
A. cold : ice
B. drizzle : downpour
C. sun : heat
D. hot : warm
MARKED ANSWER B. drizzle : downpour
WHY "drizzle : downpour" is right. It has the same link, lesser : greater degree, in the same order.
SHORTCUT Make a sentence for the stem: "warm is to hot" as lesser : greater degree. Test each choice in that sentence.

### 554 | CIVIO-ANA-DI-TABLE-000555
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Supply use of staplers by office (Planning: Jul 22, Aug 12, Sep 78; Health: Jul 66, Aug 64, Sep 68; Cashier: Jul 34, Aug 70, Sep 24). How many did Planning use in all three months?
A. 146
B. 112
C. 34
D. 37.3
MARKED ANSWER B. 112
WHY 112 is right: 22 + 12 + 78 = 112.
SHORTCUT Read across the Planning row only: 22 + 12 + 78.

### 555 | CIVIO-ANA-DI-TABLE-000556
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Supply use of toner (units) by office (HR: Apr 42, May 12, Jun 24; Health: Apr 38, May 74, Jun 24; Records: Apr 18, May 62, Jun 46). How many did Health use in all three months?
A. 148
B. 112
C. 136
D. 45.3
MARKED ANSWER C. 136
WHY 136 is right: 38 + 74 + 24 = 136.
SHORTCUT Read across the Health row only: 38 + 74 + 24.

### 556 | CIVIO-ANA-SYMBOL-SERIES-000557
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In a certain code, PUBLIC is written as OTAKHB. How is VOTER written in the same code?
A. UNSDQ
B. TMRCP
C. UNSDR
D. WPUFS
MARKED ANSWER A. UNSDQ
WHY UNSDQ is right: each letter of VOTER moved 1 place back.
SHORTCUT Compare the first letters: P became O. That is 1 place back. Check one more letter, then shift every letter of VOTER the same way.

### 557 | CIVIO-ANA-CONCLUSION-000558
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Four staff members are compared. Bea lives nearer the office than Bong. Bong lives nearer the office than Mang Jun. Mang Jun lives nearer the office than Paolo. Who is second in the order (counting from the one who lives nearest)?
A. Paolo
B. Mang Jun
C. Bea
D. Bong
MARKED ANSWER D. Bong
WHY Bong is right. The clues give Bea → Bong → Mang Jun → Paolo, so Bong is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Bea → Bong → Mang Jun → Paolo.

### 558 | CIVIO-ANA-DI-TABLE-000559
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Supply use of folders (packs) by office (Library: Apr 60, May 38, Jun 34; Cashier: Apr 62, May 68, Jun 58; Assessor: Apr 50, May 26, Jun 64). In Jun, how many more did Cashier use than Library?
A. 24
B. 56
C. 2
D. 92
MARKED ANSWER A. 24
WHY 24 is right: 58 − 34 = 24.
SHORTCUT Go to the Jun column: Cashier 58, Library 34. Subtract the smaller from the larger.

### 559 | CIVIO-ANA-SYLLOGISM-000560
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Assume these are true: none of the workers are late payers, and every one of the drivers is among the workers. What can be concluded for certain?
A. Some drivers are late payers.
B. All workers are drivers.
C. No drivers are late payers.
D. No persons with IDs are late payers.
MARKED ANSWER C. No drivers are late payers.
WHY "No drivers are late payers." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the drivers circle inside workers. The "late payers" circle sits outside workers, so it is outside drivers too.

### 560 | CIVIO-ANA-CONCLUSION-000561
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Four staff members are compared. Joy scored higher than Rogelio. Rogelio scored higher than Marites. Marites scored higher than Arnel. Who is second in the order (counting from the one who got the highest score)?
A. Joy
B. Rogelio
C. Arnel
D. Marites
MARKED ANSWER B. Rogelio
WHY Rogelio is right. The clues give Joy → Rogelio → Marites → Arnel, so Rogelio is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Joy → Rogelio → Marites → Arnel.

### 561 | CIVIO-ANA-ANALOGY-DEGREE-000562
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Cool is to cold as ____.
A. breeze : gale
B. hot : cold
C. ice : winter
D. cold : cool
MARKED ANSWER A. breeze : gale
WHY "breeze : gale" is right. It has the same link, lesser : greater degree, in the same order.
SHORTCUT Make a sentence for the stem: "cool is to cold" as lesser : greater degree. Test each choice in that sentence.

### 562 | CIVIO-ANA-SYLLOGISM-000563
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Assume these are true: every one of the judges is among the lawyers, and every one of the lawyers is among the bar members. What can be concluded for certain?
A. All bar members are judges.
B. No lawyers are judges.
C. Some bar members are not lawyers.
D. All judges are bar members.
MARKED ANSWER D. All judges are bar members.
WHY "All judges are bar members." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: judges inside lawyers, lawyers inside bar members. So judges sit inside bar members.

### 563 | CIVIO-ANA-SYMBOL-SERIES-000564
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What comes next in the series?  EP, HR, KT, NV, ___
A. XQ
B. QB
C. QX
D. OX
MARKED ANSWER C. QX
WHY QX is right: N + 3 = Q and V + 2 = X.
SHORTCUT Split each pair. First letters: E, H, K, N (jump +3). Second letters: P, R, T, V (jump +2). Move each one more step.

### 564 | CIVIO-ANA-ANALOGY-SYN-000565
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which pair shows the same relationship as "begin : start"?
A. start : stop
B. race : runner
C. end : finish
D. began : begun
MARKED ANSWER C. end : finish
WHY "end : finish" is right. It has the same link, similar meaning, in the same order.
SHORTCUT Make a sentence for the stem: "begin is to start" as similar meaning. Test each choice in that sentence.

### 565 | CIVIO-ANA-SYMBOL-SERIES-000566
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In a certain code, LEDGER is written as OHGJHU. How is PAPER written in the same code?
A. MXMBO
B. SDSHU
C. SDSHR
D. TETIV
MARKED ANSWER B. SDSHU
WHY SDSHU is right: each letter of PAPER moved 3 places forward.
SHORTCUT Compare the first letters: L became O. That is 3 places forward. Check one more letter, then shift every letter of PAPER the same way.

### 566 | CIVIO-VEN-WORD-MEANING-000567
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is closest in meaning to the word in capital letters?  RELUCTANT
A. eager
B. unwilling
C. relevant
D. resilient
MARKED ANSWER B. unwilling
WHY "unwilling" is right. "Reluctant" means unwilling.
SHORTCUT Make a short sentence with "reluctant", then swap in each choice. Watch for words that only look or sound like "reluctant".

### 567 | CIVIO-VEN-ERROR-AGREE-000568
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: The cost of the repairs ____ higher than the estimate.
A. is
B. being
C. be
D. are
MARKED ANSWER A. is
WHY "is" is right: "The cost" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The cost ____". The subject is singular, so use the singular verb.

### 568 | CIVIO-VEN-SENT-COMP-PHRASAL-000569
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the phrase that best completes the sentence: The team could not ____ the deadline and asked for more time.
A. keep up with
B. keep out
C. keep off
D. keep back
MARKED ANSWER A. keep up with
WHY "keep up with" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 569 | CIVIO-VEN-SENT-COMP-WORD-000570
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: The driver apologized ____ the delay.
A. on
B. of
C. to
D. for
MARKED ANSWER D. for
WHY "for" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 570 | CIVIO-VEN-ERROR-AGREE-000571
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: The results of the survey ____ that most residents want a clinic.
A. shows
B. show
C. showing
D. to show
MARKED ANSWER B. show
WHY "show" is right: "The results" is plural.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The results ____". The subject is plural, so use the plural verb.

### 571 | CIVIO-VEN-ERROR-AGREE-000572
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: Neither of the drivers ____ late this morning.
A. were
B. been
C. being
D. was
MARKED ANSWER D. was
WHY "was" is right: "Neither" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "Neither ____". The subject is singular, so use the singular verb.

### 572 | CIVIO-VEN-RC-VOCAB-000573
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The doctor gave a FIRM reminder to take the medicine.
A. strong and definite
B. vague
C. frozen
D. business company
MARKED ANSWER A. strong and definite
WHY "strong and definite" is right: it is the sense of "firm" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "firm".

### 573 | CIVIO-VEN-SENT-COMP-PHRASAL-000574
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the phrase that best completes the sentence: The meeting was ____ because of the typhoon.
A. called up
B. called on
C. called in
D. called off
MARKED ANSWER D. called off
WHY "called off" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 574 | CIVIO-VEN-WORD-MEANING-000575
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What does the phrase in capital letters mean?  The applicant was ON CLOUD NINE after passing the exam.
A. very happy
B. confused
C. on an airplane
D. very sad
MARKED ANSWER A. very happy
WHY "very happy" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 575 | CIVIO-VEN-WORD-MEANING-000576
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  ACCURATE
A. adequate
B. accustomed
C. wrong
D. correct
MARKED ANSWER C. wrong
WHY "wrong" is right. "Accurate" means correct; "wrong" is the reverse.
SHORTCUT First say what "accurate" means (correct). Then look for the word that means the reverse.

### 576 | CIVIO-VEN-ERROR-TENSE-000577
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the correct verb: Right now, the social welfare office staff ____ the relief goods.
A. is delivering
B. delivered
C. will have delivered
D. delivers
MARKED ANSWER A. is delivering
WHY "is delivering" is right: the present progressive matches "Right now".
SHORTCUT Find the time signal first: "Right now". It calls for the present progressive.

### 577 | CIVIO-VEN-WORD-MEANING-000578
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What does the phrase in capital letters mean?  After the audit, the officer had to FACE THE MUSIC.
A. accept the consequences
B. lose the job at once
C. avoid the blame
D. listen to a band
MARKED ANSWER A. accept the consequences
WHY "accept the consequences" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 578 | CIVIO-VEN-WORD-MEANING-000579
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  PUNCTUAL
A. punctured
B. practical
C. late
D. on time
MARKED ANSWER C. late
WHY "late" is right. "Punctual" means on time; "late" is the reverse.
SHORTCUT First say what "punctual" means (on time). Then look for the word that means the reverse.

### 579 | CIVIO-VEN-SENT-COMP-WORD-000580
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: The teacher and ____ will check the test papers.
A. mine
B. I
C. myself
D. me
MARKED ANSWER B. I
WHY "I" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 580 | CIVIO-VEN-WORD-MEANING-000581
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is closest in meaning to the word in capital letters?  LENIENT
A. tolerant
B. lean
C. strict
D. lending
MARKED ANSWER A. tolerant
WHY "tolerant" is right. "Lenient" means tolerant.
SHORTCUT Make a short sentence with "lenient", then swap in each choice. Watch for words that only look or sound like "lenient".

### 581 | CIVIO-VEN-WORD-MEANING-000582
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  VERIFY
A. doubt
B. vary
C. confirm
D. verbalize
MARKED ANSWER A. doubt
WHY "doubt" is right. "Verify" means confirm; "doubt" is the reverse.
SHORTCUT First say what "verify" means (confirm). Then look for the word that means the reverse.

### 582 | CIVIO-VEN-ERROR-AGREE-000583
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: Every one of the forms ____ a signature.
A. needing
B. needs
C. need
D. to need
MARKED ANSWER B. needs
WHY "needs" is right: "Every one" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "Every one ____". The subject is singular, so use the singular verb.

### 583 | CIVIO-VEN-ERROR-TENSE-000584
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the correct verb: In 2019, Joy ____ the plaza.
A. will have cleaned
B. cleaned
C. will clean
D. has cleaned
MARKED ANSWER B. cleaned
WHY "cleaned" is right: the simple past matches "In 2019".
SHORTCUT Find the time signal first: "In 2019". It calls for the simple past.

### 584 | CIVIO-VEN-SENT-COMP-WORD-000585
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Choose the word that best completes the sentence: The truck stayed ____ in the traffic for an hour.
A. stationary
B. stationed
C. standing
D. stationery
MARKED ANSWER A. stationary
WHY "stationary" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 585 | CIVIO-VEN-WORD-MEANING-000586
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is closest in meaning to the word in capital letters?  AUTHENTIC
A. genuine
B. authority
C. fake
D. automatic
MARKED ANSWER A. genuine
WHY "genuine" is right. "Authentic" means genuine.
SHORTCUT Make a short sentence with "authentic", then swap in each choice. Watch for words that only look or sound like "authentic".

### 586 | CIVIO-CLR-SPELL-WRONG-000587
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is misspelled?  exaggerate | requisition | sieze | license
A. exaggerate
B. requisition
C. sieze
D. license
MARKED ANSWER C. sieze
WHY "sieze" is misspelled: it swaps the order of i and e. The correct spelling is "seize".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 587 | CIVIO-CLR-SPELL-WRONG-000588
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is misspelled?  questionnaire | rhythm | defintely | maintenance
A. questionnaire
B. rhythm
C. defintely
D. maintenance
MARKED ANSWER C. defintely
WHY "defintely" is misspelled: it drops a letter. The correct spelling is "definitely".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 588 | CIVIO-CLR-FILE-POSITION-000589
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In alphabetical filing, which name is filed LAST?  Atty. Evelyn A. Aquino | Ernesto R. Reyes | Dr. Rafael N. San Pedro | Dr. Teresita S. Cruz
A. Dr. Teresita S. Cruz
B. Ernesto R. Reyes
C. Dr. Rafael N. San Pedro
D. Atty. Evelyn A. Aquino
MARKED ANSWER C. Dr. Rafael N. San Pedro
WHY "Dr. Rafael N. San Pedro" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Atty. Evelyn A. Aquino → AQUINO, Evelyn; Dr. Teresita S. Cruz → CRUZ, Teresita; Ernesto R. Reyes → REYES, Ernesto; Dr. Rafael N. San Pedro → SANPEDRO, Rafael.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 589 | CIVIO-CLR-SPELL-WRONG-000590
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is misspelled?  seze | personnel | lieutenant | beginning
A. seze
B. personnel
C. lieutenant
D. beginning
MARKED ANSWER A. seze
WHY "seze" is misspelled: it drops a letter. The correct spelling is "seize".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 590 | CIVIO-CLR-SPELL-RIGHT-000591
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is spelled correctly?  transfrred | trnsferred | transferred | transfered
A. transfrred
B. trnsferred
C. transferred
D. transfered
MARKED ANSWER C. transferred
WHY "transferred" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 591 | CIVIO-CLR-FILE-POSITION-000592
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In alphabetical filing, which name is filed FIRST?  Atty. Ramon C. San Pedro | Jose L. Dela Cruz | Imelda D. Cruz | Alfredo B. Ocampo
A. Imelda D. Cruz
B. Atty. Ramon C. San Pedro
C. Alfredo B. Ocampo
D. Jose L. Dela Cruz
MARKED ANSWER A. Imelda D. Cruz
WHY "Imelda D. Cruz" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Imelda D. Cruz → CRUZ, Imelda; Jose L. Dela Cruz → DELACRUZ, Jose; Alfredo B. Ocampo → OCAMPO, Alfredo; Atty. Ramon C. San Pedro → SANPEDRO, Ramon.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 592 | CIVIO-CLR-FILE-POSITION-000593
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In alphabetical filing, which name is filed LAST?  Ana R. De Guzman | Evelyn C. Santos-Ocampo | Victoria P. Rivera | Cristina F. Dela Torre
A. Ana R. De Guzman
B. Evelyn C. Santos-Ocampo
C. Cristina F. Dela Torre
D. Victoria P. Rivera
MARKED ANSWER B. Evelyn C. Santos-Ocampo
WHY "Evelyn C. Santos-Ocampo" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Ana R. De Guzman → DEGUZMAN, Ana; Cristina F. Dela Torre → DELATORRE, Cristina; Victoria P. Rivera → RIVERA, Victoria; Evelyn C. Santos-Ocampo → SANTOSOCAMPO, Evelyn.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 593 | CIVIO-CLR-FILE-POSITION-000594
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In alphabetical filing, which name is filed FIRST?  Nora N. Delos Reyes | Lourdes T. Manalo | Rosario C. Dela Torre | Engr. Corazon N. Santos-Ocampo
A. Lourdes T. Manalo
B. Rosario C. Dela Torre
C. Nora N. Delos Reyes
D. Engr. Corazon N. Santos-Ocampo
MARKED ANSWER B. Rosario C. Dela Torre
WHY "Rosario C. Dela Torre" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Rosario C. Dela Torre → DELATORRE, Rosario; Nora N. Delos Reyes → DELOSREYES, Nora; Lourdes T. Manalo → MANALO, Lourdes; Engr. Corazon N. Santos-Ocampo → SANTOSOCAMPO, Corazon.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 594 | CIVIO-CLR-FILE-POSITION-000595
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In alphabetical filing, which name is filed LAST?  Mario F. San Pedro | Engr. Nora F. Manalo | Teresita R. Cruz-Manalo | Engr. Corazon T. Bautista
A. Engr. Nora F. Manalo
B. Engr. Corazon T. Bautista
C. Mario F. San Pedro
D. Teresita R. Cruz-Manalo
MARKED ANSWER C. Mario F. San Pedro
WHY "Mario F. San Pedro" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Engr. Corazon T. Bautista → BAUTISTA, Corazon; Teresita R. Cruz-Manalo → CRUZMANALO, Teresita; Engr. Nora F. Manalo → MANALO, Nora; Mario F. San Pedro → SANPEDRO, Mario.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 595 | CIVIO-CLR-SPELL-WRONG-000596
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is misspelled?  threshld | requisition | occurred | questionnaire
A. threshld
B. requisition
C. occurred
D. questionnaire
MARKED ANSWER A. threshld
WHY "threshld" is misspelled: it drops a letter. The correct spelling is "threshold".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 596 | CIVIO-CLR-FILE-POSITION-000597
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
In alphabetical filing, which name is filed LAST?  Rosario M. Flores | Felipe T. Castillo | Benito B. Pedro | Ana N. San Pedro
A. Benito B. Pedro
B. Ana N. San Pedro
C. Felipe T. Castillo
D. Rosario M. Flores
MARKED ANSWER B. Ana N. San Pedro
WHY "Ana N. San Pedro" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Felipe T. Castillo → CASTILLO, Felipe; Rosario M. Flores → FLORES, Rosario; Benito B. Pedro → PEDRO, Benito; Ana N. San Pedro → SANPEDRO, Ana.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 597 | CIVIO-CLR-SPELL-RIGHT-000598
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is spelled correctly?  guerantee | guarantee | guarrantee | guarntee
A. guerantee
B. guarantee
C. guarrantee
D. guarntee
MARKED ANSWER B. guarantee
WHY "guarantee" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 598 | CIVIO-CLR-SPELL-WRONG-000599
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is misspelled?  reimbursement | achievement | conscince | phenomenon
A. reimbursement
B. achievement
C. conscince
D. phenomenon
MARKED ANSWER C. conscince
WHY "conscince" is misspelled: it drops a letter. The correct spelling is "conscience".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 599 | CIVIO-CLR-SPELL-WRONG-000600
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is misspelled?  entrepreneur | separate | grivance | accommodate
A. entrepreneur
B. separate
C. grivance
D. accommodate
MARKED ANSWER C. grivance
WHY "grivance" is misspelled: it drops a letter. The correct spelling is "grievance".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 600 | CIVIO-CLR-SPELL-RIGHT-000601
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which word is spelled correctly?  begnning | beginning | begining | beginnng
A. begnning
B. beginning
C. begining
D. beginnng
MARKED ANSWER B. beginning
WHY "beginning" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 601 | CIVIO-GI-TERM-MATCH-000602
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Under R.A. 6713, what is a "public official"?
A. Only elected officials
B. Only permanent, paid employees
C. An elective or appointive official, permanent or temporary, career or non-career, with or without pay
D. Only officials with salary grade 25 and up
MARKED ANSWER C. An elective or appointive official, permanent or temporary, career or non-career, with or without pay
WHY "An elective or appointive official, permanent or temporary, career or non-career, with or without pay" is right. R.A. 6713, Sec. 3(b) says: "whether in the career or non-career service, including military and police personnel, whether or not they receive compensation".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 3(b). The term is broad.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 602 | CIVIO-GI-TERM-MATCH-000603
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Under the 1987 Constitution, who among these is a citizen of the Philippines?
A. Anyone who has lived in the Philippines for five years
B. Those whose fathers or mothers are citizens of the Philippines
C. Anyone married to a Filipino
D. Anyone born on Philippine soil, whatever the parents' citizenship
MARKED ANSWER B. Those whose fathers or mothers are citizens of the Philippines
WHY "Those whose fathers or mothers are citizens of the Philippines" is right. Art. IV, Sec. 1(2) says: "Those whose fathers or mothers are citizens of the Philippines".
SHORTCUT Tie the fact to its section: Art. IV, Sec. 1(2). Citizenship follows the parents (jus sanguinis).
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 603 | CIVIO-GI-TERM-MATCH-000604
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Which right is recognized by Art. III, Sec. 7 of the 1987 Constitution?
A. The right to government employment
B. The right to free legal service in civil cases
C. The right of the people to information on matters of public concern
D. The right to strike
MARKED ANSWER C. The right of the people to information on matters of public concern
WHY "The right of the people to information on matters of public concern" is right. Art. III, Sec. 7 says: "The right of the people to information on matters of public concern shall be recognized".
SHORTCUT Tie the fact to its section: Art. III, Sec. 7. Right to information.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 604 | CIVIO-GI-DEADLINE-NUMBER-000605
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What is the minimum age to vote under the 1987 Constitution?
A. 21 years old
B. 15 years old
C. 18 years old
D. 16 years old
MARKED ANSWER C. 18 years old
WHY "18 years old" is right. Art. V, Sec. 1 says: "at least eighteen years of age".
SHORTCUT Tie the fact to its section: Art. V, Sec. 1. Suffrage starts at 18.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 605 | CIVIO-GI-DEADLINE-NUMBER-000606
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What is the minimum age to be appointed a member of the Supreme Court?
A. 50 years old
B. 40 years old
C. 35 years old
D. 45 years old
MARKED ANSWER B. 40 years old
WHY "40 years old" is right. Art. VIII, Sec. 7(1) says: "must be at least forty years of age".
SHORTCUT Tie the fact to its section: Art. VIII, Sec. 7(1). A Justice must be at least 40.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 606 | CIVIO-GI-DEADLINE-NUMBER-000607
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
How many consecutive terms may a Member of the House of Representatives serve?
A. Two
B. One
C. Three
D. Four
MARKED ANSWER C. Three
WHY "Three" is right. Art. VI, Sec. 7 says: "No member of the House of Representatives shall serve for more than three consecutive terms".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 7. A House Member may serve up to three terms in a row.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 607 | CIVIO-GI-TERM-MATCH-000608
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Under Art. II, Sec. 28, the State adopts and implements a policy of full public disclosure of what?
A. All its transactions involving public interest
B. Only its budget
C. All military plans
D. All private bank accounts
MARKED ANSWER A. All its transactions involving public interest
WHY "All its transactions involving public interest" is right. Art. II, Sec. 28 says: "full public disclosure of all its transactions involving public interest".
SHORTCUT Tie the fact to its section: Art. II, Sec. 28. Full public disclosure, subject to law.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 608 | CIVIO-GI-TERM-MATCH-000609
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
What may NOT be imposed as a requirement for voting?
A. Age
B. Residence
C. Citizenship
D. Literacy, property, or other substantive requirement
MARKED ANSWER D. Literacy, property, or other substantive requirement
WHY "Literacy, property, or other substantive requirement" is right. Art. V, Sec. 1 says: "No literacy, property, or other substantive requirement shall be imposed".
SHORTCUT Tie the fact to its section: Art. V, Sec. 1. Age, citizenship and residence are allowed; literacy and property tests are not.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 609 | CIVIO-GI-TERM-MATCH-000610
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
Under R.A. 6713, extending prompt, courteous and adequate service to the public is part of which norm of conduct?
A. Simple living
B. Responsiveness to the public
C. Commitment to democracy
D. Nationalism and patriotism
MARKED ANSWER B. Responsiveness to the public
WHY "Responsiveness to the public" is right. R.A. 6713, Sec. 4(A) says: "Responsiveness to the public".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). Sec. 4(A)(e).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 610 | CIVIO-GI-DEADLINE-NUMBER-000611
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-007.json
STEM
How often may impeachment proceedings be initiated against the same official?
A. Once every term
B. Once every six months
C. Not more than twice a year
D. Not more than once within a period of one year
MARKED ANSWER D. Not more than once within a period of one year
WHY "Not more than once within a period of one year" is right. Art. XI, Sec. 3(5) says: "No impeachment proceedings shall be initiated against the same official more than once within a period of one year".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 3(5). The one-year bar.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 611 | CIVIO-NUM-WP-PCT-CHANGE-000612
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A pair of school shoes is priced at ₱1,200. It is sold at 30% off. How much does a buyer pay?
A. ₱840
B. ₱1,170
C. ₱360
D. ₱1,560
MARKED ANSWER A. ₱840
WHY ₱840 is right. Check: discount ₱360; ₱1,200 − ₱360 = ₱840.
SHORTCUT Pay 70% of the price: ₱1,200 × 0.7 = ₱840.

### 612 | CIVIO-NUM-WP-PCT-CHANGE-000613
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A hardware store sold a set of school uniforms for ₱150. It raised the price by 50%. Later, it lowered the new price by 40%. What is the final price?
A. ₱202.50
B. ₱225
C. ₱165
D. ₱135
MARKED ANSWER D. ₱135
WHY ₱135 is right. Check: 150 × 1.5 = 225, and 225 × 0.6 = 135.
SHORTCUT Do one change at a time. ₱150 up 50% is ₱150 + ₱75 = ₱225. Then 40% of ₱225 is ₱90, so ₱225 − ₱90 = ₱135.

### 613 | CIVIO-NUM-SEQ-DIFF-000614
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Find the next number in the series.  2, 5, 11, 20, 32, ___
A. 50
B. 35
C. 47
D. 44
MARKED ANSWER C. 47
WHY 47 is right: 32 + 15 = 47.
SHORTCUT Write the jumps under the list: +3, +6, +9, +12. Each jump is 3 more than the one before. So the next jump is +15.

### 614 | CIVIO-NUM-SEQ-DIFF-000615
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What number comes next in the series?  15, 21, 28, 36, 45, ___
A. 56
B. 54
C. 51
D. 55
MARKED ANSWER D. 55
WHY 55 is right: 45 + 10 = 55.
SHORTCUT Write the jumps under the list: +6, +7, +8, +9. Each jump is 1 more than the one before. So the next jump is +10.

### 615 | CIVIO-NUM-SEQ-MULT-000616
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What number comes next?  3, 9, 21, 45, 93, ___
A. 192
B. 189
C. 186
D. 141
MARKED ANSWER B. 189
WHY 189 is right: 93 × 2 = 186, then + 3 gives 189.
SHORTCUT Test "times 2, then + 3" on the first numbers: 3 × 2 + 3 = 9; 9 × 2 + 3 = 21. It works, so use it on 93.

### 616 | CIVIO-NUM-SEQ-MULT-000617
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What number comes next?  1, 5, 17, 53, 161, ___
A. 483
B. 269
C. 487
D. 485
MARKED ANSWER D. 485
WHY 485 is right: 161 × 3 = 483, then + 2 gives 485.
SHORTCUT Test "times 3, then + 2" on the first numbers: 1 × 3 + 2 = 5; 5 × 3 + 2 = 17. It works, so use it on 161.

### 617 | CIVIO-NUM-OPS-ORDER-000618
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What is the value of 14 + 3 × 8 − 7?
A. 18
B. 31
C. 17
D. 129
MARKED ANSWER B. 31
WHY 31 is right: 14 + 24 = 38, and 38 − 7 = 31.
SHORTCUT Circle the × first: 3 × 8 = 24. Then go left to right: 14 + 24 − 7.

### 618 | CIVIO-NUM-SEQ-MULT-000619
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What number comes next?  3, 12, 39, 120, 363, ___
A. 606
B. 1089
C. 1095
D. 1092
MARKED ANSWER D. 1092
WHY 1092 is right: 363 × 3 = 1089, then + 3 gives 1092.
SHORTCUT Test "times 3, then + 3" on the first numbers: 3 × 3 + 3 = 12; 12 × 3 + 3 = 39. It works, so use it on 363.

### 619 | CIVIO-NUM-WP-PCT-CHANGE-000620
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A backpack is priced at ₱640. It is sold at 35% off. How much does a buyer pay?
A. ₱416
B. ₱864
C. ₱224
D. ₱605
MARKED ANSWER A. ₱416
WHY ₱416 is right. Check: discount ₱224; ₱640 − ₱224 = ₱416.
SHORTCUT Pay 65% of the price: ₱640 × 0.65 = ₱416.

### 620 | CIVIO-NUM-WP-GEOM-000621
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A rectangular basketball court is 19 m long and 4 m wide. A lace border costs ₱120 per meter. How much will it cost to put the lace border around the whole basketball court?
A. ₱46
B. ₱9,120
C. ₱2,760
D. ₱5,520
MARKED ANSWER D. ₱5,520
WHY ₱5,520 is right: 46 m × ₱120 = ₱5,520.
SHORTCUT Around = 2 × (19 + 4) = 46 m. Cost = 46 × ₱120.

### 621 | CIVIO-NUM-WP-GEOM-000622
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A rectangular school lot is 12 m long and 20 m wide. A lace border costs ₱40 per meter. How much will it cost to put the lace border around the whole school lot?
A. ₱64
B. ₱1,280
C. ₱2,560
D. ₱9,600
MARKED ANSWER C. ₱2,560
WHY ₱2,560 is right: 64 m × ₱40 = ₱2,560.
SHORTCUT Around = 2 × (12 + 20) = 64 m. Cost = 64 × ₱40.

### 622 | CIVIO-NUM-WP-PCT-CHANGE-000623
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A electric fan is priced at ₱1,500. It is sold at 15% off. How much does a buyer pay?
A. ₱1,485
B. ₱1,725
C. ₱1,275
D. ₱225
MARKED ANSWER C. ₱1,275
WHY ₱1,275 is right. Check: discount ₱225; ₱1,500 − ₱225 = ₱1,275.
SHORTCUT Pay 85% of the price: ₱1,500 × 0.85 = ₱1,275.

### 623 | CIVIO-NUM-WP-ALGEBRA-000624
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Lourdes is 5 times as old as her niece. In 14 years, Lourdes will be three times as old as the niece. How old is Lourdes now?
A. 28
B. 14
C. 84
D. 70
MARKED ANSWER D. 70
WHY 70 is right. Algebra: niece = s, Lourdes = 5s; 5s + 14 = 3(s + 14) gives s = 14, so Lourdes = 70.
SHORTCUT Try the choices. If Lourdes is 70, the niece is 14. In 14 years: 84 and 28. 84 = 3 × 28, so it works.

### 624 | CIVIO-NUM-WP-RATIO-000625
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Aling Rosa and Paolo will share ₱9,600 of allowance fund in the ratio 3 : 5. How much is Paolo's share?
A. ₱6,000
B. ₱1,920
C. ₱3,600
D. ₱1,200
MARKED ANSWER A. ₱6,000
WHY ₱6,000 is right: 5 × ₱1,200 = ₱6,000. Check: ₱3,600 + ₱6,000 = ₱9,600.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 5 = 8. One part = ₱9,600 ÷ 8 = ₱1,200. Then multiply by the parts you need.

### 625 | CIVIO-NUM-FRAC-DEC-000626
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A barangay had 1200 sacks of relief rice. It gave out 3/8 of them on Monday and 3/5 of the remaining sacks of relief rice on Tuesday. How many are left?
A. 450
B. 300
C. 750
D. 30
MARKED ANSWER B. 300
WHY 300 is right. Check: 450 + 450 + 300 = 1200.
SHORTCUT Go day by day. Monday: 3/8 of 1200 = 450, so 750 left. Tuesday: 3/5 of 750 = 450, so 750 − 450 = 300 left.

### 626 | CIVIO-NUM-SEQ-DIFF-000627
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What number comes next in the series?  5, 6, 10, 17, 27, ___
A. 43
B. 40
C. 28
D. 37
MARKED ANSWER B. 40
WHY 40 is right: 27 + 13 = 40.
SHORTCUT Write the jumps under the list: +1, +4, +7, +10. Each jump is 3 more than the one before. So the next jump is +13.

### 627 | CIVIO-NUM-WP-AVERAGE-000628
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
The average age of the 8 clerks in the municipal health office is 28 years. One more person, with 55 years, joins them. What is the new average age?
A. 279 years
B. 31.38 years
C. 31 years
D. 41.5 years
MARKED ANSWER C. 31 years
WHY 31 years is right. Long way: 8 × 28 = 224; + 55 = 279; ÷ 9 = 31.
SHORTCUT The new person is 55 − 28 = 27 above the old average. Share that among all 9 people: 27 ÷ 9 = 3. Add it: 28 + 3 = 31.

### 628 | CIVIO-NUM-WP-RATIO-000629
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Inday and Dindo will share ₱25,000 of cleanup fund in the ratio 3 : 7. How much is Dindo's share?
A. ₱17,500
B. ₱7,500
C. ₱3,571.43
D. ₱2,500
MARKED ANSWER A. ₱17,500
WHY ₱17,500 is right: 7 × ₱2,500 = ₱17,500. Check: ₱7,500 + ₱17,500 = ₱25,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱25,000 ÷ 10 = ₱2,500. Then multiply by the parts you need.

### 629 | CIVIO-NUM-WP-AVERAGE-000630
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
The average years of service of the 7 barangay health workers in the public market office is 15 years. One more person, with 23 years, joins them. What is the new average years of service?
A. 16.14 years
B. 16 years
C. 128 years
D. 19 years
MARKED ANSWER B. 16 years
WHY 16 years is right. Long way: 7 × 15 = 105; + 23 = 128; ÷ 8 = 16.
SHORTCUT The new person is 23 − 15 = 8 above the old average. Share that among all 8 people: 8 ÷ 8 = 1. Add it: 15 + 1 = 16.

### 630 | CIVIO-NUM-WP-RATE-000631
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Cora can paint a classroom in 40 hours. Aileen can do the same job in 10 hours. Working together, how long will they take?
A. 7.5 hours
B. 8 hours
C. 25 hours
D. 50 hours
MARKED ANSWER B. 8 hours
WHY 8 hours is right. Check: in 8 hours, Cora does 8/40 and Aileen does 8/10; together that is 1 whole job.
SHORTCUT Per hour, Cora does 1/40 and Aileen does 1/10. Together: 1/40 + 1/10 = 1/8. So the whole job takes 8 hours.

### 631 | CIVIO-NUM-FRAC-DEC-000632
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A barangay had 1440 rolls of tarpaulin. It gave out 1/8 of them on Monday and 3/5 of the remaining rolls of tarpaulin on Tuesday. How many are left?
A. 1260
B. 396
C. 756
D. 504
MARKED ANSWER D. 504
WHY 504 is right. Check: 180 + 756 + 504 = 1440.
SHORTCUT Go day by day. Monday: 1/8 of 1440 = 180, so 1260 left. Tuesday: 3/5 of 1260 = 756, so 1260 − 756 = 504 left.

### 632 | CIVIO-NUM-WP-GEOM-000633
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A rectangular school lot is 25 m long and 13 m wide. A fence costs ₱120 per meter. How much will it cost to put the fence around the whole school lot?
A. ₱4,560
B. ₱39,000
C. ₱9,120
D. ₱76
MARKED ANSWER C. ₱9,120
WHY ₱9,120 is right: 76 m × ₱120 = ₱9,120.
SHORTCUT Around = 2 × (25 + 13) = 76 m. Cost = 76 × ₱120.

### 633 | CIVIO-NUM-WP-RATE-000634
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Nestor can inventory a supply room in 10 hours. Rhea can do the same job in 15 hours. Working together, how long will they take?
A. 6 hours
B. 10 minutes
C. 25 hours
D. 12.5 hours
MARKED ANSWER A. 6 hours
WHY 6 hours is right. Check: in 6 hours, Nestor does 6/10 and Rhea does 6/15; together that is 1 whole job.
SHORTCUT Per hour, Nestor does 1/10 and Rhea does 1/15. Together: 1/10 + 1/15 = 1/6. So the whole job takes 6 hours.

### 634 | CIVIO-NUM-WP-RATE-000635
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Mang Jun can repack the relief goods in 6 hours. Efren can do the same job in 12 hours. Working together, how long will they take?
A. 15 minutes
B. 18 hours
C. 9 hours
D. 4 hours
MARKED ANSWER D. 4 hours
WHY 4 hours is right. Check: in 4 hours, Mang Jun does 4/6 and Efren does 4/12; together that is 1 whole job.
SHORTCUT Per hour, Mang Jun does 1/6 and Efren does 1/12. Together: 1/6 + 1/12 = 1/4. So the whole job takes 4 hours.

### 635 | CIVIO-NUM-WP-PCT-CHANGE-000636
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A sari-sari store sold a set of school uniforms for ₱400. It raised the price by 40%. Later, it lowered the new price by 30%. What is the final price?
A. ₱392
B. ₱560
C. ₱440
D. ₱548.80
MARKED ANSWER A. ₱392
WHY ₱392 is right. Check: 400 × 1.4 = 560, and 560 × 0.7 = 392.
SHORTCUT Do one change at a time. ₱400 up 40% is ₱400 + ₱160 = ₱560. Then 30% of ₱560 is ₱168, so ₱560 − ₱168 = ₱392.

### 636 | CIVIO-NUM-WP-RATIO-000637
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A ₱14,400 commission is divided between Mylene and Aling Rosa in the ratio 5 : 7. What is Aling Rosa's share?
A. ₱8,400
B. ₱6,000
C. ₱2,057.14
D. ₱1,200
MARKED ANSWER A. ₱8,400
WHY ₱8,400 is right: 7 × ₱1,200 = ₱8,400. Check: ₱6,000 + ₱8,400 = ₱14,400.
SHORTCUT Add the ratio numbers to get equal parts: 5 + 7 = 12. One part = ₱14,400 ÷ 12 = ₱1,200. Then multiply by the parts you need.

### 637 | CIVIO-NUM-OPS-ORDER-000638
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What is the value of 8 + 4 × 7 − 2?
A. 82
B. 28
C. 34
D. 17
MARKED ANSWER C. 34
WHY 34 is right: 8 + 28 = 36, and 36 − 2 = 34.
SHORTCUT Circle the × first: 4 × 7 = 28. Then go left to right: 8 + 28 − 2.

### 638 | CIVIO-NUM-WP-PCT-CHANGE-000639
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
A hardware store sold a bag of cement for ₱800. It raised the price by 30%. Later, it lowered the new price by 20%. What is the final price?
A. ₱880
B. ₱1,040
C. ₱832
D. ₱1,081.60
MARKED ANSWER C. ₱832
WHY ₱832 is right. Check: 800 × 1.3 = 1,040, and 1,040 × 0.8 = 832.
SHORTCUT Do one change at a time. ₱800 up 30% is ₱800 + ₱240 = ₱1,040. Then 20% of ₱1,040 is ₱208, so ₱1,040 − ₱208 = ₱832.

### 639 | CIVIO-NUM-OPS-ORDER-000640
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What is the value of 18 + 3 × 2 − 6?
A. 17
B. 6
C. 18
D. 36
MARKED ANSWER C. 18
WHY 18 is right: 18 + 6 = 24, and 24 − 6 = 18.
SHORTCUT Circle the × first: 3 × 2 = 6. Then go left to right: 18 + 6 − 6.

### 640 | CIVIO-NUM-WP-AVERAGE-000641
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
The average age of the 8 drivers in the city treasurer's office is 40 years. One more person, with 58 years, joins them. What is the new average age?
A. 378 years
B. 42 years
C. 49 years
D. 42.25 years
MARKED ANSWER B. 42 years
WHY 42 years is right. Long way: 8 × 40 = 320; + 58 = 378; ÷ 9 = 42.
SHORTCUT The new person is 58 − 40 = 18 above the old average. Share that among all 9 people: 18 ÷ 9 = 2. Add it: 40 + 2 = 42.

### 641 | CIVIO-ANA-SYLLOGISM-000642
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Statement 1: All workers are persons with IDs. Statement 2: All drivers are workers. Which conclusion follows from both statements?
A. All drivers are persons with IDs.
B. Some persons with IDs are not workers.
C. All persons with IDs are drivers.
D. No workers are drivers.
MARKED ANSWER A. All drivers are persons with IDs.
WHY "All drivers are persons with IDs." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: drivers inside workers, workers inside persons with IDs. So drivers sit inside persons with IDs.

### 642 | CIVIO-ANA-SYLLOGISM-000643
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Assume these are true: a few of the bridges are imported goods, and all of the bridges are structures. What can be concluded for certain?
A. Some structures are imported goods.
B. All imported goods are bridges.
C. No structures are imported goods.
D. All structures are imported goods.
MARKED ANSWER A. Some structures are imported goods.
WHY "Some structures are imported goods." is right. It follows from the two statements with no extra facts.
SHORTCUT The bridges who are imported goods are also structures. So at least some structures are imported goods.

### 643 | CIVIO-ANA-SYMBOL-SERIES-000644
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In a certain code, VOTER is written as YRWHU. How is MAYOR written in the same code?
A. JXVLO
B. QECSV
C. PDBRR
D. PDBRU
MARKED ANSWER D. PDBRU
WHY PDBRU is right: each letter of MAYOR moved 3 places forward.
SHORTCUT Compare the first letters: V became Y. That is 3 places forward. Check one more letter, then shift every letter of MAYOR the same way.

### 644 | CIVIO-ANA-SYLLOGISM-000645
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
All farmers are producers. Some farmers are scholars. Which conclusion must be true?
A. Some producers are scholars.
B. No producers are scholars.
C. All producers are scholars.
D. All scholars are farmers.
MARKED ANSWER A. Some producers are scholars.
WHY "Some producers are scholars." is right. It follows from the two statements with no extra facts.
SHORTCUT The farmers who are scholars are also producers. So at least some producers are scholars.

### 645 | CIVIO-ANA-SYMBOL-SERIES-000646
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In a certain code, STAMP is written as TUBNQ. How is CENSUS written in the same code?
A. EGPUWU
B. BDMRTR
C. DFOTVS
D. DFOTVT
MARKED ANSWER D. DFOTVT
WHY DFOTVT is right: each letter of CENSUS moved 1 place forward.
SHORTCUT Compare the first letters: S became T. That is 1 place forward. Check one more letter, then shift every letter of CENSUS the same way.

### 646 | CIVIO-ANA-SYMBOL-SERIES-000647
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What comes next in the series?  BK, FM, JO, NQ, ___
A. OS
B. RA
C. SR
D. RS
MARKED ANSWER D. RS
WHY RS is right: N + 4 = R and Q + 2 = S.
SHORTCUT Split each pair. First letters: B, F, J, N (jump +4). Second letters: K, M, O, Q (jump +2). Move each one more step.

### 647 | CIVIO-ANA-CONCLUSION-000648
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Four staff members are compared. Inday has served longer than Bong. Bong has served longer than Analyn. Grace has served longer than Inday. Who is third in the order (counting from the one who has served the longest)?
A. Grace
B. Analyn
C. Bong
D. Inday
MARKED ANSWER C. Bong
WHY Bong is right. The clues give Grace → Inday → Bong → Analyn, so Bong is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Grace → Inday → Bong → Analyn.

### 648 | CIVIO-ANA-SYMBOL-SERIES-000649
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In a certain code, CENSUS is written as FHQVXV. How is MAYOR written in the same code?
A. PDBRR
B. PDBRU
C. QECSV
D. JXVLO
MARKED ANSWER B. PDBRU
WHY PDBRU is right: each letter of MAYOR moved 3 places forward.
SHORTCUT Compare the first letters: C became F. That is 3 places forward. Check one more letter, then shift every letter of MAYOR the same way.

### 649 | CIVIO-ANA-CONCLUSION-000650
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Four staff members are compared. Grace has served longer than Bong. Kimberly has served longer than Grace. Bong has served longer than Tess. Who is third in the order (counting from the one who has served the longest)?
A. Bong
B. Kimberly
C. Grace
D. Tess
MARKED ANSWER A. Bong
WHY Bong is right. The clues give Kimberly → Grace → Bong → Tess, so Bong is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Kimberly → Grace → Bong → Tess.

### 650 | CIVIO-ANA-SYMBOL-SERIES-000651
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In a certain code, LIBRARY is written as KHAQZQX. How is CHAIR written in the same code?
A. BGZHQ
B. DIBJS
C. AFYGP
D. BGZHR
MARKED ANSWER A. BGZHQ
WHY BGZHQ is right: each letter of CHAIR moved 1 place back.
SHORTCUT Compare the first letters: L became K. That is 1 place back. Check one more letter, then shift every letter of CHAIR the same way.

### 651 | CIVIO-ANA-ANALOGY-PART-000652
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
FINGER : HAND :: ____
A. ring : jewel
B. arm : elbow
C. glove : hand
D. spoke : wheel
MARKED ANSWER D. spoke : wheel
WHY "spoke : wheel" is right. It has the same link, part : whole, in the same order.
SHORTCUT Make a sentence for the stem: "finger is to hand" as part : whole. Test each choice in that sentence.

### 652 | CIVIO-ANA-SYMBOL-SERIES-000653
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In a certain code, TAXES is written as UBYFT. How is AGENT written in the same code?
A. CIGPV
B. BHFOU
C. ZFDMS
D. BHFOT
MARKED ANSWER B. BHFOU
WHY BHFOU is right: each letter of AGENT moved 1 place forward.
SHORTCUT Compare the first letters: T became U. That is 1 place forward. Check one more letter, then shift every letter of AGENT the same way.

### 653 | CIVIO-ANA-SYLLOGISM-000654
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
All teachers are school staff. No school staff are smokers. Which conclusion must be true?
A. No government workers are smokers.
B. No teachers are smokers.
C. All school staff are teachers.
D. Some teachers are smokers.
MARKED ANSWER B. No teachers are smokers.
WHY "No teachers are smokers." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the teachers circle inside school staff. The "smokers" circle sits outside school staff, so it is outside teachers too.

### 654 | CIVIO-ANA-SYLLOGISM-000655
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Statement 1: Some tilapia are items marked for repair. Statement 2: All tilapia are fish. Which conclusion follows from both statements?
A. Some fish are items marked for repair.
B. No fish are items marked for repair.
C. All items marked for repair are tilapia.
D. All fish are items marked for repair.
MARKED ANSWER A. Some fish are items marked for repair.
WHY "Some fish are items marked for repair." is right. It follows from the two statements with no extra facts.
SHORTCUT The tilapia who are items marked for repair are also fish. So at least some fish are items marked for repair.

### 655 | CIVIO-ANA-CONCLUSION-000656
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Four staff members are compared. Datu scored higher than Bong. Efren scored higher than Datu. Bong scored higher than Paolo. Who is second in the order (counting from the one who got the highest score)?
A. Paolo
B. Efren
C. Datu
D. Bong
MARKED ANSWER C. Datu
WHY Datu is right. The clues give Efren → Datu → Bong → Paolo, so Datu is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Efren → Datu → Bong → Paolo.

### 656 | CIVIO-ANA-CONCLUSION-000657
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Four staff members are compared. Mylene finished the report earlier than Inday. Inday finished the report earlier than Cora. Bea finished the report earlier than Mylene. Who is second in the order (counting from the one who finished first)?
A. Cora
B. Mylene
C. Bea
D. Inday
MARKED ANSWER B. Mylene
WHY Mylene is right. The clues give Bea → Mylene → Inday → Cora, so Mylene is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Bea → Mylene → Inday → Cora.

### 657 | CIVIO-ANA-SYMBOL-SERIES-000658
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What comes next in the series?  GN, IO, KP, MQ, ___
A. NR
B. RO
C. OR
D. OV
MARKED ANSWER C. OR
WHY OR is right: M + 2 = O and Q + 1 = R.
SHORTCUT Split each pair. First letters: G, I, K, M (jump +2). Second letters: N, O, P, Q (jump +1). Move each one more step.

### 658 | CIVIO-ANA-ANALOGY-PART-000659
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which pair shows the same relationship as "minute : hour"?
A. year : month
B. centimeter : meter
C. second : fast
D. clock : time
MARKED ANSWER B. centimeter : meter
WHY "centimeter : meter" is right. It has the same link, smaller unit : larger unit, in the same order.
SHORTCUT Make a sentence for the stem: "minute is to hour" as smaller unit : larger unit. Test each choice in that sentence.

### 659 | CIVIO-ANA-SYMBOL-SERIES-000660
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What comes next in the series?  CM, EO, GQ, IS, ___
A. UK
B. JU
C. KV
D. KU
MARKED ANSWER D. KU
WHY KU is right: I + 2 = K and S + 2 = U.
SHORTCUT Split each pair. First letters: C, E, G, I (jump +2). Second letters: M, O, Q, S (jump +2). Move each one more step.

### 660 | CIVIO-ANA-SYMBOL-SERIES-000661
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What comes next in the series?  DM, HP, LS, PV, ___
A. TY
B. TC
C. YT
D. QY
MARKED ANSWER A. TY
WHY TY is right: P + 4 = T and V + 3 = Y.
SHORTCUT Split each pair. First letters: D, H, L, P (jump +4). Second letters: M, P, S, V (jump +3). Move each one more step.

### 661 | CIVIO-ANA-DI-TABLE-000662
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Supply use of envelopes (boxes) by office (Assessor: Apr 34, May 38, Jun 68; Planning: Apr 12, May 58, Jun 78; HR: Apr 78, May 74, Jun 32). In Jun, how many more did Planning use than HR?
A. 110
B. 66
C. 36
D. 46
MARKED ANSWER D. 46
WHY 46 is right: 78 − 32 = 46.
SHORTCUT Go to the Jun column: HR 32, Planning 78. Subtract the smaller from the larger.

### 662 | CIVIO-ANA-ASSUME-I-II-000663
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Statement: The library will extend its hours during exam week because more students come to study.
Assumption I: Students study only in libraries.
Assumption II: Demand for the library rises during exam week.
Which assumption is implicit in the statement?
A. Only II
B. Both I and II
C. Neither I nor II
D. Only I
MARKED ANSWER A. Only II
WHY "Only II" is right. Only assumption II is needed. I ("Students study only in libraries.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 663 | CIVIO-ANA-ASSUME-I-II-000664
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Statement: The mayor asked residents to report clogged canals through the new hotline.
Assumption I: Residents can reach the hotline.
Assumption II: The hotline will end all flooding in the town.
Which assumption is implicit in the statement?
A. Both I and II
B. Neither I nor II
C. Only II
D. Only I
MARKED ANSWER D. Only I
WHY "Only I" is right. Only assumption I is needed. II ("The hotline will end all flooding in the town.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 664 | CIVIO-ANA-ANALOGY-FUNCTION-000665
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Compass is to direction as ____.
A. time : watch
B. north : south
C. map : location
D. hiker : trail
MARKED ANSWER C. map : location
WHY "map : location" is right. It has the same link, tool : what it shows, in the same order.
SHORTCUT Make a sentence for the stem: "compass is to direction" as tool : what it shows. Test each choice in that sentence.

### 665 | CIVIO-ANA-SYMBOL-SERIES-000666
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What comes next in the series?  IN, MP, QR, UT, ___
A. YD
B. VY
C. YV
D. VV
MARKED ANSWER C. YV
WHY YV is right: U + 4 = Y and T + 2 = V.
SHORTCUT Split each pair. First letters: I, M, Q, U (jump +4). Second letters: N, P, R, T (jump +2). Move each one more step.

### 666 | CIVIO-VEN-ERROR-AGREE-000667
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: Everyone in the two offices ____ a shorter queue.
A. wants
B. want
C. to want
D. wanting
MARKED ANSWER A. wants
WHY "wants" is right: "Everyone" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "Everyone ____". The subject is singular, so use the singular verb.

### 667 | CIVIO-VEN-ERROR-TENSE-000668
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the correct verb: In 2019, Lourdes ____ the leave forms.
A. will have reviewed
B. will review
C. has reviewed
D. reviewed
MARKED ANSWER D. reviewed
WHY "reviewed" is right: the simple past matches "In 2019".
SHORTCUT Find the time signal first: "In 2019". It calls for the simple past.

### 668 | CIVIO-VEN-SENT-COMP-WORD-000669
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: Since the files were ____, the clerk found the record in seconds.
A. organic
B. organizing
C. scattered
D. organized
MARKED ANSWER D. organized
WHY "organized" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 669 | CIVIO-VEN-WORD-MEANING-000670
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is closest in meaning to the word in capital letters?  OBSOLETE
A. obstinate
B. modern
C. absolute
D. outdated
MARKED ANSWER D. outdated
WHY "outdated" is right. "Obsolete" means outdated.
SHORTCUT Make a short sentence with "obsolete", then swap in each choice. Watch for words that only look or sound like "obsolete".

### 670 | CIVIO-VEN-SENT-COMP-WORD-000671
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: ____ and the guard locked the office at six.
A. Herself
B. Hers
C. Her
D. She
MARKED ANSWER D. She
WHY "She" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 671 | CIVIO-VEN-WORD-MEANING-000672
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What does the phrase in capital letters mean?  The volunteers WENT THE EXTRA MILE during the relief drive.
A. walked a long way
B. worked without any rest for days
C. did more than expected
D. did the least possible
MARKED ANSWER C. did more than expected
WHY "did more than expected" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 672 | CIVIO-VEN-ERROR-AGREE-000673
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: The box of old receipts ____ more than ten kilos.
A. weighs
B. weighing
C. weigh
D. to weigh
MARKED ANSWER A. weighs
WHY "weighs" is right: "The box" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The box ____". The subject is singular, so use the singular verb.

### 673 | CIVIO-VEN-SENT-COMP-WORD-000674
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: The mayor's speech was ____; everyone understood the plan.
A. clean
B. clearly
C. confusing
D. clear
MARKED ANSWER D. clear
WHY "clear" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 674 | CIVIO-VEN-SENT-COMP-WORD-000675
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: Please put the signed forms over ____, on the second shelf.
A. theirs
B. they're
C. there
D. their
MARKED ANSWER C. there
WHY "there" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 675 | CIVIO-VEN-WORD-MEANING-000676
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What does the phrase in capital letters mean?  The plan to move the market is still UP IN THE AIR.
A. final
B. on an upper floor
C. cancelled
D. undecided
MARKED ANSWER D. undecided
WHY "undecided" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 676 | CIVIO-VEN-ERROR-TENSE-000677
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the correct verb: In 2019, Jun-jun ____ the attendance sheets.
A. has checked
B. will check
C. checked
D. will have checked
MARKED ANSWER C. checked
WHY "checked" is right: the simple past matches "In 2019".
SHORTCUT Find the time signal first: "In 2019". It calls for the simple past.

### 677 | CIVIO-VEN-WORD-MEANING-000678
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  COURTEOUS
A. rude
B. courageous
C. curious
D. polite
MARKED ANSWER A. rude
WHY "rude" is right. "Courteous" means polite; "rude" is the reverse.
SHORTCUT First say what "courteous" means (polite). Then look for the word that means the reverse.

### 678 | CIVIO-VEN-ERROR-TENSE-000679
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the correct verb: Two days ago, Bong ____ the plaza.
A. will clean
B. will have cleaned
C. cleaned
D. has cleaned
MARKED ANSWER C. cleaned
WHY "cleaned" is right: the simple past matches "Two days ago".
SHORTCUT Find the time signal first: "Two days ago". It calls for the simple past.

### 679 | CIVIO-VEN-RC-VOCAB-000680
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The report was DRAFTED by the planning office.
A. written in first form
B. finalized
C. called to the army
D. blown by wind
MARKED ANSWER A. written in first form
WHY "written in first form" is right: it is the sense of "drafted" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "drafted".

### 680 | CIVIO-VEN-ERROR-AGREE-000681
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: One of the barangay tanods ____ the school gate at night.
A. guards
B. guarding
C. to guard
D. guard
MARKED ANSWER A. guards
WHY "guards" is right: "One" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "One ____". The subject is singular, so use the singular verb.

### 681 | CIVIO-VEN-ERROR-TENSE-000682
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the correct verb: Right now, the engineering office staff ____ the drainage canal.
A. will have inspected
B. is inspecting
C. inspects
D. inspected
MARKED ANSWER B. is inspecting
WHY "is inspecting" is right: the present progressive matches "Right now".
SHORTCUT Find the time signal first: "Right now". It calls for the present progressive.

### 682 | CIVIO-VEN-SENT-COMP-WORD-000683
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: The ceremony is set ____ June 12.
A. in
B. on
C. at
D. to
MARKED ANSWER B. on
WHY "on" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 683 | CIVIO-VEN-SENT-COMP-WORD-000684
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: Each worker must keep the ____ of client records.
A. confidently
B. confidentiality
C. confident
D. confidence
MARKED ANSWER B. confidentiality
WHY "confidentiality" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 684 | CIVIO-VEN-SENT-COMP-WORD-000685
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: It was ____ who found the missing files.
A. them
B. their
C. themselves
D. they
MARKED ANSWER D. they
WHY "they" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 685 | CIVIO-VEN-SENT-COMP-WORD-000686
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Choose the word that best completes the sentence: The mayor will ____ the award to the best barangay.
A. present
B. represent
C. presence
D. presents
MARKED ANSWER A. present
WHY "present" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 686 | CIVIO-CLR-SPELL-RIGHT-000687
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  separte | separate | separrate | seperate
A. separte
B. separate
C. separrate
D. seperate
MARKED ANSWER B. separate
WHY "separate" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 687 | CIVIO-CLR-FILE-POSITION-000688
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed LAST?  Eduardo A. Cruz-Manalo | Engr. Lourdes R. Rivera | Cristina M. Dela Torre | Engr. Benito R. Tan
A. Engr. Lourdes R. Rivera
B. Cristina M. Dela Torre
C. Eduardo A. Cruz-Manalo
D. Engr. Benito R. Tan
MARKED ANSWER D. Engr. Benito R. Tan
WHY "Engr. Benito R. Tan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Eduardo A. Cruz-Manalo → CRUZMANALO, Eduardo; Cristina M. Dela Torre → DELATORRE, Cristina; Engr. Lourdes R. Rivera → RIVERA, Lourdes; Engr. Benito R. Tan → TAN, Benito.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 688 | CIVIO-CLR-SPELL-RIGHT-000689
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  entrepreneur | entreprenneur | entreprenur | entrpreneur
A. entrepreneur
B. entreprenneur
C. entreprenur
D. entrpreneur
MARKED ANSWER A. entrepreneur
WHY "entrepreneur" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 689 | CIVIO-CLR-FILE-POSITION-000690
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed FIRST?  Jose R. Del Rosario | Engr. Benito L. Delos Reyes | Atty. Nora P. Dela Cruz | Atty. Corazon M. De Guzman
A. Jose R. Del Rosario
B. Atty. Corazon M. De Guzman
C. Atty. Nora P. Dela Cruz
D. Engr. Benito L. Delos Reyes
MARKED ANSWER B. Atty. Corazon M. De Guzman
WHY "Atty. Corazon M. De Guzman" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Atty. Corazon M. De Guzman → DEGUZMAN, Corazon; Atty. Nora P. Dela Cruz → DELACRUZ, Nora; Engr. Benito L. Delos Reyes → DELOSREYES, Benito; Jose R. Del Rosario → DELROSARIO, Jose.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 690 | CIVIO-CLR-SPELL-RIGHT-000691
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  lieutenant | lieutennt | leiutenant | lieutennant
A. lieutenant
B. lieutennt
C. leiutenant
D. lieutennant
MARKED ANSWER A. lieutenant
WHY "lieutenant" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 691 | CIVIO-CLR-SPELL-RIGHT-000692
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  disbursement | disbursemant | disbursemment | disbursment
A. disbursement
B. disbursemant
C. disbursemment
D. disbursment
MARKED ANSWER A. disbursement
WHY "disbursement" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 692 | CIVIO-CLR-FILE-POSITION-000693
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed FIRST?  Engr. Elena D. De los Santos | Gloria C. Santos-Ocampo | Ernesto M. Leon | Teresita P. Del Mundo
A. Engr. Elena D. De los Santos
B. Gloria C. Santos-Ocampo
C. Teresita P. Del Mundo
D. Ernesto M. Leon
MARKED ANSWER C. Teresita P. Del Mundo
WHY "Teresita P. Del Mundo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Teresita P. Del Mundo → DELMUNDO, Teresita; Engr. Elena D. De los Santos → DELOSSANTOS, Elena; Ernesto M. Leon → LEON, Ernesto; Gloria C. Santos-Ocampo → SANTOSOCAMPO, Gloria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 693 | CIVIO-CLR-SPELL-RIGHT-000694
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  collague | coleague | colleague | collegue
A. collague
B. coleague
C. colleague
D. collegue
MARKED ANSWER C. colleague
WHY "colleague" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 694 | CIVIO-CLR-FILE-POSITION-000695
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed LAST?  Liza F. Manalo | Atty. Benito N. Pascual | Dr. Rosario D. Cruz-Manalo | Gloria R. Delos Reyes
A. Atty. Benito N. Pascual
B. Gloria R. Delos Reyes
C. Liza F. Manalo
D. Dr. Rosario D. Cruz-Manalo
MARKED ANSWER A. Atty. Benito N. Pascual
WHY "Atty. Benito N. Pascual" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Dr. Rosario D. Cruz-Manalo → CRUZMANALO, Rosario; Gloria R. Delos Reyes → DELOSREYES, Gloria; Liza F. Manalo → MANALO, Liza; Atty. Benito N. Pascual → PASCUAL, Benito.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 695 | CIVIO-CLR-FILE-POSITION-000696
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed FIRST?  Engr. Felipe A. Dela Cruz | Atty. Elena L. Dizon | Gloria B. Salazar | Alfredo D. Mendoza
A. Atty. Elena L. Dizon
B. Alfredo D. Mendoza
C. Engr. Felipe A. Dela Cruz
D. Gloria B. Salazar
MARKED ANSWER C. Engr. Felipe A. Dela Cruz
WHY "Engr. Felipe A. Dela Cruz" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Engr. Felipe A. Dela Cruz → DELACRUZ, Felipe; Atty. Elena L. Dizon → DIZON, Elena; Alfredo D. Mendoza → MENDOZA, Alfredo; Gloria B. Salazar → SALAZAR, Gloria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 696 | CIVIO-CLR-FILE-POSITION-000697
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed FIRST?  Dr. Evelyn D. Lopez | Imelda R. Castillo | Engr. Andres P. Pedro | Engr. Felipe P. Reyes
A. Engr. Felipe P. Reyes
B. Engr. Andres P. Pedro
C. Imelda R. Castillo
D. Dr. Evelyn D. Lopez
MARKED ANSWER C. Imelda R. Castillo
WHY "Imelda R. Castillo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Imelda R. Castillo → CASTILLO, Imelda; Dr. Evelyn D. Lopez → LOPEZ, Evelyn; Engr. Andres P. Pedro → PEDRO, Andres; Engr. Felipe P. Reyes → REYES, Felipe.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 697 | CIVIO-CLR-FILE-POSITION-000698
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
In alphabetical filing, which name is filed LAST?  Andres A. San Juan | Atty. Rafael D. Ocampo | Carlos S. De Leon | Teresita D. Dela Cruz
A. Andres A. San Juan
B. Atty. Rafael D. Ocampo
C. Teresita D. Dela Cruz
D. Carlos S. De Leon
MARKED ANSWER A. Andres A. San Juan
WHY "Andres A. San Juan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Teresita D. Dela Cruz → DELACRUZ, Teresita; Carlos S. De Leon → DELEON, Carlos; Atty. Rafael D. Ocampo → OCAMPO, Rafael; Andres A. San Juan → SANJUAN, Andres.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 698 | CIVIO-CLR-SPELL-RIGHT-000699
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  unanimus | unnanimous | unanmous | unanimous
A. unanimus
B. unnanimous
C. unanmous
D. unanimous
MARKED ANSWER D. unanimous
WHY "unanimous" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 699 | CIVIO-CLR-SPELL-WRONG-000700
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is misspelled?  manageable | forreign | liaison | receipt
A. manageable
B. forreign
C. liaison
D. receipt
MARKED ANSWER B. forreign
WHY "forreign" is misspelled: it doubles or undoubles a consonant. The correct spelling is "foreign".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 700 | CIVIO-CLR-SPELL-RIGHT-000701
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which word is spelled correctly?  independance | indepndence | indeppendence | independence
A. independance
B. indepndence
C. indeppendence
D. independence
MARKED ANSWER D. independence
WHY "independence" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 701 | CIVIO-GI-DEADLINE-NUMBER-000702
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
What is the maximum term of agreements for the exploration of natural resources under Art. XII, Sec. 2, before renewal?
A. 10 years
B. 25 years
C. 99 years
D. 50 years
MARKED ANSWER B. 25 years
WHY "25 years" is right. Art. XII, Sec. 2 says: "for a period not exceeding twenty-five years, renewable for not more than twenty-five years".
SHORTCUT Tie the fact to its section: Art. XII, Sec. 2. 25 years, renewable for 25 more.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 702 | CIVIO-GI-DEADLINE-NUMBER-000703
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Party-list representatives make up what share of the total House membership?
A. 20 percent
B. 10 percent
C. 50 percent
D. 25 percent
MARKED ANSWER A. 20 percent
WHY "20 percent" is right. Art. VI, Sec. 5(2) says: "twenty per centum of the total number of representatives".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 5(2). Party-list members are 20% of the House.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 703 | CIVIO-GI-DEADLINE-NUMBER-000704
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Under R.A. 6713, a violation of Sections 7, 8 or 9 is punishable by imprisonment of up to how many years?
A. 1 year
B. 5 years
C. 10 years
D. 3 years
MARKED ANSWER B. 5 years
WHY "5 years" is right. R.A. 6713, Sec. 11 says: "imprisonment not exceeding five (5) years".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 11. Up to 5 years, or a fine up to ₱5,000, or both.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 704 | CIVIO-GI-DEADLINE-NUMBER-000705
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Under R.A. 6713, a filed SALN may be made available for copying after how many working days from filing?
A. 10 working days
B. 5 working days
C. 30 working days
D. 15 working days
MARKED ANSWER A. 10 working days
WHY "10 working days" is right. R.A. 6713, Sec. 8(C)(2) says: "after ten (10) working days from the time they are filed".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 8(C)(2). Copies after 10 working days.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 705 | CIVIO-GI-WHO-HOLDS-POWER-000706
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which office investigates on its own, or on complaint, any act of a public official that appears illegal, unjust, improper or inefficient?
A. Commission on Audit
B. Department of the Interior and Local Government
C. Civil Service Commission
D. Office of the Ombudsman
MARKED ANSWER D. Office of the Ombudsman
WHY "Office of the Ombudsman" is right. Art. XI, Sec. 13 says: "appears to be illegal, unjust, improper, or inefficient".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 13. This is a power of the Ombudsman.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 706 | CIVIO-GI-TERM-MATCH-000707
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which anti-graft court continues to function under the 1987 Constitution?
A. Sandiganbayan
B. Court of Appeals
C. Court of Tax Appeals
D. Tanodbayan
MARKED ANSWER A. Sandiganbayan
WHY "Sandiganbayan" is right. Art. XI, Sec. 4 says: "The present anti-graft court known as the Sandiganbayan shall continue to function".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 4. The Sandiganbayan is the anti-graft court.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 707 | CIVIO-GI-DEADLINE-NUMBER-000708
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Under R.A. 6713, within how many working days must public officials and employees act on letters and requests from the public?
A. 30 working days
B. 10 working days
C. 15 working days
D. 5 working days
MARKED ANSWER C. 15 working days
WHY "15 working days" is right. R.A. 6713, Sec. 5(a) says: "within fifteen (15) working days from receipt thereof".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 5(a). Reply within 15 working days.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 708 | CIVIO-GI-DEADLINE-NUMBER-000709
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
How many consecutive terms may a Senator serve?
A. No limit
B. Three
C. Two
D. One
MARKED ANSWER C. Two
WHY "Two" is right. Art. VI, Sec. 4 says: "No Senator shall serve for more than two consecutive terms".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 4. A Senator may not serve more than two terms in a row.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 709 | CIVIO-GI-TERM-MATCH-000710
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which of these does the Bill of Rights prohibit?
A. Ex post facto laws and bills of attainder
B. Special laws
C. Executive orders
D. Local ordinances
MARKED ANSWER A. Ex post facto laws and bills of attainder
WHY "Ex post facto laws and bills of attainder" is right. Art. III, Sec. 22 says: "No ex post facto law or bill of attainder shall be enacted".
SHORTCUT Tie the fact to its section: Art. III, Sec. 22. No ex post facto laws, no bills of attainder.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 710 | CIVIO-GI-TERM-MATCH-000711
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-008.json
STEM
Which principle does Art. II, Sec. 6 of the 1987 Constitution declare inviolable?
A. Separation of powers
B. Freedom of the press
C. Local autonomy
D. Separation of Church and State
MARKED ANSWER D. Separation of Church and State
WHY "Separation of Church and State" is right. Art. II, Sec. 6 says: "The separation of Church and State shall be inviolable".
SHORTCUT Tie the fact to its section: Art. II, Sec. 6. Church and State are separate.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 711 | CIVIO-NUM-WP-RATIO-000712
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Cora and Nestor will share ₱12,500 of cleanup fund in the ratio 2 : 3. How much is Nestor's share?
A. ₱2,500
B. ₱4,166.67
C. ₱7,500
D. ₱5,000
MARKED ANSWER C. ₱7,500
WHY ₱7,500 is right: 3 × ₱2,500 = ₱7,500. Check: ₱5,000 + ₱7,500 = ₱12,500.
SHORTCUT Add the ratio numbers to get equal parts: 2 + 3 = 5. One part = ₱12,500 ÷ 5 = ₱2,500. Then multiply by the parts you need.

### 712 | CIVIO-NUM-FRAC-DEC-000713
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A barangay had 1200 notebooks. It gave out 1/4 of them on Monday and 1/6 of the remaining notebooks on Tuesday. How many are left?
A. 150
B. 750
C. 900
D. 700
MARKED ANSWER B. 750
WHY 750 is right. Check: 300 + 150 + 750 = 1200.
SHORTCUT Go day by day. Monday: 1/4 of 1200 = 300, so 900 left. Tuesday: 1/6 of 900 = 150, so 900 − 150 = 750 left.

### 713 | CIVIO-NUM-WP-RATIO-000714
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Aileen and Datu will share ₱5,000 of harvest income in the ratio 3 : 7. How much is Datu's share?
A. ₱714.29
B. ₱3,500
C. ₱1,500
D. ₱500
MARKED ANSWER B. ₱3,500
WHY ₱3,500 is right: 7 × ₱500 = ₱3,500. Check: ₱1,500 + ₱3,500 = ₱5,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱5,000 ÷ 10 = ₱500. Then multiply by the parts you need.

### 714 | CIVIO-NUM-SEQ-DIFF-000715
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What number comes next in the series?  15, 16, 20, 27, 37, ___
A. 47
B. 53
C. 50
D. 38
MARKED ANSWER C. 50
WHY 50 is right: 37 + 13 = 50.
SHORTCUT Write the jumps under the list: +1, +4, +7, +10. Each jump is 3 more than the one before. So the next jump is +13.

### 715 | CIVIO-NUM-WP-PCT-CHANGE-000716
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A cooperative member borrows ₱50,000 at 12% simple interest per year. How much interest is due after 2 years?
A. ₱6,000
B. ₱12,000
C. ₱62,000
D. ₱120,000
MARKED ANSWER B. ₱12,000
WHY ₱12,000 is right. Check: 50,000 × 0.12 × 2 = 12,000.
SHORTCUT Find one year first: 12% of ₱50,000 = ₱6,000. Time is 2 years. Multiply: 2 × ₱6,000 = ₱12,000.

### 716 | CIVIO-NUM-SEQ-MULT-000717
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What number comes next?  4, 6, 10, 18, 34, ___
A. 50
B. 64
C. 68
D. 66
MARKED ANSWER D. 66
WHY 66 is right: 34 × 2 = 68, then − 2 gives 66.
SHORTCUT Test "times 2, then − 2" on the first numbers: 4 × 2 − 2 = 6; 6 × 2 − 2 = 10. It works, so use it on 34.

### 717 | CIVIO-NUM-WP-RATE-000718
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Bea can paint a classroom in 21 hours. Liza can do the same job in 28 hours. Working together, how long will they take?
A. 24.5 hours
B. 5 minutes
C. 49 hours
D. 12 hours
MARKED ANSWER D. 12 hours
WHY 12 hours is right. Check: in 12 hours, Bea does 12/21 and Liza does 12/28; together that is 1 whole job.
SHORTCUT Per hour, Bea does 1/21 and Liza does 1/28. Together: 1/21 + 1/28 = 1/12. So the whole job takes 12 hours.

### 718 | CIVIO-NUM-OPS-ORDER-000719
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What is the value of 17 + 9 × 3 − 12?
A. -64
B. 17
C. 66
D. 32
MARKED ANSWER D. 32
WHY 32 is right: 17 + 27 = 44, and 44 − 12 = 32.
SHORTCUT Circle the × first: 9 × 3 = 27. Then go left to right: 17 + 27 − 12.

### 719 | CIVIO-NUM-OPS-ORDER-000720
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What is the value of 14 + 2 × 9 − 1?
A. 24
B. 30
C. 31
D. 143
MARKED ANSWER C. 31
WHY 31 is right: 14 + 18 = 32, and 32 − 1 = 31.
SHORTCUT Circle the × first: 2 × 9 = 18. Then go left to right: 14 + 18 − 1.

### 720 | CIVIO-NUM-WP-RATE-000721
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Jomar can label the census boxes in 21 hours. Bong can do the same job in 28 hours. Working together, how long will they take?
A. 49 hours
B. 12 hours
C. 5 minutes
D. 24.5 hours
MARKED ANSWER B. 12 hours
WHY 12 hours is right. Check: in 12 hours, Jomar does 12/21 and Bong does 12/28; together that is 1 whole job.
SHORTCUT Per hour, Jomar does 1/21 and Bong does 1/28. Together: 1/21 + 1/28 = 1/12. So the whole job takes 12 hours.

### 721 | CIVIO-NUM-WP-RATE-000722
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Liza can paint a classroom in 18 hours. Rogelio can do the same job in 9 hours. Working together, how long will they take?
A. 13.5 hours
B. 10 minutes
C. 27 hours
D. 6 hours
MARKED ANSWER D. 6 hours
WHY 6 hours is right. Check: in 6 hours, Liza does 6/18 and Rogelio does 6/9; together that is 1 whole job.
SHORTCUT Per hour, Liza does 1/18 and Rogelio does 1/9. Together: 1/18 + 1/9 = 1/6. So the whole job takes 6 hours.

### 722 | CIVIO-NUM-WP-PCT-CHANGE-000723
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A market stall sold a bag of cement for ₱1,200. It raised the price by 40%. Later, it lowered the new price by 10%. What is the final price?
A. ₱2,116.80
B. ₱1,512
C. ₱1,560
D. ₱1,680
MARKED ANSWER B. ₱1,512
WHY ₱1,512 is right. Check: 1,200 × 1.4 = 1,680, and 1,680 × 0.9 = 1,512.
SHORTCUT Do one change at a time. ₱1,200 up 40% is ₱1,200 + ₱480 = ₱1,680. Then 10% of ₱1,680 is ₱168, so ₱1,680 − ₱168 = ₱1,512.

### 723 | CIVIO-NUM-WP-GEOM-000724
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A rectangular basketball court is 28 m long and 20 m wide. A chain-link fence costs ₱150 per meter. How much will it cost to put the chain-link fence around the whole basketball court?
A. ₱14,400
B. ₱96
C. ₱84,000
D. ₱7,200
MARKED ANSWER A. ₱14,400
WHY ₱14,400 is right: 96 m × ₱150 = ₱14,400.
SHORTCUT Around = 2 × (28 + 20) = 96 m. Cost = 96 × ₱150.

### 724 | CIVIO-NUM-WP-PCT-CHANGE-000725
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A umbrella set is priced at ₱2,400. It is sold at 20% off. How much does a buyer pay?
A. ₱480
B. ₱2,880
C. ₱1,920
D. ₱2,380
MARKED ANSWER C. ₱1,920
WHY ₱1,920 is right. Check: discount ₱480; ₱2,400 − ₱480 = ₱1,920.
SHORTCUT Pay 80% of the price: ₱2,400 × 0.8 = ₱1,920.

### 725 | CIVIO-NUM-WP-PCT-CHANGE-000726
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A backpack is priced at ₱560. It is sold at 25% off. How much does a buyer pay?
A. ₱700
B. ₱420
C. ₱140
D. ₱535
MARKED ANSWER B. ₱420
WHY ₱420 is right. Check: discount ₱140; ₱560 − ₱140 = ₱420.
SHORTCUT Pay 75% of the price: ₱560 × 0.75 = ₱420.

### 726 | CIVIO-NUM-WP-PCT-CHANGE-000727
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A umbrella set is priced at ₱1,800. It is sold at 15% off. How much does a buyer pay?
A. ₱2,070
B. ₱270
C. ₱1,785
D. ₱1,530
MARKED ANSWER D. ₱1,530
WHY ₱1,530 is right. Check: discount ₱270; ₱1,800 − ₱270 = ₱1,530.
SHORTCUT Pay 85% of the price: ₱1,800 × 0.85 = ₱1,530.

### 727 | CIVIO-NUM-WP-PCT-CHANGE-000728
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A vendor borrows ₱40,000 at 4% simple interest per year. How much interest is due after 2 years and 6 months?
A. ₱4,160
B. ₱4,000
C. ₱3,200
D. ₱44,000
MARKED ANSWER B. ₱4,000
WHY ₱4,000 is right. Check: 40,000 × 0.04 × 2.5 = 4,000.
SHORTCUT Find one year first: 4% of ₱40,000 = ₱1,600. Time is 2.5 years. Multiply: 2.5 × ₱1,600 = ₱4,000.

### 728 | CIVIO-NUM-OPS-ORDER-000729
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What is the value of 15 + 7 × 3 − 3?
A. 15
B. 33
C. 63
D. 22
MARKED ANSWER B. 33
WHY 33 is right: 15 + 21 = 36, and 36 − 3 = 33.
SHORTCUT Circle the × first: 7 × 3 = 21. Then go left to right: 15 + 21 − 3.

### 729 | CIVIO-NUM-WP-AVERAGE-000730
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
The average years of service of the 4 staff members in the agriculture office is 15 years. One more person, with 25 years, joins them. What is the new average years of service?
A. 17 years
B. 85 years
C. 17.5 years
D. 20 years
MARKED ANSWER A. 17 years
WHY 17 years is right. Long way: 4 × 15 = 60; + 25 = 85; ÷ 5 = 17.
SHORTCUT The new person is 25 − 15 = 10 above the old average. Share that among all 5 people: 10 ÷ 5 = 2. Add it: 15 + 2 = 17.

### 730 | CIVIO-NUM-SEQ-DIFF-000731
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What number comes next in the series?  10, 15, 21, 28, 36, ___
A. 41
B. 45
C. 46
D. 44
MARKED ANSWER B. 45
WHY 45 is right: 36 + 9 = 45.
SHORTCUT Write the jumps under the list: +5, +6, +7, +8. Each jump is 1 more than the one before. So the next jump is +9.

### 731 | CIVIO-NUM-WP-AVERAGE-000732
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
The average age of the 8 staff members in the social welfare office is 29 years. One more person, with 38 years, joins them. What is the new average age?
A. 30.12 years
B. 30 years
C. 33.5 years
D. 270 years
MARKED ANSWER B. 30 years
WHY 30 years is right. Long way: 8 × 29 = 232; + 38 = 270; ÷ 9 = 30.
SHORTCUT The new person is 38 − 29 = 9 above the old average. Share that among all 9 people: 9 ÷ 9 = 1. Add it: 29 + 1 = 30.

### 732 | CIVIO-NUM-WP-PCT-CHANGE-000733
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A cooperative member borrows ₱24,000 at 6% simple interest per year. How much interest is due after 3 years and 6 months?
A. ₱5,184
B. ₱5,040
C. ₱4,320
D. ₱29,040
MARKED ANSWER B. ₱5,040
WHY ₱5,040 is right. Check: 24,000 × 0.06 × 3.5 = 5,040.
SHORTCUT Find one year first: 6% of ₱24,000 = ₱1,440. Time is 3.5 years. Multiply: 3.5 × ₱1,440 = ₱5,040.

### 733 | CIVIO-NUM-WP-GEOM-000734
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A rectangular school lot is 22 m long and 20 m wide. A lace border costs ₱150 per meter. How much will it cost to put the lace border around the whole school lot?
A. ₱84
B. ₱12,600
C. ₱66,000
D. ₱6,300
MARKED ANSWER B. ₱12,600
WHY ₱12,600 is right: 84 m × ₱150 = ₱12,600.
SHORTCUT Around = 2 × (22 + 20) = 84 m. Cost = 84 × ₱150.

### 734 | CIVIO-NUM-WP-AVERAGE-000735
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
The average age of the 6 barangay health workers in the public market office is 41 years. One more person, with 48 years, joins them. What is the new average age?
A. 42 years
B. 44.5 years
C. 294 years
D. 42.17 years
MARKED ANSWER A. 42 years
WHY 42 years is right. Long way: 6 × 41 = 246; + 48 = 294; ÷ 7 = 42.
SHORTCUT The new person is 48 − 41 = 7 above the old average. Share that among all 7 people: 7 ÷ 7 = 1. Add it: 41 + 1 = 42.

### 735 | CIVIO-NUM-WP-GEOM-000736
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A rectangular vegetable garden is 28 m long and 15 m wide. A edging costs ₱40 per meter. How much will it cost to put the edging around the whole vegetable garden?
A. ₱86
B. ₱3,440
C. ₱1,720
D. ₱16,800
MARKED ANSWER B. ₱3,440
WHY ₱3,440 is right: 86 m × ₱40 = ₱3,440.
SHORTCUT Around = 2 × (28 + 15) = 86 m. Cost = 86 × ₱40.

### 736 | CIVIO-NUM-SEQ-DIFF-000737
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Find the next number in the series.  15, 18, 24, 33, 45, ___
A. 63
B. 48
C. 57
D. 60
MARKED ANSWER D. 60
WHY 60 is right: 45 + 15 = 60.
SHORTCUT Write the jumps under the list: +3, +6, +9, +12. Each jump is 3 more than the one before. So the next jump is +15.

### 737 | CIVIO-NUM-WP-PCT-CHANGE-000738
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A sari-sari store sold a gallon of paint for ₱400. It raised the price by 25%. Later, it lowered the new price by 10%. What is the final price?
A. ₱562.50
B. ₱450
C. ₱500
D. ₱460
MARKED ANSWER B. ₱450
WHY ₱450 is right. Check: 400 × 1.25 = 500, and 500 × 0.9 = 450.
SHORTCUT Do one change at a time. ₱400 up 25% is ₱400 + ₱100 = ₱500. Then 10% of ₱500 is ₱50, so ₱500 − ₱50 = ₱450.

### 738 | CIVIO-NUM-WP-PCT-CHANGE-000739
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A cooperative store sold a sack of rice for ₱1,200. It raised the price by 50%. Later, it lowered the new price by 10%. What is the final price?
A. ₱2,430
B. ₱1,680
C. ₱1,800
D. ₱1,620
MARKED ANSWER D. ₱1,620
WHY ₱1,620 is right. Check: 1,200 × 1.5 = 1,800, and 1,800 × 0.9 = 1,620.
SHORTCUT Do one change at a time. ₱1,200 up 50% is ₱1,200 + ₱600 = ₱1,800. Then 10% of ₱1,800 is ₱180, so ₱1,800 − ₱180 = ₱1,620.

### 739 | CIVIO-NUM-WP-RATIO-000740
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Tess and Ramon will share ₱3,500 of allowance fund in the ratio 3 : 4. How much is Ramon's share?
A. ₱2,000
B. ₱1,500
C. ₱875
D. ₱500
MARKED ANSWER A. ₱2,000
WHY ₱2,000 is right: 4 × ₱500 = ₱2,000. Check: ₱1,500 + ₱2,000 = ₱3,500.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 4 = 7. One part = ₱3,500 ÷ 7 = ₱500. Then multiply by the parts you need.

### 740 | CIVIO-NUM-FRAC-DEC-000741
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A barangay had 480 notebooks. It gave out 1/8 of them on Monday and 1/6 of the remaining notebooks on Tuesday. How many are left?
A. 350
B. 340
C. 70
D. 420
MARKED ANSWER A. 350
WHY 350 is right. Check: 60 + 70 + 350 = 480.
SHORTCUT Go day by day. Monday: 1/8 of 480 = 60, so 420 left. Tuesday: 1/6 of 420 = 70, so 420 − 70 = 350 left.

### 741 | CIVIO-ANA-DI-TABLE-000742
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Supply use of toner (units) by office (Planning: Apr 72, May 40, Jun 10; Records: Apr 30, May 76, Jun 44; Cashier: Apr 60, May 64, Jun 22). How many did Cashier use in all three months?
A. 146
B. 124
C. 180
D. 48.7
MARKED ANSWER A. 146
WHY 146 is right: 60 + 64 + 22 = 146.
SHORTCUT Read across the Cashier row only: 60 + 64 + 22.

### 742 | CIVIO-ANA-DI-TABLE-000743
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Supply use of toner (units) by office (Planning: Apr 14, May 34, Jun 18; Health: Apr 56, May 18, Jun 72; Records: Apr 34, May 78, Jun 42). How many did Records use in all three months?
A. 154
B. 51.3
C. 130
D. 112
MARKED ANSWER A. 154
WHY 154 is right: 34 + 78 + 42 = 154.
SHORTCUT Read across the Records row only: 34 + 78 + 42.

### 743 | CIVIO-ANA-SYLLOGISM-000744
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Statement 1: No boats are unregistered items. Statement 2: All ferries are boats. Which conclusion follows from both statements?
A. No ferries are unregistered items.
B. All boats are ferries.
C. Some ferries are unregistered items.
D. No inspected vessels are unregistered items.
MARKED ANSWER A. No ferries are unregistered items.
WHY "No ferries are unregistered items." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the ferries circle inside boats. The "unregistered items" circle sits outside boats, so it is outside ferries too.

### 744 | CIVIO-ANA-SYMBOL-SERIES-000745
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In a certain code, RIVER is written as QHUDQ. How is BOARD written in the same code?
A. ZMYPB
B. ANZQC
C. ANZQD
D. CPBSE
MARKED ANSWER B. ANZQC
WHY ANZQC is right: each letter of BOARD moved 1 place back.
SHORTCUT Compare the first letters: R became Q. That is 1 place back. Check one more letter, then shift every letter of BOARD the same way.

### 745 | CIVIO-ANA-SYMBOL-SERIES-000746
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In a certain code, BUDGET is written as DWFIGV. How is LIBRARY written in the same code?
A. JGZPYPW
B. NKDTCTA
C. NKDTCTY
D. OLEUDUB
MARKED ANSWER B. NKDTCTA
WHY NKDTCTA is right: each letter of LIBRARY moved 2 places forward.
SHORTCUT Compare the first letters: B became D. That is 2 places forward. Check one more letter, then shift every letter of LIBRARY the same way.

### 746 | CIVIO-ANA-SYMBOL-SERIES-000747
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What comes next in the series?  EL, IN, MP, QR, ___
A. UB
B. TU
C. RT
D. UT
MARKED ANSWER D. UT
WHY UT is right: Q + 4 = U and R + 2 = T.
SHORTCUT Split each pair. First letters: E, I, M, Q (jump +4). Second letters: L, N, P, R (jump +2). Move each one more step.

### 747 | CIVIO-ANA-SYMBOL-SERIES-000748
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In a certain code, PERMIT is written as QFSNJU. How is FILES written in the same code?
A. EHKDR
B. GJMFT
C. HKNGU
D. GJMFS
MARKED ANSWER B. GJMFT
WHY GJMFT is right: each letter of FILES moved 1 place forward.
SHORTCUT Compare the first letters: P became Q. That is 1 place forward. Check one more letter, then shift every letter of FILES the same way.

### 748 | CIVIO-ANA-CONCLUSION-000749
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Four staff members are compared. Rogelio has served longer than Aileen. Inday has served longer than Rogelio. Bea has served longer than Inday. Who is second in the order (counting from the one who has served the longest)?
A. Bea
B. Aileen
C. Rogelio
D. Inday
MARKED ANSWER D. Inday
WHY Inday is right. The clues give Bea → Inday → Rogelio → Aileen, so Inday is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Bea → Inday → Rogelio → Aileen.

### 749 | CIVIO-ANA-CONCLUSION-000750
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Four staff members are compared. Aileen encoded more forms than Inday. Cora encoded more forms than Teresa. Inday encoded more forms than Cora. Who is second in the order (counting from the one who encoded the most forms)?
A. Cora
B. Teresa
C. Aileen
D. Inday
MARKED ANSWER D. Inday
WHY Inday is right. The clues give Aileen → Inday → Cora → Teresa, so Inday is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Aileen → Inday → Cora → Teresa.

### 750 | CIVIO-ANA-SYMBOL-SERIES-000751
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What comes next in the series?  FR, HS, JT, LU, ___
A. VN
B. NZ
C. NV
D. MV
MARKED ANSWER C. NV
WHY NV is right: L + 2 = N and U + 1 = V.
SHORTCUT Split each pair. First letters: F, H, J, L (jump +2). Second letters: R, S, T, U (jump +1). Move each one more step.

### 751 | CIVIO-ANA-SYMBOL-SERIES-000752
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In a certain code, CLERK is written as AJCPI. How is STAMP written in the same code?
A. UVCOR
B. QRYKN
C. PQXJM
D. QRYKP
MARKED ANSWER B. QRYKN
WHY QRYKN is right: each letter of STAMP moved 2 places back.
SHORTCUT Compare the first letters: C became A. That is 2 places back. Check one more letter, then shift every letter of STAMP the same way.

### 752 | CIVIO-ANA-CONCLUSION-000753
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Four staff members are compared. Ramon has served longer than Marites. Teresa has served longer than Bea. Bea has served longer than Ramon. Who is second in the order (counting from the one who has served the longest)?
A. Marites
B. Teresa
C. Ramon
D. Bea
MARKED ANSWER D. Bea
WHY Bea is right. The clues give Teresa → Bea → Ramon → Marites, so Bea is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Teresa → Bea → Ramon → Marites.

### 753 | CIVIO-ANA-SYMBOL-SERIES-000754
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In a certain code, BRIDGE is written as CSJEHF. How is PAPER written in the same code?
A. RCRGT
B. OZODQ
C. QBQFS
D. QBQFR
MARKED ANSWER C. QBQFS
WHY QBQFS is right: each letter of PAPER moved 1 place forward.
SHORTCUT Compare the first letters: B became C. That is 1 place forward. Check one more letter, then shift every letter of PAPER the same way.

### 754 | CIVIO-ANA-SYLLOGISM-000755
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
All encoders are clerks. All clerks are employees. Which conclusion must be true?
A. All employees are encoders.
B. No clerks are encoders.
C. Some employees are not clerks.
D. All encoders are employees.
MARKED ANSWER D. All encoders are employees.
WHY "All encoders are employees." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: encoders inside clerks, clerks inside employees. So encoders sit inside employees.

### 755 | CIVIO-ANA-SYLLOGISM-000756
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Assume these are true: none of the plants are expired stock, and every one of the seedlings is among the plants. What can be concluded for certain?
A. All plants are seedlings.
B. No seedlings are expired stock.
C. No nursery stock are expired stock.
D. Some seedlings are expired stock.
MARKED ANSWER B. No seedlings are expired stock.
WHY "No seedlings are expired stock." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the seedlings circle inside plants. The "expired stock" circle sits outside plants, so it is outside seedlings too.

### 756 | CIVIO-ANA-DI-TABLE-000757
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Supply use of ballpens (boxes) by office (Health: Jul 12, Aug 22, Sep 10; Assessor: Jul 58, Aug 76, Sep 58; Cashier: Jul 72, Aug 18, Sep 54). In Sep, how many more did Cashier use than Health?
A. 64
B. 100
C. 44
D. 60
MARKED ANSWER C. 44
WHY 44 is right: 54 − 10 = 44.
SHORTCUT Go to the Sep column: Health 10, Cashier 54. Subtract the smaller from the larger.

### 757 | CIVIO-ANA-ANALOGY-FUNCTION-000758
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Find the pair whose link matches the link between "pilot" and "airplane".
A. train : driver
B. sky : cloud
C. passenger : bus
D. captain : ship
MARKED ANSWER D. captain : ship
WHY "captain : ship" is right. It has the same link, worker : what they operate, in the same order.
SHORTCUT Make a sentence for the stem: "pilot is to airplane" as worker : what they operate. Test each choice in that sentence.

### 758 | CIVIO-ANA-CONCLUSION-000759
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Four staff members are compared. Arnel lives nearer the office than Aileen. Tess lives nearer the office than Cora. Aileen lives nearer the office than Tess. Who is second in the order (counting from the one who lives nearest)?
A. Arnel
B. Cora
C. Tess
D. Aileen
MARKED ANSWER D. Aileen
WHY Aileen is right. The clues give Arnel → Aileen → Tess → Cora, so Aileen is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Arnel → Aileen → Tess → Cora.

### 759 | CIVIO-ANA-DI-TABLE-000760
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Supply use of folders (packs) by office (Cashier: Apr 72, May 14, Jun 64; Engineering: Apr 66, May 78, Jun 78; Health: Apr 58, May 66, Jun 40). How many did Cashier use in all three months?
A. 86
B. 158
C. 50
D. 150
MARKED ANSWER D. 150
WHY 150 is right: 72 + 14 + 64 = 150.
SHORTCUT Read across the Cashier row only: 72 + 14 + 64.

### 760 | CIVIO-ANA-DI-TABLE-000761
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Supply use of staplers by office (Planning: Apr 60, May 80, Jun 74; Assessor: Apr 64, May 18, Jun 32; Cashier: Apr 18, May 20, Jun 26). How many did Cashier use in all three months?
A. 118
B. 38
C. 64
D. 21.3
MARKED ANSWER C. 64
WHY 64 is right: 18 + 20 + 26 = 64.
SHORTCUT Read across the Cashier row only: 18 + 20 + 26.

### 761 | CIVIO-ANA-DI-TABLE-000762
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Supply use of ballpens (boxes) by office (Health: Jul 80, Aug 26, Sep 70; Cashier: Jul 40, Aug 28, Sep 76; Planning: Jul 34, Aug 18, Sep 70). How many did Planning use in all three months?
A. 122
B. 72
C. 40.7
D. 52
MARKED ANSWER A. 122
WHY 122 is right: 34 + 18 + 70 = 122.
SHORTCUT Read across the Planning row only: 34 + 18 + 70.

### 762 | CIVIO-ANA-SYLLOGISM-000763
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
All nurses are health workers. No health workers are late payers. Which conclusion must be true?
A. No nurses are late payers.
B. Some nurses are late payers.
C. All health workers are nurses.
D. No public servants are late payers.
MARKED ANSWER A. No nurses are late payers.
WHY "No nurses are late payers." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the nurses circle inside health workers. The "late payers" circle sits outside health workers, so it is outside nurses too.

### 763 | CIVIO-ANA-ANALOGY-FUNCTION-000764
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which pair shows the same relationship as "hungry : eat"?
A. food : plate
B. drink : thirsty
C. tired : rest
D. hunger : pain
MARKED ANSWER C. tired : rest
WHY "tired : rest" is right. It has the same link, need : action that meets it, in the same order.
SHORTCUT Make a sentence for the stem: "hungry is to eat" as need : action that meets it. Test each choice in that sentence.

### 764 | CIVIO-ANA-ASSUME-I-II-000765
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Statement: The office replaced its old printer with a faster one.
Assumption I: The new printer will never break down.
Assumption II: Faster printers are always cheaper.
Which assumption is implicit in the statement?
A. Only II
B. Neither I nor II
C. Both I and II
D. Only I
MARKED ANSWER B. Neither I nor II
WHY "Neither I nor II" is right. Neither assumption is needed; both go beyond the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 765 | CIVIO-ANA-ASSUME-I-II-000766
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Statement: The town will plant trees along the river to slow down soil erosion.
Assumption I: Tree roots can help hold soil in place.
Assumption II: Planting trees costs nothing.
Which assumption is implicit in the statement?
A. Only I
B. Neither I nor II
C. Only II
D. Both I and II
MARKED ANSWER A. Only I
WHY "Only I" is right. Only assumption I is needed. II ("Planting trees costs nothing.") is not required by the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 766 | CIVIO-VEN-WORD-MEANING-000767
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What does the phrase in capital letters mean?  Finishing the census early was A PIECE OF CAKE for the team.
A. very easy
B. a reward of food
C. the only task done
D. very hard
MARKED ANSWER A. very easy
WHY "very easy" is right: that is what the idiom means here.
SHORTCUT Skip the literal picture. Ask what the speaker wants to say in this situation.

### 767 | CIVIO-VEN-SENT-COMP-WORD-000768
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: The report must ____ the law that allows the fee.
A. recite
B. site
C. cite
D. sight
MARKED ANSWER C. cite
WHY "cite" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 768 | CIVIO-VEN-WORD-MEANING-000769
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  ABUNDANT
A. redundant
B. abandoned
C. plentiful
D. scarce
MARKED ANSWER D. scarce
WHY "scarce" is right. "Abundant" means plentiful; "scarce" is the reverse.
SHORTCUT First say what "abundant" means (plentiful). Then look for the word that means the reverse.

### 769 | CIVIO-VEN-SENT-COMP-WORD-000770
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: The ____ of the new hall is near the public market.
A. sight
B. cite
C. site
D. side
MARKED ANSWER C. site
WHY "site" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 770 | CIVIO-VEN-RC-VOCAB-000771
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The new policy will BENEFIT small farmers.
A. help
B. fund-raising event
C. harm
D. bend
MARKED ANSWER A. help
WHY "help" is right: it is the sense of "benefit" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "benefit".

### 771 | CIVIO-VEN-WORD-MEANING-000772
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  AUTHENTIC
A. fake
B. genuine
C. automatic
D. authority
MARKED ANSWER A. fake
WHY "fake" is right. "Authentic" means genuine; "fake" is the reverse.
SHORTCUT First say what "authentic" means (genuine). Then look for the word that means the reverse.

### 772 | CIVIO-VEN-WORD-MEANING-000773
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  DILIGENT
A. diluted
B. hard-working
C. delicate
D. lazy
MARKED ANSWER D. lazy
WHY "lazy" is right. "Diligent" means hard-working; "lazy" is the reverse.
SHORTCUT First say what "diligent" means (hard-working). Then look for the word that means the reverse.

### 773 | CIVIO-VEN-WORD-MEANING-000774
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is closest in meaning to the word in capital letters?  IMMINENT
A. about to happen
B. far off
C. eminent
D. immense
MARKED ANSWER A. about to happen
WHY "about to happen" is right. "Imminent" means about to happen.
SHORTCUT Make a short sentence with "imminent", then swap in each choice. Watch for words that only look or sound like "imminent".

### 774 | CIVIO-VEN-ERROR-AGREE-000775
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: The schedule of the trainings ____ every quarter.
A. change
B. changing
C. to change
D. changes
MARKED ANSWER D. changes
WHY "changes" is right: "The schedule" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The schedule ____". The subject is singular, so use the singular verb.

### 775 | CIVIO-VEN-SENT-COMP-WORD-000776
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: Honesty is the first ____ of public service.
A. principal
B. practice
C. principles
D. principle
MARKED ANSWER D. principle
WHY "principle" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 776 | CIVIO-VEN-WORD-MEANING-000777
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is closest in meaning to the word in capital letters?  MEAGER
A. plentiful
B. eager
C. meaningful
D. scanty
MARKED ANSWER D. scanty
WHY "scanty" is right. "Meager" means scanty.
SHORTCUT Make a short sentence with "meager", then swap in each choice. Watch for words that only look or sound like "meager".

### 777 | CIVIO-VEN-SENT-COMP-WORD-000778
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: The applicant is interested ____ the clerk position.
A. in
B. for
C. on
D. at
MARKED ANSWER A. in
WHY "in" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 778 | CIVIO-VEN-ERROR-AGREE-000779
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: The group of farmers ____ every Saturday at the plaza.
A. to meet
B. meets
C. meeting
D. meet
MARKED ANSWER B. meets
WHY "meets" is right: "The group" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The group ____". The subject is singular, so use the singular verb.

### 779 | CIVIO-VEN-WORD-MEANING-000780
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is closest in meaning to the word in capital letters?  TEMPORARY
A. permanent
B. contemporary
C. short-term
D. temperate
MARKED ANSWER C. short-term
WHY "short-term" is right. "Temporary" means short-term.
SHORTCUT Make a short sentence with "temporary", then swap in each choice. Watch for words that only look or sound like "temporary".

### 780 | CIVIO-VEN-ERROR-TENSE-000781
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the correct verb: By next week, Aileen ____ the relief goods.
A. delivered
B. will have delivered
C. has delivered
D. is delivering
MARKED ANSWER B. will have delivered
WHY "will have delivered" is right: the future perfect matches "By next week".
SHORTCUT Find the time signal first: "By next week". It calls for the future perfect.

### 781 | CIVIO-VEN-SENT-COMP-WORD-000782
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: Although the clerk was new, she was very ____ and finished early.
A. efficient
B. slow
C. efficiency
D. sufficient
MARKED ANSWER A. efficient
WHY "efficient" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 782 | CIVIO-VEN-ERROR-TENSE-000783
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the correct verb: By the end of the year, the civil registry staff ____ the attendance sheets.
A. checked
B. is checking
C. will have checked
D. has checked
MARKED ANSWER C. will have checked
WHY "will have checked" is right: the future perfect matches "By the end of the year".
SHORTCUT Find the time signal first: "By the end of the year". It calls for the future perfect.

### 783 | CIVIO-VEN-SENT-COMP-WORD-000784
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the word that best completes the sentence: The award went to the clerk ____ worked overtime all month.
A. whose
B. whom
C. who
D. which
MARKED ANSWER C. who
WHY "who" is right. It is the form the slot needs.
SHORTCUT Cover the other name and read the sentence with only the pronoun. "Gave to me" sounds right; "gave to I" does not.

### 784 | CIVIO-VEN-RC-VOCAB-000785
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The treasurer's report was SOUND and well supported.
A. weak
B. reliable
C. noisy
D. asleep
MARKED ANSWER B. reliable
WHY "reliable" is right: it is the sense of "sound" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "sound".

### 785 | CIVIO-VEN-ERROR-TENSE-000786
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Choose the correct verb: Two days ago, the district hospital staff ____ the drainage canal.
A. will inspect
B. will have inspected
C. has inspected
D. inspected
MARKED ANSWER D. inspected
WHY "inspected" is right: the simple past matches "Two days ago".
SHORTCUT Find the time signal first: "Two days ago". It calls for the simple past.

### 786 | CIVIO-CLR-SPELL-RIGHT-000787
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is spelled correctly?  occasionally | occasinally | occsionally | ocasionally
A. occasionally
B. occasinally
C. occsionally
D. ocasionally
MARKED ANSWER A. occasionally
WHY "occasionally" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 787 | CIVIO-CLR-FILE-POSITION-000788
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed LAST?  Engr. Liza B. Del Rosario | Nora A. Reyes-Tan | Carlos A. Dela Cruz | Atty. Cristina P. Cruz-Manalo
A. Engr. Liza B. Del Rosario
B. Atty. Cristina P. Cruz-Manalo
C. Carlos A. Dela Cruz
D. Nora A. Reyes-Tan
MARKED ANSWER D. Nora A. Reyes-Tan
WHY "Nora A. Reyes-Tan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Atty. Cristina P. Cruz-Manalo → CRUZMANALO, Cristina; Carlos A. Dela Cruz → DELACRUZ, Carlos; Engr. Liza B. Del Rosario → DELROSARIO, Liza; Nora A. Reyes-Tan → REYESTAN, Nora.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 788 | CIVIO-CLR-SPELL-RIGHT-000789
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is spelled correctly?  managable | mannageable | manageable | manageible
A. managable
B. mannageable
C. manageable
D. manageible
MARKED ANSWER C. manageable
WHY "manageable" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 789 | CIVIO-CLR-FILE-POSITION-000790
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed FIRST?  Dr. Carlos A. De los Santos | Engr. Liza V. Dela Cruz | Atty. Evelyn F. Lopez | Ana D. Del Rosario
A. Atty. Evelyn F. Lopez
B. Dr. Carlos A. De los Santos
C. Ana D. Del Rosario
D. Engr. Liza V. Dela Cruz
MARKED ANSWER D. Engr. Liza V. Dela Cruz
WHY "Engr. Liza V. Dela Cruz" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Engr. Liza V. Dela Cruz → DELACRUZ, Liza; Dr. Carlos A. De los Santos → DELOSSANTOS, Carlos; Ana D. Del Rosario → DELROSARIO, Ana; Atty. Evelyn F. Lopez → LOPEZ, Evelyn.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 790 | CIVIO-CLR-SPELL-WRONG-000791
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is misspelled?  miscellaneous | address | gurantee | seize
A. miscellaneous
B. address
C. gurantee
D. seize
MARKED ANSWER C. gurantee
WHY "gurantee" is misspelled: it drops a letter. The correct spelling is "guarantee".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 791 | CIVIO-CLR-FILE-POSITION-000792
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed LAST?  Atty. Andres M. De los Santos | Engr. Corazon L. Castillo | Lourdes V. Lopez | Rafael V. Aquino
A. Atty. Andres M. De los Santos
B. Lourdes V. Lopez
C. Rafael V. Aquino
D. Engr. Corazon L. Castillo
MARKED ANSWER B. Lourdes V. Lopez
WHY "Lourdes V. Lopez" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Rafael V. Aquino → AQUINO, Rafael; Engr. Corazon L. Castillo → CASTILLO, Corazon; Atty. Andres M. De los Santos → DELOSSANTOS, Andres; Lourdes V. Lopez → LOPEZ, Lourdes.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 792 | CIVIO-CLR-SPELL-RIGHT-000793
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is spelled correctly?  maintnance | maintenance | maintenence | maintennance
A. maintnance
B. maintenance
C. maintenence
D. maintennance
MARKED ANSWER B. maintenance
WHY "maintenance" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 793 | CIVIO-CLR-FILE-POSITION-000794
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed FIRST?  Nora P. Del Mundo | Atty. Rodrigo D. Lim | Engr. Rosario F. Austria | Gloria G. Pedro
A. Nora P. Del Mundo
B. Engr. Rosario F. Austria
C. Gloria G. Pedro
D. Atty. Rodrigo D. Lim
MARKED ANSWER B. Engr. Rosario F. Austria
WHY "Engr. Rosario F. Austria" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Engr. Rosario F. Austria → AUSTRIA, Rosario; Nora P. Del Mundo → DELMUNDO, Nora; Atty. Rodrigo D. Lim → LIM, Rodrigo; Gloria G. Pedro → PEDRO, Gloria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 794 | CIVIO-CLR-SPELL-WRONG-000795
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is misspelled?  cemetery | conscence | permissible | accommodate
A. cemetery
B. conscence
C. permissible
D. accommodate
MARKED ANSWER B. conscence
WHY "conscence" is misspelled: it drops a letter. The correct spelling is "conscience".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 795 | CIVIO-CLR-FILE-POSITION-000796
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed FIRST?  Nora M. Jose | Mario V. Aquino | Engr. Victoria L. Cruz | Evelyn F. Pedro
A. Mario V. Aquino
B. Engr. Victoria L. Cruz
C. Evelyn F. Pedro
D. Nora M. Jose
MARKED ANSWER A. Mario V. Aquino
WHY "Mario V. Aquino" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Mario V. Aquino → AQUINO, Mario; Engr. Victoria L. Cruz → CRUZ, Victoria; Nora M. Jose → JOSE, Nora; Evelyn F. Pedro → PEDRO, Evelyn.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 796 | CIVIO-CLR-FILE-POSITION-000797
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed LAST?  Dr. Danilo T. Delos Reyes | Nora G. De los Santos | Atty. Liza L. De Leon | Eduardo E. San Juan
A. Dr. Danilo T. Delos Reyes
B. Eduardo E. San Juan
C. Atty. Liza L. De Leon
D. Nora G. De los Santos
MARKED ANSWER B. Eduardo E. San Juan
WHY "Eduardo E. San Juan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Atty. Liza L. De Leon → DELEON, Liza; Dr. Danilo T. Delos Reyes → DELOSREYES, Danilo; Nora G. De los Santos → DELOSSANTOS, Nora; Eduardo E. San Juan → SANJUAN, Eduardo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 797 | CIVIO-CLR-FILE-POSITION-000798
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed FIRST?  Rosario C. Del Mundo | Engr. Cristina F. Del Rosario | Felipe D. Dela Torre | Mario N. Mendoza
A. Mario N. Mendoza
B. Rosario C. Del Mundo
C. Felipe D. Dela Torre
D. Engr. Cristina F. Del Rosario
MARKED ANSWER C. Felipe D. Dela Torre
WHY "Felipe D. Dela Torre" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Felipe D. Dela Torre → DELATORRE, Felipe; Rosario C. Del Mundo → DELMUNDO, Rosario; Engr. Cristina F. Del Rosario → DELROSARIO, Cristina; Mario N. Mendoza → MENDOZA, Mario.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 798 | CIVIO-CLR-FILE-POSITION-000799
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
In alphabetical filing, which name is filed LAST?  Dr. Ernesto S. Reyes-Tan | Dr. Victoria S. Juan | Dr. Benito S. Pascual | Cristina V. De los Santos
A. Dr. Victoria S. Juan
B. Dr. Ernesto S. Reyes-Tan
C. Dr. Benito S. Pascual
D. Cristina V. De los Santos
MARKED ANSWER B. Dr. Ernesto S. Reyes-Tan
WHY "Dr. Ernesto S. Reyes-Tan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Cristina V. De los Santos → DELOSSANTOS, Cristina; Dr. Victoria S. Juan → JUAN, Victoria; Dr. Benito S. Pascual → PASCUAL, Benito; Dr. Ernesto S. Reyes-Tan → REYESTAN, Ernesto.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 799 | CIVIO-CLR-SPELL-WRONG-000800
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is misspelled?  parliament | allotment | inoculte | disbursement
A. parliament
B. allotment
C. inoculte
D. disbursement
MARKED ANSWER C. inoculte
WHY "inoculte" is misspelled: it drops a letter. The correct spelling is "inoculate".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 800 | CIVIO-CLR-SPELL-RIGHT-000801
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Which word is spelled correctly?  reimbursement | reimbursemant | riembursement | reimbursemment
A. reimbursement
B. reimbursemant
C. riembursement
D. reimbursemment
MARKED ANSWER A. reimbursement
WHY "reimbursement" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 801 | CIVIO-GI-DEADLINE-NUMBER-000802
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
A people's initiative to amend the Constitution needs a petition from at least what percent of all registered voters?
A. 10 percent
B. 3 percent
C. 12 percent
D. 20 percent
MARKED ANSWER C. 12 percent
WHY "12 percent" is right. Art. XVII, Sec. 2 says: "at least twelve per centum of the total number of registered voters".
SHORTCUT Tie the fact to its section: Art. XVII, Sec. 2. 12% nationwide, with at least 3% in every district.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 802 | CIVIO-GI-TERM-MATCH-000803
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What does the civil service cover under the 1987 Constitution?
A. Only national government agencies
B. Only the executive branch
C. All branches, subdivisions, instrumentalities and agencies of the Government, including GOCCs with original charters
D. All corporations doing business in the Philippines
MARKED ANSWER C. All branches, subdivisions, instrumentalities and agencies of the Government, including GOCCs with original charters
WHY "All branches, subdivisions, instrumentalities and agencies of the Government, including GOCCs with original charters" is right. Art. IX-B, Sec. 2(1) says: "embraces all branches, subdivisions, instrumentalities, and agencies of the Government, including government-owned or controlled corporations with original charters".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 2(1). The civil service is government-wide, including chartered GOCCs.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 803 | CIVIO-GI-WHO-HOLDS-POWER-000804
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
According to the 1987 Constitution, sovereignty resides in whom?
A. The Congress
B. The people
C. The President
D. The Armed Forces
MARKED ANSWER B. The people
WHY "The people" is right. Art. II, Sec. 1 says: "Sovereignty resides in the people and all government authority emanates from them".
SHORTCUT Tie the fact to its section: Art. II, Sec. 1. All authority comes from the people.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 804 | CIVIO-GI-DEADLINE-NUMBER-000805
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What vote of both Houses in joint session, voting separately, is needed to declare the existence of a state of war?
A. Three-fourths
B. Majority
C. Unanimous
D. Two-thirds
MARKED ANSWER D. Two-thirds
WHY "Two-thirds" is right. Art. VI, Sec. 23(1) says: "by a vote of two-thirds of both Houses in joint session assembled, voting separately".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 23(1). Declaring war needs two-thirds.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 805 | CIVIO-GI-DEADLINE-NUMBER-000806
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Under R.A. 6713, Sec. 7, for how long after resignation, retirement or separation do the prohibitions on financial and material interests and outside employment continue to apply (subject to one stated exception)?
A. Six months
B. Two years
C. Five years
D. One year
MARKED ANSWER D. One year
WHY "One year" is right. R.A. 6713, Sec. 7(b) says: "continue to apply for a period of one (1) year after resignation, retirement, or separation from public office".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 7(b). The one-year bar.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 806 | CIVIO-GI-TERM-MATCH-000807
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Under R.A. 6713, providing service to everyone without unfair discrimination regardless of party affiliation is which norm of conduct?
A. Commitment to democracy
B. Justness and sincerity
C. Political neutrality
D. Professionalism
MARKED ANSWER C. Political neutrality
WHY "Political neutrality" is right. R.A. 6713, Sec. 4(A) says: "Political neutrality".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). This is political neutrality, Sec. 4(A)(d).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 807 | CIVIO-GI-DEADLINE-NUMBER-000808
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
How long is the term of the President under the 1987 Constitution?
A. 6 years, with no re-election
B. 6 years, with one re-election
C. 3 years, with re-election
D. 4 years, with one re-election
MARKED ANSWER A. 6 years, with no re-election
WHY "6 years, with no re-election" is right. Art. VII, Sec. 4 says: "The President shall not be eligible for any re-election".
SHORTCUT Tie the fact to its section: Art. VII, Sec. 4. One 6-year term; the President cannot be re-elected.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 808 | CIVIO-GI-TERM-MATCH-000809
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Under the Bill of Rights, no person shall be imprisoned for what?
A. Estafa
B. Theft
C. Debt or non-payment of a poll tax
D. Contempt of court
MARKED ANSWER C. Debt or non-payment of a poll tax
WHY "Debt or non-payment of a poll tax" is right. Art. III, Sec. 20 says: "No person shall be imprisoned for debt or non-payment of a poll tax".
SHORTCUT Tie the fact to its section: Art. III, Sec. 20. No prison for debt.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 809 | CIVIO-GI-TERM-MATCH-000810
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
Under R.A. 6713, always upholding the public interest over personal interest is which norm of conduct?
A. Commitment to public interest
B. Nationalism and patriotism
C. Political neutrality
D. Simple living
MARKED ANSWER A. Commitment to public interest
WHY "Commitment to public interest" is right. R.A. 6713, Sec. 4(A) says: "always uphold the public interest over and above personal interest".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). This is commitment to public interest, Sec. 4(A)(a).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 810 | CIVIO-GI-DEADLINE-NUMBER-000811
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-009.json
STEM
What vote of all House Members is needed to affirm or override a committee resolution on impeachment?
A. Majority
B. At least one-third
C. Three-fourths
D. Two-thirds
MARKED ANSWER B. At least one-third
WHY "At least one-third" is right. Art. XI, Sec. 3(3) says: "A vote of at least one-third of all the Members of the House shall be necessary".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 3(3). One-third of the House is enough.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 811 | CIVIO-NUM-WP-RATE-000812
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Analyn can label the census boxes in 15 hours. Bea can do the same job in 10 hours. Working together, how long will they take?
A. 10 minutes
B. 25 hours
C. 6 hours
D. 12.5 hours
MARKED ANSWER C. 6 hours
WHY 6 hours is right. Check: in 6 hours, Analyn does 6/15 and Bea does 6/10; together that is 1 whole job.
SHORTCUT Per hour, Analyn does 1/15 and Bea does 1/10. Together: 1/15 + 1/10 = 1/6. So the whole job takes 6 hours.

### 812 | CIVIO-NUM-WP-RATIO-000813
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A ₱9,600 harvest income is divided between Inday and Aileen in the ratio 3 : 5. What is Aileen's share?
A. ₱1,920
B. ₱3,600
C. ₱1,200
D. ₱6,000
MARKED ANSWER D. ₱6,000
WHY ₱6,000 is right: 5 × ₱1,200 = ₱6,000. Check: ₱3,600 + ₱6,000 = ₱9,600.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 5 = 8. One part = ₱9,600 ÷ 8 = ₱1,200. Then multiply by the parts you need.

### 813 | CIVIO-NUM-WP-RATE-000814
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Rogelio can sort a sack of mail in 15 hours. Tess can do the same job in 10 hours. Working together, how long will they take?
A. 6 hours
B. 12.5 hours
C. 10 minutes
D. 25 hours
MARKED ANSWER A. 6 hours
WHY 6 hours is right. Check: in 6 hours, Rogelio does 6/15 and Tess does 6/10; together that is 1 whole job.
SHORTCUT Per hour, Rogelio does 1/15 and Tess does 1/10. Together: 1/15 + 1/10 = 1/6. So the whole job takes 6 hours.

### 814 | CIVIO-NUM-WP-RATE-000815
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Paolo can clean the plaza in 35 hours. Liza can do the same job in 14 hours. Working together, how long will they take?
A. 24.5 hours
B. 10 hours
C. 6 minutes
D. 49 hours
MARKED ANSWER B. 10 hours
WHY 10 hours is right. Check: in 10 hours, Paolo does 10/35 and Liza does 10/14; together that is 1 whole job.
SHORTCUT Per hour, Paolo does 1/35 and Liza does 1/14. Together: 1/35 + 1/14 = 1/10. So the whole job takes 10 hours.

### 815 | CIVIO-NUM-WP-RATIO-000816
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Cora and Kimberly will share ₱3,500 of harvest income in the ratio 3 : 4. How much is Kimberly's share?
A. ₱1,500
B. ₱875
C. ₱500
D. ₱2,000
MARKED ANSWER D. ₱2,000
WHY ₱2,000 is right: 4 × ₱500 = ₱2,000. Check: ₱1,500 + ₱2,000 = ₱3,500.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 4 = 7. One part = ₱3,500 ÷ 7 = ₱500. Then multiply by the parts you need.

### 816 | CIVIO-NUM-SEQ-DIFF-000817
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Find the next number in the series.  11, 13, 17, 23, 31, ___
A. 43
B. 39
C. 41
D. 33
MARKED ANSWER C. 41
WHY 41 is right: 31 + 10 = 41.
SHORTCUT Write the jumps under the list: +2, +4, +6, +8. Each jump is 2 more than the one before. So the next jump is +10.

### 817 | CIVIO-NUM-WP-PCT-CHANGE-000818
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A vendor borrows ₱30,000 at 6% simple interest per year. How much interest is due after 3 years?
A. ₱35,400
B. ₱54,000
C. ₱1,800
D. ₱5,400
MARKED ANSWER D. ₱5,400
WHY ₱5,400 is right. Check: 30,000 × 0.06 × 3 = 5,400.
SHORTCUT Find one year first: 6% of ₱30,000 = ₱1,800. Time is 3 years. Multiply: 3 × ₱1,800 = ₱5,400.

### 818 | CIVIO-NUM-FRAC-DEC-000819
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A barangay had 600 vitamin packs. It gave out 2/5 of them on Monday and 1/3 of the remaining vitamin packs on Tuesday. How many are left?
A. 240
B. 120
C. 160
D. 360
MARKED ANSWER A. 240
WHY 240 is right. Check: 240 + 120 + 240 = 600.
SHORTCUT Go day by day. Monday: 2/5 of 600 = 240, so 360 left. Tuesday: 1/3 of 360 = 120, so 360 − 120 = 240 left.

### 819 | CIVIO-NUM-WP-PCT-CHANGE-000820
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A supplier sold a set of school uniforms for ₱1,200. It raised the price by 20%. Later, it lowered the new price by 10%. What is the final price?
A. ₱1,440
B. ₱1,296
C. ₱1,555.20
D. ₱1,320
MARKED ANSWER B. ₱1,296
WHY ₱1,296 is right. Check: 1,200 × 1.2 = 1,440, and 1,440 × 0.9 = 1,296.
SHORTCUT Do one change at a time. ₱1,200 up 20% is ₱1,200 + ₱240 = ₱1,440. Then 10% of ₱1,440 is ₱144, so ₱1,440 − ₱144 = ₱1,296.

### 820 | CIVIO-NUM-WP-RATIO-000821
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Jun-jun and Joy will share ₱22,500 of allowance fund in the ratio 4 : 5. How much is Joy's share?
A. ₱4,500
B. ₱12,500
C. ₱10,000
D. ₱2,500
MARKED ANSWER B. ₱12,500
WHY ₱12,500 is right: 5 × ₱2,500 = ₱12,500. Check: ₱10,000 + ₱12,500 = ₱22,500.
SHORTCUT Add the ratio numbers to get equal parts: 4 + 5 = 9. One part = ₱22,500 ÷ 9 = ₱2,500. Then multiply by the parts you need.

### 821 | CIVIO-NUM-WP-PCT-CHANGE-000822
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A electric fan is priced at ₱640. It is sold at 20% off. How much does a buyer pay?
A. ₱768
B. ₱512
C. ₱128
D. ₱620
MARKED ANSWER B. ₱512
WHY ₱512 is right. Check: discount ₱128; ₱640 − ₱128 = ₱512.
SHORTCUT Pay 80% of the price: ₱640 × 0.8 = ₱512.

### 822 | CIVIO-NUM-WP-ALGEBRA-000823
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Nonoy is 3 times as old as his niece. In 5 years, Nonoy will be twice as old as the niece. How old is Nonoy now?
A. 5
B. 15
C. 20
D. 10
MARKED ANSWER B. 15
WHY 15 is right. Algebra: niece = s, Nonoy = 3s; 3s + 5 = 2(s + 5) gives s = 5, so Nonoy = 15.
SHORTCUT Try the choices. If Nonoy is 15, the niece is 5. In 5 years: 20 and 10. 20 = 2 × 10, so it works.

### 823 | CIVIO-NUM-SEQ-DIFF-000824
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What number comes next in the series?  5, 8, 12, 17, 23, ___
A. 29
B. 30
C. 31
D. 26
MARKED ANSWER B. 30
WHY 30 is right: 23 + 7 = 30.
SHORTCUT Write the jumps under the list: +3, +4, +5, +6. Each jump is 1 more than the one before. So the next jump is +7.

### 824 | CIVIO-NUM-WP-PCT-CHANGE-000825
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A umbrella set is priced at ₱640. It is sold at 35% off. How much does a buyer pay?
A. ₱864
B. ₱416
C. ₱605
D. ₱224
MARKED ANSWER B. ₱416
WHY ₱416 is right. Check: discount ₱224; ₱640 − ₱224 = ₱416.
SHORTCUT Pay 65% of the price: ₱640 × 0.65 = ₱416.

### 825 | CIVIO-NUM-WP-AVERAGE-000826
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
The average years of service of the 8 clerks in the civil registry is 11 years. One more person, with 20 years, joins them. What is the new average years of service?
A. 12 years
B. 12.12 years
C. 108 years
D. 15.5 years
MARKED ANSWER A. 12 years
WHY 12 years is right. Long way: 8 × 11 = 88; + 20 = 108; ÷ 9 = 12.
SHORTCUT The new person is 20 − 11 = 9 above the old average. Share that among all 9 people: 9 ÷ 9 = 1. Add it: 11 + 1 = 12.

### 826 | CIVIO-NUM-WP-GEOM-000827
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A rectangular school lot is 11 m long and 3 m wide. A chain-link fence costs ₱50 per meter. How much will it cost to put the chain-link fence around the whole school lot?
A. ₱28
B. ₱700
C. ₱1,650
D. ₱1,400
MARKED ANSWER D. ₱1,400
WHY ₱1,400 is right: 28 m × ₱50 = ₱1,400.
SHORTCUT Around = 2 × (11 + 3) = 28 m. Cost = 28 × ₱50.

### 827 | CIVIO-NUM-WP-ALGEBRA-000828
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Analyn is 4 times as old as her daughter. In 24 years, Analyn will be twice as old as the daughter. How old is Analyn now?
A. 72
B. 12
C. 48
D. 36
MARKED ANSWER C. 48
WHY 48 is right. Algebra: daughter = s, Analyn = 4s; 4s + 24 = 2(s + 24) gives s = 12, so Analyn = 48.
SHORTCUT Try the choices. If Analyn is 48, the daughter is 12. In 24 years: 72 and 36. 72 = 2 × 36, so it works.

### 828 | CIVIO-NUM-WP-PCT-CHANGE-000829
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A backpack is priced at ₱960. It is sold at 30% off. How much does a buyer pay?
A. ₱930
B. ₱1,248
C. ₱288
D. ₱672
MARKED ANSWER D. ₱672
WHY ₱672 is right. Check: discount ₱288; ₱960 − ₱288 = ₱672.
SHORTCUT Pay 70% of the price: ₱960 × 0.7 = ₱672.

### 829 | CIVIO-NUM-OPS-ORDER-000830
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What is the value of 5 + 7 × 6 − 6?
A. 41
B. 5
C. 66
D. 12
MARKED ANSWER A. 41
WHY 41 is right: 5 + 42 = 47, and 47 − 6 = 41.
SHORTCUT Circle the × first: 7 × 6 = 42. Then go left to right: 5 + 42 − 6.

### 830 | CIVIO-NUM-WP-PCT-CHANGE-000831
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A supplier sold a set of school uniforms for ₱150. It raised the price by 20%. Later, it lowered the new price by 30%. What is the final price?
A. ₱126
B. ₱151.20
C. ₱180
D. ₱135
MARKED ANSWER A. ₱126
WHY ₱126 is right. Check: 150 × 1.2 = 180, and 180 × 0.7 = 126.
SHORTCUT Do one change at a time. ₱150 up 20% is ₱150 + ₱30 = ₱180. Then 30% of ₱180 is ₱54, so ₱180 − ₱54 = ₱126.

### 831 | CIVIO-NUM-WP-PCT-CHANGE-000832
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A government employee borrows ₱25,000 at 3% simple interest per year. How much interest is due after 3 years?
A. ₱27,250
B. ₱22,500
C. ₱2,250
D. ₱750
MARKED ANSWER C. ₱2,250
WHY ₱2,250 is right. Check: 25,000 × 0.03 × 3 = 2,250.
SHORTCUT Find one year first: 3% of ₱25,000 = ₱750. Time is 3 years. Multiply: 3 × ₱750 = ₱2,250.

### 832 | CIVIO-NUM-OPS-ORDER-000833
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What is the value of 3 + 8 × 7 − 8?
A. 10
B. 51
C. -5
D. 69
MARKED ANSWER B. 51
WHY 51 is right: 3 + 56 = 59, and 59 − 8 = 51.
SHORTCUT Circle the × first: 8 × 7 = 56. Then go left to right: 3 + 56 − 8.

### 833 | CIVIO-NUM-WP-GEOM-000834
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A rectangular vegetable garden is 30 m long and 13 m wide. A fence costs ₱150 per meter. How much will it cost to put the fence around the whole vegetable garden?
A. ₱12,900
B. ₱58,500
C. ₱6,450
D. ₱86
MARKED ANSWER A. ₱12,900
WHY ₱12,900 is right: 86 m × ₱150 = ₱12,900.
SHORTCUT Around = 2 × (30 + 13) = 86 m. Cost = 86 × ₱150.

### 834 | CIVIO-NUM-WP-ALGEBRA-000835
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Aling Rosa is 3 times as old as her niece. In 7 years, Aling Rosa will be twice as old as the niece. How old is Aling Rosa now?
A. 21
B. 14
C. 7
D. 28
MARKED ANSWER A. 21
WHY 21 is right. Algebra: niece = s, Aling Rosa = 3s; 3s + 7 = 2(s + 7) gives s = 7, so Aling Rosa = 21.
SHORTCUT Try the choices. If Aling Rosa is 21, the niece is 7. In 7 years: 28 and 14. 28 = 2 × 14, so it works.

### 835 | CIVIO-NUM-SEQ-DIFF-000836
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which number should come next?  8, 13, 21, 32, 46, ___
A. 63
B. 51
C. 66
D. 60
MARKED ANSWER A. 63
WHY 63 is right: 46 + 17 = 63.
SHORTCUT Write the jumps under the list: +5, +8, +11, +14. Each jump is 3 more than the one before. So the next jump is +17.

### 836 | CIVIO-NUM-WP-PCT-CHANGE-000837
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A market stall sold a gallon of paint for ₱150. It raised the price by 20%. Later, it lowered the new price by 30%. What is the final price?
A. ₱135
B. ₱126
C. ₱151.20
D. ₱180
MARKED ANSWER B. ₱126
WHY ₱126 is right. Check: 150 × 1.2 = 180, and 180 × 0.7 = 126.
SHORTCUT Do one change at a time. ₱150 up 20% is ₱150 + ₱30 = ₱180. Then 30% of ₱180 is ₱54, so ₱180 − ₱54 = ₱126.

### 837 | CIVIO-NUM-WP-GEOM-000838
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A rectangular vegetable garden is 25 m long and 18 m wide. A edging costs ₱120 per meter. How much will it cost to put the edging around the whole vegetable garden?
A. ₱86
B. ₱54,000
C. ₱5,160
D. ₱10,320
MARKED ANSWER D. ₱10,320
WHY ₱10,320 is right: 86 m × ₱120 = ₱10,320.
SHORTCUT Around = 2 × (25 + 18) = 86 m. Cost = 86 × ₱120.

### 838 | CIVIO-NUM-OPS-ORDER-000839
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What is the value of 6 + 6 × 5 − 2?
A. 24
B. 15
C. 34
D. 58
MARKED ANSWER C. 34
WHY 34 is right: 6 + 30 = 36, and 36 − 2 = 34.
SHORTCUT Circle the × first: 6 × 5 = 30. Then go left to right: 6 + 30 − 2.

### 839 | CIVIO-NUM-SEQ-MULT-000840
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What number comes next?  5, 8, 14, 26, 50, ___
A. 96
B. 74
C. 98
D. 100
MARKED ANSWER C. 98
WHY 98 is right: 50 × 2 = 100, then − 2 gives 98.
SHORTCUT Test "times 2, then − 2" on the first numbers: 5 × 2 − 2 = 8; 8 × 2 − 2 = 14. It works, so use it on 50.

### 840 | CIVIO-NUM-FRAC-DEC-000841
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
A barangay had 900 notebooks. It gave out 2/5 of them on Monday and 1/6 of the remaining notebooks on Tuesday. How many are left?
A. 450
B. 90
C. 390
D. 540
MARKED ANSWER A. 450
WHY 450 is right. Check: 360 + 90 + 450 = 900.
SHORTCUT Go day by day. Monday: 2/5 of 900 = 360, so 540 left. Tuesday: 1/6 of 540 = 90, so 540 − 90 = 450 left.

### 841 | CIVIO-ANA-CONCLUSION-000842
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Four staff members are compared. Carlo lives nearer the office than Bea. Arnel lives nearer the office than Carlo. Bea lives nearer the office than Teresa. Who is second in the order (counting from the one who lives nearest)?
A. Carlo
B. Bea
C. Teresa
D. Arnel
MARKED ANSWER A. Carlo
WHY Carlo is right. The clues give Arnel → Carlo → Bea → Teresa, so Carlo is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Arnel → Carlo → Bea → Teresa.

### 842 | CIVIO-ANA-SYLLOGISM-000843
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Statement 1: Some auditors are choir members. Statement 2: All auditors are accountants. Which conclusion follows from both statements?
A. No accountants are choir members.
B. All choir members are auditors.
C. Some accountants are choir members.
D. All accountants are choir members.
MARKED ANSWER C. Some accountants are choir members.
WHY "Some accountants are choir members." is right. It follows from the two statements with no extra facts.
SHORTCUT The auditors who are choir members are also accountants. So at least some accountants are choir members.

### 843 | CIVIO-ANA-SYLLOGISM-000844
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Statement 1: No fish are recalled items. Statement 2: All tilapia are fish. Which conclusion follows from both statements?
A. All fish are tilapia.
B. No market goods are recalled items.
C. No tilapia are recalled items.
D. Some tilapia are recalled items.
MARKED ANSWER C. No tilapia are recalled items.
WHY "No tilapia are recalled items." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the tilapia circle inside fish. The "recalled items" circle sits outside fish, so it is outside tilapia too.

### 844 | CIVIO-ANA-ASSUME-I-II-000845
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Statement: The barangay held its assembly in the covered court.
Assumption I: Everyone in the barangay plays basketball.
Assumption II: The covered court is the largest room in the province.
Which assumption is implicit in the statement?
A. Neither I nor II
B. Only II
C. Both I and II
D. Only I
MARKED ANSWER A. Neither I nor II
WHY "Neither I nor II" is right. Neither assumption is needed; both go beyond the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 845 | CIVIO-ANA-CONCLUSION-000846
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Four staff members are compared. Paolo encoded more forms than Jomar. Cora encoded more forms than Paolo. Jomar encoded more forms than Bea. Who is second in the order (counting from the one who encoded the most forms)?
A. Cora
B. Bea
C. Jomar
D. Paolo
MARKED ANSWER D. Paolo
WHY Paolo is right. The clues give Cora → Paolo → Jomar → Bea, so Paolo is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Cora → Paolo → Jomar → Bea.

### 846 | CIVIO-ANA-SYMBOL-SERIES-000847
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What comes next in the series?  IU, KV, MW, OX, ___
A. PY
B. QY
C. QC
D. YQ
MARKED ANSWER B. QY
WHY QY is right: O + 2 = Q and X + 1 = Y.
SHORTCUT Split each pair. First letters: I, K, M, O (jump +2). Second letters: U, V, W, X (jump +1). Move each one more step.

### 847 | CIVIO-ANA-ANALOGY-FUNCTION-000848
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
HAMMER : NAIL :: ____
A. wood : board
B. screw : screwdriver
C. saw : carpenter
D. key : lock
MARKED ANSWER D. key : lock
WHY "key : lock" is right. It has the same link, tool : what it acts on, in the same order.
SHORTCUT Make a sentence for the stem: "hammer is to nail" as tool : what it acts on. Test each choice in that sentence.

### 848 | CIVIO-ANA-CONCLUSION-000849
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Four staff members are compared. Tess scored higher than Bong. Bong scored higher than Mylene. Ramon scored higher than Tess. Who is second in the order (counting from the one who got the highest score)?
A. Bong
B. Ramon
C. Tess
D. Mylene
MARKED ANSWER C. Tess
WHY Tess is right. The clues give Ramon → Tess → Bong → Mylene, so Tess is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Ramon → Tess → Bong → Mylene.

### 849 | CIVIO-ANA-CONCLUSION-000850
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Four staff members are compared. Aling Rosa has served longer than Ramon. Ramon has served longer than Jun-jun. Efren has served longer than Aling Rosa. Who is second in the order (counting from the one who has served the longest)?
A. Ramon
B. Efren
C. Aling Rosa
D. Jun-jun
MARKED ANSWER C. Aling Rosa
WHY Aling Rosa is right. The clues give Efren → Aling Rosa → Ramon → Jun-jun, so Aling Rosa is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Efren → Aling Rosa → Ramon → Jun-jun.

### 850 | CIVIO-ANA-SYMBOL-SERIES-000851
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In a certain code, LIBRARY is written as OLEUDUB. How is PAPER written in the same code?
A. SDSHU
B. TETIV
C. MXMBO
D. SDSHR
MARKED ANSWER A. SDSHU
WHY SDSHU is right: each letter of PAPER moved 3 places forward.
SHORTCUT Compare the first letters: L became O. That is 3 places forward. Check one more letter, then shift every letter of PAPER the same way.

### 851 | CIVIO-ANA-SYMBOL-SERIES-000852
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In a certain code, PUBLIC is written as SXEOLF. How is PERMIT written in the same code?
A. SHUPLW
B. MBOJFQ
C. SHUPLT
D. TIVQMX
MARKED ANSWER A. SHUPLW
WHY SHUPLW is right: each letter of PERMIT moved 3 places forward.
SHORTCUT Compare the first letters: P became S. That is 3 places forward. Check one more letter, then shift every letter of PERMIT the same way.

### 852 | CIVIO-ANA-SYLLOGISM-000853
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Assume these are true: a few of the tilapia are gifts from the province, and all of the tilapia are fish. What can be concluded for certain?
A. All gifts from the province are tilapia.
B. Some fish are gifts from the province.
C. All fish are gifts from the province.
D. No fish are gifts from the province.
MARKED ANSWER B. Some fish are gifts from the province.
WHY "Some fish are gifts from the province." is right. It follows from the two statements with no extra facts.
SHORTCUT The tilapia who are gifts from the province are also fish. So at least some fish are gifts from the province.

### 853 | CIVIO-ANA-SYLLOGISM-000854
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
All jeepneys are public vehicles. Some jeepneys are second-hand goods. Which conclusion must be true?
A. Some public vehicles are second-hand goods.
B. All public vehicles are second-hand goods.
C. No public vehicles are second-hand goods.
D. All second-hand goods are jeepneys.
MARKED ANSWER A. Some public vehicles are second-hand goods.
WHY "Some public vehicles are second-hand goods." is right. It follows from the two statements with no extra facts.
SHORTCUT The jeepneys who are second-hand goods are also public vehicles. So at least some public vehicles are second-hand goods.

### 854 | CIVIO-ANA-SYMBOL-SERIES-000855
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In a certain code, RIVER is written as PGTCP. How is BRIDGE written in the same code?
A. YOFADB
B. ZPGBEE
C. DTKFIG
D. ZPGBEC
MARKED ANSWER D. ZPGBEC
WHY ZPGBEC is right: each letter of BRIDGE moved 2 places back.
SHORTCUT Compare the first letters: R became P. That is 2 places back. Check one more letter, then shift every letter of BRIDGE the same way.

### 855 | CIVIO-ANA-DI-TABLE-000856
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Supply use of folders (packs) by office (Engineering: Apr 34, May 80, Jun 14; Planning: Apr 32, May 64, Jun 52; Library: Apr 30, May 66, Jun 34). In Jun, how many more did Planning use than Engineering?
A. 38
B. 2
C. 66
D. 20
MARKED ANSWER A. 38
WHY 38 is right: 52 − 14 = 38.
SHORTCUT Go to the Jun column: Planning 52, Engineering 14. Subtract the smaller from the larger.

### 856 | CIVIO-ANA-SYMBOL-SERIES-000857
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In a certain code, HEALTH is written as IFBMUI. How is FILES written in the same code?
A. HKNGU
B. GJMFT
C. EHKDR
D. GJMFS
MARKED ANSWER B. GJMFT
WHY GJMFT is right: each letter of FILES moved 1 place forward.
SHORTCUT Compare the first letters: H became I. That is 1 place forward. Check one more letter, then shift every letter of FILES the same way.

### 857 | CIVIO-ANA-SYMBOL-SERIES-000858
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What comes next in the series?  EK, HL, KM, NN, ___
A. OQ
B. QW
C. QO
D. OO
MARKED ANSWER C. QO
WHY QO is right: N + 3 = Q and N + 1 = O.
SHORTCUT Split each pair. First letters: E, H, K, N (jump +3). Second letters: K, L, M, N (jump +1). Move each one more step.

### 858 | CIVIO-ANA-SYMBOL-SERIES-000859
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In a certain code, NOTICE is written as LMRGAC. How is BOARD written in the same code?
A. ZMYPB
B. YLXOA
C. DQCTF
D. ZMYPD
MARKED ANSWER A. ZMYPB
WHY ZMYPB is right: each letter of BOARD moved 2 places back.
SHORTCUT Compare the first letters: N became L. That is 2 places back. Check one more letter, then shift every letter of BOARD the same way.

### 859 | CIVIO-ANA-DI-TABLE-000860
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Supply use of bond paper (reams) by office (Planning: Jan 24, Feb 34, Mar 54; Assessor: Jan 58, Feb 40, Mar 16; Records: Jan 58, Feb 44, Mar 66). In Mar, how many more did Records use than Assessor?
A. 50
B. 0
C. 54
D. 82
MARKED ANSWER A. 50
WHY 50 is right: 66 − 16 = 50.
SHORTCUT Go to the Mar column: Assessor 16, Records 66. Subtract the smaller from the larger.

### 860 | CIVIO-ANA-DI-TABLE-000861
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Supply use of staplers by office (Records: Jan 48, Feb 34, Mar 56; HR: Jan 10, Feb 32, Mar 32; Cashier: Jan 22, Feb 38, Mar 48). In Mar, how many more did Records use than Cashier?
A. 30
B. 104
C. 8
D. 26
MARKED ANSWER C. 8
WHY 8 is right: 56 − 48 = 8.
SHORTCUT Go to the Mar column: Cashier 48, Records 56. Subtract the smaller from the larger.

### 861 | CIVIO-ANA-SYMBOL-SERIES-000862
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What comes next in the series?  HR, LT, PV, TX, ___
A. ZX
B. XZ
C. UZ
D. XH
MARKED ANSWER B. XZ
WHY XZ is right: T + 4 = X and X + 2 = Z.
SHORTCUT Split each pair. First letters: H, L, P, T (jump +4). Second letters: R, T, V, X (jump +2). Move each one more step.

### 862 | CIVIO-ANA-SYLLOGISM-000863
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Assume these are true: none of the elected officials are job-order hires, and every one of the barangay captains is among the elected officials. What can be concluded for certain?
A. All elected officials are barangay captains.
B. Some barangay captains are job-order hires.
C. No public officers are job-order hires.
D. No barangay captains are job-order hires.
MARKED ANSWER D. No barangay captains are job-order hires.
WHY "No barangay captains are job-order hires." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the barangay captains circle inside elected officials. The "job-order hires" circle sits outside elected officials, so it is outside barangay captains too.

### 863 | CIVIO-ANA-DI-TABLE-000864
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Supply use of bond paper (reams) by office (HR: Apr 34, May 60, Jun 60; Assessor: Apr 26, May 32, Jun 62; Records: Apr 52, May 58, Jun 22). How many did Assessor use in all three months?
A. 120
B. 150
C. 40
D. 58
MARKED ANSWER A. 120
WHY 120 is right: 26 + 32 + 62 = 120.
SHORTCUT Read across the Assessor row only: 26 + 32 + 62.

### 864 | CIVIO-ANA-SYMBOL-SERIES-000865
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What comes next in the series?  AM, EP, IS, MV, ___
A. QC
B. YQ
C. QY
D. NY
MARKED ANSWER C. QY
WHY QY is right: M + 4 = Q and V + 3 = Y.
SHORTCUT Split each pair. First letters: A, E, I, M (jump +4). Second letters: M, P, S, V (jump +3). Move each one more step.

### 865 | CIVIO-ANA-ASSUME-I-II-000866
TRACK professional | DOMAIN analytical | SKILL Assumptions and conclusions | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Statement: The town band played at the opening of the new public market.
Assumption I: Every vendor in the market is a musician.
Assumption II: The market will close if the band does not play again.
Which assumption is implicit in the statement?
A. Only II
B. Both I and II
C. Only I
D. Neither I nor II
MARKED ANSWER D. Neither I nor II
WHY "Neither I nor II" is right. Neither assumption is needed; both go beyond the statement.
SHORTCUT Negate each assumption. If the statement stops making sense, the assumption is needed.

### 866 | CIVIO-VEN-SENT-COMP-WORD-000867
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: To save paper, the office will ____ old forms as scratch pads.
A. discard
B. reuse
C. refuse
D. reused
MARKED ANSWER B. reuse
WHY "reuse" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 867 | CIVIO-VEN-SENT-COMP-WORD-000868
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The new rule is different ____ the old one.
A. with
B. at
C. of
D. from
MARKED ANSWER D. from
WHY "from" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 868 | CIVIO-VEN-SENT-COMP-WORD-000869
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The guard will ____ visitors to sign the logbook.
A. devise
B. advice
C. advise
D. advised
MARKED ANSWER C. advise
WHY "advise" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 869 | CIVIO-VEN-WORD-MEANING-000870
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is closest in meaning to the word in capital letters?  CONCISE
A. wordy
B. concave
C. precise
D. brief
MARKED ANSWER D. brief
WHY "brief" is right. "Concise" means brief.
SHORTCUT Make a short sentence with "concise", then swap in each choice. Watch for words that only look or sound like "concise".

### 870 | CIVIO-VEN-ERROR-TENSE-000871
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the correct verb: Since January, the barangay hall staff ____ the plaza on time each week.
A. will clean
B. has cleaned
C. will have cleaned
D. cleaned
MARKED ANSWER B. has cleaned
WHY "has cleaned" is right: the present perfect matches "Since January".
SHORTCUT Find the time signal first: "Since January". It calls for the present perfect.

### 871 | CIVIO-VEN-ERROR-TENSE-000872
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the correct verb: Right now, Nestor ____ the voters' list.
A. is updating
B. updates
C. updated
D. will have updated
MARKED ANSWER A. is updating
WHY "is updating" is right: the present progressive matches "Right now".
SHORTCUT Find the time signal first: "Right now". It calls for the present progressive.

### 872 | CIVIO-VEN-SENT-COMP-WORD-000873
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The money was split ____ the two schools.
A. through
B. among
C. across
D. between
MARKED ANSWER D. between
WHY "between" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 873 | CIVIO-VEN-ERROR-AGREE-000874
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The leader of the volunteers ____ at every barangay assembly.
A. to speak
B. speak
C. speaking
D. speaks
MARKED ANSWER D. speaks
WHY "speaks" is right: "The leader" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The leader ____". The subject is singular, so use the singular verb.

### 874 | CIVIO-VEN-ERROR-TENSE-000875
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the correct verb: Next month, Arnel ____ the plaza.
A. cleaned
B. has cleaned
C. will have cleaned
D. will clean
MARKED ANSWER D. will clean
WHY "will clean" is right: the simple future matches "Next month".
SHORTCUT Find the time signal first: "Next month". It calls for the simple future.

### 875 | CIVIO-VEN-WORD-MEANING-000876
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  LENIENT
A. tolerant
B. strict
C. lending
D. lean
MARKED ANSWER B. strict
WHY "strict" is right. "Lenient" means tolerant; "strict" is the reverse.
SHORTCUT First say what "lenient" means (tolerant). Then look for the word that means the reverse.

### 876 | CIVIO-VEN-SENT-COMP-WORD-000877
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: Do not ____ the receipt; you will need it for the refund.
A. loss
B. lost
C. loose
D. lose
MARKED ANSWER D. lose
WHY "lose" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 877 | CIVIO-VEN-WORD-MEANING-000878
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is closest in meaning to the word in capital letters?  TRANSPARENT
A. hidden
B. transport
C. transient
D. open
MARKED ANSWER D. open
WHY "open" is right. "Transparent" means open.
SHORTCUT Make a short sentence with "transparent", then swap in each choice. Watch for words that only look or sound like "transparent".

### 878 | CIVIO-VEN-SENT-COMP-WORD-000879
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The office ran out of ____ for the printer.
A. station
B. stationed
C. stationary
D. stationery
MARKED ANSWER D. stationery
WHY "stationery" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 879 | CIVIO-VEN-SENT-COMP-WORD-000880
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The guard remained ____ even when the crowd shouted at him.
A. angry
B. calm
C. calmly
D. calf
MARKED ANSWER B. calm
WHY "calm" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 880 | CIVIO-VEN-RC-VOCAB-000881
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The speaker tried to CHECK her anger during the hearing.
A. pay by bank note
B. hold back
C. examine
D. let loose
MARKED ANSWER B. hold back
WHY "hold back" is right: it is the sense of "check" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "check".

### 881 | CIVIO-VEN-SENT-COMP-PHRASAL-000882
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the phrase that best completes the sentence: The chief asked us to ____ the noise during the exam.
A. cut in
B. cut out
C. cut off
D. cut down on
MARKED ANSWER D. cut down on
WHY "cut down on" is right. It gives the meaning the sentence needs.
SHORTCUT Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.

### 882 | CIVIO-VEN-ERROR-AGREE-000883
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The cost of the repairs ____ doubled since last year.
A. have
B. having
C. to have
D. has
MARKED ANSWER D. has
WHY "has" is right: "The cost" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The cost ____". The subject is singular, so use the singular verb.

### 883 | CIVIO-VEN-ERROR-AGREE-000884
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Choose the word that best completes the sentence: The members of the board ____ given copies of the agenda.
A. been
B. being
C. were
D. was
MARKED ANSWER C. were
WHY "were" is right: "The members" is plural.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The members ____". The subject is plural, so use the plural verb.

### 884 | CIVIO-VEN-RC-VOCAB-000885
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The judge asked the witness to STATE her name.
A. hide
B. say clearly
C. province
D. condition
MARKED ANSWER B. say clearly
WHY "say clearly" is right: it is the sense of "state" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "state".

### 885 | CIVIO-VEN-WORD-MEANING-000886
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  DETERIORATE
A. determine
B. improve
C. detour
D. worsen
MARKED ANSWER B. improve
WHY "improve" is right. "Deteriorate" means worsen; "improve" is the reverse.
SHORTCUT First say what "deteriorate" means (worsen). Then look for the word that means the reverse.

### 886 | CIVIO-CLR-SPELL-RIGHT-000887
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is spelled correctly?  liaison | liaisson | liison | liason
A. liaison
B. liaisson
C. liison
D. liason
MARKED ANSWER A. liaison
WHY "liaison" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 887 | CIVIO-CLR-FILE-POSITION-000888
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed FIRST?  Alfredo G. Santos-Ocampo | Imelda A. Bautista | Engr. Danilo A. Aquino | Atty. Teresita L. Jose
A. Imelda A. Bautista
B. Alfredo G. Santos-Ocampo
C. Atty. Teresita L. Jose
D. Engr. Danilo A. Aquino
MARKED ANSWER D. Engr. Danilo A. Aquino
WHY "Engr. Danilo A. Aquino" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Engr. Danilo A. Aquino → AQUINO, Danilo; Imelda A. Bautista → BAUTISTA, Imelda; Atty. Teresita L. Jose → JOSE, Teresita; Alfredo G. Santos-Ocampo → SANTOSOCAMPO, Alfredo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 888 | CIVIO-CLR-SPELL-WRONG-000889
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is misspelled?  beginning | embarrass | indpendence | receipt
A. beginning
B. embarrass
C. indpendence
D. receipt
MARKED ANSWER C. indpendence
WHY "indpendence" is misspelled: it drops a letter. The correct spelling is "independence".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 889 | CIVIO-CLR-FILE-POSITION-000890
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed FIRST?  Engr. Victoria C. Pedro | Teresita C. Castillo | Atty. Jose L. Navarro | Engr. Andres N. Cruz
A. Engr. Andres N. Cruz
B. Engr. Victoria C. Pedro
C. Teresita C. Castillo
D. Atty. Jose L. Navarro
MARKED ANSWER C. Teresita C. Castillo
WHY "Teresita C. Castillo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Teresita C. Castillo → CASTILLO, Teresita; Engr. Andres N. Cruz → CRUZ, Andres; Atty. Jose L. Navarro → NAVARRO, Jose; Engr. Victoria C. Pedro → PEDRO, Victoria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 890 | CIVIO-CLR-SPELL-RIGHT-000891
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is spelled correctly?  noticeable | noticeible | notticeable | noticable
A. noticeable
B. noticeible
C. notticeable
D. noticable
MARKED ANSWER A. noticeable
WHY "noticeable" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 891 | CIVIO-CLR-SPELL-WRONG-000892
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is misspelled?  surveillance | occasionally | beleve | definitely
A. surveillance
B. occasionally
C. beleve
D. definitely
MARKED ANSWER C. beleve
WHY "beleve" is misspelled: it drops a letter. The correct spelling is "believe".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 892 | CIVIO-CLR-SPELL-WRONG-000893
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is misspelled?  unanimous | appropriation | occrrence | schedule
A. unanimous
B. appropriation
C. occrrence
D. schedule
MARKED ANSWER C. occrrence
WHY "occrrence" is misspelled: it drops a letter. The correct spelling is "occurrence".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 893 | CIVIO-CLR-FILE-POSITION-000894
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed FIRST?  Elena L. De Guzman | Rosario N. Santos-Ocampo | Dr. Liza D. Garcia-Lopez | Alfredo T. Jose
A. Dr. Liza D. Garcia-Lopez
B. Alfredo T. Jose
C. Rosario N. Santos-Ocampo
D. Elena L. De Guzman
MARKED ANSWER D. Elena L. De Guzman
WHY "Elena L. De Guzman" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Elena L. De Guzman → DEGUZMAN, Elena; Dr. Liza D. Garcia-Lopez → GARCIALOPEZ, Liza; Alfredo T. Jose → JOSE, Alfredo; Rosario N. Santos-Ocampo → SANTOSOCAMPO, Rosario.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 894 | CIVIO-CLR-FILE-POSITION-000895
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed FIRST?  Maria B. Dizon | Andres D. Navarro | Imelda N. Manalo | Teresita M. De los Santos
A. Imelda N. Manalo
B. Teresita M. De los Santos
C. Andres D. Navarro
D. Maria B. Dizon
MARKED ANSWER B. Teresita M. De los Santos
WHY "Teresita M. De los Santos" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Teresita M. De los Santos → DELOSSANTOS, Teresita; Maria B. Dizon → DIZON, Maria; Imelda N. Manalo → MANALO, Imelda; Andres D. Navarro → NAVARRO, Andres.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 895 | CIVIO-CLR-FILE-POSITION-000896
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed LAST?  Dr. Ernesto N. Cruz-Manalo | Engr. Ramon T. Del Rosario | Eduardo L. Dela Cruz | Imelda T. Manalo
A. Imelda T. Manalo
B. Eduardo L. Dela Cruz
C. Dr. Ernesto N. Cruz-Manalo
D. Engr. Ramon T. Del Rosario
MARKED ANSWER A. Imelda T. Manalo
WHY "Imelda T. Manalo" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Dr. Ernesto N. Cruz-Manalo → CRUZMANALO, Ernesto; Eduardo L. Dela Cruz → DELACRUZ, Eduardo; Engr. Ramon T. Del Rosario → DELROSARIO, Ramon; Imelda T. Manalo → MANALO, Imelda.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 896 | CIVIO-CLR-FILE-POSITION-000897
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed LAST?  Engr. Rosario R. San Juan | Engr. Teresita B. Austria | Cristina C. Flores | Dr. Maria C. Navarro
A. Cristina C. Flores
B. Dr. Maria C. Navarro
C. Engr. Rosario R. San Juan
D. Engr. Teresita B. Austria
MARKED ANSWER C. Engr. Rosario R. San Juan
WHY "Engr. Rosario R. San Juan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Engr. Teresita B. Austria → AUSTRIA, Teresita; Cristina C. Flores → FLORES, Cristina; Dr. Maria C. Navarro → NAVARRO, Maria; Engr. Rosario R. San Juan → SANJUAN, Rosario.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 897 | CIVIO-CLR-SPELL-WRONG-000898
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is misspelled?  liaison | acquaintance | correspondance | colleague
A. liaison
B. acquaintance
C. correspondance
D. colleague
MARKED ANSWER C. correspondance
WHY "correspondance" is misspelled: it is spelled the way the word sounds. The correct spelling is "correspondence".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 898 | CIVIO-CLR-FILE-POSITION-000899
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In alphabetical filing, which name is filed LAST?  Rosario S. Del Mundo | Corazon V. Navarro | Evelyn L. Delos Reyes | Jose S. San Pedro
A. Rosario S. Del Mundo
B. Jose S. San Pedro
C. Corazon V. Navarro
D. Evelyn L. Delos Reyes
MARKED ANSWER B. Jose S. San Pedro
WHY "Jose S. San Pedro" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Rosario S. Del Mundo → DELMUNDO, Rosario; Evelyn L. Delos Reyes → DELOSREYES, Evelyn; Corazon V. Navarro → NAVARRO, Corazon; Jose S. San Pedro → SANPEDRO, Jose.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 899 | CIVIO-CLR-SPELL-RIGHT-000900
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is spelled correctly?  cemetery | cemetary | cemettery | cemtery
A. cemetery
B. cemetary
C. cemettery
D. cemtery
MARKED ANSWER A. cemetery
WHY "cemetery" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 900 | CIVIO-CLR-SPELL-RIGHT-000901
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Which word is spelled correctly?  occurence | occrrence | occurrance | occurrence
A. occurence
B. occrrence
C. occurrance
D. occurrence
MARKED ANSWER D. occurrence
WHY "occurrence" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 901 | CIVIO-GI-TERM-MATCH-000902
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Under the 1987 Constitution, the right of government employees to do what shall not be denied?
A. Hold two government posts
B. Strike
C. Self-organization
D. Campaign for candidates
MARKED ANSWER C. Self-organization
WHY "Self-organization" is right. Art. IX-B, Sec. 2(5) says: "The right to self-organization shall not be denied to government employees".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 2(5). Employees may form unions (self-organization).
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 902 | CIVIO-GI-DEADLINE-NUMBER-000903
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
How many Senators make up the Senate under the 1987 Constitution?
A. 24
B. 30
C. 25
D. 12
MARKED ANSWER A. 24
WHY "24" is right. Art. VI, Sec. 2 says: "The Senate shall be composed of twenty-four Senators".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 2. The Senate has 24 members elected at large.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 903 | CIVIO-GI-DEADLINE-NUMBER-000904
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
How many members does the Commission on Audit have, counting the Chairman?
A. 3
B. 7
C. 2
D. 5
MARKED ANSWER A. 3
WHY "3" is right. Art. IX-D, Sec. 1(1) says: "composed of a Chairman and two Commissioners".
SHORTCUT Tie the fact to its section: Art. IX-D, Sec. 1(1). COA: a Chairman and two Commissioners.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 904 | CIVIO-GI-WHO-HOLDS-POWER-000905
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
In whom is legislative power vested under the 1987 Constitution?
A. The Commission on Elections
B. The Supreme Court
C. The Congress of the Philippines
D. The President
MARKED ANSWER C. The Congress of the Philippines
WHY "The Congress of the Philippines" is right. Art. VI, Sec. 1 says: "The legislative power shall be vested in the Congress of the Philippines".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 1. Congress (Senate and House) holds legislative power.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 905 | CIVIO-GI-WHO-HOLDS-POWER-000906
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What does the 1987 Constitution say about suing the State?
A. The State may be sued in any court at any time
B. The State may be sued only by foreigners
C. The State may not be sued without its consent
D. Only the President may be sued
MARKED ANSWER C. The State may not be sued without its consent
WHY "The State may not be sued without its consent" is right. Art. XVI, Sec. 3 says: "The State may not be sued without its consent".
SHORTCUT Tie the fact to its section: Art. XVI, Sec. 3. State immunity from suit.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 906 | CIVIO-GI-TERM-MATCH-000907
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Under the 1987 Constitution, can a civil service officer or employee be suspended or dismissed without cause?
A. No; only for cause provided by law
B. Yes, after 30 days' notice
C. Only during the first year of service
D. Yes, at the pleasure of the head of office
MARKED ANSWER A. No; only for cause provided by law
WHY "No; only for cause provided by law" is right. Art. IX-B, Sec. 2(3) says: "No officer or employee of the civil service shall be removed or suspended except for cause provided by law".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 2(3). Security of tenure: removal only for legal cause.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 907 | CIVIO-GI-TERM-MATCH-000908
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Under R.A. 6713, may a public official use confidential information known by reason of office for private advantage?
A. Yes, if no money is involved
B. No
C. Yes, after leaving office
D. Yes, with a superior's consent
MARKED ANSWER B. No
WHY "No" is right. R.A. 6713, Sec. 7(c) says: "Disclosure and/or misuse of confidential information".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 7(c). Misuse of confidential information is prohibited.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 908 | CIVIO-GI-TERM-MATCH-000909
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Under the 1987 Constitution, appointments in the civil service shall be made only according to what?
A. Merit and fitness, determined as far as practicable by competitive examination
B. Seniority alone
C. Length of residence in the area
D. Recommendation of a local official
MARKED ANSWER A. Merit and fitness, determined as far as practicable by competitive examination
WHY "Merit and fitness, determined as far as practicable by competitive examination" is right. Art. IX-B, Sec. 2(2) says: "according to merit and fitness to be determined, as far as practicable".
SHORTCUT Tie the fact to its section: Art. IX-B, Sec. 2(2). Merit and fitness is the constitutional rule.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 909 | CIVIO-GI-DEADLINE-NUMBER-000910
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
What vote of each House is needed to override a presidential veto?
A. Majority of all its Members
B. Three-fourths of all its Members
C. One-third of all its Members
D. Two-thirds of all its Members
MARKED ANSWER D. Two-thirds of all its Members
WHY "Two-thirds of all its Members" is right. Art. VI, Sec. 27(1) says: "two-thirds of all the Members of that House".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 27(1). Override: two-thirds in each House.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 910 | CIVIO-GI-WHO-HOLDS-POWER-000911
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-010.json
STEM
Under the 1987 Constitution, who owns lands of the public domain, waters, minerals, and other natural resources?
A. The State
B. The local government units where they are found
C. The first private person to claim them
D. The President personally
MARKED ANSWER A. The State
WHY "The State" is right. Art. XII, Sec. 2 says: "are owned by the State".
SHORTCUT Tie the fact to its section: Art. XII, Sec. 2. Regalian doctrine: the State owns natural resources.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 911 | CIVIO-NUM-OPS-ORDER-000912
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What is the value of 7 + 3 × 6 − 11?
A. 49
B. -8
C. 5
D. 14
MARKED ANSWER D. 14
WHY 14 is right: 7 + 18 = 25, and 25 − 11 = 14.
SHORTCUT Circle the × first: 3 × 6 = 18. Then go left to right: 7 + 18 − 11.

### 912 | CIVIO-NUM-WP-PCT-CHANGE-000913
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A rice cooker is priced at ₱1,800. It is sold at 30% off. How much does a buyer pay?
A. ₱540
B. ₱1,260
C. ₱1,770
D. ₱2,340
MARKED ANSWER B. ₱1,260
WHY ₱1,260 is right. Check: discount ₱540; ₱1,800 − ₱540 = ₱1,260.
SHORTCUT Pay 70% of the price: ₱1,800 × 0.7 = ₱1,260.

### 913 | CIVIO-NUM-OPS-ORDER-000914
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What is the value of 10 + 6 × 7 − 6?
A. 106
B. 17
C. 46
D. 16
MARKED ANSWER C. 46
WHY 46 is right: 10 + 42 = 52, and 52 − 6 = 46.
SHORTCUT Circle the × first: 6 × 7 = 42. Then go left to right: 10 + 42 − 6.

### 914 | CIVIO-NUM-SEQ-DIFF-000915
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which number should come next?  6, 8, 13, 21, 32, ___
A. 49
B. 43
C. 34
D. 46
MARKED ANSWER D. 46
WHY 46 is right: 32 + 14 = 46.
SHORTCUT Write the jumps under the list: +2, +5, +8, +11. Each jump is 3 more than the one before. So the next jump is +14.

### 915 | CIVIO-NUM-WP-AVERAGE-000916
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
The average age of the 7 teachers in the barangay hall is 21 years. One more person, with 29 years, joins them. What is the new average age?
A. 25 years
B. 22 years
C. 22.14 years
D. 176 years
MARKED ANSWER B. 22 years
WHY 22 years is right. Long way: 7 × 21 = 147; + 29 = 176; ÷ 8 = 22.
SHORTCUT The new person is 29 − 21 = 8 above the old average. Share that among all 8 people: 8 ÷ 8 = 1. Add it: 21 + 1 = 22.

### 916 | CIVIO-NUM-WP-PCT-CHANGE-000917
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A office chair is priced at ₱400. It is sold at 35% off. How much does a buyer pay?
A. ₱365
B. ₱260
C. ₱540
D. ₱140
MARKED ANSWER B. ₱260
WHY ₱260 is right. Check: discount ₱140; ₱400 − ₱140 = ₱260.
SHORTCUT Pay 65% of the price: ₱400 × 0.65 = ₱260.

### 917 | CIVIO-NUM-WP-PCT-CHANGE-000918
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A hardware store sold a bag of cement for ₱150. It raised the price by 40%. Later, it lowered the new price by 10%. What is the final price?
A. ₱195
B. ₱189
C. ₱264.60
D. ₱210
MARKED ANSWER B. ₱189
WHY ₱189 is right. Check: 150 × 1.4 = 210, and 210 × 0.9 = 189.
SHORTCUT Do one change at a time. ₱150 up 40% is ₱150 + ₱60 = ₱210. Then 10% of ₱210 is ₱21, so ₱210 − ₱21 = ₱189.

### 918 | CIVIO-NUM-SEQ-MULT-000919
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What number comes next?  1, 6, 21, 66, 201, ___
A. 606
B. 609
C. 336
D. 603
MARKED ANSWER A. 606
WHY 606 is right: 201 × 3 = 603, then + 3 gives 606.
SHORTCUT Test "times 3, then + 3" on the first numbers: 1 × 3 + 3 = 6; 6 × 3 + 3 = 21. It works, so use it on 201.

### 919 | CIVIO-NUM-WP-GEOM-000920
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A rectangular basketball court is 34 m long and 20 m wide. A edging costs ₱25 per meter. How much will it cost to put the edging around the whole basketball court?
A. ₱108
B. ₱2,700
C. ₱1,350
D. ₱17,000
MARKED ANSWER B. ₱2,700
WHY ₱2,700 is right: 108 m × ₱25 = ₱2,700.
SHORTCUT Around = 2 × (34 + 20) = 108 m. Cost = 108 × ₱25.

### 920 | CIVIO-NUM-WP-PCT-CHANGE-000921
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A supplier sold a tank of LPG for ₱600. It raised the price by 40%. Later, it lowered the new price by 20%. What is the final price?
A. ₱672
B. ₱720
C. ₱840
D. ₱940.80
MARKED ANSWER A. ₱672
WHY ₱672 is right. Check: 600 × 1.4 = 840, and 840 × 0.8 = 672.
SHORTCUT Do one change at a time. ₱600 up 40% is ₱600 + ₱240 = ₱840. Then 20% of ₱840 is ₱168, so ₱840 − ₱168 = ₱672.

### 921 | CIVIO-NUM-WP-RATE-000922
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Tess can sort a sack of mail in 12 hours. Bea can do the same job in 4 hours. Working together, how long will they take?
A. 16 hours
B. 3 hours
C. 8 hours
D. 20 minutes
MARKED ANSWER B. 3 hours
WHY 3 hours is right. Check: in 3 hours, Tess does 3/12 and Bea does 3/4; together that is 1 whole job.
SHORTCUT Per hour, Tess does 1/12 and Bea does 1/4. Together: 1/12 + 1/4 = 1/3. So the whole job takes 3 hours.

### 922 | CIVIO-NUM-WP-PCT-CHANGE-000923
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A farmer borrows ₱15,000 at 10% simple interest per year. How much interest is due after 3 years and 6 months?
A. ₱5,250
B. ₱4,500
C. ₱20,250
D. ₱5,400
MARKED ANSWER A. ₱5,250
WHY ₱5,250 is right. Check: 15,000 × 0.1 × 3.5 = 5,250.
SHORTCUT Find one year first: 10% of ₱15,000 = ₱1,500. Time is 3.5 years. Multiply: 3.5 × ₱1,500 = ₱5,250.

### 923 | CIVIO-NUM-WP-PCT-CHANGE-000924
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A umbrella set is priced at ₱1,800. It is sold at 35% off. How much does a buyer pay?
A. ₱630
B. ₱2,430
C. ₱1,765
D. ₱1,170
MARKED ANSWER D. ₱1,170
WHY ₱1,170 is right. Check: discount ₱630; ₱1,800 − ₱630 = ₱1,170.
SHORTCUT Pay 65% of the price: ₱1,800 × 0.65 = ₱1,170.

### 924 | CIVIO-NUM-WP-RATIO-000925
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A ₱15,000 prize money is divided between Jun-jun and Liza in the ratio 3 : 7. What is Liza's share?
A. ₱1,500
B. ₱4,500
C. ₱2,142.86
D. ₱10,500
MARKED ANSWER D. ₱10,500
WHY ₱10,500 is right: 7 × ₱1,500 = ₱10,500. Check: ₱4,500 + ₱10,500 = ₱15,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱15,000 ÷ 10 = ₱1,500. Then multiply by the parts you need.

### 925 | CIVIO-NUM-WP-AVERAGE-000926
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
The average years of service of the 6 barangay health workers in the barangay hall is 8 years. One more person, with 15 years, joins them. What is the new average years of service?
A. 63 years
B. 11.5 years
C. 9 years
D. 9.17 years
MARKED ANSWER C. 9 years
WHY 9 years is right. Long way: 6 × 8 = 48; + 15 = 63; ÷ 7 = 9.
SHORTCUT The new person is 15 − 8 = 7 above the old average. Share that among all 7 people: 7 ÷ 7 = 1. Add it: 8 + 1 = 9.

### 926 | CIVIO-NUM-WP-AVERAGE-000927
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
The average years of service of the 8 drivers in the public library is 13 years. One more person, with 40 years, joins them. What is the new average years of service?
A. 144 years
B. 16 years
C. 16.38 years
D. 26.5 years
MARKED ANSWER B. 16 years
WHY 16 years is right. Long way: 8 × 13 = 104; + 40 = 144; ÷ 9 = 16.
SHORTCUT The new person is 40 − 13 = 27 above the old average. Share that among all 9 people: 27 ÷ 9 = 3. Add it: 13 + 3 = 16.

### 927 | CIVIO-NUM-WP-PCT-CHANGE-000928
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A sari-sari store sold a bag of cement for ₱800. It raised the price by 50%. Later, it lowered the new price by 40%. What is the final price?
A. ₱720
B. ₱1,080
C. ₱1,200
D. ₱880
MARKED ANSWER A. ₱720
WHY ₱720 is right. Check: 800 × 1.5 = 1,200, and 1,200 × 0.6 = 720.
SHORTCUT Do one change at a time. ₱800 up 50% is ₱800 + ₱400 = ₱1,200. Then 40% of ₱1,200 is ₱480, so ₱1,200 − ₱480 = ₱720.

### 928 | CIVIO-NUM-WP-RATIO-000929
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Mang Jun and Datu will share ₱3,500 of prize money in the ratio 3 : 4. How much is Datu's share?
A. ₱1,500
B. ₱2,000
C. ₱875
D. ₱500
MARKED ANSWER B. ₱2,000
WHY ₱2,000 is right: 4 × ₱500 = ₱2,000. Check: ₱1,500 + ₱2,000 = ₱3,500.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 4 = 7. One part = ₱3,500 ÷ 7 = ₱500. Then multiply by the parts you need.

### 929 | CIVIO-NUM-FRAC-DEC-000930
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A barangay had 480 hygiene kits. It gave out 1/6 of them on Monday and 3/4 of the remaining hygiene kits on Tuesday. How many are left?
A. 400
B. 40
C. 300
D. 100
MARKED ANSWER D. 100
WHY 100 is right. Check: 80 + 300 + 100 = 480.
SHORTCUT Go day by day. Monday: 1/6 of 480 = 80, so 400 left. Tuesday: 3/4 of 400 = 300, so 400 − 300 = 100 left.

### 930 | CIVIO-NUM-WP-RATE-000931
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Carlo can repack the relief goods in 3 hours. Kimberly can do the same job in 6 hours. Working together, how long will they take?
A. 4.5 hours
B. 30 minutes
C. 2 hours
D. 9 hours
MARKED ANSWER C. 2 hours
WHY 2 hours is right. Check: in 2 hours, Carlo does 2/3 and Kimberly does 2/6; together that is 1 whole job.
SHORTCUT Per hour, Carlo does 1/3 and Kimberly does 1/6. Together: 1/3 + 1/6 = 1/2. So the whole job takes 2 hours.

### 931 | CIVIO-NUM-OPS-ORDER-000932
TRACK both | DOMAIN numerical | SKILL Basic operations | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What is the value of 20 + 5 × 3 − 1?
A. 74
B. 27
C. 34
D. 30
MARKED ANSWER C. 34
WHY 34 is right: 20 + 15 = 35, and 35 − 1 = 34.
SHORTCUT Circle the × first: 5 × 3 = 15. Then go left to right: 20 + 15 − 1.

### 932 | CIVIO-NUM-WP-RATIO-000933
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Rhea and Arnel will share ₱30,000 of prize money in the ratio 3 : 7. How much is Arnel's share?
A. ₱4,285.71
B. ₱3,000
C. ₱21,000
D. ₱9,000
MARKED ANSWER C. ₱21,000
WHY ₱21,000 is right: 7 × ₱3,000 = ₱21,000. Check: ₱9,000 + ₱21,000 = ₱30,000.
SHORTCUT Add the ratio numbers to get equal parts: 3 + 7 = 10. One part = ₱30,000 ÷ 10 = ₱3,000. Then multiply by the parts you need.

### 933 | CIVIO-NUM-WP-GEOM-000934
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A rectangular drying yard is 29 m long and 10 m wide. A edging costs ₱40 per meter. How much will it cost to put the edging around the whole drying yard?
A. ₱3,120
B. ₱78
C. ₱11,600
D. ₱1,560
MARKED ANSWER A. ₱3,120
WHY ₱3,120 is right: 78 m × ₱40 = ₱3,120.
SHORTCUT Around = 2 × (29 + 10) = 78 m. Cost = 78 × ₱40.

### 934 | CIVIO-NUM-WP-RATE-000935
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Marites can paint a classroom in 4 hours. Carlo can do the same job in 12 hours. Working together, how long will they take?
A. 20 minutes
B. 16 hours
C. 3 hours
D. 8 hours
MARKED ANSWER C. 3 hours
WHY 3 hours is right. Check: in 3 hours, Marites does 3/4 and Carlo does 3/12; together that is 1 whole job.
SHORTCUT Per hour, Marites does 1/4 and Carlo does 1/12. Together: 1/4 + 1/12 = 1/3. So the whole job takes 3 hours.

### 935 | CIVIO-NUM-WP-ALGEBRA-000936
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Inday is 3 times as old as her niece. In 14 years, Inday will be twice as old as the niece. How old is Inday now?
A. 56
B. 28
C. 42
D. 14
MARKED ANSWER C. 42
WHY 42 is right. Algebra: niece = s, Inday = 3s; 3s + 14 = 2(s + 14) gives s = 14, so Inday = 42.
SHORTCUT Try the choices. If Inday is 42, the niece is 14. In 14 years: 56 and 28. 56 = 2 × 28, so it works.

### 936 | CIVIO-NUM-WP-ALGEBRA-000937
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Ramon is 4 times as old as his niece. In 8 years, Ramon will be three times as old as the niece. How old is Ramon now?
A. 72
B. 24
C. 64
D. 16
MARKED ANSWER C. 64
WHY 64 is right. Algebra: niece = s, Ramon = 4s; 4s + 8 = 3(s + 8) gives s = 16, so Ramon = 64.
SHORTCUT Try the choices. If Ramon is 64, the niece is 16. In 8 years: 72 and 24. 72 = 3 × 24, so it works.

### 937 | CIVIO-NUM-SEQ-MULT-000938
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What number comes next?  3, 8, 18, 38, 78, ___
A. 156
B. 118
C. 158
D. 160
MARKED ANSWER C. 158
WHY 158 is right: 78 × 2 = 156, then + 2 gives 158.
SHORTCUT Test "times 2, then + 2" on the first numbers: 3 × 2 + 2 = 8; 8 × 2 + 2 = 18. It works, so use it on 78.

### 938 | CIVIO-NUM-SEQ-DIFF-000939
TRACK both | DOMAIN numerical | SKILL Number sequence | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What number comes next in the series?  2, 3, 7, 14, 24, ___
A. 25
B. 34
C. 37
D. 40
MARKED ANSWER C. 37
WHY 37 is right: 24 + 13 = 37.
SHORTCUT Write the jumps under the list: +1, +4, +7, +10. Each jump is 3 more than the one before. So the next jump is +13.

### 939 | CIVIO-NUM-WP-PCT-CHANGE-000940
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A vendor borrows ₱18,000 at 12% simple interest per year. How much interest is due after 4 years and 6 months?
A. ₱9,936
B. ₱9,720
C. ₱27,720
D. ₱8,640
MARKED ANSWER B. ₱9,720
WHY ₱9,720 is right. Check: 18,000 × 0.12 × 4.5 = 9,720.
SHORTCUT Find one year first: 12% of ₱18,000 = ₱2,160. Time is 4.5 years. Multiply: 4.5 × ₱2,160 = ₱9,720.

### 940 | CIVIO-NUM-FRAC-DEC-000941
TRACK both | DOMAIN numerical | SKILL Word problems | DIFFICULTY hard | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
A barangay had 960 seedlings. It gave out 2/5 of them on Monday and 1/6 of the remaining seedlings on Tuesday. How many are left?
A. 416
B. 576
C. 480
D. 96
MARKED ANSWER C. 480
WHY 480 is right. Check: 384 + 96 + 480 = 960.
SHORTCUT Go day by day. Monday: 2/5 of 960 = 384, so 576 left. Tuesday: 1/6 of 576 = 96, so 576 − 96 = 480 left.

### 941 | CIVIO-ANA-DI-TABLE-000942
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Supply use of toner (units) by office (Health: Jul 38, Aug 54, Sep 62; Library: Jul 50, Aug 62, Sep 80; Engineering: Jul 18, Aug 56, Sep 80). How many did Engineering use in all three months?
A. 172
B. 74
C. 51.3
D. 154
MARKED ANSWER D. 154
WHY 154 is right: 18 + 56 + 80 = 154.
SHORTCUT Read across the Engineering row only: 18 + 56 + 80.

### 942 | CIVIO-ANA-DI-TABLE-000943
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Supply use of folders (packs) by office (HR: Jul 80, Aug 48, Sep 66; Library: Jul 70, Aug 76, Sep 28; Engineering: Jul 38, Aug 68, Sep 16). In Sep, how many more did HR use than Library?
A. 94
B. 38
C. 10
D. 20
MARKED ANSWER B. 38
WHY 38 is right: 66 − 28 = 38.
SHORTCUT Go to the Sep column: Library 28, HR 66. Subtract the smaller from the larger.

### 943 | CIVIO-ANA-DI-TABLE-000944
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Supply use of toner (units) by office (Health: Jul 58, Aug 56, Sep 52; Engineering: Jul 46, Aug 60, Sep 20; Library: Jul 74, Aug 66, Sep 80). In Sep, how many more did Health use than Engineering?
A. 72
B. 32
C. 12
D. 40
MARKED ANSWER B. 32
WHY 32 is right: 52 − 20 = 32.
SHORTCUT Go to the Sep column: Engineering 20, Health 52. Subtract the smaller from the larger.

### 944 | CIVIO-ANA-SYLLOGISM-000945
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Assume these are true: every one of the barangay captains is among the elected officials, and every one of the elected officials is among the public officers. What can be concluded for certain?
A. All barangay captains are public officers.
B. Some public officers are not elected officials.
C. All public officers are barangay captains.
D. No elected officials are barangay captains.
MARKED ANSWER A. All barangay captains are public officers.
WHY "All barangay captains are public officers." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: barangay captains inside elected officials, elected officials inside public officers. So barangay captains sit inside public officers.

### 945 | CIVIO-ANA-SYMBOL-SERIES-000946
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In a certain code, PUBLIC is written as QVCMJD. How is OFFICE written in the same code?
A. QHHKEG
B. NEEHBD
C. PGGJDF
D. PGGJDE
MARKED ANSWER C. PGGJDF
WHY PGGJDF is right: each letter of OFFICE moved 1 place forward.
SHORTCUT Compare the first letters: P became Q. That is 1 place forward. Check one more letter, then shift every letter of OFFICE the same way.

### 946 | CIVIO-ANA-SYMBOL-SERIES-000947
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In a certain code, PAPER is written as NYNCP. How is MEMO written in the same code?
A. KCKM
B. JBJL
C. OGOQ
D. KCKO
MARKED ANSWER A. KCKM
WHY KCKM is right: each letter of MEMO moved 2 places back.
SHORTCUT Compare the first letters: P became N. That is 2 places back. Check one more letter, then shift every letter of MEMO the same way.

### 947 | CIVIO-ANA-SYLLOGISM-000948
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
All volunteers are helpers. No helpers are job-order hires. Which conclusion must be true?
A. No volunteers are job-order hires.
B. Some volunteers are job-order hires.
C. All helpers are volunteers.
D. No registered persons are job-order hires.
MARKED ANSWER A. No volunteers are job-order hires.
WHY "No volunteers are job-order hires." is right. It follows from the two statements with no extra facts.
SHORTCUT Put the volunteers circle inside helpers. The "job-order hires" circle sits outside helpers, so it is outside volunteers too.

### 948 | CIVIO-ANA-SYLLOGISM-000949
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Assume these are true: a few of the teachers are union members, and all of the teachers are school staff. What can be concluded for certain?
A. All school staff are union members.
B. No school staff are union members.
C. All union members are teachers.
D. Some school staff are union members.
MARKED ANSWER D. Some school staff are union members.
WHY "Some school staff are union members." is right. It follows from the two statements with no extra facts.
SHORTCUT The teachers who are union members are also school staff. So at least some school staff are union members.

### 949 | CIVIO-ANA-SYMBOL-SERIES-000950
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What comes next in the series?  AP, EQ, IR, MS, ___
A. QF
B. QT
C. TQ
D. NT
MARKED ANSWER B. QT
WHY QT is right: M + 4 = Q and S + 1 = T.
SHORTCUT Split each pair. First letters: A, E, I, M (jump +4). Second letters: P, Q, R, S (jump +1). Move each one more step.

### 950 | CIVIO-ANA-CONCLUSION-000951
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Four staff members are compared. Arnel finished the report earlier than Mang Jun. Aling Rosa finished the report earlier than Marites. Marites finished the report earlier than Arnel. Who is second in the order (counting from the one who finished first)?
A. Mang Jun
B. Marites
C. Aling Rosa
D. Arnel
MARKED ANSWER B. Marites
WHY Marites is right. The clues give Aling Rosa → Marites → Arnel → Mang Jun, so Marites is second.
SHORTCUT Start from the person nobody beats and follow the clues down: Aling Rosa → Marites → Arnel → Mang Jun.

### 951 | CIVIO-ANA-SYMBOL-SERIES-000952
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In a certain code, CHAIR is written as DIBJS. How is PERMIT written in the same code?
A. QFSNJU
B. ODQLHS
C. QFSNJT
D. RGTOKV
MARKED ANSWER A. QFSNJU
WHY QFSNJU is right: each letter of PERMIT moved 1 place forward.
SHORTCUT Compare the first letters: C became D. That is 1 place forward. Check one more letter, then shift every letter of PERMIT the same way.

### 952 | CIVIO-ANA-DI-TABLE-000953
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Supply use of staplers by office (Health: Apr 58, May 38, Jun 60; Assessor: Apr 52, May 68, Jun 58; Engineering: Apr 12, May 62, Jun 56). In Jun, how many more did Health use than Assessor?
A. 118
B. 2
C. 22
D. 6
MARKED ANSWER B. 2
WHY 2 is right: 60 − 58 = 2.
SHORTCUT Go to the Jun column: Assessor 58, Health 60. Subtract the smaller from the larger.

### 953 | CIVIO-ANA-ANALOGY-FORM-000954
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Find the pair whose link matches the link between "frown" and "displeasure".
A. applause : approval
B. joy : laugh
C. smile : frown
D. face : mouth
MARKED ANSWER A. applause : approval
WHY "applause : approval" is right. It has the same link, sign : what it shows, in the same order.
SHORTCUT Make a sentence for the stem: "frown is to displeasure" as sign : what it shows. Test each choice in that sentence.

### 954 | CIVIO-ANA-SYMBOL-SERIES-000955
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In a certain code, SCHOOL is written as UEJQQN. How is RIVER written in the same code?
A. PGTCP
B. ULYHU
C. TKXGT
D. TKXGR
MARKED ANSWER C. TKXGT
WHY TKXGT is right: each letter of RIVER moved 2 places forward.
SHORTCUT Compare the first letters: S became U. That is 2 places forward. Check one more letter, then shift every letter of RIVER the same way.

### 955 | CIVIO-ANA-SYLLOGISM-000956
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Statement 1: All accountants are licensed workers. Statement 2: All auditors are accountants. Which conclusion follows from both statements?
A. All licensed workers are auditors.
B. All auditors are licensed workers.
C. No accountants are auditors.
D. Some licensed workers are not accountants.
MARKED ANSWER B. All auditors are licensed workers.
WHY "All auditors are licensed workers." is right. It follows from the two statements with no extra facts.
SHORTCUT Draw circles: auditors inside accountants, accountants inside licensed workers. So auditors sit inside licensed workers.

### 956 | CIVIO-ANA-SYMBOL-SERIES-000957
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In a certain code, BOARD is written as CPBSE. How is CENSUS written in the same code?
A. DFOTVT
B. BDMRTR
C. EGPUWU
D. DFOTVS
MARKED ANSWER A. DFOTVT
WHY DFOTVT is right: each letter of CENSUS moved 1 place forward.
SHORTCUT Compare the first letters: B became C. That is 1 place forward. Check one more letter, then shift every letter of CENSUS the same way.

### 957 | CIVIO-ANA-DI-TABLE-000958
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Supply use of staplers by office (Planning: Jan 66, Feb 62, Mar 44; HR: Jan 30, Feb 40, Mar 76; Assessor: Jan 66, Feb 66, Mar 72). How many did Planning use in all three months?
A. 128
B. 172
C. 57.3
D. 168
MARKED ANSWER B. 172
WHY 172 is right: 66 + 62 + 44 = 172.
SHORTCUT Read across the Planning row only: 66 + 62 + 44.

### 958 | CIVIO-ANA-SYMBOL-SERIES-000959
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What comes next in the series?  DN, HO, LP, PQ, ___
A. TR
B. TD
C. QR
D. RT
MARKED ANSWER A. TR
WHY TR is right: P + 4 = T and Q + 1 = R.
SHORTCUT Split each pair. First letters: D, H, L, P (jump +4). Second letters: N, O, P, Q (jump +1). Move each one more step.

### 959 | CIVIO-ANA-CONCLUSION-000960
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Four staff members are compared. Nonoy has served longer than Bong. Kimberly has served longer than Datu. Bong has served longer than Kimberly. Who is third in the order (counting from the one who has served the longest)?
A. Kimberly
B. Nonoy
C. Bong
D. Datu
MARKED ANSWER A. Kimberly
WHY Kimberly is right. The clues give Nonoy → Bong → Kimberly → Datu, so Kimberly is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Nonoy → Bong → Kimberly → Datu.

### 960 | CIVIO-ANA-DI-TABLE-000961
TRACK professional | DOMAIN analytical | SKILL Data interpretation | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Supply use of bond paper (reams) by office (Records: Jul 32, Aug 24, Sep 68; Cashier: Jul 78, Aug 42, Sep 16; HR: Jul 26, Aug 16, Sep 38). In Sep, how many more did Records use than Cashier?
A. 46
B. 12
C. 52
D. 84
MARKED ANSWER C. 52
WHY 52 is right: 68 − 16 = 52.
SHORTCUT Go to the Sep column: Records 68, Cashier 16. Subtract the smaller from the larger.

### 961 | CIVIO-ANA-SYMBOL-SERIES-000962
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What comes next in the series?  HN, JP, LR, NT, ___
A. PV
B. OV
C. VP
D. PW
MARKED ANSWER A. PV
WHY PV is right: N + 2 = P and T + 2 = V.
SHORTCUT Split each pair. First letters: H, J, L, N (jump +2). Second letters: N, P, R, T (jump +2). Move each one more step.

### 962 | CIVIO-ANA-ANALOGY-FUNCTION-000963
TRACK professional | DOMAIN analytical | SKILL Word association (analogy) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which pair shows the same relationship as "doctor : diagnosis"?
A. plan : engineer
B. architect : blueprint
C. nurse : doctor
D. patient : medicine
MARKED ANSWER B. architect : blueprint
WHY "architect : blueprint" is right. It has the same link, worker : what they produce, in the same order.
SHORTCUT Make a sentence for the stem: "doctor is to diagnosis" as worker : what they produce. Test each choice in that sentence.

### 963 | CIVIO-ANA-CONCLUSION-000964
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Four staff members are compared. Bong arrived earlier than Kimberly. Jomar arrived earlier than Bong. Inday arrived earlier than Jomar. Who is third in the order (counting from the one who arrived first)?
A. Jomar
B. Inday
C. Kimberly
D. Bong
MARKED ANSWER D. Bong
WHY Bong is right. The clues give Inday → Jomar → Bong → Kimberly, so Bong is third.
SHORTCUT Start from the person nobody beats and follow the clues down: Inday → Jomar → Bong → Kimberly.

### 964 | CIVIO-ANA-SYMBOL-SERIES-000965
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What comes next in the series?  GP, IR, KT, MV, ___
A. OY
B. NX
C. XO
D. OX
MARKED ANSWER D. OX
WHY OX is right: M + 2 = O and V + 2 = X.
SHORTCUT Split each pair. First letters: G, I, K, M (jump +2). Second letters: P, R, T, V (jump +2). Move each one more step.

### 965 | CIVIO-ANA-SYLLOGISM-000966
TRACK professional | DOMAIN analytical | SKILL Logic | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
All tilapia are fish. Some tilapia are second-hand goods. Which conclusion must be true?
A. All fish are second-hand goods.
B. No fish are second-hand goods.
C. All second-hand goods are tilapia.
D. Some fish are second-hand goods.
MARKED ANSWER D. Some fish are second-hand goods.
WHY "Some fish are second-hand goods." is right. It follows from the two statements with no extra facts.
SHORTCUT The tilapia who are second-hand goods are also fish. So at least some fish are second-hand goods.

### 966 | CIVIO-VEN-ERROR-AGREE-000967
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: The quality of the roads ____ improved this year.
A. has
B. having
C. to have
D. have
MARKED ANSWER A. has
WHY "has" is right: "The quality" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The quality ____". The subject is singular, so use the singular verb.

### 967 | CIVIO-VEN-SENT-COMP-WORD-000968
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: The forms were divided ____ the three clerks.
A. between
B. among
C. within
D. along
MARKED ANSWER B. among
WHY "among" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 968 | CIVIO-VEN-WORD-MEANING-000969
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is closest in meaning to the word in capital letters?  PUNCTUAL
A. practical
B. on time
C. late
D. punctured
MARKED ANSWER B. on time
WHY "on time" is right. "Punctual" means on time.
SHORTCUT Make a short sentence with "punctual", then swap in each choice. Watch for words that only look or sound like "punctual".

### 969 | CIVIO-VEN-WORD-MEANING-000970
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is closest in meaning to the word in capital letters?  FRUGAL
A. fruitful
B. wasteful
C. fragile
D. thrifty
MARKED ANSWER D. thrifty
WHY "thrifty" is right. "Frugal" means thrifty.
SHORTCUT Make a short sentence with "frugal", then swap in each choice. Watch for words that only look or sound like "frugal".

### 970 | CIVIO-VEN-SENT-COMP-WORD-000971
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: The office is responsible ____ the safekeeping of records.
A. on
B. of
C. for
D. to
MARKED ANSWER C. for
WHY "for" is right: it is the standard pairing in this sentence.
SHORTCUT Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).

### 971 | CIVIO-VEN-WORD-MEANING-000972
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  NEGLIGENT
A. negligible
B. attentive
C. negotiable
D. careless
MARKED ANSWER B. attentive
WHY "attentive" is right. "Negligent" means careless; "attentive" is the reverse.
SHORTCUT First say what "negligent" means (careless). Then look for the word that means the reverse.

### 972 | CIVIO-VEN-ERROR-AGREE-000973
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: Each of the new clerks ____ a copy of the office manual.
A. receiving
B. to receive
C. receive
D. receives
MARKED ANSWER D. receives
WHY "receives" is right: "Each" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "Each ____". The subject is singular, so use the singular verb.

### 973 | CIVIO-VEN-ERROR-TENSE-000974
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the correct verb: Last Friday, Aileen ____ the leave forms.
A. has reviewed
B. will have reviewed
C. will review
D. reviewed
MARKED ANSWER D. reviewed
WHY "reviewed" is right: the simple past matches "Last Friday".
SHORTCUT Find the time signal first: "Last Friday". It calls for the simple past.

### 974 | CIVIO-VEN-ERROR-TENSE-000975
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the correct verb: By the end of the year, Bea ____ the voters' list.
A. updated
B. has updated
C. is updating
D. will have updated
MARKED ANSWER D. will have updated
WHY "will have updated" is right: the future perfect matches "By the end of the year".
SHORTCUT Find the time signal first: "By the end of the year". It calls for the future perfect.

### 975 | CIVIO-VEN-ERROR-AGREE-000976
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: The results of the survey ____ posted online.
A. was
B. been
C. were
D. being
MARKED ANSWER C. were
WHY "were" is right: "The results" is plural.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The results ____". The subject is plural, so use the plural verb.

### 976 | CIVIO-VEN-SENT-COMP-WORD-000977
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: The new curfew had a strong ____ on street crime.
A. afect
B. affect
C. effect
D. effort
MARKED ANSWER C. effect
WHY "effect" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 977 | CIVIO-VEN-ERROR-TENSE-000978
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the correct verb: Next month, Jomar ____ the voters' list.
A. updated
B. has updated
C. will update
D. will have updated
MARKED ANSWER C. will update
WHY "will update" is right: the simple future matches "Next month".
SHORTCUT Find the time signal first: "Next month". It calls for the simple future.

### 978 | CIVIO-VEN-WORD-MEANING-000979
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is closest in meaning to the word in capital letters?  ACCURATE
A. correct
B. accustomed
C. wrong
D. adequate
MARKED ANSWER A. correct
WHY "correct" is right. "Accurate" means correct.
SHORTCUT Make a short sentence with "accurate", then swap in each choice. Watch for words that only look or sound like "accurate".

### 979 | CIVIO-VEN-ERROR-TENSE-000980
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY easy | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the correct verb: In 2019, Marites ____ the voters' list.
A. will have updated
B. has updated
C. updated
D. will update
MARKED ANSWER C. updated
WHY "updated" is right: the simple past matches "In 2019".
SHORTCUT Find the time signal first: "In 2019". It calls for the simple past.

### 980 | CIVIO-VEN-WORD-MEANING-000981
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  MEAGER
A. eager
B. plentiful
C. scanty
D. meaningful
MARKED ANSWER B. plentiful
WHY "plentiful" is right. "Meager" means scanty; "plentiful" is the reverse.
SHORTCUT First say what "meager" means (scanty). Then look for the word that means the reverse.

### 981 | CIVIO-VEN-SENT-COMP-WORD-000982
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: Only employees, ____ the guards, may enter after 6 p.m.
A. expect
B. excepting
C. accept
D. except
MARKED ANSWER D. except
WHY "except" is right. It has the meaning and the word form the sentence needs.
SHORTCUT Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.

### 982 | CIVIO-VEN-SENT-COMP-WORD-000983
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: Because of the ____ rains, the river overflowed.
A. heavily
B. light
C. heavy
D. heavenly
MARKED ANSWER C. heavy
WHY "heavy" is right: it fits the clue in the sentence and is the right word form.
SHORTCUT Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.

### 983 | CIVIO-VEN-ERROR-AGREE-000984
TRACK both | DOMAIN verbal_en | SKILL Grammar and correct usage | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Choose the word that best completes the sentence: The basket of mangoes ____ to the canteen.
A. belongs
B. to belong
C. belonging
D. belong
MARKED ANSWER A. belongs
WHY "belongs" is right: "The basket" is singular.
SHORTCUT Cover the phrase that starts with "of", "on" or "in". Read "The basket ____". The subject is singular, so use the singular verb.

### 984 | CIVIO-VEN-WORD-MEANING-000985
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is most nearly OPPOSITE in meaning to the word in capital letters?  IMMINENT
A. immense
B. eminent
C. about to happen
D. far off
MARKED ANSWER D. far off
WHY "far off" is right. "Imminent" means about to happen; "far off" is the reverse.
SHORTCUT First say what "imminent" means (about to happen). Then look for the word that means the reverse.

### 985 | CIVIO-VEN-RC-VOCAB-000986
TRACK both | DOMAIN verbal_en | SKILL Vocabulary | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In the sentence below, what does the word in capital letters most nearly mean?  The barangay will WAIVE the fee for senior citizens.
A. set aside
B. double
C. collect
D. wave
MARKED ANSWER A. set aside
WHY "set aside" is right: it is the sense of "waive" that fits the sentence.
SHORTCUT Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of "waive".

### 986 | CIVIO-CLR-FILE-POSITION-000987
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In alphabetical filing, which name is filed FIRST?  Alfredo D. San Pedro | Victoria G. Del Rosario | Engr. Ernesto S. De Leon | Ana E. Bautista
A. Victoria G. Del Rosario
B. Engr. Ernesto S. De Leon
C. Ana E. Bautista
D. Alfredo D. San Pedro
MARKED ANSWER C. Ana E. Bautista
WHY "Ana E. Bautista" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Ana E. Bautista → BAUTISTA, Ana; Engr. Ernesto S. De Leon → DELEON, Ernesto; Victoria G. Del Rosario → DELROSARIO, Victoria; Alfredo D. San Pedro → SANPEDRO, Alfredo.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 987 | CIVIO-CLR-FILE-POSITION-000988
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In alphabetical filing, which name is filed FIRST?  Dr. Liza F. Tan | Juan V. Dela Cruz | Corazon N. De Leon | Elena D. Leon
A. Elena D. Leon
B. Dr. Liza F. Tan
C. Corazon N. De Leon
D. Juan V. Dela Cruz
MARKED ANSWER D. Juan V. Dela Cruz
WHY "Juan V. Dela Cruz" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Juan V. Dela Cruz → DELACRUZ, Juan; Corazon N. De Leon → DELEON, Corazon; Elena D. Leon → LEON, Elena; Dr. Liza F. Tan → TAN, Liza.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 988 | CIVIO-CLR-SPELL-WRONG-000989
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is misspelled?  lieutenant | questonnaire | achievement | mischievous
A. lieutenant
B. questonnaire
C. achievement
D. mischievous
MARKED ANSWER B. questonnaire
WHY "questonnaire" is misspelled: it drops a letter. The correct spelling is "questionnaire".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 989 | CIVIO-CLR-SPELL-WRONG-000990
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is misspelled?  phenomenon | collague | acknowledgment | assessment
A. phenomenon
B. collague
C. acknowledgment
D. assessment
MARKED ANSWER B. collague
WHY "collague" is misspelled: it drops a letter. The correct spelling is "colleague".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 990 | CIVIO-CLR-FILE-POSITION-000991
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In alphabetical filing, which name is filed FIRST?  Corazon S. San Pedro | Dr. Rafael M. Santos-Ocampo | Ramon E. Garcia-Lopez | Maria L. Tan
A. Corazon S. San Pedro
B. Maria L. Tan
C. Ramon E. Garcia-Lopez
D. Dr. Rafael M. Santos-Ocampo
MARKED ANSWER C. Ramon E. Garcia-Lopez
WHY "Ramon E. Garcia-Lopez" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Ramon E. Garcia-Lopez → GARCIALOPEZ, Ramon; Corazon S. San Pedro → SANPEDRO, Corazon; Dr. Rafael M. Santos-Ocampo → SANTOSOCAMPO, Rafael; Maria L. Tan → TAN, Maria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 991 | CIVIO-CLR-SPELL-WRONG-000992
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is misspelled?  questionnaire | persnnel | jewelry | dilemma
A. questionnaire
B. persnnel
C. jewelry
D. dilemma
MARKED ANSWER B. persnnel
WHY "persnnel" is misspelled: it drops a letter. The correct spelling is "personnel".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 992 | CIVIO-CLR-FILE-POSITION-000993
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In alphabetical filing, which name is filed LAST?  Maria E. Del Rosario | Ernesto A. Dela Torre | Atty. Ramon R. Dizon | Engr. Mario L. San Juan
A. Atty. Ramon R. Dizon
B. Ernesto A. Dela Torre
C. Engr. Mario L. San Juan
D. Maria E. Del Rosario
MARKED ANSWER C. Engr. Mario L. San Juan
WHY "Engr. Mario L. San Juan" is right. It comes last when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Ernesto A. Dela Torre → DELATORRE, Ernesto; Maria E. Del Rosario → DELROSARIO, Maria; Atty. Ramon R. Dizon → DIZON, Ramon; Engr. Mario L. San Juan → SANJUAN, Mario.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 993 | CIVIO-CLR-SPELL-RIGHT-000994
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is spelled correctly?  parliamment | parlament | parliament | perliament
A. parliamment
B. parlament
C. parliament
D. perliament
MARKED ANSWER C. parliament
WHY "parliament" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 994 | CIVIO-CLR-FILE-POSITION-000995
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In alphabetical filing, which name is filed FIRST?  Maria L. Santos | Engr. Evelyn V. Pedro | Jose P. Castillo | Corazon M. Mendoza
A. Corazon M. Mendoza
B. Maria L. Santos
C. Jose P. Castillo
D. Engr. Evelyn V. Pedro
MARKED ANSWER C. Jose P. Castillo
WHY "Jose P. Castillo" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 5), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Jose P. Castillo → CASTILLO, Jose; Corazon M. Mendoza → MENDOZA, Corazon; Engr. Evelyn V. Pedro → PEDRO, Evelyn; Maria L. Santos → SANTOS, Maria.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 995 | CIVIO-CLR-SPELL-RIGHT-000996
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is spelled correctly?  schedule | shedule | schdule | schedulle
A. schedule
B. shedule
C. schdule
D. schedulle
MARKED ANSWER A. schedule
WHY "schedule" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 996 | CIVIO-CLR-SPELL-RIGHT-000997
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is spelled correctly?  foregn | foreign | foriegn | forreign
A. foregn
B. foreign
C. foriegn
D. forreign
MARKED ANSWER B. foreign
WHY "foreign" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 997 | CIVIO-CLR-SPELL-WRONG-000998
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is misspelled?  accessible | reciept | rhythm | omission
A. accessible
B. reciept
C. rhythm
D. omission
MARKED ANSWER B. reciept
WHY "reciept" is misspelled: it swaps the order of i and e. The correct spelling is "receipt".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 998 | CIVIO-CLR-SPELL-RIGHT-000999
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is spelled correctly?  miscelaneous | misellaneous | miscellaneous | miscellanous
A. miscelaneous
B. misellaneous
C. miscellaneous
D. miscellanous
MARKED ANSWER C. miscellaneous
WHY "miscellaneous" is the standard spelling.
SHORTCUT Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.

### 999 | CIVIO-CLR-SPELL-WRONG-001000
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which word is misspelled?  deceive | weird | recmmend | occurred
A. deceive
B. weird
C. recmmend
D. occurred
MARKED ANSWER C. recmmend
WHY "recmmend" is misspelled: it drops a letter. The correct spelling is "recommend".
SHORTCUT Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.

### 1000 | CIVIO-CLR-FILE-POSITION-001001
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In alphabetical filing, which name is filed FIRST?  Benito E. Rosario | Gloria D. De Guzman | Dr. Corazon V. Flores | Atty. Cristina A. Santos
A. Benito E. Rosario
B. Atty. Cristina A. Santos
C. Dr. Corazon V. Flores
D. Gloria D. De Guzman
MARKED ANSWER D. Gloria D. De Guzman
WHY "Gloria D. De Guzman" is right. It comes first when every name is indexed surname first, letter by letter. This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule 6), not a rule published by the CSC.
SHORTCUT Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: Gloria D. De Guzman → DEGUZMAN, Gloria; Dr. Corazon V. Flores → FLORES, Corazon; Benito E. Rosario → ROSARIO, Benito; Atty. Cristina A. Santos → SANTOS, Cristina.
LEGAL SOURCE https://webstore.ansi.org/standards/arma/ansiarma122005

### 1001 | CIVIO-GI-DEADLINE-NUMBER-001002
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
How long must a voter have resided in the place where he or she proposes to vote, immediately before the election?
A. At least 2 years
B. At least 1 year
C. At least 3 months
D. At least 6 months
MARKED ANSWER D. At least 6 months
WHY "At least 6 months" is right. Art. V, Sec. 1 says: "in the place wherein they propose to vote, for at least six months".
SHORTCUT Tie the fact to its section: Art. V, Sec. 1. Six months in the place; one year in the Philippines.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1002 | CIVIO-GI-TERM-MATCH-001003
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Under R.A. 6713, upholding the principle of public accountability and the supremacy of civilian authority over the military is which norm?
A. Political neutrality
B. Commitment to democracy
C. Professionalism
D. Nationalism and patriotism
MARKED ANSWER B. Commitment to democracy
WHY "Commitment to democracy" is right. R.A. 6713, Sec. 4(A) says: "Commitment to democracy".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 4(A). Sec. 4(A)(g).
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 1003 | CIVIO-GI-TERM-MATCH-001004
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Under the Bill of Rights, all persons shall have the right to what before all judicial, quasi-judicial, or administrative bodies?
A. Skip preliminary investigation
B. A speedy disposition of their cases
C. Choose their own judge
D. Free transportation to hearings
MARKED ANSWER B. A speedy disposition of their cases
WHY "A speedy disposition of their cases" is right. Art. III, Sec. 16 says: "the right to a speedy disposition of their cases before all judicial, quasi-judicial, or administrative bodies".
SHORTCUT Tie the fact to its section: Art. III, Sec. 16. Speedy disposition of cases.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1004 | CIVIO-GI-DEADLINE-NUMBER-001005
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
What is the minimum age to be appointed Ombudsman?
A. 45 years old
B. 40 years old
C. 30 years old
D. 35 years old
MARKED ANSWER B. 40 years old
WHY "40 years old" is right. Art. XI, Sec. 8 says: "at least forty years old".
SHORTCUT Tie the fact to its section: Art. XI, Sec. 8. The Ombudsman must be at least 40.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1005 | CIVIO-GI-TERM-MATCH-001006
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which are the three Constitutional Commissions under Article IX of the 1987 Constitution?
A. Commission on Elections, Ombudsman, and Commission on Audit
B. Civil Service Commission, Commission on Elections, and Commission on Audit
C. Civil Service Commission, Commission on Elections, and Commission on Appointments
D. Civil Service Commission, Commission on Human Rights, and Commission on Audit
MARKED ANSWER B. Civil Service Commission, Commission on Elections, and Commission on Audit
WHY "Civil Service Commission, Commission on Elections, and Commission on Audit" is right. Art. IX-A, Sec. 1 says: "The Constitutional Commissions, which shall be independent, are the Civil Service Commission, the Commission on Elections, and the Commission on Audit".
SHORTCUT Tie the fact to its section: Art. IX-A, Sec. 1. CSC, COMELEC and COA are the three.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1006 | CIVIO-GI-TERM-MATCH-001007
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Under R.A. 6713, may a public employee engage in a private practice of profession during incumbency?
A. Yes, if done on weekends
B. Only if authorized by the Constitution or law, and it does not conflict with official functions
C. Never, under any condition
D. Yes, with no limits
MARKED ANSWER B. Only if authorized by the Constitution or law, and it does not conflict with official functions
WHY "Only if authorized by the Constitution or law, and it does not conflict with official functions" is right. R.A. 6713, Sec. 7(b) says: "unless authorized by the Constitution or law, provided, that such practice will not conflict or tend to conflict with their official functions".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 7(b). Allowed only when authorized and with no conflict.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 1007 | CIVIO-GI-DEADLINE-NUMBER-001008
TRACK both | DOMAIN general_information | SKILL Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Under R.A. 6713, within how many days must an official resign from a private business after assuming office, when there is a conflict of interest?
A. 30 days
B. 60 days
C. 15 days
D. 90 days
MARKED ANSWER A. 30 days
WHY "30 days" is right. R.A. 6713, Sec. 9 says: "within thirty (30) days from his assumption of office".
SHORTCUT Tie the fact to its section: R.A. 6713, Sec. 9. Divest or resign within 30 days.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html

### 1008 | CIVIO-GI-DEADLINE-NUMBER-001009
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Under the 1987 Constitution, what is the minimum age to be elected Senator?
A. 40 years old
B. 25 years old
C. 30 years old
D. 35 years old
MARKED ANSWER D. 35 years old
WHY "35 years old" is right. Art. VI, Sec. 3 says: "at least thirty-five years of age".
SHORTCUT Tie the fact to its section: Art. VI, Sec. 3. A Senator must be at least 35 on election day.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1009 | CIVIO-GI-TERM-MATCH-001010
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
Which of these is a territorial and political subdivision named in Art. X, Sec. 1 of the 1987 Constitution?
A. Barangays
B. Puroks
C. Sitios
D. Congressional districts
MARKED ANSWER A. Barangays
WHY "Barangays" is right. Art. X, Sec. 1 says: "The territorial and political subdivisions of the Republic of the Philippines are the provinces, cities, municipalities, and barangays".
SHORTCUT Tie the fact to its section: Art. X, Sec. 1. Provinces, cities, municipalities and barangays.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1010 | CIVIO-GI-WHO-HOLDS-POWER-001011
TRACK both | DOMAIN general_information | SKILL Philippine Constitution | DIFFICULTY medium | LANGUAGE en | REVIEW approved/passed
ORIGIN docs/batches/batch-011.json
STEM
In whom is judicial power vested under the 1987 Constitution?
A. The Congress
B. One Supreme Court and such lower courts as may be established by law
C. The Ombudsman
D. The Department of Justice
MARKED ANSWER B. One Supreme Court and such lower courts as may be established by law
WHY "One Supreme Court and such lower courts as may be established by law" is right. Art. VIII, Sec. 1 says: "The judicial power shall be vested in one Supreme Court and in such lower courts as may be established by law".
SHORTCUT Tie the fact to its section: Art. VIII, Sec. 1. Judicial power is with the Supreme Court and the lower courts.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1011 | CIVIO-VFIL-20261013-0001
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Sa ulat, inilalarawan ang kawani bilang MASIGASIG sa pag-asikaso ng mga kahilingan.
A. masipag
B. marahas
C. malungkutin
D. pabaya
MARKED ANSWER A. masipag
WHY Kasingkahulugan ng masigasig ang masipag.

### 1012 | CIVIO-VFIL-20261013-0002
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Naging SALAT sa pondo ang programa matapos bawasan ang badyet.
A. kulang
B. sagana
C. malinaw
D. sikat
MARKED ANSWER A. kulang
WHY Ang salat sa pondo ay kulang sa salapi.

### 1013 | CIVIO-VFIL-20261013-0003
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Hiniling ng opisina ang isang PAYAK na paliwanag.
A. paligoy-ligoy
B. simple
C. masalimuot
D. mahaba
MARKED ANSWER B. simple
WHY Ang payak ay simple at madaling unawain.

### 1014 | CIVIO-VFIL-20261013-0004
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Nananatiling MAHINAHON ang tagapamagitan sa gitna ng pagtatalo.
A. maingay
B. padalos-dalos
C. marupok
D. kalmado
MARKED ANSWER D. kalmado
WHY Ang mahinahon ay kalmado at hindi bugso ng damdamin.

### 1015 | CIVIO-VFIL-20261013-0005
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
MASALIMUOT ang proseso dahil maraming kailangang sundin.
A. madali
B. maikli
C. komplikado
D. payak
MARKED ANSWER C. komplikado
WHY Ang masalimuot ay maraming bahagi o komplikasyon.

### 1016 | CIVIO-VFIL-20261013-0006
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
MAPANURI ang auditor bago pumirma sa ulat.
A. palaging magmadali
B. madaling maniwala
C. masusing magsuri
D. umiwas sa detalye
MARKED ANSWER C. masusing magsuri
WHY Ang mapanuri ay nag-iisip at nagsusuri nang mabuti.

### 1017 | CIVIO-VFIL-20261013-0007
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
May PAG-AALINLANGAN ang grupo sa hindi pa nasusuring datos.
A. pagmamadali
B. katiyakan
C. kasiyahan
D. pagdududa
MARKED ANSWER D. pagdududa
WHY Ang pag-aalinlangan ay pagdududa.

### 1018 | CIVIO-VFIL-20261013-0008
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
MAKABULUHAN ang mungkahi dahil tumutugon ito sa tunay na problema.
A. may saysay
B. paulit-ulit
C. maingay
D. walang kaugnayan
MARKED ANSWER A. may saysay
WHY Ang makabuluhan ay may saysay o kabuluhan.

### 1019 | CIVIO-VFIL-20261013-0009
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ipinahayag ng pinuno ang MARUBDOB niyang hangaring makatulong.
A. matindi
B. mababaw
C. malamig
D. walang pakialam
MARKED ANSWER A. matindi
WHY Ang marubdob na hangarin ay matindi at taos-puso.

### 1020 | CIVIO-VFIL-20261013-0010
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Nais ng pangkat ng WASTONG talaan bago mag-ulat.
A. hindi kumpleto
B. palihim
C. kulang
D. tama
MARKED ANSWER D. tama
WHY Ang wasto ay tama o nararapat.

### 1021 | CIVIO-VFIL-20261013-0011
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MATATAG sa pangungusap: Matatag ang tulay matapos ang pagkukumpuni?
A. matiyaga
B. marupok
C. matatagalan
D. matibay
MARKED ANSWER B. marupok
WHY Kasalungat ng matatag sa tibay ang marupok.

### 1022 | CIVIO-VFIL-20261013-0012
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng PANANDALIAN sa pangungusap: Panandalian lamang ang pagsasara?
A. pansamantala
B. pangmatagalan
C. sandali
D. mabilis
MARKED ANSWER B. pangmatagalan
WHY Kasalungat ng panandalian ang pangmatagalan.

### 1023 | CIVIO-VFIL-20261013-0013
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MASIGLA sa pangungusap: Masigla ang talakayan?
A. matamlay
B. masaya
C. aktibo
D. masigabo
MARKED ANSWER A. matamlay
WHY Ang matamlay ay kabaligtaran ng masigla.

### 1024 | CIVIO-VFIL-20261013-0014
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MADALAS sa pangungusap: Madalas siyang dumalo sa pulong?
A. paulit-ulit
B. lagi
C. bihira
D. palagi
MARKED ANSWER C. bihira
WHY Ang bihira ay hindi madalas mangyari.

### 1025 | CIVIO-VFIL-20261013-0015
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng LUBOS sa pangungusap: Lubos ang kanyang suporta?
A. taos-puso
B. ganap
C. bahagya
D. buo
MARKED ANSWER C. bahagya
WHY Ang bahagya ay hindi buo o lubos.

### 1026 | CIVIO-VFIL-20261013-0016
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MAINGAT sa pangungusap: Maingat niyang binasa ang dokumento?
A. padalos-dalos
B. mahinahon
C. masusi
D. mapanuri
MARKED ANSWER A. padalos-dalos
WHY Ang padalos-dalos ay walang sapat na pag-iingat.

### 1027 | CIVIO-VFIL-20261013-0017
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MALINAW sa pangungusap: Malinaw ang ibinigay na tagubilin?
A. tuwiran
B. tiyak
C. hayag
D. malabo
MARKED ANSWER D. malabo
WHY Ang malabo ay hindi malinaw.

### 1028 | CIVIO-VFIL-20261013-0018
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MATIYAGA sa pangungusap: Matiyaga niyang inayos ang mga rekord?
A. matatag
B. mainipin
C. matiisin
D. masipag
MARKED ANSWER B. mainipin
WHY Ang mainipin ay madaling mawalan ng tiyaga.

### 1029 | CIVIO-VFIL-20261013-0019
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng MATIBAY sa pangungusap: Matibay ang kahong pinaglagyan ng rekord?
A. marupok
B. matatag
C. matigas
D. matibay-tibay
MARKED ANSWER A. marupok
WHY Ang marupok ay madaling masira, kabaligtaran ng matibay.

### 1030 | CIVIO-VFIL-20261013-0020
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang KASALUNGAT ng TAHIMIK sa pangungusap: Tahimik ang silid-aklatan?
A. banayad
B. kalma
C. payapa
D. maingay
MARKED ANSWER D. maingay
WHY Ang maingay ay kabaligtaran ng tahimik.

### 1031 | CIVIO-VFIL-20261013-0021
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ang salitang PANGUNAHIN sa pariralang pangunahing layunin ay pinakamalapit sa:
A. hindi kailangan
B. pinakamahalaga
C. pinakamaliit
D. pinakahuli
MARKED ANSWER B. pinakamahalaga
WHY Ang pangunahin ay pinakamahalaga o una sa prayoridad.

### 1032 | CIVIO-VFIL-20261013-0022
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Kapag sinabi ng guro na MALAWAK ang saklaw ng aralin, ang ibig sabihin ay:
A. maraming bahagi
B. walang hangganan sa batas
C. napakaliit
D. walang paksa
MARKED ANSWER A. maraming bahagi
WHY Ang malawak na saklaw ay marami o sari-saring bahagi.

### 1033 | CIVIO-VFIL-20261013-0023
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ang KAPAKI-PAKINABANG na impormasyon ay:
A. walang pinagmulan
B. mahirap hanapin
C. laging mahaba
D. may praktikal na gamit
MARKED ANSWER D. may praktikal na gamit
WHY Kapaki-pakinabang ang impormasyong may gamit o pakinabang.

### 1034 | CIVIO-VFIL-20261013-0024
TRACK both | DOMAIN verbal_fil | SKILL Word meaning | DIFFICULTY easy | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Sa pangungusap na Sinuri ang datos nang MASUSI, ang masusi ay nangangahulugang:
A. pabaya
B. walang ayos
C. detalyado at maingat
D. pahapyaw
MARKED ANSWER C. detalyado at maingat
WHY Ang masusing pagsusuri ay detalyado at maingat.

### 1035 | CIVIO-VFIL-20261013-0025
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Upang maiwasan ang pagkalito, dapat _____ ang mga tagubilin bago magsimula ang gawain.
A. itago
B. kaligtaan
C. linawin
D. ipagpaliban
MARKED ANSWER C. linawin
WHY Ang linawin ay angkop dahil layunin ang pag-iwas sa pagkalito.

### 1036 | CIVIO-VFIL-20261013-0026
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Bagaman limitado ang oras, _____ ng pangkat ang pagsumite sa takdang araw.
A. iniwasan
B. ipinagwalang-bahala
C. nakalimutan
D. naipagtagumpay
MARKED ANSWER D. naipagtagumpay
WHY Naipagtagumpay ang akma sa positibong resulta sa kabila ng limitadong oras.

### 1037 | CIVIO-VFIL-20261013-0027
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Hindi tinanggap ang tala dahil _____ ang ilang mahahalagang detalye.
A. kulang
B. tumpak
C. masusi
D. ganap
MARKED ANSWER A. kulang
WHY Tumutukoy ang kulang sa nawawalang impormasyon.

### 1038 | CIVIO-VFIL-20261013-0028
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
_____ sa mga nakasaad na patakaran ang pagsusuri ng mga aplikasyon.
A. Alinsunod
B. Hiwalay
C. Salungat
D. Malayo
MARKED ANSWER A. Alinsunod
WHY Ang alinsunod ay nangangahulugang ayon sa patakaran.

### 1039 | CIVIO-VFIL-20261013-0029
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Naglatag ang opisina ng malinaw na iskedyul _____ malaman ng lahat ang kanilang tungkulin.
A. bagaman
B. samantala
C. upang
D. ngunit
MARKED ANSWER C. upang
WHY Ginagamit ang upang sa pagpapahayag ng layunin.

### 1040 | CIVIO-VFIL-20261013-0030
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Nagtanim ng mga puno ang mga residente _____ mabawasan ang init sa kanilang lugar.
A. dahil dito
B. gayunman
C. upang
D. subalit
MARKED ANSWER C. upang
WHY Ang pangalawang sugnay ay nagsasaad ng layunin.

### 1041 | CIVIO-VFIL-20261013-0031
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Maagang dumating ang mga boluntaryo; _____, natapos ang paghahanda bago dumating ang mga bisita.
A. sa kabila nito
B. bunga nito
C. sa halip
D. gayunman
MARKED ANSWER B. bunga nito
WHY Ang bunga nito ay nagpapakita ng naging resulta.

### 1042 | CIVIO-VFIL-20261013-0032
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
_____ malakas ang ulan, nagpatuloy ang serbisyong pangkalusugan.
A. Upang
B. Kahit
C. Dahil
D. Samakatuwid
MARKED ANSWER B. Kahit
WHY Ang kahit ay nagpapakita ng pagsalungat sa inaasahang epekto ng ulan.

### 1043 | CIVIO-VFIL-20261013-0033
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Pinag-aralan muna ang mga reklamo _____ gumawa ng pasiya.
A. sapagkat
B. dahil dito
C. samantala
D. bago
MARKED ANSWER D. bago
WHY Ang bago ang tamang pang-ugnay sa pagkakasunod ng dalawang gawain.

### 1044 | CIVIO-VFIL-20261013-0034
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Kailangan ng sapat na ebidensiya _____ makagawa ng makatarungang pasiya.
A. upang
B. kahit
C. ngunit
D. maliban
MARKED ANSWER A. upang
WHY Ang upang ay nagpapahayag ng layunin ng pagkalap ng ebidensiya.

### 1045 | CIVIO-VFIL-20261013-0035
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Mahalagang _____ ang natanggap na dokumento upang madaling mahanap sa susunod.
A. itapon
B. ibalewala
C. itala
D. itago nang walang rekord
MARKED ANSWER C. itala
WHY Ang pagtatala ay tumutulong sa maayos na paghahanap ng dokumento.

### 1046 | CIVIO-VFIL-20261013-0036
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Sinuri ang bilang ng mga nakatanggap ng serbisyo _____ ihambing ang resulta sa nakaraang buwan.
A. gayunman
B. subalit
C. bagaman
D. upang
MARKED ANSWER D. upang
WHY Ang upang ay nagpapakita ng dahilan o layunin ng pagsusuri.

### 1047 | CIVIO-VFIL-20261013-0037
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Hindi sapat ang mabilis na pagtugon kung _____ naman ang impormasyong ibinibigay.
A. mali
B. kumpleto
C. napapanahon
D. wasto
MARKED ANSWER A. mali
WHY Sinasalungat ng mali ang pagiging kapaki-pakinabang ng mabilis na tugon.

### 1048 | CIVIO-VFIL-20261013-0038
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
_____ sa maikling abiso, maagang nakahanda ang mga kawani.
A. Alinsunod
B. Sa kabila
C. Dahil
D. Kasama
MARKED ANSWER B. Sa kabila
WHY Ang sa kabila ay angkop sa hindi inaasahang paghahanda kahit maikli ang abiso.

### 1049 | CIVIO-VFIL-20261013-0039
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ang datos ay kailangang _____ bago gamitin sa opisyal na ulat.
A. hulaan
B. palitan nang basta-basta
C. burahin kaagad
D. beripikahin
MARKED ANSWER D. beripikahin
WHY Kailangang beripikahin o tiyakin ang kawastuhan ng datos.

### 1050 | CIVIO-VFIL-20261013-0040
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Iba-iba ang panukala, _____ iisa ang layunin ng mga kasapi.
A. upang
B. dahil
C. ngunit
D. kaya
MARKED ANSWER C. ngunit
WHY Ang ngunit ay nagpapakita ng pagkakaiba ng panukala at pagkakapareho ng layunin.

### 1051 | CIVIO-VFIL-20261013-0041
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Pinili ng lupon ang mungkahing _____ sa kanilang badyet.
A. akma
B. labis
C. wala
D. salungat
MARKED ANSWER A. akma
WHY Akma ang mungkahing naaayon sa takdang badyet.

### 1052 | CIVIO-VFIL-20261013-0042
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Nagbigay ang guro ng halimbawa _____ mas maunawaan ng mga mag-aaral ang aralin.
A. samantala
B. bagaman
C. ngunit
D. upang
MARKED ANSWER D. upang
WHY Ang upang ay angkop sa layunin ng pagbibigay ng halimbawa.

### 1053 | CIVIO-VFIL-20261013-0043
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
_____ ang lahat ng pahina ng dokumento bago ito pirmahan.
A. Itapon
B. Basahin
C. Takpan
D. Ipagwalang-bahala
MARKED ANSWER B. Basahin
WHY Ang basahin ay angkop upang masuri ang kabuuan bago pumirma.

### 1054 | CIVIO-VFIL-20261013-0044
TRACK both | DOMAIN verbal_fil | SKILL Sentence completion | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Naglaan ng karagdagang oras sa pagsasanay _____ dumami ang mga bagong kawani.
A. sa halip
B. dahil
C. gayunman
D. subalit
MARKED ANSWER B. dahil
WHY Ang dahil ay nagpapakita ng sanhi ng karagdagang pagsasanay.

### 1055 | CIVIO-VFIL-20261013-0045
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Piliin ang pangungusap na may wastong gamit ng ng at nang.
A. Nagsumite siya ng ulat ng maaga.
B. Nagsumite siya nang ulat ng maaga.
C. Nagsumite siya ng ulat nang maaga.
D. Nagsumite siya nang ulat nang maaga.
MARKED ANSWER C. Nagsumite siya ng ulat nang maaga.
WHY Ginagamit ang ng para sa layon na ulat at nang para sa paraan o oras na maaga.

### 1056 | CIVIO-VFIL-20261013-0046
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Piliin ang wastong pangungusap.
A. Bawat kawani ay may tungkuling dapat gampanan.
B. Bawat kawani ay may tungkuling dapat gampanan ng lahat nilang bawat isa.
C. Bawat kawani ay may tungkulin na dapat gampanan nila bawat isa.
D. Bawat kawani ay may mga tungkuling dapat gampanan nilang lahat.
MARKED ANSWER A. Bawat kawani ay may tungkuling dapat gampanan.
WHY Maikli, malinaw, at wastong pangungusap ang unang pagpipilian.

### 1057 | CIVIO-VFIL-20261013-0047
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang wastong pagsulat ng pangungusap?
A. Dahil umulan, ipinagpaliban ang palaro.
B. Dahil umulan ipinagpaliban ang palaro.
C. Dahil, umulan ipinagpaliban ang palaro.
D. Dahil umulan; ipinagpaliban ang palaro.
MARKED ANSWER A. Dahil umulan, ipinagpaliban ang palaro.
WHY Ang kuwit ay naghihiwalay sa panimulang sugnay na Dahil umulan.

### 1058 | CIVIO-VFIL-20261013-0048
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang wastong pangungusap?
A. Ang ulat ay sinuri muna ngunit bago inilathala.
B. Ang ulat ay sinuri muna bago inilathala.
C. Ang ulat ay sinuri muna sa bago inilathala.
D. Ang ulat ay sinuri muna habang bago inilathala.
MARKED ANSWER B. Ang ulat ay sinuri muna bago inilathala.
WHY Ang bago ay malinaw na nagpapakita ng pagkakasunod ng gawain.

### 1059 | CIVIO-VFIL-20261013-0049
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Piliin ang wastong gamit ng na at ng.
A. Maayos na naitala na kawani ang mga kahilingan.
B. Maayos ng naitala na kawani ang mga kahilingan.
C. Maayos ng naitala ng kawani ang mga kahilingan.
D. Maayos na naitala ng kawani ang mga kahilingan.
MARKED ANSWER D. Maayos na naitala ng kawani ang mga kahilingan.
WHY Na ang pang-ugnay pagkatapos ng maayos at ng ang pananda sa kawani.

### 1060 | CIVIO-VFIL-20261013-0050
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang may pinakamalinaw na pagkakabuo?
A. Ipinadala ang paalala ng kahapon sa opisina ng mga aplikante.
B. Mga aplikante kahapon ipinadala sa paalala ang opisina.
C. Ipinadala ng opisina ang paalala sa mga aplikante kahapon.
D. Kahapon sa paalala ay ipinadala ng opisina ang mga aplikante.
MARKED ANSWER C. Ipinadala ng opisina ang paalala sa mga aplikante kahapon.
WHY Malinaw ang simuno, pandiwa, at layon sa unang pangungusap.

### 1061 | CIVIO-VFIL-20261013-0051
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang wastong pangungusap na nagsasaad ng layunin?
A. Nagsagawa ng pagsasanay gayunman mapabuti ang serbisyo.
B. Nagsagawa ng pagsasanay ngunit mapabuti ang serbisyo.
C. Nagsagawa ng pagsasanay upang mapabuti ang serbisyo.
D. Nagsagawa ng pagsasanay samantala mapabuti ang serbisyo.
MARKED ANSWER C. Nagsagawa ng pagsasanay upang mapabuti ang serbisyo.
WHY Ang upang ang tamang pang-ugnay para sa layunin.

### 1062 | CIVIO-VFIL-20261013-0052
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang pangungusap na may wastong paghahambing?
A. Mas mahaba ang pila ngayon kaysa sa noon kahapon bukas.
B. Mas mahaba ang pila ngayon pero kaysa kahapon.
C. Mas mahaba ang pila ngayon ng kahapon.
D. Mas mahaba ang pila ngayon kaysa kahapon.
MARKED ANSWER D. Mas mahaba ang pila ngayon kaysa kahapon.
WHY Kaysa ang karaniwang panandang panghambing.

### 1063 | CIVIO-VFIL-20261013-0053
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Piliin ang pangungusap na may wastong gamit ng mayroon.
A. Mayroon ng kaming sapat na upuan para sa mga bisita.
B. Mayroon kaming sapat na upuan para sa mga bisita.
C. Mayroon kaming sa sapat na upuan ng mga bisita.
D. Mayroon kami sapat na upuan sa mga bisita.
MARKED ANSWER B. Mayroon kaming sapat na upuan para sa mga bisita.
WHY Ang mayroon kaming ay wastong anyo sa pangungusap.

### 1064 | CIVIO-VFIL-20261013-0054
TRACK both | DOMAIN verbal_fil | SKILL Sentence structure | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Alin ang pangungusap na may malinaw na sanhi at bunga?
A. Nasira ang tubo ngunit pansamantalang nawalan ng tubig kaya.
B. Nasira ang tubo kaya pansamantalang nawalan ng tubig.
C. Nasira ang tubo upang pansamantalang nawalan ng tubig.
D. Nasira ang tubo samantala kaya nawalan ng tubig.
MARKED ANSWER B. Nasira ang tubo kaya pansamantalang nawalan ng tubig.
WHY Ang kaya ay nag-uugnay ng sanhi at bunga.

### 1065 | CIVIO-VFIL-20261013-0055
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Sa isang barangay, naglagay ng kahon para sa mga lumang baterya sa tabi ng tanggapan. Tuwing Biyernes, kinukuha ito ng awtorisadong tagapangalap. Ipinaliwanag ng mga opisyal na hindi dapat ihalo ang mga baterya sa karaniwang basura dahil may mga sangkap itong maaaring makapinsala.

Tanong: Ano ang pangunahing layunin ng kahon?
A. Mag-imbak ng pagkain
B. Mangalap ng donasyong pera
C. Magsilbing dekorasyon
D. Maghiwalay ng lumang baterya mula sa karaniwang basura
MARKED ANSWER D. Maghiwalay ng lumang baterya mula sa karaniwang basura
WHY Itinatabi ang lumang baterya upang hindi mahalo sa karaniwang basura.

### 1066 | CIVIO-VFIL-20261013-0056
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Sa isang barangay, naglagay ng kahon para sa mga lumang baterya sa tabi ng tanggapan. Tuwing Biyernes, kinukuha ito ng awtorisadong tagapangalap. Ipinaliwanag ng mga opisyal na hindi dapat ihalo ang mga baterya sa karaniwang basura dahil may mga sangkap itong maaaring makapinsala.

Tanong: Kailan kinukuha ang mga baterya?
A. Tuwing Biyernes
B. Isang beses sa isang taon
C. Araw-araw
D. Tuwing Lunes
MARKED ANSWER A. Tuwing Biyernes
WHY Tuwirang nakasaad ang Biyernes.

### 1067 | CIVIO-VFIL-20261013-0057
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Sa isang barangay, naglagay ng kahon para sa mga lumang baterya sa tabi ng tanggapan. Tuwing Biyernes, kinukuha ito ng awtorisadong tagapangalap. Ipinaliwanag ng mga opisyal na hindi dapat ihalo ang mga baterya sa karaniwang basura dahil may mga sangkap itong maaaring makapinsala.

Tanong: Bakit hindi dapat ihalo ang baterya sa ordinaryong basura?
A. Maaaring makapinsala ang ilang sangkap nito
B. Mas mahal itong itapon kapag magkahiwalay
C. Mas magaan ang karaniwang basura
D. Lahat ng baterya ay nabubulok
MARKED ANSWER A. Maaaring makapinsala ang ilang sangkap nito
WHY May binanggit na mga sangkap na maaaring makapinsala.

### 1068 | CIVIO-VFIL-20261013-0058
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Sa isang barangay, naglagay ng kahon para sa mga lumang baterya sa tabi ng tanggapan. Tuwing Biyernes, kinukuha ito ng awtorisadong tagapangalap. Ipinaliwanag ng mga opisyal na hindi dapat ihalo ang mga baterya sa karaniwang basura dahil may mga sangkap itong maaaring makapinsala.

Tanong: Alin ang hindi binanggit sa talata?
A. Ang uri ng basurang ihihiwalay
B. Ang lokasyon ng kahon
C. Ang araw ng koleksiyon
D. Ang kabuuang timbang ng nakolektang baterya
MARKED ANSWER D. Ang kabuuang timbang ng nakolektang baterya
WHY Walang numerong nagsasabi ng timbang sa talata.

### 1069 | CIVIO-VFIL-20261013-0059
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagbukas ang munisipyo ng dagdag na pila para sa matatanda at mga taong may kapansanan. Sa unang linggo, mas umikli ang paghihintay ng mga kabilang sa grupong ito. Gayunman, sinusukat pa ng opisina kung nakatulong din ang pagbabago sa kabuuang daloy ng mga aplikante.

Tanong: Ano ang ginawa ng munisipyo?
A. Nagbukas ng dagdag na pila para sa ilang aplikante
B. Kinansela ang lahat ng aplikasyon
C. Nagtaas agad ng bayarin
D. Isinara ang lahat ng tanggapan
MARKED ANSWER A. Nagbukas ng dagdag na pila para sa ilang aplikante
WHY Dagdag na pila ang pangunahing pagbabago.

### 1070 | CIVIO-VFIL-20261013-0060
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagbukas ang munisipyo ng dagdag na pila para sa matatanda at mga taong may kapansanan. Sa unang linggo, mas umikli ang paghihintay ng mga kabilang sa grupong ito. Gayunman, sinusukat pa ng opisina kung nakatulong din ang pagbabago sa kabuuang daloy ng mga aplikante.

Tanong: Ano ang naobserbahan sa unang linggo?
A. Bumaba ang lahat ng bayarin
B. Nawala ang lahat ng pila
C. Mas umikli ang paghihintay ng partikular na grupo
D. Dumoble ang bilang ng kawani
MARKED ANSWER C. Mas umikli ang paghihintay ng partikular na grupo
WHY Mas maikli ang paghihintay para sa inilaanang grupo.

### 1071 | CIVIO-VFIL-20261013-0061
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagbukas ang munisipyo ng dagdag na pila para sa matatanda at mga taong may kapansanan. Sa unang linggo, mas umikli ang paghihintay ng mga kabilang sa grupong ito. Gayunman, sinusukat pa ng opisina kung nakatulong din ang pagbabago sa kabuuang daloy ng mga aplikante.

Tanong: Bakit patuloy pa rin ang pagsukat ng opisina?
A. Hindi nagbukas ang dagdag na pila
B. Walang dumating na aplikante
C. Hindi pa tiyak ang epekto sa kabuuang daloy
D. Ipinagbawal ang pagtatala
MARKED ANSWER C. Hindi pa tiyak ang epekto sa kabuuang daloy
WHY Inaalam pa nila ang pangkalahatang epekto.

### 1072 | CIVIO-VFIL-20261013-0062
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagbukas ang munisipyo ng dagdag na pila para sa matatanda at mga taong may kapansanan. Sa unang linggo, mas umikli ang paghihintay ng mga kabilang sa grupong ito. Gayunman, sinusukat pa ng opisina kung nakatulong din ang pagbabago sa kabuuang daloy ng mga aplikante.

Tanong: Aling konklusyon ang HINDI pa suportado ng talata?
A. Patuloy ang pagsusuri ng opisina
B. Bumilis na ang serbisyo para sa lahat ng aplikante
C. May nasukat na pagbabago sa unang linggo
D. May bagong pila para sa ilang aplikante
MARKED ANSWER B. Bumilis na ang serbisyo para sa lahat ng aplikante
WHY Walang patunay na ang lahat ng aplikante ay mas mabilis nang napagsilbihan.

### 1073 | CIVIO-VFIL-20261013-0063
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagplano ang paaralan ng reading corner sa lumang silid. Nag-ambag ng mga aklat ang mga magulang at inayos ng mga guro ang mga estante. Bago ito buksan, sinuri ng tagapangasiwa kung ligtas ang mga upuan at maayos ang bentilasyon. Itinakda ang pagbubukas sa susunod na buwan.

Tanong: Ano ang pangunahing proyekto?
A. Pagtatayo ng bagong palaruan
B. Paggawa ng reading corner
C. Pagbili ng mga sasakyan
D. Pagpapalit ng lahat ng silid-aralan
MARKED ANSWER B. Paggawa ng reading corner
WHY Reading corner ang paksa ng buong talata.

### 1074 | CIVIO-VFIL-20261013-0064
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagplano ang paaralan ng reading corner sa lumang silid. Nag-ambag ng mga aklat ang mga magulang at inayos ng mga guro ang mga estante. Bago ito buksan, sinuri ng tagapangasiwa kung ligtas ang mga upuan at maayos ang bentilasyon. Itinakda ang pagbubukas sa susunod na buwan.

Tanong: Sino ang nag-ayos ng mga estante?
A. Mga guro
B. Mga magulang
C. Mga mag-aaral
D. Mga bisita
MARKED ANSWER A. Mga guro
WHY Nabanggit na inayos ng mga guro ang estante.

### 1075 | CIVIO-VFIL-20261013-0065
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagplano ang paaralan ng reading corner sa lumang silid. Nag-ambag ng mga aklat ang mga magulang at inayos ng mga guro ang mga estante. Bago ito buksan, sinuri ng tagapangasiwa kung ligtas ang mga upuan at maayos ang bentilasyon. Itinakda ang pagbubukas sa susunod na buwan.

Tanong: Ano ang ginawa bago ang pagbubukas?
A. Inilipat ang paaralan
B. Giniba ang silid
C. Ipinagbili ang mga aklat
D. Sinuri ang kaligtasan at bentilasyon
MARKED ANSWER D. Sinuri ang kaligtasan at bentilasyon
WHY Kaligtasan ng upuan at bentilasyon ang sinuri.

### 1076 | CIVIO-VFIL-20261013-0066
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Nagplano ang paaralan ng reading corner sa lumang silid. Nag-ambag ng mga aklat ang mga magulang at inayos ng mga guro ang mga estante. Bago ito buksan, sinuri ng tagapangasiwa kung ligtas ang mga upuan at maayos ang bentilasyon. Itinakda ang pagbubukas sa susunod na buwan.

Tanong: Kailan inaasahang buksan ang reading corner?
A. Walang itinakdang panahon
B. Ngayong araw
C. Sa susunod na buwan
D. Noong nakaraang taon
MARKED ANSWER C. Sa susunod na buwan
WHY Itinakda ang pagbubukas sa susunod na buwan.

### 1077 | CIVIO-VFIL-20261013-0067
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Upang mabawasan ang mga maling impormasyon sa isang tanggapan, gumawa ang pangkat ng iisang talaan para sa mga anunsiyo. Isang itinalagang kawani lamang ang maaaring magpalit ng opisyal na bersiyon. Maaari pa ring magmungkahi ang lahat, ngunit sinusuri muna ang mungkahi bago ito ilathala.

Tanong: Ano ang layunin ng iisang talaan?
A. Mabawasan ang maling impormasyon
B. Maitago ang lahat ng anunsiyo
C. Madagdagan ang magkakaibang bersiyon
D. Matanggal ang bawat mungkahi
MARKED ANSWER A. Mabawasan ang maling impormasyon
WHY Ang iisang talaan ay ginawa upang mabawasan ang maling impormasyon.

### 1078 | CIVIO-VFIL-20261013-0068
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Upang mabawasan ang mga maling impormasyon sa isang tanggapan, gumawa ang pangkat ng iisang talaan para sa mga anunsiyo. Isang itinalagang kawani lamang ang maaaring magpalit ng opisyal na bersiyon. Maaari pa ring magmungkahi ang lahat, ngunit sinusuri muna ang mungkahi bago ito ilathala.

Tanong: Sino ang maaaring magpalit ng opisyal na bersiyon?
A. Tanging dating empleyado
B. Sinumang bisita
C. Lahat nang walang pagsusuri
D. Isang itinalagang kawani
MARKED ANSWER D. Isang itinalagang kawani
WHY Iisa lamang na itinalagang kawani ang may kapangyarihan.

### 1079 | CIVIO-VFIL-20261013-0069
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Upang mabawasan ang mga maling impormasyon sa isang tanggapan, gumawa ang pangkat ng iisang talaan para sa mga anunsiyo. Isang itinalagang kawani lamang ang maaaring magpalit ng opisyal na bersiyon. Maaari pa ring magmungkahi ang lahat, ngunit sinusuri muna ang mungkahi bago ito ilathala.

Tanong: Ano ang nangyayari sa mga mungkahi?
A. Hindi kailanman tinatanggap
B. Agad itinatapon
C. Sinusuri muna bago ilathala
D. Awtomatikong nilalathala
MARKED ANSWER C. Sinusuri muna bago ilathala
WHY Pinapayagan ang mungkahi ngunit sinusuri muna.

### 1080 | CIVIO-VFIL-20261013-0070
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Upang mabawasan ang mga maling impormasyon sa isang tanggapan, gumawa ang pangkat ng iisang talaan para sa mga anunsiyo. Isang itinalagang kawani lamang ang maaaring magpalit ng opisyal na bersiyon. Maaari pa ring magmungkahi ang lahat, ngunit sinusuri muna ang mungkahi bago ito ilathala.

Tanong: Aling gawain ang salungat sa proseso?
A. Pagbabago ng opisyal na bersiyon ng sinumang kawani
B. Pagsusuri sa mungkahi
C. Pagtatalaga ng responsable sa bersiyon
D. Paggamit ng iisang talaan
MARKED ANSWER A. Pagbabago ng opisyal na bersiyon ng sinumang kawani
WHY Hindi lahat ng kawani ang maaaring magpalit ng opisyal na bersiyon.

### 1081 | CIVIO-VFIL-20261013-0071
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Tuwing umaga, binibilang ng kooperatiba ang natitirang ani bago magtakda ng dami ng ibebenta. Kapag may sobra, inuuna nilang ibigay ito sa mga kasaping may naunang order. Hindi nila agad binabaan ang presyo sapagkat maaari pang may dumating na karagdagang kahilingan sa hapon.

Tanong: Ano ang unang ginagawa tuwing umaga?
A. Kinakansela ang mga order
B. Isinasara ang pamilihan
C. Binabaan agad ang presyo
D. Binibilang ang natitirang ani
MARKED ANSWER D. Binibilang ang natitirang ani
WHY Pagbibilang ng ani ang unang hakbang.

### 1082 | CIVIO-VFIL-20261013-0072
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Tuwing umaga, binibilang ng kooperatiba ang natitirang ani bago magtakda ng dami ng ibebenta. Kapag may sobra, inuuna nilang ibigay ito sa mga kasaping may naunang order. Hindi nila agad binabaan ang presyo sapagkat maaari pang may dumating na karagdagang kahilingan sa hapon.

Tanong: Sino ang inuuna kapag may sobrang ani?
A. Mga mamimiling walang tala
B. Mga kasaping may naunang order
C. Mga hindi pa nag-oorder
D. Mga kasaping nahuling umorder
MARKED ANSWER B. Mga kasaping may naunang order
WHY Mga kasaping may naunang order ang inuuna.

### 1083 | CIVIO-VFIL-20261013-0073
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Tuwing umaga, binibilang ng kooperatiba ang natitirang ani bago magtakda ng dami ng ibebenta. Kapag may sobra, inuuna nilang ibigay ito sa mga kasaping may naunang order. Hindi nila agad binabaan ang presyo sapagkat maaari pang may dumating na karagdagang kahilingan sa hapon.

Tanong: Bakit hindi agad ibinababa ang presyo?
A. Hindi nila binibilang ang ani
B. Maaaring may bagong kahilingan sa hapon
C. Walang ani sa umaga
D. Ipinagbawal ang pagtitinda
MARKED ANSWER B. Maaaring may bagong kahilingan sa hapon
WHY Posibleng madagdagan ang demand sa hapon.

### 1084 | CIVIO-VFIL-20261013-0074
TRACK both | DOMAIN verbal_fil | SKILL Reading comprehension | DIFFICULTY medium | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Basahin ang talata:
Tuwing umaga, binibilang ng kooperatiba ang natitirang ani bago magtakda ng dami ng ibebenta. Kapag may sobra, inuuna nilang ibigay ito sa mga kasaping may naunang order. Hindi nila agad binabaan ang presyo sapagkat maaari pang may dumating na karagdagang kahilingan sa hapon.

Tanong: Ano ang pinakamainam na paglalarawan sa proseso?
A. Awtomatikong inuubos lahat ng ani
B. Laging pareho ang dami ng ibinebenta
C. Walang sinusunod na prayoridad
D. Nakasalalay sa tala ng ani at order ang pasiya
MARKED ANSWER D. Nakasalalay sa tala ng ani at order ang pasiya
WHY Binibilang ang ani at inuuna ang dating order bago magpasya.

### 1085 | CIVIO-VFIL-20261013-0075
TRACK both | DOMAIN verbal_fil | SKILL Paragraph organization | DIFFICULTY hard | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ayusin ang mga pangungusap upang maging malinaw ang daloy.
1. Unang itinakda ng grupo ang layunin ng proyekto.
2. Pagkatapos ay inilista nila ang mga kailangang kagamitan.
3. Nang makumpleto ang listahan, nagsimula ang pagbili.
4. Sa huli, sinuri nila ang mga resibo.
Alin ang wastong pagkakasunod?
A. 2-1-3-4
B. 1-2-3-4
C. 4-1-2-3
D. 2-3-1-4
MARKED ANSWER B. 1-2-3-4
WHY Nagsisimula sa layunin, sinusundan ng listahan, pagbili at pagsusuri.

### 1086 | CIVIO-VFIL-20261013-0076
TRACK both | DOMAIN verbal_fil | SKILL Paragraph organization | DIFFICULTY hard | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ayusin ang mga pangungusap upang maging malinaw ang daloy.
1. Nakatanggap ang opisina ng bagong reklamo.
2. Itinala muna ang mahahalagang detalye nito.
3. Pagkatapos ay ipinasa ang tala sa kaukulang yunit.
4. Sa wakas, ipinaalam sa nagreklamo ang susunod na hakbang.
Alin ang wastong pagkakasunod?
A. 4-1-2-3
B. 1-3-2-4
C. 1-2-3-4
D. 2-3-1-4
MARKED ANSWER C. 1-2-3-4
WHY Magkakasunod ang pagtanggap, pagtatala, pagpapasa at pagtugon.

### 1087 | CIVIO-VFIL-20261013-0077
TRACK both | DOMAIN verbal_fil | SKILL Paragraph organization | DIFFICULTY hard | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ayusin ang mga pangungusap upang maging malinaw ang daloy.
1. Nagpasya ang paaralan na magtanim ng mga gulay.
2. Pinili nila ang bakanteng bahagi ng bakuran.
3. Inihanda ng mga mag-aaral ang lupa at mga punla.
4. Pagkaraan ng ilang linggo, inani nila ang mga gulay.
Alin ang wastong pagkakasunod?
A. 4-1-2-3
B. 1-2-4-3
C. 1-2-3-4
D. 2-3-1-4
MARKED ANSWER C. 1-2-3-4
WHY Ang pasiya at pagpili ng lugar ay nauuna sa pagtatanim at pag-aani.

### 1088 | CIVIO-VFIL-20261013-0078
TRACK both | DOMAIN verbal_fil | SKILL Paragraph organization | DIFFICULTY hard | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ayusin ang mga pangungusap upang maging malinaw ang daloy.
1. May napansing tagas sa silid-aklatan.
2. Agad na iniulat ito sa tagapangasiwa.
3. Sinuri ng tagapag-ayos ang tubo at inayos ang sira.
4. Matapos ang pagkukumpuni, muling binuksan ang silid.
Alin ang wastong pagkakasunod?
A. 2-3-1-4
B. 4-1-2-3
C. 1-2-3-4
D. 3-1-2-4
MARKED ANSWER C. 1-2-3-4
WHY Tamang panahon ang pagkatuklas, pag-uulat, pagkukumpuni at pagbubukas.

### 1089 | CIVIO-VFIL-20261013-0079
TRACK both | DOMAIN verbal_fil | SKILL Paragraph organization | DIFFICULTY hard | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ayusin ang mga pangungusap upang maging malinaw ang daloy.
1. Nalaman ng pangkat na kulang ang mga datos.
2. Humingi sila ng karagdagang tala mula sa iba pang yunit.
3. Pinagsama at sinuri nila ang mga natanggap na datos.
4. Doon lamang nila isinulat ang pinal na ulat.
Alin ang wastong pagkakasunod?
A. 4-1-2-3
B. 1-2-3-4
C. 2-3-1-4
D. 2-1-3-4
MARKED ANSWER B. 1-2-3-4
WHY Kailangang makumpleto at masuri ang datos bago magsulat ng pinal na ulat.

### 1090 | CIVIO-VFIL-20261013-0080
TRACK both | DOMAIN verbal_fil | SKILL Paragraph organization | DIFFICULTY hard | LANGUAGE fil | REVIEW draft/unreviewed
ORIGIN docs/research/filipino-supplement-001.json
STEM
Ayusin ang mga pangungusap upang maging malinaw ang daloy.
1. Nag-anunsiyo ang barangay ng libreng seminar.
2. Nagparehistro ang mga nais dumalo.
3. Sa araw ng seminar, pinatunayan ang pagdalo ng mga kalahok.
4. Pagkatapos, nangalap ng puna ang mga tagapag-ayos.
Alin ang wastong pagkakasunod?
A. 4-1-2-3
B. 1-2-3-4
C. 2-3-1-4
D. 1-3-2-4
MARKED ANSWER B. 1-2-3-4
WHY Sunod-sunod ang anunsiyo, rehistrasyon, pagdalo at feedback.

### 1091 | CIVIO-GI-20261013-0001
TRACK both | DOMAIN general_information | SKILL Solid waste | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A local council wants a law specifically governing ecological solid waste management. Which law should it consult?
A. R.A. 9275
B. R.A. 9147
C. R.A. 8749
D. R.A. 9003
MARKED ANSWER D. R.A. 9003
WHY R.A. 9003 is the Ecological Solid Waste Management Act of 2000.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html

### 1092 | CIVIO-GI-20261013-0002
TRACK both | DOMAIN general_information | SKILL Source segregation | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Under R.A. 9003, what does segregation at source chiefly require?
A. Burying reusable materials with residual waste
B. Mixing compostable and hazardous wastes
C. Separating kinds of waste where they are generated
D. Combining all wastes before collection
MARKED ANSWER C. Separating kinds of waste where they are generated
WHY Source segregation means separating waste at the place where it is generated.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html

### 1093 | CIVIO-GI-20261013-0003
TRACK both | DOMAIN general_information | SKILL Composting | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which action best illustrates composting as described in R.A. 9003?
A. Burning discarded plastics in an open lot
B. Allowing organic scraps to decompose under controlled conditions
C. Dumping mixed waste into a creek
D. Mixing batteries with food scraps
MARKED ANSWER B. Allowing organic scraps to decompose under controlled conditions
WHY Composting uses controlled biological decomposition of organic materials.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html

### 1094 | CIVIO-GI-20261013-0004
TRACK both | DOMAIN general_information | SKILL Waste minimization | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A barangay encourages residents to reuse containers before discarding them. Which R.A. 9003 principle does this practice support?
A. Waste avoidance and resource conservation
B. Discharging untreated wastewater
C. Increased disposal without sorting
D. Unrestricted burning of waste
MARKED ANSWER A. Waste avoidance and resource conservation
WHY Reuse supports reducing waste and recovering useful resources.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html

### 1095 | CIVIO-GI-20261013-0005
TRACK both | DOMAIN general_information | SKILL Government responsibility | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Under R.A. 9003, which level of government retains primary responsibility for implementing solid waste management?
A. Foreign embassies
B. International courts
C. Private advertising agencies
D. Local government units
MARKED ANSWER D. Local government units
WHY R.A. 9003 assigns primary responsibility to local government units.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html

### 1096 | CIVIO-GI-20261013-0006
TRACK both | DOMAIN general_information | SKILL Clean Air Act | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A citizen asks which Philippine statute mainly addresses air pollution control. Which is correct?
A. R.A. 8749
B. R.A. 9147
C. R.A. 9275
D. R.A. 9003
MARKED ANSWER A. R.A. 8749
WHY R.A. 8749 is the Philippine Clean Air Act of 1999.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html

### 1097 | CIVIO-GI-20261013-0007
TRACK both | DOMAIN general_information | SKILL Air pollution | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A factory releases soot that degrades air quality. Which environmental problem is most directly involved?
A. Groundwater over-extraction
B. Air pollution
C. Coastal erosion
D. Loss of topsoil fertility only
MARKED ANSWER B. Air pollution
WHY Soot released to the atmosphere is relevant to air pollution under the Clean Air Act.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html

### 1098 | CIVIO-GI-20261013-0008
TRACK both | DOMAIN general_information | SKILL Polluter pays | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which principle recognized in the Philippine Clean Air Act connects pollution costs to those responsible for polluting?
A. Environmental costs belong only to residents
B. All polluters are exempt
C. Polluters must pay
D. Permits remove all cleanup obligations
MARKED ANSWER C. Polluters must pay
WHY R.A. 8749 recognizes the polluters-must-pay principle.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html

### 1099 | CIVIO-GI-20261013-0009
TRACK both | DOMAIN general_information | SKILL Public participation | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A city invites residents to comment on an air-quality plan. Which R.A. 8749 approach is being applied?
A. Exclusion of the public from air monitoring
B. Removal of accountability for emitters
C. Suspension of all air standards
D. Public participation in environmental planning
MARKED ANSWER D. Public participation in environmental planning
WHY The law encourages public involvement in air-quality planning and monitoring.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html

### 1100 | CIVIO-GI-20261013-0010
TRACK both | DOMAIN general_information | SKILL Air quality | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which is a central objective of R.A. 8749?
A. Preventing and controlling harmful emissions into the air
B. Determining the minimum voting age
C. Regulating only wildlife hunting licenses
D. Setting graduation requirements for public schools
MARKED ANSWER A. Preventing and controlling harmful emissions into the air
WHY The statute establishes a broad national policy for air pollution management.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html

### 1101 | CIVIO-GI-20261013-0011
TRACK both | DOMAIN general_information | SKILL Clean Water Act | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which law establishes the Philippine Clean Water Act of 2004?
A. R.A. 9729
B. R.A. 9275
C. R.A. 8749
D. R.A. 9003
MARKED ANSWER B. R.A. 9275
WHY R.A. 9275 is the Philippine Clean Water Act of 2004.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html

### 1102 | CIVIO-GI-20261013-0012
TRACK both | DOMAIN general_information | SKILL Water bodies | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which water bodies fall within the water-quality protection policy of R.A. 9275?
A. Only privately owned wells
B. Only swimming pools
C. Fresh, brackish, and marine waters
D. Only mountain waterfalls
MARKED ANSWER C. Fresh, brackish, and marine waters
WHY R.A. 9275 covers the quality of fresh, brackish, and marine waters.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html

### 1103 | CIVIO-GI-20261013-0013
TRACK both | DOMAIN general_information | SKILL Water pollution | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A community finds untreated wastewater flowing into a river. What concern is most directly addressed by R.A. 9275?
A. Aircraft registration
B. Road traffic signs
C. Building-height restrictions
D. Water pollution prevention and control
MARKED ANSWER D. Water pollution prevention and control
WHY R.A. 9275 provides a framework for reducing and controlling water pollution.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html

### 1104 | CIVIO-GI-20261013-0014
TRACK both | DOMAIN general_information | SKILL Land-based sources | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which pollution source does R.A. 9275 emphasize in its primary coverage?
A. Pollution from land-based sources
B. Only sound from aircraft
C. Only ultraviolet radiation
D. Only pollution originating from satellites
MARKED ANSWER A. Pollution from land-based sources
WHY Its coverage primarily emphasizes water pollution from land-based sources, while standards apply broadly.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html

### 1105 | CIVIO-GI-20261013-0015
TRACK both | DOMAIN general_information | SKILL Environmental management | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A local plan combines monitoring, prevention, and community education to protect waterways. Which approach best matches R.A. 9275?
A. Disposal of all waste into drains
B. Treating public information as unnecessary
C. Integrated water-quality management
D. Removal of monitoring systems
MARKED ANSWER C. Integrated water-quality management
WHY The law supports coordinated prevention, monitoring and informed public participation.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html

### 1106 | CIVIO-GI-20261013-0016
TRACK both | DOMAIN general_information | SKILL Wildlife law | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A conservation officer is looking for the law protecting wildlife species and habitats. Which statute is directly relevant?
A. R.A. 9147
B. R.A. 8749
C. R.A. 9003
D. R.A. 9275
MARKED ANSWER A. R.A. 9147
WHY R.A. 9147 is the Wildlife Resources Conservation and Protection Act.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html

### 1107 | CIVIO-GI-20261013-0017
TRACK both | DOMAIN general_information | SKILL Wildlife habitat | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
What is a principal goal of R.A. 9147?
A. Prohibit all scientific biodiversity research
B. Replace native species with imported species
C. Convert every habitat into commercial housing
D. Conserve wildlife and the habitats they depend on
MARKED ANSWER D. Conserve wildlife and the habitats they depend on
WHY The law aims to conserve wildlife species, habitats and ecological balance.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html

### 1108 | CIVIO-GI-20261013-0018
TRACK both | DOMAIN general_information | SKILL Endemic species | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Under the definitions in R.A. 9147, what is an endemic species?
A. A species that lives only in captivity
B. A species with no natural habitat
C. A species naturally found only in specific areas of the country
D. Any species recently imported from abroad
MARKED ANSWER C. A species naturally found only in specific areas of the country
WHY Endemic means naturally occurring only in particular areas of the country.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html

### 1109 | CIVIO-GI-20261013-0019
TRACK both | DOMAIN general_information | SKILL Wildlife trade | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which activity is among those regulated under R.A. 9147?
A. Sale of ordinary office supplies
B. Collection and trade of wildlife
C. Registration of school attendance
D. Library book borrowing
MARKED ANSWER B. Collection and trade of wildlife
WHY The law regulates collection, exchange, importation and exportation of wildlife.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html

### 1110 | CIVIO-GI-20261013-0020
TRACK both | DOMAIN general_information | SKILL Habitat | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which description best matches the legal concept of habitat in R.A. 9147?
A. The natural place or environment where a species occurs
B. A list of endangered species only
C. The price of a wildlife product
D. Any construction site near a city
MARKED ANSWER A. The natural place or environment where a species occurs
WHY A habitat is the place or environment where a species naturally occurs or has established a population.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html

### 1111 | CIVIO-GI-20261013-0021
TRACK both | DOMAIN general_information | SKILL Climate Change Act | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which law established the Climate Change Commission?
A. R.A. 8749
B. R.A. 9147
C. R.A. 9003
D. R.A. 9729
MARKED ANSWER D. R.A. 9729
WHY R.A. 9729 is the Climate Change Act of 2009 and created the Climate Change Commission.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html

### 1112 | CIVIO-GI-20261013-0022
TRACK both | DOMAIN general_information | SKILL Adaptation | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A flood-prone community raises critical equipment above expected flood levels. This is chiefly an example of:
A. Open dumping
B. Wildlife importation
C. Climate adaptation
D. Air-quality sampling only
MARKED ANSWER C. Climate adaptation
WHY Adaptation means adjusting systems to actual or expected climate effects.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html

### 1113 | CIVIO-GI-20261013-0023
TRACK both | DOMAIN general_information | SKILL Anthropogenic causes | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
The word anthropogenic in R.A. 9729 refers to causes arising from:
A. Only earthquakes
B. Human activities
C. Only natural lunar cycles
D. Only changes in ocean tides
MARKED ANSWER B. Human activities
WHY Anthropogenic causes are produced by human activities.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html

### 1114 | CIVIO-GI-20261013-0024
TRACK both | DOMAIN general_information | SKILL Climate policy | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
According to the Climate Change Act, climate concerns should be incorporated into:
A. Government policy and development planning
B. Only school uniforms
C. Only private entertainment programs
D. Only road sign colors
MARKED ANSWER A. Government policy and development planning
WHY R.A. 9729 directs the integration of climate change in government policy and development plans.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html

### 1115 | CIVIO-GI-20261013-0025
TRACK both | DOMAIN general_information | SKILL Safe Spaces Act | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which law is formally called the Safe Spaces Act?
A. R.A. 9003
B. R.A. 8749
C. R.A. 9275
D. R.A. 11313
MARKED ANSWER D. R.A. 11313
WHY R.A. 11313 is the Safe Spaces Act.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html

### 1116 | CIVIO-GI-20261013-0026
TRACK both | DOMAIN general_information | SKILL Gender-based harassment | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
A commuter experiences unwanted sexual remarks in a terminal. Which Philippine law directly addresses gender-based harassment in public spaces?
A. R.A. 11313
B. R.A. 9147
C. R.A. 9729
D. R.A. 9003
MARKED ANSWER A. R.A. 11313
WHY The Safe Spaces Act covers gender-based harassment in public spaces, including transport terminals.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html

### 1117 | CIVIO-GI-20261013-0027
TRACK both | DOMAIN general_information | SKILL Online safety | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which situation is addressed by the online-harassment provisions of R.A. 11313?
A. Legitimate classroom attendance
B. Unwanted gender-based sexual harassment directed at a person online
C. A polite request for a work update
D. Filing an ordinary public-record request
MARKED ANSWER B. Unwanted gender-based sexual harassment directed at a person online
WHY The Act also covers gender-based online sexual harassment.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html

### 1118 | CIVIO-GI-20261013-0028
TRACK both | DOMAIN general_information | SKILL Public-space coverage | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which is among the public places contemplated by R.A. 11313?
A. Only distant fishing grounds
B. Only private bedrooms
C. Public transport terminals
D. Only uninhabited islands
MARKED ANSWER C. Public transport terminals
WHY The law's public-space definition includes transportation terminals.
LEGAL SOURCE https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html

### 1119 | CIVIO-GI-20261013-0029
TRACK both | DOMAIN general_information | SKILL Ecology right | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which provision expressly protects the right to a balanced and healthful ecology?
A. Article I, Section 1
B. Article XVII, Section 30
C. Article III, Section 25
D. Article II, Section 16 of the 1987 Constitution
MARKED ANSWER D. Article II, Section 16 of the 1987 Constitution
WHY Article II, Section 16 protects the right to a balanced and healthful ecology.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1120 | CIVIO-GI-20261013-0030
TRACK both | DOMAIN general_information | SKILL Equal protection | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-general-info-supplement-001.json
STEM
Which part of the Constitution contains the equal protection guarantee?
A. Article III, Section 1
B. Article X, Section 20
C. Article XVII, Section 1
D. Article I, Section 1
MARKED ANSWER A. Article III, Section 1
WHY Article III, Section 1 contains due process and equal protection guarantees.
LEGAL SOURCE https://lawphil.net/consti/cons1987.html

### 1121 | CIVIO-CLR-20261013-0001
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed FIRST?
Folders: Alma Serrano | Anton Santos | Bea Salcedo | Carlo Santiago
A. Alma Serrano
B. Carlo Santiago
C. Bea Salcedo
D. Anton Santos
MARKED ANSWER C. Bea Salcedo
WHY Use surname first, then given name, in alphabetical order. The first folder is Bea Salcedo.

### 1122 | CIVIO-CLR-20261013-0002
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed LAST?
Folders: Dina Mercado | Dina Mendoza | Dina Mendez | Dina Melchor
A. Dina Melchor
B. Dina Mendoza
C. Dina Mercado
D. Dina Mendez
MARKED ANSWER C. Dina Mercado
WHY Use surname first, then given name, in alphabetical order. The last folder is Dina Mercado.

### 1123 | CIVIO-CLR-20261013-0003
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed FIRST?
Folders: Elise Cabrera | Emil Cabral | Elena Caballero | Edgar Cabantog
A. Elena Caballero
B. Elise Cabrera
C. Emil Cabral
D. Edgar Cabantog
MARKED ANSWER A. Elena Caballero
WHY Use surname first, then given name, in alphabetical order. The first folder is Elena Caballero.

### 1124 | CIVIO-CLR-20261013-0004
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed LAST?
Folders: Liza Villanueva | Leo Villamor | Lorna Villar | Luz Villegas
A. Leo Villamor
B. Liza Villanueva
C. Lorna Villar
D. Luz Villegas
MARKED ANSWER D. Luz Villegas
WHY Use surname first, then given name, in alphabetical order. The last folder is Luz Villegas.

### 1125 | CIVIO-CLR-20261013-0005
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed FIRST?
Folders: Nina Roldan | Noel Robles | Nico Roxas | Nena Roman
A. Nico Roxas
B. Noel Robles
C. Nena Roman
D. Nina Roldan
MARKED ANSWER B. Noel Robles
WHY Use surname first, then given name, in alphabetical order. The first folder is Noel Robles.

### 1126 | CIVIO-CLR-20261013-0006
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed LAST?
Folders: Pablo Valencia | Paula Valdez | Patricia Valerio | Paolo Valles
A. Patricia Valerio
B. Paolo Valles
C. Pablo Valencia
D. Paula Valdez
MARKED ANSWER B. Paolo Valles
WHY Use surname first, then given name, in alphabetical order. The last folder is Paolo Valles.

### 1127 | CIVIO-CLR-20261013-0007
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed FIRST?
Folders: Rico Alvarez | Rita Alvarado | Rina Alonzo | Ramon Alva
A. Rico Alvarez
B. Rina Alonzo
C. Ramon Alva
D. Rita Alvarado
MARKED ANSWER B. Rina Alonzo
WHY Use surname first, then given name, in alphabetical order. The first folder is Rina Alonzo.

### 1128 | CIVIO-CLR-20261013-0008
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
A filing clerk arranges records alphabetically by surname, then given name. Which folder should be filed LAST?
Folders: Sofia Bautista | Samuel Batong | Shiela Bañez | Sandro Bayani
A. Samuel Batong
B. Sofia Bautista
C. Sandro Bayani
D. Shiela Bañez
MARKED ANSWER C. Sandro Bayani
WHY Use surname first, then given name, in alphabetical order. The last folder is Sandro Bayani.

### 1129 | CIVIO-CLR-20261013-0009
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
The registry uses ascending numerical filing by the full five-digit reference number. Which record should be placed FIRST?
Records: 00142 | 00124 | 00141 | 00114
A. 00124
B. 00141
C. 00142
D. 00114
MARKED ANSWER D. 00114
WHY Compare the complete five-digit reference numbers numerically, preserving leading zeros.

### 1130 | CIVIO-CLR-20261013-0010
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
The registry uses ascending numerical filing by the full five-digit reference number. Which record should be placed LAST?
Records: 00709 | 00790 | 00719 | 00791
A. 00709
B. 00719
C. 00790
D. 00791
MARKED ANSWER D. 00791
WHY Compare the complete five-digit reference numbers numerically, preserving leading zeros.

### 1131 | CIVIO-CLR-20261013-0011
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
The registry uses ascending numerical filing by the full five-digit reference number. Which record should be placed FIRST?
Records: 02004 | 02040 | 02400 | 02003
A. 02003
B. 02040
C. 02400
D. 02004
MARKED ANSWER A. 02003
WHY Compare the complete five-digit reference numbers numerically, preserving leading zeros.

### 1132 | CIVIO-CLR-20261013-0012
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
The registry uses ascending numerical filing by the full five-digit reference number. Which record should be placed LAST?
Records: 10021 | 10102 | 10012 | 10020
A. 10020
B. 10021
C. 10012
D. 10102
MARKED ANSWER D. 10102
WHY Compare the complete five-digit reference numbers numerically, preserving leading zeros.

### 1133 | CIVIO-CLR-20261013-0013
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
The registry uses ascending numerical filing by the full five-digit reference number. Which record should be placed FIRST?
Records: 04318 | 04381 | 04138 | 04319
A. 04319
B. 04138
C. 04318
D. 04381
MARKED ANSWER B. 04138
WHY Compare the complete five-digit reference numbers numerically, preserving leading zeros.

### 1134 | CIVIO-CLR-20261013-0014
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
The registry uses ascending numerical filing by the full five-digit reference number. Which record should be placed LAST?
Records: 09001 | 00901 | 09010 | 09011
A. 09001
B. 09011
C. 00901
D. 09010
MARKED ANSWER B. 09011
WHY Compare the complete five-digit reference numbers numerically, preserving leading zeros.

### 1135 | CIVIO-CLR-20261013-0015
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Documents are filed from earliest date to latest, using YYYY-MM-DD. Which dated record should be placed FIRST?
Dates: 2026-10-01 | 2026-09-30 | 2026-10-03 | 2026-09-28
A. 2026-10-01
B. 2026-09-30
C. 2026-10-03
D. 2026-09-28
MARKED ANSWER D. 2026-09-28
WHY Compare year, then month, then day to find the correct chronological position.

### 1136 | CIVIO-CLR-20261013-0016
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Documents are filed from earliest date to latest, using YYYY-MM-DD. Which dated record should be placed LAST?
Dates: 2026-01-05 | 2026-01-15 | 2026-02-01 | 2026-01-25
A. 2026-02-01
B. 2026-01-15
C. 2026-01-05
D. 2026-01-25
MARKED ANSWER A. 2026-02-01
WHY Compare year, then month, then day to find the correct chronological position.

### 1137 | CIVIO-CLR-20261013-0017
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Documents are filed from earliest date to latest, using YYYY-MM-DD. Which dated record should be placed FIRST?
Dates: 2025-12-21 | 2026-01-02 | 2025-11-30 | 2025-12-03
A. 2025-11-30
B. 2025-12-03
C. 2026-01-02
D. 2025-12-21
MARKED ANSWER A. 2025-11-30
WHY Compare year, then month, then day to find the correct chronological position.

### 1138 | CIVIO-CLR-20261013-0018
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Documents are filed from earliest date to latest, using YYYY-MM-DD. Which dated record should be placed LAST?
Dates: 2026-07-31 | 2026-08-01 | 2026-07-30 | 2026-08-03
A. 2026-08-03
B. 2026-07-31
C. 2026-07-30
D. 2026-08-01
MARKED ANSWER A. 2026-08-03
WHY Compare year, then month, then day to find the correct chronological position.

### 1139 | CIVIO-CLR-20261013-0019
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Documents are filed from earliest date to latest, using YYYY-MM-DD. Which dated record should be placed FIRST?
Dates: 2026-03-01 | 2026-02-28 | 2026-03-03 | 2026-02-27
A. 2026-03-01
B. 2026-02-27
C. 2026-03-03
D. 2026-02-28
MARKED ANSWER B. 2026-02-27
WHY Compare year, then month, then day to find the correct chronological position.

### 1140 | CIVIO-CLR-20261013-0020
TRACK subprofessional | DOMAIN clerical | SKILL Filing | DIFFICULTY medium | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Documents are filed from earliest date to latest, using YYYY-MM-DD. Which dated record should be placed LAST?
Dates: 2026-11-14 | 2026-11-04 | 2026-10-30 | 2026-10-31
A. 2026-10-31
B. 2026-11-04
C. 2026-11-14
D. 2026-10-30
MARKED ANSWER C. 2026-11-14
WHY Compare year, then month, then day to find the correct chronological position.

### 1141 | CIVIO-CLR-20261013-0021
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a place to stay" in a government memo?
A. acomodation
B. accommodation
C. acommodation
D. accomodation
MARKED ANSWER B. accommodation
WHY The standard spelling is "accommodation". Check its exact letter order and doubled consonants where present.

### 1142 | CIVIO-CLR-20261013-0022
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "upkeep" in a government memo?
A. maintainance
B. maintenance
C. maintenence
D. maintinance
MARKED ANSWER B. maintenance
WHY The standard spelling is "maintenance". Check its exact letter order and doubled consonants where present.

### 1143 | CIVIO-CLR-20261013-0023
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "not joined" in a government memo?
A. seperete
B. seperate
C. separrate
D. separate
MARKED ANSWER D. separate
WHY The standard spelling is "separate". Check its exact letter order and doubled consonants where present.

### 1144 | CIVIO-CLR-20261013-0024
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "required" in a government memo?
A. nessesary
B. necesary
C. neccessary
D. necessary
MARKED ANSWER D. necessary
WHY The standard spelling is "necessary". Check its exact letter order and doubled consonants where present.

### 1145 | CIVIO-CLR-20261013-0025
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a formal suggestion" in a government memo?
A. recommendation
B. reccommendation
C. recommenddation
D. recomendation
MARKED ANSWER A. recommendation
WHY The standard spelling is "recommendation". Check its exact letter order and doubled consonants where present.

### 1146 | CIVIO-CLR-20261013-0026
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "proof of payment" in a government memo?
A. reciept
B. receipt
C. receeipt
D. receit
MARKED ANSWER B. receipt
WHY The standard spelling is "receipt". Check its exact letter order and doubled consonants where present.

### 1147 | CIVIO-CLR-20261013-0027
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a special right" in a government memo?
A. privelege
B. privilage
C. privilege
D. priviledge
MARKED ANSWER C. privilege
WHY The standard spelling is "privilege". Check its exact letter order and doubled consonants where present.

### 1148 | CIVIO-CLR-20261013-0028
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "without doubt" in a government memo?
A. definitely
B. definitly
C. definately
D. defenitely
MARKED ANSWER A. definitely
WHY The standard spelling is "definitely". Check its exact letter order and doubled consonants where present.

### 1149 | CIVIO-CLR-20261013-0029
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a group assigned a task" in a government memo?
A. committie
B. comittee
C. commitee
D. committee
MARKED ANSWER D. committee
WHY The standard spelling is "committee". Check its exact letter order and doubled consonants where present.

### 1150 | CIVIO-CLR-20261013-0030
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a particular event" in a government memo?
A. ocassion
B. occassion
C. ocasian
D. occasion
MARKED ANSWER D. occasion
WHY The standard spelling is "occasion". Check its exact letter order and doubled consonants where present.

### 1151 | CIVIO-CLR-20261013-0031
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "the staff of an organization" in a government memo?
A. personnell
B. personnel
C. personeel
D. personel
MARKED ANSWER B. personnel
WHY The standard spelling is "personnel". Check its exact letter order and doubled consonants where present.

### 1152 | CIVIO-CLR-20261013-0032
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "to cause awkwardness" in a government memo?
A. embarrass
B. embarass
C. embbarass
D. embarras
MARKED ANSWER A. embarrass
WHY The standard spelling is "embarrass". Check its exact letter order and doubled consonants where present.

### 1153 | CIVIO-CLR-20261013-0033
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a list of survey questions" in a government memo?
A. questionnaire
B. questionaire
C. questinnaire
D. questionnair
MARKED ANSWER A. questionnaire
WHY The standard spelling is "questionnaire". Check its exact letter order and doubled consonants where present.

### 1154 | CIVIO-CLR-20261013-0034
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a schedule of dates" in a government memo?
A. calandar
B. calender
C. calendar
D. callendar
MARKED ANSWER C. calendar
WHY The standard spelling is "calendar". Check its exact letter order and doubled consonants where present.

### 1155 | CIVIO-CLR-20261013-0035
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a person connecting groups" in a government memo?
A. liaisson
B. laysion
C. liason
D. liaison
MARKED ANSWER D. liaison
WHY The standard spelling is "liaison". Check its exact letter order and doubled consonants where present.

### 1156 | CIVIO-CLR-20261013-0036
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "without delay" in a government memo?
A. imediately
B. immediateley
C. immediatly
D. immediately
MARKED ANSWER D. immediately
WHY The standard spelling is "immediately". Check its exact letter order and doubled consonants where present.

### 1157 | CIVIO-CLR-20261013-0037
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "easy to reach or use" in a government memo?
A. accessable
B. acessible
C. accessible
D. accesible
MARKED ANSWER C. accessible
WHY The standard spelling is "accessible". Check its exact letter order and doubled consonants where present.

### 1158 | CIVIO-CLR-20261013-0038
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "an event or happening" in a government memo?
A. occurrence
B. occurrance
C. occurence
D. ocurrence
MARKED ANSWER A. occurrence
WHY The standard spelling is "occurrence". Check its exact letter order and doubled consonants where present.

### 1159 | CIVIO-CLR-20261013-0039
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "an administrative system" in a government memo?
A. bureacracy
B. bureaucracy
C. beaurocracy
D. burocracy
MARKED ANSWER B. bureaucracy
WHY The standard spelling is "bureaucracy". Check its exact letter order and doubled consonants where present.

### 1160 | CIVIO-CLR-20261013-0040
TRACK subprofessional | DOMAIN clerical | SKILL Spelling | DIFFICULTY easy | LANGUAGE en | REVIEW draft/unreviewed
ORIGIN docs/research/subprofessional-clerical-supplement-001.json
STEM
Which choice correctly spells the word meaning the office term "a person supervising an organization" in a government memo?
A. superintendant
B. superintendent
C. supertendent
D. superintendantt
MARKED ANSWER B. superintendent
WHY The standard spelling is "superintendent". Check its exact letter order and doubled consonants where present.


## Complete Civio research/design specification (source copy)

# Civio CSE Question Design Spec

Version: 0.1.4 (CoS rulings on batches 002–011: new codes, tense cap, frame rule, filing sub-reasons, baseline dedup; see 10.3)
Date: 5 Oct 2026 (Asia/Manila); approved 7 Oct 2026
Owner: GT
Status: **Approved by GT on 7 Oct 2026.** The canonical copy lives in GT's Obsidian vault; this repo copy
records the Section 10 decisions below. No item has been written under it yet.

---

## 0. How to use this spec

- This spec says how every Civio Civil Service Exam (CSE) item must be built, checked, and explained.
- It is based on (a) the official CSC scope and (b) patterns seen in public Philippine CSE reviewers (Section 2).
- Reviewer pages were **read only**. No question, number, name, or wording from them is used here or may go into the bank.
- **Gate:** No bulk writer (human or AI) may run until GT or the Chief of Staff approves this spec in writing. See Section 9.

---

## 1. Official scope

Source: CSC Examination Announcement No. 03, s. 2026 (CSE-PPT, 09 August 2026), Section F "Scope of Examination" and Section G "Passing Grade". PDF: https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf

### 1.1 Format

| | Professional | Subprofessional |
|---|---|---|
| Scored items | 150 | 145 |
| Time | 3 h 10 min (190 min) | 2 h 40 min (160 min) |
| Average time budget | about 76 s per item | about 66 s per item |
| Passing | General rating of at least 80.00 | Same |
| Calculator | Not allowed (any type, including watch calculators) | Same |
| Subtest weights | Not published by CSC | Not published by CSC |

Notes:
- Passing grade, calculator ban, and scope are stated in the announcement.
- Item counts and time come from GT's brief. The announcement text does not list them. They match reviewer sites, which say 170 / 165 printed items including about 20 personal-information items (so about 150 / 145 scored).
- CSC does not publish weights per subtest. Any mix in this spec is a Civio practice choice, not an official weight. Never tell users otherwise.

### 1.2 Subtests

**Both levels**

- **General Information** (in English)
  1. 1987 Philippine Constitution
  2. R.A. 6713 (Code of Conduct and Ethical Standards for Public Officials and Employees)
  3. Peace and human rights issues and concepts
  4. Environment management and protection
- **Verbal Ability** (in English and Filipino)
  1. Word meaning
  2. Sentence completion
  3. Error recognition
  4. Sentence structure
  5. Paragraph organization
  6. Reading comprehension
- **Numerical Ability** (in English)
  1. Basic operations
  2. Number sequence
  3. Word problems

**Professional only**

- **Analytical Ability** (in English): word analogy; symbolic logic / abstract reasoning; identifying assumptions and drawing conclusions; data interpretation.

**Subprofessional only**

- **Clerical Ability** (in English): filing; spelling.

### 1.3 What examinees report

- Time is the hard part. Plan for about 1 minute per item.
- Math word problems and paragraph organization eat the clock.
- Constitution and R.A. 6713 items are "match the rule": you either know the provision or you don't.

Design consequence: Civio items must train **speed with accuracy**. Every item has a target time, and every Reveal teaches a shortcut that saves time on the next item.

---

## 2. Research log (Stage 1)

Read-only. Only aggregate patterns were recorded. No item content was kept.

### 2.1 URLs opened

| # | URL | Tool | Result | Subtest |
|---|---|---|---|---|
| 1 | https://testpinoy.com/cse-reviewer-math-1/ | WebFetch | Worked (40 items) | Numerical |
| 2 | https://testpinoy.com/cse-reviewer-math-2/ | WebFetch | Worked (35 items) | Numerical |
| 3 | https://csereviewer.com/numerical-reasoning/number-series-sequence/ | WebFetch | Worked (15 items) | Numerical (sequence) |
| 4 | https://testpinoy.com/cse-correct-usage/ | WebFetch | Worked (40 items) | Verbal EN |
| 5 | https://testpinoy.com/cse-paragraph-development/ | WebFetch | Worked (10 items, 4 paragraphs) | Verbal EN |
| 6 | https://csereviewer.com/reading-comprehension/cse-reading-comprehension-mock-quiz/ | WebFetch | Worked (15 items, 3 passages) | Verbal EN |
| 7 | https://testpinoy.com/cse-kasing-kahulugan/ | WebFetch | First try timed out; retry worked (25 items) | Verbal FIL |
| 8 | https://testpinoy.com/cse-kasalungat/ | WebFetch | Worked (25 items) | Verbal FIL |
| 9 | https://testpinoy.com/cse-filipino-wikain/ | WebFetch | Worked (25 items) | Verbal FIL |
| 10 | https://testpinoy.com/cse-double-word-analogy/ | WebFetch | Worked (40 items) | Analytical |
| 11 | https://csereviewer.com/logical-reasoning/civil-service-exam-logic-practice-test/ | WebFetch | Worked (20 items), but many items are general-aptitude types outside CSC scope | Analytical |
| 12 | https://filipiknow.net/wp-content/uploads/2021/05/Analytical-Ability-Practice-Test-Set-2.pdf | curl + pdftotext (WebFetch cannot read PDFs) | Worked (10 items) | Analytical (assumptions/conclusions) |
| 13 | https://filipiknow.net/wp-content/uploads/2022/12/Data-Interpretation-Practice-Questions.pdf | curl + pdftotext | Partial: 5 items; charts are images, only tables readable | Analytical (data interpretation) |
| 14 | https://topnotcher.ph/data-interpretation-practice-test/ | WebFetch | Opened, **no items** (quiz loads by script; guidance text only) | Analytical |
| 15 | https://csereviewer.com/clerical-operations/cse-alphabetical-filing/ | WebFetch | Worked (20 items) | Clerical (filing) |
| 16 | https://filipiknow.net/wp-content/uploads/2021/06/Clerical-Ability-Practice-Test-Set-2.pdf | curl + pdftotext | Worked (20 items) | Clerical (spelling) |
| 17 | https://csereviewer.com/general-information/republic-act-6713-reviewer/ | WebFetch | Worked (20 items) | General Information |
| 18 | https://csereviewer.com/general-information/philippine-constitution-reviewer/ | WebFetch | Worked (15 items) | General Information |
| 19 | http://www.philmetrics.com/2025/04/cse-43-civil-service-examination.html | WebFetch | **Failed** (403 Forbidden) | Verbal EN |
| 20 | CSC Exam Announcement No. 03 s. 2026 PDF (link in Section 1) | curl + pdftotext | Worked. Official scope; **no items** | Scope |

Pages seen only as search snippets (not opened, not used): filipiknow.net verbal PDFs, cseexamreview.com, lisensyaprep.com, open-exam-prep.com, civpasser.com, supertutor.ph, examreviewph.com.

No Indian "CSE aptitude" material was used.

### 2.2 Cross-site findings

1. **Third-party answer keys are not reliable.** Across URLs 1, 2 and 11, at least four keyed answers did not match the arithmetic or the logic. Civio must never import or trust a third-party key. This is one more reason for the "original items only" rule.
2. **Choice count varies.** Some sites use 4 choices, some 5 (URLs 5, 6, 11, 15, 16, 17). Civio standard is 4 choices.
3. **Underlines get lost.** Several items depend on an underlined word or name. On the web pages the underline was gone, so the item could not be answered. Civio must not rely on underline or color alone (see Section 4).
4. **Scope drift.** Some GI pages include international bodies and unrelated laws. Some logic pages include family-relation, clock, and mirror puzzles. These are outside the CSC list. Civio stays inside Section 1.2.
5. **Filing rules differ between sites** (for example, how to file numerals inside business names). Civio must publish one rule set and avoid disputed edge cases until it is approved.

### 2.3 Per-URL pattern notes (aggregate only)

| # | Steps | Main trap | Wording level | Difficulty | Typical wrong choices | Time per item |
|---|---|---|---|---|---|---|
| 1 | 1–2 (compute), 2–3 (short word problems) | Order of operations; percent "of" vs "is what percent of"; odd/even and divisibility claims | Short, plain, symbols-heavy | Easy–medium | Off by one digit or one step; reverse operation; wrong base | 30–60 s |
| 2 | 2–4 | Percent change base; successive % changes do not cancel; reverse percent; unit conversion; "more than twice" | Plain English, peso and everyday office/home contexts | Medium–hard | Partial answer (one step missing); added % instead of multiplied; decimal shifted ×10; the given number reused | 60–120 s |
| 3 | 1–2 | Rule has 2 layers (differences grow; ×k then +c; alternating sign; two interleaved series) | Numbers only | Easy–hard by rule depth | Value from a simpler, wrong rule; sign error; skipped a step | 30–60 s |
| 4 | 1 | Homophones; phrasal verb particles; word choice pairs | Short sentences, common words | Easy | Sound-alike word; same verb with wrong particle; wrong verb form | 15–30 s |
| 5 | Read 5 sentences, find order, then answer 2–3 questions | Topic sentence placement; transition words; concluding sentence | Medium, civic/public topics | Medium | Orders that keep one correct pair but misplace the opener; titles too broad or too narrow | 60–90 s per question |
| 6 | Read about 250–300 words, then 5 questions | Mostly literal recall and main idea | Medium | Easy (too literal for real exam) | Not in passage; too extreme; opposite of passage | about 60 s per question incl. reading |
| 7 | 1 | Deep Tagalog word; context sentence gives a weak clue | Formal Filipino | Easy–hard by word rarity | Same-field word with different meaning; right field, wrong intensity | 15–30 s |
| 8 | 1–2 (find meaning, then flip) | A synonym of the target is placed among choices | Formal Filipino | Medium | The synonym trap; unrelated same-field word | 20–30 s |
| 9 | 1 | Idiom read literally | Idiomatic Filipino | Medium | Literal meaning; nearby emotion; partial meaning | 15–30 s |
| 10 | 2 (name relation, test choices) | Same topic but different relation; reversed order | High-register English at hard level | Easy–hard | Topic-related pair with wrong relation; reversed pair; pair linked by sound | 20–40 s |
| 11 | 2–4 | Syllogism "valid vs true"; ordering puzzles | Plain | Medium | Converse error; "could be" vs "must be" | 45–90 s |
| 12 | 2 | Over-strong quantifiers ("all", "everyone") vs "most"; true-but-irrelevant assumption | Plain | Medium | Over-strong claim; irrelevant fact; "sole cause" claim | 45–75 s |
| 13 | 2–3 | Read the right row; average; percent of total; "cannot be determined" | Plain, with table or chart | Easy–medium | Wrong row; wrong base; arithmetic slip | 45–90 s |
| 15 | 3–5 (convert each name to filing order, compare letter by letter) | One-letter differences; prefixes; titles; leading "The"; numerals | Names and business names | Medium | Word-by-word instead of letter-by-letter; title counted; prefix split off | 30–60 s |
| 16 | 1 (scan for the misspelling) | Single-letter errors: doubled consonant, ie/ei, dropped letter, spelling by sound | Long, formal English words | Easy–medium | Correct but unusual-looking words placed beside the misspelled one | 10–20 s |
| 17 | 1 (recall) or 2 (apply rule to scenario) | Neighboring deadlines from the same law; near-synonym ethics words | Formal, legal paraphrase | Medium | Neighboring number; nice-sounding but wrong principle | 20–40 s |
| 18 | 1 | Similar bodies or similar terms (sibling terms) | Formal | Easy–medium | Wrong body; sibling term; near-title of a law | 15–30 s |

---

## 3. Per-subtest design

### 3.0 Shared definitions

**Difficulty tiers (apply to every subtest):**

| Tier | Definition | Time rule |
|---|---|---|
| Easy | One step or direct recall. Common words. No trap beyond basic care. | Solvable within the target time by a prepared examinee |
| Medium | Two steps, **or** one step plus one named trap. | Within target time if the shortcut is known |
| Hard | Three or more steps, **or** two traps that interact, **or** uncommon vocabulary / provision. | Must still be solvable within 1.5× target time without a calculator |

Once real answer data exists, recalibrate: easy at least 80% correct, medium 50–80%, hard below 50%.

**Distractor rule (all subtests):** Every wrong choice must be the result of one specific, real mistake. Record that mistake by code (lists below) in `distractor_reasoning`. A wrong choice that is "just a random nearby value" fails review.

Avoid "all of the above" and "none of the above". "Cannot be determined" is allowed only in Analytical items where it is a real possibility, and it must sometimes be the right answer.

**Overall time check:** A Civio practice set should average at most 60 s per item, leaving time to review within the official budget (76 s Pro, 66 s Sub).

---

### 3.1 Numerical Ability (both levels, in English)

Informed by: URLs 1, 2, 3, 13.

| Archetype | What it is | Steps | Typical trap | Target s |
|---|---|---|---|---|
| NUM-OPS-ORDER | Evaluate a mixed expression | 1–2 | Left-to-right instead of order of operations | 35 |
| NUM-PCT-BASIC | Percent of / is what percent of / is P% of what | 1 | Wrong base (divides the wrong way) | 35 |
| NUM-FRAC-DEC | Fractions, mixed numbers, decimals | 1–2 | Adds denominators; decimal place slip | 40 |
| NUM-PROPERTY | Odd/even, divisibility, which statement is always true | 1–2 | Assumes the converse is true | 40 |
| NUM-SHIFTED-BLOCK | Sum of a block of numbers, given a related block sum | 1–2 | Re-adds everything; adds the shift only once | 40 |
| NUM-SEQ-DIFF | Next term; differences grow by a fixed amount | 2 | Uses first difference only | 45 |
| NUM-SEQ-MULT | Next term; ×k, or ×k then ±c | 2 | Sees only the +c or only the ×k | 45 |
| NUM-SEQ-ALT | Two interleaved series or alternating signs | 2 | Treats it as one series | 50 |
| NUM-WP-PCT-CHANGE | Increase/decrease, markup/discount, successive changes, reverse percent | 2–3 | Adds percents; uses new value as base | 90 |
| NUM-WP-AVERAGE | Average, target average, missing value | 2 | Uses the target average as the answer | 60 |
| NUM-WP-RATE | Unit price, speed, work, rent vs buy | 2–3 | Unit mismatch; compares wrong totals | 90 |
| NUM-WP-RATIO | Split a total in a ratio / "X times as much" | 2 | Divides by the multiplier instead of parts | 75 |
| NUM-WP-GEOM | Perimeter, area, surface count | 2–3 | Area vs perimeter mix-up; counts faces wrongly | 90 |
| NUM-WP-ALGEBRA | "k more than m times a number" type setup | 2–3 | Translates words in the wrong order | 90 |

Wording level: short sentences, everyday Philippine settings (barangay, office, market, salary, bills), pesos written as "PHP" or "₱" (see encoding rule 8.1). Numbers must be computable by hand in the target time.

Distractor codes:
- `NUM-PARTIAL` stopped one step early
- `NUM-EXTRA-STEP` did one step too many
- `NUM-WRONG-BASE` percent or ratio taken of the wrong quantity
- `NUM-PCT-ADD` added or subtracted percents instead of chaining them
- `NUM-OP-SWAP` multiplied instead of divided (or added instead of subtracted)
- `NUM-ORDER-OPS` ignored order of operations
- `NUM-DECIMAL` decimal point shifted
- `NUM-UNIT` forgot a unit conversion
- `NUM-GIVEN-REUSED` picked a number already in the stem
- `NUM-SEQ-OTHER-RULE` next term under a simpler but wrong rule
- `NUM-OFF-BY-ONE` counting fence-post error
- `NUM-OTHER-SHARE` answered the other party's share (added v0.1.3, CoS)

Suggested Civio mix: basic operations 30%, number sequence 20%, word problems 50%. Difficulty mix per set: 30% easy, 50% medium, 20% hard.

---

### 3.2 Verbal Ability, English (both levels)

Informed by: URLs 4, 5, 6 (URL 19 failed).

| Archetype | What it is | Steps | Typical trap | Target s |
|---|---|---|---|---|
| VEN-WORD-MEANING | Meaning of a word in a sentence | 1 | Common meaning vs meaning in this context | 20 |
| VEN-SENT-COMP-WORD | Fill the blank with the right word | 1 | Homophone; near-synonym with wrong tone | 25 |
| VEN-SENT-COMP-PHRASAL | Fill the blank with the right phrasal verb | 1 | Same verb, wrong particle | 25 |
| VEN-ERROR-AGREE | Find the error: subject-verb or pronoun-antecedent agreement | 1–2 | Phrase between subject and verb; collective nouns; "each/everyone" | 35 |
| VEN-ERROR-TENSE | Find the error: tense consistency, verb form | 1–2 | Tense shift mid-sentence | 35 |
| VEN-ERROR-MODIFIER | Find the error: adjective vs adverb, comparison, parallelism | 2 | Adjective used for adverb; unbalanced list | 40 |
| VEN-SENT-STRUCTURE | Choose the best-built sentence | 2 | Run-on, fragment, misplaced modifier | 40 |
| VEN-PARA-ORDER | Order 4–5 sentences; asked for first/last/Nth sentence | 3 | Starts with a detail, not the topic sentence; ignores transitions | 75 |
| VEN-PARA-INSERT | Where an added sentence fits / new order | 3 | Puts a "however" sentence before the idea it answers | 75 |
| VEN-RC-MAIN | Main idea / best title | 2 | Too broad or too narrow | 60 |
| VEN-RC-DETAIL | Stated fact | 1 | Plausible but not in text | 45 |
| VEN-RC-INFER | What the passage implies | 2 | Goes beyond the text; extreme words | 70 |
| VEN-RC-VOCAB | Word meaning in the passage | 1 | Dictionary meaning that does not fit here | 40 |

Wording level: sentences 10–25 words; passages 150–250 words (shorter than some reviewers, to keep the clock realistic); topics are civic, workplace, health, environment, community. Note: URL 6 was almost all literal recall. Civio RC sets must include at least one inference and one vocabulary-in-context item per passage.

Distractor codes:
- `VEN-NEAREST-NOUN` verb agrees with the closest noun, not the subject
- `VEN-TENSE` wrong tense for the time signal in the sentence
- `VEN-HOMOPHONE` sounds the same, means something else
- `VEN-PARTICLE` right verb, wrong particle
- `VEN-FORM` wrong verb form (participle, gerund, infinitive)
- `VEN-REGISTER` right meaning, wrong tone or formality
- `RC-NOT-IN-TEXT` true-sounding but not supported
- `RC-TOO-BROAD` / `RC-TOO-NARROW`
- `RC-EXTREME` uses "always/never/completely" beyond the text
- `RC-OPPOSITE` reverses the passage
- `VRB-SYNONYM-TRAP` a word that means the same as the cue (or a real sense of the word that does not fit this sentence), offered where something else is asked (v0.1.4)
- `VRB-ANTONYM-TRAP` a word that means the opposite of what is asked (v0.1.4)
- `PO-OPENER-MISPLACED` topic sentence not first
- `PO-TRANSITION-IGNORED` sentence with a link word placed before what it links to

Suggested Civio mix (English half of Verbal): word meaning 15%, sentence completion 20%, error recognition 20%, sentence structure 10%, paragraph organization 15%, reading comprehension 20%.

---

### 3.3 Verbal Ability, Filipino (both levels)

Informed by: URLs 7, 8, 9.

| Archetype | What it is | Steps | Typical trap | Target s |
|---|---|---|---|---|
| VFIL-KASINGKAHULUGAN | Synonym of the marked word in a sentence | 1 | Same-field word with a different meaning | 20 |
| VFIL-KASALUNGAT | Antonym of the marked word | 2 | A synonym of the word is among the choices | 25 |
| VFIL-WIKAIN | Meaning of an idiom (sawikain) in a sentence | 1 | Literal reading of the idiom | 25 |
| VFIL-BALARILA | Correct usage (ng/nang, may/mayroon, pang-ukol, panghalip) | 1–2 | Everyday spoken form that is not standard | 30 |
| VFIL-PAGBASA | Short Filipino passage, main idea / detail / inference | 2 | Same as RC codes | 60 |
| VFIL-PAGSUSUNOD | Order sentences in Filipino | 3 | Same as paragraph codes | 75 |

Wording level: standard formal Filipino. Target words: "malalim" but real and current, not archaic. Check every word in a standard Filipino dictionary (UP Diksiyonaryong Filipino or KWF). Do not mark the target word by underline only (see 4.6).

Distractor codes:
- `FIL-SAME-FIELD` related meaning, wrong word
- `FIL-SYNONYM-TRAP` (antonym items) gives a synonym instead of an antonym
- `FIL-LITERAL` idiom taken word-for-word
- `FIL-INTENSITY` right direction, wrong strength
- `FIL-SPOKEN-FORM` common spoken usage that breaks the standard rule
- plus the RC and paragraph codes from 3.2

Suggested Civio mix (Filipino half of Verbal): synonym 25%, antonym 20%, idiom 15%, grammar 15%, reading 15%, paragraph order 10%.

---

### 3.4 Analytical Ability (Professional only, in English)

Informed by: URLs 10, 11, 12, 13 (URL 14 had no items).

| Archetype | What it is | Steps | Typical trap | Target s |
|---|---|---|---|---|
| ANA-ANALOGY-SYN/ANT | A:B :: ? where A and B are synonyms or antonyms | 2 | Choice pair is on topic but has the other relation | 25 |
| ANA-ANALOGY-DEGREE | Mild : strong form | 2 | Reversed direction | 30 |
| ANA-ANALOGY-PART/WHOLE | Part : whole, member : group | 2 | Whole : part (reversed) | 30 |
| ANA-ANALOGY-FUNCTION | Worker : tool, item : purpose, container : contents | 2 | Topic match, function mismatch | 30 |
| ANA-ANALOGY-FORM | Word forms: singular/plural, abbreviation, pronoun case | 2 | Pair with the right words, wrong form | 30 |
| ANA-SYLLOGISM | Two premises; which conclusion must follow | 2 | Converse; undistributed middle; "true in real life" vs "follows" | 60 |
| ANA-SYMBOL-SERIES | Letter or symbol series; coded rules | 2 | Tracks one rule, misses a second rule | 50 |
| ANA-ABSTRACT-FIGURE | Figure series (needs images) | 2 | Second, alternating rule | 60 |
| ANA-ASSUMPTION | Which unstated idea the argument needs | 2 | Over-strong quantifier; true but irrelevant | 60 |
| ANA-ASSUME-I-II | Statement plus assumptions I and II; choose only I / only II / both / neither | 2–3 | Accepts an assumption that is merely plausible | 60 |
| ANA-CONCLUSION | What must follow from a passage | 2 | "Could be true" instead of "must be true" | 60 |
| ANA-DI-TABLE | Read a table; total, average, difference, percent | 2–3 | Wrong row/column; wrong base | 75 |
| ANA-DI-CHART | Read a bar/line/pie chart | 2–3 | Scale or unit ignored ("in thousands") | 75 |

Scope rule: family-relation puzzles, clock angles, mirror images, and direction puzzles (seen on URL 11) are **not** in the CSC list. Do not write them.

Figure items (`ANA-ABSTRACT-FIGURE`, `ANA-DI-CHART`) need a stored image with alt text and a text table fallback. Do not write them until the image pipeline is confirmed.

Wording level: plain English stems; analogy vocabulary goes from common (easy) to formal (hard). Analogy words must have one clear relation.

Distractor codes:
- `ANA-SAME-TOPIC` pair from the same topic, different relation
- `ANA-REVERSED` right relation, wrong direction
- `ANA-ONE-LINK` pair linked to only one of the stem words
- `ANA-SOUND` pair linked by spelling or sound, not meaning
- `ANA-OTHER-RELATION` pair with a different clear relation (for example container : contents for a part : whole stem) (added v0.1.3, CoS)
- `LOG-CONVERSE` reverses "all A are B"
- `LOG-COULD-NOT-MUST` possible but not forced
- `LOG-OVERSTRONG` "all/only/sole" where the text supports less
- `LOG-IRRELEVANT` true statement the argument does not need
- `LOG-MISSED-NEEDED` rejects an assumption the argument does need (v0.1.4)
- `LOG-ORDER-SWAP` ordering: swaps the asked place with its neighbor (v0.1.4)
- `LOG-ORDER-REVERSED` ordering: counts from the wrong end of the line (v0.1.4, approved by CoS)
- `LOG-IGNORED-CLUE` ordering: an answer that is possible only if one clue is skipped (v0.1.4)
- `DI-WRONG-CELL` read the wrong row or column
- `DI-WRONG-BASE` percent of the wrong total
- `DI-SCALE` ignored unit or scale label
- `DI-NOT-SUPPORTED` reasonable claim the data does not show

Suggested Civio mix: analogy 30%, symbolic logic 20%, assumptions and conclusions 25%, data interpretation 25%.

---

### 3.5 Clerical Ability (Subprofessional only, in English)

Informed by: URLs 15, 16.

| Archetype | What it is | Steps | Typical trap | Target s |
|---|---|---|---|---|
| CLR-FILE-POSITION | 4 names; where does the named one fall in filing order | 3–4 | One-letter differences; prefixes; titles | 45 |
| CLR-FILE-ORDER | 4 names numbered; pick the correct order code | 4–5 | Word-by-word instead of letter-by-letter | 60 |
| CLR-FILE-BUSINESS | Business or agency names | 3–4 | Leading "The"; numerals; initials | 50 |
| CLR-FILE-NUMERIC | Order numbers or codes (including decimals) | 2–3 | Compares digit count, not value (or the reverse, per the rule) | 40 |
| CLR-SPELL-WRONG | Which of 4 words is misspelled | 1 | Unusual but correct words beside the wrong one | 15 |
| CLR-SPELL-RIGHT | Which of 4 spellings is correct | 1 | Spelling by sound | 15 |
| CLR-SPELL-CONTEXT | Which word fits the sentence (look-alike word pairs) | 1 | Look-alike word | 20 |

Rule set: Civio must publish **Civio Filing Rules v1** (surname first; letter by letter; prefixes are part of the surname; titles and suffixes do not change order except as tie-breakers; leading "The" ignored). Every filing item cites the rule number it tests. Until v1 is approved, do not write items on disputed edge cases (numerals inside names, Jr./Sr. ties).

Distractor codes:
- `CLR-WORD-BY-WORD` compared whole words instead of letters
- `CLR-PREFIX-SPLIT` filed a prefix as a separate word
- `CLR-TITLE-COUNTED` used a title (Dr., Mrs.) in the sort
- `CLR-ARTICLE-COUNTED` sorted by a leading "The"
- `CLR-FIRSTNAME-FIRST` sorted by given name
- `CLR-SPELL-CORRECT-FOIL` a correctly spelled word that looks unusual, offered beside the one misspelled word (v0.1.4)
- `CLR-LETTER-ORDER` misread the letter-by-letter order of the indexed units (v0.1.4, approved by CoS; filing sub-reason only)
- `SPL-DOUBLE` doubled or undoubled consonant
- `SPL-IE-EI` vowel order swapped
- `SPL-DROP` missing letter
- `SPL-SOUND` spelled as it sounds

Suggested Civio mix: filing 55%, spelling 45%.

---

### 3.6 General Information (both levels, in English)

Informed by: URLs 17, 18.

| Archetype | What it is | Steps | Typical trap | Target s |
|---|---|---|---|---|
| GI-TERM-MATCH | A provision is described; name the term or principle | 1 | Sibling term from the same article (terms for related processes or principles) | 20 |
| GI-WHO-HOLDS-POWER | Which office or body has a stated power | 1 | Similar body (one chamber vs the other; an officer vs the body) | 20 |
| GI-DEADLINE-NUMBER | A period, age, term length, or count set by law | 1 | Neighboring standard number from the same law | 20 |
| GI-SCENARIO-APPLY | A short workplace scenario; which act violates (or follows) the rule | 2 | Nice-sounding behavior that is not what the rule says | 35 |
| GI-RIGHTS-APPLY | A situation; which right or guarantee applies | 2 | Nearby right in the same article | 30 |
| GI-ENV-PRINCIPLE | Environment duty or principle in the Constitution or a law on LawPhil | 1–2 | General green idea not in the cited text | 25 |

Allowed sources (and only these): 1987 Constitution, R.A. 6713 and its implementing rules, LawPhil, the Official Gazette, CSC issuances. Every item cites the article and section (for example "1987 Const., Art. XI, Sec. 1" or "R.A. 6713, Sec. 4(a)") in `source`. No current events, no international bodies, no unrelated laws.

Wording level: formal, but paraphrase the law in plain English. Do not copy long legal text into the stem.

Distractor codes:
- `GI-SIBLING-TERM` related term from the same topic
- `GI-WRONG-BODY` similar office or chamber
- `GI-NEIGHBOR-NUMBER` another number that appears in the same law or topic
- `GI-SOUNDS-RIGHT` ethical-sounding but not the rule
- `GI-OLD-RULE` rule from an older constitution or superseded text

Suggested Civio mix: Constitution 40%, R.A. 6713 35%, peace and human rights 15%, environment 10%.

---

## 4. Item rules

1. **Normal exam item.** The stem reads like a real CSE item. It does not teach. No definitions or hints inside the stem (for example, never "An integer, which is a whole number, …"). Teaching belongs in the Reveal. A GI term-match stem that describes a provision is allowed because the description is the question. GT to confirm this reading.
2. **One defensible answer.** A careful expert must reach exactly one choice. If a second choice can be argued, rewrite.
3. **Four choices.** Exactly four, each with a stable `option_id`. Similar length and form. No "all/none of the above".
4. **Original.** New situation, new numbers, new names, new wording. Nothing from any reviewer site, book, or past exam. No third-party items, even reworded.
5. **GI facts.** Only from the sources in 3.6, with article/section cited.
6. **No formatting-only signals.** Never rely on underline, bold, or color alone to mark the target word or name. Put the target in quotation marks or name it in the question ("What is the meaning of the word 'X' in the sentence?").
7. **Hand-solvable.** Numerical and data items must be solvable without a calculator within the target time.
8. **Inclusive and neutral.** Filipino names and places from many regions; no stereotypes; no real living politicians; no partisan content.
9. **Language.** GI, Numerical, Analytical and Clerical items are in English (per the announcement). Verbal items are in English or Filipino, tagged in `language`.

---

## 5. Reveal format

Order is fixed. Short sentences. One idea per sentence.

1. **Meaning of basic terms.** Plain-language meaning of any basic term used (integer, percent, average, ratio, subject, verb, and so on). One or two lines each. Skip if no such term.
2. **Shortcut (Kumon-style).** One short, easy trick. If the trick is abstract, show a tiny worked example with small numbers first, then apply it.
3. **Why the right choice is right.** Name the choice by its content (the value or the word). Show a quick check.
4. **Why each wrong choice is wrong.** One line per wrong choice. Name the real mistake that produces it.

Rules:
- Name choices by their content, never by a letter (letters change after shuffling; see 8.2).
- No new jargon in the Reveal. If you must use a term, it goes in step 1.
- Target length: 60–150 words.

### 5.1 "Simpler than" benchmark

GT found this explanation confusing: a block-sum item (1 + 2 + … + 15 = 120; find 16 + 17 + … + 30) explained through "shifted pairs". Every Civio Reveal must be at least as plain as this rewrite of that explanation:

> **Shortcut:** Line the two lists up. 16 sits under 1. 17 sits under 2. Each bottom number is the top number plus 15.
> There are 15 numbers. Each one is 15 bigger. So the new sum is 15 × 15 = 225 bigger.
> 120 + 225 = 345.

That is the bar: three short lines, no algebra words, one check.

---

## 6. Item metadata fields

| Field | Type | Rule |
|---|---|---|
| `id` | string | Stable, never reused. Format `CIVIO-<DOMAIN>-<ARCHETYPE>-<6 digits>`, for example `CIVIO-NUM-WP-AVERAGE-000001` |
| `track` | enum | `pro`, `sub`, `both` |
| `domain` | enum | `general_information`, `verbal_en`, `verbal_fil`, `numerical`, `analytical`, `clerical` |
| `competency` | string | Official CSC topic from Section 1.2 (for example "Word problems") |
| `concept` | string | The idea tested (for example "average") |
| `micro_skill` | string | The exact move (for example "find a missing value to reach a target average") |
| `archetype` | string | Code from Section 3 |
| `difficulty` | enum | `easy`, `medium`, `hard` (Section 3.0) |
| `est_seconds` | integer | Target time from the archetype table |
| `language` | enum | `en`, `fil` |
| `stem` | string | UTF-8 text |
| `options` | array | Exactly 4 objects: `{option_id, text}` |
| `answer_option_id` | string | The `option_id` of the right choice. Never a letter or index |
| `reveal` | object | `{terms, shortcut, why_correct, why_wrong: {option_id: text}}` |
| `distractor_reasoning` | object | `{option_id: distractor_code}` for each wrong choice |
| `distractor_subreason` | object | Filing items only (v0.1.4): `{option_id: "CLR-… : breaks ARMA Rule N (…)"}`; the parent code in `distractor_reasoning` is `CLR-FILE-ORDER` |
| `source` | string | GI: article/section citation. Others: "Original, Civio" plus any rule cited (for example "Civio Filing Rules v1, Rule 3") |
| `provenance` | object | `{author, method: human or ai_assisted, created_at, spec_version}` |
| `status` | enum | `draft`, `curated`, `generated`, `reviewed`, `approved`, `deprecated` |
| `review_status` | enum | `unreviewed`, `in_review`, `changes_requested`, `passed`, `failed` |
| `reviewer` | string | Who reviewed |
| `reviewed_at` | datetime | With time zone |
| `notes` | string | Optional |

Status meanings:
- `draft`: a new Civio item waiting for review (section 10, item 6). Never shown to users. (added v0.1.3, CoS)
- `curated`: hand-written by GT or a named human from official sources.
- `generated`: drafted by a tool or AI. Never shown to users.
- `reviewed`: passed the checklist in Section 7 by a reviewer other than the author.
- `approved`: GT (or delegate) approved for users.
- `deprecated`: retired. Kept for history. Never shown.

Only `approved` items reach users.

---

## 7. Quality checklist (every item, before it enters the bank)

An item enters the bank only if every box is ticked.

**Content**
- [ ] Matches an official topic in Section 1.2 and the right `track`.
- [ ] Uses a named archetype from Section 3.
- [ ] Original: no situation, number, name, or wording from any outside item.
- [ ] Exactly one defensible answer (checked by a second person).
- [ ] Four choices; each wrong choice has a distractor code and is a real mistake.
- [ ] No "all/none of the above"; "cannot be determined" only where allowed.
- [ ] Stem has no definitions or hints.
- [ ] Target word or name is marked in text, not by formatting only.
- [ ] Numerical work is hand-solvable within target time; answer recomputed by reviewer.
- [ ] GI: fact matches the cited article/section; citation is in `source`.
- [ ] Filipino words checked in a standard dictionary.

**Reveal**
- [ ] Four parts in the right order.
- [ ] Names choices by content, not letters.
- [ ] Shortcut is short; tiny example included if the trick is abstract.
- [ ] Every wrong choice explained with its real mistake.
- [ ] As plain as the benchmark in 5.1.

**Technical**
- [ ] `answer_option_id` matches one `option_id`.
- [ ] `distractor_reasoning` and `why_wrong` cover the other three `option_id`s.
- [ ] Encoding check passes (8.1).
- [ ] Shuffle test passes (8.2).
- [ ] All metadata fields filled.

### 7.1 Approval gate and batch rule

- **No bulk writer** (script, AI batch, or contractor) may run until **GT or the Chief of Staff approves this spec in writing**.
- After approval, the **first batch is small: 10 items** (suggested: 3 Numerical, 3 Verbal, 2 GI, 1 Analytical, 1 Clerical).
- That batch is reviewed item by item. Fix the spec if needed. Only then may a larger batch start.
- Every later batch keeps a spot-check: at least 1 in 5 items re-reviewed by GT or a delegate.

---

## 8. Known bank bugs to avoid

### 8.1 Math operators lost as "??" (encoding)

Cause: text passed through a non-UTF-8 step (for example a Windows tool writing ANSI or UTF-16, or a database column not set to full UTF-8). Characters like ×, ÷, −, ₱, ñ become "?" or "??".

Rules:
- UTF-8 end to end: source files, scripts, API, database (for MySQL use `utf8mb4`), and export.
- On Windows, always set the encoding explicitly when reading or writing files. Do not rely on the default.
- Validation rejects any item whose text contains "??", the replacement character (U+FFFD), or a lone "?" between two numbers.
- Round-trip test before each import: write and read back a test string containing × ÷ − ₱ ñ é ≤ ≥ ½ and compare byte for byte.

### 8.2 Reveal marks the wrong choice after option shuffle

Cause: the answer was stored as a letter or position ("C"), then the options were shuffled.

Rules:
- Store the answer as `answer_option_id` only. Never a letter or index.
- `why_wrong` and `distractor_reasoning` are keyed by `option_id`.
- Reveal text never says "A", "B", "choice C", and so on. It names the choice by content.
- The screen maps `option_id` to the shown letter at display time.
- Test: shuffle each item 20 times; every time, the choice marked right in the Reveal must equal `answer_option_id`.

---

## 9. Worked sample items (2 only)

Both are fully original. They are examples of format, not bank entries. They are **not** inserted anywhere.

### 9.1 Sample 1: Numerical

- `id`: CIVIO-NUM-WP-AVERAGE-SAMPLE01 (sample, not in bank)
- `track`: both
- `domain`: numerical
- `competency`: Word problems
- `concept`: average
- `micro_skill`: find the missing value that reaches a target average
- `archetype`: NUM-WP-AVERAGE
- `difficulty`: medium (two steps, one trap)
- `est_seconds`: 60
- `language`: en
- `source`: Original, Civio
- `status`: generated (sample) / `review_status`: unreviewed

**Stem:**
A health center recorded an average of 35 patient visits per day for 4 days. How many visits must it record on the 5th day so that the 5-day average becomes 37?

| option_id | text | shown as |
|---|---|---|
| n1 | 37 | A |
| n2 | 39 | B |
| n3 | 45 | C |
| n4 | 47 | D |

`answer_option_id`: n3

`distractor_reasoning`: n1 = `NUM-GIVEN-REUSED`; n2 = `NUM-PARTIAL`; n4 = `NUM-OFF-BY-ONE`

**Reveal**

1. *Meaning.* "Average" means share equally. An average of 35 for 4 days is the same as 35 on each day.
2. *Shortcut: count what is missing.*
   Tiny example first. Two quizzes average 8. You want a 3-quiz average of 9. Each old quiz is 1 short of 9. That is 2 short in all. So quiz 3 = 9 + 2 = 11.
   Now this item. Each of the 4 days is 2 short of 37. That is 8 short in all. So day 5 = 37 + 8 = 45.
3. *Why 45 is right.* Check: 4 × 35 = 140. 140 + 45 = 185. 185 ÷ 5 = 37. ✓
4. *Why the others are wrong.*
   - 37: This is just the new average. It forgets the first 4 days are short.
   - 39: This adds the 2-visit gap only once, not once for each of the 4 days.
   - 47: This counts 5 short days (5 × 2 = 10). But only the first 4 days are short.

### 9.2 Sample 2: Verbal (English)

- `id`: CIVIO-VEN-ERROR-AGREE-SAMPLE02 (sample, not in bank)
- `track`: both
- `domain`: verbal_en
- `competency`: Sentence completion (grammar and correct usage)
- `concept`: subject-verb agreement
- `micro_skill`: ignore the phrase between subject and verb
- `archetype`: VEN-ERROR-AGREE
- `difficulty`: medium (one trap: plural nouns right before the blank)
- `est_seconds`: 30
- `language`: en
- `source`: Original, Civio
- `status`: generated (sample) / `review_status`: unreviewed

**Stem:**
The schedule for the vaccination teams in the two districts ______ updated every Friday.

| option_id | text | shown as |
|---|---|---|
| v1 | is | A |
| v2 | are | B |
| v3 | were | C |
| v4 | have been | D |

`answer_option_id`: v1

`distractor_reasoning`: v2 = `VEN-NEAREST-NOUN`; v3 = `VEN-TENSE`; v4 = `VEN-NEAREST-NOUN` (plus `VEN-TENSE`)

**Reveal**

1. *Meaning.* The subject is who or what the sentence is about. The verb tells what it is or does. Singular means one. Plural means more than one.
2. *Shortcut: cover the middle.* Hide the words that start with "for", "of", "in", or "with". Read what is left.
   Tiny example first. "The bag of apples ___ heavy." Hide "of apples". "The bag ___ heavy." One bag, so "is".
   Now this item. Hide "for the vaccination teams in the two districts". Left: "The schedule ___ updated every Friday."
3. *Why "is" is right.* "Schedule" is one thing, so it takes a singular verb. "Every Friday" is a regular habit, so present tense fits.
4. *Why the others are wrong.*
   - "are": It matches "teams" or "districts", the plural nouns near the blank. They are not the subject.
   - "were": It is plural, and it is past tense. "Every Friday" calls for present tense.
   - "have been": It is a plural form. It also changes the time meaning.

---

## 10. Decisions (approved by GT, 7 Oct 2026)

1. **GI term-match stems are allowed:** a plain-English description of the provision,
   the article and section cited in `source`, and sibling-term distractors. The
   no-teaching-in-stems rule still applies to every other subtest.
2. **Practice mixes are Civio choices, never CSC weights,** and will be recalibrated
   with data:

   | Subtest | Mix (%) |
   | --- | --- |
   | Numerical | operations 30 / sequence 20 / word problems 50 |
   | Verbal (English) | meaning 15 / completion 20 / error 20 / structure 10 / paragraph organization 15 / reading 20 |
   | Verbal (Filipino) | synonym 25 / antonym 20 / idiom 15 / grammar 15 / reading 15 / paragraph order 10 |
   | Analytical | analogy 30 / symbolic logic 20 / assumptions and conclusions 25 / data interpretation 25 |
   | Clerical | filing 55 / spelling 45 |
   | General Information | Constitution 40 / RA 6713 35 / peace and human rights 15 / environment 10 |

3. **Civio Filing Rules v1.** Every filing item cites its rule number; disputed
   cases wait for v1.1.
   1. Surname first.
   2. Letter by letter.
   3. Prefixes are part of the surname.
   4. Titles and suffixes only break ties.
   5. A leading "The" is ignored.
4. **The first release is text only.** Text tables are fine. Figures and charts wait
   for an image pipeline with alt text and a text fallback.
5. **Item review:** the CSE author writes; the Chief of Staff reviews against the
   Section 7 checklist (Codex as alternate); GT approves item by item, then
   spot-checks 1 in 5. The first batch is 10 items: 3 Numerical, 3 Verbal, 2 GI,
   1 Analytical, 1 Clerical (spelling).

New items get `questions.source_group = civio` and `status = draft` until GT approves
them (see `docs/QUESTION_SOURCE_GROUPS.md`).

*End of spec.*

## 10.1 Civio Filing Rules v1: CSC source check (v0.1.2, 2026-10-13; superseded by 10.2)

**Condition from Chief of Staff (GT delegated Civio decisions):** every rule in Civio Filing Rules v1 must cite a CSC source link; any rule without one is dropped.

**What CSC publishes:** CSC exam announcements list "Clerical Ability (in English): Filing; Spelling" as a Sub-Professional test area, and nothing more. For example, Examination Announcement No. 05, s. 2025: https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2025/Examination%20Announcement%20No.%2005%20s.%202025.pdf . CSC does not publish a filing or alphabetizing rulebook. The fallback, NAP General Circular No. 1 (records management, https://nationalarchives.gov.ph/downloads/nap-general-circular-1-2-and-grds/), only defines "file" and gives no alphabetical-filing rules. It is also not a CSC source.

| # | Rule | CSC source link | Status |
| --- | --- | --- | --- |
| 1 | Surname first | None (CSC only names "Filing" as scope) | **Dropped** |
| 2 | Letter by letter | None | **Dropped** |
| 3 | Prefixes are part of the surname | None | **Dropped** |
| 4 | Titles/suffixes only break ties | None | **Dropped** |
| 5 | Leading "The" ignored | None | **Dropped** |

**Effect:** Civio Filing Rules v1 has no rules in force. Write no filing items (CLR-FILE-*) and put none in the bank until CoS rules on a source standard that is not from CSC. Clerical spelling items are unaffected. The CSC announcement link above stays the scope citation for the Clerical "Filing" area.

## 10.2 Civio Filing Rules v2: ARMA simplified rules (v0.1.3, 2026-10-13)

**Chief of Staff ruling (GT delegated Civio decisions), 2026-10-13:** CSC publishes no filing rulebook (see 10.1), so ARMA International's Simplified Filing Standard Rules (alphabetic filing) are the approved source. Civio Filing Rules v2 replace v1 and the 10.1 drop. Each rule cites ARMA.

**Sources (checked on the web 2026-10-13):**
- [A1] ARMA International, *Alphabetic Filing Rules*, ANSI/ARMA 1-1995 (3rd ed.). Listing: https://webstore.ansi.org/standards/arma/ansiarma1995
- [A2] ARMA International, *Establishing Alphabetic, Numeric and Subject Filing Systems*, ANSI/ARMA 12-2005 (ARMA: "contains standard rules for indexing alphabetic data"). Listings: https://webstore.ansi.org/standards/arma/ansiarma122005 and https://www.pathlms.com/arma-international/courses/57497 . ARMA's standards page: https://www.arma.org/general/custom.asp?page=standards
- Note: A1 and A2 are paid documents, and I found no ARMA-hosted free copy of the "Simplified Filing Standard Rules". The rule numbers and wording below were checked against public reproductions that cite ARMA, for example https://www.slideserve.com/dane-keller/arma-filing-rules . Check against a licensed copy of A2 before you rely on a fine point.

| # | Civio rule (ARMA simplified rule) | Citation |
| --- | --- | --- |
| 1 | **Indexing order of units.** Personal names: surname, then given name, then middle name or initial. Business names: as written. Compare unit by unit, letter by letter; "nothing comes before something" (Baker before Bakersly). | ARMA Simplified Filing Standard Rules, Rule 1 [A2] |
| 2 | **Minor words and symbols in business names.** Articles, prepositions, conjunctions and symbols (&, %, $) are separate units; a symbol is indexed as if spelled out. "The" as the first word is the last unit. | Rule 2 [A2] |
| 3 | **Punctuation and possessives.** Ignore all punctuation; a hyphenated name is one unit (Garcia-Lopez = GarciaLopez). | Rule 3 [A2] |
| 4 | **Single letters and abbreviations.** Initials in personal names are separate units. Abbreviated given names and nicknames are indexed as written. Business acronyms and abbreviations are indexed as written. | Rule 4 [A2] |
| 5 | **Titles and suffixes.** A title before a name (Dr., Atty., Engr.) or a seniority or professional suffix after it (Jr., III, CPA) is the last unit. Numeric suffixes file before alphabetic ones. | Rule 5 [A2] |
| 6 | **Prefixes, articles and particles.** A prefix (de, de la, del, Mac, Mc, O', San, Van) joins the part that follows into one unit (De la Cruz = DelaCruz, filed under D). | Rule 6 [A2] |
| 7 | **Numbers in business names.** Digits file before letters, in ascending order. Arabic numerals file before Roman numerals. Spelled-out numbers file alphabetically. Ignore ordinal endings (1st = 1). | Rule 7 [A2] |
| 8 | **Organizations and institutions.** Index the name as written on the letterhead. | Rule 8 [A2] |

**Reveal wording (required on every filing item):** "This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule N), not a rule published by the CSC." Every filing item cites its rule number in `source`, for example "Civio Filing Rules v2 / ARMA Rule 6".

**Still out until v2.1:** identical names filed by address and government-agency names (ARMA rules 9 and 10). I did not verify these against a source here.

## 10.3 CoS rulings on generated batches 002–011 (v0.1.4, 2026-10-13)

**Chief of Staff ruling (GT delegated Civio decisions), 2026-10-13.** Enforced by `scripts/batches/qa.py`.

1. **Tense cap.** Verb-tense items are at most 25% of Verbal (50 of 200) and at most 5 per batch. The rest of Verbal is spread across vocabulary in context, synonyms and antonyms, idioms, subject-verb agreement, prepositions, sentence completion, confused words, phrasal verbs and pronoun case.
2. **Frames.** Every syllogism type (chain, some, none) and every analogy type (function, part, synonym, degree, form) has at least 3 stem frames, each used with fresh content. No frame appears more than twice in one batch.
3. **Codes adopted.** `LOG-MISSED-NEEDED`, `VRB-SYNONYM-TRAP`, `VRB-ANTONYM-TRAP`. Synonym and antonym traps use the VRB codes, not `RC-OPPOSITE` (which stays for reading passages). Ordering items give each wrong choice its own code (`LOG-ORDER-SWAP`, `LOG-ORDER-REVERSED`, `LOG-IGNORED-CLUE`); one code on every wrong choice fails QA.
4. **Filing sub-reasons.** Filing distractors keep `CLR-FILE-ORDER` as the parent code. Each also gets a `distractor_subreason` that names the ARMA rule it breaks (for example "CLR-PREFIX-SPLIT: breaks ARMA Rule 6").
5. **Dedup.** Every new stem is checked against the baseline bank (the seed scripts in `scripts/`), all earlier batches and the dev DB: exact match and near match on normalized stems.
6. **Added the same day.** `LOG-ORDER-REVERSED`, `CLR-LETTER-ORDER` and `CLR-SPELL-CORRECT-FOIL` are approved; "which word is misspelled" items are back on. Thin topics get a floor: fractions and work rate at least 20 each, assumption/conclusion at least 15, with the room taken from topics over the per-batch cap. Every item that names a person is rescanned for pronouns that match the name.



## Historical build audit and release constraints (snapshot before concurrent approval metadata update)

NOTE: The audit text below was committed before the 4a996c2 bulk approval record and therefore contains outdated counts for passed/unreviewed items. Use the UPDATED STATUS in this master document and actual JSON metadata instead.

# Civio · Subprofessional Bank Build and Release Audit

Date: 13 October 2026  
Status: **Build changes committed; editorial review still required. Not deployed.**  
Independent CSE practice material. Civio is not endorsed by the Civil Service Commission.

## 1. Source of truth and scope

Official CSC Examination Announcement No. 03, s. 2026, Section F:  
https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf

**Subprofessional:** General Information in English; Verbal Ability in English and Filipino; Numerical Ability in English; and **Clerical Ability (filing, spelling)** in English. **Analytical Ability belongs to Professional, not Subprofessional.** No CSC-authored question bank is used. The CSC does not publish fixed weights for these subtests in that announcement. Minimum general passing rating is 80.00. Calculators are not allowed for the cited examination.

## 2. Existing question bank audit

Reviewed repository `Vincenzo-OPC/Civio` `docs/batches/batch-001.json` through `batch-011.json` before adding the supplements.

| Existing component | Items | Finding |
| --- | ---: | --- |
| Original batches 001–011 | 1,010 | 10 approved, 1,000 draft / unreviewed |
| Numerical | 303 | Broadest domain |
| Analytical, Professional only | 251 | Excluded from Subprofessional |
| Verbal, English | 203 | No Filipino in original batches |
| Clerical | 151 | Mostly spelling and alphabetic filing |
| General Information | 102 | Cites Constitution and R.A. 6713 only |
| Filipino Verbal | 0 | Material missing domain |
| Unique existing archetype codes | 34 | Risk of template repetition |
| Existing items marked Medium difficulty | 875 | 86.6% of bank, weak calibration |

Exact stem and ID duplicate scans of the original 1,010 items found none; initial four-choice/reference checks found none invalid. These are **structural checks, not content approval**, and do not confirm that the answers are correct.

The earlier separate Deep Research report's 30-item prototype is **not imported**: it contained demonstrable incorrect keys, ties, ambiguous wording and unverified claims. Never activate it without rewriting and rechecking.

## 3. New authored content (all in Draft status)

| Source | Items | Purpose |
| --- | ---: | --- |
| `docs/research/filipino-supplement-001.json` | 80 | 24 vocabulary, 20 sentence completion, 10 sentence structure/grammar, 20 reading comprehension, 6 paragraph organization |
| `docs/research/subprofessional-general-info-supplement-001.json` | 30 | Primary-law-backed questions expanding environment and human rights |
| `docs/research/subprofessional-clerical-supplement-001.json` | 40 | 8 surname filing, 6 numerical filing, 6 chronological filing, 20 spelling |
| **Total new** | **150** | AI-assisted original practice items, **not** CSC past-paper questions |

**Bank repository inventory after this contribution: 1,160 question records; only 10 approved in the original batches, with 1,150 draft or unreviewed.** Source JSON files are not proof of DB import or live availability.

Question source URLs in the General Information supplement reference:
- 1987 Constitution: https://lawphil.net/consti/cons1987.html
- R.A. 9003: https://lawphil.net/statutes/repacts/ra2001/ra_9003_2001.html
- R.A. 8749: https://lawphil.net/statutes/repacts/ra1999/ra_8749_1999.html
- R.A. 9275: https://lawphil.net/statutes/repacts/ra2004/ra_9275_2004.html
- R.A. 9147: https://lawphil.net/statutes/repacts/ra2001/ra_9147_2001.html
- R.A. 9729: https://lawphil.net/statutes/repacts/ra2009/ra_9729_2009.html
- R.A. 11313: https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html

## 4. Security and editorial activation gate

`app/Console/Commands/ImportBatchCommand.php` now **rejects `--status=active` unless every item has BOTH `status=approved` and `review_status=passed`**. This also protects the default import mode, which previously implied `active`. The rejected import writes **zero** items. A regression test is in `tests/Feature/Bank/ImportBatchTest.php`.

The supplements additionally have a structural regression test in `tests/Feature/Bank/ResearchSupplementTest.php`. It validates counts, unique stems, unique IDs, four distinct options, a valid answer-option reference, unreviewed status, domain/track, and primary-law URL presence where required.

**Automated checks do not constitute independent legal, linguistic, or pedagogical review.** The new supplements have not passed the full generator-specific `scripts/batches/qa.py` semantic solver because they introduce new archetypes that the existing solver does not yet support. Treat all as drafts until that work is completed.

## 5. Next release operations

1. Run CI and all repo checks. Stop on any failure. Never deploy a red commit.
2. Complete a human Filipino-language pass, a primary-source legal fact check for all 30 GI items, and blind clerical checks. Correct answer keys, distractors and pedagogy where needed.
3. Add new archetype-specific independent solvers to `scripts/batches/qa.py`; check similarity beyond exact duplicate stems against baseline and all 11 batches.
4. Record `review_status=passed` and `status=approved` per **individual item** only after the reviewer approves it.
5. Use the existing importer to load drafts into a development DB only:
   ```bash
   php artisan civio:import-batch docs/research/filipino-supplement-001.json --status=draft
   php artisan civio:import-batch docs/research/subprofessional-general-info-supplement-001.json --status=draft
   php artisan civio:import-batch docs/research/subprofessional-clerical-supplement-001.json --status=draft
   ```
6. Re-run mock generation tests and confirm **Subprofessional excludes Analytical**, **Professional excludes Clerical**, and answer keys never reach clients before submission.
7. Only after editorial approval and green checks should reviewed items be promoted through the guarded importer. Do not activate the 1,000 older drafts indiscriminately.
8. Keep Netlify build credits unused: where deployment is eventually needed, build locally and use `netlify deploy --prod --no-build` for static assets; include `[skip netlify]` in connected repo commits. Do not deploy as part of this audit.

## 6. Claims not made

- This is **not** a 1,160-item vetted or publicly released bank. Only 10 original records have an approval flag, which is not an independent audit of their correctness.
- There is **no** claim that the items resemble actual 2026 confidential CSC questions.
- The Subprofessional exam blueprint proportions in the Civio app are product choices, not official CSC distributions.
- The independent 30-item research prototype is not accepted into the live question bank.

