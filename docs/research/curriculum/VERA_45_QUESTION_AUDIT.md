# Vera 45-question audit and reconciliation

Repository examined: `dbdf2bc04fe8d7edde4c8b7cf1e87be01138abe1`. Research date: 21 October 2026.

All **45/45** founder-supplied source IDs are accounted for. The source has 43 pictures according to the founder; the pictures themselves and Facebook publication URLs were unavailable. These are third-party practice examples, not authenticated CSC questions. This report publishes analytical summaries, not the transcribed stems or choices.

**Nine questions have no correct listed option under their intended interpretations:** 001, 002, 007, 014, 015, 021, 025, 040, 041. Item 040 also needs an explicit wrapping rule. The other 36 are not automatically approved: see wording and scope qualifications below. The two explicitly supplied source category errors are 041 and 043.

Categories after correction: 25 Numerical, 6 Analytical, 10 General Information (including two supplemental local-government topics), 3 English Verbal, 1 Clerical. Analytical placement describes the tested skill; a reading-inference adaptation of 004 could be shared verbal practice. Difficulty estimates are provisional.

The machine-readable [ledger](data/vera-45-ledger.json) contains every requested tracking field, exact candidate IDs, paths, digests, source limitations and pending action. A related item is not evidence that a whole competency has adequate depth. Baseline numeric IDs are historical export IDs, not confirmed current database IDs. `CURR-001` through `CURR-010` refer to the original draft batch documented in the production plan.

