<?php

declare(strict_types=1);

/**
 * Local-study / CIVIO guest policy flags.
 * Production should keep guest_unlimited=false so free-attempt walls stay.
 */
return [
    // When true: guests may start unlimited mocks, submit, see scorecard/review,
    // and start another mock without forced register redirects.
    // Unset defaults to true only for APP_ENV=local/testing (local study);
    // any other environment (production, staging) defaults to false so a
    // missing variable never opens unlimited guest access. Docker study
    // stacks set CIVIO_GUEST_UNLIMITED=true explicitly.
    'guest_unlimited' => filter_var(
        env('CIVIO_GUEST_UNLIMITED', in_array(env('APP_ENV', 'production'), ['local', 'testing'], true)),
        FILTER_VALIDATE_BOOLEAN
    ),

    // When false: content shield is disabled (copy/paste allowed for study).
    // Set CIVIO_CONTENT_SHIELD=true only for real production exams.
    'content_shield' => filter_var(
        env('CIVIO_CONTENT_SHIELD', false),
        FILTER_VALIDATE_BOOLEAN
    ),

    'allow_browser_migrations' => (bool) env('CIVIO_ALLOW_BROWSER_MIGRATIONS', false),

    // Node binary that runs scripts/fsrs-apply.mjs. The production image
    // keeps this binary and ts-fsrs, and does not keep npm.
    'fsrs_node' => env('CIVIO_FSRS_NODE', 'node'),

    // One learner at a time. The lock is held while Node runs so two
    // submits cannot schedule the same card from the same old state.
    // The wait is long enough for one 5 second Node timeout. A timeout
    // leaves the event unscheduled.
    'fsrs_lock_seconds' => (int) env('CIVIO_FSRS_LOCK_SECONDS', 20),
    'fsrs_lock_wait' => (int) env('CIVIO_FSRS_LOCK_WAIT', 10),

    // Lite L2 offline drill packs: request limits per user (or IP) per minute.
    'offline' => [
        'packs_per_minute' => (int) env('CIVIO_OFFLINE_PACKS_PER_MINUTE', 60),
        'sync_per_minute' => (int) env('CIVIO_OFFLINE_SYNC_PER_MINUTE', 20),
    ],

    // Abandoned exam-session pruning (civio:prune-exam-sessions, daily).
    // Local study recovery promises 30 days, so retention is clamped to
    // 31..365 days whatever the env says. Default 45 leaves a 15-day margin.
    'prune_exam_sessions' => [
        'retention_days' => (int) env('CIVIO_EXAM_SESSION_RETENTION_DAYS', 45),
        'min_days' => 31,
        'max_days' => 365,
        'batch_size' => 500,
    ],
];
