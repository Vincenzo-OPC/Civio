#!/usr/bin/env python3
"""Build the flat-2100 manifest (22 Oct 2026). Run from the repo root after draft_review_queue_2026_10_22.py.

Domain targets (CoS/tracker definition): Numerical, Analytical and Verbal EN 400 each; Verbal Fil, Clerical and GI 300 each.
The rule is deterministic and fills each domain in tier order until it reaches its target:
  T1 approved: unique by normalized stem; ties go to the first file in sorted git order.
     If a corrected draft replacement exists, it takes the original's slot and the original goes to retire_on_signoff.
  T2 reviewed (queue result = pass)
  T3 passing unique drafts (queue result = pass, adds_unique = yes). civio-flat-2100 goes first, then the queue's file priority, then id.
  T4 legacy baseline drafts whose only queue flags are metadata gaps (difficulty or est_seconds). Tagged needs_metadata.
Always excluded: the trim lists, the superseded clone files (civio-exact-flat-cleaned, civio-fixed-flat-final, civio-final-rewrite), retired items, any other queue flag (near-dups, previously rejected, missing passage,
duplicate options and so on), and percent-change items above the Numerical cap of 40 (MILESTONE_2000_PLAN.md).
content_sha256 is sha256 of the item's canonical JSON (sorted keys, compact): domain, track, language, stem, options,
answer_option_id, reveal. It is a manifest checksum, not BankContent::fingerprint.
"""
from __future__ import annotations
import collections, csv, hashlib, json, re, subprocess
from pathlib import Path

TARGETS = {"numerical": 400, "analytical": 400, "verbal_en": 400, "verbal_fil": 300, "clerical": 300, "general_information": 300}
PCT_CAP = 40
OUT_JSON = Path("docs/research/bank/civio-flat-2100-manifest-2026-10-22.json")
OUT_CSV = Path("docs/research/bank/civio-flat-2100-manifest-2026-10-22.csv")
QUEUE = Path("docs/research/bank/draft-review-queue-2026-10-22.csv")
TRIM = Path("docs/research/civio-trim-lists-2026-10-22.json")
REPL_FILE = "docs/research/audit/fixes/signoff-replacements-2026-10-22.json"
# LINTFIX drafts that already carry the same fix as the sign-off scan (missing VFIL instruction).
LINTFIX_SUBS = ["CIVIO-VFIL-20261013-00%02d" % n for n in (2, 5, 6, 7, 10)]
META_ONLY = {"missing_difficulty", "missing_est_seconds", "bad_difficulty", "difficulty_vs_time", "percent_change_topic"}
PCT_STEM = re.compile(r"percent(age)? (increase|decrease|change)|(increase|decrease|rise|drop|grew|fell)[sd]? by \d+(\.\d+)? ?%|by what percent|% off|discount", re.I)
SKIP = ("draft-review-queue", "baseline-550-2026-10-17", "retired/", "curriculum/data", "gi-currency", "exact-flat-cleaned",
        "fixed-flat-final", "final-rewrite", "flat-2100-manifest")
PRIO = ["civio-flat-2100", "gap-fill-2000-", "round-03-baseline", "baseline-550-spec", "batch-subpro", "original-foundations", "chatgpt-batch"]


def norm(s):
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


