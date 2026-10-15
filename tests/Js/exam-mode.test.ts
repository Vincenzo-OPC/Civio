import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    EXAM_MODE_LABELS,
    isTimerOn,
    parseExamMode,
    showsStudyTools,
} from '../../resources/js/pages/user/exams/utils/exam-mode';
import { EXAM_CONSTANTS } from '../../resources/js/pages/user/exams/utils/exam-utils';
import { mockSessionBody } from '../../resources/js/pages/user/exams/utils/mock-session';

describe('Exam Simulation modes', () => {
    it('labels the two modes', () => {
        assert.deepEqual(EXAM_MODE_LABELS, {
            study: 'Study Mode',
            strict: 'Exam Mode',
        });
    });

    it('defaults anything unknown to study', () => {
        assert.equal(parseExamMode('strict'), 'strict');
        assert.equal(parseExamMode('study'), 'study');
        assert.equal(parseExamMode(undefined), 'study');
        assert.equal(parseExamMode('STRICT!'), 'study');
    });

    it('forces the timer on in Strict and leaves it optional in Study', () => {
        assert.equal(isTimerOn('strict', false), true);
        assert.equal(isTimerOn('strict', true), true);
        assert.equal(isTimerOn('study', false), false);
        assert.equal(isTimerOn('study', true), true);
    });

    it('hides Reveal, Dexter and Copy for AI only in a Strict Mock', () => {
        assert.equal(showsStudyTools('strict', false), false);
        assert.equal(showsStudyTools('study', false), true);
        assert.equal(showsStudyTools('strict', true), true);
    });

    it('sends the mode with the mock request and caps the bias hints', () => {
        const body = mockSessionBody('Professional', 'strict', {
            wrongIds: Array.from({ length: 2500 }, (_, i) => i),
            weakSubcategories: [],
            weakCategories: ['Verbal Ability'],
        });
        assert.equal(body.mode, 'strict');
        assert.equal(body.track, 'Professional');
        assert.equal(body.bias.wrong_ids.length, 2000);
    });

    it('keeps the guide pace in line with the real mock sizes', () => {
        assert.equal(EXAM_CONSTANTS.PROFESSIONAL_TOTAL_ITEMS, 150);
        assert.equal(EXAM_CONSTANTS.SUBPROFESSIONAL_TOTAL_ITEMS, 145);
        assert.equal(
            Math.round(EXAM_CONSTANTS.PROFESSIONAL_TIME_LIMIT_SECS / 150),
            76,
        );
        assert.equal(
            Math.round(EXAM_CONSTANTS.SUBPROFESSIONAL_TIME_LIMIT_SECS / 145),
            66,
        );
    });
});
