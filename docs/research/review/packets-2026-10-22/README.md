# Review packets, 2026-10-22

723 non-approved manifest rows in 28 packets (at most 40 items each). Built by `scripts/batches/qa/review_packets_2026_10_22.py`.

Order of work: P1 (second pass on already-reviewed rows), then P2 (rows with a review note), then P3 (new 22 Oct drafts), then P4.

| Priority | Items | analytical | clerical | general_information | numerical | verbal_en | verbal_fil |
|---|---|---|---|---|---|---|---|
| P1 | 42 | 0 | 0 | 0 | 42 | 0 | 0 |
| P2 | 84 | 14 | 0 | 9 | 46 | 15 | 0 |
| P3 | 258 | 43 | 50 | 43 | 23 | 99 | 0 |
| P4 | 339 | 102 | 48 | 35 | 32 | 0 | 122 |

Review notes in P2:

- 46 × legacy row: no domain solver; key checked by hand sheet (audit/legacy_keys or GI evidence sheet)
- 38 × stem frame shared by N bank rows: check it is not a numeric/name variant
- 7 × reading passage is N words, under the N-word spec minimum

Record decisions in `decisions.csv`. ACCEPT from a human reviewer is the only path to approval; the bank worker never approves.
