<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use Symfony\Component\HttpFoundation\BinaryFileResponse;

/**
 * Serves the built service worker (public/build/sw.js) at /sw.js so its scope
 * is the whole site. From /build/sw.js it could only control /build/ pages,
 * which meant it controlled none.
 */
class ServiceWorkerController extends Controller
{
    public function __invoke(): BinaryFileResponse
    {
        $path = public_path('build/sw.js');

        abort_unless(is_file($path), 404);

        return response()->file($path, [
            'Content-Type' => 'text/javascript; charset=utf-8',
            'Cache-Control' => 'no-cache',
            'Service-Worker-Allowed' => '/',
        ]);
    }
}
