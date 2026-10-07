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

export type StudyBiasInput = {
    /** Missed this attempt (wrong or unanswered), from server grading. */
    wrongIds: number[];
    /** Answered correctly this attempt — dropped from the retry list. */
    correctIds?: number[];
    categoryScoreMap: Record<string, CategoryScore>;
};

/**
 * Pure merge of one graded attempt into a track's bias.
 *
 * - New misses go to the front of the retry list; items now answered
 *   correctly drop out, so the tutor loop closes once a miss is fixed.
 * - Categories / subcategories scored this attempt are re-judged (< 80% is
 *   weak). Ones not covered this attempt keep their previous status, so a
 *   one-category drill does not wipe the other weak areas.
 */
export function mergeTrackBias(
    previous: TrackBias | undefined,
    input: StudyBiasInput,
): TrackBias {
    const prev = previous ?? emptyTrack();
    const correct = new Set(asIdList(input.correctIds ?? []));
    const mergedWrong: number[] = [];

    for (const id of [...asIdList(input.wrongIds), ...prev.wrongIds]) {
        if (!correct.has(id) && !mergedWrong.includes(id)) {
            mergedWrong.push(id);
        }
    }

    const judgedCategories = new Set<string>();
    const judgedSubcategories = new Set<string>();
    const weakCategories: string[] = [];
    const weakSubcategories: string[] = [];

    for (const [cat, val] of Object.entries(input.categoryScoreMap || {})) {
        if (!val || val.total <= 0) {
            continue;
        }

        judgedCategories.add(cat);

        if (val.correct / val.total < STRENGTH_RATIO) {
            weakCategories.push(cat);
        }

        for (const [sub, subVal] of Object.entries(val.subcats || {})) {
            if (!subVal || subVal.total <= 0) {
                continue;
            }

            judgedSubcategories.add(sub);

            if (subVal.correct / subVal.total < STRENGTH_RATIO) {
                weakSubcategories.push(sub);
            }
        }
    }

    for (const cat of prev.weakCategories) {
        if (!judgedCategories.has(cat) && !weakCategories.includes(cat)) {
            weakCategories.push(cat);
        }
    }

    for (const sub of prev.weakSubcategories) {
        if (!judgedSubcategories.has(sub) && !weakSubcategories.includes(sub)) {
            weakSubcategories.push(sub);
        }
    }

    return {
        wrongIds: mergedWrong.slice(0, MAX_WRONG_IDS),
        weakCategories,
        weakSubcategories,
    };
}

export function recordGuestStudyBias(
    track: StudyTrack,
    input: StudyBiasInput,
): void {
    if (typeof window === 'undefined') {
        return;
    }

    const store = readGuestStudyBias();
    store[track] = mergeTrackBias(store[track], input);

    try {
        window.localStorage.setItem(
            GUEST_STUDY_BIAS_KEY,
            JSON.stringify(store),
        );
    } catch {
        // Private mode / quota: next pool simply stays unbiased.
    }
}

export function studyTrackForExam(examId: number | null): StudyTrack {
    if (examId === 1) {
        return 'Professional';
    }

    if (examId === 2) {
        return 'Subprofessional';
    }

    return 'Drill';
}

type ServerGradeResponse = {
    success?: boolean;
    cat_scores?: {
        categoryScoreMap?: Record<string, CategoryScore>;
        metadata?: { wrong_question_ids?: unknown };
    };
    answer_keys?: Array<{ id: number; correct_option: number }>;
    answers?: Record<string, number | null>;
};

/**
 * Build the bias input from the server's grading response
 * (POST /exams/attempts). Returns null when the server did not grade, so the
 * client never guesses misses while answer keys are withheld.
 */
