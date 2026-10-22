#!/usr/bin/env python3
"""Draft review queue (22 Oct 2026): mechanical QA of every non-approved bank item.

This only flags items. It doesn't change any status, approve anything or rewrite content.
Run from the repo root.
Outputs: docs/research/bank/draft-review-queue-2026-10-22.csv plus a JSON summary.
"""
from __future__ import annotations
import csv, json, re, subprocess, collections
from pathlib import Path

CSV_OUT = Path("docs/research/bank/draft-review-queue-2026-10-22.csv")
SUM_OUT = Path("docs/research/bank/draft-review-queue-2026-10-22.json")
DOMAINS = ["general_information", "clerical", "numerical", "analytical", "verbal_en", "verbal_fil"]
CANON_TRACKS = {"professional", "subprofessional", "both"}
MOJIBAKE = re.compile("Ã|â€|Â|\ufffd|\\?\\?")
HOLD = re.compile(r"mutia|tayone|csereviewer|cse reviewer\.pdf|recalled|actual (cse|exam) item|leaked", re.I)
PCT_TAG = re.compile(r"percent", re.I)
PCT_STEM = re.compile(r"percent(age)? (increase|decrease|change)|(increase|decrease|rise|drop|grew|fell)[sd]? by \d+(\.\d+)? ?%|by what percent", re.I)
LATER_WINS = ["civio-flat-2100-2026-10-22.json"]  # newest flat file


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout


def norm(s):
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


def toks(s):
    return set(re.findall(r"\w+", (s or "").lower()))


def kind_of(path, item):
    if "baseline-550" in path:
        return "baseline"
    if item.get("fix_of") or "lintfix" in path or "round-03-baseline" in path:
        return "revision"
    return "new"


def num(s):
    f = re.fullmatch(r"\s*(-?\d+)\s*/\s*(\d+)\s*", str(s))
    if f:
        return int(f.group(1)) / int(f.group(2))
    m = re.fullmatch(r"\s*[₱P$]?\s*(-?[\d,]*\.?\d+)\s*(%|pesos?|sacks?|km|kg|hours?|days?|minutes?|years?|cm|m|items?)?\s*", str(s))
    return float(m.group(1).replace(",", "")) if m else None


# Cheap GI fact rules: (stem pattern, key must match, source)
GI_RULES = [
    (r"\b(annual|yearly|every year)\b.*\bSALN\b.*(deadline|on or before|filed|due)|\bSALN\b.*\b(annual|yearly|every year)\b.*(deadline|on or before|due|when)", r"april 30", "RA 6713 s.8: SALN on or before April 30"),
    (r"(act on|respond to).*(letters?|requests?|communications?).*(within|how many)", r"fifteen|15", "RA 6713 s.5(a): 15 working days"),
    (r"term of (office of )?the president", r"six|6", "1987 Const. Art. VII s.4"),
    (r"term of (office of )?(a )?senators?", r"six|6", "Art. VI s.4"),
    (r"term of (office of )?(the )?members? of the house", r"three|3", "Art. VI s.7"),
    (r"(minimum )?age.*(president|vice.?president)\b", r"forty|40", "Art. VII s.2-3"),
    (r"(minimum )?age.*senator", r"thirty.?five|35", "Art. VI s.3"),
    (r"(minimum )?age.*(house of representatives|district representative|congressman)", r"twenty.?five|25", "Art. VI s.6"),
    (r"how many (justices|members).*supreme court", r"fifteen|15", "Art. VIII s.4(1)"),
    (r"(retire|retirement age).*(justice|judge)", r"seventy|70", "Art. VIII s.11"),
    (r"bill of rights.*(article|found)|article.*bill of rights", r"\bIII\b|3", "Art. III"),
    (r"(right of )?suffrage.*(age|years old)|voting age", r"eighteen|18", "Art. V s.1"),
    (r"civil service commission.*article|article.*civil service commission", r"IX", "Art. IX-B"),
    (r"republic act no\.? 6713.*(known as|title)|code of conduct and ethical standards.*republic act", r"6713|code of conduct", "RA 6713"),
    (r"6713.*(enacted|approved|signed).*(year)|year.*6713.*(enacted|approved)", r"1989", "RA 6713 approved 20 Feb 1989"),
]


