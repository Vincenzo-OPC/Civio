# Civio handoff for any AI (ChatGPT first)

Written 17 October 2026 (Asia/Manila) by Grok Bot. GT may stop paying for Grok Bot (possibly December 2026). This file explains how ChatGPT, or any other AI, takes over every job Grok Bot does on Civio. It assumes no chat history. Everything an agent needs is in this repo or in the docs linked here.

If this file and the code disagree, the code and tests win. If this file and a linked doc disagree, trust the linked doc. It is the source, and this file is only a map.

## 1. The project in brief

**Civio** is a Philippine Civil Service Exam (CSE) reviewer: Professional and Subprofessional mocks, drills, Reveal explanations, and the Dexter key check. It is **not** official CSC software. Repo: `Vincenzo-OPC/Civio`, branch `main`. Owner and final approver: GT (Gian Terence Savellano).

- **Stack:** PHP 8.4, Laravel 13, Inertia 3, React 19, TypeScript, Vite, Tailwind 4, Pest 4, Postgres (SQLite in-memory for tests), ts-fsrs (scheduler math only, not wired), PWA. Details are in [AGENTS.md](../AGENTS.md) under "Stack".
- **Checks.** Run all of these before every push that touches code:

  ```bash
  php artisan test        # Pest
  npm run types:check     # tsc --noEmit
  npm run lint:check      # eslint
  npm run test:js         # tsx --test tests/Js/*.test.ts
  npm run format:check    # prettier
  composer lint:check     # pint --test (CI runs this)
  npm run build
  npm run size            # size-limit budgets, brotli
  ```

  Docs-only commits don't need the app checks, but question JSON changes do need the Python QA (section 3).
- **CI:** [.github/workflows/tests.yml](../.github/workflows/tests.yml) runs build, types, JS tests, size and Pest on PHP 8.4 and 8.5. [.github/workflows/lint.yml](../.github/workflows/lint.yml) is check-only: `composer lint:check`, `npm run format:check` and `npm run lint:check`. Workflow files need a token with `workflow` scope, so push those from GT's own clone.
- **Bundle limit** ([.size-limit.json](../.size-limit.json)): all JS together may use 1,040 kB brotli. The last recorded figure is about 1,037,038 B, which leaves roughly 3 kB. The exam chunk may use 11 kB and was at 10.22 kB. Trim lazy chunks before you add JS, and never raise a budget without saying why in the commit. The latest figures are in [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md).
- **Push rules:** use normal `git push origin main` only. Run `git pull --rebase` first, because several agents push. Never force-push and never use `--no-verify`. Never commit secrets or `.env`. Use Conventional Commits. Add `[skip netlify]` to docs and bank-only commits. When behaviour changes, update [CHANGES_SINCE_BASELINE.md](CHANGES_SINCE_BASELINE.md) in the same commit.
- **Not deployed.** Nothing is live on the public internet. Hosting is GT's decision: [DEPLOY.md](DEPLOY.md) describes the plan, and GT must create any accounts himself. Deploys and spending need GT.

Read these in order: [AGENTS.md](../AGENTS.md), then [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) (§5 lists the security invariants), [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md) (the only roadmap), and [CIVIO_CURRENT_STATE_HANDOFF.md](CIVIO_CURRENT_STATE_HANDOFF.md).

## 2. Roles today and who replaces each

