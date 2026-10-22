/**
 * Server-side FSRS step. PHP passes JSON on stdin and reads JSON on stdout.
 * The browser never supplies the next due date.
 *
 * Same parameters as resources/js/lib/review/fsrs.ts:
 * ts-fsrs 5.4.2, fuzz off, short-term steps on.
 */
import { createEmptyCard, fsrs, generatorParameters, Rating } from 'ts-fsrs';

const ratings = {
    again: Rating.Again,
    hard: Rating.Hard,
    good: Rating.Good,
    easy: Rating.Easy,
};

const states = ['new', 'learning', 'review', 'relearning'];

function revive(card) {
    if (!card || typeof card !== 'object') {
        return null;
    }

    return {
        ...card,
        due: new Date(card.due),
        last_review: card.last_review ? new Date(card.last_review) : undefined,
        state: Number(card.state),
    };
}

function serialize(card) {
    return {
        due: card.due.toISOString(),
        stability: card.stability,
        difficulty: card.difficulty,
        elapsed_days: card.elapsed_days,
        scheduled_days: card.scheduled_days,
        learning_steps: card.learning_steps,
        reps: card.reps,
        lapses: card.lapses,
        state: card.state,
        last_review: card.last_review
            ? new Date(card.last_review).toISOString()
            : null,
    };
}

const raw = await new Promise((resolve, reject) => {
    const chunks = [];
    process.stdin.on('data', (chunk) => chunks.push(chunk));
    process.stdin.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    process.stdin.on('error', reject);
});

const input = JSON.parse(raw || '{}');
const now = new Date(input.now);

if (Number.isNaN(now.getTime())) {
    process.stderr.write('FSRS now is not a time.\n');
    process.exit(2);
}

const scheduler = fsrs(
    generatorParameters({
        enable_fuzz: false,
        enable_short_term: true,
    }),
);

const reviews = Array.isArray(input.reviews) ? input.reviews : [];
const results = [];

for (const review of reviews) {
    const rating = ratings[review.rating];

    if (rating === undefined) {
        process.stderr.write('FSRS rating is not allowed.\n');
        process.exit(2);
    }

    const current = revive(review.card) ?? createEmptyCard(now);
    const next = scheduler.next(current, now, rating);
    const card = serialize(next.card);

    results.push({
        key: String(review.key),
        card,
        due: card.due,
        state: states[next.card.state] ?? 'new',
        stability: card.stability,
        difficulty: card.difficulty,
        reps: card.reps,
        lapses: card.lapses,
        scheduled_days: card.scheduled_days,
    });
}

process.stdout.write(
    JSON.stringify({
        scheduler: 'ts-fsrs@5.4.2',
        parameters: { enable_fuzz: false, enable_short_term: true },
        results,
    }),
);
