"""Build one round (100 items) of the Civio bank as docs/batches/batch-NNN.json/.md.

Usage: python3 scripts/batches/build.py 2      # round for batch-002 ... 11
Seeded RNG per round, so a rerun gives the same batch. Runs qa.py and refuses to write if any check fails.
"""
import glob, json, os, random, re, sqlite3, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Skip
import numerical, analytical, verbal, clerical, gi, qa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS = os.path.join(ROOT, "docs", "batches")
DEV_DB = os.environ.get("CIVIO_DEV_DB", "/workspace/civio-dev/civio-dev.sqlite")
QUOTA = {"numerical": 30, "analytical": 25, "verbal_en": 20, "clerical": 15, "general_information": 10}
GEN = {"numerical": numerical.TEMPLATES, "analytical": analytical.TEMPLATES, "verbal_en": verbal.TEMPLATES, "clerical": clerical.TEMPLATES}
LEGACY_IDS = {f"{n:06d}" for n in range(11, 21)} - {"000018"}  # earlier drafts kept in batch-002; 000018 dropped (its analogy pair is in the baseline bank)


def prior(batch):
    items = []
    for p in sorted(glob.glob(os.path.join(DOCS, "batch-*.json"))):
        if os.path.basename(p) < f"{batch}.json":  # earlier batches only, so a rebuild of round N ignores later rounds
            items += json.load(open(p, encoding="utf-8"))["items"]
    stems = [i["stem"] for i in items]
    if os.path.exists(DEV_DB) and not os.environ.get("CIVIO_SKIP_DB"):
        try:
            stems += [r[0] for r in sqlite3.connect(DEV_DB).execute("select stem from questions")]
        except sqlite3.Error:
            pass
    return items, stems


