import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { toDisplayQuestion } from '../../resources/js/lib/offline/grader';
import {
    answersFromSession,
    applyVerdicts,
    enqueue,
    MAX_QUEUE,
    nextBatch,
    syncQueue,
    toBiasInput,
} from '../../resources/js/lib/offline/sync-queue';
import type { StudyBiasInput } from '../../resources/js/lib/guest-study-bias';
import type {
    OfflinePackItem,
    QueuedAnswer,
    SyncResponse,
} from '../../resources/js/lib/offline/types';

const item: OfflinePackItem = {
    id: 7,
    stem: 'Q?',
    options: ['A', 'B', 'C', 'D'],
    correct_option: 1,
    explanation: 'B.',
    category: 'General Information',
    subcategory: 'Constitution',
    language: 'English',
};

function answer(id: string, questionId = 7): QueuedAnswer {
    return {
        client_id: id,
        question_id: questionId,
        selected_option: 1,
        claimed_correct_option: 1,
        pack_version: 'v1',
        answered_at: '2026-10-07T00:00:00.000Z',
    };
}

describe('offline sync queue', () => {
    it('queues answered items in original option order with the claimed key', () => {
        const question = toDisplayQuestion(item, () => 0.1);
        const display = (question.originalOptionIndices ?? []).indexOf(3);
        let n = 0;

        const queued = answersFromSession(
            [item, { ...item, id: 8 }],
            [question, toDisplayQuestion({ ...item, id: 8 }, () => 0.5)],
            { 0: display },
            { 'General Information': 'v9' },
            new Date('2026-10-07T01:00:00Z'),
            () => `id-${++n}`,
        );

        assert.deepEqual(queued, [
            {
                client_id: 'id-1',
                question_id: 7,
                selected_option: 3,
                claimed_correct_option: 1,
                pack_version: 'v9',
                answered_at: '2026-10-07T01:00:00.000Z',
            },
        ]);
    });

    it('dedupes by client id and caps the queue', () => {
        const merged = enqueue([answer('a')], [answer('a'), answer('b')]);
        assert.deepEqual(
            merged.map((a) => a.client_id),
            ['a', 'b'],
        );

        const many = Array.from({ length: MAX_QUEUE + 5 }, (_, i) =>
            answer(`x${i}`),
        );
        const capped = enqueue([], many);
        assert.equal(capped.length, MAX_QUEUE);
        assert.equal(capped[0]?.client_id, 'x5');
    });

    it('batches and drops answers that got a verdict', () => {
        const queue = [answer('a'), answer('b'), answer('c')];

        assert.equal(nextBatch(queue, 2).length, 2);
        assert.deepEqual(
            applyVerdicts(queue, [
                {
                    client_id: 'a',
                    question_id: 7,
                    status: 'accepted',
                    reason: null,
                    duplicate: false,
                    correct: true,
                },
                {
                    client_id: 'c',
                    question_id: 7,
                    status: 'rejected',
                    reason: 'key_mismatch',
                    duplicate: false,
                },
            ]).map((a) => a.client_id),
            ['b'],
        );
    });

    it('turns the server bias block into study bias input (empty PHP array too)', () => {
        assert.deepEqual(
            toBiasInput({
                wrong_ids: [1],
                correct_ids: [2],
                category_scores: [],
            }),
            { wrongIds: [1], correctIds: [2], categoryScoreMap: {} },
        );
    });

    it('syncs in batches, records bias only from server verdicts, and keeps new answers', async () => {
        let stored: QueuedAnswer[] = Array.from({ length: 250 }, (_, i) =>
            answer(`q${i}`),
        );
        const posted: number[] = [];
        const bias: StudyBiasInput[] = [];
        let added = false;

        const summary = await syncQueue({
            loadQueue: async () => stored,
            saveQueue: async (q) => {
                stored = q;
            },
            post: async (batch): Promise<SyncResponse> => {
                posted.push(batch.length);

                if (!added) {
                    added = true;
                    stored = [...stored, answer('late')];
                }

                return {
                    success: true,
                    results: batch.map((a, i) => ({
                        client_id: a.client_id,
                        question_id: a.question_id,
                        status: i === 0 ? 'rejected' : 'accepted',
                        reason: i === 0 ? 'key_mismatch' : null,
                        duplicate: false,
                        correct: i % 2 === 1,
                    })),
                    bias: {
                        wrong_ids: [9],
                        correct_ids: [7],
                        category_scores: {},
                    },
                };
            },
            recordBias: (input) => bias.push(input),
            isOnline: () => true,
        });

        assert.deepEqual(posted, [200, 51]);
        assert.equal(summary.sent, 251);
        assert.equal(summary.rejected, 2);
        assert.equal(summary.accepted, 249);
        assert.equal(summary.remaining, 0);
        assert.equal(summary.error, null);
        assert.equal(bias.length, 2);
        assert.deepEqual(stored, []);
    });

    it('keeps the queue when offline or when the request fails', async () => {
        let stored = [answer('a')];
        const deps = {
            loadQueue: async () => stored,
            saveQueue: async (q: QueuedAnswer[]) => {
                stored = q;
            },
            recordBias: () => assert.fail('no bias without a verdict'),
        };

        const offline = await syncQueue({
            ...deps,
            post: async () => assert.fail('no post offline'),
            isOnline: () => false,
        });
        assert.equal(offline.error, 'offline');
        assert.equal(offline.remaining, 1);

        const failed = await syncQueue({
            ...deps,
            post: async () => {
                throw new Error('Sync failed (500)');
            },
            isOnline: () => true,
        });
        assert.equal(failed.error, 'Sync failed (500)');
        assert.equal(stored.length, 1);
    });
});
