<?php

declare(strict_types=1);

namespace App\DTOs\Exam;

use App\Http\Requests\User\Exam\StoreExamAttemptRequest;

readonly class SubmitExamAttemptData
{
    /**
     * @param  array<int, int>  $questionIds
     * @param  array<int|string, mixed>  $answers
     * @param  array<string, mixed>  $catScores
     */
    public function __construct(
        public ?int $categoryId,
        public array $questionIds,
        public array $answers,
        public array $catScores,
    ) {}

    public static function fromRequest(StoreExamAttemptRequest $request): self
    {
        $v = $request->validated();

        return new self(
            categoryId: isset($v['category_id']) ? (int) $v['category_id'] : null,
            questionIds: (array) ($v['question_ids'] ?? []),
            answers: (array) ($v['answers'] ?? []),
            catScores: (array) ($v['cat_scores'] ?? []),
        );
    }

    /**
     * @return array{
     *     category_id: ?int,
     *     question_ids: array<int, int>,
     *     answers: array<int|string, mixed>,
     *     cat_scores: array<string, mixed>
     * }
     */
    public function toArray(): array
    {
        return [
            'category_id' => $this->categoryId,
            'question_ids' => $this->questionIds,
            'answers' => $this->answers,
            'cat_scores' => $this->catScores,
        ];
    }
}
