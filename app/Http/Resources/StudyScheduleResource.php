<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\StudySchedule;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin StudySchedule
 */
class StudyScheduleResource extends JsonResource
{
    /**
     * The "data" wrapper that should be applied.
     *
     * @var string|null
     */
    public static $wrap = null;

    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $studyDate = $this->study_date instanceof \DateTimeInterface
            ? $this->study_date->format('Y-m-d')
            : (is_string($this->study_date) ? $this->study_date : null);

        $studyTime = $this->study_time instanceof \DateTimeInterface
            ? $this->study_time->format('H:i')
            : (is_string($this->study_time) ? substr($this->study_time, 0, 5) : null);

        return [
            'id' => $this->id,
            'user_id' => $this->user_id,
            'study_date' => $studyDate,
            'study_time' => $studyTime,
            'title' => $this->title,
            'description' => $this->description,
            'subcategory_id' => $this->subcategory_id,
            'is_done' => (bool) $this->is_done,
            'subcategory' => $this->whenLoaded('subcategory'),
            'created_at' => $this->created_at?->toISOString() ?? $this->created_at,
            'updated_at' => $this->updated_at?->toISOString() ?? $this->updated_at,
        ];
    }
}
