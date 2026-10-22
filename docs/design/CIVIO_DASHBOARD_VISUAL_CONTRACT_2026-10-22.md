# Civio Dashboard Visual Contract and Grok Chief-of-Staff Execution Brief
Owner decision: GT, 22 October 2026. Scope: Civio learner dashboard, responsive UI, copy and existing visual components. This is an **implementation directive**, not permission to deploy. Design intent from PRO2000, GRIP PH and Undercor is authoritative for this UI pass; tests and actual rendered measurements remain the proof.

## 1. Confirmed Design Lineage and Precedence

Source comparisons read directly from the other repositories:
- `Vincenzo-OPC/PRO2000/docs/PRO2000_EDITORIAL_STYLE.md` and `docs/MICROCOPY_STANDARD.md`: Title Case for labels, headings, metrics and actions; ALL CAPS only for short eyebrow labels; body/help in sentence case; repeated controls align; no redundant descriptions.
- `Vincenzo-OPC/Undercor/docs/BRAND.md` and `public/style.css`: display typography with deliberate tight tracking; sober black/white surfaces; one volt accent; **no gradients, glass, invented visuals or card wall**.
- `Vincenzo-OPC/Grip-PH/deploy/css/styles.css`: condensed bold display font, Inter reading font, consistent 4px spacing scale, compact section rhythm, tabular numeric alignment, careful accents. Its site-specific motion/effects are *not* blanket permission to copy them into Civio.
- Existing `docs/DESIGN_RESEARCH_AND_ANTI_AI_SLOP.md` already rejects gradients, glows, icon overload and decorative dashboard clutter. This owner directive supersedes its earlier generic advice to avoid uppercase headings: **Civio headings are Title Case by default; selective display titles may be ALL CAPS if optically superior.**

**Brand name remains “Civio” in displayed written copy** as required by `AGENTS.md`. Do not turn it into all-caps “CIVIO” in text merely because a stylized logo graphic looks uppercase.

## 2. Typography and Copy: Explicit Owner Preferences

- **Title Case**: page titles, card headings, navigation items, metric names, action buttons, status chips when label-like. Example: `Mock Accuracy`, `Daily Goal`, `Study Plan`, `Practice Drills`, `Next Milestone`, `Exam Day Today`.
- **ALL CAPS**: only short, intentionally designed eyebrow tags or large editorial hero typography, with measured letter spacing. Examples: `EXAM COUNTDOWN`, `GET STARTED`. Do **not** mechanically uppercase every heading.
- **Sentence case**: paragraph explanations, warnings, instructions, aria labels and ordinary sentences. E.g. `Counting to the start of exam day in Philippine time.`
- No orphaned punctuation, ambiguous labels, slash-stacked copy, decorative emojis, repeated “Mock” or “Study” in one cluster, or gratuitous colon.
- Review glyph shape, counters, descenders, letter collisions, short labels and kerning at actual display sizes. Owner is particularly sensitive to awkward Y/G shapes and crowded adjacent characters. Prioritize meaning, accessibility and product consistency over arbitrary letter avoidance.
- For a disputed prominent label (such as `Smart Study Launchers`, `Your Study So Far` or `Take a Study Mock`), generate **10 concise alternatives internally**. Check semantic accuracy, length, visual rhythm, uppercase/lowercase shape, wrap behavior and accessibility. Select the clearest naturally balanced term; present at most 3 finalists to GT *only* if it materially changes product meaning. Do not launch open-ended naming exercises.
- Do not change schema names/route names/API keys merely to correct displayed labels.
- Current cross-app font family in Civio: `Inter` for reading, `Outfit` for headings, see `resources/css/app.css`. First tune existing fonts and weights. Evaluate whether an already-licensed, already-bundled condensed display style fits; **do not introduce a new font or dependency by default**. No text squeezing with CSS transforms. Limit heading tracking, check descenders and optical alignments at 320/360/390/412/768/1280/1440 CSS px.
- Use `tabular-nums` in countdown, metrics and scores; constrain clock width against digit changes.

### Display-copy candidate replacements to inspect in context (not mandatory blind renames)
| Current / screenshot | Proposed default | Reason |
| --- | --- | --- |
| `Welcome back, User` (guest) | `Start Your CSE Review` (guest) | Not falsely personalized; Title Case |
| `Smart Study Launchers` | `Study Tools` | Less developer-facing, short and stable |
| `Your Study So Far` | `Study Overview` | Short balanced metric title |
| `Take a Study Mock` | `Start a Study Mock` | Verb label; retain correct behavior |
| `View In-Depth AI Analysis` | `View Practice Analytics` | No false AI guarantee while AI is locked |
| `Until exam day` eyebrow | `UNTIL EXAM DAY` | Explicit short eyebrow, not a page heading |
| `No Mock Exam Data Yet` | `No Mocks Yet` | Short, readable empty state |
| `Daily Habit & Goal` | `Daily Goal` | Avoid doubled concepts if habit is visible inside |
Keep `Professional`, `Subprofessional`, `Strict Mock`, `Study Mode` and `Exam Mode` semantically correct. Do not rename exam types just to look better.