| Role | Today | Job | When Grok is gone |
|---|---|---|---|
| Engineering | **Codex Astra** (OpenAI Codex) | Owns all app code, tests, CI and the MSI clone. Builds from briefs in `docs/` | Stays the same while GT has a ChatGPT plan with Codex usage. If Codex runs out, ChatGPT can do small slices in a fresh clone under the same rules |
| Heavy UI work | **Grok Build** | Large frontend builds from briefs such as [DESIGN_IMPLEMENTATION_BRIEF.md](DESIGN_IMPLEMENTATION_BRIEF.md) and [REVIEW_MISTAKES_BRIEF.md](REVIEW_MISTAKES_BRIEF.md) | **Codex.** Paste the brief's prompt into Codex unchanged |
| Question writing | **ChatGPT** | Writes 100-item draft batches from [research/CHATGPT_NEXT_PROMPT.md](research/CHATGPT_NEXT_PROMPT.md) | Same. Prompt (b) in section 7 |
| Question review | **Chief of Staff** (a Grok agent that holds GT's delegation for Civio approvals) | Rules on review packets: accept, fix, retire, approve | **GT himself**, or a separate ChatGPT conversation that GT names as reviewer. The reviewer must never be the session that wrote or audited the items. Only GT or his named delegate may set `approved` |
| Audit, Sentinel research and QA | **Grok Bot** (CSE / Sentinel) | Audits batches with `qa.py` and by hand, writes review packets, applies rulings, imports into local Civio, runs the CSC monitor, the security probe, the competitor scan and the coverage count | **ChatGPT** (with Codex when it needs to run Python or Docker). Prompts (c) and (d), plus the checklists in sections 3 to 5 |

Briefs are how work moves between AIs. Write the task into `docs/` as a brief, commit it, and paste a short prompt that points at the file.

## 3. Question pipeline, step by step

1. **Spec.** The current spec is [CSE-Question-Design-Spec.md](CSE-Question-Design-Spec.md), **v0.1.8**. Check the `Version:` line at the top, because the rulings in §10.x get added over time. §4 has the item rules, §5 the Reveal format, §6 the fields, including the optional `shortcut` (300 characters or fewer, honest, shown first as "Shortcut: …" with the worked steps as "Method: …"), and §7 the checklist. Distractor codes are spec codes only. `qa.py` reads them from the spec file.
2. **Draft.** ChatGPT writes `docs/research/chatgpt-batch-NNN.json` (or a `gap-fill-NNN.json`) with `status: "draft"` and `review_status: "unreviewed"`. Every item needs the fields the spec requires and a `provenance` block. GI items must quote the law, checked against lawphil.net or the official text. Filing explanations cite ARMA (ANSI/ARMA 12-2005) as "not a rule published by the CSC".
3. **Automated QA** (a full clone with Python 3 is required; a GitHub connector cannot run it):
   - [scripts/batches/qa.py](../scripts/batches/qa.py) is a library: `check_item`, `check_round(items, prior_stems)` (near-duplicate at 0.65 token overlap), `baseline_hits`, `check_batch_rules`, `check_bank_rules` and `check_gi_evidence`. It covers solver-recomputed keys, required fields, spec codes, no order key matching the listed order, unique spelling targets with matching error codes, the 25% stem cap per domain, KWF spelling (no `nakaka-`, no `kanya/kanyang`), no option inside its own Filipino vocabulary stem, and the shortcut length.
   - `python3 scripts/batches/qa_all.py` checks the whole generated bank (batches 002–011 plus any `round-*-fixes.json` overlays). `--no-fixes` checks the committed batch files alone. It exits 1 on any failure.
   - `python3 scripts/batches/qa_fil.py` checks the Filipino pool and lists key/trap pairs, which the mock builder keeps apart.
   - Items with no solver (Filipino, RC, hand-written GI) are keyed by hand. Say so in the packet, and never claim QA passed when it didn't run.
4. **Review packet.** Write `docs/research/audit/round-NN-<scope>-review-request.md`, copying the shape of [round-03-baseline-b2-gi-review-request.md](research/audit/round-03-baseline-b2-gi-review-request.md):
   - a header (author, date, source file or DB export, "No content was changed")
   - a **Summary** with counts per verdict (`KEY ERROR / FIX / DUPLICATE / OK` for existing rows, `ACCEPT / ACCEPT as variant / FIX / HOLD / REJECT` for new drafts)
   - a **Per item** table (`ID | Sub | Key now | Finding | Verdict | Proposal`)
   - the questions for the reviewer

   Put the script that regenerates it in `scripts/batches/audit/`. Proposed rewrites go in a separate JSON file (as in `research/round-02-fixes.json`, where each item carries a `replaces` field with the old stem and key), never into the source batch.
5. **Ruling.** The reviewer rules item by item. Apply exactly what was ruled, rerun QA until it's green, then set `status: "approved"` and `review_status: "passed"` on the approved items only. Never approve your own work.
6. **Import.** Run `php artisan civio:import-batch <file> --dry-run`, then the same without `--dry-run`. With the default `--status=active`, the importer refuses any item that isn't `approved` plus `passed`. Use `--status=draft` to load unreviewed items for viewing. The importer upserts by **stem** in `source_group='civio'`, so a reworded item creates a new row.
7. **Retire old-stem rows.** After a reworded item is imported, set the old row to draft (history kept, never deleted). In the local DB: `UPDATE questions SET status='draft' WHERE source_group='civio' AND stem = '<old stem>';`. Baseline duplicates retire the same way, by `id`. Then clear the cache (`php artisan cache:forget questions.active`, or restart the app).
8. **Log it** in [research/AUDIT_TRACKER.md](research/AUDIT_TRACKER.md), the single source of progress: a dated section with the counts, the decisions, the files and what's next. Update the table at the top when a round closes.

**Target:** first milestone **exactly 2,000 approved questions**, a clean hundred per subject (GT, 17 October 2026). The split and the Release Collection are proposed in [research/MILESTONE_2000_PLAN.md](research/MILESTONE_2000_PLAN.md), pending GT's approval. The long-term goal stays about **3,000 verified active questions**. The local DB had 1,856 active items that day. Fill the gaps in [research/audit/COVERAGE_GAP_MAP.md](research/audit/COVERAGE_GAP_MAP.md) and Sentinel §F7 first: English reading comprehension, paragraph organization and sentence structure, plus GI peace and human rights. Ease off percent change. No filler clones (see AGENTS.md, "Question bank rule").

**Open question work as of 17 October 2026** (check AUDIT_TRACKER.md for anything newer):
- Fix the 12 baseline spelling rows by swapping in new target words.
- Write gap-fill-004: 2 items each on R.A. 7610, 9710, 9745, 10353 and 9851.
- Audit `chatgpt-batch-002.json` (100 English drafts).
- Baseline B3 (branch grok/batch-3-independent-audit) and B4 Numerical word problems (branch grok/batch-4-numerical-word-problems) await CoS verdicts. Next baseline batches: B5 Analytical 114, B6 Verbal 130. Run `scripts/batches/audit/explanation_lint.py` on every batch with `qa_file.py`.
- Audit Codex's 496-item `scripts/seeds/baseline_reparameterized.json` as its own round.

## 4. Local Civio on GT's MSI

- Clone: `C:\Users\GT\Desktop\Claude\Civio` (Entire hooks run there; see [ENTIRE.md](../ENTIRE.md)).
- Stack: [docker-compose.local.yml](../docker-compose.local.yml), project `civio-local`. The app runs in container `civio-local-app` at http://localhost:8090, and Postgres in `civio-local-db` on `127.0.0.1:5434` (database `civio_local`, user `civio`).
- **Never touch** the older study stack on `:8080` / `:5433` (containers `previous-review-app` and `previous-review-db`) or Hermes on `:8642`. Don't stop, rebuild or query them.

Rebuild after a `git pull`. Always back up first. Copy the dump out with `docker cp`, not a PowerShell `>` pipe, because Windows PowerShell 5.1 corrupts binary and non-ASCII output:

```powershell
cd C:\Users\GT\Desktop\Claude\Civio
git pull --rebase
$d = Get-Date -Format yyyyMMdd-HHmm
docker exec civio-local-db pg_dump -U civio -d civio_local -Fc -f /tmp/civio-$d.dump
docker cp civio-local-db:/tmp/civio-$d.dump .\backups\civio-$d.dump
docker compose -p civio-local -f docker-compose.local.yml up -d --build --no-deps app
```

`--no-deps` rebuilds only the app and leaves the DB container alone. To import a batch into the running app:

```powershell
docker cp .\docs\research\gap-fill-004.json civio-local-app:/tmp/batch.json
docker exec civio-local-app php artisan civio:import-batch /tmp/batch.json --dry-run
docker exec civio-local-app php artisan civio:import-batch /tmp/batch.json
```

To count active items per subject:

```powershell
docker exec civio-local-db psql -U civio -d civio_local -c "SELECT c.name, count(*) FROM questions q JOIN subcategories s ON s.id=q.subcategory_id JOIN categories c ON c.id=s.category_id WHERE q.status='active' GROUP BY c.name ORDER BY 1;"
```

## 5. Sentinel duties as manual weekly checklists

Sentinel is independent research and QA. It never edits app code, approves questions or deploys. Findings go in a new dated `docs/research/sentinel/DOSSIER_YYYY-MM-DD.md` and a row in [research/sentinel/README.md](research/sentinel/README.md). Evidence labels: A = reproduced or official primary source, B = code or vendor page read, C = secondary or snippet, D = anecdote. The first dossier is [DOSSIER_2026-10-17.md](research/sentinel/DOSSIER_2026-10-17.md).

**CSC monitor.** Run it daily from 1 November 2026 through the March 2027 exam, and weekly otherwise.
- [ ] Open https://csc.gov.ph/examination-advisories and the exam-announcement download lists for 2026 and 2027 (links are in Dossier §1). **Official csc.gov.ph only.** Never take a date from cse.ph, reviewers, news or social media. cse.ph had wrong dates on 17 October 2026.
- [ ] Look for: the specific March 2027 announcement (requirements, centres, scope, passing grade), filing news (filing opens 2 November 2026), school assignments for the 22 November 2026 reset exam, and any move of the reset to 24 January 2027.
- [ ] If something changed, update `app/Support/CseExamDates.php` and its `LAST_CHECKED` through Codex (it's app code). Then tell GT in one line, with the link.

**Security probe.** Run it weekly, and after any change to `routes/`, `app/Services/Exam*`, `app/Http/Controllers/User/Exam*`, grading or submit actions, `resources/js/pages/user/exams/**` or migrations.
- [ ] In a **scratch clone** (never commit it), add the Pest file from Dossier **Appendix A** and run `php artisan test tests/Feature/SentinelProbe`.
- [ ] Check the invariants in [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §5.
- [ ] Report regressions to GT and Codex. On 17 October 2026, P1–P4 still showed the bugs (answer keys during a Strict Mock, subset submit, late submit, draft keys via Reveal). Once Codex fixes them, the flipped tests become regression tests.

**Competitor and tech scan.** Mondays.
- [ ] Check prices and plans at CSEPass, cseexamreview.com, Super Tutor and CSE Buddy (URLs in Dossier §F10), and look for new Philippine CSE entrants.
- [ ] Check releases of ts-fsrs, LanguageTool (Tagalog) and calamanCy that matter to Civio.
- [ ] Send one digest, or nothing if nothing changed. Label search snippets as evidence C.

**Coverage count.** Thursdays, and after a batch merges.
- [ ] Count active items per domain and concept (section 4 SQL), and drafts per file in `docs/research/*.json` and `docs/batches/*.json`.
- [ ] Compare against the target (section 3), the official scope (spec §1) and [COVERAGE_GAP_MAP.md](research/audit/COVERAGE_GAP_MAP.md). Flag any concept that is thin or over a cap.
- [ ] Turn the biggest gap into the next ChatGPT batch prompt.

## 6. Standing rules

- Write **Civio** in Title Case. Lowercase only in identifiers and URLs. The tutor is **Dexter**, and Dexter is a key check, not a chat tutor.
- Never say or imply that Civio is official CSC or endorsed by the CSC.
- Never put another app's name in the product, code, UI or seeds. The product is Civio everywhere.
- No invented stats, pass rates, readiness scores or "AI predictor" percentages. Meters must come from stored data. Sentinel §F3 flags the current dashboard card.
- No deploy, no spending and no new accounts without GT.
- Drafts stay `draft` and inactive until reviewed and approved (section 3). Never auto-approve.
- No new bank items or question-text edits outside the pipeline. No filler clones.
- UI constraints: [AGENTS.md](../AGENTS.md), plus the "Do not restore" and "Design that stays" sections of [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md) (violet `#5B35F5`, logo green `#B3F52D`, no Auto-Next, no new animation package, keep the bundle budget).
- Security invariants: [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §5. No answer keys in the live exam payload, and the server grades.
- Never touch the protected MSI containers or Hermes (section 4).

## 7. Copy-paste prompts for ChatGPT

**(a) Project onboarding**

```
You are taking over audit, QA and research work on Civio, a Philippine Civil Service Exam reviewer, in GitHub repo Vincenzo-OPC/Civio (branch main). Civio is not official CSC software; never imply it is. Write "Civio" in Title Case.
Read, in order: docs/HANDOFF_ANY_AI.md, AGENTS.md, docs/CODEX_HANDOFF_PLAN.md (section 5), docs/CIVIO_NEXT_AGENT_EXECUTION_PLAN.md, docs/CSE-Question-Design-Spec.md (note the version) and docs/research/AUDIT_TRACKER.md.
Then tell me in plain words: what Civio is, what is built, what the open question work is, and the 5 rules you must never break. Do not change any file yet. Never deploy, spend, approve your own work, force-push, or touch the MSI containers on ports 8080/5433 or Hermes on 8642.
```

**(b) Question batch.** Open [research/CHATGPT_NEXT_PROMPT.md](research/CHATGPT_NEXT_PROMPT.md) and paste everything below its line. For a new batch, first change the file name, counts and archetypes to the gap the coverage count found, and keep every rule in it.

**(c) Audit**

```
Audit docs/research/<FILE>.json in GitHub repo Vincenzo-OPC/Civio (main) as Civio's question auditor. Follow docs/HANDOFF_ANY_AI.md section 3 and docs/CSE-Question-Design-Spec.md (current version).
1. In a full clone, run python3 scripts/batches/qa.py checks (check_item, check_round against all existing stems at 0.65, baseline_hits, check_batch_rules, check_bank_rules) and qa_all.py / qa_fil.py where relevant. If you cannot run Python, say so plainly; never claim QA passed.
2. Re-key every item by hand where no solver exists. Check every GI quote against lawphil.net or the official text.
3. Write docs/research/audit/round-NN-<scope>-review-request.md in the same shape as round-03-baseline-b2-gi-review-request.md (Summary counts, per-item table with verdict and proposal, questions for the reviewer). Put proposed rewrites in a separate JSON; do not edit the source batch.
4. Add a dated section to docs/research/AUDIT_TRACKER.md. Commit with [skip netlify], git pull --rebase, normal push. Keep every item draft. Do not import, approve or deploy.
```

**(d) Weekly Sentinel**

```
Run this week's Civio Sentinel checks from docs/HANDOFF_ANY_AI.md section 5 for repo Vincenzo-OPC/Civio: (1) CSC monitor on csc.gov.ph only, (2) security probe from docs/research/sentinel/DOSSIER_2026-10-17.md Appendix A in a scratch clone (never commit it), (3) competitor and tech scan, (4) coverage count against the 2,000 milestone in docs/research/MILESTONE_2000_PLAN.md (long-term goal about 3,000).
Label evidence A/B/C/D. Do not edit app code, approve questions or deploy. If anything changed, write docs/research/sentinel/DOSSIER_<today>.md, add a row to docs/research/sentinel/README.md, commit with [skip netlify], pull --rebase and push normally. Then give me a 5-line summary, ranked, with links. If nothing changed, say "No change" and write nothing.
```
