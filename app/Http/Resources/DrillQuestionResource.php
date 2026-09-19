<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Enums\QuestionLanguage;
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
        $rawLang = $this->language instanceof QuestionLanguage
            ? $this->language->value
            : (string) ($this->language ?? '');

        $language = QuestionLanguage::fromRaw($rawLang)->value;

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
