import { execFileSync } from 'node:child_process';
import { expect } from '@playwright/test';
import type { BrowserContext, Page, Response } from '@playwright/test';
import { assertThrowawayDb } from '../db-guard.mjs';

export type Served = { id: number; [key: string]: unknown };

/** Run PHP against the throwaway SQLite DB the app server uses (setup only). */
export function php(code: string): string {
    assertThrowawayDb(process.env);

    return execFileSync('php', ['artisan', 'tinker', '--execute', code], {
        env: process.env,
        encoding: 'utf8',
    }).trim();
}

export const isProgress = (r: Response) =>
    r.url().endsWith('/exams/sessions/progress');

export async function toasts(p: Page): Promise<string[]> {
    return p.locator('[data-sonner-toast]').allInnerTexts();
}

/** POST JSON from inside the page, with its CSRF token and cookies. */
export async function call(
    p: Page,
    url: string,
    body: unknown,
): Promise<{ status: number; body: any }> {
    return p.evaluate(
        async ([url, body]) => {
            const token =
                document
                    .querySelector('meta[name="csrf-token"]')
                    ?.getAttribute('content') ?? '';
            const r = await fetch(url as string, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json',
                    'X-CSRF-TOKEN': token,
                },
                body: JSON.stringify(body),
            });

            return { status: r.status, body: await r.json().catch(() => null) };
        },
        [url, body] as const,
    );
}

export const progress = (p: Page, sid: string) =>
    call(p, '/exams/sessions/progress', { exam_session_id: sid }).then(
        (r) => r.body,
    );

export const pending = (p: Page, sid: string) =>
    p.evaluate(
        (sid) => localStorage.getItem(`civio_strict_pending:${sid}`),
        sid,
    );

export const pick = (p: Page, label: string) =>
    p
        .locator('button', { hasText: new RegExp(`^[A-D]\\s*${label}$`) })
        .first()
        .click();

export async function waitForExam(p: Page) {
    await p
        .locator('button', { hasText: /Bravo$/ })
        .first()
        .waitFor();
    await p.waitForTimeout(500);
}

/** Start a Strict mock as a fresh guest; no key may reach the browser. */
export async function startStrict(ctx: BrowserContext) {
    const p = await ctx.newPage();
    await p.goto('/exams');
    await p.getByRole('button', { name: 'ACCEPT' }).click();
    await p.getByText('Exam Mode', { exact: true }).click();
    const created = p.waitForResponse(
        (r) =>
            r.url().endsWith('/exams/sessions') &&
            r.request().method() === 'POST',
    );
    await p.getByRole('button', { name: /Begin/ }).first().click();
    const session = await (await created).json();
    expect(session.mode).toBe('strict');

    for (const q of session.questions) {
        expect(q, 'no key before submit').not.toHaveProperty('correct_option');
        expect(q, 'no explanation before submit').not.toHaveProperty(
            'explanation',
        );
    }

    await waitForExam(p);

    return {
        p,
        sid: session.session_id as string,
        q: session.questions as Served[],
    };
}

export async function answerOnline(
    p: Page,
    label: string,
    qid: number,
    value: number,
) {
    const saved = p.waitForResponse(
        (r) =>
            isProgress(r) &&
            (r.request().postData() ?? '').includes(`"${qid}":${value}`),
    );
    await pick(p, label);

    return (await saved).json();
}
