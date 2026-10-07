<?php

use App\Enums\QuestionSourceGroup;
use App\Http\Resources\DrillQuestionResource;
use App\Http\Resources\ExamQuestionResource;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Support\Facades\DB;

function rawSeedRow(Subcategory $sub, User $user, array $overrides = []): int
{
    return DB::table('questions')->insertGetId(array_merge([
        'subcategory_id' => $sub->id,
        'language' => 'English',
        'stem' => 'Raw seed stem '.fake()->unique()->numberBetween(1, 99999),
        'options' => json_encode(['A', 'B', 'C', 'D']),
        'correct_option' => 0,
        'explanation' => 'Seeded.',
        'status' => 'active',
        'created_by' => $user->id,
        'created_at' => now(),
        'updated_at' => now(),
    ], $overrides));
}

test('questions created through the app are tagged civio', function () {
    $question = Question::factory()->create();

    expect($question->fresh()->source_group)->toBe(QuestionSourceGroup::Civio);
});

test('seed scripts can tag their items as baseline', function () {
    $question = Question::factory()->create(['source_group' => QuestionSourceGroup::Baseline]);

    expect($question->fresh()->source_group)->toBe(QuestionSourceGroup::Baseline);
});

test('civio:tag-source-groups tags raw SQL seed rows as baseline and is idempotent', function () {
    $sub = Subcategory::factory()->create();
    $user = User::factory()->create();
    $raw = rawSeedRow($sub, $user);
    $authored = Question::factory()->create(['subcategory_id' => $sub->id]);

    $this->artisan('civio:tag-source-groups --dry-run')
        ->expectsOutputToContain('Would tag 1 untagged question(s)')
        ->assertSuccessful();
    expect(DB::table('questions')->where('id', $raw)->value('source_group'))->toBeNull();

    $this->artisan('civio:tag-source-groups')
        ->expectsOutputToContain('Tagged 1 untagged question(s)')
        ->assertSuccessful();
    expect(DB::table('questions')->where('id', $raw)->value('source_group'))->toBe('baseline')
        ->and($authored->fresh()->source_group)->toBe(QuestionSourceGroup::Civio);

    $this->artisan('civio:tag-source-groups')
        ->expectsOutputToContain('Tagged 0 untagged question(s)')
        ->assertSuccessful();
});

test('the migration tags existing rows: baseline-era items baseline, later drafts civio', function () {
    $migration = require database_path('migrations/2026_10_07_000100_add_source_group_to_questions_table.php');
    $migration->down();

    $sub = Subcategory::factory()->create();
    $user = User::factory()->create();
    $before = '2026-10-04 12:00:00';
    $after = '2026-10-07 12:00:00';

    $baselineActive = rawSeedRow($sub, $user, ['created_at' => $before]);
    $baselineDraft = rawSeedRow($sub, $user, ['status' => 'draft', 'created_at' => $before]);
    $seededToday = rawSeedRow($sub, $user, ['created_at' => $after]);
    $customDraft = rawSeedRow($sub, $user, ['status' => 'draft', 'created_at' => $after]);

    $migration->up();

    $groups = DB::table('questions')->pluck('source_group', 'id');

    expect($groups[$baselineActive])->toBe('baseline')
        ->and($groups[$baselineDraft])->toBe('baseline')
        ->and($groups[$seededToday])->toBe('baseline')
        ->and($groups[$customDraft])->toBe('civio');
});

test('source_group never reaches exam or drill payloads', function () {
    $question = Question::factory()->create();
    $payload = json_encode([
        (new ExamQuestionResource($question))->resolve(),
        (new DrillQuestionResource($question))->resolve(),
    ]);

    expect($payload)->not->toContain('source_group');
});
