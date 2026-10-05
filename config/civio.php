<?php

declare(strict_types=1);

/**
 * Local-study / CIVIO guest policy flags.
 * Production should keep guest_unlimited=false so free-attempt walls stay.
 */
return [
    // When true: guests may start unlimited mocks, submit, see scorecard/review,
    // and start another mock without forced register redirects.
    'guest_unlimited' => filter_var(
        env('CIVIO_GUEST_UNLIMITED', true),
        FILTER_VALIDATE_BOOLEAN
    ),

    // When false: content shield is disabled (copy/paste allowed for study).
    // Set CIVIO_CONTENT_SHIELD=true only for real production exams.
    'content_shield' => filter_var(
        env('CIVIO_CONTENT_SHIELD', false),
        FILTER_VALIDATE_BOOLEAN
    ),

    'allow_browser_migrations' => (bool) env('CIVIO_ALLOW_BROWSER_MIGRATIONS', false),
];
