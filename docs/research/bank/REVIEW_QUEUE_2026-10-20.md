# Question-bank evidence and review queue - 20 October 2026

This packet records engineering investigation and mechanical checks. It approves no questions and makes no live-bank count or reliability claim.

## Reproducible evidence

[source-lock-2026-10-20.json](source-lock-2026-10-20.json) pins main at `06f3d23` and open PRs #3-12 to exact commits. GitHub PRs #1-16 were checked and remained OPEN/unmerged on 20 October. No branch was merged. Source paths and byte digests are preserved in [mechanical-review-2026-10-20.json](mechanical-review-2026-10-20.json).

```sh
# Fetch the commit SHAs listed in the source lock from origin if absent.
python scripts/batches/audit/inventory.py --lock docs/research/bank/source-lock-2026-10-20.json --out /tmp/civio-bank-inventory.json
python scripts/batches/audit/test_inventory.py
python scripts/batches/qa_all.py --no-fixes
```

The inventory reads Git objects, including historical exports, proposed fixes and unmerged drafts. It never imports, chooses a winning revision or interprets an embedded approval label as authorization. Its snapshot-local identities for numeric legacy IDs are deliberately provisional. A fingerprint mapping from a fresh sanitized runtime export remains necessary before any runtime reconciliation.

| Measure | Result | Meaning |
| --- | ---: | --- |
| Artifacts | 143 | Pinned main files plus changed bank/review/tool artifacts in the ten PRs |
| Item occurrences | 4,276 | Repeated versions and historical snapshots included; not bank size |
| Identity groups | 3,705 | Includes deliberately separate snapshot identities and unmapped replacements |
| Groups with differing content versions | 294 | A reconciliation queue, not 294 proven defects |
| Generic/placeholder explanation flags | 592 occurrences | A heuristic across versions, not a live-item count |
| Identity-mapping flags | 1,673 occurrences | Not safe to address by snapshot database ID |
| Duplicate-option flags | 2 occurrences | Both refer to baseline #462 in two historical representations |

The full generated inventory is reproducible from the lock; its large occurrence/conflict lists stay in the task artifact rather than duplicating bank content in Git. The checked-in mechanical report preserves per-artifact hashes, declarations and coverage.

## Existing work to reconcile

| PR | Inspected work | Decision boundary |
| --- | --- | --- |
| #3 | fact_id/theme schema and import groundwork | Reconcile with current importer protections; passage grouping and all selection paths still need engineering |
| #4 | B3 audit, 44 replacement drafts | Proposed verdicts and drafts await independent review/GT; do not apply the CSV as retirement authority |
| #5 | B4 numerical audit, 5 replacement drafts | Retain numerical recomputation evidence; review explanations and editorial verdicts separately |
| #6 | 550-row schema conversion | Historical migration aid; conversion does not approve the baseline or update live status |
| #7-10 | Gap-fill draft batches of 99, 108, 101 and 83 occurrences | Audit unique tasks and coverage before commissioning more items |
| #11 | 15 new drafts and 117 English lint-fix proposals | Reconcile fix_of targets and changed options/keys, not just lint scores |
| #12 | 247 non-English lint fixes plus 7 passage companions | Review five passage sets together; accepting one companion cannot silently mix passage versions |

PR #12 also repeats the 99-item #7 draft artifact; adding PR file counts would double-count it. The old integration merge-order packet is historical and includes superseded app implementations. Its union-merge suggestion for audit logs cannot settle contradictory verdicts. Current security code is stronger evidence for the shipped security boundary.

## QA coverage actually established

Existing `qa_all.py --no-fixes` passed its checks over 1,000 main batch occurrences, comparing 647 baseline stems, with zero reported exact/near baseline hits. **GI quotations were skipped because the official-text cache was absent.** Its GREEN output does not certify law, factual accuracy or all bank files.

