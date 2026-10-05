# Civio AI Study, Tutor, UX & Spelling System

**Status:** Product direction / implementation brief  
**Date:** 5 Oct 2026 (Asia/Manila)  
**Owner:** GT  
**Repo:** `Vincenzo-OPC/Civio`

Civio should feel like a modern learning product, not a static reviewer with an AI button bolted onto it. The core product is the practice engine. AI behaves like a teacher sitting beside the learner when useful, while Live Simulation stays clean and exam-like.

---

## 1. Product principles

1. **Idiot-proof by design.** The interface is for a broad Philippine CSE audience, including first-time test takers and users who are not highly technical. Every important action should be obvious without onboarding.
2. **Study Mode and Live Simulation are different products.**
   - Study Mode teaches.
   - Live Simulation measures.
3. **Do not make AI decorative.** Replace static "Reveal Answer" behavior with a contextual tutor that can explain, question, retry, generate practice, and remember weak concepts.
4. **Free-first.** Core study features work without a paid AI provider. AI degrades gracefully to deterministic explanations and local/static features.
5. **Fast first.** No AI request should block ordinary question navigation, scoring, pausing, or review.
6. **Accessible visual language.** Mostly white / very light neutral surfaces, near-black text, restrained violet as the primary brand/action color, and neon-lime only for success, active progress, pause/resume, or mastery. No loud gradients, glassmorphism, gaming-dashboard clutter, or unnecessary neon.
7. **Teach the skill, not the answer.** Wrong answers should trigger active recall, correction, and a transfer question whenever practical.
8. **Question-bank integrity.** Live Simulation must never expose answer keys or explanations in the initial exam payload.

---

## 2. Brand and visual direction

**Working product name:** Civio.

Do not use Civix as the public brand. The repo and product currently use **Civio**.

### Visual system

- White / soft-gray background
- Near-black navy text
- Primary: clean violet
- Accent: neon lime, used sparingly
- Thin borders, generous whitespace, large readable type
- Subtle depth only where hierarchy needs it
- No strong gradients
- No glowing sci-fi cards
- No excessive rounded pills
- No "crypto dashboard" aesthetic
- Keep the earlier simple two-stroke / abstract lime mark as the preferred logo direction until branding is finalized
- Product should look credible beside modern global learning and productivity SaaS, not like a government portal

### Color meaning

- Violet = primary action / current item / selected state
- Lime = success / mastery / resume / on-track
- Red = destructive / serious error only
- Amber = warning / needs review
- Neutral gray = unanswered / secondary metadata

Do not use multiple bright colors to decorate the same screen.

---

## 3. Exam shell redesign

### Header

Keep only:
- Civio logo
- mode: Study or Live Simulation
- level: Professional / Subprofessional
- current category
- calculator
- notes
- focus
- pause
- exit

Avoid duplicating timers, progress percentages, or answered counts in multiple places.

### Progress

Replace the giant "Question Palette" as the primary navigation model.

Preferred model:
- a compact **question rail / scrubber**
- current question is obvious
- answered, unanswered, and flagged states visible at a glance
- show a local window around the current question, e.g. 66–85
- arrows or a small drawer can jump elsewhere
- optionally offer "All questions" in a collapsible navigator
- do not render 145 equally prominent squares by default

The learner should spend attention on the question, not on a spreadsheet of numbered boxes.

### Main question area

Order:
1. category / question type
2. question stem
3. choices
4. primary navigation
5. optional study controls

Large tap/click targets. Whole answer row is clickable. Keyboard shortcuts are optional but must not be required.

### Pause

Live Simulation must have a clear **Pause** control.

When paused:
- freeze countdown immediately
- freeze per-item timing
- autosave current selection, flag state, notes, and current question
- show a calm full-screen or large modal pause state:
  - "Exam paused"
  - exact remaining time
  - "Resume Exam"
  - optional "End Exam"
- prevent accidental question interaction behind the pause layer
- resuming returns to the exact item and state
- session recovery should preserve paused state after accidental refresh where feasible

Do not continue the timer while the learner eats, takes a bathroom break, answers a call, etc.

---

