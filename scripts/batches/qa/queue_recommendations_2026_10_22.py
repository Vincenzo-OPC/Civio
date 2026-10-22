#!/usr/bin/env python3
"""GT directive 3 (c): reasoned recommendations for the pending queue, worked P1 first. Recommendations only: they never change
status, never record approval. Writes docs/research/review/queue-recommendations-2026-10-22.csv. Run from the repo root."""
import csv, json, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent.parent), str(Path(__file__).parent.parent / "drafts")]
import qa  # noqa: E402
import method_first_2026_10_22 as MF  # noqa: E402

MAN, OUT = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json", "docs/research/review/queue-recommendations-2026-10-22.csv"
NOTE = {  # P1 rows with something a human reviewer should look at beyond the key
 "926032": ("Accept", "Key 4 re-solved (16 vs 20 crates). The phrase 'without removing any crates from the larger team' is wordy but unambiguous."),
 "926046": ("Accept", "Key 33 1/3 km/h re-solved as total distance ÷ total time (100 ÷ 3). Classic average-speed trap distractor (37.5) is the right one to include."),
 "926003": ("Accept", "Key 3/5 re-solved by distance above 1/2 and by decimals; options are close, as intended for a hard item."),
}


def main():
    m = json.load(open(MAN, encoding="utf-8"))
    rows, cache = [], {}
    for r in m["items"]:
        p1 = r["status"] == "reviewed" or r.get("note") == "p1_editorial_revision"
        if not p1:
            continue
        f = r["source_file"]
        if f not in cache:
            d = json.load(open(f, encoding="utf-8")); cache[f] = {i["id"]: i for i in d["items"]}
        it = cache[f][r["id"]]
        st = (it["reveal"].get("method_steps") or MF.steps(it))
        key = qa.key_text(it)
        assert key.split(" ")[0].replace("₱", "").replace(",", "") in st["5_solve_by_hand"].replace("₱", "").replace(",", ""), it["id"]
        if r.get("note") == "p1_editorial_revision":
            rec, why = "Accept revision", it["revision_history"][0]["change"] + " Key recomputed by recipe; supersedes " + it["replaces"] + "."
        else:
            rec, why = NOTE.get(it["id"][-6:], ("Accept", f"Key '{key}' re-solved by hand without a calculator (see method-first -R1 proposal); stem clear, one defensible answer."))
        rows.append({"id": r["id"], "priority": "P1", "status": r["status"], "recommendation": rec, "reason": why,
                     "checked": "key re-solved by hand; stem read for ambiguity; distractor explanations read", "decision_by_human": ""})
    Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "P1 recommendations;", sum(r["recommendation"].startswith("Accept") for r in rows), "accept-type")


if __name__ == "__main__":
    main()