The existing PR #12 explanation linter was inspected and reused directly at commit `7220b8a`; its SHA and per-artifact results are in the mechanical report. It processed the eligible spec-schema occurrences in 36 artifacts with zero tool errors. Legacy rows without answer_option_id were outside its coverage. Its length, answer-mention and citation-pattern heuristics are review flags; adding an answer line or citation string cannot prove an explanation is valid. No legal-source fetching or independent mathematical review was performed by this run.

`qa_file.py`, `qa_fixfile.py` and `release_manifest.py` were inspected before introducing new tooling. The new inventory provides provenance/conflict reporting, which those checks do not provide. Their existing solver/source-cache exclusions remain relevant. No whole-bank duplicate/correctness certificate is issued here.

The release selector is unsuitable as a release approval gate as written: it trusts embedded approved/passed labels, includes active converted baseline candidates without completed editorial approval, excludes some candidates on proposed REJECT verdicts, and `--include-drafts` can reach the target with unapproved content. Its hard-coded subject/subtopic quotas and heuristic category mappings are proposals. Preserve it as evidence/projection until policy, provenance and versioned membership are approved; do not activate its output.

## Independent review and GT queue

1. Reconcile the latest per-item verdicts against exact content digests. Preserve #277/#282/#287's later corrected outcomes; do not reopen their old audit defects. Confirm #312's later Sergeant/Questionnaire conflict against the latest independent verdict before proposing any edit.
2. Resolve baseline #462's documented duplicate options using independently reviewed original content. Its current live status is NOT VERIFIED. Do not retire or rewrite it merely from an old row number.
3. Review B3 HOLDs: #224 classification/source, #86 source evidence and #181/#265/#489 proposed percent-policy treatment. The percent cap is not approved policy. B3's source_quote placeholders require actual source evidence before approval.
4. Independently review PR #12's seven decision groups: whole passage sets, citation correction, qualifier wording, duplicate baseline facts, proposed vocabulary replacement, filing-solver wording mismatch, and rebased series/record stems. Generator assertions and the author's reported checks do not substitute for independent review. No authored fixes are created here.
5. Obtain a fresh sanitized runtime export through an approved process. Match stable identities and reviewed fingerprints; engineering does not query the live study database.
6. After these reviews, present a versioned candidate collection with exact item revision/content digests, inclusion/exclusion reasons and measured coverage gaps. GT then confirms or revises the proposed 300/300/400/400/300/300 split. Do not pad, relabel approved data, automatically retire surplus or activate a collection to hit 2,000.
7. Only then commission bounded original drafts for verified gaps, with separate author, independent reviewer and GT approval. Keep corrections and proposals separate from approved sources. Future mock selection must take whole eligible passage sets consecutively or skip them, one item per non-null fact_id and at most two first-measure-misleads items across every selection path.

## Delivered and remaining

Delivered engineering: fail-closed replacement/general import boundaries, independent signed approval contract, immutable identity ledger, signed promotion of unchanged tracked drafts, transactional cache behavior, tests and a reproducible provenance inventory.

Partial: artifact reconciliation and mechanical QA. The 294 conflict groups still need explicit editorial reconciliation; the inventory intentionally makes no automatic winning-version choice. Unresolved independent review, GT approvals, trusted-key provisioning and sanitized runtime reconciliation block content release. Complete question revision history, an approved collection schema/selector and a new editorial authoring program are not shipped.

Next bounded bank slice: independently reconcile one review packet (start with the baseline #462 evidence and B3 HOLD/source gaps), then prepare exact digest-bound decisions for GT. The broader product backlog still contains fabricated-readiness removal, Review Mistakes, mock grouping and exposure balancing.

Paper practice remains an assessment in [PAPER_PRACTICE_ASSESSMENT.md](../../PAPER_PRACTICE_ASSESSMENT.md): future booklets need immutable question/option/key versions, a persistent reference and errata handling; paper results cannot establish Strict Mock timing or independence. No paper flow or Complete Reviewer was built.