## 3. Visual Language: Flat, Aligned, Intentional

Non-negotiable rejects: `bg-gradient-*`, `bg-linear-*`, `bg-radial-*`, `backdrop-blur-*` glass cards, ambient glows, neon borders, glassmorphism, gratuitous `Sparkles` icons, bouncy/hover-float card effects, decorative animated blobs, and stacked micro-badges. If a component requires a gradient for a *functional chart*, document and isolate it; dashboard decoration gets no exception.

- Preserve Civio violet `#5B35F5` and lime `#B3F52D` as restrained functional accents, not large competing multicolor floods. White/warm paper + ink and charcoal/black are the main surfaces. Prefer neutral 1px borders and a minimal shadow, or no shadow.
- Use a **small consistent radius scale**: e.g. outer panels `rounded-xl` (12px), inner tiles `rounded-lg` (8px), pills only for actual pill controls. Do not mix three pill/rounded types without semantic need.
- Choose one coherent page/card surface hierarchy in both themes. Do not alternate `dark:bg-black`, `dark:bg-slate-900`, `dark:bg-slate-950` and glowing-blue panels arbitrarily.
- Avoid tiny 9px/10px text for necessary labels. Main learner text >= 14px where feasible; secondary >= 12px with good contrast.
- Use precise spacing: 16px mobile outer gutters, 20-24px desktop card gaps, matching 20-24px inner padding on equal card types, consistent icons and text baselines.
- Every border/button/label should have a reason to exist. Remove redundant headings, repeated disclaimers, and decorative icon chips that add visual noise.

## 4. Code-level Layout Fixes: Exact Targets

Main route: `resources/js/pages/user/dashboard/index.tsx`.

- Existing dashboard grid uses `grid grid-cols-1 items-start gap-5 sm:gap-6 md:grid-cols-2`. Change **`items-start` to `items-stretch`**, then make each paired card root stretch (`h-full min-w-0`) within that row. Do not use blanket fixed heights.
- Pair 1: `ai-readiness-bento-card.tsx` / `daily-goal-streak-card.tsx`; headers and bottoms should align. Empty analytics must be compact and intentional.
- Pair 2: `smart-study-launchers.tsx` / `study-schedule-activity-card.tsx`. Both currently use `min-h-115`; **remove that artificial min-height**. Remove `my-auto` and unnecessary `overflow-y-auto` from passive empty states; use content height and stretch only in actual equal-height desktop pairs.
- `study-totals-card.tsx` sits in a single orphaned left grid column. Give its wrapper `md:col-span-2` and use a compact horizontally aligned full-width metrics strip, with proper fallback for no history.
- `exam-countdown.tsx`: existing gradient on outer section must become a solid card surface (`bg-white dark:bg-[#141414]`, existing border), not a three-color gradient. Keep clock functionality and the source/date/Pro/Subpro selector. Confirm track preference is used by any relevant exam launch, not merely saved to localStorage.
- `dashboard-hero.tsx`: shorten oversized welcome area, correct guest copy, and avoid a dominant redundant Open Mock CTA if the contextual next action already exists.
- `continue-studying-card.tsx`: make one clear primary action, maintain short Title Case CTA text and clean responsive alignment.
- `daily-goal-streak-card.tsx`: remove `backdrop-blur-xl`, decorative gradients, and repeated action links; keep useful progress, weekly habit and icons only when informative.
- `smart-study-launchers.tsx`: remove four tile gradients, hover-translate effects and badge noise; maintain a true equal-height 2x2 desktop tile grid with matching icon/title/text/CTA baselines and stable mobile collapse.
- `ai-readiness-bento-card.tsx`: remove background gradients and decorative sparkle overload. Preserve the recent verified Mock Accuracy data and distinction between Strict/Study/legacy; do not restore fake pass predictions.
- `study-schedule-activity-card.tsx`: remove `min-h-115` and scrolling empty space; show a short meaningful no-data state; never invent tasks or run history.
- `study-totals-card.tsx`: metrics must be from stored attempts; no faux mastery or pass probability.
- Audit all affected components for `bg-linear`, `bg-gradient`, `backdrop-blur`, `hover:-translate-y`, `shadow-*`, `Sparkles`, `text-[9px]`, `text-[10px]` and inconsistent Title Case.

