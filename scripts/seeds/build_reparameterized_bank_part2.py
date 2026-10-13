"""Second half of the re-parameterized bank builder. Imported by the main script."""

from __future__ import annotations

import json
from pathlib import Path

from build_reparameterized_bank import (  # type: ignore
    explain,
    item,
    pack,
)

# Words with one standard spelling and three real misspellings.
SPELLING = [
    ("receive", ["recieve", "receeve", "recive"], "Receive uses i before e is wrong here: it is e then i, r-e-c-e-i-v-e."),
    ("necessary", ["neccessary", "necessery", "neccesary"], "Necessary has one c and double s."),
    ("publicly", ["publically", "publickly", "publiclly"], "Publicly has no extra al. It is public plus ly."),
    ("calendar", ["calender", "calander", "calandar"], "Calendar ends in ar, not er."),
    ("definite", ["definate", "definete", "defenite"], "Definite has i in the second syllable: def-i-nite."),
    ("environment", ["enviroment", "enviornment", "environement"], "Environment keeps the n after o: envi-ron-ment."),
    ("government", ["goverment", "governement", "govermment"], "Government keeps the n: govern-ment."),
    ("committee", ["comittee", "commitee", "commite"], "Committee has double m, double t, and double e."),
    ("guarantee", ["garantee", "gaurantee", "guarentee"], "Guarantee starts with gua and ends with ee."),
    ("recommend", ["reccomend", "recomend", "reccommend"], "Recommend has one c and double m."),
    ("colleague", ["collegue", "colleage", "coleague"], "Colleague has ea before gue."),
    ("correspondence", ["correspondance", "corespondence", "correspodence"], "Correspondence ends in ence, with double r."),
    ("occasionally", ["occassionally", "ocasionally", "ocassionally"], "Occasionally has two c's and one s: o-c-c-a-s-i-o-n-a-l-l-y."),
    ("perseverance", ["perseverence", "perserverance", "perserverence"], "Perseverance has an a before nce, and no extra r."),
    ("cemetery", ["cemetary", "cematery", "cemetry"], "Cemetery uses e in all three vowel spots."),
    ("harass", ["harrass", "haras", "harras"], "Harass has one r and double s."),
    ("noticeable", ["noticable", "noticeble", "noticible"], "Noticeable keeps the e from notice."),
    ("relevant", ["relevent", "relavant", "relavent"], "Relevant has an a after the l: rel-e-vant."),
    ("rhythm", ["rythm", "rhythem", "rythym"], "Rhythm starts with rh and has no extra vowel."),
    ("sergeant", ["sargent", "sergent", "sargeant"], "Sergeant is s-e-r-g-e-a-n-t."),
    ("vacuum", ["vacum", "vaccuum", "vaccum"], "Vacuum has one c and double u."),
    ("weird", ["wierd", "weerd", "weired"], "Weird is one of the e-i words: w-e-i-r-d."),
    ("achieve", ["acheive", "acheve", "achive"], "Achieve is a-c-h-i-e-v-e."),
    ("believe", ["beleive", "belive", "beleave"], "Believe is b-e-l-i-e-v-e."),
    ("foreign", ["foriegn", "foregn", "forign"], "Foreign is f-o-r-e-i-g-n."),
    ("height", ["heigth", "hieght", "heighth"], "Height ends in ght, not gth."),
    ("library", ["libary", "librery", "liberry"], "Library keeps the r after b."),
    ("neighbor", ["nieghbor", "neigbor", "neighber"], "Neighbor is n-e-i-g-h-b-o-r."),
    ("profession", ["profesion", "proffession", "professon"], "Profession has one f and double s."),
    ("restaurant", ["restarant", "restuarant", "restraunt"], "Restaurant is r-e-s-t-a-u-r-a-n-t."),
    ("schedule", ["schedual", "shedule", "scedule"], "Schedule starts with sche."),
    ("tomorrow", ["tommorow", "tommorrow", "tomorow"], "Tomorrow has one m and double r."),
    ("acquaintance", ["acquaintence", "acquantance", "aquaintance"], "Acquaintance keeps acquai and ends in ance."),
    ("beneficiary", ["beneficary", "benificiary", "benefitiary"], "Beneficiary has i after f and ends in ciary."),
    ("consensus", ["concensus", "consensous", "consenus"], "Consensus has no c before the s: con-sen-sus."),
    ("maintenance", ["maintainance", "maintenence", "maintanance"], "Maintenance keeps ten, not tain."),
]


