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
const about = readFileSync(
    new URL('../../resources/js/pages/public/about.tsx', import.meta.url),
    'utf8',
);
const footer = readFileSync(
    new URL(
        '../../resources/js/components/layout/site-footer.tsx',
        import.meta.url,
    ),
    'utf8',
);
const guide = readFileSync(
    new URL(
        '../../resources/js/components/domain/reviewer-guide-tabs.tsx',
        import.meta.url,
    ),
    'utf8',
);
const shell = readFileSync(
    new URL('../../resources/views/app.blade.php', import.meta.url),
    'utf8',
);
const brand = readFileSync(
    new URL(
        '../../resources/js/components/shared/brand-name.tsx',
        import.meta.url,
    ),
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
        assert.match(welcome, /The explanation comes after/);
        assert.doesNotMatch(welcome, /help you improve/);
    });

    it('has no redundant Mock button or free-exam picker modal', () => {
        assert.doesNotMatch(welcome, /Try Mock Test/);
        assert.doesNotMatch(welcome, /isFreeExamModalOpen/);
    });

    it('keeps the name Civio and the about page factual', () => {
        assert.doesNotMatch(brand, /Review/);
        assert.doesNotMatch(about, /My Story/);
        assert.doesNotMatch(about, /Empowering Filipinos/);
        assert.match(about, /not the Civil Service Commission/);
        assert.match(footer, /All Rights Reserved/);
        assert.match(footer, /bir-registered-2025/);
        assert.doesNotMatch(footer, /tax registration/);
        assert.doesNotMatch(footer, /not affiliated/);
        assert.doesNotMatch(footer, /any Philippine government agency/);
        assert.doesNotMatch(shell, /Ace the/);
        assert.doesNotMatch(shell, /first attempt/);
        assert.doesNotMatch(guide, /dual-stage/);
        assert.doesNotMatch(guide, /passing mark/);
        assert.match(guide, /150/);
        assert.match(guide, /at least 80\.00/);
    });
});
