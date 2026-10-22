import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
    httpStatusOf,
    mergeResumed,
    pendingKey,
    persistPending,
    readPending,
    saveProgressPatch,
    settleSave,
    withoutWithdrawn,
} from '../../resources/js/pages/user/exams/utils/progress-save';
import type { Question } from '../../resources/js/pages/user/exams/types';
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
        questions: {
            current: [{ id: 7 }, { id: 8 }, { id: 9 }] as unknown as Question[],
        },
        hydrate(server: Record<string, number | null>) {
            const ids = [7, 8, 9];
            ui.answers = Object.fromEntries(
                ids.flatMap((id, i) =>
                    server[id] == null ? [] : [[i, server[id] as number]],
                ),
            );
        },
        toast: Object.fromEntries(
            ['info', 'success', 'warning', 'error'].map((level) => [
                level,
                (message: string) => ui.notices.push(`${level}: ${message}`),
            ]),
        ) as Record<
            'info' | 'success' | 'warning' | 'error',
            (m: string) => number
        >,
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
            }),
    };
}

test('UI: a mixed save keeps active answers, drops the retired one and warns once', () => {
    // Positions 0,1,2 hold items 7,8,9: answers are keyed by position.
    const h = harness({ 0: 1, 1: 0, 2: 3 });
    const version = h.settle(
        { kind: 'saved', version: 2, withdrawn: [9] },
        { 7: 1, 8: 0, 9: 3 },
    );
    assert.equal(version, 2);
    assert.deepEqual(
        h.ui.answers,
        { 0: 1, 1: 0 },
        'only position 2 (item 9) is cleared',
    );
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
    const h = harness({ 0: 1, 2: 2 });
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
    assert.deepEqual(h.ui.answers, { 0: 1 });
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

function memoryStorage() {
    const data = new Map<string, string>();
    return {
        data,
        getItem: (k: string) => data.get(k) ?? null,
        setItem: (k: string, v: string) => void data.set(k, v),
        removeItem: (k: string) => void data.delete(k),
    };
}

test('resume: offline answers survive a reload and are newer when the server is unchanged', () => {
    const storage = memoryStorage();
    const h = harness({ 7: 1 });
    Object.assign(h.state, {
        sessionId: 'S',
        storage,
        server: { 7: 1, 8: null },
    });

    h.settle({ kind: 'offline' }, { 7: 3 });
    h.settle({ kind: 'offline' }, { 8: 0 });
    assert.deepEqual(readPending('S', storage), { 7: [3, 1], 8: [0, null] });

    // A second offline change to item 7 keeps the original server base.
    h.state.pending.set(7, 2);
    h.settle({ kind: 'offline' }, { 7: 2 });
    assert.deepEqual(readPending('S', storage)[7], [2, 1]);

    // Reload: the server still has the old values, so local answers win and are resent.
    const merged = mergeResumed(
        res({ answers: { 7: 1 }, save_version: 4 }),
        readPending('S', storage),
        [7, 8, 9],
    );
    assert.deepEqual(merged.answers, { 7: 2, 8: 0 });
    assert.deepEqual(merged.resend, { 7: 2, 8: 0 });
    assert.deepEqual(merged.superseded, []);
});

test('resume: a change saved elsewhere after the offline answer wins', () => {
    const merged = mergeResumed(
        res({ answers: { 7: 0, 8: 1 } }),
        { 7: [2, 1], 8: [1, null] },
        [7, 8],
    );
    assert.deepEqual(merged.answers, { 7: 0, 8: 1 });
    assert.deepEqual(
        merged.resend,
        {},
        'item 8 already matches; item 7 changed on the server',
    );
    assert.deepEqual(merged.superseded, [7]);
});

test('resume: after the deadline or submit nothing local is applied or resent', () => {
    for (const server of [
        res({ answers: { 7: 1 }, server_now: '2026-10-22T10:00:00Z' }),
        res({ answers: { 7: 1 }, submitted: true }),
    ]) {
        const merged = mergeResumed(server, { 7: [3, 1] }, [7]);
        assert.deepEqual(merged.answers, { 7: 1 });
        assert.deepEqual(merged.resend, {});
    }
});

test('resume: unserved, malformed or tampered local entries are ignored', () => {
    const storage = memoryStorage();
    storage.setItem(
        pendingKey('S'),
        JSON.stringify({
            7: [1, null],
            99: [0, null],
            x: [1, 1],
            8: ['a', 1],
            9: [1],
        }),
    );
    const local = readPending('S', storage);
    assert.deepEqual(local, { 7: [1, null], 99: [0, null] });
    assert.deepEqual(mergeResumed(res(), local, [7]).resend, { 7: 1 });
    storage.setItem(pendingKey('S'), '{not json');
    assert.deepEqual(readPending('S', storage), {});
});

test('resume: storage is cleared once everything is saved, and on withdrawal', () => {
    const storage = memoryStorage();
    const h = harness();
    Object.assign(h.state, { sessionId: 'S', storage, server: {} });
    h.settle({ kind: 'offline' }, { 7: 1, 9: 2 });
    h.settle({ kind: 'saved', version: 2, withdrawn: [9] }, { 7: 1, 9: 2 });
    assert.equal(storage.data.has(pendingKey('S')), false);
    assert.deepEqual(h.state.server, { 7: 1 });
    persistPending(h.state);
    assert.equal(storage.data.size, 0);
});

test('UI: a conflict merge rehydrates by position and keeps answers still pending', () => {
    const h = harness({ 0: 0 });
    h.state.pending.set(9, 3);
    h.settle(
        { kind: 'merged', version: 4, answers: { 7: 1, 8: 2 }, withdrawn: [] },
        { 8: 2 },
    );
    assert.deepEqual(h.ui.answers, { 0: 1, 1: 2, 2: 3 });
    assert.ok(h.ui.notices.some((n) => /updated from another tab/.test(n)));
});

test('an empty batch (all withdrawn) sends nothing', async () => {
    let calls = 0;
    const out = await saveProgressPatch(
        async () => (calls++, res()),
        's',
        {},
        5,
    );
    assert.deepEqual(out, { kind: 'saved', version: 5, withdrawn: [] });
    assert.equal(calls, 0);
});
