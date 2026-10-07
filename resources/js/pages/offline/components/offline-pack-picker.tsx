import { useState } from 'react';
import type { StoredPack } from '@/lib/offline/types';

const COUNTS = [10, 20, 50] as const;

type Count = (typeof COUNTS)[number] | 'all';

interface OfflinePackPickerProps {
    packs: StoredPack[];
    onStart: (pack: StoredPack, count: Count) => void;
}

/** Downloaded packs with their version and a start button. */
export function OfflinePackPicker({ packs, onStart }: OfflinePackPickerProps) {
    const [count, setCount] = useState<Count>(10);

    if (packs.length === 0) {
        return (
            <p className="text-sm text-muted-foreground">
                No packs on this device yet. Go online and open Practice Drills
                to download one.
            </p>
        );
    }

    return (
        <div className="flex flex-col gap-3">
            <label className="flex items-center gap-2 text-sm">
                Items per drill
                <select
                    value={String(count)}
                    onChange={(event) =>
                        setCount(
                            event.target.value === 'all'
                                ? 'all'
                                : (Number(event.target.value) as Count),
                        )
                    }
                    className="rounded border border-border bg-background px-2 py-1"
                >
                    {COUNTS.map((n) => (
                        <option key={n} value={n}>
                            {n}
                        </option>
                    ))}
                    <option value="all">All</option>
                </select>
            </label>

            <ul className="flex flex-col gap-2">
                {packs.map((pack) => (
                    <li
                        key={pack.categoryId}
                        className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border p-3"
                    >
                        <div className="min-w-0">
                            <p className="text-sm font-semibold">
                                {pack.category}
                            </p>
                            <p className="text-xs text-muted-foreground">
                                {pack.items.length} items · version{' '}
                                {pack.version} · saved{' '}
                                {new Date(
                                    pack.downloadedAt,
                                ).toLocaleDateString()}
                            </p>
                        </div>
                        <button
                            type="button"
                            onClick={() => onStart(pack, count)}
                            className="lite-tap rounded-lg bg-blue-700 px-4 py-1.5 text-sm font-bold text-white"
                        >
                            Start drill
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
