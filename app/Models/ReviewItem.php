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
    'first_wrong_at',
    'last_result_at',
    'wrong_count',
    'status',
    'resolved_at',
    'resolved_by_attempt_id',
    'last_attempt_id',
])]
class ReviewItem extends Model
{
    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'question_id' => 'integer',
            'source_attempt_id' => 'integer',
            'first_wrong_at' => 'datetime',
            'last_result_at' => 'datetime',
            'wrong_count' => 'integer',
            'resolved_at' => 'datetime',
            'resolved_by_attempt_id' => 'integer',
            'last_attempt_id' => 'integer',
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
