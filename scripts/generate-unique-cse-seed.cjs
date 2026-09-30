/**
 * Local CIVIO/Hiraya bank expansion — CSE Professional-style practice (NOT official CSC items).
 * Append-only INSERT into questions. Run: node scripts/generate-unique-cse-seed.mjs
 */
const fs = require('fs');
const path = require('path');

const CREATED_BY = 1;

/** @type {{sub:number, lang?:string, stem:string, options:string[], correct:number, expl:string}[]} */
const Q = [];

function add(sub, stem, options, correct, expl, lang = 'English') {
  if (!Array.isArray(options) || options.length < 2) throw new Error('bad options: ' + stem.slice(0, 40));
  if (correct < 0 || correct >= options.length) throw new Error('bad correct: ' + stem.slice(0, 40));
  if (!stem || !stem.trim()) throw new Error('empty stem');
  Q.push({ sub, lang, stem: stem.trim(), options, correct, expl: expl.trim() });
}

// ========== GENERAL INFORMATION — Philippine Constitution (1) ==========
add(1, 'Under the 1987 Constitution, sovereignty resides in the people and all government authority emanates from them. This principle is primarily found in:',
  ['Article II (Declaration of Principles and State Policies)', 'Article III (Bill of Rights)', 'Article VI (Legislative Department)', 'Article VII (Executive Department)'],
  0, 'Article II, Section 1 affirms that the Philippines is a democratic and republican State; sovereignty resides in the people.');
add(1, 'The power of judicial review allows the Supreme Court to:',
  ['Enact statutes when Congress fails to act', 'Determine whether a law or act is unconstitutional', 'Appoint Cabinet secretaries', 'Dissolve local government units unilaterally'],
  1, 'Judicial review is the authority of courts to invalidate governmental acts that conflict with the Constitution.');
add(1, 'Which body has the exclusive power to initiate impeachment cases against impeachable officers?',
  ['The Senate', 'The House of Representatives', 'The Supreme Court', 'The Ombudsman'],
  1, 'The House of Representatives has the exclusive power to initiate impeachment; the Senate tries impeachment cases.');
add(1, 'Members of the House of Representatives are elected for a term of:',
  ['Three years', 'Four years', 'Five years', 'Six years'],
  0, 'Article VI provides a three-year term for members of the House of Representatives.');
add(1, 'The Commission on Elections (COMELEC) is a:',
  ['Regular executive department under the DILG', 'Constitutional Commission under Article IX', 'Ad hoc body created only during election years', 'Committee of Congress'],
  1, 'COMELEC is one of the three independent Constitutional Commissions under Article IX.');
add(1, 'Natural-born citizens of the Philippines are those:',
  ['Who were naturalized by Congress only', 'Who are citizens from birth without having to perform any act to acquire or perfect citizenship', 'Who resided in the Philippines for ten continuous years', 'Who hold dual citizenship exclusively'],
  1, 'Article IV defines natural-born citizens as those who are citizens from birth without needing any act to acquire or perfect citizenship.');
add(1, 'The Writ of Amparo is primarily intended to protect:',
  ['Property rights in land disputes', 'The right to life, liberty, and security against extralegal threats', 'Corporate franchise renewals', 'Customs valuation disputes'],
  1, 'The Writ of Amparo is a remedy to protect persons whose right to life, liberty, and security is violated or threatened.');
add(1, 'Local government units enjoy local autonomy subject to:',
  ['Complete independence from national laws', 'Supervision by the President and applicable laws', 'Approval of barangay assemblies only', 'Exclusive control by the judiciary'],
  1, 'LGUs enjoy local autonomy but remain under the general supervision of the President and must follow national laws.');
add(1, 'The party-list system is designed primarily to:',
  ['Replace district representation entirely', 'Give marginalized and underrepresented sectors a voice in Congress', 'Elect the President by popular vote only', 'Appoint justices of the Supreme Court'],
  1, 'The party-list system aims to enable marginalized and underrepresented sectors to obtain seats in the House.');
add(1, 'Which of the following is NOT a Constitutional Commission?',
  ['Civil Service Commission', 'Commission on Audit', 'Commission on Human Rights', 'Commission on Elections'],
  2, 'CHR is an independent office created by the Constitution but is not one of the three Constitutional Commissions (CSC, COMELEC, COA).');

// ========== GI — RA 6713 (2) ==========
add(2, 'Under R.A. 6713, public officials must always put which interest above personal interest?',
  ['Party interest', 'Public interest', 'Family business interest', 'Agency overtime interest only'],
  1, 'R.A. 6713 emphasizes that public interest must be upheld over personal interest.');
add(2, 'A Statement of Assets, Liabilities and Net Worth (SALN) must generally be filed:',
  ['Only when promoted', 'Upon assumption of office, annually, and upon separation', 'Every ten years', 'Only if salary exceeds a fixed threshold'],
  1, 'SALN filing is required upon assumption, every year thereafter, and upon separation from service.');
add(2, 'Which act is generally prohibited for public officials under the Code of Conduct?',
  ['Attending official training', 'Accepting gifts in connection with official duties', 'Reporting anomalies to proper authorities', 'Consulting stakeholders in policymaking'],
  1, 'Soliciting or accepting gifts related to official duties is among the prohibited acts under R.A. 6713.');
add(2, 'Transparency of public transactions under ethical standards typically requires:',
  ['Keeping all procurement secret until after award forever', 'Making information accessible as required by law and policy', 'Publishing only favorable news', 'Avoiding written records'],
  1, 'Ethical standards promote transparency and accessibility of public information consistent with law.');
add(2, 'Divestment under conflict-of-interest rules generally means:',
  ['Transferring conflicting financial interests within a required period', 'Resigning from all government posts immediately', 'Hiding assets from the SALN', 'Donating salary to charity'],
  0, 'Divestment refers to disposing of conflicting financial interests within the period required by law.');
add(2, 'Simple living as a norm for public officials under R.A. 6713 means officials should:',
  ['Live beyond their means to inspire confidence', 'Lead modest lives appropriate to their positions and income', 'Avoid any community involvement', 'Refuse all lawful compensation'],
  1, 'The Code encourages simple and modest living commensurate with position and lawful income.');
add(2, 'Which is an example of a conflict of interest?',
  ['An official deciding a bid where a close relative owns a bidder', 'An official attending a public hearing', 'An official filing a leave form', 'An official reading the Official Gazette'],
  0, 'Participating in a decision that affects a relative\'s business interest is a classic conflict of interest.');
add(2, 'Whistleblowing about graft, when done through proper channels, is generally:',
  ['A prohibited act under R.A. 6713', 'Consistent with the duty to uphold public interest', 'Grounds for automatic dismissal', 'Allowed only for Cabinet members'],
  1, 'Reporting wrongdoing through lawful channels aligns with public interest and ethical duties.');

// ========== GI — Peace and Human Rights (3) ==========
add(3, 'The principle of non-discrimination in human rights means rights apply:',
  ['Only to citizens with college degrees', 'To all persons without unjust distinction', 'Only during peacetime', 'Only to government employees'],
  1, 'Human rights are universal and must be enjoyed without unjust discrimination.');
add(3, 'Habeas corpus primarily protects against:',
  ['Unlawful detention', 'Unpaid taxes', 'Zoning violations', 'Trademark infringement'],
  0, 'Habeas corpus is a remedy against unlawful restraint of liberty.');
