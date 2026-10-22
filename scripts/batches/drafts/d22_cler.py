"""B1 subprofessional Clerical (40): 20 spelling (new bank-wide targets) + 20 filing items under ANSI/ARMA 12-2005.
Filing keys are computed here with this module's own indexer; qa.py rechecks them with arma_solver.py."""
import re
from d22_common import mk

T, D = "subprofessional", "clerical"
D_, I_, X_, S_, Q_ = "SPL-DOUBLE", "SPL-IE-EI", "SPL-DROP", "SPL-SILENT", "SPL-SOUND"
from spell_2026_10_22 import SPELL  # noqa: E402
EXPL = {D_: "doubles or undoubles a letter", I_: "swaps the order of i and e", X_: "drops a letter", S_: "drops a silent letter", Q_: "spells the word the way it sounds"}
FOILS = ["memorandum", "procurement", "voucher", "treasurer", "receptionist", "affidavit"]
ITEMS = []
n = 0
for k, (w, ms, meaning, sent) in enumerate(SPELL):
    n += 1
    iid = f"CIVIO-D1022-SPCLR-{n:04d}"
    tip = "Say the word slowly by syllable and picture each part: " + "-".join(re.findall(r"[^aeiou]*[aeiou]+(?:[^aeiou](?![aeiou]))?", w)) + "."
    if k % 10 < 7:  # spelled-correctly items
        opts_ = [w] + [m for m, _ in ms]
        frame = (f"Which word is spelled correctly?  " if k < 10 else f"Which spelling belongs in the blank? \"{sent}\"  ")
        stem = frame + " | ".join(sorted(opts_, key=lambda t: (len(t), t)))
        ITEMS.append(mk(id=iid, track=T, domain=D, competency="Spelling", concept="spelling", micro_skill="recognize the standard spelling of a commonly misspelled word",
                        archetype="CLR-SPELL-RIGHT", difficulty="easy", est=15 if k < 10 else 20, stem=stem, correct=w,
                        wrong=[(m, c, f"\"{m}\" {EXPL[c]}; the standard spelling is \"{w}\".") for m, c in ms],
                        terms=f"\"{w}\" means {meaning}.", shortcut=tip,
                        why_correct=f"\"{w}\" is the standard spelling (Merriam-Webster). Each other choice is a real-world misspelling: one letter pattern is changed, dropped or doubled. Check doubled letters and vowel pairs first; they are where most spelling errors happen."))
    else:  # misspelled-word items
        m, c = ms[0]
        foils = FOILS[(k % 10 - 7) * 2:(k % 10 - 7) * 2 + 2] + [SPELL[(k + 5) % 20][0]]
        opts_ = [m] + foils
        stem = "Which word is misspelled?  " + " | ".join(sorted(opts_, key=lambda t: (len(t), t)))
        ITEMS.append(mk(id=iid, track=T, domain=D, competency="Spelling", concept="spelling", micro_skill="spot the misspelled word among correct ones",
                        archetype="CLR-SPELL-WRONG", difficulty="easy", est=15, stem=stem, correct=m,
                        wrong=[(f, "CLR-SPELL-CORRECT-FOIL", f"\"{f}\" is spelled correctly, so it is not the answer.") for f in foils],
                        terms=f"\"{w}\" means {meaning}. The misspelling here {EXPL[c]}.", shortcut=tip,
                        why_correct=f"\"{m}\" is misspelled: it {EXPL[c]}. The standard spelling is \"{w}\" (Merriam-Webster). The other three words are spelled correctly, so they are foils.",
                        error_code=c))

# ---------- Filing (ARMA) ----------
TITLES = {"dr", "atty", "engr", "mr", "mrs", "ms", "hon", "prof"}
PREF = {"de", "del", "dela", "delos", "san", "santa", "van", "von"}
ROM = {"ii": 2, "iii": 3, "iv": 4}


