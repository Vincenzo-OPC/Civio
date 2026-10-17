/**
 * Visual state of one choice. Correctness is never shown before Reveal,
 * and never during a Strict Mock.
 */
export type AnswerVisual =
    | 'unanswered'
    | 'selected'
    | 'correct'
    | 'correct-unselected'
    | 'incorrect';

export function answerOptionVisual(input: {
    optionIndex: number;
    selectedIndex: number | null | undefined;
    revealed: boolean;
    strict: boolean;
    correctIndex: number | null | undefined;
}): { visual: AnswerVisual; status: string | null } {
    const selected = input.selectedIndex === input.optionIndex;
    const showKey =
        input.revealed &&
        !input.strict &&
        typeof input.correctIndex === 'number';

    if (showKey && input.optionIndex === input.correctIndex && selected) {
        return { visual: 'correct', status: 'Your answer · Correct' };
    }

    if (showKey && input.optionIndex === input.correctIndex) {
        return { visual: 'correct-unselected', status: 'Correct answer' };
    }

    if (showKey && selected) {
        return { visual: 'incorrect', status: 'Your answer · Incorrect' };
    }

    if (selected) {
        return { visual: 'selected', status: 'Selected' };
    }

    return { visual: 'unanswered', status: null };
}

/** Study Mock and drills can pause. A Strict Mock cannot. */
export function canPauseExam(
    isDrill: boolean,
    mode: 'study' | 'strict',
): boolean {
    return isDrill || mode === 'study';
}

/**
 * A restored session does not start the clock by itself.
 * An already-expired timed session is left running so auto-submit can fire.
 */
export function recoveredSessionStartsPaused(
    isTimed: boolean,
    timeLeft: number,
): boolean {
    return !(isTimed && timeLeft <= 0);
}

export function shouldRunExamClock(input: {
    isExamActive: boolean;
    isExamSubmitted: boolean;
    isPaused: boolean;
}): boolean {
    return input.isExamActive && !input.isExamSubmitted && !input.isPaused;
}