## 4. Two-mode learning model

## Live Simulation

Goal: approximate actual exam pressure.

During active play:
- timer
- pause
- flag
- notes
- calculator only if Civio intentionally provides it as practice convenience, but label exam-policy differences clearly
- question navigation
- no tutor
- no hints
- no similar-question generator
- no answer reveal unless simulation settings explicitly allow "practice simulation"

Recommended default: **no answer reveal until submission**.

After submission:
- score
- category breakdown
- timing analysis
- wrong answers
- flagged questions
- tutor becomes available for review

## Study Mode

Goal: learning and mastery.

Available:
- instant feedback
- contextual tutor
- hint ladder
- explain simply
- why my answer is wrong
- teach the rule
- similar question
- spaced repetition
- weakness-based sequencing
- alternate-language explanation
- retry before full reveal

The user should never have to understand which model/provider is active to learn effectively.

---

## 5. Replace "Reveal Answer" with a teaching flow

Static Reveal is too weak.

After the learner commits an answer in Study Mode, Civio should show a compact result state:

**Correct**
or
**Not quite**

Then the learner gets one primary action:

**Ask Tutor ✦**

Suggested quick actions:
- Give me a hint
- Explain simply
- Why is my answer wrong?
- Teach me the rule
- Show the shortcut
- Give me a similar question
- Explain in Taglish
- Quiz me again

Below that is a normal message composer:

> Ask anything about this question…

The tutor automatically receives structured context:
- question ID
- category/subcategory
- exact stem
- options
- learner's answer
- correct answer
- canonical explanation
- target skill/rule
- prior attempts on the same skill
- timing on this question
- learner's selected explanation language
- whether the answer is currently allowed to be revealed

### Hint ladder

Do not jump straight to the answer.

**Hint 1:** point attention to the relevant feature/rule.  
**Hint 2:** explain the concept without naming the answer.  
**Hint 3:** walk through the reasoning.  
**Reveal:** show the answer and explanation only after explicit request or after the configured attempt threshold.

This makes AI useful as a tutor rather than an answer dispenser.

---

## 6. Conversational tutor behavior

Working tutor name can remain **Dexter** unless branding changes later.

The tutor should support normal conversational follow-up:
- "Hindi ko gets."
- "Explain like I'm 12."
- "Bakit mali ang B?"
- "Ano dapat tandaan ko sa exam?"
- "Give me another example."
- "Tagalog please, but keep the English grammar rule."
- "Quiz me without showing the answer."
- "I keep forgetting this word."

### Tutor response contract

Default response should be short:
1. direct explanation
2. one memorable rule or shortcut
3. one micro-check / question back to the learner

Do not dump an essay unless the learner asks.

### Socratic mode

For reasoning, grammar, math, filing, and similar skills:
- ask the next useful question
- do not reveal the entire solution immediately
- detect where the learner's reasoning diverged
- give one step at a time
- after success, create a fresh transfer item

### Teach → Test loop

One tap should support:
1. 20–60 second micro-lesson
2. one worked example if needed
3. one fresh test item
4. result
5. schedule the concept for later review if weak

---

## 7. Spelling should not be taught like ordinary multiple choice

Spelling is a production skill. Recognition alone creates false confidence.

Civio needs a dedicated **Spelling Coach** inside Clerical Ability.

### Simulation format

Live Simulation should still mimic the intended CSE item style in the approved question spec.

### Study format

Preferred spelling study loop:

1. **Hear it**
   - play the target word using browser speech synthesis first
   - optionally play it inside a sentence
2. **Type it**
   - learner types the spelling from memory
   - no visible answer choices on the first attempt
3. **Commit**
   - answer must be submitted before any letter-level help appears
4. **Diagnose**
   - compare typed form with the target
   - highlight the exact missing, extra, transposed, or substituted letters
5. **Teach**
   - show a short pattern, chunk, syllable/morpheme cue, or memory hook
6. **Retype**
   - hide the correct spelling and require the learner to type it again correctly
7. **Transfer**
   - use the word in a new sentence or contrast it with a confusable spelling
8. **Schedule**
   - send it into spaced repetition based on performance

