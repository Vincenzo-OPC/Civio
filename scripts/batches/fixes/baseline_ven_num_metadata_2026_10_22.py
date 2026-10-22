#!/usr/bin/env python3
"""Baseline Verbal EN and Numerical drafts for the flat-2100 manifest (22 Oct 2026, GT approved). Run from the repo root.

For each candidate (baseline-550-spec drafts flagged only for missing metadata, in manifest rank order), until there
are 88 Verbal EN and 21 Numerical passes:
  1. HOLD screen against the 9 local HOLD text files (CSE Reviewer.pdf via OCR). Flag hold_phrase_overlap if the item
     shares >= 20% of its 5-grams with a HOLD file, or if its whole stem (4+ words) appears verbatim.
  2. Content QA: 4 options, distinct option texts, key among the options, no editorial notes in options, right domain
     (no Filipino in Verbal EN), keys checked by hand (MANUAL below), and no near-duplicate of an earlier accepted item.
  3. A pass gets difficulty and est_seconds by rule from approved norms (easy = recall or single step, medium = standard,
     hard = multi-step), plus hold_screen, metadata_note and a revisions entry.
     A fail gets qa_flags, which the review queue blocks, so the manifest takes the next eligible item.
Status stays draft. Needs /workspace/civio-external-reviewers/hold/*.txt, which is local only and never committed.
"""
from __future__ import annotations
import csv, glob, json, re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "qa"))
from flat_2100_manifest_2026_10_22 import is_pct  # noqa: E402  (Numerical percent change is capped and full)

SPEC = "docs/research/audit/data/baseline-550-spec-2026-10-18.json"
QUEUE = "docs/research/bank/draft-review-queue-2026-10-22.csv"
HOLD_GLOB = "/workspace/civio-external-reviewers/hold/*.txt"
QUOTA = {"verbal_en": 88, "numerical": 21}
TODAY = "2026-10-22"
META_ONLY = {"missing_difficulty", "missing_est_seconds", "bad_difficulty", "difficulty_vs_time", "percent_change_topic"}
HOLD_SRC = "9 HOLD files (Mutia-Tayone 255/300 and 2019/2020 compilations, CSEReviewer.com Pro/SubPro v1.0, CSE Reviewer.pdf via OCR)"
# Manual content review, 22 Oct 2026.
MANUAL = {
    "CIVIO-BASELINE-0018": "ambiguous_key: 'staff' can take 'was' or 'were', so both are defensible",
    "CIVIO-BASELINE-0109": "option_artifact: an option carries the note '(informal)'",
    "CIVIO-BASELINE-0112": "ambiguous_key: 'Covered in dust, the clerk…' is also a misplaced modifier",
    "CIVIO-BASELINE-0241": "option_artifact: an option carries the note '(as written)'",
    "CIVIO-BASELINE-0119": "near_dup: same item as 0024 (topic sentence)",
    "CIVIO-BASELINE-0120": "near_dup: same item as 0025 (coherence)",
    "CIVIO-BASELINE-0193": "near_dup: same series as 0185 (squares, next is 36)",
    "CIVIO-BASELINE-0420": "near_dup: same target and relation as 0230 (tenacious)",
    "CIVIO-BASELINE-0425": "near_dup: same target and relation as 0094 (impartial)",
    "CIVIO-BASELINE-0428": "near_dup: same item as 0091 (antonym of scarce)",
    "CIVIO-BASELINE-0440": "near_dup: same error as 0107 ('Between you and I')",
}
FIL = re.compile(r"\b(ang|ng|mga|piliin|alin|wastong|pangungusap|ayos)\b", re.I)
ARTIFACT = re.compile(r"\((as written|informal|sic)\)", re.I)
HARD_SEQ = {"CIVIO-BASELINE-0189", "CIVIO-BASELINE-0191", "CIVIO-BASELINE-0192", "CIVIO-BASELINE-0194"}
MULTI_OP = {"CIVIO-BASELINE-0174", "CIVIO-BASELINE-0182", "CIVIO-BASELINE-0183"}


