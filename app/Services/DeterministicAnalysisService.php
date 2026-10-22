<?php

namespace App\Services;

use App\Enums\SelectionPolicy;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamDate;
use App\Models\Question;
use App\Models\Subcategory;
use Carbon\Carbon;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Schema;

class DeterministicAnalysisService
{
    protected array $categories = [
        'Verbal Ability',
        'Clerical Ability',
        'General Information',
        'Numerical Ability',
        'Analytical Ability',
    ];

    /**
     * Generate deterministic analysis for a user's exam attempts.
     *
     * @return array<string, mixed>
     */
    public function generate(int $userId, int $latestAttemptId, bool $singleAttemptOnly = false): array
    {
        $attempts = $this->resolveAttempts($userId, $latestAttemptId, $singleAttemptOnly);
        if (! $attempts) {
            return $this->getEmptyAnalysis();
        }

        $metrics = $this->aggregateAttemptMetrics($attempts);
        $totalAttempts = $attempts->count();

        // Volume-weighted overall average calculation
        if ($metrics['mockTotalQuestions'] > 0) {
            $avgScore = (int) round(($metrics['mockTotalCorrect'] / $metrics['mockTotalQuestions']) * 100);
            $trendScores = ! empty($metrics['mockScores']) ? $metrics['mockScores'] : $metrics['scores'];
        } else {
            $avgScore = $metrics['allTotalQuestions'] > 0 ? (int) round(($metrics['allTotalCorrect'] / $metrics['allTotalQuestions']) * 100) : 0;
            $trendScores = ! empty($metrics['scores']) ? $metrics['scores'] : $metrics['mockScores'];
        }
        $passingRate = $metrics['mockExamCount'] > 0 ? round(($metrics['passCount'] / $metrics['mockExamCount']) * 100) : 0;

        $subtopicStats = $this->calculateSubtopicStats($attempts);
        $mastery = $this->evaluateSubjectMastery($metrics['categoryTotals']);
        $trend = $this->calculateTrend($trendScores);
        $examDate = $this->resolveExamDate();

        $mockAccuracy = $this->buildMockAccuracy($metrics);

        $completionPace = $this->pickTemplate('completion_pace_'.$trend, compact('totalAttempts'));
        $remediation = $this->buildRemediationMatrix($subtopicStats, $mastery['criticalWeaknesses']);
        $studyPlan = $this->buildPersonalizedStudyPlan($remediation['recommendedSubcatIds'], $remediation['recommendedModules']);

        // Context-aware personalized text
        $scoreTier = $avgScore >= 80 ? 'high' : ($avgScore >= 60 ? 'mid' : 'low');
        $strengthsList = implode(' and ', array_slice($mastery['strengths'], 0, 2)) ?: 'none identified yet';
        $weakList = implode(' and ', array_slice($mastery['criticalWeaknesses'], 0, 2)) ?: 'none identified yet';
        $topModule = $remediation['recommendedModules'][0] ?? 'General Review';

        $daysUntilExam = $examDate['daysUntilExam'];
        $examDateStr = $examDate['examDateStr'];
        $mockExamCount = $metrics['mockExamCount'];

        $templateVars = compact(
            'totalAttempts', 'avgScore', 'daysUntilExam',
            'examDateStr', 'strengthsList', 'weakList', 'topModule',
            'mockExamCount', 'passingRate', 'trend'
        );

        if ($mockExamCount === 0) {
            $verdict = $metrics['allTotalQuestions'] > 0
                ? $this->pickTemplate('verdict_no_mock', $templateVars)
                : $this->pickTemplate('verdict_empty', []);
        } else {
            $verdict = $this->pickTemplate("verdict_{$scoreTier}", $templateVars);
        }

        $encouragement = $this->pickTemplate("encouragement_{$scoreTier}_{$trend}", $templateVars)
            ?? $this->pickTemplate("encouragement_{$scoreTier}", $templateVars);
        $priorityAction = count($remediation['recommendedModules']) > 0
            ? $this->pickTemplate('priority_action', $templateVars)
            : $this->pickTemplate('priority_action_none', $templateVars);

        return [
            'mock_accuracy' => $mockAccuracy,
            'verdict' => $verdict,
            'trend' => $trend,
            'strengths' => $mastery['strengths'],
            'critical_weaknesses' => array_slice($mastery['criticalWeaknesses'], 0, 3),
            'priority_action' => $priorityAction,
            'recommended_modules' => array_slice($remediation['recommendedModules'], 0, 3),
            'encouragement' => $encouragement,
            'predictive_metrics' => [
                'completion_pace' => $completionPace,
            ],
            'subject_mastery' => $mastery['subjectMastery'],
            'timeline_prediction' => [
                'current_stage' => $this->resolveCurrentStage($avgScore),
                'milestone_prediction' => $this->pickTemplate("milestone_{$scoreTier}", $templateVars),
                'potential_score_improvement' => $this->pickTemplate("improvement_{$scoreTier}", $templateVars),
            ],
            'remediation_matrix' => $remediation['remediationMatrix'],
            'personalized_study_plan' => $studyPlan,
        ];
    }

