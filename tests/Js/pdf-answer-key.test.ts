import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { pdfAnswerLetters } from '../../resources/js/lib/pdf-answer-key';

test('letters identify the correct choice in printed option order', () => {
    const items = [0, 1, 2, 3].map((key) => ({
        options: ['one', 'two', 'three', 'four'],
        correct_option: key,
    }));
    assert.deepEqual(pdfAnswerLetters(items), ['A', 'B', 'C', 'D']);
    const reordered = {
        options: ['four', 'one', 'two', 'three'],
        correct_option: 0,
    };
    assert.deepEqual(pdfAnswerLetters([reordered]), ['A']);
    assert.equal(reordered.options[reordered.correct_option], 'four');
});

test('any missing or invalid key suppresses the whole answer key', () => {
    for (const key of [undefined, null, -1, 4, 0.5, NaN, Infinity]) {
        assert.equal(
            pdfAnswerLetters([
                { options: ['A', 'B'], correct_option: 1 },
                { options: ['A', 'B', 'C', 'D'], correct_option: key },
            ]),
            null,
        );
    }
    assert.equal(pdfAnswerLetters([]), null);
    assert.equal(pdfAnswerLetters([{ options: [], correct_option: 0 }]), null);
});

test('renderer omits the entire key page and export preserves option order', () => {
    const renderer = readFileSync(
        'resources/js/pages/user/exams/components/printable-exam.tsx',
        'utf8',
    );
    assert.match(renderer, /pdfAnswerLetters\(questions\)/);
    assert.match(renderer, /answerKeyColumns.length > 0 &&/);
    assert.doesNotMatch(renderer, /correct_option \?\? 0/);
    const hook = readFileSync(
        'resources/js/pages/user/exams/hooks/use-exam-state.ts',
        'utf8',
    );
    const handler = hook.slice(
        hook.indexOf('const handlePrintExam'),
        hook.indexOf('const getActiveTimeLimitSecs'),
    );
    assert.match(handler, /\/exams\/export-pdf/);
    assert.doesNotMatch(
        handler,
        /startMockSession|shuffleOptionsForQuestion|export-pdf-check/,
    );
});
