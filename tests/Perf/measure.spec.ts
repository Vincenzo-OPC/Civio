/**
 * Records low-end performance numbers to tests/Perf/results/*.json.
 * Not a CI gate: timings depend on the host. Run with
 *   PERF_MEASURE=1 PERF_LABEL=before npx playwright test -c playwright.perf.config.ts measure
 */
import fs from 'node:fs';
import { expect, test } from '@playwright/test';
import { openFirstQuestion, resetLimits, firstOption } from './flows';
import { NetLog, installVitals, readVitals, setLite, kb } from './lib';
import type { NetworkName } from './lib';

test.skip(
    !process.env.PERF_MEASURE,
    'set PERF_MEASURE=1 to record measurements',
);
test.describe.configure({ mode: 'serial' });

const label = process.env.PERF_LABEL || 'run';
const out: Record<string, unknown> = {
    label,
    at: new Date().toISOString(),
    runs: {},
};
const runs = out.runs as Record<string, unknown>;
const save = () => {
    fs.mkdirSync('tests/Perf/results', { recursive: true });
    fs.writeFileSync(
        `tests/Perf/results/${label}.json`,
        JSON.stringify(out, null, 2),
    );
};

const matrix: [NetworkName, number][] = [
    ['none', 1],
    ['400kbps', 4],
    ['400kbps', 6],
    ['250kbps', 4],
    ['250kbps', 6],
];

for (const lite of [false, true]) {
    for (const [net, cpu] of matrix) {
        const name = `exam-cold+warm lite=${lite ? 'on' : 'off'} net=${net} cpu=${cpu}x`;
        test(name, async ({ browser }) => {
            resetLimits();
            const ctx = await browser.newContext({
                viewport: { width: 360, height: 740 },
                hasTouch: true,
            });
            await setLite(ctx, lite);
            await installVitals(ctx);
            const p = await ctx.newPage();
            const log = await NetLog.attach(p, net, cpu);
            const cold = await openFirstQuestion(p);
            await p.waitForTimeout(1500);
            const coldVitals = await readVitals(p);
            const coldNet = log.totals();
            const coldHeap = await log.heapMB();

            // Let the service worker (if any) finish precaching, then count it.
            await p.waitForTimeout(net === 'none' ? 3000 : 20000);
            const afterIdle = log.totals();

            // Warm: a second visit in the same browser profile.
            const mark = log.mark();
            const warm = await openFirstQuestion(p);
            await p.waitForTimeout(1000);
            const warmNet = log.totals(mark);
            const warmVitals = await readVitals(p);

            runs[name] = {
                lite,
                net,
                cpu,
                served: cold.session?.questions.length ?? 0,
                cold: {
                    setupVisibleMs: cold.tSetup,
                    firstQuestionMs: cold.tFirstQuestion,
                    kb: kb(coldNet.bytes),
                    requests: coldNet.requests,
                    byTypeKB: Object.fromEntries(
                        Object.entries(coldNet.byType).map(([k, v]) => [
                            k,
                            kb(v),
                        ]),
                    ),
                    lcpMs: Math.round(coldVitals.lcp),
                    cls: Math.round(coldVitals.cls * 1000) / 1000,
                    tbtMs: Math.round(coldVitals.tbt),
                    longTasks: coldVitals.longTasks,
                    heapMB: coldHeap,
                },
                backgroundAfterFirstQuestionKB: kb(
                    afterIdle.bytes - coldNet.bytes,
                ),
                warm: {
                    resumedUnfinishedMock: warm.resumed,
                    firstQuestionMs: warm.tFirstQuestion,
                    kb: kb(warmNet.bytes),
                    requests: warmNet.requests,
                    wireRequests: warmNet.wireRequests,
                    lcpMs: Math.round(warmVitals.lcp),
                    cls: Math.round(warmVitals.cls * 1000) / 1000,
                },
            };
            save();
            await ctx.close();
        });
    }
}

