import { Timer } from 'lucide-react';
import React, { useSyncExternalStore } from 'react';
import {
    examClockTone,
    formatExamLeft,
    formatItemElapsed,
    itemClockTone,
} from '@/lib/exam-clock';
import type { ClockTone } from '@/lib/exam-clock';
import type { ExamClockSnapshot } from '../hooks/use-exam-timer';

interface ExamTimerDisplayProps {
    isTimed: boolean;
    timeLeft: number;
    itemElapsed: number;
    formatTime: (secs: number) => string;
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
}: {
    isTimed: boolean;
    timeLeft: number;
    itemElapsed: number;
}) {
    return (
        <div className="inline-flex items-center gap-2 text-xs font-semibold tabular-nums">
            {isTimed ? (
                <span
                    className={toneClass(examClockTone(timeLeft))}
                    title="Time left for the whole mock"
                >
                    {formatExamLeft(timeLeft)}
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
    subscribeClock,
    getClockSnapshot,
}: {
    isTimed: boolean;
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
        />
    );
}

export const ExamTimerDisplay = React.memo(function ExamTimerDisplay({
    isTimed,
    timeLeft,
    itemElapsed,
    subscribeClock,
    getClockSnapshot,
}: ExamTimerDisplayProps) {
    if (subscribeClock && getClockSnapshot) {
        return (
            <LiveClock
                isTimed={isTimed}
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
        />
    );
});
