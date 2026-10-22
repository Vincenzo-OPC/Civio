"""Clerical set 2 (22 Oct 2026, afternoon), Subprofessional only: 12 spelling (new bank-wide targets), 12 ARMA filing,
6 chronological, 4 numeric and 6 copy-checking (error recognition) items. Keys are computed here; qa.py rechecks spelling
against its word list, filing with arma_solver, and the date/number/copy items through recipe ops in solver_2026_10_22."""
import re
from datetime import datetime
from d22_common import mk
import d22_cler as C

T, D = "subprofessional", "clerical"
D_, I_, X_, S_, Q_ = "SPL-DOUBLE", "SPL-IE-EI", "SPL-DROP", "SPL-SILENT", "SPL-SOUND"
EXPL = C.EXPL
from spell_2026_10_22 import SPELL2  # noqa: E402
FOILS = ["memorandum", "voucher", "treasurer", "receptionist", "affidavit", "procurement", "receipt", "schedule"]
ITEMS = []
n = 0


def nid():
    global n
    n += 1
    return f"CIVIO-D1022-SPCLR2-{n:04d}"


for k, (w, ms, meaning, sent) in enumerate(SPELL2):
    tip = "Say the word slowly by syllable and picture each part: " + "-".join(re.findall(r"[^aeiou]*[aeiou]+(?:[^aeiou](?![aeiou]))?", w)) + "."
    if k < 8:
        opts_ = [w] + [m for m, _ in ms]
        stem = f"Fill in the blank with the standard spelling. \"{sent}\"  " + " | ".join(sorted(opts_, key=lambda t: (len(t), t)))
        ITEMS.append(mk(id=nid(), track=T, domain=D, competency="Spelling", concept="spelling", micro_skill="recognize the standard spelling of a commonly misspelled word",
                        archetype="CLR-SPELL-RIGHT", difficulty="easy", est=20, stem=stem, correct=w,
                        wrong=[(m, c, f"\"{m}\" {EXPL[c]}; the standard spelling is \"{w}\".") for m, c in ms],
                        terms=f"\"{w}\" means {meaning}.", shortcut=tip,
                        why_correct=f"\"{w}\" is the standard spelling (Merriam-Webster). Each other choice changes one letter pattern: a doubled or single letter, a dropped letter, or a spelling by sound."))
    else:
        m, c = ms[0]
        foils = FOILS[(k - 8) * 2:(k - 8) * 2 + 2] + [SPELL2[k - 8][0]]
        stem = "Find the misspelled word in this list of office terms:  " + " | ".join(sorted([m] + foils, key=lambda t: (len(t), t)))
        ITEMS.append(mk(id=nid(), track=T, domain=D, competency="Spelling", concept="spelling", micro_skill="spot the misspelled word among correct ones",
                        archetype="CLR-SPELL-WRONG", difficulty="easy", est=15, stem=stem, correct=m,
                        wrong=[(f, "CLR-SPELL-CORRECT-FOIL", f"\"{f}\" is spelled correctly, so it is not the answer.") for f in foils],
                        terms=f"\"{w}\" means {meaning}. The misspelling here {EXPL[c]}.", shortcut=tip,
                        why_correct=f"\"{m}\" is misspelled: it {EXPL[c]}. The standard spelling is \"{w}\" (Merriam-Webster). The other three words are spelled correctly.",
                        error_code=c))