| ID | Verified answer | Competency | Candidate Civio IDs | Action / defect |
|---|---|---|---|---|
| VERA-001 | 4.8 days; no choice | combined work and relative efficiency | `CIVIO-NUM-WP-RATE-000011` | Missing correct option; assume equal job units, independent constant additive rates. |
| VERA-002 | 800 liters; no choice | fractional change of a whole | `200`, `497` | Missing correct option. |
| VERA-003 | B: 680 pesos | percentage discount | `CIVIO-NUM-WP-PCT-CHANGE-000030` | Sound key; basic one-step application. |
| VERA-004 | A within the stated premise | stated cause versus evidence for cause | `331` | Do not teach that before/after association alone proves causation. For reading practice, ask what the passage claims; for analytical practice, ask what evidence would strengthen causality. |
| VERA-005 | C: hardworking | synonym | `CIVIO-VEN-WORD-MEANING-000268` | Acceptable elementary vocabulary; context would improve discrimination. |
| VERA-006 | D: 24 days | direct proportional work | `198`, `269` | State four identical tasks done sequentially at the same constant rate. |
| VERA-007 | 195 pesos; no choice | multiply then add costs | `48`, `203` | Missing correct option. |
| VERA-008 | C: 200 km | distance at constant speed | `351`, `496` | Sound assuming constant speed. |
| VERA-009 | B: 320 pesos | percentage discount | `CIVIO-NUM-WP-PCT-CHANGE-000030` | Same competency as VERA-003 and 043; do not count three coverage gaps. |
| VERA-010 | C: 2 hours 45 minutes | elapsed clock time | `264` | Sound for same-day travel. |
| VERA-011 | C: 6 workers | staffing and inverse proportion | `CIVIO-NUM-WP-RATE-000011`, `494` | Assume identical daily output, equal hours and perfect divisibility of work. |
| VERA-012 | C: 17 under the intended +3 rule | arithmetic progression | `45`, `CIVIO-NUM-SEQ-DIFF-000002` | Use the simplest consistent rule; a finite sequence alone cannot logically determine every continuation. |
| VERA-013 | C: 140 pesos | cost then change | `203` | Sound. |
| VERA-014 | 1/2; no choice | elementary probability complement | No adequate direct match established | Missing correct option; equal selection chance assumed. Probability is not separately named in the retrieved CSC scope. |
| VERA-015 | 70 square meters; no choice | perimeter constraint to area | `206` | Missing correct option; distinguish area from perimeter. |
| VERA-016 | C: 26 | substitute into an expression | No adequate direct match established | Sound. |
| VERA-017 | C: 60 km/h | average speed | `197` | Sound; average speed uses total distance divided by total elapsed time. |
| VERA-018 | A: 28 | translate less than a multiple | `CIVIO-NUM-WP-ALGEBRA-000025` | Sound; explicit expression helps explanation. |
| VERA-019 | C: 3/15, equal to 1/5 | elementary probability sample space | No adequate direct match established | Unsimplified fraction is valid. Same scope caution as VERA-014. |
| VERA-020 | C: 96 square meters | rectangular area | `206` | Sound. |
| VERA-021 | 22; no choice | distributive linear equation | `CIVIO-NUM-WP-ALGEBRA-000025` | Missing correct option. |
| VERA-022 | C: 300 km | unit speed then distance | `351`, `496` | Sound; duplicates the competency of VERA-008, not an additional gap. |
| VERA-023 | C, with the joint-session qualification | congressional war power | `CIVIO-GI-DEADLINE-NUMBER-000805` | Key points to the correct body but choice omits a constitutionally material procedure. |
| VERA-024 | B: post hoc reasoning | causal inference | `331` | Sound as an assessment of the evidence offered; the conclusion could still happen to be true. |
| VERA-025 | 43.2; no choice | fractional equation | `CIVIO-GAP2-NUM-OPS-FRAC-DEC-0006` | Missing correct option; a noninteger answer is legitimate. |
| VERA-026 | C: 9% less, for a positive starting quantity | successive percentage changes | `CIVIO-NUM-WP-PCT-CHANGE-000001` | Specify a positive price or amount: zero remains zero; negative values complicate comparative wording. |
| VERA-027 | D: arbitrary | semantic grouping | `94`, `425` | Least-related judgments need context; not every use of neutral means impartial. |
| VERA-028 | B: provincial governor | local executive authority | No adequate direct match established | Replace administrative head with chief executive to avoid confusion with provincial administrator. LGU detail is not a separately named CSC topic. |
| VERA-029 | A: judge and verdict | producer and product | `CIVIO-ANA-ANALOGY-FUNCTION-000057` | Best available analogy; relationships simplify institutional processes. Professional analytical topic. |
| VERA-030 | C is the best offered option, but overbroad | CSC mandate | No adequate direct match established | Do not imply the CSC personally recruits or appoints every government employee. |
| VERA-031 | B: seven regular members | barangay council composition | No adequate direct match established | Distinguish seven regular kagawads from the whole council including its presiding punong barangay and SK chair. |
| VERA-032 | C: answerable for actions and decisions | public accountability | `CIVIO-GI-TERM-MATCH-001003` | Sound but recall-level; add a concrete reporting and correction scenario. |
| VERA-033 | C: adopt the appointment system | identify a recommendation | `CIVIO-ANA-CONCLUSION-000047` | Sound. Ordering items tagged ANA-CONCLUSION do not automatically cover argument conclusions. |
| VERA-034 | A if spaces ignored; D under word-by-word sorting | multiword surname convention | `CIVIO-GAP1-CLR-FILE-ORDER-0021` | No unique unconditional key without the filing convention. Neither convention is established here as an official CSC rule. |
| VERA-035 | B: right to due process | due process | `363` | Sound but nearly tautological; scenario-based application gives better evidence of understanding. |
| VERA-036 | B: waste disposal and drainage maintenance | urban drainage and waste | `CIVIO-GI-ENV-PRINCIPLE-060095` | Best offered practice; does not guarantee prevention of all flooding. |
| VERA-037 | C is the safest best choice in the given client setting | gifts connected to duties | `CIVIO-GI-TERM-MATCH-000405` | Bare gift wording overgeneralizes. Low cost alone does not establish an exception; specify a pending transaction and requested favor. |
| VERA-038 | A intended; not strictly entailed as worded | preserve the predicate in deduction | `CIVIO-ANA-SYLLOGISM-000755` | Repair the premise or conclusion so they use the same predicate; no causal assumption about early arrival. |
| VERA-039 | B: convincing, closest available | credible in context | `98` | Use credible testimony without an unnecessary article; believable is a sharper target than convincing. |
| VERA-040 | A after explicit alphabet wrapping; absent from choices | letter-position sequence | No adequate direct match established | Missing correct option under the intended rule and unspecified wrapping. No wrap means no letter at position 27. |
| VERA-041 | 4.5 days; no choice | fixed worker-days | `CIVIO-NUM-WP-RATE-000011`, `494` | Missing correct option and source category error; do not round to an offered choice. |
| VERA-042 | D: six years for one term | Senate term and tenure limit | `CIVIO-GI-DEADLINE-NUMBER-000106`, `CIVIO-GI-DEADLINE-NUMBER-000709` | Replace maximum length with duration of a regular term; avoid confusing 6 with 12 years. |
| VERA-043 | A: 23800 pesos | percentage discount | `CIVIO-NUM-WP-PCT-CHANGE-000030` | Source category error; otherwise sound. |
| VERA-044 | B: 8000 pesos | recover total from one ratio share | `CIVIO-NUM-WP-RATIO-000003` | Sound; distinguish known-share inversion from splitting a known total. |
| VERA-045 | C, limited to appointments requiring its consent | confirmation of specified appointments | No adequate direct match established | Not all presidential appointments require confirmation; distinguish JBC nominations and other appointments. |

