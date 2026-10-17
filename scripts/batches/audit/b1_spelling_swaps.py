"""Round 03 B1: proposed target swaps for the 12 baseline spelling rows whose target repeats a bank target, plus #308 and #311 (retired, new targets pending).
Proposals only (no DB change). Writes docs/research/audit/fixes/round-03-baseline-b1-spelling-swaps.json and checks:
key is a dictionary word, every foil is not; target unused anywhere in the repo bank or the baseline 550; foils not keyboard slips."""
import json, glob, re, sys
from spellchecker import SpellChecker
S = [  # row, old target, stem, options, key index, codes for the foils, explanation
 (54, "bureaucracy", "Choose the correctly spelled word for a special right that comes with an office:", ["Perogative", "Prerogative", "Prerogitive", "Prerrogative"], 1,
  {"Perogative": "SPL-DROP", "Prerogitive": "SPL-SOUND", "Prerrogative": "SPL-DOUBLE"},
  "Prerogative starts with pre- (before), then -rog- (ask), then -ative. People often drop the first r (perogative) or hear the second vowel as i."),
 (292, "accommodate", "Which spelling correctly completes this sentence: The clerk _____ the complaint to the legal unit yesterday.", ["Refered", "Reffered", "Referred", "Refferred"], 2,
  {"Refered": "SPL-DOUBLE", "Reffered": "SPL-DOUBLE", "Refferred": "SPL-DOUBLE"},
  "Refer is stressed on the last syllable, so the final r doubles before -ed: referred. The f never doubles."),
 (293, "maintenance", "Select the correctly spelled word for money sent to pay a bill.", ["Remitance", "Remmitance", "Remittence", "Remittance"], 3,
  {"Remitance": "SPL-DOUBLE", "Remmitance": "SPL-DOUBLE", "Remittence": "SPL-SOUND"},
  "Remit is stressed on -mit, so the t doubles before -ance: remittance. The m stays single, and the ending is -ance, not -ence."),
 (294, "separate", "Which spelling is correct in the instruction \u201cAttach your travel _____ to the request\u201d?", ["Itinerary", "Itinery", "Itenerary", "Itinerery"], 0,
  {"Itinery": "SPL-DROP", "Itenerary": "SPL-SOUND", "Itinerery": "SPL-SOUND"},
  "Itinerary has five syllables, i-tin-er-ar-y. Saying each one keeps the -ar- that people drop (itinery) and the i vowels."),
 (295, "privilege", "Which word is correctly spelled in the phrase \u201ca health _____ for every household\u201d?", ["Pamflet", "Pamphlet", "Pamplet", "Pamphlit"], 1,
  {"Pamflet": "SPL-SOUND", "Pamplet": "SPL-DROP", "Pamphlit": "SPL-SOUND"},
  "Pamphlet spells the f sound with ph and ends in -let."),
 (296, "questionnaire", "An agreement reached by the whole group is a _____; choose the correct spelling.", ["Concensus", "Consencus", "Consensus", "Consensous"], 2,
  {"Concensus": "SPL-SOUND", "Consencus": "SPL-SOUND", "Consensous": "SPL-SOUND"},
  "Consensus comes from consent, so both s sounds are spelled with s: con-sen-sus. It is not related to census."),
 (297, "occurrence", "Choose the correct spelling in the phrase \u201ca _____ to fast service.\u201d", ["Hinderance", "Hindrence", "Hinderence", "Hindrance"], 3,
  {"Hinderance": "SPL-SOUND", "Hindrence": "SPL-SOUND", "Hinderence": "SPL-SOUND"},
  "Hindrance drops the e of hinder (hind-rance) and ends in -ance."),
 (298, "liaison", "Which spelling is correct for a written order to appear in court?", ["Subpoena", "Supoena", "Subpena", "Subpeona"], 0,
  {"Supoena": "SPL-SILENT", "Subpena": "SPL-DROP", "Subpeona": "SPL-IE-EI"},
  "Subpoena keeps the silent b of sub- and the Latin -poena (o before e)."),
 (300, "embarrass", "Which spelling completes the instruction \u201cLate applicants _____ their slot\u201d?", ["Forfiet", "Forfeit", "Forfit", "Forefeit"], 1,
  {"Forfiet": "SPL-IE-EI", "Forfit": "SPL-DROP", "Forefeit": "SPL-SOUND"},
  "Forfeit is one of the exceptions to the i-before-e rule, spelled -feit. The prefix is for-, not fore-."),
 (306, "necessary", "Which spelling is correct in the sentence \u201cThe signature on the form is _____\u201d?", ["Illegable", "Ilegible", "Illegible", "Illegeble"], 2,
  {"Illegable": "SPL-SOUND", "Ilegible": "SPL-DOUBLE", "Illegeble": "SPL-SOUND"},
  "Illegible is il- + legible: the l doubles where the prefix meets legible, and legible ends in -ible."),
 (312, "definitely", "Which spelling is correct in the phrase \u201cThe new form is _____ faster\u201d?", ["Undoubtably", "Undoutedly", "Undoubtly", "Undoubtedly"], 3,
  {"Undoubtably": "SPL-SOUND", "Undoutedly": "SPL-SILENT", "Undoubtly": "SPL-DROP"},
  "Undoubtedly is un- + doubted + -ly. It keeps the silent b of doubt and the -ed."),
 (550, "calendar", "Which spelling correctly completes \u201cWith only two clerks on duty, delays were _____\u201d?", ["Inevitable", "Inevitible", "Inevatable", "Innevitable"], 0,
  {"Inevitible": "SPL-SOUND", "Inevatable": "SPL-SOUND", "Innevitable": "SPL-DOUBLE"},
  "Inevitable is in- + evitable (avoidable), with a single n and the -able ending."),
 # CoS 2026-10-17 approved "pick a different target, or retire" for #308 (Supercede is a dictionary variant) and #311 (Publically is a recorded variant).
 # Both rows were retired now; these replacement targets wait for CoS like the 12 above.
 (308, "supersede", "Which spelling is correct in the sentence \u201cThe clerk _____ deleted the wrong file\u201d?", ["Accedentally", "Accidentaly", "Accidentally", "Acidentally"], 2,
  {"Accedentally": "SPL-SOUND", "Accidentaly": "SPL-DOUBLE", "Acidentally": "SPL-DOUBLE"},
  "Accidentally is accidental + -ly, so it keeps -al- and ends in -lly. The double c of accident stays."),
 (311, "publicly", "Choose the correctly spelled word for something that annoys or causes trouble.", ["Nuisence", "Nusiance", "Nuisanse", "Nuisance"], 3,
  {"Nuisence": "SPL-SOUND", "Nusiance": "SPL-IE-EI", "Nuisanse": "SPL-SOUND"},
  "Nuisance is spelled nui-sance: u before i, and the ending is -ance with a c."),
]
sp = SpellChecker()
bank = []
for f in glob.glob("docs/batches/*.json") + glob.glob("docs/research/**/*.json", recursive=True):
    if "audit/" in f: continue
    try: d = json.load(open(f))
    except Exception: continue
    it = d.get("items", d) if isinstance(d, dict) else d
    if isinstance(it, list): bank += [json.dumps(x, ensure_ascii=False).lower() for x in it if isinstance(x, dict) and "archetype" in x]
