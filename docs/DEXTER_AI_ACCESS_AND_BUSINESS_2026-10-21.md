# Dexter AI access, user-funded inference and Civio revenue

> **Binding GT decision, 22 Oct 2026:** Owner-funded AI budget is exactly **₱0**, including tiny charges that become meaningful when multiplied by thousands of simultaneous free users. Development of disabled-by-default Dexter is allowed; activating any owner-funded model is not. A user must fund eligible inference with their own allowed account/plan/credits, or an actually zero-owner-exposure path must be proved and accepted by GT. Do not assume free tiers can operate uncapped for an unlimited public user base. See [zero-cost activation gate](DEXTER_ZERO_COST_ACTIVATION_GATE_2026-10-22.md). This supersedes any suggestion below of even a 'low-cost' platform-funded fallback; that option is now **rejected** pending an explicit new funding decision.
Research snapshot: 21 October 2026 (Asia/Manila). STATUS: policy and feasibility study; NO provider, payment, billing, keys, partnership or deployment authorized.
Parent: [Dexter implementation master plan](DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md).

## Business goal
GT's idea: Civio operates the valuable tutor, approved content, learning records, adaptive review and analytics; the student optionally funds generative inference using a plan or account they control. Civio earns only from its independently delivered learning services, optional membership, institutional licensing, or from documented/approved commercial terms. **No automatic commission or markup arises merely from sending users to Google, OpenAI, Anthropic, OpenRouter or OpenCode.** Never pool consumer accounts or provide a general-purpose model-resale proxy.

Offer zero-inference-cost mode (deterministic explanations, checked solvers, approved review items, analytics, FSRS locally/server-side, downloadable offline drills). AI is an optional convenience, never necessary to finish core learning.

## Provider matrix, verified against official docs on 21 Oct 2026
### External assistant handoff, first
ChatGPT / Gemini / Copilot / Grok external chats: currently the most practical zero-API-bill option for Civio. Student uses their own product/account, interaction stays in their external conversation. Civio cannot read the conversation, reliably grade a generated follow-up, write learner memory or charge that provider for usage; the tutor policy and optional summary are copied. Current resources/js/lib/ai-handoff.ts uses provider-dependent prefill, and the fallback clipboard path should be upgraded.
Source: [existing Civio external AI handoff](EXTERNAL_AI_HANDOFF.md).

### Sign in with ChatGPT, conditional, not a commercial toll booth
OpenAI's Sept 29, 2026 terms and October help docs describe eligible Go/Plus/Pro plan usage in **approved participating commercial apps**, separately from sign-in-only. Civio is NOT yet an approved partner and must not claim entitlement.
Mandatory restrictions: requests originate from user's local runtime or remote environment **controlled by that user**; tokens must persist locally under that user's control, not on a Civio-managed backend; use solely for that user and connected app; **must let the user use their ChatGPT plan without paying Civio or upgrading in Civio**; absolutely no pooled subscriptions, usage resale, account rotation or credentials/cookies collection. Other independently delivered premium Civio features may be sold under provider terms, but cannot gate or markup the SIWC plan path. Verify license, onboarding requirements, and any commercial-partner approval with OpenAI before implementation. Do not use a server-side SaaS proxy to store SIWC plan tokens.
Sources:
- https://openai.com/policies/sign-in-with-chatgpt-terms/
- https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites
- https://developers.openai.com/siwc/website
- https://developers.openai.com/siwc/quickstart
- https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform

### Google/Gemini
Sign in with Google is IDENTITY only. It does not transfer Gemini consumer subscription benefits into Civio and does not automatically settle Gemini API costs. Gemini API belongs to a Cloud project with separate quotas/billing, possibly a limited free tier; Google AI Pro/other consumer membership is not a generic commercial API allowance. Google documents OAuth for API credentials, but obtaining an identity token alone is not sufficient to use a customer's paid subscription. A true user-funded route would require customer-controlled Cloud project credentials/quota, explicit consent, current provider rules, careful key scoping and billing transparency; investigate before offering. Paid Gemini API credits in the developer project are Civio expenses and must be opt-in, capped and explicitly authorized.
Sources:
- https://ai.google.dev/gemini-api/docs/billing/
- https://ai.google.dev/gemini-api/docs/oauth
- https://ai.google.dev/gemini-api/docs/api-key

