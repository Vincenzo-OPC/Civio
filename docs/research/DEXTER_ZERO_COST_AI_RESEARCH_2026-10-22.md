# Dexter zero-owner-cost AI research (22 October 2026)

**Status:** Research and recommendation only. Not implementation evidence, not activation authority. Author: Grok Bot (independent research). Reviewers: Astra (architecture), Codex (implementation in a separately started session). Binding constraint: [DEXTER_ZERO_COST_ACTIVATION_GATE_2026-10-22.md](../DEXTER_ZERO_COST_ACTIVATION_GATE_2026-10-22.md) — **₱0 owner-funded generative inference**. Tracking: [Issue #17](https://github.com/Vincenzo-OPC/Civio/issues/17).

All sources below were checked on **2026-10-22 (Asia/Manila)** unless noted. Provider terms change often; re-verify before any activation decision.

## 1. Current implementation status (verified against code on `main` @ 74809c2)

| Component | Code location | Status | Notes |
| --- | --- | --- | --- |
| `TutorProvider` contract (`explainAnswer`, `generateHint`, `classifyMistake`) | `app/Ai/Contracts/TutorProvider.php` | **Implemented (interface)** | Stateless, single-question. No session/memory, no learner context, no quota/availability method, no streaming. |
| `NullTutorProvider` | `app/Ai/Providers/NullTutorProvider.php`, bound in `AppServiceProvider` | **Implemented, but unused** | Returns stored explanation, one generic hint, correct/incorrect/skipped. `rg` finds no caller outside the service provider binding: the contract is plumbing, not a feature. |
| `RevealTutor` (deterministic Reveal) | `app/Services/Exam/Reveal/RevealTutor.php` + 10 solvers | **Implemented** | Rectangle perimeter, terminal-digit and alphabetical filing, Fibonacci/number sequences, mixture, grammar rule, order of operations, checked quantity/pattern solvers. Publishes a pattern explanation only when the recomputed value matches the key; returns concept, steps, shortcut, common mistakes, visual, same-skill follow-up. Tests: `tests/Unit/Exam/RevealTutorTest.php`, `tests/Feature/User/RevealTutorTest.php`. |
| FSRS scheduler | `app/Services/Exam/FsrsScheduler.php`, `FsrsRatingPolicy.php`, `ReviewScheduleApplier.php`, models `ReviewCard`, `ReviewEvent`, `ReviewItem`, `ReviewHelp` | **Implemented online, not production-verified** | Runs `ts-fsrs@5.4.2` server-side via Node with a 5 s timeout; server-graded ratings only. Offline reconciliation **planned**. |
| Review Mistakes, fresh same-skill practice, Today's Focus, weak-skill drill, independent vs assisted accuracy, retention, streak, per-subject pace | Exam services/controllers (recent commits bb25ff8, b0f0903, 1a55813) | **Implemented** | Deterministic. Do not rebuild. |
| Copy for AI (external handoff) | `resources/js/lib/ai-handoff.ts`, `copy-for-ai-button.tsx`, test `tests/Js/ai-handoff.test.ts` | **Implemented** | Built from structured data, not DOM. Key/result/explanation only included when attempt state says revealed/review. This is already a genuine ₱0, user-funded AI path. |
| Distractor/error codes, misconception taxonomy, prerequisite graph, BKT/Elo mastery | — | **Planned (absent)** | No migration or model contains distractor codes, misconception ids, prerequisite edges or mastery probabilities. This is the main blocker to real personalization. |
| `AiGatewayService` (Workers AI, Gemini, Groq URLs) + `GenerateUserAnalysisJob` / `AiAnalysisOrchestrator` | `app/Services/Ai/AiGatewayService.php`, `app/Jobs/GenerateUserAnalysisJob.php` | **Implemented, dormant (credential-gated)** | ⚠️ **Owner-key path.** Uses server-level `CLOUDFLARE_API_TOKEN` / `GEMINI_API_KEY`. If those env vars are ever set in production, analytics automatically dispatches AI analysis jobs on the owner's account (default user mode is `'ai'`). Falls back to deterministic analysis only when unset. This conflicts with the zero-cost gate's "no shared owner key" rule and should be gated by an explicit kill switch. |
| `GenerateQuestionsJob` (Gemini) | `app/Jobs/GenerateQuestionsJob.php` | **Implemented, dormant** | Admin bank-generation path using the owner Gemini key. Not learner-facing, but still owner-funded if enabled. Generated drafts must never bypass the signed bank approval gate. |
| In-app conversational Dexter | — | **Disabled / not built** | No route, controller, or UI calls a live tutor. |

**What Dexter does today without AI:** checked Reveal explanations with recomputed answers for ~10 pattern families; stored explanations split into concept/steps; same-skill follow-up; Review Mistakes; FSRS due queue; fresh unseen same-skill practice; Today's Focus; weak-skill progression with independent-only evidence; Copy for AI to the learner's own chatbot.

**What blocks genuine personalization:** (1) no item-level distractor → misconception mapping, so a wrong choice cannot be diagnosed beyond "incorrect"; (2) no skill/prerequisite graph, so Dexter cannot step back to a prerequisite (e.g. percent → fraction ↔ decimal); (3) no per-skill mastery estimate with uncertainty; (4) the provider contract has no learner context, session, or availability/quota concept.

## 2. Provider comparison and who actually pays

| Option | Category | Who pays | Verified limits / terms | Fit for Civio | Source |
| --- | --- | --- | --- | --- | --- |
| **Sign in with ChatGPT – plan usage** | User's consumer subscription | **Learner** (Go/Plus/Pro plan usage, optionally their credits) | Identity sign-in is separate from plan-usage permission. Plan usage "available to all open-source partners and selected private clients"; commercial = "limited trial"; paid or remotely hosted apps must use the interest form. User sets weekly per-app limit. Free ChatGPT users cannot share plan usage. | **Best long-term match**, but **not available to hosted Civio today** without OpenAI partner acceptance. | https://developers.openai.com/siwc/quickstart ; https://developers.openai.com/siwc/token-sharing-open-source ; https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites ; https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt |
| **OpenRouter OAuth PKCE** | Genuinely user-funded | **Learner** (their OpenRouter credits) | OAuth PKCE mints a key on the user's account; "requests are billed to their own OpenRouter credits, so you don't pay for their inference". Free `:free` models: 20 RPM, **50 requests/day per account** (<10 credits purchased) or 1,000/day after buying 10 credits; negative balance → 402 even on free models. | **Available now, self-serve.** Realistic BYOK path. Free tier per learner (50/day) is enough for hints, not long chats. | https://openrouter.ai/docs/use-cases/oauth-pkce ; https://openrouter.ai/docs/api_reference/limits |
| **Gemini API free tier** | Limited free tier (developer) | Google, under the **key owner's** project | Free tier exists for several Flash/Flash-Lite models (not Pro/flagship). Limits are **per project**, shown only in AI Studio; "not guaranteed". **Free-tier content is used to improve Google products and may be read by human reviewers.** Terms: users must be **18+**, and the API may not be used in apps "directed towards or likely to be accessed by" under-18s; "for developers … not for consumer use"; available regions only; EEA/CH/UK require paid. Adding billing auto-promotes to Tier 1 with up to $250 cap. | **Owner key: reject** (shared quota, privacy, auto-billing risk). **User-own key:** technically possible but the "not for consumer use" clause makes asking ordinary learners to create developer keys a terms risk; Astra must decide. Philippines regional availability **not re-verified** this session. | https://ai.google.dev/gemini-api/docs/pricing (updated 2026-10-19) ; https://ai.google.dev/gemini-api/docs/rate-limits ; https://ai.google.dev/gemini-api/terms |
| **Cloudflare Workers AI** | Limited free allocation (owner account) | Cloudflare up to **10,000 Neurons/day**, then owner must be on Workers Paid ($0.011/1k Neurons) | On Workers Free, exceeding the limit makes "further operations fail with an error" (fails closed). Example: llama-3.1-8b-fp8-fast ≈ 34,868 Neurons per M output tokens → ~285k output tokens/day for the **whole app**, i.e. a few hundred short hints/day, shared by all users. Several frontier models require paid billing. | **Reject for public tutoring.** Usable only for an owner-only offline eval, never as the learner service. | https://developers.cloudflare.com/workers-ai/platform/pricing/ (updated 2026-10-20) |
| **Groq free tier** | Limited free tier (developer) | Groq, under the key owner's org | Org-level limits, e.g. gpt-oss-120b 30 RPM / 1K RPD / 8K TPM / 200K TPD. | Owner key: reject (shared, tiny). BYOK same terms questions as Gemini. | https://console.groq.com/docs/rate-limits |
| **GitHub Models** | — | — | **Retired 30 July 2026**, including inference API and BYOK. | **Not an option.** Remove from any plan. | https://github.blog/changelog/2026-07-30-github-models-is-now-retired/ |
| **Chrome built-in AI (Prompt API, Gemini Nano)** | On-device, free | **Learner's device** | Stable in Chrome 148+ on Windows/macOS/Linux/Chromebook Plus only; **not Android/iOS**; needs 22 GB free disk, >4 GB VRAM or 16 GB RAM + 4 cores; unmetered network for download. "No data is sent to Google." Languages (Chrome 149): EN/ES/JA/DE/FR — **no Filipino**. | Genuinely ₱0 and private, but excludes most Filipino phone-first learners. Optional desktop enhancement only. | https://developer.chrome.com/docs/ai/prompt-api ; https://developer.chrome.com/docs/ai/get-started |
| **WebLLM / WebGPU, Ollama (local)** | User-operated | Learner's hardware | Not re-verified this session. Known constraints: large model downloads, WebGPU support, power users only. | Optional, power users. Low priority. | (not verified this session) |
| **Copy for AI (existing)** | User's own chatbot | **Learner** (any free or paid chatbot) | Already built; no key handling, no Civio inference. | **Keep as the default AI path.** | in repo |
| Sponsored / education grants | Third-party credits | Sponsor | No specific programme verified this session. Credits are finite and usually tied to the owner's billing account. | Treat as developer credits for offline evals only; never as a public service. | (not verified) |

**Categories, separated:** free trials / developer credits (finite, owner account, can auto-bill) ≠ limited free tiers (shared per project, privacy-reducing) ≠ consumer subscriptions (user pays, but only SIWC turns that into API usage, and only for approved apps) ≠ genuinely user-funded inference (OpenRouter OAuth today; SIWC once approved). **Logging in with Google gives no Gemini API access; logging in with ChatGPT gives identity only unless the separate plan-usage scope is granted to an approved app.**

## 3. Sign in with ChatGPT feasibility

- **What it is:** OIDC + PKCE sign-in, plus an optional, separately consented scope letting eligible Go/Plus/Pro users route eligible Responses API requests through their plan usage; users set weekly per-app limits in ChatGPT settings.
- **Eligibility today:** open-source and locally hosted apps can use plan usage via dynamic client registration (no client secret), with a persisted opaque `ext_agent_host_id` per host. **Hosted/commercial apps need OpenAI's interest form and acceptance** into a limited trial. Civio is a hosted web app → **not eligible without approval**. The open-source path is designed for tools users run themselves (laptop/self-hosted VM), not a central Laravel server holding everyone's tokens.
- **Free learners:** ChatGPT Free users cannot use plan sharing in commercial apps. Many Civio learners will have no paid plan → they still need the deterministic tutor.
- **Implementation steps (only after GT approval and OpenAI acceptance):** (1) GT submits the interest form describing Civio honestly (free CSE reviewer, MCQ, no resale of plan usage); (2) on acceptance, implement sign-in as an *additional* linked identity, not a replacement login; (3) request plan-usage scope only when the learner opts into AI tutoring; (4) store tokens encrypted per user (or client-side if required by OpenAI terms), never pooled; (5) `store:false`, streamed Responses calls through a `SiwcTutorProvider`; (6) handle declined consent, revoked sessions and limit exhaustion by falling back to `NullTutorProvider`; (7) never charge an access toll for plan usage.
- **Verdict:** preferred *future* route; **blocked on OpenAI partner approval**. Nothing Codex builds now should assume it.

## 4. Recommended zero-owner-cost architecture

GT's direction is right, with three challenges:

1. **Deterministic Dexter is the product, not the fallback.** Most learners will never connect AI. Investment should go into item metadata (distractor → misconception codes), a skill/prerequisite graph and a mastery model — this is what makes Dexter "intelligent" and it costs ₱0 per request.
2. **The LLM must never be the grader or the answer source.** Civio sends the LLM only the stem, options, the learner's choice and Civio's *checked* explanation, **after** reveal. In Strict Mock or before reveal, the provider receives no key and may only give a Socratic hint; the server rejects any provider call for an unsubmitted mock item.
3. **Remove the owner-key path before adding user-key paths.** The dormant `AiGatewayService` analytics/generation jobs are the only way Civio can currently bill GT; put them behind an explicit `DEXTER_OWNER_FUNDED_AI=false` hard kill switch (default false, ignored in production) before any BYOK work.

**Layers:**
- **L0 Civio core (₱0):** bank, server grading, Reveal solvers, explanations, FSRS, Review Mistakes, fresh practice, analytics.
- **L1 Deterministic tutor brain (₱0):** misconception diagnosis from distractor codes; prerequisite graph; per-skill mastery (Elo-style item/learner rating or BKT with conservative priors, independent answers only); a transparent next-question selector (weakest prerequisite with evidence → due FSRS → fresh transfer item → blueprint balance) that explains "why this question".
- **L2 Optional generative module:** `TutorProvider` v2 with `isAvailable(user)`, `quotaState`, and `null | openrouter-oauth | siwc (future) | chrome-local (client)` implementations. Per-user credentials only. Any 401/402/429/timeout → `NullTutorProvider` with honest "AI unavailable, here's Civio's explanation" copy. No retry onto a different paid model.
- **L3 External handoff (₱0, exists):** Copy for AI stays available to everyone.

**Security:** BYOK/OAuth keys encrypted at rest with Laravel encryption, scoped per user, never sent to the browser after storage (or kept browser-only if Astra prefers client-side calls; then the answer key must not be shipped to the client before reveal). Treat model output as untrusted: render as text, no HTML; strip any claim of a different correct answer by checking against the server key; ignore instructions embedded in question text or learner messages; rate-limit per user to avoid draining the learner's own credits; let users revoke and delete keys; log no prompts with personal data. Minors: Gemini terms bar under-18-likely apps; Civio should state an 18+ requirement for any connected AI and keep it off by default.

**Cost and scale:** L0–L1 and L3 scale with ordinary hosting only. L2 costs GT ₱0 because every request is authorized by and billed to the learner's own account; the server makes no provider call without a per-user credential. Hosting/bandwidth costs remain separate and are not covered by this research.

## 5. StudyStash-inspired MCQ improvements (MCQ only)

Sources: https://studystash.com/en-us ; https://studystash.com/en-gb/about/news/studystash-joins-kortext (via existing brief; not re-fetched). Marketing pilot numbers are self-reported, not evidence.

Adopt the principles, not the formats:
1. **Diagnostic distractors:** every wrong option in Subprofessional math, spelling and clerical gets a misconception code (e.g. `pct_of_wrong_base`, `fraction_add_denominators`, `filing_ignores_particle`). Reveal names the likely misconception from the chosen option.
2. **Prerequisite step-back:** two independent misses on a skill trigger one easier prerequisite MCQ, then return to the original skill with a fresh item.
3. **Independent transfer check:** after a reveal, the next same-skill item must be unseen and answered without help before it counts (already partly built in fresh practice — extend with misconception targeting, don't rebuild).
4. **Spaced review:** keep FSRS for retention; assisted answers never rate "Good/Easy".
5. **Measurable learning:** report per-skill independent accuracy on unseen items with sample size and delayed retention; no mastery percentages without evidence.

No flashcards, matching, podcasts or new item types.

## 6. Ranked development priorities (all ₱0, no activation)

1. **Kill switch for owner-funded AI** (`AiGatewayService` analytics and generation jobs) + test that no provider HTTP call occurs when the switch is off, even with keys present.
2. **Distractor/misconception schema** (nullable per-option code + taxonomy file) and tagging tooling for Subprofessional Numerical, spelling and Clerical drafts, reviewed through the existing bank review packets (no approval changes by agents).
3. **Skill/prerequisite graph** as a versioned data file with tests (e.g. fractions → decimals → percent → percent change → discount).
4. **Mastery estimate** (Elo or BKT, independent answers only, min-sample gating) feeding the existing Today's Focus/weak-skill selector; expose "why this question".
5. **Reveal misconception feedback** using the chosen option's code; expand solvers for percent, ratio, work-rate, age and distance problems.
6. **`TutorProvider` v2 contract** (availability, quota, learner-context DTO with no key pre-reveal) with `NullTutorProvider` and a fixture-backed fake provider for tests; UI states for "AI off / not connected / quota exhausted". No real provider wired.
7. **Offline golden evaluation suite** for hints/explanations using fixtures; CI makes no network calls.
8. **Only after GT approval:** OpenRouter OAuth PKCE provider behind a feature flag; SIWC after OpenAI acceptance.

## 7. Risks, blockers and open questions

- **Blocker:** SIWC plan usage requires OpenAI approval for hosted apps; status unknown until GT applies.
- **Risk:** dormant owner-key jobs become live the moment a key is placed in env (see §1).
- **Risk:** Gemini/Groq free tiers are per project and train on free-tier data (Gemini); unsuitable for a public service on an owner key.
- **Open:** may ordinary learners lawfully use their own Gemini developer keys given the "not for consumer use" and 18+ clauses? Needs Astra/legal read.
- **Open:** is Gemini API currently available in the Philippines? Not re-verified this session.
- **Open:** server-side vs browser-only storage of OpenRouter keys (XSS exposure vs server breach exposure).
- **Open:** minimum learner age policy for Civio overall.
- **Risk:** LLM hints that contradict the checked key; mitigated by server key check and never using LLM output as grade.
- **Not verified:** WebLLM/Ollama current requirements, education/sponsor grant programmes.

## 8. Handoff

**Astra (architecture review):** decide (a) L0–L3 layering above; (b) client- vs server-side BYOK storage; (c) whether user-owned Gemini/Groq keys are acceptable under their terms; (d) mastery model choice (Elo vs BKT) and minimum-sample rules; (e) whether GT should file the SIWC interest form. Write an ADR; approve, revise or reject.

**Codex (separate session, ₱0, no deploy):** implement priorities 1–7 in order, in small tested commits with `[skip netlify]`. Do not wire any real provider, set any env key, change bank approval status, or touch MSI/Hermes. Do not rebuild Today's Focus, fresh practice, independent accuracy, FSRS or Review Mistakes. Every provider-related test must assert zero outbound HTTP.

**Still disabled pending GT approval:** any live generative provider (owner or user-funded), OpenRouter OAuth, SIWC, the owner-key analytics/generation jobs, any paid plan or billing account.
