import { execFileSync } from 'node:child_process';
import type { Page } from '@playwright/test';
import { assertThrowawayDb } from '../E2E/db-guard.mjs';

/** Reset rate-limit counters in the throwaway perf DB between runs. */
export function resetLimits() {
    assertThrowawayDb(process.env);
    execFileSync('php', ['artisan', 'cache:clear'], {
        env: process.env,
        stdio: 'ignore',
    });
}

export const firstOption = (p: Page) =>
    p.locator('button', { hasText: /^A\s*\S/ }).first();

/** /exams -> accept -> mode -> Begin -> first answer button visible + enabled. */
export async function openFirstQuestion(
    p: Page,
    mode: 'strict' | 'study' = 'strict',
) {
    const t0 = Date.now();
    await p.goto('/exams', { waitUntil: 'commit' });
    const accept = p.getByRole('button', { name: 'ACCEPT' });
    // A returning visitor with an unfinished mock is resumed straight into it.
    await accept.or(firstOption(p)).first().waitFor({ timeout: 120_000 });
    const tSetup = Date.now() - t0;

    if (!(await accept.isVisible())) {
        await waitEnabled(p);

        return {
            tSetup,
            tFirstQuestion: Date.now() - t0,
            session: null,
            resumed: true,
        };
    }

    await accept.click();

    if (mode === 'strict') {
        await p.getByText('Exam Mode', { exact: true }).click();
    }

    const created = p.waitForResponse(
        (r) =>
            r.url().endsWith('/exams/sessions') &&
            r.request().method() === 'POST',
        { timeout: 120_000 },
    );
    await p.getByRole('button', { name: /Begin/ }).first().click();
    const session = await (await created).json();
    await waitEnabled(p);

    return { tSetup, tFirstQuestion: Date.now() - t0, session, resumed: false };
}

async function waitEnabled(p: Page) {
    const opt = firstOption(p);
    await opt.waitFor({ timeout: 120_000 });
    await p.waitForFunction(
        (el) => !!el && !(el as HTMLButtonElement).disabled,
        await opt.elementHandle(),
        { timeout: 120_000 },
    );
}
