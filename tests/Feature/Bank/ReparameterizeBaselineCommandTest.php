<?php

use App\Enums\QuestionSourceGroup;
use App\Enums\QuestionStatus;
use App\Models\Question;
use App\Services\Bank\BankApproval;
use App\Services\Bank\BankContent;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Event;

require_once __DIR__.'/../../Support/BankApprovalFixtures.php';

beforeEach(function () {
    $this->original = Question::factory()->create([
        'source_group' => QuestionSourceGroup::Baseline, 'status' => 'active',
        'stem' => 'Synthetic original fixture', 'options' => ['One', 'Two', 'Three', 'Four'],
        'correct_option' => 0,
    ]);
    $this->rows = [[
        'id' => 'TEST-REPLACEMENT-1', 'prior_stem' => $this->original->stem,
        'original_sha256' => BankContent::fingerprint($this->original),
        'stem' => 'Synthetic replacement fixture', 'language' => 'English',
        'options' => ['First', 'Second', 'Third', 'Fourth'], 'correct_option' => 1,
        'explanation' => 'Synthetic explanation for regression only.',
    ]];
});

function runReplacements(array $rows, array $options = [], bool $sign = true): mixed
{
    $path = bankJson($rows);
    $approval = $sign ? bankSign($path) : [];

    return test()->artisan('civio:reparameterize-baseline', ['--path' => $path, ...$approval, ...$options]);
}

test('reviewed replacement imports atomically and an exact rerun writes nothing', function () {
    $path = bankJson($this->rows);
    $args = ['--path' => $path, ...bankSign($path)];
    $this->artisan('civio:reparameterize-baseline', [...$args, '--dry-run' => true])->assertSuccessful();
    expect(Question::count())->toBe(1)->and(DB::table('bank_import_entries')->count())->toBe(0);
    $this->artisan('civio:reparameterize-baseline', $args)->expectsOutputToContain('Inserted: 1')->assertSuccessful();
    $replacement = Question::where('replaces_question_id', $this->original->id)->firstOrFail();
    expect($this->original->fresh()->status)->toBe(QuestionStatus::Draft)
        ->and($replacement->status)->toBe(QuestionStatus::Active)
        ->and($replacement->correct_option)->toBe(1);
    $this->artisan('civio:reparameterize-baseline', $args)->expectsOutputToContain('unchanged: 1')->assertSuccessful();
    expect(Question::count())->toBe(2)->and(DB::table('bank_import_entries')->count())->toBe(1);
});

test('all rows must validate before any mutation in dry run and apply', function (bool $dry) {
    $this->rows[] = ['id' => 'malformed'];
    runReplacements($this->rows, ['--dry-run' => $dry])->assertFailed();
    expect(Question::count())->toBe(1)->and($this->original->fresh()->status)->toBe(QuestionStatus::Active);
})->with([false, true]);

test('invalid replacement fields fail closed', function (string $field, mixed $value) {
    $this->rows[0][$field] = $value;
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe(1);
})->with([
    ['correct_option', '1'], ['correct_option', 4], ['options', ['A', ' a ', 'B', 'C']],
    ['options', ['', 'B', 'C', 'D']], ['explanation', ''], ['id', ''], ['language', 'xx'],
    ['original_sha256', str_repeat('0', 64)],
]);

test('duplicate identities sources and normalized stems are rejected', function (string $duplicate) {
    $second = $this->rows[0];
    $second['id'] = 'TEST-REPLACEMENT-2';
    $second['stem'] = 'Different fixture';
    $second['prior_stem'] = 'Other original';
    $second[$duplicate] = $this->rows[0][$duplicate];
    $this->rows[] = $second;
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe(1);
})->with(['id', 'stem', 'prior_stem']);

test('nonbaseline or ambiguous baseline sources cannot be selected', function (bool $ambiguous) {
    if ($ambiguous) {
        Question::factory()->create(['source_group' => 'baseline', 'stem' => $this->original->stem]);
    } else {
        $this->original->update(['source_group' => 'civio']);
    }
    $count = Question::count();
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe($count);
})->with([false, true]);

test('missing signed authorization cannot be replaced by self approval fields', function () {
    $this->rows[0]['approved'] = true;
    runReplacements($this->rows, [], false)->assertFailed();
    expect(Question::count())->toBe(1);
});

