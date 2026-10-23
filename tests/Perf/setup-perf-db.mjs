// Fresh throwaway SQLite for perf runs, seeded with enough unique items for a
// full 150-item Professional mock plus offline-eligible items for drill packs.
// Stems/options are synthetic (factory text), sized like real CSE items.
// Never touches a real database: same guard as the Strict Mock E2E.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import process from 'node:process';
import { assertThrowawayDb } from '../E2E/db-guard.mjs';

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
    `mt_srand(7); fake()->seed(7);
    $owner = App\\Models\\User::factory()->create();
    foreach (["Verbal Ability"=>80,"Analytical Ability"=>70,"Numerical Ability"=>70,"General Information"=>30,"Clerical Ability"=>60] as $c=>$n) {
        $cat = App\\Models\\Category::factory()->create(["name"=>$c,"is_demographic"=>false]);
        $sub = App\\Models\\Subcategory::factory()->create(["category_id"=>$cat->id]);
        for ($i = 0; $i < $n + 30; $i++) {
            App\\Models\\Question::factory()->create([
                "subcategory_id"=>$sub->id, "created_by"=>$owner->id, "status"=>"active",
                "language"=>($c === "Verbal Ability" && $i % 2) ? "fil" : "en",
                "stem"=>"Item $c $i: ".fake()->sentences(3, true)." Which option is correct?",
                "options"=>[fake()->sentence(5), fake()->sentence(5), fake()->sentence(5), fake()->sentence(5)],
                "correct_option"=>$i % 4, "explanation"=>fake()->paragraph(3),
                "offline_eligible"=>$i >= $n,
            ]);
        }
    }`,
);
console.log(`[perf] throwaway DB ready: ${db}`);
