<?php

declare(strict_types=1);

namespace App\Providers;

use App\Repositories\QuestionRepository;
use App\Repositories\QuestionRepositoryInterface;
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
    }
}
