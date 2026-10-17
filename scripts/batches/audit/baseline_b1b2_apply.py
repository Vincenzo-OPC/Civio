"""Round 03 CoS verdicts (2026-10-17) on baseline B1 Clerical and B2 GI: builds the change list and the SQL for the MSI local DB.
Writes docs/research/audit/fixes/round-03-baseline-b1b2-cos.json and /workspace/tmp/b1b2.sql.
Every UPDATE is guarded by id, source_group='baseline' and the exported stem, so a row that changed since the export is skipped."""
import json, re, runpy, io, contextlib
SRC = "docs/research/audit/data/baseline-550-2026-10-17.json"
B = {x["id"]: x for x in json.load(open(SRC))}
with contextlib.redirect_stdout(io.StringIO()):
    b1 = runpy.run_path("scripts/batches/audit/baseline_b1_clerical.py")["F_"]
    b2 = runpy.run_path("scripts/batches/audit/baseline_b2_gi.py")["F_"]
def BP(e):
    e = re.sub(r'([^.!?\u201d"])\s+Therefore, the correct option is', r'\1. Therefore, the correct option is', e)
    e = e.replace('.."', '."').replace("The other choices fail because the other choices", "The other choices fail because they")
    return e
RETIRE = {i for i, v in b1.items() if v[0] == "DUPLICATE"} | {292} | {308, 311}  # 308/311: "pick a different target, or retire": retired; new targets go to the pending swap file
RETIRE |= {i for i, v in b2.items() if v[0] == "DUPLICATE"} | {77, 79, 226, 227, 400, 403, 404, 415, 549}  # rewrite-or-retire items: retired; 77/226/227 topics are covered by gap-fill-004
HOLD = {}  # 304 was held (CoS foil 'Indispensible' was already a choice); CoS ruled 'Indispencible' at 3:11 PM, applied below
U = {}  # id -> dict of new fields
def opt(i, idx, text):
    U.setdefault(i, {}).setdefault("options", list(B[i]["options"]))[idx] = text
def set_(i, **kw):
    U.setdefault(i, {}).update(kw)
