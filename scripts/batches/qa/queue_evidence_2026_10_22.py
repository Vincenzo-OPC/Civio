#!/usr/bin/env python3
"""Evidence pass over the pending queue (P2-P4) for GT directive 3 (c). For each item: how the key was verified
(independent solver / recipe solver / evidence sheet / none), qa.check_item problems, and quality heuristics
(key is the conspicuously longest option, absolute words, duplicate frame in the manifest, review notes).
Writes docs/research/review/queue-evidence-2026-10-22.json. Read-only on bank data."""
import collections, csv, json, re, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent.parent), str(Path(__file__).parent.parent / "audit"), str(Path(__file__).parent.parent / "drafts")]
import qa
sys.path.insert(0, str(Path(__file__).parent))
import adversarial_read_2026_10_22 as AR  # noqa: E402
import distractor_length_2026_10_22 as DL  # noqa: E402
import verified_keys_2026_10_22 as VK  # noqa: E402

MAN = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json"
DEC = "docs/research/review/packets-2026-10-22/decisions.csv"
OUT = "docs/research/review/queue-evidence-2026-10-22.json"
ABS = re.compile(r"\b(always|never|all|none|only|every|must)\b", re.I)


def frame(s):
    return re.sub(r"\d[\d,./]*|₱", "#", re.sub(r"\b[A-Z][a-z]+\b", "N", s.split("\n\n")[-1]))[:90]


def main():
    m = json.load(open(MAN, encoding="utf-8"))
    pr = {r["id"]: r for r in csv.DictReader(open(DEC, encoding="utf-8"))}
    cache, items = {}, []
    for r in m["items"]:
        f = r["source_file"]
        if f not in cache:
            d = json.load(open(f, encoding="utf-8")); cache[f] = {i["id"]: i for i in (d["items"] if isinstance(d, dict) else d) if isinstance(i, dict)}
        items.append((r, cache[f][r["id"]]))
    frames = collections.Counter(frame(i["stem"]) for _, i in items)
    out = []
    for r, it in items:
        p = pr.get(r["id"], {}).get("priority")
        if p not in ("P2", "P3", "P4"):
            continue
        try:
            errs = qa.check_item(it)
        except Exception as x:  # noqa: BLE001
            errs = [f"check_item crashed: {type(x).__name__}"]
        solver_ran = not any("solver could not" in e or "crashed" in e for e in errs) and (
            it.get("recipe", {}).get("op") not in (None, "judgment") or it["domain"] in ("numerical", "analytical", "clerical", "verbal_en"))
        sheet = VK.verify(it)
        judg = it.get("recipe", {}).get("op") == "judgment"
        how = ("none (judgment item)" if judg else "recipe solver" if it.get("recipe", {}).get("op") not in (None, "judgment") and solver_ran else
               "bank solver" if solver_ran and it["domain"] != "verbal_fil" and it["domain"] != "general_information" else
               "lawphil evidence" if it["domain"] == "general_information" and not any("GI" in e for e in errs) and (it.get("source_quote") or it.get("source_url")) else
               "evidence sheet" if sheet else "none (judgment item)")
        if sheet:
            errs = [e for e in errs if not re.search(r"GI key mismatch|GI url not verified|solver could not", e)]
        opts = {o["option_id"]: o["text"] for o in it["options"]}
        key = opts[it["answer_option_id"]]
        lens = sorted(len(t) for k, t in opts.items() if k != it["answer_option_id"])
        flags = []
        if len(key) > 1.6 * lens[-1] and len(key) > 30:
            flags.append("key is conspicuously the longest option")
        if ABS.search(key) and it["domain"] in ("verbal_en", "verbal_fil", "analytical"):
            flags.append("absolute word in key")
        if frames[frame(it["stem"])] >= 4 and it["domain"] in ("numerical", "general_information"):
            flags.append(f"shares a stem frame with {frames[frame(it['stem'])] - 1} other manifest items")
        row = {"id": r["id"], "priority": p, "domain": r["domain"], "status": r["status"], "source_file": r["source_file"],
               "key_check": how, "qa_errors": errs, "flags": flags, "review_notes": pr[r["id"]].get("review_notes", "")}
        if "D1022" in r["id"] and (how.startswith("none") or r["id"] in DL.LONGER):
            row["adversarial_read"] = AR.record(it)
        out.append(row)
    Path(OUT).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    c = collections.Counter((e["domain"], e["key_check"]) for e in out)
    print(len(out)); [print(k, v) for k, v in sorted(c.items())]
    print("qa errors:", sum(bool(e["qa_errors"]) for e in out), collections.Counter(x for e in out for x in e["qa_errors"]).most_common(6))
    print("flags:", collections.Counter(x.split(" with ")[0] for e in out for x in e["flags"]))


if __name__ == "__main__":
    main()
