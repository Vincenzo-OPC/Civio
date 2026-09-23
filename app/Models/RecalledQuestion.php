<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable([
    'user_id',
    'stem',
    'options',
    'correct_option',
    'category',
    'subcategory',
    'note',
    'status',
    'moderator_note',
])]
class RecalledQuestion extends Model
{
    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'options' => 'array',
            'correct_option' => 'integer',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
