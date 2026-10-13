# Civio batch 002 (draft for Chief of Staff review)

Spec: `docs/CSE-Question-Design-Spec.md` v0.1.3. Author: CSE (Grok Bot, AI-assisted). Reviewer: Chief of Staff (not the author).
All items are original, `source_group: civio`, `status: draft`, `review_status: unreviewed`. Not imported into any database. Seed-ready copy: `docs/batches/batch-002.json` (import after approval with `php artisan civio:import-batch`).
Civio is an independent reviewer and is not affiliated with the Civil Service Commission.

Mix: 4 Numerical, 4 Analytical (Professional), 1 Verbal (English), 1 General Information.

## 1. CIVIO-NUM-WP-RATE-000011

- track: both · domain: numerical · archetype: NUM-WP-RATE · difficulty: medium · est: 90 s
- competency: Word problems · concept: work rate
- micro_skill: add two work rates to find the time working together
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** Liza can encode a box of survey forms in 6 hours. Ramon can encode the same box in 3 hours. If they work together, how long will it take them to encode one box?

| option_id | text | shown as |
|---|---|---|
| n1 | 30 minutes | A |
| n2 | 2 hours | B |
| n3 | 4 hours 30 minutes | C |
| n4 | 9 hours | D |

`answer_option_id`: n2 (2 hours)

`distractor_reasoning`: n1 = `NUM-PARTIAL`; n3 = `NUM-WRONG-BASE`; n4 = `NUM-OP-SWAP`

**Reveal**

1. *Meaning.* A "rate" is how much work gets done in one hour.
2. *Shortcut.* Turn each time into "part of the job per hour", then add. Liza does 1/6 of the box each hour. Ramon does 1/3, which is 2/6. Together they do 3/6 = 1/2 of the box each hour. Half a box per hour means one box takes 2 hours.
3. *Why it is right.* 2 hours is right. Check: in 2 hours Liza does 2/6 = 1/3 and Ramon does 2/3. 1/3 + 2/3 = 1 whole box.
4. *Why the others are wrong.*
   - 30 minutes: 30 minutes reads the rate "1/2 box per hour" as "1/2 hour". It stops before turning the rate back into time.
   - 4 hours 30 minutes: 4 hours 30 minutes is the average of 6 and 3. Working together is faster than either person alone, so the answer must be under 3 hours.
   - 9 hours: 9 hours adds the two times. You add the rates, not the times.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 2. CIVIO-NUM-WP-AVERAGE-000012

- track: both · domain: numerical · archetype: NUM-WP-AVERAGE · difficulty: medium · est: 60 s
- competency: Word problems · concept: average
- micro_skill: find the new average after one value is added
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** The average age of the 5 staff members in a municipal library is 32. A new librarian who is 44 years old joins them. What is the new average age of the 6 staff members?

| option_id | text | shown as |
|---|---|---|
| a1 | 34 | A |
| a2 | 34.4 | B |
| a3 | 38 | C |
| a4 | 204 | D |

`answer_option_id`: a1 (34)

`distractor_reasoning`: a2 = `NUM-OFF-BY-ONE`; a3 = `NUM-WRONG-BASE`; a4 = `NUM-PARTIAL`

**Reveal**

1. *Meaning.* "Average" means share equally. An average age of 32 for 5 people is the same as all 5 being 32.
2. *Shortcut.* Share the extra years. The new person is 44 − 32 = 12 years above the old average. Those 12 extra years are shared by all 6 people now: 12 ÷ 6 = 2. So the average goes up by 2: 32 + 2 = 34.
3. *Why it is right.* 34 is right. Check the long way: 5 × 32 = 160. 160 + 44 = 204. 204 ÷ 6 = 34.
4. *Why the others are wrong.*
   - 34.4: 34.4 shares the 12 extra years among 5 people. After the new librarian joins there are 6 people.
   - 38: 38 is the average of 32 and 44. That treats the 5 old staff as if they were one person.
   - 204: 204 is the total of all 6 ages. It stops before dividing by 6.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 3. CIVIO-NUM-WP-PCT-CHANGE-000013

- track: both · domain: numerical · archetype: NUM-WP-PCT-CHANGE · difficulty: medium · est: 75 s
- competency: Word problems · concept: simple interest
- micro_skill: use interest = principal × rate × time with time in years
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** A cooperative member borrows ₱20,000 at 6% simple interest per year. How much interest will she owe after 2 years and 6 months?

| option_id | text | shown as |
|---|---|---|
| i1 | ₱2,400 | A |
| i2 | ₱3,000 | B |
| i3 | ₱3,120 | C |
| i4 | ₱23,000 | D |

`answer_option_id`: i2 (₱3,000)

