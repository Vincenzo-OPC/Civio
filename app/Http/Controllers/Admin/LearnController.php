<?php

namespace App\Http\Controllers\Admin;

use App\Actions\Learn\BulkUpdateLearnModulesAction;
use App\DTOs\Learn\UpsertLearnModuleData;
use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\Learn\BulkDestroyLearnModulesRequest;
use App\Http\Requests\Admin\Learn\BulkUpdateLearnModuleStatusRequest;
use App\Http\Requests\Admin\Learn\GenerateLearnModuleRequest;
use App\Http\Requests\Admin\Learn\StoreLearnModuleRequest;
use App\Http\Requests\Admin\Learn\UpdateLearnModuleRequest;
use App\Jobs\GenerateLearnModuleJob;
use App\Models\Category;
use App\Models\LearnModule;
use App\Services\LearnModuleService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Str;
use Inertia\Response;

class LearnController extends Controller
{
    public function __construct(
        protected LearnModuleService $service,
        protected BulkUpdateLearnModulesAction $bulkAction
    ) {}

    /**
     * List all learn modules for admin curation dashboard.
     */
    public function index(Request $request): Response
    {
        $filters = [
            'search' => $request->input('search'),
            'status' => $request->input('status', 'all'),
            'category' => $request->input('category', 'all'),
            'subcategory' => $request->input('subcategory', 'all'),
            'per_page' => min(50, max(5, (int) $request->input('per_page', 10))),
        ];

        $data = $this->service->getAdminModules($filters, $filters['per_page']);

        return $this->render('admin/learn/index', [
            'modules' => $data['modules'],
            'pagination' => $data['pagination'],
            'filters' => [
                'search' => $filters['search'] ?? '',
                'status' => $filters['status'],
                'category' => $filters['category'],
                'subcategory' => $filters['subcategory'],
                'per_page' => $filters['per_page'],
            ],
            'categories' => $data['categories'],
        ]);
    }

    /**
     * Show the learning module creation panel.
     */
    public function create(Request $request): Response
    {
        $categories = Category::with('subcategory')->orderBy('sort_order')->get();

        return $this->render('admin/learn/create', [
            'categories' => $categories,
            'initialTopic' => $request->query('topic', ''),
        ]);
    }

    /**
     * Store a manually created or generated learn module in the database.
     */
    public function store(StoreLearnModuleRequest $request): RedirectResponse
    {
        // Bulk AI Learn Module commit
        if ($request->has('modules') && is_array($request->input('modules'))) {
            $savedCount = $this->bulkAction->commitApprovedDrafts(
                $request->input('modules'),
                (int) auth()->id()
            );

            return redirect()->route('admin.learn.drafts')
                ->with('success', "{$savedCount} approved learning modules published successfully!");
        }

        $dto = UpsertLearnModuleData::fromStoreRequest($request);
        $this->service->createModule($dto, (int) auth()->id());

        return $this->backWithSuccess('Learning module created successfully!');
    }

    /**
     * Show the edit panel for a learning module.
     */
    public function edit(string $id): Response
    {
        $module = LearnModule::findOrFail($id);
        $categories = Category::with('subcategory')->orderBy('sort_order')->get();

        return $this->render('admin/learn/edit', [
            'module' => [
                'id' => $module->id,
                'category_id' => $module->category_id,
                'subcategory_id' => $module->subcategory_id,
                'title' => $module->title,
                'topic' => $module->topic,
                'summary' => $module->summary,
                'content' => $module->content,
                'estimated_minutes' => $module->estimated_minutes,
                'is_published' => (bool) $module->is_published,
            ],
            'categories' => $categories,
        ]);
    }

    /**
     * Update the specified learning module.
     */
    public function update(UpdateLearnModuleRequest $request, string $id): RedirectResponse|JsonResponse
    {
        $module = LearnModule::findOrFail($id);
        Gate::authorize('update', $module);

        $dto = UpsertLearnModuleData::fromUpdateRequest($request);
        $this->service->updateModule($module, $dto);

        if ($request->wantsJson()) {
            return response()->json([
                'success' => true,
                'message' => 'Learning module draft updated successfully!',
            ]);
        }

        if (str_contains(request()->header('Referer', ''), '/learn/drafts')) {
            return $this->redirectWithSuccess('admin.learn.drafts', 'Learning module draft updated successfully!');
        }

        return $this->redirectWithSuccess('admin.learn.index', 'Learning module updated successfully!');
    }

    /**
     * Remove the specified learning module.
     */
    public function destroy(string $id): RedirectResponse
    {
        $module = LearnModule::findOrFail($id);
        Gate::authorize('delete', $module);

        $this->service->deleteModule($module);

        return $this->redirectWithSuccess('admin.learn.index', 'Learning module deleted successfully!');
    }

    /**
     * Bulk delete learning modules.
     */
    public function bulkDestroy(BulkDestroyLearnModulesRequest $request): RedirectResponse
    {
        Gate::authorize('manageAny', LearnModule::class);

        $validated = $request->validated();
        $this->bulkAction->bulkDelete($validated['ids']);

        return $this->redirectWithSuccess('admin.learn.index', 'Selected learning modules deleted successfully!');
    }

    /**
     * Bulk update learning module status.
     */
    public function bulkUpdateStatus(BulkUpdateLearnModuleStatusRequest $request): RedirectResponse
    {
        $validated = $request->validated();
        $this->bulkAction->bulkUpdateStatus($validated['ids'], (bool) $validated['is_published']);

        return $this->redirectWithSuccess('admin.learn.index', 'Selected learning modules updated successfully!');
    }

    public function generate(GenerateLearnModuleRequest $request): JsonResponse
    {
        $validated = $request->validated();
        $topic = $validated['topic'] ?? 'default';
        $lockKey = 'generate-learn-lock:'.Str::slug($topic);
        $lock = Cache::lock($lockKey, 180);

        if (! $lock->get()) {
            return response()->json([
                'success' => false,
                'message' => 'A learning module generation process is already in progress for this topic. Please wait for it to complete.',
            ], 429);
        }

        GenerateLearnModuleJob::dispatchAfterResponse(
            $validated,
            (int) (auth()->id() ?: 1),
            $validated['primary_model'] ?? 'llama-3.3-70b-versatile',
            $lock->owner()
        );

        return response()->json([
            'success' => true,
            'queued' => true,
            'message' => 'Generation is running in the background. Please wait 1-2 minutes before checking your drafts. It is not available immediately.',
        ]);
    }

    /**
     * Display a listing of draft learning modules for review.
     */
    public function drafts(Request $request): Response
    {
        $filters = [
            'search' => $request->input('search'),
            'category' => $request->input('category', 'all'),
            'subcategory' => $request->input('subcategory', 'all'),
            'per_page' => min(50, max(5, (int) $request->input('per_page', 10))),
        ];

        $data = $this->service->getAdminDrafts($filters, $filters['per_page']);

        return $this->render('admin/learn/drafts', [
            'initialDrafts' => $data['drafts'],
            'pagination' => $data['pagination'],
            'filters' => [
                'search' => $filters['search'] ?? '',
                'category' => $filters['category'],
                'subcategory' => $filters['subcategory'],
                'per_page' => $filters['per_page'],
            ],
            'categories' => $data['categories'],
        ]);
    }
}
