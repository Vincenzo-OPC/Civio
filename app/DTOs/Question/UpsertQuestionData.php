<?php

declare(strict_types=1);

namespace App\DTOs\Question;

use App\Http\Requests\StoreQuestionRequest;
use App\Http\Requests\UpdateQuestionRequest;

readonly class UpsertQuestionData
{
    /**
     * @param  array<int, string>  $options
     */
    public function __construct(
        public string $stem,
        public string $category,
        public ?string $subcategory,
        public string $language,
        public array $options,
        public ?int $correctOption,
        public ?string $explanation,
        public string $status,
        public ?int $createdBy = null,
    ) {}

    public static function fromStoreRequest(StoreQuestionRequest $request): self
    {
        $v = $request->validated();

        return new self(
            stem: (string) $v['stem'],
            category: (string) $v['category'],
            subcategory: isset($v['subcategory']) ? (string) $v['subcategory'] : null,
            language: (string) ($v['language'] ?? 'English'),
            options: (array) $v['options'],
            correctOption: isset($v['correct_option']) ? (int) $v['correct_option'] : null,
            explanation: isset($v['explanation']) ? (string) $v['explanation'] : null,
            status: strtolower((string) ($v['status'] ?? 'draft')),
            createdBy: $request->user()?->id,
        );
    }

    public static function fromUpdateRequest(UpdateQuestionRequest $request): self
    {
        $v = $request->validated();

        return new self(
            stem: (string) $v['stem'],
            category: (string) $v['category'],
            subcategory: isset($v['subcategory']) ? (string) $v['subcategory'] : null,
            language: (string) ($v['language'] ?? 'English'),
            options: (array) $v['options'],
            correctOption: isset($v['correct_option']) ? (int) $v['correct_option'] : null,
            explanation: isset($v['explanation']) ? (string) $v['explanation'] : null,
            status: strtolower((string) ($v['status'] ?? 'draft')),
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        return array_filter([
            'stem' => $this->stem,
            'language' => $this->language,
            'options' => $this->options,
            'correct_option' => $this->correctOption,
            'explanation' => $this->explanation,
            'status' => $this->status,
            'created_by' => $this->createdBy,
        ], fn ($val) => $val !== null);
    }
}
