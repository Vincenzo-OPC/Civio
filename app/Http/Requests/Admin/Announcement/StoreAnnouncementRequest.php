<?php

namespace App\Http\Requests\Admin\Announcement;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreAnnouncementRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'message' => ['required', 'string', 'max:5000'],
            'type' => ['required', Rule::in(['info', 'warning', 'success'])],
            'is_active' => ['boolean'],
            'expires_at' => ['nullable', 'date', 'after:today'],
            'last_checked_at' => ['nullable', 'date'],
        ];
    }
}
