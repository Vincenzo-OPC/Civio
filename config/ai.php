<?php

use App\Services\Ai\OwnerAiSpendLock;
use Illuminate\Support\Env;

return [
    /*
    | Default tutor provider. "null" works with no API keys.
    | Future values (prism-backed): gemini, openai, xai, anthropic, stub.
    */
    'tutor_provider' => env('CIVIO_TUTOR_PROVIDER', 'null'),

    /*
    | When using Prism-backed providers, keys stay server-side only.
    | Never put these in VITE_* variables.
    */
    'prism_default_provider' => env('PRISM_PROVIDER', env('CIVIO_TUTOR_PROVIDER', 'null')),

    /*
    | Issue #18: fail-closed owner-funded AI lock. OFF unless the raw env value
    | is exactly "true" (not "1", "yes", "TRUE", "on"). Ignored in production.
    | Credentials alone never enable a request.
    */
    'owner_funded_inference_enabled' => OwnerAiSpendLock::parseFlag(Env::getRepository()->get('CIVIO_OWNER_FUNDED_AI')),
];
