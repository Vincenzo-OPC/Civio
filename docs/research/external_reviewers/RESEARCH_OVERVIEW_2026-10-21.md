# External CSE reviewer research overview (2026-10-21)

> Phase 1 research inventory by Grok Bot, 21 Oct 2026 (Asia/Manila). Research only: nothing here is approved for Civio, no question text is copied, and nothing was imported into the bank. Question approval stays with Astra, Chief of Staff and GT.

Source folder: [CIVIL SERVICE REVIEWERS](https://drive.google.com/drive/folders/1ZiU50XySwmTd-fh6fOg2wcN-BTtBpDMg) (`1ZiU50XySwmTd-fh6fOg2wcN-BTtBpDMg`).

## Method
- The Google Drive connector returned "operation not supported" for folder listing and metadata on this folder, so the tree was walked through Drive's public `embeddedfolderview` page, recursively, and each file was downloaded read-only from the public link to a scratch box. No Drive file was modified, moved, shared or deleted.
- Per file: MD5 computed locally (Drive `md5Checksum` was not available through the connector), byte size, `pdfinfo` page count and PDF metadata, full `pdftotext` extraction (first 400 pages), and keyword scans for answer keys, explanations, links, rights text and recall claims.
- 12 priority files were sampled by a person-style read of their first pages (text or rendered image). Nothing was validated end to end.

## Totals
- Folders examined: **26** (root + 25 subfolders, up to 4 levels deep). No folder failed to list.
- Files discovered: **99** (98 PDF, 1 DOCX). Accessible: **99**. Inaccessible: **0** (one file returned HTTP 503 on the first try and downloaded on retry).
- Unique binaries (by MD5): **80**. So 19 files are byte-identical copies.
- Text-extractable: 90; image-only/scanned (no text layer): 9.
- Total size: 170 MB.

## By subject (file count, duplicates included)
- Mixed full reviewer/mock: 46
- General Information/Legal: 16
- Verbal (English): 10
- Numerical: 9
- Current events (GI, dated): 8
- Forms/Printables: 6
- Analytical/Abstract: 3
- Exam info/tips: 1

## By priority
- MEDIUM: 64
- LOW: 18
- HOLD: 9
- HIGH: 8

## By year in filename (content year otherwise UNKNOWN)
- 2011: 1
- 2013: 2
- 2016: 1
- 2017: 1
- 2018: 3
- 2019: 2
- 2020: 5
- 2021: 2
- 2022: 3
- UNKNOWN: 79

## Key sources
- **Leonalyn Mutia-Tayone** math set (255, 300 and 250 items, 180 abstract/spatial, 2019/2020 complete reviewers): detailed worked solutions and YouTube links. Strongest numerical teaching material, but her own preface says some items come from "previous CSE exams (shared by those who took the exam)". So item reuse is on **HOLD**; use them only to study teaching methods.
- **Pinoy Einstein 2021** (312 pp): lesson-plus-quiz format with answer keys. Best explanation-style Verbal source. "Not for sale / free reviewer" text only, and no reuse licence.
- **CSEReviewer.com SubPro / Professional v1.0** (Joel Conrado Dancalan): covers the full SubPro scope, including Clerical. Its disclaimer cites remembered past-exam questions, so it is **HOLD**.
- **Masterclass Numerical Reasoning (255 Q)** and **Math Reviewer for CSE**: plain item drills with keys. Fraction layout is broken in the text layer.
- **ACE Review Center (~900 items)** and **MSA Civil Service Reviewer**: scanned commercial books. They are image-only and copyrighted. Useful for format and difficulty benchmarks only.

## Access limitations
- 8 files are image-only and need OCR or visual reading: both ACE copies, all three MSA copies, `CSE Reviewer.pdf`, `CSC_MC_No_11 s1996`, and `Sample Answer Sheet` (2 copies).
- Equations, stacked fractions, exponents, figures and tables are unreliable in every math or abstract PDF's text layer.

## Major reliability concerns
1. Recall-sourced items: 9 files are HOLD (see the shortlist and flags).
2. Outdated content: current events 2013-2022, the 19th Congress senators, a 2022 directory, 2008 data in ACE, and "CAT" exam naming.
3. Heavy duplication: one 2018 reviewer appears 3 times, and the Masterclass "PDF" folder repeats the 5-Part drill.
4. Commercial copyrighted works: Ed Swick verb drills, the Oxford thesaurus, the logic book, "Basic Synonyms", MSA and ACE.

## Preliminary recommendations
- Don't import anything. Use these files to (a) benchmark difficulty and formats, (b) find competency gaps against `docs/research/curriculum/CSC_COMPETENCY_GAP_MAP.md`, and (c) study explanation techniques. Then write original Civio items.
- For legal and GI facts, cite primary sources (lawphil / Official Gazette), not these PDFs.
