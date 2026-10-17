interface KeyedItem {
    readonly options: readonly string[];
    readonly correct_option?: number | null;
}

/** Fail closed for the entire booklet; never guess a missing key. */
export function pdfAnswerLetters(
    questions: readonly KeyedItem[],
): string[] | null {
    if (
        questions.length === 0 ||
        questions.some(
            (question) =>
                !Number.isInteger(question.correct_option) ||
                question.correct_option == null ||
                question.correct_option < 0 ||
                question.correct_option >= question.options.length,
        )
    ) {
        return null;
    }

    return questions.map((question) =>
        String.fromCharCode(65 + question.correct_option!),
    );
}
