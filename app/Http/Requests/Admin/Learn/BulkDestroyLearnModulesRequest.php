<?php

namespace App\Http\Requests\Admin\Learn;

use Illuminate\Foundation\Http\FormRequest;

class BulkDestroyLearnModulesRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'ids' => ['required', 'array'],
            'ids.*' => ['integer', 'exists:learn_modules,id'],
        ];
    }
}