add(3, 'The Commission on Human Rights (CHR) is empowered to:',
  ['Convict criminal offenders in regular courts', 'Investigate human rights violations and monitor compliance', 'Enact criminal codes', 'Replace the Department of Justice'],
  1, 'CHR investigates human rights violations and monitors government observance of human rights; it does not try and convict as a regular court.');
add(3, 'Children\'s rights under Philippine policy emphasize:',
  ['Forced labor as character building', 'Protection, education, and best interests of the child', 'Political campaigning before age 10', 'Exemption from all parental guidance'],
  1, 'Philippine policy prioritizes the best interests of the child, including protection and education.');
add(3, 'Freedom of expression may be limited when:',
  ['The government dislikes criticism of any kind', 'Speech creates a clear and present danger of substantive evil as allowed by law', 'A private citizen asks politely', 'An election is more than one year away'],
  1, 'Constitutional freedoms may be restricted under lawful standards such as clear and present danger, not mere dislike of criticism.');
add(3, 'Peace education in communities often focuses on:',
  ['Glorifying violence', 'Conflict resolution, respect for rights, and dialogue', 'Eliminating all elections', 'Banning all civic organizations'],
  1, 'Peace education promotes nonviolent conflict resolution, human rights, and constructive dialogue.');
add(3, 'Indigenous peoples\' rights in the Philippines are principally framed by:',
  ['R.A. 8371 (IPRA)', 'The Clean Air Act alone', 'The Negotiable Instruments Law', 'The Tariff and Customs Code only'],
  0, 'R.A. 8371, the Indigenous Peoples\' Rights Act (IPRA), is the principal statute on IP rights.');
add(3, 'Extrajudicial killing, if proven, violates primarily the right to:',
  ['Travel abroad', 'Life', 'Form corporations', 'Inherit property only'],
  1, 'Arbitrary deprivation of life violates the fundamental right to life.');

// ========== GI — Environment (4) ==========
add(4, 'R.A. 9003 primarily deals with:',
  ['Clean air standards only', 'Ecological solid waste management', 'Income taxation', 'Civil service eligibility'],
  1, 'R.A. 9003 is the Ecological Solid Waste Management Act.');
add(4, 'An Environmental Impact Statement (EIS) system is important because it:',
  ['Removes all project regulation', 'Assesses potential environmental effects before major projects proceed', 'Replaces building permits entirely', 'Applies only to residential backyard gardens'],
  1, 'The EIS system evaluates significant environmental impacts of covered projects before implementation.');
add(4, 'The precautionary principle in environmental policy suggests that:',
  ['Action to prevent harm may be taken even if scientific certainty is incomplete', 'Pollution should continue until absolute proof of harm', 'Only foreign companies need permits', 'Trees may be cut without assessment always'],
  0, 'The precautionary approach supports preventive measures despite incomplete scientific certainty of harm.');
add(4, 'Climate change adaptation in local governance commonly includes:',
  ['Ignoring flood maps', 'Disaster risk reduction planning and resilient infrastructure', 'Banning all weather forecasts', 'Removing drainage systems'],
  1, 'Adaptation includes DRRM planning, resilient design, and risk-informed land use.');
add(4, 'Illegal logging primarily threatens:',
  ['Forest ecosystems and biodiversity', 'Only coastal mangroves in other countries', 'Stock market indexes exclusively', 'Postal delivery schedules'],
  0, 'Illegal logging depletes forests and harms biodiversity and watershed functions.');
add(4, 'Segregation at source in solid waste management means:',
  ['Mixing all waste before collection', 'Separating recyclables, biodegradables, and residuals at the household or establishment', 'Burning plastics in open pits only', 'Dumping waste in rivers'],
  1, 'Segregation at source separates waste types where they are generated to enable proper processing.');
add(4, 'Protected areas under the NIPAS framework are intended to:',
  ['Maximize commercial mining without review', 'Conserve biodiversity and ecological processes', 'Convert all forests to subdivisions automatically', 'Eliminate tourism forever'],
  1, 'NIPAS aims to protect and maintain biodiversity and vital ecological processes in protected areas.');
add(4, 'Which agency is primarily associated with environmental management and natural resources at the national level?',
  ['Department of Environment and Natural Resources (DENR)', 'Bureau of Internal Revenue', 'Philippine Statistics Authority alone', 'Land Transportation Office alone'],
  0, 'DENR is the primary national agency for environment and natural resources management.');

// ========== VERBAL — Word meaning (5) ==========
add(5, 'The word PRUDENT most nearly means:',
  ['Reckless', 'Wise and careful', 'Noisy', 'Obsolete'],
  1, 'Prudent means acting with or showing care and thought for the future.');
add(5, 'An antonym of SCARCE is:',
  ['Rare', 'Abundant', 'Limited', 'Sparse'],
  1, 'Scarce means in short supply; abundant is the opposite.');
add(5, 'CANDID most nearly means:',
  ['Deceitful', 'Frank and honest', 'Ambiguous', 'Hostile'],
  1, 'Candid means truthful and straightforward.');
add(5, 'The word MITIGATE is closest in meaning to:',
  ['Intensify', 'Lessen or make less severe', 'Ignore completely', 'Celebrate'],
  1, 'To mitigate is to make milder or less severe.');
add(5, 'OBSOLETE most nearly means:',
  ['Brand new', 'Outdated or no longer in use', 'Essential', 'Transparent'],
  1, 'Obsolete means no longer produced or used; out of date.');
add(5, 'A synonym of IMPARTIAL is:',
  ['Biased', 'Fair and unbiased', 'Emotional', 'Secretive'],
  1, 'Impartial means treating all rivals or disputants equally; fair.');
add(5, 'The word VERBOSE describes writing that is:',
  ['Concise', 'Wordy', 'Silent', 'Illustrated only'],
  1, 'Verbose means using more words than needed.');
add(5, 'RESILIENT most nearly means:',
  ['Fragile', 'Able to recover quickly', 'Permanent', 'Indifferent'],
  1, 'Resilient means able to withstand or recover quickly from difficulties.');
add(5, 'An antonym of TRANSPARENT (in governance contexts) is:',
  ['Open', 'Opaque or secretive', 'Clear', 'Accountable'],
  1, 'Transparent means open/clear; opaque or secretive is opposite in this sense.');
add(5, 'CREDIBLE evidence is evidence that is:',
  ['Unbelievable', 'Believable and trustworthy', 'Illegal', 'Anonymous only'],
  1, 'Credible means able to be believed; convincing.');

// ========== VERBAL — Sentence completion (6) ==========
add(6, 'Despite the limited budget, the agency remained _____ and completed the project on time.',
  ['profligate', 'resourceful', 'apathetic', 'negligent'],
  1, 'Resourceful fits: they found ways despite constraints.');
add(6, 'The auditor\'s report was so _____ that even non-experts understood the findings.',
  ['obscure', 'lucid', 'convoluted', 'ambiguous'],
  1, 'Lucid means clear and easy to understand.');
add(6, 'Public servants are expected to act with _____ even when no one is watching.',
  ['integrity', 'indifference', 'partiality', 'hostility'],
  0, 'Integrity is honesty and strong moral principles.');
add(6, 'The committee postponed the hearing _____ additional documents could be reviewed.',
  ['unless', 'so that', 'although', 'despite'],
  1, '"So that" expresses purpose for the postponement.');
add(6, 'Her explanation failed to _____ the panel\'s doubts about the data.',
  ['aggravate', 'allay', 'amplify', 'announce'],
  1, 'Allay means to diminish or put to rest (fears/doubts).');
