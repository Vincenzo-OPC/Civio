<?php

declare(strict_types=1);

namespace App\Http\Requests\User\Exam;

use Illuminate\Foundation\Http\FormRequest;

final class ExportPdfRequest extends FormRequest
{
    public function authorize(): bool
    {
        // Permission is checked by checkPdfExportLimit before any key is read.
        return true;
    }

    /** @return array<string, string> */
    public function rules(): array
    {
        return [
            'track' => 'required|string|in:Professional,Subprofessional',
            'question_ids' => 'prohibited',
            'exam_session_id' => 'prohibited',
        ];
    }
}