`distractor_reasoning`: i1 = `NUM-PARTIAL`; i3 = `NUM-UNIT`; i4 = `NUM-EXTRA-STEP`

**Reveal**

1. *Meaning.* "Simple interest" is the extra money paid for borrowing. It is the same amount every year. "6% per year" means ₱6 for every ₱100, each year.
2. *Shortcut.* Find one year first, then multiply by the years. One year: 6% of ₱20,000 = ₱1,200. Six months is half a year, so 2 years and 6 months = 2.5 years. 2.5 × ₱1,200 = ₱3,000.
3. *Why it is right.* ₱3,000 is right. Check: 20,000 × 0.06 × 2.5 = 1,200 × 2.5 = 3,000.
4. *Why the others are wrong.*
   - ₱2,400: ₱2,400 counts only 2 years. It leaves out the 6 months.
   - ₱3,120: ₱3,120 uses 2.6 years. Six months is 0.5 of a year, not 0.6.
   - ₱23,000: ₱23,000 is the loan plus the interest. The question asks for the interest only.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 4. CIVIO-NUM-WP-ALGEBRA-000014

- track: both · domain: numerical · archetype: NUM-WP-ALGEBRA · difficulty: hard · est: 90 s
- competency: Word problems · concept: age problem
- micro_skill: set up 'times as old now' and 'twice as old later' and solve
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** Teresa is 3 times as old as her son. In 12 years, she will be twice as old as her son. How old is Teresa now?

| option_id | text | shown as |
|---|---|---|
| t1 | 12 | A |
| t2 | 24 | B |
| t3 | 36 | C |
| t4 | 48 | D |

`answer_option_id`: t3 (36)

`distractor_reasoning`: t1 = `NUM-OTHER-SHARE`; t2 = `NUM-OTHER-SHARE`; t4 = `NUM-EXTRA-STEP`

**Reveal**

1. *Meaning.* "3 times as old" means her age is her son's age multiplied by 3. "Twice" means multiplied by 2.
2. *Shortcut.* Try the choices instead of using algebra. Take each choice as Teresa's age now, divide by 3 for the son, add 12 to both, and see if she is twice his age. 36: son is 12. In 12 years: 48 and 24. 48 is twice 24.
3. *Why it is right.* 36 is right. Algebra check: son = s, Teresa = 3s. 3s + 12 = 2(s + 12), so 3s + 12 = 2s + 24, so s = 12 and Teresa = 36.
4. *Why the others are wrong.*
   - 12: 12 is the son's age now. The question asks for Teresa's age.
   - 24: 24 is the son's age 12 years from now.
   - 48: 48 is Teresa's age 12 years from now, not her age today.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 5. CIVIO-ANA-SYLLOGISM-000015

- track: pro · domain: analytical · archetype: ANA-SYLLOGISM · difficulty: medium · est: 60 s
- competency: Logic · concept: syllogism
- micro_skill: chain 'all A are B' and 'no B is C' to 'no A is C'
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** All records clerks in the provincial office are trained in filing. No employee trained in filing is a new hire. Which statement must be true?

| option_id | text | shown as |
|---|---|---|
| l1 | All employees trained in filing are records clerks. | A |
| l2 | No records clerk in the provincial office is a new hire. | B |
| l3 | Some employees who are not new hires are not records clerks. | C |
| l4 | No new hire works in the records section. | D |

`answer_option_id`: l2 (No records clerk in the provincial office is a new hire.)

`distractor_reasoning`: l1 = `LOG-CONVERSE`; l3 = `LOG-COULD-NOT-MUST`; l4 = `LOG-OVERSTRONG`

**Reveal**

1. *Meaning.* "Must be true" means it follows from the two statements alone, with no outside facts. "Could be true" is not enough.
2. *Shortcut.* Draw circles. The records-clerk circle sits inside the trained-in-filing circle. The new-hire circle sits outside the trained-in-filing circle. So the records-clerk circle cannot touch the new-hire circle.
3. *Why it is right.* "No records clerk in the provincial office is a new hire" is right. Every clerk is trained in filing, and nobody trained in filing is a new hire.
4. *Why the others are wrong.*
   - All employees trained in filing are records clerks.: This flips the first statement. "All clerks are trained" does not mean "all trained people are clerks".
   - Some employees who are not new hires are not records clerks.: This could be true, but nothing forces it. Every trained employee might be a records clerk.
   - No new hire works in the records section.: This goes too far. A new hire could work in the records section in a job other than records clerk, for example as a driver.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 6. CIVIO-ANA-ASSUME-I-II-000016

