<?php

use App\Console\Commands\ImportBatchCommand;
use App\Models\Question;
use Illuminate\Support\Facades\DB;

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

test('self declared approved metadata cannot activate an unsigned batch', function () {
    $this->artisan('civio:import-batch', ['path' => base_path('docs/batches/batch-001.json')])->assertFailed();
    expect(Question::count())->toBe(0);
});

test('batch draft import cannot overwrite or demote an active bank row', function () {
    $path = base_path('docs/batches/batch-001.json');
    $this->artisan('civio:import-batch', ['path' => $path, ...bankSign($path, 'import-batch-active')])->assertSuccessful();
    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'draft'])->assertFailed();
    expect(Question::where('status', 'active')->count())->toBe(10);
});

test('changed batch revisions and duplicate option IDs fail without mutation', function (string $defect) {
    $batch = json_decode(file_get_contents(base_path('docs/batches/batch-001.json')), true);
    $path = bankJson($batch);
    $this->artisan('civio:import-batch', ['path' => $path, '--status' => 'draft'])->assertSuccessful();
    if ($defect === 'revision') {
        $batch['items'][0]['reveal']['why_correct'] = 'Changed explanation';
    } else {
        $batch['items'][1]['options'][1]['option_id'] = $batch['items'][1]['options'][0]['option_id'];
    }
    $this->artisan('civio:import-batch', ['path' => bankJson($batch), '--status' => 'draft'])->assertFailed();
    expect(Question::count())->toBe(10);
})->with(['revision', 'option-id']);

test('malformed batch item types fail cleanly', function (mixed $item) {
    $this->artisan('civio:import-batch', ['path' => bankJson(['items' => [$item]]), '--status' => 'draft'])->assertFailed();
    expect(Question::count())->toBe(0);
})->with([[null], ['text'], [['id' => 'x', 'domain' => ['bad']]]]);

test('an unchanged draft requires exact independently signed review before promotion', function () {
    $batch = json_decode(file_get_contents(base_path('docs/batches/batch-001.json')), true);
    foreach ($batch['items'] as &$item) {
        $item['status'] = 'draft';
        $item['review_status'] = 'unreviewed';
    }
    unset($item);
    $draft = bankJson($batch);
    $this->artisan('civio:import-batch', ['path' => $draft, '--status' => 'draft'])->assertSuccessful();
    $ids = Question::orderBy('id')->pluck('id')->all();
    foreach ($batch['items'] as &$item) {
        $item['status'] = 'approved';
        $item['review_status'] = 'passed';
    }
    unset($item);
    $approved = bankJson($batch);
    $this->artisan('civio:import-batch', ['path' => $approved])->assertFailed();
    expect(Question::where('status', 'active')->count())->toBe(0);
    $this->artisan('civio:import-batch', ['path' => $approved, ...bankSign($approved, 'import-batch-active')])->assertSuccessful();
    expect(Question::where('status', 'active')->count())->toBe(10)
        ->and(Question::orderBy('id')->pluck('id')->all())->toBe($ids)
        ->and(DB::table('bank_import_entries')->whereNotNull('approval_sha256')->count())->toBe(10);
});