    /**
     * Resolve the collection of attempts to evaluate.
     *
     * @return Collection<int, ExamAttempt>|null
     */
    protected function resolveAttempts(int $userId, int $latestAttemptId, bool $singleAttemptOnly): ?Collection
    {
        // Limit evaluation to the latest 10 attempts to reflect current readiness rather than stale historical scores
        $allAttempts = ExamAttempt::where('user_id', $userId)->latest()->take(10)->get()->reverse()->values();

        if ($allAttempts->isEmpty()) {
            return null;
        }

        $latestAttempt = $allAttempts->firstWhere('id', $latestAttemptId) ?? ExamAttempt::find($latestAttemptId);
        if (! $latestAttempt) {
            return null;
        }

        if ($singleAttemptOnly) {
            return collect([$latestAttempt]);
        }

        $latestMeta = $latestAttempt->cat_scores['metadata'] ?? [];
        $latestTrack = $latestMeta['track'] ?? 'Drill';
        if ($latestAttempt->category_id !== null && ! isset($latestMeta['track'])) {
            $latestTrack = 'Drill';
        }

        if ($latestTrack === 'Drill') {
            $mostRecentMock = $allAttempts->reverse()->first(function (ExamAttempt $attempt): bool {
                $meta = $attempt->cat_scores['metadata'] ?? [];
                $track = $meta['track'] ?? 'Drill';
                if ($attempt->category_id !== null && ! isset($meta['track'])) {
                    $track = 'Drill';
                }

                return $track !== 'Drill';
            });
            if ($mostRecentMock) {
                $mockMeta = $mostRecentMock->cat_scores['metadata'] ?? [];
                $latestTrack = $mockMeta['track'] ?? 'Professional';
            } else {
                $latestTrack = 'Professional';
            }
        }

        $filteredAttempts = $allAttempts->filter(function (ExamAttempt $attempt) use ($latestTrack): bool {
            $meta = $attempt->cat_scores['metadata'] ?? [];
            $track = $meta['track'] ?? 'Drill';
            if ($attempt->category_id !== null && ! isset($meta['track'])) {
                $track = 'Drill';
            }

            return $track === $latestTrack || $track === 'Drill';
        });

        if ($filteredAttempts->count() === 0) {
            return null;
        }

        return $filteredAttempts;
    }

    /**
     * Aggregate volume-weighted scores, pass counts, and category totals.
     *
     * @param  Collection<int, ExamAttempt>  $attempts
     * @return array{
     *     scores: array<int, int>,
     *     mockScores: array<int, int>,
     *     mockExamCount: int,
     *     passCount: int,
     *     allTotalCorrect: int,
     *     allTotalQuestions: int,
     *     mockTotalCorrect: int,
     *     mockTotalQuestions: int,
     *     mockBuckets: array<string, array<string, int>>,
     *     mockTracks: array<int, string>,
     *     categoryTotals: array<string, array{correct: int, total: int}>
     * }
     */
    protected function aggregateAttemptMetrics(Collection $attempts): array
    {
        $scores = [];
        $mockScores = [];
        $mockExamCount = 0;
        $passCount = 0;
        $allTotalCorrect = 0;
        $allTotalQuestions = 0;
        $mockTotalCorrect = 0;
        $mockTotalQuestions = 0;
        $mockBuckets = [
            'representative' => ['correct' => 0, 'total' => 0, 'mocks' => 0],
            'personalized' => ['correct' => 0, 'total' => 0, 'mocks' => 0, 'legacy' => 0],
        ];
        $mockTracks = [];

        $categoriesMap = Category::all()->keyBy('id');

        $categoryTotals = [];
        foreach ($this->categories as $cat) {
            $categoryTotals[$cat] = ['correct' => 0, 'total' => 0];
        }

        foreach ($attempts as $attempt) {
            $meta = $attempt->cat_scores['metadata'] ?? [];
            $correct = $meta['correct_count'] ?? 0;
            $total = $meta['total_questions'] ?? count($attempt->question_ids ?? []);
            $percentage = $total > 0 ? round(($correct / $total) * 100) : 0;

            $track = $meta['track'] ?? 'Drill';
            if ($attempt->category_id !== null && ! isset($meta['track'])) {
                $track = 'Drill';
            }

            $allTotalCorrect += $correct;
            $allTotalQuestions += $total;

            if ($track !== 'Drill') {
                $mockExamCount++;
                $mockTotalCorrect += $correct;
                $mockTotalQuestions += $total;
                $mockScores[] = (int) $percentage;
                $mockTracks[(string) $track] = true;
                $policy = $attempt->selection_policy instanceof SelectionPolicy ? $attempt->selection_policy : null;
                $bucket = $policy === SelectionPolicy::Representative ? 'representative' : 'personalized';
                $mockBuckets[$bucket]['correct'] += (int) $correct;
                $mockBuckets[$bucket]['total'] += (int) $total;
                $mockBuckets[$bucket]['mocks']++;
                if ($policy === null && $bucket === 'personalized') {
                    $mockBuckets['personalized']['legacy']++;
                }
                if ($percentage >= 80) {
                    $passCount++;
                }
            } else {
                $scores[] = (int) $percentage;
            }

            $scoreMap = $attempt->cat_scores['categoryScoreMap'] ?? [];
            if (! empty($scoreMap)) {
                foreach ($scoreMap as $catName => $scoreData) {
                    $normalizedCat = $this->normalizeCategory($catName);
                    if (isset($categoryTotals[$normalizedCat])) {
                        $categoryTotals[$normalizedCat]['correct'] += $scoreData['correct'] ?? 0;
                        $categoryTotals[$normalizedCat]['total'] += $scoreData['total'] ?? 0;
                    }
                }
            } else {
                $drillCatId = $attempt->category_id;
                $drillCategoryName = null;
                if ($drillCatId && isset($categoriesMap[$drillCatId])) {
                    $drillCategoryName = $categoriesMap[$drillCatId]->name;
                } elseif (isset($meta['category_name'])) {
                    $drillCategoryName = $meta['category_name'];
                }

                if ($drillCategoryName) {
                    $normalizedCat = $this->normalizeCategory($drillCategoryName);
                    if (isset($categoryTotals[$normalizedCat])) {
                        $categoryTotals[$normalizedCat]['correct'] += $correct;
                        $categoryTotals[$normalizedCat]['total'] += $total;
                    }
                }
            }
        }

        return [
            'scores' => $scores,
            'mockScores' => $mockScores,
            'mockExamCount' => $mockExamCount,
            'passCount' => $passCount,
            'allTotalCorrect' => $allTotalCorrect,
            'allTotalQuestions' => $allTotalQuestions,
            'mockTotalCorrect' => $mockTotalCorrect,
            'mockTotalQuestions' => $mockTotalQuestions,
            'mockBuckets' => $mockBuckets,
            'mockTracks' => array_keys($mockTracks),
            'categoryTotals' => $categoryTotals,
        ];
    }

