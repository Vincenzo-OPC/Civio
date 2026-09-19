<?php

declare(strict_types=1);

namespace App\DTOs\Drill;

use App\Http\Requests\User\Drill\SavedDrillSets\StoreSavedDrillSetRequest;
use App\Http\Requests\User\Drill\SavedDrillSets\UpdateSavedDrillSetRequest;

readonly class UpsertSavedDrillSetData
{
    /**
     * @param  array<int, int>  $questionIds
     */
    public function __construct(
        public string $name,
        public ?string $description = null,
        public string $color = 'blue',
        public array $questionIds = [],
    ) {}

    public static function fromStoreRequest(StoreSavedDrillSetRequest $request): self
    {
        $v = $request->validated();

        return new self(
            name: trim((string) $v['name']),
            description: isset($v['description']) ? (string) $v['description'] : null,
            color: $v['color'] ?? 'blue',
            questionIds: array_map('intval', $v['question_ids'] ?? []),
        );
    }

    public static function fromUpdateRequest(UpdateSavedDrillSetRequest $request, ?string $fallbackColor = 'blue'): self
    {
        $v = $request->validated();

        return new self(
            name: trim((string) $v['name']),
            description: array_key_exists('description', $v) ? (string) $v['description'] : null,
            color: $v['color'] ?? $fallbackColor ?? 'blue',
            questionIds: [],
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toAttributes(): array
    {
        return [
            'name' => $this->name,
            'description' => $this->description,
            'color' => $this->color,
        ];
    }
}
