/**
 * Scorecard note for items withdrawn after the mock was served. They are not
 * counted as wrong or skipped, and the score is out of the remaining items.
 */
export function retiredNotice(
    retired: number | undefined,
    scored: number,
): string | null {
    if (!retired || retired < 1) {
        return null;
    }

    const items = retired === 1 ? '1 item was' : `${retired} items were`;

    return `${items} withdrawn by Civio after this mock started. ${retired === 1 ? 'It is' : 'They are'} not counted as wrong or skipped: your score is out of ${scored}, not ${scored + retired}.`;
}
