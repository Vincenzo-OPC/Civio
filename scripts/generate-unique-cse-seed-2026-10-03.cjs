/**
 * Local Civio bank expansion — original CSE-style practice only.
 * Adds 80 new items (clerical priority, then analytical and numerical).
 * Generates an append-only SQL seed with exact-stem protection.
 */
const fs = require('fs');
const path = require('path');

const CREATED_BY = 1;
const Q = [];

function add(sub, stem, options, correct, expl, lang = 'English') {
  if (!Array.isArray(options) || options.length !== 4) throw new Error(`expected 4 options: ${stem}`);
  if (correct < 0 || correct > 3) throw new Error(`bad correct option: ${stem}`);
  if (!stem.trim() || !expl.trim()) throw new Error(`empty stem/explanation: ${stem}`);
  Q.push({ sub, lang, stem: stem.trim(), options, correct, expl: expl.trim() });
}

// ========== CLERICAL — Filing / alphabetizing / indexing (18) ==========
add(18, 'Which file order is correct when arranging surnames alphabetically?',
  ['Cruz, Ana; Cruz, Ben; Cruz, Carlo; Cruz, Dina', 'Cruz, Carlo; Cruz, Ana; Cruz, Dina; Cruz, Ben', 'Cruz, Ben; Cruz, Dina; Cruz, Ana; Cruz, Carlo', 'Cruz, Dina; Cruz, Carlo; Cruz, Ben; Cruz, Ana'],
  0, 'Compare the given names after the identical surname; Ana, Ben, Carlo, Dina are in alphabetical order.');
add(18, 'Which sequence correctly files these surnames?',
  ['Abad', 'Abalos', 'Aquino', 'Arce'],
  0, 'Compare the surnames from left to right: Abad, Abalos, Aquino, and Arce are in ascending alphabetic order.');
add(18, 'Under alphabetic filing, which comes immediately before “Reyes, Maria”?',
  ['Reyes, Mark', 'Reyes, Luis', 'Rivera, Ana', 'Robles, Ana'],
  1, 'Within the Reyes surname group, Luis precedes Maria because L comes before M.');
add(18, 'Which sequence correctly files the surnames Delos Santos, Dela Cruz, Del Mundo, and Del Rosario?',
  ['Dela Cruz; Del Mundo; Del Rosario; Delos Santos', 'Del Mundo; Dela Cruz; Delos Santos; Del Rosario', 'Delos Santos; Del Rosario; Del Mundo; Dela Cruz', 'Del Rosario; Delos Santos; Dela Cruz; Del Mundo'],
  0, 'Ignore spaces for the comparison and compare letter by letter: Dela, Del M, Del R, Delos.');
add(18, 'When filing personal names, which is the primary filing unit in “Garcia, Noel”?',
  ['Noel', 'Garcia', 'The middle initial only', 'The person’s job title'],
  1, 'In standard alphabetic name filing, the surname is the primary unit, followed by the given name.');
add(18, 'Which number-file order is ascending?',
  ['104; 14; 41; 401', '14; 41; 104; 401', '41; 14; 401; 104', '401; 104; 41; 14'],
  1, 'Ascending numeric order compares numerical value: 14, 41, 104, 401.');
add(18, 'A folder labeled “2026-004” should be filed before:',
  ['2025-120', '2026-003', '2026-010', '2026-001'],
  2, 'In year-number filing, 2026-004 precedes 2026-010 but follows earlier 2026 and all 2025 records.');
add(18, 'Which is the correct chronological order for the dates?',
  ['15 Mar 2026; 02 Jan 2026; 28 Feb 2026; 01 Apr 2026', '02 Jan 2026; 28 Feb 2026; 15 Mar 2026; 01 Apr 2026', '01 Apr 2026; 15 Mar 2026; 28 Feb 2026; 02 Jan 2026', '28 Feb 2026; 02 Jan 2026; 01 Apr 2026; 15 Mar 2026'],
  1, 'Chronological filing runs from the earliest calendar date to the latest: January, February, March, April.');
