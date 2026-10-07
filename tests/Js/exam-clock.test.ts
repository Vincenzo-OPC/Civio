import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    EXAM_DURATION_SECS,
    examClockTone,
    formatExamLeft,
    formatItemElapsed,
    itemClockTone,
} from '../../resources/js/lib/exam-clock';
import { EXAM_CONSTANTS } from '../../resources/js/pages/user/exams/utils/exam-utils';

describe('exam clock durations', () => {
    it('Professional starts at 3:10:00 and Subprofessional at 2:40:00', () => {
        assert.equal(formatExamLeft(EXAM_DURATION_SECS.Professional), '3:10:00');
        assert.equal(
            formatExamLeft(EXAM_DURATION_SECS.Subprofessional),
            '2:40:00',
        );
    });

    it('matches the session limits the exam hooks actually use', () => {
        assert.equal(
            EXAM_CONSTANTS.PROFESSIONAL_TIME_LIMIT_SECS,
            EXAM_DURATION_SECS.Professional,
        );
        assert.equal(
            EXAM_CONSTANTS.SUBPROFESSIONAL_TIME_LIMIT_SECS,
            EXAM_DURATION_SECS.Subprofessional,
        );
    });
});

describe('examClockTone (Exam left)', () => {
    it('is calm while more than 10 minutes remain', () => {
        assert.equal(examClockTone(EXAM_DURATION_SECS.Professional), 'calm');
        assert.equal(examClockTone(601), 'calm');
    });

    it('turns amber in the last 10 minutes', () => {
        assert.equal(examClockTone(600), 'amber');
        assert.equal(examClockTone(121), 'amber');
    });

    it('turns red in the last 2 minutes and at zero', () => {
        assert.equal(examClockTone(120), 'red');
        assert.equal(examClockTone(1), 'red');
        assert.equal(examClockTone(0), 'red');
        assert.equal(examClockTone(-5), 'red');
    });
});

describe('itemClockTone (This item)', () => {
    it('is calm under 45 seconds', () => {
        assert.equal(itemClockTone(0), 'calm');
        assert.equal(itemClockTone(44), 'calm');
        assert.equal(itemClockTone(44.9), 'calm');
    });

    it('is amber from 45s through 75s', () => {
        assert.equal(itemClockTone(45), 'amber');
        assert.equal(itemClockTone(60), 'amber');
        assert.equal(itemClockTone(75), 'amber');
    });

    it('is red after 75s', () => {
        assert.equal(itemClockTone(76), 'red');
        assert.equal(itemClockTone(600), 'red');
    });
});

describe('clock formatting', () => {
    it('formats the exam countdown as H:MM:SS', () => {
        assert.equal(formatExamLeft(599), '0:09:59');
        assert.equal(formatExamLeft(0), '0:00:00');
        assert.equal(formatExamLeft(-3), '0:00:00');
    });

    it('formats the item clock as M:SS', () => {
        assert.equal(formatItemElapsed(5), '0:05');
        assert.equal(formatItemElapsed(65), '1:05');
        assert.equal(formatItemElapsed(600), '10:00');
    });
});
