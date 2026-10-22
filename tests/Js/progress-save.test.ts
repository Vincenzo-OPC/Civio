import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
    httpStatusOf,
    saveProgressPatch,
    settleSave,
    withoutWithdrawn,
} from '../../resources/js/pages/user/exams/utils/progress-save';
import type { ProgressResponse } from '../../resources/js/pages/user/exams/utils/progress-save';

const fail = (status: number) =>
    new Error(
        `API request to /exams/sessions/progress failed with status ${status}`,
    );
const res = (over: Partial<ProgressResponse> = {}): ProgressResponse => ({
    deadline_at: '2026-10-22T10:00:00Z',
    server_now: '2026-10-22T09:00:00Z',
    answers: {},
    save_version: 0,
    submitted: false,
    ...over,
});

test('reads the status from apiPost errors', () => {
    assert.equal(httpStatusOf(fail(409)), 409);
    assert.equal(httpStatusOf(new TypeError('Failed to fetch')), null);
});

test('a normal save sends only this item and adopts the new version', async () => {
    const calls: Record<string, unknown>[] = [];
    const out = await saveProgressPatch(
        async (p) => (calls.push(p), res({ save_version: 4 })),
        's',
        { 7: 2 },
        3,
    );
    assert.deepEqual(out, { kind: 'saved', version: 4, withdrawn: [] });
    assert.deepEqual(calls, [
        { exam_session_id: 's', expected_version: 3, answers: { 7: 2 } },
    ]);
});

test('one patch mixing active and retired answers saves the active ones and reports the retired one', async () => {
    const calls: Record<string, unknown>[] = [];
    const out = await saveProgressPatch(
        async (p) => (
            calls.push(p),
            res({
                save_version: 2,
                answers: { 7: 1, 8: 0 },
                withdrawn_ids: [9],
            })
        ),
        's',
        { 7: 1, 8: 0, 9: 3 },
        1,
    );
    assert.deepEqual(out, { kind: 'saved', version: 2, withdrawn: [9] });
    assert.equal(calls.length, 1, 'a single request, no retry');
    assert.deepEqual(calls[0].answers, { 7: 1, 8: 0, 9: 3 });
});

test('a 422 is a hard failure and is never retried in a loop', async () => {
    let n = 0;
    const out = await saveProgressPatch(
        async () => {
            n++;
            throw fail(422);
        },
        's',
        { 7: 1 },
        0,
    );
    assert.deepEqual(out, { kind: 'failed' });
    assert.equal(n, 1);
});

test('withdrawn ids survive a conflict retry', async () => {
    let n = 0;
    const out = await saveProgressPatch(
        async (p) => {
            n++;
            if (n === 1) throw fail(409);
            if (!('answers' in p)) return res({ save_version: 3 });
            return res({
                save_version: 4,
                answers: { 7: 1 },
                withdrawn_ids: [9],
            });
        },
        's',
        { 7: 1, 9: 0 },
        2,
    );
    assert.deepEqual(out, {
        kind: 'merged',
        version: 4,
        answers: { 7: 1 },
        withdrawn: [9],
    });
});

test('a version conflict re-reads, retries once and returns merged answers', async () => {
    const calls: Record<string, unknown>[] = [];
    const out = await saveProgressPatch(
        async (p) => {
            calls.push(p);
            if (calls.length === 1) throw fail(409);
            if (!('answers' in p))
                return res({ save_version: 5, answers: { 8: 0 } });
            return res({ save_version: 6, answers: { 7: 1, 8: 0 } });
        },
        's',
        { 7: 1 },
        3,
    );
    assert.deepEqual(out, {
        kind: 'merged',
        version: 6,
        answers: { 7: 1, 8: 0 },
        withdrawn: [],
    });
    assert.equal(
        (calls[2] as { expected_version: number }).expected_version,
        5,
    );
});

test('a 409 after the deadline or submit closes saving without retry', async () => {
    for (const latest of [
        res({ server_now: '2026-10-22T10:00:01Z' }),
        res({ submitted: true }),
    ]) {
        let patches = 0;
        const out = await saveProgressPatch(
            async (p) => {
                if ('answers' in p) {
                    patches++;
                    throw fail(409);
                }
                return latest;
            },
            's',
            { 7: 1 },
            0,
        );
        assert.equal(out.kind, 'closed');
        assert.equal(patches, 1);
    }
});

