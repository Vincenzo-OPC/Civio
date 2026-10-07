import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
    CURRENT_KEY_PREFIX,
    LEGACY_KEY_PREFIX,
    migrateKeys,
    migrateLegacyStorageKeys,
} from '../../resources/js/lib/legacy-storage';

function memoryStorage(initial: Record<string, string> = {}) {
    const map = new Map(Object.entries(initial));

    return {
        map,
        getItem: (key: string) => map.get(key) ?? null,
        setItem: (key: string, value: string) => void map.set(key, value),
        removeItem: (key: string) => void map.delete(key),
    };
}

const legacy = (suffix: string) => `${LEGACY_KEY_PREFIX}${suffix}`;
const current = (suffix: string) => `${CURRENT_KEY_PREFIX}${suffix}`;

describe('legacy storage migration', () => {
    it('copies old keys to civio_ keys and removes the old ones', () => {
        const local = memoryStorage({
            [legacy('guest_study_bias_v1')]: '{"weak":["Verbal"]}',
            [legacy('cookie_consent')]: 'true',
        });
        const session = memoryStorage({
            [legacy('exam_origin')]: '/dashboard',
        });

        assert.equal(migrateLegacyStorageKeys({ local, session }), 3);
        assert.equal(
            local.map.get(current('guest_study_bias_v1')),
            '{"weak":["Verbal"]}',
        );
        assert.equal(local.map.get(current('cookie_consent')), 'true');
        assert.equal(session.map.get(current('exam_origin')), '/dashboard');
        assert.ok(
            [...local.map.keys(), ...session.map.keys()].every((k) =>
                k.startsWith(CURRENT_KEY_PREFIX),
            ),
        );
    });

    it('never overwrites a value already saved under the new key', () => {
        const local = memoryStorage({
            [legacy('drills_active_tab')]: 'old',
            [current('drills_active_tab')]: 'new',
        });

        assert.equal(migrateKeys(local, ['drills_active_tab']), 0);
        assert.equal(local.map.get(current('drills_active_tab')), 'new');
        assert.equal(local.map.has(legacy('drills_active_tab')), false);
    });

    it('is idempotent and ignores unknown keys', () => {
        const local = memoryStorage({
            [legacy('cookie_consent')]: 'true',
            [legacy('something_else')]: 'x',
        });

        assert.equal(migrateLegacyStorageKeys({ local }), 1);
        assert.equal(migrateLegacyStorageKeys({ local }), 0);
        assert.equal(local.map.get(legacy('something_else')), 'x');
    });

    it('keeps booting when storage throws', () => {
        const broken = {
            getItem: () => {
                throw new Error('SecurityError');
            },
            setItem: () => undefined,
            removeItem: () => undefined,
        };

        assert.equal(migrateLegacyStorageKeys({ local: broken }), 0);
        assert.equal(migrateLegacyStorageKeys({}), 0);
    });
});
