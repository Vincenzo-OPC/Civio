import { Link } from '@inertiajs/react';
import { CheckCircle2, Circle, ChevronRight } from 'lucide-react';
import { useState } from 'react';
import { index as historyIndex } from '@/routes/history';
import { index as calendarIndex } from '@/routes/study-schedules/index';
import type { TodayTaskItem, RecentAttemptItem } from '../types';
import { DashPanel } from './dash-panel';

interface StudyScheduleActivityCardProps {
    todayTasks?: TodayTaskItem[];
    overdueTasksCount?: number;
    recentAttempts?: RecentAttemptItem[];
}

export function StudyScheduleActivityCard({
    todayTasks = [],
    overdueTasksCount = 0,
    recentAttempts = [],
}: StudyScheduleActivityCardProps) {
    const [tasks, setTasks] = useState(todayTasks);

    const toggleTask = async (taskId: number, currentStatus: boolean) => {
        // Optimistic UI update
        const newStatus = !currentStatus;
        setTasks((prev) =>
            prev.map((t) =>
                t.id === taskId ? { ...t, is_done: newStatus } : t,
            ),
        );

        try {
            const csrfToken =
                (
                    document.querySelector(
                        'meta[name="csrf-token"]',
                    ) as HTMLMetaElement
                )?.content || '';

            const res = await fetch(`/study-schedules/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': csrfToken,
                    Accept: 'application/json',
                },
                body: JSON.stringify({
                    is_done: newStatus,
                }),
            });

            if (!res.ok) {
                // Revert on error
                setTasks(todayTasks);
            }
        } catch {
            setTasks(todayTasks);
        }
    };

    const visibleAttempts = recentAttempts.slice(0, 4);

    return (
        <DashPanel
            id="activity-title"
            title="Plan and Results"
            subtitle="Today's study tasks and your latest scores."
            footer={
                <Link href={historyIndex()} className="dash-link">
                    Full History
                    <ChevronRight className="size-4" aria-hidden />
                </Link>
            }
        >
            {overdueTasksCount > 0 && (
                <div className="dash-tile mb-4 flex items-center justify-between gap-3 px-3 py-2 text-sm">
                    <span className="font-semibold">
                        {overdueTasksCount} overdue{' '}
                        {overdueTasksCount === 1 ? 'task' : 'tasks'}
                    </span>
                    <Link href={calendarIndex()} className="dash-link">
                        Review
                    </Link>
                </div>
            )}

            <div className="mb-2 flex items-center justify-between">
                <h3 className="dash-muted text-xs font-semibold">
                    Today&apos;s Tasks
                </h3>
                <Link href={calendarIndex()} className="dash-link text-[13px]">
                    {tasks.length > 0 ? 'Study Planner' : 'Plan a Session'}
                </Link>
            </div>

            {tasks.length > 0 ? (
                <ul className="space-y-1.5">
                    {tasks.map((task) => (
                        <li
                            key={task.id}
                            className="dash-tile flex items-center justify-between gap-3 px-3 py-2"
                        >
                            <div className="flex min-w-0 items-center gap-2.5">
                                <button
                                    type="button"
                                    onClick={() =>
                                        toggleTask(task.id, task.is_done)
                                    }
                                    className="shrink-0 rounded-full"
                                    aria-label={
                                        task.is_done
                                            ? 'Mark as incomplete'
                                            : 'Mark as complete'
                                    }
                                >
                                    {task.is_done ? (
                                        <CheckCircle2 className="size-5 text-(--dash-mark)" />
                                    ) : (
                                        <Circle className="dash-muted size-5" />
                                    )}
                                </button>
                                <div className="min-w-0">
                                    <p
                                        className={`truncate text-sm font-medium ${
                                            task.is_done
                                                ? 'dash-muted line-through'
                                                : ''
                                        }`}
                                    >
                                        {task.title}
                                    </p>
                                    {task.subcategory_name && (
                                        <p className="dash-muted truncate text-xs">
                                            {task.subcategory_name}
                                        </p>
                                    )}
                                </div>
                            </div>
                            {task.study_time && (
                                <span className="dash-muted shrink-0 text-xs tabular-nums">
                                    {task.study_time}
                                </span>
                            )}
                        </li>
                    ))}
                </ul>
            ) : (
                <p className="dash-muted text-sm">Nothing scheduled today.</p>
            )}

            <h3 className="dash-muted mt-5 mb-2 text-xs font-semibold">
                Recent Results
            </h3>
            {visibleAttempts.length > 0 ? (
                <ul className="divide-y divide-(--dash-line)">
                    {visibleAttempts.map((attempt) => (
                        <li key={attempt.id}>
                            <Link
                                href={historyIndex()}
                                className="flex items-center justify-between gap-3 py-2"
                            >
                                <div className="min-w-0">
                                    <p className="truncate text-sm font-medium">
                                        {attempt.title}
                                    </p>
                                    <p className="dash-muted text-xs">
                                        {attempt.total_questions} items ·{' '}
                                        {attempt.created_at_human}
                                    </p>
                                </div>
                                <span className="shrink-0 font-heading text-base font-semibold tabular-nums">
                                    {attempt.score_percentage}%
                                </span>
                            </Link>
                        </li>
                    ))}
                </ul>
            ) : (
                <p className="dash-muted text-sm">
                    No results yet. Finish a drill or mock to see scores here.
                </p>
            )}
        </DashPanel>
    );
}
