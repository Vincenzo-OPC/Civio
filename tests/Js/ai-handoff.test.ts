import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    AI_HANDOFF_EXPLAIN_PROMPT,
    AI_HANDOFF_HINT_PROMPT,
    buildAiHandoffText,
    toPlainText,
} from '../../resources/js/lib/ai-handoff';
import type {
    AiHandoffAttemptState,
    AiHandoffQuestion,
} from '../../resources/js/lib/ai-handoff';

// Display order as the learner sees it. The bank order was
// [Removing all verbs, Using proper punctuation…, Writing only fragments,
//  Adding more unrelated clauses…]; the live exam shuffled it.
const shuffledQuestion: AiHandoffQuestion & {
    correct_option?: number;
    explanation?: string;
} = {
    stem: 'A run-on sentence is best corrected by:',
    options: [
        'Writing only fragments',
        'Using proper punctuation or conjunctions to separate independent clauses',
        'Adding more unrelated clauses without punctuation',
        'Removing all verbs',
    ],
    category: 'Verbal Ability',
    subcategory: 'Sentence Structure',
    // Present in memory on purpose: must never leak before Reveal.
    correct_option: 1,
    explanation: 'SECRET-EXPLANATION',
};

const baseAttempt: AiHandoffAttemptState = {
    mode: 'study',
    revealed: false,
    selectedDisplayIndex: 1,
    questionNumber: 3,
    totalQuestions: 30,
    examLevel: 'Subprofessional',
};

describe('buildAiHandoffText — before Reveal', () => {
    it('produces the exact clean plain-text handoff', () => {
        const text = buildAiHandoffText(shuffledQuestion, baseAttempt);

        assert.equal(
            text,
            [
                'Philippine Civil Service Exam — Subprofessional',
                'Category: Verbal Ability',
                'Topic: Sentence Structure',
                '',
                'Question:',
                'A run-on sentence is best corrected by:',
                '',
                'A. Writing only fragments',
                'B. Using proper punctuation or conjunctions to separate independent clauses',
                'C. Adding more unrelated clauses without punctuation',
                'D. Removing all verbs',
                '',
                'My answer: B',
                '',
                'Do not reveal the correct answer yet. Give me one useful hint and help me reason it out.',
            ].join('\n'),
        );
    });

    it('never leaks the answer, result or explanation even when keys are in memory', () => {
        const text = buildAiHandoffText(
            shuffledQuestion,
            {
                ...baseAttempt,
                // Even if a caller passes verified data, the flag gates it.
                verifiedCorrectDisplayIndex: 1,
                verifiedExplanation: 'SECRET-EXPLANATION',
                result: 'Correct',
                learnerNote: 'my private note',
            },
            { includeLearnerNote: true },
        );

        assert.doesNotMatch(text, /Correct answer/);
        assert.doesNotMatch(text, /Result:/);
        assert.doesNotMatch(text, /SECRET-EXPLANATION/);
        assert.doesNotMatch(text, /Civio explanation/);
        assert.doesNotMatch(text, /my private note/);
        assert.ok(text.endsWith(AI_HANDOFF_HINT_PROMPT));
    });

    it('says when nothing is answered yet and omits an empty topic', () => {
        const text = buildAiHandoffText(
            { ...shuffledQuestion, subcategory: '' },
            { ...baseAttempt, selectedDisplayIndex: undefined },
        );

        assert.match(text, /\nMy answer: not answered yet\n/);
        assert.doesNotMatch(text, /Topic:/);
    });

    it('keeps the hint prompt in strict live mode', () => {
        const text = buildAiHandoffText(shuffledQuestion, {
            ...baseAttempt,
            mode: 'live',
        });
        assert.ok(text.endsWith(AI_HANDOFF_HINT_PROMPT));
    });
});

describe('buildAiHandoffText — after Reveal and in review', () => {
    it('includes the verified answer and Civio explanation after Reveal', () => {
        const text = buildAiHandoffText(shuffledQuestion, {
            ...baseAttempt,
            revealed: true,
            verifiedCorrectDisplayIndex: 1,
            verifiedExplanation:
                'A run-on joins independent clauses without proper punctuation.',
        });

        assert.equal(
            text,
            [
                'Philippine Civil Service Exam — Subprofessional',
                'Category: Verbal Ability',
                'Topic: Sentence Structure',
                '',
                'Question:',
                'A run-on sentence is best corrected by:',
                '',
                'A. Writing only fragments',
                'B. Using proper punctuation or conjunctions to separate independent clauses',
                'C. Adding more unrelated clauses without punctuation',
                'D. Removing all verbs',
                '',
                'My answer: B',
                'Result: Correct',
                '',
                'Correct answer: B. Using proper punctuation or conjunctions to separate independent clauses',
                '',
                'Civio explanation:',
                'A run-on joins independent clauses without proper punctuation.',
                '',
                AI_HANDOFF_EXPLAIN_PROMPT,
            ].join('\n'),
        );
        assert.doesNotMatch(text, /Source\/rule/);
        assert.doesNotMatch(text, /My note/);
    });

    it('includes the explanation in review mode without a Reveal click', () => {
        const text = buildAiHandoffText(shuffledQuestion, {
            ...baseAttempt,
            mode: 'review',
            selectedDisplayIndex: 0,
            verifiedCorrectDisplayIndex: 1,
            verifiedExplanation: 'Review explanation.',
        });

        assert.match(text, /\nMy answer: A\nResult: Incorrect\n/);
        assert.match(text, /\nCivio explanation:\nReview explanation\.\n/);
        assert.ok(text.endsWith(AI_HANDOFF_EXPLAIN_PROMPT));
    });

    it('reports Not answered and adds the note / source only when allowed', () => {
        const attempt: AiHandoffAttemptState = {
            ...baseAttempt,
            mode: 'review',
            selectedDisplayIndex: null,
            verifiedCorrectDisplayIndex: 1,
            verifiedExplanation: 'Because.',
            learnerNote: 'Remember: comma splice ≠ run-on',
        };

        const without = buildAiHandoffText(shuffledQuestion, attempt);
        assert.match(
            without,
            /\nMy answer: not answered yet\nResult: Not answered\n/,
        );
        assert.doesNotMatch(without, /My note/);

        const withNote = buildAiHandoffText(
            { ...shuffledQuestion, source_rule: 'Civio grammar rule G-12' },
            attempt,
            { includeLearnerNote: true },
        );
        assert.match(withNote, /\nSource\/rule: Civio grammar rule G-12\n/);
        assert.match(
            withNote,
            /\nMy note:\nRemember: comma splice ≠ run-on\n\nPlease explain/,
        );
    });
});