### Example

Target: **accommodate**

Learner types: `acomodate`

Bad feedback:
> Wrong. Correct answer: accommodate.

Civio feedback:
> You're missing one **c** and one **m**: **ac + com + modate**.  
> Think: **AC COM**modate = double C, double M.

Then hide the answer:

> Type it again from memory.

After a correct retry:

> Good. Now spell it once more from audio only.

The purpose is retrieval, not recognition.

### Error taxonomy

Store spelling mistakes by type:
- omitted letter
- added letter
- doubled-letter error
- transposition
- vowel confusion
- suffix/prefix error
- homophone/confusable
- capitalization
- hyphenation
- unknown pattern

This lets Civio say:
> You are not generally "bad at spelling." Most of your misses are doubled consonants and -ance / -ence endings.

That is actionable.

### Progressive help

Attempt 1:
- audio + sentence only

Attempt 2:
- syllable/chunk count or first letter

Attempt 3:
- reveal difficult chunk only

Final help:
- full spelling + explanation

Then require a clean retype.

Never leave the learner after passively reading the revealed answer.

### Confusion sets

Build groups such as:
- separate / desperate
- privilege / prestigious
- maintenance / maintain
- accommodate / accommodation

Use carefully curated sets. AI may suggest candidates, but canonical word lists and definitions should be verified before entering the permanent bank.

### Mnemonics

AI can generate personalized memory hooks, but:
- label them as memory tricks
- do not invent fake etymology
- prefer short visual/verbal patterns
- allow learner to save their own mnemonic

### Audio

Free-first implementation:
- browser `speechSynthesis` for basic pronunciation
- sentence context displayed in text
- allow replay
- allow slower replay where supported
- provide text-only fallback for accessibility

Later optional providers can improve voice quality, but core spelling practice must not depend on paid TTS.

---

## 8. Spaced repetition and mastery

Use the existing FSRS direction as the scheduling base.

Track at least:
- item ID
- concept / rule
- category
- attempts
- first-try correctness
- assisted correctness
- number of hints
- response time
- confidence
- last seen
- next review
- mastery estimate

For spelling, schedule the **word + underlying pattern**, not only the exact item.

Example:
- missed `accommodate`
- schedule `accommodate`
- also tag `double consonants`
- later test a different word with the same difficulty pattern

A learner should not "master" a word merely because they recognized it from four choices.

---

## 9. Mistake Memory

Civio should maintain a user-facing weakness model.

Examples:
- Pronoun case: 63%
- Filing order: 91%
- Spelling, double consonants: 48%
- Spelling, suffixes: 70%
- Number sequences: 55%
- RA 6713 concepts: 82%

AI uses this context to teach, but the underlying mastery data should be deterministic and queryable without AI.

### Smart Review

Do not only offer:
> Review 18 wrong questions

Prefer:
> 5 concepts need work

Then cluster mistakes by concept:
- double consonants
- pronoun case
- percentage word problems
- alphabetical filing edge cases
- public-official prohibited acts

Review should mix:
- original misses
- new transfer items
- spaced recall
- one final mastery check

---

## 10. AI provider architecture

Civio already has provider abstraction direction. Extend it rather than coupling the UI to one vendor.

Suggested layers:

`Tutor UI → Tutor orchestration → provider adapter → provider`

Providers:
1. deterministic / no-AI fallback
2. Gemini
3. OpenAI
4. xAI/Grok if desired
5. Claude if desired
6. local/stub for development

Never expose provider API keys in client code.

### Provider-agnostic capabilities

The frontend should request a capability:
- explain
- hint
- Socratic turn
- similar item
- simplify
- translate/explain in Taglish
- generate mnemonic
- summarize weakness
- generate micro-lesson

It should not hard-code "call Gemini" or "call OpenAI".

---

## 11. Sign in with ChatGPT readiness

OpenAI's current **Sign in with ChatGPT** supports identity, and eligible integrations can let eligible users use their ChatGPT plan for supported AI requests without manually pasting an API key.

