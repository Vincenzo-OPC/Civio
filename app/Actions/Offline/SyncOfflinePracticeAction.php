<?php

declare(strict_types=1);

namespace App\Actions\Offline;

use App\Data\Offline\OfflineAnswer;
use App\Enums\QuestionStatus;
use App\Models\OfflinePracticeResult;
use App\Models\Question;

/**
 * Re-grades queued offline drill answers with server keys (Lite L2).
 *
 * - Only active, offline-eligible items are graded. Anything else is rejected
 *   as "not_offline" without saying whether the answer was right, so this
 *   endpoint can't be used to check answers to mock items.
 * - If the client's claimed key differs from the server key, the answer is
 *   rejected as "key_mismatch" (tampered or stale pack) and not counted.
 * - Idempotent per (owner, client_id): a re-sent answer returns the stored
 *   verdict and is never stored twice.
 * - Accepted answers are tagged source "offline_practice". Only these feed
 *   weak-topic stats (the returned `bias`).
 */
final class SyncOfflinePracticeAction
{
    public const NOT_OFFLINE = 'not_offline';

    public const KEY_MISMATCH = 'key_mismatch';

    public const INVALID_OPTION = 'invalid_option';

    /**
     * @param  list<OfflineAnswer>  $answers
     * @return array{results: list<array<string, mixed>>, bias: array{wrong_ids: list<int>, correct_ids: list<int>, category_scores: array<string, array{correct: int, total: int, subcats: array<string, array{correct: int, total: int}>}>}}
     */
    public function handle(string $ownerKey, ?int $userId, array $answers): array
    {
        $questions = Question::query()
            ->with('subcategory.category')
            ->whereIn('id', array_unique(array_map(fn (OfflineAnswer $a): int => $a->questionId, $answers)))
            ->get()
            ->keyBy('id');

        $existing = OfflinePracticeResult::query()
            ->where('owner_key', $ownerKey)
            ->whereIn('client_id', array_map(fn (OfflineAnswer $a): string => $a->clientId, $answers))
            ->get()
            ->keyBy('client_id');

        $results = [];
        $bias = ['wrong_ids' => [], 'correct_ids' => [], 'category_scores' => []];

        foreach ($answers as $answer) {
            /** @var OfflinePracticeResult|null $row */
            $row = $existing->get($answer->clientId);
            $duplicate = $row !== null;

            if ($row === null) {
                /** @var Question|null $question */
                $question = $questions->get($answer->questionId);
                [$status, $reason, $isCorrect] = self::grade($question, $answer);

                $row = OfflinePracticeResult::query()->createOrFirst(
                    ['owner_key' => $ownerKey, 'client_id' => $answer->clientId],
                    [
                        'user_id' => $userId,
                        'question_id' => $question?->id ?? null,
                        'selected_option' => $answer->selectedOption,
                        'claimed_correct_option' => $answer->claimedCorrectOption,
                        'is_correct' => $isCorrect,
                        'status' => $status,
                        'reason' => $reason,
                        'source' => OfflinePracticeResult::SOURCE,
                        'pack_version' => $answer->packVersion,
                        'answered_at' => $answer->answeredAt ?? now(),
                    ],
                );
                $duplicate = ! $row->wasRecentlyCreated;
            }

            $accepted = $row->status === OfflinePracticeResult::ACCEPTED;
            $result = [
                'client_id' => $answer->clientId,
                'question_id' => $answer->questionId,
                'status' => $row->status,
                'reason' => $row->reason,
                'duplicate' => $duplicate,
            ];

            if ($accepted) {
                $result['correct'] = (bool) $row->is_correct;
                self::addToBias($bias, $questions->get($row->question_id), (bool) $row->is_correct);
            }

            $results[] = $result;
        }

        $bias['wrong_ids'] = array_values(array_unique($bias['wrong_ids']));
        $bias['correct_ids'] = array_values(array_unique($bias['correct_ids']));

        return ['results' => $results, 'bias' => $bias];
    }

    /** @return array{0: string, 1: string|null, 2: bool} */
    private static function grade(?Question $question, OfflineAnswer $answer): array
    {
        if ($question === null || $question->status !== QuestionStatus::Active || ! $question->offline_eligible) {
            return [OfflinePracticeResult::REJECTED, self::NOT_OFFLINE, false];
        }

        if ($answer->selectedOption >= count((array) $question->options)) {
            return [OfflinePracticeResult::REJECTED, self::INVALID_OPTION, false];
        }

        if ($answer->claimedCorrectOption !== (int) $question->correct_option) {
            return [OfflinePracticeResult::REJECTED, self::KEY_MISMATCH, false];
        }

        return [OfflinePracticeResult::ACCEPTED, null, $answer->selectedOption === (int) $question->correct_option];
    }

    /** @param array{wrong_ids: list<int>, correct_ids: list<int>, category_scores: array<string, array{correct: int, total: int, subcats: array<string, array{correct: int, total: int}>}>} $bias */
    private static function addToBias(array &$bias, ?Question $question, bool $correct): void
    {
        if ($question === null) {
            return;
        }

        $bias[$correct ? 'correct_ids' : 'wrong_ids'][] = (int) $question->id;
        $category = (string) ($question->subcategory?->category?->name ?? 'Unknown');
        $sub = (string) ($question->subcategory?->name ?? 'Unknown');
        $bias['category_scores'][$category] ??= ['correct' => 0, 'total' => 0, 'subcats' => []];
        $bias['category_scores'][$category]['total']++;
        $bias['category_scores'][$category]['subcats'][$sub] ??= ['correct' => 0, 'total' => 0];
        $bias['category_scores'][$category]['subcats'][$sub]['total']++;

        if ($correct) {
            $bias['category_scores'][$category]['correct']++;
            $bias['category_scores'][$category]['subcats'][$sub]['correct']++;
        }
    }
}
