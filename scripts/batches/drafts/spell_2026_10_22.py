"""Spelling targets of the 22 Oct 2026 drafts (new bank-wide targets). Each: word, three real misspellings with error codes, meaning, sentence."""
D_, I_, X_, S_, Q_ = "SPL-DOUBLE", "SPL-IE-EI", "SPL-DROP", "SPL-SILENT", "SPL-SOUND"
SPELL = [  # word, [(misspelling, code)], meaning, context sentence with ____
 ("accumulate", [("accumalate", Q_), ("acumulate", D_), ("accummulate", D_)], "to gather or pile up over time", "Unpaid fines tend to ____ if no one sends a reminder."),
 ("acquittal", [("aquittal", S_), ("acquital", D_), ("acquitall", D_)], "a court's finding that the accused is not guilty", "The lawyer filed a copy of the ____ with the records section."),
 ("auxiliary", [("auxilary", X_), ("auxillary", Q_), ("auxiliery", Q_)], "giving extra help or support", "The ____ generator runs only during brownouts."),
 ("bankruptcy", [("bankrupcy", X_), ("bankruptsy", Q_), ("bankrupty", X_)], "the legal state of being unable to pay debts", "The supplier's ____ delayed three deliveries."),
 ("bureau", [("bureu", X_), ("beaureau", Q_), ("burau", X_)], "a government office or department", "Send the request to the ____ of local government finance."),
 ("commemorate", [("comemorate", D_), ("commemmorate", D_), ("commemerate", Q_)], "to honor the memory of an event or person", "The town will ____ its founding with a parade."),
 ("deductible", [("deductable", Q_), ("deductibel", Q_), ("deducktible", Q_)], "able to be subtracted, as from taxable income", "Only receipts for ____ expenses go in this folder."),
 ("discrepancy", [("discrepency", Q_), ("descrepancy", Q_), ("discrepansy", Q_)], "a difference between things that should match", "The auditor found a ____ between the ledger and the bank statement."),
 ("dissatisfied", [("disatisfied", D_), ("dissatisified", Q_), ("dissatisfyed", Q_)], "not pleased", "A ____ client may file a complaint at the action center."),
 ("embassy", [("embasy", D_), ("embessy", Q_), ("embassey", Q_)], "the office of an ambassador in a foreign country", "Visa forms are released at the ____ every Tuesday."),
 ("facsimile", [("facsimilie", Q_), ("facsimle", X_), ("fascimile", Q_)], "an exact copy, especially one sent by fax", "Attach a ____ of the signed contract."),
 ("feasible", [("feasable", Q_), ("feasibel", Q_), ("fesible", X_)], "possible and practical to do", "The engineers said the bridge repair is ____ within the budget."),
 ("indictment", [("inditment", S_), ("indictmant", Q_), ("endictment", Q_)], "a formal charge of a serious crime", "The clerk stamped the ____ before sending it to the court."),
 ("laboratory", [("labratory", X_), ("laboritory", Q_), ("laboratary", Q_)], "a room for scientific tests", "Water samples go to the provincial ____ for testing."),
 ("quarantine", [("quarentine", Q_), ("quarantene", Q_), ("quaranteen", Q_)], "a period of isolation to stop disease from spreading", "Arriving livestock must stay in ____ for seven days."),
 ("rehearsal", [("rehersal", X_), ("rehearsel", Q_), ("reharsal", X_)], "a practice session before a performance or event", "The emergency drill had a full ____ on Friday."),
 ("sponsor", [("sponser", Q_), ("sponsur", Q_), ("sponssor", D_)], "a person or group that supports an activity", "A local bank agreed to ____ the reading program."),
 ("supersede", [("supercede", Q_), ("superseed", Q_), ("supersade", Q_)], "to replace something older", "The new memo will ____ the circular issued last year."),
 ("susceptible", [("suseptible", S_), ("susceptable", Q_), ("succeptible", Q_)], "easily affected or harmed", "Older paper records are ____ to moisture damage."),
 ("unnecessary", [("unecessary", D_), ("unnecesary", D_), ("unneccessary", D_)], "not needed", "Please avoid ____ photocopies of the forms."),
]

# Set 2 targets (22 Oct 2026, afternoon): words not yet tested anywhere in the bank.
SPELL2 = [  # word, misspellings, meaning, sentence
 ("referral", [("referal", D_), ("refferal", D_), ("referrel", Q_)], "the act of sending someone to another office or person for help", "The health center gave the patient a ____ slip for the provincial hospital."),
 ("occasion", [("occassion", D_), ("ocasion", D_), ("ocassion", D_)], "a particular time or event", "The mayor's speech was prepared for the ____ of the town fiesta."),
 ("indispensable", [("indispensible", Q_), ("indespensable", Q_), ("indispensabel", Q_)], "absolutely necessary", "A complete logbook is ____ during an audit."),
 ("bulletin", [("bulletin", None), ("buletin", D_), ("bulliten", D_)], "a short official notice posted for the public", "The new office hours were posted on the ____ board."),
 ("gauge", [("guage", Q_), ("gage", X_), ("gauje", Q_)], "an instrument that measures, or to measure", "The guard checked the fuel ____ before the trip."),
 ("knowledgeable", [("knowledgable", X_), ("knowlegeable", X_), ("nowledgeable", S_)], "having much information about a subject", "Ask a ____ clerk about the requirements for a permit."),
 ("nuisance", [("nuisanse", Q_), ("nusance", X_), ("nuissance", D_)], "a person or thing that causes trouble or annoyance", "Loud karaoke after midnight is a public ____ under the ordinance."),
 ("pavilion", [("pavillion", D_), ("pavilon", X_), ("pavilyon", Q_)], "a large open structure used for events", "The job fair will be held at the provincial ____."),
 ("vicinity", [("vicinty", X_), ("vecinity", Q_), ("vicinnity", D_)], "the area near a place", "No vendors are allowed in the ____ of the school gate."),
 ("miniature", [("miniture", X_), ("minature", X_), ("miniatur", X_)], "a very small copy of something", "The architect showed a ____ model of the new city hall."),
 ("sergeant", [("sargeant", Q_), ("sergant", X_), ("seargent", Q_)], "a police or military officer above a corporal", "The desk ____ recorded the complaint in the blotter."),
 ("pastime", [("pasttime", D_), ("pastimme", D_), ("pass time", Q_)], "an activity done for enjoyment", "Reading became her favorite ____ after retirement."),
]
SPELL2[3] = ("bulletin", [("bulliten", Q_), ("buletin", D_), ("bullettin", D_)], SPELL2[3][2], SPELL2[3][3])
