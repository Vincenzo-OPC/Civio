<?php

declare(strict_types=1);

namespace App\Services\Learning;

use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\OfflinePracticeResult;
use App\Models\ReviewItem;

/**
 * Every question a learner has ever been shown: submitted attempts, served
 * mock sessions, review items and offline practice. Full history, no cap.
 */
final class ExposureHistory
{
    /** @return array<int, true> */
    public function forUser(int $userId): array
    {
        $seen = [];

        foreach ([ExamAttempt::class, ExamSession::class] as $model) {
            $model::query()->where('user_id', $userId)->select(['id', 'question_ids'])
                ->chunkById(500, function ($rows) use (&$seen) {
                    foreach ($rows as $row) {
                        foreach ((array) $row->question_ids as $qid) {
                            $seen[(int) $qid] = true;
                        }
                    }
                });
        }

        foreach ([ReviewItem::class, OfflinePracticeResult::class] as $model) {
            foreach ($model::query()->where('user_id', $userId)->pluck('question_id') as $qid) {
                $seen[(int) $qid] = true;
            }
        }

        return $seen;
    }
}
