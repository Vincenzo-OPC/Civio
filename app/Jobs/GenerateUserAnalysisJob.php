<?php

namespace App\Jobs;

use App\Events\AiGenerationCompleted;
use App\Models\UserAiAnalysis;
use App\Services\Ai\AiGatewayService;
use App\Services\DeterministicAnalysisService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class GenerateUserAnalysisJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $timeout = 300;

    public $tries = 3;

    public function __construct(
        protected int $userId,
        protected int $latestAttemptId,
        protected string $primaryModel = AiGatewayService::DEFAULT_WORKERS_AI_MODEL
    ) {}

    public function handle(): void
    {
        set_time_limit(300);
        Log::info("GenerateUserAnalysisJob: Started for user {$this->userId} with attempt {$this->latestAttemptId}");

        try {
            $deterministicService = new DeterministicAnalysisService;
            $deterministicData = $deterministicService->generate($this->userId, $this->latestAttemptId);

            $aiGateway = app(AiGatewayService::class);
            $cfConfigured = $aiGateway->isWorkersAiConfigured();
            $geminiConfigured = $aiGateway->isGeminiConfigured();

            if (! $cfConfigured && ! $geminiConfigured) {
                Log::info('GenerateUserAnalysisJob: No AI credentials configured. Saving deterministic analysis directly.');
                UserAiAnalysis::updateOrCreate(
                    ['user_id' => $this->userId],
                    [
                        'last_exam_attempt_id' => $this->latestAttemptId,
                        'analysis_json' => $deterministicData,
                    ]
                );
                event(new AiGenerationCompleted($this->userId, 'analysis', 'analysis'));

                return;
            }

            $passProb = $deterministicData['pass_probability'] ?? 0;
            $scoreTier = $passProb >= 80 ? 'High (80%+)' : ($passProb >= 60 ? 'Moderate (60-79%)' : 'Needs Improvement (<60%)');
            $topStrengths = array_slice($deterministicData['strengths'] ?? [], 0, 2);
            $topWeaknesses = array_slice($deterministicData['critical_weaknesses'] ?? [], 0, 2);
            $topModule = ($deterministicData['recommended_modules'] ?? [])[0] ?? 'General Review';

            $normalizedProfile = [
                'score_tier' => $scoreTier,
                'pass_probability' => $passProb,
                'strengths' => $topStrengths,
                'critical_weaknesses' => $topWeaknesses,
                'priority_focus' => $topModule,
                'draft_verdict' => $deterministicData['verdict'] ?? '',
                'draft_encouragement' => $deterministicData['encouragement'] ?? '',
                'draft_priority_action' => $deterministicData['priority_action'] ?? '',
            ];

            $systemPrompt = "You are an encouraging and expert Philippine Civil Service Examination coach.
Rewrite the coaching commentary fields to make them highly personalized, professional, and natural.

CRITICAL RULES:
1. Rewrite only the following text fields: `verdict`, `encouragement`, `priority_action`.
2. STRICT THEMATIC CONSISTENCY: Your `priority_action` and `encouragement` MUST strictly align with the student's top weakness in `critical_weaknesses` and top focus in `priority_focus`.
3. Keep the tone empathetic, practical, motivating, and culturally attuned to Philippine civil service examinees.
4. You must respond ONLY with a valid JSON object matching the provided schema.";

            $userPrompt = "Here is the student's performance profile:\n".json_encode($normalizedProfile)."\n\nPlease rewrite the verbal coaching fields (`verdict`, `encouragement`, `priority_action`).";

            $responseSchema = [
                'type' => 'OBJECT',
                'properties' => [
                    'verdict' => ['type' => 'STRING'],
                    'encouragement' => ['type' => 'STRING'],
                    'priority_action' => ['type' => 'STRING'],
                ],
                'required' => [
                    'verdict', 'encouragement', 'priority_action',
                ],
            ];

            $finalData = null;
            $errorMsg = null;

            // 1. Try Cloudflare Workers AI first as default
            if ($cfConfigured) {
                $cfModel = $aiGateway->isWorkersAiModel($this->primaryModel)
                    ? $this->primaryModel
                    : AiGatewayService::DEFAULT_WORKERS_AI_MODEL;

                Log::info("GenerateUserAnalysisJob: Calling Cloudflare Workers AI with model: {$cfModel}");
                $cfRes = $aiGateway->generateStructuredJson($cfModel, $systemPrompt, $userPrompt, $responseSchema);

                if ($cfRes['success'] && isset($cfRes['data']['verdict'])) {
                    $finalData = array_merge($deterministicData, array_filter($cfRes['data'], fn ($v) => ! is_null($v)));
                } else {
                    $errorMsg = $cfRes['error'] ?? 'Invalid response from Cloudflare Workers AI';
                    Log::warning("GenerateUserAnalysisJob: Cloudflare Workers AI failed or hit limit ({$errorMsg}), falling back to Gemini.");
                }
            }

            // 2. Fallback to Gemini if CF failed or wasn't configured
            if ($finalData === null && $geminiConfigured) {
                $geminiModel = ! $aiGateway->isWorkersAiModel($this->primaryModel)
                    ? $this->primaryModel
                    : AiGatewayService::FALLBACK_GEMINI_MODEL;

                Log::info("GenerateUserAnalysisJob: Calling Gemini API with model: {$geminiModel}");
                $geminiRes = $aiGateway->generateStructuredJson($geminiModel, $systemPrompt, $userPrompt, $responseSchema);

                if ($geminiRes['success'] && isset($geminiRes['data']['verdict'])) {
                    $finalData = array_merge($deterministicData, array_filter($geminiRes['data'], fn ($v) => ! is_null($v)));
                } else {
                    $errorMsg = $geminiRes['error'] ?? 'Invalid response from Gemini API';
                    Log::warning("GenerateUserAnalysisJob: Gemini API failed: {$errorMsg}");
                }
            }

            if ($finalData === null) {
                Log::warning('GenerateUserAnalysisJob: AI generation model failed, falling back to deterministic data: '.$errorMsg);
                UserAiAnalysis::updateOrCreate(
                    ['user_id' => $this->userId],
                    [
                        'last_exam_attempt_id' => $this->latestAttemptId,
                        'analysis_json' => $deterministicData,
                    ]
                );
                event(new AiGenerationCompleted($this->userId, 'analysis', 'analysis'));

                return;
            }

            UserAiAnalysis::updateOrCreate(
                ['user_id' => $this->userId],
                [
                    'last_exam_attempt_id' => $this->latestAttemptId,
                    'analysis_json' => $finalData,
                ]
            );

            Log::info("GenerateUserAnalysisJob: Successfully saved analysis and dispatched event for user {$this->userId}.");
            event(new AiGenerationCompleted($this->userId, 'analysis', 'analysis'));

        } catch (\Exception $e) {
            Log::error('GenerateUserAnalysisJob Exception, falling back to deterministic data: '.$e->getMessage());
            UserAiAnalysis::updateOrCreate(
                ['user_id' => $this->userId],
                [
                    'last_exam_attempt_id' => $this->latestAttemptId,
                    'analysis_json' => $deterministicData,
                ]
            );
            event(new AiGenerationCompleted($this->userId, 'analysis', 'analysis'));
        } finally {
            Cache::forget("ai-analysis-generating-{$this->userId}");
        }
    }
}
