# gap-fill-2000-04: Clerical filing (48) and R.A. 6713 (35) drafts, review request for Chief of Staff

Grok Bot, 2026-10-18 (Asia/Manila). File `docs/research/gap-fill-2000-04.json`. Generator `scripts/batches/gapfill/gap_fill_2000_04.py`, which reads `gf04_filing.py`, `gf04_filing_data.py` and `gf04_ra6713.py`. Every item is draft/unreviewed, and nothing is imported.

## Why

The 2,000 plan needs Clerical filing 165 and proposes an R.A. 6713 floor of 90 (§9 Q2, still open).

- **Filing.** The gap table (`gap-2000-2026-10-18.md`) puts filing at 124 of 165, so 41 short, counting the 30 baseline filing rows. On `main` alone, `release_manifest.py` sees 94 approved filing items.
- **R.A. 6713.** It sits at 58 after B3 against the proposed 90, so about 32 short. On `main` alone the manifest sees 48.

## Contents

**Clerical filing, 48 items** (41 needed, plus a 7-item buffer for rejects):
- **Archetypes:** {'CLR-FILE-BUSINESS': 22, 'CLR-FILE-ORDER': 8, 'CLR-FILE-POSITION': 18}.
- **ARMA rules targeted:** {'1': 2, '2': 7, '3': 6, '4': 7, '5': 6, '6': 8, '7': 7, '8': 5}.
- The weight is on Rules 2 to 8, per the §10.5 ruling on filing coverage. The bank's 58 approved CLR-FILE-POSITION items test only Rules 1, 5 and 6.
- Every item uses only Rules 1 to 8 of Civio Filing Rules v2. None uses Rules 9 or 10 (identical names, government agencies), which are still out until v2.1.
- Every Reveal carries the required ARMA sentence and cites ANSI/ARMA 12-2005.

**R.A. 6713, 35 items** (about 30 needed, plus a buffer). Each tests a provision the bank does not test yet:
- Sec. 3(a), (c), (d), (e), (f), (k)
- Sec. 4(B) and Sec. 5(c)
- Sec. 6: award criteria, members, promotion, forms
- Sec. 7(b): the post-separation practice bar on matters before the former office
- Sec. 7(d)(ii) and (iii), and the Ombudsman's regulations under it
- Sec. 8(A): exemptions, joint filing by spouses, and the filing offices for judges, local officials, AFP colonels and "all other" officials
- Sec. 8(C)(3) and (4), and Sec. 8(D)
- Sec. 9 (partners), Sec. 10(b), Sec. 11(a) suspension, 11(b), 11(c) and 11(d), Sec. 12 (Ombudsman protection), Sec. 13 and Sec. 17

## Standards and how they were checked

**Filing keys are computed twice:**
- `gf04_filing.py` indexes every name and derives the key.
- `scripts/batches/arma_solver.py` is a separate implementation, now wired into `qa.py` for newline-format filing stems. It recomputes every key, and all 48 agree.
- As a cross-check, the solver also reproduces the keys of the 3 CoS-approved CLR-FILE-ORDER items in `gap-fill-001.json`. Those items used to fail with "solver could not recompute the key".

**No disputed edge cases:**
- For business names, the build rejects any set where ARMA unit-by-unit order differs from plain letter-by-letter order. Sets with numbers are the exception, since Rule 7 decides those.
- No set mixes a title with a suffix in a tie.
- No name uses ñ.

**Distractors:**
- Every filing item has at least one distractor produced by a real misapplication of the targeted rule. Examples: "The" counted, & skipped, abbreviation spelled out, hyphen split, Mc read as Mac, digits compared as text, digits filed after letters, prefix split, given name first, title counted, organization filed under its key word.
- Each distractor has a `distractor_subreason` using approved codes only: CLR-PREFIX-SPLIT, CLR-FIRSTNAME-FIRST, CLR-TITLE-COUNTED, CLR-ARTICLE-COUNTED, CLR-LETTER-ORDER.
- No new codes are proposed.

**R.A. 6713 sources:**
- Every item carries `source_quote`, the exact LawPhil sentence it rests on, plus `fact_id` and `source` with the section number.
- On 2026-10-18 the build checked every quote verbatim against the live LawPhil page (https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html). All 35 matched.

**Balance:**
- Key positions: Clerical 12/12/12/12; R.A. 6713 9/8/9/9.
- R.A. 6713 key length rank: longest in 9 of 35 items, 2nd in 11, 3rd in 5, shortest in 10.

**QA:**
- `qa_file.py` 0 problems.
- `explanation_lint.py --strict` 0 flagged.
- `qa_all.py` QA GREEN.

## Reviewer focus

