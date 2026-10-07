<?php

use App\Models\Category;
use App\Models\OfflinePracticeResult;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Support\Facades\Cache;

/**
 * General Information bank with 16 unique items (offline cap 16 - 12 = 4),
 * plus a demographic item.
 *
 * @return array{gi: Category, sub: Subcategory, ids: array<int, int>, demographic: int}
 */
function seedOfflineBank(int $count = 16): array
{
    $author = User::factory()->create();
    $gi = Category::factory()->create(['name' => 'General Information', 'is_demographic' => false]);
    $sub = Subcategory::factory()->create(['category_id' => $gi->id, 'name' => 'Constitution']);
    $ids = [];

    for ($i = 0; $i < $count; $i++) {
        $ids[] = Question::factory()->create([
            'subcategory_id' => $sub->id,
            'created_by' => $author->id,
            'status' => 'active',
            'stem' => "Constitution item {$i}: which article covers this topic?",
            'options' => ["A {$i}", "B {$i}", "C {$i}", "D {$i}"],
            'correct_option' => 1,
            'explanation' => "Because B {$i}.",
        ])->id;
    }

    $demoCategory = Category::factory()->create(['name' => 'Demographic Profile', 'is_demographic' => true]);
    $demoSub = Subcategory::factory()->create(['category_id' => $demoCategory->id, 'name' => 'Age']);
    $demographic = Question::factory()->create(['subcategory_id' => $demoSub->id, 'created_by' => $author->id, 'status' => 'active'])->id;

    return ['gi' => $gi, 'sub' => $sub, 'ids' => $ids, 'demographic' => $demographic];
}

/** @return array<int, int> */
function offlineIds(): array
{
    return Question::query()->where('offline_eligible', true)->orderBy('id')->pluck('id')->all();
}

test('the command marks up to the cap, never demographics, and dry run saves nothing', function () {
    $bank = seedOfflineBank();

    $this->artisan('civio:mark-offline-eligible', ['--dry-run' => true])
        ->expectsOutputToContain('Would mark 4 question(s)')
        ->assertSuccessful();
    expect(offlineIds())->toBe([]);

    Cache::put('questions.active', collect());
    $this->artisan('civio:mark-offline-eligible')->expectsOutputToContain('Marked 4 question(s)')->assertSuccessful();

    expect(offlineIds())->toBe(array_slice($bank['ids'], 0, 4))
        ->and(offlineIds())->not->toContain($bank['demographic'])
        ->and(Cache::has('questions.active'))->toBeFalse();

    // Idempotent: a second run adds nothing.
    $this->artisan('civio:mark-offline-eligible')->expectsOutputToContain('Marked 0 question(s)')->assertSuccessful();
    expect(offlineIds())->toHaveCount(4);
});

test('strict mocks never serve offline-eligible items', function () {
    seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();

    $served = $this->postJson(route('exams.sessions.store'), ['track' => 'professional'])
        ->assertOk()
        ->json('questions.*.id');

    // General Information quota is 8; 12 items are left for mocks.
    expect($served)->toHaveCount(8)
        ->and(array_intersect($served, offlineIds()))->toBe([]);
});

test('guests get a manifest and pages with keys and explanations for offline items only', function () {
    $bank = seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();

    $manifest = $this->getJson(route('offline.packs.index'))->assertOk();
    $manifest->assertJsonPath('per_page', 40)
        ->assertJsonPath('packs.0.category', 'General Information')
        ->assertJsonPath('packs.0.items', 4)
        ->assertJsonPath('packs.0.pages', 1)
        ->assertJsonPath('packs.0.subcategories.0.name', 'Constitution');
    expect($manifest->json('packs'))->toHaveCount(1)
        ->and($manifest->json('packs.0.bytes'))->toBeGreaterThan(100)
        ->and($manifest->headers->get('ETag'))->not->toBeNull();

    $page = $this->getJson(route('offline.packs.show', ['category' => $bank['gi']->id]))->assertOk();
    $items = collect($page->json('items'));

    expect($items->pluck('id')->all())->toBe(offlineIds())
        ->and($page->json('version'))->toBe($manifest->json('packs.0.version'));

    $first = $items->first();
    expect($first)->toHaveKeys(['id', 'stem', 'options', 'correct_option', 'explanation', 'category', 'subcategory', 'language'])
        ->and($first['correct_option'])->toBe(1)
        ->and($first['explanation'])->toStartWith('Because B');

    $this->getJson(route('offline.packs.show', ['category' => $bank['gi']->id, 'subcategory' => $bank['sub']->id]))
        ->assertOk()->assertJsonPath('total', 4);
    $this->getJson(route('offline.packs.show', ['category' => $bank['gi']->id, 'page' => 2]))->assertNotFound();
});

test('pack pages are cacheable with an ETag and answer 304 when unchanged', function () {
    $bank = seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    $url = route('offline.packs.show', ['category' => $bank['gi']->id]);

    $first = $this->getJson($url)->assertOk();
    $etag = $first->headers->get('ETag');
    expect($first->headers->get('Cache-Control'))->toContain('public')->toContain('max-age=300');

    $this->getJson($url, ['If-None-Match' => $etag])->assertStatus(304);

    Question::query()->whereKey(offlineIds()[0])->update(['updated_at' => now()->addMinute()]);
    $changed = $this->getJson($url, ['If-None-Match' => $etag])->assertOk();
    expect($changed->headers->get('ETag'))->not->toBe($etag);
});

test('a category with no offline items has no pack', function () {
    $bank = seedOfflineBank();

    $this->getJson(route('offline.packs.index'))->assertOk()->assertJsonPath('packs', []);
    $this->getJson(route('offline.packs.show', ['category' => $bank['gi']->id]))->assertNotFound();
});

