"""Adversarial content read (22 Oct 2026, 4:03 PM directive) of the 139 D1022 judgment items (106 Verbal EN, 33 Analytical)
and the 23 distractor-lengthened GI rows. Each item was attacked for: a second defensible answer, a key the passage does not
support, a faulty analogy relation, an invalid inference, a grammar error and a weak or giveaway distractor.
This is the author's own read, NOT an independent check: needs_human_read stays "yes" for every row."""

ATTACKS = {
    "ANA-ANALOGY": "relation stated and tested against all four pairs (reversed pair, same-topic pair, other-relation pair); one pair only keeps the relation and its order",
    "VEN-RC": "key located in the passage; each wrong option checked for partial support, overreach or an outside fact; main-idea keys tested against the whole passage",
    "VEN-PARA-INSERT": "the added sentence tried after every sentence; pronoun/connector reference must resolve in one slot only",
    "VEN-PARA-ORDER": "every option order read as a paragraph; connectors (this, also, therefore, another, since then) must fix one order",
    "GI": "key checked against the constitutional text; each lengthened wrong option checked so that the added words do not make it true or give the key away",
}

# id -> (finding, action). Ids not listed: no defect found.
FINDINGS = {
    "CIVIO-D1022-ANA-0038": ("second defensible answer: 'general : army' is also member : organized group, like soldier : battalion",
                             "repaired in the draft: distractor changed to 'army : navy' (a different relation)"),
    "CIVIO-D1022-ANA-0029": ("weak point: 'cold : hot' could be argued as lower to higher temperature, close to tepid : scalding",
                             "repaired in the draft: distractor changed to 'heat : thermometer' (a different relation)"),
    "CIVIO-D1022-VEN-INS-0008": ("logic error: 'Those children often had to walk' after 'Some children missed classes' says the children who missed class walked to class",
                                 "repaired in the draft: added sentence is now 'Others had to walk for an hour on the muddy road instead.'"),
    "CIVIO-D1022-VEN-INS-0012": ("second defensible answer: the health-certificate sentence fit after sentence 2 or after sentence 3",
                                 "repaired in the draft: the certificate rule became sentence 3 and the added sentence is now 'These fees pay for the lighting and cleaning of the promenade.', which fits only after the fee sentence"),
    "CIVIO-D1022-VEN-INS-0015": ("second defensible answer: the class-size sentence fit after sentence 1 or after sentence 2",
                                 "repaired in the draft: added sentence is now 'That is enough time, because each class has only fifteen learners.', which needs the four Saturdays of sentence 2"),
}

WATCH = {  # no defect, but a reviewer may want to look
    "CIVIO-D1022-VEN-PO-0002": "P-S-R-Q is readable; P-R-S-Q is better because 'As a result' must follow the reminder system, not the forgetting",
    "CIVIO-D1022-VEN-PO-0018": "Q-P-R-S is readable; Q-R-P-S is better because the fare check explains why complaints dropped",
    "CIVIO-D1022-VEN-PO-0025": "S-P-R-Q is readable; S-R-P-Q is better because 'also welcome' in Q must follow the users named in P",
    "CIVIO-D1022-VEN-PO-0013": "R-P-S-Q is readable; R-S-P-Q is better because S defines the agenda before P uses 'With it'",
}


def kind(it):
    a = it.get("archetype", "")
    for k in ("VEN-PARA-INSERT", "VEN-PARA-ORDER", "VEN-RC", "ANA-ANALOGY"):
        if a.startswith(k):
            return k
    return "GI" if it.get("domain") == "general_information" else a


def record(it):
    f, w = FINDINGS.get(it["id"]), WATCH.get(it["id"])
    return {"date": "2026-10-22", "by": "bank worker (author; not independent)", "attacks": ATTACKS.get(kind(it), "content read"),
            "result": "defect found and repaired" if f else ("no defect; watch note" if w else "no defect found"),
            "finding": f[0] if f else (w or ""), "action": f[1] if f else "", "needs_human_read": "yes"}
