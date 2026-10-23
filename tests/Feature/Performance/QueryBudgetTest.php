<?php

use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;

/*
 * Issue #27: database work per request on a typical learner session.
 *
 * Runs with the production-like database session and cache drivers so the
 * session, rate-limit and cache writes are counted too. Budgets are query
 * counts (deterministic), not timings. Set PERF_QUERY_REPORT=path to write
 * the measured numbers as JSON for docs/PERFORMANCE_REPORT.md. Budgets are
 * the measured counts plus a little headroom; raise one only on purpose.
 */

function seedPerfBank(int $perCategory = 45): void
{
    $author = User::factory()->create();
    foreach (['Verbal Ability' => 50, 'Analytical Ability' => 55, 'Numerical Ability' => 48, 'General Information' => 10] as $name => $n) {
        $category = Category::factory()->create(['name' => $name, 'is_demographic' => false]);
        $sub = Subcategory::factory()->create(['category_id' => $category->id]);
        for ($i = 0; $i < max($n, $perCategory); $i++) {
            Question::factory()->create([
                'subcategory_id' => $sub->id,
                'created_by' => $author->id,
                'status' => 'active',
                'language' => ($name === 'Verbal Ability' && $i % 2) ? 'fil' : 'en',
                'stem' => "{$name} perf item {$i}: which is correct?",
                'options' => ["A{$i}", "B{$i}", "C{$i}", "D{$i}"],
                'correct_option' => 1,
            ]);
        }
    }
}

beforeEach(function () {
    config(['session.driver' => 'database', 'cache.default' => 'database']);
});

test('a guest strict-mock session stays within its query budget', function () {
    seedPerfBank();
    $report = [];
    $budget = [];

    // Each closure is one HTTP request in a typical session. DB::listen keeps
    // every listener, so counts are taken as deltas from a single listener.
    $log = [];
    DB::listen(function (QueryExecuted $e) use (&$log) {
        preg_match('/^\s*(\w+)/', $e->sql, $m);
        $log[] = ['kind' => strtolower($m[1] ?? ''), 'sql' => $e->sql];
        if (env('PERF_QUERY_SQL')) {
            fwrite(STDERR, $e->sql."\n");
        }
    });
    $step = function (string $label, int $max, callable $fn) use (&$log, &$report, &$budget) {
        $start = count($log);
        $fn();
        $slice = array_slice($log, $start);
        $report[$label] = [
            'total' => count($slice),
            'reads' => count(array_filter($slice, fn ($q) => $q['kind'] === 'select')),
            'writes' => count(array_filter($slice, fn ($q) => $q['kind'] !== 'select')),
            'bank_queries' => count(array_filter($slice, fn ($q) => str_contains($q['sql'], 'from "questions"'))),
        ];
        $budget[$label] = $max;
    };

    $step('GET /exams (setup page)', 17, fn () => $this->get('/exams')->assertOk());
    $sessionId = null;
    $ids = [];
    $step('POST /exams/sessions (start strict mock)', 16, function () use (&$sessionId, &$ids) {
        $r = $this->postJson(route('exams.sessions.store'), ['track' => 'professional', 'mode' => 'strict'])->assertOk();
        $sessionId = $r->json('session_id');
        $ids = collect($r->json('questions'))->pluck('id')->all();
    });
    expect(count($ids))->toBeGreaterThanOrEqual(150);

    $version = 0;
    $step('POST /exams/sessions/progress (one answer)', 11, function () use ($sessionId, $ids, &$version) {
        $r = $this->postJson(route('exams.sessions.progress'), [
            'exam_session_id' => $sessionId,
            'answers' => [(string) $ids[0] => 1],
            'expected_version' => $version,
        ])->assertOk();
        $version = $r->json('save_version');
    });
    $step('POST /exams/attempts (submit 150)', 22, function () use ($sessionId, $ids) {
        $this->postJson(route('exams.attempts.store'), [
            'exam_session_id' => $sessionId,
            'question_ids' => $ids,
            'answers' => collect($ids)->mapWithKeys(fn ($id) => [(string) $id => 1])->all(),
            'metadata' => ['track' => 'Professional', 'duration_secs' => 600, 'is_timed' => true],
        ])->assertOk();
    });
    $step('GET /dashboard (guest)', 8, fn () => $this->get('/dashboard')->assertOk());
    $step('GET /drills (guest)', 11, fn () => $this->get('/drills')->assertOk());

    if ($path = env('PERF_QUERY_REPORT')) {
        file_put_contents($path, json_encode($report, JSON_PRETTY_PRINT));
    }

    // The setup page shows no items, so it must not load the bank (Issue #27).
    expect($report['GET /exams (setup page)']['bank_queries'])->toBe(0);

    foreach ($report as $label => $q) {
        expect($q['total'])->toBeLessThanOrEqual($budget[$label], "{$label}: {$q['total']} queries");
    }
});
