import type { Question } from '../types';
import {
    EXAM_CONSTANTS,
    fisherYatesShuffle,
    isDemographicQuestion,
    shuffleHardBiased,
    stemDedupeKey,
} from './exam-utils';

/**
 * Pure mock-pool builder (no React), so it can be unit-tested.
 *
 * Unique items only: "(variant N)" clones are dropped up front, an item is
 * never used twice, and exact duplicates (same stem and options under another
 * ID) are skipped. There is no padding: if the bank is short for a category,
 * the mock is simply shorter and the caller shows the real count.
 */

const VARIANT_CLONE_RE = /\(variant\s*\d+\)/i;

/** Old seeder filler rows ("... (variant 3)"). Never real questions. */
export function isVariantClone(q: Pick<Question, 'stem'>): boolean {
    return VARIANT_CLONE_RE.test(q.stem || '');
}

/** Same stem and same options = the same item, whatever its ID. */
export function exactItemKey(q: Pick<Question, 'stem' | 'options'>): string {
    const stem = (q.stem || '').toLowerCase().replace(/\s+/g, ' ').trim();
    const options = (Array.isArray(q.options) ? q.options : [])
        .map((o) =>
            String(o ?? '')
                .toLowerCase()
                .replace(/\s+/g, ' ')
                .trim(),
        )
        .join('\u241f');

    return `${stem}\u241e${options}`;
}

export type MockLevel = 'Professional' | 'Subprofessional';

export interface MockBlueprintBlock {
    category: string;
    count: number;
    splitLanguage?: boolean;
}

export const MOCK_BLUEPRINT: Record<MockLevel, MockBlueprintBlock[]> = {
    Professional: [
        { category: 'Verbal Ability', count: 45, splitLanguage: true },
        { category: 'Analytical Ability', count: 52 },
        { category: 'Numerical Ability', count: 45 },
        { category: 'General Information', count: 8 },
    ],
    Subprofessional: [
        { category: 'Verbal Ability', count: 45, splitLanguage: true },
        { category: 'Clerical Ability', count: 47 },
        { category: 'Numerical Ability', count: 45 },
        { category: 'General Information', count: 8 },
    ],
};

export function mockLevelForExam(examId: number | null): MockLevel {
    return examId === 2 ? 'Subprofessional' : 'Professional';
}

export function mockTargetForExam(examId: number | null): number {
    return examId === 2
        ? EXAM_CONSTANTS.SUBPROFESSIONAL_SCORED_ITEMS
        : EXAM_CONSTANTS.PROFESSIONAL_SCORED_ITEMS;
}

/** Items a mock may draw from: no demographics, no clones, no exact duplicates. */
export function uniqueMockSource(questions: Question[]): Question[] {
    const seenIds = new Set<number>();
    const seenKeys = new Set<string>();
    const out: Question[] = [];

    for (const q of questions) {
        if (
            isDemographicQuestion(q) ||
            isVariantClone(q) ||
            seenIds.has(q.id)
        ) {
            continue;
        }

        const key = exactItemKey(q);

        if (seenKeys.has(key)) {
            continue;
        }

        seenIds.add(q.id);
        seenKeys.add(key);
        out.push(q);
    }

    return out;
}

export function shuffleOptionsForQuestion(q: Question): Question {
    let options = q.options;
    const hasKey = typeof q.correct_option === 'number';
    let correctOption = hasKey ? (q.correct_option as number) : 0;

    if (options.length > 5) {
        options = options.slice(0, 5);

        if (hasKey && correctOption >= 5) {
            correctOption = 0;
        }
    }

    const indices = options.map((_, i) => i);
    const shuffledIndices = fisherYatesShuffle(indices);

    const shuffledOptions = shuffledIndices.map((i) => options[i]);
    // When answer keys are withheld, omit remapped correct_option (Reveal uses /exams/reveal).
    const remapped: Question = {
        ...q,
        options: shuffledOptions,
        originalOptionIndices: shuffledIndices,
    };

    if (hasKey) {
        remapped.correct_option = shuffledIndices.indexOf(correctOption);
    } else {
        delete remapped.correct_option;
        delete remapped.explanation;
    }

    return remapped;
}

