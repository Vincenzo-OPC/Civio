<?php

declare(strict_types=1);

namespace App\Services\Exam;

use Carbon\Carbon;
use Illuminate\Support\Facades\Process;
use RuntimeException;

/**
 * Runs the existing ts-fsrs package on the server.
 * Callers pass a graded rating. They do not pass a browser-chosen due date.
 */
final class FsrsScheduler
{
    public const VERSION = 'ts-fsrs@5.4.2';

    /**
     * @param  list<array{key: string, card: array<string, mixed>|null, rating: string}>  $reviews
     * @return array<string, array<string, mixed>>
     */
    public function applyMany(array $reviews, \DateTimeInterface $now): array
    {
        if ($reviews === []) {
            return [];
        }

        $process = Process::timeout(15)->path(base_path())->input(json_encode([
            'now' => Carbon::parse($now)->utc()->toISOString(),
            'reviews' => array_map(fn (array $review): array => [
                'key' => $review['key'],
                'card' => $review['card'],
                'rating' => $review['rating'],
            ], $reviews),
        ], JSON_THROW_ON_ERROR))->run(['node', base_path('scripts/fsrs-apply.mjs')]);

        if (! $process->successful()) {
            throw new RuntimeException('FSRS scheduler failed. '.$process->errorOutput());
        }

        $decoded = json_decode($process->output(), true);

        if (! is_array($decoded) || ! is_array($decoded['results'] ?? null)) {
            throw new RuntimeException('FSRS scheduler returned an unusable schedule.');
        }

        $byKey = [];

        foreach ($decoded['results'] as $result) {
            if (! is_array($result) || ! isset($result['key'], $result['due'], $result['card']) || ! is_array($result['card'])) {
                throw new RuntimeException('FSRS scheduler omitted a card.');
            }

            $byKey[(string) $result['key']] = $result;
        }

        return $byKey;
    }
}
