/**
 * Lite L2: downloaded packs and the sync queue in IndexedDB (idb-keyval).
 * The adapter is injectable so tests run without IndexedDB. The drills hub
 * loads idb-keyval lazily; the offline page imports it statically so the
 * service worker precaches it with the page (it must work with no network).
 */
import type * as IdbKeyval from 'idb-keyval';
import type { QueuedAnswer, StoredPack } from './types';

export interface KeyValueAdapter {
    get: <T>(key: string) => Promise<T | undefined>;
    set: (key: string, value: unknown) => Promise<void>;
    del: (key: string) => Promise<void>;
    keys: () => Promise<string[]>;
}

export const PACK_PREFIX = 'pack:';
export const QUEUE_KEY = 'queue';
export const DB_NAME = 'civio-offline';
export const STORE_NAME = 'kv';

export function packKey(categoryId: number): string {
    return `${PACK_PREFIX}${categoryId}`;
}

type IdbModule = typeof IdbKeyval;

/** Wrap an idb-keyval module in the adapter shape, with Civio's own database. */
export function adapterFromIdb(idb: IdbModule): KeyValueAdapter {
    const store = idb.createStore(DB_NAME, STORE_NAME);

    return {
        get: <T>(key: string) => idb.get<T>(key, store),
        set: (key: string, value: unknown) => idb.set(key, value, store),
        del: (key: string) => idb.del(key, store),
        keys: async () => (await idb.keys(store)).map((key) => String(key)),
    };
}

let defaultAdapter: Promise<KeyValueAdapter> | null = null;

/** idb-keyval imported on first use (the drills hub panel). */
export function idbAdapter(): Promise<KeyValueAdapter> {
    defaultAdapter ??= import('idb-keyval').then(adapterFromIdb);

    return defaultAdapter;
}

export interface PackStore {
    listPacks: () => Promise<StoredPack[]>;
    getPack: (categoryId: number) => Promise<StoredPack | undefined>;
    savePack: (pack: StoredPack) => Promise<void>;
    removePack: (categoryId: number) => Promise<void>;
    loadQueue: () => Promise<QueuedAnswer[]>;
    saveQueue: (queue: QueuedAnswer[]) => Promise<void>;
}

export function createPackStore(
    adapter: () => Promise<KeyValueAdapter> = idbAdapter,
): PackStore {
    return {
        async listPacks() {
            const kv = await adapter();
            const packKeys = (await kv.keys()).filter((key) =>
                key.startsWith(PACK_PREFIX),
            );
            const packs = await Promise.all(
                packKeys.map((key) => kv.get<StoredPack>(key)),
            );

            return packs
                .filter((pack): pack is StoredPack => pack !== undefined)
                .sort((a, b) => a.category.localeCompare(b.category));
        },
        async getPack(categoryId) {
            return (await adapter()).get<StoredPack>(packKey(categoryId));
        },
        async savePack(pack) {
            await (await adapter()).set(packKey(pack.categoryId), pack);
        },
        async removePack(categoryId) {
            await (await adapter()).del(packKey(categoryId));
        },
        async loadQueue() {
            const queue = await (
                await adapter()
            ).get<QueuedAnswer[]>(QUEUE_KEY);

            return Array.isArray(queue) ? queue : [];
        },
        async saveQueue(queue) {
            await (await adapter()).set(QUEUE_KEY, queue);
        },
    };
}
