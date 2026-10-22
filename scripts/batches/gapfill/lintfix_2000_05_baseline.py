"""Schema completion for baseline items included in the gap-fill-2000-05 lint fixes.
Baseline items converted from the Oct 17 export lack terms, shortcut, distractor codes and why_wrong; a lint fix must make them full-spec.
COMPLETE[id] = (terms, shortcut, {wrong_option_text: (code, why)}); STEM[id] = clearer stem where the old stem near-duplicated another item."""
T_SENT = "An independent clause has a subject and verb and can stand alone. A dependent clause (starting with because, although, when...) cannot."
T_PARA = "Unity = every sentence supports one main idea. Coherence = ideas follow a logical order with clear transitions."
T_RC = "The right answer is stated in the passage or follows directly from it, without adding claims the text does not make."
S_RC = "Underline the key claim in the passage, then reject any choice that reverses it, overstates it, or talks about something else."
STEM = {
 "CIVIO-BASELINE-0023": "Which of these sentences joins two independent clauses with a comma and a coordinating conjunction?",
 "CIVIO-BASELINE-0114": "Which sentence pairs a dependent clause with an independent clause (a complex sentence)?",
 "CIVIO-BASELINE-0117": "Which word group cannot stand alone as a sentence because it has no main clause?",
 "CIVIO-BASELINE-0453": "In a paragraph, which connecting word tells the reader that a result or consequence follows?",
}
COMPLETE = {
 "CIVIO-BASELINE-0022": (T_SENT, "Count the clauses that can stand alone: a simple sentence has exactly one.", {
   "Two dependent clauses only": ("VEN-FRAGMENT", "Two dependent clauses with no main clause make a fragment, not a sentence."),
   "No verb": ("VEN-FRAGMENT", "Every sentence needs a verb; a word group without one is a fragment."),
   "Only a phrase": ("VEN-FRAGMENT", "A phrase has no subject-verb pair, so it is not a sentence at all.")}),
 "CIVIO-BASELINE-0023": (T_SENT, "Look for two complete thoughts joined by \", and\", \", but\" or \", so\".", {
   "Studying hard for the exam.": ("VEN-FRAGMENT", "This -ing phrase has no subject or main verb; it is a fragment."),
   "When I arrived.": ("VEN-FRAGMENT", "\"When\" makes this a dependent clause; alone it is a fragment."),
   "Because it rained.": ("VEN-FRAGMENT", "\"Because\" makes this a dependent clause; alone it is a fragment.")}),
 "CIVIO-BASELINE-0113": (T_SENT, "Compound = two or more independent clauses joined by a conjunction or a semicolon.", {
   "One independent clause with no other clause": ("VEN-FORM", "One independent clause alone is a simple sentence, not a compound one."),
   "Only dependent clauses with no main clause": ("VEN-FRAGMENT", "Dependent clauses alone form a fragment, not any kind of sentence."),
   "A heading or title that has no verb in it": ("VEN-FRAGMENT", "A title without a verb is not a sentence.")}),
 "CIVIO-BASELINE-0114": (T_SENT, "Find a clause that starts with although, because, when or if, joined to a full sentence.", {
   "The clerk filed the papers on Monday and left the office at noon.": ("VEN-FORM", "This is a simple sentence with a compound verb (filed ... and left); it has no dependent clause."),
   "The clerk filed the papers, and the manager signed them.": ("VEN-FORM", "Two independent clauses joined by \"and\" make a compound sentence, not a complex one."),
   "File the papers. Sign the form. Archive the folder today.": ("VEN-FORM", "These are three separate simple commands, not one complex sentence.")}),
 "CIVIO-BASELINE-0116": (T_SENT, "A run-on jams two sentences together; fix it with a period, a semicolon, or a comma plus a conjunction.", {
   "Adding more unrelated clauses without punctuation": ("VEN-RUN-ON", "Adding clauses without punctuation makes the run-on worse."),
   "Removing every verb so that no clause is left in the sentence": ("VEN-FRAGMENT", "Removing verbs destroys the clauses and leaves fragments."),
   "Breaking it into fragments that cannot stand alone as sentences": ("VEN-FRAGMENT", "Fragments are a different error; each part must still be a complete sentence.")}),
 "CIVIO-BASELINE-0117": (T_SENT, "Cover the first word: if \"because\" or \"when\" leaves no complete thought, it is a fragment.", {
   "The training starts at nine.": ("VEN-FORM", "This has a subject and verb and stands alone; it is a complete sentence."),
   "Please submit your forms today.": ("VEN-FORM", "A command has an understood subject (you); it is a complete sentence."),
   "Who will lead the briefing?": ("VEN-FORM", "A question with a subject and verb is a complete sentence.")}),
 "CIVIO-BASELINE-0242": (T_SENT, "Two full sentences need a period, a semicolon, or a comma plus and/but/so between them.", {
   "The forms arrived, they were incomplete.": ("VEN-RUN-ON", "A comma alone between two independent clauses is a comma splice."),
   "The forms arrived they were incomplete.": ("VEN-RUN-ON", "Two independent clauses with no punctuation make a fused run-on."),
   "The forms arrived, and incomplete.": ("VEN-FORM", "\"and incomplete\" has no verb; the second half is not a clause, so the sentence is ungrammatical.")}),
 "CIVIO-BASELINE-0024": (T_PARA, "Ask: which sentence could serve as the paragraph's title in sentence form?", {
   "Lists unrelated facts that do not share a point": ("PO-OPENER-MISPLACED", "Unrelated facts break unity; a topic sentence gives one main idea."),
   "Appears only at the end of every essay": ("PO-OPENER-MISPLACED", "A topic sentence usually opens a paragraph; it is not limited to essay endings."),
   "Replaces the concluding sentence of the paragraph": ("PO-TRANSITION-IGNORED", "The concluding sentence has a different job: it wraps up the idea the topic sentence introduced.")}),
 "CIVIO-BASELINE-0025": (T_PARA, "Coherent = each sentence connects clearly to the one before it.", {
   "Randomly arranged": ("RC-OPPOSITE", "Random order is the opposite of coherence."),
   "All one-word answers": ("LOG-IRRELEVANT", "Sentence length has nothing to do with coherence."),
   "Never supported": ("LOG-IRRELEVANT", "Support concerns development, and unsupported ideas weaken a paragraph rather than define coherence.")}),
 "CIVIO-BASELINE-0119": (T_PARA, "The topic sentence names the idea the rest of the paragraph explains.", {
   "Hides the main idea until the last footnote": ("RC-OPPOSITE", "A topic sentence states the main idea openly, not hidden in a footnote."),
   "Lists only unrelated examples": ("LOG-IRRELEVANT", "Unrelated examples break unity and do not state a main idea."),
   "Must be a question always": ("RC-EXTREME", "A topic sentence may be a statement or a question; \"always\" is too strong.")}),
 "CIVIO-BASELINE-0120": (T_PARA, "Coherence comes from order plus signposts such as first, however and as a result.", {
   "Random jumps between unrelated topics": ("RC-OPPOSITE", "Random jumps destroy coherence."),
   "Repeating the same sentence ten times": ("LOG-IRRELEVANT", "Repetition adds nothing and does not connect ideas."),
   "Omitting all examples": ("LOG-IRRELEVANT", "Removing examples weakens support; it does not improve coherence.")}),
 "CIVIO-BASELINE-0122": (T_PARA, "A concluding sentence looks back at the main idea; it does not open a new one.", {
   "Introduces an entirely new topic without link": ("PO-TRANSITION-IGNORED", "A new, unlinked topic at the end breaks unity."),
   "Deletes the topic sentence retroactively": ("LOG-IRRELEVANT", "A sentence cannot delete another sentence; this is meaningless."),
   "Must apologize for the content": ("LOG-IRRELEVANT", "Apologizing is not the function of a concluding sentence.")}),
 "CIVIO-BASELINE-0123": (T_PARA, "Unity test: does every sentence support the one main idea?", {
   "Each sentence discusses a different subject": ("RC-OPPOSITE", "Different subjects in each sentence is the opposite of unity."),
   "No examples are allowed": ("LOG-IRRELEVANT", "Examples are allowed and usually support unity."),
   "Only questions are used": ("LOG-IRRELEVANT", "Sentence type has nothing to do with unity.")}),
 "CIVIO-BASELINE-0124": (T_PARA, "Transitions are signposts: however = contrast, therefore = result.", {
   "The font size used in the text": ("LOG-IRRELEVANT", "Font size is formatting, not a relationship between ideas."),
   "The width of the page margins": ("LOG-IRRELEVANT", "Margins are layout, not meaning."),
   "How loudly the speaker talks": ("LOG-IRRELEVANT", "Volume is not something a written transition shows.")}),
 "CIVIO-BASELINE-0244": (T_PARA, "General before specific: give the background, then the details that depend on it.", {
   "Unrelated jokes that do not connect to the topic": ("LOG-IRRELEVANT", "Unrelated material breaks unity wherever it is placed."),
   "Deleting the topic sentence from the paragraph": ("LOG-IRRELEVANT", "Deleting is not something you place in an order."),
   "Rules about the punctuation at the end of sentences": ("LOG-IRRELEVANT", "Punctuation rules are not paragraph content.")}),
 "CIVIO-BASELINE-0245": (T_PARA, "first, then, finally = sequence in time.", {
   "Spatial description only": ("PO-TRANSITION-IGNORED", "Spatial order uses words like above, beside and behind, not first/then/finally."),
   "Cause without sequence": ("PO-TRANSITION-IGNORED", "Cause-effect uses because, so and as a result; these markers show sequence."),
   "Font changes": ("LOG-IRRELEVANT", "Markers are words, not formatting.")}),
 "CIVIO-BASELINE-0449": (T_PARA, "A topic sentence states a claim the rest of the paragraph can support.", {
   "The permit office building has three large windows.": ("RC-TOO-NARROW", "A detail about the building does not state the paragraph's idea about faster processing."),
   "Yesterday was humid, and many applicants came late.": ("LOG-IRRELEVANT", "Weather and lateness are not about faster permit processing."),
   "Some of the permit forms are printed on blue paper.": ("RC-TOO-NARROW", "Form color is a minor detail, not a main idea.")}),
 "CIVIO-BASELINE-0450": (T_PARA, "Follow the real order of the task: fill in, attach, check, submit.", {
   "Submit first, then decide which form is needed.": ("LOG-ORDER-SWAP", "Submitting before choosing the form reverses the process."),
   "Archive the form before writing on it.": ("LOG-ORDER-SWAP", "Archiving comes after a form is completed, not before."),
   "Choose a filing shelf before reading the instructions.": ("PO-OPENER-MISPLACED", "The process starts with the form itself, not with storage.")}),
 "CIVIO-BASELINE-0451": (T_PARA, "Unity: remove or move the sentence that does not support the main idea.", {
   "Add three more parking sentences": ("RC-OPPOSITE", "More parking sentences make the paragraph less unified."),
   "Delete the document-security details": ("RC-OPPOSITE", "The security sentences are the main idea; deleting them removes the point."),
   "Change every verb to past tense": ("LOG-IRRELEVANT", "Tense does not affect unity.")}),
 "CIVIO-BASELINE-0452": (T_PARA, "however = contrast; similarly = likeness; therefore = result; for example = illustration.", {
   "Similarly": ("PO-TRANSITION-IGNORED", "\"Similarly\" shows likeness, not contrast."),
   "Therefore": ("PO-TRANSITION-IGNORED", "\"Therefore\" shows a result, not contrast."),
   "For example": ("PO-TRANSITION-IGNORED", "\"For example\" introduces an illustration, not contrast.")}),
 "CIVIO-BASELINE-0453": (T_PARA, "therefore = result; meanwhile = time; for instance = example; likewise = likeness.", {
   "Meanwhile": ("PO-TRANSITION-IGNORED", "\"Meanwhile\" shows events at the same time, not a result."),
   "For instance": ("PO-TRANSITION-IGNORED", "\"For instance\" introduces an example, not a result."),
   "Likewise": ("PO-TRANSITION-IGNORED", "\"Likewise\" shows similarity, not a result.")}),
 "CIVIO-BASELINE-0534": (T_PARA, "A concluding sentence returns to the topic and sums it up.", {
   "The office has a green door near the main lobby.": ("LOG-IRRELEVANT", "A detail about the door is unrelated to password practices."),
   "Some of the office keyboards are wireless models.": ("RC-TOO-NARROW", "Keyboards are a side detail, not a conclusion about passwords."),
   "Yesterday had light traffic on the road to work.": ("LOG-IRRELEVANT", "Traffic is unrelated to the paragraph's topic.")}),
 "CIVIO-BASELINE-0026": (T_RC, "Ask what the whole passage is mostly about, not about one detail.", {
   "How many commas are used?": ("LOG-IRRELEVANT", "Punctuation counts do not reveal the main idea."),
   "Who printed the page?": ("LOG-IRRELEVANT", "The printer of the page is unrelated to the passage's message."),
   "What font size is used?": ("LOG-IRRELEVANT", "Font size is formatting, not meaning.")}),
 "CIVIO-BASELINE-0027": (T_RC, "An inference goes one step beyond the text but must be backed by it.", {
   "Copied word for word from the passage": ("RC-SUPPORTED-NOT-ASKED", "Copied text is a stated detail, not an inference."),
   "Always stated directly in the title": ("RC-NOT-IN-TEXT", "An inference is not stated directly anywhere, including the title."),
   "Impossible to support with the text": ("RC-OPPOSITE", "A valid inference must be supported by the text.")}),
 "CIVIO-BASELINE-0125": (T_RC, S_RC, {
   "Prevents all corruption automatically and completely": ("RC-EXTREME", "The passage only says citizens can examine spending; \"all corruption\" overstates it."),
   "Replaces the need for citizens to vote in elections": ("RC-NOT-IN-TEXT", "Elections are not mentioned."),
   "Applies only to the records of private banks": ("RC-OPPOSITE", "The passage is about government spending, not private banks.")}),
 "CIVIO-BASELINE-0126": (T_RC, S_RC, {
   "Training is useless in all cases and should stop": ("RC-EXTREME", "The passage says gains are short-lived without coaching, not that training is useless."),
   "Coaching can fully replace all formal training": ("RC-NOT-IN-TEXT", "Nothing suggests coaching replaces training; it follows training."),
   "Gains from training never occur at all": ("RC-OPPOSITE", "The passage says gains occur but fade.")}),
 "CIVIO-BASELINE-0127": (T_RC, S_RC, {
   "Never used by anyone during actual evacuations": ("RC-NOT-IN-TEXT", "Nothing says the maps are unused; yearly updates suggest the opposite."),
   "Illegal to post in barangay halls and public places": ("RC-NOT-IN-TEXT", "Legality is not mentioned."),
   "Only decorative pictures that are not meant to guide anyone": ("RC-OPPOSITE", "Evacuation maps that are updated yearly are meant to be used.")}),
 "CIVIO-BASELINE-0128": (T_RC, S_RC, {
   "Hiring by personal connections always builds public trust": ("RC-OPPOSITE", "The passage credits merit, not connections, with building trust."),
   "Government offices should ignore merit when they hire staff": ("RC-OPPOSITE", "This reverses the passage's point."),
   "Public trust has nothing to do with how officials are hired": ("RC-OPPOSITE", "The passage links hiring and trust directly.")}),
 "CIVIO-BASELINE-0129": (T_RC, S_RC, {
   "The high cost of printer ink in government offices": ("RC-NOT-IN-TEXT", "Printer ink is not mentioned."),
   "Too many service centers built in the downtown area": ("RC-NOT-IN-TEXT", "Service-center locations are not mentioned."),
   "Too many paper forms required for every service": ("RC-NOT-IN-TEXT", "The passage is about digital skills, not paper forms.")}),
 "CIVIO-BASELINE-0130": (T_RC, S_RC, {
   "Personal anecdotes vs. poems": ("RC-NOT-IN-TEXT", "Poetry is not mentioned; the contrast is data vs. anecdotes."),
   "Public policy vs. law dictionaries": ("RC-NOT-IN-TEXT", "Law dictionaries are not mentioned."),
   "Office servers vs. desktop computers": ("LOG-IRRELEVANT", "Computer hardware has nothing to do with the passage.")}),
 "CIVIO-BASELINE-0131": (T_RC, "Rules with \"unless\" or \"except\" have two parts; keep both.", {
   "Ignore the exception and apply the rule": ("RC-TOO-NARROW", "Ignoring the exception misreads the passage."),
   "Assume that no exceptions ever exist anywhere": ("RC-OPPOSITE", "The passage states an exception, so this contradicts it."),
   "Skip the passage and read only the title": ("LOG-IRRELEVANT", "Skipping the passage cannot capture the rule or the exception.")}),
 "CIVIO-BASELINE-0132": (T_RC, S_RC, {
   "Community feedback had no effect at all": ("RC-OPPOSITE", "The passage says feedback shortened the process."),
   "Permits were abolished after the feedback": ("RC-NOT-IN-TEXT", "Permits still exist; the process only got shorter."),
   "Two days were added to the permit process": ("RC-OPPOSITE", "Two days were removed, not added.")}),
 "CIVIO-BASELINE-0246": (T_RC, S_RC, {
   "Hide their performance expectations from the public": ("RC-OPPOSITE", "Publishing standards is the opposite of hiding them."),
   "Abolish all of their public services": ("RC-NOT-IN-TEXT", "Nothing suggests services are being abolished."),
   "Replace written laws with posters on the wall": ("RC-NOT-IN-TEXT", "Laws are not mentioned.")}),
 "CIVIO-BASELINE-0247": (T_RC, "Read the cause and the effect in order: ambiguous instructions (cause) → more errors (effect).", {
   "Errors → clearer instructions always": ("LOG-CONVERSE", "This reverses cause and effect and adds \"always\"."),
   "No relationship": ("RC-OPPOSITE", "The passage states a relationship."),
   "Ambiguity reduces errors": ("RC-OPPOSITE", "The passage says errors rise, not fall.")}),
 "CIVIO-BASELINE-0454": (T_RC, "List the conditions (complete form AND before noon); the answer must meet both.", {
   "A visitor with an incomplete form at 10:00 a.m.": ("LOG-MISSED-NEEDED", "Before noon, but the form is incomplete."),
   "A visitor with a complete form submitted at 1:00 p.m.": ("LOG-MISSED-NEEDED", "Complete, but submitted after noon."),
   "A person who never submits a form": ("LOG-MISSED-NEEDED", "No form was submitted, so neither condition is met.")}),
 "CIVIO-BASELINE-0455": (T_RC, "Without a comparison group, a before-and-after change suggests a possible cause, not proof.", {
   "Peer review alone caused every improvement": ("LOG-OVERSTRONG", "\"Alone\" and \"every\" claim proof the report does not give."),
   "Errors will never return": ("RC-EXTREME", "Nothing supports a permanent prediction."),
   "Other offices cannot use peer review": ("RC-NOT-IN-TEXT", "Other offices were not studied, so nothing is said about them.")}),
 "CIVIO-BASELINE-0456": (T_RC, "A balanced conclusion keeps both the benefit and the limitation.", {
   "Online forms have no possible benefit for the office": ("RC-OPPOSITE", "The paragraph says online forms save encoding time."),
   "Internet access is irrelevant to online forms": ("RC-OPPOSITE", "The paragraph says they require reliable internet."),
   "Paper forms are now always illegal to use": ("RC-NOT-IN-TEXT", "Legality of paper forms is not mentioned.")}),
 "CIVIO-BASELINE-0457": (T_RC, "Served ÷ total, then simplify: 30/40 = 3/4.", {
   "One-fourth": ("NUM-OTHER-SHARE", "One-fourth (10 of 40) is the share NOT served."),
   "Two-fifths": ("NUM-WRONG-BASE", "Two-fifths would be 16 of 40, which does not match 30 of 40."),
   "Four-thirds": ("NUM-WRONG-BASE", "Four-thirds divides total by served (40/30), which is upside down.")}),
 "CIVIO-BASELINE-0458": (T_RC, "\"Unless\" introduces the exception to a rule.", {
   "A quiet office": ("RC-NOT-IN-TEXT", "Office noise is not mentioned in the policy."),
   "A new printer": ("RC-NOT-IN-TEXT", "Printers are not mentioned in the policy."),
   "A staff meeting": ("RC-NOT-IN-TEXT", "Meetings are not mentioned in the policy.")}),
 "CIVIO-BASELINE-0535": (T_RC, "Check both conditions: complete AND received by Friday.", {
   "Incomplete and received Thursday": ("LOG-MISSED-NEEDED", "On time but incomplete."),
   "Complete and received Saturday": ("LOG-MISSED-NEEDED", "Complete but received after the Friday cutoff."),
   "Complete but never received": ("LOG-MISSED-NEEDED", "Never received, so it cannot enter the batch.")}),
}
