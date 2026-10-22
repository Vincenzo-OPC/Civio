<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable([
    'user_id',
    'question_id',
    'source_attempt_id',
    'outcome',
    'rating',
    'assisted',
    'scheduled',
    'due_at',
    'reviewed_at',
    'scheduler_version',
    'policy_version',
    'card_before',
    'card_after',
    'question_fingerprint',
])]
class ReviewEvent extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'question_id' => 'integer',
            'source_attempt_id' => 'integer',
            'assisted' => 'boolean',
            'scheduled' => 'boolean',
            'due_at' => 'datetime',
            'reviewed_at' => 'datetime',
            'card_before' => 'array',
            'card_after' => 'array',
            'created_at' => 'datetime',
        ];
    }

    /** @return BelongsTo<User, $this> */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /** @return BelongsTo<Question, $this> */
    public function question(): BelongsTo
    {
        return $this->belongsTo(Question::class);
    }
}
