import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    createGuardedFetch,
    requestMethod,
} from '../../resources/js/lib/guarded-fetch.ts';

// Behavioural: a mocked fetch counts calls. Only GET/HEAD may be retried;
// a write is sent exactly once whether it gets 429/502/503/504 or throws.
type Script = Array<number | 'throw'>;

function harness(script: Script, offline = false) {
    const calls: string[] = [];
    const events: string[] = [];
    let i = 0;
    const fake = (async (input: RequestInfo | URL, init?: RequestInit) => {
        calls.push(requestMethod(input, init));
        const step = script[Math.min(i++, script.length - 1)];

        if (step === 'throw') {
            throw new TypeError('Failed to fetch');
        }

        return new Response('x', { status: step });
    }) as typeof fetch;
    const guarded = createGuardedFetch(
        fake,
        {
            onRetrying: (r) => events.push(`retrying:${r}`),
            onFailure: (t) => events.push(`failure:${t}`),
        },
        { sleep: async () => {}, isOffline: () => offline },
    );

    return { guarded, calls, events };
}

const WRITES = ['POST', 'PATCH', 'PUT', 'DELETE'];
const STATUSES = [429, 502, 503, 504];

describe('traffic overload guard: writes are never replayed', () => {
    for (const method of WRITES) {
        for (const status of STATUSES) {
            it(`${method} with HTTP ${status} is sent once and returned`, async () => {
                const h = harness([status, 200]);
                const res = await h.guarded('/x', { method });
                assert.equal(h.calls.length, 1);
                assert.equal(res.status, status, 'failure is not masked');
                assert.deepEqual(h.events, [
                    `failure:${status === 429 ? 'rate_limit' : 'overload'}`,
                ]);
            });
        }

        it(`${method} network error is thrown after one call`, async () => {
            const h = harness(['throw', 200]);
            await assert.rejects(h.guarded('/x', { method }), TypeError);
            assert.equal(h.calls.length, 1);
            assert.deepEqual(h.events, []);
        });

        it(`${method} via Request input is sent once`, async () => {
            const h = harness([503, 200]);
            const req = new Request('http://t/x', {
                method,
                body: method === 'DELETE' ? null : 'a=1',
            });
            const res = await h.guarded(req);
            assert.equal(h.calls.length, 1);
            assert.equal(res.status, 503);
        });
    }

    it('lowercase init.method is normalised', async () => {
        const h = harness([502, 200]);
        await h.guarded('/x', { method: 'post' });
        assert.equal(h.calls.length, 1);
    });

    it('init.method overrides Request.method', async () => {
        assert.equal(
            requestMethod(new Request('http://t/x'), { method: 'post' }),
            'POST',
        );
        assert.equal(
            requestMethod(
                new Request('http://t/x', { method: 'PUT', body: 'a' }),
            ),
            'PUT',
        );
        assert.equal(requestMethod('/x'), 'GET');
        const h = harness([429, 200]);
        await h.guarded(new Request('http://t/x'), { method: 'POST' });
        assert.equal(h.calls.length, 1);
    });
});

describe('traffic overload guard: reads keep retrying', () => {
    for (const status of STATUSES) {
        it(`GET with HTTP ${status} retries then succeeds`, async () => {
            const h = harness([status, status, 200]);
            const res = await h.guarded('/x');
            assert.equal(res.status, 200);
            assert.equal(h.calls.length, 3);
            assert.deepEqual(h.events, [
                'retrying:true',
                'retrying:true',
                'retrying:false',
            ]);
        });
    }

    it('GET gives up after 3 retries with overload feedback', async () => {
        const h = harness([503]);
        const res = await h.guarded('/x');
        assert.equal(res.status, 503);
        assert.equal(h.calls.length, 4);
        assert.equal(h.events.at(-1), 'failure:overload');
    });

    it('HEAD 429 retries and ends in rate_limit feedback', async () => {
        const h = harness([429]);
        await h.guarded('/x', { method: 'HEAD' });
        assert.equal(h.calls.length, 4);
        assert.equal(h.events.at(-1), 'failure:rate_limit');
    });

    it('GET network error retries then recovers', async () => {
        const h = harness(['throw', 200]);
        const res = await h.guarded(new Request('http://t/x'));
        assert.equal(res.status, 200);
        assert.equal(h.calls.length, 2);
    });

    it('GET network error while offline fails at once', async () => {
        const h = harness(['throw', 200], true);
        await assert.rejects(h.guarded('/x'));
        assert.equal(h.calls.length, 1);
    });

    it('Inertia 503 (maintenance) is not retried', async () => {
        const calls: number[] = [];
        const g = createGuardedFetch(
            (async () => {
                calls.push(1);
                return new Response('', {
                    status: 503,
                    headers: { 'x-inertia': 'true' },
                });
            }) as typeof fetch,
            { onRetrying: () => {}, onFailure: () => {} },
            { sleep: async () => {} },
        );
        await g('/x');
        assert.equal(calls.length, 1);
    });
});
