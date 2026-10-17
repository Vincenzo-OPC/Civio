# Milestone 2,000: proposed subject split and Release Collection

- **Status: PROPOSAL.** GT approves it before anything changes. This file changes no app code, no database row and no question.
- Written 17 October 2026 (Asia/Manila) by Grok Bot for GT, Chief of Staff (CoS) and Codex Astra.
- Repo state read: `main` at `2313fbd` (17 Oct 2026, 15:46 PHT).
- GT's decision (17 Oct 2026): the first milestone is **exactly 2,000 approved, high-quality questions**. Each subject's count must be a clean hundred. The long-term goal stays **about 3,000**. This replaces the earlier "about 3,000, about 2,000 usable in a Subprofessional mock" line in [HANDOFF_ANY_AI.md](../HANDOFF_ANY_AI.md) §3 as the near-term target. The 3,000 goal is unchanged.

## 1. Recommendation in one table

| Subject | Levels | GT's example | **Recommended** | Active now (MSI) | Approx. new items needed |
|---|---|---:|---:|---:|---|
| Verbal Ability (English 300 + Filipino 300) | Both | 600 | **600** | 604 | 118 to 152 |
| Numerical Ability | Both | 400 | **400** | 400 | 38 to 129 |
| Analytical Ability | Professional only | 300 | **400** | 365 | 92 to 152 |
| Clerical Ability | Subprofessional only | 300 | **300** | 262 | 41 |
| General Information | Both | 400 | **300** | 347 | about 20 to 45 |
| **Total** | | 2,000 | **2,000** | 1,978 | **about 310 to 520** |

"New items needed" is the number of new approved items it takes to fill every subtopic floor in §5 while honouring the caps. The low end assumes every baseline item that has not been audited yet passes its audit. The high end assumes every one of them fails. Earlier audits found about a fifth to almost half of a baseline slice duplicated, so expect a figure in between (§3.4).

**Why this differs from GT's example (one swap: Analytical 400, GI 300):**
1. Analytical is the largest block in a Professional mock (52 of 150 items, `MockPoolSelector::BLUEPRINT`). At 300 items it gives only 5 full Professional mocks without repeating an Analytical item. At 400 it gives 7 (§4).
2. GI takes only 8 items per mock. 300 GI items still give 37 non-repeating mocks, and 400 would mostly add recall items on the same few statutes. R.A. 6713 is a single law: a 400-item GI set at the spec's 35% share would need 140 items on it, which invites the repeated facts GT ruled out.
3. Analytical is genuinely thin where it matters. Word analogy is 59 of 365 items (16%) against the spec's 30% practice mix, and data interpretation is 69 (19%) against 25%. Symbol series alone is 31% of Civio's approved Analytical items.
4. Verbal stays 600 because it has the most ground to cover: six CSC areas in two languages (12 cells, about 50 items each). The spec says Filipino is half of Verbal, and Filipino has only 189 items today.
5. Clerical stays 300. It has only two CSC areas (150 items each at 300). Going to 400 would cost 138 new items for one more Subprofessional mock.

## 2. What the CSC actually covers (checked 17 Oct 2026)

Source: [CSC Examination Announcement No. 03, s. 2026 (PDF)](https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf), §F "Scope of Examination", read 17 Oct 2026. Evidence A.

| Subject | Professional | Subprofessional | CSC subtopics |
|---|---|---|---|
| General Information (in English) | Yes | Yes | Philippine Constitution; R.A. 6713; Peace and Human Rights Issues and Concepts; Environment Management and Protection |
| Verbal Ability (in English and Filipino) | Yes | Yes | Word meaning; sentence completion; error recognition; sentence structure; paragraph organization; reading comprehension |
| Analytical Ability (in English) | Yes | **No** | Word analogy; symbolic logic/abstract reasoning; identifying assumptions and drawing conclusions; data interpretation |
| Clerical Ability (in English) | **No** | Yes | Filing; spelling |
| Numerical Ability (in English) | Yes | Yes | Basic operations; number sequence; word problems |

Passing grade: a general rating of at least 80.00 (§G).

