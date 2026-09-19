<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\ExamDate\StoreExamDateRequest;
use App\Http\Requests\Admin\ExamDate\UpdateExamDateRequest;
use App\Models\ExamDate;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;

class ExamDateController extends Controller
{
    public function index()
    {
        $examDates = ExamDate::orderBy('date', 'desc')->get();

        return Inertia::render('admin/exam-dates/index', [
            'examDates' => $examDates,
        ]);
    }

    public function store(StoreExamDateRequest $request)
    {
        Gate::authorize('create', ExamDate::class);

        $validated = $request->validated();

        ExamDate::create([
            'date' => $validated['date'],
            'description' => $validated['description'],
            'is_active' => $validated['is_active'] ?? true,
        ]);

        Cache::forget('exam_dates.active');

        return $this->backWithSuccess('Exam date added successfully.');
    }

    public function update(UpdateExamDateRequest $request, ExamDate $examDate)
    {
        Gate::authorize('update', $examDate);

        $validated = $request->validated();

        $examDate->update([
            'date' => $validated['date'],
            'description' => $validated['description'],
            'is_active' => $request->has('is_active') ? $validated['is_active'] : $examDate->is_active,
        ]);

        Cache::forget('exam_dates.active');

        return $this->backWithSuccess('Exam date updated successfully.');
    }

    public function destroy(ExamDate $examDate)
    {
        Gate::authorize('delete', $examDate);

        $examDate->delete();
        Cache::forget('exam_dates.active');

        return $this->backWithSuccess('Exam date deleted successfully.');
    }
}
