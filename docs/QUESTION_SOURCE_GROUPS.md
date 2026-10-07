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
are `civio` and stay `draft` until GT approves them.

## Future workflow: re-parameterize

Baseline items can later be re-parameterized in batches, using `source_group =
baseline` to find them. Re-parameterizing keeps the item's soul and changes its
surface:

- **Keep:** the subtest, the skill being tested, the reasoning steps, the
  difficulty, the number of options, the kind of distractors, and the Reveal
  structure.
- **Vary:** names, places, numbers, amounts and units (re-solving the key), and
  the phrasing of the stem, options and explanation.
- **Check:** the new key is re-derived, not copied; the item passes the
  Section 7 checklist; there is still exactly one defensible answer.
- **Record:** the new item is a `civio` draft that points back to the item it
  came from, and goes through the normal review in Section 10. The old item is
  set to `draft` only after the new one is approved, so attempts that point to it
  keep working.

No item has been re-parameterized yet. The workflow needs GT's go-ahead per batch.
