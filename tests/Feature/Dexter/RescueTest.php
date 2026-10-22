<?php

use App\Models\Category;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/** @return array{failed: Question, others: list<Question>} */
function rescueBank(int $others = 1, string $archetype = 'NUM-WP-PCT-CHANGE'): array
{
    $sub = Subcategory::factory()->create(['category_id' => Category::factory()->create(['name' => 'Numerical Ability', 'is_demographic' => false])->id, 'name' => 'Word problems']);
    $make = fn (int $i) => Question::factory()->create([
        'subcategory_id' => $sub->id, 'status' => 'active', 'archetype' => $archetype,
        'stem' => "A price rose from 200 to 250 (case {$i}). What is the percent increase?",
        'options' => ['20%', '25%', '50%', '125%'], 'correct_option' => 1,
        'explanation' => 'Change 50 divided by the original 200 is 25%.',
        'distractor_codes' => ['0' => 'NUM-WRONG-BASE', '2' => 'NUM-PARTIAL', '3' => 'NUM-PCT-ADD'],
    ]);

    return ['failed' => $make(0), 'others' => $others > 0 ? array_map($make, range(1, $others)) : []];
}

function rescueOn(array $validated = []): void
{
    config(['dexter_rescue.enabled' => true, 'dexter_rescue.validated_question_ids' => $validated]);
}

test('gate off (default): 404 and nothing about the item', function () {
    $bank = rescueBank();
    expect(config('dexter_rescue.enabled'))->toBeFalse();

    $body = $this->actingAs(User::factory()->create())
        ->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])
        ->assertNotFound()->assertExactJson(['enabled' => false])->getContent();

    expect($body)->not->toContain('NUM-');
});

test('gate on, unvalidated metadata: checked explanation, no diagnosis claimed, no code leaked', function () {
    $bank = rescueBank();
    rescueOn();

    $res = $this->actingAs(User::factory()->create())
        ->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])->assertOk();

    expect($res->json('rescue.state'))->toBe('explained')
        ->and($res->json('rescue.diagnosis'))->toBeNull()
        ->and($res->json('rescue.explanation.source'))->toBe('checked_explanation')
        ->and($res->getContent())->not->toContain('NUM-WRONG-BASE');
});

test('gate on, validated metadata: the reviewed code becomes a diagnosis', function () {
    $bank = rescueBank();
    rescueOn([$bank['failed']->id]);

    $res = $this->actingAs(User::factory()->create())
        ->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])->assertOk();

    expect($res->json('rescue.diagnosis.code'))->toBe('NUM-WRONG-BASE')
        ->and($res->json('rescue.explanation.source'))->toBe('validated_diagnosis');
});

test('an active Strict Mock blocks Rescue with 423 and no details', function () {
    $bank = rescueBank();
    rescueOn([$bank['failed']->id]);
    $user = User::factory()->create();
    ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict',
        'question_ids' => [$bank['others'][0]->id], 'started_at' => now(), 'deadline_at' => now()->addHour()]);

    $body = $this->actingAs($user)->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])
        ->assertStatus(423)->getContent();

    expect(array_keys(json_decode($body, true)))->toBe(['locked', 'message'])
        ->and($body)->not->toContain('NUM-')
        ->and($body)->not->toContain('diagnosis');
});

test('no fresh question available gives an honest fallback', function () {
    $bank = rescueBank(0);
    rescueOn();

    $this->actingAs(User::factory()->create())
        ->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])
        ->assertOk()->assertJsonPath('rescue.next.kind', 'none');
});

test('the fresh question is a different item of the same skill, served without key or codes', function () {
    $bank = rescueBank(1);
    rescueOn();

    $res = $this->actingAs(User::factory()->create())
        ->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])->assertOk();

    expect($res->json('rescue.next.kind'))->toBe('fresh_same_skill')
        ->and($res->json('rescue.next.question.id'))->toBe($bank['others'][0]->id)
        ->and($res->json('rescue.next.question'))->not->toHaveKey('correct_option')
        ->and($res->json('rescue.next.question'))->not->toHaveKey('distractor_codes')
        ->and($res->json('rescue.next.question'))->not->toHaveKey('explanation');
});

test('outside the pilot skills or on a correct answer Rescue stays idle', function () {
    $bank = rescueBank(1, 'NUM-WP-RATE');
    rescueOn([$bank['failed']->id]);
    $user = User::factory()->create();

    $this->actingAs($user)->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0])
        ->assertOk()->assertExactJson(['rescue' => ['state' => 'idle', 'skill' => null]]);
});

test('guests cannot use Rescue (auth.or.fail answers 404)', function () {
    $bank = rescueBank();
    rescueOn();

    $this->withoutExceptionHandling();

    expect(fn () => $this->postJson(route('dexter.rescue'), ['question_id' => $bank['failed']->id, 'chosen_option' => 0]))
        ->toThrow(NotFoundHttpException::class);
});
