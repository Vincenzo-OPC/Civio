<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable([
    'user_id',
    'question_id',
    'scheduler_version',
    'policy_version',
    'card_state',
    'due_at',
    'state',
    'last_rating',
    'last_reviewed_at',
    'reps',
    'lapses',
    'question_fingerprint',
])]
class ReviewCard extends Model
{
    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'question_id' => 'integer',
            'card_state' => 'array',
            'due_at' => 'datetime',
            'last_reviewed_at' => 'datetime',
            'reps' => 'integer',
            'lapses' => 'integer',
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