# --- B1 key corrections
opt(277, 1, "Dela Cruz; Del Mundo; Delos Santos; Del Rosario"); set_(277, correct_option=1, explanation="Treat each prefix as part of the surname and compare letter by letter (ARMA Rule 6): DELACRUZ, DELMUNDO, DELOSSANTOS, DELROSARIO. After D-E-L the next letters are a, m, o and r, so the order is Dela Cruz, Del Mundo, Delos Santos, Del Rosario.")
set_(287, correct_option=0, explanation="Compare letter by letter. Bayani is shorter than Bayanihan and nothing comes before something, so Bayani Foundation is first and Bayanihan Center second. Bayview comes next (v after a in the fourth letter), and Bazaars is last (z after y in the third letter).")
opt(282, 0, "Under L, after \u201cLeave Application\u201d"); set_(282, explanation="Subject filing uses the main subject, so the memo goes under L. Among the Leave entries, compare the second word: Application (A) comes before Credits (C), so \u201cLeave Credits\u201d is filed after \u201cLeave Application\u201d.")
# --- B1 fixes
set_(51, explanation="Compare the first letter of each surname: G (Garcia) comes before R (Reyes), S (Santos) and T (Torres), so Garcia, Ana is filed first.")
set_(52, explanation="All five names start with L, so compare the second letter. The i in Lim comes before the o in Lopez, while Luna and Luz (u) and Lyons (y) come after it. Only Lim is filed before Lopez.")
set_(212, options=["Topic or subject matter", "Date the record was received", "Name of the correspondent", "Assigned file number"], explanation="Subject filing groups records by topic. Filing by date received is chronological, by correspondent name is alphabetic, and by file number is numeric.")
set_(213, options=["Reminder or follow-up by date", "Moving inactive records to storage", "Listing where every record is kept", "Keeping permanent records only"], explanation="A tickler file is arranged by future date so the clerk is reminded to act on time. Moving inactive records is a transfer file, listing locations is an index, and keeping permanent records is an archive; none of them prompts follow-up.")
set_(216, options=["Name of addressee or subject per office rules", "Date sent only, with no name or subject", "Name of the sending office", "File number only, with no index"], explanation="Outgoing letters are filed under the addressee or the subject so they sit with the matching incoming letters. Date alone or number alone cannot be searched without an index, and the sending office's own name would put every letter in one folder.")
set_(217, options=["Date order", "Alphabetic order of the author", "Subject or topic", "Numeric file code"], explanation="Chronological filing arranges records by date. Alphabetic, subject and numeric filing are different methods.")
set_(275, stem="Which surname is filed first?", explanation="All four start with A. In the second letter, b (Abad, Abalos) comes before q (Aquino) and r (Arce). Abad and Abalos share A-B-A; in the fourth letter, d comes before l, so Abad is filed first.")
set_(290, options=["A retrieval description or subject", "The number of pages in the record", "The name of the clerk who encoded it", "The paper size of the record"], explanation="An index is used to find a record, so beside the identifier it needs a description or subject that a searcher can look up. Page count, the encoder's name and paper size do not help anyone locate the record.")
opt(304, 3, "Indispencible"); set_(304, explanation="Indispensable is in-dis-pens-able: the middle is -pens- (with s, not c), and the ending is -able, not -ible.")
opt(299, 3, "Milenium")
set_(301, explanation="Conscientious is built on science: con-sci-en-tious. Keep the sc and the t before -ious.")
opt(305, 3, "Miscellanious")
opt(309, 3, "Reconsiliation")
opt(313, 3, "Pronounciasion")
set_(548, stem="Which spelling is correct for the word meaning to get or accept something given?", explanation="Receive follows the rule \u201ci before e, except after c\u201d: after the c, write ei, as in rec-ei-ve.")
# --- B2 fixes (texts checked against LawPhil: cons1987, ra_6770_1989)
set_(1, explanation="The Constitution is the fundamental and supreme law; the Civil Code, the Penal Code and the Local Government Code are statutes that must conform to it. The 1987 Constitution took effect on its ratification in a plebiscite (Art. XVIII, Sec. 27).")
set_(5, stem="The Bill of Rights is found in:", explanation="Article III of the 1987 Constitution is the Bill of Rights. Article II is the Declaration of Principles and State Policies, Article VI the Legislative Department, and Article VII the Executive Department.")
set_(10, explanation="Art. XIII, Sec. 17(1) creates \u201can independent office called the Commission on Human Rights.\u201d It is not a Cabinet department, a private NGO or a local government unit.")
set_(354, options=["Public accountability", "Separation of powers", "Local autonomy", "Civilian supremacy"], explanation="Art. XI, Sec. 1: public office is a public trust, and public officers and employees must at all times be accountable to the people. Separation of powers divides authority among the branches, local autonomy gives powers to local governments, and civilian supremacy places civilian authority over the military; none of them is the duty to answer to the people.")
opt(355, 3, "The constitutional commissions"); set_(355, explanation="Art. VI, Sec. 1 vests legislative power in the Congress. The executive branch carries out laws, the judicial branch interprets them, and the constitutional commissions are independent bodies that do not pass statutes.")
opt(357, 1, "The Philippine National Police"); opt(357, 2, "The Cabinet"); set_(357, explanation="Art. VII, Sec. 18: the President is the Commander-in-Chief of all armed forces of the Philippines. The police force is civilian in character (Art. XVI, Sec. 6), the Cabinet heads departments under the President's control, and the constitutional commissions are independent; none of them is a military command.")
set_(358, options=["Freedom of the press", "Right to information on matters of public concern", "Freedom of assembly", "Privacy of communication"], explanation="Art. III, Sec. 4 bars any law abridging the freedom of speech, of expression, or of the press. Stopping a newspaper from printing criticism restrains the press. The right to information (Sec. 7) concerns access to official records, peaceable assembly concerns gatherings, and privacy of communication (Sec. 3) protects private messages.")
set_(363, options=["Arbitrary government action", "Unequal treatment of people in the same class", "Taking private property without payment", "Punishment under a law passed after the act"], explanation="Art. III, Sec. 1: no person shall be deprived of life, liberty, or property without due process of law, which guards against arbitrary government action. Unequal treatment is the concern of equal protection, taking property without payment is barred by the just-compensation rule (Sec. 9), and punishing past acts is an ex post facto law (Sec. 22).")
set_(367, stem="A valid classification for equal-protection purposes should be related to the purpose of the law and apply to:", explanation=BP(B[367]["explanation"]))
set_(373, stem="Which constitutional office investigates illegal acts of public officials and, as provided by law, prosecutes them?", options=["The Office of the Ombudsman", "The Commission on Audit", "The Civil Service Commission", "The Commission on Human Rights"], explanation="Art. XI, Sec. 13(1) empowers the Ombudsman to investigate any act or omission of a public official that appears illegal, unjust, improper or inefficient, and R.A. 6770, Sec. 15(1), as provided by law, gives the Office the power to investigate and prosecute. COA audits government accounts, the CSC is the central personnel agency, and the CHR investigates human rights violations; none of them prosecutes officials.")
opt(374, 2, "Govern as independent federal states"); opt(374, 3, "Act free from the general supervision of the President"); set_(374, explanation="Art. X, Sec. 2 guarantees local autonomy, and Sec. 4 keeps local governments under the President's general supervision. Autonomy means managing local affairs within the Constitution and national law; it does not let a local government ignore national statutes, act as a federal state, or escape presidential supervision.")
set_(521, options=["Congress", "The President", "The Department of Budget and Management", "The Commission on Audit"], explanation="Art. VI, Sec. 29(1): no money shall be paid out of the Treasury except in pursuance of an appropriation made by law, and Congress makes the laws. The President submits the budget proposal (Art. VII, Sec. 22), the DBM prepares and releases funds, and COA audits how they are spent.")
opt(522, 1, "Imposes a tax on the property"); opt(522, 3, "Regulates a business through a permit"); set_(522, explanation="Art. III, Sec. 9: private property shall not be taken for public use without just compensation. A tax and a police-power permit regulate or burden property without taking it, so no compensation is owed, and a public hearing takes nothing.")
set_(219, stem="Art. VII, Sec. 19 names which case as the one where the President may not grant reprieves, commutations and pardons?", options=["Violations of election law without COMELEC recommendation", "Impeachment", "Traffic violations only", "Tax evasion exclusively"], explanation="Art. VII, Sec. 19 opens: \u201cExcept in cases of impeachment, or as otherwise provided in this Constitution.\u201d Impeachment is the case it names. The election-law limit is a different rule in Art. IX-C, Sec. 5, and it is conditional: the President may pardon such violations with COMELEC's favorable recommendation. Traffic violations and tax evasion are not exceptions.")
# --- generic: explanation punctuation on every retained row in B1/B2
keep = (set(b1) | set(b2)) - RETIRE - set(HOLD)
for i in keep:
    e = U.get(i, {}).get("explanation", B[i]["explanation"])
    if BP(e) != e:
        set_(i, explanation=BP(e))
