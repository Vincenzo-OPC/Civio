<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\ReviewEvent;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\Learning\LearningInsightsService;

function insightItems(string $cat, int $n): array
{
    $sub = Subcategory::factory()->create(['category_id' => Category::factory()->create(['name' => $cat, 'is_demographic' => false])->id]);

    return Question::factory()->count($n)->create(['subcategory_id' => $sub->id, 'status' => 'active', 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1])->pluck('id')->all();
}

function insightAttempt(User $user, array $ids, ExamMode $mode, array $answers, array $times = []): ExamAttempt
{
    return ExamAttempt::create(['user_id' => $user->id, 'mode' => $mode->value, 'question_ids' => $ids, 'answers' => $answers,
        'cat_scores' => ['categoryScoreMap' => [], 'metadata' => ['question_times' => $times]]]);
}

function assistedEvent(User $user, ExamAttempt $attempt, int $qid): void
{
    ReviewEvent::query()->insert(['user_id' => $user->id, 'question_id' => $qid, 'source_attempt_id' => $attempt->id, 'outcome' => 'assisted_correct',
        'assisted' => true, 'scheduled' => false, 'reviewed_at' => now(), 'scheduler_version' => 't', 'policy_version' => 't', 'created_at' => now()]);
}

test('an assisted correct answer never counts toward mastery', function () {
    $user = User::factory()->create();
    [$a, $b] = insightItems('Numerical Ability', 2);
    $attempt = insightAttempt($user, [$a, $b], ExamMode::Study, [(string) $a => 1, (string) $b => 1]);
    assistedEvent($user, $attempt, $b);

    $m = app(LearningInsightsService::class)->forUser($user->id)['mastery'];

    expect($m)->toBe([['name' => 'Numerical Ability', 'correct' => 1, 'total' => 1, 'percentage' => 100]]);
});

test('timed practice is suggested only at 30+ independent items and 80%+', function () {
    $user = User::factory()->create();
    $ids = insightItems('Verbal Ability', 30);
    $answers = [];
    foreach ($ids as $i => $id) {
        $answers[(string) $id] = $i < 24 ? 1 : 0; // 24/30 = 80%
    }
    insightAttempt($user, array_slice($ids, 0, 29), ExamMode::Strict, $answers);

    expect(app(LearningInsightsService::class)->forUser($user->id)['timedSuggestions'])->toBe([]);

    insightAttempt($user, [$ids[29]], ExamMode::Strict, [(string) $ids[29] => 1]);
    $out = app(LearningInsightsService::class)->forUser($user->id);

    expect($out['timedSuggestions'])->toBe(['Verbal Ability'])
        ->and(json_encode($out))->not->toContain('roficien');
});

test('pace is seconds per answered item by subject, skipping blanks', function () {
    $user = User::factory()->create();
    [$a, $b, $c] = insightItems('Clerical Ability', 3);
    insightAttempt($user, [$a, $b, $c], ExamMode::Study, [(string) $a => 1, (string) $b => 0, (string) $c => null], [0 => 40, 1 => 20, 2 => 90]);

    expect(app(LearningInsightsService::class)->forUser($user->id)['pace'])
        ->toBe([['name' => 'Clerical Ability', 'secondsPerItem' => 30.0, 'items' => 2]]);
});
