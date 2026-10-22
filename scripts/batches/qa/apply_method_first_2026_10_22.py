#!/usr/bin/env python3
"""Apply method-first explanations (drafts/method_first_2026_10_22.py) to every draft Numerical row of the flat-2100 manifest
that lacks reveal.method_steps, in its own source file. Approved and reviewed rows are never edited: for them a -R1 proposal
(status draft, replaces=<id>) is written to docs/research/audit/fixes/method-first-r1-proposals-2026-10-22.json.
The final step of every solve is checked against the key. Run from the repo root, then manifest_swap (refreshes hashes)."""
import collections, copy, json, re, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent), str(Path(__file__).parent.parent), str(Path(__file__).parent.parent / "drafts")]
from flat_2100_manifest_2026_10_22 import OUT_JSON  # noqa: E402
import qa  # noqa: E402
import method_first_2026_10_22 as MF  # noqa: E402

R1 = Path("docs/research/audit/fixes/method-first-r1-proposals-2026-10-22.json")


def main(limit_r1=None):
    m = json.load(open(OUT_JSON, encoding="utf-8"))
    by_file = collections.defaultdict(list)
    for r in m["items"]:
        if r["domain"] == "numerical":
            by_file[r["source_file"]].append(r)
    done, skipped, props = collections.Counter(), [], []
    for f, rows in by_file.items():
        raw = open(f, encoding="utf-8").read()
        d = json.loads(raw)
        ind = len(raw.split("\n")[1]) - len(raw.split("\n")[1].lstrip(" ")) or 1
        L = d["items"] if isinstance(d, dict) else d
        idx = {i["id"]: i for i in L if isinstance(i, dict) and "id" in i}
        changed = False
        for r in rows:
            it = idx[r["id"]]
            if isinstance(it.get("reveal"), dict) and it["reveal"].get("method_steps"):
                continue
            st = MF.steps(it)
            if not st:
                skipped.append(r["id"]); continue
            kt = re.sub(r"[^\d/]", "", qa.key_text(it).split(" ")[0])
            assert kt and kt in re.sub(r"[^\d/ ]", "", st["5_solve_by_hand"]).split() or kt in re.sub(r",", "", st["5_solve_by_hand"]), (r["id"], kt, st["5_solve_by_hand"])
            if r["status"] == "draft":
                it["reveal"]["method_steps"] = st; changed = True; done["draft_in_place"] += 1
            else:
                p = copy.deepcopy(it)
                p.update({"id": it["id"] + "-R1" if not it["id"].endswith("-R1") else it["id"] + "b", "replaces": it["id"], "status": "draft",
                          "review_status": "unreviewed", "reviewer": None, "reviewed_at": None,
                          "notes": f"Method-first explanation proposal for {it['id']} (original status: {r['status']}); content and key unchanged. 22 Oct 2026."})
                p["reveal"]["method_steps"] = st
                props.append(p); done[f"r1_{r['status']}"] += 1
        if changed:
            Path(f).write_text(json.dumps(d, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    if props:
        R1.write_text(json.dumps({"date": "2026-10-22", "note": "Proposals only: never approved, signed or imported by the bank worker.", "items": props},
                                 ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"applied": dict(done), "no_template_yet": len(skipped), "skipped_ids": skipped[:20]}, indent=1))


if __name__ == "__main__":
    main()