- **Filing edge rulings to confirm** (numbers are CLR-FILE IDs):
  - Rule 5: Roman-numeral suffixes file before Jr./Sr. (items 0022, 0023, 0025).
  - Rule 6: "San Juan" and "Sanjuan" index identically (0034).
  - Rule 3: "Lola's" files as LOLAS, after "Lola Kitchenette" (0011).
  - Rule 4: "Ma." and "Sto." are indexed as written, not as Maria or Santo (0016, 0018, 0020).
  - Rule 7: spelled-out numbers file as words, among the letters (0035, 0039, 0040).
- **R.A. 6713 judgment calls** (numbers are GI IDs):
  - 0002: Sec. 3(c) says an unsolicited insignificant gift is not a "gift". Is the scenario clear enough?
  - 0016: Sec. 7(d)(iii) does not say who issues waivers, so the Ombudsman distractor is wrong only because the head of office decides.
  - 0021: a municipal councilor is treated as a "local official".
  - 0035: the 15-day Civil Code distractor.
- **Topic mix:** if CoS keeps R.A. 6713 below 90 (§9 Q2), the R.A. 6713 items become the buffer and do not count toward the 2,000.
- Accept, revise or reject each ID.

## Item list

| ID | Type | ARMA rule | Key |
|---|---|---|---|
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0001 | BUSINESS | 2 | Goldfield Hardware |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0002 | BUSINESS | 2 | Santos & Garcia Law Office |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0003 | BUSINESS | 2 | The Mango Tree Café |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0004 | BUSINESS | 2 | Reyes Bicycle Shop |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0005 | BUSINESS | 2 | Pancit ni Aling Dely |
| CIVIO-GF2K04-CLR-FILE-ORDER-0006 | ORDER | 2 | 1, 3, 4, 2 |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0007 | BUSINESS | 2 | Lim Bakeshop |
| CIVIO-GF2K04-CLR-FILE-POSITION-0008 | POSITION | 3 | Teodoro S. Reyes |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0009 | BUSINESS | 3 | Nena Printing |
| CIVIO-GF2K04-CLR-FILE-POSITION-0010 | POSITION | 3 | Carlos M. Cruz-Manalo |
| CIVIO-GF2K04-CLR-FILE-ORDER-0011 | ORDER | 3 | 2, 4, 1, 3 |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0012 | BUSINESS | 3 | Kata Surf School |
| CIVIO-GF2K04-CLR-FILE-POSITION-0013 | POSITION | 3 | Gloria R. Santos-Ocampo |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0014 | BUSINESS | 4 | Santos Clinic |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0015 | BUSINESS | 4 | Mt. Apo Tours |
| CIVIO-GF2K04-CLR-FILE-POSITION-0016 | POSITION | 4 | Ma. Teresa L. Gomez |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0017 | BUSINESS | 4 | Sison Printing |
| CIVIO-GF2K04-CLR-FILE-POSITION-0018 | POSITION | 4 | Maria A. Valdez |
| CIVIO-GF2K04-CLR-FILE-ORDER-0019 | ORDER | 4 | 4, 2, 1, 3 |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0020 | BUSINESS | 4 | Sto. Tomas Lumber |
| CIVIO-GF2K04-CLR-FILE-POSITION-0021 | POSITION | 5 | Engr. Alfredo T. Ilagan |
| CIVIO-GF2K04-CLR-FILE-POSITION-0022 | POSITION | 5 | Jose R. Lim II |
| CIVIO-GF2K04-CLR-FILE-POSITION-0023 | POSITION | 5 | Danilo P. Aquino Sr. |
| CIVIO-GF2K04-CLR-FILE-POSITION-0024 | POSITION | 5 | Hon. Imelda B. Navarro |
| CIVIO-GF2K04-CLR-FILE-ORDER-0025 | ORDER | 5 | 3, 4, 1, 2 |
| CIVIO-GF2K04-CLR-FILE-POSITION-0026 | POSITION | 5 | Dr. Corazon L. Salvador |
| CIVIO-GF2K04-CLR-FILE-POSITION-0027 | POSITION | 6 | Andres P. De Vera |
| CIVIO-GF2K04-CLR-FILE-POSITION-0028 | POSITION | 6 | Liza M. Valencia |
| CIVIO-GF2K04-CLR-FILE-POSITION-0029 | POSITION | 6 | Felipe N. McKinley |
| CIVIO-GF2K04-CLR-FILE-POSITION-0030 | POSITION | 6 | Rodrigo P. Ocampo |
| CIVIO-GF2K04-CLR-FILE-POSITION-0031 | POSITION | 6 | Corazon P. Delgado |
| CIVIO-GF2K04-CLR-FILE-ORDER-0032 | ORDER | 6 | 3, 2, 1, 4 |
| CIVIO-GF2K04-CLR-FILE-POSITION-0033 | POSITION | 6 | Maria T. Reyes |
| CIVIO-GF2K04-CLR-FILE-POSITION-0034 | POSITION | 6 | Eduardo M. Juanico |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0035 | BUSINESS | 7 | 8 Stars Printing |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0036 | BUSINESS | 7 | Alpha Travel Agency |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0037 | BUSINESS | 7 | 100 Islands Resort |
| CIVIO-GF2K04-CLR-FILE-ORDER-0038 | ORDER | 7 | 2, 3, 1, 4 |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0039 | BUSINESS | 7 | 40 Hands Crafts |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0040 | BUSINESS | 7 | 20 Pesos Store |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0041 | BUSINESS | 7 | Sixto Hardware |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0042 | BUSINESS | 8 | Samahan ng Tsuper ng Davao |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0043 | BUSINESS | 8 | Kapit-Bisig Foundation |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0044 | BUSINESS | 8 | Association of Rice Traders |
| CIVIO-GF2K04-CLR-FILE-ORDER-0045 | ORDER | 8 | 1, 3, 4, 2 |
| CIVIO-GF2K04-CLR-FILE-BUSINESS-0046 | BUSINESS | 8 | Nightingale Nursing Review |
| CIVIO-GF2K04-CLR-FILE-POSITION-0047 | POSITION | 1 | Victoria A. Tolentino |
| CIVIO-GF2K04-CLR-FILE-ORDER-0048 | ORDER | 1 | 3, 4, 2, 1 |

