// Issue #27: production caching lives in conf/nginx/civio-cache.conf and
// public/.htaccess, and is mirrored by the local perf proxy. Keep the three
// in step so a measured "after" number matches what production would send.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
// @ts-expect-error -- plain .mjs dev script without type declarations
import { cacheControlFor } from '../Perf/gzip-proxy.mjs';

const nginx = readFileSync('conf/nginx/civio-cache.conf', 'utf8');
const htaccess = readFileSync('public/.htaccess', 'utf8');
const dockerfile = readFileSync('Dockerfile', 'utf8');

test('hashed build assets are immutable for a year everywhere', () => {
    const value = 'public, max-age=31536000, immutable';
    assert.equal(cacheControlFor('/build/assets/app-abc123.js'), value);
    assert.match(
        nginx,
        /location \^~ \/build\/assets\/ \{\s+add_header Cache-Control "public, max-age=31536000, immutable" always;/,
    );
    assert.match(
        htaccess,
        /m#\^\/build\/assets\/#[\s\S]*?max-age=31536000, immutable/,
    );
});

test('unhashed manifests revalidate', () => {
    assert.equal(cacheControlFor('/build/manifest.json'), 'no-cache');
    assert.equal(cacheControlFor('/manifest.json'), 'no-cache');
    assert.match(
        nginx,
        /location = \/manifest\.json \{\s+add_header Cache-Control "no-cache" always;/,
    );
});

test('HTML, Inertia responses and the service worker are never given static rules', () => {
    for (const path of ['/', '/exams', '/sw.js', '/offline/pack/1']) {
        assert.equal(cacheControlFor(path), null, path);
    }
    assert.doesNotMatch(nginx, /location[^\n]*(sw\.js|\/exams|\/offline)/);
});

test('the Docker image installs the nginx cache rules', () => {
    assert.match(
        dockerfile,
        /COPY[^\n]*conf\/nginx\/civio-cache\.conf \/etc\/nginx\/server-opts\.d\/civio-cache\.conf/,
    );
});
