# Subprofessional coverage gap map (v1, 2026-10-13)

**Official scope:** CSC Examination Announcement No. 03, s. 2026 (CSE-PPT, 09 Aug 2026), Section F, as quoted in the spec §1 and the master research doc. Subprofessional covers:

- **Verbal (English and Filipino):** word meaning, sentence completion, error recognition, sentence structure, paragraph organization and reading comprehension
- **Numerical:** basic operations, sequence and word problems
- **Clerical:** filing and spelling
- **GI:** the 1987 Constitution, R.A. 6713, peace and human rights, and environmental management and protection

CSC publishes no subtest weights.

Counts are active items in the local dev DB as of 2026-10-13, plus drafts in the repo.

| Competency | Baseline (active) | Civio 001-011 (active) | Drafts (ChatGPT supp + gap-fill-001) | Gap |
|---|---|---|---|---|
| Verbal EN: vocabulary, synonym, antonym, idiom | part of 130 | ~70 | – | OK |
| Verbal EN: grammar, error recognition | part of 130 | ~100 (agreement, tense, prepositions, pronoun case) | – | Error recognition in sentence form is thin |
| Verbal EN: reading comprehension | part of 130 | 0 | 4 | **Gap** |
| Verbal EN: paragraph organization | part of 130 | 0 | 3 | **Gap** |
| Verbal FIL: all types | part of 130 (1 Filipino seed file) | 0 | 80 + 8 sawikain | **Gap**. Depends on fixing ChatGPT's 80 |
| Numerical: basic operations, sequence, word problems | 91 | 303 | – | Fractions and decimals as plain operations are thin |
| Clerical: spelling | part of 81 | 93 | 20 | OK |
| Clerical: filing | part of 81 | 58 (personal names only) | 20 + 3 | Business names and ARMA Rules 2, 7 and 8 are thin |
| GI: Constitution | part of 134 | ~70 | 2 | OK |
| GI: R.A. 6713 | part of 134 | ~28 | – | OK |
| GI: peace and human rights | part of 134 | ~3 | 5 | **Gap**, partly filled |
| GI: environment | part of 134 | 1 | 28 | Filled once ChatGPT's GI is fixed |

The baseline per-subtopic split is not yet audited (round 03+).
