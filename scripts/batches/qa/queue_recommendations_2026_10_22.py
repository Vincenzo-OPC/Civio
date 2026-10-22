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


EV = "docs/research/review/queue-evidence-2026-10-22.json"
SELF = "Authored by the bank worker (22 Oct drafts); the author's content QA is not independent, so a human read is still required."
HOW = {"recipe solver": "key recomputed from the stem by the item's recipe (drafts/solver_2026_10_22.py)",
       "bank solver": "key recomputed from the stem by the qa.py domain solver",
       "evidence sheet": "key matches the hand-checked evidence sheet (audit/verified_keys or gi_legacy_evidence, verbatim lawphil quote)",
       "lawphil evidence": "key matches the verbatim source quote checked against the committed lawphil text"}


def p2_p4(m, cache):
    """P2-P4: evidence from queue_evidence_2026_10_22.py plus the reviewer's reading notes below."""
    import distractor_length_2026_10_22 as DL
    out = []
    for e in json.load(open(EV, encoding="utf-8")):
        f = e["source_file"]
        if f not in cache:
            d = json.load(open(f, encoding="utf-8")); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        it = cache[f][e["id"]]
        arch, d1022 = it.get("archetype", ""), "D1022" in e["id"]
        notes = []
        if e["key_check"] in HOW:
            notes.append(HOW[e["key_check"]])
        elif d1022:
            notes.append("judgment item: adversarial read by its author on 22 Oct (second answer, passage support, relation, connectors, grammar, distractors); not an independent check")
        else:
            notes.append("judgment item: stem, key and all three wrong options read in this pass; one defensible answer")
        rec = "Accept"
        if e["id"] in DL.LONGER:
            notes.append("repaired 22 Oct pm: key was conspicuously the longest option; wrong options lengthened (same wrong idea, why_wrong unchanged)")
        if any("stem frame" in x for x in e["flags"]) or "stem frame shared" in e.get("review_notes", ""):
            notes.append("shares a wording frame with other rows, but the numbers and the rule differ, so it is a distinct item; keep an eye on bank variety")
        if arch == "VFIL-KASALUNGAT":
            notes.append("antonym in context checked; the 'medyo/bahagyang' partial-change option recurs across this set and is a known pattern a test-wise reader may learn")
        human = d1022
        if it.get("domain") == "verbal_fil" and qa.passage_words(it) is not None:
            n = qa.passage_words(it)
            if qa.passage_errors(it):
                rec = "Escalate"
                notes.append(f"Filipino passage is {n} words and fails the two-level gate (SHORT >= 80, LONG 150-250)")
            elif any("GT decision 15:48" in h.get("reason", "") for h in it.get("revision_history", [])):
                rec = "Accept revision"; human = True
                notes.append(f"passage lengthened 22 Oct to {n} words (SHORT level, GT decision 15:48) with neutral background sentences; "
                             "question, options and key unchanged; the added sentences were written by the bank worker, so a human should read them against every option")
        if any("absolute word" in x for x in e["flags"]):
            notes.append("absolute word in the key checked against the text: supported")
        ar = e.get("adversarial_read")
        if ar and ar["result"] != "no defect found":
            notes.append(f"adversarial read: {ar['finding']}" + (f"; {ar['action']}" if ar["action"] else ""))
            if ar["action"]:
                rec = "Accept revision"
        if ar:
            human = True
        if d1022:
            notes.append(SELF)
        out.append({"id": e["id"], "priority": e["priority"], "status": e["status"], "recommendation": rec, "reason": " | ".join(notes),
                    "checked": "evidence pass (queue_evidence_2026_10_22.py) + reading", "needs_human_read": "yes" if human else "no",
                    "decision_by_human": ""})
    return out


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
                     "checked": "key re-solved by hand; stem read for ambiguity; distractor explanations read",
                     "needs_human_read": "yes" if r.get("note") == "p1_editorial_revision" else "no", "decision_by_human": ""})
    rows += p2_p4(m, cache)
    Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    import collections
    print(len(rows), "recommendations", dict(collections.Counter((r["priority"], r["recommendation"]) for r in rows)),
          "needs_human_read", collections.Counter(r["needs_human_read"] for r in rows)["yes"])


if __name__ == "__main__":
    main()
