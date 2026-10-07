# Desktop patches to port (MSI → GitHub)

Source of truth for study UX is GT's MSI local Docker tree (`localhost:8080`).
The baseline commit `d3f0368` (tag `baseline`) **is** that desktop tree. Phase 0.5 (7 Oct 2026, Asia/Manila) re-checked each item against
the desktop sources copied to the box on 5 Oct (`desktop-live-exam-view.tsx`,
`desktop-use-exam-timer.ts`, `desktop-guest-study-bias.ts`,
`desktop-setup-exam-view.tsx`, `desktop-civio-study.ts`) and the MSI note
`Local-Study-Patches.md`. The MSI itself was offline on 7 Oct, so the live
container and the compiled `app-CpqM_WR8.js` bundle were not diffed.

| Patch | Status | Notes |
| --- | --- | --- |
| Guest unlimited access | IN BASELINE | `config/civio.php` + `CIVIO_GUEST_UNLIMITED` |
| Demographics removed from mocks | IN BASELINE | `includeDemographics = false` in pool builder |
| Mock button removed | PORTED (Phase 0.5) | Home shows Start Pro · Start Sub Pro · Practice Drills; the old "Try Mock Test" button and its picker modal are gone. Already in baseline; guarded by `tests/Js/home-launchers.test.ts`. Sidebar "Mock Exams" and the dashboard "Take Mock Exam" menu are the setup page entry points and were not removed. |
| Tutor loop with study bias | PORTED (Phase 0.5) | Scorecard strengths/weaknesses → weak-area drill → next pool biased to misses. Now records from **server** grading (keys stay withheld), drops items once answered correctly, and topic drills lean to past misses / weak subtopics. `resources/js/lib/guest-study-bias.ts`, `tests/Js/study-bias.test.ts`. FSRS not wired here (no per-item review state yet). |
| Exam countdown + per-item clock + urgency colors | PORTED (Phase 0.5) | Exam left 3:10:00 / 2:40:00, amber ≤ 10 min, red ≤ 2 min, auto-submit at 0. This item counts up, resets on move, amber 45–75s, red > 75s. No sound. `resources/js/lib/exam-clock.ts`, `tests/Js/exam-clock.test.ts`. |
| Repositories incomplete-class / cache fix | IN BASELINE (re-verify) | `getActivePool` incomplete-class guard |
| Sirit / Reveal marks wrong after option shuffle | FIXED IN PHASE 0 | ID-keyed answers + original option indices |
| `??` lost math operators | FIXED AT SOURCE (Phase 0.5); MSI rows not yet repaired | Root cause: Windows PowerShell 5.1 `Get-Content file.sql \| docker exec -i … psql` turned each non-ASCII byte into `?`. Seed SQL now sets `client_encoding`, `scripts/import-sql-utf8.ps1` avoids the pipe, and `php artisan civio:repair-bank-encoding` repairs rows idempotently from the UTF-8 seeds. Run it where the bank lives (MSI DB / Neon) with `--dry-run` first; it lists IDs it cannot repair. |
| "(variant N)" clone questions | REMOVED ON GITHUB (7 Oct 2026); MSI DB not yet cleaned | The old `scripts/seeds/seed_real_practice.php` saved every item 8 times, adding " (variant 2)" … " (variant 8)" to the stem, so mocks could hit 150/145. The seeder now saves one copy per item (re-runs skip existing items). The pool builder no longer has `FILL_VARIANTS_AFTER_UNIQUE`, variant fill or cross-category padding; it drops clones and exact copies, and a short bank gives a shorter mock with a toast showing the real count. `php artisan civio:remove-variant-clones` cleans existing rows. See "MSI: remove variant clones" below. |

Do not mark PORTED until re-verified from MSI sources and covered by automated tests.

## Desktop paths and containers (desktop ops only)

These are real names on GT's MSI and are only used in the commands below. Never
stop, rebuild or edit them from an agent; GT runs these himself.

| What | Name |
| --- | --- |
| Desktop study tree | `C:\Users\GT\Desktop\Grok\CSE\Hiraya-Review` |
| Civio clone for agents and Entire | `C:\Users\GT\Desktop\Claude\Civio` |
| App container (`:8080`) | `hiraya-review-app` |
| Postgres container (`:5433`) | `hiraya-review-db`, database `cse_reviewer`, user `hiraya` |

