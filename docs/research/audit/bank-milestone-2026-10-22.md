# Bank milestone — 2026-10-22 (CONTINUE directive, BANK section)

Recounted from source files via `scripts/batches/audit/master_audit_2026_10_22.py` and `scripts/batches/qa/validate_flat_2100_manifest.py`.

| Tier | Count |
|---|---|
| Manifest rows (raw) | 2,100 |
| Unique (id + content) | 2,100 |
| Mechanically QA-valid (audit 0 unresolved issues) | 2,100 |
| Content-reviewed (status reviewed) | 42 |
| Approved (by GT, unchanged) | 1,377 |
| Active | 0 changed by this worker (no activation) |

Domains: Numerical 400, Analytical 400 (all professional), Verbal EN 400, Verbal FIL 300, Clerical 300 (all subprofessional), GI 300.

Replaced in manifest this cycle: 268 (231 weak/no explanation, 23 GI template padding, 9 numeric/analytical twins, 5 disputed ARMA filing variants).
New draft files (489 items): analytical-professional 127, gi-applied 90, numerical-series 13, subpro-clerical 50, subpro-filipino 50, subpro-math 60, verbal-en-organization-reading 99. Draft review queue: 489/489 pass.

Audit now also enforces: Analytical professional-only, Clerical subprofessional-only, difficulty/est_seconds present, why_correct + 3 why_wrong on every row. Two syllogism near-dup pairs (945/247, 956/253) were hand-checked and recorded as distinct (different premises/conclusions).

Pending human review: 723 non-approved rows (681 draft + 42 reviewed). Nothing self-approved.

## Update — 2026-10-22 afternoon

- **Legacy rows now checked inside `qa.check_item`** (`qa.legacy_errors`): GI rows must match a verbatim lawphil quote
  (`audit/gi_legacy_evidence_2026_10_22.py`, 90 hand-located quotes; `audit/verified_keys_2026_10_22.py`; or the row's own
  `source_quote`), numerical/verbal_en rows must match a hand-checked key (`audit/legacy_keys_2026_10_22.py`, 109 rows re-solved).
  The lawphil texts are committed under `docs/research/sources/lawphil/` so QA no longer depends on a box-local cache.
  217 of 217 legacy rows in the manifest pass.
- **Replaced 2** legacy GI drafts that could not be verified (no statute cited; placeholder "TO BE QUOTED" quote) with gi-applied drafts.
- **Deeper content QA on the 489 new drafts:** every math key re-solved by hand (73), all 7 syllogisms and 12 ordering/conditional
  items checked for validity, all 90 GI quotes found in the lawphil text, all 72 analogies read for a single same-order relation.
  Fixed: 1 analogy with no clean relation (seed : orchard, rebuilt), 1 analogy distractor that shared the stem relation (judge : court),
  1 table title (three vs four precincts), 1 GI key reworded to match its quote, 1 GI quote replaced with the clause that supports the key,
  decimal distractors on 6 whole-count word problems replaced with integer misconceptions.
- **Review packets:** 723 non-approved rows in 28 independent packets (`docs/research/review/packets-2026-10-22/`):
  P1 42, P2 84, P3 258, P4 339. Key and explanation sit in a separate answer sheet; decisions go in `decisions.csv`.

## Late-afternoon update (22 Oct 2026, after 2:55 PM directive)

