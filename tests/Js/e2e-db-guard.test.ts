import assert from 'node:assert/strict';
import path from 'node:path';
import { test } from 'node:test';
import { assertThrowawayDb } from '../E2E/db-guard.mjs';

const tmp = path.resolve('/tmp/guard-root');
const db = path.join(tmp, 'civio-e2e.sqlite');
const ok = { DB_CONNECTION: 'sqlite', DB_DATABASE: db, E2E_DB: db };
const check = (env: Record<string, string | undefined>) =>
    assertThrowawayDb(env, [tmp]);

test('the throwaway SQLite file in a temp directory is accepted', () => {
    assert.equal(check(ok), db);
});

test('E2E aborts for any connection but sqlite (Postgres, MySQL, unset)', () => {
    for (const DB_CONNECTION of ['pgsql', 'mysql', undefined]) {
        assert.throws(() => check({ ...ok, DB_CONNECTION }), /E2E aborted/);
    }
});

test('E2E aborts unless DB_DATABASE is exactly the throwaway path', () => {
    assert.throws(
        () => check({ ...ok, DB_DATABASE: 'civio' }),
        /throwaway path/,
    );
    assert.throws(() => check({ ...ok, E2E_DB: undefined }), /E2E_DB/);
    const repoDb = path.resolve('database/database.sqlite');
    assert.throws(
        () => check({ ...ok, DB_DATABASE: repoDb, E2E_DB: repoDb }),
        /civio-e2e/,
    );
    const outside = '/var/lib/civio-e2e.sqlite';
    assert.throws(
        () => check({ ...ok, DB_DATABASE: outside, E2E_DB: outside }),
        /temp directory/,
    );
});

test('E2E aborts when DB_URL or a protected port could point elsewhere', () => {
    assert.throws(
        () => check({ ...ok, DB_URL: 'pgsql://x@127.0.0.1:5433/civio' }),
        /DB_URL/,
    );

    for (const env of [
        { DB_PORT: '5433' },
        { DB_PORT: '5434' },
        { BASE_URL: 'http://127.0.0.1:8080' },
        { APP_URL: 'http://localhost:8080' },
    ]) {
        assert.throws(() => check({ ...ok, ...env }), /protected port/);
    }
});
