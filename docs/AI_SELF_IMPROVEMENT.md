# AI Self-Improvement: Civio Participation

**Status:** Future opt-in evaluation target, not an active autonomous feature.
**Recorded:** 2026-10-08.
**Canonical evolution engine:** [THE-MACHINE](https://github.com/Vincenzo-OPC/THE-MACHINE), `docs/24_RECURSIVE_SELF_IMPROVEMENT.md`.

## Intent

Civio is the **first proposed external test repository** for THE-MACHINE's agent-level recursive self-improvement (RSI), because its Laravel/Pest and React/TypeScript checks provide measurable software tasks. Do not build a separate RSI engine in Civio. Civio's immediate product roadmap remains authoritative; this research does not automatically outrank current security fixes, study flows, or launch tasks.

## Candidate improvements to benchmark

1. Improve *coding agents' development workflow* on scoped Civio maintenance tasks: defect detection, type-safe refactors, test generation, accessibility, Lite/offline performance and cost per accepted solution.
2. Later, independently benchmark Dexter tutor prompt/retrieval strategies against approved factual-answer, learning-quality and hallucination checks. A better-sounding explanation is **not** proof of improved teaching.
3. Track candidate generation/lineage in THE-MACHINE; verify against untouched holdout tests and compare to both the unchanged agent and fixed meta-strategy.

## Guardrails

- Preserve server-side grading, answer-key secrecy, strict mock bank uniqueness, question-source policy and `offline_eligible` separation.
- Do not generate/add/modify approved question-bank items without the explicit design approval required by `docs/CSE-Question-Design-Spec.md`.
- Never alter tests, grading rules or hidden evaluation answers to improve a score. Use held-out fixtures under independent control.
- No MSI Docker container disruption, no client-side API keys, no learner PII in model prompts or stored experiments.
- No unattended merges, hosting changes or production deployment. Follow AGENTS.md, CLAUDE.md, and `docs/CODEX_HANDOFF_PLAN.md`.
- Local benchmark work is optional and budget-capped; first show an improvement over using the existing Codex agent normally.

## Agent procedure on relevant future tasks

Read AGENTS.md and handoff plan; identify one narrow, measurable task and acceptance test; establish baseline; only then propose a reversible experiment. Changes produced by an experimental agent are reviewable candidates, not approved code. Preserve Git lineage, run required repo checks before any release, log negative results. Do **not** start a self-modification loop simply because this note exists.

## Success criterion

Reproducibly higher held-out task success at similar or lower cost and no security, grading, reliability, accessibility or Lite-mode regression. If the improvement fails these criteria, retain the findings without adoption.
