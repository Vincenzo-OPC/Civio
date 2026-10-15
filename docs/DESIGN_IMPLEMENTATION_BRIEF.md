# Civio Final Design and Frontend Implementation Brief

**Repository:** `Vincenzo-OPC/Civio`  
**Reference:** Attached latest Civio Focused Learning Canvas mockup
Mockup: docs/design/focused-learning-canvas-mockup.png (direction only, not pixel spec; it wrongly shows B selected-green before Reveal).

I had GPT-6 High independently inspect the latest Civio mockup and the actual GitHub codebase.

We are keeping the new visual direction, but the mockup is **not a pixel-perfect specification**. There are design errors, state inconsistencies, and interaction problems that must be corrected before implementation.

This is now an engineering and product-design assignment, not another request to generate a pretty dashboard.

## 1. Start With the Actual Repository

Pull the latest `main`. Read these documents in order:

1. `docs/CODEX_HANDOFF_PLAN.md`
2. `AGENTS.md`
3. `docs/CHANGES_SINCE_BASELINE.md`
4. `docs/CODE_STANDARD.md`
5. `docs/LITE_MODE_PLAN.md`
6. `docs/DESIGN_RESEARCH_AND_ANTI_AI_SLOP.md`
7. `docs/AI_STUDY_AND_SPELLING_SYSTEM.md`
8. `docs/EXTERNAL_AI_HANDOFF.md`
9. `docs/CSE-Question-Design-Spec.md`

The latest `main` checked by ChatGPT was `7b6a173`.

Follow the current repository rules, including working on `main`, making small logical commits, keeping checks green, never force-pushing, and updating `docs/CHANGES_SINCE_BASELINE.md` for behavioral changes.

Do not disrupt the MSI study installation, Docker containers on ports 8080/5433, or Hermes on 8642.

## 2. Existing Implementation You Must Inspect

These are real paths from the current GitHub repository.

**Exam interface**

- `resources/js/pages/user/exams/index.tsx`
- `resources/js/pages/user/exams/components/live-exam-view.tsx`
- `resources/js/pages/user/exams/components/lite-exam-body.tsx`
- `resources/js/pages/user/exams/components/question-palette-panel.tsx`
- `resources/js/pages/user/exams/components/exam-timer-display.tsx`
- `resources/js/pages/user/exams/components/review-exam-view.tsx`
- `resources/js/pages/user/exams/components/scorecard-view.tsx`

**State and timing**

- `resources/js/pages/user/exams/hooks/use-exam-state.ts`
- `resources/js/pages/user/exams/hooks/use-exam-timer.ts`
- `resources/js/pages/user/exams/hooks/use-exam-persistence.ts`
- `resources/js/pages/user/exams/context/exam-context.tsx`
- `resources/js/pages/user/exams/utils/exam-mode.ts`

**Copy for AI**

- `resources/js/pages/user/exams/components/copy-for-ai-button.tsx`
- `resources/js/lib/ai-handoff.ts`
- `tests/Js/ai-handoff.test.ts`

**Layout and styling**

- `resources/css/app.css`
- `resources/js/layouts/app-layout.tsx`
- `resources/js/layouts/app/app-sidebar-layout.tsx`
- `resources/js/components/layout/app-header.tsx`
- `resources/js/components/layout/app-sidebar.tsx`

Inspect their actual dependencies before restructuring.

Do not assume the attached screenshot accurately represents what is already implemented.

## 3. Architecture Decision

`live-exam-view.tsx` is approximately 1,520 lines and currently combines too many responsibilities.

I want the learner-facing presentation separated from the established exam logic.

Create a cleaner component architecture where appropriate:

- `StudySessionShell`
- `SimulationShell`
- `QuestionHeader`
- `QuestionContent`
- `AnswerOption`
- `AnswerFeedback`
- `StudyActions`
- `SessionProgress`
- `QuestionNavigator`
- `SessionToolbar`
- `TutorPanel`
- `PauseOverlay`

These are suggested conceptual components, not mandatory filenames. Fit them to the existing React and TypeScript architecture.

Preserve the existing server grading, session selection, shuffled-option mapping, Reveal authorization, mock submission, and Strict Mock lock.

Do not rewrite working backend functionality to achieve the new design.

## 4. Final Visual Direction

The attached mock is the preferred aesthetic direction.

Keep:

