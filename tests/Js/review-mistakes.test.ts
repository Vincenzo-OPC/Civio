import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { reviewMistakesCopy } from '../../resources/js/lib/review-mistakes.ts';

describe('review mistakes copy', () => {
    it('calls the list practice history and does not claim mastery or readiness', () => {
        const copy = reviewMistakesCopy();
        const text = `${copy.title} ${copy.note}`.toLowerCase();

        assert.match(text, /practice history/);
        assert.equal(text.includes('mastery'), false);
        assert.equal(text.includes('readiness'), false);
    });
});
