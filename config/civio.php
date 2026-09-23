<?php

declare(strict_types=1);

$appEnv = env('APP_ENV', 'production');
$guestUnlimitedRaw = env('CIVIO_GUEST_UNLIMITED');

if ($guestUnlimitedRaw === null) {
    $guestUnlimited = in_array($appEnv, ['local', 'testing'], true);
} else {
    $guestUnlimited = filter_var($guestUnlimitedRaw, FILTER_VALIDATE_BOOLEAN);
}

return [
    'guest_unlimited' => $guestUnlimited,
    'explain_provider' => env('CIVIO_EXPLAIN_PROVIDER', 'stub'),
    'explain_api_key' => env('CIVIO_EXPLAIN_API_KEY'),
    'explain_model' => env('CIVIO_EXPLAIN_MODEL'),
    'explain_base_url' => env('CIVIO_EXPLAIN_BASE_URL'),
    'content_shield' => filter_var(env('CIVIO_CONTENT_SHIELD', false), FILTER_VALIDATE_BOOLEAN),
    'tutor_name' => env('CIVIO_TUTOR_NAME', 'Dexter'),
    'domain' => env('CIVIO_DOMAIN', 'civio.ph'),
];
