<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Http\Requests\User\StudySchedule\ApplySuggestionsRequest;
use App\Http\Requests\User\StudySchedule\ApplyTemplateRequest;
use App\Models\StudySchedule;
use App\Services\StudyPlanAnalyzer;
use App\Services\StudyPlanTemplateService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class StudySuggestionController extends Controller
{
    public function __construct(
        protected StudyPlanAnalyzer $analyzer,
        protected StudyPlanTemplateService $templateService
    ) {}

    public function getTemplates(): JsonResponse
    {
        return response()->json([
            'templates' => array_values($this->templateService->getTemplates()),
        ]);
    }

    public function applyTemplate(ApplyTemplateRequest $request): JsonResponse
    {
        $validated = $request->validated();
        $count = $this->templateService->applyTemplate(
            $validated['template_id'],
            $validated['start_date'],
            $validated['preferred_time'] ?? '19:00',
            $request->boolean('replace_existing', false)
        );

        return response()->json([
            'message' => "Successfully applied study template! Created {$count} daily study sessions.",
            'count' => $count,
        ], 201);
    }

    public function getSuggestions(Request $request): JsonResponse
    {
        $track = (string) $request->query('track', 'All');
        $timeOfDay = (string) $request->query('time_of_day', 'Evening');
        $topicsPerDay = (int) $request->query('topics_per_day', '1');
        $suggestions = $this->analyzer->generateSuggestions($this->requireUser(), $track, $timeOfDay, $topicsPerDay);

        return response()->json($suggestions);
    }

    public function applySuggestions(ApplySuggestionsRequest $request): JsonResponse
    {
        $validated = $request->validated();
        $user = $this->requireUser();

        $created = [];

        foreach ($validated['suggestions'] as $suggestion) {
            $desc = $suggestion['description'] ?? '';

            if (! empty($suggestion['module_links']) && is_array($suggestion['module_links'])) {
                $desc .= "\n\nLinks:";
                foreach ($suggestion['module_links'] as $link) {
                    $desc .= ' ['.$link['title'].']('.$link['url'].')';
                }
            }

            $schedule = StudySchedule::firstOrCreate([
                'user_id' => $user->id,
                'study_date' => $suggestion['study_date'],
                'study_time' => $suggestion['study_time'] ?? null,
                'title' => $suggestion['title'],
            ], [
                'description' => $desc,
            ]);

            if ($schedule->wasRecentlyCreated) {
                $created[] = $schedule;
            }
        }

        return response()->json([
            'message' => count($created).' study sessions added to your calendar',
            'count' => count($created),
        ], 201);
    }
}
