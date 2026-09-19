<?php

namespace App\Models;

use App\Enums\LegalContentType;
use Illuminate\Database\Eloquent\Model;

class LegalContent extends Model
{
    protected $fillable = [
        'type',
        'content',
    ];

    protected $casts = [
        'type' => LegalContentType::class,
        'updated_at' => 'datetime',
    ];
}
