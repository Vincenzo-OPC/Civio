<?php

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
];
