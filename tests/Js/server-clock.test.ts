import assert from 'node:assert/strict';
import { test } from 'node:test';
import { restoreAnswerPositions } from '../../resources/js/pages/user/exams/utils/answer-state';
import { localDeadline, secondsUntil } from '../../resources/js/pages/user/exams/utils/server-clock';

test('remaining time follows elapsed wall time after background throttling', () => {
    const deadline = 190000;
    assert.equal(secondsUntil(deadline, 0), 190);
    assert.equal(secondsUntil(deadline, 120000), 70);
    assert.equal(secondsUntil(deadline, 190000), 0);
    assert.equal(secondsUntil(deadline, 250000), 0);
});

test('server recovery corrects device clock offset without granting extra time', () => {
    const deadline = '2026-10-20T12:03:00Z';
    assert.equal(localDeadline(deadline, '2026-10-20T12:00:00Z', 1000), 181000);
    const recovered = localDeadline(deadline, '2026-10-20T12:02:00Z', 900000);
    assert.equal(secondsUntil(recovered, 900000), 60);
    assert.equal(secondsUntil(recovered, 960000), 0);
});
test('saved answers restore by question identity and original option order', () => {
    assert.deepEqual(restoreAnswerPositions([
        { id: 42, originalOptionIndices: [2, 0, 3, 1] }, { id: 99 },
    ], { 42: 1, 99: 0, 123: 2 }), { 0: 3, 1: 0 });
});

test('unanswered and unavailable original options stay blank on recovery', () => {
    assert.deepEqual(restoreAnswerPositions([
        { id: 42, originalOptionIndices: [2, 0] }, { id: 99 }, { id: 100 },
    ], { 42: 1, 99: null }), {});
});