# ---------- Filing: clean Rule 1, 2, 5 and 8 cases only (no punctuation, number or prefix variants) ----------
FIL2 = [
 ("personal", ["Jose Manalo", "Josefina Manalo", "Joel Manalo", "Jose Manalang"], "FIRST", 1, {}),
 ("personal", ["Teresita Bacani", "Teresa Bacani", "Tereso Bacani", "Teresa Bacay"], "THIRD", 1, {}),
 ("personal", ["Ramil Ocampo", "Ramon Ocampo", "Rommel Ocampo", "Ramil Ocampos"], "LAST", 1, {}),
 ("personal", ["Felipe Aquino", "Felix Aquino", "Filipe Aquino", "Felipe Aquinto"], "SECOND", 1, {}),
 ("personal", ["Nora Villanueva", "Nora Villaflor", "Norma Villanueva", "Nora Villareal"], "FIRST", 1, {}),
 ("personal", ["Cesar Pineda", "Cesario Pineda", "Cesar Pinedo", "Cecil Pineda"], "LAST", 1, {}),
 ("business", ["The Golden Harvest Store", "Golden Grains Mill", "Golden Harvest Rice Mill", "Goldenrod Printing"], "SECOND", 2, {}),
 ("business", ["Reyes & Daughters Bakery", "Reyes Car Wash", "Reyes and Co. Trading", "Reyes Dental Clinic"], "FIRST", 2, {}),
 ("business", ["The Bamboo Hut", "Bamboo Craft Center", "Bamboo Grill", "Bamboo Hut Resort"], "THIRD", 2, {}),
 ("organization", ["Social Security System", "Social Welfare Office", "Society of Engineers", "Sociedad Cooperative"], "SECOND", 8, {}),
 ("organization", ["Bureau of Fire Protection", "Bureau of Customs", "Bureau of Internal Revenue", "Bureau of Immigration"], "THIRD", 8, {}),
 ("organization", ["Philippine Coast Guard", "Philippine Statistics Authority", "Philippine Postal Corporation", "Philippine Sports Commission"], "LAST", 8, {}),
]
RANK = C.RANK
for k, (kind, names, r, rule, subs) in enumerate(FIL2):
    ix = C.ix_person if kind == "personal" else C.ix_bus
    order = sorted(names, key=ix)
    assert len({tuple(ix(x)) for x in names}) == 4
    key = order[RANK[r]]
    q = C.INTRO[k % 4].format(r=r, kind=kind)
    if kind != "personal" and not re.search(r"business|organization", q, re.I):
        q = q.replace("Which name", f"Which {kind} name")
    if kind == "personal" and "personal" not in q:
        q = q.replace("Which name", "Which personal name")
    stem = q + "\n" + " | ".join(names)
    pos = {nm: order.index(nm) + 1 for nm in names}
    wrong, sub = [], {}
    for nm in names:
        if nm == key:
            continue
        txt, rn = C.SUBR[subs.get(nm, {1: "unit", 2: "the" if nm.startswith("The ") or "&" in nm else "unit", 5: "title", 8: "org"}[rule])]
        wrong.append((nm, "CLR-FILE-ORDER", f"\"{nm}\" indexes as {C.show(ix(nm))} and files {['first', 'second', 'third', 'fourth'][pos[nm] - 1]}, so it is not {r.lower()}. Picking it ignores this: " + txt.split('(')[1].rstrip(')') + "."))
        sub[nm] = txt
    item = mk(id=nid(), track=T, domain=D, competency="Filing", concept="alphabetic filing (ARMA rules)", micro_skill=f"apply ARMA Rule {rule} when indexing",
              archetype="CLR-FILE-POSITION" if kind == "personal" else "CLR-FILE-BUSINESS", difficulty="medium", est=45 if kind == "personal" else 50,
              stem=stem, correct=key, wrong=wrong,
              terms="Indexing writes a name as filing units: surname, given name, middle initial for people; words as written for businesses and organizations. Compare unit by unit, letter by letter.",
              shortcut="Rewrite each name in indexed form first, then sort the rewritten forms.",
              why_correct=f"\"{key}\" is filed {r.lower()}. Indexed order: " + "; ".join(C.show(ix(x)) for x in order) + f". {C.RULE[rule]} {C.ARMA.format(rule)} Source standard: ANSI/ARMA 12-2005.",
              source="Civio Filing Rules v2 / ANSI/ARMA 12-2005", url="https://webstore.ansi.org/standards/arma/ansiarma122005")
    by_text = {o["text"]: o["option_id"] for o in item["options"]}
    item["distractor_subreason"] = {by_text[nm]: v for nm, v in sub.items()}
    ITEMS.append(item)

# ---------- Chronological filing (mixed date formats) ----------
FMTS = ["%B %d, %Y", "%d %B %Y", "%Y-%m-%d"]


def pdate(s):
    for f in FMTS:
        try:
            return datetime.strptime(s.strip(), f)
        except ValueError:
            pass
    raise ValueError(s)


