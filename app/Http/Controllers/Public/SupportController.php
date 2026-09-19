<?php

namespace App\Http\Controllers\Public;

use App\DTOs\Support\SupportMessageData;
use App\Http\Controllers\Controller;
use App\Http\Requests\Public\SupportRequest;
use App\Services\SupportService;
use Illuminate\Http\RedirectResponse;

class SupportController extends Controller
{
    public function __construct(
        protected SupportService $supportService
    ) {}

    /**
     * Handle the incoming contact support request.
     */
    public function store(SupportRequest $request): RedirectResponse
    {
        $dto = SupportMessageData::fromRequest($request);

        $this->supportService->handleSubmission($dto, (string) $request->ip());

        return back()->with([
            'success' => 'Thank you for reaching out, '.$dto->name.'! We have received your message and will reply within 24 hours.',
        ]);
    }
}