test('approval content tampering expired records self review and untrusted keys fail', function (string $defect) {
    $path = bankJson($this->rows);
    $overrides = match ($defect) {
        'expired' => ['expires_at' => '2000-01-01T00:00:00Z'],
        'self-review' => ['reviewer' => ' TEST-AUTHOR '],
        default => [],
    };
    $args = bankSign($path, 'replace-baseline', $overrides);
    match ($defect) {
        'manifest' => file_put_contents($path, file_get_contents($path).' '),
        'report' => file_put_contents($args['--review-report'], 'tampered'),
        'record' => file_put_contents($args['--approval'], str_replace('test-author', 'other-author', file_get_contents($args['--approval']))),
        'signature' => file_put_contents($args['--approval'].'.sig', 'malformed'),
        'key' => config(['bank.approval_public_key' => null]),
        default => null,
    };
    $this->artisan('civio:reparameterize-baseline', ['--path' => $path, ...$args])->assertFailed();
    expect(Question::count())->toBe(1)->and(DB::table('bank_import_entries')->count())->toBe(0);
})->with(['manifest', 'report', 'record', 'signature', 'key', 'expired', 'self-review']);

test('a later source mismatch rejects the complete manifest', function () {
    $other = Question::factory()->create(['source_group' => 'baseline', 'status' => 'active']);
    $second = $this->rows[0];
    $second['id'] = 'TEST-2';
    $second['stem'] = 'Other replacement';
    $second['prior_stem'] = $other->stem;
    $second['original_sha256'] = str_repeat('0', 64);
    $this->rows[] = $second;
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe(2)->and($this->original->fresh()->status)->toBe(QuestionStatus::Active);
});

test('a failure during the second write rolls back originals ledger and replacements', function () {
    $other = Question::factory()->create(['source_group' => 'baseline', 'status' => 'active']);
    $second = $this->rows[0];
    $second['id'] = 'TEST-2';
    $second['stem'] = 'Second replacement';
    $second['prior_stem'] = $other->stem;
    $second['original_sha256'] = BankContent::fingerprint($other);
    $this->rows[] = $second;
    Event::listen('eloquent.creating: '.Question::class, function (Question $question) {
        if ($question->stem === 'Second replacement') {
            throw new RuntimeException('Synthetic write failure.');
        }
    });
    Cache::put('questions.active', 'sentinel');
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe(2)->and(DB::table('bank_import_entries')->count())->toBe(0)
        ->and($this->original->fresh()->status)->toBe(QuestionStatus::Active)
        ->and($other->fresh()->status)->toBe(QuestionStatus::Active)
        ->and(Cache::get('questions.active'))->toBe('sentinel');
});

test('existing replacement content is immutable even with a newly signed manifest', function () {
    runReplacements($this->rows)->assertSuccessful();
    $this->rows[0]['explanation'] = 'Changed fixture';
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe(2)
        ->and(Question::where('replaces_question_id', $this->original->id)->first()->explanation)->not->toBe('Changed fixture');
});

test('existing bank stem collisions and database drift fail without overwriting', function (string $defect) {
    if ($defect === 'collision') {
        Question::factory()->create(['stem' => '  SYNTHETIC replacement fixture  ']);
    } else {
        runReplacements($this->rows)->assertSuccessful();
        Question::where('replaces_question_id', $this->original->id)->update(['explanation' => 'External edit']);
    }
    runReplacements($this->rows)->assertFailed();
    expect(Question::count())->toBe(2);
})->with(['collision', 'drift']);

test('invalid UTF-8 and nonlist JSON cannot mutate the bank', function () {
    foreach (["[\"\xff\"]", '{}', '[]'] as $content) {
        $this->artisan('civio:reparameterize-baseline', ['--path' => bankArtifact($content)])->assertFailed();
    }
    expect(Question::count())->toBe(1);
});

test('real OpenSSH generated approval verifies with no SSH executable at runtime', function () {
    $fixture = json_decode(file_get_contents(base_path('tests/Fixtures/bank-approval-openssh.json')), true, 512, JSON_THROW_ON_ERROR);
    $record = bankArtifact($fixture['record']);
    file_put_contents($record.'.sig', $fixture['signature']);
    register_shutdown_function(static fn () => is_file($record.'.sig') ? unlink($record.'.sig') : null);
    config(['bank.approval_public_key' => $fixture['public_key']]);
    app(BankApproval::class)->verify('interop-manifest', 'replace-baseline', $record, bankArtifact('interop-review'));
    expect(true)->toBeTrue();
});
