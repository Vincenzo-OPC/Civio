# Civio Home Page: Choose Your Exam, 2026 Redesign

**Status:** Proposed UX implementation brief, not yet deployed
**Date:** 15 October 2026
**Audience:** Grok Bot / Codex working in `Vincenzo-OPC/Civio`
**Source:** User's pasted Grok preview + independently inspected GitHub main.

## Goal

The public root home page must make a single choice easy: **Professional or Subprofessional**, then a clear path into mock setup. It is NOT the authenticated learning dashboard. The currently pasted experience over-explains counts/timing, contains multiple competing rings, uses a static exam screenshot, and appears more like a feature demo than a trustworthy exam entry point.

Make it feel like Civio's approved **Focused Learning Canvas**:
- warm near-white canvas `#FAFAF7`
- ink `#101426`
- violet `#5B35F5`
- restrained acid lime `#B6F72D`
- editorial typography and simple dividers
- one quiet navigation system
- no gradients, glow, big feature tiles, giant sidebar, decorative timer rings, mock screenshot, or fake scores.

## Actual code to update

- `resources/js/pages/public/welcome.tsx` currently renders the H1, explanatory copy, picker, CTA row, duplicate links, `ExamScreenPreview`, and `ExamFormat`.
- `resources/js/components/domain/exam-level-picker.tsx` currently includes a decorative `TimeDial` and a line saying the ring shows duration. Replace the ring with **150 questions / 3h 10m** and **145 questions / 2h 40m** as real text. Preserve keyboard-controlled radiogroup and accessible state.
- `resources/js/components/domain/exam-screen-preview.tsx` is a static screenshot with question 1/150; REMOVE IT FROM THE PUBLIC HOME. The component can remain if still used elsewhere.
- `resources/js/components/domain/exam-format.tsx` currently shows an 80.00 circle, duplicates exam data and makes rating resemble score. Replace its homepage use with compact non-graphical CSC facts, or remove this component from the homepage.
- `resources/js/lib/exam-dials.ts` is the existing source of truth for item counts, duration, and descriptions. Reuse it.
- `resources/js/components/layout/site-header.tsx` and `site-footer.tsx` control header/footer. Simplify the homepage header if necessary without breaking other pages.

## Recommended copy and visible content

Eyebrow: `PHILIPPINE CIVIL SERVICE EXAM`

H1: **Choose your exam.**

Description: `The right practice starts here. Pick your level, choose how you want to study, and get straight to the questions.`

Level control, two **large radio options**, no ring:

**Professional**
For professional, technical, and supervisory positions.
- **150 scored questions**
- **3h 10m time limit**

**Subprofessional**
For clerical, trades, and custodial positions.
- **145 scored questions**
- **2h 40m time limit**

Primary CTA changes based on choice:
- `Set Up Professional Mock →`
- `Set Up Subprofessional Mock →`

Route must preserve existing `/exams?start=professional` or `/exams?start=subprofessional` and guest free-attempt behavior, as appropriate.

Secondary option: `I'd rather practice by topic ↗` → `/drills`.

Below CTA: `Next: choose Study Mock or Strict Mock. Nothing starts until you're ready.`

If an authenticated learner has a genuinely resumable session, **Resume Studying** can be shown contextually with the actual resume destination. Do not call `/exams` a guaranteed resume link if no session exists.

## Learning mode explainer below first fold

Heading: **One goal. Three ways to prepare.**

Three succinct editorial columns, no cards:

- **Study Mock:** Answer at your pace. Reveal explanations as you go; AI tutor optional.
- **Strict Mock:** Realistic countdown, no answers or explanations until you submit.
- **Practice Drills:** Work on one skill at a time, e.g. Clerical Ability / spelling.

The public homepage is primarily an entry page. Do NOT show an entire mock exam, report button, copy for AI button, personalized analytics or a Tutor thread on it. Those belong in Study Mode, and strict exam mode does not show them during the exam.

## Trust and CSC facts, below the core choice

Use one quiet prose block:
`The CSC states a general passing rating of at least 80.00. Civio's mock includes only scored test-proper items; the separate 20-item Examinee Descriptive Questionnaire is not part of the mock. Civio is independent and not affiliated with the CSC.`

Link to CSC August 2026 official document:
https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf

**Never** present `80.00` as a donut/progress ring, mock score, performance prediction, or automatic 80%-raw-questions equivalence.

## Interaction/state requirements

- Professional default selected; user can change to Subprofessional.
- Selected radio has violet focus/border and explicit marker, not lime success coloring.
- CTA text dynamically reflects selected level.
- Arrow keys change level selection and manage focus.
- Tab/Enter/Space work correctly for keyboard users.
- Mobile is designed independently: stacked options and full-width primary button.
- Both low-data and dark-mode behavior remain usable.
- No fake statistics, invented question count totals, streaks, progress, or generic “AI” claims.
- Use real text for time; remove the confusing time rings.
- Avoid double explanations and duplicated links.

## Implementation protocol

1. Read `AGENTS.md`, `docs/CODEX_HANDOFF_PLAN.md` and `docs/DESIGN_IMPLEMENTATION_BRIEF.md`.
2. Implement through reusable React components, preserving guest and auth routes.
3. Update `docs/CHANGES_SINCE_BASELINE.md` in the same behavioral change.
4. Run: `npm run types:check`, `npm run lint:check`, `npm run format:check`, `npm run test:js`, `npm run build`, `npm run size`, `php artisan test`.
5. Show real desktop (1440 px) and mobile (390 px) **browser screenshots** of the running application before concluding.
6. Do not confuse this homepage redesign with the authenticated user dashboard or the Focused Learning Canvas actual question screen.

## Definition of done

Within three seconds a new user understands:
**Which exam do I need? How long is it? How many scored questions? What does the button do?**

The first viewport presents a legitimate task flow and little else. The finished screen feels intentionally designed and is distinguishable from Hiraya, a generic government portal, and generated SaaS dashboards.
