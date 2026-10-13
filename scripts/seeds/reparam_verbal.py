"""Original verbal, logic, data, and filing-order items for the re-parameterized bank."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from build_reparameterized_bank import explain, item, pack

COMPLETIONS = [
    ("The clerk stayed _____ and finished the inventory before the typhoon.", "calm", ["careless", "absent", "noisy"], "The sentence says the work was finished, so the missing word is a steady manner."),
    ("The memo was _____ enough for a new hire to follow.", "clear", ["silent", "missing", "partial"], "A memo a new hire can follow is clear."),
    ("Officers are expected to act with _____ even when the supervisor is away.", "integrity", ["delay", "secrecy", "favoritism"], "Integrity is the conduct expected when nobody is watching."),
    ("The hearing was moved _____ the missing annex could be attached.", "so that", ["despite", "unless", "during"], "So that introduces the purpose of moving the hearing."),
    ("The second count did not _____ the first count.", "match", ["erase", "print", "fold"], "Did not match means the two counts disagreed."),
    ("The form was rewritten _____ applicants kept skipping the same box.", "because", ["although", "until", "without"], "Because introduces the reason for the rewrite."),
    ("A good index lets a clerk find a folder with little _____.", "delay", ["ink", "noise", "weather"], "The point of an index here is speed, so delay is what is reduced."),
    ("The drill is not optional; it is _____.", "required", ["rumored", "decorated", "forgotten"], "Not optional means required."),
    ("The denial was _____. It left no doubt about the decision.", "firm", ["vague", "missing", "late"], "No doubt means the denial was firm."),
    ("A new procedure must stay _____ with the written rule.", "consistent", ["contrary", "unrelated", "hidden"], "Stay consistent with means it must not conflict with the rule."),
    ("A second reviewer _____ the first count.", "confirmed", ["erased", "guessed", "hid"], "A second review that supports the count confirms it."),
    ("Staff were told to _____ from commenting on the open case.", "refrain", ["benefit", "arrive", "expand"], "Refrain from means do not do it."),
    ("The folders were labeled today, _____ the audit can start tomorrow.", "so", ["unless", "although", "despite"], "So connects the labeling to the result that the audit can start."),
    ("The guard stayed at the desk _____ the line grew longer.", "although", ["because", "unless", "until"], "Although introduces a contrast: the guard stayed even as the line grew."),
    ("Check the control number _____ you submit the form.", "before", ["despite", "unless", "during"], "Before places the check earlier than the submission."),
    ("The office rewrote the notice _____ readers had misread the date.", "after", ["unless", "despite", "without"], "After places the rewrite later than the misreading."),
    ("The sign uses short words _____ every visitor can follow it.", "so that", ["unless", "despite", "although"], "So that introduces the purpose."),
    ("Follow the checklist _____ a personal shortcut.", "rather than", ["because of", "except", "during"], "Rather than contrasts the checklist with a personal shortcut."),
    ("The session was reset _____ two members were still in the field.", "because", ["although", "until", "without"], "Because gives the reason for the reset."),
    ("The team finished the count _____ the rain.", "despite", ["because", "unless", "after"], "Despite means the rain did not stop the count."),
    ("Bring a photocopy _____ the original certificate.", "of", ["despite", "unless", "during"], "A photocopy of the original is the standard phrase."),
    ("The request moves forward _____ every required box is filled.", "once", ["unless", "despite", "although"], "Once means as soon as the boxes are filled."),
    ("The board approved the draft _____ counsel had signed it.", "after", ["unless", "despite", "although"], "After places the approval later than the signature."),
    ("Keep the receipt _____ the supply officer asks for it.", "until", ["despite", "unless", "although"], "Until means keep it up to the time of the request."),
    ("The gate stays shut _____ the duty officer opens it.", "until", ["because", "despite", "although"], "Until marks the time the shut gate changes."),
    ("File the annex _____ the main report, not in a separate drawer.", "with", ["despite", "unless", "although"], "With means the annex stays together with the report."),
]

ERRORS = [
    ("Which sentence has an error in subject-verb agreement?", "The list of names are on the desk.", ["The list of names is on the desk.", "The names on the list are complete.", "Both clerks are ready."], "List is singular, so the verb is is, not are."),
    ("Which sentence has an error in pronoun case?", "The memo was addressed to her and I.", ["The memo was addressed to her and me.", "She and I signed the memo.", "The clerk handed it to me."], "The object form after to is me, not I."),
    ("Which sentence uses a dangling modifier?", "Walking into the room, the folder was already open.", ["Walking into the room, the clerk found the folder open.", "The clerk found the folder open.", "The folder on the desk was open."], "The opener must name who was walking."),
    ("Which sentence pairs a past time word with a present verb?", "Yesterday the clerk submits the report.", ["Yesterday the clerk submitted the report.", "The clerk submits a report every Monday.", "The report was submitted yesterday."], "Yesterday needs a past verb, submitted."),
    ("Which sentence has a preposition error?", "The result was different than the estimate.", ["The result was different from the estimate.", "The result differed from the estimate.", "The estimate and the result differ."], "Different is followed by from in this standard use."),
    ("Which sentence has an article error?", "She is honest employee.", ["She is an honest employee.", "She is honest.", "An honest employee reported the gap."], "Honest starts with a vowel sound, so the article is an, and the noun needs it here."),
    ("Which sentence has a comparison error?", "This file is more better than the old one.", ["This file is better than the old one.", "This file is more complete than the old one.", "The old file is worse."], "Better is already the comparative. More better is a double comparison."),
    ("Which sentence has a misplaced modifier?", "The clerk found a memo in the drawer that was unsigned.", ["The clerk found an unsigned memo in the drawer.", "The unsigned memo was in the drawer.", "The clerk, who was careful, found the memo."], "That was unsigned seems to modify drawer. The memo is what was unsigned."),
    ("Which sentence has an error?", "Each of the forms have a signature.", ["Each of the forms has a signature.", "All of the forms have signatures.", "Every form has a signature."], "Each is singular, so the verb is has."),
    ("Which sentence uses the pronoun ambiguously?", "When Ana met Luz, she signed the log.", ["When Ana met Luz, Ana signed the log.", "Ana signed the log after the meeting.", "Luz signed her own log."], "She could be Ana or Luz. Naming the person removes the ambiguity."),
    ("Which sentence has a comma splice?", "The form was incomplete, the clerk returned it.", ["The form was incomplete, so the clerk returned it.", "The form was incomplete. The clerk returned it.", "Because the form was incomplete, the clerk returned it."], "Two full sentences cannot be joined by a comma alone."),
    ("Which sentence shifts tense without a reason?", "The team opens the box and counted the seals.", ["The team opened the box and counted the seals.", "The team opens the box and counts the seals.", "After the team opened the box, it counted the seals."], "Opens is present and counted is past. Keep one time."),
    ("Which sentence has a parallel-structure error?", "The job requires filing, to type, and answers calls.", ["The job requires filing, typing, and answering calls.", "The job requires a clerk to file, type, and answer calls.", "Filing, typing, and answering calls are required."], "The list should use the same form: filing, typing, and answering."),
    ("Which sentence has a word-choice error?", "The office will except late forms.", ["The office will accept late forms.", "The office will not accept late forms.", "Late forms are the exception."], "Accept means receive. Except means leave out."),
    ("Which of these sentences follows standard grammar?", "Neither the clerk nor the guard was late.", ["Neither the clerk nor the guard were late.", "Neither the clerk or the guard was late.", "Neither the clerks was late."], "Neither-nor takes the verb that matches the nearer subject, guard, which is singular."),
    ("Which sentence has an error in word order?", "She only filed the copies, not the originals, yesterday the annex.", ["Yesterday she filed only the copies, not the originals.", "She filed the copies yesterday.", "Only the copies were filed."], "The first sentence leaves yesterday the annex without a role in the sentence."),
    ("Which sentence uses a wrong verb form?", "The report has already been submit.", ["The report has already been submitted.", "The clerk submitted the report.", "The report is submitted."], "After been, the verb form is submitted."),
    ("Which sentence has two independent clauses joined incorrectly?", "The gate is shut the visitors wait outside.", ["The gate is shut, and the visitors wait outside.", "Because the gate is shut, the visitors wait outside.", "The visitors wait outside while the gate is shut."], "Two clauses need a joining word or separate sentences."),
]

STRUCTURES = [
    ("A compound sentence contains which of these?", "Two independent clauses", ["Only a phrase", "One dependent clause and no independent clause", "A subject with no verb"], "A compound sentence joins two clauses that could each stand alone."),
    ("Which of these is a complex sentence?", "The clerk waited until the stamp dried.", ["The clerk waited.", "The clerk waited, and the stamp dried.", "Waiting by the desk."], "Until the stamp dried is a dependent clause attached to an independent clause."),
    ("Which sentence uses parallel structure?", "She files, labels, and stores the folders.", ["She files, to label, and storage.", "She files and to label folders.", "Filing, she stores, and to label."], "Files, labels, and stores share one form."),
    ("A run-on is best repaired by which change?", "Use a period or a joining word.", ["Delete the verb", "Add a second subject with no punctuation change", "Capitalize every noun"], "A period or a conjunction separates the two clauses."),
    ("Which option is a fragment?", "Because the annex was missing.", ["The annex was missing.", "The clerk noticed the missing annex.", "The annex was missing, so the clerk called."], "Because the annex was missing cannot stand alone."),
    ("Which sentence is in the active voice?", "The clerk sealed the box.", ["The box was sealed by the clerk.", "The box was sealed.", "Sealed by the clerk, the box."], "The clerk, the actor, comes before the verb sealed."),
    ("Which join avoids a comma splice?", "The count was short, so the clerk recounted it.", ["The count was short, the clerk recounted it.", "The count was short the clerk recounted it.", "The count, was short, the clerk."], "So joins the two clauses. A comma alone does not."),
    ("A relative clause often begins with which word?", "Which", ["And", "But", "So"], "Which, who, and that commonly open a relative clause. And, but, and so are coordinators."),
    ("Which choice is a compound sentence?", "The lamp failed, and the clerk fetched a spare.", ["When the lamp failed, the clerk fetched a spare.", "The clerk fetching a spare.", "Because the lamp failed."], "And joins two independent clauses."),
    ("Which revision fixes the run-on “The box was open the seal was broken”?", "The box was open, and the seal was broken.", ["The box was open the seal was broken yesterday it.", "Open box seal broken.", "The box open, the seal."], "And joins the two complete clauses."),
    ("Which sentence combines the ideas without changing them?", "The folder was old, but it was still readable.", ["The folder was old it was still readable.", "Old folder readable but.", "Because readable, the folder old."], "But joins the age and the readability."),
    ("In a complex sentence, the dependent clause does what?", "It cannot stand as a full sentence by itself.", ["It always contains two verbs and no subject.", "It must begin with and.", "It replaces the subject of the main clause."], "A dependent clause needs the main clause to be complete."),
    ("Which sentence keeps one subject for a compound verb?", "The clerk checked the total and signed the sheet.", ["The clerk checked the total and the sheet signed.", "Checked and signed the clerk the sheet.", "The total checked the clerk and signed."], "One subject, the clerk, does both actions."),
    ("Which option is a simple sentence?", "The archive closes at five.", ["The archive closes at five, and the gate shuts.", "When the archive closes, the gate shuts.", "Closing at five and shutting the gate."], "One independent clause and no dependent clause makes a simple sentence."),
    ("Which word set can join two independent clauses?", "And, but, or", ["Because, although, when", "Which, who, that", "Of, in, on"], "And, but, and or can coordinate two independent clauses. The others introduce dependent clauses or phrases."),
]

PARAGRAPHS = [
    ("The topic sentence of a paragraph usually does what?", "States the main point", ["Lists every exception first", "Replaces the evidence", "Ends the whole memo"], "The topic sentence tells the reader the paragraph's main point."),
    ("Coherence in a paragraph means the sentences do what?", "Connect in a clear order", ["Use the same noun four times only", "Avoid every transition", "Each introduce a new subject"], "Coherent sentences follow one another in an order the reader can track."),
    ("Which order best fits a short process paragraph?", "Gather the forms, check the dates, then file the set.", ["File the set, then explain why the forms were gathered.", "Check the dates after the paragraph ends.", "Start with the signature and never name the step."], "A process moves from the first action to the last."),
    ("A concluding sentence often does what?", "Restates the point without adding a new subject", ["Opens a second unrelated subject", "Deletes the evidence", "Asks the reader to ignore the paragraph"], "The close returns to the point already made."),
    ("Unity in a paragraph means what?", "Every sentence bears on the one main point", ["Every sentence is the same length", "The paragraph names four topics", "Transitions are forbidden"], "A unified paragraph stays on one point."),
    ("Words such as however and therefore help a paragraph show what?", "How the next sentence relates to the previous one", ["The font size", "The clerk's birthday", "That the paragraph has no order"], "Those words mark contrast or result."),
    ("When you arrange a paragraph, background usually comes before what?", "The conclusion that depends on it", ["The title of a different memo", "A second unrelated story", "The page number"], "The reader needs the background before the conclusion that uses it."),
    ("Markers such as first, then, and finally signal what?", "Time or step order", ["A contradiction only", "A list of unrelated names", "That the paragraph should be deleted"], "Those markers show sequence."),
    ("Which is the best topic sentence for a paragraph about shorter permit lines?", "Permit lines grew shorter after the office split intake from payment.", ["The office bought new chairs.", "Tuesday is a weekday.", "Some visitors carry blue folders."], "The sentence states the permit-line point. The others do not."),
    ("Which order best gives instructions for submitting a form?", "Complete every box, attach the annex, then hand the set to the window.", ["Hand in the set, then learn which boxes exist.", "Attach the annex after the window has already returned it.", "Skip the boxes and start with the receipt."], "The steps follow the order a clerk would actually use."),
    ("A paragraph has one sentence about parking and four about locked cabinets. To improve unity, the writer should do what?", "Remove or relocate the parking sentence", ["Add three more parking sentences and drop the cabinets", "Delete the topic sentence", "Repeat the parking sentence four times"], "The stray parking sentence breaks a paragraph about cabinets."),
    ("Which linking word best marks a contrast?", "However", ["Therefore", "For example", "Then"], "However marks a turn. Therefore marks a result."),
    ("Which linking word best marks a result?", "Therefore", ["However", "Meanwhile", "For instance"], "Therefore introduces a result."),
    ("Which sentence best closes a paragraph about choosing a strong password?", "A long password that is not reused is harder to guess.", ["The cafeteria opens at noon.", "Passwords are a kind of word.", "The next paragraph will discuss vehicles."], "The close stays on the password point."),
]

READINGS = [
    ("A notice says: “Visitors who bring a complete folder before noon are screened the same day.” Who is screened the same day?", "A visitor with a complete folder who arrives before noon", ["Any visitor who arrives after noon", "A visitor with a missing annex who arrives at 11", "A visitor who brings no folder"], "Both conditions are required: a complete folder and arrival before noon."),
    ("A note says training without a follow-up check fades within a month. A careful inference is that:", "A later check is part of keeping the skill", ["Training should be cancelled", "A follow-up check replaces the training", "Skills never fade"], "The note ties lasting skill to the follow-up, not to cancelling training."),
    ("A barangay updates its flood map every year. The safest reading is that the map is:", "Treated as something that can change", ["Useless after the first year", "A substitute for an evacuation drill", "Required to stay identical forever"], "Updating it yearly means the office expects the map to need changes."),
    ("A memo says hiring by posted rules increased trust in the office. Which restatement stays closest?", "People trusted the office more when hiring followed posted rules.", ["Trust replaces the need for rules.", "Posted rules ended hiring.", "The memo measured every agency in the country."], "The restatement keeps both the rules and the rise in trust."),
    ("A report says people without a stable connection use the online portal less. The problem it highlights is:", "Unequal access to the online service", ["That paper forms are illegal", "That every user prefers the portal", "That connections are unrelated to use"], "Less use among people without a connection is an access gap."),
    ("A paragraph says a policy should rest on counts, not on one vivid story. The author contrasts:", "Records and a single anecdote", ["Two identical counts", "A story and another story with the same numbers", "A law and its article number"], "Counts are set against one story."),
    ("If a passage states a rule and then an exception, a careful reader should:", "Apply the exception only to the case it names", ["Ignore the rule", "Treat the exception as the rule for every case", "Skip both"], "The exception is narrower than the rule."),
    ("Community comments cut two days from a permit step. A reasonable conclusion is that:", "Those comments were followed by a shorter step", ["Comments always lengthen a permit", "Two days is the legal time limit", "The permit step was abolished"], "The sentence links the comments to a shorter step. It does not set a legal limit."),
    ("A citizen charter posts the steps and the time for each service. A reader can infer that the office wants clients to:", "Know what to expect and when", ["Skip the steps", "Guess the time limit", "Avoid the office"], "Posting steps and times is how clients know what to expect."),
    ("A line says unclear instructions are followed by more errors. The implied relationship is:", "Unclear instructions go together with more errors", ["Errors remove the need for instructions", "Clear instructions cause errors", "Errors and instructions are unrelated"], "The line connects lack of clarity with a higher error count."),
    ("Errors fell after a peer check, and the report does not mention other offices. The safest inference is:", "The peer check is one change that came before the drop in that office", ["Peer checks reduce errors in every office", "The drop had no other possible cause", "The office stopped using peer checks"], "The report supports a link in that office, not a universal cause."),
    ("Online forms take less encoding time but need a working connection. A balanced conclusion is:", "The time saving depends on the connection", ["Online forms are always faster, even offline", "Connections are irrelevant", "Encoding time always increases online"], "Both parts of the sentence have to stay in the conclusion."),
    ("A pilot served 24 of 40 applicants. What fraction were served?", "3/5", ["2/5", "24/100", "4/5"], "24 over 40 reduces to 3/5."),
    ("Records are kept for five years unless a case hold applies. What is the exception?", "A case hold", ["The five-year period itself", "Any routine file", "A missing folder label"], "Unless introduces the case hold as the exception."),
    ("A memo says: “Only complete applications received by Friday enter Monday's review.” Which application enters?", "A complete application received on Thursday", ["A complete application received on Saturday", "An incomplete application received on Friday", "A complete application with no received date"], "It must be complete and received by Friday. Thursday meets both."),
    ("A chart note says waiting time fell for six straight months. The trend described is:", "A decline across those six months", ["A rise each month", "No change", "A decline in only the first month"], "Fell for six straight months is a decline."),
    ("A desk note says 18 of 20 sampled folders had a date stamp. What percent of the sample had a stamp?", "90 percent", ["18 percent", "20 percent", "80 percent"], "18 divided by 20 is 0.9, or 90 percent."),
]

ASSUMPTIONS = [
    ("“Add a second window because the first window has a long line.” The argument assumes that:", "A second window can take part of that line", ["Long lines are required by law", "The first window should close", "Visitors prefer to wait"], "The proposal works only if the new window would serve people now in the line."),
    ("All complete forms have a blue stamp. Form K has no blue stamp. What follows?", "Form K is not a complete form", ["Form K is complete", "Every unstamped form is complete", "The stamp rule was repealed"], "If every complete form is stamped, an unstamped form is not complete."),
    ("If the shelf is low, an order is sent. No order was sent. What follows?", "The shelf was not low", ["The shelf was low", "The order was lost in the mail", "Shelves are always low"], "If low shelves always produce an order, no order means the shelf was not low."),
    ("Either the folder is in cabinet A or cabinet B. It is not in cabinet A. What follows?", "It is in cabinet B", ["It is in neither cabinet", "It is in cabinet A", "Both cabinets are empty"], "With only two stated places, ruling out A leaves B."),
    ("All archived files are indexed. File X is indexed. Which conclusion is valid?", "File X might be archived, but that does not follow from the premises", ["File X must be archived", "File X cannot be archived", "No archived file is indexed"], "All archived files are indexed does not mean all indexed files are archived."),
    ("Some sealed folders are restricted. Folder Z is sealed. Which conclusion follows?", "Folder Z may be restricted, but the premises do not say it is", ["Folder Z is restricted", "Folder Z is not restricted", "No sealed folder is restricted"], "Some does not mean every sealed folder."),
    ("All approved requests have reference numbers. Request R has no reference number. What follows?", "Request R is not approved", ["Request R is approved", "Reference numbers are optional for approved requests", "Request R has two numbers"], "If approval always brings a number, a request without one is not approved."),
    ("Ben did not file on time. Every on-time filing was accepted. What follows about Ben?", "The premises do not say Ben's filing was accepted", ["Ben's filing was accepted", "Ben filed on time", "Nobody filed on time"], "The acceptance rule covers on-time filings. Ben is outside that group."),
    ("“The room is full, so the next session should be online.” The conclusion assumes that:", "An online session can take the people who do not fit in the room", ["A full room is illegal", "Online sessions are always shorter", "The room should be locked permanently"], "Moving online helps only if it actually seats the overflow."),
    ("“Install a queue display because visitors cannot tell when they will be called.” This assumes that:", "A display would show the call order visitors cannot now see", ["Visitors should not be called", "Displays replace the need for a queue", "The office has no visitors"], "The display is useful only if it gives the missing information."),
    ("“Publish a checklist to reduce incomplete applications.” The strongest supporting evidence would be:", "Incomplete applications that are missing items the checklist names", ["A checklist printed in a larger font only", "Fewer visitors in the building", "A new office logo"], "The evidence has to link the missing items to what the checklist would catch."),
    ("Attacking the speaker instead of the claim is which flaw?", "A personal attack in place of a reason", ["A careful definition", "A counted sample", "A stated exception"], "The flaw replaces a reason about the claim with a remark about the person."),
    ("Accidents fell after the new paint. Saying the paint caused the drop may ignore what?", "Another change that happened at the same time", ["The fact that the paint is visible", "The definition of a road", "That counts can be written down"], "A before-and-after drop can have more than one cause."),
    ("Which claim is a value judgment rather than a count?", "The office ought to open on Saturdays.", ["The office opened on four Saturdays.", "Forty people were in line.", "The window handled 30 forms."], "Ought states a judgment. The other sentences report counts."),
    ("A survey says 70 percent of respondents favor flex time. The strongest caution is:", "The respondents may not match the whole staff", ["70 percent is a number", "Surveys use words", "Flex time is a schedule"], "A survey result depends on who was asked."),
    ("“Program X caused the score rise.” The weakest support would be:", "The score rose in a year when Program X did not run", ["The score rose in the sections that used Program X and not in the others", "The rise followed the program and other changes were held still", "The same rise appeared when Program X was tried again"], "A rise without the program undercuts the claim that the program caused it."),
    ("Which assumption is needed for “Cameras will reduce theft in this stockroom”?", "Theft in this stockroom is the kind a camera would deter or record", ["Cameras are expensive", "The stockroom has a door", "Theft never happens at night"], "If the thefts would be unchanged by a camera, the proposal fails."),
    ("Circular reasoning happens when:", "The claim and the reason are the same statement", ["A sample is counted twice by mistake", "A definition is given before an example", "Two different counts are compared"], "The argument does not move past repeating the claim."),
    ("Which is the best counterexample to “Every government website is always online”?", "One agency website was offline on Tuesday", ["A private shop has a website", "Some websites use https", "Tuesday is a weekday"], "One offline government site is enough to defeat every and always."),
    ("Waiting time fell after a new queue. A cautious conclusion is:", "The new queue is one change that came before a shorter wait", ["The queue is the only possible cause", "Waiting time will never rise again", "Every office now has the same wait"], "The timing supports a lead, not a proof that nothing else mattered."),
    ("“Repeat the training because errors rose after six months.” This assumes that:", "The rise in errors is tied to skill that the training can refresh", ["Errors should be ignored", "Six months is a holiday", "Training caused the errors"], "Repeating training helps only if the errors come from a skill the training covers."),
    ("Which is a necessary assumption for “A help desk will cut the questions about where to file”?", "People ask because they cannot find the filing place, and the desk would answer that", ["A help desk needs chairs", "Questions are always hostile", "Filing should stop"], "The desk has to be able to answer the question the visitors are actually asking."),
    ("If all clerks are staff, and some staff are drivers, which must be true when at least one clerk exists?", "At least one clerk is staff", ["At least one clerk is a driver", "No clerk is staff", "Every driver is a clerk"], "The first premise already puts every clerk inside staff. It does not put any clerk among the drivers."),
    ("Only badge holders may enter the archive. Nina entered the archive. What follows?", "Nina is a badge holder", ["Nina has no badge", "The archive was closed", "Every visitor is named Nina"], "Entry was limited to badge holders, and Nina entered, so she holds a badge."),
]


def build_from_bank(old: dict, bank: list[tuple], index: int) -> dict:
    stem, correct, wrongs, why = bank[index]
    options, key = pack(correct, wrongs, old["id"])
    return item(old, stem, options, key, explain(options[key], why, [option for i, option in enumerate(options) if i != key]))


def build_symbolic(old: dict, index: int) -> dict:
    qid = old["id"]
    kind = index % 9
    tag = ("north desk", "south desk", "east desk", "west desk")[index // 9]
    if kind == 0:
        groups = (("badge holder", "staff member", "visitor"), ("driver", "employee", "contractor"), ("coder", "analyst", "auditor"))
        a, b, c = groups[index // 9 % 3]
        stem = f"At the {tag}: if every {a} is a {b}, and no {b} is a {c}, which must be true?"
        correct = f"No {a} is a {c}"
        wrongs = [f"Every {c} is a {a}", f"Some {c}s are {a}s", f"Every {b} is a {c}"]
        why = f"Every {a} is inside the {b} group, and that group does not overlap the {c} group."
    elif kind == 1:
        words = ("PLAN", "MATH", "CODE", "FIRE")
        word = words[index // 9 % 4]
        correct = "".join(chr(ord(ch) + 1) for ch in word)
        wrongs = [word, word[::-1], correct[:-1] + "A"]
        stem = f"Each letter moves one place forward. What does {word} become?"
        why = "Each letter moves to the next letter in the alphabet."
    elif kind == 2:
        left = 8 + index
        mid = 4
        right = 3
        answer = left + mid - right
        stem = f"If the triangle means plus and the square means minus, what is {left} triangle {mid} square {right}?"
        correct = str(answer)
        wrongs = [str(left + mid + right), str(left - mid - right), str(left * mid - right)]
        why = f"{left} plus {mid} is {left + mid}, and {left + mid} minus {right} is {answer}."
    elif kind == 3:
        left = 3 + (index % 4)
        right = 5 + (index % 3)
        answer = left + right * left
        stem = f"Using ordinary order, a triangle is {left} and a square is {right}. What is triangle plus square multiplied by triangle?"
        correct = str(answer)
        wrongs = [str((left + right) * left), str(left * right), str(left + right)]
        why = f"Multiply first: {right} times {left} is {right * left}. Then add {left} to get {answer}."
    elif kind == 4:
        dividend = 18 + index
        # keep divisible by 3
        dividend = dividend - (dividend % 3)
        divisor = 3
        add = 4 + (index % 3)
        answer = dividend // divisor + add
        stem = f"The symbol @ means divided by, and # means plus. What is {dividend} @ {divisor} # {add}?"
        correct = str(answer)
        wrongs = [str(dividend // divisor), str(answer + divisor), str(dividend // (divisor + add) if divisor + add else answer + 1)]
        why = f"{dividend} divided by {divisor} is {dividend // divisor}. Plus {add} is {answer}."
    elif kind == 5:
        first = "square" if index % 2 == 0 else "circle"
        second = "circle" if first == "square" else "square"
        stem = f"On the {tag}, a row repeats {first}, {second}, {first}, {second}, {first}. What comes next?"
        correct = second.capitalize()
        wrongs = [first.capitalize(), "Triangle", "Star"]
        why = f"The shapes take turns. After a {first}, the next shape is a {second}."
    elif kind == 6:
        rows = (("W", "X", "Y", "Z"), ("A", "B", "C", "D"), ("P", "Q", "R", "S"), ("K", "L", "M", "N"))
        row = rows[index % 4]
        correct = ", ".join((row[1], row[2], row[3], row[0]))
        wrongs = [", ".join(reversed(row)), ", ".join(row), ", ".join((row[2], row[3], row[0], row[1]))]
        stem = f"The row {', '.join(row)} moves one place left, and the first symbol goes to the end. What is the new row?"
        why = f"The left shift is {correct}."
    elif kind == 7:
        stem = f"Which figure, unlike a general four-sided shape, must have four right angles? Item {index + 1} uses the ordinary definition."
        correct = "A rectangle"
        wrongs = ["A general triangle", "A pentagon", "An open curve"]
        why = "A rectangle has four right angles. A general quadrilateral does not have to."
    else:
        series = (
            ("4, 9, 16, 20", "20", ["4", "9", "16"], "4, 9, and 16 are squares. 20 is not."),
            ("8, 27, 64, 30", "30", ["8", "27", "64"], "8, 27, and 64 are cubes. 30 is not."),
            ("2, 3, 5, 9", "9", ["2", "3", "5"], "2, 3, and 5 are prime. 9 is not."),
            ("6, 10, 15, 16", "16", ["6", "10", "15"], "6, 10, and 15 are triangular numbers in that run. 16 is not."),
        )
        stem_bits, correct, wrongs, why = series[index % 4]
        stem = f"Which number does not belong with the others: {stem_bits}?"
    options, key = pack(correct, wrongs, qid)
    return item(old, stem, options, key, explain(options[key], why, [option for i, option in enumerate(options) if i != key]))


def build_data(old: dict, index: int) -> dict:
    qid = old["id"]
    places = (
        "San Roque", "Poblacion", "Mabini", "Rizal", "Luna", "Bonifacio", "Del Pilar",
        "Burgos", "Jacinto", "Silang", "Gomez", "Aquino", "Magsaysay", "Quezon",
        "Osmena", "Roxas", "Laurel", "Quirino", "Magsaysay North", "Magsaysay South",
        "San Isidro", "San Jose", "Santa Cruz", "Santa Maria", "Santo Nino",
    )
    place = places[index]
    kind = index % 12
    shift = index // 12
    if kind == 0:
        a, b = 30 + shift * 15, 45 + shift * 15
        total = a + b
        share = b * 100 // total
        if b * 100 % total != 0:
            a, b, share, total = 40, 60, 60, 100
        stem = f"In {place}, Office A issued {a} permits and Office B issued {b}. What percent of the combined total came from Office B?"
        correct = f"{share} percent"
        wrongs = [f"{a} permits", f"{b} permits", f"{total} permits"]
        why = f"{b} divided by {total} is {share} percent."
    elif kind == 1:
        base = 60 + shift * 6
        scores = (base, base + 6, base + 12)
        mean = sum(scores) // 3
        stem = f"In {place}, the scores are {scores[0]}, {scores[1]}, and {scores[2]}. What is the mean?"
        correct = str(mean)
        wrongs = [str(scores[0]), str(sum(scores)), str(mean + 5)]
        why = f"The sum is {sum(scores)}. Divided by 3, the mean is {mean}."
    elif kind == 2:
        whole, pct = 200 + shift * 40, 25
        count = whole * pct // 100
        stem = f"In {place}, {pct} percent of {whole} complaints are about delays. How many complaints are about delays?"
        correct = str(count)
        wrongs = [str(pct), str(whole // 10), str(count + 20)]
        why = f"{pct} percent of {whole} is {count}."
    elif kind == 3:
        old_n = 120 + shift * 40
        new_n = old_n + old_n // 4
        pct = (new_n - old_n) * 100 // old_n
        stem = f"In {place}, output rose from {old_n} units to {new_n} units. What is the percent increase?"
        correct = f"{pct} percent"
        wrongs = [f"{new_n - old_n} percent", "50 percent", f"{pct + 10} percent"]
        why = f"The rise is {new_n - old_n}. Divided by {old_n}, that is {pct} percent."
    elif kind == 4:
        nums = [4 + shift, 11 + shift, 7 + shift, 9 + shift, 15 + shift]
        ordered = sorted(nums)
        median = ordered[len(ordered) // 2]
        stem = f"What is the median of these {place} counts: {', '.join(str(n) for n in nums)}?"
        correct = str(median)
        wrongs = [str(ordered[0]), str(ordered[-1]), str(median + 2)]
        why = f"In order the list is {', '.join(str(n) for n in ordered)}. The middle value is {median}."
    elif kind == 5:
        errors, files = 4 + shift, 20
        if shift:
            errors, files = 6, 24
        rate = errors * 100 // files
        stem = f"In {place}, {errors} of {files} checked files had an error. What is the error rate?"
        correct = f"{rate} percent"
        wrongs = [f"{errors} percent", f"{files + errors} percent", f"{100 - rate} percent"]
        why = f"{errors} divided by {files} is {rate} percent."
    elif kind == 6:
        female, male = 60 + shift * 10, 40
        total = female + male
        pct = female * 100 // total
        if female * 100 % total != 0:
            female, male, total, pct = 60, 40, 100, 60
        stem = f"The {place} roster has {male} men and {female} women. What percent of the roster is women?"
        correct = f"{pct} percent"
        wrongs = [f"{male} people", f"{female} people", f"{total} percent"]
        why = f"{female} divided by {total} is {pct} percent."
    elif kind == 7:
        y1 = 180 + shift * 20
        y2 = y1 + 45
        stem = f"{place} enrollment was {y1} in year one and {y2} in year two. What is the absolute increase?"
        correct = str(y2 - y1)
        wrongs = [str(y1), str(y2), str(y2 + y1)]
        why = f"{y2} minus {y1} is {y2 - y1}."
    elif kind == 8:
        budget = 80000 + shift * 20000
        supplies, training = 20, 15
        both = budget * (supplies + training) // 100
        stem = f"The {place} budget of {budget:,} pesos assigns {supplies} percent to supplies and {training} percent to training. How much is assigned to those two together?"
        correct = f"{both:,} pesos"
        wrongs = [f"{budget * supplies // 100:,} pesos", f"{budget * training // 100:,} pesos", f"{budget - both:,} pesos"]
        why = f"{supplies + training} percent of {budget:,} is {both:,} pesos."
    elif kind == 9:
        done, total = 21, 28
        if shift:
            done, total = 18, 24
        rate = done * 100 // total
        stem = f"A {place} team finished {done} of {total} reviews. What percent are finished?"
        correct = f"{rate} percent"
        wrongs = [f"{100 - rate} percent", f"{done} percent", f"{total} percent"]
        why = f"{done} divided by {total} is {rate} percent."
    elif kind == 10:
        start = 80 + shift * 40
        end = start + start // 4
        stem = f"{place} output rises from {start} items to {end} items. The increase is what fraction of the original?"
        correct = "1/4"
        wrongs = ["1/5", "4/5", "1/2"]
        why = f"The increase is {end - start}. {end - start} over {start} is 1/4."
    else:
        received = 50 + shift * 10
        approved = 32 + shift * 6
        rejected = 8 + shift * 2
        pending = received - approved - rejected
        stem = f"The {place} window receives {received} applications, approves {approved}, and rejects {rejected}. How many are still pending?"
        correct = str(pending)
        wrongs = [str(approved - rejected), str(received - approved), str(rejected)]
        why = f"{received} minus {approved} minus {rejected} is {pending}."
    options, key = pack(correct, wrongs, qid)
    return item(old, stem, options, key, explain(options[key], why, [option for i, option in enumerate(options) if i != key]))


def _fmt_names(seq: list[tuple[str, str]]) -> str:
    return "; ".join(f"{last}, {first}" for last, first in seq)


def build_filing_order(old: dict, index: int) -> dict:
    qid = old["id"]
    kind = index % 6
    batch = index // 6
    if kind == 0:
        families = (
            ("Ramos", ("Aldo", "Ben", "Cora", "Dina")),
            ("Cruz", ("Ana", "Bea", "Carlo", "Dina")),
            ("Flores", ("Isko", "Liza", "Marco", "Nena")),
            ("Garcia", ("Ariel", "Bela", "Cesar", "Dante")),
        )
        surname, givens = families[batch % len(families)]
        names = [(surname, given) for given in givens]
        ordered = sorted(names, key=lambda pair: (pair[0].lower(), pair[1].lower()))
        correct = _fmt_names(ordered)
        wrongs = [
            _fmt_names(list(reversed(ordered))),
            _fmt_names([ordered[1], ordered[0], ordered[2], ordered[3]]),
            _fmt_names([ordered[0], ordered[1], ordered[3], ordered[2]]),
        ]
        stem = f"Which order files these {surname} names from first to last?"
        why = f"The surname is the same, so the given names decide the order: {_fmt_names(ordered)}."
    elif kind == 1:
        sets = (
            ("Abad", "Abalos", "Aquino", "Arce"),
            ("Bajo", "Baluyot", "Bautista", "Bernardo"),
            ("Cabrera", "Calderon", "Castro", "Cruz"),
            ("Dalisay", "David", "De Jesus", "Domingo"),
        )
        surnames = sets[batch % len(sets)]
        ordered = sorted(surnames)
        correct = ordered[0]
        wrongs = ordered[1:]
        stem = f"Under ordinary alphabetic filing, which surname comes first: {', '.join(surnames)}?"
        why = f"{correct} comes before the other surnames."
    elif kind == 2:
        targets = (
            ("Santos", "Mira", "Lino", "Pia"),
            ("Reyes", "Nora", "Luis", "Omar"),
            ("Torres", "Rina", "Paolo", "Sara"),
            ("Villanueva", "Cora", "Ben", "Dina"),
        )
        surname, target, earlier, later = targets[batch % len(targets)]
        correct = f"{surname}, {earlier}"
        wrongs = [f"{surname}, {later}", f"Salazar, Ana", f"Santiago, Ana"]
        stem = f"Which file comes immediately before “{surname}, {target}”?"
        why = f"Within {surname}, {earlier} comes before {target}. The other names do not."
    elif kind == 3:
        sets = ([8, 19, 104, 140], [7, 18, 102, 120], [6, 16, 101, 110], [9, 21, 108, 180])
        nums = sets[batch % len(sets)]
        ordered = sorted(nums)
        correct = ", ".join(f"{number:03d}" for number in ordered)
        wrongs = [
            ", ".join(f"{number:03d}" for number in reversed(ordered)),
            ", ".join(f"{number:03d}" for number in [ordered[0], ordered[2], ordered[1], ordered[3]]),
            ", ".join(f"{number:03d}" for number in [ordered[1], ordered[0], ordered[3], ordered[2]]),
        ]
        stem = f"Which numeric file order is ascending for {correct.replace(', ', ', ')} and the other rows?"
        stem = "Which numeric file order is ascending?"
        # Keep the stem unique by naming the set.
        stem = f"Which order is ascending: the set that starts with {ordered[0]:03d}?"
        why = f"As numbers, the order is {correct}."
    elif kind == 4:
        shift = batch
        dates = [date(2028, 1, 9 + shift), date(2028, 2, 14), date(2028, 3, 2), date(2028, 4, 11)]
        labels = [day.strftime("%d %b %Y") for day in dates]

        def show(seq: list[str]) -> str:
            return "; ".join(seq)

        correct = show(labels)
        wrongs = [show(list(reversed(labels))), show([labels[1], labels[0], labels[2], labels[3]]), show([labels[2], labels[1], labels[0], labels[3]])]
        stem = f"Which date order runs from earliest to latest, starting in January 2028 day {9 + shift}?"
        why = f"The earliest date comes first: {correct}."
    else:
        base = 200 + batch * 7
        reference = f"18-{base}"
        correct = f"18-{base + 1}"
        wrongs = [f"18-{base - 1}", f"18-{base - 100}", f"17-{base}"]
        stem = f"Which file number is filed immediately after {reference} in an ascending numeric file?"
        why = f"{correct} is the next number. The others come before {reference}."
    options, key = pack(correct, wrongs, qid)
    return item(old, stem, options, key, explain(options[key], why, [option for i, option in enumerate(options) if i != key]))


FILIPINO = {
    404: (
        "Piliin ang wastong salita: “_____ lumubog ang araw, umuwi ang mga mangingisda.”",
        "Nang",
        ["Ng", "Na ng", "Kung sa"],
        "Nang ang ginagamit dito bilang pangatnig na katumbas ng noong. Ang ng ay pananda ng layon o pagmamay-ari.",
        "Filipino",
    ),
    405: (
        "Alin sa mga ito ang wastong pangungusap?",
        "Maingat na sinuri ng kawani ang listahan.",
        [
            "Maingat nang sinuri ng kawani ang listahan.",
            "Maingat ng sinuri ang ng kawani listahan.",
            "Sinuri maingat na ang listahan kawani.",
        ],
        "Iniuugnay ang pang-abay na maingat sa pandiwa sa pamamagitan ng na.",
        "Filipino",
    ),
    406: (
        "Piliin ang wastong utos: “_____ ninyo ang pinto.”",
        "Isara",
        ["Isarado", "Saradohin", "Magsarado"],
        "Ang utos na tumutukoy sa pinto ay isara. Hindi karaniwang anyo ang isarado o saradohin.",
        "Filipino",
    ),
    407: (
        "Alin ang tamang baybay ng salitang mula sa danas?",
        "Karanasan",
        ["Karanassan", "Karanasaan", "Karranasan"],
        "Ang karanasan ay may isang r at isang s.",
        "Filipino",
    ),
    408: (
        "Alin ang wastong gamit ng rin pagkatapos ng patinig?",
        "Mabuti rin ang tugon.",
        ["Mabuti din ang tugon.", "Mabuti rin din ang tugon.", "Mabuti nang rin ang tugon."],
        "Patinig ang huling tunog ng mabuti, kaya rin ang kasunod, hindi din.",
        "Filipino",
    ),
    409: (
        "Alin ang halimbawa ng karaniwang ayos?",
        "Naghain ng ulat ang kawani.",
        ["Ang kawani ay naghain ng ulat.", "Ng ulat ang naghain kawani.", "Ulat ang kawani naghain ng."],
        "Sa karaniwang ayos, nauuna ang panaguri at sumusunod ang simuno.",
        "Filipino",
    ),
    410: (
        "Alin ang nasa di-karaniwang ayos?",
        "Ang kawani ay naghain ng ulat.",
        ["Naghain ng ulat ang kawani.", "Naghain ang ulat ng kawani.", "Kawani ulat ay naghain ang."],
        "Sa di-karaniwang ayos, nauuna ang simuno at ginagamit ang ay.",
        "Filipino",
    ),
    411: (
        "Basahin: “Maaga silang nagtipon upang maihanda ang mga papeles.” Ano ang layunin ng maagang pagtitipon?",
        "Maihanda ang mga papeles",
        ["Maantala ang pulong", "Isara ang tanggapan", "Palitan ang gusali"],
        "Ang upang ay nagsasaad ng layunin. Ang binanggit na layunin ay ang paghahanda ng mga papeles.",
        "Filipino",
    ),
}


def build_filipino(old: dict) -> dict:
    stem, correct, wrongs, why, language = FILIPINO[old["id"]]
    options, key = pack(correct, wrongs, old["id"])
    wrong_text = ", ".join(f"“{option}”" for option in options if option != options[key])
    why_line = why.strip()
    if not why_line.endswith((".", "?", "!")):
        why_line += "."
    choice = options[key].strip()
    quoted = f"“{choice}”" if choice.endswith((".", "?", "!")) else f"“{choice}.”"
    explanation = f"{why_line} Ang tugmang sagot ay {quoted} {wrong_text} ay hindi tumutugma sa tuntunin."
    return item(old, stem, options, key, explanation, language)


def load_fact_stems(path: Path) -> dict[int, str]:
    stems: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        qid, stem = line.split("\t", 1)
        stems[int(qid)] = stem.strip()
    return stems


def build_fact(old: dict, stems: dict[int, str]) -> dict:
    options = json.loads(old["options"]) if isinstance(old["options"], str) else list(old["options"])
    if len(options) != 4:
        raise ValueError(old["id"])
    correct = options[old["correct_option"]]
    shuffled, key = pack(correct, [option for i, option in enumerate(options) if i != old["correct_option"]], old["id"])
    raw = old["explanation"].split(" Therefore,")[0].split(" The other choices")[0].strip()
    why = raw if raw else "The choice states the rule this item asks for."
    stem = stems[old["id"]]
    return item(old, stem, shuffled, key, explain(shuffled[key], why, [option for i, option in enumerate(shuffled) if i != key]))
