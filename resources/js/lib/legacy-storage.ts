/**
 * One-time browser storage migration for returning users.
 *
 * Builds before the Civio rename stored progress under a different key prefix.
 * On boot we copy each old key to its `civio_` name (only when the new key is
 * still empty) and delete the old one, so study bias, cookie consent, the drills
 * tab and in-tab navigation state survive the rename. Safe to call repeatedly.
 */

/** The only place the pre-rename key prefix is spelled out. */
export const LEGACY_KEY_PREFIX = 'hiraya_';
export const CURRENT_KEY_PREFIX = 'civio_';

/** Key suffixes (after the prefix) kept in localStorage. */
export const LEGACY_LOCAL_KEYS = [
    'guest_study_bias_v1',
    'cookie_consent',
    'drills_active_tab',
] as const;

/** Key suffixes (after the prefix) kept in sessionStorage. */
export const LEGACY_SESSION_KEYS = [
    'previous_location',
    'back_anchor',
    'exam_origin',
] as const;

type KeyValueStorage = Pick<Storage, 'getItem' | 'setItem' | 'removeItem'>;

export interface StorageTargets {
    readonly local?: KeyValueStorage | null;
    readonly session?: KeyValueStorage | null;
}

/** Moves the given legacy keys in one storage. Returns how many were moved. */
export function migrateKeys(
    storage: KeyValueStorage,
    suffixes: readonly string[],
): number {
    let moved = 0;

    for (const suffix of suffixes) {
        const from = `${LEGACY_KEY_PREFIX}${suffix}`;
        const to = `${CURRENT_KEY_PREFIX}${suffix}`;
        const legacy = storage.getItem(from);

        if (legacy === null) {
            continue;
        }

        if (storage.getItem(to) === null) {
            storage.setItem(to, legacy);
            moved++;
        }

        storage.removeItem(from);
    }

    return moved;
}

function browserStorage(kind: 'local' | 'session'): KeyValueStorage | null {
    if (typeof window === 'undefined') {
        return null;
    }

    try {
        return kind === 'local' ? window.localStorage : window.sessionStorage;
    } catch {
        return null; // storage disabled (privacy mode, blocked cookies)
    }
}

/** Migrates every known legacy key. Never throws. */
export function migrateLegacyStorageKeys(
    targets: StorageTargets = {
        local: browserStorage('local'),
        session: browserStorage('session'),
    },
): number {
    let moved = 0;

    try {
        if (targets.local) {
            moved += migrateKeys(targets.local, LEGACY_LOCAL_KEYS);
        }

        if (targets.session) {
            moved += migrateKeys(targets.session, LEGACY_SESSION_KEYS);
        }
    } catch {
        // quota exceeded or storage revoked mid-way: keep booting
    }

    return moved;
}