## VERA-001: combined work and relative efficiency

**Verification:** 1/12+1.5/12=5/24 job/day; inverse=24/5. Check 4.8/12+1.5*4.8/12=1.

**Wording and difficulty:** Missing correct option; assume equal job units, independent constant additive rates. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-008; convert relative efficiency into a rate before adding. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-002: fractional change of a whole

**Verification:** 9/10-3/4=3/20; 120/(3/20)=800. Check 600+120=720.

**Wording and difficulty:** Missing correct option. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-003; infer a budget from a change in its spent fraction. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-003: percentage discount

**Verification:** 850*(1-20/100)=680; discount=170.

**Wording and difficulty:** Sound key; basic one-step application. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Link existing discount coverage after editorial review; no duplicate needed. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-004: stated cause versus evidence for cause

**Verification:** The premise explicitly attributes the reduction to the scheme. A restates that premise; other options add unsupported facts.

**Wording and difficulty:** Do not teach that before/after association alone proves causation. For reading practice, ask what the passage claims; for analytical practice, ask what evidence would strengthen causality. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Author a comparison-group causal-evidence item; distinguish from VERA-024. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-005: synonym

**Verification:** Diligent describes sustained careful effort; hardworking is the closest available meaning.

**Wording and difficulty:** Acceptable elementary vocabulary; context would improve discrimination. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Link existing diligent item; retain unseen vocabulary for transfer. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-006: direct proportional work

**Verification:** Four equal jobs at six days each require 4*6=24 days.

**Wording and difficulty:** State four identical tasks done sequentially at the same constant rate. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Use production units and a changed work quantity; current examples are partial rate coverage. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-007: multiply then add costs

**Verification:** 5*30+3*15=150+45=195.

**Wording and difficulty:** Missing correct option. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-004; evaluate a fixed fee plus a per-unit charge, not another notebook purchase. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-008: distance at constant speed

**Verification:** 120/3=40 km/h; 40*5=200.

**Wording and difficulty:** Sound assuming constant speed. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Link historical distance items only after identity and approval reconciliation. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-009: percentage discount

**Verification:** 400*0.8=320; check 80+320=400.

**Wording and difficulty:** Same competency as VERA-003 and 043; do not count three coverage gaps. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Reuse existing discount family; prioritize reverse percentage instead. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-010: elapsed clock time

**Verification:** 11:15 minus 08:30 = 165 minutes.

**Wording and difficulty:** Sound for same-day travel. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-006; cross noon explicitly, with hours-to-minutes checking. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-011: staffing and inverse proportion

**Verification:** 3*8=24 worker-days; 24/4=6.

**Wording and difficulty:** Assume identical daily output, equal hours and perfect divisibility of work. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-009; explicit staff-hours capacity rather than unsupported real-world scalability. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-012: arithmetic progression

**Verification:** Successive differences are 3; 14+3=17.

**Wording and difficulty:** Use the simplest consistent rule; a finite sequence alone cannot logically determine every continuation. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Link historical basic and current second-difference items; test rule explanation. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-013: cost then change

**Verification:** 500-8*45=500-360=140.

**Wording and difficulty:** Sound. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Add a distinct mixed-cost change task only after baseline reconciliation. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-014: elementary probability complement

**Verification:** Non-red count=3+2=5; total=10; probability=5/10.

**Wording and difficulty:** Missing correct option; equal selection chance assumed. Probability is not separately named in the retrieved CSC scope. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Hold as supporting/enrichment arithmetic pending scope decision; original unequal category complement task. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-015: perimeter constraint to area

**Verification:** 2(w+w+3)=34 gives w=7, length=10; area=70.

**Wording and difficulty:** Missing correct option; distinguish area from perimeter. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-010; derive area of a mat from edge length and a dimension difference. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-016: substitute into an expression

**Verification:** 2*3+4*5=6+20=26.

**Wording and difficulty:** Sound. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-004; substitution followed by order of operations. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-017: average speed

**Verification:** 120/2=60 km/h.

**Wording and difficulty:** Sound; average speed uses total distance divided by total elapsed time. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Link baseline; later add stops and unequal journey segments. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-018: translate less than a multiple

