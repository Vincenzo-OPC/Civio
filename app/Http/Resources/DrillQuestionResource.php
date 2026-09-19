<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\Question;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Question
 */
class DrillQuestionResource extends JsonResource
{
    /**
     * The "data" wrapper that should be applied.
     *
     * @var string|null
     */
    public static $wrap = null;

    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $languageRaw = strtolower((string) ($this->language ?? ''));
        $language = (str_contains($languageRaw, 'tagalog') || str_contains($languageRaw, 'filipino'))
            ? 'Filipino'
            : 'English';

        $data = [
            'id' => $this->id,
            'stem' => $this->stem,
            'options' => $this->options ?? [],
            'correct_option' => (int) $this->correct_option,
            'explanation' => $this->explanation ?? '',
            'category' => $this->subcategory?->category?->name ?? 'General Information',
            'subcategory' => $this->subcategory?->name ?? '',
            'language' => $language,
            'isDemographic' => (bool) ($this->subcategory?->category?->is_demographic ?? false),
        ];

        if ($this->created_by !== null) {
            $data['isCustom'] = true;
        }

        return $data;
    }
}
