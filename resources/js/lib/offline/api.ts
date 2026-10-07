/** Lite L2: network calls for offline packs and answer sync. */
import type {
    OfflineManifest,
    OfflinePackPage,
    OfflinePackSummary,
    QueuedAnswer,
    StoredPack,
    SyncResponse,
} from './types';

function xsrfToken(): string {
    if (typeof document === 'undefined') {
        return '';
    }

    const match = document.cookie.match(/(?:^|;\s*)XSRF-TOKEN=([^;]+)/);

    return match ? decodeURIComponent(match[1] ?? '') : '';
}

async function getJson<T>(url: string): Promise<T> {
    const response = await fetch(url, {
        headers: {
            Accept: 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin',
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }

    return (await response.json()) as T;
}

export function fetchManifest(): Promise<OfflineManifest> {
    return getJson<OfflineManifest>('/offline/packs');
}

/** Download every page of one category pack. */
export async function downloadPack(
    summary: OfflinePackSummary,
    now: Date = new Date(),
): Promise<StoredPack> {
    const items: StoredPack['items'] = [];
    let version = summary.version;

    for (let page = 1; page <= Math.max(1, summary.pages); page++) {
        const data = await getJson<OfflinePackPage>(
            `/offline/packs/${summary.category_id}?page=${page}`,
        );
        items.push(...data.items);
        version = data.version;
    }

    return {
        categoryId: summary.category_id,
        category: summary.category,
        version,
        bytes: summary.bytes,
        downloadedAt: now.toISOString(),
        items,
    };
}

export async function postOfflineAttempts(
    batch: QueuedAnswer[],
): Promise<SyncResponse> {
    const response = await fetch('/offline/attempts', {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': xsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ attempts: batch }),
    });

    if (!response.ok) {
        throw new Error(`Sync failed (${response.status})`);
    }

    return (await response.json()) as SyncResponse;
}

export function formatKb(bytes: number): string {
    return `${Math.max(1, Math.round(bytes / 1024))} KB`;
}