## Desktop study log, 3 Oct 2026 (folded in from the old local patch log)

Done directly on the MSI containers (not in git except where noted):

- **Reveal ("sirit") fix:** the live exam shuffles options but `/exams/reveal`
  returned the key for the original order, so the shown answer could be wrong.
  The desktop fix mapped the index back through `originalOptionIndices` and was
  copied into the running container's `public/build` (service-worker cache v7).
  GitHub has the tested fix since Phase 0 (`d19afda`).
- **Bank expansion on the MSI DB:** 197 of the 200-item pack inserted (3 exact
  active-stem duplicates skipped by the seed guard); active total 722 → 919.
  Coverage: Constitution 30, RA 6713 23, peace/human rights 9, environment 15,
  verbal (English/Filipino) 54, analytical 22, numerical 17, clerical 27. Checks
  on inserted rows: 4 options each, valid 0-based `correct_option`, the answer
  text present in every explanation, no `??` artifacts; 0 items rejected in
  fact-check. The pack is `scripts/seed_cse_pack_200_2026-10-03.sql`.
- **Row repairs on the MSI DB:** broken `??`/quote-marker text and explanations in
  the newest rows, plus wrong numeric choices in two items (the 10% discount item
  and the 6, 10, 18, 34 sequence). These were ID-specific desktop edits; recount and
  re-check after `civio:repair-bank-encoding` runs there.

## MSI: remove variant clones

The MSI desktop DB (Postgres container above, port 5433) still has the clones. Its mocks keep padding with them until this
runs once. Nothing has been run on the MSI; GT runs it when the MSI is online.

Rules (same for the command and the SQL):

- **Clone:** stem matches `\(variant\s*\d+\)`, case-insensitive.
- **Delete:** the clone is not referenced anywhere.
- **Archive:** the clone is referenced by an attempt (`exam_attempts.question_ids`
  or a key of `exam_attempts.answers`), a `saved_drill_items` row or a question
  `feedbacks` report. Its `status` is set to `draft`, the only non-active status
  `questions.status` allows. Draft rows are never in the active pool, so they
  never enter a mock or drill, while old attempts, saved drill sets and reports
  keep a valid row. Caveats: an admin could re-publish a draft from the review
  queue, and archived items no longer show in the detailed review of old
  attempts (that review is built from the active pool; stored scores are kept).
- **Skip:** the clone is referenced and already `draft`. A second run deletes
  and archives nothing.

**If the desktop app has the command** (only after its code is updated from
GitHub; the desktop baseline does not have it):

```bash
docker exec hiraya-review-app php artisan civio:remove-variant-clones --dry-run
docker exec hiraya-review-app php artisan civio:remove-variant-clones
```

**Otherwise, use SQL.** Preview first (read-only):

```sql
SELECT count(*) FILTER (WHERE NOT referenced)                    AS would_delete,
       count(*) FILTER (WHERE referenced AND status = 'active')  AS would_archive,
       count(*) FILTER (WHERE referenced AND status <> 'active') AS would_skip
FROM (
    SELECT q.status,
           EXISTS (SELECT 1 FROM exam_attempts a
                   WHERE a.question_ids @> jsonb_build_array(q.id)
                      OR a.question_ids @> jsonb_build_array(q.id::text)
                      OR (jsonb_typeof(a.answers) = 'object' AND a.answers ? q.id::text))
           OR EXISTS (SELECT 1 FROM saved_drill_items s WHERE s.question_id = q.id)
           OR EXISTS (SELECT 1 FROM feedbacks f
                      WHERE f.flaggable_type = 'App\Models\Question' AND f.flaggable_id = q.id)
           AS referenced
    FROM questions q
    WHERE q.stem ~* '\(variant\s*[0-9]+\)'
) c;
```

Then apply `scripts/seeds/remove_variant_clones.sql`. It is ASCII-only and runs
in one transaction:

```powershell
docker cp .\scripts\seeds\remove_variant_clones.sql hiraya-review-db:/tmp/remove_variant_clones.sql
docker exec hiraya-review-db psql -v ON_ERROR_STOP=1 -U hiraya -d cse_reviewer -f /tmp/remove_variant_clones.sql
docker exec hiraya-review-db rm -f /tmp/remove_variant_clones.sql
```

Full SQL (same as the file):

