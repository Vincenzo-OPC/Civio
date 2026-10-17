/**
 * One-time browser storage migration for returning users.
 *
 * Older builds stored a few keys under a retired prefix. On boot we copy each
 * known suffix to its `civio_` name when that name is still empty, then delete
 * the old key. Safe to call repeatedly.
 */

export const CURRENT_KEY_PREFIX = 'civio_';

/** Key suffixes kept in localStorage. */
export const LEGACY_LOCAL_KEYS = [
    'guest_study_bias_v1',
    'cookie_consent',
    'drills_active_tab',
] as const;

/** Key suffixes kept in sessionStorage. */
export const LEGACY_SESSION_KEYS = [
    'previous_location',
    'back_anchor',
    'exam_origin',
] as const;

type KeyValueStorage = Pick<Storage, 'getItem' | 'setItem' | 'removeItem'> & {
    readonly length?: number;
    key?: (index: number) => string | null;
};

export interface StorageTargets {
    readonly local?: KeyValueStorage | null;
    readonly session?: KeyValueStorage | null;
}

/** Moves a non-civio key that ends in a known suffix. Returns how many were moved. */
export function migrateKeys(
    storage: KeyValueStorage,
    suffixes: readonly string[],
): number {
    if (
        typeof storage.key !== 'function' ||
        typeof storage.length !== 'number'
    ) {
        return 0;
    }

    const found: string[] = [];

    for (let index = 0; index < storage.length; index++) {
        const name = storage.key(index);

        if (
            name &&
            !name.startsWith(CURRENT_KEY_PREFIX) &&
            suffixes.some((suffix) => name.endsWith(suffix))
        ) {
            found.push(name);
        }
    }

    let moved = 0;

    for (const from of found) {
        const suffix = suffixes.find((item) => from.endsWith(item));

        if (!suffix) {
            continue;
        }

        const to = `${CURRENT_KEY_PREFIX}${suffix}`;
        const previous = storage.getItem(from);

        if (previous === null) {
            continue;
        }

        if (storage.getItem(to) === null) {
            storage.setItem(to, previous);
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