add(18, 'For a subject filing system, where should a memo on “Leave Credits” be placed?',
  ['Under L, before “Leave Application”', 'Under A, because application is a form', 'Under C, because credits are numbers', 'At the end of the cabinet regardless of subject'],
  0, 'Subject filing uses the principal subject; “Leave Credits” belongs under L and is compared with other Leave entries.');
add(18, 'Which cross-reference is most useful when a record may be requested under two subjects?',
  ['A note directing the user from the secondary subject to the primary file', 'A second unmarked copy in a random drawer', 'Deleting the primary file', 'Changing the record number each time'],
  0, 'A cross-reference points from an alternate access point to the official primary file without creating confusion.');
add(18, 'In terminal-digit filing of 12-34-56, which pair is read first?',
  ['12', '34', '56', 'The digits are ignored'],
  2, 'Terminal-digit filing uses the rightmost digit group as the primary key, so 56 is read first.');
add(18, 'Which filing label is clearest for a folder containing approved travel claims for May 2026?',
  ['May', 'Approved Travel Claims — May 2026', 'Claims', 'Old papers'],
  1, 'A useful label identifies the subject, status, and time period so retrieval does not depend on guesswork.');
add(18, 'A document numbered 009 belongs immediately before:',
  ['008', '010', '090', '900'],
  1, 'Numeric filing compares the values; 009 is followed by 010.');
add(18, 'Which sequence correctly files the organization names?',
  ['Bayani Foundation; Bayanihan Center; Bayview Office; Bazaars Inc.', 'Bayanihan Center; Bayani Foundation; Bazaars Inc.; Bayview Office', 'Bazaars Inc.; Bayani Foundation; Bayanihan Center; Bayview Office', 'Bayview Office; Bayanihan Center; Bayani Foundation; Bazaars Inc.'],
  1, 'Compare character by character: the shorter Bayani precedes Bayanihan; both Bay names precede Baz, and Bayview follows the Baya-n entries.');
add(18, 'For a correspondence file, the date used for chronological filing is usually the:',
  ['Date the paper was printed only', 'Date of the correspondence or action recorded', 'Date the cabinet was purchased', 'Date the clerk took lunch'],
  1, 'Chronological filing uses the document’s relevant correspondence or action date, as defined by the filing policy.');
add(18, 'Which action best prevents misfiling after a folder is removed?',
  ['Leave an out-guide showing the folder’s location and borrower', 'Move neighboring folders to a different cabinet', 'Erase the folder label', 'Place unrelated papers in the gap'],
  0, 'An out-guide records what was removed and where it went, supporting accurate refiling and follow-up.');
add(18, 'A file index should normally contain the record identifier and:',
  ['A retrieval description or subject', 'The clerk’s favorite color', 'An unrelated advertisement', 'Only the paper weight'],
  0, 'An index maps identifiers to searchable subjects or descriptions, allowing a record to be located efficiently.');
add(18, 'Which is the correct order from broadest subject to narrower subject in a subject file?',
  ['Personnel → Leave → Vacation Leave → 2026', '2026 → Vacation Leave → Leave → Personnel', 'Vacation Leave → Personnel → 2026 → Leave', 'Leave → 2026 → Personnel → Vacation Leave'],
  0, 'Subject filing commonly moves from the broad class to the specific subtopic and period.');

// ========== CLERICAL — Spelling (22) ==========
add(19, 'Which spelling correctly completes this sentence: The hotel will _____ every guest\'s request.',
  ['Accomodate', 'Acommodate', 'Accommodate', 'Accommadate'],
  2, 'Accommodate has double c and double m: ac-com-mo-date.');
add(19, 'Select the correctly spelled word for the office\'s building upkeep.',
  ['Maintenance', 'Maintainance', 'Maintenence', 'Maintanance'],
  0, 'The standard spelling is maintenance, retaining the “-tenance” ending.');
add(19, 'Which spelling is correct in the instruction “_____ the pages into separate folders”?',
  ['Separate', 'Seperate', 'Seperrate', 'Separete'],
  0, 'Separate is spelled with “par” in the middle: sep-a-rate.');
