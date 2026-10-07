<?php

declare(strict_types=1);

namespace App\Models;

use App\Enums\QuestionSourceGroup;
use App\Enums\QuestionStatus;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['subcategory_id', 'language', 'stem', 'options', 'correct_option', 'explanation', 'created_by', 'status', 'source_group'])]
class Question extends Model
{
    use HasFactory;

    protected static function booted(): void
    {
        // Anything created through the app is Civio-authored unless a seed says otherwise.
        static::creating(function (Question $question): void {
            $question->source_group ??= QuestionSourceGroup::Civio;
        });
    }

    protected function casts(): array
    {
        return [
            'subcategory_id' => 'integer',
            'options' => 'array',
            'correct_option' => 'integer',
            'created_by' => 'integer',
            'status' => QuestionStatus::class,
            'source_group' => QuestionSourceGroup::class,
        ];
    }

    /** @return BelongsTo<Subcategory, $this> */
    public function subcategory(): BelongsTo
    {
        return $this->belongsTo(Subcategory::class);
    }

    /** @return BelongsTo<User, $this> */
    public function createdBy(): BelongsTo
    {
        return $this->belongsTo(User::class, 'created_by');
    }
}
