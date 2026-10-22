#!/usr/bin/env python3
"""Remaining non-GI baseline rows without difficulty (22 Oct 2026, GT approved: "Fill difficulty/est_seconds for the remaining
non-GI baseline rows: HOLD-screen first, content-check, flag failures, keep draft, revisions entries"). Run from the repo root.

Scope: items in baseline-550-spec with no difficulty, domain != general_information, and no qa_flags yet (rows that the
earlier VEN/NUM pass already flagged are left as they are). For each row:
  1. HOLD screen against the 9 local HOLD files: flag hold_phrase_overlap at >= 20% shared 5-grams or a verbatim stem of 4+ words.
  2. Content QA: 4 distinct options, key among them, no option artifacts (slash alternatives, stray notes, words inside
     numeric options), right language for the domain, arithmetic keys recomputed (CALC below), spelling target not used by
     another bank item, and the hand review in MANUAL (near-duplicates, broken codes, unclear relations, stem artifacts).
  3. A pass gets difficulty / est_seconds from the spec archetype targets (docs/CSE-Question-Design-Spec.md, archetype
     tables) and the approved norms, plus hold_screen, metadata_note and a revisions entry. A fail gets qa_flags + qa_note.
Status stays draft. The 2,100 manifest is not rebuilt (none of these rows is in it, and metadata is outside content_hash).
"""
from __future__ import annotations
import glob, json, re, subprocess
from fractions import Fraction as Fr
from pathlib import Path