Caveats:
- This is the **August 2026** announcement. CSC promised a specific announcement for the **14 March 2027** sitting about three weeks before filing opens on 2 Nov 2026. As of 17 Oct 2026 it is not posted: the [Examination Advisories list](https://csc.gov.ph/examination-advisories) ends at Advisory No. 18 (16 Oct 2026), and the [2026 exam-announcement downloads](https://www.csc.gov.ph/downloads/examination/category/560-exam-announcement-2026) list Nos. 01 to 04 plus the FSO notice. Re-check the scope when it appears. The calendar itself is [Announcement No. 05, s. 2026](https://csc.gov.ph/examination-advisories/examination-announcement-no-05-s-2026-calendar-of-civil-service-examinations-pen-and-paper-test-for-cy-2027).
- **CSC publishes no item counts or weights per subject.** The announcement lists topics only. The mock quotas (Verbal 45, Analytical 52, Numerical 45, Clerical 47, GI 8) are Civio's own. They were ported from the baseline client pool builder in `c825fe9` ([LITE_MODE_PLAN.md](../LITE_MODE_PLAN.md)). [COVERAGE_GAP_MAP.md](audit/COVERAGE_GAP_MAP.md) says the same. The practice mixes in spec §8 / [CODEX_HANDOFF_PLAN.md](../CODEX_HANDOFF_PLAN.md) §8.2 are also Civio's choices, "recalibrated with data". Nothing in this plan claims an official weighting.

## 3. The bank today

### 3.1 Live counts (MSI `civio-local-db`, read-only SELECTs, 17 Oct 2026)

1,978 active items and 227 drafts. No item is `offline_eligible`.

| Subject | Active | Civio (approved JSON) | Baseline | Subcategory labels in use |
|---|---:|---:|---:|---:|
| Verbal Ability | 604 | 475 (English 287, Filipino 188) | 130 | 9 |
| Numerical Ability | 400 | 309 | 91 | 4 |
| Analytical Ability | 365 | 251 | 114 | 7 |
| General Information | 347 | 236 | 111 | 39 |
| Clerical Ability | 262 | 207 | 55 | 3 |
| **Total** | **1,978** | **1,477 in the DB** (1,478 approved in repo JSON) | **501** | |

The repo JSON has one more approved Verbal item than the DB (605 against 604). The difference is not traced yet.

### 3.2 Per CSC subtopic

Civio items are counted by `archetype` in the approved batch JSON (`docs/batches/batch-*.json` and `docs/research/*.json`, excluding the `round-02-fixes.json` overlay that is already merged). Baseline items are counted by their DB subcategory.

**Verbal, English (416).**

| CSC area | Civio archetypes | Civio | Baseline | Total |
|---|---|---:|---:|---:|
| Word meaning | VEN-WORD-MEANING | 54 | 30 | 84 |
| Sentence completion | VEN-SENT-COMP-WORD 59, -PHRASAL 12 | 71 | 28 | 99 |
| Error recognition | VEN-ERROR-AGREE 31, -TENSE 30, VEN-ERROR 5 | 66 | 19 | 85 |
| Sentence structure | VEN-SENT-STRUCTURE | 20 | 17 | 37 |
| Paragraph organization | VEN-PARA-ORDER 12, -INSERT 8, VEN-PO 3 | 23 | 16 | 39 |
| Reading comprehension | VEN-RC-VOCAB 22, -INFER 15, -DETAIL 7, -MAIN 5, VEN-RC 4 | 53 | 19 | 72 |

**Verbal, Filipino (189).** Synonym and vocabulary 49 (VFIL-KASINGKAHULUGAN 25, VFIL-VOCAB 24), antonym 20, idiom (sawikain) 23, grammar and completion 46 (VFIL-BALARILA 15, VFIL-GRAM 10, VFIL-COMP 20, plus 1 baseline), reading 35, paragraph order 16.

**Numerical (400).** Basic operations 87 (Civio 56: OPS-ORDER 30, FRAC-DEC 20, OPS-FRAC-DEC 6; baseline 31). Number sequence 77 (49 + 28). Word problems 236 (Civio 204: **PCT-CHANGE 78**, RATIO 30, RATE 29, AVERAGE 27, GEOM 24, ALGEBRA 16; baseline 32).

**Analytical (365).** Word analogy 59 (30 + 29). Symbolic logic 108 (SYMBOL-SERIES 77 + 31). Assumptions and conclusions 129 (SYLLOGISM 45, CONCLUSION 39, ASSUME-I-II 19, plus 26). Data interpretation 69 (DI-TABLE 41 + 28).

**Clerical (262).** Filing 124 (Civio 94: FILE-POSITION 58, FILE-ORDER 16, NAMES 8, NUMERIC 6, CHRONOLOGICAL 6; baseline 30). Spelling 138 (Civio 113: SPELL-WRONG 57, SPELL-RIGHT 36, SPELLING 20; baseline 25).

**General Information (347).** Constitution 136 (baseline 38). R.A. 6713 85 (37). Peace and human rights 53 (9). Environment 73 (27). Civio GI by item type: GI-DEADLINE-NUMBER 60 (25%), GI-TERM-MATCH 46 (19%), GI-SOURCE-BASED-SCENARIO 30, GI-RIGHTS-APPLY 29, GI-SCENARIO-APPLY 27, GI-WHO-HOLDS-POWER 23, GI-ENV-PRINCIPLE 21. Recall types are 44% of Civio GI. Applied types are 36%.

### 3.3 Lopsided areas

- **Percent change** is 78 items, 25% of Civio's approved Numerical items (Sentinel [F7](sentinel/DOSSIER_2026-10-17.md) counted about 26%).
- **Basic operations** is 22% of Numerical against the spec's 30% mix.
- **Word analogy** (16% of Analytical) and **data interpretation** (19%) are under the spec's 30% and 25%. Symbol series is 31% of Civio Analytical.
- **Filipino** is 31% of Verbal. The spec says it is half (spec, Filipino section: "Filipino half of Verbal"). Filipino antonyms (20) and paragraph order (16) are thinnest.
- **English paragraph organization** (39) and **sentence structure** (37) were the big gaps. gap-fill-005 filled them partly.
- **GI is recall-heavy.** Deadlines and term matching are 44% of Civio GI. R.A. 6713 has 85 items on one statute.
- **Difficulty labels are not data.** They are author-assigned. 1,246 of 1,478 approved Civio items say `medium`, and Analytical is 250 of 251 `medium`. Nothing in this plan uses them as a floor until real item statistics exist (Sentinel F8).
- **Track tags.** Five items use `pro` or `sub` instead of `professional` or `subprofessional`. That's harmless today, but it needs normalizing before a collection reads them.

### 3.4 Baseline items not yet audited

Round 03 audited baseline Clerical (B1, 81 items: 3 key errors, 37 duplicates retired) and baseline GI Constitution plus Peace and Human Rights (B2, 70 items: 14 duplicates). See [AUDIT_TRACKER.md](AUDIT_TRACKER.md). These are **not audited yet**: Analytical 114, Verbal 130, Numerical 91, and GI R.A. 6713 plus Environment 64, about **399 items**. Codex's 496-item reworded set (`scripts/seeds/baseline_reparameterized.json`) is unapplied and gets its own audit round. **Proposal:** a baseline item joins the Release Collection only after it passes its round-03 audit.

### 3.5 Mock composition follows subcategory labels, not CSC topics (new finding)

Evidence B: read in `MockPoolSelector::quotasForSubcats` at `2313fbd` and checked against the MSI label counts. Not run.

With no weak-topic bias, a subject's mock quota is split **evenly across the subcategory labels present**, whatever their size. A label with fewer items than its share contributes all of them, and the remainder tops up from the whole subject. Consequences on today's DB:

- **GI:** 39 labels for 8 slots. 30 of those labels hold a single item each. They come from `subprofessional-general-info-supplement-001.json`, whose `competency` field is a micro-topic (e.g. "Composting", "Habitat"). Each mock draws 8 labels at random, so on average about 6 of its 8 GI items come from those 30 items, which are 9% of the GI pool, and mostly environment.
- **Numerical:** 4 labels, so about 11 slots each. The label "Numerical Ability" holds only 6 items (gap-fill-002 fractions and decimals), so **all 6 appear in every unbiased mock**. Word problems (256 items in the DB) get about 11 slots plus the top-up.
- **Clerical:** 3 labels, so about 15 or 16 slots each. "Clerical Ability" holds 16 filing items (gap-fill-001 to 003), so nearly all of them appear in every Subprofessional mock.
- **Verbal:** labels such as "Grammar and correct usage" (117) and "Vocabulary" (84) are not CSC area names. Filipino gets at most 2 of the about 5 slots in each of the 6 labels that have Filipino items. That's about 12 of 45, not the half the spec intends.

So a curated collection with good subtopic floors would still produce lopsided mocks until (a) labels map to the CSC subtopics and (b) the selector applies per-subtopic quotas. Both are in the Codex brief (§7). Relabelling rows is a bank data change, so it needs GT's approval.

## 4. How many non-repeating mocks each split supports

A mock never repeats an item, but nothing stops the next mock reusing items. "Non-repeating mocks" here is `floor(subject pool ÷ quota per mock)`, the number of full mocks a learner can take before seeing any item in that subject again. Quotas per mock: Professional Verbal 45 + Analytical 52 + Numerical 45 + GI 8 = 150. Subprofessional Verbal 45 + Clerical 47 + Numerical 45 + GI 8 = 145.

| Split | Verbal | Numerical | Analytical | Clerical | GI | Professional (binding subject) | Subprofessional (binding subject) |
|---|---:|---:|---:|---:|---:|---|---|
| Today (1,978 active) | 13 | 8 | 7 | 5 | 43 | **7** (Analytical) | **5** (Clerical) |
| GT's example | 13 | 8 | 5 | 6 | 50 | **5** (Analytical) | **6** (Clerical) |
| **Recommended** | 13 | 8 | 7 | 6 | 37 | **7** (Analytical) | **6** (Clerical) |
| Alternative: Verbal 500, Clerical 400 | 11 | 8 | 7 | 8 | 37 | 7 | 8 (Clerical / Numerical) |

- Per level, the recommended collection holds **1,700 Professional-usable items** (Verbal, Numerical, Analytical, GI) and **1,600 Subprofessional-usable items** (Verbal, Numerical, Clerical, GI). 1,300 of them are shared.
- The alternative row is there in case GT wants more Subprofessional mocks. It costs 100 Verbal items (thinner Filipino) and needs about 138 new Clerical items. I don't recommend it for the first milestone.
- If Astra or GT later raise GI's share per mock (the 8 is not official), 300 GI items still support 15 mocks at 20 GI per mock.

## 5. Floors and caps inside each subject (proposal)

Floors and caps use the approved practice mixes (spec §8 / CODEX_HANDOFF_PLAN §8.2) unless marked as a proposed change, which needs a CoS ruling and GT approval.

| Subject | Subtopic | Floor or target in the collection | Have (incl. unaudited baseline) | New needed (low to high) |
|---|---|---|---:|---|
| **Verbal EN 300** | Word meaning 15% | 45 | 84 | 0 |
| | Sentence completion 20% | 60 | 99 | 0 |
| | Error recognition 20% | 60 | 85 | 0 |
| | Sentence structure 10% | 30 | 37 | 0 to 10 |
| | Paragraph organization 15% | 45 | 39 | 6 to 22 |
| | Reading comprehension 20% | 60, as passage sets of 2 or 3 (spec §10.8) | 72 | 0 to 7 |
| **Verbal FIL 300** | Synonym 25% | 75 | 49 | 26 |
| | Antonym 20% | 60 | 20 | 40 |
| | Idiom 15% | 45 | 23 | 22 |
| | Grammar 15% (incl. completion) | 45 | 46 | 0 |
| | Reading 15% | 45 | 35 | 10 |
| | Paragraph order 10% | 30 | 16 | 14 |
| **Numerical 400** | Basic operations 30% | 120 | 87 | 33 to 64 |
| | Number sequence 20% | 80 | 77 | 3 to 31 |
| | Word problems 50% | 200, with **percent change capped at 40** (10% of Numerical) and no other WP archetype above 60 | 236 (78 percent change) | 2 to 34 |
| **Analytical 400** | Word analogy 30% | 120, spread across the analogy relations (function, part-whole, degree, synonym/antonym, form) | 59 | 61 to 90 |
| | Symbolic logic 20% | 80 (cap; symbol series is over) | 108 | 0 to 3 |
| | Assumptions and conclusions 25% | 100 (cap) | 129 | 0 |
| | Data interpretation 25% | 100, text tables only (spec §8.4) | 69 | 31 to 59 |
| **Clerical 300** | Filing 55% | 165; no single filing format above 40% of filing; all ARMA rules 1 to 8 present | 124 (all audited) | 41 |
| | Spelling 45% | 135; one target word per item, bank-wide (qa.py) | 138 | 0 |
| **GI 300** (proposed topic mix) | Constitution | 120 | 136 | 0 |
| | R.A. 6713 | **90 (proposed; spec mix says 35% = 105)** | 85 | 5 to 42 |
| | Peace and human rights | **50 (proposed; spec 15% = 45)** | 53 | 0 |
| | Environment | **40 (proposed; spec 10% = 30)** | 73 | 0 |
| | Across GI | Recall types (deadline, term match) at most 35%. Applied types (scenario, rights-apply, source-based) at least 35% | Civio: recall 44%, applied 36% | about 20 applied items |

Rules that apply to every subject:
- **No repeated facts.** Items that share a `fact_id` may both sit in the collection (recall and applied formats, CoS round 03), but a mock serves only one ([FACT_ID_MOCK_RULE_BRIEF.md](../FACT_ID_MOCK_RULE_BRIEF.md)). At most 2 items per `theme` per mock. A reading passage set counts as one passage.
- **No frame over 25% of a subject** (the existing qa.py stem cap), and no near-duplicates at 0.65 token overlap.
- **No filler and no "(variant N)" clones** (AGENTS.md, "Question bank rule"). If a floor can't be met with good items, the collection stays short and the shortfall is reported. It is never padded to reach the round number.
- **Filipino mapping (open question for CoS).** The spec's Filipino mix folds sentence completion, error recognition and sentence structure into "grammar 15%". CoS may want a separate small floor for each, since the CSC lists all six areas for both languages.

## 6. Release Collection versus the full verified bank

There are two different things, and they shouldn't be confused:

- **The verified bank** is every item with `status = active` that passed review. Today that's 1,978. It keeps growing toward 3,000. Drills, Review Mistakes, offline packs and future spaced review use the whole bank.
- **The 2,000 Release Collection** is a curated, versioned **selection** from the verified bank: exactly 2,000 items in clean hundreds per subject, meeting the floors and caps in §5. It's what "Milestone 2,000" means, and it's what full mocks draw from first.

What does not happen:
- No approved item is retired, set to draft or deleted to make the numbers round. Surplus verified items, about 290 once the gaps are filled, **stay active** in the bank and keep serving drills and practice.
- Being outside the collection is not a quality verdict. It means "over a cap for this release" (for example the 38 percent-change items above the cap of 40) or "baseline item not audited yet".
- The collection never contains a draft, a rejected item or an unaudited baseline item.

How membership is decided:
1. A script, the audit agent's job, proposes the membership from the approved JSON plus the DB. It ranks within each subtopic: audited and approved first, then applied over recall in GI, items with a checked Reveal solver, stem variety (no frame over 25%), and the one-per-`fact_id` spread. It writes a review packet listing every included and excluded item with its reason.
2. CoS reviews the packet under the existing flow (spec §8.5, [HANDOFF_ANY_AI.md](../HANDOFF_ANY_AI.md) §3). GT approves the manifest. Nobody approves their own work.
3. New items reach the collection only through the normal pipeline: ChatGPT drafts, Grok Bot (or its replacement) audits with qa.py, CoS rules, then approval and import. No new review shortcut is created.

## 7. Brief for Codex: implementing the collection (proposal; Astra decides the engineering)

Recommended shape: **a versioned membership table**, not a boolean flag.

1. **Tables.** `question_collections` (`slug` such as `release-2000`, `version`, `status` draft/approved, `approved_by`, `approved_at`, `notes`) and `question_collection_items` (`collection_id`, `question_id`, `subject`, `subtopic`, `reason`, timestamps; unique on collection and question). Question rows stay untouched, so approved content is never edited to join a collection.
   - Why not `questions.in_release` (boolean): it has no version history, the 3,000 milestone would overwrite it, and it can't compare scores across releases.
   - Why not a JSON-only tag: the selector runs on the DB.
2. **Manifest in the repo.** For example `docs/research/collections/release-2000.v1.json`, listing item **stable IDs**, not DB IDs, because MSI and production IDs differ. Civio items already have stable IDs (`CIVIO-…`). Baseline items don't. They need one, for example `BASELINE-<id>` from the `audit/data/baseline-550-2026-10-17.json` export, or a stem hash. **Open decision.**
3. **Command.** Something like `php artisan civio:sync-collection <manifest> [--dry-run]`. It refuses any item that isn't active and approved, reports per-subtopic floors and caps, and fails when a subject is not its clean hundred. It never changes question rows.
4. **Prerequisites.** (a) Normalize subcategory labels to the CSC subtopics (bank data change, GT approval). (b) Per-subtopic quotas in `MockPoolSelector` that follow the practice mix, not the label count (§3.5). (c) The `fact_id`, `theme` and `passage_id` rules in [FACT_ID_MOCK_RULE_BRIEF.md](../FACT_ID_MOCK_RULE_BRIEF.md).
5. **Where mocks draw from (recommendation).** Full mocks, Study and Strict, draw from the active collection first. When a learner has already seen the collection's items in a subtopic, the selector may top up from other **verified active** items in the same subtopic, never from drafts. Store the collection slug and version on `exam_sessions` so Strict Mock results can be compared within one release. Until an approved collection can fill a full 150/145 mock, mocks keep using the whole active bank as today, so mock length never regresses. Drills, Review Mistakes and offline packs use the whole verified bank.
6. **Offline packs.** Offline items never enter mocks (invariant 5). The planner must not mark collection items offline unless full mocks still fill, the same check `civio:mark-offline-eligible` already runs.
7. **Security first.** This comes after the F1, F2 and F6 fixes in [ASTRA_PENDING_HANDOFF.md](../ASTRA_PENDING_HANDOFF.md) §1. No collection endpoint may return keys or explanations.
8. **Tests (Pest).** A collection mock fills 150/145 when the collection can. It never includes a non-collection item while unseen collection items remain in that subtopic. A manifest with a draft item is rejected. Per-subtopic quotas hold. Drills are unaffected. A missing collection falls back to today's behaviour.

## 8. Order of content work

1. **Filipino Verbal, about 112.** Antonyms 40, synonyms 26, idioms 22, paragraph order 14, reading 10. It's the largest gap, and KWF spelling and LanguageTool checks (Sentinel F9) help QA.
2. **Analytical, about 92.** Word analogy 61 across all relation types, and data interpretation 31 as text tables.
3. **Clerical filing, 41.** Business names, numeric, chronological and terminal-digit formats, ARMA rules 2 to 8.
4. **Numerical basic operations, about 33**, plus about 3 sequences and 2 non-percent word problems. No new percent-change items.
5. **GI applied, about 20.** R.A. 6713 and Constitution scenarios, quotes checked on LawPhil.
6. **English paragraph organization, 6 or more.** Varied option sets (CoS gap-fill-005 note).
7. **In parallel:** baseline audits B3 onward (about 399 items). Each one moves the "new needed" figure toward its low end or its high end.

ChatGPT's next prompt ([CHATGPT_NEXT_PROMPT.md](CHATGPT_NEXT_PROMPT.md)) should take its batch from the top of this list once GT approves the plan.

## 9. Questions for GT

1. Approve the split (Verbal 600, Numerical 400, Analytical 400, Clerical 300, GI 300), keep your example, or take the alternative in §4?
2. Approve the proposed GI topic mix (Constitution 120, R.A. 6713 90, Peace and HR 50, Environment 40) in place of the spec's 40/35/15/10?
3. Should full mocks draw from the collection first (§7.5)?
4. May the subcategory labels be normalized to the CSC subtopics? It's a data-only change with a backup first.
5. Should unaudited baseline items stay out of the collection until audited?
