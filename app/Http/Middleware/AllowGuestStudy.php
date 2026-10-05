<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

/**
 * Local-study: allow guests through when CIVIO_GUEST_UNLIMITED is on.
 * Otherwise behave like auth.or.fail (404 for unauthenticated).
 */
class AllowGuestStudy
{
    /**
     * @param  Closure(Request): (Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (Auth::check()) {
            return $next($request);
        }

        if (config('civio.guest_unlimited')) {
            return $next($request);
        }

        abort(404);
    }
}