add(19, 'Which word is correctly spelled in the phrase “a special _____”?',
  ['Privilege', 'Privelege', 'Priviledge', 'Privilage'],
  0, 'Privilege is spelled p-r-i-v-i-l-e-g-e, without a d.');
add(19, 'A survey form is a _____; choose the correct spelling.',
  ['Questionnaire', 'Questionaire', 'Questionnare', 'Questioneer'],
  0, 'Questionnaire has a double n and the ending “-naire.”');
add(19, 'Choose the correct spelling in the phrase “an _____ of errors.”',
  ['Occurrence', 'Occurence', 'Occurrance', 'Ocurrence'],
  0, 'Occurrence uses double c and double r before the ending “-ence.”');
add(19, 'Which spelling is correct for a connection between parties?',
  ['Liaison', 'Liason', 'Liaision', 'Liasion'],
  0, 'The standard spelling is liaison: l-i-a-i-s-o-n.');
add(19, 'Choose the correctly spelled word for a period of one thousand years.',
  ['Millennium', 'Millenium', 'Milennium', 'Milleniun'],
  0, 'Millennium has double l and double n: mil-len-ni-um.');
add(19, 'Which spelling completes the instruction “Do not _____ the applicant”?',
  ['Embarrass', 'Embarass', 'Embarrase', 'Embarres'],
  0, 'Embarrass is spelled with double r and double s.');
add(19, 'Choose the correctly spelled word meaning careful and diligent.',
  ['Conscientious', 'Consciencious', 'Consientious', 'Conscientous'],
  0, 'Conscientious contains “sci-ent-i-ous”; the first option follows the standard spelling.');
add(19, 'Which spelling names a person who starts a business?',
  ['Entrepreneur', 'Enterpreneur', 'Entreprenuer', 'Entrepenur'],
  0, 'Entrepreneur is spelled e-n-t-r-e-p-r-e-n-e-u-r.');
add(19, 'Choose the correctly spelled word for a ranked system of levels.',
  ['Hierarchy', 'Heirarchy', 'Hierachy', 'Hierarcy'],
  0, 'Hierarchy is spelled h-i-e-r-a-r-c-h-y.');
add(19, 'Which word is correctly spelled in the phrase “an _____ component”?',
  ['Indispensable', 'Indispensible', 'Indespensable', 'Indispensabel'],
  0, 'Indispensable ends in “-able,” not “-ible.”');
add(19, 'Select the correct spelling for the word meaning varied or mixed.',
  ['Miscellaneous', 'Miscelaneous', 'Miscellanous', 'Misceallaneous'],
  0, 'Miscellaneous contains “-cellan-” and ends in “-eous.”');
add(19, 'Which spelling is correct in the sentence “A valid ID is _____”?',
  ['Necessary', 'Necesary', 'Neccessary', 'Necessery'],
  0, 'Necessary has one c and double s.');
add(19, 'Choose the correctly spelled word for a person known to you.',
  ['Acquaintance', 'Aqaintance', 'Acquaintence', 'Acquantance'],
  0, 'Acquaintance begins “acqu-” and uses the “-ance” ending.');
add(19, 'Which spelling is correct for the verb meaning to replace or take the place of?',
  ['Supersede', 'Supercede', 'Superscede', 'Supersied'],
  0, 'Supersede is the standard spelling, ending in “-sede.”');
add(19, 'Select the correct spelling for the act of restoring agreement.',
  ['Reconciliation', 'Reconcilation', 'Reconcilliation', 'Reconcilitation'],
  0, 'Reconciliation follows reconcile plus “-ation,” retaining the second i.');
add(19, 'Which spelling correctly completes “Do not _____ the total cost”?',
  ['Exaggerate', 'Exagerrate', 'Exagerate', 'Exaggerete'],
  0, 'Exaggerate has double g and ends with “-ate.”');
add(19, 'Choose the standard adverb formed from the word “public.”',
  ['Publicly', 'Publically', 'Publikly', 'Publicaly'],
  0, 'Publicly is the standard adverb; the extra “al” is unnecessary.');
