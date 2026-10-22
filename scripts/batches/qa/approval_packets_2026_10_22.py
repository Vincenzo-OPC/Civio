#!/usr/bin/env python3
"""Evidence-backed approval packets for the 723 pending rows (GT review, 22 Oct 2026, 4:18 PM). Replaces the P1-P4 packets.

Each packet holds 25-40 rows of ONE domain and ONE evidence type:
  solver-verified        the key was recomputed from the stem by code (recipe solver, bank solver or the hand-written
                         formula sheet audit/verified_keys_2026_10_22.py). Proves the arithmetic/rule, not the wording.
  law-text-verified      the key matches a verbatim quote found in the cached lawphil.net text. Proves the quote exists,
                         not that the paraphrase in the key is exact or that the law is unamended.
  human-judgment-needed  no machine can check the key (reading, analogy, Filipino usage). Only a human read decides.
Packets are ordered highest risk first. Every packet opens with a one-page summary: evidence, risks and the exact checks
a reviewer must make. Items are listed without keys; the answer sheet with keys, explanations and evidence is at the end,
so the reviewer solves first. A decision needs a reason per item (decision_by_human in the queue CSV). Nothing here approves.
Writes docs/research/review/approval-packets-2026-10-22/. Run from the repo root."""
import collections, csv, json, math, re, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).parent), str(Path(__file__).parent.parent)]
import qa  # noqa: E402

MAN = "docs/research/bank/civio-flat-2100-manifest-2026-10-22.json"
EV = "docs/research/review/queue-evidence-2026-10-22.json"
REC = "docs/research/review/queue-recommendations-2026-10-22.csv"
OUT = Path("docs/research/review/approval-packets-2026-10-22")
LO, HI = 25, 40
ETYPE = {"recipe solver": "solver-verified", "bank solver": "solver-verified", "evidence sheet": "solver-verified",
         "lawphil evidence": "law-text-verified", "none (judgment item)": "human-judgment-needed"}

PROVES = {
    "solver-verified": ("Code recomputed the key from the numbers/rule in the stem and it matched exactly one option.",
                        "It does not check the wording, realism of the scenario, distractor quality or the explanation."),
    "law-text-verified": ("A verbatim quote supporting the key was found in the cached lawphil.net text of the provision.",
                          "It does not prove the key's paraphrase is exact, that no other option is also true, or that the law is unamended."),
    "human-judgment-needed": ("Nothing machine-checked. The author (bank worker) read and attacked each item; GT's independent review already caught items the author missed.",
                              "The author's read is not independent. Treat every key as unconfirmed until you have solved the item yourself."),
}
CHECKS = {
    ("numerical", "solver-verified"): ["Solve each item on paper before the answer sheet; your answer must match the key.",
        "Exactly one option is correct, and each wrong option is a real mistake (not a random number).",
        "The scenario is realistic (ages, prices, quantities) and the stem has no ambiguity in units or rounding.",
        "method_steps teaches a no-calculator path a Subprofessional examinee can follow."],
    ("analytical", "solver-verified"): ["Solve first; for logic items, the conclusion must follow from the premises alone (no outside knowledge).",
        "For series/coding, the rule is the simplest one and gives exactly one next term.",
        "No wrong option is also defensible under a different but equally simple rule."],
    ("analytical", "human-judgment-needed"): ["State the stem relation in one sentence before looking at options.",
        "Exactly one pair keeps that relation AND its order; check reversed pairs and 'other relation' pairs that could be argued.",
        "Words are common enough for the CSE level; no regional or archaic sense needed."],
    ("clerical", "solver-verified"): ["Work the filing/copying task yourself; apply the ARMA rule named in the answer sheet.",
        "The rule gives one order only (watch prefixes, hyphens, numbers-as-words, identical names).",
        "Copy-check items: count the differences yourself; exactly one option matches."],
    ("general_information", "law-text-verified"): ["Open the source_url and find the quoted provision; read the whole section, not just the quote.",
        "The key's paraphrase says what the provision says (no narrowing or widening).",
        "No wrong option is also true under another provision or a later law; lengthened wrong options did not become true.",
        "The provision is current (no amendment or superseding law)."],
    ("verbal_en", "solver-verified"): ["Grammar/usage: confirm the key against a standard reference; exactly one option is correct in formal written English."],
    ("verbal_en", "human-judgment-needed"): ["Answer from the passage/sentences only, before the answer sheet.",
        "Insert items: try the sentence in every slot; it must fit one slot only (pronouns, 'also', 'these', time words).",
        "Order items: read every option order as a paragraph; only one may be coherent.",
        "Reading items: the key is stated or clearly implied; no wrong option is partly supported; main-idea keys cover the whole passage."],
    ("verbal_fil", "human-judgment-needed"): ["Sagutin muna bago tingnan ang susi.",
        "Iisa lang ang tamang sagot; walang ibang opsiyong maipagtatanggol.",
        "Wasto ang baybay at gamit ayon sa KWF; natural ang Filipino.",
        "Reading items: lengthened passages (GT 15:48) must not make a wrong option supported."],
}


