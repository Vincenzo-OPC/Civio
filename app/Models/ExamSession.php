<?php

declare(strict_types=1);

namespace App\Models;

use App\Enums\ExamMode;
use App\Enums\SelectionPolicy;
use App\Services\Exam\MockPoolSelector;
use Carbon\CarbonInterface;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * A server-picked mock: which items the server chose for one Professional or
 * Subprofessional mock. Linked to the graded attempt on submit.
 *
 * `mode` is Study or Strict. An open Strict session locks its items' keys on
 * the server (see App\Services\Exam\StrictMockLock) until it is submitted.
 *
 * @property string $id
 * @property int|null $user_id
 * @property string $track
 * @property ExamMode $mode
 * @property array<int, int> $question_ids
 * @property int|null $exam_attempt_id
 */
#[Fillable(['user_id', 'track', 'mode', 'selection_policy', 'selection_policy_version', 'question_ids', 'exam_attempt_id', 'started_at', 'deadline_at', 'saved_answers', 'save_version', 'owner_session_hash'])]
class ExamSession extends Model
{
    use HasUlids;

    /** Laravel session key holding the IDs of guest-owned exam sessions. */
    public const GUEST_SESSION_KEY = 'civio_exam_session_ids';

    protected function casts(): array
    {
        return [
            'started_at' => 'immutable_datetime',
            'deadline_at' => 'immutable_datetime',
            'saved_answers' => 'array',
            'save_version' => 'integer',
            'user_id' => 'integer',
            'mode' => ExamMode::class,
            'selection_policy' => SelectionPolicy::class,
            'question_ids' => 'array',
            'exam_attempt_id' => 'integer',
        ];
    }

    /** @var array<string, mixed> */
    protected $attributes = [
        'mode' => 'study',
    ];

    public function isStrict(): bool
    {
        return $this->mode === ExamMode::Strict;
    }

    /** Legacy sessions retain the deadline implied by their original creation. */
    public function deadline(): ?CarbonInterface
    {
        if (! $this->isStrict()) {
            return null;
        }

        return $this->deadline_at ?? $this->created_at?->copy()->addSeconds(
            MockPoolSelector::timeLimitFor(
                MockPoolSelector::levelFor($this->track)
            )
        );
    }

    public function isExpired(): bool
    {
        return $this->deadline()?->lessThanOrEqualTo(now()) ?? false;
    }

    public function isOpen(): bool
    {
        return $this->exam_attempt_id === null;
    }

    /** @return BelongsTo<User, $this> */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /** @return BelongsTo<ExamAttempt, $this> */
    public function examAttempt(): BelongsTo
    {
        return $this->belongsTo(ExamAttempt::class);
    }
}
