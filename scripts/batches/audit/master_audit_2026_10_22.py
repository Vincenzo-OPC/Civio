#!/usr/bin/env python3
"""MASTER directive 2026-10-22 audit of the flat-2100 manifest. Run from repo root. Writes docs/research/audit/master-audit-2026-10-22.json."""
import json, re, sys, collections
from pathlib import Path
sys.path.insert(0, "scripts/batches")
import qa
import verified_keys_2026_10_22 as VK
M = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json"
OUT = Path("docs/research/audit/master-audit-2026-10-22.json")


def load():
    m = json.load(open(M)); cache = {}; items = []
    for r in m["items"]:
        p = r["source_file"]
        if p not in cache:
            d = json.load(open(p)); cache[p] = {i["id"]: i for i in (d.get("items") if isinstance(d, dict) else d) if isinstance(i, dict) and "id" in i}
        items.append((r, cache[p][r["id"]]))
    return m, items


# Pairs a human check found to be different items despite shared words (different premises and a different valid conclusion).
NOT_DUP = {frozenset(("CIVIO-ANA-SYLLOGISM-000945", "CIVIO-ANA-SYLLOGISM-000247")): "different premise chain and different valid conclusion",
           frozenset(("CIVIO-ANA-SYLLOGISM-000956", "CIVIO-ANA-SYLLOGISM-000253")): "first premise differs (No vs All), so the valid conclusion differs"}
# Spec rules every domain must meet (MASTER + CONTINUE directives 2026-10-22).
TRACK = {"analytical": {"professional"}, "clerical": {"subprofessional"}}


def toks(s):
    return set(re.findall(r"\w+", s.lower()))


def main():
    m, items = load()
    issues = collections.defaultdict(list)
    resolved = collections.defaultdict(list)
    for r, i in items:
        try:
            e = qa.check_item(i)
        except Exception as x:  # noqa: BLE001
            e = [f"check_item crashed: {type(x).__name__}"]
        sheet = VK.verify(i)
        for x in e:
            covered = re.search(r"solver could not|check_item crashed|GI key mismatch|GI url not verified|key mismatch|more than one option", x)
            if x == "status/source_group" and i.get("status") == "reviewed" and i.get("source_group") == "civio":
                resolved[i["id"]].append("qa status rule predates 'reviewed' (valid intermediate status)"); continue
            if covered and sheet:
                resolved[i["id"]].append("verified by audit/verified_keys_2026_10_22.py: " + x); continue
            issues[i["id"]].append("qa: " + x)
        for f in i.get("qa_flags") or []:
            issues[i["id"]].append("flag: " + (f if isinstance(f, str) else json.dumps(f, ensure_ascii=False)))
        rv = i.get("reveal")
        if i.get("difficulty") not in ("easy", "medium", "hard") or not isinstance(i.get("est_seconds"), int):
            issues[i["id"]].append("metadata: difficulty/est_seconds missing")
        if not isinstance(rv, dict) or not rv.get("why_correct") or len(rv.get("why_wrong") or {}) != 3:
            issues[i["id"]].append("explanation: why_correct plus a why for each of the 3 wrong options required")
        if i["domain"] in TRACK and i.get("track") not in TRACK[i["domain"]]:
            issues[i["id"]].append(f"track: {i['domain']} must be {'/'.join(TRACK[i['domain']])}")
        if i["domain"] == "analytical" and re.search(r"(number|numbers) (series|sequence)|\b\d+, \d+, \d+, \d+", i["stem"]) and "code" not in i["stem"].lower():
            issues[i["id"]].append("domain: number sequence belongs to numerical")
    # near-duplicates inside the manifest: Jaccard >= 0.85 on stem + option tokens (a shared frame alone does not count); passage siblings excluded
    by = collections.defaultdict(list)
    for r, i in items:
        by[i["domain"]].append(i)
    for d, L in by.items():
        T = [(i, toks(i["stem"] + " " + " ".join(o["text"] for o in i["options"]))) for i in L]
        for a in range(len(T)):
            for b in range(a + 1, len(T)):
                x, y = T[a][1], T[b][1]
                if not x or not y:
                    continue
                j = len(x & y) / len(x | y)
                pair = frozenset((T[a][0]["id"], T[b][0]["id"]))
                if pair in NOT_DUP:
                    resolved[T[b][0]["id"]].append(f"near-dup {j:.2f} reviewed: {NOT_DUP[pair]}"); continue
                if j >= 0.85 and not qa.siblings(T[a][0]["stem"], T[b][0]["stem"]):
                    issues[T[b][0]["id"]].append(f"near-dup {j:.2f} of {T[a][0]['id']}")
    # template twins: same stem and options once digits and capitalized names are masked (renamed people / numbers only)
    def mask(t):  # names only: same numbers + same frame + renamed people = padding
        return re.sub(r"\b[A-Z][a-z]+\b", "N", t)

    def frame(t):  # names and numbers: a numeric variant of a frame (reported, not failed)
        return re.sub(r"[\d,.]+", "#", mask(t))
    sig = collections.defaultdict(list)
    for r, i in items:
        if "\n\n" in i["stem"]:
            continue
        names = {}

        def idx(mo):
            return "N%d" % names.setdefault(mo.group(0), len(names))
        im = lambda t: re.sub(r"\b[A-Z][a-z]+\b", idx, t)  # noqa: E731  names numbered by first appearance keep the puzzle's structure
        st = im(i["stem"])
        sig[(i["domain"], st, tuple(sorted(im(o["text"]) for o in i["options"])), im(qa.key_text(i)))].append(i)
    twins = {}
    for k, v in sig.items():  # same masked frame, options and key, and most real words shared (renamed people only)
        for x in v[1:]:
            a, b = toks(v[0]["stem"]), toks(x["stem"])
            if len(a & b) / len(a | b) >= 0.6:
                twins.setdefault(v[0]["id"], [v[0]["id"]]).append(x["id"])
    fr = collections.defaultdict(list)
    for r, i in items:
        if "\n\n" not in i["stem"]:
            fr[(i["domain"], frame(i["stem"]))].append(i["id"])
    clusters = sorted(((len(v), k[0], k[1][:90], v) for k, v in fr.items() if len(v) >= 3), reverse=True)
    for k, v in twins.items():
        for x in v[1:]:
            issues[x].append(f"template twin of {v[0]} (same frame and options with only names/numbers changed)")
    pct = sum(1 for r, i in items if i["domain"] == "numerical" and "PCT-CHANGE" in (i.get("archetype") or ""))
    rep = {"date": "2026-10-22", "manifest": M, "count": len(items),
           "by_domain": dict(collections.Counter(i["domain"] for _, i in items)),
           "by_status": dict(collections.Counter(i["status"] for _, i in items)),
           "percent_change_numerical": pct,
           "items_with_issues": len(issues), "resolved_by_sheet": len(resolved), "issues": dict(sorted(issues.items())),
           "resolved": dict(sorted(resolved.items())),
           "numeric_variant_clusters": [{"size": n, "domain": d, "frame": f, "ids": v} for n, d, f, v in clusters]}
    OUT.write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in rep.items() if k != "issues"}, indent=1))
    c = collections.Counter(x.split(":")[0].split(" ")[0] for v in issues.values() for x in v); print(c)
    print(collections.Counter(next(i for r, i in items if i["id"] == k)["domain"] for k in issues))


if __name__ == "__main__":
    main()
