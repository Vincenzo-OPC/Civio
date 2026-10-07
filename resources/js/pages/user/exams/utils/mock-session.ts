import { readGuestStudyBias } from '@/lib/guest-study-bias';
import type { Question } from '../types';
import { apiPost } from './exam-utils';
import { mockLevelForExam, shuffleOptionsForQuestion } from './mock-pool';

/**
 * Lite L1: the server picks the mock (POST /exams/sessions) and sends only
 * those items, keys withheld. This browser's past misses and weak topics are
 * sent as hints so the server can lean the mock toward them; they only
 * reorder the pick and never unlock answers.
 */

export type MockSession = {
    sessionId: string;
    questions: Question[];
    notice: string | null;
};

type MockSessionResponse = {
    success: boolean;
    session_id: string;
    track: string;
    target: number;
    short: boolean;
    notice: string | null;
    questions: Question[];
};

export async function startMockSession(
    examId: number | null,
): Promise<MockSession> {
    const level = mockLevelForExam(examId);
    const bias = readGuestStudyBias()[level];

    const data = await apiPost<MockSessionResponse>('/exams/sessions', {
        track: level,
        bias: {
            wrong_ids: bias.wrongIds.slice(-2000),
            weak_subcategories: bias.weakSubcategories.slice(0, 100),
            weak_categories: bias.weakCategories.slice(0, 20),
        },
    });

    return {
        sessionId: data.session_id,
        questions: (data.questions ?? []).map(shuffleOptionsForQuestion),
        notice: data.notice ?? null,
    };
}
