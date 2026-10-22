"""Independent answer-key sheet for manifest items the qa.py solvers cannot parse (MASTER directive 2026-10-22).
NUM: each key recomputed here from a formula written from the stem. TEXT: keys checked by hand against the stem, with the reason.
CLR: small independent solvers for the 2026-10-13 clerical formats. GI: evidence strings checked against the cached lawphil text."""
import os, re
import unicodedata
from fractions import Fraction as F

NUM = {  # id: (expected key text, formula/working)
 "CIVIO-NUM-WP-AVERAGE-000012": ("34", (5 * 32 + 44) / 6),
 "CIVIO-NUM-WP-RATE-000011": ("2 hours", 1 / (F(1, 6) + F(1, 3))),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0006": ("1 7/12", F(3, 4) + F(5, 6)),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0007": ("0.1", F("2.5") * F("0.04")),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0008": ("90", F("7.2") / F("0.08")),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0009": ("5/8", max([F("0.6"), F(5, 8), F("0.58"), F(3, 5)])),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0010": ("175", 500 - 500 * F(2, 5) - 500 * F(1, 4)),
 "CIVIO-GAP2-NUM-OPS-FRAC-DEC-0011": ("1", F(5, 3) * F(3, 5)),
 "CIVIO-NUM-PCT-BASIC-926013": ("54 notebooks", 360 * F(15, 100)),
 "CIVIO-NUM-PCT-BASIC-926014": ("30%", F(18, 60) * 100),
 "CIVIO-NUM-PCT-BASIC-926015": ("288 files", 72 / F(25, 100)),
 "CIVIO-NUM-PCT-BASIC-926018": ("68%", (20 * F(80, 100) + 30 * F(60, 100)) / 50 * 100),
 "CIVIO-NUM-PCT-BASIC-926019": ("90%", F(72, 80) * 100),
 "CIVIO-NUM-PCT-BASIC-926022": ("20 children", 400 * F(30, 100) - 250 * F(40, 100)),
 "CIVIO-NUM-WP-ALGEBRA-926033": ("32 folders", 49 - 17),
 "CIVIO-NUM-WP-ALGEBRA-926034": ("11 beads", F(45, 3) - 4),
 "CIVIO-NUM-WP-ALGEBRA-926035": ("41 kilometers", F(68 + 14, 2)),
 "CIVIO-NUM-WP-ALGEBRA-926036": ("40", F(78, 2) + 1),
 "CIVIO-NUM-WP-ALGEBRA-926038": ("8 booklets", F(400 - 120, 35)),
 "CIVIO-NUM-WP-ALGEBRA-926039": ("30 kilograms", (12 + 3) * 2),          # S - 12 = S/2 + 3
 "CIVIO-NUM-WP-ALGEBRA-926040": ("10 beads", F(42 - 12, 3)),              # 2(x + 6) + x = 42
 "CIVIO-NUM-WP-ALGEBRA-926041": ("12 years", F(21 - 5 + 20, 3)),          # x + 16 = 4(x - 5)
 "CIVIO-NUM-WP-ALGEBRA-926042": ("17 years", F(48 - 8 - 6, 2)),           # y + (y + 6) + 8 = 48
 "CIVIO-NUM-WP-ALGEBRA-926048": ("₱240", 1200 - 18 * 45 - 6 * 25),
 "CIVIO-NUM-WP-ALGEBRA-926051": ("12 forms", F(24, 3) + 4),
 "CIVIO-NUM-WP-AVERAGE-926049": ("₱51 per kilogram", F(3 * 45 + 2 * 60, 5)),
 "CIVIO-NUM-WP-RATE-926029": ("₱650", F(390, 6) * 10),
 "CIVIO-NUM-WP-RATE-926030": ("10 hours", F(8 * 15, 12)),
 "CIVIO-NUM-WP-RATE-926031": ("30 kilometers", F(15, 2) * 4),
 "CIVIO-NUM-WP-RATE-926043": ("400 kits", F(360, 3 * 6) * 5 * 4),
 "CIVIO-NUM-WP-RATE-926044": ("4 4/5 hours", 1 / (F(1, 8) + F(1, 12))),
 "CIVIO-NUM-WP-RATE-926045": ("2 1/2 hours", 120 / (72 / F(3, 2))),
 "CIVIO-NUM-WP-RATE-926046": ("33 1/3 km/h", F(100, 1 + 2)),
 "CIVIO-NUM-WP-RATE-926047": ("₱234", 18 * (35 - 22)),
 "CIVIO-NUM-WP-RATIO-926027": ("8 cups", F(20, 5) * 2),
 "CIVIO-NUM-FRAC-DEC-926001": ("5/8 meter", F(7, 8) - F(1, 4)),
 "CIVIO-NUM-FRAC-DEC-926002": ("27 seats", 72 * F(3, 8)),
 "CIVIO-NUM-FRAC-DEC-926003": ("3/5", max([F(4, 7), F(5, 9), F(7, 12), F(3, 5)])),
 "CIVIO-NUM-FRAC-DEC-926004": ("17/7", F(2 * 7 + 3, 7)),
 "CIVIO-NUM-FRAC-DEC-926005": ("8 bags", 6 // F(3, 4)),
 "CIVIO-NUM-FRAC-DEC-926006": ("72 blankets", 45 / F(5, 8)),
 "CIVIO-NUM-FRAC-DEC-926007": ("4 servings", F(3, 2) / F(3, 8)),
 "CIVIO-NUM-FRAC-DEC-926008": ("3 5/6 kilograms", F(5, 3) + F(13, 6)),
 "CIVIO-NUM-FRAC-DEC-926009": ("1/2", 1 - F(3, 10) - F(1, 5)),
 "CIVIO-NUM-FRAC-DEC-926010": ("5/8", F("0.625")),
 "CIVIO-NUM-FRAC-DEC-926011": ("18 seedlings", 45 * F(2, 3) * F(3, 5)),
 "CIVIO-NUM-FRAC-DEC-926012": ("2 kilometers", F(8, 3) * F(3, 4)),
 "CIVIO-NUM-WP-RATIO-926025": ("35 stools", 55 * F(7, 11)),
 "CIVIO-NUM-WP-RATIO-926026": ("48 sacks", F(30, 5) * 8),
 "CIVIO-NUM-WP-RATIO-926028": ("50 kits", 100 * F(5, 10)),
 "CIVIO-NUM-WP-RATIO-926032": ("4 crates", 36 * F(5, 9) - 36 * F(4, 9)),
}

TEXT = {  # id: (expected key, reason)
 "CIVIO-ANA-ANALOGY-PART-WHOLE-000009": ("barangay : municipality", "part to whole: a page is part of a book; a barangay is part of a municipality"),
 "CIVIO-ANA-ASSUME-I-II-000016": ("Only I", "the later hours assume residents cannot come during work hours; higher total collection is not assumed"),
 "CIVIO-ANA-SYLLOGISM-000015": ("No records clerk in the provincial office is a new hire.", "All A are B; no B is C; so no A is C"),
 "CIVIO-ANA-SYMBOL-SERIES-000017": ("T", "B+3=E, +4=I, +5=N, +6=T"),
 "CIVIO-VEN-SENT-COMP-PHRASAL-000005": ("off", "\"call off\" = cancel"),
 "CIVIO-VEN-SENT-COMP-WORD-000006": ("affect", "verb meaning to influence; \"effect\" is the noun"),
 "CIVIO-VEN-WORD-MEANING-000004": ("postpone", "defer the vote until all can attend = postpone"),
 "CIVIO-VEN-ERROR-TENSE-000019": ("finishes encoding", "\"Last Friday\" and \"closed\" need the past tense \"finished\""),
 "CIVIO-GAP1-VEN-PO-0018": ("PRSQ", "First (P), then (R), Next (S), Finally (Q)"),
 "CIVIO-GAP1-VEN-PO-0019": ("QRSP", "problem Q, cause R, proposal S, result \"As a result\" P"),
 "CIVIO-GAP1-VEN-PO-0020": ("QPRS", "bins Q, \"However\" problem P, \"To fix this\" R, result S"),
 "CIVIO-GAP1-VEN-RC-0014": ("Moving the counter made in-person payment easier for senior citizens", "covers the move, the reason and the result"),
 "CIVIO-GAP1-VEN-RC-0015": ("Asked relatives to pay for them", "stated in sentence 2"),
 "CIVIO-GAP1-VEN-RC-0016": ("It depends on how long the line is in August", "\"will also add a second counter if the line stays long\""),
 "CIVIO-GAP1-VEN-RC-0017": ("Every senior citizen now pays in person", "\"every\" is not supported; the other three are stated"),
 "CIVIO-GAP2-VEN-ERROR-0001": ("The list of applicants was posted on the board yesterday.", "head noun \"list\" is singular; \"yesterday\" needs past"),
 "CIVIO-GAP2-VEN-ERROR-0002": ("The office will release its report on Monday.", "\"will\" + base verb, possessive \"its\", \"on Monday\""),
 "CIVIO-GAP2-VEN-ERROR-0003": ("Between you and me, the memo is unclear.", "object pronoun after a preposition; \"between\" for two"),
 "CIVIO-CLR-20261013-0021": ("accommodation", "double c, double m (Merriam-Webster)"),
 "CIVIO-CLR-20261013-0025": ("recommendation", "one c, double m (Merriam-Webster)"),
 "CIVIO-CLR-20261013-0030": ("occasion", "double c, single s (Merriam-Webster)"),
 "CIVIO-CLR-20261013-0036": ("immediately", "double m, keep the e before -ly (Merriam-Webster)"),
 "CIVIO-CLR-20261013-0040": ("superintendent", "ends in -ent (Merriam-Webster)"),
 "CIVIO-GAP2-VEN-ERROR-0004": ("When the auditor arrived, the clerk had already filed the vouchers.", "past perfect for the earlier past action"),
}


def _fold(t):
    """ARMA treats letters with marks as the plain letter (ñ = n)."""
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if not unicodedata.combining(c))


