"""gap-fill-2000-05 (part A): English Verbal drafts: paragraph organization 8 (need 6) + reading comprehension 7 (need 5).
Hand-written passage items carry _legacy=True like gap-fill-005 (no deterministic solver exists for passage items); keys are justified in why_correct.
Run: python3 scripts/batches/gapfill/gap_fill_2000_05.py -> docs/research/gap-fill-2000-05.json"""
import json, os, random
from collections import Counter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
rng = random.Random(200005)
PO = [  # topic, sentences in logical order
("a barangay water interruption", ["The water district announced a twelve-hour interruption for pipe repairs on Saturday.", "On Friday evening, residents filled pails and drums with enough water for the day.", "During the repair, a tanker truck parked at the barangay hall for those who ran short.", "By Saturday night, the water was back on and the tanker left."]),
("renewing a driver's license", ["Ramon booked an online appointment two weeks before his license expired.", "At the LTO office, he first passed the medical examination.", "He then paid the renewal fee at the cashier and had his photo taken.", "He left the office with a new license valid for ten years."]),
("a new filing system", ["The records unit kept losing folders because files were stored by date received.", "The supervisor proposed filing every folder by client surname instead.", "Over one weekend, the staff relabeled and moved all the folders.", "Since then, retrieval time has dropped from minutes to seconds."]),
("a school feeding program", ["Teachers noticed that many pupils came to class without breakfast.", "The school then asked parents and a local bakery to help.", "Starting in June, every pupil received bread and milk before the first class.", "By the end of the quarter, attendance and attention in class had improved."]),
("a typhoon response", ["PAGASA raised a wind signal over the province on Tuesday afternoon.", "That night, the municipal disaster office moved coastal families to the gym.", "The typhoon made landfall early Wednesday and toppled several power posts.", "Once the winds eased, linemen restored electricity within two days."]),
("an office energy-saving drive", ["The agency's electricity bill rose sharply over the summer.", "To find out why, the admin officer checked every floor after office hours.", "She found air conditioners and computers left running overnight.", "A shutdown checklist was posted, and the next bill fell by a fifth."]),
("a citizen's complaint", ["A resident wrote to the city hall about a broken streetlight near the school.", "The engineering office logged the letter and sent a crew to inspect the post.", "The crew replaced the faulty bulb and its wiring the next morning.", "The office then wrote back to tell the resident the repair was done."]),
("a community garden", ["An empty lot behind the health center had become a dumping site.", "Volunteers cleared the trash and tested the soil with help from the agriculture office.", "They then planted pechay, tomatoes and eggplant in raised beds.", "Today the harvest goes to the center's nutrition classes for mothers."]),
]
RC = [  # passage, question, key, opposite, not-in-text, extreme/narrow, code4, reason, archetype
("The city opened a weekend lane at its civil registry for working residents. In the first month, the lane handled about 300 requests, most of them for birth certificates. Staff noticed, however, that many applicants arrived without a valid ID and had to come back. The registry now posts the list of requirements on its social media page every Friday.",
 "Why does the registry now post the requirements every Friday?", "Many weekend applicants lacked a valid ID and had to return.", "Applicants complained that the weekend lane was always empty.", "The registry wanted to stop issuing birth certificates on weekends.", "Every applicant in the first month came without a valid ID.", "RC-EXTREME",
 "The passage links the Friday posts to the many applicants who came without a valid ID and had to come back.", "VEN-RC-DETAIL"),
("Mangrove seedlings planted in the wrong zone often die within months. Seedlings placed too low on the shore are drowned by the tide twice a day, while those placed too high dry out. Groups that first study where wild mangroves already grow tend to see far more of their seedlings survive.",
 "What can be inferred about successful mangrove planting?", "Choosing the right spot on the shore matters as much as planting.", "Planting more seedlings guarantees success in any part of the shore.", "Mangrove seedlings grow best when they are watered by hand daily.", "Seedlings planted low on the shore always survive the tides.", "RC-EXTREME",
 "Seedlings die when placed too low or too high, and groups that copy where wild mangroves grow see more survive, so location is key.", "VEN-RC-INFER"),
("Before the new queue system, clients at the municipal treasury stood in one long line regardless of their transaction. Now a guard gives each client a numbered stub for one of three windows: payments, certifications and inquiries. Average waiting time fell from about an hour to twenty minutes, although clients with several transactions must now line up more than once.",
 "Which statement best summarizes the passage?", "Separate windows cut waiting time, though some clients queue more than once.", "The new queue system made waiting time at the treasury longer than before.", "The treasury hired more guards to handle complaints about the old line.", "Clients now wait twenty minutes for each of their several transactions.", "RC-TOO-NARROW",
 "The summary must keep both the main result (waiting fell from an hour to twenty minutes) and the stated drawback (several transactions mean several lines).", "VEN-RC-MAIN"),
("In the memo, the director asked division chiefs to \"temper\" their requests for new equipment because the budget for the coming year had been reduced. Chiefs were told to list only items needed to keep current services running.",
 "As used in the memo, \"temper\" most nearly means", "moderate or scale down", "increase or expand greatly", "harden by heating and cooling", "express in an angry mood", "VRB-SYNONYM-TRAP",
 "The budget was reduced and chiefs must list only essential items, so \"temper\" means to moderate or scale down the requests.", "VEN-RC-VOCAB"),
("A rural health unit began sending text reminders to mothers two days before their children's vaccination dates. Over six months, the share of children who missed a scheduled dose fell from one in four to one in ten. Nurses say some mothers still miss visits because the nearest jeepney stop is far from their homes.",
 "Based on the passage, which statement is best supported?", "Reminders helped, but distance still keeps some mothers from visits.", "The text reminders had no effect on missed vaccination doses at all.", "The health unit has started a free jeepney service for mothers.", "Text reminders have completely ended missed vaccination doses.", "RC-EXTREME",
 "Missed doses fell from one in four to one in ten, but nurses say distance still causes some missed visits, so both parts are supported.", "VEN-RC-INFER"),
("Under the new rule, government offices must act on simple transactions within three working days. A simple transaction is one that needs only a routine check of submitted documents. Requests that require a technical evaluation, such as a building permit, follow longer timelines set by each office.",
 "According to the passage, which request follows a longer timeline?", "A building permit that needs a technical evaluation", "A simple request needing only a routine document check", "A request filed at an office outside the city hall", "Every request filed during the three-day period", "RC-TOO-BROAD",
 "The passage names building permits as requests that need technical evaluation and so follow longer timelines.", "VEN-RC-DETAIL"),
("A fishing cooperative in Bohol began keeping a logbook of every catch: the species, its size and where it was caught. After two years, the records showed that juvenile fish were caught most often near a single reef. The members voted to stop fishing there for six months each year.",
 "What is the main idea of the passage?", "Catch records helped the cooperative decide how to protect young fish.", "The cooperative stopped keeping records because they were not useful.", "The cooperative moved its members to a new town in another province.", "The logbook recorded only the species and size of each catch.", "RC-TOO-NARROW",
 "The passage moves from keeping records, to what they showed about juvenile fish, to the decision to close the reef seasonally.", "VEN-RC-MAIN"),
]
items = []
L = "PQRS"
for n, (topic, ss) in enumerate(PO, 1):
    while True:
        perm = rng.sample(range(4), 4)
        if perm != [0, 1, 2, 3]: break
    lab = {perm[j]: L[j] for j in range(4)}
    code = lambda seq: "-".join(lab[i] for i in seq)
    key, d1, d2, d3 = code([0, 1, 2, 3]), code([3, 0, 1, 2]), code([0, 2, 1, 3]), code([0, 1, 3, 2])
    lead = ["Arrange the sentences into a logical paragraph about", "Which order makes a coherent paragraph about", "Choose the best sequence for a paragraph about", "Put these sentences in order to describe"][n % 4]
    stem = f"{lead} {topic}.\n" + "\n".join(f"{L[j]}. {ss[perm[j]]}" for j in range(4))
    items.append(dict(arch="VEN-PARA-ORDER", comp="Paragraph organization", concept="ordering", ms="sequence sentences by time and cause-effect clues", sec=60,
        stem=stem, key=key, ds=[(d1, "PO-OPENER-MISPLACED", f"\"{d1}\" puts the closing outcome ({lab[3]}) first; the paragraph must open with {lab[0]}."),
                                (d2, "LOG-ORDER-SWAP", f"\"{d2}\" swaps {lab[1]} and {lab[2]}; {lab[1]} has to happen before {lab[2]}."),
                                (d3, "PO-TRANSITION-IGNORED", f"\"{d3}\" places the outcome ({lab[3]}) before the step it follows ({lab[2]}).")],
        terms="A coherent paragraph moves from the starting situation through the steps in time order to the result.",
        sc="Find the opener (the situation or trigger) and the closer (the result); then order the middle by time words.",
        why=f"Answer: \"{key}\". {lab[0]} sets up the situation, {lab[1]} and {lab[2]} are the next steps in time order, and {lab[3]} gives the result."))
