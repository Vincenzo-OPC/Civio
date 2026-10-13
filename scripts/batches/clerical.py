"""Clerical Ability: spelling (coded misspellings) and ARMA filing (order computed by rule)."""
import re
from common import make, Skip

B = dict(track="subprofessional", domain="clerical")
ARMA_NOTE = "This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule {n}), not a rule published by the CSC."

WORDS = ["accommodate", "occurrence", "embarrass", "harass", "necessary", "committee", "receive", "achievement", "conscientious", "maintenance",
         "privilege", "separate", "definitely", "occasionally", "recommend", "questionnaire", "millennium", "personnel", "liaison", "bureaucracy",
         "reimbursement", "acknowledgment", "correspondence", "perseverance", "irrelevant", "guarantee", "surveillance", "lieutenant", "itinerary",
         "parliament", "pronunciation", "transferred", "accessible", "commitment", "deceive", "foreign", "weird", "seize", "believe", "grievance",
         "conscience", "exaggerate", "possession", "address", "beginning", "occurred", "colleague", "license", "miscellaneous", "rhythm",
         "vacuum", "existence", "independence", "attendance", "acquaintance", "convenience", "permissible", "noticeable", "manageable", "inoculate",
         "calendar", "cemetery", "dilemma", "entrepreneur", "fluorescent", "hierarchy", "jewelry", "mischievous", "omission", "phenomenon",
         "receipt", "schedule", "threshold", "unanimous", "withhold", "assessment", "allotment", "appropriation", "disbursement", "requisition"]
MISS = {"SPL-DOUBLE": "doubles or undoubles a consonant", "SPL-IE-EI": "swaps the order of i and e", "SPL-DROP": "drops a letter",
        "SPL-SOUND": "is spelled the way the word sounds"}


def misspell(w, rng):
    out = []
    m = [i for i in range(len(w) - 1) if w[i] == w[i + 1] and w[i] not in "aeiou"]
    if m:
        i = rng.choice(m)
        out.append((w[:i] + w[i + 1:], "SPL-DOUBLE"))
    else:
        c = [i for i in range(1, len(w) - 1) if w[i] in "lmnprst" and w[i - 1] in "aeiou" and w[i + 1] in "aeiou"]
        if c:
            i = rng.choice(c)
            out.append((w[:i] + w[i] + w[i:], "SPL-DOUBLE"))
    for a, b in (("ie", "ei"), ("ei", "ie")):
        if a in w:
            out.append((w.replace(a, b, 1), "SPL-IE-EI"))
            break
    for pat, rep in (("ance", "ence"), ("ence", "ance"), ("ible", "able"), ("able", "ible"), ("ph", "f"), ("sc", "s"), ("tion", "sion"),
                     ("ar", "er"), ("ous", "us"), ("ery", "ary"), ("eue", "ue"), ("ious", "eous"), ("ge", "j"), ("que", "k"), ("ment", "mant")):
        if pat in w:
            out.append((w.replace(pat, rep, 1), "SPL-SOUND"))
            break
    v = [i for i in range(2, len(w) - 2) if w[i] in "aeiou"]
    rng.shuffle(v)
    for i in v:
        out.append((w[:i] + w[i + 1:], "SPL-DROP"))
    seen, res = set(), []
    for t, c in out:
        if t != w and t not in seen and t not in WORDS:
            seen.add(t)
            res.append((t, c))
    return res


