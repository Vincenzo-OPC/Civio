/**
 * Exam Simulation modes.
 *
 * - Study Mode: Show Explanation, Copy Question, and the external assistant. The timer is optional.
 * - Exam Mode: exam rehearsal. The timer is always on and the server keeps
 *   every key locked until the mock is submitted (StrictMockLock).
 *
 * Drills are not mocks: they always keep their study tools.
 */
export type ExamMode = 'study' | 'strict';

export const EXAM_MODES: readonly ExamMode[] = ['study', 'strict'];

export const EXAM_MODE_LABELS: Record<ExamMode, string> = {
    study: 'Study Mode',
    strict: 'Exam Mode',
};

export function parseExamMode(value: unknown): ExamMode {
    return value === 'strict' ? 'strict' : 'study';
}

/** Strict forces the timer on; Study follows the learner's choice. */
export function isTimerOn(mode: ExamMode, studyTimed: boolean): boolean {
    return mode === 'strict' || studyTimed;
}

/** Reveal, Copy Question, and Ask show everywhere except a Strict Mock. */
export function showsStudyTools(mode: ExamMode, isDrill: boolean): boolean {
    return isDrill || mode === 'study';
}