def toks(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def grams(t, n=5):
    return {" ".join(t[k:k + n]) for k in range(len(t) - n + 1)}


def rule(i):
    """Return (difficulty, est_seconds, why) by approved norms per domain and subtype."""
    c, iid = i.get("competency", ""), i["id"]
    if i["domain"] == "numerical":
        if c == "Number sequence":
            return ("hard", 50, "second-order or combined rule") if iid in HARD_SEQ else ("medium", 45, "single-rule series")
        return ("medium", 45, "multi-step operation") if iid in MULTI_OP else ("easy", 35, "single-step operation")
    if c == "Word meaning":
        return ("easy", 20, "vocabulary recall")
    if c == "Sentence completion":
        return ("medium", 25, "context clue plus word form")
    if c == "Error recognition":
        return ("medium", 25, "grammar and correct usage")
    if c == "Sentence structure":
        applied = bool(re.search(r"\b(which|option|sentence has|revision|combines|is used in|illustrated by)\b", i["stem"], re.I))
        return ("medium", 40, "applied sentence structure") if applied else ("easy", 40, "definition recall")
    if c == "Paragraph organization":
        applied = bool(re.search(r"\b(which|order|should)\b", i["stem"], re.I))
        return ("medium", 45, "applies a paragraph principle") if applied else ("easy", 30, "definition recall (shorter than the 75 s norm for full arrangement tasks)")
    return ("medium", 30, "default")


def main():
    corpus = {p: grams(toks(open(p, encoding="utf-8", errors="ignore").read())) for p in sorted(glob.glob(HOLD_GLOB))}
    assert len(corpus) == 9, f"expected 9 HOLD files, found {len(corpus)}"
    flat = {p: " ".join(toks(open(p, encoding="utf-8", errors="ignore").read())) for p in corpus}
    q = [r for r in csv.DictReader(open(QUEUE, encoding="utf-8"))
         if r["kind"] == "baseline" and r["domain"] in QUOTA and r["result"] == "flag"
         and {f.split(":")[0] for f in r["reasons"].split(";") if f and not f.startswith("also_in")} <= META_ONLY]
    q.sort(key=lambda r: r["id"])
    raw = open(SPEC, encoding="utf-8").read()
    d = json.loads(raw)
    byid = {i["id"]: i for i in d["items"]}
    trim = json.load(open("docs/research/civio-trim-lists-2026-10-22.json"))
    trimmed = set(trim["trimmed_numerical_ids"]) | set(trim["trimmed_verbal_fil_ids"])
    got = {k: 0 for k in QUOTA}
    report = []
    for r in q:
        i = byid[r["id"]]
        dom = i["domain"]
        if got[dom] >= QUOTA[dom] or i["id"] in trimmed or (dom == "numerical" and is_pct(i)):
            continue
        t = toks(i["stem"] + " " + " ".join(o["text"] for o in i["options"]))
        g = grams(t)
        frac = max((len(g & cg) / len(g) for cg in corpus.values()), default=0.0) if g else 0.0
        st = toks(i["stem"])
        verbatim = len(st) >= 4 and any(" ".join(st) in f for f in flat.values())
        fails = []
        if frac >= 0.2 or verbatim:
            fails.append(f"hold_phrase_overlap: shared 5-grams {frac:.2f}, verbatim stem {verbatim}")
        opts = [o["text"] for o in i["options"]]
        if len(opts) != 4 or len({o.strip().lower() for o in opts}) != 4:
            fails.append("options_shape")
        if i["answer_option_id"] not in {o["option_id"] for o in i["options"]}:
            fails.append("key_missing")
        if any(ARTIFACT.search(o) for o in opts):
            fails.append("option_artifact")
        if dom == "verbal_en" and FIL.search(i["stem"] + " " + " ".join(opts)):
            fails.append("wrong_domain: the item is in Filipino")
        if i["id"] in MANUAL:
            fails.append(MANUAL[i["id"]])
        screen = {"date": TODAY, "sources": HOLD_SRC, "shared_5gram_fraction": round(frac, 2), "verbatim_stem": verbatim}
        i["hold_screen"] = screen
        if fails:
            i["qa_flags"] = sorted({f.split(":")[0] for f in fails})
            i["qa_note"] = f"{TODAY} screen: " + "; ".join(fails)
            report.append((i["id"], dom, "fail", "; ".join(fails)))
            continue
        diff, secs, why = rule(i)
        prior = {"difficulty": i.get("difficulty"), "est_seconds": i.get("est_seconds")}
        i["difficulty"], i["est_seconds"] = diff, secs
        i["metadata_note"] = (f"difficulty/est_seconds added {TODAY} by rule (easy = recall or single step, medium = standard, "
                              f"hard = multi-step), using approved norms for {dom} / {i.get('competency')}: {why}. The reviewer confirms.")
        i.setdefault("revisions", []).append({"date": TODAY, "approved_by": "GT", "change": "HOLD-screened, content QA passed, metadata added; still draft.", "prior": prior})
        got[dom] += 1
        report.append((i["id"], dom, "pass", f"{diff}/{secs}s"))
    assert got == QUOTA, got
    Path(SPEC).write_text(json.dumps(d, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    for row in report:
        print(*row, sep="\t")


if __name__ == "__main__":
    main()
