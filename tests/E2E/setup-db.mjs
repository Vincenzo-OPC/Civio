// Creates a fresh throwaway SQLite DB for the browser E2E, then seeds it.
// Runs before the app server starts (see playwright.config.ts).
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import { assertThrowawayDb } from './db-guard.mjs';

const db = assertThrowawayDb(process.env);
fs.rmSync(db, { force: true });
fs.writeFileSync(db, '');

const artisan = (...args) =>
    execFileSync('php', ['artisan', ...args], {
        env: process.env,
        stdio: 'inherit',
    });

artisan('migrate', '--force', '--no-interaction');
artisan(
    'tinker',
    '--execute',
    `foreach (["Verbal Ability","Analytical Ability","Numerical Ability","General Information"] as $c) {
        $cat = App\\Models\\Category::factory()->create(["name"=>$c,"is_demographic"=>false]);
        $sub = App\\Models\\Subcategory::factory()->create(["category_id"=>$cat->id]);
        App\\Models\\Question::factory()->count(6)->create(["subcategory_id"=>$sub->id,"status"=>"active","options"=>["Alpha","Bravo","Charlie","Delta"],"correct_option"=>1]);
    }`,
);
console.log(`[e2e] throwaway DB ready: ${db}`);
