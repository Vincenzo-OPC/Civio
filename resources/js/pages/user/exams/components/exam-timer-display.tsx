import { Timer } from 'lucide-react';
import React from 'react';

interface ExamTimerDisplayProps {
    isTimed: boolean;
    timeLeft: number;
    itemElapsed: number;
    formatTime: (secs: number) => string;
}

type ClockTone = 'calm' | 'amber' | 'red';

function formatExamLeft(secs: number): string {
    const safe = Math.max(0, Math.floor(secs));
    const h = Math.floor(safe / 3600);
    const m = Math.floor((safe % 3600) / 60);
    const s = safe % 60;

    return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function formatItemElapsed(secs: number): string {
    const safe = Math.max(0, Math.floor(secs));
    const m = Math.floor(safe / 60);
    const s = safe % 60;

    return `${m}:${String(s).padStart(2, '0')}`;
}

function examTone(timeLeft: number): ClockTone {
    if (timeLeft <= 120) {
        return 'red';
    }

    if (timeLeft <= 600) {
        return 'amber';
    }

    return 'calm';
}

function itemTone(elapsed: number): ClockTone {
    if (elapsed > 75) {
        return 'red';
    }

    if (elapsed >= 45) {
        return 'amber';
    }

    return 'calm';
}

function toneClass(tone: ClockTone): string {
    if (tone === 'red') {
        return 'border-rose-300 bg-rose-50 text-rose-700 dark:border-rose-900/60 dark:bg-rose-950/60 dark:text-rose-300';
    }

    if (tone === 'amber') {
        return 'border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-900/60 dark:bg-amber-950/50 dark:text-amber-300';
    }

    return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900/40 dark:bg-emerald-950/40 dark:text-emerald-300';
}

function ClockChip({
    label,
    value,
    tone,
    title,
}: {
    label: string;
    value: string;
    tone: ClockTone;
    title: string;
}) {
    return (
        <div
            className={`inline-flex h-8 items-center gap-1.5 rounded-lg border px-2.5 text-xs font-semibold tracking-tight ${toneClass(tone)}`}
            title={title}
            aria-live="polite"
        >
            <Timer className="size-3.5 shrink-0 opacity-80" />
            <span className="whitespace-nowrap">{label}</span>
            <span className="font-mono font-bold tabular-nums">{value}</span>
        </div>
    );
}

export const ExamTimerDisplay = React.memo(function ExamTimerDisplay({
    isTimed,
    timeLeft,
    itemElapsed,
}: ExamTimerDisplayProps) {
    return (
        <div className="inline-flex items-center gap-1.5">
            {isTimed ? (
                <ClockChip
                    label="Exam left"
                    value={formatExamLeft(timeLeft)}
                    tone={examTone(timeLeft)}
                    title="Time left for the whole mock. Amber in the last 10 minutes, red in the last 2."
                />
            ) : (
                <div className="inline-flex h-8 items-center gap-1.5 rounded-lg border border-border bg-muted/60 px-3 text-xs font-semibold text-muted-foreground">
                    <Timer className="size-3.5 text-muted-foreground" />
                    <span>Untimed</span>
                </div>
            )}
            <ClockChip
                label="This item"
                value={formatItemElapsed(itemElapsed)}
                tone={itemTone(itemElapsed)}
                title="Time on this item only. Resets when you move. Amber from 45s, red after 75s."
            />
        </div>
    );
});
