"""Gap fill 003: ARMA Rules 2, 3, 4, 7, 8 business/organization filing drafts. Each key is computed from indexed units."""
import json, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ROMAN = {"III": 3, "VII": 7}
NOTE = "This follows the standard office filing rule (ARMA International Simplified Filing Standard Rules, Rule {n}), not a rule published by the CSC. Source standard: ANSI/ARMA 12-2005."


def ukey(u):
    if re.fullmatch(r"\d+", u):
        return (0, int(u), "")
    if u in ROMAN:
        return (1, ROMAN[u], "")
    return (2, 0, u.lower())


def order(units):
    return sorted(units, key=lambda kv: [ukey(u) for u in kv[1]])

# (rule, ask, [(name, units)], key name, {wrong name: (subreason, why)}, terms, shortcut, why_correct)
ITEMS = [
 (2, "FIRST", [("R & S Hardware", ["R", "and", "S", "Hardware"]), ("R Best Laundry", ["R", "Best", "Laundry"]),
   ("R Cruz Pharmacy", ["R", "Cruz", "Pharmacy"]), ("Rabago Store", ["Rabago", "Store"])],
  {"R Best Laundry": ("CLR-LETTER-ORDER: skips the symbol, breaks ARMA Rule 2", "Files first only if \"&\" is skipped. Spelled out as \"and\", R & S comes before R Best."),
   "R Cruz Pharmacy": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "Second unit \"Cruz\" comes after \"and\" and \"Best\"."),
   "Rabago Store": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"R\" alone comes before \"Rabago\": nothing comes before something.")},
  "A symbol such as & is indexed as if spelled out (\"and\") and is its own unit.",
  "Read \"&\" aloud as \"and\", then compare.",
  "Units: R / and / S / Hardware. The second units are and, Best, Cruz; \"and\" is first."),
 (2, "LAST", [("Lucky Star Bakery", ["Lucky", "Star", "Bakery"]), ("Luz Bakeshop", ["Luz", "Bakeshop"]),
   ("The Luz Garden", ["Luz", "Garden", "The"]), ("Luz of the Valley Resort", ["Luz", "of", "the", "Valley", "Resort"])],
  {"The Luz Garden": ("CLR-ARTICLE-COUNTED: breaks ARMA Rule 2", "Files last only if the leading \"The\" is counted first (T). It moves to the end: Luz Garden The."),
   "Luz Bakeshop": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Bakeshop\" is the earliest second unit among the Luz names."),
   "Lucky Star Bakery": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Lucky\" comes before \"Luz\", so it files first, not last.")},
  "A leading \"The\" becomes the last unit. Other minor words (of, the, and) inside the name stay where they are, as units.",
  "Move a leading \"The\" to the end first; leave inner minor words alone.",
  "Second units among the Luz names: Bakeshop, Garden, of. \"of\" is last, so Luz of the Valley Resort is last."),
 (3, "FIRST", [("Ana's Bakery", ["Anas", "Bakery"]), ("Ana Carinderia", ["Ana", "Carinderia"]),
   ("Anas Printing", ["Anas", "Printing"]), ("Anastacia Salon", ["Anastacia", "Salon"])],
  {"Ana's Bakery": ("CLR-LETTER-ORDER: drops the possessive s, breaks ARMA Rule 3", "Files first only if \"'s\" is dropped (Ana Bakery). The apostrophe is ignored but the s stays: Anas."),
   "Anas Printing": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Anas\" comes after \"Ana\": nothing comes before something."),
   "Anastacia Salon": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Anastacia\" is longer than \"Ana\" and \"Anas\", so it comes after them.")},
  "Punctuation is ignored. A possessive keeps its s: Ana's = Anas.",
  "Delete the apostrophe, keep every letter.",
  "Units: Ana / Carinderia; Anas / Bakery; Anas / Printing; Anastacia / Salon. \"Ana\" alone files first."),
 (3, "LAST", [("Cruz-Lim Trading", ["CruzLim", "Trading"]), ("Cruz Lumber", ["Cruz", "Lumber"]),
   ("Cruzada Store", ["Cruzada", "Store"]), ("Cruzlan Rice Mill", ["Cruzlan", "Rice", "Mill"])],
  {"Cruzlan Rice Mill": ("CLR-LETTER-ORDER: splits the hyphenated name, breaks ARMA Rule 3", "Files last only if Cruz-Lim is split into Cruz / Lim. As one unit, CruzLim comes after Cruzlan (cruzla comes before cruzli)."),
   "Cruzada Store": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Cruzada\" comes before \"Cruzlan\" and \"CruzLim\" (a before l)."),
   "Cruz Lumber": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Cruz\" alone files first: nothing comes before something.")},
  "Punctuation is ignored, and a hyphenated name is one unit: Cruz-Lim = CruzLim.",
  "Close up the hyphen, then compare letter by letter.",
  "Units in order: Cruz, Cruzada, Cruzlan, CruzLim. CruzLim is last (cruzli comes after cruzla)."),
 (4, "FIRST", [("J. Ramos", ["Ramos", "J"]), ("Jose Ramos", ["Ramos", "Jose"]), ("Juan B. Ramos", ["Ramos", "Juan", "B"]), ("Jo Anne Ramos", ["Ramos", "Jo", "Anne"])],
  {"Jo Anne Ramos": ("CLR-LETTER-ORDER: breaks ARMA Rule 4", "\"Jo\" comes after the initial \"J\": a single letter files before any name that starts with it."),
   "Jose Ramos": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Jose\" comes after \"J\" and \"Jo\"."),
   "Juan B. Ramos": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Juan\" comes after \"J\", \"Jo\" and \"Jose\".")},
  "An initial in a personal name is its own unit. Surname first, then given name or initial.",
  "A lone initial comes before every name that starts with that letter (nothing before something).",
  "All file under Ramos. Second units: J, Jo, Jose, Juan. The initial J is first."),
 (4, "FIRST", [("ABC Glass", ["ABC", "Glass"]), ("A B Cruz Store", ["A", "B", "Cruz", "Store"]), ("Abaca Crafts", ["Abaca", "Crafts"]), ("ABS Motors", ["ABS", "Motors"])],
  {"ABC Glass": ("CLR-LETTER-ORDER: splits the acronym, breaks ARMA Rule 4", "Files first only if ABC is split into A / B / C. A business acronym is one unit, written as it is: ABC."),
   "Abaca Crafts": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Abaca\" comes after the single letter \"A\"."),
   "ABS Motors": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"ABS\" comes after \"A\", \"Abaca\" and \"ABC\".")},
  "Single letters separated by spaces are separate units. An acronym written without spaces (ABC) is one unit.",
  "Spaces decide: \"A B\" is two units, \"ABC\" is one.",
  "First units: A, Abaca, ABC, ABS. The single letter A is first."),
 (7, "FIRST", [("100 Islands Tours", ["100", "Islands", "Tours"]), ("7 Seas Shipping", ["7", "Seas", "Shipping"]),
   ("VII Arts Studio", ["VII", "Arts", "Studio"]), ("Seven Hills Inn", ["Seven", "Hills", "Inn"])],
  {"100 Islands Tours": ("CLR-LETTER-ORDER: compares digits one by one, breaks ARMA Rule 7", "Files first only if 100 is read digit by digit (1 before 7). Numbers file in ascending order: 7 before 100."),
   "VII Arts Studio": ("CLR-LETTER-ORDER: breaks ARMA Rule 7", "Roman numerals file after Arabic numerals."),
   "Seven Hills Inn": ("CLR-LETTER-ORDER: breaks ARMA Rule 7", "A spelled-out number files with the letters, after all numerals.")},
  "Arabic numerals first, in ascending order, then Roman numerals, then names that start with letters.",
  "Compare numbers by value, not by first digit.",
  "Order: 7, 100, VII, Seven. 7 Seas Shipping is first."),
 (7, "LAST", [("3rd Avenue Cafe", ["3", "Avenue", "Cafe"]), ("III Kings Bakery", ["III", "Kings", "Bakery"]),
   ("Three Sisters Bakery", ["Three", "Sisters", "Bakery"]), ("Thomas Bakery", ["Thomas", "Bakery"])],
  {"Thomas Bakery": ("CLR-LETTER-ORDER: files a spelled-out number with the numerals, breaks ARMA Rule 7", "Files last only if \"Three\" is filed as the number 3. A spelled-out number files alphabetically: Thomas before Three."),
   "III Kings Bakery": ("CLR-LETTER-ORDER: breaks ARMA Rule 7", "Roman numerals file before any name that starts with a letter."),
   "3rd Avenue Cafe": ("CLR-LETTER-ORDER: breaks ARMA Rule 7", "Arabic numerals file first; the ordinal ending \"rd\" is ignored.")},
  "Spelled-out numbers are filed as words. Ordinal endings (st, nd, rd, th) are ignored.",
  "Only digits and Roman numerals go in the number group; words go with the letters.",
  "Order: 3rd Avenue, III Kings, Thomas, Three. \"Thr\" comes after \"Tho\", so Three Sisters Bakery is last."),
 (8, "LAST", [("University of the East", ["University", "of", "the", "East"]), ("University of Santo Tomas", ["University", "of", "Santo", "Tomas"]),
   ("University of San Carlos", ["University", "of", "San", "Carlos"]), ("Union Bank", ["Union", "Bank"])],
  {"University of Santo Tomas": ("CLR-LETTER-ORDER: drops a minor word, breaks ARMA Rule 8", "Files last only if \"the\" is dropped (University of East). The name is indexed as written, so \"the\" is the third unit."),
   "University of San Carlos": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"San\" comes before \"Santo\" and \"the\": nothing comes before something."),
   "Union Bank": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Union\" comes before \"University\".")},
  "An organization is indexed as written on its letterhead, minor words included; only a leading \"The\" moves to the end.",
  "Do not rearrange a school's name to its key word; read it as written.",
  "Third units among the University names: San, Santo, the. \"the\" is last, so University of the East is last."),
 (8, "LAST", [("Ateneo de Davao University", ["Ateneo", "de", "Davao", "University"]), ("Ateneo de Manila University", ["Ateneo", "de", "Manila", "University"]),
   ("Ateneo Graduate School", ["Ateneo", "Graduate", "School"]), ("Ateneo Law School", ["Ateneo", "Law", "School"])],
  {"Ateneo de Manila University": ("CLR-LETTER-ORDER: drops a minor word, breaks ARMA Rule 8", "Files last only if \"de\" is dropped (Ateneo Manila). As written, \"de\" is the second unit and comes before Graduate and Law."),
   "Ateneo Graduate School": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"Graduate\" comes before \"Law\"."),
   "Ateneo de Davao University": ("CLR-LETTER-ORDER: breaks ARMA Rule 1", "\"de Davao\" files first: de, then Davao before Manila.")},
  "An organization is indexed as written on its letterhead; small words such as \"de\" are units in their place.",
  "Keep every word of the official name, in order.",
  "Second units: de, de, Graduate, Law. \"Law\" is last, so Ateneo Law School is last."),
]

