import { router } from '@inertiajs/react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { useEffect, useState } from 'react';
import { createGuardedFetch } from '@/lib/guarded-fetch';

export function TrafficOverloadGuard() {
    const [isOpen, setIsOpen] = useState(false);
    const [isRetrying, setIsRetrying] = useState(false);
    const [errorType, setErrorType] = useState<'overload' | 'rate_limit'>(
        'overload',
    );

    useEffect(() => {
        // 1. Intercept Inertia requests exception states
        const unregisterHttpException = router.on('httpException', (event) => {
            const status = event.detail.response.status;
            const isInertiaResponse =
                event.detail.response.headers &&
                event.detail.response.headers['x-inertia'];

            if (status === 429) {
                setErrorType('rate_limit');
                setIsOpen(true);
            } else if (
                status === 504 ||
                status === 502 ||
                (status === 503 && !isInertiaResponse)
            ) {
                setErrorType('overload');
                setIsOpen(true);
            }
        });

        // 2. Guard global fetch: only GET/HEAD are retried; writes go
        // straight back to their caller's recovery logic.
        const originalFetch = window.fetch;
        window.fetch = createGuardedFetch(originalFetch.bind(window), {
            onRetrying: setIsRetrying,
            onFailure: (type) => {
                setErrorType(type);
                setIsOpen(true);
            },
        });

        return () => {
            unregisterHttpException();
            window.fetch = originalFetch;
        };
    }, []);

    if (!isOpen && !isRetrying) {
        return null;
    }

    return (
        <>
            {/* Background Retrying Toast Notification */}
            {isRetrying && !isOpen && (
                <div className="dark:bg-amber-950/30/90 fixed right-4 bottom-4 z-[9999] flex animate-bounce items-center gap-3 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 shadow-lg backdrop-blur transition-all dark:border-amber-900/50 dark:bg-amber-950/95">
                    <RefreshCw className="size-4 animate-spin text-amber-600 dark:text-amber-400" />
                    <div className="flex flex-col">
                        <span className="text-xs font-semibold text-amber-900 dark:text-amber-300">
                            Connection unstable
                        </span>
                        <span className="dark:text-amber-405 mt-0.5 text-[10px] leading-none text-amber-700">
                            Retrying request in background...
                        </span>
                    </div>
                </div>
            )}

            {/* Final Overload Warning Modal (shown only after all retries fail) */}
            {isOpen && (
                <div className="animate-fade-in fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/60 p-4 backdrop-blur-sm">
                    <div className="relative w-full max-w-2xl animate-in overflow-hidden rounded-3xl border border-slate-200/80 bg-white p-4 shadow-2xl transition-all duration-200 zoom-in-95 fade-in sm:p-6 dark:border-slate-800 dark:bg-slate-900">
                        {/* Decorative Background */}
                        <div className="pointer-events-none absolute -top-24 -right-24 h-48 w-48 rounded-full bg-amber-500/5 blur-3xl" />

                        <div className="flex flex-col items-center p-2 text-center">
                            <div className="mb-5 flex size-16 animate-bounce items-center justify-center rounded-2xl border border-amber-200 bg-amber-50 text-amber-600 dark:border-amber-900/40 dark:border-amber-900/50 dark:bg-amber-950/30 dark:bg-amber-950/40 dark:text-amber-400">
                                <AlertCircle className="size-8" />
                            </div>

                            <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                                {errorType === 'rate_limit'
                                    ? 'Too Many Requests'
                                    : 'Server Under Heavy Load'}
                            </h3>

                            <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
                                {errorType === 'rate_limit'
                                    ? 'You have made too many requests in a short period. Our security rate-limiter is currently pacing your access.'
                                    : 'Our servers are currently experiencing extremely high traffic from civil service review students.'}
                            </p>

                            <p className="mt-2 border-t border-slate-100 pt-3 text-base leading-relaxed text-slate-500 dark:border-slate-800 dark:text-slate-400">
                                To protect database stability and ensure active
                                study tools work correctly, access is
                                temporarily queued. Please wait a few moments
                                and try your action again!
                            </p>

                            <div className="mt-6 flex w-full gap-3">
                                <button
                                    onClick={() => setIsOpen(false)}
                                    className="flex-1 cursor-pointer rounded-xl bg-slate-100 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
                                >
                                    Dismiss
                                </button>
                                <button
                                    onClick={() => {
                                        setIsOpen(false);
                                        window.location.reload();
                                    }}
                                    className="flex-1 cursor-pointer rounded-xl bg-[#5B35F5] py-3 text-sm font-semibold text-white transition hover:bg-[#4a2ad4]"
                                >
                                    Reload Page
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
