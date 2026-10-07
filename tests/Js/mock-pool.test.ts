import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import type { Question } from '../../resources/js/pages/user/exams/types';
import {
    mockLevelForExam,
    mockTargetForExam,
    shortMockNotice,
    shuffleOptionsForQuestion,
} from '../../resources/js/pages/user/exams/utils/mock-pool';

// Item selection now happens on the server (MockPoolSelector, covered by
// Pest). The client keeps the option shuffle and the short-mock notice.

function item(id: number, extra: Partial<Question> = {}): Question {
    return {
        id,
        stem: `Question ${id}?`,
        options: [`A${id}`, `B${id}`, `C${id}`, `D${id}`],
        category: 'Verbal Ability',
        subcategory: 'Grammar',
        language: 'English',
        ...extra,
    };
}

describe('shuffleOptionsForQuestion', () => {
    it('keeps the option shuffle mapping intact when a key is present', () => {
        for (let id = 1; id <= 50; id++) {
            const original = item(id, { correct_option: id % 4 });
            const q = shuffleOptionsForQuestion(original);
            const indices = q.originalOptionIndices!;

            assert.equal(indices.length, original.options.length);
            indices.forEach((orig, shown) => {
                assert.equal(q.options[shown], original.options[orig]);
            });
            assert.equal(
                q.options[q.correct_option!],
                original.options[original.correct_option!],
            );
        }
    });

    it('never invents a key when the server withheld it', () => {
        const q = shuffleOptionsForQuestion(item(7));

        assert.equal('correct_option' in q, false);
        assert.equal('explanation' in q, false);
        assert.deepEqual([...q.originalOptionIndices!].sort(), [0, 1, 2, 3]);
    });
});

describe('mock levels', () => {
    it('maps exam IDs to the official level and item count', () => {
        assert.equal(mockLevelForExam(1), 'Professional');
        assert.equal(mockLevelForExam(2), 'Subprofessional');
        assert.equal(mockTargetForExam(1), 150);
        assert.equal(mockTargetForExam(2), 145);
    });
});

describe('shortMockNotice', () => {
    it('states the real count when a mock is short', () => {
        assert.equal(shortMockNotice(1, 150), null);
        assert.equal(shortMockNotice(2, 145), null);
        assert.equal(shortMockNotice(null, 3), null);
        assert.match(shortMockNotice(1, 120)!, /has 120 items, not 150/);
        assert.match(shortMockNotice(2, 0)!, /can't start/);
    });
});
