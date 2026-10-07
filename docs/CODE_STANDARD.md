# Civio code standard

The bar for new code and for any inherited file you touch. Leave a file better
than you found it, keep behaviour the same unless the change says otherwise, and
keep every check green.

## Backend (PHP 8.4, Laravel 13)

- `declare(strict_types=1);` in new files. Typed properties, parameters and returns
  everywhere; generics in PHPDoc for relations and collections
  (`@return BelongsTo<User, $this>`, `@return Collection<int, Question>`).
- **Controllers are thin:** validate with a Form Request, call one Action or
  Service, return an Inertia page, a JSON Resource or a redirect. No queries or
  business rules in controllers.
- **Actions** (`app/Actions/<Area>/<Verb><Noun>Action.php`) do one write use case
  and own their transaction. **Services** hold reusable read or domain logic.
  Repositories only where caching or a query shape is shared.
- **DTOs** are `final readonly class` with named constructors (`fromRequest`,
  `fromArray`); no arrays of unknown shape crossing layers.
- Enums for every closed set (`QuestionStatus`, `QuestionSourceGroup`, `ExamTrack`).
  Casts on models, never string comparisons.
- Resources whitelist fields. Never add `correct_option`, `explanation` or bank
  metadata to a live exam payload.
- Config through `config/civio.php`; never `env()` outside config files.
- Rate-limit every public write and every endpoint that returns bank content.
- Tests: Pest. Feature test per endpoint (happy path, auth/guest, validation,
  tamper); unit test per pure service. Seeded randomness (`Random\Randomizer` with
  `Xoshiro256StarStar`) so tests are deterministic.
- Format: `vendor/bin/pint` (formatting-only changes go in their own `style:` commit).

## Frontend (React 19, TypeScript strict, Inertia 3)

- No `any`. Use `unknown` plus a type guard, or a real type from `resources/js/types`.
- Props are named interfaces with `readonly` fields; components are small (aim for
  under ~200 lines) and do one thing. Split big screens into a page shell, sections
  and pure helpers.
- Logic that can be pure lives in `lib/` or `utils/` as plain functions with tests
  in `tests/Js/*.test.ts` (`node:test` via `tsx`).
- Hooks own state and effects; components render. Shared app state uses small
  stores (`useSyncExternalStore`), not prop drilling or globals.
- Heavy or rare code is lazy (`React.lazy`, dynamic `import()`): charts, PDF, the
  offline runner, IndexedDB. Check `npm run size` before and after.
- Browser storage keys are `civio_*`; read and migrate older keys in
  `lib/legacy-storage.ts` only.
- Accessibility: real buttons and links, labels on inputs, visible focus, 44 px tap
  targets on phones.
- Format: `npm run format` (prettier) and `npm run lint` (eslint); formatting-only
  changes go in their own `style:` commit.

## Every change

- Small commits, Conventional Commit messages, normal pushes to `main`.
- Behaviour change → `docs/CHANGES_SINCE_BASELINE.md` row in the same commit.
- Before push: Pest, `types:check`, `lint:check`, `test:js`, build, `npm run size`.

## Modernization backlog

Ranked by value and risk (do the top first). Each item is one or more small
commits with tests green before and after. "Done when" is the acceptance bar.

| # | Module | Today | Work | Risk | Value | Done when |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Formatting leftovers | Pint: `AllowFreeAttempt`, `AllowGuestStudy`, `DeterministicAnalysisService`, `ExamGradingService`, `ExamAttemptFormatter`, `scripts/_check_demo.php`. Prettier: 23 files under `resources/` (exam views and hooks, public pages, learn pages, sidebar/header) | One `style:` commit per area | Low | Medium | `vendor/bin/pint --test` and `npm run format:check` pass on the whole repo |
| 2 | Exam grading core (`ExamGradingService`, `ExamAttemptFormatter`, `SubmitExamAttemptAction`) | Arrays of loose shape between layers | Readonly DTOs for graded answers and scores; typed returns; unit tests per scoring rule | Medium | High (security core) | Same scores on the existing Pest suites; new unit tests for each category and legacy attempt shape |
| 3 | Exam client state (`use-exam-state`, `use-exam-hydration`, `use-exam-persistence`, `use-exam-submission`) | Large hooks with intertwined effects | Typed reducer (pure, tested) plus thin hooks; persistence through one storage module | High | High | `tests/Js` covers start, answer, reveal, resume, submit; manual mobile check of resume |
| 4 | Exam screens (`live-exam-view` 1.4k lines, `review-exam-view` 1.8k, `scorecard-view`) | Monolith components | Split into header, question card, palette, dialogs; typed props; no `any` | Medium | High | Each file under ~300 lines; Lite and normal screens unchanged visually |
| 5 | Guest/attempt middleware (`AllowGuestStudy`, `AllowFreeAttempt`) | Mixed policy and request handling | Policy object in `app/Support` with unit tests; middleware just calls it | Medium | Medium | Guest-unlimited tests still green; new unit tests for each flag combination |
| 6 | Admin questions (`Admin\QuestionController` 440 lines, `pages/admin/questions/*`) | Fat controller, large pages | Form Requests + Actions per use case; split pages; new items `civio` + `draft` | Medium | Medium | Feature tests per admin endpoint; no behaviour change |
| 7 | AI generation (`GenerateQuestionsJob`, `AiGatewayService`) | Job does prompt, parse and save | Action for save, DTO for generated item, provider contract like `TutorProvider`; drafts only | Medium | Medium | Job test with a fake provider; generated items are `civio` drafts |
| 8 | Analysis (`DeterministicAnalysisService` 1k lines, `StudyPlanAnalyzer`) | One big class | Split by concern (readiness, subject breakdown, recommendations) with unit tests | Medium | Medium | Same output on fixture attempts (snapshot tests) |
| 9 | `any` removal | 107 uses (most in `app.tsx`, `ssr.tsx`, curation shells, quick-edit modal, AI analysis page) | Replace per module with real types or `unknown` + guards | Low | Medium | `rg ": any|as any" resources/js` returns 0; eslint rule `no-explicit-any` set to error |
| 10 | Drills custom builder (`custom-builder-view` 1.9k lines) | Monolith | Split builder, preview and save; DTO-backed save endpoint already exists | Medium | Medium | Under ~300 lines per file; JS tests for item validation |
| 11 | `pages/dev-docs.tsx` (4.1k lines) | Shipped as a route chunk | Move to docs or gate to admin/dev only | Low | Low | Not reachable for learners; bundle unchanged or smaller |
| 12 | Printable exam / PDF (`printable-exam` 1.5k lines) | Lazy already; large | Split watermark, cover and item renderers | Low | Low | Print output identical on a sample attempt |

Touched and modernized in the de-baseline batch (7 Oct 2026): `site-footer.tsx`
(typed link list, small components), `app-logo-icon.tsx`, `lib/legacy-storage.ts`
(pure, tested), the inline Blade scripts (plain JS, tested), `Question` model
(typed relations, enum casts), `TagQuestionSourceGroupsCommand`, and the
offline-pack modules added in L2.