add(6, 'The policy was revised _____ feedback from frontline employees.',
  ['in spite of', 'in light of', 'instead of ignoring', 'regardless without'],
  1, '"In light of" means considering / because of.');
add(6, 'Efficient filing systems help clerks retrieve records with minimal _____.',
  ['delay', 'clarity', 'accuracy', 'legibility'],
  0, 'Good systems reduce delay in retrieval.');
add(6, 'The mayor emphasized that disaster drills are not optional but _____.',
  ['discretionary', 'mandatory', 'decorative', 'theoretical only'],
  1, 'Mandatory means required by rules or law.');

// ========== VERBAL — Error recognition (7) ==========
add(7, 'Identify the sentence with a grammatical error.',
  ['One of the applicants has incomplete papers.', 'Neither the manager nor the clerks was informed.', 'The number of complaints have increased this month.', 'She, as well as her colleagues, supports the reform.'],
  2, '"The number" is singular; use "has increased," not "have."');
add(7, 'Which sentence contains an error?',
  ['The data suggest a clear trend.', 'Between you and I, the plan needs work.', 'Everybody is ready for the briefing.', 'Fewer errors appeared in the revised draft.'],
  1, 'Correct pronoun: "Between you and me" (object of preposition).');
add(7, 'Choose the sentence with incorrect subject-verb agreement.',
  ['Mathematics is challenging for many students.', 'The committee have reached different private opinions but issues one report.', 'There are several options on the table.', 'News is broadcast daily.'],
  1, 'As a collective acting as one body issuing one report, "committee" often takes singular in formal AmE; the error intended is informal mismatch — better: "The scissors is..." Actually fix: use classic error.',
  ); // will fix - wait I made a bad one

// Fix last - remove and re-add properly by not using that broken one
Q.pop();
add(7, 'Choose the sentence with incorrect subject-verb agreement.',
  ['Mathematics is challenging for many students.', 'Each of the reports need further review.', 'There are several options on the table.', 'News is broadcast daily.'],
  1, '"Each" is singular; use "needs," not "need."');
add(7, 'Which sentence has a pronoun error?',
  ['Everyone should bring his or her ID.', 'The team submitted their joint proposal.', 'If a person works hard, they will succeed eventually. (informal)', 'Me and him will attend the orientation.'],
  3, 'Subject pronouns needed: "He and I will attend..."');
add(7, 'Identify the erroneous sentence.',
  ['She speaks both English and Filipino fluently.', 'He don\'t know the deadline.', 'They have already left the office.', 'We were informed yesterday.'],
  1, 'Third-person singular: "He doesn\'t know..."');
add(7, 'Which sentence uses a wrong comparative form?',
  ['This form is simpler than the old one.', 'She is the most qualified among the three.', 'This approach is more better than the last.', 'Our office is farther from the hall than yours.'],
  2, '"More better" is a double comparative; use "better."');
add(7, 'Choose the sentence with a misplaced modifier problem.',
  ['Walking to the office, Ana reviewed her notes.', 'Covered in dust, the clerk filed the old folders carefully.', 'Running late, the report was submitted by the staff.', 'After the meeting, they clarified the agenda.'],
  2, 'The report was not running late; the modifier dangles. Better: "Running late, the staff submitted the report."');

// ========== VERBAL — Sentence structure (8) ==========
add(8, 'A compound sentence typically contains:',
  ['One independent clause only', 'Two or more independent clauses joined appropriately', 'Only dependent clauses', 'A title without a verb'],
  1, 'Compound sentences join independent clauses (e.g., with coordinating conjunctions).');
add(8, 'Which is a complex sentence?',
  ['The clerk filed the papers.', 'The clerk filed the papers, and the manager signed them.', 'Although the clerk filed the papers, the manager requested revisions.', 'File. Sign. Archive.'],
  2, 'A complex sentence has an independent clause plus at least one dependent clause ("Although...").');
add(8, 'Parallel structure is correctly used in:',
  ['She likes hiking, to swim, and biking.', 'She likes hiking, swimming, and biking.', 'She likes hike, swimming, and to bike.', 'She likes hiking, swim, and biked.'],
  1, 'Parallel gerunds: hiking, swimming, and biking.');
add(8, 'A run-on sentence is best corrected by:',
  ['Adding more unrelated clauses without punctuation', 'Using proper punctuation or conjunctions to separate independent clauses', 'Removing all verbs', 'Writing only fragments'],
  1, 'Run-ons need correct separation/joining of independent clauses.');
add(8, 'Which option is a sentence fragment?',
  ['The training starts at nine.', 'Because the documents were incomplete.', 'Please submit your forms today.', 'Who will lead the briefing?'],
  1, '"Because..." alone is a dependent clause fragment.');
add(8, 'Active voice is illustrated by:',
  ['The report was written by the analyst.', 'The analyst wrote the report.', 'The report has been being written.', 'Writing of the report was done.'],
  1, 'Active: subject performs the action — "The analyst wrote..."');

// ========== VERBAL — Paragraph organization (9) ==========
add(9, 'The topic sentence of a paragraph usually:',
  ['Hides the main idea until the last footnote', 'States the main idea the paragraph develops', 'Lists only unrelated examples', 'Must be a question always'],
  1, 'A topic sentence presents the paragraph\'s controlling idea.');
add(9, 'Coherence in a paragraph is improved by:',
  ['Random jumps between unrelated topics', 'Logical order and clear transitions', 'Repeating the same sentence ten times', 'Omitting all examples'],
  1, 'Coherence comes from logical sequencing and transitional devices.');
add(9, 'Which order best fits a process paragraph?',
  ['Random steps', 'Chronological or sequential steps', 'Alphabetical only by author surname', 'Reverse of conclusion first without setup always'],
  1, 'Process writing typically follows chronological/sequential order.');
add(9, 'A concluding sentence often:',
  ['Introduces an entirely new topic without link', 'Restates or wraps up the paragraph\'s idea', 'Deletes the topic sentence retroactively', 'Must apologize for the content'],
  1, 'Conclusions reinforce or close the paragraph\'s point.');
add(9, 'Unity in a paragraph means:',
  ['All sentences support one main idea', 'Each sentence discusses a different subject', 'No examples are allowed', 'Only questions are used'],
  0, 'Unity requires relevance of all sentences to one controlling idea.');
add(9, 'Transitional words like "however" and "therefore" help show:',
  ['Font size', 'Logical relationships between ideas', 'Page margins', 'Speaker volume'],
  1, 'Transitions signal contrast, cause-effect, addition, etc.');

// ========== VERBAL — Reading comprehension (10) ==========
add(10, 'Passage: "Open data portals allow citizens to examine government spending." The author\'s main point is that open data:',
  ['Prevents all corruption automatically', 'Helps citizens scrutinize how public funds are used', 'Replaces the need for elections', 'Applies only to private banks'],
  1, 'The sentence links open data to citizen examination of spending.');
add(10, 'Passage: "Training without follow-up coaching yields short-lived gains." An inference is that:',
  ['Coaching after training can help sustain improvements', 'Training is useless in all cases', 'Coaching replaces all training', 'Gains never occur'],
  0, 'If lack of follow-up shortens gains, coaching after training likely helps sustain them.');
add(10, 'Passage: "Flood-prone barangays updated their evacuation maps yearly." This suggests the maps are:',
  ['Never used', 'Treated as living documents needing periodic revision', 'Illegal', 'Only decorative'],
  1, 'Yearly updates imply maps are maintained and revised over time.');