MEANINGS = [
    ("synonym", "arduous", "Difficult and tiring", ["Easy and brief", "Already finished", "Loud and public"], "Arduous work is hard and tiring."),
    ("synonym", "benign", "Harmless", ["Dangerous", "Hidden", "Required by law"], "Benign means not harmful."),
    ("synonym", "coerce", "Force someone to act", ["Invite without pressure", "Forget a date", "Measure a length"], "To coerce is to pressure someone into acting."),
    ("synonym", "deplete", "Use up", ["Fill again", "Sort alphabetically", "Delay on purpose"], "To deplete a supply is to use it up."),
    ("synonym", "eloquent", "Fluent and persuasive", ["Unable to speak", "Written in numbers only", "Secret"], "Eloquent speech is fluent and persuasive."),
    ("synonym", "frugal", "Careful with money", ["Wasteful", "Late", "Angry"], "A frugal person avoids unnecessary spending."),
    ("synonym", "futile", "Useless", ["Sure to work", "Required", "Very large"], "A futile effort does not succeed."),
    ("synonym", "hasty", "Done too quickly", ["Carefully delayed", "Already filed", "Jointly owned"], "Hasty means rushed."),
    ("synonym", "inevitable", "Certain to happen", ["Easy to avoid", "Against the rules", "Already cancelled"], "Inevitable means it cannot be avoided."),
    ("synonym", "novice", "Beginner", ["Senior specialist", "Written rule", "Closed office"], "A novice is a beginner."),
    ("synonym", "obscure", "Hard to understand", ["Perfectly clear", "Very short", "Already signed"], "Obscure wording is difficult to understand."),
    ("synonym", "reluctant", "Unwilling", ["Eager", "Qualified", "Temporary"], "A reluctant person does not want to act."),
    ("synonym", "subtle", "Not obvious", ["Loud", "Illegal", "Final"], "A subtle difference is easy to miss."),
    ("synonym", "trivial", "Unimportant", ["Urgent", "Confidential", "Accurate"], "A trivial detail does not matter much."),
    ("antonym", "lenient", "Strict", ["Gentle", "Mild", "Forgiving"], "Lenient means not strict, so strict is the opposite."),
    ("synonym", "mandatory", "Required", ["Optional", "Hidden", "Outdated"], "Mandatory means required."),
    ("synonym", "negligent", "Careless", ["Careful", "Prompt", "Neutral"], "Negligent means failing to take proper care."),
    ("synonym", "pertinent", "Relevant", ["Unrelated", "Secret", "Late"], "Pertinent means relevant to the matter."),
    ("synonym", "tentative", "Not yet final", ["Already enacted", "Very loud", "Fully paid"], "A tentative plan can still change."),
    ("antonym", "expand", "Shrink", ["Enlarge", "Increase", "Extend"], "To expand is to grow, so shrink is the opposite."),
    ("synonym", "abate", "Become less intense", ["Become illegal", "Multiply at once", "Move in order"], "Abate means to lessen in force."),
    ("synonym", "concise", "Brief", ["Wordy", "Angry", "Hidden"], "Concise writing uses few words. Wordy is the opposite idea, so brief is the synonym asked here."),
    ("synonym", "meticulous", "Very careful about details", ["Carelessly rushed", "Unable to count", "Publicly announced"], "Meticulous means exact and careful."),
    ("synonym", "viable", "Workable in practice", ["Sure to fail", "Already repealed", "Impossible to name"], "A viable plan can actually be carried out."),
    ("antonym", "scarce", "Plentiful", ["Rare", "Limited", "Short"], "Scarce means in short supply. Plentiful is the opposite."),
    ("synonym", "impartial", "Fair to every side", ["Secretly favoring a friend", "Based only on a rumor", "Decided before the facts"], "Impartial means not taking a side."),
]