- **Verbal EN:** 12 new original passages (158–185 words), 4 questions each = 48 drafts (`verbal-en-reading-set2-2026-10-22.json`) covering main idea, detail, inference, vocabulary in context, author's purpose and relation between parts. The 7 short-passage drafts (CIVIO-GF2K05-RCD-0001/0002, RCI-0001/0002, RCM-0001/0002, RCV-0001) were swapped out for RC2 items; 41 RC2 items stay as spares.
- **Clerical:** 40 Subpro-only spare drafts (`subpro-clerical-set2-2026-10-22.json`): 12 spelling, 12 alphabetic filing (ARMA Rules 1, 2, 8), 6 chronological, 4 numeric filing (Rule 7), 6 copy-check. Spec proposals pending CoS: archetypes CLR-CHRONOLOGICAL and CLR-COPY-CHECK, distractor code CLR-COPY-MISMATCH.
- **Numerical method-first:** `reveal.method_steps` (asked, givens, method, why, solve by hand, check, distractors, shortcut) added in place to all 76 non-D1022 numerical draft rows (the 25 D1022 drafts already had them). Hashes refreshed by the swap script, now for every draft row. 59 approved rows got -R1 proposals only (`audit/fixes/method-first-r1-proposals-2026-10-22.json`, content and key unchanged, not in the manifest). Not yet covered: 42 reviewed rows (batch-subpro-num-001) and about 240 other approved rows (no template yet).
- **Flags for review:** signoff-replacements-2026-10-22 has template padding (5 near-identical rectangle-edging items, 3 near-identical chair-discount items), and gap-fill-2000-02 has 20 templated order-of-operations items. These are drafts only.
- **Manifest:** 2,100 (Num 400, Ana 400, VEN 400, VFIL 300, CLR 300, GI 300); percent-change rows 40/40; validator 0 problems; master audit Counter().

## GT directive 3 update (22 Oct 2026, 3:30 PM)

See `AUDIT_TRACKER.md` ("GT directive 3, BANK"). The 150-word passage gate is enforced in `qa.check_item`. 4 P1 editorial -R1 drafts took their originals' slots. 24 templated Numerical drafts were swapped for distinct spares. Method-first -R1 proposals now cover all 295 approved and reviewed Numerical rows. The 42 P1 recommendations are written. Manifest: 2,100 (approved 1,377, draft 685, reviewed 38); percent-change rows 38/40.

**Spec proposals for GT:** CLR-CHRONOLOGICAL, CLR-COPY-CHECK, CLR-COPY-MISMATCH (proposals), and whether VFIL-PAGBASA passages need a word floor (38 Filipino passage items are 32–54 words).

## GT decisions 15:48: Filipino passage levels, Numerical template audit, queue (2026-10-22, 4:40 PM)

- **Filipino passage gate (qa.py):** two levels. SHORT is 80-149 words, LONG is 150-250. A passage under 80 or over 250 fails. When an item sets `passage_level`, the word count must match that level.
  - Detection covers VFIL-PAGBASA and VFIL-READ, plus the instruction lines "Basahin ang talata", "Basahin at unawain", "Suriin ang talata" and "Talata:". The instruction line is not counted.
  - English stays at a 150-word minimum.
  - 5 new Filipino-gate tests plus 1 Numerical-replacement test in `test_bank_gates_2026_10_22.py` (15 tests in total).
- **Short Filipino passages: 47 items, not 38.** The earlier detector only knew the "Basahin ang talata" instruction, so it found 35 approved items and 3 drafts (38). With every instruction variant it finds 47, all under 80 words (36-55): 35 approved and 12 drafts.
  - **12 drafts (CIVIO-GF2K02-PAGBASA-0001 to 0012):** passages lengthened in place to 80-98 words and marked `passage_level: short`, with a revision_history entry each. Manifest hashes refreshed.
  - **35 approved (VFIL-PAGBASA-040076 to 040090, VFIL-20261013-0055 to 0074):** left unchanged. Each has a -R1 proposal in `audit/fixes/vfil-passage-r1-2026-10-22.json`. The 20 VFIL-READ rows share 5 passages. Proposals are status draft with reviewer null and are not in the manifest.
  - The master audit lists these 35 under `flagged_pending_authorized_review` (not as unhandled defects).
  - **How the passages were lengthened:** each one got neutral background sentences (`drafts/fil_passages_2026_10_22.py`). The question, options, key and explanations are unchanged. Each addition was read against every option, so a wrong option did not become supported and a "hindi binanggit" answer did not become mentioned. A human should still read the new sentences.
- **Approved Numerical template audit:** `audit/num-template-audit-2026-10-22.md` and `.json`, built by `qa/num_template_audit_2026_10_22.py`.
  - **Test used:** same archetype, identical stem numbers and the same key, with wording that differs only in names or the task noun.
  - **Result:** 14 groups (ratio-share, work-together and age items) and 21 repeats. The first item of each group is kept. Each repeat has one replacement draft (`<id>-TR1`) with new numbers, a verified recipe (solver) and method_steps, in `audit/fixes/num-template-replacements-2026-10-22.json`.
  - None of the drafts are swapped in, and no approved item was edited, retired or removed.
  - 47 same-frame groups with different numbers are listed for information only, with no replacement (GT rule: sharing a method is not repetition).
