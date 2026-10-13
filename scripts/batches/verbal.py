"""Verbal Ability (English). Grammar frames with coded errors, plus curated word tables."""
from common import make, Skip, FIRST, PLACES, OFFICES
import verbal_more as VM

B = dict(track="both", domain="verbal_en")

# (subject phrase, nearest plural noun, [(singular verb, plural verb, rest)])
AGREE = [
    ("The list of approved applicants", "applicants", [("is", "are", "posted at the city hall lobby"), ("needs", "need", "to be checked again before Friday")]),
    ("The box of old receipts", "receipts", [("was", "were", "found under the cashier's table"), ("weighs", "weigh", "more than ten kilos")]),
    ("The head of the three sections", "sections", [("signs", "sign", "every leave form"), ("was", "were", "absent during the audit")]),
    ("Each of the new clerks", "clerks", [("has", "have", "a separate locker"), ("receives", "receive", "a copy of the office manual")]),
    ("One of the barangay tanods", "tanods", [("guards", "guard", "the school gate at night"), ("was", "were", "given a commendation")]),
    ("The supply of vaccines", "vaccines", [("lasts", "last", "until the end of the month"), ("was", "were", "delivered on Monday")]),
    ("The leader of the volunteers", "volunteers", [("speaks", "speak", "at every barangay assembly"), ("has", "have", "asked for more trash bags")]),
    ("Every one of the forms", "forms", [("needs", "need", "a signature"), ("was", "were", "filed by noon")]),
    ("The cost of the repairs", "repairs", [("is", "are", "higher than the estimate"), ("has", "have", "doubled since last year")]),
    ("A stack of folders", "folders", [("sits", "sit", "on the chief's desk"), ("was", "were", "left in the conference room")]),
    ("The report on the floods", "floods", [("shows", "show", "damage in six barangays"), ("was", "were", "sent to the governor")]),
    ("The schedule of the trainings", "trainings", [("changes", "change", "every quarter"), ("is", "are", "posted on the bulletin board")]),
    ("The quality of the roads", "roads", [("affects", "affect", "the travel time of buses"), ("has", "have", "improved this year")]),
    ("Neither of the drivers", "drivers", [("knows", "know", "the new route"), ("was", "were", "late this morning")]),
    ("The number of complaints", "complaints", [("has", "have", "gone down"), ("is", "are", "lower than last month")]),
    ("The basket of mangoes", "mangoes", [("belongs", "belong", "to the canteen"), ("was", "were", "a gift from the farmers")]),
    ("The price of school supplies", "supplies", [("rises", "rise", "every June"), ("was", "were", "discussed at the meeting")]),
    ("Everyone in the two offices", "offices", [("wants", "want", "a shorter queue"), ("was", "were", "invited to the seminar")]),
]
PLURAL = {"are", "were", "have"}


def agree(rng, iid):
    subj, noun, preds = rng.choice(AGREE)
    vs, vp, rest = rng.choice(preds)
    plural = vs in PLURAL or not vs.endswith("s")
    base = vs if plural else vp
    stem = f"Choose the word that best completes the sentence: {subj} ____ {rest}."
    third = {"is": "being", "are": "being", "was": "being", "were": "being", "has": "having", "have": "having"}.get(vs, (base[:-1] if base.endswith("e") else base) + "ing")
    fourth = {"is": "be", "are": "be", "was": "been", "were": "been", "has": "to have", "have": "to have"}.get(vs, "to " + base)
    wrong = [(vp, "VEN-NEAREST-NOUN", f"\"{vp}\" agrees with \"{noun}\", the nearest noun, not with the true subject."),
             (third, "VEN-FORM", f"\"{third}\" cannot be the main verb on its own; the sentence would have no full verb."),
             (fourth, "VEN-FORM", f"\"{fourth}\" is not a verb form that can stand alone after this subject.")]
    head = subj.split(" of ")[0].split(" on ")[0].split(" in ")[0]
    num = "plural" if plural else "singular"
    it = make(id=iid, **B, competency="Grammar and correct usage", concept="subject-verb agreement", micro_skill="find the true subject past a prepositional phrase",
              archetype="VEN-ERROR-AGREE", difficulty="medium", est=30, stem=stem, correct=vs, wrong=wrong,
              terms="The \"subject\" is who or what the sentence is about. A singular subject takes a singular verb (often ending in -s); a plural subject takes a plural verb.",
              shortcut=f"Cover the phrase that starts with \"of\", \"on\" or \"in\". Read \"{head} ____\". The subject is {num}, so use the {num} verb.",
              why_correct=f"\"{vs}\" is right: \"{head}\" is {num}.", rng=rng)
    it["_sig"] = stem
    return it


