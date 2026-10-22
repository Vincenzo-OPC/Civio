# Strict mock end-to-end checks (manual, headless)

These checks are not part of `npm run test:js`. They need a running app and headless Chrome.

`strict-mock.e2e.mjs` runs four scenarios, each as a fresh guest:

1. **Offline reload:** answer item 1 online, go offline and answer item 2, close the tab, reconnect and reopen `/exams`. Item 2 is restored with a notice and saved, item 1 is kept, and the local copy is cleared.
2. **Two tabs:** both tabs resume the same mock. Tab A saves, then tab B's stale save gets a 409, re-reads, retries once and shows the merge notice. Both answers end up on the server.
3. **Deadline while offline:** the deadline is moved to 4 s ahead and passes while offline. On reconnect the late save is refused with 409 and "Time is up" shows. A final submit that still carries the late answer is graded on saved answers only.
4. **Double submit:** two concurrent submits give exactly one 200 and one refusal, and only one attempt exists. A later retry and any further save return 409. A refresh does not resume the exam and the local resume copy is cleared.

Every scenario also checks that no key or explanation is sent before submit. Scenario 3 moves the deadline with `php artisan tinker` against the same SQLite file, so run the suite with the same DB environment variables as the server.

Run it like this (SQLite, so no live database is touched):

```bash
touch /tmp/e2e.sqlite
export DB_CONNECTION=sqlite DB_DATABASE=/tmp/e2e.sqlite SESSION_DRIVER=database CACHE_STORE=database
php artisan migrate --force
php artisan tinker --execute '
foreach (["Verbal Ability","Analytical Ability","Numerical Ability","General Information"] as $c) {
  $cat = App\Models\Category::factory()->create(["name"=>$c,"is_demographic"=>false]);
  $sub = App\Models\Subcategory::factory()->create(["category_id"=>$cat->id]);
  App\Models\Question::factory()->count(6)->create(["subcategory_id"=>$sub->id,"status"=>"active","options"=>["Alpha","Bravo","Charlie","Delta"],"correct_option"=>1]);
}'
npm run build && php artisan serve --port=8123 &
npm i --no-save playwright-core && node tests/E2E/strict-mock.e2e.mjs   # CHROME=/path/to/chrome
```

**Caution:** set the SQLite variables only for the server and E2E commands, never with `export` in the shell where you run `php artisan test`. Pest inherits them, runs against the E2E file and wipes its data, and CSRF checks then fail with 419.
