/**
 * Lite L2: keep the offline drill page available with no network.
 * Matches the `civio-offline-shell` route in resources/js/sw.ts.
 */
export const OFFLINE_PAGE_URL = '/offline';
export const OFFLINE_SHELL_CACHE = 'civio-offline-shell';

/** Store a fresh copy of the /offline HTML. Safe to call often. */
export async function warmOfflineShell(): Promise<void> {
    if (typeof caches === 'undefined') {
        return;
    }

    try {
        const cache = await caches.open(OFFLINE_SHELL_CACHE);
        await cache.add(
            new Request(OFFLINE_PAGE_URL, {
                credentials: 'same-origin',
                headers: { Accept: 'text/html' },
            }),
        );
    } catch {
        /* offline or storage full: the next visit tries again */
    }
}
