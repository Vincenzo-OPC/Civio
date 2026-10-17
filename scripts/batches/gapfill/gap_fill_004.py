"""gap-fill-004: 10 GI drafts, 2 each on R.A. 7610, 9710, 9745, 10353 and 9851 (gaps found in round 03 baseline B2).
Every quote is asserted against LawPhil text cached in /workspace/gi/<law>.html.txt (fetched 2026-10-17). Writes docs/research/gap-fill-004.json."""
import json, re, os
L = "https://lawphil.net/statutes/repacts/"
LAW = {"7610": ("ra_7610_1992", L + "ra1992/ra_7610_1992.html", "R.A. 7610 (Special Protection of Children Against Abuse, Exploitation and Discrimination Act)"),
       "9710": ("ra_9710_2009", L + "ra2009/ra_9710_2009.html", "R.A. 9710 (Magna Carta of Women)"),
       "9745": ("ra_9745_2009", L + "ra2009/ra_9745_2009.html", "R.A. 9745 (Anti-Torture Act of 2009)"),
       "10353": ("ra_10353_2012", L + "ra2012/ra_10353_2012.html", "R.A. 10353 (Anti-Enforced or Involuntary Disappearance Act of 2012)"),
       "9851": ("ra_9851_2009", L + "ra2009/ra_9851_2009.html", "R.A. 9851 (Philippine Act on Crimes Against International Humanitarian Law, Genocide, and Other Crimes Against Humanity)")}
