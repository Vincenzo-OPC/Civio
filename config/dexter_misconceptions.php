<?php

/*
 * Dexter misconception taxonomy (deterministic, no AI).
 *
 * Codes are the distractor codes from docs/CSE-Question-Design-Spec.md section 3,
 * so bank items tagged under the spec map one-to-one. Learner text names the
 * likely mistake and the method; it never says the learner "doesn't know" a topic.
 * `remedial_skill` points at an archetype in config/dexter_skill_graph.php.
 *
 * Bump `version` whenever a code, label or mapping changes.
 */
return [
    'version' => '2026-10-22.1',

    'codes' => [
        // Numerical (spec 3.1)
        'NUM-PARTIAL' => ['domain' => 'numerical', 'label' => 'Stopped one step early', 'method' => 'Reread the question: what quantity does it ask for? Finish every step before choosing.', 'remedial_skill' => null],
        'NUM-EXTRA-STEP' => ['domain' => 'numerical', 'label' => 'Did one step too many', 'method' => 'Stop when you reach the quantity the question names. Check the units of your answer.', 'remedial_skill' => null],
        'NUM-WRONG-BASE' => ['domain' => 'numerical', 'label' => 'Took the percent of the wrong number', 'method' => 'The base is the number after "of", or the original value before a change.', 'remedial_skill' => 'NUM-PCT-BASIC'],
        'NUM-PCT-ADD' => ['domain' => 'numerical', 'label' => 'Added percents instead of chaining them', 'method' => 'Apply each change to the new amount: multiply by (1 + rate) each time.', 'remedial_skill' => 'NUM-WP-PCT-CHANGE'],
        'NUM-OP-SWAP' => ['domain' => 'numerical', 'label' => 'Used the opposite operation', 'method' => 'Say the relation in words first ("per", "times as many", "shared among"), then pick the operation.', 'remedial_skill' => 'NUM-OPS-ORDER'],
        'NUM-ORDER-OPS' => ['domain' => 'numerical', 'label' => 'Worked left to right instead of using order of operations', 'method' => 'Parentheses, then exponents, then multiply/divide left to right, then add/subtract left to right.', 'remedial_skill' => 'NUM-OPS-ORDER'],
        'NUM-DECIMAL' => ['domain' => 'numerical', 'label' => 'Shifted the decimal point', 'method' => 'Estimate first (round the numbers), then check your answer has the right size.', 'remedial_skill' => 'NUM-FRAC-DEC'],
        'NUM-UNIT' => ['domain' => 'numerical', 'label' => 'Forgot a unit conversion', 'method' => 'Write units beside each number and convert before calculating.', 'remedial_skill' => 'NUM-WP-RATE'],
        'NUM-GIVEN-REUSED' => ['domain' => 'numerical', 'label' => 'Picked a number already in the question', 'method' => 'A number from the question is rarely the answer. Work it out, then compare.', 'remedial_skill' => null],
        'NUM-SEQ-OTHER-RULE' => ['domain' => 'numerical', 'label' => 'Used a simpler rule that does not fit every term', 'method' => 'Check the rule against every term, not just the first two. Try differences of differences, then ratios.', 'remedial_skill' => 'NUM-SEQ-DIFF'],
        'NUM-OFF-BY-ONE' => ['domain' => 'numerical', 'label' => 'Counted one too many or too few', 'method' => 'Draw a tiny case (3 posts, 2 gaps) and count, then scale up.', 'remedial_skill' => null],
        'NUM-OTHER-SHARE' => ['domain' => 'numerical', 'label' => "Answered the other person's share", 'method' => 'Underline whose amount is asked, then take that many parts.', 'remedial_skill' => 'NUM-WP-RATIO'],

        // Clerical filing (spec 3.5)
        'CLR-WORD-BY-WORD' => ['domain' => 'clerical', 'label' => 'Compared whole words instead of letters', 'method' => 'Compare unit by unit, then letter by letter within the first unit that differs.', 'remedial_skill' => 'CLR-FILE-POSITION'],
        'CLR-PREFIX-SPLIT' => ['domain' => 'clerical', 'label' => 'Treated a name prefix as a separate word', 'method' => 'Prefixes such as De, Mac, Van file as part of the surname.', 'remedial_skill' => 'CLR-FILE-POSITION'],
        'CLR-TITLE-COUNTED' => ['domain' => 'clerical', 'label' => 'Sorted by a title', 'method' => 'Ignore titles such as Dr. or Mrs. when sorting; they come last as the final unit if needed.', 'remedial_skill' => 'CLR-FILE-POSITION'],
        'CLR-ARTICLE-COUNTED' => ['domain' => 'clerical', 'label' => 'Sorted by a leading "The"', 'method' => 'A leading "The" files last, not first.', 'remedial_skill' => 'CLR-FILE-POSITION'],
        'CLR-FIRSTNAME-FIRST' => ['domain' => 'clerical', 'label' => 'Sorted by given name', 'method' => 'Personal names file by surname first, then given name.', 'remedial_skill' => 'CLR-FILE-POSITION'],
        'CLR-LETTER-ORDER' => ['domain' => 'clerical', 'label' => 'Misread the letter order', 'method' => 'Slow down at the first letter that differs and compare only that letter.', 'remedial_skill' => 'CLR-FILE-POSITION'],
        'CLR-SPELL-CORRECT-FOIL' => ['domain' => 'clerical', 'label' => 'Picked a correct word that only looks unusual', 'method' => 'Check each choice against a rule you know (doubling, ie/ei, silent letters) before deciding it is wrong.', 'remedial_skill' => 'CLR-SPELL-WRONG'],
        'CLR-COPY-MISMATCH' => ['domain' => 'clerical', 'label' => 'Missed a changed character in a copy', 'method' => 'Compare in small chunks (3-4 characters) and check digits and punctuation one by one.', 'remedial_skill' => null],

        // Spelling (spec 3.5)
        'SPL-DOUBLE' => ['domain' => 'clerical', 'label' => 'Doubled or undoubled a consonant', 'method' => 'Double the final consonant before a suffix only when the stressed syllable ends in one vowel + one consonant.', 'remedial_skill' => 'CLR-SPELL-RIGHT'],
        'SPL-IE-EI' => ['domain' => 'clerical', 'label' => 'Swapped ie and ei', 'method' => 'i before e except after c, or when sounded like "ay" (neighbor); learn the common exceptions.', 'remedial_skill' => 'CLR-SPELL-RIGHT'],
        'SPL-DROP' => ['domain' => 'clerical', 'label' => 'Left out a letter', 'method' => 'Say the word syllable by syllable and check each syllable has its letters.', 'remedial_skill' => 'CLR-SPELL-RIGHT'],
        'SPL-SOUND' => ['domain' => 'clerical', 'label' => 'Spelled it the way it sounds', 'method' => 'For -ance/-ence and -ant/-ent, link the word to a related form you know (confident/confidence).', 'remedial_skill' => 'CLR-SPELL-RIGHT'],
        'SPL-SILENT' => ['domain' => 'clerical', 'label' => 'Dropped a silent letter', 'method' => 'Link to a related word where the letter is heard (govern -> government).', 'remedial_skill' => 'CLR-SPELL-RIGHT'],
    ],
];