add(10, 'Passage: "Merit-based hiring strengthens public trust in bureaucracy." Which restatement is best?',
  ['Hiring by connections always builds trust', 'Selecting officials based on qualifications can increase confidence in government', 'Bureaucracy should ignore merit', 'Trust is unrelated to hiring'],
  1, 'Merit-based selection is linked to stronger public trust.');
add(10, 'Passage: "Digital literacy gaps widen inequality in accessing e-government services." The problem highlighted is:',
  ['Printer ink costs only', 'Unequal ability to use digital tools limiting access to services', 'Too many service centers downtown', 'Excess paper forms exclusively'],
  1, 'Digital literacy gaps create unequal access to online government services.');
add(10, 'Passage: "Evidence-based policy relies on data rather than anecdotes alone." The author contrasts:',
  ['Data-informed decisions vs. story-only decisions', 'Anecdotes vs. poetry', 'Policy vs. law dictionaries', 'Servers vs. desktops'],
  0, 'The contrast is between data/evidence and anecdote-only approaches.');
add(10, 'If a passage states a rule and an exception, a careful reader should:',
  ['Ignore the exception', 'Note both the general rule and the stated exception', 'Assume no exceptions ever exist', 'Skip to the title only'],
  1, 'Accurate comprehension includes both the rule and any stated exceptions.');
add(10, 'Passage: "Community feedback shortened the permit process by two days." A reasonable conclusion is that:',
  ['Feedback had no effect', 'Stakeholder input contributed to process improvement', 'Permits were abolished', 'Two days were added'],
  1, 'The stated result links feedback to a shorter process.');


// ========== ANALYTICAL — Word analogy (11) ==========
add(11, 'Judge is to Court as Physician is to:',
  ['Hospital', 'Medicine bottle', 'Ambulance siren', 'Prescription pad only'],
  0, 'A judge works in a court; a physician commonly works in a hospital.');
add(11, 'Author is to Book as Composer is to:',
  ['Concert hall', 'Symphony', 'Instrument case', 'Audience'],
  1, 'An author produces a book; a composer produces a musical work such as a symphony.');
add(11, 'Vaccine is to Prevention as Antibiotic is to:',
  ['Diagnosis only', 'Treatment of bacterial infection', 'Surgery theater', 'X-ray film'],
  1, 'Vaccines prevent disease; antibiotics treat bacterial infections.');
add(11, 'Blueprint is to Building as Agenda is to:',
  ['Meeting', 'Calendar app icon', 'Coffee break', 'Name tag'],
  0, 'A blueprint guides construction; an agenda guides a meeting.');
add(11, 'Archipelago is to Islands as Constellation is to:',
  ['Planets only', 'Stars', 'Oceans', 'Comets exclusively'],
  1, 'An archipelago is a group of islands; a constellation is a group of stars.');
add(11, 'Librarian is to Catalog as Accountant is to:',
  ['Ledger', 'Bookshelf', 'Barcode', 'Reading lamp'],
  0, 'Librarians organize via catalogs; accountants organize via ledgers.');
add(11, 'Drought is to Scarcity as Flood is to:',
  ['Abundance of water / excess', 'Desertification only', 'Evaporation', 'Irrigation canal'],
  0, 'Drought relates to scarcity of water; flood relates to excess water.');
add(11, 'Hypothesis is to Experiment as Verdict is to:',
  ['Trial', 'Lawyer briefcase', 'Courtroom sketch', 'Bail bond'],
  0, 'A hypothesis is tested by experiment; a verdict results from a trial.');
add(11, 'Filter is to Purification as Audit is to:',
  ['Verification / accountability check', 'Celebration', 'Decoration', 'Translation only'],
  0, 'Filtering purifies; auditing verifies accountability.');
add(11, 'Scout is to Reconnaissance as Spy satellite is to:',
  ['Surveillance', 'Agriculture subsidy', 'Postal sorting', 'Museum tour'],
  0, 'Scouts perform reconnaissance; spy satellites perform surveillance.');

// ========== ANALYTICAL — Symbolic logic / abstract (12) ==========
add(12, 'If all A are B, and some B are C, which must be true?',
  ['All A are C', 'Some A may or may not be C; not determined from given alone', 'No A are C', 'All C are A'],
  1, 'From all A are B and some B are C, the relation of A to C is not forced.');
add(12, 'Statement: If it rains, the event is moved indoors. It did not rain. Therefore:',
  ['The event must have been outdoors', 'We cannot conclude the event location from this alone', 'The event was canceled', 'It must have flooded'],
  1, 'Denying the antecedent does not validly deny the consequent.');
add(12, 'Which pair is the odd one out by pattern: 2A, 4C, 6E, 9G?',
  ['2A', '4C', '6E', '9G'],
  3, 'Numbers increase by +2 and letters skip one; 9 breaks the +2 number pattern (should be 8G).');
add(12, 'Complete the series: AZ, BY, CX, _____',
  ['DW', 'EV', 'DU', 'CW'],
  0, 'First letters A,B,C,D; second letters Z,Y,X,W yielding DW.');
add(12, 'If triangle means addition and circle means subtraction, then 8 triangle 3 circle 2 equals:',
  ['9', '13', '3', '6'],
  0, '8+3-2 = 9.');
add(12, 'All managers are employees. Some employees are engineers. Which is valid if at least one manager exists?',
  ['All managers are engineers', 'Some managers are definitely engineers', 'Some employees are managers', 'No employees are managers'],
  2, 'Each manager is an employee, so some employees are managers.');
add(12, 'Find the next in pattern: circle, square, circle, square, circle, _____',
  ['Square', 'Triangle', 'Pentagon', 'Line'],
  0, 'Alternating circle/square continues with square.');
add(12, 'Which conclusion follows? Only citizens may vote. Alex voted.',
  ['Alex is a citizen', 'Alex is a government employee', 'Alex is over 60', 'Alex owns land'],
  0, 'If only citizens may vote and Alex voted, Alex must be a citizen.');
add(12, 'Code: FIRE = 1234, LIFE = 5124. Then LIE could be:',
  ['514', '152', '512', '124'],
  0, 'L=5, I=1, E=4 so LIE = 514.');
add(12, 'If the first two are true, is the third necessarily true? (1) All roses are flowers. (2) Some flowers fade quickly. (3) Some roses fade quickly.',
  ['Yes, necessarily', 'No, not necessarily', 'Yes only if all flowers are roses', 'Cannot read'],
  1, 'Some flowers fading does not force roses to be among those that fade.');

// ========== ANALYTICAL — Assumptions / conclusions (13) ==========
add(13, 'Argument: We should hire more clerks because queues are long. An unstated assumption is that:',
  ['Long queues are unrelated to staffing', 'Additional clerks would help reduce queue length', 'Queues are preferred by clients', 'Hiring is free'],
  1, 'The recommendation assumes more clerks would address the queue problem.');
add(13, 'All eligible applicants submitted forms on time. Ben did not submit on time. Conclusion:',
  ['Ben is eligible', 'Ben is not an eligible applicant under the given rule', 'Ben will be hired', 'Ben submitted early'],
  1, 'By contraposition, not on time implies not among those eligible applicants described.');
add(13, 'Which is a value judgment rather than a factual claim?',
  ['The office processed 120 applications yesterday', 'Transparency is more important than speed in this case', 'The building has five floors', 'The meeting starts at 9:00 a.m.'],
  1, 'Calling one value more important is a normative judgment.');
