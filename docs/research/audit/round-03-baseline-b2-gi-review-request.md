# Round 03 baseline audit, batch B2: General Information, Constitution and Peace/Human Rights (70 items), review request for Chief of Staff

Grok Bot, 2026-10-17. Source: `source_group='baseline'` GI rows in the MSI local Civio DB (Philippine Constitution 49, Peace and Human Rights 21), exported read-only to `docs/research/audit/data/baseline-550-2026-10-17.json`. Keys checked against the 1987 Constitution text on LawPhil. **No content was changed.** The remaining 64 baseline GI items (R.A. 6713 37, Environment 27) are batch B3, not started.

## Summary

- **0 key errors.** Every key matches the Constitution or the cited law.
- **14 duplicates**: 8 repeat facts already in the approved bank (000007, 000108, 000304, 000507, 000804, 000808, 000903, 000910); 6 repeat other baseline items (habeas corpus, amparo, natural-born, universality, law-making).
- **23 fixes**: 5 placeholder explanations; joke distractors that make the key obvious on about 25 items; 7 Peace items with no legal source (common-sense mediation and peace-education questions, which CSC coverage frames as issues and concepts, not etiquette); one grammar error (#367); boilerplate explanations missing a period on #354-#549.
- **33 OK** (several with optional distractor polish noted).

**Gap noted:** Peace and Human Rights has no items on R.A. 9851 (IHL), R.A. 9745 (Anti-Torture), R.A. 10353 (Anti-Enforced Disappearance), R.A. 9710 (Magna Carta of Women) or R.A. 7610, all Philippine laws within CSC's stated scope. Proposed for a future gap-fill.

## Per item

| ID | Sub | Key now | Finding | Verdict | Proposal |
|---|---|---|---|---|---|
| 1 | Constitution | Constitution | Placeholder explanation ('Local practice item for Docker study.'). | FIX | Real explanation (Art. XVIII, Sec. 27 ratification; the Constitution is the fundamental law). Keep. |
| 2 | Constitution | People | Same fact as approved bank item 000804, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 3 | Constitution | 6 years | Same fact as approved bank item 000808, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 4 | Constitution | Legislative | Placeholder explanation ('Local practice item for Docker study.'). Same task as #355. | DUPLICATE | Retire; keep #355. |
| 5 | Constitution | Article III | Placeholder explanation ('Local practice item for Docker study.'). | FIX | Real explanation: Article III is the Bill of Rights; drop 'mainly'. |
| 9 | Peace/HR | Inherent, inalienable, and universal | Placeholder explanation ('Local practice item for Docker study.'). Same idea as #399 and #74 (universality, non-discrimination). | DUPLICATE | Retire; keep #399. |
| 10 | Peace/HR | Constitutional independent office | Placeholder explanation ('Local practice item for Docker study.'). | FIX | Real explanation: Art. XIII, Sec. 17 creates the CHR as an independent office. |
| 56 | Constitution | Article II (Declaration of Principles and State Policies) | Art. II, Sec. 1. | OK |  |
| 57 | Constitution | Determine whether a law or act is unconstitutional | Judicial review. | OK |  |
| 58 | Constitution | The House of Representatives | Same fact as approved bank item 000007, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 59 | Constitution | Three years | Same fact as approved bank item 000108, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 60 | Constitution | Constitutional Commission under Article IX | COMELEC under Art. IX-C. | OK |  |
| 61 | Constitution | Who are citizens from birth without having to perform any act to acquire or perfect citizenship | Art. IV, Sec. 2. Keep; #361 duplicates it. | OK |  |
| 62 | Constitution | The right to life, liberty, and security against extralegal threats | Keep; #402 duplicates it. | OK | Note: amparo comes from a Supreme Court rule (2007), not the Constitution; recategorize under Peace and Human Rights. |
| 63 | Constitution | Supervision by the President and applicable laws | Art. X, Sec. 4: general supervision of the President. | OK |  |
| 64 | Constitution | Give marginalized and underrepresented sectors a voice in Congress | Party-list (Art. VI, Sec. 5; R.A. 7941). | OK |  |
| 65 | Constitution | Commission on Human Rights | CHR is not one of the three commissions. | OK |  |
| 74 | Peace/HR | To all persons without unjust distinction | Same idea as #399 and #9. | DUPLICATE | Retire. |
| 75 | Peace/HR | Unlawful detention | Keep; #365 duplicates it. | OK |  |
| 76 | Peace/HR | Investigate human rights violations and monitor compliance | CHR investigates, does not convict. | OK |  |
| 77 | Peace/HR | Protection, education, and best interests of the child | Not tied to any law; Joke distractors make the key obvious ('Forced labor as character building'). | FIX | Anchor to R.A. 7610 or the Constitution (Art. XV, Sec. 3(2)) and use real distractors, or retire. |
| 78 | Peace/HR | Speech creates a clear and present danger of substantive evil as allowed by law | Clear and present danger. | OK | Replace 'A private citizen asks politely' with a real test (e.g. 'the speech is unpopular'). |
| 79 | Peace/HR | Conflict resolution, respect for rights, and dialogue | Joke distractors make the key obvious ('Glorifying violence'). | FIX | Retire or rewrite with a real peace-process concept. |
| 80 | Peace/HR | R.A. 8371 (IPRA) | R.A. 8371 (IPRA). | OK |  |
| 81 | Peace/HR | Life | Right to life. | OK | Distractors are weak. |
| 219 | Constitution | Impeachment | Art. VII, Sec. 19: except in cases of impeachment. | OK | Replace 'All criminal offenses without limit' with 'Final conviction of a public official'. |
| 220 | Constitution | Limitations and a defined period set by law | Art. VI, Sec. 23(2). | OK |  |
| 221 | Constitution | Law | Art. IV, Sec. 5. | OK |  |
| 222 | Constitution | 24 | Same fact as approved bank item 000903, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 226 | Peace/HR | A fundamental human right that must be respected | Joke distractors make the key obvious; 'derogable' is not explained. | FIX | Anchor to Art. III, Sec. 12(2) and R.A. 9745 (Anti-Torture Act). |
| 227 | Peace/HR | Equal opportunities and non-discrimination | Not tied to any law; Joke distractors make the key obvious. | FIX | Anchor to Art. II, Sec. 14 or R.A. 9710 (Magna Carta of Women), or retire. |
| 354 | Constitution | Public accountability | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors make the key obvious ('Hereditary succession'). | FIX | Real distractors: separation of powers, local autonomy, civilian supremacy. |
| 355 | Constitution | The legislative branch | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). 'Local school boards' is a joke option. | FIX | Keep; replace that option with 'Constitutional commissions'. |
| 356 | Constitution | The Senate | Senate tries impeachment. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 357 | Constitution | The armed forces of the Philippines | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors make the key obvious ('All private corporations', 'Every foreign military'). | FIX | Real distractors: the PNP, the Cabinet, the National Security Council. |
| 358 | Constitution | Freedom of the press | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors. | FIX | Real distractors: right to information, freedom of assembly, privacy of communication. |
| 359 | Constitution | Right against unreasonable searches and seizures | Art. III, Sec. 2. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 360 | Constitution | Commission on Audit | Same fact as approved bank item 000304, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 361 | Constitution | Natural-born citizenship | Same as #61. | DUPLICATE | Retire. |
| 362 | Constitution | Civil Service Commission | CSC (Art. IX-B). | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 363 | Constitution | Arbitrary government action | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors ('Routine filing errors'). | FIX | Real distractors: equal protection, just compensation, ex post facto. |
| 364 | Constitution | It settles actual controversies involving enforceable rights | Art. VIII, Sec. 1. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 365 | Constitution | Protection against unlawful detention | Same as #75. | DUPLICATE | Retire. |
| 366 | Constitution | Civilian authority is supreme over the military | Same fact as approved bank item 000507, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 367 | Constitution | All members of the same class | Grammar: 'related to the law purpose'. Joke distractors. | FIX | Stem: 'related to the purpose of the law'. |
| 368 | Constitution | Eminent domain | Eminent domain. | OK | Replace 'Police patrol only' with 'Police power'; 'Taxation' as another real power. |
| 369 | Constitution | Two-thirds of all the members of each House vote to pass it again | Same fact as approved bank item 000910, which has full spec metadata. | DUPLICATE | Retire the baseline copy. |
| 370 | Constitution | At least 35 years old on election day | Art. VI, Sec. 3: at least 35 on election day. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 371 | Constitution | Suffrage | Suffrage (Art. V). | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 372 | Constitution | Punish an act that was not criminal when done | Ex post facto (Art. III, Sec. 22). | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 373 | Constitution | The Office of the Ombudsman | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors make the key obvious ('Weather Bureau', 'National Library'). | FIX | Real distractors: COA, CSC, CHR. |
| 374 | Constitution | Manage local affairs within the Constitution and national law | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors ('Print national currency'). | FIX | Real distractors: federal autonomy, independence from presidential supervision. |
| 375 | Constitution | Commission on Elections | COMELEC. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 376 | Constitution | Matters of public concern subject to lawful limitations | Art. III, Sec. 7. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 377 | Constitution | The accused is presumed innocent until the contrary is proved | Art. III, Sec. 14(2). | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 378 | Constitution | Pursuant to an appropriation made by law | Art. VI, Sec. 29(1). | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 399 | Peace/HR | All people without unjust discrimination | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors. | FIX | Keep as the one universality item. |
| 400 | Peace/HR | Use dialogue, evidence, and nonviolent conflict resolution | Common-sense item, no source; Joke distractors make the key obvious. | FIX | Retire or anchor to a named peace framework. |
| 401 | Peace/HR | Privacy and information about a person | Habeas data (Supreme Court rule, 2008). | OK | Recategorize as a rule-of-court remedy; joke distractors. |
| 402 | Peace/HR | Life, liberty, and security | Same as #62. | DUPLICATE | Retire. |
| 403 | Peace/HR | Respects dignity, equality, participation, and accountability | Common-sense item, no source; joke distractors. | FIX | Retire or anchor to the human-rights-based approach as CHR defines it. |
| 404 | Peace/HR | Teaching mediation and respect for different identities | Common-sense item, no source; joke distractors. | FIX | Retire. |
| 415 | Peace/HR | Check compliance and surface problems early | Common-sense item, no source; joke distractors. | FIX | Retire. |
| 416 | Peace/HR | A place where they face serious persecution or harm | Non-refoulement. | OK | Distractors are jokes; replace. |
| 519 | Constitution | Government may not legislatively declare a person guilty and punish them | Bill of attainder (Art. III, Sec. 22). | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 520 | Constitution | Freedom of expression and equal protection | Expression and equal protection. | OK | Two rights in one key is fine; distractors are jokes. |
| 521 | Constitution | Congress | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors make the key obvious ('A barangay sports club'). | FIX | Real distractors: the President, the DBM, COA. |
| 522 | Constitution | Takes private property for public use | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). Joke distractors ('Publishes a weather bulletin'). | FIX | Real distractors: imposes a tax, regulates a business (police power). |
| 523 | Constitution | The state may not establish a religion or prohibit its free exercise, subject to lawful limits | Art. III, Sec. 5. | OK | Explanation boilerplate lacks a period ('... Therefore, the correct option is ...'). |
| 549 | Peace/HR | Applying agreed ground rules to every participant | Common-sense item, no source; joke distractors. | FIX | Retire. |

## Asks for CoS

1. Approve retiring the 14 duplicates (draft, history kept).
2. For the FIX items: approve rewritten replacements in a gap-fill file (drafts), or retire the common-sense Peace items outright.
3. Approve a Peace and Human Rights gap-fill on the laws listed above.
