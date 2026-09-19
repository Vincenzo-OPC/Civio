<?php

namespace App\Http\Controllers\Admin;

use App\Enums\LegalContentType;
use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\Legal\LegalContentRequest;
use App\Repositories\LegalContentRepositoryInterface;

class LegalContentController extends Controller
{
    public function __construct(
        protected LegalContentRepositoryInterface $legalContentRepository
    ) {}

    public function edit()
    {
        $privacy = $this->legalContentRepository->findByType(LegalContentType::Privacy);
        $terms = $this->legalContentRepository->findByType(LegalContentType::Terms);

        return $this->render('admin/legal-content/edit', [
            'privacy' => $privacy,
            'terms' => $terms,
        ]);
    }

    public function update(LegalContentRequest $request)
    {
        $validated = $request->validated();

        $this->legalContentRepository->updateAllContents($validated['content']);

        return $this->backWithSuccess('Legal content updated successfully.');
    }
}