def _names(stem):
    return [x.strip() for x in stem.split(":")[-1].split("|")]


def clr(it):
    s, a = it["stem"], it.get("archetype", "")
    q = s.split("\n")[0]
    rank = re.search(r"\b(FIRST|LAST|SECOND|THIRD)\b", q)
    pick = (lambda L: L[{"FIRST": 0, "SECOND": 1, "THIRD": 2, "LAST": -1}[rank.group(1)]]) if rank else None
    if a == "CLR-NAMES":
        L = sorted(_names(s), key=lambda n: (_fold(n.split()[-1]), _fold(" ".join(n.split()[:-1]))))
        return pick(L)
    if a == "CLR-NUMERIC":
        return pick(sorted(_names(s), key=lambda x: int(re.sub(r"\D", "", x))))
    if a == "CLR-CHRONOLOGICAL":
        return pick(sorted(_names(s)))
    if a == "CLR-SPELLING":
        import qa
        opts = [o["text"] for o in it["options"]]
        ok = [t for t in opts if t in qa.CORRECT]
        return ok[0] if len(ok) == 1 else None
    return None


GI = {  # id: (lawphil file, evidence)
 "CIVIO-GI-SCENARIO-APPLY-000008": ("ra_6713_1989.html.txt", "They shall not indulge in extravagant or ostentatious display of wealth in any form"),
 "CIVIO-GI-WHO-HOLDS-POWER-000007": ("cons1987.html.txt", "The House of Representatives shall have the exclusive power to initiate all cases of impeachment"),
 "CIVIO-GI-DEADLINE-NUMBER-000020": ("ra_6713_1989.html.txt", "within fifteen (15) working days from receipt thereof, respond to letters"),
 "CIVIO-GAP1-GI-SCENARIO-APPLY-0004": ("cons1987.html.txt", "Exercise visitorial powers over jails, prisons, or detention facilities"),
 "CIVIO-GAP1-GI-SCENARIO-APPLY-0005": ("cons1987.html.txt", "If the person cannot afford the services of counsel, he must be provided with one"),
 "CIVIO-GAP1-GI-TERM-MATCH-0001": ("cons1987.html.txt", "renounces war as an instrument of national policy"),
 "CIVIO-GAP1-GI-TERM-MATCH-0002": ("cons1987.html.txt", "The State values the dignity of every human person and guarantees full respect for human rights"),
 "CIVIO-GAP1-GI-WHO-HOLDS-POWER-0003": ("cons1987.html.txt", "composed of a Chairman and four Members"),
 "CIVIO-GI-20261013-0001": ("ra_9003_2001.html.txt", "Ecological Solid Waste Management Act of 2000"),
 "CIVIO-GI-20261013-0006": ("ra_8749_1999.html.txt", "Philippine Clean Air Act of 1999"),
 "CIVIO-GI-20261013-0011": ("ra_9275_2004.html.txt", "Philippine Clean Water Act of 2004"),
 "CIVIO-GI-20261013-0016": ("ra_9147_2001.html.txt", "Wildlife Resources Conservation and Protection Act"),
 "CIVIO-GI-20261013-0021": ("ra_9729_2009.html.txt", "Climate Change Commission"),
 "CIVIO-GI-20261013-0025": ("ra_11313_2019.html.txt", "Safe Spaces Act"),
 "CIVIO-GI-20261013-0029": ("cons1987.html.txt", "balanced and healthful ecology"),
}
R6713 = "https://lawphil.net/statutes/repacts/ra1989/ra_6713_1989.html"


