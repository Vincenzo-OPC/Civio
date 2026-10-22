// Refuses to run the browser E2E against anything but a throwaway SQLite file.
// Used by the Playwright config, the DB setup script and every PHP helper call.
import os from 'node:os';
import path from 'node:path';

/** Ports that belong to real databases and apps on GT's machines. */
const PROTECTED_PORTS = ['5432', '5433', '5434', '8080'];
const NAME = /^civio-e2e[\w.-]*\.sqlite$/;

/** The default throwaway path: a fixed name in the OS temp directory. */
export function defaultThrowawayDb(env = process.env) {
    return path.join(env.RUNNER_TEMP || os.tmpdir(), 'civio-e2e.sqlite');
}

/**
 * Throws unless `env` points Laravel at the throwaway SQLite file named by
 * E2E_DB. Returns the resolved path.
 */
export function assertThrowawayDb(env = process.env, tmpRoots = null) {
    const fail = (why) => {
        throw new Error(
            `E2E aborted: ${why}. The browser tests only run against a throwaway SQLite file (see tests/E2E/README.md).`,
        );
    };
    const roots = (tmpRoots ?? [os.tmpdir(), env.RUNNER_TEMP])
        .filter(Boolean)
        .map((r) => path.resolve(r));

    if (env.DB_CONNECTION !== 'sqlite') {
        fail(`DB_CONNECTION is "${env.DB_CONNECTION ?? ''}", not "sqlite"`);
    }

    if (!env.E2E_DB || !path.isAbsolute(env.E2E_DB)) {
        fail('E2E_DB must be an absolute path to the throwaway file');
    }

    if (env.DB_DATABASE !== env.E2E_DB) {
        fail('DB_DATABASE is not the throwaway path in E2E_DB');
    }

    const db = path.resolve(env.DB_DATABASE);

    if (!NAME.test(path.basename(db))) {
        fail('the throwaway file must be named civio-e2e*.sqlite');
    }

    if (!roots.some((r) => db.startsWith(r + path.sep))) {
        fail(
            `the throwaway file must be inside a temp directory (${roots.join(', ')})`,
        );
    }

    if (env.DB_URL) {
        fail('DB_URL is set; it would override the SQLite file');
    }

    for (const key of ['DB_PORT', 'BASE_URL', 'APP_URL']) {
        const value = String(env[key] ?? '');

        for (const port of PROTECTED_PORTS) {
            if (value === port || value.includes(`:${port}`)) {
                fail(`${key} points at protected port ${port}`);
            }
        }
    }

    return db;
}
