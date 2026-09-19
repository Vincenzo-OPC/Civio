<?php

namespace App\Http\Requests\Settings;

use App\Enums\AnalysisMode;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Enum;

class UpdatePreferencesRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'analysis_mode' => ['required', new Enum(AnalysisMode::class)],
        ];
    }
}
