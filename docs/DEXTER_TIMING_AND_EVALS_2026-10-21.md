# Dexter pacing, learning telemetry and AI evaluations

**21 October 2026 | Research and Astra decision brief | Not implemented**

Read with [the master plan](DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md), [tutor policy](DEXTER_TUTOR_POLICY_2026-10-21.md), and [current execution priorities](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md). This brief records GT's latest ideas and gives **Astra final technical judgment** about which features to keep, change, defer or reject. Codex should critically research and evaluate before implementing. An agent only acts when a user launches it.

## User experience proposal

Consider an optional **question pacing bar**. For example, a learner may answer an item in 10 seconds against an illustrative 60-second target; Civio would show elapsed time, improvement against prior comparable independent attempts, and what to practice next. The values 10 and 60 are EXAMPLES, never universal exam norms. The visual should be lightweight, optional, calm, accessible, reduced-motion friendly and render clearly on cheap Android phones/Lite Mode. Never create extra React rerenders of the main question each second.

**Priority rule: independent accuracy -> new-item transfer -> delayed retention -> calibrated speed.** Fast correct may indicate fluency OR a guess OR memorized exact item. Slow correct on an unfamiliar difficult task can show strong reasoning. A guessed fast wrong, or an assisted correct answer, is not mastery. Do not train people to click quickly at the expense of understanding or fair access.

Provide a text alternative and optional post-answer feedback:
- Slow + repeated wrong: teach missing prerequisite or problem setup.
- Fast + repeated wrong: check rushing, guessing and misunderstood wording.
- Correct on fresh items but consistently slow relative to comparable items: teach efficient method, then test speed on new matched items without sacrificing accuracy.
- Fast on repeats, slow or wrong on fresh variants: schedule transfer items instead of counting repeated memorized answers.
- Fast, independently correct on multiple fresh difficult items and delayed retest: advance difficulty / interleave another subject, conditional on coverage.
- No history or insufficient comparable items: show elapsed only and explain insufficient evidence.

Compare durations only within similar concept, item difficulty, reading burden, language, novelty, assist state and device/accessibility conditions; use robust medians, sample counts and uncertainty. Explore calibrated targets from sufficiently clean learner/reference data. Do not present a universal per-item CSC time allocation as official. During Strict Mock, preserve ordinary overall timed simulation without distractive tutoring; analyze individual pace AFTER submission.

## Existing code and engineering investigation

As inspected 21 Oct 2026:
- `resources/js/pages/user/exams/hooks/use-exam-timer.ts` already tracks `questionTimes` and `itemElapsed` with clock snapshots and optimized, infrequent state flushing.
- `resources/js/pages/user/exams/hooks/use-exam-state.ts` passes `questionTimes` into exam submission.
- `app/DTOs/Exam/SubmitExamAttemptData.php` accepts `question_times` as **non-authoritative client metadata**.
- `app/Actions/Exam/SubmitExamAttemptAction.php` derives a mock's session duration from server timestamps.
- There is no verified trustworthy per-concept pacing or speed-based learner model. Inspect latest HEAD; do not claim it exists.

Astra should audit time-to-first-selection, active time, total revisits and end-to-end session time. Handle pause/resume, hidden tab, inactivity, multiple tabs, clock changes, device sleep, offline sync, reloaded answers and answer changes. Browser timing is useful **advisory learning telemetry**, not secure evidence for high-stakes proctored grading. Correctness and help/reveal state remain server validated. Avoid needless personal telemetry or background tracking. Explicit consent, retention/export/delete and no sharing detailed student history with external providers by default.

## AI-native educational design

Civio should combine deterministic mathematics/answer checking, approved primary sources, retrieval practice, knowledge tracing, FSRS spaced scheduling, Socratic tutoring and optional appropriately authorized AI. Dexter should use evidence of misconceptions, independent answers, novel transfer, forgetting and timing to select a teaching intervention; not imply it reads minds or has access to missing history.