TENSE = [("Yesterday", "past"), ("Last Friday", "past"), ("Two days ago", "past"), ("In 2019", "past"), ("Tomorrow", "future"), ("Next month", "future"),
         ("By next week", "futperf"), ("By the end of the year", "futperf"), ("Since January", "presperf"), ("Right now", "prog")]
TV = [("submit", "submitted", "will submit", "submits", "has submitted", "will have submitted", "is submitting", "the payroll"),
      ("inspect", "inspected", "will inspect", "inspects", "has inspected", "will have inspected", "is inspecting", "the drainage canal"),
      ("visit", "visited", "will visit", "visits", "has visited", "will have visited", "is visiting", "the health center"),
      ("review", "reviewed", "will review", "reviews", "has reviewed", "will have reviewed", "is reviewing", "the leave forms"),
      ("deliver", "delivered", "will deliver", "delivers", "has delivered", "will have delivered", "is delivering", "the relief goods"),
      ("check", "checked", "will check", "checks", "has checked", "will have checked", "is checking", "the attendance sheets"),
      ("clean", "cleaned", "will clean", "cleans", "has cleaned", "will have cleaned", "is cleaning", "the plaza"),
      ("update", "updated", "will update", "updates", "has updated", "will have updated", "is updating", "the voters' list"),
      ("encode", "encoded", "will encode", "encodes", "has encoded", "will have encoded", "is encoding", "the census forms")]


def tense(rng, iid):
    sig, t = rng.choice(TENSE)
    base, past, fut, pres, pp, fp, prog, obj = rng.choice(TV)
    forms = {"past": past, "future": fut, "present": pres, "presperf": pp, "futperf": fp, "prog": prog}
    names = {"past": "simple past", "future": "simple future", "present": "simple present", "presperf": "present perfect", "futperf": "future perfect", "prog": "present progressive"}
    who = rng.choice(FIRST + [f"the {o} staff" for o in OFFICES])
    if t == "presperf":
        stem = f"Choose the correct verb: {sig}, {who} ____ {obj} on time each week."
    else:
        stem = f"Choose the correct verb: {sig}, {who} ____ {obj}."
    c = forms[t]
    others = {"past": ["future", "presperf", "futperf"], "future": ["past", "presperf", "futperf"], "futperf": ["past", "presperf", "prog"],
              "presperf": ["past", "future", "futperf"], "prog": ["past", "futperf", "present"]}[t]
    wrong = [(forms[k], "VEN-TENSE", f"\"{forms[k]}\" is {names[k]}. It does not fit the time signal \"{sig}\".") for k in others[:3]]
    it = make(id=iid, **B, competency="Grammar and correct usage", concept="verb tense", micro_skill="match tense to a time signal", archetype="VEN-ERROR-TENSE",
                difficulty="easy" if t in ("past", "future") else "medium", est=25, stem=stem, correct=c, wrong=wrong,
                terms="\"Tense\" tells when an action happens. A \"time signal\" is a word like yesterday, tomorrow or since that fixes the time.",
                shortcut=f"Find the time signal first: \"{sig}\". It calls for the {names[t]}.",
                why_correct=f"\"{c}\" is right: the {names[t]} matches \"{sig}\".", rng=rng)
    it["_sig"] = sig + base
    return it


