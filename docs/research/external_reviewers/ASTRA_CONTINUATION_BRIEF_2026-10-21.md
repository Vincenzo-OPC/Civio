# Astra continuation brief — external reviewers (2026-10-21)

> Phase 1 research by Grok Bot, 21 Oct 2026 (Asia/Manila). Research only: nothing here is approved, imported or validated.

This is the entry point. Read this first, then the CSV.

## 1. What this is and isn't
- **Grok Bot did:** a full recursive inventory of the Drive folder, local MD5 hashing, automated text extraction and keyword scans of every file, and a short first-pages sample of 12 priority files.
- **Grok Bot did not:** solve, key-check or validate any question; compare items with Civio's bank; OCR the scanned books; or make any educational judgment beyond triage. Every count of "answer keys" or "explanations" in the CSV comes from a keyword heuristic, not a verified fact.
- **Astra's existing audit is not restarted.** It continues per `docs/research/AUDIT_TRACKER.md` and `docs/research/curriculum/`.

## 2. Files in this package
- `SOURCE_INVENTORY_2026-10-21.csv`: 99 rows, one per Drive file. Key columns: `drive_file_id`, `url`, `relative_path`, `md5`, `pages`, `subject`, `level_relevance`, `exact_dup_group`, `suspected_dup_group`, `rights_notes`, `reliability_notes`, `priority`, `examination_level`.
- `RESEARCH_OVERVIEW_2026-10-21.md`: totals and method.
- `SOURCE_RIGHTS_LEDGER_2026-10-21.md`: rights classes and the HOLD list.
- `DUPLICATE_AND_QUALITY_FLAGS_2026-10-21.md`: duplicate groups, observed defects and outdated items.
- `ASTRA_REVIEW_SHORTLIST_2026-10-21.md`: the ranked top 10.