def c_(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def ix_person(nm):
    t = nm.split()
    tail = None
    if c_(t[0]) in TITLES:
        tail = c_(t.pop(0))
    if c_(t[-1]) in {"jr", "sr"} | set(ROM):
        tail = c_(t.pop())
    if any(re.fullmatch(r"[A-Z]\.", x) for x in t):
        j = max(i for i, x in enumerate(t) if re.fullmatch(r"[A-Z]\.", x))
        g, s = t[:j + 1], t[j + 1:]
    else:
        j = next((i for i, x in enumerate(t) if i >= 1 and c_(x) in PREF), len(t) - 1)
        g, s = t[:j], t[j:]
    u = [(1, 0, "".join(c_(x) for x in s))] + [(1, 0, c_(x)) for x in g]
    if tail:
        u.append((0, ROM[tail], "") if tail in ROM else (1, 0, tail))
    return u


def ix_bus(nm):
    t = nm.replace("&", " and ").split()
    if t[0].lower() == "the":
        t = t[1:] + ["the"]
    out = []
    for x in t:
        m = re.fullmatch(r"(\d+)(st|nd|rd|th)?", c_(x))
        out.append((0, int(m.group(1)), "") if m else (1, 0, c_(x)))
    return out


def show(u):
    return " / ".join(x[2].upper() if x[0] else str(x[1]) for x in u)


SUBR = {
    "prefix": ("CLR-PREFIX-SPLIT: breaks ARMA Rule 6 (a prefix joins the rest of the surname as one unit)", 6),
    "first": ("CLR-FIRSTNAME-FIRST: breaks ARMA Rule 1 (personal names are indexed surname first)", 1),
    "title": ("CLR-TITLE-COUNTED: breaks ARMA Rule 5 (a title or suffix is the last unit)", 5),
    "mc": ("CLR-LETTER-ORDER: breaks ARMA Rule 6 (Mc is indexed as written, not as Mac)", 6),
    "hyphen": ("CLR-LETTER-ORDER: breaks ARMA Rule 3 (a hyphenated name is one unit)", 3),
    "abbr": ("CLR-LETTER-ORDER: breaks ARMA Rule 4 (abbreviations are indexed as written, not spelled out)", 4),
    "suffix": ("CLR-LETTER-ORDER: breaks ARMA Rule 5 (numeric suffixes such as II file before alphabetic ones such as Jr.)", 5),
    "the": ("CLR-ARTICLE-COUNTED: breaks ARMA Rule 2 (a leading \"The\" is the last unit)", 2),
    "amp": ("CLR-LETTER-ORDER: breaks ARMA Rule 2 (the symbol & is indexed as the word \"and\")", 2),
    "poss": ("CLR-LETTER-ORDER: breaks ARMA Rule 3 (drop the apostrophe but keep the s: Nena's = NENAS)", 3),
    "numval": ("CLR-LETTER-ORDER: breaks ARMA Rule 7 (numbers file in ascending order of value, not digit by digit)", 7),
    "numfirst": ("CLR-LETTER-ORDER: breaks ARMA Rule 7 (names that begin with digits file before names that begin with letters)", 7),
    "org": ("CLR-LETTER-ORDER: breaks ARMA Rule 8 (an organization is indexed as written, starting with its first word)", 8),
    "unit": ("CLR-LETTER-ORDER: breaks ARMA Rule 1 (compare unit by unit, letter by letter; nothing comes before something)", 1),
}
RULE = {1: "Index each name into units and compare unit by unit, letter by letter; nothing comes before something (ARMA Rule 1).",
        2: "Read & as \"and\" and treat a leading \"The\" as the last unit (ARMA Rule 2).",
        3: "Ignore punctuation; a hyphenated or possessive name is one unit with the marks removed (ARMA Rule 3).",
        4: "Index abbreviations such as Ma. or St. exactly as written; do not spell them out (ARMA Rule 4).",
        5: "A title (Dr., Atty.) or suffix (Jr., II) is the last unit; numeric suffixes file before alphabetic ones (ARMA Rule 5).",
        6: "A surname prefix (de, dela, del, delos, san) joins the rest of the surname as one unit, and Mc is spelled as written (ARMA Rule 6).",
        7: "Names that start with digits file before names that start with letters, in ascending order of value; ordinal endings are ignored (ARMA Rule 7).",
        8: "Index an organization's name as written, starting with its first word (ARMA Rule 8)."}
ARMA = "This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule {}), not a rule published by the CSC."
INTRO = ["Under ANSI/ARMA 12-2005, a clerk files these folders alphabetically. Which name goes {r}?",
         "A records officer indexes four personal names using the ARMA filing rules. Which name is filed {r}?",
         "Applying the ARMA simplified filing rules, which of these {kind} names comes {r} in the drawer?",
         "A municipal records section sorts new folders by ARMA rules. Which {kind} name should be placed {r}?"]
FIL = [  # (kind, names, rank, rule, {name: subreason})
 ("personal", ["Ana dela Cruz", "Ben Del Rosario", "Carlo De Guzman", "Dina Delos Reyes"], "FIRST", 6, {"Ana dela Cruz": "unit", "Ben Del Rosario": "prefix", "Dina Delos Reyes": "prefix"}),
 ("personal", ["Dr. Elena Ramos", "Atty. Felix Ramos", "Engr. Gina Ramirez", "Hon. Ivan Ramos"], "LAST", 5, {"Dr. Elena Ramos": "title", "Atty. Felix Ramos": "title", "Engr. Gina Ramirez": "title"}),
 ("personal", ["Mark Santos", "Marko Santos", "Mark A. Santos", "Marco Santos"], "THIRD", 1, {"Mark Santos": "unit", "Marko Santos": "unit", "Marco Santos": "unit"}),
 ("personal", ["Lea Reyes-Tan", "Lea Reyes", "Lea Reyesa", "Leo Reyes"], "LAST", 3, {"Lea Reyes": "hyphen", "Lea Reyesa": "hyphen", "Leo Reyes": "unit"}),
 ("personal", ["Paolo San Diego", "Paolo Sandoval", "Paolo Santiago", "Paolo San Jose"], "THIRD", 6, {"Paolo San Diego": "prefix", "Paolo Sandoval": "prefix", "Paolo Santiago": "prefix"}),
 ("personal", ["Zeny Abad", "Adela Zamora", "Bert Yap", "Yolly Bautista"], "SECOND", 1, {"Zeny Abad": "first", "Adela Zamora": "first", "Bert Yap": "first"}),
 ("personal", ["Dr. Rosa Lim", "Rosa Lim", "Rosa Lim-Ong", "Rosa Limbo"], "SECOND", 5, {"Rosa Lim": "title", "Rosa Lim-Ong": "hyphen", "Rosa Limbo": "unit"}),
 ("business", ["The Sampaguita Bakery", "Sampaguita Bakeshop", "Sampaguita Bakery and Cafe", "Sampaguita Bake House"], "THIRD", 2, {"Sampaguita Bakeshop": "unit", "Sampaguita Bakery and Cafe": "the", "Sampaguita Bake House": "unit"}),
 ("business", ["Cruz & Sons Hardware", "Cruz Andres Trading", "Cruz Hardware", "Cruz and Daughters Store"], "SECOND", 2, {"Cruz Andres Trading": "amp", "Cruz Hardware": "amp", "Cruz and Daughters Store": "unit"}),
 ("business", ["Nena's Carinderia", "Nenas Laundry Shop", "Nena Carinderia", "Nenita's Salon"], "SECOND", 3, {"Nenas Laundry Shop": "poss", "Nena Carinderia": "poss", "Nenita's Salon": "unit"}),
 ("organization", ["Philippine Red Cross", "Red Bank Lending", "Philippine Ports Authority", "Redwood Tutorial Center"], "SECOND", 8, {"Red Bank Lending": "org", "Philippine Ports Authority": "unit", "Redwood Tutorial Center": "org"}),
 ("personal", ["Carmela Ortiz", "Carmelo Ortiz", "Carmen Ortiz", "Carmina Ortega"], "SECOND", 1, {"Carmela Ortiz": "unit", "Carmelo Ortiz": "unit", "Carmina Ortega": "unit"}),
 ("personal", ["Noel B. Villar", "Noel Villar", "Noel Bautista Villar", "Noelle Villar"], "FIRST", 1, {"Noel B. Villar": "unit", "Noel Bautista Villar": "unit", "Noelle Villar": "unit"}),
 ("personal", ["Gil Pascual", "Pascual Gil", "Gilda Pascua", "Gil Pascua"], "LAST", 1, {"Gil Pascual": "first", "Gilda Pascua": "unit", "Gil Pascua": "unit"}),
 ("personal", ["Rey Tolentino", "Tess Tolentino", "Rey Tolentin", "Ruth Tolentino"], "THIRD", 1, {"Rey Tolentino": "unit", "Tess Tolentino": "unit", "Rey Tolentin": "unit"}),
 ("personal", ["Lorna Abaya", "Abaya Lorna", "Lorena Abayan", "Lorna Abad"], "SECOND", 1, {"Abaya Lorna": "first", "Lorena Abayan": "unit", "Lorna Abad": "unit"}),
 ("personal", ["Hon. Pia Buenaventura", "Pia Buenavista", "Engr. Pio Buenaventura", "Pia Buenaventura"], "FIRST", 5, {"Hon. Pia Buenaventura": "title", "Pia Buenavista": "unit", "Engr. Pio Buenaventura": "title"}),
 ("personal", ["Arnel de Vera", "Arnel Dejesus", "Arnel Deveza", "Arnel De Venecia"], "SECOND", 6, {"Arnel Dejesus": "prefix", "Arnel Deveza": "prefix", "Arnel De Venecia": "prefix"}),
 ("personal", ["Susan Santa Maria", "Susan Santamarina", "Susan Santana", "Susan Sant"], "LAST", 6, {"Susan Santamarina": "prefix", "Susan Santana": "unit", "Susan Sant": "unit"}),
 ("business", ["The Green Leaf Market", "Green Field Movers", "Greenhills Dental", "Green Leaf Catering"], "LAST", 2, {"Green Field Movers": "unit", "Greenhills Dental": "unit", "Green Leaf Catering": "the"}),
 ("business", ["Lopez & Rivera Law Office", "Lopez Andrada Clinic", "Lopez Auto Supply", "Lopez and Reyes Bakery"], "FIRST", 2, {"Lopez & Rivera Law Office": "amp", "Lopez Auto Supply": "amp", "Lopez and Reyes Bakery": "unit"}),
 ("business", ["Mabuhay Pawnshop", "Mabuhay Pharmacy", "Mabuhay Pawn and Lending", "Mabuhay Print Center"], "SECOND", 1, {"Mabuhay Pawnshop": "unit", "Mabuhay Pharmacy": "unit", "Mabuhay Print Center": "unit"}),
 ("business", ["Sunrise Water Refilling", "Sun Rise Bakery", "Sunrise Bakery", "Sunray Motors"], "THIRD", 1, {"Sun Rise Bakery": "unit", "Sunrise Water Refilling": "unit", "Sunray Motors": "unit"}),
 ("organization", ["National Food Authority", "National Irrigation Administration", "Nation Builders Cooperative", "Natural Farming Association"], "SECOND", 8, {"National Irrigation Administration": "org", "Nation Builders Cooperative": "org", "Natural Farming Association": "org"}),
 ("organization", ["Land Bank of the Philippines", "Land Transportation Office", "Landmark Realty", "Land Registration Authority"], "THIRD", 8, {"Land Bank of the Philippines": "org", "Land Registration Authority": "org", "Landmark Realty": "unit"}),
 ("business", ["The Daily Grind Cafe", "Daily Bread Bakery", "Daily Fresh Grocery", "Dailyn Boutique"], "SECOND", 2, {"Daily Bread Bakery": "unit", "Daily Fresh Grocery": "unit", "Dailyn Boutique": "unit"}),
 ("personal", ["Atty. Lito Agustin", "Lito Agustin", "Dr. Lita Agustin", "Lito Agustines"], "LAST", 5, {"Atty. Lito Agustin": "title", "Lito Agustin": "unit", "Dr. Lita Agustin": "title"}),

 ("business", ["Bayan Water District", "Bayani Cooperative", "Bayan Rural Bank", "Bayanihan Clinic"], "SECOND", 1, {"Bayani Cooperative": "unit", "Bayan Rural Bank": "unit", "Bayanihan Clinic": "unit"}),
]
RANK = {"FIRST": 0, "SECOND": 1, "THIRD": 2, "LAST": -1}
for k, (kind, names, r, rule, subs) in enumerate(FIL):
    n += 1
    ix = ix_person if kind == "personal" else ix_bus
    order = sorted(names, key=ix)
    key = order[RANK[r]]
    intro = INTRO[k % 4]
    if k % 4 == 1 and kind != "personal":
        intro = INTRO[0]
    q = intro.format(r=r, kind=kind)
    if kind != "personal" and not re.search(r"business|organization", q, re.I):
        q = q.replace("Which name", f"Which {kind} name")
    stem = q + "\n" + " | ".join(names)
    subs = {nm: subs.get(nm, {1: "unit", 2: "unit", 5: "title", 6: "prefix", 8: "org"}.get(rule, "unit")) for nm in names if nm != key}
    pos = {nm: order.index(nm) + 1 for nm in names}
    wrong = []
    sub = {}
    for nm in names:
        if nm == key:
            continue
        txt, rn = SUBR[subs[nm]]
        wrong.append((nm, "CLR-FILE-ORDER", f"\"{nm}\" indexes as {show(ix(nm))} and files {['first', 'second', 'third', 'fourth'][pos[nm] - 1]}, so it is not {r.lower()}. Picking it {txt.split('(')[1].rstrip(')').lower() if False else 'ignores this: ' + txt.split('(')[1].rstrip(')')}."))
        sub[nm] = txt
    item = mk(id=f"CIVIO-D1022-SPCLR-{n:04d}", track=T, domain=D, competency="Filing", concept="alphabetic filing (ARMA rules)",
              micro_skill=f"apply ARMA Rule {rule} when indexing", archetype="CLR-FILE-POSITION" if kind == "personal" else "CLR-FILE-BUSINESS",
              difficulty="medium", est=45 if kind == "personal" else 50, stem=stem, correct=key, wrong=wrong,
              terms="Indexing writes a name as filing units: surname, given name, middle initial for people; words as written for businesses. Compare unit by unit, letter by letter.",
              shortcut="Rewrite each name in indexed form first, then sort the rewritten forms.",
              why_correct=f"\"{key}\" is filed {r.lower()}. Indexed order: " + "; ".join(show(ix(x)) for x in order) + f". {RULE[rule]} {ARMA.format(rule)} Source standard: ANSI/ARMA 12-2005.",
              source="Civio Filing Rules v2 / ANSI/ARMA 12-2005", url="https://webstore.ansi.org/standards/arma/ansiarma122005")
    by_text = {o["text"]: o["option_id"] for o in item["options"]}
    item["distractor_subreason"] = {by_text[nm]: v for nm, v in sub.items()}
    ITEMS.append(item)

ORD = [
 ("personal", ["Rosa delos Santos", "Rosa Delgado", "Rosa de Leon", "Rosa Del Rosario"], 6,
  [("2, 3, 4, 1", "prefix", "files under the part after the prefix (Leon, Rosario, Santos)"), ("3, 2, 4, 1", "unit", "puts DELROSARIO before DELOSSANTOS; compare letter by letter: O comes before R"), ("2, 3, 1, 4", "unit", "puts DELGADO before DELEON; E comes before G")]),
 ("business", ["The Bay Leaf Cafe", "Bay Area Movers", "B & B Pharmacy", "Baywalk Inn"], 2,
  [("3, 2, 4, 1", "the", "files The Bay Leaf Cafe under T"), ("2, 3, 1, 4", "amp", "drops the & so B & B Pharmacy loses its first-unit place"), ("1, 2, 3, 4", "unit", "keeps the order as listed without indexing")]),
]
for kind, names, rule, wr in ORD:
    n += 1
    ix = ix_person if kind == "personal" else ix_bus
    order = sorted(range(4), key=lambda i: ix(names[i]))
    key = ", ".join(str(i + 1) for i in order)
    q = (f"Arrange these {'personal' if kind == 'personal' else 'business'} names in ARMA filing order. Which sequence is correct?\n"
         + "\n".join(f"{i + 1}. {nm}" for i, nm in enumerate(names)))
    item = mk(id=f"CIVIO-D1022-SPCLR-{n:04d}", track=T, domain=D, competency="Filing", concept="alphabetic filing (ARMA rules)",
              micro_skill=f"apply ARMA Rule {rule} to a full sequence", archetype="CLR-FILE-ORDER", difficulty="medium", est=60, stem=q, correct=key,
              wrong=[(t, "CLR-FILE-ORDER", f"This sequence {why}.") for t, s, why in wr],
              terms="Indexing writes a name as filing units; a full sequence is right only if every pair is in order.",
              shortcut="Index all four names first, then sort; check the two closest names letter by letter.",
              why_correct=f"Correct sequence {key}. Indexed order: " + "; ".join(show(ix(names[i])) for i in order) + f". {RULE[rule]} {ARMA.format(rule)} Source standard: ANSI/ARMA 12-2005.",
              source="Civio Filing Rules v2 / ANSI/ARMA 12-2005", url="https://webstore.ansi.org/standards/arma/ansiarma122005")
    by_text = {o["text"]: o["option_id"] for o in item["options"]}
    item["distractor_subreason"] = {by_text[t]: SUBR[s][0] for t, s, _ in wr}
    ITEMS.append(item)
