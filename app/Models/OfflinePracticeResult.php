<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * One offline drill answer after server re-grade (Lite L2).
 *
 * `status` is "accepted" (counted, `is_correct` from the server key) or
 * "rejected" (`reason`: key_mismatch, not_offline). `source` is always
 * "offline_practice".
 */
#[Fillable(['owner_key', 'user_id', 'client_id', 'question_id', 'selected_option', 'claimed_correct_option', 'is_correct', 'status', 'reason', 'source', 'pack_version', 'answered_at'])]
class OfflinePracticeResult extends Model
{
    public const SOURCE = 'offline_practice';

    public const ACCEPTED = 'accepted';

    public const REJECTED = 'rejected';

    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'question_id' => 'integer',
            'selected_option' => 'integer',
            'claimed_correct_option' => 'integer',
            'is_correct' => 'boolean',
            'answered_at' => 'datetime',
        ];
    }

    /** @return BelongsTo<Question, $this> */
    public function question(): BelongsTo
    {
        return $this->belongsTo(Question::class);
    }

    /** @return BelongsTo<User, $this> */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