- **Queue (723 rows):** the CSV has a new `needs_human_read` column. It is "yes" for all 139 self-authored D1022 judgment items and for every other row a human still has to read (317 in total). The 12 former Escalate rows are now "Accept revision" (passage lengthened). Totals: 707 Accept, 16 Accept revision (4 P1 plus 12 Filipino), 0 Escalate. Recommendations only; `decision_by_human` is empty.
- **QA fix:** a solver crash in `qa.py` on stems outside the solver's frames (batch-subpro-num-001) now records "solver could not recompute the key" instead of crashing.

## Adversarial read of D1022 judgment items and distractor-lengthened rows; old qa_file problems (2026-10-22, 5:10 PM)

- **Scope:** the 139 D1022 judgment items (106 Verbal EN, 33 Analytical) and the 23 distractor-lengthened GI rows. I am their author, so this is not an independent check and `needs_human_read` stays "yes".
- **What each item was attacked for:** a second defensible answer, a key the passage doesn't support, a faulty analogy relation, an invalid inference, a grammar error and a weak or giveaway distractor.
  - Every added sentence (INSERT items) was tried in every slot.
  - Every option order (ORDER items) was read as a paragraph.
  - Every lengthened GI wrong option was checked against the constitutional text.
- **Where it is recorded:** each of the 162 rows has an `adversarial_read` record in `review/queue-evidence-2026-10-22.json` (attacks tried, result, finding, action), from `qa/adversarial_read_2026_10_22.py`.
- **Defects found and repaired in the drafts (5):** fixed in the generators (`drafts/d22_analogy.py`, `drafts/en_text_2026_10_22.py`); count still 2,100.
  - **ANA-0038 (soldier : battalion):** "general : army" was a second member-to-group answer. That option is now "army : navy".
  - **ANA-0029 (tepid : scalding):** "cold : hot" could be argued as a lower-to-higher degree. That option is now "heat : thermometer".
  - **VEN-INS-0008:** "Those children often had to walk" contradicted "missed classes". It now reads "Others had to walk ... instead."
  - **VEN-INS-0012:** the health-certificate sentence fit after sentence 2 or sentence 3. The paragraph was rebuilt so the added sentence "These fees pay for ..." fits only after the fee sentence.
  - **VEN-INS-0015:** the class-size sentence fit after sentence 1 or sentence 2. It is now "That is enough time, because each class has only fifteen learners.", which needs sentence 2.
- **No defect found:** the other 134 judgment items and all 23 GI rows. 4 paragraph-order items (PO-0002, PO-0013, PO-0018, PO-0025) have a readable second order that is clearly weaker; they carry watch notes.
- **Old qa_file problems fixed:**
  - **fact_id format:** the 50 `num-original-9260NN` fact_ids in batch-subpro-num-001 (and the 4 P1 -R1s that copy them) are now `FACT-NUM-ORIGINAL-9260NN`.
  - **gap-fill-2000-02 "near-duplicate" (NUMOPS-0050 vs ORDER-000240):** a false positive. Word overlap matched two bare expressions that differ (69 × (19 − 2) + 11 vs 19 × 2 − 10 ÷ 2). The near-duplicate check now treats bare arithmetic stems with different expressions as distinct. The item is outside the manifest and carries a GT-approved revision, so its content was not touched.
  - **"reviewed" status:** qa.py now accepts it as valid, as the master audit already did.
  - **Solver false positive:** the discount solver no longer misreads an offer-comparison stem (926024: correct key ₱30).
  - **Revisions:** qa_file no longer flags an -R1 as a duplicate of the original it replaces.
  - **Key sheet:** qa_file now accepts keys verified by the hand-checked key sheet. The 7 off-manifest percent-change rows were re-solved and added to it.
  - **Result:** qa_file reports 0 problems for batch-subpro-num-001, gap-fill-2000-02, the P1 -R1 file and both D1022 files.
