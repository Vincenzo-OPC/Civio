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
     * When false (default), withhold correct_option / explanation for live play.
     * When true, include keys for scorecard / review after submission.
     */
    protected bool $includeAnswerKey = false;

    public function withAnswerKey(bool $include = true): static
    {
        $this->includeAnswerKey = $include;

        return $this;
    }

    /**
     * @param  iterable<int, Question>  $questions
     * @return array<int, array<string, mixed>>
     */
    public static function collectionForExam(iterable $questions, bool $includeAnswerKey = false): array
    {
        $out = [];
        foreach ($questions as $question) {
            $resource = new self($question);
            $resource->withAnswerKey($includeAnswerKey);
            $out[] = $resource->resolve();
        }

        return $out;
    }

    /**
     * @return array{
     *     id: int,
     *     stem: string,
     *     options: array<int, string>,
     *     correct_option?: int,
     *     explanation?: string,
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

        $payload = [
            'id' => (int) $this->id,
            'stem' => (string) $this->stem,
            'options' => $this->options ?? [],
            'category' => $this->subcategory?->category?->name ?? 'General Information',
            'subcategory' => $this->subcategory?->name ?? '',
            'language' => $language,
            'isDemographic' => (bool) ($this->subcategory?->category?->is_demographic ?? false),
        ];

        if ($this->includeAnswerKey) {
            $payload['correct_option'] = (int) $this->correct_option;
            $payload['explanation'] = (string) ($this->explanation ?? '');
        }

        return $payload;
    }
}
