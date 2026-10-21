<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Models\Question;
use App\Models\ReviewCard;
use App\Models\ReviewEvent;
use App\Models\ReviewHelp;
use App\Models\ReviewItem;
use Carbon\Carbon;
use Illuminate\Support\Collection;
use Throwable;

/**
 * Remembers a signed-in learner's wrong practice answers.
 * A Strict Mock writes nothing. Help counts only for the served batch or
 * Study Mock that showed the explanation, and only when that item is answered.
 * An independent result updates the FSRS card. An assisted result does not.
 */
final class ReviewMistakeRecorder
{
    public function __construct(
        private readonly FsrsScheduler $scheduler,
        private readonly FsrsRatingPolicy $policy,
    ) {}

    /**
     * @param  array<int|string, mixed>  $chosenByQuestionId
     * @param  Collection<int, Question>  $questions
     */
    public function record(
        ?int $userId,
        int $attemptId,
        bool $strict,
        array $chosenByQuestionId,
        Collection $questions,
        ?string $sessionHash = null,
    ): void {
        if ($userId === null || $strict || $questions->isEmpty()) {
            return;
        }

        $ids = $questions->map(fn (Question $question): int => (int) $question->id)->all();
        $helped = [];

        if ($sessionHash !== null) {
            $helped = array_flip(ReviewHelp::query()
                ->where('user_id', $userId)
                ->where('session_hash', $sessionHash)
                ->whereIn('question_id', $ids)
                ->pluck('question_id')
                ->map(fn ($id): int => (int) $id)
                ->all());
        }

        $answered = [];
        /** @var list<array{question: Question, correct: bool, assisted: bool}> $jobs */
        $jobs = [];

        foreach ($questions as $question) {
            if ((bool) ($question->subcategory?->category?->is_demographic ?? false)) {
                continue;
            }

            $questionId = (int) $question->id;
            $chosen = $chosenByQuestionId[$questionId] ?? $chosenByQuestionId[(string) $questionId] ?? null;

            if ($chosen === null || $chosen === '') {
                continue;
            }

            $answered[] = $questionId;
            $correct = (int) $chosen === (int) $question->correct_option;
            $assisted = isset($helped[$questionId]);
            $item = ReviewItem::query()
                ->where('user_id', $userId)
                ->where('question_id', $questionId)
                ->first();

            if ($item !== null && (int) $item->last_attempt_id === $attemptId) {
                continue;
            }

            if ($correct && $item === null) {
                continue;
            }

            if ($correct && $assisted) {
                $item?->forceFill([
                    'last_attempt_id' => $attemptId,
                    'last_result_at' => now(),
                ])->save();
                $jobs[] = ['question' => $question, 'correct' => true, 'assisted' => true];

                continue;
            }

            if ($correct) {
                $item->forceFill([
                    'status' => 'resolved',
                    'resolved_at' => now(),
                    'resolved_by_attempt_id' => $attemptId,
                    'last_attempt_id' => $attemptId,
                    'last_result_at' => now(),
                ])->save();
                $jobs[] = ['question' => $question, 'correct' => true, 'assisted' => false];

                continue;
            }

            if ($item === null) {
                ReviewItem::query()->create([
                    'user_id' => $userId,
                    'question_id' => $questionId,
                    'source_attempt_id' => $attemptId,
                    'first_wrong_at' => now(),
                    'last_result_at' => now(),
                    'wrong_count' => 1,
                    'status' => 'pending',
                    'last_attempt_id' => $attemptId,
                ]);
            } else {
                $item->forceFill([
                    'status' => 'pending',
                    'wrong_count' => $item->wrong_count + 1,
                    'resolved_at' => null,
                    'resolved_by_attempt_id' => null,
                    'last_attempt_id' => $attemptId,
                    'last_result_at' => now(),
                ])->save();
            }

            $jobs[] = ['question' => $question, 'correct' => false, 'assisted' => $assisted];
        }

        if ($sessionHash !== null && $answered !== []) {
            ReviewHelp::query()
                ->where('user_id', $userId)
                ->where('session_hash', $sessionHash)
                ->whereIn('question_id', $answered)
                ->delete();
        }

        $this->scheduleMany($userId, $attemptId, $jobs);
    }

    public function noteHelp(?int $userId, int $questionId, ?string $sessionHash): void
    {
        if ($userId === null || $sessionHash === null) {
            return;
        }

        ReviewHelp::query()->create([
            'user_id' => $userId,
            'question_id' => $questionId,
            'session_hash' => $sessionHash,
        ]);
    }