## 3. Coverage status
- **Inventoried (all 99):** metadata plus an automated full-text scan.
- **Sampled (12):**
  - [Numerical Reasoning (255 Questions with Answers).pdf](https://drive.google.com/file/d/1cOD5t3qz_c46m2pLVmXLrYvqc_nnxmQb/view): first 3 pages read: stacked fractions split across lines; several items have choices separated from letters (a.-d. then values) - mapping needs visual check
  - [Numerical Reasoning - CSE Reviewer.pdf](https://drive.google.com/file/d/1HSY50sAVLF7ljG6hn3md04vlr69czkm-/view): page 3 rendered: scanned mock that reproduces CSC booklet layout (examinee questionnaire items 1-20, then TEST BEGINS); provenance unknown
  - [CSE Reviewer, P1 (1Taker).pdf](https://drive.google.com/file/d/1aBXEycGZBYzey2Y0Hf6yOaYZZyV2IcfA/view): first 3 pages read: blog-style tips + drills; mentions CAT
  - [CSE Reviewer Professional v.1.0.pdf](https://drive.google.com/file/d/18tHd15NF9GoPEgDTr2swbKBmZD0Q4_sY/view): first page read: same publisher as SubPro v1.0
  - [CSE Reviewer SubPro v.1.0.pdf](https://drive.google.com/file/d/1g9KL2b8brKKxEBbcHO_yl1KQs4acgbFN/view): first 3 pages read: CSEReviewer.com, full SubPro scope incl. Clerical; disclaimer says not affiliated with CSC
  - [CSE Reviewer.pdf](https://drive.google.com/file/d/1xhGzoodE-yuChDj8d8BjUwlrkt_Foyks/view): page 3 rendered: scanned mock that reproduces CSC booklet layout (examinee questionnaire items 1-20, then TEST BEGINS); provenance unknown
  - [180 Abstract and Spatial Reasoning Reviewer with tutorial videos (1).pdf](https://drive.google.com/file/d/1ZIKl80G5aM78jmF9z9bB5Gz0QYy4CnWc/view): first 3 pages read: figure-based; text layer has only headers; all items need visual inspection
  - [255 item Mathematics with detailed solutions (1).pdf](https://drive.google.com/file/d/1zYqN2ZNibf1si8egzhm8QiPYsbbt4Xdj/view): first 3 pages read: stacked fractions lost in text layer (e.g. "45 is of what number?" missing the fraction); one worked answer rounds 14.625 to "14" - verify visually
  - [Mathematics_300 items_Reviewer_with_detailed_solutions (1).pdf](https://drive.google.com/file/d/1l4gtd71_9fnQYhh82XvNquSiBZde7_yo/view): first 3 pages read: exponents flattened (10^2 extracted as "102"), signs/fractions need visual check
  - [4_ACE_Review_Center_Exam_Reviewer_Around_900_Items_With_Answers (1).pdf](https://drive.google.com/file/d/1i-bK31tp193BYlQ74pBU1SZogJirK6Km/view): page 3 rendered: scanned; 2007-2008 data tables/graphs; 5-option numbered choices
  - [FREE 250 MATH Problems with links for tutorial VIDEOS (1).pdf](https://drive.google.com/file/d/1N5Pe-G7fLSKqYhHvO5M0paMS_AQ0beb2/view): first 3 pages read: warm-up arithmetic then harder word problems; video links
  - [MSA Civil Service Exam Reviewer (1).pdf](https://drive.google.com/file/d/1R-BCo-SFxiBEW11o_WGUtaBoephSoYUy/view): page 3 rendered: scanned commercial book "MSA Civil Service Reviewer, New Millennium Edition, MSA Math Tutoring Center"
  - [Civil Service Exam Reviewer 2021 - Pinoy Einstein (1).pdf](https://drive.google.com/file/d/1FsvsHsIjRtXs242822A1gSnjAx7NTmfM/view): first 3 pages read: lesson-style Verbal notes + quizzes; 312 pp, ~101 answer-key markers; best explanation-style source
- **Unexamined in substance:** everything else, including all item-level content in every file.
- **Needs human or visual verification:** every math, abstract or data-interpretation item; all 8 scanned files; the provenance of `CSE Reviewer.pdf`; and every HOLD file's recall claim.

## 4. How to compare with Civio's bank (suggested)
1. Use only the de-duplicated set: one file per `exact_dup_group`, and prefer the copy in `12. COMPILATIONS` or `1. CSE Masterclass`.
2. Extract a **competency list, not items**, from each shortlisted file (e.g. "fraction of a number, reverse form", "work-rate with 3 workers", "ARMA business-name filing"). Map each one to the rows of `CSC_COMPETENCY_GAP_MAP.md` and the counts in `CURRENT_BANK_ASSESSMENT.md`.
3. Record gaps as `competency → external evidence (file id + page) → Civio count`. Civio then writes original items through the normal spec v0.1.9 / Chief of Staff (CoS) / GT pipeline, and they stay draft until CoS reviews them.
4. Benchmark difficulty by timing a few external items yourself, not by copying them.
5. Never place any external-derived content in reserved unseen mocks.

## 5. Integrity rules (must keep)
- No verbatim or near-verbatim stems, options, number sets or passages from any file. HOLD files stay study-only.
- Never trust external answer keys. Re-solve independently, and cite primary sources for GI (lawphil / Official Gazette / csc.gov.ph).
- Public Drive access, or "FREE / NOT FOR SALE", is not a licence.
- Civio isn't official CSC and must never imply it.
- Don't add bank records, activate anything or change approval statuses.

## 6. Suggested next steps for Astra (in order)
1. Numerical gap pass: use FREE 250 MATH, Masterclass Numerical 255, Math Reviewer and Age Problems, plus the method notes from the 255/300 HOLD files. Map them to fractions, percent, ratio, algebra and word problems. Read the page images, not the text layer.
2. Clerical gap: confirm that this folder has no filing-rules source, and use ARMA/official rules instead.
3. Verbal: study Pinoy Einstein's explanation patterns for the Dexter tutor's explanations.
4. OCR the ACE and MSA scans only if difficulty benchmarking needs them, and keep the output off GitHub.
5. Ask GT whether to request permission from Leonalyn Mutia-Tayone or PinoyEinstein to *link* their free videos.

## 7. Resume checkpoint
- Inventory: **complete**, 26/26 folders and 99/99 files, as of 2026-10-21 ~23:00 Asia/Manila. Drive folder last-modified dates were 10/16/24, so the folder looks static.
- To re-verify: re-walk `https://drive.google.com/embeddedfolderview?id=1ZiU50XySwmTd-fh6fOg2wcN-BTtBpDMg`, then compare file ids and MD5s with the CSV. Any new id is unprocessed.
- Nothing is pending from Phase 1. Phase 2 (educational review) hasn't started.
