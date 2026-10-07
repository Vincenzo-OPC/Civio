import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    combinedStudyBias,
    mergeTrackBias,
    pickDrillItemsWithBias,
    studyBiasInputFromServer,
    studyTrackForExam,
} from '../../resources/js/lib/guest-study-bias';
import type { TrackBias } from '../../resources/js/lib/guest-study-bias';

const identity = <U>(items: U[]): U[] => [...items];

const empty: TrackBias = {
    wrongIds: [],
    weakCategories: [],
    weakSubcategories: [],
};

describe('studyBiasInputFromServer', () => {
    it('returns null when the server did not grade (keys withheld)', () => {
        assert.equal(studyBiasInputFromServer(null), null);
        assert.equal(studyBiasInputFromServer({ success: false }), null);
        assert.equal(studyBiasInputFromServer({ success: true }), null);
    });

    it('uses server wrong ids and derives correct ids from answer keys', () => {
        const input = studyBiasInputFromServer({
            success: true,
            cat_scores: {
                categoryScoreMap: {
                    'Numerical Ability': {
                        correct: 1,
                        total: 3,
                        subcats: { 'Word problems': { correct: 1, total: 3 } },
                    },
                },
                metadata: { wrong_question_ids: [11, 12] },
            },
            answer_keys: [
                { id: 10, correct_option: 2 },
                { id: 11, correct_option: 0 },
                { id: 12, correct_option: 1 },
            ],
            // Original (bank) option indexes, keyed by question id.
            answers: { '10': 2, '11': 3, '12': null },
        });

        assert.ok(input);
        assert.deepEqual(input.wrongIds, [11, 12]);
        assert.deepEqual(input.correctIds, [10]);
    });
});

describe('mergeTrackBias', () => {
    it('adds new misses first and drops items now answered correctly', () => {
        const next = mergeTrackBias(
            { ...empty, wrongIds: [1, 2, 3] },
            { wrongIds: [9], correctIds: [2], categoryScoreMap: {} },
        );
        assert.deepEqual(next.wrongIds, [9, 1, 3]);
    });

    it('re-judges covered topics and keeps uncovered weak topics', () => {
        const next = mergeTrackBias(
            {
                wrongIds: [],
                weakCategories: ['Numerical Ability', 'Verbal Ability'],
                weakSubcategories: ['Word problems', 'Spelling'],
            },
            {
                wrongIds: [],
                categoryScoreMap: {
                    // 9/10 = strong now: no longer weak.
                    'Numerical Ability': {
                        correct: 9,
                        total: 10,
                        subcats: { 'Word problems': { correct: 9, total: 10 } },
                    },
                    // 1/4 = weak.
                    'Analytical Ability': {
                        correct: 1,
                        total: 4,
                        subcats: { 'Word analogy': { correct: 1, total: 4 } },
                    },
                },
            },
        );

        assert.deepEqual(next.weakCategories, [
            'Analytical Ability',
            'Verbal Ability',
        ]);
        assert.deepEqual(next.weakSubcategories, ['Word analogy', 'Spelling']);
    });
});

describe('combinedStudyBias', () => {
    it('unions every track without duplicates', () => {
        const merged = combinedStudyBias({
            Professional: {
                wrongIds: [1, 2],
                weakCategories: ['Numerical Ability'],
                weakSubcategories: ['Word problems'],
            },
            Subprofessional: {
                wrongIds: [2, 3],
                weakCategories: ['Clerical Ability'],
                weakSubcategories: [],
            },
            Drill: { ...empty, wrongIds: [4] },
        });

        assert.deepEqual(merged.wrongIds, [1, 2, 3, 4]);
        assert.deepEqual(merged.weakCategories, [
            'Numerical Ability',
            'Clerical Ability',
        ]);
    });
});

describe('pickDrillItemsWithBias', () => {
    const pool = Array.from({ length: 20 }, (_, i) => ({
        id: i + 1,
        category: 'Numerical Ability',
        subcategory: i < 10 ? 'Basic operations' : 'Word problems',
    }));

    it('serves past misses first, then weak topics, up to half the drill', () => {
        const picked = pickDrillItemsWithBias(
            pool,
            {
                wrongIds: [20, 19],
                weakCategories: [],
                weakSubcategories: ['Word problems'],
            },
            10,
            identity,
        );

        assert.equal(picked.length, 10);
        // 5 priority slots: misses 19, 20 then weak-topic items 11, 12, 13.
        assert.deepEqual(
            picked.slice(0, 5).map((q) => q.id),
            [19, 20, 11, 12, 13],
        );
        // The rest still covers non-weak ground.
        assert.deepEqual(
            picked.slice(5).map((q) => q.id),
            [1, 2, 3, 4, 5],
        );
    });

    it('fills from leftover weak items when the rest of the pool runs out', () => {
        const small = pool.slice(9, 14); // ids 10..14
        const picked = pickDrillItemsWithBias(
            small,
            { ...empty, weakSubcategories: ['Word problems'] },
            5,
            identity,
        );
        assert.deepEqual(
            picked.map((q) => q.id).sort((a, b) => a - b),
            [10, 11, 12, 13, 14],
        );
    });

    it('never returns duplicates or more than the pool holds', () => {
        const picked = pickDrillItemsWithBias(
            pool.slice(0, 3),
            { ...empty, wrongIds: [1] },
            30,
        );
        assert.equal(picked.length, 3);
        assert.equal(new Set(picked.map((q) => q.id)).size, 3);
    });

    it('is a plain sample when there is no bias yet', () => {
        const picked = pickDrillItemsWithBias(pool, empty, 4, identity);
        assert.deepEqual(
            picked.map((q) => q.id),
            [1, 2, 3, 4],
        );
    });
});

describe('studyTrackForExam', () => {
    it('maps exams 1 and 2 to the strict tracks and everything else to Drill', () => {
        assert.equal(studyTrackForExam(1), 'Professional');
        assert.equal(studyTrackForExam(2), 'Subprofessional');
        assert.equal(studyTrackForExam(null), 'Drill');
        assert.equal(studyTrackForExam(7), 'Drill');
    });
});
