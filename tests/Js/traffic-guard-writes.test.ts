import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

// The global fetch guard retried any request that threw, POSTs included,
// three times over ~7 s while navigator.onLine was true. A Strict-mock save
// whose response was lost could be resent, and the offline queue only saw
// the failure seconds later. Writes must fail at once on a network error.
const src = readFileSync(
    new URL(
        '../../resources/js/components/shared/traffic-overload-guard.tsx',
        import.meta.url,
    ),
    'utf8',
);

describe('traffic overload guard', () => {
    it('does not retry a write after a network error', () => {
        const catchBlock = src.slice(src.indexOf('} catch (error) {'));
        assert.match(catchBlock, /method !== 'GET' && method !== 'HEAD'/);
        assert.ok(
            catchBlock.indexOf("method !== 'GET'") <
                catchBlock.indexOf('retries < maxRetries'),
            'the write check runs before any retry',
        );
    });
});
