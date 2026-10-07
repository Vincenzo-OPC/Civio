import { useCallback, useEffect, useState } from 'react';
import { OnlineBadge } from '@/components/shared/online-badge';
import { Card } from '@/components/ui/card';
import { useOnlineStatus } from '@/hooks/use-online-status';
import { writeOfflineOptIn } from '@/lib/lite-mode';
import { downloadPack, fetchManifest, formatKb } from '@/lib/offline/api';
import { createPackStore } from '@/lib/offline/pack-store';
import { OFFLINE_PAGE_URL, warmOfflineShell } from '@/lib/offline/shell';
import type { OfflinePackSummary, StoredPack } from '@/lib/offline/types';
import { registerServiceWorker } from '@/lib/pwa-register';

const store = createPackStore();

type BusyState = 'downloading' | 'removing';

/**
 * Lite L2: "Download for offline" in the Practice Drills hub. Lists category
 * packs with their size, and the downloaded ones with version, Update pack
 * and Remove. Loaded lazily, so idb-keyval stays out of the drills chunk.
 */
export default function OfflinePacksPanel() {
    const online = useOnlineStatus();
    const [manifest, setManifest] = useState<OfflinePackSummary[] | null>(null);
    const [stored, setStored] = useState<StoredPack[]>([]);
    const [busy, setBusy] = useState<Record<number, BusyState | undefined>>({});
    const [error, setError] = useState<string | null>(null);

    const refreshStored = useCallback(async () => {
        setStored(await store.listPacks());
    }, []);

    useEffect(() => {
        let alive = true;

        store
            .listPacks()
            .then((packs) => alive && setStored(packs))
            .catch(() => alive && setStored([]));

        return () => {
            alive = false;
        };
    }, []);

    useEffect(() => {
        if (!online) {
            return;
        }

        fetchManifest()
            .then((data) => setManifest(data.packs))
            .catch(() => setError('Could not load offline packs.'));
    }, [online]);

    useEffect(() => {
        if (online && stored.length > 0) {
            void warmOfflineShell();
        }
    }, [online, stored.length]);

    const setRowBusy = (categoryId: number, state: BusyState | undefined) =>
        setBusy((current) => ({ ...current, [categoryId]: state }));

    const download = async (summary: OfflinePackSummary) => {
        setRowBusy(summary.category_id, 'downloading');
        setError(null);

        try {
            await store.savePack(await downloadPack(summary));
            writeOfflineOptIn(true);
            registerServiceWorker();
            await warmOfflineShell();
            await refreshStored();
        } catch {
            setError(`Could not download ${summary.category}. Try again.`);
        } finally {
            setRowBusy(summary.category_id, undefined);
        }
    };

    const remove = async (categoryId: number) => {
        setRowBusy(categoryId, 'removing');

        try {
            await store.removePack(categoryId);
            await refreshStored();
        } finally {
            setRowBusy(categoryId, undefined);
        }
    };

    const storedById = new Map(stored.map((pack) => [pack.categoryId, pack]));
    const listed = new Set((manifest ?? []).map((s) => s.category_id));
    const rows: PackRowData[] = [
        ...(manifest ?? []).map((summary) => ({
            id: summary.category_id,
            summary,
            pack: storedById.get(summary.category_id),
        })),
        ...stored
            .filter((pack) => !listed.has(pack.categoryId))
            .map((pack) => ({ id: pack.categoryId, pack })),
    ];

    return (
        <Card className="flex flex-col gap-3 p-4 sm:p-6">
            <div className="flex flex-wrap items-center justify-between gap-2">
                <h2 className="text-base font-bold">Download for offline</h2>
                <OnlineBadge online={online} />
            </div>
            <p className="text-sm text-muted-foreground">
                Practise without a connection. Answers are saved on this device
                and checked by Civio when you are back online. Offline items
                never appear in full mock exams.
            </p>

            {error && <p className="text-sm text-red-600">{error}</p>}
            {manifest === null && online && !error && (
                <p className="text-sm text-muted-foreground">Loading packs…</p>
            )}
            {manifest !== null && rows.length === 0 && (
                <p className="text-sm text-muted-foreground">
                    No offline packs yet.
                </p>
            )}

            <ul className="flex flex-col gap-2">
                {rows.map((row) => (
                    <PackRow
                        key={row.id}
                        row={row}
                        online={online}
                        busy={busy[row.id]}
                        onDownload={download}
                        onRemove={remove}
                    />
                ))}
            </ul>

            {stored.length > 0 && (
                // Full page load on purpose: the service worker serves this
                // page from its cache when there is no network.
                <a
                    href={OFFLINE_PAGE_URL}
                    className="lite-tap self-start rounded-lg bg-blue-700 px-4 py-2 text-sm font-bold text-white"
                >
                    Open offline drills
                </a>
            )}
        </Card>
    );
}

interface PackRowData {
    id: number;
    summary?: OfflinePackSummary;
    pack?: StoredPack;
}

interface PackRowProps {
    row: PackRowData;
    online: boolean;
    busy?: BusyState;
    onDownload: (summary: OfflinePackSummary) => Promise<void>;
    onRemove: (categoryId: number) => Promise<void>;
}

function PackRow({ row, online, busy, onDownload, onRemove }: PackRowProps) {
    const { summary, pack } = row;
    const name = summary?.category ?? pack?.category ?? '';
    const outdated = !!summary && !!pack && summary.version !== pack.version;
    const button =
        'lite-tap rounded-lg border border-border px-3 py-1.5 text-sm font-semibold disabled:opacity-40';

    return (
        <li className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border p-3">
            <div className="min-w-0">
                <p className="text-sm font-semibold">{name}</p>
                <p className="text-xs text-muted-foreground">
                    {summary
                        ? `${summary.items} items · ${formatKb(summary.bytes)}`
                        : `${pack?.items.length ?? 0} items`}
                    {pack && ` · downloaded, version ${pack.version}`}
                    {outdated && ' · update available'}
                </p>
            </div>
            <div className="flex gap-2">
                {summary && (!pack || outdated) && (
                    <button
                        type="button"
                        className={button}
                        disabled={!online || !!busy}
                        onClick={() => void onDownload(summary)}
                    >
                        {busy === 'downloading'
                            ? 'Downloading…'
                            : pack
                              ? 'Update pack'
                              : `Download (${formatKb(summary.bytes)})`}
                    </button>
                )}
                {pack && (
                    <button
                        type="button"
                        className={button}
                        disabled={!!busy}
                        onClick={() => void onRemove(pack.categoryId)}
                    >
                        Remove
                    </button>
                )}
            </div>
        </li>
    );
}
