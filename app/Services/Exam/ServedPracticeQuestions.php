<?php

declare(strict_types=1);

namespace App\Services\Exam;

use Illuminate\Contracts\Session\Session;

/** Browser-owned, bounded eligibility for legacy drill and retake submissions. */
final class ServedPracticeQuestions
{
    public function remember(Session $session, ?int $userId, array $ids): string
    {
        $batches = array_values(array_filter((array) $session->get($this->key($userId), []),
            fn ($batch) => is_array($batch) && ($batch['until'] ?? 0) > now()->timestamp));
        $id = bin2hex(random_bytes(16));
        $batches[] = [
            'id' => $id,
            'ids' => array_slice(array_values(array_unique(array_map('intval', $ids))), 0, 300),
            'until' => now()->addDay()->timestamp,
        ];
        $session->put($this->key($userId), array_slice($batches, -20));

        return $id;
    }

    /** Newest served batch whose items include every submitted id. */
    public function coveringBatchId(Session $session, ?int $userId, array $questionIds): ?string
    {
        $wanted = array_map('intval', $questionIds);
        $found = null;

        foreach ($this->openBatches($session, $userId) as $batch) {
            if (array_diff($wanted, $batch['ids']) === []) {
                $found = $batch['id'];
            }
        }

        return $found;
    }

    /** Newest served batch whose ids are exactly the submitted set. */
    public function exactBatchId(Session $session, ?int $userId, array $questionIds): ?string
    {
        $wanted = array_values(array_unique(array_map('intval', $questionIds)));
        sort($wanted);
        $found = null;

        foreach ($this->openBatches($session, $userId) as $batch) {
            $ids = array_values(array_unique($batch['ids']));
            sort($ids);

            if ($ids === $wanted) {
                $found = $batch['id'];
            }
        }

        return $found;
    }

    /** The claimed batch belongs to this browser and contains every submitted id. */
    public function ownsBatch(Session $session, ?int $userId, string $batchId, array $questionIds): bool
    {
        if (strlen($batchId) !== 32) {
            return false;
        }

        $wanted = array_map('intval', $questionIds);

        foreach ($this->openBatches($session, $userId) as $batch) {
            if (! hash_equals($batch['id'], $batchId)) {
                continue;
            }

            return array_diff($wanted, $batch['ids']) === [];
        }

        return false;
    }

    /** Newest served batch that included this one item. */
    public function questionBatchId(Session $session, ?int $userId, int $questionId): ?string
    {
        $found = null;

        foreach ($this->openBatches($session, $userId) as $batch) {
            if (in_array($questionId, $batch['ids'], true)) {
                $found = $batch['id'];
            }
        }

        return $found;
    }

    /**
     * @return list<array{id: string, ids: array<int, int>}>
     */
    private function openBatches(Session $session, ?int $userId): array
    {
        $open = [];

        foreach ((array) $session->get($this->key($userId), []) as $batch) {
            if (! is_array($batch) || ($batch['until'] ?? 0) <= now()->timestamp || ! is_string($batch['id'] ?? null)) {
                continue;
            }

            $open[] = [
                'id' => $batch['id'],
                'ids' => array_map('intval', (array) ($batch['ids'] ?? [])),
            ];
        }

        return $open;
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
