type Listenable = Pick<EventTarget, 'addEventListener' | 'removeEventListener'>;

/**
 * Wire page-exit flushes and return a function that removes every listener.
 * The visibilitychange handler must be removable too: a leftover handler keeps
 * an old save closure alive and can re-save a submitted exam as "resumable".
 */
export function bindFlushListeners(
    win: Listenable,
    doc: Listenable & { visibilityState?: string },
    flush: () => void,
): () => void {
    const onHidden = () => {
        if (doc.visibilityState === 'hidden') {
            flush();
        }
    };

    win.addEventListener('pagehide', flush);
    win.addEventListener('beforeunload', flush);
    doc.addEventListener('visibilitychange', onHidden);

    return () => {
        win.removeEventListener('pagehide', flush);
        win.removeEventListener('beforeunload', flush);
        doc.removeEventListener('visibilitychange', onHidden);
    };
}
