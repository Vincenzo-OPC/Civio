<?php

namespace App\Models;

use App\Enums\ExamMode;
use App\Enums\SelectionPolicy;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['category_id', 'user_id', 'mode', 'selection_policy', 'selection_policy_version', 'question_ids', 'answers', 'cat_scores'])]
class ExamAttempt extends Model
{
    protected function casts(): array
    {
        return [
            'category_id' => 'integer',
            'user_id' => 'integer',
            'mode' => ExamMode::class,
            'selection_policy' => SelectionPolicy::class,
            'question_ids' => 'array',
            'answers' => 'array',
            'cat_scores' => 'array',
        ];
    }

    /** @var array<string, mixed> */
    protected $attributes = [
        'mode' => 'study',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }
}
