import type { BrowserContext, CDPSession, Page } from '@playwright/test';

/** CDP network profiles (bytes/second). Latency is round-trip ms. */
export const NETWORKS = {
    none: null,
    '400kbps': {
        latency: 300,
        downloadThroughput: 400_000 / 8,
        uploadThroughput: 200_000 / 8,
    },
    '250kbps': {
        latency: 400,
        downloadThroughput: 250_000 / 8,
        uploadThroughput: 100_000 / 8,
    },
} as const;
export type NetworkName = keyof typeof NETWORKS;

export type Req = {
    url: string;
    type: string;
    bytes: number;
    status: number;
    cached: boolean;
    sw: boolean;
    method: string;
};

/** Counts every request and its on-the-wire (encoded) bytes via CDP. */
export class NetLog {
    reqs = new Map<string, Req>();
    cdp!: CDPSession;

    static async attach(page: Page, net: NetworkName = 'none', cpu = 1) {
        const log = new NetLog();
        log.cdp = await page.context().newCDPSession(page);
        await log.cdp.send('Network.enable');
        const n = NETWORKS[net];

        if (n) {
            await log.cdp.send('Network.emulateNetworkConditions', {
                offline: false,
                ...n,
            });
        }

        if (cpu > 1) {
            await log.cdp.send('Emulation.setCPUThrottlingRate', { rate: cpu });
        }

        log.cdp.on('Network.requestWillBeSent', (e) => {
            log.reqs.set(e.requestId, {
                url: e.request.url,
                type: e.type ?? 'Other',
                bytes: 0,
                status: 0,
                cached: false,
                sw: false,
                method: e.request.method,
            });
        });
        log.cdp.on('Network.responseReceived', (e) => {
            const r = log.reqs.get(e.requestId);

            if (r) {
                r.status = e.response.status;
                r.cached =
                    !!e.response.fromDiskCache ||
                    !!e.response.fromPrefetchCache;
                r.sw = !!e.response.fromServiceWorker;
            }
        });
        log.cdp.on('Network.requestServedFromCache', (e) => {
            const r = log.reqs.get(e.requestId);

            if (r) {
                r.cached = true;
            }
        });
        log.cdp.on('Network.loadingFinished', (e) => {
            const r = log.reqs.get(e.requestId);

            if (r) {
                r.bytes = e.encodedDataLength;
            }
        });

        return log;
    }

    async offline(on: boolean) {
        await this.cdp.send('Network.emulateNetworkConditions', {
            offline: on,
            latency: 0,
            downloadThroughput: -1,
            uploadThroughput: -1,
        });
    }

    mark() {
        return new Set(this.reqs.keys());
    }

    /** Totals, optionally only for requests not in `since`. Cache/SW hits count 0 wire bytes. */
    totals(since?: Set<string>) {
        const out = {
            requests: 0,
            wireRequests: 0,
            bytes: 0,
            byType: {} as Record<string, number>,
            list: [] as Req[],
        };

        for (const [id, r] of this.reqs) {
            if (since?.has(id) || r.url.startsWith('data:')) {
                continue;
            }

            out.requests++;
            const wire = r.cached || r.sw ? 0 : r.bytes;

            if (wire > 0) {
                out.wireRequests++;
            }

            out.bytes += wire;
            out.byType[r.type] = (out.byType[r.type] ?? 0) + wire;
            out.list.push(r);
        }

        return out;
    }

    async heapMB() {
        await this.cdp.send('Performance.enable');
        const m = await this.cdp.send('Performance.getMetrics');
        const v =
            m.metrics.find((x) => x.name === 'JSHeapUsedSize')?.value ?? 0;

        return Math.round((v / 1048576) * 10) / 10;
    }
}

/** Collects LCP, CLS and long tasks (TBT proxy) in the page. */
export async function installVitals(ctx: BrowserContext) {
    await ctx.addInitScript(() => {
        const w = window as any;
        w.__perf = { lcp: 0, cls: 0, tbt: 0, longTasks: 0, inp: 0 };

        try {
            new PerformanceObserver((l) => {
                for (const e of l.getEntries()) {
                    w.__perf.lcp = e.startTime;
                }
            }).observe({ type: 'largest-contentful-paint', buffered: true });
            new PerformanceObserver((l) => {
                for (const e of l.getEntries() as any[]) {
                    if (!e.hadRecentInput) {
                        w.__perf.cls += e.value;
                    }
                }
            }).observe({ type: 'layout-shift', buffered: true });
            new PerformanceObserver((l) => {
                for (const e of l.getEntries()) {
                    w.__perf.longTasks++;
                    w.__perf.tbt += Math.max(0, e.duration - 50);
                }
            }).observe({ type: 'longtask', buffered: true });
            new PerformanceObserver((l) => {
                for (const e of l.getEntries() as any[]) {
                    if (e.interactionId) {
                        w.__perf.inp = Math.max(w.__perf.inp, e.duration);
                    }
                }
            }).observe({
                type: 'event',
                buffered: true,
                durationThreshold: 16,
            } as any);
        } catch {
            /* older engines */
        }
    });
}

export async function readVitals(page: Page) {
    return page.evaluate(
        () =>
            (window as any).__perf as {
                lcp: number;
                cls: number;
                tbt: number;
                longTasks: number;
                inp: number;
            },
    );
}

export async function setLite(ctx: BrowserContext, on: boolean) {
    await ctx.addInitScript(
        (pref) => localStorage.setItem('civio_lite_pref', pref),
        on ? 'on' : 'off',
    );
}

export const kb = (b: number) => Math.round(b / 102.4) / 10;
