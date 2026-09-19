<?php

declare(strict_types=1);

namespace App\DTOs\Learn;

use Illuminate\Http\Request;

readonly class LearnFilterData
{
    public function __construct(
        public ?string $search = null,
        public string $status = 'all',
        public string $category = 'all',
        public string $subcategory = 'all',
        public int $perPage = 10,
    ) {}

    public static function fromRequest(Request $request): self
    {
        return new self(
            search: $request->filled('search') ? (string) $request->input('search') : null,
            status: (string) $request->input('status', 'all'),
            category: (string) $request->input('category', 'all'),
            subcategory: (string) $request->input('subcategory', 'all'),
            perPage: min(50, max(5, $request->integer('per_page', 10))),
        );
    }

    /**
     * @return array{
     *     search: string,
     *     status: string,
     *     category: string,
     *     subcategory: string,
     *     per_page: int
     * }
     */
    public function toArray(): array
    {
        return [
            'search' => $this->search ?? '',
            'status' => $this->status,
            'category' => $this->category,
            'subcategory' => $this->subcategory,
            'per_page' => $this->perPage,
        ];
    }
}