add(13, 'Survey: 70% of respondents support flex-time. Strongest caution?',
  ['Sample may not represent the whole workforce', 'Percentages are never useful', 'Flex-time is illegal always', 'Surveys cannot ask about time'],
  0, 'Representativeness of the sample limits generalization.');
add(13, 'If whenever inventory is low, orders are placed, and orders were not placed, then:',
  ['Inventory must be low', 'Inventory is not low', 'Suppliers failed', 'Prices rose'],
  1, 'Modus tollens: not orders implies not low inventory.');
add(13, 'Claim: Program X caused the score increase. Weakest support would be:',
  ['Randomized controlled comparison', 'Anecdote from one participant only', 'Pre-post study with controls', 'Replication across sites'],
  1, 'A single anecdote is weak causal evidence.');
add(13, 'Which is a necessary assumption for Install CCTV to reduce theft?',
  ['Theft is partly deterred or detectable via CCTV', 'CCTV entertains visitors', 'Theft only happens online', 'Cameras replace locks always'],
  0, 'The policy assumes CCTV helps deter or detect theft.');
add(13, 'Premises: Either the file is in Cabinet A or Cabinet B. It is not in Cabinet A. Conclusion:',
  ['It is in Cabinet B', 'It is lost forever', 'It is in both', 'Cabinets are empty'],
  0, 'Disjunctive syllogism yields Cabinet B.');
add(13, 'An argument attacks the speaker character instead of the claim. This fallacy is:',
  ['Ad hominem', 'Valid deduction', 'Statistical sampling', 'Analogy'],
  0, 'Ad hominem targets the person rather than the argument.');
add(13, 'After the new pavement, accidents fell; therefore pavement caused the drop. The flaw may be:',
  ['Ignoring other concurrent causes', 'Using too much data', 'Preferring experiments always illegally', 'Measuring accidents'],
  0, 'Post hoc or omitted variable issues may explain the drop.');

// ========== ANALYTICAL — Data interpretation (14) ==========
add(14, 'A chart shows Office A: 40 permits, Office B: 60 permits. Office B share of the combined total is:',
  ['40%', '50%', '60%', '66%'],
  2, '60/(40+60)=60%.');
add(14, 'Scores: 70, 80, 90. The mean is:',
  ['70', '80', '90', '240'],
  1, '(70+80+90)/3 = 80.');
add(14, 'If a pie chart shows 25% of 200 complaints are about delays, the number about delays is:',
  ['25', '50', '75', '100'],
  1, '0.25 times 200 = 50.');
add(14, 'Production rose from 120 to 150 units. The percent increase is:',
  ['20%', '25%', '30%', '80%'],
  1, '(30/120)*100% = 25%.');
add(14, 'Region X has population 2M and cases 400; Region Y has 1M and cases 300. Higher cases per million?',
  ['Region X', 'Region Y', 'Equal', 'Cannot tell'],
  1, 'X: 200 per M; Y: 300 per M so Y is higher.');
add(14, 'Median of 3, 9, 5, 7, 11 is:',
  ['3', '7', '9', '11'],
  1, 'Ordered 3,5,7,9,11; median 7.');
add(14, 'A bar shows Q1=10, Q2=15, Q3=15, Q4=20. Best description:',
  ['Steady decline all year', 'Rise then plateau then rise', 'All quarters equal', 'Only Q1 nonzero'],
  1, '10 to 15 rise; 15 plateau; 15 to 20 rise.');
add(14, 'If 3 out of 12 audited files had errors, the error rate is:',
  ['12%', '20%', '25%', '30%'],
  2, '3/12 = 25%.');
add(14, 'A line graph of wait time falls each month for six months. The trend is:',
  ['Increasing', 'Decreasing', 'Cyclical with peaks every month', 'Undefined'],
  1, 'Consistently falling values indicate a decreasing trend.');
add(14, 'Dual bar chart: male 40, female 60 in Unit 1. Female percentage in Unit 1 is:',
  ['40%', '50%', '60%', '100%'],
  2, '60/(40+60)=60%.');

// ========== NUMERICAL — Basic operations (15) ==========
add(15, 'What is 18% of 450?',
  ['72', '81', '90', '98'],
  1, '0.18 times 450 = 81.');
add(15, 'Simplify: 3/4 + 2/3',
  ['5/7', '17/12', '6/12', '1'],
  1, 'LCD 12: 9/12 + 8/12 = 17/12.');
add(15, 'Compute 125 times 0.8',
  ['90', '100', '110', '120'],
  1, '125 times 0.8 = 100.');
add(15, 'What is the value of 2 to the 5th power?',
  ['10', '16', '32', '64'],
  2, '2^5 = 32.');
add(15, 'Round 3,847 to the nearest hundred:',
  ['3,800', '3,850', '3,900', '4,000'],
  0, 'Nearest hundred for 3,847 is 3,800.');
add(15, 'Find the LCM of 6 and 8:',
  ['12', '24', '48', '14'],
  1, 'LCM(6,8)=24.');
add(15, 'Find the GCF of 36 and 54:',
  ['6', '9', '18', '27'],
  2, 'GCF(36,54)=18.');
add(15, 'Convert 0.125 to a fraction in lowest terms:',
  ['1/5', '1/8', '1/4', '3/25'],
  1, '0.125 = 1/8.');
add(15, 'If a price increases from 200 pesos to 260 pesos, the percent increase is:',
  ['25%', '30%', '60%', '130%'],
  1, '60/200 = 30%.');
add(15, 'Evaluate: 15 - 3 times 4 + 6',
  ['9', '18', '54', '6'],
  0, 'Multiplication first: 15 - 12 + 6 = 9.');
add(15, 'A ratio of 3:5 equals which fraction for the first part over total?',
  ['3/5', '3/8', '5/3', '5/8'],
  1, 'First/total = 3/8.');
add(15, 'What is 2.5% of 800?',
  ['15', '20', '25', '40'],
  1, '0.025 times 800 = 20.');

// ========== NUMERICAL — Number sequence (16) ==========
add(16, 'Find the next number: 4, 9, 16, 25, _____',
  ['30', '36', '49', '32'],
  1, 'Squares: next is 36.');
add(16, 'Find the next number: 5, 10, 20, 40, _____',
  ['60', '80', '70', '100'],
  1, 'Each term doubles: 80.');
add(16, 'Find the next: 1, 1, 2, 3, 5, 8, _____',
  ['10', '11', '13', '15'],
  2, 'Fibonacci: 5+8=13.');
add(16, 'Find the next: 81, 27, 9, 3, _____',
  ['1', '0', '2', '6'],
  0, 'Divide by 3 each time: 1.');
add(16, 'Find the missing: 2, 6, 12, 20, 30, _____',
  ['36', '40', '42', '44'],
  2, 'Differences increase by 2; next 42.');
add(16, 'Find the next: 7, 14, 28, 56, _____',
  ['84', '98', '112', '120'],
  2, 'Doubling: 112.');
add(16, 'Find the next: 3, 7, 15, 31, _____',
  ['47', '63', '62', '55'],
  1, 'Pattern times 2 plus 1: 63.');
add(16, 'Find the next: 100, 95, 85, 70, _____',
  ['50', '55', '60', '40'],
  0, 'Subtract 5,10,15,20 yielding 50.');
add(16, 'Find the next: 1, 4, 9, 16, 25, _____',
  ['30', '36', '49', '35'],
  1, 'Perfect squares: 36.');
