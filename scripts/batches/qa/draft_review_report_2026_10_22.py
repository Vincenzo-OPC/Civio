#!/usr/bin/env python3
"""Render docs/research/DRAFT_REVIEW_QUEUE_2026-10-22.md from the queue CSV and JSON. Run after draft_review_queue_2026_10_22.py."""
import csv, collections, json

s = json.load(open("docs/research/bank/draft-review-queue-2026-10-22.json"))
r = list(csv.DictReader(open("docs/research/bank/draft-review-queue-2026-10-22.csv")))
retired = json.load(open("docs/research/bank/retired/filler-clones-2026-10-22.json"))
D = ["general_information", "clerical", "numerical", "analytical", "verbal_en", "verbal_fil"]
N = dict(zip(D, ["GI", "Clerical", "Numerical", "Analytical", "Verbal EN", "Verbal Fil"]))
t = collections.defaultdict(collections.Counter)
files = collections.defaultdict(collections.Counter)
for x in r:
    t[x["domain"]][x["result"]] += 1
    t[x["domain"]][x["kind"]] += 1
    files[x["file"].split("/")[-1]][x["result"]] += 1
ap, rec, add = s["approved_by_domain"], s["recommended_by_domain"], s["adds_unique_pass_by_domain"]
P, T, S = s["projected_if_signed"], s["targets"], s["shortfall"]
gib = [x for x in r if x["domain"] == "general_information" and x["kind"] == "baseline"]
desc = {
    "missing_est_seconds": "Baseline-550 rows outside GI still have no difficulty or est_seconds (metadata only).",
    "near_dup_approved": "Lint-fix revisions close to the approved item they fix. Expected, and not blocking for revisions.",
    "previously_rejected": "Already rejected in the ChatGPT batch 002/003 reviews.",
    "near_dup_draft": "Near-duplicate of another draft.",
    "passage_missing_or_unlinked": "Baseline reading item with no linked passage.",
    "circular_reveal": "The explanation only restates the key (`civio-final-rewrite`).",
    "duplicate_options": "Two identical options, e.g. CIVIO-CLEAN-0060 with \"liaison\" twice.",
    "template_stem_place_name": "\"…for use in an official <City> document\": the place name adds nothing.",
    "key_not_in_reveal": "Numerical baseline items whose explanation never states the answer.",
    "gi_citation_doubt": "Wrong R.A. 6713 section: nepotism as §7(a) (it is EO 292 §59), share conflicts as §7(b) (§9 divestment), late SALN with a remedy §8 does not give.",
    "superseded_by_lintfix": "A baseline row has a lint-fixed revision. Review that instead.",
    "hold_phrase_overlap": "Baseline GI 0006 (the R.A. 6713 title) and 0056 (the Art. II §1 quote) share 20–30% of their 5-grams with a HOLD file. That is public statutory text, but a human must confirm.",
    "percent_change_topic": "Information only: the bank is already over the percent-change cap of 40.",
    "difficulty_vs_time": "Information only: the label and the time disagree.",
}
L = ["# Draft review queue (22 Oct 2026, updated after clone retirement and baseline GI fix)\n",
     "Mechanical QA of every non-approved item in the bank JSON. **No status was changed to approved and no content was rewritten.** GT-approved changes in this pass:\n",
     f"- **Retired {retired['count']} filler clones** to `docs/research/bank/retired/filler-clones-2026-10-22.json` (status `retired`, reason `filler_clone`, `clone_of` recorded). One representative per group stays in its source file.",
     f"- **Baseline GI (134 rows):** HOLD-screened against all 9 HOLD files, with `CSE Reviewer.pdf` read by OCR. No verbatim match. 2 rows are flagged `hold_phrase_overlap`. Difficulty and est_seconds were added by rule: 114 easy at 30 s and 20 medium at 45 s, within the approved GI range of 20–70 s. Fact spot-check: SALN timing (30 days, April 30, 30 days after separation), 15 working days, three signatories and Art. VII §19 impeachment all match R.A. 6713 §§5 and 8 and the 1987 Constitution. Status stays draft. Result: {sum(1 for x in gib if x['result']=='pass')} pass, {sum(1 for x in gib if x['result']=='flag')} flag.\n",
     "Script: `scripts/batches/qa/draft_review_queue_2026_10_22.py`, rendered by `draft_review_report_2026_10_22.py`. Per-item CSV: `docs/research/bank/draft-review-queue-2026-10-22.csv` (GI, then Clerical, then the rest).\n",
     f"## Scope\n\n{s['raw_non_approved_rows']} non-approved rows reduce to **{s['unique_drafts']} unique stems**. The approved unique count is **{s['approved_unique']}** (" + ", ".join(f"{N[d]} {ap.get(d,0)}" for d in D) + ").\n",
     "## Pass/flag by subject\n\n| Subject | Unique drafts | Pass | Flag | new | revision | rev. of approved | baseline |\n|---|---|---|---|---|---|---|---|"]