The real moat is **measurable independent improvement on unfamiliar tasks**, not a flashy "AI" badge or a giant unverified question bank. For GT, begin with Subprofessional mathematics (fractions, decimals, percentages, word problems, ratios, sequences) and spelling/filing, but continue sampling other subjects to detect false confidence. Research actual exam scope through official CSC announcements and public/consented examinee experiences. Never describe an unofficial invented question as an actual exam question.

## Evaluations before and during implementation

Create a **versioned, provider-neutral, cost-controlled evaluation harness**. Astra first compares alternatives, documents an ADR and chooses appropriate gates.

1. Deterministic tests: correct solutions, no answer-key leaks, lock and authorization checks, server grading, study/strict separation, time/pause events, idempotency, ownership, reliability, offline/Lite functionality.
2. Expert-reviewed golden examples: approved problems, plausible student misconceptions, worked solutions, spelling distractors, ambiguous items, official legal references where applicable. Independent test families must not overlap with training/practice.
3. Multi-turn simulated learners: unsure novice, confidently wrong student, slow accurate student, fast guesser, hint dependency, Taglish requests, question with a wrong stored key, missing progress history, exhausted free AI quota.
4. Hybrid evaluation: exact and programmatic graders for hard safety and math; reference/source checking for GI; separately calibrated LLM judge for tutoring behavior; sampled human ratings especially on subtle misconception diagnosis. Keep inter-rater disagreement visible. An AI judge must NEVER override deterministic safety failures or certify actual learning alone.
5. Rubric: factual accuracy, no unrevealed answer, source correctness, one question at a time, helpful scaffolding, correct diagnosis with uncertainty, independent transfer and delayed follow-up, learner autonomy, latency and cost, device compatibility.
6. Outcome validation: new unseen question accuracy, independence, 1/7/28-day delayed recall, response time conditional on correctness and difficulty, confidence calibration, longitudinal error changes and held-out timed mock performance. Study time and no-AI comparison controls matter.
7. Gate prompt/model changes with reusable fixtures, human review and explicit pass/fail counts. AI calls in routine CI default to OFF; separate opt-in paid grading only after GT approves budget. Never put API keys in the browser bundle or store unnecessary learner chat content.

**October 2026 tooling note:** OpenAI says its legacy Evals platform becomes read-only 31 Oct 2026 and shuts down 30 Nov 2026. Prefer in-repo provider-neutral datasets and current Datasets/Graders patterns over retiring endpoints.

## Research citations
- Adaptive assessment length vs accuracy (2024): https://onlinelibrary.wiley.com/doi/full/10.1111/jcal.13074
- Early response-time-aware item response modeling (2025, limited math sample): https://www.mdpi.com/2076-3417/15/13/6999
- FSRS memory model: https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm
- Anthropic evaluation methodology: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- OpenAI Datasets and graders: https://developers.openai.com/api/docs/guides/evaluation-getting-started
- OpenAI platform transition: https://developers.openai.com/api/docs/guides/evals
- Automated pedagogy grader limits, AIED 2025: https://discovery.ucl.ac.uk/id/eprint/10212920/

## Mandatory Astra decision record before feature build

Write an ADR covering alternatives (elapsed-only vs estimated pace vs adaptive benchmark), source of trusted evidence, novelty/difficulty normalization, accuracy-speed guardrails, accessibility, expected cost, unknowns, measurement plan, red-team evals and what to defer. Do not blindly implement all proposed UI. Preserve existing security-first roadmap, bank approval, 360px/Lite performance, no unauthorized deploy and no spending. Then implement **one approved bounded slice**, with tests and benchmark, and update Issue #17 and the project execution notes.

Candidate order **after existing security/Review Mistakes gates**: time telemetry audit + tests; optional calm elapsed-only bar; robust owner-scoped response-event persistence; descriptive matched timing analytics; calibrated tutoring selector + transfer tests; optional AI grader and in-app Dexter after golden/human rubric validation.
