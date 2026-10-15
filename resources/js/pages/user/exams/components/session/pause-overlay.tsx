interface PauseOverlayProps {
    strict: boolean;
    onResume: () => void;
}

export function PauseOverlay({ strict, onResume }: PauseOverlayProps) {
    return (
        <div
            className="absolute inset-0 z-40 flex items-center justify-center bg-[var(--civio-paper)] p-6"
            role="dialog"
            aria-modal="true"
            aria-labelledby="civio-pause-title"
        >
            <div className="w-[min(28rem,100%)] text-center">
                <h2
                    id="civio-pause-title"
                    className="font-heading text-2xl font-semibold text-[var(--civio-ink)]"
                >
                    The clock is stopped
                </h2>
                <p className="mt-3 text-sm leading-relaxed text-[var(--civio-ink)]/80">
                    {strict
                        ? 'This Exam Mode was restored with the clock stopped. Continue when you are ready. You cannot pause during the exam.'
                        : 'Pause freezes the session clock and the time on this item. It is a study convenience, not an uninterrupted official exam.'}
                </p>
                <button
                    type="button"
                    onClick={onResume}
                    className="mt-6 bg-[var(--civio-violet)] px-5 py-2.5 text-sm font-semibold text-white"
                >
                    {strict ? 'Continue' : 'Resume'}
                </button>
            </div>
        </div>
    );
}
