export type GuardFailure = 'overload' | 'rate_limit';

export interface GuardHooks {
    onRetrying: (retrying: boolean) => void;
    onFailure: (type: GuardFailure) => void;
}

export interface GuardOptions {
    maxRetries?: number;
    initialDelayMs?: number;
    sleep?: (ms: number) => Promise<void>;
    isOffline?: () => boolean;
}

/** Resolve the effective HTTP method once: init.method wins over Request.method. */
export function requestMethod(
    input: RequestInfo | URL,
    init?: RequestInit,
): string {
    const fromInit = init?.method;
    const fromRequest =
        typeof Request !== 'undefined' && input instanceof Request
            ? input.method
            : undefined;

    return (fromInit ?? fromRequest ?? 'GET').toUpperCase();
}

export function isRetryableStatus(response: Response): boolean {
    return (
        response.status === 429 ||
        response.status === 502 ||
        response.status === 504 ||
        (response.status === 503 && !response.headers.get('x-inertia'))
    );
}

/**
 * Wrap fetch so only idempotent reads (GET/HEAD) are retried with backoff.
 * Writes are never replayed: a failed write's response or error goes straight
 * back to the caller, whose own recovery (e.g. the Strict Mock autosave queue)
 * decides what to do. A write whose response was lost may already be saved.
 */
export function createGuardedFetch(
    originalFetch: typeof fetch,
    hooks: GuardHooks,
    options: GuardOptions = {},
): typeof fetch {
    const maxRetries = options.maxRetries ?? 3;
    const sleep =
        options.sleep ??
        ((ms: number) => new Promise<void>((r) => setTimeout(r, ms)));
    const isOffline =
        options.isOffline ??
        (() => typeof navigator !== 'undefined' && navigator.onLine === false);

    return async (input: RequestInfo | URL, init?: RequestInit) => {
        const method = requestMethod(input, init);
        const canRetry = method === 'GET' || method === 'HEAD';
        // A Request body can only be read once; clone per retry for safe reads.
        const attempt = () =>
            originalFetch(
                typeof Request !== 'undefined' && input instanceof Request
                    ? input.clone()
                    : input,
                init,
            );

        let retries = 0;
        let delay = options.initialDelayMs ?? 1000;

        for (;;) {
            let response: Response;

            try {
                response = await attempt();
            } catch (error) {
                // Offline is not overload, and writes are never resent.
                if (!canRetry || isOffline()) {
                    if (retries > 0) {
                        hooks.onRetrying(false);
                    }

                    throw error;
                }

                if (retries < maxRetries) {
                    retries++;
                    hooks.onRetrying(true);
                    await sleep(delay);
                    delay *= 2;
                    continue;
                }

                hooks.onRetrying(false);
                hooks.onFailure('overload');

                throw error;
            }

            if (!isRetryableStatus(response)) {
                if (retries > 0) {
                    hooks.onRetrying(false);
                }

                return response;
            }

            if (canRetry && retries < maxRetries) {
                retries++;
                hooks.onRetrying(true);
                await sleep(delay);
                delay *= 2;
                continue;
            }

            // Out of retries, or a write: surface feedback, hand back the
            // real failing response so the caller never mistakes it for success.
            if (retries > 0) {
                hooks.onRetrying(false);
            }

            hooks.onFailure(
                response.status === 429 ? 'rate_limit' : 'overload',
            );

            return response;
        }
    };
}