- clean, light editorial layout
- generous whitespace
- near-black typography
- strong question hierarchy
- violet identity
- restrained acid-lime accents
- clear answer choices separated mainly by spacing and horizontal rules
- four quiet global destinations: Study, Simulate, Smart Review, Library
- contextual utilities rather than permanent sidebars
- simple bottom session controls

Remove:

- generic SaaS dashboard cards
- giant Question Palette
- duplicated navigation
- floating tool towers
- decorative gradients
- excessive rounded rectangles
- artificial glow and glass effects
- unnecessary feature tiles
- repeated metadata

Use design principles from Linear, Notion, Brilliant, Khan Academy, Swiss typography, and established usability research.

Do not imitate their branding.

I want Civio to feel designed by a serious product team, not automatically generated.

## 5. Color System

Use these as starting tokens:

| Role | Color |
|---|---|
| Civio Violet | `#5B35F5` |
| Deep Violet | `#3D20C8` |
| Acid Lime | `#B6F72D` |
| Ink | `#101426` |
| Warm White | `#FAFAF7` |
| Surface | `#F4F5F2` |
| Border | `#E3E5EA` |
| Error | `#E5484D` |

The current `resources/css/app.css` still includes blue-oriented tokens such as `#2563eb`.

Develop a proper Civio semantic token system.

However, do not blindly recolor global administration pages. Scope changes carefully and ensure dark-mode and Lite Mode still work.

Lime is a **semantic signal**, not a default CTA color.

It should communicate:
- correct
- mastery
- completed
- positive progress
- resume

Use violet for:
- selected
- current
- focused
- brand
- ordinary primary action

Always validate accessibility contrast. Text on bright lime should generally be dark.

## 6. Critical Answer-State Correction

The mock currently shows answer B in green even though Reveal Answer is still available.

That is inconsistent.

Implement an explicit visual state model:

**Unanswered**
- neutral options

**Selected, not revealed**
- selected option in violet
- no green
- no correctness indicators

**Revealed correct**
- correct selected option in lime
- clear success feedback
- verified explanation available

**Revealed incorrect**
- learner selection marked incorrect
- correct choice highlighted separately
- explanation addresses the misconception

**Strict Mock**
- selection is recorded
- correctness stays hidden until submission

Do not communicate states through color alone.

Add tests for these interactions.

## 7. Action Hierarchy

Do not make every button visually equal.

Before Reveal:

Primary:
**Reveal Answer**

Secondary:
**Ask Tutor**
**Copy for AI**

After Reveal:

Primary:
**Next Question**

Secondary:
**Ask Tutor**
**Try Similar Question**
**Save to Review**

All required learning features remain available. We are reducing unnecessary visibility, not removing capabilities.

Do not display "Reveal always works, AI features are optional" after every question.

If AI fails, offer a useful fallback message only when relevant.

## 8. Tutor and Copy for AI

These features already have specifications and some existing implementation.

Do not rebuild Copy for AI from scratch.

Preserve:
- structured data export
- no DOM scraping
- clean plain-text output
- no hidden answer before Reveal
- shuffled-answer correctness
- Filipino/Unicode compatibility

Keep the current `buildAiHandoffText()` utility and its tests unless an actual problem requires a change.

Tutor should open as a contextual panel only when requested.

The tutor should know the current question, chosen answer, canonical explanation, and applicable learning context.

Static Reveal always remains available without AI.

## 9. Replace the Question Palette Presentation

Preserve the navigation logic from:

`question-palette-panel.tsx`

But replace the permanent giant grid as the default experience.

Proposed:

- question count shown quietly
- slim progress indicator
- Navigator opened on demand
- current, answered, unanswered, and flagged states
- jump-to-question capability
- useful filtering
- keyboard and screen-reader support

The full grid can exist inside a drawer when useful.

Default Study Mode should show the question, not a wall of numbers.

## 10. Timer and Pause

Inspect:

`use-exam-timer.ts`  
`use-exam-state.ts`  
`use-exam-persistence.ts`

The existing timer hook does not appear to expose a proper `isPaused` mechanism.

Add proper pause/resume state without breaking expiration or session persistence.

Required behavior:

- Pause freezes overall countdown
- Pause freezes per-item time
- State is saved
- Question interaction is blocked while paused
- Resume restores exactly where the learner left off
- Refresh/recovery does not silently resume the timer
- Timer does not duplicate intervals
- Auto-submit occurs correctly when active time expires

