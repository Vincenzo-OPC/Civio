#!/usr/bin/env python3
"""Sign-off sample fixes, 22 Oct 2026 (GT approved). Run once from the repo root.

Draft items are edited in place, and each change adds a `revisions` entry.
Approved items stay as they are; each gets a corrected draft replacement
(<id>-R1, `replaces` = original id) in
docs/research/audit/fixes/signoff-replacements-2026-10-22.json.
The flat-2100 manifest marks the original as retire_on_signoff.
Nothing is approved, signed, or imported.
"""
from __future__ import annotations
import copy, json, re
from pathlib import Path

TODAY = "2026-10-22"
LAWPHIL_6713 = "https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html"
OUT = Path("docs/research/audit/fixes/signoff-replacements-2026-10-22.json")
VFIL_INSTR = "Ano ang kasingkahulugan ng salitang nasa malalaking titik? "


def load(p):
    raw = open(p, encoding="utf-8").read()
    d = json.loads(raw)
    for ind in (2, 1):
        if json.dumps(d, ensure_ascii=False, indent=ind) in (raw, raw.rstrip("\n")):
            return d, ind, raw.endswith("\n")
    raise SystemExit(f"cannot round-trip {p}")


def save(p, d, ind, nl):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=ind) + ("\n" if nl else ""), encoding="utf-8")


def find(d, iid):
    hit = [i for i in d["items"] if i.get("id") == iid]
    assert len(hit) == 1, iid
    return hit[0]


def note(i, change, prior, source=None):
    r = {"date": TODAY, "approved_by": "GT", "change": change, "prior": prior}
    if source:
        r["source"] = source
    i.setdefault("revisions", []).append(r)


def sub_all(obj, old, new):
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, list):
        return [sub_all(x, old, new) for x in obj]
    if isinstance(obj, dict):
        return {k: sub_all(v, old, new) for k, v in obj.items()}
    return obj


# ---------- drafts edited in place ----------
SPELL_STEM = "Which word is spelled correctly?"
DRAFT_EDITS = {
    "docs/research/civio-flat-2100-2026-10-22.json": [
        (x, "stem", SPELL_STEM, "Word-level spelling item: the sentence- or line-style stem was replaced with the standard spelling instruction.")
        for x in ("CIVIO-2100-0061", "CIVIO-2100-0064", "CIVIO-2100-0075", "CIVIO-2100-0079", "CIVIO-2100-0090", "CIVIO-2100-0095", "CIVIO-2100-0099")
    ],
    "docs/research/gap-fill-2000-02.json": [
        ("CIVIO-GF2K02-NUMOPS-0050", "stem", "What is the value of 69 × (19 − 2) + 11?", "Punctuation: the command 'Find the value of … ?' became a question."),
    ],
    "docs/research/chatgpt-batch-002.json": [
        ("CIVIO-VEN-ERROR-AGREE-050061", "stem", "Which version uses correct grammar?", "Removed the scenario lead-in, which has nothing to do with the grammar point."),
        ("CIVIO-VEN-ERROR-MODIFIER-050090", "stem", "Which sentence follows the appropriate grammar rule?", "Removed the scenario lead-in, which has nothing to do with the grammar point."),
    ],
}
B3_FILE = "docs/research/audit/fixes/round-03-baseline-b3-drafts.json"
B3_ID = "CIVIO-B3-GI-SCENARIO-APPLY-0072"
B3_TERMS = ("Conflict of interest (Sec. 3(i)): an official's private interest in a business, as a board member, officer, "
            "substantial stockholder, owner or holder of a substantial interest, may be opposed to or affected by the faithful "
            "performance of official duty.")
B3_WHY = ("Answer: A conflict of interest. Her shares give her a financial interest in a supplier whose bid her own office will "
          "decide, so her private interest can be affected by her official duty (Sec. 3(i)). The item does not depend on whether "
          "20% makes her a \"substantial stockholder\" (Sec. 3(f): enough shares to elect a director). Sec. 7(a) bars any financial "
          "or material interest in a transaction requiring her office's approval, and Sec. 9 requires divestment when a conflict arises.")
LINTFIX_FILE = "docs/research/audit/fixes/gap-fill-2000-06-lintfix.json"
VFIL_LINTFIX = ["CIVIO-VFIL-20261013-00%02d-LINTFIX" % n for n in (2, 5, 6, 7, 10)]

# ---------- approved items: corrected draft replacements ----------
ARTICLE = {  # id -> file
    **{f"CIVIO-NUM-WP-PCT-CHANGE-000{n}": f"docs/batches/batch-0{b}.json" for n, b in
       [("221", "04"), ("323", "05"), ("423", "06"), ("517", "07"), ("528", "07"), ("537", "07"), ("623", "08"), ("725", "09"),
        ("727", "09"), ("822", "10"), ("825", "10"), ("917", "11"), ("924", "11")]},
    **{f"CIVIO-NUM-WP-GEOM-000{n}": f"docs/batches/batch-0{b}.json" for n, b in
       [("226", "04"), ("534", "07"), ("736", "09"), ("838", "10"), ("920", "11"), ("934", "11")]},
}
SYLLOGISM = {  # id -> (file, nonsense term, replacement term)
    "CIVIO-ANA-SYLLOGISM-000053": ("docs/batches/batch-002.json", "rentals", "exports"),
    "CIVIO-ANA-SYLLOGISM-000643": ("docs/batches/batch-008.json", "imported goods", "landmarks"),
    "CIVIO-ANA-SYLLOGISM-000655": ("docs/batches/batch-008.json", "items marked for repair", "export products"),
    "CIVIO-ANA-SYLLOGISM-000853": ("docs/batches/batch-010.json", "gifts from the province", "pond-raised stock"),
    "CIVIO-ANA-SYLLOGISM-000966": ("docs/batches/batch-011.json", "second-hand goods", "market items"),
}
RATE = ("CIVIO-NUM-WP-RATE-000116", "docs/batches/batch-003.json")
VFIL_APPROVED = ["CIVIO-VFIL-20261013-00%02d" % n for n in (1, 3, 4, 8, 9)]
VFIL_FILE = "docs/research/filipino-supplement-001.json"
STRIP = ("reviewer", "reviewed_at", "review_line", "previous_review", "gen_sig")


