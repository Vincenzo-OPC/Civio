# BetterGov Philippine Quiz: CSE relevance assessment

Date: 18 October 2026 (Asia/Manila)  
Status: **Research only. No items approved, imported, or deployed.**  
Reviewer: ChatGPT initial screening. Per-item audit **pending access to full questions**.

## Public evidence checked

- BetterGov quiz: https://quiz.bettergov.ph/ — the landing page advertises a 24-question random test and four categories with 24 questions each: History, Culture & Traditions, Government & Politics, and Geography. This does **not** establish there are 96 unique, non-overlapping stems.
- BetterGov project listing: https://about.bettergov.ph/projects/ identifies the Philippine Quiz as a community/learning project.
- Official CSC CSE-PPT 2026 announcement, section F: https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf
- Civio canonical requirements: docs/CSE-Question-Design-Spec.md (currently v0.1.9); docs/HANDOFF_ANY_AI.md; docs/research/AUDIT_TRACKER.md; AGENTS.md.

## Category screening (not an item audit)

| Quiz category | CSE relevance | Routing |
| --- | --- | --- |
| Government & Politics | Potentially direct where it evaluates the 1987 Constitution, R.A. 6713, peace/human rights, or environmental governance | Screen item-by-item for General Information (both exam levels) |
| History | Background, not separately enumerated by the official current CSE scope | Optional enrichment, not scored mock by default |
| Geography | Background, not separately enumerated by the official current CSE scope | Optional enrichment, not scored mock by default |
| Culture & Traditions | Background, not separately enumerated by the official current CSE scope | Optional enrichment, not scored mock by default |

The CSC General Information scope is **Philippine Constitution; R.A. 6713; Peace and Human Rights Issues and Concepts; Environment Management and Protection**. Other CSE subtests are verbal, numerical, Professional analytical, and Subprofessional clerical. Questions about government and politics are **not automatically** CSE aligned; map each to an enumerated topic.

## Source and permissions

The BetterGov main website GitHub repository has a CC0 dedication; **this does not by itself prove that the quiz subdomain's question bank is covered by CC0**. The quiz application's original source repository and content license were not verified in this review. Do not copy quiz stems, choices, keys, or explanations into Civio. Civio's own question design spec requires independently authored original questions and a documented provenance trail. Even if quiz permission is later established, prefer original Civio items informed by verified primary sources.

## Audit required before any bank changes

1. Obtain quiz question data/source and verify its applicable content license or written reuse permission; preserve source URL and revision date.
2. Inventory all distinct stems and associated keys, labels, and explanations **in a temporary review-only working area**, not an active bank or release collection.
3. Tag each item: direct CSE scope / optional civic enrichment / out of scope, with precise concept and primary reference.
4. Independently verify law and governance details against official/legal primary sources; check dated or disputed claims, ambiguous choices, bad keys, and duplicates versus Civio's existing bank.
5. Draft **original** Civio-formatted questions only for identified gaps, with full provenance and spec-required distractors/explanations. Mark `status: draft`, `review_status: unreviewed`.
6. Run qa.py / qa_all.py in a real checkout; pass review to an independent reviewer or GT. Only an authorized human/delegate may approve. Record any decision in AUDIT_TRACKER.md before import.

## Website copy decision

Approved positioning, added to public landing page under “Choose Your Exam”:

> Civio: An independent platform helping Filipinos prepare for public service through accessible, reliable Civil Service Exam education.

Maintain a separate explicit statement of no CSC affiliation (on the About page and page metadata). Do **not** present this review as a BetterGov partnership or endorsement.