add(16, 'Find the next: 2, 3, 5, 8, 12, _____',
  ['15', '17', '18', '20'],
  1, 'Differences +1,+2,+3,+4,+5 yielding 17.');
add(16, 'Find the next: 64, 32, 16, 8, _____',
  ['2', '4', '6', '1'],
  1, 'Halving: 4.');
add(16, 'Find the next: 11, 13, 17, 19, 23, _____',
  ['25', '27', '29', '31'],
  2, 'Primes: next is 29.');

// ========== NUMERICAL — Word problems (17) ==========
add(17, 'A train travels 180 km in 3 hours. Average speed is:',
  ['50 km/h', '60 km/h', '90 km/h', '120 km/h'],
  1, '180/3 = 60 km/h.');
add(17, 'If 5 clerks process 100 forms in 2 hours at equal rates, forms per clerk per hour is:',
  ['5', '10', '20', '25'],
  1, '100/(5*2)=10.');
add(17, 'An item costing 1200 pesos is sold at 15% discount. Sale price is:',
  ['180 pesos', '1020 pesos', '1050 pesos', '1380 pesos'],
  1, 'Discount 180; price 1020.');
add(17, 'A tank is 3/4 full. If 60 liters more fill it completely, capacity is:',
  ['180 L', '200 L', '240 L', '300 L'],
  2, 'One-fourth capacity = 60 so capacity = 240 L.');
add(17, 'Two numbers sum to 50 and differ by 8. The larger is:',
  ['21', '29', '31', '42'],
  1, 'Larger is 29.');
add(17, 'A worker earns 750 pesos/day. In 12 days with no deductions, earnings are:',
  ['8000 pesos', '9000 pesos', '9500 pesos', '7500 pesos'],
  1, '750*12=9000.');
add(17, 'Bus fare is 15 pesos. For 8 passengers paying exact fare, total collection is:',
  ['100 pesos', '120 pesos', '125 pesos', '150 pesos'],
  1, '15*8=120.');
add(17, 'A recipe needs flour:sugar = 5:2. For 35 cups flour, sugar needed is:',
  ['10', '12', '14', '20'],
  2, 'One part = 7; sugar = 14.');
add(17, 'Simple interest on 5000 pesos at 6% per year for 2 years is:',
  ['300 pesos', '600 pesos', '5600 pesos', '3000 pesos'],
  1, 'I=Prt=600.');
add(17, 'A rectangle is 12 m by 5 m. Its perimeter is:',
  ['17 m', '34 m', '60 m', '30 m'],
  1, 'Perimeter 34 m.');
add(17, 'If 8 identical packs weigh 36 kg, one pack weighs:',
  ['4 kg', '4.5 kg', '5 kg', '6 kg'],
  1, '36/8=4.5 kg.');
add(17, 'A project is 40% complete. Of the remaining work, half is done next week. Percent still unfinished after next week:',
  ['20%', '30%', '40%', '60%'],
  1, 'Remaining 60%; half done leaves 30% unfinished.');
add(17, 'Sharing 900 pesos in ratio 2:3:4, the middle share is:',
  ['200 pesos', '300 pesos', '400 pesos', '450 pesos'],
  1, 'Middle share 300.');
add(17, 'A car averages 12 km per liter. Liters needed for 180 km:',
  ['12', '15', '18', '20'],
  1, '180/12=15 liters.');

// ========== CLERICAL — Filing (18) ==========
add(18, 'In alphabetical filing, which name comes first?',
  ['Santos, Ana', 'Santos, Andres', 'Santos, Anita', 'Santos, Angelo'],
  0, 'Ana precedes the others alphabetically.');
add(18, 'Numeric filing in ascending order places which first?',
  ['101', '11', '1001', '110'],
  1, 'As numbers: 11 comes first.');
add(18, 'Subject filing groups records by:',
  ['Topic or subject matter', 'Employee birthday only', 'Ink color', 'Random lottery'],
  0, 'Subject filing organizes by topic.');
add(18, 'A tickler file is primarily used for:',
  ['Reminder or follow-up by date', 'Permanent archives only', 'Destroying records weekly', 'Storing broken stamps'],
  0, 'Tickler files prompt action on future dates.');
add(18, 'Which is correct A-Z order?',
  ['Brown, Browne, Browning', 'Browne, Brown, Browning', 'Browning, Brown, Browne', 'Brown, Browning, Browne'],
  0, 'Brown, then Browne, then Browning.');
add(18, 'Cross-referencing in filing helps when:',
  ['A record may be sought under more than one title', 'Only one title ever exists', 'Folders must stay empty', 'Dates are banned'],
  0, 'Cross-references guide retrieval under alternate captions.');
add(18, 'Outgoing correspondence is often filed by:',
  ['Name of addressee or subject per office rules', 'Weather on mailing day', 'Stamp price only', 'Courier shoe size'],
  0, 'Offices typically file by correspondent name or subject.');
add(18, 'Chronological filing arranges records by:',
  ['Date order', 'Author shoe size', 'Random hash only', 'Ink brand'],
  0, 'Chronological means by date.');

// ========== CLERICAL — Spelling (19) ==========
add(18, 'Which comes last alphabetically among Lopez given names Ana, Beatriz, Carla, Diana?',
  ['Lopez, Ana', 'Lopez, Beatriz', 'Lopez, Carla', 'Lopez, Diana'],
  3, 'Diana is last among the given names.');
add(19, 'Choose the correctly spelled word:',
  ['Accomodate', 'Accommodate', 'Acommodate', 'Acomodate'],
  1, 'Accommodate has double c and double m.');
add(19, 'Choose the correctly spelled word:',
  ['Seperate', 'Separate', 'Seperete', 'Separete'],
  1, 'Separate.');
add(19, 'Choose the correctly spelled word:',
  ['Definately', 'Definitely', 'Definitley', 'Definatly'],
  1, 'Definitely.');
add(19, 'Choose the correctly spelled word:',
  ['Occurence', 'Occurrence', 'Ocurrence', 'Occurance'],
  1, 'Occurrence.');
add(19, 'Choose the correctly spelled word:',
  ['Priviledge', 'Privilege', 'Privillage', 'Previlage'],
  1, 'Privilege.');
add(19, 'Choose the correctly spelled word:',
  ['Maintenance', 'Maintainance', 'Maintanance', 'Maintenence'],
  0, 'Maintenance.');
add(19, 'Choose the correctly spelled word:',
  ['Recieve', 'Receive', 'Receve', 'Riceive'],
  1, 'Receive.');
add(19, 'Choose the correctly spelled word:',
  ['Questionnaire', 'Questionaire', 'Questionnare', 'Questionnair'],
  0, 'Questionnaire.');

// ========== EXTRA BATCH to clear +150 unique (more GI/Verbal/Analytical/Numerical) ==========
add(1, 'The President may grant reprieves, commutations, and pardons, except in cases of:',
  ['All criminal offenses without limit', 'Impeachment', 'Traffic violations only', 'Tax evasion exclusively'],
  1, 'Pardon power generally excludes impeachment cases.');
add(1, 'Emergency powers may be delegated to the President by Congress subject to:',
  ['Permanent transfer of legislative power', 'Limitations and a defined period set by law', 'Supreme Court enactment of statutes', 'Barangay veto only'],
  1, 'Delegation of emergency powers requires statutory limits and duration.');
add(1, 'Dual allegiance of citizens is inimical to national interest and shall be dealt with by:',
  ['Local ordinances only', 'Law', 'Executive order alone without statute', 'Private contracts'],
  1, 'The Constitution provides that dual allegiance shall be dealt with by law.');
