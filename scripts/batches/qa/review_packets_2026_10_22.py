#!/usr/bin/env python3
"""Priority assignment (decisions.csv) for every non-approved row; the packet files themselves are superseded by
approval_packets_2026_10_22.py. Originally: independent review packets for every non-approved row of the flat-2100 manifest (CONTINUE directive 2026-10-22).

Independent means the reviewer solves each item before seeing the key: every packet lists the items with their
options only, and the key, explanation, source and machine-QA notes sit in a separate answer sheet at the end.
Packets are grouped by priority, then domain, at most 40 items each. Nothing here approves, signs or activates.

Priority
  P1  status "reviewed": one human pass done, waiting for the second (final) decision.
  P1  also holds the P1 editorial -R1 revisions (draft) that replace a reviewed row; review them against the original.
  P2  carries a review note: qa_flags, a legacy row checked only by a hand sheet, a reading passage under the
      150-word spec minimum, or an item whose stem frame repeats inside the bank (possible template variant).
  P3  new 22 Oct drafts: machine QA + hand check by the bank worker, never human-reviewed.
  P4  other drafts that pass every machine check.
Run from the repo root."""
import collections, csv, json, re, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent), str(Path(__file__).parent.parent)]
from flat_2100_manifest_2026_10_22 import OUT_JSON  # noqa: E402
import qa  # noqa: E402

OUT = Path("docs/research/review/packets-2026-10-22")
SIZE = 40
CHECK = {
    "numerical": "Solve it yourself first. Is exactly one option correct? Do the wrong options come from real mistakes? Does the method_steps explanation teach a no-calculator path?",
    "analytical": "Solve it first. Is the conclusion forced by the premises (no outside knowledge)? For analogies, does exactly one pair share the stem relation, in the same order?",
    "verbal_en": "Answer from the passage/sentences only. Is the key the single best answer? Is any distractor also defensible?",
    "verbal_fil": "Sagutin muna. Tama ba ang baybay ayon sa KWF? Iisa lang ba ang tamang sagot? Natural ba ang Filipino?",
    "clerical": "Work it first. For filing, apply the ARMA rule named in the answer sheet; does it give exactly one order?",
    "general_information": "Open the source_url and find the quoted text. Does it support the key exactly, and is the law still current (no amendment)?",
}


def load(path, cache={}):
    if path not in cache:
        d = json.load(open(path, encoding="utf-8"))
        cache[path] = {i["id"]: i for i in (d.get("items") if isinstance(d, dict) else d) if isinstance(i, dict) and "id" in i}
    return cache[path]


def words(t):
    return len(re.findall(r"[A-Za-z']+", t))


def notes(it, frames):
    n = []
    if it.get("qa_flags"):
        n += ["qa_flag: " + (f if isinstance(f, str) else json.dumps(f, ensure_ascii=False)) for f in it["qa_flags"]]
    if it.get("_legacy"):
        n.append("legacy row: no domain solver; key checked by hand sheet (audit/legacy_keys or GI evidence sheet)")
    if it["domain"] == "verbal_en" and re.match(r"VEN-RC", it.get("archetype", "")):
        body = it.get("passage") or it["stem"].rsplit("\n\n", 1)[0]
        if words(body) < 150:
            n.append(f"reading passage is {words(body)} words, under the 150-word spec minimum")
    f = qa.stem_frame(it["stem"]) if hasattr(qa, "stem_frame") else it["stem"][:40]
    if frames[(it["domain"], f)] > 3 and it["domain"] in ("numerical", "analytical"):
        n.append(f"stem frame shared by {frames[(it['domain'], f)]} bank rows: check it is not a numeric/name variant")
    return n