    /**
     * Compute correctness counts per subtopic from attempt answers.
     *
     * @param  Collection<int, ExamAttempt>  $attempts
     * @return array<string, array{correct: int, total: int}>
     */
    protected function calculateSubtopicStats(Collection $attempts): array
    {
        $subtopicStats = [];
        $allQuestionIds = [];
        foreach ($attempts as $attempt) {
            if ($attempt->question_ids) {
                $allQuestionIds = array_merge($allQuestionIds, $attempt->question_ids);
            }
        }
        $allQuestionIds = array_unique($allQuestionIds);

        $questionsMap = [];
        if (! empty($allQuestionIds)) {
            $questionsMap = Question::whereIn('id', $allQuestionIds)
                ->with('subcategory')
                ->get()
                ->keyBy('id');
        }

        foreach ($attempts as $attempt) {
            $answers = $attempt->answers ?? [];
            if (empty($answers) || empty($attempt->question_ids)) {
                continue;
            }
            $qIds = array_values(array_map('intval', $attempt->question_ids));
            $grading = app(ExamGradingService::class);
            foreach ($qIds as $qId) {
                if (! isset($questionsMap[$qId])) {
                    continue;
                }
                $q = $questionsMap[$qId];
                $subcatName = $q->subcategory?->name ?? 'General Info';
                $userAns = $grading->chosenForQuestion($answers, $qIds, $qId, $attempt->cat_scores['metadata']['answer_schema'] ?? null);
                $isCorrect = ($userAns !== null && (int) $userAns === (int) $q->correct_option);

                if (! isset($subtopicStats[$subcatName])) {
                    $subtopicStats[$subcatName] = ['correct' => 0, 'total' => 0];
                }
                $subtopicStats[$subcatName]['total']++;
                if ($isCorrect) {
                    $subtopicStats[$subcatName]['correct']++;
                }
            }
        }

        return $subtopicStats;
    }

    /**
     * Evaluate subject mastery, strengths, and critical weaknesses.
     *
     * @param  array<string, array{correct: int, total: int}>  $categoryTotals
     * @return array{
     *     categoryBreakdown: array<string, array{correct: int, total: int, percentage: float|int}>,
     *     strengths: array<int, string>,
     *     criticalWeaknesses: array<int, string>,
     *     subjectMastery: array<int, array{subject: string, rating: string, color: string, insight: string, recommended_action: string}>
     * }
     */
    protected function evaluateSubjectMastery(array $categoryTotals): array
    {
        $categoryBreakdown = [];
        foreach ($categoryTotals as $catName => $data) {
            $categoryBreakdown[$catName] = [
                'correct' => $data['correct'],
                'total' => $data['total'],
                'percentage' => $data['total'] > 0 ? round(($data['correct'] / $data['total']) * 100) : 0,
            ];
        }

        $strengths = [];
        $weaknesses = [];
        $subjectMastery = [];

        foreach ($categoryBreakdown as $subject => $data) {
            $pct = $data['percentage'];
            $totalQ = $data['total'];

            if ($totalQ === 0) {
                $rating = 'Insufficient Data';
                $color = 'sky';
                $insight = $this->pickTemplate('insight_no_data', compact('subject'));
                $action = $this->pickTemplate('action_no_data', compact('subject'));
            } elseif ($pct >= 80) {
                $rating = 'Practice 80+';
                $color = 'emerald';
                $insight = $this->pickTemplate('insight_mastered', compact('subject', 'pct'));
                $action = $this->pickTemplate('action_mastered', compact('subject'));
                $strengths[] = $subject;
            } elseif ($pct >= 60) {
                $rating = 'Needs Practice';
                $color = 'amber';
                $insight = $this->pickTemplate('insight_moderate', compact('subject', 'pct'));
                $action = $this->pickTemplate('action_moderate', compact('subject'));
                $weaknesses[$subject] = $pct;
            } else {
                $rating = 'Below 60%';
                $color = 'rose';
                $insight = $this->pickTemplate('insight_critical', compact('subject', 'pct'));
                $action = $this->pickTemplate('action_critical', compact('subject'));
                $weaknesses[$subject] = $pct;
            }

            $subjectMastery[] = [
                'subject' => $subject,
                'rating' => $rating,
                'color' => $color,
                'insight' => $insight,
                'recommended_action' => $action,
            ];
        }

        asort($weaknesses);
        $criticalWeaknesses = array_keys($weaknesses);

        if (empty($strengths) && empty($criticalWeaknesses)) {
            $criticalWeaknesses = [$this->categories[0]];
        }

        return [
            'categoryBreakdown' => $categoryBreakdown,
            'strengths' => $strengths,
            'criticalWeaknesses' => $criticalWeaknesses,
            'subjectMastery' => $subjectMastery,
        ];
    }

