# Civio Design Research & Anti-AI-Slop Standard

**Status:** Required design gate before major frontend redesign  
**Date:** 13 Oct 2026 (Asia/Manila)  
**Repo:** `Vincenzo-OPC/Civio`

Civio must not accept a generated dashboard simply because it is clean, modern, or uses the correct colors. The current visual direction still risks looking like generic AI-generated SaaS: rounded white cards, a sidebar, a right rail full of widgets, violet CTAs, lime progress, and too many interchangeable feature blocks.

Before major UI implementation, the designer/agent must perform a short **reference and design-principle audit** and show its reasoning at the product/design level.

---

## 1. The problem to solve

Civio is not a dashboard. It is a learning product.

The core learner loop is:

**Read → Answer → Learn → Next**

Every screen must make that loop more obvious, not less.

AI-generated web layouts often converge on the same visual clichés:
- left sidebar + top bar + card grid
- large border-radius everywhere
- every feature in its own rounded card
- decorative gradients
- pill tabs
- icon + label tiles
- excessive whitespace without hierarchy
- “premium SaaS” styling that does not express the product
- dashboards full of widgets that merely prove features exist

Civio should avoid this convergence.

---

## 2. Required external reference audit

Before redesigning the core learner experience, inspect real products and design literature. Do not copy any one product. Extract principles.

Create a short matrix:

| Reference | What works | What Civio should borrow | What Civio should NOT copy |
|---|---|---|---|

At minimum, study:

### Product/UI references

**Linear (2026 UI refresh)**
- calmer interface
- consistent headers and controls
- dimmer navigation so content dominates
- pruning accumulated UI complexity
- predictable placement of actions

**Notion**
- neutral visual system
- typography and content first
- progressive disclosure
- low visual noise
- tools appear when needed

**Brilliant**
- learning interaction over dashboard decoration
- problem-first experience
- active participation
- immediate feedback
- visual explanation only where it teaches

**Khan Academy / Khanmigo**
- instructional clarity
- guided learning
- AI as tutor, not decoration
- progress and mastery remain understandable

**Quizlet / modern flashcard products**
- fast study loops
- mode switching
- low-friction repetition
- clear answer/review states

**Stripe / Linear / Vercel-level product craft**
- spacing precision
- typography hierarchy
- restrained borders
- consistent interaction patterns
- detail quality

### Philippine / exam context references

Also inspect:
- current Philippine CSE reviewer apps
- local review-center websites/apps
- government forms/portals only to understand familiar terminology and accessibility problems
- CSC materials to understand information density, not to imitate CSC branding

Civio must remain visibly independent from CSC.

---

## 3. Design philosophy references

Use these as principles, not as visual templates.

### Dieter Rams / Braun: “Less, but better”
Ask for every visible element:
- Is this useful right now?
- Is it understandable?
- Can it disappear until needed?
- Does it compete with the learner’s task?

### Swiss / International Typographic Style
Borrow:
- strong grid
- typographic hierarchy
- clarity
- alignment
- restrained palette
- information over ornament

Do not turn it into a poster aesthetic.

### Progressive disclosure
Primary actions should be visible.
Secondary/advanced actions should appear only when needed.

For Civio:
- Question
- Answers
- Reveal
- Ask Tutor
- Next

Everything else should be secondary or contextual.

### Gestalt principles
Use proximity, grouping, similarity, and hierarchy so the user understands structure before reading labels.

### Hick’s Law
Do not expose too many choices at once.

### Fitts’s Law
Frequent actions need large, obvious targets.

### Cognitive load
The learner is already solving a question. The interface should not ask them to solve the interface too.

### Recognition over recall
Navigation and modes should be obvious and consistent.

---

## 4. Research current professional UX guidance

Use current UX guidance, including:

- Nielsen Norman Group on application UX, progressive disclosure, visual hierarchy, and minimizing visual search
- contemporary dashboard/UI criticism from respected design publications
- current platform HIG/design systems where relevant

Do not blindly implement a design system. Use them to validate usability decisions.

---

## 5. Use AI design tools as critics, not as aesthetic authority

If available, consult more than one design-generation/refinement tool.

Possible tools:
- Figma Make / Figma Agent
- v0
- Relume
- other current UI-generation or critique tools

Recommended process:

1. Give each tool the same Civio UX brief.
2. Generate at least 3 materially different directions.
3. Do not choose the prettiest screenshot immediately.
4. Compare them against:
   - task clarity
   - hierarchy
   - cognitive load
   - originality
   - mobile behavior
   - accessibility
   - build feasibility
   - separation from generic reviewer layouts
5. Take useful ideas, then redesign manually/agentically into one coherent Civio system.

