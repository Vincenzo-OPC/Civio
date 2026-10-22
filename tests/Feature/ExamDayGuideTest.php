<?php

use Inertia\Testing\AssertableInertia as Assert;

test('the exam-day guide is public and renders its page', function () {
    $this->withoutVite()->get(route('exam-day'))->assertOk()
        ->assertInertia(fn (Assert $page) => $page->component('public/exam-day'));
});

test('every exam-day guide section cites an official csc.gov.ph source and no pass rate is invented', function () {
    $src = file_get_contents(resource_path('js/pages/public/exam-day.tsx'));

    expect($src)->toContain('https://www.csc.gov.ph/examination-advisories/examination-announcement-no-03-s-2026')
        ->toContain('https://www.csc.gov.ph/examination-advisories/examination-announcement-no-05-s-2026')
        ->not->toMatch('/pass(ing)? rate/i');
    expect(preg_match_all("/source: 'ann0\\d',/", $src))->toBe(preg_match_all("/title: '/", $src))->toBeGreaterThan(5);
});
