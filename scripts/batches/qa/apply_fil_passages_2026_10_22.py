#!/usr/bin/env python3
"""GT decision 15:48: lengthen every short Filipino passage to the SHORT level (>= 80 words).
Draft rows are edited in place in their source file. Approved rows are never touched: each gets a -R1 proposal (status draft,
reviewer null, `replaces` set) in docs/research/audit/fixes/vfil-passage-r1-2026-10-22.json, NOT swapped into the manifest.
Siblings that share a passage (VFIL-READ, 4 questions each) all get the same lengthened passage. Idempotent."""
import copy, json, sys
from collections import Counter
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent.parent), str(Path(__file__).parent.parent / "drafts")]
import qa, fil_passages_2026_10_22 as FP  # noqa: E402

MAN = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json"
R1 = Path("docs/research/audit/fixes/vfil-passage-r1-2026-10-22.json")
HIST = {"date": "2026-10-22", "by": "bank worker", "reason": "GT decision 15:48: Filipino SHORT passages need at least 80 words",
        "change": "Passage lengthened with neutral background sentences; question, options, key and explanations unchanged."}


def main():
    m = json.load(open(MAN)); cache, raw = {}, {}
    for r in m["items"]:
        f = r["source_file"]
        if r["domain"] == "verbal_fil" and f not in cache:
            raw[f] = Path(f).read_text(encoding="utf-8"); d = json.loads(raw[f])
            cache[f] = (d, {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)})
    # passage text -> addition, so siblings sharing a passage get the same text
    by_text = {}
    for r in m["items"]:
        if r["id"] in FP.ADD:
            by_text[FP.split(cache[r["source_file"]][1][r["id"]]["stem"])[1]] = (r["id"], FP.ADD[r["id"]])
    props, done, dirty = [], Counter(), set()
    for r in m["items"]:
        if r["domain"] != "verbal_fil":
            continue
        it = cache[r["source_file"]][1][r["id"]]
        n = qa.passage_words(it)
        if n is None:
            continue
        p = FP.split(it["stem"])[1]
        hit = by_text.get(p)
        if hit is None:
            if n < qa.FIL_SHORT_MIN and not any(a in p for _, a in by_text.values()):
                raise SystemExit(f"short Filipino passage with no lengthening text: {r['id']} ({n} words)")
            continue
        key, add = hit
        if add in p:  # already lengthened (idempotent rerun)
            continue
        new = FP.lengthen(it["stem"], add, FP.WHERE.get(key, "end"))
        if it["status"] == "draft":
            it["stem"] = new; it["passage_level"] = "short"
            it.setdefault("revision_history", []).append(dict(HIST, words_before=n, words_after=qa.passage_words(it)))
            dirty.add(r["source_file"]); done["draft_in_place"] += 1
        else:
            pr = copy.deepcopy(it)
            pr.update(id=it["id"] + "-R1", stem=new, passage_level="short", status="draft", review_status="unreviewed",
                      reviewer=None, reviewed_at=None, replaces=it["id"],
                      revision_history=[dict(HIST, **{"from": it["id"], "original_status": it["status"], "words_before": n})])
            pr["revision_history"][0]["words_after"] = qa.passage_words(pr)
            for k in ("approved_by", "approved_at", "signoff", "signed_by"):
                pr.pop(k, None)
            props.append(pr); done["approved_r1_proposal"] += 1
    for p_ in props + [i for f in dirty for i in cache[f][1].values() if i.get("passage_level")]:
        e = qa.check_item(p_)
        assert not e, (p_["id"], e)
    for f in dirty:
        ind = 2 if raw[f].startswith("{\n  \"") else 1
        Path(f).write_text(json.dumps(cache[f][0], ensure_ascii=False, indent=ind) + ("\n" if raw[f].endswith("\n") else ""), encoding="utf-8")
    R1.write_text(json.dumps({"batch": "vfil-passage-r1-2026-10-22", "status": "draft proposals (pending authorized review; not approved, not in manifest)",
                              "note": "Approved originals stay in the bank unchanged until an authorized reviewer accepts or rejects each proposal.",
                              "items": props}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(done)))


if __name__ == "__main__":
    main()
