<?php

declare(strict_types=1);

namespace App\Services;

use App\Actions\StudySchedule\BulkUpdateStudyScheduleAction;
use App\Actions\StudySchedule\ShiftStudyScheduleAction;
use App\DTOs\StudySchedule\ShiftScheduleData;
use App\DTOs\StudySchedule\UpsertStudyScheduleData;
use App\Http\Resources\StudyScheduleResource;
use App\Models\ExamDate;
use App\Models\LearnModule;
use App\Models\StudySchedule;
use App\Models\Subcategory;
use App\Repositories\StudyScheduleRepositoryInterface;
use Carbon\Carbon;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Schema;

class StudyScheduleService
{
    public function __construct(
        protected StudyScheduleRepositoryInterface $scheduleRepository,
        protected ShiftStudyScheduleAction $shiftAction,
        protected BulkUpdateStudyScheduleAction $bulkAction
    ) {}

    /**
     * @return array{
     *     schedules: mixed,
     *     examDates: array<int, string>,
     *     pastPending: mixed,
     *     nextExam: ?array{date: string, description: string, days_remaining: int}
     * }
     */
    public function getCalendarData(int $userId, int $year, int $month): array
    {
        $startDate = now()->setDate($year, $month, 1)->startOfDay();
        $endDate = $startDate->copy()->endOfMonth();

        $rawSchedules = $this->scheduleRepository->getMonthSchedules($userId, $startDate, $endDate);

        $schedules = $rawSchedules
            ->groupBy(fn ($schedule) => $schedule->study_date->format('Y-m-d'))
            ->map(fn ($items) => StudyScheduleResource::collection($items)->resolve());

        $examDates = [];
        if (Schema::hasTable('exam_dates')) {
            $allExamDates = Cache::rememberForever('exam_dates.active', function () {
                return ExamDate::where('is_active', true)
                    ->get()
                    ->pluck('date')
                    ->map(fn ($date) => Carbon::parse($date)->format('Y-m-d'))
                    ->toArray();
            });

            $examDates = array_values(array_filter($allExamDates, function ($date) use ($startDate, $endDate) {
                return $date >= $startDate->format('Y-m-d') && $date <= $endDate->format('Y-m-d');
            }));
        }

        $rawPastPending = $this->scheduleRepository->getPastPending($userId);
        $pastPending = StudyScheduleResource::collection($rawPastPending)->resolve();

        $nextExam = null;
        if (Schema::hasTable('exam_dates')) {
            $nextExamModel = ExamDate::where('is_active', true)
                ->where('date', '>=', Carbon::today())
                ->orderBy('date', 'asc')
                ->first();

            if ($nextExamModel) {
                $nextExam = [
                    'date' => $nextExamModel->date->format('Y-m-d'),
                    'description' => $nextExamModel->description,
                    'days_remaining' => (int) Carbon::today()->diffInDays($nextExamModel->date, false),
                ];
            }
        }

        return [
            'schedules' => $schedules,
            'examDates' => $examDates,
            'pastPending' => $pastPending,
            'nextExam' => $nextExam,
        ];
    }

    /**
     * @return array{schedule?: StudySchedule, duplicate?: StudySchedule, is_duplicate: bool}
     */
    public function createSchedule(int $userId, UpsertStudyScheduleData $data): array
    {
        $existing = $this->scheduleRepository->findDuplicate($userId, (string) $data->studyDate, (string) $data->title);

        if ($existing) {
            return [
                'duplicate' => $existing,
                'is_duplicate' => true,
            ];
        }

        $attributes = array_merge(['user_id' => $userId], $data->toArray());
        $schedule = $this->scheduleRepository->create($attributes);

        return [
            'schedule' => $schedule,
            'is_duplicate' => false,
        ];
    }

    public function updateSchedule(StudySchedule $schedule, UpsertStudyScheduleData $data): StudySchedule
    {
        $this->scheduleRepository->update($schedule->id, $data->toArray());

        return $schedule->fresh(['subcategory.category']);
    }

    /**
     * @return array{
     *     subcategories: \Illuminate\Database\Eloquent\Collection<int, Subcategory>,
     *     modules: Collection<int, array{
     *         title: string,
     *         slug: string,
     *         topic: string,
     *         subcategory_name: ?string,
     *         category_name: ?string
     *     }>
     * }
     */
    public function getAvailableSubcategoriesAndModules(): array
    {
        $subcategories = Subcategory::whereHas('category', function ($query) {
            $query->where('is_demographic', false);
        })->orderBy('name')->get(['id', 'name', 'category_id']);

        $modules = LearnModule::where('is_published', true)
            ->with(['subcategory:id,name', 'category:id,name'])
            ->get(['id', 'title', 'slug', 'topic', 'subcategory_id', 'category_id']);

        return [
            'subcategories' => $subcategories,
            'modules' => $modules->map(fn ($m) => [
                'title' => $m->title,
                'slug' => $m->slug,
                'topic' => $m->topic,
                'subcategory_name' => $m->subcategory?->name,
                'category_name' => $m->category?->name,
            ]),
        ];
    }

    public function shiftSchedule(int $userId, ShiftScheduleData $data): int
    {
        return $this->shiftAction->execute($userId, $data);
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkRescheduleToday(int $userId, array $ids = []): int
    {
        return $this->bulkAction->rescheduleToday($userId, $ids);
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkMarkDone(int $userId, array $ids = []): int
    {
        return $this->bulkAction->markDone($userId, $ids);
    }

    public function bulkUpdateStudyTime(
        int $userId,
        ?string $time,
        ?string $startDate = null,
        ?string $endDate = null,
        ?int $categoryId = null
    ): int {
        return $this->bulkAction->updateStudyTime($userId, $time, $startDate, $endDate, $categoryId);
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkDelete(int $userId, array $ids = [], ?string $scope = null, ?string $date = null): int
    {
        return $this->bulkAction->delete($userId, $ids, $scope, $date);
    }

    public function destroyAll(int $userId): int
    {
        return $this->bulkAction->destroyAll($userId);
    }

    public function deleteSchedule(StudySchedule $schedule): bool
    {
        return $this->scheduleRepository->delete($schedule->id);
    }
}