add(1, 'The Senate is composed of how many members elected at large?',
  ['12', '24', '250', '300'],
  1, 'The Senate has 24 members elected at large.');
add(2, 'Public officials shall not dispose of government property without:',
  ['Social media announcement', 'Proper authority and legal basis', 'Family consent', 'Newspaper ads only'],
  1, 'Disposition of government property requires lawful authority.');
add(2, 'Nepotism restrictions generally aim to prevent:',
  ['Merit-based promotions', 'Favoritism in appointing relatives within prohibited degrees', 'Training of staff', 'Use of email'],
  1, 'Anti-nepotism rules curb favoritism toward relatives in appointments.');
add(2, 'Ethical standards require officials to act with professionalism, which includes:',
  ['Ignoring deadlines freely', 'Competence, courtesy, and dedication to duty', 'Sharing passwords publicly', 'Skipping required reports'],
  1, 'Professionalism covers competence and proper conduct in duty.');
add(3, 'Freedom from torture is:',
  ['A derogable privilege for convenience', 'A fundamental human right that must be respected', 'Allowed during investigations always', 'Only for foreign nationals'],
  1, 'Freedom from torture is a core non-negotiable human right.');
add(3, 'Gender equality policies in public service promote:',
  ['Exclusion of one sex from all posts', 'Equal opportunities and non-discrimination', 'Quotas without any competence standards ever', 'Secret hiring only'],
  1, 'Gender equality emphasizes equal opportunity and non-discrimination.');
add(4, 'Watershed protection is important because watersheds:',
  ['Supply and regulate freshwater resources', 'Only produce oil', 'Block all rainfall', 'Replace power plants'],
  0, 'Watersheds are critical for freshwater supply and regulation.');
add(4, 'Open dumping of waste is discouraged because it:',
  ['Improves groundwater always', 'Risks pollution, disease vectors, and environmental harm', 'Is required by R.A. 9003', 'Increases recycling automatically'],
  1, 'Open dumps pose health and environmental hazards; law pushes proper management.');

add(5, 'TENACIOUS most nearly means:',
  ['Giving up easily', 'Persistent and determined', 'Fragile', 'Silent'],
  1, 'Tenacious means not readily letting go; persistent.');
add(5, 'An antonym of EXPAND is:',
  ['Enlarge', 'Contract', 'Increase', 'Amplify'],
  1, 'Contract means to shrink — opposite of expand.');
add(5, 'PLAUSIBLE most nearly means:',
  ['Impossible', 'Seemingly reasonable', 'Proven false', 'Illegal'],
  1, 'Plausible means seeming reasonable or probable.');
add(5, 'SCRUTINIZE means to:',
  ['Glance quickly and forget', 'Examine closely', 'Hide permanently', 'Celebrate'],
  1, 'To scrutinize is to inspect carefully.');
add(5, 'AMBIGUOUS language is:',
  ['Crystal clear', 'Open to more than one interpretation', 'Always mathematical', 'Illegal to print'],
  1, 'Ambiguous means having uncertain or double meaning.');

add(6, 'The spokesperson gave a _____ denial, leaving no room for doubt about the agency\'s position.',
  ['vague', 'categorical', 'hesitant', 'muted'],
  1, 'Categorical means absolute / unconditional.');
add(6, 'Innovation in service delivery should be _____ with existing legal standards.',
  ['at odds always', 'aligned', 'ignorant of', 'hostile to'],
  1, 'Aligned means consistent with standards.');
add(6, 'The findings were _____ by a second independent review.',
  ['contradicted without data', 'corroborated', 'erased', 'ignored'],
  1, 'Corroborated means confirmed by additional evidence.');
add(6, 'Employees were asked to _____ from making public comments on the pending case.',
  ['refrain', 'insist', 'amplify', 'broadcast'],
  0, 'Refrain from = hold back from doing.');

add(7, 'Identify the sentence with an error in article usage.',
  ['She is an honest official.', 'He is a university scholar.', 'They visited an European museum exhibit.', 'It was an honor to serve.'],
  2, 'European begins with a consonant sound /j/; use "a European."');
add(7, 'Which sentence has a tense error?',
  ['By tomorrow, we will have finished the audit.', 'Yesterday she submit the forms.', 'They have worked here since 2019.', 'He is preparing the slides now.'],
  1, 'Past: "submitted," not "submit."');
add(7, 'Choose the sentence with a preposition error.',
  ['She is good at analysis.', 'Discuss about the agenda thoroughly is required. (as written)', 'He arrived at the office early.', 'They depend on accurate data.'],
  1, '"Discuss" does not take "about" — "Discuss the agenda..."');

add(8, 'Which option correctly combines clauses without a comma splice?',
  ['The forms arrived, they were incomplete.', 'The forms arrived; they were incomplete.', 'The forms arrived they were incomplete.', 'The forms arrived, and incomplete.'],
  1, 'A semicolon (or period/conjunction) correctly joins related independent clauses.');
add(8, 'A relative clause is introduced by words such as:',
  ['and / but only', 'who / which / that', 'therefore alone', 'etc. only'],
  1, 'Relative pronouns/adverbs like who, which, that introduce relative clauses.');

add(9, 'When arranging sentences into a coherent paragraph, place background before:',
  ['Unrelated jokes only', 'Specific supporting details that rely on that background', 'Deleting the topic', 'Ending punctuation rules'],
  1, 'General/background context usually precedes dependent details.');
add(9, 'Chronological markers like "first," "then," and "finally" signal:',
  ['Spatial description only', 'Time order', 'Cause without sequence', 'Font changes'],
  1, 'These markers indicate sequence in time.');

add(10, 'Passage: "Citizen charters publish service standards and timeframes." A reader can infer agencies aim to:',
  ['Hide performance expectations', 'Make service expectations clearer to the public', 'Abolish all services', 'Replace laws with posters'],
  1, 'Publishing standards increases clarity of what citizens can expect.');
add(10, 'Passage: "When instructions are ambiguous, error rates rise." The implied relationship is:',
  ['Ambiguity → higher errors', 'Errors → clearer instructions always', 'No relationship', 'Ambiguity reduces errors'],
  0, 'Ambiguous instructions are linked to higher error rates.');

add(11, 'Key is to Lock as Password is to:',
  ['Account access control', 'Keyboard only', 'Monitor', 'Mouse pad'],
  0, 'A key opens/secures a lock; a password controls account access.');
add(11, 'Seed is to Tree as Foundation is to:',
  ['Building', 'Roof tile only', 'Window', 'Paint'],
  0, 'A seed grows into a tree; a foundation underlies a building.');
add(11, 'Scalpel is to Surgeon as Mallet is to:',
  ['Judge (ceremonial gavel association) / carpenter tool user', 'Pilot', 'Chef exclusively', 'Librarian'],
  0, 'Tool-to-professional associations: scalpel–surgeon; mallet–often carpenter (or judge\'s gavel loosely). Prefer carpenter sense in options.',
  );
Q.pop();
add(11, 'Scalpel is to Surgeon as Trowel is to:',
  ['Mason / bricklayer', 'Pilot', 'Accountant', 'Pharmacist'],
  0, 'A scalpel is a surgeon\'s tool; a trowel is a mason\'s tool.');
add(11, 'Odometer is to Distance as Thermometer is to:',
  ['Temperature', 'Speed only', 'Pressure exclusively', 'Time zones'],
  0, 'Odometers measure distance; thermometers measure temperature.');

