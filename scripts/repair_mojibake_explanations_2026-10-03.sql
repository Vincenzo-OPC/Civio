BEGIN;
-- Repair mojibake-style quote markers and possessive apostrophes in the older local batch.
UPDATE questions
SET stem = replace(replace(stem, '???s', chr(39) || 's'), '???', chr(34)),
    explanation = replace(replace(explanation, '???s', chr(39) || 's'), '???', chr(34)),
    options = (
      SELECT jsonb_agg(to_jsonb(replace(replace(value, '???s', chr(39) || 's'), '???', chr(34))) ORDER BY ord)
      FROM jsonb_array_elements_text(options) WITH ORDINALITY AS a(value, ord)
    )
WHERE status='active' AND (stem LIKE '%???%' OR options::text LIKE '%???%' OR explanation LIKE '%???%');

UPDATE questions SET explanation = CASE id
  WHEN 1341 THEN 'Subject filing uses the principal subject, so "Leave Credits" is filed under L and compared with other Leave entries. The correct option is "Under L, before \"Leave Application\"." The other choices use the wrong subject, the wrong number, or no filing rule.'
  WHEN 1347 THEN 'Chronological filing uses the date of the correspondence or recorded action, not an incidental printing or cabinet date. The correct option is "Date of the correspondence or action recorded." The other choices do not identify the filing date of the transaction.'
  WHEN 1352 THEN 'The standard spelling is maintenance, with the letters mainten-ance. The correct option is "Maintenance." The other choices alter the vowel sequence or omit a required letter.'
  WHEN 1353 THEN 'The standard spelling is separate: sep-a-rate, with a second e after the p. The correct option is "Separate." The other choices misspell the middle vowel pattern or add an extra consonant.'
  WHEN 1355 THEN 'The standard spelling is questionnaire, with double n and the ending -naire. The correct option is "Questionnaire." The other choices omit or rearrange letters in that ending.'
  WHEN 1356 THEN 'The standard spelling is occurrence, with double c and double r before -ence. The correct option is "Occurrence." The other choices omit or misplace one of those doubled consonants.'
  WHEN 1360 THEN 'The standard spelling is conscientious, whose middle sequence is sci-ent-i and whose ending is -ous. The correct option is "Conscientious." The other choices change that sequence or omit a letter.'
  WHEN 1363 THEN 'The standard spelling is indispensable, ending in -able rather than -ible. The correct option is "Indispensable." The other choices use the wrong ending or rearrange letters.'
  WHEN 1364 THEN 'The standard spelling is miscellaneous, containing -cellan- and ending in -eous. The correct option is "Miscellaneous." The other choices omit or rearrange letters in the middle or ending.'
  WHEN 1366 THEN 'The standard spelling is acquaintance, beginning with acqu- and ending in -ance. The correct option is "Acquaintance." The other choices omit letters or use the wrong ending.'
  WHEN 1367 THEN 'The standard spelling is supersede, ending in -sede. The correct option is "Supersede." The other choices use the incorrect -cede or alter the consonants.'
  WHEN 1368 THEN 'The standard spelling is reconciliation, formed from reconcile with the ending -ation and the required i. The correct option is "Reconciliation." The other choices omit, duplicate, or replace letters.'
  WHEN 1369 THEN 'The standard spelling is exaggerate, with double g and the ending -ate. The correct option is "Exaggerate." The other choices use one g, the wrong vowel, or the wrong ending.'
  WHEN 1370 THEN 'The standard adverb is publicly; public plus -ly does not require an extra al. The correct option is "Publicly." The other choices add unnecessary letters or misspell the word.'
  WHEN 1371 THEN 'The standard spelling is definitely, containing the sequence finite. The correct option is "Definitely." The other choices change or omit letters in the middle.'
  WHEN 1380 THEN 'Use the stated values and order of operations: x plus y multiplied by x equals 4 plus 7 multiplied by 4, or 4 plus 28, which is 32. The correct option is "32." The other choices result from adding or multiplying the terms incorrectly.'
  WHEN 1382 THEN 'Shift each letter one place forward in the alphabet: M becomes N, A becomes B, T becomes U, and H becomes I. The correct option is "NBUI." The other choices shift a letter backward, leave a letter unchanged, or use the wrong alphabetic step.'
  WHEN 1383 THEN 'Apply the stated rule to 17: double 17 to get 34, then subtract 1 to get 33. The correct option is "33." The other choices do not apply both operations in the stated order.'
  WHEN 1387 THEN 'The rule says approved requests have reference numbers; it does not say that every numbered request is approved. Because R has no reference number, approval is not established. The correct option is "R is not shown to be an approved request." The other choices claim certainty or fraud that the rule does not support.'
  WHEN 1389 THEN 'The statement gives archived records as a subset of indexed records. Being indexed does not prove that File X is archived. The correct option is "X may be archived, but indexing alone does not prove it." The other choices reverse the implication or assert destruction without evidence.'
  WHEN 1391 THEN 'The strongest evidence directly compares incomplete-application rates before and after the checklist is used. The correct option is "A trial showing fewer incomplete applications after checklist use." The other choices do not measure whether the proposal works.'
  WHEN 1392 THEN 'Find the change by subtracting January from March: 180 minus 120 equals 60. The correct option is "60." The other choices use the wrong endpoint difference or report a value not supported by the data.'
  WHEN 1393 THEN 'Add the allocations first: 25 percent plus 15 percent equals 40 percent. Forty percent of 80,000 is 32,000. The correct option is "32,000." The other choices use only one percentage or apply the wrong percentage.'
  WHEN 1394 THEN 'Find how many more by subtracting Team B from Team A: 48 minus 36 equals 12. The correct option is "12." The other choices use an incorrect subtraction or add the two totals.'
  WHEN 1395 THEN 'Add the four attendance figures to get 200, then divide by 4: 200 divided by 4 equals 50. The correct option is "50." The other choices do not use the complete total or divide by the wrong count.'
  WHEN 1397 THEN 'If 70 percent are complete, 30 percent are incomplete. Thirty percent of 200 equals 60. The correct option is "60." The other choices use the complete percentage, the wrong base, or an incorrect conversion.'
  WHEN 1398 THEN 'Follow order of operations: 48 divided by 6 is 8, and 7 multiplied by 2 is 14; 8 plus 14 equals 22. The correct option is "22." The other choices ignore multiplication or division precedence or compute one operation incorrectly.'
  WHEN 1399 THEN 'Compute three-fifths of 250 by dividing 250 by 5 to get 50, then multiplying by 3 to get 150. The correct option is "150." The other choices use the wrong fraction or omit a multiplication step.'
  WHEN 1401 THEN 'A 10 percent discount on 800 is 80; subtract 80 from 800 to get 720. The correct option is "720." The other choices fail to subtract the full discount or increase the original price.'
  WHEN 1402 THEN 'Each term is doubled: 32 multiplied by 2 equals 64. The correct option is "64." The other choices do not continue the doubling pattern.'
  WHEN 1404 THEN 'Each term is divided by 3: 3 divided by 3 equals 1. The correct option is "1." The other choices do not follow the repeated division rule.'
  WHEN 1405 THEN 'Each term is multiplied by 2 and then increased by 2: 34 multiplied by 2 plus 2 equals 70, so the correct option is "70." The other choices fail to apply the recurring rule to the last term.'
  WHEN 1406 THEN 'The terms are consecutive squares: 1 squared, 2 squared, 3 squared, and 4 squared. The next is 5 squared, or 25. The correct option is "25." The other choices are not the next square in sequence.'
  WHEN 1407 THEN 'Multiply the rate by the time: 18 folders per hour multiplied by 4 hours equals 72 folders. The correct option is "72." The other choices use the wrong rate or time.'
  WHEN 1408 THEN 'Eight percent of 600 is 48; add it to the original price to get 648. The correct option is "648." The other choices omit the increase, use a different rate, or add the wrong amount.'
  WHEN 1409 THEN 'First find the speed: 180 kilometers divided by 3 hours equals 60 kilometers per hour. In 5 hours, 60 multiplied by 5 equals 300 kilometers. The correct option is "300 km." The other choices use the wrong speed or time.'
  WHEN 1410 THEN 'Two-thirds of 45 is 30, so the pages remaining are 45 minus 30, or 15. The correct option is "15." The other choices confuse pages used with pages remaining or subtract the wrong amount.'
  WHEN 1411 THEN 'Divide the total equally: 125 forms divided by 5 boxes equals 25 forms per box. The correct option is "25." The other choices do not divide the total by the number of boxes.'
  WHEN 1412 THEN 'Compute the completion rate as 24 divided by 30, which is 0.8 or 80 percent. The correct option is "80%." The other choices use an incorrect numerator, denominator, or percentage conversion.'
  ELSE explanation
END
WHERE id IN (1341,1347,1352,1353,1355,1356,1360,1363,1364,1366,1367,1368,1369,1370,1371,1380,1382,1383,1387,1389,1391,1392,1393,1394,1395,1397,1398,1399,1401,1402,1404,1405,1406,1407,1408,1409,1410,1411,1412);

UPDATE questions SET stem='If x = 4 and y = 7, what is x + (y multiplied by x)?' WHERE id=1380;
UPDATE questions SET stem='Compute: 48 divided by 6 plus 7 multiplied by 2.' WHERE id=1398;
UPDATE questions SET options='["720", "760", "790", "880"]'::jsonb WHERE id=1401;
UPDATE questions SET options='["54", "64", "72", "82"]'::jsonb WHERE id=1407;
COMMIT;
