# Civio × Fernly: learner experience design proposal (18 October 2026)

> **Status: concept and implementation brief, NOT shipped UI.** Design visuals are illustrative. No repository application code, routes, permissions, scoring, or learning metrics changed in this commit. Review this alongside [the sole execution roadmap](../CIVIO_NEXT_AGENT_EXECUTION_PLAN.md), [current-state handoff](../CIVIO_CURRENT_STATE_HANDOFF.md), and [anti-slop design rules](../DESIGN_RESEARCH_AND_ANTI_AI_SLOP.md). Existing code and tests override design assumptions.

## Reference, licensing and boundaries

- Inspiration: [Fernly live preview](https://demo.codeandchill.store/fernly/) and [official Fernly product description](https://codeandchill.store/templates/fernly), by Code and Chill. Creator's reel supplied by GT as visual reference.
- Fernly is a **paid**, seven-page project dashboard (Dashboard, Tasks, Calendar, Analytics, Team, Settings, Help); its product listing describes vanilla JavaScript/CSS/SVG with GSAP, **not React**. Its demo contains illustrative project data and no real backend. **Do not copy or redistribute its paid source**, clone its brand, buy it without owner approval, or add GSAP.
- Borrow only principles: responsive information density; precise card spacing; visual hierarchy; directional navigation; a visually distinct time instrument; charts that explain real data; active states; subtle motion.
- Civio remains a CSE learning product, not an admin dashboard. Preserve violet `#5B35F5`, lime `#B3F52D`, paper `#FAFAF7`, true-black dark mode; **no blur/glass on dark cards**. Existing Lite, question-state, offline, and server-secrecy rules remain.
- Design artifact: [desktop exam workspace SVG](./CIVIO_EXAM_WORKSPACE_FERNLY_INSPIRED_2026.svg). It shows a **fictional illustrative 18%-of-250 sample item**: B (45) is selected violet, *not* marked correct. Example progress/time are **mock-up figures**, not live learner data. The actual production question bank is unchanged.
- Concept PNGs were generated for review in the originating ChatGPT conversation. The SVG here is the durable, vector design reference on GitHub. It is deliberately not production application code.

## Every Fernly page considered, adapted to Civio's real pages

| Fernly section | Civio target | Design action | Data constraints / existing source |
| --- | --- | --- | --- |
| Dashboard | Learner Home, `resources/js/pages/user/dashboard/` | One dominant **Continue Studying** action, resume context, small verified study totals, recent attempts, next relevant action; avoid four interchangeable KPI cards. | Existing `DashboardHero`, `SmartStudyLaunchers`, activity/streak cards; only derive numbers from stored attempts/tasks. |
| Tasks | Practice Drills and future review queue, `resources/js/pages/user/drills/` | Subject selection and topic filters as a clean task/workflow; saved practice sets; genuine reviewed-mistakes actions. | Saved sets and custom drills exist; **FSRS due queue does not**. Never visually imply due-review scheduling exists. |
| Calendar | Study Plan, `resources/js/pages/user/calendar/` | Clear upcoming sessions, task status, weekly/month/agenda controls, compact date rail and natural mobile agenda. | Existing templates, grid, agenda, drag-and-drop, exam countdown: reuse, don't duplicate. |
| Analytics | Performance Analytics, `resources/js/pages/user/analytics/` | Restrained subject breakdown, score trend, practice volume, pacing, filter controls, accessible data tables in Lite. | Existing lazy `AnalyticsCharts`, `MetricsGrid`, `CseReadinessCard`. Audit readiness calculation; NO fabricated mastery, rates, forecasts, or AI insight. |
| Team | Study Hub / subject catalogue, `resources/js/pages/user/learn/` | Use Fernly's scannable profiles only as inspiration for **subject cards** and lesson status, not fake social features. | Existing modules, search and lesson progress. Avoid inventing human cohorts/teams. |
| Settings | Civio preferences | Cohesive appearance, Lite Auto/On/Off, readable labels, keyboard preferences and accessibility. | Existing Lite system. Do not create another independent performance tier or gratuitous accent picker. |
| Help | Onboarding, terms, support | Contextual low-friction explanations, reference links and next-step guidance only when needed. | Preserve verified CSC disclaimer and actual help routes. |

## Additional Civio-specific screens (the essential design work)

### 1. Exam selection and setup

- Existing files: `resources/js/pages/public/welcome.tsx`, `resources/js/components/domain/exam-level-picker.tsx`, `resources/js/pages/user/exams/components/setup-exam-view.tsx`.
- Preserve **Choose Your Exam.** with no subtitle; Professional (150, 03h 10m) / Subprofessional (145, 02h 40m) and approved occupational descriptions. Existing count-up and `TimeDial` already work; no duplicate counter.
- Study Mode: optional timer, authorized Show Explanation and Copy Question / external AI handoff. Exam Mode: strict timer, no Reveal/Ask during attempt; answers after submission. Do not advertise Dexter as a chatbot.
- The highest priority interaction is selecting a mode without reading a paragraph or mistaking a locked timer checkbox for an error.

### 2. Actual **Study Mode** workspace (highest-priority concept)

- Existing files: `resources/js/pages/user/exams/components/live-exam-view.tsx`, `session/answer-option.tsx`, `session/answer-reveal.tsx`, `exam-timer-display.tsx`, `question-palette-panel.tsx`, and `hooks/use-exam-state.ts`.
- Focused, paper-like question canvas. Header: exam track, subject/topic, current question, Flag, Question List. The question is visually dominant; 4 clear options, comfortable reading measure, subtle separators. Violet means selected, never correct until authorized reveal.
- Secondary actions group: **Show Explanation**, **Copy Question**, **Ask** (external assistant, when enabled). Keep current **Show/Hide Explanation** as one control. On-demand Tools (Notes, keyboard help, Focus, Lite); Question List closed by default.
- Question progress, optional clock, previous/next and pause where permitted should be calm and coherent; not a permanently exposed tool drawer. Use the existing subscription-driven `ExamTimerDisplay` rather than adding tick-driven React updates.
- The first generated Study Mode concept is illustrative, not a screenshot from the actual browser, and contains an ambiguous English sample. **Do not put it into a production question bank.** The canonical vector SVG uses a correct arithmetic sample instead.

### 3. **Exam Mode** / Strict Mock (precision timer concept)

- Make time the sole prominent secondary visual on large screens. A fine circular timer and large stable tabular digits may sit in a compact exam-information zone, reducing to a small pinned timer on mobile. Actual existing `TimeDial` can be styled/repositioned, not duplicated.
- Example: Professional total **03h 10m**, question **12 of 150**, live remaining time measured by actual session state. Never treat the concept's number as live data.
- **No Pause action** in strict mode when rules disallow it; no explanation, tutor, external AI or answer-leaking PDF actions. No difficulty badges without verified metadata.
- Navigation remains obvious; active question/answered/flagged accessible through on-demand Question List. No Auto-Next.

### 4. Results and review

- Existing: `resources/js/pages/user/exams/components/scorecard-view.tsx`, `review-exam-view.tsx`, `resources/js/pages/user/history/`.
- One clear score number and practice-rating caveat; a concise subject breakdown based on server result; meaningful **Review Answers** / **Review Mistakes** actions; explain wrong options where verified.
- Do not claim practice scores equal official CSC general rating, or show invented pass probability. Data visualizations must match stored graded data.
- Illustrated demo `112/150` is sample math, not a real student's result.

### 5. Analytics and learner return loop

- Group metrics by decision: *How did I perform? What went wrong? What should I practice next?* Link to actual drill filters and saved mistakes when implemented.
- Distinguish supported lesson-completion percentages from FSRS-derived mastery (not shipped). Existing `fsrs.ts` is scheduler math only; due reviews require new persistence and review events.
- Avoid made-up charts, congratulations, cartoon badges, filler words and static 5-day streaks.

### 6. Mobile / Lite

- 320/375/390/430px: single column, large answer tap targets, short header, pinned minimal timer where relevant, bottom-safe navigation, no always-on right rail. Full Question List in accessible drawer.
- Existing `resources/js/lib/lite-mode.ts` and `lite-exam-body.tsx` remain authoritative. Do not add Motion or GSAP. Respect Save-Data, manual Lite choice, reduced motion, and bundle gates.
- Offline drills continue to work. No fake offline strict-mock permissions, stale scores or key caching.

## Art direction and behavior tokens

- Brand: exam light `#5B35F5` violet / `#B3F52D` lime for confirmed positive states; ink `#101426`; paper `#FAFAF7`; fine border `#E3E5EA`; dark paper `#000000`.
- Typographic art direction: high-quality existing heading/body faces, restrained sizes, precise optical placement of A/B/C/D, tabular time/count numerals, balanced line wrapping, no one-word orphans. Keep microcopy natural; never elongate just for symmetry.
- Interaction: 120–180ms subtle color/selection transitions; no continuous chart animations; optional one-time counter/sweep; no selected-answer lime before reveal; full reduced-motion and Lite fallbacks. Reuse Lucide, Tailwind, SVG, Radix; no heavy new JS.
- Avoid permanent admin sidebars, GSAP, unrelated calendar/team features, glossy gradients, duplicate timers, unreliable readouts, decorative readiness meters, or mock source citations.
- The showcase image uses sample screens. **No illustration is verified live UI**; the first task for a coding agent is actual browser capture and comparison.

## Recommended delivery sequence, not a replacement roadmap

1. **Visual QA** on real code: desktop Study, Exam Mode, reveal, results, analytics, mobile/light/dark/Lite. Compare to `CIVIO_EXAM_WORKSPACE_FERNLY_INSPIRED_2026.svg`, not to paid Fernly code.
2. Prototype small refinements using existing components; preserve user controls, strict locks, keyboard behavior and tests. Do not alter application architecture purely for visual fidelity.
3. Implement and test desktop Study/Exam workspace timer hierarchy and question/option typography, then mobile, then scorecard.
4. Audit real dashboard/analytics metrics and improve information hierarchy without inventing data. Later FSRS work follows the sole execution roadmap.
5. Screenshot actual implementation, verify accessibility, `npm run types:check`, `npm run lint:check`, `npm run test:js`, `php artisan test`, `npm run build`, `npm run size`, and formatting as applicable.
6. Record changes in existing changelog and handoff if production behavior changes; require owner visual approval before major UI replacement. No deploy or paid-template purchase.

## Concept acceptance

The design succeeds only if a new learner knows the next action within 2 seconds, the question is the focal point, the timer is precise but not stressful, Study and Exam Mode differ appropriately, mobile never feels like compressed desktop, and statistics are truthful. Preserve independent CSC positioning. This document records **inspiration and proposals**, not shipped features.

