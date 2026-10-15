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
- `resources/js/components/domain/exam-level-picker.tsx` currently includes a decorative `TimeDial` and a line saying the ring shows duration. Replace the ring with **150 Questions / 3 hr 10 min** and **145 Questions / 2 hr 40 min** as consistently spaced real text. Preserve keyboard-controlled radiogroup and accessible state.
- `resources/js/components/domain/exam-screen-preview.tsx` is a static screenshot with question 1/150; REMOVE IT FROM THE PUBLIC HOME. The component can remain if still used elsewhere.
- `resources/js/components/domain/exam-format.tsx` currently shows an 80.00 circle, duplicates exam data and makes rating resemble score. Replace its homepage use with compact non-graphical CSC facts, or remove this component from the homepage.
- `resources/js/lib/exam-dials.ts` is the existing source of truth for item counts, duration, and descriptions. Reuse it.
- `resources/js/components/layout/site-header.tsx` and `site-footer.tsx` control header/footer. Simplify the homepage header if necessary without breaking other pages.

## Locked Homepage Microcopy and Typography Standard (15 October refinement)

The copy below **supersedes all prior wording** for this homepage. Do not restore the old prototype copy. Treat capitalization, punctuation, word spacing, and label casing as product-design decisions.

### Rules

- Product brand: **Civio**, never `CIVIO`, `Civio.`, or `Civio.CSE REVIEWER`. No added brand dot.
- In the brand lockup only, the tiny secondary line may read **CSE REVIEWER**, uppercase with tracking and a visible gap beneath the name.
- Eyebrow/overline: all caps, but only for one short micro-label such as **PHILIPPINE CIVIL SERVICE EXAM**. Keep font size and tracking intentionally restrained.
- Page title, headings, form labels, option names, navigation and buttons: **Title Case**. E.g. `Choose Your Exam`, `Time Limit`, `Practice by Topic`, `Sign In`, `Create Account`.
- Sentences/paragraphs, explanations, notes and legal text: **sentence case**; do not Title Case every word in prose.
- No decorative punctuation on page titles: **Choose Your Exam**, not `Choose your exam.`.
- Timing: always **3 hr 10 min** and **2 hr 40 min** in homepage UI (space before/after units). Do not mix `3h 10m`, `3 hours 10 minutes`, and `3 hr 10 min` in the same surface.
- Counts: keep the number and unit visually separate, e.g. **150** / **Questions**, with explicit layout gap, never `150Questions` or `150 questions3h 10m`.
- Control/metadata groups must have consistent baseline, gap, font size, and weight. Avoid arbitrary uppercase, broken responsive wrapping, icons touching text, or glued-together links.
- Remove duplicated helper labels, numbering like `01 / LEARN`, repeated destinations, and verbose reassurance.
- No feature claims on homepage that aren't implemented; avoid decorative AI badges, fake metrics and generic motivational copy.

### Exact Content Order

Header wordmark: **Civio**  
Optional tiny wordmark subtitle: **CSE REVIEWER**

Header account actions:
- **Sign In**
- **Create Account**

Eyebrow (uppercase micro-label):
`PHILIPPINE CIVIL SERVICE EXAM`

H1: **Choose Your Exam**

One-sentence introduction:
`Choose your exam level and start practicing with a full-length mock.`

Two selectable exam levels, **without** redundant "Exam Level / Select One to Continue" headings:

**Professional**
`For professional, technical, and supervisory positions.`
- `150` + `Questions`
- `3 hr 10 min` + `Time Limit`

**Subprofessional**
`For clerical, trades, and custodial positions.`
- `145` + `Questions`
- `2 hr 40 min` + `Time Limit`

Dynamic primary CTA:
- **Set Up Professional Mock** (when Professional is selected)
- **Set Up Subprofessional Mock** (when Subprofessional is selected)

Secondary destination: **Practice by Topic** → `/drills`.

Helper sentence:
`Choose Study Mock or Strict Mock on the next screen.`

Secondary editorial section H2:
**Three Ways to Prepare**

Three minimal text columns, **no numbered pre-labels, feature cards or duplicate links**:
- **Study Mock:** `Answer questions and reveal explanations as you go.`
- **Strict Mock:** `Practice against the clock. Review answers after submission.`
- **Practice Drills:** `Focus on one skill at a time and strengthen weak areas.`

Quiet informational section:
- Heading: **About the Exam**
- Copy: `The CSC publishes a general passing rating of at least 80.00. Civio mocks include only the scored questions, excluding the separate 20-item Examinee Descriptive Questionnaire. Civio is independent and not affiliated with the CSC.`
- Link: **CSC Exam Reference**

Footer:
`© 2026 Civio. All rights reserved.`
- **Terms**
- **Privacy**
- **Support**

### Visual Composition Requirements

- One restrained header with brand left and account actions right. Do not replicate a second top-level nav on this public entry page if it dilutes the single exam-choice task.
- On desktop, title/description can live left of the two-level selector; on mobile, stack them naturally. Do not add a decorative sidebar, screen preview or information rings.
- Selected radio gets a violet border and explicit checked marker, not lime.
- Title Case labels must remain legible and not become tiny all-caps labels to save space.
- Keep both **Sign In** and **Create Account** accessible on mobile without collision or horizontal scrolling.
- Keep CSC facts and independence disclosure visually quiet, below the primary action.

Route must preserve existing `/exams?start=professional` and `/exams?start=subprofessional` and appropriate guest free-attempt behavior.

If an authenticated learner has a genuinely resumable session, show **Resume Studying** contextually with a real resume destination. Do not imply that `/exams` guarantees resumption when no session exists.

## Learning Modes Versus Homepage

Study Mode contains Reveal, optional AI Tutor and Copy for AI. Strict Mock hides answers and explanations until submission. These modes should be explained concisely on the homepage, not rendered as static faux exam screen.

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

The first viewport presents a legitimate task flow and little else. The finished screen feels intentionally designed and is distinguishable from a generic government portal and from generated SaaS dashboards.