- **Still reported by qa_file (not in this scope; master audit is clean):**
  - gap-fill-2000-05: the 7 short English originals, which GT replaced and which are outside the manifest.
  - round-03 b3/b4: 6 legacy rows without a key sheet or lawphil evidence.
  - signoff-replacements: 29 percent-change R1s near-duplicate their originals by design.
  - gap-fill-2000-06-lintfix: 398 legacy findings, many on rows outside the manifest.
- **Queue:** 707 Accept, 16 Accept revision, 0 Escalate before this read. The 5 repaired items moved from Accept to Accept revision, so it is now 702 Accept and 21 Accept revision. 317 rows have needs_human_read = yes. `decision_by_human` is empty.
- **Tests:** 16 bank-gate tests. New: adversarial-read records exist for exactly 139 + 23 rows, all with needs_human_read = yes, and the 4 repairs checked by the test are present in the drafts.

## GT independent review follow-up: ambiguous items, approval-claim notes, approval packets (2026-10-22, 4:45 PM)

- **Items revised again; all 5 are recommended "Revise" until a reviewer confirms each one now has a single answer:**
  - **VEN-INS-0015:** sentence 3 is now "On the first Saturday, learners set up their own email accounts." The added sentence is "On the last Saturday, they fill out a sample online job application." It must follow sentence 3 and come before "these skills" in sentence 4.
  - **VEN-PO-0002:** S now needs "those cards" from R.
  - **VEN-PO-0013:** P now needs "these topics" from S.
  - **VEN-PO-0018:** P now needs the fare check in R ("easy to spot").
  - **VEN-PO-0025:** P now needs "the refrigerator" named in R.
  - In each ordering item, the wrong option that was also coherent is now broken. The changes are in `drafts/en_text_2026_10_22.py` and recorded in `qa/adversarial_read_2026_10_22.py` (GT_REVISE). The count stays 2,100.
- **"GT approved" notes:** the 22 Oct draft builders wrote "New original draft, 22 Oct 2026 (GT approved)". It now reads "New original draft, 22 Oct 2026. Design approach approved by GT; item not yet reviewed".
  - **Scope:** 529 draft records in 8 files. 226 are in the two files GT counted (analytical-professional 127, verbal-en-organization-reading 99). The rest: GI 90, subpro-math 60, subpro-clerical 50, subpro-filipino 50, subpro-clerical-set2 40, numerical-series 13.
  - The 295 method-first proposal notes "(approved)" now read "(original status: approved)".
  - No status was changed.
- **New QA gate:** `qa.approval_claim_errors` runs in `check_item` and fails any non-approved row that does one of these:
  - carries approved_by, approved_at, signed_by, signed_at or signoff;
  - is a draft with review_status passed or approved;
  - says "GT/CoS approved" or "approved by GT/CoS" in its notes, provenance or review notes.
  - **Allowed:** "Design approach approved by GT", `revisions[].approved_by` (GT approved that specific edit, not the item), and status "reviewed" with review_status "passed".
  - **Tests:** a unit test of the gate, and a check that no manifest row claims approval it doesn't have. A scan of every research JSON file finds no remaining claims.
- **Approval packets:** `review/approval-packets-2026-10-22/`, built by `qa/approval_packets_2026_10_22.py`. They replace the P1-P4 packets; `packets-2026-10-22/` keeps `decisions.csv` and the independent AI review.
  - 23 packets cover all 723 pending rows. Each packet holds one domain and one evidence type: solver-verified, law-text-verified or human-judgment-needed. Sizes are 29-36, except one packet of the 8 Verbal EN grammar items that a solver checked.
  - Packets are ordered by item risk, highest first: Revise, then revision, then not machine-checkable, then self-authored, then flags, then legal content.
  - Each packet opens with a one-page summary: what the evidence proves, what it does NOT show, the risk counts, numbered checks for that domain and evidence type, and the items to look at hardest.
  - Items are listed without keys. The answer sheet with keys, evidence and risk notes comes at the end, so the reviewer solves first.
  - A decision needs a reason for each item; a whole-packet stamp is not accepted.
- **Queue:** 698 Accept, 20 Accept revision, 5 Revise; 317 rows need a human read. `decision_by_human` is empty.
- **Tests:** 19 bank-gate tests, all passing.
