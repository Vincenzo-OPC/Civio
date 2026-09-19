<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\DTOs\StudySchedule\ShiftScheduleData;
use App\DTOs\StudySchedule\UpsertStudyScheduleData;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\StudySchedule\BulkDeleteStudyScheduleRequest;
use App\Http\Requests\User\StudySchedule\BulkMarkDoneRequest;
use App\Http\Requests\User\StudySchedule\BulkRescheduleTodayRequest;
use App\Http\Requests\User\StudySchedule\BulkUpdateStudyTimeRequest;
use App\Http\Requests\User\StudySchedule\ShiftStudyScheduleRequest;
use App\Http\Requests\User\StudySchedule\StoreStudyScheduleRequest;
use App\Http\Requests\User\StudySchedule\UpdateStudyScheduleRequest;
use App\Http\Resources\StudyScheduleResource;
use App\Models\StudySchedule;
use App\Services\StudyScheduleService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Response;

class StudyScheduleController extends Controller
{
    public function __construct(
        protected StudyScheduleService $scheduleService
    ) {}

    public function index(Request $request): Response
    {
        $year = (int) $request->query('year', (string) now()->year);
        $month = (int) $request->query('month', (string) now()->month);

        $calendarData = $this->scheduleService->getCalendarData($this->requireUser()->id, $year, $month);

        return $this->render('user/calendar/index', $calendarData);
    }

    public function data(Request $request): JsonResponse
    {
        $year = (int) $request->query('year', (string) now()->year);
        $month = (int) $request->query('month', (string) now()->month);

        $calendarData = $this->scheduleService->getCalendarData($this->requireUser()->id, $year, $month);

        return response()->json($calendarData);
    }

    public function store(StoreStudyScheduleRequest $request): JsonResponse
    {
        $dto = UpsertStudyScheduleData::fromStoreRequest($request);
        $result = $this->scheduleService->createSchedule($this->requireUser()->id, $dto);

        if ($result['is_duplicate']) {
            return response()->json([
                'message' => 'A study item with the same title already exists on this date.',
                'duplicate' => new StudyScheduleResource($result['duplicate']),
            ], 409);
        }

        return response()->json(new StudyScheduleResource($result['schedule']), 201);
    }

    public function update(UpdateStudyScheduleRequest $request, StudySchedule $studySchedule): JsonResponse
    {
        Gate::authorize('update', $studySchedule);

        $dto = UpsertStudyScheduleData::fromUpdateRequest($request);
        $updated = $this->scheduleService->updateSchedule($studySchedule, $dto);

        return response()->json(new StudyScheduleResource($updated));
    }

    public function getSubcategories(): JsonResponse
    {
        return response()->json($this->scheduleService->getAvailableSubcategoriesAndModules());
    }

    public function bulkUpdateTime(BulkUpdateStudyTimeRequest $request): JsonResponse
    {
        $validated = $request->validated();

        $this->scheduleService->bulkUpdateStudyTime(
            $this->requireUser()->id,
            $validated['study_time'] ?? null,
            $validated['start_date'] ?? null,
            $validated['end_date'] ?? null,
            isset($validated['category_id']) ? (int) $validated['category_id'] : null
        );

        return response()->json(['message' => 'Study times updated successfully.']);
    }

    public function bulkRescheduleToday(BulkRescheduleTodayRequest $request): JsonResponse
    {
        $count = $this->scheduleService->bulkRescheduleToday(
            $this->requireUser()->id,
            $request->validated('ids') ?? []
        );

        return response()->json([
            'message' => "Successfully rescheduled {$count} study sessions to today.",
            'count' => $count,
        ]);
    }

    public function bulkMarkDone(BulkMarkDoneRequest $request): JsonResponse
    {
        $count = $this->scheduleService->bulkMarkDone(
            $this->requireUser()->id,
            $request->validated('ids') ?? []
        );

        return response()->json([
            'message' => "Successfully marked {$count} study sessions as completed.",
            'count' => $count,
        ]);
    }

    public function bulkDelete(BulkDeleteStudyScheduleRequest $request): JsonResponse
    {
        $validated = $request->validated();

        $count = $this->scheduleService->bulkDelete(
            $this->requireUser()->id,
            $validated['ids'] ?? [],
            $validated['scope'] ?? null,
            $validated['date'] ?? null
        );

        return response()->json([
            'message' => "Successfully deleted {$count} study sessions.",
            'count' => $count,
        ]);
    }

    public function destroyAll(): JsonResponse
    {
        $this->scheduleService->destroyAll($this->requireUser()->id);

        return response()->json(null, 204);
    }

    public function shiftSchedule(ShiftStudyScheduleRequest $request): JsonResponse
    {
        $dto = ShiftScheduleData::fromRequest($request);
        $count = $this->scheduleService->shiftSchedule($this->requireUser()->id, $dto);

        if ($count === 0) {
            return response()->json([
                'message' => 'No incomplete study sessions to shift.',
                'count' => 0,
            ]);
        }

        return response()->json([
            'message' => "Successfully shifted {$count} study sessions.",
            'count' => $count,
        ]);
    }

    public function destroy(StudySchedule $studySchedule): JsonResponse
    {
        Gate::authorize('delete', $studySchedule);

        $this->scheduleService->deleteSchedule($studySchedule);

        return response()->json(null, 204);
    }
}
