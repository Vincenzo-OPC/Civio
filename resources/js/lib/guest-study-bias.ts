import type { CategoryScore } from '@/pages/user/exams/types';

export const GUEST_STUDY_BIAS_KEY = 'civio_guest_study_bias_v1';

export type StudyTrack = 'Professional' | 'Subprofessional' | 'Drill';

export type TrackBias = {
    wrongIds: number[];
    weakCategories: string[];
    weakSubcategories: string[];
};

export type StrengthRow = {
    kind: 'category' | 'subcategory';
    name: string;
    parent?: string;
    correct: number;
    /** Not correct on this attempt: wrong answers plus unanswered. */
    missed: number;
    total: number;
};

const TRACKS: StudyTrack[] = ['Professional', 'Subprofessional', 'Drill'];
const MAX_WRONG_IDS = 300;
const STRENGTH_RATIO = 0.8;

function emptyTrack(): TrackBias {
    return { wrongIds: [], weakCategories: [], weakSubcategories: [] };
}

function emptyStore(): Record<StudyTrack, TrackBias> {
    return {
        Professional: emptyTrack(),
        Subprofessional: emptyTrack(),
        Drill: emptyTrack(),
    };
}

function asIdList(value: unknown): number[] {
    if (!Array.isArray(value)) {
        return [];
    }

    const ids: number[] = [];

    for (const item of value) {
        const n = Number(item);

        if (Number.isFinite(n) && n > 0) {
            ids.push(n);
        }
    }

    return ids;
}

function asNameList(value: unknown): string[] {
    if (!Array.isArray(value)) {
        return [];
    }

    return value
        .map((item) => String(item || '').trim())
        .filter((name) => name.length > 0);
}

export function readGuestStudyBias(): Record<StudyTrack, TrackBias> {
    const store = emptyStore();

    if (typeof window === 'undefined') {
        return store;
    }

    try {
        const raw = window.localStorage.getItem(GUEST_STUDY_BIAS_KEY);

        if (!raw) {
            return store;
        }

        const parsed = JSON.parse(raw) as Partial<
            Record<StudyTrack, Partial<TrackBias>>
        >;

        for (const track of TRACKS) {
            const row = parsed?.[track];

            store[track] = {
                wrongIds: asIdList(row?.wrongIds).slice(0, MAX_WRONG_IDS),
                weakCategories: asNameList(row?.weakCategories),
                weakSubcategories: asNameList(row?.weakSubcategories),
            };
        }
    } catch {
        return emptyStore();
    }

    return store;
}

export function recordGuestStudyBias(
    track: StudyTrack,
    input: {
        wrongIds: number[];
        categoryScoreMap: Record<string, CategoryScore>;
    },
): void {
    if (typeof window === 'undefined') {
        return;
    }

    const store = readGuestStudyBias();
    const previous = store[track] ?? emptyTrack();
    const latestWrong = asIdList(input.wrongIds);
    const mergedWrong = [...latestWrong];

    for (const id of previous.wrongIds) {
        if (!mergedWrong.includes(id)) {
            mergedWrong.push(id);
        }
    }

    const weakCategories: string[] = [];
    const weakSubcategories: string[] = [];

    for (const [cat, val] of Object.entries(input.categoryScoreMap || {})) {
        if (!val || val.total <= 0) {
            continue;
        }

        if (val.correct / val.total < STRENGTH_RATIO) {
            weakCategories.push(cat);
        }

        for (const [sub, subVal] of Object.entries(val.subcats || {})) {
            if (!subVal || subVal.total <= 0) {
                continue;
            }

            if (subVal.correct / subVal.total < STRENGTH_RATIO) {
                weakSubcategories.push(sub);
            }
        }
    }

    store[track] = {
        wrongIds: mergedWrong.slice(0, MAX_WRONG_IDS),
        weakCategories,
        weakSubcategories,
    };

    try {
        window.localStorage.setItem(
            GUEST_STUDY_BIAS_KEY,
            JSON.stringify(store),
        );
    } catch {
        // Private mode / quota: next pool simply stays unbiased.
    }
}

export function summarizeAttemptStrengths(
    map?: Record<string, CategoryScore> | null,
): { strengths: StrengthRow[]; weaknesses: StrengthRow[] } {
    const strengths: StrengthRow[] = [];
    const weaknesses: StrengthRow[] = [];

    if (!map) {
        return { strengths, weaknesses };
    }

    const push = (row: StrengthRow) => {
        if (row.total <= 0) {
            return;
        }

        if (row.correct / row.total >= STRENGTH_RATIO) {
            strengths.push(row);
        } else {
            weaknesses.push(row);
        }
    };

    for (const [cat, val] of Object.entries(map)) {
        push({
            kind: 'category',
            name: cat,
            correct: val.correct ?? 0,
            missed: Math.max(0, (val.total ?? 0) - (val.correct ?? 0)),
            total: val.total ?? 0,
        });

        for (const [sub, subVal] of Object.entries(val.subcats || {})) {
            push({
                kind: 'subcategory',
                name: sub,
                parent: cat,
                correct: subVal.correct ?? 0,
                missed: Math.max(0, (subVal.total ?? 0) - (subVal.correct ?? 0)),
                total: subVal.total ?? 0,
            });
        }
    }

    weaknesses.sort(
        (a, b) => b.missed - a.missed || a.name.localeCompare(b.name),
    );
    strengths.sort((a, b) => {
        const aPct = a.total > 0 ? a.correct / a.total : 0;
        const bPct = b.total > 0 ? b.correct / b.total : 0;

        return bPct - aPct || a.name.localeCompare(b.name);
    });

    return { strengths, weaknesses };
}