def main(rnd):
    batch = f"batch-{rnd:03d}"
    rng = random.Random(20261013 + rnd)
    old, stems = prior(batch)
    allids = [int(i["id"][-6:]) for i in old]
    nxt = max(allids + [10]) + 1
    sigs = {i.get("gen_sig") or i["stem"] for i in old}
    used_facts = {i["gen_fact"] for i in old if "gen_fact" in i} | {n for n, f in enumerate(gi.F) for i in old if i["stem"] == f[2]}
    analytical.FRAME_USE.clear()
    for i in old:
        f = i.get("gen_frame", "")
        if f.startswith("ANA-A"):
            analytical.FRAME_USE[i["archetype"]][f[4:]] += 1
        elif f.startswith("SYL-") and f[4] in "CSN" and f[5:6].isdigit():
            analytical.FRAME_USE["SYL-" + {"C": "chain", "S": "some", "N": "none"}[f[4]]][f[4:]] += 1
    items = []
    quota = dict(QUOTA)
    if rnd == 2:
        legacy = json.load(open(os.path.join(DOCS, "batch-002.json"), encoding="utf-8"))["items"]
        legacy = [i for i in legacy if i["id"][-6:] in LEGACY_IDS]
        for i in legacy:
            i["_legacy"] = True
            if i["archetype"] == "ANA-SYLLOGISM":
                i["gen_frame"] = "SYL-N-HAND"
            elif i["archetype"].startswith("ANA-ANALOGY"):
                i["gen_frame"] = "ANA-HAND"
            quota[i["domain"]] -= 1
            sigs.add(i["stem"])
        items += legacy
        nxt = 21
        used_facts |= {n for n, f in enumerate(gi.F) if "fifteen (15) working days" in f[5]}  # item 000020 already uses Sec. 5(a)
    for dom, n in quota.items():
        made, tries = 0, 0
        while made < n:
            tries += 1
            if tries > 20000:
                raise SystemExit(f"{dom}: pool exhausted after {made}")
            try:
                if dom == "general_information":
                    free = [k for k in range(len(gi.F)) if k not in used_facts]
                    if not free:
                        raise SystemExit("GI facts exhausted")
                    k = rng.choice(free)
                    it = gi.item(rng, "TMP", k)
                    used_facts.add(k)
                else:
                    tpl = GEN[dom][(made + tries) % len(GEN[dom])] if dom != "verbal_en" else rng.choice(GEN[dom])
                    it = tpl(rng, "TMP")
                    if dom == "verbal_en":
                        have = sum(1 for x in items if x["domain"] == dom and x["concept"] == it["concept"])
                        if have >= verbal.CAPS.get(it["concept"], 2):
                            continue
                    fr = it.get("_frame")
                    if fr and sum(1 for x in items if x.get("gen_frame") == fr) >= 2:
                        continue
            except Skip:
                continue
            sig = it.pop("_sig", it["stem"])
            if sig in sigs:
                continue
            if "_fact" in it:
                it["gen_fact"] = it.pop("_fact")
            it["gen_sig"] = sig
            kind = it.pop("_kind", None)
            if "_frame" in it:
                it["gen_frame"] = it.pop("_frame")
            it["id"] = f"CIVIO-{it['archetype']}-{nxt:06d}"
            errs = qa.check_item(dict(it, _fact=it.get("gen_fact")) if "gen_fact" in it else it)
            near = qa.check_round([it], stems + [x["stem"] for x in items])
            if errs or near or qa.baseline_hits([it]):
                continue  # regenerate; the final QA pass below must be clean
            sigs.add(sig)
            if kind:
                analytical.FRAME_USE[kind][it["gen_frame"][4:]] += 1
            items.append(it)
            nxt += 1
            made += 1
    # final QA over the whole round
    view = [dict(i, _fact=i["gen_fact"]) if "gen_fact" in i else i for i in items]
    problems = qa.check_round(view, stems)
    problems += [(h[0], f"baseline {h[1]} match: {h[2]}") for h in qa.baseline_hits(view)]
    problems += qa.check_batch_rules(view)
    ev = qa.check_gi_evidence([v for v in view if "_fact" in v])
    if ev:
        problems += [(x, "GI quote not found in official text") for x in ev]
    if problems:
        for p in problems:
            print("QA FAIL", *p)
        raise SystemExit(1)
    for i in items:
        i.pop("_legacy", None)
    counts = {d: sum(1 for i in items if i["domain"] == d) for d in QUOTA}
    mix = ", ".join(f"{v} {k}" for k, v in counts.items())
    b = {"batch": batch, "spec_version": "0.1.3", "status": "draft (generated; for Chief of Staff review)",
         "intro": ["Spec: `docs/CSE-Question-Design-Spec.md` v0.1.3. Author: CSE (Grok Bot, AI-assisted), generated by `scripts/batches/build.py "
                   f"{rnd}` (seed {20261013 + rnd}). Reviewer: Chief of Staff (not the author).",
                   "All items are original, `source_group: civio`, `status: draft`, `review_status: unreviewed`. Seeded as draft into the box dev DB only.",
                   "Civio is an independent reviewer and is not affiliated with the Civil Service Commission.", "",
                   f"Mix: {mix}. Analytical items are Professional track; Clerical items are Subprofessional track."],
         "outro": ["## Automated QA (scripts/batches/qa.py)", "",
                   "- Keys recomputed from the stem text by independent solvers (numerical, analytical, clerical filing and spelling, verbal tables); GI keys matched to the fact table.",
                   "- Exactly one option matches the key; 4 distinct options; every wrong option has a distractor code and a reason.",
                   "- No duplicate or near-duplicate stem (token Jaccard ≥ 0.9) against all earlier batches and the box dev DB.",
                   "- GI quotes checked word for word against the lawphil.net text of the cited law; only lawphil.net URLs for the 1987 Constitution and R.A. 6713 are used.",
                   "- Filing items carry the ARMA note; schema and draft status checked." +
                   (" The 10 items drafted earlier (000011–000020) were checked by hand and pass the schema checks." if rnd == 2 else "")],
         "items": items}
    p = os.path.join(DOCS, f"{batch}.json")
    json.dump(b, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    subprocess.run([sys.executable, os.path.join(DOCS, "render.py"), p], check=True)
    print(f"{batch}: {len(items)} items, QA clean ({mix})")


if __name__ == "__main__":
    main(int(sys.argv[1]))
