"""CoS verdict 2026-10-17 on chatgpt-batch-002: reject the 75 para-order/error items and 13 RC items; keep and fix 12 RC items.
For each kept item: trim the padded closing sentences (keeping the spec's 150-word minimum), rewrite every distractor as a plausible unsupported or
contradicted reading, recode every distractor, rewrite the why lines, balance key positions and lengths, and tag the 'first-measure-misleads'
theme (a mock serves at most 2; the app rule is in docs/FACT_ID_MOCK_RULE_BRIEF.md)."""
import json, re
P = "docs/research/chatgpt-batch-002.json"
raw = open(P).read(); d = json.loads(raw)
REV = {"reviewer": "Chief of Staff (final approval, delegated by GT)", "reviewed_at": "2026-10-17"}
THEME = "first-measure-misleads"
# id: (max sentences to trim, key position, key, key why, [(distractor, code, why)], method, terms, themed)
K = {
"050002": (2, 2, "One stall's late shipment had not yet been put out for sale.",
  "The larger shipment arrived on the last day and was never displayed, so those leftovers had no fair chance to sell.",
  [("The stall's vendors had recorded their daily sales carelessly.", "RC-NOT-IN-TEXT", "The passage never questions the vendors' records; the problem was timing."),
   ("The other two stalls had hidden some unsold boxes from the manager.", "RC-NOT-IN-TEXT", "Nothing suggests any stall hid stock."),
   ("The manager had already cut that stall's allocation before the review.", "RC-OPPOSITE", "He only proposed the cut; the review came first and changed the plan.")],
  "Look for the sentence with \"however\": it names what the first comparison missed.", "Inference: a conclusion the passage supports without stating it word for word.", True),
"050003": (2, 1, "Showing the date and hour each station was last checked",
  "The makers added the date and hour of the last observation so users can judge how fresh each entry is.",
  [("Letting business owners post corrections without a volunteer's review", "RC-OPPOSITE", "The passage requires a volunteer to confirm every correction first."),
   ("Adding automatic user reports so the map updates more often", "RC-OPPOSITE", "The team postponed automatic reports until it could stop false submissions."),
   ("Marking each station as permanently open or permanently closed", "RC-OPPOSITE", "The makers chose not to label points as permanently available.")],
  "Match the risk (a station open in the morning may close later) to the feature that answers it.", "Detail question: the answer is stated in the passage.", False),
"050005": (2, 3, "A new service should work for all patients in everyday conditions.",
  "Every adjustment (bigger numbers, a printed backup, spoken announcements, a busy-morning test) makes the display work for different patients in ordinary use.",
  [("Digital displays should replace staff announcements in busy clinics.", "RC-OPPOSITE", "The clinic added spoken announcements alongside the display."),
   ("New systems are best tested during quiet hours to avoid disruption.", "RC-OPPOSITE", "The team moved its test to a busy morning on purpose."),
   ("Clinics should cut down how often patients need to speak with reception.", "RC-TOO-NARROW", "Fewer queue questions was one early benefit, not the principle behind the changes.")],
  "Find the manager's sentence that states the rule: judge a tool by whether different patients can use it in ordinary conditions.", "Main idea: the principle that explains every change, not just one of them.", True),
"050007": (2, 0, "Agreeing to local archiving was not the same as agreeing to online posting.",
  "The passage says consent to a recording for local archiving did not necessarily mean consent to unlimited online publication.",
  [("Researchers had offered to correct the names and dates in the notes.", "RC-NOT-IN-TEXT", "The center offered the narrators, not the researchers, a chance to correct the notes."),
   ("Some elders had told their stories without allowing any recording.", "RC-NOT-IN-TEXT", "True, but those stories were never recorded, so they were not part of the posting question."),
   ("A new rule required a separate permit for every file posted online.", "RC-NOT-IN-TEXT", "No such rule is mentioned; the review was the center's own choice.")],
  "The word \"because\" in the review sentence gives the reason directly.", "Detail question: the reason is stated in the passage.", False),
"050011": (2, 1, "Patients still waiting for results could now answer the survey.",
  "Moving the survey to appointment slips let waiting patients answer, so the sample now included the delays the first survey missed.",
  [("The laboratory took longer to release results that same week.", "RC-OPPOSITE", "The passage says laboratory procedures had not changed that week."),
   ("Patients gave negative answers to protest the new appointment slips.", "RC-NOT-IN-TEXT", "No protest is mentioned; the director told staff not to blame patients."),
   ("Fewer patients answered once the survey moved to appointment slips.", "RC-NOT-IN-TEXT", "The passage never says the number of answers fell.")],
  "Ask who could answer before and after the change.", "Inference: explain a result using what the passage states.", True),
"050012": (2, 2, "Water from the roof edge added to one container's rainfall.",
  "The container below the roof edge caught runoff as well as rain, so it measured more than the rainfall at that spot.",
  [("The western side of the campus really does receive more rain.", "RC-NOT-IN-TEXT", "The passage treats that conclusion as hasty; the gap shrank once the container was moved."),
   ("The students read the containers at different times after each storm.", "RC-NOT-IN-TEXT", "Reading times are never mentioned."),
   ("One container was a different size from the others that were used.", "RC-OPPOSITE", "The students used identical containers.")],
  "The teacher's question (was it measuring rainfall alone?) points to the cause.", "Inference: identify what weakened a comparison.", True),
"050015": (2, 3, "A central register that departments check before assigning a number",
  "The duplicates came from separate numbering sequences, and a shared register checked before each new number removes that cause.",
  [("Rescanning every cover page at a higher resolution", "RC-OPPOSITE", "The audit found the scans were accurate; scanning was not the cause."),
   ("Letting each department keep its own separate numbering sequence", "RC-OPPOSITE", "Separate sequences were what produced the duplicates."),
   ("Deleting the duplicate entries so that only one copy of each remains", "RC-OPPOSITE", "The unit kept the original entries for audit instead of deleting them.")],
  "Find the cause the audit named (how numbers were assigned), then the change aimed at it.", "Inference: match a fix to the cause the passage identifies.", True),
"050019": (2, 0, "The evidence could not support an exact year for some photos.",
  "Contributors often remembered places but not years, so the archivist recorded ranges rather than claim a precision the evidence lacked.",
  [("Contributors had asked that their photos carry no exact dates.", "RC-NOT-IN-TEXT", "No contributor made such a request."),
   ("The age of the buildings already showed the precise year of each photo.", "RC-OPPOSITE", "The archivist declined to date photos from building age alone."),
   ("Ranges let the archives avoid having to revise any captions later.", "RC-OPPOSITE", "The archives did revise captions, and corrections are documented openly.")],
  "Find what contributors could not remember, then why a range is used instead.", "Inference: explain a choice from the facts the passage gives.", False),
"050020": (2, 1, "Shaded panels could not store enough energy for the night.",
  "New branches shaded the panels during the day, so the batteries held too little energy to light the lamps all night.",
  [("The batteries were the wrong type for the lamps installed.", "RC-NOT-IN-TEXT", "Battery type is never mentioned; battery checks were added only later."),
   ("Residents had switched off some lamps to save electricity.", "RC-NOT-IN-TEXT", "Nothing says residents turned lamps off."),
   ("The first inspection had missed lamps that never switched on.", "RC-OPPOSITE", "The first inspection found every lamp switched on at dusk.")],
  "Follow the chain the workers found: branches, shade, too little stored energy.", "Inference: trace a stated cause and effect.", True),
"050022": (2, 2, "Listing each offer's delivery, moisture, payment and deductions",
  "Prices only became comparable once the bulletin showed the conditions behind each one.",
  [("Adding a short summary so members could scan the bulletin quickly", "RC-NOT-IN-TEXT", "The summary made the bulletin easier to read; the passage does not credit it with fairness."),
   ("Showing only the highest offer from each buyer every week", "RC-NOT-IN-TEXT", "The cooperative never limited the bulletin to top offers."),
   ("Asking buyers to post one price that covers every delivery term", "RC-NOT-IN-TEXT", "The passage describes no such request to buyers.")],
  "Find the stated unfairness (prices under different conditions), then the change that exposes those conditions.", "Inference: match a fix to the problem the passage describes.", True),
"050023": (2, 3, "Whether listeners could name the right meeting point unprompted",
  "The office asked new residents to describe the instructions without prompting and counted location mistakes.",
  [("Whether the message sounded more official than before", "RC-OPPOSITE", "Staff said a message succeeds when listeners can act on it, not when it sounds official."),
   ("Whether more households tuned in to the practice broadcast", "RC-NOT-IN-TEXT", "Audience size is never mentioned."),
   ("Whether dialect speakers understood the message as well as others", "RC-NOT-IN-TEXT", "That test was only planned for later; it did not judge this revision.")],
  "Look for the test after the revision and what it counted.", "Inference: identify the measure of success the passage describes.", True),
"050025": (2, 1, "Households differed in medicine left and in how safely they could be reached.",
  "Some patients had one day's supply and others several weeks, and routes differed in safety, so equal treatment did not mean identical scheduling.",
  [("Giving every household the same priority would make the records too long to keep.", "RC-NOT-IN-TEXT", "Record length is never given as a reason."),
   ("Remote households had asked to be served after the town center.", "RC-NOT-IN-TEXT", "No household made such a request."),
   ("Treating everyone identically is unfair in every situation.", "RC-EXTREME", "The nurse said equal treatment does not always mean identical scheduling, not that it is never fair.")],
  "The nurse's explanation follows the colon: supplies differed.", "Inference: explain a decision from the reasons the passage states.", False),
}
IDS = ["o1", "o2", "o3", "o4"]
def trim(stem, n):
    lead, body, q = stem.split("\n\n")
    sents = re.split(r"(?<=[.!?])\s+", body.strip())
    while n and len(" ".join(sents[:-n]).split()) < 150:  # trim the padded tail, but keep the spec's 150-word minimum
        n -= 1
    body = " ".join(sents[:-n]) if n else body.strip()
    return f"{lead}\n\n{body}\n\n{q}", len(body.split())
