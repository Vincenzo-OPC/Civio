<?php

use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Support\Facades\Artisan;

test('question import keeps one row per stem and drops variant copies', function () {
    $user = User::factory()->create();
    $subcategory = Subcategory::factory()->create([
        'name' => 'Philippine Constitution',
    ]);

    $path = storage_path('framework/testing-practice-bank.json');
    file_put_contents($path, json_encode([
        [
            'subcategory' => $subcategory->name,
            'stem' => 'The Bill of Rights is found mainly in Article III.',
            'options' => ['Yes', 'No', 'Maybe', 'Never'],
            'correct_option' => 0,
            'explanation' => 'Article III.',
        ],
        [
            'subcategory' => $subcategory->name,
            'stem' => 'The Bill of Rights is found mainly in Article III. (variant 2)',
            'options' => ['Yes', 'No', 'Maybe', 'Never'],
            'correct_option' => 0,
        ],
        [
            'subcategory' => $subcategory->name,
            'stem' => 'Sovereignty resides in the people.',
            'options' => ['People', 'President'],
            'correct_option' => 'A',
        ],
    ]));

    $exit = Artisan::call('questions:import', [
        'path' => $path,
        '--user' => $user->email,
    ]);

    expect($exit)->toBe(0);
    expect(Question::query()->count())->toBe(2);
    expect(Question::query()->where('stem', 'like', '%variant%')->exists())->toBeFalse();

    @unlink($path);
});