# confused words: (sentence with ____, right, [(wrong, code, why)])
CONFUSED = [
    ("The new curfew had a strong ____ on street crime.", "effect", [("affect", "VEN-HOMOPHONE", "\"affect\" is usually a verb (to influence); a noun is needed after \"a strong\"."), ("afect", "VEN-FORM", "This is a misspelling."), ("effort", "VEN-REGISTER", "\"effort\" means trying hard; it does not fit the meaning.")]),
    ("Heavy rain can ____ the delivery of relief goods.", "affect", [("effect", "VEN-HOMOPHONE", "\"effect\" is usually a noun (a result); a verb is needed after \"can\"."), ("infect", "VEN-HOMOPHONE", "\"infect\" means to spread a disease."), ("affection", "VEN-FORM", "\"affection\" is a noun meaning fondness.")]),
    ("Please put the signed forms over ____, on the second shelf.", "there", [("their", "VEN-HOMOPHONE", "\"their\" shows ownership (their office)."), ("they're", "VEN-HOMOPHONE", "\"they're\" means \"they are\"."), ("theirs", "VEN-FORM", "\"theirs\" is a possessive pronoun.")]),
    ("The applicants left ____ IDs at the guard post.", "their", [("there", "VEN-HOMOPHONE", "\"there\" points to a place."), ("they're", "VEN-HOMOPHONE", "\"they're\" means \"they are\"."), ("them", "VEN-FORM", "\"them\" cannot show ownership before a noun.")]),
    ("The mayor will ____ the award to the best barangay.", "present", [("presence", "VEN-FORM", "\"presence\" is a noun."), ("presents", "VEN-FORM", "After \"will\" the base form is needed."), ("represent", "VEN-HOMOPHONE", "\"represent\" means to act for someone.")]),
    ("All offices must ____ with the new dress code.", "comply", [("compile", "VEN-HOMOPHONE", "\"compile\" means to collect into one list."), ("complain", "VEN-HOMOPHONE", "\"complain\" means to say you are unhappy."), ("comply to", "VEN-PARTICLE", "The usual pairing is \"comply with\"; \"with\" is already in the sentence.")]),
    ("The treasurer gave sound ____ on the budget.", "advice", [("advise", "VEN-FORM", "\"advise\" is the verb; a noun is needed after \"sound\"."), ("advices", "VEN-FORM", "\"advice\" is uncountable and has no -s plural."), ("device", "VEN-HOMOPHONE", "\"device\" is a tool or gadget.")]),
    ("The guard will ____ visitors to sign the logbook.", "advise", [("advice", "VEN-FORM", "\"advice\" is a noun; a verb is needed after \"will\"."), ("advised", "VEN-FORM", "After \"will\" the base form is needed."), ("devise", "VEN-HOMOPHONE", "\"devise\" means to invent a plan.")]),
    ("The ____ of the school called a parents' meeting.", "principal", [("principle", "VEN-HOMOPHONE", "\"principle\" is a rule or belief, not a person."), ("principally", "VEN-FORM", "\"principally\" is an adverb."), ("principled", "VEN-FORM", "\"principled\" is an adjective.")]),
    ("Honesty is the first ____ of public service.", "principle", [("principal", "VEN-HOMOPHONE", "\"principal\" is a head person or main sum of money."), ("principles", "VEN-FORM", "After \"the first\" a singular noun is needed."), ("practice", "VEN-REGISTER", "\"practice\" is a habit or doing, not a basic rule.")]),
    ("The office ran out of ____ for the printer.", "stationery", [("stationary", "VEN-HOMOPHONE", "\"stationary\" means not moving."), ("station", "VEN-HOMOPHONE", "\"station\" is a place."), ("stationed", "VEN-FORM", "\"stationed\" is a verb form.")]),
    ("The truck stayed ____ in the traffic for an hour.", "stationary", [("stationery", "VEN-HOMOPHONE", "\"stationery\" is paper and office supplies."), ("stationed", "VEN-FORM", "\"stationed\" means assigned to a place."), ("standing", "VEN-REGISTER", "\"standing\" is used for people, not a truck stuck in traffic.")]),
    ("The new road will be finished ____ than planned.", "later", [("latter", "VEN-HOMOPHONE", "\"latter\" means the second of two."), ("lately", "VEN-FORM", "\"lately\" means recently."), ("latest", "VEN-FORM", "\"latest\" cannot be used with \"than\".")]),
    ("The team worked faster ____ the other shift.", "than", [("then", "VEN-HOMOPHONE", "\"then\" is about time (first this, then that)."), ("that", "VEN-FORM", "\"that\" cannot follow a comparison like \"faster\"."), ("as", "VEN-FORM", "\"as\" pairs with \"as fast as\", not \"faster\".")]),
    ("The clerk will ____ the old files to make space.", "lose", [("loose", "VEN-HOMOPHONE", "\"loose\" means not tight."), ("loss", "VEN-FORM", "\"loss\" is a noun."), ("lost", "VEN-FORM", "After \"will\" the base form is needed.")]) if False else
    ("Do not ____ the receipt; you will need it for the refund.", "lose", [("loose", "VEN-HOMOPHONE", "\"loose\" means not tight."), ("loss", "VEN-FORM", "\"loss\" is a noun."), ("lost", "VEN-FORM", "After \"do not\" the base form is needed.")]),
    ("The ____ of the new hall is near the public market.", "site", [("sight", "VEN-HOMOPHONE", "\"sight\" is the ability to see or a view."), ("cite", "VEN-HOMOPHONE", "\"cite\" means to quote a source."), ("side", "VEN-HOMOPHONE", "\"side\" is one edge of something.")]),
    ("The report must ____ the law that allows the fee.", "cite", [("site", "VEN-HOMOPHONE", "\"site\" is a place."), ("sight", "VEN-HOMOPHONE", "\"sight\" is a view."), ("recite", "VEN-REGISTER", "\"recite\" means to say aloud from memory.")]),
    ("Only employees, ____ the guards, may enter after 6 p.m.", "except", [("accept", "VEN-HOMOPHONE", "\"accept\" means to receive."), ("expect", "VEN-HOMOPHONE", "\"expect\" means to think something will happen."), ("excepting", "VEN-REGISTER", "\"excepting\" is stiff and rare here.")]),
    ("The committee voted to ____ the new proposal.", "accept", [("except", "VEN-HOMOPHONE", "\"except\" means leaving out."), ("access", "VEN-HOMOPHONE", "\"access\" means a way in."), ("accepts", "VEN-FORM", "After \"to\" the base form is needed.")]),
    ("The town ____ the drivers who joined the cleanup.", "complimented", [("complemented", "VEN-HOMOPHONE", "\"complemented\" means completed or matched well."), ("complied", "VEN-HOMOPHONE", "\"complied\" means obeyed."), ("compliment", "VEN-FORM", "The sentence needs the past tense.")]),
    ("The ____ of the new policy was explained at the flag ceremony.", "purpose", [("propose", "VEN-HOMOPHONE", "\"propose\" is a verb meaning to suggest."), ("purpost", "VEN-FORM", "This is not a word."), ("porpoise", "VEN-HOMOPHONE", "A \"porpoise\" is a sea animal.")]),
    ("Each worker must keep the ____ of client records.", "confidentiality", [("confidence", "VEN-HOMOPHONE", "\"confidence\" means trust in oneself."), ("confident", "VEN-FORM", "\"confident\" is an adjective."), ("confidently", "VEN-FORM", "\"confidently\" is an adverb.")]),
]

