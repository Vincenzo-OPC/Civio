<?php

declare(strict_types=1);

namespace App\Actions\Question;

use App\Models\Category;
use App\Models\Subcategory;
use App\Repositories\QuestionRepositoryInterface;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class BulkUpdateQuestionsAction
{
    public function __construct(
        protected QuestionRepositoryInterface $questionRepository
    ) {}

    /**
     * @param  array<int, int|string>  $ids
     */
    public function updateStatus(array $ids, string $status): int
    {
        return DB::transaction(fn () => $this->questionRepository->bulkUpdateStatus($ids, $status));
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function delete(array $ids): int
    {
        return DB::transaction(fn () => $this->questionRepository->bulkDelete($ids));
    }

    /**
     * @param  array<int, array<string, mixed>>  $questionsData
     */
    public function updateQuestions(array $questionsData): void
    {
        DB::transaction(function () use ($questionsData) {
            foreach ($questionsData as $qData) {
                if (empty($qData['id'])) {
                    continue;
                }

                $category = Category::firstOrCreate([
                    'name' => $qData['category'],
                ], [
                    'slug' => Str::slug($qData['category']),
                    'sort_order' => 1,
                ]);

                $subcategoryName = $qData['subcategory'] ?? $qData['category'];

                $subcategory = Subcategory::firstOrCreate([
                    'category_id' => $category->id,
                    'name' => $subcategoryName,
                ], [
                    'slug' => Str::slug($subcategoryName),
                    'language' => $qData['language'] ?? 'English',
                ]);

                $this->questionRepository->update($qData['id'], [
                    'subcategory_id' => $subcategory->id,
                    'language' => $qData['language'] ?? 'English',
                    'stem' => $qData['stem'],
                    'options' => $qData['options'],
                    'correct_option' => (int) $qData['correct_option'],
                    'explanation' => $qData['explanation'] ?? '',
                    'status' => $qData['status'],
                ]);
            }
            Cache::forget('questions.active');
        });
    }
}
