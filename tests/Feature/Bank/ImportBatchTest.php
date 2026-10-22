<?php

use App\Console\Commands\ImportBatchCommand;
use App\Models\Question;

require_once __DIR__.'/../../Support/BankApprovalFixtures.php';

test('batch 001 imports as active civio items, keyed, and re-running changes nothing', function () {
    $path = base_path('docs/batches/batch-001.json');

    $this->artisan('civio:import-batch', ['path' => $path, ...bankSign($path, 'import-batch-active')])
        ->expectsOutputToContain('Imported 10 item(s): 10 inserted or promoted, 0 unchanged.')
        ->assertSuccessful();

    expect(Question::count())->toBe(10)
        ->and(Question::where('status', 'active')->where('source_group', 'civio')->count())->toBe(10)
        ->and(Question::where('offline_eligible', true)->count())->toBe(0);

    $q = Question::where('stem', 'like', 'A barangay will split%')->firstOrFail();
    expect($q->options[$q->correct_option])->toBe('₱10,000')
        ->and($q->subcategory->category->name)->toBe('Numerical Ability')
        ->and($q->explanation)->toContain('Shortcut:')->not->toMatch('/\b[ABCD]\)/');

    $spell = Question::where('stem', 'like', 'Which word is misspelled?%')->firstOrFail();
    expect($spell->options[$spell->correct_option])->toBe('aquire');

    $this->artisan('civio:import-batch', ['path' => $path, ...bankSign($path, 'import-batch-active')])
        ->expectsOutputToContain('0 inserted or promoted, 10 unchanged.')
        ->assertSuccessful();
    expect(Question::count())->toBe(10);
});

test('dry run saves nothing and a bad file fails', function () {
    $this->artisan('civio:import-batch', ['path' => base_path('docs/batches/batch-001.json'), '--dry-run' => true, ...bankSign(base_path('docs/batches/batch-001.json'), 'import-batch-active')])
        ->expectsOutputToContain('Validated 10 item(s)')
        ->assertSuccessful();
    expect(Question::count())->toBe(0);

    $bad = tempnam(sys_get_temp_dir(), 'batch');
    file_put_contents($bad, json_encode(['items' => [['id' => 'X', 'domain' => 'numerical', 'competency' => 'Word problems', 'stem' => 'S?', 'options' => [['option_id' => 'a', 'text' => '1']], 'answer_option_id' => 'a', 'reveal' => ['shortcut' => 'x']]]]));
    $this->artisan('civio:import-batch', ['path' => $bad])->assertFailed();
    expect(Question::count())->toBe(0);
});

test('imported items stay out of offline packs, so the offline caps still hold', function () {
    $this->artisan('civio:import-batch', ['path' => base_path('docs/batches/batch-001.json'), ...bankSign(base_path('docs/batches/batch-001.json'), 'import-batch-active')])->assertSuccessful();

    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    expect(Question::where('offline_eligible', true)->count())->toBe(0);
});

test('a generated batch imports as drafts with --status=draft, all 100 items, none active', function () {
    $path = base_path('docs/batches/batch-002.json');

    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'draft'])
        ->expectsOutputToContain('Imported 100 item(s): 100 inserted or promoted, 0 unchanged.')
        ->assertSuccessful();

    expect(Question::where('status', 'draft')->count())->toBe(100)
        ->and(Question::where('status', 'active')->count())->toBe(0);

    $filing = Question::where('stem', 'like', 'In alphabetical filing%')->firstOrFail();
    expect($filing->explanation)->toContain('ARMA International Simplified Filing Standard Rules, Rule')
        ->toContain('not a rule published by the CSC');

    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'bogus'])->assertFailed();
});

test('generated unreviewed items cannot be activated even when the operator omits draft mode', function () {
    // batch-002 is now CoS-approved, so rebuild an unreviewed copy of it as the fixture.
    $batch = json_decode(file_get_contents(base_path('docs/batches/batch-002.json')), true);
    foreach ($batch['items'] as &$item) {
        $item['status'] = 'draft';
        $item['review_status'] = 'unreviewed';
        $item['reviewer'] = null;
        $item['reviewed_at'] = null;
    }
    unset($item);
    $path = tempnam(sys_get_temp_dir(), 'unreviewed-batch-');
    file_put_contents($path, json_encode($batch));

    $this->artisan('civio:import-batch', ['path' => $path, ...bankSign($path, 'import-batch-active')])
        ->expectsOutputToContain('active import requires status=approved and review_status=passed')
        ->assertFailed();

    expect(Question::count())->toBe(0)
        ->and(Question::where('status', 'active')->count())->toBe(0);

    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'draft'])
        ->assertSuccessful();

    expect(Question::where('status', 'draft')->count())->toBe(100)
        ->and(Question::where('status', 'active')->count())->toBe(0);
});

test('an optional item-level shortcut leads the Reveal and the worked steps follow as Method', function () {
    $item = json_decode(file_get_contents(base_path('docs/batches/batch-001.json')), true)['items'][0];
    $texts = array_column($item['options'], 'text', 'option_id');
    unset($item['shortcut']);

    $plain = ImportBatchCommand::explanation($item, $texts);
    expect($plain)->toContain('Shortcut: '.$item['reveal']['shortcut'])->not->toContain('Method:');

    $item['shortcut'] = 'Chain the changes as multipliers: ₱250 × 1.2 × 0.8 = ₱240.';
    $with = ImportBatchCommand::explanation($item, $texts);
    expect($with)->toContain("Shortcut: {$item['shortcut']}\nMethod: {$item['reveal']['shortcut']}");
});

test('fact_id and theme tags are saved, and an untagged re-import keeps them', function () {
    $source = base_path('docs/batches/batch-001.json');
    $data = json_decode((string) file_get_contents($source), true);
    $data['items'][0]['fact_id'] = 'FACT-TEST-0001';
    $data['items'][0]['theme'] = 'test-theme';
    $tagged = tempnam(sys_get_temp_dir(), 'batch');
    file_put_contents($tagged, json_encode($data));

    $this->artisan('civio:import-batch', ['path' => $tagged, ...bankSign($tagged, 'import-batch-active')])->assertSuccessful();

    $q = Question::where('stem', $data['items'][0]['stem'])->firstOrFail();
    expect($q->fact_id)->toBe('FACT-TEST-0001')
        ->and($q->theme)->toBe('test-theme')
        ->and(Question::whereNull('fact_id')->count())->toBe(9);

    $this->artisan('civio:import-batch', ['path' => $source, ...bankSign($source, 'import-batch-active')])->assertSuccessful();

    expect($q->fresh()->fact_id)->toBe('FACT-TEST-0001')
        ->and($q->fresh()->theme)->toBe('test-theme');
});
