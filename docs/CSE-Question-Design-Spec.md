# Civio CSE Question Design Spec

Version: 0.1
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
- `LOG-CONVERSE` reverses "all A are B"
- `LOG-COULD-NOT-MUST` possible but not forced
- `LOG-OVERSTRONG` "all/only/sole" where the text supports less
- `LOG-IRRELEVANT` true statement the argument does not need
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
| `source` | string | GI: article/section citation. Others: "Original, Civio" plus any rule cited (for example "Civio Filing Rules v1, Rule 3") |
| `provenance` | object | `{author, method: human or ai_assisted, created_at, spec_version}` |
| `status` | enum | `curated`, `generated`, `reviewed`, `approved`, `deprecated` |
| `review_status` | enum | `unreviewed`, `in_review`, `changes_requested`, `passed`, `failed` |
| `reviewer` | string | Who reviewed |
| `reviewed_at` | datetime | With time zone |
| `notes` | string | Optional |

Status meanings:
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
