export const REVIEW_MISTAKES_LABEL = 'Review Mistakes';

export const REVIEW_MISTAKES_NOTE =
    'This is practice history. A later correct answer, given without an explanation, clears the item.';

export function reviewMistakesCopy(): { title: string; note: string } {
    return {
        title: REVIEW_MISTAKES_LABEL,
        note: REVIEW_MISTAKES_NOTE,
    };
}
