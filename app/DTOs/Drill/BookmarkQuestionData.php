<?php

declare(strict_types=1);

namespace App\DTOs\Drill;

use App\Http\Requests\User\Drill\SavedDrillSets\AddQuestionToSavedSetRequest;

readonly class BookmarkQuestionData
{
    public function __construct(
        public int $questionId,
        public ?int $savedDrillSetId = null,
        public ?string $newSetName = null,
    ) {}

    public static function fromRequest(AddQuestionToSavedSetRequest $request): self
    {
        $v = $request->validated();

        return new self(
            questionId: (int) $v['question_id'],
            savedDrillSetId: isset($v['saved_drill_set_id']) ? (int) $v['saved_drill_set_id'] : null,
            newSetName: isset($v['new_set_name']) ? trim((string) $v['new_set_name']) : null,
        );
    }
}