| ID | Section | Key |
|---|---|---|
| CIVIO-GF2K04-GI-TERM-MATCH-0001 | Sec. 3(a) | Government-owned or controlled corporations and their subsidiaries |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0002 | Sec. 3(c) | It falls outside the Act's definition of a "gift" |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0003 | Sec. 3(c) | A gift, because a simulated sale falls under the term |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0004 | Sec. 3(d) | No; it is still "receiving any gift" since the value is not nominal |
| CIVIO-GF2K04-GI-TERM-MATCH-0005 | Sec. 3(e) | Simple loan, commodatum, and guarantees or financing arrangements |
| CIVIO-GF2K04-GI-TERM-MATCH-0006 | Sec. 3(f) | One who owns enough shares to elect a director |
| CIVIO-GF2K04-GI-DEADLINE-NUMBER-0007 | Sec. 3(k) | Fourth civil degree of consanguinity or affinity |
| CIVIO-GF2K04-GI-TERM-MATCH-0008 | Sec. 4(B) | Merit increases beyond regular progression steps |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0009 | Sec. 5(c) | The official next-in-rank or the officer in charge |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0010 | Sec. 6 | The Chairman of the Commission on Audit |
| CIVIO-GF2K04-GI-TERM-MATCH-0011 | Sec. 6 | The obscurity of the position |
| CIVIO-GF2K04-GI-TERM-MATCH-0012 | Sec. 6 | Automatic promotion to the next higher position |
| CIVIO-GF2K04-GI-TERM-MATCH-0013 | Sec. 6 | Directorships in government-owned or controlled corporations |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0014 | Sec. 7(b) | No; for one year the lawyer cannot practice on matters before the former office |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0015 | Sec. 7(d) | It may be accepted, because Congress consents to fellowship grants |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0016 | Sec. 7(d) | Permission from the head of the engineer's office |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0017 | Sec. 7(d) | The Ombudsman |
| CIVIO-GF2K04-GI-TERM-MATCH-0018 | Sec. 8(A) | Laborers and casual or temporary workers |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0019 | Sec. 8(A) | Jointly or separately, as they choose |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0020 | Sec. 8(A) | The Court Administrator |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0021 | Sec. 8(A) | The Deputy Ombudsman for that region |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0022 | Sec. 8(A) | The Office of the President |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0023 | Sec. 8(A) | The Civil Service Commission |
| CIVIO-GF2K04-GI-TERM-MATCH-0024 | Sec. 8(C) | A reasonable fee for reproduction, mailing and certification |
| CIVIO-GF2K04-GI-DEADLINE-NUMBER-0025 | Sec. 8(C) | 10 years |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0026 | Sec. 8(D) | No; commercial use is barred, except news reporting by the media |
| CIVIO-GF2K04-GI-DEADLINE-NUMBER-0027 | Sec. 11(d) | ₱25,000 |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0028 | Sec. 9 | Yes; the same rule applies to a partner in a partnership |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0029 | Sec. 10(b) | The member is not subject to any sanction under the Act |
| CIVIO-GF2K04-GI-DEADLINE-NUMBER-0030 | Sec. 11(a) | One year |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0031 | Sec. 11(b) | Yes; proof in the administrative case is sufficient cause |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0032 | Sec. 11(c) | The same penal liabilities as the officer, tried jointly |
| CIVIO-GF2K04-GI-WHO-HOLDS-POWER-0033 | Sec. 12 | The Ombudsman |
| CIVIO-GF2K04-GI-SCENARIO-APPLY-0034 | Sec. 13 | No; the Act does not derogate from more stringent standards |
| CIVIO-GF2K04-GI-DEADLINE-NUMBER-0035 | Sec. 17 | 30 days after publication is completed in the Official Gazette or two newspapers |
