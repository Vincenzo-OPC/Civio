<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Models\ReviewCard;
use App\Models\ReviewEvent;
use Carbon\Carbon;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\UniqueConstraintViolationException;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Throwable;

/**
 * Applies staged review events with ts-fsrs.
 * Node runs before the card row is locked. A failed run leaves the event
 * unscheduled so a later try can finish it. It does not invent a success.
 */
final class ReviewScheduleApplier
{
    public const SAVED = 'saved';

    public const UNCHANGED = 'unchanged';

    public const FAILED = 'failed';

    public function __construct(private readonly FsrsScheduler $scheduler) {}

    public function hasPending(int $userId): bool
    {
        return $this->pending($userId)->exists();
    }

    public function apply(int $userId): string
    {
        $lock = Cache::lock('review-schedule:'.$userId, 20);

        try {
            $lock->block(10);
        } catch (Throwable $exception) {
            report($exception);

            return self::FAILED;
        }

        try {
            return $this->applyUnlocked($userId);
        } finally {
            $lock->release();
        }
    }

    private function applyUnlocked(int $userId): string
    {
        if (! $this->hasPending($userId)) {
            return self::UNCHANGED;
        }

        $failed = false;

        for ($wave = 0; $wave < 8 && $this->hasPending($userId); $wave++) {
            $events = $this->oldestPerQuestion($userId);

            if ($events->isEmpty()) {
                break;
            }

            if (! $this->applyBatch($userId, $events)) {
                $failed = true;
                break;
            }
        }

        if ($failed || $this->hasPending($userId)) {
            return self::FAILED;
        }

        return self::SAVED;
    }

    /**
     * @return Collection<int, ReviewEvent>
     */
    private function oldestPerQuestion(int $userId): Collection
    {
        return $this->pending($userId)
            ->orderBy('id')
            ->get()
            ->unique('question_id')
            ->values();
    }

    /**
     * @param  Collection<int, ReviewEvent>  $events
     */
    private function applyBatch(int $userId, Collection $events): bool
    {
        for ($try = 0; $try < 2; $try++) {
            $questionIds = $events->map(fn (ReviewEvent $event): int => (int) $event->question_id)->all();
            $cards = ReviewCard::query()
                ->where('user_id', $userId)
                ->whereIn('question_id', $questionIds)
                ->get()
                ->keyBy(fn (ReviewCard $card): int => (int) $card->question_id);
            $stamps = [];
            $reviews = [];

            foreach ($events as $event) {
                $questionId = (int) $event->question_id;
                $card = $cards->get($questionId);
                $stamps[$questionId] = $this->stamp($card);
                $reviews[] = [
                    'key' => (string) $event->id,
                    'card' => is_array($card?->card_state) ? $card->card_state : null,
                    'rating' => (string) $event->rating,
                ];
            }

            try {
                $scheduled = $this->scheduler->applyMany($reviews, now());
            } catch (Throwable $exception) {
                report($exception);

                return false;
            }

            try {
                $written = DB::transaction(function () use ($userId, $events, $stamps, $scheduled): bool {
                    $lockedCards = ReviewCard::query()
                        ->where('user_id', $userId)
                        ->whereIn('question_id', array_keys($stamps))
                        ->lockForUpdate()
                        ->get()
                        ->keyBy(fn (ReviewCard $card): int => (int) $card->question_id);

                    foreach (array_keys($stamps) as $questionId) {
                        if ($this->stamp($lockedCards->get($questionId)) !== $stamps[$questionId]) {
                            return false;
                        }
                    }

                    $ready = [];

                    foreach ($events as $event) {
                        $lockedEvent = ReviewEvent::query()->whereKey($event->id)->lockForUpdate()->first();

                        if ($lockedEvent === null || $lockedEvent->scheduled) {
                            continue;
                        }

                        $next = $scheduled[(string) $event->id] ?? null;

                        if (! is_array($next)) {
                            return false;
                        }

                        $ready[] = [$lockedEvent, $next];
                    }

                    foreach ($ready as [$lockedEvent, $next]) {
                        $questionId = (int) $lockedEvent->question_id;
                        $card = $lockedCards->get($questionId);
                        $before = is_array($card?->card_state) ? $card->card_state : null;
                        $due = Carbon::parse($next['due'])->timezone((string) config('app.timezone'));
                        $payload = [
                            'scheduler_version' => FsrsScheduler::VERSION,
                            'policy_version' => FsrsRatingPolicy::VERSION,
                            'card_state' => $next['card'],
                            'due_at' => $due,
                            'state' => (string) $next['state'],
                            'last_rating' => (string) $lockedEvent->rating,
                            'last_reviewed_at' => now(),
                            'reps' => (int) ($next['reps'] ?? 0),
                            'lapses' => (int) ($next['lapses'] ?? 0),
                            'question_fingerprint' => $lockedEvent->question_fingerprint,
                        ];

                        if ($card === null) {
                            $lockedCards->put($questionId, ReviewCard::query()->create([
                                'user_id' => $userId,
                                'question_id' => $questionId,
                                ...$payload,
                            ]));
                        } else {
                            $card->forceFill($payload)->save();
                        }

                        $lockedEvent->forceFill([
                            'scheduled' => true,
                            'due_at' => $due,
                            'card_before' => $before,
                            'card_after' => $next['card'],
                        ])->save();
                    }

                    return true;
                });
            } catch (UniqueConstraintViolationException) {
                $written = false;
            }

            if ($written) {
                return true;
            }

            $events = ReviewEvent::query()
                ->whereIn('id', $events->modelKeys())
                ->where('scheduled', false)
                ->orderBy('id')
                ->get();

            if ($events->isEmpty()) {
                return true;
            }
        }

        return false;
    }

    /** @return Builder<ReviewEvent> */
    private function pending(int $userId)
    {
        return ReviewEvent::query()
            ->where('user_id', $userId)
            ->where('scheduled', false)
            ->where('assisted', false)
            ->whereNotNull('rating');
    }

    private function stamp(?ReviewCard $card): string
    {
        if ($card === null) {
            return 'none';
        }

        $encoded = json_encode($card->card_state, JSON_THROW_ON_ERROR);

        return $card->updated_at?->utc()->format('U.u').'|'.hash('sha256', (string) $encoded);
    }
}