bank = " ".join(bank)
base = json.load(open("docs/research/audit/data/baseline-550-2026-10-17.json"))
btxt = json.dumps(base, ensure_ascii=False).lower()
KB = "qwertyuiop asdfghjkl zxcvbnm".split()
def adj(a, b): return any(a in r and b in r and abs(r.index(a) - r.index(b)) == 1 for r in KB)
errs, out = [], []
for row, old, stem, opts, k, codes, why in S:
    key = opts[k]; w = key.lower()
    old_key = next(x for x in base if x["id"] == row)["options"]
    if w not in sp: errs.append((row, "key not a dictionary word"))
    for o in opts:
        if o != key and o.lower() in sp: errs.append((row, f"foil {o} is a real word"))
        if o != key and len(o) == len(key) and sum(a != b for a, b in zip(o.lower(), w)) == 1:
            i = next(i for i, (a, b) in enumerate(zip(o.lower(), w)) if a != b)
            if adj(o.lower()[i], w[i]): errs.append((row, f"foil {o} is a keyboard slip"))
    if re.search(r"\b" + w[:-1], bank) or re.search(r"\b" + w[:-1], btxt): errs.append((row, f"target {w} already used"))
    if len(set(opts)) != 4 or set(codes) != set(opts) - {key}: errs.append((row, "options/codes"))
    out.append({"baseline_id": row, "old_target": old, "old_options": old_key, "new_target": key, "stem": stem, "options": opts, "correct_option": k,
                "foil_codes": codes, "explanation": why, "status": "proposed (CoS verdict pending; no DB change)"})
print(errs or "swaps OK:", len(out))
if errs: sys.exit(1)
json.dump({"round": "03", "batch": "baseline-b1", "date": "2026-10-17", "note": "Proposed fixes only. Apply after CoS approves. Rows keep their id; the remaining duplicates of these old targets (#53, #55, #509-#514, #516, #517, #547) still retire.", "swaps": out},
          open("docs/research/audit/fixes/round-03-baseline-b1-spelling-swaps.json", "w"), ensure_ascii=False, indent=1)