Generated outputs are **references**, not production designs.

If all generated directions look like generic SaaS dashboards, reject all of them.

---

## 6. Mandatory anti-slop critique

Before presenting a design, answer:

1. If the Civio logo and colors were removed, would this still look recognizably like Civio?
2. Does it look like a learning product or a SaaS admin dashboard?
3. Is the main question unquestionably the focal point?
4. How many competing visual blocks are visible?
5. Is there a card around content that does not need a card?
6. Are rounded rectangles being used as a substitute for hierarchy?
7. Are icons adding meaning or merely decorating labels?
8. Is lime communicating a semantic state, or merely adding excitement?
9. Is purple carrying brand/action hierarchy consistently?
10. Could a first-time CSE taker use the screen without explanation?
11. Does the user know what to do next within 2 seconds?
12. Is the right rail actually necessary?
13. Does the layout still resemble a generic reviewer?
14. Does mobile preserve the same clarity rather than shrink desktop?
15. Is every persistent widget worth stealing attention from the question?

If several answers are weak, redesign before coding.

---

## 7. Explore non-dashboard layouts

The agent must not assume Civio needs:
- a permanent left sidebar
- a permanent right sidebar
- a grid of cards
- a dashboard shell

Explore at least three structural concepts.

### Direction A: Focused learning canvas
- thin global navigation
- centered question canvas
- contextual bottom/side drawer
- almost no persistent secondary widgets

### Direction B: Split learning workspace
- question on left/center
- contextual tutor/review pane appears only after user asks
- navigation collapses when studying

### Direction C: Session-first layout
- start a study session
- full-screen problem flow
- progress at top
- tools emerge contextually
- resembles a deliberate learning environment more than an app dashboard

Compare these before deciding.

---

## 8. Civio’s visual identity should come from behavior, not decoration

Civio should become recognizable through:

- consistent question rhythm
- distinctive answer-state behavior
- clear mastery language
- Study vs Simulation contrast
- spelling production workflow
- source-grounded explanation cards
- Smart Review concept summaries
- restrained violet/lime semantics
- typography
- motion restraint
- unique microcopy

Not from:
- gradients
- blobs
- glowing cards
- AI sparkles everywhere
- a custom icon on every tile

---

## 9. Color standard

Working palette direction remains:

- warm white / off-white base
- near-black / ink text
- Civio violet as brand/current/action
- acid lime as success/mastery/resume
- neutral grays for structure
- red only for wrong/destructive/error
- amber only for caution/bookmark if needed

Purple and lime must not be 50/50.

Recommended visual balance:
- ~75% neutral/light
- ~15% ink/structure
- ~7% violet
- ~3% lime

The CU convenience-store reference is color inspiration only. Do not reproduce CU’s retail saturation or magenta.

---

## 10. Typography and density

Use typography to create hierarchy before adding cards.

Requirements:
- readable body size
- strong question type
- clear labels
- line lengths suitable for exam reading
- consistent numeric/timer typography
- limited type scale
- no tiny metadata
- avoid all-caps except rare micro labels

Study screens can be spacious.
Simulation screens should be denser but calmer.

---

## 11. Motion

Motion should explain state.

Use only for:
- answer feedback
- opening Tutor/Notebook
- progress completion
- pause/resume
- subtle navigation context

Avoid:
- floating decorations
- glow pulses
- constant progress animation
- bouncy cards
- gratuitous page transitions

Support reduced motion.

---

## 12. Design deliverable before coding

Before major implementation, provide:

1. reference matrix
2. anti-slop critique of the current Civio mock
3. structural comparison against a generic reviewer
4. three materially different wireframe/layout directions
5. one recommended direction and why
6. desktop study screen
7. desktop strict simulation screen
8. mobile study screen
9. mobile simulation screen
10. design tokens
11. component hierarchy
12. interaction-state map
13. accessibility check
14. what was deliberately removed from the old interface

Do not move to full implementation merely because one generated mock “looks modern.”

---

## 13. Current external design references checked

- Linear 2026 UI refresh: calmer, more consistent UI, predictable controls, dimmer sidebar to emphasize content.
- Nielsen Norman Group: progressive disclosure, visual hierarchy, minimizing visual search, learnability in complex applications.
- Figma Make / Figma Agent: useful for generating multiple interactive directions and refining actual design systems/components, but output must be curated rather than accepted automatically.
- Current dashboard/UX literature: overcrowding and flat hierarchy increase cognitive load; visual design should guide attention toward the next decision.

These references validate the central Civio principle:

> **The product should remove decisions from the learner, not add more interface decisions around the exam question.**
