# Grok Bot audit of chatgpt-batch-003, items 060051-060075 (R.A. 6713).
S, B, W, N = "GI-SIBLING-TERM", "GI-WRONG-BODY", "GI-SOUNDS-RIGHT", "GI-NEIGHBOR-NUMBER"
D = {
"060051": dict(sc="Sec. 4(A)(a): public interest over personal interest; government resources used efficiently, honestly and economically.", o={
  "o1": (None, S, "Simple living is about a modest personal lifestyle; using an agency vehicle for a holiday misuses government resources, which Sec. 4(A)(a) covers."),
  "o2": (None, S, "Political neutrality concerns serving people regardless of party."),
  "o3": (None, S, "Professionalism concerns excellence and skill in one's duties, not the use of government property.")}),
"060052": dict(sc="Sec. 4(A)(b): excellence, professionalism, intelligence and skill; not a dispenser of undue patronage.", o={
  "o1": (None, S, "Political neutrality concerns serving people regardless of party."),
  "o2": (None, S, "Simple living concerns a modest personal lifestyle."),
  "o4": (None, S, "Nationalism concerns loyalty to the Republic and promoting local goods.")}),
"060053": dict(sc="Sec. 4(A)(c): act with justness and sincerity; do not discriminate, especially against the poor and underprivileged.", o={
  "o1": ("Political neutrality", S, "Neutrality concerns party affiliation; not discriminating against the poor is justness and sincerity."),
  "o3": ("Simple living", S, "Simple living concerns a modest personal lifestyle."),
  "o4": ("Responsiveness to the public", S, "Responsiveness concerns prompt, courteous service; the rule against discriminating against the poor is under justness and sincerity.")}),
"060054": dict(sc="Sec. 4(A)(d): serve everyone without unfair discrimination, regardless of party affiliation or preference.", o={
  "o1": ("Commitment to democracy", S, "Commitment to democracy covers accountability and civilian supremacy; serving regardless of party is political neutrality."),
  "o2": (None, S, "Nationalism concerns loyalty to the Republic and promoting local goods."),
  "o4": ("Justness and sincerity", S, "Justness and sincerity bars discrimination, especially against the poor; party affiliation is the specific subject of political neutrality.")}),
"060055": dict(sc="Sec. 4(A)(e): prompt, courteous and adequate service; clear procedures; encourage suggestions; avoid red tape.", o={
  "o1": (None, S, "Simple living concerns a modest personal lifestyle."),
  "o2": ("Professionalism", S, "Professionalism concerns excellence and skill; clear instructions, courtesy and inviting suggestions are listed under responsiveness."),
  "o3": ("Political neutrality", S, "Political neutrality concerns serving people regardless of party.")}),
"060056": dict(sc="Sec. 4(A)(f): loyalty to the Republic; promote locally produced goods, resources and technology; pride of country.", o={
  "o2": (None, S, "Political neutrality concerns serving people regardless of party."),
  "o3": ("Commitment to public interest", S, "Public interest concerns using resources efficiently and honestly; promoting local goods and pride of country is nationalism and patriotism."),
  "o4": (None, S, "Simple living concerns a modest personal lifestyle.")}),
"060057": dict(sc="Sec. 4(A)(g): democratic values, public accountability, civilian supremacy over the military, loyalty to country above persons or party.", o={
  "o1": (None, S, "Simple living concerns a modest personal lifestyle."),
  "o2": ("Nationalism and patriotism", S, "Nationalism covers loyalty to the Republic and local goods; civilian supremacy and putting country above party are under commitment to democracy."),
  "o4": ("Political neutrality", S, "Neutrality concerns serving everyone regardless of party; it does not cover civilian supremacy.")}),
"060058": dict(sc="Sec. 4(A)(h): modest lives appropriate to position and income; no extravagant or ostentatious display of wealth.", o={
  "o2": (None, S, "Professionalism concerns excellence and skill in one's duties."),
  "o3": (None, S, "Political neutrality concerns serving people regardless of party."),
  "o4": ("Commitment to public interest", S, "Public interest concerns the use of government resources; a modest personal lifestyle is simple living.")}),
"060059": dict(sc="Sec. 5(a): reply within 15 working days from receipt, stating the action taken.", o={
  "o1": ("10 working days", N, "Ten working days is when filed SALNs become available for copying (Sec. 8(C)(2))."),
  "o2": ("30 days", N, "30 days is the SALN filing period after assuming office or after separation."),
  "o3": (None, N, "45 working days is the deadline for annual performance reports (Sec. 5(b)).")}),
"060060": dict(sc="Sec. 5(a): the reply must contain the action taken on the request.", o={
  "o2": (None, W, "The reply must state the action taken; it need not grant the request."),
  "o3": ("The name of the employee who received it", W, "An acknowledgment of receipt is not enough; Sec. 5(a) requires the action taken."),
  "o4": (None, W, "Office hours do not tell the sender what was done.")}),
"060061": dict(sc="Sec. 5(b): agency heads render a performance report within 45 working days from the end of the year.", o={
  "o1": ("Within 15 working days", N, "15 working days is the deadline to reply to letters (Sec. 5(a))."),
  "o3": ("Within 30 days", N, "30 days is the SALN filing period after assumption or separation."),
  "o4": ("On or before April 30", N, "April 30 is the yearly SALN deadline (Sec. 8(A)).")}),
"060062": dict(sc="Sec. 5(c): documents should have, as far as practicable, not more than three signatories.", o={
  "o1": (None, N, "Sec. 5(c) sets three as the practicable maximum, not five."),
  "o2": (None, N, "The law does not require a single signatory; the limit is not more than three."),
  "o4": (None, N, "Nine is the number in the scenario, which the law says should be cut to three.")}),
"060063": dict(sc="Sec. 5(d): attend to anyone who wants the office's services, and act promptly and expeditiously.", o={
  "o1": ("Attend to them only by appointment", W, "Sec. 5(d) requires prompt attention to anyone seeking the office's services; it does not require appointments."),
  "o2": ("Refer them to the agency's website first", W, "A referral does not meet the duty to attend promptly to people seeking service."),
  "o3": (None, W, "Favoring people recommended by officials violates the duty to attend to anyone promptly.")}),
"060064": dict(k="Make public documents accessible for inspection", sc="Sec. 5(e): public documents must be accessible to, and readily available for inspection by, the public within reasonable working hours.", o={
  "o1": ("Release documents only upon a court order", W, "Sec. 5(e) makes public documents accessible during reasonable working hours without a court order."),
  "o2": ("Release documents only to the person they concern", W, "Public documents are open to the public, not only to the person concerned."),
  "o4": ("Keep records closed until the yearly audit", W, "No waiting period exists; public documents must be accessible during reasonable working hours.")}),
"060065": dict(k="Financial or material interest in the transaction", sc="Sec. 7(a): no direct or indirect financial or material interest in any transaction requiring the approval of one's office.", o={
  "o1": ("Outside employment with a regulated enterprise", S, "That bars working for an enterprise the office regulates; owning a stake in a transaction the office must approve is Sec. 7(a)."),
  "o3": ("Disclosure of confidential information", S, "Nothing here involves leaking nonpublic information."),
  "o4": ("Solicitation or acceptance of gifts", S, "No gift is offered; the problem is the regulator's own stake in the transaction.")}),
"060066": dict(sc="Sec. 7(b)(1): no ownership, management or employment in a private enterprise regulated, supervised or licensed by one's office, unless expressly allowed by law.", o={
  "o2": ("Financial or material interest in a transaction", S, "Sec. 7(a) concerns a stake in a transaction needing approval; taking a job with a licensed company is Sec. 7(b)(1)."),
  "o3": ("Private practice of a profession", S, "Private practice concerns practicing one's own profession; this is a job with a company the office licenses."),
  "o4": ("Recommending a person to a private enterprise", S, "No one is being recommended; the employee is taking the job himself.")}),
"060067": dict(sc="Sec. 7(b)(2): no private practice unless authorized by the Constitution or law, and only if it does not conflict with official functions.", o={
  "o1": ("Outside employment with a regulated enterprise", S, "That bars jobs in enterprises the office regulates; practicing one's own profession is Sec. 7(b)(2)."),
  "o2": ("Disclosure of confidential information", S, "Nothing confidential is being used."),
  "o3": ("Political neutrality", S, "Party affiliation is not involved.")}),
"060068": dict(k="Recommending someone to a firm dealing with his office", sc="Sec. 7(b)(3): do not recommend anyone to a position in a private enterprise with a regular or pending official transaction with your office.", o={
  "o2": ("Outside employment with a regulated enterprise", S, "The officer is not taking the job; he is recommending someone else, which Sec. 7(b)(3) bars."),
  "o3": ("Solicitation or acceptance of gifts", S, "No gift is involved."),
  "o4": ("Financial or material interest in a transaction", S, "The officer has no stake in the transaction itself; the prohibited act is the recommendation.")}),
"060069": dict(sc="Sec. 7(c): do not use or divulge confidential information known by reason of office to further private interests or prejudice the public interest.", o={
  "o1": ("Financial or material interest in a transaction", S, "No stake in a transaction is described; passing nonpublic data for advantage is Sec. 7(c)."),
  "o2": ("Solicitation or acceptance of gifts", S, "No gift is involved."),
  "o4": ("Recommending a person to a private enterprise", S, "No one is being recommended.")}),
"060070": dict(k="Solicitation or acceptance of gifts", sc="Sec. 7(d): no gift, favor, entertainment, loan or anything of monetary value connected with official duties.", o={
  "o2": ("Financial or material interest in a transaction", S, "The official has no stake in the transaction; an offered favor is a gift problem under Sec. 7(d)."),
  "o3": ("Disclosure of confidential information", S, "No confidential information is involved."),
  "o4": ("Outside employment with a regulated enterprise", S, "No job is offered; it is a favor tied to a decision.")}),
"060071": dict(sc="Sec. 8(A): SALN within 30 days after assumption, on or before April 30 every year, and within 30 days after separation.", o={
  "o1": ("Only upon separation from the service", N, "Filing is also required at assumption and every year, not only at separation."),
  "o2": ("On or before April 30 of the first year", N, "April 30 is the yearly deadline afterward; the first filing is within 30 days of assumption."),
  "o3": ("Within 60 days after assuming office", N, "60 days is the divestment period (Sec. 9); the first SALN is due within 30 days.")}),
"060072": dict(sc="Sec. 8(A): yearly SALN on or before April 30.", o={
  "o2": ("Within 30 days after assuming office", N, "That is the first filing; the yearly deadline is April 30."),
  "o3": (None, N, "December 31 is not a SALN deadline in R.A. 6713; the yearly deadline is April 30."),
  "o4": (None, N, "June 30 is not a SALN deadline in R.A. 6713; the yearly deadline is April 30.")}),
"060073": dict(sc="Sec. 8(A): within 30 days after separation from the service.", o={
  "o1": (None, N, "Sec. 8(A) requires a filing within 30 days after separation."),
  "o3": ("Within 60 days after separation", N, "60 days is the divestment period; the separation filing is due within 30 days."),
  "o4": ("On or before April 30 of the next year", N, "April 30 is the yearly deadline; separation requires filing within 30 days.")}),
"060074": dict(sc="Sec. 8(C)(2): filed statements are available for copying after ten working days.", o={
  "o1": (None, N, "45 working days is the performance-report deadline (Sec. 5(b))."),
  "o2": ("15 working days", N, "15 working days is the reply period for letters (Sec. 5(a))."),
  "o4": ("30 days", N, "30 days is a SALN filing period, not the wait before copying.")}),
"060075": dict(sc="Sec. 9: resign from the private position within 30 days; divest shares within 60 days from assumption.", o={
  "o1": (None, N, "15 working days is the reply period for letters (Sec. 5(a))."),
  "o2": (None, N, "One year is how long the Sec. 7(b) prohibitions continue after leaving office."),
  "o3": (None, N, "30 days is the deadline to resign from a private business position; divesting shares gets 60 days.")}),
}
