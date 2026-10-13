<?php

declare(strict_types=1);

namespace App\Models;

use App\Enums\ExamMode;
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
#[Fillable(['user_id', 'track', 'mode', 'question_ids', 'exam_attempt_id'])]
class ExamSession extends Model
{
    use HasUlids;

    /** Laravel session key holding the IDs of guest-owned exam sessions. */
    public const GUEST_SESSION_KEY = 'civio_exam_session_ids';

    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'mode' => ExamMode::class,
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
