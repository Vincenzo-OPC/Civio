/**
 * Offline page store. idb-keyval is imported statically here so the service
 * worker precaches it with this page; the page has to open with no network.
 */
import * as idb from 'idb-keyval';
import { adapterFromIdb, createPackStore } from '@/lib/offline/pack-store';

const adapter = adapterFromIdb(idb);

export const offlineStore = createPackStore(() => Promise.resolve(adapter));