CHR = [  # dates, want, trap explanation per wrong date
 (["March 4, 2026", "4 February 2026", "2026-03-01", "February 28, 2026"], "first"),
 (["2025-12-30", "January 2, 2026", "31 December 2025", "December 29, 2025"], "last"),
 (["10 October 2026", "October 1, 2026", "2026-09-30", "September 3, 2026"], "first"),
 (["July 15, 2026", "2026-07-05", "15 June 2026", "June 30, 2026"], "last"),
 (["2026-01-11", "11 November 2025", "January 1, 2026", "November 21, 2025"], "first"),
 (["April 9, 2026", "2026-04-19", "9 May 2026", "May 1, 2026"], "last"),
]
for dates, want in CHR:
    srt = sorted(dates, key=pdate)
    key = srt[0] if want == "first" else srt[-1]
    stem = (f"Letters are filed in chronological order, earliest date first. The dates are written in different formats. Which date is filed {want.upper()}?\n"
            + " | ".join(dates))
    rank = {d: srt.index(d) + 1 for d in dates}
    wrong = []
    for d_ in dates:
        if d_ == key:
            continue
        p = pdate(d_)
        wrong.append((d_, "CLR-FILE-ORDER", f"\"{d_}\" is {p.strftime('%d %B %Y').lstrip('0')}, which is number {rank[d_]} of 4 in time order, so it is not {want}."
                      + (" Reading the day number first (or the month name alone) causes this mistake." if rank[d_] in (1, 4) else "")))
    ITEMS.append(mk(id=nid(), track=T, domain=D, competency="Filing", concept="chronological filing", micro_skill="put dates written in different formats into time order",
                    archetype="CLR-CHRONOLOGICAL", difficulty="medium", est=40, stem=stem, correct=key, wrong=wrong,
                    terms="Chronological filing orders records by date: compare the year first, then the month, then the day.",
                    shortcut="Rewrite every date as YYYY-MM-DD, then compare left to right.",
                    why_correct=f"Rewritten as YYYY-MM-DD: " + "; ".join(pdate(x).strftime("%Y-%m-%d") for x in srt) + f". So \"{key}\" is {want}.",
                    recipe={"op": "clr_date", "args": {"want": want}, "fmt": "str"}))

# ---------- Numeric filing ----------
NUMF = [
 (["RF-1088", "RF-998", "RF-1080", "RF-10080"], "first"),
 (["PR-2041", "PR-241", "PR-2014", "PR-20140"], "last"),
 (["Case 5012", "Case 512", "Case 5102", "Case 521"], "second"),
 (["Lot 77", "Lot 707", "Lot 770", "Lot 7007"], "third"),
]
POS = {"first": 0, "second": 1, "third": 2, "last": -1}
for codes, want in NUMF:
    v = lambda s: int(re.sub(r"\D", "", s))
    srt = sorted(codes, key=v)
    key = srt[POS[want]]
    stem = (f"Folders are filed in ascending order of their number, read as a whole number (not digit by digit). Which folder is filed {want.upper()}?\n"
            + " | ".join(codes))
    wrong = [(c, "CLR-FILE-ORDER", f"\"{c}\" has the value {v(c):,} and is number {srt.index(c) + 1} of 4 in ascending order."
              + (" Comparing digit by digit from the left puts it in the wrong place." if len(str(v(c))) != len(str(v(key))) else ""))
             for c in codes if c != key]
    ITEMS.append(mk(id=nid(), track=T, domain=D, competency="Filing", concept="numeric filing", micro_skill="order numbers by value, not by their first digit",
                    archetype="CLR-FILE-NUMERIC", difficulty="medium", est=35, stem=stem, correct=key, wrong=wrong,
                    terms="Numeric filing orders records by the value of the number. A number with fewer digits is smaller, whatever its first digit.",
                    shortcut="Count the digits first: fewer digits file earlier. Compare digit by digit only when the counts are equal.",
                    why_correct="Ascending values: " + "; ".join(f"{c} ({v(c):,})" for c in srt) + f". So \"{key}\" is {want}. " + C.RULE[7] + " " + C.ARMA.format(7),
                    recipe={"op": "clr_num", "args": {"want": want}, "fmt": "str"}))
    _it = ITEMS[-1]
    _it["distractor_subreason"] = {oid: C.SUBR["numval"][0] for oid in _it["distractor_reasoning"]}

