import { CalendarDays, Flag } from 'lucide-react';
import { useEffect, useState } from 'react';
import {
    examCountdown,
    formatPhDate,
    milestoneText,
    nextMilestone,
    readTrack,
    TRACK_LABEL,
    TRACK_STORAGE_KEY,
} from '@/lib/exam-countdown';
import type {
    ExamMilestone,
    ExamSitting,
    ExamTrack,
} from '@/lib/exam-countdown';

interface ExamCountdownProps {
    sittings: ExamSitting[];
    milestones?: ExamMilestone[];
    sourceUrl?: string | null;
    source?: 'csc' | 'admin' | null;
    /** Test hook: a fixed clock. The live dashboard leaves it unset. */
    initialNow?: number;
}

const TRACKS: ExamTrack[] = ['professional', 'subprofessional'];

function pad(n: number): string {
    return String(n).padStart(2, '0');
}

/**
 * Live countdown to 00:00 Philippine time on the next confirmed CSC exam day.
 * Ticks every second; the target never depends on the browser's timezone.
 */
export function ExamCountdown({
    sittings,
    milestones = [],
    sourceUrl,
    source = 'csc',
    initialNow,
}: ExamCountdownProps) {
    const [now, setNow] = useState(() => initialNow ?? Date.now());
    const [track, setTrack] = useState<ExamTrack>(() => {
        try {
            return readTrack(
                typeof window === 'undefined'
                    ? null
                    : localStorage.getItem(TRACK_STORAGE_KEY),
            );
        } catch {
            return 'professional'; // Storage blocked.
        }
    });

    useEffect(() => {
        const id = window.setInterval(() => setNow(Date.now()), 1000);

        return () => window.clearInterval(id);
    }, []);

    const chooseTrack = (next: ExamTrack) => {
        setTrack(next);

        try {
            localStorage.setItem(TRACK_STORAGE_KEY, next);
        } catch {
            // Ignore: the choice still applies for this visit.
        }
    };

    const state = examCountdown(sittings, now);
    const milestone = nextMilestone(milestones, now);

    const units =
        state.phase === 'counting'
            ? [
                  ['Days', state.parts.days],
                  ['Hours', state.parts.hours],
                  ['Mins', state.parts.minutes],
                  ['Secs', state.parts.seconds],
              ]
            : [];

    return (
        <section
            data-testid="exam-countdown"
            aria-label="Exam countdown"
            className="rounded-2xl border border-[#5B35F5]/20 bg-gradient-to-br from-[#5B35F5]/[0.06] via-white to-[#B3F52D]/[0.12] p-4 sm:p-6 dark:border-[#B3F52D]/20 dark:from-[#5B35F5]/20 dark:via-slate-950 dark:to-[#B3F52D]/[0.06]"
        >
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div className="min-w-0 space-y-3">
                    <div
                        role="radiogroup"
                        aria-label="Exam level"
                        className="inline-flex rounded-full border border-[#E3E5EA] bg-white p-1 dark:border-slate-700 dark:bg-slate-900"
                    >
                        {TRACKS.map((t) => (
                            <button
                                key={t}
                                type="button"
                                role="radio"
                                aria-checked={track === t}
                                onClick={() => chooseTrack(t)}
                                className={`rounded-full px-3 py-1.5 text-xs font-semibold transition-colors focus-visible:ring-2 focus-visible:ring-[#5B35F5] focus-visible:outline-none sm:text-sm ${
                                    track === t
                                        ? 'bg-[#5B35F5] text-white dark:bg-[#B3F52D] dark:text-[#0A0A0A]'
                                        : 'text-slate-600 hover:text-[#101426] dark:text-slate-300 dark:hover:text-white'
                                }`}
                            >
                                {TRACK_LABEL[t]}
                            </button>
                        ))}
                    </div>

                    {state.phase === 'none' ? (
                        <div>
                            <h2 className="text-lg font-semibold text-[#101426] dark:text-white">
                                No confirmed CSC exam date yet
                            </h2>
                            <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
                                The countdown returns once the Civil Service
                                Commission publishes the next sitting.
                            </p>
                        </div>
                    ) : (
                        <div>
                            <p className="text-xs font-semibold tracking-wider text-[#5B35F5] uppercase dark:text-[#B3F52D]">
                                {state.phase === 'today'
                                    ? 'Exam Day Today'
                                    : 'Until exam day'}
                            </p>
                            <h2 className="mt-1 flex items-start gap-2 text-lg font-semibold text-[#101426] sm:text-xl dark:text-white">
                                <CalendarDays className="mt-0.5 size-5 shrink-0 text-[#5B35F5] dark:text-[#B3F52D]" />
                                <span>
                                    CSE {TRACK_LABEL[track]} ·{' '}
                                    {formatPhDate(state.sitting.date)}
                                </span>
                            </h2>
                            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                {source === 'csc' ? (
                                    <>
                                        Confirmed by the{' '}
                                        {sourceUrl ? (
                                            <a
                                                href={sourceUrl}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="underline underline-offset-2"
                                            >
                                                CSC exam calendar
                                            </a>
                                        ) : (
                                            'CSC exam calendar'
                                        )}
                                        . Counting to 12:00 AM Philippine time.
                                    </>
                                ) : (
                                    'Date set by your Civio admin. Counting to 12:00 AM Philippine time.'
                                )}
                            </p>
                        </div>
                    )}
                </div>

                {state.phase === 'counting' && (
                    <div
                        className="grid grid-cols-4 gap-2 sm:gap-3"
                        aria-live="off"
                    >
                        {units.map(([label, value]) => (
                            <div
                                key={label}
                                data-unit={label}
                                className="flex min-w-0 flex-col items-center rounded-xl border border-[#E3E5EA] bg-white px-2 py-2.5 sm:min-w-[4.75rem] sm:px-3 sm:py-3 dark:border-slate-800 dark:bg-slate-900"
                            >
                                <span
                                    className={`font-mono text-2xl font-semibold tabular-nums sm:text-3xl ${
                                        label === 'Secs'
                                            ? 'text-[#5B35F5] dark:text-[#B3F52D]'
                                            : 'text-[#101426] dark:text-white'
                                    }`}
                                >
                                    {label === 'Days'
                                        ? value
                                        : pad(value as number)}
                                </span>
                                <span className="mt-0.5 text-[11px] font-medium text-slate-500 uppercase sm:text-xs dark:text-slate-400">
                                    {label}
                                </span>
                            </div>
                        ))}
                    </div>
                )}

                {state.phase === 'today' && (
                    <div className="rounded-xl bg-[#B3F52D] px-4 py-3 text-center text-base font-semibold text-[#0A0A0A]">
                        Good luck today
                    </div>
                )}
            </div>

            {milestone && (
                <div
                    data-testid="exam-milestone"
                    className="mt-4 flex flex-wrap items-center gap-x-2 gap-y-1 border-t border-[#5B35F5]/10 pt-3 text-sm text-slate-600 dark:border-white/10 dark:text-slate-300"
                >
                    <Flag className="size-4 shrink-0 text-[#5B35F5] dark:text-[#B3F52D]" />
                    <span className="font-medium text-[#101426] dark:text-white">
                        Next milestone:
                    </span>
                    <span>
                        {formatPhDate(milestone.date)} ·{' '}
                        {milestoneText(milestone)}
                    </span>
                </div>
            )}
        </section>
    );
}