def main():
    m = json.load(open(OUT_JSON, encoding="utf-8"))
    rows = [r for r in m["items"] if r["status"] != "approved"]
    allit = [load(r["source_file"])[r["id"]] for r in m["items"]]
    frames = collections.Counter((i["domain"], qa.stem_frame(i["stem"]) if hasattr(qa, "stem_frame") else i["stem"][:40]) for i in allit)
    recs = []
    for r in rows:
        it = load(r["source_file"])[r["id"]]
        n = notes(it, frames)
        p = "P1" if r["status"] == "reviewed" or r.get("note") == "p1_editorial_revision" else "P2" if n else "P3" if "D1022" in r["id"] else "P4"
        recs.append((p, r, it, n))
    recs.sort(key=lambda x: (x[0], x[1]["domain"], x[1]["id"]))
    OUT.mkdir(parents=True, exist_ok=True)
    for old in [p for p in OUT.glob("*.md") if re.fullmatch(r"P[1-4]-[a-z_]+-\d\d\.md|README\.md", p.name)]:  # only files this script writes; keep reviewer files
        old.unlink(missing_ok=True)
    index, groups = [], collections.defaultdict(list)
    for rec in recs:
        groups[(rec[0], rec[1]["domain"])].append(rec)
    for (p, dom), recs_g in sorted(groups.items()):
        for k in range(0, len(recs_g), SIZE):
            chunk = recs_g[k:k + SIZE]
            name = f"{p}-{dom}-{k // SIZE + 1:02d}.md"
            L = [f"# Review packet {name[:-3]}", "", f"Priority {p}, domain {dom}, {len(chunk)} items. Status of every item: not approved.", "",
                 "**How to review independently:** answer every item below before opening the answer sheet. "
                 "Then compare, and mark each item ACCEPT / FIX (say what) / REJECT in `decisions.csv` (one row per id). "
                 "Do not edit the item files; the bank worker applies fixes as draft replacements.", "",
                 f"**Check for this domain:** {CHECK[dom]}", "", "## Items", ""]
            for n_, (_, r, it, _n) in enumerate(chunk, 1):
                L += [f"### {n_}. `{r['id']}`  ({it.get('track')}, {it.get('difficulty')}, {it.get('est_seconds')} s)", "", it["stem"].strip(), ""]
                L += [f"- ({chr(65 + j)}) {o['text']}" for j, o in enumerate(it["options"])] + [""]
            L += ["---", "", "## Answer sheet (open only after answering)", ""]
            for n_, (_, r, it, nt) in enumerate(chunk, 1):
                kj = next(j for j, o in enumerate(it["options"]) if o["option_id"] == it["answer_option_id"])
                rv = it.get("reveal") or {}
                L += [f"### {n_}. `{r['id']}`: key ({chr(65 + kj)}) {it['options'][kj]['text']}", ""]
                if isinstance(rv, dict):
                    L.append(f"- Why correct: {rv.get('why_correct', '')}")
                    for j, o in enumerate(it["options"]):
                        w = (rv.get("why_wrong") or {}).get(o["option_id"])
                        if w:
                            L.append(f"- ({chr(65 + j)}) {w}")
                else:
                    L.append(f"- Explanation: {rv}")
                if it.get("source_url"):
                    L.append(f"- Source: {it.get('source', '')} <{it['source_url']}>" + (f"; quote: \"{it['source_quote']}\"" if it.get("source_quote") else ""))
                L.append(f"- File: `{r['source_file']}`")
                for x in nt:
                    L.append(f"- Review note: {x}")
                L.append("")
            pass  # packet files superseded by approval_packets_2026_10_22.py (GT review 22 Oct, 4:18 PM); only decisions.csv is kept
            for _, r, it, nt in chunk:
                index.append({"priority": p, "packet": name, "id": r["id"], "domain": dom, "track": it.get("track"), "status": r["status"],
                              "source_file": r["source_file"], "review_notes": " | ".join(nt), "decision": "", "reviewer": "", "comment": ""})
    with (OUT / "decisions.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(index[0]), lineterminator="\n"); w.writeheader(); w.writerows(index)
    by = collections.Counter((x["priority"], x["domain"]) for x in index)
    pk = collections.Counter(x["priority"] for x in index)
    R = ["# Review packets, 2026-10-22", "", f"{len(index)} non-approved manifest rows in {len({x['packet'] for x in index})} packets "
         f"(at most {SIZE} items each). Built by `scripts/batches/qa/review_packets_2026_10_22.py`.", "",
         "Order of work: P1 (second pass on already-reviewed rows), then P2 (rows with a review note), then P3 (new 22 Oct drafts), then P4.", "",
         "| Priority | Items | " + " | ".join(sorted({d for _, d in by})) + " |", "|---|---|" + "---|" * len({d for _, d in by})]
    for p in sorted(pk):
        R.append(f"| {p} | {pk[p]} | " + " | ".join(str(by[(p, d)]) for d in sorted({d for _, d in by})) + " |")
    notes_c = collections.Counter(re.sub(r"\d+", "N", n.split(":")[0] if n.startswith("qa_flag") else n) for x in index for n in x["review_notes"].split(" | ") if n)
    R += ["", "Review notes in P2:", ""] + [f"- {v} × {k}" for k, v in notes_c.most_common()]
    R += ["", "Record decisions in `decisions.csv`. ACCEPT from a human reviewer is the only path to approval; the bank worker never approves."]
    (OUT / "README.md").write_text("# Superseded\n\nThe P1-P4 packets were replaced by evidence-typed approval packets in "
                                   "`../approval-packets-2026-10-22/`. This folder keeps `decisions.csv` (priority per row, read by the evidence pass) "
                                   "and the independent AI review of P1.\n", encoding="utf-8")
    print(json.dumps({"items": len(index), "packets": len({x['packet'] for x in index}), "by_priority": dict(pk)}, indent=1))


if __name__ == "__main__":
    main()
