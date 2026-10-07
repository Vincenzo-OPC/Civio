import type { Question } from '../types';
import { EXAM_CONSTANTS, fisherYatesShuffle } from './exam-utils';

/**
 * Client helpers for mocks. Lite L1 moved item selection to the server
 * (`App\Services\Exam\MockPoolSelector`, POST /exams/sessions): unique items
 * only, blueprint quotas, weak-topic bias, no clones and no padding. The
 * client only shuffles options (keeping `originalOptionIndices`) and words the
 * short-mock notice.
 */

export type MockLevel = 'Professional' | 'Subprofessional';

export function mockLevelForExam(examId: number | null): MockLevel {
    return examId === 2 ? 'Subprofessional' : 'Professional';
}

export function mockTargetForExam(examId: number | null): number {
    return examId === 2
        ? EXAM_CONSTANTS.SUBPROFESSIONAL_SCORED_ITEMS
        : EXAM_CONSTANTS.PROFESSIONAL_SCORED_ITEMS;
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
