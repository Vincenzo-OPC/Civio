"""General Information items, one per verified fact (gi_facts.F). Only verified lawphil.net URLs are used."""
from common import make
from gi_facts import F, C, R

WHY = {"GI-NEIGHBOR-NUMBER": "is a nearby number, but not the one in the text", "GI-WRONG-BODY": "names a different office or body",
       "GI-WHO-HOLDS-POWER": "names someone who does not hold this power", "GI-SIBLING-TERM": "is a related term, but not the one the text uses",
       "GI-SOUNDS-RIGHT": "sounds reasonable, but the text does not say it", "GI-OLD-RULE": "was the rule under an older charter, not the 1987 text",
       "GI-TERM-MATCH": "is one of the listed items, so it cannot be the exception", "GI-RIGHTS-APPLY": "is not what this provision covers",
       "GI-ENV-PRINCIPLE": "is not the right the text protects", "GI-DEADLINE-NUMBER": "is a deadline from a different provision"}
LAW = {C: "the 1987 Constitution", R: "R.A. 6713"}


def item(rng, iid, idx):
    src, cite, q, c, wr, ev, ex = F[idx]
    it = make(id=iid, track="both", domain="general_information", competency="Philippine Constitution" if src == C else
              "Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713)", concept=cite, micro_skill="recall a provision",
              archetype="GI-DEADLINE-NUMBER" if any(w[1] == "GI-NEIGHBOR-NUMBER" for w in wr) else "GI-TERM-MATCH", difficulty="medium", est=25,
              stem=q, correct=c, wrong=[(t, code, f"\"{t}\" {WHY[code]}.") for t, code in wr],
              terms=f"This item is about {LAW[src]}, {cite}.",
              shortcut=f"Tie the fact to its section: {cite}. {ex}",
              why_correct=f"\"{c}\" is right. {cite} says: \"{ev}\".", source=f"{LAW[src][0].upper() + LAW[src][1:]}, {cite}", url=src, rng=rng)
    it["_sig"] = "GI:" + q
    it["_fact"] = idx
    return it
