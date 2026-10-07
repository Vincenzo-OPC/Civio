<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Services\Offline\OfflinePackService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response as InertiaResponse;
use Symfony\Component\HttpFoundation\Response;

/**
 * Lite L2 offline drill packs. Guests allowed; throttled by `offline-packs`.
 * Only offline-eligible items, which never appear in strict mocks.
 */
class OfflinePackController extends Controller
{
    private const MAX_AGE = 300;

    public function __construct(private readonly OfflinePackService $packs) {}

    /** The offline drill runner shell (cached by the service worker). */
    public function page(): InertiaResponse
    {
        return Inertia::render('offline/index');
    }

    public function index(Request $request): Response
    {
        $manifest = $this->packs->manifest();

        return $this->cacheable($request, response()->json($manifest), 'm-'.$manifest['version']);
    }

    public function show(Request $request, int $category): Response
    {
        $subcategory = $request->filled('subcategory') ? (int) $request->query('subcategory') : null;
        $page = max(1, (int) $request->query('page', '1'));
        $version = $this->packs->scopeVersion($category, $subcategory);

        abort_if($version === null, 404);

        $etag = 'p-'.$version.'-'.($subcategory ?? 'all').'-'.$page;
        $probe = response()->noContent(200);
        $probe->setEtag($etag);

        if ($probe->isNotModified($request)) {
            return $this->withCacheHeaders($probe);
        }

        $payload = $this->packs->page($category, $subcategory, $page);

        abort_if($payload === null, 404);

        return $this->cacheable($request, response()->json($payload), $etag);
    }

    private function cacheable(Request $request, JsonResponse $response, string $etag): Response
    {
        $response->setEtag($etag);
        $response->isNotModified($request);

        return $this->withCacheHeaders($response);
    }

    private function withCacheHeaders(Response $response): Response
    {
        $response->setPublic();
        $response->setMaxAge(self::MAX_AGE);

        return $response;
    }
}