# R.A. 6713 section checks (text of R.A. 6713, 1989): s.7(a) financial/material interest in transactions,
# s.7(b) outside employment/private practice, s.7(c) confidential information, s.7(d) gifts,
# s.8 SALN and disclosure of relatives, s.9 divestment, s.11 penalties. Nepotism is Admin Code (EO 292) Bk V s.59.
RA6713_CITES = [
    (r"§\s*7\s*\(a\).*(spouse|cousin|relative|kin|brother|sister|son|daughter)", "nepotism is EO 292 s.59, not RA 6713 s.7(a)"),
    (r"§\s*7\s*\(b\).*\bshares?\b", "share conflicts fall under s.9 divestment, not s.7(b)"),
    (r"§\s*8\b.*(late|after the deadline)", "s.8 sets the duty and deadline, the remedy in the key is not in s.8"),
]


def items_of(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    it = d.get("items") if isinstance(d, dict) else d
    return [i for i in it if isinstance(i, dict) and i.get("stem")] if isinstance(it, list) else []


def main():
    files = [p for p in sh("git", "ls-files", "docs").split() if p.endswith(".json") and "draft-review-queue" not in p
             and "baseline-550-2026-10-17" not in p]  # raw legacy dump; the -spec file is the converted copy
    approved, approved_dom, pool = {}, collections.Counter(), {}
    for p in files:
        rows = items_of(p)
        if not rows:
            continue
        for i in rows:
            k = norm(i["stem"])
            if i.get("status") == "approved":
                if k not in approved:
                    approved[k] = i
                    approved_dom[i.get("domain")] += 1
    approved_toks = [(k, toks(k)) for k in approved]
    raw = 0
    for p in files:
        rows = items_of(p)
        if not rows:
            continue
        for i in rows:
            if i.get("status") == "approved":
                continue
            raw += 1
            k = norm(i["stem"])
            if k in approved:
                k = "REV:" + k + ":" + str(i.get("id"))  # revision of an approved item, same stem
            if k in pool and not any(p.endswith(x) for x in LATER_WINS):
                pool[k]["dup_files"].append(p)
                continue
            prev = pool.get(k, {}).get("dup_files", [])
            pool[k] = {"item": i, "file": p, "dup_files": prev + ([pool[k]["file"]] if k in pool else [])}
    # Lint-fix revisions supersede the draft they fix.
    fixed = {e["item"].get("fix_of") for e in pool.values() if e["item"].get("fix_of")}

    rows_out, stats = [], collections.defaultdict(collections.Counter)
    pool_fix = {e["item"].get("id"): e["item"].get("fix_of") for e in pool.values()}
    pool_list = list(pool.values())
    pool_toks = [toks(e["item"]["stem"]) for e in pool_list]
    skeletons, skeletons2 = {}, {}
    for idx, e in enumerate(pool_list):
        i, p = e["item"], e["file"]
        dom = i.get("domain", "?")
        kind = "revision_of_approved" if norm(i["stem"]) in approved else kind_of(p, i)
        flags = []
        if i.get("id") in fixed:
            flags.append("superseded_by_lintfix")
        for f in ["id", "track", "domain", "competency", "difficulty", "est_seconds", "options", "answer_option_id", "reveal"]:
            if f not in i or i[f] in (None, "", [], {}):
                flags.append(f"missing_{f}")
        if dom not in DOMAINS:
            flags.append("bad_domain")
        if i.get("track") not in CANON_TRACKS:
            flags.append(f"track_noncanonical:{i.get('track')}")
        if dom == "clerical" and i.get("track") == "professional":
            flags.append("clerical_professional_only")
        opts = i.get("options") or []
        if len(opts) != 4 or not all(isinstance(o, dict) and "option_id" in o and "text" in o for o in opts):
            flags.append("options_shape")
        else:
            texts = [re.sub(r"\s+", " ", str(o["text"]).strip().lower()) for o in opts]
            if len(set(texts)) != 4:
                flags.append("duplicate_options")
            if i.get("answer_option_id") not in {o["option_id"] for o in opts}:
                flags.append("key_not_in_options")
        blob = json.dumps(i, ensure_ascii=False)
        if MOJIBAKE.search(blob):
            flags.append("mojibake")
        if re.search(r"\(variant \d+\)", blob, re.I):
            flags.append("variant_clone")
        if HOLD.search(blob):
            flags.append("hold_source_red_flag")
        if i.get("review_status") == "rejected":
            flags.append("previously_rejected")
        t = toks(i["stem"])
        if len(t) >= 6:
            for k2, t2 in approved_toks:
                if len(t & t2) / len(t | t2) >= 0.9:
                    flags.append("near_dup_approved"); break
            for j in range(idx):
                t2 = pool_toks[j]
                if len(t2) >= 6 and len(t & t2) / len(t | t2) >= 0.9:
                    flags.append(f"near_dup_draft:{pool_list[j]['item'].get('id')}"); break
        d, s = i.get("difficulty"), i.get("est_seconds")
        if d not in {"easy", "medium", "hard"}:
            flags.append("bad_difficulty")
        elif isinstance(s, (int, float)) and ((d == "hard" and s <= 25) or (d == "easy" and s >= 90)):
            flags.append("difficulty_vs_time")
        tag = " ".join(str(i.get(x, "")) for x in ("archetype", "concept", "micro_skill", "competency"))
        if (PCT_TAG.search(tag) and re.search(r"change|increase|decrease", tag, re.I)) or PCT_STEM.search(i["stem"]):
            flags.append("percent_change_topic")
        key = next((o.get("text") for o in opts if isinstance(o, dict) and o.get("option_id") == i.get("answer_option_id")), None)
        # Arithmetic: direct expressions.
        m = re.search(r"(?:value of|Evaluate|Compute|Calculate|Simplify)\s*:?\s*([0-9 +\-−×÷*/().]+?)\s*[?.]?$", i["stem"].strip())
        if m and dom in ("numerical", "analytical") and re.search(r"\d", m.group(1)):
            try:
                v = eval(m.group(1).replace("×", "*").replace("÷", "/").replace("−", "-"), {"__builtins__": {}})
                kv = num(key)
                if kv is None or abs(kv - v) > 1e-6:
                    flags.append(f"arithmetic_key_mismatch:{v:g}")
            except Exception:
                pass
        mm = re.search(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(?:₱|P)?\s*([\d,]+(?:\.\d+)?)\s*\??$", i["stem"].strip())
        if mm and dom == "numerical":
            v = float(mm.group(1)) * float(mm.group(2).replace(",", "")) / 100
            kv = num(key)
            if kv is not None and abs(kv - v) > 1e-6:
                flags.append(f"percent_of_mismatch:{v:g}")
        # Reveal's final "= N" vs key (numerical only).
        rv = i.get("reveal")
        rtxt = json.dumps(rv, ensure_ascii=False) if not isinstance(rv, str) else rv
        if dom == "numerical" and key is not None and num(key) is not None:
            kt = str(key).strip().lstrip("₱P$").replace(",", "")
            kt = re.sub(r"\s*(%|pesos?|sacks?|km|kg|hours?|days?|minutes?|years?|cm|m|items?)$", "", kt)
            if kt and kt not in rtxt.replace(",", ""):
                flags.append(f"key_not_in_reveal:{kt}")
            if re.search(r"\d+\.\d+", rtxt) and re.search(r"sacks|people|persons|students|employees|items|boxes|chairs", i["stem"], re.I) and "." not in str(key):
                flags.append("non_integer_count_in_reveal")
        if re.search(r"reading|passage", str(i.get("competency", "")) + str(i.get("archetype", "")), re.I) and len(i["stem"]) < 180 and not i.get("passage") and not i.get("passage_id"):
            flags.append("passage_missing_or_unlinked")
        if dom == "general_information" and key:
            for pat, want, src in GI_RULES:
                if re.search(pat, i["stem"], re.I) and not re.search(want, str(key), re.I):
                    flags.append(f"gi_fact_doubt:{src}")
        if re.match(r"Select the correctly spelled word for use in an official [A-Z]", i["stem"]):
            flags.append("template_stem_place_name")
        if isinstance(rv, str) and key and re.search(r"requires?:\s*" + re.escape(str(key)[:40]), rv, re.I):
            flags.append("circular_reveal")
        skel = re.sub(r"\b[A-Z][a-z]+\b", "", i["stem"][1:])
        skel = re.sub(r"\W+", " ", skel.lower()).strip()
        skel += "|" + "|".join(sorted(re.sub(r"\s+", " ", str(o.get("text", "")).lower()) for o in opts if isinstance(o, dict)))
        if skel in skeletons and dom != "verbal_fil":
            flags.append(f"place_swap_clone:{skeletons[skel]}")
        else:
            skeletons.setdefault(skel, i.get("id"))
        skel2 = re.sub(r"\b[A-Z][a-zñ]+\b|[₱P]?[\d,]+(\.\d+)?|\([Ss]cenario \d+\)", "", i["stem"][1:])
        skel2 = re.sub(r"\W+", " ", skel2.lower()).strip() + "|" + str(key).lower()
        if skel2 in skeletons2 and dom != "verbal_fil" and num(key) is None and not any(f.startswith("place_swap_clone") for f in flags):
            flags.append(f"place_or_amount_swap_clone:{skeletons2[skel2]}")
        else:
            skeletons2.setdefault(skel2, i.get("id"))
        stem = i["stem"]
        for pat, why in RA6713_CITES:
            if re.search(pat, stem, re.I | re.S):
                flags.append(f"gi_citation_doubt:{why}")
        if e["dup_files"]:
            flags.append("also_in:" + "|".join(sorted(set(e["dup_files"]))))
        info_only = {"percent_change_topic", "difficulty_vs_time"}
        if kind in ("revision", "revision_of_approved"):
            info_only = info_only | {"near_dup_approved"}
        blocking = [f for f in flags if f.split(":")[0] not in info_only and not f.startswith("also_in")]
        result = "flag" if blocking else "pass"
        rows_out.append({"domain": dom, "id": i.get("id"), "file": p, "kind": kind, "track": i.get("track"),
                         "difficulty": d, "est_seconds": s, "status": i.get("status"), "review_status": i.get("review_status"),
                         "result": result, "reasons": ";".join(flags), "stem": i["stem"][:140].replace("\n", " / ")})
        stats[(dom, kind)][result] += 1
    # Recommended sign-off set toward GT's split (Verbal 600, Num 400, GI 400, Ana 300, Cler 300).
    # Counts only items that add a unique stem: passing new drafts, plus passing baseline replacements
    # (fix_of empty). Revisions of approved items replace, not add. Earlier pipeline files go first.
    targets = {"verbal": 600, "numerical": 400, "general_information": 400, "analytical": 300, "clerical": 300}
    group = lambda d: "verbal" if d.startswith("verbal") else d
    have = collections.Counter()
    for d, n in approved_dom.items():
        have[group(d)] += n
    prio = ["gap-fill-2000-", "round-03-baseline", "batch-subpro", "original-foundations", "civio-final-rewrite",
            "civio-exact-flat", "civio-flat-2100", "civio-fixed-flat", "chatgpt-batch"]
    def rank(r):
        return (next((n for n, x in enumerate(prio) if x in r["file"]), 99), r["id"] or "")
    adds = [r for r in rows_out if r["result"] == "pass" and (r["kind"] == "new" or (r["kind"] == "revision" and not pool_fix.get(r["id"])))]
    # Verbal: balance English first (smaller pool), then Filipino.
    adds.sort(key=lambda r: (r["domain"] != "verbal_en", rank(r)))
    for r in rows_out:
        r["adds_unique"] = "yes" if r in adds else "no"
        r["recommended"] = "no"
    for r in adds:
        g = group(r["domain"])
        if have[g] < targets[g]:
            r["recommended"] = "yes"
            have[g] += 1
    order = {d: n for n, d in enumerate(DOMAINS)}
    rows_out.sort(key=lambda r: (order.get(r["domain"], 99), r["kind"], r["result"], r["id"] or ""))
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader(); w.writerows(rows_out)
    flagc = collections.Counter(x.split(":")[0] for r in rows_out for x in r["reasons"].split(";") if x and not x.startswith("also_in"))
    summ = {"raw_non_approved_rows": raw, "unique_drafts": len(rows_out), "approved_unique": sum(approved_dom.values()),
            "approved_by_domain": dict(approved_dom),
            "recommended_by_domain": dict(collections.Counter(r["domain"] for r in rows_out if r["recommended"] == "yes")),
            "adds_unique_pass_by_domain": dict(collections.Counter(r["domain"] for r in rows_out if r["adds_unique"] == "yes")),
            "projected_if_signed": {g: have[g] for g in targets}, "targets": targets,
            "shortfall": {g: max(0, targets[g] - have[g]) for g in targets},
            "by_domain_kind": {f"{d}|{k}": dict(v) for (d, k), v in sorted(stats.items())}, "flag_counts": dict(flagc.most_common())}
    SUM_OUT.write_text(json.dumps(summ, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
