import { Head } from '@inertiajs/react';
import { useCallback, useEffect, useState } from 'react';
import { OnlineBadge } from '@/components/shared/online-badge';
import { useOnlineStatus } from '@/hooks/use-online-status';
import { recordGuestStudyBias } from '@/lib/guest-study-bias';
import { postOfflineAttempts } from '@/lib/offline/api';
import { buildOfflineSession, scoreOfflineSession } from '@/lib/offline/grader';
import type { LocalScore } from '@/lib/offline/grader';
import {
    answersFromSession,
    enqueue,
    syncQueue,
} from '@/lib/offline/sync-queue';
import type { SyncSummary } from '@/lib/offline/sync-queue';
import type { StoredPack } from '@/lib/offline/types';
import { OfflineDrillRunner } from './components/offline-drill-runner';
import type { OfflineSession } from './components/offline-drill-runner';
import { OfflinePackPicker } from './components/offline-pack-picker';
import { offlineStore } from './store';

/**
 * Lite L2 offline drills. Opens with no network (service worker cache), runs
 * drills from downloaded packs, grades locally, queues answers in IndexedDB
 * and syncs them when online. Only the server's re-grade updates study stats.
 */
export default function OfflineDrillsPage() {
    const online = useOnlineStatus();
    const [packs, setPacks] = useState<StoredPack[]>([]);
    const [pending, setPending] = useState(0);
    const [session, setSession] = useState<OfflineSession | null>(null);
    const [score, setScore] = useState<LocalScore | null>(null);
    const [sync, setSync] = useState<SyncSummary | null>(null);
    const [syncing, setSyncing] = useState(false);

    const refresh = useCallback(async () => {
        const [storedPacks, queue] = await Promise.all([
            offlineStore.listPacks(),
            offlineStore.loadQueue(),
        ]);
        setPacks(storedPacks);
        setPending(queue.length);
    }, []);

    const runSync = useCallback(async () => {
        if (!navigator.onLine) {
            return;
        }

        setSyncing(true);

        try {
            setSync(
                await syncQueue({
                    loadQueue: offlineStore.loadQueue,
                    saveQueue: offlineStore.saveQueue,
                    post: postOfflineAttempts,
                    recordBias: (input) => recordGuestStudyBias('Drill', input),
                    isOnline: () => navigator.onLine,
                }),
            );
        } finally {
            setSyncing(false);
            await refresh();
        }
    }, [refresh]);

    // Load packs; sync right away if answers are waiting and we are online.
    useEffect(() => {
        let alive = true;

        Promise.all([offlineStore.listPacks(), offlineStore.loadQueue()])
            .then(([storedPacks, queue]) => {
                if (!alive) {
                    return;
                }

                setPacks(storedPacks);
                setPending(queue.length);

                if (queue.length > 0 && navigator.onLine) {
                    void runSync();
                }
            })
            .catch(() => alive && setPacks([]));

        return () => {
            alive = false;
        };
    }, [runSync]);

    // Sync when the connection comes back.
    useEffect(() => {
        const onOnline = () => void runSync();
        window.addEventListener('online', onOnline);

        return () => window.removeEventListener('online', onOnline);
    }, [runSync]);

    const start = (pack: StoredPack, count: number | 'all') => {
        const built = buildOfflineSession(pack.items, count, Math.random);
        setScore(null);
        setSession({ title: `${pack.category} (offline)`, ...built });
    };

    const finish = async (answers: Record<number, number>) => {
        if (!session) {
            return;
        }

        const versions = Object.fromEntries(
            packs.map((pack) => [pack.category, pack.version]),
        );
        const queued = answersFromSession(
            session.items,
            session.questions,
            answers,
            versions,
            new Date(),
        );

        await offlineStore.saveQueue(
            enqueue(await offlineStore.loadQueue(), queued),
        );
        setScore(
            scoreOfflineSession(session.items, session.questions, answers),
        );
        setSession(null);
        await refresh();
        await runSync();
    };

    if (session) {
        return (
            <>
                <Head title="Offline drill" />
                <OfflineDrillRunner
                    session={session}
                    onFinish={(answers) => void finish(answers)}
                    onExit={() => setSession(null)}
                />
            </>
        );
    }

    return (
        <div className="min-h-screen bg-background p-3 text-foreground sm:p-6">
            <Head title="Offline drills" />
            <div className="mx-auto flex w-full max-w-2xl flex-col gap-4">
                <div className="flex items-center justify-between gap-2">
                    <h1 className="text-lg font-bold">Offline drills</h1>
                    <OnlineBadge online={online} />
                </div>

                {score && <ScoreCard score={score} online={online} />}

                <SyncStatus
                    pending={pending}
                    online={online}
                    syncing={syncing}
                    last={sync}
                    onSync={() => void runSync()}
                />

                <OfflinePackPicker packs={packs} onStart={start} />

                {online && (
                    <a href="/drills" className="text-sm underline">
                        Back to Practice Drills
                    </a>
                )}
            </div>
        </div>
    );
}

function ScoreCard({ score, online }: { score: LocalScore; online: boolean }) {
    return (
        <div className="rounded-lg border border-border p-3 text-sm">
            <p className="font-bold">
                Drill done: {score.correct} of {score.total} correct (
                {score.answered} answered)
            </p>
            <p className="text-muted-foreground">
                {online
                    ? 'Checking your answers with Civio now.'
                    : 'Saved on this device. Civio checks them when you are back online.'}
            </p>
        </div>
    );
}

interface SyncStatusProps {
    pending: number;
    online: boolean;
    syncing: boolean;
    last: SyncSummary | null;
    onSync: () => void;
}

function SyncStatus({
    pending,
    online,
    syncing,
    last,
    onSync,
}: SyncStatusProps) {
    return (
        <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border p-3 text-sm">
            <div>
                <p>
                    {pending === 0
                        ? 'All answers synced.'
                        : `${pending} answer${pending === 1 ? '' : 's'} waiting to sync.`}
                </p>
                {last && last.sent > 0 && (
                    <p className="text-xs text-muted-foreground">
                        Last sync: {last.accepted} checked ({last.correct}{' '}
                        correct)
                        {last.rejected > 0
                            ? `, ${last.rejected} not counted (pack out of date)`
                            : ''}
                        .
                    </p>
                )}
                {last?.error && last.error !== 'offline' && (
                    <p className="text-xs text-red-600">
                        Sync stopped: {last.error}. Your answers are kept.
                    </p>
                )}
            </div>
            {pending > 0 && (
                <button
                    type="button"
                    onClick={onSync}
                    disabled={!online || syncing}
                    className="lite-tap rounded-lg border border-border px-3 py-1.5 font-semibold disabled:opacity-40"
                >
                    {syncing ? 'Syncing…' : 'Sync now'}
                </button>
            )}
        </div>
    );
}