**Verification:** 3*12-8=28, not 3*(12-8).

**Wording and difficulty:** Sound; explicit expression helps explanation. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-004 is prerequisite only; add a fresh translation task without the implausible age context. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-019: elementary probability sample space

**Verification:** 3 blue out of 5+3+7=15; only C equals 1/5.

**Wording and difficulty:** Unsimplified fraction is valid. Same scope caution as VERA-014. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Scope hold with VERA-014; do not create two redundant introductory probability items. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-020: rectangular area

**Verification:** 12*8=96; square units required.

**Wording and difficulty:** Sound. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-010 is a harder application; add foundational area-versus-perimeter guided practice. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-021: distributive linear equation

**Verification:** 3x-12=2x+10 => x=22. Substitute: both sides=54.

**Wording and difficulty:** Missing correct option. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-005; direct distribution and collect-like-terms task. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-022: unit speed then distance

**Verification:** 120/2*5=300.

**Wording and difficulty:** Sound; duplicates the competency of VERA-008, not an additional gap. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Reconcile baseline IDs; no additional distance clone. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-023: congressional war power

**Verification:** Article VI Section 23(1): Congress alone; two-thirds of both Houses; assembled in joint session; voting separately.

**Wording and difficulty:** Key points to the correct body but choice omits a constitutionally material procedure. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Existing item states the full rule; legal reviewer confirms source and eligibility. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-024: causal inference

**Verification:** Temporal order alone does not establish cause; alternative explanations are not excluded.

**Wording and difficulty:** Sound as an assessment of the evidence offered; the conclusion could still happen to be true. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** One original controlled-comparison task with VERA-004; do not reproduce the police scenario. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-025: fractional equation

**Verification:** (2/3-1/4)x=18 => (5/12)x=18 => x=216/5. Check 28.8-10.8=18.

**Wording and difficulty:** Missing correct option; a noninteger answer is legitimate. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-003 applies a fractional difference; CURR-005 supplies equation prerequisites. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-026: successive percentage changes

**Verification:** 1.30*0.70=0.91; final amount is 91% of original.

**Wording and difficulty:** Specify a positive price or amount: zero remains zero; negative values complicate comparative wording. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Existing positive-price item is preferable; no redundant pair of changes. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-027: semantic grouping

**Verification:** Impartial, objective and neutral cluster around unbiased judgment; arbitrary lacks a consistent reason or principle.

**Wording and difficulty:** Least-related judgments need context; not every use of neutral means impartial. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Use a fresh sentence contrasting evidence-based and arbitrary decisions, not word-list memorization. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-028: local executive authority

**Verification:** R.A. 7160 Sections 465 and 41(a): governor is provincial chief executive and elected at large.

**Wording and difficulty:** Replace administrative head with chief executive to avoid confusion with provincial administrator. LGU detail is not a separately named CSC topic. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Retain source in ledger; hold an original LGU item pending curriculum-scope approval. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-029: producer and product

**Verification:** A legislator makes law; a judge renders a verdict. Other pairs describe workplace or participation.

**Wording and difficulty:** Best available analogy; relationships simplify institutional processes. Professional analytical topic. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Existing worker/workplace item is related but does not close producer/product coverage; review analogy pool before drafting. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-030: CSC mandate

**Verification:** Article IX-B Section 3 and CSC mandate identify a central personnel agency with career-service, merit and HR responsibilities.

**Wording and difficulty:** Do not imply the CSC personally recruits or appoints every government employee. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Prepare a source-based distinction between personnel standards and agency appointing authority. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-031: barangay council composition

**Verification:** R.A. 7160 Sections 387 and 390 specify seven regular sangguniang barangay members; population is irrelevant here.

**Wording and difficulty:** Distinguish seven regular kagawads from the whole council including its presiding punong barangay and SK chair. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Scope hold with VERA-028; avoid treating a whole-council count as seven. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-032: public accountability

**Verification:** Accountability involves being answerable; Article XI Section 1 and R.A. 6713 Section 2 support public accountability.

**Wording and difficulty:** Sound but recall-level; add a concrete reporting and correction scenario. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Related democracy-norm item is partial coverage; design an accountability application. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-033: identify a recommendation

**Verification:** The recommendation is supported by the offered queue and efficiency reasons.

**Wording and difficulty:** Sound. Ordering items tagged ANA-CONCLUSION do not automatically cover argument conclusions. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Author argument structure, not another ordering chain; inspect baseline verbal inferences first. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-034: multiword surname convention