add(19, 'Which spelling is correct in the phrase “I am _____ sure”?',
  ['Definitely', 'Definately', 'Definitly', 'Definetely'],
  0, 'Definitely is spelled with “finite” in the middle: de-f-i-n-i-t-e-l-y.');
add(19, 'Choose the correct spelling for the act of saying a word aloud.',
  ['Pronounciation', 'Pronunciation', 'Pronounciaton', 'Pronunciashun'],
  1, 'Pronunciation is spelled without the extra o after the n: pro-nun-ci-a-tion.');

// ========== ANALYTICAL — Word analogy (6) ==========
add(11, 'Pen is to Write as Camera is to:',
  ['Listen', 'Photograph', 'Calculate', 'Measure'],
  1, 'A pen is a tool for writing; a camera is a tool for photographing.');
add(11, 'Generous is to Giving as Cautious is to:',
  ['Careful', 'Noisy', 'Rapid', 'Decorative'],
  0, 'The relation is adjective to its defining behavior: cautious means careful.');
add(11, 'Thermometer is to Temperature as Barometer is to:',
  ['Distance', 'Pressure', 'Humidity only', 'Weight'],
  1, 'A thermometer measures temperature; a barometer measures atmospheric pressure.');
add(11, 'Blueprint is to Building as Outline is to:',
  ['Argument', 'Hammer', 'Window', 'Paint'],
  0, 'A blueprint guides construction; an outline guides development of an argument.');
add(11, 'Benevolent is to Kindness as Hostile is to:',
  ['Friendliness', 'Opposition', 'Accuracy', 'Silence'],
  1, 'Benevolent describes kindness, while hostile describes opposition or antagonism.');
add(11, 'Archive is to Preserve as Filter is to:',
  ['Separate', 'Invent', 'Publish', 'Multiply'],
  0, 'An archive preserves records; a filter separates selected material from the rest.');

// ========== ANALYTICAL — Symbolic / abstract reasoning (7) ==========
add(12, 'If A means “is greater than” and B means “is equal to,” which statement is true?',
  ['7 A 4', '3 A 9', '5 B 6', '2 A 2'],
  0, 'The symbol A means greater than, and 7 is greater than 4.');
add(12, 'If ▲ = 4 and ■ = 7, what is ▲ + ■ × ▲?',
  ['44', '32', '28', '20'],
  1, 'Apply multiplication first: 4 + (7×4) = 32.');
add(12, 'Find the missing symbol in the pattern: ○, △, ○, △, ○, __.',
  ['○', '△', '□', '◇'],
  1, 'The symbols alternate circle and triangle, so the sixth symbol is a triangle.');
add(12, 'If every coded letter is shifted one place forward, CODE becomes DPEF. Using the same rule, MATH becomes:',
  ['LZSG', 'NBUI', 'NBSI', 'MBTG'],
  1, 'Shift each letter one position forward: M→N, A→B, T→U, H→I.');
add(12, 'A sequence doubles, then subtracts one: 3, 5, 9, 17, __. What is next?',
  ['25', '31', '33', '35'],
  2, 'Each term is previous term ×2 −1: 17×2−1 = 33.');
add(12, 'Which figure property distinguishes a rectangle from a general quadrilateral?',
  ['It has four sides', 'It has four right angles', 'It has at least one vertex', 'It is a closed shape'],
  1, 'Both are quadrilaterals, but a rectangle is defined by four right angles.');
add(12, 'If the order of symbols is □, ○, △, ★ and each moves one place right cyclically, the new order is:',
  ['★, □, ○, △', '○, △, ★, □', '△, ★, □, ○', '□, ★, △, ○'],
  0, 'Moving every symbol one position right sends the last symbol to the first position.');

// ========== ANALYTICAL — Assumptions / conclusions (6) ==========
add(13, 'Claim: “The office should add a help desk because many visitors ask where to submit forms.” Which assumption is required?',
  ['Visitors would benefit from guidance at the office', 'All visitors dislike forms', 'The office will stop accepting forms', 'A help desk must be outdoors'],
  0, 'The recommendation depends on the assumption that on-site guidance would address the observed need.');
