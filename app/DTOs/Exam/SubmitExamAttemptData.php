<?php

declare(strict_types=1);

namespace App\DTOs\Exam;

use App\Http\Requests\User\Exam\StoreExamAttemptRequest;

readonly class SubmitExamAttemptData
{
    /**
     * @param  array<int, int>  $questionIds
     * @param  array<int|string, mixed>  $answers
     * @param  array<string, mixed>  $clientMetadata  Non-authoritative client timing/track fields only.
     */
    public function __construct(
        public ?int $categoryId,
        public array $questionIds,
        public array $answers,
        public array $clientMetadata = [],
    ) {}

    public static function fromRequest(StoreExamAttemptRequest $request): self
    {
        $v = $request->validated();

        $meta = [];
        if (isset($v['metadata']) && is_array($v['metadata'])) {
            $meta = $v['metadata'];
        } elseif (isset($v['cat_scores']['metadata']) && is_array($v['cat_scores']['metadata'])) {
            // Accept legacy nested shape but strip score fields later in grading.
            $meta = $v['cat_scores']['metadata'];
        }

        // Only keep non-score client context.
        $allowed = [
            'track', 'category_name', 'duration_secs', 'is_timed',
            'question_times', 'answer_changes', 'selected_subcategories',
            'language', 'question_count',
        ];
        $clientMetadata = [];
        foreach ($allowed as $key) {
            if (array_key_exists($key, $meta)) {
                $clientMetadata[$key] = $meta[$key];
            }
        }

        return new self(
            categoryId: isset($v['category_id']) ? (int) $v['category_id'] : null,
            questionIds: array_values(array_map('intval', (array) ($v['question_ids'] ?? []))),
            answers: (array) ($v['answers'] ?? []),
            clientMetadata: $clientMetadata,
        );
    }

    /**
     * @return array{
     *     category_id: ?int,
     *     question_ids: array<int, int>,
     *     answers: array<int|string, mixed>,
     *     client_metadata: array<string, mixed>
     * }
     */
    public function toArray(): array
    {
        return [
            'category_id' => $this->categoryId,
            'question_ids' => $this->questionIds,
            'answers' => $this->answers,
            'client_metadata' => $this->clientMetadata,
        ];
    }
}
