#!/usr/bin/env python3
"""MASTER directive 2026-10-22: swap known-defective or padding candidates out of the flat-2100 manifest and put QA-valid
22 Oct drafts in their place, one for one inside each domain. Edits the manifest rows in place (no rebuild), recomputes the
summary, appends a swap log, and rewrites the CSV. Idempotent: rows already swapped are skipped. Run from the repo root."""
import collections, csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from flat_2100_manifest_2026_10_22 import content_hash, OUT_JSON, OUT_CSV, TARGETS, PCT_CAP, is_pct  # noqa: E402

D = "docs/research/batches/drafts/"
NEW = {"analytical": [D + "analytical-professional-2026-10-22.json"], "clerical": [D + "subpro-clerical-2026-10-22.json"],
       "general_information": [D + "gi-applied-2026-10-22.json"], "verbal_en": [D + "verbal-en-organization-reading-2026-10-22.json"],
       "numerical": [D + "numerical-series-2026-10-22.json", D + "subpro-math-2026-10-22.json"]}
FLAT, BASE = "docs/research/civio-flat-2100-2026-10-22.json", "docs/research/audit/data/baseline-550-spec-2026-10-18.json"
GISUP = "docs/research/subprofessional-general-info-supplement-001.json"
REASON = {
    FLAT: "weak_explanation: one-line reveal string, no distractor codes or per-option why (fails qa.check_item)",
    BASE: "no_explanation: reveal.terms/shortcut empty and no distractor codes (fails qa.check_item)",
}
PADDING = {"CIVIO-NUM-FRAC-DEC-000713": "CIVIO-NUM-FRAC-DEC-000440", "CIVIO-NUM-WP-AVERAGE-000927": "CIVIO-NUM-WP-AVERAGE-000114",
           "CIVIO-NUM-WP-RATE-000931": "CIVIO-NUM-WP-RATE-000524", "CIVIO-NUM-WP-RATIO-000712": "CIVIO-NUM-WP-RATIO-000434",
           # same ordering puzzle (same relation graph, same asked place) with the people renamed; found by audit/master_audit_2026_10_22.py
           "CIVIO-ANA-CONCLUSION-000546": "CIVIO-ANA-CONCLUSION-000262", "CIVIO-ANA-CONCLUSION-000657": "CIVIO-ANA-CONCLUSION-000451",
           "CIVIO-ANA-CONCLUSION-000749": "CIVIO-ANA-CONCLUSION-000461", "CIVIO-ANA-CONCLUSION-000964": "CIVIO-ANA-CONCLUSION-000457",
           # same syllogism with one predicate noun swapped
           "CIVIO-ANA-SYLLOGISM-000342": "CIVIO-ANA-SYLLOGISM-000147"}
DISPUTED = ["CIVIO-GAP3-CLR-FILE-ORDER-00%d" % n for n in (17, 20, 21, 22, 23)]


def rr(items, key):
    """Round-robin by key so each domain gets a spread of formats, deterministic."""
    g = collections.defaultdict(list)
    for i in items:
        g[key(i)].append(i)
    out, ks = [], sorted(g)
    while any(g.values()):
        for k in ks:
            if g[k]:
                out.append(g[k].pop(0))
    return out


def main():
    m = json.load(open(OUT_JSON, encoding="utf-8"))
    rows = m["items"]
    done = {s["out"] for s in m.get("swaps_2026_10_22", [])}
    out_ids = {}
    for r in rows:
        if r["id"] in done:
            continue
        if r["source_file"] in REASON:
            out_ids[r["id"]] = REASON[r["source_file"]]
        elif r["id"] in PADDING:
            out_ids[r["id"]] = f"padding: same item as {PADDING[r['id']]} with only names, objects or one noun changed (kept the earlier twin)"
        elif r["id"] in DISPUTED:
            out_ids[r["id"]] = "disputed_filing_variant: bank ARMA solver disagrees with the key (punctuation/number/prefix variant); avoid disputed variants"
    # GI template supplement: keep the first item per law, swap the rest (five near-identical \"which law\" items per statute)
    seen = set()
    for r in rows:
        if r["source_file"] == GISUP and r["id"] not in done:
            it = next(i for i in json.load(open(GISUP))["items"] if i["id"] == r["id"])
            if it.get("source_url") in seen:
                out_ids[r["id"]] = "template_padding: repeated \"which law is R.A. X\" recall item for the same statute"
            seen.add(it.get("source_url"))
    need = collections.Counter(r["domain"] for r in rows if r["id"] in out_ids)
    inman = {r["id"] for r in rows}
    pool = {}
    for dom, files in NEW.items():
        its = [(f, i) for f in files for i in json.load(open(f))["items"] if i["id"] not in inman]
        pool[dom] = rr(its, key=lambda fi: (fi[0], fi[1]["archetype"]))
    log = m.setdefault("swaps_2026_10_22", [])
    for r in rows:
        if r["id"] not in out_ids:
            continue
        f, it = pool[r["domain"]].pop(0)
        log.append({"out": r["id"], "out_source": r["source_file"], "out_status": r["status"], "reason": out_ids[r["id"]],
                    "in": it["id"], "in_source": f})
        r.update({"id": it["id"], "track": it["track"], "status": it["status"], "tier": 4, "source_file": f,
                  "content_sha256": content_hash(it), "retire_on_signoff": "", "note": "d1022_replacement"})
    sub = collections.defaultdict(collections.Counter)
    for r in rows:
        sub[r["domain"]][r["track"]] += 1
    m.update({"count": len(rows), "by_domain": dict(collections.Counter(r["domain"] for r in rows)),
              "by_status": dict(collections.Counter(r["status"] for r in rows)),
              "by_tier": {str(k): v for k, v in sorted(collections.Counter(r["tier"] for r in rows).items())},
              "by_track": dict(collections.Counter(r["track"] for r in rows)), "track_by_domain": {d: dict(v) for d, v in sub.items()},
              "subprofessional_eligible": sum(1 for r in rows if r["track"] in ("subprofessional", "both")),
              "subprofessional_only": sum(1 for r in rows if r["track"] == "subprofessional")})
    pct = 0
    for r in rows:
        if r["domain"] == "numerical":
            d = json.load(open(r["source_file"])); L = d.get("items") if isinstance(d, dict) else d
            pct += is_pct(next(i for i in L if isinstance(i, dict) and i.get("id") == r["id"]))
    m["percent_change_numerical"] = pct
    assert pct <= PCT_CAP and m["by_domain"] == TARGETS, (pct, m["by_domain"])
    m["status"] = "manifest only; nothing approved, signed or imported. 22 Oct swaps: drafts in, see swaps_2026_10_22"
    OUT_JSON.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(json.dumps({"swapped_now": sum(need.values()), "by_domain": dict(need), "total_swaps": len(log), "pct": pct,
                      "by_status": m["by_status"]}, indent=1))


if __name__ == "__main__":
    main()