SPEC = "docs/research/audit/data/baseline-550-spec-2026-10-18.json"
HOLD_GLOB = "/workspace/civio-external-reviewers/hold/*.txt"
TODAY = "2026-10-22"
HOLD_SRC = "9 HOLD files (Mutia-Tayone 255/300 and 2019/2020 compilations, CSEReviewer.com Pro/SubPro v1.0, CSE Reviewer.pdf via OCR)"
B = "CIVIO-BASELINE-"
MANUAL = {
    "0031": "option_artifact: 'Pilotist' is not a word", "0133": "near_dup: same relation as 0028 (worker : workplace, physician/teacher)",
    "0139": "option_artifact: slash alternatives in the key", "0140": "unclear_relation: hypothesis/experiment does not match verdict/trial",
    "0141": "option_artifact: slash alternatives in the key", "0151": "broken_code: FIRE = 1234 and LIFE = 5124 give F and I two codes",
    "0152": "near_dup: same syllogism form as 0143", "0165": "near_dup: same item as 0039 (25% of 200)",
    "0172": "near_dup: same data and question as 0163 (40 vs 60 share)", "0202": "near_dup: same frame as 0049 (daily wage x days)",
    "0203": "near_dup: same frame as 0048 (fare x passengers)", "0215": "near_dup: same concept as 0283 (cross-reference)",
    "0218": "near_dup: same item as 0273 (Lopez, Diana last)", "0249": "unclear_relation: seed grows into a tree, a foundation does not grow into a building",
    "0250": "option_artifact: slash alternatives in the key", "0252": "unclear_stem: the code premise is incoherent ('Monday has 8 letters')",
    "0255": "near_dup: same syllogism form as 0143", "0315": "unclear_relation: generous/giving is trait-to-act, cautious/careful is a synonym",
    "0317": "near_dup: same first pair as 0136 (blueprint : building)", "0322": "near_dup: same alternating pattern as 0149",
    "0344": "near_dup: same doubling series as 0046", "0345": "near_dup: same series as 0047 (2, 5, 10, 17, 26)",
    "0348": "near_dup: same squares series as 0268 and 0185", "0457": "wrong_domain: a fraction computation, not reading",
    "0467": "near_dup: same first pair as 0136 (blueprint : building)", "0469": "near_dup: same first pair as 0316 (thermometer : temperature)",
    "0471": "near_dup: same frame as 0147 (symbol plus/minus)", "0472": "near_dup: same +1 letter code as 0323",
    "0477": "near_dup: same form as 0328 (all X have a mark; K has none)", "0487": "near_dup: same item as 0262 (7/8 of 64)",
    "0494": "near_dup: same frame as 0198 (clerks, forms, hours)", "0500": "near_dup: same frame as 0276 (immediately before Surname, Maria)",
    "0503": "near_dup: same frame as 0280 (folder number filed before)", "0544": "near_dup: same frame as 0280 (folder number filed before)",
    "0504": "near_dup: same item as 0285 (approved travel claims label)", "0545": "near_dup: same frame as 0285 (most retrievable label)",
    "0505": "near_dup: same concept as 0289 (out-guide)", "0506": "near_dup: same concept as 0284 (terminal digit)",
    "0507": "near_dup: same concept as 0283 (cross-reference)", "0508": "near_dup: same frame as 0281 (chronological dates)",
    "0535": "near_dup: same frame as 0454 (who qualifies by deadline)",
    **{k: "stem_artifact: placeholder stem ('the selected term', 'Item N') with no word or sentence" for k in
       ("0509", "0510", "0511", "0512", "0513", "0514", "0515", "0516", "0517", "0518", "0546", "0547")},
}
# Arithmetic keys recomputed here (exact fractions), compared with the numeric part of the key text.
CALC = {
    "0038": Fr(60, 40) * 100, "0039": Fr(25, 100) * 200, "0040": Fr(100 - 80, 80) * 100, "0041": 15 + 27, "0042": Fr(96, 8), "0043": 7 * 9,
    "0044": 100 - 37, "0045": 15, "0046": 80, "0047": 17 + 9, "0048": 13 * 4, "0049": 800 * 5, "0050": 500 * Fr(90, 100), "0163": Fr(60, 100) * 100,
    "0164": Fr(70 + 80 + 90, 3), "0166": Fr(30, 120) * 100, "0168": sorted([3, 9, 5, 7, 11])[2], "0170": Fr(3, 12) * 100, "0181": Fr(60, 200) * 100,
    "0196": 29, "0197": Fr(180, 3), "0198": Fr(100, 5 * 2), "0199": 1200 * Fr(85, 100), "0200": 60 / Fr(1, 4), "0201": Fr(50 + 8, 2),
    "0204": 35 * Fr(2, 5), "0205": 5000 * Fr(6, 100) * 2, "0206": 2 * (12 + 5), "0207": Fr(36, 8), "0208": (100 - 40) * Fr(1, 2),
    "0209": 900 * Fr(3, 9), "0210": Fr(180, 12), "0254": 6 + 2 * 3, "0259": 250 - 200, "0260": Fr(90 * 2, 3), "0262": 64 * Fr(7, 8),
    "0263": 14, "0264": Fr(35, 10) * 60, "0265": 180 / Fr(120, 100), "0266": 20 + 5, "0267": 24 * 5, "0268": 49, "0269": Fr(90, 3 * 15) * 10,
    "0270": 30000 * Fr(12, 112), "0271": Fr(10, 4), "0272": Fr(2 * 10 + 3 * 20, 5), "0321": 4 + 7 * 4, "0324": 17 * 2 - 1,
    "0333": 180 - 120, "0334": 80000 * Fr(40, 100), "0335": Fr(24, 30) * 100, "0336": Fr(40 + 50 + 45 + 65, 4), "0337": Fr(5, 20) * 100,
    "0338": 200 * Fr(30, 100), "0339": Fr(48, 6) + 7 * 2, "0340": 240 * Fr(15, 100), "0341": 250 * Fr(3, 5), "0342": Fr(275, 100) + Fr(16, 10),
    "0346": Fr(3, 3), "0347": 34 + 32, "0350": 600 * Fr(108, 100), "0351": Fr(180, 3) * 5, "0352": 45 - 45 * Fr(2, 3), "0353": Fr(125, 5),
    "0473": 25 + 3, "0480": Fr(9, 36) * 100, "0481": 120000 * Fr(60, 100), "0483": Fr(15 + 15, 2), "0485": Fr(84, 7) + 6 * 3,
    "0486": 250 * Fr(18, 100), "0488": Fr(64, 10) - Fr(275, 100), "0489": 1500 * Fr(88, 100), "0490": 33 * 2 - 1, "0491": 20 + 10,
    "0492": Fr(12, 2), "0493": 24 * 2, "0495": 2400 * Fr(85, 100), "0496": Fr(210 * 2, Fr(35, 10)), "0497": 72 / Fr(3, 5),
    "0498": 18 - 18 * Fr(2, 3) - 4, "0537": Fr(18, 3) + 4, "0539": 50 - 32 - 8, "0540": 7 * 8 - 15, "0541": 55 - 25, "0542": Fr(240, 6) * 9,
    "0147": 8 + 3 - 2, "0167": max((Fr(400, 2), "Region X"), (Fr(300, 1), "Region Y"))[1], "0482": "One-fourth" if Fr(24 - 18, 24) == Fr(1, 4) else None,
    "0484": "One-fourth" if Fr(20, 80) == Fr(1, 4) else None,
}
HARD_SEQ = {"0047", "0196", "0266", "0267", "0347", "0490", "0491", "0541", "0324", "0473"}
MULTI = {"0200", "0201", "0204", "0208", "0209", "0265", "0269", "0270", "0272", "0496", "0497", "0498", "0339", "0485", "0352",
         "0167", "0334", "0336", "0481", "0483", "0168", "0338", "0539", "0164"}
