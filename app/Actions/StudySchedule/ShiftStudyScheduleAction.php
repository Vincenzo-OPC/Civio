<?php

declare(strict_types=1);

namespace App\Actions\StudySchedule;

use App\DTOs\StudySchedule\ShiftScheduleData;
use App\Repositories\StudyScheduleRepositoryInterface;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;

class ShiftStudyScheduleAction
{
    public function __construct(
        protected StudyScheduleRepositoryInterface $scheduleRepository
    ) {}

    public function execute(int $userId, ShiftScheduleData $data): int
    {
        $incompleteSchedules = $this->scheduleRepository->getIncompleteSchedules($userId);

        if ($incompleteSchedules->isEmpty()) {
            return 0;
        }

        $today = Carbon::today();

        return DB::transaction(function () use ($data, $incompleteSchedules, $today) {
            $count = 0;

            if ($data->mode === 'start_today') {
                $earliest = Carbon::parse($incompleteSchedules->first()->study_date)->startOfDay();
                $dayDifference = $earliest->diffInDays($today, false);

                if ($dayDifference > 0) {
                    foreach ($incompleteSchedules as $schedule) {
                        $originalDate = Carbon::parse($schedule->study_date);
                        $newDate = $originalDate->copy()->addDays($dayDifference);
                        $this->scheduleRepository->update($schedule->id, [
                            'study_date' => $newDate->toDateString(),
                        ]);
                        $count++;
                    }
                }
            } elseif ($data->mode === 'shift_by_days') {
                $days = $data->days;
                $fromDate = ! empty($data->fromDate) ? Carbon::parse($data->fromDate)->startOfDay() : null;

                foreach ($incompleteSchedules as $schedule) {
                    $schedDate = Carbon::parse($schedule->study_date)->startOfDay();

                    if ($fromDate && $schedDate->lt($fromDate)) {
                        continue;
                    }

                    $newDate = $schedDate->copy()->addDays($days);
                    $this->scheduleRepository->update($schedule->id, [
                        'study_date' => $newDate->toDateString(),
                    ]);
                    $count++;
                }
            }

            return $count;
        });
    }
}
