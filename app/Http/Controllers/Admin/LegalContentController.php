<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\Legal\LegalContentRequest;
use App\Models\LegalContent;

class LegalContentController extends Controller
{
    public function edit()
    {
        $privacy = LegalContent::where('type', 'privacy')->first();
        $terms = LegalContent::where('type', 'terms')->first();

        return $this->render('admin/legal-content/edit', [
            'privacy' => $privacy,
            'terms' => $terms,
        ]);
    }

    public function update(LegalContentRequest $request)
    {
        $validated = $request->validated();

        foreach ($validated['content'] as $type => $content) {
            LegalContent::updateOrCreate(
                ['type' => $type],
                ['content' => $content]
            );
        }

        return $this->backWithSuccess('Legal content updated successfully.');
    }
}
