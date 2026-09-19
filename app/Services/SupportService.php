<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Support\SupportMessageData;
use App\Mail\SupportSubmittedMail;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Validation\ValidationException;

class SupportService
{
    /**
     * @throws ValidationException
     */
    public function handleSubmission(SupportMessageData $data, string $ip): void
    {
        if (app()->isProduction() || config('services.support.test_rate_limit')) {
            if (RateLimiter::tooManyAttempts('support-submission:'.$ip, 1)) {
                throw ValidationException::withMessages([
                    'rate_limit' => 'You have already submitted a support request today. To prevent spam, submissions are limited to one per day.',
                ]);
            }

            RateLimiter::hit('support-submission:'.$ip, 86400); // 24 hours
        }

        Log::info('Support submission logged', [
            'name' => $data->name,
            'email' => $data->email,
            'message_length' => strlen($data->message),
        ]);

        $recipient = env('DEV_EMAIL', config('mail.from.address'));

        Mail::to($recipient)->send(new SupportSubmittedMail($data->toArray()));
    }
}
