<?php

use App\Models\User;
use Illuminate\Auth\Events\Login;

test('guest can access the exams page', function () {
    $response = $this->get(route('exams.index', ['free_attempt' => '1']));

    $response->assertOk();
});

test('guest can POST to exams/attempts', function () {
    $response = $this->postJson(route('exams.attempts.store'), [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 0,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ]);

    $response->assertOk();
    $response->assertJson(['success' => true]);
});

test('authenticated user can POST to exams/attempts', function () {
    $user = User::factory()->create();
    $this->actingAs($user);

    $response = $this->postJson(route('exams.attempts.store'), [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 0,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ]);

    $response->assertOk();
    $response->assertJson(['success' => true]);
});

test('guest attempt is claimed by user upon registration or login', function () {
    $response = $this->postJson(route('exams.attempts.store'), [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 0,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ]);

    $response->assertOk();
    $attemptId = $response->json('attempt_id');
    expect($attemptId)->not->toBeNull();

    $this->assertDatabaseHas('exam_attempts', [
        'id' => $attemptId,
        'user_id' => null,
    ]);

    $user = User::factory()->create();
    event(new Login('web', $user, false));

    $this->assertDatabaseHas('exam_attempts', [
        'id' => $attemptId,
        'user_id' => $user->id,
    ]);
});

test('incomplete guest attempt is rejected', function () {
    $response = $this->postJson(route('exams.attempts.store'), [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => null, 3 => 1], // Incomplete
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 1,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ]);

    $response->assertStatus(422);
    $response->assertJson(['success' => false]);
});

test('guest can submit another mock when practice is unlimited', function () {
    $payload = [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 0,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ];

    $this->postJson(route('exams.attempts.store'), $payload)->assertOk();
    $this->postJson(route('exams.attempts.store'), $payload)->assertOk()->assertJson(['success' => true]);
});

test('guest is not locked on the scorecard when practice is unlimited', function () {
    $this->postJson(route('exams.attempts.store'), [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 0,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ])->assertOk();

    $this->get(route('exams.index', ['free_attempt' => '1']))->assertOk();
});

test('guest second mock is blocked when unlimited practice is off', function () {
    config(['civio.guest_unlimited' => false]);

    $payload = [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'category_name' => 'Professional Level Reviewer',
                'correct_count' => 2,
                'total_questions' => 3,
                'skipped_count' => 0,
                'duration_secs' => 180,
                'is_timed' => true,
            ],
        ],
    ];

    $this->postJson(route('exams.attempts.store'), $payload)->assertOk();

    $this->postJson(route('exams.attempts.store'), $payload)
        ->assertStatus(403)
        ->assertJson(['success' => false]);
});

test('guest is redirected to the scorecard when unlimited practice is off', function () {
    config(['civio.guest_unlimited' => false]);

    $this->withSession(['pending_guest_attempt_id' => 123])
        ->get(route('exams.index', ['free_attempt' => '1']))
        ->assertRedirect(route('exams.index', ['attempt_id' => 123, 'limit' => '1']));
});