PHRASAL = [
    ("The fire truck had to ____ the road because of the flood.", "turn back", [("turn up", "VEN-PARTICLE", "\"turn up\" means to appear or arrive."), ("turn in", "VEN-PARTICLE", "\"turn in\" means to submit."), ("turn over", "VEN-PARTICLE", "\"turn over\" means to hand to someone.")]),
    ("Please ____ your report before Friday.", "hand in", [("hand out", "VEN-PARTICLE", "\"hand out\" means to give to many people."), ("hand down", "VEN-PARTICLE", "\"hand down\" means to pass to a younger person."), ("hand over", "VEN-PARTICLE", "\"hand over\" means to give control to someone; \"hand in\" is the usual term for submitting work.")]),
    ("The meeting was ____ because of the typhoon.", "called off", [("called on", "VEN-PARTICLE", "\"called on\" means visited or asked to speak."), ("called up", "VEN-PARTICLE", "\"called up\" means phoned or drafted."), ("called in", "VEN-PARTICLE", "\"called in\" means asked to come.")]),
    ("The new clerk ____ the forms carefully before filing them.", "looked over", [("looked after", "VEN-PARTICLE", "\"looked after\" means took care of."), ("looked up to", "VEN-PARTICLE", "\"looked up to\" means admired."), ("looked out", "VEN-PARTICLE", "\"looked out\" means watched for danger.")]),
    ("The office will ____ a new system for leave requests.", "set up", [("set off", "VEN-PARTICLE", "\"set off\" means to start a trip or trigger."), ("set back", "VEN-PARTICLE", "\"set back\" means to delay."), ("set aside", "VEN-PARTICLE", "\"set aside\" means to save for later.")]),
    ("The guard ____ a wallet at the gate and returned it.", "came across", [("came over", "VEN-PARTICLE", "\"came over\" means visited."), ("came up", "VEN-PARTICLE", "\"came up\" means was mentioned."), ("came down", "VEN-PARTICLE", "\"came down\" means fell or got lower.")]),
    ("The barangay will ____ the cause of the blackout.", "look into", [("look for", "VEN-PARTICLE", "\"look for\" means to search for something lost."), ("look up", "VEN-PARTICLE", "\"look up\" means to find in a book or list."), ("look on", "VEN-PARTICLE", "\"look on\" means to watch without helping.")]),
    ("The team could not ____ the deadline and asked for more time.", "keep up with", [("keep off", "VEN-PARTICLE", "\"keep off\" means to stay away."), ("keep out", "VEN-PARTICLE", "\"keep out\" means to stay outside."), ("keep back", "VEN-PARTICLE", "\"keep back\" means to hold something back.")]),
    ("The old printer finally ____ after ten years.", "broke down", [("broke up", "VEN-PARTICLE", "\"broke up\" means ended a relationship or split."), ("broke in", "VEN-PARTICLE", "\"broke in\" means entered by force."), ("broke out", "VEN-PARTICLE", "\"broke out\" means started suddenly, like a fire.")]),
    ("We ran ____ of bond paper this morning.", "out", [("over", "VEN-PARTICLE", "\"ran over\" means hit with a vehicle."), ("into", "VEN-PARTICLE", "\"ran into\" means met by chance."), ("off", "VEN-PARTICLE", "\"ran off\" means left quickly.")]),
    ("The chief asked us to ____ the noise during the exam.", "cut down on", [("cut off", "VEN-PARTICLE", "\"cut off\" means to stop a supply."), ("cut in", "VEN-PARTICLE", "\"cut in\" means to interrupt."), ("cut out", "VEN-PARTICLE", "\"cut out\" means to remove by cutting.")]),
    ("Volunteers ____ food packs to the evacuees.", "gave out", [("gave up", "VEN-PARTICLE", "\"gave up\" means stopped trying."), ("gave in", "VEN-PARTICLE", "\"gave in\" means agreed after refusing."), ("gave off", "VEN-PARTICLE", "\"gave off\" means released a smell or heat.")]),
]

