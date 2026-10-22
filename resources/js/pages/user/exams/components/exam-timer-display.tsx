import React, { useSyncExternalStore } from 'react';
import { TimeDial } from '@/components/domain/time-dial';
import { examClockTone, formatExamLeft } from '@/lib/exam-clock';
import type { ClockTone } from '@/lib/exam-clock';
import { formatSitting } from '@/lib/exam-dials';
import type { ExamClockSnapshot } from '../hooks/use-exam-timer';

interface ExamTimerDisplayProps {
    isTimed: boolean;
    timeLeft: number;
    itemElapsed: number;
    formatTime: (secs: number) => string;
    totalSeconds?: number;
    subscribeClock?: (listener: () => void) => () => void;
    getClockSnapshot?: () => ExamClockSnapshot;
}

function toneClass(tone: ClockTone): string {
    if (tone === 'red') {
        return 'text-[var(--civio-error)]';
    }

    if (tone === 'amber') {
        return 'text-amber-700 dark:text-amber-300';
    }

    return 'text-[var(--civio-ink)]/70';
}

/**
 * Untimed sessions show no clock. Timed: a compact pill on phones, a hairline
 * ring beside larger tabular digits from `sm` up. The ring and digits both read
 * the same authoritative snapshot; this component adds no interval.
 */
function ClockReadout({
    isTimed,
    timeLeft,
    totalSeconds,
}: {
    isTimed: boolean;
    timeLeft: number;
    totalSeconds?: number;
}) {
    if (!isTimed) {
        return null;
    }

    const tone = examClockTone(timeLeft);
    const hasTotal = !!totalSeconds && totalSeconds > 0;

    return (
        <div
            role="timer"
            data-clock-tone={tone}
            className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-[var(--civio-line)] px-2.5 py-1 text-xs font-semibold tabular-nums sm:gap-2 sm:border-transparent sm:px-1 sm:text-sm"
        >
            {hasTotal ? (
                <TimeDial
                    compact
                    fine
                    decorative
                    totalSeconds={totalSeconds}
                    remainingSeconds={timeLeft}
                    tone={tone}
                    className="sm:size-8"
                />
            ) : null}
            <span
                className={toneClass(tone)}
                title={
                    hasTotal
                        ? `Time left of ${formatSitting(totalSeconds)}`
                        : 'Time left for the whole mock'
                }
            >
                {formatExamLeft(timeLeft)}
                {hasTotal ? (
                    <span className="sr-only">
                        {' '}
                        left of {formatSitting(totalSeconds)}
                    </span>
                ) : null}
            </span>
        </div>
    );
}

function LiveClock({
    isTimed,
    totalSeconds,
    subscribeClock,
    getClockSnapshot,
}: {
    isTimed: boolean;
    totalSeconds?: number;
    subscribeClock: (listener: () => void) => () => void;
    getClockSnapshot: () => ExamClockSnapshot;
}) {
    const snap = useSyncExternalStore(
        subscribeClock,
        getClockSnapshot,
        getClockSnapshot,
    );

    return (
        <ClockReadout
            isTimed={isTimed}
            timeLeft={snap.timeLeft}
            totalSeconds={totalSeconds}
        />
    );
}

export const ExamTimerDisplay = React.memo(function ExamTimerDisplay({
    isTimed,
    timeLeft,
    totalSeconds,
    subscribeClock,
    getClockSnapshot,
}: ExamTimerDisplayProps) {
    if (subscribeClock && getClockSnapshot) {
        return (
            <LiveClock
                isTimed={isTimed}
                totalSeconds={totalSeconds}
                subscribeClock={subscribeClock}
                getClockSnapshot={getClockSnapshot}
            />
        );
    }

    return (
        <ClockReadout
            isTimed={isTimed}
            timeLeft={timeLeft}
            totalSeconds={totalSeconds}
        />
    );
});
