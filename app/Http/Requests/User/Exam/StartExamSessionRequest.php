<?php

declare(strict_types=1);

namespace App\Http\Requests\User\Exam;

use Illuminate\Foundation\Http\FormRequest;

class StartExamSessionRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Bias inputs only reorder which bank items are picked; they can never
     * reveal answer keys. Sizes are capped.
     */
    public function rules(): array
    {
        return [
            'track' => ['required', 'string', 'in:professional,subprofessional,Professional,Subprofessional'],
            'bias' => ['sometimes', 'array'],
            'bias.wrong_ids' => ['sometimes', 'array', 'max:2000'],
            'bias.wrong_ids.*' => ['integer'],
            'bias.weak_subcategories' => ['sometimes', 'array', 'max:100'],
            'bias.weak_subcategories.*' => ['string', 'max:191'],
            'bias.weak_categories' => ['sometimes', 'array', 'max:20'],
            'bias.weak_categories.*' => ['string', 'max:191'],
        ];
    }
}
