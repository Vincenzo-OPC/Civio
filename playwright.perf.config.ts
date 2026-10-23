import os from 'node:os';
import path from 'node:path';
import { defineConfig, devices } from '@playwright/test';
import { assertThrowawayDb } from './tests/E2E/db-guard.mjs';

/**
 * Low-end performance runs (Issue #27). Same throwaway-SQLite guard as the
 * Strict Mock E2E, a separate file and port. A gzip proxy (Node built-ins)
 * sits in front of `php artisan serve` so byte counts match a compressing
 * production server. `budget.spec.ts` is the deterministic CI gate (bytes and
 * request counts only); `measure.spec.ts` records timings and runs only with
 * PERF_MEASURE=1.
 */
const E2E_DB =
    process.env.PERF_DB ||
    path.join(process.env.RUNNER_TEMP || os.tmpdir(), 'civio-e2e-perf.sqlite');
const APP_PORT = 8144;
const PROXY_PORT = 8145;
// PERF_REUSE=1 reuses a server already started with tests/Perf/serve.mjs (local only).

Object.assign(process.env, {
    E2E_DB,
    DB_CONNECTION: 'sqlite',
    DB_DATABASE: E2E_DB,
    DB_URL: '',
    SESSION_DRIVER: 'database',
    CACHE_STORE: 'database',
    QUEUE_CONNECTION: 'sync',
    APP_ENV: 'testing',
    APP_DEBUG: 'false',
    PERF_APP_PORT: String(APP_PORT),
    PERF_PROXY_PORT: String(PROXY_PORT),
    PERF_CACHE_RULES: '1',
    BASE_URL: `http://127.0.0.1:${PROXY_PORT}`,
});
assertThrowawayDb(process.env);

export default defineConfig({
    testDir: './tests/Perf',
    testMatch: /.*\.spec\.ts/,
    fullyParallel: false,
    workers: 1,
    forbidOnly: !!process.env.CI,
    retries: 0,
    timeout: 600_000,
    reporter: process.env.CI ? [['list'], ['github']] : 'list',
    use: { baseURL: process.env.BASE_URL },
    projects: [
        {
            name: 'chromium-mobile',
            use: {
                ...devices['Desktop Chrome'],
                viewport: { width: 360, height: 740 },
                isMobile: false,
                hasTouch: true,
            },
        },
    ],
    webServer: {
        command: `node tests/Perf/setup-perf-db.mjs && node tests/Perf/serve.mjs`,
        url: `http://127.0.0.1:${PROXY_PORT}/up`,
        reuseExistingServer: !!process.env.PERF_REUSE,
        timeout: 240_000,
        env: { ...(process.env as Record<string, string>) },
    },
});
