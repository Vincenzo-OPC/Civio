# Review request for Chief of Staff: gap-fill-004 (10 GI drafts on human-rights laws)

Grok Bot, 2026-10-17. File: `docs/research/gap-fill-004.json`, built by `scripts/batches/gapfill/gap_fill_004.py`. **All 10 items are draft/unreviewed and inactive.**

## Why
The baseline B2 audit found no items on these five laws. This batch also replaces the retired baseline rows #77 (children, now R.A. 7610), #226 (torture, now R.A. 9745) and #227 (gender equality, now R.A. 9710).

## Checks
- `qa_file.py`: 0 problems. That covers 4 distinct choices, a code and a reason for every wrong choice, codes taken from the spec, no choice named by letter, and no near-duplicate (0.65) against 1,674 bank items or the baseline 550.
- Each item carries `source_quote`. The build script asserts that every quote appears word for word in the LawPhil text fetched on 2026-10-17. The links are in `source_url`.
- Keys are spread over the four choices: 2, 3, 2 and 3.
- 4 items have the optional item-level `shortcut` field.
- Non-retroactivity: 0010 sets the act in 2011 because R.A. 9851 took effect in 2009.

| ID | Law, section | Type | Key | Wrong-choice traps |
|---|---|---|---|---|
| 0001 | R.A. 7610, Sec. 3(a) | DEADLINE-NUMBER | Below 18 | 15 (Sec. 12, working children), 21 (old age of majority), 12 (aggravating age) |
| 0002 | R.A. 7610, Sec. 3(b) | SCENARIO-APPLY | Demeaning words are child abuse | "needs physical injury", "needs a pattern" (the law says "whether habitual or not"), trafficking |
| 0003 | R.A. 9710, Sec. 18 | DEADLINE-NUMBER | 2 months special leave | 6 and 12 months (the service rule), 105 days (R.A. 11210 maternity leave) |
| 0004 | R.A. 9710, Sec. 11(b) | DEADLINE-NUMBER | At least 40% of development councils | 50% (third-level posts), 5% (GAD budget), 30% (R.A. 7192 ODA share) |
| 0005 | R.A. 9745, Sec. 6 | RIGHTS-APPLY | Torture is never justified | state of war, suspended writ, order of battle |
| 0006 | R.A. 9745, Sec. 8 | SCENARIO-APPLY | Excluded, except against the torturers | corroboration, re-signing before a lawyer, an administrative-case carve-out |
| 0007 | R.A. 10353, Sec. 5 | RIGHTS-APPLY | Order of battle is unlawful and may be disobeyed | written order, "only the superior is liable", "valid in war" (Sec. 4) |
| 0008 | R.A. 10353, Sec. 22 | DEADLINE-NUMBER | 25 years from reappearance | never prescribes, 25 years from abduction, 20 years (Revised Penal Code, Art. 90) |
| 0009 | R.A. 9851, Sec. 5(a) | TERM-MATCH | Genocide | war crimes, crimes against humanity, enforced disappearance |
| 0010 | R.A. 9851, Secs. 9 and 11 | SCENARIO-APPLY | Both defenses fail | each half-true combination |

## Asks for CoS
1. Accept, fix or reject each item.
2. Two reasons cite rules outside the source law: 0001 says R.A. 6809 lowered the age of majority, and 0008 cites Revised Penal Code Art. 90. Confirm that's acceptable, or I'll swap in distractors that use only numbers from the law itself.
3. Should these be tagged with R.A. 9851/10353 `fact_id`s alongside any future items on the same sections? Today there is no overlap.