# synonyms: (word, sentence context, right, [(wrong, code, why)])
SYN = [
    ("diligent", "hard-working", [("lazy", "VRB-ANTONYM-TRAP", "\"lazy\" is the opposite."), ("diluted", "VEN-HOMOPHONE", "\"diluted\" only looks like \"diligent\"; it means made weaker."), ("delicate", "VEN-HOMOPHONE", "\"delicate\" only looks similar; it means easily broken.")]),
    ("candid", "frank", [("secretive", "VRB-ANTONYM-TRAP", "\"secretive\" is the opposite."), ("candied", "VEN-HOMOPHONE", "\"candied\" means coated in sugar."), ("candidate", "VEN-HOMOPHONE", "A candidate is a person running for a post.")]),
    ("meager", "scanty", [("plentiful", "VRB-ANTONYM-TRAP", "\"plentiful\" is the opposite."), ("eager", "VEN-HOMOPHONE", "\"eager\" only sounds alike; it means keen."), ("meaningful", "VEN-HOMOPHONE", "\"meaningful\" only looks similar.")]),
    ("prudent", "careful", [("reckless", "VRB-ANTONYM-TRAP", "\"reckless\" is the opposite."), ("prude", "VEN-HOMOPHONE", "A prude is easily shocked."), ("prominent", "VEN-HOMOPHONE", "\"prominent\" means well known.")]),
    ("obsolete", "outdated", [("modern", "VRB-ANTONYM-TRAP", "\"modern\" is the opposite."), ("absolute", "VEN-HOMOPHONE", "\"absolute\" sounds alike; it means complete."), ("obstinate", "VEN-HOMOPHONE", "\"obstinate\" means stubborn.")]),
    ("lenient", "tolerant", [("strict", "VRB-ANTONYM-TRAP", "\"strict\" is the opposite."), ("lending", "VEN-HOMOPHONE", "\"lending\" means giving a loan."), ("lean", "VEN-HOMOPHONE", "\"lean\" means thin.")]),
    ("verify", "confirm", [("doubt", "VRB-ANTONYM-TRAP", "\"doubt\" is close to the opposite."), ("vary", "VEN-HOMOPHONE", "\"vary\" means to change."), ("verbalize", "VEN-HOMOPHONE", "\"verbalize\" means to say in words.")]),
    ("abundant", "plentiful", [("scarce", "VRB-ANTONYM-TRAP", "\"scarce\" is the opposite."), ("abandoned", "VEN-HOMOPHONE", "\"abandoned\" means left behind."), ("redundant", "VEN-HOMOPHONE", "\"redundant\" means more than needed.")]),
    ("hostile", "unfriendly", [("welcoming", "VRB-ANTONYM-TRAP", "\"welcoming\" is the opposite."), ("hostel", "VEN-HOMOPHONE", "A hostel is a cheap place to stay."), ("hostage", "VEN-HOMOPHONE", "A hostage is a person held captive.")]),
    ("tedious", "boring", [("exciting", "VRB-ANTONYM-TRAP", "\"exciting\" is the opposite."), ("tidy", "VEN-HOMOPHONE", "\"tidy\" means neat."), ("timid", "VEN-HOMOPHONE", "\"timid\" means shy.")]),
    ("feasible", "workable", [("impossible", "VRB-ANTONYM-TRAP", "\"impossible\" is the opposite."), ("festive", "VEN-HOMOPHONE", "\"festive\" means cheerful, like a fiesta."), ("visible", "VEN-HOMOPHONE", "\"visible\" means can be seen.")]),
    ("concise", "brief", [("wordy", "VRB-ANTONYM-TRAP", "\"wordy\" is the opposite."), ("concave", "VEN-HOMOPHONE", "\"concave\" means curved inward."), ("precise", "VEN-HOMOPHONE", "\"precise\" means exact, not short.")]),
    ("vacant", "empty", [("occupied", "VRB-ANTONYM-TRAP", "\"occupied\" is the opposite."), ("vacation", "VEN-HOMOPHONE", "A vacation is a holiday."), ("vague", "VEN-HOMOPHONE", "\"vague\" means unclear.")]),
    ("imminent", "about to happen", [("far off", "VRB-ANTONYM-TRAP", "\"far off\" is the opposite."), ("eminent", "VEN-HOMOPHONE", "\"eminent\" means famous and respected."), ("immense", "VEN-HOMOPHONE", "\"immense\" means huge.")]),
    ("frugal", "thrifty", [("wasteful", "VRB-ANTONYM-TRAP", "\"wasteful\" is the opposite."), ("fragile", "VEN-HOMOPHONE", "\"fragile\" means easily broken."), ("fruitful", "VEN-HOMOPHONE", "\"fruitful\" means productive.")]),
    ("authentic", "genuine", [("fake", "VRB-ANTONYM-TRAP", "\"fake\" is the opposite."), ("authority", "VEN-HOMOPHONE", "\"authority\" means power to decide."), ("automatic", "VEN-HOMOPHONE", "\"automatic\" means working by itself.")]),
    ("reluctant", "unwilling", [("eager", "VRB-ANTONYM-TRAP", "\"eager\" is the opposite."), ("relevant", "VEN-HOMOPHONE", "\"relevant\" means related to the topic."), ("resilient", "VEN-HOMOPHONE", "\"resilient\" means able to recover.")]),
    ("integrity", "honesty", [("corruption", "VRB-ANTONYM-TRAP", "\"corruption\" is the opposite."), ("integration", "VEN-HOMOPHONE", "\"integration\" means joining parts together."), ("intensity", "VEN-HOMOPHONE", "\"intensity\" means strength of feeling.")]),
    ("negligent", "careless", [("attentive", "VRB-ANTONYM-TRAP", "\"attentive\" is the opposite."), ("negligible", "VEN-HOMOPHONE", "\"negligible\" means too small to matter."), ("negotiable", "VEN-HOMOPHONE", "\"negotiable\" means open to discussion.")]),
    ("transparent", "open", [("hidden", "VRB-ANTONYM-TRAP", "\"hidden\" is the opposite."), ("transport", "VEN-HOMOPHONE", "\"transport\" means to carry."), ("transient", "VEN-HOMOPHONE", "\"transient\" means brief, passing.")]),
    ("punctual", "on time", [("late", "VRB-ANTONYM-TRAP", "\"late\" is the opposite."), ("punctured", "VEN-HOMOPHONE", "\"punctured\" means pierced."), ("practical", "VEN-HOMOPHONE", "\"practical\" means useful.")]),
    ("courteous", "polite", [("rude", "VRB-ANTONYM-TRAP", "\"rude\" is the opposite."), ("courageous", "VEN-HOMOPHONE", "\"courageous\" means brave."), ("curious", "VEN-HOMOPHONE", "\"curious\" means wanting to know.")]),
    ("deteriorate", "worsen", [("improve", "VRB-ANTONYM-TRAP", "\"improve\" is the opposite."), ("determine", "VEN-HOMOPHONE", "\"determine\" means to decide."), ("detour", "VEN-HOMOPHONE", "A detour is a different route.")]),
    ("accurate", "correct", [("wrong", "VRB-ANTONYM-TRAP", "\"wrong\" is the opposite."), ("accustomed", "VEN-HOMOPHONE", "\"accustomed\" means used to."), ("adequate", "VEN-HOMOPHONE", "\"adequate\" means enough.")]),
    ("temporary", "short-term", [("permanent", "VRB-ANTONYM-TRAP", "\"permanent\" is the opposite."), ("temperate", "VEN-HOMOPHONE", "\"temperate\" means mild."), ("contemporary", "VEN-HOMOPHONE", "\"contemporary\" means of the same time or modern.")]),
]
CTX = ["The {w} staff of the {o} drew praise.", "The memo described the plan as {w}.", "Everyone noticed how {w} the new officer was.",
       "In the {o}, the word \"{w}\" appeared in the report.", "The auditor used the word \"{w}\" in her findings."]