# ---------- Copy checking (error recognition) ----------
CMP = [  # original, copies A-D, mode, errors {letter: description}
 ("Ma. Teresa B. Villanueva, 1452 Rizal Ave., Brgy. San Isidro, Tarlac City 2300",
  ["Ma. Teresa B. Villanueva, 1452 Rizal Ave., Brgy. San Isidro, Tarlac City 2300", "Ma. Teresa B. Villaneuva, 1452 Rizal Ave., Brgy. San Isidro, Tarlac City 2300",
   "Ma. Teresa B. Villanueva, 1425 Rizal Ave., Brgy. San Isidro, Tarlac City 2300", "Ma. Teresa D. Villanueva, 1452 Rizal Ave., Brgy. San Isidro, Tarlac City 2300"], "same"),
 ("TIN 412-087-356-000, Official Receipt No. 0047813, dated 14 August 2026",
  ["TIN 412-087-356-000, Official Receipt No. 0047183, dated 14 August 2026", "TIN 412-087-365-000, Official Receipt No. 0047813, dated 14 August 2026",
   "TIN 412-087-356-000, Official Receipt No. 0047813, dated 14 August 2026", "TIN 412-087-356-000, Official Receipt No. 0047813, dated 14 August 2025"], "same"),
 ("Engr. Rodolfo C. Macaraeg, Plantilla Item OSEC-ENGR3-1270-2019",
  ["Engr. Rodolfo C. Macaraeg, Plantilla Item OSEC-ENGR3-1270-2019", "Engr. Rodolfo C. Macaraeg, Plantilla Item OSEC-ENGR3-1270-2019",
   "Engr. Rodolfo C. Macaraeg, Plantilla Item OSEC-ENGR3-1207-2019", "Engr. Rodolfo C. Macaraeg, Plantilla Item OSEC-ENGR3-1270-2019"], "diff"),
 ("Purok 6, Brgy. Bagong Pag-asa, Mun. of Sta. Cruz, Laguna, Tel. (049) 501-2286",
  ["Purok 6, Brgy. Bagong Pag-asa, Mun. of Sta. Cruz, Laguna, Tel. (049) 501-2286", "Purok 6, Brgy. Bagong Pag-asa, Mun. of Sta. Cruz, Laguna, Tel. (049) 501-2286",
   "Purok 6, Brgy. Bagong Pag-asa, Mun. of Sta. Cruz, Laguna, Tel. (049) 501-2286", "Purok 6, Brgy. Bagong Pagasa, Mun. of Sta. Cruz, Laguna, Tel. (049) 501-2286"], "diff"),
 ("PhilHealth No. 19-025544871-3, Josephine A. Dumalagan, born 07/23/1988",
  ["PhilHealth No. 19-025544871-3, Josephine A. Dumalagan, born 07/23/1988", "PhilHealth No. 19-025548471-3, Josephine A. Dumalagan, born 07/23/1988",
   "PhilHealth No. 19-025544871-3, Josefine A. Dumalagan, born 07/23/1988", "PhilHealth No. 19-025544871-3, Josephine A. Dumalagan, born 07/23/1998"], "same"),
 ("Voucher 2026-08-0631 for P48,750.00 payable to Tri-Star Office Supply",
  ["Voucher 2026-08-0631 for P48,750.00 payable to Tri-Star Office Supply", "Voucher 2026-08-0631 for P48,570.00 payable to Tri-Star Office Supply",
   "Voucher 2026-08-0631 for P48,750.00 payable to Tri-Star Office Supply", "Voucher 2026-08-0631 for P48,750.00 payable to Tri-Star Office Supply"], "diff"),
]


def diff_desc(a, b):
    """Name the first stretch where copy b differs from original a, by word."""
    wa, wb = a.split(), b.split()
    for x, y in zip(wa, wb):
        if x != y:
            return f"it has \"{y}\" where the original has \"{x}\""
    return "it differs in length from the original"


for orig, copies, mode in CMP:
    L = "ABCD"
    same = [L[i] for i, c in enumerate(copies) if c == orig]
    bad = [L[i] for i, c in enumerate(copies) if c != orig]
    assert (len(same) == 1) if mode == "same" else (len(bad) == 1)
    key = f"Copy {(same if mode == 'same' else bad)[0]}"
    ask = "Which copy matches the original exactly?" if mode == "same" else "Three copies match the original exactly. Which copy contains an error?"
    stem = f"Compare each copy with the original record. {ask}\nOriginal: {orig}\n" + "\n".join(f"Copy {L[i]}: {c}" for i, c in enumerate(copies))
    wrong = []
    for i, c in enumerate(copies):
        t = f"Copy {L[i]}"
        if t == key:
            continue
        wrong.append((t, "CLR-COPY-MISMATCH", (f"Copy {L[i]} is not exact: {diff_desc(orig, c)}." if mode == "same" else f"Copy {L[i]} matches the original character for character.")))
    kc = copies[L.index(key[-1])]
    ITEMS.append(mk(id=nid(), track=T, domain=D, competency="Checking", concept="comparing records for errors", micro_skill="compare names, numbers and addresses character by character",
                    archetype="CLR-COPY-CHECK", difficulty="easy" if mode == "diff" else "medium", est=35 if mode == "diff" else 45, stem=stem, correct=key, wrong=wrong,
                    terms="Copy checking: compare the copy with the original one part at a time (name, number, date, address), character by character.",
                    shortcut="Check numbers digit by digit first; swapped digits (1270 vs 1207) are the most common copying error. Then check spelling of names.",
                    why_correct=(f"{key} is identical to the original." if mode == "same" else f"{key} is the only copy with an error: {diff_desc(orig, kc)}."),
                    recipe={"op": "clr_copy", "args": {"mode": mode}, "fmt": "str"}))