    /**
     * Determine trend direction based on historical score progression.
     *
     * @param  array<int, int>  $trendScores
     */
    protected function calculateTrend(array $trendScores): string
    {
        if (count($trendScores) >= 3) {
            $recent = array_slice($trendScores, -3);
            if ($recent[2] > $recent[0] + 5) {
                return 'improving';
            }
            if ($recent[2] < $recent[0] - 5) {
                return 'declining';
            }

            return 'stable';
        }

        if (count($trendScores) < 2) {
            return 'insufficient_data';
        }

        return 'stable';
    }

    /**
     * Resolve days until exam and formatted exam date string.
     *
     * @return array{daysUntilExam: int, examDateStr: string}
     */
    protected function resolveExamDate(): array
    {
        $daysUntilExam = null;
        $examDateStr = 'Not set';

        if (Schema::hasTable('exam_dates')) {
            $examDate = ExamDate::where('is_active', true)
                ->where('date', '>', now())
                ->orderBy('date')
                ->first();
            if ($examDate) {
                $examDateCarbon = Carbon::parse($examDate->date);
                $daysUntilExam = (int) ceil(now()->diffInDays($examDateCarbon, false));
                $examDateStr = $examDateCarbon->format('F j, Y');
            }
        }

        if ($daysUntilExam === null) {
            $daysUntilExam = (int) ceil(now()->diffInDays(Carbon::parse('2026-08-09'), false));
            $examDateStr = 'August 9, 2026';
        }

        return [
            'daysUntilExam' => $daysUntilExam,
            'examDateStr' => $examDateStr,
        ];
    }

    /**
     * Mock Accuracy: correct over scored questions on submitted full mocks.
     * A practice measurement only, never a pass prediction. Representative
     * (Strict, server policy stored per attempt) mocks are kept apart from
     * personalized ones (Study/adaptive, plus legacy rows with no policy).
     *
     * @param  array<string, mixed>  $metrics
     * @return array<string, mixed>
     */
    protected function buildMockAccuracy(array $metrics): array
    {
        $part = function (array $b): array {
            $total = (int) $b['total'];

            return [
                'correct' => (int) $b['correct'],
                'total' => $total,
                'mocks' => (int) $b['mocks'],
                'percent' => $total > 0 ? round(((int) $b['correct'] / $total) * 100, 1) : null,
            ];
        };

        $all = [
            'correct' => (int) $metrics['mockTotalCorrect'],
            'total' => (int) $metrics['mockTotalQuestions'],
            'mocks' => (int) $metrics['mockExamCount'],
        ];
        $buckets = $metrics['mockBuckets'];

        return array_merge($part($all), [
            'tracks' => array_values($metrics['mockTracks']),
            'representative' => $part($buckets['representative']),
            'personalized' => array_merge($part($buckets['personalized']), ['legacy' => (int) $buckets['personalized']['legacy']]),
            'note' => 'Practice accuracy on submitted Civio mocks. Not an official rating or a pass prediction.',
        ]);
    }

