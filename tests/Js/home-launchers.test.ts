import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

// MSI desktop patch: Home offers Start Pro, Start Sub Pro and Practice Drills.
// The separate "Try Mock Test" button (which opened a duplicate track picker)
// was removed. Guard against it coming back.
const welcome = readFileSync(
    new URL('../../resources/js/pages/public/welcome.tsx', import.meta.url),
    'utf8',
);

describe('home launchers', () => {
    it('offers Start Pro, Start Sub Pro and Practice Drills', () => {
        assert.match(welcome, /Start Pro\b/);
        assert.match(welcome, /Start Sub Pro\b/);
        assert.match(welcome, /Practice Drills/);
    });

    it('does not bring back the marketing essay or a fake question count', () => {
        assert.doesNotMatch(welcome, /Turning dreams/);
        assert.doesNotMatch(welcome, /2000\+/);
        assert.doesNotMatch(welcome, /Tools Built for Success/);
        assert.doesNotMatch(welcome, /guaranteed points/);
        assert.match(welcome, /Continue Studying/);
        assert.match(welcome, /at least 80\.00/);
    });

    it('has no redundant Mock button or free-exam picker modal', () => {
        assert.doesNotMatch(welcome, /Try Mock Test/);
        assert.doesNotMatch(welcome, /isFreeExamModalOpen/);
    });
});
