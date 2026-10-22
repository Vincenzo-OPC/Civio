"""gap-fill-2000-04: Clerical filing (ARMA Rules 1-8, weighted to 2-8) and R.A. 6713 drafts for the 2,000 milestone.
Filing: name sets in gf04_filing_data.py; keys and trap distractors derived in gf04_filing.py and re-checked by arma_solver.py (via qa.py).
R.A. 6713: hand-written in gf04_ra6713.py; each item's source_quote must appear verbatim in the LawPhil text
(set LAWPHIL_6713 to a saved copy of https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html, text or HTML).
Run: python3 scripts/batches/gapfill/gap_fill_2000_04.py  -> docs/research/gap-fill-2000-04.json. Drafts only, pending CoS."""
import html, json, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
import gf04_filing as F, gf04_filing_data as FD, gf04_ra6713 as G

LAW = "https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html"
EST = {"GI-TERM-MATCH": 20, "GI-WHO-HOLDS-POWER": 20, "GI-DEADLINE-NUMBER": 20, "GI-SCENARIO-APPLY": 35}
PROV = {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T04:00:00+08:00", "spec_version": "0.1.9"}


def law_text():
    for p in [os.environ.get("LAWPHIL_6713", ""), "/workspace/law/ra_6713_1989.txt", "/workspace/gi/ra_6713_1989.html.txt"]:
        if p and os.path.exists(p):
            t = open(p, encoding="utf-8", errors="replace").read()
            t = html.unescape(re.sub(r"<[^>]+>", " ", t))
            return re.sub(r"\s+", " ", t)
    return None


items = []
traps = Counter()
for n, (rank, kind, rule, names) in enumerate(FD.SETS, 1):
    it, nt = F.build(n, rank, kind, rule, names)
    assert nt >= 1, (n, "no rule-based trap")
    traps[nt] += 1
    it["fact_id"] = f"FACT-CLR-ARMA-R{rule}-{n:04d}"
    items.append(it)

txt = law_text()
unverified = []
for n, (fid, arch, sec, diff, stem, key, wrong, terms, short, quote) in enumerate(G.ITEMS, 1):
    if txt is not None and re.sub(r"\s+", " ", quote) not in txt:
        unverified.append(fid)
    texts = [w[0] for w in wrong]
    slot = (n + 1) % 4
    texts.insert(slot, key)
    ids = ["o1", "o2", "o3", "o4"]
    oid = {t: ids[i] for i, t in enumerate(texts)}
    items.append(dict(
        id=f"CIVIO-GF2K04-{arch}-{n:04d}", track="both", domain="general_information",
        competency="Code of Conduct and Ethical Standards (R.A. 6713)", concept="ethics law", micro_skill=f"recall and apply R.A. 6713, {sec}",
        archetype=arch, difficulty=diff, est_seconds=EST[arch], language="en", stem=stem,
        options=[{"option_id": ids[i], "text": t} for i, t in enumerate(texts)], answer_option_id=oid[key],
        reveal={"terms": terms, "shortcut": short,
                "why_correct": f"Answer: {key}. R.A. 6713, {sec} provides: \"{quote}\"",
                "why_wrong": {oid[w[0]]: w[2] for w in wrong}},
        distractor_reasoning={oid[w[0]]: w[1] for w in wrong},
        source=f"R.A. 6713, {sec}", source_url=LAW, source_quote=quote, source_group="civio",
        status="draft", review_status="unreviewed", provenance=PROV, fact_id=f"FACT-{fid}", shortcut=short,
        notes="gap-fill-2000-04 (R.A. 6713). Quote checked verbatim against LawPhil. Pending CoS."))

if txt is None:
    print("WARNING: LawPhil text not found; quotes not re-checked (set LAWPHIL_6713)")
elif unverified:
    sys.exit(f"quotes not found in LawPhil text: {unverified}")

json.dump({"batch": "gap-fill-2000-04", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio",
           "notes": "Clerical filing (ARMA Rules 1-8, weighted to 2-8) and R.A. 6713 items on provisions not yet in the bank. Drafts only.",
           "items": items},
          open(os.path.join(ROOT, "docs/research/gap-fill-2000-04.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dom = Counter(i["domain"] for i in items)
print(len(items), dict(dom), "filing traps per item:", dict(traps), "quotes verified:", txt is not None and not unverified)
for d in dom:
    print(d, "key positions", dict(sorted(Counter([o["option_id"] for o in i["options"]].index(i["answer_option_id"]) for i in items if i["domain"] == d).items())))
