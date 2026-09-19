<?php

declare(strict_types=1);

namespace App\DTOs\Drill;

use App\Http\Requests\User\Drill\StoreCustomDrillQuestionRequest;

readonly class StoreCustomQuestionData
{
    /**
     * @param  array<int, string>  $options
     */
    public function __construct(
        public int $subcategoryId,
        public string $stem,
        public array $options,
        public int $correctOption,
        public ?string $explanation = null,
        public string $language = 'English',
    ) {}

    public static function fromRequest(StoreCustomDrillQuestionRequest $request): self
    {
        $v = $request->validated();

        return new self(
            subcategoryId: (int) $v['subcategory_id'],
            stem: (string) $v['stem'],
            options: $v['options'],
            correctOption: (int) $v['correct_option'],
            explanation: isset($v['explanation']) ? (string) $v['explanation'] : null,
            language: $v['language'] ?? 'English',
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toAttributes(int $userId): array
    {
        return [
            'subcategory_id' => $this->subcategoryId,
            'language' => $this->language,
            'stem' => $this->stem,
            'options' => $this->options,
            'correct_option' => $this->correctOption,
            'explanation' => $this->explanation ?? '',
            'created_by' => $userId,
            'status' => 'active',
        ];
    }
}
