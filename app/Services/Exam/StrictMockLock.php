<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Enums\ExamMode;
use App\Models\ExamSession;
use Illuminate\Contracts\Session\Session;
use Illuminate\Database\Eloquent\Builder;

/**
 * Server-side answer lock for Strict Mocks.
 *
 * While a learner (signed in, or a guest's browser session) has an open
 * Strict session, the keys and explanations of its items are withheld by
 * every endpoint that could return them: Reveal, Expound, drill payloads,
 * scorecards of older attempts and grading of any other attempt. Submitting
 * the Strict Mock closes the session and lifts the lock.
 *
 * A session nobody submits stops locking once its time limit plus a grace
 * period has passed, so an abandoned mock cannot lock items forever.
 */
final class StrictMockLock
{
    public const GRACE_SECS = 600;

    public const MESSAGE = 'Answers stay hidden until you submit your Strict Mock.';

    /**
     * Item IDs locked for this learner right now.
     *
     * @return array<int, int>
     */
    public function lockedQuestionIds(?int $userId, ?Session $session, ?string $exceptSessionId = null): array
    {
        $guestIds = $session !== null
            ? array_values(array_filter((array) $session->get(ExamSession::GUEST_SESSION_KEY, []), 'is_string'))
            : [];

        if ($userId === null && $guestIds === []) {
            return [];
        }

        $oldest = now()->subSeconds(max(MockPoolSelector::TIME_LIMIT_SECS) + self::GRACE_SECS);

        $sessions = ExamSession::query()
            ->where('mode', ExamMode::Strict->value)
            ->whereNull('exam_attempt_id')
            ->where('created_at', '>=', $oldest)
            ->where(function (Builder $query) use ($userId, $guestIds): void {
                if ($userId !== null) {
                    $query->orWhere('user_id', $userId);
                }

                if ($guestIds !== []) {
                    $query->orWhere(fn (Builder $guest) => $guest->whereNull('user_id')->whereIn('id', $guestIds));
                }
            })
            ->when($exceptSessionId !== null, fn (Builder $query) => $query->where('id', '!=', $exceptSessionId))
            ->get(['id', 'track', 'question_ids', 'created_at']);

        $locked = [];

        foreach ($sessions as $examSession) {
            if (! $this->stillRunning($examSession)) {
                continue;
            }

            foreach ((array) $examSession->question_ids as $id) {
                $locked[(int) $id] = (int) $id;
            }
        }

        return array_values($locked);
    }

    public function isLocked(int $questionId, ?int $userId, ?Session $session): bool
    {
        return in_array($questionId, $this->lockedQuestionIds($userId, $session), true);
    }

    /**
     * Remove keys and explanations of locked items from question payloads.
     *
     * @param  array<int, array<string, mixed>>  $questions
     * @param  array<int, int>  $lockedIds
     * @return array<int, array<string, mixed>>
     */
    public static function withholdKeys(array $questions, array $lockedIds): array
    {
        if ($lockedIds === []) {
            return $questions;
        }

        $locked = array_flip($lockedIds);

        return array_map(function (array $question) use ($locked): array {
            if (isset($locked[(int) ($question['id'] ?? 0)])) {
                unset($question['correct_option'], $question['explanation']);
                $question['keyLocked'] = true;
            }

            return $question;
        }, $questions);
    }

    private function stillRunning(ExamSession $examSession): bool
    {
        $limit = MockPoolSelector::timeLimitFor(MockPoolSelector::levelFor($examSession->track));

        return $examSession->created_at !== null
            && $examSession->created_at->greaterThanOrEqualTo(now()->subSeconds($limit + self::GRACE_SECS));
    }
}
