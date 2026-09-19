<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Question\UpsertQuestionData;
use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Repositories\QuestionRepositoryInterface;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;

class QuestionService
{
    public function __construct(
        protected QuestionRepositoryInterface $questionRepository
    ) {}

    public function getQuestion(int|string $id): Question
    {
        /** @var Question */
        return $this->questionRepository->findOrFail($id, relations: ['subcategory.category']);
    }

    /**
     * @param  array<string, mixed>  $filters
     */
    public function getPaginatedQuestions(array $filters, int $perPage = 10): LengthAwarePaginator
    {
        return $this->questionRepository->paginateFiltered($filters, $perPage);
    }

    public function createQuestion(UpsertQuestionData $data): Question
    {
        $subcategoryId = $this->resolveSubcategoryId($data->category, $data->subcategory, $data->language);

        $attributes = [
            'subcategory_id' => $subcategoryId,
            'language' => $data->language,
            'stem' => $data->stem,
            'options' => $data->options,
            'correct_option' => $data->correctOption !== null ? $data->correctOption : -1,
            'explanation' => $data->explanation ?? '',
            'created_by' => $data->createdBy ?: (auth()->id() ?: (User::first()?->id ?: 1)),
            'status' => $data->status === 'active' ? 'active' : 'draft',
        ];

        /** @var Question $question */
        $question = $this->questionRepository->create($attributes);
        Cache::forget('questions.active');

        return $question->load('subcategory.category');
    }

    public function updateQuestion(int|string $id, UpsertQuestionData $data): Question
    {
        /** @var Question $question */
        $question = $this->questionRepository->findOrFail($id);
        $subcategoryId = $this->resolveSubcategoryId($data->category, $data->subcategory, $data->language);

        $attributes = [
            'subcategory_id' => $subcategoryId,
            'language' => $data->language,
            'stem' => $data->stem,
            'options' => $data->options,
            'correct_option' => $data->correctOption !== null ? $data->correctOption : -1,
            'explanation' => $data->explanation ?? '',
            'status' => $data->status === 'active' ? 'active' : 'draft',
        ];

        $this->questionRepository->update($id, $attributes);
        Cache::forget('questions.active');

        return $question->fresh(['subcategory.category']);
    }

    public function deleteQuestion(int|string $id): bool
    {
        $deleted = $this->questionRepository->delete($id);
        Cache::forget('questions.active');

        return $deleted;
    }

    /**
     * @param  array<int, array<string, mixed>>  $questionsData
     */
    public function commitBatchQuestions(array $questionsData): int
    {
        $savedCount = 0;

        foreach ($questionsData as $qData) {
            try {
                $subcategoryId = $this->resolveSubcategoryId(
                    (string) ($qData['category'] ?? 'General Information'),
                    (string) ($qData['subcategory'] ?? 'Core Concepts'),
                    (string) ($qData['language'] ?? 'English')
                );

                $dbQuestion = null;
                if (! empty($qData['id'])) {
                    $dbQuestion = $this->questionRepository->find($qData['id']);
                }

                $attributes = [
                    'subcategory_id' => $subcategoryId,
                    'language' => $qData['language'] ?? 'English',
                    'stem' => $qData['stem'],
                    'options' => $qData['options'],
                    'correct_option' => (int) $qData['correct_option'],
                    'explanation' => $qData['explanation'] ?? '',
                    'status' => 'active',
                ];

                if ($dbQuestion) {
                    $this->questionRepository->update($dbQuestion->id, $attributes);
                } else {
                    $this->questionRepository->create(array_merge($attributes, [
                        'created_by' => auth()->id() ?: (User::first()?->id ?: 1),
                    ]));
                }
                $savedCount++;
            } catch (\Throwable) {
                // Ignore failure in batch item to continue committing rest
            }
        }

        Cache::forget('questions.active');

        return $savedCount;
    }

    protected function resolveSubcategoryId(string $categoryName, ?string $subcategoryName, string $language = 'English'): ?int
    {
        $category = Category::firstOrCreate(
            ['slug' => Str::slug($categoryName)],
            ['name' => $categoryName]
        );

        $name = ! empty($subcategoryName) ? $subcategoryName : $categoryName;

        $subcategory = Subcategory::firstOrCreate(
            [
                'category_id' => $category->id,
                'slug' => Str::slug($name),
            ],
            [
                'name' => $name,
                'language' => $language,
            ]
        );

        return $subcategory->id;
    }
}