**Illustrative Tailwind implementation shape (adapt to existing components, do not paste blindly):**
```tsx
<div className="grid grid-cols-1 items-stretch gap-4 md:grid-cols-2 md:gap-5">
  <section className="min-w-0 h-full rounded-xl border bg-card p-5">...</section>
  <section className="min-w-0 h-full rounded-xl border bg-card p-5">...</section>
  <section className="min-w-0 h-full rounded-xl border bg-card p-5">...</section>
  <section className="min-w-0 h-full rounded-xl border bg-card p-5">...</section>
  <section className="min-w-0 rounded-xl border bg-card p-5 md:col-span-2">...</section>
</div>
```
Avoid nesting duplicate visible panel borders if individual components already supply `Card`.

## 5. UX and Mobile Acceptance

- Countdown is the essential exam context; the learner's **one next practice action** is obvious within two seconds. No competing full-color CTAs.
- At <= 412px, reorder for study intent: countdown, next action/daily target, mock accuracy, launchers, history/secondary tools. No duplicate information.
- Screenshot at 320, 360, 390, 412, 768, 1280 and 1440 CSS px, light and dark, logged-out/no-attempt and populated learners.
- No overflow, clipping, mid-word wrap, heading collisions, chopped descenders, illegible clock labels, hover-only actions, layout shift on ticking, or navigation to the wrong selected track.
- Prefer 44px touch targets, contrast at least WCAG AA for ordinary text, keyboard focus indicators and `prefers-reduced-motion` adherence.
- For each desktop pair, assert card left/right edges and heights within 2 CSS px when shown in the same row. Cards can differ across separate rows. Internal four launcher tiles must align within 2px.
- Screenshot review must be done against **the real built application**, not AI-generated mockups. Capture actual box measurements and before/after screenshot paths. Long user names, translated strings, real attempt counts and zero-data states must be tested.

## 6. Grok Chief of Staff: Delegation and Independent QA

Chief of Staff owns scope, priorities, integration, final cross-agent review, and report. Delegate parallel read-only audit work; do not let two writers modify the same components simultaneously.

1. **Design-System Agent**: read PRO2000, GRIP PH and Undercor standards; identify all offending gradients, glows, tokens, radii, tiny labels; own tokens/component styling.
2. **Layout/Responsive Agent**: own dashboard grid geometry, equal-row heights, empty-state compression, mobile breakpoints, 2x2 tile symmetry; produce Playwright DOM measurements.
3. **Editorial/Type Agent**: own Title Case, all-caps eyebrow usage, exact button labels, optical typography and 10-candidate headline vetting when needed. Check semantics and accessibility; no generic AI copy.
4. **QA/Security Agent**: independently check nav links, selected track behavior, ARIA/focus, countdown/timezone, Strict vs Study metric truth, offline E2E race and database grant concurrent requests in isolated Postgres. Report genuine regressions only.
5. Chief of Staff reconciles review findings, makes final product calls not requiring GT approval, implements minimal components, verifies with tests, and requests an independent second-pass critique from a different reviewer than the implementer.

**Do not open another planning phase**. A read-only audit should be a short input to code, not a multi-day deliverable. Agents must cite files/lines and proposed minimal changes, then work with disjoint file ownership. Do not add agents as decorative roles without executing their work.

## 7. Other Confirmed Technical Work, Not to Forget

- Strict Mock offline-reload Playwright test can mistake a browser-aborted save response for a server write that actually completed. Cover *request never reached server* and *server committed but browser lost response* separately, without weakening data-integrity assertions. Repeat both scenarios and retain all 5 existing E2E scenarios.
- Custom drill 100-distinct-new-question budget/saved-set loophole addressed in `445f09d`; verify real simultaneous Postgres requests on disposable DB. Multi-account and guest shared-IP budget are documented residuals; do not start identity-surveillance work.
- Mock Accuracy replaced pass probability in `618611e`. The UI must display correct/total, number of submitted mocks, track, and Strict vs Study separation correctly. No fake passing odds, no AI costs.
- PHP runtime security branch remains a separately reviewed PR; do not merge/deploy as a side effect of this visual pass.
- No paid inference, no changes to question bank, no Rescue activation, no MSI services (8090/5434; 8080/5433; 8642), no production/Netlify deployment.
- Preserve 11 kB exam JS budget; dashboards should not import exam code into their bundle.
- Commit small verified slices with `[skip netlify]`; apply baseline change-log rule; run PHP, JS, types, lint, formatting, build, bundle size and GitHub E2E. Clearly label anything not run.

## 8. Final Report (no vague "looks premium")

Deliver commit links and actual before/after screenshots. Include the measured card dimensions, mobile overflow result, examples of Title Case/copy corrections, inventory of gradients/glows removed, actual test and CI outcomes, verified track behavior, and remaining defects with owners. GT should be able to judge the improvement from the screenshots without reading the implementation essay.
