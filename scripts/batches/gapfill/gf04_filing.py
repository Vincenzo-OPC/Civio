"""gap-fill-2000-04, Clerical filing: hand-written name sets, keys and traps derived by the ARMA rules below.
Each set lists the four names, the rank asked (or ORDER), the ARMA rule it targets, and the name type.
The key is checked a second time by scripts/batches/arma_solver.py through qa.py."""
import re

ARMA = "This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule {}), not a rule published by the CSC."
TITLES = ["Dr.", "Atty.", "Engr.", "Mrs.", "Hon.", "Prof."]
SUFFIXES = {"Jr.": None, "Sr.": None, "II": 2, "III": 3, "IV": 4}
PREF = ["de los", "de la", "delos", "dela", "del", "de", "san", "santa", "van", "mac", "mc", "o'"]
ABBR = {"St.": "Saint", "Sto.": "Santo", "Sta.": "Santa", "Mt.": "Mount", "Ma.": "Maria", "Gen.": "General", "Bro.": "Brother", "Ft.": "Fort"}
GENERIC = {"university", "college", "association", "samahan", "kapisanan", "foundation", "institute", "society", "federation", "league",
           "cooperative", "club", "of", "ng", "mga", "the", "and", "para", "sa"}


def letters(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def U(t):
    c = letters(t)
    m = re.fullmatch(r"(\d+)(st|nd|rd|th)?", c)
    return (0, int(m.group(1)), "") if m else (1, 0, c)


# ---------- personal names ----------
def parse_person(n):
    toks = n.split()
    title = toks.pop(0) if toks[0] in TITLES else None
    suf = toks.pop() if toks[-1] in SUFFIXES else None
    mi = next(i for i, t in enumerate(toks) if re.fullmatch(r"[A-Z]\.", t))
    return dict(title=title, suf=suf, given=toks[:mi], mid=toks[mi], sur=toks[mi + 1:])


def last_unit(p, alpha_first=False):
    x = p["title"] or p["suf"]
    if not x:
        return []
    v = SUFFIXES.get(x)
    if alpha_first:
        return [(0, 0, letters(x))] if v is None else [(1, 0, letters(x))]
    return [(0, v, "")] if v is not None else [(1, 0, letters(x))]


def idx_person(n, mode=None):
    p = parse_person(n)
    sur = " ".join(p["sur"])
    if mode == "prefix_split":
        low = sur.lower()
        for pre in PREF:
            if low.startswith(pre) and len(low) > len(pre):
                sur = sur[len(pre):].strip(" '")
                break
        else:
            return None
    if mode == "mc_as_mac":
        if not sur.lower().startswith("mc"):
            return None
        sur = "Mac" + sur[2:]
    if mode == "hyphen_split":
        if "-" not in sur:
            return None
        surs = [(1, 0, letters(x)) for x in sur.split("-")]
    else:
        surs = [(1, 0, letters(sur))]
    given = p["given"]
    if mode == "abbrev_spelled":
        if not any(g in ABBR for g in given):
            return None
        given = [ABBR.get(g, g) for g in given]
    g = [(1, 0, letters(x)) for x in given] + [(1, 0, letters(p["mid"]))]
    lu = last_unit(p, alpha_first=(mode == "suffix_alpha"))
    if mode == "firstname_first":
        return g + surs + lu
    if mode == "title_counted":
        return lu + surs + g if lu else surs + g
    return surs + g + lu


def show_person(n):
    p = parse_person(n)
    out = [letters(" ".join(p["sur"])).upper()] + [letters(x).upper() for x in p["given"]] + [letters(p["mid"]).upper()]
    x = p["title"] or p["suf"]
    if x:
        out.append(letters(x).upper())
    return " / ".join(out)


# ---------- business names ----------
def idx_business(n, mode=None):
    toks = n.split()
    if mode == "symbol_ignored":
        if "&" not in toks:
            return None
        toks = [t for t in toks if t != "&"]
    else:
        toks = ["and" if t == "&" else t for t in toks]
    if mode == "abbrev_spelled":
        if not any(t in ABBR for t in toks):
            return None
        toks = [ABBR.get(t, t) for t in toks]
    if mode == "possessive_dropped":
        if not any(t.endswith("'s") for t in toks):
            return None
        toks = [t[:-2] if t.endswith("'s") else t for t in toks]
    if mode == "hyphen_split":
        if not any("-" in t for t in toks):
            return None
        toks = [x for t in toks for x in t.split("-")]
    if mode == "org_keyword":
        if toks[0].lower() not in GENERIC:
            return None
        toks = [t for t in toks if t.lower() not in GENERIC] + toks
    if toks[0].lower() == "the" and mode != "article_counted":
        toks = toks[1:] + [toks[0]]
    elif mode == "article_counted" and toks[0].lower() != "the":
        pass
    units = [U(t) for t in toks if letters(t)]
    if mode == "num_text":
        if not any(u[0] == 0 for u in units):
            return None
        units = [(0, 0, str(u[1])) if u[0] == 0 else u for u in units]
        units = [(0, 0, u[2]) if u[0] == 0 else (1, 0, u[2]) for u in units]
    if mode == "num_after":
        if not any(u[0] == 0 for u in units):
            return None
        units = [(2, u[1], "") if u[0] == 0 else u for u in units]
    return units


def show_business(n):
    toks = ["AND" if t == "&" else t for t in n.split()]
    if toks[0].lower() == "the":
        toks = toks[1:] + [toks[0]]
    return " / ".join(re.sub(r"[^A-Za-z0-9]", "", t).upper() for t in toks if letters(t))


MIS_P = ["prefix_split", "firstname_first", "title_counted", "mc_as_mac", "hyphen_split", "abbrev_spelled", "suffix_alpha"]
MIS_B = ["article_counted", "symbol_ignored", "possessive_dropped", "abbrev_spelled", "hyphen_split", "num_text", "num_after", "org_keyword"]
SUB = {
    "prefix_split": ("CLR-PREFIX-SPLIT: breaks ARMA Rule 6 (a prefix joins the rest of the surname as one unit)", "split the surname prefix off and filed the name under the rest of the surname"),
    "firstname_first": ("CLR-FIRSTNAME-FIRST: breaks ARMA Rule 1 (personal names are indexed surname first)", "sorted by the given name instead of the surname"),
    "title_counted": ("CLR-TITLE-COUNTED: breaks ARMA Rule 5 (a title or suffix is the last unit)", "sorted by the title or suffix instead of treating it as the last unit"),
    "mc_as_mac": ("CLR-LETTER-ORDER: breaks ARMA Rule 6 (Mc is indexed as written, not as Mac)", "filed Mc as if it were spelled Mac"),
    "hyphen_split": ("CLR-LETTER-ORDER: breaks ARMA Rule 3 (a hyphenated name is one unit)", "split the hyphenated name into two units"),
    "abbrev_spelled": ("CLR-LETTER-ORDER: breaks ARMA Rule 4 (abbreviations are indexed as written, not spelled out)", "spelled out the abbreviation instead of indexing it as written"),
    "suffix_alpha": ("CLR-LETTER-ORDER: breaks ARMA Rule 5 (numeric suffixes such as II file before alphabetic ones such as Jr.)", "filed the alphabetic suffix (Jr., Sr.) before the numeric one (II, III)"),
    "article_counted": ("CLR-ARTICLE-COUNTED: breaks ARMA Rule 2 (a leading \"The\" is the last unit)", "filed the name under its leading \"The\""),
    "symbol_ignored": ("CLR-LETTER-ORDER: breaks ARMA Rule 2 (the symbol & is indexed as the word \"and\")", "skipped the & instead of reading it as \"and\""),
    "possessive_dropped": ("CLR-LETTER-ORDER: breaks ARMA Rule 3 (drop the apostrophe but keep the s: Nena's = NENAS)", "dropped the possessive s along with the apostrophe"),
    "num_text": ("CLR-LETTER-ORDER: breaks ARMA Rule 7 (numbers file in ascending order of value, not digit by digit)", "compared the numbers digit by digit instead of by value"),
    "num_after": ("CLR-LETTER-ORDER: breaks ARMA Rule 7 (names that begin with digits file before names that begin with letters)", "filed the names that begin with digits after the names that begin with letters"),
    "org_keyword": ("CLR-LETTER-ORDER: breaks ARMA Rule 8 (an organization is indexed as written, starting with its first word)", "filed the organization under its key word instead of its first word as written"),
    "generic": ("CLR-LETTER-ORDER: breaks ARMA Rule 1 (compare unit by unit, letter by letter)", None),
}
RULE_TEXT = {
    1: "Index each name into units and compare unit by unit, letter by letter; nothing comes before something (ARMA Rule 1).",
    2: "Read & as \"and\" and treat a leading \"The\" as the last unit (ARMA Rule 2).",
    3: "Ignore punctuation; a hyphenated or possessive name is one unit with the marks removed (ARMA Rule 3).",
    4: "Index abbreviations, acronyms and short forms such as Ma. or St. exactly as written; do not spell them out (ARMA Rule 4).",
    5: "A title (Dr., Atty.) or suffix (Jr., II) is the last unit; numeric suffixes file before alphabetic ones (ARMA Rule 5).",
    6: "A surname prefix (de, dela, del, delos, san, van, Mc, O') joins the rest of the surname as one unit, spelled as written (ARMA Rule 6).",
    7: "Names that start with digits file before names that start with letters, in ascending order of value; ordinal endings are ignored (ARMA Rule 7).",
    8: "Index an organization's name as written on its letterhead, starting with its first word (ARMA Rule 8).",
}
SHORT = {
    2: "Rewrite first: & becomes \"and\", and a leading \"The\" moves to the end. Then compare word by word.",
    3: "Erase hyphens, apostrophes and periods, then join: Reyes-Tan becomes REYESTAN, Nena's becomes NENAS.",
    4: "Index short forms exactly as printed: St. is ST, Ma. is MA. Do not expand them.",
    5: "Cover the title or suffix with your thumb; use it only to break a tie, and II comes before Jr.",
    6: "Glue the prefix to the surname (San Diego = SANDIEGO) and spell Mc and O' as written.",
    7: "Digits first, smallest value first: 8 comes before 15. Drop -st, -nd, -rd, -th.",
    8: "File the name as printed on the letterhead. Do not jump to the key word.",
}
ORD = {0: "first", 1: "second", 2: "third", 3: "last"}


def index(kind, n, mode=None):
    f = idx_person if kind == "P" else idx_business
    r = f(n, mode) if mode else None
    return r if r is not None else f(n)


def concat_ok(kind, names):
    """Business names: unit-by-unit order must equal plain letter-by-letter order (avoids disputed word-by-word cases)."""
    if kind != "B" or any(re.search(r"\d", n) for n in names):
        return True
    a = sorted(names, key=lambda n: index("B", n))
    b = sorted(names, key=lambda n: "".join(u[2] for u in index("B", n)))
    return a == b


def build(n, rank, kind, rule, names, prefix="CIVIO-GF2K04"):
    show = show_person if kind == "P" else show_business
    assert len(set(names)) == 4
    keyed = [tuple(index(kind, x)) for x in names]
    assert len(set(keyed)) == 4, ("tie", names)
    assert concat_ok(kind, names), ("disputed word-by-word vs letter-by-letter", names)
    order = sorted(names, key=lambda x: index(kind, x))
    mis = sorted(MIS_P if kind == "P" else MIS_B, key=lambda m: f"Rule {rule} " not in SUB[m][0])
    noun = "personal name" if kind == "P" else "business name"
    traps = {}
    if rank != "ORDER":
        r = {"FIRST": 0, "SECOND": 1, "THIRD": 2, "LAST": 3}[rank]
        key = order[r]
        for m in mis:
            w = sorted(names, key=lambda x: index(kind, x, m))[r]
            if w != key and w not in traps:
                traps[w] = m
        wrong = [x for x in names if x != key]
        for x in wrong:
            traps.setdefault(x, "generic")
        stems = {"FIRST": ["Under ARMA alphabetic filing rules, which {} is filed FIRST?", "A records clerk files these four folders alphabetically. Which {} goes FIRST in the drawer?"],
                 "LAST": ["Under ARMA alphabetic filing rules, which {} is filed LAST?", "A records clerk files these four folders alphabetically. Which {} goes LAST in the drawer?"],
                 "SECOND": ["Using standard alphabetic indexing, which {} comes SECOND?"],
                 "THIRD": ["Using standard alphabetic indexing, which {} comes THIRD?"]}[rank]
        stem = stems[n % len(stems)].format(noun) + "\n" + " | ".join(names)
        others = wrong
        slot = n % 4
        opts = others[:]
        opts.insert(slot, key)
        why_w, sub = {}, {}
        pos = {x: order.index(x) for x in names}
        for x in wrong:
            m = traps[x]
            if m == "generic":
                why_w[x] = f"\"{x}\" indexes as {show(x)} and files {ORD[pos[x]]}, not {ORD[r]}."
            else:
                why_w[x] = f"\"{x}\" is the answer only if you {SUB[m][1]}. Indexed correctly it is {show(x)}, which files {ORD[pos[x]]}."
            sub[x] = SUB[m][0]
        units = "; ".join(f"{show(x)}" for x in order)
        why_c = (f"\"{key}\" is filed {ORD[r]}. In filing order the indexed units are: {units}. {RULE_TEXT[rule]} "
                 + ARMA.format(rule) + " Source standard: ANSI/ARMA 12-2005.")
        arch = "CLR-FILE-POSITION" if kind == "P" else "CLR-FILE-BUSINESS"
        concept = "alphabetic filing of personal names" if kind == "P" else "business and organization filing (ARMA rules)"
        texts = opts
        est = 45 if kind == "P" else 50
    else:
        seq = lambda lst: ", ".join(str(names.index(x) + 1) for x in lst)
        key = seq(order)
        cand = {}
        for m in mis:
            s = seq(sorted(names, key=lambda x: index(kind, x, m)))
            if s != key and s not in cand:
                cand[s] = (m, None)
        for i in range(3):
            sw = order[:]
            sw[i], sw[i + 1] = sw[i + 1], sw[i]
            s = seq(sw)
            if s not in cand and s != key:
                cand[s] = ("generic", (order[i], order[i + 1]))
        wrong = list(cand)[:3]
        assert key.replace(", ", "") != "1234", names
        stem = (["Arrange these {}s in correct alphabetic filing order. Which sequence is correct?", "Which sequence files the four {}s below in ARMA alphabetic order?"][n % 2].format(noun)
                + "\n" + "\n".join(f"{i + 1}. {x}" for i, x in enumerate(names)))
        slot = n % 4
        texts = wrong[:]
        texts.insert(slot, key)
        why_w, sub = {}, {}
        for s in wrong:
            m, sw = cand[s]
            if m == "generic":
                a, b = sw
                why_w[s] = f"{s} puts \"{b}\" before \"{a}\", but {show(a)} comes before {show(b)} letter by letter."
            else:
                why_w[s] = f"{s} is the order you get if you {SUB[m][1]}."
            sub[s] = SUB[m][0]
            traps[s] = m
        units = "; ".join(f"{names.index(x) + 1}. {show(x)}" for x in order)
        why_c = f"The correct sequence is {key}. Indexed in filing order: {units}. {RULE_TEXT[rule]} " + ARMA.format(rule) + " Source standard: ANSI/ARMA 12-2005."
        arch = "CLR-FILE-ORDER"
        concept = "personal-name filing order (ARMA rules)" if kind == "P" else "business-name filing order (ARMA rules)"
        est = 60
    ids = ["o1", "o2", "o3", "o4"]
    oid = {t: ids[i] for i, t in enumerate(texts)}
    item = dict(id=f"{prefix}-{arch}-{n:04d}", track="subprofessional", domain="clerical", competency="Filing", concept=concept,
                micro_skill=f"apply ARMA Rule {rule} when indexing", archetype=arch, difficulty="medium" if rank != "ORDER" else "hard", est_seconds=est, language="en",
                stem=stem, options=[{"option_id": ids[i], "text": t} for i, t in enumerate(texts)], answer_option_id=oid[key],
                reveal={"terms": "Indexing means writing a name as filing units in order: surname, given name, middle initial for people; words as written for businesses. Compare unit by unit, letter by letter.",
                        "shortcut": SHORT.get(rule, "Index every name first, then compare unit by unit."), "why_correct": why_c,
                        "why_wrong": {oid[x]: why_w[x] for x in why_w}},
                distractor_reasoning={oid[x]: "CLR-FILE-ORDER" for x in why_w}, distractor_subreason={oid[x]: sub[x] for x in sub},
                source=f"Civio Filing Rules v2 / ARMA Rule {rule} (ANSI/ARMA 12-2005)", source_url="https://webstore.ansi.org/standards/arma/ansiarma122005",
                source_group="civio", status="draft", review_status="unreviewed",
                provenance={"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T04:00:00+08:00", "spec_version": "0.1.9"},
                shortcut=SHORT.get(rule, "Index every name first, then compare unit by unit."),
                notes="gap-fill-2000-04 (Clerical filing). Pending CoS.")
    ntrap = sum(1 for m in traps.values() if m != "generic")
    return item, ntrap