```sql
-- Civio: remove "(variant N)" clone questions. Same rules as
--   php artisan civio:remove-variant-clones
-- * clone not referenced anywhere          -> DELETE
-- * referenced by an attempt (question_ids or an answers key), a saved drill
--   item or a question feedback report, and still active -> status = 'draft'
--   (archived: never enters the active pool; history rows keep their target)
-- * referenced and already draft           -> skipped
-- Idempotent: a second run deletes 0 and archives 0.
-- ASCII-only file. Preview first with the SELECT in docs/DESKTOP_PATCHES_TO_PORT.md.
BEGIN;

CREATE TEMP TABLE civio_variant_clones ON COMMIT DROP AS
SELECT q.id,
       q.status,
       (
           EXISTS (
               SELECT 1 FROM exam_attempts a
               WHERE a.question_ids @> jsonb_build_array(q.id)
                  OR a.question_ids @> jsonb_build_array(q.id::text)
                  OR (jsonb_typeof(a.answers) = 'object' AND a.answers ? q.id::text)
           )
           OR EXISTS (SELECT 1 FROM saved_drill_items s WHERE s.question_id = q.id)
           OR EXISTS (
               SELECT 1 FROM feedbacks f
               WHERE f.flaggable_type = 'App\Models\Question' AND f.flaggable_id = q.id
           )
       ) AS referenced
FROM questions q
WHERE q.stem ~* '\(variant\s*[0-9]+\)';

SELECT count(*) FILTER (WHERE NOT referenced)                    AS deleted,
       count(*) FILTER (WHERE referenced AND status = 'active')  AS archived,
       count(*) FILTER (WHERE referenced AND status <> 'active') AS skipped
FROM civio_variant_clones;

UPDATE questions q
SET status = 'draft', updated_at = now()
FROM civio_variant_clones v
WHERE q.id = v.id AND v.referenced AND q.status = 'active';

DELETE FROM questions q
USING civio_variant_clones v
WHERE q.id = v.id AND NOT v.referenced;

-- The app caches the active pool forever. With the database cache store,
-- drop those entries so the change shows up without restarting anything.
DO $$
BEGIN
    IF to_regclass('cache') IS NOT NULL THEN
        DELETE FROM cache WHERE key LIKE '%questions.active' OR key LIKE '%categories.tree';
    END IF;
END $$;

COMMIT;
```

The app caches the active pool forever. The SQL clears the `questions.active` and
`categories.tree` entries when the database cache store is used. With a file or
Redis store, the old pool stays cached until `php artisan cache:clear` (or
`cache:forget questions.active`) runs in the app container.

Desktop code note: the desktop pool builder still has the variant-fill and
"any leftover category" padding. With the clones gone, it pads with items from
other categories instead. Port `utils/mock-pool.ts` to stop that.

Tested on 7 Oct 2026 against a throwaway Postgres 17 DB seeded from this repo with
the old seeder (935 questions, 385 clones) plus four references: the SQL and the
command both gave 381 deleted, 3 archived and 1 skipped, then 0/0/4 on a second run.

### Unique pool after clean-up (repo seed data)

Counted on 7 Oct 2026 from a fresh DB built from this repo: `DatabaseSeeder`, the
new `seed_real_practice.php` (55 items) and `scripts/seed_unique_cse_batch_2026-09-30.sql`,
`scripts/seed_unique_cse_batch_2026-10-03.sql` and `scripts/seed_cse_pack_200_2026-10-03.sql`
(495 inserted). That is 550 active, non-demographic, distinct items. The
ID-specific UPDATE scripts (`replace_first_20.sql`, `_fix1405.sql`, …) add none.

| Category | Unique items | Professional needs | Subprofessional needs |
| --- | ---: | ---: | ---: |
| Verbal Ability | 130 (1 Filipino) | 45 | 45 |
| Analytical Ability | 114 | 52 | — |
| Numerical Ability | 91 | 45 | 45 |
| Clerical Ability | 81 | — | 47 |
| General Information | 134 | 8 | 8 |
| **Level pool** | | **469 → 150 reachable** | **436 → 145 reachable** |

Every subcategory has at least 16 items. Running the real pool builder on this bank
gave a full 150 (45/52/45/8) and a full 145 (45/47/45/8) with no repeats. The MSI
DB differs from the repo seed (it had desktop-only edits), so recount there after
the clean-up.
