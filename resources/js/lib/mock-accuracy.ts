/**
 * Mock Accuracy: correct over scored questions on submitted Civio mocks.
 * A practice measurement, never a pass prediction. Representative (Strict)
 * mocks are reported apart from personalized (Study and legacy) mocks.
 */
export interface MockAccuracyPart {
    correct: number;
    total: number;
    mocks: number;
    percent: number | null;
}

export interface MockAccuracy extends MockAccuracyPart {
    tracks: string[];
    representative: MockAccuracyPart;
    personalized: MockAccuracyPart & { legacy: number };
    note?: string;
}

export interface MockAccuracySummary {
    hasMocks: boolean;
    percent: number | null;
    display: string;
    counts: string;
    sample: string;
    track: string;
    strictLine: string;
    personalizedLine: string;
}

const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? '' : 's'}`;

function partLine(label: string, p: MockAccuracyPart | undefined): string {
    if (!p || p.mocks <= 0 || p.total <= 0) {
        return `${label}: none yet`;
    }

    return `${label}: ${p.correct}/${p.total} correct (${p.percent ?? 0}%) in ${plural(p.mocks, 'mock')}`;
}

/** Safe for missing or legacy payloads: never throws, never invents a number. */
export function summarizeMockAccuracy(
    ma: Partial<MockAccuracy> | null | undefined,
): MockAccuracySummary {
    const total = Number(ma?.total ?? 0);
    const mocks = Number(ma?.mocks ?? 0);
    const hasMocks = total > 0 && mocks > 0;
    const percent =
        hasMocks && typeof ma?.percent === 'number' ? ma.percent : null;
    const tracks = Array.isArray(ma?.tracks) ? ma.tracks : [];
    const legacy = Number(ma?.personalized?.legacy ?? 0);

    return {
        hasMocks,
        percent,
        display: percent === null ? '—' : `${percent}%`,
        counts: hasMocks
            ? `${ma?.correct ?? 0}/${total} correct`
            : 'No mock yet',
        sample: hasMocks
            ? `${plural(mocks, 'mock')}, ${plural(total, 'scored question')}`
            : 'No submitted mocks',
        track: tracks.length > 0 ? tracks.join(', ') : '—',
        strictLine: partLine('Strict (representative)', ma?.representative),
        personalizedLine:
            partLine('Study and older personalized', ma?.personalized) +
            (legacy > 0 ? `, ${legacy} from before policies were stored` : ''),
    };
}