for i, u in U.items():
    assert i in keep, i
    o = u.get("options", B[i]["options"]); assert len(o) == 4 and len({x.strip().lower() for x in o}) == 4, i
def q(s): return "'" + s.replace("'", "''") + "'"
sql = ["SET client_encoding TO 'UTF8';", "BEGIN;"]
sql.append(f"UPDATE questions SET status='draft', updated_at=NOW() WHERE source_group='baseline' AND status='active' AND id IN ({','.join(map(str, sorted(RETIRE)))});")
for i in sorted(U):
    sets = [f"{k}={q(v) if isinstance(v, str) else (q(json.dumps(v, ensure_ascii=False)) + '::jsonb' if isinstance(v, list) else v)}" for k, v in U[i].items()]
    sql.append(f"UPDATE questions SET {', '.join(sets)}, updated_at=NOW() WHERE id={i} AND source_group='baseline' AND stem={q(B[i]['stem'])};")
sql.append("COMMIT;")
open("/workspace/tmp/b1b2.sql", "w").write("\n".join(sql) + "\n")
out = {"round": "03", "date": "2026-10-17", "verdict": "Chief of Staff (final approval, delegated by GT)", "retire": sorted(RETIRE), "hold": HOLD,
       "updates": [{"id": i, "old": {k: B[i][k] for k in U[i]}, "new": U[i]} for i in sorted(U)]}
json.dump(out, open("docs/research/audit/fixes/round-03-baseline-b1b2-cos.json", "w"), ensure_ascii=False, indent=1)
print(len(RETIRE), "retire;", len(U), "updates;", len(HOLD), "hold")
