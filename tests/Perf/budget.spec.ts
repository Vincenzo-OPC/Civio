import { expect, test } from '@playwright/test';
import { resetLimits, openFirstQuestion } from './flows';
import { NetLog, kb, setLite } from './lib';

/**
 * Deterministic low-end budget (Issue #27). Bytes and request counts only,
 * no timings, so it cannot flake on a slow runner. Numbers are gzip bytes on
 * the wire through tests/Perf/gzip-proxy.mjs with the production cache rules.
 * Measured 2026-10-23 (after): cold 401.3 KB / 76 requests, images 8 KB,
 * script 332.4 KB, warm 1.4-7.4 KB / 1-3 wire requests (Lite off/on). See docs/PERFORMANCE_REPORT.md.
 */
const BUDGET = {
    coldKB: 420,
    coldRequests: 80,
    scriptKB: 345,
    imageKB: 16,
    warmKB: 12,
    warmWireRequests: 3,
};

test.skip(!!process.env.PERF_MEASURE, 'measurement run');

for (const lite of [false, true]) {
    test(`first Strict Mock question stays within the data budget (lite=${lite})`, async ({
        browser,
    }) => {
        resetLimits();
        const ctx = await browser.newContext({
            viewport: { width: 360, height: 740 },
            hasTouch: true,
        });
        await setLite(ctx, lite);
        const p = await ctx.newPage();
        const log = await NetLog.attach(p);

        await openFirstQuestion(p);
        const cold = log.totals();
        expect
            .soft(kb(cold.bytes), 'cold KB')
            .toBeLessThanOrEqual(BUDGET.coldKB);
        expect
            .soft(cold.requests, 'cold requests')
            .toBeLessThanOrEqual(BUDGET.coldRequests);
        expect
            .soft(kb(cold.byType.Script ?? 0), 'script KB')
            .toBeLessThanOrEqual(BUDGET.scriptKB);
        expect
            .soft(kb(cold.byType.Image ?? 0), 'image KB')
            .toBeLessThanOrEqual(BUDGET.imageKB);

        const mark = log.mark();
        await openFirstQuestion(p);
        const warm = log.totals(mark);
        expect
            .soft(kb(warm.bytes), 'warm KB')
            .toBeLessThanOrEqual(BUDGET.warmKB);
        expect
            .soft(warm.wireRequests, 'warm wire requests')
            .toBeLessThanOrEqual(BUDGET.warmWireRequests);
        await ctx.close();
    });
}
