"""gap-fill-2000-05 (part B): explanation/lint fixes for Release Collection picks in English Verbal that fail explanation_lint.
Priority: sentence structure, then error recognition, paragraph organization, reading comprehension.
Each fix is a full copy of the picked item with id <orig>-LINTFIX, fix_of=<orig>, status draft/unreviewed. Originals are NOT edited.
Only reveal text is changed, except LONG-KEY items, where wrong options are rewritten to similar length (same error, same code).
Run: python3 scripts/batches/gapfill/lintfix_2000_05.py MANIFEST.json BASELINE.json -> docs/research/audit/fixes/gap-fill-2000-05-lintfix.json"""
import copy, glob, json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "batches", "audit"))
import explanation_lint as L
sys.path.insert(0, os.path.dirname(__file__))
from lintfix_2000_05_baseline import COMPLETE, STEM
sys.path.insert(0, os.path.join(ROOT, "scripts", "batches"))
import qa
manifest = json.load(open(sys.argv[1]))["manifest"]["verbal_en"]
idx = {}
for f in glob.glob(os.path.join(ROOT, "docs/batches/batch-*.json")) + glob.glob(os.path.join(ROOT, "docs/research/*.json")) + [sys.argv[2]]:
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    for i in (d.get("items") if isinstance(d, dict) else d) or []:
        if isinstance(i, dict) and "id" in i: idx.setdefault(i["id"], i)
