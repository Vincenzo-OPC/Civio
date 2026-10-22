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

WATCH = {}  # the 4 watch-noted ordering items were revised after GT's independent review (see GT_REVISE)

# GT's independent review (22 Oct, 4:18 PM): still ambiguous after the first repair, or a second coherent order.
# Revised again by the bank worker; recommendation stays "Revise" until a reviewer confirms one slot/order only.
GT_REVISE = {
    "CIVIO-D1022-VEN-INS-0015": "GT: the class-size sentence still fit after sentence 2 or 3. Rebuilt: sentence 3 is now 'On the first Saturday, learners set up their own email accounts.' and the added sentence is 'On the last Saturday, they fill out a sample online job application.', which must follow sentence 3 and precede 'these skills' in sentence 4",
    "CIVIO-D1022-VEN-PO-0002": "GT: P-S-R-Q was also coherent. Sentence S now reads 'Now a text arrives two days before each appointment, so parents no longer depend on those cards.', which needs the cards of R",
    "CIVIO-D1022-VEN-PO-0013": "GT: R-P-S-Q was also coherent. Sentence P now reads 'Because they know these topics in advance, members can prepare their reports ahead of time.', which needs the topics listed in S",
    "CIVIO-D1022-VEN-PO-0018": "GT: Q-P-R-S was also coherent. Sentence P now reads 'Because overcharging is now easy to spot, complaints about it dropped soon after the rule took effect.', which needs the fare check in R",
    "CIVIO-D1022-VEN-PO-0025": "GT: S-P-R-Q was also coherent. Sentence P now reads 'Thanks to the refrigerator, mothers who work at the capitol can store milk there during their breaks.', which needs the refrigerator named in R",
}


def kind(it):
    a = it.get("archetype", "")
    for k in ("VEN-PARA-INSERT", "VEN-PARA-ORDER", "VEN-RC", "ANA-ANALOGY"):
        if a.startswith(k):
            return k
    return "GI" if it.get("domain") == "general_information" else a


def record(it):
    f, w = FINDINGS.get(it["id"]), WATCH.get(it["id"])
    if it["id"] in GT_REVISE:
        f = ("found by GT's independent review, not by the author's read: " + GT_REVISE[it["id"]].split(". ")[0],
             "revised again in the draft: " + GT_REVISE[it["id"]].split(". ", 1)[1] + "; recommendation Revise until a reviewer confirms")
    return {"date": "2026-10-22", "by": "bank worker (author; not independent)", "attacks": ATTACKS.get(kind(it), "content read"),
            "result": ("revised after GT review; awaiting re-check" if it["id"] in GT_REVISE else "defect found and repaired") if f else ("no defect; watch note" if w else "no defect found"),
            "finding": f[0] if f else (w or ""), "action": f[1] if f else "", "needs_human_read": "yes"}