def confused(rng, iid):
    sent, c, wr = rng.choice(CONFUSED)
    return make(id=iid, **B, competency="Grammar and correct usage", concept="commonly confused words", micro_skill="tell look-alike words apart",
                archetype="VEN-SENT-COMP-WORD", difficulty="medium", est=25, stem=f"Choose the word that best completes the sentence: {sent}", correct=c, wrong=wr,
                terms="Some English words look or sound alike but mean different things. Read the whole sentence before choosing.",
                shortcut="Decide what kind of word the blank needs (a thing, an action, a describing word), then match the meaning.",
                why_correct=f"\"{c}\" is right. It has the meaning and the word form the sentence needs.", rng=rng)


def phrasal(rng, iid):
    sent, c, wr = rng.choice(PHRASAL)
    return make(id=iid, **B, competency="Grammar and correct usage", concept="phrasal verbs", micro_skill="pick the right particle", archetype="VEN-SENT-COMP-PHRASAL",
                difficulty="medium", est=25, stem=f"Choose the phrase that best completes the sentence: {sent}", correct=c, wrong=wr,
                terms="A \"phrasal verb\" is a verb plus a small word (up, out, off, in) that together have their own meaning.",
                shortcut="Put each choice in the blank and say the sentence. Only one gives the meaning the sentence needs.",
                why_correct=f"\"{c}\" is right. It gives the meaning the sentence needs.", rng=rng)


