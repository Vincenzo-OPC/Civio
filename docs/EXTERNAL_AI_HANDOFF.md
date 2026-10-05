# Civio External AI Handoff

**Status:** Product / UX specification  
**Date:** 5 Oct 2026 (Asia/Manila)  
**Repo:** `Vincenzo-OPC/Civio`

## Decision

Civio should support a lightweight **external AI handoff** for learners who already like discussing questions in ChatGPT, Claude, Gemini, Grok, or another assistant.

This is separate from Civio Tutor.

The point is not to force an account connection. It is to make the user's existing workflow one click instead of manually highlighting question text, copying choices, copying the reveal, and rebuilding context in another AI app.

## Recommended UX

Default button:

**Copy for AI**

After copying, show a small toast:

> Copied with context. Paste into ChatGPT, Claude, Gemini, or Grok.

If the learner has chosen a preferred external assistant in Settings, the label may become:

**Discuss in ChatGPT**

or

**Discuss in Claude**

etc.

When browser/platform behavior allows it, the action may:
1. copy the structured context to the clipboard, then
2. offer/open the user's preferred AI destination in a new tab.

Do not depend on undocumented URL-prefill behavior. Clipboard export is the universal fallback.

## Why this belongs beside Civio Tutor

Three valid learner paths should coexist:

1. **Reveal Answer**  
   Zero-token, instant, deterministic.

2. **Ask Tutor**  
   In-app contextual AI, powered by whatever provider Civio can use.

3. **Copy for AI / Discuss externally**  
   User takes the structured question context to ChatGPT, Claude, Gemini, Grok, or another assistant they already use.

This avoids making Civio's learning experience dependent on:
- a ChatGPT subscription
- Gemini quota
- Civio's own AI budget
- provider downtime
- any single AI vendor

## Placement

In Study Mode, preferred compact row:

`Reveal Answer` · `Ask Tutor` · `Copy for AI`

Secondary actions can stay behind More / Tutor:
- Hint
- Explain Simply
- Similar Question
- Save to Notebook

Do not add five provider-branded buttons directly under every question.

## Clipboard payload

The copied payload should be **Markdown**, readable by any modern AI assistant.

Example:

```md
I'm studying for the Philippine Civil Service Exam.

Level: Subprofessional
Mode: Study
Category: Clerical Ability
Skill: Filing
Question: 70 of 145

QUESTION
Which label best identifies approved travel claims for the second quarter of 2027?

OPTIONS
A. Travel
B. Claims maybe
C. Approved Travel Claims, Q2 2027
D. Second

MY ANSWER
C. Approved Travel Claims, Q2 2027

RESULT
Correct

CIVIO VERIFIED EXPLANATION
[canonical explanation here]

SOURCE / RULE
[verified source or Civio rule, if relevant]

MY NOTE
[optional learner note]

Please act as a tutor. Do not just repeat the answer. Explain the underlying rule clearly, identify what I should remember for the CSE, and give me one short similar question to check whether I understood it.
```

## Before Reveal

If the learner has **not** revealed/submitted the answer, do not leak:
- correct option
- canonical answer
- hidden explanation

Payload example:

```md
I'm studying for the Philippine Civil Service Exam.

Level: Subprofessional
Category: Clerical Ability

QUESTION
...

OPTIONS
...

MY CURRENT ANSWER
B

I have not revealed the correct answer yet. Tutor me without giving the answer immediately. Start with one useful hint.
```

## After Reveal

After Reveal, include:
- chosen answer
- correct answer
- canonical explanation
- rule / source
- learner note if they opt in
- weakness/concept tag where useful

## Simulation behavior

True Live Simulation should not provide an external AI handoff during active play by default.

Recommended:
- disable or hide `Copy for AI` while a strict simulation is running
- allow it after submission/review
- optionally permit it in an explicitly labeled **Practice Simulation** setting

This preserves the distinction:

**Study teaches. Simulation measures.**

## Privacy controls

Default copied context should include only what is needed for the learning task.

Do not include automatically:
- real name
- email
- account ID
- full study history
- private uploaded documents
- unrelated notes
- hidden profile data

If the learner chooses **Copy full study context**, preview exactly what will be copied.

## Copy variants

Keep the default action simple. Advanced options may sit in a dropdown:

### Copy question
Question + choices only.

### Copy with answer
Question + choices + learner answer + result.

### Copy with Civio explanation
Adds canonical explanation and source/rule.

### Copy full study context
Adds selected concept mastery, prior misses, learner note, and preferred tutor instruction.

### Copy source excerpt
For General Information or Notebook tasks, include the relevant verified source passage/citation when permitted.

