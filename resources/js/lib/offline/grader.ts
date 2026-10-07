/**
 * Lite L2 offline drills: build a session from a downloaded pack and grade it
 * on the device. Pure. The server re-grades every answer on sync; nothing
 * graded here counts until then.
 */
import type { CategoryScore, Question } from '@/pages/user/exams/types';
import type { OfflinePackItem } from './types';

export type RandomSource = () => number;

/** Fisher-Yates with an injectable random source (tests pass a seeded one). */
export function shuffle<T>(values: readonly T[], random: RandomSource): T[] {
    const out = [...values];

    for (let i = out.length - 1; i > 0; i--) {
        const j = Math.floor(random() * (i + 1));
        [out[i], out[j]] = [out[j] as T, out[i] as T];
    }

    return out;
}

/** Display copy of an item with shuffled options; keys stay out of `Question`. */
export function toDisplayQuestion(
    item: OfflinePackItem,
    random: RandomSource,
): Question {
    const order = shuffle(
        item.options.map((_, index) => index),
        random,
    );

    return {
        id: item.id,
        stem: item.stem,
        options: order.map((index) => item.options[index] ?? ''),
        originalOptionIndices: order,
        category: item.category,
        subcategory: item.subcategory,
        language: item.language,
    };
}

/** Pick `count` items (or all) in random order and shuffle their options. */
export function buildOfflineSession(
    items: readonly OfflinePackItem[],
    count: number | 'all',
    random: RandomSource,
): { items: OfflinePackItem[]; questions: Question[] } {
    const picked = shuffle(items, random).slice(
        0,
        count === 'all' ? items.length : Math.max(0, count),
    );

    return {
        items: picked,
        questions: picked.map((item) => toDisplayQuestion(item, random)),
    };
}

export function toOriginalIndex(
    question: Pick<Question, 'originalOptionIndices'>,
    displayIndex: number,
): number {
    return question.originalOptionIndices?.[displayIndex] ?? displayIndex;
}

export function correctDisplayIndex(
    question: Pick<Question, 'originalOptionIndices'>,
    item: Pick<OfflinePackItem, 'correct_option'>,
): number {
    const order = question.originalOptionIndices ?? [];
    const index = order.indexOf(item.correct_option);

    return index === -1 ? item.correct_option : index;
}

export function isCorrectLocally(
    item: Pick<OfflinePackItem, 'correct_option'>,
    originalSelected: number,
): boolean {
    return item.correct_option === originalSelected;
}

export interface LocalScore {
    correct: number;
    answered: number;
    total: number;
    categoryScoreMap: Record<string, CategoryScore>;
}

/** Score a finished session. `answers` maps item position to display index. */
export function scoreOfflineSession(
    items: readonly OfflinePackItem[],
    questions: readonly Question[],
    answers: Readonly<Record<number, number>>,
): LocalScore {
    const categoryScoreMap: Record<string, CategoryScore> = {};
    let correct = 0;
    let answered = 0;

    items.forEach((item, index) => {
        const question = questions[index];
        const display = answers[index];
        const category = (categoryScoreMap[item.category] ??= {
            correct: 0,
            total: 0,
            subcats: {},
        });
        const sub = (category.subcats[item.subcategory] ??= {
            correct: 0,
            total: 0,
        });

        category.total++;
        sub.total++;

        if (display === undefined || !question) {
            return;
        }

        answered++;

        if (isCorrectLocally(item, toOriginalIndex(question, display))) {
            correct++;
            category.correct++;
            sub.correct++;
        }
    });

    return { correct, answered, total: items.length, categoryScoreMap };
}