test('full strict mock: incremental data after first question, INP proxy at 6x CPU', async ({
    browser,
}) => {
    resetLimits();
    const ctx = await browser.newContext({
        viewport: { width: 360, height: 740 },
        hasTouch: true,
    });
    await setLite(ctx, true);
    await installVitals(ctx);
    const p = await ctx.newPage();
    const log = await NetLog.attach(p, 'none', 6);
    const { session } = await openFirstQuestion(p);
    const mark = log.mark();
    const n = session.questions.length as number;
    const next = p.getByRole('button', { name: 'Next' });

    for (let i = 0; i < n; i++) {
        await firstOption(p).click();

        if (i < n - 1) {
            await next.click();
        }
    }

    await p.waitForTimeout(2000);
    const answered = log.totals(mark);
    const heap = await log.heapMB();
    const v = await readVitals(p);
    // Submit and load the scorecard.
    const before = log.mark();
    await p
        .getByRole('button', { name: /Submit|Finish/i })
        .first()
        .click();
    const confirm = p
        .getByRole('button', { name: /Submit|Finish|Confirm/i })
        .last();
    await confirm.click({ timeout: 5000 }).catch(() => undefined);
    await p.waitForLoadState('networkidle');
    await p.waitForTimeout(2000);
    const submitted = log.totals(before);
    const writes = answered.list.filter((r) => r.method !== 'GET');
    runs['full-mock'] = {
        served: n,
        answeringKB: kb(answered.bytes),
        answeringRequests: answered.requests,
        writeRequests: writes.length,
        submitAndScorecardKB: kb(submitted.bytes),
        submitRequests: submitted.requests,
        totalIncrementalKB: kb(answered.bytes + submitted.bytes),
        perItemBytes: Math.round((answered.bytes + submitted.bytes) / n),
        projected150KB: kb(((answered.bytes + submitted.bytes) / n) * 150),
        maxInteractionMs: Math.round(v.inp),
        tbtMs: Math.round(v.tbt),
        heapAfterMockMB: heap,
        urls: [
            ...new Set(
                answered.list
                    .concat(submitted.list)
                    .map((r) => `${r.method} ${new URL(r.url).pathname}`),
            ),
        ],
    };
    save();
    expect(n).toBeGreaterThan(0);
    await ctx.close();
});

test('intermittent: 400 kbps, drop to offline for 5 answers, reconnect', async ({
    browser,
}) => {
    resetLimits();
    const ctx = await browser.newContext({
        viewport: { width: 360, height: 740 },
        hasTouch: true,
    });
    await setLite(ctx, true);
    const p = await ctx.newPage();
    const log = await NetLog.attach(p, '400kbps', 4);
    const { session } = await openFirstQuestion(p);
    const next = p.getByRole('button', { name: 'Next' });
    await firstOption(p).click();
    await next.click();
    await log.offline(true);
    await ctx.setOffline(true);
    const offlineMark = log.mark();

    for (let i = 0; i < 5; i++) {
        await firstOption(p).click();
        await next.click();
    }

    const offlineAttempts = log.totals(offlineMark).requests;
    await log.offline(false);
    await ctx.setOffline(false);
    await log.cdp.send('Network.emulateNetworkConditions', {
        offline: false,
        latency: 300,
        downloadThroughput: 50_000,
        uploadThroughput: 25_000,
    });
    const t = Date.now();
    await p.evaluate(() => window.dispatchEvent(new Event('online')));
    const sid = session.session_id as string;
    let saved = 0;
    await expect
        .poll(
            async () => {
                const r = await p.evaluate(async (sid) => {
                    // Use the live XSRF-TOKEN cookie (as axios/Inertia do); the meta tag can be stale.
                    const token = decodeURIComponent(
                        document.cookie.match(
                            /(?:^|; )XSRF-TOKEN=([^;]*)/,
                        )?.[1] ?? '',
                    );
                    const res = await fetch('/exams/sessions/progress', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            Accept: 'application/json',
                            'X-XSRF-TOKEN': token,
                        },
                        body: JSON.stringify({ exam_session_id: sid }),
                    });

                    return {
                        status: res.status,
                        ...(res.ok ? await res.json() : {}),
                    };
                }, sid);
                saved = Object.values(r.answers ?? {}).filter(
                    (x) => x !== null,
                ).length;

                return saved;
            },
            { timeout: 60_000 },
        )
        .toBeGreaterThanOrEqual(6)
        // Recorded, not asserted: see docs/PERFORMANCE_REPORT.md (offline
        // before the progress-save chunk loads leaves saves stuck).
        .catch(() => undefined);
    runs.intermittent = {
        answeredOffline: 5,
        requestsWhileOffline: offlineAttempts,
        savedAfterReconnect: saved,
        resyncMs: Date.now() - t,
    };
    save();
    await ctx.close();
});

test('offline practice: download one pack, practise offline, sync', async ({
    browser,
}) => {
    resetLimits();
    const ctx = await browser.newContext({
        viewport: { width: 360, height: 740 },
        hasTouch: true,
    });
    await setLite(ctx, true);
    const p = await ctx.newPage();
    const log = await NetLog.attach(p, '400kbps', 4);
    await p.goto('/drills');
    await p
        .getByRole('button', { name: /^Download/ })
        .first()
        .waitFor({ timeout: 120_000 });
    const pageLoad = log.totals();
    const m = log.mark();
    await p
        .getByRole('button', { name: /^Download/ })
        .first()
        .click();
    await p.waitForTimeout(15000);
    const pack = log.totals(m);
    runs['offline-pack'] = {
        drillsPageKB: kb(pageLoad.bytes),
        drillsPageRequests: pageLoad.requests,
        packDownloadKB: kb(pack.bytes),
        packRequests: pack.requests,
        packUrls: pack.list.map(
            (r) =>
                `${r.method} ${new URL(r.url).pathname} ${kb(r.cached || r.sw ? 0 : r.bytes)}KB`,
        ),
    };
    save();
    await ctx.close();
});
