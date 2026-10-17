<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Http\Resources\ExamQuestionResource;
use App\Repositories\QuestionRepositoryInterface;

final class PdfExamExportService
{
    public function __construct(
        private QuestionRepositoryInterface $questions,
        private MockPoolSelector $selector,
    ) {}

    /** @return array<int, array<string, mixed>> */
    public function questions(string $track): array
    {
        $pool = $this->questions->getActivePool()->keyBy('id');
        $rows = $pool->map(fn ($question) => MockSessionService::selectorRow($question))->values()->all();
        $selection = $this->selector->select($rows, MockPoolSelector::levelFor($track));
        $selected = [];

        foreach ($selection['items'] as $item) {
            $question = $pool->get($item['id']);
            $options = $question->options;
            $key = $question->correct_option;
            abort_unless(is_array($options) && array_is_list($options) && is_int($key)
                && $key >= 0 && $key < count($options), 422, 'An export item has an invalid answer key.');
            $selected[] = $question;
        }

        // Keep the stored option order: keys index exactly the choices printed.
        return ExamQuestionResource::collectionForExam($selected, true);
    }
}
