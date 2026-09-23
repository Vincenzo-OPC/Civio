<?php

declare(strict_types=1);

namespace App\Http\Requests\Community;

use App\Rules\NoEmojis;
use App\Rules\NoHtml;
use App\Rules\NoProfanity;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Validator;

class StoreRecalledQuestionRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /**
     * @return array<string, mixed>
     */
    public function rules(): array
    {
        return [
            'stem' => ['required', 'string', 'min:12', 'max:2000', new NoHtml, new NoEmojis, new NoProfanity],
            'options' => ['nullable', 'array', 'max:5'],
            'options.*' => ['nullable', 'string', 'max:500', new NoHtml],
            'correct_option' => ['nullable', 'integer', 'min:0', 'max:4'],
            'category' => ['nullable', 'string', 'max:200'],
            'subcategory' => ['nullable', 'string', 'max:200'],
            'note' => ['nullable', 'string', 'max:1000', new NoHtml, new NoProfanity],
        ];
    }

    public function withValidator(Validator $validator): void
    {
        $validator->after(function (Validator $validator): void {
            $blob = strtolower(implode(' ', [
                (string) $this->input('stem', ''),
                (string) $this->input('note', ''),
            ]));

            if (preg_match('/official\s+(csc|csdex)|exact\s+(csc|exam)\s+(paper|question)|leaked\s+exam/i', $blob) === 1) {
                $validator->errors()->add(
                    'stem',
                    'Submit a paraphrase for practice. Do not claim this is an official CSC or CSDEx paper.'
                );
            }
        });
    }
}