add(12, 'If Monday is coded as 123455, and letters map to positions in "MONDAY" uniquely, which statement is safest?',
  ['Codes must be analyzed with a known mapping key', 'Any code equals any word', 'Codes never use digits', 'Monday has 8 letters'],
  0, 'Without a defined mapping, decode carefully from the given key.');
add(12, 'Odd one out: Triangle, Square, Pentagon, Circle',
  ['Triangle', 'Square', 'Pentagon', 'Circle'],
  3, 'Circle has no straight sides; others are polygons.');
add(12, 'If P means +, Q means ×, then 6 P 2 Q 3 =',
  ['12', '18', '24', '36'],
  0, '6 + 2 × 3 = 6 + 6 = 12 (× before +).');
add(12, 'All poets are writers. Some writers are teachers. Therefore some poets are teachers:',
  ['Necessarily true', 'Not necessarily true', 'Necessarily false', 'Meaningless'],
  1, 'Overlap between poets and teachers is not forced.');

add(13, 'Policy memo: "Ban plastic bags to cut marine litter." A critical question is:',
  ['Whether bag bans reduce marine litter in context', 'The color of bags only', 'Whether paper exists', 'Font choice'],
  0, 'Causal effectiveness of the ban is central.');
add(13, 'Which is the best counterexample to "All government websites are always online"?',
  ['A documented outage of a government site', 'A private blog offline', 'A newspaper article on gardening', 'A working private shop site'],
  0, 'One government site outage falsifies "always online."');
add(13, 'Circular reasoning occurs when:',
  ['Evidence is independent of the claim', 'The claim is restated as its own support', 'Data are tabulated', 'Samples are large'],
  1, 'Circularity uses the conclusion as a premise.');

add(14, 'Enrollment: Year1=200, Year2=250. Absolute increase is:',
  ['25', '50', '450', '20%'],
  1, '250−200=50 (absolute).');
add(14, 'If Category A is twice Category B and together they total 90, A equals:',
  ['30', '45', '60', '90'],
  2, '2x + x = 90 → x=30 → A=60.');
add(14, 'A stacked bar totals 100%. Segment heights 20, 30, 50 represent:',
  ['Equal shares', '20%, 30%, 50% shares', 'Only raw counts without percent', 'Errors always'],
  1, 'On a 100% stacked bar, heights are percentage shares.');

add(15, 'Compute 7/8 of 64:',
  ['48', '56', '60', '72'],
  1, '(7/8)×64=56.');
add(15, 'What is the square root of 196?',
  ['12', '13', '14', '16'],
  2, '14×14=196.');
add(15, 'Convert 3.5 hours to minutes:',
  ['180', '200', '210', '240'],
  2, '3.5×60=210 minutes.');
add(15, 'A number increased by 20% becomes 180. The original number is:',
  ['144', '150', '160', '216'],
  1, '1.2x=180 → x=150.');

add(16, 'Find the next: 10, 11, 13, 16, 20, _____',
  ['24', '25', '26', '30'],
  1, 'Differences +1,+2,+3,+4,+5 → 20+5=25.');
add(16, 'Find the next: 1, 2, 6, 24, _____',
  ['48', '96', '120', '100'],
  2, '×2,×3,×4,×5 → 24×5=120.');
add(16, 'Find the next: 9, 16, 25, 36, _____',
  ['42', '45', '49', '64'],
  2, 'Squares: 3^2…7^2=49.');

add(17, 'Three printers print 90 pages in 15 minutes at equal speed. Pages from one printer in 10 minutes:',
  ['10', '15', '20', '30'],
  2, 'Each does 30 pages in 15 min → 2 pages/min → 20 in 10 min.');
add(17, 'A laptop priced ₱30,000 has 12% VAT included. VAT amount is approximately:',
  ['₱3,214', '₱3,600', '₱2,800', '₱4,000'],
  0, 'Price = base×1.12 → base=30000/1.12≈26786; VAT≈3214.');
add(17, 'Walking 4 km/h, time to walk 10 km is:',
  ['2 hours', '2.5 hours', '3 hours', '4 hours'],
  1, '10/4=2.5 hours.');
add(17, 'Mixture: 2 liters of 10% solution + 3 liters of 20% solution. Resulting concentration:',
  ['14%', '15%', '16%', '18%'],
  2, 'Solute: 0.2+0.6=0.8 L in 5 L → 16%.');

add(18, 'Chronological filing arranges records by:',
  ['Date order', 'Author shoe size', 'Random hash only', 'Ink brand'],
  0, 'Chronological = by date.');
add(18, 'Which comes last alphabetically?',
  ['Lopez, Ana', 'Lopez, Beatriz', 'Lopez, Carla', 'Lopez, Diana'],
  3, 'Diana is last among the given given names.');

add(19, 'Choose the correctly spelled word:',
  ['Bureaucracy', 'Bureacracy', 'Beaurocracy', 'Burocracy'],
  0, 'Bureaucracy.');
add(19, 'Choose the correctly spelled word:',
  ['Consensus', 'Concensus', 'Consencus', 'Concenssus'],
  0, 'Consensus.');

console.log('TOTAL_QUESTIONS', Q.length);

// Dedupe against existing bank prefixes
const existPath = path.join(__dirname, '_existing_stems.txt');
const existing = new Set(
  fs.existsSync(existPath)
    ? fs.readFileSync(existPath, 'utf8').split(/\r?\n/).map((s) => s.trim().toLowerCase()).filter(Boolean)
    : []
);

function prefix(stem) {
  return stem.toLowerCase().replace(/\s+/g, ' ').trim().slice(0, 60);
}

const seen = new Set();
const unique = [];
let skippedDup = 0;
for (const q of Q) {
  const pfx = prefix(q.stem);
  let hit = false;
  for (const e of existing) {
    if (!e) continue;
    if (pfx.slice(0, 48) === e.slice(0, 48) || e.slice(0, 48) === pfx.slice(0, 48)) {
      hit = true;
      break;
    }
  }
  if (hit || seen.has(pfx.slice(0, 48))) {
    skippedDup++;
    continue;
  }
  seen.add(pfx.slice(0, 48));
  unique.push(q);
}

function sqlEscape(s) {
  return String(s).replace(/'/g, "''");
}

const lines = [];
lines.push('-- CIVIO/Hiraya local bank expansion — CSE-style practice (NOT official CSC exam items)');
lines.push('-- Append-only; generated ' + new Date().toISOString());
lines.push('BEGIN;');
for (const q of unique) {
  const opts = JSON.stringify(q.options);
  lines.push(
    `INSERT INTO questions (subcategory_id, language, stem, options, correct_option, explanation, status, created_by, created_at, updated_at) VALUES (${q.sub}, '${sqlEscape(q.lang)}', '${sqlEscape(q.stem)}', '${sqlEscape(opts)}'::jsonb, ${q.correct}, '${sqlEscape(q.expl)}', 'active', ${CREATED_BY}, NOW(), NOW());`
  );
}
lines.push('COMMIT;');
lines.push(`-- inserted_unique=${unique.length} skipped_near_dup=${skippedDup} raw=${Q.length}`);

const outSql = path.join(__dirname, 'seed_unique_cse_batch_2026-09-30.sql');
fs.writeFileSync(outSql, lines.join('\n') + '\n', 'utf8');
console.log('Wrote', outSql);
console.log('INSERT_COUNT', unique.length, 'SKIPPED', skippedDup);