ANALOGIES = [
    ("Nurse", "clinic", "mechanic", "garage", ["engine", "invoice", "highway"], "A nurse works in a clinic. A mechanic works in a garage."),
    ("Author", "novel", "chef", "dish", ["stove", "menu", "apron"], "An author produces a novel. A chef produces a dish."),
    ("Key", "lock", "password", "account", ["keyboard", "screen", "desk"], "A key controls a lock. A password controls an account."),
    ("Odometer", "distance", "scale", "weight", ["time", "color", "sound"], "An odometer measures distance. A scale measures weight."),
    ("Seed", "tree", "blueprint", "building", ["hammer", "paint", "window"], "A seed develops into a tree. A blueprint develops into a building."),
    ("Gloves", "hands", "helmet", "head", ["road", "engine", "ticket"], "Gloves protect hands. A helmet protects the head."),
    ("Pen", "write", "brush", "paint", ["measure", "listen", "file"], "A pen is used to write. A brush is used to paint."),
    ("Drought", "water shortage", "flood", "excess water", ["desert sand", "empty tank", "dry wind"], "A drought is too little water. A flood is too much water."),
    ("Librarian", "catalog", "teller", "ledger", ["bookshelf", "stamp", "chair"], "A librarian uses a catalog. A teller uses a ledger."),
    ("Filter", "remove unwanted material", "audit", "check the records", ["decorate the room", "translate a sign", "close the office"], "A filter separates what is unwanted. An audit checks records."),
    ("Rain gauge", "rainfall", "sundial", "time of day", ["distance", "volume", "weight"], "A rain gauge measures rainfall. A sundial indicates the time of day."),
    ("Referee", "decision", "proofreader", "correction", ["weather", "fuel", "medicine"], "A referee issues a decision. A proofreader issues a correction."),
    ("Recipe", "dish", "pattern", "garment", ["needle", "store", "button"], "A recipe guides a dish. A pattern guides a garment."),
    ("Archipelago", "islands", "constellation", "stars", ["planets only", "oceans", "comets only"], "An archipelago is a group of islands. A constellation is a group of stars."),
    ("Scout", "reconnaissance", "auditor", "verification", ["celebration", "decoration", "translation"], "A scout gathers field information. An auditor verifies records."),
    ("Generous", "giving", "cautious", "careful", ["noisy", "rapid", "decorative"], "Generous describes giving. Cautious describes being careful."),
    ("Archive", "preserve", "shredder", "destroy", ["invent", "publish", "multiply"], "An archive keeps records. A shredder destroys papers."),
    ("Barometer", "air pressure", "odometer", "distance", ["humidity only", "weight", "color"], "A barometer measures air pressure. An odometer measures distance."),
    ("Surgeon", "scalpel", "mason", "trowel", ["pilot", "ledger", "siren"], "A surgeon uses a scalpel. A mason uses a trowel."),
    ("Hypothesis", "experiment", "complaint", "investigation", ["briefcase", "sketch", "holiday"], "A hypothesis is tested by an experiment. A complaint is tested by an investigation."),
    ("Vaccine", "prevention", "antibiotic", "treatment of bacteria", ["diagnosis only", "surgery theater", "x-ray film"], "A vaccine is for prevention. An antibiotic is for treating bacteria."),
    ("Map", "route", "agenda", "meeting", ["coffee", "name tag", "holiday"], "A map guides a route. An agenda guides a meeting."),
    ("Leaf", "tree", "page", "book", ["ink", "shelf", "stamp"], "A leaf is part of a tree. A page is part of a book."),
    ("Teacher", "lesson", "coach", "practice drill", ["whistle only", "scoreboard", "locker"], "A teacher prepares a lesson. A coach prepares a practice drill."),
    ("Candle", "light", "heater", "warmth", ["shadow", "noise", "receipt"], "A candle produces light. A heater produces warmth."),
]


def build_spelling(old: dict, index: int) -> dict:
    word, wrongs, why = SPELLING[index]
    options, key = pack(word, [w.capitalize() if word[:1].isupper() else w for w in wrongs], old["id"])
    # Show the choices in sentence case for the correct word too.
    options = [option[:1].upper() + option[1:] if option[:1].islower() else option for option in options]
    correct = options[key]
    stem = f"Which spelling is correct for the word meaning the standard form of “{word}”?"
    # The stem above gives the answer away. Ask without printing the correct spelling as the only readable word.
    stem = "Which spelling is the standard one?"
    # Still too bare and duplicates. Include a short clue that is not the spelling.
    clues = [
        "to get something that was sent",
        "needed, not optional",
        "in a public way",
        "a chart of months",
        "clear and fixed",
        "the surroundings",
        "the ruling body of a state",
        "a group assigned to a task",
        "a promise that something will be done",
        "to suggest as suitable",
        "a fellow worker",
        "letters exchanged",
        "from time to time",
        "steady effort",
        "a burial ground",
        "to trouble someone repeatedly",
        "easy to see",
        "connected to the matter",
        "a repeating beat",
        "a noncommissioned officer",
        "an empty space without air",
        "strange",
        "to reach a goal",
        "to accept as true",
        "from another country",
        "how tall something is",
        "a place that lends books",
        "a person who lives next door",
        "an occupation",
        "a place that serves meals",
        "a timetable",
        "the day after today",
        "a person one knows",
        "a person who receives a benefit",
        "general agreement",
        "the work of keeping something in good condition",
    ]
    stem = f"Choose the correctly spelled word for this meaning: {clues[index]}."
    explanation = explain(correct, why, [option for i, option in enumerate(options) if i != key])
    return item(old, stem, options, key, explanation)


def build_meaning(old: dict, index: int) -> dict:
    kind, word, correct, wrongs, why = MEANINGS[index]
    if kind == "antonym":
        stem = f"Which word is the opposite of “{word}”?"
    else:
        stem = f"The word “{word}” most nearly means:"
    options, key = pack(correct, wrongs, old["id"])
    return item(old, stem, options, key, explain(options[key], why, [o for i, o in enumerate(options) if i != key]))


def build_analogy(old: dict, index: int) -> dict:
    left_a, left_b, right_a, correct, wrongs, why = ANALOGIES[index]
    stem = f"{left_a} is to {left_b} as {right_a} is to:"
    options, key = pack(correct, wrongs, old["id"])
    return item(old, stem, options, key, explain(options[key], why, [o for i, o in enumerate(options) if i != key]))
