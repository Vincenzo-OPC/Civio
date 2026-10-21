import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { reviewMistakesCopy } from '../../resources/js/lib/review-mistakes.ts';

describe('review mistakes copy', () => {
    it('explains the reminder and does not claim mastery or readiness', () => {
        const copy = reviewMistakesCopy();
        const text =
            `${copy.title} ${copy.note} ${copy.due} ${copy.upcoming} ${copy.needs} ${copy.complete} ${copy.empty} ${copy.reminderFailed} ${copy.reminderRetry}`.toLowerCase();

        assert.match(text, /before you forget/);
        assert.match(text, /due today/);
        assert.match(text, /upcoming reviews/);
        assert.match(text, /needs review/);
        assert.match(text, /review complete/);
        assert.match(text, /your answer was saved/);
        assert.match(text, /the next reminder was not/);
        assert.equal(text.includes('mastery'), false);
        assert.equal(text.includes('readiness'), false);
        assert.equal(text.includes('fsrs'), false);
    });
});
