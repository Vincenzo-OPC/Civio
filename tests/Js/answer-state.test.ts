import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    answerOptionVisual,
    canPauseExam,
    recoveredSessionStartsPaused,
    shouldRunExamClock,
} from '../../resources/js/pages/user/exams/utils/answer-state';
import { retiredNotice } from '../../resources/js/pages/user/exams/utils/retired-notice';

describe('answer option visuals', () => {
    it('stays neutral until a choice is selected', () => {
        assert.deepEqual(
            answerOptionVisual({
                optionIndex: 1,
                selectedIndex: undefined,
                revealed: false,
                strict: false,
                correctIndex: 0,
            }),
            { visual: 'unanswered', status: null },
        );
    });

    it('marks a selection violet-state without saying it is correct', () => {
        assert.deepEqual(
            answerOptionVisual({
                optionIndex: 1,
                selectedIndex: 1,
                revealed: false,
                strict: false,
                correctIndex: 1,
            }),
            { visual: 'selected', status: 'Selected' },
        );
    });

    it('shows correct and incorrect only after Reveal', () => {
        assert.deepEqual(
            answerOptionVisual({
                optionIndex: 0,
                selectedIndex: 1,
                revealed: true,
                strict: false,
                correctIndex: 0,
            }),
            { visual: 'correct-unselected', status: 'Correct answer' },
        );
        assert.deepEqual(
            answerOptionVisual({
                optionIndex: 1,
                selectedIndex: 1,
                revealed: true,
                strict: false,
                correctIndex: 0,
            }),
            { visual: 'incorrect', status: 'Your answer · Incorrect' },
        );
        assert.deepEqual(
            answerOptionVisual({
                optionIndex: 0,
                selectedIndex: 0,
                revealed: true,
                strict: false,
                correctIndex: 0,
            }),
            { visual: 'correct', status: 'Your answer · Correct' },
        );
    });

    it('keeps a Strict Mock selection secret even if a key is present', () => {
        assert.deepEqual(
            answerOptionVisual({
                optionIndex: 1,
                selectedIndex: 1,
                revealed: true,
                strict: true,
                correctIndex: 0,
            }),
            { visual: 'selected', status: 'Selected' },
        );
    });
});

describe('exam pause', () => {
    it('allows pause in Study and drills, not in a Strict Mock', () => {
        assert.equal(canPauseExam(false, 'study'), true);
        assert.equal(canPauseExam(true, 'strict'), true);
        assert.equal(canPauseExam(false, 'strict'), false);
    });

    it('does not run the clock while paused or after submit', () => {
        assert.equal(
            shouldRunExamClock({
                isExamActive: true,
                isExamSubmitted: false,
                isPaused: false,
            }),
            true,
        );
        assert.equal(
            shouldRunExamClock({
                isExamActive: true,
                isExamSubmitted: false,
                isPaused: true,
            }),
            false,
        );
        assert.equal(
            shouldRunExamClock({
                isExamActive: true,
                isExamSubmitted: true,
                isPaused: false,
            }),
            false,
        );
    });

    it('restores with the clock stopped unless the timed session already expired', () => {
        assert.equal(recoveredSessionStartsPaused(true, 120), true);
        assert.equal(recoveredSessionStartsPaused(false, 40), true);
        assert.equal(recoveredSessionStartsPaused(true, 0), false);
    });
});

it('scorecard explains withdrawn items without counting them wrong or skipped', () => {
    assert.equal(retiredNotice(0, 150), null);
    assert.equal(retiredNotice(undefined, 150), null);
    assert.equal(
        retiredNotice(1, 149),
        '1 item was withdrawn by Civio after this mock started. It is not counted as wrong or skipped: your score is out of 149, not 150.',
    );
    assert.match(
        retiredNotice(2, 148) ?? '',
        /^2 items were withdrawn .* They are not counted .* out of 148, not 150\.$/,
    );
});