for n, (p, q, k, opp, nit, oth, c4, why, arch) in enumerate(RC, 1):
    w4 = {"RC-EXTREME": "overstates the passage; it goes further than what is said", "RC-TOO-NARROW": "covers only one detail, not the whole passage",
          "RC-TOO-BROAD": "is too broad; the passage singles out one kind of request", "VRB-SYNONYM-TRAP": "is a different sense of the word that does not fit this sentence"}[c4]
    c1 = "VRB-ANTONYM-TRAP" if arch == "VEN-RC-VOCAB" else "RC-OPPOSITE"
    c2 = "VRB-SYNONYM-TRAP" if arch == "VEN-RC-VOCAB" else "RC-NOT-IN-TEXT"
    if arch == "VEN-RC-VOCAB": c4 = "VRB-SYNONYM-TRAP"; w4 = "is another sense of \"temper\" (anger) that does not fit the memo"
    items.append(dict(arch=arch, comp="Reading comprehension", concept="comprehension", ms="identify what the passage states or supports", sec=70,
        stem=f"Read the passage.\n{p}\n\n{q}", key=k,
        ds=[(opp, c1, f"\"{opp}\" says the opposite of the passage."), (nit, c2, f"\"{nit}\" " + ("is another sense of the word that does not fit." if arch == "VEN-RC-VOCAB" else "is not mentioned in the passage.")), (oth, c4, f"\"{oth}\" {w4}.")],
        terms="The correct answer is stated in the passage or follows directly from it.", sc="Check each choice against a specific sentence in the passage; reject any choice with no support or that overstates.",
        why=f"Answer: \"{k}\" {why}" if k.endswith(".") else f"Answer: \"{k}\". {why}"))
