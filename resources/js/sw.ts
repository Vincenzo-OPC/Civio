/// <reference lib="webworker" />
import { clientsClaim } from 'workbox-core';
import { cleanupOutdatedCaches, precacheAndRoute } from 'workbox-precaching';
import { NavigationRoute, registerRoute } from 'workbox-routing';
import { NetworkFirst, NetworkOnly } from 'workbox-strategies';

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