def synonym(rng, iid):
    w, c, wr = rng.choice(SYN)
    return make(id=iid, **B, competency="Vocabulary", concept="synonyms", micro_skill="word meaning", archetype="VEN-WORD-MEANING", difficulty="medium", est=20,
                stem=f"Which word is closest in meaning to the word in capital letters?  {w.upper()}", correct=c, wrong=wr,
                terms="A \"synonym\" is a word with nearly the same meaning.",
                shortcut=f"Make a short sentence with \"{w}\", then swap in each choice. Watch for words that only look or sound like \"{w}\".",
                why_correct=f"\"{c}\" is right. \"{w.capitalize()}\" means {c}.", rng=rng)


def antonym(rng, iid):
    w, syn, wr = rng.choice(SYN)
    opp = wr[0][0]
    return make(id=iid, **B, competency="Vocabulary", concept="antonyms", micro_skill="word meaning (opposite)", archetype="VEN-WORD-MEANING", difficulty="medium", est=20,
                stem=f"Which word is most nearly OPPOSITE in meaning to the word in capital letters?  {w.upper()}", correct=opp,
                wrong=[(syn, "VRB-SYNONYM-TRAP", f"\"{syn}\" means the same as \"{w}\", not the opposite.")] + [(t, c, y) for t, c, y in wr[1:]],
                terms="An \"antonym\" is a word with the opposite meaning.",
                shortcut=f"First say what \"{w}\" means ({syn}). Then look for the word that means the reverse.",
                why_correct=f"\"{opp}\" is right. \"{w.capitalize()}\" means {syn}; \"{opp}\" is the reverse.", rng=rng)


PRON = [("The certificates were given to Liza and ____.", "me", [("I", "VEN-FORM", "\"I\" is a subject pronoun; after \"to\" you need an object pronoun."), ("myself", "VEN-FORM", "\"myself\" is used only when the subject is also \"I\"."), ("mine", "VEN-FORM", "\"mine\" shows ownership.")]),
        ("____ and the guard locked the office at six.", "She", [("Her", "VEN-FORM", "\"Her\" is an object pronoun; the subject needs \"She\"."), ("Herself", "VEN-FORM", "\"Herself\" cannot be a subject."), ("Hers", "VEN-FORM", "\"Hers\" shows ownership.")]),
        ("The chief asked Ramon and ____ to stay late.", "us", [("we", "VEN-FORM", "\"we\" is a subject pronoun; after \"asked\" you need an object."), ("ourselves", "VEN-FORM", "\"ourselves\" needs \"we\" as the subject."), ("ours", "VEN-FORM", "\"ours\" shows ownership.")]),
        ("Between you and ____, the plan needs more work.", "me", [("I", "VEN-FORM", "\"Between\" takes object pronouns: \"between you and me\"."), ("myself", "VEN-FORM", "\"myself\" is not used after \"between\"."), ("mine", "VEN-FORM", "\"mine\" shows ownership.")]),
        ("It was ____ who found the missing files.", "they", [("them", "VEN-REGISTER", "In formal writing, \"It was they who...\" is the expected form; \"them\" is casual."), ("their", "VEN-FORM", "\"their\" must come before a noun."), ("themselves", "VEN-FORM", "\"themselves\" cannot stand in this slot.")]),
        ("The teacher and ____ will check the test papers.", "I", [("me", "VEN-FORM", "\"me\" is an object pronoun; this is part of the subject."), ("myself", "VEN-FORM", "\"myself\" cannot be a subject."), ("mine", "VEN-FORM", "\"mine\" shows ownership.")]),
        ("Each employee must bring ____ own ID.", "his or her", [("their own's", "VEN-FORM", "This is not a correct English form."), ("its", "VEN-FORM", "\"its\" is for things, not people."), ("one's", "VEN-REGISTER", "\"one's\" does not match \"each employee\".")]),
        ("The award went to the clerk ____ worked overtime all month.", "who", [("whom", "VEN-FORM", "\"whom\" is an object; here the word is the subject of \"worked\"."), ("which", "VEN-FORM", "\"which\" is for things."), ("whose", "VEN-FORM", "\"whose\" shows ownership.")]),
        ("To ____ should I give the signed vouchers?", "whom", [("who", "VEN-REGISTER", "After \"to\", formal English uses \"whom\"."), ("whose", "VEN-FORM", "\"whose\" shows ownership."), ("which", "VEN-FORM", "\"which\" is for things.")]),
        ("The new rules apply to both you and ____.", "them", [("they", "VEN-FORM", "\"they\" is a subject pronoun; after \"to\" you need \"them\"."), ("themselves", "VEN-FORM", "\"themselves\" needs \"they\" as the subject."), ("theirs", "VEN-FORM", "\"theirs\" shows ownership.")]),
]