def risk(r, e, it):
    """(score, reasons) - higher is riskier."""
    s, why = 0, []
    if r["recommendation"] == "Revise":
        s += 100; why.append("REVISE: revised after GT's independent review; confirm the fix")
    elif r["recommendation"] == "Accept revision":
        s += 50; why.append("revised content; compare with the original")
    ar = (e or {}).get("adversarial_read") or {}
    if ar.get("finding") and r["recommendation"] != "Revise":
        s += 20; why.append("adversarial read: " + ar["finding"][:140])
    if ETYPE.get((e or {}).get("key_check"), "solver-verified") == "human-judgment-needed":
        s += 30; why.append("key not machine-checkable")
    if "D1022" in r["id"]:
        s += 10; why.append("self-authored 22 Oct draft (author read only)")
    for f in (e or {}).get("flags", []):
        s += 10; why.append(f)
    if r["priority"] == "P1":
        s += 5; why.append("P1: one review pass done; this is the final decision")
    if it.get("domain") == "general_information":
        s += 15; why.append("legal content: paraphrase and currency must be checked")
    return s, why


def main():
    m = json.load(open(MAN)); man = {r["id"]: r for r in m["items"]}
    ev = {e["id"]: e for e in json.load(open(EV))}
    recs = list(csv.DictReader(open(REC)))
    cache = {}

    def item(i):
        f = man[i]["source_file"]
        if f not in cache:
            d = json.load(open(f)); cache[f] = {x["id"]: x for x in (d["items"] if isinstance(d, dict) else d) if isinstance(x, dict)}
        return cache[f][i]

    groups = collections.defaultdict(list)
    for r in recs:
        it, e = item(r["id"]), ev.get(r["id"])
        et = ETYPE[e["key_check"]] if e else "solver-verified"
        if it["domain"] == "general_information" and et == "solver-verified":
            et = "law-text-verified"  # GI evidence sheet = verbatim legal quotes checked against lawphil  # P1 rows: keys in the hand-checked formula sheet
        sc, why = risk(r, e, it)
        groups[(it["domain"], et)].append({"r": r, "it": it, "e": e, "score": sc, "why": why})
    packets = []
    for (dom, et), rows in groups.items():
        rows.sort(key=lambda x: (-x["score"], x["it"]["id"]))
        k = max(1, math.ceil(len(rows) / HI))
        size = math.ceil(len(rows) / k)
        for n in range(k):
            chunk = rows[n * size:(n + 1) * size]
            packets.append({"dom": dom, "et": et, "rows": chunk, "max": chunk[0]["score"], "mean": sum(x["score"] for x in chunk) / len(chunk)})
    packets.sort(key=lambda p: (-p["max"], -p["mean"]))
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.md"):
        f.unlink()
    index = []
    for n, p in enumerate(packets, 1):
        name = f"A{n:02d}-{p['dom']}-{p['et']}.md"
        rows = p["rows"]
        recc = collections.Counter(x["r"]["recommendation"] for x in rows)
        riskc = collections.Counter()
        for x in rows:
            for w in x["why"]:
                riskc[w.split(":")[0] if ":" in w else w] += 1
        proves, gap = PROVES[p["et"]]
        L = [f"# Packet A{n:02d}: {p['dom']}, {p['et']} ({len(rows)} items)", "",
             "## One-page summary", "",
             f"**Risk rank:** {n} of {len(packets)} (highest risk first). Highest item risk score {p['max']}, mean {p['mean']:.0f}.", "",
             f"**Evidence.** {proves}", "", f"**What the evidence does NOT show.** {gap}", "",
             f"**Bank worker's recommendations (not decisions):** " + ", ".join(f"{v} {k}" for k, v in recc.most_common()) + ".", "",
             "**Risks in this packet:**", ""]
        L += [f"- {v} × {k}" for k, v in riskc.most_common(8)]
        L += ["", "**You must check, for every item:**", ""] + [f"{i}. {c}" for i, c in enumerate(CHECKS[(p["dom"], p["et"])], 1)]
        top = [x for x in rows if x["score"] >= 50]
        if top:
            L += ["", "**Look hardest at:** " + "; ".join(f"{x['it']['id']} ({x['why'][0]})" for x in top[:8])]
        L += ["", "**How to decide.** Solve each item below before opening the answer sheet. For each item write Accept, Revise or Reject "
              "with a one-line reason in `decision_by_human` of `review/queue-recommendations-2026-10-22.csv`. "
              "A packet-level 'all accepted' without per-item reasons is not a review.", "", "---", "", "## Items (no keys)", ""]
        for i, x in enumerate(rows, 1):
            it = x["it"]
            L += [f"### {i}. {it['id']}  ({x['r']['status']}, {x['r']['priority']})", "", it["stem"], ""]
            L += [f"- {o['option_id']}: {o['text']}" for o in it["options"]]
            L += [""]
        L += ["---", "", "## Answer sheet and evidence (open only after solving)", "",
              "| # | id | key | evidence | risk notes | recommendation |", "|---|---|---|---|---|---|"]
        for i, x in enumerate(rows, 1):
            it, e = x["it"], x["e"]
            evid = (e["key_check"] if e else "hand-checked formula sheet") + (f"; {it.get('source_url')}" if it.get("source_url") else "")
            L.append(f"| {i} | {it['id']} | {it['answer_option_id']}: {qa.key_text(it)} | {evid} | {'; '.join(x['why']).replace('|', '/')} | {x['r']['recommendation']} |")
        L += ["", "### Explanations", ""]
        for i, x in enumerate(rows, 1):
            rv = x["it"]["reveal"]
            L.append(f"{i}. **{x['it']['id']}**: {rv.get('why_correct', '')}")
        (OUT / name).write_text("\n".join(L) + "\n", encoding="utf-8")
        index.append((name, len(rows), p["max"], round(p["mean"]), dict(recc)))
    sizes = [x[1] for x in index]
    R = ["# Approval packets, 22 Oct 2026", "",
         f"{sum(sizes)} pending rows in {len(index)} packets, highest risk first. Each packet is one domain and one evidence type "
         "and opens with a one-page summary of the evidence, the risks and what to check. These replace the earlier P1-P4 packets.", "",
         "| Packet | Items | Max risk | Mean risk | Recommendations |", "|---|---|---|---|---|"]
    R += [f"| [{a}]({a}) | {b} | {c} | {d} | {e} |" for a, b, c, d, e in index]
    R += ["", "Packet sizes outside 25-40: " + (", ".join(f"{a} ({b})" for a, b, *_ in index if not LO <= b <= HI) or "none") + "."]
    (OUT / "README.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    print(len(index), "packets", sorted(sizes))


if __name__ == "__main__":
    main()
