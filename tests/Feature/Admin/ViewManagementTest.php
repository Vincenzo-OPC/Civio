<?php

use App\Models\RolePermission;
use App\Models\User;

test('admin can view view management page', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $response = $this->actingAs($admin)->get(route('admin.view-management.index'));

    $response->assertOk();
    $response->assertInertia(fn ($page) => $page
        ->component('admin/view-management/index')
        ->has('permissions')
        ->has('availableViews')
    );
});

test('admin can update view permissions without 403 forbidden', function () {
    $admin = User::factory()->create([
        'role' => 'admin',
        'is_active' => true,
    ]);

    $permission = RolePermission::create([
        'role' => 'user',
        'view_name' => 'mock-exams',
        'is_visible' => true,
    ]);

    $response = $this->actingAs($admin)->put(route('admin.view-management.update'), [
        'permissions' => [
            [
                'id' => $permission->id,
                'is_visible' => false,
            ],
        ],
    ]);

    $response->assertSessionHasNoErrors();
    $response->assertRedirect();
    expect($permission->fresh()->is_visible)->toBeFalse();
});

test('non-admin cannot update view permissions', function () {
    $user = User::factory()->create([
        'role' => 'user',
        'is_active' => true,
    ]);

    $permission = RolePermission::create([
        'role' => 'user',
        'view_name' => 'mock-exams',
        'is_visible' => true,
    ]);

    $response = $this->actingAs($user)->put(route('admin.view-management.update'), [
        'permissions' => [
            [
                'id' => $permission->id,
                'is_visible' => false,
            ],
        ],
    ]);

    $response->assertNotFound();
});