DEFN = {"0026", "0027", "0131", "0161", "0258", "0212", "0213", "0215", "0216", "0217", "0278", "0288", "0290", "0283", "0289",
        "0505", "0507", "0261", "0171", "0169", "0453", "0325", "0023", "0114", "0117"}
FIL = re.compile(r"\b(ang|ng|mga|piliin|alin|wastong|pangungusap|ayos|basahin)\b", re.I)
ARTIFACT = re.compile(r"\((as written|informal|sic)\)|\s/\s|^\s|\bvon\b", re.I)


def toks(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def grams(t, n=5):
    return {" ".join(t[k:k + n]) for k in range(len(t) - n + 1)}


def keynum(t):
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", t)
    return Fr(m.group().replace(",", "")) if m else None


def bank_spell_targets(exclude):
    out = {}
    files = subprocess.run(["git", "ls-files", "docs"], capture_output=True, text=True).stdout.split()
    for p in files:
        if not p.endswith(".json") or "retired/" in p or "flat-2100-manifest" in p or "draft-review-queue" in p:
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for it in (d.get("items") if isinstance(d, dict) else d) or []:
            if isinstance(it, dict) and str(it.get("archetype", "")).startswith("CLR-SPELL") and it.get("id") not in exclude and it.get("options"):
                k = next((o["text"] for o in it["options"] if o["option_id"] == it.get("answer_option_id")), "")
                out.setdefault(k.lower(), set()).add(it["id"])
    return out


def rule(i):
    n, c, dom = i["id"][-4:], i.get("competency", ""), i["domain"]
    if dom == "numerical":
        if c == "Number sequence":
            return ("hard", 50, "second-order or combined rule") if n in HARD_SEQ else ("medium", 45, "single-rule series")
        if c == "Word problems":
            return ("medium", 75, "two or more steps") if n in MULTI else ("easy", 45, "one step")
        return ("medium", 40, "two operations or a reverse step") if n in MULTI else ("easy", 35, "single operation")
    if dom == "analytical":
        if c == "Word analogy":
            return ("easy", 25, "familiar relation")
        if c.startswith("Symbolic"):
            if n in HARD_SEQ:
                return ("medium", 50, "two-step series")
            if re.search(r"\b(all|some|no|only|if)\b", i["stem"], re.I) and not re.search(r"means|coded|code", i["stem"], re.I):
                return ("medium", 60, "syllogism or conditional")
            return ("easy", 40, "single rule (symbol, code or pattern)")
        if c.startswith("Identifying"):
            return ("easy", 30, "definition recall") if n in DEFN else ("medium", 60, "assumption or conclusion")
        return ("easy", 30, "reading a described chart") if n in DEFN else (("medium", 75, "two or more steps") if n in MULTI else ("easy", 45, "one step"))
    if dom == "clerical":
        if c == "Spelling":
            return ("easy", 20, "spelling in context") if re.search(r"_{3,}|phrase|sentence", i["stem"]) else ("easy", 15, "spelling recognition")
        if n in DEFN or not re.search(r"order|sequence|first|last|before|ascending|chronological", i["stem"], re.I):
            return ("easy", 30, "filing concept recall")
        if re.search(r"sequence|order is|order for|A-Z order", i["stem"], re.I):
            return ("medium", 60, "orders four entries")
        return ("easy", 40 if re.search(r"\d{2}", i["stem"]) else 45, "one placement decision")
    if dom == "verbal_fil":
        return ("medium", 30, "balarila")
    if c == "Reading comprehension":
        return ("easy", 30, "reading-skill definition") if n in DEFN else ("medium", 45, "one-sentence passage, detail or inference")
    if c == "Sentence structure":
        return ("easy", 40, "identifies a sentence type") if n in DEFN else ("medium", 40, "applied sentence structure")
    if c == "Paragraph organization":
        return ("easy", 25, "transition recall") if n in DEFN else ("medium", 45, "applies a paragraph principle")
    return ("medium", 30, "default")


def main():
    corpus = {p: grams(toks(open(p, encoding="utf-8", errors="ignore").read())) for p in sorted(glob.glob(HOLD_GLOB))}
    assert len(corpus) == 9, f"expected 9 HOLD files, found {len(corpus)}"
    flat = {p: " ".join(toks(open(p, encoding="utf-8", errors="ignore").read())) for p in corpus}
    raw = open(SPEC, encoding="utf-8").read()
    d = json.loads(raw)
    todo = [i for i in d["items"] if i["domain"] != "general_information" and not i.get("difficulty") and not i.get("qa_flags")]
    spell = bank_spell_targets({i["id"] for i in todo})
    counts = {"pass": 0, "fail": 0}
    for i in todo:
        n, dom = i["id"][-4:], i["domain"]
        opts = [o["text"] for o in i["options"]]
        t = toks(i["stem"] + " " + " ".join(opts))
        g = grams(t)
        frac = max((len(g & cg) / len(g) for cg in corpus.values()), default=0.0) if g else 0.0
        st = toks(i["stem"])
        verbatim = len(st) >= 4 and any(" ".join(st) in f for f in flat.values())
        fails = []
        if frac >= 0.2 or verbatim:
            fails.append(f"hold_phrase_overlap: shared 5-grams {frac:.2f}, verbatim stem {verbatim}")
        if len(opts) != 4 or len({o.strip().lower() for o in opts}) != 4:
            fails.append("options_shape: options are not 4 distinct texts")
        key = next((o["text"] for o in i["options"] if o["option_id"] == i["answer_option_id"]), None)
        if key is None:
            fails.append("key_missing")
        if any(ARTIFACT.search(o) for o in opts) and n not in MANUAL:
            fails.append("option_artifact: stray note, slash alternative or leading space in an option")
        if dom == "numerical" and any(re.search(r"\d", o) and re.search(r"\b(?!km|kg|m|L|liters?|hours?|pesos?)[a-z]{3,}\b", o) for o in opts):
            fails.append("option_artifact: words inside a numeric option")
        if dom == "verbal_en" and FIL.search(i["stem"] + " " + " ".join(opts)):
            fails.append("wrong_domain: the item is in Filipino")
        if n in CALC and key is not None:
            exp = CALC[n]
            ok = (key == exp) if isinstance(exp, str) or exp is None else (keynum(key) is not None and abs(keynum(key) - Fr(exp)) < Fr(1, 2))
            if not ok:
                fails.append(f"key_mismatch: key {key!r}, recomputed {exp}")
        if dom == "clerical" and i.get("competency") == "Spelling" and key and key.lower() in spell:
            fails.append(f"spelling_target_repeat: '{key}' is also the target of {sorted(spell[key.lower()])[0]}")
        if n in MANUAL:
            fails.append(MANUAL[n])
        i["hold_screen"] = {"date": TODAY, "sources": HOLD_SRC, "shared_5gram_fraction": round(frac, 2), "verbatim_stem": verbatim}
        if fails:
            i["qa_flags"] = sorted({f.split(":")[0] for f in fails})
            i["qa_note"] = f"{TODAY} screen: " + "; ".join(fails)
            i.setdefault("revisions", []).append({"date": TODAY, "approved_by": "GT", "change": "HOLD-screened; content QA failed (see qa_note); no metadata added; still draft."})
            counts["fail"] += 1
            print(i["id"], dom, "fail", "; ".join(fails), sep="\t")
            continue
        diff, secs, why = rule(i)
        prior = {"difficulty": i.get("difficulty"), "est_seconds": i.get("est_seconds")}
        i["difficulty"], i["est_seconds"] = diff, secs
        i["metadata_note"] = (f"difficulty/est_seconds added {TODAY} by rule (easy = recall or single step, medium = standard, hard = multi-step), "
                              f"from the spec archetype targets and approved norms for {dom} / {i.get('competency')}: {why}. The reviewer confirms.")
        i.setdefault("revisions", []).append({"date": TODAY, "approved_by": "GT", "change": "HOLD-screened, content QA passed, metadata added; still draft.", "prior": prior})
        counts["pass"] += 1
        print(i["id"], dom, "pass", f"{diff}/{secs}s", sep="\t")
    assert all(i["status"] == "draft" for i in todo)
    Path(SPEC).write_text(json.dumps(d, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    print("TOTAL", len(todo), counts)


if __name__ == "__main__":
    main()
