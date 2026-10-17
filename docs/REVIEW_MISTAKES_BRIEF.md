# Review Mistakes: build brief

Written 17 October 2026 for Grok Build or Codex. Nothing here is built yet.
Source: [LEARNING_DELIVERY_RECOMMENDATION.md](LEARNING_DELIVERY_RECOMMENDATION.md),
"Highest-value next learning slice". Read that file, `AGENTS.md`, and
[CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) section 5 (security invariants) first.

## What the learner gets

A signed-in learner who gets a drill item wrong finds it again under
**Review Mistakes**. They answer it again, without the key showing, and only then
can they open the existing checked explanation. An item leaves the list only
when a later answer is correct **and** was given without help.

The screen is labelled **practice history**. It never says mastery, readiness,
strength, score prediction or anything similar.

## Scope

In:

1. **Storage.** One new table, for example `review_items`: `user_id`,
   `question_id`, `source_attempt_id`, `first_wrong_at`, `last_result_at`,
   `wrong_count`, `status` (`pending` or `resolved`), `resolved_at`,
   `resolved_by_attempt_id`, timestamps. Unique on (`user_id`, `question_id`)
   so one item has one row; a separate unique key on
   (`source_attempt_id`, `question_id`) for idempotent writes is fine if a log
   table is used instead.
2. **Write path.** Write from the existing server-graded submission in
   `app/Actions/Exam/SubmitExamAttemptAction.php`, inside its
   `DB::transaction`, using the graded answers from `ExamGradingService`. Only
   for signed-in users and only for drill/study attempts, not Strict Mocks.
   Never take correctness, question IDs to save, or "help used" from the
   browser.
3. **Help used.** An answer counts as assisted if the server saw a Reveal,
   Explanation or tutor request for that user and question in that attempt
   (for example recorded by `ExamController::revealAnswer`). Assisted correct
   answers are stored but do not resolve an item.
4. **List.** An owner-scoped page and JSON endpoint listing pending items,
   newest first, paginated. Exclude drafts, deleted questions and anything the
   `StrictMockLock` currently protects. One entry point from the drills page
   that also works in Lite Mode.
5. **Retry.** Starting a review reuses the existing drill renderer and
   withholds keys exactly as drills do now. Grading goes through the same
   server path; re-check the Strict Mock lock on submit and on explanation
   access.
6. **Resolve.** A pending item becomes `resolved` only after a later,
   independent, server-graded correct answer. A repeat submission of the same
   attempt must not change anything. A wrong answer on a resolved item sets it
   back to `pending` and increments `wrong_count`.

Out: FSRS scheduling, due dates, a learner model, dashboard meters, guests,
offline drills, new AI calls, changes to mock scoring, and any question bank
edit.

## Tests (Pest unless noted)

- A wrong drill answer creates one pending row; a correct one creates none.
- Submitting the same attempt twice leaves one row and one `wrong_count`.
- User B cannot list, start or resolve user A's items (404 or 403).
- Rows persist across logout and login.
- An assisted correct answer leaves the item pending; an unassisted correct
  answer resolves it.
- A Strict Mock attempt writes nothing, and a locked item is not listed or
  retryable.
- Drafts and deleted questions drop out of the list.
- The review payload never includes `correct_option` or the explanation before
  submission.
- The empty state renders.
- JS (`npm run test:js`): list-state helper and the label copy ("practice
  history", no "mastery" or "readiness").

## Acceptance

- Every check in `AGENTS.md` passes: `php artisan test`, `npm run types:check`,
  `npm run lint:check`, `npm run test:js`, `npm run format:check`,
  `composer lint:check`, `npm run build`, `npm run size`.
- **Bundle budget.** After the CSE 2027 dates page the all-chunks total is
  1,037,038 of 1,040,000 B brotli (about 3 kB of headroom, 17 October 2026). Keep the page lazy,
  add no dependency, keep the exam chunk under 11 kB, and do not raise any
  budget in `.size-limit.json`. If it cannot fit, stop and report what to trim
  instead of raising the limit.
- Works at 360 px wide with no horizontal scroll and no hover-only controls.
- `docs/CHANGES_SINCE_BASELINE.md` and
  `docs/CIVIO_NEXT_AGENT_EXECUTION_PLAN.md` updated.
- Small commits on `main`, `git pull --rebase` before each push, no
  force-push, no deploy.

## Paste prompt

```
git pull. Read AGENTS.md, docs/LEARNING_DELIVERY_RECOMMENDATION.md and docs/REVIEW_MISTAKES_BRIEF.md, then build Review Mistakes exactly as the brief scopes it, in small verified commits on main (all checks green, bundle budget untouched, no question bank edits, no deploy, git pull --rebase before each push, never force-push).
```
