import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    canRequestRescue,
    rescueHeading,
} from '../../resources/js/lib/dexter/rescue';

describe('Dexter Rescue client guard', () => {
    const base = {
        mode: 'study' as const,
        strictMockActive: false,
        graded: true,
        correct: false,
    };

    it('allows a graded wrong Study answer', () => {
        assert.equal(canRequestRescue(base), true);
    });

    it('never asks during Strict mode or an active Strict Mock', () => {
        assert.equal(canRequestRescue({ ...base, mode: 'strict' }), false);
        assert.equal(
            canRequestRescue({ ...base, strictMockActive: true }),
            false,
        );
    });

    it('never asks before grading, for a blank, or for a right answer', () => {
        assert.equal(canRequestRescue({ ...base, graded: false }), false);
        assert.equal(canRequestRescue({ ...base, correct: null }), false);
        assert.equal(canRequestRescue({ ...base, correct: true }), false);
    });

    it('does not claim a diagnosis without a validated one', () => {
        assert.equal(
            rescueHeading({
                state: 'explained',
                skill: 'NUM-WP-RATIO',
                diagnosis: null,
            }),
            'Why this option is wrong',
        );
        assert.equal(
            rescueHeading({
                state: 'explained',
                skill: 'NUM-WP-RATIO',
                diagnosis: {
                    code: 'X',
                    label: 'Used the wrong base',
                    method: 'm',
                },
            }),
            'Used the wrong base',
        );
    });
});
