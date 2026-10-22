# Review packet P4-numerical-01

Priority P4, domain numerical, 8 items. Status of every item: not approved.

**How to review independently:** answer every item below before opening the answer sheet. Then compare, and mark each item ACCEPT / FIX (say what) / REJECT in `decisions.csv` (one row per id). Do not edit the item files; the bank worker applies fixes as draft replacements.

**Check for this domain:** Solve it yourself first. Is exactly one option correct? Do the wrong options come from real mistakes? Does the method_steps explanation teach a no-calculator path?

## Items

### 1. `CIVIO-B3-NUM-SEQ-MULT-0190`  (both, easy, 30 s)

Continue the series 7, 14, 28, 56 with the next term.

- (A) 112
- (B) 84
- (C) 98
- (D) 70

### 2. `CIVIO-GF2K02-NUMOPS-0041`  (both, medium, 35 s)

Determine the value of 52 − 20 ÷ 4 + 3?

- (A) 50
- (B) 11
- (C) 47
- (D) 44

### 3. `CIVIO-GF2K02-NUMOPS-0047`  (both, medium, 35 s)

Calculate the value of 91 × (5 − 2) + 16?

- (A) 469
- (B) 273
- (C) 289
- (D) 110

### 4. `CIVIO-GF2K02-NUMOPS-0054`  (both, medium, 35 s)

Calculate the value of 2 × 12 ÷ (12 − 8)?

- (A) -6
- (B) 6
- (C) 24
- (D) 96

### 5. `CIVIO-NUM-WP-ALGEBRA-926051`  (subprofessional, medium, 90 s)

A training group prepares 3 identical sets of forms. Each set has x forms after 4 damaged forms are removed. If the three sets contain 24 usable forms in total, how many forms were in each set before the damaged forms were removed?

- (A) 8 forms
- (B) 12 forms
- (C) 4 forms
- (D) 28 forms

### 6. `CIVIO-NUM-WP-GEOM-000226-R1`  (both, medium, 75 s)

A rectangular parking area is 22 m long and 7 m wide. Edging costs ₱40 per meter. How much will it cost to put the edging around the whole parking area?

- (A) ₱6,160
- (B) ₱58
- (C) ₱2,320
- (D) ₱1,160

### 7. `CIVIO-NUM-WP-PCT-CHANGE-000221-R1`  (both, easy, 45 s)

An office chair is priced at ₱480. It is sold at 15% off. How much does a buyer pay?

- (A) ₱72
- (B) ₱408
- (C) ₱465
- (D) ₱552

### 8. `CIVIO-NUM-WP-RATE-000116-R1`  (both, medium, 90 s)

Nestor can paint a classroom in 21 hours. Aling Rosa can do the same job in 28 hours. Working together, how long will they take?

- (A) 12 hours
- (B) 24.5 hours
- (C) 49 hours
- (D) 7 hours

---

## Answer sheet (open only after answering)

### 1. `CIVIO-B3-NUM-SEQ-MULT-0190`: key (A) 112

- Why correct: Answer: 112. Multiply by 2: 56 × 2 = 112.
- (B) Added 28 (the previous term).
- (C) Added 42.
- (D) Added 14 (the first difference).
- File: `docs/research/audit/fixes/round-03-baseline-b3-drafts.json`

### 2. `CIVIO-GF2K02-NUMOPS-0041`: key (A) 50

- Why correct: Answer: 50. 20 ÷ 4 = 5; 52 − 5 = 47; 47 + 3 = 50.
- (B) 11 subtracts first: (52 − 20) ÷ 4 + 3. Division comes before subtraction.
- (C) 47 stops at 52 − 5 and forgets to add 3.
- (D) 44 subtracts 3 instead of adding it.
- File: `docs/research/gap-fill-2000-02.json`

### 3. `CIVIO-GF2K02-NUMOPS-0047`: key (C) 289

- Why correct: Answer: 289. 5 − 2 = 3; 91 × 3 = 273; 273 + 16 = 289.
- (A) 469 drops the parentheses and computes 91 × 5 − 2 + 16.
- (B) 273 stops at 91 × 3 and forgets to add 16.
- (D) 110 adds 91 instead of multiplying by 91.
- File: `docs/research/gap-fill-2000-02.json`

### 4. `CIVIO-GF2K02-NUMOPS-0054`: key (B) 6

- Why correct: Answer: 6. 2 × 12 = 24; 12 − 8 = 4; 24 ÷ 4 = 6.
- (A) -6 drops the parentheses and computes 2 × 12 ÷ 12 − 8.
- (C) 24 stops at 2 × 12 and forgets to divide by 4.
- (D) 96 multiplies by 4 instead of dividing.
- File: `docs/research/gap-fill-2000-02.json`

### 5. `CIVIO-NUM-WP-ALGEBRA-926051`: key (B) 12 forms

- Why correct: 12 forms is correct. Removing 4 from each original set leaves 8, and 3 × 8 = 24 usable forms.
- (A) 8 forms is the number left in each set after the damaged forms are removed, not the starting number.
- (C) 4 forms is the number removed from each set, not the number originally prepared.
- (D) 28 forms adds the four damaged forms only once to the total of 24 usable forms, then stops before dividing the usable total among 3 sets.
- File: `docs/research/batch-subpro-num-001.json`

### 6. `CIVIO-NUM-WP-GEOM-000226-R1`: key (C) ₱2,320

- Why correct: ₱2,320 is right: 58 m × ₱40 = ₱2,320.
- (A) This uses the area (154 square meters). Going around uses the perimeter.
- (B) ₱58 is just the perimeter in meters written as pesos. It stops before multiplying by ₱40.
- (D) This uses only one length and one width (29 m). A rectangle has two of each.
- File: `docs/research/audit/fixes/signoff-replacements-2026-10-22.json`

### 7. `CIVIO-NUM-WP-PCT-CHANGE-000221-R1`: key (B) ₱408

- Why correct: ₱408 is right. Check: discount ₱72; ₱480 − ₱72 = ₱408.
- (A) ₱72 is the discount itself. The buyer pays the price minus this amount.
- (C) ₱465 subtracts 15 pesos, not 15% of the price.
- (D) ₱552 adds 15% instead of taking it off.
- File: `docs/research/audit/fixes/signoff-replacements-2026-10-22.json`

### 8. `CIVIO-NUM-WP-RATE-000116-R1`: key (A) 12 hours

- Why correct: 12 hours is right. Check: in 12 hours, Nestor does 12/21 and Aling Rosa does 12/28; together that is 1 whole job.
- (B) 24.5 hours is the average of the two times. Together they must be faster than the faster person alone.
- (C) 49 hours adds the two times. Add the work done per hour, not the hours.
- (D) 7 hours subtracts the two times (28 − 21). Add the work done per hour; do not subtract the hours.
- File: `docs/research/audit/fixes/signoff-replacements-2026-10-22.json`

