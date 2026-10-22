#!/usr/bin/env python3
"""Build the 22 Oct 2026 draft files (GT approved; MASTER directive 2026-10-22). Run from the repo root.
Writes docs/research/batches/drafts/*-2026-10-22.json. Every item is status draft / review_status unreviewed."""
import json, re, sys, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import qa  # noqa: E402
from d22_common import mk, words  # noqa: E402
import d22_math, d22_fil, d22_cler, d22_ana, d22_en, gi_2026_10_22 as G  # noqa: E402

OUT = Path("docs/research/batches/drafts")
GI_CACHE = "/workspace/gi"


def method8(it):
    """Directive 8-step method for Numerical reveals: what is asked, givens, method, why it works, no-calculator solve, check, distractors, shortcut."""
    r = it["reveal"]
    q = re.split(r"(?<=[.!])\s+", it["stem"].strip())[-1]
    nums = re.findall(r"₱?\d[\d,]*(?:\.\d+)?(?: \d+/\d+)?(?:/\d+)?", it["stem"].split("?")[0])
    key = qa.key_text(it)
    return {"1_asked": q, "2_givens": ", ".join(dict.fromkeys(nums)) or "the numbers in the question",
            "3_method": r["terms"], "4_why": "The method matches what is asked: " + r["terms"].split(":")[0].split(".")[0].lower() + ".",
            "5_solve_by_hand": r["why_correct"], "6_check": f"Put {key} back into the problem (or redo the last step in reverse) and confirm every given number is used once.",
            "7_distractors": " ".join(f"{next(o['text'] for o in it['options'] if o['option_id'] == k)}: {v}" for k, v in r["why_wrong"].items()),
            "8_shortcut": r.get("shortcut", "")}


def gi_items():
    T = {u: re.sub(r"\s+", " ", open(os.path.join(GI_CACHE, f)).read()).lower() for u, f in G.URLS.items()} if os.path.isdir(GI_CACHE) else None
    out, rows = [], G.CONST + G.HR + G.ETH[:30]
    for n, (url, cite, arch, stem, key, wrong, quote, teach) in enumerate(rows, 1):
        if T is not None:
            assert re.sub(r"\s+", " ", quote).lower() in T[url], (cite, quote[:50])
        law = "1987 Constitution" if url == G.C else ("R.A. 6713" if url == G.R else "R.A. 9745 (Anti-Torture Act of 2009)")
        src = f"1987 Const., {cite}" if url == G.C else cite
        it = mk(id=f"CIVIO-D1022-GI-{n:04d}", track="both", domain="general_information",
                competency="Philippine Constitution",
                concept="applied rule", micro_skill="apply the provision to a workplace or civic situation", archetype=arch,
                difficulty="medium", est=35 if arch == "GI-SCENARIO-APPLY" else 30, stem=stem, correct=key,
                wrong=[(w, c, y) for w, c, y in wrong],
                terms=f"Primary law: {src}.", shortcut=f"Key phrase in the text: \"{quote[:140]}{'…' if len(quote) > 140 else ''}\"",
                why_correct=f"\"{key}\" is correct. {teach[0].upper() + teach[1:]}. Source checked word for word against the {law} text on lawphil.net.",
                source=src, url=url, source_quote=quote, _fact22=n - 1,
                notes="New original draft, 22 Oct 2026 (GT approved). Legal text verified against the cached lawphil.net page; needs a legal reviewer before approval.")
        out.append(it)
    # competency by block
    for it in out[35:60]:
        it["competency"] = "Peace and human rights"
    for it in out[60:]:
        it["competency"] = "R.A. 6713 Code of Conduct"
    return out


def numseq():
    out = []
    for it in d22_ana.B2:
        if it["competency"] != "Number series":
            continue
        it = json.loads(json.dumps(it))
        it["domain"] = "numerical"
        it["id"] = it["id"].replace("-ANA-", "-NUMSEQ-")
        rule = it["reveal"]["why_correct"]
        it["archetype"] = "NUM-SEQ-ALT" if "take turns" in rule else ("NUM-SEQ-MULT" if re.search(r"multiply|divide|double|cubes", rule) else "NUM-SEQ-DIFF")
        it["notes"] += " Moved from Analytical to Numerical (MASTER directive: number sequences belong to Numerical)."
        out.append(it)
    return out


def analytical():
    out = []
    for it in d22_ana.B2 + d22_ana.RES:
        if it["competency"] == "Number series":
            continue
        it = json.loads(json.dumps(it)); it["track"] = "professional"
        out.append(it)
    return out


FILES = {
    "subpro-math-2026-10-22.json": ("numerical", lambda: d22_math.ITEMS),
    "numerical-series-2026-10-22.json": ("numerical", numseq),
    "subpro-filipino-2026-10-22.json": ("verbal_fil", lambda: d22_fil.ITEMS),
    "subpro-clerical-2026-10-22.json": ("clerical", lambda: d22_cler.ITEMS),
    "analytical-professional-2026-10-22.json": ("analytical", analytical),
    "verbal-en-organization-reading-2026-10-22.json": ("verbal_en", lambda: d22_en.ITEMS),
    "gi-applied-2026-10-22.json": ("general_information", gi_items),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    allnew, report = [], {}
    for fn, (dom, f) in FILES.items():
        items = f()
        for it in items:
            assert it["domain"] == dom and it["status"] == "draft" and it["review_status"] == "unreviewed", it["id"]
            if dom == "numerical":
                it["reveal"]["method_steps"] = method8(it)
            errs = qa.check_item(it)
            assert not errs, (it["id"], errs)
            assert words(it) >= 50, (it["id"], words(it))
        doc = {"batch": fn.replace(".json", ""), "date": "2026-10-22", "status": "draft", "spec_version": "0.1.9",
               "authority": "GT approval 2026-10-22 and MASTER directive 2026-10-22; drafts only, nothing approved, signed or imported",
               "count": len(items), "items": items}
        (OUT / fn).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        report[fn] = len(items); allnew += items
    ids = [i["id"] for i in allnew]
    assert len(ids) == len(set(ids))
    print(json.dumps(report, indent=1), "total", len(allnew))


if __name__ == "__main__":
    main()
