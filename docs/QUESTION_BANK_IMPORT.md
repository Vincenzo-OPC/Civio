# Practice question import

CIVIO stores practice items in the existing `questions` table. Do not add a parallel bank. Imports are paraphrased study items, not official CSC or CSDEx papers.

## Table

`questions` columns used by import:

| Column | Required | Notes |
| --- | --- | --- |
| `subcategory_id` | yes | Resolved from `subcategory` name (must already exist from the syllabus seeder) or `subcategory_id` |
| `language` | no | Defaults to `English` |
| `stem` | yes | Trailing ` (variant N)` is stripped. A second row with the same stem is skipped |
| `options` | yes | JSON array of 2–5 strings, or CSV columns `option_a` … `option_e` |
| `correct_option` | yes | Zero-based index, or a letter `A`–`E` |
| `explanation` | no | Defaults to a practice-paraphrase note |
| `status` | no | `active` or `draft`. CLI `--status` is the default |
| `created_by` | yes | Existing user id. CLI `--user=` accepts an id or email |

Sampling for a fresh Professional mock prefers one question per normalized stem and does not clone `(variant N)` copies to fill the ~150 scored slots. Demographics stay off (`includeDemographics = false`).

## JSON

```json
[
  {
    "subcategory": "Philippine Constitution",
    "language": "English",
    "stem": "The Bill of Rights is found mainly in which article?",
    "options": ["Article III", "Article II", "Article VI", "Article VII"],
    "correct_option": 0,
    "explanation": "Article III is the Bill of Rights.",
    "status": "active"
  }
]
```

## CSV header

```text
subcategory,language,stem,option_a,option_b,option_c,option_d,correct_option,explanation,status
Philippine Constitution,English,The Bill of Rights is found mainly in which article?,Article III,Article II,Article VI,Article VII,A,Article III is the Bill of Rights.,active
```

## Command

```bash
php artisan questions:import storage/app/practice-bank.json --user=you@example.com --status=active
php artisan questions:import storage/app/practice-bank.csv --status=draft
```

Rows that repeat a stem already in the database, or that only differ by a `(variant N)` suffix, are skipped. Approved community paraphrases stay in `recalled_questions` until an editor copies them into a file like this and imports them.