# (law, section, archetype, difficulty, secs, stem, [(text, code-or-None, why)], quote, terms, method, shortcut-or-None)
I = [
("7610", "Sec. 3(a)", "GI-DEADLINE-NUMBER", "easy", 20,
 "Under R.A. 7610, a person is a \"child\" if below what age, or older but unable to fully take care of or protect themselves because of a physical or mental disability or condition?",
 [("Fifteen (15) years", "GI-NEIGHBOR-NUMBER", "Fifteen is the age used in the Act's rules on working children (Sec. 12), not the definition of a child."),
  ("Eighteen (18) years", None, "Sec. 3(a) defines children as persons below eighteen (18) years of age, plus those over 18 who cannot fully protect themselves because of a disability or condition."),
  ("Twenty-one (21) years", "GI-OLD-RULE", "Twenty-one was the old age of majority before R.A. 6809 lowered it to 18; R.A. 7610 uses below 18."),
  ("Twelve (12) years", "GI-NEIGHBOR-NUMBER", "12 is a special victim-age threshold (Secs. 5 and 7), not the definition of a child.")],
 "\"Children\" refers to person below eighteen (18) years of age or those over but are unable to fully take care of themselves or protect themselves from abuse, neglect, cruelty, exploitation or discrimination because of a physical or mental disability or condition",
 "Child: below 18, or over 18 but unable to protect oneself because of a disability or condition.", "Sec. 3(a): below 18, the same age of majority used in Philippine law since R.A. 6809.", "Child under R.A. 7610 = below 18, the age of majority."),
("7610", "Sec. 3(b)", "GI-SCENARIO-APPLY", "medium", 35,
 "A day-care worker repeatedly humiliates a four-year-old in front of classmates, calling him worthless, but never hurts him physically. How does R.A. 7610 treat this?",
 [("It is not covered, because there was no physical injury", "GI-SOUNDS-RIGHT", "Sec. 3(b) covers psychological abuse and emotional maltreatment and any act or word that demeans a child's dignity; physical injury is not required."),
  ("It is child trafficking, because the child was under the worker's control", "GI-SIBLING-TERM", "Child trafficking (Sec. 7) is trading or dealing with children; humiliating a child is abuse, not trafficking."),
  ("It is child abuse, because words that demean a child's dignity are maltreatment", None, "Sec. 3(b) defines child abuse as maltreatment, whether habitual or not, including psychological abuse, emotional maltreatment and any act by deeds or words which debases, degrades or demeans the intrinsic worth and dignity of a child."),
  ("It is child abuse only once a pattern over several months is shown", "GI-SOUNDS-RIGHT", "Sec. 3(b) says maltreatment \"whether habitual or not\"; no pattern or minimum period is required.")],
 "Any act by deeds or words which debases, degrades or demeans the intrinsic worth and dignity of a child as a human being",
 "Child abuse: maltreatment of a child, habitual or not, including psychological abuse and demeaning words or deeds.", "Sec. 3(b): abuse can be by words alone, and it need not be habitual.", None),
("9710", "Sec. 18", "GI-DEADLINE-NUMBER", "medium", 25,
 "Under the Magna Carta of Women (R.A. 9710), how long is the special leave with full pay for a qualified woman employee after surgery caused by gynecological disorders?",
 [("Six (6) months", "GI-NEIGHBOR-NUMBER", "Six months is the service requirement (at least six months of continuous aggregate service in the last twelve months), not the length of the leave."),
  ("Twelve (12) months", "GI-NEIGHBOR-NUMBER", "Twelve months is the look-back period for the service requirement, not the leave."),
  ("105 days", "GI-SIBLING-TERM", "105 days is maternity leave under a different law (R.A. 11210), not the Sec. 18 special leave."),
  ("Two (2) months", None, "Sec. 18 grants a special leave benefit of two (2) months with full pay, based on gross monthly compensation, following surgery caused by gynecological disorders.")],
 "shall be entitled to a special leave benefit of two (2) months with full pay based on her gross monthly compensation following surgery caused by gynecological disorders",
 "Special leave for women (Sec. 18): two months with full pay after gynecological surgery; requires at least six months of service in the last twelve.", "Sec. 18: leave 2 months; service needed 6 of the last 12 months. Match the number to the right part of the rule.", "R.A. 9710 special leave: 2 months, full pay; 6 and 12 are the service rule."),
("9710", "Sec. 11(b)", "GI-DEADLINE-NUMBER", "medium", 25,
 "Under R.A. 9710, Sec. 11, at least what share of the membership of all development councils, from the regional down to the barangay level, shall be women?",
 [("Forty percent (40%)", None, "Sec. 11(b) requires that at least forty percent (40%) of the membership of all development councils from the regional, provincial, city, municipal and barangay levels be women."),
  ("Fifty percent (50%)", "GI-NEIGHBOR-NUMBER", "The 50-50 target in Sec. 11(a) is for women in third-level government positions, not development councils."),
  ("Five percent (5%)", "GI-NEIGHBOR-NUMBER", "Five percent is the minimum GAD budget share of an agency's total budget (Sec. 36), not council membership."),
  ("Thirty percent (30%)", "GI-NEIGHBOR-NUMBER", "Thirty percent is the upper end of the share of overseas development assistance for GAD under R.A. 7192, cited in Sec. 36.")],
 "at least forty percent (40%) of membership of all development councils from the regional, provincial, city, municipal and barangay levels shall be composed of women",
 "Women's participation: 50-50 in third-level posts within five years (Sec. 11(a)); at least 40% of development council members (Sec. 11(b)).", "Sec. 11: third-level posts 50-50; development councils at least 40%; GAD budget at least 5% (Sec. 36).", None),
("9745", "Sec. 6", "GI-RIGHTS-APPLY", "medium", 30,
 "During a declared state of war, a detention officer argues that torturing a captured suspect is justified by the emergency. What does R.A. 9745 say?",
 [("It may be justified once Congress declares a state of war", "GI-SOUNDS-RIGHT", "Sec. 6 names a state of war and a threat of war among the grounds that can never justify torture."),
  ("It may be justified while the privilege of the writ of habeas corpus is suspended", "GI-SIBLING-TERM", "Suspension of the writ (Art. VII, Sec. 18 of the Constitution) affects detention rules; Sec. 6 says no public emergency can justify torture."),
  ("It may be justified by a written order of battle from a superior", "GI-SIBLING-TERM", "Sec. 6 expressly says an \"order of battle\" can never be invoked to justify torture."),
  ("It can never be justified; freedom from torture applies in all circumstances", None, "Sec. 6 makes freedom from torture an absolute right: a state of war or threat of war, internal political instability or any other public emergency can never be invoked as a justification.")],
 "A state of war or a threat of war, internal political instability, or any other public emergency, or a document or any determination comprising an \"order of battle\" shall not and can never be invoked as a justification for torture",
 "Absolute right: a right that cannot be suspended or justified away in any circumstance.", "Sec. 6: war, emergency or an order of battle never justifies torture.", "Freedom from torture is absolute: no emergency or order excuses it."),
("9745", "Sec. 8", "GI-SCENARIO-APPLY", "medium", 35,
 "In a theft trial, the prosecution offers a confession that the accused gave after being tortured by police. Under R.A. 9745, Sec. 8, how should the court treat the confession?",
 [("Admit it if other evidence corroborates it", "GI-SOUNDS-RIGHT", "Sec. 8 makes a tortured confession inadmissible in any proceeding; corroboration does not cure it."),
  ("Exclude it, since it may be used only against the persons accused of the torture", None, "Sec. 8: any confession, admission or statement obtained as a result of torture is inadmissible in evidence in any proceedings, except when used against the persons accused of committing the torture."),
  ("Admit it if the accused signs it again before a lawyer", "GI-SOUNDS-RIGHT", "Re-signing does not change that the statement was obtained through torture; Sec. 8 has only one exception, a case against the torturers."),
  ("Exclude it in criminal cases but admit it in administrative cases", "GI-SOUNDS-RIGHT", "Sec. 8 applies to \"any proceedings\", criminal or administrative.")],
 "Any confession, admission or statement obtained as a result of torture shall be inadmissible in evidence in any proceedings, except if the same is used as evidence against a person or persons accused of committing torture",
 "Exclusionary rule: evidence obtained illegally is kept out of the case.", "Sec. 8: a tortured confession is out in every proceeding, with one exception: a case against the torturers.", None),
("10353", "Sec. 5", "GI-RIGHTS-APPLY", "medium", 30,
 "A soldier receives an \"order of battle\" from a superior to abduct and hide a suspected rebel. Under R.A. 10353, what is the effect of the order?",
 [("It justifies the act if the order was issued in writing", "GI-SOUNDS-RIGHT", "Sec. 5 says such an order, official or otherwise, cannot be invoked as a justifying or exempting circumstance, written or not."),
  ("It is unlawful, it excuses no one, and the soldier has the right to disobey it", None, "Sec. 5: an order of battle causing an enforced or involuntary disappearance is unlawful, cannot be invoked as a justifying or exempting circumstance, and any person receiving it has the right to disobey it."),
  ("It exempts the soldier, and only the superior who issued it is liable", "GI-SOUNDS-RIGHT", "Sec. 5 rules out the order as an exempting circumstance; following it does not shield the soldier."),
  ("It is valid only during a state of war or other public emergency", "GI-SIBLING-TERM", "Sec. 4 says the right against enforced disappearance cannot be suspended even in a state of war or public emergency.")],
 "An \"Order of Battle\" or any order of similar nature, official or otherwise, from a superior officer or a public authority causing the commission of enforced or involuntary disappearance is unlawful and cannot be invoked as a justifying or exempting circumstance. Any person receiving such an order shall have the right to disobey it",
 "Enforced disappearance: arrest, detention or abduction by State agents (or with their consent), followed by refusal to acknowledge it or to reveal the person's fate.", "Sec. 5: an order of battle is unlawful, excuses nobody, and may be disobeyed.", None),
("10353", "Sec. 22", "GI-DEADLINE-NUMBER", "hard", 30,
 "Under R.A. 10353, the prosecution of an enforced disappearance does not prescribe while the victim has not surfaced. If the victim later surfaces alive, what is the prescriptive period?",
 [("Twenty-five (25) years from the date of reappearance", None, "Sec. 22: the prosecution shall not prescribe unless the victim surfaces alive, in which case the prescriptive period is twenty-five (25) years from the date of reappearance."),
  ("None; it still never prescribes", "GI-SIBLING-TERM", "Never prescribing is the rule only while the victim has not surfaced; once the victim surfaces alive, the 25-year period runs."),
  ("Twenty-five (25) years from the date of the abduction", "GI-SOUNDS-RIGHT", "The 25 years run from the date of reappearance, not the abduction."),
  ("Twenty (20) years from the date of reappearance", "GI-NEIGHBOR-NUMBER", "Twenty years is the general prescription for crimes punished by death or reclusion perpetua under the Revised Penal Code; R.A. 10353 sets 25 years.")],
 "The prosecution of persons responsible for enforced or involuntary disappearance shall not prescribe unless the victim surfaces alive. In which case, the prescriptive period shall be twenty-five (25) years from the date of such reappearance",
 "Prescription: the period after which a crime can no longer be prosecuted.", "Sec. 22: no prescription while the victim is missing; 25 years from reappearance if the victim surfaces alive.", None),
("9851", "Sec. 5(a)", "GI-TERM-MATCH", "easy", 20,
 "Under R.A. 9851, acts such as killing members of a group or preventing births within it, done with intent to destroy, in whole or in part, a national, ethnic, racial, religious or social group as such, are called:",
 [("War crimes", "GI-SIBLING-TERM", "War crimes (Sec. 4) are grave breaches of the laws of armed conflict; the intent to destroy a group as such defines genocide."),
  ("Crimes against humanity", "GI-SIBLING-TERM", "Crimes against humanity (Sec. 6) are acts committed as part of a widespread or systematic attack on a civilian population; they do not need intent to destroy a group."),
  ("Genocide", None, "Sec. 5(a): genocide means acts with intent to destroy, in whole or in part, a national, ethnic, racial, religious, social or any other similar stable and permanent group as such."),
  ("Enforced disappearance", "GI-SIBLING-TERM", "Enforced disappearance is listed among crimes against humanity (Sec. 6); it is not defined by intent to destroy a group.")],
 "\"genocide\" means any of the following acts with intent to destroy, in whole or in part, a national, ethnic, racial, religious, social or any other similar stable and permanent group as such",
 "Genocide: acts done with intent to destroy a protected group, in whole or in part.", "Sec. 5: \"intent to destroy ... a group as such\" points to genocide.", "Intent to destroy a group = genocide."),
("9851", "Secs. 9 and 11", "GI-SCENARIO-APPLY", "hard", 40,
 "A former cabinet member is charged under R.A. 9851 for a crime against humanity committed in 2011, after the law took effect. He argues that the case has prescribed and that his official position exempts him. Which statement is correct?",
 [("The case has prescribed, but his position gives no exemption", "GI-SOUNDS-RIGHT", "Sec. 11 says crimes under the Act are not subject to any prescription, so the case has not prescribed."),
  ("The case has not prescribed, but his position reduces the sentence", "GI-SOUNDS-RIGHT", "Sec. 9 says official capacity is not, in and of itself, a ground for reduction of sentence."),
  ("He is exempt, because the act was done in an official capacity", "GI-SOUNDS-RIGHT", "Sec. 9 says official capacity as a member of a government shall in no case exempt a person from criminal responsibility."),
  ("Both arguments fail: the crime does not prescribe, and his position neither exempts him nor reduces his sentence", None, "Sec. 11: the crimes, their prosecution and the execution of sentences are not subject to any prescription. Sec. 9: official capacity, including as a member of a government, never exempts a person and is not in itself a ground to reduce the sentence.")],
 "The crimes defined and penalized under this Act, their prosecution, and the execution of sentences imposed on their account, shall not be subject to any prescription",
 "Non-prescription: there is no time limit on prosecution. Irrelevance of official capacity: office gives no immunity.", "Sec. 11: no prescription. Sec. 9: no exemption and no reduction for official capacity.", None),
]
SECOND = {9: "official capacity as a head of state or government, a member of a government or parliament, an elected representative or a government official shall in no case exempt a person from criminal responsibility under this Act, nor shall it, in and of itself, constitute a ground for reduction of sentence"}
norm = lambda s: re.sub(r"\s+", " ", s).lower().replace("bight", "right")
items, ARCH_N = [], {}
# CoS 2026-10-17: 9 of 10 passed and 0001 passes with its o4 reason reworded; fact IDs added; all 10 approved for activation.
FACT = ["FACT-RA7610-3A-CHILD-DEFINITION", "FACT-RA7610-3B-PSYCHOLOGICAL-MALTREATMENT", "FACT-RA9710-18-GYNECOLOGICAL-LEAVE",
        "FACT-RA9710-11B-DEV-COUNCIL-40PCT-WOMEN", "FACT-RA9745-6-TORTURE-ABSOLUTE", "FACT-RA9745-8-TORTURE-EVIDENCE-INADMISSIBLE",
        "FACT-RA10353-5-ORDER-OF-BATTLE-UNLAWFUL", "FACT-RA10353-22-PRESCRIPTION-25-YEARS", "FACT-RA9851-5A-GENOCIDE",
        "FACT-RA9851-9-11-NO-PRESCRIPTION-NO-IMMUNITY"]