POS = [2, 0, 3, 1, 1, 2, 0, 3, 3, 0]


def build():
    out = []
    for n, (rule, ask, names, wrong, terms, short, wc) in enumerate(ITEMS):
        srt = [nm for nm, _ in order(names)]
        key = srt[0] if ask == "FIRST" else srt[-1]
        assert key not in wrong and len(wrong) == 3, key
        others = [nm for nm, _ in names if nm != key]
        opts = others[:]
        opts.insert(POS[n], key)
        ids = [f"o{i+1}" for i in range(4)]
        oid = dict(zip(opts, ids))
        num = 15 + n
        out.append({
            "id": f"CIVIO-GAP3-CLR-FILE-ORDER-{num:04d}", "track": "subprofessional", "domain": "clerical", "competency": "Clerical Ability",
            "concept": "business and organization filing (ARMA rules)" if rule != 4 else "personal and business name filing (ARMA rules)",
            "micro_skill": f"apply ARMA Rule {rule}", "archetype": "CLR-FILE-ORDER", "difficulty": "medium", "est_seconds": 45, "language": "en",
            "stem": f"Using standard alphabetic filing, which name is filed {ask}?\n" + " | ".join(nm for nm, _ in names),
            "options": [{"option_id": oid[o], "text": o} for o in opts], "answer_option_id": oid[key],
            "reveal": {"terms": terms, "shortcut": short, "why_correct": wc + " " + NOTE.format(n=rule),
                       "why_wrong": {oid[w]: wrong[w][1] for w in others}},
            "distractor_reasoning": {oid[w]: "CLR-FILE-ORDER" for w in others},
            "distractor_subreason": {oid[w]: wrong[w][0] for w in others},
            "computed_order": srt,
            "source": f"Civio Filing Rules v2 / ARMA Rule {rule}", "source_url": None, "source_group": "civio",
            "status": "draft", "review_status": "unreviewed", "reviewer": None, "reviewed_at": None,
            "provenance": {"author": "CSE (Grok Bot)", "method": "ai_assisted", "created_at": "2026-10-13", "spec_version": "0.1.6"},
            "notes": "Gap fill round 03 (CoS round 02 ruling: filing coverage for ARMA Rules 2, 3, 4, 7, 8); needs independent review."})
    return {"batch": "gap-fill-003", "spec_version": "0.1.6", "status": "draft (gap fill; for independent review)", "items": out}


if __name__ == "__main__":
    d = build()
    open(os.path.join(ROOT, "docs/research/gap-fill-003.json"), "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    for i in d["items"]:
        print(i["id"], i["computed_order"], "->", next(o["text"] for o in i["options"] if o["option_id"] == i["answer_option_id"]))