def pronoun(rng, iid):
    sent, c, wr = rng.choice(PRON)
    return make(id=iid, **B, competency="Grammar and correct usage", concept="pronoun case", micro_skill="subject vs object pronoun", archetype="VEN-SENT-COMP-WORD",
                difficulty="medium", est=25, stem=f"Choose the word that best completes the sentence: {sent}", correct=c, wrong=wr,
                terms="A \"subject pronoun\" (I, she, we, they) does the action. An \"object pronoun\" (me, her, us, them) receives it or comes after words like to and between.",
                shortcut="Cover the other name and read the sentence with only the pronoun. \"Gave to me\" sounds right; \"gave to I\" does not.",
                why_correct=f"\"{c}\" is right. It is the form the slot needs.", rng=rng)


AGREE += VM.AGREE_MORE


def vocab_context(rng, iid):
    sent, word, c, wr = rng.choice(VM.VIC)
    it = make(id=iid, **B, competency="Vocabulary", concept="vocabulary in context", micro_skill="pick the sense that fits the sentence", archetype="VEN-RC-VOCAB",
              difficulty="medium", est=30, stem=f"In the sentence below, what does the word in capital letters most nearly mean?  {sent}", correct=c, wrong=wr,
              terms="Many words have more than one meaning. \"In context\" means the meaning that fits this sentence.",
              shortcut=f"Cover the word in capitals and guess what fits the gap. Then pick the choice closest to your guess, not the most common meaning of \"{word}\".",
              why_correct=f"\"{c}\" is right: it is the sense of \"{word}\" that fits the sentence.", rng=rng)
    it["_sig"] = "VIC:" + sent
    return it


def idiom(rng, iid):
    sent, c, wr = rng.choice(VM.IDIOMS)
    it = make(id=iid, **B, competency="Vocabulary", concept="idioms", micro_skill="meaning of an idiom", archetype="VEN-WORD-MEANING", difficulty="medium", est=25,
              stem=f"What does the phrase in capital letters mean?  {sent}", correct=c, wrong=wr,
              terms="An \"idiom\" is a set phrase whose meaning is not the meaning of its separate words.",
              shortcut="Skip the literal picture. Ask what the speaker wants to say in this situation.",
              why_correct=f"\"{c}\" is right: that is what the idiom means here.", rng=rng)
    it["_sig"] = "IDM:" + sent
    return it


def preposition(rng, iid):
    sent, c, wr = rng.choice(VM.PREP)
    it = make(id=iid, **B, competency="Grammar and correct usage", concept="prepositions", micro_skill="pick the preposition the word pairs with",
              archetype="VEN-SENT-COMP-WORD", difficulty="medium", est=20, stem=f"Choose the word that best completes the sentence: {sent}", correct=c, wrong=wr,
              terms="A \"preposition\" is a small linking word (in, on, at, for, with). Many words always pair with one preposition.",
              shortcut="Read the word just before the blank and recall the phrase it usually forms (interested in, comply with).",
              why_correct=f"\"{c}\" is right: it is the standard pairing in this sentence.", rng=rng)
    it["_sig"] = "PRP:" + sent
    return it


def completion(rng, iid):
    sent, c, wr = rng.choice(VM.SCOMP)
    it = make(id=iid, **B, competency="Vocabulary", concept="sentence completion", micro_skill="use clue words to fill the blank", archetype="VEN-SENT-COMP-WORD",
              difficulty="medium", est=30, stem=f"Choose the word that best completes the sentence: {sent}", correct=c, wrong=wr,
              terms="Clue words such as because, although, so and since tell you whether the blank agrees with or contrasts with the rest.",
              shortcut="Find the clue word, decide if the blank should agree or contrast, then check that the choice is the right word form.",
              why_correct=f"\"{c}\" is right: it fits the clue in the sentence and is the right word form.", rng=rng)
    it["_sig"] = "SCP:" + sent
    return it


TEMPLATES = [agree, tense, confused, phrasal, synonym, antonym, pronoun, vocab_context, idiom, preposition, completion]
# per-batch caps by concept (CoS ruling: tense at most 5 per batch and 50 of 200 overall)
CAPS = {"verb tense": 4, "subject-verb agreement": 4, "synonyms": 3, "antonyms": 3, "commonly confused words": 3, "phrasal verbs": 2, "pronoun case": 2,
        "vocabulary in context": 3, "idioms": 2, "prepositions": 2, "sentence completion": 2}
