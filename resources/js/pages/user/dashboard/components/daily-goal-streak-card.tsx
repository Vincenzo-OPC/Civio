import { CheckCircle2 } from 'lucide-react';
import type { DailyGoalStats } from '../types';
import { DashPanel } from './dash-panel';

interface DailyGoalStreakCardProps {
    dailyGoal?: DailyGoalStats;
}

const DAYS_OF_WEEK = [
    { label: 'M', name: 'Monday' },
    { label: 'T', name: 'Tuesday' },
    { label: 'W', name: 'Wednesday' },
    { label: 'T', name: 'Thursday' },
    { label: 'F', name: 'Friday' },
    { label: 'S', name: 'Saturday' },
    { label: 'S', name: 'Sunday' },
];

export function DailyGoalStreakCard({ dailyGoal }: DailyGoalStreakCardProps) {
    const streak = dailyGoal?.streak ?? 0;
    const questionsToday = dailyGoal?.questionsToday ?? 0;
    const goalTarget = dailyGoal?.goalTarget ?? 20;

    const progressPct = Math.min(
        100,
        Math.round((questionsToday / goalTarget) * 100),
    );
    const isGoalMet = questionsToday >= goalTarget;

    // 0 = Monday, 6 = Sunday
    const todayDayIndex = (new Date().getDay() + 6) % 7;

    return (
        <DashPanel
            id="daily-goal-title"
            title="Daily Goal"
            subtitle={`Answer ${goalTarget} questions a day.`}
            footer={
                <>
                    <span className="text-sm font-semibold">
                        {streak > 0 ? `${streak}-Day Streak` : 'No Streak Yet'}
                    </span>
                    <span className="dash-muted text-xs">
                        Resets at 12:00 AM
                    </span>
                </>
            }
        >
            <div className="flex items-end justify-between gap-3">
                <p className="font-heading text-4xl leading-none font-semibold tracking-tight tabular-nums">
                    {questionsToday}
                    <span className="dash-muted text-xl font-medium">
                        {' '}
                        / {goalTarget}
                    </span>
                </p>
                <p className="dash-muted text-sm tabular-nums">
                    {progressPct}%
                </p>
            </div>

            <div
                className="mt-3 h-2 overflow-hidden rounded-full bg-(--dash-track)"
                role="progressbar"
                aria-label="Questions answered today"
                aria-valuemin={0}
                aria-valuemax={goalTarget}
                aria-valuenow={Math.min(questionsToday, goalTarget)}
            >
                <div
                    className="h-full rounded-full bg-(--dash-accent)"
                    style={{ width: `${progressPct}%` }}
                />
            </div>

            <p className="mt-2 flex items-center gap-1.5 text-sm">
                {isGoalMet ? (
                    <>
                        <CheckCircle2
                            className="size-4 text-(--dash-mark)"
                            aria-hidden
                        />
                        <span className="font-medium">Goal met for today.</span>
                    </>
                ) : (
                    <span className="dash-muted">
                        {goalTarget - questionsToday} more to reach today's
                        goal.
                    </span>
                )}
            </p>

            <div className="mt-auto pt-5">
                <p className="dash-muted mb-2 text-xs font-medium">This Week</p>
                <ol className="grid grid-cols-7 gap-1.5">
                    {DAYS_OF_WEEK.map((day, idx) => {
                        const isToday = idx === todayDayIndex;
                        const isCompleted =
                            streak > 0 &&
                            idx <= todayDayIndex &&
                            todayDayIndex - idx < streak;

                        return (
                            <li
                                key={idx}
                                aria-label={`${day.name}: ${
                                    isCompleted
                                        ? 'goal met'
                                        : isToday
                                          ? 'today'
                                          : 'not yet'
                                }`}
                                className={`flex h-8 items-center justify-center rounded-md text-xs font-semibold ${
                                    isCompleted
                                        ? 'bg-(--dash-accent) text-(--dash-on-accent)'
                                        : isToday
                                          ? 'border border-(--dash-accent) text-(--dash-mark)'
                                          : 'dash-tile dash-muted'
                                }`}
                            >
                                {day.label}
                            </li>
                        );
                    })}
                </ol>
            </div>
        </DashPanel>
    );
}