    /**
     * Build remediation matrix and recommended subcategories/modules based on weak subtopics.
     *
     * @param  array<string, array{correct: int, total: int}>  $subtopicStats
     * @param  array<int, string>  $criticalWeaknesses
     * @return array{
     *     remediationMatrix: array<int, array{subtopic: string, difficulty_level: string, reason_for_struggle: string, coaching_tip: string}>,
     *     recommendedSubcatIds: array<int, int>,
     *     recommendedModules: array<int, string>
     * }
     */
    protected function buildRemediationMatrix(array $subtopicStats, array $criticalWeaknesses): array
    {
        $subcategories = Subcategory::with('category')->get();

        $worstSubtopics = [];
        foreach ($subtopicStats as $subcatName => $data) {
            $pct = round(($data['correct'] / $data['total']) * 100);
            if ($pct < 75) {
                $worstSubtopics[$subcatName] = $pct;
            }
        }
        asort($worstSubtopics);

        $primaryWeakSubject = $criticalWeaknesses[0] ?? null;
        $remediationMatrix = [];
        $recommendedSubcatIds = [];
        $recommendedModules = [];

        $availableSubcatMap = [];
        foreach ($subcategories as $sub) {
            $availableSubcatMap[$sub->name] = $sub;
        }

        // 1. Prioritize worst subtopics belonging to the primary critical weakness subject
        if ($primaryWeakSubject) {
            foreach (array_keys($worstSubtopics) as $worstName) {
                if (isset($availableSubcatMap[$worstName])) {
                    $sub = $availableSubcatMap[$worstName];
                    if ($sub->category?->name === $primaryWeakSubject && ! in_array($sub->name, $recommendedModules, true)) {
                        $remediationMatrix[] = [
                            'subtopic' => $sub->name,
                            'difficulty_level' => 'Hard',
                            'reason_for_struggle' => $this->pickTemplate('struggle_reason_hard', ['subtopic' => $sub->name]),
                            'coaching_tip' => $this->pickTemplate('coaching_hard', ['subtopic' => $sub->name]),
                        ];
                        $recommendedSubcatIds[] = $sub->id;
                        $recommendedModules[] = $sub->name;
                        if (count($recommendedModules) >= 3) {
                            break;
                        }
                    }
                }
            }
        }

        // 2. If still need modules, add other worst subtopics
        if (count($recommendedModules) < 3) {
            foreach (array_keys($worstSubtopics) as $worstName) {
                if (isset($availableSubcatMap[$worstName])) {
                    $sub = $availableSubcatMap[$worstName];
                    if (! in_array($sub->name, $recommendedModules, true)) {
                        $remediationMatrix[] = [
                            'subtopic' => $sub->name,
                            'difficulty_level' => 'Hard',
                            'reason_for_struggle' => $this->pickTemplate('struggle_reason_hard', ['subtopic' => $sub->name]),
                            'coaching_tip' => $this->pickTemplate('coaching_hard', ['subtopic' => $sub->name]),
                        ];
                        $recommendedSubcatIds[] = $sub->id;
                        $recommendedModules[] = $sub->name;
                        if (count($recommendedModules) >= 3) {
                            break;
                        }
                    }
                }
            }
        }

        // 3. If still need modules, fill from critical weaknesses categories
        if (count($recommendedModules) < 3) {
            foreach ($criticalWeaknesses as $weakSubject) {
                foreach ($subcategories as $sub) {
                    if ($sub->category?->name === $weakSubject && ! in_array($sub->name, $recommendedModules, true)) {
                        $remediationMatrix[] = [
                            'subtopic' => $sub->name,
                            'difficulty_level' => 'Medium',
                            'reason_for_struggle' => $this->pickTemplate('struggle_reason_medium', ['subtopic' => $sub->name]),
                            'coaching_tip' => $this->pickTemplate('coaching_medium', ['subtopic' => $sub->name]),
                        ];
                        $recommendedSubcatIds[] = $sub->id;
                        $recommendedModules[] = $sub->name;
                        if (count($recommendedModules) >= 3) {
                            break 2;
                        }
                    }
                }
            }
        }

        return [
            'remediationMatrix' => $remediationMatrix,
            'recommendedSubcatIds' => $recommendedSubcatIds,
            'recommendedModules' => $recommendedModules,
        ];
    }

    /**
     * Build 7-day personalized study schedule tasks.
     *
     * @param  array<int, int>  $recommendedSubcatIds
     * @param  array<int, string>  $recommendedModules
     * @return array<int, array{day: string, tasks: array<int, array{focus_topic: string, activity: string, subcategory_id: int|null}>}>
     */
    protected function buildPersonalizedStudyPlan(array $recommendedSubcatIds, array $recommendedModules): array
    {
        $personalizedStudyPlan = [];
        for ($day = 1; $day <= 7; $day++) {
            $subcatIndex = ($day - 1) % max(1, count($recommendedSubcatIds));
            $subcatId = ! empty($recommendedSubcatIds) ? $recommendedSubcatIds[$subcatIndex] : null;
            $subcatName = ! empty($recommendedModules) ? $recommendedModules[$subcatIndex] : 'General Info';

            $personalizedStudyPlan[] = [
                'day' => "Day {$day}",
                'tasks' => [
                    [
                        'focus_topic' => "Targeted study: {$subcatName}",
                        'activity' => "Spend 30 minutes reading the modules for {$subcatName} and complete 10 topic drills.",
                        'subcategory_id' => $subcatId,
                    ],
                ],
            ];
        }

        return $personalizedStudyPlan;
    }

    /**
     * Resolve the current learning and readiness stage based on volume-weighted score.
     */
    protected function resolveCurrentStage(int $avgScore): string
    {
        if ($avgScore >= 85) {
            return 'Practice 85+';
        }
        if ($avgScore >= 80) {
            return 'Practice 80–84';
        }
        if ($avgScore >= 70) {
            return 'Practice 70–79';
        }
        if ($avgScore >= 60) {
            return 'Practice 60–69';
        }

        return 'Practice under 60';
    }

