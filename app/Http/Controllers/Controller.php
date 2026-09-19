<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

abstract class Controller
{
    use AuthorizesRequests;

    /**
     * Get the currently authenticated user with strict User model typing.
     */
    protected function user(): ?User
    {
        /** @var ?User */
        return Auth::user();
    }

    /**
     * Get the authenticated user or abort with a 401 response.
     */
    protected function requireUser(): User
    {
        $user = $this->user();
        if (! $user) {
            abort(401, 'Unauthenticated.');
        }

        return $user;
    }

    /**
     * Redirect back with a flash success message.
     */
    protected function backWithSuccess(string $message): RedirectResponse
    {
        return redirect()->back()->with('success', $message);
    }

    /**
     * Redirect back with a flash error message.
     */
    protected function backWithError(string $message): RedirectResponse
    {
        return redirect()->back()->with('error', $message);
    }

    /**
     * Redirect to a named route with a flash success message.
     *
     * @param  array<string, mixed>  $parameters
     */
    protected function redirectWithSuccess(string $route, string $message, array $parameters = []): RedirectResponse
    {
        return redirect()->route($route, $parameters)->with('success', $message);
    }

    /**
     * Redirect to a named route with a flash error message.
     *
     * @param  array<string, mixed>  $parameters
     */
    protected function redirectWithError(string $route, string $message, array $parameters = []): RedirectResponse
    {
        return redirect()->route($route, $parameters)->with('error', $message);
    }

    /**
     * Standard JSON success response.
     */
    protected function jsonSuccess(mixed $data = null, string $message = 'Success', int $status = 200): JsonResponse
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
        ], $status);
    }

    /**
     * Standard JSON error response.
     */
    protected function jsonError(string $message = 'An error occurred.', int $status = 400, mixed $errors = null): JsonResponse
    {
        return response()->json([
            'success' => false,
            'message' => $message,
            'errors' => $errors,
        ], $status);
    }
}
