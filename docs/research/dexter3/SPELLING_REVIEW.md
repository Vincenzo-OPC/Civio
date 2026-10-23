# Clerical spelling screen: 133 records

This is a deterministic first-pass lexical check over three spelling families in the repository candidate ledger. It uses the host's Hunspell 1.7 library and the en_US dictionary package `hunspell-en-us 1:2020.12.07-2`. `audit_spell133.py` records each option result with the exact source record hash; `validate_spell133.py` verifies counts and the two lexical exceptions. A dictionary hit is not a complete linguistic judgment: it can accept a real word used with the wrong meaning and can vary by regional, dialect, proper-name, or inflectional conventions.

| Scope | Records | Bank labels |
| --- | ---: | ---: |
| `CLR-SPELL-WRONG` | 63 | counted in total below |
| `CLR-SPELL-RIGHT` | 50 | counted in total below |
| `CLR-SPELLING` | 20 | counted in total below |
| **Total** | **133** | **113 approved, 20 draft** |

The screen supports the stored key under the generic “correctly spelled”/“incorrectly spelled” rule for 131 questions. Two require lexical context review. `CIVIO-CLR-20261013-0034` gives the meaning “a schedule of dates,” which distinguishes **calendar** from **calender**, a correctly spelled word for a roller or machine. Keep that meaning cue; the answer is contextually unique. Merriam-Webster defines the words separately: [calendar](https://www.merriam-webster.com/dictionary/calendar) and [calender](https://www.merriam-webster.com/dictionary/calender).

`CIVIO-CLR-SPELL-RIGHT-000900` offers **yield** and **yeld** without a meaning or target-variety constraint. Collins records *yeld* as a Scottish/Northern English dialect word (including an adjective meaning barren); therefore “Which word is spelled correctly?” does not establish one answer in broad English. Replace that distractor with an unambiguously misspelled form or define the target word/variety. See [Collins: yeld](https://www.collinsdictionary.com/us/dictionary/english/yeld).

All 133 have wrong-option feedback text. Twenty already have pilot tutoring bindings, which were left unchanged. This batch did not re-audit all 20 rationales for linguistic accuracy. The 20 draft bank records are excluded from any release-ready count. No human review was completed; no question or approval status was changed; the audit and any future tutoring remain non-runtime drafts. These results are lexical screening, not complete editorial approval.

Run `python3 docs/research/dexter3/audit_spell133.py` followed by `python3 docs/research/dexter3/validate_spell133.py`. The first command needs the stated host Hunspell library and dictionary; the JSON result preserves source hashes so later content changes are detectable.
