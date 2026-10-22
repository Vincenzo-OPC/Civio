# Dexter Rescue editorial validation packet (2026-10-22)

- Status: **ready for two human reviewers. Nothing reviewed, nothing approved.** Agents never fill the reviewer columns.
- Packet: `dexter-rescue-pilot-packet-2026-10-22.csv`. That is 60 approved items, 20 each of NUM-WP-PCT-CHANGE, NUM-WP-RATIO and CLR-SPELL-WRONG, with one row per wrong option (180 rows).
- Rebuild: `python3 docs/research/dexter2/pilot/build_pilot_packet.py` (seed 20261022; the CSV sha256 is in `pilot-packet-summary.json`).
- Selection: one item per rough stem family (numbers and names masked), then a seeded draw. The family heuristic is a tool, not a judgement; reviewers judge variety.

## How to review

For each row, reviewers 1 and 2 work **independently** (don't look at each other's columns):

| column | values |
|---|---|
| `rN_code_matches_error` | yes / no / unclear: does `distractor_code` name the real mistake that leads to `distractor_option`? |
| `rN_why_wrong_accurate` | yes / no / unclear: is `why_wrong` correct, and does it name that mistake? |
| `rN_item_family_distinct` | yes / no: is this item meaningfully different from the others of its skill (fill on the item's first row)? |
| `rN_notes` | free text |

Then an adjudicator fills:

- `agreement`: agree / disagree
- `disagreement_note` and `ambiguity_note`
- `adjudication`: validated / rejected / needs_edit
- `adjudicator` and `adjudicated_at`

Nobody adjudicates their own authored items.

## Gate

An item may go into `config/dexter_rescue.php` → `validated_question_ids` only when all three of its distractor rows are adjudicated `validated`.

The pilot passes as a **review gate** if ≥ 90% of rows are agreed `yes` on both checks. Passing is evidence that this metadata is usable for Rescue. It is **not proof** that the codes are right for learners, and it doesn't validate any other skill.

Editing a code or explanation is a bank change for the bank owner, not part of this review.

## Known gaps (from `../bank_metadata_audit.json`)

- **Basic percent**: 0 approved NUM-PCT-BASIC items, so Rescue can't send learners to that prerequisite yet.
- **Filing codes unmapped**: all 58 approved CLR-FILE-POSITION items use the parent code `CLR-FILE-ORDER`, which isn't in the Dexter taxonomy. Their `distractor_subreason` codes (CLR-LETTER-ORDER, CLR-FIRSTNAME-FIRST, CLR-PREFIX-SPLIT, CLR-TITLE-COUNTED) are in it. Mapping them is an editorial decision.
- **NUM-PARTIAL overuse**: 332 uses across approved items. It says "stopped early" without saying where, so it's weak as a diagnosis. Reviewers should mark it `unclear` when it doesn't name the actual stopping point.
- **Near-duplicate families**: NUM-WP-PCT-CHANGE has 37 approved items but only about 20 families, so this packet uses every family. NUM-OPS-ORDER has 30 items in about 6 families. Fresh follow-ups in these skills will feel repetitive.