add(13, 'Statement: All approved requests have reference numbers. Request R has no reference number. What follows logically?',
  ['R is certainly approved', 'R is not shown to be an approved request', 'R must be fraudulent', 'Every request lacks a number'],
  1, 'From approved → reference number, lacking a number means approval is not established; it does not prove fraud.');
add(13, 'Argument: “The training room is full, so the next session should be held online.” The conclusion assumes that:',
  ['Online delivery can accommodate the additional participants', 'The training topic is unimportant', 'No one has internet access', 'The room will be demolished'],
  0, 'The proposed solution requires that online delivery is feasible for the participants.');
add(13, 'All archived records are indexed. File X is indexed. Which conclusion is valid?',
  ['X is definitely archived', 'X may be archived, but indexing alone does not prove it', 'No archived record is indexed', 'X is definitely destroyed'],
  1, 'The implication runs archived → indexed; the converse is not logically guaranteed.');
add(13, 'A report says response time fell after a new queue system was installed. A cautious conclusion is:',
  ['The system may have contributed to faster response', 'The system alone definitely caused every improvement', 'Response time can never change again', 'The report proves the system is unnecessary'],
  0, 'A before-and-after association supports a possible contribution, but does not establish sole causation without controls.');
add(13, 'Proposal: “Publish a checklist to reduce incomplete applications.” The strongest supporting evidence would be:',
  ['A trial showing fewer incomplete applications after checklist use', 'The checklist uses a blue cover', 'The office has many chairs', 'Applicants prefer long documents in every case'],
  0, 'Evidence directly measuring incomplete applications before and after use best supports the proposal.');

// ========== ANALYTICAL — Data interpretation (6) ==========
add(14, 'A unit processed 120, 150, and 180 requests in January, February, and March. What is the increase from January to March?',
  ['30', '50', '60', '90'],
  2, 'Subtract the endpoints: 180 − 120 = 60 requests.');
add(14, 'A budget of 80,000 is divided 25% for supplies and 15% for training. How much is allocated to both combined?',
  ['20,000', '28,000', '32,000', '40,000'],
  2, 'The combined share is 40%; 0.40 × 80,000 = 32,000.');
add(14, 'A report lists 24 completed tasks out of 30 assigned. What is the completion rate?',
  ['60%', '70%', '80%', '90%'],
  2, 'Compute 24 ÷ 30 = 0.8, which is 80%.');
add(14, 'Monthly attendance was 40, 50, 45, and 65. What was the average?',
  ['45', '48', '50', '55'],
  2, 'Sum the observations (200) and divide by four: 200 ÷ 4 = 50.');
add(14, 'A chart shows errors falling from 20 to 15 after review. The percentage decrease is:',
  ['5%', '20%', '25%', '75%'],
  2, 'Decrease is 5; relative to 20, 5/20 = 25%.');
add(14, 'Of 200 applications, 70% were complete on first submission. How many were incomplete?',
  ['30', '60', '70', '140'],
  1, 'Incomplete share is 30%; 0.30 × 200 = 60.');

// ========== NUMERICAL — Basic operations (5) ==========
add(15, 'Compute: 48 ÷ 6 + 7 × 2.',
  ['17', '22', '30', '35'],
  1, 'Use multiplication and division before addition: 48÷6 + 7×2 = 8 + 14 = 22.');
add(15, 'What is 15% of 240?',
  ['24', '30', '36', '40'],
  2, '15% = 0.15; 0.15 × 240 = 36.');
add(15, 'A clerk records 3/5 of 250 forms. How many forms is that?',
  ['100', '125', '150', '200'],
  2, '(3/5) × 250 = 3 × 50 = 150.');
add(15, 'Evaluate: 2.75 + 1.6.',
  ['3.35', '4.05', '4.35', '4.85'],
  2, 'Align decimal places: 2.75 + 1.60 = 4.35.');
add(15, 'A price of 800 is discounted by 10%. What is the sale price?',
  ['720', ' von 760', '790', '880'],
  0, 'Ten percent of 800 is 80; subtracting gives 800 − 80 = 720.');