**Verification:** Letter strings: delacruz < delapena < deleon < delrosario. With separate words, De la Cruz precedes De Leon, then Dela, then Del Rosario.

**Wording and difficulty:** No unique unconditional key without the filing convention. Neither convention is established here as an official CSC rule. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** State surname-first, letter-by-letter, ignore spaces/punctuation, treatment of accents; use wholly new names. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-035: due process

**Verification:** Article III Section 1 protects life, liberty and property against deprivation without due process.

**Wording and difficulty:** Sound but nearly tautological; scenario-based application gives better evidence of understanding. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Reconcile baseline legal item; create a notice-and-opportunity scenario only if coverage remains weak. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-036: urban drainage and waste

**Verification:** Keeping waste out of waterways and maintaining drainage reduces blockage-related flooding; DENR-NCR supports this mechanism.

**Wording and difficulty:** Best offered practice; does not guarantee prevention of all flooding. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Current flood-adaptation item is related, not identical; verify disposal coverage before adding. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-037: gifts connected to duties

**Verification:** Sections 3(c), 3(d), 7(d) distinguish prohibited official-connection gifts and statutory qualifications.

**Wording and difficulty:** Bare gift wording overgeneralizes. Low cost alone does not establish an exception; specify a pending transaction and requested favor. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Use the existing official-transaction scenario; retain exception nuance in explanation. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-038: preserve the predicate in deduction

**Verification:** A comparative more productive predicate does not by itself establish an absolute productive classification.

**Wording and difficulty:** Repair the premise or conclusion so they use the same predicate; no causal assumption about early arrival. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Use existing all-A/all-B chain; new variation only if it tests a distinct quantifier. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-039: credible in context

**Verification:** Credible primarily means believable or worthy of belief; convincing is closest among the choices.

**Wording and difficulty:** Use credible testimony without an unnecessary article; believable is a sharper target than convincing. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Reconcile baseline synonym; original evidence-reliability context if a new item is justified. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-040: letter-position sequence

**Verification:** Positions 2,5,9,14,20 have increments 3,4,5,6; next=27. In a cyclic alphabet 27 maps to A.

**Wording and difficulty:** Missing correct option under the intended rule and unspecified wrapping. No wrap means no letter at position 27. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Use a stated cyclic alphabet or keep all positions within 26; review existing symbol-series families. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-041: fixed worker-days

**Verification:** 3*12=36 worker-days; 36/8=4.5. Check 8*4.5=36.

**Wording and difficulty:** Missing correct option and source category error; do not round to an offered choice. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-009 covers staff-hours with explicit assumptions; same competency as VERA-011. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-042: Senate term and tenure limit

**Verification:** Article VI Section 4 distinguishes six-year terms from at most two consecutive terms.

**Wording and difficulty:** Replace maximum length with duration of a regular term; avoid confusing 6 with 12 years. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Link existing term and consecutive-limit items as a fact family, separated across mocks. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-043: percentage discount

**Verification:** 28000*0.85=23800; 10%=2800 and 5%=1400, so subtract4200.

**Wording and difficulty:** Source category error; otherwise sound. easy; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Same discount coverage as VERA-003 and 009; no new clone. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-044: recover total from one ratio share

**Verification:** Five parts=4000, one part=800, ten parts=8000.

**Wording and difficulty:** Sound; distinguish known-share inversion from splitting a known total. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** CURR-007 tests the missing unit-part step and a different requested subtotal. Independent editorial verification and GT approval required for any new or corrected bank item.

## VERA-045: confirmation of specified appointments

**Verification:** Article VI Section 18 and Article VII Section 16: Commission on Appointments consent applies to specified presidential appointments.

**Wording and difficulty:** Not all presidential appointments require confirmation; distinguish JBC nominations and other appointments. medium; editorial estimate, not empirical calibration

**Reconciliation and remaining action:** Prepare a source-based appointment-category item after legal review; a CA distractor elsewhere is not coverage. Independent editorial verification and GT approval required for any new or corrected bank item.

## Evidence and approval boundary

Constitutional and statutory checks use [S2-S5 in the source ledger](CSC_COMPETENCY_GAP_MAP.md#source-ledger); environment uses S6. Mathematical results were derived independently from the supplied facts, with exact rational arithmetic where needed. VERA-034 has been sorted under both stated conventions; the source does not establish which convention its author intended. No confidential examination material was used.

Existing approval labels are preserved as historical metadata. No item in this reconciliation is newly approved. A separate reviewer must examine drafts and corrections, followed by the current signed approval gate.