def parse_num(t):
    t = t.replace("₱", "").replace(",", "").split(" per ")[0]
    m = re.match(r"(\d+) (\d+)/(\d+)|(\d+)/(\d+)|(\d+(?:\.\d+)?)", t)
    if not m:
        return None
    if m.group(1):
        return int(m.group(1)) + F(int(m.group(2)), int(m.group(3)))
    if m.group(4):
        return F(int(m.group(4)), int(m.group(5)))
    return F(m.group(6))


def verify(it, cache=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "docs", "research", "sources", "lawphil")):
    """True/False when the sheet covers the item, None when it does not."""
    import os, qa
    k, i = qa.key_text(it), it["id"]
    if i in NUM:
        t, v = NUM[i]
        return k == t and parse_num(k) == F(v)
    if i in TEXT:
        return k == TEXT[i][0]
    if i.startswith("CIVIO-CLR-20261013"):
        return clr(it) == k if i not in TEXT else k == TEXT[i][0]
    if it.get("domain") == "general_information" and (i in GI or it.get("source_quote")):
        if i in GI:
            f, q = GI[i]
        else:
            u = it.get("source_url") or ""
            f = "ra_6713_1989.html.txt" if "RA6713" in u else u.rstrip("/").split("/")[-1] + ".txt"
            q = it["source_quote"]
        p = os.path.join(cache, f)
        if not os.path.exists(p):
            return None
        return re.sub(r"\s+", " ", q).lower() in re.sub(r"\s+", " ", open(p, encoding="utf-8", errors="ignore").read()).lower()
    return None
