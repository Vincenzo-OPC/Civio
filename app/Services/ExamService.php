<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Exam\ExamSessionQueryData;
use App\Http\Resources\ExamQuestionResource;
use App\Http\Resources\ExamScorecardResource;
use App\Models\Question;
use App\Repositories\QuestionRepositoryInterface;
use App\Repositories\UserRepositoryInterface;
use Illuminate\Support\Collection;
use Inertia\DeferProp;
use Inertia\Inertia;

class ExamService
{
    public function __construct(
        protected QuestionRepositoryInterface $questionRepository,
        protected ExamAttemptService $attemptService,
        protected CategoryService $categoryService,
        protected DeterministicAnalysisService $deterministicService,
        protected UserRepositoryInterface $userRepository
    ) {}

    /**
     * Prepare all data required to initialize the interactive exam simulation session.
     *
     * @return array{
     *     questions: array<int, mixed>,
     *     categories: array<int, mixed>,
     *     savedAttempt: array<string, mixed>|null,
     *     retakeSource: array{attempt_id: int, question_ids: array<int, int>, track: string, mode: string}|null,
     *     aiAnalysis: array{status: string, data: array<string, mixed>|null}|DeferProp
     * }
     */
    public function getExamSessionData(ExamSessionQueryData $query, ?int $userId, bool $lite = false): array
    {
        $activeQuestions = $this->questionRepository->getActivePool();
        $savedAttempt = null;
        $retakeSource = null;
        $attempt = null;
        $includeAnswerKey = false;

        if ($query->attemptId !== null) {
            $attempt = $this->attemptService->getScorecardAttempt(
                attemptId: $query->attemptId,
                userId: $userId,
                pendingGuestId: $query->pendingGuestAttemptId
            );

            $includeAnswerKey = true;
            $savedAttempt = (new ExamScorecardResource($attempt))->resolve();
        } elseif ($query->retakeSame !== null || $query->retakeFresh !== null) {
            $retakeId = $query->retakeSame ?? $query->retakeFresh;
            $mode = $query->retakeSame !== null ? 'same' : 'fresh';

            if ($userId !== null && $retakeId !== null) {
                $retakeSource = $this->attemptService->getRetakeSource($retakeId, $userId, $mode);
                $attempt = $this->attemptService->getScorecardAttempt($retakeId, $userId, null);
            }
        }

        // Lite L1: never ship the whole bank. Full mocks are picked on the
        // server (POST /exams/sessions); this page only carries the items a
        // scorecard, retake or drill actually needs.
        if ($attempt !== null) {
            $wanted = array_map('intval', (array) $attempt->question_ids);
            $selected = $activeQuestions->whereIn('id', $wanted);
        } elseif ($query->isDrill) {
            $selected = $this->drillCandidates($activeQuestions, $query);
        } else {
            $selected = $activeQuestions->take(0);
        }

        $questions = collect(ExamQuestionResource::collectionForExam($selected, $includeAnswerKey));

        if (($savedAttempt || $retakeSource) && $attempt) {
            $questions = $questions->sortBy(function ($q) use ($attempt) {
                return array_search($q['id'], $attempt->question_ids);
            })->values();
        } else {
            $questions = $questions->values();
        }

        $categories = $this->categoryService->getCategoryTree();

        $resolveAnalysis = function () use ($userId, $query): array {
            if ($userId === null) {
                return ['status' => 'no_data', 'data' => null];
            }

            $targetAttemptId = $query->attemptId ?? $this->attemptService->getLatestUserAttemptId($userId);

            if (! $targetAttemptId) {
                return ['status' => 'no_data', 'data' => null];
            }

            return [
                'status' => 'ready',
                'data' => $this->deterministicService->generate($userId, $targetAttemptId, true),
            ];
        };

        return [
            'questions' => $questions->all(),
            'categories' => $categories,
            'savedAttempt' => $savedAttempt,
            'retakeSource' => $retakeSource,
            // Lite: the scorecard analysis follows after first paint.
            'aiAnalysis' => $lite ? Inertia::defer($resolveAnalysis) : $resolveAnalysis(),
        ];
    }

    /**
     * Items a drill launch may draw from: hand-picked IDs, else the requested
     * category (by ID, then by name like the client used to match), else the
     * first 30 scored items (the client's old fallback). Keys stay withheld.
     *
     * @param  Collection<int, Question>  $pool
     * @return Collection<int, Question>
     */
    protected function drillCandidates(Collection $pool, ExamSessionQueryData $query): Collection
    {
        $scored = $pool->reject(fn (Question $q) => (bool) ($q->subcategory?->category?->is_demographic ?? false));

        if ($query->customQuestionIds !== []) {
            $custom = $scored->whereIn('id', $query->customQuestionIds);

            if ($custom->isNotEmpty()) {
                return $custom;
            }
        }

        $matches = collect();

        if ($query->drillCategoryId !== null) {
            $matches = $scored->filter(fn (Question $q) => (int) ($q->subcategory?->category_id ?? 0) === $query->drillCategoryId);
        }

        if ($matches->isEmpty() && $query->drillCategoryName !== null && $query->drillCategoryName !== '') {
            $name = mb_strtolower($query->drillCategoryName);
            $matches = $scored->filter(function (Question $q) use ($name) {
                $category = mb_strtolower($q->subcategory?->category?->name ?? 'General Information');

                return str_contains($category, $name) || str_contains($name, $category);
            });
        }

        return $matches->isNotEmpty() ? $matches : $scored->take(30);
    }

    /**
     * Record a successful examination booklet PDF export.
     */
    public function trackPdfDownload(int $userId): void
    {
        $this->userRepository->incrementPdfDownloads($userId);
    }
}
