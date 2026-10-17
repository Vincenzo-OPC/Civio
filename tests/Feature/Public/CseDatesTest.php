<?php

use App\Support\CseExamDates;
use Inertia\Testing\AssertableInertia as Assert;

test('the CSE 2027 dates page is public and passes every date with its source', function () {
    $this->get(route('cse-dates'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('public/cse-dates')
            ->where('lastChecked', CseExamDates::LAST_CHECKED)
            ->has('dates', count(CseExamDates::all())));
});

test('the March 2027 sitting carries the dates published in Exam Announcement No. 05, s. 2026', function () {
    $march = collect(CseExamDates::all())->where('sitting', '14 March 2027 CSE-PPT')->keyBy('label');

    expect($march['Filing opens']['date'])->toBe('2026-11-02')
        ->and($march['Filing opens']['status'])->toBe('confirmed')
        ->and($march['Exam day (Professional and Subprofessional)']['date'])->toBe('2027-03-14')
        ->and($march['Exam day (Professional and Subprofessional)']['status'])->toBe('confirmed')
        ->and($march['Results']['status'])->toBe('target')
        ->and($march['Filing opens']['source_title'])->toContain('Examination Announcement No. 05, s. 2026');
});

test('every row cites an official CSC page and a last-checked date', function () {
    foreach (CseExamDates::all() as $row) {
        expect(parse_url($row['source_url'], PHP_URL_SCHEME))->toBe('https')
            ->and(parse_url($row['source_url'], PHP_URL_HOST))->toBeIn(['csc.gov.ph', 'www.csc.gov.ph'])
            ->and($row['last_checked'])->toMatch('/^\d{4}-\d{2}-\d{2}$/')
            ->and($row['status'])->toBeIn(['confirmed', 'target', 'unconfirmed']);
    }
});

test('a row without a published date is never shown as confirmed', function () {
    foreach (CseExamDates::all() as $row) {
        if ($row['date'] === null) {
            expect($row['status'])->toBe('unconfirmed');
        } else {
            expect($row['date'])->toMatch('/^\d{4}-\d{2}-\d{2}$/');
        }

        if ($row['status'] === 'unconfirmed') {
            expect($row['date'])->toBeNull();
        }
    }
});

test('the sitemap lists the dates page', function () {
    $this->get('/sitemap.xml')->assertOk()->assertSee('/cse-2027-dates', false);
});