// ========== NUMERICAL — Number sequence (5) ==========
add(16, 'Find the next number: 4, 8, 16, 32, __.',
  ['48', '56', '64', '72'],
  2, 'Each term is doubled, so 32×2 = 64.');
add(16, 'Find the next number: 2, 5, 10, 17, 26, __.',
  ['35', '36', '37', '38'],
  2, 'Differences are +3, +5, +7, +9; next is +11, giving 37.');
add(16, 'Find the next number: 81, 27, 9, 3, __.',
  ['0', '1', '2', '6'],
  1, 'Each term is divided by 3; 3 ÷ 3 = 1.');
add(16, 'Find the missing term: 6, 10, 18, 34, __.',
  ['50', '58', '66', '70'],
  2, 'Each term is previous ×2 −2: 34×2−2 = 66.');
add(16, 'Find the next number: 1, 4, 9, 16, __.',
  ['20', '24', '25', '36'],
  2, 'These are consecutive squares 1², 2², 3², 4²; next is 5² = 25.');

// ========== NUMERICAL — Word problems (5) ==========
add(17, 'A team files 18 folders per hour. At the same rate, how many folders can it file in 4 hours?',
  ['54', ' sixty-four', '72', '82'],
  2, 'Multiply the hourly rate by time: 18 × 4 = 72 folders.');
add(17, 'A 600-peso item is increased by 8%. What is the new price?',
  ['608', '624', '648', '680'],
  2, 'The increase is 0.08×600 = 48; 600 + 48 = 648.');
add(17, 'A bus travels 180 km in 3 hours. At that average speed, how far in 5 hours?',
  ['240 km', '270 km', '300 km', '360 km'],
  2, 'Speed is 180÷3 = 60 km/h; 60×5 = 300 km.');
add(17, 'A project uses 2/3 of a 45-page allowance. How many pages remain?',
  ['12', '15', '20', '30'],
  1, 'Used pages = (2/3)×45 = 30; remaining = 45−30 = 15.');
add(17, 'Five equal boxes contain 125 forms altogether. How many forms are in each box?',
  ['20', '25', '30', '35'],
  1, 'Equal division gives 125 ÷ 5 = 25 forms per box.');

if (Q.length !== 80) throw new Error(`expected 80 questions, got ${Q.length}`);
const normalizedStems = Q.map((q) => q.stem.toLowerCase().replace(/\s+/g, ' ').trim());
if (new Set(normalizedStems).size !== normalizedStems.length) throw new Error('duplicate stem inside generated batch');

function sqlEscape(s) { return String(s).replace(/'/g, "''"); }
function jsonSql(value) { return sqlEscape(JSON.stringify(value)); }

const lines = [
  '-- Civio local bank expansion — 80 original CSE-style practice items; NOT official CSC items',
  '-- Append-only with exact active-stem protection; generated ' + new Date().toISOString(),
  "SET client_encoding = 'UTF8';",
  'BEGIN;'
];
for (const q of Q) {
  const stem = sqlEscape(q.stem);
  lines.push(
    `INSERT INTO questions (subcategory_id, language, stem, options, correct_option, explanation, status, created_by, created_at, updated_at) ` +
    `SELECT ${q.sub}, '${sqlEscape(q.lang)}', '${stem}', '${jsonSql(q.options)}'::jsonb, ${q.correct}, '${sqlEscape(q.expl)}', 'active', ${CREATED_BY}, NOW(), NOW() ` +
    `WHERE NOT EXISTS (SELECT 1 FROM questions WHERE status='active' AND lower(btrim(stem))=lower(btrim('${stem}')));`
  );
}
lines.push('COMMIT;');
lines.push(`-- generated_items=${Q.length}`);

const outSql = path.join(__dirname, 'seed_unique_cse_batch_2026-10-03.sql');
fs.writeFileSync(outSql, lines.join('\n') + '\n', 'utf8');
console.log('TOTAL_QUESTIONS', Q.length);
console.log('Wrote', outSql);
