<?php

use App\Models\Category;
use App\Models\Question;
use App\Models\User;

function guestSubmit($test)
{
    return $test->postJson(route('exams.attempts.store'), [
        'category_id' => null,
        'question_ids' => [1, 2, 3],
        'answers' => [1 => 0, 2 => 2, 3 => 1],
        'cat_scores' => ['categoryScoreMap' => [], 'metadata' => [
            'track' => 'Professional', 'category_name' => 'Professional Level Reviewer',
            'correct_count' => 2, 'total_questions' => 3, 'skipped_count' => 0, 'duration_secs' => 180, 'is_timed' => true,
        ]],
    ]);
}

beforeEach(function () {
    Question::factory()->count(3)->create(['status' => 'active']);
    Category::query()->update(['is_demographic' => false]);
    config(['civio.guest_unlimited' => false]);
    $this->withoutVite();
});

test('query params cannot reset a used guest free attempt', function (array $query) {
    $this->get(route('exams.index', ['free_attempt' => '1', 'drill' => 'true', 'custom_question_ids' => '[1,2,3]']))->assertOk();
    guestSubmit($this)->assertOk();

    $this->get(route('exams.index', $query))->assertRedirect();
    $this->get(route('exams.index', ['free_attempt' => '1', 'drill' => 'true', 'custom_question_ids' => '[1,2,3]']));

    guestSubmit($this)->assertStatus(403);
})->with([
    'start' => [['start' => '1']],
    'free_attempt' => [['free_attempt' => '1']],
    'start + free_attempt' => [['start' => '1', 'free_attempt' => '1']],
]);

test('a guest who used the free attempt cannot open new mock sessions', function () {
    $this->withSession(['pending_guest_attempt_id' => 1])
        ->postJson(route('exams.sessions.store'), ['track' => 'Professional'])
        ->assertStatus(403);
});

test('signed-in users can still start fresh', function () {
    $this->actingAs(User::factory()->create())
        ->withSession(['pending_guest_attempt_id' => 99])
        ->get(route('exams.index', ['start' => '1']))->assertOk();
});

test('guest unlimited (local study) still lets guests start again', function () {
    config(['civio.guest_unlimited' => true]);
    $this->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => '[1,2,3]']))->assertOk();
    guestSubmit($this)->assertOk();
    $this->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => '[1,2,3]']))->assertOk();
    guestSubmit($this)->assertOk();
});

test('production does not default to unlimited guests', function () {
    $load = function (string $env): bool {
        $old = [getenv('APP_ENV'), getenv('CIVIO_GUEST_UNLIMITED')];
        putenv('APP_ENV='.$env);
        putenv('CIVIO_GUEST_UNLIMITED');
        unset($_ENV['CIVIO_GUEST_UNLIMITED'], $_SERVER['CIVIO_GUEST_UNLIMITED']);
        $_ENV['APP_ENV'] = $_SERVER['APP_ENV'] = $env;
        try {
            return (bool) (require base_path('config/civio.php'))['guest_unlimited'];
        } finally {
            putenv('APP_ENV='.$old[0]);
            $_ENV['APP_ENV'] = $_SERVER['APP_ENV'] = (string) $old[0];
        }
    };

    expect($load('production'))->toBeFalse()
        ->and($load('staging'))->toBeFalse()
        ->and($load('local'))->toBeTrue();
});
