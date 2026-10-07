import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import type { Question } from '../../resources/js/pages/user/exams/types';
import {
    buildMockScoredPool,
    exactItemKey,
    isVariantClone,
    MOCK_BLUEPRINT,
    shortMockNotice,
    shuffleOptionsForQuestion,
    uniqueMockSource,
} from '../../resources/js/pages/user/exams/utils/mock-pool';

let nextId = 1;

function item(
    category: string,
    subcategory: string,
    stem: string,
    extra: Partial<Question> = {},
): Question {
    const id = nextId++;

    return {
        id,
        stem,
        options: [`A${id}`, `B${id}`, `C${id}`, `D${id}`],
        correct_option: 0,
        category,
        subcategory,
        language: 'English',
        ...extra,
    };
}

/** n distinct items per subcategory, plus 7 "(variant N)" clones of each. */
function bank(
    layout: Record<string, Record<string, number>>,
    withClones = true,
): Question[] {
    const out: Question[] = [];

    for (const [category, subs] of Object.entries(layout)) {
        for (const [sub, n] of Object.entries(subs)) {
            for (let i = 1; i <= n; i++) {
                const base = item(
                    category,
                    sub,
                    `${sub} question number ${i} about topic ${i}?`,
                );
                out.push(base);

                if (withClones) {
                    for (let copy = 2; copy <= 8; copy++) {
                        out.push({
                            ...base,
                            id: nextId++,
                            stem: `${base.stem} (variant ${copy})`,
                        });
                    }
                }
            }
        }
    }

    return out;
}

const fullBank = {
    'Verbal Ability': { 'Word meaning': 30, 'Sentence completion': 30 },
    'Analytical Ability': { 'Word analogy': 30, 'Data interpretation': 30 },
    'Numerical Ability': { 'Basic operations': 30, 'Word problems': 30 },
    'Clerical Ability': { Filing: 30, Spelling: 30 },
    'General Information': { 'Philippine Constitution': 20 },
};

function assertUnique(items: Question[]) {
    assert.equal(
        new Set(items.map((q) => q.id)).size,
        items.length,
        'duplicate IDs',
    );
    assert.equal(
        new Set(items.map(exactItemKey)).size,
        items.length,
        'duplicate stem+options',
    );
}

describe('variant clones', () => {
    it('recognises "(variant N)" stems in any case and spacing', () => {
        assert.equal(isVariantClone({ stem: 'Pick one (variant 3)' }), true);
        assert.equal(isVariantClone({ stem: 'Pick one (VARIANT 12)' }), true);
        assert.equal(isVariantClone({ stem: 'Pick one (variant12)' }), true);
        assert.equal(
            isVariantClone({ stem: 'A variant spelling of colour' }),
            false,
        );
        assert.equal(isVariantClone({ stem: 'Pick one (variant)' }), false);
    });

    it('drops clones, exact copies and demographics from the source', () => {
        const a = item(
            'Numerical Ability',
            'Basic operations',
            'What is 2 + 2?',
        );
        const copy = { ...a, id: 999_001 };
        const clone = { ...a, id: 999_002, stem: 'What is 2 + 2? (variant 2)' };
        const demo = item('Demographic Profile', 'Age', 'Your age?');
        const source = uniqueMockSource([a, copy, clone, demo]);

        assert.deepEqual(
            source.map((q) => q.id),
            [a.id],
        );
    });

    it('keeps real items that share an opening but differ in options', () => {
        const s1 = item(
            'Clerical Ability',
            'Spelling',
            'Choose the correctly spelled word:',
        );
        const s2 = item(
            'Clerical Ability',
            'Spelling',
            'Choose the correctly spelled word:',
        );

        assert.equal(uniqueMockSource([s1, s2]).length, 2);
    });
});

describe('buildMockScoredPool', () => {
    for (const examId of [1, 2] as const) {
        const level = examId === 1 ? 'Professional' : 'Subprofessional';

        it(`fills a full ${level} mock from unique items only`, () => {
            const questions = bank(fullBank);
            const { items, target, short } = buildMockScoredPool(
                questions,
                examId,
            );

            assert.equal(target, examId === 1 ? 150 : 145);
            assert.equal(items.length, target);
            assert.equal(short, false);
            assert.equal(items.some(isVariantClone), false);
            assertUnique(items);

            for (const block of MOCK_BLUEPRINT[level]) {
                assert.equal(
                    items.filter((q) => q.category === block.category).length,
                    block.count,
                    block.category,
                );
            }
        });
    }

    it('gives a shorter mock, not a padded one, when the bank is short', () => {
        const questions = bank({
            'Verbal Ability': { 'Word meaning': 10 },
            'Analytical Ability': { 'Word analogy': 5 },
            'Numerical Ability': { 'Basic operations': 7 },
            'General Information': { 'Philippine Constitution': 3 },
            'Clerical Ability': { Filing: 40 },
        });
        const { items, target, short } = buildMockScoredPool(questions, 1);

        assert.equal(target, 150);
        assert.equal(short, true);
        assert.equal(items.length, 25);
        assert.equal(items.some(isVariantClone), false);
        assert.equal(
            items.some((q) => q.category === 'Clerical Ability'),
            false,
            'no cross-level padding',
        );
        assertUnique(items);
    });

    it('copes with an empty or clone-only bank without throwing', () => {
        const clonesOnly = bank({
            'Verbal Ability': { 'Word meaning': 3 },
        }).filter(isVariantClone);

        assert.deepEqual(buildMockScoredPool([], 2).items, []);
        assert.deepEqual(buildMockScoredPool(clonesOnly, 2).items, []);
    });

    it('still leans toward wrong items and weak categories', () => {
        const questions = bank(fullBank, false);
        const wrongIds = questions
            .filter((q) => q.subcategory === 'Word meaning')
            .slice(0, 20)
            .map((q) => q.id);
        const counts = { wrong: 0, numerical: 0 };
        const runs = 20;

        for (let r = 0; r < runs; r++) {
            const { items } = buildMockScoredPool(questions, 1, {
                seenIds: questions.map((q) => q.id),
                wrongIds,
                weakCategories: ['Numerical Ability'],
            });
            counts.wrong += items.filter((q) => wrongIds.includes(q.id)).length;
            counts.numerical += items.filter(
                (q) => q.category === 'Numerical Ability',
            ).length;
            assertUnique(items);
        }

        // Word meaning gets ~22-23 slots; at least half go to the 20 wrong items.
        assert.ok(
            counts.wrong / runs >= 11,
            `wrong share ${counts.wrong / runs}`,
        );
        // Half of 150 should be the weak category (60 Numerical items exist).
        assert.ok(
            counts.numerical / runs >= 60,
            `weak share ${counts.numerical / runs}`,
        );
    });

    it('keeps the option shuffle mapping intact', () => {
        const questions = bank(fullBank, false);
        const { items } = buildMockScoredPool(questions, 2);
        const byId = new Map(questions.map((q) => [q.id, q]));

        for (const q of items.map(shuffleOptionsForQuestion)) {
            const original = byId.get(q.id)!;
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
