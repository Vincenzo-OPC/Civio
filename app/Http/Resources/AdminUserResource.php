<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Enums\UserRole;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin User
 */
class AdminUserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'role' => $this->role instanceof UserRole ? $this->role->value : ($this->role ?? 'user'),
            'created_at' => $this->created_at ? $this->created_at->format('Y-m-d H:i') : 'N/A',
            'last_login_at' => $this->last_login_at ? $this->last_login_at->format('Y-m-d H:i') : 'Never',
            'is_active' => (bool) $this->is_active,
            'terms_accepted_at' => $this->terms_accepted_at ? $this->terms_accepted_at->format('Y-m-d H:i') : null,
            'deleted_at' => null,
            'attempts_count' => (int) ($this->attempts_count ?? 0),
            'mock_exams_count' => (int) ($this->mock_exams_count ?? 0),
            'drills_count' => (int) ($this->drills_count ?? 0),
            'pdf_downloads_count' => (int) ($this->pdf_downloads_count ?? 0),
            'can_download_pdf' => (bool) ($this->can_download_pdf ?? false),
        ];
    }
}