def spell_right(rng, iid):
    w = rng.choice(WORDS)
    ms = misspell(w, rng)
    codes, pick = set(), []
    for t, c in ms:
        if c not in codes or len(pick) + (3 - len(pick)) > len([x for x in ms if x[1] not in codes]):
            pick.append((t, c)); codes.add(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        raise Skip()
    it = make(id=iid, **B, competency="Spelling", concept="correct spelling", micro_skill="spot the correct spelling", archetype="CLR-SPELL-RIGHT",
              difficulty="medium", est=15, stem="Which word is spelled correctly?", correct=w,
              wrong=[(t, c, f"\"{t}\" {MISS[c]}. The correct spelling is \"{w}\".") for t, c in pick],
              terms="Look at each word letter by letter. Exactly one choice is spelled the standard way.",
              shortcut="Check the tricky spots first: double letters, i and e together, and endings like -ance/-ence and -able/-ible.",
              why_correct=f"\"{w}\" is the standard spelling.", rng=rng)
    it["stem"] += "  " + " | ".join(o["text"] for o in it["options"])
    it["_sig"] = "R:" + w
    return it


def spell_wrong(rng, iid):
    w = rng.choice(WORDS)
    ms = misspell(w, rng)
    if not ms:
        raise Skip()
    bad, code = rng.choice(ms)
    others = rng.sample([x for x in WORDS if x != w], 3)
    it = make(id=iid, **B, competency="Spelling", concept="misspelled word", micro_skill="find the one misspelled word", archetype="CLR-SPELL-WRONG",
              difficulty="medium", est=15, stem="Which word is misspelled?", correct=bad,
              wrong=[(o, "CLR-SPELL-WRONG", f"\"{o}\" is spelled correctly, even if it looks unusual.") for o in others],
              terms="Exactly one of the words has a spelling mistake. The others are correct.",
              shortcut="Scan for the usual traps: double letters, i and e order, dropped vowels and sound-alike endings.",
              why_correct=f"\"{bad}\" is misspelled: it {MISS[code]}. The correct spelling is \"{w}\".", rng=rng)
    it["stem"] += "  " + " | ".join(o["text"] for o in it["options"])
    it["_sig"] = "W:" + bad
    return it


GIVEN = ["Maria", "Jose", "Ana", "Juan", "Rosario", "Ramon", "Teresita", "Eduardo", "Liza", "Carlos", "Elena", "Mario", "Lourdes", "Andres", "Cristina", "Benito",
         "Gloria", "Felipe", "Nora", "Rodrigo", "Imelda", "Ernesto", "Corazon", "Danilo", "Victoria", "Alfredo", "Evelyn", "Rafael"]
MID = list("ABCDEFGLMNPRSTV")
PLAIN = ["Cruz", "Reyes", "Santos", "Bautista", "Garcia", "Mendoza", "Torres", "Ramos", "Castillo", "Flores", "Rivera", "Aquino", "Navarro", "Lopez",
         "Salazar", "Villanueva", "Dizon", "Pascual", "Leon", "Rosario", "Juan", "Pedro", "Jose", "Austria", "Lim", "Tan", "Ocampo", "Manalo"]
PREFIXED = ["Dela Cruz", "De Leon", "Del Rosario", "San Juan", "De los Santos", "San Pedro", "Delos Reyes", "De Guzman", "Dela Torre", "Del Mundo"]
HYPH = ["Garcia-Lopez", "Reyes-Tan", "Santos-Ocampo", "Cruz-Manalo"]
TITLES = ["Dr.", "Atty.", "Engr."]


def key_ok(p):
    t, g, m, s = p
    return (re.sub(r"[^a-z]", "", s.lower()), g.lower(), m.lower(), t)


def key_first(p):
    t, g, m, s = p
    return (g.lower(), re.sub(r"[^a-z]", "", s.lower()))


def key_split(p):
    t, g, m, s = p
    return (re.sub(r"[^a-z]", "", s.split()[-1].split("-")[0].lower()), g.lower())


def key_title(p):
    t, g, m, s = p
    return ((t or "").lower().rstrip("."), re.sub(r"[^a-z]", "", s.lower())) if t else ("zzz", "")


def show(p):
    t, g, m, s = p
    return f"{t + ' ' if t else ''}{g} {m}. {s}"


def idx(p):
    return re.sub(r"[^A-Za-z]", "", p[3]).upper()


def file_position(rng, iid):
    for _ in range(200):
        ppl = []
        for _ in range(4):
            r = rng.random()
            s = rng.choice(PREFIXED) if r < 0.35 else rng.choice(HYPH) if r < 0.45 else rng.choice(PLAIN)
            t = rng.choice(TITLES) if rng.random() < 0.3 else ""
            ppl.append((t, rng.choice(GIVEN), rng.choice(MID), s))
        if len({p[3] for p in ppl}) < 4 or len({p[1] for p in ppl}) < 4:
            continue
        last = rng.random() < 0.4
        pick = (max if last else min)
        c = pick(ppl, key=key_ok)
        traps = []
        for kf, code in ((key_split, "CLR-PREFIX-SPLIT"), (key_first, "CLR-FIRSTNAME-FIRST"), (key_title, "CLR-TITLE-COUNTED")):
            if kf is key_title and not any(p[0] for p in ppl):
                continue
            w = (max if last and kf is not key_title else min)(ppl, key=kf)
            if w != c and w not in [x[0] for x in traps]:
                traps.append((w, code))
        if len(traps) < 2:
            continue
        rest = [p for p in ppl if p != c and p not in [x[0] for x in traps]]
        if len(traps) == 2:
            if not rest:
                continue
            traps.append((rest[0], "CLR-WORD-BY-WORD" if False else "CLR-FILE-ORDER"))
        break
    else:
        raise Skip()
    order = sorted(ppl, key=key_ok)
    why = {"CLR-PREFIX-SPLIT": "files the prefix as a separate word (for example \"Dela Cruz\" under C). A prefix joins the rest of the surname",
           "CLR-FIRSTNAME-FIRST": "sorts by the given name. Personal names file by surname first",
           "CLR-TITLE-COUNTED": "sorts by the title (Dr., Atty., Engr.). A title is only the last unit",
           "CLR-FILE-ORDER": "is not at that end of the order"}
    usesprefix = any(" " in p[3] for p in ppl)
    rule = 6 if usesprefix else 5 if any(p[0] for p in ppl) else 1
    word = "LAST" if last else "FIRST"
    units = "; ".join(f"{show(p)} → {re.sub(r'[^A-Za-z]', '', p[3]).upper()}, {p[1]}" for p in order)
    it = make(id=iid, **B, competency="Filing", concept="alphabetic filing of personal names", micro_skill="surname, prefix and title rules",
              archetype="CLR-FILE-POSITION", difficulty="medium", est=45,
              stem=f"In alphabetical filing, which name is filed {word}?  " + " | ".join(show(p) for p in ppl), correct=show(c),
              wrong=[(show(p), "CLR-FILE-ORDER", f"\"{show(p)}\" {why[code]}." if code != "CLR-FILE-ORDER" else
                      f"\"{show(p)}\" files as {idx(p)}, which comes {'before' if last else 'after'} {idx(c)}.") for p, code in traps[:3]],
              terms="\"Indexing\" means writing a name in filing order: surname first, then given name, then middle initial. A title such as Dr. is the last unit.",
              shortcut=f"Rewrite each surname as one block: drop spaces and hyphens, keep the prefix (Dela Cruz = DELACRUZ). Then compare letter by letter (ARMA Rule 1). Order: {units}.",
              why_correct=f"\"{show(c)}\" is right. It comes {'last' if last else 'first'} when every name is indexed surname first, letter by letter. " + ARMA_NOTE.format(n=rule),
              source=f"Civio Filing Rules v2 / ARMA Rule {rule}", url="https://webstore.ansi.org/standards/arma/ansiarma122005", rng=rng)
    sub = {"CLR-PREFIX-SPLIT": "CLR-PREFIX-SPLIT: breaks ARMA Rule 6 (a prefix joins the rest of the surname as one unit)",
           "CLR-FIRSTNAME-FIRST": "CLR-FIRSTNAME-FIRST: breaks ARMA Rule 1 (personal names are indexed surname first)",
           "CLR-TITLE-COUNTED": "CLR-TITLE-COUNTED: breaks ARMA Rule 5 (a title is the last unit, used only to break ties)",
           "CLR-FILE-ORDER": "CLR-LETTER-ORDER: breaks ARMA Rule 1 (compare unit by unit, letter by letter)"}
    shown = {show(p): code for p, code in traps[:3]}
    txt = {o["option_id"]: o["text"] for o in it["options"]}
    it["distractor_subreason"] = {oid: sub[shown[txt[oid]]] for oid in it["distractor_reasoning"]}
    it["_sig"] = it["stem"]
    return it


TEMPLATES = [spell_right, spell_wrong, file_position, file_position]
