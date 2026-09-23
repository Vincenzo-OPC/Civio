<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Services\Dexter\ExplainQuestionService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class DexterExplainController extends Controller
{
    public function __construct(
        protected ExplainQuestionService $explainer
    ) {}

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'stem' => ['required', 'string', 'max:8000'],
            'options' => ['required', 'array', 'min:2', 'max:8'],
            'options.*' => ['required', 'string', 'max:2000'],
            'chosen_index' => ['nullable', 'integer', 'min:0', 'max:7'],
            'correct_index' => ['required', 'integer', 'min:0', 'max:7'],
            'explanation' => ['nullable', 'string', 'max:8000'],
            'category' => ['nullable', 'string', 'max:200'],
            'subcategory' => ['nullable', 'string', 'max:200'],
        ]);

        $explain = $this->explainer->explain($data);

        return response()->json([
            'success' => true,
            'tutor' => (string) config('civio.tutor_name', 'Dexter'),
            'explain' => $explain,
        ]);
    }
}