# hand-written reasons (replace the whole why_correct body after "Answer: ...")
WHY = {
 "CIVIO-VEN-ERROR-AGREE-000076": "The subject is \"stack\", which is singular; \"of folders\" only describes it. A singular past subject takes \"was\".",
 "CIVIO-VEN-ERROR-AGREE-000167": "The subject is \"head\", which is singular; \"of the three sections\" only describes it, so the verb is \"was\".",
 "CIVIO-VEN-ERROR-AGREE-000172": "The subject is \"list\", which is singular; \"of approved applicants\" only describes it, so the verb is \"is\".",
 "CIVIO-VEN-ERROR-AGREE-000470": "The subject is \"box\", which is singular; \"of old receipts\" only describes it, so the verb is \"was\".",
 "CIVIO-VEN-ERROR-AGREE-000568": "The subject is \"cost\", which is singular; \"of the repairs\" only describes it, so the verb is \"is\".",
 "CIVIO-VEN-ERROR-AGREE-000572": "\"Neither\" used alone as the subject is singular (neither one), so it takes \"was\", not \"were\".",
 "CIVIO-VEN-ERROR-AGREE-000681": "The subject is \"One\", which is singular; \"of the barangay tanods\" only describes it, so the verb takes -s: \"guards\".",
 "CIVIO-BASELINE-0022": "A simple sentence has exactly one independent clause: one subject-verb pair that can stand alone.",
 "CIVIO-BASELINE-0023": "It joins two independent clauses (\"I studied\" and \"I rested\") with a comma and the conjunction \"and\". The other choices are fragments.",
 "CIVIO-BASELINE-0024": "A topic sentence tells the reader what the paragraph is about; the other sentences then support it.",
 "CIVIO-BASELINE-0025": "Coherence means each idea connects logically to the one before it, usually with clear order and transitions.",
 "CIVIO-BASELINE-0026": "The main idea is what the whole passage is mostly about, not a small detail of how it was printed or punctuated.",
 "CIVIO-BASELINE-0027": "An inference is not stated outright; it is a conclusion the reader can reasonably draw from evidence in the text.",
 "CIVIO-GAP5-VEN-RC-DETAIL-0019": "The passage says real redelivery fees are paid at the couriers' branches or in their official apps, never through a texted link.",
}
SENT_GENERIC = "It is the only choice that is one complete, correctly joined sentence with every describing phrase in place. "
# LONG-KEY: rewrite wrong options to similar length; {id: {old_text: new_text}}. Each keeps the same error and code.
OPT = {
 "CIVIO-BASELINE-0113": {"One independent clause only": "One independent clause with no other clause", "Only dependent clauses": "Only dependent clauses with no main clause", "A title without a verb": "A heading or title that has no verb in it"},
 "CIVIO-BASELINE-0114": {"The clerk filed the papers.": "The clerk filed the papers on Monday and left the office at noon.", "File. Sign. Archive.": "File the papers. Sign the form. Archive the folder today."},
 "CIVIO-BASELINE-0116": {"Removing all verbs": "Removing every verb so that no clause is left in the sentence", "Writing only fragments": "Breaking it into fragments that cannot stand alone as sentences"},
 "CIVIO-BASELINE-0024": {"Lists unrelated facts only": "Lists unrelated facts that do not share a point", "Ends every essay": "Appears only at the end of every essay", "Replaces the conclusion": "Replaces the concluding sentence of the paragraph"},
 "CIVIO-BASELINE-0124": {"Font size": "The font size used in the text", "Page margins": "The width of the page margins", "Speaker volume": "How loudly the speaker talks"},
 "CIVIO-BASELINE-0244": {"Unrelated jokes only": "Unrelated jokes that do not connect to the topic", "Deleting the topic": "Deleting the topic sentence from the paragraph", "Ending punctuation rules": "Rules about the punctuation at the end of sentences"},
 "CIVIO-BASELINE-0449": {"The building has three windows.": "The permit office building has three large windows.", "Yesterday was humid.": "Yesterday was humid, and many applicants came late.", "Some forms are blue.": "Some of the permit forms are printed on blue paper."},
 "CIVIO-BASELINE-0534": {"The office has a green door.": "The office has a green door near the main lobby.", "Some keyboards are wireless.": "Some of the office keyboards are wireless models.", "Yesterday had light traffic.": "Yesterday had light traffic on the road to work."},
 "CIVIO-GAP1-VEN-RC-0014": {"Stairs are dangerous in all public buildings": "Stairs are dangerous for everyone in all public buildings", "Relatives should stop paying for senior citizens": "Relatives should stop paying taxes for senior citizens now", "The treasurer's office will close in August": "The treasurer's office will close its ground-floor counter in August"},
 "CIVIO-GAP1-VEN-RC-0015": {"Paid at a second counter": "Paid at a second counter upstairs", "Paid online": "Paid online through the city website", "Stopped paying their taxes": "Stopped paying their taxes entirely"},
 "CIVIO-BASELINE-0027": {"Copied word-for-word only": "Copied word for word from the passage", "Always stated in the title": "Always stated directly in the title", "Impossible to support": "Impossible to support with the text"},
 "CIVIO-BASELINE-0125": {"Prevents all corruption automatically": "Prevents all corruption automatically and completely", "Replaces the need for elections": "Replaces the need for citizens to vote in elections", "Applies only to private banks": "Applies only to the records of private banks"},
 "CIVIO-BASELINE-0126": {"Training is useless in all cases": "Training is useless in all cases and should stop", "Coaching replaces all training": "Coaching can fully replace all formal training", "Gains never occur": "Gains from training never occur at all"},
 "CIVIO-BASELINE-0127": {"Never used": "Never used by anyone during actual evacuations", "Illegal": "Illegal to post in barangay halls and public places", "Only decorative": "Only decorative pictures that are not meant to guide anyone"},
 "CIVIO-BASELINE-0128": {"Hiring by connections always builds trust": "Hiring by personal connections always builds public trust", "Bureaucracy should ignore merit": "Government offices should ignore merit when they hire staff", "Trust is unrelated to hiring": "Public trust has nothing to do with how officials are hired"},
 "CIVIO-BASELINE-0129": {"Printer ink costs only": "The high cost of printer ink in government offices", "Too many service centers downtown": "Too many service centers built in the downtown area", "Excess paper forms exclusively": "Too many paper forms required for every service"},
 "CIVIO-BASELINE-0130": {"Anecdotes vs. poetry": "Personal anecdotes vs. poems", "Policy vs. law dictionaries": "Public policy vs. law dictionaries", "Servers vs. desktops": "Office servers vs. desktop computers"},
 "CIVIO-BASELINE-0131": {"Ignore the exception": "Ignore the exception and apply the rule", "Assume no exceptions ever exist": "Assume that no exceptions ever exist anywhere", "Skip to the title only": "Skip the passage and read only the title"},
 "CIVIO-BASELINE-0132": {"Feedback had no effect": "Community feedback had no effect at all", "Permits were abolished": "Permits were abolished after the feedback", "Two days were added": "Two days were added to the permit process"},
 "CIVIO-BASELINE-0246": {"Hide performance expectations": "Hide their performance expectations from the public", "Abolish all services": "Abolish all of their public services", "Replace laws with posters": "Replace written laws with posters on the wall"},
 "CIVIO-BASELINE-0456": {"Online forms have no possible benefit": "Online forms have no possible benefit for the office", "Internet access is irrelevant": "Internet access is irrelevant to online forms", "Paper forms are always illegal": "Paper forms are now always illegal to use"},
 "CIVIO-BASELINE-0466": {"Magsara nang mas maaga": "Magsara nang mas maaga sa hapon", "Magdaos ng paligsahan": "Magdaos ng paligsahan sa tanggapan", "Magpalit ng gusali": "Lumipat sa bagong gusali ng tanggapan"},
}
def clean(w):
    w = w.replace(SENT_GENERIC, "")
    m = re.search(r"\s*Therefore, the correct option is .*$", w, re.S)
    if m: w = w[:m.start()].rstrip() + "."
    w = re.sub(r"^Answer:[^.]*\.\s*", "", w)
    return w.strip()
