<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Models\Question;
use App\Models\ReviewHelp;
use App\Models\ReviewItem;
use Illuminate\Contracts\Session\Session;
use Illuminate\Support\Collection;

/**
 * Remembers a signed-in learner's wrong practice answers.
 * A Strict Mock writes nothing. Help counts only inside the browser session
 * that saw the explanation, and only for an answer that was actually submitted.
 */
final class ReviewMistakeRecorder
{
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

                continue;
            }

            $item->forceFill([
                'status' => 'pending',
                'wrong_count' => $item->wrong_count + 1,
                'resolved_at' => null,
                'resolved_by_attempt_id' => null,
                'last_attempt_id' => $attemptId,
                'last_result_at' => now(),
            ])->save();
        }

        if ($sessionHash !== null && $answered !== []) {
            ReviewHelp::query()
                ->where('user_id', $userId)
                ->where('session_hash', $sessionHash)
                ->whereIn('question_id', $answered)
                ->delete();
        }
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

    /** Stable for one signed-in sitting, including a rotated cookie. */
    public function sittingHash(?Session $session): ?string
    {
        if ($session === null) {
            return null;
        }

        $token = $session->get('civio_review_sitting');

        if (! is_string($token) || strlen($token) < 16) {
            $token = bin2hex(random_bytes(16));
            $session->put('civio_review_sitting', $token);
        }

        return hash('sha256', $token);
    }
}