### OpenRouter user-owned account
OpenRouter documents OAuth authorization-code/PKCE exchange producing a user-controlled API key with optional limit, plus user-funded credits. This is a plausible BYO-CREDIT integration for a commercial web app, subject to security review and current agreements; OpenRouter does not magically pay Civio a revenue share. For a hosted Civio service, never expose durable provider keys in JS bundles or logs; if server-side use is chosen, encrypt user-delegated secrets at rest, scope/rotate/revoke keys, bind to owner, and gate requests with per-user budgets and explicit user consent. Prefer OAuth limited delegated keys over requiring a raw unrestricted key. Test credit exhaustion safely, without falling back to platform-paid usage.
Sources:
- https://openrouter.ai/docs/api/api-reference/o-auth/create-auth-keys-code
- https://openrouter.ai/docs/api/api-reference/o-auth/exchange-auth-code-for-api-key
- https://openrouter.ai/docs/use-cases

### Anthropic Claude, OpenCode, and Claude Code
Claude consumer subscriptions and Claude API usage are distinct. Claude Code may authenticate with supported Claude Pro/Max plans within Claude's authorized coding client; this is not evidence that a hosted Civio tutor may use those consumer subscriptions. OpenCode is a client/provider router for coding, not a customer billing channel or automatically a supported Dexter integration; its ChatGPT, Copilot and other provider connections are client workflows, not reusable hosted SaaS credentials. Do not extract CLI auth files, impersonate these apps, or send server requests with client-specific tokens. Claude API via separately funded user API credentials may be explored with legal/security review.
Sources:
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- https://docs.opencode.ai/docs/providers/

### Optional platform-funded low-cost fallback (NOT zero-dollar guarantee)
Cloudflare Workers AI publishes 10,000 free Neurons/day with limitations, then paid usage; some models require paid methods. Other Gemini API models have limited free-tier access. Free quotas and prices can change; do NOT enable automatic paid rollover, surprise expenses, or unbounded prompts. Default to hard stop and an external/free learning path.
Sources:
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://ai.google.dev/gemini-api/docs/billing/

## Candidate business packages, pricing only after unit economics + GT approval
A. Free Civio: approved question bank, mocks, deterministic tutor, mistake history, schedules, progress and offline packs, with external AI handoff. No API charges.
B. Optional learner-funded AI: provider's own billing account/credits or approved allowed connected-plan workflow. Charge neither markup on SIWC plan use nor an access toll. Maintain clear origin and remaining usage.
C. Civio Premium: legitimately independently supplied features: rich personally managed study schedules/coach dashboards, enhanced original curricula, authored reviewer/study studio, advanced analytics and institutional cohorts. Need written product and legal review before selecting which premium gates are appropriate; never gate mandatory free ChatGPT SIWC path.
D. Institutions/review centers: seats, analytics and managed courseware with explicit consent boundaries. Institutional contracts do not entitle Civio to reuse personal provider plans.

## Cost architecture and acceptance
- Separate identity auth from inference authorization, provider payment, and Civio billing. Logging in with Google does NOT purchase or authorize AI.
- Central provider adapter for external handoff (no keys), null/deterministic fallback, OpenRouter BYO-CREDIT proof of concept, optional Gemini/Cloudflare/API with separate approval. No production secret uploads.
- Meter requests and tokens per user and tenant, provider-specific caps, latency/quality/error statistics (no prompt contents by default), consent timestamps and source/provider versions; clear billing attribution and user opt-in.
- No surprise fallback from free/user-funded to Civio-paid API. On failure display no-cost path and avoid interrupting exam.
- PCI/payment processor must handle card information. Never store card numbers. Do not design subscription checkout until real merchant acceptance, tax/privacy assessment and explicit GT approval.
- Maintain full core study functionality with AI disabled. Any external provider can be disconnected; clear exported history separately from Civio's retained learning records as requested.
- For every provider claim, include a primary-source link and date of verification. Build spike only after testing public availability/partner approval and documented terms. Never describe a proposed billing route as operational.
