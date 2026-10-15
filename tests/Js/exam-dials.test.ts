import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';
import { EXAM_DURATION_SECS } from '../../resources/js/lib/exam-clock';
import {
    CLOCK_TICKS,
    clockTick,
    EXAM_DIALS,
    formatSitting,
} from '../../resources/js/lib/exam-dials';
import { EXAM_CONSTANTS } from '../../resources/js/pages/user/exams/utils/exam-utils';

const dialSource = readFileSync(
    new URL(
        '../../resources/js/components/domain/time-dial.tsx',
        import.meta.url,
    ),
    'utf8',
);

describe('exam dial sittings', () => {
    it('matches the CSC scored mock: 150 in 3 hr 10 min, 145 in 2 hr 40 min', () => {
        assert.equal(EXAM_DIALS.professional.questions, 150);
        assert.equal(EXAM_DIALS.professional.seconds, 11400);
        assert.equal(
            formatSitting(EXAM_DIALS.professional.seconds),
            '3 hr 10 min',
        );
        assert.equal(EXAM_DIALS.subprofessional.questions, 145);
        assert.equal(EXAM_DIALS.subprofessional.seconds, 9600);
        assert.equal(
            formatSitting(EXAM_DIALS.subprofessional.seconds),
            '2 hr 40 min',
        );
    });

    it('uses the same limits as the clock and the exam session', () => {
        assert.equal(
            EXAM_DIALS.professional.seconds,
            EXAM_DURATION_SECS.Professional,
        );
        assert.equal(
            EXAM_DIALS.subprofessional.seconds,
            EXAM_DURATION_SECS.Subprofessional,
        );
        assert.equal(
            EXAM_DIALS.professional.seconds,
            EXAM_CONSTANTS.PROFESSIONAL_TIME_LIMIT_SECS,
        );
        assert.equal(
            EXAM_DIALS.subprofessional.seconds,
            EXAM_CONSTANTS.SUBPROFESSIONAL_TIME_LIMIT_SECS,
        );
        assert.equal(
            EXAM_DIALS.professional.questions,
            EXAM_CONSTANTS.PROFESSIONAL_SCORED_ITEMS,
        );
        assert.equal(
            EXAM_DIALS.subprofessional.questions,
            EXAM_CONSTANTS.SUBPROFESSIONAL_SCORED_ITEMS,
        );
    });

    it('does not draw tick marks around the ring', () => {
        assert.doesNotMatch(dialSource, /civio-tick/);
        assert.doesNotMatch(dialSource, /CLOCK_TICKS/);
        assert.equal(CLOCK_TICKS, 12);
        assert.equal(clockTick(0).role, 'cardinal');
        assert.equal(clockTick(3).angle, 90);
    });
});
