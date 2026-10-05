import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    initCard,
    previewRatings,
    scheduleAfterAnswer,
} from '../../resources/js/lib/review/fsrs';

describe('fsrs wrapper', () => {
    it('initCard returns a new due card', () => {
        const now = new Date('2026-10-05T09:00:00.000Z');
        const card = initCard(now);
        assert.equal(card.state, 'new');
        assert.ok(card.due);
        assert.ok(card.card);
    });

    it('scheduleAfterAnswer advances due date on Good', () => {
        const now = new Date('2026-10-05T09:00:00.000Z');
        const card = initCard(now);
        const { next } = scheduleAfterAnswer(card, 'good', now);
        assert.notEqual(next.due, card.due);
        assert.ok(new Date(next.due).getTime() >= now.getTime());
    });

    it('previewRatings returns four branches', () => {
        const now = new Date('2026-10-05T09:00:00.000Z');
        const card = initCard(now);
        const preview = previewRatings(card, now);
        assert.ok(preview.again);
        assert.ok(preview.hard);
        assert.ok(preview.good);
        assert.ok(preview.easy);
    });
});