def content_hash(i):
    keep = {k: i.get(k) for k in ("domain", "track", "language", "stem", "options", "answer_option_id", "reveal")}
    return hashlib.sha256(json.dumps(keep, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def is_pct(i):
    return "PCT-CHANGE" in (i.get("id") or "") or "PCT-CHANGE" in (i.get("archetype") or "") or bool(PCT_STEM.search(i["stem"]))


def tracked_items():
    files = sorted(p for p in subprocess.run(["git", "ls-files", "docs"], capture_output=True, text=True).stdout.split()
                   if p.endswith(".json") and not any(x in p for x in SKIP))
    for p in files:
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        it = d.get("items") if isinstance(d, dict) else d
        if isinstance(it, list):
            for i in it:
                if isinstance(i, dict) and i.get("stem") and i.get("id"):
                    yield p, i


def main():
    trim = json.load(open(TRIM))
    trimmed = set(trim["trimmed_numerical_ids"]) | set(trim["trimmed_verbal_fil_ids"])
    by_id = collections.defaultdict(list)
    for p, i in tracked_items():
        by_id[i["id"]].append((p, i))
    def first(iid, want_file=None):
        rows = [r for r in by_id[iid] if want_file is None or r[0] == want_file]
        return rows[0] if rows else None

    queue = {r["id"]: r for r in csv.DictReader(open(QUEUE, encoding="utf-8"))}
    subs = {}  # original id -> (file, replacement item)
    for p, i in by_id_items(by_id, REPL_FILE):
        subs[i["replaces"]] = (p, i)
    for oid in LINTFIX_SUBS:
        subs[oid] = first(oid + "-LINTFIX", "docs/research/audit/fixes/gap-fill-2000-06-lintfix.json")

    cand, excl = collections.defaultdict(list), []
    seen_stem = set()
    # T1 approved
    for p, i in sorted(((p, i) for rows in by_id.values() for p, i in rows if i.get("status") == "approved"), key=lambda r: (r[0], r[1]["id"])):
        k = norm(i["stem"])
        if k in seen_stem:
            continue
        seen_stem.add(k)
        if i["id"] in subs:
            rp, ri = subs[i["id"]]
            if queue.get(ri["id"], {}).get("result") != "pass":
                raise SystemExit(f"replacement {ri['id']} does not pass the queue")
            cand[ri["domain"]].append({"tier": 1, "file": rp, "item": ri, "retire_on_signoff": i["id"], "note": "replacement"})
        else:
            cand[i["domain"]].append({"tier": 1, "file": p, "item": i})
    # T2-T4 from the queue
    def rank(r):
        return (next((n for n, x in enumerate(PRIO) if x in r["file"]), 99), r["id"])
    repl_ids = {ri["id"] for _, ri in subs.values()}
    for r in sorted(queue.values(), key=rank):
        iid = r["id"]
        if iid in repl_ids:
            continue
        flags = {f.split(":")[0] for f in r["reasons"].split(";") if f and not f.startswith("also_in")}
        if iid in trimmed:
            excl.append((iid, r["domain"], "trim_list")); continue
        hit = first(iid, r["file"])
        if not hit:
            excl.append((iid, r["domain"], "superseded_clone_file")); continue
        if norm(hit[1]["stem"]) in seen_stem:
            excl.append((iid, r["domain"], "duplicate_stem")); continue
        tier, note = None, ""
        if r["status"] == "reviewed" and r["result"] == "pass":
            tier = 2
        elif r["result"] == "pass" and r["adds_unique"] == "yes":
            tier = 3
        elif r["kind"] == "baseline" and r["result"] == "flag" and flags and flags <= META_ONLY:
            tier, note = 4, "needs_metadata"
        if tier is None:
            excl.append((iid, r["domain"], "flag:" + ",".join(sorted(flags)) if r["result"] == "flag" else "revision_of_existing_item"))
            continue
        seen_stem.add(norm(hit[1]["stem"]))
        cand[r["domain"]].append({"tier": tier, "file": hit[0], "item": hit[1], "note": note})

    chosen, pct = [], 0
    for dom, target in TARGETS.items():
        # Stable sort on tier keeps the insertion order inside a tier: T1 by (file, id), T2-T4 by queue rank.
        rows = sorted(cand[dom], key=lambda c: c["tier"])
        n = 0
        for c in rows:
            i = c["item"]
            if dom == "numerical" and is_pct(i):
                if pct >= PCT_CAP:
                    excl.append((i["id"], dom, "percent_change_over_cap")); continue
                pct += 1
            if n >= target:
                excl.append((i["id"], dom, f"over_domain_target_tier{c['tier']}")); continue
            chosen.append((dom, c)); n += 1
        if n < target:
            raise SystemExit(f"{dom}: only {n} of {target}")

    rows_out = []
    for dom, c in chosen:
        i = c["item"]
        rows_out.append({"id": i["id"], "domain": dom, "track": i.get("track"), "status": i.get("status"), "tier": c["tier"],
                         "source_file": c["file"], "content_sha256": content_hash(i),
                         "retire_on_signoff": c.get("retire_on_signoff", ""), "note": c.get("note", "")})
    sub = collections.defaultdict(collections.Counter)
    for r in rows_out:
        sub[r["domain"]][r["track"]] += 1
    summary = {
        "manifest": "civio-flat-2100", "date": "2026-10-22", "count": len(rows_out), "targets": TARGETS,
        "by_domain": dict(collections.Counter(r["domain"] for r in rows_out)),
        "by_status": dict(collections.Counter(r["status"] for r in rows_out)),
        "by_tier": {str(k): v for k, v in sorted(collections.Counter(r["tier"] for r in rows_out).items())},
        "by_track": dict(collections.Counter(r["track"] for r in rows_out)),
        "track_by_domain": {d: dict(v) for d, v in sub.items()},
        "subprofessional_eligible": sum(1 for r in rows_out if r["track"] in ("subprofessional", "both")),
        "subprofessional_only": sum(1 for r in rows_out if r["track"] == "subprofessional"),
        "percent_change_numerical": pct, "percent_change_cap": PCT_CAP,
        "retire_on_signoff": sorted(r["retire_on_signoff"] for r in rows_out if r["retire_on_signoff"]),
        "exclusions_by_reason": dict(collections.Counter(e[2].split(":")[0] if e[2].startswith("flag") else e[2] for e in excl).most_common()),
        "exclusions": [{"id": a, "domain": b, "reason": c} for a, b, c in excl],
        "rule": __doc__.strip(),
        "status": "manifest only; nothing approved, signed or imported",
        "items": rows_out,
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()), lineterminator="\n")
        w.writeheader(); w.writerows(rows_out)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("items", "exclusions", "rule", "retire_on_signoff")}, indent=1))


def by_id_items(by_id, f):
    return [(p, i) for rows in by_id.values() for p, i in rows if p == f]


if __name__ == "__main__":
    main()