SKIP = {"CIVIO-BASELINE-0466": "Filipino-language item classified as English Verbal; CoS should move it to verbal_fil or drop it from the EV pick",
        "CIVIO-GAP1-VEN-RC-0014": "passage set 0014-0017 shares a passage under the 400-character sibling floor; the original set already fails qa_file; CoS: lengthen the passage or keep one question",
        "CIVIO-GAP1-VEN-RC-0015": "same passage set as 0014", "CIVIO-GAP1-VEN-RC-0017": "same passage set as 0014"}
STEM.update({"CIVIO-GAP2-VEN-ERROR-0002": "Which sentence about the office report is written correctly?"})
out, log, skipped = [], [], []
order = ["sentence structure", "error recognition", "paragraph organization", "reading comprehension", "sentence completion", "word meaning"]
for sub in order:
    for oid in manifest.get(sub, []):
        it = idx[oid]; probs = L.lint_item(it)
        if not probs: continue
        if oid in SKIP: skipped.append((oid, SKIP[oid])); continue
        fx = copy.deepcopy(it)
        changed_opts = []
        for o in fx["options"]:
            new = OPT.get(oid, {}).get(o["text"])
            if new and o["option_id"] != fx["answer_option_id"]:
                ww = fx["reveal"]["why_wrong"].get(o["option_id"], "")
                fx["reveal"]["why_wrong"][o["option_id"]] = f"\"{new}\" — " + re.sub(r"^\"[^\"]*\"\s*(—|-|:)?\s*", "", ww or "does not answer the question.")
                o["text"] = new; changed_opts.append(o["option_id"])
        if oid in COMPLETE:
            terms, sc, wr = COMPLETE[oid]
            fx["reveal"]["terms"], fx["reveal"]["shortcut"] = terms, sc
            fx["distractor_reasoning"], fx["reveal"]["why_wrong"] = {}, {}
            for o in fx["options"]:
                if o["option_id"] != fx["answer_option_id"]:
                    c, w = wr[o["text"]]; fx["distractor_reasoning"][o["option_id"]] = c; fx["reveal"]["why_wrong"][o["option_id"]] = w
        if oid in STEM: fx["stem"] = STEM[oid]
        if not fx.get("_legacy") and qa.solve_verb(fx) is None: fx["_legacy"] = True  # hand-written verbal item with no deterministic solver (as gap-fill-005)
        key = next(o["text"] for o in fx["options"] if o["option_id"] == fx["answer_option_id"])
        body = WHY.get(oid) or clean(fx["reveal"]["why_correct"])
        fx["reveal"]["why_correct"] = f"Answer: \"{key}\"{'' if key.rstrip()[-1:] in '.?!' else '.'} {body}"
        fx["id"] = oid + "-LINTFIX"; fx["fix_of"] = oid
        fx["status"] = "draft"; fx["review_status"] = "unreviewed"
        for k in ("reviewer", "reviewed_at", "review_line"): fx.pop(k, None)
        fx["source_group"] = "civio"
        fx["notes"] = (f"gap-fill-2000-05 lint fix of {oid} (was: {', '.join(probs)}). " + ("Wrong options rewritten for length: " + ", ".join(changed_opts) + ". " if changed_opts else "") + "Pending CoS.")
        out.append(fx); log.append((sub, oid, probs, changed_opts))
dst = os.path.join(ROOT, "docs/research/audit/fixes/gap-fill-2000-05-lintfix.json")
os.makedirs(os.path.dirname(dst), exist_ok=True)
json.dump({"batch": "gap-fill-2000-05-lintfix", "spec_version": "0.1.9", "status": "draft (pending CoS)", "items": out}, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), Counter(s for s, *_ in log)); print("skipped:", skipped)
json.dump(skipped, open("/tmp/lintfix_skipped.json", "w"))