function quotasForSubcats(
    names: string[],
    groups: Record<string, Question[]>,
    targetCount: number,
    weakSubSet: Set<string>,
): Record<string, number> {
    const quotas: Record<string, number> = {};
    names.forEach((name) => {
        quotas[name] = 0;
    });

    const place = (bucket: string[], share: number): number => {
        if (bucket.length === 0 || share <= 0) {
            return 0;
        }

        let left = share;
        const base = Math.floor(share / bucket.length);
        let rem = share % bucket.length;

        for (const name of bucket) {
            const want = base + (rem > 0 ? 1 : 0);

            if (rem > 0) {
                rem--;
            }

            const give = Math.min(groups[name]?.length ?? 0, want);
            quotas[name] += give;
            left -= give;
        }

        if (left > 0) {
            for (const name of bucket) {
                if (left <= 0) {
                    break;
                }

                const room = (groups[name]?.length ?? 0) - quotas[name];
                const add = Math.min(Math.max(0, room), left);
                quotas[name] += add;
                left -= add;
            }
        }

        return share - left;
    };

    const weakNames = names.filter((name) => weakSubSet.has(name));
    const otherNames = names.filter((name) => !weakSubSet.has(name));

    if (weakNames.length > 0 && otherNames.length > 0) {
        const weakAvailable = weakNames.reduce(
            (sum, name) => sum + (groups[name]?.length ?? 0),
            0,
        );
        const weakShare = Math.min(
            weakAvailable,
            Math.round(targetCount * EXAM_CONSTANTS.WRONG_PRIORITY_PERCENTAGE),
        );
        const placedWeak = place(weakNames, weakShare);
        place(otherNames, Math.max(0, targetCount - placedWeak));
    } else {
        const baseQuota = Math.floor(targetCount / names.length);
        let remainder = targetCount % names.length;

        for (const name of names) {
            quotas[name] = baseQuota + (remainder > 0 ? 1 : 0);

            if (remainder > 0) {
                remainder--;
            }
        }
    }

    return quotas;
}

/**
 * About half the scored items should come from previously-weak categories
 * when unused items in those categories remain. Swaps only within the
 * level's categories and never brings in a duplicate.
 */
function raiseWeakCategoryShare(
    scoredPool: Question[],
    sourcePool: Question[],
    weakCategories: string[],
    targetCount: number,
    levelCategories: Set<string>,
): Question[] {
    if (weakCategories.length === 0 || scoredPool.length === 0) {
        return scoredPool;
    }

    const weakSet = new Set(
        weakCategories.filter((cat) => levelCategories.has(cat)),
    );

    if (weakSet.size === 0) {
        return scoredPool;
    }

    const isWeak = (q: Question) => weakSet.has(q.category || '');
    const weakTarget = Math.min(
        targetCount,
        Math.round(targetCount * EXAM_CONSTANTS.WRONG_PRIORITY_PERCENTAGE),
    );
    const result = [...scoredPool];
    let weakCount = result.filter(isWeak).length;

    if (weakCount >= weakTarget) {
        return result;
    }

    const usedIds = new Set(result.map((q) => q.id));
    const usedKeys = new Set(result.map(exactItemKey));
    const extras = fisherYatesShuffle(
        sourcePool.filter(
            (q) =>
                !usedIds.has(q.id) &&
                !usedKeys.has(exactItemKey(q)) &&
                isWeak(q),
        ),
    );
    let extraIdx = 0;

    for (
        let i = result.length - 1;
        i >= 0 && weakCount < weakTarget && extraIdx < extras.length;
        i--
    ) {
        if (!isWeak(result[i])) {
            result[i] = extras[extraIdx++];
            weakCount++;
        }
    }

    return result;
}

export interface MockPoolBias {
    seenIds?: number[];
    wrongIds?: number[];
    weakSubcategories?: string[];
    weakCategories?: string[];
}

export interface MockPoolResult {
    /** Scored items in final order (options not yet shuffled). */
    items: Question[];
    /** Official item count for the level (150 Professional, 145 Subprofessional). */
    target: number;
    /** True when the bank could not fill the official count. */
    short: boolean;
}

/**
 * Build the scored items for a full Professional (examId 1) or
 * Subprofessional (examId 2) mock from unique items only.
 */
