export const REVIEW_MISTAKES_LABEL = 'Review Mistakes';

export const REVIEW_MISTAKES_NOTE =
    'Civio reminds you to practice a question again before you forget it. A correct answer without an explanation clears the mistake. One clear does not finish the question.';

export const REVIEW_DUE_LABEL = 'Due Today';
export const REVIEW_UPCOMING_LABEL = 'Upcoming Reviews';
export const REVIEW_NEEDS_LABEL = 'Needs Review';
export const REVIEW_COMPLETE_LABEL = 'Review Complete';
export const REVIEW_EMPTY_LABEL = 'No mistakes to review yet.';
export const REVIEW_REMINDER_FAILED =
    'Your answer was saved. The next reminder was not. Try again.';
export const REVIEW_REMINDER_RETRY = 'Save the reminder';

export function reviewMistakesCopy(): {
    title: string;
    note: string;
    due: string;
    upcoming: string;
    needs: string;
    complete: string;
    empty: string;
    reminderFailed: string;
    reminderRetry: string;
} {
    return {
        title: REVIEW_MISTAKES_LABEL,
        note: REVIEW_MISTAKES_NOTE,
        due: REVIEW_DUE_LABEL,
        upcoming: REVIEW_UPCOMING_LABEL,
        needs: REVIEW_NEEDS_LABEL,
        complete: REVIEW_COMPLETE_LABEL,
        empty: REVIEW_EMPTY_LABEL,
        reminderFailed: REVIEW_REMINDER_FAILED,
        reminderRetry: REVIEW_REMINDER_RETRY,
    };
}
