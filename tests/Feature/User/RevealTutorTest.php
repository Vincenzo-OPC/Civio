<?php

declare(strict_types=1);

use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

it('returns a checked reveal and an easier follow-up after a miss', function () {
    $author = User::factory()->create();
    $category = Category::factory()->create(['name' => 'Numerical Ability', 'is_demographic' => false]);
    $subcategory = Subcategory::factory()->create([
        'category_id' => $category->id,
        'name' => 'Word problems',
    ]);

    $hard = Question::factory()->create([
        'subcategory_id' => $subcategory->id,
        'created_by' => $author->id,
        'status' => 'active',
        'language' => 'English',
        'stem' => 'A rectangle is 12 m by 5 m. Its perimeter is: '.str_repeat('Read the whole stem before you mark a choice. ', 6),
        'options' => ['34 m', '60 m', '17 m', '24 m'],
        'correct_option' => 0,
        'explanation' => 'Perimeter is the distance around.',
    ]);
    $easy = Question::factory()->create([
        'subcategory_id' => $subcategory->id,
        'created_by' => $author->id,
        'status' => 'active',
        'language' => 'English',
        'stem' => 'Short?',
        'options' => ['1', '2', '3', '4'],
        'correct_option' => 0,
        'explanation' => 'One.',
    ]);

    $response = $this->postJson(route('exams.reveal'), [
        'question_id' => $hard->id,
        'chosen_option' => 1,
    ])->assertOk()
        ->assertJsonPath('tutor.steps.0', '12 + 5 + 12 + 5 = 34 m.')
        ->assertJsonPath('tutor.followUp.questionId', $easy->id)
        ->assertJsonPath('tutor.followUp.direction', 'easier')
        ->assertJsonPath('tutor.followUp.question.id', $easy->id)
        ->assertJsonPath('tutor.followUp.question.stem', 'Short?');

    expect($response->json('tutor.followUp.question'))->not->toHaveKey('correct_option');
});
