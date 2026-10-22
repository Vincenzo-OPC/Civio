# Dexter generative AI: ZERO OWNER-COST activation gate (GT directive, 22 Oct 2026)

**Status:** Binding product and engineering constraint, not evidence that in-app generative AI is built, active, free at scale, or approved for any provider. This decision supersedes speculative provider activation language elsewhere. It does not stop ongoing bank QA, deterministic teaching, external Ask/Copy, Review Mistakes, FSRS, learner-model research or testable disabled-by-default code. User explicitly says **if Civio must pay for inference, the answer is NO for now**.

## Product decision

- **Owner-funded generative inference budget: ₱0.** Do not sign up for billed developer APIs, add automatic billing, configure pay-as-you-go/overages, buy credits, activate a billable provider, accept a trial that can auto-upgrade to paid, or incur hosting/inference fees on GT's behalf. If uncertain whether a request would cost GT money: **do not make the request**.
- **Keep in-app generative Dexter OFF and inaccessible to ordinary users**, including unrevealed/paid backdoor endpoints, until GT explicitly approves a lawful provider architecture, security checks, zero-owner-cost proof and activation. Do not mistake a provider stub or research roadmap for a running conversation service.
- **Keep building behind the switch:** provider interfaces/NullTutorProvider, safe independent pedagogical logic, checked MCQ explanations/hints, consented-data model, cost-aware simulations using fixtures, versioned offline golden evaluations and provider-agnostic UX can be improved without new recurring costs. Mock and exam keys remain server-locked.
- **Default experience still works without AI:** approved multiple-choice practice, existing rule-based Reveal, authoritative scores, no-key-leak external Ask/Copy handoff, mistake review and due scheduling when verified, Lite/offline study. When AI is unavailable, do not punish the learner, block practice, or display a misleading 'Dexter online' badge.
- **No automatic paid fallback.** Any free trial, capped free-tier account, user-owned provider credits, usage-sharing plan or local model that exhausts capacity MUST stop AI requests cleanly and fall back to normal Civio MCQs. No GT-funded overage, no silent switch to more expensive models.
- **No silent activation by Grok Bot/Codex/Astra.** Research, plans, draft code and GitHub instructions are not authority to deploy/enable a provider; GT makes the final explicit activation decision.

## Source-verified funding candidates (22 October 2026)

| Candidate | Owner funding | Product eligibility / constraint | Decision |
| --- | --- | --- | --- |
| **OpenAI Sign in with ChatGPT / plan usage** | Eligible consenting user uses included ChatGPT usage and optionally their expressly authorized credits; not a Civio-paid API bill | Real feature, but identity sign-in is NOT inference authorization. Hosted commercial Civio needs approved-partner/onboarding path; open-source/local flow is distinct. SIWC terms require requests from user-controlled runtime, local user-controlled persistent tokens, no pooled accounts, no access toll on plan use; eligible commercial plan usage may vary by app/plan. Civio has NO verified approval. | **Preferred path to investigate, OFF until partner acceptance and technical proof** |
| **Google Gemini Developer API free tier** | Google provides certain eligible free tokens, subject to model/project/rate limits, availability and data-use terms | NOT unlimited, not a consumer Gemini subscription share. Owner-operated free key/quota is not viable as an uncapped public service; if eventual testing is approved, require a no-billing-path configuration and fail closed at quota. Free-tier input may be used for Google's product improvement; avoid transferring identifiable student content until privacy review. | **Research / optionally local non-billed proof of concept only by explicit GT permission; public service OFF** |
| **Cloudflare Workers AI free allocation** | 10,000 free Neurons/day at time of check; supported models only | Free plan has finite allowance, some frontier models require paid billing; do not upgrade to Workers Paid, add a card or commit owner funding. Capacity insufficiently demonstrated for multi-user Socratic tutoring. | **Research only, public service OFF** |
| **OpenRouter OAuth user-funded credits / BYO key** | Each user pays their own provider directly | OAuth delegated keys and budget caps are plausible, but hosted-app secret handling, terms and privacy must be reviewed. Never upload unrestricted keys into public browser source or expose another user's credentials. No fallback to owner-funded key. | **Potential opt-in alternative; OFF pending security and GT approval** |
| **User-operated local model** | User's own hardware/compute | True user-operated runtime, low-end Android constraints, model quality and engineering overhead unknown; do not make it a requirement. | **Optional research only** |
| **External Ask ChatGPT/Gemini etc.** | Learner's own external app/site plan; no Civio API request | Existing external handoff is not embedded Dexter, and Civio cannot see the conversation or promise that the assistant has persistent Civio history. Follow strict-mode and privacy rules. | **Continue zero-owner-inference-cost option; review functionality normally** |

