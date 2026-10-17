<?php

declare(strict_types=1);

use App\Models\Category;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

function seedPdfItems(): array
{
    $category = Category::factory()->create(['name' => 'Numerical Ability', 'is_demographic' => false]);
    $sub = Subcategory::factory()->create(['category_id' => $category->id]);

    return collect(range(0, 3))->map(fn (int $key) => Question::factory()->create([
        'subcategory_id' => $sub->id,
        'status' => 'active',
        'offline_eligible' => false,
        'stem' => "Export fixture {$key}",
        'options' => ["First {$key}", "Second {$key}", "Third {$key}", "Fourth {$key}"],
        'correct_option' => $key,
    ]))->all();
}

test('authorized PDF keys match stored choices in every answer position without creating a session', function (string $role) {
    $items = seedPdfItems();
    $user = User::factory()->create(['role' => $role, 'can_download_pdf' => $role !== 'admin']);
    $response = $this->actingAs($user)->postJson(route('exams.exportPdf'), ['track' => 'Professional'])->assertOk();
    expect($response->headers->get('Cache-Control'))->toContain('no-store');
    $questions = $response->json('questions');
    expect($questions)->toHaveCount(4);
    $letters = [];
    foreach ($questions as $question) {
        $stored = Question::findOrFail($question['id']);
        expect($question['options'])->toBe($stored->options)
            ->and($question['correct_option'])->toBe($stored->correct_option)
            ->and($question['options'][$question['correct_option']])->toBe($stored->options[$stored->correct_option]);
        $letters[] = chr(65 + $question['correct_option']);
    }
    sort($letters);
    expect($letters)->toBe(['A', 'B', 'C', 'D'])
        ->and(ExamSession::count())->toBe(0);
})->with(['user', 'admin']);

test('ordinary mock payload continues to withhold all keys for PDF-enabled users', function () {
    seedPdfItems();
    $this->actingAs(User::factory()->create(['can_download_pdf' => true]));
    $questions = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional'])->assertOk()->json('questions');
    expect($questions)->toHaveCount(4);
    foreach ($questions as $question) {
        expect($question)->not->toHaveKey('correct_option')->not->toHaveKey('explanation');
    }
});

test('PDF export rejects guests and unauthorized users even with an invented token', function () {
    $this->postJson(route('exams.exportPdf'), ['track' => 'Professional'])->assertStatus(404);
    $this->actingAs(User::factory()->create(['can_download_pdf' => false]))
        ->postJson(route('exams.exportPdf'), ['track' => 'Professional', 'export_token' => str_repeat('a', 40)])
        ->assertForbidden()->assertJsonMissingPath('questions');
});

test('PDF export rejects arbitrary item and session selection', function (array $extra) {
    $this->actingAs(User::factory()->create(['role' => 'admin', 'can_download_pdf' => false]))
        ->postJson(route('exams.exportPdf'), ['track' => 'Professional', ...$extra])
        ->assertUnprocessable()->assertJsonMissingPath('questions');
})->with([[['question_ids' => [1]]], [['exam_session_id' => 'invented']], [['track' => 'invalid']]]);

test('PDF export cannot bypass an active strict mock including guest sessions after login', function (bool $guest) {
    $items = seedPdfItems();
    $user = User::factory()->create(['role' => 'admin', 'can_download_pdf' => false]);
    $session = ExamSession::create([
        'user_id' => $guest ? null : $user->id,
        'track' => 'Professional', 'mode' => 'strict',
        'question_ids' => [$items[0]->id],
    ]);
    if ($guest) {
        $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    }
    $this->actingAs($user)->postJson(route('exams.exportPdf'), ['track' => 'Subprofessional'])
        ->assertStatus(423)->assertJsonMissingPath('questions');
})->with([false, true]);

test('PDF export rejects invalid stored keys', function () {
    $items = seedPdfItems();
    $items[0]->update(['correct_option' => 8]);
    $this->actingAs(User::factory()->create(['role' => 'admin', 'can_download_pdf' => false]))
        ->postJson(route('exams.exportPdf'), ['track' => 'Professional'])
        ->assertUnprocessable()->assertJsonMissingPath('questions');
});

test('an expired strict mock no longer blocks export', function () {
    $items = seedPdfItems();
    $user = User::factory()->create(['role' => 'admin', 'can_download_pdf' => false]);
    ExamSession::create([
        'user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict',
        'question_ids' => [$items[0]->id],
    ])->forceFill(['created_at' => now()->subDay()])->save();
    $this->actingAs($user)->postJson(route('exams.exportPdf'), ['track' => 'Professional'])->assertOk();
});

test('PDF export shares the daily authorization throttle', function () {
    seedPdfItems();
    $this->actingAs(User::factory()->create(['can_download_pdf' => true]));
    $this->postJson(route('exams.exportPdf'), ['track' => 'Professional'])->assertOk();
    $this->postJson(route('exams.exportPdf'), ['track' => 'Professional'])->assertStatus(429);
});
