import { ChevronLeft, Flag, LayoutGrid, Moon, Timer } from 'lucide-react';

const CHOICES: { letter: string; text: string; selected?: boolean }[] = [
    { letter: 'A', text: '₱150' },
    { letter: 'B', text: '₱300', selected: true },
    { letter: 'C', text: '₱350' },
    { letter: 'D', text: '₱1,700' },
];

/**
 * Static picture of the Study Mock. Same header, progress, and choice rows
 * as the exam. Nothing here is scored and nothing is clickable.
 */
export function ExamScreenPreview() {
    return (
        <figure className="civio-session overflow-hidden border border-[var(--civio-line)] bg-[var(--civio-paper)] text-[var(--civio-ink)]">
            <div className="flex items-center gap-0.5 border-b border-[var(--civio-line)] px-1 py-1 sm:px-2">
                <span className="flex size-9 shrink-0 items-center justify-center">
                    <ChevronLeft className="size-5" />
                </span>
                <span className="min-w-0 flex-1" />
                <span className="inline-flex shrink-0 items-center gap-1.5 text-xs font-semibold tabular-nums">
                    <svg viewBox="0 0 36 36" className="size-5" aria-hidden>
                        <circle
                            cx="18"
                            cy="18"
                            r="12"
                            fill="none"
                            stroke="currentColor"
                            strokeOpacity="0.18"
                            strokeWidth="5"
                        />
                        <circle
                            cx="18"
                            cy="18"
                            r="12"
                            fill="none"
                            stroke="var(--civio-violet)"
                            strokeWidth="5"
                            strokeDasharray="70 76"
                            transform="rotate(-90 18 18)"
                        />
                    </svg>
                    <span className="text-[var(--civio-ink)]/70">3:10:00</span>
                    <span className="text-[var(--civio-line)]">·</span>
                    <span className="inline-flex items-center gap-1 text-[var(--civio-ink)]/70">
                        <Timer className="size-3.5 opacity-70" />
                        0:12
                    </span>
                </span>
                <span className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-ink)]/60">
                    <Moon className="size-4" />
                </span>
                <span className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-ink)]/60">
                    <Flag className="size-4" />
                </span>
                <span className="flex size-9 shrink-0 items-center justify-center text-[var(--civio-violet)]">
                    <LayoutGrid className="size-4" />
                </span>
            </div>

            <div className="flex items-center justify-between gap-3 px-3 py-2 text-xs sm:px-5">
                <p className="min-w-0">
                    <span className="text-sm font-semibold">Study Mock</span>
                    <span className="mx-1.5 opacity-40">·</span>
                    <span className="font-semibold">1 of 150</span>
                    <span className="mt-0.5 block opacity-60">
                        Professional
                    </span>
                </p>
                <p className="shrink-0 font-semibold">
                    <span className="opacity-70">Tools</span>
                    <span className="ml-3">Pause</span>
                </p>
            </div>

            <div className="h-1 bg-[var(--civio-line)]" aria-hidden>
                <div
                    className="h-full bg-[var(--civio-violet)]"
                    style={{ width: `${(1 / 150) * 100}%` }}
                />
            </div>

            <div className="px-4 py-5 sm:px-6 sm:py-6">
                <p className="text-lg leading-relaxed md:text-xl">
                    15% of ₱2,000 is:
                </p>
                <p className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs font-semibold">
                    <span className="opacity-60">Report</span>
                    <span className="rounded-lg bg-[var(--civio-violet)] px-2.5 py-1.5 text-[11px] font-bold text-white">
                        Reveal Answer
                    </span>
                    <span className="opacity-70">Copy for AI</span>
                </p>
                <div className="mt-4 flex flex-col" role="list">
                    {CHOICES.map((choice) => (
                        <div
                            key={choice.letter}
                            role="listitem"
                            className={`flex min-h-12 items-start gap-3 border-x-0 border-t-0 border-b px-1 py-3.5 ${
                                choice.selected
                                    ? 'border-[var(--civio-violet)] bg-[var(--civio-violet)]/10'
                                    : 'border-[var(--civio-line)]'
                            }`}
                        >
                            <span
                                className={`flex size-7 shrink-0 items-center justify-center border text-xs font-bold ${
                                    choice.selected
                                        ? 'border-[var(--civio-violet)] bg-[var(--civio-violet)] text-white'
                                        : 'border-[var(--civio-line)]'
                                }`}
                            >
                                {choice.letter}
                            </span>
                            <span className="text-sm leading-relaxed md:text-base">
                                {choice.text}
                                {choice.selected && (
                                    <span className="mt-1 block text-xs font-semibold">
                                        Selected
                                    </span>
                                )}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
            <figcaption className="sr-only">
                The Study Mock screen. Item 1 of 150. Choice B is selected. This
                picture is not a scored item.
            </figcaption>
        </figure>
    );
}
