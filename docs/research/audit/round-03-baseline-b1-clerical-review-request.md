# Round 03 baseline audit, batch B1: Clerical (81 items), review request for Chief of Staff

Grok Bot, 2026-10-17. Source: the 81 `source_group='baseline'` Clerical rows (Filing 42, Spelling 39) in the MSI local Civio DB, exported read-only. **No content was changed** in the DB or the repo; these are findings and proposals for CoS.

## Summary

- **3 key errors** (#277, #287, #282): wrong answer marked, live in active mocks today.
- **37 duplicates to retire**: same filing task repeated (#499-#550 restate #274-#313 almost item for item), and 11 spelling targets used 2-3 times. 12 spelling targets also repeat targets already in the bank (CoS rule: unique targets).
- **18 fixes**: 5 placeholder explanations ('Local practice item for Docker study.'), joke distractors on filing-concept items, implausible misspellings (CoS rule: only real misspellings), one wrong spelling rule in an explanation, broken explanation punctuation.
- **23 OK** as they stand (some with optional polish).

If CoS accepts every proposal, 44 baseline Clerical items stay active (3 with corrected keys, 18 fixed) and 37 retire to draft (history kept, as in round 02).

## Note on the paraphrase set (988d862)

`scripts/seeds/baseline_reparameterized.json` (Codex, 2026-10-13) would draft each baseline row and add a new Civio item matched by prior stem. It is **not applied** on the MSI (no rows with `replaces_question_id`). Its 76 Clerical items are new items rather than paraphrases (for example #277 becomes 'which surname comes first: Bajo, Baluyot...'), so they need their own audit. Quick look: spelling targets such as calendar, necessary, publicly and maintenance repeat bank targets, 'Publically' is used as a wrong form, and explanations end with the boilerplate 'do not follow the same steps.' **Ask:** should round 03 fix the baseline rows, or audit the paraphrase set and retire the baseline instead?

## Per item

| ID | Sub | Key now | Finding | Verdict | Proposal |
|---|---|---|---|---|---|
| 51 | Filing | Garcia, Ana | Placeholder explanation ('Local practice item for Docker study.'). | FIX | Write a real explanation: G comes before R, S and T. |
| 52 | Filing | Lim | Placeholder explanation ('Local practice item for Docker study.'). | FIX | Real explanation: Li comes before Lo; Lu and Ly come after. |
| 53 | Spelling | Accommodation | Placeholder explanation ('Local practice item for Docker study.'). Target 'accommodation' repeats #292/#509 (accommodate) and a bank target. | DUPLICATE | Retire. |
| 54 | Spelling | Bureaucracy | Placeholder explanation ('Local practice item for Docker study.'). 'Bureaukracy' is not a real misspelling; 'bureaucracy' is a bank target. | DUPLICATE | Retire. |
| 55 | Spelling | Separate | Placeholder explanation ('Local practice item for Docker study.'). 'separate' repeats #294, #511 and the bank; 'Seperete' is implausible. | DUPLICATE | Retire. |
| 211 | Filing | 11 | 11 before 101, 110, 1001. | OK |  |
| 212 | Filing | Topic or subject matter | Joke distractors (birthday, ink color, lottery). | FIX | Use real methods as distractors: date received, correspondent's name, file number. |
| 213 | Filing | Reminder or follow-up by date | Joke distractors (broken stamps, destroying records weekly). | FIX | Use real file types: transfer file, index file, archive file. |
| 214 | Filing | Brown, Browne, Browning | Nothing before something: Brown, Browne, Browning. | OK |  |
| 215 | Filing | A record may be sought under more than one title | Cross-reference repeated in #283 and #507; joke distractors. | DUPLICATE | Keep #283; retire #215. |
| 216 | Filing | Name of addressee or subject per office rules | Joke distractors (weather, stamp price, shoe size). | FIX | Use real alternatives: date sent only, sender's own name, file number only. |
| 217 | Filing | Date order | Joke distractors (shoe size, hash, ink brand). | FIX | Use real methods: alphabetic, subject, numeric. |
| 218 | Filing | Lopez, Diana | Keep; #273 duplicates it (retire those). | OK |  |
| 273 | Filing | Lopez, Diana | Exact duplicate of #218; explanation says 'given given names'. | DUPLICATE | Retire. |
| 274 | Filing | Cruz, Ana; Cruz, Ben; Cruz, Carlo; Cruz, Dina | Same surname: Ana, Ben, Carlo, Dina. | OK |  |
| 275 | Filing | Abad | Stem asks for a 'sequence' but the options are single surnames. | FIX | Stem: 'Which surname is filed first?' (Abad: d before l). |
| 276 | Filing | Reyes, Luis | Keep; #500 duplicates it (retire those). | OK |  |
| 277 | Filing | Dela Cruz; Del Mundo; Del Rosario; Delos Santos | With the prefix joined and filed letter by letter (ARMA Rule 6), the order is Dela Cruz, Del Mundo, Delos Santos, Del Rosario (dela < delm < delo < delr). The key puts Del Rosario before Delos Santos, and no option has the right order. | KEY ERROR | Replace option 2 with 'Dela Cruz; Del Mundo; Delos Santos; Del Rosario', make it the key, and fix the explanation. |
| 278 | Filing | Garcia | Surname is the first unit. | OK |  |
| 279 | Filing | 14; 41; 104; 401 | Keep; #502 duplicates it (retire those). | OK |  |
| 280 | Filing | 2026-010 | Keep; #503, #544 duplicates it (retire those). | OK |  |
| 281 | Filing | 02 Jan 2026; 28 Feb 2026; 15 Mar 2026; 01 Apr 2026 | Keep; #508 duplicates it (retire those). | OK |  |
| 282 | Filing | Under L, before “Leave Application” | 'Leave Application' files before 'Leave Credits' (A before C), so the key 'Under L, before Leave Application' is wrong and no option is right. | KEY ERROR | Change the key text to 'Under L, after "Leave Application"'. |
| 283 | Filing | A note directing the user from the secondary subject to the primary file | Cross-reference points to the primary file. | OK | Replace the joke distractors. |
| 284 | Filing | 56 | Keep; #506 duplicates it (retire those). | OK |  |
| 285 | Filing | Approved Travel Claims — May 2026 | Keep; #504, #545 duplicates it (retire those). | OK |  |
| 286 | Filing | 010 | 009 then 010. | OK |  |
| 287 | Filing | Bayanihan Center; Bayani Foundation; Bazaars Inc.; Bayview Office | The key (Bayanihan Center; Bayani Foundation; Bazaars Inc.; Bayview Office) puts Bayanihan before Bayani and Baz before Bay. Nothing-before-something gives option 1: Bayani Foundation; Bayanihan Center; Bayview Office; Bazaars Inc. The explanation already describes option 1. | KEY ERROR | Set correct_option to index 0. |
| 288 | Filing | Date of the correspondence or action recorded | Date of the correspondence. | OK | Replace 'Date the clerk took lunch' with 'Date the paper was filed'. |
| 289 | Filing | Leave an out-guide showing the folder’s location and borrower | Keep; #505 duplicates it (retire those). | OK |  |
| 290 | Filing | A retrieval description or subject | Joke distractors (favorite color, advertisement). | FIX | Use real index fields: retention period, location only, date only. |
| 291 | Filing | Personnel → Leave → Vacation Leave → 2026 | Broad to narrow. | OK |  |
| 292 | Spelling | Accommodate | Keep as the one 'accommodate' item (retire #53, #509). | OK | Check against the bank's 'accommodation' target; if CoS counts them as one word, retire this too. |
| 293 | Spelling | Maintenance | 'maintenance' repeats #513 and the bank. | DUPLICATE | Retire. |
| 294 | Spelling | Separate | 'separate' repeats #55, #511 and the bank. | DUPLICATE | Retire. |
| 295 | Spelling | Privilege | 'privilege' repeats #512 and the bank. | DUPLICATE | Retire. |
| 296 | Spelling | Questionnaire | 'questionnaire' repeats #514 and the bank; 'Questioneer' is implausible. | DUPLICATE | Retire. |
| 297 | Spelling | Occurrence | 'occurrence' repeats #510, #547 and the bank. | DUPLICATE | Retire. |
| 298 | Spelling | Liaison | 'liaison' is a bank target; 'Liaision' is implausible. | DUPLICATE | Retire. |
| 299 | Spelling | Millennium | 'Milleniun' is a keyboard slip, not a real misspelling. | FIX | Replace it with 'Milenium'. |
| 300 | Spelling | Embarrass | 'embarrass' repeats #516 and the bank; 'Embarres' is implausible. | DUPLICATE | Retire. |
| 301 | Spelling | Conscientious | 'conscientious' repeats #515. Explanation says 'the first option', which breaks when choices are shuffled. | FIX | Keep this one, retire #515; reword the explanation without a position. |
| 302 | Spelling | Entrepreneur | Keep as the one 'entrepreneur' item (retire #546). | OK |  |
| 303 | Spelling | Hierarchy | Heirarchy and Hierachy are real misspellings. | OK |  |
| 304 | Spelling | Indispensable | 'Indispensabel' is not a real misspelling. | FIX | Replace it with 'Indespensable'. |
| 305 | Spelling | Miscellaneous | 'miscellaneous' repeats #518; 'Misceallaneous' is implausible. | FIX | Keep this one, retire #518; replace that foil with 'Miscellanious'. |
| 306 | Spelling | Necessary | 'necessary' is a bank target. | DUPLICATE | Retire. |
| 307 | Spelling | Acquaintance | Foils are real misspellings. | OK |  |
| 308 | Spelling | Supersede | 'Supercede' is listed as a variant in major dictionaries, so marking it wrong is arguable; 'Supersied' is implausible. | FIX | Pick a different target, or retire. |
| 309 | Spelling | Reconciliation | 'Reconcilitation' is implausible. | FIX | Replace it with 'Reconsiliation'. |
| 310 | Spelling | Exaggerate | Exagerate and Exagerrate are real. | OK | Optional: replace 'Exaggerete'. |
| 311 | Spelling | Publicly | 'Publically' is a recorded variant (CoS ruled it out as a wrong form in round 02); 'Publikly' is implausible. | FIX | Pick a different target, or retire. |
| 312 | Spelling | Definitely | 'definitely' repeats #517 and the bank. | DUPLICATE | Retire. |
| 313 | Spelling | Pronunciation | 'Pronunciashun' is a joke spelling. | FIX | Replace it with 'Pronounciasion'. |
| 499 | Filing | Alonzo, Alvarado, Amador, Aquino | Key correct; explanation boilerplate lacks a period ('Aquino Therefore'). Same in #499-#550. | FIX | Fix punctuation, drop 'The other choices fail because the other choices'. |
| 500 | Filing | Santos, Luis | Same task as #276. | DUPLICATE | Retire. |
| 501 | Filing | De Leon, Carla | De Leon before Delos Reyes (dele < delo). | OK | Explanation punctuation. |
| 502 | Filing | 007, 018, 102, 120 | Same task as #279. | DUPLICATE | Retire. |
| 503 | Filing | 2027-015 | Same task as #280. | DUPLICATE | Retire. |
| 504 | Filing | Approved Travel Claims, Q2 2027 | Same task as #285; joke distractors ('Claims maybe'). | DUPLICATE | Retire. |
| 505 | Filing | The folder and the borrower or destination | Same task as #289. | DUPLICATE | Retire. |
| 506 | Filing | 83 | Same task as #284. | DUPLICATE | Retire. |
| 507 | Filing | Direct the user from an alternate subject to the primary file | Same task as #283. | DUPLICATE | Retire. |
| 508 | Filing | 08 February 2027; 19 February 2027; 03 March 2027; 12 April 2027 | Same task as #281. | DUPLICATE | Retire. |
| 509 | Spelling | Accommodate | 'accommodate' repeat; vague stem. | DUPLICATE | Retire. |
| 510 | Spelling | Occurrence | 'occurrence' repeat; vague stem. | DUPLICATE | Retire. |
| 511 | Spelling | Separate | 'separate' repeat. | DUPLICATE | Retire. |
| 512 | Spelling | Privilege | 'privilege' repeat. | DUPLICATE | Retire. |
| 513 | Spelling | Maintenance | 'maintenance' repeat. | DUPLICATE | Retire. |
| 514 | Spelling | Questionnaire | 'questionnaire' repeat. | DUPLICATE | Retire. |
| 515 | Spelling | Conscientious | 'conscientious' repeat. | DUPLICATE | Retire. |
| 516 | Spelling | Embarrass | 'embarrass' repeat; stem says 'item 8'. | DUPLICATE | Retire. |
| 517 | Spelling | Definitely | 'definitely' repeat; stem says 'item 9'. | DUPLICATE | Retire. |
| 518 | Spelling | Miscellaneous | 'miscellaneous' repeat; stem says 'item 10'. | DUPLICATE | Retire. |
| 543 | Filing | Garcia, Liza | Garcia, Liza first. | OK | Explanation punctuation. |
| 544 | Filing | 03-119 | Same task as #280. | DUPLICATE | Retire. |
| 545 | Filing | Personnel Leave Requests, Approved, January 2027 | Same task as #285; joke distractors. | DUPLICATE | Retire. |
| 546 | Spelling | Entrepreneur | 'entrepreneur' repeat; stem 'for the first term' is meaningless. | DUPLICATE | Retire. |
| 547 | Spelling | Occurrence | 'occurrence', third copy. | DUPLICATE | Retire. |
| 548 | Spelling | Receive | Explanation says receive follows 'i-before-e after c'; the rule is the reverse (e before i after c). | FIX | Explanation: 'i before e except after c: rec-ei-ve.' |
| 550 | Spelling | Calendar | 'calendar' is a bank target. | DUPLICATE | Retire. |

## Asks for CoS

1. Approve the 3 key corrections (they affect active mocks now).
2. Approve retiring the duplicates (set to draft, not deleted).
3. Approve the fixes, or ask for rewritten items in a gap-fill file instead.
4. Rule on the paraphrase set (note above).
