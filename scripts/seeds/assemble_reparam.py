#!/usr/bin/env python3
"""Assemble baseline_reparameterized.json. Run from scripts/seeds."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_reparameterized_bank as core
import build_reparameterized_bank_part2 as words
import reparam_verbal as verbal

FACT_SUBS = {1, 2, 3, 4}


def main() -> None:
    rows = json.loads(core.SNAPSHOT.read_text(encoding="utf-8"))
    fact_stems = verbal.load_fact_stems(core.FACTS)
    counters: Counter[int] = Counter()
    built = []
    for old in rows:
        qid = old["id"]
        sub = old["subcategory_id"]
        if qid in verbal.FILIPINO:
            built.append(verbal.build_filipino(old))
            continue
        if sub in FACT_SUBS or qid in fact_stems:
            if qid not in fact_stems:
                raise SystemExit(f"missing fact stem for {qid}")
            built.append(verbal.build_fact(old, fact_stems))
            continue
        index = counters[sub]
        counters[sub] += 1
        if sub == 5:
            built.append(words.build_meaning(old, index))
        elif sub == 6:
            built.append(verbal.build_from_bank(old, verbal.COMPLETIONS, index))
        elif sub == 7:
            built.append(verbal.build_from_bank(old, verbal.ERRORS, index))
        elif sub == 8:
            built.append(verbal.build_from_bank(old, verbal.STRUCTURES, index))
        elif sub == 9:
            built.append(verbal.build_from_bank(old, verbal.PARAGRAPHS, index))
        elif sub == 10:
            built.append(verbal.build_from_bank(old, verbal.READINGS, index))
        elif sub == 11:
            built.append(words.build_analogy(old, index))
        elif sub == 12:
            built.append(verbal.build_symbolic(old, index))
        elif sub == 13:
            built.append(verbal.build_from_bank(old, verbal.ASSUMPTIONS, index))
        elif sub == 14:
            built.append(verbal.build_data(old, index))
        elif sub == 15:
            built.append(core.build_operations(old, index))
        elif sub == 16:
            built.append(core.build_sequence(old, index))
        elif sub == 17:
            built.append(core.build_word_problem(old, index))
        elif sub == 18:
            built.append(verbal.build_filing_order(old, index))
        elif sub == 19:
            built.append(words.build_spelling(old, index))
        else:
            raise SystemExit(f"unhandled subcategory {sub}")

    stems = [row["stem"] for row in built]
    prior = [row["prior_stem"] for row in built]
    if len(stems) != len(set(stems)):
        dupes = [stem for stem, count in Counter(stems).items() if count > 1]
        raise SystemExit("duplicate stems:\n" + "\n".join(dupes[:20]))
    if len(prior) != len(set(prior)):
        raise SystemExit("duplicate prior stems")
    if len(built) != len(rows):
        raise SystemExit(f"count {len(built)} != {len(rows)}")
    overlap = sorted(set(stems) & set(prior))
    if overlap:
        raise SystemExit("new stem repeats an old stem:\n" + "\n".join(overlap[:20]))
    core.OUT.write_text(json.dumps(built, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(built)} items to {core.OUT}")


if __name__ == "__main__":
    main()
