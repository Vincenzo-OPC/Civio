<?php

declare(strict_types=1);

namespace App\Providers;

use App\Repositories\ExamAttemptRepository;
use App\Repositories\ExamAttemptRepositoryInterface;
use App\Repositories\LearnModuleRepository;
use App\Repositories\LearnModuleRepositoryInterface;
use App\Repositories\QuestionRepository;
use App\Repositories\QuestionRepositoryInterface;
use App\Repositories\SavedDrillSetRepository;
use App\Repositories\SavedDrillSetRepositoryInterface;
use App\Repositories\StudyScheduleRepository;
use App\Repositories\StudyScheduleRepositoryInterface;
use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        $this->app->singleton(
            QuestionRepositoryInterface::class,
            QuestionRepository::class
        );

        $this->app->singleton(
            ExamAttemptRepositoryInterface::class,
            ExamAttemptRepository::class
        );

        $this->app->singleton(
            LearnModuleRepositoryInterface::class,
            LearnModuleRepository::class
        );

        $this->app->singleton(
            StudyScheduleRepositoryInterface::class,
            StudyScheduleRepository::class
        );

        $this->app->singleton(
            SavedDrillSetRepositoryInterface::class,
            SavedDrillSetRepository::class
        );
    }
}
