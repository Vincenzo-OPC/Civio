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
class ExamQuestionResource extends JsonResource
{
    /**
     * Transform the question into the shape required by the interactive exam simulation.
     *
     * @return array{
     *     id: int,
     *     stem: string,
     *     options: array<int, string>,
     *     correct_option: int,
     *     explanation: string,
     *     category: string,
     *     subcategory: string,
     *     language: string,
     *     isDemographic: bool
     * }
     */
    public function toArray(Request $request): array
    {
        $rawLang = $this->language instanceof QuestionLanguage
            ? $this->language->value
            : (string) ($this->language ?? '');

        $language = QuestionLanguage::fromRaw($rawLang)->value;

        return [
            'id' => (int) $this->id,
            'stem' => (string) $this->stem,
            'options' => $this->options ?? [],
            'correct_option' => (int) $this->correct_option,
            'explanation' => (string) ($this->explanation ?? ''),
            'category' => $this->subcategory?->category?->name ?? 'General Information',
            'subcategory' => $this->subcategory?->name ?? '',
            'language' => $language,
            'isDemographic' => (bool) ($this->subcategory?->category?->is_demographic ?? false),
        ];
    }
}
