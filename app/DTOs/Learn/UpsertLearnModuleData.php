<?php

declare(strict_types=1);

namespace App\DTOs\Learn;

use App\Http\Requests\StoreLearnModuleRequest;
use App\Http\Requests\UpdateLearnModuleRequest;

readonly class UpsertLearnModuleData
{
    public function __construct(
        public ?int $categoryId,
        public ?int $subcategoryId,
        public ?string $categoryName,
        public ?string $subcategoryName,
        public string $title,
        public string $topic,
        public string $summary,
        public string $content,
        public int $estimatedMinutes,
        public bool $isPublished,
        public ?int $createdBy = null,
    ) {}

    public static function fromStoreRequest(StoreLearnModuleRequest $request): self
    {
        $v = $request->validated();

        return new self(
            categoryId: isset($v['category_id']) ? (int) $v['category_id'] : null,
            subcategoryId: isset($v['subcategory_id']) ? (int) $v['subcategory_id'] : null,
            categoryName: isset($v['category']) ? (string) $v['category'] : null,
            subcategoryName: isset($v['subcategory']) ? (string) $v['subcategory'] : null,
            title: (string) $v['title'],
            topic: (string) $v['topic'],
            summary: (string) $v['summary'],
            content: (string) $v['content'],
            estimatedMinutes: (int) $v['estimated_minutes'],
            isPublished: (bool) $v['is_published'],
            createdBy: $request->user()?->id,
        );
    }

    public static function fromUpdateRequest(UpdateLearnModuleRequest $request): self
    {
        $v = $request->validated();

        return new self(
            categoryId: isset($v['category_id']) ? (int) $v['category_id'] : null,
            subcategoryId: isset($v['subcategory_id']) ? (int) $v['subcategory_id'] : null,
            categoryName: isset($v['category']) ? (string) $v['category'] : null,
            subcategoryName: isset($v['subcategory']) ? (string) $v['subcategory'] : null,
            title: (string) $v['title'],
            topic: (string) $v['topic'],
            summary: (string) $v['summary'],
            content: (string) $v['content'],
            estimatedMinutes: (int) $v['estimated_minutes'],
            isPublished: (bool) $v['is_published'],
        );
    }

    /**
     * @param  array<string, mixed>  $data
     */
    public static function fromArray(array $data, ?int $createdBy = null): self
    {
        return new self(
            categoryId: isset($data['category_id']) ? (int) $data['category_id'] : null,
            subcategoryId: isset($data['subcategory_id']) ? (int) $data['subcategory_id'] : null,
            categoryName: isset($data['category']) ? (string) $data['category'] : null,
            subcategoryName: isset($data['subcategory']) ? (string) $data['subcategory'] : null,
            title: (string) $data['title'],
            topic: (string) $data['topic'],
            summary: (string) $data['summary'],
            content: (string) $data['content'],
            estimatedMinutes: (int) ($data['estimated_minutes'] ?? 15),
            isPublished: (bool) ($data['is_published'] ?? true),
            createdBy: $createdBy,
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        return array_filter([
            'category_id' => $this->categoryId,
            'subcategory_id' => $this->subcategoryId,
            'title' => $this->title,
            'topic' => $this->topic,
            'summary' => $this->summary,
            'content' => $this->content,
            'estimated_minutes' => $this->estimatedMinutes,
            'is_published' => $this->isPublished,
            'created_by' => $this->createdBy,
        ], fn ($val) => $val !== null);
    }
}
