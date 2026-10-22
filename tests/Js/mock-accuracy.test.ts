import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';
import { summarizeMockAccuracy } from '../../resources/js/lib/mock-accuracy';

describe('summarizeMockAccuracy', () => {
    it('shows correct/total, sample, track and the policy split', () => {
        const s = summarizeMockAccuracy({
            correct: 285,
            total: 450,
            mocks: 3,
            percent: 63.3,
            tracks: ['Professional'],
            representative: { correct: 120, total: 150, mocks: 1, percent: 80 },
            personalized: {
                correct: 165,
                total: 300,
                mocks: 2,
                percent: 55,
                legacy: 1,
            },
        });
        assert.equal(s.display, '63.3%');
        assert.equal(s.counts, '285/450 correct');
        assert.equal(s.sample, '3 mocks, 450 scored questions');
        assert.equal(s.track, 'Professional');
        assert.match(
            s.strictLine,
            /^Strict \(representative\): 120\/150 correct \(80%\) in 1 mock$/,
        );
        assert.match(
            s.personalizedLine,
            /2 mocks, 1 from before policies were stored$/,
        );
    });

    it('never invents a number for missing or legacy payloads', () => {
        for (const input of [
            undefined,
            null,
            {},
            { pass_probability: 90 } as never,
        ]) {
            const s = summarizeMockAccuracy(input);
            assert.equal(s.hasMocks, false);
            assert.equal(s.percent, null);
            assert.equal(s.display, '—');
        }
    });
});

describe('learner-facing pass prediction is gone', () => {
    const files = [
        'resources/js/pages/user/dashboard/ai-analysis.tsx',
        'resources/js/pages/user/dashboard/components/ai-readiness-card.tsx',
        'resources/js/pages/user/dashboard/components/ai-readiness-bento-card.tsx',
        'resources/js/pages/user/dashboard/types.ts',
    ];
    for (const f of files) {
        it(f, () => {
            const src = readFileSync(f, 'utf8');
            assert.doesNotMatch(
                src,
                /pass(ing)?[ _]probability|days[ _]to[ _]readiness|estimated_exam_score|mock_pass_confidence/i,
            );
        });
    }
});
