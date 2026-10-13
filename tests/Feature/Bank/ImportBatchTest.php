<?php

use App\Models\Question;

test('batch 001 imports as active civio items, keyed, and re-running changes nothing', function () {
    $path = base_path('docs/batches/batch-001.json');

    $this->artisan('civio:import-batch', ['path' => $path])
        ->expectsOutputToContain('Imported 10 item(s): 10 created, 0 updated.')
        ->assertSuccessful();

    expect(Question::count())->toBe(10)
        ->and(Question::where('status', 'active')->where('source_group', 'civio')->count())->toBe(10)
        ->and(Question::where('offline_eligible', true)->count())->toBe(0);

    $q = Question::where('stem', 'like', 'A barangay will split%')->firstOrFail();
    expect($q->options[$q->correct_option])->toBe('₱10,000')
        ->and($q->subcategory->category->name)->toBe('Numerical Ability')
        ->and($q->explanation)->toContain('Shortcut:')->not->toMatch('/\b[ABCD]\)/');

    $spell = Question::where('stem', 'Which word is misspelled?')->firstOrFail();
    expect($spell->options[$spell->correct_option])->toBe('ocassion');

    $this->artisan('civio:import-batch', ['path' => $path])
        ->expectsOutputToContain('0 created, 10 updated.')
        ->assertSuccessful();
    expect(Question::count())->toBe(10);
});

test('dry run saves nothing and a bad file fails', function () {
    $this->artisan('civio:import-batch', ['path' => base_path('docs/batches/batch-001.json'), '--dry-run' => true])
        ->expectsOutputToContain('Validated 10 item(s)')
        ->assertSuccessful();
    expect(Question::count())->toBe(0);

    $bad = tempnam(sys_get_temp_dir(), 'batch');
    file_put_contents($bad, json_encode(['items' => [['id' => 'X', 'domain' => 'numerical', 'competency' => 'Word problems', 'stem' => 'S?', 'options' => [['option_id' => 'a', 'text' => '1']], 'answer_option_id' => 'a', 'reveal' => ['shortcut' => 'x']]]]));
    $this->artisan('civio:import-batch', ['path' => $bad])->assertFailed();
    expect(Question::count())->toBe(0);
});

test('imported items stay out of offline packs, so the offline caps still hold', function () {
    $this->artisan('civio:import-batch', ['path' => base_path('docs/batches/batch-001.json')])->assertSuccessful();

    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    expect(Question::where('offline_eligible', true)->count())->toBe(0);
});

test('a generated batch imports as drafts with --status=draft, all 100 items, none active', function () {
    $path = base_path('docs/batches/batch-002.json');

    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'draft'])
        ->expectsOutputToContain('Imported 100 item(s): 100 created, 0 updated.')
        ->assertSuccessful();

    expect(Question::where('status', 'draft')->count())->toBe(100)
        ->and(Question::where('status', 'active')->count())->toBe(0);

    $filing = Question::where('stem', 'like', 'In alphabetical filing%')->firstOrFail();
    expect($filing->explanation)->toContain('ARMA International Simplified Filing Standard Rules, Rule')
        ->toContain('not a rule published by the CSC');

    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'bogus'])->assertFailed();
});

test('generated unreviewed items cannot be activated even when the operator omits draft mode', function () {
    $path = base_path('docs/batches/batch-002.json');

    $this->artisan('civio:import-batch', ['path' => $path])
        ->expectsOutputToContain('active import requires status=approved and review_status=passed')
        ->assertFailed();

    expect(Question::count())->toBe(0)
        ->and(Question::where('status', 'active')->count())->toBe(0);

    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'draft'])
        ->assertSuccessful();

    expect(Question::where('status', 'draft')->count())->toBe(100)
        ->and(Question::where('status', 'active')->count())->toBe(0);
});
