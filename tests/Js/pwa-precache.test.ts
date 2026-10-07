import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
    collectCriticalFiles,
    keepPrecacheEntry,
    PRECACHE_ROOTS,
    toBuildUrl,
} from '../../resources/js/lib/pwa-precache';
import type { ViteManifest } from '../../resources/js/lib/pwa-precache';

const manifest: ViteManifest = {
    'resources/js/app.tsx': {
        file: 'assets/app-1.js',
        imports: ['_vendor-react.js'],
        css: ['assets/app-1.css'],
    },
    '_vendor-react.js': { file: 'assets/vendor-react-1.js' },
    'resources/js/pages/user/exams/index.tsx': {
        file: 'assets/exams-1.js',
        imports: ['_button.js', 'resources/js/app.tsx'],
    },
    '_button.js': { file: 'assets/button-1.js' },
    'resources/js/pages/admin/dashboard/index.tsx': {
        file: 'assets/index-admin.js',
        imports: ['_chart.js'],
    },
    '_chart.js': { file: 'assets/chart-1.js' },
};

test('collects static imports and css of the roots, following cycles once', () => {
    const files = collectCriticalFiles(manifest, [
        'resources/js/app.tsx',
        'resources/js/pages/user/exams/index.tsx',
    ]);

    assert.deepEqual([...files].sort(), [
        'assets/app-1.css',
        'assets/app-1.js',
        'assets/button-1.js',
        'assets/exams-1.js',
        'assets/vendor-react-1.js',
    ]);
});

test('admin pages, charts and unknown roots are not precached', () => {
    const files = collectCriticalFiles(manifest, [
        'resources/js/app.tsx',
        'resources/js/pages/missing.tsx',
    ]);

    assert.equal(keepPrecacheEntry('assets/index-admin.js', files), false);
    assert.equal(keepPrecacheEntry('assets/chart-1.js', files), false);
    assert.equal(keepPrecacheEntry('assets/app-1.js', files), true);
});

test('normalises url prefixes; files outside the critical graph are dropped', () => {
    const files = collectCriticalFiles(manifest, ['resources/js/app.tsx']);

    assert.equal(keepPrecacheEntry('/build/assets/app-1.js', files), true);
    assert.equal(keepPrecacheEntry('./assets/app-1.js', files), true);
    assert.equal(keepPrecacheEntry('icons/icon-512x512.png', files), false);
    assert.equal(keepPrecacheEntry('images/hero_image.png', files), false);
});

test('precache urls are absolute under /build/ (the worker is served from /sw.js)', () => {
    assert.equal(toBuildUrl('assets/app-1.js'), '/build/assets/app-1.js');
    assert.equal(toBuildUrl('./assets/app-1.js'), '/build/assets/app-1.js');
    assert.equal(
        toBuildUrl('/build/assets/app-1.js'),
        '/build/assets/app-1.js',
    );
});

test('the offline drill page is precached so it opens with no network', () => {
    assert.ok(PRECACHE_ROOTS.includes('resources/js/pages/offline/index.tsx'));
});
