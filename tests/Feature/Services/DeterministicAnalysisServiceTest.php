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

    expect($result)->not->toHaveKey('pass_probability')
        ->and($result['mock_accuracy']['mocks'])->toBe(0)
        ->and($result['mock_accuracy']['percent'])->toBeNull()
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
        'mock_accuracy',
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
        ->and($result)->not->toHaveKey('pass_probability')
        ->and($result['mock_accuracy']['correct'])->toBe(1)
        ->and($result['mock_accuracy']['total'])->toBe(1)
        ->and($result['mock_accuracy']['percent'])->toEqual(100)
        ->and($result['mock_accuracy']['tracks'])->toBe(['Professional'])
        ->and($result['timeline_prediction']['current_stage'])->toBe('Practice 85+')
        ->and(collect($result['subject_mastery'])->pluck('rating')->all())->not->toContain('Critical Concern')
        ->and(collect($result['subject_mastery'])->pluck('rating')->all())->not->toContain('Mastered')
        ->and($result['predictive_metrics']['completion_pace'])->not->toContain('accelerat');
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
        ->and($resultMulti['mock_accuracy']['mocks'])->toBe(0)
        ->and($resultMulti['mock_accuracy']['percent'])->toBeNull();

    // Single attempt evaluation
    $resultSingle = $service->generate($user->id, $attempt1->id, singleAttemptOnly: true);
    expect($resultSingle['verdict'])->toBeString()
        ->and($resultSingle['strengths'])->toContain('Verbal Ability');
});
