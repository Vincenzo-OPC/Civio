<?php

declare(strict_types=1);

namespace App\Http\Requests\User\Offline;

use App\Data\Offline\OfflineAnswer;
use Illuminate\Foundation\Http\FormRequest;

/** Queued offline drill answers (Lite L2). Guests allowed. */
class SyncOfflineAttemptsRequest extends FormRequest
{
    public const MAX_ITEMS = 200;

    public function authorize(): bool
    {
        return true;
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'attempts' => ['required', 'array', 'min:1', 'max:'.self::MAX_ITEMS],
            'attempts.*.client_id' => ['required', 'string', 'max:64', 'regex:/^[A-Za-z0-9_-]+$/', 'distinct'],
            'attempts.*.question_id' => ['required', 'integer', 'min:1'],
            'attempts.*.selected_option' => ['required', 'integer', 'min:0', 'max:9'],
            'attempts.*.claimed_correct_option' => ['required', 'integer', 'min:0', 'max:9'],
            'attempts.*.pack_version' => ['nullable', 'string', 'max:40'],
            'attempts.*.answered_at' => ['nullable', 'date'],
        ];
    }

    /** @return list<OfflineAnswer> */
    public function answers(): array
    {
        /** @var array<int, array<string, mixed>> $attempts */
        $attempts = $this->validated('attempts');

        return array_values(array_map(OfflineAnswer::fromArray(...), $attempts));
    }

    /** Stable owner for idempotency: user id, or a hash of the guest session. */
    public function ownerKey(): string
    {
        $user = $this->user();

        return $user !== null
            ? 'u:'.$user->getAuthIdentifier()
            : 'g:'.hash('sha256', $this->session()->getId());
    }
}