Important current constraint:
- website/commercial access is still limited to selected partners / trial
- open-source plan-usage flows have a documented path
- therefore Civio should be architecturally ready, but must not make the feature a launch dependency

Prepare now:
- provider adapter for OpenAI Responses API
- account connection table capable of storing provider + external subject + scopes
- feature flag: `OPENAI_SIWC_ENABLED`
- UI slot in Settings → AI Connections
- "Continue with ChatGPT" only when actually approved/configured
- when ChatGPT plan usage is active, show a small "Using ChatGPT plan" state near the tutor composer/settings
- never imply ChatGPT connection grants access to the user's ChatGPT conversations

Fallback if unavailable:
- Gemini free tier or deterministic tutor

References checked 5 Oct 2026:
- https://developers.openai.com/siwc/quickstart
- https://developers.openai.com/siwc/website
- https://developers.openai.com/siwc/token-sharing-open-source
- https://developers.openai.com/siwc/ui-ux-guidelines

---

## 12. Gemini free-first role

Gemini is a practical default/fallback because the Gemini Developer API has a free tier for supported models and tools.

Use cases:
- short question explanations
- Socratic tutor turns
- similar-question drafts
- Taglish/simple-English transformations
- mnemonic drafts
- weak-concept summaries
- grounded study chat over approved materials

### File Search

Gemini File Search can support a lightweight Notebook-style experience:
- index Civio's approved lessons
- official CSC scope documents
- Constitution / RA 6713 source material
- admin-approved study notes
- optionally user-uploaded notes later

Use retrieval so tutor answers can cite the approved source context instead of hallucinating from model memory.

Do **not** depend on Gemini Notebook / NotebookLM as a product integration. Recreate the useful interaction pattern inside Civio with our own corpus + retrieval layer.

References checked 5 Oct 2026:
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/file-search

---

## 13. Notebook / source-grounded study mode

Future module:

**My Notebook**
- upload PDF / notes
- create study set
- ask questions about sources
- generate summary
- generate flashcards
- generate practice questions
- ask "where did this come from?"
- save source-linked notes

For official-law/general-information study, prefer grounded answers with citations to the source excerpt.

Do not silently mix user-uploaded material into the global Civio question bank.

---

## 14. Free-first feature ladder

### Tier 0: no AI required

Works for everyone:
- exam simulations
- pause/resume
- deterministic explanations
- question review
- spelling audio using browser speech synthesis
- letter-diff feedback
- retries
- FSRS
- analytics
- mistake taxonomy
- saved notes
- static shortcuts/rules

### Tier 1: free/low-cost AI

When provider quota is available:
- conversational explanations
- Socratic tutoring
- Taglish/simple-English explanations
- mnemonic generation
- similar-question drafts
- weakness summaries
- grounded file chat

### Tier 2: user-connected AI

When integrations are available:
- use the learner's connected ChatGPT plan where eligible
- optional future provider connections
- always show which connection is active
- no API-key copy/paste requirement for Sign in with ChatGPT

Civio must remain useful if every AI provider is unavailable.

---

## 15. Tutor safety and question-bank quality

AI-generated content is **ephemeral by default**.

A generated similar question may be used for the current learner, but it does not enter the canonical shared bank automatically.

Permanent bank flow:
1. AI/human draft
2. validation
3. duplicate check
4. factual/key verification
5. style check against `CSE-Question-Design-Spec.md`
6. admin approval
7. publish

For spelling:
- use a canonical dictionary / curated word source where possible
- never trust AI alone for the official spelling, definition, pronunciation, or etymology
- AI may explain an approved answer but should not redefine the answer key

---

## 16. Data model additions to consider

### `learning_events`
- user_id
- question_id
- concept_id
- mode
- answer_state
- correct_first_try
- correct_after_help
- hints_used
- response_ms
- provider_used
- created_at

### `concepts`
- id
- category
- subcategory
- slug
- title
- canonical_rule
- metadata

### `question_concepts`
- question_id
- concept_id
- weight

### `spelling_items`
- question_id or word_id
- canonical_word
- pronunciation_hint
- example_sentence
- chunks
- confusable_group
- error_patterns
- verified_at
- verified_by

