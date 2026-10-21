<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['user_id', 'question_id'])]
class ReviewHelp extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return [
            'user_id' => 'integer',
            'question_id' => 'integer',
            'created_at' => 'datetime',
        ];
    }
}
