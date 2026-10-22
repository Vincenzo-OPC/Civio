import { defineConfig, devices } from '@playwright/test';
import {
    assertThrowawayDb,
    defaultThrowawayDb,
} from './tests/E2E/db-guard.mjs';

/**
 * Strict mock browser E2E. Chromium only, one worker, one throwaway SQLite
 * file in a temp directory. The DB variables are set here, for the app server
 * and the PHP helpers only, so they never reach a Pest run.
 */
const E2E_DB = process.env.E2E_DB || defaultThrowawayDb();
const PORT = 8123;

Object.assign(process.env, {
    E2E_DB,
    DB_CONNECTION: 'sqlite',
    DB_DATABASE: E2E_DB,
    DB_URL: '',
    SESSION_DRIVER: 'database',
    CACHE_STORE: 'database',
    QUEUE_CONNECTION: 'sync',
    BASE_URL: `http://127.0.0.1:${PORT}`,
});
assertThrowawayDb(process.env);

export default defineConfig({
    testDir: './tests/E2E/playwright',
    fullyParallel: false,
    workers: 1,
    forbidOnly: !!process.env.CI,
    retries: 0,
    timeout: 90_000,
    reporter: process.env.CI ? [['list'], ['github']] : 'list',
    use: {
        baseURL: process.env.BASE_URL,
        trace: 'retain-on-failure',
    },
    projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
    webServer: {
        command: `node tests/E2E/setup-db.mjs && php artisan serve --host=127.0.0.1 --port=${PORT}`,
        url: `http://127.0.0.1:${PORT}/up`,
        // Never reuse a server already on the port: it could use another DB.
        reuseExistingServer: false,
        timeout: 180_000,
        env: { ...(process.env as Record<string, string>) },
    },
});
