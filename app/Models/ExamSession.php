<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * A server-picked mock: which items the server chose for one Professional or
 * Subprofessional mock. Linked to the graded attempt on submit.
 */
#[Fillable(['user_id', 'track', 'question_ids', 'exam_attempt_id'])]
class ExamSession extends Model
{
    use HasUlids;

    /** Laravel session key holding the IDs of guest-owned exam sessions. */
    public const GUEST_SESSION_KEY = 'civio_exam_session_ids';

    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'question_ids' => 'array',
            'exam_attempt_id' => 'integer',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function examAttempt(): BelongsTo
    {
        return $this->belongsTo(ExamAttempt::class);
    }
}
