<?php

namespace App\Http\Controllers\Admin;

use App\DTOs\User\UpdateUserData;
use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\User\AdminUserUpdateRequest;
use App\Http\Resources\AdminUserResource;
use App\Models\User;
use App\Services\UserService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Response;

class UserController extends Controller
{
    public function __construct(
        protected UserService $userService
    ) {}

    /**
     * Show all users with their statistics for the admin dashboard.
     */
    public function index(Request $request): Response
    {
        $data = $this->userService->getAdminUsersData();

        return $this->render('admin/users/index', [
            'users' => AdminUserResource::collection($data['users'])->resolve(),
            'stats' => $data['stats'],
        ]);
    }

    /**
     * Update user role.
     */
    public function update(AdminUserUpdateRequest $request, int $id): RedirectResponse
    {
        $user = User::findOrFail($id);

        Gate::authorize('update', $user);

        $dto = UpdateUserData::fromRequest($request);
        $this->userService->updateUser($id, $dto, (int) auth()->id());

        return back();
    }

    /**
     * Permanently delete user account.
     */
    public function destroy(int $id): RedirectResponse
    {
        $user = User::findOrFail($id);

        Gate::authorize('delete', $user);

        $this->userService->deleteUser($id, (int) auth()->id());

        return back();
    }
}
