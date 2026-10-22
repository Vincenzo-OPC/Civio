<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\OfflinePracticeResult;
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

test('an idle item cannot skew pace beyond the per-item cap', function () {
    $user = User::factory()->create();
    [$a, $b] = insightItems('Numerical Ability', 2);
    insightAttempt($user, [$a, $b], ExamMode::Study, [(string) $a => 1, (string) $b => 1], [0 => 60, 1 => 5000]);

    expect(app(LearningInsightsService::class)->forUser($user->id)['pace'][0]['secondsPerItem'])
        ->toEqual((60 + LearningInsightsService::MAX_ITEM_SECONDS) / 2);
});

test('independent accuracy matches a hand count across Strict, unassisted and assisted practice', function () {
    $user = User::factory()->create();
    $ids = insightItems('Numerical Ability', 6);
    // Strict: 2/3 correct (always counts). Study: 1 correct unassisted, 1 wrong assisted, 1 correct assisted.
    insightAttempt($user, array_slice($ids, 0, 3), ExamMode::Strict, [(string) $ids[0] => 1, (string) $ids[1] => 1, (string) $ids[2] => 0]);
    $study = insightAttempt($user, array_slice($ids, 3, 3), ExamMode::Study, [(string) $ids[3] => 1, (string) $ids[4] => 0, (string) $ids[5] => 1]);
    assistedEvent($user, $study, $ids[4]);
    assistedEvent($user, $study, $ids[5]);

    expect(app(LearningInsightsService::class)->forUser($user->id)['mastery'][0])
        ->toMatchArray(['correct' => 3, 'total' => 4, 'percentage' => 75]);
});

test('weak-skill progression ranks building skills first and never says mastered', function () {
    $user = User::factory()->create();
    $weak = insightItems('Numerical Ability', 10);
    $strong = insightItems('Verbal Ability', 20);
    $answers = [];
    foreach ($weak as $i => $id) {
        $answers[(string) $id] = $i < 3 ? 1 : 0; // 30%
    }
    foreach ($strong as $id) {
        $answers[(string) $id] = 1; // 100% over 20
    }
    insightAttempt($user, [...$weak, ...$strong], ExamMode::Strict, $answers);

    $skills = app(LearningInsightsService::class)->forUser($user->id)['skills'];

    expect($skills[0])->toMatchArray(['subject' => 'Numerical Ability', 'stage' => 'building', 'percentage' => 30])
        ->and(collect($skills)->firstWhere('subject', 'Verbal Ability')['stage'])->toBe('timed')
        ->and(json_encode($skills))->not->toMatch('/master|proficien/i');
});

test('retention needs enough day-apart re-checks and counts kept items', function () {
    $user = User::factory()->create();
    $ids = insightItems('Clerical Ability', 10);
    $first = array_fill_keys(array_map('strval', $ids), 1);
    $again = $first;
    $again[(string) $ids[0]] = 0;
    $again[(string) $ids[1]] = 0;

    $a = insightAttempt($user, $ids, ExamMode::Strict, $first);
    $a->forceFill(['created_at' => now()->subDays(3)])->save();
    expect(app(LearningInsightsService::class)->forUser($user->id)['retention'])->toBeNull();

    insightAttempt($user, $ids, ExamMode::Strict, $again);
    expect(app(LearningInsightsService::class)->forUser($user->id)['retention'])
        ->toBe(['checked' => 10, 'kept' => 8, 'percentage' => 80]);
});

test('a same-day repeat does not count as retention', function () {
    $user = User::factory()->create();
    $ids = insightItems('Clerical Ability', 10);
    $answers = array_fill_keys(array_map('strval', $ids), 1);
    insightAttempt($user, $ids, ExamMode::Strict, $answers);
    insightAttempt($user, $ids, ExamMode::Strict, $answers);

    expect(app(LearningInsightsService::class)->forUser($user->id)['retention'])->toBeNull();
});

test('nextFocus uses only independent answers on archetype-tagged items', function () {
    $user = User::factory()->create();
    $ids = insightItems('Numerical Ability', 8);
    Question::whereIn('id', $ids)->update(['archetype' => 'NUM-WP-PCT-CHANGE']);
    $wrong = [];
    foreach ($ids as $id) {
        $wrong[(string) $id] = 0;
    }

    // Six wrong Strict answers on the tagged skill: weak, enough evidence.
    insightAttempt($user, array_slice($ids, 0, 6), ExamMode::Strict, array_slice($wrong, 0, 6, true));
    $focus = app(LearningInsightsService::class)->forUser($user->id)['nextFocus'];

    expect($focus['skill'])->toBe('NUM-OPS-ORDER')
        ->and($focus['basedOn'])->toBe('0 of 6 independent answers correct in Percent change, discounts and markups');

    // Assisted answers add nothing to the evidence.
    $attempt = insightAttempt($user, array_slice($ids, 6, 2), ExamMode::Study, [(string) $ids[6] => 1, (string) $ids[7] => 1]);
    assistedEvent($user, $attempt, $ids[6]);
    assistedEvent($user, $attempt, $ids[7]);

    expect(app(LearningInsightsService::class)->forUser($user->id)['nextFocus']['basedOn'])
        ->toBe('0 of 6 independent answers correct in Percent change, discounts and markups');
});

test('nextFocus is null when no item carries a graph archetype', function () {
    $user = User::factory()->create();
    $ids = insightItems('Numerical Ability', 6);
    insightAttempt($user, $ids, ExamMode::Strict, array_fill_keys(array_map('strval', $ids), 0));

    expect(app(LearningInsightsService::class)->forUser($user->id)['nextFocus'])->toBeNull();
});

test('skill evidence: blanks are not wrong, repeats do not inflate, offline answers count with their time', function () {
    $user = User::factory()->create();
    $ids = insightItems('Numerical Ability', 6);
    Question::whereIn('id', $ids)->update(['archetype' => 'NUM-WP-PCT-CHANGE']);
    $skill = fn () => collect(app(LearningInsightsService::class)->forUser($user->id)['skillEvidence'])->firstWhere('skill', 'NUM-WP-PCT-CHANGE');

    // Six blanks: no wrong evidence, no recommendation.
    insightAttempt($user, $ids, ExamMode::Strict, []);
    expect($skill())->toMatchArray(['independent' => 0, 'unanswered' => 6, 'status' => 'insufficient'])
        ->and(app(LearningInsightsService::class)->forUser($user->id)['nextFocus'])->toBeNull();

    // The same two questions answered correctly three times: two independent answers, four repeats.
    foreach ([1, 2, 3] as $_) {
        insightAttempt($user, array_slice($ids, 0, 2), ExamMode::Strict, [(string) $ids[0] => 1, (string) $ids[1] => 1]);
    }
    expect($skill())->toMatchArray(['independent' => 2, 'repeats' => 4, 'status' => 'insufficient']);

    // Accepted offline answers to three new questions reach five distinct answers.
    foreach (array_slice($ids, 2, 3) as $i => $qid) {
        OfflinePracticeResult::create(['owner_key' => 'u'.$user->id, 'user_id' => $user->id, 'client_id' => 'c'.$i,
            'question_id' => $qid, 'selected_option' => 0, 'claimed_correct_option' => 1, 'is_correct' => false,
            'status' => 'accepted', 'source' => 'offline_practice', 'pack_version' => 't', 'answered_at' => now()->subHour()]);
    }
    expect($skill())->toMatchArray(['independent' => 5, 'status' => 'estimate'])
        ->and(array_keys($skill()))->not->toContain('estimate');
});
