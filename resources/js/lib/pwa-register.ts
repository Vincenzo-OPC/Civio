/**
 * Registers the Civio service worker (vite-plugin-pwa, prompt-to-update).
 * Called at boot, and again when a Lite user downloads an offline pack
 * (Lite skips the service worker until the user opts into offline use).
 */
let registered = false;

export function registerServiceWorker(): void {
    if (typeof window === 'undefined' || registered) {
        return;
    }

    registered = true;
    void removeLegacyRegistrations();

    void import('virtual:pwa-register')
        .then(({ registerSW }) => {
            registerSW({
                immediate: true,
                onNeedRefresh() {
                    // Prompt-style update: ask once, then reload into new SW.
                    if (
                        window.confirm(
                            'A new Civio version is available. Reload to update?',
                        )
                    ) {
                        window.location.reload();
                    }
                },
            });
        })
        .catch(() => {
            /* SW unavailable in some local/dev contexts */
        });
}

/**
 * Earlier builds registered /build/sw.js with scope /build/, which controlled
 * no page. Drop those registrations; the worker now lives at /sw.js.
 */
async function removeLegacyRegistrations(): Promise<void> {
    try {
        const registrations =
            (await navigator.serviceWorker?.getRegistrations()) ?? [];

        await Promise.all(
            registrations
                .filter((registration) =>
                    new URL(registration.scope).pathname.startsWith('/build/'),
                )
                .map((registration) => registration.unregister()),
        );
    } catch {
        /* not supported here */
    }
}
