<?php

namespace App\Http\Controllers\Settings;

use App\Http\Controllers\Controller;
use App\Http\Requests\Settings\UpdatePreferencesRequest;
use App\Services\UserPreferenceService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

class PreferencesController extends Controller
{
    public function __construct(
        protected UserPreferenceService $preferenceService
    ) {}

    /**
     * Show the user's preferences page.
     */
    public function edit(Request $request): Response
    {
        $userId = $request->user()->id;

        return $this->render('settings/preferences', [
            'analysisMode' => $this->preferenceService->getAnalysisMode($userId),
            'aiAvailable' => $this->preferenceService->isAiAvailable(),
        ]);
    }

    /**
     * Update the user's preferences.
     */
    public function update(UpdatePreferencesRequest $request): RedirectResponse
    {
        $userId = $request->user()->id;
        $mode = $request->validated('analysis_mode');

        $this->preferenceService->switchAnalysisMode($userId, $mode);

        Inertia::flash('toast', ['type' => 'success', 'message' => __('Analysis preferences updated.')]);

        return to_route('preferences.edit');
    }
}