## Preferred AI setting

Settings → AI Connections / External AI:

**Preferred assistant**
- ChatGPT
- Claude
- Gemini
- Grok
- Other

This setting should only alter convenience labels/actions. Clipboard Markdown remains provider-neutral.

## Sign in with ChatGPT relationship

This feature is **not** the same as Sign in with ChatGPT.

Current OpenAI behavior as of 5 Oct 2026:
- Sign in with ChatGPT can authenticate users on supported/partner apps.
- Eligible Plus/Pro users can allow participating apps to use ChatGPT plan usage for eligible AI requests.
- It does not expose the user's existing ChatGPT conversations or memory to Civio.
- Commercial website plan-usage access remains limited/partner-gated; open-source client usage has a documented path.

Therefore:

- **Copy for AI** should ship independently.
- **Ask Tutor via ChatGPT plan** can be added when Civio becomes eligible/configured.
- A future Civio ChatGPT plugin/app can provide deeper handoff and tool access, but the clipboard path must remain.

References:
- https://developers.openai.com/siwc
- https://developers.openai.com/siwc/quickstart
- https://developers.openai.com/siwc/website
- https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites
- https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk

## Future: Civio inside ChatGPT

A later Apps SDK / MCP surface could let a learner ask ChatGPT:

> Open my Civio mistakes from Clerical Ability.

or:

> Quiz me on the five concepts Civio says I am weak at.

Potential tools:
- get current question
- get canonical explanation
- get due reviews
- get concept mastery
- create a temporary practice set
- save a note
- mark a generated drill result

This should use scoped, explicit permissions. Do not expose the full question bank or answer key as a general-purpose tool.

## Acceptance criteria

- one click copies clean Markdown context
- payload works in ChatGPT, Claude, Gemini, and Grok
- answer key is omitted before Reveal
- strict Simulation hides/disables the action
- no personal data is copied by default
- copied source/rule is clearly separated from AI-generated discussion
- app still works if all AI services are unavailable
- external handoff never changes canonical Civio answers


---

## Critical implementation rule: never copy rendered page text

The button must **not** copy the DOM, selected page text, `innerText`, or accessibility/rendered labels from the exam screen.

Bad output looks like this:

```text
Multiple Choice
svgReport IssuesvgFlag for ReviewReveal
A run-on sentence is best corrected by:
A
Removing all verbs
svg
B
Using proper punctuation...
svgPrevious QuestionNext Question
```

That is UI noise, not study context.

### Build the export from structured question data

Generate the clipboard payload directly from the application's question object / attempt state:

- question type
- category / skill
- clean question stem
- clean option labels and option text
- learner's selected answer, when applicable
- correctness/result, only when allowed
- canonical explanation, only after Reveal/submission
- verified source/rule, when available
- optional learner note
- optional tutor instruction

Do not include:
- SVG labels
- icon alt text
- Report Issue
- Flag for Review
- Previous / Next buttons
- navigation
- timer
- progress widgets
- accessibility-only UI strings
- hidden DOM
- CSS-generated text
- provider/model UI

### Default clipboard format should be plain, human-readable text

Markdown is fine internally, but the copied result should look clean when pasted into any chat box.

Example:

```text
Philippine Civil Service Exam — Subprofessional
Category: Verbal Ability
Topic: Sentence Structure

Question:
A run-on sentence is best corrected by:

A. Removing all verbs
B. Using proper punctuation or conjunctions to separate independent clauses
C. Writing only fragments
D. Adding more unrelated clauses without punctuation

My answer: B
Result: Correct

Civio explanation:
A run-on sentence joins two or more independent clauses without proper punctuation or a coordinating/subordinating conjunction. Separate the clauses correctly or connect them with an appropriate conjunction.

Please explain the rule simply, tell me what to remember for the CSE, and give me one similar question.
```

Before Reveal/submission, omit the correct answer and explanation:

```text
Philippine Civil Service Exam — Subprofessional
Category: Verbal Ability
Topic: Sentence Structure

Question:
A run-on sentence is best corrected by:

A. Removing all verbs
B. Using proper punctuation or conjunctions to separate independent clauses
C. Writing only fragments
D. Adding more unrelated clauses without punctuation

My current answer: B

Do not reveal the correct answer yet. Give me one useful hint and help me reason it out.
```

### Product behavior

Default action: **Copy for AI**

Toast:

> Copied clean question context.

Optional secondary action, when a preferred assistant is configured:

> Discuss in ChatGPT

The copied payload remains provider-neutral and should paste cleanly into ChatGPT, Claude, Gemini, Grok, email, Notes, or any plain-text field.