    protected function normalizeCategory(string $catName): string
    {
        if (str_contains($catName, 'Verbal')) {
            return 'Verbal Ability';
        }
        if (str_contains($catName, 'Clerical')) {
            return 'Clerical Ability';
        }
        if (str_contains($catName, 'General')) {
            return 'General Information';
        }
        if (str_contains($catName, 'Numerical')) {
            return 'Numerical Ability';
        }
        if (str_contains($catName, 'Analytical')) {
            return 'Analytical Ability';
        }

        return $catName;
    }

    /**
     * Mock Accuracy for a user's latest track, computed from attempts.
     *
     * @return array<string, mixed>
     */
    public function mockAccuracyFor(int $userId): array
    {
        $latestId = (int) ExamAttempt::where('user_id', $userId)->latest('id')->value('id');
        $attempts = $latestId > 0 ? $this->resolveAttempts($userId, $latestId, false) : null;

        return $attempts ? $this->buildMockAccuracy($this->aggregateAttemptMetrics($attempts)) : $this->emptyMockAccuracy();
    }

    /**
     * Strip retired prediction fields from a stored (possibly legacy) analysis
     * and make sure it carries Mock Accuracy. Old rows may hold
     * pass_probability, days_to_readiness, estimated_exam_score and
     * mock_pass_confidence; none of them may reach a learner.
     *
     * @return array<string, mixed>|null
     */
    public function sanitizeStored(mixed $data, int $userId): ?array
    {
        if (! is_array($data)) {
            return null;
        }

        unset($data['pass_probability']);

        if (isset($data['predictive_metrics']) && is_array($data['predictive_metrics'])) {
            unset(
                $data['predictive_metrics']['days_to_readiness'],
                $data['predictive_metrics']['estimated_exam_score'],
                $data['predictive_metrics']['mock_pass_confidence'],
            );
        }

        if (! isset($data['mock_accuracy']) || ! is_array($data['mock_accuracy'])) {
            $data['mock_accuracy'] = $this->mockAccuracyFor($userId);
        }

        return $data;
    }

    /** @return array<string, mixed> */
    public function emptyMockAccuracy(): array
    {
        $zero = ['correct' => 0, 'total' => 0, 'mocks' => 0, 'percent' => null];

        return array_merge($zero, [
            'tracks' => [],
            'representative' => $zero,
            'personalized' => array_merge($zero, ['legacy' => 0]),
            'note' => 'Practice accuracy on submitted Civio mocks. Not an official rating or a pass prediction.',
        ]);
    }

    protected function getEmptyAnalysis(): array
    {
        return [
            'mock_accuracy' => $this->emptyMockAccuracy(),
            'verdict' => $this->pickTemplate('verdict_empty', []),
            'trend' => 'insufficient_data',
            'strengths' => [],
            'critical_weaknesses' => [],
            'priority_action' => $this->pickTemplate('priority_action_empty', []),
            'recommended_modules' => [],
            'encouragement' => $this->pickTemplate('encouragement_empty', []),
            'predictive_metrics' => [
                'completion_pace' => 'N/A',
            ],
            'subject_mastery' => array_map(fn ($s) => [
                'subject' => $s,
                'rating' => 'Insufficient Data',
                'color' => 'sky',
                'insight' => $this->pickTemplate('insight_no_data', ['subject' => $s]),
                'recommended_action' => $this->pickTemplate('action_no_data', ['subject' => $s]),
            ], $this->categories),
            'timeline_prediction' => [
                'current_stage' => 'No practice yet',
                'milestone_prediction' => $this->pickTemplate('milestone_empty', []),
                'potential_score_improvement' => $this->pickTemplate('improvement_empty', []),
            ],
            'remediation_matrix' => [],
            'personalized_study_plan' => [],
        ];
    }

    /**
     * Select a random template from a keyed pool and interpolate variables.
     */
    protected function pickTemplate(string $key, array $vars): string
    {
        $pool = $this->getTemplatePool($key);

        if ($pool->isEmpty()) {
            return '';
        }

        $template = $pool->random();

        foreach ($vars as $name => $value) {
            $template = str_replace("{{$name}}", (string) $value, $template);
        }

        return $template;
    }

