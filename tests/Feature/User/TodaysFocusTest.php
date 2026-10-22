<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;
use Inertia\Testing\AssertableInertia as Assert;

function focusSubject(string $name, int $n): array
{
    $sub = Subcategory::factory()->create(['category_id' => Category::factory()->create(['name' => $name, 'is_demographic' => false])->id]);

    return Question::factory()->count($n)->create(['subcategory_id' => $sub->id, 'status' => 'active', 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1])->pluck('id')->all();
}

function focusServed($response): array
{
    return collect($response->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all();
}

/** A Strict attempt with the given correct/total per subject, tagged with a track. */
function focusHistory(User $user, string $track, array $results): void
{
    $ids = [];
    $answers = [];
    foreach ($results as [$pool, $correct, $total]) {
        foreach (array_slice($pool, 0, $total) as $i => $id) {
            $ids[] = $id;
            $answers[(string) $id] = $i < $correct ? 1 : 0;
        }
    }
    ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Strict->value, 'question_ids' => $ids, 'answers' => $answers,
        'cat_scores' => ['categoryScoreMap' => [], 'metadata' => ['track' => $track]]]);
}

test('focus serves 15 from the weakest well-sampled subject then 10 mixed, unseen first, no keys, no duplicates', function () {
    $user = User::factory()->create();
    $num = focusSubject('Numerical Ability', 40);
    $ver = focusSubject('Verbal Ability', 40);
    $cle = focusSubject('Clerical Ability', 20);
    focusHistory($user, 'Subprofessional', [[$num, 2, 10], [$ver, 9, 10]]);

    $page = $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'focus_today' => '1']))->assertOk();
    $ids = focusServed($page);
    $focus = array_slice($ids, 0, 15);

    expect($ids)->toHaveCount(25)
        ->and(count(array_unique($ids)))->toBe(25)
        ->and(array_intersect($focus, $num))->toHaveCount(15)
        ->and(array_intersect($focus, array_slice($num, 0, 10)))->toBe([]) // 30 unseen exist, so no seen items
        ->and(array_intersect(array_slice($ids, 15), [...$ver, ...$cle]))->toHaveCount(10);
    $page->assertInertia(fn (Assert $p) => $p->missing('questions.0.correct_option'));
});

test('a subject with too few independent items is not ranked weakest', function () {
    $user = User::factory()->create();
    $num = focusSubject('Numerical Ability', 20);
    $ver = focusSubject('Verbal Ability', 20);
    // Numerical 0/3 (too few to judge), Verbal 6/10 (judged).
    focusHistory($user, 'Subprofessional', [[$num, 0, 3], [$ver, 6, 10]]);

    expect(app(ExamService::class)->todaysFocusSubject(['Numerical Ability', 'Verbal Ability'], $user->id))->toBe('Verbal Ability');
});

test('subject eligibility follows the level: no Analytical for Subprofessional, no Clerical for Professional', function () {
    expect(ExamService::focusSubjectsFor('Subprofessional'))->not->toContain('Analytical Ability')->toContain('Clerical Ability')
        ->and(ExamService::focusSubjectsFor('Professional'))->not->toContain('Clerical Ability')->toContain('Analytical Ability')
        ->and(ExamService::focusSubjectsFor(null))->not->toContain('Clerical Ability')->not->toContain('Analytical Ability');

    $user = User::factory()->create();
    $ana = focusSubject('Analytical Ability', 30);
    $num = focusSubject('Numerical Ability', 30);
    focusHistory($user, 'Subprofessional', [[$num, 9, 10]]);

    $ids = focusServed($this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'focus_today' => '1'])));
    expect(array_intersect($ids, $ana))->toBe([]);
});

test('a guest gets a weekday rotation over shared subjects only', function () {
    focusSubject('Numerical Ability', 20);
    $cle = focusSubject('Clerical Ability', 20);
    $ids = focusServed($this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'focus_today' => '1']))->assertOk());

    expect(array_intersect($ids, $cle))->toBe([]);
});

test('the drills page passes the learner level to the focus launcher, and an explicit track wins', function () {
    $user = User::factory()->create();
    $ana = focusSubject('Analytical Ability', 30);
    $cle = focusSubject('Clerical Ability', 30);
    focusHistory($user, 'Professional', [[$ana, 9, 10]]);

    $this->actingAs($user)->withoutVite()->get(route('drills.index'))
        ->assertInertia(fn (Assert $p) => $p->where('focusLevel', 'Professional'));

    $ids = focusServed($this->get(route('exams.index', ['drill' => 'true', 'focus_today' => '1', 'track' => 'Subprofessional'])));
    expect(array_intersect($ids, $ana))->toBe([]);
    expect(array_intersect($ids, $cle))->not->toBe([]);
});