### `user_concept_mastery`
- user_id
- concept_id
- mastery_score
- due_at
- streak
- lapse_count

### `ai_connections`
- user_id
- provider
- external_subject
- encrypted token/reference fields as appropriate
- scopes
- plan_usage_enabled
- expires_at

Exact schema should be reconciled with the current code before migration.

---

## 17. AI tutor UX states

### Before connection

**AI Tutor**  
Ask about this question.

If Gemini/free provider is enabled:
- just work without forcing account connection

If optional ChatGPT connection is available:
- Settings → AI Connections → **Continue with ChatGPT**

### In conversation

Composer placeholder:
> Ask anything about this question…

Tiny context label:
> Question 70 · Clerical Ability

Optional provider state:
> Using Civio AI
or
> Using ChatGPT plan

Do not put a giant provider logo in the learning flow. Civio is the product.

### Failure state

If AI fails:
> Tutor is unavailable right now. Your saved explanation is still available.

Then show deterministic explanation immediately.

Never strand the learner behind a loading spinner.

---

## 18. Accessibility and low-friction UX

- plain labels over clever labels
- visible text with icons, not icon-only controls for core actions
- minimum comfortable touch targets
- strong contrast
- readable font sizes
- keyboard support
- focus states
- screen-reader labels
- text-size control
- reduced-motion support
- do not communicate answer state by color alone
- confirmation only for destructive actions, not routine navigation

Preferred wording:
- Pause Exam
- Resume Exam
- Flag for Review
- Notes
- Previous
- Next Question
- Ask Tutor
- Try Again
- Show Answer

Avoid jargon like:
- inference
- context window
- retrieval
- provider routing
- model credits

Those belong in developer/admin settings only.

---

## 19. Priority build order

### P0
- preserve/fix scoring and answer-key security
- ensure current desktop/MSI tree is the correct build base
- keep local study environment stable

### P1: exam UX
- clean Civio visual system
- pause/resume
- question rail / compact navigator
- remove redundant dashboard widgets
- simplify header
- responsive/mobile behavior
- accessible controls

### P2: Study Mode
- Ask Tutor panel
- hint ladder
- deterministic fallback
- Teach → Test
- quick prompts
- Taglish/simple-English explanation

### P3: Spelling Coach
- audio → type → diagnose → retype → transfer
- browser TTS
- letter diff
- error taxonomy
- FSRS scheduling
- confusion groups
- concept mastery

### P4: Adaptive learning
- Mistake Memory
- concept graph
- Smart Review
- weakness-driven practice
- fresh transfer items

### P5: AI connections
- provider abstraction cleanup
- Gemini production fallback within safe quotas
- source grounding / File Search
- OpenAI Sign in with ChatGPT feature-flagged readiness
- settings UI for provider connection status

### P6: Notebook-style study
- source uploads
- grounded Q&A
- flashcards
- summaries
- practice generation
- source-linked notes

---

## 20. Acceptance tests for the new direction

A build should not be considered successful just because it looks good.

### Exam
- pausing freezes all relevant timers
- refresh/recovery does not silently lose attempt state
- answer keys are not present in active exam payload
- navigation works without a 145-square wall
- one-handed/mobile use is practical

### Tutor
- tutor knows the current question and user's selected answer
- learner can ask follow-up questions naturally
- deterministic fallback appears if provider fails
- Live Simulation does not leak tutor/reveal unless settings allow it
- similar generated items never auto-publish to the bank

### Spelling
- first attempt can require typed recall
- audio can be replayed
- exact letter difference is shown
- learner must retype after reveal
- error type is recorded
- a future review is scheduled
- a later transfer check can test the same spelling pattern with a different item

### Visual
- no loud gradient dashboard
- violet and lime have semantic roles
- main question is the visual focus
- controls use plain language
- works for a first-time user without explanation

---

## 21. Product north star

Civio should not become "a CSE website with ChatGPT."

It should become a **Civil Service learning operating system**:

**diagnose → teach → practice → test → remember → retest**

The AI layer should make that loop feel personal and conversational. The deterministic learning engine should make it reliable even when AI is unavailable.