describe('option shuffle', () => {
    it('letters follow display order and the verified letter maps to the displayed text', () => {
        // Same item, different shuffle: the right answer now sits at D.
        const reshuffled: AiHandoffQuestion = {
            ...shuffledQuestion,
            options: [
                'Removing all verbs',
                'Writing only fragments',
                'Adding more unrelated clauses without punctuation',
                'Using proper punctuation or conjunctions to separate independent clauses',
            ],
        };

        const text = buildAiHandoffText(reshuffled, {
            ...baseAttempt,
            revealed: true,
            selectedDisplayIndex: 3,
            verifiedCorrectDisplayIndex: 3,
            verifiedExplanation: 'x',
        });

        assert.match(text, /\nA\. Removing all verbs\n/);
        assert.match(text, /\nMy answer: D\nResult: Correct\n/);
        assert.match(
            text,
            /\nCorrect answer: D\. Using proper punctuation or conjunctions to separate independent clauses\n/,
        );
    });
});

describe('clean semantic export', () => {
    it('contains no UI or markup noise', () => {
        const text = buildAiHandoffText(
            {
                ...shuffledQuestion,
                stem: '<p>Which figure completes the series?</p><svg viewBox="0 0 10 10"><text>Previous</text><path d="M0 0"/></svg>',
            },
            {
                ...baseAttempt,
                mode: 'review',
                verifiedCorrectDisplayIndex: 1,
                verifiedExplanation: '<b>Bold</b> reason',
            },
        );

        for (const noise of [
            /svg/i,
            /Report Issue/,
            /Flag/,
            /Previous/,
            /Next/,
            /\d+:\d{2}(:\d{2})?/, // timers
            /Question \d+ of \d+/,
            /<[a-z/]/i,
        ]) {
            assert.doesNotMatch(text, noise);
        }

        assert.match(
            text,
            /\nQuestion:\nWhich figure completes the series\?\n\[figure not included\]\n/,
        );
        assert.match(text, /\nCivio explanation:\nBold reason\n/);
    });

    it('keeps Filipino / Taglish Unicode intact', () => {
        const text = buildAiHandoffText(
            {
                stem: '“Si Señor Niño ay nagbayad ng ₱1,250 — magkano ang sukli mula ₱2,000?”',
                options: [
                    '₱750',
                    '₱650',
                    'Wala sa nabanggit',
                    '₱1,000 × 2 − ₱1,250',
                ],
                category: 'Numerical Ability',
                subcategory: 'Word problems',
            },
            {
                ...baseAttempt,
                examLevel: 'Professional',
                selectedDisplayIndex: 0,
            },
        );

        assert.match(text, /^Philippine Civil Service Exam — Professional\n/);
        assert.match(
            text,
            /\n“Si Señor Niño ay nagbayad ng ₱1,250 — magkano ang sukli mula ₱2,000\?”\n/,
        );
        assert.match(text, /\nD\. ₱1,000 × 2 − ₱1,250\n/);
        assert.doesNotMatch(text, /\?\?|\uFFFD/);
    });

    it('preserves multiline stems', () => {
        const text = buildAiHandoffText(
            {
                ...shuffledQuestion,
                stem: 'Read the passage.\r\n\r\nLine one of the passage.\nLine two of the passage.\n\n\n\nWhich statement is true?',
            },
            baseAttempt,
        );

        assert.match(
            text,
            /\nQuestion:\nRead the passage\.\n\nLine one of the passage\.\nLine two of the passage\.\n\nWhich statement is true\?\n\nA\./,
        );
    });

    it('uses Practice for drills', () => {
        const text = buildAiHandoffText(shuffledQuestion, {
            ...baseAttempt,
            examLevel: 'Practice',
        });
        assert.match(text, /^Philippine Civil Service Exam — Practice\n/);
    });
});

describe('toPlainText', () => {
    it('strips markup but not math or blanks', () => {
        assert.equal(
            toPlainText('If x<y and 3*4 = 12, fill ____ in.'),
            'If x<y and 3*4 = 12, fill ____ in.',
        );
        assert.equal(
            toPlainText('Area = 5<sup>2</sup> &times; 2'),
            'Area = 5² × 2',
        );
        assert.equal(
            toPlainText('**Note:** see [rule](https://x.y)'),
            'Note: see rule',
        );
        assert.equal(toPlainText('a<br>b&nbsp;&amp;&nbsp;c'), 'a\nb & c');
    });
});