test('pack downloads are throttled', function () {
    config(['civio.offline.packs_per_minute' => 2]);
    seedOfflineBank();

    $this->getJson(route('offline.packs.index'))->assertOk();
    $this->getJson(route('offline.packs.index'))->assertOk();
    $this->getJson(route('offline.packs.index'))->assertStatus(429);
});

test('sync is throttled', function () {
    config(['civio.offline.sync_per_minute' => 1]);
    $payload = ['attempts' => [['client_id' => 'a1', 'question_id' => 1, 'selected_option' => 0, 'claimed_correct_option' => 0]]];

    $this->postJson(route('offline.attempts.store'), $payload)->assertOk();
    $this->postJson(route('offline.attempts.store'), $payload)->assertStatus(429);
});

test('sync re-grades with the server key and tags results offline_practice', function () {
    seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    [$a, $b] = offlineIds();
    $user = User::factory()->create();

    $response = $this->actingAs($user)->postJson(route('offline.attempts.store'), ['attempts' => [
        ['client_id' => 'c-1', 'question_id' => $a, 'selected_option' => 1, 'claimed_correct_option' => 1, 'pack_version' => 'abc', 'answered_at' => now()->subHour()->toIso8601String()],
        ['client_id' => 'c-2', 'question_id' => $b, 'selected_option' => 3, 'claimed_correct_option' => 1],
    ]])->assertOk();

    $response->assertJsonPath('results.0.status', 'accepted')
        ->assertJsonPath('results.0.correct', true)
        ->assertJsonPath('results.1.correct', false)
        ->assertJsonPath('bias.correct_ids', [$a])
        ->assertJsonPath('bias.wrong_ids', [$b])
        ->assertJsonPath('bias.category_scores.General Information.total', 2)
        ->assertJsonPath('bias.category_scores.General Information.correct', 1)
        ->assertJsonPath('bias.category_scores.General Information.subcats.Constitution.total', 2);

    $rows = OfflinePracticeResult::query()->orderBy('client_id')->get();
    expect($rows)->toHaveCount(2)
        ->and($rows->pluck('source')->unique()->all())->toBe(['offline_practice'])
        ->and($rows->pluck('user_id')->unique()->all())->toBe([$user->id])
        ->and($rows[0]->owner_key)->toBe('u:'.$user->id)
        ->and($rows[0]->pack_version)->toBe('abc');
});

test('a tampered key claim is rejected and not counted', function () {
    seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    $id = offlineIds()[0];

    // Client says option 3 is correct (it is 1) and picks 3.
    $response = $this->postJson(route('offline.attempts.store'), ['attempts' => [
        ['client_id' => 't-1', 'question_id' => $id, 'selected_option' => 3, 'claimed_correct_option' => 3],
    ]])->assertOk();

    $response->assertJsonPath('results.0.status', 'rejected')
        ->assertJsonPath('results.0.reason', 'key_mismatch')
        ->assertJsonMissingPath('results.0.correct')
        ->assertJsonPath('bias.correct_ids', [])
        ->assertJsonPath('bias.wrong_ids', []);

    expect(OfflinePracticeResult::query()->sole()->is_correct)->toBeFalse();
});

test('sync never grades items outside offline packs, so it is not an answer oracle', function () {
    $bank = seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    $mockItem = $bank['ids'][10];

    $response = $this->postJson(route('offline.attempts.store'), ['attempts' => [
        ['client_id' => 'o-1', 'question_id' => $mockItem, 'selected_option' => 1, 'claimed_correct_option' => 1],
        ['client_id' => 'o-2', 'question_id' => 999999, 'selected_option' => 0, 'claimed_correct_option' => 0],
    ]])->assertOk();

    $response->assertJsonPath('results.0.status', 'rejected')
        ->assertJsonPath('results.0.reason', 'not_offline')
        ->assertJsonMissingPath('results.0.correct')
        ->assertJsonPath('results.1.reason', 'not_offline');
});

test('sync is idempotent per client id', function () {
    seedOfflineBank();
    $this->artisan('civio:mark-offline-eligible')->assertSuccessful();
    $id = offlineIds()[0];
    $payload = ['attempts' => [['client_id' => 'same-1', 'question_id' => $id, 'selected_option' => 1, 'claimed_correct_option' => 1]]];
    $this->actingAs(User::factory()->create());

    $this->postJson(route('offline.attempts.store'), $payload)->assertOk()->assertJsonPath('results.0.duplicate', false);
    $this->postJson(route('offline.attempts.store'), $payload)
        ->assertOk()
        ->assertJsonPath('results.0.duplicate', true)
        ->assertJsonPath('results.0.correct', true);

    expect(OfflinePracticeResult::query()->count())->toBe(1);
});

test('sync validates its input', function () {
    $this->postJson(route('offline.attempts.store'), ['attempts' => []])->assertUnprocessable();
    $this->postJson(route('offline.attempts.store'), ['attempts' => [
        ['client_id' => 'bad id!', 'question_id' => 1, 'selected_option' => 0, 'claimed_correct_option' => 0],
    ]])->assertUnprocessable()->assertJsonValidationErrors('attempts.0.client_id');
    $this->postJson(route('offline.attempts.store'), ['attempts' => array_fill(0, 201, [
        'client_id' => 'x', 'question_id' => 1, 'selected_option' => 0, 'claimed_correct_option' => 0,
    ])])->assertUnprocessable();
});

test('the offline page opens for guests', function () {
    $this->get(route('offline.index'))->assertOk()->assertInertia(fn ($page) => $page->component('offline/index', false));
});