export function studyBiasInputFromServer(
    data: ServerGradeResponse | null | undefined,
): StudyBiasInput | null {
    const map = data?.cat_scores?.categoryScoreMap;

    if (!data?.success || !map || typeof map !== 'object') {
        return null;
    }

    const answers = data.answers ?? {};
    const keys = Array.isArray(data.answer_keys) ? data.answer_keys : [];
    const correctIds: number[] = [];
    const derivedWrong: number[] = [];

    for (const key of keys) {
        const chosen = answers[String(key.id)];

        if (chosen === undefined || chosen === null) {
            derivedWrong.push(key.id);
        } else if (Number(chosen) === Number(key.correct_option)) {
            correctIds.push(key.id);
        } else {
            derivedWrong.push(key.id);
        }
    }

    const serverWrong = data.cat_scores?.metadata?.wrong_question_ids;

    return {
        // Prefer the server list (it already skips demographic items).
        wrongIds: Array.isArray(serverWrong)
            ? asIdList(serverWrong)
            : derivedWrong,
        correctIds,
        categoryScoreMap: map,
    };
}

/** Union of every track's bias — drills learn from mocks and vice versa. */
export function combinedStudyBias(
    store: Record<StudyTrack, TrackBias> = readGuestStudyBias(),
): TrackBias {
    const out = emptyTrack();

    for (const track of TRACKS) {
        const row = store[track] ?? emptyTrack();

        for (const id of row.wrongIds) {
            if (!out.wrongIds.includes(id)) {
                out.wrongIds.push(id);
            }
        }

        for (const cat of row.weakCategories) {
            if (!out.weakCategories.includes(cat)) {
                out.weakCategories.push(cat);
            }
        }

        for (const sub of row.weakSubcategories) {
            if (!out.weakSubcategories.includes(sub)) {
                out.weakSubcategories.push(sub);
            }
        }
    }

    return out;
}

/** Share of a drill reserved for past misses and weak topics. */
export const DRILL_WEAK_SHARE = 0.5;

type BiasItem = { id: number; category?: string; subcategory?: string };

function defaultShuffle<T>(items: T[]): T[] {
    const arr = [...items];

    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }

    return arr;
}

/**
 * Pick `count` items for a practice drill, biased toward the learner's weak
 * spots: up to half the drill comes from past misses first, then weak
 * subcategories / categories, and the rest from the remaining pool so the
 * drill still covers new ground. Final order is shuffled.
 */
export function pickDrillItemsWithBias<T extends BiasItem>(
    pool: T[],
    bias: TrackBias,
    count: number,
    shuffle: <U>(items: U[]) => U[] = defaultShuffle,
): T[] {
    const target = Math.max(0, Math.min(Math.floor(count), pool.length));

    if (target === 0) {
        return [];
    }

    const wrong = new Set(bias.wrongIds);
    const weakSubs = new Set(bias.weakSubcategories);
    const weakCats = new Set(bias.weakCategories);

    const missed = shuffle(pool.filter((q) => wrong.has(q.id)));
    const weakTopic = shuffle(
        pool.filter(
            (q) =>
                !wrong.has(q.id) &&
                (weakSubs.has(q.subcategory ?? '') ||
                    weakCats.has(q.category ?? '')),
        ),
    );
    const rest = shuffle(
        pool.filter(
            (q) =>
                !wrong.has(q.id) &&
                !weakSubs.has(q.subcategory ?? '') &&
                !weakCats.has(q.category ?? ''),
        ),
    );

    const priority = [...missed, ...weakTopic];
    const weakQuota = Math.min(
        priority.length,
        Math.ceil(target * DRILL_WEAK_SHARE),
    );
    const picked = priority.slice(0, weakQuota);

    for (const q of rest) {
        if (picked.length >= target) {
            break;
        }

        picked.push(q);
    }

    for (const q of priority.slice(weakQuota)) {
        if (picked.length >= target) {
            break;
        }

        picked.push(q);
    }

    return shuffle(picked);
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
                missed: Math.max(
                    0,
                    (subVal.total ?? 0) - (subVal.correct ?? 0),
                ),
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
