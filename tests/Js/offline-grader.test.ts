import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
    buildOfflineSession,
    correctDisplayIndex,
    isCorrectLocally,
    scoreOfflineSession,
    shuffle,
    toDisplayQuestion,
    toOriginalIndex,
} from '../../resources/js/lib/offline/grader';
import type { OfflinePackItem } from '../../resources/js/lib/offline/types';

function seeded(seed = 42): () => number {
    let state = seed;

    return () => {
        state = (state * 1664525 + 1013904223) % 4294967296;

        return state / 4294967296;
    };
}

function item(
    id: number,
    correct = 2,
    category = 'General Information',
    subcategory = 'Constitution',
): OfflinePackItem {
    return {
        id,
        stem: `Item ${id}?`,
        options: [`A${id}`, `B${id}`, `C${id}`, `D${id}`],
        correct_option: correct,
        explanation: `Because C${id}.`,
        category,
        subcategory,
        language: 'English',
    };
}

describe('offline grader', () => {
    it('shuffles without losing or duplicating values', () => {
        const out = shuffle([1, 2, 3, 4, 5, 6], seeded());

        assert.deepEqual([...out].sort(), [1, 2, 3, 4, 5, 6]);
    });

    it('maps display choices back to original indices', () => {
        const question = toDisplayQuestion(item(1), seeded(7));
        const order = question.originalOptionIndices ?? [];

        assert.equal(order.length, 4);
        order.forEach((original, display) => {
            assert.equal(question.options[display], `${'ABCD'[original]}1`);
            assert.equal(toOriginalIndex(question, display), original);
        });

        const correctAt = correctDisplayIndex(question, item(1));
        assert.equal(question.options[correctAt], 'C1');
        assert.ok(
            isCorrectLocally(item(1), toOriginalIndex(question, correctAt)),
        );
    });

    it('never puts the key or explanation on the display question', () => {
        const question = toDisplayQuestion(item(3), seeded());

        assert.equal('correct_option' in question, false);
        assert.equal('explanation' in question, false);
    });

    it('builds a session of the requested size', () => {
        const items = [1, 2, 3, 4, 5].map((id) => item(id));

        assert.equal(
            buildOfflineSession(items, 3, seeded()).questions.length,
            3,
        );
        assert.equal(
            buildOfflineSession(items, 'all', seeded()).items.length,
            5,
        );
    });

    it('scores a session with per-category and per-subcategory totals', () => {
        const items = [
            item(1),
            item(2),
            item(3, 0, 'Numerical Ability', 'Arithmetic'),
        ];
        const questions = items.map((i) => toDisplayQuestion(i, seeded(i.id)));
        const answers = {
            0: correctDisplayIndex(questions[0]!, items[0]!),
            1: (correctDisplayIndex(questions[1]!, items[1]!) + 1) % 4,
        };

        const score = scoreOfflineSession(items, questions, answers);

        assert.equal(score.correct, 1);
        assert.equal(score.answered, 2);
        assert.equal(score.total, 3);
        assert.deepEqual(score.categoryScoreMap['General Information'], {
            correct: 1,
            total: 2,
            subcats: { Constitution: { correct: 1, total: 2 } },
        });
        assert.deepEqual(score.categoryScoreMap['Numerical Ability'], {
            correct: 0,
            total: 1,
            subcats: { Arithmetic: { correct: 0, total: 1 } },
        });
    });
});