    /**
     * Centralized template pools for all dynamic text.
     *
     * @return Collection<int, string>
     */
    protected function getTemplatePool(string $key): Collection
    {
        $pools = [
            // ── Verdicts ───────────────────────────────────────────
            'verdict_high' => [
                'Across {totalAttempts} attempts your practice average is {avgScore}%. {daysUntilExam} days remain until the date you set. That is not a pass forecast.',
                'Practice average {avgScore}% after {totalAttempts} attempts. The published general passing rating is at least 80.00. This average is not that rating.',
                'With {totalAttempts} attempts your practice average is {avgScore}%. Civio does not forecast a pass.',
                '{totalAttempts} attempts, practice average {avgScore}%. That number is not a Civil Service Commission rating.',
            ],
            'verdict_mid' => [
                'After {totalAttempts} attempts your practice average is {avgScore}%. The subjects you missed most: {weakList}.',
                'Practice average {avgScore}%, with {daysUntilExam} days until the date you set. Drill {weakList} if you want more items there.',
                'Your practice average is {avgScore}% after {totalAttempts} attempts. That is not a prediction you will pass.',
                'Practice average {avgScore}%. Before {examDateStr}, the subjects with more misses are {weakList}.',
                'Practice average {avgScore}%. A higher score on {weakList} here is still not an official rating.',
            ],
            'verdict_low' => [
                'Practice average {avgScore}% after {totalAttempts} attempts. The subjects with more misses: {weakList}.',
                'Practice average {avgScore}%. {daysUntilExam} days remain until the date you set. That is not a forecast.',
                '{totalAttempts} attempts, practice average {avgScore}%. The published general passing rating is at least 80.00. This average is not that rating.',
                'Practice average {avgScore}% before {examDateStr}. Misses are concentrated in {weakList}.',
                'Practice average {avgScore}%. A higher score here is still not an official rating.',
            ],
            'verdict_empty' => [
                'No attempts yet. A mock or a drill will show a practice score.',
                'There is no practice score until you finish a mock or a drill.',
                'Finish one mock or one drill. The score is a practice score, not a forecast.',
            ],
            'verdict_no_mock' => [
                'You have drill scores and no full mock yet. A mock is 150 or 145 scored items. Civio does not calculate an official pass probability.',
                'Drill scores are in. They are not a pass forecast. A full mock is the timed 150-item or 145-item set.',
                'Finish a Professional or Subprofessional mock if you want a timed practice score. That score is not an official result.',
            ],

            // ── Encouragement (by score tier + trend) ─────────────
            'encouragement_high' => [
                'Practice average is in the high band. It is not an official rating.',
                'Recent practice is in the high band. The next mock is a separate score.',
                'A high practice average is still a practice score.',
                'The published general passing rating is at least 80.00. This band is not that rating.',
            ],
            'encouragement_high_improving' => [
                'The last mocks are higher than the ones before them. That is a practice trend, not a forecast.',
                'Practice scores moved up. The next mock can still move either way.',
            ],
            'encouragement_high_declining' => [
                'The last mocks are lower than the ones before them. That is a practice trend, not a forecast.',
                'A lower recent mock is one result. It does not change the published passing rating.',
            ],
            'encouragement_mid' => [
                'Practice average is in the middle band. It is not a prediction you will pass.',
                'Middle-band practice. The published general passing rating is at least 80.00.',
                'More items in the subjects you missed will change this average. It will still be a practice score.',
                'This band is a practice average, not an official result.',
            ],
            'encouragement_mid_improving' => [
                'Recent practice scores are higher than earlier ones. That is not a pass forecast.',
                'The practice trend is up. The next mock is a separate score.',
            ],
            'encouragement_mid_declining' => [
                'Recent practice scores are lower than earlier ones. Check the subjects you missed.',
                'The practice trend is down. A drill on the missed subjects is the next step, not a forecast.',
            ],
            'encouragement_low' => [
                'Practice average is in the low band. The missed subjects are listed on this page.',
                'A low practice average is a count of misses. It is not an official rating.',
                'One subject at a time is enough. The score after that drill is still a practice score.',
                'The subjects with more misses are named above. That list is from your attempts, not from CSC.',
            ],
            'encouragement_low_improving' => [
                'Recent practice scores are higher than earlier ones. The average is still a practice score.',
                'The practice trend is up from a low average. It is not a forecast.',
            ],
            'encouragement_low_declining' => [
                'Recent practice scores are lower than earlier ones. Start with the subject you missed most.',
                'The practice trend is down. A short drill is a practice score, not a forecast.',
            ],
            'encouragement_empty' => [
                'Finish a mock or a drill to see a practice score.',
                'There is no score until an attempt is submitted.',
                'A mock is 150 or 145 scored items. A drill is one subject.',
            ],

            // ── Priority Actions ──────────────────────────────────
            'priority_action' => [
                'A 30-minute drill on {topModule} covers the subject with more misses.',
                'Open a {topModule} drill if you want more items from that subject.',
                'Ten {topModule} items is one way to add practice there.',
                'Today\'s misses are concentrated in {topModule}.',
            ],
            'priority_action_none' => [
                'A drill adds a practice score. It does not forecast a pass.',
                'Finish a drill to see which items you missed.',
                'A mock is the timed 150-item or 145-item set.',
            ],
            'priority_action_empty' => [
                'Finish a mock or a drill to see a practice score.',
                'A short drill is enough to start a practice record.',
                'Pick one subject and finish a drill.',
            ],

            // ── Subject Mastery Insights ──────────────────────────
            'insight_no_data' => [
                'No {subject} items yet.',
                '{subject} has no submitted items.',
                'A {subject} drill would add the first score for this subject.',
            ],
            'insight_mastered' => [
                '{subject} practice accuracy is {pct}%. That is not an official rating.',
                '{pct}% of your {subject} items were correct. This is a practice count.',
                'You can spend the next session on another subject. {subject} is at {pct}% in practice.',
                '{subject} is the higher practice score at {pct}%.',
            ],
            'insight_moderate' => [
                '{subject} practice accuracy is {pct}%.',
                '{pct}% of your {subject} items were correct.',
                'A {subject} drill adds items to this {pct}% practice score.',
                '{pct}% in {subject} is a practice count, not a point total on the exam.',
            ],
            'insight_critical' => [
                '{subject} practice accuracy is {pct}%. More of these items were missed.',
                '{subject} is at {pct}% in practice. That is the lower score on this page.',
                '{pct}% of your {subject} items were correct.',
                '{subject} is at {pct}%. A drill there changes this practice count only.',
            ],

            // ── Subject Mastery Recommended Actions ───────────────
            'action_no_data' => [
                'Start with a short {subject} drill.',
                'A {subject} drill records the first score for this subject.',
                'Ten {subject} items is enough for a first count.',
            ],
            'action_mastered' => [
                'A timed {subject} drill checks pace. The Professional mock allows about 76 seconds an item.',
                'One {subject} review a week keeps the practice count current.',
                'Harder {subject} items are in the drill filters.',
                'A short timed {subject} set is optional. It is not required by CSC.',
            ],
            'action_moderate' => [
                'A medium {subject} drill adds items to this practice count.',
                'Twenty minutes on the {subject} notes, then a drill, is one session.',
                'The {subject} subtopics you missed are the ones to drill.',
                'Two or three {subject} drills this week change this practice count only.',
            ],
            'action_critical' => [
                'A {subject} drill is a smaller set than a full mock.',
                'Read the {subject} notes, then a short drill.',
                'Split {subject} into subtopics and drill one.',
                'The next few sessions can stay on {subject}. The score is still a practice score.',
            ],

            // ── Remediation: Struggle Reasons ────────────────────
            'struggle_reason_hard' => [
                'More {subtopic} items were missed than the other subtopics.',
                'Both speed and accuracy are lower on {subtopic} items.',
                '{subtopic} items are missed more often than the rest.',
                '{subtopic} shows up often among the missed items.',
            ],
            'struggle_reason_medium' => [
                '{subtopic} items are sometimes missed.',
                '{subtopic} is correct on some items and missed on others.',
                '{subtopic} results are mixed across attempts.',
                '{subtopic} accuracy is not stable yet.',
            ],

            // ── Remediation: Coaching Tips ───────────────────────
            'coaching_hard' => [
                'Ten {subtopic} items, accuracy before speed.',
                'Read the {subtopic} notes, then drill. 80% here is a practice target, not an official cutoff.',
                'Split {subtopic} into smaller sets.',
                'Fifteen minutes on the {subtopic} notes, then ten items.',
            ],
            'coaching_medium' => [
                'Read the {subtopic} notes, then a drill.',
                'Five easier {subtopic} items, then a medium set.',
                'Save missed {subtopic} items and drill them again.',
                'A short {subtopic} note, then a timed drill. About 76 seconds an item on the Professional mock.',
            ],

            // ── Completion Pace (by trend) ──────────────────────
            'completion_pace_improving' => [
                'The last three practice scores are higher than the earlier ones. {totalAttempts} attempts are in this summary.',
                'Recent practice scores went up. That describes these attempts only.',
            ],
            'completion_pace_declining' => [
                'The last three practice scores are lower than the earlier ones. {totalAttempts} attempts are in this summary.',
                'Recent practice scores went down. That describes these attempts only.',
            ],
            'completion_pace_stable' => [
                '{totalAttempts} attempts are in this summary. The recent scores did not move by more than 5 points.',
                'Recent practice scores stayed within 5 points. That is not a forecast.',
            ],
            'completion_pace_insufficient_data' => [
                'Fewer than three scores, so no practice trend yet.',
                'Not enough finished attempts to compare scores.',
            ],

            // ── Milestone Predictions ────────────────────────────
            'milestone_high' => [
                'Your recent practice is the score you have. Civio does not forecast the exam on {examDateStr}.',
                'Keep the subjects you already answer correctly. That is not a prediction you will pass.',
                'The date you set is {examDateStr}. A practice score is not the exam result.',
            ],
            'milestone_mid' => [
                'Drill {weakList}. Civio will not estimate how many points that adds.',
                'More items on {weakList} will change this practice average. It will not certify a pass.',
                'By {examDateStr} you can finish more mocks. The average here is not a passing forecast.',
            ],
            'milestone_low' => [
                'The misses are concentrated. Drill those subjects. Civio does not promise a point gain.',
                'A low practice average means those items were missed. It does not predict the next score.',
                'Use the time before the exam on the subjects you miss. No point gain is guaranteed.',
            ],
            'milestone_empty' => [
                'Finish a mock to see a practice score.',
                'A drill or a mock has to be finished before there is a score to show.',
            ],
            'improvement_high' => [
                'Civio does not estimate a future point gain.',
                'Another timed mock will show a new practice score. It is not a forecast.',
                'The next score is the next score. This page will not add points in advance.',
            ],
            'improvement_mid' => [
                'Civio does not estimate a future point gain.',
                'Drill the subjects you miss, then take another mock if you want a new average.',
                'No percentage gain is promised for the next two weeks.',
            ],
            'improvement_low' => [
                'Civio does not estimate a future point gain.',
                'A low average is the items missed so far. It is not a forecast of the exam.',
                'Another mock replaces this average. It does not guarantee a higher one.',
            ],
            'improvement_empty' => [
                'There is no score to improve yet.',
                'Finish a mock before treating any number as a baseline.',
            ],
        ];

        return collect($pools[$key] ?? []);
    }
}