test('a repeated 409 with an unchanged version fails instead of looping', async () => {
    const out = await saveProgressPatch(
        async (p) => {
            if ('answers' in p) throw fail(409);
            return res({ save_version: 0 });
        },
        's',
        { 7: 1 },
        0,
    );
    assert.deepEqual(out, { kind: 'failed' });
});

test('a network drop is offline so the caller can hold the answer', async () => {
    const out = await saveProgressPatch(
        async () => {
            throw new TypeError('Failed to fetch');
        },
        's',
        { 7: 1 },
        0,
    );
    assert.deepEqual(out, { kind: 'offline' });
});

function harness(answers: Record<number, number> = {}) {
    const ui = {
        answers: { ...answers },
        notices: [] as string[],
        closed: [] as boolean[],
        setAnswers(
            update: (prev: Record<number, number>) => Record<number, number>,
        ) {
            ui.answers = update(ui.answers);
        },
        hydrate() {},
        notify(level: string, message: string) {
            ui.notices.push(`${level}: ${message}`);
        },
    };
    const state = {
        pending: new Map<number, number | null>(),
        withdrawnIds: new Set<number>(),
        offline: { current: false },
    };
    return {
        state,
        ui,
        settle: (
            outcome: Parameters<typeof settleSave>[0],
            sent: Record<number, number | null>,
        ) =>
            settleSave(outcome, sent, state, {
                ...ui,
                closed: (s: boolean) => ui.closed.push(s),
                setAnswers: ui.setAnswers,
                notify: ui.notify,
            }),
    };
}

test('UI: a mixed save keeps active answers, drops the retired one and warns once', () => {
    const h = harness({ 7: 1, 8: 0, 9: 3 });
    const version = h.settle(
        { kind: 'saved', version: 2, withdrawn: [9] },
        { 7: 1, 8: 0, 9: 3 },
    );
    assert.equal(version, 2);
    assert.deepEqual(h.ui.answers, { 7: 1, 8: 0 });
    assert.equal(h.ui.notices.length, 1);
    assert.match(
        h.ui.notices[0],
        /^warning: One item was withdrawn .*not be scored.*other answers are saved/,
    );
    assert.ok(h.state.withdrawnIds.has(9));

    // Re-answering the withdrawn item is never sent again: no 422 loop.
    assert.deepEqual(withoutWithdrawn({ 9: 2, 7: 0 }, h.state.withdrawnIds), {
        7: 0,
    });
    assert.deepEqual(withoutWithdrawn({ 9: 2 }, h.state.withdrawnIds), {});

    // The same withdrawal reported again does not repeat the notice.
    h.settle({ kind: 'saved', version: 3, withdrawn: [9] }, { 7: 0 });
    assert.equal(h.ui.notices.length, 1);
});

test('UI: offline answers are held, then a mixed flush clears them and drops the retired one', () => {
    const h = harness({ 7: 1, 9: 2 });
    assert.equal(h.settle({ kind: 'offline' }, { 7: 1 }), null);
    h.settle({ kind: 'offline' }, { 9: 2 });
    assert.deepEqual(
        [...h.state.pending],
        [
            [7, 1],
            [9, 2],
        ],
    );
    assert.equal(
        h.ui.notices.filter((n) => n.startsWith('warning: Connection lost'))
            .length,
        1,
    );

    h.settle(
        { kind: 'saved', version: 5, withdrawn: [9] },
        Object.fromEntries(h.state.pending),
    );
    assert.equal(h.state.pending.size, 0);
    assert.deepEqual(h.ui.answers, { 7: 1 });
    assert.ok(h.ui.notices.some((n) => n.startsWith('success: Reconnected')));
});

test('UI: a newer choice made while a save was in flight stays pending', () => {
    const h = harness();
    h.state.pending.set(7, 2);
    h.settle({ kind: 'saved', version: 1, withdrawn: [] }, { 7: 1 });
    assert.equal(h.state.pending.get(7), 2);
});

test('UI: a submitted mock closes saving and a hard failure throws', () => {
    const h = harness();
    h.state.pending.set(7, 1);
    assert.equal(h.settle({ kind: 'closed', submitted: true }, { 7: 1 }), null);
    assert.deepEqual(h.ui.closed, [true]);
    assert.equal(h.state.pending.size, 0);
    assert.throws(() => h.settle({ kind: 'failed' }, { 7: 1 }));
});