kept, rej = [], []
for it in d["items"]:
    s = it["id"][-6:]
    if it.get("reviewer"):  # already applied
        continue
    if s in K:
        n, pos, key, kwhy, wrong, method, terms, themed = K[s]
        it["stem"], wc = trim(it["stem"], n)
        assert 150 <= wc <= 250, (s, wc)
        ch = list(wrong); ch.insert(pos, (key, None, kwhy))
        it["options"] = [{"option_id": IDS[i], "text": c[0]} for i, c in enumerate(ch)]
        it["answer_option_id"] = IDS[pos]
        it["distractor_reasoning"] = {IDS[i]: c[1] for i, c in enumerate(ch) if c[1]}
        it["reveal"] = {"terms": terms, "shortcut": method, "why_correct": kwhy, "why_wrong": {IDS[i]: c[2] for i, c in enumerate(ch) if c[1]}}
        if themed: it["theme"] = THEME
        it.update(status="approved", review_status="passed", **REV)
        note = re.sub(r"\s*\|?\s*Grok Bot audit 2026-10-17:[^|]*Still draft\.", "", it.get("notes") or "").strip(" |")
        it["notes"] = (note + " | Grok Bot fix 2026-10-17: padded tail trimmed, every distractor rewritten and recoded, whys rewritten. Approved by CoS 2026-10-17.").strip(" |")
        kept.append((s, wc, it["answer_option_id"], themed))
    else:
        it.update(status="draft", review_status="rejected", **REV)
        why = "the key is also semantically odd; " if s == "050075" else ""
        what = "RC item not kept (single-theme batch; 12 of 25 RC kept)" if "RC" in it["archetype"] else "templated item"
        it["notes"] = ((it.get("notes") or "") + f" | Rejected by CoS 2026-10-17: {why}{what}.").strip(" |")
        rej.append(s)
d["status"] = "reviewed by CoS 2026-10-17 (12 approved, 88 rejected)"
open(P, "w").write(json.dumps(d, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""))
print(len(kept), "kept", len(rej), "rejected", kept)
