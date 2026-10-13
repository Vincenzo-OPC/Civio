# Question source groups

`questions.source_group` records where a bank item came from. It is metadata
only: it never changes grading, mock selection, visibility or what the learner
sees, and it is not sent to the browser.

| Value | Meaning | How it is set |
| --- | --- | --- |
| `baseline` | Shipped with the baseline seeds (`d3f0368`) | The migration tags rows already in the bank; seed scripts set it; `php artisan civio:tag-source-groups` tags rows inserted by raw SQL seeds |
| `civio` | Written in Civio (admin editor, AI generation, user custom drills, new authored items) | Set automatically when the app creates a question |
| `NULL` | Inserted outside the app and not tagged yet | Run `php artisan civio:tag-source-groups [--dry-run]` |

Migration rule for rows that already exist: draft rows created on or after
6 Oct 2026 (Asia/Manila) are Civio-era custom or AI drafts and become `civio`;
everything else becomes `baseline`.

New authored items follow `docs/CSE-Question-Design-Spec.md` (Section 10): they
are `civio` and stay `draft` until GT approves them. The 14 Oct 2026
re-parameterized copies are the exception recorded below: GT asked for them to
replace the served baseline bank, so they were inserted as `active`.

## Re-parameterize

Baseline items can be re-parameterized with `php artisan civio:reparameterize-baseline`.
The command reads `scripts/seeds/baseline_reparameterized.json`, matches each row
by the exact old stem (not by id), inserts an active `civio` copy, and sets the
old row to `draft`. `questions.replaces_question_id` points at the old row.
Attempts that already point at the old id keep working. The command is
idempotent. A new stem that collides with a different item is skipped and the
old row is left as it is.

On 14 Oct 2026 GT asked for the served baseline bank to be paraphrased. The
local preview database was updated that day: 496 baseline rows drafted, 496
active `civio` replacements inserted. The MSI Docker database was not touched.
Run the same command there only if you want that bank changed too.

What changed in the items:

- **Kept:** subcategory, language where it was already Filipino, option count
  (four), and one defensible answer.
- **Numerical, sequence, word-problem, data, symbolic, and filing-order items:**
  new names, places, and numbers. The key was recomputed, not copied.
- **General information, ethics, peace and human rights, and environment:**
  the legally correct option text was kept (a president's term stays six years,
  and the other statutory figures stay). The stem was rephrased and the options
  were shuffled.
- **Filing concepts** that state a rule, rather than an order to compute, were
  treated the same way. One old filing item whose key looked alphabetically
  wrong was rebuilt as a computed order instead of copying that key.
- **Not a second-person review.** A 1-in-5 spot check is still owed. These rows
  are active because GT asked for the live bank to change. They are practice
  items, not official CSC questions.

Regenerate the JSON from `scripts/seeds` with `python3 assemble_reparam.py`
before editing stems by hand. The assembler refuses a new stem that repeats an
old stem.