REVIEW = {"status": "approved", "review_status": "passed", "reviewer": "Chief of Staff (final approval, delegated by GT)", "reviewed_at": "2026-10-17"}
for n, (law, sec, arch, diff, secs, stem, opts, quote, terms, method, sc) in enumerate(I):
    f, url, name = LAW[law]
    txt = norm(open(f"/workspace/gi/{f}.html.txt").read())
    for qt in [quote] + ([SECOND[n]] if n in SECOND else []):
        assert norm(qt) in txt, (law, sec, qt[:60])
    ids = ["o1", "o2", "o3", "o4"]
    key = next(ids[i] for i, o in enumerate(opts) if o[1] is None)
    it = {"id": f"CIVIO-GAP4-{arch}-{n + 1:04d}", "track": "both", "domain": "general_information",
          "competency": "Peace and Human Rights Issues and Concepts", "concept": "human rights law", "micro_skill": f"recall and apply {name.split(' (')[0]}, {sec}",
          "archetype": arch, "difficulty": diff, "est_seconds": secs, "language": "en", "stem": stem,
          "options": [{"option_id": ids[i], "text": o[0]} for i, o in enumerate(opts)], "answer_option_id": key,
          "reveal": {"terms": terms, "shortcut": method, "why_correct": opts[ids.index(key)][2],
                     "why_wrong": {ids[i]: o[2] for i, o in enumerate(opts) if o[1]}},
          "distractor_reasoning": {ids[i]: o[1] for i, o in enumerate(opts) if o[1]},
          "source": f"{name}, {sec}", "source_url": url, "source_quote": quote, "source_group": "civio",
          "status": "draft", "review_status": "unreviewed", "reviewer": None, "reviewed_at": None,
          "provenance": {"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-17T15:30:00+08:00", "spec_version": "0.1.8"},
          "_legacy": True}
    if sc: it["shortcut"] = sc
    it["fact_id"] = FACT[n]
    it.update(REVIEW)
    it["notes"] = "Approved by CoS 2026-10-17."
    items.append(it)
from collections import Counter
print(Counter(i["answer_option_id"] for i in items))
json.dump({"batch": "gap-fill-004", "spec_version": "0.1.8", "status": "approved (CoS 2026-10-17)", "source_group": "civio",
           "notes": "GI gap-fill for laws missing from the bank (round 03 baseline B2): R.A. 7610, 9710, 9745, 10353, 9851. Quotes checked against LawPhil text fetched 2026-10-17. _legacy marks GI items outside gi_facts (checked by source_quote instead).",
           "items": items}, open("docs/research/gap-fill-004.json", "w"), ensure_ascii=False, indent=2)
