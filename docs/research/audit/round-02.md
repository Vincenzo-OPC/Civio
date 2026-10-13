# Audit round 02: Subprofessional parts of batches 001-011 (759 items)

Scope: clerical 151, Verbal EN 203, GI 102, Numerical 303. These were already approved by Chief of Staff. Content findings are proposals for CoS; I made only one metadata change, which follows the §10.4 ruling.

Method:
- `qa_all.py` green: every key recomputed by its solver, exactly one right answer, no duplicates against the baseline or within the batches, and GI quotes matched against official text.
- Clerical: a script compared each spelling Reveal's stated error type with the actual error.
- Frame and answer-position counts for every domain.
- A manual read of 8 random items each from Verbal, Numerical and GI, plus every clerical item.

## Results

| Domain | Items | Key correct | Content fail | Fix proposed (CoS decision) |
|---|---|---|---|---|
| Clerical | 151 | 151 | 0 | ~25 spelling items (realism) and 2 Reveal labels |
| Verbal EN | 203 | 203 | 0 | frame repetition |
| GI | 102 | 102 | 0 | none |
| Numerical | 303 | 303 | 0 | frame repetition |

## Applied (metadata only, per §10.4 rule 3)

- 58 alphabetic-filing items: added "Source standard: ANSI/ARMA 12-2005." to `why_correct`.
- The batch `.md` files were re-rendered from the JSON. They had also been showing the old draft status.

## Issues for CoS

1. **Unrealistic misspellings (clerical).** About 25 misspelled forms look like keyboard typos rather than real spelling traps. Examples:
   - parliamnt, liison, pronnciation, harss, licnse, commttee, indepndence, threshld, grivance, persnnel, recmmend, occrrence, inoculte, conscence, irrelvant, beginnng, seze, beleve, maintennce, millnnium, accessble, occsionally, questonnaire, indpendence
   - Real CSE traps look like *seperate, recieve, occurence, accomodate, priviledge*.
   - **Proposal:** replace each with a common real misspelling. The same applies to typo-style distractors in "spelled correctly" items, such as calndar, schdule, allotmnt and acknwledgment.
2. **Reused words.** The same misspelling appears across batches, for example:
   - indepndence ×3
   - unanimus, consceince/conscince, occsionally, beginnng, foregn/forreign, pronnciation, notticeable, defintely, liison, recmmend, occrrence, collague, separrate, acquaintence, phenomnon ×2
   - **Proposal:** dedupe at the word level.
3. **Reveal error-type labels.** CIVIO-CLR-SPELL-WRONG-000194 (privilej) and 000195 (unanimus) say "sound", but the error is a dropped letter. These are minor.
4. **Filing coverage.** The 58 filing items use only ARMA Rules 1, 5 and 6, all with one stem frame ("In alphabetical filing, which name is filed FIRST/LAST?"). Rules 2, 3 and 7 are now covered by gap-fill-001 and gap-fill-002.
5. **Verbal frame repetition.** 89 of 203 items use "Choose the word that best completes the sentence". There are no reading-comprehension, paragraph-organization or sentence-form error-recognition items; gap fills 001 and 002 add these.
6. **Numerical frame repetition.** For example, 30 items use "What is the value of N + N × N − N?", and the discount items share one frame. **Proposal:** extend the §10.3 frame rule (at least 3 frames, at most 2 uses per batch) to numerical.
7. **Minor.** CIVIO-VEN-…-000875: "Next month, Arnel ____ the plaza." The distractor "will have cleaned" is close to acceptable without "By". **Proposal:** add "By" to a different distractor stem, or replace that distractor.

GI: in the sample, every item matched the Constitution or R.A. 6713, including Art. VI, Sec. 4 (two consecutive terms), Art. VIII, Sec. 7(1) (age 40), Art. XI, Sec. 8 (7 years without reappointment), Art. VII, Sec. 18 (60 days) and R.A. 6713, Sec. 11 (5 years).

## Gap fill 002

`docs/research/gap-fill-002.json`: 14 original drafts.
- 5 English error-recognition items in sentence form, using VEN-* codes
- 6 fractions and decimals items, all computed by hand
- 3 business-name filing items: ARMA Rule 2 ("The" last), Rule 7 (digits first, ascending), and Rule 3 (hyphenated names are one unit)

Each has a coded distractor and a why-wrong line for every wrong option. They pass the importer's dry run and have no baseline or batch duplicates.
