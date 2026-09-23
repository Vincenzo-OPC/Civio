<?php

use App\Models\RecalledQuestion;
use App\Models\User;

test('a guest can submit a paraphrased practice question', function () {
    $this->postJson(route('community.recalled.store'), [
        'stem' => 'The Bill of Rights is mostly found in which article of the Constitution?',
        'note' => 'I think the answer was Article III.',
        'subcategory' => 'Philippine Constitution',
    ])->assertOk()->assertJson(['success' => true]);

    $this->assertDatabaseHas('recalled_questions', [
        'status' => 'pending',
        'user_id' => null,
    ]);
});

test('a submission cannot claim to be an official paper', function () {
    $this->postJson(route('community.recalled.store'), [
        'stem' => 'This is the official CSC paper question about the president term.',
    ])->assertStatus(422);
});

test('an admin can moderate the practice queue', function () {
    $admin = User::factory()->create(['role' => 'admin']);
    $row = RecalledQuestion::query()->create([
        'stem' => 'A paraphrased practice item about public office.',
        'status' => 'pending',
    ]);

    $this->actingAs($admin)
        ->put(route('admin.recalled-questions.updateStatus', $row), [
            'status' => 'approved',
        ])
        ->assertRedirect();

    expect($row->fresh()->status)->toBe('approved');
});

test('guests cannot open the moderation queue', function () {
    $this->get(route('admin.recalled-questions.index'))->assertNotFound();
});
