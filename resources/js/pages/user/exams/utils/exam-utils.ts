import type { Question } from '../types';

export const EXAM_CONSTANTS = {
    PROFESSIONAL_TIME_LIMIT_SECS: 11400,
    SUBPROFESSIONAL_TIME_LIMIT_SECS: 9600,
    PROFESSIONAL_TOTAL_ITEMS: 150, // was 170; demographics omitted for mocks
    SUBPROFESSIONAL_TOTAL_ITEMS: 145, // was 165; demographics omitted for mocks
    PROFESSIONAL_SCORED_ITEMS: 150,
    SUBPROFESSIONAL_SCORED_ITEMS: 145,
    DEMOGRAPHIC_QUESTION_COUNT: 20,
    WRONG_PRIORITY_PERCENTAGE: 0.3,
    TIMER_RED_ZONE_SECS: 600,
    SHIELD_COOLDOWN_MS: 3000,
} as const;

export function isDemographicQuestion(q?: Partial<Question> | null): boolean {
    if (!q) {
        return false;
    }

    if (q.isDemographic) {
        return true;
    }

    if (!q.category) {
        return false;
    }

    const cat = q.category.toLowerCase();

    return cat === 'demographic profile' || cat.includes('demographic');
}

export function fisherYatesShuffle<T>(array: T[]): T[] {
    const result = [...array];

    for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [result[i], result[j]] = [result[j], result[i]];
    }

    return result;
}

export async function apiPost<T = any>(url: string, payload: any): Promise<T> {
    const csrfToken =
        typeof document !== 'undefined'
            ? (
                  document.querySelector(
                      'meta[name="csrf-token"]',
                  ) as HTMLMetaElement
              )?.content || ''
            : '';

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-CSRF-TOKEN': csrfToken,
        },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        throw new Error(
            `API request to ${url} failed with status ${res.status}`,
        );
    }

    return res.json();
}

const VARIANT_SUFFIX = /\s*\(variant\s+\d+\)\s*$/i;

/** Keep in sync with App\Support\QuestionStem. */
export function normalizeQuestionStem(stem: string | null | undefined): string {
    return (stem || '')
        .replace(VARIANT_SUFFIX, '')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
}

export function isVariantStem(stem: string | null | undefined): boolean {
    return VARIANT_SUFFIX.test(stem || '');
}

export function preferUniqueStems<T extends { stem?: string | null }>(
    pool: T[],
): T[] {
    const byStem = new Map<string, T>();

    for (const question of pool) {
        const key = normalizeQuestionStem(question.stem);

        if (!key) {
            continue;
        }

        const existing = byStem.get(key);

        if (!existing) {
            byStem.set(key, question);
            continue;
        }

        if (isVariantStem(existing.stem) && !isVariantStem(question.stem)) {
            byStem.set(key, question);
        }
    }

    return [...byStem.values()];
}
