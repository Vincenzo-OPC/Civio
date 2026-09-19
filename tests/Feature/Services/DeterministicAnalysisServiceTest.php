<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\DeterministicAnalysisService;

test('it returns empty analysis when user has no exam attempts', function () {
    $user = User::factory()->create();
    $service = new DeterministicAnalysisService;

    $result = $service->generate($user->id, 99999);

    expect($result['pass_probability'])->toBe(0)
        ->and($result['trend'])->toBe('insufficient_data')
        ->and($result['strengths'])->toBeEmpty()
        ->and($result['critical_weaknesses'])->toBeEmpty()
        ->and($result['subject_mastery'])->toHaveCount(5);
});

test('it generates full deterministic analysis with mock exam attempts', function () {
    $user = User::factory()->create();

    $category = Category::create([
        'name' => 'Numerical Ability',
        'slug' => 'numerical-ability',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Fractions',
        'slug' => 'fractions',
    ]);

    $question = Question::factory()->create([
        'subcategory_id' => $subcategory->id,
        'correct_option' => 0,
    ]);

    $attempt = ExamAttempt::create([
        'user_id' => $user->id,
        'category_id' => null,
        'question_ids' => [$question->id],
        'answers' => [$question->id => 0],
        'cat_scores' => [
            'categoryScoreMap' => [
                'Numerical Ability' => ['correct' => 1, 'total' => 1],
            ],
            'metadata' => [
                'track' => 'Professional',
                'correct_count' => 1,
                'total_questions' => 1,
            ],
        ],
    ]);

    $service = new DeterministicAnalysisService;
    $result = $service->generate($user->id, $attempt->id);

    expect($result)->toHaveKeys([
        'pass_probability',
        'verdict',
        'trend',
        'strengths',
        'critical_weaknesses',
        'priority_action',
        'recommended_modules',
        'encouragement',
        'predictive_metrics',
        'subject_mastery',
        'timeline_prediction',
        'remediation_matrix',
        'personalized_study_plan',
    ])
        ->and($result['personalized_study_plan'])->toHaveCount(7)
        ->and($result['pass_probability'])->toBeGreaterThan(0);
});

test('it handles drill attempts and singleAttemptOnly option correctly', function () {
    $user = User::factory()->create();

    $category = Category::create([
        'name' => 'Verbal Ability',
        'slug' => 'verbal-ability',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Grammar',
        'slug' => 'grammar',
    ]);

    $question = Question::factory()->create([
        'subcategory_id' => $subcategory->id,
        'correct_option' => 0,
    ]);

    $attempt1 = ExamAttempt::create([
        'user_id' => $user->id,
        'category_id' => $category->id,
        'question_ids' => [$question->id],
        'answers' => [$question->id => 0],
        'cat_scores' => [
            'metadata' => [
                'track' => 'Drill',
                'category_name' => 'Verbal Ability',
                'correct_count' => 1,
                'total_questions' => 1,
            ],
        ],
    ]);

    $attempt2 = ExamAttempt::create([
        'user_id' => $user->id,
        'category_id' => $category->id,
        'question_ids' => [$question->id],
        'answers' => [$question->id => 1],
        'cat_scores' => [
            'metadata' => [
                'track' => 'Drill',
                'category_name' => 'Verbal Ability',
                'correct_count' => 0,
                'total_questions' => 1,
            ],
        ],
    ]);

    $service = new DeterministicAnalysisService;

    // Normal multi-attempt evaluation
    $resultMulti = $service->generate($user->id, $attempt2->id, singleAttemptOnly: false);
    expect($resultMulti['verdict'])->toBeString()
        ->and($resultMulti['predictive_metrics']['estimated_exam_score'])->toBe('Complete a Mock Exam to unlock score prediction');

    // Single attempt evaluation
    $resultSingle = $service->generate($user->id, $attempt1->id, singleAttemptOnly: true);
    expect($resultSingle['verdict'])->toBeString()
        ->and($resultSingle['strengths'])->toContain('Verbal Ability');
});
