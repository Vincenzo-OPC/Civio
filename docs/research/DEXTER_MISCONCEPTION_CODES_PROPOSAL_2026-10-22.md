# Dexter misconception codes: data proposal for the bank owner (22 Oct 2026)

**Status:** Proposal only. The schema and engine are on `main`; **no bank data, manifest or importer was changed**. Another worker owns the bank. Generative AI stays off.

## What exists now
- `questions.archetype` (nullable string) and `questions.distractor_codes` (nullable JSON `{stored option index: code}`). Migration `2026_10_22_170000_add_dexter_metadata_to_questions.php`. `distractor_codes` is `#[Hidden]` on the model because it implies the key.
- `config/dexter_misconceptions.php` (version `2026-10-22.1`): the spec §3 distractor codes for Numerical, Clerical filing and Spelling, each with learner wording, a method line and an optional `remedial_skill` archetype.
- `App\Services\Dexter\MisconceptionDiagnoser`:
  - `diagnose()`: names the likely mistake after grading.
  - `problems()`: a QA check for out-of-range indexes, a code on the correct option, or unknown codes.

## Proposed import mapping (for the bank owner to implement and review)
1. **archetype:** take it from the spec item `archetype` field, or from the id prefix (`CIVIO-NUM-WP-PCT-CHANGE-123456` → `NUM-WP-PCT-CHANGE`). The `CLR-SPELL-*` and `CLR-FILE-*` families map to the skill graph ids of the same name.
2. **distractor_codes:** bank sources hold `distractor_reasoning: {option_id: code}`. At import, translate each `option_id` to the **stored** option index (the same index `correct_option` uses, before any display shuffle). Store only the wrong options.
3. **Filing items:** keep the parent `CLR-FILE-ORDER` out of the learner path. When `distractor_subreason` names a more specific code (`CLR-WORD-BY-WORD`, `CLR-PREFIX-SPLIT`, …), store that code instead.
4. **QA gate:** run `MisconceptionDiagnoser::problems()` on every imported item and fail the import on any problem. Untagged items are allowed (no diagnosis is shown).
5. **Approval:** tagging is content. It goes through the existing review packets. Agents must not mark items approved.

## Priority order
1. Subprofessional Numerical: `NUM-WP-PCT-CHANGE`, `NUM-FRAC-DEC`, `NUM-PCT-BASIC`, `NUM-WP-RATIO`, `NUM-WP-RATE`, `NUM-WP-ALGEBRA`, `NUM-OPS-ORDER`.
2. Spelling: `CLR-SPELL-RIGHT`, `CLR-SPELL-WRONG`.
3. Filing: `CLR-FILE-POSITION`.

Verbal (VEN/RC) codes exist in the spec but are not yet in the taxonomy. Add them with learner wording in a later version bump.

## Not verified
I didn't count how many bank source items already carry `distractor_reasoning`, because the bank files are in flux.
