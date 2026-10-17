# Grok Bot audit of chatgpt-batch-003, items 060001-060025.
# Per item: optional new key text "k", reveal.shortcut "sc", and every wrong option: (new text or None, code or None, why).
S, B, W, N = "GI-SIBLING-TERM", "GI-WRONG-BODY", "GI-SOUNDS-RIGHT", "GI-NEIGHBOR-NUMBER"
D = {
"060001": dict(sc="Art. II, Sec. 3: civilian authority is, at all times, supreme over the military.", o={
  "o1": ("The Commander-in-Chief clause makes the military co-equal with civilian officials.", W, "The Commander-in-Chief is a civilian, and Sec. 3 puts civilian authority above the military, not beside it."),
  "o3": ("Renunciation of war as an instrument of national policy", S, "That is Art. II, Sec. 2, about relations with other states, not about who outranks whom at home."),
  "o4": ("Separation of Church and State", S, "Art. II, Sec. 6 concerns religion and government, not civilian control of the military.")}),
"060002": dict(sc="Art. II, Sec. 4 opens with the prime duty: to serve and protect the people.", o={
  "o2": ("To promote a just and dynamic social order", S, "That is a State policy in Art. II, Sec. 9; Sec. 4 names serving and protecting the people as the prime duty."),
  "o3": ("To maintain peace and order", S, "Art. II, Sec. 5 calls peace and order essential, but it is not the duty Sec. 4 calls prime."),
  "o4": ("To require every citizen to render military service", W, "Sec. 4 says citizens may be required to render military or civil service; that is a power of the Government, not its prime duty.")}),
"060003": dict(sc="Art. II, Sec. 14: women's role in nation-building and the fundamental equality before the law of women and men.", o={
  "o1": ("The State shall equally protect the life of the mother and of the unborn.", S, "That is Art. II, Sec. 12 on the family, not equality of women and men."),
  "o2": ("The State recognizes the vital role of the youth in nation-building.", S, "That is Art. II, Sec. 13 on the youth."),
  "o3": ("The State values the dignity of every human person.", W, "Art. II, Sec. 11 states a general value; Sec. 14 is the specific policy on equality of women and men.")}),
"060004": dict(sc="Art. II, Sec. 25: the State shall ensure the autonomy of local governments.", o={
  "o2": ("Fiscal autonomy", S, "Fiscal autonomy is given to bodies such as the Judiciary and the constitutional commissions; Sec. 25 speaks of the autonomy of local governments."),
  "o3": ("Federalism", W, "The 1987 Constitution keeps a unitary state; Sec. 25 promises local autonomy, not a federal system."),
  "o4": ("Separation of powers", S, "Separation of powers divides power among the three branches, not between the national and local governments.")}),
"060005": dict(sc="Art. II, Sec. 28: full public disclosure of transactions involving public interest, subject to reasonable conditions set by law.", o={
  "o1": ("Disclosure only of transactions the agency head chooses", W, "Sec. 28 makes disclosure the policy, limited only by reasonable conditions set by law, not by an agency head's choice."),
  "o2": ("Confidentiality of procurement until contracts are paid", W, "Blanket confidentiality is the opposite of the full-disclosure policy in Sec. 28."),
  "o4": ("Honesty and integrity in the public service", S, "That is Art. II, Sec. 27, which targets graft and corruption; Sec. 28 is the disclosure policy.")}),
"060006": dict(k="Congress of the Philippines", sc="Art. VI, Sec. 1: legislative power is vested in Congress (Senate + House), except what the people reserve through initiative and referendum.", o={
  "o2": ("The President, through executive orders", B, "Executive orders carry out laws; Art. VI, Sec. 1 vests the power to make laws in Congress."),
  "o3": ("The Senate alone", B, "Congress has two chambers; the Senate alone does not hold the legislative power."),
  "o4": ("The people, through initiative and referendum", S, "The people hold only the part reserved by initiative and referendum; the general legislative power is vested in Congress.")}),
"060007": dict(sc="Art. VI, Sec. 24: appropriation, revenue and tariff bills originate exclusively in the House; the Senate may propose or concur with amendments.", o={
  "o1": (None, B, "The Senate may amend a revenue bill, but the bill cannot start there."),
  "o2": ("Office of the President, through the budget message", B, "The President submits the budget, but the revenue bill itself must originate in the House."),
  "o3": ("Either chamber, whichever files it first", W, "Sec. 24 says such bills originate exclusively in the House.")}),
"060008": dict(sc="Art. VI, Sec. 27(1): each House votes separately, and the override needs two-thirds of ALL its members.", o={
  "o2": ("A majority of all members of each House", N, "A majority passes a bill; overriding a veto needs two-thirds of all members of each House."),
  "o3": ("Three-fourths of all members of each House", N, "Three-fourths is not the override threshold; Sec. 27(1) sets two-thirds."),
  "o4": ("Two-thirds of the members present in a joint session", N, "The Houses vote separately, and the count is two-thirds of all members, not of those present in a joint session.")}),
"060009": dict(sc="Art. VI, Sec. 28(1): the rule of taxation shall be uniform and equitable, and Congress shall evolve a progressive system.", o={
  "o1": ("Congress shall evolve a regressive system of taxation.", S, "Sec. 28(1) directs a progressive system, not a regressive one."),
  "o3": (None, W, "Uniform means the same rule for the same class of taxpayers, not the same peso amount for everyone."),
  "o4": ("A tax exemption needs a majority of all members of Congress.", S, "That is Sec. 28(4), a voting rule for tax exemptions, not the uniformity and equity rule.")}),
"060010": dict(sc="Initiative = the people propose a law; referendum = the people approve or reject one (Art. VI, Sec. 32).", o={
  "o1": ("Recall", S, "Recall removes a local official; it does not propose laws."),
  "o2": ("Plebiscite", S, "A plebiscite ratifies constitutional changes or changes to local units; it is not how voters propose laws."),
  "o4": ("Referendum", S, "A referendum lets voters approve or reject a law already passed; proposing a new law is initiative.")}),
"060011": dict(sc="Art. VII, Sec. 1: the executive power shall be vested in the President of the Philippines.", o={
  "o1": ("The Vice-President", B, "The Vice-President may sit in the Cabinet but does not hold the executive power."),
  "o2": ("The Cabinet as a collegial body", B, "Department secretaries act for the President; Sec. 1 vests executive power in the President alone."),
  "o3": (None, B, "The Chief Justice heads the Judiciary, not the executive branch.")}),
"060012": dict(sc="Art. VII, Sec. 21: no treaty is valid without the concurrence of at least two-thirds of ALL the members of the Senate.", o={
  "o1": ("All members of the Senate, by a majority vote", N, "The Senate is right, but the vote is two-thirds, not a majority."),
  "o2": ("Congress voting jointly, by a majority of all its members", B, "Joint majority votes are for martial law; treaties need only the Senate, by two-thirds of all its members."),
  "o4": (None, B, "The House has no role in concurring with treaties.")}),
"060013": dict(sc="Art. VII, Sec. 18: the President proclaims (up to 60 days); Congress, voting jointly by a majority of all members, may revoke or, on the President's initiative, extend.", o={
  "o1": ("The President alone, for another 60 days", B, "The President may proclaim martial law for up to 60 days, but only Congress can extend it."),
  "o3": ("The Senate alone, by two-thirds of all its members", B, "Extension is by both Houses voting jointly, by a majority of all members."),
  "o4": ("The Supreme Court, on petition of any citizen", B, "The Court reviews whether the proclamation has a sufficient factual basis; it does not extend it.")}),
"060014": dict(sc="Art. VIII, Sec. 1: judicial power includes the duty to determine grave abuse of discretion by any branch or instrumentality.", o={
  "o2": (None, S, "Control over executive offices belongs to the President; ruling on grave abuse of discretion is a judicial duty."),
  "o3": ("Legislative inquiry", S, "Congress conducts inquiries in aid of legislation (Art. VI, Sec. 21); it does not rule on grave abuse of discretion."),
  "o4": ("Administrative supervision over lower courts", S, "Administrative supervision (Art. VIII, Sec. 6) concerns running the courts, not deciding whether another body gravely abused its discretion.")}),
"060015": dict(sc="Art. VIII, Sec. 8-9: the Judicial and Bar Council recommends; the President appoints from its list, with no confirmation needed.", o={
  "o1": ("Commission on Appointments", B, "The Commission on Appointments confirms certain executive appointments; judicial appointees come from JBC lists and need no confirmation."),
  "o2": ("Integrated Bar of the Philippines", B, "The IBP has a representative in the JBC, but it does not itself recommend nominees."),
  "o3": ("Supreme Court en banc", B, "The Supreme Court appoints court officials and employees, not judges; judicial nominees come from the JBC.")}),
"060016": dict(sc="Article IX has three: CSC (IX-B), COMELEC (IX-C) and COA (IX-D).", o={
  "o2": (None, S, "The Office of the Ombudsman is created under Article XI, not Article IX."),
  "o3": (None, S, "The Judicial and Bar Council is created under Article VIII (the Judiciary)."),
  "o4": (None, S, "The Commission on Human Rights is created under Article XIII, not Article IX.")}),
"060017": dict(k="Appointment according to merit and fitness", sc="Art. IX-B, Sec. 2(2): appointments are made according to merit and fitness, by competitive examination as far as practicable.", o={
  "o1": ("Security of tenure", S, "Tenure protects employees already appointed from removal without cause; the issue here is how applicants are chosen."),
  "o2": ("Ban on partisan political campaigning", S, "That bars electioneering; the problem here is choosing people by recommendation instead of qualifications."),
  "o4": ("Ban on appointing losing candidates within one year", S, "Art. IX-B, Sec. 6 concerns losing election candidates, not hiring by personal recommendation.")}),
"060018": dict(k="Security of tenure", sc="Art. IX-B, Sec. 2(3): no civil-service officer or employee shall be removed or suspended except for cause provided by law.", o={
  "o2": ("Appointment according to merit and fitness", S, "Merit and fitness governs hiring; removal without a stated cause is a tenure issue."),
  "o3": ("Right to self-organization", S, "Self-organization lets employees form associations; it does not govern removal."),
  "o4": ("Standardization of compensation", S, "Art. IX-B, Sec. 5 concerns salaries, not removal from office.")}),
"060019": dict(k="Ban on electioneering and partisan political campaigns", sc="Art. IX-B, Sec. 2(4): no civil-service officer or employee shall engage, directly or indirectly, in electioneering or partisan political campaigns.", o={
  "o1": ("Ban on holding more than one government position", S, "Art. IX-B, Sec. 7 bars dual positions; campaigning is barred by Sec. 2(4)."),
  "o2": ("Appointment according to merit and fitness", S, "Merit and fitness concerns hiring, not campaigning."),
  "o3": ("Freedom of speech and expression", W, "Free speech does not permit a civil servant to campaign; Sec. 2(4) bars partisan campaigning by civil-service employees.")}),
"060020": dict(k="Right to self-organization", sc="Art. IX-B, Sec. 2(5): the right to self-organization shall not be denied to government employees.", o={
  "o1": ("Right to strike in government service", W, "The Constitution protects self-organization; it does not give government workers a right to strike."),
  "o2": ("Security of tenure", S, "Tenure protects against removal without cause; it does not concern forming associations."),
  "o4": ("Appointment according to merit and fitness", S, "Merit and fitness governs hiring, not employee associations.")}),
"060021": dict(sc="Art. IX-C, Sec. 2(1): COMELEC enforces and administers all election laws.", o={
  "o1": (None, B, "The Commission on Human Rights investigates human-rights violations; it does not run elections."),
  "o3": (None, B, "COA audits government accounts; it does not run elections."),
  "o4": (None, B, "The CSC is the government's central personnel agency; it does not run elections.")}),
"060022": dict(sc="Art. IX-D, Sec. 2(1): COA examines, audits and settles all government accounts, revenue and expenditure.", o={
  "o1": (None, B, "The CSC handles government personnel, not audit."),
  "o2": (None, B, "COMELEC runs elections, not audits."),
  "o4": ("Department of Budget and Management", B, "DBM prepares and manages the budget; the constitutional audit power belongs to COA.")}),
"060023": dict(sc="Art. XI, Sec. 1 opens the accountability article: public office is a public trust.", o={
  "o1": ("Public office is a privilege of the appointee.", W, "Art. XI, Sec. 1 makes office a public trust, not a personal privilege."),
  "o2": ("Civilian authority is supreme over the military.", S, "That is Art. II, Sec. 3, not the accountability maxim."),
  "o3": ("Sovereignty resides in the people.", S, "That is Art. II, Sec. 1 on where sovereignty lies; Art. XI, Sec. 1 is the rule on public office.")}),
"060024": dict(sc="Art. XI, Sec. 3: the House initiates; the Senate tries and decides.", o={
  "o2": (None, B, "The Supreme Court has no role in initiating impeachment."),
  "o3": (None, B, "The Ombudsman is one of the officials who can be impeached; it cannot initiate impeachment."),
  "o4": (None, B, "The Senate tries and decides impeachment cases; it cannot initiate them.")}),
"060025": dict(sc="Art. XI, Sec. 3(6): the Senate has the sole power to try and decide all cases of impeachment.", o={
  "o1": (None, B, "The House initiates and prosecutes the case; it does not try it."),
  "o2": ("Supreme Court", B, "The Chief Justice presides when the President is tried, but the Senate decides."),
  "o4": ("Congress in joint session", B, "The trial is by the Senate alone, not both Houses jointly.")}),
}
