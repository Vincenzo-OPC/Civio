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

    it('has no redundant Mock button or free-exam picker modal', () => {
        assert.doesNotMatch(welcome, /Try Mock Test/);
        assert.doesNotMatch(welcome, /isFreeExamModalOpen/);
    });
});
