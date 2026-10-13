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
