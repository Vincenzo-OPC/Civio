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
    /** Controlled exam level (the dashboard lifts it to drive mock launches). */
    track?: ExamTrack;
    onTrackChange?: (track: ExamTrack) => void;
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
    track: controlledTrack,
    onTrackChange,
}: ExamCountdownProps) {
    const [now, setNow] = useState(() => initialNow ?? Date.now());
    const [ownTrack, setTrack] = useState<ExamTrack>(() => {
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

    const track = controlledTrack ?? ownTrack;

    useEffect(() => {
        const id = window.setInterval(() => setNow(Date.now()), 1000);

        return () => window.clearInterval(id);
    }, []);

    const chooseTrack = (next: ExamTrack) => {
        setTrack(next);
        onTrackChange?.(next);

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

    const trackPicker = (
        <div
            role="radiogroup"
            aria-label="Exam level"
            className="inline-flex shrink-0 rounded-lg border border-(--dash-line) bg-(--dash-sunken) p-0.5"
        >
            {TRACKS.map((t) => (
                <button
                    key={t}
                    type="button"
                    role="radio"
                    aria-checked={track === t}
                    onClick={() => chooseTrack(t)}
                    className={`rounded-md px-2.5 py-1.5 text-[13px] font-semibold transition-colors @xs:px-3 @xs:text-sm ${
                        track === t
                            ? 'bg-(--dash-accent) text-(--dash-on-accent)'
                            : 'dash-muted hover:text-(--dash-ink)'
                    }`}
                >
                    {TRACK_LABEL[t]}
                </button>
            ))}
        </div>
    );

    return (
        <section
            data-testid="exam-countdown"
            aria-label="Exam countdown"
            className="dash-panel @container"
        >
            {state.phase === 'none' ? (
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                        <h2 className="dash-title">
                            No confirmed CSC exam date yet
                        </h2>
                        <p className="dash-muted mt-1 text-sm">
                            The countdown returns once the Civil Service
                            Commission publishes the next sitting.
                        </p>
                    </div>
                    {trackPicker}
                </div>
            ) : (
                <div className="flex flex-col gap-5 @5xl:flex-row @5xl:items-center @5xl:justify-between @5xl:gap-8">
                    <div className="min-w-0 space-y-3">
                        <div className="flex flex-wrap items-center justify-between gap-3">
                            <p className="dash-eyebrow">
                                {state.phase === 'today'
                                    ? 'Exam Day Today'
                                    : 'Until exam day'}
                            </p>
                            {trackPicker}
                        </div>
                        <h2 className="flex items-start gap-2 font-heading text-xl font-semibold tracking-tight sm:text-2xl">
                            <CalendarDays className="mt-1 size-5 shrink-0 text-(--dash-mark)" />
                            <span>
                                CSE {TRACK_LABEL[track]}
                                <span className="sr-only @lg:not-sr-only">
                                    {' '}
                                    ·{' '}
                                </span>
                                <span className="block whitespace-nowrap @lg:inline">
                                    {formatPhDate(state.sitting.date)}
                                </span>
                            </span>
                        </h2>
                        <p className="dash-muted text-xs leading-relaxed">
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

                    {state.phase === 'counting' && (
                        <div
                            className="grid grid-cols-4 gap-2 sm:gap-3 @5xl:w-[26rem] @5xl:shrink-0"
                            aria-live="off"
                        >
                            {units.map(([label, value]) => (
                                <div
                                    key={label}
                                    data-unit={label}
                                    className="dash-tile flex min-w-0 flex-col items-center px-1 py-3 sm:py-4"
                                >
                                    <span
                                        className={`font-heading text-2xl leading-none font-semibold tracking-tight tabular-nums sm:text-4xl ${
                                            label === 'Days'
                                                ? 'text-(--dash-mark)'
                                                : ''
                                        }`}
                                    >
                                        {label === 'Days'
                                            ? value
                                            : pad(value as number)}
                                    </span>
                                    <span className="dash-muted mt-1.5 text-xs font-medium">
                                        {label}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}

                    {state.phase === 'today' && (
                        <div className="rounded-lg bg-[#B3F52D] px-5 py-3 text-center text-base font-semibold text-[#0A0A0A]">
                            Good luck today
                        </div>
                    )}
                </div>
            )}

            {milestone && (
                <div
                    data-testid="exam-milestone"
                    className="dash-muted mt-5 flex flex-wrap items-center gap-x-2 gap-y-1 border-t border-(--dash-line) pt-4 text-sm"
                >
                    <Flag className="size-4 shrink-0 text-(--dash-mark)" />
                    <span className="font-semibold text-(--dash-ink)">
                        Next Milestone
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
