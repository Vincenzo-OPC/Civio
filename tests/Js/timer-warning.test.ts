import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { dueTimerWarning } from '../../resources/js/pages/user/exams/utils/server-clock';

describe('dueTimerWarning', () => {
    it('fires the 10-minute warning even when a throttled tab skips 600', () => {
        assert.equal(dueTimerWarning(571, false, false), '10m');
    });

    it('fires the 1-minute warning when the clock jumps past 60', () => {
        assert.equal(dueTimerWarning(42, false, false), '1m');
    });

    it('never repeats a warning already shown', () => {
        assert.equal(dueTimerWarning(500, true, false), null);
        assert.equal(dueTimerWarning(30, true, true), null);
    });

    it('stays quiet above ten minutes and at zero', () => {
        assert.equal(dueTimerWarning(601, false, false), null);
        assert.equal(dueTimerWarning(0, false, false), null);
    });
});