- track: pro · domain: analytical · archetype: ANA-ASSUME-I-II · difficulty: medium · est: 60 s
- competency: Assumptions and conclusions · concept: assumptions
- micro_skill: keep the assumption the plan needs and drop one that is only plausible
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** Statement: The municipal treasurer's office will stay open until 7 p.m. so that working residents can pay their real property tax after work.
Assumption I: Some residents cannot pay during regular office hours because of their work.
Assumption II: Staying open later will increase the town's total tax collection.
Which assumption is implicit in the statement?

| option_id | text | shown as |
|---|---|---|
| s1 | Only I | A |
| s2 | Only II | B |
| s3 | Both I and II | C |
| s4 | Neither I nor II | D |

`answer_option_id`: s1 (Only I)

`distractor_reasoning`: s2 = `LOG-IRRELEVANT`; s3 = `LOG-COULD-NOT-MUST`; s4 = `LOG-MISSED-NEEDED`

**Reveal**

1. *Meaning.* An "assumption" is an idea the speaker takes for granted without saying it. If the assumption were false, the plan would make no sense.
2. *Shortcut.* Use the "if not" test. Say the opposite of each assumption and ask: does the plan still make sense? If the plan falls apart, the assumption is needed.
3. *Why it is right.* "Only I" is right. If no resident had trouble paying during work hours, there would be no reason to open until 7 p.m. So I is needed. If collection stayed the same, the plan could still help residents pay more easily. So II is not needed.
4. *Why the others are wrong.*
   - Only II: II is not needed, and it leaves out I. The plan is about making payment convenient, not about raising more money.
   - Both I and II: II is reasonable, but the plan does not depend on it. A merely plausible idea is not an assumption.
   - Neither I nor II: I fails the "if not" test. Without it, the longer hours have no purpose.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 7. CIVIO-ANA-SYMBOL-SERIES-000017

- track: pro · domain: analytical · archetype: ANA-SYMBOL-SERIES · difficulty: medium · est: 50 s
- competency: Logic · concept: letter series
- micro_skill: find the growing gap between letter positions
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** What letter comes next in the series?  B, E, I, N, ___

| option_id | text | shown as |
|---|---|---|
| x1 | Q | A |
| x2 | S | B |
| x3 | T | C |
| x4 | U | D |

`answer_option_id`: x3 (T)

`distractor_reasoning`: x1 = `NUM-SEQ-OTHER-RULE`; x2 = `NUM-PARTIAL`; x4 = `NUM-OFF-BY-ONE`

**Reveal**

1. *Meaning.* A letter's "position" is its place in the alphabet: A = 1, B = 2, C = 3, and so on.
2. *Shortcut.* Change letters to numbers, then look at the jumps. B, E, I, N = 2, 5, 9, 14. The jumps are +3, +4, +5. The next jump is +6: 14 + 6 = 20, and the 20th letter is T.
3. *Why it is right.* T is right. Check by counting from N: O, P, Q, R, S, T is 6 steps.
4. *Why the others are wrong.*
   - Q: Q uses +3 every time, the first jump only. The jumps grow by 1.
   - S: S repeats the last jump, +5. The next jump should be +6.
   - U: U jumps +7. That skips a step in the growing jumps.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 8. CIVIO-ANA-ANALOGY-FUNCTION-000018

- track: pro · domain: analytical · archetype: ANA-ANALOGY-FUNCTION · difficulty: easy · est: 30 s
- competency: Word association (analogy) · concept: instrument : what it measures
- micro_skill: match tool-to-quantity-measured in the same order
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** THERMOMETER : TEMPERATURE :: ______

| option_id | text | shown as |
|---|---|---|
| f1 | odometer : distance | A |
| f2 | weight : scale | B |
| f3 | speedometer : car | C |
| f4 | ruler : pencil | D |

`answer_option_id`: f1 (odometer : distance)

`distractor_reasoning`: f2 = `ANA-REVERSED`; f3 = `ANA-OTHER-RELATION`; f4 = `ANA-SAME-TOPIC`

**Reveal**

1. *Meaning.* An "analogy" compares two pairs. The second pair must have the same link, in the same order.
2. *Shortcut.* Make a sentence for the first pair: "A thermometer measures temperature." Put each choice into the same sentence.
3. *Why it is right.* "Odometer : distance" is right. "An odometer measures distance." Same link, same order.
4. *Why the others are wrong.*
   - weight : scale: "Weight is measured by a scale" is the same link backwards. The measuring tool should come first.
   - speedometer : car: "A speedometer is found in a car." That is tool and where it is installed, not tool and what it measures.
   - ruler : pencil: A ruler and a pencil are both desk tools. Being on the same topic is not the same link.

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 9. CIVIO-VEN-ERROR-TENSE-000019