def replacement(orig, change):
    r = copy.deepcopy(orig)
    for k in STRIP:
        r.pop(k, None)
    r["id"] = orig["id"] + "-R1"
    r["status"] = "draft"
    r["review_status"] = "unreviewed"
    r["fix_of"] = orig["id"]
    r["replaces"] = orig["id"]
    r["retire_on_signoff"] = orig["id"]
    r["revisions"] = [{"date": TODAY, "approved_by": "GT", "change": change,
                       "prior": {"id": orig["id"], "stem": orig["stem"], "options": orig["options"], "reveal": orig.get("reveal")}}]
    return r


def main():
    for p, edits in DRAFT_EDITS.items():
        d, ind, nl = load(p)
        for iid, field, new, why in edits:
            i = find(d, iid)
            assert i.get("status") == "draft", iid
            if new == SPELL_STEM:  # bank convention: list the words in the stem
                new = SPELL_STEM + "  " + " | ".join(o["text"] for o in i["options"])
            if i[field] != new:
                note(i, why, {field: i[field]})
                i[field] = new
        save(p, d, ind, nl)

    d, ind, nl = load(B3_FILE)
    i = find(d, B3_ID)
    assert i["status"] == "draft"
    if i["reveal"].get("why_correct") != B3_WHY:
        note(i, "Explanation no longer calls a 20% holding a 'substantial stockholder'. It now rests on financial interest: Sec. 3(i), Sec. 7(a), Sec. 9.",
             {"reveal": copy.deepcopy(i["reveal"])}, LAWPHIL_6713)
        i["reveal"]["terms"], i["reveal"]["why_correct"] = B3_TERMS, B3_WHY
    save(B3_FILE, d, ind, nl)

    d, ind, nl = load(LINTFIX_FILE)
    for iid in VFIL_LINTFIX:
        i = find(d, iid)
        assert i["status"] == "draft"
        if not i["stem"].startswith(VFIL_INSTR):
            note(i, "Added the missing instruction to the stem.", {"stem": i["stem"]})
            i["stem"] = VFIL_INSTR + i["stem"]
    save(LINTFIX_FILE, d, ind, nl)

    out = []
    cache = {}
    def orig(iid, p):
        if p not in cache:
            cache[p] = load(p)[0]
        o = find(cache[p], iid)
        assert o["status"] == "approved", iid
        return o
    for iid, p in ARTICLE.items():
        o = orig(iid, p)
        r = replacement(o, "Article: 'A' became 'An' before a vowel sound ('A edging' became 'Edging').")
        r["stem"] = re.sub(r"\bA edging\b", "Edging", r["stem"])  # mass noun: no article
        r["stem"] = re.sub(r"\bA (?=[aeiouAEIOU])", "An ", r["stem"])
        assert r["stem"] != o["stem"], iid
        out.append(r)
    for iid, (p, bad, good) in SYLLOGISM.items():
        o = orig(iid, p)
        r = replacement(o, f"Swapped the template filler '{bad}' for a sensible category, '{good}'. Changed 'who' to 'that' for things. The logic and key are unchanged.")
        for k in ("stem", "options", "reveal"):
            r[k] = sub_all(r[k], bad, good)
        r["reveal"] = sub_all(r["reveal"], " who are ", " that are ")
        assert bad not in json.dumps(r["stem"]) + json.dumps(r["options"]), iid
        out.append(r)
    o = orig(*RATE)
    r = replacement(o, "Swapped the implausible '5 minutes' distractor for '7 hours', the difference of the two times.")
    opt = [x for x in r["options"] if x["text"] == "5 minutes"][0]
    opt["text"] = "7 hours"
    r["reveal"]["why_wrong"][opt["option_id"]] = "7 hours subtracts the two times (28 − 21). Add the work done per hour; do not subtract the hours."
    r.setdefault("distractor_reasoning", {})[opt["option_id"]] = "NUM-OP-SWAP"
    out.append(r)
    for iid in VFIL_APPROVED:
        o = orig(iid, VFIL_FILE)
        r = replacement(o, "Added the missing instruction to the stem.")
        r["stem"] = VFIL_INSTR + r["stem"]
        out.append(r)

    OUT.write_text(json.dumps({
        "batch": "signoff-replacements-2026-10-22",
        "status": "draft (pending CoS; not approved, not signed, not imported)",
        "note": "Corrected draft replacements for approved items found in the 22 Oct sign-off sample and the pattern scan. "
                "Originals are unchanged; the flat-2100 manifest lists them as retire_on_signoff.",
        "count": len(out), "items": out}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "replacements")


if __name__ == "__main__":
    main()
