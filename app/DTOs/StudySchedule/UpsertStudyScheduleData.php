<?php

declare(strict_types=1);

namespace App\DTOs\StudySchedule;

use App\Http\Requests\User\StudySchedule\StoreStudyScheduleRequest;
use App\Http\Requests\User\StudySchedule\UpdateStudyScheduleRequest;

readonly class UpsertStudyScheduleData
{
    public function __construct(
        public ?string $studyDate,
        public ?string $studyTime,
        public ?string $title,
        public ?string $description = null,
        public ?int $subcategoryId = null,
        public ?bool $isDone = null,
    ) {}

    public static function fromStoreRequest(StoreStudyScheduleRequest $request): self
    {
        $v = $request->validated();

        return new self(
            studyDate: (string) $v['study_date'],
            studyTime: isset($v['study_time']) ? (string) $v['study_time'] : null,
            title: (string) $v['title'],
            description: isset($v['description']) ? (string) $v['description'] : null,
            subcategoryId: isset($v['subcategory_id']) ? (int) $v['subcategory_id'] : null,
            isDone: isset($v['is_done']) ? (bool) $v['is_done'] : false,
        );
    }

    public static function fromUpdateRequest(UpdateStudyScheduleRequest $request): self
    {
        $v = $request->validated();

        $studyTime = isset($v['study_time']) ? (string) $v['study_time'] : null;
        if ($studyTime !== null && strlen($studyTime) === 5) {
            $studyTime .= ':00';
        }

        return new self(
            studyDate: isset($v['study_date']) ? (string) $v['study_date'] : null,
            studyTime: $studyTime,
            title: isset($v['title']) ? (string) $v['title'] : null,
            description: array_key_exists('description', $v) ? (string) $v['description'] : null,
            subcategoryId: array_key_exists('subcategory_id', $v) && $v['subcategory_id'] !== null ? (int) $v['subcategory_id'] : null,
            isDone: isset($v['is_done']) ? (bool) $v['is_done'] : null,
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        $data = [];

        if ($this->studyDate !== null) {
            $data['study_date'] = $this->studyDate;
        }
        if ($this->studyTime !== null) {
            $data['study_time'] = $this->studyTime;
        }
        if ($this->title !== null) {
            $data['title'] = $this->title;
        }
        if ($this->description !== null) {
            $data['description'] = $this->description;
        }
        if ($this->subcategoryId !== null) {
            $data['subcategory_id'] = $this->subcategoryId;
        }
        if ($this->isDone !== null) {
            $data['is_done'] = $this->isDone;
        }

        return $data;
    }
}