Primary sources:
- https://developers.openai.com/siwc/quickstart
- https://developers.openai.com/siwc/token-sharing-open-source
- https://openai.com/policies/sign-in-with-chatgpt-terms/ (29 Sept 2026)
- https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites
- https://openai.com/form/sign-in-with-chatgpt-interest/
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://openrouter.ai/docs/api/api-reference/o-auth/create-auth-keys-code

### Clarify 'sign in' and 'user uses own tokens'

A user authenticating with Google/ChatGPT does not by itself supply API tokens, credit, or authorization for Civio inference. OpenAI offers optional permission for supported apps to use eligible ChatGPT plan allowances, but **Civio is not currently a verified participating approved commercial partner**. The open-source flow cannot simply be repurposed as a centralized SaaS proxy using ChatGPT browser cookies/CLI keys. Persistent OpenAI SIWC authentication tokens must be kept local under that user's control. Treat any proposed shared host/backend integration as blocked until its architecture satisfies the actual approved commercial terms.

### Avoid the 'free API' trap

Gemini/Cloudflare free tier is **developer/project quota**, not automatically per-Civio-learner unlimited entitlement. A public site with a single free project can exhaust its quota, hit request limits, change terms, or expose provider-specific data-use conditions. Never promise 'free Dexter for everyone' based only on a quota table. A safe experiment explicitly fails with 'AI currently unavailable' and no financial exposure. Nothing should route personal learning records externally without consent.

## Current repository reality (checked Oct 22)

- `app/Ai/Contracts/TutorProvider.php` specifies a provider contract; `app/Ai/Providers/NullTutorProvider.php` is a **non-generative stub** that returns stored explanations and static hints. It does not represent a configured live LLM.
- `app/Services/Exam/Reveal/RevealTutor.php` implements deterministic checked-solvers and question follow-ups.
- `docs/FEATURE_CATALOG.md` describes Dexter as a partial key check, not an in-app conversation tutor, and in-app generative tutor as planned.
- Operational details, provider secrets, paid execution or deployment were **not verified in a running host**. Inspect the latest code and tests before implementation; code/docs are not proof that a production feature is off.

## Nonnegotiable activation checklist (all required, GT explicitly approves last)

1. Identify a concrete provider model and **who actually pays** for each request; confirm zero GT funding on both ordinary and worst-case/max-usage paths, including retries, rate-limit and exhaustion.
2. Verify provider terms, eligibility/approval (especially hosted SIWC), credential storage, user-owned funding, consent and revocation. No cross-user usage.
3. Prove on sandbox/free-fixture tests: backend refuses all owner-funded inference when flag off; strict mock lock; no answer-key leakage; per-user isolation; opt-in data sharing; usage caps; explicit user-controlled provider disconnection; predictable 429/quota fallback and zero paid rollover.
4. Confirm no automatic upgrade, new billing relationship, owner-supplied global production key, background AI polling, or paid evaluation calls. Read privacy/data-retention rules, verify supported countries/plans and usage limits.
5. Prove each tutoring response grounds in stored-key safe method, new approved MCQ, and that generated uncertainty is surfaced; remain functional without any generative provider.
6. Confirm costs and resource use from trustworthy account-side dashboards and logs; run an approved limited test before broad rollout, still with no owner expenses.
7. **Ask GT explicitly** before enabling ANY first-party generative inference even if free or user-funded. Current decision is **NO activation**.

## For Astra, Codex and Grok Bot

**Astra:** evaluate a user-funded/zero-owner-cost architecture and reject unsupported integration claims. Do not use OpenAI consumer accounts through proxy hacks. Propose a kill-switch and hard zero-spend tests, but do not implement billable behavior. **Codex:** safely improve modular provider interfaces, deterministic Dexter and offline/unit-tested architecture while AI remains completely disabled for users. Respect existing security/bank gates, keep all changes independently verified and never deploy. **Grok Bot:** periodically verify official SIWC commercial access, Gemini/Cloudflare free limits/terms and BYOK feasibility; update source-based evidence, not marketing guesses. None of these are standing autonomous execution instructions.
