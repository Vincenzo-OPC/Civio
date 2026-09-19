<?php

declare(strict_types=1);

use App\Models\Category;
use App\Models\LearnModule;
use App\Models\Subcategory;
use App\Models\User;

test('admin can view learn modules index', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create([
        'name' => 'General Information',
        'slug' => 'general-information',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Philippine Constitution',
        'slug' => 'philippine-constitution',
        'language' => 'English',
    ]);

    LearnModule::create([
        'category_id' => $category->id,
        'subcategory_id' => $subcategory->id,
        'title' => 'Introduction to the Constitution',
        'slug' => 'introduction-to-the-constitution',
        'topic' => 'Preamble',
        'summary' => 'Basic overview of the constitution.',
        'content' => 'Full lesson content goes here.',
        'estimated_minutes' => 15,
        'is_published' => true,
        'created_by' => $admin->id,
    ]);

    $response = $this->actingAs($admin)->get(route('admin.learn.index'));

    $response->assertOk();
});

test('admin can create a learn module', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create([
        'name' => 'Numerical Ability',
        'slug' => 'numerical-ability',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Basic Operations',
        'slug' => 'basic-operations',
        'language' => 'English',
    ]);

    $response = $this->actingAs($admin)->post(route('admin.learn.store'), [
        'category_id' => $category->id,
        'subcategory_id' => $subcategory->id,
        'title' => 'Arithmetic Fundamentals',
        'topic' => 'Order of Operations',
        'summary' => 'Mastering PEMDAS and BODMAS.',
        'content' => '# Order of Operations\n\nContent details...',
        'estimated_minutes' => 20,
        'is_published' => true,
    ]);

    $response->assertRedirect();
    $this->assertDatabaseHas('learn_modules', [
        'title' => 'Arithmetic Fundamentals',
        'topic' => 'Order of Operations',
        'slug' => 'arithmetic-fundamentals',
    ]);
});

test('admin can update a learn module', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $category = Category::create([
        'name' => 'Verbal Ability',
        'slug' => 'verbal-ability',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Grammar and Correct Usage',
        'slug' => 'grammar-and-correct-usage',
        'language' => 'English',
    ]);

    $module = LearnModule::create([
        'category_id' => $category->id,
        'subcategory_id' => $subcategory->id,
        'title' => 'Subject-Verb Agreement',
        'slug' => 'subject-verb-agreement',
        'topic' => 'Singular and Plural Verbs',
        'summary' => 'Rules on subject-verb agreement.',
        'content' => 'Content details...',
        'estimated_minutes' => 15,
        'is_published' => false,
        'created_by' => $admin->id,
    ]);

    $response = $this->actingAs($admin)->put(route('admin.learn.update', $module->id), [
        'category_id' => $category->id,
        'subcategory_id' => $subcategory->id,
        'title' => 'Advanced Subject-Verb Agreement',
        'topic' => 'Compound Subjects',
        'summary' => 'Updated summary rules.',
        'content' => 'Updated content...',
        'estimated_minutes' => 25,
        'is_published' => true,
    ]);

    $response->assertRedirect();
    $this->assertDatabaseHas('learn_modules', [
        'id' => $module->id,
        'title' => 'Advanced Subject-Verb Agreement',
        'topic' => 'Compound Subjects',
        'is_published' => true,
    ]);
});

test('admin can delete a learn module', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $module = LearnModule::factory()->create();

    $response = $this->actingAs($admin)->delete(route('admin.learn.destroy', $module->id));

    $response->assertRedirect();
    $this->assertDatabaseMissing('learn_modules', [
        'id' => $module->id,
    ]);
});

test('admin can bulk update status and bulk delete learn modules', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $modules = LearnModule::factory()->count(3)->create(['is_published' => false]);
    $ids = $modules->pluck('id')->toArray();

    // Bulk update status to published
    $responseUpdate = $this->actingAs($admin)->post(route('admin.learn.bulkDestroy'), [
        'ids' => [$ids[0]],
    ]);
    $responseUpdate->assertRedirect();
    $this->assertDatabaseMissing('learn_modules', ['id' => $ids[0]]);

    // Bulk delete remaining
    $responseDelete = $this->actingAs($admin)->post(route('admin.learn.bulkDestroy'), [
        'ids' => [$ids[1], $ids[2]],
    ]);
    $responseDelete->assertRedirect();
    $this->assertDatabaseMissing('learn_modules', ['id' => $ids[1]]);
    $this->assertDatabaseMissing('learn_modules', ['id' => $ids[2]]);
});

test('admin can view drafts and commit approved draft modules', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $responseDrafts = $this->actingAs($admin)->get(route('admin.learn.drafts'));
    $responseDrafts->assertOk();

    $responseCommit = $this->actingAs($admin)->post(route('admin.learn.store'), [
        'modules' => [
            [
                'title' => 'AI Generated Lesson 1',
                'topic' => 'Logic Inferences',
                'summary' => 'Premise and conclusion deduction.',
                'content' => 'Detailed logic content...',
                'estimated_minutes' => 15,
                'category' => 'Analytical Ability',
                'subcategory' => 'Logical Reasoning',
            ],
        ],
    ]);

    $responseCommit->assertRedirect(route('admin.learn.drafts'));
    $this->assertDatabaseHas('learn_modules', [
        'title' => 'AI Generated Lesson 1',
        'is_published' => true,
    ]);
});

test('users can view published learn modules catalog and show detail', function () {
    $user = User::factory()->create();

    $category = Category::create([
        'name' => 'Analytical Ability',
        'slug' => 'analytical-ability',
    ]);

    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Data Interpretation',
        'slug' => 'data-interpretation',
        'language' => 'English',
    ]);

    $module = LearnModule::create([
        'category_id' => $category->id,
        'subcategory_id' => $subcategory->id,
        'title' => 'Reading Tables and Graphs',
        'slug' => 'reading-tables-and-graphs',
        'topic' => 'Bar Charts',
        'summary' => 'Interpreting statistical figures.',
        'content' => "Paragraph 1\n\nParagraph 2\n\nParagraph 3\n\nParagraph 4\n\nParagraph 5",
        'estimated_minutes' => 10,
        'is_published' => true,
        'created_by' => $user->id,
    ]);

    // User catalog
    $this->actingAs($user)->get(route('learn.index'))->assertOk();

    // User show
    $this->actingAs($user)->get(route('learn.show', $module->slug))->assertOk();

    // Toggle complete
    $this->actingAs($user)->post(route('learn.complete', $module->slug))->assertRedirect();

    $module->refresh();
    expect($module->isCompletedBy($user->id))->toBeTrue();
});
