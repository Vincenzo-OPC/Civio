<?php

declare(strict_types=1);

use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

test('admin can view questions index with pagination', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create([
        'name' => 'Analytical Ability',
        'slug' => 'analytical-ability',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Word analogy',
        'slug' => 'word-analogy',
        'language' => 'English',
    ]);

    Question::create([
        'subcategory_id' => $subcategory->id,
        'stem' => 'Sample test stem',
        'options' => ['A', 'B', 'C', 'D'],
        'correct_option' => 1,
        'explanation' => 'Test explanation',
        'language' => 'English',
        'status' => 'active',
        'created_by' => $admin->id,
    ]);

    $response = $this->actingAs($admin)->get(route('questions.index'));

    $response->assertOk();
    $response->assertInertia(fn ($page) => $page
        ->component('admin/questions/index')
        ->has('questions')
        ->has('pagination')
        ->has('categories')
    );
});

test('admin can store question via FormRequest and DTO pipeline', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $response = $this->actingAs($admin)->post(route('questions.store'), [
        'category' => 'Verbal Ability',
        'subcategory' => 'Grammar and Correct Usage',
        'language' => 'English',
        'stem' => 'Which of the following is correct?',
        'options' => ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
        'correct_option' => 2,
        'explanation' => 'Rule explanation here.',
        'status' => 'active',
    ]);

    $response->assertSessionHas('success');

    $this->assertDatabaseHas('questions', [
        'stem' => 'Which of the following is correct?',
        'correct_option' => 2,
        'status' => 'active',
    ]);
});

test('admin can view single question show page', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create(['name' => 'Numerical Ability', 'slug' => 'numerical-ability']);
    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Basic Operations',
        'slug' => 'basic-operations',
        'language' => 'English',
    ]);

    $question = Question::create([
        'subcategory_id' => $subcategory->id,
        'stem' => 'What is 5 + 5?',
        'options' => ['5', '10', '15', '20'],
        'correct_option' => 1,
        'explanation' => '5+5 equals 10.',
        'language' => 'English',
        'status' => 'active',
        'created_by' => $admin->id,
    ]);

    $response = $this->actingAs($admin)->get(route('questions.show', $question->id));

    $response->assertOk();
    $response->assertInertia(fn ($page) => $page
        ->component('admin/questions/show')
        ->where('question.id', $question->id)
        ->where('question.stem', 'What is 5 + 5?')
    );
});

test('admin can update a question', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create(['name' => 'General Information', 'slug' => 'general-information']);
    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Philippine Constitution',
        'slug' => 'philippine-constitution',
        'language' => 'English',
    ]);

    $question = Question::create([
        'subcategory_id' => $subcategory->id,
        'stem' => 'Original Stem Question',
        'options' => ['A', 'B', 'C', 'D'],
        'correct_option' => 0,
        'explanation' => 'Original explanation.',
        'language' => 'English',
        'status' => 'draft',
        'created_by' => $admin->id,
    ]);

    $response = $this->actingAs($admin)->put(route('questions.update', $question->id), [
        'category' => 'General Information',
        'subcategory' => 'Philippine Constitution',
        'language' => 'English',
        'stem' => 'Updated Stem Question via DTO',
        'options' => ['A', 'B', 'C', 'D'],
        'correct_option' => 3,
        'explanation' => 'Updated explanation.',
        'status' => 'active',
    ]);

    $response->assertRedirect(route('questions.index'));

    $this->assertDatabaseHas('questions', [
        'id' => $question->id,
        'stem' => 'Updated Stem Question via DTO',
        'correct_option' => 3,
        'status' => 'active',
    ]);
});

test('admin can delete a question', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create(['name' => 'Clerical Ability', 'slug' => 'clerical-ability']);
    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Filing',
        'slug' => 'filing',
        'language' => 'English',
    ]);

    $question = Question::create([
        'subcategory_id' => $subcategory->id,
        'stem' => 'Question to delete',
        'options' => ['A', 'B', 'C', 'D'],
        'correct_option' => 0,
        'explanation' => 'Exp',
        'language' => 'English',
        'status' => 'draft',
        'created_by' => $admin->id,
    ]);

    $response = $this->actingAs($admin)->delete(route('questions.destroy', $question->id));

    $response->assertRedirect(route('questions.index'));
    $this->assertDatabaseMissing('questions', ['id' => $question->id]);
});

test('admin can bulk update status and bulk delete questions via action', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create(['name' => 'Analytical Ability', 'slug' => 'analytical-ability']);
    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Number series',
        'slug' => 'number-series',
        'language' => 'English',
    ]);

    $q1 = Question::create([
        'subcategory_id' => $subcategory->id,
        'stem' => 'Q1',
        'options' => ['1', '2', '3', '4'],
        'correct_option' => 0,
        'explanation' => '',
        'language' => 'English',
        'status' => 'draft',
        'created_by' => $admin->id,
    ]);

    $q2 = Question::create([
        'subcategory_id' => $subcategory->id,
        'stem' => 'Q2',
        'options' => ['1', '2', '3', '4'],
        'correct_option' => 1,
        'explanation' => '',
        'language' => 'English',
        'status' => 'draft',
        'created_by' => $admin->id,
    ]);

    // Bulk update questions
    $responseUpdate = $this->actingAs($admin)->put(route('questions.bulkUpdate'), [
        'questions' => [
            [
                'id' => $q1->id,
                'category' => 'Analytical Ability',
                'subcategory' => 'Number series',
                'language' => 'English',
                'stem' => 'Q1 Updated',
                'options' => ['1', '2', '3', '4'],
                'correct_option' => 0,
                'explanation' => '',
                'status' => 'active',
            ],
            [
                'id' => $q2->id,
                'category' => 'Analytical Ability',
                'subcategory' => 'Number series',
                'language' => 'English',
                'stem' => 'Q2 Updated',
                'options' => ['1', '2', '3', '4'],
                'correct_option' => 1,
                'explanation' => '',
                'status' => 'active',
            ],
        ],
    ]);
    $responseUpdate->assertOk();
    $this->assertDatabaseHas('questions', ['id' => $q1->id, 'stem' => 'Q1 Updated', 'status' => 'active']);
    $this->assertDatabaseHas('questions', ['id' => $q2->id, 'stem' => 'Q2 Updated', 'status' => 'active']);

    // Bulk delete
    $responseDelete = $this->actingAs($admin)->post(route('questions.bulkDestroy'), [
        'ids' => [$q1->id, $q2->id],
    ]);
    $responseDelete->assertRedirect();
    $this->assertDatabaseMissing('questions', ['id' => $q1->id]);
    $this->assertDatabaseMissing('questions', ['id' => $q2->id]);
});
