<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AllowFreeAttempt
{
    /**
     * Handle an incoming request.
     *
     * @param  Closure(Request): (Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        // Starting a new track/mock should not reuse a stale guest scorecard redirect.
        $startingFresh = $request->has('start')
            || ($request->query('free_attempt') == '1' && ! $request->has('attempt_id'));

        // A limited guest who already submitted keeps that marker: 'start' or
        // 'free_attempt=1' in the URL must not hand out another free attempt.
        // Signed-in users and local-study (guest_unlimited) may start fresh.
        $usedFreeAttempt = ! Auth::check()
            && ! config('civio.guest_unlimited')
            && $request->session()->has('pending_guest_attempt_id');

        if ($startingFresh && $usedFreeAttempt) {
            $startingFresh = false;
        }

        if ($startingFresh) {
            $request->session()->forget('pending_guest_attempt_id');
            $request->session()->put('is_free_attempt_active', true);
        }

        // Local study / CIVIO: guests get full exam access (no one-shot wall).
        if (config('civio.guest_unlimited')) {
            if (! Auth::check()) {
                $request->session()->put('is_free_attempt_active', true);
            }

            return $next($request);
        }

        // If they already have a completed guest attempt, redirect them to its scorecard
        if (! Auth::check() && $request->session()->has('pending_guest_attempt_id') && ! $startingFresh) {
            $pendingId = $request->session()->get('pending_guest_attempt_id');
            if ($request->query('attempt_id') != $pendingId) {
                return redirect()->route('exams.index', ['attempt_id' => $pendingId, 'limit' => '1']);
            }

            return $next($request);
        }

        // Allow access if free_attempt parameter is present
        if ($request->has('free_attempt') && $request->query('free_attempt') == '1') {
            $request->session()->put('is_free_attempt_active', true);

            return $next($request);
        }

        // Allow access if there is an active free attempt session flag
        if ($request->session()->get('is_free_attempt_active') === true) {
            return $next($request);
        }

        // Allow access if there is a pending guest attempt in session (for viewing the scorecard)
        if ($request->session()->has('pending_guest_attempt_id')) {
            return $next($request);
        }

        // Otherwise require authentication
        if (! Auth::check()) {
            abort(404);
        }

        return $next($request);
    }
}