export function buildMockScoredPool(
    questions: Question[],
    examId: number | null,
    bias: MockPoolBias = {},
): MockPoolResult {
    const level = mockLevelForExam(examId);
    const blueprint = MOCK_BLUEPRINT[level];
    const target = mockTargetForExam(examId);
    const sourcePool = uniqueMockSource(questions);

    const seenSet = new Set(bias.seenIds ?? []);
    const wrongSet = new Set(bias.wrongIds ?? []);
    const weakSubSet = new Set(bias.weakSubcategories ?? []);

    // Shared across the whole mock: an item (or an exact copy) appears once.
    const usedIds = new Set<number>();
    const usedKeys = new Set<string>();

    const isFree = (q: Question) =>
        !usedIds.has(q.id) && !usedKeys.has(exactItemKey(q));

    const pickFlat = (
        pool: Question[],
        count: number,
        fallbackPool: Question[] = [],
    ): Question[] => {
        const picked: Question[] = [];
        const prefixKeys = new Set<string>();

        if (count <= 0) {
            return picked;
        }

        const take = (q: Question) => {
            picked.push(q);
            usedIds.add(q.id);
            usedKeys.add(exactItemKey(q));
            const prefix = stemDedupeKey(q.stem || '');

            if (prefix) {
                prefixKeys.add(prefix);
            }
        };

        /**
         * spreadStems = true: also skip items whose stem opens like one
         * already picked here (variety first). The top-up pass relaxes that
         * to "distinct items only", since real items can share an opening
         * such as "Choose the correctly spelled word:".
         */
        const pushWithLimit = (
            items: Question[],
            quota: number,
            spreadStems: boolean,
        ) => {
            let added = 0;

            for (const q of items) {
                if (added >= quota || picked.length >= count) {
                    break;
                }

                if (!isFree(q)) {
                    continue;
                }

                if (spreadStems) {
                    const prefix = stemDedupeKey(q.stem || '');

                    if (prefix && prefixKeys.has(prefix)) {
                        continue;
                    }
                }

                take(q);
                added++;
            }
        };

        const wrongFromSeen = pool.filter((q) => wrongSet.has(q.id));
        const unseen = pool.filter((q) => !seenSet.has(q.id));
        const seenCorrect = pool.filter(
            (q) => seenSet.has(q.id) && !wrongSet.has(q.id),
        );
        const wrongQuota = Math.ceil(
            count * EXAM_CONSTANTS.WRONG_PRIORITY_PERCENTAGE,
        );
        const wrongOrdered = shuffleHardBiased(
            fisherYatesShuffle(wrongFromSeen),
        );

        // Variety pass: wrong first (weak-topic bias), then unseen, then seen.
        pushWithLimit(wrongOrdered, wrongQuota, true);
        pushWithLimit(shuffleHardBiased(unseen), count, true);
        pushWithLimit(shuffleHardBiased(seenCorrect), count, true);
        pushWithLimit(wrongOrdered, count, true);
        pushWithLimit(shuffleHardBiased(fallbackPool), count, true);

        // Top-up pass: any remaining distinct item. Still no clones or copies.
        pushWithLimit(
            shuffleHardBiased([...unseen, ...wrongOrdered, ...seenCorrect]),
            count,
            false,
        );
        pushWithLimit(shuffleHardBiased(fallbackPool), count, false);

        return picked;
    };

    const pickBalanced = (
        pool: Question[],
        targetCount: number,
        splitLanguage = false,
    ): Question[] => {
        const groups: Record<string, Question[]> = {};
        pool.forEach((q) => {
            const key = q.subcategory || 'General';

            if (!groups[key]) {
                groups[key] = [];
            }

            groups[key].push(q);
        });

        const subcatNames = fisherYatesShuffle(Object.keys(groups));

        if (subcatNames.length === 0) {
            return [];
        }

        const quotas = quotasForSubcats(
            subcatNames,
            groups,
            targetCount,
            weakSubSet,
        );
        const picked: Question[] = [];

        for (const subName of subcatNames) {
            const quota = quotas[subName] ?? 0;

            if (quota <= 0) {
                continue;
            }

            const subPool = groups[subName];

            if (splitLanguage || subName === 'Word analogy') {
                const engPool = subPool.filter((q) => {
                    const lang = (q.language || '').toLowerCase();

                    return lang === 'english' || lang === '' || lang === 'en';
                });
                const filPool = subPool.filter((q) => {
                    const lang = (q.language || '').toLowerCase();

                    return (
                        lang.includes('filipino') || lang.includes('tagalog')
                    );
                });
                const filQuota =
                    filPool.length > 0
                        ? Math.min(Math.floor(quota / 2), filPool.length)
                        : 0;

                picked.push(...pickFlat(filPool, filQuota));
                picked.push(...pickFlat(engPool, quota - filQuota, subPool));
            } else {
                picked.push(...pickFlat(subPool, quota));
            }
        }

        // Subcategory split left a gap: top up from the same category only.
        if (picked.length < targetCount) {
            picked.push(...pickFlat(pool, targetCount - picked.length));
        }

        return fisherYatesShuffle(picked.slice(0, targetCount));
    };

    const scored: Question[] = [];

    for (const block of blueprint) {
        const categoryPool = sourcePool.filter(
            (q) => q.category === block.category,
        );
        scored.push(
            ...pickBalanced(categoryPool, block.count, block.splitLanguage),
        );
    }

    const levelCategories = new Set(blueprint.map((b) => b.category));
    const biased = raiseWeakCategoryShare(
        scored,
        sourcePool,
        bias.weakCategories ?? [],
        target,
        levelCategories,
    );
    const items = fisherYatesShuffle(biased);

    return { items, target, short: items.length < target };
}

/**
 * User-facing note for a mock that could not reach the official count.
 * Returns null when the mock is full (or the session is not a full mock).
 */
export function shortMockNotice(
    examId: number | null,
    itemCount: number,
): string | null {
    if (examId !== 1 && examId !== 2) {
        return null;
    }

    const target = mockTargetForExam(examId);

    if (itemCount >= target) {
        return null;
    }

    const level = mockLevelForExam(examId);

    if (itemCount <= 0) {
        return `No ${level} practice items are available right now, so a mock can't start.`;
    }

    return `This ${level} mock has ${itemCount} items, not ${target}. The question bank only has ${itemCount} unique items for it right now, and repeats are not used to pad it.`;
}
