import { Link, router, usePage } from '@inertiajs/react';
import { ChevronRight, Loader2, AlertCircle } from 'lucide-react';
import { useEffect, useState } from 'react';
import { summarizeMockAccuracy } from '@/lib/mock-accuracy';
import { connectRealtime } from '@/lib/realtime';
import type { Auth } from '@/types';
import type { AiAnalysisData } from '../types';
import { DashPanel } from './dash-panel';

interface AiReadinessBentoCardProps {
    aiAnalysis?: {
        status: 'no_data' | 'generating' | 'ready' | 'failed' | 'no_exam_date';
        data: AiAnalysisData | null;
    };
}

export function AiReadinessBentoCard({
    aiAnalysis,
}: AiReadinessBentoCardProps) {
    const { auth, pusher } = usePage<{ auth: Auth; pusher?: any }>().props;
    const initialStatus = aiAnalysis?.status || 'no_data';
    const [localStatus, setLocalStatus] = useState(initialStatus);
    const [prevInitialStatus, setPrevInitialStatus] = useState(initialStatus);
    const [progress, setProgress] = useState(25);
    const data = aiAnalysis?.data;

    if (initialStatus !== prevInitialStatus) {
        setPrevInitialStatus(initialStatus);
        setLocalStatus(initialStatus);
    }

    useEffect(() => {
        if (localStatus !== 'generating') {
            // eslint-disable-next-line react-hooks/set-state-in-effect
            setProgress(25);

            return;
        }

        const interval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 92) {
                    return 92;
                }

                const step = Math.floor(Math.random() * 8) + 4;

                return Math.min(prev + step, 92);
            });
        }, 400);

        return () => clearInterval(interval);
    }, [localStatus]);

    useEffect(() => {
        if (localStatus !== 'generating' || !auth?.user?.id || !pusher?.key) {
            return;
        }

        return connectRealtime(pusher, (echo) => {
            const channel = echo.private(`App.Models.User.${auth.user.id}`);

            channel.listen('.ai-analysis-ready', () => {
                setProgress(100);
                router.reload({ only: ['aiAnalysis'] });
            });

            channel.listen('.ai-analysis-failed', () => {
                setLocalStatus('failed');
            });

            return () => {
                channel.stopListening('.ai-analysis-ready');
                channel.stopListening('.ai-analysis-failed');
                echo.leave(`App.Models.User.${auth.user.id}`);
            };
        });
    }, [localStatus, auth?.user?.id, pusher]);

    const accuracy = summarizeMockAccuracy(data?.mock_accuracy);
    const pct = accuracy.percent ?? 0;
    const primaryWeakness = data?.critical_weaknesses?.[0];
    const noMock = !accuracy.hasMocks;
    const showEmpty =
        localStatus === 'no_data' || (localStatus === 'ready' && noMock);

    return (
        <DashPanel
            id="mock-accuracy-title"
            title="Mock Accuracy"
            subtitle="Correct answers over scored mock questions. Not a pass prediction."
            footer={
                <Link
                    href="/analytics/ai-analysis?from=/dashboard"
                    className="dash-link"
                >
                    View Practice Analytics
                    <ChevronRight className="size-4" aria-hidden />
                </Link>
            }
        >
            {localStatus === 'ready' && data && !noMock && (
                <div className="flex flex-1 flex-col">
                    <div className="flex items-end justify-between gap-3">
                        <p className="font-heading text-4xl leading-none font-semibold tracking-tight tabular-nums">
                            {accuracy.display}
                        </p>
                        <p className="dash-muted text-sm tabular-nums">
                            {accuracy.counts}
                        </p>
                    </div>
                    <div className="mt-3 h-2 overflow-hidden rounded-full bg-(--dash-track)">
                        <div
                            className="h-full rounded-full bg-(--dash-accent)"
                            style={{ width: `${pct}%` }}
                        />
                    </div>

                    <p className="mt-3 text-sm leading-relaxed">
                        {data.priority_action ||
                            'The next drill adds a practice score. It does not forecast a pass.'}
                    </p>

                    <dl
                        className="dash-muted mt-3 space-y-0.5 text-xs leading-5"
                        data-testid="mock-accuracy-detail"
                    >
                        <div>
                            <dt className="inline font-semibold">Track: </dt>
                            <dd className="inline">
                                {accuracy.track} · {accuracy.sample}
                            </dd>
                        </div>
                        <div>{accuracy.strictLine}</div>
                        <div>{accuracy.personalizedLine}</div>
                    </dl>

                    {primaryWeakness && (
                        <div className="dash-tile mt-auto flex items-center justify-between gap-3 px-3 py-2.5">
                            <p className="min-w-0 truncate text-sm">
                                <span className="dash-muted">Focus: </span>
                                <span className="font-semibold">
                                    {primaryWeakness}
                                </span>
                            </p>
                            <Link
                                href={`/drills?category=${encodeURIComponent(primaryWeakness)}&from=/dashboard`}
                                className="dash-link shrink-0"
                            >
                                Drill It
                                <ChevronRight className="size-4" aria-hidden />
                            </Link>
                        </div>
                    )}
                </div>
            )}

            {showEmpty && (
                <div className="flex flex-1 flex-col justify-center">
                    <p className="text-base font-semibold">No Mocks Yet</p>
                    <p className="dash-muted mt-0.5 text-sm">
                        Finish a full mock to see your accuracy. A full mock is
                        150 or 145 scored items.
                    </p>
                </div>
            )}

            {localStatus === 'generating' && (
                <div className="flex flex-1 flex-col justify-center gap-3">
                    <p className="flex items-center gap-2 text-sm font-medium">
                        <Loader2 className="size-4 animate-spin" aria-hidden />
                        Reading your finished attempts.
                    </p>
                    <div className="h-2 overflow-hidden rounded-full bg-(--dash-track)">
                        <div
                            className="h-full rounded-full bg-(--dash-accent)"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                </div>
            )}

            {localStatus === 'no_exam_date' && (
                <p className="dash-tile flex items-center gap-2 p-3 text-sm">
                    <AlertCircle className="size-4 shrink-0" aria-hidden />
                    Set an exam date if you want a countdown. The countdown is
                    not a forecast.
                </p>
            )}

            {localStatus === 'failed' && (
                <div className="dash-tile flex items-center justify-between gap-3 p-3 text-sm">
                    <span className="flex items-center gap-2">
                        <AlertCircle className="size-4 shrink-0" aria-hidden />
                        Analysis unavailable right now.
                    </span>
                    <button
                        type="button"
                        className="dash-link"
                        onClick={() => router.reload()}
                    >
                        Retry
                    </button>
                </div>
            )}
        </DashPanel>
    );
}
