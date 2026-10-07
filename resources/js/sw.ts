/// <reference lib="webworker" />
import { clientsClaim } from 'workbox-core';
import { ExpirationPlugin } from 'workbox-expiration';
import { cleanupOutdatedCaches, precacheAndRoute } from 'workbox-precaching';
import { NavigationRoute, registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, NetworkOnly } from 'workbox-strategies';

declare let self: ServiceWorkerGlobalScope;

// Versioned precache from vite-plugin-pwa injectManifest
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();
self.skipWaiting();
clientsClaim();

/** Never cache exam/drill answer payloads or mutating API. */
const NETWORK_ONLY_PREFIXES = [
    '/exams',
    '/drills',
    '/api',
    '/sanctum',
    '/livewire',
    '/broadcasting',
    '/admin',
    '/login',
    '/register',
    '/logout',
    '/auth',
    '/dashboard',
    '/settings',
    '/analytics',
    '/history',
    '/study-schedules',
    '/study-suggestions',
];

function isSensitive(url: URL): boolean {
    return NETWORK_ONLY_PREFIXES.some(
        (p) => url.pathname === p || url.pathname.startsWith(`${p}/`),
    );
}

registerRoute(({ url, request }) => {
    if (request.method !== 'GET') {
        return true;
    }

    return isSensitive(url);
}, new NetworkOnly());

// Lite L2: the offline drill page. Network-first, with its own cache so it is
// never evicted with other pages; the drills hub refreshes it after a pack
// download. Pack JSON (/offline/packs) and sync (/offline/attempts) are not
// cached here: packs live in IndexedDB and POSTs are NetworkOnly above.
registerRoute(
    ({ url, request }) =>
        request.method === 'GET' &&
        url.origin === self.location.origin &&
        url.pathname === '/offline' &&
        request.mode === 'navigate',
    new NetworkFirst({
        cacheName: 'civio-offline-shell',
        networkTimeoutSeconds: 4,
    }),
);

// HTML navigations: network-first (never serve stale exam shells forever)
registerRoute(
    new NavigationRoute(
        new NetworkFirst({
            cacheName: 'civio-pages',
            networkTimeoutSeconds: 5,
        }),
        {
            denylist: NETWORK_ONLY_PREFIXES.map(
                (p) => new RegExp(`^${p.replace(/\//g, '\\/')}`),
            ),
        },
    ),
);

// Lite L0: only the app shell is precached. Other hashed build chunks (admin,
// charts, PDF export, rarely used pages) are cached the first time they load.
// Filenames are content-hashed, so a cached copy is never stale.
registerRoute(
    ({ url, request }) =>
        request.method === 'GET' &&
        url.origin === self.location.origin &&
        url.pathname.startsWith('/build/assets/'),
    new CacheFirst({
        cacheName: 'civio-assets',
        plugins: [
            new ExpirationPlugin({
                maxEntries: 150,
                maxAgeSeconds: 30 * 24 * 60 * 60,
                purgeOnQuotaError: true,
            }),
        ],
    }),
);
