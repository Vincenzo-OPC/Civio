type AnswerKey = { id: number; correct_option: number; explanation?: string };

/**
 * Merge the keys the server releases after submit into the review screen.
 * Loaded on demand so the exam chunk stays within budget; exam state listens
 * for the event and patches activeQuestions.
 */
export function publishAnswerKeys(
    keys: AnswerKey[],
    answers: Record<number, number>,
    target: Pick<Window, 'dispatchEvent'> | undefined = typeof window !==
    'undefined'
        ? window
        : undefined,
): void {
    const keyById = Object.fromEntries(
        keys.map((k) => [
            k.id,
            {
                correct_option: k.correct_option,
                explanation: k.explanation ?? '',
            },
        ]),
    );

    target?.dispatchEvent(
        new CustomEvent('civio:exam-answer-keys', {
            detail: { keys: keyById, answers },
        }),
    );
}
