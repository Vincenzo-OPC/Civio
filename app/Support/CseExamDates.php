<?php

declare(strict_types=1);

namespace App\Support;

use Carbon\CarbonImmutable;
use Carbon\CarbonInterface;

/**
 * Public CSE 2027 dates, copied by hand from official CSC pages only.
 *
 * Every row names its source and the day it was last checked. A row without a
 * published date stays "unconfirmed" with a null date; never fill one in from
 * reviewers, news sites or social media. Update LAST_CHECKED whenever the CSC
 * pages are re-read, even if nothing changed.
 */
final class CseExamDates
{
    public const LAST_CHECKED = '2026-10-17';

    public const ANNOUNCEMENT_TITLE = 'CSC Examination Announcement No. 05, s. 2026 (CY 2027 Pen and Paper Test calendar, published 03 September 2026)';

    public const ANNOUNCEMENT_URL = 'https://csc.gov.ph/examination-advisories/examination-announcement-no-05-s-2026-calendar-of-civil-service-examinations-pen-and-paper-test-for-cy-2027';

    public const ADVISORIES_URL = 'https://www.csc.gov.ph/examination-advisories';

    /**
     * @return list<array{sitting: string, label: string, date: ?string, status: 'confirmed'|'target'|'unconfirmed', note: ?string, source_title: string, source_url: string, last_checked: string}>
     */
    public static function all(): array
    {
        $row = fn (string $sitting, string $label, ?string $date, string $status, ?string $note = null, ?string $title = null, ?string $url = null): array => [
            'sitting' => $sitting,
            'label' => $label,
            'date' => $date,
            'status' => $status,
            'note' => $note,
            'source_title' => $title ?? self::ANNOUNCEMENT_TITLE,
            'source_url' => $url ?? self::ANNOUNCEMENT_URL,
            'last_checked' => self::LAST_CHECKED,
        ];

        $march = '14 March 2027 CSE-PPT';
        $august = '08 August 2027 CSE-PPT';

        return [
            $row($march, 'Filing opens', '2026-11-02', 'confirmed', 'Applications are accepted continuously until slots are filled or the CSC announces otherwise.'),
            $row($march, 'Filing closes', null, 'unconfirmed', 'No closing date is published. Slots (350,000 target) can run out early.'),
            $row($march, 'Detailed announcement (testing centers, requirements, how to file)', null, 'unconfirmed', 'The CSC says it issues this three weeks before filing opens. It was not on the CSC advisories page when last checked.', 'CSC Examination Advisories', self::ADVISORIES_URL),
            $row($march, 'Exam day (Professional and Subprofessional)', '2027-03-14', 'confirmed'),
            $row($march, 'Results', '2027-05-11', 'target', 'This is the CSC target release date, not a promise.'),
            $row($august, 'Filing opens', '2027-05-10', 'confirmed'),
            $row($august, 'Exam day (Professional and Subprofessional)', '2027-08-08', 'confirmed'),
            $row($august, 'Results', '2027-10-05', 'target', 'This is the CSC target release date, not a promise.'),
        ];
    }

    public const TIMEZONE = 'Asia/Manila';

    /**
     * Confirmed exam days and filing openings whose Philippine calendar day has
     * not ended yet, soonest first. An exam day stays listed for the whole of
     * that day in Manila, so "Exam Day Today" holds until PH midnight.
     *
     * @return array{sittings: list<array{date: string, sitting: string, label: string}>, milestones: list<array{date: string, sitting: string, label: string, kind: 'filing_opens'|'exam_day'}>, source_title: string, source_url: string, last_checked: string}
     */
    public static function upcoming(?CarbonInterface $now = null): array
    {
        $today = CarbonImmutable::instance($now ?? CarbonImmutable::now())
            ->setTimezone(self::TIMEZONE)
            ->toDateString();

        $sittings = [];
        $milestones = [];

        foreach (self::all() as $row) {
            if ($row['status'] !== 'confirmed' || $row['date'] === null || $row['date'] < $today) {
                continue;
            }

            $isExam = str_starts_with($row['label'], 'Exam day');
            $isFiling = $row['label'] === 'Filing opens';

            if (! $isExam && ! $isFiling) {
                continue;
            }

            $item = ['date' => $row['date'], 'sitting' => $row['sitting'], 'label' => $row['label']];

            if ($isExam) {
                $sittings[] = $item;
            }

            $milestones[] = $item + ['kind' => $isExam ? 'exam_day' : 'filing_opens'];
        }

        usort($sittings, fn (array $a, array $b): int => strcmp($a['date'], $b['date']));
        usort($milestones, fn (array $a, array $b): int => strcmp($a['date'], $b['date']));

        return [
            'sittings' => $sittings,
            'milestones' => $milestones,
            'source_title' => self::ANNOUNCEMENT_TITLE,
            'source_url' => self::ANNOUNCEMENT_URL,
            'last_checked' => self::LAST_CHECKED,
        ];
    }
}
