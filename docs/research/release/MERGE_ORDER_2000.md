# Merge order for the 2,000 Release Collection (integration-tested 2026-10-18 02:55 PHT)

A local branch `integration/2000` was built from main `f2766db` by merging the branches below in this order. Nothing was pushed. All 11 merges went through **without manual conflicts**. The three append-only docs were merged with git's `union` strategy, which keeps every section.

| # | Branch | Kind | Conflict notes |
|---|---|---|---|
| 1 | grok/fix-welcome-format | app (welcome.tsx) | none |
| 2 | grok/drill-choice-shuffle | app: drill payloads stop sending answer keys | touches CHANGES_SINCE_BASELINE.md |
| 3 | grok/fact-id-theme | app + migration (fact_id, theme) | CHANGES_SINCE_BASELINE.md: append-only, keep both sections |
| 4 | grok/batch-3-independent-audit | audit data/docs | HANDOFF_ANY_AI.md, AUDIT_TRACKER.md |
| 5 | grok/batch-4-numerical-word-problems | audit data/docs | HANDOFF and TRACKER: append-only, keep all |
| 6 | grok/baseline-550-spec-convert | baseline spec JSON (needed by release_manifest.py) | TRACKER: keep all |
| 7 | grok/gap-fill-2000-01 | FV drafts + release_manifest.py + explanation_lint.py | TRACKER: keep all |
| 8 | grok/gap-fill-2000-02 | Num + FV drafts | TRACKER: keep all |
| 9 | grok/gap-fill-2000-03 | Analytical drafts; qa.py solver additions; di_grid.py | qa.py auto-merged with 04 |
| 10 | grok/gap-fill-2000-04 | Clerical filing + R.A. 6713 drafts; qa.py; arma_solver.py | qa.py auto-merged (check the diff during review) |
| 11 | grok/gap-fill-2000-05 | EV drafts + 117 EV lint-fix drafts + qa_fixfile.py | TRACKER: keep all |

Rules for GitHub merges:
- Any conflict in `docs/research/AUDIT_TRACKER.md`, `docs/HANDOFF_ANY_AI.md` or `docs/CHANGES_SINCE_BASELINE.md` is caused by sections appended in parallel. Resolve it by keeping every section from both sides.
- `scripts/batches/explanation_lint.py` is added identically by 01, 03, 04 and 05.
- If `qa.py` conflicts, keep both sets of solver additions. 03 changed the analogy/DI solvers and 04 the filing solver.
- Other grok/* branches (dashboard-refine, deadlines-tracker-scope, exam-typography-breadcrumb, exam-workspace-timer-answers) were **not** part of this integration test. Merge them after #11 and re-run the checks.

## Results on integration/2000

- `qa_all.py`: QA GREEN. `qa_fil.py`: QA GREEN.
- `qa_file.py`: 0 problems on each of gap-fill-2000-01 (99 items), 02 (108), 03 (101), 04 (83) and 05 (15).
- `qa_fixfile.py` on gap-fill-2000-05-lintfix (117 items): 0 problems.
- `explanation_lint.py`: 0 flagged in all six files; positions are balanced.
- `release_manifest.py --include-drafts`: **EXACT**. EV 300, FV 300, Num 400, Ana 400, Cler 300, GI 300 = 2,000, and every subtopic quota is met. Exit 0.
- `release_manifest.py` counting approved items only: 1,641, not exact. The drafts need CoS approval before the Release Collection is real.
- **Caveat:** 364 of the 2,000 picks still fail explanation_lint. Most are older approved and baseline items (EV 117, FV 39, Ana 96, Cler 58, GI 54). The 117 EV failures are covered by the gap-fill-2000-05 lint-fix drafts once CoS accepts them. The remaining 247 need a lint-fix batch per subject.
