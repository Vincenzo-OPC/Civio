import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
    createPackStore,
    packKey,
    QUEUE_KEY,
} from '../../resources/js/lib/offline/pack-store';
import type { KeyValueAdapter } from '../../resources/js/lib/offline/pack-store';
import type { StoredPack } from '../../resources/js/lib/offline/types';

function memoryAdapter(): {
    map: Map<string, unknown>;
    adapter: () => Promise<KeyValueAdapter>;
} {
    const map = new Map<string, unknown>();
    const kv: KeyValueAdapter = {
        get: async <T>(key: string) => map.get(key) as T | undefined,
        set: async (key, value) => void map.set(key, value),
        del: async (key) => void map.delete(key),
        keys: async () => [...map.keys()],
    };

    return { map, adapter: async () => kv };
}

function pack(categoryId: number, category: string): StoredPack {
    return {
        categoryId,
        category,
        version: 'v1',
        bytes: 2048,
        downloadedAt: '2026-10-07T00:00:00.000Z',
        items: [],
    };
}

describe('offline pack store', () => {
    it('saves, lists (sorted, packs only), reads and removes packs', async () => {
        const { map, adapter } = memoryAdapter();
        const store = createPackStore(adapter);

        await store.savePack(pack(5, 'Numerical Ability'));
        await store.savePack(pack(2, 'General Information'));
        await store.saveQueue([]);

        assert.deepEqual(
            (await store.listPacks()).map((p) => p.categoryId),
            [2, 5],
        );
        assert.equal((await store.getPack(5))?.category, 'Numerical Ability');
        assert.ok(map.has(packKey(5)));

        await store.removePack(5);
        assert.equal(await store.getPack(5), undefined);
        assert.deepEqual(
            (await store.listPacks()).map((p) => p.categoryId),
            [2],
        );
    });

    it('returns an empty queue when nothing or junk is stored', async () => {
        const { map, adapter } = memoryAdapter();
        const store = createPackStore(adapter);

        assert.deepEqual(await store.loadQueue(), []);
        map.set(QUEUE_KEY, 'junk');
        assert.deepEqual(await store.loadQueue(), []);
    });
});
