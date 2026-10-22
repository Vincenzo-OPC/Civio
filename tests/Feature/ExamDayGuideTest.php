<?php

use Inertia\Testing\AssertableInertia as Assert;

test('the exam-day guide is public and renders its page', function () {
    $this->withoutVite()->get(route('exam-day'))->assertOk()
        ->assertInertia(fn (Assert $page) => $page->component('public/exam-day'));
});