Study session timing and Strict Mock timing should remain distinguishable.

A paused practice simulation is a convenience feature, not an exact reproduction of an uninterrupted official exam. Keep that distinction clear.

## 11. Correct Information Hierarchy

The screenshot still duplicates category and progress information.

Aim for:

**Top:** Civio / navigation

**Context:** Subprofessional · Verbal Ability · Sentence Structure

**Question:** dominant content

**Answers:** clear and readable

**Learning actions:** Reveal · Tutor · Copy

**Navigation:** Previous · Next

**Session footer:** Mode · Progress · Timer · Pause · Tools

Avoid showing the same information in multiple places without a purpose.

Constrain question reading width intelligently. Do not force excessively long lines on ultrawide displays.

Allow diagrams, data tables, and mathematical content enough room when necessary.

## 12. Tools Menu

The screenshot's open utility menu is a design illustration, not its default state.

Actual behavior:

- closed by default
- opened through a clear Tools action
- keyboard navigable
- proper focus management
- Escape to close
- click outside to close
- correct stacking without obscuring essential controls
- responsive mobile drawer if needed

Include:
- Question Navigator
- Tutor
- Notes
- Sources when applicable
- Similar Question
- Report Issue

Do not show Official Source as if every grammar/spelling question has a government citation.

## 13. Mobile and Lite Mode

This is non-negotiable.

The repository already has a separate Lite Mode implementation:

`lite-exam-body.tsx`

Keep it lightweight and compatible with the same question state.

Do not create two independent exam engines.

Design proper layouts for:
- desktop
- tablet
- narrow Android phones
- Lite Mode
- Study Mock
- Strict Mock
- post-exam review

Use real viewport testing.

The interface must work without horizontal scrolling and without depending on hover.

## 14. Brand Consistency

The attached mock uses the simple abstract lime mark and Civio wordmark.

The repository already contains its own Civio logo assets.

Audit the logo treatment across:
- header
- favicon
- PWA icons
- mobile
- print/PDF

Propose one consistent final mark aligned with the approved visual direction. Do not silently leave mismatched identities.

Civio is always Title Case.

Do not make the interface resemble an official CSC government application.

## 15. Do Not Implement Fake Learning

Do not introduce decorative:
- mastery scores
- AI confidence
- readiness percentages
- progress meters
- review predictions
- question difficulty labels

unless they are backed by actual data.

The current roadmap already specifies FSRS, concept mastery, readiness, and review work.

Read `docs/CODEX_HANDOFF_PLAN.md`.

Every learning indicator must have a real source and a test.

Do not make the UI look impressive by inventing analytics.

## 16. Testing and Repository Discipline

Use the actual project's testing stack, not an invented Vitest setup.

Current JS tests run through:

`npm run test:js`

Required checks:

```bash
php artisan test
npm run types:check
npm run lint:check
npm run test:js
npm run format:check
npm run build
npm run size
```

Run applicable PHP formatting checks for touched files.

Add regression tests for:

- selected/revealed/correct/incorrect states
- strict answer secrecy
- pause/resume and recovery
- question navigation
- keyboard interactions
- Copy for AI
- Lite Mode compatibility
- shuffled answers
- exam submission behavior

Do not modify the question bank as part of this visual redesign.

No automatic deployment. No Netlify build-credit spending.

## 17. Deliverables

First provide:

1. Current component and state ownership map
2. Specific issues in the latest mock
3. Risks in the existing implementation
4. Final design tokens
5. Proposed component hierarchy
6. Desktop/mobile behavior specification
7. Exact files to modify
8. Small logical implementation sequence

Then implement in verified increments.

I want before/after screenshots from the actual running application, not AI-generated concept art.

Use Playwright or equivalent browser inspection if available.

Test the visual states:

- unanswered
- selected
- revealed correct
- revealed incorrect
- Tutor open
- Navigator open
- paused
- strict simulation
- mobile

Show the actual application with realistic questions, not fabricated progress numbers.

**Final acceptance criterion:**

The Civio question should feel like a beautifully designed digital exam paper with intelligent learning tools available on demand.

It must be visually original, functionally reliable, easy for ordinary Filipino CSE candidates, and clearly different from a generic reviewer template.

Keep the underlying intelligence. Replace the visual clutter.

Less, but significantly better.
