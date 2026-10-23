<?php

use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Schedule;

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote');

// Issue #26: daily cleanup of abandoned guest exam sessions. Runs only where
// the Laravel scheduler (`php artisan schedule:run` every minute) is enabled.
Schedule::command('civio:prune-exam-sessions')->dailyAt('03:30')->withoutOverlapping()->onOneServer();