for d in D:
    v = t[d]
    L.append(f"| {N[d]} | {v['pass']+v['flag']} | {v['pass']} | {v['flag']} | {v['new']} | {v['revision']} | {v['revision_of_approved']} | {v['baseline']} |")
L.append("\n## Open defects\n")
for k, v in s["flag_counts"].items():
    if k in desc:
        L.append(f"- `{k}` ({v}): {desc[k]}")
L.append("\nNot found: mojibake, \"(variant N)\", keys outside the options, HOLD-source markers, or arithmetic key errors in the computable items.\n")
L.append("## By file\n\n| File | Pass | Flag |\n|---|---|---|")
for f, v in sorted(files.items(), key=lambda kv: -(kv[1]["pass"] + kv[1]["flag"])):
    L.append(f"| {f} | {v['pass']} | {v['flag']} |")
L.append("\n## Recommended 'ready for CoS/GT sign-off' set (GT split)\n\nOrder: gap-fill-2000 files, then round-03 replacements, then baseline GI, then flat/rewrite files. Verbal takes English first. Rows are marked `recommended=yes`.\n")
L.append("| Subject | Approved | Passing adds available | Recommended | Projected if signed | Target | Shortfall |\n|---|---|---|---|---|---|---|")
rows = [("Verbal (EN+Fil)", ap.get("verbal_en", 0) + ap.get("verbal_fil", 0), add.get("verbal_en", 0) + add.get("verbal_fil", 0), rec.get("verbal_en", 0) + rec.get("verbal_fil", 0), "verbal")]
rows += [(N[d], ap.get(d, 0), add.get(d, 0), rec.get(d, 0), d) for d in ["numerical", "general_information", "analytical", "clerical"]]
for n, a, ad, rc, g in rows:
    L.append(f"| {n} | {a} | {ad} | {rc} | {P[g]} | {T[g]} | {S[g]} |")
tot = sum(P.values())
L.append(f"| **Total** | **{s['approved_unique']}** | | **{sum(rec.values())}** | **{tot}** | **2,000** | **{max(0,2000-tot)}** |\n")
L.append(f"Verbal split: EN {rec.get('verbal_en',0)} + Fil {rec.get('verbal_fil',0)}. GI draws on baseline rows: about {sum(1 for x in r if x['recommended']=='yes' and x['kind']=='baseline')} of the {rec.get('general_information',0)} recommended GI items.\n")
L.append("## Next\n\n1. Fix the R.A. 6713 citations and circular explanations (`civio-final-rewrite`, `civio-flat-2100`).\n2. A human checks the 2 `hold_phrase_overlap` rows.\n3. CoS reviews the recommended set by subject, then GT signs per batch. Nothing is activated before that.\n4. Baseline rows outside GI still need metadata before they can count.\n")
open("docs/research/DRAFT_REVIEW_QUEUE_2026-10-22.md", "w").write("\n".join(L))
print("\n".join(L[-14:]))
