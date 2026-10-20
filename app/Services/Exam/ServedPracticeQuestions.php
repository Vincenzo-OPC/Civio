<?php

declare(strict_types=1);

namespace App\Services\Exam;

use Illuminate\Contracts\Session\Session;

/** Browser-owned, bounded eligibility for legacy drill and retake submissions. */
final class ServedPracticeQuestions
{
    public function remember(Session $session, ?int $userId, array $ids): void
    {
        $batches = array_filter((array) $session->get($this->key($userId), []),
            fn ($batch) => is_array($batch) && ($batch['until'] ?? 0) > now()->timestamp);
        $batches[] = [
            'ids' => array_slice(array_values(array_unique(array_map('intval', $ids))), 0, 300),
            'until' => now()->addDay()->timestamp,
        ];
        $session->put($this->key($userId), array_slice(array_values($batches), -20));
    }

    public function allows(Session $session, ?int $userId, array $ids): bool
    {
        foreach ((array) $session->get($this->key($userId), []) as $batch) {
            if (is_array($batch) && ($batch['until'] ?? 0) > now()->timestamp
                && array_diff($ids, $batch['ids'] ?? []) === []) {
                return true;
            }
        }

        return false;
    }

    private function key(?int $userId): string
    {
        return 'civio_practice_served_'.($userId ?? 'guest');
    }
}
