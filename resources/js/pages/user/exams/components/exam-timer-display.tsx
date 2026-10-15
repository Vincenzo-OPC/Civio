import { Timer } from 'lucide-react';
import React, { useSyncExternalStore } from 'react';
import { TimeDial } from '@/components/domain/time-dial';
import {
    examClockTone,
    formatExamLeft,
    formatItemElapsed,
    itemClockTone,
} from '@/lib/exam-clock';
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

function ClockReadout({
    isTimed,
    timeLeft,
    itemElapsed,
    totalSeconds,
}: {
    isTimed: boolean;
    timeLeft: number;
    itemElapsed: number;
    totalSeconds?: number;
}) {
    const tone = examClockTone(timeLeft);

    return (
        <div className="inline-flex shrink-0 items-center gap-1.5 text-xs font-semibold tabular-nums">
            {isTimed && totalSeconds && totalSeconds > 0 ? (
                <TimeDial
                    compact
                    decorative
                    totalSeconds={totalSeconds}
                    remainingSeconds={timeLeft}
                    tone={tone}
                />
            ) : null}
            {isTimed ? (
                <span
                    className={toneClass(tone)}
                    title={
                        totalSeconds && totalSeconds > 0
                            ? `Time left of ${formatSitting(totalSeconds)}`
                            : 'Time left for the whole mock'
                    }
                >
                    {formatExamLeft(timeLeft)}
                    {totalSeconds && totalSeconds > 0 ? (
                        <span className="sr-only">
                            {' '}
                            left of {formatSitting(totalSeconds)}
                        </span>
                    ) : null}
                </span>
            ) : (
                <span className="text-[var(--civio-ink)]/60">Untimed</span>
            )}
            <span className="text-[var(--civio-line)]" aria-hidden>
                ·
            </span>
            <span
                className={`inline-flex items-center gap-1 ${toneClass(itemClockTone(itemElapsed))}`}
                title="Time on this item. Resets when you move."
            >
                <Timer className="size-3.5 shrink-0 opacity-70" />
                {formatItemElapsed(itemElapsed)}
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
            itemElapsed={snap.itemElapsed}
            totalSeconds={totalSeconds}
        />
    );
}

export const ExamTimerDisplay = React.memo(function ExamTimerDisplay({
    isTimed,
    timeLeft,
    itemElapsed,
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
            itemElapsed={itemElapsed}
            totalSeconds={totalSeconds}
        />
    );
});