    /**
     * @param  list<array{question: Question, correct: bool, assisted: bool}>  $jobs
     */
    private function scheduleMany(int $userId, int $attemptId, array $jobs): void
    {
        if ($jobs === []) {
            return;
        }

        $already = array_flip(ReviewEvent::query()
            ->where('user_id', $userId)
            ->where('source_attempt_id', $attemptId)
            ->whereIn('question_id', array_map(fn (array $job): int => (int) $job['question']->id, $jobs))
            ->pluck('question_id')
            ->map(fn ($id): int => (int) $id)
            ->all());

        $jobs = array_values(array_filter(
            $jobs,
            fn (array $job): bool => ! isset($already[(int) $job['question']->id]),
        ));

        if ($jobs === []) {
            return;
        }

        $reviews = [];

        foreach ($jobs as $job) {
            $rating = $this->policy->rating($job['correct'], $job['assisted']);

            if ($rating === null) {
                continue;
            }

            $reviews[] = [
                'key' => (string) $job['question']->id,
                'card' => null,
                'rating' => $rating,
            ];
        }

        $cards = ReviewCard::query()
            ->where('user_id', $userId)
            ->whereIn('question_id', array_map(fn (array $job): int => (int) $job['question']->id, $jobs))
            ->lockForUpdate()
            ->get()
            ->keyBy(fn (ReviewCard $card): int => (int) $card->question_id);

        foreach ($reviews as $index => $review) {
            $existing = $cards->get((int) $review['key']);
            $reviews[$index]['card'] = is_array($existing?->card_state) ? $existing->card_state : null;
        }

        $scheduled = [];

        if ($reviews !== []) {
            try {
                $scheduled = $this->scheduler->applyMany($reviews, now());
            } catch (Throwable $exception) {
                report($exception);
            }
        }

        foreach ($jobs as $job) {
            $question = $job['question'];
            $questionId = (int) $question->id;
            $rating = $this->policy->rating($job['correct'], $job['assisted']);
            $card = $cards->get($questionId);
            $before = is_array($card?->card_state) ? $card->card_state : null;
            $next = $scheduled[(string) $questionId] ?? null;
            $applied = is_array($next) ? $rating : null;
            $due = $card?->due_at;

            if (is_array($next)) {
                $due = Carbon::parse($next['due'])->timezone(config('app.timezone'));
                $payload = [
                    'scheduler_version' => FsrsScheduler::VERSION,
                    'policy_version' => FsrsRatingPolicy::VERSION,
                    'card_state' => $next['card'],
                    'due_at' => $due,
                    'state' => (string) $next['state'],
                    'last_rating' => $rating,
                    'last_reviewed_at' => now(),
                    'reps' => (int) ($next['reps'] ?? 0),
                    'lapses' => (int) ($next['lapses'] ?? 0),
                    'question_fingerprint' => $this->fingerprint($question),
                ];

                if ($card === null) {
                    ReviewCard::query()->create([
                        'user_id' => $userId,
                        'question_id' => $questionId,
                        ...$payload,
                    ]);
                } else {
                    $card->forceFill($payload)->save();
                }
            }

            ReviewEvent::query()->create([
                'user_id' => $userId,
                'question_id' => $questionId,
                'source_attempt_id' => $attemptId,
                'outcome' => $this->outcome($job['correct'], $job['assisted']),
                'rating' => $applied,
                'assisted' => $job['assisted'],
                'scheduled' => $applied !== null,
                'due_at' => $due,
                'reviewed_at' => now(),
                'scheduler_version' => FsrsScheduler::VERSION,
                'policy_version' => FsrsRatingPolicy::VERSION,
                'card_before' => $before,
                'card_after' => is_array($next) ? $next['card'] : $before,
                'question_fingerprint' => $this->fingerprint($question),
            ]);
        }
    }

    private function outcome(bool $correct, bool $assisted): string
    {
        if (! $correct) {
            return 'incorrect';
        }

        return $assisted ? 'assisted_correct' : 'independent_correct';
    }

    private function fingerprint(Question $question): string
    {
        return hash('sha256', implode('|', [
            (string) $question->id,
            (string) $question->updated_at,
            (string) $question->correct_option,
            (string) $question->stem,
        ]));
    }
}
