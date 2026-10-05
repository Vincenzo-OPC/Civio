import {
    createEmptyCard,
    fsrs,
    generatorParameters,
    Rating,
    State
    
    
    
} from 'ts-fsrs';
import type {Card, Grade, RecordLogItem} from 'ts-fsrs';

export type ReviewRating = 'again' | 'hard' | 'good' | 'easy';

export type CivioCard = {
    /** Opaque scheduler state (ts-fsrs Card JSON). */
    card: Card;
    /** Due instant (ISO). */
    due: string;
    state: 'new' | 'learning' | 'review' | 'relearning';
};

const ratingMap: Record<ReviewRating, Grade> = {
    again: Rating.Again,
    hard: Rating.Hard,
    good: Rating.Good,
    easy: Rating.Easy,
};

const stateMap: Record<State, CivioCard['state']> = {
    [State.New]: 'new',
    [State.Learning]: 'learning',
    [State.Review]: 'review',
    [State.Relearning]: 'relearning',
};

function toCivioCard(card: Card): CivioCard {
    return {
        card,
        due: card.due.toISOString(),
        state: stateMap[card.state] ?? 'new',
    };
}

/** Create a new FSRS card (not yet reviewed). */
export function initCard(now: Date = new Date()): CivioCard {
    return toCivioCard(createEmptyCard(now));
}

/**
 * Schedule the next review after a rating.
 * Pure aside from the provided `now` clock — safe for unit tests.
 */
export function scheduleAfterAnswer(
    current: CivioCard,
    rating: ReviewRating,
    now: Date = new Date(),
): { next: CivioCard; log: RecordLogItem } {
    const scheduler = fsrs(
        generatorParameters({
            enable_fuzz: false,
            enable_short_term: true,
        }),
    );
    const result = scheduler.next(current.card, now, ratingMap[rating]);

    return {
        next: toCivioCard(result.card),
        log: result,
    };
}

export function previewRatings(
    current: CivioCard,
    now: Date = new Date(),
): Record<ReviewRating, CivioCard> {
    const scheduler = fsrs(
        generatorParameters({
            enable_fuzz: false,
            enable_short_term: true,
        }),
    );
    const repeat = scheduler.repeat(current.card, now);

    return {
        again: toCivioCard(repeat[Rating.Again].card),
        hard: toCivioCard(repeat[Rating.Hard].card),
        good: toCivioCard(repeat[Rating.Good].card),
        easy: toCivioCard(repeat[Rating.Easy].card),
    };
}

export { Rating, State };
