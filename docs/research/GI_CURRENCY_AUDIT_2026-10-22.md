# GI currency audit (22 Oct 2026)

Scope: all **approved** GI items plus the **recommended** GI drafts from the draft review queue, deduped to 400 unique stems. Each one was scanned for time-sensitive content: officials and incumbents, "current/latest/as of", years, recent R.A. numbers, statistics, wages, ASEAN/UN, election facts and named persons. The 56 matches were checked against official text as of 22 Oct 2026. Per-item CSV: `docs/research/bank/gi-currency-audit-2026-10-22.csv`.

## Result

- **Outdated: 0** (approved 0, draft 0). No approved item needs retiring or replacing for currency.
- **No item depends on a current officeholder, statistic, wage or ASEAN/UN rotation.** The GI bank tests constitutional and statutory rules, not incumbents.
- **Watch: 6.** The law is in force, but an amendment is pending. Recheck when it is enacted:
  - CIVIO-GI-20261013-0018 (approved): R.A. 9147 in force; amendment SB 997 filed 6 Aug 2025, not enacted as of check.
  - CIVIO-GI-20261013-0020 (approved): R.A. 9147 in force; amendment SB 997 filed 6 Aug 2025, not enacted as of check.
  - CIVIO-GI-20261013-0025 (approved): R.A. 11313 in force; amendment SB 2897 passed Senate 14 Jan 2025, not enacted as of check.
  - CIVIO-GI-20261013-0026 (approved): R.A. 11313 in force; amendment SB 2897 passed Senate 14 Jan 2025, not enacted as of check.
  - CIVIO-GI-20261013-0027 (approved): R.A. 11313 in force; amendment SB 2897 passed Senate 14 Jan 2025, not enacted as of check.
  - CIVIO-GI-20261013-0028 (approved): R.A. 11313 in force; amendment SB 2897 passed Senate 14 Jan 2025, not enacted as of check.
- The rest are current. Many keyword hits are false positives ("present needs", "Chief Justice" in a count question, "election day" in an age rule).

## Checks made (official sources)

| Fact base | Finding as of 2026-10-22 | Source |
|---|---|---|
| const | 1987 Constitution; no amendment ratified or sent to plebiscite as of 2026-10-22 | https://www.officialgazette.gov.ph/constitutions/1987-constitution/ ; https://www.inquirer.net/476662/comelec-no-election-via-constitutional-amendment-not-possible/ |
| ra6713 | R.A. 6713 text unamended; SALN deadlines restated in CSC 2025 Omnibus SALN Rules (Res. 2500632, eff. 29 Sep 2025) | https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html ; https://csc.gov.ph/new-omnibus-rules-on-saln-released-updated-guidelines-for-2026-filing |
| ra9710 | R.A. 9710 s.18: special leave two (2) months with full pay; no amendment found | https://lawphil.net/statutes/repacts/ra2009/ra_9710_2009.html |
| ra11313 | R.A. 11313 in force; amendment SB 2897 passed Senate 14 Jan 2025, not enacted as of check | https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html |
| ra9147 | R.A. 9147 in force; amendment SB 997 filed 6 Aug 2025, not enacted as of check | https://bills.juris.ph/bills/senate/sbn-997 |
| ra9003 | R.A. 9003 as amended by R.A. 11898 (2022); no later amendment found | https://lawphil.net/statutes/repacts/ra2022/ra_11898_2022.html |
| ra9851 | R.A. 9851 (2009) in force; no amendment found | https://lawphil.net/statutes/repacts/ra2009/ra_9851_2009.html |
| env | Definition / principle (Brundtland; R.A. 11038 E-NIPAS 2018); not time-sensitive | https://lawphil.net/statutes/repacts/ra2018/ra_11038_2018.html |

Also verified directly in the law text: R.A. 6713 §5(a) (15 working days), §5(c) (three signatories), §5(e) (public access), §6 (automatic promotion of awardees), §7(a)–(d), §8 (30 days, April 30, 30 days after separation), §9 (divestment within 60 days), §11 (penalties) and §12 (CSC enforces; the Ombudsman protects complainants).

Related rule change (not a statute): the CSC's 2025 Omnibus Rules on the SALN repealed MC No. 2, s. 2013 and the 2015 SALN form (2025 form mandatory from 1 Jan 2026; spouse signature no longer required). No bank item cites the repealed circular or form.

## Draft fixes made in this pass

18 draft items: 17 in `civio-final-rewrite` and CIVIO-2100-0114. Wrong R.A. 6713 citations were corrected and restated-answer explanations rewritten from the official text. Each item keeps the prior text in a `revisions` field. Status stays draft. The commit message has the details.

## Fact categories that need periodic recheck

| Category | Why it changes | Recheck |
|---|---|---|
| Constitution (1987) | Charter change via Con-Ass, Con-Con or people's initiative plus plebiscite | Each exam cycle; immediately on any plebiscite |
| R.A. 6713 and CSC SALN rules | Amending bills pending; CSC rules change (2025 Omnibus Rules) | Before each CSE date (Mar/Aug) |
| Gender/harassment laws (R.A. 11313, 9710, 11210) | SB 2897 Safe Spaces amendment pending | Quarterly |
| Environment laws (R.A. 9003/11898, 9147, 11038, 9275, 8749) | SB 997 Wildlife amendment pending; EPR rules | Quarterly |
| Human rights / IHL (R.A. 9851, 9745, 10353) | Rare amendments | Yearly |
| Officeholders (President, VP, Senate President, Speaker, Chief Justice, CSC/COMELEC/COA chairs, Ombudsman, cabinet) | Elections (next national: May 2028), appointments, resignations | Avoid in items; if used, recheck monthly |
| Statistics (population, GDP, inflation, poverty, unemployment) | PSA releases | Avoid; if used, cite the PSA release date |
| Minimum wage, salary grades, GSIS/PhilHealth rates | Wage orders, SSL tranches | Avoid; if used, each new wage order |
| ASEAN chair/summit host, UN officials | Annual rotation / terms | Avoid; if used, yearly |
| CSE exam rules (passing rate, item counts, schedule, fees) | CSC announcements | Each exam announcement |
| Holidays and observances | Proclamations each year | Yearly |

## Effect on the 2,000 count

None. No approved item is outdated, so nothing leaves the approved count. The 18 corrected drafts were not in the recommended set (the circular-explanation and citation flags kept them out). Once rechecked, they can join the GI reserve. The recommended set still projects exactly 2,000 if signed.
