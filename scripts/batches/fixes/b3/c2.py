# Grok Bot audit of chatgpt-batch-003, items 060026-060050. "stem" replaces the stem where noted.
S, B, W, N, O = "GI-SIBLING-TERM", "GI-WRONG-BODY", "GI-SOUNDS-RIGHT", "GI-NEIGHBOR-NUMBER", "GI-OLD-RULE"
D = {
"060026": dict(stem="A municipal office threatens to confiscate a resident's property without notice or a hearing. Which protection is implicated?",
  sc="Art. III, Sec. 1: no deprivation of life, liberty or property without due process of law.", o={
  "o2": ("Just compensation", S, "Just compensation applies when property is lawfully taken for public use; the problem here is the missing notice and hearing."),
  "o3": (None, S, "Equal protection concerns unequal treatment of people in similar situations; the problem here is missing procedure."),
  "o4": (None, S, "Double jeopardy bars a second prosecution for the same offense; no criminal case is involved.")}),
"060027": dict(sc="Same situation, different treatment, no valid reason: equal protection (Art. III, Sec. 1).", o={
  "o1": ("Due process of law", S, "Due process concerns fair procedure before a deprivation; the complaint here is unequal treatment of people in similar situations."),
  "o2": ("Non-impairment of contracts", S, "Non-impairment (Sec. 10) protects existing contracts from later laws; no contract is involved."),
  "o3": ("Free access to the courts", S, "Free access (Sec. 11) protects against denial of court access because of poverty; the issue here is unequal treatment under a rule.")}),
"060028": dict(sc="Art. III, Sec. 2: probable cause is determined personally by the judge, after examining the complainant and witnesses under oath.", o={
  "o2": ("A prosecutor", O, "Earlier constitutions let another officer authorized by law issue warrants; under the 1987 Constitution only a judge may determine probable cause for a warrant."),
  "o3": ("The Chief of the Philippine National Police", B, "Police apply for warrants; they cannot issue or approve them."),
  "o4": ("A barangay captain", B, "Barangay officials have no power to determine probable cause for warrants.")}),
"060029": dict(sc="Art. III, Sec. 2: a warrant must particularly describe the place to be searched and the persons or things to be seized. No general warrants.", o={
  "o1": ("Probable cause personally determined by a judge", S, "That is also required by Sec. 2, but the defect described is that the warrant names no particular place or things."),
  "o3": ("Examination of the complainant under oath", S, "Also required by Sec. 2, but nothing says it was skipped; the defect shown is the lack of a particular description."),
  "o4": ("Prior approval by the barangay", W, "No such requirement exists; Sec. 2 requires a particular description of the place and things.")}),
"060030": dict(sc="Art. III, Sec. 3(1): privacy of communication and correspondence is inviolable, except by court order or when public safety or order requires it as prescribed by law.", o={
  "o2": ("Right to information on matters of public concern", S, "That gives access to public records; private letters are protected by Sec. 3(1)."),
  "o3": ("Freedom of the press", S, "Press freedom protects publishing; intercepting private letters is a privacy issue."),
  "o4": ("Liberty of abode", S, "Liberty of abode concerns where one lives, not correspondence.")}),
"060031": dict(sc="Art. III, Sec. 3(2): evidence obtained in violation of Sec. 2 or 3 is inadmissible for any purpose in any proceeding.", o={
  "o1": (None, W, "The exclusion covers any proceeding, civil or criminal."),
  "o2": ("They are admissible if the court finds them relevant.", W, "Relevance does not cure the violation; Sec. 3(2) bars such evidence for any purpose."),
  "o3": ("They may be used only to impeach a witness.", W, "Sec. 3(2) allows no exception; the evidence is inadmissible for any purpose.")}),
"060032": dict(k="Freedom of assembly and petition", sc="Art. III, Sec. 4: peaceably assemble and petition the government for redress of grievances.", o={
  "o1": ("Right to information on matters of public concern", S, "Asking for reconsideration is a petition; the right to information is about getting public records."),
  "o2": ("Freedom of association", S, "Association covers forming groups; peacefully gathering to petition is assembly and petition."),
  "o4": ("Liberty of abode and travel", S, "That concerns where one lives and travels, not gathering to petition.")}),
"060033": dict(sc="Art. III, Sec. 4: no law shall be passed abridging freedom of speech, of expression, or of the press.", o={
  "o1": ("Right to information on matters of public concern", S, "That concerns access to public records; a ban on criticism abridges speech."),
  "o3": ("Freedom of religion", S, "Nothing here involves religious belief."),
  "o4": ("Freedom of assembly", S, "Assembly protects gatherings; this law punishes the criticism itself, which is speech.")}),
"060034": dict(sc="Art. III, Sec. 5: no religious test shall be required for the exercise of civil or political rights.", o={
  "o2": ("Freedom of speech and expression", S, "Speech is not at issue; Sec. 5 bars any religious test for civil or political rights."),
  "o3": ("Right to information on matters of public concern", S, "That concerns access to public records, not a religious requirement."),
  "o4": ("Liberty of abode", S, "Liberty of abode concerns where a person lives, not religion.")}),
"060035": dict(sc="Art. III, Sec. 5: no law shall be made respecting an establishment of religion.", o={
  "o1": ("Prohibition of religious tests", S, "That bars requiring a religion for civil or political rights; declaring an official religion is establishment."),
  "o2": ("Freedom of speech and expression", S, "Speech is not at issue; an official religion violates the non-establishment clause."),
  "o3": ("Academic freedom", S, "Academic freedom (Art. XIV) protects institutions of higher learning, not religion.")}),
"060036": dict(sc="Art. III, Sec. 6: abode is limited only by court order; travel only for national security, public safety or public health, as provided by law.", o={
  "o2": ("Liberty of abode", S, "Liberty of abode concerns where a person lives and can be limited only by a court order; the restriction here is on travel."),
  "o3": ("Freedom of association", S, "Nothing here concerns forming groups."),
  "o4": ("Freedom of expression", S, "Nothing here involves speech.")}),
"060037": dict(sc="Art. III, Sec. 7: the right of the people to information on matters of public concern, subject to limits provided by law.", o={
  "o1": ("Freedom of the press", S, "Press freedom protects publishing; access to government records is the right to information."),
  "o2": ("Privacy of communication and correspondence", S, "Privacy protects private correspondence, not access to public records."),
  "o4": ("Full public disclosure policy", S, "Art. II, Sec. 28 is a State policy; the right a resident invokes is the right to information in Art. III, Sec. 7.")}),
"060038": dict(sc="Art. III, Sec. 8: the right to form unions, associations or societies for purposes not contrary to law shall not be abridged.", o={
  "o2": ("Freedom of peaceable assembly", S, "Assembly concerns gathering; forming a lasting group is association."),
  "o3": ("Non-impairment of contracts", S, "Nothing here involves an existing contract."),
  "o4": (None, S, "Voting is suffrage (Art. V), not association.")}),
"060039": dict(sc="Art. III, Sec. 9: private property shall not be taken for public use without just compensation.", o={
  "o1": ("Market value as fixed by the local assessor", W, "Just compensation is decided by the courts; an assessor's figure does not settle it."),
  "o2": ("Payment only if the owner consents to the taking", W, "Expropriation does not need the owner's consent; it needs public use and just compensation."),
  "o3": ("A replacement lot of equal size", W, "The Constitution requires just compensation, not a replacement lot.")}),
"060040": dict(k="Free access to the courts and adequate legal assistance", sc="Art. III, Sec. 11: free access to the courts and adequate legal assistance shall not be denied to any person by reason of poverty.", o={
  "o2": ("Right to bail", S, "Bail concerns temporary liberty of an accused; the problem here is being shut out of court because of poverty."),
  "o3": ("Speedy disposition of cases", S, "Speedy disposition concerns delay, not denial of access because of poverty."),
  "o4": ("Right to counsel during custodial investigation", S, "That applies to suspects under investigation (Sec. 12); Sec. 11 covers court access for the poor.")}),
"060041": dict(k="Right to remain silent and to counsel, and to be told of these rights", sc="Art. III, Sec. 12(1): a person under investigation has the right to remain silent and to competent, independent counsel, and must be informed of these rights.", o={
  "o1": ("Presumption of innocence", S, "That protects the accused at trial; Sec. 12(1) is about warnings during custodial investigation."),
  "o3": ("Right to be informed of the nature and cause of the accusation", S, "That applies at trial (Sec. 14(2)); a suspect being questioned must be told of silence and counsel."),
  "o4": ("Right to bail", S, "Bail concerns provisional liberty, not warnings during questioning.")}),
"060042": dict(k="Torture, force, threats or intimidation that vitiate free will", sc="Art. III, Sec. 12(2): no torture, force, violence, threat or intimidation that vitiates free will may be used against him.", o={
  "o1": ("Questioning a suspect without a video recording", W, "The Constitution does not require video; it bans torture, force, threats and intimidation."),
  "o2": ("Questioning a suspect for more than one hour", W, "Sec. 12(2) sets no time limit; it bans force and intimidation."),
  "o4": (None, W, "Providing counsel is required, not prohibited.")}),
"060043": dict(stem="An accused charged with a bailable offense asks, before conviction, to post sufficient bail. Which constitutional protection applies?", k="Right to bail before conviction",
  sc="Art. III, Sec. 13: all persons have the right to bail before conviction, except those charged with offenses punishable by reclusion perpetua when evidence of guilt is strong.", o={
  "o1": ("Presumption of innocence", S, "Innocence is presumed at trial; release on sufficient sureties is the right to bail."),
  "o2": ("Right to a speedy trial", S, "Speedy trial concerns delay, not release pending trial."),
  "o3": ("Right to bail after any conviction", W, "Sec. 13 gives the right before conviction, and it excludes offenses punishable by reclusion perpetua when evidence of guilt is strong.")}),
"060044": dict(stem="A criminal court treats a defendant as guilty before the evidence is presented. Which constitutional guarantee is violated?",
  sc="Art. III, Sec. 14(2): the accused is presumed innocent until the contrary is proved.", o={
  "o1": ("Presumption of regularity in official duty", S, "That evidence rule favors officials' acts; the Constitution's guarantee to the accused is the presumption of innocence."),
  "o2": ("Right to bail", S, "Bail concerns release; treating the accused as guilty before evidence violates the presumption of innocence."),
  "o4": ("Privilege against self-incrimination", S, "Nothing here involves compelled testimony.")}),
"060045": dict(sc="Art. III, Sec. 14(2): the accused shall be informed of the nature and cause of the accusation against him.", o={
  "o1": ("Right to a speedy, impartial and public trial", S, "That concerns how the trial is held; not knowing the charge breaches the right to be informed of the accusation."),
  "o3": ("Right to confront witnesses", S, "Confrontation concerns witnesses at trial, not notice of the charge."),
  "o4": ("Presumption of innocence", S, "The accused is still presumed innocent; the defect described is lack of notice of the charge.")}),
"060046": dict(sc="Art. III, Sec. 15: only invasion or rebellion, when public safety requires it. 'Imminent danger' was dropped in 1987.", o={
  "o2": ("Invasion, rebellion, or imminent danger thereof", O, "'Imminent danger' was a ground under earlier constitutions; the 1987 text keeps only actual invasion or rebellion."),
  "o3": ("Lawless violence or public disorder", S, "Lawless violence lets the President call out the armed forces (Art. VII, Sec. 18); it is not a ground for suspending the writ."),
  "o4": ("A national emergency declared by Congress", S, "Emergency powers (Art. VI, Sec. 23) are separate; the writ may be suspended only for invasion or rebellion when public safety requires it.")}),
"060047": dict(stem="A complaint has been pending for years before an administrative body without action. Which constitutional right most specifically applies?",
  sc="Speedy TRIAL is for criminal cases (Sec. 14(2)); speedy DISPOSITION covers judicial, quasi-judicial and administrative bodies (Sec. 16).", o={
  "o1": ("Right to a speedy trial", S, "Speedy trial applies to criminal prosecutions; before any judicial, quasi-judicial or administrative body, the right is speedy disposition (Sec. 16)."),
  "o2": ("Free access to the courts", S, "Access is not denied here; the problem is delay."),
  "o3": ("Right to information on matters of public concern", S, "That concerns access to records, not delay in deciding a case.")}),
"060048": dict(sc="Art. III, Sec. 17: no person shall be compelled to be a witness against himself.", o={
  "o2": ("Right to remain silent during custodial investigation", S, "Sec. 12 covers suspects under custodial investigation; a witness compelled to testify invokes the privilege against self-incrimination (Sec. 17)."),
  "o3": (None, W, "A witness must still appear; the privilege lets the witness refuse only incriminating answers."),
  "o4": ("Presumption of innocence", S, "That protects an accused at trial; it does not address compelled testimony by a witness.")}),
"060049": dict(sc="Art. III, Sec. 20: no imprisonment for debt or non-payment of a poll tax.", o={
  "o1": (None, W, "Creditors may still sue to collect; what is barred is imprisonment for debt."),
  "o2": ("No imprisonment for failure to pay any tax", W, "Sec. 20 covers only non-payment of a poll tax; it does not bar penalties for other taxes."),
  "o4": ("Prohibition of involuntary servitude", S, "Involuntary servitude (Sec. 18(2)) concerns forced labor; jailing for unpaid debt is covered by Sec. 20.")}),
"060050": dict(sc="Art. XIII, Sec. 18(1): the CHR investigates, on its own or on complaint, all forms of human-rights violations involving civil and political rights.", o={
  "o2": ("Civil Service Commission", B, "The CSC handles personnel matters, not human-rights complaints."),
  "o3": (None, B, "COMELEC runs elections; it does not investigate human-rights violations."),
  "o4": ("Department of Justice", B, "The DOJ prosecutes crimes; the constitutional body that investigates human-rights violations is the CHR.")}),
}
