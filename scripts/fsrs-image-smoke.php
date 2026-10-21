<?php

declare(strict_types=1);

/**
 * Production-image check. Proves Node and ts-fsrs survive the image build,
 * a signed-in miss stores a due time, a later independent correct moves it,
 * and a scheduler failure stays visible until a later try saves it.
 *
 * Run after the application is bootstrapped with sqlite. See scripts/fsrs-image-smoke.sh.
 */

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\ReviewCard;
use App\Models\ReviewEvent;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\Exam\ReviewMistakeRecorder;
use App\Services\Exam\ReviewScheduleApplier;
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\Process;

foreach ([
    'APP_ENV' => 'local',
    'APP_DEBUG' => 'true',
    'APP_URL' => 'http://localhost',
    'DB_CONNECTION' => 'sqlite',
    'DB_DATABASE' => '/tmp/civio-smoke.sqlite',
    'CACHE_STORE' => 'array',
    'SESSION_DRIVER' => 'array',
    'QUEUE_CONNECTION' => 'sync',
    'LOG_CHANNEL' => 'stderr',
    'CIVIO_FSRS_NODE' => 'node',
] as $name => $value) {
    putenv($name.'='.$value);
    $_ENV[$name] = $value;
    $_SERVER[$name] = $value;
}

if ((getenv('APP_KEY') ?: '') === '') {
    fwrite(STDERR, "APP_KEY is required.\n");
    exit(1);
}

require __DIR__.'/../vendor/autoload.php';
$app = require __DIR__.'/../bootstrap/app.php';
$kernel = $app->make(Kernel::class);
$kernel->bootstrap();

function smokeFail(string $message): never
{
    fwrite(STDERR, $message."\n");
    exit(1);
}

if (PHP_MAJOR_VERSION !== 8 || PHP_MINOR_VERSION !== 4) {
    smokeFail('PHP 8.4 is required in the production image. Found '.PHP_VERSION);
}

if (! extension_loaded('sodium')) {
    smokeFail('sodium is missing from the production image.');
}

$node = Process::timeout(5)->run(['node', '-v']);
$nodeVersion = trim($node->output());

if (! $node->successful() || ! str_starts_with($nodeVersion, 'v22.')) {
    smokeFail('Node 22 was not retained. Found: '.$nodeVersion.$node->errorOutput());
}

if (is_file('/usr/local/bin/npm') || is_file('/usr/bin/npm')) {
    smokeFail('npm must not remain in the production image.');
}

$nodeModules = array_values(array_diff(scandir(base_path('node_modules')) ?: [], ['.', '..']));

if ($nodeModules !== ['ts-fsrs']) {
    smokeFail('node_modules must contain only ts-fsrs. Found: '.implode(', ', $nodeModules));
}

$kernel->call('migrate', ['--force' => true]);

function smokeQuestion(User $user, string $stem): Question
{
    $category = Category::query()->create([
        'name' => 'Numerical '.$stem,
        'slug' => 'numerical-'.substr(sha1($stem), 0, 12),
        'is_demographic' => false,
    ]);
    $subcategory = Subcategory::query()->create([
        'category_id' => $category->id,
        'name' => 'Basic',
        'slug' => 'basic-'.substr(sha1($stem), 0, 12),
    ]);

    return Question::query()->create([
        'subcategory_id' => $subcategory->id,
        'language' => 'en',
        'stem' => $stem,
        'options' => ['12', '34', '56', '78'],
        'correct_option' => 1,
        'explanation' => 'Because 34.',
        'created_by' => $user->id,
        'status' => 'active',
    ])->load('subcategory.category');
}

function smokeAttempt(User $user, Question $question): ExamAttempt
{
    return ExamAttempt::query()->create([
        'user_id' => $user->id,
        'mode' => 'study',
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 0],
        'cat_scores' => [],
    ]);
}

$user = User::query()->create([
    'name' => 'Smoke',
    'email' => 'smoke@example.com',
    'password' => 'secret-secret',
    'role' => 'user',
]);
$question = smokeQuestion($user, 'Which value is larger?');
$recorder = app(ReviewMistakeRecorder::class);
$applier = app(ReviewScheduleApplier::class);
$attempt = smokeAttempt($user, $question);
$recorder->record($user->id, (int) $attempt->id, false, [$question->id => 0], new Collection([$question]));
$firstStatus = $applier->apply($user->id);

if ($firstStatus !== ReviewScheduleApplier::SAVED) {
    smokeFail('A wrong answer did not save a reminder. Status: '.$firstStatus);
}

$card = ReviewCard::query()->where('question_id', $question->id)->first();

if ($card === null || $card->due_at === null || $card->due_at->lessThanOrEqualTo(now())) {
    smokeFail('The wrong answer did not persist a future due time.');
}

$firstDue = $card->due_at->copy();
$correct = smokeAttempt($user, $question);
$recorder->record($user->id, (int) $correct->id, false, [$question->id => 1], new Collection([$question]));
$moved = $applier->apply($user->id);
$card->refresh();

if ($moved !== ReviewScheduleApplier::SAVED || $card->due_at->lessThanOrEqualTo($firstDue) || $card->last_rating !== 'good') {
    smokeFail('An independent correct answer did not move the due time.');
}

config(['civio.fsrs_node' => '/bin/false']);
$other = smokeQuestion($user, 'Which value is smaller?');
$missed = smokeAttempt($user, $other);
$recorder->record($user->id, (int) $missed->id, false, [$other->id => 0], new Collection([$other]));
$failed = $applier->apply($user->id);

if ($failed !== ReviewScheduleApplier::FAILED || ReviewCard::query()->where('question_id', $other->id)->exists()) {
    smokeFail('A scheduler failure looked saved.');
}

$event = ReviewEvent::query()->where('question_id', $other->id)->first();

if ($event === null || $event->scheduled || $event->rating !== 'again') {
    smokeFail('The failed reminder was not kept for a later try.');
}

config(['civio.fsrs_node' => 'node']);
$recovered = $applier->apply($user->id);
$recoveredCard = ReviewCard::query()->where('question_id', $other->id)->first();

if ($recovered !== ReviewScheduleApplier::SAVED || $recoveredCard === null || $recoveredCard->due_at->lessThanOrEqualTo(now())) {
    smokeFail('The reminder did not recover after the scheduler worked again.');
}

fwrite(STDOUT, 'php '.PHP_VERSION."\n");
fwrite(STDOUT, 'node '.$nodeVersion."\n");
fwrite(STDOUT, "sodium loaded\n");
fwrite(STDOUT, "fsrs image smoke passed\n");
