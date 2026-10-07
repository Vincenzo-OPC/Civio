<?php

namespace App\Http\Requests\User\Exam;

use Illuminate\Foundation\Http\FormRequest;

class StoreExamAttemptRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    protected function prepareForValidation(): void
    {
        // Flatten legacy cat_scores.metadata into metadata for validation / DTO.
        if (! $this->has('metadata') && $this->has('cat_scores')) {
            $catScores = $this->input('cat_scores', []);
            if (is_array($catScores) && isset($catScores['metadata']) && is_array($catScores['metadata'])) {
                $this->merge(['metadata' => $catScores['metadata']]);
            }
        }

        if (! $this->has('metadata') && ($this->has('score') || $this->has('track'))) {
            $this->merge([
                'metadata' => [
                    'track' => $this->input('track', 'Drill'),
                    'category_name' => $this->input('category_name', 'Practice Drill'),
                    'duration_secs' => $this->input('duration_secs', 0),
                    'is_timed' => $this->boolean('is_timed', true),
                    'question_times' => $this->input('question_times', []),
                    'answer_changes' => $this->input('answer_changes', []),
                    'selected_subcategories' => $this->input('selected_subcategories', []),
                    'language' => $this->input('language', 'English'),
                    'question_count' => $this->input('question_count', 30),
                ],
            ]);
        }
    }

    public function rules(): array
    {
        return [
            'category_id' => ['nullable', 'integer'],
            // Lite L1: server-picked mock this attempt belongs to (full mocks only).
            'exam_session_id' => ['sometimes', 'nullable', 'string', 'size:26'],
            'question_ids' => ['required', 'array', 'min:1'],
            'question_ids.*' => ['integer'],
            'answers' => ['required', 'array'],
            // Client may still send cat_scores for backward-compatible clients; ignored for scoring.
            'cat_scores' => ['sometimes', 'array'],
            'metadata' => ['sometimes', 'array'],
            'metadata.track' => ['sometimes', 'string'],
            'metadata.category_name' => ['sometimes', 'nullable', 'string'],
            'metadata.duration_secs' => ['sometimes', 'numeric'],
            'metadata.is_timed' => ['sometimes', 'boolean'],
            'metadata.question_times' => ['sometimes', 'array'],
            'metadata.answer_changes' => ['sometimes', 'array'],
            'metadata.selected_subcategories' => ['sometimes', 'array'],
            'metadata.language' => ['sometimes', 'string'],
            'metadata.question_count' => ['sometimes'],
        ];
    }
}
