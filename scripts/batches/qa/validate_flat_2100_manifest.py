#!/usr/bin/env python3
"""Validate docs/research/bank/civio-flat-2100-manifest-2026-10-22.json. Run from the repo root. Exit 1 on any failure.

Checks:
- count is 2,100, and the domain totals match the targets
- ids and stems are unique
- every id resolves to exactly one item in its source_file, with matching domain and status, and its content hash matches
- no trim-list or retired id is present
- no item marked retire_on_signoff is itself in the manifest
- every replacement points back to the original it replaces
- the CSV matches the JSON
"""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from flat_2100_manifest_2026_10_22 import content_hash, norm, TARGETS, OUT_JSON, OUT_CSV, TRIM  # noqa: E402


def main():
    m = json.load(open(OUT_JSON, encoding="utf-8"))
    rows, errs = m["items"], []
    if len(rows) != 2100 or m["count"] != 2100:
        errs.append(f"count {len(rows)} != 2100")
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        errs.append("duplicate ids")
    per = {}
    for r in rows:
        per[r["domain"]] = per.get(r["domain"], 0) + 1
    if per != TARGETS:
        errs.append(f"domain totals {per} != {TARGETS}")
    trim = json.load(open(TRIM))
    banned = set(trim["trimmed_numerical_ids"]) | set(trim["trimmed_verbal_fil_ids"])
    retire = {r["retire_on_signoff"] for r in rows if r["retire_on_signoff"]}
    cache, stems = {}, set()
    for r in rows:
        p = r["source_file"]
        if p not in cache:
            d = json.load(open(p, encoding="utf-8"))
            cache[p] = d.get("items") if isinstance(d, dict) else d
        hit = [i for i in cache[p] if isinstance(i, dict) and i.get("id") == r["id"]]
        if len(hit) != 1:
            errs.append(f"{r['id']}: {len(hit)} matches in {p}"); continue
        i = hit[0]
        if content_hash(i) != r["content_sha256"]:
            errs.append(f"{r['id']}: hash mismatch")
        if i.get("domain") != r["domain"] or i.get("status") != r["status"]:
            errs.append(f"{r['id']}: domain/status drift")
        if i.get("status") == "retired" or r["id"] in banned:
            errs.append(f"{r['id']}: retired or trimmed")
        if r["id"] in retire:
            errs.append(f"{r['id']}: marked retire_on_signoff but still listed")
        if r["retire_on_signoff"] and r["retire_on_signoff"] not in (i.get("fix_of"), i.get("replaces")):
            errs.append(f"{r['id']}: replacement does not reference {r['retire_on_signoff']}")
        k = norm(i["stem"])
        if k in stems:
            errs.append(f"{r['id']}: duplicate stem")
        stems.add(k)
    with open(OUT_CSV, encoding="utf-8") as f:
        c = list(csv.DictReader(f))
    if [x["id"] for x in c] != ids or any(x["content_sha256"] != r["content_sha256"] for x, r in zip(c, rows)):
        errs.append("CSV does not match JSON")
    for e in errs[:50]:
        print("FAIL", e)
    print(f"{'FAIL' if errs else 'OK'}: {len(rows)} ids, domains {per}, {len(errs)} problems")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
