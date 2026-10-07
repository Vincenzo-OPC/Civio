import type Echo from 'laravel-echo';

/** Pusher/Reverb settings shared by the server as the `pusher` Inertia prop. */
export interface RealtimeConfig {
    key?: string | null;
    cluster?: string | null;
    host?: string | null;
    port?: number | null;
    scheme?: string | null;
}

export type RealtimeEcho = Echo<'pusher'>;

/**
 * Open a realtime (Echo + Pusher) connection on demand.
 *
 * laravel-echo and pusher-js (~70 KB raw) are loaded with a dynamic import the
 * first time a screen actually subscribes, so they never sit in the first-load
 * bundle. Returns a synchronous cleanup suitable for a React effect.
 */
export function connectRealtime(
    config: RealtimeConfig | null | undefined,
    setup: (echo: RealtimeEcho) => void | (() => void),
): () => void {
    if (!config?.key || typeof window === 'undefined') {
        return () => {};
    }

    let cancelled = false;
    let echo: RealtimeEcho | null = null;
    let teardown: void | (() => void);

    void Promise.all([import('laravel-echo'), import('pusher-js')])
        .then(([{ default: EchoClass }, { default: Pusher }]) => {
            if (cancelled) {
                return;
            }

            (window as unknown as { Pusher: unknown }).Pusher = Pusher;
            echo = new EchoClass({
                broadcaster: 'pusher',
                key: config.key as string,
                cluster: config.cluster ?? 'ap1',
                wsHost: config.host
                    ? config.host
                    : `ws-${config.cluster}.pusher.com`,
                wsPort: config.port ?? 80,
                wssPort: config.port ?? 443,
                forceTLS: (config.scheme ?? 'https') === 'https',
                enabledTransports: ['ws', 'wss'],
            });
            teardown = setup(echo);
        })
        .catch(() => {
            /* realtime is best-effort; pages still work without it */
        });

    return () => {
        cancelled = true;

        if (typeof teardown === 'function') {
            teardown();
        }

        echo?.disconnect();
    };
}