out = []
PFX = {"VEN-PARA-ORDER": "PO", "VEN-RC-DETAIL": "RCD", "VEN-RC-INFER": "RCI", "VEN-RC-MAIN": "RCM", "VEN-RC-VOCAB": "RCV"}
cnt = Counter()
for n, it in enumerate(items):
    opts = [it["key"]] + [x[0] for x in it["ds"]]
    slot = n % 4; order = opts[1:]; order.insert(slot, opts[0])
    ids = ["o1", "o2", "o3", "o4"]; idx = {t: ids[i] for i, t in enumerate(order)}
    cnt[it["arch"]] += 1
    out.append(dict(id=f"CIVIO-GF2K05-{PFX[it['arch']]}-{cnt[it['arch']]:04d}", track="both", domain="verbal_en", competency=it["comp"], concept=it["concept"],
        micro_skill=it["ms"], archetype=it["arch"], difficulty="medium", est_seconds=it["sec"], language="en", stem=it["stem"],
        options=[{"option_id": ids[i], "text": t} for i, t in enumerate(order)], answer_option_id=idx[it["key"]],
        reveal={"terms": it["terms"], "shortcut": it["sc"], "why_correct": it["why"], "why_wrong": {idx[t]: w for t, _, w in it["ds"]}},
        distractor_reasoning={idx[t]: c for t, c, _ in it["ds"]}, source="Original, Civio", source_url=None, source_group="civio",
        status="draft", review_status="unreviewed", _legacy=True,
        provenance={"author": "Grok Bot", "method": "ai_assisted", "created_at": "2026-10-18T03:00:00+08:00", "spec_version": "0.1.9"},
        notes="gap-fill-2000-05 (English Verbal). Pending CoS."))
json.dump({"batch": "gap-fill-2000-05", "spec_version": "0.1.9", "status": "draft (pending CoS)", "source_group": "civio",
           "notes": "English Verbal paragraph organization + reading comprehension gap fill for the exact-2,000 Release Collection.", "items": out},
          open(os.path.join(ROOT, "docs/research/gap-fill-2000-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), Counter(i["archetype"] for i in out))