- track: both · domain: verbal_en · archetype: VEN-ERROR-TENSE · difficulty: medium · est: 35 s
- competency: Grammar and correct usage · concept: tense consistency
- micro_skill: match the verb to a past time signal
- source: Original, Civio
- status: draft · review_status: unreviewed

**Stem:** Which part of the sentence contains an error?  Last Friday, the new clerk / finishes encoding / all the leave forms / before the office closed.

| option_id | text | shown as |
|---|---|---|
| v1 | Last Friday, the new clerk | A |
| v2 | finishes encoding | B |
| v3 | all the leave forms | C |
| v4 | before the office closed | D |

`answer_option_id`: v2 (finishes encoding)

`distractor_reasoning`: v1 = `VEN-TENSE`; v3 = `VEN-NEAREST-NOUN`; v4 = `VEN-TENSE`

**Reveal**

1. *Meaning.* "Tense" tells when an action happens: past, present, or future. A "time signal" is a word like "last Friday" or "tomorrow".
2. *Shortcut.* Find the time signal first, then check every verb against it. "Last Friday" is past. So every action in the sentence should be past.
3. *Why it is right.* "Finishes encoding" is the error. It is present tense, but "last Friday" is past. It should be "finished encoding".
4. *Why the others are wrong.*
   - Last Friday, the new clerk: "Last Friday, the new clerk" is the time signal and the subject. It is correct, and it is what shows the other verb is wrong.
   - all the leave forms: "All the leave forms" is a correct plural object. Plural nouns do not change the verb tense.
   - before the office closed: "Before the office closed" is already in the past tense, which matches "last Friday".

Review: [ ] CoS pass  [ ] GT approve  Notes:

## 10. CIVIO-GI-DEADLINE-NUMBER-000020

- track: both · domain: general_information · archetype: GI-DEADLINE-NUMBER · difficulty: easy · est: 20 s
- competency: Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713) · concept: duties of public officials
- micro_skill: recall the deadline to answer letters from the public
- source: R.A. 6713, Sec. 5(a) (https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html)
- status: draft · review_status: unreviewed

**Stem:** Under R.A. 6713, within how many working days must public officials and employees respond to letters and requests sent by the public?

| option_id | text | shown as |
|---|---|---|
| d1 | 10 working days | A |
| d2 | 15 working days | B |
| d3 | 30 days | C |
| d4 | 45 working days | D |

`answer_option_id`: d2 (15 working days)

`distractor_reasoning`: d1 = `GI-NEIGHBOR-NUMBER`; d3 = `GI-NEIGHBOR-NUMBER`; d4 = `GI-NEIGHBOR-NUMBER`

**Reveal**

1. *Meaning.* "Working days" are office days. Weekends and holidays are not counted.
2. *Shortcut.* Link each number in the law to its job: 15 = answer the public's letters. 30 = file the SALN after taking office. 45 = agency's yearly performance report. 10 = when a filed SALN can be copied.
3. *Why it is right.* "15 working days" is right. R.A. 6713, Sec. 5(a) says officials and employees shall respond to letters and other communications from the public within fifteen working days from receipt, and the reply must state the action taken.
4. *Why the others are wrong.*
   - 10 working days: 10 working days is when filed SALNs become available for copying (Sec. 8(C)(2)), not the deadline to answer letters.
   - 30 days: 30 days is the deadline to file the SALN after taking office (Sec. 8(A)).
   - 45 working days: 45 working days is the deadline for an agency's annual performance report (Sec. 5(b)).

Review: [ ] CoS pass  [ ] GT approve  Notes:

## Checks done by the author

- Math, twice (by hand and asserted in the generator): item 11: 1/6 + 1/3 = 1/2 box per hour, so 2 h; in 2 h, 2/6 + 4/6 = 1. Item 12: 5 × 32 = 160, + 44 = 204, ÷ 6 = 34; also 32 + 12 ÷ 6 = 34. Item 13: 20,000 × 0.06 = 1,200 per year × 2.5 = 3,000. Item 14: s = 12, Teresa 36; in 12 years 48 = 2 × 24. Item 17: B, E, I, N = 2, 5, 9, 14; +6 gives 20 = T.
- GI text checked against the LawPhil copy of R.A. 6713: Sec. 5(a) (15 working days), Sec. 5(b) (45 working days), Sec. 8(A) (30 days), Sec. 8(C)(2) (10 working days).
- For CoS: item 16 uses the proposed code `LOG-MISSED-NEEDED` (not yet in the spec). Item 17 reuses the numerical series codes because section 3.4 has no series codes. Item 13 uses `NUM-WP-PCT-CHANGE` for simple interest, the closest listed archetype.
