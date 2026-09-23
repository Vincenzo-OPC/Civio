<?php

test('the public guide renders the exam path notes', function () {
    $this->withoutVite();

    $this->get(route('guide'))
        ->assertOk()
        ->assertInertia(fn ($page) => $page->component('guide'));
});
